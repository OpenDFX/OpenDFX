"""Check a board's release files against OpenDFX for Printed Circuit Boards.

Run:  python3 check_release.py RELEASE_FOLDER [--board BOARD.kicad_pcb] [--json]

RELEASE_FOLDER holds what you would send the fab and the assembler: the Gerber files, the drill files,
the IPC-D-356 netlist, the placement (XY) file and the BOM. Written for files exported from KiCad 10;
files from other design tools may be read wrongly.

With --board, it also runs KiCad's design rule check on the board (PCB-DFM-016), using the project's own
rules file, and compares the placement file with the board. That needs kicad-cli.

It prints a table with one row for each check: the recommendation, what was checked, a status and a note.
The statuses are the ones in "Using this book with an AI agent" (opendfx.org/00-start-here/05-using-this-book-with-an-ai-agent/):
  Met             the files follow the recommendation
  Not met         they don't; the note says what to fix
  Needs a person  only a person can check it, or the files don't say
It exits with 1 if any check is "Not met".

To export a release that follows the book from KiCad 10, run these from your project's folder, in bash or zsh.
myboard is your project's name. Keep the quotation marks. The double quotation marks let a path have spaces in it.
The single quotation marks stop the shell from changing KiCad's field names ${QUANTITY} and ${DNP}.
  kicad-cli pcb export gerbers --no-protel-ext -o "release/" "myboard.kicad_pcb"
  kicad-cli pcb export drill --excellon-separate-th --excellon-zeros-format keep -o "release/" "myboard.kicad_pcb"
  kicad-cli pcb export ipcd356 -o "release/myboard.d356" "myboard.kicad_pcb"
  kicad-cli pcb export pos --format ascii --units mm --side both -o "release/myboard-pos.txt" "myboard.kicad_pcb"
  kicad-cli sch export bom --ref-range-delimiter "" --fields 'Reference,Value,Footprint,${QUANTITY},Manufacturer,MPN,MSL,Alternates,${DNP}' --labels 'Reference,Value,Footprint,Qty,Manufacturer,MPN,MSL,Alternates,DNP' --group-by 'Value,Footprint,MPN' -o "release/myboard-bom.csv" "myboard.kicad_sch"
These commands are tested in bash and zsh. They haven't been tested in Windows PowerShell or Command Prompt.
The BOM fields Manufacturer, MPN, MSL and Alternates must exist on your symbols.

From OpenDFX for Printed Circuit Boards by Chris Denney, https://opendfx.org. Licensed under the MIT License (LICENSE-CODE).
"""
import csv
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SITE = "opendfx.org"
MET, NOT_MET, PERSON = "Met", "Not met", "Needs a person"


class Report:
    def __init__(self):
        self.rows = []

    def add(self, rec_id, what, status, note=""):
        self.rows.append({"id": rec_id, "address": f"https://{SITE}/{rec_id}", "check": what, "status": status, "note": note})

    def markdown(self):
        out = ["| Recommendation | What was checked | Status | Note |", "|---|---|---|---|"]
        for r in self.rows:
            note = r["note"].replace("|", "\\|")
            out.append(f"| [{r['id']}]({r['address']}) | {r['check']} | {r['status']} | {note} |")
        counts = {s: sum(r["status"] == s for r in self.rows) for s in (MET, NOT_MET, PERSON)}
        out.append("")
        out.append(f"{counts[MET]} met, {counts[NOT_MET]} not met, {counts[PERSON]} need a person.")
        return "\n".join(out)


# ---------- Gerber files ----------

KICAD_NAMES = {  # without X2 attributes, recognize KiCad's own file names
    "F_Cu": "Copper,L1,Top", "B_Cu": "Copper,Ln,Bot", "F_Mask": "Soldermask,Top", "B_Mask": "Soldermask,Bot",
    "F_Silkscreen": "Legend,Top", "B_Silkscreen": "Legend,Bot", "F_SilkS": "Legend,Top", "B_SilkS": "Legend,Bot",
    "F_Paste": "Paste,Top", "B_Paste": "Paste,Bot", "Edge_Cuts": "Profile",
}


def function_from_name(name):
    m = re.search(r"In(\d+)_Cu", name)
    if m:
        return f"Copper,L{int(m.group(1)) + 1},Inr"
    for token, function in KICAD_NAMES.items():
        if token in name:
            return function
    return ""


class Gerber:
    """Just enough of a Gerber file to check it: attributes, units, apertures and flashed pads."""

    def __init__(self, path):
        self.path = path
        self.text = path.read_text(errors="replace")
        self.attrs = dict(re.findall(r"%TF\.(\w+),([^*]*)\*%", self.text))
        self.x2 = bool(self.attrs)
        self.function = self.attrs.get("FileFunction", "") or function_from_name(path.name)
        fs = re.search(r"%FSLAX(\d)(\d)Y\d\d\*%", self.text)
        self.decimals = int(fs.group(2)) if fs else 6
        self.scale = 25.4 if "%MOIN*%" in self.text else 1.0
        self.apertures, self.functions = {}, {}
        self.flashes = []   # (x, y, aperture definition, aperture function)
        self.points = []    # every coordinate, for the board outline's extents
        self._read()

    def _read(self):
        function = ""
        current = None
        x = y = 0
        for block in re.split(r"\*%?\s*%?", self.text):
            block = block.strip()
            m = re.match(r"TA\.AperFunction,(.*)", block)
            if m:
                function = m.group(1)
                continue
            if block.startswith("TD"):
                function = ""
                continue
            m = re.match(r"ADD(\d+)(.*)", block)
            if m:
                self.apertures[m.group(1)] = m.group(2)
                self.functions[m.group(1)] = function
                continue
            m = re.match(r"(?:G54)?D(\d+)$", block)
            if m and int(m.group(1)) >= 10:
                current = m.group(1)
                continue
            m = re.match(r"(?:G0?[123])?(?:X(-?\d+))?(?:Y(-?\d+))?(?:I-?\d+)?(?:J-?\d+)?D0?([123])$", block)
            if m and (m.group(1) or m.group(2)):
                if m.group(1):
                    x = int(m.group(1)) / 10 ** self.decimals * self.scale
                if m.group(2):
                    y = int(m.group(2)) / 10 ** self.decimals * self.scale
                self.points.append((x, y))
                if m.group(3) == "3" and current:
                    self.flashes.append((round(x, 4), round(y, 4), self.apertures.get(current, ""), self.functions.get(current, "")))


def aperture_size(definition):
    """Outer width and height of a pad's aperture, in the file's units, or None if the shape isn't known.
    Comparing sizes, not text, means two ways of writing the same shape count as the same."""
    m = re.match(r"([A-Za-z]+),(.*)", definition)
    if not m:
        return None
    shape, params = m.group(1), [float(v) for v in re.findall(r"-?[\d.]+", m.group(2))]
    if shape == "C" and params:
        return (params[0], params[0])
    if shape in ("R", "O") and len(params) >= 2:
        return (params[0], params[1])
    if shape == "RoundRect" and len(params) >= 9:
        radius, xs, ys = params[0], params[1:9:2], params[2:9:2]
        return (max(xs) - min(xs) + 2 * radius, max(ys) - min(ys) + 2 * radius)
    return None


def same_aperture(a, b):
    if a == b:
        return True
    sa, sb = aperture_size(a), aperture_size(b)
    return bool(sa and sb) and abs(sa[0] - sb[0]) < 0.005 and abs(sa[1] - sb[1]) < 0.005


# ---------- Drill files ----------

class Drill:
    def __init__(self, path):
        self.path = path
        self.text = path.read_text(errors="replace")
        self.function = (re.search(r"TF\.FileFunction,([^\n*]*)", self.text) or [None, ""])[1]
        self.metric = "METRIC" in self.text
        self.inch = re.search(r"^INCH", self.text, re.M) is not None
        fmt = re.search(r"FORMAT=\{([^}]*)\}", self.text)
        self.format = fmt.group(1) if fmt else ""
        self.holes = self._holes()

    def _holes(self):
        digits = re.match(r"(\d):(\d)", self.format)
        int_d, dec_d = (int(digits.group(1)), int(digits.group(2))) if digits else ((3, 3) if self.metric else (2, 4))
        trailing = "suppress trailing" in self.format
        scale = 25.4 if self.inch else 1.0
        holes = []
        body = self.text.split("%", 1)[-1]
        for line in body.splitlines():
            m = re.match(r"X(-?[\d.]+)Y(-?[\d.]+)", line)
            if not m:
                continue
            values = []
            for raw in m.groups():
                if "." in raw:
                    values.append(float(raw) * scale)
                    continue
                sign = -1 if raw.startswith("-") else 1
                raw = raw.lstrip("-")
                if trailing:
                    raw = raw.ljust(int_d + dec_d, "0")
                values.append(sign * int(raw) / 10 ** dec_d * scale)
            holes.append(tuple(values))
        return holes


# ---------- Placement (XY) file and BOM ----------

def read_placement(path):
    text = path.read_text(errors="replace")
    header = [l for l in text.splitlines() if l.startswith("#")]
    rows = []
    if path.suffix.lower() == ".csv":
        for row in csv.DictReader(text.splitlines()):
            rows.append({"ref": row.get("Ref", ""), "x": row.get("PosX"), "y": row.get("PosY"), "side": row.get("Side", "")})
    else:
        for line in text.splitlines():
            if line.startswith("#") or not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 5:  # the value and package columns can be blank
                rows.append({"ref": parts[0], "x": parts[-4], "y": parts[-3], "side": parts[-1]})
    return header, rows


def expand_refs(text):
    """'R1,R2-R4' or 'R1 R2' -> ['R1', 'R2', 'R3', 'R4']."""
    refs = []
    for part in re.split(r"[,\s;]+", text.strip()):
        m = re.match(r"([A-Za-z_]+)(\d+)-(?:[A-Za-z_]+)?(\d+)$", part)
        if m:
            refs += [f"{m.group(1)}{n}" for n in range(int(m.group(2)), int(m.group(3)) + 1)]
        elif part:
            refs.append(part)
    return refs


def find_column(header, names):
    for col in header:
        key = re.sub(r"[^a-z]", "", col.lower())
        if any(key == n or key.startswith(n) for n in names):
            return col
    return None


# ---------- The checks ----------

def check(folder, board=None):
    r = Report()
    files = [p for p in sorted(folder.iterdir()) if p.is_file()]
    gerbers = []
    for p in files:
        head = p.read_text(errors="replace")[:4000] if p.stat().st_size < 50_000_000 else ""
        if "%FSLA" in head or "%TF." in head:
            gerbers.append(Gerber(p))
    drills = [Drill(p) for p in files if p.suffix.lower() in (".drl", ".xln", ".exc", ".txt") and "M48" in p.read_text(errors="replace")[:200]]
    gerber_drills = [g for g in gerbers if g.function.startswith(("Plated", "NonPlated"))]
    layers = [g for g in gerbers if g not in gerber_drills]
    job = next((p for p in files if p.suffix == ".gbrjob"), None)
    job_data = json.loads(job.read_text()) if job else {}

    # PCB-DFM-008: one complete package, Gerber X2, .gbr, from one revision
    if not layers:
        r.add("PCB-DFM-008", "Gerber files", NOT_MET, "No Gerber files found.")
        return r
    no_x2 = [g.path.name for g in layers if not g.x2]
    r.add("PCB-DFM-008", "Gerber X2 attributes in every Gerber file", NOT_MET if no_x2 else MET,
          f"No X2 attributes in: {', '.join(no_x2)}." if no_x2 else f"{len(layers)} Gerber files, all with X2 attributes.")
    odd = [g.path.name for g in layers if g.path.suffix.lower() != ".gbr"]
    r.add("PCB-DFM-008", "The standard .gbr file extension", NOT_MET if odd else MET,
          f"Rename or re-export with the .gbr extension (KiCad: --no-protel-ext): {', '.join(odd[:6])}{' …' if len(odd) > 6 else ''}." if odd else "")
    funcs = [g.function for g in layers]
    copper = sorted({f.split(",")[1] for f in funcs if f.startswith("Copper,")})
    count = job_data.get("GeneralSpecs", {}).get("LayerNumber") or len(copper)
    if any(",Ln," in f for f in funcs):  # named from the file, not numbered: the bottom layer is the last one
        funcs = [f.replace("Copper,Ln,", f"Copper,L{count},") for f in funcs]
    needed = {f"Copper,L{i}": f"copper layer {i}" for i in range(1, int(count) + 1)}
    needed.update({"Soldermask,Top": "top solder mask", "Soldermask,Bot": "bottom solder mask",
                   "Legend,Top": "top legend", "Legend,Bot": "bottom legend",
                   "Paste,Top": "top paste", "Paste,Bot": "bottom paste", "Profile": "board outline"})
    missing = [name for key, name in needed.items() if not any(f.startswith(key) for f in funcs)]
    r.add("PCB-DFM-008", "Every copper layer, both solder masks, both legends, both paste layers and the outline",
          NOT_MET if missing else MET, f"Missing: {', '.join(missing)}." if missing else f"{count} copper layers and all the other layers are there.")
    projects = {g.attrs.get("ProjectId") for g in layers if g.attrs.get("ProjectId")}
    times = []
    for item in layers + drills:
        m = re.search(r"TF\.CreationDate,([0-9T:+\-]+)", item.text)
        if m:
            try:
                times.append(datetime.fromisoformat(m.group(1)))
            except ValueError:
                pass
    spread = (max(times) - min(times)).total_seconds() / 60 if len(times) > 1 else 0
    if len(projects) > 1:
        r.add("PCB-DFM-008", "All files from one design and one revision", NOT_MET, f"The Gerber files name {len(projects)} different projects or revisions.")
    elif spread > 30:
        r.add("PCB-DFM-008", "All files from one design and one revision", NOT_MET, f"The files were made {spread:.0f} minutes apart. Export them all again together.")
    else:
        r.add("PCB-DFM-008", "All files from one design and one revision", MET, "One project, and all files exported together.")

    # PCB-DFM-009: netlist
    netlists = [p for p in files if p.suffix.lower() in (".d356", ".ipc", ".net356") or "IPC-D-356" in p.read_text(errors="replace")[:2000]]
    r.add("PCB-DFM-009", "An IPC-D-356 netlist", MET if netlists else NOT_MET,
          netlists[0].name if netlists else "Export one with the Gerbers (KiCad: kicad-cli pcb export ipcd356).")

    # PCB-DFM-011: separate plated and non-plated holes; unambiguous format; same origin
    all_drills = drills + gerber_drills
    if not all_drills:
        r.add("PCB-DFM-011", "Drill files", NOT_MET, "No drill files found.")
    else:
        plated = [d for d in all_drills if d.function.startswith("Plated")]
        nonplated = [d for d in all_drills if d.function.startswith("NonPlated")]
        mixed = [d.path.name for d in all_drills if "Mixed" in d.function or not d.function]
        ok = plated and nonplated and not mixed
        r.add("PCB-DFM-011", "Plated and non-plated holes in separate drill files", MET if ok else NOT_MET,
              "" if ok else f"Export them separately (KiCad: --excellon-separate-th). Mixed or unlabeled: {', '.join(mixed) or 'none'}.")
        bad = []
        for d in drills:
            if not (d.metric or d.inch):
                bad.append(f"{d.path.name} doesn't state its units")
            elif "decimal" in d.format:
                continue
            elif d.metric and not d.format.startswith("3:3"):
                bad.append(f"{d.path.name} is metric {d.format.split('/')[0].strip()}, not 3:3")
            elif d.inch and not d.format.startswith("2:4"):
                bad.append(f"{d.path.name} is inch {d.format.split('/')[0].strip()}, not 2:4")
            elif not re.search(r"keep zeros|suppress leading|suppress trailing", d.format):
                bad.append(f"{d.path.name} doesn't state its zero suppression")
        r.add("PCB-DFM-011", "Excellon format 3:3 metric or 2:4 inch, with units and zeros stated", NOT_MET if bad else MET,
              "; ".join(bad) + "." if bad else "")
        outline = next((g for g in layers if g.function.startswith("Profile")), None)
        holes = [h for d in drills for h in d.holes]
        if outline and outline.points and holes:
            xs, ys = [p[0] for p in outline.points], [p[1] for p in outline.points]
            box = (min(xs) - 0.5, min(ys) - 0.5, max(xs) + 0.5, max(ys) + 0.5)
            outside = [h for h in holes if not (box[0] <= h[0] <= box[2] and box[1] <= h[1] <= box[3])]
            r.add("PCB-DFM-011", "Drill files use the same origin as the Gerber files", NOT_MET if outside else MET,
                  f"{len(outside)} of {len(holes)} holes fall outside the board outline. Use the same origin for drill files and Gerbers." if outside else f"All {len(holes)} holes are inside the board outline.")

    # PCB-DFM-016: design rule check
    if board:
        report = folder / ".opendfx-drc.json"
        subprocess.run(["kicad-cli", "pcb", "drc", "--format", "json", "--severity-error", "-o", str(report), str(board)], capture_output=True)
        try:
            drc = json.loads(report.read_text())
            errors = len(drc.get("violations", []))
            unconnected = len(drc.get("unconnected_items", []))
            report.unlink()
            ok = errors == 0 and unconnected == 0
            r.add("PCB-DFM-016", "No design rule errors and no unconnected nets", MET if ok else NOT_MET,
                  f"{errors} errors and {unconnected} unconnected items." + ("" if (board.with_suffix(".kicad_dru")).exists() else " The project has no rules file, so only KiCad's own rules were checked; add opendfx.kicad_dru."))
        except (OSError, ValueError):
            r.add("PCB-DFM-016", "No design rule errors and no unconnected nets", PERSON, "kicad-cli couldn't run the design rule check.")
    else:
        r.add("PCB-DFM-016", "No design rule errors and no unconnected nets", PERSON, "Run again with --board to check, or run KiCad's design rule check yourself.")

    # PCB-DFA-018 and PCB-DFA-019: paste 1:1 with copper, and none on test pads
    for side in ("Top", "Bot"):
        cu = next((g for g in layers if g.function.startswith("Copper,") and g.function.endswith(side)), None)
        paste = next((g for g in layers if g.function.startswith("Paste," + side)), None)
        if not cu or not paste:
            continue
        pads = {(x, y): (ap, fn) for x, y, ap, fn in cu.flashes}
        differ, testpads = [], []
        for x, y, ap, _ in paste.flashes:
            if (x, y) not in pads:
                continue
            cu_ap, fn = pads[(x, y)]
            if not same_aperture(ap, cu_ap):
                differ.append((x, y))
            if fn.startswith("TestPad"):
                testpads.append((x, y))
        name = "top" if side == "Top" else "bottom"
        if paste.flashes:
            r.add("PCB-DFA-018", f"Paste openings the same size and shape as their pads, {name}", NOT_MET if differ else MET,
                  f"{len(differ)} of {len(paste.flashes)} paste openings differ from their pads, for example at X {differ[0][0]:.2f} mm, Y {differ[0][1]:.2f} mm. Set the paste margins to zero." if differ else f"{len(paste.flashes)} paste openings checked.")
        if testpads:
            r.add("PCB-DFA-019", f"No paste on test pads, {name}", NOT_MET, f"{len(testpads)} test pads have paste. Remove it, unless the finish is OSP.")
    r.add("PCB-DFA-019", "Paste on every pad that should be soldered", PERSON, "Check the paste layers pad by pad. Only you know which pads must stay bare.")

    # PCB-DFA-064 and PCB-DFA-066: placement file
    placement = next((p for p in files if re.search(r"(pos|xy|centroid|place)", p.stem, re.I) and p.suffix.lower() in (".txt", ".csv", ".pos")), None)
    refs_xy, excluded = [], []
    if not placement:
        r.add("PCB-DFA-064", "A placement (XY) file", NOT_MET, "No placement file found. Export one (KiCad: kicad-cli pcb export pos --units mm --side both).")
    else:
        header, rows = read_placement(placement)
        refs_xy = [row["ref"] for row in rows]
        unit = next((l for l in header if "Unit" in l), "")
        if "mm" in unit:
            r.add("PCB-DFA-064", "Placement file in millimeters, with its units stated", MET, placement.name)
        elif "in" in unit.lower():
            r.add("PCB-DFA-064", "Placement file in millimeters, with its units stated", NOT_MET, "The file is in inches. Export it in millimeters (KiCad: --units mm).")
        else:
            r.add("PCB-DFA-064", "Placement file in millimeters, with its units stated", NOT_MET, "The file doesn't state its units. Use KiCad's ASCII format with --units mm, which states them in the header.")
        sides = {row["side"].lower() for row in rows}
        side_line = next((l for l in header if "Side" in l), "")
        both = ("top" in sides and "bottom" in sides) or "All" in side_line
        r.add("PCB-DFA-064", "Parts on both sides listed", MET if both else PERSON,
              "" if both else f"Only {', '.join(sorted(sides)) or 'no'} side parts are listed. Check whether the board has parts on the other side.")
        r.add("PCB-DFA-064", "The origin stated", PERSON, "Say where the origin is, in the file header or the assembly notes.")
        outline = next((g for g in layers if g.function.startswith("Profile")), None)
        if outline and outline.points and rows:
            xs, ys = [p[0] for p in outline.points], [p[1] for p in outline.points]
            outside = 0
            for row in rows:
                try:
                    x, y = float(row["x"]), float(row["y"])
                except (TypeError, ValueError):
                    continue
                if "mm" not in unit:
                    break
                if not (min(xs) - 0.5 <= x <= max(xs) + 0.5 and min(ys) - 0.5 <= y <= max(ys) + 0.5):
                    outside += 1
            if "mm" in unit:
                r.add("PCB-DFA-064", "Placement file uses the same origin as the Gerber files", NOT_MET if outside else MET,
                      f"{outside} parts fall outside the board outline." if outside else "")
        dupes = sorted({x for x in refs_xy if refs_xy.count(x) > 1})
        long_refs = [x for x in refs_xy if len(x) > 8]
        r.add("PCB-DFA-066", "Unique reference designators of 8 characters or fewer", NOT_MET if dupes or long_refs else MET,
              " ".join(filter(None, [f"Repeated: {', '.join(dupes[:8])}." if dupes else "", f"Longer than 8 characters: {', '.join(long_refs[:8])}." if long_refs else ""])))
        excluded = []
        if board:
            on_board = board_refs(board)
            if on_board is not None:
                placed, excluded = on_board
                gone = sorted(set(placed) - set(refs_xy))
                r.add("PCB-DFA-064", "Every part on the board, including do-not-place parts, in the placement file", NOT_MET if gone else MET,
                      f"Missing: {', '.join(gone[:10])}. Keep do-not-place parts in the file; mark them in the BOM." if gone else "")
                if excluded:
                    r.add("PCB-DFA-064", "Footprints left out of the placement file on purpose", PERSON,
                          f"{', '.join(sorted(excluded)[:12])} are set to be left out. That's right for logos, mounting holes and jumpers, but every part the assembler places should be in the file.")

    # PCB-DFA-068, 069, 071 and 091: BOM
    bom_path = next((p for p in files if p.suffix.lower() == ".csv" and re.search(r"bom|bill", p.stem, re.I)), None)
    if not bom_path:
        r.add("PCB-DFA-068", "A BOM", NOT_MET, "No BOM found. Send it as CSV, with 'bom' in the file name.")
    else:
        rows = list(csv.DictReader(bom_path.read_text(errors="replace").splitlines()))
        header = list(rows[0].keys()) if rows else []
        cols = {
            "refs": find_column(header, ["reference", "refdes", "designator", "refs", "ref"]),
            "qty": find_column(header, ["qty", "quantity"]),
            "mfr": find_column(header, ["manufacturer", "mfr", "mfg", "maker"]),
            "mpn": find_column(header, ["mpn", "manufacturerpartnumber", "mfrpart", "mfgpart", "partnumber"]),
            "desc": find_column(header, ["description", "value", "desc"]),
            "dnp": find_column(header, ["dnp", "donotplace", "donotpopulate", "fitted", "populate"]),
            "msl": find_column(header, ["msl", "moisture"]),
            "alt": find_column(header, ["alternate", "alternative", "alt", "locked", "substitut"]),
        }
        if cols["mfr"] == cols["mpn"]:
            cols["mfr"] = None
        labels = {"refs": "reference designators", "qty": "quantity", "mfr": "manufacturer", "mpn": "manufacturer's part number", "desc": "description or value"}
        absent = [labels[k] for k in labels if not cols[k]]
        r.add("PCB-DFA-068", "BOM columns: designators, quantity, manufacturer, part number, description", NOT_MET if absent else MET,
              f"Missing columns: {', '.join(absent)}." if absent else bom_path.name)

        def is_dnp(row):
            value = (row.get(cols["dnp"]) or "").strip().lower() if cols["dnp"] else ""
            return value not in ("", "no", "n", "false", "0", "fitted", "yes-fit")

        if cols["mfr"] and cols["mpn"]:
            empty = [expand_refs(row.get(cols["refs"]) or "?")[0] for row in rows if not is_dnp(row) and not ((row.get(cols["mfr"]) or "").strip() and (row.get(cols["mpn"]) or "").strip())]
            r.add("PCB-DFA-068", "Manufacturer and part number on every fitted line", NOT_MET if empty else MET,
                  f"{len(empty)} of {len(rows)} lines have no manufacturer or part number, for example the lines for {', '.join(empty[:3])}." if empty else "")
        refs_bom = []
        if cols["refs"]:
            wrong_qty = []
            for row in rows:
                refs = expand_refs(row.get(cols["refs"]) or "")
                refs_bom += refs
                if cols["qty"]:
                    try:
                        if int(float(row.get(cols["qty"]) or 0)) != len(refs):
                            wrong_qty.append(refs[0] if refs else "?")
                    except ValueError:
                        pass
            if wrong_qty:
                r.add("PCB-DFA-068", "Quantity matches the designators on each line", NOT_MET, f"Lines starting {', '.join(wrong_qty[:5])} have a quantity that doesn't match their designators.")
            if refs_xy:
                only_bom = sorted(set(refs_bom) - set(refs_xy) - set(excluded))
                only_xy = sorted(set(refs_xy) - set(refs_bom))
                ok = not only_bom and not only_xy
                r.add("PCB-DFA-068", "BOM designators match the placement file exactly", MET if ok else NOT_MET,
                      "" if ok else " ".join(filter(None, [f"Only in the BOM: {', '.join(only_bom[:10])}." if only_bom else "",
                                                           f"Only in the placement file: {', '.join(only_xy[:10])}." if only_xy else ""])))
        r.add("PCB-DFA-069", "Each line marked locked or with alternates", MET if cols["alt"] else NOT_MET,
              "" if cols["alt"] else "Add a column saying which lines are locked to one part, and list alternates for the rest.")
        r.add("PCB-DFA-071", "Do-not-place lines marked", MET if cols["dnp"] else NOT_MET,
              "" if cols["dnp"] else "Add a DNP column, and keep do-not-place parts on the BOM.")
        if cols["msl"]:
            blank = [row for row in rows if not is_dnp(row) and not (row.get(cols["msl"]) or "").strip()]
            r.add("PCB-DFA-091", "A moisture sensitivity level (MSL) for each part", PERSON if blank else MET,
                  f"{len(blank)} fitted lines have no MSL. Fill it in from each datasheet, or write N/A for parts that don't have one." if blank else "")
        else:
            r.add("PCB-DFA-091", "A moisture sensitivity level (MSL) for each part", NOT_MET, "Add an MSL column, filled in from each part's datasheet.")
        long_bom = sorted({x for x in refs_bom if len(x) > 8}) if cols["refs"] else []
        if long_bom:
            r.add("PCB-DFA-066", "BOM reference designators of 8 characters or fewer", NOT_MET, f"Longer than 8 characters: {', '.join(long_bom[:8])}.")
        r.add("PCB-DFA-070", "Every value and part number checked, and every part still made", PERSON, "Check each line against what you meant, and each part's lifecycle and stock with a distributor.")

    # Things only a drawing or a person can say
    finish = job_data.get("GeneralSpecs", {}).get("Finish")
    r.add("PCB-DFM-036", "Surface finish named", PERSON,
          ("The board's setup names no finish. " if finish in (None, "", "None") else f"The board's setup says {finish}. ") + "Name it on the fabrication drawing and in the order.")
    r.add("PCB-DFM-014", "A fabrication drawing", PERSON, "Check it gives the class, material, thickness, copper weights, stack-up, finish, colors and via treatment.")
    r.add("PCB-DFA-067", "An assembly drawing, where the files can't show something", PERSON, "Check for bent leads, hardware and torque, heights, glue and coating keep-outs.")
    return r


def board_refs(board):
    """(placed, excluded): reference designators of the footprints on the board, read from the .kicad_pcb file.
    Excluded footprints are set to be left out of placement files (logos, mounting holes, jumpers)."""
    try:
        text = Path(board).read_text(errors="replace")
    except OSError:
        return None
    placed, excluded = [], []
    for block in re.split(r"\n\t\(footprint ", text)[1:]:
        ref = re.search(r'\(property "Reference" "([^"]+)"', block)
        if not ref:
            continue
        attr = re.search(r"\(attr ([^)]*)\)", block)
        if attr and ("exclude_from_pos_files" in attr.group(1) or "board_only" in attr.group(1)):
            excluded.append(ref.group(1))
        else:
            placed.append(ref.group(1))
    return placed, excluded


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if args else 2)
    folder = Path(args[0])
    board = Path(args[args.index("--board") + 1]) if "--board" in args else None
    if not folder.is_dir():
        sys.exit(f"Not a folder: {folder}")
    report = check(folder, board)
    print(json.dumps(report.rows, indent=2) if "--json" in args else report.markdown())
    sys.exit(1 if any(row["status"] == NOT_MET for row in report.rows) else 0)


if __name__ == "__main__":
    main()

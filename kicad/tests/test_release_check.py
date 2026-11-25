"""Prove that kicad/check_release.py passes a good release and catches each mistake (Q155).

Run: python3 kicad/tests/test_release_check.py

Needs KiCad 10 (pcbnew and kicad-cli). It draws a small two-sided board, exports a release the way the book
recommends, and writes a BOM for it. Every check must then be "Met" or "Needs a person". Then it makes one
mistake at a time, re-runs the checker, and expects exactly that check to say "Not met".
"""
import csv
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pcbnew
from pcbnew import VECTOR2I
from pcbnew import FromMM as mm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import check_release as cr  # noqa: E402

NAME = "release-test"
PARTS = [  # reference, side, x, y
    ("R1", "top", 10, 10), ("R2", "top", 14, 10), ("C1", "top", 18, 10),
    ("C2", "bottom", 10, 20), ("U1", "bottom", 16, 20),
]


def V(x, y):
    return VECTOR2I(mm(x), mm(y))


def make_board(path, paste_margin=0.0, testpad_paste=False):
    board = pcbnew.NewBoard(str(path))
    for x1, y1, x2, y2 in [(0, 0, 30, 0), (30, 0, 30, 30), (30, 30, 0, 30), (0, 30, 0, 0)]:
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(V(x1, y1))
        s.SetEnd(V(x2, y2))
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(mm(0.1))
        board.Add(s)
    for ref, side, x, y in PARTS:
        f = pcbnew.FOOTPRINT(board)
        f.SetReference(ref)
        f.SetValue("1k")
        f.SetAttributes(pcbnew.FP_SMD)
        f.SetPosition(V(x, y))
        board.Add(f)
        for i, dx in enumerate((-0.75, 0.75)):
            p = pcbnew.PAD(f)
            p.SetNumber(str(i + 1))
            p.SetAttribute(pcbnew.PAD_ATTRIB_SMD)
            p.SetShape(pcbnew.PAD_SHAPE_RECTANGLE)
            p.SetSize(VECTOR2I(mm(0.9), mm(1.0)))
            p.SetLayerSet(p.SMDMask())
            if paste_margin and ref == "R1":
                p.SetLocalSolderPasteMargin(mm(paste_margin))
            f.Add(p)
            p.SetPosition(V(x + dx, y))
        if side == "bottom":
            f.Flip(f.GetPosition(), pcbnew.FLIP_DIRECTION_TOP_BOTTOM)
    # A test point, a plated through-hole part and a non-plated mounting hole.
    tp = pcbnew.FOOTPRINT(board)
    tp.SetReference("TP1")
    tp.SetAttributes(pcbnew.FP_SMD)
    tp.SetPosition(V(24, 10))
    board.Add(tp)
    p = pcbnew.PAD(tp)
    p.SetNumber("1")
    p.SetAttribute(pcbnew.PAD_ATTRIB_SMD)
    p.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
    p.SetSize(VECTOR2I(mm(1.0), mm(1.0)))
    p.SetProperty(pcbnew.PAD_PROP_TESTPOINT)
    layers = p.SMDMask() if testpad_paste else pcbnew.LSET()
    if not testpad_paste:
        layers.AddLayer(pcbnew.F_Cu)
        layers.AddLayer(pcbnew.F_Mask)
    p.SetLayerSet(layers)
    tp.Add(p)
    p.SetPosition(V(24, 10))
    j = pcbnew.FOOTPRINT(board)
    j.SetReference("J1")
    j.SetAttributes(pcbnew.FP_THROUGH_HOLE)
    j.SetPosition(V(22, 22))
    board.Add(j)
    for i in range(2):
        p = pcbnew.PAD(j)
        p.SetNumber(str(i + 1))
        p.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
        p.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
        p.SetSize(VECTOR2I(mm(1.7), mm(1.7)))
        p.SetDrillSize(VECTOR2I(mm(1.0), mm(1.0)))
        p.SetLayerSet(p.PTHMask())
        j.Add(p)
        p.SetPosition(V(22 + 2.54 * i, 22))
    h = pcbnew.FOOTPRINT(board)
    h.SetReference("H1")
    h.SetAttributes(pcbnew.FP_EXCLUDE_FROM_POS_FILES | pcbnew.FP_EXCLUDE_FROM_BOM)
    h.SetPosition(V(4, 26))
    board.Add(h)
    p = pcbnew.PAD(h)
    p.SetAttribute(pcbnew.PAD_ATTRIB_NPTH)
    p.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
    p.SetSize(VECTOR2I(mm(3.2), mm(3.2)))
    p.SetDrillSize(VECTOR2I(mm(3.2), mm(3.2)))
    p.SetLayerSet(p.UnplatedHoleMask())
    h.Add(p)
    p.SetPosition(V(4, 26))
    pcbnew.SaveBoard(str(path), board)


def cli(*args):
    subprocess.run(["kicad-cli", "pcb", "export", *args], check=True, capture_output=True)


def export(board, out, gerber_opts=(), drill_opts=("--excellon-separate-th", "--excellon-zeros-format", "keep"),
           pos_opts=("--format", "ascii", "--units", "mm", "--side", "both"), netlist=True):
    out.mkdir(parents=True, exist_ok=True)
    cli("gerbers", "--no-protel-ext", *gerber_opts, "-o", str(out) + "/", str(board))
    cli("drill", *drill_opts, "-o", str(out) + "/", str(board))
    suffix = ".csv" if "csv" in pos_opts else ".txt"
    cli("pos", *pos_opts, "-o", str(out / f"{NAME}-pos{suffix}"), str(board))
    if netlist:
        cli("ipcd356", "-o", str(out / f"{NAME}.d356"), str(board))


def write_bom(out, drop=(), refs=None, long_ref=False):
    columns = [c for c in ["Reference", "Qty", "Manufacturer", "MPN", "Value", "MSL", "Alternates", "DNP"] if c not in drop]
    lines = [
        {"Reference": "R1,R2", "Qty": "2", "Manufacturer": "Maker A", "MPN": "RES-1K-0603", "Value": "1k", "MSL": "1", "Alternates": "Any 1k 1% 0603", "DNP": ""},
        {"Reference": "C1,C2", "Qty": "2", "Manufacturer": "Maker B", "MPN": "CAP-100N-0603", "Value": "100n", "MSL": "1", "Alternates": "Any 100n X7R 0603", "DNP": ""},
        {"Reference": "U1", "Qty": "1", "Manufacturer": "Maker C", "MPN": "CHIP-01", "Value": "MCU", "MSL": "3", "Alternates": "Locked: firmware", "DNP": ""},
        {"Reference": "J1", "Qty": "1", "Manufacturer": "Maker D", "MPN": "HDR-2", "Value": "Header", "MSL": "N/A", "Alternates": "Any 2.54 mm header", "DNP": ""},
        {"Reference": "TP1", "Qty": "1", "Manufacturer": "", "MPN": "", "Value": "Test point", "MSL": "", "Alternates": "", "DNP": "DNP"},
    ]
    if refs is not None:
        lines = [l for l in lines if l["Reference"] in refs]
    if long_ref:
        lines[0]["Reference"] = "R1,R2_TOOLONG1"
    if "empty-mpn" in drop:
        lines[2]["MPN"] = ""
    with open(out / f"{NAME}-bom.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        w.writeheader()
        w.writerows(lines)


def status(rows, words):
    hits = [r["status"] for r in rows if words in r["check"]]
    return hits


def main():
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        board = tmp / f"{NAME}.kicad_pcb"
        make_board(board)
        good = tmp / "good"
        export(board, good)
        write_bom(good)
        rows = cr.check(good, board).rows
        bad = [r for r in rows if r["status"] == cr.NOT_MET and "design rule" not in r["check"]]
        for r in bad:
            failures.append(f"GOOD RELEASE  {r['id']} {r['check']}: {r['note']}")
        print(f"Good release: {sum(r['status'] == cr.MET for r in rows)} met, {len(bad)} not met.")

        def case(label, folder, words, board_path=None, also=()):
            rows = cr.check(folder, board_path).rows
            got = status(rows, words)
            if cr.NOT_MET not in got:
                failures.append(f"MISSED  {label}: expected '{words}' to be Not met, got {got or 'no such check'}")
            others = [r for r in rows if r["status"] == cr.NOT_MET and words not in r["check"] and "design rule" not in r["check"]
                      and not any(a in r["check"] for a in also)]
            for r in others:
                failures.append(f"EXTRA   {label}: also Not met: {r['check']}")

        def variant(name, **kw):
            folder = tmp / name
            shutil.copytree(good, folder)
            return folder

        f = tmp / "protel"; export(board, f, gerber_opts=()); write_bom(f)
        for g in f.glob("*.gbr"):
            if "_Cu" in g.name:
                g.rename(g.with_suffix(".gtl" if "F_Cu" in g.name else ".gbl"))
        case("old-style extensions", f, ".gbr file extension")
        f = tmp / "nox2"; export(board, f, gerber_opts=("--no-x2",)); write_bom(f)
        case("no X2 attributes", f, "X2 attributes")
        f = variant("nopaste"); next(f.glob("*F_Paste.gbr")).unlink()
        case("missing paste layer", f, "Every copper layer")
        f = variant("old"); g = next(f.glob("*B_Cu.gbr"))
        g.write_text(re.sub(r"(TF\.CreationDate,\d{4}-\d\d-\d\dT)\d\d", r"\g<1>01", g.read_text()))
        case("one file from another export", f, "one design and one revision")
        f = variant("nonet"); next(f.glob("*.d356")).unlink()
        case("no netlist", f, "IPC-D-356")
        f = tmp / "onedrill"; export(board, f, drill_opts=("--excellon-zeros-format", "keep")); write_bom(f)
        case("one drill file", f, "separate drill files")
        f = variant("format"); d = next(f.glob("*-PTH.drl"))
        d.write_text(d.read_text().replace("FORMAT={3:3/", "FORMAT={3:2/"))
        case("3:2 metric drill format", f, "Excellon format", also=("same origin",))  # a misread format moves the holes too
        f = variant("origin"); d = next(f.glob("*-PTH.drl"))
        d.write_text(re.sub(r"^X(-?\d+)Y", lambda m: f"X{int(m.group(1)) + 100000:06d}Y", d.read_text(), flags=re.M))
        case("drill origin moved", f, "Drill files use the same origin")
        f = tmp / "inch"; export(board, f, pos_opts=("--format", "ascii", "--units", "in", "--side", "both")); write_bom(f)
        case("placement in inches", f, "millimeters")
        f = tmp / "csvpos"; export(board, f, pos_opts=("--format", "csv", "--units", "mm", "--side", "both")); write_bom(f)
        case("placement with no units stated", f, "millimeters")
        b2 = tmp / "pastes" / f"{NAME}.kicad_pcb"; b2.parent.mkdir(); make_board(b2, paste_margin=-0.05)
        f = tmp / "shrunk"; export(b2, f); write_bom(f)
        case("paste shrunk on R1", f, "Paste openings the same size and shape as their pads, top")
        b3 = tmp / "tppaste" / f"{NAME}.kicad_pcb"; b3.parent.mkdir(); make_board(b3, testpad_paste=True)
        f = tmp / "tp"; export(b3, f); write_bom(f)
        case("paste on a test pad", f, "No paste on test pads")
        f = variant("longref"); write_bom(f, long_ref=True)
        case("reference designator too long", f, "8 characters or fewer", also=("match the placement file",))
        f = variant("nompn"); write_bom(f, drop=("empty-mpn",))
        case("a line with no part number", f, "Manufacturer and part number on every fitted line")
        f = variant("missingline"); write_bom(f, refs={"R1,R2", "C1,C2", "J1", "TP1"})
        case("U1 missing from the BOM", f, "match the placement file")
        f = variant("nomsl"); write_bom(f, drop=("MSL",))
        case("no MSL column", f, "moisture sensitivity")
        f = variant("noalt"); write_bom(f, drop=("Alternates",))
        case("no alternates column", f, "locked or with alternates")
        f = variant("nodnp"); write_bom(f, drop=("DNP",))
        case("no DNP column", f, "Do-not-place", also=("Manufacturer and part number",))  # the test point then looks fitted
        f = variant("nobom"); next(f.glob("*-bom.csv")).unlink()
        case("no BOM", f, "A BOM")

        for suffix in (".kicad_pcb", ".kicad_pro"):
            if (tmp / f"{NAME}{suffix}").exists():
                shutil.copy(tmp / f"{NAME}{suffix}", HERE / f"{NAME}{suffix}")
    if failures:
        print("\n".join(failures))
        sys.exit(1)
    print("The checker passed the good release and caught every mistake.")


if __name__ == "__main__":
    main()

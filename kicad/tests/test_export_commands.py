"""Prove that the export commands in kicad/check_release.py's help text work as written (AI3, R6).

Run: python3 kicad/tests/test_export_commands.py

Needs KiCad 10's kicad-cli, and bash. zsh is also tested when it is installed.
It takes the five commands from the help text, exactly as printed, and runs them through each shell
from a folder whose path has spaces in it, for a project whose name has a space in it.
QUANTITY and DNP are removed from the shell's environment first, so the test can't pass by accident.
The schematic has two resistors that group into one BOM line, and a third marked do not populate.
The test checks the BOM's references, quantities and DNP values, and that every other command wrote its files.
"""
import csv
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import check_release as cr  # noqa: E402

PROJECT = "my board"
BOARD = HERE / "opendfx-test.kicad_pcb"  # any board will do for the board exports


def u():
    return str(uuid.uuid4())


FONT = "(effects (font (size 1.27 1.27)))"
HIDDEN = "(effects (font (size 1.27 1.27)) (hide yes))"
LIB = f"""\t(lib_symbols
\t\t(symbol "Device:R" (pin_numbers (hide yes)) (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
\t\t\t(property "Reference" "R" (at 2.032 0 90) {FONT})
\t\t\t(property "Value" "R" (at 0 0 90) {FONT})
\t\t\t(property "Footprint" "" (at 0 0 0) {HIDDEN})
\t\t\t(property "Datasheet" "~" (at 0 0 0) {HIDDEN})
\t\t\t(property "Description" "Resistor" (at 0 0 0) {HIDDEN})
\t\t\t(symbol "R_0_1" (rectangle (start -1.016 -2.54) (end 1.016 2.54) (stroke (width 0.254) (type default)) (fill (type none))))
\t\t\t(symbol "R_1_1"
\t\t\t\t(pin passive line (at 0 3.81 270) (length 1.27) (name "~" {FONT}) (number "1" {FONT}))
\t\t\t\t(pin passive line (at 0 -3.81 90) (length 1.27) (name "~" {FONT}) (number "2" {FONT})))
\t\t\t(embedded_fonts no)))
"""


def symbol(root, ref, value, mpn, x, dnp):
    fields = [("Reference", ref), ("Value", value), ("Footprint", "Resistor_SMD:R_0603_1608Metric"),
              ("Datasheet", "~"), ("Manufacturer", "Example Maker"), ("MPN", mpn), ("MSL", "1"), ("Alternates", "")]
    props = "\n".join(f'\t\t(property "{k}" "{v}" (at {x} 50 0) {HIDDEN if k != "Reference" else FONT})'
                      for k, v in fields)
    return f"""\t(symbol (lib_id "Device:R") (at {x} 50 0) (unit 1) (exclude_from_sim no) (in_bom yes) (on_board yes)
\t\t(dnp {"yes" if dnp else "no"}) (uuid "{u()}")
{props}
\t\t(pin "1" (uuid "{u()}")) (pin "2" (uuid "{u()}"))
\t\t(instances (project "{PROJECT}" (path "/{root}" (reference "{ref}") (unit 1)))))
"""


def schematic():
    root = u()
    parts = [("R1", "10k", "RC0603-10K", 50, False), ("R2", "10k", "RC0603-10K", 60, False),
             ("R3", "4.7k", "RC0603-4K7", 70, True)]
    body = "".join(symbol(root, *p) for p in parts)
    return (f'(kicad_sch (version 20250114) (generator "eeschema") (generator_version "9.0")\n'
            f'\t(uuid "{root}") (paper "A4")\n{LIB}{body}'
            f'\t(sheet_instances (path "/" (page "1")))\n\t(embedded_fonts no))\n')


def help_commands():
    """The kicad-cli lines from the help text, exactly as printed, for this test's project name."""
    lines = [l.strip() for l in cr.__doc__.splitlines() if l.strip().startswith("kicad-cli ")]
    assert len(lines) == 5, f"expected 5 export commands in the help text, found {len(lines)}"
    return [l.replace("myboard", PROJECT) for l in lines]


def run_in(shell, folder):
    out = folder / "release"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir()
    env = {k: v for k, v in os.environ.items() if k not in ("QUANTITY", "DNP")}
    for cmd in help_commands():
        r = subprocess.run([shell, "-c", cmd], cwd=folder, env=env, capture_output=True, text=True)
        assert r.returncode == 0, f"{shell}: {cmd}\n{r.stdout}{r.stderr}"
    return out


def check_release_folder(shell, out):
    names = [p.name for p in out.iterdir()]
    for want in (f"{PROJECT}-F_Cu.gbr", f"{PROJECT}-Edge_Cuts.gbr", f"{PROJECT}.d356", f"{PROJECT}-pos.txt", f"{PROJECT}-bom.csv"):
        assert want in names, f"{shell}: {want} wasn't written; found {sorted(names)}"
    assert any(n.endswith("-PTH.drl") for n in names) and any(n.endswith("-NPTH.drl") for n in names), \
        f"{shell}: separate plated and non-plated drill files weren't written"
    with open(out / f"{PROJECT}-bom.csv", newline="") as f:
        rows = list(csv.DictReader(f))
    got = {r["Reference"]: (r["Qty"], r["DNP"].strip(), r["MPN"]) for r in rows}
    want = {"R1,R2": ("2", "", "RC0603-10K"), "R3": ("1", "DNP", "RC0603-4K7")}
    assert got == want, f"{shell}: BOM lines {got}, expected {want}"
    return rows


def main():
    if not shutil.which("kicad-cli") or not shutil.which("bash"):
        sys.exit("Needs kicad-cli (KiCad 10) and bash.")
    shells = ["bash"] + (["zsh"] if shutil.which("zsh") else [])
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp) / "My PCB Projects" / "rev A"
        folder.mkdir(parents=True)
        (folder / f"{PROJECT}.kicad_sch").write_text(schematic())
        shutil.copy(BOARD, folder / f"{PROJECT}.kicad_pcb")
        for shell in shells:
            rows = check_release_folder(shell, run_in(shell, folder))
            print(f"{shell}: all 5 export commands ran from a path with spaces; the BOM has {len(rows)} lines, "
                  "with R1 and R2 grouped as quantity 2 and R3 marked DNP.")
    if "zsh" not in shells:
        print("zsh isn't installed, so it wasn't tested.")


if __name__ == "__main__":
    main()

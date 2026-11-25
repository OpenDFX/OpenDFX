"""opendfx: the recommendations of OpenDFX for Printed Circuit Boards, from the command line.

  opendfx show PCB-DFM-020              one recommendation in full
  opendfx stage placement               every recommendation for one design stage
  opendfx stages                        the design stages, in order
  opendfx search "fiducial"             recommendations that contain every word
  opendfx check-release RELEASE_FOLDER [--board BOARD.kicad_pcb] [--json]
                                        check a board's release files (see opendfx check-release --help)
  opendfx kicad-rules PROJECT.kicad_pro copy the KiCad rules file next to a project, named after it
  opendfx path data|rules               where the data file or the KiCad rules file is installed
  opendfx --version

Add --json to show, stage or search to print the records as JSON.
From OpenDFX for Printed Circuit Boards by Chris Denney, https://opendfx.org.
"""
import json
import shutil
import sys
from pathlib import Path

from . import STAGES, __version__, for_stage, get, rules_path, data_path, search

FIELDS = [("Recommendation", "recommendation"), ("Why", "why"), ("Typical values", "typical_values"),
          ("What goes wrong if you don't", "what_goes_wrong"), ("Applies to", "applies_to")]


def show(r):
    print(f"## {r['id']}: {r['title']}")
    print(r["permalink"])
    for label, key in FIELDS:
        if r.get(key):
            print(f"\n{label}:\n{r[key]}")
    for c in r.get("checks", []):
        print(f"\nChecked by the KiCad rules file: {c['check']}. Recommended {c['recommended']} {c['unit']}. Minimum {c['minimum']} {c['unit']}.")
    print()


def output(records, as_json):
    if as_json:
        print(json.dumps(records, indent=2, ensure_ascii=False))
    else:
        for r in records:
            show(r)


def kicad_rules(target):
    target = Path(target)
    if target.is_dir():
        projects = sorted(target.glob("*.kicad_pro"))
        if len(projects) != 1:
            sys.exit(f"Name the project file: {target} holds {len(projects)} .kicad_pro files.")
        target = projects[0]
    if target.suffix != ".kicad_pro" or not target.exists():
        sys.exit(f"Not a KiCad project file: {target}")
    dest = target.with_suffix(".kicad_dru")
    if dest.exists():
        sys.exit(f"{dest} already exists. Rename or remove it first, so your own rules aren't lost.")
    shutil.copyfile(rules_path(), dest)
    print(f"Wrote {dest}")
    print("In KiCad, also set Board Setup, Solder Mask/Paste, Minimum web width to 0.1 mm. See https://opendfx.org/kicad/")


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in args
    cmd = args[0] if args else ""
    rest = [a for a in args[1:] if a != "--json"]
    if cmd in ("", "-h", "--help", "help"):
        print(__doc__)
        sys.exit(0 if cmd else 2)
    if cmd == "--version":
        print(f"opendfx {__version__}")
    elif cmd == "show" and rest:
        try:
            output([get(i) for i in rest], as_json)
        except KeyError as e:
            sys.exit(e.args[0])
    elif cmd == "stage" and len(rest) == 1:
        if rest[0] not in STAGES:
            sys.exit(f"Unknown design stage {rest[0]}. The stages are: {', '.join(STAGES)}")
        output(for_stage(rest[0]), as_json)
    elif cmd == "stages":
        print("\n".join(STAGES))
    elif cmd == "search" and rest:
        found = search(" ".join(rest))
        if not found:
            sys.exit("No recommendation contains all of those words.")
        output(found, as_json)
    elif cmd == "check-release":
        from . import check_release
        sys.argv = ["opendfx check-release"] + args[1:]
        check_release.main()
    elif cmd == "kicad-rules" and len(rest) == 1:
        kicad_rules(rest[0])
    elif cmd == "path" and rest in (["data"], ["rules"]):
        print(data_path() if rest == ["data"] else rules_path())
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()

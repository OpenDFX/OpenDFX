"""Print OpenDFX recommendations from recommendations.json (next to this skill's SKILL.md).
It finds that file from its own location, so it runs from any folder, such as your PCB project.
Replace <skill folder> with the real path, and keep the quotation marks, so a path with spaces still works.

  python3 "<skill folder>/scripts/recommendations.py" --stage placement   every recommendation for one design stage
  python3 "<skill folder>/scripts/recommendations.py" --id PCB-DFM-020    one recommendation in full
  python3 "<skill folder>/scripts/recommendations.py" --stages            the design stages, in order
"""
import json
import sys
from pathlib import Path

STAGES = ["parts", "library", "placement", "routing", "outline", "release", "production"]
DATA = Path(__file__).resolve().parent.parent / "recommendations.json"
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


def main():
    recs = json.loads(DATA.read_text())["recommendations"]
    args = sys.argv[1:]
    if args[:1] == ["--stages"]:
        print("\n".join(STAGES))
    elif args[:1] == ["--stage"] and len(args) > 1 and args[1] in STAGES:
        for r in recs:
            if args[1] in r["design_stages"]:
                show(r)
    elif args[:1] == ["--id"] and len(args) > 1:
        found = [r for r in recs if r["id"] == args[1].upper()]
        if not found:
            sys.exit(f"No recommendation {args[1]}")
        show(found[0])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()

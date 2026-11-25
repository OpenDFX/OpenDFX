"""Rebuild every file that is made from the book's pages, in the right order.

Run: python3 tools/build_all.py           (after editing a page)
     python3 tools/build_all.py --check   (exits 1 if anything is out of date; run it before a pull request)

It runs, in order:
  1. tools/build_appendices.py   the checklist, design-stage index, standards and sources in book/09-appendices/
  2. tools/build_kicad_rules.py  the KiCad design-rules file and its website page
  3. tools/build_data.py         data/recommendations.json and .yaml, llms.txt, llms-full.txt and robots.txt
  4. tools/build_skill.py        the Agent Skill in skill/opendfx-pcb-design/

Needs: pip install pyyaml (and jsonschema, to check the data file against its schema).
The website, the PDF and the EPUB are built separately; see CONTRIBUTING.md.
"""
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
STEPS = ["build_appendices.py", "build_kicad_rules.py", "build_data.py", "build_skill.py"]


def main():
    check = "--check" in sys.argv[1:]
    failed = []
    for step in STEPS:
        cmd = [sys.executable, str(TOOLS / step)] + (["--check"] if check else [])
        print(f"build_all: {' '.join(['tools/' + step] + cmd[2:])}", flush=True)
        if subprocess.run(cmd, cwd=TOOLS.parent).returncode != 0:
            failed.append(step)
            if not check:  # a later step reads what an earlier one wrote, so stop at the first failure
                break
    if failed:
        print(f"build_all: {', '.join(failed)} failed" + (": run python3 tools/build_all.py, then commit what it changed" if check else ""))
        return 1
    print("build_all: everything is up to date" if check else "build_all: done")
    return 0


if __name__ == "__main__":
    sys.exit(main())

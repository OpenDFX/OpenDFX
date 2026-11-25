"""Tests for the installed opendfx package (M42). tools/build_pypi.py runs them in a fresh virtual environment.

Run: python3 test_package.py [REPOSITORY]
With the repository's folder, it also checks the installed data file matches data/recommendations.json.
The release checker itself is tested with KiCad by kicad/tests/test_release_check.py.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import opendfx

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else None
CLI = [str(Path(sys.executable).parent / "opendfx")]


def run(*args, ok=True):
    p = subprocess.run(CLI + list(args), capture_output=True, text=True)
    assert (p.returncode == 0) == ok, f"opendfx {' '.join(args)} exited {p.returncode}: {p.stderr}"
    return p.stdout


def main():
    data = opendfx.data()
    recs = opendfx.recommendations()
    assert len(recs) == data["count"] > 100
    assert opendfx.get("pcb-dfa-006")["permalink"] == "https://opendfx.org/PCB-DFA-006"
    try:
        opendfx.get("PCB-XYZ-999")
        raise AssertionError("get() should raise KeyError")
    except KeyError:
        pass
    assert all(opendfx.for_stage(s) for s in opendfx.STAGES)
    assert opendfx.search("fiducial")
    assert "(version 1)" in opendfx.rules_path().read_text()
    assert opendfx.__version__ != "0.0.0"
    if ROOT:
        assert data == json.loads((ROOT / "data" / "recommendations.json").read_text())

    out = run("show", "PCB-DFM-020")
    assert out.startswith("## PCB-DFM-020: ") and "https://opendfx.org/PCB-DFM-020" in out
    assert json.loads(run("stage", "placement", "--json"))
    assert run("stages").split() == list(opendfx.STAGES)
    assert run("--version").strip() == f"opendfx {opendfx.__version__}"
    assert Path(run("path", "data").strip()) == opendfx.data_path()
    run("show", "PCB-XYZ-999", ok=False)
    run("stage", "nowhere", ok=False)
    run(ok=False)
    assert "RELEASE_FOLDER" in run("check-release", "--help")

    with tempfile.TemporaryDirectory() as tmp:
        pro = Path(tmp) / "myboard.kicad_pro"
        pro.write_text("{}")
        run("kicad-rules", str(pro))
        assert (Path(tmp) / "myboard.kicad_dru").read_text() == opendfx.rules_path().read_text()
        run("kicad-rules", str(pro), ok=False)  # never overwrites a rules file

    with tempfile.TemporaryDirectory() as tmp:  # an empty release folder: the checker still reports every check
        p = subprocess.run(CLI + ["check-release", tmp, "--json"], capture_output=True, text=True)
        rows = json.loads(p.stdout)
        assert p.returncode == 1 and rows, p.stderr
        assert all(r["status"] in ("Met", "Not met", "Needs a person") for r in rows)
        assert any(r["status"] == "Not met" for r in rows)

    print("opendfx package tests passed.")


if __name__ == "__main__":
    main()

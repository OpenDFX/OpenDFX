"""Build the opendfx package for PyPI (M42, PYPI1): build/pypi/dist/opendfx-<version>.tar.gz and .whl.

Run: python3 tools/build_pypi.py          (builds the package and tests it)
     python3 tools/build_pypi.py --no-test (builds only)

The package's own code, README and tests are in python/.
This script copies them into build/pypi/ and adds the generated files beside them, so the repository keeps
only one copy of each:
  src/opendfx/data/recommendations.json         data/recommendations.json (CC BY 4.0)
  src/opendfx/data/recommendations.schema.json  data/recommendations.schema.json
  src/opendfx/data/opendfx.kicad_dru            kicad/opendfx.kicad_dru (MIT)
  src/opendfx/check_release.py                  kicad/check_release.py (MIT)
  LICENSE-CODE, LICENSE-DATA                    the licenses
The version is the book's version, from CITATION.cff.

Run it after tools/build_kicad_rules.py and tools/build_data.py, because it copies their files.
Needs `pip install build`; building also downloads hatchling. The tests install the wheel into a fresh virtual
environment and run python/tests/test_package.py there.
PyPI never accepts the same version twice, so a change to the data needs a new book version in CITATION.cff.
The workflow .github/workflows/pypi.yml publishes it.
"""
import re
import shutil
import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "python"
OUT = ROOT / "build" / "pypi"


def version():
    m = re.search(r'^version:\s*"?([^"\n]+)"?', (ROOT / "CITATION.cff").read_text(), re.M)
    if not m:
        sys.exit("No version in CITATION.cff")
    return m.group(1).strip()


def stage():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    pkg = OUT / "src" / "opendfx"
    (pkg / "data").mkdir(exist_ok=True)
    copies = {
        ROOT / "data" / "recommendations.json": pkg / "data" / "recommendations.json",
        ROOT / "data" / "recommendations.schema.json": pkg / "data" / "recommendations.schema.json",
        ROOT / "kicad" / "opendfx.kicad_dru": pkg / "data" / "opendfx.kicad_dru",
        ROOT / "kicad" / "check_release.py": pkg / "check_release.py",
        ROOT / "LICENSE-CODE": OUT / "LICENSE-CODE",
        ROOT / "LICENSE-DATA": OUT / "LICENSE-DATA",
    }
    for src, dst in copies.items():
        shutil.copyfile(src, dst)
    v = version()
    (pkg / "_version.py").write_text(f'__version__ = "{v}"\n')
    toml = OUT / "pyproject.toml"
    text = toml.read_text()
    toml.write_text(text.replace('version = "0.0.0"', f'version = "{v}"', 1))
    return v


def build():
    subprocess.run([sys.executable, "-m", "build", "--outdir", str(OUT / "dist"), str(OUT)], check=True)
    return sorted((OUT / "dist").glob("*.whl"))[-1]


def test(wheel):
    env = OUT / "venv"
    venv.create(env, with_pip=True)
    py = env / ("Scripts" if sys.platform == "win32" else "bin") / "python"
    subprocess.run([str(py), "-m", "pip", "install", "-q", str(wheel)], check=True)
    subprocess.run([str(py), "-I", str(SRC / "tests" / "test_package.py"), str(ROOT)], check=True, cwd=str(OUT))


def main():
    v = stage()
    wheel = build()
    print(f"Built opendfx {v}: {wheel.relative_to(ROOT)}")
    if "--no-test" not in sys.argv:
        test(wheel)


if __name__ == "__main__":
    main()

"""Render an SVG to a PNG with a browser (Chromium through Playwright), for the few drawings the PDF engine can't draw.

Run: python3 tools/books/rasterize.py IN.svg OUT.png WIDTH_PX
WeasyPrint, which makes the PDF, doesn't support SVG masks or filters. The cover and D68 use them,
so build_books.py puts a 300 dpi PNG of each into the PDF instead. Rendered PNGs are committed, with the
SHA-256 of their SVG beside them (OUT.png.sha256), so the build can tell when one is out of date.
Needs node and Playwright (both are in Claude's cloud sessions; not needed in the website workflow).
"""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def svg_hash(svg):
    return hashlib.sha256(Path(svg).read_bytes()).hexdigest()


def rasterize(svg, png, width_px):
    svg, png = Path(svg).resolve(), Path(png).resolve()
    import re
    vb = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', svg.read_text())
    w, h = float(vb.group(1)), float(vb.group(2))
    css_w = width_px // 2  # render_svg.js renders at device scale factor 2
    css_h = round(css_w * h / w)
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "page.html"
        page.write_text(f'<html><body style="margin:0"><img src="{svg.as_uri()}" style="display:block;width:{css_w}px;height:{css_h}px"></body></html>')
        subprocess.run(["node", str(ROOT / "tools" / "render_svg.js"), str(page), str(png), str(css_w), str(css_h), "light"], check=True)
    Path(str(png) + ".sha256").write_text(svg_hash(svg) + "\n")


if __name__ == "__main__":
    rasterize(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    print(f"Wrote {sys.argv[2]}")

"""Part 8 diagrams (D66) in the OpenDFX style.
Run: python3 tools/diagrams/part8_diagrams.py         (writes trials/python-N-<name>.svg for review)
     python3 tools/diagrams/part8_diagrams.py --book  (writes book/08-working-with-a-manufacturer/images/<name>.svg)"""
from pathlib import Path
import math
import re
import sys

import drawsvg as dw
import opendfx_draw
from opendfx_draw import Sheet

BOOK = "--book" in sys.argv
OUT = (Path(__file__).parent / "trials") if not BOOK else (
    Path(__file__).parents[2] / "book" / "08-working-with-a-manufacturer" / "images")
OUT.mkdir(exist_ok=True)

EXTRA = """
.step    { fill: #e6eef8; stroke: #2563a8; stroke-width: 1.2; }
.stepfa  { fill: #fdf0d8; stroke: #a8741a; stroke-width: 1.2; }
.flow    { stroke: #5b636b; stroke-width: 1.4; fill: none; }
.flowhd  { fill: #5b636b; }
.fa      { fill: #a8741a; }
.batch   { fill: #1e7a3e; stroke: #ffffff; stroke-width: 0.8; }
@media (prefers-color-scheme: dark) {
  .step   { fill: #1d2a3a; stroke: #79aef0; }
  .stepfa { fill: #3a2f1a; stroke: #e0b062; }
  .flow   { stroke: #a3abb3; }
  .flowhd { fill: #a3abb3; }
  .fa     { fill: #e0b062; }
  .batch  { stroke: #16191c; }
}
"""


def out(n, name):
    opendfx_draw.CURRENT_D = n
    return OUT / (f"{name}.svg" if BOOK else f"python-{n}-{name}.svg")


def sheet(*a, **k):
    s = Sheet(*a, **k)
    s.d.append(dw.Raw(f"<style>{print_css(s, EXTRA)}</style>"))
    return s


def print_css(s, css):
    """This script's own styles with stroke widths and dashes sized for print, as the kit does for its own (DRW1)."""
    css = re.sub(r"stroke-width: ([\d.]+)(?!px)", lambda m: f"stroke-width: {s.sw(float(m.group(1)))}", css)
    return re.sub(r"stroke-dasharray: ([\d. ]+);", lambda m: "stroke-dasharray: " + " ".join(
        str(round(float(v) * s.f, 2)) for v in m.group(1).split()) + ";", css)


def production_ramp():
    """D66: the steps from prototype to production."""
    title = "D66: From prototype to production in steps"
    desc = ("D66 is a flow diagram, not to scale. Five steps run left to right: 5 prototypes that prove the design; "
            "a pilot build of 20; 200 boards with first articles at the start; 1,000 boards, the first large batch, "
            "which runs slower while the assembler learns the board; then full volume, released in batches of whole "
            "panels, shown as batches of 27 boards from a 9-up panel. Each step is wider than the last, because it "
            "builds more boards.")
    W, H = 980, 480
    s = sheet(W, H, title, desc)
    steps = [("5", "Prototypes", False), ("20", "Pilot build", False), ("200", "First articles first", True),
             ("1,000", "First large batch", False), ("2,000 +", "Full volume", False)]
    widths = [88, 112, 140, 168, 230]
    gap, x, y, h = 30, 30, 50, 92
    centers = []
    for (qty, name, fa), w in zip(steps, widths):
        s.d.append(dw.Rectangle(x, y, w, h, rx=8, class_="stepfa" if fa else "step"))
        s.text(qty, x + w / 2, y + 44, size=26, anchor="middle", weight="700", px=True)
        s.text("boards", x + w / 2, y + 66, size=12.5, anchor="middle", cls="muted", px=True)
        s.text(name, x + w / 2, y - 12, size=13, anchor="middle", weight="600", px=True)
        centers.append((x, w))
        if len(centers) < len(steps):
            ax = x + w + 4
            s.d.append(dw.Line(ax, y + h / 2, ax + gap - 10, y + h / 2, class_="flow"))
            s.d.append(dw.Lines(ax + gap - 8, y + h / 2, ax + gap - 16, y + h / 2 - 5, ax + gap - 16, y + h / 2 + 5,
                                close=True, class_="flowhd"))
        x += w + gap
    fx, fw = centers[2]
    # Batches of whole panels inside the full-volume step: 27 = one 9-up panel three times.
    vx, vw = centers[4]
    for b in range(4):
        bx0 = vx + 14 + b * 52
        for k in range(3):
            s.d.append(dw.Rectangle(bx0 + k * 14, y + 76, 12, 12, class_="batch"))
    # Balloons and key. Targets are given in px, so scale is 1 and ox, oy are 0.
    by = y + h + 50
    s.balloon(1, (centers[0][0] + centers[0][1] / 2, y + h), (centers[0][0] + centers[0][1] / 2, by),
              "Prototypes prove the design works")
    s.balloon(2, (centers[1][0] + centers[1][1] / 2, y + h), (centers[1][0] + centers[1][1] / 2, by),
              "A pilot build shows what was done by hand", "Replace hand-fitted and hard-to-find parts now")
    s.balloon(3, (fx + fw / 2, y + h), (fx + fw / 2, by), "First articles, if anything changed since the last build",
              "One panel at least, checked before the rest are built")
    s.balloon(4, (centers[3][0] + centers[3][1] / 2, y + h), (centers[3][0] + centers[3][1] / 2, by),
              "The first large batch runs slower", "The assembler learns the board; expect a few more issues")
    s.balloon(5, (vx + vw / 2, y + h), (vx + vw / 2, by), "Full volume, released in batches of whole panels",
              "Each square is one 9-up panel; a batch of 3 panels is 27 boards")
    y = s.key(40, by + 50 * s.f, width=600)
    s.height = round(y + 26 * s.f)
    s.save(out(66, "production-ramp"))


if __name__ == "__main__":
    production_ramp()

"""Part 0 diagrams (D67) in the OpenDFX style.
Run: python3 tools/diagrams/part0_diagrams.py         (writes trials/python-N-<name>.svg for review)
     python3 tools/diagrams/part0_diagrams.py --book  (writes book/00-start-here/images/<name>.svg)"""
from pathlib import Path
import re
import sys

import drawsvg as dw
import opendfx_draw
from opendfx_draw import Sheet

BOOK = "--book" in sys.argv
OUT = (Path(__file__).parent / "trials") if not BOOK else (
    Path(__file__).parents[2] / "book" / "00-start-here" / "images")
OUT.mkdir(exist_ok=True)

EXTRA = """
.step    { fill: #e6eef8; stroke: #2563a8; stroke-width: 1.2; }
.stepin  { fill: #fdf0d8; stroke: #a8741a; stroke-width: 1.2; }
.span    { fill: #eef0f2; stroke: #5b636b; stroke-width: 1.2; }
.flow    { stroke: #5b636b; stroke-width: 1.4; fill: none; }
.flowhd  { fill: #5b636b; }
@media (prefers-color-scheme: dark) {
  .step   { fill: #1d2a3a; stroke: #79aef0; }
  .stepin { fill: #3a2f1a; stroke: #e0b062; }
  .span   { fill: #24282d; stroke: #a3abb3; }
  .flow   { stroke: #a3abb3; }
  .flowhd { fill: #a3abb3; }
}
"""


def out(n, name):
    opendfx_draw.CURRENT_D = n
    return OUT / (f"{name}.svg" if BOOK else f"python-{n}-{name}.svg")


def sheet(*a, **k):
    s = Sheet(*a, **k)
    extra = re.sub(r"stroke-width: ([\d.]+)", lambda m: f"stroke-width: {s.sw(float(m.group(1)))}", EXTRA)
    s.d.append(dw.Raw(f"<style>{extra}</style>"))
    return s


def arrow(s, x1, y1, x2, y2):
    """A straight flow arrow from (x1, y1) to (x2, y2), horizontal or vertical, in px."""
    a, b = 8 * s.f, 5 * s.f
    s.d.append(dw.Line(x1, y1, x2, y2, class_="flow"))
    if y1 == y2:
        d = 1 if x2 > x1 else -1
        s.d.append(dw.Lines(x2, y2, x2 - a * d, y2 - b, x2 - a * d, y2 + b, close=True, class_="flowhd"))
    else:
        d = 1 if y2 > y1 else -1
        s.d.append(dw.Lines(x2, y2, x2 - b, y2 - a * d, x2 + b, y2 - a * d, close=True, class_="flowhd"))


def box(s, x, y, w, h, part, name, lines, cls="step"):
    s.d.append(dw.Rectangle(x, y, w, h, rx=8, class_=cls))
    s.text(part, x + w / 2, y + 24, size=10.5, anchor="middle", cls="muted", px=True)
    for i, n in enumerate(name):
        s.text(n, x + w / 2, y + 50 + i * 21, size=13, anchor="middle", weight="700", px=True)
    top = y + 56 + len(name) * 21
    for i, t in enumerate(lines):
        s.text(t, x + w / 2, top + i * 19, size=10.5, anchor="middle", cls="muted", px=True)


def board_path():
    """D67: the path a board takes, from design files to delivered product."""
    title = "D67: The path a board takes"
    desc = ("D67 is a flow diagram, not to scale. Six steps run left to right, each with the Part of the book that "
            "covers it: the design package (Part 1), the panel (Part 2), bare-board fabrication (Part 3), assembly "
            "(Part 5), test and programming (Part 6), and packing and shipping (Part 7). Components and materials "
            "(Part 4) feed into assembly from above, alongside the bare boards. A bar under every step shows working "
            "with a manufacturer (Part 8), which runs through the whole path.")
    W, H = 980, 474
    s = sheet(W, H, title, desc)
    steps = [
        ("Part 1", ["The design", "package"], ["Files, drawings", "and the BOM"]),
        ("Part 2", ["The panel"], ["PCBs joined", "for machine", "assembly"]),
        ("Part 3", ["Bare-board", "fabrication"], ["Layers, holes,", "mask and finish"]),
        ("Part 5", ["Assembly"], ["Paste, placement,", "soldering,", "inspection"]),
        ("Part 6", ["Test and", "programming"], ["Test points,", "fixtures,", "firmware"]),
        ("Part 7", ["Packing and", "shipping"], ["Static, moisture", "and boxes"]),
    ]
    w, h, gap, x0, y = 148, 152, 14, 14, 186
    xs = [x0 + i * (w + gap) for i in range(len(steps))]
    for i, (x, (part, name, lines)) in enumerate(zip(xs, steps)):
        box(s, x, y, w, h, part, name, lines)
        if i + 1 < len(steps):
            arrow(s, x + w + 1, y + h / 2, x + w + gap - 1, y + h / 2)
    # Parts feed into assembly from above.
    ax = xs[3]
    py, ph = 4, 156
    box(s, ax, py, w, ph, "Part 4", ["Components", "and materials"], ["Buying, storing", "and supplying", "parts"],
        cls="stepin")
    arrow(s, ax + w / 2, py + ph + 2, ax + w / 2, y - 2)
    # Part 8 runs under the whole path.
    by, bh = y + h + 26, 100
    bw = xs[-1] + w - x0
    s.d.append(dw.Rectangle(x0, by, bw, bh, rx=8, class_="span"))
    s.text("Part 8", x0 + bw / 2, by + 24, size=10.5, anchor="middle", cls="muted", px=True)
    s.text("Working with a manufacturer, at every step", x0 + bw / 2, by + 52, size=13, anchor="middle",
           weight="700", px=True)
    s.text("Cost, lead time, prototype to production, and design reviews", x0 + bw / 2, by + 80, size=12,
           anchor="middle", cls="muted", px=True)
    s.save(out(67, "board-path"))


if __name__ == "__main__":
    board_path()

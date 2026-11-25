"""Part 7 diagrams (D65) in the OpenDFX style.
Run: python3 tools/diagrams/part7_diagrams.py         (writes trials/python-N-<name>.svg for review)
     python3 tools/diagrams/part7_diagrams.py --book  (writes book/07-handling-packaging-and-shipping/images/<name>.svg)"""
from pathlib import Path
import re
import sys

import drawsvg as dw
import opendfx_draw
from opendfx_draw import Sheet

BOOK = "--book" in sys.argv
OUT = (Path(__file__).parent / "trials") if not BOOK else (
    Path(__file__).parents[2] / "book" / "07-handling-packaging-and-shipping" / "images")
OUT.mkdir(exist_ok=True)

# Packaging colors (not board colors).
EXTRA = """
.carton   { fill: #c49a6c; stroke: #8a6a45; stroke-width: 0.8; }
.flute    { stroke: #8a6a45; stroke-width: 0.7; fill: none; }
.fill     { fill: #ece6da; stroke: #b8ad98; stroke-width: 0.6; }
.pink     { fill: #f3a9c2; stroke: #c76f90; stroke-width: 0.6; }
.pinkbag  { stroke: #e07aa0; stroke-width: 2.2; fill: none; }
.shield   { stroke: #8f969d; stroke-width: 2.6; fill: none; }
.tape     { fill: #d8c48a; stroke: #8a7a52; stroke-width: 0.6; }
.zap      { fill: #e0392b; stroke: #7a1a12; stroke-width: 0.8; }
.good     { fill: #2f9e4f; }
.bad      { fill: #b23a2b; }
@media (prefers-color-scheme: dark) {
  .fill   { fill: #4a463e; stroke: #7d7564; }
  .shield { stroke: #c9ccd1; }
  .good   { fill: #5cc47d; }
  .bad    { fill: #f08a7a; }
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


def packed_board():
    """D65: a board packed to ship, beside the same board in a pink anti-static bag only."""
    title = "D65: A board packed to ship, compared with a board in an anti-static bag only"
    desc = ("D65 is a cross-section, drawn to scale. Left, marked good: a 100 mm board 1.6 mm thick with parts on top "
            "is wrapped in pink anti-static bubble wrap, then sealed in a metallized static-shielding bag folded over and "
            "taped, in a corrugated box with filler. A spark from outside stops at the shielding bag. Right, marked "
            "avoid: the same board in a pink anti-static bag only; the spark passes through the bag to the board.")
    S = 2.6                                    # px per mm
    W, H = 980, 560
    s = sheet(W, H, title, desc, scale=S, ox=0, oy=0)

    def panel(x0, good):
        """Draw one packed board with its box. x0 is the left edge of the box in mm."""
        bw, bh, wall = 150.0, 62.0, 4.0        # box outside width and height, wall thickness
        y0 = 30.0
        # Box: corrugated walls drawn as a shell with flutes.
        s.rect(x0, y0, bw, bh, "carton")
        s.rect(x0 + wall, y0 + wall, bw - 2 * wall, bh - 2 * wall, "bg")
        for i in range(int(bw / 3)):
            for yy in (y0 + wall / 2, y0 + bh - wall / 2):
                s.line(x0 + i * 3, yy - 1.2, x0 + i * 3 + 1.5, yy + 1.2, "flute")
        # Filler (crumpled paper) below and above the bag.
        ix, iw = x0 + wall, bw - 2 * wall
        for yy, hh in ((y0 + wall, 12.0), (y0 + bh - wall - 12.0, 12.0)):
            s.rect(ix + 1, yy + 1, iw - 2, hh - 2, "fill", rx=3)
        # The board: 100 mm long, 1.6 mm thick, centered, with parts and solder on top.
        bx, by, L, T = x0 + (bw - 100.0) / 2, y0 + bh / 2 + 2.0, 100.0, 1.6
        s.rect(bx, by, L, T, "mask-on-fr4")
        parts = [(8, 5.0, 2.0), (22, 7.0, 1.2), (34, 12.0, 1.0), (52, 9.0, 3.5), (70, 3.2, 1.6), (82, 10.0, 6.0)]
        for px, pw, ph in parts:
            s.rect(bx + px - 0.6, by - 0.4, pw + 1.2, 0.4, "solder")
            s.rect(bx + px, by - 0.4 - ph, pw, ph, "part")
        top = by - 0.4 - 6.0                    # tallest part
        if good:
            # Pink anti-static bubble wrap: a sheet with 4 mm bubbles, wrapped round the board.
            for side, yy in ((-1, top - 1.0), (1, by + T + 1.0)):
                s.rect(bx - 5, yy - (2.0 if side < 0 else 0), L + 10, 2.0, "pink")
                for k in range(int((L + 10) / 5)):
                    cy = yy - 2.0 - 1.6 if side < 0 else yy + 2.0 + 1.6
                    s.circle(bx - 3 + k * 5, cy, 1.8, "pink")
            s.rect(bx - 6.5, top - 7.0, 2.0, by + T + 7.0 - (top - 7.0), "pink")
            s.rect(bx + L + 4.5, top - 7.0, 2.0, by + T + 7.0 - (top - 7.0), "pink")
            # Shielding bag round the wrapped board, folded over at the right and taped.
            g = 2.0
            s.d.append(dw.Rectangle(s.X(bx - 9), s.Y(top - 9.5), s.L(L + 18), s.L(by + T + 9.5 - (top - 9.5)),
                                    rx=s.L(g), class_="shield"))
            fx = bx + L + 9
            s.line(fx, top - 9.5, fx + 5, top - 6.0, "shield")
            s.rect(fx - 1.5, top - 4.0, 6.0, 8.0, "tape")
            return dict(bag=(bx - 9, top - 9.5), board=(bx + 52, by - 0.4 - 3.5), box=(x0 + bw - 2, y0 + 50),
                        bubble=(bx + 30, by + T + 4.6), tape=(fx + 1.5, top))
        # Pink anti-static bag only, fitted close round the board.
        s.d.append(dw.Rectangle(s.X(bx - 3), s.Y(top - 3), s.L(L + 6), s.L(by + T + 3 - (top - 3)),
                                rx=s.L(1.5), class_="pinkbag"))
        return dict(bag=(bx - 3, top + 4), board=(bx + 52, by - 0.4 - 3.5), box=(x0 + 2, y0 + 20))

    def spark(x, y_from, y_to, through):
        """A zig-zag spark coming down from outside the box to y_to (mm)."""
        pts = [(x, y_from), (x - 3, y_from + 6), (x + 2, y_from + 9), (x - 2, y_to - 3), (x + 1, y_to)]
        p = dw.Path(class_="zap")
        p.M(s.X(pts[0][0]) - 3, s.Y(pts[0][1]))
        for a, b in pts[1:]:
            p.L(s.X(a) - 3, s.Y(b))
        for a, b in reversed(pts[1:]):
            p.L(s.X(a) + 3, s.Y(b))
        p.Z()
        s.d.append(p)

    a = panel(6.0, True)
    b = panel(200.0, False)
    # Sparks from a charged hand or box above each package.
    spark(6.0 + 95, 18.0, a["bag"][1], False)
    spark(200.0 + 95, 18.0, b["board"][1] - 2.0, True)

    # Panel labels.
    s.d.append(dw.Circle(s.X(10), s.Y(13), 7, class_="good"))
    s.text("Good: bubble wrap inside a sealed shielding bag", s.X(10) + 14, s.Y(13) + 5, size=14, weight="600",
           px=True)
    s.d.append(dw.Circle(s.X(204), s.Y(13), 7, class_="bad"))
    s.text("Avoid: pink anti-static bag on its own", s.X(204) + 14, s.Y(13) + 5, size=14, weight="600", px=True)

    by_ = s.Y(100)
    s.balloon(1, a["board"], (s.X(a["board"][0]), by_), "Assembled board, 100 mm long and 1.6 mm thick")
    s.balloon(2, a["bubble"], (s.X(a["bubble"][0]), by_), "Pink anti-static bubble wrap, safe against the board",
              "Low-charging, but it does not shield")
    s.balloon(3, a["bag"], (s.X(a["bag"][0]), by_), "Metallized static-shielding bag",
              "Stops a discharge from outside, but only while closed")
    s.balloon(4, a["tape"], (s.X(a["tape"][0]), by_), "Top folded over and taped shut")
    s.balloon(5, a["box"], (s.X(a["box"][0]), by_), "Corrugated box with paper filler")
    s.balloon(6, b["bag"], (s.X(b["bag"][0]), by_), "Pink anti-static bag: low-charging only",
              "A discharge from outside passes straight through")
    ky = by_ + 60 * s.f
    y1 = s.key(40, ky, width=440, only=(1, 2, 3))
    y2 = s.key(525, ky, width=425, title="", only=(4, 5, 6))
    y = max(y1, y2) + 40 * s.f
    s.note("Drawn to scale. The bags are drawn thicker than they are, so they can be seen.", 40, y)
    s.height = round(y + 26 * s.f)
    s.save(out(65, "packed-board"))


if __name__ == "__main__":
    packed_board()

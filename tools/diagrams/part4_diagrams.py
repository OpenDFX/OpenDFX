"""Part 4 diagrams D56-D60 in the OpenDFX style.
Run: python3 tools/diagrams/part4_diagrams.py         (writes trials/python-N-<name>.svg for review)
     python3 tools/diagrams/part4_diagrams.py --book  (writes book/04-components-and-materials/images/<name>.svg)"""
from pathlib import Path
import re
import sys

import drawsvg as dw
import opendfx_draw
from opendfx_draw import Sheet

BOOK = "--book" in sys.argv
OUT = (Path(__file__).parent / "trials") if not BOOK else (
    Path(__file__).parents[2] / "book" / "04-components-and-materials" / "images")
OUT.mkdir(exist_ok=True)

# Packaging colors (not board colors): carrier tape, cover tape, tubes, bags, cards.
EXTRA = """
.tape   { fill: #2b2e33; }
.pocket { fill: #111315; }
.cover  { fill: #bcd7ee; fill-opacity: 0.45; stroke: #7da7c9; stroke-width: 0.8; }
.sprk   { fill: #ffffff; }
.reel   { fill: #3a78c2; fill-opacity: 0.25; stroke: #3a78c2; stroke-width: 1.4; }
.hub    { fill: #ffffff; stroke: #3a78c2; stroke-width: 1.4; }
.tube   { fill: #cfd8de; fill-opacity: 0.55; stroke: #5b636b; stroke-width: 1.2; }
.stopper{ fill: #2f9e4f; }
.tray   { fill: #2b2e33; }
.tcell  { fill: #3f444b; }
.bag    { fill: #b9c0c7; fill-opacity: 0.35; stroke: #5b636b; stroke-width: 1.4; }
.seal   { fill: #8f969d; }
.card   { fill: #f4f1e6; stroke: #5b636b; stroke-width: 1; }
.dry    { fill: #3a6fd8; }
.wet    { fill: #e58fb4; }
.desic  { fill: #ece6d2; stroke: #8a8270; stroke-width: 1; }
.caution{ fill: #f2c94c; stroke: #8a6d00; stroke-width: 1; }
.cardink{ fill: #1d2125; }
.good   { fill: #2f9e4f; }
.bad    { fill: #b23a2b; }
@media (prefers-color-scheme: dark) {
  .tape   { fill: #4a5058; }
  .pocket { fill: #23272b; }
  .sprk   { fill: #16191c; }
  .hub    { fill: #16191c; }
  .tray   { fill: #4a5058; }
  .tcell  { fill: #5d646d; }
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


def fit(s, y):
    """Make the sheet just tall enough for content ending at y (px)."""
    s.height = round(y + 26 * s.f)


def lh(s, size=11):
    """Line spacing for lines of text of this size."""
    return s.fs(size) * 1.35


def print_css(s, css):
    """This script's own styles with stroke widths and dashes sized for print, as the kit does for its own (DRW1)."""
    css = re.sub(r"stroke-width: ([\d.]+)(?!px)", lambda m: f"stroke-width: {s.sw(float(m.group(1)))}", css)
    return re.sub(r"stroke-dasharray: ([\d. ]+);", lambda m: "stroke-dasharray: " + " ".join(
        str(round(float(v) * s.f, 2)) for v in m.group(1).split()) + ";", css)


def tape(s, x0, y0, n, filled, part=(1.6, 0.8), pitch=4.0, w=8.0, cover=True):
    """8 mm carrier tape running in +x from (x0, y0), n pockets; filled(i) says whether pocket i holds a part.
    Per EIA-481: sprocket holes 1.5 mm on a 4 mm pitch, 1.75 mm from the top edge; each pocket centered 3.5 mm from
    the sprocket-hole line and 2 mm along from a hole. A chip part (part = length, width) lies across the tape, its
    terminations towards and away from the sprocket holes."""
    L = n * pitch
    s.rect(x0, y0, L, w, "tape")
    k = 1
    while k * 4.0 < L - 0.5:
        s.circle(x0 + k * 4.0, y0 + 1.75, 0.75, "sprk")
        k += 1
    for i in range(n):
        cx, cy = x0 + pitch * (i + 0.5), y0 + 1.75 + 3.5
        s.rect(cx - 0.55, cy - 0.95, 1.1, 1.9, "pocket", rx=0.1)
        if filled(i):
            pl, pw = part
            s.rect(cx - pw / 2, cy - pl / 2, pw, pl, "capbody")
            s.rect(cx - pw / 2, cy - pl / 2, pw, 0.3, "capterm")
            s.rect(cx - pw / 2, cy + pl / 2 - 0.3, pw, 0.3, "capterm")
    if cover:
        s.rect(x0, y0 + 3.3, L, 3.9, "cover")


def feed_arrow(s, x1, x2, y, label):
    """Arrow from x1 to x2 (mm) at height y showing the direction the tape travels into the feeder."""
    s.line(x1, y, x2, y, "lead")
    X, Y = s.X(x2), s.Y(y)
    a = 8 * s.f
    s.d.append(dw.Lines(X, Y, X - a, Y - a / 2, X - a, Y + a / 2, close=True, class_="dot"))
    s.text(label, x1, y - 8 * s.f / s.scale, size=12, cls="muted")


def packaging():
    # D56 (PCB-DFA-089, 101): the four ways parts arrive. Each panel has its own scale.
    s = sheet(980, 900, "How surface-mount parts arrive: tape, reel, tube and tray",
              "Four panels, not to the same scale. Top: 8 mm carrier tape, enlarged, drawn to scale: sprocket holes "
              "1.5 mm across every 4 mm along one edge only, pockets every 4 mm holding chip parts lying across the tape, "
              "with their ends towards and away from the sprocket holes, a clear cover tape "
              "sealed over the pockets, and empty pockets at the leading end as leader, with an arrow showing the direction "
              "of feed. Middle left: a 178 mm (7 in) reel "
              "with tape coming off the top to the right, so the reel turns clockwise. Middle right: a plastic tube about 500 mm long holding a row of SOIC chips, "
              "with a stopper in each end. Bottom: a tray about 323 by 136 mm with a grid of pockets, each holding a "
              "large chip.", scale=7.5, ox=90, oy=120)
    # Panel A: carrier tape, to scale at 7.5 px/mm
    tape(s, 0, 0, 14, lambda i: i <= 8)
    s.text("Carrier tape, 8 mm wide (enlarged)", 0, -8.5, size=14, weight="600")
    s.dim_v(0, 8, -3.0, "8 mm", ext_from=0, text_left=True)
    s.dim_h(14, 18, 10.2, "4 mm pitch", ext_from=8.0, text_above=False)
    feed_arrow(s, 57.5, 70, 5.25, "Direction of feed")
    s.balloon(1, (8.0, 1.75), (s.X(8.0), s.Y(-4.5)), "Sprocket holes on one side only",
              "So tape up to 24 mm wide loads only one way")
    s.balloon(2, (2.0, 5.25), (s.X(2.0), s.Y(14.2)), "One part per pocket")
    s.balloon(3, (38.0, 3.6), (s.X(38.0), s.Y(-4.5)), "Cover tape", "Peeled back at the machine")
    s.balloon(4, (50.0, 5.25), (s.X(50.0), s.Y(14.2)), "Empty pockets at the leading end: leader",
              "Threaded into the feeder first")
    # Panel B: reel (1 px/mm), drawn in px
    d = s.d
    L = lh(s, 12)
    top = 300                                   # titles of panels B and C
    cx, cy, R = 150, top + 125, 89
    d.append(dw.Circle(cx, cy, R, class_="reel"))
    d.append(dw.Circle(cx, cy, 30, class_="hub"))
    d.append(dw.Circle(cx, cy, 6.5, class_="hub"))
    d.append(dw.Circle(cx, cy, 60, class_="thin"))
    d.append(dw.Rectangle(cx, cy - R, 210, 8, class_="tape"))
    # clockwise arrow round the hub: an arc from 200 to 320 degrees (screen angles), arrowhead along its tangent
    import math
    ra, a0, a1 = 46, math.radians(200), math.radians(320)
    x0, y0 = cx + ra * math.cos(a0), cy + ra * math.sin(a0)
    x1, y1 = cx + ra * math.cos(a1), cy + ra * math.sin(a1)
    p = dw.Path(class_="lead", stroke_width=s.sw(1.6))
    p.M(x0, y0).A(ra, ra, 0, 0, 1, x1, y1)
    d.append(p)
    tx, ty = -math.sin(a1), math.cos(a1)                               # direction of travel at the end
    nx, ny = math.cos(a1), math.sin(a1)                                # outward, across the arc
    tip = (x1 + 9 * tx, y1 + 9 * ty)
    d.append(dw.Lines(*tip, x1 - 4 * tx + 6 * nx, y1 - 4 * ty + 6 * ny, x1 - 4 * tx - 6 * nx, y1 - 4 * ty - 6 * ny,
                      close=True, class_="dot"))
    d.append(dw.Text("Reel, 178 mm (7 in)", s.fs(14), 60, top, class_="ink", font_weight="600"))
    for i, t in enumerate(("Thousands of parts on one tape", "Feeds one pocket at a time",
                           "Larger reels: 330 mm (13 in)")):
        d.append(dw.Text(t, s.fs(12), 60, cy + R + 32 + i * L, class_="muted"))
    # Panel C: tube (0.75 px/mm)
    tx, ty, tl, th = 430, top + 90, 500 * 0.75, 18
    d.append(dw.Text("Tube, about 500 mm long", s.fs(14), tx, top, class_="ink", font_weight="600"))
    for i in range(int((tl - 20) / 6.5)):
        d.append(dw.Rectangle(tx + 12 + i * 6.5, ty + 4, 4.6, th - 8, class_="part"))
    d.append(dw.Rectangle(tx, ty, tl, th, class_="tube"))
    for x in (tx - 4, tx + tl - 6):
        d.append(dw.Rectangle(x, ty + 2, 10, th - 4, rx=2, class_="stopper"))
    d.append(dw.Text("50–100 parts in a row, fed by vibration", s.fs(12), tx, ty + th + 32, class_="muted"))
    d.append(dw.Text("Symmetrical: can be loaded backwards", s.fs(12), tx, ty + th + 32 + L, class_="muted"))
    d.append(dw.Text("Stopper", s.fs(12), tx + tl, ty - 12, text_anchor="end", class_="muted"))
    # Panel D: tray (0.75 px/mm): JEDEC outline 322.6 x 135.9 mm
    gx, gy, gw, gh = 430, ty + th + 32 + L + 70, 322.6 * 0.75, 135.9 * 0.75
    d.append(dw.Text("Tray, about 323 × 136 mm", s.fs(14), gx, gy - 16, class_="ink", font_weight="600"))
    d.append(dw.Rectangle(gx, gy, gw, gh, rx=4, class_="tray"))
    cols, rows = 8, 3
    cw, ch = (gw - 24) / cols, (gh - 20) / rows
    for r in range(rows):
        for c in range(cols):
            x, y = gx + 12 + c * cw, gy + 10 + r * ch
            d.append(dw.Rectangle(x + 2, y + 2, cw - 4, ch - 4, class_="tcell"))
            m = min(cw, ch) - 12
            d.append(dw.Rectangle(x + (cw - m) / 2, y + (ch - m) / 2, m, m, class_="part"))
            d.append(dw.Circle(x + (cw - m) / 2 + 4, y + (ch - m) / 2 + 4, 1.6, class_="dot"))
    d.append(dw.Text("For large or delicate chips (QFPs, BGAs)", s.fs(12), gx, gy + gh + 32, class_="muted"))
    d.append(dw.Text("Pin 1 the same way in every pocket", s.fs(12), gx, gy + gh + 32 + L, class_="muted"))
    ky = gy + gh + 32 + L + 70
    y1 = s.key(60, ky, width=410, only=(1, 2))
    y2 = s.key(510, ky, width=410, title="", only=(3, 4))
    y = max(y1, y2) + 40 * s.f
    s.note("Panels not to the same scale; the tape is enlarged and drawn to scale.", 60, y)
    s.note("Tape and reel sizes per EIA-481.", 60, y + lh(s))
    fit(s, y + lh(s))
    s.save(out(56, "packaging-types"))


def pads(s, add, cls, items):
    for x, y, w, h in items:
        add(s.R(x - w / 2, y - h / 2, w, h, cls))


def dual_footprint():
    # D57 (PCB-DFA-084): two ways for a board to take either of two packages, drawn to scale.
    s = sheet(980, 830, "A footprint that takes either of two packages",
              "Drawn to scale, plan views. Left: a SOT-23-6 footprint, six pads 0.6 by 1.1 mm on a 0.95 mm pitch in "
              "two rows 2.5 mm apart, with the six pads of a small 1.0 by 0.8 mm leadless package in the space between "
              "the rows; each leadless pad is joined to the SOT-23 pad beside it by a short trace under the mask. "
              "Either package can be fitted. Right: for packages that can't share space, a SOT-23-6 footprint and an "
              "SC-70-6 footprint side by side, labeled U1 and U2, each pin wired to the same net as its partner "
              "(traces not shown); the BOM fits one and marks the other DNP.", scale=55, ox=230, oy=250)
    sot = [(sx * 1.25, (k - 1) * 0.95, 1.1, 0.6) for sx in (-1, 1) for k in range(3)]
    son = [(sx * 0.33, (k - 1) * 0.35, 0.3, 0.2) for sx in (-1, 1) for k in range(3)]

    def geom_a(add, cu, fr4):
        add(s.R(-2.6, -2.4, 5.2, 4.8, fr4))
        for (x, y, w, h), (x2, y2, _, _) in zip(sot, son):
            add(s.PL([(x - (0.45 if x > 0 else -0.45), y), (x2 + (0.1 if x > 0 else -0.1), y2)], "s-" + cu, 0.15))
        pads(s, add, cu, sot)
        pads(s, add, cu, son)
    opens = [s.R(x - w / 2 - 0.05, y - h / 2 - 0.05, w + 0.1, h + 0.1, "bg") for x, y, w, h in sot + son]
    s.board_view((-2.6, -2.4, 5.2, 4.8), geom_a, openings=opens)
    for x, y, w, h in [(-1.0, -1.85, 2.0, 0.12), (-1.0, 1.73, 2.0, 0.12)]:
        s.rect(x, y, w, h, "silkscreen")
    s.circle(-1.95, -1.95, 0.12, "silkscreen")
    s.text("One footprint, two packages", 0, -3.7, size=14, anchor="middle", weight="600")
    s.dim_h(-1.25, 1.25, -2.85, "2.5", ext_from=-1.25)
    s.dim_v(-1.25, -0.30, -3.1, "0.95", ext_from=-1.8, text_left=True)
    s.balloon(1, (-0.6, 0.62), (s.X(-0.6), s.Y(3.4)), "Short trace joins each pair", "Under the mask")
    s.balloon(2, (0.33, 0.35), (s.X(0.33), s.Y(3.4)), "Leadless package pads", "1.0 × 0.8 mm package, example")
    s.balloon(3, (1.45, 0.95), (s.X(1.45), s.Y(3.4)), "SOT-23-6 pads", "Example sizes, after IPC-7351")
    # Right: side by side
    ox = 6.0
    sc = [(ox + 4.2 + sx * 0.95, (k - 1) * 0.65, 0.9, 0.4) for sx in (-1, 1) for k in range(3)]
    sot2 = [(ox + x, y, w, h) for x, y, w, h in sot]

    def geom_b(add, cu, fr4):
        add(s.R(ox - 2.6, -2.4, 9.0, 4.8, fr4))
        pads(s, add, cu, sot2)
        pads(s, add, cu, sc)
    opens = [s.R(x - w / 2 - 0.05, y - h / 2 - 0.05, w + 0.1, h + 0.1, "bg") for x, y, w, h in sot2 + sc]
    s.board_view((ox - 2.6, -2.4, 9.0, 4.8), geom_b, openings=opens)
    for x0, x1, y in ((ox - 1.0, ox + 1.0, -1.85), (ox - 1.0, ox + 1.0, 1.73), (ox + 3.6, ox + 4.8, -1.35), (ox + 3.6, ox + 4.8, 1.23)):
        s.rect(x0, y, x1 - x0, 0.12, "silkscreen")
    s.text("U1", s.X(ox), s.Y(-2.0), size=13, cls="silkscreen", anchor="middle", px=True)
    s.text("U2", s.X(ox + 4.2), s.Y(-1.5), size=13, cls="silkscreen", anchor="middle", px=True)
    s.text("Two footprints, one fitted", ox + 1.9, -3.7, size=14, anchor="middle", weight="600")
    s.balloon(4, (ox + 1.45, 0.95), (s.X(ox + 1.45), s.Y(3.4)), "U1: SOT-23-6", "Fitted, or DNP")
    s.balloon(5, (ox + 5.15, 0.65), (s.X(ox + 5.15), s.Y(3.4)), "U2: SC-70-6, 0.65 mm pitch",
              "DNP when U1 is fitted")
    ky = 590
    y1 = s.key(40, ky, width=440, only=(1, 2, 3))
    y2 = s.key(520, ky, width=420, title="", only=(4, 5))
    y = max(y1, y2) + 50 * s.f
    s.legend(40, y, [("cu-exposed", "Exposed copper"), ("mask-on-cu", "Mask over copper"),
             ("mask-on-fr4", "Mask over FR4"), ("silkscreen", "Silkscreen")])
    for i, t in enumerate(("Drawn to scale. Dimensions in mm; pad sizes are examples.",
                           "Right: traces not shown; each pin shares a net with its partner.",
                           "Use a combined footprint only where the part maker publishes one;",
                           "name the fitted package on the BOM.")):
        s.note(t, 330, y + i * lh(s))
    fit(s, y + 3 * 22 * s.f)
    s.save(out(57, "dual-footprint"))


def cut_tape():
    # D58 (PCB-DFA-101, 105): consigned cut tape: one long strip vs strips too short to handle. Every pocket filled,
    # as cut tape nearly always arrives (Chris, 2026-11-08): no leader is expected.
    s = sheet(980, 720, "Consigned cut tape: long strips, not short ones",
              "Drawn to scale, 8 mm carrier tape seen from above, with a part in every pocket. Top: one continuous "
              "strip 240 mm long, with the round sprocket holes along the top and an arrow showing the direction of feed "
              "to the right (EIA-481), so the right-hand end goes into the feeder first; 50 mm is marked as the "
              "shortest strip that can be handled and 150 mm as the preferred minimum, and the parts at both ends "
              "are marked as the ones that may be lost. Bottom: the same kind of parts sent as five strips of ten, each 40 mm long, shorter than the "
              "50 mm minimum.", scale=3.4, ox=50, oy=160)
    L = 240
    tape(s, 0, 0, 60, lambda i: True)
    s.text("✓ One continuous strip", 0, -19, size=14, weight="600", cls="ink")
    s.dim_h(0, 50, 12, "50 mm minimum", ext_from=8, text_above=False)
    s.dim_h(0, 150, 24, "150 mm or more, preferred", ext_from=8, text_above=False)
    y2 = 56
    s.text("✗ Strips of ten, 40 mm each", 0, y2 - 4, size=14, weight="600", cls="ink")
    for k in range(5):
        tape(s, k * 47, y2, 10, lambda i: True)
    s.dim_h(47, 87, y2 + 12, "40 mm", ext_from=y2 + 8, text_above=False)
    feed_arrow(s, L + 2, L + 14, 5.25, "Feed")
    s.balloon(1, (2, 5.25), (s.X(2), s.Y(-10)), "Last part in: the trailing end", "May be lost")
    s.balloon(2, (122, 3.6), (s.X(122), s.Y(-10)), "A part in every pocket", "Usually no empty leader on cut tape")
    s.balloon(3, (L - 2, 5.25), (s.X(L - 2), s.Y(-10)), "First part in: the leading end",
              "May be lost; buy a little extra (attrition)")
    s.balloon(4, (96, y2 + 5.25), (s.X(96), s.Y(y2 + 20)), "Each strip loaded or spliced by hand",
              "Shorter than 50 mm: too short to load")
    ky = s.Y(y2 + 20) + 70 * s.f
    y1 = s.key(50, ky, width=430, only=(1, 2))
    y2_ = s.key(520, ky, width=430, title="", only=(3, 4))
    y = max(y1, y2_) + 50 * s.f
    s.legend(50, y, [("tape", "Carrier tape"), ("cover", "Cover tape"), ("capbody", "Part")])
    for i, t in enumerate(("Drawn to scale: 8 mm tape, 4 mm pitch.",
                           "Shortest strip: 50 mm minimum, 150 mm or more preferred",
                           "(Worthington Assembly and CircuitHub).",
                           "Feed direction per EIA-481: cover tape up, round sprocket",
                           "holes at the top, unreeling to the right.")):
        s.note(t, 330, y + i * lh(s))
    fit(s, y + 4 * lh(s))
    s.save(out(58, "cut-tape-length"))


def soic_top(s, cx, cy, flip):
    """SOIC-8 seen from above, 4.9 mm long in x; pin-1 dot at the left end unless flipped."""
    L, W = 4.9, 3.9
    s.rect(cx - L / 2, cy - W / 2, L, W, "part")
    for k in range(4):
        x = cx - 1.905 + k * 1.27
        for sy in (-1, 1):
            s.rect(x - 0.2, cy + sy * W / 2 - (0.0 if sy > 0 else 1.0), 0.4, 1.0, "term")
    dx = -1.6 if not flip else 1.6
    s.circle(cx + dx, cy - 0.9, 0.35, "bg")


def tubes():
    # D59 (PCB-DFA-101): a tube refilled with every part the same way, and one with parts mixed.
    s = sheet(980, 600, "Tubes: every part facing the same way",
              "Drawn to scale, seen from above, part of a tube of SOIC-8 chips, the tube shortened. Top: every chip "
              "has its pin-1 dot at the left. Bottom: a tube refilled by hand with some chips turned end for end, so "
              "their pin-1 dots are at the right; the assembler must empty and reload it.", scale=11, ox=100, oy=150)
    for row, (title, flips) in enumerate((("✓ All the same way", [False] * 10),
                                          ("✗ Mixed", [False, True, False, False, True, True, False, True,
                                                       False, False]))):
        y = row * 14
        s.text(title, 0, y - (9.5 if row == 0 else 4.6), size=14, weight="600")
        for i, f in enumerate(flips):
            soic_top(s, 4 + i * 6.2, y, f)
        s.rect(0, y - 3.2, 64, 6.4, "tube")
        s.rect(-1.2, y - 2.6, 1.6, 5.2, "stopper", rx=0.3)
        s.text("tube continues…", 65, y + 0.5, size=12, cls="muted")
    s.balloon(1, (10.2 - 1.6, -0.9), (s.X(10.2 - 1.6), s.Y(-6.0)), "Pin-1 dot", "Every part the same way round")
    s.balloon(2, (10.2 + 1.6, 14 - 0.9), (s.X(10.2 + 1.6), s.Y(22.5)), "Part turned end for end",
              "The whole tube must be emptied and reloaded")
    s.balloon(3, (-1.2, 0), (s.X(-1.2) - 50 * s.f, s.Y(0)), "Stopper")
    ky = s.Y(22.5) + 70 * s.f
    y1 = s.key(60, ky, width=430, only=(1, 2))
    y2 = s.key(530, ky, width=420, title="", only=(3,))
    y = max(y1, y2) + 40 * s.f
    s.note("Drawn to scale: SOIC-8, 4.9 × 3.9 mm, tube shortened.", 60, y)
    s.note("A tube is symmetrical, so it can also be loaded into the feeder backwards.", 60, y + lh(s))
    fit(s, y + lh(s))
    s.save(out(59, "tube-orientation"))


def moisture_bag():
    # D60 (PCB-DFA-094, 102): what goes in a moisture barrier bag. Not to scale.
    s = sheet(980, 960, "What goes in a moisture barrier bag",
              "Not to scale. A moisture barrier bag, heat-sealed across the top, holding a reel of parts, a desiccant "
              "pouch and a humidity indicator card with three spots marked 5%, 10% and 60%, all blue (dry). A "
              "moisture-sensitivity caution label on the outside gives the level, the floor life and the seal date. "
              "A note says to push the air out but not to vacuum-seal tight.")
    d = s.d
    bx, by, bw, bh = 80, 70, 470, 560
    d.append(dw.Rectangle(bx, by, bw, bh, rx=10, class_="bag"))
    d.append(dw.Rectangle(bx, by + 18, bw, 16, class_="seal"))
    d.append(dw.Circle(bx + 190, by + 280, 150, class_="reel"))
    d.append(dw.Circle(bx + 190, by + 280, 50, class_="hub"))
    d.append(dw.Circle(bx + 190, by + 280, 11, class_="hub"))
    d.append(dw.Circle(bx + 190, by + 280, 100, class_="thin"))
    d.append(dw.Rectangle(bx + 330, by + 90, 125, 80, rx=8, class_="desic"))
    d.append(dw.Text("DESICCANT", s.fs(12), bx + 392.5, by + 137, text_anchor="middle", class_="cardink", font_weight="600"))
    cx0, cy0 = bx + 330, by + 200
    d.append(dw.Rectangle(cx0, cy0, 125, 170, rx=4, class_="card"))
    d.append(dw.Text("HUMIDITY", s.fs(10.5), cx0 + 62.5, cy0 + 20, text_anchor="middle", class_="cardink", font_weight="600"))
    for k, pct in enumerate(("60%", "10%", "5%")):
        yy = cy0 + 50 + k * 42
        d.append(dw.Circle(cx0 + 35, yy, 14, class_="dry"))
        d.append(dw.Text(pct, s.fs(12), cx0 + 60, yy + 6, class_="cardink"))
    lx, ly = bx + 30, by + 445
    L = lh(s)
    d.append(dw.Rectangle(lx, ly, 380, 18 + 4 * L, rx=4, class_="caution"))
    for i, (t, w) in enumerate((("CAUTION: MOISTURE-SENSITIVE", "600"), ("LEVEL 3", "600"),
                                ("Floor life 168 h at ≤ 30 °C / 60% RH", None), ("Bag seal date: ____", None))):
        kw = {"font_weight": w} if w else {}
        d.append(dw.Text(t, s.fs(11), lx + 12, ly + 6 + (i + 1) * L, class_="cardink", **kw))

    def bal(n, tx, ty, ax, ay, label, detail=""):
        s.balloon(n, ((tx - s.ox) / s.scale, (ty - s.oy) / s.scale), (ax, ay), label, detail)
    bal(1, bx + 400, by + 26, 620, 96, "Heat seal", "Better than tape, which can peel")
    bal(2, bx + 440, by + 105, 620, by + 105, "Desiccant", "Fresh each time the bag is resealed")
    bal(3, cx0 + 110, cy0 + 71, 620, cy0 + 71, "Humidity indicator card",
        "A spot turns pink when that humidity is passed")
    bal(4, bx + 250, by + 420, 620, 480, "Reel of parts")
    bal(5, lx + 370, ly + 30, 620, 560, "Caution label on the outside", "Level, floor life, seal date")
    ky = by + bh + 60 * s.f
    y = s.key(80, ky, width=440)
    for i, t in enumerate(("Not to scale.", "Push the air out, but don't vacuum-seal tight:",
                           "the desiccant needs some air to work.", "Use a bag made for electronics: moisture barrier",
                           "and static shielding together.")):
        s.note(t, 570, ky + 10 * s.f + 30 * s.f + i * lh(s))
    fit(s, y)
    s.save(out(60, "moisture-bag"))


if __name__ == "__main__":
    packaging()
    dual_footprint()
    cut_tape()
    tubes()
    moisture_bag()
    print("written to", OUT)

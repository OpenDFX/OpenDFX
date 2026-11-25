"""Part 6 diagrams (D61, D62, D64) in the OpenDFX style.
Run: python3 tools/diagrams/part6_diagrams.py         (writes trials/python-N-<name>.svg for review)
     python3 tools/diagrams/part6_diagrams.py --book  (writes book/06-test-and-programming/images/<name>.svg)"""
from pathlib import Path
import math
import re
import sys

import drawsvg as dw
import opendfx_draw
from opendfx_draw import Sheet

BOOK = "--book" in sys.argv
OUT = (Path(__file__).parent / "trials") if not BOOK else (
    Path(__file__).parents[2] / "book" / "06-test-and-programming" / "images")
OUT.mkdir(exist_ok=True)

# Test-equipment colors (not board colors): probe plates, probes, chips in a block diagram.
EXTRA = """
.plate  { fill: #c9b98f; stroke: #8a7a52; stroke-width: 1; }
.probe  { fill: #b9c0c7; stroke: #5b636b; stroke-width: 0.8; }
.recept { fill: #d9b44a; stroke: #8a6d45; stroke-width: 0.8; }
.chip   { fill: #3b3f45; }
.chipin { fill: #ffffff; }
.pin    { fill: #c9ccd1; }
.wire   { stroke: #1d2125; stroke-width: 1.6; fill: none; }
.wire2  { stroke: #2563a8; stroke-width: 1.6; fill: none; }
.wire3  { stroke: #b23a2b; stroke-width: 1.6; fill: none; }
.good   { fill: #2f9e4f; }
.bad    { fill: #b23a2b; }
.bad-s  { stroke: #b23a2b; stroke-width: 2.4; fill: none; }
.capcan { fill: #2c3e66; stroke: #1b2744; stroke-width: 0.8; }
.capsleeve { fill: #c9ccd1; }
.conn   { fill: #26292d; }
.membox { fill: #c9ccd1; }   /* a chip without boundary scan: light gray in both modes */
.memtxt { fill: #1d2125; }   /* dark text on it in both modes, 10 to 1 (M13a) */
@media (prefers-color-scheme: dark) {
  .plate  { fill: #8a7a52; stroke: #c9b98f; }
  .chip   { fill: #5d646d; }
  .wire   { stroke: #e8eaed; }
  .wire2  { stroke: #79aef0; }
  .wire3  { stroke: #f08a7a; }
  .good   { fill: #5cc47d; }
  .bad    { fill: #f08a7a; }
  .bad-s  { stroke: #f08a7a; }
  .capcan { fill: #4a6296; stroke: #9fb3dd; }
  .conn   { fill: #4a5058; }
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


def notes(s, x, y, lines):
    """Notes, one per line, from y; returns the y of the last line."""
    for i, t in enumerate(lines):
        s.note(t, x, y + i * lh(s))
    return y + (len(lines) - 1) * lh(s)


def print_css(s, css):
    """This script's own styles with stroke widths and dashes sized for print, as the kit does for its own (DRW1)."""
    css = re.sub(r"stroke-width: ([\d.]+)(?!px)", lambda m: f"stroke-width: {s.sw(float(m.group(1)))}", css)
    return re.sub(r"stroke-dasharray: ([\d. ]+);", lambda m: "stroke-dasharray: " + " ".join(
        str(round(float(v) * s.f, 2)) for v in m.group(1).split()) + ";", css)


def test_points():
    # D61 (PCB-DFT-008, PCB-DFT-009): test point size, spacing and keep-outs, plan view, drawn to scale.
    s = sheet(1000, 860, "Test point size, spacing and keep-outs",
              "Drawn to scale, plan view of the corner of a board with the bottom edge of the board along the bottom. "
              "Three round test points TP1 to TP3 sit in a row, each a copper pad 1.0 mm in diameter (0.9 mm minimum) with the "
              "solder mask cleared round it, 2.54 mm apart center to center (1.9 mm minimum), each fed by a trace under "
              "the mask. An 0603 resistor sits 1 mm from TP1, the minimum gap to a short part. A fourth test point, TP4, "
              "is kept 5 mm from a tall radial capacitor 8 mm in diameter; a probe can't reach the shaded 5 mm zone around it. The "
              "strip along the board edge that conveyors and fixtures grip is marked at 3 mm (minimum) and 5 mm "
              "(recommended); no test point is inside it.",
              scale=20, ox=60, oy=70)
    W, H = 36.0, 22.0
    tps = [(6.0, 12.0), (8.54, 12.0), (11.08, 12.0)]
    tp4 = (16.4, 12.0)
    cap = (26.0, 9.5)
    res = (3.25, 12.0)          # 0603 resistor, horizontal; right pad edge at 4.5, 1.0 mm from TP1's edge (5.5)

    def geom(add, cu, fr4):
        add(s.R(0, 0, W, H, fr4))
        for x, y in tps + [tp4]:
            add(s.PL([(x, y), (x, 0)], "s-" + cu, 0.25))
        for dx in (-0.8, 0.8):  # 0603 pads 0.9 x 0.95 on 1.6 mm centers
            add(s.R(res[0] + dx - 0.45, res[1] - 0.475, 0.9, 0.95, cu))
        add(s.PL([(res[0] - 0.8, res[1]), (res[0] - 0.8, 0)], "s-" + cu, 0.25))
        add(s.PL([(res[0] + 0.8, res[1]), (res[0] + 0.8, 0)], "s-" + cu, 0.25))
        for x, y in tps + [tp4]:
            add(s.C(x, y, 0.5, cu))
        for dx in (-1.75, 1.75):  # radial capacitor, 3.5 mm lead spacing
            add(s.C(cap[0] + dx, cap[1], 0.9, cu))
    opens = [s.C(x, y, 0.6, "bg") for x, y in tps + [tp4]]
    opens += [s.R(res[0] + dx - 0.5, res[1] - 0.525, 1.0, 1.05, "bg") for dx in (-0.8, 0.8)]
    opens += [s.C(cap[0] + dx, cap[1], 1.0, "bg") for dx in (-1.75, 1.75)]
    s.board_view((0, 0, W, H), geom, openings=opens,
                 holes=[(cap[0] - 1.75, cap[1], 0.45), (cap[0] + 1.75, cap[1], 0.45)])
    # parts and silkscreen
    # 0603 chip resistor: black body, tinned ends (the same look as the other drawings)
    s.rect(res[0] - 0.8, res[1] - 0.4, 1.6, 0.8, "part")
    s.rect(res[0] - 0.8, res[1] - 0.4, 0.32, 0.8, "term")
    s.rect(res[0] + 0.48, res[1] - 0.4, 0.32, 0.8, "term")
    s.d.append(dw.Circle(s.X(cap[0]), s.Y(cap[1]), s.L(4.15), class_="s-silkscreen", stroke_width=s.sw(2)))
    s.text("R1", s.X(res[0]), s.Y(res[1] - 1.1), size=12, cls="silkscreen", anchor="middle", px=True)
    s.text("C1", s.X(cap[0]), s.Y(cap[1] + 2.9), size=12, cls="silkscreen", anchor="middle", px=True)
    s.text("+", s.X(cap[0] - 3.0), s.Y(cap[1] + 0.35), size=14, cls="silkscreen", anchor="middle", px=True)
    for i, (x, y) in enumerate(tps + [tp4], 1):
        s.text(f"TP{i}", s.X(x + 0.75), s.Y(y - 0.85), size=12, cls="silkscreen", px=True)
    # keep-out round the tall part and the gripped edge strip
    zc = s.clipped([s.R(0, 0, W, H, "bg")])
    zc.append(dw.Circle(s.X(cap[0]), s.Y(cap[1]), s.L(4.0 + 5.0), class_="zone"))
    zc.append(dw.Circle(s.X(cap[0]), s.Y(cap[1]), s.L(4.0 + 5.0), class_="zone-s"))
    s.d.append(zc)
    s.dim_h(cap[0] - 9.0, cap[0] - 4.0, cap[1], "5")
    s.line(0, H - 3, W, H - 3, "ko-min")
    s.line(0, H - 5, W, H - 5, "ko-rec")
    s.line(0, H, W, H, "edge")
    # dimensions
    s.dim_h(tps[1][0], tps[2][0], 10.0, "2.54", ext_from=11.5)
    s.dim_h(tp4[0] - 0.5, tp4[0] + 0.5, 15.0, "Ø 1.0", ext_from=12.5, text_side="left")
    s.dim_h(4.5, 5.5, 15.0, "1.0", ext_from=12.5, text_side="left")
    s.dim_v(H - 3, H, W + 1.2, "3", ext_from=W)
    s.dim_v(H - 5, H, W + 4.4, "5", ext_from=W)
    # balloons
    s.balloon(1, (tps[1][0] + 0.35, 12.35), (s.X(8.5), 600), "Test point 1.0 mm in diameter, 2.54 mm apart",
              "At least 0.9 mm in diameter and 1.9 mm apart")
    s.balloon(2, (res[0] + 0.8, 12.0), (s.X(2.0), 600), "Short part: at least 1 mm away")
    s.balloon(3, (cap[0] - 6.5, 14.0), (s.X(22.0), 600), "Tall part: probes can't reach this zone",
              "5 mm from parts taller than 5.7 mm (IPC-2221C)")
    s.balloon(4, (13.0, H - 4.0), (s.X(13.0), 600), "Edge strip held by conveyors and fixtures",
              "3 mm minimum, 5 mm recommended")
    ky = 600 + 70 * s.f
    y1 = s.key(60, ky, width=440, only=(1, 2))
    y2 = s.key(540, ky, width=420, title="", only=(3, 4))
    y = max(y1, y2) + 50 * s.f
    s.legend(60, y, [("cu-exposed", "Exposed copper"), ("mask-on-cu", "Mask over copper"),
                     ("mask-on-fr4", "Mask over FR4"), ("silkscreen", "Silkscreen"), ("drill", "Hole")])
    notes(s, 340, y, ("Drawn to scale. Dimensions in mm.", "All test points on one side of the board.",
                      "Test points: mask cleared, no paste, name in silkscreen."))
    fit(s, y + 4 * 22 * s.f)
    s.save(out(61, "test-points"))


def probe_access():
    # D62 (PCB-DFT-009, PCB-DFT-011): probes reaching a board, side view, drawn to scale.
    s = sheet(980, 880, "Probes reaching a board in a bed-of-nails fixture",
              "Drawn to scale, side view. A 1.6 mm board carries its parts on top: an 0603 resistor, a radial "
              "capacitor 8 mm in diameter and 11.5 mm tall, and a connector 8 mm tall. On the left, all the test points are "
              "on the bottom of the board, the side with no parts, and spring-loaded probes rise from one plate of "
              "probes 10 mm thick, each in a replaceable receptacle; every probe is the same short length. On the "
              "right, the same board with one test point on top, 1 mm from the tall capacitor: a probe from a top "
              "plate needs a cut-out round the tall parts and a probe longer than the capacitor, squeezed into a 1 mm "
              "gap. It's marked to avoid.",
              scale=10, ox=50, oy=90)
    T = 1.6

    def board(x0, w, y0, tp_bottom, tp_top=()):
        s.rect(x0, y0, w, T, "fr4-exposed")
        s.rect(x0, y0 - 0.05, w, 0.05, "mask-on-fr4")
        s.rect(x0, y0 + T, w, 0.05, "mask-on-fr4")
        for x in tp_bottom:
            s.rect(x - 0.5, y0 + T, 1.0, 0.07, "cu-exposed")
        for x in tp_top:
            s.rect(x - 0.5, y0 - 0.07, 1.0, 0.07, "cu-exposed")

    def parts(x0, y0):
        s.rect(x0 + 4.2, y0 - 0.45, 1.6, 0.45, "part")                 # 0603 resistor: black body, tinned ends
        s.rect(x0 + 4.2, y0 - 0.45, 0.32, 0.45, "term")
        s.rect(x0 + 5.48, y0 - 0.45, 0.32, 0.45, "term")
        s.rect(x0 + 13.0, y0 - 11.5, 8.0, 11.5, "capcan", rx=0.6)       # radial can
        s.rect(x0 + 13.0, y0 - 11.5, 8.0, 0.6, "capsleeve")
        s.rect(x0 + 29.0, y0 - 8.0, 8.0, 8.0, "conn", rx=0.3)          # connector
        for dx in (15.25, 18.75):
            s.rect(x0 + dx - 0.25, y0 + T, 0.5, 1.0, "solder")
        for dx in (30.0, 32.5, 35.0):
            s.rect(x0 + dx - 0.3, y0 + T, 0.6, 1.4, "pin")

    def probe(x, ytip, length, up=True):
        # tip at ytip; barrel 1.0 mm, plunger 0.6 mm, receptacle 1.6 mm
        if up:
            s.rect(x - 0.3, ytip, 0.6, 3.0, "probe")
            s.rect(x - 0.5, ytip + 3.0, 1.0, length - 3.0, "probe")
            s.d.append(dw.Lines(s.X(x - 0.3), s.Y(ytip), s.X(x), s.Y(ytip - 0.5), s.X(x + 0.3), s.Y(ytip),
                                close=True, class_="probe"))
        else:
            s.rect(x - 0.3, ytip - 3.0, 0.6, 3.0, "probe")
            s.rect(x - 0.5, ytip - length, 1.0, length - 3.0, "probe")
            s.d.append(dw.Lines(s.X(x - 0.3), s.Y(ytip), s.X(x), s.Y(ytip + 0.5), s.X(x + 0.3), s.Y(ytip),
                                close=True, class_="probe"))

    yb = 30.0
    # left: good
    xl = 2.0
    tpl = [xl + 3.0, xl + 8.0, xl + 23.0, xl + 37.0]
    board(xl, 40.0, yb, tpl)
    parts(xl, yb)
    plate_y = yb + T + 9.0
    s.rect(xl - 1, plate_y, 42.0, 10.0, "plate")
    for x in tpl:
        s.rect(x - 0.8, plate_y - 1.0, 1.6, 11.0, "recept")
        probe(x, yb + T + 0.6, plate_y - (yb + T + 0.6) + 2.0)
    s.text("✓ Test points on the bottom", xl + 20, yb - 31.0, size=14, anchor="middle", weight="600")
    s.text("One plate, short probes", xl + 20, yb - 31.0 + lh(s, 14) / s.scale, size=12, cls="muted",
           anchor="middle")
    # right: avoid
    xr = 46.0
    tpx = xr + 11.5
    board(xr, 40.0, yb, [], tp_top=[tpx])
    parts(xr, yb)
    top_y = yb - 11.5 - 3.0
    s.rect(xr - 1, top_y - 10.0, 42.0, 10.0, "plate")
    s.rect(xr + 12.5, top_y - 5.0, 26.0, 5.0, "bg")          # cut-out in the top plate over the tall parts
    s.d.append(dw.Rectangle(s.X(xr + 12.5), s.Y(top_y - 5.0), s.L(26.0), s.L(5.0), class_="zone-s"))
    probe(tpx, yb - 0.6, (yb - 0.6) - (top_y - 6.0), up=False)
    s.rect(tpx - 0.8, top_y - 7.0, 1.6, 7.0, "recept")
    s.text("✗ Test point on top", xr + 20, yb - 31.0, size=14, anchor="middle", weight="600")
    s.text("1 mm from a tall part", xr + 20, yb - 31.0 + lh(s, 14) / s.scale, size=12, cls="muted",
           anchor="middle")
    s.dim_h(tpx + 0.5, xr + 13.0, yb - 2.0, "1.0", text_side="left")
    s.dim_v(yb - 11.5, yb, xr + 23.0, "11.5", ext_from=xr + 21.0)
    s.dim_v(yb, yb + T, xl - 2.0, "1.6", ext_from=xl, text_left=True)
    s.dim_v(plate_y, plate_y + 10.0, xl + 42.0, "10", ext_from=xl + 41.0)
    # balloons
    by = s.Y(plate_y + 10.0) + 50 * s.f
    s.balloon(1, (tpl[1], yb + T + 0.05), (s.X(tpl[1]), by), "Test point on the bottom, the side with no parts")
    s.balloon(2, (tpl[2], plate_y + 6.0), (s.X(tpl[2]), by), "Spring probe in a replaceable receptacle")
    s.balloon(3, (xl + 32.0, plate_y + 8.0), (s.X(xl + 32), by), "One plate of probes, about 10 mm FR4",
              "Production grade; acrylic or MDF for development")
    s.balloon(4, (tpx, yb - 7.0), (s.X(tpx), by), "Probe longer than the part beside it",
              "In a 1 mm gap; easily bent or knocked")
    s.balloon(5, (xr + 30.0, top_y - 2.5), (s.X(xr + 30.0), by), "Cut-out in the top plate to clear tall parts")
    ky = by + 60 * s.f
    y1 = s.key(40, ky, width=440, only=(1, 2, 3))
    y2 = s.key(510, ky, width=440, title="", only=(4, 5))
    y = notes(s, 40, max(y1, y2) + 40 * s.f, (
        "Drawn to scale (probe tips simplified). Dimensions in mm.",
        "A flying-probe tester can reach both sides, but one side is still quicker.",
        "The left half is how a board should be laid out for a fixture; it can be flying-probed too."))
    fit(s, y)
    s.save(out(62, "probe-access"))


def boundary_scan():
    # D64 (PCB-DFT-012): a boundary-scan chain, block diagram, not to scale.
    s = sheet(980, 630, "A boundary-scan (JTAG) chain",
              "Block diagram, not to scale. A six-pin connector J1 carries TCK, TMS, TRST, TDI, TDO and ground. TDI "
              "from the connector goes into the first chip, U1; U1's TDO goes into U2's TDI; U2's TDO into U3's TDI; "
              "and U3's TDO back to the connector, making one chain. TCK, TMS and TRST run to all three chips in "
              "parallel. TMS and TDI have pull-up resistors and TRST a pull-down, as the chip makers advise. A memory "
              "chip next to U1 doesn't support boundary scan, but its connections to U1 can still be tested through "
              "U1's pins.", scale=1, ox=0, oy=0)
    d = s.d
    jx, jy = 80, 130
    rows = {"TCK": 0, "TMS": 1, "TRST": 2, "TDI": 3, "TDO": 4, "GND": 5}
    def ry(n):
        return jy + 25 + rows[n] * 36
    d.append(dw.Rectangle(jx, jy, 60, 222, rx=4, class_="conn"))
    for n in rows:
        d.append(dw.Circle(jx + 42, ry(n), 7, class_="pin"))
        d.append(dw.Text(n, s.fs(12), jx - 8, ry(n) + 4, text_anchor="end", class_="ink"))
    d.append(dw.Text("J1", s.fs(14), jx + 30, jy - 10, text_anchor="middle", class_="ink", font_weight="600"))
    xs, cw, cy, ch = (400, 590, 780), 150, 130, 222
    pin_y = {"TCK": cy + 30, "TMS": cy + 62, "TRST": cy + 94, "TDI": cy + 190}
    for (name, kind), x in zip((("U1", "Processor"), ("U2", "FPGA"), ("U3", "CPLD")), xs):
        d.append(dw.Rectangle(x, cy, cw - 40, ch, rx=6, class_="chip"))
        d.append(dw.Text(name, s.fs(16), x + (cw - 40) / 2, cy + 136, text_anchor="middle", class_="chipin",
                         font_weight="700"))
        d.append(dw.Text(kind, s.fs(11.5), x + (cw - 40) / 2, cy + 156, text_anchor="middle", class_="chipin"))
        for lbl, yy in pin_y.items():
            d.append(dw.Text(lbl, s.fs(11), x + 8, yy + 4, class_="chipin"))
        d.append(dw.Text("TDO", s.fs(11), x + cw - 48, pin_y["TDI"] + 4, text_anchor="end", class_="chipin"))
    x0 = jx + 49
    # Every wire is a list of horizontal and vertical segments, grouped by net, so that crossings between
    # different nets can be drawn as hops (small arches) and joins within a net as dots.
    nets = {}
    def wire(net, cls, *pts):
        segs = nets.setdefault(net, [cls, []])[1]
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            segs.append((xa, ya, xb, yb))
    # chain (red): J1 TDI -> U1, U1 -> U2 -> U3, U3 TDO -> J1 TDO
    wire("TDI", "wire3", (x0, ry("TDI")), (300, ry("TDI")), (300, pin_y["TDI"]), (xs[0], pin_y["TDI"]))
    for k, (x1, x2) in enumerate(zip(xs, xs[1:])):
        wire(f"CHAIN{k}", "wire3", (x1 + cw - 40, pin_y["TDI"]), (x2, pin_y["TDI"]))
    wire("TDO", "wire3", (xs[2] + cw - 40, pin_y["TDI"]), (925, pin_y["TDI"]), (925, 490), (180, 490),
         (180, ry("TDO")), (x0, ry("TDO")))
    # shared signals (blue): from J1 up to a bus above the chips, then a drop to each chip's pin
    for n, bx, top, dx in (("TCK", 200, 16, 16), ("TMS", 215, 32, 32), ("TRST", 230, 48, 48)):
        yb = cy - top
        wire(n, "wire2", (x0, ry(n)), (bx, ry(n)), (bx, yb), (xs[2] - dx, yb))
        for x in xs:
            wire(n, "wire2", (x - dx, yb), (x - dx, pin_y[n]), (x, pin_y[n]))
    # crossings: a vertical segment of one net over a horizontal segment of another gets a hop
    R = 5
    def inside(v, a, b):
        return min(a, b) + 0.5 < v < max(a, b) - 0.5
    for net, (cls, segs) in nets.items():
        for (xa, ya, xb, yb) in segs:
            if ya == yb:
                d.append(dw.Line(xa, ya, xb, yb, class_=cls))
                continue
            hops = sorted({hy for other, (_, osegs) in nets.items() if other != net
                           for (ha, hy, hb, hy2) in osegs if hy == hy2 and inside(xa, ha, hb) and inside(hy, ya, yb)})
            down = yb > ya
            if not down:
                hops = hops[::-1]
            path = dw.Path(class_=cls)
            path.M(xa, ya)
            for hy in hops:
                path.L(xa, hy - R if down else hy + R)
                path.A(R, R, 0, 0, 1 if down else 0, xa, hy + R if down else hy - R)
            path.L(xb, yb)
            d.append(path)
    # joins: where a segment ends part-way along another segment of the same net
    for net, (cls, segs) in nets.items():
        for (xa, ya, xb, yb) in segs:
            for px, py in ((xa, ya), (xb, yb)):
                for (ca, cya, cb, cyb) in segs:
                    on_h = cya == cyb == py and inside(px, ca, cb)
                    on_v = ca == cb == px and inside(py, cya, cyb)
                    if on_h or on_v:
                        d.append(dw.Circle(px, py, 3.6, class_="dot"))
    # pull resistors, marked in words on the J1 side
    for n, lbl in (("TMS", "pull-up"), ("TDI", "pull-up"), ("TRST", "pull-down")):
        d.append(dw.Text(lbl, s.fs(10.5), 147, ry(n) - 5, class_="muted"))
    # memory without boundary scan
    d.append(dw.Rectangle(380, 400, 150, 44, rx=6, class_="membox"))
    d.append(dw.Text("Memory", s.fs(12), 455, 420, text_anchor="middle", class_="memtxt"))
    d.append(dw.Text("(no boundary scan)", s.fs(10.5), 455, 436, text_anchor="middle", class_="memtxt"))
    for k in range(3):
        d.append(dw.Line(420 + k * 25, cy + ch, 420 + k * 25, 400, class_="wire"))
    # legend and notes
    y = 490 + 60 * s.f
    for i, (cls, t) in enumerate((("wire3", "Chain: TDI → each chip → TDO, back to J1"),
                                  ("wire2", "TCK, TMS, TRST: shared by every chip"),
                                  ("wire", "Ordinary connections, tested through U1's pins"))):
        yy = y + i * lh(s, 12.5)
        d.append(dw.Line(80, yy - 4 * s.f, 120, yy - 4 * s.f, class_=cls))
        d.append(dw.Text(t, s.fs(12.5), 132, yy, class_="ink"))
    y = notes(s, 80, y + 2 * lh(s, 12.5) + 40 * s.f, (
        "Block diagram, not to scale.",
        "Resistor values and TCK termination: follow each chip maker's guidance.",
        "Ground sits beside the signals in J1."))
    fit(s, y)
    s.save(out(64, "boundary-scan-chain"))


def spring_pin_pads():
    # D63 (PCB-DFT-013): pads for a 6-pin spring-pin programming cable, after one maker's published footprint.
    s = sheet(980, 800, "Pads for a spring-pin programming cable",
              "Drawn to scale, plan view, after one cable maker's published footprint for a six-pin cable without "
              "retaining legs. Six round copper pads 0.787 mm in diameter sit in two rows of three on a 1.27 mm grid, "
              "numbered 1, 3, 5 along the bottom row and 2, 4, 6 along the top. Three non-plated holes 0.991 mm in diameter "
              "locate the cable: one on the pin-1 end, 2.54 mm from the center on the center line, and two on the far "
              "end, 2.54 mm from the center and 1.016 mm above and below the center line, so the cable fits only one "
              "way. The area between the rows is a keep-out with no tracks or vias, and nothing else comes within "
              "0.5 mm of a pad. Traces leave each pad outwards, up or down. The pads get no paste.",
              scale=62, ox=300, oy=280)
    pads_xy = [(-1.27, 0.635), (-1.27, -0.635), (0, 0.635), (0, -0.635), (1.27, 0.635), (1.27, -0.635)]
    holes = [(-2.54, 0.0), (2.54, -1.016), (2.54, 1.016)]
    R, HR = 0.787 / 2, 0.991 / 2
    win = (-4.2, -3.4, 8.4, 6.8)

    def geom(add, cu, fr4):
        add(s.R(*win, fr4))
        for x, y in pads_xy:
            d = 1 if y > 0 else -1
            add(s.PL([(x, y), (x, y + d * 1.5), (x + (x if x else 0) * 0.6 + 0.0, y + d * (1.5 + abs(x) * 0.6)),
                      (x * 1.6, d * 3.6)], "s-" + cu, 0.2))
        for x, y in pads_xy:
            add(s.C(x, y, R, cu))
    opens = [s.C(x, y, R + 0.05, "bg") for x, y in pads_xy] + [s.C(x, y, HR + 0.1, "bg") for x, y in holes]
    s.board_view(win, geom, openings=opens, holes=[(x, y, HR) for x, y in holes])
    # keep-out between the rows, and the 0.5 mm clearance round each pad
    s.d.append(dw.Rectangle(s.X(-1.27), s.Y(-0.635), s.L(2.54), s.L(1.27), class_="zone"))
    s.d.append(dw.Rectangle(s.X(-1.27), s.Y(-0.635), s.L(2.54), s.L(1.27), class_="zone-s"))
    s.d.append(dw.Circle(s.X(1.27), s.Y(0.635), s.L(R + 0.5), class_="ko-min"))   # 0.5 mm clearance, shown on pad 5
    for n, (x, y) in zip((1, 2, 3, 4, 5, 6), pads_xy):
        s.text(str(n), s.X(x - 0.62), s.Y(y + (0.95 if y > 0 else -0.62)), size=13, cls="silkscreen",
               anchor="middle", weight="600", px=True)
    # dimensions
    s.dim_h(-1.27, 0, -2.35, "1.27", ext_from=-1.1)
    s.dim_h(-2.54, 2.54, -2.95, "5.08", ext_from=-0.6)
    s.dim_v(-0.635, 0.635, -3.6, "1.27", ext_from=-1.8, text_left=True)
    s.dim_v(-1.016, 1.016, 3.6, "2.03", ext_from=3.1)
    s.dim_h(1.27 - R, 1.27 + R, -1.85, "Ø 0.787 pad", ext_from=-0.635, text_side="right")
    s.dim_h(-2.54 - HR, -2.54 + HR, 2.6, "Ø 0.991 hole", ext_from=0.0, text_side="right")
    s.balloon(1, (1.0, 0.0), (s.X(3.35), s.Y(0.0)), "Keep-out: no tracks or vias between the rows")
    s.balloon(2, (1.27 + 0.63, 0.635 + 0.63), (s.X(1.9), 560), "Nothing else within 0.5 mm of a pad",
              "Shown round pad 5")
    s.balloon(3, (0.25, 0.835), (s.X(0.25), 560), "Contact pads: no paste, mask cleared")
    s.balloon(4, (-2.54 - 0.35, -0.35), (s.X(-3.75), s.Y(-1.7)), "Non-plated locating holes",
              "One at one end, two at the other: fits one way only", free=True)
    ky = 560 + 70 * s.f
    y1 = s.key(60, ky, width=430, only=(1, 2))
    y2 = s.key(520, ky, width=430, title="", only=(3, 4))
    y = max(y1, y2) + 50 * s.f
    s.legend(60, y, [("cu-exposed", "Exposed copper"), ("mask-on-cu", "Mask over copper"),
                     ("mask-on-fr4", "Mask over FR4"), ("silkscreen", "Silkscreen"), ("drill", "Hole")])
    notes(s, 340, y, ("Drawn to scale, after one cable maker's footprint.", "Dimensions in mm.",
                      "Use the exact footprint for the cable you'll use."))
    fit(s, y + 4 * 22 * s.f)
    s.save(out(63, "spring-pin-pads"))


if __name__ == "__main__":
    test_points()
    probe_access()
    spring_pin_pads()
    boundary_scan()
    print("written to", OUT)

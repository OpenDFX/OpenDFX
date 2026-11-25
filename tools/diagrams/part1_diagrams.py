"""Part 1 diagrams D9-D11 in the OpenDFX style.
Run: python3 tools/diagrams/part1_diagrams.py         (writes trials/python-N-<name>.svg for review)
     python3 tools/diagrams/part1_diagrams.py --book  (writes book/01-design-package/images/<name>.svg)"""
from pathlib import Path
import sys
import drawsvg as dw

import opendfx_draw
from opendfx_draw import Sheet

BOOK = "--book" in sys.argv
OUT = (Path(__file__).parent / "trials") if not BOOK else (Path(__file__).parents[2] / "book" / "01-design-package" / "images")
OUT.mkdir(exist_ok=True)


def out(n, name):
    """trials/python-<n>-<name>.svg for review, or images/<name>.svg for the book."""
    opendfx_draw.CURRENT_D = n
    return OUT / (f"{name}.svg" if BOOK else f"python-{n}-{name}.svg")


def notes(s, x, y, lines):
    """Notes under a drawing, one per line, spaced for print (DRW1). Returns the y below the last line."""
    for i, t in enumerate(lines):
        s.note(t, x, y + i * 19 * s.f)
    return y + len(lines) * 19 * s.f


def chip_on_pads(s, cx, cy, gap, pad_l=0.6, pad_w=0.7, L=1.0, W=0.5, t=0.25):
    """An 0402 chip (L x W, terminations t) centered on two pads with the given gap."""
    s.rect(cx - gap / 2 - pad_l, cy - pad_w / 2, pad_l, pad_w, "copper")
    s.rect(cx + gap / 2, cy - pad_w / 2, pad_l, pad_w, "copper")
    s.rect(cx - L / 2, cy - W / 2, L, W, "part")
    s.rect(cx - L / 2, cy - W / 2, t, W, "term")
    s.rect(cx + L / 2 - t, cy - W / 2, t, W, "term")


def chip_footprint():
    s = Sheet(980, 680,
              "An 0402 footprint: the gap between the pads",
              "Enlarged and drawn to scale. Left: the recommended 0402 footprint, two pads 0.6 mm long and "
              "0.7 mm wide on a 1.0 mm pitch, leaving a 0.4 mm gap; the part's metal ends sit fully on the pads. "
              "Right: a footprint whose gap is 0.7 mm; the part's ends only just reach the pads, which is how "
              "tombstoning and head-in-pillow start.",
              scale=170, ox=40, oy=80)
    a, b, y = 1.6, 3.9, 0.9
    chip_on_pads(s, a, y, 0.4)
    chip_on_pads(s, b, y, 0.7)
    s.dim_h(a - 0.8, a - 0.2, y - 0.5, "0.6", ext_from=y - 0.35, text_side="left")
    s.dim_h(a - 0.2, a + 0.2, y + 0.5, "0.4 gap", ext_from=y + 0.35)
    s.dim_h(a - 0.5, a + 0.5, y + 0.8, "1.0 pitch", ext_from=y + 0.25)
    s.dim_v(y - 0.35, y + 0.35, a + 0.95, "0.7", ext_from=a + 0.8)
    s.dim_h(b - 0.35, b + 0.35, y + 0.5, "0.7 gap", ext_from=y + 0.35)
    s.text("✓ Recommended", a, y + 1.2, size=14, anchor="middle", weight="600")
    s.text("✗ Gap too wide", b, y + 1.2, size=14, anchor="middle", weight="600")
    s.balloon(1, (a - 0.7, y + 0.2), (s.X(a - 1.15), s.Y(y + 0.35)), "Copper pad")
    s.balloon(2, (a - 0.38, y - 0.15), (s.X(a - 1.15), s.Y(y - 0.15)), "Part's metal end", "Rests fully on the pad")
    s.balloon(3, (b - 0.42, y - 0.1), (s.X(b - 0.42) + 30, s.Y(y - 0.9)), "Metal end barely on the pad", "Tombstoning and head-in-pillow start here")
    s.key(40, 480, width=380)
    notes(s, 520, 500, ["Enlarged and drawn to scale. Dimensions in mm.", "0402 (1005 metric) part: 1.0 × 0.5 mm.",
                        "Footprint from the table in PCB-DFA-029."])
    s.save(out(9, "chip-footprint"))


def mask_dam():
    s = Sheet(980, 700,
              "A solder mask dam between fine-pitch pads",
              "Enlarged and drawn to scale. Top: three pads of a 0.5 mm-pitch part, each 0.25 mm wide with "
              "0.25 mm of space between them. Each pad has its own mask opening, 0.075 mm larger on each side, "
              "which leaves a 0.1 mm strip of solder mask, the dam, between neighboring pads. Bottom: the same "
              "pads in one large opening with no dams, where solder can bridge from pad to pad.",
              scale=225, ox=130, oy=70)
    P, Wc, reg = 0.5, 0.25, 0.075
    for row, gang in ((0.15, False), (1.65, True)):
        s.rect(-0.2, row, 1.9, 0.8, "mask")
        if gang:
            s.rect(0.125 - reg, row + 0.1 - reg, 2 * P + Wc + 2 * reg, 0.6 + 2 * reg, "bare")
        for i in range(3):
            x = 0.125 + i * P
            if not gang:
                s.rect(x - reg, row + 0.1 - reg, Wc + 2 * reg, 0.6 + 2 * reg, "bare")
            s.rect(x, row + 0.1, Wc, 0.6, "copper")
    s.dim_h(0.55, 0.625, 1.03, "0.075", ext_from=0.85)
    s.dim_h(0.45, 0.55, 1.15, "0.1 dam", ext_from=0.85, text_side="left")
    s.dim_h(0.375, 0.625, 1.3, "0.25", ext_from=0.85)
    s.text("✓ A dam between every pad", -0.2, 0.08, size=14, weight="600")
    s.text("✗ One opening, no dams", -0.2, 1.57, size=14, weight="600")
    s.balloon(1, (0.25, 0.45), (s.X(-0.45), s.Y(0.45)), "Copper pad", "0.25 mm wide at 0.5 mm pitch")
    s.balloon(2, (0.5, 0.6), (s.X(1.95), s.Y(0.6)), "Solder mask dam", "0.1 mm; never give it up")
    s.balloon(3, (0.07, 1.85), (s.X(-0.45), s.Y(1.85)), "Mask opening", "0.075 mm larger than the pad, each side")
    s.balloon(4, (0.5, 2.15), (s.X(1.95), s.Y(2.15)), "Bare board between pads", "Solder can bridge across")
    y = s.key(615, 90, width=355)
    notes(s, 615, y + 40 * s.f, ["Enlarged and drawn to scale.", "Dimensions in mm.",
                                  "0.25 copper gap = 0.075 + 0.1 + 0.075", "(PCB-DFA-032)."])
    s.save(out(10, "mask-dam"))


def polarity_marks():
    s = Sheet(980, 1040,
              "Pin-1 and polarity marks done well and badly",
              "Drawn to scale. Top left: an 8-pin IC footprint with a rectangular pin-1 pad, rounded other pads "
              "and a silkscreen dot right beside pin 1, outside the part's outline, so it stays visible after "
              "placement. Top right: the same footprint with all pads alike and the dot inside the outline, hidden "
              "once the part is placed. Bottom left: two 0603 LEDs on the recommended 0603 footprint, one marked "
              "with the letter K beside the cathode pad, the other with a short bar beside the cathode pad, about "
              "as long as the pad is wide. Bottom right: the same footprint with the cathode bar under the part, "
              "hidden once the part is placed. Marks under a part are lost as soon as it is placed.",
              scale=32, ox=66, oy=80)

    def soic(cx, cy, good):
        s.rect(cx - 6, cy - 4.5, 12, 9, "mask")
        for i in range(4):
            y = cy - 1.905 + i * 1.27
            for side, x in ((0, cx - 2.7 - 0.775), (1, cx + 2.7 - 0.775)):
                rx = 0 if (good and side == 0 and i == 0) else (0.25 if good else 0)
                s.rect(x, y - 0.3, 1.55, 0.6, "copper", rx=rx)
        s.rect(cx - 1.95, cy - 2.45, 3.9, 4.9, "outline")
        if good:
            s.circle(cx - 4.05, cy - 1.905, 0.3, "silk")      # right beside pin 1, outside the part
        else:
            s.circle(cx - 1.3, cy - 1.8, 0.3, "silk")         # inside the outline: hidden once placed

    def led(cx, cy, mark):
        # 0603 LED on the recommended 0603 footprint: 0.7 x 1.0 mm pads, 1.4 mm pitch, 0.7 mm gap (PCB-DFA-029).
        # The cathode is the left pad.
        s.rect(cx - 1.05, cy - 0.5, 0.7, 1.0, "copper")
        s.rect(cx + 0.35, cy - 0.5, 0.7, 1.0, "copper")
        s.rect(cx - 0.8, cy - 0.4, 1.6, 0.8, "outline")
        if mark == "K":
            s.text("K", cx - 1.65, cy + 0.33, size=15, cls="silk", anchor="middle", weight="700")
        elif mark == "bar":
            s.rect(cx - 1.45, cy - 0.5, 0.15, 1.0, "silk")      # about as long as the pad is wide
        else:
            s.rect(cx - 0.3, cy - 0.3, 0.12, 0.6, "silk")      # under the part: hidden once placed
    soic(6, 4.5, True)
    soic(20.5, 4.5, False)
    s.rect(0, 11.5, 12, 6, "mask")
    s.rect(14.5, 11.5, 12, 6, "mask")
    led(3.4, 14.5, "K")
    led(8.6, 14.5, "bar")
    led(20.5, 14.5, "under")
    s.text("✓ Visible after placement", 6, -0.6, size=14, anchor="middle", weight="600")
    s.text("✗ Hidden under the part", 20.5, -0.6, size=14, anchor="middle", weight="600")
    s.balloon(1, (3.3, 2.595), (s.X(3.3), s.Y(0.9)), "Rectangular pin-1 pad", "Other pads rounded")
    s.balloon(2, (1.95, 2.595), (s.X(1.95), s.Y(0.9)), "Pin-1 dot right beside pin 1", "Outside the part, still visible once placed")
    s.balloon(3, (20.5 - 1.3, 2.7), (s.X(20.5 - 1.3), s.Y(0.9)), "Dot inside the outline", "Hidden once the part is placed")
    s.balloon(4, (3.4 - 1.65, 14.2), (s.X(0.8), s.Y(12.4)), "K beside the cathode pad")
    s.balloon(5, (8.6 - 1.38, 14.0), (s.X(8.6 - 1.38) - 45, s.Y(12.4)), "Bar beside the cathode pad", "About as long as the pad is wide", free=True)
    s.balloon(6, (20.5 - 0.24, 14.3), (s.X(20.5 - 0.24) + 45, s.Y(12.4)), "Bar under the part", "Hidden once the part is placed", free=True)
    ky = s.Y(17.5) + 60 * s.f
    y1 = s.key(66, ky, width=400, only=(1, 2, 3))
    y2 = s.key(530, ky, width=400, title="", only=(4, 5, 6))
    notes(s, 66, max(y1, y2) + 40 * s.f, ["Drawn to scale. Dashed lines: the part's outline.",
                                          "Use one cathode mark per LED: a K or a bar. Marks under a part are lost once it is placed.",
                                          "PCB-DFA-034 and PCB-DFA-035."])
    s.save(out(11, "polarity-marks"))


# Chris's Rev E chip footprints (PCB-DFA-029), with nominal part sizes.
# size: (metric, pad length, pad width, pitch, mask expansion note, part L, part W, termination length)
CHIPS = {
    "008004": ("0201", 0.20, 0.20, 0.30, "Solder mask expansion 0 (untested footprint)", 0.25, 0.125, 0.065),
    "01005": ("0402", 0.25, 0.23, 0.41, "Solder mask expansion 0.025 mm maximum", 0.4, 0.2, 0.1),
    "0201": ("0603", 0.25, 0.35, 0.55, "Solder mask expansion 0.05 mm maximum", 0.6, 0.3, 0.15),
    "0402": ("1005", 0.60, 0.70, 1.00, "", 1.0, 0.5, 0.25),
    "0603": ("1608", 0.70, 1.00, 1.40, "", 1.6, 0.8, 0.3),
    "0805": ("2012", 0.90, 1.40, 1.80, "", 2.0, 1.25, 0.4),
}


def chip_size_footprint(n, size):
    metric, pl, pw, pitch, mask, L, W, t = CHIPS[size]
    gap = round(pitch - pl, 2)
    scale = 420 / (pitch + pl)
    s = Sheet(980, 620,
              f"The recommended {size} footprint",
              f"Enlarged and drawn to scale. The recommended {size} ({metric} metric) footprint: two pads "
              f"{pl} mm long and {pw} mm wide on a {pitch} mm pitch, leaving a {gap} mm gap. The {L} × {W} mm "
              f"part sits with both metal ends on the pads." + (f" {mask}." if mask else ""),
              scale=scale, ox=490 - 210, oy=0)
    cx, cy = (pitch + pl) / 2, 200 / scale
    chip_on_pads(s, cx, cy, gap, pad_l=pl, pad_w=pw, L=L, W=W, t=t)
    u = 1 / scale  # one px in mm
    left = cx - gap / 2 - pl
    s.dim_h(left, left + pl, cy - pw / 2 - 40 * u, f"{pl}", ext_from=cy - pw / 2, text_side="left")
    s.dim_h(cx - gap / 2, cx + gap / 2, cy + pw / 2 + 40 * u, f"{gap} gap", ext_from=cy + pw / 2)
    s.dim_h(cx - pitch / 2, cx + pitch / 2, cy + pw / 2 + 95 * u, f"{pitch} pitch", ext_from=cy + pw / 2)
    s.dim_v(cy - pw / 2, cy + pw / 2, cx + gap / 2 + pl + 40 * u, f"{pw}", ext_from=cx + gap / 2 + pl)
    s.text(f"{size} ({metric} metric)", 40, 40, size=16, weight="600", px=True)
    s.balloon(1, (left + pl * 0.3, cy + pw * 0.35), (s.X(left) - 60, s.Y(cy + pw * 0.35)), "Copper pad", f"{pl} × {pw} mm")
    s.balloon(2, (cx - L / 2 + t / 2, cy - W * 0.25), (s.X(left) - 60, s.Y(cy - W * 0.25)), "Part's metal end", "Rests on the pad")
    s.key(40, 450, width=380)
    notes(s, 520, 470, ["Enlarged and drawn to scale. Dimensions in mm.", f"{size} part: {L} × {W} mm."] +
          ([mask + "."] if mask else []) + ["Footprint from the table in PCB-DFA-029."])
    s.save(out(n, f"chip-footprint-{size}"))



def pth_sizing():
    # Three steps, drawn to scale: measure the lead, size the hole, size the pad (density level A).
    s = Sheet(980, 680,
              "Sizing a plated through-hole and its pad from the lead",
              "Enlarged and drawn to scale, three steps. One: measure the lead; a round lead across its diameter, "
              "a rectangular lead corner to corner. Two: the hole is the largest lead diameter plus 0.25 mm, so a "
              "0.5 mm lead needs a 0.75 mm hole. Three: the pad is the hole plus twice (0.05 mm minimum annular "
              "ring plus 0.3 mm allowance), so a 0.75 mm hole gets a 1.45 mm pad.",
              scale=110, ox=60, oy=80)
    import math
    s.text("1. Measure the lead", 1.0, -0.2, size=14, anchor="middle", weight="600")
    s.circle(1.0, 1.0, 0.25, "term")
    s.dim_h(0.75, 1.25, 0.5, "0.5", ext_from=1.0)
    w, h = 0.5, 0.3
    cx, cy = 1.0, 2.4
    s.rect(cx - w / 2, cy - h / 2, w, h, "term")
    s.line(cx - w / 2, cy + h / 2, cx + w / 2, cy - h / 2, "dim")
    s.text(f"{math.hypot(w, h):.2f} corner to corner", cx, cy + h / 2 + 0.3, size=12, cls="dimtxt", anchor="middle")
    hx = 3.6
    s.text("2. Hole = lead + 0.25", hx, -0.2, size=14, anchor="middle", weight="600")
    s.circle(hx, 1.4, 0.375, "hole")
    s.circle(hx, 1.4, 0.25, "term")
    s.dim_h(hx - 0.375, hx + 0.375, 0.6, "0.75 hole", ext_from=1.4)
    s.dim_h(hx - 0.25, hx + 0.25, 2.2, "0.5 lead", ext_from=1.4, text_above=False)
    px = 6.3
    s.text("3. Pad = hole + 2 × (0.05 + 0.3)", px, -0.2, size=14, anchor="middle", weight="600")
    s.circle(px, 1.4, 0.725, "copper")
    s.circle(px, 1.4, 0.375, "hole")
    s.dim_h(px - 0.725, px + 0.725, 0.4, "1.45 pad", ext_from=1.4)
    s.dim_h(px - 0.375, px + 0.375, 2.45, "0.75 hole", ext_from=1.4, text_above=False)
    s.balloon(1, (px + 0.55, 1.4), (s.X(px + 1.3), s.Y(1.4)), "Ring of copper, 0.35 each side", "0.05 mm minimum ring + 0.3 mm allowance")
    s.balloon(2, (hx + 0.31, 1.4), (s.X(hx + 1.0), s.Y(1.0)), "Clearance around the lead", "0.125 mm each side", free=True)
    s.key(60, 480, width=420)
    notes(s, 540, 492, ["Enlarged and drawn to scale. Dimensions in mm.",
                        "IPC density level A (least dense, easiest to build).",
                        "Levels B and C use smaller margins (PCB-DFA-037)."])
    s.save(out(23, "pth-sizing"))

def pour_pad_mask():
    # D26 (I2, PCB-DFA-033). The corner of a 0.5 mm-pitch QFN, three times. Every pad has the same mask opening;
    # what shows inside it is bare FR4, or copper where the pad is tied straight into a pour.
    s = Sheet(1060, 990, "Pads on a copper pour: the same mask opening shows FR4 or copper",
              "Drawn to scale, plan view of the corner of a 0.5 mm-pitch QFN, three times, with the exposed pad at the "
              "top left. Every pad has the same mask opening, 0.075 mm larger than the pad. Left, marked right: the two "
              "ground pads at the corner each have a single trace to a via, and bare FR4 shows around them inside their "
              "openings, like every other pad. Middle, marked wrong: a ground pour surrounds the corner and the two "
              "ground pads are tied straight into it, so copper fills their openings and they look larger than the other "
              "pads. Right, marked right: the pour is kept back from the two ground pads and joins them through thin "
              "thermal spokes, so they look like the other pads again.",
              scale=52, ox=30, oy=200)
    PW, PLN, RX, M, CL, TW = 0.25, 0.8, 0.06, 0.075, 0.25, 0.15   # pad, rounding, mask margin, clearance, trace
    ROW = [-0.5, 0.0, 0.5, 1.0, 1.5]          # pad centers along each side; the last one is ground
    TP = 2.55                                  # corner of the exposed pad
    TP_VIAS = [(x, y) for x in (0.0, 1.15, 2.2) for y in (0.0, 1.15, 2.2)]
    GND_VIAS = [(1.5, 4.4), (4.4, 1.5)]
    WIN = 5.8

    def layout(dx):
        pads = []                                  # (rect, ground?, side)
        for x in ROW:
            pads.append(((x - PW / 2 + dx, 3.0, PW, PLN), x == 1.5, "b"))
        for y in ROW:
            pads.append(((3.0 + dx, y - PW / 2, PLN, PW), y == 1.5, "r"))
        sig = [[(x + dx, 3.4), (x + dx, 4.05), (x - 2.0 + dx, 6.05)] for x in ROW[:-1]]
        sig += [[(3.4 + dx, y), (4.05 + dx, y), (6.05 + dx, y - 2.0)] for y in ROW[:-1]]
        return pads, sig

    def panel(i, kind):
        dx = 1.0 + i * 6.7
        pads, sig = layout(dx)

        def geom(add, cu, fr4):
            add(s.R(dx - 2.5, -2.5, WIN + 3, WIN + 3, fr4 if kind == "trace" else cu))   # bare board, or the pour
            if kind != "trace":
                add(s.R(dx - 2.5, -2.5, 5.5, 5.5, fr4))                                # no pour under the part
                for (x, y, w, h), gnd, _ in pads:                                         # clearance round other nets
                    if not gnd or kind == "relief":
                        add(s.R(x - CL, y - CL, w + 2 * CL, h + 2 * CL, fr4, rx=RX + CL))
                for t in sig:
                    add(s.PL(t, "s-" + fr4, TW + 2 * CL))
                if kind == "relief":                                                      # two spokes per ground pad
                    add(s.R(1.4 + dx, 3.75, 0.2, CL + 0.15, cu))
                    add(s.R(1.575 + dx, 3.3, CL + 0.15, 0.2, cu))
                    add(s.R(3.75 + dx, 1.4, CL + 0.15, 0.2, cu))
                    add(s.R(3.3 + dx, 1.575, 0.2, CL + 0.15, cu))
            add(s.R(dx - 2.5, -2.5, TP + 2.5, TP + 2.5, cu, rx=0.1))                    # exposed pad
            for (x, y, w, h), _, _ in pads:
                add(s.R(x, y, w, h, cu, rx=RX))
            for t in sig:
                add(s.PL(t, "s-" + cu, TW))
            if kind == "trace":                                                           # ground pads: trace to a via
                add(s.PL([(1.5 + dx, 3.4), (1.5 + dx, 4.4)], "s-" + cu, TW))
                add(s.PL([(3.4 + dx, 1.5), (4.4 + dx, 1.5)], "s-" + cu, TW))
            for x, y in GND_VIAS:
                add(s.C(x + dx, y, 0.3, cu))

        openings = [s.R(x - M, y - M, w + 2 * M, h + 2 * M, "bg", rx=RX + M) for (x, y, w, h), _, _ in pads]
        openings.append(s.R(dx - 2.5, -2.5, TP + 2.5 + M, TP + 2.5 + M, "bg", rx=0.1 + M))
        holes = [(x + dx, y, 0.15) for x, y in TP_VIAS + GND_VIAS]
        s.board_view((dx - 1.0, -1.0, WIN, WIN), geom, openings, holes)
        return dx

    titles = [("trace", ["✓ Single trace", "to each ground pad"]), ("pool", ["✗ Ground pads tied", "straight into the pour"]),
              ("relief", ["✓ Ground pads", "on thermal reliefs"])]
    dxs = []
    f = s.f
    for i, (kind, title) in enumerate(titles):
        dx = panel(i, kind)
        dxs.append(dx)
        for k, line in enumerate(title):
            s.text(line, s.X(dx + 1.9), s.Y(-1.0) - 14 * f - (len(title) - 1 - k) * 21 * f, size=14,
                   anchor="middle", weight="600", px=True)
    row = s.Y(4.8) + 40 * f
    s.balloon(1, (dxs[0] + 0.5 - PW / 2 - 0.04, 3.45), (s.X(dxs[0] + 0.5) - 20, row), "Mask opening, the same on every pad",
              "Bare FR4 shows around the copper")
    s.balloon(2, (dxs[1] + 1.625 + 0.04, 3.45), (s.X(dxs[1] + 1.625) + 30, row), "Ground pad tied straight into the pour",
              "Copper fills its opening, so it looks like a bigger pad")
    s.balloon(3, (dxs[2] + 1.5, 3.8 + 0.2), (s.X(dxs[2] + 1.5) + 30, row), "Thermal spoke",
              "Only a sliver of copper shows, like a trace")
    ky = row + 70 * f
    s.key(30, ky, width=500)
    s.legend(590, ky + 12 * f, [("cu-exposed", "Exposed copper"), ("fr4-exposed", "Exposed FR4"),
                                ("mask-on-cu", "Mask over copper"), ("mask-on-fr4", "Mask over FR4"), ("drill", "Hole")])
    notes(s, 590, ky + 12 * f + 5 * 22 * f + 14 * f,
          ["Drawn to scale. Dimensions in mm.", "Corner of a 0.5 mm-pitch QFN, 0.25 mm pads.",
           "Mask openings 0.075 mm larger than each pad", "(PCB-DFA-032).",
           "Pour clearance and relief gap 0.25 mm,", "spokes 0.2 mm: example values."])
    s.save(out(26, "pour-pad-mask"))


def overhang_outline():
    # D27 (I3, PCB-DFA-036). A connector footprint at the board edge. Left: silkscreen stops at the edge.
    # Right: silkscreen drawn past the edge as if it could print there; the fab trims it, but sees the overhang.
    s = Sheet(860, 800, "A connector outline in silkscreen, with the overhang past the board edge",
              "Drawn to scale, plan view of a connector footprint at the edge of a board, twice. The board has a ground "
              "pour, four surface-mount pads at the back of the connector with traces running into the board, and two "
              "plated mounting holes. Left, marked wrong: the connector's silkscreen outline stops at the board edge, so "
              "nothing shows that the connector hangs 3 mm past it. Right, marked right: the outline continues 3 mm past "
              "the edge, over the area outside the board, as if silkscreen could print there.",
              scale=26, ox=50, oy=370)
    RX, M, CL, TW = 0.15, 0.075, 0.3, 0.25
    PADS = [(x - 0.3, -7.9, 0.6, 1.4) for x in (-1.5, -0.5, 0.5, 1.5)]
    PEGS = [(-3.4, -3.5), (3.4, -3.5)]

    def panel(i, full):
        dx = 6.5 + i * 15

        def geom(add, cu, fr4):
            add(s.R(dx - 7, -11, 14, 11, cu))                         # ground pour
            add(s.R(dx - 7, -0.5, 14, 0.5, fr4))                      # pour pulled back from the edge
            for x, y, w, h in PADS:
                add(s.R(x + dx - CL, y - CL, w + 2 * CL, h + 2 * CL, fr4, rx=RX + CL))
                add(s.PL([(x + dx + 0.3, y + 0.7), (x + dx + 0.3, -11)], "s-" + fr4, TW + 2 * CL))
            for x, y in PEGS:
                add(s.C(x + dx, y, 0.9 + CL, fr4))
            for x, y, w, h in PADS:
                add(s.R(x + dx, y, w, h, cu, rx=RX))
                add(s.PL([(x + dx + 0.3, y + 0.7), (x + dx + 0.3, -11)], "s-" + cu, TW))
            for x, y in PEGS:
                add(s.C(x + dx, y, 0.9, cu))

        openings = [s.R(x + dx - M, y - M, w + 2 * M, h + 2 * M, "bg", rx=RX + M) for x, y, w, h in PADS]
        openings += [s.C(x + dx, y, 0.9 + M, "bg") for x, y in PEGS]
        s.d.append(s.R(dx - 6.5, 0, 13, 4.5, "offboard"))
        s.board_view((dx - 6.5, -10, 13, 10), geom, openings, [(x + dx, y, 0.55) for x, y in PEGS])
        outline = [(dx - 4.5, 3.0), (dx - 4.5, -6), (dx + 4.5, -6), (dx + 4.5, 3.0), (dx - 4.5, 3.0)] if full else \
                  [(dx - 4.5, 0), (dx - 4.5, -6), (dx + 4.5, -6), (dx + 4.5, 0)]
        s.d.append(s.PL(outline, "s-silkscreen", 0.15))
        s.text("Outside the board", s.X(dx - 6.0), s.Y(4.0), size=11, cls="silk", px=True)
        return dx

    d0 = panel(0, False)
    d1 = panel(1, True)
    s.text("✗ Silkscreen stops at the edge", s.X(d0), s.Y(-10.6), size=14, anchor="middle", weight="600", px=True)
    s.text("✓ Silkscreen drawn past the edge", s.X(d1), s.Y(-10.6), size=14, anchor="middle", weight="600", px=True)
    s.dim_v(0, 3.0, d1 + 7.2, "3 mm", ext_from=d1 + 4.5)
    s.balloon(1, (d0 + 4.5, -0.4), (s.X(d0 + 4.5) + 20, 540), "Silkscreen stops at the board edge",
              "Nothing shows the 3 mm overhang")
    s.balloon(2, (d1 + 1.5, 3.0), (s.X(d1 + 1.5) + 20, 540), "Silkscreen drawn past the edge",
              "The fab trims it, but sees the overhang first")
    s.key(50, 600, width=380)
    s.legend(470, 612, [("cu-exposed", "Exposed copper"), ("fr4-exposed", "Exposed FR4"), ("mask-on-cu", "Mask over copper"),
              ("mask-on-fr4", "Mask over FR4"), ("silkscreen", "Silkscreen"), ("offboard", "Outside the board")])
    notes(s, 50, 760, ["Drawn to scale. Dimensions in mm.",
                       "Example connector: 9 mm wide, 6 mm deep on the board, 3 mm past the edge."])
    s.save(out(27, "overhang-outline"))


def nonplated_hole():
    # D28 (I5, PCB-DFM-007). A 3.2 mm non-plated hole in a ground pour. Left: the pour runs right up to the hole, so
    # copper shows at its edge, like the ring of a plated hole. Right: the pour is kept 0.2 mm back, so the opening
    # shows a ring of bare FR4 and the hole is clearly not plated. CLR is the 0.2 mm minimum (Chris, 2026-11-05, Q60b).
    s = Sheet(880, 880, "A non-plated hole in a copper pour: pour up to the hole vs pour kept back",
              "Drawn to scale, plan view of a 3.2 mm non-plated hole in a ground pour, twice, with a trace and a via "
              "nearby. The mask opening is 0.1 mm larger than the hole in both. Left, marked wrong: the pour runs right "
              "up to the hole, so a ring of copper shows at its edge, like the ring of a plated hole. Right, marked "
              "right: the pour is kept 0.2 mm back from the hole, so the opening shows a ring of bare FR4 and mask covers the rest of the gap. Enlarged "
              "views below show the edge of the hole in each.",
              scale=60, ox=50, oy=290)
    H, M, CLR, CL, TW = 1.6, 0.1, 0.2, 0.25, 0.25     # hole radius, mask margin, pour clearance to the hole, trace
    dxs = []
    for i in range(2):
        dx = 3.0 + i * 7.0
        dxs.append(dx)

        def geom(add, cu, fr4, i=i, dx=dx):
            add(s.R(dx - 4, -4, 8, 8, cu))                                    # ground pour
            for t in ([(dx + 2.4, -4), (dx + 2.4, 4)], [(dx - 4, -1.2), (dx - 1.4, -3.8), (dx - 1.4, -4)]):
                add(s.PL(t, "s-" + fr4, TW + 2 * CL))
                add(s.PL(t, "s-" + cu, TW))
            if i == 1:
                add(s.C(dx, 0, H + CLR, fr4))                                  # pour kept back from the hole
            add(s.C(dx - 2.2, 2.0, 0.3, cu))                                   # ground via
        s.board_view((dx - 3, -3, 6, 6), geom, [s.C(dx, 0, H + M, "bg")], [(dx, 0, H), (dx - 2.2, 2.0, 0.15)])
    for dx, title in zip(dxs, ["✗ Pour runs up to the hole", "✓ Pour kept 0.2 mm back"]):
        s.text(title, s.X(dx), s.Y(-3.5), size=14, anchor="middle", weight="600", px=True)
    K = 400                                   # px per mm in the enlarged views
    for dx, band, label in ((dxs[0], "cu-exposed", ["0.1 mm of copper", "at the hole's edge"]),
                            (dxs[1], "fr4-exposed", ["0.2 mm without copper,", "0.1 mm of it bare"])):
        x0, y0 = s.X(dx) - 110, 510
        s.d.append(dw.Rectangle(x0, y0, 220, 50, class_="mask-on-cu"))
        s.d.append(dw.Rectangle(x0, y0, 80, 50, class_="drill"))
        if band == "fr4-exposed":            # no copper for 0.2 mm; the outer 0.1 mm is under the mask
            s.d.append(dw.Rectangle(x0 + 80, y0, CLR * K, 50, class_="mask-on-fr4"))
        s.d.append(dw.Rectangle(x0 + 80, y0, M * K, 50, class_=band))
        s.d.append(dw.Rectangle(x0, y0, 220, 50, class_="thin"))
        s.text("Edge of the hole, enlarged", x0, y0 - 8, size=11, cls="muted", px=True)
        for k, line in enumerate(label):
            s.text(line, x0 + 80, y0 + 74 + k * 21 * s.f, size=12, cls="ink", px=True)
    s.balloon(1, (dxs[0] - 1.17, 1.17), (s.X(dxs[0] - 1.17), s.Y(2.45)), "Copper at the edge of the hole",
              "Looks like the ring of a plated hole")
    s.balloon(2, (dxs[1] - 1.2, 1.2), (s.X(dxs[1] - 1.2), s.Y(2.45)), "Pour kept 0.2 mm back",
              "Bare FR4 shows: clearly not plated")
    s.key(50, 680, width=380)
    s.legend(500, 692, [("cu-exposed", "Exposed copper"), ("fr4-exposed", "Exposed FR4"),
                        ("mask-on-cu", "Mask over copper"), ("mask-on-fr4", "Mask over FR4"), ("drill", "Hole")])
    notes(s, 50, 830, ["Drawn to scale. Dimensions in mm.",
                       "Non-plated hole 3.2 mm in diameter. Mask opening 0.1 mm larger than the hole."])
    s.save(out(28, "nonplated-hole"))


def zero_rotation():
    """D44: IPC-7351B zero rotations for six common packages (PCB-DFA-065)."""
    s = Sheet(980, 860,
              "Zero rotation: how to draw common footprints at 0°",
              "Drawn to scale, six footprints at their IPC-7351B zero rotation, each on solder mask. Parts "
              "that could be placed the wrong way round have a pin-1 or cathode mark; the chip and the SOT-23 don't need one. A 0603 chip resistor or capacitor lies horizontal, with no polarity mark, since it isn't polarized. A SOD-123 "
              "diode lies horizontal with the cathode on the left. A SOT-23 has pins 1 and 2 on the left, pin 1 "
              "at the top, and pin 3 on the right, with no mark, since its pad pattern only fits one way. An 8-pin SOIC has pins 1 to 4 down the left side with pin 1 "
              "at the upper left. A 16-pin QFN has pin 1 at the top of the left side. A BGA has ball A1 at the "
              "upper left. The cross at the center of each part is the point the placement (XY) file gives.",
              scale=32, ox=0, oy=0)
    cells = [(160, 150), (490, 150), (820, 150), (160, 480), (490, 480), (820, 480)]

    def cell(i, title, sub):
        cx, cy = cells[i]
        s.d.append(__import__("drawsvg").Rectangle(cx - 150, cy - 105, 300, 200, class_="mask"))
        s.text(title, cx, cy - 115, size=13, anchor="middle", weight="600", px=True)
        for k, line in enumerate(sub):
            s.text(line, cx, cy + 124 + k * 20 * s.f, size=12, cls="muted", anchor="middle", px=True)
        return cx / s.scale, cy / s.scale  # center in mm

    def cross(x, y):
        for a, b, c, d in ((x - 0.35, y, x + 0.35, y), (x, y - 0.35, x, y + 0.35)):
            s.d.append(dw.Line(s.X(a), s.Y(b), s.X(c), s.Y(d), class_="ink-s", stroke_width=s.sw(1.0)))

    def pad(x, y, w, h, rx=0):  # centered pad, mm
        s.rect(x - w / 2, y - h / 2, w, h, "copper", rx=rx)

    # 0603 chip: recommended footprint (PCB-DFA-029), pin 1 left
    x, y = cell(0, "0603 chip resistor or capacitor", ["Horizontal, with no polarity", "mark needed"])
    pad(x - 0.7, y, 0.7, 1.0); pad(x + 0.7, y, 0.7, 1.0)
    s.rect(x - 0.8, y - 0.4, 1.6, 0.8, "outline")
    cross(x, y)
    # SOD-123 diode, cathode left
    x, y = cell(1, "SOD-123 diode", ["Horizontal, with the cathode", "(pin 1) on the left"])
    pad(x - 1.6, y, 0.9, 1.2); pad(x + 1.6, y, 0.9, 1.2)
    s.rect(x - 1.35, y - 0.8, 2.7, 1.6, "outline")
    s.text("K", x - 2.45, y + 0.2, size=15, cls="silk", anchor="middle", weight="700")
    cross(x, y)
    # SOT-23: pins 1, 2 left (1 at top), pin 3 right
    x, y = cell(2, "SOT-23", ["Pins 1 and 2 on the left,", "with no mark needed"])
    pad(x - 1.1, y - 0.95, 1.0, 0.6); pad(x - 1.1, y + 0.95, 1.0, 0.6); pad(x + 1.1, y, 1.0, 0.6)
    s.rect(x - 0.65, y - 1.45, 1.3, 2.9, "outline")
    cross(x, y)
    # SOIC-8: pins 1-4 down the left
    x, y = cell(3, "SOIC-8", ["Pin 1 at the upper left,", "pins 1 to 4 down the left side"])
    for i in range(4):
        yy = y - 1.905 + i * 1.27
        pad(x - 2.7, yy, 1.55, 0.6, rx=0 if i == 0 else 0.25)
        pad(x + 2.7, yy, 1.55, 0.6, rx=0.25)
    s.rect(x - 1.95, y - 2.45, 3.9, 4.9, "outline")
    s.circle(x - 3.85, y - 2.6, 0.15, "silk")
    cross(x, y)
    # QFN-16, 3 x 3 mm, 0.5 mm pitch: pin 1 at the top of the left side
    x, y = cell(4, "QFN-16 (3 × 3 mm)", ["Pin 1 at the upper left,", "at the top of the left side"])
    for i in range(4):
        o = -0.75 + i * 0.5
        pad(x - 1.45, y + o, 0.8, 0.25); pad(x + 1.45, y + o, 0.8, 0.25)
        pad(x + o, y - 1.45, 0.25, 0.8); pad(x + o, y + 1.45, 0.25, 0.8)
    pad(x, y, 1.7, 1.7)
    s.rect(x - 1.5, y - 1.5, 3.0, 3.0, "outline")
    s.circle(x - 2.1, y - 1.2, 0.15, "silk")
    cross(x, y)
    # BGA 5 x 5 at 0.8 mm pitch: A1 upper left
    x, y = cell(5, "BGA (5 × 5 balls, 0.8 mm pitch)", ["Ball A1 at the upper left"])
    for r in range(5):
        for c in range(5):
            s.circle(x - 1.6 + c * 0.8, y - 1.6 + r * 0.8, 0.2, "copper")
    s.rect(x - 2.25, y - 2.25, 4.5, 4.5, "outline")
    s.circle(x - 2.55, y - 2.55, 0.15, "silk")
    s.text("A1", x - 2.75, y - 1.45, size=11, cls="silk", anchor="end", weight="700")
    cross(x, y)
    notes(s, 20, 690, ["Drawn to scale. Dashed line: the part's outline.",
                       "White dot or K: pin-1 or cathode mark, only where the pads would fit either way.",
                       "Cross: the part's center, the point the XY file gives.",
                       "Rotation in the XY file is measured from this drawing.",
                       "Source: IPC-7351B, section 16 and Figure 16-1.",
                       "IPC-7352 leaves the convention to each library standard."])
    s.save(out(44, "zero-rotation"))


if __name__ == "__main__":
    zero_rotation()
    chip_footprint()
    mask_dam()
    polarity_marks()
    pth_sizing()
    pour_pad_mask()
    overhang_outline()
    nonplated_hole()
    for n, size in zip((12, 13, 14, 22, 15, 16), CHIPS):
        chip_size_footprint(n, size)
    print("written to", OUT)

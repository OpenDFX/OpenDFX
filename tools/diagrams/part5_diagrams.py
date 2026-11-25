"""Part 5 diagrams D6-D8 in the OpenDFX style.
Run: python3 tools/diagrams/part5_diagrams.py         (writes trials/python-N-<name>.svg for review)
     python3 tools/diagrams/part5_diagrams.py --book  (writes book/05-assembly/images/<name>.svg)"""
from pathlib import Path
import sys

import drawsvg as dw
import opendfx_draw
from opendfx_draw import Sheet

BOOK = "--book" in sys.argv
OUT = (Path(__file__).parent / "trials") if not BOOK else (Path(__file__).parents[2] / "book" / "05-assembly" / "images")
OUT.mkdir(exist_ok=True)


def out(n, name):
    """trials/python-<n>-<name>.svg for review, or images/<name>.svg for the book."""
    opendfx_draw.CURRENT_D = n
    return OUT / (f"{name}.svg" if BOOK else f"python-{n}-{name}.svg")


def key_below(s, y, notes=(), x=40, gap=40, cols=2):
    """DRW1 (Q177 option A): the key in columns under the drawing, then the notes, one per line; the sheet's height is
    set to fit. y is the top of the key in px. Returns the sheet's new height."""
    f = s.f
    ns = sorted(n for n, _, _ in s.balloons)
    per = -(-len(ns) // cols)
    width = (s.width - 2 * x - gap * (cols - 1)) / cols
    end = y
    for c in range(cols):
        part = ns[c * per:(c + 1) * per]
        if part:
            end = max(end, s.key(x + c * (width + gap), y, width=width, title="Key" if c == 0 else "", only=part))
    end += 14 * f
    for line in notes:
        end += 20 * f
        s.note(line, x, end)
    s.height = end + 22 * f
    return s.height


def notes_at(s, y, notes, x=40):
    """Notes one per line from y (px); sets the sheet's height to fit and returns it."""
    for line in notes:
        y += 20 * s.f
        s.note(line, x, y)
    s.height = y + 22 * s.f
    return s.height


def note_lines(s, x, y, lines):
    """Notes one per line from y (px), spaced for their print size. Returns the y of the last line."""
    for i, line in enumerate(lines):
        s.note(line, x, y + i * 21 * s.f)
    return y + (len(lines) - 1) * 21 * s.f


def poly(s, pts_mm, cls):
    """Closed polygon from mm points."""
    flat = [v for x, y in pts_mm for v in (s.X(x), s.Y(y))]
    s.d.append(dw.Lines(*flat, close=True, class_=cls))


def stencil_area_ratio():
    # Two cross-sections through the same 0.25 mm square opening: 5 mil foil (top) and 3 mil foil (bottom).
    s = Sheet(980, 600,
              "Stencil area ratio: the same small opening in a thick and a thin stencil",
              "Enlarged and drawn to scale. Two cross-sections through a stencil opening 0.25 mm square, "
              "over a copper pad. In a 0.127 mm (5 mil) thick stencil the area ratio is 0.49, below the "
              "0.66 minimum, so paste sticks to the walls instead of releasing onto the pad. In a 0.076 mm "
              "(3 mil) thick stencil the area ratio is 0.82, above the minimum, and the paste releases. "
              "Area ratio is the opening's area divided by the area of its walls.",
              scale=260, ox=230, oy=10)
    W = 0.25

    def section(y0, t_mm, t_label, ar, ok):
        # board surface at y0 + t_mm + copper; stencil sits on the pad
        cu = 0.035
        base = y0 + t_mm + cu
        s.rect(-0.45, base, W + 0.9, 0.12, "mask-lt")
        s.rect(0, base - cu, W, cu, "copper")
        s.rect(-0.45, y0, 0.45, t_mm, "foil")
        s.rect(W, y0, 0.45, t_mm, "foil")
        s.rect(0, y0, W, t_mm, "paste")
        s.line(0, y0, 0, y0 + t_mm, "wall")
        s.line(W, y0, W, y0 + t_mm, "wall")
        s.dim_h(0, W, y0 - 0.07, "0.25", ext_from=y0)
        s.dim_v(y0, y0 + t_mm, W + 0.55, t_label, ext_from=W + 0.45)
        tx, f = 610, s.f
        s.text(f"Area ratio = 0.25 ÷ (4 × {t_mm:.3f}) = {ar}", tx, s.Y(y0) + 14 * f, size=13, px=True)
        verdict = ["✓ Above 0.66:", "the paste releases"] if ok else ["✗ Below 0.66:", "paste sticks in the opening"]
        for i, line in enumerate(verdict):
            s.text(line, tx, s.Y(y0) + (38 + 20 * i) * f, size=13, cls="ink", px=True, weight="600")
    section(0.40, 0.127, "0.127 (5 mil)", "0.49", False)
    section(1.17, 0.076, "0.076 (3 mil)", "0.82", True)
    f = s.f
    s.balloon(1, (-0.30, 0.43), (s.X(-0.30), s.Y(0.40) - 52 * f), "Stencil foil")
    s.balloon(2, (0.21, 0.46), (s.X(0.21), s.Y(0.40) - 52 * f), "Opening filled with paste")
    s.balloon(3, (0.0, 0.49), (s.X(-0.45) - 26 * f, s.Y(0.49)), "Walls", "Paste grips the walls")
    s.balloon(4, (0.125, 0.545), (s.X(0.125), s.Y(0.682) + 34 * f), "Copper pad", "Paste must grip the pad more")
    key_below(s, s.Y(1.42) + 50 * f, [
        "Drawn to scale. Dimensions in mm.",
        "Area ratio = opening area ÷ wall area; for a square opening, width ÷ (4 × thickness).",
        "Minimum area ratio 0.66 (IPC-7525).",
        "A thinner stencil helps the small part but gives every large part less paste (PCB-DFA-020)."])
    s.save(out(6, "stencil-area-ratio"))


def double_sided_plan():
    # Side view of a double-sided board on its second pass through the oven.
    s = Sheet(980, 640,
              "Which parts go on which side of a double-sided board",
              "Drawn to scale, side view. A 1.6 mm board on its second pass through the reflow oven. "
              "The side built second faces up and carries the heavy parts: a large inductor and a USB "
              "connector whose pegs go through the board. The side built first hangs underneath and "
              "carries only small, light parts: a QFN chip and small resistors and capacitors, held on by "
              "the surface tension of the melted solder.",
              scale=19, ox=60, oy=205)
    T = 1.6
    s.rect(0, 0, 44, T, "mask")
    # second side (up): inductor 10 x 10 x 5, connector 9 long x 3.2 high with pegs through the board
    s.rect(4, -5.0, 10, 5.0, "part")
    s.rect(20, -3.2, 9, 3.2, "stub")
    for px_ in (20.6, 27.6):
        s.rect(px_, -0.2, 0.8, T + 1.2, "term")
    s.rect(32, -1.8, 6, 1.8, "part")
    # first side (hanging): QFN 4 x 0.9, 0402s 1.0 x 0.35, 0603s
    s.rect(6, T, 4, 0.9, "part")
    for x in (13, 15, 17):
        s.rect(x, T, 1.0, 0.35, "part")
    for x in (34, 36.5, 39):
        s.rect(x, T, 1.6, 0.45, "part")
    s.text("Second side, built last (facing up in the oven)", 0, -8.5, size=13, cls="ink", weight="600")
    s.text("First side, built first (hanging upside down)", 0, T + 8.0, size=13, cls="ink", weight="600")
    s.balloon(1, (9, -2.5), (s.X(16), s.Y(-6.5)), "Heavy parts on the second side", "Inductors, buzzers, large capacitors")
    s.balloon(2, (24.5, -1.6), (s.X(31), s.Y(-5.5)), "Parts with pegs through the board", "All on the second side, together")
    s.balloon(3, (21, T + 1.0), (s.X(25), s.Y(T + 4.6)), "Pegs poke out the first side", "So the first side is printed before they're fitted")
    s.balloon(4, (15.5, T + 0.2), (s.X(21), s.Y(T + 4.6)), "Small, light parts hang underneath", "Held on by surface tension")
    s.balloon(5, (35, -0.9), (s.X(41), s.Y(-4)), "Bulky parts", "Here, a large capacitor")
    key_below(s, s.Y(T + 8.0) + 60 * s.f, [
        "Drawn to scale. Board 1.6 mm thick.",
        "Rule of thumb for a part on the first side: weight ÷ total pad area ≤ about 30 g/in² (0.047 g/mm²),",
        "or it must be glued (PCB-DFA-024)."])
    s.save(out(7, "double-sided-plan"))


def part_spacing():
    # Left: top view, 1 mm spacing. Right: side view, a tall capacitor shadowing a neighbor from an angled camera.
    s = Sheet(980, 560,
              "Space between parts, and the shadow of a tall part",
              "Drawn to scale. Left, top view: small capacitors placed 1 mm from the edge of a BGA and 1 mm "
              "from each other. Right, side view: a 10 mm tall aluminum capacitor. Light from an inspection "
              "camera's angled projector is blocked by the tall part, so a small resistor right beside it sits "
              "in its shadow and can't be measured; a resistor further away is in clear view.",
              scale=16, ox=80, oy=150)
    # top view: BGA 10 x 10 with 0402s 1 mm away
    s.rect(0, 0, 10, 10, "part", rx=0.3)
    for i in range(10):
        for j in range(10):
            s.circle(0.5 + i, 0.5 + j, 0.25, "term")
    for k in range(3):
        y = 1 + k * 1.5
        s.rect(11, y, 1.0, 0.5, "part")
        s.rect(11, y, 0.2, 0.5, "term")
        s.rect(11.8, y, 0.2, 0.5, "term")
    s.dim_h(10, 11, 11.5, "1.0", ext_from=10, text_side="right")
    s.dim_v(1.5, 2.5, 13.2, "1.0", ext_from=12)
    s.text("Top view", 0, -5.0, size=13, cls="ink", weight="600")
    # side view, origin shifted right
    ox = 26
    base = 12
    s.rect(ox, base, 26, 1.6, "mask")
    s.rect(ox + 4, base - 10, 8, 10, "stub", rx=0.6)       # aluminum capacitor 8 mm dia, 10 mm tall
    s.rect(ox + 12.5, base - 0.35, 1.0, 0.35, "part")      # 0402 in the shadow
    s.rect(ox + 22, base - 0.35, 1.0, 0.35, "part")        # 0402 in clear view
    # light from upper left at 45 degrees, grazing the top corner of the capacitor
    poly(s, [(ox + 12, base - 10), (ox + 22, base), (ox + 12, base)], "shadow")
    s.line(ox + 6, base - 16, ox + 22, base, "ray")
    s.text("Side view", ox, -5.0, size=13, cls="ink", weight="600")
    s.text("✗", ox + 13, base + 3.4, size=20, cls="ink", anchor="middle", weight="700")
    s.text("✓", ox + 22.5, base + 3.4, size=20, cls="ink", anchor="middle", weight="700")
    f = s.f
    s.balloon(1, (0.5, 5.5), (s.X(0) - 28 * f, s.Y(5.5)), "BGA")
    s.balloon(2, (11.5, 4.25), (s.X(11.5) + 30, s.Y(4.25) + 70), "Small capacitors", "About 1 mm from the BGA and each other")
    s.balloon(3, (ox + 8, base - 6), (s.X(ox + 8) - 30, s.Y(base - 10) - 40), "Tall aluminum capacitor")
    s.balloon(4, (ox + 7, base - 15), (s.X(ox + 7) + 70, s.Y(base - 15)), "Camera's angled light")
    s.balloon(5, (ox + 17.5, base - 1.0), (s.X(ox + 17.5), s.Y(base + 1.6) + 40 * f), "Shadow",
              "A part here can't be measured")
    key_below(s, s.Y(base + 1.6) + 110 * f, [
        "Drawn to scale. Dimensions in mm.",
        "Everyday spacing: about 1 mm edge to edge (PCB-DFA-023).",
        "The shadow's length depends on the camera's angle."])
    s.save(out(8, "part-spacing"))



def _fillet(s, cx, ys, d, pad_half, pin_half, h, cls="solder"):
    """A solder fillet round a lead, as a cross-section: concave from the pad edge (cx +/- pad_half, ys) up the lead
    to height h. d = -1 for the top side (rising), +1 for the bottom side (hanging). Draw the lead after this."""
    def side(sx):
        ax, ay = cx + sx * pad_half, ys
        bx, by = cx + sx * pin_half, ys + d * h
        mx, my = (ax + bx) / 2, (ay + by) / 2
        kx, ky = mx + 0.6 * (bx - mx), my + 0.6 * (ay - my)     # control point pulled toward the corner
        return [((1 - t) ** 2 * ax + 2 * (1 - t) * t * kx + t * t * bx,
                 (1 - t) ** 2 * ay + 2 * (1 - t) * t * ky + t * t * by) for t in [k / 10 for k in range(11)]]
    left, right = side(-1), side(1)
    poly(s, left + list(reversed(right)), cls)


def selective_keepout():
    # D17 (PCB-DFA-043), redrawn 2026-11-05 in the board color key: solder side of the board, a row of three
    # through-hole pads with the keep-out around them, outlined rather than shaded.
    s = Sheet(980, 600,
              "Keep-out around through-hole pins for selective soldering",
              "Drawn to scale, solder side of the board. A row of three through-hole pads on a 2.54 mm pitch, with "
              "traces under the mask. A white dashed line marks the recommended keep-out, 3 mm beyond the outer edge of "
              "the pads on three sides and 5 mm on the side where the board leaves the solder wave; a red dashed line "
              "inside it marks the 2 mm absolute minimum. A small surface-mount part sits just outside the keep-out, "
              "pointing at the pins rather than lying side-on to them.",
              scale=30, ox=230, oy=170)
    pad, pitch = 1.6, 2.54
    x0, y0 = 5.0, 3.0
    row_w = 2 * pitch + pad
    g = s.clipped([s.R(x0 - 8, y0 - 6, row_w + 18, pad + 15, "bg")])
    g.append(s.R(x0 - 8, y0 - 6, row_w + 18, pad + 15, "mask-on-fr4"))
    for i in range(3):
        cx = x0 + pad / 2 + i * pitch
        g.append(s.PL([(cx, y0 + pad / 2), (cx, y0 - 2.2), (cx - 2.5, y0 - 4.7), (cx - 2.5, y0 - 7)], "s-mask-on-cu", 0.3))
    cx1 = x0 + pad / 2 + pitch
    g.append(s.PL([(cx1, y0 + pad + 5.35), (cx1, y0 + pad + 7.0), (cx1 + 3, y0 + pad + 10)], "s-mask-on-cu", 0.3))
    for i in range(3):
        cx = x0 + pad / 2 + i * pitch
        g.append(s.C(cx, y0 + pad / 2, pad / 2 + 0.075, "fr4-exposed"))
        g.append(s.C(cx, y0 + pad / 2, pad / 2, "cu-exposed"))
        g.append(s.C(cx, y0 + pad / 2, 0.45, "drill"))
    for y in (y0 + pad + 3.6, y0 + pad + 5.0):
        g.append(s.R(cx1 - 0.575, y - 0.075, 1.15, 0.85, "fr4-exposed", rx=0.1))
        g.append(s.R(cx1 - 0.5, y, 1.0, 0.7, "cu-exposed", rx=0.08))
    s.d.append(g)
    s.d.append(s.PL([(x0 - 0.5, y0 - 0.5), (x0 + row_w + 0.5, y0 - 0.5), (x0 + row_w + 0.5, y0 + pad + 0.5),
                     (x0 - 0.5, y0 + pad + 0.5), (x0 - 0.5, y0 - 0.5)], "s-silkscreen", 0.15))
    s.text("J1", s.X(x0 + row_w + 0.9), s.Y(y0 + 0.4), size=11, cls="silk", px=True)
    s.text("R1", s.X(cx1 + 1.0), s.Y(y0 + pad + 5.2), size=11, cls="silk", px=True)
    s.rect(x0 - 3, y0 - 3, row_w + 3 + 5, pad + 6, "ko-rec")
    s.rect(x0 - 2, y0 - 2, row_w + 4, pad + 4, "ko-min")
    s.dim_v(y0 + pad, y0 + pad + 3, x0 - 4.2, "3", ext_from=x0)
    s.dim_v(y0 + pad, y0 + pad + 2, x0 - 6.0, "2 min", ext_from=x0, text_left=True)
    s.dim_h(x0 + row_w, x0 + row_w + 5, y0 - 4.2, "5", ext_from=y0)
    s.dim_h(x0 - 3, x0, y0 - 4.2, "3", ext_from=y0, text_side="left")
    s.balloon(1, (x0 + pad / 2 + 0.6, y0 + pad / 2 + 0.3), (s.X(x0 + pad / 2), s.Y(y0 + pad + 9.3)), "Through-hole pad")
    s.balloon(2, (x0 + row_w + 5, y0 + 2.5), (s.X(x0 + row_w + 8.5), s.Y(y0 + 2.5)), "Keep-out, recommended",
              "3 mm; 5 mm on the side leaving the wave")
    s.balloon(3, (x0 - 2, y0 - 1.0), (s.X(x0 - 9.0), s.Y(y0 - 1.0)), "Absolute minimum", "2 mm")
    s.balloon(4, (cx1 + 0.5, y0 + pad + 4.6), (s.X(cx1 + 6), s.Y(y0 + pad + 6)), "Surface-mount part outside",
              "Pointing at the pins, not side-on")
    f = s.f
    y = key_below(s, s.Y(y0 + pad + 9.3) + 60 * f) - 22 * f + 34 * f
    s.legend(40, y, [("cu-exposed", "Exposed copper"), ("mask-on-cu", "Mask over copper")])
    s.legend(330, y, [("mask-on-fr4", "Mask over FR4"), ("drill", "Hole")])
    s.d.append(dw.Rectangle(616, y - 15 * f, 26 * f, 44 * f, class_="mask-on-fr4"))
    s.d.append(dw.Line(620, y - 4 * f, 638, y - 4 * f, class_="ko-rec"))
    s.text("Keep-out, recommended", 620 + 30 * f, y + 1 * f, size=12, px=True)
    s.d.append(dw.Line(620, y + 18 * f, 638, y + 18 * f, class_="ko-min"))
    s.text("Absolute minimum", 620 + 30 * f, y + 23 * f, size=12, px=True)
    notes_at(s, y + 40 * f, [
        "Drawn to scale, solder side. Dimensions in mm from the outer edge of the through-hole pads.",
        "PCB-DFA-043. Ask your assembler which side the board leaves the wave."])
    s.save(out(17, "selective-keepout"))


def pin_in_paste():
    # D18 (PCB-DFA-041), redrawn 2026-11-05: the pin has an outline so it stands apart from the paste, it is drawn
    # over the solder, and the after-reflow joint has fillets on both sides.
    s = Sheet(980, 580,
              "Pin-in-paste: paste printed beyond the hole, drawn in when it melts",
              "Drawn to scale, cross-sections through a 1.6 mm board. Left, after printing: solder paste fills the "
              "plated hole and is printed well beyond the pad onto the solder mask around it, and the pin has been "
              "pushed through it. Right, after reflow: the paste has melted and been drawn into the hole, filling it "
              "round the pin with a fillet on each side, leaving only flux residue on the mask where the paste was.",
              scale=33, ox=46, oy=160)
    T, hole, pad, pin = 1.6, 1.0, 1.8, 0.6

    def board(cx):
        s.rect(cx - 6, 0, 12, T, "mask-on-fr4")
        s.rect(cx - pad / 2, -0.05, pad, 0.05, "cu-exposed")
        s.rect(cx - pad / 2, T, pad, 0.05, "cu-exposed")
        s.rect(cx - hole / 2, 0, hole, T, "bg")
        s.rect(cx - hole / 2, 0, 0.05, T, "cu-exposed")
        s.rect(cx + hole / 2 - 0.05, 0, 0.05, T, "cu-exposed")
    board(6)
    s.rect(6 - hole / 2 + 0.05, 0, hole - 0.1, T, "paste")
    s.rect(6 - 4.5, -0.17, 9, 0.12, "paste")
    s.rect(6 - pin / 2, -2.0, pin, T + 2.8, "foil")
    board(21)
    s.rect(21 - 4.5, -0.08, 9, 0.03, "flux")
    s.rect(21 - hole / 2 + 0.05, 0, hole - 0.1, T, "solder")
    _fillet(s, 21, -0.05, -1, pad / 2, pin / 2, 0.75)
    _fillet(s, 21, T + 0.05, 1, pad / 2, pin / 2, 0.55)
    s.rect(21 - pin / 2, -2.0, pin, T + 2.8, "foil")
    s.text("After printing", 6, -3.0, size=14, anchor="middle", weight="600")
    s.text("After reflow", 21, -3.0, size=14, anchor="middle", weight="600")
    s.dim_h(6 - 4.5, 6 + 4.5, 3.2, "paste printed onto the mask", ext_from=T)
    s.balloon(1, (6 + 3, -0.11), (s.X(9.5), s.Y(-2.2)), "Paste printed beyond the pad", "Several mm onto the solder mask")
    s.balloon(2, (6 - 0.38, 0.8), (s.X(0.6), s.Y(-1.6)), "Paste in the hole", "Only about half of it is metal")
    s.balloon(3, (21 + 0.6, -0.2), (s.X(24.8), s.Y(-1.8)), "Fillet on each side", "The extra paste was drawn in")
    s.balloon(4, (6 - 0.3, -1.4), (s.X(3.0), s.Y(-1.4)), "Through-hole pin", "Pushed through the paste after printing")
    s.balloon(5, (21 - 3.5, -0.07), (s.X(16.5), s.Y(3.4)), "Flux residue", "Where the extra paste was")
    f = s.f
    y = key_below(s, s.Y(3.4) + 60 * f) + 12 * f
    s.legend(40, y, [("paste", "Solder paste"), ("solder", "Solder")])
    s.legend(330, y, [("foil", "Pin"), ("cu-exposed", "Copper")])
    s.legend(620, y, [("mask-on-fr4", "Board")])
    notes_at(s, y + 40 * f, [
        "Drawn to scale except copper thickness. Board 1.6 mm, hole 1.0 mm.",
        "Leave room around the part for the extra paste (PCB-DFA-041)."])
    s.save(out(18, "pin-in-paste"))


def thermal_relief():
    # D19 (PCB-DFA-044), redrawn 2026-11-05: the plane is under the solder mask; only the pad's mask opening is
    # exposed. Solid: the opening shows copper all round. Relief: it shows the pad, bare FR4 in the gap, and spokes.
    s = Sheet(980, 540,
              "A through-hole pad in a plane: solid, and with thermal relief",
              "Drawn to scale, top side of the board. In both, the copper plane is under the solder mask and only "
              "the pad's mask opening is bare. Left: the pad is joined to the plane all round, so the plane draws heat "
              "away as fast as the soldering tool supplies it, and the opening shows copper right to its edge. Right: "
              "the same pad separated from the plane by a clearance ring and joined to it by four thin spokes, which "
              "keep the heat in the joint; the opening shows the pad, a little bare FR4 and the ends of the spokes.",
              scale=30, ox=100, oy=80)
    for cx, relief in ((5, False), (17, True)):
        def geom(add, cu, fr4, cx=cx, relief=relief):
            add(s.R(cx - 4.5, 0.5, 9, 9, cu))
            if relief:
                add(s.C(cx, 5, 1.7, fr4))
                for dx, dy, w, h in ((-0.15, -1.7, 0.3, 1.7), (-0.15, 0, 0.3, 1.7), (-1.7, -0.15, 1.7, 0.3), (0, -0.15, 1.7, 0.3)):
                    add(s.R(cx + dx, 5 + dy, w, h, cu))
            add(s.C(cx, 5, 1.0, cu))
        s.board_view((cx - 4.5, 0.5, 9, 9), geom, [s.C(cx, 5, 1.15, "bg")], [(cx, 5, 0.5)])
    s.text("✗ Solid connection", 5, 12.4, size=14, anchor="middle", weight="600")
    s.text("✓ Thermal relief", 17, 12.4, size=14, anchor="middle", weight="600")
    s.balloon(1, (8, 2), (s.X(8.8), s.Y(-0.4)), "Copper plane, under the mask")
    s.balloon(2, (5 + 1.05, 5.3), (s.X(1.2), s.Y(10.3)), "Copper right to the opening's edge")
    s.balloon(3, (18.3, 6.1), (s.X(20.6), s.Y(10.3)), "Clearance ring")
    s.balloon(4, (17, 3.6), (s.X(20.6), s.Y(-0.4)), "Spokes", "Longer and narrower keep more heat in")
    f = s.f
    y = key_below(s, s.Y(12.4) + 60 * f) + 12 * f
    s.legend(40, y, [("cu-exposed", "Exposed copper"), ("fr4-exposed", "Exposed FR4")])
    s.legend(330, y, [("mask-on-cu", "Mask over copper"), ("mask-on-fr4", "Mask over FR4")])
    s.legend(620, y, [("drill", "Hole")])
    notes_at(s, y + 40 * f, ["Drawn to scale. Use spokes on every layer the pad connects to (PCB-DFA-044)."])
    s.save(out(19, "thermal-relief"))


def rf_shields():
    # Side views: a one-piece shield over small parts, and a two-piece shield (frame soldered, lid fitted last).
    s = Sheet(980, 560,
              "One-piece and two-piece RF shields",
              "Drawn to scale, side views of a 1.6 mm board. Left: a one-piece shield, a closed metal can soldered "
              "over small parts, which hides them from inspection once it is on. Right: a two-piece shield: an "
              "open frame soldered with the other parts, so the parts inside can still be inspected, and a lid "
              "pressed on at the end.",
              scale=24, ox=46, oy=200)
    T = 1.6

    def board(x0):
        s.rect(x0, 0, 16, T, "mask")
        for x in (x0 + 4, x0 + 6.5, x0 + 9, x0 + 11):
            s.rect(x, -0.35, 1.0, 0.35, "part")
        s.rect(x0 + 7.2, -0.8, 1.6, 0.8, "part")
    board(0)
    s.rect(2, -2.8, 12, 0.15, "stub")
    s.rect(2, -2.8, 0.15, 2.8, "stub")
    s.rect(13.85, -2.8, 0.15, 2.8, "stub")
    board(20)
    s.rect(22, -2.5, 0.15, 2.5, "stub")
    s.rect(33.85, -2.5, 0.15, 2.5, "stub")
    s.rect(21.8, -5.4, 12.4, 0.15, "stub")
    s.rect(21.8, -5.4, 0.15, 1.2, "stub")
    s.rect(34.05, -5.4, 0.15, 1.2, "stub")
    s.text("One-piece: thousands of boards", 8, -6.6, size=14, anchor="middle", weight="600")
    s.text("Two-piece: up to a few hundred", 28, -6.6, size=14, anchor="middle", weight="600")
    s.balloon(1, (8, -2.73), (s.X(8), s.Y(-4.6)), "One-piece shield", "Hides the parts under it once fitted")
    s.balloon(2, (22.07, -1.5), (s.X(19), s.Y(-3.4)), "Frame", "Soldered with the other parts", free=True)
    s.balloon(3, (33.6, -5.33), (s.X(36.6), s.Y(-3.6)), "Lid", "Pressed on after inspection", free=True)
    s.balloon(4, (26.5, -0.3), (s.X(28), s.Y(-3.6)), "Parts inside", "Still visible to inspection")
    key_below(s, s.Y(T) + 60 * s.f, ["Drawn to scale. Board 1.6 mm.",
                                      "Shield clips work like a two-piece shield (PCB-DFA-050)."])
    s.save(out(20, "rf-shields"))


def cleaning_gap():
    # Side views: the gap under a QFN and under a BGA.
    s = Sheet(980, 520,
              "The gap under a QFN and under a BGA",
              "Enlarged and drawn to scale, side views. Left: a QFN sits on its soldered pads only about 0.05 mm "
              "above the board, leaving almost no room for cleaning fluid to get under it. Right: a BGA's solder "
              "balls hold it about 0.3 mm above the board, leaving a gap the fluid can reach and rinse.",
              scale=60, ox=60, oy=200)
    # QFN 4 x 0.9 on 0.05 standoff
    s.rect(0, 0, 5, 0.3, "mask")
    s.rect(0.5, -0.05, 4, 0.05, "paste")
    s.rect(0.5, -0.95, 4, 0.9, "part")
    # BGA 5 mm wide, balls 0.4 mm dia at 0.8 pitch, standoff 0.3
    s.rect(8, 0, 6, 0.3, "mask")
    for i in range(6):
        s.circle(8.6 + i * 0.95, -0.15, 0.2, "paste")
    s.rect(8.4, -0.3 - 1.0, 5.2, 1.0, "part")
    s.dim_v(-0.05, 0, 5.4, "0.05", ext_from=4.5)
    s.dim_v(-0.3, 0, 14.0, "0.3", ext_from=13.6)
    s.text("QFN: hard to clean under", 2.5, -1.9, size=14, anchor="middle", weight="600")
    s.text("BGA: room for the fluid", 11, -1.9, size=14, anchor="middle", weight="600")
    s.balloon(1, (2.5, -0.5), (s.X(2.5), s.Y(1.5)), "QFN body", "About 0.05 mm above the board")
    s.balloon(2, (10.5, -0.15), (s.X(10.5), s.Y(1.5)), "Solder balls", "Hold the BGA about 0.3 mm up")
    key_below(s, s.Y(1.5) + 60 * s.f, [
        "Enlarged and drawn to scale (gaps approximate).",
        "Give parts on washed boards as much clearance underneath as you can (PCB-DFA-057)."])
    s.save(out(21, "cleaning-gap"))



def _rot(pts, px, py, a):
    import math
    c, sn = math.cos(a), math.sin(a)
    return [(px + (x - px) * c - (y - py) * sn, py + (x - px) * sn + (y - py) * c) for x, y in pts]


def standoff_paste():
    # D34 (I16, PCB-DFA-019; Q88, Q91): a surface-mount standoff with no paste in its footprint vs the maker's stencil.
    # The hole is drawn plated, as on nearly every real board (Chris, Q91), although this maker asks for non-plated.
    # Geometry from Würth Elektronik's WA-SMSI M3 datasheet (9774xxx360R, here 5 mm long) and the WA-SMSx flyer:
    # body 6.0 mm, locating collar 4.2 mm x 1.4 mm, M3 through thread; land pattern: 7.4 mm pad, 4.4 mm NON-plated
    # hole; stencil: ring 4.48-7.27 mm split by four 0.8 mm webs, paste at least 150 um thick.
    CU, SM, T = 0.07, 0.04, 1.6          # copper and mask drawn thicker than true scale so they can be seen
    PAD, HOLE, BODY, COLLAR, BORE, LEN, CL = 3.7, 2.2, 3.0, 2.1, 1.25, 5.0, 1.4
    S_IN, S_OUT, WEB = 2.24, 3.635, 0.8
    s = Sheet(1000, 1140, "A surface-mount standoff: no paste in the footprint vs the maker's stencil",
              "Drawn to scale except copper and mask thickness, after a maker's datasheet for an M3 surface-mount "
              "standoff 5 mm long, with the plated hole most boards use. Top: plan views of the footprint, a 7.4 mm round "
              "copper pad around a 4.4 mm plated hole. Left, marked wrong: no paste in the footprint, so the pad stays bare. Right, marked "
              "right: the maker's stencil, a ring of paste from 4.48 to 7.27 mm split into four segments by 0.8 mm "
              "webs. Bottom: cut-away side views after reflow. The standoff's 6 mm body sits on the pad and its "
              "4.2 mm locating collar drops 1.4 mm into the hole; its M3 thread runs right through. Left: no solder, "
              "so the standoff sits loose on the pad. Right: solder under the body, a fillet from the body out "
              "to the pad's edge, and solder drawn down the plated hole round the collar.",
              scale=29, ox=80, oy=90)
    cy, top = 4.0, 17.0
    f = s.f
    for i, paste in enumerate((False, True)):
        cx = 5.5 + i * 13.5
        # plan view
        s.rect(cx - 5, cy - 4.5, 10, 9, "mask-on-fr4")
        s.circle(cx, cy, PAD + 0.075, "fr4-exposed")
        s.circle(cx, cy, PAD, "cu-exposed")
        if paste:
            s.circle(cx, cy, S_OUT, "solder-paste")
            s.rect(cx - WEB / 2, cy - S_OUT, WEB, 2 * S_OUT, "cu-exposed")
            s.rect(cx - S_OUT, cy - WEB / 2, 2 * S_OUT, WEB, "cu-exposed")
            s.circle(cx, cy, S_IN, "cu-exposed")
        s.circle(cx, cy, HOLE, "drill")
        s.text(["\u2717 No paste in the footprint", "\u2713 Paste openings as the maker draws them"][i], s.X(cx),
               s.Y(-1.3), size=14, anchor="middle", weight="600", px=True)
        s.text("Plan view of the footprint", s.X(cx), s.Y(cy + 5.3), size=12, cls="muted", anchor="middle", px=True)
        # side view, cut through the middle: board with a non-plated hole
        for sgn in (-1, 1):
            x_in, x_out = cx + sgn * HOLE, cx + sgn * 5             # x_in: the finished (plated) hole wall
            x_dr = cx + sgn * (HOLE + CU)                             # the drilled wall, inside the plating
            s.rect(min(x_dr, x_out), top, abs(x_out - x_dr), T, "fr4-exposed")
            x_pad = cx + sgn * PAD
            s.rect(min(x_in, x_pad), top - CU, abs(x_pad - x_in), CU, "cu-exposed")
            x_m = cx + sgn * (PAD + 0.075)
            s.rect(min(x_m, x_out), top - SM, abs(x_out - x_m), SM, "mask-on-fr4")
            s.rect(min(x_in, x_pad), top + T, abs(x_pad - x_in), CU, "cu-exposed")       # bottom pad
            s.rect(min(x_m, x_out), top + T, abs(x_out - x_m), SM, "mask-on-fr4")
            s.rect(min(x_in, x_dr), top - CU, CU, T + 2 * CU, "cu-exposed")  # plating on the hole wall
        gap = 0.1 if paste else 0.0
        base = top - CU - gap                                    # the standoff's shoulder
        if paste:                                                # solder first, the part on top
            for sgn in (-1, 1):                                  # drawn down the plated hole round the collar
                poly(s, [(cx + sgn * HOLE, base), (cx + sgn * COLLAR, base), (cx + sgn * COLLAR, base + CL),
                         (cx + sgn * HOLE, base + CL + 0.15)], "solder")
                poly(s, [(cx + sgn * S_IN, top - CU), (cx + sgn * PAD, top - CU), (cx + sgn * BODY, base - 0.65),
                         (cx + sgn * BODY, base), (cx + sgn * S_IN, base)], "solder")
        for sgn in (-1, 1):                                      # body and collar, cut away to show the bore
            poly(s, [(cx + sgn * BORE, base - LEN), (cx + sgn * BODY, base - LEN), (cx + sgn * BODY, base),
                     (cx + sgn * COLLAR, base), (cx + sgn * COLLAR, base + CL), (cx + sgn * BORE, base + CL)], "foil")
        s.text("After reflow, cut-away side view", s.X(cx), s.Y(top + T + 1.2), size=12, cls="muted",
               anchor="middle", px=True)
    L, R = 5.5, 19.0
    s.dim_h(L - HOLE, L + HOLE, cy + 0.9, "\u2300 4.4 hole")
    s.dim_h(L - PAD, L + PAD, -0.4, "\u2300 7.4 pad", ext_from=cy)
    s.dim_h(L - BODY, L + BODY, top - LEN - 0.9, "\u2300 6.0", ext_from=top - LEN)
    s.dim_v(top - CU - LEN, top - CU, L + 4.4, "5.0", ext_from=L + BODY)
    s.balloon(1, (L + 1.56, cy - 1.56), (s.X(L) + 190, s.Y(cy) - 80), "Plated hole, 4.4 mm",
              "As on nearly every board")
    s.balloon(2, (L - 3.0, cy + 1.6), (s.X(L) - 150, s.Y(cy) + 20), "Copper pad, 7.4 mm", "Bare: nothing to solder")
    s.balloon(3, (R + 2.1, cy - 2.1), (s.X(R) + 160, s.Y(cy) - 90), "Paste: ring 4.48 to 7.27 mm",
              "Four segments with 0.8 mm webs")
    s.balloon(4, (R + 2.2 - 0.05, top + 0.7), (s.X(R) + 160, s.Y(top) + 30), "Locating collar, 4.2 mm",
              "Drops 1.4 mm into the hole and centers the standoff")
    s.balloon(5, (R + 3.35, top - 0.3), (s.X(R) + 160, s.Y(top) - 40), "Solder fillet",
              "Some solder also drains down the hole")
    s.balloon(6, (L - 2.6, top - CU), (s.X(L) - 150, s.Y(top) - 40), "No joint",
              "The standoff just sits on the pad")
    s.balloon(7, (R, top - 3.0), (s.X(R) + 160, s.Y(top) - 120), "M3 thread, open at both ends",
              "The screw comes up through the hole")
    ky = s.Y(top + T + 1.2) + 56 * f
    y1 = s.key(40, ky, width=510, only=(1, 2, 3, 4))
    y2 = s.key(590, ky, width=370, title="", only=(5, 6, 7))
    s.legend(s.X(R + 6.2), s.Y(cy - 0.6), [("cu-exposed", "Exposed copper"), ("fr4-exposed", "FR4 (cut)"),
                                           ("drill", "Hole"), ("solder-paste", "Solder paste"),
                                           ("solder", "Solder"), ("foil", "Standoff, steel")])
    notes_at(s, max(y1, y2) + 16 * f, [
        "Drawn to scale except copper and mask thickness. Steel and FR4 are shown cut.",
        "The maker's stencil is a starting point: the assembler often prints more paste than this.",
        "After a maker's datasheet: M3 standoff, 5 mm long, drawn with the plated hole most boards use."])
    s.save(out(34, "standoff-paste"))


def joined_pins():
    # D36 (I20, PCB-DFA-038): two neighboring pins joined in copper. Right: the link is under the mask and a dam
    # stays between the pads, giving two normal joints. Wrong: the copper between them is bare, so solder runs across
    # and it looks like a bridge. 0.5 mm pitch, 0.25 mm pads, 0.075 mm mask margin (PCB-DFA-032).
    s = Sheet(760, 660, "Two pins joined in copper: under the mask with a dam, vs bare copper between",
              "Drawn to scale, plan views of four leads of a 0.5 mm-pitch part after soldering; the middle two are "
              "meant to be connected. Left, marked right: they are joined by copper under the solder mask, with a mask "
              "dam between their pads, so each has its own normal joint. Right, marked wrong: the copper between the "
              "two pads is left bare, so solder runs across it and the pair looks like a solder bridge.",
              scale=95, ox=70, oy=110)
    W, L, M = 0.25, 1.5, 0.075
    for v, good in enumerate((True, False)):
        dx = v * 3.4
        xs = [dx + 0.55 + 0.5 * k for k in range(4)]
        s.rect(dx, 0, 2.6, 2.4, "mask-on-fr4")
        a, b = xs[1] + W / 2, xs[2] - W / 2
        if good:
            s.rect(a - 0.01, 0.95, b - a + 0.02, 0.5, "mask-on-cu")
            for x in xs:
                s.rect(x - W / 2 - M, 0.45 - M, W + 2 * M, L + 2 * M, "fr4-exposed")
            s.rect(a, 0.95, M, 0.5, "cu-exposed"); s.rect(b - M, 0.95, M, 0.5, "cu-exposed")
        else:
            for k, x in enumerate(xs):
                if k in (0, 3):
                    s.rect(x - W / 2 - M, 0.45 - M, W + 2 * M, L + 2 * M, "fr4-exposed")
            s.rect(xs[1] - W / 2 - M, 0.45 - M, xs[2] - xs[1] + W + 2 * M, L + 2 * M, "fr4-exposed")
            s.rect(a, 0.95, b - a, 0.5, "cu-exposed")
        for x in xs:
            s.rect(x - W / 2, 0.45, W, L, "cu-exposed")
        for k, x in enumerate(xs):
            if good or k in (0, 3):
                s.rect(x - 0.12, 0.6, 0.24, 1.25, "solder", rx=0.05)
        if not good:
            s.rect(xs[1] - 0.12, 0.6, xs[2] - xs[1] + 0.24, 1.25, "solder", rx=0.05)
        for x in xs:
            s.rect(x - 0.09, -0.05, 0.18, 1.7, "foil")
        s.text(["✓ Joined under the mask, with a dam", "✗ Copper left bare between them"][v], s.X(dx + 1.3),
               s.Y(-0.45), size=14, anchor="middle", weight="600", px=True)
    s.balloon(1, (1.3, 1.2), (s.X(1.3), s.Y(3.0)), "Copper link under the mask")
    s.balloon(2, (1.3, 0.55), (s.X(-0.35), s.Y(0.2)), "Mask dam between the pads", "Two separate, normal joints")
    s.balloon(3, (3.4 + 1.3, 1.2), (s.X(3.4 + 1.3), s.Y(3.0)), "Bare copper between the pads",
              "Solder runs across: it looks like a bridge")
    s.key(70, 420, width=380)
    s.legend(500, 432, [("cu-exposed", "Exposed copper"), ("fr4-exposed", "Exposed FR4"), ("mask-on-cu", "Mask over copper"),
                        ("mask-on-fr4", "Mask over FR4"), ("solder", "Solder"), ("foil", "Lead")])
    note_lines(s, 500, 580, [
        "Drawn to scale. 0.5 mm pitch,",
        "0.25 mm pads, 0.075 mm mask margin",
        "(PCB-DFA-032)."])
    s.save(out(36, "joined-pins"))


def _pth(s, x, top, T=1.6, hole=0.9, pad=1.5, fill=True):
    """A plated hole in side view: solder fill (optional), copper barrel and pads."""
    if fill:
        s.rect(x - hole / 2, top, hole, T, "solder")
    s.rect(x - hole / 2 - 0.06, top, 0.06, T, "cu-exposed")
    s.rect(x + hole / 2, top, 0.06, T, "cu-exposed")
    s.rect(x - pad / 2, top - 0.06, pad, 0.06, "cu-exposed")
    s.rect(x - pad / 2, top + T, pad, 0.06, "cu-exposed")


def hybrid_usbc():
    # D37 (I21, PCB-DFA-040): side view of a hybrid USB-C receptacle: through-hole shell pegs soldered through the
    # board, surface-mount signal pins at the back.
    s = Sheet(760, 570, "A hybrid USB-C connector: through-hole pegs, surface-mount signal pins",
              "Drawn to scale except copper thickness, side view of a USB-C receptacle on a 1.6 mm board. Its metal "
              "shell has two pegs that go through plated holes and are soldered through the board, which takes the "
              "force of plugging and unplugging. Its signal pins come out of the back and are soldered to pads on the "
              "surface.",
              scale=40, ox=140, oy=40)
    top = 5
    s.rect(-1.5, top, 12, 1.6, "mask-on-fr4")
    for x in (1.6, 5.6):
        _pth(s, x, top, hole=1.0, pad=1.6)
    s.rect(0, top - 3.26, 7.35, 3.26, "foil", rx=0.4)
    s.rect(0.3, top - 2.6, 1.2, 1.9, "part")
    for x in (1.6, 5.6):
        _fillet(s, x, top + 1.66, 1, 0.8, 0.3, 0.6)
        s.rect(x - 0.3, top - 0.2, 0.6, 1.6 + 0.9, "foil")
    s.rect(7.5, top - 0.06, 1.0, 0.06, "cu-exposed")
    s.rect(7.35, top - 0.75, 0.4, 0.15, "foil")
    s.rect(7.6, top - 0.75, 0.15, 0.65, "foil")
    s.rect(7.6, top - 0.21, 0.75, 0.15, "foil")
    poly(s, [(7.5, top - 0.06), (7.75, top - 0.5), (7.75, top - 0.06)], "solder")
    poly(s, [(8.35, top - 0.21), (8.5, top - 0.06), (8.35, top - 0.06)], "solder")
    s.balloon(1, (1.6, top + 2.1), (s.X(-1.5) - 40, s.Y(top + 3.2)), "Through-hole shell pegs",
              "Soldered through the board; take the plugging force")
    s.balloon(2, (7.9, top - 0.15), (s.X(10.5), s.Y(top - 2.6)), "Surface-mount signal pins", "Soldered in reflow with the rest")
    s.balloon(3, (3.5, top - 3.26), (s.X(3.5), s.Y(top - 4.4)), "Metal shell")
    s.key(80, 380, width=380)
    s.legend(500, 392, [("foil", "Metal"), ("cu-exposed", "Copper"), ("solder", "Solder"), ("mask-on-fr4", "Board")])
    note_lines(s, 500, 496, [
        "Drawn to scale except copper thickness.",
        "Receptacle about 7.35 mm deep",
        "and 3.26 mm tall."])
    s.save(out(37, "hybrid-usbc"))


def lead_length():
    # D38 (I22, PCB-DFA-045): two neighboring through-hole leads at 1.27 mm pitch: about 1 mm out (a good fillet),
    # too short (no fillet on the solder side), too long (solder bridges the long leads).
    s = Sheet(760, 640, "Through-hole lead length at fine pitch",
              "Drawn to scale except copper thickness, side views through two neighboring leads of a 1.27 mm-pitch "
              "connector on a 1.6 mm board, three times. Left, marked right: the leads stick out about 1 mm and each "
              "has a full fillet. Middle, marked wrong: the leads end inside the holes, with no fillet on the solder "
              "side. Right, marked wrong: the leads stick out about 4 mm, and solder bridges between them against the board.",
              scale=45, ox=60, oy=130)
    for i, prot in enumerate((1.0, -0.4, 4.0)):
        dx = i * 4.6
        xs = (dx + 1.17, dx + 1.17 + 1.27)
        s.rect(dx, 0, 3.6, 1.6, "mask-on-fr4")
        for x in xs:
            _pth(s, x, 0, hole=0.8, pad=1.0, fill=(prot > 0))
            if prot <= 0:
                s.rect(x - 0.4, 0.5, 0.8, 1.1, "solder")
        s.rect(dx + 0.3, -2.0, 3.0, 2.0, "part")
        if prot > 3:                                  # a bridge forms against the board, between the fillets
            poly(s, [(xs[0], 1.66), (xs[1], 1.66), (xs[1], 2.6), (xs[0] + 0.9, 2.45), (xs[0] + 0.37, 2.45), (xs[0], 2.6)], "solder")
        for x in xs:
            if prot > 0:
                _fillet(s, x, 1.66, 1, 0.5, 0.25, 0.65)
            s.rect(x - 0.25, -1.5, 0.5, 1.5 + 1.6 + prot, "foil")
        s.text(["✓ About 1 mm through", "✗ Too short", "✗ Too long"][i], s.X(dx + 1.8), s.Y(-2.6),
               size=14, anchor="middle", weight="600", px=True)
    s.balloon(1, (1.17 + 0.42, 2.0), (s.X(1.17) - 10, s.Y(5.4)), "A full fillet round the lead")
    s.balloon(2, (4.6 + 1.17, 1.2), (s.X(4.6 + 1.8), s.Y(5.4)), "Lead ends inside the hole", "No fillet on the solder side")
    s.balloon(3, (9.2 + 1.8, 2.3), (s.X(9.2 + 3.6) + 20, s.Y(5.4)), "Solder bridges the long leads", "Right against the board")
    s.key(60, 420, width=380)
    note_lines(s, 480, 440, [
        "Drawn to scale except copper thickness.",
        "1.27 mm pitch, 0.5 mm leads, 1.6 mm board.",
        "About 1 mm out suits single-nozzle",
        "selective soldering (PCB-DFA-045)."])
    s.save(out(38, "lead-length"))


def self_holding():
    # D39 (I23, PCB-DFA-046), redrawn 2026-11-05: the same right-angle connector twice, its front overhanging the
    # board edge. With snap-in pegs it stays flat; without them its weight, which is out over the edge, tips it
    # forward and lifts its back pins in their holes.
    s = Sheet(760, 600, "The same part with and without snap-in pegs",
              "Side views of the same right-angle connector at the edge of a board, before soldering. Its housing "
              "reaches past the board edge, so most of its weight is in front of its pins. Left, marked right: the "
              "connector has snap-in pegs whose barbs hook under the board, so it stays flat. Right, marked wrong: the "
              "same connector without pegs tips forward over the edge under its own weight, lifting its pins in their "
              "holes.",
              scale=24, ox=60, oy=90)
    top = 8

    def connector(dx, pegs, a):
        pv = (dx + 8, top)
        Rt = lambda pts: _rot(pts, pv[0], pv[1], a)
        s.rect(dx, top, 8, 1.6, "mask-on-fr4")
        for x in (dx + 1.2, dx + 2.4) + ((dx + 5.5,) if pegs else ()):
            s.rect(x - 0.45, top, 0.9, 1.6, "drill")
        for p in ([(dx + 3.0, top - 3.2), (dx + 1.2, top - 3.2), (dx + 1.2, top + 2.4)],
                  [(dx + 3.0, top - 1.6), (dx + 2.4, top - 1.6), (dx + 2.4, top + 2.4)]):
            s.d.append(s.PL(Rt(p), "s-foil-edge", 0.62))
            s.d.append(s.PL(Rt(p), "s-foil", 0.5))
        if pegs:
            x = dx + 5.5
            for shape in ([(x - 0.4, top), (x + 0.4, top), (x + 0.4, top + 2.3), (x - 0.4, top + 2.3)],
                          [(x - 0.8, top + 1.6), (x - 0.4, top + 1.6), (x - 0.4, top + 2.4)],
                          [(x + 0.8, top + 1.6), (x + 0.4, top + 1.6), (x + 0.4, top + 2.4)]):
                poly(s, shape, "part")
        poly(s, Rt([(dx + 3, top - 4.5), (dx + 10, top - 4.5), (dx + 10, top), (dx + 3, top)]), "part")
        poly(s, Rt([(dx + 9.6, top - 3.7), (dx + 10, top - 3.7), (dx + 10, top - 0.8), (dx + 9.6, top - 0.8)]), "foil")
    connector(0, True, 0.0)
    connector(15, False, 0.12)
    s.text("✓ Snap-in pegs hold it flat", s.X(5), s.Y(-1.5), size=14, anchor="middle", weight="600", px=True)
    s.text("✗ No pegs: tips forward over the edge", s.X(20), s.Y(-1.5), size=14, anchor="middle", weight="600", px=True)
    s.balloon(1, (5.5 - 0.6, top + 1.9), (s.X(3), s.Y(top + 5)), "Snap-in peg", "Barbs hook under the board")
    s.balloon(2, (15 + 10, top + 0.2), (s.X(15 + 12), s.Y(top + 4)), "Weight past the edge", "Tips the part forward")
    s.balloon(3, (15 + 1.2, top - 0.1), (s.X(15 + 1.2) - 30, s.Y(top + 5)), "Pins lift in their holes")
    s.key(60, 440, width=380)
    note_lines(s, 480, 460, [
        "Side views, before soldering.",
        "PCB-DFA-046."])
    s.save(out(39, "self-holding"))


def bolt_first():
    # D40 (I24, PCB-DFA-048): a connector bolted to the board. Wrong: soldered first, then tightened: the flange is
    # pulled down to the board and the solder joints are strained. Right: tightened first, then soldered.
    s = Sheet(760, 580, "Bolted connector: soldered then tightened, vs tightened then soldered",
              "Side views of a connector whose metal flange is bolted to the board, with three leads soldered through "
              "it. Left, marked wrong: the leads were soldered while the flange stood slightly off the board; "
              "tightening the bolts afterwards pulls the flange down, bending it and straining the solder joints, "
              "marked in red. Right, marked right: the bolts were tightened first, so the flange sits flat and the "
              "joints carry no strain.",
              scale=22, ox=60, oy=70)
    top = 8
    for i in range(2):
        dx = i * 15.5
        s.rect(dx, top, 14, 1.6, "mask-on-fr4")
        lift = 0.0 if i else 0.45
        if i == 0:
            poly(s, [(dx + 1, top - 0.6), (dx + 3, top - 0.6 - lift), (dx + 11, top - 0.6 - lift), (dx + 13, top - 0.6),
                     (dx + 13, top), (dx + 11, top - lift), (dx + 3, top - lift), (dx + 1, top)], "foil")
        else:
            s.rect(dx + 1, top - 0.6, 12, 0.6, "foil")
        s.rect(dx + 3, top - 0.6 - lift - 4.5, 8, 4.5, "part")
        for x in (dx + 2, dx + 12):
            s.rect(x - 0.6, top - 1.2, 1.2, 0.6, "foil")
            s.rect(x - 0.25, top - 0.6, 0.5, 1.6 + 1.4, "foil")
            s.rect(x - 0.7, top + 1.6, 1.4, 0.6, "foil")
        for x in (dx + 5, dx + 7, dx + 9):
            _pth(s, x, top, hole=0.8, pad=1.2)
            _fillet(s, x, top + 1.66, 1, 0.6, 0.2, 0.55)
            s.rect(x - 0.2, top - 0.6 - lift, 0.4, 0.6 + lift + 1.6 + 0.8, "foil")
            if i == 0:
                s.circle(x, top + 1.9, 0.3, "contact")
        s.text(["✗ Soldered, then tightened", "✓ Tightened, then soldered"][i], s.X(dx + 7), s.Y(-0.6),
               size=14, anchor="middle", weight="600", px=True)
    s.balloon(1, (12, top - 0.3), (s.X(12) + 20, s.Y(1.5)), "Flange pulled down by the bolts", "Bent after the joints set")
    s.balloon(2, (7, top + 1.9), (s.X(7), s.Y(top + 5)), "Strained solder joints")
    s.balloon(3, (15.5 + 12, top - 0.9), (s.X(15.5 + 12) + 20, s.Y(1.5)), "Bolt tightened first", "Flange flat on the board")
    s.key(60, 410, width=380)
    note_lines(s, 480, 430, [
        "Side views. Flange lift exaggerated.",
        "Give a torque for every screw and nut",
        "(PCB-DFA-048)."])
    s.save(out(40, "bolt-first"))


def hold_downs():
    # D41 (I25, PCB-DFA-051): two hardware hold-downs for a heavy capacitor: a bracket with screws through the board
    # and nuts beneath, and a cable tie through two holes and round the part.
    import math
    s = Sheet(760, 690, "Holding a heavy capacitor down: a bracket, or a cable tie",
              "Drawn to scale except the board, side views of a 16 mm capacitor on a board, twice. Left: a hold-down "
              "bracket fits over the capacitor and is screwed through the board, with nuts underneath. Right: the "
              "capacitor lies on its side and a cable tie passes through two holes in the board and round it. In both, "
              "the hold-down, not the solder joints, carries the part's weight under vibration.",
              scale=9, ox=60, oy=110)
    top = 40
    dx = 0
    s.rect(dx, top, 34, 1.6, "mask-on-fr4")
    for x in (dx + 14, dx + 20):
        _fillet(s, x, top + 1.66, 1, 1.0, 0.3, 0.9)
        s.rect(x - 0.3, top - 0.5, 0.6, 3.2, "foil")
    s.rect(dx + 9, top - 30, 16, 30, "foil", rx=1)
    for r in ((dx + 5, top - 32, 24, 2), (dx + 5, top - 32, 2, 30), (dx + 27, top - 32, 2, 30),
              (dx + 2, top - 2, 5, 2), (dx + 27, top - 2, 5, 2)):
        s.rect(*r, "part")
    for x in (dx + 3.5, dx + 30.5):
        s.rect(x - 1, top - 3.2, 2, 1.2, "foil")
        s.rect(x - 0.5, top - 2, 1, 2 + 1.6 + 1.6, "foil")
        s.rect(x - 1.3, top + 1.6, 2.6, 1.3, "foil")
    s.text("✓ Bracket screwed through the board", s.X(dx + 17), s.Y(top - 36), size=14, anchor="middle",
           weight="600", px=True)
    dx = 40
    s.rect(dx, top, 34, 1.6, "mask-on-fr4")
    cx, cy, r = dx + 17, top - 8, 8
    rt = r + 0.6                                  # the tie hugs the capacitor, then drops through two holes
    for x in (cx - rt, cx + rt):
        s.rect(x - 0.8, top, 1.6, 1.6, "drill")
    s.circle(cx, cy, r, "foil")
    s.circle(cx, cy, r - 1.2, "thin")
    yb, rc = top + 1.6 + 0.6, 1.6                 # run under the board, with round corners
    p = dw.Path(class_="s-part", stroke_width=s.L(1.0))
    p.M(s.X(cx), s.Y(yb))
    p.L(s.X(cx - rt + rc), s.Y(yb))
    p.A(s.L(rc), s.L(rc), 0, 0, 1, s.X(cx - rt), s.Y(yb - rc))
    p.L(s.X(cx - rt), s.Y(cy))
    p.A(s.L(rt), s.L(rt), 0, 0, 1, s.X(cx + rt), s.Y(cy))
    p.L(s.X(cx + rt), s.Y(yb - rc))
    p.A(s.L(rc), s.L(rc), 0, 0, 1, s.X(cx + rt - rc), s.Y(yb))
    p.Z()
    s.d.append(p)
    s.text("✓ Cable tie through two holes", s.X(dx + 17), s.Y(top - 36), size=14, anchor="middle", weight="600", px=True)
    s.balloon(1, (17, top - 31), (s.X(17) + 130, s.Y(top - 20)), "Hold-down bracket")
    s.balloon(2, (30.5, top + 2.2), (s.X(34) + 10, s.Y(top + 6)), "Screw through the board, nut beneath")
    s.balloon(3, (40 + 17, cy - r - 0.6), (s.X(40 + 17) + 120, s.Y(top - 20)), "Cable tie round the part",
              "Through two holes in the board")
    s.key(60, 540, width=400)
    note_lines(s, 500, 560, [
        "Drawn to scale except the board thickness.",
        "Example: 16 mm capacitor.",
        "Fit the bracket or tie before the part",
        "is soldered (PCB-DFA-051)."])
    s.save(out(41, "hold-downs"))


def underfill_corners():
    # D42 (I26, PCB-DFA-054), redrawn 2026-11-05: underfill and corner-bond adhesive are viscous, so their edges are
    # rounded menisci, and corner-bond adhesive wicks a little way under the package.
    import math
    import drawsvg as dw
    s = Sheet(780, 640, "Underfill under a BGA, and corner bonding",
              "Drawn to scale, side views of a BGA on its solder balls, with plan views beside them. Top: underfill "
              "fills the whole gap under the package, round every ball, with a rounded fillet along its edges. "
              "Bottom: corner bonding puts a bead of adhesive at each of the package's four corners; being a viscous "
              "fluid, it has soft, rounded edges and wicks a little way under the package, but the rest of the gap "
              "stays open.",
              scale=32, ox=60, oy=80)

    def meniscus(x_side, y_top_of_side, x_foot, y_board, n=12):
        # concave fillet from the package side down to the board: an elliptical arc centered away from the corner
        cxm, cym = x_foot, y_top_of_side
        rx, ry = x_side - x_foot, y_board - y_top_of_side
        return [(cxm + rx * math.cos(t), cym + ry * math.sin(t)) for t in [k * (math.pi / 2) / n for k in range(n + 1)]]

    for v in range(2):
        top = 3 + v * 6
        s.rect(0, top, 14, 1.6, "mask-on-fr4")
        if v == 0:
            s.rect(1, top - 0.35, 12, 0.36, "adhesive")
            for side in (-1, 1):
                xs = 1 if side < 0 else 13
                arc = meniscus(xs, top - 0.62, xs + side * 0.8, top)
                poly(s, arc + [(xs, top)], "adhesive")
        else:
            for side in (-1, 1):
                xs = 1 if side < 0 else 13
                arc = meniscus(xs, top - 1.0, xs + side * 1.3, top)
                poly(s, arc + [(xs, top)], "adhesive")
                s.rect(min(xs, xs - side * 1.4), top - 0.36, 1.4, 0.37, "adhesive", rx=0.17)
        for k in range(14):
            s.circle(1.6 + 0.8 * k, top - 0.2, 0.24, "solder")
        s.rect(1, top - 0.71, 12, 0.36, "part")
        s.rect(1.5, top - 1.51, 11, 0.8, "part")
        s.text(["Underfill", "Corner bonding"][v], s.X(0), s.Y(top - 2.2), size=14, weight="600", px=True)
        x0, y0 = 560, s.Y(top - 1.6) - 40
        s.d.append(dw.Rectangle(x0, y0, 130, 130, class_="mask-on-fr4"))
        if v == 0:
            s.d.append(dw.Rectangle(x0 + 4, y0 + 4, 122, 122, rx=8, class_="adhesive"))
        else:
            for cx, cy in ((x0 + 12, y0 + 12), (x0 + 118, y0 + 12), (x0 + 12, y0 + 118), (x0 + 118, y0 + 118)):
                s.d.append(dw.Ellipse(cx, cy, 15, 13, class_="adhesive"))
        s.d.append(dw.Rectangle(x0 + 10, y0 + 10, 110, 110, class_="part"))
        s.text("Plan view", x0, y0 - 8, size=11, cls="muted", px=True)
    s.balloon(1, (7, 3 - 0.18), (s.X(7), s.Y(4.9)), "Underfill round every ball")
    s.balloon(2, (13.5, 9 - 0.3), (s.X(14) + 20, s.Y(10.6)), "Adhesive at the corners only",
              "Soft edges; wicks a little way under")
    s.key(60, 470, width=420)
    s.legend(540, 482, [("part", "BGA package"), ("solder", "Solder ball"), ("adhesive", "Underfill or adhesive"),
                        ("mask-on-fr4", "Board")])
    note_lines(s, 60, 610, [
        "Drawn to scale: 0.8 mm-pitch BGA, 12 mm package."])
    s.save(out(42, "underfill-corners"))


def coating_keepouts():
    # D43 (I27, PCB-DFA-061): an assembly drawing with do-not-coat areas round a connector, a switch and test points,
    # and 2-3 mm between a keep-out edge and a part that must be coated.
    s = Sheet(900, 1012, "Do-not-coat areas on an assembly drawing",
              "Drawn to scale, plan view of a 60 by 40 mm board as it would appear on an assembly drawing. Areas that "
              "must stay free of conformal coating are outlined in red and labeled: a connector's mating area at the "
              "right edge, a push switch, and a row of test points. The nearest part that must be coated sits 2 to 3 "
              "mm from the edge of the connector's keep-out.",
              scale=12.5, ox=75, oy=110)
    s.rect(0, 0, 60, 40, "mask-on-fr4")
    # traces under the mask, each running between two real connections, with 45-degree bends
    QY = [13.3 + 1.4 * k for k in range(5)]          # QFN side-pad centers
    CYS = [13.1 + 2.6 * k for k in range(6)]         # connector pad centers
    traces = []
    for k in range(5):                               # QFN right side to connector pins 1-5
        d = CYS[k] - QY[k]
        xs = 40 - 1.0 * k
        traces.append([(32.2, QY[k]), (xs, QY[k]), (xs + d, CYS[k]), (51.4, CYS[k])])
    traces.append([(51.4, CYS[5]), (46.0, CYS[5])])  # connector pin 6 to a ground via
    traces.append([(23.8, QY[4]), (19.9, QY[4]), (19.9, 21.0), (13.9, 27.0), (13.0, 27.0)])   # QFN to the switch
    traces.append([(7.0, 33.0), (4.0, 33.0)])                                                  # switch to ground via
    traces.append([(25.3, 20.2), (25.3, 30.0), (24.0, 31.3), (24.0, 34.0)])                   # QFN to TP1
    traces.append([(29.5, 20.2), (29.5, 32.0), (29.0, 32.5), (29.0, 34.0)])                   # QFN to TP2
    traces.append([(30.9, 20.2), (30.9, 24.0), (34.0, 27.1), (34.0, 34.0)])                   # QFN to TP3
    traces.append([(30.9, 11.8), (30.9, 10.4), (32.85, 8.45), (43.9, 8.45)])                  # QFN to C1
    traces.append([(44.9, 8.45), (45.6, 8.45), (45.6, 5.0)])                                  # C1 to ground via
    traces.append([(25.3, 11.8), (25.3, 6.0), (22.3, 3.0), (6.0, 3.0)])                       # QFN to off-board
    traces.append([(23.8, QY[0]), (12.0, QY[0]), (9.0, 10.3), (3.0, 10.3)])
    for t in traces:
        s.d.append(s.PL(t, "s-mask-on-cu", 0.3))
    for x, y in ((46.0, CYS[5]), (4.0, 33.0), (45.6, 5.0), (3.0, 10.3), (6.0, 3.0), (28.0, 16.0)):
        s.circle(x, y, 0.4, "mask-on-cu"); s.circle(x, y, 0.15, "drill")
    for k in range(6):
        s.rect(50.3, 12.6 + k * 2.6, 2.2, 1.0, "cu-exposed")
    s.d.append(s.PL([(52.8, 11), (60, 11), (60, 29), (52.8, 29), (52.8, 11)], "s-silkscreen", 0.15))
    for k in range(5):
        for x, y, w, h in ((23.4, 13.1 + 1.4 * k, 0.8, 0.4), (31.8, 13.1 + 1.4 * k, 0.8, 0.4),
                           (25.1 + 1.4 * k, 11.4, 0.4, 0.8), (25.1 + 1.4 * k, 19.8, 0.4, 0.8)):
            s.rect(x, y, w, h, "cu-exposed")
    s.rect(25.5, 13.5, 5, 5, "cu-exposed")
    s.circle(28.0, 16.0, 0.15, "drill")
    s.d.append(s.PL([(23.0, 11.0), (33.0, 11.0), (33.0, 21.0), (23.0, 21.0), (23.0, 11.0)], "s-silkscreen", 0.15))
    s.circle(22.4, 10.4, 0.25, "silkscreen")
    for txt, x, y in (("U1", 28.0, 23.2), ("J1", 56.4, 10.2), ("SW1", 10.0, 24.3), ("C1", 44.4, 10.3)):
        s.text(txt, s.X(x), s.Y(y), size=11, cls="silk", anchor="middle", weight="600", px=True)
    for k, x in enumerate((24.0, 29.0, 34.0)):
        s.text(f"TP{k + 1}", s.X(x + 0.9), s.Y(34.45), size=10, cls="silk", weight="600", px=True)
    for x, y in ((7, 27), (13, 27), (7, 33), (13, 33)):
        s.rect(x - 0.6, y - 0.6, 1.2, 1.2, "cu-exposed")
    s.d.append(s.PL([(7, 27), (13, 27), (13, 33), (7, 33), (7, 27)], "s-silkscreen", 0.15))
    s.circle(10, 30, 1.8, "thin")
    for x in (24, 29, 34):
        s.circle(x, 34, 0.6, "fr4-exposed"); s.circle(x, 34, 0.5, "cu-exposed")
    s.rect(43.6, 8.2, 0.6, 0.5, "cu-exposed"); s.rect(44.6, 8.2, 0.6, 0.5, "cu-exposed")
    for x, y, w, h, ly in ((47.6, 9, 12.4, 22, 30.3), (5, 25, 10, 10, 36.3), (21.5, 31.5, 15, 5, 37.8)):
        s.rect(x, y, w, h, "zone"); s.rect(x, y, w, h, "zone-s")
        s.text("DO NOT COAT", s.X(x + w / 2), s.Y(ly), size=10, cls="silk", anchor="middle", weight="700", px=True)
    s.dim_h(45.2, 47.6, -3, "2–3 mm", ext_from=8.2)
    s.balloon(1, (60, 15), (s.X(60) + 25, s.Y(4)), "Connector mating area")
    s.balloon(2, (5, 30), (s.X(-3), s.Y(30)), "Push switch")
    s.balloon(3, (34.0, 34.3), (s.X(34.0), s.Y(40) + 34 * s.f), "Test points you'll probe")
    s.balloon(4, (44.4, 8.45), (s.X(40), s.Y(-3.5)), "Part that must be coated", "2–3 mm from the keep-out", free=True)
    f = s.f
    y = key_below(s, s.Y(40) + 90 * f) + 12 * f
    s.legend(40, y, [("zone", "Do not coat")])
    notes_at(s, y + 20 * f, [
        "Drawn to scale. Dimensions in mm.",
        "2–3 mm is about the closest a selective coating process holds to a keep-out edge (PCB-DFA-061)."])
    s.save(out(43, "coating-keepouts"))


if __name__ == "__main__":
    stencil_area_ratio()
    double_sided_plan()
    part_spacing()
    selective_keepout()
    pin_in_paste()
    thermal_relief()
    rf_shields()
    cleaning_gap()
    standoff_paste()
    joined_pins()
    hybrid_usbc()
    lead_length()
    self_holding()
    bolt_first()
    hold_downs()
    underfill_corners()
    coating_keepouts()
    print("written to", OUT)

"""Part 3 diagrams D1-D5 and D24 in the OpenDFX style.
Run: python3 tools/diagrams/trial_diagrams.py         (writes trials/python-N-<name>.svg for review)
     python3 tools/diagrams/trial_diagrams.py --book  (writes book/02-the-panel/images/<name>.svg)"""
from pathlib import Path
import opendfx_draw
from opendfx_draw import Sheet

import sys

BOOK = "--book" in sys.argv
OUT = (Path(__file__).parent / "trials") if not BOOK else (Path(__file__).parents[2] / "book" / "02-the-panel" / "images")
OUT.mkdir(exist_ok=True)


def key_below(s, y, x=40, width=None, split=None, notes=(), gap=40):
    """The key in two columns under the drawing (DRW1, Q177 option A), then the notes; the sheet is cut to fit.
    split: how many balloons go in the left column (default half, rounded up)."""
    f = s.f
    width = width or s.width - 2 * x
    ns = sorted(n for n, _, _ in s.balloons)
    k = split if split is not None else (len(ns) + 1) // 2
    colw = (width - gap) / 2
    y1 = s.key(x, y, width=colw, only=ns[:k])
    y2 = s.key(x + colw + gap, y, width=colw, title="", only=ns[k:]) if ns[k:] else y1
    y = max(y1, y2) + 12 * f
    for t in notes:
        y += 22 * f
        s.note(t, x, y)
    s.height = y + 18 * f
    return y


def out(n, name):
    """trials/python-<n>-<name>.svg for review, or images/<name>.svg for the book."""
    opendfx_draw.CURRENT_D = n
    return OUT / (f"{name}.svg" if BOOK else f"python-{n}-{name}.svg")


def panel_anatomy():
    # 2 x 2 panel of 70 x 45 mm boards, 10 mm rails top and bottom, V-scored. True scale.
    BW, BH, RAIL = 70, 45, 10
    PW, PH = 2 * BW, 2 * BH + 2 * RAIL
    s = Sheet(800, 850,
              "Panel anatomy: 2 × 2 V-scored panel with rails",
              "Drawn to scale. Four 70 × 45 mm boards in two rows of two, with a 10 mm rail along the top and "
              "bottom long edges, making a 140 × 110 mm panel. The rails carry three global fiducials, one on the top rail and two on the bottom rail, and four "
              "optional 3/16 in tooling holes. Dashed V-score lines run edge to edge between the boards and "
              "between the boards and the rails. Each board has two fiducials near opposite corners. The panel "
              "travels left to right, parallel to the rails.",
              scale=3.7, ox=150, oy=110)
    s.rect(0, 0, PW, RAIL, "waste")
    s.rect(0, PH - RAIL, PW, RAIL, "waste")
    for r in range(2):
        for c in range(2):
            s.rect(c * BW, RAIL + r * BH, BW, BH, "mask")
    s.rect(0, 0, PW, PH, "edge")
    for y in (RAIL, RAIL + BH, PH - RAIL):
        s.line(-3, y, PW + 3, y, "score")
    s.line(BW, -3, BW, PH + 3, "score")
    for x, y in ((5, 5), (PW - 5, 5), (5, PH - 5), (PW - 5, PH - 5)):
        s.circle(x, y, 4.76 / 2, "hole")
    for x, y in ((PW - 15, 5), (15, PH - 5), (PW - 15, PH - 5)):
        s.circle(x, y, 1.0, "bare")
        s.circle(x, y, 0.5, "copper")
    for r in range(2):
        for c in range(2):
            x0, y0 = c * BW, RAIL + r * BH
            for x, y in ((x0 + 5, y0 + 5), (x0 + BW - 5, y0 + BH - 5)):
                s.circle(x, y, 1.0, "bare")
                s.circle(x, y, 0.5, "copper")
    # direction of travel
    s.d.append(__import__("drawsvg").Line(s.X(0), 40, s.X(PW), 40, class_="lead"))
    s._arrowhead(s.X(PW), 40, 0)
    s.text("Direction of travel", s.X(0), 32, size=12, cls="muted", px=True)
    # dimensions
    s.dim_h(0, BW, PH + 9, "70 mm board", ext_from=PH)
    s.dim_h(0, PW, PH + 20, "140 mm panel", ext_from=PH)
    s.dim_v(0, RAIL, -9, "10 mm rail", ext_from=0, text_left=True)
    s.dim_v(RAIL, RAIL + BH, -9, "45 mm board", ext_from=0, text_left=True)
    # balloons
    top = s.Y(0) - 22
    s.balloon(1, (40, 3), (s.X(40) + 30, top), "Rail", "About 10 mm; carried by conveyors and clamps")
    s.balloon(2, (PW - 15, 5), (s.X(PW - 15) - 40, top), "Global fiducial", "On the rail; used while the panel is whole")
    s.balloon(3, (PW - 5, 5), (s.X(PW) - 6, top), "Tooling hole (optional)", "3/16 in at one assembler; now often unused")
    s.balloon(4, (BW + 5, RAIL + 5), (s.X(BW + 5) + 34, s.Y(RAIL + 5) + 30), "Board fiducial", "1 mm dot, 2 mm mask opening, 2 per board")
    s.balloon(5, (BW, RAIL + BH + 20), (s.X(BW) + 40, s.Y(RAIL + BH + 20) + 26), "V-score line", "Runs edge to edge in a straight line")
    s.balloon(6, (35, RAIL + 22), (s.X(35), s.Y(RAIL + 22)), "Board", "Your design: one of four in the panel")
    key_below(s, s.Y(PH + 20) + 60 * s.f, notes=("Drawn to scale. Dimensions in mm.",))
    s.save(out(1, "panel-anatomy"))


def fiducial_detail():
    # Close-up of a board fiducial near the panel edge. Panel edge at x = 0.
    s = Sheet(760, 700,
              "Fiducial detail: size and distance from the panel edge",
              "Enlarged and drawn to scale. A round copper dot 1 mm across sits in a 2 mm circular "
              "opening in the solder mask, leaving a 0.5 mm ring of bare board. The outer 3 mm of the panel edge "
              "is shaded as the zone that machine clamps cover. The center of the copper dot is 5 mm in from the "
              "panel edge, so the clamps cannot hide it.",
              scale=40, ox=60, oy=90)
    W, H = 15, 10
    s.rect(0, 0, W, H, "mask-lt")
    s.rect(0, 0, 3, H, "zone")
    s.line(3, 0, 3, H, "zone-s")
    s.line(0, 0, 0, H, "edge")
    cx, cy = 5.0, 5
    s.circle(cx, cy, 1.0, "bare")
    s.circle(cx, cy, 0.5, "copper")
    s.dim_h(cx - 0.5, cx + 0.5, cy - 1.9, "Ø 1.0", ext_from=cy)
    s.dim_h(cx - 1.0, cx + 1.0, cy + 2.0, "Ø 2.0", ext_from=cy, text_above=False)
    s.dim_h(0, cx, cy - 3.4, "5.0 to the center", ext_from=cy)
    s.balloon(1, (cx, cy), (s.X(cx) + 200, s.Y(cy)), "Copper dot", "Round or square, 1 mm across; no label needed")
    s.balloon(2, (cx + 0.45, cy + 0.8), (s.X(cx) + 200, s.Y(cy) + 40), "Bare board ring", "Mask opening 2 mm across")
    s.balloon(3, (11, 7.5), (s.X(11) + 40, s.Y(H) + 40), "Solder mask over FR4")
    s.balloon(4, (1.5, 8.5), (s.X(1.5) + 70, s.Y(H) + 40), "Clamp zone", "Outer ~3 mm of the panel edge")
    s.rect(0, 0, W, H, "mask-lt-s")
    key_below(s, s.Y(H) + 100 * s.f, notes=("Drawn to scale. Panel edge on the left. Dimensions in mm.",))
    s.save(out(2, "fiducial-detail"))


def vscore_clearance():
    # Top view across a V-score line at x = 0; board A on the left, board B on the right.
    s = Sheet(800, 860,
              "Clearances either side of a V-score line",
              "Enlarged and drawn to scale. A vertical dashed V-score line separates two boards. On the "
              "right-hand board, shaded bands show copper kept 0.5 mm back from the line, ordinary components "
              "kept 1.3 mm back, and ceramic capacitors kept 5 mm back. A resistor sits 1.5 mm from the line "
              "and a ceramic capacitor 5.5 mm from it, both turned parallel to the line. On the left-hand "
              "board, a ceramic capacitor turned across the line and only 1 mm from it is marked as wrong.",
              scale=30, ox=290, oy=150)
    H = 14
    s.rect(-6, 0, 6, H, "mask-lt")
    s.rect(0, 0, 12, H, "mask-lt")
    s.rect(0, 0, 0.5, H, "zone")
    s.rect(0.5, 0, 0.8, H, "keep")
    s.line(5, 0, 5, H, "keep-s")
    s.line(1.3, 0, 1.3, H, "keep-s")
    s.line(0, -0.6, 0, H + 0.6, "score")
    # trace ending at 0.5 mm
    s.rect(0.5, 2.6, 11.5, 0.25, "mask-on-cu")
    # resistor 0603 (1.6 x 0.8), parallel to line, 1.5 mm away
    def chip(x, y, w, h, vertical, cap=False):
        # Resistor: black body, tinned ends. Ceramic capacitor (MLCC): tan ceramic body, metal end caps.
        body, term, t = ("capbody", "capterm", 0.25) if cap else ("part", "term", 0.2)
        if vertical:
            s.rect(x, y, h, w, body, rx=0.08 if cap else 0)
            s.rect(x, y, h, w * t, term, rx=0.08 if cap else 0)
            s.rect(x, y + w * (1 - t), h, w * t, term, rx=0.08 if cap else 0)
        else:
            s.rect(x, y, w, h, body, rx=0.08 if cap else 0)
            s.rect(x, y, w * t, h, term, rx=0.08 if cap else 0)
            s.rect(x + w * (1 - t), y, w * t, h, term, rx=0.08 if cap else 0)
    chip(1.5, 5.0, 1.6, 0.8, vertical=True)
    chip(5.5, 9.0, 2.0, 1.25, vertical=True, cap=True)     # MLCC 0805, parallel, 5.5 mm away
    chip(-3.0, 9.4, 2.0, 1.25, vertical=False, cap=True)   # MLCC across the line, 1 mm away: wrong
    s.text("✗", -2.0, 12.6, size=22, cls="ink", anchor="middle", weight="700")
    s.text("✓", 6.1, 12.8, size=22, cls="ink", anchor="middle", weight="700")
    s.dim_h(0, 0.5, -1.0, "0.5", ext_from=0, text_side="left")
    s.dim_h(0, 1.3, -2.2, "1.3", ext_from=0)
    s.dim_h(0, 5.0, -3.4, "5.0", ext_from=0)
    s.rect(-6, 0, 18, H, "mask-lt-s")
    s.text("Board A", -3, 1.0, size=12, cls="silk", anchor="middle")
    s.text("Board B", 9, 1.0, size=12, cls="silk", anchor="middle")
    s.balloon(1, (0, 7), (s.X(0) - 70, s.Y(7) - 40), "V-score line")
    s.balloon(2, (0.25, 12.5), (s.X(0.25) + 40, s.Y(H) + 34), "Copper keep-out", "0.5 mm minimum, 1.0 mm preferred")
    s.balloon(3, (2.3, 5.8), (s.X(2.3) + 60, s.Y(5.8) - 50), "Resistor, 1.3 mm or more", "Long axis parallel to the line")
    s.balloon(4, (6.1, 10), (s.X(6.1) + 80, s.Y(10)), "Ceramic capacitor, 5 mm or more", "Long axis parallel to the line")
    s.balloon(5, (-2.0, 10), (s.X(-2.0) - 60, s.Y(H) + 34), "Avoid", "Capacitor across the line and too close")
    key_below(s, s.Y(H) + 100 * s.f, notes=("Drawn to scale. Dimensions in mm from the score line.",
                                             "Values from PCB-DFM-002, PCB-DFA-016 and PCB-DFA-017."))
    s.save(out(3, "vscore-clearance"))


def _path(s, pts_mm, cls, close=True):
    """Polygon from (x, y) points in mm."""
    import drawsvg as dw
    d = dw.Path(class_=cls)
    x, y = pts_mm[0]
    d.M(s.X(x), s.Y(y))
    for x, y in pts_mm[1:]:
        d.L(s.X(x), s.Y(y))
    if close:
        d.Z()
    s.d.append(d)


def recessed_tab():
    # D4: why a recess at each tab keeps the broken tab stub inside the board outline.
    # Values from the Worthington Assembly article "Recessing Your PCB Edge for Perforated Tabs":
    # 0.5 mm holes pulled back 0.1 mm from the edge. Tab width, slot width and recess depth are examples.
    # Redrawn 2026-11-05: frame, tab and board are all board material, and every routed slot is cut by a 2 mm bit,
    # so its ends and inside corners have a 1 mm radius.
    import drawsvg as dw
    K = 20
    s = Sheet(980, 1030,
              "Recessing the board edge at a breakaway tab",
              "Four close-ups of a board edge at a breakaway tab, drawn to scale. Top row, in the panel: a 2 mm "
              "routed slot, cut with a 2 mm router bit so its ends are round, separates the board from the panel "
              "frame, and a 5 mm tab bridges it. A row of 0.5 mm holes (mouse bites) runs along the board edge where "
              "the tab joins. Left column, without a recess: the holes sit on the straight board edge. Right column, "
              "with a recess: the router cuts 1 mm deeper into the board either side of the tab, so the holes sit 1 mm "
              "inside the board outline. Bottom row, after breaking: without a recess, a rough stub sticks out past "
              "the board outline; with a recess, the stub stays inside it, so the board fits its enclosure without "
              "filing.",
              scale=K, ox=140, oy=130)
    W, H, SLOT0, SLOT1, TAB0, TAB1 = 18, 11, 3, 5, 6.5, 11.5
    REC0, REC1, DEPTH = 4.5, 13.5, 1.0          # the bit cuts 2 mm wide pockets either side of the tab
    COLS, ROWS = (0, 22), (0, 10.5)
    s.text("Without a recess", s.X(W / 2), s.Y(-3.4), size=14, cls="ink", anchor="middle", weight="600", px=True)
    s.text("With a recess", s.X(COLS[1] + W / 2), s.Y(-3.4), size=14, cls="ink", anchor="middle", weight="600", px=True)
    # Row headings turned to read bottom to top, so the two columns of close-ups can use the full width (DRW1).
    for label, y in (("In the panel", H / 2), ("After breaking", ROWS[1] + (SLOT1 - 1.2 + H) / 2)):
        x0, y0 = s.X(-4.6), s.Y(y)
        s.d.append(dw.Text(label, s.fs(14), x0, y0, text_anchor="middle", class_="ink", font_weight="600",
                           transform=f"rotate(-90 {x0} {y0})"))
    XS = [TAB0 + 0.4 + 0.75 * k for k in range(int((TAB1 - TAB0 - 0.8) / 0.75 + 1e-6) + 1)]

    def zigzag(c, y, amp=0.12):
        pts, x, k = [], c + TAB0, 0
        while x < c + TAB1 - 1e-6:
            pts.append((x, y + (amp if k % 2 else -amp)))
            x += 0.25; k += 1
        return pts + [(c + TAB1, y)]

    for c, recess in zip(COLS, (False, True)):
        edge = SLOT1 + (DEPTH if recess else 0)
        hy = edge + 0.35
        # --- in the panel
        g = s.clipped([s.R(c, 0, W, H, "bg")])
        g.append(s.R(c, 0, W, H, "mask-on-fr4"))
        g.append(s.R(c - 2, SLOT0, TAB0 + 2, 2, "bg", rx=1))
        g.append(s.R(c + TAB1, SLOT0, W - TAB1 + 2, 2, "bg", rx=1))
        if recess:
            g.append(s.R(c + REC0, SLOT0, TAB0 - REC0, 2 + DEPTH, "bg", rx=1))
            g.append(s.R(c + TAB1, SLOT0, REC1 - TAB1, 2 + DEPTH, "bg", rx=1))
        g.append(s.R(c + 1, edge + 1.1, W - 2, 0.3, "mask-on-cu"))
        for x in XS:
            g.append(s.C(c + x, hy, 0.25, "drill"))
        s.d.append(g)
        s.line(c, SLOT1, c + W, SLOT1, "zone-s")
        # --- after breaking
        r = ROWS[1]
        stub_top = edge - 0.4
        g = s.clipped([s.R(c, r + SLOT1 - 1.2, W, H - SLOT1 + 1.2, "bg")])
        g.append(s.R(c, r + SLOT1, W, H - SLOT1, "mask-on-fr4"))
        if recess:
            g.append(s.R(c + REC0, r + SLOT1 - 1, TAB0 - REC0, 1 + DEPTH, "bg", rx=1))
            g.append(s.R(c + TAB1, r + SLOT1 - 1, REC1 - TAB1, 1 + DEPTH, "bg", rx=1))
            pts = [(c + TAB0, r + SLOT1 - 1)] + [(x, r + y) for x, y in zigzag(0, stub_top)] + [(c + TAB1, r + SLOT1 - 1)]
            pts = [(c + TAB0, r + SLOT1 - 1)] + [(c + x, r + y) for x, y in zigzag(0, stub_top)] + [(c + TAB1, r + SLOT1 - 1)]
            p = dw.Path(class_="bg"); p.M(s.X(pts[0][0]), s.Y(pts[0][1]))
            for x, y in pts[1:]:
                p.L(s.X(x), s.Y(y))
            p.Z(); g.append(p)
        else:
            pts = [(c + TAB0, r + hy)] + [(c + x, r + y) for x, y in zigzag(0, stub_top)] + [(c + TAB1, r + hy)]
            p = dw.Path(class_="mask-on-fr4"); p.M(s.X(pts[0][0]), s.Y(pts[0][1]))
            for x, y in pts[1:]:
                p.L(s.X(x), s.Y(y))
            p.Z(); g.append(p)
        for x in XS:
            g.append(s.C(c + x, r + hy, 0.25, "bg"))
        g.append(s.R(c + 1, r + edge + 1.1, W - 2, 0.3, "mask-on-cu"))
        s.d.append(g)
        s.line(c - 0.5, r + SLOT1, c + W + 0.5, r + SLOT1, "zone-s")
        s.text("✗" if not recess else "✓", s.X(c + W - 1.5), s.Y(r + 3.6), size=24, cls="ink",
               anchor="middle", weight="700", px=True)
    s.dim_h(COLS[1] + TAB0, COLS[1] + TAB1, -1.0, "5 mm tab (example)", ext_from=SLOT0)
    s.dim_v(SLOT1, SLOT1 + DEPTH, COLS[1] - 1.0, "1 mm", ext_from=COLS[1] + REC0, text_left=True)
    s.dim_v(SLOT0, SLOT1, COLS[0] - 0.4, "2 mm", text_left=True)
    s.balloon(1, (1.2, 1.5), (s.X(1.2), s.Y(-1.4)), "Panel frame or rail")
    s.balloon(2, (4.2, 4), (s.X(4.2), s.Y(-1.4)), "Routed slot", "2 mm router bit: round ends, 1 mm radius")
    s.balloon(3, (TAB0 + 1, 4), (s.X(TAB1 + 3), s.Y(-1.4)), "Breakaway tab", "Example 5 mm wide")
    s.balloon(4, (COLS[1] + TAB0 + 0.4, SLOT1 + DEPTH + 0.35), (s.X(COLS[1] + 3), s.Y(SLOT1 + DEPTH + 3)),
              "Mouse bites", "0.5 mm holes, 0.1 mm inside the edge")
    s.balloon(5, (COLS[1] + REC1 - 1, SLOT1 + 0.9), (s.X(COLS[1] + 16), s.Y(SLOT1 + 3.2)), "Recess in the board outline",
              "Cut by the same 2 mm bit")
    s.balloon(6, (TAB1 - 0.5, ROWS[1] + SLOT1 - 0.2), (s.X(TAB1 + 2.5), s.Y(ROWS[1] + 2.2)),
              "Stub sticks out past the outline", "Must be filed or sanded off")
    s.balloon(7, (COLS[1] + TAB1 - 0.5, ROWS[1] + SLOT1 + 0.8), (s.X(COLS[1] + TAB1 + 2.5), s.Y(ROWS[1] + 2.2)),
              "Stub stays inside the recess", "Board fits its enclosure as is")
    s.balloon(8, (COLS[0] + 15, ROWS[1] + SLOT1 + 1.25), (s.X(COLS[0] + 16), s.Y(ROWS[1] + H + 1.6)),
              "Nearest trace", "1.1 mm or more from the edge (see D5)")
    s.balloon(9, (COLS[0] + 17.5, ROWS[1] + SLOT1), (s.X(COLS[0] + 19.7), s.Y(ROWS[1] + H + 1.6)),
              "Board outline", "Dashed line")
    s.balloon(10, (COLS[1] + REC0 + 0.2, SLOT1 + 0.6), (s.X(COLS[1] + 3), s.Y(SLOT1 + DEPTH + 3)), "Recess depth",
              "Example 1 mm; agree it with your fab and assembler")
    key_below(s, s.Y(ROWS[1] + H + 1.6) + 70 * s.f, split=5,
              notes=("Drawn to scale. Tab, slot and recess sizes are examples.",))
    s.save(out(4, "recessed-tab"))


def mouse_bite_clearance():
    # D5: mouse-bite hole clearances, after the figure in the Worthington Assembly article.
    s = Sheet(980, 520,
              "Mouse-bite clearances at a breakaway tab",
              "A close-up of a board edge at a tab, enlarged and drawn to scale. Non-plated holes "
              "0.5 mm across run along the edge, each pulled back 0.1 mm from the edge. Traces, pads and plated "
              "holes are kept at least 0.5 mm from the holes, which puts them at least 1.1 mm from the board edge.",
              scale=100, ox=90, oy=90)
    W, H, EDGE = 4.0, 3.2, 3.2           # board occupies x 0..EDGE; edge on the right
    s.rect(0, 0, W, H, "mask-lt")                 # board, and the tab continuing past the edge
    s.line(EDGE, -0.15, EDGE, H + 0.15, "zone-s")
    cx = EDGE - 0.1 - 0.25
    for cy in (0.6, 1.35, 2.1, 2.85):
        s.circle(cx, cy, 0.25, "drill")
        s.circle(cx, cy, 0.25, "thin")
    tx = EDGE - 1.1 - 0.25
    s.rect(tx, 0, 0.25, H, "mask-on-cu")
    s.dim_h(cx - 0.25, cx + 0.25, -0.35, "Ø 0.5", ext_from=0.6)
    s.dim_h(cx + 0.25, EDGE, -0.35, "0.1", ext_from=0.6)
    s.dim_h(tx + 0.25, cx - 0.25, H + 0.35, "0.5", ext_from=2.85, text_above=False)
    s.dim_h(tx + 0.25, EDGE, H + 0.75, "1.1 mm minimum to the edge", ext_from=H, text_above=False)
    s.balloon(1, (cx, 1.35), (s.X(cx) + 150, s.Y(1.35) - 40), "Mouse-bite hole", "Non-plated, 0.5 mm across")
    s.balloon(2, (EDGE, 2.4), (s.X(EDGE) + 150, s.Y(2.4) + 30), "Board edge", "Holes pulled back 0.1 mm")
    s.balloon(3, (tx + 0.12, 1.0), (s.X(tx) - 90, s.Y(1.0) - 40), "Nearest trace, pad or plated hole",
              "At least 0.5 mm from the holes")
    s.key(640, 110, width=320)
    s.note("Drawn to scale. Dimensions in mm.", 640, 430)
    s.note("From a published assembler guideline.", 640, 448)
    s.save(out(5, "mouse-bite-clearance"))


def overhang_vscore():
    # D24 (I11, PCB-DFA-010), redrawn 2026-11-05 in the board color key and D25's style.
    # Left: a coax connector on board A hangs 7 mm past a V-score, over board B; bending B to snap the score lifts B
    # into the connector. Right: A's edge is routed and held by tabs, with a routed relief cut-out leaving 10 mm.
    import math
    # Redrawn for print (DRW1, Q177 option A): the views side by side, the key in two columns below them.
    s = Sheet(1040, 1030,
              "A connector overhanging a breakaway edge",
              "Drawn to scale, plan views with side views below. Left, marked wrong: boards A and B meet at a V-score "
              "line, and a coax connector on board A hangs 7 mm past it, over board B. In the side view, board B is "
              "bent up to snap the score and meets the underside of the connector, marked in red, before the score "
              "can break. Right, marked right: board A's edge is routed and held by two tabs with mouse bites, and a "
              "routed relief cut-out in the panel leaves 10 mm from board A's edge, so nothing is in the way. The "
              "connector's silkscreen outline includes the part past the edge.",
              scale=13, ox=60, oy=130)
    f = s.f
    AW, H, R, SV, T2 = 14, 26, 38, 37, 0.8
    CY0, CY1, BY0, BY1 = 9.8, 16.2, 10.7, 15.3

    def board_a_details(dx, add):
        for t in ([(dx + 5.3, 12.0), (dx + 3.0, 12.0), (dx + 1.5, 10.5), (dx + 1.5, -1)],
                  [(dx + 5.3, 14.0), (dx + 3.0, 14.0), (dx + 1.5, 15.5), (dx + 1.5, 27)]):
            add(s.PL(t, "s-mask-on-cu", 0.3))
        for y in (11.5, 13.5):
            add(s.R(dx + 4.6, y, 1.4, 1.0, "fr4-exposed", rx=0.1))
            add(s.R(dx + 4.675, y + 0.075, 1.25, 0.85, "cu-exposed", rx=0.08))
        for x in (3.4, 4.9):
            add(s.R(dx + x, 4.0, 0.9, 1.0, "cu-exposed", rx=0.1))
        for x in (3.4, 4.9):
            add(s.R(dx + x, 21.0, 0.9, 1.0, "cu-exposed", rx=0.1))

    def connector_top(dx):
        s.d.append(s.PL([(dx + 6.6, CY0 - 0.4), (dx + 21.4, CY0 - 0.4), (dx + 21.4, CY1 + 0.4),
                         (dx + 6.6, CY1 + 0.4), (dx + 6.6, CY0 - 0.4)], "s-silkscreen", 0.15))
        s.rect(dx + 7, CY0, 7, CY1 - CY0, "foil")
        s.rect(dx + 14, BY0, 7, BY1 - BY0, "foil", rx=0.3)
        for k in range(6):
            s.line(dx + 15.2 + k, BY0, dx + 15.2 + k, BY1, "thin")
        s.text("J1", s.X(dx + 10.5), s.Y(CY0 - 1.0), size=10, cls="silk", anchor="middle", px=True)
        s.text("C1", s.X(dx + 4.3), s.Y(3.4), size=10, cls="silk", anchor="middle", px=True)
        s.text("C2", s.X(dx + 4.3), s.Y(20.5), size=10, cls="silk", anchor="middle", px=True)

    def connector_side(dx):
        s.rect(dx + 7, SV - 6, 7, 6, "foil")
        s.rect(dx + 14, SV - 5.3, 7, 4.3, "foil", rx=0.3)
        for k in range(6):
            s.line(dx + 15.2 + k, SV - 5.3, dx + 15.2 + k, SV - 1.0, "thin")

    # ---------- left: V-scored, overhang across the score (wrong)
    g = s.clipped([s.R(0, 0, 30, H, "bg")])
    g.append(s.R(0, 0, 30, H, "mask-on-fr4"))
    board_a_details(0, g.append)
    for x, y in ((22, 4), (24, 21)):
        g.append(s.R(x, y, 0.9, 1.0, "cu-exposed", rx=0.1)); g.append(s.R(x + 1.5, y, 0.9, 1.0, "cu-exposed", rx=0.1))
    g.append(s.PL([(25.5, 4.5), (28, 4.5), (31, 1.5)], "s-mask-on-cu", 0.3))
    s.d.append(g)
    s.line(AW, -1.2, AW, H + 1.2, "score")
    connector_top(0)
    s.text("Board A", s.X(4.6), s.Y(H - 1.0), size=11, cls="silk", anchor="middle", px=True)
    s.text("Board B", s.X(25.4), s.Y(H - 1.0), size=11, cls="silk", anchor="middle", px=True)
    s.text("✗ Overhang across a V-score", s.X(15), s.Y(-6.0), size=15, cls="ink", anchor="middle", weight="600", px=True)
    s.dim_h(AW, AW + 7, -1.6, "7 mm overhang", ext_from=BY0)
    # side view: board B bent up about the score until it meets the connector
    def rot(pts, a):
        return [(x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)) for x, y in pts]
    def solve(f):
        lo, hi = 0.0, 0.6
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(lo) * f(mid) > 0 else (lo, mid)
        return (lo + hi) / 2
    def gap(a):
        t = (7 + T2 * math.sin(a)) / math.cos(a)
        return t * math.sin(a) + T2 * math.cos(a) - (T2 + 1.0)
    up = solve(gap)
    S = lambda pts: [(AW + x, SV + T2 - y) for x, y in pts]
    _path(s, S([(-14, T2), (-0.3, T2), (0, 0.3), (0, -0.3), (-0.3, -T2), (-14, -T2)]), "mask-on-fr4")
    _path(s, S(rot([(0, 0.3), (0.3, T2), (16, T2), (16, -T2), (0.3, -T2), (0, -0.3)], up)), "mask-on-fr4")
    connector_side(0)
    t = (7 + T2 * math.sin(up)) / math.cos(up)
    hit = S(rot([(t, T2)], up))[0]
    s.circle(hit[0], hit[1], 0.5, "contact")
    s.text("Side view: board B bent to snap the score", s.X(0), s.Y(SV + 4.2), size=12, cls="muted", px=True)

    # ---------- right: routed edge with tabs and a relief cut-out (right)
    g = s.clipped([s.R(R, 0, 34, H, "bg")])
    g.append(s.R(R, 0, 34, H, "mask-on-fr4"))
    board_a_details(R, g.append)
    x_slot = R + AW + 1
    for y0, y1 in ((-2, 1), (6, 20), (25, 28)):
        g.append(s.PL([(x_slot, y0), (x_slot, y1)], "s-offboard", 2))
    g.append(s.R(R + AW, 8.1, 10, 9.8, "offboard", rx=1))
    for y in (2.4, 3.15, 3.9, 4.65, 21.4, 22.15, 22.9, 23.65):
        g.append(s.C(R + AW - 0.35, y, 0.25, "drill"))
    for x, y in ((R + 30.3, 4), (R + 30.3, 21)):
        g.append(s.R(x, y, 0.9, 1.0, "cu-exposed", rx=0.1)); g.append(s.R(x + 1.5, y, 0.9, 1.0, "cu-exposed", rx=0.1))
    s.d.append(g)
    s.line(R + 28, -1.2, R + 28, H + 1.2, "score")
    connector_top(R)
    s.text("Board A", s.X(R + 4.6), s.Y(H - 1.0), size=11, cls="silk", anchor="middle", px=True)
    s.text("Board B", s.X(R + 31), s.Y(H - 1.0), size=11, cls="silk", anchor="middle", px=True)
    s.text("✓ Routed edge with a relief cut-out", s.X(R + 17), s.Y(-6.0), size=15, cls="ink", anchor="middle",
           weight="600", px=True)
    s.dim_h(R + AW, R + AW + 10, H + 1.8, "10 mm clearance", ext_from=17.9, text_above=False)
    s.rect(R, SV, AW, 1.6, "mask-on-fr4")
    s.rect(R + AW + 10, SV, 4, 1.6, "mask-on-fr4")
    s.rect(R + 28, SV, 6, 1.6, "mask-on-fr4")
    s.line(R + 28, SV - 0.4, R + 28, SV + 2.0, "score")
    connector_side(R)
    s.text("Side view, through the cut-out:", s.X(R), s.Y(SV + 4.2), size=12, cls="muted", px=True)
    s.text("nothing under the connector", s.X(R), s.Y(SV + 4.2) + 22 * f, size=12, cls="muted", px=True)

    s.balloon(1, (AW, 23.5), (s.X(AW) - 60, s.Y(H) + 34 * f), "V-score line")
    s.balloon(2, (19, BY1), (s.X(19) + 30, s.Y(H) + 34 * f), "Connector hangs 7 mm past board A", "Over board B")
    s.balloon(3, hit, (s.X(hit[0]) + 70, s.Y(SV) - 120), "Board B meets the connector", "The score can't be snapped")
    s.balloon(4, (R + 22.5, 9.0), (s.X(R + 22.5), s.Y(-1.4)), "Routed relief cut-out",
              "About 10 mm from the edge for a 7 mm overhang")
    s.balloon(5, (R + AW - 0.35, 3.15), (s.X(R + AW), s.Y(-1.4)), "Edge routed and held by tabs",
              "Mouse bites just inside the edge")
    s.balloon(6, (R + 21.4, CY0 - 0.4), (s.X(R + 21.4), s.Y(-1.4)), "Silkscreen outline of the whole part",
              "Including the overhang (PCB-DFA-036)")
    ky = s.Y(SV + 4.2) + 64 * f
    y1 = s.key(60, ky, width=430, only=(1, 2, 3))
    y2 = s.key(560, ky, width=430, title="", only=(4, 5, 6))
    y = max(y1, y2) + 34 * f
    s.note("Drawn to scale. Dimensions in mm. Values from PCB-DFA-010.", 60, y)
    s.save(out(24, "overhang-vscore"))


def overhang_facing():
    # D25 (I11, PCB-DFA-010). Two overhangs facing each other across a V-score, side views. A connector on board B's
    # top hangs over board A; a connector on board A's underside hangs under board B. Bending B up drops its own
    # connector onto A; bending it down lands B on A's connector. Each blocks one way, so the score can't snap.
    import math
    s = Sheet(900, 900, "Two overhangs facing each other across a V-score",
              "Drawn to scale, three side views of two boards joined by a V-score. A connector on the top of board B "
              "hangs 7 mm past the score, over board A. A connector on the underside of board A hangs 7 mm past the "
              "score, under board B. Top left: as placed, with the key beside it. Below left: board B bent up to snap the "
              "score; its own connector comes down onto board A, marked in red. Below right: board B bent down; board B comes down onto board A's "
              "connector, marked in red. Each overhang blocks one direction, so the score can't be snapped either way.",
              scale=12, ox=60, oy=80)
    # Laid out two by two for print (DRW1, Q177 option A): as placed at the top left, the key beside it, and the
    # two bent views below.
    T2, BY = 0.8, 11.0
    VX = [14, 14, 47]
    VY = [BY, BY + 27, BY + 27]
    def rect(x, y, w, h):
        return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    def rot(pts, a):
        return [(x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)) for x, y in pts]
    def solve(f):
        lo, hi = 0.0, 0.6
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(lo) * f(mid) > 0 else (lo, mid)
        return (lo + hi) / 2
    up = solve(lambda a: -7 * math.sin(a) + 1.8 * math.cos(a) - T2)          # B's barrel corner reaches A's top
    def down_gap(a):                                                           # B's underside reaches A's barrel
        t = (7 + T2 * math.sin(a)) / math.cos(a)
        return -t * math.sin(a) - T2 * math.cos(a) + 1.8
    down = solve(down_gap)
    A = [(-14, T2), (-0.3, T2), (0, 0.3), (0, -0.3), (-0.3, -T2), (-14, -T2)]
    B = [(0, 0.3), (0.3, T2), (14, T2), (14, -T2), (0.3, -T2), (0, -0.3)]
    C2_BODY, C2_BARREL = rect(0, T2, 7, 6), rect(-7, T2 + 1.0, 7, 4.3)          # on B's top
    C1_BODY, C1_BARREL = rect(-7, -T2 - 6, 7, 6), rect(0, -T2 - 5.3, 7, 4.3)    # under A
    def S(k, pts):
        return [(VX[k] + x, VY[k] - y) for x, y in pts]
    def threads(k, x0, y0, y1, a=0.0):
        for j in range(6):
            (xa, ya), (xb, yb) = S(k, rot([(x0 + 1.2 + j, y0), (x0 + 1.2 + j, y1)], a))
            s.line(xa, ya, xb, yb, "thin")
    contacts = []
    for k, a in enumerate((0.0, up, -down)):
        _path(s, S(k, C1_BODY), "foil"); _path(s, S(k, C1_BARREL), "foil", ); threads(k, 0, -6.1, -1.8)
        _path(s, S(k, A), "mask-on-fr4")
        _path(s, S(k, rot(B, a)), "mask-on-fr4")
        _path(s, S(k, rot(C2_BODY, a)), "foil"); _path(s, S(k, rot(C2_BARREL, a)), "foil"); threads(k, -7, 1.8, 6.1, a)
    hit_up = S(1, rot([(-7, 1.8)], up))[0]
    t = (7 + T2 * math.sin(down)) / math.cos(down)
    hit_down = S(2, rot([(t, -T2)], -down))[0]
    for x, y in (hit_up, hit_down):
        s.circle(x, y, 0.55, "contact")
    s.text("Board A", s.X(VX[0] - 9), s.Y(BY) + 4, size=11, cls="silk", anchor="middle", px=True)
    s.text("Board B", s.X(VX[0] + 10.5), s.Y(BY) + 4, size=11, cls="silk", anchor="middle", px=True)
    for k, title in enumerate(["✗ Overhangs facing each other", "Bend board B up: blocked", "Bend board B down: blocked"]):
        s.text(title, s.X(VX[k]), s.Y(VY[k] - 12.2), size=14, anchor="middle", weight="600", px=True)
    s.dim_h(VX[0] - 7, VX[0], BY - 7.6, "7 mm", ext_from=BY - 6.1)
    s.dim_h(VX[0], VX[0] + 7, BY + 7.6, "7 mm", ext_from=BY + 6.1, text_above=False)
    s.balloon(1, (VX[0] - 3.5, BY - 3.95), (s.X(VX[0] - 14), s.Y(BY - 3.95)), "Connector on board B's top", "Hangs 7 mm over board A")
    s.balloon(2, (VX[0] + 3.5, BY + 3.95), (s.X(VX[0] + 13), s.Y(BY + 3.95)), "Connector on board A's underside",
              "Hangs 7 mm under board B")
    s.balloon(3, hit_up, (s.X(VX[1] - 12), s.Y(VY[1] - 8.0)), "Board B's connector lands on board A")
    s.balloon(4, hit_down, (s.X(VX[2] + 12), s.Y(VY[2] + 9.5)), "Board B lands on board A's connector")
    f = s.f
    s.key(s.X(VX[2] - 14), s.Y(VY[0] - 9), width=s.X(VX[2] + 15) - s.X(VX[2] - 14))
    y = s.Y(VY[2] + 9.5) + 30 * f
    for t in ("Drawn to scale. Dimensions in mm.",
              "Each overhang blocks one way of bending, so together they block both.",
              "Fix: keep overhangs off breakaway edges, or route the edge and leave a relief cut-out (D24).",
              "Example values from PCB-DFA-010."):
        y += 22 * f
        s.note(t, s.X(0), y)
    s.height = y + 18 * f
    s.save(out(25, "overhang-facing"))



def _plan_board(s, x, y, w, h, pads=()):
    """A small board in plan view, in the board color key: mask over FR4, with a few exposed pads."""
    s.rect(x, y, w, h, "mask-on-fr4")
    for px, py, pw, ph in pads:
        s.rect(x + px, y + py, pw, ph, "cu-exposed")


def _fiducial(s, x, y):
    s.circle(x, y, 1.0, "fr4-exposed")     # 2 mm mask opening
    s.circle(x, y, 0.5, "cu-exposed")      # 1 mm copper dot


def small_board_panel():
    # D29 (I7, PCB-DFA-002): a 15 x 10 mm board alone drops into the gap between two machines' conveyors;
    # the same board in a 60 x 50 mm panel spans it. Gap from PCB-DFA-002.
    import drawsvg as dw
    s = Sheet(900, 780, "A small board on its own, and the same board in a panel",
              "Drawn to scale, plan view of the end of one machine's conveyor and the start of the next, about 50 mm "
              "apart, twice. Top, marked wrong: a 15 by 10 mm board on its own has just left the first conveyor and "
              "has nothing under it; it is far shorter than the gap. Bottom, marked right: the same board in a panel "
              "of 24, 120 by 50 mm with 10 mm rails, rests on both conveyors at once; it is longer than twice the gap, so it "
              "never hangs more than halfway off a conveyor and tips.",
              scale=4.5, ox=330, oy=100)
    CHIP = [(3, 3, 1.6, 1.0), (3, 6, 1.6, 1.0), (9, 4, 1.0, 2.5)]
    def belts(y0, y1):
        for x0, x1 in ((-60, 0), (50, 110)):
            s.rect(x0, y0 - 1, x1 - x0, 3, "foil")
            s.rect(x0, y1 - 2, x1 - x0, 3, "foil")
    # top: a board on its own
    belts(0, 10)
    _plan_board(s, 2, 0, 15, 10, CHIP)
    s.text("Machine A", s.X(-30), s.Y(-3), size=12, cls="muted", anchor="middle", px=True)
    s.text("Machine B", s.X(80), s.Y(-3), size=12, cls="muted", anchor="middle", px=True)
    s.text("✗ A 15 × 10 mm board on its own", s.X(25), s.Y(-8), size=14, anchor="middle", weight="600", px=True)
    s.dim_h(0, 50, 16, "About 50 mm between machines", ext_from=11, text_above=False)
    # bottom: the same board in a panel
    D = 40
    belts(D, D + 50)
    s.rect(-35, D, 120, 50, "mask-on-fr4")
    for i in range(8):
        for j in range(3):
            for px, py, pw, ph in CHIP:
                s.rect(-35 + 15 * i + px, D + 10 + 10 * j + py, pw, ph, "cu-exposed")
    for y in (10, 20, 30, 40):
        s.line(-37, D + y, 87, D + y, "score")
    for x in (-20, -5, 10, 25, 40, 55, 70):
        s.line(x, D + 8, x, D + 42, "score")
    for x, y in ((75, D + 5), (-25, D + 45), (75, D + 45)):
        _fiducial(s, x, y)
    s.text("✓ The same board in a 120 × 50 mm panel", s.X(25), s.Y(D - 7), size=14, anchor="middle",
           weight="600", px=True)
    s.dim_h(-35, 85, D + 56, "120 mm panel: more than twice the gap", ext_from=D + 51, text_above=False)
    s.d.append(dw.Line(s.X(-60), s.Y(-14), s.X(-40), s.Y(-14), class_="lead"))
    s._arrowhead(s.X(-40), s.Y(-14), 0)
    s.text("Direction of travel", s.X(-37), s.Y(-14) + 4, size=12, cls="muted", px=True)
    s.balloon(1, (-5, 2), (s.X(-5), s.Y(5.5)), "End of one machine's conveyor")
    s.balloon(2, (9.5, 5), (s.X(32), s.Y(5)), "15 mm board", "Nothing under it in the gap")
    s.balloon(3, (80, D + 25), (s.X(100), s.Y(D + 25)), "120 mm panel", "On both conveyors before it can tip")
    key_below(s, s.Y(D + 56) + 70 * s.f, x=60, split=2,
              notes=("Drawn to scale. Dimensions in mm. Gap between machines from PCB-DFA-002.",))
    s.save(out(29, "small-board-panel"))


def panel_sag():
    # D30 (I8, PCB-DFA-004): end-on views of a panel on the oven's pin rails. A 200 mm span sags in the middle;
    # a 100 mm span barely moves (sag goes with span^4). Sag exaggerated by the same factor in both views.
    s = Sheet(820, 620, "A long span between the rails sags; a short one stays flat",
              "Drawn to scale except for the sag, end-on views of a 1.6 mm panel resting on the oven's pin rails, which "
              "grip about 3 mm of each edge. Top, marked wrong: the panel is 200 mm across the rails and sags in the "
              "middle. Bottom, marked right: a panel 100 mm across sags one sixteenth as much. The sag is exaggerated by "
              "the same factor in both views.",
              scale=3, ox=90, oy=90)
    T = 1.6
    def view(y0, span, sag):
        for x0 in (-10, span - 3):
            s.rect(x0, y0 + T + 0.2, 13, 5, "foil")
        n = 40
        top = [(span * k / n, y0 + sag * 4 * (k / n) * (1 - k / n)) for k in range(n + 1)]
        _path(s, top + [(x, y + T) for x, y in reversed(top)], "mask-on-fr4")
        s.dim_h(0, span, y0 + T + 15, f"{span} mm across the rails", ext_from=y0 + T + 6, text_above=False)
    view(0, 200, 8)
    s.text("✗ 200 mm between the rails: sags in the middle", s.X(100), s.Y(-8), size=14, anchor="middle",
           weight="600", px=True)
    view(50, 100, 0.5)
    s.text("✓ 100 mm between the rails: stays flat", s.X(50), s.Y(42), size=14, anchor="middle",
           weight="600", px=True)
    s.balloon(1, (1.5, T + 1.0), (s.X(-15), s.Y(-6)), "Pin rail", "Grips about 3 mm of the edge")
    s.balloon(2, (60, 6.72 + T), (s.X(60), s.Y(25)), "Sag in the middle", "Parts shift; the panel can drop")
    key_below(s, 390, x=60, split=1,
              notes=("Drawn to scale except the sag, which is exaggerated by the same factor in both views.",
                     "Sag grows with the fourth power of the span: twice the span, sixteen times the sag.",
                     "1.6 mm panel. Values from PCB-DFA-004."))
    s.save(out(30, "panel-sag"))


def local_fiducials():
    # D31 (I9, PCB-DFA-008), redrawn 2026-11-05: a close-up of a 0.8 mm-pitch BGA as it looks on a real board, with a
    # local fiducial just outside two opposite corners. Inner balls fan out to dog-bone vias; the outer ring escapes
    # straight out. Traces are under the mask.
    s = Sheet(760, 820, "Local fiducials beside a BGA",
              "Drawn to scale, plan view of a 0.8 mm-pitch BGA with 144 balls on a board. Each inner ball connects by "
              "a short trace to a via between the balls; the outer ring of balls escapes with traces straight out. The "
              "BGA has a silkscreen outline, a pin-1 dot and its reference designator U1. A local fiducial, FID1 and "
              "FID2, sits just outside two opposite corners of the BGA. Each fiducial is a 1 mm copper dot in a 2 mm "
              "mask opening. The board's own fiducials are at its corners, outside this view.",
              scale=34, ox=60, oy=70)
    VW, VH, CX, CY, P = 18, 16, 9, 8, 0.8
    g = s.clipped([s.R(0, 0, VW, VH, "bg")])
    add = g.append
    add(s.R(0, 0, VW, VH, "mask-on-fr4"))
    pos = [(i, j, CX + (i - 5.5) * P, CY + (j - 5.5) * P) for i in range(12) for j in range(12)]
    for i, j, x, y in pos:
        if i in (0, 11) or j in (0, 11):
            dx, dy = (-1, 0) if i == 0 else (1, 0) if i == 11 else (0, -1) if j == 0 else (0, 1)
            add(s.PL([(x, y), (x + dx * 20, y + dy * 20)], "s-mask-on-cu", 0.1))
        else:
            add(s.PL([(x, y), (x + P / 2, y + P / 2)], "s-mask-on-cu", 0.1))
    for i, j, x, y in pos:
        if not (i in (0, 11) or j in (0, 11)):
            add(s.C(x + P / 2, y + P / 2, 0.225, "mask-on-cu"))
    for i, j, x, y in pos:
        add(s.C(x, y, 0.25, "fr4-exposed"))
        add(s.C(x, y, 0.2, "cu-exposed"))
    for i, j, x, y in pos:
        if not (i in (0, 11) or j in (0, 11)):
            add(s.C(x + P / 2, y + P / 2, 0.1, "drill"))
    add(s.PL([(CX - 5, CY - 5), (CX + 5, CY - 5), (CX + 5, CY + 5), (CX - 5, CY + 5), (CX - 5, CY - 5)], "s-silkscreen", 0.15))
    add(s.C(CX - 5.6, CY - 5.6, 0.2, "silkscreen"))
    for (x, y), name, tx, ty in (((CX - 6.7, CY - 6.7), "FID1", CX - 6.7, CY - 8.1), ((CX + 6.7, CY + 6.7), "FID2", CX + 6.7, CY + 5.0)):
        add(s.C(x, y, 1.0, "fr4-exposed"))
        add(s.C(x, y, 0.5, "cu-exposed"))
    s.d.append(g)
    s.text("U1", s.X(CX + 5.9), s.Y(CY - 5.4), size=14, cls="silk", weight="600", px=True)
    s.text("FID1", s.X(CX - 6.7), s.Y(CY - 5.05), size=12, cls="silk", anchor="middle", px=True)
    s.text("FID2", s.X(CX + 6.7), s.Y(CY + 5.45), size=12, cls="silk", anchor="middle", px=True)
    s.balloon(1, (CX - 6.7, CY - 6.7), (s.X(-0.6), s.Y(-1.0)), "Local fiducials, FID1 and FID2",
              "At two opposite corners of the BGA")
    s.balloon(2, (CX + 4.0, CY + 2.4), (s.X(VW) + 30, s.Y(CY + 2.4)), "Dog-bone vias", "Inner balls fan out, under the mask")
    s.balloon(3, (CX + 5, CY - 2), (s.X(VW) + 30, s.Y(CY - 2)), "Silkscreen outline", "With pin-1 dot and U1")
    key_below(s, s.Y(VH) + 50 * s.f, x=60, split=2,
              notes=("Drawn to scale. Dimensions in mm. 0.8 mm-pitch BGA, 12 × 12 balls.",
                     "Fiducials: 1 mm copper dot in a 2 mm mask opening.",
                     "The board's own fiducials sit at its corners, outside this view."))
    s.save(out(31, "local-fiducials"))


def outline_shapes():
    # D32 (I10, PCB-DFM-001): a 2 x 2 panel of rectangular boards V-scored edge to edge, beside round boards that
    # need routed slots and tabs with mouse bites.
    s = Sheet(800, 640, "A rectangular outline is V-scored; a curved one needs routing and tabs",
              "Drawn to scale, plan views of two 80 by 70 mm panels with 10 mm rails. Left, marked right: four "
              "rectangular boards separated by V-score lines that run straight across the whole panel. Right: four "
              "round boards, each cut out by a 2 mm routed slot with round ends, and held to the panel by four tabs "
              "with mouse bites just inside the board edge.",
              scale=3.8, ox=60, oy=110)
    PADS = [(6, 6, 2, 1.2), (6, 9, 2, 1.2), (14, 8, 4, 4), (28, 12, 1.2, 2)]
    # left: rectangular boards, V-scored
    s.rect(0, 0, 80, 70, "mask-on-fr4")
    for i in range(2):
        for j in range(2):
            for px, py, pw, ph in PADS:
                s.rect(40 * i + px, 10 + 25 * j + py, pw, ph, "cu-exposed")
    for y in (10, 35, 60):
        s.line(-3, y, 83, y, "score")
    s.line(40, -3, 40, 73, "score")
    R0 = 95
    s.rect(R0, 0, 80, 70, "mask-on-fr4")
    import math
    for cx, cy in ((R0 + 20, 22.5), (R0 + 60, 22.5), (R0 + 20, 47.5), (R0 + 60, 47.5)):
        half = (1.5 + 1.0) / 11                  # a 3 mm tab, plus the bit's 1 mm radius at each slot end
        for k in range(4):
            a0, a1 = k * math.pi / 2 + half, (k + 1) * math.pi / 2 - half
            pts = [(cx + 11 * math.cos(a0 + (a1 - a0) * t / 24), cy + 11 * math.sin(a0 + (a1 - a0) * t / 24)) for t in range(25)]
            s.d.append(s.PL(pts, "s-offboard", 2))
        for px, py, pw, ph in ((-4, -3, 2, 1.2), (-4, 0, 2, 1.2), (1, -2, 4, 4)):
            s.rect(cx + px, cy + py, pw, ph, "cu-exposed")
        for k in (-1.0, -0.33, 0.33, 1.0):
            for x, y in ((cx + 9.65, cy + k), (cx - 9.65, cy + k), (cx + k, cy - 9.65), (cx + k, cy + 9.65)):
                s.circle(x, y, 0.25, "drill")
    for x, y in ((65, 5), (15, 65), (65, 65)):
        _fiducial(s, x, y); _fiducial(s, R0 + x, y)
    s.text("✓ Straight edges: V-scored edge to edge", s.X(40), s.Y(-6), size=14, anchor="middle", weight="600", px=True)
    s.text("Curved outline: routed slots and tabs", s.X(R0 + 40), s.Y(-6), size=14, anchor="middle", weight="600", px=True)
    s.balloon(1, (40, 48), (s.X(40) + 60, s.Y(76)), "V-score line", "Runs straight across the whole panel", free=True)
    s.balloon(2, (R0 + 20 + 10.3, 22.5 + 4.5), (s.X(R0 + 40), s.Y(76)), "Routed slot", "2 mm bit: round ends at each tab")
    s.balloon(3, (R0 + 60, 22.5 - 11), (s.X(R0 + 80) + 20, s.Y(22.5 - 11)), "Tab with mouse bites", "Holds the board in")
    s.key(60, 430, width=360)
    s.legend(470, 442, [("mask-on-fr4", "Board"), ("cu-exposed", "Exposed copper"),
                        ("offboard", "Routed away"), ("drill", "Hole")])
    s.note("Drawn to scale. Dimensions in mm.", 470, 442 + 4 * 22 * s.f + 8 * s.f)
    s.height = 430 + (10 + 3 * 42) * s.f + 24 * s.f
    s.save(out(32, "outline-shapes"))


def enclosure_room():
    # D33 (I12, PCB-DFA-011): a board in its enclosure with 1 mm all round; a tab stub left by a breakaway tab needs
    # that room; the edge that must be held tightly is marked critical and routed (about +/-0.1 mm).
    import drawsvg as dw
    s = Sheet(900, 700, "A board in its enclosure: room all round, and a critical edge",
              "Drawn to scale, plan view of a 50 by 30 mm board inside an enclosure, with 1 mm of room all round. On "
              "the left edge, a small stub of a breakaway tab sticks out about 0.5 mm, shown enlarged on the right; "
              "the room around the board leaves space for it. The right edge is marked as critical, so the assembler "
              "routes it instead of scoring or tabbing it, holding it to about plus or minus 0.1 mm.",
              scale=8, ox=90, oy=110)
    s.rect(-4, -4, 58, 38, "enclosure")
    s.rect(-1, -1, 52, 32, "bg")
    s.rect(0, 0, 50, 30, "mask-on-fr4")
    for px, py, pw, ph in ((8, 8, 2, 1.2), (8, 11, 2, 1.2), (20, 10, 8, 8), (36, 20, 1.2, 2), (40, 6, 4, 2)):
        s.rect(px, py, pw, ph, "cu-exposed")
    s.rect(-0.5, 13, 0.5, 4, "mask-on-fr4")                      # tab stub
    s.line(50, 0, 50, 30, "wall")                                # critical edge
    s.dim_h(0, 50, 38, "50 ±0.1 mm, critical: route this edge", ext_from=30.5, text_above=False)
    s.rect(-2, 12, 4, 6, "asm")
    # enlarged view of the tab stub
    K, IX, IY = 40, 640, 160                                     # px per mm, origin of the enlarged view
    def ip(x, y):
        return IX + (x + 2) * K, IY + (y - 12) * K
    x0, y0 = ip(-2, 12)
    s.d.append(dw.Rectangle(x0, y0, K * 1, K * 6, class_="enclosure"))
    s.d.append(dw.Rectangle(x0 + K * 1, y0, K * 1, K * 6, class_="bg"))
    s.d.append(dw.Rectangle(x0 + K * 2, y0, K * 2, K * 6, class_="mask-on-fr4"))
    s.d.append(dw.Rectangle(x0 + K * 1.5, y0 + K * 1, K * 0.5, K * 4, class_="mask-on-fr4"))
    for k in range(5):
        cx, cy = ip(-0.5, 13.4 + k * 0.8)
        s.d.append(dw.Circle(cx, cy, K * 0.25, class_="bg"))
    s.d.append(dw.Rectangle(x0, y0, K * 4, K * 6, class_="thin"))
    s.text("Left edge, enlarged", x0, y0 - 10 * s.f, size=11, cls="muted", px=True)
    for a, b, yy, label in ((-1, 0, 17.6, "1 mm room"), (-0.5, 0, 12.5, "0.5 mm stub")):
        (xa, ya), (xb, _) = ip(a, yy), ip(b, yy)
        s.d.append(dw.Line(xa, ya, xb, ya, class_="dim"))
        s._arrowhead(xa, ya, 3.1416); s._arrowhead(xb, ya, 0)
        s.d.append(dw.Text(label, s.fs(12), IX + 4 * K + 8 * s.f, ya + 4 * s.f, class_="dimtxt"))
    s.d.append(dw.Line(s.X(2), s.Y(12), x0, y0, class_="thin"))
    s.balloon(1, (-0.25, 15), (s.X(-8), s.Y(-6)), "Tab stub", "About 0.5 mm left by a breakaway tab")
    s.balloon(2, (50, 22), (s.X(56) + 30, s.Y(26)), "Critical edge", "Routed, about ±0.1 mm")
    s.balloon(3, (-2.5, 25), (s.X(-8), s.Y(32)), "Enclosure wall", "1 mm from the board all round")
    key_below(s, s.Y(38) + 70 * s.f, x=60, split=2,
              notes=("Drawn to scale. Dimensions in mm. Values from PCB-DFA-011.",
                     "Room: about 1 mm all round, 0.5 mm at the very least."))
    s.save(out(33, "enclosure-room"))


def panel_style():
    # D48 (PCB-DFA-076, 077, 005): one assembler's panel style, top and bottom sides. 10 mm rails on all four
    # sides and between the boards; three fiducials of different sizes on the short-edge rails, round on top and
    # square on the bottom; side and part number printed on the long-edge rail opposite the 2 and 3 mm fiducials.
    BW, BH, R = 60, 40, 10
    PW, PH = 3 * R + 2 * BW, 3 * R + 2 * BH
    s = Sheet(980, 1150, "One assembler's panel: fiducials and labels that can't be mistaken",
              "Drawn to scale, the top and the bottom of a 150 by 110 mm panel of four 60 by 40 mm boards, with 10 mm "
              "rails on all four sides and between the boards. Each side has three fiducials on the short-edge rails, "
              "centered in the rail and 15 mm from the long edges: 1 mm at the upper left, 2 mm at the lower left and "
              "3 mm at the lower right. They are round on the top side and square on the bottom side, as the "
              "enlarged row below shows. The rail along the long edge opposite the 2 and 3 mm fiducials carries the "
              "side, Top or Bottom, and the board's part number in silkscreen.",
              scale=2.6, ox=75, oy=130)
    CHIP = [(8, 8, 6, 6), (20, 14, 10, 10), (40, 10, 2, 5), (36, 26, 4, 2), (14, 28, 2, 4)]

    def fid(x, y, d, shape):
        if shape == "round":
            s.circle(x, y, d, "fr4-exposed")
            s.circle(x, y, d / 2, "cu-exposed")
        else:
            s.rect(x - d, y - d, 2 * d, 2 * d, "fr4-exposed")
            s.rect(x - d / 2, y - d / 2, d, d, "cu-exposed")

    G = 30
    for k, (side, shape) in enumerate((("Top", "round"), ("Bottom", "square"))):
        x0 = k * (PW + G)
        s.rect(x0, 0, PW, PH, "mask-on-fr4")                       # rails and frame: board material
        for r in range(2):
            for c in range(2):
                bx, by = x0 + R + c * (BW + R), R + r * (BH + R)
                for px, py, pw, ph in CHIP:
                    s.rect(bx + px, by + py, pw, ph, "cu-exposed")
                s.rect(bx, by, BW, BH, "edge")
        s.rect(x0, 0, PW, PH, "edge")
        for (fx, fy, d) in ((x0 + 5, 15, 1), (x0 + 5, PH - 15, 2), (x0 + PW - 5, PH - 15, 3)):
            fid(fx, fy, d, shape)
        s.text(side, x0 + R + BW / 2, 6.6, size=12, cls="silk", anchor="middle", weight="700")
        s.text("PART-123", x0 + 2 * R + 1.5 * BW, 6.6, size=12, cls="silk", anchor="middle", weight="700")
        s.text(f"{side} side", x0 + PW / 2, -18, size=14, anchor="middle", weight="600")
    s.dim_v(0, R, -6, "10 rail", ext_from=0, text_left=True)
    s.dim_v(PH - 15, PH, -6, "15", ext_from=0, text_left=True)
    s.dim_h(0, 5, PH + 7, "5", ext_from=PH, text_side="left")
    s.dim_h(0, PW, PH + 17, "150 mm panel", ext_from=PH)
    s.balloon(4, (R + BW / 2 - 8, 2.5), (s.X(R + BW / 2 - 8), s.Y(-9)), "Side, printed on the rail", "Top or Bottom")
    s.balloon(5, (2 * R + 1.5 * BW - 18, 2.5), (s.X(2 * R + 1.5 * BW - 18), s.Y(-9)), "Part number, printed on the rail")
    s.balloon(1, (5, 15), (s.X(-14), s.Y(30)), "1 mm fiducial", "Upper corner, on the short-edge rail")
    s.balloon(2, (5, PH - 15), (s.X(-14), s.Y(PH - 32)), "2 mm fiducial", "Lower corner, same rail")
    s.balloon(3, (PW - 5, PH - 15), (s.X(PW) + 25, s.Y(PH - 15)), "3 mm fiducial", "Other end, same long edge as the 2 mm")
    # enlarged row of the six fiducials
    s.scale, s.ox, s.oy = 9, 75, 560
    s.text("Enlarged:", 0, -6, size=13, weight="600")
    for i, (shape, d) in enumerate([("round", 1), ("round", 2), ("round", 3), ("square", 1), ("square", 2), ("square", 3)]):
        x = 6 + i * 13 + (6 if shape == "square" else 0)
        fid(x, 4, d, shape)
        s.text(f"{d} mm", x, 11.5, size=12, anchor="middle")
    s.text("Top side: round", 6 + 13, 15.5, size=12, cls="muted", anchor="middle")
    s.text("Bottom side: square", 6 + 6 + 4 * 13, 15.5, size=12, cls="muted", anchor="middle")
    key_below(s, s.Y(15.5) + 60 * s.f, x=40, split=3,
              notes=("Drawn to scale. Dimensions in mm. 10 mm rails on all four sides and between boards.",
                     "Fiducials centered in the short-edge rails, 15 mm from the long edges.",
                     "Copper dots 1, 2 and 3 mm, each in a mask opening twice its size.",
                     "After one assembler's panel guidelines (PCB-DFA-076, 077)."))
    s.save(out(48, "panel-style"))


if __name__ == "__main__":
    panel_style()
    panel_anatomy()
    fiducial_detail()
    vscore_clearance()
    recessed_tab()
    mouse_bite_clearance()
    overhang_vscore()
    overhang_facing()
    small_board_panel()
    panel_sag()
    local_fiducials()
    outline_shapes()
    enclosure_room()
    print("written to", OUT)

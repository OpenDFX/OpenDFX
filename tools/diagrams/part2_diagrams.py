"""Part 2 diagrams D45-D47 in the OpenDFX style.
Run: python3 tools/diagrams/part2_diagrams.py         (writes trials/python-N-<name>.svg for review)
     python3 tools/diagrams/part2_diagrams.py --book  (writes book/03-bare-board-fabrication/images/<name>.svg)"""
from pathlib import Path
import math
import sys

import drawsvg as dw
import opendfx_draw
from opendfx_draw import Sheet

BOOK = "--book" in sys.argv
OUT = (Path(__file__).parent / "trials") if not BOOK else (Path(__file__).parents[2] / "book" / "03-bare-board-fabrication" / "images")
OUT.mkdir(exist_ok=True)

# Thin layers (copper, mask) are drawn thicker than true scale so they can be seen.
CU, SM = 0.06, 0.09


def out(n, name):
    opendfx_draw.CURRENT_D = n
    return OUT / (f"{name}.svg" if BOOK else f"python-{n}-{name}.svg")


def fit(build, W, H):
    """DRW1: build(W, H) draws a sheet and returns (sheet, y where its content ends). Text grows with the print
    sizes, so the sheet's height is set to its content and the drawing is built again until the two agree."""
    for _ in range(8):
        s, end = build(W, H)
        need = math.ceil(end + 18 * s.f)
        if abs(need - H) <= 3:
            break
        H = need
    return s


def swatches(s, x0, y, items):
    """Color swatches with labels in rows across the sheet (DRW1). Returns the y of the last row."""
    f = s.f
    x = x0
    for cls, label in items:
        w = 22 * f + 0.55 * s.fs(12) * len(label)
        if x + w > s.width - x0 and x > x0:
            x, y = x0, y + 24 * f
        s.d.append(dw.Rectangle(x, y - 11 * f, 14 * f, 14 * f, class_=cls))
        s.d.append(dw.Rectangle(x, y - 11 * f, 14 * f, 14 * f, class_="thin"))
        s.text(label, x + 22 * f, y + 1 * f, size=12, px=True)
        x += w + 24 * f
    return y


def foot(s, y, notes=(), x0=40, legend=None):
    """DRW1, Q177 option A: the key in two columns under the drawing, then the color legend and the notes across
    the full width. A note of "" leaves a small gap. Returns the y of the last line."""
    f = s.f
    rows = sorted(s.balloons)
    hts = [26 + (16 if d else 0) for _, _, d in rows]
    best = min(range(1, len(rows) + 1), key=lambda k: max(sum(hts[:k]), sum(hts[k:])))
    if len(rows) <= 3:
        best = len(rows)                    # a short key stays in one column
    colw = (s.width - 2 * x0 - 40 * f) / 2
    y1 = s.key(x0, y, width=colw, only=[n for n, _, _ in rows[:best]])
    y2 = s.key(x0 + colw + 40 * f, y, width=colw, title="", only=[n for n, _, _ in rows[best:]]) if best < len(rows) else y1
    y = max(y1, y2) + 12 * f
    if legend:
        y = swatches(s, x0, y + 30 * f, legend) + 6 * f
    for line in notes:
        y += (20 if line else 8) * f
        if line:
            s.note(line, x0, y)
    return y


def poly(s, pts, cls):
    flat = [v for x, y in pts for v in (s.X(x), s.Y(y))]
    s.d.append(dw.Lines(*flat, close=True, class_=cls))


def lpi(s, x0, x1, y0, d, pads=(), holes=(), opens=(), film=None, t=None, cu=None, sag=0.9):
    """Liquid photoimageable solder mask (LPI) from x0 to x1 on the board face at y0; d = -1 on the top side, +1 on
    the bottom. It is drawn as a liquid that flowed and set (IMG3, Chris 2026-11-07): its surface is a smoothed copy
    of what lies under it, so the coat is thickest on bare FR4, thinner on copper, thinnest at the copper's corners,
    and it sags where it spans a hole.
    pads: (a, b, h) copper (or flush fill) h thick on this face. holes: (a, b) open holes, tented unless in `opens`.
    opens: (a, b) zones the mask is pulled back from; its edge rounds off like a meniscus.
    film: (a, b, h) a flat dry-film tent, h thick, laid over the pads first (IPC-4761 Type II)."""
    t = SM if t is None else t
    cu = CU if cu is None else cu
    sig = 1.3 * cu
    n = max(2, int((x1 - x0) / (cu / 12)) + 1)
    xs = [x0 + i * (x1 - x0) / (n - 1) for i in range(n)]

    def pad_h(x):
        return max([h for a, b, h in pads if a <= x <= b] or [0.0])

    def hole_at(x):
        return next(((a, b) for a, b in holes if a < x < b), None)

    ftop = 0.0
    if film:
        fa, fb, fh = film
        base = max([h for a, b, h in pads if b > fa and a < fb] or [0.0])
        ftop = base + fh
        s.rect(fa, y0 + d * base if d > 0 else y0 - ftop, fb - fa, fh, "mask-on-fr4")
    H, base_cls = [], []
    for x in xs:
        if film and film[0] <= x <= film[1]:
            H.append(ftop); base_cls.append("mask-on-cu")
            continue
        hl = hole_at(x)
        if hl:            # bridge the hole at the height of the copper round it, for the leveling
            H.append(max(pad_h(hl[0]), pad_h(hl[1]))); base_cls.append("mask-on-cu")
        else:
            h = pad_h(x)
            H.append(h); base_cls.append("mask-on-cu" if h > 0 else "mask-on-fr4")
    k = int(3 * sig / (xs[1] - xs[0])) + 1
    w = [math.exp(-0.5 * ((j * (xs[1] - xs[0])) / sig) ** 2) for j in range(-k, k + 1)]
    sw = sum(w)
    M = []
    rc = 0.4 * t                                  # the thinnest coat, round the copper's corners and sides
    kc = int(rc / (xs[1] - xs[0])) + 1
    for i in range(n):
        acc = sum(w[j + k] * H[min(n - 1, max(0, i + j))] for j in range(-k, k + 1))
        hug = max(H[q] + math.sqrt(max(0.0, rc * rc - (xs[q] - xs[i]) ** 2))
                  for q in range(max(0, i - kc), min(n, i + kc + 1)))
        M.append(max(t + 0.72 * acc / sw, hug))
    B = list(H)
    for i, x in enumerate(xs):
        hl = None if (film and film[0] <= x <= film[1]) else hole_at(x)
        if hl:
            u = (x - (hl[0] + hl[1]) / 2) / ((hl[1] - hl[0]) / 2)
            M[i] -= sag * t * (1 - u * u)
            B[i] = M[i] - 0.75 * t
        M[i] = max(M[i], B[i] + 0.3 * t) if hl else M[i]
    on = []
    for i, x in enumerate(xs):
        inside = any(a <= x <= b for a, b in opens)
        e = min([min(abs(x - a), abs(x - b)) for a, b in opens] or [9.0])
        if not inside and e < 2.2 * t:          # meniscus at a pulled-back edge
            M[i] = B[i] + (M[i] - B[i]) * math.sqrt(max(e, 1e-9) / (2.2 * t))
        on.append(not inside)
    i = 0
    while i < n:
        if not on[i]:
            i += 1
            continue
        j = i
        while j + 1 < n and on[j + 1] and base_cls[j + 1] == base_cls[i]:
            j += 1
        jj = min(n - 1, j + 1) if (j + 1 < n and on[j + 1]) else j
        ii = i - 1 if (i > 0 and on[i - 1]) else i                # overlap neighbors by a sample: no seams
        top = [(xs[q], y0 + d * M[q]) for q in range(ii, jj + 1)]
        bot = [(xs[q], y0 + d * (min(B[j], B[q]) if q == jj else min(B[i], B[q]) if q == ii else B[q]))
               for q in range(jj, ii - 1, -1)]
        poly(s, top + bot, base_cls[i])
        i = j + 1
    return xs, [y0 + d * m for m in M]           # the mask's surface, for anything printed on top of it


def via(s, cx, T, hole=0.3, pad=0.6, half=1.15, top="open", bot="open", fill=None, cap=False, cover=False):
    """Cross-section of a plated via in a board of thickness T (mm), centered at cx, built the way a fab builds it:
    the plating lines the hole and joins the surface pads and the inner-layer pads; solder mask lies on the board
    surface and steps up over a pad when it covers one.
    top/bot: "open" (mask stops short of the pad) or "tent" (mask laid over pad and hole).
    fill: None, "plug" (plugged about a third of the way in from each side) or "full"."""
    r = hole / 2
    s.rect(cx - half, 0, 2 * half, T, "bare")                               # FR4
    s.rect(cx - r, -CU, hole, T + 2 * CU, "drill")                          # the hole
    for y in (T / 3, 2 * T / 3):                                            # inner-layer pads
        s.rect(cx - pad / 2, y - CU / 2, pad / 2 - r, CU, "copper")
        s.rect(cx + r, y - CU / 2, pad / 2 - r, CU, "copper")
    for y in (-CU, T):                                                      # surface pads
        s.rect(cx - pad / 2, y, pad / 2 - r, CU, "copper")
        s.rect(cx + r, y, pad / 2 - r, CU, "copper")
    s.rect(cx - r, -CU, CU, T + 2 * CU, "copper")                           # barrel plating
    s.rect(cx + r - CU, -CU, CU, T + 2 * CU, "copper")
    w = hole - 2 * CU
    if fill == "full":
        s.rect(cx - w / 2, -CU, w, T + 2 * CU, "capbody")
    elif fill == "plug":
        s.rect(cx - w / 2, -CU, w, T / 3 + CU, "capbody")
        s.rect(cx - w / 2, T - T / 3, w, T / 3 + CU, "capbody")
    if cap:                                                                 # copper plated flat over the fill
        s.rect(cx - pad / 2, -2 * CU, pad, CU, "copper")
        s.rect(cx - pad / 2, T + CU, pad, CU, "copper")
    r_in = r - CU                                                           # the plated hole's open radius
    for side, mode in (("top", top), ("bot", bot)):
        y0, dd = (0, -1) if side == "top" else (T, 1)
        if cap:
            pads, holes = [(cx - pad / 2, cx + pad / 2, 2 * CU)], []
        elif fill == "full":
            pads, holes = [(cx - pad / 2, cx + pad / 2, CU)], []
        else:
            pads = [(cx - pad / 2, cx - r_in, CU), (cx + r_in, cx + pad / 2, CU)]
            holes = [(cx - r_in, cx + r_in)]
        opens = [(cx - pad / 2 - 0.06, cx + pad / 2 + 0.06)] if mode == "open" else []
        film = (cx - pad / 2 - 0.05, cx + pad / 2 + 0.05, 0.5 * SM) if (cover and mode == "tent") else None
        lpi(s, cx - half, cx + half, y0, dd, pads=pads, holes=holes, opens=opens, film=film)

def via_types():
    s = fit(_via_types, 1000, 1290)
    s.save(out(45, "via-treatments"))


def _via_types(W, H):
    # D45. DRW1: two rows of five, the enlarged views, then the key in two columns and the notes (Q177 option A).
    s = Sheet(W, H,
              "The IPC-4761 via treatments, in cross-section",
              "Cross-sections of a 0.3 mm plated via in a 1.6 mm board, as a fab builds it: the plating lines the hole "
              "and joins the surface pads and two inner-layer pads; solder mask lies on the board surface. Open: mask "
              "pulled back, pads and hole exposed. Ia: mask laid over the pad and across the hole on one side only. "
              "Ib: the same on both sides. II: tented on both sides and covered with a second coat of mask. III: "
              "plugged a third of the way in from each side, air in the middle, pads exposed. IV: plugged, then "
              "covered with mask on both sides. V: completely filled, flush with the pads. VI: filled and covered "
              "with mask. VII: filled, then plated flat with copper over the hole, so a pad can sit on top. Ia is "
              "marked avoid: tenting one side only traps air and process chemistry. Type II is rarely used. Solder mask is "
              "a liquid coat that flows before it sets: thickest on bare FR4, thinnest at the copper's corners, "
              "and sagging where it spans a hole. Below, enlarged to true scale, the top of one via tented (left) and "
              "with the mask pulled back (right).",
              scale=56, ox=20, oy=80)
    f = s.f
    T, SC, PITCH = 1.6, 56, 194 / 56          # via scale, and the cell pitch in mm (194 units)
    row_top = [80, 80]
    lab = [28 * f, 48 * f, 68 * f]            # title, name and "avoid" baselines below the board's bottom face
    row_top[1] = row_top[0] + T * SC + lab[1] + 22 * f
    rows = [[("Open", "Not covered", dict()),
             ("✗ Type Ia", "Tented, one side", dict(top="tent")),
             ("Type Ib", "Tented, both sides", dict(top="tent", bot="tent")),
             ("Type II", "Tented and covered", dict(top="tent", bot="tent", cover=True)),
             ("Type III", "Plugged", dict(fill="plug"))],
            [("Type IV", "Plugged and covered", dict(fill="plug", top="tent", bot="tent")),
             ("Type V", "Filled", dict(fill="full")),
             ("Type VI", "Filled and covered", dict(fill="full", top="tent", bot="tent")),
             ("Type VII", "Filled and capped", dict(fill="full", cap=True))]]
    cx0 = (100 - 20) / SC
    for ri, row in enumerate(rows):
        s.oy = row_top[ri]
        for i, (t, name, kw) in enumerate(row):
            cx = cx0 + i * PITCH
            via(s, cx, T, **kw)
            yb = s.Y(T)
            s.text(t, s.X(cx), yb + lab[0], size=14, anchor="middle", weight="600", px=True)
            s.text(name, s.X(cx), yb + lab[1], size=11.5, cls="muted", anchor="middle", px=True)
    s.oy = row_top[0]
    c = cx0 + PITCH          # Ia, for the balloons
    s.balloon(1, (c - 0.8, 1.2), (s.X(c - 1.1), s.Y(-0.9)), "FR4")
    s.balloon(2, (c - 0.3, 2 * T / 3), (s.X(c - 0.55), s.Y(-0.9)), "Inner-layer pad")
    s.balloon(3, (c - 0.15 + 0.02, 1.25), (s.X(c), s.Y(-0.9)), "Plated hole wall", "Joins the surface and inner-layer pads")
    s.balloon(4, (c + 0.2, -CU - SM / 2), (s.X(c + 0.55), s.Y(-0.9)), "Solder mask over the pad and hole (the tent)")
    s.balloon(5, (c + 0.8, -0.03), (s.X(c + 1.1), s.Y(-0.9)), "Solder mask on FR4")
    c2 = cx0 + 3 * PITCH
    s.balloon(6, (c2 + 0.5, -CU - 2 * SM + 0.01), (s.X(c2 + 0.6), s.Y(-0.9)), "Second coat of mask")
    s.oy = row_top[1]
    c3 = cx0 + 1 * PITCH
    s.balloon(7, (c3, 0.9), (s.X(c3 + PITCH / 2), s.Y(0.9)), "Fill or plug material", free=True)
    c4 = cx0 + 3 * PITCH
    s.balloon(8, (c4 + 0.25, -1.5 * CU), (s.X(c4 + PITCH / 2), s.Y(0.2)), "Copper cap, plated flat over the fill",
              free=True)
    # Enlarged detail at true scale: the top 0.12 mm of a 0.3 mm via, tented and open.
    sc = 330
    oy = s.Y(T) + lab[1] + 26 * f + 0.2 * sc + 14 * f
    s.scale, s.oy = sc, oy
    cu, t, rd, pl = 0.05, 0.025, 0.175, 0.025       # copper with its plating, mask on FR4, drilled radius, plating
    for k, mode in enumerate(("tent", "open")):
        s.ox = 40 + k * 490
        cx, half, depth = 0.55, 0.55, 0.12
        s.rect(cx - half, 0, 2 * half, depth, "bare")
        s.rect(cx - rd, -cu, 2 * rd, depth + cu, "drill")
        s.rect(cx - rd, -cu, pl, depth + cu, "copper"); s.rect(cx + rd - pl, -cu, pl, depth + cu, "copper")
        s.rect(cx - 0.3, -cu, 0.3 - rd + pl, cu, "copper"); s.rect(cx + rd - pl, -cu, 0.3 - rd + pl, cu, "copper")
        r_in = rd - pl
        lpi(s, cx - half, cx + half, 0, -1, pads=[(cx - 0.3, cx - r_in, cu), (cx + r_in, cx + 0.3, cu)],
            holes=[(cx - r_in, cx + r_in)], opens=[(cx - 0.36, cx + 0.36)] if mode == "open" else [], t=t, cu=cu)
        s.text(["Enlarged, true scale: tented", "Enlarged, true scale: mask pulled back"][k], cx, -0.2, size=13,
               anchor="middle", weight="600")
    s.ox = 40
    s.balloon(9, (0.12, -0.022), (s.X(0.12), s.Y(0.2)), "Thickest on bare FR4", "The liquid levels out between features")
    s.balloon(10, (0.55 - 0.3 - 0.004, -cu - 0.004), (s.X(0.3), s.Y(0.2)), "Thinnest at the copper's corner")
    s.balloon(11, (0.55, -cu + 0.002), (s.X(0.6), s.Y(0.2)), "Sags over the hole", "A tent is thin and can crack")
    s.ox = 530
    s.balloon(12, (0.55 + 0.37, -0.008), (s.X(0.95), s.Y(0.2)), "Rounded edge where the mask is pulled back")
    y = foot(s, s.Y(0.2) + 40 * f, [
        "A 0.3 mm via in a 1.6 mm board, to scale. Copper and mask are drawn thicker than true scale so they show.",
        "Enlarged views: copper about 50 µm with its plating, and mask about 25 µm on FR4 (an example; fabs vary).",
        "\"Tented\" here means IPC's Type I, mask over ring and hole. Type II is rarely used."])
    s.scale, s.ox, s.oy = 56, 20, 80
    return s, y


def qfn_thermal_vias():
    s = fit(_qfn_thermal_vias, 980, 640)
    s.save(out(46, "qfn-thermal-vias"))


def _qfn_thermal_vias(W, H):
    s = Sheet(W, H,
              "Thermal vias under a QFN: right and wrong",
              "Cross-sections through a QFN's ground pad on a 1.6 mm board with three 0.3 mm thermal vias. Left: "
              "vias open on both sides, so gas from the solder and flux can escape. Middle: vias filled and capped "
              "flat with copper, so nothing is trapped. Right, wrong: vias masked on the bottom and open on top; "
              "air and flux are trapped in the closed holes and expand in the oven, blowing voids into the joint or "
              "lifting the part.",
              scale=56, ox=20, oy=172)
    f = s.f
    T, W, gap = 1.6, 4.6, 1.15
    for k, (title, mode) in enumerate((("✓ Open both sides", "open"), ("✓ Filled and capped", "cap"),
                                       ("✗ Masked on the bottom", "tent"))):
        x0 = k * (W + gap)
        c = x0 + W / 2
        s.rect(x0, 0, W, T, "bare")                                  # laminate (FR4)
        s.rect(c - 1.7, -CU, 3.4, CU, "copper")                         # ground pad
        lpi(s, x0, x0 + W, 0, -1, pads=[(c - 1.7, c + 1.7, CU)], opens=[(c - 1.78, c + 1.78)])
        s.rect(c - 1.6, -CU - 0.12, 3.2, 0.12, "paste")                 # solder
        s.rect(c - 1.7, -CU - 0.12 - 0.1, 3.4, 0.1, "term")             # QFN exposed pad
        s.rect(c - 2.1, -CU - 0.22 - 0.75, 4.2, 0.75, "part")           # QFN body
        for j in (-1, 0, 1):
            vx = c + j * 1.0
            s.rect(vx - 0.3, T, 0.6, CU, "copper")                      # bottom pad
            s.rect(vx - 0.15, -CU, 0.3, T + 2 * CU, "drill")
            if mode == "open":
                s.rect(vx - 0.15, -CU, 0.3, T + 2 * CU, "drill")
            s.rect(vx - 0.15, 0, CU, T, "copper"); s.rect(vx + 0.15 - CU, 0, CU, T, "copper")
            if mode == "tent":
                for by, br in ((0.45, 0.07), (0.9, 0.05), (1.3, 0.06)):
                    s.circle(vx, by, br, "zone-s")
            if mode == "cap":
                s.rect(vx - 0.1, 0, 0.2, T, "capbody")
                s.rect(vx - 0.15, -CU, 0.3, CU, "copper"); s.rect(vx - 0.15, T, 0.3, CU, "copper")
        bpads = [(c + j * 1.0 + sg * 0.3, c + j * 1.0 + sg * (0.15 - CU), CU) for j in (-1, 0, 1) for sg in (-1, 1)]
        bpads = [(min(a, b), max(a, b), h) for a, b, h in bpads]
        if mode == "cap":
            bpads = [(c + j * 1.0 - 0.3, c + j * 1.0 + 0.3, CU) for j in (-1, 0, 1)]
        bholes = [] if mode == "cap" else [(c + j * 1.0 - 0.15 + CU, c + j * 1.0 + 0.15 - CU) for j in (-1, 0, 1)]
        lpi(s, x0, x0 + W, T, 1, pads=bpads, holes=bholes,
            opens=[] if mode == "tent" else [(c - 1.3, c + 1.3)])
        s.text(title, c, -1.75, size=14, anchor="middle", weight="600")
    x2 = 2 * (W + gap)
    s.balloon(1, (2.3 - 1.8, -0.6), (s.X(-0.1) + 14 * f, s.Y(-2.4) - 4 * f), "QFN")
    s.balloon(2, (2.3 + 1.2, -0.11), (s.X(2.3 + 1.6), s.Y(-2.4) - 4 * f), "Solder under the ground pad")
    s.balloon(3, (2.3 + 0.0, 1.0), (s.X(1.0), s.Y(3.0)), "Open thermal via", "About 0.3 mm; gas can escape")
    s.balloon(4, (W + gap + 2.3, 1.0), (s.X(W + gap + 1.0), s.Y(3.0)), "Filled and capped via", "IPC-4761 Type VII")
    s.balloon(5, (x2 + 3.9, T + 0.07), (s.X(x2 + 4.0), s.Y(3.0)), "Solder mask over the bottom", "Never do this")
    s.balloon(6, (x2 + 2.3 + 1.0, 0.9), (s.X(x2 + 2.4), s.Y(3.0)), "Trapped air and flux", "Expand in the oven")
    y = foot(s, s.Y(3.0) + 50 * f, [
        "Board 1.6 mm, vias 0.3 mm, to scale. Copper, mask and solder are drawn thicker",
        "than true scale so they show.",
        "Never put solder mask on thermal vias under a QFN, on either side (PCB-DFA-075)."])
    return s, y


def aspect_annular():
    s = fit(_aspect_annular, 980, 560)
    s.save(out(47, "aspect-ratio-annular-ring"))


def _aspect_annular(W, H):
    s = Sheet(W, H,
              "Aspect ratio and annular ring",
              "Left: a cross-section of a 1.6 mm board with a 0.2 mm drilled hole, an aspect ratio of 8 to 1, the "
              "recommended limit. Right: top views of a 0.6 mm pad on a 0.3 mm hole. Centered, the copper ring "
              "around the hole, the annular ring, is 0.15 mm all round. With the drill 0.1 mm off center, the ring "
              "is only 0.05 mm on one side: still inside the pad, which is what the margin is for.",
              scale=110, ox=70, oy=80)
    f = s.f
    T, d = 1.6, 0.2
    cx = 0.9
    s.rect(cx - 0.7, 0, 1.4, T, "bare")
    s.rect(cx - d / 2, 0, d, T, "drill")
    s.rect(cx - d / 2, 0, 0.02, T, "copper"); s.rect(cx + d / 2 - 0.02, 0, 0.02, T, "copper")
    s.rect(cx - 0.25, -0.03, 0.5, 0.03, "copper"); s.rect(cx - 0.25, T, 0.5, 0.03, "copper")
    s.dim_v(0, T, cx + 1.0, "1.6 board", ext_from=cx + 0.7)
    s.dim_h(cx - d / 2, cx + d / 2, T + 0.4, "0.2 drill", ext_from=T + 0.05)
    s.text("8 : 1", cx, -0.35, size=16, anchor="middle", weight="600")
    s.text("Aspect ratio = board ÷ drill", cx, T + 0.95, size=12, cls="muted", anchor="middle")
    for k, (off, title) in enumerate(((0.0, "Drill centered"), (0.1, "Drill 0.1 mm off center"))):
        px = 3.6 + k * 2.6
        py = 0.9
        s.circle(px, py, 0.3, "copper")
        s.circle(px + off, py, 0.15, "hole")
        s.text(title, px, py - 0.75, size=13, anchor="middle", weight="600")
        if k == 0:
            s.dim_h(px + 0.15, px + 0.3, py + 0.55, "0.15 ring", ext_from=py)
            s.dim_h(px - 0.3, px + 0.3, py - 0.42, "0.6 pad", ext_from=py)
        else:
            s.dim_h(px + off + 0.15, px + 0.3, py + 0.55, "0.05 left", ext_from=py)
    s.balloon(1, (cx - d / 2 + 0.01, 0.8), (s.X(cx - 0.7) - 30, s.Y(0.8)), "Plated hole wall")
    s.balloon(2, (3.6 - 0.25, 0.9), (s.X(3.6 - 0.6), s.Y(1.9)), "Annular ring")
    y = foot(s, s.Y(T + 0.95) + 44 * f, [
        "Drawn to scale. Dimensions in mm.",
        "Aspect ratio: 8:1 or less is recommended, and 10:1 at most (PCB-DFM-024).",
        "Annular ring: design 0.15 mm on outer layers. IPC Class 3 needs 50 µm on the finished board (PCB-DFM-026)."],
        x0=70)
    return s, y


def via_web():
    s = fit(_via_web, 980, 560)
    s.save(out(49, "via-mask-web"))


def _via_web(W, H):
    # D49 (PCB-DFA-078): a via beside a pad: mask web between them, tented, or no web.
    s = Sheet(W, H, "A via beside a pad: a mask web between them, tented, or no web",
              "Drawn to scale, plan views of a 1.0 by 1.2 mm pad joined by a 0.25 mm trace to a via with a 0.3 mm hole "
              "and a 0.6 mm ring. Left, right: the via is 0.55 mm from the pad and each has its own mask opening, "
              "leaving a 0.15 mm web of mask between them. Middle, right: the via is tented, covered with mask. Right, "
              "wrong: the via is closer and its opening runs into the pad's, so there is no web and solder can run "
              "from the pad onto the via and down the hole.",
              scale=80, ox=130, oy=150)
    f = s.f
    M = 0.05                                     # mask opening margin round copper
    cases = [("web", 1.05, "✓ Mask web between via and pad"), ("tent", 1.05, "✓ Via tented"),
             ("none", 0.85, "✗ No web")]
    for i, (kind, vx, title) in enumerate(cases):
        dx = i * 3.2

        def geom(add, cu, fr4, dx=dx, vx=vx):
            add(s.R(dx - 1.0, -1.1, 2.9, 2.2, fr4))
            add(s.R(dx - 0.5, -0.6, 1.0, 1.2, cu))
            add(s.R(dx, -0.125, vx, 0.25, cu))
            add(s.C(dx + vx, 0, 0.3, cu))
        openings = [s.R(dx - 0.5 - M, -0.6 - M, 1.0 + 2 * M, 1.2 + 2 * M, "bg")]
        if kind != "tent":
            openings.append(s.C(dx + vx, 0, 0.3 + M, "bg"))
        if kind == "none":
            openings.append(s.R(dx + 0.5, -0.125 - M, vx - 0.5, 0.25 + 2 * M, "bg"))
        s.board_view((dx - 1.0, -1.1, 2.9, 2.2), geom, openings, [(dx + vx, 0, 0.15)])
        s.text(title, s.X(dx + 0.45), s.Y(-1.35), size=14, anchor="middle", weight="600", px=True)
    s.dim_h(0.5 + M, 1.05 - 0.3 - M, -0.85, "0.15 web", ext_from=-0.15)
    s.balloon(1, (-0.1, 0.35), (s.X(-0.1), s.Y(1.55)), "Pad, in its own mask opening")
    s.balloon(2, (0.625, 0.05), (s.X(0.9), s.Y(1.55)), "Mask web", "At least 0.1 mm; wider is better", free=True)
    s.balloon(3, (3.2 + 1.05 + 0.2, 0.15), (s.X(3.2 + 1.05) + 10, s.Y(1.55)), "Tented via", "Mask covers ring and hole")
    s.balloon(4, (6.4 + 0.65, 0.0), (s.X(6.4 + 0.65) + 10, s.Y(1.55)), "No mask between pad and via",
              "Solder runs onto the via and down the hole")
    y = foot(s, s.Y(1.55) + 50 * f, [
        "Drawn to scale. Mask openings 0.05 mm larger than the copper.",
        "Thermal vias in a QFN's ground pad stay open on purpose (PCB-DFA-075)."],
        legend=[("cu-exposed", "Exposed copper"), ("fr4-exposed", "Exposed FR4"), ("mask-on-cu", "Mask over copper"),
                ("mask-on-fr4", "Mask over FR4"), ("drill", "Hole")])
    return s, y


def bga_pads():
    s = fit(_bga_pads, 980, 680)
    s.save(out(50, "bga-pads"))


def _bga_pads(W, H):
    # D50 (PCB-DFA-079): BGA pads, copper-defined (NSMD) vs mask-defined (SMD), in cross-section after reflow.
    s = Sheet(W, H, "BGA pads: copper-defined and mask-defined",
              "Enlarged, drawn to scale, cross-sections through one solder ball of a 0.8 mm-pitch BGA after reflow. Left, "
              "copper-defined (NSMD): a 0.35 mm copper pad with a mask opening 0.45 mm across, so the mask does not "
              "touch the pad and the solder wraps round the pad's sides. Right, mask-defined (SMD): a 0.45 mm pad with "
              "the mask overlapping its edge to leave a 0.35 mm opening, so the solder meets the mask in a notch.",
              scale=380, ox=70, oy=290)
    f = s.f
    cu, t, gap = 0.035, 0.025, 0.30
    for k, kind in enumerate(("nsmd", "smd")):
        cx = 0.5 + k * 1.05
        s.rect(cx - 0.5, 0, 1.0, 0.22, "bare")                       # board laminate
        pw = 0.35 if kind == "nsmd" else 0.45
        s.rect(cx - pw / 2, -cu, pw, cu, "copper")
        opens = [(cx - 0.225, cx + 0.225)] if kind == "nsmd" else [(cx - 0.175, cx + 0.175)]
        lpi(s, cx - 0.5, cx + 0.5, 0, -1, pads=[(cx - pw / 2, cx + pw / 2, cu)], opens=opens, t=t, cu=cu)
        # the ball, collapsed between the two pads
        yb, yt = -cu, -cu - gap
        wb = pw / 2 if kind == "nsmd" else 0.175
        wt, wm = 0.2, 0.25
        pts = []
        n = 40
        for j in range(n + 1):
            u = j / n
            y = yb + (yt - yb) * u
            w = wb + (wt - wb) * u + (wm - (wb + wt) / 2) * math.sin(math.pi * u)
            pts.append((cx + w, y))
        left = [(2 * cx - x, y) for x, y in reversed(pts)]
        poly(s, pts + left, "solder")
        if kind == "nsmd":                                           # solder wraps the pad's sides
            for sg in (-1, 1):
                poly(s, [(cx + sg * (pw / 2 - 0.01), -cu - 0.01), (cx + sg * (pw / 2 + 0.045), 0), (cx + sg * pw / 2, 0)], "solder")
            s.rect(cx - pw / 2, -cu, pw, cu, "copper")
        # the package above: laminate, its pad and its mask
        s.rect(cx - 0.5, yt - cu - 0.18, 1.0, 0.18, "part")
        s.rect(cx - 0.2, yt - cu, 0.4, cu, "copper")
        s.text(["✓ Copper-defined (NSMD)", "Mask-defined (SMD)"][k], cx, yt - 0.33, size=14, anchor="middle",
               weight="600")
        s.text(["Usual choice", "Only where the BGA maker calls for it"][k], cx, 0.43, size=12, cls="muted",
               anchor="middle")
    s.dim_h(0.5 - 0.175, 0.5 + 0.175, 0.12, "0.35 pad", text_above=False)
    s.balloon(1, (0.5 + 0.2, -0.025), (s.X(0.5) + 150, s.Y(0.31)), "Mask kept clear of the pad")
    s.balloon(2, (0.5 - 0.19, -0.012), (s.X(0.5) - 150, s.Y(0.31)), "Solder wraps the pad's side", "Anchors the joint")
    s.balloon(3, (1.55 + 0.195, -0.04), (s.X(1.55) + 150, s.Y(0.31)), "Mask over the pad's edge", "Sets the opening")
    s.balloon(4, (1.55 - 0.17, -0.06), (s.X(1.55) - 150, s.Y(0.31)), "Notch where mask meets solder",
              "Where cracks can start")
    y = foot(s, s.Y(0.43) + 50 * f, [
        "Enlarged, drawn to scale. A 0.8 mm-pitch BGA, with example sizes.",
        "Follow the BGA maker's land pattern where it gives one."],
        legend=[("copper", "Copper"), ("bare", "FR4"), ("mask-on-cu", "Mask over copper"),
                ("mask-on-fr4", "Mask over FR4"), ("solder", "Solder")])
    return s, y


def router_corners():
    s = fit(_router_corners, 980, 760)
    s.save(out(51, "router-corners"))


def _router_corners(W, H):
    # D51 (PCB-DFM-042): what a router bit leaves: inside-corner radius, slot width, and corner relief for a square part.
    s = Sheet(W, H, "Allowing for the router: inside corners, slots and corner relief",
              "Drawn to scale, plan view of part of a board. Left: a 10 by 6 mm cut-out routed with a 2 mm bit; every "
              "inside corner has a 1 mm radius, the bit's own, and a 2 mm circle shows the bit in one corner. Middle: "
              "a slot 1 mm wide with round ends. Right: a cut-out for a square part 8 by 6 mm, with a round relief "
              "drilled into each corner so the part's square corners fit.",
              scale=30, ox=40, oy=80)
    f = s.f
    s.rect(0, 0, 30, 10, "mask-on-fr4")
    s.rect(2, 2, 10, 6, "bg", rx=1.0)                          # cut-out, 1 mm inside radius
    s.circle(3.0, 3.0, 1.0, "ray")                           # the 2 mm bit, in a corner
    s.rect(15, 2, 1.0, 6, "bg", rx=0.5)                          # 1 mm slot
    s.rect(20, 2, 8, 6, "bg")                                    # square cut-out ...
    for x, y in ((20, 2), (28, 2), (20, 8), (28, 8)):            # ... with corner reliefs, 1 mm bit
        ox = 0.35 if x == 20 else -0.35
        oy = 0.35 if y == 2 else -0.35
        s.circle(x + ox, y + oy, 0.6, "bg")
    s.rect(20, 2, 8, 6, "asm")                                   # the square part's outline
    s.text("Cut-out, 2 mm bit", s.X(7), s.Y(-0.6), size=13, anchor="middle", weight="600", px=True)
    s.text("Slot", s.X(15.5), s.Y(-0.6), size=13, anchor="middle", weight="600", px=True)
    s.text("Square part: corner relief", s.X(24), s.Y(-0.6), size=13, anchor="middle", weight="600", px=True)
    s.dim_h(15, 16, 9.0, "1.0", ext_from=8.0)
    s.dim_h(2, 12, 9.0, "10", ext_from=8.0)
    s.balloon(1, (2.29, 2.29), (s.X(0.5), s.Y(12.4)), "Inside corner radius 1 mm", "The radius of a 2 mm router bit")
    s.balloon(2, (3.0, 3.7), (s.X(6), s.Y(12.4)), "The router bit, 2 mm", "Can't reach further into the corner")
    s.balloon(3, (15.5, 5), (s.X(15.5), s.Y(12.4)), "Slot at least 1 mm wide", "Round ends, the bit's radius")
    s.balloon(4, (20.1, 2.1), (s.X(21), s.Y(12.4)), "Relief in each corner", "The part's square corner fits")
    s.balloon(5, (28, 5), (s.X(28), s.Y(12.4)), "Square part's outline")
    y = foot(s, s.Y(12.4) + 50 * f, [
        "Drawn to scale. Dimensions in mm.",
        "A 1 mm bit leaves a 0.5 mm radius, on request. Routed edges hold about ±0.1 mm."],
        legend=[("mask-on-fr4", "Board (mask over FR4)"), ("bg", "Cut away")])
    return s, y


def gold_fingers():
    s = fit(_gold_fingers, 980, 1000)
    s.save(out(52, "gold-fingers"))


def _gold_fingers(W, H):
    # D52 (PCB-DFM-038): edge-connector fingers: hard gold, mask cleared, chamfered corners; side view of the bevel.
    s = Sheet(W, H, "Edge-connector fingers: hard gold, no mask, a bevel",
              "Drawn to scale. Top: plan view of the edge of a board with six gold fingers on a 2.54 mm pitch, 1.5 mm "
              "wide and 7 mm long, ending 0.6 mm short of the edge. The solder mask is cleared from the whole finger "
              "area and the board corners beside the fingers are chamfered. Bottom: side view of the edge of a "
              "1.6 mm board, beveled at 30 degrees on both faces over the last 0.5 mm, with the gold fingers stopping "
              "0.6 mm from the edge, before the bevel.",
              scale=28, ox=110, oy=90)
    f = s.f
    W, L = 24.0, 11.0                                          # board window: edge at y = L
    pts = [(0, 0), (W, 0), (W, L - 1.5), (W - 1.5, L), (1.5, L), (0, L - 1.5)]
    poly(s, pts, "mask-on-fr4")
    x0 = (W - 5 * 2.54 - 1.5) / 2
    s.rect(x0 - 1.0, L - 8.6, 5 * 2.54 + 3.5, 8.6, "fr4-exposed")   # mask cleared over the finger area
    poly(s, [(x0 - 1.0, L), (x0 - 1.0, L - 8.6), (x0 + 5 * 2.54 + 2.5, L - 8.6), (x0 + 5 * 2.54 + 2.5, L)],
         "fr4-exposed")
    for i in range(6):
        s.rect(x0 + i * 2.54, L - 7.6, 1.5, 7.0, "cu-exposed", rx=0.2)
    s.text("Plan view of the edge", s.X(W / 2), s.Y(-0.6), size=13, anchor="middle", weight="600", px=True)
    s.dim_h(x0, x0 + 1.5, L + 1.0, "1.5", ext_from=L - 0.6)
    s.dim_h(x0 + 2.54, x0 + 2.54 + 2.54, L + 1.0, "2.54 pitch", ext_from=L - 0.6)
    # side view, enlarged 2.5x
    k = 2.5
    sx, sy = 2.0, 16.0
    T, B, G = 1.6, 0.5, 0.6                                       # thickness, bevel length, finger-to-edge gap
    tb = math.tan(math.radians(30)) * B                          # thickness removed each side
    E = 4.0                                                      # length of board shown, edge at sx + E*k
    side = [(sx, sy), (sx + (E - B) * k, sy), (sx + E * k, sy + tb * k), (sx + E * k, sy + (T - tb) * k),
            (sx + (E - B) * k, sy + T * k), (sx, sy + T * k)]
    poly(s, side, "fr4-exposed")
    s.rect(sx, sy - 0.05 * k, (E - G) * k, 0.05 * k, "cu-exposed")
    s.rect(sx, sy + T * k, (E - G) * k, 0.05 * k, "cu-exposed")
    s.text("Side view of the edge, enlarged 2.5×", s.X(sx + E * k / 2), s.Y(sy - 1.0), size=13, anchor="middle",
           weight="600", px=True)
    s.text("30°", s.X(sx + E * k) + 6, s.Y(sy + tb * k) + 16, size=12, cls="dimtxt", px=True)
    s.dim_v(sy, sy + T * k, sx + E * k + 2.0, "1.6", ext_from=sx + E * k)
    s.balloon(1, (x0 + 0.75, L - 4), (s.X(x0) - 70, s.Y(L - 4)), "Hard gold finger", "Over nickel; see Typical values")
    s.balloon(2, (x0 + 1.9, L - 6), (s.X(x0) - 70, s.Y(L - 7.6)), "No mask over the finger area")
    s.balloon(3, (W - 0.6, L - 0.6), (s.X(W) + 40, s.Y(L - 3)), "Corners chamfered")
    s.balloon(4, (sx + (E - B / 2) * k, sy + tb * k / 2), (s.X(sx + E * k + 3.6), s.Y(sy - 0.5)), "Bevel, 30° here",
              "0.5 mm long in this example")
    s.balloon(5, (sx + (E - G) * k - 0.2, sy - 0.025 * k), (s.X(sx) - 30, s.Y(sy - 0.5)), "Finger stops short of the edge",
              "0.6 mm here, clear of the bevel")
    yk = s.key(620, s.Y(sy - 1.0), width=330)
    y = s.Y(sy + T * k) + 60 * f
    for cls, label in (("cu-exposed", "Hard gold over copper"), ("fr4-exposed", "Exposed FR4"),
                       ("mask-on-fr4", "Mask over FR4")):
        swatches(s, 40, y, [(cls, label)])
        y += 24 * f
    y = max(y, yk) + 20 * f
    s.note("Drawn to scale, with the side view enlarged 2.5×. Example sizes.", 40, y)
    s.note("Bevel 30° or 45°, 0.5 to 1.0 mm deep. Ask your fab.", 40, y + 20 * f)
    return s, y + 20 * f


def npth_mask():
    s = fit(_npth_mask, 980, 700)
    s.save(out(53, "npth-mask"))


def _npth_mask(W, H):
    # D53 (PCB-DFM-034): solder mask clearance round a non-plated mounting hole.
    s = Sheet(W, H, "Solder mask round a non-plated hole: clear by 0.1 mm, or a ring that gets drilled",
              "Drawn to scale, plan views of a 3.2 mm non-plated mounting hole. Left, right: the mask opening is "
              "0.1 mm larger than the hole all round, so a thin ring of bare board shows and the drill never touches "
              "the mask. Right, wrong: the opening is only 0.025 mm larger than the hole; with the drill 0.08 mm off "
              "center, the drill cuts into the mask on one side and leaves chipped, flaking mask at the hole's edge.",
              scale=80, ox=60, oy=110)
    f = s.f
    R = 1.6
    for k, (title, ro, off) in enumerate((("✓ Mask cleared by 0.1 mm", R + 0.1, 0.0),
                                          ("✗ Mask opening a hair bigger than the hole", R + 0.025, 0.08))):
        cx, cy = 2.2 + k * 5.4, 2.2
        s.rect(cx - 2.2, cy - 2.2, 4.4, 4.4, "mask-on-fr4")
        s.circle(cx, cy, ro, "fr4-exposed")
        s.circle(cx + off, cy, R, "drill")
        if off:
            import random
            rnd = random.Random(3)
            for j in range(9):                                   # chips of mask torn off at the edge
                a = math.radians(-60 + j * 15)
                r0 = R - 0.02 - rnd.random() * 0.05
                x, y = cx + off + r0 * math.cos(a), cy + r0 * math.sin(a)
                poly(s, [(x, y), (x + 0.05, y + 0.02), (x + 0.02, y + 0.06)], "mask-on-fr4")
        s.text(title, s.X(cx), s.Y(-0.4), size=14, anchor="middle", weight="600", px=True)
    s.dim_h(2.2 + R, 2.2 + R + 0.1, 2.2 + 2.5, "0.1", ext_from=2.2)
    s.balloon(1, (2.2 - R - 0.05, 2.2), (s.X(0.3), s.Y(4.85)), "Ring of bare board, 0.1 mm",
              "The drill never reaches the mask")
    s.balloon(2, (7.6 + 0.08 + R - 0.05, 2.2 - 0.3), (s.X(9.5), s.Y(4.85)), "Mask drilled into",
              "Chips and flakes at the hole's edge")
    y = foot(s, s.Y(4.85) + 50 * f, [
        "Drawn to scale. A 3.2 mm hole, with the drill 0.08 mm off center on the right."], x0=60,
        legend=[("mask-on-fr4", "Mask over FR4"), ("fr4-exposed", "Exposed FR4"), ("drill", "Hole")])
    return s, y


def dam_room():
    s = fit(_dam_room, 980, 680)
    s.save(out(54, "dam-room"))


def _dam_room(W, H):
    # D54 (PCB-DFM-035): a mask dam needs room; what happens when the pads leave none.
    s = Sheet(W, H, "A mask dam needs room between the pads",
              "Enlarged and drawn to scale, plan views of three pads of a 0.4 mm-pitch part. Left, wrong: pads 0.25 mm "
              "wide leave 0.15 mm between them; with mask openings 0.05 mm larger on each side, only 0.05 mm of mask "
              "would be left, too thin to hold. Middle, wrong: the fab's quick fix, one opening round all the pads, "
              "with no dam at all. Right, right: pads 0.2 mm wide leave room for a 0.1 mm dam; this is also what the "
              "fab trims your pads to if you draw them too wide.",
              scale=210, ox=60, oy=130)
    f = s.f
    P, L, M = 0.4, 0.8, 0.05
    cases = [("drawn", 0.25, "✗ As drawn: no room for a dam"), ("gang", 0.25, "✗ Dam removed"),
             ("room", 0.2, "✓ Room for a 0.1 mm dam")]
    for k, (kind, w, title) in enumerate(cases):
        dx = k * 1.45

        def geom(add, cu, fr4, dx=dx, w=w):
            add(s.R(dx - 0.1, -0.15, 1.3, L + 0.3, fr4))
            for i in range(3):
                add(s.R(dx + 0.1 + i * P - w / 2 + 0.125, 0, w, L, cu))
        if kind == "gang":
            openings = [s.R(dx + 0.1 + 0.125 - w / 2 - M, -M, 2 * P + w + 2 * M, L + 2 * M, "bg")]
        else:
            openings = [s.R(dx + 0.1 + i * P - w / 2 + 0.125 - M, -M, w + 2 * M, L + 2 * M, "bg") for i in range(3)]
        s.board_view((dx - 0.1, -0.15, 1.3, L + 0.3), geom, openings)
        s.text(title, s.X(dx + 0.55), s.Y(-0.3), size=13, anchor="middle", weight="600", px=True)
    x0 = 0.1 + 0.125
    s.dim_h(x0 + 0.125 + M, x0 + P - 0.125 - M, L + 0.35, "0.05", ext_from=L)
    x2 = 2 * 1.45 + 0.1 + 0.125
    s.dim_h(x2 + 0.1 + M, x2 + P - 0.1 - M, L + 0.35, "0.1 dam", ext_from=L, text_side="left")
    s.balloon(1, (x0 + 0.6, 0.4), (s.X(x0 + 0.6), s.Y(1.42)), "A dam only 0.05 mm wide", "Too thin to hold; it flakes off")
    s.balloon(2, (1.45 + x0 + 0.2, 0.4), (s.X(1.45 + 0.6), s.Y(1.42)), "One opening, no dam",
              "Solder bridges from pad to pad")
    s.balloon(3, (x2 + 0.6, 0.4), (s.X(x2 + 0.6), s.Y(1.42)), "Pads 0.2 mm wide, 0.1 mm dam",
              "Design it this way, or the fab trims your pads to it")
    y = foot(s, s.Y(1.42) + 50 * f, [
        "Enlarged, to scale. 0.4 mm pitch, with mask openings 0.05 mm larger than the pads.",
        "Make the dam at least 0.1 mm wide (PCB-DFA-032)."], x0=60,
        legend=[("cu-exposed", "Exposed copper"), ("fr4-exposed", "Exposed FR4"), ("mask-on-fr4", "Mask over FR4")])
    return s, y


def bga_pour():
    s = fit(_bga_pour, 980, 820)
    s.save(out(55, "bga-pour"))


def _bga_pour(W, H):
    # D55 (PCB-DFA-082): BGA pads straight in a pour vs joined by a short trace.
    s = Sheet(W, H, "BGA pads in a copper pour: straight in, or joined by a short trace",
              "Drawn to scale, plan views of the corner of a 0.8 mm-pitch BGA with 0.35 mm pads and mask openings "
              "0.45 mm across, on a ground pour. Left, wrong: three ground pads sit straight in the pour, so the whole "
              "0.45 mm opening shows copper and those pads come out bigger than the rest. Right, right: the pour is "
              "kept back from every pad, and each ground pad is joined to it by a 0.15 mm trace, so all the pads "
              "show the same 0.35 mm of copper.",
              scale=125, ox=70, oy=120)
    f = s.f
    P, r, ro, clr = 0.8, 0.175, 0.225, 0.2
    gnd = {(0, 0), (1, 0), (0, 1)}
    for k, (kind, title) in enumerate((("in", "✗ Ground pads straight in the pour"),
                                       ("trace", "✓ Ground pads joined by a short trace"))):
        dx = k * 3.9
        pads = [(dx + 0.6 + i * P, 0.6 + j * P, (i, j)) for i in range(3) for j in range(3)]

        def geom(add, cu, fr4, dx=dx, kind=kind, pads=pads):
            add(s.R(dx, 0, 3.0, 3.0, cu))                       # the ground pour
            for x, y, ij in pads:
                if kind == "trace" or ij not in gnd:
                    add(s.C(x, y, r + clr, fr4))                # clearance round the pad
            for x, y, ij in pads:
                add(s.C(x, y, r, cu))
                if kind == "trace" and ij in gnd:
                    add(s.R(x - r - clr - 0.05, y - 0.075, r + clr + 0.05, 0.15, cu))
        openings = [s.C(x, y, ro, "bg") for x, y, _ in pads]
        s.board_view((dx, 0, 3.0, 3.0), geom, openings)
        s.text(title, s.X(dx + 1.5), s.Y(-0.3), size=13, anchor="middle", weight="600", px=True)
    s.balloon(1, (0.6 + 0.2, 0.6), (s.X(0.3), s.Y(3.35)), "Ground pad in the pour",
              "The 0.45 mm opening sets its size")
    s.balloon(2, (0.6 + 2 * P, 0.6 + 2 * P + 0.1), (s.X(2.2), s.Y(3.35)), "Pad on its own: 0.35 mm of copper")
    s.balloon(3, (3.9 + 0.6 - 0.32, 0.6), (s.X(4.4), s.Y(3.35)), "Short trace to the pour", "0.15 mm wide")
    s.balloon(4, (3.9 + 0.6 + 0.2, 0.6 + P), (s.X(6.3), s.Y(3.35)), "Every pad the same size")
    y = foot(s, s.Y(3.35) + 50 * f, [
        "Drawn to scale. 0.8 mm pitch, 0.35 mm pads, 0.45 mm mask openings and 0.2 mm pour clearance.",
        "The same applies to QFN and DFN pads."], x0=70,
        legend=[("cu-exposed", "Exposed copper"), ("fr4-exposed", "Exposed FR4"),
                ("mask-on-cu", "Mask over copper"), ("mask-on-fr4", "Mask over FR4")])
    return s, y

# ---- Legend (silkscreen), D68-D70
TXT = 1.0          # legend text height, mm (PCB-DFM-039)


def silk_text(s, txt, x, y, rot=0, h=TXT, parent=None):
    """Legend text h mm tall (cap height), centered on (x, y) mm, turned rot degrees (-90 reads from the right edge)."""
    X, Y = s.X(x), s.Y(y)
    t = dw.Text(txt, s.L(h / 0.72), X, Y + s.L(h) / 2, text_anchor="middle", class_="silkscreen",
                transform=f"rotate({rot},{X},{Y})" if rot else None)
    (parent if parent is not None else s.d).append(t)


def silk_box(s, x, y, w, h, lw=0.15):
    s.d.append(s.PL([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], "s-silkscreen", lw))


def legend_vias():
    s = fit(_legend_vias, 1000, 990)
    s.save(out(68, "legend-over-vias"))


def _legend_vias(W, H):
    # D68 (PCB-DFM-045): legend beside the vias, over tented vias, over open vias.
    s = Sheet(W, H, "Legend beside vias, over tented vias, and over open vias",
              "Drawn to scale. Three plan views of the same 0603 resistor, R7, with two vias joined to its pads and a "
              "third via between them. The designator is 1 mm tall. Left, recommended: the designator sits beside the "
              "part on flat solder mask, clear of the vias. Middle, acceptable when there is no other room: the "
              "designator is printed across tented vias; it prints, but the ink dips where the mask sags over each "
              "hole, so the characters come out slightly distorted and thinner over each via. Right, avoid: the vias are open, so the fab clips "
              "the legend about 0.1 mm back from their exposed copper and the designator is cut into pieces. Below, an "
              "enlarged cross-section at true scale of a legend line printed across a tented 0.3 mm via: the mask "
              "sags into the hole and the legend ink follows it down.",
              scale=56, ox=40, oy=80)
    f = s.f
    W, H = 5.0, 3.4
    vias = [(0.9, 2.45), (1.7, 2.45), (2.5, 2.45)]
    cases = [("beside", "✓ Beside the vias"), ("tent", "Over tented vias: only if there's no room"),
             ("open", "✗ Over open vias")]
    for i, (kind, title) in enumerate(cases):
        dx = i * (W + 0.9)

        def geom(add, cu, fr4, dx=dx):
            add(s.R(dx, 0, W, H, fr4))
            for px in (0.9, 2.5):
                add(s.R(dx + px - 0.45, 0.45, 0.9, 0.95, cu))
                add(s.R(dx + px - 0.125, 1.0, 0.25, 1.45, cu))
            add(s.R(dx + 1.7 - 0.125, 2.45, 0.25, H - 2.45, cu))
            for vx, vy in vias:
                add(s.C(dx + vx, vy, 0.3, cu))
        openings = [s.R(dx + px - 0.5, 0.4, 1.0, 1.05, "bg") for px in (0.9, 2.5)]
        if kind == "open":
            openings += [s.C(dx + vx, vy, 0.35, "bg") for vx, vy in vias]
        s.board_view((dx, 0, W, H), geom, openings, [(dx + vx, vy, 0.15) for vx, vy in vias])
        if kind == "beside":
            silk_text(s, "R7", dx + 3.95, 0.92)
        else:
            m = dw.Mask(id=f"clip68-{kind}")
            m.append(dw.Rectangle(s.X(dx), s.Y(0), s.L(W), s.L(H), fill="white"))
            if kind == "open":                       # the fab clips legend 0.1 mm back from exposed copper
                for vx, vy in vias:
                    m.append(dw.Circle(s.X(dx + vx), s.Y(vy), s.L(0.45), fill="black"))
            if kind == "tent":                       # crisp on flat mask, wavy and thinner where it dips into a via
                for vx, vy in vias:
                    m.append(dw.Circle(s.X(dx + vx), s.Y(vy), s.L(0.34), fill="black"))
            g = dw.Group(mask=m)
            silk_text(s, "R7", dx + 1.7, 2.45, parent=g)
            s.d.append(g)
            if kind == "tent":
                s.d.append(dw.Raw('<filter id="dip68" x="-10%" y="-10%" width="120%" height="120%">'
                                  '<feTurbulence type="fractalNoise" baseFrequency="0.09" numOctaves="2" seed="4"/>'
                                  '<feDisplacementMap in="SourceGraphic" scale="7" xChannelSelector="R" '
                                  'yChannelSelector="G"/></filter>'))
                m2 = dw.Mask(id="dip68-mask")
                for vx, vy in vias:
                    m2.append(dw.Circle(s.X(dx + vx), s.Y(vy), s.L(0.34), fill="white"))
                g2 = dw.Group(mask=m2)
                g3 = dw.Group(filter="url(#dip68)", opacity=0.8)
                silk_text(s, "R7", dx + 1.7, 2.45, parent=g3)
                g2.append(g3)
                s.d.append(g2)
        s.text(title, s.X(dx + W / 2), s.Y(-0.3), size=13.5, anchor="middle", weight="600", px=True)
    s.balloon(1, (3.95 + 0.2, 1.3), (s.X(4.15), s.Y(H + 0.7)), "Designator on flat mask", "Prints cleanly")
    s.balloon(2, (W + 0.9 + 1.7, 2.45 + 0.42), (s.X(W + 0.9 + 1.7), s.Y(H + 0.7)), "Over a tented via",
              "Prints, but the ink dips into each via")
    s.balloon(3, (2 * (W + 0.9) + 1.3, 2.9), (s.X(2 * (W + 0.9) + 1.3), s.Y(H + 0.7)),
              "Clipped back from an open via", "The fab removes legend near exposed copper")
    # Enlarged cross-section at true scale: a legend line across a tented via.
    sc, ox0 = 420, 70
    oy0 = s.Y(H + 0.7) + 50 * f + 0.2 * sc + 30 * f
    s.scale, s.ox, s.oy = sc, ox0, oy0
    cu, t, rd, pl, ink = 0.05, 0.025, 0.175, 0.025, 0.02
    cx, half, depth = 0.65, 0.65, 0.12
    s.rect(cx - half, 0, 2 * half, depth, "bare")
    s.rect(cx - rd, -cu, 2 * rd, depth + cu, "drill")
    s.rect(cx - rd, -cu, pl, depth + cu, "copper"); s.rect(cx + rd - pl, -cu, pl, depth + cu, "copper")
    s.rect(cx - 0.3, -cu, 0.3 - rd + pl, cu, "copper"); s.rect(cx + rd - pl, -cu, 0.3 - rd + pl, cu, "copper")
    r_in = rd - pl
    xs, top = lpi(s, cx - half, cx + half, 0, -1, pads=[(cx - 0.3, cx - r_in, cu), (cx + r_in, cx + 0.3, cu)],
                  holes=[(cx - r_in, cx + r_in)], t=t, cu=cu)
    a, b = cx - 0.55, cx + 0.55
    pts = [(x, y) for x, y in zip(xs, top) if a <= x <= b]
    poly(s, pts + [(x, y - ink) for x, y in reversed(pts)], "silkscreen")
    s.text("Enlarged, true scale: a legend line across a tented via", s.X(cx), s.Y(-0.2), size=13.5,
           anchor="middle", weight="600", px=True)
    s.balloon(4, (cx - 0.48, top[0] - 0.01), (s.X(cx - 0.48), s.Y(0.23)), "Legend ink on flat mask")
    s.balloon(5, (cx, min(y for x, y in pts if abs(x - cx) < 0.01) - 0.01), (s.X(cx), s.Y(0.23)),
              "Ink follows the mask down into the via", "So the character is slightly distorted")
    s.balloon(6, (cx + 0.24, -cu - 0.012), (s.X(cx + 0.3), s.Y(0.23)), "Solder mask tent over the via")
    s.balloon(7, (cx - 0.1, 0.09), (s.X(cx - 0.1), s.Y(0.23)), "Plated hole, 0.3 mm in diameter")
    y = foot(s, s.Y(0.23) + 50 * f, [
        "Drawn to scale. Vias 0.3 mm in diameter with 0.6 mm rings. Legend 1 mm tall.",
        "Enlarged view: copper about 50 µm, mask about 25 µm and legend ink about 20 µm (an example)."],
        legend=[("cu-exposed", "Exposed copper"), ("mask-on-cu", "Mask over copper"),
              ("mask-on-fr4", "Mask over FR4"), ("fr4-exposed", "Exposed FR4"), ("silkscreen", "Legend (silkscreen)"),
              ("drill", "Hole")])
    s.scale, s.ox, s.oy = 56, 40, 80
    return s, y


def _parts_board(s, dx, parts, W, H, traces=()):
    """A patch of board with chip parts. parts: (x, y, vertical, designator, rot, tx, ty)."""
    def geom(add, cu, fr4):
        add(s.R(dx, 0, W, H, fr4))
        for a in traces:
            add(s.PL([(dx + x, y) for x, y in a], "s-" + cu, 0.25))
        for x, y, v, *_ in parts:
            for k in (-1, 1):
                if v:
                    add(s.R(dx + x - 0.45, y + k * 0.8 - 0.475, 0.9, 0.95, cu))
                else:
                    add(s.R(dx + x + k * 0.8 - 0.45, y - 0.475, 0.9, 0.95, cu))
    ops = []
    for x, y, v, *_ in parts:
        for k in (-1, 1):
            if v:
                ops.append(s.R(dx + x - 0.5, y + k * 0.8 - 0.525, 1.0, 1.05, "bg"))
            else:
                ops.append(s.R(dx + x + k * 0.8 - 0.5, y - 0.525, 1.0, 1.05, "bg"))
    s.board_view((dx, 0, W, H), geom, ops)
    for x, y, v, ref, rot, tx, ty in parts:
        silk_text(s, ref, dx + tx, ty, rot)


def read_arrow(s, x, y, ang, label):
    """An eye-side arrow pointing at the board: the edge a reader stands at (px, ang in degrees)."""
    a = math.radians(ang)
    L = 34 * s.f
    x0, y0 = x - L * math.cos(a), y - L * math.sin(a)
    s.d.append(dw.Line(x0, y0, x - 7 * s.f * math.cos(a), y - 7 * s.f * math.sin(a), class_="dim"))
    s._arrowhead(x, y, a)
    s.d.append(dw.Text(label, s.fs(12), x0 - 4 * math.cos(a), y0 - 4 * math.sin(a) + 4,
                       text_anchor="middle" if abs(math.cos(a)) < 0.5 else ("end" if math.cos(a) > 0 else "start"),
                       class_="dimtxt"))


def legend_orientation():
    s = fit(_legend_orientation, 1040, 760)
    s.save(out(69, "legend-orientation"))


def _legend_orientation(W, H):
    # D69 (PCB-DFA-127): designators read from two edges of the board, not four.
    s = Sheet(W, H, "Designators that read from two edges of the board, not four",
              "Drawn to scale. Two copies of the same small area of a board with eight 0603 resistors and capacitors, "
              "some placed horizontally and some vertically, with designators 1 mm tall. Left, recommended: every "
              "horizontal designator reads left to right from the bottom edge, and every vertical designator reads "
              "bottom to top, from the right edge, so a person only ever holds the board one of two ways. Right, "
              "avoid: the designators are turned every way, some upside down and some reading top to bottom, so the "
              "board has to be turned to all four sides to read them.",
              scale=30, ox=40, oy=130)
    f = s.f
    W, H = 13.0, 11.6
    # (x, y, vertical, designator, rotation, text x, text y) for the good and bad layouts
    base = [(2.4, 2.0, False, "R1"), (6.4, 2.0, False, "R2"), (10.6, 2.6, True, "C1"), (2.0, 6.2, True, "C2"),
            (6.4, 5.6, False, "R3"), (10.6, 7.6, True, "C3"), (4.6, 9.2, False, "R4"), (8.2, 9.2, False, "C4")]
    good, bad = [], []
    bad_rot = {"R1": 0, "R2": 180, "C1": 90, "C2": -90, "R3": 180, "C3": 90, "R4": 0, "C4": 180}
    for x, y, v, ref in base:
        if v:
            good.append((x, y, v, ref, -90, x + 1.25, y))
            bad.append((x, y, v, ref, bad_rot[ref], x + 1.25 if bad_rot[ref] == -90 else x - 1.25, y))
        else:
            good.append((x, y, v, ref, 0, x, y - 1.3))
            bad.append((x, y, v, ref, bad_rot[ref], x, y - 1.3 if bad_rot[ref] == 0 else y + 1.3))
    traces = [[(3.2, 2.0), (5.6, 2.0)], [(7.2, 2.0), (9.3, 2.0), (10.6, 0.7), (10.6, 1.8)],
              [(2.0, 7.2), (2.0, 9.2), (3.8, 9.2)], [(7.2, 5.6), (9.0, 5.6), (10.6, 7.2 - 0.4)],
              [(5.4, 9.2), (7.4, 9.2)]]
    for k, (parts, title) in enumerate(((good, "✓ Two reading directions"), (bad, "✗ Four reading directions"))):
        dx = k * (W + 4.0)
        _parts_board(s, dx, parts, W, H, traces)
        s.text(title, s.X(dx + W / 2), s.Y(-2.3), size=14, anchor="middle", weight="600", px=True)
        s.d.append(dw.Rectangle(s.X(dx), s.Y(0), s.L(W), s.L(H), class_="edge"))
        read_arrow(s, s.X(dx + 3.5), s.Y(H) + 8 * f, -90, "")
        read_arrow(s, s.X(dx + W) + 8 * f, s.Y(4.6), 180, "")
        if k == 1:
            read_arrow(s, s.X(dx + 3.5), s.Y(0) - 8 * f, 90, "")
            read_arrow(s, s.X(dx) - 8 * f, s.Y(4.6), 0, "")
    s.balloon(1, (6.4 - 0.5, 0.7), (s.X(5.0), s.Y(-1.1)), "Horizontal designators read left to right",
              "From the bottom edge")
    s.balloon(2, (10.6 + 1.25, 2.6 + 0.6), (s.X(12.2), s.Y(-1.1)), "Vertical designators all read bottom to top",
              "From the right edge, a quarter turn")
    s.balloon(3, (W + 4.0 + 6.4, 3.3 - 0.2), (s.X(W + 4.0 + 6.4), s.Y(-1.1)), "Upside down",
              "A half turn to read")
    s.balloon(4, (W + 4.0 + 10.6 - 1.25, 2.6 - 0.3), (s.X(W + 4.0 + 9.35), s.Y(-1.1)), "Reads top to bottom",
              "A three-quarter turn to read")
    y = foot(s, s.Y(H) + 34 * f + 50 * f, [
        "Drawn to scale. 0603 parts, designators 1 mm tall.",
        "The blue arrows show the edges a person reads from."], x0=50,
        legend=[("cu-exposed", "Exposed copper"), ("mask-on-cu", "Mask over copper"),
                ("mask-on-fr4", "Mask over FR4"), ("silkscreen", "Legend (silkscreen)")])
    return s, y


def legend_callout():
    s = fit(_legend_callout, 1000, 920)
    s.save(out(70, "legend-callout-box"))


def _legend_callout(W, H):
    # D70 (PCB-DFA-128): a callout box for parts packed too tightly for their designators.
    s = Sheet(W, H, "A callout box for parts packed too tightly for their designators",
              "Drawn to scale. A QFN, U3, with eight 0402 capacitors packed tightly beside it, 0.25 mm apart, so "
              "there is no room for a designator beside each one. A legend box is drawn round the group of "
              "capacitors. Next to it, a second, larger legend box acts as a map: it holds the eight designators, C11 "
              "to C18, each in the same position and turned the same way as its capacitor in the group, so a person "
              "matches each designator to its part by position. A straight legend line joins the two boxes. All of "
              "it is drawn in the legend.",
              scale=46, ox=70, oy=120)
    f = s.f
    W, H = 19.6, 10.0
    # QFN-24 4 x 4 mm, 0.5 mm pitch, centered at (4.0, 5.0)
    qx, qy = 4.0, 5.0
    caps = []                                  # (x, y, vertical, designator)
    for i in range(4):                         # top row: vertical caps, 0.9 mm pitch
        caps.append((8.0 + i * 0.9, 3.8, True, f"C{11 + i}"))
    for i in range(2):                         # bottom: two columns of horizontal caps
        for j in range(2):
            caps.append((8.55 + i * 1.8, 5.9 + j * 0.85, False, f"C{15 + 2 * i + j}"))
    pw, pl, pp = 0.55, 0.5, 0.5                 # 0402 pads, pad centers 0.5 mm from the part center

    def cap_pads(x, y, v):
        return [(x - pw / 2, y + k * pp - pl / 2, pw, pl) if v else (x + k * pp - pl / 2, y - pw / 2, pl, pw)
                for k in (-1, 1)]

    qpads = []
    for i in range(6):
        o = -1.25 + i * 0.5
        qpads += [(qx - 2.0 - 0.1, qy + o - 0.125, 0.7, 0.25), (qx + 2.0 - 0.6, qy + o - 0.125, 0.7, 0.25),
                  (qx + o - 0.125, qy - 2.0 - 0.1, 0.25, 0.7), (qx + o - 0.125, qy + 2.0 - 0.6, 0.25, 0.7)]

    def geom(add, cu, fr4):
        add(s.R(0, 0, W, H, fr4))
        add(s.PL([(qx + 2.1, 4.25), (7.75, 4.25)], "s-" + cu, 0.2))
        add(s.PL([(qx + 2.1, 5.75), (7.6, 5.75), (7.75, 5.9)], "s-" + cu, 0.2))
        add(s.R(qx - 1.35, qy - 1.35, 2.7, 2.7, cu))
        for p in qpads:
            add(s.R(*p, cu))
        for x, y, v, _ in caps:
            for p in cap_pads(x, y, v):
                add(s.R(*p, cu))
    ops = [s.R(qx - 1.4, qy - 1.4, 2.8, 2.8, "bg")] + [s.R(a - 0.05, b - 0.05, c + 0.1, d + 0.1, "bg")
                                                         for a, b, c, d in qpads]
    for x, y, v, _ in caps:
        ops += [s.R(a - 0.05, b - 0.05, c + 0.1, d + 0.1, "bg") for a, b, c, d in cap_pads(x, y, v)]
    s.board_view((0, 0, W, H), geom, ops)
    s.d.append(dw.Rectangle(s.X(0), s.Y(0), s.L(W), s.L(H), class_="edge"))
    # the parts, placed: QFN body and 0402 capacitors (1.0 by 0.5 mm, 0.25 mm terminations)
    s.rect(qx - 2.0, qy - 2.0, 4.0, 4.0, "part")
    s.circle(qx - 1.5, qy - 1.5, 0.15, "term")
    for x, y, v, _ in caps:
        if v:
            s.rect(x - 0.25, y - 0.5, 0.5, 1.0, "capbody")
            s.rect(x - 0.25, y - 0.5, 0.5, 0.25, "capterm"); s.rect(x - 0.25, y + 0.25, 0.5, 0.25, "capterm")
        else:
            s.rect(x - 0.5, y - 0.25, 1.0, 0.5, "capbody")
            s.rect(x - 0.5, y - 0.25, 0.25, 0.5, "capterm"); s.rect(x + 0.25, y - 0.25, 0.25, 0.5, "capterm")
    # QFN outline, pin 1 dot and designator
    for a, b in (((qx - 2.4, qy - 2.4), (qx - 1.7, qy - 2.4)), ((qx + 1.7, qy - 2.4), (qx + 2.4, qy - 2.4)),
                 ((qx - 2.4, qy + 2.4), (qx - 1.7, qy + 2.4)), ((qx + 1.7, qy + 2.4), (qx + 2.4, qy + 2.4))):
        s.d.append(s.PL([a, b], "s-silkscreen", 0.15))
    for a, b in (((qx - 2.4, qy - 2.4), (qx - 2.4, qy - 1.7)), ((qx + 2.4, qy - 2.4), (qx + 2.4, qy - 1.7)),
                 ((qx - 2.4, qy + 2.4), (qx - 2.4, qy + 1.7)), ((qx + 2.4, qy + 2.4), (qx + 2.4, qy + 1.7))):
        s.d.append(s.PL([a, b], "s-silkscreen", 0.15))
    s.circle(qx - 2.75, qy - 2.75, 0.18, "silkscreen")
    silk_text(s, "U3", qx, qy - 3.4)
    # the box round the group, then the map box
    gx0, gy0, gx1, gy1 = 7.3, 2.75, 11.35, 7.35
    silk_box(s, gx0, gy0, gx1 - gx0, gy1 - gy0)
    k, mx0, my0 = 1.65, 12.2, 1.2                # the map is the group enlarged by k
    silk_box(s, mx0, my0, k * (gx1 - gx0), k * (gy1 - gy0))
    for x, y, v, ref in caps:
        silk_text(s, ref, mx0 + k * (x - gx0), my0 + k * (y - gy0), -90 if v else 0)
    s.d.append(s.PL([(gx1, 5.0), (mx0, 5.0)], "s-silkscreen", 0.15))       # the line joining the two boxes
    s.balloon(1, (gx0 + 0.3, gy1), (s.X(gx0 + 0.3), s.Y(H + 1.1)), "Box round the tightly packed group",
              "Kept clear of the pads")
    s.balloon(2, (10.35, 6.75), (s.X(10.35), s.Y(H + 1.1)), "Capacitors 0.25 mm apart",
              "No room for a designator beside each")
    s.balloon(4, (mx0 + 0.4, my0 + k * (gy1 - gy0)), (s.X(mx0 + 0.4), s.Y(H + 1.1)),
              "The callout box: a map of the group", "Enlarged, beside the group")
    s.balloon(5, (mx0 + k * (8.0 - gx0), my0 + k * (3.8 - gy0) - 0.9), (s.X(mx0 + k * (8.0 - gx0)), s.Y(-1.2)),
              "Each designator where its part is", "And turned the same way")
    s.balloon(3, ((gx1 + mx0) / 2, 5.0), (s.X((gx1 + mx0) / 2), s.Y(H + 1.1)), "A line joins the two boxes",
              "As straight as it can be")
    y = foot(s, s.Y(H + 1.1) + 50 * f, [
        "Drawn to scale. 0402 capacitors and a QFN-24, 4 by 4 mm. Designators 1 mm tall, legend lines 0.15 mm."],
        x0=70, legend=[("cu-exposed", "Exposed copper"), ("mask-on-cu", "Mask over copper"),
                       ("mask-on-fr4", "Mask over FR4"), ("silkscreen", "Legend (silkscreen)"), ("part", "Part body")])
    return s, y


if __name__ == "__main__":
    via_types()
    qfn_thermal_vias()
    aspect_annular()
    via_web()
    bga_pads()
    router_corners()
    gold_fingers()
    npth_mask()
    dam_room()
    bga_pour()
    legend_vias()
    legend_orientation()
    legend_callout()
    print("written to", OUT)

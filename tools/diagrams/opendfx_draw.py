"""OpenDFX diagram style kit.

Every book diagram is drawn with these helpers so they share one look: drawing-sheet
style, true scale in millimeters, numbered balloons with a key, and real dimension
lines. Output is SVG with real text, a <title> and <desc>, and light/dark colors.
"""
import math
import re
from pathlib import Path
import drawsvg as dw

from embed_fonts import FONT_STACK, embed_file

# The diagram number of the drawing being saved, set by each script's out(); used for the corner label.
CURRENT_D = None
_RECS = None


def _recs_for(n):
    """Recommendation IDs for diagram n, read from the README table."""
    global _RECS
    if _RECS is None:
        _RECS = {}
        for line in (Path(__file__).with_name("README.md")).read_text().splitlines():
            m = re.match(r"\| D(\d+)(?:\u2013D(\d+))? \|(.*)", line)
            if m:
                ids = list(dict.fromkeys(re.findall(r"PCB-DF[AMT]-\d{3}", m.group(3))))
                for k in range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1):
                    _RECS[k] = ids
    return _RECS.get(n, [])

# Atkinson Hyperlegible Next (FONT1, Q182), embedded in every drawing by embed_fonts.py when it is saved.
FONT = FONT_STACK

# Print sizes (DRW1, Q172 and Q174). A drawing is printed at the print version's text width, or its height limit,
# whichever is smaller. Text and lines are sized in points at that size, so they are never smaller than 7 pt and
# 0.75 pt (KDP's minimums), and a little larger where there is room. The scripts still give sizes in drawing
# units as they were designed; text_pt() and line_pt() turn those into points.
PT_MM = 25.4 / 72
PAGE = {"portrait": (175.9, 200.0),     # the print text width; a figure is at most 200 mm tall
        "landscape": (231.4, 150.0)}    # turned sideways on a page of its own, with room for the caption
TEXT_MIN_PT = 7.0
LINE_MIN_PT = 0.8                       # a little above KDP's 0.75 pt


def text_pt(size):
    """The printed size in points for a text size the scripts give in drawing units: 12 (a label) prints at 8.5 pt."""
    return max(TEXT_MIN_PT, 7.5 + (size - 10) * 0.5)


def line_pt(width):
    """The printed width in points for a stroke width given in drawing units: 0.9 (a leader) prints at 0.95 pt."""
    return max(LINE_MIN_PT, 0.8 + (width - 0.6) * 0.5)

# Color tokens. Light values first, then dark-mode overrides.
CSS = """
svg { font-family: %(font)s; }
.bg      { fill: #ffffff; }
.ink     { fill: #1d2125; }
.ink-s   { stroke: #1d2125; }
.muted   { fill: #5b636b; }
.thin    { stroke: #5b636b; stroke-width: 0.9; fill: none; }
.mask    { fill: #1e7a3e; }   /* mask over FR4, Chris's key */
.mask-lt { fill: #1e7a3e; }
.mask-lt-s { stroke: #1e7a3e; stroke-width: 1.2; fill: none; }
.waste   { fill: #1e7a3e; }   /* rails, tabs, frames: board material too */
.edge    { stroke: #1d2125; stroke-width: 1.4; fill: none; }
.copper  { fill: #d9b44a; }   /* exposed copper */
.bare    { fill: #9c7a4a; }   /* exposed FR4 */
.hole    { fill: #17191c; stroke: #17191c; stroke-width: 1.2; }
.score   { stroke: #b23a2b; stroke-width: 1.6; stroke-dasharray: 7 4; fill: none; }
.zone    { fill: #b23a2b; fill-opacity: 0.12; }
.zone-s  { stroke: #b23a2b; stroke-width: 0.9; stroke-dasharray: 3 3; fill: none; }
.keep    { fill: #2563a8; fill-opacity: 0.10; }
.keep-s  { stroke: #2563a8; stroke-width: 0.9; stroke-dasharray: 3 3; fill: none; }
.part    { fill: #3b3f45; }
.term    { fill: #c9ccd1; }
.balloon { fill: #ffffff; stroke: #1d2125; stroke-width: 1.2; }
.lead    { stroke: #1d2125; stroke-width: 0.9; fill: none; }
.dim     { stroke: #2563a8; stroke-width: 0.9; fill: none; }
.dimtxt  { fill: #2563a8; paint-order: stroke; stroke: #ffffff; stroke-width: 3px; stroke-linejoin: round; }
.arrow   { fill: #2563a8; }
.dot     { fill: #1d2125; }
.capbody { fill: #c8a878; stroke: #8a6d45; stroke-width: 0.6; }
.capterm { fill: #d9dde2; stroke: #8f969d; stroke-width: 0.6; }
.stub    { fill: #9aa69e; stroke: #3b4147; stroke-width: 0.8; }
.foil    { fill: #b9c0c7; stroke: #5b636b; stroke-width: 0.8; }
.paste   { fill: #bdbdb6; }   /* solder paste */
.wall    { stroke: #b23a2b; stroke-width: 2.4; fill: none; }
.shadow  { fill: #1d2125; fill-opacity: 0.12; }
.ray     { stroke: #b23a2b; stroke-width: 1.1; stroke-dasharray: 5 3; fill: none; }
.silk    { fill: #ffffff; }
.silk-s  { stroke: #ffffff; stroke-width: 2.2; fill: none; }
.outline { stroke: #e8eaed; stroke-width: 1.1; stroke-dasharray: 4 3; fill: none; }
.asm     { stroke: #1d2125; stroke-width: 1.2; stroke-dasharray: 6 3; fill: none; }
/* Board colors, from Chris's key (2026-11-05). A board looks the same in light and dark mode. */
.cu-exposed    { fill: #d9b44a; }
.fr4-exposed   { fill: #9c7a4a; }
.mask-on-cu    { fill: #2f9e4f; }
.mask-on-fr4   { fill: #1e7a3e; }
.silkscreen    { fill: #f2f2ef; }
.solder-paste  { fill: #bdbdb6; }
.drill         { fill: #17191c; }
.offboard      { fill: #3b4046; }
.contact       { fill: #e0392b; }
.adhesive      { fill: #8fb3d1; }
.s-part        { stroke: #3b3f45; fill: none; stroke-linecap: round; stroke-linejoin: round; }
.solder        { fill: #d0d4d8; stroke: #8f969d; stroke-width: 0.6; }
.s-cu-exposed, .s-fr4-exposed, .s-mask-on-cu, .s-mask-on-fr4, .s-silkscreen, .s-offboard, .s-foil, .s-foil-edge
               { fill: none; stroke-linecap: round; stroke-linejoin: round; }
.s-cu-exposed  { stroke: #d9b44a; }
.s-fr4-exposed { stroke: #9c7a4a; }
.s-mask-on-cu  { stroke: #2f9e4f; }
.s-mask-on-fr4 { stroke: #1e7a3e; }
.s-silkscreen  { stroke: #f2f2ef; }
.s-offboard    { stroke: #3b4046; }
.s-foil        { stroke: #b9c0c7; }
.s-foil-edge   { stroke: #5b636b; }
.enclosure     { fill: #26292d; }
.flux          { fill: #c8a24a; fill-opacity: 0.35; }
.figbox        { fill: none; stroke: #1d2125; stroke-width: 2; }
.ko-rec        { stroke: #f2f2ef; stroke-width: 1.6; stroke-dasharray: 7 4; fill: none; }
.ko-min        { stroke: #ff7a66; stroke-width: 1.6; stroke-dasharray: 3 3; fill: none; }
@media (prefers-color-scheme: dark) {
  .figbox { stroke: #e8eaed; }
  .enclosure { fill: #3d434a; }
  .bg      { fill: #16191c; }
  .ink     { fill: #e8eaed; }
  .ink-s   { stroke: #e8eaed; }
  .muted   { fill: #a3abb3; }
  .thin    { stroke: #a3abb3; }
  .edge    { stroke: #e8eaed; }
  .score   { stroke: #f08a7a; }
  .zone    { fill: #f08a7a; }
  .zone-s  { stroke: #f08a7a; }
  .keep    { fill: #79aef0; }
  .keep-s  { stroke: #79aef0; }
  .part    { fill: #c7cbd1; }
  .term    { fill: #6e747b; }
  .balloon { fill: #16191c; stroke: #e8eaed; }
  .lead    { stroke: #e8eaed; }
  .dim     { stroke: #79aef0; }
  .dimtxt  { fill: #79aef0; stroke: #16191c; }
  .arrow   { fill: #79aef0; }
  .dot     { fill: #e8eaed; }
  .capbody { fill: #a88a5e; stroke: #d8c3a0; }
  .capterm { fill: #9aa1a8; stroke: #d8dde2; }
  .stub    { fill: #5d6a62; stroke: #c7cbd1; }
  .foil    { fill: #5b636b; stroke: #a3abb3; }
  .wall    { stroke: #f08a7a; }
  .shadow  { fill: #e8eaed; fill-opacity: 0.14; }
  .ray     { stroke: #f08a7a; }
  .asm     { stroke: #e8eaed; }
}
""" % {"font": FONT}


class Sheet:
    """A drawing sheet. Geometry is given in mm and placed at `scale` px per mm,
    offset by (ox, oy) px. Labels and the key are laid out in px."""

    def __init__(self, width, height, title, desc, scale=1.0, ox=0, oy=0, page="portrait"):
        self.scale, self.ox, self.oy = scale, ox, oy
        self.width, self.height = width, height
        self.page = page
        pw, ph = PAGE[page]
        self.mm_per_unit = min(pw / width, ph / (height + 40))      # 40: the band with the D-number
        self.f = self.fs(12) / 12               # how much the furniture (balloons, key rows, arrowheads) grows
        self.d = dw.Drawing(width, height, role="img", aria_labelledby="title desc")
        self.d.append(dw.Raw(f'<title id="title">{title}</title><desc id="desc">{desc}</desc>'))
        self.d.append(dw.Raw(f"<style>{self.css()}</style>"))
        self.d.append(dw.Rectangle(0, 0, width, height, class_="bg"))
        self.balloons = []
        self._pending = []

    # print sizes
    def u(self, pt):
        """Points at print size -> drawing units."""
        return pt * PT_MM / self.mm_per_unit

    def fs(self, size):
        """A text size as the scripts give it -> the size to draw, never smaller than designed."""
        return round(max(size, self.u(text_pt(size))), 2)

    def sw(self, width):
        """A stroke width in drawing units -> the width to draw, never thinner than designed."""
        return round(max(width, self.u(line_pt(width))), 2)

    def css(self):
        """The stylesheet with stroke widths and dashes sized for print on this sheet."""
        out = re.sub(r"stroke-width: ([\d.]+)(?!px)", lambda m: f"stroke-width: {self.sw(float(m.group(1)))}", CSS)
        out = re.sub(r"stroke-width: ([\d.]+)px", lambda m: f"stroke-width: {round(float(m.group(1)) * min(self.f, 1.15), 2)}px", out)   # the label halo: kept light
        return re.sub(r"stroke-dasharray: ([\d. ]+);", lambda m: "stroke-dasharray: " + " ".join(
            str(round(float(v) * self.f, 2)) for v in m.group(1).split()) + ";", out)

    # mm -> px
    def X(self, x):
        return self.ox + x * self.scale

    def Y(self, y):
        return self.oy + y * self.scale

    def L(self, v):
        return v * self.scale

    # basic shapes, in mm
    def rect(self, x, y, w, h, cls, rx=0):
        self.d.append(dw.Rectangle(self.X(x), self.Y(y), self.L(w), self.L(h), rx=self.L(rx), class_=cls))

    def circle(self, x, y, r, cls):
        self.d.append(dw.Circle(self.X(x), self.Y(y), self.L(r), class_=cls))

    def line(self, x1, y1, x2, y2, cls):
        self.d.append(dw.Line(self.X(x1), self.Y(y1), self.X(x2), self.Y(y2), class_=cls))

    def text(self, s, x, y, size=13, cls="ink", anchor="start", weight=None, px=False):
        if not px:
            x, y = self.X(x), self.Y(y)
        kw = {"font_weight": weight} if weight else {}
        self.d.append(dw.Text(s, self.fs(size), x, y, text_anchor=anchor, class_=cls, **kw))

    # drawing-sheet furniture
    def _arrowhead(self, x, y, angle):
        a, s = angle, 7.0 * self.f
        p1 = (x - s * math.cos(a - 0.38), y - s * math.sin(a - 0.38))
        p2 = (x - s * math.cos(a + 0.38), y - s * math.sin(a + 0.38))
        self.d.append(dw.Lines(x, y, *p1, *p2, close=True, class_="arrow"))

    def dim_h(self, x1, x2, y, label, ext_from=None, text_above=True, text_side="right"):
        """Horizontal dimension between x1 and x2 (mm) drawn at height y (mm).
        ext_from: y (mm) the extension lines start from."""
        X1, X2, Y = self.X(x1), self.X(x2), self.Y(y)
        f = self.f
        if ext_from is not None:
            E = self.Y(ext_from)
            gap = (3 if E < Y else -3) * f
            for X in (X1, X2):
                self.d.append(dw.Line(X, E + gap, X, Y + (4 if E < Y else -4) * f, class_="dim"))
        inside = abs(X2 - X1) > 30 * f
        self.d.append(dw.Line(X1, Y, X2, Y, class_="dim"))
        if inside:
            self._arrowhead(X1, Y, math.pi)
            self._arrowhead(X2, Y, 0)
        else:  # arrows outside, pointing in
            self.d.append(dw.Line(X1 - 14 * f, Y, X1, Y, class_="dim"))
            self.d.append(dw.Line(X2, Y, X2 + 14 * f, Y, class_="dim"))
            self._arrowhead(X1, Y, 0)
            self._arrowhead(X2, Y, math.pi)
        if inside:
            ty = Y - 5 * f if text_above else Y + 15 * f
            self.d.append(dw.Text(label, self.fs(12), (X1 + X2) / 2, ty, text_anchor="middle", class_="dimtxt"))
        else:  # too short for the text: put it beside the outer arrow
            if text_side == "left":
                self.d.append(dw.Text(label, self.fs(12), X1 - 18 * f, Y + 4 * f, text_anchor="end", class_="dimtxt"))
            else:
                self.d.append(dw.Text(label, self.fs(12), X2 + 18 * f, Y + 4 * f, text_anchor="start", class_="dimtxt"))

    def dim_v(self, y1, y2, x, label, ext_from=None, text_left=False):
        X, Y1, Y2 = self.X(x), self.Y(y1), self.Y(y2)
        f = self.f
        if ext_from is not None:
            E = self.X(ext_from)
            gap = (3 if E < X else -3) * f
            for Y in (Y1, Y2):
                self.d.append(dw.Line(E + gap, Y, X + (4 if E < X else -4) * f, Y, class_="dim"))
        inside = abs(Y2 - Y1) > 30 * f
        self.d.append(dw.Line(X, Y1, X, Y2, class_="dim"))
        if inside:
            self._arrowhead(X, Y1, -math.pi / 2)
            self._arrowhead(X, Y2, math.pi / 2)
        else:
            self.d.append(dw.Line(X, Y1 - 14 * f, X, Y1, class_="dim"))
            self.d.append(dw.Line(X, Y2, X, Y2 + 14 * f, class_="dim"))
            self._arrowhead(X, Y1, math.pi / 2)
            self._arrowhead(X, Y2, -math.pi / 2)
        tx = X - 6 * f if text_left else X + 6 * f
        self.d.append(dw.Text(label, self.fs(12), tx, (Y1 + Y2) / 2 + 4 * f, text_anchor="end" if text_left else "start",
                              class_="dimtxt"))

    def balloon(self, n, target, at, label, detail="", free=False):
        """Numbered balloon near `at` (px) with a leader to `target` (mm).
        `label` and `detail` go into the key.
        Balloons are drawn when the sheet is saved: each one keeps the row (or column) `at` puts it in, but slides
        along it to sit straight below, above or beside its target, so leaders are straight lines (see _layout_balloons).
        free=True keeps `at` exactly, with a straight leader at whatever angle it needs."""
        self.balloons.append((n, label, detail))
        self._pending.append(dict(n=n, tx=self.X(target[0]), ty=self.Y(target[1]), bx=at[0], by=at[1], free=free))

    # ---- balloon layout: straight leaders, no crossings
    BALLOON_R = 10
    BALLOON_GAP = 26            # center-to-center spacing of balloons in a row

    @staticmethod
    def _spread(want, gap, lo, hi):
        """Positions as close as possible to `want` (sorted), at least `gap` apart, within [lo, hi].
        Least-squares fit by pool-adjacent-violators on want[i] - i*gap."""
        n = len(want)
        if not n:
            return []
        q = [w - i * gap for i, w in enumerate(want)]
        blocks = []                                  # [sum, count]
        for v in q:
            blocks.append([v, 1])
            while len(blocks) > 1 and blocks[-2][0] / blocks[-2][1] > blocks[-1][0] / blocks[-1][1]:
                a = blocks.pop()
                blocks[-1][0] += a[0]
                blocks[-1][1] += a[1]
        out = []
        for sm, c in blocks:
            out += [sm / c] * c
        pos = [v + i * gap for i, v in enumerate(out)]
        if pos[0] < lo:
            pos = [p + lo - pos[0] for p in pos]
        if pos[-1] > hi:
            pos = [p - (pos[-1] - hi) for p in pos]
        return pos

    def _layout_balloons(self):
        """Place pending balloons and draw them with straight or single-jog leaders."""
        r, gap = self.BALLOON_R * self.f, self.BALLOON_GAP * self.f
        groups = {}
        for b in self._pending:
            if b["free"]:
                self._draw_balloon(b, [(b["tx"], b["ty"]), (b["bx"], b["by"])])
                continue
            dx, dy = b["bx"] - b["tx"], b["by"] - b["ty"]
            vertical = abs(dy) >= 0.5 * abs(dx)
            side = ("below" if dy > 0 else "above") if vertical else ("right" if dx > 0 else "left")
            line = b["by"] if vertical else b["bx"]  # the row's y, or the column's x
            for key in groups:                       # join a row or column within 24 px
                if key[0] == side and abs(key[1] - line) <= 24:
                    groups[key].append(b)
                    break
            else:
                groups[(side, line)] = [b]
        for (side, line), bs in groups.items():
            vertical = side in ("below", "above")
            sgn = 1 if side in ("below", "right") else -1
            along = (lambda b: b["tx"]) if vertical else (lambda b: b["ty"])
            across = (lambda b: b["ty"]) if vertical else (lambda b: b["tx"])
            bs.sort(key=along)
            row = sum((b["by"] if vertical else b["bx"]) for b in bs) / len(bs)
            hi = (self.width if vertical else self.height) - r - 4
            pos = self._spread([along(b) for b in bs], gap, r + 4, hi)
            # Knees for jogged leaders sit in the band between the targets and the row; the balloon moved
            # furthest gets the knee nearest its target, so jogs nest and never cross.
            nearest = max(sgn * across(b) for b in bs) * sgn
            band_a = nearest + sgn * 8
            band_b = row - sgn * (r + 6)
            for direction in (-1, 1):
                moved = [(abs(p - along(b)), i) for i, (b, p) in enumerate(zip(bs, pos))
                         if (p - along(b)) * direction > 1.5]
                moved.sort(reverse=True)
                k = len(moved)
                for j, (_, i) in enumerate(moved):
                    t = (j + 1) / (k + 1)
                    bs[i]["knee"] = band_a + (band_b - band_a) * t if sgn * (band_b - band_a) > 6 * k else \
                        row - sgn * (r + 6 + 6 * (k - j))
            for b, p in zip(bs, pos):
                if vertical:
                    b["bx"], b["by"] = p, row
                    if "knee" in b:
                        pts = [(b["tx"], b["ty"]), (b["tx"], b["knee"]), (p, b["knee"]), (p, row)]
                    else:
                        pts = [(b["tx"], b["ty"]), (b["tx"], row)]
                else:
                    b["bx"], b["by"] = row, p
                    if "knee" in b:
                        pts = [(b["tx"], b["ty"]), (b["knee"], b["ty"]), (b["knee"], p), (row, p)]
                    else:
                        pts = [(b["tx"], b["ty"]), (row, b["ty"])]
                self._draw_balloon(b, pts)
        self._pending = []

    def _draw_balloon(self, b, pts):
        r = self.BALLOON_R * self.f
        (x0, y0), (x1, y1) = pts[-2], pts[-1]
        ang = math.atan2(y0 - y1, x0 - x1)
        end = (x1 + r * math.cos(ang), y1 + r * math.sin(ang))   # stop the leader at the balloon's edge
        path = dw.Path(class_="lead", fill="none")
        path.M(*pts[0])
        for x, y in pts[1:-1]:
            path.L(x, y)
        path.L(*end)
        self.d.append(path)
        self.d.append(dw.Circle(pts[0][0], pts[0][1], 2.2 * self.f, class_="dot"))
        self.d.append(dw.Circle(x1, y1, r, class_="balloon"))
        self.d.append(dw.Text(str(b["n"]), self.fs(11.5), x1, y1 + 4 * self.f, text_anchor="middle", class_="ink", font_weight="600"))

    def key(self, x, y, width=240, title="Key", only=None):
        """The numbered key, like a parts list on a drawing (px). `only` lists the balloon numbers to show, so a long
        key can be split into columns (give the second column title=""). Returns the y of the last line."""
        f = self.f
        if title:
            self.d.append(dw.Text(title, self.fs(13), x, y, class_="ink", font_weight="600"))
        y += 10 * f
        self.d.append(dw.Line(x, y, x + width, y, class_="thin"))
        for n, label, detail in sorted(self.balloons):
            if only is not None and n not in only:
                continue
            y += 26 * f
            self.d.append(dw.Circle(x + 10 * f, y - 4 * f, 9 * f, class_="balloon"))
            self.d.append(dw.Text(str(n), self.fs(10.5), x + 10 * f, y, text_anchor="middle", class_="ink",
                                  font_weight="600"))
            self.d.append(dw.Text(label, self.fs(12.5), x + 28 * f, y, class_="ink"))
            if detail:
                y += 16 * f
                self.d.append(dw.Text(detail, self.fs(11), x + 28 * f, y, class_="muted"))
        return y

    # ---- board views in Chris's color key: shapes are returned, not drawn, so they can be grouped and clipped
    def R(self, x, y, w, h, cls, rx=0):
        return dw.Rectangle(self.X(x), self.Y(y), self.L(w), self.L(h), rx=self.L(rx), class_=cls)

    def C(self, x, y, r, cls):
        return dw.Circle(self.X(x), self.Y(y), self.L(r), class_=cls)

    def PL(self, pts, cls, width):
        p = dw.Path(class_=cls, stroke_width=round(max(self.L(width), self.u(LINE_MIN_PT)), 2))
        p.M(self.X(pts[0][0]), self.Y(pts[0][1]))
        for x, y in pts[1:]:
            p.L(self.X(x), self.Y(y))
        return p

    def clipped(self, shapes):
        cp = dw.ClipPath()
        for sh in shapes:
            cp.append(sh)
        return dw.Group(clip_path=cp)

    def board_view(self, window, geom, openings=(), holes=()):
        """Plan view of a board inside window (x, y, w, h) in mm.
        geom(add, cu, fr4) draws the copper layout with fill classes cu and fr4 (strokes use 's-' + class).
        It is drawn once as it looks under the mask, then again inside the mask openings, then the holes."""
        outer = self.clipped([self.R(*window, "bg")])
        under = dw.Group()
        geom(under.append, "mask-on-cu", "mask-on-fr4")
        outer.append(under)
        if openings:
            inside = self.clipped(openings)
            geom(inside.append, "cu-exposed", "fr4-exposed")
            outer.append(inside)
        for x, y, r in holes:
            outer.append(self.C(x, y, r, "drill"))
        self.d.append(outer)
        return outer

    def legend(self, x, y, items):
        """Color swatches with labels (px)."""
        f = self.f
        for i, (cls, label) in enumerate(items):
            yy = y + i * 22 * f
            self.d.append(dw.Rectangle(x, yy - 11 * f, 14 * f, 14 * f, class_=cls))
            self.d.append(dw.Rectangle(x, yy - 11 * f, 14 * f, 14 * f, class_="thin"))
            self.d.append(dw.Text(label, self.fs(12), x + 22 * f, yy + 1 * f, class_="ink"))

    def note(self, s, x, y):
        self.d.append(dw.Text(s, self.fs(11), x, y, class_="muted"))

    def save(self, path):
        self._layout_balloons()
        if CURRENT_D is not None:
            # The drawing's number, boxed in a band added above it, so it never collides with the content and every
            # drawing can be referred to by number. Recommendation IDs sit beside it.
            f = self.f
            band = 40 * f
            out = dw.Drawing(self.width, self.height + band, role="img", aria_labelledby="title desc")
            for e in self.d.elements[:2]:                      # <title>/<desc>, then the stylesheet
                out.append(e)
            out.append(dw.Rectangle(0, 0, self.width, self.height + band, class_="bg"))
            g = dw.Group(transform=f"translate(0,{band})")
            for e in self.d.elements[3:]:                      # everything after the original background
                g.append(e)
            out.append(g)
            num = f"D{CURRENT_D}"
            w = (16 + 10.5 * len(num)) * f
            out.append(dw.Rectangle(12 * f, 8 * f, w, 26 * f, rx=6 * f, class_="figbox"))
            out.append(dw.Text(num, self.fs(16), 12 * f + w / 2, 27 * f, text_anchor="middle", font_weight="700",
                               class_="ink"))
            recs = " \u00b7 ".join(_recs_for(CURRENT_D))
            if recs:
                out.append(dw.Text(recs, self.fs(13), 12 * f + w + 10 * f, 26 * f, class_="muted"))
            out.save_svg(path)
            embed_file(path)
            return
        self.d.save_svg(path)
        embed_file(path)

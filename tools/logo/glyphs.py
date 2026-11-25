"""Text as outlines in Atkinson Hyperlegible Next, for the logo (M44).

Face(style).run(text, size, x, baseline, fill) shapes the text with HarfBuzz (so kerning applies) and returns
one SVG path and the advance width, so a logo file never depends on a font being installed.
Used by build_brand.py. Needs pip install fonttools uharfbuzz.
"""
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONTS = Path(__file__).resolve().parent.parent.parent / "fonts"


class Face:
    def __init__(self, style):
        path = FONTS / f"AtkinsonHyperlegibleNext-{style}.ttf"
        data = path.read_bytes()
        self.hb_font = hb.Font(hb.Face(data))
        self.tt = TTFont(path)
        self.upm = self.tt["head"].unitsPerEm
        self.glyphs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        os2 = self.tt["OS/2"]
        self.cap = os2.sCapHeight

    def run(self, text, size, x, y, fill, extra_track=0.0):
        """Shaped text as one SVG path. y is the baseline. Returns (svg, advance)."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb_font, buf, {"kern": True, "liga": True})
        s = size / self.upm
        parts = []
        pen_x = 0.0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            name = self.order[info.codepoint]
            pen = SVGPathPen(self.glyphs)
            gx = x + (pen_x + pos.x_offset) * s
            gy = y - pos.y_offset * s
            self.glyphs[name].draw(TransformPen(pen, (s, 0, 0, -s, gx, gy)))
            parts.append(pen.getCommands())
            pen_x += pos.x_advance + extra_track * self.upm
        return f'<path fill="{fill}" d="{" ".join(parts)}"/>', (pen_x - extra_track * self.upm) * s

    def width(self, text, size, extra_track=0.0):
        return self.run(text, size, 0, 0, "none", extra_track)[1]

    def cap_h(self, size):
        return self.cap * size / self.upm


REGULAR = Face("Regular")
MEDIUM = Face("Medium")
BOLD = Face("Bold")
EXTRABOLD = Face("ExtraBold")

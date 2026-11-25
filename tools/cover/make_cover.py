"""Draw the book's cover (M13, Q165 to Q170).

Run: python3 tools/cover/make_cover.py
Writes tools/cover/cover.svg and tools/cover/cover.png, a 300 dpi rendering used by the PDF and the EPUB
(needs node and Playwright; WeasyPrint can't draw the SVG's masks, so the PDF uses the PNG).

The board on the cover is a real one: The Public Radio's circuit board (PR9028), used with permission (Q169).
Its copper, solder mask, silkscreen and board outline were exported with KiCad 10 from a tidied copy of
the board, which is kept private (TPR1, Q184), into tools/cover/board/ (kicad-cli pcb export svg --mode-multi
--black-and-white --exclude-drawing-sheet --page-size-mode 2 --drill-shape-opt 2 -l F.Cu,F.Mask,F.Silkscreen,Edge.Cuts).
Those four layer drawings are the cover's source: this script rebuilds the cover from them alone.
This script draws them in the book's board color key, so every pad, trace, via, hole and silkscreen line
is where it is on the real board.
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools" / "diagrams"))
from embed_fonts import FONT_STACK, embed_file  # noqa: E402

# The board color key (tools/diagrams/opendfx_draw.py).
CU, FR4, MCU, MFR4, SILK, HOLE = "#d9b44a", "#9c7a4a", "#2f9e4f", "#1e7a3e", "#f2f2ef", "#17191c"
BG = "#262a2f"  # charcoal, the logo's dark board (Q242)
GREY = "#c9cdd1"  # the subtitle
W, H = 850, 1100  # US Letter, 8.5 x 11 in at 100 units per inch

# The board outline (from public-radio-Edge_Cuts.svg): a 65.9 mm square with 34.2 mm corner arcs, and the speaker cut-out.
R = "34.2269 34.2269 0 0 1"
OUTLINE = (f"M21.2190 0 L44.7190 0 A{R} 65.9380 21.2190 L65.9380 44.7190 A{R} 44.7190 65.9380 "
           f"L21.2190 65.9380 A{R} 0 44.7190 L0 21.2190 A{R} 21.2190 0 Z "
           "M20.9690 32.9690 a12 12 0 1 0 24 0 a12 12 0 1 0 -24 0 Z")
CENTER = 32.9690


def layer(name):
    """The drawing inside one exported layer SVG, without its <svg>, title and description."""
    t = (HERE / "board" / f"public-radio-{name}.svg").read_text()
    inner = t[t.index(">", t.index("<svg")) + 1: t.rindex("</svg>")]
    return re.sub(r"<title>.*?</title>|<desc>.*?</desc>", "", inner, flags=re.S)


def recolor(s, black, white):
    """KiCad plots each layer in black, with drilled holes in white."""
    return s.replace("#000000", black).replace("#FFFFFF", white)


def board():
    """The board in the color key, in millimeters: mask over FR4, mask over copper, openings, silkscreen, holes."""
    cu, mask, silk = layer("F_Cu"), layer("F_Mask"), layer("F_Silkscreen")
    big = 'x="-50" y="-50" width="200" height="200"'
    return f'''<defs>
 <mask id="open" maskUnits="userSpaceOnUse" {big}><rect {big} fill="black"/>{recolor(mask, "#fff", "#fff")}</mask>
 <mask id="closed" maskUnits="userSpaceOnUse" {big}><rect {big} fill="white"/>{recolor(mask, "#000", "#000")}</mask>
 <clipPath id="outline"><path d="{OUTLINE}" clip-rule="evenodd"/></clipPath>
</defs>
<g clip-path="url(#outline)">
 <rect {big} fill="{MFR4}"/>
 <g>{recolor(cu, MCU, "none")}</g>
 <rect {big} fill="{FR4}" mask="url(#open)"/>
 <g mask="url(#open)">{recolor(cu, CU, "none")}</g>
 <g mask="url(#closed)">{recolor(silk, SILK, SILK)}</g>
 <g>{recolor(cu, "none", HOLE)}</g>
</g>'''


def title_block():
    """The title (Q242): the logo's symbol drawn down beside the two title lines, so it runs from the top of the
    capitals of "OpenDFX" to the baseline of "for Printed Circuit Boards". The subtitle and the author line up under
    the words. Returns the SVG."""
    sys.path.insert(0, str(ROOT / "tools" / "logo"))
    import build_brand as bb
    cap = bb.CAP / bb.SIZE           # cap height as a fraction of the font size
    x, top, name, line2 = 70, 92, 106, 40
    b1 = top + cap * name            # baseline of "OpenDFX"
    b2 = b1 + name * 0.62            # baseline of "for Printed Circuit Boards"
    sym = b2 - top                   # the symbol's height and width
    tx = x + sym * 1.22              # where the words start
    tm = (f'<tspan font-size="{name * 0.34:.1f}" font-weight="700" dx="{name * 0.04:.1f}" '
          f'dy="{-name * (cap - 0.34 * 0.7):.1f}">™</tspan>')
    font = f'font-family="{FONT_STACK}"'
    return f'''<g transform="translate({x} {top}) scale({sym / 100:.4f})">{bb.symbol_body("green")}</g>
<g {font} fill="{SILK}">
<text x="{tx:.1f}" y="{b1:.1f}" font-size="{name}" font-weight="700" letter-spacing="{-0.01 * name:.2f}">OpenDFX{tm}</text>
<text x="{tx:.1f}" y="{b2:.1f}" font-size="{line2}" font-weight="600">for Printed Circuit Boards</text>
<text x="{tx:.1f}" y="{b2 + 56:.1f}" font-size="24" font-weight="500" fill="{GREY}">Practical recommendations for manufacturing,</text>
<text x="{tx:.1f}" y="{b2 + 87:.1f}" font-size="24" font-weight="500" fill="{GREY}">assembly and test</text>
<text x="{tx:.1f}" y="{b2 + 148:.1f}" font-size="34" font-weight="700">Chris Denney</text>
</g>'''


def cover():
    width = 1060  # the board's width on the cover, in cover units
    s = width / 65.938
    cx, cy = 425, 975
    tx, ty = cx - CENTER * s, cy - CENTER * s
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="cover-title cover-desc">
<title id="cover-title">OpenDFX for Printed Circuit Boards, by Chris Denney</title>
<desc id="cover-desc">The cover, on a charcoal background. At the top, the OpenDFX logo's symbol, an open solder jumper with two copper pads inside a white outline on a green square, beside the title in white, with the subtitle and the author below it. Below them, a real circuit board drawn in the book's colors: gold copper pads, green solder mask over traces, white silkscreen outlines and reference designators, and black drilled holes. It is The Public Radio's circuit board, with its round speaker cut-out in the middle.</desc>
<rect width="{W}" height="{H}" fill="{BG}"/>
<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})">{board()}</g>
{title_block()}
</svg>
'''


def main():
    svg = HERE / "cover.svg"
    svg.write_text(cover())
    embed_file(svg)  # the font travels inside the SVG (FONT1), so the cover looks the same everywhere
    sys.path.insert(0, str(ROOT / "tools" / "books"))
    from rasterize import rasterize
    png = HERE / "cover.png"
    try:  # 2550 x 3300 pixels: 300 dpi on US Letter, for the PDF (WeasyPrint can't draw the masks) and the EPUB
        rasterize(svg, png, 2550)
    except (OSError, subprocess.CalledProcessError) as e:
        sys.exit(f"Wrote {svg.relative_to(ROOT)}, but couldn't render the PNG: {e}")
    print(f"Wrote {svg.relative_to(ROOT)} and {png.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

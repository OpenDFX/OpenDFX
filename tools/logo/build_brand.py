"""The OpenDFX logo and press kit (M44, Q227 and Q233, 2026-11-15).

The logo is K6 from the drafts (round 5): an open solder jumper, two D-shaped copper pads facing each other
across a gap, inside a white legend outline that is broken where the jumper is open. So it holds an O and a
D. It comes on a green board or a charcoal board, beside the wordmark OpenDFX in Atkinson Hyperlegible Next
Bold. Everything is drawn here from one definition, as outlines, so no file needs a font.

Writes public/brand/ (served at opendfx.org/brand/, and zipped by tools/build_site.py as
/opendfx-brand.zip), public/favicon.svg, public/favicon.ico, public/apple-touch-icon.png and the link preview
public/og-image.png (Q237).
The PNG files are drawn by Chromium (tools/logo/render_png.js; needs node and Playwright).

    python3 tools/logo/build_brand.py           write everything
    python3 tools/logo/build_brand.py --check   report SVG files that are out of date (PNGs are not compared)

Needs pip install fonttools uharfbuzz pillow.
"""
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from glyphs import BOLD, MEDIUM  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
PUBLIC = ROOT / "public"
BRAND = PUBLIC / "brand"

# The logo's colors, from the book's board color key (tools/diagrams/opendfx_draw.py), plus charcoal.
GREEN = "#1e7a3e"     # solder mask over FR4
CHARCOAL = "#262a2f"  # the dark board
COPPER = "#d9b44a"    # exposed copper
SILK = "#f2f2ef"      # silkscreen legend
INK = "#1d2125"       # the wordmark on light backgrounds
PAPER = "#ffffff"
INK_DARK = "#e8eaed"  # the wordmark on dark backgrounds
NIGHT = "#16191c"     # the website's dark background
GREEN_BRIGHT = "#2f9e4f"  # solder mask over copper, for the rule on the link preview

COLORS = [
    ("Solder-mask green", GREEN, "The green board, and the main brand color."),
    ("Charcoal", CHARCOAL, "The dark board."),
    ("Copper", COPPER, "The two pads of the jumper."),
    ("Silkscreen white", SILK, "The legend outline around the pads."),
    ("Ink", INK, "The wordmark on light backgrounds."),
    ("Light ink", INK_DARK, "The wordmark on dark backgrounds."),
]

BOARDS = {"green": GREEN, "charcoal": CHARCOAL}

# The symbol, on a 100 by 100 grid. The tile's corners have a radius of 14.
TILE = "M14,0 H86 A14,14 0 0 1 100,14 V86 A14,14 0 0 1 86,100 H14 A14,14 0 0 1 0,86 V14 A14,14 0 0 1 14,0 Z"
# The pads: half discs 24 in radius, 8 apart.
PADS = "M46,26 A24,24 0 0 0 46,74 Z M54,26 A24,24 0 0 1 54,74 Z"
# The legend: two arcs 4 wide, centered 31 from the middle of each pad's flat side, open top and bottom.
LEGEND = ("M44,17 A33,33 0 0 0 44,83 V79 A29,29 0 0 1 44,21 Z "
          "M56,17 A33,33 0 0 1 56,83 V79 A29,29 0 0 0 56,21 Z")


def symbol_body(board):
    """The symbol in full color on the given board."""
    return (f'<path d="{TILE}" fill="{BOARDS[board]}"/><path d="{PADS}" fill="{COPPER}"/>'
            f'<path d="{LEGEND}" fill="{SILK}"/>')


def symbol_one_color(color):
    """The symbol in one color: the tile is solid and the pads and legend are cut out, so the background shows."""
    return f'<path fill-rule="evenodd" d="{TILE} {PADS} {LEGEND}" fill="{color}"/>'


def svg(w, h, body, title="OpenDFX"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" width="{w:.0f}" height="{h:.0f}" '
            f'role="img" aria-label="{title}">\n<title>{title}</title>\n{body}\n</svg>\n')


# The wordmark, at a font size of 100. The trademark sign sits at the top right, at a third of the size.
SIZE = 100
CAP = BOLD.cap_h(SIZE)
# How far the p hangs below the baseline, from the font, so no file cuts it off.
DESC = -BOLD.tt['glyf'][BOLD.tt.getBestCmap()[ord('p')]].yMin * SIZE / BOLD.upm
TRACK = -0.01


def wordmark(x, baseline, color, tm=True):
    text, w = BOLD.run("OpenDFX", SIZE, x, baseline, color, extra_track=TRACK)
    if tm:
        mark, mw = BOLD.run("™", SIZE * 0.34, x + w + SIZE * 0.04, baseline - CAP + SIZE * 0.34 * 0.7, color)
        return text + mark, w + SIZE * 0.04 + mw
    return text, w


def horizontal(symbol, ink, tm=True):
    """The symbol beside the wordmark. The symbol is 1.5 times the wordmark's cap height."""
    sym = CAP * 1.5
    gap = sym * 0.32
    text, w = wordmark(sym + gap, sym / 2 + CAP / 2, ink, tm)
    body = f'<g transform="scale({sym / 100:.4f})">{symbol}</g>{text}'
    return svg(sym + gap + w, max(sym, sym / 2 + CAP / 2 + DESC), body)


def stacked(symbol, ink, tm=True):
    """The symbol above the wordmark, for square spaces."""
    _, w = wordmark(0, 0, ink, tm)
    sym = w * 0.5
    gap = sym * 0.22
    text, _ = wordmark(0, sym + gap + CAP, ink, tm)
    body = f'<g transform="translate({(w - sym) / 2:.2f} 0) scale({sym / 100:.4f})">{symbol}</g>{text}'
    return svg(w, sym + gap + CAP + DESC, body)


def wordmark_svg(ink, tm=True):
    text, w = wordmark(0, CAP, ink, tm)
    return svg(w, CAP + DESC, text)


def avatar(board):
    """A profile picture: the board fills the square, and the symbol sits in the middle 64 percent, so a round crop
    never cuts it."""
    body = (f'<rect width="100" height="100" fill="{BOARDS[board]}"/>'
            f'<g transform="translate(18 18) scale(0.64)"><path d="{PADS}" fill="{COPPER}"/>'
            f'<path d="{LEGEND}" fill="{SILK}"/></g>')
    return svg(100, 100, body)


def share_card():
    """The link preview (Q237, Q242): the picture shown when someone shares opendfx.org, 1200 by 630 pixels.
    It matches the cover: charcoal, the symbol drawn down beside the two title lines, and the real board."""
    sys.path.insert(0, str(ROOT / "tools" / "cover"))
    import make_cover as mc
    W, H = 1200, 630
    cap = CAP / SIZE
    x, top, name, line2 = 80, 96, 96, 36
    b1 = top + cap * name
    b2 = b1 + name * 0.62
    sym = b2 - top
    tx = x + sym * 1.22
    s = 900 / 65.938
    board = (f'<g transform="translate({1090 - mc.CENTER * s:.2f} {560 - mc.CENTER * s:.2f}) scale({s:.4f})">'
             f'{mc.board()}</g>')
    name_svg = wordmark(0, 0, SILK)[0]
    body = (f'<rect width="{W}" height="{H}" fill="{CHARCOAL}"/>{board}'
            f'<g transform="translate({x} {top}) scale({sym / 100:.4f})">{symbol_body("green")}</g>'
            f'<g transform="translate({tx:.1f} {b1:.1f}) scale({name / SIZE:.4f})">{name_svg}</g>'
            + BOLD.run("for Printed Circuit Boards", line2, tx, b2, SILK)[0]
            + MEDIUM.run("Practical recommendations for", 26, tx, b2 + 60, "#c9cdd1")[0]
            + MEDIUM.run("manufacturing, assembly and test", 26, tx, b2 + 94, "#c9cdd1")[0]
            + BOLD.run("opendfx.org", 30, tx, b2 + 170, COPPER)[0])
    return svg(W, H, body, "OpenDFX for Printed Circuit Boards, at opendfx.org")


def files():
    """Every SVG in the kit: {published path relative to public/: text}."""
    out = {}
    for board in BOARDS:
        sym = symbol_body(board)
        out[f"brand/opendfx-symbol-{board}.svg"] = svg(100, 100, sym)
        out[f"brand/opendfx-logo-{board}.svg"] = horizontal(sym, INK)
        out[f"brand/opendfx-logo-{board}-on-dark.svg"] = horizontal(sym, INK_DARK)
        out[f"brand/opendfx-logo-stacked-{board}.svg"] = stacked(sym, INK)
        out[f"brand/opendfx-logo-stacked-{board}-on-dark.svg"] = stacked(sym, INK_DARK)
        out[f"brand/opendfx-avatar-{board}.svg"] = avatar(board)
    for name, color in (("black", INK), ("white", PAPER)):
        one = symbol_one_color(color)
        out[f"brand/opendfx-symbol-{name}.svg"] = svg(100, 100, one)
        out[f"brand/opendfx-logo-{name}.svg"] = horizontal(one, color)
        out[f"brand/opendfx-logo-stacked-{name}.svg"] = stacked(one, color)
        out[f"brand/opendfx-wordmark-{name}.svg"] = wordmark_svg(color)
    out["favicon.svg"] = svg(100, 100, symbol_body("green"))
    out["og-image.svg"] = share_card()
    out["brand/colors.json"] = json.dumps(
        [{"name": n, "hex": h, "rgb": [int(h[i:i + 2], 16) for i in (1, 3, 5)], "use": u} for n, h, u in COLORS],
        indent=2) + "\n"
    out["brand/README.txt"] = README
    return out


README = """OpenDFX logo and press kit
==========================

The full guide, with the rules and colors, is at https://opendfx.org/brand/

The logo is an open solder jumper: two copper pads facing each other across a gap, inside a white legend
outline that is open where the jumper is open. It comes on a green board or a charcoal board.

  opendfx-logo-*            the symbol beside the wordmark (use this one when you can)
  opendfx-logo-stacked-*    the symbol above the wordmark, for square spaces
  opendfx-symbol-*          the symbol alone
  opendfx-wordmark-*        the name alone
  opendfx-avatar-*          a square profile picture that survives a round crop
  -on-dark                  for dark backgrounds
  -black, -white            one color, for print or for photos and colored backgrounds
  colors.json               the brand colors

Every logo comes as SVG (any size) and PNG (transparent background).

Please:
  - Leave clear space around the logo of at least a quarter of the symbol's height.
  - Don't make the symbol smaller than 16 pixels on a screen or 6 mm in print.
  - Don't stretch, rotate, recolor, outline or add effects to the logo, or set the name in another typeface.
  - Write the name as one word, OpenDFX, with capital O, D, F and X.

OpenDFX is a trademark of Chris Denney. You're welcome to use the logo to link to OpenDFX, to write about it,
or to say that your work is based on it. Please don't use it in a way that suggests Chris Denney endorses
your product or service, or as part of your own logo. If you're not sure, ask at hello@opendfx.org.
"""

# PNG sizes: the logos at a height in pixels, the symbols and avatars as squares.
PNG = {
    "opendfx-logo-": [120, 480],
    "opendfx-logo-stacked-": [480, 1200],
    "opendfx-symbol-": [512, 1024],
    "opendfx-wordmark-": [120, 480],
    "opendfx-avatar-": [400, 1024],
}


def png_jobs(svgs):
    jobs = []
    for rel in svgs:
        name = Path(rel).name
        if not rel.startswith("brand/") or not name.endswith(".svg"):
            continue
        key = next((k for k in sorted(PNG, key=len, reverse=True) if name.startswith(k)), None)
        if key is None:
            continue
        for h in PNG[key]:
            jobs.append({"svg": str(PUBLIC / rel), "png": str(BRAND / "png" / f"{name[:-4]}-{h}.png"), "height": h})
    for h, out in ((180, "apple-touch-icon.png"), (192, "brand/png/opendfx-icon-192.png"),
                   (512, "brand/png/opendfx-icon-512.png")):
        jobs.append({"svg": str(BRAND / "opendfx-avatar-green.svg"), "png": str(PUBLIC / out), "height": h})
    jobs.append({"svg": str(PUBLIC / "og-image.svg"), "png": str(PUBLIC / "og-image.png"), "height": 630})
    for h in (16, 32, 48):
        jobs.append({"svg": str(PUBLIC / "favicon.svg"), "png": f"ICO{h}", "height": h})
    return jobs


def main():
    svgs = files()
    if "--check" in sys.argv:
        stale = [rel for rel, text in svgs.items() if not (PUBLIC / rel).exists() or (PUBLIC / rel).read_text() != text]
        if stale:
            print("build_brand: out of date:", *stale, sep="\n  ")
            sys.exit(1)
        print(f"build_brand: {len(svgs)} files up to date")
        return
    for rel, text in svgs.items():
        (PUBLIC / rel).parent.mkdir(parents=True, exist_ok=True)
        (PUBLIC / rel).write_text(text)
    (BRAND / "png").mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        jobs = png_jobs(svgs)
        for j in jobs:
            if j["png"].startswith("ICO"):
                j["png"] = str(Path(tmp) / f"{j['png']}.png")
        (Path(tmp) / "jobs.json").write_text(json.dumps(jobs))
        subprocess.run(["node", str(Path(__file__).with_name("render_png.js")), str(Path(tmp) / "jobs.json")], check=True)
        from PIL import Image
        icons = [Image.open(Path(tmp) / f"ICO{h}.png") for h in (16, 32, 48)]
        icons[-1].save(PUBLIC / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)], append_images=icons[:-1])
    print(f"build_brand: {len(svgs)} SVG and JSON files, {len(jobs)} PNG files -> public/brand/")


if __name__ == "__main__":
    main()

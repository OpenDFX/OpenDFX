"""Put the book's font inside a drawing (FONT1, Q210).

A drawing shown on a web page is an image, and an image can't use the page's fonts, so a reader who doesn't
have Atkinson Hyperlegible Next installed would see another font, wider or narrower than the one the drawing
was laid out for. So each drawing carries its own copy: for every weight it uses, a subset of the font
holding only the characters it uses, as a WOFF2 file inside an @font-face rule in its stylesheet.
That adds roughly 10 to 15 KB per weight.

Used by opendfx_draw.Sheet.save() and tools/cover/make_cover.py. Needs pip install fonttools brotli.
"""
import base64
import html
import io
import re
from functools import lru_cache
from pathlib import Path

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont

FONTS = Path(__file__).resolve().parent.parent.parent / "fonts"
FAMILY = "Atkinson Hyperlegible Next"
SYMBOLS_FAMILY = "OpenDFX Symbols"
# The font list for drawings: Atkinson, then the symbols it lacks, then common fonts if neither loads.
FONT_STACK = f"'{FAMILY}', '{SYMBOLS_FAMILY}', 'Helvetica Neue', Helvetica, Arial, sans-serif"
STYLES = {400: "Regular", 500: "Medium", 600: "SemiBold", 700: "Bold", 800: "ExtraBold"}
NAMED = {"normal": 400, "bold": 700}
MARK = "/* fonts embedded by embed_fonts.py */"
MARK_END = "/* end of embedded fonts */"


@lru_cache(maxsize=None)
def _font_bytes(path):
    return Path(path).read_bytes()


@lru_cache(maxsize=None)
def _cmap(path):
    return frozenset(TTFont(io.BytesIO(_font_bytes(path))).getBestCmap())


def _subset_woff2(path, text):
    font = TTFont(io.BytesIO(_font_bytes(path)), recalcTimestamp=False)
    opts = Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt", "ccmp", "locl", "mark", "mkmk"]
    opts.name_IDs = [0, 1, 2, 3, 4, 5, 6, 13, 14]   # keep the copyright and license notice
    opts.notdef_outline = True
    sub = Subsetter(opts)
    sub.populate(text=text)
    sub.subset(font)
    font.flavor = "woff2"
    buf = io.BytesIO()
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def _weights(svg):
    found = {400}
    for w in re.findall(r'font-weight\s*[=:]\s*"?\s*([a-z0-9]+)', svg):
        w = NAMED.get(w, w)
        found.add(min(STYLES, key=lambda s: abs(s - int(w))))
    return sorted(found)


def _text(svg):
    body = re.sub(r"<style.*?</style>", "", svg, flags=re.S)
    parts = re.findall(r"<(?:text|tspan)\b[^>]*>([^<]*)", body)
    return html.unescape("".join(parts))


def font_css(svg):
    """The @font-face rules a drawing needs, as CSS text."""
    chars = "".join(sorted(set(_text(svg)) - set("\n\r\t")))
    if not chars.strip():
        return ""
    rules = []
    for w in _weights(svg):
        path = FONTS / f"AtkinsonHyperlegibleNext-{STYLES[w]}.ttf"
        have = _cmap(str(path))
        mine = "".join(c for c in chars if ord(c) in have)
        rules.append(_rule(FAMILY, w, _subset_woff2(str(path), mine)))
        missing = "".join(c for c in chars if ord(c) not in have and not c.isspace())
        sym = FONTS / f"OpenDFXSymbols-{STYLES[w]}.otf"
        if missing and sym.exists():
            theirs = "".join(c for c in missing if ord(c) in _cmap(str(sym)))
            if theirs:
                rules.append(_rule(SYMBOLS_FAMILY, w, _subset_woff2(str(sym), theirs)))
    return "\n".join(rules)


def _rule(family, weight, data):
    return (f"@font-face {{ font-family: '{family}'; font-weight: {weight}; font-style: normal; "
            f"src: url(data:font/woff2;base64,{data}) format('woff2'); }}")


def embed(svg):
    """Return the SVG text with its fonts added at the start of its first stylesheet (or a new one)."""
    if MARK in svg:
        svg = re.sub(re.escape(MARK) + r".*?" + re.escape(MARK_END) + r"\n?", "", svg, flags=re.S)
    css = font_css(svg)
    if not css:
        return svg
    block = f"{MARK}\n{css}\n{MARK_END}\n"
    m = re.search(r"<style[^>]*>(<!\[CDATA\[)?", svg)
    if m:
        return svg[:m.end()] + "\n" + block + svg[m.end():]
    m = re.search(r"<svg\b[^>]*>", svg)
    return svg[:m.end()] + f"\n<style>\n{block}</style>" + svg[m.end():]


def embed_file(path):
    path = Path(path)
    path.write_text(embed(path.read_text(encoding="utf-8")), encoding="utf-8")

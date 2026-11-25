#!/usr/bin/env python3
"""Build the book's fonts from the upstream files in fonts/source/ (FONT1, Q182, Q210).

    python3 tools/build_fonts.py           (write the fonts)
    python3 tools/build_fonts.py --check   (report fonts that are missing or out of date)

The book, the drawings, the cover and the website use Atkinson Hyperlegible Next, with
Atkinson Hyperlegible Mono for code. Both are variable fonts under the SIL Open Font License 1.1,
with no Reserved Font Name, so modified copies may keep their names. This script makes two changes:

1. It adds the micro sign (U+00B5, in "µm") and the ohm sign (U+2126), drawn with the font's own
   Greek mu and omega. Atkinson has the Greek letters but not these two signs, so without the
   change every "µm" in the book would fall back to another font.
2. It makes static fonts, one file per weight, for the PDF build (WeasyPrint) and the drawings,
   because both handle static fonts more reliably than variable ones.

It also makes "OpenDFX Symbols", a small subset of Inter (also SIL Open Font License 1.1) holding the
few symbols the drawings and pages use that Atkinson doesn't have: the check mark, the cross, the
star, the warning sign and the arrows. It is named in every font list straight after Atkinson.

Outputs (all committed):
  fonts/*.ttf               static fonts for the PDF build and for embedding in the drawings
  site/static/fonts/*.woff2 the website's fonts (variable, so one file covers every weight)
Needs: pip install fonttools brotli. Inter comes from the system (Ubuntu's fonts-inter package),
and only when the symbols font is rebuilt.
"""
import io
import sys
from pathlib import Path

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "fonts" / "source"
OUT = ROOT / "fonts"
WEB = ROOT / "site" / "static" / "fonts"
INTER = Path("/usr/share/fonts/opentype/inter")

NEXT = SRC / "AtkinsonHyperlegibleNext[wght].ttf"
NEXT_ITALIC = SRC / "AtkinsonHyperlegibleNext-Italic[wght].ttf"
MONO = SRC / "AtkinsonHyperlegibleMono[wght].ttf"

# Static weights: (source, weight, file style, subfamily name)
STATIC = [
    (NEXT, 400, "Regular"), (NEXT, 500, "Medium"), (NEXT, 600, "SemiBold"),
    (NEXT, 700, "Bold"), (NEXT, 800, "ExtraBold"),
    (NEXT_ITALIC, 400, "Italic"), (NEXT_ITALIC, 700, "BoldItalic"),
    (MONO, 400, "Regular"), (MONO, 700, "Bold"),
]
# Signs Atkinson lacks, drawn with a glyph it has.
ALIASES = {0x00B5: 0x03BC, 0x2126: 0x03A9}
# Symbols for OpenDFX Symbols: check mark, heavy check, cross, heavy cross, star, warning sign, arrows.
# The space and no-break space are there too: a space after a symbol stays in the symbol's font, and without its
# own glyph WeasyPrint gives it a made-up width, which fails PDF/UA (veraPDF rule 7.21.5-1).
SYMBOLS = "✓✔✗✘★⚠←↑→↓↔ \u00a0"
SYMBOL_WEIGHTS = ["Regular", "Medium", "SemiBold", "Bold", "ExtraBold"]


def add_aliases(font):
    for table in font["cmap"].tables:
        if table.isUnicode():
            for new, old in ALIASES.items():
                if old in table.cmap and new not in table.cmap:
                    table.cmap[new] = table.cmap[old]
    return font


def to_bytes(font, flavor=None):
    font.flavor = flavor
    font.recalcTimestamp = False  # keep the output identical from run to run, for --check
    buf = io.BytesIO()
    font.save(buf, reorderTables=True)
    return buf.getvalue()


def family_file(src):
    return "AtkinsonHyperlegibleMono" if src == MONO else "AtkinsonHyperlegibleNext"


def build():
    """Return {path: bytes} for every output file."""
    files = {}
    for src, weight, style in STATIC:
        font = instancer.instantiateVariableFont(add_aliases(TTFont(src)), {"wght": weight},
                                                 updateFontNames=True)
        files[OUT / f"{family_file(src)}-{style}.ttf"] = to_bytes(font)
    for src in (NEXT, NEXT_ITALIC, MONO):
        name = src.name.replace("[wght]", "-Variable").replace(".ttf", ".woff2")
        files[WEB / name] = to_bytes(add_aliases(TTFont(src)), "woff2")
    if INTER.exists():
        for style in SYMBOL_WEIGHTS:
            font = TTFont(INTER / f"Inter-{style}.otf")
            opts = Options()
            opts.name_IDs = ["*"]
            opts.layout_features = []
            sub = Subsetter(opts)
            sub.populate(text=SYMBOLS)
            sub.subset(font)
            rename(font, "OpenDFX Symbols", style)
            files[OUT / f"OpenDFXSymbols-{style}.otf"] = to_bytes(font)
            if style in ("Regular", "SemiBold", "Bold"):
                files[WEB / f"OpenDFXSymbols-{style}.woff2"] = to_bytes(font, "woff2")
    else:
        print(f"{INTER} not found (apt install fonts-inter): keeping the committed OpenDFX Symbols fonts.")
        for path in list(OUT.glob("OpenDFXSymbols-*.otf")) + list(WEB.glob("OpenDFXSymbols-*.woff2")):
            files[path] = path.read_bytes()
    files[WEB / "OFL.txt"] = license_text().encode()
    files[OUT / "OFL.txt"] = license_text().encode()
    return files


def rename(font, family, style):
    """Give a subset font its own family name, as the Open Font License asks of modified fonts."""
    name = font["name"]
    full = f"{family} {style}"
    ps = f"{family.replace(' ', '')}-{style}"
    sub = "Regular" if style == "Regular" else style
    for rec in list(name.names):
        if rec.nameID in (1, 2, 3, 4, 6, 16, 17, 21, 22):
            name.removeNames(nameID=rec.nameID)
    if style in ("Regular", "Bold"):
        name.setName(family, 1, 3, 1, 0x409)
        name.setName(sub, 2, 3, 1, 0x409)
    else:
        name.setName(f"{family} {style}", 1, 3, 1, 0x409)
        name.setName("Regular", 2, 3, 1, 0x409)
        name.setName(family, 16, 3, 1, 0x409)
        name.setName(style, 17, 3, 1, 0x409)
    name.setName(f"{ps};OpenDFX", 3, 3, 1, 0x409)
    name.setName(full, 4, 3, 1, 0x409)
    name.setName(ps, 6, 3, 1, 0x409)
    if "CFF " in font:
        cff = font["CFF "].cff
        cff.fontNames = [ps]
        top = cff.topDictIndex[0]
        top.FullName, top.FamilyName = full, family


def license_text():
    parts = []
    for f in ("OFL.txt", "OFL-Mono.txt"):
        parts.append((SRC / f).read_text())
    parts.append(INTER_OFL)
    return ("The book's fonts. Each is licensed under the SIL Open Font License, Version 1.1.\n"
            "Atkinson Hyperlegible Next and Mono: the micro sign and the ohm sign were added, and static\n"
            "weights were made from the variable fonts. OpenDFX Symbols: a subset of Inter, renamed.\n"
            "Made by tools/build_fonts.py in the OpenDFX repository.\n\n"
            + "\n\n========================================================================\n\n".join(parts))


INTER_OFL = """Copyright (c) 2016 The Inter Project Authors (https://github.com/rsms/inter)

This Font Software is licensed under the SIL Open Font License, Version 1.1,
as is the full text of the license above (https://openfontlicense.org).
OpenDFX Symbols is a subset of Inter, renamed as the license asks of modified versions."""


def main():
    files = build()
    stale = [p for p, data in files.items() if not p.exists() or p.read_bytes() != data]
    if "--check" in sys.argv:
        for p in stale:
            print(f"stale: {p.relative_to(ROOT)}")
        sys.exit(1 if stale else 0)
    for p in stale:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(files[p])
    print(f"{len(files)} font files, {len(stale)} written.")


if __name__ == "__main__":
    main()

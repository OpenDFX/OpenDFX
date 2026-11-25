"""Build the PDF and EPUB of the whole book from its pages (M13, T8).

Run: python3 tools/build_books.py                (screen PDF and EPUB)
     python3 tools/build_books.py --print        (also the print version of the PDF, for print on demand)
     python3 tools/build_books.py --sample OUT   (a short sample PDF for review: cover, front matter, contents, one page, one appendix)
     python3 tools/build_books.py --site DIR     (also copy the screen PDF and the EPUB into DIR as opendfx-pcb.pdf and .epub;
                                                  the website workflow passes site/dist, so opendfx.org always has the latest)

Writes into build/ (Git-ignored):
  opendfx-pcb-<version>.pdf         for reading on a screen (Q162): single-sided, no blank pages, links clickable
  opendfx-pcb-<version>-print.pdf   for print on demand (Q164): wider inside margin, parts start on a right-hand page
  opendfx-pcb-<version>.epub        for e-readers

Pages come from book/ in the same order as the website and the data file (Part 0 to Part 8, then the appendices),
and the version from CITATION.cff, like the citation. The plan is tools/M13-PLAN.md.
Needs pandoc (3.1 or later) and WeasyPrint (pip install weasyprint pyyaml).
"""
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_appendices as ba  # noqa: E402
import build_data as bd  # noqa: E402

ROOT = ba.ROOT
BOOK = ba.BOOK
TOOLS = ROOT / "tools"
OUT = ROOT / "build"
COVER = TOOLS / "cover" / "cover.svg"
COVER_PNG = TOOLS / "cover" / "cover.png"
LOGO = ROOT / "public" / "brand" / "opendfx-symbol-green.svg"  # the logo's symbol on the title page (M44)
RASTER = TOOLS / "books" / "raster"
# Drawings that use SVG features WeasyPrint can't draw (masks, filters): the PDF uses a 300 dpi PNG made by
# tools/books/rasterize.py instead. The EPUB and the website use the SVG.
RASTER_DRAWINGS = {"legend-over-vias.svg"}  # D68
PDF_SVG = OUT / "pdf-svg"
DIMTXT_RULE = re.compile(r"\.dimtxt\s*\{[^}]*\}")
DIMTXT_TEXT = re.compile(r'<text\b[^>]*class="[^"]*\bdimtxt\b[^"]*"[^>]*>.*?</text>', re.S)
ABOUT = ROOT / "site" / "src" / "content" / "docs" / "about.md"
REPO = bd.REPO
VERSION = bd.VERSION
NAME = f"opendfx-pcb-{VERSION}"

LINK_RE = re.compile(r"(!?)\[((?:[^\[\]]|\[[^\]]*\])*)\]\(([^)\s]+)\)")
REC_ID_RE = re.compile(r'<h3 id="((?:p\d\d-\d\d-)?pcb-(dfa|dfm|dft)-(\d{3})[^"]*)">')


def book_pages():
    return [p.relative_to(BOOK).as_posix() for p in sorted(BOOK.glob("0[0-9]-*/[0-9]*.md"))]


def page_key(rel):
    """A short id for a page, used to keep heading ids unique across the whole book: 02-the-panel/04-x.md -> p02-04."""
    folder, name = rel.split("/")
    return f"p{folder[:2]}-{name[:2]}"


def source_markdown(rel):
    """A page's Markdown without the generated-file comment and the website footer, with links made book-wide."""
    text = (BOOK / rel).read_text()
    text = re.sub(r"<!--.*?-->\n?", "", text, flags=re.S)
    text = re.split(r"\n---\n\*From OpenDFX", text)[0].rstrip() + "\n"
    base = Path(rel).parent

    def fix(m):
        bang, label, target = m.groups()
        if re.match(r"[a-z]+:", target) or target.startswith("#"):
            return m.group(0)
        path, _, anchor = target.partition("#")
        resolved = (Path("/") / base / path).resolve().as_posix().lstrip("/")
        if bang:  # images: an absolute path, so pandoc and WeasyPrint find them
            return f"{bang}[{label}]({(BOOK / resolved).as_uri()})"
        if resolved.endswith(".md") and (BOOK / resolved).exists() and re.match(r"0\d-[^/]+/\d", resolved):
            key = page_key(resolved)
            return f"[{label}](#{key}-{anchor or 'top'})"
        outside = (Path("/book") / base / path).resolve().as_posix().lstrip("/")
        return f"[{label}]({REPO}/blob/main/{outside}{'#' + anchor if anchor else ''})"

    return LINK_RE.sub(fix, text)


def pandoc_html(markdown, shift=1):
    r = subprocess.run(["pandoc", "-f", "gfm", "-t", "html5", "--wrap=none", f"--shift-heading-level-by={shift}"],
                       input=markdown, capture_output=True, text=True, check=True)
    # Pandoc wraps an email link's text in a <span>. WeasyPrint then makes two link areas for it and tags only one,
    # which fails PDF/UA (rule 7.18.5-1: every link annotation must be tagged), so the span is removed.
    return re.sub(r'(<a\s[^>]*>)<span>(.*?)</span>(</a>)', r"\1\2\3", r.stdout, flags=re.S)


def prefix_ids(h, key):
    """Make every heading id and in-page link on one page unique in the book by prefixing the page's key."""
    h = re.sub(r'\sid="([^"]+)"', lambda m: f' id="{key}-{m.group(1)}"', h)
    h = re.sub(r'href="#(?!p\d\d-\d\d-)([^"]+)"', lambda m: f'href="#{key}-{m.group(1)}"', h)
    return h


def figures(h):
    """A drawing and the italic caption under it become one <figure>, kept together on one page.
    The alt text stays on the image for screen readers; the caption is the written description everyone sees."""
    def wrap(m):
        img, cap = m.group(1), m.group(2)
        return f'<figure>{img}<figcaption>{cap}</figcaption></figure>'
    h = re.sub(r'<p>(<img [^>]+>)</p>\s*<p><em>(D\d+ .*?)</em></p>', wrap, h, flags=re.S)
    return re.sub(r'<p>(<img [^>]+>)</p>', r'<figure>\1</figure>', h)


def permalinks(h):
    """Print each recommendation's permanent address under its heading, so a printed copy can be looked up and cited."""
    out, pos = [], 0
    for m in REC_ID_RE.finditer(h):
        rid = f"PCB-{m.group(2).upper()}-{m.group(3)}"
        end = h.index("</h3>", m.end()) + len("</h3>")
        out.append(h[pos:m.start()])
        out.append(h[m.start():end].replace("<h3 ", '<h3 class="rec" ', 1))
        out.append(f'<p class="permalink"><a href="https://opendfx.org/{rid}">opendfx.org/{rid}</a></p>')
        pos = end
    out.append(h[pos:])
    return "".join(out)


def page_html(rel):
    key = page_key(rel)
    h = pandoc_html(source_markdown(rel))
    h = prefix_ids(h, key)
    h = figures(h)
    h = permalinks(h)
    # The page's own heading carries the page's id, so links to the page itself land on it.
    h = re.sub(r'<h2 id="[^"]+"', f'<h2 id="{key}-top"', h, count=1)
    return f'<section class="page" id="{key}">\n{h}\n</section>\n'


def part_title(num, titles):
    return f"Part {num}: {titles[num]}" if num in titles else "Appendices"


def contents(pages, titles):
    """The contents list: every part and every page, with page numbers filled in by the PDF engine."""
    out = ['<nav class="toc" role="doc-toc" aria-labelledby="toc-title"><h1 id="toc-title" class="front">Contents</h1><ol>',
           '<li class="toc-part"><a href="#preface">Preface</a></li>']
    current = None
    for rel in pages:
        num = int(rel[:2])
        if num != current:
            if current is not None:
                out.append("</ol></li>")
            out.append(f'<li class="toc-part"><a href="#part-{num}">{html.escape(part_title(num, titles))}</a><ol>')
            current = num
        title = bd.page_title((BOOK / rel).read_text())
        out.append(f'<li><a href="#{page_key(rel)}-top">{html.escape(title)}</a></li>')
    out.append("</ol></li></ol></nav>")
    return "\n".join(out)


def about_html():
    """The website's About page (who wrote the book, how, corrections, license), as front matter."""
    text = ABOUT.read_text()
    text = re.sub(r"\A---.*?---\n", "", text, flags=re.S)
    text = text.replace("](/preface/)", "](#preface)")  # the website's Preface page is the book's own Preface
    text = text.replace("](/changelog/)", "](https://opendfx.org/changelog/)")  # the change log is only on the website (M14)
    return pandoc_html(text, shift=0)  # its sections are level 2, under the level-1 "About the book"


def front_page(name, cls):
    """A front-matter page from book/front-matter/ (the dedication or the preface), under its own level-1 heading."""
    h = pandoc_html(source_markdown(f"front-matter/{name}.md"), shift=0)
    h = re.sub(r'<h1 id="[^"]*"', f'<h1 id="{name}" class="front"', h, count=1)
    return f'<section class="{cls}">\n{h}\n</section>'


def front_matter(titles, kind="screen"):
    citation = html.escape(bd.CITATION)
    # A printed book's cover is a separate file (front, spine and back), so the print interior starts with the title page.
    cover = "" if kind == "print" else f'''<section class="cover" aria-label="Cover"><img src="{COVER_PNG.as_uri()}" alt="The cover of OpenDFX for Printed Circuit Boards by Chris Denney: the title on a dark background above a real circuit board drawn in the book's colors."></section>'''
    return f'''
{cover}
<section class="titlepage">
<div class="titleblock">
<img class="titlelogo" src="{LOGO.as_uri()}" alt="The OpenDFX logo: an open solder jumper, two copper pads inside a white outline on a green square.">
<h1 class="front booktitle" id="book-title"><span class="name">OpenDFX<span class="tm">™</span></span> <span class="line2">for Printed Circuit Boards</span></h1>
</div>
<p class="subtitle">Practical recommendations for manufacturing, assembly and test</p>
<p class="author">Chris Denney</p>
<p class="edition">Version {VERSION}</p>
</section>
<section class="copyright">
<p><strong>OpenDFX for Printed Circuit Boards</strong>, version {VERSION}, by Chris Denney.</p>
<p>The text and drawings are licensed under the Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0), <a href="https://creativecommons.org/licenses/by-sa/4.0/">creativecommons.org/licenses/by-sa/4.0</a>.
You may share and adapt them, including commercially, if you credit the book and share your changes under the same license.
The recommendations data files are licensed CC BY 4.0.
The code, including the KiCad design-rules file, is licensed under the MIT License.</p>
<p>OpenDFX is a trademark of Chris Denney. Please share OpenDFX as widely as you can. Teach from it, quote it, link to it, translate it and build on it, under the licenses above. The licenses cover the text, drawings, data and code, but not the OpenDFX name, so readers can always tell what is official. You may say that your work is based on OpenDFX, and the license requires you to credit it. Please ask before using OpenDFX in a domain name, a software package name, or the name of a social media account or group. Posts, pages and groups about the book are welcome, as long as they don't look like an official OpenDFX account. Please don't use the name as the title or brand of your own book, product or service, or in a way that suggests Chris Denney endorses it. If you're not sure, ask at <a href="mailto:hello@opendfx.org">hello@opendfx.org</a>; the answer is usually yes.</p>
<p>The latest version is always at <a href="https://opendfx.org">opendfx.org</a>.
Every recommendation has a permanent address, such as <a href="https://opendfx.org/PCB-DFA-006">opendfx.org/PCB-DFA-006</a>, printed under its heading.
Use it to link to a recommendation and to cite it.</p>
<p>To cite the book: {citation}.</p>
<p>Corrections are welcome at <a href="{REPO}/issues">github.com/OpenDFX/OpenDFX/issues</a>, or by email to <a href="mailto:hello@opendfx.org">hello@opendfx.org</a>.</p>
<p>The cover shows The Public Radio's circuit board, drawn from its design files and used with permission.</p>
</section>
{front_page("dedication", "dedication")}
<section class="about" id="about"><h1 class="front">About the book</h1>
{about_html()}
</section>
{contents(book_pages(), titles)}
{front_page("preface", "preface")}
'''


def body(pages, titles):
    out, current = [], None
    for rel in pages:
        num = int(rel[:2])
        if num != current:
            if current is not None:
                out.append("</section>")
            out.append(f'<section class="part" id="part-{num}"><h1 class="part-title">{html.escape(part_title(num, titles))}</h1>')
            current = num
        out.append(page_html(rel))
    out.append("</section>")
    return "\n".join(out)


def document(pages, titles, css, kind="screen"):
    return f'''<!DOCTYPE html>
<html lang="en-US"><head><meta charset="utf-8">
<title>OpenDFX for Printed Circuit Boards</title>
<meta name="author" content="Chris Denney">
<meta name="description" content="Practical recommendations for designing printed circuit boards that are easy to make, assemble and test.">
<meta name="keywords" content="printed circuit board, PCB, design for manufacturing, design for assembly, design for test">
<style>{css}</style></head>
<body>
{front_matter(titles, kind)}
{body(pages, titles)}
</body></html>'''


# The print version's margins, in millimeters (Q164). They meet both print-on-demand services' rules as found on
# 2026-11-13, which check_print() checks on every build:
#   KDP (Paperback Submission Guidelines, kdp.amazon.com/en_US/help/topic/G201857950, read 2026-11-13):
#        inside (gutter) margin at least 0.375 in up to 150 pages, 0.5 in to 300, 0.625 in to 500, 0.75 in to 700,
#        0.875 in to 828; outside, top and bottom at least 0.25 in without bleed; page size exactly the trim size;
#        text at least 7 pt; lines at least 0.75 pt; images at least 300 dpi (600 recommended at most); fonts embedded;
#        transparency flattened; no crop marks, bookmarks, comments, annotations or metadata.
#   Lulu (interior PDF settings article and File Setup Guide, read 2026-11-13): body text at least 0.5 in from the
#        trim edge, headers and footers 0.25 in; at least 0.2 in gutter; fonts embedded; transparency flattened;
#        300 to 600 ppi images; single pages; bleed only for full-page artwork; no trim marks or passwords.
PRINT_MARGINS = {"inside": 24, "outside": 16, "top": 24, "bottom": 24}
KDP_GUTTER_IN = [(150, 0.375), (300, 0.5), (500, 0.625), (700, 0.75), (828, 0.875)]
KDP_PAGES = (72, 590)  # 8.5 x 11 in: standard color 72 to 600 pages, premium color 24 to 590
KDP_MIN_LINE_PT = 0.75
LULU_SAFETY_IN = 0.5
LULU_GUTTER_IN = 0.2
MM_PER_IN = 25.4


def css(kind):
    base = (TOOLS / "books" / "book.css").read_text()
    if kind == "print":
        m = PRINT_MARGINS
        base += (TOOLS / "books" / "print.css").read_text()
        base += (f"@page :left {{ margin: {m['top']}mm {m['inside']}mm {m['bottom']}mm {m['outside']}mm; }}\n"
                 f"@page :right {{ margin: {m['top']}mm {m['outside']}mm {m['bottom']}mm {m['inside']}mm; }}\n")
    return base


def weasy(html_text, out, variant="pdf/ua-1"):
    from weasyprint import HTML
    HTML(string=html_text, base_url=str(ROOT)).write_pdf(out, pdf_variant=variant, uncompressed_pdf=False)


EMBEDDED_FONTS = re.compile(r"/\* fonts embedded by embed_fonts.py \*/.*?/\* end of embedded fonts \*/\n?", re.S)


# Symbols Atkinson lacks (see fonts/README.md). Inside a drawing, WeasyPrint looks for a missing character among the
# system's fonts rather than the next font in the list, so the PDF's copies name OpenDFX Symbols on each one.
SYMBOLS = re.compile("([\u2713\u2714\u2717\u2718\u2605\u26a0\u2190-\u2194])")


def symbol_spans(content):
    """Wrap each symbol in a drawing's text (outside any tag) in a tspan set in OpenDFX Symbols."""
    parts = re.split(r"(<[^>]*>)", content)
    return "".join(s if s.startswith("<") else SYMBOLS.sub(r"<tspan font-family='OpenDFX Symbols'>\1</tspan>", s)
                   for s in parts)


def pdf_svg(src):
    """A copy of a drawing that WeasyPrint draws the same as a browser. Dimension labels have a white halo made with
    `paint-order: stroke`, which WeasyPrint ignores, so the halo would be painted over the text and hide it.
    The copy draws the halo as a separate white copy of each label, behind it.
    It also drops the font subsets each drawing carries for web browsers (FONT1): the PDF already has the full fonts
    from tools/books/book.css, so it needn't carry 69 partial copies of the same font as well."""
    t = EMBEDDED_FONTS.sub("", src.read_text())
    t = re.sub(r"(<text\b[^>]*>)(.*?)(</text>)", lambda m: m.group(1) + symbol_spans(m.group(2)) + m.group(3), t, flags=re.S)
    rule = DIMTXT_RULE.search(t)
    halo = re.search(r"stroke-width:\s*([\d.]+px)", rule.group(0)).group(1) if rule else "3px"   # the kit scales it per drawing
    t = DIMTXT_RULE.sub(".dimtxt { fill: #2563a8; } .dimtxt-halo { fill: #ffffff; stroke: #ffffff; stroke-width: %s; "
                        "stroke-linejoin: round; }" % halo, t)
    t = DIMTXT_TEXT.sub(lambda m: re.sub(r'\bdimtxt\b', "dimtxt-halo", m.group(0).replace(' id="', ' data-id="'), count=1) + m.group(0), t)
    out = PDF_SVG / src.parent.parent.name / src.name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(t)
    return out


def check_raster(png, svg):
    import hashlib
    want = hashlib.sha256(svg.read_bytes()).hexdigest()
    sha = Path(str(png) + ".sha256")
    if not png.exists() or not sha.exists() or sha.read_text().strip() != want:
        sys.exit(f"build_books: {png.relative_to(ROOT)} is out of date with {svg.relative_to(ROOT)}. "
                 f"Run python3 tools/books/rasterize.py {svg.relative_to(ROOT)} {png.relative_to(ROOT)} 2400")


def pdf_images(doc):
    """Point the PDF's drawings at the copies WeasyPrint can draw (see pdf_svg and RASTER_DRAWINGS)."""
    check_raster(COVER_PNG, COVER)

    def swap(m):
        path = Path(m.group(1))
        if path.suffix != ".svg" or BOOK not in path.parents:
            return m.group(0)
        if path.name in RASTER_DRAWINGS:
            png = RASTER / (path.stem + ".png")
            check_raster(png, path)
            return f'src="{png.as_uri()}"'
        return f'src="{pdf_svg(path).as_uri()}"'

    return re.sub(r'src="file://([^"]+)"', swap, doc)


PRINT_PNG = OUT / "print-png"
PRINT_DPI = 600  # KDP: at least 300 dpi, at most 600 recommended; line art looks best at 600


def print_images(doc):
    """For the print version, every drawing becomes an opaque 600 dpi PNG drawn by Chromium (the website's engine).
    Both print services ask for transparency to be flattened, and the drawings use transparent fills;
    flattening the PDF afterwards (Ghostscript) turned every page into a picture. The screen PDF keeps vector drawings."""
    import hashlib
    import json
    width_in = (215.9 - PRINT_MARGINS["inside"] - PRINT_MARGINS["outside"]) / MM_PER_IN
    jobs, mapping = [], {}
    PRINT_PNG.mkdir(parents=True, exist_ok=True)
    for src in sorted(set(re.findall(r'src="file://([^"]+\.svg)"', doc))):
        svg = Path(src)
        vb = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', svg.read_text())
        w, h = float(vb.group(1)), float(vb.group(2))
        css_w = 1000
        css_h = round(css_w * h / w)
        scale = width_in * PRINT_DPI / css_w
        png = PRINT_PNG / f"{svg.parent.parent.name}-{svg.stem}.png"
        stamp = Path(str(png) + ".sha256")
        key = hashlib.sha256(svg.read_bytes() + str(scale).encode()).hexdigest()
        if not png.exists() or not stamp.exists() or stamp.read_text() != key:
            jobs.append({"svg": str(svg), "png": str(png), "width": css_w, "height": css_h, "scale": scale, "key": key})
        mapping[src] = png
    if jobs:
        listing = PRINT_PNG / "jobs.json"
        listing.write_text(json.dumps(jobs))
        subprocess.run(["node", str(TOOLS / "books" / "render_many.js"), str(listing)], check=True)
        from PIL import Image
        for j in jobs:  # stitch the strips; drop any alpha channel, which a PDF would turn into transparency
            n = int(Path(j["png"] + ".strips").read_text())
            strips = [Image.open(f'{j["png"]}.{i}').convert("RGB") for i in range(n)]
            whole = Image.new("RGB", (strips[0].width, sum(s.height for s in strips)), "white")
            y = 0
            for s in strips:
                whole.paste(s, (0, y))
                y += s.height
            whole.save(j["png"], optimize=True)
            for i in range(n):
                Path(f'{j["png"]}.{i}').unlink()
            Path(j["png"] + ".strips").unlink()
            Path(j["png"] + ".sha256").write_text(j["key"])
    return re.sub(r'src="file://([^"]+\.svg)"', lambda m: f'src="{mapping[m.group(1)].as_uri()}"', doc)


def plain_print(doc):
    """KDP asks for no bookmarks, annotations or metadata in a print file, and links can't be clicked on paper,
    so links become plain text and no bookmarks are made."""
    # An emoji marker (U+FE0F) makes a symbol such as the warning sign print as a color emoji picture, which has a
    # transparent background; without it the symbol prints as text from OpenDFX Symbols (see fonts/README.md).
    doc = doc.replace("\ufe0f", "")
    doc = re.sub(r"<a\s[^>]*>", "<span>", doc)
    doc = doc.replace("</a>", "</span>")
    return doc.replace("</style>", "* { bookmark-level: none !important; }</style>", 1)


def strip_print_metadata(pdf):
    """Remove the document information, XMP metadata, outline and any annotations from the print PDF (KDP)."""
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import NameObject
    reader = PdfReader(pdf)
    # WeasyPrint shares one resource list across pages, and it can hold images no page draws, such as a small
    # transparent one. A printer's preflight may flag those, so images and states no page uses are removed.
    used = set()

    def scan(data):
        used.update(re.findall(rb"/([^\s/\[\]<>()]+)\s+(?:Do|gs)\b", data))

    def contents(page):  # page.get_contents() returns nothing for WeasyPrint's pages, so read /Contents directly
        c = page.get("/Contents")
        if c is None:
            return b""
        c = c.get_object()
        return c.get_data() if hasattr(c, "get_data") else b"".join(x.get_object().get_data() for x in c)

    for page in reader.pages:
        scan(contents(page))
        xo = (page.get("/Resources") or {}).get("/XObject")
        for v in (xo.get_object().values() if xo else []):
            v = v.get_object()
            if v.get("/Subtype") == "/Form":
                scan(v.get_data())
    writer = PdfWriter()
    for page in reader.pages:
        if "/Annots" in page:
            del page[NameObject("/Annots")]
        res = page.get("/Resources")
        if res:
            res = res.get_object()
            for kind in ("/XObject", "/ExtGState"):
                d = res.get(kind)
                if d:
                    d = d.get_object()
                    for name in [k for k in d if k[1:].encode() not in used]:
                        del d[name]
        writer.add_page(page)
    writer._info = None  # no /Info dictionary
    writer.write(pdf)


def check_links(doc):
    """Every link inside the book must land on a heading that exists, and every drawing file must exist."""
    ids = set(re.findall(r'\sid="([^"]+)"', doc))
    bad = sorted({h for h in re.findall(r'href="#([^"]+)"', doc) if h not in ids})
    missing = sorted({s for s in re.findall(r'src="file://([^"]+)"', doc) if not Path(s).exists()})
    problems = [f"link to #{h} has no target" for h in bad] + [f"image {s} is missing" for s in missing]
    if problems:
        sys.exit("build_books: " + "\nbuild_books: ".join(problems))


def build_pdf(kind, pages, titles):
    OUT.mkdir(exist_ok=True)
    out = OUT / (f"{NAME}-print.pdf" if kind == "print" else f"{NAME}.pdf")
    doc = document(pages, titles, css(kind), kind)
    # An emoji marker (U+FE0F) makes a symbol such as the warning sign draw as a color emoji picture from Noto Color
    # Emoji. WeasyPrint 70 can crash drawing those, so both PDFs drop the marker and draw the symbol as text from
    # OpenDFX Symbols. The warning sign is colored amber so it still stands out (Q211).
    doc = doc.replace("\ufe0f", "")
    body = doc.index("<body")
    doc = doc[:body] + doc[body:].replace("\u26a0", '<span class="warn-sign">\u26a0</span>')
    check_links(doc)
    if kind == "print":
        weasy(plain_print(print_images(doc)), out, variant=None)
        even_pages(out)
        strip_print_metadata(out)
        check_print(out)
    else:
        weasy(pdf_images(doc), out)
    return out


def even_pages(pdf):
    """A printed book has an even number of pages (each sheet has two sides), so add a blank last page if needed."""
    from pypdf import PdfReader, PdfWriter
    reader = PdfReader(pdf)
    if len(reader.pages) % 2:
        writer = PdfWriter(clone_from=pdf)
        box = reader.pages[0].mediabox
        writer.add_blank_page(width=float(box.width), height=float(box.height))
        writer.write(pdf)


def smallest_drawing_text_pt():
    """The smallest text in any drawing, in points, at the print version's text width. [(pt, file)], smallest first."""
    width_mm = 215.9 - PRINT_MARGINS["inside"] - PRINT_MARGINS["outside"]
    rows = []
    for f in sorted(BOOK.glob("0*/images/*.svg")):
        t = f.read_text()
        vb = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', t)
        sizes = [float(s) for s in re.findall(r'font-size[=:]\s*"?([\d.]+)', t)]
        if vb and sizes:
            scale = min(width_mm / float(vb.group(1)), 200 / float(vb.group(2)))  # mm per unit; figures are at most 200 mm tall
            rows.append((min(sizes) * scale / 0.3528, f.relative_to(BOOK).as_posix()))
    return sorted(rows)


def thinnest_drawing_line_pt():
    """The thinnest line in any drawing, in points, at the print version's text width. [(pt, file)], thinnest first."""
    width_mm = 215.9 - PRINT_MARGINS["inside"] - PRINT_MARGINS["outside"]
    rows = []
    for f in sorted(BOOK.glob("0*/images/*.svg")):
        t = f.read_text()
        vb = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', t)
        widths = [float(s) for s in re.findall(r'stroke-width[=:]\s*"?([\d.]+)', t) if float(s) > 0]
        if vb and widths:
            scale = min(width_mm / float(vb.group(1)), 200 / float(vb.group(2)))
            rows.append((min(widths) * scale / 0.3528, f.relative_to(BOOK).as_posix()))
    return sorted(rows)


def check_print(pdf):
    """Check the print PDF against the print-on-demand services' interior rules, and write build/print-check.txt.
    Hard rules stop the build; the drawings' small text is reported as a warning (see OPEN-ITEMS, Q172)."""
    from pypdf import PdfReader
    reader = PdfReader(pdf)
    n = len(reader.pages)
    errors, notes = [], []
    sizes = {(round(float(p.mediabox.width), 1), round(float(p.mediabox.height), 1)) for p in reader.pages}
    if sizes != {(612.0, 792.0)}:
        errors.append(f"every page must be exactly 8.5 x 11 in (612 x 792 pt); found {sorted(sizes)}")
    if n % 2:
        errors.append(f"the page count must be even; it is {n}")
    if not KDP_PAGES[0] <= n <= KDP_PAGES[1]:
        errors.append(f"KDP prints 8.5 x 11 in color books of {KDP_PAGES[0]} to {KDP_PAGES[1]} pages "
                      f"(standard color from 72, premium color up to 590); this one has {n}")
    annots = sum(len(p.get("/Annots", []) or []) for p in reader.pages)
    if annots or "/Outlines" in reader.trailer["/Root"] or "/Metadata" in reader.trailer["/Root"] or reader.metadata:
        errors.append("KDP asks for no bookmarks, annotations or metadata in the print file; "
                      f"found {annots} annotations, outline {'/Outlines' in reader.trailer['/Root']}, metadata {bool(reader.metadata) or '/Metadata' in reader.trailer['/Root']}")
    transparent = 0
    for p in reader.pages:
        states = (p.get("/Resources") or {}).get("/ExtGState")
        for v in (states.get_object().values() if states else []):
            v = v.get_object()
            if float(v.get("/CA", 1)) < 1 or float(v.get("/ca", 1)) < 1 or str(v.get("/SMask", "/None")) != "/None":
                transparent += 1
        xobjects = (p.get("/Resources") or {}).get("/XObject")
        for x in (xobjects.get_object().values() if xobjects else []):
            if "/SMask" in x.get_object():
                transparent += 1
    if transparent:
        errors.append(f"both services ask for transparency to be flattened; found {transparent} transparent objects")
    need = next((g for limit, g in KDP_GUTTER_IN if n <= limit), None)
    inside_in = PRINT_MARGINS["inside"] / MM_PER_IN
    if need is None or inside_in < need:
        errors.append(f"KDP needs an inside margin of at least {need} in for {n} pages; it is {inside_in:.2f} in")
    if inside_in < LULU_SAFETY_IN + LULU_GUTTER_IN:
        errors.append(f"Lulu needs at least {LULU_SAFETY_IN + LULU_GUTTER_IN} in on the inside; it is {inside_in:.2f} in")
    # Every word on every page must sit inside the safety margin, running heads and page numbers included.
    bbox = subprocess.run(["pdftotext", "-bbox", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    closest = 1e9
    for page in re.findall(r"<page [^>]*>(.*?)</page>", bbox, re.S):
        for x0, y0, x1, y1 in re.findall(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)"', page):
            x0, y0, x1, y1 = map(float, (x0, y0, x1, y1))
            closest = min(closest, x0, y0, 612 - x1, 792 - y1)
    if closest / 72 < LULU_SAFETY_IN:
        errors.append(f"some text is {closest / 72:.2f} in from the trim edge; Lulu's safety margin is {LULU_SAFETY_IN} in")
    fonts = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True, check=True).stdout.splitlines()[2:]
    if [f for f in fonts if f.split()[-5:-4] == ["no"]]:
        errors.append("some fonts are not embedded")
    thin = [r for r in thinnest_drawing_line_pt() if r[0] < KDP_MIN_LINE_PT]
    if thin:
        notes.append(f"{len(thin)} drawings have lines thinner than KDP's {KDP_MIN_LINE_PT} pt minimum at print size; the thinnest is "
                     f"{thin[0][0]:.2f} pt ({thin[0][1]}). To fix with the drawing text (Q172).")
    small = [r for r in smallest_drawing_text_pt() if r[0] < 7]
    if small:
        notes.append(f"{len(small)} drawings have text smaller than KDP's 7 pt minimum at print size; the smallest is "
                     f"{small[0][0]:.1f} pt ({small[0][1]}). Decision pending (Q172).")
    report = [f"Print check for {pdf.name}: {n} pages, 8.5 x 11 in, no bleed, cover in a separate file.",
              f"Inside margin {inside_in:.2f} in (KDP needs {need} in for {n} pages, Lulu {LULU_SAFETY_IN + LULU_GUTTER_IN} in).",
              f"Closest text to a trim edge: {closest / 72:.2f} in (Lulu's safety margin is {LULU_SAFETY_IN} in).",
              "Fonts: all embedded." if not any("fonts" in e for e in errors) else "Fonts: NOT all embedded."]
    report += [f"ERROR: {e}" for e in errors] + [f"WARNING: {w}" for w in notes]
    (OUT / "print-check.txt").write_text("\n".join(report) + "\n")
    print("\n".join(report))
    if errors:
        sys.exit("build_books: the print PDF doesn't meet the print-on-demand rules.")


# The fonts the EPUB carries (FONT1): text, bold, italic, code and the symbols. tools/books/epub.css names them;
# a reader can still choose their own font in the e-reader's settings.
EPUB_FONTS = [ROOT / "fonts" / f for f in (
    "AtkinsonHyperlegibleNext-Regular.ttf", "AtkinsonHyperlegibleNext-Bold.ttf",
    "AtkinsonHyperlegibleNext-Italic.ttf", "AtkinsonHyperlegibleNext-BoldItalic.ttf",
    "AtkinsonHyperlegibleMono-Regular.ttf", "OpenDFXSymbols-Regular.otf", "OpenDFXSymbols-Bold.otf")]


def build_epub(pages, titles):
    """The EPUB, made by pandoc from the same HTML as the PDF, without the PDF's cover page and contents list
    (an e-reader shows its own), with the accessibility metadata from tools/books/epub-metadata.xml."""
    OUT.mkdir(exist_ok=True)
    out = OUT / f"{NAME}.epub"
    doc = document(pages, titles, "")
    doc = re.sub(r'<section class="cover".*?</section>', "", doc, flags=re.S)
    doc = re.sub(r'<nav class="toc".*?</nav>', "", doc, flags=re.S)
    doc = re.sub(r"</?section[^>]*>", "", doc)  # pandoc splits chapters only at top-level headings
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "book.html"
        src.write_text(doc)
        subprocess.run([
            "pandoc", str(src), "-f", "html", "-t", "epub3", "-o", str(out),
            "--epub-cover-image", str(COVER_PNG),
            "--css", str(TOOLS / "books" / "epub.css"),
            "--epub-metadata", str(TOOLS / "books" / "epub-metadata.xml"),
            "--metadata", "title=OpenDFX for Printed Circuit Boards",
            "--metadata", "author=Chris Denney", "--metadata", "lang=en-US",
            "--split-level=2", "--toc", "--toc-depth=2",
        ] + [f"--epub-embed-font={f}" for f in EPUB_FONTS], check=True)
    add_accessibility_metadata(out)
    return out


A11Y = """
    <meta property="schema:accessMode">textual</meta>
    <meta property="schema:accessMode">visual</meta>
    <meta property="schema:accessModeSufficient">textual</meta>
    <meta property="schema:accessibilityFeature">alternativeText</meta>
    <meta property="schema:accessibilityFeature">longDescription</meta>
    <meta property="schema:accessibilityFeature">structuralNavigation</meta>
    <meta property="schema:accessibilityFeature">tableOfContents</meta>
    <meta property="schema:accessibilityFeature">readingOrder</meta>
    <meta property="schema:accessibilityFeature">displayTransformability</meta>
    <meta property="schema:accessibilityHazard">none</meta>
    <meta property="schema:accessibilitySummary">Every drawing has alternative text and a written caption that describes it in full, so no fact is given only in a picture. Headings follow the book's structure: part, page and recommendation. Text can be resized and restyled by the reading system.</meta>
"""


def add_accessibility_metadata(epub):
    """Write the EPUB Accessibility metadata into the package file. Pandoc keeps only Dublin Core metadata,
    so these are added after it runs. Pandoc 3.1 also names the SVG drawings .svgz although they aren't compressed,
    which some reading systems misread, so they are renamed .svg. The mimetype entry must stay first and uncompressed."""
    import zipfile
    tmp = epub.with_suffix(".tmp")
    with zipfile.ZipFile(epub) as zin, zipfile.ZipFile(tmp, "w") as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.endswith((".opf", ".xhtml", ".ncx")):
                text = data.decode().replace(".svgz", ".svg").replace("_svgz", "_svg")
                if item.filename.endswith(".opf"):
                    text = text.replace("</metadata>", A11Y + "  </metadata>", 1)
                    text = text.replace('<package version="3.0"', '<package version="3.0" xml:lang="en-US"', 1)
                if item.filename.endswith("nav.xhtml"):
                    text = text.replace('<nav epub:type="toc"', '<nav epub:type="toc" role="doc-toc"', 1)
                data = text.encode()
            if item.filename.endswith(".svgz"):
                item.filename = item.filename[:-1]
            compress = zipfile.ZIP_STORED if item.filename == "mimetype" else zipfile.ZIP_DEFLATED
            zout.writestr(item, data, compress_type=compress)
    tmp.replace(epub)


def build_sample(out_path, titles):
    """A short PDF for reviewing the look: front matter, contents, the rails page and the start of the glossary."""
    from pypdf import PdfReader, PdfWriter
    pages = ["02-the-panel/02-rails-tooling-holes-fiducials.md", "09-appendices/03-glossary.md"]
    with tempfile.TemporaryDirectory() as tmp:
        full = Path(tmp) / "sample.pdf"
        weasy(pdf_images(document(pages, titles, css("screen"))), full)
        reader = PdfReader(full)
        n = len(reader.pages)
        keep = list(range(min(n, 18)))  # front matter, the rails page and a first glossary page
        writer = PdfWriter(clone_from=full)
        for i in reversed(range(n)):
            if i not in keep:
                writer.remove_page(i)
        writer.write(out_path)
    return out_path


def main():
    if not shutil.which("pandoc"):
        sys.exit("build_books needs pandoc (https://pandoc.org).")
    titles = ba.parts()
    pages = book_pages()
    if "--sample" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--sample") + 1])
        print(f"Wrote {build_sample(out, titles)}")
        return
    made = [build_pdf("screen", pages, titles)]
    if "--print" in sys.argv:
        made.append(build_pdf("print", pages, titles))
    made.append(build_epub(pages, titles))
    for path in made:
        print(f"Wrote {path.relative_to(ROOT)} ({path.stat().st_size // 1024} KB)")
    if "--site" in sys.argv:
        site = Path(sys.argv[sys.argv.index("--site") + 1])
        shutil.copy(OUT / f"{NAME}.pdf", site / "opendfx-pcb.pdf")
        shutil.copy(OUT / f"{NAME}.epub", site / "opendfx-pcb.epub")
        print(f"Copied the PDF and EPUB into {site}")


if __name__ == "__main__":
    main()

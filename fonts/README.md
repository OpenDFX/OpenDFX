# The book's fonts

The book, the drawings, the cover and the website use **Atkinson Hyperlegible Next**, a typeface designed for readers with low vision, with **Atkinson Hyperlegible Mono** for code (Q182, FONT1).
Its zero has a slash, so a zero can't be mistaken for the letter O in a value or a recommendation ID.

All the fonts here are licensed under the SIL Open Font License 1.1 (`OFL.txt`), not under the book's or the code's license.

| File | What it is for |
|---|---|
| `source/` | The upstream variable fonts (version 2.001, from the Google Fonts repository) and their licenses. Never edited. |
| `AtkinsonHyperlegibleNext-*.ttf`, `AtkinsonHyperlegibleMono-*.ttf` | Static weights for the PDF build and for embedding in the drawings. |
| `OpenDFXSymbols-*.otf` | A small subset of Inter holding the symbols Atkinson doesn't have: the check mark, the cross, the star, the warning sign and the arrows. Every font list names it straight after Atkinson. |
| `../site/static/fonts/*.woff2` | The website's copies (variable fonts, one file for every weight). |

`python3 tools/build_fonts.py` makes all of them from `source/` (`--check` reports stale files).
Atkinson has the Greek letters mu and omega but not the micro sign (µ, U+00B5) or the ohm sign (U+2126), so the script adds both, drawn with the Greek letters.
Needs `pip install fonttools brotli`, and Ubuntu's `fonts-inter` package to rebuild OpenDFX Symbols.

## Where each one is used

- **PDF:** `tools/books/book.css` loads the static fonts with `@font-face`, so nothing needs installing.
- **EPUB:** `tools/build_books.py` embeds the regular, bold and italic weights and the symbols; e-readers still let readers choose their own font.
- **Drawings:** the drawing kit (`tools/diagrams/opendfx_draw.py`) puts a subset of each weight a drawing uses inside the drawing itself, holding only the characters it uses. A drawing shown on a web page can't use the page's fonts, so without this a reader who doesn't have Atkinson installed would see another font. The drawings for the print PDF are drawn by Chromium from the same files.
- **Cover:** `tools/cover/make_cover.py` embeds a subset the same way.
- **Website:** `site/src/styles/opendfx.css` loads the woff2 copies.

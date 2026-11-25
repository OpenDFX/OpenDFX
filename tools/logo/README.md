# The OpenDFX logo

The logo is an open solder jumper: two D-shaped copper pads facing each other across a gap, inside a white
legend outline that is broken where the jumper is open. The pads together make an O, and each one is a D.
Chris chose it on 2026-11-15 (Q227, Q233) after six rounds of drafts. It is K6 from round 5 (L0 in round 6).

- `build_brand.py` draws every logo file from one definition and writes the press kit into `public/brand/`
  (served at opendfx.org/brand/ and zipped by `tools/build_site.py` as `/opendfx-brand.zip`), plus
  `public/favicon.svg`, `favicon.ico` and `apple-touch-icon.png`. `--check` reports SVG files that are out of
  date; the website workflow runs it. The PNG files are drawn by Chromium with `render_png.js`.
  Needs `pip install fonttools uharfbuzz pillow`, node and Playwright.
- The rules, colors and downloads are on the website page `site/src/content/docs/brand.md` (`/brand/`).
- `glyphs.py` turns text into outlines in Atkinson Hyperlegible Next, so no logo file needs a font.
- The six rounds of drafts that led to the logo were moved to the private sources repository
  (`marketing/logo-drafts/`, Q239).

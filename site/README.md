# The OpenDFX website

The website at https://opendfx.org (M9), built with [Starlight](https://starlight.astro.build).
Its pages are not written here: `tools/build_site.py` copies them from `book/` every time the site is built.
To change what the site says, edit the page in `book/`.

## What lives where

| Path | What it is |
|---|---|
| `src/content/docs/index.mdx` | The home page (written by hand). |
| `src/content/docs/about.md` | The About page (written by hand, from M6). |
| `src/content/docs/404.md` | The "page not found" page. |
| `src/pages/[id].astro` | The short permanent address for each recommendation, such as `/PCB-DFA-006/`, which forwards to its place in the book (Q136). |
| `src/components/Footer.astro` | Adds the author line to the foot of every page. |
| `src/styles/opendfx.css` | Colors and small layout changes. |
| `src/plugins/` | Small fixes to how Markdown is turned into HTML. |
| `static/` | Files copied to the site's root as they are, such as `CNAME`. |

Generated on each build, and Git-ignored: the book's pages in `src/content/docs/0*/`, the sidebar and the permanent-address list in `src/generated/`, and `public/` (a copy of the repository's `public/` and `data/`).

## Building it

You need Node 22 and Python 3 with PyYAML.

```sh
cd site
npm ci           # once
npm run dev      # a live preview at http://localhost:4321
npm run build    # the finished site, in site/dist/
```

`npm run build` fails if any link or heading anchor in the book is broken, and then checks that every permanent address lands on its recommendation.

## Publishing

`.github/workflows/website.yml` builds the site on every pull request and publishes it to GitHub Pages whenever `main` changes.
Publishing is switched off until the repository variable `PAGES_ENABLED` is set to `true` (Settings, then Secrets and variables, then Actions, then Variables). Set it once GitHub Pages is turned on, after the repository goes public. Until then, every change is still built and checked.
Run `python3 tools/build_data.py` and `python3 tools/build_appendices.py` after changing a page, as before: the workflow refuses to publish if the data files are out of date.

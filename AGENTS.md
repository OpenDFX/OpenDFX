# Instructions for AI agents working on OpenDFX

This repository is the source of OpenDFX for Printed Circuit Boards, an open book of recommendations for designing circuit boards that are easy to make, assemble and test.
Read `CONTRIBUTING.md` first: these instructions are a short version of it for an AI agent helping someone contribute.

If you want to use the book while designing a board, rather than change it, read `book/00-start-here/05-using-this-book-with-an-ai-agent.md` instead, and see https://opendfx.org/ai/ to set up your AI tool.
This file is for changing the book, so don't copy it into your own PCB project.

## Where things are

- `book/`: the book's pages, in Markdown, one folder per part. `book/TEMPLATE.md` shows the layout of a page and what each section is for.
- `data/`: the recommendations as JSON and YAML, made from the pages. Don't edit these by hand.
- `site/`: the website. Its pages are copied from `book/` on every build, so edit the book, never the copies.
- `kicad/`: the KiCad design-rules file, the starter project and the release checker.
- `tools/`: the scripts that build everything. `tools/diagrams/` draws the drawings.
- `python/`: the `opendfx` package for PyPI.

## Rules for changing the book

1. **Recommendations, not rules.** Prefer "avoid" to "never". Give a minimum and a recommended value wherever possible.
2. **Permanent IDs.** Each recommendation has an ID such as `PCB-DFM-014`. Never renumber, reuse or delete an ID. A new recommendation gets its ID from the maintainer; ask rather than choosing one.
3. **Plain words.** Whole sentences, one idea each. Give each number its own sentence, and say what it is for. No shorthand such as "min" or "+/−". A hole has a diameter, not a width "across". US spelling.
4. **One sentence per line** in the Markdown, with a blank line between paragraphs. `python3 tools/one_sentence_per_line.py <file>` rewraps a page safely.
5. **No names** of people or companies in the advice or stories. Standards such as IPC-7351 are fine.
6. **Sources** for every recommendation: standards by number and title; podcast episodes by full title, linked, with the date and timestamps.
7. **Drawings** are made with the kit in `tools/diagrams/`. Follow `tools/diagrams/README.md`. Alt text and captions start with the drawing's D-number. No fact may live only in a drawing.
8. **Don't paste** text or figures from standards, datasheets or other books. Describe them in your own words and cite them.

## Before you finish

```bash
python3 tools/build_all.py
python3 tools/build_all.py --check
```

The first rebuilds the appendices, the data file, `llms.txt`, the KiCad rules file and the Agent Skill from the pages.
The second must report that everything is up to date.
Commit what the first one changed together with your edit.

To check the website builds with no broken links: `cd site && npm ci && npm run build`.

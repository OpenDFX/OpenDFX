# Change log

Every version of OpenDFX for Printed Circuit Boards, newest first.
Each change names the recommendations it touches, by ID.
Everyone whose report or pull request is used is credited by their GitHub username.

A recommendation's ID never changes, so a link to `opendfx.org/<ID>` always leads to the current version of that recommendation.
The book's version is in `CITATION.cff`, and on the title page of the PDF and EPUB.

## Version 1.0, released 2026-11-25

The first public release.

- 192 recommendations: 128 on design for assembly (DFA), 45 on design for manufacturing (DFM) and 19 on design for test (DFT).
- 69 drawings, each drawn to scale in the board color key.
- The book follows the path a board takes through a factory, in nine parts: start here, the design package, the panel, bare-board fabrication, components and materials, assembly, test and programming, handling, packaging and shipping, and working with a manufacturer.
- The appendices: a checklist to run before you release a design, an index of the recommendations by design stage, a glossary, the standards cited, and the sources.
- The website, [opendfx.org](https://opendfx.org), with a permanent address for every recommendation, such as `opendfx.org/PCB-DFA-007`.
- A PDF and an EPUB of the whole book.
- The recommendations as data, in JSON and YAML, with a JSON Schema.
- `llms.txt`, `llms-full.txt`, and a Markdown copy of every page and every recommendation, for AI tools. Each recommendation in them gives its permanent address under its heading, so AI tools quote it.
- An Agent Skill, so AI agents can follow the book while they design a board.
- A setup page for AI tools, [opendfx.org/ai](https://opendfx.org/ai/): three steps for any AI chat tool (download one file, attach it to a new chat, paste one prompt), and notes on projects, the Agent Skill and coding agents.
- A design-rules file for KiCad 10, with a starter project.
- A release checker that reports which recommendations a set of release files meets.
- The `opendfx` package on PyPI, with the data, the rules file and the release checker.

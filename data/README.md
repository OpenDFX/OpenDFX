# Recommendations data

These files hold every recommendation in *OpenDFX for Printed Circuit Boards* as structured data, for people and tools that want the advice without reading the whole book.
`recommendations.json` and `recommendations.yaml` hold the same records.

They are generated from the book's pages by `tools/build_data.py`, so don't edit them by hand.
Edit the page and run the script.
The same script writes `llms.txt`, `llms-full.txt` and `robots.txt` into `public/`, which the website serves at its root.

The data is licensed [CC BY 4.0](../LICENSE-DATA).
Credit "OpenDFX for Printed Circuit Boards by Chris Denney" with a link to https://opendfx.org.
The book's text is licensed CC BY-SA 4.0.
The top of `recommendations.json` also gives `attribution`, the credit line, and `citation`, the full citation for a paper or a report.
The book's citation details are in [`CITATION.cff`](../CITATION.cff), and the website's [How to cite](https://opendfx.org/cite/) page explains them.

`recommendations.schema.json` is a [JSON Schema](https://json-schema.org/) that describes every field, so other tools can check the data before they use it.
`tools/build_data.py` checks the data against it every time it runs.

The website also publishes every recommendation on its own as Markdown, at its permanent address with `.md` added, such as `https://opendfx.org/PCB-DFA-006.md`.

These are recommendations, not rules.
Each record links to its page in the book, which has the drawings and the full discussion.

## Fields

Each record in `recommendations` has these fields.
Text fields are Markdown, with links written as full website addresses.

| Field | What it holds |
|---|---|
| `id` | The permanent ID, for example `PCB-DFA-006`. It never changes and is never reused. |
| `title` | The recommendation as one short sentence. |
| `category` | `DFA` (assembly), `DFM` (bare-board fabrication) or `DFT` (test). |
| `category_name` | The category in words. |
| `part`, `part_title` | The part of the book it is in. |
| `page_title` | The page it is on. |
| `permalink` | The recommendation's short permanent address, such as `https://opendfx.org/PCB-DFA-006`. It forwards to the recommendation and never changes, so use it when you link or cite. |
| `url` | The address of the recommendation on its page. It can change if the page moves or the title is reworded. |
| `source_file` | The page's Markdown file in this repository. |
| `design_stages` | When in the design it applies: `parts`, `library`, `placement`, `routing`, `outline`, `release` or `production`. |
| `recommendation` | What to do. |
| `why` | How the problem happens. |
| `typical_values` | The numbers, as written text, and whether they are common industry values or one manufacturer's example. Not every recommendation has one. |
| `what_goes_wrong` | What you will see, and what it costs you, if you don't follow it. Not every recommendation has one. |
| `example` | A short true story from the factory floor. Not every recommendation has one. |
| `applies_to` | Whether it is general practice or varies by manufacturer. |
| `checks` | Only on the recommendations the [KiCad design-rules file](https://opendfx.org/kicad/) checks. Each entry gives `check`, what is checked, with its `minimum` and `recommended` values as numbers and their `unit`. The numbers are the book's own; the written text in `typical_values` stays the full story. |
| `figures` | The drawings in that recommendation, each with its D-number, alt text and address. |
| `sources.text` | The sources as written in the book. |
| `sources.episodes` | Each podcast episode cited, with its title, address, date and timestamps in seconds. |
| `sources.standards` | Each standard cited, such as `IPC-6012F`. |
| `sources.other` | Other published documents cited, with their addresses. |
| `last_reviewed` | The date the author last reviewed it. |

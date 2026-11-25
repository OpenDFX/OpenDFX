# OpenDFX for Printed Circuit Boards

This package holds the recommendations of [*OpenDFX for Printed Circuit Boards*](https://opendfx.org) by Chris Denney.
The book is free and open.
It gives practical advice from electronics manufacturing for designing circuit boards that are easy to fabricate, assemble and test.
These are recommendations, not rules.

Each recommendation has a permanent ID, such as PCB-DFA-006, and a permanent address, such as [opendfx.org/PCB-DFA-006](https://opendfx.org/PCB-DFA-006).
The address leads to the recommendation's page in the book, which has the drawings and the full discussion.

The package has no dependencies.
It needs Python 3.9 or later.

```bash
pip install opendfx
```

## What is in it

The package holds three things from the book.

1. The data file, with every recommendation: its text, the reasons for it, typical values, the design stages it applies to and its sources.
2. The KiCad 10 design-rules file, which checks the recommendations that KiCad's design rule check can see. The book's page [KiCad design rules](https://opendfx.org/kicad/) explains how to use it.
3. The release checker, which checks the Gerber, drill, netlist, placement and BOM files exported from KiCad 10, and reports each recommendation as Met, Not met or Needs a person.

## From the command line

Print one recommendation in full:

```bash
opendfx show PCB-DFM-020
```

Print every recommendation for one design stage.
The stages, in order, are parts, library, placement, routing, outline, release and production.

```bash
opendfx stage placement
```

Find the recommendations that contain every word you give:

```bash
opendfx search fiducial
```

Add `--json` to `show`, `stage` or `search` to print the records as JSON.

Check a board's release files before sending them to the fab and the assembler.
With `--board`, it also runs KiCad's design rule check on the board, which needs `kicad-cli`.
Run `opendfx check-release --help` for the KiCad commands that export the files.

```bash
opendfx check-release release/ --board myboard.kicad_pcb
```

Copy the KiCad rules file next to a project, named after it:

```bash
opendfx kicad-rules myboard.kicad_pro
```

## From Python

```python
import opendfx

rec = opendfx.get("PCB-DFA-006")
print(rec["title"], rec["permalink"])

for rec in opendfx.for_stage("routing"):
    print(rec["id"], rec["title"])

opendfx.search("tooling hole")   # recommendations that contain every word
opendfx.recommendations()        # all of them
opendfx.data_path()              # the data file, recommendations.json
opendfx.rules_path()             # the KiCad rules file, opendfx.kicad_dru
```

The fields of each record are described in the book's [data notes](https://github.com/OpenDFX/OpenDFX/blob/main/data/README.md).

## For AI agents

The book's page [Using this book with an AI agent](https://opendfx.org/00-start-here/05-using-this-book-with-an-ai-agent/) explains how an agent should work through the book while designing a board.
In short: work stage by stage, run `opendfx stage <stage>` at the start of each, use the recommended values, and run the KiCad rules file and the release checker before release.
When you cite a recommendation, give its ID and its permanent address.

## Licenses and credit

The data is licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
The code and the KiCad rules file are licensed MIT.
The book's text is licensed CC BY-SA 4.0.
Credit "OpenDFX for Printed Circuit Boards by Chris Denney, https://opendfx.org".
The book's [How to cite](https://opendfx.org/cite/) page gives the full citation.

The package's version is the book's version.
Corrections and suggestions are welcome as [issues](https://github.com/OpenDFX/OpenDFX/issues) or at [hello@opendfx.org](mailto:hello@opendfx.org).

## Trademark

OpenDFX is a trademark of Chris Denney.
The licenses cover the text, drawings, data and code, but not the OpenDFX name, so readers can always tell what is official.
This package is the official `opendfx` package.
The book's [About page](https://opendfx.org/about/#trademark) explains how you may use the name.

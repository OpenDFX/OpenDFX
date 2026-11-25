# Contributing to OpenDFX

Thank you for helping.
OpenDFX began as one engineer's experience in one part of the industry.
It gets better every time someone who designs, builds or tests circuit boards tells us where it's wrong, what it's missing, or how they do it differently.

You don't need to write code, or know Git, to help.
Most contributions start as an issue: a short form on GitHub.

Everyone taking part follows the [code of conduct](CODE_OF_CONDUCT.md).

## Ways to help

### Report a mistake

If a recommendation is wrong, out of date or unclear, [open a correction](https://github.com/OpenDFX/OpenDFX/issues/new/choose).
A good correction gives:

1. The recommendation's ID, such as `PCB-DFA-007`, or the page's web address.
2. What is wrong.
3. What it should say instead.
4. The evidence. A standard, a datasheet, a fab's or assembler's published guideline, or your own experience on the line are all welcome. Say which it is.

Small fixes, such as a typo or a broken link, need only a sentence.

### Tell us you do it differently

Many recommendations are the practice of one factory.
If your factory or design team does something differently, and it works, we want to know.
[Open a "We do it differently" issue](https://github.com/OpenDFX/OpenDFX/issues/new/choose), say how you do it and why, and what kind of boards and volumes you build.
When good practices differ, the book should say so, and say what each choice gives up.

### Suggest a new recommendation

[Open a "Suggest a new recommendation" issue](https://github.com/OpenDFX/OpenDFX/issues/new/choose) with the problem it prevents, the advice, the values, and the evidence.
Once it's agreed, you or the maintainer write it up.
New recommendations get their permanent ID from the maintainer when they're merged.

### Send a pull request

Pull requests are welcome for anything: a corrected value, a clearer sentence, a better drawing, a fix to the website or the tools, or a rules file for another design tool.
For anything bigger than a small fix, please open an issue first, so we can agree what to do before you spend time on it.

## Who decides

OpenDFX is run in the open, like many open-source projects.
Most decisions are made by agreement, in issues and pull requests, where anyone can take part.
When people can't agree, the maintainer, Chris Denney, weighs the arguments and the evidence, makes the decision, and explains it.
A decision can always be reopened when new evidence turns up.
Every decision serves the same aim: a free, vendor-neutral reference on circuit board design that is accurate, clear and kept up to date.

As the project grows, the maintainer may name co-maintainers to look after a part of the book or the tools.
They will be listed here.
If you'd like to help maintain a part of OpenDFX, say so in an issue.

## How changes are reviewed

The maintainer reviews every change to a recommendation before it is merged.
When he does, the recommendation's "Last reviewed" date changes.
Changes to the website and the tools are reviewed the same way.

Every change is listed in the [change log](CHANGELOG.md) under the next version, with its recommendation IDs.
Everyone whose report or pull request is used is credited there by their GitHub username.
If you'd rather not be credited, say so in your issue or pull request.

## Permanent IDs

Every recommendation has an ID such as `PCB-DFM-014`: the board type, which kind of advice it is, and a number.

- `DFM` is design for manufacturing: making the bare board.
- `DFA` is design for assembly, including panels and fiducials. Advice that fits both fabrication and assembly goes under DFA.
- `DFT` is design for test.

IDs are permanent.
People cite them in design reviews, and every ID has a web address, such as `opendfx.org/PCB-DFM-014`.
So an ID is never reused or renumbered, even when its recommendation moves to another page.
If a recommendation is withdrawn, its ID is retired and stays retired.

## How the book is written

The book's pages are Markdown files in [`book/`](book/), one folder per part.
[`book/TEMPLATE.md`](book/TEMPLATE.md) shows the layout of a page and what each section is for.

### Recommendations, not rules

Write recommendations, not rules.
Prefer "avoid" to "never", and say what a designer gives up when they choose something else.
Give a minimum value and a recommended value wherever you can.

### Plain words, whole sentences

The book is for professional engineers, so the words matter.

- Write whole sentences, with one idea in each.
- Use ordinary connecting words, such as "so", "but" and "because".
- Give each number its own sentence. Don't pack several into one line with commas, slashes or brackets.
- Say what a number is for: "at least 3 mm from the edge of the board", not "3 mm from the edge".
- Spell words out. Avoid shorthand such as "min", "rec." and "+/−".
- Use the correct technical term. A hole or a round pad has a diameter: "3 mm in diameter", not "3 mm across".
- Use US spelling: color, center, aluminum, labeled, gray.

### One sentence per line

In the Markdown files, put each sentence on its own line, and leave a blank line between paragraphs.
This lets reviewers comment on an exact sentence, and keeps changes small and easy to read.
`python3 tools/one_sentence_per_line.py <file>` rewraps a page for you, and refuses to write if the page would look different.

### No names

Don't name people or companies in the advice or the stories, including fabs, assemblers, distributors and tool vendors.
Write "a customer" or "one assembler" instead.
Standards bodies and their standards, such as IPC-7351, are fine.
The book recommends practices, not suppliers.

### Sources

Give a source for every recommendation.
Name standards with their number and title.
For podcast episodes, give the full published title, linked to the episode's page, with the date and the timestamps.

### Drawings

Drawings are made in Python with the shared style kit in [`tools/diagrams/`](tools/diagrams/), drawn to scale in the board color key.
[`tools/diagrams/README.md`](tools/diagrams/README.md) explains the kit, the colors and the rules.
Each drawing's alt text and caption start with its D-number, such as "D24 is drawn to scale…".
No fact may live only in a drawing: every number in a drawing must also be in the text.
If you'd like a drawing but don't want to make it, describe it in an issue.

## Building it yourself

Several files are made from the book's pages: the appendices, the data file, `llms.txt`, the KiCad rules file and the Agent Skill.
After you edit a page, rebuild them all with one command, and commit what it changes:

```bash
pip install pyyaml jsonschema
python3 tools/build_all.py
```

`python3 tools/build_all.py --check` tells you if anything is out of date.
Every pull request runs the same check.

To see the website as it will look:

```bash
cd site
npm ci
npm run dev
```

`npm run build` builds the whole site, and fails on any broken link.
The pull request checks also build the PDF and the EPUB, and check every page for accessibility.
You don't need to run those yourself; GitHub runs them on your pull request.

## License of contributions

Contributions are accepted under the same licenses as the files they change.
There is no agreement to sign.

- Book text and drawings: [CC BY-SA 4.0](LICENSE).
- The recommendations data files: [CC BY 4.0](LICENSE-DATA).
- Code, the KiCad design-rules file and the Agent Skill's scripts: the [MIT License](LICENSE-CODE).

Only contribute work that you have the right to share under these licenses.
Please don't paste text or figures from standards, datasheets or other books.
Describe what they say in your own words, and cite them.

## Questions

Ask in an issue, or write to [hello@opendfx.org](mailto:hello@opendfx.org) for anything private.

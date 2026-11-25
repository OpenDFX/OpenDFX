<p>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="public/brand/opendfx-logo-green-on-dark.svg">
    <img src="public/brand/opendfx-logo-green.svg" alt="OpenDFX" height="72">
  </picture>
</p>

# OpenDFX™ for Printed Circuit Boards

**A free, open-source book of practical advice for designing circuit boards that are easy to make, assemble and test.
It is written for engineers, and for the AI tools that now help them design boards.**

The book holds 192 recommendations.
Each one says what to do, why it matters, and what goes wrong if you don't.
Where it can, it gives a minimum value and a recommended value.
Most come with a drawing made to scale.

Every recommendation has a permanent ID, such as `PCB-DFA-007`, and its own short web address, such as [opendfx.org/PCB-DFA-007](https://opendfx.org/PCB-DFA-007).
The IDs never change, so you can cite one in a design review, a fab note or a ticket.

The book is written by Chris Denney, from more than 25 years in electronics manufacturing at Worthington Assembly and CircuitHub, and from six years of the Pick, Place, Podcast.
It is open so that people across the industry can correct it and add to it.

## Read it

- **On the website:** [opendfx.org](https://opendfx.org).
- **As a PDF:** [opendfx.org/opendfx-pcb.pdf](https://opendfx.org/opendfx-pcb.pdf), for reading on a screen, printing or sending to a colleague.
- **As an EPUB:** [opendfx.org/opendfx-pcb.epub](https://opendfx.org/opendfx-pcb.epub), for e-readers and phones.
- **In this repository:** the pages are plain Markdown in [`book/`](book/).

## Give it to your AI agent

**Set up your tool:** [opendfx.org/ai](https://opendfx.org/ai/) gives the book to any AI chat tool in three steps: download one file, attach it to a new chat, and paste one prompt.
It also covers projects, the Agent Skill and coding agents.

- **The Agent Skill:** download [opendfx.org/opendfx-pcb-design.zip](https://opendfx.org/opendfx-pcb-design.zip) and add it to any tool that supports Agent Skills. In a coding agent, put it in your own PCB project.
- **The whole book as one file:** download [opendfx.org/llms-full.txt](https://opendfx.org/llms-full.txt) and attach it to a chat or a project.
- **Your project's instructions:** paste the block from [Using this book with an AI agent](https://opendfx.org/00-start-here/05-using-this-book-with-an-ai-agent/) into `CLAUDE.md`, `AGENTS.md`, Cursor's rules or Copilot's instructions. This repository's own `AGENTS.md` is for changing the book, so don't copy it into your project.
- **The data:** every recommendation is a record in [`data/recommendations.json`](data/recommendations.json) and [`.yaml`](data/recommendations.yaml), described in [`data/README.md`](data/README.md).
- **For language models:** [opendfx.org/llms.txt](https://opendfx.org/llms.txt) is a short index of the book. Every page and every recommendation is also published as Markdown.

## Check your board

- **KiCad design rules:** [`kicad/opendfx.kicad_dru`](kicad/opendfx.kicad_dru) checks a board in KiCad 10 against the book's numbers. Each error names the recommendation behind it. See [opendfx.org/kicad](https://opendfx.org/kicad/) and the [starter project](kicad/opendfx-starter/).
- **The release checker:** [`kicad/check_release.py`](kicad/check_release.py) reads a folder of release files (Gerbers, drill files, IPC-D-356 netlist, placement file and BOM) and reports which recommendations they meet.
- **From Python:** `pip install opendfx` gives you the data, the rules file and the release checker, with an `opendfx` command. See [`python/README.md`](python/README.md).

## Help improve it

OpenDFX gets better every time someone who builds boards tells us where it's wrong, or how they do it differently.
You don't need to write code to help.

- **Found a mistake?** [Report a correction](https://github.com/OpenDFX/OpenDFX/issues/new/choose).
- **Do it differently in your factory or design team?** Tell us how, and why.
- **Want to add something?** Suggest a new recommendation, or send a pull request.

Read [CONTRIBUTING.md](CONTRIBUTING.md) first.
Everyone taking part follows the [code of conduct](CODE_OF_CONDUCT.md).
Contributors are credited in the [change log](CHANGELOG.md).

## License

- **Book text and drawings:** [CC BY-SA 4.0](LICENSE). Share and adapt them freely, including commercially, as long as you credit "OpenDFX by Chris Denney" with a link to https://opendfx.org, and share your changes under the same license.
- **Recommendations data files:** [CC BY 4.0](LICENSE-DATA). Use them in any tool or product, as long as you give credit.
- **Code, the KiCad design-rules file and the Agent Skill's scripts:** [MIT](LICENSE-CODE). Use them in any project, including commercial ones, as long as you keep the copyright notice.
- **Fonts** (in `fonts/`, and the subsets inside each drawing): Atkinson Hyperlegible Next and Mono, and OpenDFX Symbols (a subset of Inter), under the [SIL Open Font License 1.1](fonts/OFL.txt). See [`fonts/README.md`](fonts/README.md).

Contributions are accepted under the same licenses as the files they change.

## How to cite

See [opendfx.org/cite](https://opendfx.org/cite/), or use the "Cite this repository" button on GitHub, which reads [`CITATION.cff`](CITATION.cff).

## Trademark

OpenDFX is a trademark of Chris Denney.
Please share OpenDFX as widely as you can.
Teach from it, quote it, link to it, translate it and build on it, under the licenses above.
The licenses cover the text, drawings, data and code, but not the OpenDFX name, so readers can always tell what is official.
You may say that your work is based on OpenDFX, and the license requires you to credit it.
Please ask before using OpenDFX in a domain name, a software package name, or the name of a social media account or group.
Posts, pages and groups about the book are welcome, as long as they don't look like an official OpenDFX account.
Please don't use the name as the title or brand of your own book, product or service, or in a way that suggests Chris Denney endorses it.
The logo, its colors and how to use them are at [opendfx.org/brand](https://opendfx.org/brand/).
If you're not sure, ask at [hello@opendfx.org](mailto:hello@opendfx.org); the answer is usually yes.

## Contact

[hello@opendfx.org](mailto:hello@opendfx.org)

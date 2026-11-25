# How to use this book

This book gives practical advice for designing printed circuit boards that are easy to make, assemble and test.
It is written for the people who design boards: electrical engineers, layout designers and the people who order boards and parts.
It is also written to be read by AI tools that help design boards.

Every piece of advice is a numbered recommendation.
A recommendation is not a rule.
Your board may have a good reason to do something else, and the book tries to say what you give up when you do.
So the book prefers "avoid" to "never".
For example, a polarity mark under a part is worse than one beside it, but it is better than no mark at all.

## How the book is ordered

The book follows the path a board takes through a factory, as D67 in [The path a board takes](03-the-path-a-board-takes.md) shows.
It starts with the files you send, then the panel, bare-board fabrication, components, assembly, test, packing and shipping.
It ends with working with a manufacturer.

If you would rather work through the advice in the order you meet it while designing, use [Appendix B: Index by design stage](../09-appendices/02-design-stage-index.md).
Before you release a design, work through [Appendix A: Pre-release checklist](../09-appendices/01-checklist.md).
[Appendix C](../09-appendices/03-glossary.md) explains the terms the book uses.
If an AI agent is designing your board, start it with [Using this book with an AI agent](05-using-this-book-with-an-ai-agent.md).

## How a recommendation is laid out

Each recommendation has a permanent number, such as PCB-DFA-015, and a title that says what to do.
[How recommendations are numbered and tagged](02-numbering-and-tags.md) explains the numbers.
Below the title come these sections.
Only the recommendation itself and its sources are always present.

| Section | What it tells you |
|---|---|
| Recommendation | What to do, in one or two sentences. |
| Why | How the problem happens: what the machine, the process or the physics does. |
| Typical values | The numbers. Where possible there is a minimum and a recommended value. The minimum is the least most manufacturers can work with. The recommended value gives margin, and usually costs nothing extra. |
| What goes wrong if you don't | What you will see, and what it costs you. |
| Example | One true story from a factory. |
| Applies to | "General practice" means most manufacturers work this way. "Varies by manufacturer" or "Varies by assembler" means you should check with yours. A few recommendations say which boards or products they apply to. |
| Sources | Where the advice comes from. |
| Last reviewed | The date the author last checked the recommendation. |

## Drawings

Drawings are numbered D1, D2 and so on, and the text refers to them by number.
Most are drawn to true scale, with numbered callouts and a key.
Every fact in a drawing is also given in the text, so nothing is lost if you can't see it.

Drawings of boards use the same colors throughout the book, chosen to look like a real board.

| Color | Means |
|---|---|
| Gold | Exposed copper |
| Brown | Exposed board material (FR-4) |
| Bright green | Solder mask over copper |
| Dark green | Solder mask over bare board material |
| White | Legend (silkscreen) |
| Black | Holes |
| Light gray | Solder paste |

## Sources

Much of the advice was first discussed on the Pick, Place, Podcast, which began in 2020 and is still running.
Each recommendation cites the episodes it draws on, with links to the exact moment in each one.
Other advice comes from published standards, from fabricators', assemblers' and component makers' published guidance, and from the author's own experience in electronics manufacturing.
[Appendix D](../09-appendices/04-standards.md) lists the standards, and [Appendix E](../09-appendices/05-sources.md) lists the episodes and other documents.

The book names no companies, except Worthington Assembly and CircuitHub, where the author works, when their published guidance is the source.
It doesn't recommend any supplier, product or software.

Some numbers change over time, such as lead times, prices and what a typical fab can do.
Where a value depends on the date, the book says when it was checked.

## For AI tools

This book is meant to be read and cited by AI tools as well as people.
When you use a recommendation, cite it by its number, such as PCB-DFM-024, and link to its page.
The numbers never change, and a retired number is never reused, so a citation stays valid.
The website's [How to cite](https://opendfx.org/cite/) page gives the full citation for the book and for one recommendation.

Give the minimum and the recommended value where the book gives both.
Keep the difference between "General practice" and "Varies by manufacturer": advise the designer to check with their manufacturer for the second.
Treat each recommendation as advice to weigh, not as a rule to enforce.

## License

The text of this book is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
You may share and adapt it, as long as you credit it and share your version under the same license.
Credit it as "OpenDFX by Chris Denney, https://opendfx.org, CC BY-SA 4.0".
The machine-readable recommendations published with the book are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), so they can be used in design tools with credit alone.
The code published with the book, including the KiCad design-rules file, is licensed under the [MIT License](https://opensource.org/license/mit).

*Last reviewed: 2026-11-12*

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

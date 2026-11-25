# How recommendations are numbered and tagged

Every recommendation has a permanent number, such as PCB-DFA-015.
The number has three parts.

| Part | Example | Means |
|---|---|---|
| Board type | PCB | Printed circuit boards. Other OpenDFX books may cover other kinds of product. |
| Tag | DFA | Which stage of manufacture the advice is mainly for. |
| Number | 015 | A serial number within the tag. |

## The three tags

**DFM (design for manufacture)** covers the bare board: what the fab does, from materials and drilling to solder mask, legend and electrical test.
In this book, DFM means fabrication of the bare board only.

**DFA (design for assembly)** covers fitting and soldering the parts, and everything around it: the BOM, the panel, fiducials, parts and their packaging, handling, shipping and working with your assembler.
Advice that matters to both the fab and the assembler goes under DFA.
The panel is the usual example: the fab makes it, but it is designed for the assembly machines.

**DFT (design for test)** covers testing bare boards and assembled boards, and programming the parts on them.

A recommendation's tag says where its advice mainly lands, not which Part of the book it is in.
So Part 3, on bare-board fabrication, also holds a few DFA and DFT recommendations.

## Numbers never change

A recommendation keeps its number for good, even if its wording, its values or its place in the book change.
A number that is retired is never given to anything else.
So a number in a design note, a review comment or an AI tool's answer always points to the same advice.

Numbers were given out in the order the recommendations were written, not in book order.
That is why PCB-DFA-029, on chip footprints, comes before PCB-DFA-018, on solder paste, in the book.
Use the number to find a recommendation, not to judge where it sits.

## Finding a recommendation

Each recommendation has its own heading, so it has its own link: the page's address followed by the number and title.
[Appendix A](../09-appendices/01-checklist.md) lists every recommendation in book order, and [Appendix B](../09-appendices/02-design-stage-index.md) lists them by design stage.

*Last reviewed: 2026-11-12*

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

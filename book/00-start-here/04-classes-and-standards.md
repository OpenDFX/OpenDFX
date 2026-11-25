# Classes and standards in one page

Most boards are made and inspected to IPC standards.
IPC is the electronics industry's trade association, now called the Global Electronics Association.
Its standards keep the IPC name, such as IPC-A-610, so the book calls them IPC standards.
This page explains the three IPC classes, which the book refers to often, and lists the standards it uses most.
[Appendix D](../09-appendices/04-standards.md) lists every standard the book mentions.

## The three IPC classes

The IPC standards sort products into three classes.
The class sets what is acceptable in the bare board and in the assembly, such as the size of the annular ring, the thickness of plating in the holes and the shape of each solder joint.

| Class | Meant for | Share of what is built |
|---|---|---|
| Class 1 | General electronic products, where the main need is that the product works. | About 5% |
| Class 2 | Dedicated service products, which should work reliably for a long life but are not critical. Most commercial and industrial products are Class 2. | About 90% |
| Class 3 | High-performance products, which must keep working whenever they are called on, sometimes in harsh conditions. Examples are life-support medical equipment, aerospace and some automotive and military products. | The rest |

Class 3 limits are tighter, so Class 3 boards cost much more to make and inspect.
One estimate is ten times as much or more.
Some Class 3 limits can only be met if the design allows them.
For example, a Class 3 annular ring needs pads big enough for it.
So a board designed to Class 2 doesn't become a Class 3 board because the order says Class 3.

The book's recommendation is to build to Class 2 unless the product truly needs Class 3, and to design for Class 3 from the start if it does.
See [PCB-DFT-003](../03-bare-board-fabrication/11-bare-board-test.md#pcb-dft-003-ask-for-ipc-class-2-unless-the-product-needs-class-3-and-know-class-3-is-a-design-standard-too).

State the class on the fabrication drawing, and on the assembly drawing if it differs.
If you don't, the bare-board standard IPC-6012 defaults to Class 2.
See [PCB-DFM-014](../01-design-package/01-fabrication-data.md#pcb-dfm-014-put-everything-the-gerbers-cant-say-on-the-fabrication-drawing).

## The standards the book uses most

| Standard | What it covers |
|---|---|
| IPC-2221 | How to design a printed board: the generic design standard, including test lands. |
| IPC-7351 | Land patterns (footprints) for surface-mount parts, and the zero-rotation convention for placement data. |
| IPC-6012 | What a finished rigid bare board must meet, class by class. |
| IPC-4761 | Ways of protecting vias: tenting, plugging and filling. |
| IPC-D-356 | The netlist format the fab uses to test bare boards. |
| IPC-A-610 | What an acceptable assembled board looks like, class by class. |
| J-STD-001 | The requirements for soldered assemblies, which go with IPC-A-610. |
| J-STD-020 and J-STD-033 | How moisture-sensitive parts are rated, and how they must be stored, handled and baked. |
| ANSI/ESD S20.20 | The requirements for a factory's static control program. |

Standards are revised every few years.
The book names a revision where it quotes a value from one.
Check that you are using the current revision, and say which one you mean when it matters.

*Last reviewed: 2026-11-12*

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

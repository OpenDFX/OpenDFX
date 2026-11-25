# Inner layers and lamination

On a multilayer board, each inner layer is imaged and etched on its own core, then the cores are stacked with prepreg and pressed together under heat.
In the press, the material moves: each layer shrinks or stretches slightly, and not always by the same amount.
The holes are drilled afterwards, through all the layers at once, so every hole has to land on pads that may have moved a little.

Most of what a designer can do here is leave room for that movement.

## PCB-DFM-022: Keep copper 0.25 mm or more from drilled holes on every layer

**Recommendation:** Keep at least 0.25 mm (10 mil) between the edge of any drilled hole and the nearest copper it isn't meant to connect to, on every layer, including plane clearances.
Go down to 0.2 mm (8 mil) only in a tight area, and avoid going below 0.15 mm (6 mil).

**Why:** Layers move during lamination, and the drill has its own positional tolerance.
The gap between a hole and nearby copper is what absorbs both.
Measure it edge to edge: from the edge of the hole to the edge of the copper.

**Typical values:** 0.25–0.3 mm (10–12 mil): good boards every time.
0.2 mm (8 mil): possible, harder.
0.15 mm (6 mil): in one small, tight area only; below that, few fabs will build it.

**What goes wrong if you don't:** Shorts between a hole and an inner-layer trace or plane, found at electrical test as scrapped boards, or worse, not found until later.

**Applies to:** General practice; fab capability varies.

**Sources:** [“Inner Layer Production w/ CAM Engineer Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/9018673-inner-layer-production-w-cam-engineer-dave-wilcox) (Aug 2021), [01:13:00](https://www.buzzsprout.com/1066066/episodes/9018673?t=4380)–01:17:00; fabs' published design rules (about 0.2 mm typical drill-to-copper).

*Last reviewed: 2026-11-07*

---

## PCB-DFA-074: On very large boards, expect the fab to scale the outer layers, and tell the assembler

**Recommendation:** If your board is very large (about 400 mm or longer), ask the fab whether they had to scale the outer layers, and make sure the stencil is made to match the boards as built.

**Why:** On a large board, the movement in the press adds up from one end to the other.
To keep the holes on their pads, the fab may scale the drill data and then scale the outer-layer artwork to match.
A stencil cut from your original data is then slightly too small or too large for the board.

**What goes wrong if you don't:** Paste prints that are on the pads at one end of the board and off them at the other.

**Applies to:** Large boards; panels are usually kept small enough to avoid it.

**Sources:** [“Inner Layer Production w/ CAM Engineer Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/9018673-inner-layer-production-w-cam-engineer-dave-wilcox) (Aug 2021), [01:14:00](https://www.buzzsprout.com/1066066/episodes/9018673?t=4440)–01:16:00.

*Last reviewed: 2026-11-07*

---

## Related pages
- [Materials and stack-up](01-materials-and-stack-up.md)
- [Drilling](03-drilling.md)
- [Solder paste printing and stencils](../05-assembly/01-solder-paste-and-stencils.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

# Plating

After drilling, the fab makes the hole walls conductive with a thin chemical layer, then electroplates copper onto them.
The same plating builds up copper on the outer layers at the same time.
That's why outer layers end up thicker than the foil they started with, and why plated holes are drilled larger than the size you asked for.

## PCB-DFM-028: Know what plating does to your holes and outer copper

**Recommendation:** Design with plating in mind:
- give finished hole sizes ([PCB-DFM-023](03-drilling.md#pcb-dfm-023-give-hole-sizes-as-finished-sizes));
- set outer-layer trace and space rules for the plated copper thickness, not the starting foil ([PCB-DFM-020](01-materials-and-stack-up.md#pcb-dfm-020-size-traces-and-gaps-for-the-finished-copper-weight));
- keep the aspect ratio within what plates well ([PCB-DFM-024](03-drilling.md#pcb-dfm-024-keep-the-aspect-ratio-at-81-or-less-and-holes-025-mm-or-larger-where-you-can));
- if you need more copper in the holes than the standard, say so on the drawing.

**Why:** Plating adds copper to the hole walls and the outer surfaces in one step.
Getting the minimum thickness in the middle of a deep, narrow hole means the surface gets more than that.
Very small microvias are plated with a slower electroless copper process that covers their walls more reliably than the faster direct-metallization lines.

**Typical values:** IPC-6012F minimum copper in plated holes:

| Copper plating thickness | Class 2 | Class 3 |
|---|---|---|
| Through-holes, blind and buried vias: average | 20 µm | 25 µm |
| Through-holes, blind and buried vias: thinnest spot | 18 µm | 20 µm |
| Microvias: average / thinnest | 12 / 10 µm | 12 / 10 µm |
| Copper cap over a filled via (minimum) | 5 µm | 12 µm |

The outer surfaces gain at least as much copper as the hole walls, often more, so a 1 oz finished outer layer is usually reached from thinner starting foil plus plating.

**What goes wrong if you don't:** Outer-layer gaps too tight once the copper has grown, or holes that are too small.

**Applies to:** General practice.

**Sources:** IPC-6012F (Sept 2023), section 3.6.2.11 and Tables 3-10, 3-11 and 3-13; [“Outer Layer Imaging w/ CAM Engineer Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/11724857-outer-layer-imaging-w-cam-engineer-dave-wilcox) (Nov 2022), [18:00](https://www.buzzsprout.com/1066066/episodes/11724857?t=1080)–19:00 and [30:00](https://www.buzzsprout.com/1066066/episodes/11724857?t=1800)–38:00.

*Last reviewed: 2026-11-07*

---

## Related pages
- [Drilling](03-drilling.md)
- [Outer layers](05-outer-layers.md)
- [Via treatments](06-via-treatments.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

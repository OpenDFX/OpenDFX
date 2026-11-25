# Outer layers

The outer layers are imaged after drilling and plating, usually with a laser that exposes a photoresist directly from your data, and then etched.
The CAM engineer prepares the artwork first: compensating trace widths for the etch, adding small fillets, and checking every clearance.
Clean, unambiguous geometry in your design leaves less for them to change.

## PCB-DFM-029: Avoid acute angles, keep pour clearances to your trace rules, and fan out fine-pitch parts through vias

**Recommendation:**
- Avoid acute (sharper than 90°) inside corners in traces and copper pours.
- Set the clearance between copper pours and other copper to at least your trace spacing.
- To escape the inner pads of a fine-pitch BGA or QFN, drop to an inner layer through a via, rather than squeezing a trace between pads on the outer layer.

**Why:** Etchant pools in acute corners and eats into the copper; CAM software fills them in automatically, which changes your copper.
A pour clearance tighter than your trace rules becomes the tightest gap on the board.
A trace between fine-pitch pads leaves almost no room for etching tolerance or solder mask.

**Typical values:** Pour clearance equal to trace spacing, for example 0.15 mm (6 mil) on 1 oz copper.

**What goes wrong if you don't:** Artwork changed by the fab without your knowing; shorts in the narrowest gaps; bridges between fine-pitch pads.

**Applies to:** General practice.

**Sources:** [“The PCB CAM Process w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/8226431-the-pcb-cam-process-w-dave-wilcox) (Mar 2021), [46:00](https://www.buzzsprout.com/1066066/episodes/8226431?t=2760)–51:00; [“An overview of bare PCB fabrication w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/6388663-an-overview-of-bare-pcb-fabrication-w-dave-wilcox) (Nov 2020), [01:02:00](https://www.buzzsprout.com/1066066/episodes/6388663?t=3720)–01:03:00; [“Outer Layer Imaging w/ CAM Engineer Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/11724857-outer-layer-imaging-w-cam-engineer-dave-wilcox) (Nov 2022), [27:00](https://www.buzzsprout.com/1066066/episodes/11724857?t=1620)–28:00.

*Last reviewed: 2026-11-07*

---

## Related pages
- [Materials and stack-up](01-materials-and-stack-up.md)
- [Plating](04-plating.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

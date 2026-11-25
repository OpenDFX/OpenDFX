# Optical and X-ray inspection

After reflow, an assembled board is inspected.
Automated optical inspection (AOI) machines photograph the board and check that every part is present, the right way round and soldered.
2D machines compare flat images; 3D machines also measure heights, and see solder joints and dark parts on dark boards better.
X-ray inspection looks through parts at joints no camera can see, such as the balls under a BGA or the pad under a QFN.

Inspection checks the assembler's work, not the bare board: shorts and opens in the board itself are the fab's job to find.
Programming a 3D machine takes time for every new part number, so a small order is often inspected by people instead; on repeat orders, the program is already written and pays for itself.
What your design controls is mostly covered elsewhere: footprints and markings that can be checked by eye ([Part 1.4](../01-design-package/04-footprints.md)), space around tall parts so cameras can see their neighbors ([PCB-DFA-023](02-component-placement.md)), and solder mask color (Part 2.8).

## PCB-DFA-038: Join neighboring pins in copper, and keep a solder mask dam between them

**Recommendation:** Where two neighboring pins of a part are meant to be connected, connect them in copper, and keep a solder mask dam between the two pads, as you would between any other fine-pitch pads ([PCB-DFA-032](../01-design-package/04-footprints.md#pcb-dfa-032-put-a-solder-mask-dam-between-every-pad-of-a-fine-pitch-part)).
Avoid leaving the copper between them exposed.

**Why:** With no mask between the pads, solder flows across the joining copper and forms what looks exactly like a solder bridge.
Operators and inspection machines are trained to treat bridges as defects, so an intended connection that looks like one causes confusion.
A mask dam keeps two separate, normal-looking joints; the copper underneath still makes the connection.

![D36: Drawn to scale, plan views of four leads of a 0.5 mm-pitch part after soldering, the middle two meant to be connected. Joined by copper under the mask with a dam between their pads, each has its own normal joint. With the copper between them left bare, solder runs across and the pair looks like a solder bridge.](images/joined-pins.svg)

*D36 is drawn to scale.
Joined under the mask, with a dam between the pads, the two pins solder like any others and inspection sees two normal joints.
With the copper between them left bare, solder runs across it and the pair looks exactly like a bridge.*

**What goes wrong if you don't:** Boards held while the assembler checks whether the bridge is intended, or a "defect" removed by an operator.

**Applies to:** General practice.

**Sources:** [“The PCB assembly process”](https://www.buzzsprout.com/1066066/episodes/4364141-the-pcb-assembly-process) (Jun 2020), [16:00](https://www.buzzsprout.com/1066066/episodes/4364141?t=960)–17:00; [“Automated Optical Inspection (AOI) for PCB Assembly”](https://www.buzzsprout.com/1066066/episodes/6598753-automated-optical-inspection-aoi-for-pcb-assembly) (Nov 2020), [04:00](https://www.buzzsprout.com/1066066/episodes/6598753?t=240)–17:00, for the chapter opening.

*Last reviewed: 2026-11-04*

---

## Related pages
- [Component placement](02-component-placement.md)
- [Footprints and the component library](../01-design-package/04-footprints.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

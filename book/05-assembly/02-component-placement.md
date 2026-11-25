# Component placement

A placement machine picks each part from its tape, tray or tube with a vacuum nozzle, checks it with a camera and puts it down in the wet solder paste.
Modern machines are fast and very accurate, but every part has a target, and smaller targets are harder to hit every time.

What your design controls is the size of those targets and how crowded they are: which packages you choose, and how close together you put them.
Footprint shapes, pin-1 marks and polarity marks also matter a great deal, and have their own chapter (Part 1.4, Footprints and the component library).

## PCB-DFA-021: Use the largest package the board has room for

**Recommendation:** For resistors and capacitors, use 0603 where you have room and 0402 where you need to save space.
Go to 0201 or smaller only when the product truly needs it.
For chips, use the larger package when the part comes in more than one and the larger one fits: an SO-8 rather than a tiny BGA, for example.

**Why:** Smaller parts need more accurate feeders, nozzles, printing and inspection, and slower machine speeds.
They also get less solder (see [PCB-DFA-020](01-solder-paste-and-stencils.md)) and are harder to rework and test.
0603 parts are big enough to carry printed value markings, so inspection cameras can check them; 0402 parts aren't.

**Typical values:** 0603: comfortable · 0402: the everyday floor, placed by the million without trouble · 0201: workable, with more care at every step · 01005 and smaller: only when needed.

**What goes wrong if you don't:** Lower yield, longer lead times and higher prices, for no benefit when the board had room.

**Applies to:** General practice.

**Sources:** [“The pick and place assembly process”](https://www.buzzsprout.com/1066066/episodes/4928099-the-pick-and-place-assembly-process) (Aug 2020), [44:00](https://www.buzzsprout.com/1066066/episodes/4928099?t=2640)–48:00; [“Solder paste printing”](https://www.buzzsprout.com/1066066/episodes/5321710-solder-paste-printing) (Sep 2020), [01:07:00](https://www.buzzsprout.com/1066066/episodes/5321710?t=4020)–01:08:00; [“To BGA or Not to BGA”](https://www.buzzsprout.com/1066066/episodes/19944540-to-bga-or-not-to-bga) (Oct 2026), [16:43](https://www.buzzsprout.com/1066066/episodes/19944540?t=1003)–17:57.

*Last reviewed: 2026-11-01*

---

## PCB-DFA-022: At fine pitch, choose a BGA or QFN over a leaded QFP

**Recommendation:** If a chip comes in a 0.4 mm-pitch QFP and a BGA, choose the BGA.
Avoid 0.4 mm-pitch QFPs altogether if you can; 0.5 mm-pitch QFPs are fine.
Choose the very finest packages (0.4 mm-pitch chip-scale packages and finer) only when the product needs to be that small.

**Why:** Fine leads are fragile: they bend in packaging and handling, they don't sit flat (poor coplanarity), and the process drifts.
A BGA or QFN has no leads to damage, and once the printing process is tuned it stays tuned, so its yield is higher.
The drawback is that a defect under a BGA or QFN is harder and more expensive to fix.
At the finest pitches the whole job gets harder: routing needs via-in-pad, the stencil needs coatings or steps, and at about 0.3 mm pitch the part may be dipped in flux and placed with no paste at all, which requires special tools that not every assembler has.

**Typical values:** 0.5 mm-pitch QFP: easy · 0.8 and 0.65 mm-pitch BGA: easy, often easier than a QFP · 0.4 mm-pitch QFP: avoid · 0.4 mm-pitch BGA or chip-scale package: expensive, only when needed · about 0.3 mm pitch: flux-dip assembly.

**What goes wrong if you don't:** Defects that persist however the process is tuned, and some high-volume assemblers refuse to quote 0.4 mm-pitch QFPs at all.

**Applies to:** General practice.
Leaded parts remain the right choice for boards that will be hand-assembled.

**Sources:** [“To BGA or Not to BGA”](https://www.buzzsprout.com/1066066/episodes/19944540-to-bga-or-not-to-bga) (Oct 2026), [11:21](https://www.buzzsprout.com/1066066/episodes/19944540?t=681)–19:32; [“The pick and place assembly process”](https://www.buzzsprout.com/1066066/episodes/4928099-the-pick-and-place-assembly-process) (Aug 2020), [50:00](https://www.buzzsprout.com/1066066/episodes/4928099?t=3000)–53:00; [“Gloves not Mittens”](https://www.buzzsprout.com/1066066/episodes/19269842-gloves-not-mittens) (Jun 2026), [28:00](https://www.buzzsprout.com/1066066/episodes/19269842?t=1680)–29:00.

*Last reviewed: 2026-11-01*

---

## PCB-DFA-023: Leave room around every part, and keep tall parts away from tiny ones

**Recommendation:** Aim for about 1 mm from the edge of one part to the edge of the next.
Where a board is too dense for that, the absolute minimums are in the table below; check with your assembler before designing to them.
Keep tiny parts (0402 and smaller) away from tall ones such as aluminum electrolytic capacitors.

**Why:** A placement nozzle that has just put down a tall part can hit it while placing a tiny part beside it.
A small part placed slightly off can end up under a large part placed next to it, such as a BGA.
Tall parts also cast shadows that hide their neighbors from 3D inspection cameras, and they make rework harder.

**Typical values:** About 1 mm edge to edge, as an everyday rule of thumb (one assembler's).

| Part size (inch / metric) | Absolute minimum gap, side by side | Absolute minimum gap, end to end |
|---|---|---|
| 01005 / 0402 | 0.13 mm | 0.11 mm |
| 0201 / 0603 | 0.18 mm | 0.17 mm |
| 0402 / 1005 | 0.11 mm | 0.08 mm |
| 0603 / 1608 | 0.21 mm | 0.17 mm |

⚠️ **These minimums are hard to achieve.**
They are a leading placement-machine maker's absolute minimums, published by Worthington Assembly.
Use them only after you've confirmed your assembler's machines are specified for them, and agreed it with the assembler before layout.

![D8: Drawn to scale: on the left, a top view of small capacitors 1 mm from a BGA and 1 mm from each other; on the right, a side view of a 10 mm tall aluminum capacitor whose shadow hides a small resistor right beside it from an inspection camera's angled light, while a resistor further away is in clear view.](images/part-spacing.svg)

*D8 is drawn to scale.
On the left, a top view: small capacitors sit 1 mm from the edge of a BGA and 1 mm from each other.
On the right, a side view: a 10 mm tall aluminum capacitor blocks the angled light of a 3D inspection camera.
A small resistor right beside it is in its shadow and can't be measured; a resistor further away is in clear view.
How long the shadow is depends on the camera's angle.*

**What goes wrong if you don't:** Parts knocked off or placed on top of each other, defects that inspection can't see, and boards that are hard to rework.

**Applies to:** Everyday spacing: general practice.
Absolute minimums: varies by manufacturer; check with yours.

**Sources:** [“The pick and place assembly process”](https://www.buzzsprout.com/1066066/episodes/4928099-the-pick-and-place-assembly-process) (Aug 2020), [48:00](https://www.buzzsprout.com/1066066/episodes/4928099?t=2880)–50:00; [“Automated Optical Inspection (AOI) for PCB Assembly”](https://www.buzzsprout.com/1066066/episodes/6598753-automated-optical-inspection-aoi-for-pcb-assembly) (Nov 2020), [45:00](https://www.buzzsprout.com/1066066/episodes/6598753?t=2700)–46:00; [Discrete Component Spacing](https://www.worthingtonassembly.com/s/Discrete-Component-Spacing.pdf) (Worthington Assembly, PDF).

*Last reviewed: 2026-11-01*

---

## Related pages
- [Solder paste printing and stencils](01-solder-paste-and-stencils.md)
- [Reflow soldering](03-reflow-soldering.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

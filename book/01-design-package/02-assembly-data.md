# Assembly data

To build an assembled board, the assembler needs more than the bare-board data.
They need to know which part goes where, which way round, and on which side: that comes from the placement (XY) file and the bill of materials ([The BOM](03-bom.md)).
Anything the data can't show, such as how to bend a lead or how tight to make a screw, comes from an assembly drawing.

The assembler's programmers check every one of these against each other and against your copper and legend layers.
Where they disagree, the job stops until someone asks you.

## PCB-DFA-064: Always send the XY file, and send native design files and the schematic when you can

**Recommendation:** Send a placement file (also called an XY, centroid or pick-and-place file) with every assembly order.
List every part location on the board, on both sides, with:
- reference designator (exactly as in the BOM);
- X and Y of the part's center, in mm;
- rotation in degrees;
- side (top or bottom);
- whether it's surface-mount or through-hole.

Keep do-not-place locations in the file; whether a location is fitted belongs in the BOM ([PCB-DFA-071](03-bom.md#pcb-dfa-071-mark-do-not-place-and-customer-supplied-lines-clearly)).
Also send your native design files and the schematic, in a separate folder marked "reference only" (see [PCB-DFM-008](01-fabrication-data.md#pcb-dfm-008-send-one-complete-fabrication-package-in-one-format-from-one-revision)).

**Why:** Gerbers show pads, not parts.
Without the XY file, someone has to find and type in the position of every part by hand.
Do-not-place locations stay in because a BOM change on a later order can fill them, and the assembler then already has their positions.
With the schematic and design files, the assembler can answer their own questions about polarity, pin 1 and which part goes where, instead of putting the job on hold to ask you.

**Typical values:** Millimeters, with the origin and units stated in the header.
Rotations positive counter-clockwise, as most assemblers expect.
Plain text or CSV.
Without the file, making placement data by hand takes about 3 minutes a part: about 5 hours for a 100-part board (one assembler).

**What goes wrong if you don't:** A job put on hold while someone asks you a question the schematic would have answered; a four-day turn can become something like seven days.
With no XY file at all, extra programming time and cost.

**Example:** One assembler says the XY file is the one file new customers most often don't know about, because a board soldered by hand on the bench never needs one.
Assembly inspectors say the schematic is what they open when they can't work out a part's orientation from the placement viewer.

**Applies to:** General practice.
Online assemblers vary in whether they want through-hole parts in the file; listing every location and marking the type works for all of them.

**Sources:** [Necessary Documentation](https://www.worthingtonassembly.com/documentation) (Worthington Assembly); [“All the Tricks and Gotchas in Surface Mount Assembly (Repost from the Coriolis Effect)”](https://www.buzzsprout.com/1066066/episodes/11006453-all-the-tricks-and-gotchas-in-surface-mount-assembly-repost-from-the-coriolis-effect) (Jul 2022), [06:00](https://www.buzzsprout.com/1066066/episodes/11006453?t=360)–08:00; [“The PCB assembly inspection process”](https://www.buzzsprout.com/1066066/episodes/5713750-the-pcb-assembly-inspection-process) (Oct 2020), [17:00](https://www.buzzsprout.com/1066066/episodes/5713750?t=1020)–20:00; [“The PCB assembly process”](https://www.buzzsprout.com/1066066/episodes/4364141-the-pcb-assembly-process) (Jun 2020), [08:00](https://www.buzzsprout.com/1066066/episodes/4364141?t=480); two large online assemblers' published file requirements (checked Nov 2026); KiCad 10 documentation, component placement files; Chris Denney (author).

*Last reviewed: 2026-11-07*

---

## PCB-DFA-065: Draw footprints to the IPC zero rotation, and write your convention down

**Recommendation:** Draw every footprint in your library at the zero rotation shown in IPC-7351B, Figure 16-1, and write the convention into your library's rules so everyone who adds a footprint follows it.
Expect the assembler to check every rotation anyway.

**Why:** The rotation in the XY file is the part's angle relative to how its footprint was drawn.
If footprints are drawn in different orientations, the same rotation number means different things on different parts.
The current standard, IPC-7352 (2023), no longer lists zero rotations; it says each organization's library standard should define them.
IPC-7351B's figure is still the convention most libraries follow.
Parts on reels sit in many orientations, depending on the maker, so the assembler always matches each reel to your footprint by hand; a consistent library means one correction per package type instead of one per part.

**Typical values:** IPC-7351B zero rotation, by package (drawn in D44):

| Package | Zero rotation |
|---|---|
| Chip resistors, capacitors, inductors; molded and MELF parts; aluminum electrolytics | Horizontal, pin 1 on the left. Pin 1 is the positive pin, or the cathode for diodes. |
| SOT, SOT-23, SOT-223, DPAK, SOIC, TSSOP, SON, DFN, QFP, QFN, chip arrays | Pin 1 at the upper left |
| BGA, LGA | Pin A1 at the upper left |
| PLCC, LCC, bumpered QFP with pin 1 at the center of a side | Pin 1 at the top center |

For example, a part that sits on its tape with pin 1 at the lower left is 90° counter-clockwise from its zero rotation.

![D44 is drawn to scale: six footprints at their IPC zero rotation: a horizontal 0603 chip with no polarity mark; a horizontal SOD-123 diode with the cathode on the left; a SOT-23 with pins 1 and 2 on the left, pin 1 at the top, and no mark; an 8-pin SOIC with pin 1 at the upper left; a 3 × 3 mm QFN with pin 1 at the top of the left side; a BGA with ball A1 at the upper left. Each has a cross at its center.](images/zero-rotation.svg)

*D44 is drawn to scale and shows six footprints at the IPC-7351B zero rotation.
The 0603 chip resistor or capacitor lies horizontal with no polarity mark, since it isn't polarized; the SOD-123 diode lies horizontal with its cathode, marked K, on the left.
The SOIC, QFN and BGA, whose pads would fit either way round, each have a white pin-1 dot.
The SOT-23 has pins 1 and 2 on the left, pin 1 at the top, and pin 3 on the right; it needs no mark, because its pads only fit one way.
The 8-pin SOIC has pins 1 to 4 down the left side, pin 1 at the upper left.
The 16-pin QFN has pin 1 at the top of the left side, and the BGA has ball A1 at the upper left.
The cross at each part's center is the point the XY file gives; the rotation in the XY file is measured from this drawing.*

**What goes wrong if you don't:** More time spent lining up rotations before the first board can be built, and more chances to place a part backwards.

**Example:** At one assembler, lining up rotations from customers' XY files commonly takes about half an hour per job.
Because the rotations are at least consistent within a package type, the usual fix is "turn every 0402 by 90°", and the rest follow.
LEDs are the hardest: each maker orients them differently in the tape and uses different polarity marks.

**Applies to:** General practice.
If you use a different convention, that's fine; the assembler will work it out.
Use one convention throughout the library.

**Sources:** IPC-7351B, section 16 and Figure 16-1; IPC-7352 (May 2023), section 7; [“All the Tricks and Gotchas in Surface Mount Assembly (Repost from the Coriolis Effect)”](https://www.buzzsprout.com/1066066/episodes/11006453-all-the-tricks-and-gotchas-in-surface-mount-assembly-repost-from-the-coriolis-effect) (Jul 2022), [07:00](https://www.buzzsprout.com/1066066/episodes/11006453?t=420)–11:00; Chris Denney (author).

*Last reviewed: 2026-11-07*

---

## PCB-DFA-066: Give every part a unique reference designator, placed next to its own part

**Recommendation:** Give every part on the board its own reference designator (R1, U4), with no duplicates and no suffixes like U4_1 and U4_2 left over from copied schematic blocks.
Use only letters and numbers.
If the legend shows reference designators, place each one where it clearly belongs to its own part.

**Why:** The reference designator is how everyone talks about a part: the BOM, the XY file, the inspection report and every email.
Duplicates make every conversation ambiguous.
Some inspection and programming software can't handle unusual characters in designators.
Printed designators nudged around to fit can end up beside the wrong part, and the assembler uses them to check placement.

**Typical values:** Up to about 8 characters is safe; at least one inspection machine's software fails on longer ones.

**What goes wrong if you don't:** A question that takes half an hour to answer instead of seconds; in the worst case, the wrong part soldered to a pad because its designator sat beside the neighboring footprint.

**Example:** One assembler's inspection machine crashes outright on some unusual designators; they now run their own check on every job for long or odd designators before it reaches the machine.

**Applies to:** General practice.

**Sources:** [“Showstoppers that delay PCB assembly w/ Production Manager, Rob OConnell”](https://www.buzzsprout.com/1066066/episodes/9741439-showstoppers-that-delay-pcb-assembly-w-production-manager-rob-oconnell) (Dec 2021), [40:00](https://www.buzzsprout.com/1066066/episodes/9741439?t=2400)–43:00; [“Mastering Vias: Plugging, Filling, and Best Practices”](https://www.buzzsprout.com/1066066/episodes/16036518-mastering-vias-plugging-filling-and-best-practices) (Nov 2024), [28:00](https://www.buzzsprout.com/1066066/episodes/16036518?t=1680)–30:00.

*Last reviewed: 2026-11-07*

---

## PCB-DFA-067: Put everything the data can't show on an assembly drawing

**Recommendation:** Add an assembly drawing, or a short marked-up image, for anything the XY file and BOM can't express:
- through-hole leads that must be bent, with the angle and the direction;
- screws, nuts and other hardware, with a torque value;
- parts that must sit at a set height or stand-off, or be glued, sleeved or potted;
- areas to keep clear of coating, glue or labels;
- any special process or material, specified by what it must do rather than by brand.

**Why:** Placement data says where a part goes and which way it faces, not how its leads are formed or how tight a screw is.
"Tight" means something different to every operator; a torque value can be set on a torque driver and checked.
Assemblers are wary of choosing a torque for you, because they don't know your materials and loads.
Branded solder pastes, wires and other materials get discontinued or go out of stock, and a drawing that names one product can stop a build.

**Typical values:** Torque in N·m (or in·lb), from the fastener maker, a calculation, or a pull test on a few samples.

**What goes wrong if you don't:** Parts fitted the way the data shows, which may not be what you meant, and a second build to fix it.

**Example:** A customer wanted a through-hole LED bent at 90° and lined up with another feature, but sent no drawing; the LEDs were fitted the way the design appeared to call for, and the customer was disappointed.
Screenshots and marked-up 3D renders of tricky areas help fabs and assemblers as much as formal drawings.

**Applies to:** General practice.

**Sources:** [“Showstoppers that delay PCB assembly w/ Production Manager, Rob OConnell”](https://www.buzzsprout.com/1066066/episodes/9741439-showstoppers-that-delay-pcb-assembly-w-production-manager-rob-oconnell) (Dec 2021), [29:00](https://www.buzzsprout.com/1066066/episodes/9741439?t=1740)–31:00; [“Alternative Component Mounting”](https://www.buzzsprout.com/1066066/episodes/10030215-alternative-component-mounting) (Feb 2022), [33:00](https://www.buzzsprout.com/1066066/episodes/10030215?t=1980)–35:00; [“The nitty gritty details on solder”](https://www.buzzsprout.com/1066066/episodes/11129008-the-nitty-gritty-details-on-solder) (Aug 2022), [41:00](https://www.buzzsprout.com/1066066/episodes/11129008?t=2460)–44:00; [“Impedance Control Demo w/ NCAB Group Field Application Engineer Ryan Miller”](https://www.buzzsprout.com/1066066/episodes/13789746-impedance-control-demo-w-ncab-group-field-application-engineer-ryan-miller) (Oct 2023), [25:00](https://www.buzzsprout.com/1066066/episodes/13789746?t=1500)–27:00.

*Last reviewed: 2026-11-07*

---

## Related pages
- [Fabrication data](01-fabrication-data.md)
- [The BOM](03-bom.md)
- [Footprints and the component library](04-footprints.md)
- [Component placement](../05-assembly/02-component-placement.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

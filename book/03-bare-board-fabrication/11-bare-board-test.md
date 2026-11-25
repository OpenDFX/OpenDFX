# Bare board electrical test and inspection

Before boards leave the fab, they're tested for opens and shorts and inspected against the standard they were built to.
This is the last chance to catch a fault before parts are soldered on, when finding it becomes far more expensive.
The assembler's own inspection checks its soldering and parts, not the bare board's copper.

## PCB-DFT-002: Have every bare board electrically tested against your netlist

**Recommendation:** Ask for 100% electrical test of every bare board, against the netlist you supplied (see [PCB-DFM-009](../01-design-package/01-fabrication-data.md#pcb-dfm-009-always-send-a-netlist-made-from-the-same-revision-as-the-gerbers)).
Expect a flying-probe test for prototypes and small batches, and a fixture (bed of nails) for large, repeat orders.

**Why:** Electrical test finds opens and shorts in the copper, including faults hidden on inner layers and in plated holes.
Tested against your netlist rather than a netlist the fab extracted from your Gerbers, it also catches a Gerber that doesn't match the design.
Assembly inspection can't do this: it looks at parts and solder joints, and assumes the bare board is right.
A hole the plating missed, for example, fails electrical test at the fab instead of failing in the field.

**Typical values:** Flying probe: no tooling, slower per board.
Fixture: tooling cost and a few days to build, then fast.

**What goes wrong if you don't:** A short or open found only after assembly, when the board is full of parts and the fault is much harder to find and fix.

**Applies to:** General practice.

**Sources:** [“The PCB CAM Process w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/8226431-the-pcb-cam-process-w-dave-wilcox) (Mar 2021), [12:00](https://www.buzzsprout.com/1066066/episodes/8226431?t=720)–19:00; [“Outer Layer Imaging w/ CAM Engineer Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/11724857-outer-layer-imaging-w-cam-engineer-dave-wilcox) (Nov 2022), [18:00](https://www.buzzsprout.com/1066066/episodes/11724857?t=1080); [“Automated Optical Inspection (AOI) for PCB Assembly”](https://www.buzzsprout.com/1066066/episodes/6598753-automated-optical-inspection-aoi-for-pcb-assembly) (Nov 2020), [04:00](https://www.buzzsprout.com/1066066/episodes/6598753?t=240); [“What factors influence PCB quotes w/ Brett Babilonia”](https://www.buzzsprout.com/1066066/episodes/14580855-what-factors-influence-pcb-quotes-w-brett-babilonia) (Feb 2024), [09:00](https://www.buzzsprout.com/1066066/episodes/14580855?t=540)–11:00; fabs' published electrical-test guidance (IPC-D-356 netlists, flying probe and fixture).

*Last reviewed: 2026-11-08*

---

## PCB-DFT-003: Ask for IPC Class 2 unless the product needs Class 3, and know Class 3 is a design standard too

**Recommendation:** Build to IPC Class 2, which suits nearly all products, unless the product's use truly needs Class 3 (high reliability: medical life support, aerospace, some automotive and military).
If you do need Class 3, design for it from the start, not only at ordering, and call out the class instead of writing your own acceptance criteria.

**Why:** The IPC classes set what's acceptable in the bare board (IPC-6012) and the assembly (IPC-A-610): annular ring, plating thickness, solder fillets and much more.
Class 3 limits are tighter, so they cost more to make and inspect, and some can only be met if the design allows them: a Class 3 annular ring needs pads big enough for it, for example.
Ordering Class 3 for a board designed to Class 2 doesn't make it a Class 3 product.

**Typical values:** Class 1, simple products, about 5% of what's built; Class 2, about 90%; Class 3, the rest, at a much higher cost (one estimate: ten times or more).

**What goes wrong if you don't:** Paying far more than you need to, or ordering Class 3 for a design that can't meet it and getting rejects or waivers.

**Applies to:** General practice.

**Sources:** [“An Answering Your Questions Grab Bag”](https://www.buzzsprout.com/1066066/episodes/13847902-an-answering-your-questions-grab-bag) (Oct 2023), [17:00](https://www.buzzsprout.com/1066066/episodes/13847902?t=1020)–20:00; [“What factors influence PCB quotes w/ Brett Babilonia”](https://www.buzzsprout.com/1066066/episodes/14580855-what-factors-influence-pcb-quotes-w-brett-babilonia) (Feb 2024), [49:00](https://www.buzzsprout.com/1066066/episodes/14580855?t=2940)–51:00; [“How IPC helps the global manufacturing ecosystem build electronics better w/ Teresa Rowe and Patrick Crawford”](https://www.buzzsprout.com/1066066/episodes/10444705-how-ipc-helps-the-global-manufacturing-ecosystem-build-electronics-better-w-teresa-rowe-and-patrick-crawford) (Apr 2022), [07:00](https://www.buzzsprout.com/1066066/episodes/10444705?t=420)–11:00; IPC-6012F (Sept 2023), Table 3-7.

*Last reviewed: 2026-11-08*

---

## PCB-DFT-004: For boards that matter, ask for the fab's evidence

**Recommendation:** For Class 3 boards, impedance-controlled boards and anything safety-critical, ask the fab to ship its evidence with the boards: a certificate of conformance, the electrical test result, the impedance test report where it applies, and cross-sections (microsections) of test coupons for Class 3.
Write what you need on the fabrication drawing or purchase order, so it's quoted from the start.

**Why:** A pass label on its own doesn't say what was tested, against which netlist, or to which limits.
A cross-section of a coupon cut from the same panel shows the plating thickness in the holes and the layer build, which no electrical test can.
Asking up front costs little; asking after the boards have shipped usually can't be done.

**What goes wrong if you don't:** No proof the boards meet the drawing when a customer, auditor or failure investigation asks for it.

**Applies to:** General practice; report formats vary by fab.

**Sources:** IPC-6012F (Sept 2023), quality conformance testing and coupons; fabs' published electrical-test and quality documents. Not covered in the podcast.

*Last reviewed: 2026-11-08*

---

## Related pages
- [Fabrication data](../01-design-package/01-fabrication-data.md)
- [Plating](04-plating.md)
- [Inspection](../05-assembly/04-inspection.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

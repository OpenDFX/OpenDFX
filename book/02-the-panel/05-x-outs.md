# X-outs: accepting panels with a bad board

Bare boards are tested at the fab.
When one board on a panel fails, the fab can scrap the whole panel or mark the bad board and ship the rest.
A marked board is called an **X-out**: it's crossed out with a marker, and a colored sticker is put at an agreed spot on the panel.
When the machines see the sticker, they skip that board: no paste, no parts, no inspection.

## PCB-DFM-004: Accept X-outs unless you have a real reason not to

**Recommendation:** Allow your fab and assembler to use panels with X-outs.
If your process truly can't handle them (for example a test fixture that needs every position filled), say so up front and expect to pay for it.

**Why:** The other boards on the panel are perfectly good.
Refusing X-outs means the fab scraps whole panels, and that cost is passed on to you.

**Typical values:** Refusing X-outs can cost about 20–30 % more per board (one assembler's estimate, as of 2023).

**What goes wrong if you don't:** You pay a premium for every board, often without seeing it on the quote.

**Applies to:** Varies by manufacturer.
Check with yours.

**Sources:** [“An Answering Your Questions Grab Bag”](https://www.buzzsprout.com/1066066/episodes/13847902-an-answering-your-questions-grab-bag) (Oct 2023), [13:00](https://www.buzzsprout.com/1066066/episodes/13847902?t=780)–20:00.

*Last reviewed: 2026-10-28*

---

## PCB-DFM-005: Design with margin above the fab's minimums to avoid X-outs in the first place

**Recommendation:** Don't design right at the fab's stated minimum trace width and spacing.
Use 6 mil (0.15 mm) as an everyday minimum and 8 mil (0.2 mm) where you have room.
Design for the copper weight you'll actually order: 2 oz copper needs wider gaps than 1 oz.

**Why:** Tight features are fine on one small board but get much harder to make perfectly when they're repeated many times across a large panel.
Margin lets the fab hit its tolerances every time, so fewer boards fail.

**Typical values:** Most fabs' practical limit is about 4 mil (0.1 mm) · 6 mil (0.15 mm) everyday minimum · 8 mil (0.2 mm) comfortable, and recommended for 2 oz copper.

**What goes wrong if you don't:** More boards fail at the fab.
Panels arrive full of X-outs, the fab has to make extra panels to fill your order, and the cost and delay come back to you.

**Example:** A power-supply board designed with 1 oz spacing but ordered in 2 oz copper came back with so many X-outs that about 400 panels had to be made to deliver an order that should have needed 250.
Redesigning to 8 mil trace and gap fixed it.
The other way round, a designer who chose 8 mil instead of the fab's 6 mil minimum reported zero X-outs across many thousands of boards.

**Applies to:** General practice.
Exact limits vary by fab.

**Sources:** [“Inner Layer Production w/ CAM Engineer Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/9018673-inner-layer-production-w-cam-engineer-dave-wilcox) (Aug 2021), [01:09:00](https://www.buzzsprout.com/1066066/episodes/9018673?t=4140)–01:11:00; [“Outer Layer Imaging w/ CAM Engineer Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/11724857-outer-layer-imaging-w-cam-engineer-dave-wilcox) (Nov 2022), [43:00](https://www.buzzsprout.com/1066066/episodes/11724857?t=2580)–44:00; [“Advanced Drilling w/ CAM Engineer, Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/10611991-advanced-drilling-w-cam-engineer-dave-wilcox) (May 2022), [35:00](https://www.buzzsprout.com/1066066/episodes/10611991?t=2100)–38:00; [“An EDA Tool Walks Into a CM w/ Fusion 360 Electronics Product Manager, Ben Jordan”](https://www.buzzsprout.com/1066066/episodes/9171908-an-eda-tool-walks-into-a-cm-w-fusion-360-electronics-product-manager-ben-jordan) (Sep 2021), [50:00](https://www.buzzsprout.com/1066066/episodes/9171908?t=3000)–53:00.

*Last reviewed: 2026-10-28*

---

## PCB-DFM-006: Prefer smaller panels for designs that are hard to make

**Recommendation:** If your design pushes the fab's limits, ask for a smaller panel (for example 3- or 4-up) rather than a large one (for example 15-up).

**Why:** A large panel collects more bad boards per panel.
Some fabs resist shipping panels with many X-outs, and a panel that is mostly X-outs wastes assembly time.

**Applies to:** Varies by manufacturer.
Check with yours.

**Sources:** [“The PCB CAM Process w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/8226431-the-pcb-cam-process-w-dave-wilcox) (Mar 2021), [01:11:00](https://www.buzzsprout.com/1066066/episodes/8226431?t=4260)–01:13:00; [“Advanced Drilling w/ CAM Engineer, Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/10611991-advanced-drilling-w-cam-engineer-dave-wilcox) (May 2022), [35:00](https://www.buzzsprout.com/1066066/episodes/10611991?t=2100)–36:00.

*Last reviewed: 2026-10-28*

---

## Related pages
- [Why boards are built in panels](01-why-panels.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

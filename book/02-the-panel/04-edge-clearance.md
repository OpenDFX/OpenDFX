# Clearance near board and panel edges

The outer few millimeters of a board are a busy place.
Conveyors and clamps grip it, depaneling tools cut and bend it, and the fab's router or scoring blade runs along it.
Keeping your parts and copper back from the edge is one of the cheapest things you can do to make a board easier to build.

## Edge clearances at a glance

| What | From | Minimum | Better | Recommendation |
|---|---|---|---|---|
| Components and exposed (solderable) copper | Any edge the machines grip, if you want to avoid rails | 3 mm | 5 mm | [PCB-DFA-015](#pcb-dfa-015-keep-parts-and-exposed-copper-at-least-3-mm-from-the-edges-5-mm-if-you-can) |
| Copper, any layer (traces, pours) | A V-score line | 0.5 mm (20 mil) | 1.0 mm | [PCB-DFM-002](#pcb-dfm-002-keep-copper-back-from-the-board-edge-further-for-v-score-than-for-routing) |
| Copper, any layer (traces, pours) | A routed edge | 0.25 mm (10 mil) | | [PCB-DFM-002](#pcb-dfm-002-keep-copper-back-from-the-board-edge-further-for-v-score-than-for-routing) |
| General components | A V-scored or routed edge | 1.3 mm (50 mil) | | [PCB-DFA-016](#pcb-dfa-016-keep-components-back-from-breakaway-edges-and-ceramic-capacitors-further-still) |
| Ceramic capacitors (MLCCs) | A V-scored edge, or a breakaway tab | 5 mm (0.2 in) | 10 mm | [PCB-DFA-016](#pcb-dfa-016-keep-components-back-from-breakaway-edges-and-ceramic-capacitors-further-still) |

These come from the podcast episodes and published fab guidelines.
Your manufacturer's may differ.

![D3: Drawn to scale: a V-score line between two boards, with copper kept 0.5 mm back, a resistor 1.3 mm or more back and a ceramic capacitor 5 mm or more back, both turned parallel to the line; a capacitor turned across the line 1 mm from it is marked as wrong.](images/vscore-clearance.svg)

*D3 is enlarged and drawn to scale.
A dashed V-score line separates two boards.
Copper is kept at least 0.5 mm from the line, ordinary parts such as resistors at least 1.3 mm, and ceramic capacitors at least 5 mm.
The resistor and the good capacitor lie with their long axis parallel to the line.
A capacitor lying across the line, only 1 mm from it, is marked as wrong.*

## PCB-DFA-015: Keep parts and exposed copper at least 3 mm from the edges, 5 mm if you can

**Recommendation:** Keep every component and every piece of exposed, solderable copper at least 3 mm from the board's long edges, and preferably 5 mm.
This is generally not possible, but very convenient when possible.
If you manage this, plus fiducials on the board, tell your assembler: they may be able to run the board without rails.

**Why:** Equipment built to the SMEMA conveyor standard (IPC-SMEMA-9851) grips about 3 mm of the board edge, and the standard allows a conveyor to use up to 5 mm.
Anything in that strip can be crushed, hidden from cameras or kept from getting solder paste.
Without the clearance, the assembler has to add rails, which costs panel material and depaneling time.

**Typical values:** 3 mm minimum · 5 mm recommended.
Copper that is covered by solder mask can come much closer (see PCB-DFM-002).

**What goes wrong if you don't:** Rails on every panel, a depaneling step on every board, and extra handling stress on the parts near the edge.

**Applies to:** General practice.
Most assemblers add rails by default anyway; ask yours whether they'll run your board without them.

**Sources:** [“Small PCB layout decisions that have a significant impact on assembly”](https://www.buzzsprout.com/1066066/episodes/8957623-small-pcb-layout-decisions-that-have-a-significant-impact-on-assembly) (Aug 2021), [17:00](https://www.buzzsprout.com/1066066/episodes/8957623?t=1020)–23:00 and [27:00](https://www.buzzsprout.com/1066066/episodes/8957623?t=1620); [“PCB Depaneling”](https://www.buzzsprout.com/1066066/episodes/8035612-pcb-depaneling) (Mar 2021), [31:00](https://www.buzzsprout.com/1066066/episodes/8035612?t=1860); [“Conveyers, An Episode You Didn't Know You Needed”](https://www.buzzsprout.com/1066066/episodes/13980495-conveyers-an-episode-you-didn-t-know-you-needed) (Nov 2023), [35:00](https://www.buzzsprout.com/1066066/episodes/13980495?t=2100)–37:00; [“What factors influence PCB quotes w/ Brett Babilonia”](https://www.buzzsprout.com/1066066/episodes/14580855-what-factors-influence-pcb-quotes-w-brett-babilonia) (Feb 2024), [32:00](https://www.buzzsprout.com/1066066/episodes/14580855?t=1920)–33:00.

*Last reviewed: 2026-10-28*

---

## PCB-DFM-002: Keep copper back from the board edge, further for V-score than for routing

**Recommendation:** Keep traces and copper pours, on every layer, at least 0.5 mm (20 mil) from a V-score line, and 1.0 mm if you have room.
On routed edges, 0.25 mm (10 mil) is a common minimum.
Some fabs can route closer, down to about 0.13 mm (5 mil), if you agree it with them first.

**Why:** The V-score blade cuts a groove into the board, and its position varies by a few tenths of a millimeter.
Copper too close to it gets cut, exposed or cracked when the board is snapped apart.
Routing is more precise and puts less stress on the edge.

**Typical values:** V-score: 0.45–0.5 mm minimum in published fab rules (one European fab: 0.45 mm on all layers; one US fab: 20 mil), with some fabs asking for up to 1.0 mm · routed: about 0.25 mm on outer layers (some fabs ask 0.4 mm on inner layers).
Copper right up to the edge can't be V-scored at all.

**What goes wrong if you don't:** The fab flags the design and puts it on hold, or rejects it.

**Applies to:** Varies by manufacturer.
Check with yours.

**Sources:** [“How PCB panelization methods inform depanelization”](https://www.buzzsprout.com/1066066/episodes/11289685-how-pcb-panelization-methods-inform-depanelization) (Sep 2022), [26:00](https://www.buzzsprout.com/1066066/episodes/11289685?t=1560) and [28:00](https://www.buzzsprout.com/1066066/episodes/11289685?t=1680); [“Small PCB layout decisions that have a significant impact on assembly”](https://www.buzzsprout.com/1066066/episodes/8957623-small-pcb-layout-decisions-that-have-a-significant-impact-on-assembly) (Aug 2021), [17:00](https://www.buzzsprout.com/1066066/episodes/8957623?t=1020)–23:00; published design rules from several PCB fabs (checked Oct 2026).

*Last reviewed: 2026-10-28*

---

## PCB-DFA-016: Keep components back from breakaway edges, and ceramic capacitors further still

**Recommendation:** Keep components at least 1.3 mm (50 mil) from any edge that will be V-scored or tab-routed.
Keep multilayer ceramic capacitors (MLCCs) at least 5 mm (0.2 in) from a V-scored edge and from each breakaway tab, and 10 mm if you have room.
If an MLCC has to sit closer than 5 mm, use a flexible-termination MLCC, or ask for a routed slot between the part and the break line.

**Why:** Breaking a panel apart bends the board along the break line, and the strain is highest right next to it, and highest of all at a tab.
Most parts can take it.
MLCCs are ceramic: they don't bend, they crack.

**Typical values:** Components 1.3 mm (50 mil) · MLCCs 5 mm (0.2 in) minimum, as two capacitor makers advise · MLCCs 10 mm better, as a third maker advises for board edges, screw holes and connectors.
Flexible-termination MLCCs are rated for up to 5 mm of board bending in the standard bend test, against the usual 2 mm minimum.
Near an MLCC, a routed slot is a gentler break line than a row of mouse bites.
Some assemblers accept MLCCs as close as 3.2 mm (125 mil) on low-volume boards, at higher risk.

**What goes wrong if you don't:** Cracked capacitors are hard to catch.
Many pass test and fail weeks or months later in the field, sometimes as a short that can overheat.
On a run of 50 boards you may never see it; at automotive volumes, you will.

**Example:** Ceramic capacitors placed close to the edge cracked during depaneling, and many boards had to be reworked.

**Applies to:** General practice.

**Sources:** [“How PCB panelization methods inform depanelization”](https://www.buzzsprout.com/1066066/episodes/11289685-how-pcb-panelization-methods-inform-depanelization) (Sep 2022), [26:00](https://www.buzzsprout.com/1066066/episodes/11289685?t=1560)–29:00; [“An Answering Your Questions Grab Bag”](https://www.buzzsprout.com/1066066/episodes/13847902-an-answering-your-questions-grab-bag) (Oct 2023), [43:00](https://www.buzzsprout.com/1066066/episodes/13847902?t=2580)–44:00; capacitor makers' guidance on preventing MLCC flex cracks (checked Oct 2026), including [“Strain Crack Mechanism and Preventive Measures for Multilayer Ceramic Capacitors”](https://article.murata.com/en-global/article/strain-crack-mechanism-and-preventive-measures-for-mlcc), section 5.

*Last reviewed: 2026-10-28*

---

## PCB-DFA-017: Turn ceramic capacitors and other chip parts near a break line parallel to it

**Recommendation:** Where a chip part (especially an MLCC) has to sit near a V-score line or breakaway tab, turn it so its long axis runs parallel to the line, not across it.
If you can't, ask your assembler about a routed slot between the part and the line.

**Why:** Snapping a panel bends the board along the break line, and the strain runs across the line.
A part lying across the line is stretched end to end, which is how MLCCs crack.
A part lying along the line sees much less of that strain.
Capacitor makers rank parallel placement as the lowest-stress option.

**What goes wrong if you don't:** Cracked capacitors that may pass test and fail later in the field.
A cracked MLCC can short and overheat.

**Applies to:** General practice.
Distance from the line (PCB-DFA-016) still matters most.

**Sources:** Capacitor makers' layout guidance on preventing MLCC flex cracks (two major makers, checked Oct 2026); [“PCB Depaneling”](https://www.buzzsprout.com/1066066/episodes/8035612-pcb-depaneling) (Mar 2021), [32:00](https://www.buzzsprout.com/1066066/episodes/8035612?t=1920), for stress from the depaneling knife.

*Last reviewed: 2026-10-28*

---

## PCB-DFM-003: If copper must run to the board edge, say so

**Recommendation:** If your design really needs copper right up to the edge (for example an edge connector or an edge-plated shield), state it clearly in the fabrication notes.

**Why:** Fab engineers are trained to pull copper back from the edge by default, because routing through copper wears out router bits faster.
They can do it, but only if they know you mean it.

**What goes wrong if you don't:** The fab quietly pulls your copper back, or puts the job on hold with questions.

**Applies to:** General practice.

**Sources:** [“The PCB CAM Process w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/8226431-the-pcb-cam-process-w-dave-wilcox) (Mar 2021), [52:00](https://www.buzzsprout.com/1066066/episodes/8226431?t=3120)–54:00.

*Last reviewed: 2026-10-28*

---

## Related pages
- [Rails, tooling holes and fiducials](02-rails-tooling-holes-fiducials.md)
- [Breakaway methods: V-score, tabs and mouse bites](03-breakaway-methods.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

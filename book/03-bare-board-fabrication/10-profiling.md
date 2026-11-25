# Profiling: routing, scoring, slots and cut-outs

Profiling cuts the board to shape: its outline, internal slots and cut-outs, and any special edges.
Most of it is done with a spinning router bit, so every cut has the bit's width and every inside corner its radius.
How boards are joined in the panel and broken out of it (V-score, tabs and mouse bites) is in [Part 2: The panel](../02-the-panel/03-breakaway-methods.md); this page is about the shape of each board.

## PCB-DFM-041: Draw the outline, slots and cut-outs as closed shapes on one layer

**Recommendation:** Draw the board outline, and every internal slot and cut-out, as closed shapes on one mechanical layer, and send that layer as its own file.
Put nothing else on that layer.
Draw plated slots in the drill data, not as outline.

**Why:** CAM builds the router path from the outline layer.
Gaps, overlapping lines, dimensions or a title block on that layer make it guess where the edge is.
A slot drawn only on a copper or legend layer may never be cut at all.

**What goes wrong if you don't:** Fab queries and delay, or a slot or cut-out missing from the finished board.

**Applies to:** General practice.

**Sources:** Fabs' published outline and Gerber guidelines; the Gerber format's guidance on profile layers.
Not covered in the podcast.

*Last reviewed: 2026-11-08*

---

## PCB-DFM-042: Allow for the router: a radius in every inside corner and slots at least 1 mm wide

**Recommendation:** Give every inside corner a radius of at least half the router bit's width, and design for 1 mm unless you need tighter.
Make routed slots at least 1 mm wide.
If a part needs a square inside corner, ask the fab for a smaller bit or draw small relief cut-outs at the corner.

**Why:** A round bit can't cut a sharp inside corner: it leaves a radius equal to its own.
Fabs route outlines with bits about 2 mm in diameter, which leaves a 1 mm radius, and use smaller bits on request at extra time and risk of breakage.
A slot can't be narrower than the bit that cuts it.

![D51: Drawn to scale, plan view of part of a board. A 10 by 6 mm cut-out routed with a 2 mm bit has a 1 mm radius in every inside corner, with the bit drawn in one corner. A slot 1 mm wide has round ends. A cut-out for a square 8 by 6 mm part has a round relief at each corner so the part's corners fit.](images/router-corners.svg)

*D51 is drawn to scale.
A 2 mm router bit leaves a 1 mm radius in every inside corner of a cut-out, and a slot can't be narrower than the bit.
Where a square part must drop into a cut-out, a small round relief at each corner makes room for the part's square corners.*

**Typical values:** Inside corner radius 1 mm with a standard 2 mm bit; about 0.5 mm with a 1 mm bit, on request.
Routed slot at least 1 mm wide; non-plated slots 1 mm, plated slots from about 0.5 mm at some fabs.
Routed edge tolerance about ±0.1 mm; V-scored edges are looser.

**What goes wrong if you don't:** A rectangular part that won't drop into its cut-out, a board that doesn't fit its enclosure, or a fab query.

**Applies to:** Varies by manufacturer; check with yours.

**Sources:** [“PCB Depaneling”](https://www.buzzsprout.com/1066066/episodes/8035612-pcb-depaneling) (Mar 2021), [34:00](https://www.buzzsprout.com/1066066/episodes/8035612?t=2040); [“How to develop a PCBA functional test system w/ FixturFab”](https://www.buzzsprout.com/1066066/episodes/10100478-how-to-develop-a-pcba-functional-test-system-w-fixturfab) (Feb 2022), [01:07:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=4020); fabs' published routing minimums (0.4–0.5 mm smallest inside radius, 0.8–1.0 mm smallest slot, ±0.1–0.15 mm).

*Last reviewed: 2026-11-08*

---

## PCB-DFM-043: Dimension castellations, edge plating, countersinks and bevels on the drawing, and expect them to cost more

**Recommendation:** Treat any edge feature beyond a plain routed edge as a special: castellated (half-cut plated) holes, plated edges, countersunk or counterbored holes, and bevels.
Show and dimension each one on the fabrication drawing, mention it when you order, and expect extra cost and lead time.
If the feature is unusual, talk to the fab and assembler with a sketch before you commit the design.

**Why:** Each one needs an extra process step: castellations are drilled and plated, then routed through the middle of the holes; edge plating is plated before routing; countersinks are cut with a separate tool.
None of them shows clearly in Gerber data, so a fab that isn't told may simply route a plain edge.

**Typical values:** Castellated holes about 0.8 mm finished (0.5 mm the usual minimum) with 1.5 mm pads, at least 0.6 mm apart.
Countersinks: give the angle (82° or 90° are common) and the top diameter.

**What goes wrong if you don't:** Features left off or built wrong, half-holes that tear their plating out, or a quote that changes after you order.

**Example:** An open-source wrist-worn heart-rate monitor needed a notch to hold a watch band's spring pin, with no work after assembly.
The designer used a castellated hole as the notch, with a zero-ohm resistor on each side to trap the pin.
They talked it through with the assembler first, with drawings, to settle how close to the castellation the resistors could sit.

**Applies to:** Varies by manufacturer; check with yours.

**Sources:** [“How Joel Murphy went from visual artist to electronics design engineer”](https://www.buzzsprout.com/1066066/episodes/5963659-how-joel-murphy-went-from-visual-artist-to-electronics-design-engineer) (Oct 2020), [01:16:00](https://www.buzzsprout.com/1066066/episodes/5963659?t=4560)–01:19:00; fabs' published castellation, edge-plating and countersink guidelines.

*Last reviewed: 2026-11-08*

---

## Related pages
- [Breakaway methods](../02-the-panel/03-breakaway-methods.md)
- [Edge clearance](../02-the-panel/04-edge-clearance.md)
- [Fabrication data](../01-design-package/01-fabrication-data.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

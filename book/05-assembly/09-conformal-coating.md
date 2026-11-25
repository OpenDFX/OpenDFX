# Conformal coating

Conformal coating is a thin protective film (acrylic, silicone, urethane, parylene and others) applied over an assembled board to keep out moisture, dust and chemicals.
It's applied by spraying, dipping, brushing or vapor deposition, often by a specialist coating contractor, and it adds cost to every board.

Coating keeps bad things off the board, but it also seals in whatever is already on it.
What your design controls is whether the board is clean underneath, and which areas must stay uncoated.

## PCB-DFA-060: Clean boards before they're coated, where you can

**Recommendation:** If a board will be conformally coated, cleaning it first is recommended.
Coating over no-clean flux residue without cleaning is common, and many boards built that way are proving reliable; if you choose it, qualify that flux and coating together for your product (for example with surface insulation resistance testing, [PCB-DFA-055](08-cleaning.md)) rather than assuming it.
Avoid treating coating as a substitute for cleaning.

**Why:** Electrochemical migration needs three things: a voltage, a conductive residue and moisture.
Coating a board over residue seals the residue in, with any moisture already there, right where the voltage is.
Properly heated no-clean residue is far less active than other fluxes' residue, which is why coating over it often works.

**What goes wrong if you don't:** Residue trapped under the coating, and the failures you coated the board to prevent.

**Applies to:** General practice.
Coating over no-clean flux is not unusual; cleaning first is still the safer choice.

**Sources:** [“Board Cleaning w/ Mike Konrad (part 2)”](https://www.buzzsprout.com/1066066/episodes/8488862-board-cleaning-w-mike-konrad-part-2) (May 2021), [01:06:00](https://www.buzzsprout.com/1066066/episodes/8488862?t=3960)–01:08:00; [“The role of flux in PCB assembly”](https://www.buzzsprout.com/1066066/episodes/10791051-the-role-of-flux-in-pcb-assembly) (Jun 2022), [22:00](https://www.buzzsprout.com/1066066/episodes/10791051?t=1320), on no-clean residue; the author's own experience of coated no-clean boards.

*Last reviewed: 2026-11-04*

---

## PCB-DFA-061: Mark on the drawing the areas that must not be coated

**Recommendation:** On the assembly drawing, mark every area that must stay free of coating: connector mating areas, switches, test points you'll probe, and anything adjusted or contacted after assembly.
Leave a few millimeters between keep-out areas and parts that must be coated.

**Why:** The coater masks or avoids exactly what the drawing shows.
Selective coating machines can't hold an edge right up to a keep-out, so they need some room.

**Typical values:** About 2–3 mm is usually the closest a selective coating process can reliably hold to a keep-out edge (one industry article).

![D43: Plan view of a 60 by 40 mm board as it would appear on an assembly drawing. Areas outlined in red and labeled do not coat cover a connector's mating area, a push switch and a row of test points. The nearest part that must be coated sits 2 to 3 mm from the connector's keep-out.](images/coating-keepouts.svg)

*D43 is drawn to scale.
Each area that must stay free of coating is outlined and labeled on the assembly drawing.
Parts that must be coated sit 2–3 mm from a keep-out edge, about the closest a selective coating process can reliably hold.*

**What goes wrong if you don't:** Coated connectors that won't make contact, or test points that can't be probed.

**Applies to:** General practice.
Whether test points are coated varies by customer; some require them coated.

**Sources:** Industry guidance on conformal coating drawings and keep-outs, including IPC-HDBK-830 (checked Nov 2026; not from the podcast).

*Last reviewed: 2026-11-04*

---

## Related pages
- [Cleaning](08-cleaning.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

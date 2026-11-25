# Moisture and storage

Moisture matters at three stages.
Bare boards absorb it before assembly, and that is covered by [PCB-DFA-080](../03-bare-board-fabrication/08-surface-finish.md).
Moisture-sensitive parts absorb it before they're soldered, and that is covered by [PCB-DFA-091 to 094](../04-components-and-materials/03-moisture-sensitive-parts.md).
This page covers the boards and parts you keep yourself: spare bare boards, spare parts and finished boards waiting to be used.

## PCB-DFA-113: Store spare boards and parts sealed in bags that block both static and moisture, with desiccant and a humidity card

**Recommendation:** Keep spare bare boards, moisture-sensitive parts and assembled boards you store for months in a moisture barrier bag made for electronics.
The bag should also protect against static.
Put fresh desiccant and a humidity indicator card in the bag, and heat-seal it, as in D60 in [Part 4](../04-components-and-materials/03-moisture-sensitive-parts.md).
Don't use a moisture barrier bag made for other goods, such as machine parts.
Don't use a plain static-shielding bag for long storage, because it doesn't keep moisture out.
Label each bag with what is inside and the date it was sealed.
When you send stored boards or parts to an assembler, send them in the sealed bag and say on the packing slip how long they have been stored.

**Why:** Bags made for electronics combine a moisture barrier with a static-safe inner layer and a metal layer that shields.
Moisture barrier bags made for other goods may block moisture but generate static.
A plain shielding bag blocks static but lets moisture through over weeks.
The humidity card shows whether the bag has kept the moisture out.
Bare boards take on moisture and their finish ages, so they may need baking or a solderability check before use (PCB-DFA-080).
Parts that have taken on moisture need baking before reflow (PCB-DFA-094).

**Typical values:** IPC-1602A says bare boards dry-packed this way should keep for at least a year below 40 °C and 90% relative humidity.
It recommends against drawing a full vacuum on the bag, because that can damage the desiccant, warp boards and puncture the bag.
For moisture-sensitive parts, J-STD-033 sets the floor life and the bake times.

**What goes wrong if you don't:** Stored boards or parts need baking before they can be built, which adds days to the job.
Or they're built without baking, and parts crack or joints fail in reflow.

**Applies to:** General practice, for anything you store for more than a few weeks.

**Sources:** ["How to Manage Moisture Sensitive Devices"](https://www.buzzsprout.com/1066066/episodes/10522014-how-to-manage-moisture-sensitive-devices) (May 2022), [21:00](https://www.buzzsprout.com/1066066/episodes/10522014?t=1260)–22:00 and [54:00](https://www.buzzsprout.com/1066066/episodes/10522014?t=3240)–56:00; IPC-1602A, *Standard for Printed Board Handling and Storage* (Nov 2024), section 4; IPC/JEDEC J-STD-033D, *Handling, Packing, Shipping and Use of Moisture/Reflow Sensitive Surface Mount Devices*.

*Last reviewed: 2026-11-12*

---

## Related pages
- [Static (ESD) protection](01-static-protection.md)
- [Surface finish](../03-bare-board-fabrication/08-surface-finish.md) (PCB-DFA-080, bare-board shelf life)
- [Moisture-sensitive parts](../04-components-and-materials/03-moisture-sensitive-parts.md) (PCB-DFA-091 to 094)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

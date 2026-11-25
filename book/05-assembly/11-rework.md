# Rework and repair

Rework is removing and replacing parts on an assembled board, by hand with a soldering iron, or with a hot-air or infrared rework station for BGAs and other parts with hidden joints.
It's slow, skilled work, and every rework heats the board and its neighbors again.

Much of what makes a board reworkable is decided elsewhere: space around parts ([PCB-DFA-023](02-component-placement.md)), package choice ([PCB-DFA-021 and 022](02-component-placement.md)), and reflow ratings that allow another heat cycle ([PCB-DFA-026](03-reflow-soldering.md)).
This page covers sending boards back to be fixed.

## PCB-DFA-063: Before sending boards back for repair, find the failing part and get a return number

**Recommendation:** Before you send failed boards back to your assembler, narrow the failure down to a part if you can, and tell them which part to replace.
Get a return authorization (RMA) number first, and pack the boards the way they were sent to you, in proper static-shielding packaging.

**Why:** An assembler has the tools to replace parts you can't, such as a BGA, but boards that arrive with no explanation can't be fixed efficiently.
If every board fails the same way, the cause has to be found before anything is replaced.
Boards repacked in unshielded bags can be damaged by static on the way back.

**Typical values:** For an inexpensive board (around $20), replacing a fine-pitch BGA can cost more than the board, so a refund or replacement may be offered instead.

**What goes wrong if you don't:** Delays, boards repaired without the real fault being found, or new damage in shipping.

**Applies to:** General practice.

**Sources:** [“Debugging PCB Assemblies”](https://www.buzzsprout.com/1066066/episodes/10713945-debugging-pcb-assemblies) (May 2022), [15:00](https://www.buzzsprout.com/1066066/episodes/10713945?t=900)–19:00; [“How Blue Robotics is enabling the next generation of ocean exploration robots w/ Rustom Jehangir”](https://www.buzzsprout.com/1066066/episodes/8139597-how-blue-robotics-is-enabling-the-next-generation-of-ocean-exploration-robots-w-rustom-jehangir) (Mar 2021), [53:00](https://www.buzzsprout.com/1066066/episodes/8139597?t=3180)–55:00.

*Last reviewed: 2026-11-04*

---

## Related pages
- [Component placement](02-component-placement.md)
- [Reflow soldering](03-reflow-soldering.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

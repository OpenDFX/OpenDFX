# Press-fit and mechanical parts

Some parts aren't soldered at all, or not only soldered.
Press-fit connectors and press-fit nuts are pushed into precisely sized plated holes by a press, and the tight fit makes the electrical and mechanical joint.
Heat sinks, standoffs, snap-in sockets and large connectors are often held with screws, nuts or clips as well.

Press-fit is strong and reliable, and needs no heat.
But each press-fit part needs its own press tooling and support under the board, so it isn't a standard step for every assembler.
What your design controls is which of these parts you choose, and how clearly you tell the assembler what they need.

## PCB-DFA-047: Talk to your assembler before designing in press-fit parts

**Recommendation:** Before you commit to a press-fit part, ask your assembler whether they can press it with the equipment they have, what tooling it will need and what that will cost.
Leave room on the far side of the board around each press-fit part for the support tooling.
If you order through an online quoting system, check that it has priced the press-fit parts; many don't detect them.

**Why:** Each press-fit part needs a press head shaped for it and an anvil supporting the board underneath, and the board has to be supported without crushing the surface-mount parts around it.
Simple parts such as press-fit nuts are usually easy with existing equipment; large press-fit connectors may need tooling made for them.

**What goes wrong if you don't:** A surprise tooling charge, a delay while tooling is made, or an assembler who can't do the job.

**Applies to:** Varies by manufacturer.
Check with yours.

**Sources:** [“Alternative Component Mounting”](https://www.buzzsprout.com/1066066/episodes/10030215-alternative-component-mounting) (Feb 2022), [18:00](https://www.buzzsprout.com/1066066/episodes/10030215?t=1080)–27:00.

*Last reviewed: 2026-11-04*

---

## PCB-DFA-048: Give a torque for every screw and nut, and fasten hardware before soldering

**Recommendation:** List a torque for every screw and nut in your bill of materials or assembly drawing, not just "tight".
Ask for hardware that fastens a part to the board (a connector's bolts, a regulator's heat-sink screw) to be tightened before the part is soldered.

**Why:** If a part is soldered first and then bolted down, the bolt pulls the part flat against the board and strains the joints that were made while it sat slightly high.
Over time, that strain fatigues and cracks the joints.
Fastened first, the joints only carry signals.

![D40: Side views of a connector bolted to the board, with three leads soldered through it. Soldered first and tightened afterwards, the flange is pulled down and bent, straining the solder joints. Tightened first and soldered afterwards, the flange sits flat and the joints carry no strain.](images/bolt-first.svg)

*D40.
The flange lift is exaggerated.
If the leads are soldered first, tightening the bolts pulls the part down after the joints have set, and the joints take the strain.
Tightened first, the part is already where it will stay when it is soldered.*

**What goes wrong if you don't:** Joints that pass test and crack later in the field, or hardware tightened by guesswork.

**Applies to:** General practice.

**Sources:** [“Alternative Component Mounting”](https://www.buzzsprout.com/1066066/episodes/10030215-alternative-component-mounting) (Feb 2022), [31:00](https://www.buzzsprout.com/1066066/episodes/10030215?t=1860)–35:00.

*Last reviewed: 2026-11-04*

---

## PCB-DFA-049: Avoid soldering a connector made only for press-fit

**Recommendation:** If a connector is designed only to be pressed in, press it in.
If you can't, and it has to be soldered, tell your assembler before the build.

**Why:** A press-fit connector's plastic isn't designed for soldering heat.
Soldering it needs a process that gets the heat in and out quickly enough to make the joint without damaging the housing.

**What goes wrong if you don't:** Melted or warped housings, or a delay while the assembler develops a special process.

**Applies to:** General practice.

**Sources:** [“The selective soldering process”](https://www.buzzsprout.com/1066066/episodes/7337971-the-selective-soldering-process) (Jan 2021), [41:00](https://www.buzzsprout.com/1066066/episodes/7337971?t=2460)–42:00.

*Last reviewed: 2026-11-04*

---

## Related pages
- [Through-hole soldering](05-through-hole-soldering.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

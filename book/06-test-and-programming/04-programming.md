# Programming

Most boards have at least one part that needs software before it will work, such as a microcontroller, an FPGA's configuration memory or a programmable clock.
There are three times the software can be loaded.
It can go into the loose parts before assembly, done by a distributor, a programming house or the assembler.
It can go into the finished board through a connection on the board.
Or you can load it yourself after the boards arrive.
Whichever you choose, the board and the paperwork have to allow for it.

## PCB-DFT-013: Give every programmable part a programming connection the assembler can reach: pads for a spring-pin cable, or a test fixture

**Recommendation:** If the parts aren't programmed before assembly, bring the programming signals to one place on the board that can be reached after assembly.
Include ground, and power and reset if the part's programming interface needs them.
Use a footprint of plain pads made for a spring-pin programming cable, with its locating holes, rather than fitting a connector.
Better still, put the programming signals on test points, so the test fixture programs the board as part of its test.
Put the pads on the same side as the test points (PCB-DFT-009).
Keep parts, tracks and vias out of the area the cable maker marks as a keep-out.
Leave paste off the pads.
Say on the assembly drawing or in the test plan whether the programmer powers the board, or whether the board needs its own power.

**Why:** A pad footprint adds nothing to the BOM and no step to assembly.
The cable's locating pins line it up the same way every time.
A header costs a part and a placement, often needs through-hole soldering, and stays on the board for its whole life for a job done once.
A fixture that touches every test point can reach the programming pads at the same time.
So the board is programmed and tested in one step, in one place, which is the quickest and most repeatable way of all.
A programming connection hidden under a part, behind a tall connector, or on the other side from everything else has to be reached by hand, one board at a time.

**Typical values:** Each cable maker publishes its own footprint.
D63 shows one maker's six-pin footprint, for a cable without retaining legs.
It has six round pads 0.787 mm in diameter, in two rows of three on a 1.27 mm (50 mil) grid.
Three non-plated holes 0.991 mm in diameter locate the cable.
There's one hole at one end and two at the other, so the cable only fits one way.
The maker asks for no tracks or vias between the two rows of pads.
Nothing else should come within 0.5 mm (0.020 in) of a pad.
The pads get no paste.
Use the exact footprint for the cable you'll use.
List it on the BOM as do-not-fit, so nobody tries to buy a part for it.

![D63: Plan view, drawn to scale. Six round copper pads 0.787 mm in diameter in two rows of three on a 1.27 mm grid, numbered 1, 3, 5 along the bottom and 2, 4, 6 along the top, with traces leaving each pad outwards. Three non-plated holes 0.991 mm in diameter: one at the pin-1 end on the center line, and two at the far end, 2.03 mm apart. The area between the rows is a shaded keep-out, and a dashed circle shows the 0.5 mm clearance round one pad.](images/spring-pin-pads.svg)

*D63 is drawn to scale, from one cable maker's published footprint.
The cable's spring pins land on the six pads, and its three locating pins drop into the holes.
The holes are placed so the cable only fits one way.*

**What goes wrong if you don't:** Every board has to be programmed by hand, with a clip or flying leads.
Or you pay for a connector on every board.
Or nobody can reach the part once the board is built.

**Applies to:** Varies by assembler, so ask yours which method and cable it uses.
Parts programmed before assembly don't need a connection on the board, but one is still useful for updates and repairs.

**Sources:** Chris Denney (author); a spring-pin programming-cable maker's published footprint for its six-pin cable without legs (Rev B); chip makers' programming-interface guidance.
Not covered in the podcast.

*Last reviewed: 2026-11-10*

---

## PCB-DFT-014: Say where each chip gets programmed, and give the exact file, version and checksum

**Recommendation:** For every programmable part, say who programs it and when.
That could be before assembly, on the finished board by the assembler, or by you.
Give the exact file to load, its version number and its checksum.
Also give any settings that go with it, such as fuse or option bytes, read-out protection, and serial numbers if each board gets its own.
Mark pre-programmed parts on the BOM with the file version, so a blank part can't be fitted by mistake (see [PCB-DFA-071](../01-design-package/03-bom.md#pcb-dfa-071-mark-do-not-place-and-customer-supplied-lines-clearly)).
Before the production run, have whoever will do the programming send you a few samples, and approve them.

**Why:** "Load the latest firmware" leaves the programmer guessing which file you mean.
A checksum is the only quick way to prove the right file went in.
Programming loose parts needs a socket made for that exact package.
If the programming house doesn't have one, buying it is expensive and slow.
Settings outside the main file, such as protection bits, are easy to forget, and some can't be changed once they're set.
Checking a few samples before the run stops a wrong or old file being loaded into a thousand parts.

**What goes wrong if you don't:** A thousand chips get the wrong file.
Or read-out protection is left off.
Or blank chips are fitted where programmed ones should be.

**Example:** One distributor's programming service checks the code first, then checks it has the right socket for the package.
It programs a few samples for the customer to approve before it programs the rest.
It doesn't want to program 1,000 controllers and then find out the code was wrong.

**Applies to:** General practice.

**Sources:** [“The role of electronic components distributors w/ Digi-key”](https://www.buzzsprout.com/1066066/episodes/8655719-the-role-of-electronic-components-distributors-w-digi-key) (Jun 2021), [43:00](https://www.buzzsprout.com/1066066/episodes/8655719?t=2580)–46:00.

*Last reviewed: 2026-11-10*

---

## PCB-DFT-015: Build a test mode into the production firmware rather than a separate test image

**Recommendation:** Give the production firmware a test mode that the test fixture can switch on.
For example, the fixture could hold a pin low at power-up, or send a command.
In test mode, the fixture should be able to read sensors, drive outputs and get results back.
Program each board once, with the production firmware, and test it in that state.
Make sure the test mode can't be switched on by accident in use.

**Why:** With only the normal firmware, the board does things on its own schedule.
A relay switches or a sensor is read when the firmware decides, so the test can't predict what to measure, and it checks much less.
Separate test firmware solves that, but then every board has to be programmed twice: once to test, and again to ship.
Each pass can take 30 seconds or more in the fixture, and you pay for both.
A test mode puts the board in a known state with only one programming pass.
Firmware engineers need to know about it from the start, because a test mode added late tends to have bugs that make good boards fail.

**What goes wrong if you don't:** You pay for every board to be programmed twice.
Or the test can't check much, because the board won't do what it's told.

**Applies to:** General practice.

**Sources:** [“How to develop a PCBA functional test system w/ FixturFab”](https://www.buzzsprout.com/1066066/episodes/10100478-how-to-develop-a-pcba-functional-test-system-w-fixturfab) (Feb 2022), [53:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=3180)–55:00 and [01:03:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=3780)–01:04:00.

*Last reviewed: 2026-11-10*

---

## Related pages
- [BOM](../01-design-package/03-bom.md) (customer-supplied and pre-programmed parts)
- [Consignment and spares](../04-components-and-materials/05-consignment-and-spares.md)
- [Boundary scan](03-boundary-scan.md) (the same connector often serves for both)
- [Functional test and fixtures](05-functional-test-and-fixtures.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

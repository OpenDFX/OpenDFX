# Boundary scan

Boundary scan is test circuitry built into many processors, FPGAs and other large chips.
It's defined in the standard IEEE 1149.1, and it's often called JTAG, after the group that wrote it.
Through four or five wires, a tester can take control of every pin on those chips.
It can drive the pins and read them, so it can check the connections between chips without a probe on each net.
It's useful on dense boards where test points won't fit, and under BGAs, whose pins nobody can touch.

## PCB-DFT-012: Where test points won't fit, use boundary scan: choose parts that support it and bring the chain to a connector

**Recommendation:** If the board is too dense for a test point on every net, plan for boundary scan from the start of the design.
Where you have a choice, pick parts that support boundary scan.
Get each part's boundary-scan description file (called a BSDL file) from its maker.
Link the parts into a chain: each part's TDO pin goes to the next part's TDI pin.
The TCK and TMS signals go to every part in the chain.
Bring the chain out to a connector or a set of test pads, with a ground pin beside the signals.
Follow each chip maker's advice on pull-up and pull-down resistors, and on terminating TCK.
If the advice isn't clear, leave pads for both a pull-up and a pull-down, so either can be fitted.
Make sure nothing on the board stops a chip from going into test mode, such as a pin that has to be held high or low, or a part that needs firmware before its pins work.

**Why:** Each boundary-scan part can drive and read its own pins.
So a tester can check every connection between two of these parts without touching the nets at all.
It can also check many connections to simpler parts, such as memory.
That can replace some or all of an in-circuit test fixture.
But it only works if the parts support it, the chain is complete and can be reached, and the board lets the chips go into test mode.
None of that can be added after the layout is done.
The same connector is often used for programming and debugging too (see [Programming](04-programming.md)).

**Typical values:** Boundary scan uses four signals: TCK, TMS, TDI and TDO.
Some parts add a fifth, a reset called TRST.
The connector also needs ground.
Chip makers commonly suggest pull-up resistors of 1 kΩ to 10 kΩ on TMS and TDI.
They also want TCK and TRST held at a set level, but they don't all agree on how, so follow each part's datasheet.

![D64: Block diagram, not to scale. A six-pin connector carries TCK, TMS, TRST, TDI, TDO and ground. TDI runs into U1, U1's TDO into U2, U2's TDO into U3, and U3's TDO back to the connector, forming one chain; TCK, TMS and TRST run to all three chips. TMS and TDI are pulled up and TRST pulled down. A memory chip without boundary scan is wired to U1.](images/boundary-scan-chain.svg)

*D64 is a block diagram, not to scale.
The test data runs through each boundary-scan part in turn, from TDI to TDO, and back to the connector.
The clock and control signals go to every part at once.
The memory has no boundary scan of its own, but its connections to U1 can still be tested through U1's pins.*

**What goes wrong if you don't:** On a dense board, the only way left to test the connections under the BGAs is a functional test.
A functional test often can't tell you which joint has failed.

**Applies to:** Boards with large digital parts that support boundary scan, such as processors, FPGAs and CPLDs.
Boundary scan needs its own software and controller, and the first project takes some setting up.

**Sources:** [“How to develop a PCBA functional test system w/ FixturFab”](https://www.buzzsprout.com/1066066/episodes/10100478-how-to-develop-a-pcba-functional-test-system-w-fixturfab) (Feb 2022), [24:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=1440)–27:00; IEEE 1149.1; chip makers' JTAG pin and termination guidance; boundary-scan tool makers' design-for-test guides.

*Last reviewed: 2026-11-10*

---

## Related pages
- [Flying probe and in-circuit test](02-flying-probe-and-ict.md)
- [Programming](04-programming.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

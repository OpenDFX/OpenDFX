# Design for test: test points and access

Every assembled board has to be tested to prove it works.
That's much easier if the designer planned for it.
A tester needs places to touch the board, a way to program it, and somewhere to hold it.
None of these can be added after the board is made, but most of them cost almost nothing if they're in the first layout.
For small builds, under about 1,000 boards, most customers test the boards themselves.
For larger volumes, it's normal for the assembler to test the boards on the customer's behalf.
Either way, the test plan has to start with you, because only you know what the board is meant to do.

## PCB-DFT-005: Decide how each board will be tested while you design it, and test boards before they go into anything expensive

**Recommendation:** Make testing one of the product's requirements from the first day of design.
Decide who will test each board: you, your assembler or a test house.
Decide how it will be tested: by flying probe, in a fixture, by a functional test or by boundary scan.
Test each board before it goes into a finished product, a chassis or any other step that takes real time or money.
Bring your firmware engineers in early, because the test usually needs help from the firmware.

**Why:** Test points, a programming connection, room for probes and tooling holes are all part of the layout.
If they're missing, adding them means a new board revision.
Firmware engineers write their code differently when they know from the start that it needs a test mode.
Test code added at the last minute tends to have bugs, and those bugs show up as boards failing test when nothing is wrong with them.
A bad board found after it's built into a product costs you the assembly time as well as the board.
It's also much harder to find the fault once the board is inside the product.

**What goes wrong if you don't:** You end up with a design that works but can't be tested without a redesign.
Or the test fixture costs thousands more than it needed to.
Or faulty boards are found only after hours of final assembly.

**Example:** One customer's finished product took about 17 hours to assemble after the boards arrived, and the boards weren't being tested before that work started.
Another built boards into a chassis that took about three hours to assemble before anything was powered.
In both cases a simple board test first would have caught faults before the expensive part of the build.
A purchasing manager once asked an assembler to guarantee that every board would work, for a design with no test of any kind.
There was no way to do it.

**Applies to:** General practice.

**Sources:** [“How to develop a PCBA functional test system w/ FixturFab”](https://www.buzzsprout.com/1066066/episodes/10100478-how-to-develop-a-pcba-functional-test-system-w-fixturfab) (Feb 2022), [01:02:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=3720)–01:06:00; [“Debugging PCB Assemblies”](https://www.buzzsprout.com/1066066/episodes/10713945-debugging-pcb-assemblies) (May 2022), [05:00](https://www.buzzsprout.com/1066066/episodes/10713945?t=300)–06:00; [“Inevitable Failures”](https://www.buzzsprout.com/1066066/episodes/17722984-inevitable-failures) (Aug 2025), [31:00](https://www.buzzsprout.com/1066066/episodes/17722984?t=1860)–38:00.

*Last reviewed: 2026-11-10*

---

## PCB-DFT-006: Write the test plan yourself, as numbered requirements tied to named test points

**Recommendation:** Write a test plan for every board, even a short one, and keep it with the design files.
Make each step a numbered requirement that either passes or fails.
Tie each step to a named test point, connector pin or function.
For example: "Step 3.1: TP4 reads 3.3 V, within 3%."
"Step 4.2: firmware version 2.1 loads."
"Step 5.1: LED D3 lights during boot."
Write the plan as plain text that anyone can open, not only inside one test system's software.
When a board fails in the field in a way the plan didn't catch, add a step that would have caught it.

**Why:** You know what the board is meant to do, but the assembler and the fixture builder don't.
That's especially true when you've used a common part in an unusual way.
A step tied to a test point can be built into any fixture, by anyone.
When a board fails, the report can name the step it failed.
A vague check like "it works" can't be repeated, and it doesn't tell anyone where to look.
A plain-text plan is easy to review, easy to compare between revisions, and easy to move to a different tester later.

**What goes wrong if you don't:** The assembler or fixture builder has to guess what matters.
They may test the wrong things, or nothing at all.
Failed boards come back marked "doesn't work".

**Example:** One fixture builder says only about half of its customers arrive with a test plan.
It would much rather start from one, because the designer knows the product best.

**Applies to:** General practice.

**Sources:** [“Smarter Test Plans for Inevitable Failures w/ Blue Clover CEO & Co-founder, Pete Staples”](https://www.buzzsprout.com/1066066/episodes/17955982-smarter-test-plans-for-inevitable-failures-w-blue-clover-ceo-co-founder-pete-staples) (Oct 2025), [21:30](https://www.buzzsprout.com/1066066/episodes/17955982?t=1290)–23:00 and [33:00](https://www.buzzsprout.com/1066066/episodes/17955982?t=1980)–36:30; [“How to develop a PCBA functional test system w/ FixturFab”](https://www.buzzsprout.com/1066066/episodes/10100478-how-to-develop-a-pcba-functional-test-system-w-fixturfab) (Feb 2022), [56:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=3360)–01:00:00.

*Last reviewed: 2026-11-10*

---

## PCB-DFT-007: Put a test point on every net you want to test, and on every net if you want in-circuit test

**Recommendation:** Give every net in your test plan its own test point.
If the board will get an in-circuit test, by flying probe or in a bed-of-nails fixture, aim for a test point on every net.
Make a list of any nets you leave without one on purpose.
Place test points while you lay out the board, not after the routing is finished.
Give the fixture builder a list of the test points, with each one's net name, its X and Y position from the board's origin, and which side of the board it's on.
Don't tie a part's control pins, such as enable or output-enable, straight to ground or to the supply.
Connect them through a resistor, so the tester can override them.

**Why:** In-circuit test checks each part by measuring between nets with the power off.
If the tester can't touch a net, it can't check that net or any part on it.
Probing a part's own pad or lead instead is less reliable, because the probe can slip, mark the joint or miss it.
Test points are cheap to place early, and very hard to squeeze into a finished, dense layout.
A control pin tied straight to ground or the supply can't be changed by the tester, so it can't run its standard test on that part.

**Typical values:** For full in-circuit test, one test point on every net.
IPC-2221C asks for a test land on every node, and says fewer are needed when boundary scan is used.
For functional test, a test point on each net the test plan measures.

**What goes wrong if you don't:** Faults on nets the tester can't reach go undetected.
If too many nets are missing, in-circuit test stops being worth paying for.

**Example:** At one consumer-products company, the boards were so small that not enough test points would fit for in-circuit test to be worth doing, so they relied on functional test alone.

**Applies to:** General practice.
How close to full coverage is worth paying for depends on volume and on what a missed fault would cost.

**Sources:** [“How to develop a PCBA functional test system w/ FixturFab”](https://www.buzzsprout.com/1066066/episodes/10100478-how-to-develop-a-pcba-functional-test-system-w-fixturfab) (Feb 2022), [21:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=1260)–22:00 and [57:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=3420); IPC-2221C (December 2023), sections 3.6.5.1 and 3.6.5.2; fixture makers' and test houses' published design-for-test guides.

*Last reviewed: 2026-11-10*

---

## PCB-DFT-008: Make test points surface-mount pads at least 0.9 mm in diameter and 1.9 mm apart, with no paste

**Recommendation:** Make each test point a surface-mount copper pad with the solder mask pulled back from it.
Make it at least 0.9 mm in diameter, and 1.0 mm if you can.
Round pads are the usual choice, but square pads are fine too and give the probe more room to land.
For a square pad, use the same numbers for the length of each side.
Space test points at least 1.9 mm (75 mil) apart, center to center, and 2.54 mm (100 mil) if you can.
Leave paste off the test points (see [PCB-DFA-019](../05-assembly/01-solder-paste-and-stencils.md#pcb-dfa-019-put-paste-on-every-pad-you-want-soldered-and-only-those)).
The one exception is a board with an OSP finish, where you should put paste on the test points so they're solder-coated.
Print the net name in silkscreen beside each pad.
If someone needs to clip a meter or scope probe on by hand, use a surface-mount test point (a small metal loop made for reflow), not a through-hole one.
Tell your assembler on the assembly drawing whether the test points must stay free of flux and solder.
If the test points won't be used in production, say that too.

**Why:** A probe never lands exactly on target, because the fixture and the board both have tolerances.
A bigger pad means the probe still hits it.
A square pad has about 27% more area than a round pad whose diameter equals the square's side.
IPC-2221C asks for test points to be solder-coated, or to have a surface finish that doesn't oxidize.
ENIG, HASL, immersion silver and immersion tin don't oxidize the way bare copper does, so on those boards the finish is enough.
Solder on a test point makes a dome that a probe can slide off, so avoid it on boards with those finishes.
OSP is different, because it leaves bare copper that oxidizes, and probes can't make good contact through the oxide.
So on an OSP board, a thin coat of solder on each test point is better than bare copper.
Spacing decides which probes will fit.
At 2.54 mm, the fixture can use standard probes, which are the sturdiest and cheapest.
Closer spacing needs thinner probes, which cost more, bend more easily and wear out faster.
A flying-probe tester can reach much smaller pads than a fixture can.
So a board laid out for a fixture can always be flying-probed, but not the other way round.
A surface-mount test point is placed by the machine and soldered in reflow with everything else, so it adds almost nothing to the cost.
A through-hole test point has to be fitted by hand and soldered afterwards, often by selective soldering, which is slower and harder than reflow.
Test points that must stay clean also have to be protected during selective soldering, and that can get in the way of soldering nearby through-hole parts.
If the assembler knows the test points won't be used, it doesn't have to protect them, and selective soldering is much easier.

**Typical values:**

| Test point | Minimum | Recommended |
|---|---|---|
| Pad diameter | 0.9 mm | 1.0 mm or more |
| Center-to-center spacing | 1.9 mm (75 mil) | 2.54 mm (100 mil) |

IPC-2221C says a test land used for probing should be at least 0.9 mm in diameter.
It says 0.6 mm is possible on boards smaller than 7,700 mm².
It also asks for test lands on 2.5 mm centers where possible, so standard probes can be used.
One test-equipment maker's fixture specification asks for test points at least 1.0 mm in diameter and at least 2.0 mm apart.
The fixture builder on the podcast gives 0.8 mm as its minimum.
Some published guides say 1.27 mm (50 mil) spacing is possible, but it costs more.
Flying-probe testers can usually probe pads of 0.5 mm or smaller, but check with yours.

![D61: Plan view of the corner of a board, drawn to scale. Three round test points, each a copper pad 1.0 mm in diameter with the mask cleared, sit 2.54 mm apart. An 0603 resistor sits 1 mm from the first. A fourth test point is kept 5 mm from a tall radial capacitor, and the 5 mm zone around the capacitor is shaded. The strip along the edge of the board is marked at 3 mm and 5 mm.](images/test-points.svg)

*D61 is drawn to scale.
The test points are pads 1.0 mm in diameter, 2.54 mm apart, each with its name in silkscreen.
The nearest short part is 1 mm away.
The tall capacitor has a 5 mm zone around it where a probe can't reach.
No test point is within 5 mm of the edge of the board.*

**What goes wrong if you don't:** Probes miss their pads, and good boards fail the test.
Or the fixture costs more because it needs fine probes.

**Applies to:** General practice.
Check the minimum sizes with whoever builds your fixture.

**Sources:** [“How to develop a PCBA functional test system w/ FixturFab”](https://www.buzzsprout.com/1066066/episodes/10100478-how-to-develop-a-pcba-functional-test-system-w-fixturfab) (Feb 2022), [57:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=3420)–58:00; [“All the Tricks and Gotchas in Surface Mount Assembly (Repost from the Coriolis Effect)”](https://www.buzzsprout.com/1066066/episodes/11006453-all-the-tricks-and-gotchas-in-surface-mount-assembly-repost-from-the-coriolis-effect) (Jul 2022), [01:20:00](https://www.buzzsprout.com/1066066/episodes/11006453?t=4800); [“When to use through hole vs surface mount components”](https://www.buzzsprout.com/1066066/episodes/8803410-when-to-use-through-hole-vs-surface-mount-components) (Jul 2021), [18:00](https://www.buzzsprout.com/1066066/episodes/8803410?t=1080)–22:00; Chris Denney (author); IPC-2221C (December 2023), section 3.6.5.1; a test-equipment maker's in-circuit test fixture specification (April 2020); fixture makers' and test houses' published design-for-test guides.

*Last reviewed: 2026-11-10*

---

## PCB-DFT-009: Keep test points on one side, clear of tall parts and the board edge, and off connector solder joints

**Recommendation:** Put all the test points on one side of the board, top or bottom.
Choose the side with fewer or shorter parts.
Keep each test point at least 1 mm from the body of a short surface-mount part.
Keep it 5 mm away from tall parts such as connectors, electrolytic capacitors and transformers.
Keep test points at least 3 mm from the edges of the board, and 5 mm if you can, because conveyors and fixtures grip the edges (see [PCB-DFA-015](../02-the-panel/04-edge-clearance.md#pcb-dfa-015-keep-parts-and-exposed-copper-at-least-3-mm-from-the-edges-5-mm-if-you-can)).
If a signal goes to a through-hole connector, add a test point on that net instead of probing the connector's solder joint.
Don't use gold edge-connector fingers as test points, because probes damage them.
Avoid using vias as test points.
A dedicated pad is more reliable, and a tented via can't be probed at all.
Spread the test points evenly over the board, rather than bunching them in one area.

**Why:** A fixture that probes one side needs only one plate of probes.
Probing both sides needs a second plate, lined up with the first.
That costs more, and it's less reliable over the life of the fixture.
A probe is a long, thin pin held in a plate.
Next to a tall part, the plate has to be cut away and the probe made much longer, if it fits at all.
After wave or selective soldering, the joints on a through-hole connector are covered in flux.
Probes that land on flux get dirty quickly and stop making good contact.
IPC-2221C allows through-hole pins to be used as test points to save space, but a dedicated pad is more reliable.
When the test points are bunched in one area, the probes push harder there, so the board flexes and the vacuum seal in the fixture can leak.

**Typical values:** IPC-2221C gives a simple rule for the space around a test point.
The clear space should be 80% of the height of the nearest part.
It should never be less than 0.6 mm, and it never needs to be more than 5.0 mm.
For example, next to a part 2 mm tall, keep 1.6 mm clear.
On the side being probed, IPC-2221C says parts shouldn't be taller than 5.7 mm.
Taller parts need cut-outs in the fixture, and test points should be 5.0 mm away from them.
Keep test points at least 3 mm from the edge of the board, and 5 mm if you can.
IPC-2221C also says 3.0 mm.
One test-equipment maker's fixture specification asks for at least 2 mm between a test point and any part, and between a test point and the edge of the board.

![D62: Side views, drawn to scale. Left, marked good: a 1.6 mm board with its parts on top and all its test points underneath, probed by short spring probes rising from one 10 mm plate. Right, marked to avoid: the same board with a test point on top, 1 mm from an 11.5 mm tall capacitor, reached by a long probe from a top plate that needs a cut-out over the tall parts.](images/probe-access.svg)

*D62 is drawn to scale.
On the left, all the test points are on the side with no parts, so one plate of short probes reaches them all.
On the right, a test point on top sits 1 mm from a tall capacitor.
To reach it, the fixture needs a second plate cut away around the parts, and a probe longer than the capacitor, squeezed into the 1 mm gap.*

**What goes wrong if you don't:** The fixture costs more and wears out faster.
Some nets may not be reachable at all.

**Example:** One fixture probed the flux-covered leads of through-hole parts with cup-tipped probes.
It worked on the first day.
Within a week, flux had built up in the probe tips, and good boards kept failing.
The probes had to be wire-brushed several times a day and replaced every couple of weeks, instead of every six months.

**Applies to:** General practice.
A flying-probe tester can reach both sides, but testing one side is still faster and cheaper.

**Sources:** [“How to develop a PCBA functional test system w/ FixturFab”](https://www.buzzsprout.com/1066066/episodes/10100478-how-to-develop-a-pcba-functional-test-system-w-fixturfab) (Feb 2022), [34:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=2040)–38:00, [58:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=3480) and [01:06:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=3960)–01:07:00; IPC-2221C (December 2023), section 3.6.5.1 and Figures 3-2 to 3-4; IPC-SMEMA-9851 (conveyor edge grip); one contract manufacturer's published design guidelines for in-circuit testability (2020); a test-equipment maker's in-circuit test fixture specification (April 2020).

*Last reviewed: 2026-11-10*

---

## PCB-DFT-010: Avoid potentiometers, DIP switches and jumpers that someone has to set by hand

**Recommendation:** Avoid parts that someone has to adjust or set by hand during production, such as trimming potentiometers, DIP switches and jumpers.
Set the value in firmware, with a fixed resistor, or with a digital potentiometer that the test can adjust.
If you can't avoid a mechanical part, give its setting in the test plan and on the assembly drawing.

**Why:** Every hand adjustment is a step someone can forget or get wrong, and a test can't easily check it.
Setting a potentiometer means probing and turning it at the same time, one board at a time.
These parts are often through-hole too, which adds a soldering step.
Switches can also get knocked out of position after the board has been tested.

**What goes wrong if you don't:** Boards ship with switches in the wrong position, or with trimmers never set.
Testing is slow, and the result depends on who did it.

**Applies to:** General practice.

**Sources:** [“Smarter Test Plans for Inevitable Failures w/ Blue Clover CEO & Co-founder, Pete Staples”](https://www.buzzsprout.com/1066066/episodes/17955982-smarter-test-plans-for-inevitable-failures-w-blue-clover-ceo-co-founder-pete-staples) (Oct 2025), [24:00](https://www.buzzsprout.com/1066066/episodes/17955982?t=1440)–25:00; [“When to use through hole vs surface mount components”](https://www.buzzsprout.com/1066066/episodes/8803410-when-to-use-through-hole-vs-surface-mount-components) (Jul 2021).

*Last reviewed: 2026-11-10*

---

## Related pages
- [Rails, tooling holes and fiducials](../02-the-panel/02-rails-tooling-holes-fiducials.md) (PCB-DFT-001, tooling holes for a test fixture)
- [Flying probe and in-circuit test](02-flying-probe-and-ict.md)
- [Functional test and fixtures](05-functional-test-and-fixtures.md)
- [Conformal coating](../05-assembly/09-conformal-coating.md) (keeping test points free of coating)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

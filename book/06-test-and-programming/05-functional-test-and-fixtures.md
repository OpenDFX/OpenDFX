# Functional test and fixtures

A functional test powers the board up and checks that it does its job.
The power supplies come up, the firmware loads, the inputs read correctly and the outputs work.
It's usually done in a fixture that holds the board and touches its test points with spring-loaded probes.
The fixture then runs through the test plan automatically.
A good fixture tests a board in seconds and says exactly what failed.
A poor one fails good boards and wears out quickly.

## PCB-DFT-016: Make every test failure point to a place on the board

**Recommendation:** Write each test step so that a failure names the part of the circuit involved, not just "fail".
Report the step number and where on the board the problem is.
For example, "Step 3.1 failed: 3.3 V rail low, check U4, L2 and C17" is far more useful than "power failure".
"USB port 3 of 12 failed" is far more useful than "USB failure".
Where you can, make each step a simple electrical check, such as a voltage, a current or a reply from a chip.
Don't recreate real-world conditions, such as spraying water on a water sensor, unless the product truly needs it.

**Why:** The person repairing a failed board needs to know where to look.
If a board with 400 parts just "fails the test", the fault could be in any of them.
If the failure names three parts, it can be fixed in minutes.
Simple electrical checks are fast, repeatable and cheap to build into a fixture.
Recreating real-world conditions is slow, and it adds more things that can go wrong in the fixture itself.

**What goes wrong if you don't:** Failed boards take hours to diagnose, or get set aside and never fixed.

**Example:** One customer built a test fixture with a small screen that listed the parts involved in each failure, such as U1, R13, C43 and J4.
The assembler called it "solid gold", because every failed board came back with the likely parts already named.

**Applies to:** General practice.

**Sources:** [“Debugging PCB Assemblies”](https://www.buzzsprout.com/1066066/episodes/10713945-debugging-pcb-assemblies) (May 2022), [08:00](https://www.buzzsprout.com/1066066/episodes/10713945?t=480)–10:00; [“Smarter Test Plans for Inevitable Failures w/ Blue Clover CEO & Co-founder, Pete Staples”](https://www.buzzsprout.com/1066066/episodes/17955982-smarter-test-plans-for-inevitable-failures-w-blue-clover-ceo-co-founder-pete-staples) (Oct 2025), [27:00](https://www.buzzsprout.com/1066066/episodes/17955982?t=1620)–30:30; [“How to develop a PCBA functional test system w/ FixturFab”](https://www.buzzsprout.com/1066066/episodes/10100478-how-to-develop-a-pcba-functional-test-system-w-fixturfab) (Feb 2022), [28:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=1680)–31:00.

*Last reviewed: 2026-11-10*

---

## PCB-DFT-017: Match the fixture to the volume, and send spare boards to the people building it

**Recommendation:** Choose the fixture to suit the number of boards it will test.
Use a simple development fixture for prototypes and the first few hundred boards.
Use a production fixture for steady volume.
Have it built by people who build fixtures for a living.
Ask for the probes to sit in sockets (receptacles), not soldered in, so worn probes can be swapped.
Send the fixture builder several assembled boards, not just one.
Send the schematic, the fabrication data and a 3D model of the board too.
Allow time, because a custom fixture takes weeks to design and build, and often needs a revision or two.

**Why:** A fixture is a machine that has to work thousands of times.
Its probes wear, collect flux and stick, and they need replacing.
A cheap, improvised fixture works at first, but in the end it costs more in repairs and failed good boards than a well-built one.
Boards sometimes get damaged while a fixture is being developed, so the builder needs spares.
The same goes for other custom production tooling, such as carriers and holding fixtures for assembly.
Often nobody finds out it's needed until the first larger build.

**Typical values:** A development fixture is made of acrylic or MDF and lasts for a couple of hundred boards.
A production fixture is made of FR4 plates about 10 mm thick and lasts for tens or hundreds of thousands of boards.
Probes last about six months when they land on clean pads, but as little as two weeks on flux-covered joints.
Custom tooling takes about two weeks to design, plus time to make it, try it and revise it.

**What goes wrong if you don't:** Good boards fail, or bad boards pass because a probe isn't really touching them.
A poor fixture can even damage the boards it tests.

**Example:** At one company, a spring-loaded probe in the fixture kept sticking.
When it stuck, the board's ground was left floating during the test, and the same diode burned out on board after board.
Once someone spotted the pattern, the repair became routine: "replace D1, check probe 13".
But the fault was in the fixture, not the boards.
Another customer's home-made fixtures were held together with wires and hot glue.
They worked, but they needed constant repair.

**Applies to:** General practice.

**Sources:** [“How to develop a PCBA functional test system w/ FixturFab”](https://www.buzzsprout.com/1066066/episodes/10100478-how-to-develop-a-pcba-functional-test-system-w-fixturfab) (Feb 2022), [13:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=780)–14:00, [34:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=2040)–38:00, [52:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=3120) and [56:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=3360); [“Inevitable Failures”](https://www.buzzsprout.com/1066066/episodes/17722984-inevitable-failures) (Aug 2025), [24:00](https://www.buzzsprout.com/1066066/episodes/17722984?t=1440)–28:00; [“Custom tooling to the rescue”](https://www.buzzsprout.com/1066066/episodes/10804740-custom-tooling-to-the-rescue) (Jul 2022), [15:00](https://www.buzzsprout.com/1066066/episodes/10804740?t=900)–17:00.

*Last reviewed: 2026-11-10*

---

## PCB-DFT-018: Agree with your assembler what happens to boards that fail

**Recommendation:** Before the first production run, agree with whoever tests the boards what happens to a board that fails.
- Label it straight away with the step it failed, on a printed label rather than a note on masking tape.
- Put it in an ESD-safe bin, away from the good boards.
- Tell you about each failure straight away, not in a batch at the end of the run.
- Record every repair, even when nobody knows why replacing a part fixed the board.
- Keep any parts that were removed, so they can go back to the supplier.
- Keep a shared log of each failure and what fixed it, so the next board with the same failure is quick to repair.

When you send boards back for repair, get a return number (RMA) first.
Find the cause yourself first if you can.
Pack the boards as carefully as they came to you, in ESD-shielding bags (see Part 7).

**Why:** Anyone can diagnose a board later if it's labeled with the step it failed.
Nobody can diagnose "doesn't work".
One failure on its own often doesn't tell you much.
Several boards with the same failure usually point to one cause, such as a wrong part value, a bad reel, a stencil problem or the fixture itself.
So if failures are rare, it usually pays to let a few identical ones build up and look at them together.
If a lot of boards in one batch fail, look at them straight away.
A part that's replaced and thrown away without a record hides the pattern, and loses the evidence the supplier needs.
Boards sent back loose, or in the wrong bag, can be damaged again on the way.
The assembler then has to record that damage before it can repair them.

**Typical values:** In one example, 30 failures out of a batch of 500 was enough to investigate straight away.
Otherwise, collect 20 to 40 similar failures before digging in.
For a cheap board with a fault that's hard to repair, such as a failed fine-pitch BGA, replacing the board may cost less than repairing it.

**What goes wrong if you don't:** Failed boards get mixed back in with good ones.
The same fault is diagnosed from scratch every time.
Or a whole batch is sent back with no idea what's wrong with it.

**Example:** In one investigation, 35 of 40 failed boards turned out to have the same cause.
At one contract manufacturer, technicians used to swap out a part that fixed a failing board, throw the old part away and say nothing.
Nobody could spot the pattern or send the part back to the supplier.
The company's rule became "share bad news immediately".

**Applies to:** General practice.
It matters most for repeat production.
Small builds are often tested by the customer, but at larger volumes the assembler usually does the testing.

**Sources:** [“Smarter Test Plans for Inevitable Failures w/ Blue Clover CEO & Co-founder, Pete Staples”](https://www.buzzsprout.com/1066066/episodes/17955982-smarter-test-plans-for-inevitable-failures-w-blue-clover-ceo-co-founder-pete-staples) (Oct 2025), [27:00](https://www.buzzsprout.com/1066066/episodes/17955982?t=1620)–33:00 and [39:00](https://www.buzzsprout.com/1066066/episodes/17955982?t=2340)–41:00; [“Debugging PCB Assemblies”](https://www.buzzsprout.com/1066066/episodes/10713945-debugging-pcb-assemblies) (May 2022), [09:00](https://www.buzzsprout.com/1066066/episodes/10713945?t=540)–22:00; [“Inevitable Failures”](https://www.buzzsprout.com/1066066/episodes/17722984-inevitable-failures) (Aug 2025), [24:00](https://www.buzzsprout.com/1066066/episodes/17722984?t=1440)–28:00; [“How Blue Robotics is enabling the next generation of ocean exploration robots w/ Rustom Jehangir”](https://www.buzzsprout.com/1066066/episodes/8139597-how-blue-robotics-is-enabling-the-next-generation-of-ocean-exploration-robots-w-rustom-jehangir) (Mar 2021), [53:00](https://www.buzzsprout.com/1066066/episodes/8139597?t=3180)–55:00.

*Last reviewed: 2026-11-10*

---

## Related pages
- [Design for test: test points and access](01-test-points.md)
- [Programming](04-programming.md)
- [Burn-in, stress testing and early failures](06-burn-in-and-stress.md)
- [Rework](../05-assembly/11-rework.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

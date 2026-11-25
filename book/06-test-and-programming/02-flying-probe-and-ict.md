# Flying probe and in-circuit test

In-circuit test (ICT) checks that the right parts are fitted, the right way round, and soldered.
It does this by measuring between nets with the power off.
It finds shorts, opens, wrong values, and missing or backwards parts, and it says exactly where they are.
It doesn't prove the board works.
That's the job of a functional test.
There are two ways to do it.
A flying-probe tester moves a few probes around the board from point to point, and needs no tooling.
A bed-of-nails fixture has a probe for every test point and touches them all at once.

## PCB-DFT-011: Choose flying probe or a bed-of-nails fixture by volume, and design for the one you'll use

**Recommendation:** For prototypes, small batches and designs that are still changing, plan on a flying-probe test, or none.
For steady production in the thousands, consider a bed-of-nails fixture.
If you do, lay the board out for it from the start.
That means a test point on every net (PCB-DFT-007), pads big enough and far enough apart for a fixture (PCB-DFT-008), all on one side (PCB-DFT-009), and tooling holes in the board (PCB-DFT-001).
If you're not sure which you'll use, lay the board out for a fixture anyway, because it can always be flying-probed too.
Before you finish the layout, ask your assembler or test house what equipment they have and what they'd recommend for your volume.

**Why:** A flying-probe tester only needs a program made from your design data, so it costs little to set up.
It can probe both sides of the board and reach small pads.
But it moves its probes one point at a time, so it can take minutes to test each board.
A fixture tests a board in seconds, because it touches every test point at once.
But it has to be designed and built for one revision of the board, and changed whenever a test point moves.
So a fixture is only worth its cost when it's spread over a lot of boards.
Both kinds of tester learn what a good board looks like by measuring known-good boards, so they work best once the design has settled.

**Typical values:** Fixtures come in two grades.
A development fixture is made of acrylic or MDF and lasts for a few hundred boards.
A production fixture is made of FR4 about 10 mm thick and lasts for tens or hundreds of thousands of boards.
A custom production fixture can cost tens of thousands of dollars.
In 2025, one test company put a fixture at about $50,000 and a high-end in-circuit tester at about $1,000,000.
Prices vary widely and will change.
Between a home-made fixture and a high-end tester, there are simpler production test systems built around your test plan.

**What goes wrong if you don't:** You pay for a fixture before the design has settled, and then pay again to rebuild it.
Or a high-volume board spends minutes on a flying-probe tester.
Or the layout doesn't allow either kind of test.

**Example:** One fixture builder starts by asking every customer how many boards they'll build a year.
At 1,000 a year, a $100,000 fixture doesn't make sense.
At a million a year, it does.

**Applies to:** General practice.
What's available varies by assembler and test house.

**Sources:** [“How to develop a PCBA functional test system w/ FixturFab”](https://www.buzzsprout.com/1066066/episodes/10100478-how-to-develop-a-pcba-functional-test-system-w-fixturfab) (Feb 2022), [13:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=780)–14:00, [20:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=1200)–24:00 and [59:00](https://www.buzzsprout.com/1066066/episodes/10100478?t=3540)–01:00:00; [“Smarter Test Plans for Inevitable Failures w/ Blue Clover CEO & Co-founder, Pete Staples”](https://www.buzzsprout.com/1066066/episodes/17955982-smarter-test-plans-for-inevitable-failures-w-blue-clover-ceo-co-founder-pete-staples) (Oct 2025), [17:00](https://www.buzzsprout.com/1066066/episodes/17955982?t=1020)–18:00; test houses' published comparisons of flying-probe and fixture test.

*Last reviewed: 2026-11-10*

---

## Related pages
- [Design for test: test points and access](01-test-points.md)
- [Boundary scan](03-boundary-scan.md)
- [Bare-board test](../03-bare-board-fabrication/11-bare-board-test.md) (flying probe and fixtures for the bare board, PCB-DFT-002)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

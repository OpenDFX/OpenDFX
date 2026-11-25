# Burn-in, stress testing and early failures

Even a well-designed, well-built batch has a few boards that fail early.
The cause might be a weak solder joint, a part with a hidden flaw, or a little moisture damage.
Most of these boards fail in the first hours or weeks of use.
After that, the failure rate drops to a low, steady level for the rest of the product's life.
Engineers draw this as the left-hand side of a "bathtub curve".
A production test proves a board works today.
Stress screening tries to make the weak boards fail in the factory, before they reach a customer.

## PCB-DFT-019: Decide whether your product needs thermal cycling or burn-in, ask for it by name, and don't mistake a line test for validation

**Recommendation:** For each product, decide whether the boards need stress screening before they ship.
If they do, decide which kind, for how long, and to what limits.
Write it in the test plan, and agree it with your assembler before they quote.
Thermal cycling takes boards hot and cold over and over, with a pause at each end.
It's usually the better screen for assembly defects.
Burn-in runs boards powered up at a raised temperature for hours.
It's aimed at weak parts.
Don't treat a pass on the production test as proof that the design is reliable.
Proving the design, with environmental testing, life testing and qualification, is a separate job done before production.
Check that boards built on the production line perform like the ones you tested in the lab.

**Why:** A production test checks each board for the faults in the test plan, at room temperature, for seconds or minutes.
Some faults only show up after heat, cold, vibration or hours of running.
Cracked joints, moisture damage inside a part and marginal parts are examples.
Screening isn't included unless you ask for it.
It needs test chambers, time and power, so it's quoted separately.
Products used outdoors, in vehicles, in medical equipment or in industrial plants usually need it.
Low-cost products used indoors often don't, but even they can benefit from a short thermal-cycling screen.

**Typical values:** There's no single standard for commercial boards.
The limits come from the parts' ratings and where the product will be used.
Production stress screens commonly take a few hours.
Burn-in commonly takes 24 to 48 hours, and longer when it's used to qualify a design.
Plan for a few early failures in any batch.
For example, if you need 100 good boards, order 105 to 110.

**What goes wrong if you don't:** Weak boards pass the test and fail weeks later in the field.
Each of those failures costs far more than one caught in the factory.

**Example:** A part with moisture damage passed a 30-second bench test, then failed in the field after running hot for a while.
One company launched a product that had only been proven in its engineering lab.
The production units shipped with problems nobody had checked them for, and the company changed how it launches products.
A maker of sensors for power plants puts its boards through its own environmental testing, on top of the assembler's functional test, because a production test alone isn't enough for that use.
One test engineer expects to find around ten more problems after the "golden sample" is signed off, once real production volumes start.

**Applies to:** Depends on the product's use and reliability needs.

**Sources:** [“Inevitable Failures”](https://www.buzzsprout.com/1066066/episodes/17722984-inevitable-failures) (Aug 2025), [21:00](https://www.buzzsprout.com/1066066/episodes/17722984?t=1260)–23:00 and [31:00](https://www.buzzsprout.com/1066066/episodes/17722984?t=1860)–35:00; [“Smarter Test Plans for Inevitable Failures w/ Blue Clover CEO & Co-founder, Pete Staples”](https://www.buzzsprout.com/1066066/episodes/17955982-smarter-test-plans-for-inevitable-failures-w-blue-clover-ceo-co-founder-pete-staples) (Oct 2025), [44:00](https://www.buzzsprout.com/1066066/episodes/17955982?t=2640)–51:00; [“How to Manage Moisture Sensitive Devices”](https://www.buzzsprout.com/1066066/episodes/10522014-how-to-manage-moisture-sensitive-devices) (May 2022), [16:00](https://www.buzzsprout.com/1066066/episodes/10522014?t=960)–18:00; [“How Blue Robotics is enabling the next generation of ocean exploration robots w/ Rustom Jehangir”](https://www.buzzsprout.com/1066066/episodes/8139597-how-blue-robotics-is-enabling-the-next-generation-of-ocean-exploration-robots-w-rustom-jehangir) (Mar 2021), [28:00](https://www.buzzsprout.com/1066066/episodes/8139597?t=1680)–29:00; published reliability-test practice (environmental stress screening, burn-in, HALT and HASS).

*Last reviewed: 2026-11-10*

---

## Related pages
- [Functional test and fixtures](05-functional-test-and-fixtures.md)
- [Moisture-sensitive parts](../04-components-and-materials/03-moisture-sensitive-parts.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

# Prototype versus production

A prototype proves the design works.
Production proves it can be built the same way, many times, at a cost you can sell it for.
These are different jobs.
Parts that were placed by hand on five prototypes need feeders, nozzles and machine programs for five thousand boards.
A process that was fine for a few boards can show its weak spots at volume.
This page covers how to plan the step from one to the other.
First articles, which check a proven design before a big run, are covered in [Part 6.7](../06-test-and-programming/07-first-articles.md).

## PCB-DFA-122: Plan the move from prototype to production as a ramp, not a jump

**Recommendation:** Don't go straight from a few prototypes to a full production order.
Build in steps, such as 20 boards, then 200, then 1,000, and then the full volume, as in D66.
Before the first large build, talk to your manufacturer about your volumes and anything that was done by hand on the prototypes.
Replace hard-to-find parts, hobby modules and hand-fitted parts with mainstream parts on tape where you can (PCB-DFA-083 and 085).
If anything in the design or BOM has changed since the last build, expect new first articles (PCB-DFA-107).
Check that boards built on the production line perform like the ones you tested in the lab.
Expect the first production batch to run slower than later ones, and expect to find a few more issues.
If the volume is far beyond what your manufacturer has built for you before, consider splitting the first large order between two manufacturers.

**Why:** Each step shows up problems while they're still cheap to fix.
The first large batch is where the assembler learns the board's quirks: a via in an awkward place, a part that has to be hand-soldered because of its neighbors, a polarity mark that is easy to misread.
Later batches run faster because those quirks are known.
Problems that a few prototypes never showed only appear once hundreds of boards are built.

**Typical values:** A typical ramp is 20, then 200, then 1,000, then 2,000 or more.
After a design reaches a signed-off golden sample, expect to find about ten more issues once it reaches real production volume.

**What goes wrong if you don't:** A large first order with a fault that affects every board.
Or a launch that slips while the manufacturer works out how to build the board at volume.

**Example:** In one case, about 8 months of engineering went into reaching a golden sample.
About ten more issues were still found once the product moved into production volume.

![D66: Flow diagram, not to scale. Five boxes run left to right, each wider than the last: 5 boards, prototypes; 20 boards, a pilot build; 200 boards, with first articles first; 1,000 boards, the first large batch; and 2,000 or more boards, full volume. Inside the full-volume box, small squares in groups of three show batches released as whole panels.](images/production-ramp.svg)

*D66 is not to scale.
Each step builds about ten times as many boards as the one before, up to the full volume.
First articles come at the start of the first step after anything has changed.
Full volume is released in batches of whole panels, such as 27 boards from three 9-up panels.*

**Applies to:** General practice, whenever volume rises sharply.

**Sources:** ["How Small Manufacturers Manage Large Volume Orders"](https://www.buzzsprout.com/1066066/episodes/12586426-how-small-manufacturers-manage-large-volume-orders) (Apr 2023), [32:00](https://www.buzzsprout.com/1066066/episodes/12586426?t=1920)–33:00 and [36:00](https://www.buzzsprout.com/1066066/episodes/12586426?t=2160)–40:00; ["Smarter Test Plans for Inevitable Failures w/ Blue Clover CEO & Co-founder, Pete Staples"](https://www.buzzsprout.com/1066066/episodes/17955982-smarter-test-plans-for-inevitable-failures-w-blue-clover-ceo-co-founder-pete-staples) (Oct 2025), [47:00](https://www.buzzsprout.com/1066066/episodes/17955982?t=2820)–48:00; ["How Blue Robotics is enabling the next generation of ocean exploration robots w/ Rustom Jehangir"](https://www.buzzsprout.com/1066066/episodes/8139597-how-blue-robotics-is-enabling-the-next-generation-of-ocean-exploration-robots-w-rustom-jehangir) (Mar 2021), [28:00](https://www.buzzsprout.com/1066066/episodes/8139597?t=1680)–30:00; ["Soft Skills of Engineering w/ Being an Engineer Host, Aaron Moncur"](https://www.buzzsprout.com/1066066/episodes/12593633-soft-skills-of-engineering-w-being-an-engineer-host-aaron-moncur) (Apr 2023), [52:00](https://www.buzzsprout.com/1066066/episodes/12593633?t=3120)–54:00; ["All about parts purchasing - part 1"](https://www.buzzsprout.com/1066066/episodes/4540040-all-about-parts-purchasing-part-1) (Jul 2020), [59:00](https://www.buzzsprout.com/1066066/episodes/4540040?t=3540).

*Last reviewed: 2026-11-12*

---

## PCB-DFA-123: For large orders, release boards in batches matched to the panel, and agree who holds the parts and the risk

**Recommendation:** For a large annual volume, agree a schedule of batch releases with your manufacturer, rather than one delivery of the whole quantity.
Make each batch a whole number of panels.
Agree which parts the manufacturer buys up front and which are held by a distributor and released batch by batch (PCB-DFA-098).
Before a very large order, agree in writing who carries which risks.
That includes insurance for parts held in the factory, and who pays if boards fail in the field months later.

**Why:** A batch schedule matches deliveries to how the product sells, and keeps less money tied up in parts and finished boards.
A batch of whole panels uses every board the machines build.
The costly part of a changeover is setting up the surface-mount machines, so batches are sized to spread that set-up over enough boards.
On a large order, most of the money is in parts, and someone has to hold that stock and its risk until the boards are built.

**Typical values:** In one example, a 9-up panel of 3 by 3 boards meant batches of 27 boards.
Each surface-mount feeder costs about $1,000 or more (2023 figure), which is why surface-mount set-up dominates changeover cost.
In one example of a $200,000 order, about $150,000 was parts and about $50,000 was labor.
Orders of about $100,000 often run without a formal contract.
Orders of $400,000 to $500,000 usually need one.

**What goes wrong if you don't:** Cash tied up in a year of stock, partial panels that waste boards, or a dispute about who pays after a fire, a flood or a field failure.

**Example:** One product has been built at about 2,000 boards a year for 20 years.
The customer never takes all 2,000 at once.
For years it called them off in batches of 27, a whole number of its 9-up panels, every few days.

**Applies to:** Production volumes; contracts and insurance vary by manufacturer and country.

**Sources:** ["How Small Manufacturers Manage Large Volume Orders"](https://www.buzzsprout.com/1066066/episodes/12586426-how-small-manufacturers-manage-large-volume-orders) (Apr 2023), [05:00](https://www.buzzsprout.com/1066066/episodes/12586426?t=300)–08:00, [11:00](https://www.buzzsprout.com/1066066/episodes/12586426?t=660)–13:00, [19:00](https://www.buzzsprout.com/1066066/episodes/12586426?t=1140)–22:00 and [27:00](https://www.buzzsprout.com/1066066/episodes/12586426?t=1620)–29:00.

*Last reviewed: 2026-11-12*

---

## Related pages
- [First articles](../06-test-and-programming/07-first-articles.md) (PCB-DFA-107 and 108)
- [Sourcing](../04-components-and-materials/04-sourcing.md) (PCB-DFA-098, sharing volumes)
- [Choosing parts](../04-components-and-materials/01-choosing-parts.md) (PCB-DFA-083 and 085)
- [Why boards are built in panels](../02-the-panel/01-why-panels.md)
- [What drives cost and lead time](01-cost-and-lead-time.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

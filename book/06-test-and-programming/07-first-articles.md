# First articles

A first article is the first panel of a production run.
It's built and checked before the rest of the run goes ahead.
It proves that the parts, the bare boards, the stencil and the machine programs all come together correctly on this assembler's line, before hundreds or thousands of boards are built.
It isn't a prototype, because it checks the build, not the design.

## PCB-DFA-107: Use first articles to check a proven design before a big run, not as a prototype

**Recommendation:** Ask for first articles when a design that already works is about to be built in quantity.
That includes scaling up from prototypes, moving a product to a new assembler, and making a small change, such as adding one resistor, before a large or expensive run.
For a new design or a big change, build another round of prototypes instead.
Expect at least one full panel of first articles, and a set-up charge for them.
After that, expect the volume to ramp up in steps, not jump straight to full volume.

**Why:** First articles find build problems, such as a wrong reel, a part fitted backwards, a stencil that clogs, or a footprint the assembler has to work around.
They can't tell you whether the design works, because the production run follows straight after.
A design problem found at that point means boards are already built.
Setting up the line always builds at least one full panel, so "one first article" usually means one panel's worth.
Later batches go faster as the assembler learns the board, so the first few hundred boards of a big order are the slowest.

**Typical values:** At least one panel, which is often around 200 × 150 mm.
A typical ramp-up is 20 boards, then 200, then 1,000 or more.

**What goes wrong if you don't:** A whole run gets built with the same mistake.
Or a "first article" order for an untested design turns into an expensive prototype run.

**Example:** A customer with a well-proven product placed a $200,000 order for 3,000 boards with several changes.
The first articles showed that a resistor the customer expected was missing, and that the stencil clogged.
The assembler ordered a new stencil and improved the process before building the rest.

**Applies to:** General practice.
An assembler may refuse first articles for an unproven design and ask for prototypes first.

**Sources:** [“When to request first articles”](https://www.buzzsprout.com/1066066/episodes/9645335-when-to-request-first-articles) (Dec 2021), [04:00](https://www.buzzsprout.com/1066066/episodes/9645335?t=240)–07:00, [13:00](https://www.buzzsprout.com/1066066/episodes/9645335?t=780), [16:00](https://www.buzzsprout.com/1066066/episodes/9645335?t=960)–19:00 and [28:00](https://www.buzzsprout.com/1066066/episodes/9645335?t=1680)–30:00; [“How Small Manufacturers Manage Large Volume Orders”](https://www.buzzsprout.com/1066066/episodes/12586426-how-small-manufacturers-manage-large-volume-orders) (Apr 2023), [32:00](https://www.buzzsprout.com/1066066/episodes/12586426?t=1920)–40:00.

*Last reviewed: 2026-11-10*

---

## PCB-DFA-108: Check first articles against a known-good board, and don't expect the line to wait while you do

**Recommendation:** Test first articles the way you test your own boards.
Compare them side by side with a known-good working board, not only with the drawings.
Plan to have them shipped to you and test them at your own site.
Don't expect the assembler to keep its line set up and waiting while you test at their factory.
If you find a simple problem, send clear photos and instructions for the fix.
You often won't need another full round of first articles.
For a first build, send a photo of a working prototype.
This matters most for parts that need a particular orientation, height or lead bend.

**Why:** If the silkscreen or the part's own marking is unclear, a part fitted backwards can seem to match both and pass the assembler's inspection.
Only a working board shows the truth.
An assembly line is set up for one job at a time.
Every hour it waits for a decision is an hour of expensive equipment and people standing idle.
A photo of the fix gets it right on the rest of the run without a second set-up.

**What goes wrong if you don't:** A mistake that looked right to everyone gets built into the whole run.
Or a line is held up for hours waiting for an answer.

**Example:** A customer moved a mature product to a new assembler and asked for first articles.
A voltage regulator was fitted turned 180°, because both the part's marking and the board's marking seemed to agree with that way.
The customer thought it looked right too.
It was caught only when the customer compared it with known-good boards at its own site.
About 300 boards were then built correctly.
Each board had two of these regulators, so about 600 would otherwise have needed rework.
The same assembler has tried four or five times to let a customer test the first board at the factory while the line waited.
It went badly every time.
Once, a restart agreed for 2:30 pm didn't happen until 8 pm.

**Applies to:** General practice.

**Sources:** [“When to request first articles”](https://www.buzzsprout.com/1066066/episodes/9645335-when-to-request-first-articles) (Dec 2021), [10:00](https://www.buzzsprout.com/1066066/episodes/9645335?t=600)–12:00 and [19:00](https://www.buzzsprout.com/1066066/episodes/9645335?t=1140)–23:00; [“The PCB assembly inspection process”](https://www.buzzsprout.com/1066066/episodes/5713750-the-pcb-assembly-inspection-process) (Oct 2020), [51:00](https://www.buzzsprout.com/1066066/episodes/5713750?t=3060)–52:00.

*Last reviewed: 2026-11-10*

---

## Related pages
- [Why boards are built in panels](../02-the-panel/01-why-panels.md) (a first article is at least one panel)
- [Footprints](../01-design-package/04-footprints.md) (PCB-DFA-034, pin-1 marks)
- [Inspection](../05-assembly/04-inspection.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

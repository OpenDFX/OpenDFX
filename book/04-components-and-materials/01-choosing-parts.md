# Choosing parts that can be bought and built

Every part on your schematic has to be bought, delivered and fitted, possibly for years.
A part that's perfect on paper but sold by one maker, stocked by one distributor or near the end of its life can hold up a whole build.
This page is about choosing parts with the supply chain and the factory in mind.
Package size, footprints and reflow ratings are covered in Part 5 and Part 1.4; links are at the end.

## PCB-DFA-083: Choose parts that are active, widely stocked, and made by more than one maker where you can

**Recommendation:** When you choose a part, check three things as well as its electrical fit:
- its lifecycle status is active (not "not recommended for new designs", last-time-buy or obsolete);
- several authorized distributors stock it in quantity;
- for anything but a truly special part, an equivalent exists from another maker.

Check these when you choose the part, not only when you release the BOM ([PCB-DFA-070](../01-design-package/03-bom.md)).
Before moving from prototype to production, look again at any part that was easy to find in tens but may not be in thousands.

**Why:** Parts stocked widely, by more than one maker, keep shipping when one source runs short.
A specialty part can carry a lead time of weeks where a mainstream equivalent ships the same day.
Parts reused from an old design, or an old library, may already be at the end of their life when the board reaches manufacturing.
Distributors sell in small quantities; buying straight from a maker often means minimum orders of thousands.

**Typical values:** Minimum: active, and in stock at two or more authorized distributors.
Recommended: also available from a second maker, or listed in a common-parts library chosen for deep supply.

**What goes wrong if you don't:** A build held for weeks waiting for one part, or a redesign when it can't be bought at all.

**Example:** For a 200-unit build, an assembler found that only about 204 of one pressure sensor existed in stock anywhere.
A simple 4-pin, 0.1 in header from a specialty maker had a two-week lead time, while equivalents from other makers shipped at once.

**Applies to:** General practice.

**Sources:** [“All about parts purchasing - part 1”](https://www.buzzsprout.com/1066066/episodes/4540040-all-about-parts-purchasing-part-1) (Jul 2020), [41:00](https://www.buzzsprout.com/1066066/episodes/4540040?t=2460) and [57:00](https://www.buzzsprout.com/1066066/episodes/4540040?t=3420)–59:00; [“Discussing the Global Electronics Parts Shortage w/ Digi-Key”](https://www.buzzsprout.com/1066066/episodes/8574130-discussing-the-global-electronics-parts-shortage-w-digi-key) (May 2021), [42:00](https://www.buzzsprout.com/1066066/episodes/8574130?t=2520); [“The importance of having different perspectives in engineering w/ Eli Hughes of Tzero Labs (Part 2)”](https://www.buzzsprout.com/1066066/episodes/7118017-the-importance-of-having-different-perspectives-in-engineering-w-eli-hughes-of-tzero-labs-part-2) (Jan 2021), [48:00](https://www.buzzsprout.com/1066066/episodes/7118017?t=2880)–51:00; [“The role of electronic components distributors w/ Digi-key”](https://www.buzzsprout.com/1066066/episodes/8655719-the-role-of-electronic-components-distributors-w-digi-key) (Jun 2021), [14:00](https://www.buzzsprout.com/1066066/episodes/8655719?t=840).

*Last reviewed: 2026-11-09*

---

## PCB-DFA-084: For parts at risk of shortage, give the board a way to take an alternate

**Recommendation:** For a part that's scarce, single-source or has been short before, plan an alternate into the layout:
1. First choice: an alternate in the same package and pinout, listed on the BOM ([PCB-DFA-069](../01-design-package/03-bom.md)), so the board doesn't change at all.
2. If the alternate comes in a different package: use an overlapping footprint only where the part maker publishes one, and name the package you want fitted on the BOM.
3. If the two can't overlap: draw both footprints side by side and mark the one not fitted as DNP (do not place).

**Why:** A board that already accepts a second part can be built from whatever is in stock, without a new revision.
Some makers sell the same chip in packages of different sizes with the same pinout, and publish a layout that takes either: a tiny leadless package placed inside the footprint of a leaded one, with each pin joined to its partner by a short trace, as in D57.
An overlapping footprint leaves pads unused whichever package is fitted, so the assembler needs to know which package to cut the stencil for.
Drawing your own overlap risks pads too close together, the wrong pitch, and bridges.

![D57: Drawn to scale, plan views. Left: a SOT-23-6 footprint with six pads 0.6 by 1.1 mm on a 0.95 mm pitch, in two rows 2.5 mm apart; in the space between the rows sit the six pads of a 1.0 by 0.8 mm leadless package, each joined to the SOT-23 pad beside it by a short trace under the mask. Right: a SOT-23-6 footprint labeled U1 and an SC-70-6 footprint labeled U2 side by side; the BOM fits one and marks the other DNP.](images/dual-footprint.svg)

*D57 is drawn to scale, with example pad sizes.
On the left, either package fits one footprint, the way some part makers publish it; on the right, two footprints share the same nets and only one is fitted.*


**What goes wrong if you don't:** A board respin, or a long wait, when the one part it accepts runs out.

**Example:** One designer used an op-amp sold in both SC-70 and SOT-23 packages, and set the board up to take either, so the assembler could fit whichever was in stock.

**Applies to:** General practice; most useful for parts with a history of shortages.

**Sources:** [“How Joel Murphy went from visual artist to electronics design engineer”](https://www.buzzsprout.com/1066066/episodes/5963659-how-joel-murphy-went-from-visual-artist-to-electronics-design-engineer) (Oct 2020), [52:00](https://www.buzzsprout.com/1066066/episodes/5963659?t=3120)–53:00; [“When to use through hole vs surface mount components”](https://www.buzzsprout.com/1066066/episodes/8803410-when-to-use-through-hole-vs-surface-mount-components) (Jul 2021), [39:00](https://www.buzzsprout.com/1066066/episodes/8803410?t=2340)–42:00; a chip maker's application note on dual-footprint layouts (leaded and leadless packages, 2023); Chris Denney (author).

*Last reviewed: 2026-11-09*

---

## PCB-DFA-085: In production, use the original maker's part on reel, not hobby modules or reseller strips

**Recommendation:** For anything you'll build in quantity, find the original maker and part number behind a hobby-market product, and buy that part on a reel.
Avoid breakout boards, individually bagged modules, and parts sold in short strips by hobby resellers.
If a module has no alternative, buy a reel of it yourself and consign it ([PCB-DFA-100](05-consignment-and-spares.md)).

**Why:** Hobby resellers repackage parts in small bags or strips of ten, which can't be fed to a machine without loading every strip by hand.
The original maker's part comes on continuous tape and costs far less in quantity.
Hobby products are often hard for a business to buy through normal channels, or have no published maker at all.

**Typical values:** Loading a strip of ten takes 20–60 seconds; a reel of 1,000 or more runs without stopping.

**What goes wrong if you don't:** Hours of extra set-up on a large order, a handling charge for every strip, and parts that cost several times more than they need to.

**Example:** A customer specified addressable RGB LEDs sold in strips of ten and needed thousands.
The assembler traced the original part, found it on reels of 1,000, and the reel worked out roughly 70% cheaper after shipping.

**Applies to:** General practice; matters most above a few dozen boards.

**Sources:** [“All about parts purchasing - part 1”](https://www.buzzsprout.com/1066066/episodes/4540040-all-about-parts-purchasing-part-1) (Jul 2020), [47:00](https://www.buzzsprout.com/1066066/episodes/4540040?t=2820)–50:00 and [50:00](https://www.buzzsprout.com/1066066/episodes/4540040?t=3000)–51:00; [“The RGB LED Dilemma in Manufacturing”](https://www.buzzsprout.com/1066066/episodes/15667846-the-rgb-led-dilemma-in-manufacturing) (Sep 2024), [04:00](https://www.buzzsprout.com/1066066/episodes/15667846?t=240)–13:00 and [16:00](https://www.buzzsprout.com/1066066/episodes/15667846?t=960).

*Last reviewed: 2026-11-09*

---

## PCB-DFA-086: Check that board-mount connectors suit your board thickness and the product

**Recommendation:** For every connector and mechanical part that grips or passes through the board, check its datasheet for the board thickness it's made for, and choose the version that matches your stack-up.
Check too that the part is rated for the job: current, mating cycles, temperature, and any approval the product needs (medical, automotive, life-safety).

**Why:** Mid-mount connectors, through-hole tabs, press-fit pins and snap-in parts are designed around one board thickness, often 1.6 mm, sometimes 0.8 mm or 1.0 mm.
On a thicker board the tabs don't come through far enough to solder; on a thinner one the part sits at the wrong height or rocks.
Two parts that look identical can carry very different ratings.

**What goes wrong if you don't:** Connectors that can't be soldered properly or sit crooked, found at first assembly; or a product that fails its approval because one part wasn't rated for it.

**Applies to:** General practice.

**Sources:** [“Benefits of intrusive soldering”](https://www.buzzsprout.com/1066066/episodes/10791130-benefits-of-intrusive-soldering) (Jun 2022), [26:00](https://www.buzzsprout.com/1066066/episodes/10791130?t=1560); [“How Joel Murphy went from visual artist to electronics design engineer”](https://www.buzzsprout.com/1066066/episodes/5963659-how-joel-murphy-went-from-visual-artist-to-electronics-design-engineer) (Oct 2020), [48:00](https://www.buzzsprout.com/1066066/episodes/5963659?t=2880)–52:00; connector makers' datasheets (mid-mount USB-C receptacles sold per board thickness).

*Last reviewed: 2026-11-09*

---

## PCB-DFA-087: For LEDs and other parts sold in bins, choose the bin, or test each bin and say how to handle it

**Recommendation:** Where brightness or color matters, order the LED with a named bin in its part number, if the maker offers one.
If not, get samples from several bins, test them in your circuit, and give the assembler what to do for each bin (for example, which current-limiting resistor to fit).
Don't bother for indicator LEDs where brightness doesn't matter.

**Why:** LEDs are sorted after manufacture into bins of brightness and color, and each reel carries a bin code.
Two reels of the same part number can look noticeably different side by side.

**What goes wrong if you don't:** Products whose LEDs don't match each other, or vary from one batch to the next.

**Example:** A designer whose product depended on LED brightness bought samples of each bin, found the right resistor for each on a breadboard, and gave the assembler a table of bin to resistor.

**Applies to:** LEDs and other parts sold in bins, where appearance or behavior depends on them.

**Sources:** [“How Joel Murphy went from visual artist to electronics design engineer”](https://www.buzzsprout.com/1066066/episodes/5963659-how-joel-murphy-went-from-visual-artist-to-electronics-design-engineer) (Oct 2020), [53:00](https://www.buzzsprout.com/1066066/episodes/5963659?t=3180)–55:00; LED makers' binning and labeling documents.

*Last reviewed: 2026-11-09*

---

## PCB-DFA-088: Don't name a brand of solder, flux or other process material unless the product needs it

**Recommendation:** Specify process materials by type and standard (for example, "no-clean, lead-free, SAC305, per J-STD-004 and J-STD-006"), not by brand and product name, unless a qualification or customer requirement forces a particular one.
If you must name one, list an approved alternative too.

**Why:** Named products are discontinued, reformulated or go out of stock, often after a company is bought.
The assembler then can't build to your drawing without your sign-off, and a qualified product may need requalifying.

**What goes wrong if you don't:** A build held while you approve a substitute, or the cost of requalifying a process.

**Example:** A government drawing named one flux-core solder wire, which was later discontinued; separately, a favored solder paste disappeared after its maker was acquired.

**Applies to:** General practice; products with a qualified process may have to name a material.

**Sources:** [“The nitty gritty details on solder”](https://www.buzzsprout.com/1066066/episodes/11129008-the-nitty-gritty-details-on-solder) (Aug 2022), [42:00](https://www.buzzsprout.com/1066066/episodes/11129008?t=2520)–43:00.

*Last reviewed: 2026-11-09*

---

## Related pages
- [The BOM](../01-design-package/03-bom.md)
- [Footprints and the component library](../01-design-package/04-footprints.md)
- [Component placement](../05-assembly/02-component-placement.md) (package size: PCB-DFA-021 and 022)
- [Reflow soldering](../05-assembly/03-reflow-soldering.md) (reflow ratings: PCB-DFA-026)
- [Packaging: reels, cut tape, tubes, trays](02-packaging.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

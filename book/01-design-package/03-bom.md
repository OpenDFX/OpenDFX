# The BOM

The bill of materials (BOM) lists every part on the board: what it is, how many, and where it goes.
The assembler buys parts from it, programs machines from it alongside the XY file, and inspects against it.
It's also a contract: a wrong value in the BOM gets built exactly as written.

A good BOM is one line per unique part, with enough information that a buyer who has never seen your design can order exactly the right thing, or a safe substitute.

## PCB-DFA-068: Give every BOM line the designators, quantity, maker and full part number

**Recommendation:** Give each line of the BOM at least:
- the reference designators it covers (matching the XY file and the legend exactly);
- the quantity per board;
- the manufacturer and the manufacturer's full part number, including any suffix for packaging, tolerance or termination;
- a short description (value, tolerance, voltage, package).

Useful extras: a line number (handy for listing alternates) and your own part number.

Send it as CSV or a spreadsheet.
Use the part number exactly as the maker publishes it, the same in every document, and don't add commas or other characters to it.

**Why:** The assembler matches each line to the XY file by its designators, buys by the maker's part number, and checks what arrives against it.
A distributor's own stock number, or a description alone, leaves the buyer to guess.
One character in a part number can mean a different packaging (R for reel, T for tube), or a different part entirely.
CSV files use commas to separate fields, so a comma inside a part number splits it into two.

**What goes wrong if you don't:** Questions before parts can be bought, and parts received that don't match the BOM by one character, each of which has to be confirmed before it can be used.

**Example:** Some part makers do use commas in their part numbers; one assembler had to write software to quote every part number so that its files wouldn't break.

**Applies to:** General practice.

**Sources:** [“Showstoppers that delay PCB assembly w/ Production Manager, Rob OConnell”](https://www.buzzsprout.com/1066066/episodes/9741439-showstoppers-that-delay-pcb-assembly-w-production-manager-rob-oconnell) (Dec 2021), [43:00](https://www.buzzsprout.com/1066066/episodes/9741439?t=2580)–46:00; [“How to Send Consigned Material to Your CM”](https://www.buzzsprout.com/1066066/episodes/10182930-how-to-send-consigned-material-to-your-cm) (Mar 2022), [24:00](https://www.buzzsprout.com/1066066/episodes/10182930?t=1440)–26:00; two large online assemblers' published BOM requirements (checked Nov 2026).

*Last reviewed: 2026-11-07*

---

## PCB-DFA-069: Say which lines are locked to one part, and why; list alternates for the rest

**Recommendation:** Mark each BOM line as either "this exact part only" or "equivalents allowed".
For a locked line, say which parameter makes it critical (for example, low ESR, a particular tempco, a qualified part).
For the others, list one or more approved alternate part numbers, especially for anything that's scarce, single-source, or not a simple resistor or capacitor (LEDs, diodes, connectors).

**Why:** When a part is out of stock, the assembler's buyers need to know whether they may substitute, and what a good substitute must match.
Many lines are more flexible than designers expect, and an alternate you've already approved can be bought at once.
A locked line with a reason tells them what to protect, and stops them suggesting a substitute you'll have to refuse.

**What goes wrong if you don't:** Emails back and forth, a job held waiting for a part, or a substitute chosen by someone who doesn't know which parameter mattered.

**Applies to:** General practice.

**Sources:** [“All about parts purchasing - part 1”](https://www.buzzsprout.com/1066066/episodes/4540040-all-about-parts-purchasing-part-1) (Jul 2020), [42:00](https://www.buzzsprout.com/1066066/episodes/4540040?t=2520)–44:00; [“All the Tricks and Gotchas in Surface Mount Assembly (Repost from the Coriolis Effect)”](https://www.buzzsprout.com/1066066/episodes/11006453-all-the-tricks-and-gotchas-in-surface-mount-assembly-repost-from-the-coriolis-effect) (Jul 2022), [17:00](https://www.buzzsprout.com/1066066/episodes/11006453?t=1020)–19:00; [“The Benefits of Asynchronous Design Review for Engineers & Manufacturers w/ AllSpice.io”](https://www.buzzsprout.com/1066066/episodes/11886751-the-benefits-of-asynchronous-design-review-for-engineers-manufacturers-w-allspice-io) (Dec 2022), [46:00](https://www.buzzsprout.com/1066066/episodes/11886751?t=2760)–52:00.

*Last reviewed: 2026-11-07*

---

## PCB-DFA-070: Check every value and part number before release, and check each part is still made

**Recommendation:** Before you release a BOM, check each value and part number character by character against what you meant, and check every part's lifecycle status and stock with a distributor.
Replace parts that are obsolete or not recommended for new designs.

**Why:** Part numbers are long, and one character can change the value, the tolerance, or how the part is mounted.
Libraries age: a BOM generated today from an old library can be full of parts that stopped being made years ago.

**What goes wrong if you don't:** Boards built exactly to a wrong BOM, which don't work and have to be reworked; or a quote that can't be completed until obsolete parts are replaced.

**Example:** A customer's boards wouldn't power up; the BOM had the wrong value for 20 to 30 ceramic capacitors, one zero out.
A one-character difference in another capacitor part number selects a version made for epoxy mounting instead of soldering; the two look identical and have the same electrical ratings.
One assembler received a freshly generated BOM with 16 obsolete part numbers on it.

**Applies to:** General practice.

**Sources:** [“The PCB assembly inspection process”](https://www.buzzsprout.com/1066066/episodes/5713750-the-pcb-assembly-inspection-process) (Oct 2020), [29:00](https://www.buzzsprout.com/1066066/episodes/5713750?t=1740)–30:00; [“Alternative Component Mounting”](https://www.buzzsprout.com/1066066/episodes/10030215-alternative-component-mounting) (Feb 2022), [11:00](https://www.buzzsprout.com/1066066/episodes/10030215?t=660)–15:00; [“All about parts purchasing - part 1”](https://www.buzzsprout.com/1066066/episodes/4540040-all-about-parts-purchasing-part-1) (Jul 2020), [44:00](https://www.buzzsprout.com/1066066/episodes/4540040?t=2640)–46:00.

*Last reviewed: 2026-11-07*

---

## PCB-DFA-071: Mark do-not-place and customer-supplied lines clearly

**Recommendation:** Give every location the BOM leaves empty its own line or column marked DNP (do not place), rather than deleting it.
Mark parts you'll supply yourself as CONSIGNED, and confirm with the assembler that they'll use your parts and not buy their own.
If you'll fit the through-hole parts yourself to save cost on a prototype, mark those lines DNP too.

**Why:** A location missing from the BOM looks like a mistake; one marked DNP is a decision.
Assemblers buy from the BOM unless told otherwise, so a consigned part that isn't marked may be bought again, and the wrong one fitted.
Through-hole parts are slow and costly to fit at low volumes, and leaving them off is a common, easy saving.

**What goes wrong if you don't:** A question for every empty footprint, or parts fitted that you meant to leave off; a consigned, pre-programmed chip replaced with a blank one.

**Example:** A designer consigned pre-programmed bootloader chips, and the assembler bought and fitted blank ones instead; the boards had to be shipped back and forth to put it right.

**Applies to:** General practice.

**Sources:** [“How Joel Murphy went from visual artist to electronics design engineer”](https://www.buzzsprout.com/1066066/episodes/5963659-how-joel-murphy-went-from-visual-artist-to-electronics-design-engineer) (Oct 2020), [24:00](https://www.buzzsprout.com/1066066/episodes/5963659?t=1440)–25:00; [“All the Tricks and Gotchas in Surface Mount Assembly (Repost from the Coriolis Effect)”](https://www.buzzsprout.com/1066066/episodes/11006453-all-the-tricks-and-gotchas-in-surface-mount-assembly-repost-from-the-coriolis-effect) (Jul 2022), [30:00](https://www.buzzsprout.com/1066066/episodes/11006453?t=1800)–31:00; Chris Denney (author).

*Last reviewed: 2026-11-07*

---

## PCB-DFA-072: For small builds, keep the number of unique BOM lines down

**Recommendation:** When you'll build only a few boards at a time, use as few different part numbers as you can: one resistor value where several would do, the same capacitor for all decoupling, the same connector family throughout.

**Why:** Every unique part has to be loaded onto a feeder and set up on the machine, however many boards you build.
On a run of a few boards, that set-up time is most of the cost.

**Typical values:** About 3 to 5 minutes to load each feeder.
A 100-line BOM spread over 5 boards carries the set-up cost of all 100 feeders.

**What goes wrong if you don't:** Prototype and small-batch prices that are much higher than they need to be.

**Applies to:** General practice; matters most for prototypes and small batches.

**Sources:** [“What factors influence PCB quotes w/ Brett Babilonia”](https://www.buzzsprout.com/1066066/episodes/14580855-what-factors-influence-pcb-quotes-w-brett-babilonia) (Feb 2024), [19:00](https://www.buzzsprout.com/1066066/episodes/14580855?t=1140)–21:00.

*Last reviewed: 2026-11-07*

---

## Related pages
- [Assembly data](02-assembly-data.md)
- [Fabrication data](01-fabrication-data.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

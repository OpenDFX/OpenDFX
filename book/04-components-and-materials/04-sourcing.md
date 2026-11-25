# Sourcing, counterfeits and obsolescence

Where parts come from matters as much as which parts they are.
Parts bought through the maker's own sales channels can be traced back to the factory; parts that have changed hands several times can't, and that's where counterfeits get in.
Lead times also move with the market: they stretched from weeks to most of a year during the 2021–22 shortage, then fell back.
This page is about buying parts safely and planning for the ones that are hard to get.

## PCB-DFA-095: Buy parts only from authorized distributors or the maker

**Recommendation:** Buy from the part maker or its authorized (franchised) distributors.
Don't buy from unfamiliar websites, auction sites or marketplaces, however convincing they look.
If your assembler buys for you, expect them to do the same, and to tell you before using any other source.

**Why:** Authorized distributors buy straight from the maker, so the parts are genuine and traceable.
Counterfeit parts can pass a visual check and still be wrong inside: remarked, used, or made from the wrong materials.

**What goes wrong if you don't:** Parts that don't work, melt in soldering or won't take solder, found after they're on the board.

**Example:** A customer nearly paid a convincing fake distributor website for a hard-to-find part.
Terminal blocks that looked right melted into black puddles in selective soldering, or wouldn't wet at all.
One designer received 2,000 assembled units with a counterfeit LED that didn't work, and spent a day and a half reworking them by hand.

**Applies to:** General practice.

**Sources:** [“All about parts purchasing - part 1”](https://www.buzzsprout.com/1066066/episodes/4540040-all-about-parts-purchasing-part-1) (Jul 2020), [51:00](https://www.buzzsprout.com/1066066/episodes/4540040?t=3060)–56:00; [“How Joel Murphy went from visual artist to electronics design engineer”](https://www.buzzsprout.com/1066066/episodes/5963659-how-joel-murphy-went-from-visual-artist-to-electronics-design-engineer) (Oct 2020), [22:00](https://www.buzzsprout.com/1066066/episodes/5963659?t=1320)–23:00; [“Catch up with Chris”](https://www.buzzsprout.com/1066066/episodes/13639009-catch-up-with-chris) (Sep 2023), [35:00](https://www.buzzsprout.com/1066066/episodes/13639009?t=2100)–36:00.

*Last reviewed: 2026-11-09*

---

## PCB-DFA-096: If you must buy from a broker or an unfamiliar source, ask for traceability, have the parts inspected, and try them on a small build first

**Recommendation:** When a part can only be found outside authorized channels:
- ask the seller for proof the parts came from the maker (an invoice, delivery note or goods-received record tied to the lot);
- ask whether they hold the stock themselves or are offering someone else's;
- have the parts inspected, and tested if they're costly or critical;
- build a few boards with them and check they work before committing the whole order.

**Why:** Brokers trade excess stock, which is often genuine, but every change of hands without records adds risk.
Some brokers sell only surplus bought directly from large manufacturers; others search the open market.
"Available stock" may be parts someone else holds, with a delivery time the broker doesn't control.
Inspection under a microscope can catch sanded and remarked markings or wrong plating that paperwork won't.
Two datasheets for the "same" part number can describe different parts.

**Typical values:** Inspection at 50× and 200× magnification, compared against known-good parts.
One broker spends about 40 minutes inspecting each part number.

**What goes wrong if you don't:** A full production run built with parts that don't match, or don't work.

**Example:** An assembler sourcing addressable LEDs on reel from an unfamiliar distributor found two datasheets for the same part number, in different languages and naming different makers; it got the customer's permission and tested a small build first.

**Applies to:** General practice.
Aerospace and defense work follows SAE AS5553 (buyers) and AS6081 (distributors), which require traceability, inspection and notice before any broker purchase.

**Sources:** [“How Component Sense helps components fulfill their destiny w/ Kenny McGee”](https://www.buzzsprout.com/1066066/episodes/15794357-how-component-sense-helps-components-fulfill-their-destiny-w-kenny-mcgee) (Sep 2024), [28:29](https://www.buzzsprout.com/1066066/episodes/15794357?t=1709)–29:23 and [39:49](https://www.buzzsprout.com/1066066/episodes/15794357?t=2389)–40:17; [“Navigating the Environmental Impact of Electronics w/ Component Sense Founder, Kenny McGee”](https://www.buzzsprout.com/1066066/episodes/15877892-navigating-the-environmental-impact-of-electronics-w-component-sense-founder-kenny-mcgee) (Oct 2024), [13:00](https://www.buzzsprout.com/1066066/episodes/15877892?t=780)–15:00; [“The RGB LED Dilemma in Manufacturing”](https://www.buzzsprout.com/1066066/episodes/15667846-the-rgb-led-dilemma-in-manufacturing) (Sep 2024), [09:00](https://www.buzzsprout.com/1066066/episodes/15667846?t=540)–10:00 and [14:00](https://www.buzzsprout.com/1066066/episodes/15667846?t=840)–16:00; SAE AS5553 and AS6081.

*Last reviewed: 2026-11-09*

---

## PCB-DFA-097: Find your long-lead and single-source parts early and buy them ahead, without hoarding

**Recommendation:** Before production, go through the BOM and find the parts with the longest lead times, a single source, or a history of shortages.
Buy those ahead, enough for your next several builds if you can afford it, or arrange for a distributor or your assembler to hold them for you ([PCB-DFA-098](#pcb-dfa-098-tell-your-assembler-or-distributor-your-expected-volumes)).
If you hear a part is going out of stock, tell your assembler the same day.
In a shortage, don't over-order to win a bigger share of a supplier's allocation.

**Why:** Parts, not boards, set the lead time for most production orders.
A large order may only find part of its quantity in stock, with the rest weeks away.
In a shortage, stock disappears in hours, and buying early may be the only way to get it.
But orders placed in a shortage are often non-cancellable and non-returnable, and when the market turns, buyers who over-ordered are left holding years of stock.

**Typical values:** These move with the market; check them when you plan.
Before 2021, typical lead times were about 8–12 weeks; during the 2021–22 shortage, 18–40 weeks was common, and a quoted lead time over about 50 weeks meant the part was on allocation.
Suppliers in China shut for the Lunar New Year holiday (late January or February), and lead times take one to two months to recover; order in early December what you'll need through March.

**What goes wrong if you don't:** A build stopped for months by one part, or, the other way, cash tied up in stock you'll never use.

**Example:** During the shortage, customers who hadn't planned found 26-week lead times and couldn't build for about 20 weeks.
A buyer needing 1,000 of a part found 800 in stock and waited 6–10 weeks for the rest.

**Applies to:** General practice; numbers are date-dependent.

**Sources:** [“Our top suggestions for customers w/ CircuitHub Account Manager, John Jacquinet”](https://www.buzzsprout.com/1066066/episodes/8884604-our-top-suggestions-for-customers-w-circuithub-account-manager-john-jacquinet) (Jul 2021), [23:00](https://www.buzzsprout.com/1066066/episodes/8884604?t=1380); [“All about parts purchasing - part 2”](https://www.buzzsprout.com/1066066/episodes/4704659-all-about-parts-purchasing-part-2) (Jul 2020), [17:00](https://www.buzzsprout.com/1066066/episodes/4704659?t=1020)–19:00 and [28:00](https://www.buzzsprout.com/1066066/episodes/4704659?t=1680)–30:00; [“Discussing the Global Electronics Parts Shortage w/ Digi-Key”](https://www.buzzsprout.com/1066066/episodes/8574130-discussing-the-global-electronics-parts-shortage-w-digi-key) (May 2021), [31:00](https://www.buzzsprout.com/1066066/episodes/8574130?t=1860); [“How Component Sense helps components fulfill their destiny w/ Kenny McGee”](https://www.buzzsprout.com/1066066/episodes/15794357-how-component-sense-helps-components-fulfill-their-destiny-w-kenny-mcgee) (Sep 2024), [12:16](https://www.buzzsprout.com/1066066/episodes/15794357?t=736)–17:02; [“How Chinese New Year Impacts Manufacturing”](https://www.buzzsprout.com/1066066/episodes/9863955-how-chinese-new-year-impacts-manufacturing) (Jan 2022), [12:00](https://www.buzzsprout.com/1066066/episodes/9863955?t=720)–13:00 and [31:00](https://www.buzzsprout.com/1066066/episodes/9863955?t=1860)–33:00.

*Last reviewed: 2026-11-09*

---

## PCB-DFA-098: Tell your assembler or distributor your expected volumes

**Recommendation:** As soon as you know them, share your expected annual volumes and build schedule with your assembler, or with a distributor directly.
For production quantities, ask for quoted prices rather than catalog prices, and for expensive parts, ask whether they can be held and released in batches.

**Why:** With a forecast, buyers can negotiate volume prices, place orders ahead, and warn you when a part is going on allocation.
Without one, they can only buy for the job in front of them.
Distributors can hold stock against a forecast and release it as you build, so you don't pay for a year of expensive parts up front.

**What goes wrong if you don't:** Higher prices, surprises when parts run short, and more cash tied up than necessary.

**Example:** A chip quoted automatically at about $25 each for 5,000 pieces came down to about $8 each through a distributor's quote.
A customer alarmed that 15 parts had been pulled from a supply program during a shortage calmed down when shown they added up to $300 a year, and that the distributor was already holding stock for them.

**Applies to:** General practice; most useful once you're past prototypes.

**Sources:** [“All about parts purchasing - part 2”](https://www.buzzsprout.com/1066066/episodes/4704659-all-about-parts-purchasing-part-2) (Jul 2020), [08:00](https://www.buzzsprout.com/1066066/episodes/4704659?t=480)–10:00; [“Discussing the Global Electronics Parts Shortage w/ Digi-Key”](https://www.buzzsprout.com/1066066/episodes/8574130-discussing-the-global-electronics-parts-shortage-w-digi-key) (May 2021), [37:00](https://www.buzzsprout.com/1066066/episodes/8574130?t=2220); [“How Small Manufacturers Manage Large Volume Orders”](https://www.buzzsprout.com/1066066/episodes/12586426-how-small-manufacturers-manage-large-volume-orders) (Apr 2023), [27:00](https://www.buzzsprout.com/1066066/episodes/12586426?t=1620)–29:00; [“Our top suggestions for customers w/ CircuitHub Account Manager, John Jacquinet”](https://www.buzzsprout.com/1066066/episodes/8884604-our-top-suggestions-for-customers-w-circuithub-account-manager-john-jacquinet) (Jul 2021), [21:00](https://www.buzzsprout.com/1066066/episodes/8884604?t=1260)–22:00.

*Last reviewed: 2026-11-09*

---

## PCB-DFA-099: Don't set a fixed date-code limit; store parts well, and have old or doubtful stock tested for solderability

**Recommendation:** Don't put a blanket date-code limit (such as "no older than 2 years") on your BOM or purchase orders.
Instead, store parts sealed and dry, and have the solderability of stock over about 2 years old, or of unknown history, tested to J-STD-002 before a build.
If parts won't wet in assembly, suspect contamination of the leads as well as age.

**Why:** Solderability depends on how parts were made, packed and stored more than on their age.
Properly stored parts solder well for many years, and some makers guarantee solderability for at least 2 years from shipment.
Badly stored or contaminated parts can fail sooner.
Makers and distributors, through their trade association (ECIA), recommend against general date-code limits: decades of process improvement removed most age-related failures, and the military specifications that started the practice have dropped it.

**Typical values:** Test stock older than about 2 years, or with no storage history.
J-STD-002 covers the test methods for component leads and terminations.

**What goes wrong if you don't:** Good parts refused for their age, or bad ones accepted for it.

**Example:** A broker found 2-year-old parts that wouldn't solder because their copper had tarnished, traced in one case to sulfur contamination when they were made, while 30-year-old stock it held still soldered well.
Separately, solder refused to wet a manufacturer's parts because silicone release agent from their carrier tape had transferred to the leads.

**Applies to:** General practice.

**Sources:** [“Navigating the Environmental Impact of Electronics w/ Component Sense Founder, Kenny McGee”](https://www.buzzsprout.com/1066066/episodes/15877892-navigating-the-environmental-impact-of-electronics-w-component-sense-founder-kenny-mcgee) (Oct 2024), [17:00](https://www.buzzsprout.com/1066066/episodes/15877892?t=1020)–21:00; [“Board Cleaning w/ Mike Konrad (part 1)”](https://www.buzzsprout.com/1066066/episodes/8399139-board-cleaning-w-mike-konrad-part-1) (Apr 2021), [35:00](https://www.buzzsprout.com/1066066/episodes/8399139?t=2100)–36:00; ECIA, "Managing Date Code Restrictions on Orders for Electronic Components", GIPC #101 (June 2023); IPC/EIA/JEDEC J-STD-002 (solderability tests for component leads); Chris Denney (author).

*Last reviewed: 2026-11-09*

---

## Related pages
- [Choosing parts that can be bought and built](01-choosing-parts.md)
- [The BOM](../01-design-package/03-bom.md) (alternates: PCB-DFA-069)
- [Supplying your own parts (consignment) and spares](05-consignment-and-spares.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

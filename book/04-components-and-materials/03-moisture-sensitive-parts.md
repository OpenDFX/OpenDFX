# Moisture-sensitive parts

Plastic packages absorb moisture from the air.
In the reflow oven, which runs far above the boiling point of water, that moisture turns to steam and can crack the package or lift it apart inside ("popcorning").
Each part's moisture sensitivity level (MSL) says how long it can be out of its sealed bag before it has to be soldered or baked.
The assembler manages the clock, but the designer chooses the parts, and anyone who holds or sends in their own stock shares the job.
The standards are J-STD-020, which sets a part's level, and J-STD-033, which says how to store, bake and use it.

## PCB-DFA-091: Put each part's moisture sensitivity level on the BOM, from its datasheet

**Recommendation:** Look up every plastic surface-mount part's MSL in its datasheet or the maker's product page, not the bag or a distributor's listing.
Give the BOM an MSL column, so the assembler sees the level of every part.
Flag anything at MSL 3 or higher, and parts known to be moisture-sensitive even if they aren't labeled that way (some LEDs, for example).

**Why:** Nearly any part that isn't hermetically sealed can take on moisture.
The maker's rating is the authority; packaging and listings are sometimes wrong.
The assembler can only plan exposure times and baking for parts it knows about.
It's very rare for a customer to say which parts are moisture-sensitive, so assemblers usually have to look up every one themselves; an MSL column on the BOM is the easiest way to hand them that information.

**Typical values:** Most chips are rated MSL 3 or higher.
MSL 1 parts need no special handling; MSL 2 and above are shipped in sealed bags with desiccant.

**What goes wrong if you don't:** Parts that crack or delaminate in reflow, sometimes without failing until later in the field.

**Example:** A customer sent in moisture-sensitive LEDs in ordinary packaging, with no warning; they were reflowed as received and damaged.

**Applies to:** General practice.

**Sources:** [“How to Manage Moisture Sensitive Devices”](https://www.buzzsprout.com/1066066/episodes/10522014-how-to-manage-moisture-sensitive-devices) (May 2022), [20:00](https://www.buzzsprout.com/1066066/episodes/10522014?t=1200) and [37:00](https://www.buzzsprout.com/1066066/episodes/10522014?t=2220)–39:00; [“All about parts purchasing - part 2”](https://www.buzzsprout.com/1066066/episodes/4704659-all-about-parts-purchasing-part-2) (Jul 2020), [36:00](https://www.buzzsprout.com/1066066/episodes/4704659?t=2160)–38:00; IPC/JEDEC J-STD-020 and J-STD-033.

*Last reviewed: 2026-11-09*

---

## PCB-DFA-092: Prefer a lower moisture level when you have the choice, and remember a double-sided build uses one floor life for both sides

**Recommendation:** When two parts would do, choose the one with the lower MSL.
Avoid MSL 5, 5a and 6 parts unless there's no alternative, and tell your assembler early if you use one.
On a double-sided board, plan for both sides being built within one floor life.

**Why:** Floor life is the time a part can spend in factory air, after its bag is opened, before it's soldered.
It's set at 30 °C and 60% relative humidity; warmer or damper air shortens it.
The clock runs until the part's last reflow, so building the first side doesn't reset it for the second.
Short floor lives force small batches, careful scheduling, or a bake.

**Typical values:** Floor life at up to 30 °C and 60% RH, from J-STD-033:

| MSL | Floor life |
|---|---|
| 1 | Unlimited (at up to 85% RH) |
| 2 | 1 year |
| 2a | 4 weeks |
| 3 | 168 hours (1 week) |
| 4 | 72 hours |
| 5 | 48 hours |
| 5a | 24 hours |
| 6 | Bake before use, then solder within the time on the label |

**What goes wrong if you don't:** Builds scheduled around one part's clock, extra baking, and higher cost.

**Example:** An assembler building double-sided boards with MSL 5a parts ran them in batches of 50–100 on trays, so both sides could be reflowed within 24 hours of opening the bag.

**Applies to:** General practice.

**Sources:** [“How to Manage Moisture Sensitive Devices”](https://www.buzzsprout.com/1066066/episodes/10522014-how-to-manage-moisture-sensitive-devices) (May 2022), [30:00](https://www.buzzsprout.com/1066066/episodes/10522014?t=1800)–36:00; IPC/JEDEC J-STD-033, Table 1 (floor life), as quoted in a chip maker's application reports (2017, 2018).

*Last reviewed: 2026-11-09*

---

## PCB-DFA-093: Expect cheap addressable RGB LEDs and similar parts to need baking, and budget for it

**Recommendation:** If you use low-cost addressable RGB LEDs, or other parts known to soak up moisture, expect your assembler to bake them before reflow, even when they arrive sealed.
Allow for the extra time and cost, or choose a more expensive part that doesn't need it.

**Why:** These LEDs absorb moisture readily, and their packaging often doesn't keep it out.
Baking is an extra step outside the normal flow.
Damage from moisture can be intermittent: a small delamination opens when the part warms up and closes again when it cools.

**Typical values:** A low-cost addressable LED can cost a quarter of an equivalent from a mainstream maker; part of the difference comes back as baking.

**What goes wrong if you don't:** LEDs that burn out after reflow, or boards that pass a short test and fail in the field.

**Example:** LED matrix boards passed a 30-second bench test, then failed in the sun; the heat opened small delaminations that closed again once the boards cooled.

**Applies to:** Addressable RGB LEDs and other parts with a known moisture problem.

**Sources:** [“Showstoppers that delay PCB assembly w/ Production Manager, Rob OConnell”](https://www.buzzsprout.com/1066066/episodes/9741439-showstoppers-that-delay-pcb-assembly-w-production-manager-rob-oconnell) (Dec 2021), [49:00](https://www.buzzsprout.com/1066066/episodes/9741439?t=2940); [“The RGB LED Dilemma in Manufacturing”](https://www.buzzsprout.com/1066066/episodes/15667846-the-rgb-led-dilemma-in-manufacturing) (Sep 2024), [07:00](https://www.buzzsprout.com/1066066/episodes/15667846?t=420)–09:00; [“How to Manage Moisture Sensitive Devices”](https://www.buzzsprout.com/1066066/episodes/10522014-how-to-manage-moisture-sensitive-devices) (May 2022), [16:00](https://www.buzzsprout.com/1066066/episodes/10522014?t=960)–18:00.

*Last reviewed: 2026-11-09*

---

## PCB-DFA-094: Keep your own moisture-sensitive stock sealed, and let your assembler bake anything that's been exposed

**Recommendation:** If you hold moisture-sensitive parts yourself:
- after taking parts out, reseal the bag within the hour with fresh desiccant and a humidity indicator card, ideally with a heat sealer;
- push the air out, but don't vacuum-seal tight;
- use bags made for electronics that block both moisture and static;
- if a bag stays open longer than an hour, write on it the date and time it was opened, and how long it was out;
- keep opened bags from being punctured (tube ends and sharp reel edges are the usual cause).

If the humidity card shows the parts have been exposed, don't bake them yourself: send them as they are and tell your assembler.

**Why:** A bag opened briefly and resealed straight away doesn't start the floor-life clock: J-STD-033 lets short exposures, in air no worse than 30 °C and 60% RH, be dried out again by the desiccant in a sealed bag or a dry cabinet.
This is how distributors split large packages into smaller ones without logging the few minutes the parts were out.
After more than an hour in factory air, resealing doesn't necessarily stop the clock: dry storage pauses or resets it only within the limits in the table below, and beyond them only a bake resets it.
The desiccant needs some air in the bag to draw moisture from the parts.
Plain static bags don't block moisture, and some moisture bags aren't made for electronics.
Some humidity cards change back once they dry out, so a card that looks safe may not be.
Baking needs the right temperature and time for each part's level and thickness.
Reels and tubes can't go above 40 °C, where a bake takes days or weeks; only trays rated for it can go in at 125 °C.

![D60: Not to scale. A moisture barrier bag heat-sealed across the top, holding a reel of parts, a desiccant pouch and a humidity indicator card with three spots marked 60%, 10% and 5%, all blue (dry). A caution label on the outside reads: moisture-sensitive, level 3, floor life 168 hours at up to 30 °C and 60% RH, with the bag seal date.](images/moisture-bag.svg)

*D60 shows what goes in a moisture barrier bag, not to scale.
The heat seal, fresh desiccant and humidity card keep the parts dry; the caution label gives the level, the floor life and the date the bag was sealed.*


**Typical values:** For parts that have been out in air no worse than 30 °C and 60% RH (J-STD-033D Table 4-3):

| MSL | Time out of the bag | What restores the floor life |
|---|---|---|
| 2, 2a, 3 | Less than the floor life, in total | Clock paused while stored at 10% RH or less |
| 2, 2a, 3 | 12 hours or less | Reset by dry storage for 5 times the exposure, at 10% RH or less |
| 4, 5, 5a | 8 hours or less | Reset by dry storage for 10 times the exposure, at 5% RH or less |
| Any | Longer than the above, or past the floor life | Bake, then dry-pack |

Bake times for an MSL 3 part past its floor life by more than 72 hours (J-STD-033D Table 4-1):

| Package body thickness | At 125 °C | At 90 °C | At 40 °C |
|---|---|---|---|
| Under 0.5 mm | 1 hour | 3 hours | 22 hours |
| 0.8 to 1.4 mm | 8 hours | 25 hours | 8 days |
| 1.4 to 2.0 mm | 27 hours | 4 days | 37 days |
| 2.0 to 4.5 mm | 48 hours | 10 days | 79 days |

Higher levels and thicker parts take longer; large BGAs and stacked-die parts can need 96 hours at 125 °C.
The floor life starts again from zero after a bake.

**What goes wrong if you don't:** Parts that need baking on arrival, which delays the build, or parts damaged by the wrong bake.

**Applies to:** Anyone holding or consigning moisture-sensitive parts.

**Sources:** [“All the Tricks and Gotchas in Surface Mount Assembly (Repost from the Coriolis Effect)”](https://www.buzzsprout.com/1066066/episodes/11006453-all-the-tricks-and-gotchas-in-surface-mount-assembly-repost-from-the-coriolis-effect) (Jul 2022), [44:00](https://www.buzzsprout.com/1066066/episodes/11006453?t=2640)–47:00; [“How to Manage Moisture Sensitive Devices”](https://www.buzzsprout.com/1066066/episodes/10522014-how-to-manage-moisture-sensitive-devices) (May 2022), [21:00](https://www.buzzsprout.com/1066066/episodes/10522014?t=1260)–25:00 and [41:00](https://www.buzzsprout.com/1066066/episodes/10522014?t=2460)–49:00 and [51:00](https://www.buzzsprout.com/1066066/episodes/10522014?t=3060)–56:00; [“Stick It Up Your Tube”](https://www.buzzsprout.com/1066066/episodes/14388259-stick-it-up-your-tube) (Jan 2024), [14:00](https://www.buzzsprout.com/1066066/episodes/14388259?t=840)–15:00 and [38:00](https://www.buzzsprout.com/1066066/episodes/14388259?t=2280)–40:00; IPC/JEDEC J-STD-033D, sections 4.1–4.1.2 (exposure to factory air) and Tables 4-1 and 4-3 (baking, and pausing or resetting the clock); a chip maker's application reports on floor life and baking (2017, 2018).

*Last reviewed: 2026-11-09*

---

## Related pages
- [Packaging: reels, cut tape, tubes, trays](02-packaging.md)
- [Supplying your own parts (consignment) and spares](05-consignment-and-spares.md)
- [Reflow soldering](../05-assembly/03-reflow-soldering.md)
- [Surface finish](../03-bare-board-fabrication/08-surface-finish.md) (storing and baking bare boards: PCB-DFA-080)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

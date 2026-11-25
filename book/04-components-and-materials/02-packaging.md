# Packaging: reels, cut tape, tubes, trays

Surface-mount parts reach the machine in one of four ways: on a reel of carrier tape, on a cut length of that tape, in a plastic tube, or in a tray.
How a part is packaged decides how fast and how reliably it can be placed, and sometimes what it costs.
The same part is often sold in more than one packaging, under part numbers that differ by a single character.
For supplying your own parts in the right packaging, see [Supplying your own parts](05-consignment-and-spares.md).

## PCB-DFA-089: Choose tape and reel, and use tubes only as a last resort

**Recommendation:** Choose parts sold on tape and reel.
Treat tubes as a last resort, after every other option is exhausted: a tape-and-reel version of the same part, an equivalent part on tape, or a re-taping service at the distributor.
Pay a little more for a part on tape rather than design in one that only comes in tubes.
Large or delicate chips in trays are fine.
On the BOM, give the maker's full part number including the packaging code (often a suffix such as R for reel or T for tube), so the right packaging is bought.

**Why:** Assemblers like tubes less than any other packaging.
Some assemblers, Worthington Assembly among them, are asking component makers to stop using tubes altogether.
Carrier tape feeds one pocket at a time, holds thousands of parts per reel, and can only be loaded one way round.
Tubes hold far fewer parts, feed by vibration and gravity, and jam more often, even on the best feeders.
A tube is symmetrical, so it can be loaded backwards.
Its rigid ends puncture moisture barrier bags, and it's too long for most drying ovens.
Parts sold only in tubes are often sent to a specialist to be re-taped before they can run well, which adds cost and time.

**Typical values:** A tube holds about 50–100 parts; a reel of the same part, about 2,500.
Tape from 8 mm to 24 mm wide is asymmetrical and can't be loaded backwards; wider tape marks its sides with different sprocket holes.

![D56: Four panels, not to the same scale. Carrier tape 8 mm wide, enlarged and drawn to scale, with sprocket holes along one edge every 4 mm, pockets every 4 mm holding chip parts lying across the tape under a clear cover tape, and empty pockets at the leading end as leader, with an arrow for the direction of feed. A 178 mm reel with tape coming off it. A tube about 500 mm long holding a row of SOIC chips, with a stopper in each end. A tray about 323 by 136 mm with a grid of pockets, each holding a large chip with pin 1 the same way.](images/packaging-types.svg)

*D56 shows the four ways parts arrive, not to the same scale.
Carrier tape has sprocket holes along one edge only, so it can only be loaded one way; on a full reel from the maker, the pockets at the leading end, which goes into the feeder first, are left empty as leader.
A tube holds 50–100 parts and looks the same from either end; a tray is for large or delicate chips.*


**What goes wrong if you don't:** Slower builds, more stoppages, extra handling charges, and the occasional batch of parts placed backwards from a reversed tube.

**Example:** A tube loaded backwards into a feeder put a run of parts on the board the wrong way round, and every one had to be reworked.

**Applies to:** General practice.
Tubes do have one advantage: they hold heavy through-hole parts by the body, so the leads don't bend.

**Sources:** [“Stick It Up Your Tube”](https://www.buzzsprout.com/1066066/episodes/14388259-stick-it-up-your-tube) (Jan 2024), [04:00](https://www.buzzsprout.com/1066066/episodes/14388259?t=240)–05:00 and [10:00](https://www.buzzsprout.com/1066066/episodes/14388259?t=600)–20:00 and [30:00](https://www.buzzsprout.com/1066066/episodes/14388259?t=1800)–36:00 and [38:00](https://www.buzzsprout.com/1066066/episodes/14388259?t=2280)–40:00; [“What factors influence PCB quotes w/ Brett Babilonia”](https://www.buzzsprout.com/1066066/episodes/14580855-what-factors-influence-pcb-quotes-w-brett-babilonia) (Feb 2024), [18:00](https://www.buzzsprout.com/1066066/episodes/14580855?t=1080)–19:00; [“How to Send Consigned Material to Your CM”](https://www.buzzsprout.com/1066066/episodes/10182930-how-to-send-consigned-material-to-your-cm) (Mar 2022), [24:00](https://www.buzzsprout.com/1066066/episodes/10182930?t=1440)–26:00; EIA-481 (tape and reel packaging of surface-mount parts).

*Last reviewed: 2026-11-09*

---

## PCB-DFA-090: Choose connectors packaged for machine placement: on tape, with a flat top or a pick-up cap

**Recommendation:** For surface-mount and hybrid connectors, choose a version supplied on tape and reel with a flat area for the machine's vacuum nozzle: either a flat top on the body, or a pick-up cap or polyimide (Kapton) pad fitted by the maker.
Check the order code: the cap or pad is often a separate option, sold under its own suffix.

**Why:** Placement machines pick parts with a vacuum nozzle, which needs a flat, solid surface near the part's center of mass.
Many connectors have open tops, slots or pins where a nozzle can't seal.
Some machines have grippers that can pick a part with no flat area, and an assembler can 3D-print a custom tray for loose parts, load it by hand and let the machine place from it.
Both work, but grippers are slower and harder to set up than vacuum nozzles, and a custom tray takes time to design, print and load, all of which adds cost.
Otherwise, the connector is fitted by hand.

**What goes wrong if you don't:** Connectors placed by hand, slowly and less accurately, or a machine that drops them.

**Example:** On one product, electrically identical connectors differed greatly in how quickly and accurately they could be placed, depending only on how they were packaged.

**Applies to:** General practice.

**Sources:** [“How Loci Controls automates landfill methane gas collection”](https://www.buzzsprout.com/1066066/episodes/5509702-how-loci-controls-automates-landfill-methane-gas-collection) (Sep 2020), [59:00](https://www.buzzsprout.com/1066066/episodes/5509702?t=3540)–01:00:00; connector makers' tape-and-reel options with pick-up caps and polyimide pads.

*Last reviewed: 2026-11-09*

---

## Related pages
- [Choosing parts that can be bought and built](01-choosing-parts.md)
- [Moisture-sensitive parts](03-moisture-sensitive-parts.md)
- [Supplying your own parts (consignment) and spares](05-consignment-and-spares.md)
- [Component placement](../05-assembly/02-component-placement.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

# Surface finish

Bare copper tarnishes within days and then won't take solder.
So every pad and hole left open by the solder mask gets a thin protective coat, the surface finish, just before the board is profiled and tested.
The finish decides how flat the pads are, how long the boards keep, how well they solder, and part of the price.

| Finish | What it is | Flat enough for fine pitch? | How it ages | Notes |
|---|---|---|---|---|
| ENIG | Electroless nickel with a thin immersion gold coat | Yes | Slowly: the thin, porous gold keeps the nickel from oxidizing | The common default; costs more than HASL; rare "black pad" defect if the fab's nickel process drifts |
| ENEPIG | ENIG with a palladium layer between nickel and gold | Yes | Like ENIG | For gold or aluminum wire bonding as well as soldering; less prone to black pad; costs more again |
| HASL, lead-free | Board dipped in molten solder, leveled with hot air | No: domed pads | Thin spots, such as hole edges, lose solderability first, typically in 6–12 months; the rest lasts one to two years | Cheapest; fine for through-hole and coarse surface-mount parts |
| OSP | A thin organic coat on bare copper | Yes | Fastest: check solderability after 6 months | Cheap and flat; easily damaged by handling, and weakened by each heat cycle |
| Immersion silver | A thin silver coat | Yes | Spoiled by sulfur and chlorine in the air; needs sulfur-absorbing paper in the bag | Flat; tarnishes if handled or stored badly |
| Immersion tin | A thin tin coat | Yes | Oxidizes relatively quickly, and tin-copper compounds grow through it whatever the packaging | Flat; tin whiskers are a further worry |
| Hard gold | Electroplated gold, hardened, over nickel | n/a | Slowly; thicker and less porous than ENIG | For contacts that slide or wear, such as edge fingers (see PCB-DFM-038); not for soldering |

How finishes age is from IPC-1602A (Nov 2024), section 4.1.3.
Dry-packed boards keep at least 12 months, but IPC-1602A asks for a solderability check on boards stored longer than 6 months with OSP, or a year with any other finish.

## PCB-DFM-036: Always name the surface finish on the fabrication drawing

**Recommendation:** State the surface finish on the fabrication drawing and in the order, every time, even when you'd be happy with the fab's default.
For ENIG, ENEPIG, immersion silver and immersion tin, citing the IPC finish standard (IPC-4552, IPC-4556, IPC-4553, IPC-4554) fixes the thicknesses too.

**Why:** Fabs and standards fill gaps with defaults, and those differ.
IPC-6012F, the standard most fabs build to, says that if the finish isn't specified, drawings first released on or after 1 October 2023 get ENIG, and older drawings get "X": a solder coating or fused tin-lead.
An old drawing reused without a finish can therefore legally come back with tin-lead on it.

**Typical values:** IPC-6012F Table 1-2 default: ENIG (drawings from 1 October 2023), "X" before that.

**What goes wrong if you don't:** A finish you didn't expect, which may not suit your parts, your lead-free process or your price.

**Applies to:** General practice.

**Sources:** IPC-6012F (Sept 2023), Table 1-2 and Table 3-3.

*Last reviewed: 2026-11-08*

---

## PCB-DFM-037: Choose ENIG for most boards; lead-free HASL only for coarse pitch; OSP or immersion silver for high volume with tight process control

**Recommendation:** Use ENIG unless you have a reason to choose something else.
Use lead-free HASL only on boards whose finest parts are about 0.65 mm pitch or 0603 and larger, with no BGAs or QFNs.
Consider OSP or immersion silver for high volumes where the assembler controls handling, storage and time between steps closely.
Choose ENEPIG for wire bonding, and hard gold only for contacts that wear.

**Why:** Small parts need flat pads: a domed HASL pad lets a tiny part tilt or a QFN rock, and makes paste printing uneven.
ENIG is flat, solders well, and keeps for about a year sealed, which suits small batches that may wait between bare board and assembly.
OSP and immersion silver are cheaper and flat, but much less forgiving: fingerprints, humidity and time all spoil them, and OSP weakens with every trip through the oven, which matters on double-sided boards.

**Typical values:** HASL: down to about 0.65 mm pitch and 0603.
See the table above for shelf lives.

**What goes wrong if you don't:** With HASL on fine pitch, bridges, tombstones and open joints; with OSP stored too long or handled carelessly, poor wetting and open joints on the second side.

**Applies to:** General practice; prices and shelf lives vary by fab.

**Sources:** [“All the Tricks and Gotchas in Surface Mount Assembly (Repost from the Coriolis Effect)”](https://www.buzzsprout.com/1066066/episodes/11006453-all-the-tricks-and-gotchas-in-surface-mount-assembly-repost-from-the-coriolis-effect) (Jul 2022), [01:14:00](https://www.buzzsprout.com/1066066/episodes/11006453?t=4440)–01:17:00; fabs' published surface-finish comparisons (flatness, shelf life, cost, black pad).

*Last reviewed: 2026-11-08*

---

## PCB-DFM-038: Give edge-connector fingers hard gold and a bevel, with mask and legend kept off them

**Recommendation:** For fingers that plug into a card-edge connector, specify hard (electroplated) gold over nickel, and a bevel on the inserting edge.
Keep solder mask and legend off the fingers, keep plated holes and other pads away from them, and round or chamfer the board corners beside them.
Put the gold thickness, bevel angle and bevel depth on the fabrication drawing.

**Why:** Fingers slide in and out of a connector, and the soft, thin gold of ENIG wears through after a few insertions; hard gold is made for wear.
A bevel lets the board slide into the connector instead of stubbing on its contacts.
The fingers are plated through a strip that's removed at the edge, so the fab needs them to run cleanly to the edge with nothing else in the way.

![D52: Drawn to scale. Plan view of a board edge with six hard-gold fingers, 1.5 mm wide on a 2.54 mm pitch, ending 0.6 mm from the edge, with the solder mask cleared from the whole finger area and the corners beside them chamfered. Below, enlarged 2.5 times, a side view of the 1.6 mm board beveled at 30 degrees on both faces over the last 0.5 mm, with the fingers stopping before the bevel.](images/gold-fingers.svg)

*D52 is drawn to scale, with the side view enlarged, and uses example sizes.
The fingers are hard gold with no mask over them, and the board's corners beside them are chamfered.
The inserting edge is beveled on both faces, and the fingers stop 0.6 mm short of the edge, clear of the bevel.*

**Typical values:** Hard gold at least 0.8 µm (Class 1–2) or 1.25 µm (Class 3) over at least 2.5 µm of nickel (IPC-6012F Table 3-3).
Bevel 30° or 45°, commonly 30°, about 0.5–1.0 mm deep; keep other plated features about 1 mm from the fingers.

**What goes wrong if you don't:** Fingers that wear through or scratch the connector, boards that won't insert cleanly, and fab queries about mask or holes in the plating area.

**Applies to:** General practice; bevel limits vary by fab.

**Sources:** IPC-6012F (Sept 2023), Table 3-3; fabs' published edge-connector and gold-finger guidelines. Not covered in the podcast.

*Last reviewed: 2026-11-08*

---

## PCB-DFA-080: Keep bare boards sealed, use them within the finish's shelf life, and expect a bake if they've taken on moisture

**Recommendation:** Expect bare boards to arrive dry-packed: heat-sealed in a moisture barrier bag with desiccant and a humidity indicator card, and only lightly evacuated, not vacuum-packed hard.
Keep them sealed until assembly, and build them within a year (six months for OSP).
Once a bag is opened, the boards should be built promptly, or go back into dry storage.
If the bag was damaged, the card shows moisture, or the boards are older than that, tell the assembler, and expect them to be checked, dried in dry storage or baked just before assembly, or rejected.
Don't ask the fab to bake boards before shipping.
If your board is unusually sensitive to moisture (polyimide, or thick and many-layered), say so on the drawing; IPC-1602A leaves it to the designer or user to set how much moisture the board can tolerate.

**Why:** Laminate absorbs moisture from the air.
In the reflow oven that moisture turns to steam and can blister or delaminate the board.
Finishes age too, and solder wets an old finish poorly; dry packing slows the moisture but doesn't stop the finish aging.
Squeezing all the air out of the bag stops the desiccant working, can warp boards and lets sharp corners puncture the bag.
Baking drives the moisture out but ages the finish further, so it's done only when needed and as late as possible.
A humidity card shows the air in the bag, not the moisture in the boards, so a card that has changed color after a short exposure doesn't always mean a bake: dry storage can be the safer fix.

**Typical values:** IPC-1602A, unless you specify otherwise: boards packed with no more than 0.2% moisture by weight, in a moisture barrier bag with desiccant and a three-spot humidity card (5%, 10%, 60% RH); this keeps them at least 12 months at up to 40 °C and 90% RH, and double-bagging at least two years.
Check solderability after 6 months for OSP and 12 months for other finishes.
An opened bag: boards into dry storage at 10% RH or less within an hour, or resealed with the same desiccant and card within 30 minutes.
Handle boards by the edges, with clean gloves if needed.
Immersion silver also needs sulfur-absorbing paper in the bag.

**What goes wrong if you don't:** Blistered or delaminated boards, and poorly wetted joints, often found only after assembly.

**Applies to:** General practice.

**Sources:** [“All the Tricks and Gotchas in Surface Mount Assembly (Repost from the Coriolis Effect)”](https://www.buzzsprout.com/1066066/episodes/11006453-all-the-tricks-and-gotchas-in-surface-mount-assembly-repost-from-the-coriolis-effect) (Jul 2022), [01:16:00](https://www.buzzsprout.com/1066066/episodes/11006453?t=4560)–01:17:00; IPC-1602A, Standard for Printed Board Handling and Storage (Nov 2024), sections 4.1–4.2 and 5.1–5.8; a European PCB industry association's recommendations on IPC-1601 (bake just before assembly, not at the fab).

*Last reviewed: 2026-11-08*

---

## Related pages
- [Solder mask](07-solder-mask.md)
- [Fabrication data](../01-design-package/01-fabrication-data.md)
- [Reflow soldering](../05-assembly/03-reflow-soldering.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

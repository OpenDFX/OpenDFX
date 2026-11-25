# Solder mask

Solder mask is the colored coat over most of the board.
It goes on as a liquid, is exposed through a pattern and developed away from every pad you'll solder, then cured hard.
It stops solder running where it shouldn't, insulates the copper under it, and protects it.
How much mask a fab can leave between two pads, and how closely it can line the openings up with the copper, decides how fine your pitch can go.

## PCB-DFM-033: Choose green solder mask and white legend unless you have a reason not to

**Recommendation:** Use green solder mask with white legend unless the product needs another color.
If it does, any common color can be built; expect the effects below, and choose a legend color that stands out against the mask: white on green, blue, red or black, and black on white or yellow.

**Why:** Green mask lets the most ultraviolet light through when it's exposed, so it holds the finest dams between pads.
Some fabs can hold a 0.075 mm (3 mil) dam in green, against about 0.1 mm (4 mil) in other colors.
Green also gives cameras and people the best contrast with solder and copper.
Black mask hides black parts and reflects little light back to optical inspection machines, so it's harder to rework by eye, and 3D inspection machines handle it far better than 2D ones.
Red mask can confuse inspection machines that light the board with red LEDs, because the red light coming back from the mask looks like light from a solder joint.
Some white masks turn yellow or brown after several trips through the oven, and not every fab stocks white; ask for a white made to survive repeated reflow if appearance matters, as it does on LED boards.

**Typical values:** Smallest dam between pads: about 0.075 mm in green at some fabs, 0.1 mm in black, red, blue, yellow and white; 0.1 mm is recommended for every color (see [PCB-DFA-032](../01-design-package/04-footprints.md#pcb-dfa-032-put-a-solder-mask-dam-between-every-pad-of-a-fine-pitch-part)).

**What goes wrong if you don't:** Coarser limits on fine-pitch parts, slower inspection programming, and parts that are hard to see during rework.
None of these makes a board unbuildable.

**Example:** Some widely used inspection machines light boards with red LEDs, so red mask adds programming time on them.
A designer with two near-identical boards that differed by a couple of parts used a different mask color for each, with matching kit labels, so the two could never be mixed up on the line.

**Applies to:** General practice.
Color limits vary by fab and by inspection machine.

**Sources:** [“How sensors.AFRICA empowers citizens to fight against pollution w/ Jack McLeans”](https://www.buzzsprout.com/1066066/episodes/7831030-how-sensors-africa-empowers-citizens-to-fight-against-pollution-w-jack-mcleans) (Feb 2021), [43:00](https://www.buzzsprout.com/1066066/episodes/7831030?t=2580)–47:00; [“The PCB CAM Process w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/8226431-the-pcb-cam-process-w-dave-wilcox) (Mar 2021), [40:00](https://www.buzzsprout.com/1066066/episodes/8226431?t=2400)–41:00; [“Gloves not Mittens”](https://www.buzzsprout.com/1066066/episodes/19269842-gloves-not-mittens) (Jun 2026), [18:00](https://www.buzzsprout.com/1066066/episodes/19269842?t=1080)–19:00; [“Stencils: The Unsung Heroes of PCB Perfection Pt. 2”](https://www.buzzsprout.com/1066066/episodes/15484609-stencils-the-unsung-heroes-of-pcb-perfection-pt-2) (Jul 2024), [34:00](https://www.buzzsprout.com/1066066/episodes/15484609?t=2040)–35:00; [“Impedance Control Demo w/ NCAB Group Field Application Engineer Ryan Miller”](https://www.buzzsprout.com/1066066/episodes/13789746-impedance-control-demo-w-ncab-group-field-application-engineer-ryan-miller) (Oct 2023), [37:00](https://www.buzzsprout.com/1066066/episodes/13789746?t=2220)–39:00; [“Automated Optical Inspection (AOI) for PCB Assembly”](https://www.buzzsprout.com/1066066/episodes/6598753-automated-optical-inspection-aoi-for-pcb-assembly) (Nov 2020), [32:00](https://www.buzzsprout.com/1066066/episodes/6598753?t=1920); [“The PCB assembly inspection process”](https://www.buzzsprout.com/1066066/episodes/5713750-the-pcb-assembly-inspection-process) (Oct 2020), [45:00](https://www.buzzsprout.com/1066066/episodes/5713750?t=2700)–47:00; [“The importance of having different perspectives in engineering w/ Eli Hughes of Tzero Labs (Part 2)”](https://www.buzzsprout.com/1066066/episodes/7118017-the-importance-of-having-different-perspectives-in-engineering-w-eli-hughes-of-tzero-labs-part-2) (Jan 2021), [43:00](https://www.buzzsprout.com/1066066/episodes/7118017?t=2580)–45:00; [“An Answering Your Questions Grab Bag”](https://www.buzzsprout.com/1066066/episodes/13847902-an-answering-your-questions-grab-bag) (Oct 2023), [44:00](https://www.buzzsprout.com/1066066/episodes/13847902?t=2640)–46:00.

*Last reviewed: 2026-11-08*

---

## PCB-DFA-078: Keep a solder mask web between every via and the pad beside it, or tent the via

**Recommendation:** Where an open via sits next to a pad, leave a strip of solder mask (a web) between the via's copper and the pad.
If there isn't room for the web, tent the via (see [PCB-DFM-030](06-via-treatments.md#pcb-dfm-030-tent-vias-by-default-on-both-sides-if-theyre-03-mm-or-smaller)) or move it.
The exception is thermal vias in a QFN's ground pad, which stay open on purpose (see [PCB-DFA-075](06-via-treatments.md#pcb-dfa-075-never-put-solder-mask-on-thermal-vias-under-a-qfn)).

**Why:** Molten solder flows over any bare copper it touches.
With no mask between them, solder from the pad runs onto the via ring and down the hole, and the joint is left short of solder.
A very thin web over a long run is hard for the fab to hold and may break away.

![D49: Drawn to scale, plan views of a 1.0 by 1.2 mm pad joined by a 0.25 mm trace to a via with a 0.3 mm hole and a 0.6 mm ring. Left: the via has its own mask opening, leaving a 0.15 mm web of mask between it and the pad. Middle: the via is tented. Right: the via's opening runs into the pad's, with no web between them.](images/via-mask-web.svg)

*D49 is drawn to scale.
On the left, pad and via each have their own mask opening, and a 0.15 mm web of mask separates them.
In the middle, the via is tented, so only the pad is open.
On the right, the openings run together: nothing stops solder flowing from the pad onto the via and down its hole.*

**Typical values:** Web at least 0.1 mm (4 mil) wide, and only over short distances at that width; wider is better.

**What goes wrong if you don't:** Starved joints and solder balls on the far side of the board, which need rework.

**Applies to:** General practice.

**Sources:** [“All the Tricks and Gotchas in Surface Mount Assembly (Repost from the Coriolis Effect)”](https://www.buzzsprout.com/1066066/episodes/11006453-all-the-tricks-and-gotchas-in-surface-mount-assembly-repost-from-the-coriolis-effect) (Jul 2022), [01:10:00](https://www.buzzsprout.com/1066066/episodes/11006453?t=4200)–01:13:00 and [01:20:00](https://www.buzzsprout.com/1066066/episodes/11006453?t=4800)–01:22:00; [“Reflow soldering”](https://www.buzzsprout.com/1066066/episodes/6175423-reflow-soldering) (Nov 2020), [34:00](https://www.buzzsprout.com/1066066/episodes/6175423?t=2040)–35:00.

*Last reviewed: 2026-11-08*

---

## PCB-DFM-034: Clear solder mask from non-plated holes by about 0.1 mm, with no thin ring left

**Recommendation:** Give every non-plated hole a mask opening about 0.1 mm (4 mil) larger than the hole all round.
Don't leave a mask opening only a hair bigger than the hole.

**Why:** The fab drills the hole after the mask is on, and the drill and the mask never line up perfectly.
A mask opening barely larger than the hole leaves a ring of mask about 0.025 mm wide that either gets drilled into, so mask chips into the hole, or is too thin to stay put.

![D53: Drawn to scale, plan views of a 3.2 mm non-plated hole. Left: the mask opening is 0.1 mm larger than the hole all round, leaving a thin ring of bare board. Right: the opening is only 0.025 mm larger, and with the drill 0.08 mm off center the drill cuts into the mask on one side, leaving chipped mask at the edge.](images/npth-mask.svg)

*D53 is drawn to scale.
On the left, the mask stops 0.1 mm short of the hole, so the drill never touches it.
On the right, the opening is only a hair bigger than the hole; a drill slightly off center cuts into the mask on one side and leaves it chipped and flaking.*

**Typical values:** Mask clearance about 0.1 mm per side on non-plated holes.
Copper is kept back from non-plated holes too (see [PCB-DFM-007](../01-design-package/04-footprints.md#pcb-dfm-007-dont-put-copper-on-non-plated-holes)).

**What goes wrong if you don't:** A query from the fab, or flaking mask in and around mounting holes.

**Applies to:** General practice.

**Sources:** [“The PCB CAM Process w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/8226431-the-pcb-cam-process-w-dave-wilcox) (Mar 2021), [41:00](https://www.buzzsprout.com/1066066/episodes/8226431?t=2460)–43:00.

*Last reviewed: 2026-11-08*

---

## PCB-DFM-035: Expect the fab to trim pads to keep mask dams, and check what they changed

**Recommendation:** Expect the fab's CAM engineers to adjust your data so it can be built, most often by shaving a little off fine-pitch pads to keep the dam between them.
Ask the fab to send you its questions and changes (an engineering query) before it builds, and check them, especially on a first order.
If you plan to tighten mask registration, first ask whether the fab images its mask with a laser.

**Why:** The fab needs a little clearance between each pad and its mask opening, plus a dam between openings.
When your pads are too close for both, it either trims the copper or drops the dam, and a dropped dam is worse (see [PCB-DFA-032](../01-design-package/04-footprints.md#pcb-dfa-032-put-a-solder-mask-dam-between-every-pad-of-a-fine-pitch-part)).
Changes made in CAM are silent unless you ask to see them, and some (legend resized, pads trimmed, mask opened up) change what the assembler gets.
Laser-imaged mask lines up more accurately than mask exposed through film, so it needs less clearance.

![D54: Enlarged and drawn to scale, plan views of three pads of a 0.4 mm-pitch part. Left: pads 0.25 mm wide, 0.15 mm apart, with openings 0.05 mm larger on each side leave a 0.05 mm dam, too thin to hold. Middle: the fab has made one opening round all three pads, with no dam. Right: pads 0.2 mm wide leave room for a 0.1 mm dam.](images/dam-room.svg)

*D54 is enlarged and drawn to scale.
A dam can only be so thin, so the pads must leave room for it.
Pads drawn too wide for their pitch leave the fab two choices: trim the pads, as on the right, or remove the dam, as in the middle, which lets solder bridge from pad to pad.
Draw the pads to leave room for the dam in the first place (see [PCB-DFA-032](../01-design-package/04-footprints.md#pcb-dfa-032-put-a-solder-mask-dam-between-every-pad-of-a-fine-pitch-part)).*

**Typical values:** About 0.05 mm (2 mil) between a pad and its mask opening on each side, leaving a dam of about 0.1 mm (4 mil); pads trimmed by tens of microns.

**What goes wrong if you don't:** Boards that don't match your files, discovered at assembly.

**Applies to:** Varies by manufacturer; check with yours.

**Sources:** [“The PCB CAM Process w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/8226431-the-pcb-cam-process-w-dave-wilcox) (Mar 2021), [30:00](https://www.buzzsprout.com/1066066/episodes/8226431?t=1800)–40:00; [“An EDA Tool Walks Into a CM w/ Fusion 360 Electronics Product Manager, Ben Jordan”](https://www.buzzsprout.com/1066066/episodes/9171908-an-eda-tool-walks-into-a-cm-w-fusion-360-electronics-product-manager-ben-jordan) (Sep 2021), [54:00](https://www.buzzsprout.com/1066066/episodes/9171908?t=3240)–56:00 and [01:13:00](https://www.buzzsprout.com/1066066/episodes/9171908?t=4380)–01:14:00; [“Gloves not Mittens”](https://www.buzzsprout.com/1066066/episodes/19269842-gloves-not-mittens) (Jun 2026), [19:00](https://www.buzzsprout.com/1066066/episodes/19269842?t=1140)–21:00.

*Last reviewed: 2026-11-08*

---

## PCB-DFA-079: For BGAs, use copper-defined pads unless the part maker says otherwise

**Recommendation:** Draw BGA pads as copper-defined (non-solder-mask-defined, NSMD): the copper pad sets the size, and the mask opening is a little larger, so the mask doesn't touch the pad.
Use mask-defined pads (the mask overlaps the copper and sets the opening) only where the BGA maker's land pattern calls for them, usually on the finest pitches.
Say on the drawing which you've used.

**Why:** A copper pad's size is held by etching, which is more accurate than the mask's position, so every pad comes out the same.
Solder wraps around the pad's sides as well as its top, which anchors the joint.
Mask-defined pads hold their size by the mask, leave a notch where mask meets ball that can start cracks, but give the most even paste volume at very fine pitch, which is why some makers specify them.

![D50: Enlarged and drawn to scale, cross-sections through one ball of a 0.8 mm-pitch BGA after reflow. Left, copper-defined: a 0.35 mm pad with the mask opening larger, so solder wraps round the pad's sides. Right, mask-defined: a 0.45 mm pad with the mask over its edge, leaving a 0.35 mm opening and a notch where mask meets solder.](images/bga-pads.svg)

*D50 is enlarged and drawn to scale, with example sizes.
On the left, the mask stands clear of a 0.35 mm copper pad, and the solder wraps round the pad's sides.
On the right, the mask overlaps a 0.45 mm pad and sets a 0.35 mm opening; the solder meets the mask in a notch, where cracks can start.*

**Typical values:** Mask opening about 0.05–0.075 mm larger than the pad on each side; follow the BGA maker's land pattern where one is published.

**What goes wrong if you don't:** Uneven joints across the array, or cracked joints in products that see heat cycling or shock.

**Applies to:** General practice; the part maker's land pattern wins.

**Sources:** BGA makers' land-pattern notes (two semiconductor makers' BGA application notes recommend NSMD pads); fabs' published BGA pad guidance. Not covered in the podcast.

*Last reviewed: 2026-11-08*

---

## PCB-DFA-082: Join BGA and leadless pads to copper pours with a short trace, not straight into the pour

**Recommendation:** Where a pad of a BGA, QFN, DFN or other leadless part connects to a copper pour, keep the pour back from the pad and join them with a short, narrow trace, as you would a pad on its own.
Don't let the pour run straight into the pad.
This is the BGA and leadless-part version of [PCB-DFA-033](../01-design-package/04-footprints.md#pcb-dfa-033-set-the-solder-mask-expansion-of-fine-pitch-pads-yourself) and D26.

**Why:** A pad inside a pour has no copper edge of its own: the mask opening sets its size instead.
Every mask opening is a little larger than its pad, so pads tied into the pour come out bigger than their neighbors, and they sit wherever the mask lands rather than where the copper was etched.
On a BGA or leadless part, every joint is under the part and can't be touched up, so those few oversized pads take more solder, pull the part off center, and leave neighboring joints thin.
A pad joined by a short trace keeps its copper edge, so all the pads come out the same size.

![D55: Drawn to scale, plan views of the corner of a 0.8 mm-pitch BGA with 0.35 mm pads and 0.45 mm mask openings on a ground pour. Left: three ground pads sit straight in the pour, so their whole openings show copper and they come out bigger than the rest. Right: the pour is kept back from every pad and each ground pad is joined to it by a 0.15 mm trace, so every pad shows the same copper.](images/bga-pour.svg)

*D55 is drawn to scale.
On the left, the ground pads sit straight in the pour, so the mask opening, not the copper, sets their size, and they come out bigger than their neighbors.
On the right, a short trace joins each ground pad to the pour, and every pad is the same size.*

**Typical values:** Trace about 0.15–0.2 mm wide, or no wider than about half the pad; pour kept back from the pad by your usual clearance.

**What goes wrong if you don't:** Uneven joints, opens or bridges under BGAs and leadless parts, found only by X-ray; it's one of the most common design flaws assemblers see.

**Applies to:** General practice.

**Sources:** Chris Denney (author); [“Gloves not Mittens”](https://www.buzzsprout.com/1066066/episodes/19269842-gloves-not-mittens) (Jun 2026), [21:00](https://www.buzzsprout.com/1066066/episodes/19269842?t=1260)–23:00.

*Last reviewed: 2026-11-08*

---

## Related pages
- [Footprints and the component library](../01-design-package/04-footprints.md)
- [Via treatments](06-via-treatments.md)
- [Legend (silkscreen)](09-legend.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

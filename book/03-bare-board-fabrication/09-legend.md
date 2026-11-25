# Legend (silkscreen)

The legend is the printed text and outlines on the board: reference designators, polarity marks, part outlines, logos and labels.
It used to be screen printed, which is why most people still call it silkscreen; today most fabs print it with an inkjet.
Assemblers, inspectors and repair technicians all read it, so it's worth making it legible, accurate and out of the way of the solder.
What to mark (pin 1, polarity, outlines) is in [Footprints and the component library](../01-design-package/04-footprints.md); this page is about how it's printed.

## PCB-DFM-039: Make legend text about 1 mm tall, with lines of 0.15 mm or more

**Recommendation:** Make legend text about 1 mm tall and 1 mm wide, with a line width of 0.18–0.2 mm.
Don't go below 0.15 mm line width or about 0.8 mm text height.
If text doesn't need to be small, don't make it small.

**Why:** The legend ink spreads and the printer has a resolution limit.
Lines thinner than the fab's minimum are removed or come out broken, and small text fills in until it can't be read.
Text sized generously costs nothing and is read by people at every step after.

**Typical values:** Line width 0.15 mm (6 mil) minimum, 0.18–0.2 mm recommended; text 1 mm tall, 0.8 mm minimum.
Some fabs print down to 0.1 mm lines, but readability suffers below about 0.8 mm text.

**What goes wrong if you don't:** Designators and marks that can't be read, so assembly and rework take longer and mistakes get through.

**Applies to:** General practice; minimums vary by fab and printing method.

**Sources:** [“The PCB CAM Process w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/8226431-the-pcb-cam-process-w-dave-wilcox) (Mar 2021), [20:00](https://www.buzzsprout.com/1066066/episodes/8226431?t=1200)–26:00; [“An overview of bare PCB fabrication w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/6388663-an-overview-of-bare-pcb-fabrication-w-dave-wilcox) (Nov 2020), [56:00](https://www.buzzsprout.com/1066066/episodes/6388663?t=3360)–01:03:00; [“Mastering Vias: Plugging, Filling, and Best Practices”](https://www.buzzsprout.com/1066066/episodes/16036518-mastering-vias-plugging-filling-and-best-practices) (Nov 2024), [28:00](https://www.buzzsprout.com/1066066/episodes/16036518?t=1680)–30:00; fabs' published legend minimums (0.1–0.15 mm lines, 0.8–1.0 mm text).

*Last reviewed: 2026-11-08*

---

## PCB-DFM-040: Send only the legend you want printed, keep it off exposed copper, and expect the fab to clip and resize it

**Recommendation:** Export only the legend layers you mean to print: no component value or name layers unless you want them on the board.
Keep the legend off pads, exposed copper and holes, with a small clearance.
Expect the fab's CAM engineers to clip legend that runs over pads, holes or off the board, and to resize text too small to print: lots of small legend edits are normal.
They aim to keep it legible and printable, and they shouldn't move it; if they must, ask them to check with you first.

**Why:** Ink on a pad stops solder wetting it, so fabs clip any legend that crosses exposed copper.
Legend can't print over a hole or past the board edge either.
When a designator or polarity mark sits over copper, clipping can cut it in half, so place marks where they'll print whole.
Some design tools export value and name layers by default, which crowds the board with text nobody asked for.

**Typical values:** About 0.1 mm clearance from exposed copper and holes.

**What goes wrong if you don't:** Unreadable, clipped or missing marks, and a board that doesn't look like your design.

**Applies to:** General practice.

**Sources:** [“The PCB CAM Process w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/8226431-the-pcb-cam-process-w-dave-wilcox) (Mar 2021), [22:00](https://www.buzzsprout.com/1066066/episodes/8226431?t=1320)–24:00; [“An overview of bare PCB fabrication w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/6388663-an-overview-of-bare-pcb-fabrication-w-dave-wilcox) (Nov 2020), [56:00](https://www.buzzsprout.com/1066066/episodes/6388663?t=3360)–01:03:00; fabs' published legend clearances.

*Last reviewed: 2026-11-08*

---

## PCB-DFA-081: Leave legend out where it won't fit, but keep it complete in your data

**Recommendation:** Where the board is too dense for legible legend, such as around 0.4 mm-pitch BGAs or on very small boards, leave it off the printed board rather than squeezing it in.
Keep every designator and mark complete and correct in your design data anyway, and put them on the assembly drawing.
Check designators against the netlist and BOM, not by where the text happens to sit.

**Why:** Tiny legend can't be read and may be printed over pads.
The assembler and inspector still need to know which part goes where and which way round, and an assembly drawing gives them that without printing it on the board.
When designators are crowded, text drifts onto the wrong part, so only the data can be trusted.

**What goes wrong if you don't:** Illegible marks, legend over pads, or the wrong part placed because a designator sat beside the wrong footprint.

**Applies to:** General practice.

**Sources:** [“An Answering Your Questions Grab Bag”](https://www.buzzsprout.com/1066066/episodes/13847902-an-answering-your-questions-grab-bag) (Oct 2023), [29:00](https://www.buzzsprout.com/1066066/episodes/13847902?t=1740)–30:00; [“Mastering Vias: Plugging, Filling, and Best Practices”](https://www.buzzsprout.com/1066066/episodes/16036518-mastering-vias-plugging-filling-and-best-practices) (Nov 2024), [25:00](https://www.buzzsprout.com/1066066/episodes/16036518?t=1500)–29:30; [“All the Tricks and Gotchas in Surface Mount Assembly (Repost from the Coriolis Effect)”](https://www.buzzsprout.com/1066066/episodes/11006453-all-the-tricks-and-gotchas-in-surface-mount-assembly-repost-from-the-coriolis-effect) (Jul 2022), [49:00](https://www.buzzsprout.com/1066066/episodes/11006453?t=2940)–52:00.

*Last reviewed: 2026-11-08*

---

## PCB-DFM-045: Keep legend off vias, even tented ones

**Recommendation:** Place legend text and marks on flat solder mask, clear of vias.
This applies to tented vias as well as open ones.
If there's no other room, printing legend over tented vias is acceptable.
Avoid printing legend over open vias, because the fab will clip it.

**Why:** A tented via is covered by a thin film of solder mask, and that film sags a little into the hole.
Legend printed across the via follows the dip, so the character comes out slightly distorted.
It still prints and is usually legible, and a small mark such as a dot works fine.
An open via is different.
Legend can't print over a hole, and the fab keeps it back from exposed copper (PCB-DFM-040).
So the fab cuts the legend away around every open via, and a designator printed across a row of them is cut into pieces.

**Typical values:** Over tented vias, legend can come right up to the via, or even cross it: 0 mm is acceptable.
Over open vias, keep legend back from the exposed copper by the fab's clearance, which is about 0.1 mm (PCB-DFM-040).
The recommended position is on flat mask, clear of every via.

**What goes wrong if you don't:** Over tented vias, designators and marks that look uneven and are harder to read.
Over open vias, designators clipped into pieces or removed.

**Applies to:** General practice.
Whether a via is tented is set by your data and fab notes (PCB-DFM-030).

**Sources:** [“Small PCB layout decisions that have a significant impact on assembly”](https://www.buzzsprout.com/1066066/episodes/8957623-small-pcb-layout-decisions-that-have-a-significant-impact-on-assembly) (Aug 2021), [13:00](https://www.buzzsprout.com/1066066/episodes/8957623?t=780)–14:00; Chris Denney (author); [“The PCB CAM Process w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/8226431-the-pcb-cam-process-w-dave-wilcox) (Mar 2021), [22:00](https://www.buzzsprout.com/1066066/episodes/8226431?t=1320)–24:00.

![D68: Drawn to scale, three plan views of a 0603 resistor, R7, with three vias. Left: the designator sits beside the part on flat mask. Middle: the designator is printed across tented vias. Right: the vias are open and the designator is clipped around them. Below, an enlarged cross-section of a legend line across a tented via: the mask sags into the hole and the ink follows it.](images/legend-over-vias.svg)

*D68 is drawn to scale.
On the left, the designator sits on flat mask beside the part and prints cleanly.
In the middle, it is printed across tented vias: it prints, but the ink dips into each via, so the characters come out wavy and thinner there.
On the right, the vias are open, so the fab clips the legend back from their copper and the designator is cut into pieces.
The enlarged cross-section below shows why the middle case is distorted: the mask sags into the hole, and the legend ink follows it down.*

*Last reviewed: 2026-11-12*

---

## PCB-DFA-127: Turn legend text so it reads from only two edges of the board

**Recommendation:** Keep all horizontal designators and labels the same way round, reading left to right.
Where text has to turn 90° to fit, turn all of it the same way.
Reading from bottom to top is the most common choice.
It matches engineering drawings, where text reads from the bottom or the right-hand side of the sheet, and it's what a 90° turn gives in most design tools.
Then a person can read the whole board while holding it in one of only two ways: square on, or turned a quarter turn.
Avoid text that reads upside down, or that reads from top to bottom.
Bottom-side legend follows the same rule, as seen with the board turned over.

**Why:** Assemblers, inspectors and repair technicians read designators all day.
If the text faces all four directions, they have to keep turning the board, which is slow and handles it more.
Text read upside down is easy to misread, and some characters such as 6 and 9 swap meaning.
Turning a designator to match its part doesn't help, because a person matches a designator to its part by position, not by angle.

**What goes wrong if you don't:** Slower assembly, inspection and rework, and more misread designators.

**Applies to:** General practice.

**Sources:** Chris Denney (author); published silkscreen design guides, which recommend only 0° and 90° text, read from the bottom or right edge of the board; engineering drawing practice (the aligned system, with text read from the bottom or right-hand side).

![D69: Drawn to scale, two copies of the same area of a board with eight 0603 parts, some horizontal and some vertical. Left: horizontal designators read left to right and vertical ones read bottom to top, so the board reads from the bottom and right edges. Right: designators face all four ways, some upside down, so the board must be turned to all four sides.](images/legend-orientation.svg)

*D69 is drawn to scale.
On the left, every horizontal designator reads from the bottom edge, and every vertical one reads from the right edge.
A person only ever holds the board one of two ways.
On the right, the same designators face all four ways, so the board has to be turned to every side to read them.*

*Last reviewed: 2026-11-12*

---

## PCB-DFA-128: Use a callout box where parts are packed too tightly for their designators

**Recommendation:** Where a group of parts is packed too tightly to fit a designator beside each one, draw a legend box round the group.
Then draw a second box nearby, as a map of the group.
In the map, put each designator in the same position as its part, turned the same way.
Make the map larger than the group, so the designators can be 1 mm tall (PCB-DFM-039).
Put it as close to the group as you can, on the same side of the board.
Join the two boxes with a legend line.
Make the line as straight as you can, and where it has to bend, use 45° and 90° bends.
If there's no room for a map either, leave the designators off and put them on the assembly drawing (PCB-DFA-081).

**Why:** Groups of small parts, such as decoupling capacitors round a chip, often leave no room for their designators.
Designators squeezed in between the parts end up on pads, where the fab clips them, or beside the wrong part.
A callout box keeps every designator on the board and legible.
A person finds a part by matching its position in the group to the same position in the map.
The line between the boxes shows which map belongs to which group, which matters when a board has several.

**What goes wrong if you don't:** Designators clipped, unreadable or next to the wrong part, or left off the board, so everyone has to work from the assembly drawing.

**Applies to:** Dense areas, such as decoupling capacitors beside a BGA or QFN, or parts on the back of a BGA.

**Sources:** Chris Denney (author); published silkscreen design guides, which show designators grouped in a box and arranged to match the parts.

![D70: Drawn to scale, a QFN, U3, with eight 0402 capacitors packed 0.25 mm apart beside it. A legend box surrounds the capacitors. Beside it, a larger legend box holds their designators, C11 to C18, each in the same position and orientation as its capacitor, and a straight legend line joins the two boxes.](images/legend-callout-box.svg)

*D70 is drawn to scale.
The eight capacitors beside U3 are 0.25 mm apart, so there's no room for a designator beside each one.
A box round the group marks them, and the larger box beside it is a map: each designator sits where its capacitor sits in the group, and is turned the same way.
A straight legend line joins the two boxes.*

*Last reviewed: 2026-11-12*

---

## Related pages
- [Footprints and the component library](../01-design-package/04-footprints.md)
- [Assembly data](../01-design-package/02-assembly-data.md)
- [Solder mask](07-solder-mask.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

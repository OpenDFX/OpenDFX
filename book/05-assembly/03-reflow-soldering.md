# Reflow soldering

After placement, the board rides a conveyor through a reflow oven.
The oven heats the whole assembly along a set temperature profile until the paste melts, then cools it so the solder sets into joints.
A double-sided board goes through twice: the first side is built and reflowed, the board is flipped, and the second side is built and reflowed, with the first side's parts hanging underneath.

The assembler sets the oven profile for each job.
What your design controls is how evenly the board heats, which parts must survive the heat, and what happens to the first side during the second pass.

## PCB-DFA-024: On a double-sided board, put small, light parts on one side and heavy parts on the other

**Recommendation:** Put the small, light and fine-pitch parts (chips, ICs, small passives) on the side built first.
Put the heavy and bulky parts (large inductors, connectors, buzzers) on the side built second.
Put every part whose leads or pegs go through the board, such as a USB connector with through-hole support pins, on the second side, all together.
Check the datasheets of every part on the side that's reflowed twice (the side built first).
Some manufacturers recommend reflowing their parts only once.

**Why:** During the second reflow, the first side's solder melts again with its parts hanging upside down.
Surface tension holds small, light parts on; heavy parts fall off unless they're glued.
Pegs that poke through the board stop the stencil lying flat on the second side, so they can't be printed around unless they're all on the side printed last.
Grouping fine-pitch parts on one side also lets each side have the stencil thickness it needs (see [PCB-DFA-020](01-solder-paste-and-stencils.md)).

**Typical values:** A common rule of thumb: a part stays on during the second reflow if its weight divided by its total pad area is no more than about 30 g/in² (0.047 g/mm²).
Heavier parts on the first side need glue.

![D7: Drawn to scale, side view: a 1.6 mm board on its second pass through the oven. A heavy inductor, a connector with pegs through the board and a large capacitor face up on the second side; a QFN and small resistors and capacitors hang underneath on the first side.](images/double-sided-plan.svg)

*D7 is drawn to scale.
It shows a 1.6 mm board from the side, on its second pass through the reflow oven.
The side built second faces up and carries the heavy and bulky parts: a large inductor, a large capacitor and a connector whose pegs go through the board and poke out of the first side.
The side built first hangs underneath and carries only small, light parts, a QFN chip and small resistors and capacitors, which the surface tension of the melted solder holds in place.
A part on the first side stays on if its weight divided by its total pad area is no more than about 30 g/in² (0.047 g/mm²); heavier parts must be glued.*

**What goes wrong if you don't:** Each heavy part on the first side is glued, sometimes by hand on every board, which adds labor that doesn't get cheaper with volume.
Some assemblers have automated glue-dispensing equipment, but it's rare.
Parts with pegs on both sides may not be buildable by normal methods at all.

**Example:** One design needed a spring-loaded connector on one side and a USB connector with through-hole pegs on the other, because of the enclosure.
It was nearly impossible to build by normal methods; the assembler had to invent a special process.

**Applies to:** General practice.

**Sources:** [“Get to know Melissa and Chris”](https://www.buzzsprout.com/1066066/episodes/9253950-get-to-know-melissa-and-chris) (Sep 2021), [55:00](https://www.buzzsprout.com/1066066/episodes/9253950?t=3300)–57:00; [“What factors influence PCB quotes w/ Brett Babilonia”](https://www.buzzsprout.com/1066066/episodes/14580855-what-factors-influence-pcb-quotes-w-brett-babilonia) (Feb 2024), [25:00](https://www.buzzsprout.com/1066066/episodes/14580855?t=1500)–29:00; [“Stencils: The Unsung Heroes of PCB Perfection Pt.1”](https://www.buzzsprout.com/1066066/episodes/15448360-stencils-the-unsung-heroes-of-pcb-perfection-pt-1) (Jul 2024), [19:00](https://www.buzzsprout.com/1066066/episodes/15448360?t=1140)–20:00; “Component Candidacy of Second Side Reflow with Lead-Free Solder” (conference paper, 2006), which reports the weight-to-pad-area rule of thumb (checked Oct 2026 through summaries, not the full paper).

*Last reviewed: 2026-11-01*

---

## PCB-DFA-025: Don't put a few parts on the second side just because there's room

**Recommendation:** If the board can be single-sided, keep it single-sided.
If it has to be double-sided, use the same part numbers on both sides where you can.

**Why:** Every side is a separate pass through the printer, the placement machine and the oven, with its own stencil, program and handling.
A second side that uses different parts may need a whole second machine setup.

**Typical values:** A second side adds at least about 15 % to assembly cost, even when it has only two parts, both already used on the first side.
A second side with entirely different parts can double it (one assembler's estimate, as of 2024).

**What goes wrong if you don't:** You pay for a whole extra assembly pass for one or two parts.

**Example:** A board had one resistor on its bottom side, and plenty of room for it on the top.

**Applies to:** General practice.

**Sources:** [“What factors influence PCB quotes w/ Brett Babilonia”](https://www.buzzsprout.com/1066066/episodes/14580855-what-factors-influence-pcb-quotes-w-brett-babilonia) (Feb 2024), [29:00](https://www.buzzsprout.com/1066066/episodes/14580855?t=1740)–32:00.

*Last reviewed: 2026-11-01*

---

## PCB-DFA-026: Check that every part can survive a standard lead-free reflow, and flag any that can't

**Recommendation:** Check every part's datasheet for its maximum reflow temperature and number of reflow passes, and the bare board's material too.
Tell your assembler before the build about any part that can't take a standard lead-free profile, or that asks for an unusual one.
Never design batteries to go through reflow, wave or selective soldering; they're soldered by hand.
Through-hole parts that will be soldered in the reflow oven (pin-in-paste) need plastics rated for reflow temperatures.

**Why:** Lead-free solder (such as SAC305) melts at about 217 °C, and reflow profiles peak well above that, typically around 240–250 °C.
Most parts are rated for it, but some sensors, microphones, LEDs, small solar cells and connector plastics aren't, and a double-sided board puts every part through at least two passes.
The assembler only knows a part is special if someone reads its datasheet, and it's cheaper for that to be you.

**Typical values:** Most thin lead-free packages are rated for a 260 °C peak; thicker and larger packages are often rated lower (250 °C or 245 °C), per J-STD-020.
There is no single number of passes: every part sets its own, and so does the board's laminate.
Count the passes your build needs (two for a double-sided board, plus any rework) and check each part and the board against it.

**What goes wrong if you don't:** Parts damaged in the oven, found only when the first boards are tested, or melted connector housings.

**Example:** A tiny surface-mount solar cell was destroyed by a standard lead-free reflow; nobody had checked its datasheet.
A lower-temperature solder fixed it, and the rest of the build went fine.

**Applies to:** General practice.

**Sources:** [“Reflow soldering”](https://www.buzzsprout.com/1066066/episodes/6175423-reflow-soldering) (Nov 2020), [29:00](https://www.buzzsprout.com/1066066/episodes/6175423?t=1740)–31:00; [“The nitty gritty details on solder”](https://www.buzzsprout.com/1066066/episodes/11129008-the-nitty-gritty-details-on-solder) (Aug 2022), [44:00](https://www.buzzsprout.com/1066066/episodes/11129008?t=2640)–45:00; [“Benefits of intrusive soldering”](https://www.buzzsprout.com/1066066/episodes/10791130-benefits-of-intrusive-soldering) (Jun 2022), [02:00](https://www.buzzsprout.com/1066066/episodes/10791130?t=120) and [29:00](https://www.buzzsprout.com/1066066/episodes/10791130?t=1740)–30:00; J-STD-020 (moisture/reflow sensitivity classification, peak temperatures).

*Last reviewed: 2026-11-01*

---

## PCB-DFA-027: Spread the heat load: don't put huge parts right beside tiny ones

**Recommendation:** Where you can, avoid placing a very large part, such as a big aluminum electrolytic capacitor, right beside very small parts such as 0201s.
If the board needs both, expect the assembler to profile the oven with thermocouples on the largest and the smallest parts.

**Why:** A large part soaks up heat and acts as a heat sink, while a tiny part next to it heats much faster.
The smallest parts set the highest temperature the oven may reach; the largest set how long it must soak to bring them up to soldering temperature.
Modern convection ovens and a measured profile handle most boards, but the bigger the difference, the narrower the window.

**What goes wrong if you don't:** A narrower process window: joints on the large part that aren't fully melted, or small parts overheated to get there.

**Applies to:** General practice.
Usually a minor concern; the assembler profiles the oven for each board.

**Sources:** [“Reflow soldering”](https://www.buzzsprout.com/1066066/episodes/6175423-reflow-soldering) (Nov 2020), [28:00](https://www.buzzsprout.com/1066066/episodes/6175423?t=1680)–29:00.

*Last reviewed: 2026-11-01*

---

## PCB-DFA-028: Talk to your assembler first about very thin boards and large, heavy double-sided panels

**Recommendation:** If the board is thinner than about 0.6 mm, especially if it's double-sided, ask your assembler before you commit whether it needs a carrier or custom support tooling.
Do the same for large panels with heavy parts on both sides.

**Why:** Assembly equipment relies on the board being stiff enough to be its own tooling, which a standard 1.6 mm board is.
A very thin board flexes under the squeegee and the placement nozzle.
A single-sided thin board can often be taped to a stiff carrier; a double-sided one needs tooling shaped around the parts underneath.
A double-sided board rides through the oven on its edges, so a large, heavy panel sags, and in extreme cases falls off the rails.

**Typical values:** 1.6 mm: standard · under about 0.6 mm: a conversation first · 0.2–0.4 mm: custom tooling likely if double-sided.

**What goes wrong if you don't:** Tooling charges and delays you didn't plan for, or poor print and placement quality.

**Applies to:** Varies by manufacturer.
Check with yours.

**Sources:** [“Custom tooling to the rescue”](https://www.buzzsprout.com/1066066/episodes/10804740-custom-tooling-to-the-rescue) (Jul 2022), [08:00](https://www.buzzsprout.com/1066066/episodes/10804740?t=480)–11:00; [“Advanced Drilling w/ CAM Engineer, Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/10611991-advanced-drilling-w-cam-engineer-dave-wilcox) (May 2022), [01:16:00](https://www.buzzsprout.com/1066066/episodes/10611991?t=4560).

*Last reviewed: 2026-11-01*

---

## Related pages
- [Solder paste printing and stencils](01-solder-paste-and-stencils.md)
- [Component placement](02-component-placement.md)
- [Clearance near board and panel edges](../02-the-panel/04-edge-clearance.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

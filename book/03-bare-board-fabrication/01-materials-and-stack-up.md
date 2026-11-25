# Materials and stack-up

A circuit board is a sandwich: layers of copper foil separated by glass-weave laminate (cores) and bonding sheets (prepreg), pressed together under heat.
The stack-up is the recipe for that sandwich: how many copper layers, how thick each copper and dielectric layer is, and what material it's made of.
It sets the board's thickness, its stiffness, how it behaves in the reflow oven, and the impedance of every trace.

Most boards need nothing unusual here.
The recommendations below are about not asking for more than you need, and saying clearly what you do need.

## PCB-DFM-017: Use standard FR-4 unless the product needs something else

**Recommendation:** Specify standard FR-4 epoxy-glass laminate unless your product has a real need for something else: sustained high temperature, very high frequencies, or a customer requirement.
If you need a particular material or certification, name it by its IPC-4101 specification sheet (the "slash sheet") and confirm with your fab that they stock it.

**Why:** Standard materials are in stock at every fab, in every thickness.
Exotic laminates can take about eight weeks to arrive and come with minimum order quantities, and some are harder to drill, plate and laminate.
Tg (glass transition temperature) is the temperature at which the laminate starts to soften; a higher-Tg material stays stiffer and flatter through reflow, rework and hot service.
UL flammability approval belongs to a particular fab's process with a particular material, so a different material or a custom build may not carry it.

**Typical values:** Standard FR-4 has a Tg of about 135 °C; mid-Tg is about 150 °C and high-Tg about 170 °C.
Fabs don't treat mid- or high-Tg as standard, and it usually costs more.
If you don't specify Tg, expect the cheapest material, most likely about 135 °C, but the fab may use anything reasonable it has on the shelf.
So if your product needs mid- or high-Tg, say so on the drawing; if it doesn't, don't pay for it.

**What goes wrong if you don't:** Weeks added to the lead time and a higher price for a material the product didn't need; or, the other way round, a board that softens and warps in a hot product.

**Applies to:** General practice.

**Sources:** [“Bare PCB Materials w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/7558222-bare-pcb-materials-w-dave-wilcox) (Feb 2021), [11:00](https://www.buzzsprout.com/1066066/episodes/7558222?t=660)–18:00, [31:00](https://www.buzzsprout.com/1066066/episodes/7558222?t=1860)–35:00 and [57:00](https://www.buzzsprout.com/1066066/episodes/7558222?t=3420)–58:00; IPC-6012F (Sept 2023), Table 1-2 (default material: epoxy-glass laminate); a fab-industry engineer, via Chris Denney (author).

*Last reviewed: 2026-11-07*

---

## PCB-DFM-018: Start from your fab's standard stack-up, or give them what they need to build one

**Recommendation:** Use your fab's standard stack-up for your layer count and thickness if it meets your needs.
If you need a custom one (for controlled impedance, say), don't work it out alone: give the fab the signal frequencies, the target impedances, which layers each impedance trace runs on and references, and how much the material may cost, and let their engineers propose the stack-up before you place the order.

**Why:** The fab knows which cores and prepregs it actually stocks, and how much each one thins when it's pressed.
A stack-up built from someone else's materials list will be adjusted anyway.
Fabs are allowed to tune dielectric thicknesses (by about ±20%) to hit a stated impedance, but a large change should come back to you for approval.

**Typical values:**
- Minimum dielectric thickness between copper layers, when the drawing doesn't say: 65 µm (2.56 mil) under IPC-6012F.
  Older guidance, including IPC-6012E, gave 3.5 mil (90 µm).
- One sheet of prepreg between the outer layer and the next layer is fine for most boards; use two for products that will see heavy shock and vibration.
- Avoid stacking more than three sheets of prepreg in one gap.

**What goes wrong if you don't:** A stack-up that can't be built from stock material, a week lost going back and forth, or impedances that are off because the fab had to change your dielectrics.

**Applies to:** Varies by manufacturer; standard stack-ups are fab-specific.

**Sources:** [“Understanding Controlled Impedance w/ NCAB Group Field Application Engineer, Ryan Miller”](https://www.buzzsprout.com/1066066/episodes/11631934-understanding-controlled-impedance-w-ncab-group-field-application-engineer-ryan-miller) (Nov 2022), [19:00](https://www.buzzsprout.com/1066066/episodes/11631934?t=1140)–20:00 and [25:00](https://www.buzzsprout.com/1066066/episodes/11631934?t=1500)–29:00; [“Impedance Control Demo w/ NCAB Group Field Application Engineer Ryan Miller”](https://www.buzzsprout.com/1066066/episodes/13789746-impedance-control-demo-w-ncab-group-field-application-engineer-ryan-miller) (Oct 2023), [28:00](https://www.buzzsprout.com/1066066/episodes/13789746?t=1680)–30:00, [01:03:00](https://www.buzzsprout.com/1066066/episodes/13789746?t=3780)–01:05:00 and [01:12:00](https://www.buzzsprout.com/1066066/episodes/13789746?t=4320)–01:18:00; [“Our top suggestions for customers w/ CircuitHub Account Manager, John Jacquinet”](https://www.buzzsprout.com/1066066/episodes/8884604-our-top-suggestions-for-customers-w-circuithub-account-manager-john-jacquinet) (Jul 2021), [44:00](https://www.buzzsprout.com/1066066/episodes/8884604?t=2640); IPC-6012F (Sept 2023), Table 1-2.

*Last reviewed: 2026-11-07*

---

## PCB-DFM-019: Specify controlled impedance fully, make the traces easy to find, and leave room to widen them

**Recommendation:** For every controlled-impedance requirement, state on the fabrication drawing:
- the structure (for example, surface microstrip, embedded stripline, edge-coupled differential pair, coplanar waveguide with ground);
- the layer the trace is on and the layers it references;
- the target impedance and its tolerance;
- the trace width and spacing you designed with.

Give impedance traces an unusual width, such as 0.159 mm (6.25 mil) instead of 0.15 mm, so the fab can find them among all the other traces.
Leave space beside them, so the fab can widen them if their materials need it.
Calculate your own design to within about 1% of the target before you send it.

**Why:** Gerbers show trace widths, not which traces are impedance-controlled.
An odd width lets the fab select every impedance trace at once.
Etching leaves traces narrower at the top than the bottom, and the fab adjusts widths and dielectrics to suit its own materials; if the traces are hemmed in, they can't.

**Typical values:** Tolerance ±10% is common; ±5% costs more.
Common targets: 50 Ω single-ended, 90 or 100 Ω differential.
Ask for a TDR test of the impedance coupon, or the fab's stack-up calculation, if you want proof.

**What goes wrong if you don't:** Traces that can't reach the impedance you need, discovered after the board is built.

**Example:** A board revision added an 85 Ω differential pair in a space that allowed only 3 mil traces with 3 mil gaps; the impedance was physically unachievable in that space, and the design sat stuck for over a week.

**Applies to:** General practice.

**Sources:** [“Impedance Control Demo w/ NCAB Group Field Application Engineer Ryan Miller”](https://www.buzzsprout.com/1066066/episodes/13789746-impedance-control-demo-w-ncab-group-field-application-engineer-ryan-miller) (Oct 2023), [15:00](https://www.buzzsprout.com/1066066/episodes/13789746?t=900)–25:00, [35:00](https://www.buzzsprout.com/1066066/episodes/13789746?t=2100)–37:00, [45:00](https://www.buzzsprout.com/1066066/episodes/13789746?t=2700)–49:00 and [01:10:00](https://www.buzzsprout.com/1066066/episodes/13789746?t=4200)–01:11:00; [“Understanding Controlled Impedance w/ NCAB Group Field Application Engineer, Ryan Miller”](https://www.buzzsprout.com/1066066/episodes/11631934-understanding-controlled-impedance-w-ncab-group-field-application-engineer-ryan-miller) (Nov 2022), [17:00](https://www.buzzsprout.com/1066066/episodes/11631934?t=1020)–19:00, [37:00](https://www.buzzsprout.com/1066066/episodes/11631934?t=2220)–38:00 and [42:00](https://www.buzzsprout.com/1066066/episodes/11631934?t=2520)–51:00; see also [PCB-DFM-014](../01-design-package/01-fabrication-data.md#pcb-dfm-014-put-everything-the-gerbers-cant-say-on-the-fabrication-drawing).

*Last reviewed: 2026-11-07*

---

## PCB-DFM-020: Size traces and gaps for the finished copper weight

**Recommendation:** Set your trace width and spacing rules for the copper weight the board will really have, and set the clearance from copper pours to the same values.

**Why:** Copper is etched from the side as well as from the top, so thicker copper needs wider gaps to etch cleanly.
Outer layers also gain plated copper on top of the foil.
A pour clearance left at a tight default undoes every other rule.

**Typical values:**

| Finished copper | Minimum trace and space | Recommended |
|---|---|---|
| 1 oz (35 µm) | 0.1 mm (4 mil) | 0.15 mm (6 mil) |
| 2 oz (70 µm) | 0.2 mm (8 mil) | 0.25 mm (10 mil) |

On 2 oz copper, 6 mil can be built, but with very poor yield, so avoid it.
Finer than about 0.075 mm (3 mil) needs thinner starting foil and a fab that specializes in it.

**What goes wrong if you don't:** Shorts and opens, lower yield, X-outs, and a higher price; heavy-copper boards drawn to 1 oz rules may not be buildable at all.

**Example:** A motor controller needed 2 oz copper for its current but was laid out with fine 1 oz rules; the fab's advice was to open trace and gap up to 8 mil.
On another board, trace and space were set to 6 mil, but the pour clearance was left at 2 mil.

**Applies to:** General practice; exact capability varies by fab.

**Sources:** [“An overview of bare PCB fabrication w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/6388663-an-overview-of-bare-pcb-fabrication-w-dave-wilcox) (Nov 2020), [01:01:00](https://www.buzzsprout.com/1066066/episodes/6388663?t=3660)–01:03:00; [“The PCB CAM Process w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/8226431-the-pcb-cam-process-w-dave-wilcox) (Mar 2021), [43:00](https://www.buzzsprout.com/1066066/episodes/8226431?t=2580)–46:00; [“Inner Layer Production w/ CAM Engineer Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/9018673-inner-layer-production-w-cam-engineer-dave-wilcox) (Aug 2021), [01:09:00](https://www.buzzsprout.com/1066066/episodes/9018673?t=4140)–01:11:00; [“Advanced Drilling w/ CAM Engineer, Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/10611991-advanced-drilling-w-cam-engineer-dave-wilcox) (May 2022), [37:00](https://www.buzzsprout.com/1066066/episodes/10611991?t=2220)–38:00; [“Outer Layer Imaging w/ CAM Engineer Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/11724857-outer-layer-imaging-w-cam-engineer-dave-wilcox) (Nov 2022), [41:00](https://www.buzzsprout.com/1066066/episodes/11724857?t=2460)–45:00; [“An Answering Your Questions Grab Bag”](https://www.buzzsprout.com/1066066/episodes/13847902-an-answering-your-questions-grab-bag) (Oct 2023), [07:00](https://www.buzzsprout.com/1066066/episodes/13847902?t=420); Chris Denney (author).

*Last reviewed: 2026-11-07*

---

## PCB-DFM-021: Use as few layers as the circuit needs

**Recommendation:** Use two layers when the circuit genuinely allows it, and add layers only when routing, power or signal integrity need them.

**Why:** Every extra pair of layers adds lamination, drilling depth, registration risk and cost.
Above about 12 to 16 layers, many fabs reach the limit of their equipment and need very thin cores and tighter process control.

**What goes wrong if you don't:** A higher price and a longer lead time than the board needed; at high layer counts, fewer fabs that can build it.

**Applies to:** General practice.

**Sources:** [“Inner Layer Production w/ CAM Engineer Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/9018673-inner-layer-production-w-cam-engineer-dave-wilcox) (Aug 2021), [06:00](https://www.buzzsprout.com/1066066/episodes/9018673?t=360)–11:00.

*Last reviewed: 2026-11-07*

---

## PCB-DFA-073: Expect thin boards to need a carrier during assembly

**Recommendation:** Choose the board thickness the product needs; any thickness can be assembled, even double-sided flexible boards.
For boards 0.6 mm or thinner, expect the assembler to run them on a carrier (a rigid tray that holds the board through printing, placement and reflow), and ask what it costs.

**Why:** Thin boards sag on conveyors and under the stencil, and warp in the oven.
A carrier holds them flat, but it has to be made for the board.

**Typical values:** 0.6 mm or thinner: carrier needed.
About 0.8 mm: sometimes needed.
1.0 mm and thicker: generally not needed.

**What goes wrong if you don't:** A carrier charge and lead time you didn't plan for.

**Applies to:** Varies by assembler; thresholds from Worthington Assembly and CircuitHub (2026).

**Sources:** Chris Denney (author); [“Advanced Drilling w/ CAM Engineer, Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/10611991-advanced-drilling-w-cam-engineer-dave-wilcox) (May 2022), [01:15:00](https://www.buzzsprout.com/1066066/episodes/10611991?t=4500)–01:17:00 (older, stricter limits).

*Last reviewed: 2026-11-07*

---

## Related pages
- [Fabrication data](../01-design-package/01-fabrication-data.md)
- [Drilling](03-drilling.md)
- [Why boards are built in panels](../02-the-panel/01-why-panels.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

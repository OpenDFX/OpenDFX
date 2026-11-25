# Static (ESD) protection

Static electricity is made whenever two materials touch and then separate.
Walking across a floor does it.
So does peeling tape off a roll, sliding a board into a bag or shuffling paper.
A discharge you can see, such as the spark from a doorknob, is already about 3,000 V.
Many semiconductors can be damaged by less than 100 V, so a part can be harmed by a discharge nobody felt.
Some damage kills the part at once.
Other damage only weakens it, and the board passes test and fails later in the field.
Assemblers control static inside the factory.
This page is about what happens to boards before and after they're in a controlled area: how they're packed, and how they're handled once they reach you.

## PCB-DFA-109: Ship and store assembled boards in static-shielding bags, not in plain anti-static bags

**Recommendation:** Put every assembled board that carries semiconductors in a static-shielding bag for shipping and storage.
Use a metallized shielding bag, usually silver-gray and slightly see-through, and close it by folding the top over and taping it.
Wrap the board in anti-static (usually pink) bubble wrap first, because that is safe against the board, and then put it in the shielding bag, as in D65.
Don't rely on a pink or blue anti-static bag on its own.
Never put boards or loose semiconductors in an ordinary plastic bag.
Boards that carry no semiconductors, such as a board with only connectors and passive parts, can ship in anti-static bubble wrap alone if you agree it with your assembler.

**Why:** Packaging can do three different jobs.
An anti-static (low-charging) material doesn't build up much charge itself when it rubs against the board.
A dissipative material lets any charge drain away slowly.
A shielding material has a metal layer that stops a discharge from outside reaching the board inside, like a Faraday cage.
A pink anti-static bag does only the first job.
If a charged hand or box touches it, the discharge goes straight through to the board.
ANSI/ESD S541, the static control packaging standard, says that inside a static-controlled area, packaging must be low-charging and dissipative or conductive.
Outside that area, in a warehouse, a truck or your office, it must also shield.
A shielding bag only shields while it is closed and has no holes.
An ordinary plastic bag is worse than nothing, because it makes static every time it moves.

**Typical values:** A discharge you can see is about 3,000 V.
Many semiconductors are damaged by less than 100 V, and some by far less.
The ESD Association's tests for shielding bags are ANSI/ESD STM11.31 for discharge shielding and STM11.11 for surface resistance.

**What goes wrong if you don't:** Boards arrive working, or seem to, and then fail weeks or months later.
That kind of failure is very hard to trace back to how the boards were packed.

**Example:** A maker of underwater robots found that a board damaged by static in transit might work for about six months before it failed.
An assembler's shipping team packs every board in anti-static bubble wrap and then a shielding bag.
The only exceptions are a few customers whose boards carry only through-hole connectors and no semiconductors, and who asked for bubble wrap alone.

![D65: Cross-section of two packed boxes, drawn to scale. Left, marked good: a 100 mm board 1.6 mm thick with parts on top is wrapped in pink anti-static bubble wrap, then sealed in a metallized static-shielding bag whose top is folded over and taped, in a corrugated box with paper filler above and below. A spark from outside the box stops at the shielding bag. Right, marked avoid: the same board in a pink anti-static bag on its own, and the spark passes through the bag to the board.](images/packed-board.svg)

*D65 is drawn to scale, except that the bags are drawn thicker than they are.
The pink bubble wrap touches the board, and the shielding bag goes round the outside.
A pink anti-static bag on its own makes little static, but it doesn't stop a discharge from outside.*

**Applies to:** General practice.

**Sources:** ["How to Protect PCBs from ESD Damage"](https://www.buzzsprout.com/1066066/episodes/10275936-how-to-protect-pcbs-from-esd-damage) (Mar 2022), [07:00](https://www.buzzsprout.com/1066066/episodes/10275936?t=420)–08:00 and [16:00](https://www.buzzsprout.com/1066066/episodes/10275936?t=960)–22:00; ["How to safely and successfully ship assembled PCBs w/ Nicole Poirier"](https://www.buzzsprout.com/1066066/episodes/8309835-how-to-safely-and-successfully-ship-assembled-pcbs-w-nicole-poirier) (Apr 2021), [10:00](https://www.buzzsprout.com/1066066/episodes/8309835?t=600)–13:00; ["How Blue Robotics is enabling the next generation of ocean exploration robots w/ Rustom Jehangir"](https://www.buzzsprout.com/1066066/episodes/8139597-how-blue-robotics-is-enabling-the-next-generation-of-ocean-exploration-robots-w-rustom-jehangir) (Mar 2021), [49:00](https://www.buzzsprout.com/1066066/episodes/8139597?t=2940)–52:00; ["The PCB assembly process"](https://www.buzzsprout.com/1066066/episodes/4364141-the-pcb-assembly-process) (Jun 2020), [40:00](https://www.buzzsprout.com/1066066/episodes/4364141?t=2400); ESD Association, *ESD Fundamentals*, Part 1 (sensitivity and latent failure) and Part 3 (packaging and material handling containers), esda.org; ANSI/ESD S541, *Packaging Materials for ESD Sensitive Items*.

*Last reviewed: 2026-11-12*

---

## PCB-DFA-110: Open and handle boards only at a grounded workstation, and hold them by the edges

**Recommendation:** Wherever your boards are unpacked, tested or fitted into the product, set up a grounded workstation.
At the least, that means a static-dissipative mat, a wrist strap and a cord to a known ground.
Open the shielding bag on the mat, and keep the board on the mat until it is inside its enclosure.
Keep cardboard, paper and ordinary plastic off the mat.
Hold boards by their edges, and touch the plastic bodies of parts rather than their leads or solder joints.
Tell everyone who handles your boards to do the same, including your own customers if they receive bare boards.

**Why:** A person is the most common source of a damaging discharge.
A wrist strap and a grounded mat keep the person, the mat and the board at the same voltage, so no discharge can pass between them.
The cord of a wrist strap has a resistor built in, most commonly 1 MΩ, so that the wearer isn't directly connected to ground.
Charge reaches a part through its metal leads and the copper joined to them, so holding a board by its edges keeps your fingers away from that path.
Once a board is inside its enclosure, it is far less exposed, because hands no longer touch its joints.

**Typical values:** A complete mat kit with a wrist strap and grounding cord costs about $50 (2022 price).
The resistor in a wrist strap cord is most commonly 1 MΩ.
Don't wear a wrist strap when working on circuits at 250 V or more.

**What goes wrong if you don't:** Boards your assembler built and shipped correctly are damaged on your own bench.
They fail in the field, and the failure looks like a manufacturing defect.

**Applies to:** General practice, wherever boards are handled outside an assembler's static-controlled area.

**Sources:** ["How to Protect PCBs from ESD Damage"](https://www.buzzsprout.com/1066066/episodes/10275936-how-to-protect-pcbs-from-esd-damage) (Mar 2022), [39:00](https://www.buzzsprout.com/1066066/episodes/10275936?t=2340)–40:00 and [50:00](https://www.buzzsprout.com/1066066/episodes/10275936?t=3000)–52:00; ["Inevitable Failures"](https://www.buzzsprout.com/1066066/episodes/17722984-inevitable-failures) (Aug 2025), [19:00](https://www.buzzsprout.com/1066066/episodes/17722984?t=1140)–21:00; ESD Association, *ESD Fundamentals*, Part 3 (wrist straps and workstations), esda.org.

*Last reviewed: 2026-11-12*

---

## PCB-DFA-111: Choose an assembler with a documented static control program, such as one that meets ANSI/ESD S20.20

**Recommendation:** When you choose an assembler, ask whether it runs a written static control program.
Ask whether that program follows ANSI/ESD S20.20, or the equivalent IEC 61340-5-1, and how it is checked.

**Why:** Static control only works as a complete system.
Grounded floors need grounded footwear, and wrist straps and mats need to be tested.
S20.20 sets out what a program must contain: a written plan, training, grounding of people and equipment, packaging, marking and regular checks.
An assembler that follows it can show you the plan and its test records.

**Typical values:** In a typical program, people check their wrist straps or footwear at least once a day.
Floors, mats and workstations are tested on a regular schedule.

**What goes wrong if you don't:** Boards are damaged before they ever leave the factory, and nobody can tell you how or when.

**Applies to:** General practice.

**Sources:** ["How to Protect PCBs from ESD Damage"](https://www.buzzsprout.com/1066066/episodes/10275936-how-to-protect-pcbs-from-esd-damage) (Mar 2022), [12:00](https://www.buzzsprout.com/1066066/episodes/10275936?t=720)–13:00 and [41:00](https://www.buzzsprout.com/1066066/episodes/10275936?t=2460)–44:00; ["ESD Flooring w/ SelecTech CEO Tom Ricciardelli"](https://www.buzzsprout.com/1066066/episodes/13534129-esd-flooring-w-selectech-ceo-tom-ricciardelli) (Sep 2023), [19:00](https://www.buzzsprout.com/1066066/episodes/13534129?t=1140)–21:00; ANSI/ESD S20.20, *Protection of Electrical and Electronic Parts, Assemblies and Equipment*; ESD Association, *ESD Fundamentals*, Part 2 and Part 3, esda.org.

*Last reviewed: 2026-11-12*

---

## PCB-DFA-112: Put ESD protection on every connector that people or cables can touch, as close to the connector as you can

**Recommendation:** Give every signal that reaches a connector, button or other exposed metal its own ESD protection device, usually a TVS diode array.
Place the device as close to the connector as your design rules allow.
Route each protected line straight from the connector pin to the protection device's pin, with no via between them and no branch.
Then route on to the chip being protected.
Connect the protection device's ground pin to the ground plane through the shortest path you can, with its own via or vias.
Keep unprotected traces away from the short stretch between the connector and the protection device.
Choose a device rated for at least the IEC 61000-4-2 level your product must pass.

**Why:** Once a board is in a product, the connectors are where static gets in.
A user touches a USB plug, or a cable that has picked up charge is plugged in.
The protection device clamps the voltage and steers the current to ground before it reaches the chip.
An ESD pulse rises in less than a nanosecond, so even a tiny inductance in the path adds a large voltage.
That is why the device must be close to the connector and well grounded.
If the chip is close to the connector and the protection device is further away, the current takes the path to the chip instead.
This can only be done while laying out the board.
A board without room for protection devices near its connectors can't have them added later.

**Typical values:** IEC 61000-4-2 Level 4 is 8 kV by contact discharge and 15 kV through the air.
In an 8 kV contact discharge, the current rises at about 40 A per nanosecond.
At that rate, 0.25 nH of inductance in the path adds about 10 V to the voltage the chip sees.
As a common rule of thumb, a thin trace has an inductance of about 1 nH for each millimeter of length.
A via through a 1.6 mm board has an inductance of about 1 nH.

**What goes wrong if you don't:** Products fail ESD testing for certification, or fail in the field after a user touches a connector.
Moving or adding protection devices then means a new revision of the board.

**Applies to:** Products with connectors, buttons or exposed metal that users touch.

**Sources:** Texas Instruments, *ESD Protection Layout Guide*, SLVA680A (Feb 2015, revised Apr 2022), section 2; IEC 61000-4-2, *Electrostatic discharge immunity test*.

*Last reviewed: 2026-11-12*

---

## Related pages
- [Moisture and storage](02-moisture-and-storage.md)
- [Packaging and shipping assembled boards](03-packaging-and-shipping.md)
- [Consignment and spares](../04-components-and-materials/05-consignment-and-spares.md) (PCB-DFA-102, packing consigned parts)
- [Rework](../05-assembly/11-rework.md) (PCB-DFA-063, returning boards)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

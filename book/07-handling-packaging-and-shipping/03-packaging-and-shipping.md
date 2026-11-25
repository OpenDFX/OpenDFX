# Packaging and shipping assembled boards

Most assembled boards travel at least twice.
They go from the assembler to you, and often on to a test house, a coating house or your own customer.
Some come back for repair.
Each trip is a chance for static, a crushed box or a customs hold-up to undo good work.
Packing is the assembler's job, but the designer decides things that make it easy or hard: parts that hang over the board edge, very heavy boards, and whether boards ship in the panel.

## PCB-DFA-114: Agree with your assembler how boards will be packed: in the panel or separated, how many to a bag, and in what box

**Recommendation:** Before the first order ships, agree with your assembler how the boards will be packed.
Say whether you want them in the panel or separated.
Say how many boards go in each bag, and whether each board is wrapped on its own.
For heavy boards, or boards going a long way, ask for a double-wall box and foam lining.
If boards will go from the assembler to another company first, such as a coating or cleaning house, say where they go and how they should be packed for that trip.
For boards with parts that hang over the edge, such as an antenna or a connector, ask whether they should ship in the panel to protect those parts.
If your assembler is close by and you order often, ask about reusable static-safe boxes with partitions.

**Why:** The assembler packs to a standard method unless told otherwise.
That suits most boards, but not all of them.
Heavy parts near the edge of a board can break off in transit if the box isn't lined.
A part hanging over the edge can snap off during depaneling or in the box (PCB-DFA-010).
Leaving boards in the panel protects those parts, but then you must separate them yourself.
Boards that go on to another company must be packed for a second trip, and it may cost less to ship them there directly.
Reusable partitioned boxes protect boards well and cut out most of the single-use packing.

**Typical values:** The usual pack is anti-static bubble wrap against the board, inside a static-shielding bag (PCB-DFA-109), in a box with filler, as in D65.
A single-wall box is usual for light boards sent within one country.

**What goes wrong if you don't:** Boards arrive with broken parts, or in a form you didn't expect, such as still in the panel when you wanted them separated.

**Example:** One board carried a radio module with its antenna hanging off the board edge, held to the panel only by a breakaway tab underneath.
Separating it without snapping the antenna off took several people.
It didn't always succeed.

**Applies to:** General practice; agree it once for each product.

**Sources:** ["How to safely and successfully ship assembled PCBs w/ Nicole Poirier"](https://www.buzzsprout.com/1066066/episodes/8309835-how-to-safely-and-successfully-ship-assembled-pcbs-w-nicole-poirier) (Apr 2021), [07:00](https://www.buzzsprout.com/1066066/episodes/8309835?t=420)–09:00, [12:00](https://www.buzzsprout.com/1066066/episodes/8309835?t=720)–17:00 and [34:00](https://www.buzzsprout.com/1066066/episodes/8309835?t=2040)–36:00; ["What factors influence PCB quotes w/ Brett Babilonia"](https://www.buzzsprout.com/1066066/episodes/14580855-what-factors-influence-pcb-quotes-w-brett-babilonia) (Feb 2024), [50:00](https://www.buzzsprout.com/1066066/episodes/14580855?t=3000)–51:00; ["IPC's Leadership on Sustainability in Electronics w/ Dr. John W. Mitchell and Dr. Kelly Scanlon"](https://www.buzzsprout.com/1066066/episodes/16624642-ipc-s-leadership-on-sustainability-in-electronics-w-dr-john-w-mitchell-and-dr-kelly-scanlon) (Feb 2025), [18:00](https://www.buzzsprout.com/1066066/episodes/16624642?t=1080).

*Last reviewed: 2026-11-12*

---

## PCB-DFA-115: For international shipments, give the right tariff code, a plain description of the goods and a contact telephone number

**Recommendation:** When boards or parts cross a border, work out the correct tariff code for them with your assembler or customs broker.
Choose the code from what the boards are for in the end product, not from a quick search for "circuit board".
Use a different code for boards returned for repair or under warranty.
On the customs paperwork, also write a plain description of what is in the box and why it is being sent.
For a return, say that it is a repair return of no commercial value, and give the tracking number of the original shipment.
Give a telephone number that someone will answer.
Before you send parts in from abroad, agree with your assembler who pays the duties and taxes.

**Why:** Customs officers read the paperwork, not just the codes.
The tariff system classifies an assembled board mostly by the kind of equipment it goes into.
A code chosen from a search can sit under the wrong heading, and that holds the shipment up.
A repair return sent without the right code or note can be charged duty a second time.
When customs has a question, they call the number on the paperwork, and an unanswered call means a held shipment.

**Typical values:** Bare boards and assembled boards fall under different tariff headings.
Bare boards come under heading 8534.
Assembled boards usually come under the heading for parts of the equipment they go into, which depends on the product.
Codes, duty rates and rules change, so check them for every new product and from time to time after that.

**What goes wrong if you don't:** Shipments sit in customs for days, you pay duty you didn't owe, or a delivery date you promised is missed.

**Example:** An assembler once picked a code for "assembled circuit board" from a search.
It later found the code sat several levels down under a heading for nuclear equipment.

**Applies to:** International shipments; rules vary by country and change over time.

**Sources:** ["How to safely and successfully ship assembled PCBs w/ Nicole Poirier"](https://www.buzzsprout.com/1066066/episodes/8309835-how-to-safely-and-successfully-ship-assembled-pcbs-w-nicole-poirier) (Apr 2021), [25:00](https://www.buzzsprout.com/1066066/episodes/8309835?t=1500)–29:00 and [44:00](https://www.buzzsprout.com/1066066/episodes/8309835?t=2640)–50:00; ["The Open Source Ventilator Project with Dugan Karnazes and Nadim Conti"](https://www.buzzsprout.com/1066066/episodes/5109637-the-open-source-ventilator-project-with-dugan-karnazes-and-nadim-conti) (Aug 2020), [36:00](https://www.buzzsprout.com/1066066/episodes/5109637?t=2160); ["How to Send Consigned Material to Your CM"](https://www.buzzsprout.com/1066066/episodes/10182930-how-to-send-consigned-material-to-your-cm) (Mar 2022), [46:00](https://www.buzzsprout.com/1066066/episodes/10182930?t=2760)–48:00; Harmonized System heading 8534 (printed circuits) and US Customs rulings classifying printed circuit assemblies by end use.

*Last reviewed: 2026-11-12*

---

Boards sent back for repair are covered by [PCB-DFA-063](../05-assembly/11-rework.md): get a return number first, and pack the boards the way they came to you.

## Related pages
- [Static (ESD) protection](01-static-protection.md)
- [Breakaway methods](../02-the-panel/03-breakaway-methods.md) (PCB-DFA-010, parts that hang over the edge)
- [Rework](../05-assembly/11-rework.md) (PCB-DFA-063, returns)
- [Consignment and spares](../04-components-and-materials/05-consignment-and-spares.md) (PCB-DFA-101 to 104, sending parts in)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

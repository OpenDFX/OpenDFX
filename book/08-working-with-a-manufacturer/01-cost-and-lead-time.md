# What drives cost and lead time

Most of the cost of an assembled board is decided in layout, long before anyone asks for a quote.
Most delays are decided by how quickly questions get answered, and by when orders are placed.
This page gathers the cost drivers that earlier parts of the book cover one by one, and adds what a designer or buyer can do about price and schedule when ordering.
Prices on this page are examples from particular dates, and will change.

## PCB-DFA-116: Know what drives the price of an assembly, and design with it in mind

**Recommendation:** Before you release a design, check it against the cost drivers in the table below.
Each one has its own recommendation elsewhere in the book.
Where the product needs one of them, keep it, but know that you are paying for it.
Where it doesn't, design it out.

**Why:** An assembler's price is mostly set-up time and labor.
Set-up is paid once for each batch, so it matters most on small orders.
Labor is paid for every board, so it matters most on large orders.
Anything that adds a machine set-up, a manual step or a slower process adds cost.

**Typical values:**

| Cost driver | Why it costs more | Where it's covered |
|---|---|---|
| Many unique BOM lines | Each unique part takes about 3 to 5 minutes to load onto a feeder, however few boards you build. | [PCB-DFA-072](../01-design-package/03-bom.md) |
| Parts on both sides | A second side costs at least 15% more, even if it carries only two passive parts already used on the top. It can cost about twice as much if the bottom parts are all different from the top. | [PCB-DFA-024 and 025](../05-assembly/03-reflow-soldering.md) |
| Through-hole parts | Each one is placed and soldered by hand or on a separate machine. | [PCB-DFA-039](../05-assembly/05-through-hole-soldering.md) |
| Parts in tubes or loose | They're slower to load and to place than parts on tape. | [PCB-DFA-089](../04-components-and-materials/02-packaging.md) |
| Very small or very fine-pitch parts | They need tighter process control and more inspection, and fail more often. | [PCB-DFA-021 and 022](../05-assembly/02-component-placement.md) |
| Hardware such as heatsinks, screws and brackets | Each piece is fitted by hand. | [PCB-DFA-048](../05-assembly/06-press-fit-and-mechanical.md) |
| Conformal coating | It needs masking, coating and inspection, usually by hand. | [PCB-DFA-061](../05-assembly/09-conformal-coating.md) |
| Cleaning | Many assemblers run no-clean flux only, so cleaning may be sent out to another company. | [PCB-DFA-055](../05-assembly/08-cleaning.md) |
| IPC Class 3 | Inspection is stricter, and some boards built to a Class 2 design can't meet it. | [PCB-DFT-003](../03-bare-board-fabrication/11-bare-board-test.md) |
| Tin-lead solder | Many assemblers now run lead-free only. One assembler solders tin-lead through-hole parts entirely by hand. | |
| Stepped or etched stencils | A simple laser-cut stencil cost about $300 in 2024. Stepped or chemically etched stencils cost more, up to about $900 or more. | [Solder paste and stencils](../05-assembly/01-solder-paste-and-stencils.md) |
| Small, odd or thin panels | They need special handling, carriers or extra set-up. | [Part 2](../02-the-panel/01-why-panels.md) |

**What goes wrong if you don't:** You get a quote far higher than you expected, for reasons that are hard to change once the board is laid out.

**Example:** One customer new to fine-pitch BGAs designed overlapping blind and buried vias, with laser-drilled vias much smaller than they needed to be.
The assembler put them in touch with the fab's engineers, who showed them what was driving the cost.
A couple of weeks later the customer sent a redesigned board.
Its bare-board price came down to about $30 each, about a twentieth of what the first design would have cost.

**Applies to:** General practice; prices vary by manufacturer and over time.

**Sources:** ["What factors influence PCB quotes w/ Brett Babilonia"](https://www.buzzsprout.com/1066066/episodes/14580855-what-factors-influence-pcb-quotes-w-brett-babilonia) (Feb 2024), [18:00](https://www.buzzsprout.com/1066066/episodes/14580855?t=1080)–31:00, [47:00](https://www.buzzsprout.com/1066066/episodes/14580855?t=2820)–48:00 and [49:00](https://www.buzzsprout.com/1066066/episodes/14580855?t=2940)–52:00.

*Last reviewed: 2026-11-12*

---

## PCB-DFA-117: Get your quote from real design data, and expect a repeat build to be priced differently

**Recommendation:** Ask for a quote only when you have the real BOM and board files, or something very close to them.
Don't ask for a ballpark price from a description.
When you reorder, expect the price to change a little.
If the board hasn't changed, programming and stencil costs drop out.
If the board revision has changed, expect them to come back.

**Why:** An assembly quote is built from the actual parts, the number of unique lines, the number of sides and the processes the board needs.
Without the real data, the assembler can only guess, and a guess is no use to you.
On a first build, the assembler sometimes finds the job took longer than quoted, and the repeat price is adjusted, usually upwards.
But the one-off work of the first build, such as machine programming and approving the stencil, isn't repeated for an unchanged board.

**What goes wrong if you don't:** A budget built on a ballpark figure that turns out to be wrong, or surprise at a repeat price.

**Applies to:** General practice.

**Sources:** ["What factors influence PCB quotes w/ Brett Babilonia"](https://www.buzzsprout.com/1066066/episodes/14580855-what-factors-influence-pcb-quotes-w-brett-babilonia) (Feb 2024), [13:00](https://www.buzzsprout.com/1066066/episodes/14580855?t=780)–14:00 and [43:00](https://www.buzzsprout.com/1066066/episodes/14580855?t=2580)–45:00.

*Last reviewed: 2026-11-12*

---

## PCB-DFM-044: Ask your board fab how many boards its minimum lot charge buys

**Recommendation:** When you order a small number of bare boards, ask the fab what its minimum lot charge is and how many boards it covers.
Then order that number, rather than asking for prices at several small quantities.

**Why:** Most board fabs charge a fixed minimum for any order, however few boards are in it.
Up to some quantity, more boards cost nothing extra.
Asking for prices one quantity at a time hides where that point is.
Assemblers use the term less often than fabs, and some don't have a minimum lot charge at all.

**Typical values:** In one example, a fab quoted $300 for 5 boards, and the same $300 for 7, 10 and 11 boards.
The minimum lot charge covered 13 boards.
Twenty boards cost $430.

**What goes wrong if you don't:** You pay the same price for fewer boards than you could have had.

**Applies to:** Bare-board fabrication, mainly prototypes and small orders.

**Sources:** ["What are fiducials and why you should use them"](https://www.buzzsprout.com/1066066/episodes/9355465-what-are-fiducials-and-why-you-should-use-them) (Oct 2021), [03:00](https://www.buzzsprout.com/1066066/episodes/9355465?t=180)–04:00.

*Last reviewed: 2026-11-12*

---

## PCB-DFA-118: Order a few more boards than you need: 105 to 110 when you need 100

**Recommendation:** When you need a certain number of working boards, order about 5% to 10% more.
For example, order 105 to 110 boards when you need 100.
If the boards go into a test fixture, add the spares the fixture builder needs as well (PCB-DFT-017).

**Why:** Even a good design built well has a small failure rate.
A few boards will fail test, or fail early in a stress screen (PCB-DFT-019).
Some will be damaged in handling.
Spares cost little when they're built with the rest of the batch.
Building a handful more later costs a full set-up.

**Typical values:** About 5% to 10% extra, which is 105 to 110 boards when you need 100.

**What goes wrong if you don't:** You end up a few boards short, and a small top-up order costs almost as much in set-up as the first one.

**Applies to:** General practice.

**Sources:** ["Inevitable Failures"](https://www.buzzsprout.com/1066066/episodes/17722984-inevitable-failures) (Aug 2025), [21:00](https://www.buzzsprout.com/1066066/episodes/17722984?t=1260).

*Last reviewed: 2026-11-12*

---

## PCB-DFA-119: Leave at least two weeks of margin in your schedule, and plan round long factory holidays

**Recommendation:** Plan for boards to arrive at least two weeks before you need them.
Ask each supplier when it will close for long holidays, and the last day it will take an order that ships before it closes.
Ask domestic suppliers too, because their own suppliers may close.
Place orders before that date.
For the Lunar New Year, which falls in late January or February, place orders for February and March in early December where you can.
When an order is urgent, tell your manufacturer so, and say why.
Use holiday closures for work that doesn't need a factory, such as finishing designs and tidying your parts library.

**Why:** Lead times slip for reasons outside anyone's control: a late part, a question that waits, a holiday or a delay in transit.
Many factories in China slow down a week or two before the Lunar New Year, because staff travel home for the longest holiday of the year.
After the holiday, it takes time to clear the backlog.
Domestic suppliers get busier at the same time, as customers turn to them instead.
An assembler that knows an order is urgent can warn you early if something threatens the date.

**Typical values:** At least two weeks of margin.
Expect delays for about one to two months after the Lunar New Year.

**What goes wrong if you don't:** A missed launch or delivery date, or an expensive rush order to recover it.

**Applies to:** General practice; holiday dates change every year.

**Sources:** ["How Chinese New Year Impacts Manufacturing"](https://www.buzzsprout.com/1066066/episodes/9863955-how-chinese-new-year-impacts-manufacturing) (Jan 2022), [12:00](https://www.buzzsprout.com/1066066/episodes/9863955?t=720)–13:00, [17:00](https://www.buzzsprout.com/1066066/episodes/9863955?t=1020)–18:00 and [31:00](https://www.buzzsprout.com/1066066/episodes/9863955?t=1860)–36:00.

*Last reviewed: 2026-11-12*

---

## PCB-DFA-120: Answer your manufacturer's questions quickly, and keep an engineer reachable by telephone

**Recommendation:** While your order is being built, answer your manufacturer's questions within the hour, and within about 30 minutes once the job is on the assembly line.
Give the manufacturer the telephone number of an engineer who knows the design, not only an email address.
If you'll be away during a first or critical order, name someone who can answer for you.
Keep the questions about each order in one place, such as the order's own message thread, so that everyone sees the same answers.

**Why:** When an assembler finds a problem, such as a part that doesn't match the BOM, the line often stops until it has an answer.
If no answer comes, the job is taken off the line and has to wait for the next free slot.
At the fab, an unanswered question about the panel or the drawing stops the job too.

**Typical values:** Aim to answer within about 30 minutes.
An idle surface-mount line costs from several hundred to several thousand dollars an hour (2021 figure).
The machines on one line can cost $1 million to $2 million and are expected to last about 10 years.
A 48-hour fab turn can become 3 or 4 days while questions wait for answers.

**What goes wrong if you don't:** Your job comes off the line and loses days.
Or the assembler has to guess, and the guess is wrong.

**Applies to:** General practice; most important for first builds and fast turns.

**Sources:** ["Showstoppers that delay PCB assembly w/ Production Manager, Rob OConnell"](https://www.buzzsprout.com/1066066/episodes/9741439-showstoppers-that-delay-pcb-assembly-w-production-manager-rob-oconnell) (Dec 2021), [20:00](https://www.buzzsprout.com/1066066/episodes/9741439?t=1200)–24:00; ["Our top suggestions for customers w/ CircuitHub Account Manager, John Jacquinet"](https://www.buzzsprout.com/1066066/episodes/8884604-our-top-suggestions-for-customers-w-circuithub-account-manager-john-jacquinet) (Jul 2021), [27:00](https://www.buzzsprout.com/1066066/episodes/8884604?t=1620)–28:00 and [36:00](https://www.buzzsprout.com/1066066/episodes/8884604?t=2160)–39:00; ["What factors influence PCB quotes w/ Brett Babilonia"](https://www.buzzsprout.com/1066066/episodes/14580855-what-factors-influence-pcb-quotes-w-brett-babilonia) (Feb 2024), [07:00](https://www.buzzsprout.com/1066066/episodes/14580855?t=420)–10:00.

*Last reviewed: 2026-11-12*

---

## PCB-DFA-121: Check your order before you place it, and report a mistake at once

**Recommendation:** Before you place an order, check that the options you choose on the order match your fabrication drawing and files.
Check the board thickness, the solder mask color, the surface finish and any special processes such as via-in-pad.
If you find a mistake after ordering, report it straight away.
If the order was placed only minutes ago, ask whether it is simpler to cancel it and place a new one.

**Why:** Many manufacturers build to the options on the order, so an option that disagrees with your drawing may win.
Once fabrication has started, or parts have been bought, a change costs money and time.
A change made by hand on a placed order is also a chance for a new mistake.
A fresh order goes through the normal checks.

**Typical values:** In one assembler's experience, an order can usually be canceled and replaced at no cost within about 30 minutes, before work starts.
After about 24 to 48 hours, fabrication or parts buying has usually started, and changes get harder and dearer.

**What goes wrong if you don't:** Boards built to the wrong option, or a change fee that grows the longer you wait.

**Applies to:** General practice; how orders are placed varies by manufacturer.

**Sources:** ["Our top suggestions for customers w/ CircuitHub Account Manager, John Jacquinet"](https://www.buzzsprout.com/1066066/episodes/8884604-our-top-suggestions-for-customers-w-circuithub-account-manager-john-jacquinet) (Jul 2021), [40:00](https://www.buzzsprout.com/1066066/episodes/8884604?t=2400)–48:00.

*Last reviewed: 2026-11-12*

---

## Related pages
- [Prototype versus production](02-prototype-to-production.md)
- [Design reviews and communicating intent](03-design-reviews-and-communication.md)
- [BOM](../01-design-package/03-bom.md) (PCB-DFA-072, unique lines)
- [Fabrication data](../01-design-package/01-fabrication-data.md) (PCB-DFM-013 and 014, intent in the data and on the drawing)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

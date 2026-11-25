# Design reviews and communicating intent

A manufacturer can only build what the design data and drawings tell it.
Part 1 covers what goes in that data.
This page covers the conversation around it: when to bring the manufacturer in, how to learn from each build, and when to talk before you commit to something unusual.
The common thread is to talk early, while changes are still cheap.

## PCB-DFA-124: Bring your manufacturer into the design review before the design is final

**Recommendation:** Share the design with your fab and assembler while you can still change it, at about 60% to 80% complete.
Ask them what will be hard to make, test or ship.
Review in small steps as the design develops, rather than in one large review at the end.
Before each release, compare the schematic, the board and the BOM with the previous version, so you can see exactly what changed.
Let the mechanical engineers and others who depend on the board comment on the design files themselves, not only on a summary.

**Why:** At 60% to 80%, the layout is far enough along to show real problems, and still open enough to fix them.
Small reviews get read properly, and their actions get done.
A large review at the end produces a long list, and much of it never gets done.
A comparison of versions catches changes nobody meant to make.

**Typical values:** Review with suppliers at about 60% to 80% complete.

**What goes wrong if you don't:** Problems the manufacturer would have spotted in minutes turn into a board revision.
Or a review list so long that half of it is never acted on.

**Example:** One design review produced 327 items and 557 actions.
Only about half of them were ever dealt with.

**Applies to:** General practice.

**Sources:** ["Soft Skills of Engineering w/ Being an Engineer Host, Aaron Moncur"](https://www.buzzsprout.com/1066066/episodes/12593633-soft-skills-of-engineering-w-being-an-engineer-host-aaron-moncur) (Apr 2023), [47:00](https://www.buzzsprout.com/1066066/episodes/12593633?t=2820); ["The Benefits of Asynchronous Design Review for Engineers & Manufacturers w/ AllSpice.io"](https://www.buzzsprout.com/1066066/episodes/11886751-the-benefits-of-asynchronous-design-review-for-engineers-manufacturers-w-allspice-io) (Dec 2022), [31:00](https://www.buzzsprout.com/1066066/episodes/11886751?t=1860)–37:00 and [43:00](https://www.buzzsprout.com/1066066/episodes/11886751?t=2580)–45:00.

*Last reviewed: 2026-11-12*

---

## PCB-DFA-125: Ask for feedback after every build, and fix recurring problems before you reorder

**Recommendation:** After each build, ask your assembler and fab what gave them trouble.
Make the changes they suggest before you reorder, not after.
If the same problem comes up on more than one build, treat it as a design problem and fix it in the next revision.

**Why:** The people who built the board know exactly where the time went: a through-hole connector that could have been surface-mount, a part that had to be hand-soldered, a polarity mark that was easy to misread.
A manufacturer will often work round a problem without telling you, and keep paying for it on every build.
The next revision is the cheapest place to fix it.

**What goes wrong if you don't:** The same problem costs you money on every build, and sometimes causes the same defect again.

**Applies to:** General practice; most valuable on products that are reordered.

**Sources:** ["Our top suggestions for customers w/ CircuitHub Account Manager, John Jacquinet"](https://www.buzzsprout.com/1066066/episodes/8884604-our-top-suggestions-for-customers-w-circuithub-account-manager-john-jacquinet) (Jul 2021), [18:00](https://www.buzzsprout.com/1066066/episodes/8884604?t=1080)–21:00 and [49:00](https://www.buzzsprout.com/1066066/episodes/8884604?t=2940); ["Showstoppers that delay PCB assembly w/ Production Manager, Rob OConnell"](https://www.buzzsprout.com/1066066/episodes/9741439-showstoppers-that-delay-pcb-assembly-w-production-manager-rob-oconnell) (Dec 2021), [33:00](https://www.buzzsprout.com/1066066/episodes/9741439?t=1980)–34:00.

*Last reviewed: 2026-11-12*

---

## PCB-DFA-126: Talk to your manufacturer before designing in anything unusual, and don't assume standard pricing

**Recommendation:** Before you commit to anything outside a standard surface-mount build, ask your manufacturer whether it can do it, and what it will cost.
Ask every time, whether it's a first prototype or a product moving to higher volume.
If you choose a very fine-pitch BGA or chip-scale package, choose a manufacturer that has built that kind of part before.

**Why:** Unusual processes may need tooling, a different machine, a subcontractor or skills the manufacturer doesn't have.
None of that is in a standard price.
Experience with a fine-pitch part comes only from building it, and a manufacturer still learning will have lower yields.
The earlier you ask, the more choices you still have, including changing the design.

**Typical values:** Unusual processes covered elsewhere in this book include:
- press-fit parts (PCB-DFA-047)
- one-piece RF shields (PCB-DFA-050)
- boards thicker than about 2 mm (PCB-DFA-014)
- very thin boards and large, heavy double-sided panels (PCB-DFA-028)
- conformal coating and cleaning (PCB-DFA-055 and 061)
- adhesive-mounted parts and underfill (PCB-DFA-052 to 054).

**What goes wrong if you don't:** A quote far above what you expected, a lead time with tooling added, or a manufacturer that can't build the board at all.

**Applies to:** General practice.

**Sources:** ["Alternative Component Mounting"](https://www.buzzsprout.com/1066066/episodes/10030215-alternative-component-mounting) (Feb 2022), [18:00](https://www.buzzsprout.com/1066066/episodes/10030215?t=1080)–25:00 and [57:00](https://www.buzzsprout.com/1066066/episodes/10030215?t=3420)–59:00; ["To BGA or Not to BGA"](https://www.buzzsprout.com/1066066/episodes/19944540-to-bga-or-not-to-bga) (Oct 2026), [19:30](https://www.buzzsprout.com/1066066/episodes/19944540?t=1170)–22:00.

*Last reviewed: 2026-11-12*

---

## Related pages
- [What drives cost and lead time](01-cost-and-lead-time.md)
- [Prototype versus production](02-prototype-to-production.md)
- [Fabrication data](../01-design-package/01-fabrication-data.md) and [assembly data](../01-design-package/02-assembly-data.md)
- [BOM](../01-design-package/03-bom.md) (PCB-DFA-069, parts locked to one maker and why)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

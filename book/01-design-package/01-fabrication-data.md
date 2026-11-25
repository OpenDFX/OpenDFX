# Fabrication data

The fabrication data is everything you send a board fab so they can make the bare board: the copper and other layer images, the drill files, the board outline, a netlist, and a drawing with the notes the images can't carry.
None of it goes straight onto a machine.
A CAM engineer reads it all into CAM software, checks it, and rebuilds it into the fab's own production tools.
So the goal is CAM input that is complete, consistent and impossible to misread.

Each time the CAM engineer has to ask you a question, it can cost about a day.
Most of the recommendations below exist to remove those questions.

## PCB-DFM-008: Send one complete fabrication package, in one format, from one revision

**Recommendation:** Send the fab one archive per board, holding one set of fabrication data in a single format, all exported from the same revision of the design:
- one Gerber file per layer (every copper layer, both solder masks, both legends, both paste layers), in Gerber X2 if your tool supports it;
- drill files (see [PCB-DFM-011](#pcb-dfm-011-separate-plated-and-non-plated-holes-and-use-an-unambiguous-drill-format));
- the board outline as its own file;
- an IPC-D-356 netlist (see [PCB-DFM-009](#pcb-dfm-009-always-send-a-netlist-made-from-the-same-revision-as-the-gerbers));
- a fabrication drawing, plus the same specifications in a plain-text file (see [PCB-DFM-014](#pcb-dfm-014-put-everything-the-gerbers-cant-say-on-the-fabrication-drawing)).

ODB++ or IPC-2581 can replace the Gerbers, drill files and netlist, if your fab says it reads them.
Send one format or the other, not both.

Keep your native design files and schematic out of the fab package.
Send them to your assembler, and to the fab only if asked, in a separate folder marked "reference only" (see [PCB-DFA-064](02-assembly-data.md#pcb-dfa-064-always-send-the-xy-file-and-send-native-design-files-and-the-schematic-when-you-can)).

**Why:** Every file in the archive has to be opened and checked for instructions.
Extra files waste that time, and two copies of the same board in different formats (Gerber and ODB++, say) force the CAM engineer to compare them and ask which one is right.
Native design files need the same design software to open, and the fab builds from fabrication data, not from them.
IPC-2581 and ODB++ carry the netlist and layer structure inside them, which is their advantage, but each design tool exports them a little differently and each CAM system reads them a little differently.

**Typical values:** Gerber files with the standard `.gbr` extension and Gerber X2 attributes.
Even if top and bottom solder masks are identical, send both.

**What goes wrong if you don't:** Questions, a day's delay for each, and occasionally a board built from the wrong one of two conflicting files.

**Example:** One assembler that imports IPC-2581 from several design tools found that each tool writes the same standard slightly differently, and had to handle each one separately.
Practitioners have reported pads silently missing and thermal reliefs rotated after an ODB++ import, caught only by comparing against known-good artwork.
Open your outputs in a viewer that is not part of your design tool before you send them.

**Applies to:** General practice.
Which of Gerber, ODB++ and IPC-2581 to send varies by fab; ask yours.

**Sources:** *PCB Fabrication Data: Design to Fabrication Data Transfer*, V6 (Sept 2015), the guide published by the maintainers of the Gerber format: chapters 14 to 16 (one board per archive, nothing superfluous, no duplicate formats, both masks); Gerber Layer Format Specification, revision 2026.05; KiCad 10 documentation, fabrication outputs (Gerber, IPC-2581, ODB++, IPC-D-356); [“Building the factory of the future with CircuitHub CEO, Andrew Seddon”](https://www.buzzsprout.com/1066066/episodes/19621440-building-the-factory-of-the-future-with-circuithub-ceo-andrew-seddon) (Aug 2026), [38:00](https://www.buzzsprout.com/1066066/episodes/19621440?t=2280)–39:00; [“The PCB assembly process”](https://www.buzzsprout.com/1066066/episodes/4364141-the-pcb-assembly-process) (Jun 2020), [08:00](https://www.buzzsprout.com/1066066/episodes/4364141?t=480); Chris Denney (author).

*Last reviewed: 2026-11-07*

---

## PCB-DFM-009: Always send a netlist, made from the same revision as the Gerbers

**Recommendation:** Export an IPC-D-356 netlist from your design tool every time you export Gerbers, and send it with them.
If you send ODB++ or IPC-2581, the netlist is already inside.

**Why:** The first thing a CAM engineer does is build a netlist from your Gerbers and drill files, and they re-check against it every time they edit the data.
Your netlist comes from the schematic connections in your design tool, not from the images.
Comparing the two catches a Gerber that didn't import correctly, a trace or hole deleted by mistake, and copper that shorts two nets you meant to keep apart.
Without your netlist, the fab can only test the boards against a netlist built from your images, so a wrong image is built and passes electrical test anyway.
Many design tools only regenerate the netlist when you tick a separate box, so it's easy to send an old one.

**What goes wrong if you don't:** An error in the data is built faithfully, passes the fab's electrical test, and is found only after the board is assembled.
A stale netlist does the opposite: dozens of false mismatches, and questions back to you.

**Example:** CAM engineers report receiving netlists that contained only half the board, because the netlist was not re-exported after the layout changed.
A fab's quoting engineer gives the classic case: if the Gerbers show a plated slot where there shouldn't be one, and there's no netlist, you get a plated slot.

**Applies to:** General practice.
Fabs can work without a netlist; that doesn't make it a good idea.

**Sources:** *PCB Fabrication Data: Design to Fabrication Data Transfer*, V6 (Sept 2015), chapter 11, "Always include the netlist"; one large fab's published data guidance (checks the supplied IPC netlist against its own); [“The PCB CAM Process w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/8226431-the-pcb-cam-process-w-dave-wilcox) (Mar 2021), [12:00](https://www.buzzsprout.com/1066066/episodes/8226431?t=720)–19:00; [“What factors influence PCB quotes w/ Brett Babilonia”](https://www.buzzsprout.com/1066066/episodes/14580855-what-factors-influence-pcb-quotes-w-brett-babilonia) (Feb 2024), [09:00](https://www.buzzsprout.com/1066066/episodes/14580855?t=540)–11:00.

*Last reviewed: 2026-11-07*

---

## PCB-DFM-010: Tell the fab where you join nets on purpose

**Recommendation:** If your copper deliberately joins nets that stay separate in the schematic (a star point joining analog and digital ground, a net-tie, a shorting jumper), list them in your fabrication notes.
Better still, use your design tool's net-tie feature so the netlist knows about them.

**Why:** The fab compares its netlist, built from the copper, with yours.
A deliberate join looks exactly like a short.

**What goes wrong if you don't:** The netlist check fails, and the job stops while the CAM engineer asks you whether each join is meant to be there.

**Applies to:** General practice.

**Sources:** [“The PCB CAM Process w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/8226431-the-pcb-cam-process-w-dave-wilcox) (Mar 2021), [17:00](https://www.buzzsprout.com/1066066/episodes/8226431?t=1020)–18:00.

*Last reviewed: 2026-11-07*

---

## PCB-DFM-011: Separate plated and non-plated holes, and use an unambiguous drill format

**Recommendation:** Put plated and non-plated holes in separate drill files.
Export them as Gerber X2 drill files if your fab accepts them.
If you send Excellon (NC drill) files, use one of the two safe formats, 2:4 inch or 3:3 metric, with the units and zero suppression stated in the header.
Make the drill files from the same origin as the Gerbers, so the holes land on their pads.

**Why:** If plating isn't stated, the CAM engineer guesses from the copper: a hole through a pad is plated, a hole in bare laminate is not.
A large hole you wanted plated, with no copper around it, comes back bare.
Excellon has no standard way to say where the decimal point is, so the fab has to work out the number of digits and which zeros were left off.
Formats with too few decimal places, such as 3:2 metric, round every hole position to the nearest 0.01 mm, which shifts holes off their pads.
Gerber X2 drill files have none of these problems, and they also say which layers a blind or buried via spans.

**Typical values:** 2:4 inch or 3:3 metric for Excellon; avoid 3:2 metric, 5:1, 1:5 and other unusual formats.
Metric is preferred where you have the choice.
A format that writes every coordinate with a decimal point, such as KiCad's decimal format, can't be misread either, so it is also safe.

**What goes wrong if you don't:** Holes plated that shouldn't be, or not plated that should, and drill files that need hand-work to line up with the copper.

**Applies to:** General practice.
Many fabs still ask for Excellon.
KiCad 10's drill dialog writes plated and non-plated holes to separate Excellon files by default, but its command-line export puts them in one file unless you ask for separate files.

**Sources:** [“The basics of the PCB drilling process w/ CAM Engineer Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/9091552-the-basics-of-the-pcb-drilling-process-w-cam-engineer-dave-wilcox) (Aug 2021), [24:00](https://www.buzzsprout.com/1066066/episodes/9091552?t=1440)–28:00; [“The PCB CAM Process w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/8226431-the-pcb-cam-process-w-dave-wilcox) (Mar 2021), [01:13:00](https://www.buzzsprout.com/1066066/episodes/8226431?t=4380)–01:15:00; *PCB Fabrication Data: Design to Fabrication Data Transfer*, V6 (Sept 2015), chapters 7 and 9; XNC drill format specification, revision 2021.11 (separate plated and non-plated files; metric recommended); KiCad 10 documentation, drill file options.

*Last reviewed: 2026-11-07*

---

## PCB-DFM-012: Dimension the holes that matter, with their real tolerance

**Recommendation:** If a hole's size or position matters (a press-fit pin, a connector whose datasheet says +0.1/−0 mm, a hole sized for current, a mounting hole that must line up with an enclosure), dimension it on the drill drawing with its true tolerance.
Design the hole to the middle of the allowed range, not to the nominal value.
Don't create extra hole sizes just to split the difference; a drawing callout does the job.

**Why:** Fabs adjust hole sizes to suit their process: they drill plated holes larger to allow for plating, and may enlarge an awkward size within the standard tolerance without telling you.
IPC-6012F says only holes dimensioned in the procurement documents are inspected for position; the rest are checked only through annular ring.
A one-sided tolerance such as +0.1/−0 mm is invisible in the data: a 0.7 mm hole looks like any other 0.7 mm hole.

**Typical values:** IPC-6012F default finished hole tolerances, when the drawing says nothing: ±100 µm for plated component holes, +80 µm with no lower limit for via-only holes (they may be plugged), ±80 µm for non-plated holes.
One large fab aims for the middle of any tolerance band you give it.
Tighter than standard tolerances are possible, but cost more, because every hole has to be measured and out-of-range boards scrapped.

**What goes wrong if you don't:** A connector that won't go in, or falls out; a press-fit pin that sits loose in a hole drilled too large.

**Example:** Small connectors whose datasheets call for 0.7 mm +0.1/−0 holes have repeatedly caused trouble when the footprint simply used a 0.7 mm hole, because the fab had no way of knowing the hole must never be smaller.

**Applies to:** General practice.

**Sources:** IPC-6012F (Sept 2023), Table 1-2 and section 3.4.1; [“The basics of the PCB drilling process w/ CAM Engineer Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/9091552-the-basics-of-the-pcb-drilling-process-w-cam-engineer-dave-wilcox) (Aug 2021), [18:00](https://www.buzzsprout.com/1066066/episodes/9091552?t=1080)–21:00; [“Advanced Drilling w/ CAM Engineer, Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/10611991-advanced-drilling-w-cam-engineer-dave-wilcox) (May 2022), [42:00](https://www.buzzsprout.com/1066066/episodes/10611991?t=2520)–48:00; [“The PCB CAM Process w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/8226431-the-pcb-cam-process-w-dave-wilcox) (Mar 2021), [01:00:00](https://www.buzzsprout.com/1066066/episodes/8226431?t=3600)–01:11:00; one large fab's published hole-size guidance.

*Last reviewed: 2026-11-07*

---

## PCB-DFM-013: Put your intent in the data, not in a note that contradicts it

**Recommendation:** Make the layer files show the board you want.
If you want vias tented, export the solder mask with no openings over them, rather than leaving openings and adding a note saying "tent all vias".
Don't export component values or other assembly text onto the legend layer unless you want it printed.
Keep title blocks, frames and notes out of the layer files; put them on the drawing.

**Why:** A CAM engineer treats the data as what you want.
When a note contradicts the data, they have to stop and ask which one is right.
A note like "tent all vias" also leaves them to decide which holes are vias, which is hard when a board has several via sizes and small component holes.
Value text exported to the legend lands on pads and gets clipped off, or prints as an unreadable mass of overlapping text.

**What goes wrong if you don't:** A question and a day's delay, or a board built to the data when you meant the note.

**Applies to:** General practice.
Most design tools can tent vias in the export settings; in some it takes a design rule on hole size.

**Sources:** [“The PCB CAM Process w/ Dave Wilcox”](https://www.buzzsprout.com/1066066/episodes/8226431-the-pcb-cam-process-w-dave-wilcox) (Mar 2021), [22:00](https://www.buzzsprout.com/1066066/episodes/8226431?t=1320)–24:00 and [55:00](https://www.buzzsprout.com/1066066/episodes/8226431?t=3300)–01:00:00; [“Small PCB layout decisions that have a significant impact on assembly”](https://www.buzzsprout.com/1066066/episodes/8957623-small-pcb-layout-decisions-that-have-a-significant-impact-on-assembly) (Aug 2021), [10:00](https://www.buzzsprout.com/1066066/episodes/8957623?t=600)–14:00; *PCB Fabrication Data: Design to Fabrication Data Transfer*, V6 (Sept 2015), chapter 10, "Put only data in data files".

*Last reviewed: 2026-11-07*

---

## PCB-DFM-014: Put everything the Gerbers can't say on the fabrication drawing

**Recommendation:** Give every board a fabrication drawing that states, at least:
- performance class (IPC-6012 Class 2 or Class 3);
- base material, called out by grade and Tg (for example against an IPC-4101 slash sheet), not just "FR-4", and finished board thickness and its tolerance;
- copper weight for each layer;
- stack-up, and any controlled impedance as a table: structure, layers, target impedance, tolerance and reference planes;
- surface finish, solder mask color and legend color;
- via treatment (tented, plugged, filled);
- board outline with critical dimensions, cut-outs and slots, and the drill chart with tolerances;
- revision, date and author.

Put the same specifications in a plain-text file in the package too.
If you order through a web form, make sure it matches the drawing.

**Why:** Gerbers only show shapes.
Thickness, material, finish, class and impedance can only come from you.
When the drawing is silent, IPC-6012F fills the gap with defaults the fab will build to, which may not be what you meant.
Many fabs' software can read specifications from a plain-text file automatically; none can read them from a drawing.
The same goes for the AI tools now used to check designs and prepare quotes: a text file is read exactly, a drawing has to be interpreted.

**Typical values:** IPC-6012F defaults when nothing is specified: Class 2; epoxy-glass laminate; ENIG finish for designs first released on or after 1 October 2023 (tin-lead for older ones); 1/2 oz starting copper on every layer; the hole tolerances in [PCB-DFM-012](#pcb-dfm-012-dimension-the-holes-that-matter-with-their-real-tolerance).
IPC-6012F gives no default board thickness tolerance; other dimensional tolerances fall back to the IPC-2220 design standards.
Fabs commonly quote ±10% on thickness for boards 0.8 mm and thicker, but this varies, so state the tolerance you need.
Controlled impedance is commonly held to ±10%, and ±5% on request.

**What goes wrong if you don't:** Boards that are the wrong thickness, the wrong finish, or the wrong class, and no claim against the fab, because they built what was ordered.
If controlled impedance isn't on the drawing, the fab doesn't control it, and a board that doesn't perform is still a good board as far as they're concerned.

**Example:** At one assembler that builds bare boards to what is entered on its order form, boards have come back the wrong thickness because the thickness wasn't set there.
Wrong thickness can't be reworked: it means new bare boards and a new assembly.

**Applies to:** General practice.
IPC-2611 and IPC-2614 cover fabrication documentation in full.

**Sources:** IPC-6012F (Sept 2023), section 1.3.3 and Table 1-2, Table 3-3, section 3.4; one fab's published fabrication-notes guide; *PCB Fabrication Data: Design to Fabrication Data Transfer*, V6 (Sept 2015), chapter 15; [“Understanding Controlled Impedance w/ NCAB Group Field Application Engineer, Ryan Miller”](https://www.buzzsprout.com/1066066/episodes/11631934-understanding-controlled-impedance-w-ncab-group-field-application-engineer-ryan-miller) (Nov 2022), [17:00](https://www.buzzsprout.com/1066066/episodes/11631934?t=1020)–18:00; [“Impedance Control Demo w/ NCAB Group Field Application Engineer Ryan Miller”](https://www.buzzsprout.com/1066066/episodes/13789746-impedance-control-demo-w-ncab-group-field-application-engineer-ryan-miller) (Oct 2023), [25:00](https://www.buzzsprout.com/1066066/episodes/13789746?t=1500)–27:00; [“What factors influence PCB quotes w/ Brett Babilonia”](https://www.buzzsprout.com/1066066/episodes/14580855-what-factors-influence-pcb-quotes-w-brett-babilonia) (Feb 2024), [11:00](https://www.buzzsprout.com/1066066/episodes/14580855?t=660)–12:00; [“Our top suggestions for customers w/ CircuitHub Account Manager, John Jacquinet”](https://www.buzzsprout.com/1066066/episodes/8884604-our-top-suggestions-for-customers-w-circuithub-account-manager-john-jacquinet) (Jul 2021), [40:00](https://www.buzzsprout.com/1066066/episodes/8884604?t=2400)–43:00.

*Last reviewed: 2026-11-07*

---

## PCB-DFM-015: Check a copied fabrication drawing line by line

**Recommendation:** When you start a new board from an old one's drawing or stack-up, read every note again.
Remove impedance callouts, reference planes, finishes and special processes the new board doesn't need, and add the ones it does.

**Why:** Drawings are usually copied from the last project.
Notes that were right for the old board stay on, and requirements for the new one get left off.

**Typical values:** Under IPC-6012F, a drawing first released before 1 October 2023 with no finish callout defaults to a tin-lead finish; one released after defaults to ENIG.
State the finish rather than rely on the date.

**What goes wrong if you don't:** Impedance requirements for traces that no longer exist, with questions to match, or a missing reference plane and a board that doesn't work even though it passed every inspection.

**Example:** One fab's engineers regularly find impedance callouts copied from an earlier drawing that don't apply to the new board, or reference planes left out.

**Applies to:** General practice.

**Sources:** [“Understanding Controlled Impedance w/ NCAB Group Field Application Engineer, Ryan Miller”](https://www.buzzsprout.com/1066066/episodes/11631934-understanding-controlled-impedance-w-ncab-group-field-application-engineer-ryan-miller) (Nov 2022), [39:00](https://www.buzzsprout.com/1066066/episodes/11631934?t=2340)–41:00; IPC-6012F (Sept 2023), Table 1-2 and Table 3-3.

*Last reviewed: 2026-11-07*

---

## PCB-DFM-016: Clear every design-rule error before you make the outputs

**Recommendation:** Run your design tool's design-rule check (DRC) and resolve every error, above all unconnected nets, before you export anything.
Then compare the release with the previous one, so you know exactly what changed.

**Why:** Design tools will happily export Gerbers from a board with unrouted connections.
Treat DRC errors like compiler warnings: each one is either fixed or understood.
A comparison between versions (a schematic, layout or BOM diff, not just "this file changed") catches values and net names changed by accident.

**What goes wrong if you don't:** A board with a missing connection, fixed with a wire on the prototype and a new revision afterwards.

**Example:** A first-time designer's board had a dead display because one power pin was never routed to the microcontroller.
A mentor found it from the design files, and a single wire fixed the prototype.

**Applies to:** General practice.

**Sources:** [“Building a product at a big organization vs a startup w/ Barnacle Systems CTO, Darren Beckwith”](https://www.buzzsprout.com/1066066/episodes/10360463-building-a-product-at-a-big-organization-vs-a-startup-w-barnacle-systems-cto-darren-beckwith) (Apr 2022), [52:00](https://www.buzzsprout.com/1066066/episodes/10360463?t=3120)–53:00; [“How sensors.AFRICA empowers citizens to fight against pollution w/ Jack McLeans”](https://www.buzzsprout.com/1066066/episodes/7831030-how-sensors-africa-empowers-citizens-to-fight-against-pollution-w-jack-mcleans) (Feb 2021), [23:00](https://www.buzzsprout.com/1066066/episodes/7831030?t=1380)–24:00; [“The Benefits of Asynchronous Design Review for Engineers & Manufacturers w/ AllSpice.io”](https://www.buzzsprout.com/1066066/episodes/11886751-the-benefits-of-asynchronous-design-review-for-engineers-manufacturers-w-allspice-io) (Dec 2022), [31:00](https://www.buzzsprout.com/1066066/episodes/11886751?t=1860)–34:00.

*Last reviewed: 2026-11-07*

---

## Related pages
- [Assembly data](02-assembly-data.md)
- [The BOM](03-bom.md)
- [Footprints and the component library](04-footprints.md)
- [Clearance near board and panel edges](../02-the-panel/04-edge-clearance.md)

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

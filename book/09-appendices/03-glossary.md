# Appendix C: Glossary

The terms this book uses, in alphabetical order.
Each definition is short.
The link after it goes to the page that explains the term in full.

**Alternate part.**
A second part, from another maker or in another package, that can be fitted in place of the one on the BOM.
Listing alternates lets your assembler keep building when one part is out of stock.
See [The BOM](../01-design-package/03-bom.md).

**Annular ring.**
The ring of copper left around a drilled hole on its pad.
It is measured from the edge of the hole to the edge of the pad.
See [Drilling](../03-bare-board-fabrication/03-drilling.md).

**AOI (automated optical inspection).**
A machine that photographs each assembled board and compares it with a known-good board, to find missing, misplaced and badly soldered parts.
See [Optical and X-ray inspection](../05-assembly/04-inspection.md).

**Aspect ratio.**
The thickness of a board divided by the diameter of a drilled hole.
A high aspect ratio makes a hole harder to plate evenly.
See [Drilling](../03-bare-board-fabrication/03-drilling.md).

**Assembly drawing.**
A drawing that shows how the board is to be assembled.
It gives what the placement data can't, such as hardware, torques, areas to keep free of coating, and special instructions.
See [Assembly data](../01-design-package/02-assembly-data.md).

**Authorized distributor.**
A distributor that buys parts directly from the maker under an agreement with it.
Parts bought this way are traceable to the maker.
See [Sourcing, counterfeits and obsolescence](../04-components-and-materials/04-sourcing.md).

**Bake.**
Heating parts or bare boards in an oven for a set time to drive out moisture they have absorbed, before they go through reflow.
See [Moisture-sensitive parts](../04-components-and-materials/03-moisture-sensitive-parts.md).

**Bed-of-nails fixture.**
A test fixture with a spring-loaded probe for each test point, which contacts all of them at once.
It is fast in use but costly to make, so it suits high volumes.
See [Flying probe and in-circuit test](../06-test-and-programming/02-flying-probe-and-ict.md).

**BGA (ball grid array).**
A part package with its connections as a grid of solder balls on its underside.
The joints can't be seen once the part is soldered, so they are checked by X-ray.
See [Component placement](../05-assembly/02-component-placement.md).

**Blind via.**
A via that runs from an outer layer to an inner layer without going through the whole board.
See [Drilling](../03-bare-board-fabrication/03-drilling.md).

**BOM (bill of materials).**
The list of every part on the board.
Each line gives the reference designators, the quantity, the maker and the maker's full part number.
See [The BOM](../01-design-package/03-bom.md).

**Boundary scan.**
A way of testing connections through test logic built into chips that support it, reached through a small connector.
It is also called JTAG, after the group that wrote the standard.
See [Boundary scan](../06-test-and-programming/03-boundary-scan.md).

**Breakaway tab.**
A narrow strip of board material that holds a board in its panel until it is separated.
Tabs are often drilled with a row of small holes, called mouse bites, so they snap cleanly.
See [Breakaway methods](../02-the-panel/03-breakaway-methods.md).

**Broker.**
A seller who buys parts from sources other than the maker and resells them.
Brokers can find parts that are out of stock elsewhere, but their parts carry a higher risk of being counterfeit or badly stored.
See [Sourcing, counterfeits and obsolescence](../04-components-and-materials/04-sourcing.md).

**Buried via.**
A via that joins two or more inner layers and does not reach either outer layer.
See [Drilling](../03-bare-board-fabrication/03-drilling.md).

**Burn-in.**
Running assembled boards under power, often at a raised temperature, to find early failures before the product ships.
See [Burn-in, stress testing and early failures](../06-test-and-programming/06-burn-in-and-stress.md).

**Carrier.**
A rigid frame or pallet that holds a thin or flexible board flat while it goes through assembly.
See [Materials and stack-up](../03-bare-board-fabrication/01-materials-and-stack-up.md).

**Carrier tape.**
The plastic or paper tape, with a pocket for each part, that parts come in on a reel.
See [Packaging: reels, cut tape, tubes, trays](../04-components-and-materials/02-packaging.md).

**Castellated hole.**
A plated hole cut in half by the board edge, so the board can be soldered onto another board like a part.
See [Profiling](../03-bare-board-fabrication/10-profiling.md).

**Class (IPC Class 1, 2 and 3).**
The level of quality a board is built and inspected to, set by the IPC standards.
Class 1 is for general electronic products.
Class 2 is for dedicated service products, which should work reliably but are not critical.
Class 3 is for high-performance products, which must keep working when called on, sometimes in harsh conditions.
See [Classes and standards in one page](../00-start-here/04-classes-and-standards.md).

**Conformal coating.**
A thin protective film applied over an assembled board to keep out moisture and contamination.
See [Conformal coating](../05-assembly/09-conformal-coating.md).

**Consignment.**
Supplying some or all of the parts yourself, rather than letting your assembler buy them.
Consigned parts are also called customer-supplied parts.
See [Supplying your own parts (consignment) and spares](../04-components-and-materials/05-consignment-and-spares.md).

**Contract manufacturer.**
A company that builds boards or products to a customer's design.
This book calls it your manufacturer, or your assembler when it does the assembly.
See [Design reviews and communicating intent](../08-working-with-a-manufacturer/03-design-reviews-and-communication.md).

**Controlled impedance.**
A trace whose width, copper thickness and distance from its reference plane are held to tolerances, so that its impedance meets a target value.
See [Materials and stack-up](../03-bare-board-fabrication/01-materials-and-stack-up.md).

**Copper pour.**
An area of copper filled in around traces and pads, usually joined to ground or a power net.
See [Outer layers](../03-bare-board-fabrication/05-outer-layers.md).

**Copper weight.**
The thickness of copper on a layer, given as its weight in ounces per square foot.
One ounce copper is about 35 µm thick.
See [Materials and stack-up](../03-bare-board-fabrication/01-materials-and-stack-up.md).

**Core.**
A layer of cured laminate with copper on both sides, from which the inner layers of a multilayer board are made.
See [Inner layers and lamination](../03-bare-board-fabrication/02-inner-layers-and-lamination.md).

**Counterfeit part.**
A part that is not what its marking and packaging claim: a copy, a reject, or a used part sold as new.
See [Sourcing, counterfeits and obsolescence](../04-components-and-materials/04-sourcing.md).

**Countersink.**
A cone-shaped recess drilled at the top of a hole so a flat-head screw sits flush with the board.
A counterbore is the same idea with a flat-bottomed recess.
See [Profiling](../03-bare-board-fabrication/10-profiling.md).

**Cut tape.**
A short length of carrier tape cut from a reel.
It must be long enough for the machine's feeder to hold, or it has to be spliced.
See [Packaging: reels, cut tape, tubes, trays](../04-components-and-materials/02-packaging.md).

**Date code.**
The code printed on a part or its packaging that shows when it was made.
See [Sourcing, counterfeits and obsolescence](../04-components-and-materials/04-sourcing.md).

**Depaneling.**
Separating finished boards from their panel.
It is done by snapping V-scores or tabs, cutting, or routing.
See [Depaneling](../05-assembly/10-depaneling.md).

**Design rule check (DRC).**
An automatic check in your design software that finds traces, pads and holes closer together, or smaller, than your rules allow.
See [Fabrication data](../01-design-package/01-fabrication-data.md).

**Desiccant.**
A packet of drying agent sealed in a bag with moisture-sensitive parts or boards to keep them dry.
See [Moisture and storage](../07-handling-packaging-and-shipping/02-moisture-and-storage.md).

**DFA, DFM and DFT.**
Design for assembly, design for manufacture and design for test.
In this book, DFM covers bare-board fabrication, DFA covers assembly, and DFT covers test.
See [How recommendations are numbered and tagged](../00-start-here/02-numbering-and-tags.md).

**Dielectric.**
The insulating material between copper layers.
Its thickness and its dielectric constant set the impedance of the traces above it.
See [Materials and stack-up](../03-bare-board-fabrication/01-materials-and-stack-up.md).

**DNP (do not place).**
A part that is in the design but is not to be fitted on this build.
It is also written DNI (do not install) or DNF (do not fit).
See [The BOM](../01-design-package/03-bom.md).

**Drill file.**
The file that gives the position and size of every drilled hole.
The usual format is Excellon.
See [Fabrication data](../01-design-package/01-fabrication-data.md).

**Electrical test.**
Testing a bare board for open and short circuits against its netlist, before any parts are fitted.
See [Bare board electrical test and inspection](../03-bare-board-fabrication/11-bare-board-test.md).

**ENIG (electroless nickel immersion gold).**
A surface finish of nickel with a thin layer of gold over it.
It is flat, solders well and keeps well, so it suits most boards.
ENEPIG adds a layer of palladium between the nickel and the gold.
See [Surface finish](../03-bare-board-fabrication/08-surface-finish.md).

**ESD (electrostatic discharge).**
A sudden flow of static electricity, for example from a person's finger to a board.
It can damage parts without leaving any visible mark.
See [Static (ESD) protection](../07-handling-packaging-and-shipping/01-static-protection.md).

**Fabrication drawing.**
A drawing that tells the board fab what the Gerber files can't: material, thickness, finish, colors, tolerances, class and special requirements.
See [Fabrication data](../01-design-package/01-fabrication-data.md).

**Fab.**
Short for fabricator: the company that makes the bare board.
See [Bare board fabrication](../03-bare-board-fabrication/01-materials-and-stack-up.md).

**Feeder.**
The device on a pick-and-place machine that holds a reel, tube or tray of parts and presents them one at a time.
See [Packaging: reels, cut tape, tubes, trays](../04-components-and-materials/02-packaging.md).

**Fiducial.**
A small copper target that machine cameras use to find exactly where a board or panel is.
Global fiducials are on the panel rails, board fiducials are on each board, and local fiducials sit beside a single part.
See [Rails, tooling holes and fiducials](../02-the-panel/02-rails-tooling-holes-fiducials.md).

**First article.**
The first board or boards off a production run, checked in full before the rest of the run is built.
See [First articles](../06-test-and-programming/07-first-articles.md).

**Fixture.**
A tool that holds a board for a process or test, such as a test fixture, a programming fixture or a carrier.
See [Functional test and fixtures](../06-test-and-programming/05-functional-test-and-fixtures.md).

**Floor life.**
How long a moisture-sensitive part may be out of its sealed bag, in factory air, before it must be baked.
See [Moisture-sensitive parts](../04-components-and-materials/03-moisture-sensitive-parts.md).

**Flux.**
A chemical that cleans metal surfaces so solder can wet them.
No-clean flux leaves a residue that is safe to leave on the board.
Water-soluble flux is more active and must be washed off.
See [Cleaning](../05-assembly/08-cleaning.md).

**Flying probe.**
A test machine that moves a few probes from point to point over the board, so it needs no custom fixture.
It is slower than a bed-of-nails fixture, so it suits prototypes and small builds.
See [Flying probe and in-circuit test](../06-test-and-programming/02-flying-probe-and-ict.md).

**Footprint.**
The pattern of copper pads, solder mask openings, paste openings and silkscreen that a part is soldered to.
It is also called a land pattern.
See [Footprints and the component library](../01-design-package/04-footprints.md).

**FR-4.**
The standard board material: woven glass cloth bonded with epoxy resin.
See [Materials and stack-up](../03-bare-board-fabrication/01-materials-and-stack-up.md).

**Functional test.**
A test that powers the board and checks that it does its job.
See [Functional test and fixtures](../06-test-and-programming/05-functional-test-and-fixtures.md).

**Gerber files.**
The standard file format for board layers: one file for each copper, solder mask, paste and legend layer, plus the outline.
ODB++ and IPC-2581 are alternative formats that carry all of the layers and more in one package.
See [Fabrication data](../01-design-package/01-fabrication-data.md).

**Gold fingers.**
Plated contacts along the edge of a board that plug into an edge connector.
See [Surface finish](../03-bare-board-fabrication/08-surface-finish.md).

**HASL (hot air solder leveling).**
A surface finish made by dipping the board in molten solder and blowing off the excess with hot air.
It is cheap but not flat, so it suits coarse-pitch parts.
See [Surface finish](../03-bare-board-fabrication/08-surface-finish.md).

**Head-in-pillow.**
A defect in which a part's ball or terminal rests in the solder on its pad, but the two never fuse into one joint.
The joint can look sound from outside.
It is most common under BGAs, and also happens on small chip parts whose pads are too far apart.
See [Footprints and the component library](../01-design-package/04-footprints.md).

**Humidity indicator card.**
A card packed with moisture-sensitive items whose spots change color when the humidity inside the bag is too high.
See [Moisture and storage](../07-handling-packaging-and-shipping/02-moisture-and-storage.md).

**ICT (in-circuit test).**
A test that probes each net of an assembled board through a bed-of-nails fixture, to check that each part is fitted, the right value and soldered.
See [Flying probe and in-circuit test](../06-test-and-programming/02-flying-probe-and-ict.md).

**Immersion silver and immersion tin.**
Thin, flat surface finishes deposited by a chemical reaction.
They are cheap and flat, but they tarnish, so they need careful storage.
See [Surface finish](../03-bare-board-fabrication/08-surface-finish.md).

**Intrusive soldering.**
Soldering through-hole parts in the reflow oven, with paste printed into and around their holes.
It is also called pin-in-paste.
See [Through-hole soldering](../05-assembly/05-through-hole-soldering.md).

**Keep-out.**
An area of the board where parts, copper or other features must not be placed.
See [Breakaway methods](../02-the-panel/03-breakaway-methods.md).

**Laminate.**
Board material: layers of glass cloth bonded with resin, usually with copper foil on one or both sides.
See [Materials and stack-up](../03-bare-board-fabrication/01-materials-and-stack-up.md).

**Lead time.**
The time from placing an order to receiving it.
See [What drives cost and lead time](../08-working-with-a-manufacturer/01-cost-and-lead-time.md).

**Lead-free.**
Solder and finishes made without lead.
The usual lead-free solder is an alloy of tin, silver and copper, which melts hotter than the old tin-lead solder.
See [Reflow soldering](../05-assembly/03-reflow-soldering.md).

**Legend.**
The printed text and outlines on a board, usually white.
It is also called silkscreen.
See [Legend (silkscreen)](../03-bare-board-fabrication/09-legend.md).

**Mask dam.**
A thin strip of solder mask left between two neighboring pads, which stops solder bridging between them.
It is also called a mask web.
See [Footprints and the component library](../01-design-package/04-footprints.md).

**Microvia.**
A very small via, usually laser-drilled, that joins neighboring layers.
See [Drilling](../03-bare-board-fabrication/03-drilling.md).

**MLCC (multilayer ceramic capacitor).**
The common surface-mount ceramic capacitor.
It cracks easily if the board bends, for example when a panel is broken apart.
See [Clearance near board and panel edges](../02-the-panel/04-edge-clearance.md).

**Mouse bites.**
A row of small drilled holes across a breakaway tab, so the tab snaps cleanly along that line.
See [Breakaway methods](../02-the-panel/03-breakaway-methods.md).

**MSL (moisture sensitivity level).**
A rating from 1 to 6 that says how quickly a part absorbs enough moisture to be damaged in reflow.
It sets the part's floor life.
See [Moisture-sensitive parts](../04-components-and-materials/03-moisture-sensitive-parts.md).

**Netlist.**
A list of every net on the board and the pads it joins.
The fab uses an IPC-D-356 netlist to test the bare board.
See [Fabrication data](../01-design-package/01-fabrication-data.md).

**Non-plated hole.**
A drilled hole with no copper inside it, usually for mounting or tooling.
See [Footprints and the component library](../01-design-package/04-footprints.md).

**Nozzle.**
The tip on a pick-and-place head that picks up a part by suction.
It needs a flat area on top of the part to grip.
See [Packaging: reels, cut tape, tubes, trays](../04-components-and-materials/02-packaging.md).

**OSP (organic solderability preservative).**
A thin organic coating that protects bare copper until soldering.
It is cheap and flat, but it has a short shelf life and doesn't stand up well to several heat cycles.
See [Surface finish](../03-bare-board-fabrication/08-surface-finish.md).

**Overhang.**
The part of a component, such as a connector, that extends past the edge of the board.
See [Breakaway methods](../02-the-panel/03-breakaway-methods.md).

**Pad.**
An area of exposed copper that a part's lead or terminal is soldered to.
See [Footprints and the component library](../01-design-package/04-footprints.md).

**Panel.**
A larger sheet that holds several copies of a board, or one board with rails, so it can go through fabrication and assembly.
Arranging boards in a panel is called panelization.
See [Why boards are built in panels](../02-the-panel/01-why-panels.md).

**Paste layer.**
The layer in your design data that shows where solder paste is printed.
The stencil is cut from it.
See [Solder paste printing and stencils](../05-assembly/01-solder-paste-and-stencils.md).

**Pick-and-place machine.**
The machine that takes parts from their packaging and places them on the pasted board.
See [Component placement](../05-assembly/02-component-placement.md).

**Pin 1.**
The first pin of a part, from which the rest are numbered.
It is marked on the part and should be marked beside its footprint.
See [Footprints and the component library](../01-design-package/04-footprints.md).

**Placement file.**
A file that gives the position, rotation and side of every part.
It is also called the XY file, the centroid file or the pick-and-place file.
See [Assembly data](../01-design-package/02-assembly-data.md).

**Plated through-hole.**
A drilled hole with copper plated on its wall, which joins the layers and can take a through-hole lead.
See [Footprints and the component library](../01-design-package/04-footprints.md).

**Polarity mark.**
A mark beside a footprint that shows which way round a polarized part goes, such as a diode's cathode.
See [Footprints and the component library](../01-design-package/04-footprints.md).

**Prepreg.**
Glass cloth soaked in resin that is only partly cured.
It bonds the layers of a multilayer board together when they are pressed and heated.
See [Inner layers and lamination](../03-bare-board-fabrication/02-inner-layers-and-lamination.md).

**Press-fit.**
A connector or pin that is pressed into a plated hole and held by friction, with no solder.
See [Press-fit and mechanical parts](../05-assembly/06-press-fit-and-mechanical.md).

**QFN (quad flat no-lead).**
A small square part package with pads on its underside along each edge, and usually a large thermal pad in the middle.
See [Component placement](../05-assembly/02-component-placement.md).

**QFP (quad flat package).**
A square part package with gull-wing leads along all four sides.
At fine pitch the leads bend easily and bridge, so this book prefers a BGA or QFN.
See [Component placement](../05-assembly/02-component-placement.md).

**Rail.**
A strip of extra board material along the edge of a panel, which conveyors and clamps can hold.
Rails often carry the global fiducials and tooling holes.
See [Rails, tooling holes and fiducials](../02-the-panel/02-rails-tooling-holes-fiducials.md).

**Reel.**
The usual packaging for surface-mount parts: carrier tape wound on a plastic reel.
See [Packaging: reels, cut tape, tubes, trays](../04-components-and-materials/02-packaging.md).

**Reference designator.**
The unique name of each part on a board, such as R12 or U3.
It links the part on the board to its line on the BOM.
See [Assembly data](../01-design-package/02-assembly-data.md).

**Reflow.**
Melting solder paste in an oven to solder surface-mount parts.
The temperature the board follows through the oven is called the reflow profile.
See [Reflow soldering](../05-assembly/03-reflow-soldering.md).

**Rework.**
Removing, replacing or resoldering parts on an assembled board.
See [Rework and repair](../05-assembly/11-rework.md).

**Router.**
The machine that cuts the board outline, slots and cut-outs with a spinning bit.
See [Profiling](../03-bare-board-fabrication/10-profiling.md).

**Selective soldering.**
Soldering through-hole parts one joint or one area at a time with a small fountain of molten solder.
See [Through-hole soldering](../05-assembly/05-through-hole-soldering.md).

**Shield.**
A metal can soldered over part of a board to block radio-frequency interference.
See [Shields, adhesives and underfill](../05-assembly/07-shields-adhesives-underfill.md).

**Solder bridge.**
Solder that joins two pads or leads that should not be joined.
See [Optical and X-ray inspection](../05-assembly/04-inspection.md).

**Solder mask.**
The coating, usually green, that covers the board except where parts are soldered.
It protects the copper and keeps solder off it.
A pad whose size is set by the mask opening, rather than by its copper, is called solder-mask defined.
See [Solder mask](../03-bare-board-fabrication/07-solder-mask.md).

**Solder paste.**
Tiny solder balls mixed with flux into a paste, printed onto pads through a stencil before parts are placed.
See [Solder paste printing and stencils](../05-assembly/01-solder-paste-and-stencils.md).

**Spares.**
Extra parts sent with a consigned kit to cover parts lost or damaged in setup and assembly.
It is also called overage or attrition.
See [Supplying your own parts (consignment) and spares](../04-components-and-materials/05-consignment-and-spares.md).

**SPI (solder paste inspection).**
A machine that measures the paste on every pad after printing, before parts are placed.
See [Solder paste printing and stencils](../05-assembly/01-solder-paste-and-stencils.md).

**Stack-up.**
The order, material and thickness of every copper and insulating layer in a board.
See [Materials and stack-up](../03-bare-board-fabrication/01-materials-and-stack-up.md).

**Static-shielding bag.**
A bag, usually silver-gray, with a metal layer that keeps static charge outside from reaching what is inside.
A pink anti-static bag only avoids making static itself; it does not shield.
See [Static (ESD) protection](../07-handling-packaging-and-shipping/01-static-protection.md).

**Stencil.**
A thin metal sheet with openings for each pad, through which solder paste is printed.
See [Solder paste printing and stencils](../05-assembly/01-solder-paste-and-stencils.md).

**Surface finish.**
The coating on exposed copper that protects it until soldering, such as ENIG, HASL or OSP.
See [Surface finish](../03-bare-board-fabrication/08-surface-finish.md).

**Surface mount.**
Parts soldered onto pads on the surface of the board, rather than through holes.
See [Through-hole soldering](../05-assembly/05-through-hole-soldering.md).

**Tented via.**
A via covered over with solder mask.
A plugged via is filled partly with resin, and a filled via is filled completely.
See [Via treatments](../03-bare-board-fabrication/06-via-treatments.md).

**Test point.**
A pad on a net that a test probe can touch.
See [Design for test: test points and access](../06-test-and-programming/01-test-points.md).

**Tg (glass transition temperature).**
The temperature at which board resin softens from rigid to rubbery.
Boards that see many heat cycles, or high working temperatures, use a higher-Tg material.
See [Materials and stack-up](../03-bare-board-fabrication/01-materials-and-stack-up.md).

**Thermal relief.**
A pad joined to a copper plane by a few narrow spokes, rather than solidly, so it doesn't lose heat too fast to solder.
See [Through-hole soldering](../05-assembly/05-through-hole-soldering.md).

**Through-hole.**
Parts with leads that pass through holes in the board and are soldered on the far side.
See [Through-hole soldering](../05-assembly/05-through-hole-soldering.md).

**Tombstoning.**
A defect in which a small chip part stands up on one end during reflow, because one end's solder melted and pulled before the other.
See [Footprints and the component library](../01-design-package/04-footprints.md).

**Tooling hole.**
A non-plated hole that locates a board or panel on pins in a machine or fixture.
See [Rails, tooling holes and fiducials](../02-the-panel/02-rails-tooling-holes-fiducials.md).

**Trace.**
A copper track that carries a signal or power between pads.
See [Outer layers](../03-bare-board-fabrication/05-outer-layers.md).

**Tray.**
A rigid plastic tray with a pocket for each part, used for large parts such as big BGAs and QFPs.
See [Packaging: reels, cut tape, tubes, trays](../04-components-and-materials/02-packaging.md).

**Tube.**
A plastic stick that holds parts in a row.
Tubes feed less reliably than reels, so this book recommends them only as a last resort.
See [Packaging: reels, cut tape, tubes, trays](../04-components-and-materials/02-packaging.md).

**Underfill.**
An adhesive flowed under a BGA or similar part after soldering, to strengthen its joints against shock and bending.
See [Shields, adhesives and underfill](../05-assembly/07-shields-adhesives-underfill.md).

**V-score.**
A V-shaped groove cut part-way through the board from both sides along a straight line, so the boards can be snapped apart.
See [Breakaway methods](../02-the-panel/03-breakaway-methods.md).

**Via.**
A small plated hole that joins traces on different layers.
See [Drilling](../03-bare-board-fabrication/03-drilling.md).

**Via-in-pad.**
A via placed inside a part's pad.
It is filled and plated over, so solder doesn't drain into it.
See [Via treatments](../03-bare-board-fabrication/06-via-treatments.md).

**Voiding.**
Gas bubbles trapped in a solder joint, which show as light spots on an X-ray.
See [Via treatments](../03-bare-board-fabrication/06-via-treatments.md).

**Warp and twist.**
How far a board departs from flat.
Bow is a curve along one direction, and twist is a curve across a diagonal.
See [Materials and stack-up](../03-bare-board-fabrication/01-materials-and-stack-up.md).

**Wave soldering.**
Soldering all the through-hole joints at once by passing the board over a wave of molten solder.
See [Through-hole soldering](../05-assembly/05-through-hole-soldering.md).

**X-out.**
A board in a panel that failed the fab's test and is marked with an X so it isn't assembled.
See [X-outs](../02-the-panel/05-x-outs.md).

**X-ray inspection.**
Inspection that looks through parts to see joints that are hidden, such as under BGAs and QFNs.
See [Optical and X-ray inspection](../05-assembly/04-inspection.md).

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

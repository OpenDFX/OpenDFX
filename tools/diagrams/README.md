# Book diagrams

Board views use Chris's color key (2026-11-05): gold = exposed copper, brown = exposed FR4, bright green = mask over copper, dark green = mask over FR4, white = silkscreen, black = holes, light gray = solder paste. Every diagram uses it (D1–D24 recoloured 2026-11-05).

Every drawing carries its diagram number, boxed in bold at the top left, with its recommendation IDs beside it (e.g. "D31 · PCB-DFA-008"), taken from the table below, so reviewers can refer to it.

Diagrams are drawn in Python with a shared style kit (`opendfx_draw.py`), so every diagram has the same look:
true scale in millimeters, numbered balloons with a key, real dimension lines, real text, and light and dark colors.

**Callouts** (Chris, 2026-11-12): every leader is straight, as in D65.
`Sheet.balloon(n, target, at, ...)` takes `at` only as the row or column to put the balloon in.
When the sheet is saved, each balloon slides along that row to sit straight below, above or beside its target, so its leader is one vertical or horizontal line.
Where targets are too close for that, the balloons spread apart and their leaders take one square jog, nested so that no two leaders cross.
Straight is the default, not a rule: what matters is that every leader is clean and points at one thing (Chris, PR #24 review).
- Keep balloons and leaders clear of labels, captions, dimension lines and their extension lines.
- Don't run a leader alongside, or in line with, a drawn line such as a shield wall, a lid or a silkscreen bar; it disappears into it.
- Point at the nearest example of the feature, so the leader doesn't cross another example on the way.
- Don't run a leader along a row of identical features (balls, vias); stop it at the first one it meets.
- Where an angled leader reads better, use `free=True`: the balloon stays exactly where `at` puts it, with one straight leader at any angle.
Check every drawing after changing a callout.

**Print sizes** (DRW1, Q172 and Q174 to Q177, Chris, 2026-11-13): every drawing is printed at the print version's text width of 175.9 mm, or 200 mm tall at most.
At that size, text is at least 7 pt and lines are at least 0.75 pt, the print-on-demand minimums.
The kit doesn't stop at the minimum where there's room: labels print at 8.5 pt, titles at 10 pt, notes at 7.5 pt, and lines at 0.8 pt or more.
The scripts still give sizes in drawing units, as designed; the kit turns them into points for each sheet (`text_pt()`, `line_pt()`, `Sheet.fs()`, `Sheet.sw()`), so a wide drawing gets larger text in its own units.
Balloons, key rows, arrowheads and dimension offsets grow by the same factor (`Sheet.f`), so lay out with offsets multiplied by `s.f`.
A drawing too wide for its text is redrawn taller, with its key below in two columns (`Sheet.key(..., only=...)`), on a normal page; nothing is printed sideways (Q177).
Where a small filled shape reads by its fill alone, it has no thin outline (Q176).
The same drawings serve the website and the books (Q175).
After changing a drawing, run `node tools/diagrams/check_print.js <svg>...`: it reports small text, thin lines, overlapping text and text off the drawing.

Parts 2 and 3 swapped places on 2026-11-12 (Q127): the panel is now Part 2 and bare-board fabrication Part 3. The scripts kept their old names, so `trial_diagrams.py` draws the panel and `part2_diagrams.py` draws bare-board fabrication.

**Font** (FONT1, Q182 and Q210, Chris, 2026-11-14): every drawing uses Atkinson Hyperlegible Next, with OpenDFX Symbols for ✓, ✗, ★, ⚠ and arrows (see `fonts/README.md`).
`embed_fonts.py` puts a subset of each weight a drawing uses inside the drawing when `Sheet.save()` writes it, holding only the characters it uses, about 16 KB per drawing.
A drawing shown on a web page is an image and can't use the page's fonts, so without this a reader without Atkinson installed would see another font.
After changing the kit or a script, check for labels that grew into each other; Atkinson's slashed zero is deliberate.

**Every diagram follows the book's own recommendations**, even where it's about something else: a chip part is drawn on the recommended footprint (PCB-DFA-029), fine-pitch pads have mask dams (PCB-DFA-032), and so on. Only a part marked ✗ as the bad example may break a rule, and only the rule it's showing.

Run `python3 tools/diagrams/trial_diagrams.py` (Part 2, the panel) to regenerate the review copies in `trials/` (PNG copies sit next to them for quick viewing).
Run it with `--book` to write the finished SVGs into `book/02-the-panel/images/`, the files the book pages use.
Part 5's diagrams work the same way with `part5_diagrams.py`, writing to `book/05-assembly/images/`, and Part 1's with `part1_diagrams.py`, writing to `book/01-design-package/images/`, and Part 3's (bare-board fabrication) with `part2_diagrams.py`, writing to `book/03-bare-board-fabrication/images/`, and Part 4's with `part4_diagrams.py`, writing to `book/04-components-and-materials/images/`, and Part 0's with `part0_diagrams.py`, writing to `book/00-start-here/images/`.

| ID | Diagram | File |
|---|---|---|
| D1 | Panel anatomy | `trials/python-1-panel-anatomy.svg` |
| D2 | Fiducial detail | `trials/python-2-fiducial-detail.svg` |
| D3 | Clearances at a V-score line | `trials/python-3-vscore-clearance.svg` |
| D4 | Recessing the board edge at a breakaway tab (PCB-DFA-012) | `trials/python-4-recessed-tab.svg` |
| D5 | Mouse-bite clearances | `trials/python-5-mouse-bite-clearance.svg` |
| D6 | Stencil area ratio (PCB-DFA-020) | `trials/python-6-stencil-area-ratio.svg` |
| D7 | Which parts go on which side of a double-sided board (PCB-DFA-024) | `trials/python-7-double-sided-plan.svg` |
| D8 | Part spacing and a tall part's shadow (PCB-DFA-023) | `trials/python-8-part-spacing.svg` |
| D9 | An 0402 footprint and the gap between its pads (PCB-DFA-029) | `trials/python-9-chip-footprint.svg` |
| D10 | A solder mask dam between fine-pitch pads (PCB-DFA-032) | `trials/python-10-mask-dam.svg` |
| D11 | Pin-1 and polarity marks done well and badly (PCB-DFA-034, 035) | `trials/python-11-polarity-marks.svg` |
| D17 | Selective-soldering keep-out around through-hole pins (PCB-DFA-043) | `trials/python-17-selective-keepout.svg` |
| D18 | Pin-in-paste: paste printed beyond the hole (PCB-DFA-041) | `trials/python-18-pin-in-paste.svg` |
| D19 | Thermal relief on a through-hole pad in a plane (PCB-DFA-044) | `trials/python-19-thermal-relief.svg` |
| D20 | One-piece and two-piece RF shields (PCB-DFA-050) | `trials/python-20-rf-shields.svg` |
| D21 | The gap under a QFN and under a BGA (PCB-DFA-057) | `trials/python-21-cleaning-gap.svg` |
| D23 | Sizing a plated through-hole and its pad from the lead (PCB-DFA-037); image proposal I4, after Chris's slides | `trials/python-23-pth-sizing.svg` |
| D24 | A connector overhanging a breakaway edge: blocked V-score snap vs routed edge with relief cut-out (PCB-DFA-010); image proposal I11 | `trials/python-24-overhang-vscore.svg` |
| D25 | Two overhangs facing each other across a V-score: as placed, bent up and bent down, each blocked (PCB-DFA-010); image proposal I11 | `trials/python-25-overhang-facing.svg` |
| D22 | The recommended 0402 footprint, in the same series as D12–D16 (PCB-DFA-029) | `trials/python-22-chip-footprint-0402.svg` |
| D26 | Corner of a 0.5 mm-pitch QFN three ways: single trace, ground pads tied into a pour (copper fills the opening), thermal relief (PCB-DFA-033); image proposal I2 | `trials/python-26-pour-pad-mask.svg` |
| D27 | A connector footprint at the board edge: silkscreen stopping at the edge, vs drawn 3 mm past it (PCB-DFA-036); image proposal I3 | `trials/python-27-overhang-outline.svg` |
| D28 | A non-plated hole in a copper pour: pour up to the hole (looks plated) vs pour kept 0.2 mm back, with enlarged edges (PCB-DFM-007); image proposal I5 | `trials/python-28-nonplated-hole.svg` |
| D29 | A 15 × 10 mm board alone drops into the gap between machines; the same board in a 60 × 50 mm panel spans it (PCB-DFA-002); image proposal I7 | `trials/python-29-small-board-panel.svg` |
| D30 | A panel 200 mm across the oven rails sags; one 100 mm across stays flat (PCB-DFA-004); image proposal I8 | `trials/python-30-panel-sag.svg` |
| D31 | Local fiducials at two opposite corners of a BGA, with the board's own fiducials far away (PCB-DFA-008); image proposal I9 | `trials/python-31-local-fiducials.svg` |
| D32 | Rectangular boards V-scored edge to edge, beside round boards that need routed slots and tabs (PCB-DFM-001); image proposal I10 | `trials/python-32-outline-shapes.svg` |
| D33 | A board in its enclosure with 1 mm all round, a tab stub, and a critical edge marked for routing (PCB-DFA-011); image proposal I12 | `trials/python-33-enclosure-room.svg` |
| D34 | A surface-mount standoff (after a maker's M3 datasheet, locating collar; drawn with a plated hole as on most boards, Q91) with no paste in the footprint (no joint) vs the maker's four-segment paste openings (a fillet) (PCB-DFA-019); image proposal I16; redrawn 2026-11-07 (Q88) | `trials/python-34-standoff-paste.svg` |
| D35 | Retired 2026-11-07 (Q87): dropped with the parallel-capacitors advice in PCB-DFA-027. The number is not reused. | — |
| D36 | Two pins joined in copper: under the mask with a dam (two joints) vs bare copper between (looks like a bridge) (PCB-DFA-038); image proposal I20 | `trials/python-36-joined-pins.svg` |
| D37 | Side view of a hybrid USB-C receptacle: through-hole shell pegs, surface-mount signal pins (PCB-DFA-040); image proposal I21 | `trials/python-37-hybrid-usbc.svg` |
| D38 | Through-hole leads at 1.27 mm pitch: about 1 mm through, too short, too long and bridged (PCB-DFA-045); image proposal I22 | `trials/python-38-lead-length.svg` |
| D39 | A snap-in part held flat by barbed pegs, vs a top-heavy drop-in part tipping over before soldering (PCB-DFA-046); image proposal I23 | `trials/python-39-self-holding.svg` |
| D40 | A bolted connector soldered then tightened (flange bent, joints strained) vs tightened then soldered (PCB-DFA-048); image proposal I24 | `trials/python-40-bolt-first.svg` |
| D41 | Hold-downs for a heavy capacitor: a bracket screwed through the board, and a cable tie through two holes (PCB-DFA-051); image proposal I25 | `trials/python-41-hold-downs.svg` |
| D42 | Underfill under a BGA vs corner bonding, side and plan views (PCB-DFA-054); image proposal I26 | `trials/python-42-underfill-corners.svg` |
| D43 | An assembly drawing with do-not-coat areas round a connector, a switch and test points (PCB-DFA-061); image proposal I27 | `trials/python-43-coating-keepouts.svg` |
| D48 | One assembler's panel: three fiducial sizes, round on top and square on the bottom; side and part number on the rail (PCB-DFA-076, PCB-DFA-077, PCB-DFA-005) | `trials/python-48-panel-style.svg` |
| D44 | Zero rotation for six common packages (PCB-DFA-065) | `trials/python-44-zero-rotation.svg` |
| D45 | The IPC-4761 via treatments in cross-section (PCB-DFM-030 to 032) | `trials/python-45-via-treatments.svg` |
| D46 | Thermal vias under a QFN, right and wrong (PCB-DFA-075) | `trials/python-46-qfn-thermal-vias.svg` |
| D47 | Aspect ratio and annular ring (PCB-DFM-024, 026) | `trials/python-47-aspect-ratio-annular-ring.svg` |
| D49 | A via beside a pad: mask web, tented, or no web (PCB-DFA-078) | `trials/python-49-via-mask-web.svg` |
| D50 | BGA pads, copper-defined (NSMD) and mask-defined (SMD), in cross-section (PCB-DFA-079) | `trials/python-50-bga-pads.svg` |
| D51 | Allowing for the router: inside-corner radius, slot width and corner relief (PCB-DFM-042) | `trials/python-51-router-corners.svg` |
| D52 | Edge-connector fingers: hard gold, no mask, chamfered corners, beveled edge (PCB-DFM-038) | `trials/python-52-gold-fingers.svg` |
| D53 | Solder mask round a non-plated hole: cleared by 0.1 mm vs a thin ring that gets drilled (PCB-DFM-034) | `trials/python-53-npth-mask.svg` |
| D54 | A mask dam needs room: pads too wide, dam removed, room for a 0.1 mm dam (PCB-DFM-035, PCB-DFA-032) | `trials/python-54-dam-room.svg` |
| D55 | BGA pads straight in a pour vs joined by a short trace (PCB-DFA-082) | `trials/python-55-bga-pour.svg` |
| D12–D16 | The recommended 008004, 01005, 0201, 0603 and 0805 footprints (PCB-DFA-029) | `trials/python-12-chip-footprint-008004.svg` to `python-16-chip-footprint-0805.svg` |

The draw.io and KiCad files in this folder and in `kicad/` were trials for comparison.
KiCad example files will be offered for download alongside diagrams where a real board helps.
| D56 | How parts arrive: carrier tape (enlarged, to scale), reel, tube and tray (PCB-DFA-089, PCB-DFA-101) | `trials/python-56-packaging-types.svg` |
| D57 | One footprint that takes two packages (a leadless part inside a SOT-23-6), and two footprints side by side with one DNP (PCB-DFA-084) | `trials/python-57-dual-footprint.svg` |
| D58 | Consigned cut tape: one strip of 150 mm or more (50 mm minimum), every pocket filled, vs strips of ten at 40 mm (PCB-DFA-101, PCB-DFA-105) | `trials/python-58-cut-tape-length.svg` |
| D59 | A tube with every part the same way vs mixed (PCB-DFA-101) | `trials/python-59-tube-orientation.svg` |
| D60 | What goes in a moisture barrier bag: heat seal, desiccant, humidity card, caution label (PCB-DFA-094, PCB-DFA-102) | `trials/python-60-moisture-bag.svg` |
| D61 | Test point size, spacing and keep-outs: 1.0 mm pads 2.54 mm apart (0.8 and 1.9 minimum), 1 mm from a short part, clear of a tall part and the gripped edge strip (PCB-DFT-008, PCB-DFT-009) | `trials/python-61-test-points.svg` |
| D62 | Probes reaching a board: all test points on the bottom with one plate of probes, vs a test point on top beside a tall part (PCB-DFT-009, PCB-DFT-011) | `trials/python-62-probe-access.svg` |
| D63 | Pads for a six-pin spring-pin programming cable, after one maker's footprint: pads, locating holes, keep-out (PCB-DFT-013) | `trials/python-63-spring-pin-pads.svg` |
| D64 | A boundary-scan chain: TDI through each chip to TDO, TCK, TMS and TRST shared, brought to a connector (PCB-DFT-012) | `trials/python-64-boundary-scan-chain.svg` |
| D65 | A board packed to ship: anti-static bubble wrap inside a sealed static-shielding bag in a box, vs a pink anti-static bag on its own (PCB-DFA-109, PCB-DFA-114) | `trials/python-65-packed-board.svg` |
| D66 | From prototype to production in steps: 5, 20, 200, 1,000, then full volume in batches of whole panels, with first articles marked (PCB-DFA-122, PCB-DFA-123) | `trials/python-66-production-ramp.svg` |
| D67 | The path a board takes: the design package, the panel, bare-board fabrication, assembly, test and programming, packing and shipping, with parts feeding into assembly and working with a manufacturer under every step (Part 0.3) | `trials/python-67-board-path.svg` |
| D68 | Legend beside vias, over tented vias (acceptable, slightly distorted) and over open vias (clipped), with a cross-section of ink over a tented via (PCB-DFM-045) | `trials/python-68-legend-over-vias.svg` |
| D69 | Designators that read from two edges of the board, not four (PCB-DFA-127) | `trials/python-69-legend-orientation.svg` |
| D70 | A callout box: a box round tightly packed parts and a map box beside it with their designators in the same places (PCB-DFA-128) | `trials/python-70-legend-callout-box.svg` |

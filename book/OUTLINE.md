# OpenDFX for Printed Circuit Boards: outline v0.2

Organized by how a board is actually built, in order.
Each chapter opens with a short "what happens at this step", then "what your design controls", then the recommendations.
Recommendations are tagged DFM / DFA / DFT / DFC so the same structure grows as new X's are added.

## Part 0: Start here
- 0.1 How to use this book (for people and for AI tools)
- 0.2 How recommendations are numbered and tagged
- 0.3 The path a board takes: from design files to delivered product
- 0.4 Classes and standards in one page (IPC Class 1/2/3 and others)

## Part 1: The design package (what you send)
- 1.1 Fabrication data: Gerber / ODB++ / IPC-2581, drill files, fabrication drawing
- 1.2 Assembly data: placement (XY) file, assembly drawing, notes
- 1.3 The BOM (bill of materials)
- 1.4 Footprints and the component library

## Part 2: The panel (where fabrication meets assembly)
- 2.1 Why boards are built in panels
- 2.2 Rails, tooling holes and fiducials
- 2.3 Breakaway methods: V-score, tabs, mouse bites
- 2.4 Clearance near board and panel edges
- 2.5 X-outs (accepting panels with a bad board)

## Part 3: Bare board fabrication
- 3.1 Materials and stack-up (laminates, copper weight, thickness, controlled impedance)
- 3.2 Inner layers: imaging and etching
- 3.3 Lamination
- 3.4 Drilling (mechanical, laser, aspect ratio, annular ring)
- 3.5 Plating
- 3.6 Outer layers: imaging and etching
- 3.7 Via treatments (tented, plugged, filled, via-in-pad)
- 3.8 Solder mask
- 3.9 Surface finish
- 3.10 Legend (silkscreen)
- 3.11 Profiling: routing, scoring, slots and cut-outs
- 3.12 Bare board electrical test and inspection

## Part 4: Components and materials
- 4.1 Choosing parts that can be bought and built
- 4.2 Packaging: reels, cut tape, tubes, trays
- 4.3 Moisture-sensitive parts
- 4.4 Sourcing, counterfeits and obsolescence
- 4.5 Supplying your own parts (consignment) and spares

## Part 5: Assembly
- 5.1 Solder paste printing and stencils
- 5.2 Paste inspection
- 5.3 Component placement (spacing, orientation, polarity, package choice)
- 5.4 Reflow soldering (profiles, thermal mass, double-sided boards)
- 5.5 Optical and X-ray inspection
- 5.6 Through-hole soldering: selective, wave, pin-in-paste, hand
- 5.7 Press-fit and mechanical parts
- 5.8 Shields, adhesives and underfill
- 5.9 Cleaning
- 5.10 Conformal coating
- 5.11 Depanelization
- 5.12 Rework and repair

## Part 6: Test and programming
- 6.1 Design for test: test points and access
- 6.2 Flying probe and in-circuit test
- 6.3 Boundary scan
- 6.4 Programming
- 6.5 Functional test and fixtures
- 6.6 Burn-in, stress testing and early failures
- 6.7 First articles

## Part 7: Handling, packaging and shipping
- 7.1 Static (ESD) protection
- 7.2 Moisture and storage
- 7.3 Packaging and shipping assembled boards

## Part 8: Working with a manufacturer
- 8.1 What drives cost and lead time
- 8.2 Prototype vs production
- 8.3 Design reviews and communicating intent

## Appendices
- A. Pre-release checklist (every recommendation as one checkable line)
- B. Index by design stage: schematic, library, placement, routing, release
- C. Glossary
- D. Standards referenced
- E. Sources

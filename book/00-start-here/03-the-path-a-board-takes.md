# The path a board takes

A board passes through several factories, or several departments of one factory, between your design files and a finished product.
Each step has its own machines, and each machine has its own needs.
Most of the advice in this book comes from meeting those needs.
This page follows a board along the path, and points to the Part of the book that covers each step.

![D67: A flow diagram, not to scale. Six steps run left to right: the design package (Part 1), the panel (Part 2), bare-board fabrication (Part 3), assembly (Part 5), test and programming (Part 6), and packing and shipping (Part 7). Components and materials (Part 4) feed into assembly from above. A bar under every step shows working with a manufacturer (Part 8).](images/board-path.svg)

*D67 is a flow diagram, not to scale.
Six steps run left to right, each with the Part of the book that covers it.
Components and materials feed into assembly from above, alongside the bare boards.
A bar under every step shows working with a manufacturer, which runs through the whole path.*

## The design package

Everything starts with the files you send.
The fab needs the copper, solder mask, legend and drill data, a netlist and a fabrication drawing.
The assembler needs the placement file, the BOM, the paste layer and an assembly drawing.
Anything missing or unclear turns into a question, and every question adds time.
See [Part 1: The design package](../01-design-package/01-fabrication-data.md).

## The panel

Once the order comes in, the manufacturer's CAM engineers prepare your data for production.
Part of that work is placing your boards into a panel.
The panel, not the single board, is what the fab makes and the assembly machines carry.
It holds several copies of your board, or one board with extra material around it.
It has rails for the machines to hold, and fiducials for their cameras to find.
The boards are held in by V-scores or tabs until they are separated after assembly.
The panel is set by the assembler's machines, so it is best designed with the assembler, before the bare boards are ordered.
See [Part 2: The panel](../02-the-panel/01-why-panels.md).

## Bare-board fabrication

The fab builds the bare boards, in their panel.
It images and etches the inner layers, presses them together with prepreg, drills the holes and plates them.
Then it images and etches the outer layers, and adds solder mask, the surface finish and the legend.
It cuts the panel's outline, with the V-scores or tabs that hold the boards in.
Finally it tests every board for open and short circuits.
See [Part 3: Bare board fabrication](../03-bare-board-fabrication/01-materials-and-stack-up.md).

## Components and materials

While the boards are being made, the parts are bought, or supplied by you.
They arrive on reels, in tubes or in trays, and some must be kept dry until they are used.
Parts that are hard to buy can delay a build more than any other step.
See [Part 4: Components and materials](../04-components-and-materials/01-choosing-parts.md).

## Assembly

The assembler prints solder paste onto the pads through a stencil and checks it.
A pick-and-place machine fits the surface-mount parts, and a reflow oven solders them.
Machines then inspect the joints with cameras, and with X-rays where joints are hidden.
Through-hole parts are soldered after that, by machine or by hand.
Some boards are then cleaned or coated, and finally the boards are separated from the panel.
See [Part 5: Assembly](../05-assembly/01-solder-paste-and-stencils.md).

## Test and programming

The assembled boards are tested, and their programmable parts are loaded with firmware.
Test can be a flying probe, a bed-of-nails fixture, boundary scan or a functional test that powers the board.
Each needs a way to reach the board, which has to be designed in.
See [Part 6: Test and programming](../06-test-and-programming/01-test-points.md).

## Packing and shipping

Finished boards are packed against static and moisture, and shipped.
The same care applies to boards and parts you store yourself.
See [Part 7: Handling, packaging and shipping](../07-handling-packaging-and-shipping/01-static-protection.md).

## Working with a manufacturer

All along the path, how you work with your manufacturer affects cost, lead time and quality.
That includes how you get a quote, how you move from prototype to production, and when you bring the manufacturer into your design review.
See [Part 8: Working with a manufacturer](../08-working-with-a-manufacturer/01-cost-and-lead-time.md).

*Last reviewed: 2026-11-12*

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

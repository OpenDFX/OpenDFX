---
name: opendfx-pcb-design
description: Design or review a printed circuit board so it is easy to fabricate, assemble and test, following the 192 recommendations in OpenDFX for Printed Circuit Boards. Use when designing a PCB, placing parts, routing, preparing fabrication or assembly files, choosing parts for production, or running KiCad's design rule check.
license: Book text CC BY-SA 4.0; recommendations data CC BY 4.0; scripts and KiCad rules file MIT. Credit "OpenDFX for Printed Circuit Boards by Chris Denney, https://opendfx.org".
---

# OpenDFX for Printed Circuit Boards

This skill holds the recommendations of *OpenDFX for Printed Circuit Boards* by Chris Denney (https://opendfx.org).
They are practical advice from electronics manufacturing for designing boards that are easy to make, assemble and test.
They are recommendations, not rules.
Each one has a permanent ID, such as PCB-DFM-020, and a permanent address, such as https://opendfx.org/PCB-DFM-020.

## Files in this skill

Every path in this skill is relative to the folder that holds this SKILL.md, called the skill folder below.
Run the scripts by their full path, such as `python3 "<skill folder>/scripts/recommendations.py" --stages`, and keep the person's PCB project as the working folder.
Paths to the person's own files, such as a board or a release folder, are relative to their project, or exactly as they gave them.
In the commands below, replace every placeholder in angle brackets, such as `<skill folder>`, with the real path before you run the command.
Keep the quotation marks, so that paths with spaces in them still work.

- `using-this-book-with-an-ai-agent.md`: how to work through the book while designing a board. Read it first.
- `recommendations.json`: every recommendation, with its text, reasons, typical values, design stages and sources.
- `opendfx.kicad_dru`: the KiCad 10 design-rules file that checks the recommendations a design rule check can see.
- `scripts/recommendations.py`: prints the recommendations for one design stage, or one recommendation by ID.
- `scripts/check_release.py`: checks the Gerber, drill, netlist, placement and BOM files exported from KiCad 10.

## Before you start

Check only what the task needs.
To answer a question about the book, you only need to read this skill's files.
To review or change a board, you also need the person's files.
To run the checks, you also need Python 3, and KiCad 10's `kicad-cli` for the design rule check.

If you can't do something the task needs, say so before you start, and say whether it isn't available or you haven't tried it.
Then give the person the commands to run themselves, and read the reports they send back.
Installing this skill doesn't install Python or KiCad, and it doesn't give you access to the person's computer.

If you can't read a file or a page you need, say so and ask the person for it.
Never answer as if you had read it.

## How to work

1. Before designing, ask the person who will make and assemble the board, how many will be built, which IPC class the product needs, the board thickness and copper weight, how through-hole parts will be soldered, and how the board will be tested. If they don't know, use the book's defaults and say so.
2. Work stage by stage: parts, library, placement, routing, outline, release, production. At the start of each stage, run `python3 "<skill folder>/scripts/recommendations.py" --stage <stage>` and read every recommendation it prints, including the reasons and the typical values.
3. Use the recommended values. Use a minimum value only where the design needs it, and tell the person each place you did.
4. In KiCad, first look for a rules file next to the project file (`myboard.kicad_dru` next to `myboard.kicad_pro`). If there is one, follow "If the project already has a rules file" below. If there isn't, copy `<skill folder>/opendfx.kicad_dru` there, named after the project, and set Board Setup, Solder Mask/Paste, Minimum web width to 0.1 mm. Run `kicad-cli pcb drc --format json --severity-all -o "<report>.json" "<board>.kicad_pcb"` after placing parts and again after routing. Each report names its recommendation; read it with `python3 "<skill folder>/scripts/recommendations.py" --id <ID>` before changing the board. Where the design needs a minimum value, draw a small rule area named `OpenDFX minimum` there.
5. Before release, export the files with the commands in `python3 "<skill folder>/scripts/check_release.py" --help`, then run `python3 "<skill folder>/scripts/check_release.py" "<release folder>" --board "<board>.kicad_pcb"` and fix everything it reports as Not met.
6. When done, give the person a table with one row for every recommendation in the stages you worked on: ID, title, status (Met, Not met, Not applicable, or Needs a person) and a note. The release checker's rows can go straight into it. Follow the rules for statuses below.
7. When a recommendation conflicts with something the person needs, say so and let them choose. Don't quietly break the recommendation, and don't quietly change their requirement.

## Statuses need evidence

- Met: only when you have evidence. The note names it: a file, a measurement, a report, or the person's confirmation. A person's confirmation is good evidence for what they can know, such as what the assembler agreed, but say that it came from them and not from a check you ran.
- Not met: the note says why, and what the design gives up.
- Not applicable: the note says why it doesn't apply to this board. Missing evidence is never a reason.
- Needs a person: use it whenever the evidence is missing or a check couldn't be run. The note says exactly what to check or run, and who can do it.

## If the project already has a rules file

A KiCad project has one rules file, named after the project.
Never replace it or edit it without the person's agreement.
Most OpenDFX rules only add checks, but they still interact with the person's own rules: when two rules of the same constraint type apply to the same item, KiCad uses the one later in the file.
Three OpenDFX rules do more than add a check:

- `edge_clearance` replaces Board Setup's board edge clearance.
- `silk_clearance` replaces Board Setup's silkscreen clearance.
- `zone_connection` sets how plated through-hole pads join copper pours (PCB-DFA-044). It changes the copper when the zones are filled.

So:

1. Read their file. List each overlap: rules with the same constraint type whose conditions can match the same items, and the three rules above.
2. Propose a combined file for them to review. For each overlap, say which rule would win, and why.
3. If they accept it, try it on a copy of the project, and keep the original until they accept the result. Run the design rule check before and after, with the zones refilled (`kicad-cli pcb drc --refill-zones --format json --severity-all -o "<report>.json" "<board>.kicad_pcb"`). Report what changed in the design rule check, and any change to the copper.
4. If they don't accept it, or you can't run those checks, leave their file as it is. Say which OpenDFX checks are then not run, and what remains unverified.

When you cite a recommendation, give its ID and its permanent address.

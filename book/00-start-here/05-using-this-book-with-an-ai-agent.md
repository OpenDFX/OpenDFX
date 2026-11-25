# Using this book with an AI agent

This book is written to be read by AI agents that design circuit boards, as well as by people.
This page is for both.
It tells an agent how to work through the book while it designs a board.
It also tells the person directing the agent what to ask for, and what to expect back.

## Give the agent the book

There are three ways to give an AI tool the book.
The simplest, for any chat tool, takes three steps: download one file, attach it to a new chat, and paste one prompt.
The steps and the prompt are at [opendfx.org/ai](https://opendfx.org/ai/).

The first is the Agent Skill, which is a folder of instructions and files that many AI agents can load by themselves.
Download it from [opendfx.org/opendfx-pcb-design.zip](https://opendfx.org/opendfx-pcb-design.zip).
It holds a short version of this page, the recommendations data file, the KiCad design-rules file, the release checker, and a small script that prints the recommendations for each design stage.
For a coding agent, put the skill's folder in your own PCB project, in the folder where your tool looks for skills.
For a chat tool that supports skills, upload the zip file as the tool's documentation describes.
Installing the skill doesn't install Python or KiCad, and it doesn't give the agent access to your computer.

The second is the whole book as one file, [opendfx.org/llms-full.txt](https://opendfx.org/llms-full.txt).
Attach it to a chat, or add it to a project in any AI tool that accepts files.
An uploaded file is a copy of the book on the day you downloaded it.
When the book changes, download the file again, replace the old copy, and start a new chat.
The [change log](https://opendfx.org/changelog/) lists what changed in each version.

The third is a block of instructions for your project, described in the next section.
The agent then fetches only what it needs from the website while it works.

The whole book is long, so an agent that needs only part of it can fetch just that part.
Every page of the book is also published as plain Markdown, at its web address with `.md` added in place of the final slash.
For example, the page at `opendfx.org/02-the-panel/04-edge-clearance/` is also at `opendfx.org/02-the-panel/04-edge-clearance.md`.
Every recommendation is also published on its own as Markdown, at its permanent address with `.md` added, such as `opendfx.org/PCB-DFA-006.md`.

## Or add the book to your project's instructions

Many AI coding and design tools read a file of standing instructions from the project folder.
Claude Code reads `CLAUDE.md`, and Codex and many other agents read `AGENTS.md`.
Cursor reads the files in `.cursor/rules/`, and GitHub Copilot reads `.github/copilot-instructions.md`.
Paste the block below into whichever file your tool reads.
This is the file in your own PCB project.
OpenDFX's own `AGENTS.md` is for people changing the book, so don't copy it into your project.

```markdown
## PCB design: follow OpenDFX

When you design or review a printed circuit board in this project, follow
OpenDFX for Printed Circuit Boards by Chris Denney (https://opendfx.org).

- Read https://opendfx.org/llms.txt first. It explains how to use the book.
- Before you design, ask me who will make and assemble the board, how many
  will be built, the IPC class, the board thickness and copper weight, how
  through-hole parts will be soldered, and how the board will be tested.
  If I don't know, use the book's defaults and say which you used.
- Work stage by stage: parts, library, placement, routing, outline, release,
  production. At each stage, read that stage's recommendations from
  https://opendfx.org/data/recommendations.json (field design_stages).
  Fetch one recommendation as Markdown at https://opendfx.org/<ID>.md.
- Use the recommended values. Use a minimum value only where the design
  needs it, and tell me each place you did.
- In KiCad, run the design rule check with the OpenDFX rules file
  (https://opendfx.org/kicad/) after placement and after routing.
- Cite each recommendation by its ID and its address, such as
  PCB-DFA-006 and https://opendfx.org/PCB-DFA-006.
- Never replace or change an existing .kicad_dru rules file without asking me.
- If you can't read a file or a page, or can't run a check, say so and ask
  me for it. Don't answer as if you had read it.
- When a recommendation conflicts with something I need, tell me and let me
  choose.
- Mark a recommendation Met only when you can name the evidence: a file, a
  measurement, a report, or something I confirmed.
- When you finish, give me a table of every recommendation in the stages you
  worked on: ID, title, status (Met, Not met, Not applicable or Needs a
  person) and a note.
```

## Say what the agent can and can't do

Before it starts, the agent should check what the task needs, and only that.
To answer a question about the book, it only needs to read the book.
To review or change a board, it also needs the person's files.
To run the checks, it also needs Python 3, and KiCad 10 for the design rule check.

If it can't do something the task needs, it should say so before it starts, and say whether that isn't available or hasn't been tried.
It should then give the person the commands to run, and read the reports they send back.
If it can't read a file or a page it needs, it should say so and ask for it, rather than answer as if it had read it.

## Start with the questions only the person can answer

Many recommendations depend on how the board will be built.
So before it starts, the agent should ask the person these questions, and write the answers down.

1. Who will make the bare board, and who will assemble it?
   If they publish their own limits, their limits come first ([PCB-DFA-124](../08-working-with-a-manufacturer/03-design-reviews-and-communication.md#pcb-dfa-124-bring-your-manufacturer-into-the-design-review-before-the-design-is-final)).
2. How many boards will be built, now and later?
   Volume decides many choices, such as panels, test fixtures and part packaging.
3. Which IPC class does the product need?
   Most products need Class 2 ([PCB-DFT-003](../03-bare-board-fabrication/11-bare-board-test.md#pcb-dft-003-ask-for-ipc-class-2-unless-the-product-needs-class-3-and-know-class-3-is-a-design-standard-too)).
4. How thick is the board, and how heavy is the copper?
   The book's trace and gap values are for 1 oz finished copper ([PCB-DFM-020](../03-bare-board-fabrication/01-materials-and-stack-up.md#pcb-dfm-020-size-traces-and-gaps-for-the-finished-copper-weight)).
5. How will any through-hole parts be soldered: by hand, by selective soldering or by wave soldering?
6. How will the board be tested: by flying probe, by a bed-of-nails fixture, or only by a functional test?

If the person doesn't know an answer, the agent should use the book's default and say which default it used.

## Give the agent your board

The more the agent can see, the more it can check.
Give it the answers to the questions above, and the files for the work it is doing.
For a review, that is usually the KiCad project folder, or the release folder of Gerber, drill, netlist, placement and BOM files.
If the agent can't run KiCad or the release checker, run them yourself, and give it the reports.
The design rule check's JSON report and the release checker's report are written to be read by an agent.
Tell it what you know that the files can't show, such as what the assembler agreed.

Every fact shown in a drawing is also written in the text.
If you want the agent to look at the drawing itself, give it the drawing's web link.
If it can't view the drawing, attach the relevant PDF page or a PNG or JPEG of the drawing directly to the chat.

## Work through the design stage by stage

[Appendix B: Index by design stage](../09-appendices/02-design-stage-index.md) lists every recommendation under the stage where it matters.
The [recommendations data file](https://opendfx.org/data/recommendations.json) gives the same stages in the field `design_stages`.
At the start of each stage, the agent should read that stage's recommendations in full, including the Why and the Typical values.
Then it should do the work for that stage.

The stages, in order, are:

1. Parts and schematic.
2. Library and footprints.
3. Placement.
4. Routing and copper.
5. Board outline and panel.
6. Release.
7. Ordering and production.

Where a recommendation gives a minimum and a recommended value, the agent should use the recommended value.
It should use the minimum value only where the design needs it, and tell the person each place it did.

## Check the board with KiCad's design rule check

For a board designed in KiCad, the agent should use the [OpenDFX design-rules file](https://opendfx.org/kicad/).
If the project already has a rules file of its own, the agent should first follow the next section.
It should run KiCad's design rule check after placing the parts, and again after routing.
The command `kicad-cli pcb drc --format json --severity-all` gives a report that an agent can read.

Each report names the recommendation it comes from and gives its permanent address, such as opendfx.org/PCB-DFM-020.
Before it changes the board, the agent should read that recommendation, so it fixes the cause and not only the symptom.
Where the design really needs a minimum value, the agent should draw a small rule area named `OpenDFX minimum` there, rather than change the rules.

The design rule check can only see the board.
It can't see the BOM, the drawings, the panel or the conversations with the manufacturer.
So a clean check doesn't mean every recommendation is met.

## If the project already has a rules file

A KiCad project has one rules file, named after the project.
If the project already has one, the agent should never replace it or change it without the person's agreement.
Most OpenDFX rules only add checks, but three replace a Board Setup value or a setting: the board edge clearance, the silkscreen clearance, and how plated through-hole pads join copper pours.
And when two rules of the same kind apply to the same item, KiCad uses the one later in the file.
So the agent should list where the two files overlap, and propose a combined file for the person to review.
If the person accepts it, the agent should try it on a copy of the project, refill the zones, and report any change in the check and in the copper.
Otherwise it should leave the person's file as it is, and say which OpenDFX checks are then not run.

## Check the release files

Before the files go to the fab and the assembler, the agent should check them with the OpenDFX release checker, `check_release.py`.
It comes with the Agent Skill, and it is also at [opendfx.org/check_release.py](https://opendfx.org/check_release.py).
It reads the Gerber files, the drill files, the netlist, the placement file and the BOM exported from KiCad 10.
It checks what those files can show, such as Gerber X2 files, separate drill files for plated and non-plated holes, a placement file in millimeters, and a BOM with a part number on every fitted line.
Its help text lists the KiCad commands that export a release the way this book recommends.
Its report uses the same statuses as the table below, so its rows can go straight into that table.

## Hand back a table of every recommendation

When the design is done, the agent should give the person a table with one row for every recommendation in the stages it worked on.
Each row should have the recommendation's ID, its title, a status, and a note.
The status should be one of these four.

| Status | Means |
|---|---|
| Met | The design follows the recommendation. The note names the evidence: a file, a measurement, a report, or something the person confirmed. |
| Not met | The design doesn't follow it. The note says why, and what the design gives up. |
| Not applicable | It doesn't apply to this board. The note says why. Missing evidence is never a reason. |
| Needs a person | Only a person can do it, such as agreeing a limit with the assembler, or the evidence is missing. The note says exactly what to check or do. |

For example:

| ID | Title | Status | Note |
|---|---|---|---|
| PCB-DFM-020 | Size traces and gaps for the finished copper weight | Met | Traces 0.15 mm wide or more on 1 oz copper. The KiCad check passed. |
| PCB-DFA-016 | Keep components back from breakaway edges, and ceramic capacitors further still | Met | Measured in KiCad: the nearest ceramic capacitor is 6 mm from the breakaway edge. |
| PCB-DFA-043 | Keep surface-mount parts away from through-hole pins on the solder side | Not met | Two pads of C12 are 2.4 mm from J1's pins, because the board outline is fixed. Inside an `OpenDFX minimum` area. |
| PCB-DFA-124 | Bring your manufacturer into the design review before the design is final | Needs a person | Send the design to the assembler for review before ordering. |

The agent should mark a recommendation Met only when it can name the evidence.
Something the person confirmed is good evidence for what they can know, such as what the assembler agreed.
But the note should say it came from the person, and not from a check the agent ran.

The person can then review the design by recommendation, instead of searching the board for problems.
Every "Not met" and every `OpenDFX minimum` area is a place to look closely.

## Ask the person when the book and the design disagree

These are recommendations, not rules.
When a recommendation conflicts with something the person needs, the agent should say so, and let the person choose.
It shouldn't quietly break the recommendation, and it shouldn't quietly change the person's requirement.

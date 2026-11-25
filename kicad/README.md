# OpenDFX for KiCad

The KiCad design-rules file (M12) and the files that build and test it.
How to use the file is on the website: https://opendfx.org/kicad/ (written from `site/src/content/docs/kicad.mdx`).

| File | What it is |
|---|---|
| `opendfx.kicad_dru` | The rules file for KiCad 10. Generated; don't edit it by hand. |
| `opendfx-starter/` | An empty starter project with the rules file and the Board Setup values it can't set, such as the solder mask web. |
| `tests/test_rules.py` | Draws a test board with one deliberate mistake for each rule, and a twin that just passes, then runs KiCad's design rule check and compares the reports. |
| `tests/opendfx-test.kicad_pcb` | The test board from the last run, to open in KiCad. |
| `check_release.py` | Checks a release folder exported from KiCad 10 (Gerber, drill, netlist, placement file and BOM) against the book (Q155). Its help text lists the export commands. Copied into the skill and the website by `tools/build_skill.py`. |
| `tests/test_release_check.py` | Draws a small board, exports a good release that must pass, then makes 18 mistakes one at a time and expects each to be caught. Needs KiCad 10. |
| `tests/test_export_commands.py` | Runs the five export commands from `check_release.py`'s help text, exactly as printed, through bash and zsh, from a folder path with spaces, with a tiny schematic. Checks the BOM's references, quantities and DNP values. Needs KiCad 10. |
| `examples/` | KiCad example boards for the book. |

## How it is built

The book is the one source of every number.

1. `tools/kicad_rules.yaml` lists each check: its recommendation IDs, its KiCad rule, and its minimum and recommended values as written in the book.
2. `python3 tools/build_kicad_rules.py` checks that every value appears in its recommendation's text, then writes the rules file, its copies in the starter project and `public/` (the website's download), and the website page.
3. `python3 tools/build_data.py` adds the same numbers to the data file, as `checks` (Q137).
4. `python3 tools/build_kicad_starter.py` rebuilds the starter project's Board Setup values from the same list. It needs KiCad 10.
5. `python3 kicad/tests/test_rules.py` proves every rule fires where it should and nowhere else. It needs KiCad 10.

The website's build runs step 2 with `--check`, so a stale rules file fails the build.

## Rules that only add

KiCad lets a later rule replace an earlier one, and a rules file replaces net class clearances and some Board Setup minimums.
A plain `clearance` rule of 0.15 mm, for example, silently switches off a 1 mm high-voltage net class.
So the OpenDFX rules use two kinds of constraint that are checked alongside KiCad's own:

- `assertion`, for a test on one item (trace width, hole size, annular ring, text size, test point pads);
- `physical_clearance` and `physical_hole_clearance` limited to different nets, for spacing.

Two rules use KiCad's own checks, because they measure the way designers expect.
They replace the Board Setup value of the same name: the board edge clearance (0.5 mm by default) and the silkscreen clearance (0 mm by default).
One rule is a setting: plated through-hole pads join pours through thermal reliefs (PCB-DFA-044).

## What was found while testing (KiCad 10.0.8, 2026-11-13)

- The rule area condition is `A.intersectsArea('OpenDFX minimum*')`; for spacing rules, either item inside the area counts.
- A misspelled property makes an assertion fail on every item, or, inside a sum, pass silently. On a via, the properties are `Diameter` and `Hole`; on a pad, `Size_X` and `Hole_Size_X`; on text, `Height` and `Thickness`.
- `L == '*.Mask'` limits the legend check to exposed copper, so legend over a masked trace isn't reported.
- `physical_hole_clearance` also measures silkscreen and drawing lines unless limited with `L == '*.Cu'`.
- The solder mask web can't be set by a rule. Board Setup's minimum web width merges narrower webs, and the check then reports a solder mask bridge.
- KiCad puts thermal spokes at 45 degrees on round pads.

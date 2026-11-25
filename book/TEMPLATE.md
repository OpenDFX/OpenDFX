# Page template

Every topic page follows the same layout.
Each recommendation inside it has a permanent number.
Numbers look like `PCB-DFM-014`: board type, which "X" (DFM manufacturing, DFA assembly, DFT test, DFC cleaning…), then a number that never changes.

```markdown
# <Topic title>

<One-paragraph plain-language intro: what this is and why a designer should care.>

## PCB-<X>-<nnn>: <Recommendation, written as a short imperative sentence>

**Recommendation:** <One or two sentences. Specific.>

**Why:** <What it does for the manufacturer and for you (yield, cost, lead time).>

**Typical values:** <Numbers, with units. Say if they are a common industry value or one shop's example.>

**What goes wrong if you don't:** <Concrete failure mode.>

**Example:** <Short real story, no customer names.>

**Applies to:** <General practice | Varies by manufacturer — check with yours>

**Sources:** <Full episode title as published, linked to its episode page, + date + timestamps; standards (e.g. IPC-7351); other references.>

*Last reviewed: <date>*

---
<!-- next recommendation -->

## Related pages
- <links>

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0 · <permanent URL of this page>*
```

---

## What goes in each section

"Why", "What goes wrong" and "Example" are about the same problem, so they blur easily.
Keep them apart:

| Section | Answers | Point of view | Usually starts like |
|---|---|---|---|
| **Why** | *How* the problem happens: the mechanism | The board, the machine, the physics | "Because…", "When the knife…", "Cameras need…" |
| **What goes wrong if you don't** | *What you'll see, and what it costs you* | The designer or buyer | "You'll see…", "You pay…", "Boards fail…" |
| **Example** | *Did it really happen?* One true story, no names | The factory floor | "A customer…", "One board…" |

- Test: if "What goes wrong" still reads well after the word "because", it's really a Why.
  Move it.
- If "What goes wrong" would only repeat the Why, leave it out.
  Every section except Recommendation and Sources is optional.
- Source text: **one sentence per line**, so reviewers can comment on exact sentences and diffs stay small.
  A blank line still separates paragraphs.
  Run `python3 tools/one_sentence_per_line.py <file>` to rewrap a page; it refuses to write if the rendered page would change.
- Sources: full episode title linked to its episode page, then the date, then timestamps.
  Each timestamp links to that moment: `https://www.buzzsprout.com/1066066/episodes/<id>?t=<seconds>`.

---

## Images, diagrams and tables

Welcome on any page.
Rules so they work for AI tools as well as people:
- **Tables** are real Markdown/HTML tables, never pictures of tables.
- **Diagrams** are SVG with real text labels, plus alt text and a one- or two-sentence description below saying what the diagram shows (the key numbers in words).
- **Photos** get alt text and a caption that states the lesson.
- **No fact lives only in an image.**
  Every number shown in a picture also appears in the text or a table.

---

# Worked example (early sketch; the reviewed version is `book/02-the-panel/02-rails-tooling-holes-fiducials.md`)

# Fiducials

Fiducials are small copper targets that assembly machines use to find exactly where your board is.
Nearly every machine on an assembly line has a downward-looking camera: the stencil printer, the pick-and-place machine, paste inspection, optical inspection, selective soldering, X-ray and flying-probe test.
Each one looks for fiducials first.
Adding them takes about five minutes of design time.

## PCB-DFA-006: Use plain round fiducials with a clear ring around them

**Recommendation:** Make each fiducial a round copper dot about 1 mm in diameter, with solder mask pulled back to a 2 mm circle, so a 0.5 mm ring of bare board surrounds the dot.
Don't use squares, crosses or other shapes.

**Why:** Cameras need a high-contrast target.
Glossy solder mask right next to the dot, especially white or yellow, reflects light and confuses the camera.
Modern vision systems don't need unusual shapes.

**Typical values:** 1 mm dot · 2 mm mask opening.
Common industry practice.

**What goes wrong if you don't:** The machine fails to find the board, the operator has to teach it by hand, and placement accuracy can suffer.

**Applies to:** General practice.

**Sources:** Pick, Place, Podcast, "What are fiducials and why you should use them" (Oct 2021), 23:00–26:00.

## PCB-DFA-007: Put at least two fiducials on each board, as far apart as you can

**Recommendation:** Place two fiducials near opposite corners, or three if the board is large or double-sided.
Put them on the individual board, not only on the panel rails.

**Why:** Two fiducials give the machine position and rotation.
A third lets it correct for the board stretching or shrinking slightly.
Fiducials on the board itself mean it can still be built if it's separated from its panel.

**Typical values:** 2 minimum, 3 preferred.
⚠️ *Chris to check: the episode notes say "within about 3 mm of the board edge".
Is that "at least 3 mm in from the edge"?*

**What goes wrong if you don't:** In one case a conveyor fault broke a panel apart.
Because each board had its own fiducials, the boards could still be built individually.

**Applies to:** General practice.
Distance from the edge varies by manufacturer.

**Sources:** Same episode, 10:00–14:00 and 19:00–27:00.

## PCB-DFA-008: Add local fiducials next to expensive or very fine-pitch parts

**Recommendation:** Add an extra pair of fiducials right beside high-value BGAs, fine-pitch parts and dense clusters of tiny parts (0201, 01005).

**Why:** The machine re-checks position right at that part, rather than relying on fiducials far away.

**Example:** A board carrying a single FPGA worth about $6,000 uses fiducials at the corners of the BGA.

**Applies to:** General practice.

**Sources:** Same episode, 28:00–30:00.

## PCB-DFA-009: Don't use drilled holes instead of fiducials

**Why:** Holes are drilled in a separate step from copper etching, so they never line up with the pads quite as precisely.
Fiducials are etched at the same time as the pads they help place.

**Sources:** Same episode, 19:00–20:00.

---
*From OpenDFX for Printed Circuit Boards by Chris Denney · CC BY-SA 4.0*

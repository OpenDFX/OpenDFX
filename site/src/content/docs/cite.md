---
title: How to cite
description: How to credit OpenDFX for Printed Circuit Boards when you reuse it, and how to cite the book or a single recommendation in a paper, a report or a design review.
editUrl: false
---

## In a design review

The recommendation's ID is enough, for example "see PCB-DFA-018".
Each ID is permanent.
It never changes, even when the advice is updated, and a retired ID is never reused.

To link to a recommendation, use its permanent address, which is the website followed by the ID.
For example, [opendfx.org/PCB-DFA-018](https://opendfx.org/PCB-DFA-018) always leads to PCB-DFA-018.

## When you reuse the text or drawings

The book is licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), so you may copy and adapt it, including commercially.
Give this credit with what you reuse:

> OpenDFX by Chris Denney, https://opendfx.org, CC BY-SA 4.0.

Share your adapted version under the same license.

The recommendations data files are licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), so a design tool can use them with credit alone.
The same credit works for them, with "CC BY 4.0" at the end.

## In a paper or a report

Cite the whole book like this:

> Denney, C. (2026). *OpenDFX for Printed Circuit Boards* (Version 1.0). https://opendfx.org

Cite a single recommendation by its ID, its title and its permanent address:

> Denney, C. (2026). PCB-DFA-018: Send the paste layer 1:1 with your copper pads. In *OpenDFX for Printed Circuit Boards* (Version 1.0). https://opendfx.org/PCB-DFA-018

The book is updated in public, so give the version you read.

## BibTeX

```bibtex
@book{denney_opendfx_2026,
  author = {Denney, Chris},
  title  = {OpenDFX for Printed Circuit Boards},
  year   = {2026},
  note   = {Version 1.0. Licensed under CC BY-SA 4.0},
  url    = {https://opendfx.org}
}
```

## Citation file

The book's repository has a [`CITATION.cff`](https://github.com/OpenDFX/OpenDFX/blob/main/CITATION.cff) file with the same details.
GitHub reads it and shows a "Cite this repository" button, and reference managers such as Zotero can import it.

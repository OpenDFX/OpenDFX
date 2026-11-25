"""Build the machine-readable files from the book's pages, so they never drift from the text.

Run: python3 tools/build_data.py          (writes the files)
     python3 tools/build_data.py --check  (exits 1 if any file is out of date)

Writes:
  data/recommendations.json   Every recommendation, one record each (CC BY 4.0)
  data/recommendations.yaml   The same records as YAML
  public/llms.txt             A short index of the book for AI tools (llmstxt.org format)
  public/llms-full.txt        The whole book as one Markdown file
  public/robots.txt           Lets every crawler in, AI crawlers named explicitly

It also checks the data file against its JSON Schema, data/recommendations.schema.json (written by hand),
when the jsonschema package is installed (the website workflow installs it).
The website build (tools/build_site.py) uses page_md_copy(), recommendation_md() and json_ld_page() below
to publish a Markdown copy of every page and every recommendation, and the structured data on each page (Q166).

`public/` is the website's static folder: the site (M9) serves these files at its root.
The page addresses come from page_url() below; change them there if the site's addresses change.
"""
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_appendices as ba  # noqa: E402  (shares the page parser, so both tools read the book the same way)
import build_kicad_rules as bk  # noqa: E402  (the numbers the KiCad rules file checks, M12)

ROOT = ba.ROOT
BOOK = ba.BOOK
DATA = ROOT / "data"
PUBLIC = ROOT / "public"

SITE = "https://opendfx.org"
REPO = "https://github.com/OpenDFX/OpenDFX"
BOOK_TITLE = "OpenDFX for Printed Circuit Boards"
AUTHOR = "Chris Denney"
# The version and year live in CITATION.cff (M11), so the citation is written in one place.
_CFF = (ROOT / "CITATION.cff").read_text()
VERSION = re.search(r'^version: "([^"]+)"', _CFF, re.M).group(1)
YEAR = re.search(r"^  year: (\d{4})", _CFF, re.M).group(1)
CITATION = f"Denney, C. ({YEAR}). {BOOK_TITLE} (Version {VERSION}). {SITE}"
SCHEMA_VERSION = "1.0"

FIELDS = [  # (label in the page, key in the data)
    ("Recommendation", "recommendation"),
    ("Why", "why"),
    ("Typical values", "typical_values"),
    ("What goes wrong if you don't", "what_goes_wrong"),
    ("Example", "example"),
    ("Applies to", "applies_to"),
]
FIELD_RE = re.compile(r"^\*\*(" + "|".join(re.escape(f) for f, _ in FIELDS + [("Sources", "")]) + r"):\*\*", re.M)
REVIEWED_RE = re.compile(r"^\*Last reviewed: (\d{4}-\d{2}-\d{2})\*", re.M)
FIGURE_RE = re.compile(r"!\[(D\d+): ([^\]]*)\]\(([^)\s]+)\)")
TIMESTAMP_RE = re.compile(r"\?t=(\d+)\)(?:–((?:\d+:)?\d+:\d{2}))?")
CATEGORY = {
    "DFA": "Design for assembly",
    "DFM": "Design for manufacturing (bare-board fabrication)",
    "DFT": "Design for test",
}
AI_CRAWLERS = ["ClaudeBot", "Claude-User", "Claude-SearchBot", "GPTBot", "OAI-SearchBot", "ChatGPT-User",
               "PerplexityBot", "Perplexity-User", "Google-Extended", "CCBot", "Applebot-Extended"]


def page_url(rel, anchor=None):
    """Website address of a book page, e.g. 02-the-panel/02-rails.md -> https://opendfx.org/02-the-panel/02-rails/."""
    url = f"{SITE}/{rel[:-3]}/"
    return f"{url}#{anchor}" if anchor else url


def permalink(rec_id):
    """Short permanent address that forwards to the recommendation, e.g. https://opendfx.org/PCB-DFA-006 (Q136).
    The website (M9) makes one forwarding page per ID."""
    return f"{SITE}/{rec_id}"


def absolute_links(text, rel):
    """Turn the book's relative links and image paths into full website addresses."""
    base = Path(rel).parent

    def fix(m):
        target = m.group(1)
        if re.match(r"[a-z]+:", target):
            return m.group(0)
        path, _, anchor = target.partition("#")
        if not path:
            return f"]({page_url(rel, anchor)})"
        resolved = (Path("/") / base / path).resolve().as_posix().lstrip("/")
        if resolved.endswith(".md"):
            return f"]({page_url(resolved, anchor or None)})"
        return f"]({SITE}/{resolved})"

    return re.sub(r"\]\(([^)\s]+)\)", fix, text)


def unwrap(text):
    """Join one-sentence-per-line source text into paragraphs; keep blank lines and list items."""
    out = []
    for para in re.split(r"\n\s*\n", text.strip()):
        lines = [l.strip() for l in para.splitlines() if l.strip()]
        if any(l.startswith(("- ", "* ", "| ")) or re.match(r"\d+\. ", l) for l in lines):
            out.append("\n".join(lines))
        else:
            out.append(" ".join(lines))
    return "\n\n".join(out)


def seconds(stamp):
    """'47:00' or '01:00:00' -> seconds."""
    total = 0
    for part in stamp.split(":"):
        total = total * 60 + int(part)
    return total


def parse_sources(src):
    """Split a Sources paragraph into episodes (with timestamps), standards and other documents."""
    episodes = []
    for m in ba.EPISODE_RE.finditer(src):
        title, url, eid, date = m.groups()
        # The timestamps are the links that follow this title, up to the next episode title or the end.
        nxt = ba.EPISODE_RE.search(src, m.end())
        chunk = src[m.end(): nxt.start() if nxt else len(src)]
        chunk = chunk.split(";")[0] if nxt else chunk
        stamps = []
        for t in TIMESTAMP_RE.finditer(chunk):
            start = int(t.group(1))
            end = seconds(t.group(2)) if t.group(2) else None
            stamps.append({"start_seconds": start, "end_seconds": end,
                           "url": f"https://www.buzzsprout.com/1066066/episodes/{eid}?t={start}"})
        episodes.append({"title": title, "url": url.split("?")[0], "date": date, "timestamps": stamps})
    standards = sorted(set(ba.STD_RE.findall(src)))
    others = []
    for m in ba.LINK_RE.finditer(src):
        label, url = m.groups()
        if "buzzsprout.com/1066066" in url:
            continue
        others.append({"title": label.strip("“”\""), "url": url})
    return episodes, standards, others


def fields(body):
    """{key: markdown} for each labeled section of one recommendation."""
    labels = dict(FIELDS)
    out = {}
    hits = list(FIELD_RE.finditer(body))
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(body)
        text = body[m.end():end]
        text = REVIEWED_RE.split(text)[0]
        text = re.split(r"^---\s*$", text, flags=re.M)[0]
        text = FIGURE_RE.sub("", text)
        text = re.sub(r"^\*D\d+ .*?\*$", "", text, flags=re.M | re.S)
        if m.group(1) in labels:
            out[labels[m.group(1)]] = text.strip()
    return out


def stage_map():
    return yaml.safe_load(ba.STAGES_FILE.read_text())


def build_records(pgs, part_titles):
    stages = stage_map()
    checks = bk.values_by_id()
    records = []
    for p in pgs:
        for r in p["recs"]:
            body = r["body"]
            f = fields(body)
            episodes, standards, others = parse_sources(r["sources"])
            reviewed = REVIEWED_RE.search(body)
            kind = r["id"].split("-")[1]
            rec = {
                "id": r["id"],
                "title": r["title"],
                "category": kind,
                "category_name": CATEGORY[kind],
                "part": p["part"],
                "part_title": part_titles[p["part"]],
                "page_title": p["title"],
                "permalink": permalink(r["id"]),
                "url": page_url(p["rel"], r["anchor"]),
                "source_file": f"book/{p['rel']}",
                "design_stages": stages.get(r["id"], []),
            }
            for _, key in FIELDS:
                if key in f:
                    rec[key] = unwrap(absolute_links(f[key], p["rel"]))
            if r["id"] in checks:
                rec["checks"] = checks[r["id"]]
            rec["figures"] = [
                {"id": d, "alt": unwrap(alt), "url": f"{SITE}/{(Path(p['rel']).parent / src).as_posix()}"}
                for d, alt, src in FIGURE_RE.findall(body)
            ]
            rec["sources"] = {"text": unwrap(absolute_links(r["sources"].strip(), p["rel"])), "episodes": episodes, "standards": standards, "other": others}
            rec["last_reviewed"] = reviewed.group(1) if reviewed else None
            records.append(rec)
    return records


def build_json(records):
    doc = {
        "$schema": f"{SITE}/data/recommendations.schema.json",
        "title": f"{BOOK_TITLE}: recommendations",
        "author": AUTHOR,
        "schema_version": SCHEMA_VERSION,
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "attribution": f"{BOOK_TITLE} by {AUTHOR}, {SITE}",
        "citation": CITATION,
        "note": "These are recommendations, not rules. Each record links to its page in the book, which has the full text, drawings and sources. "
                f"Records with a `checks` field are also checked by the OpenDFX KiCad design-rules file ({SITE}/opendfx.kicad_dru): "
                f"run KiCad's design rule check with it after placing and routing a board, and look up each report by its recommendation's permanent address. See {SITE}/kicad/.",
        "website": SITE,
        "repository": REPO,
        "count": len(records),
        "recommendations": records,
    }
    return doc


def dump_yaml(doc):
    class Dumper(yaml.SafeDumper):
        pass

    def str_rep(d, s):
        style = "|" if "\n" in s else None
        return d.represent_scalar("tag:yaml.org,2002:str", s, style=style)

    Dumper.add_representer(str, str_rep)
    head = "# Generated by tools/build_data.py from the book's pages. Don't edit by hand.\n"
    return head + yaml.dump(doc, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=100000)


def page_markdown(path):
    """A page's Markdown with full website links, the footer removed, sentences joined into paragraphs."""
    rel = path.relative_to(BOOK).as_posix()
    text = path.read_text()
    text = re.split(r"\n---\n\*From OpenDFX", text)[0]
    text = re.sub(r"<!--.*?-->\n?", "", text, flags=re.S)
    text = absolute_links(text, rel)
    # Join one-sentence-per-line text outside code blocks and tables.
    # A fenced block is kept exactly as written, as a paragraph of its own.
    blocks = re.split(FENCE, text)
    parts = [b.strip("\n") if b.startswith("```") else unwrap_keep_headings(b) for b in blocks]
    return add_permalinks("\n\n".join(p for p in parts if p.strip()) + "\n")


# A recommendation's own heading, such as "### PCB-DFM-026: Give every plated hole ...".
REC_HEADING = re.compile(r"^(#+ (PCB-D(?:FA|FM|FT)-\d{3}): .+)$", re.M)


def permalink_line(rec_id):
    return f"**Permanent address:** {permalink(rec_id)}"


def add_permalinks(md):
    """Put each recommendation's permanent address on a line of its own under its heading (Q275), so an AI tool
    reading the Markdown quotes opendfx.org/<ID> rather than the longer page address. Code blocks are left alone."""
    return outside_fences(md, lambda t: REC_HEADING.sub(lambda m: f"{m.group(1)}\n\n{permalink_line(m.group(2))}", t))


def permalink_problems(name, text, ids):
    """Every recommendation must have its permanent address exactly once, and nothing else may have one."""
    found = re.findall(r"^\*\*Permanent address:\*\* " + re.escape(SITE) + r"/(\S+)$", text, re.M)
    problems = [f"{name}: {i} has its permanent address {found.count(i)} times, not once"
                for i in ids if found.count(i) != 1]
    problems += [f"{name}: a permanent address for {i}, which isn't a recommendation" for i in set(found) - set(ids)]
    return problems


# A fenced code block: from a line starting with three backticks to the next such line.
FENCE = re.compile(r"(^```[^\n]*\n.*?^```[ \t]*$)", re.S | re.M)


def outside_fences(text, fn):
    """Apply fn to the text outside fenced code blocks, and leave the blocks as they are."""
    return "".join(b if b.startswith("```") else fn(b) for b in FENCE.split(text))


def unwrap_keep_headings(text):
    out = []
    for para in re.split(r"\n\s*\n", text):
        lines = [l.rstrip() for l in para.splitlines() if l.strip()]
        if not lines:
            continue
        if any(l.lstrip().startswith(("- ", "* ", "| ", "#", "<")) or re.match(r"\s*\d+\. ", l) for l in lines):
            out.append("\n".join(lines))
        else:
            out.append(" ".join(l.strip() for l in lines))
    return "\n\n".join(out)


def page_title(text):
    """The page's first level-1 heading (generated pages start with an HTML comment)."""
    return re.search(r"^# (.+)$", text, re.M).group(1).strip()


def all_pages():
    """Every page in reading order: Part 0 to Part 8, then the appendices."""
    paths = sorted(BOOK.glob("0[0-9]-*/[0-9]*.md"))
    return paths


def build_llms(pgs, part_titles, records):
    lines = [
        f"# {BOOK_TITLE}",
        "",
        f"> An open book of practical design-for-manufacturing, assembly and test recommendations for printed circuit boards, by {AUTHOR} of Worthington Assembly and CircuitHub. "
        f"It holds {len(records)} recommendations, each with a permanent ID such as PCB-DFA-006, the reason behind it, typical values and its sources. "
        "The text is CC BY-SA 4.0 and the recommendations data is CC BY 4.0.",
        "",
        "The recommendations are advice, not rules: each says what to do, why, and which values are common industry practice and which vary by manufacturer. "
        "When you use one, cite its ID and link to its permanent address, which is the website followed by the ID, "
        f"for example {permalink('PCB-DFA-006')}. "
        f"To cite the whole book: {CITATION}. More ways to cite it are at {SITE}/cite/.",
        "",
        "## Data",
        "",
        f"- [Recommendations (JSON)]({SITE}/data/recommendations.json): every recommendation as structured data, with its page address, design stages and sources",
        f"- [Recommendations (YAML)]({SITE}/data/recommendations.yaml): the same records as YAML",
        f"- [The whole book in one file]({SITE}/llms-full.txt): every page as Markdown, in reading order",
        f"- [Data file schema]({SITE}/data/recommendations.schema.json): a JSON Schema describing every field of the recommendations data",
        "",
        "Every page is also published as Markdown at its address with `.md` in place of the final slash, "
        f"for example {SITE}/02-the-panel/04-edge-clearance.md. "
        f"Every recommendation is published on its own as Markdown at its permanent address with `.md` added, for example {permalink('PCB-DFA-006')}.md. "
        "Fetch these when you need one page or one recommendation, instead of the whole book.",
        "",
        "## Designing a board with an AI agent",
        "",
        f"Start with [Using this book with an AI agent]({SITE}/00-start-here/05-using-this-book-with-an-ai-agent/): what to ask the person first, how to work through the recommendations stage by stage, and the table of every recommendation to hand back. "
        f"The book is also packaged as an Agent Skill, with the data file, the KiCad rules file and a script that prints the recommendations for each design stage: {SITE}/opendfx-pcb-design.zip",
        "",
        "## Checking a KiCad design",
        "",
        "If you design or review a board in KiCad, check it against this book with KiCad's design rule check. "
        f"Copy [the OpenDFX rules file]({SITE}/opendfx.kicad_dru) into the project folder, named after the project (myboard.kicad_dru next to myboard.kicad_pro), "
        "and set Board Setup, Solder Mask/Paste, Minimum web width to 0.1 mm. "
        f"If the project already has a rules file, keep it: follow the steps at {SITE}/00-start-here/05-using-this-book-with-an-ai-agent/#if-the-project-already-has-a-rules-file "
        "to find where the two files overlap, agree a combined file with the person, try it on a copy of the project with the zones refilled, "
        "and report the changes in the check and in the copper before you replace the original. "
        "Run the check after placing parts and again after routing, for example with `kicad-cli pcb drc --format json --severity-all`. "
        "Each report names the recommendation it comes from and its permanent address, such as opendfx.org/PCB-DFM-020; read that recommendation before you change the board. "
        "The rules check recommended values across the board, and minimum values only inside rule areas named \"OpenDFX minimum\", so keep to the recommended values unless the design needs less, and then draw a small rule area there. "
        f"The rules file checks only what the board data shows; the rest of the book still applies. How to use it: {SITE}/kicad/ "
        f"Before release, check the exported files (Gerber, drill, netlist, placement file and BOM) with {SITE}/check_release.py; its help text lists the KiCad export commands that follow the book.",
        "",
    ]
    by_part = {}
    for path in all_pages():
        by_part.setdefault(int(path.parent.name[:2]), []).append(path)
    counts = {}
    for r in records:
        counts[r["url"].split("#")[0]] = counts.get(r["url"].split("#")[0], 0) + 1
    for part, paths in sorted(by_part.items()):
        title = part_titles.get(part, "Appendices")
        lines += [f"## Part {part}: {title}" if part in part_titles else "## Appendices", ""]
        for path in paths:
            rel = path.relative_to(BOOK).as_posix()
            ptitle = page_title(path.read_text())
            n = counts.get(page_url(rel), 0)
            note = f": {n} recommendation{'s' if n != 1 else ''}" if n else ""
            lines.append(f"- [{ptitle}]({page_url(rel)}){note}")
        lines.append("")
    return "\n".join(lines)


def build_llms_full(part_titles):
    out = [
        f"# {BOOK_TITLE}",
        "",
        f"By {AUTHOR}. Text licensed CC BY-SA 4.0. Website: {SITE}",
        "",
        f"Cite as: {CITATION}",
        "",
        "Generated from the book's source pages. Each page below starts with its address.",
        "",
    ]
    for path in all_pages():
        rel = path.relative_to(BOOK).as_posix()
        md = page_markdown(path)
        # Nest every page under the book title, but leave headings inside code blocks as written.
        md = outside_fences(md, lambda t: re.sub(r"^(#+) ", lambda m: "#" + m.group(1) + " ", t, flags=re.M))
        out += ["---", "", f"Source: {page_url(rel)}", "", md]
    return "\n".join(out)


def build_robots():
    lines = [
        "# OpenDFX welcomes people, search engines and AI crawlers.",
        "# The book is CC BY-SA 4.0 and the recommendations data is CC BY 4.0.",
        "",
    ]
    for bot in AI_CRAWLERS:
        lines += [f"User-agent: {bot}", "Allow: /", ""]
    lines += ["User-agent: *", "Allow: /", "", f"Sitemap: {SITE}/sitemap-index.xml", ""]
    return "\n".join(lines)


# ---- Markdown copies and structured data for the website (Q166) ----

LICENSE_TEXT = "https://creativecommons.org/licenses/by-sa/4.0/"


def md_url(rel):
    """Address of a page's Markdown copy: 02-the-panel/04-edge-clearance.md -> https://opendfx.org/02-the-panel/04-edge-clearance.md."""
    return f"{SITE}/{rel}"


def page_md_copy(path):
    """A page as plain Markdown for AI tools, with its address and credit at the top."""
    rel = path.relative_to(BOOK).as_posix()
    head = (f"<!-- {BOOK_TITLE} by {AUTHOR}. Text CC BY-SA 4.0. "
            f"This is the Markdown copy of {page_url(rel)} -->\n\n")
    return head + page_markdown(path)


def recommendation_md(rec):
    """One recommendation as plain Markdown, served at its permanent address with .md added."""
    labels = [("Recommendation", "recommendation"), ("Why", "why"), ("Typical values", "typical_values"),
              ("What goes wrong if you don't", "what_goes_wrong"), ("Example", "example"), ("Applies to", "applies_to")]
    out = [f"# {rec['id']}: {rec['title']}", "",
           f"From *{BOOK_TITLE}* by {AUTHOR}, Part {rec['part']}: {rec['part_title']}, page \"{rec['page_title']}\". "
           f"Permanent address: {rec['permalink']}. Full page with drawings: {rec['url']}", ""]
    for label, key in labels:
        if rec.get(key):
            out += [f"**{label}:** {rec[key]}", ""]
    for c in rec.get("checks", []):
        out += [f"**Checked by the OpenDFX KiCad rules:** {c['check']}: recommended {c['recommended']} {c['unit']}, minimum {c['minimum']} {c['unit']}.", ""]
    for f in rec["figures"]:
        out += [f"**Drawing {f['id']}:** {f['alt']} ({f['url']})", ""]
    out += [f"**Design stages:** {', '.join(rec['design_stages']) or 'none'}", "",
            f"**Sources:** {rec['sources']['text']}", ""]
    if rec.get("last_reviewed"):
        out += [f"*Last reviewed: {rec['last_reviewed']}*", ""]
    out += [f"Text CC BY-SA 4.0. Cite as: {CITATION}, {rec['id']}, {rec['permalink']}", ""]
    return "\n".join(out)


def json_ld_book():
    return {"@type": "Book", "@id": f"{SITE}/#book", "name": BOOK_TITLE, "url": SITE, "inLanguage": "en-US",
            "author": {"@type": "Person", "name": AUTHOR}, "license": LICENSE_TEXT, "bookEdition": VERSION,
            "isAccessibleForFree": True}


def json_ld_page(rel, title, recs):
    """schema.org data for one page: a TechArticle in the book, listing the recommendations on it by ID."""
    doc = {"@context": "https://schema.org", "@type": "TechArticle", "headline": title, "url": page_url(rel),
           "inLanguage": "en-US", "author": {"@type": "Person", "name": AUTHOR}, "license": LICENSE_TEXT,
           "isAccessibleForFree": True, "isPartOf": json_ld_book(),
           "encoding": {"@type": "MediaObject", "encodingFormat": "text/markdown", "contentUrl": md_url(rel)}}
    if recs:
        doc["hasPart"] = [{"@type": "CreativeWork", "identifier": r["id"], "name": r["title"], "url": r["permalink"],
                           "encoding": {"@type": "MediaObject", "encodingFormat": "text/markdown", "contentUrl": r["permalink"] + ".md"}}
                          for r in recs]
    return doc


AGENT_PAGE = BOOK / "00-start-here" / "05-using-this-book-with-an-ai-agent.md"


def fence_problems(name, text, shift=""):
    """Problems with the fenced code blocks in a generated Markdown file.

    Every fence must start a line, an opening fence must follow a blank line, and a closing fence must be followed
    by a blank line. Page 0.5's instructions block must appear exactly as written, and the line that follows it in
    the book must follow it here too, outside the block (with `shift` added to a heading, as in llms-full.txt).
    """
    problems = []
    lines = text.split("\n")
    fences = [i for i, l in enumerate(lines) if l.startswith("```")]
    if len(fences) % 2:
        problems.append(f"{name}: an odd number of fences ({len(fences)})")
    for n, i in enumerate(fences):
        if n % 2 == 0 and i > 0 and lines[i - 1].strip():
            problems.append(f"{name}, line {i + 1}: an opening fence without a blank line before it")
        if n % 2 == 1 and i + 1 < len(lines) and lines[i + 1].strip():
            problems.append(f"{name}, line {i + 1}: a closing fence without a blank line after it")
    if "```" in text.replace("\n```", ""):
        problems.append(f"{name}: a fence that doesn't start a line")
    source = AGENT_PAGE.read_text()
    block = FENCE.search(source)
    after = next(l for l in source[block.end():].split("\n") if l.strip())
    after = shift + after if after.startswith("#") else after
    at = text.find(block.group(1))
    if at < 0:
        problems.append(f"{name}: page 0.5's instructions block isn't there exactly as written")
    elif next(l for l in text[at + len(block.group(1)):].split("\n") if l.strip()) != after:
        problems.append(f"{name}: page 0.5's instructions block isn't followed by \"{after}\" outside the block")
    return problems


def validate_schema(doc):
    """Check the data against data/recommendations.schema.json. Returns a list of problems, or None if jsonschema isn't installed."""
    try:
        import jsonschema
    except ImportError:
        return None
    schema = json.loads((DATA / "recommendations.schema.json").read_text())
    v = jsonschema.Draft202012Validator(schema)
    return [f"{'/'.join(map(str, e.path))}: {e.message}" for e in v.iter_errors(doc)]


def main():
    check = "--check" in sys.argv
    part_titles = ba.parts()
    pgs = ba.pages()
    records = build_records(pgs, part_titles)
    doc = build_json(records)
    problems = validate_schema(json.loads(json.dumps(doc)))
    if problems is None:
        print("build_data: jsonschema isn't installed, so the data file wasn't checked against its schema (pip install jsonschema).")
    elif problems:
        sys.exit("The data file doesn't match data/recommendations.schema.json:\n" + "\n".join(problems[:20]))
    outputs = {
        DATA / "recommendations.json": json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
        DATA / "recommendations.yaml": dump_yaml(doc),
        PUBLIC / "llms.txt": build_llms(pgs, part_titles, records),
        PUBLIC / "llms-full.txt": build_llms_full(part_titles),
        PUBLIC / "robots.txt": build_robots(),
    }
    problems = (fence_problems("llms-full.txt", outputs[PUBLIC / "llms-full.txt"], shift="#")
                + fence_problems("the Markdown copy of page 0.5", page_md_copy(AGENT_PAGE)))
    if problems:
        sys.exit("Broken code blocks in the Markdown for AI tools:\n" + "\n".join(problems))
    ids = [r["id"] for r in records]
    problems = (permalink_problems("llms-full.txt", outputs[PUBLIC / "llms-full.txt"], ids)
                + permalink_problems("the pages' Markdown copies", "\n".join(page_md_copy(p) for p in all_pages()), ids))
    if problems:
        sys.exit("Permanent addresses in the Markdown for AI tools:\n" + "\n".join(problems[:20]))
    stale = []
    for path, text in outputs.items():
        if check:
            if not path.exists() or path.read_text() != text:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(exist_ok=True)
            path.write_text(text)
    if stale:
        sys.exit("Out of date (run python3 tools/build_data.py): " + ", ".join(stale))
    if not check:
        print(f"Wrote {len(records)} recommendations and {len(outputs)} files.")


if __name__ == "__main__":
    main()

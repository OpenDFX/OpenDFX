"""Copy the book into the website project (M9), so the site is always built from the book's own pages.

Run: python3 tools/build_site.py
(`npm run build` and `npm run dev` in site/ run it first, so you rarely need to run it by hand.)

What it does:
  - copies every page in book/0N-*/ into site/src/content/docs/, with the page's first heading
    turned into its title, the "Edit page" link pointed at the real file in book/, and links
    between pages turned into website addresses (02-the-panel/04-edge-clearance.md -> /02-the-panel/04-edge-clearance/);
  - writes the Preface page (/preface/) from book/front-matter/: the dedication, then the preface (Q186);
  - writes the Change log page (/changelog/) from CHANGELOG.md (M14);
  - copies each part's images/ folder alongside, and makes each drawing a link to its full-size copy;
  - writes site/src/generated/sidebar.json (one group per part, titles from book/OUTLINE.md)
    and site/src/generated/permalinks.json (one forwarding page per recommendation ID, from data/recommendations.json);
  - copies public/ to the site's root and data/ to /data/;
  - writes a Markdown copy of every page next to it (/02-the-panel/04-edge-clearance.md) and of every
    recommendation at its permanent address with .md added (/PCB-DFA-006.md), and puts schema.org structured
    data and a link to the Markdown copy in each page's head (Q166), so AI tools can fetch only what they need.

Everything it writes is Git-ignored; the book, data/ and public/ stay the only sources.
Page addresses must match page_url() in tools/build_data.py. `npm run build` checks every link and anchor
in the book, then runs `python3 tools/build_site.py --check-dist` to check every permanent address lands on its heading.
"""
import json
import re
import shutil
import tempfile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_appendices as ba  # noqa: E402  (same part titles and page list as the other tools)
import build_data as bd  # noqa: E402  (Markdown copies and structured data, Q166)

ROOT = ba.ROOT
BOOK = ba.BOOK
SITE = ROOT / "site"
DOCS = SITE / "src" / "content" / "docs"
GENERATED = SITE / "src" / "generated"
SITE_PUBLIC = SITE / "public"
REPO = "https://github.com/OpenDFX/OpenDFX"

LINK_RE = re.compile(r"(!?)\[((?:[^\[\]]|\[[^\]]*\])*)\]\(([^)\s]+)\)")


def book_pages():
    """Every book page in reading order, as paths relative to book/ (the same set build_data.py publishes)."""
    return [p.relative_to(BOOK).as_posix() for p in sorted(BOOK.glob("0[0-9]-*/[0-9]*.md"))]


def page_path(rel):
    """Website path of a book page: 02-the-panel/02-rails.md -> /02-the-panel/02-rails/ (matches page_url())."""
    return f"/{rel[:-3]}/"


def fix_links(text, rel):
    """Rewrite links that point at other files: book pages become site paths, other repository files go to GitHub."""
    base = Path(rel).parent

    def fix(m):
        bang, label, target = m.groups()
        if re.match(r"[a-z]+:", target) or target.startswith(("#", "/")):
            return m.group(0)
        path, _, anchor = target.partition("#")
        resolved = (Path("/") / base / path).resolve().as_posix().lstrip("/")
        if bang:  # images stay relative for Astro; each is wrapped in a link that opens it full size, where it can be zoomed
            return f"[{m.group(0)}](/{resolved})" if resolved.endswith(".svg") else m.group(0)
        if resolved.endswith(".md") and (BOOK / resolved).exists() and re.match(r"0\d-[^/]+/\d", resolved):
            url = page_path(resolved)
        else:  # a file elsewhere in the repository, e.g. ../../data/README.md
            outside = (Path("/book") / base / path).resolve().as_posix().lstrip("/")
            url = f"{REPO}/blob/main/{outside}"
        return f"{bang}[{label}]({url}{'#' + anchor if anchor else ''})"

    return LINK_RE.sub(fix, text)


def plain(md):
    """Markdown to plain text, for the page description."""
    md = LINK_RE.sub(lambda m: m.group(2), md)
    md = re.sub(r"[*_`]", "", md)
    return re.sub(r"\s+", " ", md).strip()


def description(body):
    """The first ordinary paragraph, cut to whole sentences of about 160 characters, for search engines and link previews."""
    for para in re.split(r"\n\s*\n", body):
        p = para.strip()
        if not p or p.startswith(("#", "!", "|", "-", "*", "<", ">", "```")) or re.match(r"\d+\. ", p):
            continue
        text, out = plain(p), ""
        for sentence in re.split(r"(?<=[.!?])\s+", text):
            if out and len(out) + len(sentence) > 160:
                break
            out = f"{out} {sentence}".strip()
        return out
    return ""


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def recs_by_page():
    """{book-relative page path: [records]} from the data file."""
    out = {}
    for r in json.loads((ROOT / "data" / "recommendations.json").read_text())["recommendations"]:
        out.setdefault(r["source_file"][len("book/"):], []).append(r)
    return out


def head(rel, title, recs):
    """The page's <head> additions: schema.org data, and a link to its Markdown copy."""
    ld = json.dumps(bd.json_ld_page(rel, title, recs), ensure_ascii=False)
    return [{"tag": "script", "attrs": {"type": "application/ld+json"}, "content": ld},
            {"tag": "link", "attrs": {"rel": "alternate", "type": "text/markdown", "href": f"/{rel}"}}]


def convert(rel, recs=()):
    text = (BOOK / rel).read_text()
    text = re.sub(r"\A(\s*<!--.*?-->\s*)+", "", text, flags=re.S)  # generated appendices start with a comment
    m = re.search(r"^# (.+)$", text, re.M)
    title = m.group(1).strip()
    body = text[m.end():].lstrip("\n")
    body = re.split(r"\n---\n\*From OpenDFX", body)[0].rstrip() + "\n"  # the site footer carries the credit line
    body = fix_links(body, rel)
    front = [
        "---",
        f"title: {yaml_str(title)}",
        f"description: {yaml_str(description(body))}",
        f"editUrl: {yaml_str(f'{REPO}/edit/main/book/{rel}')}",
        f"head: {json.dumps(head(rel, title, list(recs)), ensure_ascii=False)}",
        "---",
        "",
    ]
    return "\n".join(front) + body


FRONT = BOOK / "front-matter"


def preface_page():
    """The website's Preface page (Q186): the dedication, then Chris's preface, both in his own words.
    The book keeps them in book/front-matter/; the PDF and EPUB give each its own page."""
    def body(name):
        text = (FRONT / name).read_text()
        return text[re.search(r"^# .+$", text, re.M).end():].strip()
    dedication, preface = body("dedication.md"), body("preface.md")
    front = [
        "---",
        'title: "Preface"',
        f"description: {yaml_str(description(preface))}",
        f"editUrl: {yaml_str(f'{REPO}/edit/main/book/front-matter/preface.md')}",
        "---",
        "",
    ]
    ded = "\n".join(f"*{line}*" for line in dedication.splitlines())
    return "\n".join(front) + f"{ded}\n\n---\n\n{preface}\n"


def changelog_page():
    """The website's Change log page (M14), from CHANGELOG.md at the top of the repository, without its first heading."""
    text = (ROOT / "CHANGELOG.md").read_text()
    body = text[re.search(r"^# .+$", text, re.M).end():].strip()
    front = [
        "---",
        'title: "Change log"',
        f"description: {yaml_str(description(body))}",
        f"editUrl: {yaml_str(f'{REPO}/edit/main/CHANGELOG.md')}",
        "---",
        "",
    ]
    return "\n".join(front) + body + "\n"


def sidebar(pages):
    """One collapsible group per part, labeled as in the outline without its aside ("Part 2: The panel")."""
    titles = ba.parts()
    groups = []
    for folder in sorted({p.split("/")[0] for p in pages}):
        num = int(folder[:2])
        label = f"Part {num}: {re.sub(r' \(.*\)$', '', titles[num])}" if num in titles else "Appendices"
        groups.append({"label": label, "collapsed": num != 0, "items": [{"autogenerate": {"directory": folder}}]})
    return groups


def permalinks():
    """{ID: site path with anchor} from the data file, e.g. PCB-DFA-006 -> /02-the-panel/02-rails.../#pcb-dfa-006-..."""
    data = json.loads((ROOT / "data" / "recommendations.json").read_text())
    out = {}
    for r in data["recommendations"]:
        url = r["url"]
        assert url.startswith(data["website"]), url
        out[r["id"]] = {"to": url[len(data["website"]):], "title": r["title"]}
    return out


def clean(path):
    if path.exists():
        shutil.rmtree(path)


def main():
    pages = book_pages()

    # Pages and their images. Only the generated part folders are removed; index.mdx etc. are hand-written.
    for old in DOCS.glob("0[0-9]-*"):
        clean(old)
    by_page = recs_by_page()
    for rel in pages:
        out = DOCS / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(convert(rel, by_page.get(rel, [])))
    for folder in sorted({p.split("/")[0] for p in pages}):
        if (BOOK / folder / "images").is_dir():
            shutil.copytree(BOOK / folder / "images", DOCS / folder / "images")

    (DOCS / "preface.md").write_text(preface_page())
    (DOCS / "changelog.md").write_text(changelog_page())

    GENERATED.mkdir(parents=True, exist_ok=True)
    (GENERATED / "sidebar.json").write_text(json.dumps(sidebar(pages), indent=2) + "\n")
    (GENERATED / "permalinks.json").write_text(json.dumps(permalinks(), indent=2, ensure_ascii=False) + "\n")

    # Static files: public/ at the root (llms.txt, robots.txt…), data/ at /data/.
    clean(SITE_PUBLIC)
    shutil.copytree(ROOT / "public", SITE_PUBLIC)
    shutil.copytree(ROOT / "data", SITE_PUBLIC / "data")
    shutil.copytree(SITE / "static", SITE_PUBLIC, dirs_exist_ok=True)
    # The Agent Skill (Q154), as a zip at /opendfx-pcb-design.zip, holding the folder skill/opendfx-pcb-design/.
    shutil.make_archive(str(SITE_PUBLIC / "opendfx-pcb-design"), "zip", ROOT / "skill", "opendfx-pcb-design")
    # The logo and press kit (M44), as a zip at /opendfx-brand.zip, holding the folder opendfx-brand/.
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copytree(ROOT / "public" / "brand", Path(tmp) / "opendfx-brand")
        shutil.make_archive(str(SITE_PUBLIC / "opendfx-brand"), "zip", tmp, "opendfx-brand")
    for folder in sorted({p.split("/")[0] for p in pages}):  # full-size drawings, at /02-the-panel/images/x.svg
        if (BOOK / folder / "images").is_dir():
            shutil.copytree(BOOK / folder / "images", SITE_PUBLIC / folder / "images")

    # Markdown copies for AI tools (Q166): every page beside its address, every recommendation at /<ID>.md.
    for rel in pages:
        (SITE_PUBLIC / rel).parent.mkdir(parents=True, exist_ok=True)
        (SITE_PUBLIC / rel).write_text(bd.page_md_copy(BOOK / rel))
    for recs in by_page.values():
        for r in recs:
            (SITE_PUBLIC / f"{r['id']}.md").write_text(bd.recommendation_md(r))

    print(f"build_site: {len(pages)} pages, {len(permalinks())} permanent addresses -> {DOCS.relative_to(ROOT)}")


def check_dist():
    """After `astro build`: every permanent address must land on a page and heading that exist in site/dist/."""
    dist = SITE / "dist"
    bad = []
    for rec_id, link in json.loads((GENERATED / "permalinks.json").read_text()).items():
        path, _, anchor = link["to"].partition("#")
        page = dist / path.strip("/") / "index.html"
        if not (dist / rec_id / "index.html").exists():
            bad.append(f"{rec_id}: no forwarding page")
        elif not page.exists():
            bad.append(f"{rec_id}: {path} does not exist")
        elif anchor and f'id="{anchor}"' not in page.read_text():
            bad.append(f"{rec_id}: no heading #{anchor} on {path}")
    for line in bad:
        print("build_site --check-dist:", line)
    print(f"build_site --check-dist: {len(bad)} broken permanent addresses")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(check_dist()) if "--check-dist" in sys.argv else main()

"""Rewrap Markdown prose to one sentence per line, changing only line breaks.

Usage: python3 tools/one_sentence_per_line.py FILE.md [...]
Paragraphs and list items are rejoined and split at sentence ends. Headings, tables, code blocks,
images, horizontal rules and blank lines are left alone. The rendered HTML is checked to be
unchanged (ignoring whitespace) before a file is written.
"""
import re
import sys
from markdown_it import MarkdownIt

# A sentence ends at . ! or ? (optionally followed by closing * _ ” ) ") and then a space,
# when the next sentence starts with a capital, a digit, an opening bracket, quote or emphasis.
END = re.compile(r'(?<=[.!?])([*_”")\]]*)\s+(?=[A-Z0-9“"(\[*_⚠])')
NO_SPLIT_BEFORE = ("e.g.", "i.e.", "vs.", "approx.", "No.", "Fig.", "etc.")


def split_sentences(text):
    out, start = [], 0
    for m in END.finditer(text):
        head = text[start:m.start()]
        if head.endswith(NO_SPLIT_BEFORE):
            continue
        out.append(text[start:m.start()] + m.group(1))
        start = m.end()
    out.append(text[start:])
    return [s for s in out if s]


def is_block_start(line):
    s = line.lstrip()
    return (s.startswith(("#", "|", "```", "![", "<!--")) or s in ("---", "***")
            or re.match(r"^\s*([-*+]|\d+\.)\s", line) is not None)


def rewrap(src):
    lines, out, i, fence = src.split("\n"), [], 0, False
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("```"):
            fence = not fence
            out.append(line); i += 1; continue
        if fence or not line.strip() or line.lstrip().startswith(("#", "|", "![", "<!--")) or line.strip() in ("---", "***"):
            out.append(line); i += 1; continue
        item = re.match(r"^(\s*(?:[-*+]|\d+\.)\s+)", line)
        prefix = item.group(1) if item else ""
        indent = " " * len(prefix)
        buf = [line[len(prefix):].strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not is_block_start(lines[i]):
            buf.append(lines[i].strip()); i += 1
        if len(buf) > 1 and all(re.match(r"(\d+(\.\d+)+|[A-Z]\.)\s", b) for b in buf):
            # Lines that each start with a section number (2.4, 5.11, A.) are a hand-made list: keep them.
            out.append(line); out.extend(lines[i - len(buf) + 1:i]); continue
        sentences = split_sentences(" ".join(buf))
        out.append(prefix + sentences[0])
        out.extend(indent + s for s in sentences[1:])
    return "\n".join(out)


def html(md):
    return re.sub(r"\s+", " ", MarkdownIt("commonmark").enable("table").render(md)).strip()


if __name__ == "__main__":
    for path in sys.argv[1:]:
        src = open(path, encoding="utf-8").read()
        new = rewrap(src)
        if html(src) != html(new):
            sys.exit(f"{path}: rendered output would change; not written")
        open(path, "w", encoding="utf-8").write(new)
        print(f"{path}: ok")

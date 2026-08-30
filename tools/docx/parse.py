# Parse a committed AFDS Markdown document into a structural AST for the Word build.
#
# Usage: python3 tools/docx/parse.py [document-key]
#
# The document key selects an entry in tools/docx/documents.json, which names the
# source Markdown, the output path, the title-page fields, and an optional annex
# sliced out of a second file. The key defaults to "spec".
import json, re, subprocess, sys, textwrap, pathlib

REPO = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
OUT = REPO / "ast.json"
WRAP = 90  # max monospace chars per rendered code line


def inline(text):
    """Split inline markdown into runs: plain, bold, code, emphasis."""
    # Normalise links: keep the label, drop the target (targets live in References).
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    runs, i = [], 0
    pattern = re.compile(r"(\*\*.+?\*\*|`[^`]+`|(?<!\w)\*[^*]+\*(?!\w))", re.S)
    for m in pattern.finditer(text):
        if m.start() > i:
            runs.append({"t": text[i:m.start()]})
        tok = m.group(0)
        if tok.startswith("**"):
            runs.append({"t": tok[2:-2], "b": True})
        elif tok.startswith("`"):
            runs.append({"t": tok[1:-1], "c": True})
        else:
            runs.append({"t": tok[1:-1], "i": True})
        i = m.end()
    if i < len(text):
        runs.append({"t": text[i:]})
    return [r for r in runs if r["t"]] or [{"t": ""}]


def wrap_code(lines):
    """Soft-wrap over-long code lines; report whether any wrapping happened."""
    out, wrapped = [], False
    for ln in lines:
        if len(ln) <= WRAP:
            out.append(ln)
            continue
        wrapped = True
        indent = re.match(r"\s*", ln).group(0) + "    "
        pieces = textwrap.wrap(
            ln, width=WRAP, subsequent_indent=indent,
            break_long_words=True, break_on_hyphens=False,
            drop_whitespace=False, replace_whitespace=False,
        )
        out.extend(pieces)
    return out, wrapped


def parse(md, h_offset):
    """Parse markdown body into blocks. h_offset shifts source heading depth."""
    lines = md.split("\n")
    blocks, i = [], 0
    while i < len(lines):
        ln = lines[i]

        if ln.startswith("<!--") or (not ln.strip() and True):
            i += 1
            continue

        if ln.startswith("```"):
            i += 1
            code = []
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            code, wrapped = wrap_code(code)
            blocks.append({"k": "code", "lines": code, "wrapped": wrapped})
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            level = len(m.group(1)) + h_offset
            blocks.append({"k": "h", "level": max(1, min(4, level)),
                           "runs": inline(m.group(2).strip())})
            i += 1
            continue

        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                raw = lines[i].strip().strip("|")
                cells = [c.strip() for c in raw.split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append([inline(c) for c in cells])
                i += 1
            ncol = max(len(r) for r in rows)
            for r in rows:
                while len(r) < ncol:
                    r.append([{"t": ""}])
            blocks.append({"k": "table", "ncol": ncol, "rows": rows})
            continue

        m = re.match(r"^(\d+)\.\s+(.*)$", ln)
        if m:
            item = [m.group(2).strip()]
            i += 1
            # 2+ space indented lines continue the same numbered item
            while i < len(lines) and re.match(r"^\s{2,}\S", lines[i]) and not lines[i].startswith("|"):
                item.append(lines[i].strip())
                i += 1
            blocks.append({"k": "li", "ord": True, "runs": inline(" ".join(item))})
            continue

        m = re.match(r"^[-*]\s+(.*)$", ln)
        if m:
            blocks.append({"k": "li", "ord": False, "runs": inline(m.group(1).strip())})
            i += 1
            continue

        # Paragraph: consecutive non-blank, non-special lines. The source uses
        # one sentence per line, so join them into a single paragraph.
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(
            r"^(#{1,6}\s|\||```|\d+\.\s|[-*]\s|<!--)", lines[i]
        ):
            para.append(lines[i].strip())
            i += 1
        if para:
            blocks.append({"k": "p", "runs": inline(" ".join(para))})
        else:
            i += 1
    return blocks


def strip_front(md):
    """Drop SPDX comments and return (h1_title, intro_paragraphs, rest)."""
    md = re.sub(r"^<!--.*?-->\s*", "", md, flags=re.S | re.M)
    m = re.search(r"^#\s+(.*)$", md, re.M)
    title = m.group(1).strip()
    after = md[m.end():]
    nxt = re.search(r"^##\s", after, re.M)
    intro, rest = after[:nxt.start()], after[nxt.start():]
    return title, [p.strip() for p in intro.strip().split("\n\n") if p.strip()], rest


key = sys.argv[1] if len(sys.argv) > 1 else "spec"
documents = json.loads((HERE / "documents.json").read_text())
if key not in documents:
    raise SystemExit(f"unknown document key {key!r}; known keys: {', '.join(sorted(documents))}")
doc = documents[key]

source_md = (REPO / doc["source"]).read_text()
_, intro_paras, body_md = strip_front(source_md)

# Optional annex: a named span sliced out of a second document.
annex_blocks = []
annex = doc.get("annex")
if annex:
    other = (REPO / annex["file"]).read_text()
    annex_md = other[other.index(annex["start"]):other.index(annex["end"])]
    annex_md = annex_md.replace(annex["start"], "").strip()
    # source h3 (each decision) -> Word Heading 2 under the annex Heading 1
    annex_blocks = parse(annex_md, -1)

commit = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                        capture_output=True, text=True).stdout.strip()

ast = {
    "key": key,
    "commit": commit,
    "doc": doc,
    # The title page records the commit, so the placeholder is filled here.
    "status": [[label, value.replace("{commit}", commit)] for label, value in doc["status"]],
    "intro": [{"k": "p", "runs": inline(" ".join(p.split("\n")))} for p in intro_paras],
    # source h2 -> Word Heading 1, h3 -> Heading 2
    "body": parse(body_md, -1),
    "annex": annex_blocks,
}
OUT.write_text(json.dumps(ast, indent=1))

kinds = {}
for b in ast["body"] + ast["annex"]:
    kinds[b["k"] + (str(b.get("level", "")) if b["k"] == "h" else "")] = \
        kinds.get(b["k"] + (str(b.get("level", "")) if b["k"] == "h" else ""), 0) + 1
print("document:", key, "from", doc["source"])
print("commit:", commit)
print("blocks:", kinds)
print("wrapped code blocks:", sum(1 for b in ast["body"] if b["k"] == "code" and b["wrapped"]))
print("intro paras:", len(ast["intro"]))

"""Repair the generated .docx: de-duplicate styles and enable field update.

The docx library emits its own default Heading1-4 definitions and then the
project overrides, leaving two <w:style> elements per styleId. Duplicate
styleIds are invalid, and Word resolves to the first, which has no
<w:outlineLvl>, so the table of contents comes out empty. Keep the last
definition of each id. Also set <w:updateFields> so Word populates the
table of contents when the document is opened.
"""
import re
import shutil
import sys
import zipfile
from pathlib import Path

src = Path(sys.argv[1])
tmp = src.with_suffix(".tmp.docx")

STYLE_RE = re.compile(r"<w:style\b.*?</w:style>", re.S)
ID_RE = re.compile(r'w:styleId="([^"]+)"')


def fix_styles(xml: str) -> tuple[str, list[str]]:
    matches = list(STYLE_RE.finditer(xml))
    last = {}
    for m in matches:
        sid = ID_RE.search(m.group(0))
        if sid:
            last[sid.group(1)] = m.start()
    removed, out, pos = [], [], 0
    for m in matches:
        sid = ID_RE.search(m.group(0))
        if sid and last[sid.group(1)] != m.start():
            removed.append(sid.group(1))
            out.append(xml[pos:m.start()])
            pos = m.end()
    out.append(xml[pos:])
    return "".join(out), removed


def fix_settings(xml: str) -> str:
    if "updateFields" in xml:
        return xml
    return xml.replace("<w:settings", "<w:settings", 1).replace(
        "</w:settings>", '<w:updateFields w:val="true"/></w:settings>', 1
    )


zin = zipfile.ZipFile(src)
report = {}
with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == "word/styles.xml":
            xml, removed = fix_styles(data.decode("utf-8"))
            report["removed_duplicate_styles"] = removed
            data = xml.encode("utf-8")
        elif item.filename == "word/settings.xml":
            data = fix_settings(data.decode("utf-8")).encode("utf-8")
            report["updateFields"] = True
        zout.writestr(item, data)
zin.close()
shutil.move(tmp, src)

# Verify the result.
z = zipfile.ZipFile(src)
styles = z.read("word/styles.xml").decode("utf-8")
ids = [ID_RE.search(m.group(0)).group(1) for m in STYLE_RE.finditer(styles)]
dupes = {i for i in ids if ids.count(i) > 1}
print("removed duplicates:", report.get("removed_duplicate_styles"))
print("remaining duplicate styleIds:", dupes or "none")
for h in ("Heading1", "Heading2", "Heading3"):
    m = re.search(rf'<w:style [^>]*w:styleId="{h}".*?</w:style>', styles, re.S)
    body = m.group(0)
    lvl = re.search(r'<w:outlineLvl w:val="(\d)"/>', body)
    col = re.search(r'<w:color w:val="([0-9A-Fa-f]{6})"/>', body)
    print(f"  {h}: outlineLvl={lvl.group(1) if lvl else 'MISSING'} colour=#{col.group(1) if col else '?'}")
print("updateFields present:", "updateFields" in z.read("word/settings.xml").decode("utf-8"))

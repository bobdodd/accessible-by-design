<!--
SPDX-FileCopyrightText: 2026 Bob Dodd
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# tools/docx — Word build for the project's documents

Generates a Word document from committed Markdown. The Markdown is authoritative; this directory only re-presents it.

The build takes a **document key** naming an entry in `documents.json`. Two documents are defined:

| Key | Source | Output |
| --- | --- | --- |
| `spec` | `docs/AFDS-PACKAGE-FORMAT.md`, plus the two adopted portable-representation decisions in `docs/COLOPHON.md` as Annex A | `dist/AFDS-Draft-Specification-v1.0.0.docx` |
| `guide` | `docs/AFDS-USER-GUIDE.md` | `dist/AFDS-User-Guide-v1.0.0.docx` |

Each entry in `documents.json` holds the source path, the output path, the title, version, subtitle, the heading used for the opening section, the rows of the title-page status table, the document metadata, and an optional `annex` block naming a second file and the span to slice out of it. Adding a document means adding an entry, not editing the scripts.

The document is built rather than exported by hand so that the accessibility properties are guaranteed by the build instead of remembered by an author.

## Running it

```
npm install docx@9
python3 tools/docx/parse.py guide                  # markdown  ->  ast.json
node     tools/docx/build.js                       # ast.json  ->  .docx
python3  tools/docx/postprocess.py dist/AFDS-User-Guide-v1.0.0.docx   # required, see below
```

The document key is `parse.py`'s only argument and defaults to `spec`. `build.js` takes no argument: it reads the key, the document's configuration, and the output path out of `ast.json`, so the parse step decides which document is being built and the two steps cannot disagree.

`parse.py` reads the document's source, slices in the annex if one is configured, and records the source commit so the title page can state it. It strips SPDX comments, joins the repository's one-sentence-per-line paragraphs into real paragraphs, and soft-wraps over-long code lines at 90 characters, printing a note wherever it wrapped.

## Why postprocess.py is not optional

The `docx` library emits its own `Heading1`–`Heading4` style definitions before the project's overrides are applied, leaving **two `<w:style>` elements with the same `w:styleId`**. Duplicate style ids are invalid OOXML, and Word resolves to the first definition it finds. The library's definitions are blue and carry **no `w:outlineLvl`**, so without this step the document would ship with blue headings and an **empty table of contents**.

`postprocess.py` keeps the last definition of each style id and injects `<w:updateFields w:val="true"/>` into `word/settings.xml` so the contents list populates on open.

## Accessibility properties the build guarantees

- Real heading styles with explicit `w:outlineLvl` 0, 1 and 2, so headings are exposed to assistive technology and to the table-of-contents field rather than being simulated with bold text.
- A live `TOC \h \o "1-3"` field, not a typed list.
- `w:tblHeader` on every table's first row and `w:cantSplit` on every row, so header context is repeated when a table crosses a page and no row is torn in half.
- `en-GB` document language, so a screen reader pronounces the project's British spellings correctly.
- Full document metadata, including title and author, so the file is identifiable without being opened.
- Black heading text at full contrast, not the library's default blue.
- A separate numbering instance for each ordered list, so a list of steps starts at 1 rather than continuing the count of the previous list and misnumbering every item in it.

## Column widths and word breaking

Word breaks a line only at whitespace or after a hyphen. It does **not** break at a dot or a slash. A dotted identifier such as `components.canonicalSources`, or a path such as `afds-inventory.json`, is therefore a single unbreakable token, and a column narrower than that token will not wrap it — it will overflow or be clipped.

`build.js` measures the longest unbreakable token in each column, reserves `240` DXA of padding plus `122` DXA per character for it as a per-column minimum, distributes the remaining width by content length, and falls back to proportional widths if the minimums exceed the usable page width. This is why table column widths are computed rather than fixed.

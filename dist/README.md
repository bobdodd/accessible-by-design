<!--
SPDX-FileCopyrightText: 2026 Bob Dodd
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# dist — published build outputs

Everything in this directory is a **derived artefact**. Nothing here is a source of truth. Each file is generated from Markdown and JSON elsewhere in this repository, and it is committed only so that a tagged release can carry it without depending on binary attachment uploads.

If a file here disagrees with the Markdown or JSON it was generated from, **the source is authoritative and the file here is stale**. Regenerate it rather than editing it.

## Contents

| File | Generated from | Regenerate with |
| --- | --- | --- |
| `AFDS-Sample-1.0.0.afds` | `afds-sample/` | `cd afds-sample && python3 tools/build-inventory.py pack ../dist/AFDS-Sample-1.0.0.afds` |
| `AFDS-Draft-Specification-v1.0.0.docx` | `docs/AFDS-PACKAGE-FORMAT.md` and the portable-representation decisions in `docs/COLOPHON.md` | see `tools/docx/README.md` |

## Verifying the sample package

```
cd afds-sample
python3 tools/build-inventory.py verify
```

The `verify` step checks that every inventory record matches the file it names, in both directions, before the package is built. It is the same check a consumer performs on the packed `.afds` file, as specified in `docs/AFDS-PACKAGE-FORMAT.md` section 9.

Inventory integrity is **not** a digital signature. A SHA-256 digest detects accidental change in transfer; it does not identify a signer and does not prove provenance. See section 10.3 of the specification.

## Digests

Recorded at the time these files were last rebuilt:

```
5d9e88a763d35763362edb910a74b2482ee1efbad5a61df2c20e12d58a93dfd1  AFDS-Draft-Specification-v1.0.0.docx
b6d9097a2767f38330551934235db8efa3c3be557a12104b0c9e0935567e81dc  AFDS-Sample-1.0.0.afds
```

Neither build is byte-for-byte reproducible. Both files are ZIP containers, so entry order and embedded timestamps depend on the build environment, and a rebuild will normally produce a different digest even from identical sources. The digests above identify **these committed files**; they are not a reproducibility target.

What must match on a rebuild is the **content**: for the package, the path, byte length, and SHA-256 digest of every inventory record; for the document, the text and structure of the Markdown it was generated from.

The document's own title page records the source commit it was generated from, so a reader can tell whether it is current without comparing digests. The `v1.0.0-draft` release tag carries the artefacts as they stood at that tag; `main` may carry newer ones.

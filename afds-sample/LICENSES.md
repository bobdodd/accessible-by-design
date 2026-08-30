<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# Licences

This package uses two licences, one for code and one for documentation.
Copyright (C) 2026 Bob Dodd.

## The arrangement

| Material | Licence | SPDX identifier |
| --- | --- | --- |
| Code, scripts, and machine-readable artefacts | GNU General Public Licence version 3 only | `GPL-3.0-only` |
| Documentation and prose | Creative Commons Attribution-ShareAlike 4.0 International | `CC-BY-SA-4.0` |

Both licences are copyleft, so a derivative of either kind of material stays under the same terms.

## Which licence applies to which file

| Path | Licence |
| --- | --- |
| `afds-manifest.json` | GPL-3.0-only |
| `afds-inventory.json` | GPL-3.0-only |
| `tokens/core.tokens.json` | GPL-3.0-only |
| `components/stack/stack.spec.json` | GPL-3.0-only |
| `evidence/at-matrix.json` | GPL-3.0-only |
| `components/stack/stack.md` | CC-BY-SA-4.0 |
| `evidence/known-limitations.md` | CC-BY-SA-4.0 |
| `adapters/README.md` | CC-BY-SA-4.0 |
| `docs/PACKAGE.md` | CC-BY-SA-4.0 |
| `LICENSES.md` | CC-BY-SA-4.0 |

The manifest declares the same arrangement in machine-readable form under its `licences` object, so a tool need not parse this table.

## Per-file headers

Every Markdown file in this package begins with two comment lines: an SPDX licence identifier and a copyright line.
A file therefore retains an unambiguous licence when it is copied out of the package.

JSON has no comment syntax, so JSON artefacts cannot carry an inline header.
Their licence is established by the manifest's `licences.code` field and by the table above.

## Attribution

Attribution should name the author and the project.

> Bob Dodd, *Accessible by Design*, https://a11ybob.com/

## Why two licences

Documentation and code are reused differently.
Prose is quoted, translated, and adapted into other guidance, which CC BY-SA 4.0 handles well and the GPL handles badly.
Machine-readable artefacts are compiled, transformed, and shipped inside tools, which is what the GPL was written for.
Using one licence for both would make one of the two uses awkward.

<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# Adapters

An adapter converts AFDS canonical artefacts into the representation another tool or platform expects.
Figma, Penpot, CSS custom properties, native platform resources, and Electron shells are all adapter targets.

This sample package ships no adapters.
This file records the rules that any adapter in a real package must follow, so that the rules travel with the format rather than living only in a specification a consumer might not have.

## The no-adapter-is-canonical rule

An adapter output MUST NOT be the only source of a fact owned by a canonical artefact.

The reason is ownership.
A token value is owned by the DTCG token file.
A component's semantic model, keyboard contract, Reflow behaviour, WCAG mapping, non-guarantees, and uncertainty are owned by the component specification.
An assistive-technology observation is owned by an evidence record.

If a fact exists only in a Figma library, a generated stylesheet, or a platform resource bundle, then the fact has left the portable bundle and the accessibility contract is no longer portable.
That is precisely the failure the package format exists to prevent.

Two practical consequences follow.

| Consequence | What it means in practice |
| --- | --- |
| Adapter output is always `derived` or `adapter` in role, never `canonical` | The inventory role field records this, and a verifier can check it |
| Regenerating an adapter output MUST be possible from the canonical artefacts alone | If regeneration loses a fact, the fact was only in the adapter and the package is non-conforming |

## Adapters report rather than flatten

Some properties cannot transfer losslessly.

A `ch`-based measure has no direct native analogue.
A forced-colours boundary expressed as a transparent outline has no equivalent in a design tool that models only fills.
A keyboard contract has no representation at all in a token pipeline.

An adapter MUST report these situations rather than silently flattening them.
Silent flattening is the more dangerous behaviour, because the output looks complete and the loss is discovered only when a user encounters it.

Every transform therefore emits a report containing mappings, warnings, losses, unsupported features, and validation status.
The shape of that report is specified in `docs/AFDS-PACKAGE-FORMAT.md` in the project repository.

## What an adapter directory looks like in a real package

A real package places each adapter in its own subdirectory under `adapters/`.

| Path | Contents |
| --- | --- |
| `adapters/<target>/adapter.json` | Adapter declaration: identifier, target, version, and the canonical inputs it consumes |
| `adapters/<target>/report.json` | The transform report for the outputs shipped in this package |
| `adapters/<target>/out/` | The generated artefacts, all with role `adapter` or `derived` |

The manifest's `adapters` array declares each adapter so that a consumer can enumerate them without walking the archive.
In this sample that array is empty, which is the correct declaration for a package with no adapters.

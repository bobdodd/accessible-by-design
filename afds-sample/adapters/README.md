<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# Adapters

An adapter moves information between AFDS canonical artefacts and the representation another tool or platform uses.
Figma, Penpot, CSS custom properties, native platform resources, and Electron shells are all adapter targets.

An adapter has a direction.
An **export** adapter reads canonical artefacts and writes what a target expects.
An **import** adapter reads a target's representation and drafts the artefacts an AFDS package requires.

This sample package ships no adapters in either direction.
This file records the rules that any adapter in a real package must follow, so that the rules travel with the format rather than living only in a specification a consumer might not have.

## The no-adapter-is-canonical rule

An adapter output MUST NOT be the only source of a fact owned by a canonical artefact.

The reason is ownership, and clause 28.2 of the AFDS specification is the authority for it.
A token value is owned by the DTCG token file.
A component's semantic model, derivation, keyboard contract, Reflow behaviour, WCAG mapping, guarantees, non-guarantees, assertions, and uncertainty are owned by the component specification.
An assistive-technology observation is owned by an evidence record.
A guarantee's substantiation status is owned by none of them, because it is computed from a guarantee and its evidence together and must not be written into either.

If a fact exists only in a Figma library, a generated stylesheet, or a platform resource bundle, then the fact has left the portable bundle and the accessibility contract is no longer portable.
That is precisely the failure the package format exists to prevent.

Two practical consequences follow.

| Consequence | What it means in practice |
| --- | --- |
| Adapter output is always `derived` or `adapter` in role, never `canonical` | The inventory role field records this, and a verifier can check it |
| Regenerating an export output MUST be possible from the canonical artefacts alone | If regeneration loses a fact, the fact was only in the adapter output and the package is non-conforming |

The regeneration rule has one exception, which is an import report.
An import reads a source that sits outside the package by definition, so no package can regenerate it.

## Adapters report rather than flatten

Some properties cannot transfer losslessly.

A `ch`-based measure has no direct native analogue.
A forced-colours boundary has no equivalent in a target with no concept of a user-forced colour palette.
A keyboard contract has no representation at all in a token pipeline.

An adapter MUST report these situations rather than silently flattening them.
Silent flattening is the more dangerous behaviour, because the output looks complete and the loss is discovered only when a user encounters it.

Every transform therefore emits a report.
Both directions report `mappings` and `warnings`.
An export report adds `losses` and `unsupported`.
An import report adds `gaps`, for facts an AFDS artefact requires and the source could not supply, and `unmapped`, for source content AFDS has no representation for.

The shape of that report is specified at clause 33.6 of the AFDS specification, in the project repository.

## What an import may not do

An import produces a draft, not a contract.

A draft becomes canonical only through **promotion**: a person reads it, supplies what the source could not, and accepts responsibility for the accessibility claims the artefact then makes.
Promotion MUST be performed by a person and MUST NOT be performed by a transform.

| Rule | Reason |
| --- | --- |
| An import MUST NOT write an artefact with role `canonical` | A representation shaped by a target's limits cannot own a fact |
| An unpromoted draft MUST NOT ship in a conforming package | A draft inside a package is indistinguishable from a contract to whoever relies on it |
| Every `gaps` entry MUST appear in the promoted artefact as uncertainty or a declared non-guarantee | An import that could not find a fact does not excuse the package from declaring the fact unknown |
| An import MUST be a discrete run producing a dated report, never a live read-through dependency | A read-through dependency makes the external tool the effective owner of whatever it supplies, and leaves no report to review |

An import report containing a `gaps` entry of `error` severity MUST report `validationStatus` as `failed`.
A failed import is not a malfunction, and for most targets it is the expected result.
It states that the source cannot yield a conforming artefact without human authorship.

## What an adapter directory looks like in a real package

A real package places each adapter in its own subdirectory under `adapters/`.

| Path | Contents |
| --- | --- |
| `adapters/<target>/adapter.json` | Adapter declaration: identifier, direction, target, version, and the inputs it consumes |
| `adapters/<target>/report.json` | The transform report for this adapter run |
| `adapters/<target>/out/` | Export output only, all with role `adapter` or `derived` |

An import adapter has no `out/` directory, because its drafts are not package artefacts.
Its declaration lists the canonical artefacts promoted from it in a `promoted` array.

A target supported in both directions is declared as two adapters sharing a `target` value, because the two carry different obligations and different reports.

The manifest's `adapters` array declares each adapter so that a consumer can enumerate them without walking the archive.
In this sample that array is empty, which is the correct declaration for a package with no adapters.

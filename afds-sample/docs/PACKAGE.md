<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# What this package demonstrates

This is **AFDS Sample** version 1.0.0.
It is a small but complete `.afds` package built to exercise the rules in `docs/AFDS-PACKAGE-FORMAT.md`.

Its purpose is to be verifiable rather than impressive.
Everything in it is either a real artefact or an explicitly marked placeholder.

## Contents

The package contains ten entries.
Nine of them are inventory records; the tenth is the inventory itself, which never records itself.

| Path | Role | What it demonstrates |
| --- | --- | --- |
| `afds-manifest.json` | canonical | A complete manifest with canonical source declarations, licences, profile, and DTCG version |
| `afds-inventory.json` | canonical | Real byte lengths and real lowercase hexadecimal SHA-256 digests for every other entry |
| `tokens/core.tokens.json` | canonical | DTCG groups, `$type`, `$value`, `$description`, and alias references |
| `components/stack/stack.spec.json` | canonical | A machine-readable component contract, including an explicit "no keyboard contract" statement |
| `components/stack/stack.md` | documentation | The human-readable counterpart of the contract |
| `evidence/at-matrix.json` | evidence | Engine-qualified evidence record structure with placeholder results |
| `evidence/known-limitations.md` | evidence | Honest limitations, non-guarantees, and uncertainty |
| `adapters/README.md` | documentation | Adapter guidance and the no-adapter-is-canonical rule |
| `docs/PACKAGE.md` | documentation | This file |
| `LICENSES.md` | documentation | The dual licensing arrangement |

## What is deliberately absent

The optional `patterns/`, `manifests/`, `schemas/`, and `stories/` directories are not present.
The `adapters/` directory is present but contains guidance only, and the manifest's `adapters` array is correspondingly empty.

Absence is declared rather than implied.
`components/stack/stack.spec.json` records the paths of its two test fixtures and states that this sample does not ship them.

### The declared target level

The manifest declares `targetConformanceLevel` as `AA`.

Clause 12.4 of the specification requires every package to declare a default target level and does not mandate which one.
Stack does not amend it, so Level AA is the effective target for the one component this sample ships.

The declaration is a statement of intent and nothing more.
Every result in `evidence/at-matrix.json` is `not-yet-tested`, so this package declares a target it has not demonstrated it meets, and clause 12.4 says in terms that a declared level is not evidence the level is met.
The `level` field inside each `wcagMapping` entry is a different thing again: it records the level WCAG itself assigns to that criterion, which is fixed by WCAG and is not a choice this package made.

### No method profile is claimed

The manifest declares `methodProfiles` as an empty array.

That is a substantive statement and not an omission.
Stack is in fact built the way Part III's `afds-layout-intrinsic` profile describes, so claiming the profile would be tempting and would be wrong.

Clause 21.4 of the specification requires a package claiming that profile to inspect every delineated surface in a forced-colours mode and to record the result as dated evidence.
This sample has no such evidence record, because it has no real evidence records at all.
A profile claim asserting a method the package cannot show it followed would be exactly the kind of unearned claim the format exists to prevent, and the specification separates the two profile axes so that the honest answer is available: this package is complete at the component level, `afds-components`, and claims no method.

The empty array and an omitted array have identical meaning under clause 20.2.
The array is written out anyway, because a reader can tell an empty declaration from an unconsidered one and cannot tell an absent field from an oversight.

## What the sample proves and what it does not

The sample proves that the container rules, the manifest shape, the inventory shape, and the verification algorithm are implementable, because a script regenerates the inventory and then verifies it.

The sample proves nothing about assistive-technology support.
Every result field in `evidence/at-matrix.json` is `not-yet-tested`.
No version, date, or observation in that file describes anything that happened.

The sample also proves nothing about provenance.
The inventory detects a change in transfer; it does not identify a signer.
A future signature mechanism is required before a package can be trusted on the strength of its own contents.

## Reading order for a newcomer

Start with `afds-manifest.json` to see what the package claims to be.
Read `tokens/core.tokens.json` next, because it is the smallest artefact and shows the alias mechanism.
Then read `components/stack/stack.md` alongside `components/stack/stack.spec.json`, which is where the accessibility contract actually lives.
Finish with `evidence/known-limitations.md`, which is the honest boundary of the whole package.

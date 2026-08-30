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

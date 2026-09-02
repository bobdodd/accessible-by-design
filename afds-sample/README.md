<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# AFDS Sample package source

This directory is the unpacked source of the **AFDS Sample** `.afds` package, version 1.0.0.
The format it conforms to is specified in Part IV of [the AFDS specification](../docs/AFDS-SPECIFICATION.md).

This directory holds sources only.
The pack command refuses any destination inside it, so a built archive can never be committed alongside the files it was built from.
The released archive is built to `dist/` at the repository root and is committed there, so that the exact bytes a consumer receives are reviewable and can be checked against a rebuild.

## What is in the package and what is not

Ten files plus the generated inventory make up the package.
Two things in this directory are repository helpers and are deliberately excluded from the package: this `README.md` and the `tools/` directory.
The specification does not describe a source directory at all, so that boundary is a convention of this repository rather than a conformance rule, and the table below is its only statement.
Open question H7 records that the specification is silent on the matter.
The verify command checks the table against the package it builds, so the two cannot drift apart.

| Path | In the package? | Purpose |
| --- | --- | --- |
| `afds-manifest.json` | Yes | Package identity, licences, profile, canonical source declarations |
| `afds-inventory.json` | Yes | Generated. Real byte lengths and real SHA-256 digests |
| `tokens/core.tokens.json` | Yes | DTCG token sample with groups and alias references |
| `components/stack/stack.spec.json` | Yes | Machine-readable Stack contract |
| `components/stack/stack.md` | Yes | Stack component documentation, the prose counterpart of the contract |
| `patterns/registry.json` | Yes | Package-level pattern registry, required by clause 24.2 of a native-first package |
| `evidence/at-matrix.json` | Yes | Assistive-technology evidence records, all results placeholders |
| `evidence/known-limitations.md` | Yes | Known limitations and uncertainty. Declared as `documentation`, not as evidence |
| `adapters/README.md` | Yes | Adapter guidance and the no-adapter-is-canonical rule |
| `docs/PACKAGE.md` | Yes | What this sample demonstrates |
| `LICENSES.md` | Yes | Dual licensing arrangement |
| `README.md` | No | This file. Repository guidance, not package content |
| `tools/build-inventory.py` | No | Helper script that builds, verifies, and packs |

The inventory therefore holds ten records, and the packed archive holds eleven entries, because the inventory never records itself.

## Prerequisites

Python 3.9 or later.
No third-party packages are required; the script uses only the standard library.

## Regenerating the inventory

Run the build command from inside this directory whenever any package file changes.

```sh
cd afds-sample
python3 tools/build-inventory.py build
```

The command rewrites `afds-inventory.json`, computing a real lowercase hexadecimal SHA-256 digest and a real byte length for every entry.
It prints one line per record so that the change is visible in the terminal as well as in the diff.
Records are sorted by path, so a rebuild that changes nothing produces no diff.

## Verifying the inventory

Run the verify command to check the source tree against the inventory.

```sh
cd afds-sample
python3 tools/build-inventory.py verify
```

The command re-walks the tree, recomputes every digest, and compares each record's path, media type, byte length, role, and digest.
It reports missing entries, uninventoried entries, and any record for the inventory itself.
It also checks the table above against what it actually builds, so a file added to the package without a row, or a row that no longer matches, fails the verification rather than going unnoticed.
It exits with status 0 on success and 1 on any failure, so it is usable in a pre-commit hook or a continuous-integration job.

Expected output for a clean tree is the following.

```text
inventory: 10 records, 10 entries digest-checked
boundary: README.md agrees with the exclusions
VERIFY PASSED: every entry is inventoried, lengths and SHA-256 digests match
```

If a file has been edited without rebuilding, the command names the file and shows both the recorded and the actual value.
That is the correct outcome, not a bug: the inventory exists precisely to notice such a change.

## Packing the `.afds` file

Pack to a destination outside the repository.

```sh
cd afds-sample
python3 tools/build-inventory.py pack /tmp/afds-sample-1.0.0.afds
```

Three behaviours of the pack command are worth knowing.
It verifies first and refuses to pack an unverified tree, so a stale inventory can never be shipped.
It refuses a destination inside this source tree, so the built artefact cannot accidentally be committed.
It writes entries at the archive root with no enclosing directory, as the container rules require, and it excludes `README.md` and `tools/`.

## Verifying a packed file

A packed file can be checked without unpacking it, using an ordinary ZIP reader.

```sh
unzip -l /tmp/afds-sample-1.0.0.afds
```

To verify integrity, extract to a scratch directory, copy the helper script in, and verify there.

```sh
mkdir -p /tmp/afds-check && cd /tmp/afds-check
unzip -q /tmp/afds-sample-1.0.0.afds
mkdir -p tools && cp /path/to/abd/afds-sample/tools/build-inventory.py tools/
python3 tools/build-inventory.py verify
```

An extracted archive carries no `README.md`, because that file is not package content.
The boundary check reports that it was skipped and the verification still passes, because a directory with no boundary to state is an unpacked package rather than a source directory.

A production consumer implements the full ten-step procedure at clause 31 of the specification, which also covers path-traversal checks, encryption checks, decompression limits, and token validation against the declared DTCG version.
The helper script here covers the inventory steps only and is a development aid rather than a conforming verifier.

## Two things this sample does not prove

The sample does not prove anything about assistive-technology support.
Every `result` field in `evidence/at-matrix.json` is `not-yet-tested`, and every engine version, date, observation, and tester is the same placeholder.
Assistive-technology version reads `not-applicable` on the records that name no assistive technology, which is the field-level sense of that value rather than a result.
No value in that file records an observation that took place.

The sample does not prove anything about provenance.
The inventory detects a change made in transfer; it does not identify a signer.
Anyone who can alter a file can also rebuild the inventory, so trust in a package must come from the channel it arrived on rather than from the package itself.

## Licences

Code and machine-readable artefacts are licensed GPL-3.0-only.
Documentation and prose are licensed CC BY-SA 4.0.
See [LICENSES.md](LICENSES.md) for the file-by-file arrangement.

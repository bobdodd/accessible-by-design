<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# Known limitations

This file records what the AFDS Sample package does not do and what remains unverified.
It exists because a package that shows only its guarantees is advocacy rather than documentation.

## Limitations of this sample as a package

The sample is deliberately small.
It contains one token file, one component, and one evidence file, so it cannot exercise every rule in the package format.

| Limitation | Consequence |
| --- | --- |
| No `schemas/` directory is shipped | Schema validation of the manifest and inventory cannot be demonstrated from inside the package |
| No `patterns/` directory is shipped | Multi-component flow documentation is untested by this sample |
| No `stories/` directory is shipped | The isolated and realistic-page fixtures referenced by `stack.spec.json` are absent |
| No adapters are shipped | `adapters/README.md` states the rules but no adapter transform report is present to check them against |
| No signature is present | The inventory detects transfer changes but proves nothing about who produced the package |

## Limitations of the evidence

No assistive-technology result in this package is real.

Every `result` field in `evidence/at-matrix.json` carries the value `not-yet-tested`, and every version, date, and observation field carries the same placeholder.
This is a deliberate choice.
Fabricated evidence is worse than absent evidence, because absent evidence is visible as a gap while fabricated evidence looks like a guarantee.

Consequently, every claim in the sample that depends on assistive-technology behaviour is uncertainty rather than a guarantee.
That includes both records in the Stack uncertainty list.

## Limitations of the Stack component

Stack supplies geometry only.
It provides no role, no accessible name, no state, and no keyboard behaviour.
A consumer that places list items inside a Stack and expects list semantics will produce inaccessible output, and the specification says so directly.

Stack also does not enforce the 60`ch` measure.
A consumer reading only the Stack documentation could reasonably assume text width is handled, so the non-guarantees list names the omission explicitly.

## Limitations of the token sample

The DTCG token file carries values, not relationships.

`colour.surface` and `colour.ink` are pairing candidates, not a verified contrast pair.
The format has no standard expression for a constraint of the form "this foreground is valid only on this background at a stated ratio", so the constraint cannot live in the token file.
In a complete package that constraint belongs in the component specification, and the gap in the token format is itself recorded as a project research item.

## How these limitations should be read

None of the entries above is a defect report against a shipped product.
They are the honest boundary of a draft sample.
A consumer MUST NOT treat any placeholder value in this package as a test result, and MUST NOT infer support for a combination merely because the combination appears in the matrix.

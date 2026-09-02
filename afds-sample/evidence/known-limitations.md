<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# Known limitations

This file records what the AFDS Sample package does not do and what remains unverified.
It exists because a package that shows only its guarantees is advocacy rather than documentation.

## Limitations of this sample as a package

The sample is deliberately small.
It contains one token file, one component, and one evidence file, so it cannot exercise every rule in the package format.
The single component is a layout primitive, so no claim in this sample exercises a role, an accessible name, a state, or a keyboard contract.

| Limitation | Consequence |
| --- | --- |
| No `schemas/` directory is shipped | Schema validation of the manifest and inventory cannot be demonstrated from inside the package |
| The `patterns/` directory holds the registry only | `patterns/registry.json` is shipped, but no pattern documentation accompanies it, so multi-component flow documentation is untested by this sample |
| No `stories/` directory is shipped | The isolated and realistic-page fixtures referenced by `stack.spec.json` are absent |
| No adapters are shipped | `adapters/README.md` states the rules but no adapter transform report is present to check them against |
| No signature is present | The inventory detects transfer changes but proves nothing about who produced the package |

## Limitations of the evidence

No assistive-technology result in this package is real.

Every `result` field in `evidence/at-matrix.json` carries the value `not-yet-tested`, and every date, observation, and tester field carries the same placeholder.
The version fields carry it too, with one exception: the record whose `at` value is `none` carries `not-applicable` for `atVersion`, because there is no assistive technology to have a version.
This is a deliberate choice.
Fabricated evidence is worse than absent evidence, because absent evidence is visible as a gap while fabricated evidence looks like a guarantee.

Consequently, every claim in the sample that depends on assistive-technology behaviour is uncertainty rather than a guarantee.
That includes all four records in the Stack uncertainty list.

The matrix records nine combinations against four claims: screen-reader announcement of the container on four engine and screen-reader pairs, rem-anchored gaps under operating-system font scaling, reflow at two environments, and voice-driven targeting on two platforms.
The environment fields `device`, `startingViewport`, and `zoom` were added so that the reflow records can state the conditions an observation would have to be made under.
They carry `not-applicable` on records whose claim does not involve them, which is the field-level sense of that value rather than the result-level one.

Two manual assertions still have no evidence record of any kind.
`stack-a5` covers text-spacing overrides with a doubled root font size, and `stack-a6` covers visual order matching DOM order.
Neither has a matching uncertainty entry or matrix row, so the propagation rule has not yet been applied to them.

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

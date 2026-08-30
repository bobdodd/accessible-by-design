<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# Stack

Stack is a layout primitive that applies consistent vertical rhythm between sibling elements in document order.
It is the human-readable counterpart of `stack.spec.json`, which is the machine-readable contract.
Where the two disagree, the machine-readable specification is canonical and the disagreement is a defect to be fixed.

## Purpose

Stack answers one question: how much space separates one block from the next.
It does so with a single flex column and a gap drawn from the spacing scale.
Because the gap is an alias of a scale step, spacing cannot drift away from the type scale.

Stack is deliberately narrow.
It supplies geometry and nothing else.

## Semantic model

Stack adds no role, no accessible name, and no state to its own element.

This is not an omission.
A layout primitive cannot know whether its children form a list, a labelled group, a set of landmarks, or a series of unrelated blocks.
Only the consumer knows, so only the consumer can supply the semantics.

The consumer therefore carries obligations.

| Situation | Consumer obligation |
| --- | --- |
| The children form a list | Supply list semantics in the consumer's own markup |
| The children form a labelled group | Supply the grouping role and an accessible name |
| The children are unrelated blocks | Nothing further is required |
| Any situation | Never rely on Stack to convey a relationship between children |

Visual order always follows DOM order, because Stack never reorders its children.

## Keyboard contract

Stack has no keyboard contract.

This is stated explicitly rather than left out, so that a reviewer cannot mistake an absent section for an oversight.
Stack is not focusable, contributes no tab stops, and defines no key bindings.
It never moves focus, never traps focus, and never restores focus.
All focus behaviour belongs to the children the consumer places inside it.

## Reflow behaviour

Stack is intrinsic rather than breakpoint-driven.

It uses a flex column with a `gap` expressed in `rem`.
The block direction grows with content, so the primitive reflows at any viewport size, any zoom level, and any root font size without a media query.
There are no author-fixed dimensions and no fixed heights, so user text-spacing overrides cannot truncate content.
The layout is complete with JavaScript disabled.

Stack arranges blocks along one axis and creates no relationship between a header and a cell.
No region arranged with Stack may claim the WCAG 1.4.10 two-dimensional exception.

Stack does not enforce the measure.
The 60`ch` measure is the responsibility of the Center primitive, and `typography.measure` is recorded in the specification only so a consumer can see which token governs it.

## WCAG mapping

Each row states the criterion, which branch of the two-way split it belongs to, and whether Stack supports it or leaves it to the consumer.

| Criterion | Name | Level | Branch | Relationship |
| --- | --- | --- | --- | --- |
| 1.3.1 | Info and Relationships | A | User technology support | Does not address; the consumer owns it |
| 1.3.2 | Meaningful Sequence | A | User technology support | Supports, because visual order follows DOM order |
| 1.4.4 | Resize Text | AA | User layout support | Supports, because the gap is rem-anchored |
| 1.4.10 | Reflow | AA | User layout support | Supports, through single-axis flex composition |
| 1.4.12 | Text Spacing | AA | User layout support | Supports, because there are no fixed heights |

## Assertions

Six assertions verify the contract.
Three are automated and three require manual observation.

| Identifier | Kind | What it verifies |
| --- | --- | --- |
| stack-a1 | Automated | The computed gap resolves to the `space.default` token value |
| stack-a2 | Automated | No fixed height or author-fixed dimension other than a hairline border |
| stack-a3 | Automated | No role, `aria-*` attribute, or `tabindex` added by the primitive |
| stack-a4 | Manual | No clipping and no page-level horizontal scrollbar at 320 CSS pixels and at 400% zoom |
| stack-a5 | Manual | Doubled root font size and text-spacing overrides cause no overlap |
| stack-a6 | Manual | Visual order matches DOM order in the realistic-page fixture |

## Non-guarantees

Stack does not provide list semantics.
Stack does not provide a grouping role or an accessible name.
Stack does not provide heading structure or a landmark.
Stack does not enforce the measure.
Stack does not manage focus order, focus trapping, or focus return.
Stack does not guarantee contrast between any pair of colour tokens.
Stack does not provide a basis for claiming the WCAG 1.4.10 two-dimensional exception.

## Uncertainty

Two questions are recorded as unknown rather than settled by assumption.

| Identifier | Subject | Status |
| --- | --- | --- |
| stack-u1 | Whether any shipping screen reader exposes the bare Stack container element | Not yet tested |
| stack-u2 | How rem-anchored gaps behave under operating-system font scaling in an Electron shell | Not yet tested |

Both point at `evidence/at-matrix.json`, where the corresponding evidence records also carry the status `not-yet-tested`.
No result in this sample package is a real test result.

## Tests

A complete package carries an isolated fixture and a realistic-page fixture for every component.
This sample records the paths `stories/stack.isolated.md` and `stories/stack.in-page.md` but does not ship them.
A consumer MUST treat those fixtures as absent here rather than assuming the tests exist.

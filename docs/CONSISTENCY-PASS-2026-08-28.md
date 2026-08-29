<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# Cross-document consistency pass, 2026-08-28

This is the audit trail for conflicts found while consolidating the research documentation.
All resolutions listed here are applied in the committed documents.
Superseded positions remain visible where they matter.

## Conflict 1: “grid-based UI” claim

**Problem.** Earlier wording implied that the WCAG 1.4.10 exception covers grid-based UI generally.
It conflated a semantic grid structure with CSS Grid layout.

**Resolution.** `REFLOW-AND-DATA-TABLES.md` now states the semantic test: an exception claim identifies meaning-bearing axes and how a cell depends on both.
The Grid primitive may never claim the exception.
`COLOPHON.md`, `LAYOUT-METHOD.md`, `RESEARCH-SUMMARY.md`, and `DESIGN-SYSTEMS.md` use the same distinction.

## Conflict 2: data-dense layout as an unresolved Reflow weakness

**Problem.** Earlier material treated wide tables at 400% zoom as a weakness of the method.

**Resolution.** Tables with genuine header-to-cell relationships are excepted.
D4 is now largely resolved; remaining questions are sticky behaviour, optional alternative views, cell-level code handling, and measure inside excepted regions.

## Conflict 3: understated Reflow claim

**Problem.** The method was described as compatible with Reflow but did not record that Flexbox is sufficient technique C31.

**Resolution.** The mapping now states that Flexbox-based composition implements a sufficient technique for SC 1.4.10.

## Conflict 4: Reel guarantee incomplete

**Problem.** Reel previously promised only honest overflow and a reachable container.

**Resolution.** Reel now also requires each item to be independently readable within 320 CSS pixels, following G225.

## Conflict 5: sticky positioning absent from the method

**Problem.** A reporting interface naturally invites sticky filters and toolbars, but fixed content can obscure focus and reduce reading space at zoom.
The usual C34 remedy uses layout media queries, which the method forbids.

**Resolution.** Sticky and fixed positioning are deferred until a container-driven alternative exists.
The usability cost is documented.

## Conflict 6: “no px” rationale overstated

**Problem.** Earlier wording implied CSS pixels are intrinsically inappropriate.

**Resolution.** The rule now concerns author-fixed values that fail to respond to user settings.
The CSS pixel remains an angular reference measurement; the project restriction is about the consequences of fixed author values.

## Conflict 7: research-agenda duplication

**Problem.** The colophon and research agenda began to duplicate and drift.

**Resolution.** `OPEN-QUESTIONS.md` is the single source of truth.
The colophon points to it and names only items directly affecting recorded decisions.

## Files reconciled

| File | Role after pass |
| --- | --- |
| `docs/COLOPHON.md` | Decision record, including superseded reasoning in notes |
| `docs/LAYOUT-METHOD.md` | Method, primitive guarantees, WCAG mapping, rules |
| `docs/REFLOW-AND-DATA-TABLES.md` | Detailed semantic scope of the Reflow exception |
| `docs/OPEN-QUESTIONS.md` | Single research-agenda source |
| `docs/RESEARCH-SUMMARY.md` | Orientation document |
| `research/DESIGN-SYSTEMS.md` | Prior art and scope research |

<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# Open Questions and Research Agenda

This is the single source of truth for what has not yet been settled, why it matters, and what would count as settling it.
Resolved items move to [COLOPHON.md](COLOPHON.md) with their decision record.

## A. Scope and structure

### A1. What exactly does the system contain?

Five layers are in use: principles, tokens, layout primitives, components, and patterns.
The current work defines principles, tokens in concept, and layout primitives.
Components and patterns remain unspecified.

**To settle:** whether the project ships components or only component specifications; whether a reference implementation is normative or illustrative; and where multi-component patterns such as error-summary forms, wizards, and filterable results live.

### A2. Component inventory

Coverage is measured against a component inventory, not page count.
No derivation method exists yet for organisations without a pre-existing design system.

**To settle:** how to identify de facto components and define a useful inventory.

### A3. Composition conformance

Components must be tested alone and in realistic pages.
The principle has no fixture design yet.

**To settle:** fixture composition, number of fixtures, and attribution rules for component versus composition failures.

## B. Tokens and interchange

### B1. Are W3C Design Tokens the source of truth?

The stable format supports aliases and OKLCH, both useful here.
CSS custom properties already satisfy the immediate need without a build step.

**To settle:** whether tokens generate CSS or CSS exports tokens.

**Partly settled.** The colophon now adopts DTCG JSON as the canonical portable representation for token values, so DTCG is the source of truth for the values themselves.
The build direction is still open, and DTCG remains explicitly incapable of carrying component semantics, keyboard behaviour, evidence, non-guarantees, or contrast assertions.

### B2. The `ch` problem

`ch` has no direct iOS or Android equivalent.

**To settle:** whether that is an explicit web-and-Electron scope limit or needs a native analogue of the measure axiom.

### B3. Contrast as a relationship

Token formats carry values, not assertions that one foreground token is valid against one background token at a threshold such as 7:1.

**To settle:** whether to propose an interchange representation and implement an interim project convention.

**Note.** [The portable representations research note](../research/PORTABLE-REPRESENTATIONS.md) records why such an assertion must not be stored only in DTCG `$extensions`, since extensions are optional metadata that a tool may preserve without understanding.

## C. Colour and typography

### C1. Colour system

OKLCH with constant-lightness pairings and a roughly 95% lightness surface is the leading candidate.

**To settle:** palette values, numeric versus perceptual contrast verification, and `prefers-contrast` behaviour.

### C2. Typeface

Atkinson Hyperlegible is the leading candidate.
[Braille Institute](https://www.brailleinstitute.org/freefont/) describes the family as fonts “designed to improve legibility and readability for individuals with low vision”, focused on “letterform distinction”, and offers them free for personal use and all commercial applications.

**Partly settled.** The monospace companion exists, so that sub-item is closed.
The download page states that “the hyperlegible® family of fonts is now available in three versions: Atkinson Hyperlegible®, Atkinson Hyperlegible Next®, and Atkinson Hyperlegible Mono®”, and describes the monospaced member as having “characters that each occupy the same amount of horizontal space, allowing for them to be scanned quickly in table-based and coding environments”.
The [release announcement](https://www.brailleinstitute.org/about-us/news/braille-institute-launches-enhanced-atkinson-hyperlegible-font-to-make-reading-easier/), dated 10 February 2025, calls it “Atkinson Hyperlegible Monospace” and says it is “specifically designed to assist coders by improving readability in environments where precise character spacing is critical”.
The two pages name that face differently, so the product name should be taken from the download page at the point of adoption rather than from the announcement.

The same announcement resolves the factual part of the variable-font sub-item and enlarges its consequences.
Next is described as “building upon the original Atkinson Hyperlegible typeface that was introduced in 2019”, supporting “over 150 languages (up from 27)”, and offering “seven font weights (up from two), as well as new variable and monospace versions”.
So a variable version is not hypothetical, and the weight axis went from two positions to seven.

That is a larger change to this item than closing the monospace sub-item.
The type scale is currently specified as discrete steps, which was an easy commitment when the typeface offered two weights and is a real design decision when it offers seven and a continuous axis.
A scale that admits intermediate weights has to say which weights carry meaning, because a weight difference that is too small to perceive is a distinction that exists in the specification and not on the screen.

Selecting between the original and Next is therefore a question about which set of letterform decisions the scale is built on, not a matter of taking the newest.

**To settle:** which of the three versions is the candidate, its performance at small data-dense sizes, and how seven weights and a continuous axis affect a type scale specified as discrete steps.

### C3. Conformance target

WCAG 2.2 AA is the floor; AAA is aspirational.

**To settle:** whether AAA is a per-surface commitment and whether 7:1 body contrast remains usable in data-dense reports.

## D. Layout method

### D1. Container queries versus the Switcher trick

The `flex-basis: calc((var(--threshold) - 100%) * 999)` technique predates container queries.

**To settle:** whether container queries improve legibility enough to replace the calc technique while preserving no-JavaScript behaviour and support requirements.

### D2. Custom elements without Shadow DOM in Electron

The decision against Shadow DOM implies build-time style generation for primitives.

**To settle:** the generator and its Electron packaging relationship.

### D3. Reel and Imposter accessibility

Reel needs a keyboard-reachable scroll container, reachable overflowed content, and 320-CSS-pixel readable items.
Imposter leaves focus trap, modal semantics, and focus return to an overlying dialog component.

**To settle:** whether these requirements become separate components or extend the primitives.

### D4. Data-dense layouts

**Largely resolved.** Data tables with genuine header-to-cell relationships are excepted from WCAG 1.4.10 Reflow.
The exception is semantic, not presentational.
Cells are semantic content; CSS Grid is a layout technique.
Flexbox is sufficient technique C31 for Reflow.

#### D4a. Sticky positioning without media queries

C34 un-fixes sticky headers using media queries, which the axioms forbid.

**To settle:** a container-driven equivalent or a narrow, documented axiom exception.
Until then sticky positioning is not used, at real cost to long results views.

#### D4b. G206 alternative views

A user option to avoid horizontal scrolling in an excepted view would exceed the requirement.

**To settle:** whether it should be offered and how it affects view density.

#### D4c. Cell-level code reflow

A code excerpt can need preserved indentation or can need wrapping.

**To settle:** a per-component judgement procedure rather than a global rule.

### D5. Measure inside excepted regions

A 60ch cap inside a narrow table cell may waste usable width, although cells must still meet Reflow.

**To settle:** whether `--measure` applies, reduces, or suspends inside excepted regions.

## E. Testing and evidence

### E1. Assistive-technology matrix

Claims must record engine, version, browser, observed behaviour, and date.
The matrix must include speech recognition and Reflow environment details: device, browser, starting viewport, and zoom.

**To settle:** supported combinations, pass criteria, re-test cadence, and stale-result marking.

### E2. Machine-checkable criteria

Reflow, root-font scaling, text spacing, and forced colours may be unusually automatable.

**To settle:** automated assertions and manual procedures for the remainder.

### E3. Usability testing with disabled people

Automated and manual testing cannot substitute for it.

**To settle:** feasible participation model or an explicit limitation statement.

## F. Positioning

### F1. Annotation tradition

GitHub and VA.gov address the designer-to-developer handoff with annotations.
Primitives may reduce annotation work by baking structural layout guarantees into code.

**To settle:** whether that reduction can be measured and what annotations remain useful.

### F2. Layered-equilibrium model

Accessibility can be treated as an emergent equilibrium between environment, technical constraints, capability, preference, and UI resources and modalities.

**To settle:** whether that becomes the explicit theoretical frame.

### F3. Honest disclaimer

A design system does not automatically make a service accessible.

**To settle:** exact project wording and where it appears.

## G. Components and APG patterns

The detailed treatment is in [the APG support research note](APG-SUPPORT.md), which ends with its own open-questions list.
The headline items are recorded here so this register stays the single source of truth.

### G1. Which APG patterns enter the approved catalogue?

A priority order exists, running from native primitives through disclosure, dialog, and status messaging, with tree, treegrid, and ARIA grid last.
The order is reasoned rather than evidenced.

**To settle:** what user or task evidence admits a pattern to the catalogue, and what removes one.

### G2. Adopting APG by reference

A proposed decision states that APG patterns are adopted by reference and not copied by default.
It is drafted but not yet adopted.

**To settle:** whether the decision moves to the colophon as written, and how a deviation from an APG convention is recorded and reviewed.

### G3. Minimum assistive-technology matrix per component

A component contract is only as real as the engine support behind it.
No minimum matrix has been fixed for an APG-derived component.

**To settle:** which browser, engine, and screen-reader pairs are mandatory, and what retest cadence applies when versions change.

## H. Portable representation and packaging

Two decisions are adopted and recorded in [the colophon](COLOPHON.md): AFDS is a portable bundle rather than a monolithic format, and a bundle is distributed as a single `.afds` package.
The supporting survey is in [the portable representations research note](../research/PORTABLE-REPRESENTATIONS.md) and the container is specified in [the AFDS package format document](AFDS-PACKAGE-FORMAT.md).
What remains open is listed there in full; the headline items follow.

### H1. The component-contract schema

A provisional component-specification format exists, pairing human-readable Markdown with machine-readable JSON.
It is project-invented terminology and has no external validation.

**To settle:** the JSON Schema, the stable identifier scheme, and how the vocabulary maps onto external work rather than becoming isolated.

### H2. Alignment targets after the UI Specification Schema group closed

The W3C UI Specification Schema Community Group was the closest external match to this project's needs.
It closed on 2026-05-21 having never chosen a chair, with an empty mailing list and no published report, so its charter is the whole of its output and there is no vocabulary to map onto.
No successor has been announced.

The live target is now the Design System Documentation Community Group, which has co-chairs, an explicit DTCG and CEM compatibility goal, and no draft yet.
The question is therefore no longer which group but what to send it.

**To settle:** which AFDS requirements are worth contributing, in what form, and by when — specifically whether assistive-technology evidence, explicit non-guarantees, and recorded uncertainty are proposed to that group as documentation fields, given that its charter does not currently mention them.

### H3. Package identity and signing

Inventory integrity uses SHA-256 and detects transfer changes.
It does not identify a signer or establish provenance.

**To settle:** the signature mechanism, what it signs, and how a consumer expresses trust in a publisher.

### H4. IANA registration and package-aware tooling

The underlying media type is `application/zip` in the interim, identified by the `.afds` extension and root manifest.
Editing an artefact currently means unpacking the whole package.

**To settle:** whether to pursue a dedicated media-type registration, and what editing, diffing, and delta-distribution tooling a package format needs to be workable.

### H5. Recording a promotion

An import adapter drafts artefacts, and a person promotes a draft to canonical by supplying what the source could not and accepting responsibility for the claims it makes.
The adapter declaration lists the artefacts promoted from an import, so the package records that a promotion happened.
What the promoted artefact says about its own origin is undefined, so a reader of a canonical contract cannot currently tell which of its statements a transform drafted and which a person authored.

**To settle:** whether a promoted artefact carries a provenance field naming the import report, whether a promotion records a reviewer and a date, and whether a reviewer's identity belongs in a package that makes no other identity claim.

## I. Deferred

- Implementation language and framework beyond Electron with raw HTML, CSS, and JavaScript
- Remediation-tool design
- Hosting, telemetry, and distribution
- Whether the project publishes a specification, tools, or both

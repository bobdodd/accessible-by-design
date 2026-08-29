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

### B2. The `ch` problem

`ch` has no direct iOS or Android equivalent.

**To settle:** whether that is an explicit web-and-Electron scope limit or needs a native analogue of the measure axiom.

### B3. Contrast as a relationship

Token formats carry values, not assertions that one foreground token is valid against one background token at a threshold such as 7:1.

**To settle:** whether to propose an interchange representation and implement an interim project convention.

## C. Colour and typography

### C1. Colour system

OKLCH with constant-lightness pairings and a roughly 95% lightness surface is the leading candidate.

**To settle:** palette values, numeric versus perceptual contrast verification, and `prefers-contrast` behaviour.

### C2. Typeface

Atkinson Hyperlegible is the leading candidate.

**To settle:** its performance at small data-dense sizes, a monospace companion, and variable-font implications for the scale.

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

## G. Deferred

- Implementation language and framework beyond Electron with raw HTML, CSS, and JavaScript
- Remediation-tool design
- Hosting, telemetry, and distribution
- Whether the project publishes a specification, tools, or both

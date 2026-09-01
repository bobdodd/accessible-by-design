<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# Research Summary to Date

This is the orientation document for the research-and-planning phase.
It states the premise, evidence, prior art, decisions, additions, and unresolved questions before implementation begins.

## Premise

Accessibility work is commonly retrofitted: build, audit late, patch individual findings, repeat.
A design-system approach instead attaches requirements to reusable components and patterns, allowing fixes and their rationale to propagate.

Survey research found design systems were the most cited of four concrete accessibility actions among practitioners, named in 28 of 58 analysed interview sessions (48%), with adoption rising from 2 of 6 sessions in 2017 (33%) to 22 of 42 between November 2019 and March 2020 (52%).
The inclusion of people with disabilities in usability testing was cited in 18 sessions (31%), training in 7 (12%), and code considerations in 5 (8%).

Accessibility is treated here as a crosscutting concern with two branches:

- *User technology support*: assistive-technology compatibility, roles, names, states, focus, keyboard
- *User layout support*: reflow, measure, spacing, contrast, reading order

The distinction is useful but not mechanical.
The Reflow exception, for example, looks geometric but is decided by whether two-dimensional semantic relationships are needed for understanding.

## Honest limit

Using a design system does not immediately make a service accessible.
A system can improve the available UI resources and modalities but cannot replace disabled-user research, assistive-technology testing, content quality, or contextual judgement.

## Design-system layers

| Layer | Contents | Accessibility role |
| --- | --- | --- |
| Principles | Non-negotiable commitments | Conformance floor |
| Tokens | Named values for colour, type, space, radii, motion | Reusable visual values and preferences |
| Layout primitives | Composable arrangement rules | Reflow, resize, text spacing, reading sequence |
| Components | Interactive elements with semantics and behaviour | Names, roles, states, keyboard, focus |
| Patterns | Multi-component flows and guidance | Error handling and cross-component focus management |

## Tokens

The W3C Design Tokens format reached its first stable version in October 2025.
It supports aliasing, theming, accessibility variants, OKLCH and other modern colour spaces, and cross-platform output.

The important limitation is that tokens represent values, not relationships with thresholds.
There is no standard way to assert that a foreground token is valid against a particular background token at 7:1.
That is a candidate contribution area.

## Prior art

### GOV.UK

The strongest public example combines automated, manual, and usability testing; tests across browsers, devices, screen readers, magnifiers, and speech recognition; records component acceptance criteria in version control; and requires components to be tested in realistic pages rather than only in isolation.

The realistic-page rule is central.
A component can pass in a Storybook cell and still create a broken heading sequence, duplicate landmark, or unreachable focus target when composed.

### Annotations

GitHub treats annotations as carriers for intent that design mock-ups do not visibly express: controls, landmarks, heading structure, image intent, labels, roles, and focus order.
VA.gov provides categories for these concerns and includes a Notes category for known uncertainty about assistive-technology behaviour.

The project adopts uncertainty as a first-class record type and follows the economy rule: do not annotate what visual design, component properties, or code already guarantee.

### Conformance gates

A common four-axis gate asks whether a component is visually accessible, screen-reader compatible, operable, and understandable.
That is useful but insufficient without engine coverage and reflow/zoom evidence.

## Recurrent gaps

1. Layout is treated as visual rather than as accessibility, despite Reflow, Resize Text, and Text Spacing being layout criteria.
2. Systems test components but not composition.
3. Screen-reader claims often omit engine, browser, version, observed behaviour, and date.
4. Tokens carry values but not accessibility constraints.
5. Prose documentation drifts when assertions do not travel with specifications.

## Layout method

The project uses Every Layout-style intrinsic primitives, not viewport breakpoints.
Every dimension is user-relative; measure is capped at 60ch; there are no fixed heights; and layout works without JavaScript.
The scale is rooted in `rem`, so a user root-font change propagates through type and space.

The primitives are Stack, Box, Center, Cluster, Sidebar, Switcher, Cover, Grid, Frame, Reel, Imposter, Icon, and Container.
Each must declare guarantees and non-guarantees.
Geometry primitives intentionally carry no ARIA because the consumer determines whether content is a list, dialog, group, or something else.

Flexbox-based composition is sufficient technique C31 for WCAG 1.4.10 Reflow.
This is stronger than claiming compatibility: the project implements a technique the Working Group lists as sufficient.

Every delineated surface uses a transparent outline so it survives forced-colours mode.
Shadow DOM is rejected because it can obstruct inherited styles, user stylesheets, forced-colours overrides, and accessible relationships across component boundaries.

## Reflow and tables

Data tables may use the two-dimensional Reflow exception only where a two-dimensional semantic relationship is needed for usage or meaning.
The exception is not an allowance for CSS Grid layout.

A table cell's meaning can depend on both row and column headers.
A card collection arranged with CSS Grid has no such relationship.
Cells, headings, introductory prose, filters, and pagination remain ordinary reflowing content.
Excepted scrolling is scoped to its own container rather than allowed to impose page-level horizontal scroll.

Every Reel item must be readable within 320 CSS pixels.
Sticky and fixed positioning are deferred because they can obscure focus at zoom and the normal media-query remedy conflicts with the no-layout-media-query axiom.

## Decisions already made

| Area | Decision |
| --- | --- |
| Unit of accessibility | Components and patterns rather than pages |
| Classification | User technology support and user layout support |
| Specifications | Assertions or manual procedures are mandatory |
| Guarantees | Non-guarantees are mandatory too |
| Conformance | Component and realistic-page composition levels |
| AT evidence | Engine, browser, version, observation, and date |
| Layout | Intrinsic primitives, no layout media queries, no fixed heights |
| Scale | Shared type-and-space modular scale rooted at `rem` |
| Measure | 60ch exception-based cap |
| Reflow exception | Semantic two-dimensional structure only; Grid primitive never qualifies |
| Scroll | Two-dimensional scrolling scoped to the excepted container |
| Positioning | No sticky or fixed positioning pending a container-driven equivalent |
| Documentation | Markdown, sentence-per-line, real headings, regular tables |
| Base representation | AFDS 1.0.0, a portable bundle rather than one universal file format |
| Distribution | One ZIP-based `.afds` package with a root manifest and a SHA-256 inventory |
| Token format | DTCG JSON is canonical for token values, and never the carrier of accessibility contracts |
| Adapters | No adapter is canonical; every transform reports mappings, warnings, and losses |
| Licencing | Code is GPL-3.0-only; documentation is CC BY-SA 4.0 |

## What this project claims to add

1. Layout as a first-class accessibility concern in the system
2. Intrinsic available-space primitives rather than breakpoint guesses
3. Engine-qualified assistive-technology claims with uncertainty recorded explicitly
4. Assertions that travel with specifications
5. Composition conformance as well as component conformance
6. A documented token-standard gap around contrast relationships
7. A portable package format that carries the accessibility contract, evidence, and uncertainty as first-class records rather than leaving them in a design tool or an untracked spreadsheet

## Open questions

The full agenda is [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md).
The most consequential near-term questions are token source-of-truth, AAA contrast in data-dense reporting, container queries versus the Switcher technique, a non-media-query strategy for sticky behaviour, and component-inventory derivation for organisations without a design system.

## Related documents

| Document | Purpose |
| --- | --- |
| [APG support](APG-SUPPORT.md) | How ARIA Authoring Practices patterns are adopted by reference, with a registry, keyboard contracts, and a testing model |
| [AFDS specification](AFDS-SPECIFICATION.md) | The full specification. Part IV carries the `.afds` container, manifest, inventory, verification procedure, and security rules |
| [Portable representations](../research/PORTABLE-REPRESENTATIONS.md) | Survey of DTCG, Custom Elements Manifest, CSF, Open UI, W3C community work, and the commercial ecosystem |

## Sources

- W3C Design Tokens Community Group, Design Tokens Format Module
- GOV.UK Design System accessibility documentation and acceptance criteria
- GitHub design-system annotation articles
- VA.gov accessibility annotations
- Supernova accessibility-in-design-system guidance
- Practitioner survey research on accessibility strategies
- Aspect-oriented accessibility modelling
- W3C WAI, Understanding SC 1.4.10 Reflow
- *Every Layout*, Heydon Pickering and Andy Bell

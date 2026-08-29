<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# Design Systems and Accessibility: Scope, Prior Art, and Where Layout Fits

This research note establishes the scope of a design system, surveys existing accessibility practice, identifies recurring gaps, and explains where the layout method belongs.

## Evidence for the approach

Design systems were the most frequently cited accessibility strategy in practitioner interviews, appearing in 48% overall and rising from 33% in 2017 to 52% in 2019-2020.
The reported conclusion was that organisations should build accessibility into components rather than rely only on specialist teams or post-hoc audits.
Usability testing with disabled people was cited in 31% of interviews, audits in 17%, and empathy labs in 10%.

Accessibility is usefully understood as a crosscutting concern.
It spans components rather than residing in one module.
A productive split is between user technology support and user layout support.

The split needs care.
The WCAG Reflow exception seems to be about layout but depends on semantics: whether the two-dimensional relationship carries meaning needed to understand the content.
Classification follows what carries meaning, not the visual mechanism that produces it.

## Five layers

| Layer | Contents | Accessibility role |
| --- | --- | --- |
| Principles | Commitments and non-negotiables | Sets floor and non-tradeable constraints |
| Tokens | Named platform-neutral values | Space, type, colour, motion, contrast pair candidates |
| Layout primitives | Composable arrangement rules | Reflow, resize, text spacing, reading sequence |
| Components | Interactive elements with semantics and behaviour | Roles, names, states, keyboard, focus |
| Patterns and guidance | Multi-component flows and documentation | Errors, focus management, workflow behaviour |

Confusing these layers is the source of many scope disputes.

## Tokens

The W3C Design Tokens format reached its first stable version in 2025.
It provides a vendor-neutral way to exchange named values, types, descriptions, aliases, themes, and modern colour spaces including OKLCH.
It supports accessibility variants and cross-platform transformation.

The format's important limitation is that it represents values, not assertions about relationships.
It has no standard expression for “this foreground token is valid only on this background token at 7:1.”
Contrast is a relationship with a threshold.
That gap is a plausible contribution area.

The modular scale and 60ch measure are token-like values.
Aliasing can express each scale step by reference to the prior step.
`ch` does not round-trip directly to native platforms, so this is a deliberate web-and-Electron scope constraint unless a native analogue is defined.

## Existing implementations

### GOV.UK Design System

GOV.UK provides the strongest public example of a rigorous and honest design system.
It says directly that using the system does not immediately make a service accessible.

Practices to adopt:

- Automated, manual, and usability testing as distinct, non-substitutable activities
- Browser, device, screen-reader, magnifier, and speech-recognition coverage
- Component acceptance criteria held in version control
- Testing components inside realistic pages, not only in isolation

The realistic-page rule matters because isolated components can still generate broken heading order, duplicate landmarks, or inaccessible focus behaviour in composition.

### Annotations

GitHub describes annotations as carriers for intent that design mock-ups do not visibly express: controls, landmarks, heading structure, image purpose, labels, roles, and focus order.
VA.gov provides categories for these concerns and includes a Notes category for known uncertainty about assistive-technology behaviour.

The project adopts uncertainty explicitly.
It also follows GitHub's economy rule: do not annotate what the visual design, component API, or coded component already guarantees.

### Readiness gates

A common readiness model checks visual accessibility, screen-reader compatibility, operability, and understandability.
It is useful but incomplete when it does not record engines tested or address reflow, zoom, text spacing, and forced colours.

## Recurring gaps

1. Layout is treated as visual rather than as an accessibility concern.
2. Components are tested in isolation but not in composition.
3. Assistive-technology claims omit engine, browser, version, observation, and test date.
4. Tokens express values but not constraints or relationships.
5. Documentation does not carry machine-readable assertions and drifts from implementation.

## How Every Layout fits

The layout method is a foundation concern, not a component concern.
It must appear in four forms.

### Principles

The measure cap, user-relative dimensions, available-space response, no fixed heights, and no-JavaScript completion are non-negotiable axioms.

### Tokens

The modular scale, type scale, and measure are named values with aliases and descriptions.

### Primitives

Primitives are distinct from semantic components.
They carry geometry, not ARIA, because the consumer knows whether the content is a list, dialog, group, or something else.
Each primitive documents both guarantees and non-guarantees.

| Primitive | Guarantees | Does not provide |
| --- | --- | --- |
| Stack | Scale-based rhythm, no redundant final margin, DOM order | List semantics |
| Box | Forced-colours boundary through transparent outline | Semantic role |
| Center | Measure enforcement | Universal zoom-visibility guarantee |
| Sidebar / Switcher | Container-driven reflow | Semantics |
| Grid | Wrapping self-contained items | Semantics or a Reflow-exception basis |
| Reel | Honest overflow, reachable container, each item readable at 320 CSS pixels | Hidden-content reachability guarantee |
| Imposter | Overlay geometry and safe overflow | Focus trap, modal semantics, return focus |

A visual Grid primitive is not a semantic grid.
No region using it may claim the WCAG Reflow exception.

### Acceptance criteria

Each primitive needs tests for 400% zoom, doubled root font size, text-spacing overrides, forced colours, DOM/visual order consistency, JavaScript-disabled operation, and realistic-page composition.

## Extensions claimed by this project

1. Layout as a first-class accessibility concern
2. Intrinsic primitives responding to available space rather than breakpoint guesses
3. Engine-qualified AT claims and first-class uncertainty
4. Assertions travelling with specifications
5. Composition conformance beside component conformance
6. A documented token-format gap around contrast relationships

## Sources

- W3C Design Tokens Community Group, Design Tokens Format Module
- GOV.UK Design System accessibility strategy and acceptance criteria
- GitHub engineering articles on design-system annotations
- VA.gov Design System accessibility annotations
- Supernova accessibility-in-design-system guidance
- Practitioner research on accessibility strategy adoption
- W3C WAI, Understanding SC 1.4.10 Reflow
- *Every Layout*, Heydon Pickering and Andy Bell

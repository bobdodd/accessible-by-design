<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# Design Systems and Accessibility: Scope, Prior Art, and Where Layout Fits

This research note establishes the scope of a design system, surveys existing accessibility practice, identifies recurring gaps, and explains where the layout method belongs.

## Evidence for the approach

Putnam, Rose and MacDonald interviewed user-experience practitioners in three phases between 2017 and 2020 and asked what their organisations had done about accessibility [1].
Of 58 analysed interview sessions, 44 (76%) reported awareness of at least some action and 14 (24%) reported that no action had been taken.
The paper identifies four common concrete actions, and gives a count for each: design systems in 28 sessions (48%), inclusion of people with disabilities in usability testing in 18 (31%), training in 7 (12%), and code considerations in 5 (8%).

Design systems were the most cited of the four, described as "component and/or pattern libraries" in which "accessibility was coded in reusable components".
Adoption rose across the fieldwork: 2 of 6 sessions in 2017 (33%), 4 of 10 in late 2018 and early 2019 (40%), and 22 of 42 between November 2019 and March 2020 (52%).
The paper states its implication for industry directly, that an organisation not moving towards a design system is "behind and therefore not capitalizing on a design system's abilities to structurally embed accessibility in your products".

Two further findings in the same paper constrain what this project may claim from it, and are recorded here for that reason.
First, the groups most cited as responsible for accessibility were dedicated teams or specialists and engineers or developers, and the paper warns that resting responsibility there can produce "an attitude of 'that is someone else's problem'" and at worst "an abdication of responsibility" among other practitioners.
A design system can concentrate responsibility the same way, if it becomes the place where accessibility is assumed to have been dealt with already.
Second, the paper reports that the primary drivers of accessibility were compliance with top-down standards rather than ethical commitment, and reads this as indicating "a need for rigorous regulation".
It does not present design systems as a replacement for audit or for regulation, and this note does not either.

Accessibility is usefully understood as a crosscutting concern.
It spans components rather than residing in one module.
A productive split is between user technology support and user layout support.

The split needs care.
The WCAG Reflow exception seems to be about layout but depends on semantics: whether the two-dimensional relationship carries meaning needed to understand the content [8].
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

The W3C Design Tokens Community Group published Design Tokens Format Module 2025.10, announced on 28 October 2025 as the specification's first stable version [2].
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
It says directly that "Using the GOV.UK Design System in a service does not immediately make that service accessible", and that additional "research, design, development and testing work" is needed "even when using accessible styles, components and patterns" [3].

Practices to adopt:

- Automated, manual, and usability testing as distinct, non-substitutable activities
- Browser, device, screen-reader, magnifier, and speech-recognition coverage
- Component acceptance criteria held in version control
- Testing components inside realistic pages, not only in isolation

The realistic-page rule matters because isolated components can still generate broken heading order, duplicate landmarks, or inaccessible focus behaviour in composition.

### Annotations

GitHub describes annotations as notes that "help make the unseen explicit by conveying design intent that isn't shown visually", adding "technical semantics and specialist knowledge" to a design [4].
VA.gov defines categories for these concerns, including Buttons, Feedback, Focus order, Headings, Images, Inputs, Landmarks, Links, Lists, and Reading order [5].
Its Notes category is for "Any details that don't fit into the other annotation categories", and the page gives uncertainty as its worked example: "if you're uncertain how an interaction may work (eg. for assistive technology users) and want to call attention to that unknown" [5].

The project adopts uncertainty explicitly, and goes further than VA.gov by making it a record type in the package rather than a note in a design file.
It also follows GitHub's economy rule, which is to "Only include key information that isn't conveyed visually, isn't in the component properties, and isn't already baked into a coded component" [6].

### Readiness gates

Vendor guidance of the kind Supernova publishes checks visual accessibility, screen-reader compatibility, operability, and understandability [7].
A model of that shape is useful but incomplete when it does not record which engines were tested, or address reflow, zoom, text spacing, and forced colours.

## Recurring gaps

1. Layout is treated as visual rather than as an accessibility concern.
2. Components are tested in isolation but not in composition.
3. Assistive-technology claims omit engine, browser, version, observation, and test date.
4. Tokens express values but not constraints or relationships.
5. Documentation does not carry machine-readable assertions and drifts from implementation.

## How Every Layout fits

The layout method, following Pickering and Bell [9], is a foundation concern, not a component concern.
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

## References

1. Putnam, C., Rose, E. J. and MacDonald, C. M. (2022). "It would be better. It would be much worse": Understanding Accessibility in User Experience Practice with Implications for Industry and Education. *ACM Transactions on Accessible Computing*. <https://doi.org/10.1145/3575662>
2. W3C Design Tokens Community Group (2025). *Design Tokens Format Module 2025.10*. <https://www.designtokens.org/TR/2025.10/format/>. Announcement, 28 October 2025: <https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/>
3. Government Digital Service. *GOV.UK Design System: accessibility*. <https://design-system.service.gov.uk/accessibility/>. Accessibility strategy: <https://design-system.service.gov.uk/accessibility/accessibility-strategy/>. Accessibility acceptance criteria in version control: <https://github.com/alphagov/govuk-frontend/blob/main/docs/contributing/test-components-using-accessibility-acceptance-criteria.md>
4. Ellis, J. *Design system annotations, part 1: How accessibility gets left out of components*. The GitHub Blog. <https://github.blog/engineering/user-experience/design-system-annotations-part-1-how-accessibility-gets-left-out-of-components/>
5. Department of Veterans Affairs. *Accessibility annotations for VA.gov applications*. VA.gov Design System. <https://design.va.gov/accessibility/accessibility-annotations>
6. Ellis, J. *Design system annotations, part 2: Advanced methods of annotating components*. The GitHub Blog. <https://github.blog/engineering/user-experience/design-system-annotations-part-2-advanced-methods-of-annotating-components/>
7. Supernova. *Accessibility in Design Systems: A Comprehensive Approach Through Documentation and Assets*. <https://www.supernova.io/blog/accessibility-in-design-systems-a-comprehensive-approach-through-documentation-and-assets>
8. W3C Web Accessibility Initiative. *Understanding Success Criterion 1.4.10: Reflow*. <https://www.w3.org/WAI/WCAG22/Understanding/reflow>
9. Pickering, H. and Bell, A. *Every Layout: Relearn CSS layout*. <https://every-layout.dev/>

## Corrections

2026-08-30. An earlier version of the "Evidence for the approach" section stated that audits were cited in 17% of interviews and empathy labs in 10%. Neither figure appears in reference [1] and neither is supported by any source. The paper reports four common concrete actions only, with counts for design systems (48%), usability testing (31%), training (12%), and code considerations (8%); it gives no percentage for audits, and "empathy lab" appears in it as one participant's description of a facility rather than as a counted category. The false figures have been removed and every remaining figure in that section has been checked against the paper.

The same version summarised the paper as concluding that organisations should build accessibility into components "rather than rely only on specialist teams or post-hoc audits". That misstated it in the direction of this project's argument. The paper does warn that concentrating responsibility in specialist teams and developers risks abdication by others, but on audit and compliance it reports the opposite emphasis, reading its findings as indicating "a need for rigorous regulation". The section now records that.

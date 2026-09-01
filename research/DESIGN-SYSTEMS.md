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

Practices to adopt, each taken from the published accessibility strategy [3]:

- Automated testing, manual testing, and user research treated as separate activities used together. The team "does not solely rely on automated testing processes", citing a 2017 GDS study that concluded "only about 30% of issues are found by automated testing tools, such as axe-core".
- Assistive-technology coverage recorded as an explicit list of access routes rather than left implicit: screen readers and screen magnifiers through Assistiv Labs and macOS, high contrast and other display modes through Assistiv Labs and browsers, and speech recognition software through Windows testing computers and macOS.
- Accessibility acceptance criteria maintained as standing guidance that manual testing follows, published in the same repository as the code [3].
- User research that "must include disabled people" and should cover a variety of access needs and impairment types.

Testing components inside realistic pages rather than only in isolation is a practice this project adds. It is not taken from GOV.UK, whose published strategy does not mention it.
It matters because isolated components can still generate broken heading order, duplicate landmarks, or inaccessible focus behaviour in composition, which is why composition conformance appears below as an extension claimed here rather than as prior art.

### Annotations

GitHub describes annotations as notes that "help make the unseen explicit by conveying design intent that isn't shown visually", adding "technical semantics and specialist knowledge" to a design [4].
VA.gov defines categories for these concerns, including Buttons, Feedback, Focus order, Headings, Images, Inputs, Landmarks, Links, Lists, and Reading order [5].
Its Notes category is for "Any details that don't fit into the other annotation categories", and the page gives uncertainty as its worked example: "if you're uncertain how an interaction may work (eg. for assistive technology users) and want to call attention to that unknown" [5].

The project adopts uncertainty explicitly, and goes further than VA.gov by making it a record type in the package rather than a note in a design file.
It also follows GitHub's economy rule, which is to "Only include key information that isn't conveyed visually, isn't in the component properties, and isn't already baked into a coded component" [6].

### Readiness gates

Vendor guidance of the kind Supernova publishes offers a component scorecard with four categories: "Visually accessible", "Screen reader compatibility", "Navigable and operable", and "Understandable" [7].
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

1. Putnam, C., Rose, E. J. and MacDonald, C. M. (2023). "It could be better. It could be much worse": Understanding Accessibility in User Experience Practice with Implications for Industry and Education. *ACM Transactions on Accessible Computing*, 16(1), 1-25. <https://doi.org/10.1145/3575662>
2. Design Tokens Community Group (a W3C Community Group). *Design Tokens Format Module 2025.10*. Editors: Daniel Banks, Mike Kamminga, Ayesha Mazrana (Mazumdar), James Nash, Adekunle Oduye, Kevin Powell. <https://www.designtokens.org/TR/2025.10/format/>. Announced as the first stable version by Kaelig Deloumeau-Prigent, 28 October 2025: <https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/>
3. GOV.UK Design System. *Accessibility*. <https://design-system.service.gov.uk/accessibility/>. *Accessibility strategy*: <https://design-system.service.gov.uk/accessibility/accessibility-strategy/>. Accessibility acceptance criteria in the govuk-frontend repository: <https://github.com/alphagov/govuk-frontend/blob/main/docs/contributing/test-components-using-accessibility-acceptance-criteria.md>. The design system homepage states that it "is maintained by a team at the Government Digital Service": <https://design-system.service.gov.uk/>
4. Jan Maarten. *Design system annotations, part 1: How accessibility gets left out of components*. The GitHub Blog. <https://github.blog/engineering/user-experience/design-system-annotations-part-1-how-accessibility-gets-left-out-of-components/>
5. VA.gov Design System. *Accessibility annotations for VA.gov applications*. <https://design.va.gov/accessibility/accessibility-annotations>
6. Jan Maarten. *Design system annotations, part 2: Advanced methods of annotating components*. The GitHub Blog. <https://github.blog/engineering/user-experience/design-system-annotations-part-2-advanced-methods-of-annotating-components/>
7. Romero, C. *Accessibility in Design Systems: A Comprehensive Approach Through Documentation and Assets*. Supernova. <https://www.supernova.io/blog/accessibility-in-design-systems-a-comprehensive-approach-through-documentation-and-assets>
8. W3C Web Accessibility Initiative. *Understanding Success Criterion 1.4.10: Reflow*. <https://www.w3.org/WAI/WCAG22/Understanding/reflow>
9. Pickering, H. and Bell, A. *Every Layout: Relearn CSS layout*. <https://every-layout.dev/>

## Corrections

2026-08-30. An earlier version of the "Evidence for the approach" section stated that audits were cited in 17% of interviews and empathy labs in 10%. Neither figure appears in reference [1] and neither is supported by any source. The paper reports four common concrete actions only, with counts for design systems (48%), usability testing (31%), training (12%), and code considerations (8%); it gives no percentage for audits, and "empathy lab" appears in it as one participant's description of a facility rather than as a counted category. The false figures have been removed and every remaining figure in that section has been checked against the paper.

The same version summarised the paper as concluding that organisations should build accessibility into components "rather than rely only on specialist teams or post-hoc audits". That misstated it in the direction of this project's argument. The paper does warn that concentrating responsibility in specialist teams and developers risks abdication by others, but on audit and compliance it reports the opposite emphasis, reading its findings as indicating "a need for rigorous regulation". The section now records that.

A check of the remaining eight references against their sources found three further faults.

References [4] and [6] were attributed to "Ellis, J.", a name that does not appear on either article and was not taken from any source. The byline on both reads "Jan Maarten", and is cited that way rather than inverted, because the published byline gives no surname to invert.

Two of the four practices listed under GOV.UK were not supported by the page they were attributed to. The accessibility strategy does not mention testing components inside realistic pages rather than in isolation; that is this project's own practice and is now identified as such, which also removes a contradiction, since composition conformance was already listed further down as an extension claimed here. The claim that acceptance criteria are held in version control is not stated on the strategy page either, though criteria are published in the govuk-frontend repository, so the bullet now says what can be shown. The remaining two bullets were vaguer than the source and are now quoted from it, including the strategy's statement that the team "does not solely rely on automated testing processes" because a 2017 GDS study concluded that "only about 30% of issues are found by automated testing tools, such as axe-core".

Reference [5] carried "Department of Veterans Affairs" as a corporate author, which the page does not state. Reference [7] had no author, and the article is by Cintia Romero. Reference [2] omitted the editors and the announcement's author. The Supernova scorecard categories were paraphrased and are now quoted. References [8] and [9] were checked and were already correct.

Reference [1] was also cited incorrectly, as "It would be better. It would be much worse" and dated 2022. The title reads "It could be better. It could be much worse", and the article was published in volume 16, issue 1, in March 2023. The 2022 date was taken from the copyright line of the author-accepted PDF rather than from the published record. Citation metadata in this note should be checked against the DOI record, not against the front matter of a hosted copy.

2026-09-01. The retraction of the two false figures was applied to this note only.
`docs/AFDS-USER-GUIDE.md` and `docs/RESEARCH-SUMMARY.md` both restated them and continued to carry them for two days after they were retracted here.
Both documents now give the supported counts instead, and the user guide points back to this note for the check.
The lesson recorded is that retracting a figure in the note that established it does not retract it from the documents derived from it, so a correction has to be followed through every document that repeated the claim.
The website did not carry the false figures and needed no change.

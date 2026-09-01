<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# Supporting the ARIA Authoring Practices Guide

This research note sets out how the design system should relate to the W3C [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/), referred to throughout as the APG.
It is written for the research-and-planning phase of this project and contains no implementation commitments.
The proposed decision at the end of the note is explicitly not yet adopted.

The short answer is that the system should treat the APG as a pattern and interaction reference, and then convert the relevant guidance into versioned component contracts, automated and manual tests, and design-tool annotations.
It should not treat APG examples as drop-in components.
It should not mistake APG conformance for [WCAG](https://www.w3.org/TR/WCAG22/) conformance.

That distinction is the reason this note exists.
The APG is informative guidance published by the W3C's ARIA Working Group.
[WCAG 2.2](https://www.w3.org/TR/WCAG22/) and [WAI-ARIA](https://www.w3.org/TR/wai-aria-1.2/) are normative standards.
A component can follow every keystroke recommendation in an APG pattern and still fail WCAG, and a component can depart from an APG key map and still conform to WCAG.
A system that blurs the two will eventually make a false conformance claim.

## The standards relationship

Five artefacts are in play, and each has a distinct job.
Confusing them is the most common cause of arguments about what a component is required to do.

| Artefact | What it governs | Role in this system |
| --- | --- | --- |
| Native HTML | Default semantics, behaviour, and baseline keyboard operation | First choice; avoid custom widgets wherever native controls work |
| WCAG 2.2 | Required accessibility outcomes and the conformance target | The floor, and the source of acceptance criteria |
| WAI-ARIA | Roles, states, properties, and accessibility-tree semantics | Used only where native HTML cannot express the interaction |
| APG | Common interaction patterns, keyboard conventions, implementation guidance, and worked examples | Reference for design intent and component behaviour |
| This design system | Approved product-specific implementation, tests, documentation, and assistive-technology evidence | The enforceable operational layer |

Read the table as a sequence of narrowing scopes rather than as a hierarchy of authority.
Native HTML supplies the widest and cheapest set of guarantees.
WCAG states the outcomes that must hold regardless of implementation choice.
ARIA supplies vocabulary for the cases HTML cannot express.
The APG explains how those pieces fit together for interactions that recur across products.
The design system is the only layer that actually ships, and therefore the only layer that can carry evidence.

Two of these are normative and three are not, and the difference matters.
WCAG and WAI-ARIA are normative: they define requirements, and a claim of conformance against them is meaningful and auditable.
The APG is informative: it describes good practice and interoperable convention without creating a conformance target.
Native HTML is normative as a specification, but "use native HTML" is a project preference rather than a WCAG requirement.
The design system is normative *within this project only*, because it is the layer where the project chooses to make its own requirements binding.

It follows that the system must never publish a sentence of the form "this component conforms to the APG" as though that were an accessibility claim.
The APG has no conformance model to conform to.
The publishable claims are the WCAG criteria met, the ARIA semantics used, and the recorded assistive-technology results.

### What the APG actually offers

The APG exists to show how ARIA semantics, HTML, CSS, JavaScript, keyboard support, accessible names, page structure, and high-contrast support fit together for common user-interface patterns.
It provides thirty patterns, ranging from buttons and disclosure controls through to complex tree grids, counted from the [pattern index](https://www.w3.org/WAI/ARIA/apg/patterns/) on 31 August 2026.
Each pattern typically describes the interaction, the required and expected keyboard behaviour, the roles, states, and properties involved, and one or more functional examples.

That combination is genuinely valuable and hard to reproduce.
The keyboard conventions in particular encode decades of accumulated desktop-platform behaviour that users already know.
Reinventing them per product is both wasteful and hostile to users.

The value is in the interaction model, not in the example code.
This note returns to that point in the section on reference implementations.

## Normative form

Clause 24 of [the AFDS specification](AFDS-SPECIFICATION.md) now carries this policy as the claimable profile `afds-patterns-native-first`, and clause 9 carries the five-status derivation vocabulary as a core requirement binding every package.
Where this note and those clauses disagree, the clauses govern.
This note remains as the reasoning behind the profile.

Two differences are worth naming.
Two of the five statuses were renamed when the vocabulary moved into the core, because the core may not name a particular external pattern library: `APG-derived` and `APG-adjacent` below are `pattern-derived` and `pattern-adjacent` in clause 9.
The other three keep their names as `native-first`, `custom`, and `prohibited`.
The twelve fields below are, in the specification, a review checklist that collects requirements stated across eight core clauses rather than a requirement of the profile itself; clause 24.4 records which clause owns each item.

The policy is adopted. The colophon decision "Native HTML first, and published patterns by reference" records it, and this project claims `afds-patterns-native-first` in the packages it publishes.
The proposed decision that formerly closed this note is withdrawn, for the reasons given under "The adopted decision" below.

## The core policy

The system should adopt a single policy statement and repeat it wherever the question arises.

> WCAG establishes the required outcome.
> Native HTML is preferred.
> ARIA fills genuine semantic gaps.
> APG supplies the interaction model for recognised custom patterns.
> Our design system specifies, tests, versions, and evidences the implementation we actually ship.

Each clause does work.

The first clause fixes the acceptance criteria in a normative standard, so that arguments about behaviour resolve against an outcome rather than a preference.
The second clause sets the default engineering answer, because native elements arrive with focus behaviour, activation semantics, disabled-state handling, and forced-colours treatment already implemented and already tested by browser vendors.
The third clause constrains ARIA to a repair role, which is the role it was designed for.
The fourth clause admits that some interactions genuinely have no native equivalent, and that when the system builds one it should behave the way users already expect.
The fifth clause locates responsibility: no external document can carry evidence about the code this project ships.

## The pattern registry

The system should maintain a registry mapping every component or pattern to exactly one of five statuses.
The registry is the mechanism that keeps the policy from becoming decorative.

| Status | Meaning | Example |
| --- | --- | --- |
| Native-first | A native element fully supplies the interaction | `<button>`, `<details>`, `<input type="checkbox">` |
| APG-derived | A custom component implements a recognised APG pattern | Dialog, Tabs, Menu Button, Combobox |
| APG-adjacent | Similar interaction, but intentionally differs from the pattern | A product-specific filter panel |
| Custom | No mature APG pattern applies | A complex audit visualisation |
| Prohibited | The pattern creates more accessibility cost than value | Site navigation implemented as an ARIA menu |

The statuses are not a quality ranking.
Native-first is the cheapest and safest status, and most of the system should sit there, but a Dialog is not defective for being APG-derived.
The point of the registry is that the status is a recorded decision with a rationale, rather than an accident of whoever wrote the component first.

Two statuses deserve particular attention.

*APG-adjacent* is the honest status for components that borrow an interaction feel without claiming the pattern.
It exists so that authors do not label a component "APG Combobox" when it deviates materially, which would mislead both implementers and testers.
An APG-adjacent entry must state which pattern it resembles and exactly where and why it departs.

*Prohibited* exists so that the system can say no once, in writing, rather than re-litigating the same bad idea in every review.
A prohibition must state the cost that motivated it, and must be revisitable if the underlying support picture changes.

### Required specification fields for an APG-derived component

Every APG-derived entry records the following twelve fields.
These are fields, not prose suggestions: a specification missing one of them is incomplete and should fail review.

These twelve are specification fields, written for engineering review.
They are not the eleven design-tool annotation fields defined further down this document, which are written for design handoff.
The two lists overlap in subject and differ in audience, count, and purpose, so a count of one is never a count of the other.

1. **APG pattern name and source URL.**
   The specific pattern, linked, so a reader can check the reference rather than trust the summary.
2. **Native alternative considered, and why it was insufficient.**
   This is the field that enforces the native-first rule.
   An entry that cannot answer it should probably be native-first.
3. **Semantic model.**
   Native elements used, ARIA roles, states, properties, and the relationships between them.
4. **Keyboard contract.**
   Required keys, optional keys, and key behaviour by state.
5. **Focus lifecycle.**
   Focus entry, focus movement, focus exit, focus return, and behaviour on error or failure.
6. **Pointer, touch, and speech-input equivalence.**
   Every function reachable by keyboard must be reachable by the other modalities, and vice versa.
7. **Visible focus and forced-colours requirements.**
   What the focus indicator must look like, and what must survive a forced-colours theme.
8. **Reflow and two-dimensional exception behaviour.**
   How the component behaves at 320 CSS pixels and at 400 per cent zoom, and, where it claims the two-dimensional exception, the semantic argument for that claim rather than a visual one.
9. **WCAG criteria affected.**
   The specific success criteria the component is responsible for, by number.
10. **Test matrix and observed assistive-technology behaviour.**
    Engine, version, browser, observed behaviour, and test date.
11. **Deviations from the pattern, and why.**
    Every departure from the APG convention, with its reason and its cost, tagged as a product-specific deviation.
    An entry with no deviations records that explicitly, so silence is never ambiguous.
12. **Explicit non-guarantees and known uncertainty.**
    What the component does not promise, and what has not been verified.

This fits the project's existing rules directly.
A specification is incomplete without assertions, and components must state both guarantees and non-guarantees.
The APG-derived fields are that principle applied to a specific class of component.

## Native first, APG second

The most likely failure mode for a system that admires the APG is to turn every familiar interaction into an APG widget.
The primary rule should therefore be stated as a restriction rather than as an endorsement.

> Use native HTML when it provides the needed semantics and interaction.
> Adopt an APG pattern only when a genuinely custom composite widget is required.

The table below shows how that rule resolves for common product needs.

| Product need | Preferred system response | Why |
| --- | --- | --- |
| Reveal supplementary content | Native `<details>`, or a button with controlled content | Often avoids a full custom disclosure implementation |
| Action | Native `<button>` | Activation, focus, disabled state, and keyboard behaviour are already provided |
| Choice between options | Native radio or checkbox inputs | Avoids recreating form semantics from scratch |
| Navigation | Links inside landmarks | Do not convert site navigation into a menu widget |
| Modal confirmation | Dialog component following the APG dialog model | A genuine composite interaction with focus-management needs |
| Rich autocomplete | Combobox, only when native controls cannot satisfy the task | High complexity; semantics and keyboard interaction must be complete |
| Large interactive results table | Native table first; ARIA grid only where directional cell navigation is genuinely needed | A visual CSS grid is not a semantic grid and does not justify the Reflow exception |

The rows are ordered roughly from cheapest to most expensive.
The first four rows should account for the large majority of interactive surface in an audit and remediation platform.

### The grid row matters most to this project

The final row is the one this project must get right, because the product is a reporting and remediation tool full of tabular results.

The APG's [Grid pattern](https://www.w3.org/WAI/ARIA/apg/patterns/grid/) describes a composite widget with directional navigation using the arrow keys, Home, and End.
Its scope ranges from a grouped set of checkboxes through to a spreadsheet-like application.

It would be convenient to say that the grid is an interaction pattern for operating cells and not a way of presenting data, but the APG does not support that reading and the system must not rely on it.
The pattern is titled "Grid (Interactive Tabular Data and Layout Containers)" in the pattern index, and the APG states that uses of it "broadly fall into two categories: presenting tabular information (data grids) and grouping other widgets (layout grids)".
It says plainly that a grid "can be used to present tabular information that has column titles, row titles, or both", that the pattern "is particularly useful if the tabular information is editable or interactive", and it ships both data grid examples and an advanced data grid example with spreadsheet-like selection.
So the role is not disqualified merely because the content is data.

What separates a grid from a table is the keyboard model, and the APG supplies the usable test itself.
In a grid, "only one of the focusable elements contained by the grid is included in the page tab sequence" and the author must "provide code that manages focus movement inside it", whereas "all focusable elements contained in a table are included in the page tab sequence".
The decision is therefore a question about interaction cost, not about subject matter: does this report need cell-by-cell directional navigation, or does it need a shorter tab sequence through many in-cell controls?
For a static audit table whose cells hold at most one link each, the answer is no, and a semantic table is correct.
For a remediation surface with editable cells or several controls per row, the grid pattern becomes a defensible choice, and the tab-sequence argument is the reason to record.

Three different things share the word "grid", and the system must keep them apart.

- An **ARIA grid** is a composite widget, distinguished by its roving-focus keyboard model and its single tab stop rather than by the kind of content it holds.
- A **semantic table** is content structure, where meaning comes from header-to-cell relationships rather than from keyboard navigation.
- **CSS Grid** is a layout technique, and `display: grid` creates no accessibility semantics at all.

It follows that a tabular audit report should not automatically become an ARIA grid.
A native table is usually better where users need to read relationships rather than operate a spreadsheet-like interface.
Adopting a grid widget adds a substantial keyboard and assistive-technology contract, and it should be paid for by a demonstrated user need.

The consequence for WCAG is stated in the project's existing layout decisions and repeated here because it is easy to get wrong.
The [WCAG 1.4.10 Reflow](https://www.w3.org/TR/WCAG22/#reflow) two-dimensional exception rests on semantic two-dimensional structure.
A region that merely looks like a grid does not qualify.
A region arranged with the Grid layout primitive may never claim the exception.
Choosing an ARIA grid role in order to unlock the exception would be an abuse of both the role and the criterion.

## The keyboard contract model

The APG's central keyboard convention for composite widgets is that only one item in the composite is normally in the Tab sequence.
Once focus enters the composite, other keys move focus internally, and the APG strongly advises using key bindings familiar from common graphical user-interface systems.
This is usually implemented with a roving `tabindex` or with `aria-activedescendant`.

The system should make that a formal, recorded decision per component rather than an implicit implementation detail.
Every interactive component specifies eight things.

### 1. Entry

What receives focus when a user Tabs into the component?
For a composite, this is a single element, and the specification names it.
It should also say what happens on re-entry after the user has moved focus internally and then left.

### 2. Internal movement

Which keys move focus inside the component?
For example, the arrow keys, Home, End, Page Up, Page Down, or a type-ahead behaviour.
The specification states whether movement wraps at the ends, and whether the implementation uses roving `tabindex` or `aria-activedescendant`.

### 3. Activation

Which keys act on the currently focused item?
For example, Enter and Space for a button-like action.
The specification distinguishes keys that change selection from keys that commit an action, because conflating them causes accidental destructive operations.

### 4. Exit

Does Tab leave the component?
Does Escape dismiss it?
Where does focus go next in each case?
An exit path that depends on the user guessing is not a contract.

### 5. State change

What does a screen reader announce after expansion, selection, validation failure, loading, or deletion?
This is where most real-world composite widgets fail, because the visual state change is obvious and the programmatic one was never implemented.
The specification names the mechanism, such as a state property change or a live region, and the expected announcement.

### 6. Restoration

If a popup or dialog closes, where does focus return?
What happens if the invoking control no longer exists, for example because the action deleted the row that contained it?
The specification names a documented logical successor for that case.

### 7. Pointer and touch parity

Can all functionality be reached without hover, without drag, and without a path-dependent pointer movement?
Touch targets and pointer alternatives are part of the component contract, not a separate mobile concern.

### 8. Speech-recognition operation

Does every visible interactive control have a stable visible label that a speech-input user can say?
Where the accessible name differs from the visible label, the visible text must be contained in the accessible name.

Specifying these eight parts is what turns APG guidance into a system contract instead of a link in documentation.

## Why "keyboard" means more than a keyboard

The keyboard requirements cover far more than keyboard hardware, and the system's language should reflect that.

WCAG's glossary definition is narrow and mechanical: a keyboard interface is an "interface used by software to obtain keystroke input", per [the definition in WCAG 2.2](https://www.w3.org/TR/WCAG22/#dfn-keyboard-interface).
The breadth comes from what drives that interface, and that list belongs to [Understanding 2.1.1 Keyboard](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html) rather than to the definition: "Keyboard emulators include speech input software, sip-and-puff software, on-screen keyboards, scanning software and a variety of assistive technologies and alternate keyboards."
The attribution matters, because a reviewer who cites the definition for the emulator list is citing the wrong document and will lose the argument as soon as someone checks it.

The definition also carries an exclusion worth knowing.
Its second note records that operation "through a keyboard-operated mouse emulator, such as MouseKeys, does not qualify as operation through a keyboard interface", because the program is being driven through its pointing-device interface instead.
So MouseKeys support does not discharge a keyboard obligation, and a component exercised only that way is untested for this purpose.

A keyboard interface is an input pathway, not a physical device.
This is why keyboard operability is such a load-bearing requirement: it is the shared abstraction that many different assistive technologies drive.

Four consequences follow directly, and each should appear as a review check.

- **Avoid fine pointer paths.**
  An interaction requiring precise or continuous pointer movement excludes users of switch and scanning input, and often fails [WCAG 2.5.1 Pointer Gestures](https://www.w3.org/TR/WCAG22/#pointer-gestures).
- **Avoid hover-only discovery.**
  Content or controls revealed only on hover are unreachable to keyboard-interface users and unstable for magnifier users.
- **Avoid drag-only movement.**
  Any reordering or moving operation needs a single-pointer and keyboard-interface alternative, which is also the substance of [WCAG 2.5.7 Dragging Movements](https://www.w3.org/TR/WCAG22/#dragging-movements).
- **Avoid inaccessible custom shortcuts.**
  Single-character shortcuts collide with speech-recognition and screen-reader command sets.
  [WCAG 2.1.4 Character Key Shortcuts](https://www.w3.org/TR/WCAG22/#character-key-shortcuts) is Level A and is satisfied by any one of three escapes: a mechanism to turn the shortcut off, a mechanism to remap it to include one or more non-printable keys such as Ctrl or Alt, or the shortcut being active "only when that component has focus".
  The third escape is the one most often forgotten, and it is frequently the cheapest, because a component-scoped shortcut needs no global preference screen to be built.

The design-system implication is that a component's keyboard contract is simultaneously its switch-access contract, its scanning contract, and a large part of its speech-input contract.
Testing with a physical keyboard is necessary and is not sufficient.

## Worked example: the Dialog component

A dialog is an appropriate APG-derived component because native HTML alone does not settle all product decisions around initial focus, focus restoration, dismissibility, destructive confirmation, and assistive-technology behaviour.
The example below illustrates the shape, abridged: classification, native baseline, APG source, guarantees, non-guarantees, keyboard contract, and assertions.
It does not restate all twelve required fields, and a real registry entry would carry every one of them, including Reflow and two-dimensional exception behaviour and its recorded deviations.

The assertions section is deliberately presented as the required shape to be filled in.
No assistive-technology results are recorded here, because none have been gathered.
Under the project's existing rule, an assistive-technology claim without a test record is uncertainty, not a guarantee.

### Classification

APG-derived composite component.

### Native baseline

The native `<dialog>` element was considered.
System behaviour is specified independently because browser and assistive-technology support must be evidenced rather than assumed.
Using `<dialog>` as the implementation substrate remains open; specifying behaviour independently means the contract does not change if that choice changes.

### APG source

The [Dialog (Modal) pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) in the ARIA Authoring Practices Guide.

### Guarantees

- Has an accessible name.
- Conveys modal state when modal behaviour is used.
- Moves focus into an intentional initial target on open.
- Keeps keyboard focus within the modal interaction while open.
- Closes on Escape unless the task explicitly requires an alternative.
- Returns focus to the invoker, or a documented logical successor, on close.
- Preserves visible focus in default and forced-colours modes.

### Does not guarantee

- That modal behaviour is appropriate for a task.
- That destructive actions are reversible.
- That every browser and screen-reader pair announces the same dialog semantics without a recorded compatibility result.

The second item is a product concern that a component cannot solve.
The third is the honest limit of any markup contract.

### Keyboard contract

The table below states the required key behaviour.
Each row is a testable assertion, not a description of typical behaviour.

| Key | Behaviour |
| --- | --- |
| Tab | Moves to the next focusable element within the dialog |
| Shift+Tab | Moves to the preceding focusable element within the dialog |
| Escape | Closes the dialog, unless documented otherwise for a specific instance |
| Enter | Activates the focused control; it is not globally mapped to "confirm" |

The Enter row is the one most often got wrong.
Mapping Enter to the dialog's primary action regardless of which control has focus produces accidental confirmations, and it is especially dangerous in a remediation tool where a confirmation may apply a bulk change.
Enter acts on the focused control, and nothing else.

### Assertions

- No focusable element outside the dialog receives Tab focus while the dialog is open.
- Opening moves focus to the named initial target.
- Closing restores focus according to the restoration rule, including the successor case where the invoker no longer exists.
- The Escape result is tested with keyboard alone.
- Forced-colours mode retains surface boundaries and focus visibility.
- Results are recorded for NVDA with Firefox, JAWS with Chrome, VoiceOver with Safari, and TalkBack with Chrome, each with date and version.

The evidence table takes the following form.
It is presented empty because the testing has not been done, and inventing entries would defeat the purpose of the record.

| Screen reader | Browser | Version | Observed behaviour | Date |
| --- | --- | --- | --- | --- |
| NVDA | Firefox | To be recorded | To be recorded | To be recorded |
| JAWS | Chrome | To be recorded | To be recorded | To be recorded |
| VoiceOver | Safari | To be recorded | To be recorded | To be recorded |
| TalkBack | Chrome | To be recorded | To be recorded | To be recorded |

The important structural point is that the APG reference is only one field among many.
The shipped component is governed by its system-level contract and its evidence, not by the guide it was derived from.

## APG examples are reference implementations

The APG provides patterns and functional examples.
The examples are pedagogical reference implementations, not production components.
They are written to be readable and to demonstrate a pattern clearly, which is a different goal from being maintainable, framework-appropriate, performant, and covered by a regression suite.

A production design system should therefore be explicit about what it takes and what it owns.

| Borrowed from the APG | Owned and tested by the system |
| --- | --- |
| Interaction intent and user-facing behaviour | Platform architecture and code style |
| Semantic model: roles, states, properties, relationships | The exact version that ships, and its tests |
| Keyboard model and conventional key bindings | Assistive-technology evidence by engine, version, and date |
| Naming and relationship expectations | Product decisions such as dismissibility and destructive confirmation |
| Awareness of the support caveats the pattern notes | Recorded deviations, non-guarantees, and uncertainty |

Six practices follow.

1. Borrow the interaction intent, semantics, and keyboard model.
2. Use the platform architecture and code style appropriate to this project.
3. Test the exact version that ships, not the version the example shipped.
4. Avoid inheriting unnecessary complexity from the example.
5. Record deliberate deviations from the APG, with reasoning.
6. Reassess an APG pattern when browser or assistive-technology support changes.

The last practice needs a trigger.
Support changes are the main reason a settled component contract becomes wrong, so a support change should reopen the specification rather than being noticed by accident.

## Five kinds of requirement

Because APG guidance is informative, the system must not present it as conformance law.
Following a specific APG key binding is generally good interoperability practice.
WCAG, however, usually evaluates outcomes such as keyboard operability rather than requiring a particular key map.

A tabs widget may remain WCAG-conformant with a different keyboard interaction model, provided it is fully keyboard operable and its state is correctly conveyed.
That is a real fact about conformance, and it is not permission to deviate freely.
Departing from an established convention adds discoverability risk for users who already know the convention, and support risk for the team that must document and defend the difference.
The correct handling is to allow the deviation, label it, and state its cost.

The system's documentation should therefore distinguish five categories, and every requirement in a component specification should be tagged with one.

| Category | What it means | If it is not met |
| --- | --- | --- |
| Required by WCAG or ARIA | A normative requirement from a W3C standard | A conformance failure |
| Strongly recommended by APG | An interoperable convention users are likely to expect | A usability and discoverability risk, not a conformance failure |
| Project convention | A choice this system has made for internal consistency | An inconsistency to be reconciled or documented |
| Product-specific deviation | A deliberate, recorded departure for a product reason | Nothing, provided the record and its reasoning exist |
| Known support limitation | A gap in browser or assistive-technology behaviour | Uncertainty to be disclosed, not a claim to be made |

Tagging prevents two opposite failures.
It stops documentation from falsely presenting all APG guidance as mandatory conformance law, which erodes trust when someone checks.
It also stops teams from dismissing APG conventions as merely optional, which is how widgets end up technically conformant and practically unusable.

## Design-tool annotation requirements

APG adoption should shape the design-to-engineering handoff as well as the code.
For every APG-derived pattern, the system should provide an annotation preset in Figma or an equivalent tool, exposing the information a visual mock-up cannot convey.

The preset should carry the following fields.

| Annotation field | What it records |
| --- | --- |
| Pattern identity | For example, "APG Dialog (Modal)" or "APG Combobox" |
| Semantic model | Native element and any ARIA roles |
| Accessible name source | Where the name comes from, and whether visible text is contained in it |
| Relationship model | `aria-controls`, `aria-expanded`, `aria-labelledby`, `aria-describedby`, and error-message relationships where relevant |
| Focus order and initial focus | Reading and focus sequence, and the initial focus target |
| Internal keyboard navigation | Which keys move focus inside the component |
| Close and restore-focus behaviour | How the component is dismissed and where focus returns |
| Hidden versus removed from the DOM | Whether content is hidden, made inert, or removed entirely |
| Required visible states | Focus is mandatory; hover is optional |
| Responsive and Reflow behaviour | How the component behaves at narrow widths and high zoom |
| Assistive-technology uncertainty marker | Behaviour known to vary or not yet verified |

The relationship model deserves emphasis because it is invisible in a mock-up and expensive to reverse-engineer later.
A designer who has decided that a control expands a panel has implicitly decided that `aria-expanded` and `aria-controls` apply, and recording that is cheaper than discovering it in an audit.

The project's existing annotation economy rule still applies.
Do not annotate what the coded component already guarantees.
The annotation should identify the selected component and any product-level choices or deviations, not restate every behaviour already baked into the component and its tests.
Restating guaranteed behaviour makes annotations long, makes them drift from the code, and trains reviewers to skim them.

## The five-level testing model

APG support should be verified at five levels.
Each level catches a class of defect the others miss, so they are not substitutes for one another.

| Level | What to test | Example |
| --- | --- | --- |
| Static semantics | Native element choice, role validity, accessible name, state, relationships | The dialog has a name; the disclosure uses the correct control relationship |
| Keyboard contract | Entry, internal navigation, activation, exit, restoration | Tab enters a composite once; arrows move within it; Escape closes the dialog |
| Visual and layout | Focus visibility, forced colours, 400% zoom, text spacing, Reflow | The focus ring remains visible; the dialog does not trap overflowed content |
| Assistive technology | Actual browser and assistive-technology behaviour, by version and date | The screen reader announces the state change and focus movement as expected |
| Composition in a realistic page | Behaviour among landmarks, headings, and realistic content | Opening a dialog does not create duplicate landmarks or leave focus obscured under page chrome |

The first three levels are largely automatable or scriptable, and should run on every change.
The fourth is manual, slow, and produces results that expire, which is why it is recorded with a date rather than treated as a permanent property.
The fifth is the level most often skipped, and it is where component-level correctness turns into page-level failure.

## Initial approved catalogue

For an accessibility testing and remediation platform, the system should not begin by implementing every APG pattern.
It should start with the smallest catalogue that supports the product, ordered by priority.

| Priority | Pattern or primitive | Why it matters |
| --- | --- | --- |
| 1 | Native Button, Link, Checkbox, Radio, Text Input, Select | Most actions, filters, and configuration controls |
| 2 | Disclosure | Show and hide issue details, advanced filters, and evidence panels |
| 3 | Dialog | Confirmation, configuration, and remediation guidance |
| 4 | Alert and status messaging | Scan progress, completed checks, and error summaries |
| 5 | Native table plus a scoped scroll container | Audit results, with the semantic Reflow exception correctly scoped |
| 6 | Tabs, only where persistent peer views genuinely improve a task | Avoid using tabs merely to compress a page |
| 7 | Combobox, only where searching a large controlled vocabulary is necessary | High complexity and high regression risk |
| 8 | Tree, Treegrid, or ARIA Grid, only after user research demonstrates the need | Complex keyboard and assistive-technology contract; do not adopt for visual density |

The ordering is deliberate.
Priorities 1 to 5 cover the product's core work and consist almost entirely of native elements and one simple composite.
Priorities 6 to 8 are gated on demonstrated need, and each gate should be recorded when it is passed.

### Caution: avoid menu and menubar for ordinary navigation or action lists

Two cautions are strong enough to belong in the catalogue itself, and this is the first.

The APG's [Menu and Menubar pattern](https://www.w3.org/WAI/ARIA/apg/patterns/menubar/) describes a widget that "offers a list of choices to the user, such as a set of actions or functions", behaving "like native operating system menus", and notes that "a menu that is visually persistent is a menubar".

Accuracy about its scope first, because the temptation is to overstate the case.
The APG does not restrict this pattern to application menus.
It ships a Navigation Menubar Example, described as demonstrating "a menubar that provides site navigation".
Using a menubar for site navigation is therefore a sanctioned use of the pattern, not a misuse of it, and this document must not claim otherwise.

The caution stands as a project convention with a stated cost, which is the honest form for it.
Adopting menubar for ordinary navigation imports the entire composite contract: a roving-focus model, a single tab stop, author-managed arrow-key movement, submenu open and close behaviour, and a role that makes a screen reader describe the thing as a menu rather than as navigation.
For this product I judge that cost unjustified, because a list of links inside a navigation landmark already gives users a structure they know and costs nothing to maintain.
A list of buttons is usually just an action group, and a toolbar is the cheaper composite where one is genuinely warranted.
If a future surface does adopt menubar, the justification belongs in its specification, tagged as a product-specific deviation from this convention, with the keyboard contract written out in full.

### Caution: do not adopt ARIA Grid for visual density

A grid widget is justified by a need for directional cell navigation, not by a table looking crowded or by a desire to avoid reflowing content.
If the underlying need is that a wide table is hard to use at high zoom, the answer is a scoped scroll container and a correctly justified two-dimensional exception, not a role change.

## The adopted decision

This note originally ended with a proposed colophon decision, marked as not yet adopted, arguing that APG patterns should be adopted by reference rather than copied and that native HTML should be preferred.
That position is now adopted, as the colophon decision "Native HTML first, and published patterns by reference" in [COLOPHON.md](COLOPHON.md).
This project claims the `afds-patterns-native-first` profile in the packages it publishes.

The proposed text is withdrawn rather than moved, because it had gone stale in two ways that the specification work exposed.
It described twelve recorded fields as an obligation of the pattern policy, when eight core clauses turned out to own them, so those fields bind every package and not only one that prefers native elements.
It also used the status names `APG-derived` and `APG-adjacent`, which became `pattern-derived` and `pattern-adjacent` when the vocabulary moved into the core, since the core may not name one external pattern library.
Its verification criteria survive in the specification, distributed across the clauses that own them, and its account of the reasoning survives in the adopted decision.

## Open questions raised

The following items follow from this note and are candidates for [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md).
Each is stated with what would count as settling it.

### Which APG patterns enter the approved catalogue, and on what evidence?

The proposed catalogue lists eight priorities, three of which are gated on demonstrated need.
**To settle:** what evidence passes the gate for Tabs, Combobox, and Tree or Treegrid, and who decides.

### What is the minimum assistive-technology test matrix for an APG-derived component?

The Dialog example names four screen-reader and browser pairs.
**To settle:** whether four pairs is the standing minimum, whether speech recognition and switch access are separate rows, and how often results must be refreshed before they are treated as expired.

### How are deviations from APG conventions recorded and reviewed?

The five requirement categories distinguish a product-specific deviation from a project convention, but there is no process attached.
**To settle:** where deviations live, whether they need sign-off, and how a user-facing discoverability cost is assessed.

### Does the system implement components or only specify them?

This question is already open in general terms, and APG-derived composites sharpen it.
**To settle:** whether the project ships a tested Dialog implementation, or a specification plus assertions that adopters implement.

### What is the reassessment trigger for a support-dependent pattern?

A pattern should be reassessed when browser or assistive-technology support changes.
**To settle:** what sources are monitored, and what change is large enough to reopen a settled component contract.

### How does the annotation economy rule apply to APG-derived components?

The rule says not to annotate what the coded component guarantees, which presumes the reader knows what it guarantees.
**To settle:** how an annotation references a component version so that its guarantees are unambiguous.

### Is there a native-first exit criterion for the Dialog substrate?

Whether the implementation uses the native `<dialog>` element is currently open.
**To settle:** what support evidence would make `<dialog>` the required substrate rather than one option.

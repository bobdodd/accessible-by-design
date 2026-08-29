<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# Colophon

This document records how *Accessible by Design* is built and, more importantly, **why each decision was made**.
It is a first-class project artefact rather than an afterthought.

A project whose subject is accessible design must be able to show its own work.
Anyone should be able to understand each consequential choice, see the trade-offs accepted, and disagree with them in the open.
Where a decision turns out to be wrong, the record says so and says what replaced it.

## How to read an entry

Every decision uses the same shape.

| Part | Purpose |
| --- | --- |
| **Decision** | What was chosen, stated plainly |
| **Reasoning** | Who it benefits and by what mechanism |
| **Cost** | What was given up, stated honestly |
| **Rejected** | Alternatives considered and why they lost |
| **Verification** | How the decision is tested |

An entry without a stated cost is incomplete.
Every choice trades something away, and a decision record that claims otherwise is advocacy rather than documentation.

## Status

| Field | Value |
| --- | --- |
| Phase | Research and planning |
| Last reviewed | 2026-08-29 |
| Implementation | Deferred until research decisions are settled |
| Documentation licence | CC BY-SA 4.0 |

## Method decisions

### The design system is the unit of accessibility

**Decision.** Accessibility requirements attach to components and patterns, not to pages or individual audit findings.

**Reasoning.** Page-level auditing produces long lists of isolated violations with no shared vocabulary, so the same defect reappears in the next release.
Attaching requirements to components lets a fix propagate to every instance and makes the reason for the fix travel with it.
Design systems were the most frequently cited accessibility strategy in practitioner interviews, rising from 33% in 2017 to 52% in 2019-2020.

**Cost.** Projects without a design system cannot adopt the method directly.
They must first identify their de facto components.

**Rejected.** Page-by-page remediation, because it treats symptoms rather than recurrence.
Automated site-wide scanning alone, because it finds only the machine-detectable subset.

**Verification.** Each component specification carries conformance assertions.
Coverage is measured against the component inventory rather than page count.

**Note.** A design system does not immediately make a service accessible.
It manages some UI resources and modalities; it cannot replace testing, user research, or judgement in context.

### Accessibility is a crosscutting concern, split two ways

**Decision.** Requirements are classified into *user technology support* (assistive-technology compatibility: roles, names, states, focus, keyboard) and *user layout support* (presentation: reflow, measure, spacing, contrast).

**Reasoning.** Accessibility spans multiple components rather than living in one module.
The split prevents semantic guarantees and geometric guarantees from being conflated.

**Cost.** Some criteria straddle the boundary and must be assigned deliberately.

**Rejected.** A flat list of WCAG criteria per component, which obscures whether a failure is geometric or semantic.

**Verification.** Every component criterion names its branch.

**Note.** The boundary is not always where it appears.
The WCAG 1.4.10 two-dimensional exception looks like a layout question but is decided by whether a user needs a two-dimensional semantic relationship to understand content.
Classification follows what carries meaning, not what produces appearance.

### Every specification is testable by construction

**Decision.** A component specification is incomplete until it carries the assertions or manual procedure needed to verify it.

**Reasoning.** When tests are authored separately from specifications, the two drift and the specification becomes aspirational.

**Cost.** Specifications take longer to write.
Some requirements need slower manual or assistive-technology testing.

**Rejected.** Prose-only specifications with tests added later.

**Verification.** Review rejects a specification without assertions or a manual procedure.

### Components declare non-guarantees

**Decision.** Every specification declares what it does not guarantee alongside what it does.

**Reasoning.** A layout primitive that silently omits semantics invites a developer to assume semantics were handled.
For example, Stack provides vertical rhythm, not list semantics; Imposter provides overlay geometry, not focus trapping, `aria-modal`, or focus return.

**Cost.** Specifications are longer and require judgement about material omissions.

**Rejected.** Guarantees-only documentation.

**Verification.** Review rejects an empty non-guarantees section.

### Conformance is measured at two levels

**Decision.** Components are tested in isolation and inside a realistic page with landmarks, header, footer, and realistic content.

**Reasoning.** A component passing in isolation can still create a broken heading sequence, duplicated landmark, or unreachable focus target in context.

**Cost.** Fixtures must be maintained, and composition failures are harder to attribute.

**Rejected.** Component-only testing.

**Verification.** Every component has an isolated test and an in-page test.

### AT contracts are only as real as engine support

**Decision.** Claims depending on assistive-technology behaviour identify the engine, version, browser, observed behaviour, and test date.

**Reasoning.** A markup contract that no shipping screen reader honours delivers nothing, however correct it is against a specification.
Support diverges across engines and browsers.

**Cost.** Testing across NVDA, JAWS, VoiceOver, TalkBack, and speech recognition is slow and results expire.

**Rejected.** Treating specification conformance alone as evidence of user experience.

**Verification.** AT-dependent claims without a test record are recorded as uncertainty, not guarantees.

### Uncertainty is a first-class record type

**Decision.** Unknown or unverified assistive-technology behaviour is recorded rather than resolved by assumption.

**Reasoning.** Giving unknowns a home prevents them being silently settled as "probably fine".

**Cost.** Documentation displays its own gaps.

**Rejected.** Omitting unknowns.

**Verification.** An AT-dependent claim without evidence moves to the uncertainty field.

## Layout decisions

Full method: [LAYOUT-METHOD.md](LAYOUT-METHOD.md).

### The layout system is intrinsic, not breakpoint-driven

**Decision.** Applications use raw HTML, CSS, and JavaScript in Electron shells, with Every Layout-style composable primitives: Stack, Box, Center, Cluster, Sidebar, Switcher, Cover, Grid, Frame, Reel, Imposter, Icon, and Container.
Primitives are native custom elements without Shadow DOM.
No layout media queries are used.

**Reasoning.** Breakpoints encode guesses about user conditions.
Intrinsic primitives respond to available space whether its cause is a small window, 400% zoom, OS font scaling, or narrow nesting.
A `rem`-anchored scale and `ch` measure let user font-size changes propagate through the interface.
Flexbox-based composition is sufficient technique C31 for SC 1.4.10 Reflow.

**Cost.** Contributors must learn composition-first CSS.
Debugging nested primitives can be difficult.
No Shadow DOM permits global styles to leak in, which is the price of allowing inherited and user styles in.

**Rejected.** Breakpoint-prefixed utility systems, component frameworks that make layout depend on JavaScript, Shadow DOM encapsulation, and fixed desktop-style Electron layouts.

**Verification.** No author-fixed dimensions except hairline borders; no layout media queries; no fixed heights.
Each primitive is tested at 400% zoom, in forced colours, with doubled root font size, and with text-spacing overrides.
Layout remains complete with JavaScript disabled.

### The measure axiom

**Decision.** The measure never exceeds 60ch, applied exception-based: cap content broadly, then name deliberate container exceptions.

**Reasoning.** Users with dyslexia, low vision, or attention-related disabilities can lose their place on over-long lines.
`ch` follows the font's character width as font size changes; a pixel width cannot guarantee a character measure.

**Cost.** The cap is blunt and needs a maintained exception list.
Different font sizes occupy different proportions of a wide container.

**Rejected.** A manually applied `.measure` utility and pixel `max-width` values.

**Verification.** Text `max-inline-size` is `var(--measure)` or a documented exception.

### Typography follows the same scale as spacing

**Decision.** Font sizes and spacing use one modular scale, rooted at `1rem`; body text uses `line-height: 1.5`; the largest and smallest text on one surface differ by no more than 3:1.

**Reasoning.** One line of text is the natural denominator for vertical rhythm.
The shared seed makes user text-size changes affect both type and space.
The 3:1 cap means screen-magnifier users need not continually adjust zoom between headings and body copy.

**Cost.** Available sizes are few and widely separated.
Display typography is constrained.

**Rejected.** Independently chosen type and spacing values.

**Verification.** Font-size declarations reference scale properties; literal values fail review.

### What the “no px” rule actually prohibits

**Decision.** No author-fixed dimensions in project stylesheets except hairline borders.
Use `rem`, `ch`, `em`, `cap`, or percentages.

**Reasoning.** The rule prohibits values frozen against user font-size and zoom settings.
A `rem`-anchored scale moves with those settings.

**Cost.** Contributors must use the scale rather than arbitrary literals.

**Rejected.** Permitting pixels for supposedly small values.

**Verification.** Literal author-fixed dimensions fail review except documented hairline borders.

**Note.** Earlier drafts treated the CSS pixel as inherently unprincipled.
That was overstated.
A CSS pixel is an angular reference measurement; the problem here is author-fixed sizing, not the unit's design.

### Box shape survives forced colours

**Decision.** Every delineated surface has a transparent outline with negative offset in addition to any background colour.

**Reasoning.** Forced-colours themes may eliminate backgrounds.
The transparent outline is normally invisible, costs no layout space, and becomes visible when forced-colours assigns a system colour.

**Cost.** Extra declarations and loss of `outline` for unrelated surface decoration.

**Rejected.** Background colour alone.

**Verification.** Every delineated surface is inspected in forced-colours mode.

### Data tables claim the two-dimensional exception explicitly

**Decision.** A region may claim the WCAG 1.4.10 two-dimensional exception only by naming the meaning-bearing axes and explaining how a cell's significance depends on both.
Every individual cell and all surrounding content are tested as ordinary reflowing content.

**Reasoning.** The exception rests on semantic two-dimensional structure, not visual layout.
Data tables qualify because of relationships between row and column headers and their cells.
The parenthetical “not individual cells” marks where that semantic relationship stops.
Headings, introductory prose, search fields, and pagination around the table are not excepted.

**Cost.** One view can contain two conformance regimes.
Specification authors must justify claims rather than inherit a blanket allowance.

**Rejected.** Treating the entire reporting view as excepted, forcing genuine tables into one column, or granting an exception because content merely looks like a grid.

**Verification.** Each cell wraps at 320 CSS pixels or provides a reveal mechanism.
The specification identifies the excepted region and meaning-bearing axes.

**Note.** Earlier research wrongly treated wide tables at 400% zoom as a weakness of the layout method.
Tables with genuine header-to-cell relationships are excepted.
A second earlier draft said the exception “covers grid-based UI generally.”
That was unsound: cells are semantic content; CSS Grid is a layout technique.

### No Grid-primitive region claims the exception

**Decision.** A region arranged with the Grid primitive may never claim the WCAG 1.4.10 two-dimensional exception.

**Reasoning.** The primitive wraps self-contained items without cross-axis semantic relationships.
`display: grid` creates no header-to-cell relationship.
A region requiring the exception needs semantic table or ARIA-grid structure first.

**Cost.** Card collections and dashboards must reflow, potentially adding vertical scrolling.

**Rejected.** Allowing an exception based on visual arrangement.

**Verification.** An exception-claiming component cannot use the Grid primitive for the excepted region.

### Two-dimensional scrolling is scoped to its container

**Decision.** A region requiring two-dimensional scrolling owns its scroll container.
Page-level horizontal scrolling is not permitted.

**Reasoning.** Scoping keeps surrounding content reflowing and avoids a page-level scrollbar that makes users search for nonexistent off-screen content.

**Cost.** Nested scroll containers add keyboard and input-method testing requirements.

**Rejected.** Letting a wide table force the entire page to scroll in two dimensions.

**Verification.** No page-level horizontal scrollbar appears; scoped containers are keyboard-reachable.

### Sticky positioning is deferred

**Decision.** No `position: sticky` or `position: fixed` is used until a container-driven equivalent exists.

**Reasoning.** Fixed content can obscure focused elements and reduce reading space at zoom.
The standard advisory remedy uses media queries, which the method forbids for layout.

**Cost.** Toolbars and filters scroll out of view on long results lists.

**Rejected.** An undocumented exception to the no-layout-media-query axiom, and sticky positioning without an un-sticking mechanism.

**Verification.** Stylesheet review rejects sticky and fixed positioning.

## Documentation decisions

### Markdown, one sentence per line

**Decision.** Prose is authored in Markdown with one sentence per line.

**Reasoning.** Diffs become sentence-level.

**Cost.** Raw source is unfamiliar to some contributors.

**Rejected.** Hard-wrapping prose at a fixed column.

### Real heading structure

**Decision.** Headings use Markdown heading syntax in strict order; bold text never imitates headings.

**Reasoning.** Screen-reader users navigate documents by heading.

**Cost.** None of consequence.

**Verification.** Review checks heading order and skipped levels.

### Tables have header rows and read linearly

**Decision.** Tables have header rows and no merged cells or nested tables.

**Reasoning.** Regular tables preserve header associations for screen readers.

**Cost.** Complex information may need several simple tables or prose.

**Rejected.** Layout tables and merged-cell summaries.

### Diagrams are described in prose

**Decision.** No diagram carries meaning absent from surrounding text.

**Reasoning.** A complex structural argument needs navigable prose, not only a long text alternative.

**Cost.** Duplication and more writing.

**Rejected.** Detailed `alt` text as the sole alternative.

### Colour never carries meaning alone

**Decision.** Status and severity use text or shape, with colour only as reinforcement.

**Reasoning.** Colour-only encoding fails for colour-vision differences and forced-colours modes.

**Cost.** Interfaces can look plainer.

**Rejected.** Unlabelled red/amber/green severity coding.

## Repository decisions

### Per-file licence headers

**Decision.** Documentation files carry SPDX identifiers and copyright lines.

**Reasoning.** A file retains an unambiguous licence when copied from the repository.

**Cost.** Two lines of boilerplate per file.

## Not yet decided

[OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) is the single source of truth for the research agenda.
The directly relevant unresolved items are the colour system, the conformance target, token authoring, contrast-as-relationship, and a container-driven alternative to sticky positioning.

## Rendering contract

This file is intended to be parseable by project tools.

- `##` marks a category and `###` marks a decision.
- Bold run-in labels delimit decision fields.
- Field order is Decision, Reasoning, Cost, Rejected, Verification, Note.
- A renderer preserves heading hierarchy and does not replace labels with colour-only badges.
- A renderer keeps Cost and Rejected visible by default.
- Superseded reasoning remains in Note fields rather than being silently deleted.

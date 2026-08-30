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
| Code licence | GPL-3.0-only |
| Base representation | AFDS draft specification 1.0.0 (project draft, not a standard) |

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

## Portable representation decisions

### AFDS uses a portable bundle, not a monolithic format

**Decision.** The project adopts the Accessibility Focused Design System (AFDS) draft specification, version 1.0.0, as the base representation for its work.
AFDS is a portable design-system bundle rather than one universal file format.
It composes specialised representations: DTCG Design Tokens JSON for token values; Markdown plus a structured component specification for component contracts; Custom Elements Manifest where Web Components are published; Storybook Component Story Format where executable stories are used; structured evidence records for assistive-technology results and known limitations; and explicit adapters for Figma, Penpot, CSS, Electron, and other targets.

**Reasoning.** No current standard represents a complete design system.
DTCG is the stable portable representation for named design-token values, but it does not carry component semantics, keyboard interaction, focus lifecycle, Reflow assertions, WCAG mapping, assistive-technology evidence, non-guarantees, or uncertainty.
Custom Elements Manifest describes a Web Component public API but not the full accessibility contract.
Component Story Format provides executable examples and fixtures but not semantic source of truth.
Using a bundle assigns each kind of fact to the representation able to carry it, while an AFDS manifest connects the sources without duplicating them.

This is particularly necessary for an accessibility-focused system.
Accessibility meaning must remain portable beyond a proprietary design tool: semantic structure, user-preference response, keyboard and focus behaviour, actual engine-qualified evidence, non-guarantees, and uncertainty all travel as first-class records.

**Cost.** The system has several artefact types and requires identifiers, schema validation, versioning, adapter maintenance, and cross-reference discipline.
Contributors cannot treat a single Figma file, token file, story, or generated API manifest as the entire system.
Some properties cannot transfer losslessly across platforms; adapters must report adaptations and unsupported features rather than silently flattening them.

**Rejected.** A proprietary design tool as the sole source of truth, because it locks essential rationale and accessibility meaning into a vendor document model.
Tokens alone as the design system, because values do not convey semantics or behaviour.
A single universal component JSON created by this project, because mature interoperability concerns are divided across specialised formats and active W3C work is still evolving.
Storing core accessibility contracts exclusively in DTCG `$extensions`, because DTCG extensions are optional metadata and should not be necessary to understand the token value.

**Verification.** Each AFDS release has a validated manifest that identifies canonical token, component, evidence, documentation, and adapter sources.
Canonical token files validate against the declared DTCG version.
Each approved component has a stable identifier, human-readable and machine-readable specifications, WCAG mapping, keyboard and focus contract, non-guarantees, uncertainty, realistic-page test, and evidence record.
Every transform emits a report containing mappings, warnings, losses, unsupported features, and validation status.
No adapter becomes the only source for a fact owned by a canonical artefact.

**Note.** AFDS 1.0.0 is a project draft, not a W3C standard.
The project will monitor and seek alignment with the W3C UI Specification Schema Community Group, the Design System Documentation Community Group, Open UI, and future DTCG work.
The AFDS component-spec and evidence formats are provisional and are intended to be mapped to, or contributed as requirements for, those efforts rather than become isolated terminology.
The supporting research is recorded in [the portable representations research note](../research/PORTABLE-REPRESENTATIONS.md).

### AFDS bundles are distributed as a single `.afds` package

**Decision.** An Accessibility Focused Design System bundle is distributed as one ZIP-based file with the `.afds` extension.
An AFDS package contains the complete declared hierarchy of canonical design tokens, component specifications, evidence, documentation, schemas, optional stories, and optional adapters.
It has no enclosing directory and MUST include root `afds-manifest.json` and `afds-inventory.json` files.

**Reasoning.** A loose hierarchy is portable in theory but cumbersome in practice: files are lost in transfer, relationships become ambiguous, integrity is difficult to verify, and consumers cannot reliably tell which folder or revision is the complete bundle.
A single ZIP container is widely supported, cross-platform, compressible, and inspectable with ordinary tools.
It keeps specialised open representations, namely DTCG JSON, Custom Elements Manifest, Component Story Format, Markdown, structured evidence, and adapters, together without claiming that they are one format.

The manifest identifies the package, version, canonical sources, conformance profiles, evidence locations, licences, and adapters.
The inventory lists every entry with its relative path, media type, byte length, role, and SHA-256 digest, so a consumer can verify transfer integrity before relying on content.
This makes the accessibility contract portable as a whole rather than scattering it between a design-tool file, a token repository, a component package, and an untracked test report.

**Cost.** A package is less convenient for line-by-line collaboration than a live repository and requires unpacking or package-aware tooling to edit individual artefacts.
ZIP inventories verify integrity but do not provide identity or authenticity; a future signature mechanism is needed for trusted distribution.
Consumers must defend against ZIP path traversal and decompression attacks.
A package format also requires schema, manifest, inventory, versioning, and adapter-maintenance discipline.

**Rejected.** Loose folders as the distribution format, because they are easy to partially copy, lose, or misidentify.
A proprietary design-tool export, because it cannot be the only carrier of accessibility semantics, evidence, non-guarantees, or uncertainty.
A monolithic custom component format, because the system composes specialised representations better served by DTCG, Custom Elements Manifest, Component Story Format, Markdown, and structured evidence.
Open Packaging Conventions, because its XML parts and relationship model add complexity without improving the project's JSON and Markdown centred representation; AFDS uses the simpler ZIP container approach while borrowing the useful principle that a package is one logical object containing related parts.

**Verification.** A conforming `.afds` package is a valid ZIP archive with no absolute or traversal paths, no encrypted entries, a root manifest, and a root inventory.
The inventory is validated before use: each entry's path, length, and SHA-256 digest must match.
The manifest identifies every canonical source and no adapter is the only source of core accessibility meaning.
Transforms emit mapping, warning, loss, and unsupported-feature reports.
The package passes configured limits for entry count, compressed and uncompressed size, nesting, and path length.

**Note.** The underlying registered media type is `application/zip` until AFDS has a dedicated IANA registration.
The `.afds` extension and root manifest identify the format in the interim.
AFDS 1.0.0 inventory integrity is not a digital signature and does not prove author identity or trusted provenance.
The container is specified in full in [the AFDS package format document](AFDS-PACKAGE-FORMAT.md).

## Repository decisions

### Per-file licence headers

**Decision.** Documentation files carry SPDX identifiers and copyright lines.

**Reasoning.** A file retains an unambiguous licence when copied from the repository.

**Cost.** Two lines of boilerplate per file.

### Code and documentation are licensed separately

**Decision.** Code is licensed GPL-3.0-only and documentation is licensed CC BY-SA 4.0.
The full texts sit at the repository root as `LICENSE` and `LICENSE-DOCS` respectively.

**Reasoning.** The two bodies of work have different reuse needs.
Copyleft on tooling keeps derived accessibility tooling open, while a Creative Commons licence lets the written method circulate in documentation, standards discussion, and teaching material where a software licence would be a poor fit.
CC BY-SA 4.0 also matches the licence used by Wikipedia and much WCAG-adjacent community documentation, so material can flow both ways.

**Cost.** A licence boundary now runs through the repository and has to stay disciplined.
CC BY-SA 4.0 is only one-way compatible with GPLv3, so prose may be absorbed into GPL works but GPL code may not be relicensed as CC BY-SA.
A code sample that appears in both a document and a shipped tool has to be marked explicitly rather than inheriting its surrounding file's licence.

**Rejected.** A single licence covering everything, which is simpler but either puts a software licence on prose or puts a documentation licence on code that needs source-provision and patent terms.
The bare `GPL-3.0` SPDX identifier, which was deprecated in SPDX License List 3.0.
`GPL-3.0-or-later`, because the decision was to stay strict and locked to version 3.

**Verification.** Every file carries an SPDX identifier matching its directory's licence.
The two licence texts are the unmodified upstream texts.
Contribution terms are stated in [the contributing guide](../CONTRIBUTING.md), and opening a pull request constitutes agreement without a separate contributor licence agreement.

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

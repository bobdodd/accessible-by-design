<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# Colophon

This document records how *Accessible by Design* is built and, more importantly,
**why each decision was made**. It is a first-class artefact of the project rather
than an afterthought.

A project whose subject is accessible design has to be able to show its own work.
Anyone should be able to read this file, understand every choice that shapes the
experience, see the trade-offs that were accepted, and disagree with them in the open.
Where a decision turned out to be wrong, the record says so and says what replaced it.

**Machine-readable source of truth.** This file is intended to be parsed and rendered
inside the applications the project produces, so each decision follows a fixed
structure. See *Rendering contract* at the end for the schema.

---

## How to read a decision entry

Every decision below uses the same five-part shape. Nothing is recorded as a bare
assertion.

| Part | Purpose |
| --- | --- |
| **Decision** | What was chosen, stated plainly |
| **Reasoning** | Who it benefits and by what mechanism |
| **Cost** | What was given up, stated honestly |
| **Rejected** | The alternatives considered and why they lost |
| **Verification** | How the decision is tested, and against which criteria |

An entry without a stated cost is treated as incomplete. Every choice trades something
away, and a decision record that claims otherwise is advocacy rather than
documentation.

---

## Status of this document

| Field | Value |
| --- | --- |
| Phase | Research and planning |
| Decisions recorded | Method, documentation, licensing, repository, layout |
| Implementation decisions | Deferred until tooling begins |
| Last reviewed | 2026-08-29 |
| Licence | CC BY-SA 4.0 |

The project currently has no running code. Stack, colour, and tooling sections are
stubbed under *Not yet decided* and kept visible rather than hidden, so the gaps are
legible.

---

## Method decisions

### The design system is the unit of accessibility

**Decision.** Accessibility requirements attach to components and patterns, not to
pages or to individual audit findings.

**Reasoning.** Page-level auditing produces long lists of individual violations with no
shared vocabulary, so the same defect reappears in the next release. Attaching the
requirement to the component means a fix propagates to every instance, and the reason
for the fix travels with it. This is also the strategy with the strongest survey
support: design systems were the most frequently cited accessibility strategy among
practitioners, rising from 33% of interviews in 2017 to 52% in 2019-2020, against 31%
for usability testing with disabled people and 17% for audits.

**Cost.** Projects without a design system cannot adopt the method directly. They must
first identify their de facto components, which is real work the method does not
remove.

**Rejected.** Page-by-page remediation, because it treats symptoms and does not prevent
recurrence. Automated site-wide scanning alone, because it finds only the
machine-detectable subset and reports it without structure.

**Verification.** Each component specification carries its own conformance assertions.
Coverage is measured against the component inventory rather than against page count.

**Note.** The method's ceiling is conceded openly, following the GOV.UK Design System's
own statement that using a design system does not immediately make a service
accessible. A design system manages the available UI resources and modalities; it
cannot determine the equilibrium on its own.

### Accessibility is a crosscutting concern, split two ways

**Decision.** Requirements are classified into *user technology support*
(assistive-technology compatibility: roles, names, states, focus, keyboard) and *user
layout support* (presentation: reflow, measure, spacing, contrast).

**Reasoning.** Accessibility spans multiple components rather than living in one
module, which is the aspect-oriented reading of it. The two-branch split keeps layout
guarantees and semantic guarantees from being conflated, which is a common design-system
error, and it maps cleanly onto the primitive-versus-component boundary this project
draws.

**Cost.** Some criteria straddle both branches and must be recorded twice or
arbitrarily assigned.

**Rejected.** A single flat list of WCAG criteria per component, which obscures whether
a failure is geometric or semantic and therefore obscures who should fix it.

**Verification.** Every criterion in a component specification carries its branch.

**Note.** The boundary is not always where it appears. The WCAG 1.4.10 two-dimensional
exception looks like a layout-support question and is decided on technology-support
grounds, because what is being asked is whether a user needs the two-dimensional
relationship to understand the content. Classification goes by what carries the
meaning, not by what produces the appearance.

### Every specification is testable by construction

**Decision.** A component specification is not complete until it carries the assertions
needed to verify it.

**Reasoning.** When tests are authored separately from specifications the two drift,
and the specification quietly becomes aspirational. Deriving tests from the spec keeps
the claim and the check in one place.

**Cost.** Specifications take longer to write and cannot be published as prose
sketches. Some requirements are not machine-verifiable and must carry a manual or
AT-testing procedure instead, which is slower.

**Rejected.** Prose-only specifications with tests added later, which is the common
practice and the source of the drift described above.

**Verification.** A specification with no assertions and no manual procedure fails
review.

### Components declare what they do not guarantee

**Decision.** Every specification carries an explicit non-guarantees section alongside
its guarantees.

**Reasoning.** A layout primitive that silently omits semantics invites a developer to
assume semantics were handled. Stating that the Stack provides vertical rhythm but not
list semantics, or that the Imposter provides overlay geometry but not focus trapping or
`aria-modal`, converts a hidden assumption into a documented handoff.

**Cost.** Specifications are longer, and the non-guarantee list is open-ended in
principle, so judgement is needed about what is worth stating.

**Rejected.** Guarantees only, which is near-universal practice and is how composition
failures get introduced by developers acting in good faith.

**Verification.** Review rejects a specification with an empty non-guarantees section.

### Conformance is measured at two levels

**Decision.** Components are tested in isolation *and* inside a realistic page with
header, footer, landmarks, and realistic content.

**Reasoning.** A component that passes in a Storybook cell can still produce a broken
heading sequence, a duplicated landmark, or an unreachable focus target in situ. The
GOV.UK Design System requires this realistic-page test in its accessibility acceptance
criteria, and it is the only surveyed system that does.

**Cost.** Fixtures must be built and maintained, and failures are harder to attribute
because the cause may be the composition rather than the component.

**Rejected.** Component-level testing alone, which is what most design systems do and
which cannot detect composition defects by construction.

**Verification.** Every component has both an isolated and an in-page test run.

### AT contracts are only as real as engine support

**Decision.** Where a specification depends on assistive-technology behaviour, the
record must state which engines were tested, their versions, the browser, and what they
actually did.

**Reasoning.** A markup contract that no shipping screen reader honours delivers
nothing to users, however correct it is against the specification. Support genuinely
diverges: roles VoiceOver honours that JAWS largely ignores, TalkBack walking elements
individually and announcing inner geometry rather than a parent group's label. Assuming
"the specification exists, therefore it works" is a recurring and costly trap.
Speech-recognition tools are included in the matrix, following GOV.UK, because they are
the most commonly omitted category.

**Cost.** Testing across NVDA, JAWS, VoiceOver, and TalkBack is slow, requires access
to multiple platforms, and the results expire as engines change.

**Rejected.** Citing specification conformance alone as evidence. It is easier and it
overstates what users receive.

**Verification.** Each affected entry names engine, version, browser, observed
behaviour, and test date.

### Uncertainty is a first-class record type

**Decision.** Unknown or unverified assistive-technology behaviour is recorded in a
dedicated field rather than resolved by assumption.

**Reasoning.** The VA.gov design system's annotation set includes a `Notes` category
explicitly for flagging where an interaction's AT behaviour is not known. Giving
unknowns a home stops them being silently settled as "probably fine", which is how
unverified claims enter a system.

**Cost.** Documentation openly displays its own gaps, which reads as less
authoritative.

**Rejected.** Omitting what is not known, which produces a document that appears
complete and is not.

**Verification.** Any AT-dependent claim without a test record is moved to the
uncertainty field rather than published as a guarantee.

### Decisions are recorded with their rejected alternatives

**Decision.** Every entry names the options considered and why they lost.

**Reasoning.** A decision without its alternatives cannot be re-examined. When
circumstances change, the rejected option may become the right one, and the record
needs to show what the original reasoning depended on.

**Cost.** Entries are longer and slower to write than a simple statement of the choice.

**Rejected.** Recording outcomes only, which produces a document that reads as
confident and cannot be audited.

**Verification.** Review rejects entries with an empty *Rejected* section.

---

## Layout and typography decisions

Recorded in full in [LAYOUT-METHOD.md](LAYOUT-METHOD.md).

### The layout system is intrinsic, not breakpoint-driven

**Decision.** Applications are Electron shells built on raw HTML, CSS, and JavaScript,
laid out using the *Every Layout* method: a small set of composable layout primitives
(Stack, Box, Center, Cluster, Sidebar, Switcher, Cover, Grid, Frame, Reel, Imposter,
Icon, Container), governed by stated axioms and a modular scale seeded from a single
ratio. Primitives are implemented as native custom elements without Shadow DOM. No
layout media queries are used.

**Reasoning.** Designing for the web is designing without seeing: the visual
combinations produced by modular layout components multiplied by each user's settings
cannot be enumerated in advance. Breakpoints encode guesses about the user's
conditions, whereas intrinsic primitives respond to available space whatever the cause
- small window, 400% zoom, raised OS font size, or a narrow nesting context. A media
query only knows the viewport and so gets the last three wrong. Because the scale is
anchored to `rem` and the measure to `ch`, user font-size changes propagate through
every space in the interface rather than breaking it. This satisfies WCAG 1.4.4 Resize
Text, 1.4.10 Reflow, and 1.4.12 Text Spacing structurally rather than by patching.
Flexbox-based composition is additionally sufficient technique C31 for SC 1.4.10, so
the method implements a technique the Working Group deems sufficient rather than merely
being compatible with the criterion. It is also the method already in use on
a11ybob.com, so the project practises what it documents.

**Cost.** Contributors must learn a composition-first mental model before writing any
CSS, which is a real barrier. Debugging is harder: when layout misbehaves the cause is
an interaction between nested primitives rather than a single rule, and `flex-basis:
calc((var(--threshold) - 100%) * 999)` is not self-explanatory. Axioms also produce
artefacts nobody pictured - elements with different font sizes occupy different
proportions of the same container because `1ch` varies - and these must be accepted as
correct rather than treated as bugs. Forgoing Shadow DOM means global styles can leak
into primitives, which is the price of letting user stylesheets and inherited styles
in.

**Rejected.** A utility-first framework such as Tailwind, which barely leverages
inheritance or universal styles and instead applies breakpoint-prefixed utilities
element by element; rejected because the breakpoint prefixes encode viewport
assumptions and the markup bloat obscures structure. A component framework (React,
Vue), rejected because it makes layout dependent on JavaScript, whereas pre-generated
primitive styles stand without it. Shadow DOM encapsulation, rejected because
`aria-labelledby`, `aria-describedby`, `aria-controls`, and `for` cannot cross a shadow
boundary without significant work, and a design system whose purpose is carrying
accessible relationships between components must not obstruct them; it would also block
user stylesheets and forced-colours overrides from reaching inside. Fixed desktop-style
layout, rejected because an Electron window is not a controlled viewport - users resize
it, zoom it, and apply OS-level font scaling regardless of the shell.

**Verification.** No author-fixed sizes in any stylesheet except hairline borders; no
spacing or font-size off the modular scale; no layout media queries (only
`prefers-reduced-motion`, `prefers-color-scheme`, `prefers-contrast`, `forced-colors`);
no fixed heights. Every primitive is tested at 400% zoom, in forced-colours mode, at
doubled root font size, and with text-spacing overrides applied. Layout must be
complete with JavaScript disabled.

**Note.** Derived from *Every Layout* by Heydon Pickering and Andy Bell, a commercial
publication; the axioms, modular scale, owl-selector Stack, Switcher threshold
technique, and transparent-outline high-contrast pattern are theirs and are attributed
in `LAYOUT-METHOD.md`. Their source and prose are not redistributed here. Superseded
position: an earlier assumption that an Electron window could be treated as a
fixed-size desktop surface; abandoned for the reasons above.

### The measure axiom

**Decision.** The measure never exceeds 60ch, applied universally through the `*`
selector with container elements named as exceptions.

**Reasoning.** Measure - line length in characters - is critical for the comfortable
scanning of successive lines, with 45 to 75 characters considered reasonable in
typographic practice. Users with dyslexia, low vision, or attention-related
disabilities lose their place on over-long lines, so this is an accessibility
requirement rather than a stylistic preference. The `ch` unit is required because there
is no relationship between character length and pixel width, so no pixel value can
guarantee a correct measure; `1ch` tracks the font's `0` character and adapts
automatically when font-size changes. An exception-based selector does most of the
styling with the least code and cannot be defeated by forgetting to apply a class.

**Cost.** The universal selector cap is blunt and needs a maintained exception list.
Wide-container layouts show elements at different font sizes occupying different
proportions of the width.

**Rejected.** A `.measure` utility class applied by hand, rejected because manual
intervention is laborious, prone to missed elements, and bloats markup. A pixel
max-width, rejected because it silently breaks whenever font-size changes.

**Verification.** No stylesheet declares a text `max-inline-size` other than
`var(--measure)` or `none`.

**Note.** The measure axiom and WCAG 1.4.10 Reflow are two expressions of one concern,
arrived at from opposite directions. The 60ch cap limits line length as a positive
design constraint; Reflow forbids the failure mode that unbounded line length produces
under magnification.

### Typography follows the same scale as spacing

**Decision.** Font sizes are points on the same modular scale as spacing, with body
text at `1rem` and `line-height: 1.5`, and the scale ratio set to 1.5 to match. The
largest and smallest text on any surface differ by no more than 3:1.

**Reasoning.** Typesetting shares a mathematical basis with music: regularity produces
harmony. Since text dominates the layout, one line of text is the natural denominator
for vertical rhythm, so deriving space from `line-height` ties type and space together
with a single seed value. Strict adherence to whichever ratio is chosen is what creates
cohesion, not the particular ratio, so there is no need to reach for the golden ratio.
The 3:1 cap exists so screen-magnifier users do not have to adjust zoom level when
moving between headings and body text.

**Cost.** The available font sizes are few and widely separated, since each step is
1.5x the last. Any design wanting a size between two points must add a point or accept
the nearest. The 3:1 cap rules out dramatic display typography.

**Rejected.** Independently chosen font sizes and spacing values, which is common
practice and produces a design with no underlying arithmetic and no defence against
gradual drift.

**Verification.** Every `font-size` declaration references a scale custom property;
literal values fail review. Largest-to-smallest ratio is checked per surface.

### What the "no px" rule actually prohibits

**Decision.** No author-fixed dimensions in any stylesheet, except hairline borders.
Dimensions are expressed in `rem`, `ch`, `em`, `cap`, or percentages.

**Reasoning.** The rule prohibits author-chosen values that are frozen against the
user's own font-size and zoom settings. A `rem`-anchored scale moves with those
settings; a pixel value does not.

**Cost.** Contributors must reach for the scale rather than a literal, and hairline
borders need a documented exemption.

**Rejected.** Permitting pixels for "small" values, rejected because the boundary is
arbitrary and erodes.

**Note.** Earlier drafts justified this rule as though pixel units were inherently
unprincipled. That was overstated and is corrected here. The CSS pixel is an angular
measurement of about 0.0213 degrees, or 1.278 arc minutes - not a length. What matters
in reading is not print size but the image projected on the retina, and phones are
designed for closer viewing than desktops, so 16px on a phone is physically smaller
than on a desktop while casting the same retinal image at its intended viewing
distance. The reference pixel exists precisely to give authors stable metrics across
devices. The rule's force is unchanged; its justification is narrower.

### Box shape survives forced colours

**Decision.** Every visually delineated surface carries a transparent outline with a
negative offset, in addition to any background colour.

**Reasoning.** Forced-colours and high-contrast themes eliminate background colours, so
a surface described only by `background-color` disappears entirely. A transparent
outline is invisible under normal conditions and has no layout impact, but a
forced-colours theme gives it a colour and the box shape is restored. The negative
`outline-offset` pulls it inside the perimeter so it behaves like a border without
increasing the element's size.

**Cost.** Two extra declarations on every surface, and the outline property is no
longer available for other purposes on those elements.

**Rejected.** Background colour alone, which is the default approach and fails in
exactly the case the project exists to serve.

**Verification.** Every delineated surface is inspected in forced-colours mode; a
surface whose boundary vanishes fails.

### Data tables claim the two-dimensional exception explicitly

**Decision.** A region may claim the WCAG 1.4.10 two-dimensional exception only by
naming the meaning-bearing axes and stating how a cell's significance depends on both.
The claim is recorded in the component specification. Every individual cell, and all
surrounding content, is tested as ordinary reflowing content.

**Reasoning.** The criterion excepts content requiring two-dimensional layout for usage
or meaning, naming data tables directly - but with the parenthetical "not individual
cells". The grounds are semantic: the criterion's own explanation is that data tables
have a two-dimensional relationship between column and row headers and their data
cells. That relationship is the test. The parenthetical is not a concession carved out
of a layout allowance; it marks precisely where the semantic relationship stops,
because a cell's contents do not depend on either axis. The exception also applies only
to the excepted section and does not extend to a preceding heading, introductory
paragraph, search field, or pagination. Requiring the axes to be named forces the
boundary to be drawn deliberately, so the exception cannot quietly expand to cover an
entire results view.

**Cost.** Two conformance regimes exist within a single view, so testing is more
intricate and a failure must be attributed to either the excepted region or its
surroundings. Specification authors must justify each claim rather than inheriting a
blanket allowance.

**Rejected.** Treating the whole reporting view as excepted, which is the easy reading
and would sweep in headings, filters, and pagination that the criterion explicitly
keeps in scope. Attempting to make wide tables reflow into a single column, rejected
because it is unnecessary and would destroy the row-and-column relationships the
exception exists to protect. Granting the exception on the basis of visual appearance,
rejected for the reasons in the note below.

**Verification.** Each cell wraps within 320 CSS pixels, or truncates with a reveal
mechanism. Headings, prose, search fields, and pagination pass Reflow independently.
The specification names which region is excepted and which axes carry meaning.

**Note.** Two superseded positions are recorded. First, an earlier research-agenda
entry treated wide tables at 400% zoom as an unresolved weakness of the layout method;
the premise was mistaken, since such tables are excepted and Flexbox is itself
sufficient technique C31 for this criterion. Second, an earlier draft stated that the
exception "covers grid-based UI generally". That was unsound: it slid from *grid* as a
semantic structure with header-to-cell relationships to *grid* as a visual arrangement
produced by a layout mechanism. Cells are semantic content; grid is a layout technique.
A CSS Grid container has no semantics whatsoever. Full analysis in
[REFLOW-AND-DATA-TABLES.md](REFLOW-AND-DATA-TABLES.md).

### No region laid out with the Grid primitive claims the exception

**Decision.** Regions arranged with the Grid primitive may never claim the WCAG 1.4.10
two-dimensional exception.

**Reasoning.** The primitive exists to wrap self-contained items that have no
cross-axis relationship, which is the definition of content that *can* reflow. Nothing
about `display: grid` or `repeat(auto-fit, ...)` creates a header-to-cell relationship.
A region that genuinely needs the exception needs a `table` or a `role="grid"`
structure, and the semantics come first.

**Cost.** A dashboard or card collection that would be more compact with
two-dimensional scrolling must instead reflow, which may mean more vertical scrolling
for sighted users at default zoom.

**Rejected.** Allowing an exception claim on the basis of visual arrangement. Treating
a visual arrangement as though it carried the semantics that arrangement resembles is
how inaccessible tables get built: `display: grid` on a set of divs looks tabular and
conveys nothing. Had this been permitted, the documentation would have appeared to
license exactly the error the project exists to attack.

**Verification.** No component specification claiming the exception uses the Grid
primitive for the excepted region.

### Two-dimensional scrolling is always scoped to its container

**Decision.** Any region requiring two-dimensional scrolling is placed in its own
scrollable container. Page-level horizontal scrolling is never permitted.

**Reasoning.** Putting the excepted region in its own scroll container lets surrounding
content reflow as its containing element adjusts. The criterion permits page-level
bidirectional scrollbars where excepted content demands them, but warns that an
unnecessary horizontal scrollbar can lead a user to believe there is off-screen content
to scroll to; if that scrollbar exists only because of one excepted element, the user
may expend effort searching for other non-reflowing content that does not exist. That
is a usability harm rather than a conformance failure, and it is sufficient reason to
scope.

**Cost.** Nested scroll containers are harder to operate with some input methods and
require their own keyboard reachability, so each one adds testing burden.

**Rejected.** Allowing the page to scroll in two dimensions when a wide table is
present, which conforms but misleads.

**Verification.** No page-level horizontal scrollbar appears in any state. Every scoped
scroll container is keyboard-reachable.

### Sticky positioning is not used until a container-driven equivalent exists

**Decision.** No sticky or fixed positioning is used in project interfaces for now.

**Reasoning.** Fixed-position content designed for large viewports obscures the focused
element and severely reduces reading space for exactly the users Reflow serves; the
guidance strongly suggests such components become statically positioned or
user-toggleable at small viewport sizes. An audit tool's natural interface - persistent
toolbar, sticky filter bar, fixed results header - is precisely the named hazard. The
advisory technique for un-fixing sticky headers (C34) uses media queries, which the
layout axioms forbid.

**Cost.** Toolbars and filter controls scroll out of view, which is a real usability
loss on long result lists. This is accepted as temporary.

**Rejected.** Using media queries for this single case, rejected for now because a
stated exception to an axiom weakens the axiom; and sticky positioning without any
un-fixing mechanism, rejected because it reproduces the documented failure.

**Verification.** No `position: sticky` or `position: fixed` in any stylesheet.

**Note.** Open: whether a container-query mechanism can un-fix sticky positioning
without a viewport query, or whether the no-media-query axiom needs a narrow,
documented exception. Tracked in `OPEN-QUESTIONS.md` as D4a.

---

## Documentation decisions

### Markdown, one sentence per line

**Decision.** Prose is authored in Markdown with each sentence on its own line.

**Reasoning.** Diffs become sentence-level, so a review can see precisely which claim
changed rather than a whole reflowed paragraph.

**Cost.** The raw files look unusual to contributors expecting wrapped paragraphs, and
some editors fight it.

**Rejected.** Hard-wrapping at a fixed column, which makes every edit reflow the block
and obscures the actual change.

### Real heading structure, never bold-as-heading

**Decision.** Section headings use Markdown heading syntax in strict order. Bold text is
never used to imitate a heading, and headings are never chosen for their size.

**Reasoning.** Screen-reader users navigate documents by heading. Bold text carries no
structural role, so a bold pseudo-heading is invisible to that navigation and the
document appears to have no structure. The converse error - using heading tags for
styling rather than to structure content - misleads the same users.

**Cost.** None of consequence. This is a discipline, not a trade-off.

**Verification.** Heading order is checked on review; no level may be skipped.

### Tables have header rows and read linearly

**Decision.** Every table carries a header row, and no table uses merged cells or
nested structure.

**Reasoning.** A screen reader announces the column header with each cell, which only
works if the header row exists and the grid is regular. Complex tables lose that
association and become unreadable in linear order.

**Cost.** Information that would fit a complex layout must be split across several
simple tables or moved into prose.

**Rejected.** Layout tables and merged-cell summaries, which look compact and fail in
exactly the case the project exists to serve.

### Link text stands alone

**Decision.** Link text describes its destination without relying on the surrounding
sentence. "Click here" and bare URLs are not used.

**Reasoning.** Screen-reader users list links out of context. A link labelled "here"
conveys nothing in that list.

**Cost.** Sentences are occasionally more awkward, and link text is longer.

### Diagrams are always described in prose

**Decision.** No diagram carries meaning that is not also stated in the surrounding
text. Diagrams that ship in the applications carry `role="img"` with `title` and `desc`
supplying an accessible name and a structural summary.

**Reasoning.** A text alternative on a complex diagram cannot realistically carry a
structural argument. If the diagram is load-bearing, the prose must carry the same
content, with the diagram as a supplement that users can re-read and navigate.

**Cost.** Duplication between diagram and prose, and more writing.

**Rejected.** Detailed `alt` text as the sole alternative, which pushes a long
description into a place users cannot navigate.

### Colour never carries meaning alone

**Decision.** Status, severity, and category are conveyed by text or shape, with colour
as reinforcement only. Where items differ, they differ in shape as well as colour.

**Reasoning.** Colour-only encoding fails for users with colour-vision deficiencies and
disappears entirely under forced-colours modes.

**Cost.** Interfaces and documents look plainer than a colour-coded equivalent.

**Rejected.** Red/amber/green severity coding without labels, the near-universal
convention in accessibility reporting tools and a poor one.

---

## Licensing decisions

### Code and prose are licensed separately

**Decision.** Code is GNU GPL v3.0 only (`GPL-3.0-only`). Documentation and written
content are CC BY-SA 4.0 (`CC-BY-SA-4.0`).

**Reasoning.** Copyleft suits the tooling, so improvements return to the commons.
Creative Commons licences are not designed for software and lack source-provision and
patent terms, so prose gets the licence built for prose.

**Cost.** Contributors must know which licence applies to the file they are editing,
and the boundary between `docs/` and `tools/` has to stay disciplined.

**Rejected.** A single GPL licence for everything, which is simpler and is what some
projects choose to avoid this exact boundary question. Rejected because the repository
is documentation-first and prose deserves prose terms.

**Note.** CC BY-SA 4.0 is one-way compatible with GPLv3. Prose from here may be
incorporated into a GPLv3 work; GPLv3 material may not be relicensed as CC BY-SA. Code
samples inside documentation are marked GPL explicitly.

### Version pinned, no "or later"

**Decision.** `GPL-3.0-only`, not `GPL-3.0-or-later`.

**Reasoning.** The licence terms are known and fixed. Adopting future versions
sight-unseen delegates a licensing decision to a future document.

**Cost.** Relicensing to a future GPL v4 would need explicit action and, with outside
contributors, their agreement.

**Note.** The bare `GPL-3.0` identifier is deprecated in the SPDX License List and is
not used anywhere in this repository.

### Third-party method is attributed, not redistributed

**Decision.** *Every Layout* is credited in full where its method is used, and neither
its prose nor its source is reproduced in this repository.

**Reasoning.** It is a commercial publication. The method can be described, discussed,
and built upon in our own words; the text cannot be copied.

**Cost.** Readers who want the original reasoning in the authors' words must buy it, so
this project's documentation has to stand alone.

**Verification.** No verbatim passages; attribution present in every document that
depends on the method.

---

## Repository decisions

### Structure

```
accessible-by-design/
+-- docs/            Method, decisions, glossary, component specifications
|   +-- COLOPHON.md                       This file
|   +-- LAYOUT-METHOD.md                  The layout method in detail
|   +-- REFLOW-AND-DATA-TABLES.md         SC 1.4.10 analysis
|   +-- OPEN-QUESTIONS.md                 Research agenda
|   +-- RESEARCH-SUMMARY.md               Orientation document
|   +-- CONSISTENCY-PASS-2026-08-28.md    Cross-document conflict record
+-- research/        Literature review, prior art, standards analysis
|   +-- DESIGN-SYSTEMS.md                 Design systems, scope, prior art
+-- tools/           Testing and remediation tooling (not yet started)
+-- LICENSE          GNU GPL v3.0 only  - code
+-- LICENSE-DOCS     CC BY-SA 4.0       - documentation
```

**Decision.** `LICENSE` holds the GPL text so GitHub's licence detection reports
GPL-3.0 for the repository as a whole.

**Reasoning.** GitHub detects a single licence and reads the file named `LICENSE`. The
repository will eventually be tooling-bearing, so GPL is the right headline. The
documentation licence sits alongside in `LICENSE-DOCS` and is described in the README so
the split is not hidden.

**Cost.** The About panel shows one licence where two apply, which the README and this
colophon have to correct.

**Note.** Neither `LICENSE` nor `LICENSE-DOCS` is present in the repository yet. They
must carry the verbatim upstream licence texts, which have not been added. Until then
this structure describes an intent rather than the current state.

### Every file carries an SPDX header

**Decision.** Documentation files open with an SPDX identifier and copyright line in an
HTML comment; source files use the equivalent comment syntax.

**Reasoning.** A per-file marker means the licence of any single file is unambiguous
when it is copied out of the repository, and licence scanners can read it without
heuristics.

**Cost.** Two lines of boilerplate per file.

---

## Not yet decided

`OPEN-QUESTIONS.md` is the single source of truth for the research agenda. The three
items below are listed here because they bear directly on decisions already recorded.

- **Colour system.** OKLCH with constant-lightness pairings is the leading candidate, on
  the reasoning that low-vision users should not have to re-adjust brightness while
  navigating, and that a tinted surface at 95% lightness is gentler than stark white for
  prolonged reading. Bears on the contrast entries above.
- **Conformance target.** WCAG 2.2 AA is the floor. Whether the project commits to AAA
  for its own surfaces is open, and the cost of AAA contrast on data-dense reporting
  views is the main unresolved question.
- **Sticky positioning.** Whether a container-driven mechanism can replace advisory
  technique C34, or whether the no-media-query axiom takes a narrow documented
  exception. Until resolved, sticky positioning is not used at all.

---

## Rendering contract

This file is written so applications built by the project can parse and display it. The
structure is stable and may be relied upon.

**Parsing rules.**

- `##` marks a category; `###` marks a single decision.
- Within a decision, bold run-in labels (`**Decision.**`, `**Reasoning.**`,
  `**Cost.**`, `**Rejected.**`, `**Verification.**`, `**Note.**`) delimit fields. All
  are optional except *Decision* and *Reasoning*.
- Field order is fixed as listed above.
- Fenced code blocks are illustrative and never carry field content.
- Tables are regular, header-first, with no merged cells.

**Rendering requirements.** A renderer must not weaken the accessibility of the source:

- Preserve heading hierarchy as real headings; do not flatten to styled text.
- Render field labels as text, not as colour-coded or icon-only badges.
- Keep *Cost* and *Rejected* visible by default. Collapsing them behind a disclosure
  would reproduce the selective-reporting problem this document exists to avoid.
- Give each decision a stable anchor derived from its heading, so entries can be cited
  from issues and reports.
- Expose the *Last reviewed* date wherever decisions are shown, so readers can judge how
  current the AT-support claims are.

**Maintenance.** When a decision changes, the entry is revised in place and the
superseded reasoning is retained in a `**Note.**` field. Entries are not silently
deleted; the record of having been wrong is part of the evidence.

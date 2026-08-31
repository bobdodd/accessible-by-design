<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# AFDS user guide

A guide to Accessibility Focused Design Systems for designers, developers, and testers who have not worked with a design system before.

This guide explains what a design system is, what it does for design work and for implementation, how it keeps branding consistent across several products, and why the project treats accessibility as the reason the system exists rather than as a feature it happens to include.
It then explains every part of AFDS itself: the layout method, the component contracts, the records that make a claim checkable, and the `.afds` package that carries all of it from one place to another.
It assumes no prior knowledge of design systems, design tokens, or WCAG.

The guide is documentation, not specification.
Where this guide and the project's canonical sources disagree, the canonical sources win and the disagreement is a defect in this guide.
Those sources are named in the references at the end.

## Who this guide is for

The guide is written for three readers at once, because AFDS only works when all three use the same record.

A **designer** decides what an interface looks like and how it behaves.
The parts most relevant to you are the design-system layers, the sections on branding and tokens, the layout method, and the annotation rules that tell a developer what a mock-up cannot show.

A **developer** builds the interface.
The parts most relevant to you are the layout primitives, the component contracts, the keyboard and focus sections, and the whole of the package format, because that is what you will consume and verify.

A **tester or QA engineer** decides whether the result is acceptable.
The parts most relevant to you are the assertions, the five levels of testing, the assistive-technology evidence records, and the realistic-page requirement.

You do not need to read the guide in order.
Each section states what problem it addresses before it explains the mechanism.

## What a design system is

A design system is the set of shared, versioned decisions that a team reuses instead of deciding again.
The project does not define it as a component library, a Figma file, or a stylesheet, because each of those is only one layer of it.

Consider how work happens without one.
A designer needs a warning message, so they pick an orange, a spacing value, and an icon.
Three weeks later another designer needs a warning message on a different screen and picks a slightly different orange and slightly different spacing.
A developer implements both, writing the colour twice.
A tester finds that one of the two oranges fails contrast against its background, files a bug against that one screen, and the other screen keeps its failing orange because nobody knew the two were related.
Six months later the brand changes and someone must find every orange by searching the codebase.

Nothing in that story is incompetence.
It is what happens when a decision has nowhere to live except in the artefact that used it.

A design system gives each decision a home, a name, and a version.

### The five layers

The project treats a design system as five layers.
This table is the operative definition: when people argue about whether something "belongs in the design system", they are almost always arguing across two of these layers without noticing.

| Layer | Contents | Accessibility role |
| --- | --- | --- |
| Principles | Commitments and non-negotiables | Sets the floor and the constraints that may not be traded away |
| Tokens | Named platform-neutral values | Space, type, colour, motion, and contrast-pair candidates |
| Layout primitives | Composable arrangement rules | Reflow, resize, text spacing, reading sequence |
| Components | Interactive elements with semantics and behaviour | Roles, names, states, keyboard, focus |
| Patterns and guidance | Multi-component flows and documentation | Errors, focus management, workflow behaviour |

Read the layers from the top down as decreasing generality.
A principle applies everywhere and is not negotiable per screen.
A token is a value with a name.
A layout primitive arranges things but does not know what they mean.
A component is an interactive thing that does know what it means.
A pattern is several components co-operating through a task.

Take the warning message from the story above and place it in the layers.
The commitment that severity is never communicated by colour alone is a principle.
The specific warning colour and the space around the text are tokens.
The arrangement of icon, heading, and body text is layout.
The message container that announces itself to a screen reader when it appears is a component.
The rule about where focus goes after the user dismisses it is a pattern.

Confusing these layers is the source of many scope disputes.
"Can we make the warning red?" is a token question.
"Should the warning steal focus?" is a pattern question, and it is a much larger question, because the answer changes what happens to the user's place in the page.

### What a design system is not

A design system is not an accessibility guarantee.
The GOV.UK Design System, which the project treats as the strongest public example of a rigorous and honest design system, says directly that using the system does not immediately make a service accessible.

The project adopts that limit as its own and states it in the same plain terms.
A system can improve the available user-interface resources and modalities, but it cannot replace research with disabled users, assistive-technology testing, content quality, or contextual judgement.

The reason is simple.
A design system supplies parts.
It cannot know whether you put the parts together in an order that makes sense, whether your error message explains anything, or whether the task you built is one a user can actually complete.
A perfectly accessible set of components can be assembled into an unusable page, and the components will still pass their own tests while doing it.

Two more things a design system is not.

It is not a component library alone.
A library gives you code.
A system also gives you the reasoning, the tests, and the record of what has and has not been verified, which is what lets somebody else trust the code.

It is not a style guide alone.
A style guide tells you what things look like.
It does not tell you what a component promises, what it refuses to promise, or which keys operate it.

## Why a design system helps design work

The practical benefit is that the number of decisions falls sharply, and the decisions that remain are the interesting ones.

### Decisions are made once and reused

Without a system, every screen re-decides spacing, type size, colour, and arrangement.
With a system, those are already chosen and named, so the designer's attention goes to the task the screen has to support.

This is not merely tidiness.
Each re-decided value is an opportunity to introduce an inconsistency that a user will experience as roughness, and that somebody will eventually have to find and fix by hand.

### Consistency becomes a property of the system, not a matter of diligence

If spacing comes from a named scale, two screens built by two people a year apart have the same rhythm without either person coordinating.
If spacing is typed in by hand, consistency depends on everyone remembering, which is a thing that works until the deadline arrives.

The project's spacing scale takes this further than most.
Every spacing token is an alias of a step on the same scale that governs type sizes, so spacing cannot drift away from the type scale even in principle.
The sample package shows the mechanism directly: `space.default` is not the number `1rem`, it is a reference to `scale.step-0`, which is `1rem`.

### The mock-up stops being the only record

A visual mock-up cannot show what a component promises, which keys operate it, where focus goes when a dialog closes, or what happens at high zoom.
In a system, those live in the component's specification, and the mock-up is annotated to say which component was chosen and what product-specific decisions apply.

The project borrows an economy rule for those annotations from GitHub's design-system practice: do not annotate what the visual design, the component API, or the coded component already guarantees.
Annotating everything makes annotations long, makes them drift from the code, and trains reviewers to skim them, which is worse than not annotating at all.

## Cross-product branding

Design systems are often adopted for this reason first, so it is worth being precise about what the mechanism actually is and where it stops.

A brand expressed as named values can be applied consistently across several products, and can be changed in one place.
A brand expressed as values typed into individual files cannot.

The mechanism is the token layer.
A token is a named value with a type and a description, held in a vendor-neutral format so that it is not trapped inside one tool.
The project uses the W3C Design Tokens format, which reached its first stable version in 2025, and which supports named values, types, descriptions, aliases, themes, and modern colour spaces including OKLCH.

Here is what that buys across products.
Two products that both consume the same token file have the same surface colour, the same body size, and the same spacing rhythm, because they are reading the same names from the same file rather than copying values.
When the brand's surface colour changes, it changes in the token file, and both products pick it up on their next build.
A third product on a different platform can consume the same names through an adapter, so the brand travels without the platforms having to agree on a stylesheet.

Two limits matter, and the project records both rather than letting an adopter discover them.

The first limit is that tokens carry values, not relationships.
The format has no standard way to say "this foreground token is valid only on this background token at a stated contrast ratio".
Contrast is a relationship with a threshold, and the token file cannot express it, so a brand palette expressed purely as tokens is a set of pairing candidates rather than a set of verified pairs.
The sample package says exactly that in the description of its colour group, and puts the pairing constraint in the component specification where it can be tested.
The project records this gap as a possible contribution to the token standard rather than pretending it is solved.

The second limit is that not every value survives every platform.
The project's measure is expressed in `ch` units, which follow the width of a character in the current font, and there is no direct native-platform equivalent.
An adapter that carries tokens to a native platform must therefore report that as a loss rather than substituting a fixed number and presenting the result as equivalent.

One caveat about this section as a whole.
Branding is not the subject of any recorded project decision, so the mechanism described here is what the token layer and the adapter rules make possible.
It is not a policy the project has committed to.

## Why a design system helps implementation

For a developer the benefit is that most interface work becomes composition of small pieces with known behaviour, rather than special-casing.

### Composition instead of special cases

The project's layout method is built from primitives, each with one job.
Composition, rather than increasingly complicated individual components, produces the interface.

A worked comparison makes the difference concrete.
Suppose a card needs its children evenly spaced, its text limited to a comfortable line length, and its surface visible in high-contrast mode.
Written as a special case, that is one CSS block containing spacing, width, and border decisions, which the next card will copy and modify slightly.
Written as composition, it is a Stack for the rhythm, a Center for the line length, and a Box for the surface, each of which is already specified and already tested.

The second version has a property the first does not: when a rule changes, it changes in one primitive, and every composition that uses it inherits the change.

### Margin becomes a relationship rather than an attribute

Stack exists because of a specific observation: margin is a relationship between adjacent elements, not an attribute of each element.
Its mechanism is the sibling relation selector `> * + *`, which applies spacing between children and therefore adds no spacing after the last one.

That is a small thing with a large consequence.
Spacing declared per element produces a redundant final margin, which someone then removes with a special case, which then has to be maintained.
Spacing declared as a relationship has no final margin to remove.

### The contract is in the repository, not in someone's memory

Each component carries a machine-readable contract alongside its prose documentation, and the contract is canonical.
A developer consuming a component can read what it guarantees, what it explicitly does not guarantee, which keys it responds to, and what has not yet been verified, without asking the author.

The project states the reason for making the machine-readable file the authority rather than the prose.
A reader naturally trusts the readable file over the machine-readable one, and in this system that instinct is wrong, because the prose is explanatory and the contract is what tests run against.

### Documentation stops drifting

A specification is incomplete until it carries the assertions or the manual procedure needed to verify it.
The reason is that when tests are authored separately from specifications, the two drift, and the specification becomes aspirational.

The sample component shows what this looks like.
Its contract carries six assertions, three automated and three manual, each with a statement of what is verified and a procedure for verifying it.
One of the automated assertions is that the computed gap resolves to the value of the `space.default` token after alias resolution, which is a check that the implementation has not quietly stopped using the scale.
## Why accessibility is the reason this system exists

Most design systems treat accessibility as a quality that components can have.
This project treats it as the thing the system is for, and that changes what the system has to record.

### The problem with retrofitting

Accessibility work is commonly retrofitted: build, audit late, patch individual findings, repeat.
That cycle treats symptoms, because a finding fixed on one page recurs on the next page that uses the same component.

A design-system approach attaches requirements to reusable components and patterns instead, so that a fix and its reasoning propagate to everything built from them.
Survey research supports the shift: design systems were the most frequently cited accessibility strategy among practitioners, rising from 33% of interviews in 2017 to 52% in 2019-2020.
For comparison, in the same research usability testing with disabled people was cited in 31% of interviews, audits in 17%, and empathy labs in 10%.

The project's own decision follows from that.
Requirements attach to components and patterns, not to pages or to individual audit findings, and coverage is measured against the component inventory rather than against a page count.

There is an honest cost, and the project records it.
An organisation without a design system cannot adopt the method directly, because it must first identify its de facto components.

### Accessibility is a crosscutting concern, split two ways

Accessibility does not sit in one module.
It spans components, which is what makes it easy to lose.

The project splits it in two.

**User technology support** covers assistive-technology compatibility: roles, accessible names, states, focus, and keyboard operation.
**User layout support** covers reflow, measure, spacing, contrast, and reading order.

Every WCAG criterion recorded against a component names which branch it belongs to.
The reason is diagnostic: a flat list of criteria per component obscures whether a failure is geometric or semantic, and those two failures have different owners and different fixes.

The split needs care rather than mechanical application.
The clearest example is the WCAG Reflow exception, which looks like a layout matter but is decided by semantics, as a later section explains.
Classification follows what carries meaning, not the visual mechanism that produced the appearance.

### The five gaps this project is trying to close

The project surveyed existing practice and recorded five recurring gaps.
Each one is the reason a later part of AFDS exists, so they are worth reading as a list of problems rather than as criticism.

1. Layout is treated as visual rather than as an accessibility concern, despite Reflow, Resize Text, and Text Spacing being layout criteria.
2. Components are tested in isolation but not in composition.
3. Assistive-technology claims omit engine, browser, version, observed behaviour, and test date.
4. Tokens express values but not constraints or relationships.
5. Documentation does not carry machine-readable assertions, and drifts from implementation.

A sixth gap sits slightly apart.
A common readiness model checks whether a component is visually accessible, screen-reader compatible, operable, and understandable, which is useful but incomplete when it does not record which engines were tested or address reflow, zoom, text spacing, and forced colours.

### What the project claims to add

Against those gaps, the project states what it is contributing.

1. Layout as a first-class accessibility concern in the system.
2. Intrinsic primitives that respond to available space rather than to breakpoint guesses.
3. Engine-qualified assistive-technology claims, with uncertainty recorded explicitly.
4. Assertions that travel with specifications.
5. Composition conformance as well as component conformance.
6. A documented token-standard gap around contrast relationships.
7. A portable package format that carries the accessibility contract, evidence, and uncertainty as first-class records rather than leaving them in a design tool or an untracked spreadsheet.

## The layout method

This is the part most likely to be unfamiliar, because it rejects the technique most web developers learned first.

The method derives from *Every Layout* by Heydon Pickering and Andy Bell.
It is described and attributed here; the authors' commercial source text and source code are not reproduced, and readers wanting the original reasoning should consult their publication.

### Designing without seeing

Designing for the web is designing without seeing.
The combinations produced by modular layout components and user settings cannot be enumerated in advance.

A user at 400% zoom, in forced colours, with a raised default font size, or inside a narrow nested container creates a condition that no fixed breakpoint can reliably anticipate.
The response is to write programs that generate layouts rather than to micro-manage named viewport artefacts.
Intrinsic layout responds to available space, whatever caused the space to be that size.

Packaging the interface in an Electron shell does not change this.
Users still resize windows, zoom, use operating-system font scaling, and select high-contrast themes.

### The five axioms

Five rules are treated as non-negotiable.

1. The measure never exceeds 60`ch`.
2. Every dimension is user-relative; no author-fixed sizes except hairline borders.
3. Layout responds to available space, not viewport width.
4. No element has fixed height.
5. Layout is complete without JavaScript.

Each of the five has a direct accessibility consequence, which the following sections give.

### The measure

Measure is line length, counted in characters.

Over-long lines make it harder to track from one line to the next, which particularly affects users with dyslexia, low vision, or attention-related disabilities.
The cap is expressed in `ch` rather than pixels because `ch` tracks a font-relative character width, and a pixel width cannot guarantee a character measure as font size changes.

The cap is applied exception-based: content is broadly capped, and deliberate container exceptions are then named.

One consequence is worth stating in advance, because it looks like a bug and is not.
Different font sizes can occupy different proportions of the same wide container, because `1ch` varies with the font size.
That is the axiom working as intended.

The measure axiom and the WCAG Reflow criterion approach one concern from opposite directions.
The axiom limits line length positively, while Reflow prevents unbounded lines under magnification.

### The scale

Body text is `1rem` with `line-height: 1.5`.
One line of text is the natural denominator for vertical rhythm, so 1.5 is also the scale ratio.

Every scale point follows the preceding one through `calc()`, anchored at a root custom property.
The following declaration shows the anchor and the first two derived steps; the pattern continues for as many steps as the system needs.

```
:root {
  --s0: 1rem;
  --s1: calc(var(--s0) * 1.5);
  --s2: calc(var(--s1) * 1.5);
}
```

The anchor `--s0` is one line of body text, and each further step multiplies the previous one by the ratio.
Because the anchor is a `rem` value, it is relative to the user's root font size, so when a user raises that setting, type, gaps, and padding all change together.

The project calls this the highest-value accessibility property of the method, and the reason is worth spelling out.
A layout whose type scales but whose spacing does not will crowd, overlap, or clip as text grows.
A layout whose spacing is derived from the same anchor as its type cannot crowd, because the space grows in proportion.

Font sizes use the same scale, and the largest and smallest text on a single surface differ by no more than 3:1.
That ratio cap exists so that screen-magnifier users need not continually adjust zoom between headings and body copy.

### What the "no px" rule actually prohibits

Beginners often hear "no pixels" as a superstition, so the project states the rule precisely.

The rule prohibits author-fixed sizes that cannot respond to user settings.
It does not claim that the CSS pixel is inherently unprincipled, and in fact a CSS pixel is an angular reference measurement rather than a physical length.
The issue is that author-chosen pixels freeze values against the user's font-size and zoom settings, whereas `rem`-anchored values move with them.

Hairline borders are the documented exception, and the permitted units are `rem`, `ch`, `em`, `cap`, and percentages.

### Styling tiers

Universal and inherited styles come first, layout primitives come second, and utility classes come last.
The governing idea is that reach is inversely proportional to specificity.

Components do not restate inherited `font-family`, `color`, or `line-height`, because restating an inherited value is how a user stylesheet gets overridden by accident.
Utilities are final adjustments, added only when actually needed.

Utility-first, breakpoint-prefixed layout is rejected, because it encodes viewport assumptions in individual elements rather than responding to available space.

### No Shadow DOM

Primitives are native custom elements without Shadow DOM.
That is an unusual choice, so the project records three reasons and the cost.

Shadow boundaries complicate accessibility relationships such as `aria-labelledby`, `aria-describedby`, `aria-controls`, and `for`.
Encapsulation can block user stylesheets and forced-colours overrides.
Light DOM allows primitive styles to be applied at build time, so layout survives with JavaScript disabled.

The cost is accepted openly: global styles can leak in.
That is the price of allowing inherited styles and user styles to reach primitive content, and the project judges the trade worth making.

### The primitives

Each primitive has one job.
The layout method documents twelve in detail, and the project's research summary names thirteen by including a Container primitive.

| Primitive | Job | Mechanism | Does not provide |
| --- | --- | --- | --- |
| Stack | Vertical rhythm between siblings | Relation selector on adjacent children | List semantics |
| Box | Surface padding, border, and colour inheritance | Intrinsic surface styles | Semantic role |
| Center | Constrains the measure, gutters growing outward | Sizing on the content box | Zoom-visibility guarantee |
| Cluster | Wraps indeterminate groups like words | Flexbox with a gap | Recorded separately |
| Sidebar | Two-part layout responding to container width | Intrinsic flex behaviour | Semantics |
| Switcher | Switches axis at a content threshold | An intrinsic threshold calculation | Semantics |
| Cover | Vertical centring with a minimum height | Minimum, never fixed, height | Recorded separately |
| Grid | Wraps self-contained items | Auto-fitting grid tracks | Semantics or a Reflow-exception basis |
| Frame | Constrains media to an aspect ratio | Aspect ratio with object fitting | Recorded separately |
| Reel | Acknowledged horizontal scrolling | Scroll container with reachable items | Hidden-content reachability |
| Imposter | Overlay geometry | Positioning with scrollable overflow | Focus trap, modal semantics, focus return |
| Icon | Sizes icons relative to text | Character-relative units | Recorded separately |

The Switcher's threshold technique is the one piece of the set that looks cryptic, so it is worth showing.

```
.switcher > * {
  flex-basis: calc((var(--threshold) - 100%) * 999);
}
```

When the container is wider than the threshold, the calculation yields a large negative number, which flexbox clamps to zero, and the children sit side by side.
When the container is narrower, it yields a large positive number, which forces each child onto its own line.
The switch therefore happens at a content threshold, in any container, with no media query and no knowledge of the viewport.

Two properties of the primitive set matter more than any individual primitive.

The first is that primitives carry geometry, not ARIA.
The consumer knows whether the content is a list, a dialog, a group, or something else, and the primitive cannot know, so it does not guess.

The second is that each primitive documents both its guarantees and its non-guarantees, which the next major section covers in full.

### Forced colours

A surface described only by `background-color` can disappear in forced-colours mode, because the mode replaces author colours with a restricted system palette.

Every delineated surface therefore also carries a transparent outline with a negative offset.
The outline is invisible normally and takes no layout space, and it becomes visible when forced colours assigns it a system colour.

### The media-query policy

The only permitted media queries are preference queries: `prefers-reduced-motion`, `prefers-color-scheme`, `prefers-contrast`, and `forced-colors`.
No layout media queries are used at all.

The reason is the one given at the start of this section.
Viewport queries cannot reliably account for zoom, operating-system font scaling, or nested container width, whereas container-relative behaviour can.

This has an unresolved consequence that the project records rather than hides.
The usual advisory technique for stopping a sticky header from consuming space at high zoom uses media queries, so until a container-driven equivalent is designed, the project uses neither sticky nor fixed positioning.
The recorded cost is real: toolbars and filters scroll out of view on long results lists.

### The criteria the layout method answers

| Criterion | How the method responds |
| --- | --- |
| 1.4.4 Resize Text | `rem`-anchored type and spacing, following technique SCR34 |
| 1.4.10 Reflow | Available-space primitives; flexbox composition is sufficient technique C31 |
| 1.4.12 Text Spacing | No fixed heights, and spacing expressed as a relationship |
| 1.4.11 Non-text Contrast | The transparent-outline pattern in forced colours |
| 1.3.2 Meaningful Sequence | DOM order is visual order; primitives never reorder content |
| 2.4.11 Focus Not Obscured | No sticky or fixed positioning |

The Reflow row carries a stronger claim than the others, and the distinction is worth understanding.
Flexbox-based reflow is technique C31, which the Working Group lists as sufficient for the criterion.
Implementing a sufficient technique is a stronger position than merely being compatible with a criterion, because it means the method implements something the standard itself accepts as adequate.

### The eleven rules that follow

These are the checks a reviewer applies.

1. No author-fixed dimensions except hairline borders.
2. No spacing or font sizes outside the modular scale.
3. No layout media queries.
4. No fixed heights.
5. Test primitives at 400% zoom, in forced colours, at doubled root font size, and with text-spacing overrides.
6. Layout remains complete with JavaScript disabled.
7. Every delineated surface uses the transparent-outline pattern.
8. DOM order matches visual order.
9. Test primitive behaviour inside realistic pages, not only in isolation.
10. Do not use `position: sticky` or `position: fixed`.
11. A Grid-primitive region may not claim the Reflow two-dimensional exception.

## Reflow and data tables

Rule 11 above needs its own section, because the exception it refers to is the most misunderstood provision in WCAG for people building data-heavy interfaces.

### What the criterion requires

WCAG 2.2 Success Criterion 1.4.10 Reflow requires that content be presentable without loss of information or functionality, and without two-dimensional scrolling, at a width equivalent to 320 CSS pixels for vertically scrolling content, or a height equivalent to 256 CSS pixels for horizontally scrolling content.

The arithmetic behind 320 is worth knowing, because it is where the number comes from.
A 320 CSS-pixel width corresponds to a 1280 CSS-pixel starting viewport at 400% zoom.
The intent is to prevent users from repeatedly scrolling back and forth to read enlarged text line by line.

### The exception, and its exact scope

The criterion excepts parts of content that require two-dimensional layout for usage or meaning.
The cited examples include images needed for understanding, video, games, presentations, data tables — and here the wording is precise — not individual cells, and interfaces where a toolbar must remain visible while content is manipulated.

Two phrases do all the work: "for usage or meaning" and "not individual cells".

The exception rests on a two-dimensional semantic relationship, not on a two-dimensional appearance.
A table qualifies when a cell's significance depends on its relationship to both row and column headers, so that flattening the structure would destroy meaning rather than merely rearrange appearance.

Stated as a slogan, which is how it is easiest to remember: cells are semantic content, and grid is a layout technique.
A CSS Grid container has no table semantics.
Declaring `display: grid` and using auto-fitting tracks creates no row headers, no column headers, and no header-to-cell relationships, so a visual grid arrangement never earns the exception.

### A decision table

This is the single most useful artefact for a reviewer, because most disputes are resolved by finding the closest row.

| Content | Basis | Excepted? |
| --- | --- | --- |
| Results table with genuine row and column header relationships | Cell significance depends on both axes | Yes, as a section |
| Programme guide organised by channel and time | Channel and time are meaningful axes | Yes, as a section |
| CSS Grid card collection | Self-contained cards; arrangement is presentational | No |
| Dashboard grid areas | Arrangement is presentational | No |
| Filter panel beside results | Adjacency is convenience, not meaning | No |

The programme-guide row is the instructive one.
It shows that a meaning-bearing two-dimensional structure need not be a conventional data table.
It does not mean that all visual grids are covered.

### Why "not individual cells" matters

The phrase marks where the semantic two-dimensional relationship stops.

The table needs both axes to mean what it means, but a cell's own content does not depend on either axis in the same way.
A cell is therefore ordinary flow content, and must itself meet Reflow, unless it contains material that independently requires two-dimensional presentation.

For an audit and remediation product this has a concrete consequence.
Long CSS selectors, URLs, failure descriptions, and code excerpts inside cells must wrap at 320 CSS pixels, or provide an accessible mechanism for revealing the complete value.

### The exception does not spread

The exception applies only to the excepted region.
It does not extend to a preceding heading, introductory prose, a search field, filter controls, pagination, or any other surrounding interface, all of which must reflow normally.

It follows that two-dimensional scrolling belongs to a scoped container rather than to the page.
Page-level bidirectional scrolling can be conforming for excepted content, but it is a poor experience, because a page-level horizontal scrollbar makes a user search for off-screen content that does not exist outside the one excepted region.
The project's rule is therefore that two-dimensional scrolling is scoped to the element that needs it and never allowed to reach the page.

### The rules adopted

1. An exception claim names the meaning-bearing axes and explains the cell-to-axis relationship.
2. "It is displayed as a grid" is never a justification.
3. A region using the Grid primitive cannot claim the exception.
4. Scrolling in two dimensions belongs to a scoped container, not the page.
5. Individual cells meet Reflow at 320 CSS pixels, or expose their complete content through an accessible mechanism.
6. Surrounding headings, prose, filters, and pagination are tested as ordinary reflowing content.
7. Reel items are independently readable within 320 CSS pixels.
8. Code preserves meaningful indentation, with exceptions decided per component.
9. Nothing disappears on reflow without remaining reachable.
10. Reflow test records include device, browser, starting viewport, and zoom level.

### Two corrections the project kept on the record

Both are instructive, because both are mistakes that are easy to make.

Earlier research treated wide tables at 400% zoom as an unresolved weakness of the layout method.
That framing was malformed, because data tables with genuine two-dimensional semantic relationships are excepted, and the real work is scoping the exception correctly and meeting Reflow everywhere else.

Earlier wording also said the exception covered grid-based user interfaces generally.
That was wrong because it conflated semantic grid structure with CSS Grid layout, and the corrected test is semantic: whether the two axes carry meaning needed to understand the content.

### Techniques referenced

| Technique | Use in this project |
| --- | --- |
| C31: Flexbox to reflow content | Primary mechanism for Cluster, Sidebar, and Switcher |
| C33: Reflow with long URLs and strings | Required for table cells |
| C38: Width, max-width, and flexbox for labels and inputs | Required for filters and forms |
| SCR34: Sizes and positions scale with text | The `rem`-anchored scale |
| G224: Meaningful indentation and Reflow | Required for code display |
| G225: Horizontally scrolling panels fit 320 pixels | Required for Reel items |
| G206: Layout alternative without horizontal scrolling | Candidate enhancement for excepted table views |
| C34: Un-fix sticky headers with media queries | Open conflict with the no-layout-media-query axiom |

### What remains unsettled

Four questions are recorded as open rather than answered.

1. Can a container-driven alternative to sticky positioning replace the media-query remedy?
2. Should excepted table views offer a user-selected non-horizontal alternative under G206?
3. When does code in a cell need preserved non-wrapping indentation, and when must it wrap?
4. Does the 60`ch` measure apply inside excepted regions, reduce there, or suspend there?
## Components, semantics, and behaviour

A layout primitive arranges boxes.
A component is something a user operates, and that raises questions geometry cannot answer: what is this thing called, what state is it in, which keys work it, and where does focus go afterwards.

### Native HTML first

The default engineering answer is a native element.

Native elements arrive with focus behaviour, activation semantics, disabled-state handling, and forced-colours treatment already implemented, and already tested by browser vendors.
Recreating any of that in a custom widget means recreating the bugs too.

The rule stated as a restriction is that native HTML is used when it provides the needed semantics and interaction, and a recognised custom pattern is adopted only when a genuinely custom composite widget is required.
The most likely failure mode for a team that has just discovered ARIA is to turn every familiar interaction into a custom widget.

This resolution table is ordered roughly from cheapest to most expensive, and the first four rows are expected to account for the large majority of interactive surface.

| Product need | Preferred response | Why |
| --- | --- | --- |
| Reveal supplementary content | Native `details`, or a button with controlled content | Often avoids a full custom disclosure implementation |
| Action | Native `button` | Activation, focus, disabled state, and keyboard behaviour are already provided |
| Choice between options | Native radio or checkbox inputs | Avoids recreating form semantics from scratch |
| Navigation | Links inside landmarks | Do not convert site navigation into a menu widget |
| Modal confirmation | Dialog component following the recognised modal dialog model | A genuine composite interaction with focus-management needs |
| Rich autocomplete | Combobox, only when native controls cannot satisfy the task | High complexity; semantics and keyboard interaction must be complete |
| Large interactive results table | Native table first, with a cell-navigation grid role only where directional navigation is genuinely needed | A visual CSS grid is not a semantic grid and does not justify the Reflow exception |

### Where the ARIA Authoring Practices Guide fits

The ARIA Authoring Practices Guide, usually called the APG, documents more than thirty interaction patterns with worked examples.

Before going further, an important status note.
The project's treatment of the APG is recorded in a research note whose final decision is proposed and not yet adopted.
It is described here because it explains how the project intends to relate to external guidance, not because it is settled policy.

The proposed policy is that the APG is used as a pattern and interaction reference, converted into versioned component contracts, tests, and design-tool annotations, and that its examples are not treated as drop-in components.

The reason for the caution is a distinction that beginners are rarely told.
WCAG 2.2 and WAI-ARIA are normative standards.
The APG is informative guidance.
A component can follow every keystroke recommendation in an APG pattern and still fail WCAG, and a component can depart from an APG key map and still conform to WCAG.

It follows that the sentence "this component conforms to the APG" must never be published as an accessibility claim, because the APG has no conformance model to conform to.
The publishable claims are the WCAG criteria met, the ARIA semantics used, and the recorded assistive-technology results.

Five artefacts therefore sit in a sequence of narrowing scope rather than a hierarchy of authority.

| Artefact | What it governs | Role in this system |
| --- | --- | --- |
| Native HTML | Default semantics, behaviour, and baseline keyboard operation | First choice; avoid custom widgets wherever native controls work |
| WCAG 2.2 | Required accessibility outcomes and the conformance target | The floor, and the source of acceptance criteria |
| WAI-ARIA | Roles, states, properties, and accessibility-tree semantics | Used only where native HTML cannot express the interaction |
| APG | Common interaction patterns, keyboard conventions, and worked examples | Reference for design intent and component behaviour |
| This design system | The implementation that ships, with its tests, documentation, and evidence | The enforceable operational layer |

The design system is the only layer that actually ships, and therefore the only layer that can carry evidence.

The split of what is borrowed and what is owned follows from that.

| Borrowed from the guide | Owned and tested by the system |
| --- | --- |
| Interaction intent and user-facing behaviour | Platform architecture and code style |
| Semantic model: roles, states, properties, relationships | The exact version that ships, and its tests |
| Keyboard model and conventional key bindings | Assistive-technology evidence by engine, version, and date |
| Naming and relationship expectations | Product decisions such as dismissibility and destructive confirmation |
| Awareness of the support caveats the pattern notes | Recorded deviations, non-guarantees, and uncertainty |

### The pattern registry

Every component is proposed to carry exactly one of five statuses, and the registry is what stops the policy becoming decorative.

| Status | Meaning | Example |
| --- | --- | --- |
| Native-first | A native element fully supplies the interaction | `button`, `details`, a checkbox input |
| APG-derived | A custom component implements a recognised pattern | Dialog, Tabs, Menu Button, Combobox |
| APG-adjacent | Similar interaction, intentionally different from the pattern | A product-specific filter panel |
| Custom | No mature pattern applies | A complex audit visualisation |
| Prohibited | The pattern costs more accessibility than it delivers | Site navigation implemented as an ARIA menu |

The statuses are not a quality ranking.
Native-first is the cheapest and safest, and most of a system should sit there, but a Dialog is not defective for being APG-derived.
The value of the registry is that the status is a recorded decision with a rationale, rather than an accident of whoever wrote the component first.

Two statuses exist for social reasons as much as technical ones.
APG-adjacent stops an author labelling a component "APG Combobox" when it deviates materially, and requires them to say which pattern it resembles and where it departs.
Prohibited lets the system say no once, in writing, rather than re-litigating the same idea in every review, and a prohibition must state the cost that motivated it and must be revisitable if support changes.

### The word "grid" means three things

This is the single most common source of confusion in accessibility work on data-heavy products, so the guide separates the three meanings every time the word appears.

An **ARIA grid** is a composite widget with a roving-focus keyboard model, intended for operating cells one at a time.
A **semantic table** is content structure, where meaning comes from header-to-cell relationships rather than from keyboard navigation.
**CSS Grid** is a layout technique, and `display: grid` creates no accessibility semantics at all.

Three consequences follow.
A tabular audit report should not automatically become an ARIA grid.
Adopting a grid widget adds a substantial keyboard and assistive-technology contract that should be paid for by a demonstrated user need.
And the Reflow exception rests on semantic structure, so choosing a grid role in order to unlock the exception would be an abuse of both the role and the criterion.

### What a component specification must contain

For a component derived from an external pattern, these are fields rather than prose suggestions, and a specification missing one of them is incomplete and should fail review.

1. The pattern name and source URL, so a reader can check the reference rather than trust the summary.
2. The native alternative considered, and why it was insufficient.
3. The semantic model: native elements used, ARIA roles, states, properties, and their relationships.
4. The keyboard contract: required keys, optional keys, and key behaviour by state.
5. The focus lifecycle: entry, movement, exit, return, and behaviour on error or failure.
6. Pointer, touch, and speech-input equivalence, in both directions.
7. Visible focus and forced-colours requirements.
8. The WCAG criteria the component is responsible for, by number.
9. The test matrix and observed assistive-technology behaviour, with engine, version, browser, observed behaviour, and test date.
10. Explicit non-guarantees and known uncertainty.

Field 2 is the one that enforces the native-first rule.
An entry that cannot answer it should probably be native-first.

### The keyboard contract

A keyboard contract is a recorded specification, not an implementation detail, and every interactive component specifies eight things.

1. **Entry.** What receives focus when a user Tabs in, and what happens on re-entry after focus has moved internally and then left.
2. **Internal movement.** Which keys move focus inside the component, whether movement wraps at the ends, and whether the implementation uses a roving `tabindex` or `aria-activedescendant`.
3. **Activation.** Which keys act on the focused item, distinguishing keys that change selection from keys that commit an action.
4. **Exit.** Whether Tab leaves, whether Escape dismisses, and where focus goes in each case.
5. **State change.** What a screen reader announces after expansion, selection, validation failure, loading, or deletion, naming the mechanism and the expected announcement.
6. **Restoration.** Where focus returns when a popup closes, including the case where the invoking control no longer exists.
7. **Pointer and touch parity.** Whether all functionality is reachable without hover, without drag, and without a path-dependent pointer movement.
8. **Speech-recognition operation.** Whether every control has a stable visible label a speech-input user can say, with the visible text contained in the accessible name.

Part 5 deserves emphasis, because it is where most real composite widgets fail.
The visual state change is obvious to whoever built it, and the programmatic one was simply never implemented.

Part 6 contains the hardest question in the list.
If an action deletes the row that contained the button that opened the dialog, the invoker no longer exists, and the specification must name a documented logical successor rather than leaving focus to fall to the top of the document.

### "Keyboard" does not mean a keyboard

WCAG defines the keyboard interface broadly, including scanning software, sip-and-puff systems, on-screen keyboards, and speech recognition.
A keyboard interface is an input pathway, not a physical device.

A component's keyboard contract is therefore simultaneously its switch-access contract, its scanning contract, and a large part of its speech-input contract.
Testing with a physical keyboard is necessary and is not sufficient.

Four review checks follow.

1. Avoid fine pointer paths, because precise or continuous pointer movement excludes switch and scanning users and often fails Pointer Gestures.
2. Avoid hover-only discovery, because hover-revealed content is unreachable to keyboard-interface users and unstable for magnifier users.
3. Avoid drag-only movement, because reordering needs a single-pointer and keyboard-interface alternative, which is the substance of Dragging Movements.
4. Avoid inaccessible custom shortcuts, because single-character shortcuts collide with speech-recognition and screen-reader command sets unless they can be turned off or remapped.

### A worked component: Dialog

A dialog is a good example precisely because native HTML alone does not settle every product decision around initial focus, focus restoration, dismissibility, destructive confirmation, and assistive-technology behaviour.

Its classification is APG-derived.
The native `dialog` element was considered, and system behaviour is specified independently because browser and assistive-technology support must be evidenced rather than assumed.
Using `dialog` as the implementation substrate remains open, and specifying behaviour independently means the contract does not change if that choice changes.

What the component guarantees:

1. It has an accessible name.
2. It conveys modal state when modal behaviour is used.
3. It moves focus to an intentional initial target on open.
4. It keeps keyboard focus within the modal interaction while open.
5. It closes on Escape unless the task explicitly requires an alternative.
6. It returns focus to the invoker, or a documented logical successor, on close.
7. It preserves visible focus in default and forced-colours modes.

What it explicitly does not guarantee:

1. That modal behaviour is appropriate for the task.
2. That destructive actions are reversible.
3. That every browser and screen-reader pair announces the same dialog semantics without a recorded compatibility result.

The second of those is a product concern a component cannot solve, and the third is the honest limit of any markup contract.

Its keyboard contract, where each row is a testable assertion rather than a description of typical behaviour:

| Key | Behaviour |
| --- | --- |
| Tab | Moves to the next focusable element within the dialog |
| Shift+Tab | Moves to the preceding focusable element within the dialog |
| Escape | Closes the dialog, unless documented otherwise for a specific instance |
| Enter | Activates the focused control; it is not globally mapped to "confirm" |

The Enter row is the one most often got wrong.
Mapping Enter to the dialog's primary action regardless of which control has focus produces accidental confirmations, and that is especially dangerous in a remediation tool where a confirmation may apply a bulk change.
Enter acts on the focused control, and nothing else.

Its evidence table is presented in the project's own note as empty, with every cell reading "to be recorded", for the four pairs NVDA with Firefox, JAWS with Chrome, VoiceOver with Safari, and TalkBack with Chrome.
It is empty because the testing has not been done, and inventing entries would defeat the purpose of the record.

That is the whole point of the example.
The external pattern reference is one field among many, and the shipped component is governed by its own contract and its own evidence.

### Five kinds of requirement

Every requirement in a component specification carries one of five tags.

| Category | What it means | If it is not met |
| --- | --- | --- |
| Required by WCAG or ARIA | A normative requirement from a W3C standard | A conformance failure |
| Strongly recommended by APG | An interoperable convention users are likely to expect | A usability and discoverability risk, not a conformance failure |
| Project convention | A choice made for internal consistency | An inconsistency to be reconciled or documented |
| Product-specific deviation | A deliberate, recorded departure for a product reason | Nothing, provided the record and its reasoning exist |
| Known support limitation | A gap in browser or assistive-technology behaviour | Uncertainty to be disclosed, not a claim to be made |

Tagging prevents two opposite failures.
It stops documentation presenting all guidance as mandatory conformance law, which erodes trust when somebody checks.
It also stops teams dismissing conventions as merely optional, which is how widgets end up technically conformant and practically unusable.

### The starting catalogue

A system does not begin by implementing every pattern.
It begins with the smallest catalogue that supports the product, in priority order, and the first five priorities consist almost entirely of native elements plus one simple composite.

| Priority | Pattern or primitive | Why it matters |
| --- | --- | --- |
| 1 | Native button, link, checkbox, radio, text input, select | Most actions, filters, and configuration controls |
| 2 | Disclosure | Show and hide issue details, advanced filters, and evidence panels |
| 3 | Dialog | Confirmation, configuration, and remediation guidance |
| 4 | Alert and status messaging | Scan progress, completed checks, and error summaries |
| 5 | Native table plus a scoped scroll container | Audit results, with the semantic Reflow exception correctly scoped |
| 6 | Tabs, only where persistent peer views genuinely improve a task | Avoid using tabs merely to compress a page |
| 7 | Combobox, only where searching a large controlled vocabulary is necessary | High complexity and high regression risk |
| 8 | Tree, Treegrid, or ARIA grid, only after user research demonstrates the need | Complex contract; do not adopt for visual density |

Priorities 6 to 8 are gated on demonstrated need, and each gate is recorded when it is passed.

## The records that make a claim checkable

Four record types carry most of the project's distinctive weight.
Each exists because a specific kind of dishonesty is easy to commit by accident.

### Non-guarantees

Every specification declares what it does not guarantee alongside what it does.

The reason is that a layout primitive which silently omits semantics invites a developer to assume semantics were handled.
Stack provides vertical rhythm, not list semantics.
Imposter provides overlay geometry, not focus trapping, modal semantics, or focus return.

The accepted cost is that specifications get longer and require judgement about which omissions are material.
The verification is blunt: review rejects an empty non-guarantees section.

### Uncertainty

Unknown or unverified assistive-technology behaviour is recorded rather than resolved by assumption.

Giving unknowns a home prevents them being silently settled as "probably fine".
The cost, accepted deliberately, is that the documentation displays its own gaps.

### Assistive-technology evidence

Any claim that depends on assistive-technology behaviour identifies the engine, version, browser, observed behaviour, and test date.

A markup contract that no shipping screen reader honours delivers nothing, however correct it is against a specification, and support diverges across engines and browsers.
The enforcement rule is the one to remember: an assistive-technology claim without a test record is recorded as uncertainty, not as a guarantee.

Testing across NVDA, JAWS, VoiceOver, TalkBack, and speech recognition is slow, and results expire, which is why a result is recorded with a date rather than treated as a permanent property of the component.

### Assertions

A specification is incomplete until it carries the assertions or the manual procedure needed to verify it.

When tests are authored separately from specifications the two drift, and the specification becomes aspirational.
Keeping them together is what makes the difference between a document that describes an intention and a document that describes a tested fact.

## Two levels of conformance, five levels of testing

Components are tested in isolation and inside a realistic page containing landmarks, header, footer, and realistic content.

The reason is that a component passing in isolation can still create a broken heading sequence, a duplicated landmark, or an unreachable focus target in context.
The accepted cost is that fixtures must be maintained and composition failures are harder to attribute.

Beneath that sit five test levels, each catching a class of defect the others miss.

| Level | What to test | Example |
| --- | --- | --- |
| Static semantics | Native element choice, role validity, accessible name, state, relationships | The dialog has a name; the disclosure uses the correct control relationship |
| Keyboard contract | Entry, internal navigation, activation, exit, restoration | Tab enters a composite once; arrows move within it; Escape closes the dialog |
| Visual and layout | Focus visibility, forced colours, 400% zoom, text spacing, Reflow | The focus ring remains visible; the dialog does not trap overflowed content |
| Assistive technology | Actual browser and assistive-technology behaviour, by version and date | The screen reader announces the state change and focus movement as expected |
| Composition in a realistic page | Behaviour among landmarks, headings, and realistic content | Opening a dialog does not create duplicate landmarks or leave focus obscured under page chrome |

The first three levels are largely automatable and should run on every change.
The fourth is manual, slow, and produces results that expire.
The fifth is the level most often skipped, and it is where component-level correctness turns into page-level failure.

## Annotating a design

The bridge between design and implementation is an annotation preset that exposes what a visual mock-up cannot convey.

| Annotation field | What it records |
| --- | --- |
| Pattern identity | For example, the modal dialog pattern or the combobox pattern |
| Semantic model | Native element and any ARIA roles |
| Accessible name source | Where the name comes from, and whether visible text is contained in it |
| Relationship model | Control, expansion, labelling, description, and error-message relationships where relevant |
| Focus order and initial focus | Reading and focus sequence, and the initial focus target |
| Internal keyboard navigation | Which keys move focus inside the component |
| Close and restore-focus behaviour | How the component is dismissed and where focus returns |
| Hidden versus removed from the DOM | Whether content is hidden, made inert, or removed entirely |
| Required visible states | Focus is mandatory; hover is optional |
| Responsive and Reflow behaviour | How the component behaves at narrow widths and high zoom |
| Assistive-technology uncertainty marker | Behaviour known to vary or not yet verified |

A designer who has decided that a control expands a panel has implicitly decided that the expansion and control relationships apply, and recording that is cheaper than discovering it in an audit.

The economy rule from the previous section applies here.
Do not annotate what the coded component already guarantees; identify the selected component and the product-level choices or deviations.
## The AFDS bundle

Everything above is a set of facts about a design system.
The remaining question is how those facts travel from the team that produced them to the team that consumes them, without any of them being lost on the way.

### Why a bundle rather than one format

No current standard represents a complete design system.

The token format is the stable portable representation for named values, but it does not carry component semantics, keyboard interaction, focus lifecycle, Reflow assertions, WCAG mapping, assistive-technology evidence, non-guarantees, or uncertainty.
Custom Elements Manifest describes a web component's public API but not its accessibility contract.
Component Story Format provides executable examples and fixtures but is not a semantic source of truth.

So AFDS composes specialised representations, assigning each kind of fact to the representation able to carry it, and uses a manifest to connect the sources without duplicating them.

The accepted cost is real and worth stating before anyone adopts it.
The system has several artefact types, and it needs identifiers, schema validation, versioning, adapter maintenance, and cross-reference discipline.
A contributor cannot treat a single design-tool file, token file, story, or generated API manifest as the whole system.

Four alternatives were considered and rejected.

1. A proprietary design tool as the sole source of truth, because it locks essential rationale and accessibility meaning into a vendor document model.
2. Tokens alone as the design system, because values do not convey semantics or behaviour.
3. A single universal component JSON invented by this project, because interoperability concerns are divided across specialised formats and relevant standards work is still evolving.
4. Storing core accessibility contracts in token-format extension fields, because extensions are optional metadata and should not be necessary to understand a token value.

### Why a single file

A loose folder hierarchy is portable in theory and cumbersome in practice.
Files are lost in transfer, relationships become ambiguous, integrity is difficult to verify, and a consumer cannot reliably tell which folder or revision is the complete bundle.

A ZIP container is widely supported, cross-platform, compressible, and inspectable with ordinary tools, and it keeps the specialised representations together without claiming that they are one format.
The result is a single file with the `.afds` extension.

The costs are recorded as plainly as the benefits.
A package is less convenient for line-by-line collaboration than a live repository, and it requires unpacking or package-aware tooling to edit an individual artefact.
A ZIP inventory verifies integrity but does not establish identity or authenticity.
And a consumer must defend against path-traversal and decompression attacks, which is why the format specifies both.

### The container rules

A conforming package satisfies every one of these requirements.

| Requirement | Statement |
| --- | --- |
| ZIP syntax | The file uses ZIP syntax and is readable by an ordinary ZIP reader |
| Extension | The file uses the `.afds` extension |
| No enclosing directory | The archive does not wrap its contents in a single top-level directory |
| Root manifest | An entry named exactly `afds-manifest.json` sits at the archive root |
| Root inventory | An entry named exactly `afds-inventory.json` sits at the archive root |
| Normalised relative paths | Every entry path is a normalised relative path using the forward slash as separator |
| No absolute paths | No path begins with a slash, or carries a drive letter or UNC prefix |
| No traversal | No path contains a parent-directory or current-directory segment |
| UTF-8 text | Text content is stored as UTF-8, with no byte-order mark |
| No encryption | No entry is encrypted when the package is intended for portable interchange |

Two of those rules have reasoning worth knowing.

The no-enclosing-directory rule exists so that a consumer can find the manifest without guessing, and many archive tools add a wrapper directory by default, so a producer must check its output rather than trusting the tool.
The path rules exist for security, and a consumer must reject a non-conforming path rather than sanitising it, because sanitising silently changes what the package says.

On media types, there is no dedicated registration, so the correct type to serve a `.afds` file with is `application/zip`, and a consumer identifies a package by opening it and finding a parseable root manifest whose format field says `afds-package`.

### The declared hierarchy

Canonical token files live in a tokens directory, component contracts in a components directory, adapter output in an adapters directory, and so on, and a producer may not place them elsewhere.

An empty optional directory carries no information, so a producer omits it rather than shipping it empty, and declares the absence in the manifest.
An empty array in the manifest is a positive declaration of absence and is preferable to omitting the field, because absence stated is checkable and silence is not.

### The six artefact roles

Every inventoried entry has exactly one role, and the role records who owns the fact the entry carries.

| Role | Meaning |
| --- | --- |
| `canonical` | The authoritative source of the facts it carries; nothing else may contradict it |
| `derived` | Generated from canonical artefacts and reproducible from them |
| `adapter` | Produced for a specific external target, and shaped by that target's limits |
| `evidence` | A record of observation: what was tested, on which engine and assistive technology, on what date, with what result |
| `documentation` | Human-readable prose explaining canonical artefacts; explanatory, not authoritative |
| `schema` | A machine-readable schema that other artefacts validate against |

From those definitions comes the rule that holds the whole format together.
A derived or adapter artefact must never be the only source of a fact owned by a canonical artefact.

A token value is owned by the canonical token file.
A component's semantic model, keyboard contract, Reflow behaviour, WCAG mapping, assertions, non-guarantees, and uncertainty are owned by the canonical component contract.
An observation of assistive-technology behaviour is owned by an evidence record.

If a fact exists only in a generated stylesheet, a design-tool library, or a platform resource bundle, then the fact has left the portable bundle, and at that point the package no longer carries the accessibility contract, which is the exact failure the format exists to prevent.

Two testable consequences follow.
Every derived or adapter artefact must be regenerable from the canonical artefacts in the same package alone, so if regeneration loses a fact then the fact was only in the derived artefact and the package does not conform.
The single exception is an import report, described later under adapters, because an import reads a source that sits outside the package and no package can regenerate it.
And a consumer may discard every derived and adapter entry and still hold a complete design system.

One further rule deserves its own emphasis, because it will feel counter-intuitive.
Documentation explains a canonical artefact and must not introduce a normative fact of its own, so where prose and contract disagree, the contract wins and the prose is a defect to be corrected.
This is stated explicitly because a reader naturally trusts the readable file over the machine-readable one, and in this format that instinct is wrong.

### The manifest

The manifest states what the package is, who may use it and on what terms, which profile it claims, and where every canonical source lives.

### The inventory

The inventory lists every entry with its relative path, media type, byte length, role, and SHA-256 digest, so a consumer can verify transfer integrity before relying on any content.

The inventory excludes itself, and its digests detect transfer changes.
They are not a digital signature: they do not identify a signer and they do not prove provenance.

### Verifying a package, step by step

A conforming consumer implements this procedure.
The steps are ordered so that a cheap check never runs after an expensive one it could have prevented, and so that nothing is parsed before the container is known to be safe.

1. Open the file as a ZIP archive; if it is not a readable ZIP archive, report a container failure and stop.
2. Check every entry path for normalisation, traversal segments, a leading slash, a drive letter, a UNC prefix, and a single enclosing top-level directory; report each violation, stop, and do not sanitise.
3. Confirm no entry is encrypted, and apply the configured limits for entry count, total compressed size, total uncompressed size, per-entry decompression ratio, nesting depth, and path length.
4. Confirm the root manifest exists, decode it as UTF-8, parse it as JSON, confirm its format field, and read its format version.
5. Confirm the root inventory exists, parse it, and confirm its format field, digest algorithm, digest encoding, self-exclusion flag, and matching package identifier and version.
6. Confirm completeness in both directions: every archive entry other than the inventory and directory entries has exactly one record, every record names an entry that exists, no record describes the inventory, and the declared entry count matches the number of records.
7. Compare each entry's uncompressed length with the recorded byte length.
8. Recompute each entry's SHA-256 digest and compare it with the record; if any digest fails, the consumer must not rely on any package content.
9. Validate each canonical token file against the declared token-format version, and if the consumer cannot validate against that version it must report that it did not validate rather than passing the step silently.
10. Emit a single report with a pass or fail verdict, the count of entries checked, and every individual problem found.

Two properties of that procedure are deliberate, and both are good practice worth copying elsewhere.

Steps 2 and 3 run before anything is parsed or extracted, so a hostile archive is rejected before its content is touched.
Steps 6 to 9 gather all problems rather than stopping at the first, because a partial report causes a producer to fix one defect at a time.

Step 10 contains a distinction that matters more than it looks.
A consumer must never report a pass when a step failed, and must distinguish "checked and passed" from "not checked".
Those two are routinely conflated by tools, and the difference is the difference between evidence and silence.

### Security

A package arrives from somewhere else, so a consumer treats it as untrusted input.

Nothing in ZIP syntax prevents an entry path being absolute or containing parent-directory segments, so a naive extractor that joins the entry path onto an output directory can be made to write outside that directory and overwrite arbitrary files.
The defence is to reject the path before extracting anything, and not to rewrite it into a safe one, because rewriting hides the attack.

Separately, a small archive can expand to an enormous volume of data and exhaust memory or disk, and nesting archives inside archives multiplies the effect, which is why the format requires configured limits rather than trusting the declared sizes.

The third security section is the one an adopter is most likely to misread, so it is stated bluntly here.
Integrity is not authenticity.
Matching digests prove that the bytes did not change in transfer; they say nothing about who produced them.

### Conformance profiles

A profile lets a package say how complete it is, so a consumer can reject a package lacking what it needs without inspecting the whole hierarchy.

| Profile | Identifier | Requires |
| --- | --- | --- |
| Tokens only | `afds-tokens` | Root manifest and inventory, and at least one canonical token file declared in the manifest |
| Components | `afds-components` | Everything in the tokens profile, plus at least one component with both a machine-readable contract and a human-readable specification |
| Full | `afds-full` | Everything in the components profile, plus canonical evidence records, a known-limitations artefact, and a declared test fixture for every component |

Three rules govern profiles.
A package satisfies every requirement of the profile it declares.
A package may exceed its declared profile, so a consumer treats the profile as a floor rather than a description.
And a consumer needing a higher profile than the package declares refuses the package even if inspection suggests the extra artefacts are present, because an undeclared artefact carries no commitment to remain present in the next version.

One provision of the full profile is the clearest illustration of the project's whole attitude.
The full profile requires evidence records but does not require that they contain results, and a record whose result is "not yet tested" conforms.
That is deliberate: recording an untested combination is the mechanism by which uncertainty becomes visible, and a profile that demanded results would create pressure to invent them.

### Adapters and honest transforms

An adapter moves information between the canonical artefacts of a package and whatever an external tool or platform uses, and design tools, CSS custom properties, native platform resources, and application shells are all adapter targets.

Adapters run in both directions, and the two directions are not mirror images of each other.

An export adapter reads canonical artefacts and writes what a target expects.
It knows the full set of facts it is allowed to state, because it reads the artefacts that own them, so its whole problem is what the target refuses to accept.

An import adapter reads a target's representation and drafts the artefacts a package requires.
Its problem is the opposite one.
The representation it reads was never obliged to carry an accessibility contract, so most of what a component contract needs simply is not there to be read.

Import matters because no existing design system began in AFDS.
An adopter arrives holding a design-tool library, a token file, a component library, and a good deal of knowledge that was never written down, and the question that decides whether adoption happens at all is what it costs to get from there to a conforming package.
Leaving import undefined would not stop anyone importing.
It would push the work into hand transcription and one-off scripts, whose output lands in a package with nothing recording which facts were real and which were guessed, and that is the silence the format exists to eliminate.

An adapter in either direction must report its mappings, its warnings, and whatever it could not carry, and must not silently flatten meaning.

Silent flattening is the more dangerous of the two behaviours, because the output looks complete.
A `ch`-based measure has no direct native analogue.
A forced-colours boundary has no equivalent in a target that has no concept of a user-forced colour palette.
A keyboard contract has no representation at all in a token pipeline.
In each case the honest output is a recorded finding, not an approximation presented as an equivalent.

No adapter output in either direction carries the canonical role.

### What an import may not do

An import produces a draft, and a draft is not a contract.

A draft becomes canonical only when a person reads it, supplies what the source could not, and accepts responsibility for the accessibility claims the artefact then makes.
The format calls that promotion, and it deliberately cannot be automated, because a canonical artefact asserts something somebody has to be willing to defend when it is challenged.

Two rules follow from that.

An unpromoted draft must never ship inside a conforming package, because once a draft is in a package it is indistinguishable from a contract to whoever relies on it.

And every gap the import recorded must appear in the promoted artefact as uncertainty or as a declared non-guarantee.
An import that could not discover a component's keyboard behaviour has not thereby excused the package from saying that the keyboard behaviour is unknown.
The uncertainty record already exists for exactly this purpose, and an import is the situation that produces the most of them.

There is also a rule about how an import runs, not just what it produces.
An import is a discrete run that leaves a dated report, and it must never be a live read-through dependency on an external tool.
A read-through dependency quietly makes the tool the owner of whatever it supplies, which is the one thing the role system exists to prevent, and it leaves nothing for a reviewer to examine.

What a package keeps from an import is the import report, which is the provenance of everything promoted from it.
The report is also the one artefact exempt from the regeneration rule, for the structural reason that its source was never in the package.

### The transform report

The transform report is where the honesty is made checkable.

These fields are required in both directions.

| Field | Meaning |
| --- | --- |
| `adapterId` | Identifier of the adapter that produced the report |
| `adapterVersion` | Version of the adapter |
| `direction` | Either export or import |
| `target` | The external tool or platform |
| `runDate` | Date of the transform run |
| `validationStatus` | One of passed, passed with warnings, or failed |
| `mappings` | One record per fact carried across |
| `warnings` | Facts carried across with a caveat |

An export report adds two arrays: `losses`, for facts the target could not accept, and `unsupported`, for source features the target has no concept of.

An import report adds the two that face the other way: `gaps`, for facts an AFDS artefact requires and the source could not supply, and `unmapped`, for source content AFDS has no representation for.

A mapping record names the source, its kind, the target name, and a fidelity of exact, approximate, or partial.
A finding record names the source, a severity of information, warning, or error, a statement, and the action a consumer must take about it.

Every array is required even when empty, and the reason is precise.
An empty losses array is a positive claim that nothing was lost, which a reviewer can challenge, whereas an omitted losses field is merely silence.
An empty gaps array makes the far stronger claim that the source supplied every fact an AFDS artefact requires, and it will rarely be true.

An export report containing a loss or unsupported entry of error severity must set its validation status to failed.

An import report containing a gap of error severity must also set its validation status to failed, and this is worth understanding rather than working around.
A failed import is not a malfunction.
For most targets it is the expected result, and what it states is that the source cannot yield a conforming artefact without human authorship.
That is the number an adopter needs before deciding what the work will cost, and a format that hid it would be flattering rather than useful.

### Round-tripping

An export followed by an import is not a round trip in any sense that returns what was sent.

An export is a projection, and a projection discards.
Running it backwards does not restore what it dropped, because the information is not in the target to be read.
A system exported to a token pipeline and imported back is a system with no keyboard contracts, no evidence, and no non-guarantees, because a token pipeline never held any of those.

The value of a defined import path is not that it makes round-tripping work.
It is that the returned system arrives saying so, in a report, instead of arriving looking complete.


### Versioning

Two versions travel in every package and they move independently.
The format version is the version of the package format, and the package version is the version of the design-system payload.

Separating them means a consumer can tell the difference between "the format changed" and "the design system changed", which are entirely different problems for whoever has to react to them.

### What is still open

Four questions about the container are recorded as unresolved: obtaining an IANA media-type registration, adding a signing mechanism, delta and patch distribution, and package-aware editing tooling.

Signing is the one to watch, because it is what would turn integrity into authenticity.

## A complete worked example

The repository ships a small but complete package, and reading it end to end is the fastest way to understand how the parts connect.
The example below quotes the sample's actual contents.

### What the manifest says

Its identifier is `com.a11ybob.abd.afds-sample` at package version `1.0.0`, and the format version is `1.0.0`.
It declares the `afds-components` profile, code under GPL-3.0-only and documentation under CC BY-SA 4.0, and a token declaration naming version `2025.10` of the token format with one canonical source at `tokens/core.tokens.json`.

It declares one component, Stack, of kind `layout-primitive`, with a machine-readable contract at `components/stack/stack.spec.json` and prose at `components/stack/stack.md`.
It declares two evidence sources and three documentation sources, and it declares empty arrays for patterns, schemas, adapters, and stories, which is the positive statement of absence described earlier.

It ends with three notes, and they are the tone of the whole project in three lines.
AFDS 1.0.0 is a project draft, not a W3C standard.
Inventory integrity is not a digital signature and does not prove provenance.
And no assistive-technology test result in the package is real, because every result field is marked "not yet tested".

### What the inventory says

The inventory declares SHA-256 digests in lowercase hexadecimal, excludes itself, and declares an entry count of nine.

Each record looks like this one, for the licence file.

```
{
  "path": "LICENSES.md",
  "mediaType": "text/markdown; charset=utf-8",
  "byteLength": 2136,
  "role": "documentation",
  "sha256": "59e2e4430494ceadffc00f9bd7c6465074df86b233fd9fe835cb538f8e3dd136"
}
```

The record gives the path to locate the entry, the media type so a consumer knows how to decode it, the byte length as a cheap first check, the role that says who owns the fact the file carries, and the digest that detects any change to the bytes.
A verifier compares the length before computing the digest, because comparing an integer is far cheaper than hashing a file, and a length mismatch already proves the content changed.

Note that the manifest carries the role `canonical` in the inventory while the licence file carries `documentation`, which is the role system doing its job at the level of individual entries.

### What the tokens say

The token file declares four groups: a scale, spacing, typography, and colour.

The scale group is the seed of everything.

```
"scale": {
  "$type": "dimension",
  "step-0": { "$value": { "value": 1, "unit": "rem" } },
  "step-1": { "$value": { "value": 1.5, "unit": "rem" } },
  "step-2": { "$value": { "value": 2.25, "unit": "rem" } },
  "step-minus-1": { "$value": { "value": 0.75, "unit": "rem" } }
}
```

Each step is a dimension expressed in `rem`, so every value tracks the user's root font size, and the steps are the modular scale described earlier: `step-0` is one line of body text, and each further step multiplies by 1.5.
The file's own description of `step-0` is "the seed of the scale: one line of body text", and its description of `step-minus-1` records that it is not used for body copy.

The spacing group then does something more interesting than holding values.

```
"space": {
  "$type": "dimension",
  "tight": { "$value": "{scale.step-minus-1}" }
}
```

The value is not a number, it is a reference to a scale step, written in the token format's alias syntax.
The file states the reason directly: spacing tokens are aliases of scale steps rather than independent values, so spacing cannot drift away from the type scale.
A consumer resolving the alias gets `0.75rem`, and if the scale changes, the spacing changes with it, because there is only one place the number exists.

### What the component contract says

The contract carries `afdsSpecVersion`, `id`, `name`, `kind`, `version`, `status`, and `summary` as its identity, and then seven fields that are the substance.

Its summary is that Stack applies consistent vertical rhythm between sibling elements in document order, and that it supplies geometry only.

Its `semanticModel` declares a role of `none`, an implicit element of `div`, and an accessible name of `none`, with a rationale that says exactly why: a layout primitive cannot know whether its children form a list, a group, a set of landmarks, or unrelated blocks, so only the consumer knows.
It also declares that DOM order is reading order, and then lists consumer obligations, including that a consumer supplying list content must supply list semantics on its own markup, and that a consumer must not rely on Stack to convey any relationship between children.

Its `keyboardContract` is the most instructive field in the whole sample, because Stack has no keyboard behaviour at all.
The contract does not omit the field.
It sets `hasKeyboardContract` to false, sets `focusable` to false and `tabStops` to zero, records an empty key-bindings list, and states in prose that the absence is stated explicitly so that a reviewer cannot mistake absence for oversight.
Its `focusLifecycle` sub-object then records false for receiving, moving, trapping, and restoring focus, with a note that focus behaviour belongs entirely to its children.

This is what a first-class record looks like in practice.
A missing field is ambiguous between "nothing to say" and "nobody thought about it", and a field explicitly set to nothing is not.

Its `reflowBehaviour` declares that the primitive is intrinsic, uses no layout media queries, has no author-fixed dimensions, and no fixed heights.
It names the mechanism as a flex column with a `rem`-expressed gap whose block direction grows with content, names `space.default` as the gap token and `typography.measure` as the measure token, and declares that it operates without JavaScript.
It also declares that it does not claim the two-dimensional exception, with the rationale that Stack arranges blocks along one axis and creates no header-to-cell relationship.

Its `wcagMapping` gives one row per criterion, and each row names the criterion number, its name, its level, its branch, the relationship, and a note.
The Reflow row is branch "user layout support" with the note that single-axis flex composition with no author-fixed dimensions is consistent with sufficient technique C31.
The Meaningful Sequence row is branch "user technology support", because reading order is a semantic matter rather than a geometric one.
That is the two-branch split doing diagnostic work at the level of an individual criterion.

Its `assertions` list carries six items, three automated and three manual, each with an identifier, a type, a statement, and a procedure.
The three automated ones are that the computed gap resolves to the value of the `space.default` token, that no descendant introduced by the primitive declares a fixed height or an author-fixed dimension, and that the primitive adds no role, ARIA attribute, or `tabindex` to its own element.
The three manual ones cover behaviour at 320 CSS pixels of available inline size and at 400% zoom, behaviour with the root font size doubled and text-spacing overrides applied, and visual order matching DOM order in the realistic-page fixture.

The first assertion repays a second look.
It does not check that the gap is `1rem`; it checks that the gap resolves to the token's value after alias resolution.
An implementation that quietly hard-coded `1rem` would pass a naive check and fail this one as soon as the scale moved, which is precisely the drift the token aliasing was designed to prevent.

Its `nonGuarantees` list carries seven items: no list semantics, no grouping role or accessible name, no heading structure or landmark, no enforcement of the measure because that is the Center primitive's job, no focus management of any kind, no guarantee of contrast between any pair of colour tokens, and no basis for claiming the two-dimensional Reflow exception.

Read that list as a design document rather than a disclaimer.
It tells a developer exactly which six responsibilities remain theirs, and each one is a real bug that a developer assuming otherwise would ship.

Its `uncertainty` list carries two records.
One says that whether any shipping screen reader announces or otherwise exposes the Stack container element itself has not been tested for this sample.
The other says that the behaviour of `rem`-anchored gaps under operating-system font scaling inside an application shell has not been tested for this sample.
Both carry the status "not yet tested" and both point at the evidence file.

Its `tests` field names an isolated fixture path and a realistic-page fixture path, and then adds a note stating that the sample does not ship the fixtures, that the paths record where they belong in a complete package, and that a consumer must treat them as absent here.

That note is worth pausing on, because it is the difference between a sample and a pretence.
The honest thing to do with a path you have not populated is to say so in the file that names it.

### What the evidence file says

The evidence file declares its own version and then, before any record, declares a result vocabulary of five values.

| Result | Meaning |
| --- | --- |
| `not-yet-tested` | No observation has been made, so the claim it would support is uncertainty rather than a guarantee |
| `supported` | The expected behaviour was observed on the stated engine, browser, and assistive-technology versions on the stated date |
| `partial` | The behaviour was observed but differs materially from the expectation, and the difference must be described |
| `unsupported` | The expected behaviour was not observed |
| `not-applicable` | The combination cannot exhibit the behaviour, for example because the platform has no such feature |

Defining the vocabulary inside the file matters, because "partial" and "unsupported" mean different things to different testers, and a shared record needs a shared meaning.

Each record then names an identifier, the component, the claim being tested, the engine, engine version, browser, browser version, assistive technology, its version, the platform, the device, the starting viewport, the zoom level, the date, the result, the observation, the tester, and a reference to the uncertainty record it relates to.

The device, starting viewport, and zoom fields describe the environment an observation was or would be made in.
They matter because a reflow claim is meaningless without them: "no content is clipped" is a different statement at a 320 CSS pixel viewport than at 1280 by 1024 with 400% zoom applied, and a screen reader on a phone is not the same observation as the same screen reader on a desktop.
On a record whose claim does not involve them, they read `not-applicable`, which is the field-level sense of that value.
A field that says "this does not apply here" is not the same as a result that says the combination cannot exhibit the behaviour, and the sample's own description separates the two senses.

In this sample every observed field reads "not yet tested", leaving only the fields that declare the combination and the environment carrying real values, and the file says so in its own description.
The record for NVDA on Chromium, for instance, names the claim that the Stack container element is not announced as an additional structural object, names Blink as the engine and Windows as the platform, and then records nothing observed, because nothing was observed.

That is an engine-qualified claim with the observation missing, which under the project's rule is uncertainty rather than a guarantee, and the record is the mechanism that makes the distinction visible instead of leaving it to be assumed.

### Rebuilding and verifying the sample

The package ships with a small tool that walks the tree, writes the inventory, verifies it, and packs the archive.
Verification recomputes every digest, and packing produces one more entry than the inventory records, because the inventory excludes itself.

That off-by-one is not a defect, it is the self-exclusion rule made visible: nine inventory records, ten packed entries.

## How each role uses this

### If you are a designer

Choose from the catalogue rather than inventing, and prefer the native-first row wherever it covers the interaction.

Use tokens by name rather than values, and remember that a colour pair is a candidate until somebody has verified its contrast, because the token file cannot express the relationship.

Annotate what the mock-up cannot show: the component chosen, the accessible name and where it comes from, the initial focus target, where focus returns, and any product-specific deviation.
Do not annotate what the coded component already guarantees.

Expect to be asked which axes carry meaning whenever you propose a two-dimensional layout, because that question decides whether a Reflow exception can be claimed.

### If you are a developer

Read the machine-readable contract, not the prose, when the two might differ.

Compose primitives rather than writing bespoke layout, and treat the non-guarantees list as your task list: the semantics the primitive refuses to supply are the semantics you must supply.

Verify a package before you trust it, and treat "not checked" as a distinct outcome from "passed".

If you write an adapter, report your losses.
An empty losses array is a claim you will be held to, and that is the point.

### If you are in QA

Test at all five levels, and notice which level a failure belongs to, because that determines who fixes it.

Never record an assistive-technology result without engine, version, browser, observation, and date, and record "not yet tested" without embarrassment when that is the truth.

Test in a realistic page, not only in isolation, because that is where component-level correctness turns into page-level failure.

Reject an empty non-guarantees section in review, and challenge any two-dimensional exception claim that does not name its meaning-bearing axes.

## Common mistakes

1. Treating a visual grid as a semantic grid, and claiming the Reflow exception for a card collection.
2. Letting a Reflow exception spread from the excepted region to the heading, filters, and pagination around it.
3. Mapping Enter to a dialog's primary action regardless of which control has focus.
4. Writing that a component conforms to the APG, which is not a claim the APG can support.
5. Recording an assistive-technology behaviour without the engine, version, browser, observation, and date that make it an observation rather than a belief.
6. Omitting a field because there is nothing to say, instead of setting it explicitly to nothing.
7. Letting a generated stylesheet or design-tool library become the only place a fact lives.
8. Trusting matching digests as proof of who produced a package.
9. Converting site navigation into a menu widget.
10. Assuming that adopting a design system has made a service accessible.

## What this guide does not settle

Several things in this guide are unfinished, and it is more useful to know which.

The project's treatment of the ARIA Authoring Practices Guide is a proposed decision in a research note, not adopted policy.
The open questions attached to it include which patterns enter the approved catalogue and on what evidence, what the minimum assistive-technology test matrix is and how often results expire, where deviations are recorded, whether the project ships implementations or only specifications, and what support evidence would make the native `dialog` element the required substrate.

The layout method has its own open questions: whether a container-driven alternative to sticky positioning can replace the media-query remedy, whether excepted table views should offer a user-selected alternative to horizontal scrolling, when code in a table cell must preserve indentation rather than wrap, and whether the measure applies inside excepted regions.

The package format has four: media-type registration, signing, delta distribution, and package-aware editing tooling.

And the largest limit is the one the guide has already stated twice.
Using a design system does not immediately make a service accessible.
It improves the resources available to the people building it, and it makes their claims checkable, which is a great deal less than a guarantee and a great deal more than nothing.

## References

Project sources, which are authoritative where this guide and they disagree.

| Source | Location |
| --- | --- |
| AFDS package format specification | `docs/AFDS-PACKAGE-FORMAT.md` |
| Layout method | `docs/LAYOUT-METHOD.md` |
| Reflow and data tables research | `docs/REFLOW-AND-DATA-TABLES.md` |
| ARIA Authoring Practices Guide support research note | `docs/APG-SUPPORT.md` |
| Research summary | `docs/RESEARCH-SUMMARY.md` |
| Decision record | `docs/COLOPHON.md` |
| Open questions | `OPEN-QUESTIONS.md` |
| Sample package | `afds-sample/` and `dist/AFDS-Sample-1.0.0.afds` |
| Repository | https://github.com/bobdodd/accessible-by-design |

External sources.

| Source | Location |
| --- | --- |
| Web Content Accessibility Guidelines 2.2 | https://www.w3.org/TR/WCAG22/ |
| Understanding Success Criterion 1.4.10 Reflow | https://www.w3.org/WAI/WCAG22/Understanding/reflow.html |
| Understanding Success Criterion 1.4.4 Resize Text | https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html |
| Understanding Success Criterion 1.4.12 Text Spacing | https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html |
| WAI-ARIA 1.2 | https://www.w3.org/TR/wai-aria-1.2/ |
| ARIA Authoring Practices Guide | https://www.w3.org/WAI/ARIA/apg/ |
| ARIA Authoring Practices Guide, Dialog (Modal) pattern | https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ |
| Design Tokens Format Module | https://tr.designtokens.org/format/ |
| GOV.UK Design System | https://design-system.service.gov.uk/ |
| Every Layout, by Heydon Pickering and Andy Bell | https://every-layout.dev/ |

The layout method in this project derives from *Every Layout* by Heydon Pickering and Andy Bell.
This guide describes and attributes that work and does not reproduce its source text or code, and a reader wanting the original reasoning should consult the authors' publication.

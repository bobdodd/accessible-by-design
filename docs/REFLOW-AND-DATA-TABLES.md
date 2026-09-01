<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# Reflow, Data Tables, and the Two-Dimensional Exception

Research note on WCAG 2.2 Success Criterion 1.4.10 Reflow.
It resolves the data-dense-layout premise formerly recorded as open question D4.

**Normative form.** Clause 22 of [the AFDS specification](AFDS-SPECIFICATION.md) now carries these rules as the claimable profile `afds-reflow-scoped`, and clause 11.2 carries the core requirement that an exception rationale rest on semantic structure.
Where this note and those clauses disagree, the clauses govern.
This note remains as the reasoning behind the profile.

The semantic reading of the exception set out below is this project's analysis of the criterion's wording, specifically of "for usage or meaning" together with "not individual cells".
It is a defensible reading and it is not a W3C ruling.
The resolution table is this project's application of that reading to cases the Working Group has not adjudicated.
Clause 22.8 of the specification records the full provenance, including which rules here are stricter than the criterion requires.

## Criterion

Content must be presentable without loss of information or functionality and without two-dimensional scrolling at a width equivalent to 320 CSS pixels for vertically scrolling content, or a height equivalent to 256 CSS pixels for horizontally scrolling content.
The exception is for parts of content that require two-dimensional layout **for usage or meaning**.

A 320 CSS-pixel width corresponds to a 1280 CSS-pixel starting viewport at 400% zoom.
The intent is to prevent users from repeatedly scrolling back and forth to read enlarged text line by line.

## The exception

The cited examples are images needed for understanding, video, games, presentations, **data tables (not individual cells)**, and interfaces where a toolbar must remain visible while content is manipulated.

The two operative phrases are “for usage or meaning” and “not individual cells.”

### Semantic, not presentational

The exception rests on a two-dimensional **semantic** relationship.
A table qualifies when a cell's significance depends on its relationship to both row and column headers, so flattening the structure would destroy meaning rather than merely rearrange appearance.

**Cells are semantic content; grid is a layout technique.**
A CSS Grid container has no table semantics.
`display: grid` and `repeat(auto-fit, ...)` do not create row headers, column headers, or header-to-cell relationships.
Visual grid arrangement therefore never earns the exception.

| Content | Basis | Excepted? |
| --- | --- | --- |
| Results table with genuine row and column header relationships | Cell significance depends on both axes | Yes, as a section |
| Programme guide organised by channel and time | Channel and time are meaningful axes | Yes, as a section |
| CSS Grid card collection | Self-contained cards; arrangement is presentational | No |
| Dashboard grid areas | Arrangement is presentational | No |
| Filter panel beside results | Adjacency is convenience, not meaning | No |

The programme-guide example shows that meaning-bearing two-dimensional structures need not be conventional data tables.
It does **not** mean that all visual grids are covered.

### Not individual cells

“Not individual cells” marks where the semantic two-dimensional relationship stops.
The table needs both axes to mean what it means; a cell's content does not depend on either axis in the same way.
A cell is therefore ordinary flow content and must itself meet Reflow unless it contains material that independently requires two-dimensional presentation for usage or meaning.

For this project, long selectors, URLs, failure descriptions, and code excerpts in cells must wrap at 320 CSS pixels or provide an accessible reveal mechanism.

### Outside the exception

The exception applies only to the excepted region.
It does not extend to a preceding heading, introductory prose, search field, filter controls, pagination, or other surrounding interface.
Those parts must reflow normally.

## Scoping scroll

Place an excepted region in its own scrollable container.
That allows surrounding content to reflow while the table preserves its semantic axes.

Page-level bidirectional scrolling can be conforming for excepted content, but it is a poor experience.
A page-level horizontal scrollbar can make a user search for off-screen content that does not exist outside one excepted region.

**Project rule:** two-dimensional scrolling is scoped to the element that needs it and never allowed to reach the page.

## Related constraints

### Resize Text

Text must be increaseable to at least 200% while satisfying Resize Text.
Reflow itself does not require a specific amount of text enlargement at a particular breakpoint.
If a 200% zoom produces a viewport smaller than Reflow's test condition, two-dimensional scrolling is not necessarily a Reflow failure.

This does not weaken the project scale.
The `rem`-anchored scale normally makes special reductions unnecessary.

### Focus Not Obscured

Sticky and fixed content can obscure focused elements and reduce usable reading space at zoom.
At small conditions, such content should become static or user-toggleable.
The usual advisory technique uses media queries.
Because this project forbids layout media queries, it currently forbids sticky and fixed positioning until a container-driven equivalent is designed.

### Meaningful indentation

Nested lists and code can depend on indentation for meaning.
Where it does, reduce indentation under magnification rather than remove it.
A code cell may need a component-level judgement about whether wrapping would destroy meaning.

### Truncated strings

Long strings may be truncated only if a user can reveal the complete value or reach a complete alternative presentation.

### Reels

A horizontally scrolling panel set can conform if every individual panel fits 320 CSS pixels so users only scroll in one direction to read an item.
This is the project standard for Reel.

## Techniques used

| Technique | Project use |
| --- | --- |
| C31: Flexbox to reflow content | Primary mechanism for Cluster, Sidebar, and Switcher |
| C33: Reflow with long URLs and strings | Required for table cells |
| C38: Width, max-width, and flexbox for labels and inputs | Required for filters and forms |
| SCR34: Sizes and positions scale with text | `rem`-anchored scale |
| G224: Meaningful indentation and Reflow | Required for code display |
| G225: Horizontally scrolling panels fit 320px | Required for Reel items |
| G206: Layout alternative without horizontal scrolling | Candidate enhancement for excepted table views |
| C34: Un-fix sticky headers with media queries | Open conflict with no-layout-media-query axiom |

Flexbox is itself sufficient technique C31 for SC 1.4.10.
The project therefore implements a sufficient technique, rather than merely being compatible with the criterion.

## Rules adopted

1. An exception claim names the meaning-bearing axes and explains the cell-to-axis relationship.
2. “It is displayed as a grid” is never a justification.
3. A region using the Grid primitive cannot claim the exception.
4. Scrolling in two dimensions belongs to a scoped container, not the page.
5. Individual cells meet Reflow at 320 CSS pixels or expose complete content through an accessible mechanism.
6. Surrounding headings, prose, filters, and pagination are tested as ordinary reflowing content.
7. Reel items are independently readable within 320 CSS pixels.
8. Code preserves meaningful indentation; exceptions are decided per component.
9. Nothing disappears on reflow without remaining reachable.
10. Reflow test records include device, browser, starting viewport, and zoom level.

## Corrections retained

**Correction 1.** Earlier research treated wide tables at 400% zoom as an unresolved weakness of the layout method.
That was malformed: data tables with genuine two-dimensional semantic relationships are excepted.
The real work is correctly scoping the exception and meeting Reflow everywhere else.

**Correction 2.** Earlier wording said the exception “covers grid-based UI generally.”
That was wrong because it conflated semantic grid structure with CSS Grid layout.
The corrected test is semantic: whether the two axes carry meaning needed to understand the content.

## Remaining questions

- Can a container-driven alternative to sticky positioning replace the media-query remedy?
- Should excepted table views offer a user-selected non-horizontal alternative under G206?
- When does code in a cell need preserved non-wrapping indentation, and when must it wrap?
- Does the 60ch measure apply inside excepted regions, reduce there, or suspend there?

## Source

W3C WAI, *Understanding Success Criterion 1.4.10: Reflow*, WCAG 2.2 Understanding documents.

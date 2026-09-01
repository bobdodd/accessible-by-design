<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# The Layout Method

How layout is done in this project, and why.
The method derives from *Every Layout* by Heydon Pickering and Andy Bell.
The method is described and attributed here; its commercial source text and source code are not reproduced.

**Normative form.** Clause 21 of [the AFDS specification](AFDS-SPECIFICATION.md) now carries this method as the claimable profile `afds-layout-intrinsic`.
Where this note and clause 21 disagree, clause 21 governs.
This note remains as the reasoning behind the profile, and is the longer-form argument rather than the requirement.

## Core argument

Designing for the web is designing **without seeing**.
The combinations produced by modular layout components and user settings cannot be enumerated in advance.
The response is to write programs that generate layouts rather than to micro-manage named viewport artefacts.

A user at 400% zoom, in forced colours, with a raised default font size, or inside a narrow nested container creates a condition no fixed breakpoint can reliably anticipate.
Intrinsic layout responds to available space whatever caused it.
Electron does not change this: users resize windows, zoom, use OS font scaling, and select high-contrast themes.

## Axioms

1. The measure never exceeds 60ch.
2. Every dimension is user-relative; no author-fixed sizes except hairline borders.
3. Layout responds to available space, not viewport width.
4. No element has fixed height.
5. Layout is complete without JavaScript.

### The measure axiom

Measure is line length in characters.
Over-long lines make it harder to track from one line to the next, especially for users with dyslexia, low vision, or attention-related disabilities.
`ch` tracks a font-relative character width; a pixel width cannot guarantee a character measure as font size changes.

The method applies the cap exception-based: broadly cap content, then name deliberate container exceptions.
A consequence is that different font sizes can occupy different proportions of a wide container because `1ch` varies.
That is an expected result of the axiom, not an automatic bug.

The measure axiom and WCAG Reflow address one concern from opposite directions.
The axiom limits line length positively; Reflow prevents unbounded lines under magnification.

## Scale and typography

Body text is `1rem` with `line-height: 1.5`.
One line of text is the natural denominator for vertical rhythm, so 1.5 is the scale ratio.
Every scale point follows the preceding one through `calc()`, anchored at `--s0: 1rem`.
When a user changes root font size, type, gaps, and padding change together.

This is the highest-value accessibility property of the method.
No value may be author-fixed because it must respond to user settings.
Font sizes use the same scale, and the largest and smallest text on a surface differ by no more than 3:1.

### What “no px” prohibits

The rule prohibits **author-fixed sizes that cannot respond to user settings**.
It does not claim that the CSS pixel is inherently unprincipled.
A CSS pixel is an angular reference measurement, not a physical length.
The issue here is that author-chosen pixels freeze values against user font-size and zoom settings, whereas `rem`-anchored values move with them.
Hairline borders are the documented exception.

## Styling tiers

Universal and inherited styles come first, layout primitives come second, and utility classes come last.
Reach is inversely proportional to specificity.
Components do not restate inherited `font-family`, `color`, or `line-height`.
Utilities are final adjustments and are only added when actually needed.

Utility-first, breakpoint-prefixed layout is rejected because it encodes viewport assumptions in individual elements rather than responding to available space.

## No Shadow DOM

Primitives are native custom elements without Shadow DOM.

- Shadow boundaries complicate relationships such as `aria-labelledby`, `aria-describedby`, `aria-controls`, and `for`.
- Encapsulation can block user stylesheets and forced-colours overrides.
- Light DOM enables build-time primitive styles, so layout survives without JavaScript.

The cost is possible global-style leakage.
That is accepted because inherited and user styles must be able to reach primitive content.

## Primitives

Each primitive has one job.
Composition, not increasingly complex individual components, produces the interface.

### Stack

Vertical rhythm through `> * + *`.
Margin is a relationship between adjacent elements, not an attribute of each element.

**Guarantees:** scale-based vertical rhythm, no redundant final margin, DOM order preserved.

**Does not provide:** list semantics.
The consumer applies list semantics where appropriate.

### Box

Intrinsic surface styles: padding, border treatment, and colour inheritance.

**Guarantees:** surface boundaries survive forced colours through the transparent-outline pattern.

**Does not provide:** semantic role.

### Center

Constrains measure using `content-box` so gutters grow outward.

**Guarantees:** measure enforcement.

**Does not provide:** a guarantee that visually centred content remains visible in every zoomed context.

### Cluster

Wraps indeterminate groups like words through Flexbox and `gap`.

### Sidebar and Switcher

Respond to container width, not viewport width.
Switcher uses the intrinsic `flex-basis: calc((var(--threshold) - 100%) * 999)` threshold technique.

**Guarantees:** container-driven reflow.

**Does not provide:** semantics.

### Cover

Vertically centres content with a minimum height, not a fixed height.

### Grid

Wraps self-contained items with `repeat(auto-fit, minmax(...))`.

**Guarantees:** content-driven wrapping.

**Does not provide:** semantics.
A CSS Grid layout is presentational and can never itself justify the WCAG 1.4.10 two-dimensional exception.
A region needing that exception needs semantic table or ARIA-grid structure first.

### Frame

Constrain media with aspect ratio and `object-fit`.

### Reel

A horizontally scrolling container that acknowledges overflow.

**Guarantees:** honest overflow, keyboard-reachable scroll container, and each item independently readable within 320 CSS pixels.
The last requirement follows G225 and is stricter than merely allowing horizontal scrolling.

**Does not provide:** a guarantee that hidden content is otherwise reachable.
F102 still applies: reflow must not make content disappear without access.

### Imposter

Overlay geometry with `overflow: auto` so content cannot be trapped.

**Does not provide:** focus trap, `aria-modal`, or focus return.
Those belong to a dialog component layered over the primitive.

### Icon

Sizes icons relative to text through `1cap` or `1em`.

## Forced colours

A surface described only by `background-color` can disappear in forced-colours mode.
Every delineated surface therefore gets a transparent outline with negative offset.
It is invisible normally, takes no layout space, and becomes visible when forced colours assigns a system colour.

## Container behaviour

Allowed media queries are preference queries: `prefers-reduced-motion`, `prefers-color-scheme`, `prefers-contrast`, and `forced-colors`.
No layout media queries are permitted.

Viewport queries cannot account reliably for zoom, OS font scaling, or nested width.
Container-relative behaviour can.

An open problem remains: advisory technique C34 un-fixes sticky headers using media queries.
Until a container-driven equivalent exists, the project uses neither sticky nor fixed positioning.

## WCAG mapping

| Criterion | Method response |
| --- | --- |
| 1.4.4 Resize Text | `rem`-anchored type and spacing; SCR34 |
| 1.4.10 Reflow | Available-space primitives; Flexbox-based composition is sufficient technique C31 |
| 1.4.12 Text Spacing | No fixed heights; relationship-based spacing |
| 1.4.11 Non-text Contrast | Transparent-outline pattern in forced colours |
| 1.3.2 Meaningful Sequence | DOM order is visual order; primitives do not reorder content |
| 2.4.11 Focus Not Obscured | No sticky or fixed positioning |

C31 is a stronger claim than compatibility.
Flexbox-based primitives implement a technique the Working Group deems sufficient for Reflow.
C33, C38, G224, and G225 govern specific contexts and primitives.

## Project rules

1. No author-fixed dimensions except hairline borders.
2. No spacing or font sizes outside the modular scale.
3. No layout media queries.
4. No fixed heights.
5. Test primitives at 400% zoom, forced colours, doubled root font size, and text-spacing overrides.
6. Layout remains complete with JavaScript disabled.
7. Every delineated surface uses the transparent-outline pattern.
8. DOM order matches visual order.
9. Test primitive behaviour inside realistic pages, not only in isolation.
10. Do not use `position: sticky` or `position: fixed`.
11. A Grid-primitive region may not claim the Reflow two-dimensional exception.

## Attribution

The axioms, scale, Stack relation selector, Switcher threshold, transparent-outline pattern, and primitive approach derive from *Every Layout* by Heydon Pickering and Andy Bell, at <https://every-layout.dev/>.
Readers should consult the authors' publication for the original reasoning.

The adjacent-sibling selector `* + *` that Stack rests on was introduced as the "lobotomized owl selector" by Heydon Pickering in *Axiomatic CSS and Lobotomized Owls*, A List Apart, 21 October 2014, at <https://alistapart.com/article/axiomatic-css-and-lobotomized-owls/>.
The argument that margin is a relationship between adjacent elements rather than a property of an element belongs to that article.

**Correction, 2026-09-01.** This project has described the primitive set as "the twelve Every Layout primitives".
That wording implied Every Layout names twelve.
Its own list of layouts names thirteen, including The Container, which this project does not adopt.
The accurate statement is that this project adopts twelve of the primitives Every Layout names.

What does not derive from Every Layout, and is this project's own, is recorded in clause 21.8 of the specification.
It includes the Shadow DOM prohibition, the absolute prohibition on layout media queries, the requirement that forced-colours inspection be recorded as dated evidence, the prohibition on a Grid-primitive region claiming the Reflow two-dimensional exception, the strict reading of G225 for Reel items, and the deferral of sticky and fixed positioning.

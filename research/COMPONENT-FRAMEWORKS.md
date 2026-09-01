# Component Design Frameworks and the Assembly Problem

*Research note for the Accessibility by Design (AFDS) project.*
*Status: draft for review. Not yet committed to `accessible-by-design`.*
*Supersedes the survey-oriented first draft of `research/COMPONENT-FRAMEWORKS.md`.*

---

## 0. Summary

A component design framework supplies reusable possibilities. It does not supply an
accessible page. The central finding of this note is that **accessibility is not closed
under composition**: two accessible components do not necessarily compose into an
accessible compound component, and a page assembled entirely from accessible components
is not necessarily an accessible page.

The GOV.UK Design System states this limitation directly: using its styles, components
and patterns does not remove the need for further research, design, development and
testing at service level. Its contribution guidance goes further, requiring components to
be tested inside realistic pages with representative content and real assistive
technology combinations, and requiring newly discovered problems to be written up as
accessibility acceptance criteria.

WCAG makes the same point at the other end of the scale. Where several pages are needed
to complete an activity, the *complete process* is the unit of conformance, and every
page in that process must conform. The conformance boundary is therefore neither the
component nor even the single page.

An AFDS is the artefact that sits between those two facts. It is not a catalogue. It is
the record of the rendering and interaction rules selected for a particular interface,
driven by user capability, user preference and application need — and, for the purposes
of this note, the record of **what may be assembled with what, who owns which
accessibility responsibility, which guarantees survive assembly, and what must be
evidenced again at each boundary**.

---

## 1. Market survey (context only)

The survey is retained here in short form because the architectural split it reveals
matters to the argument, not because the catalogue itself is the research.

### 1.1 The three layers

Most component frameworks are structured as design tokens, a component library, and
guidelines. Tokens are the atomic style values (colour, spacing, type scale, radii,
motion durations), increasingly expressed in the W3C Design Tokens Community Group
format, which reached its first stable version in October 2025. The component library
consumes those tokens and exposes constrained variants. The guidelines say when and how
to use each component.

### 1.2 Styled versus headless

The split that matters for AFDS:

- **Styled / opinionated** — Material (Google), Fluent (Microsoft), Spectrum (Adobe),
  Lightning (Salesforce), Carbon (IBM), Polaris (Shopify), Atlaskit (Atlassian),
  Fiori (SAP), Ant Design, Chakra, Mantine, PatternFly (Red Hat), Bootstrap.
  Behaviour and appearance ship together.
- **Headless / behaviour-only** — React Aria (Adobe), Radix UI, Headless UI, Ariakit.
  Focus management, keyboard grammar, ARIA roles and states ship *without* styling.

The headless model is the closer analogue to an AFDS, because it separates the part that
can be guaranteed (interaction semantics) from the part that must be selected per
instance (presentation). This is the same philosophy as Bryan Garaventa's AccDC and its
"Automatically Accessible Technologies" claim: accessibility as a byproduct of the
framework rather than a later audit.

### 1.3 Standards-first and public-sector systems

- **GOV.UK Design System** — WCAG AA baseline, progressive enhancement, published
  accessibility strategy, published accessibility acceptance criteria practice.
- **USWDS** (United States), **Designsystemet** (Norway), **DKFDS** (Denmark),
  **NL Design System** (Netherlands), **Canada.ca**.
- **KoliBri** (ITZBund, Germany) — framework-agnostic WCAG/BITV reference implementation.
- **Lion** (ING) — white-label accessible Web Components designed to be restyled.
- **WAI-ARIA Authoring Practices Guide (APG)** — not a library, but the behavioural
  specification most libraries implement.

The NL Design System is the most interesting governance model for AFDS purposes: it is an
*architecture* that individual agencies build their own component libraries against,
rather than a single shared library. That is structurally closer to a portable AFDS
bundle than a conventional vendor system is.

### 1.4 What the survey does not tell us

Every system above documents components in isolation. Almost none of them publish a
machine-readable statement of **what may contain what**, **who owns focus when two
components are nested**, or **which guarantees are invalidated by an override**. That
absence is the gap this note is about, and it is the gap AFDS exists to fill.

---

## 2. The assembly hierarchy

Accessibility responsibility changes character at each level of assembly. AFDS should
name these levels explicitly.

| Level | Example | Dominant accessibility responsibility |
|---|---|---|
| 0. Primitive | button, input, heading, link | Native semantics, accessible name, state, target size, focus appearance |
| 1. Simple component | search field, alert, card, field group | Relationships among primitives, label association, reading order |
| 2. Composite component | combobox, tablist, data grid, date picker, menu | Internal focus model, keyboard grammar, owned roles, state announcement |
| 3. Region | header, primary navigation, form, results panel | Landmark identity, heading level, region-scoped status |
| 4. Page | the assembled document | Landmark set, heading outline, focus sequence, reflow, duplication, conflict arbitration |
| 5. Process | registration, checkout, application flow | Continuity, state retention, error recovery, consistent navigation, end-to-end conformance |

Two observations follow.

First, most component libraries stop at level 2 and most automated tooling operates at
level 4. Levels 3 and 5 are the least-served and are where composition failures
concentrate.

Second, WCAG's "complete processes" provision means level 5 is a *conformance* level, not
merely a testing convenience. A component-level claim can never discharge a level 5
obligation.

---

## 3. Compositional failure modes

This is the core of the note. Each failure mode below is invisible when components are
inspected in isolation and only appears on assembly.

### 3.1 Semantic collision

The component's semantics are correct alone but wrong, invalid or ambiguous in context.

- A card that owns an `h3` produces a broken outline when placed under an `h1`.
- A navigation component nested inside another `nav` yields two indistinguishable
  landmarks unless each is named.
- A page-shell component and a content component both emit `main`.
- A button nested inside a clickable card creates nested interactive controls with
  ambiguous activation and an unclear accessibility tree.
- A list component wrapped in a layout element that applies `role="presentation"`, or in
  a grid container that breaks `ul`/`li` parent-child integrity, silently loses list
  semantics.
- A cell component is valid only inside the expected row/table ancestry; used standalone
  its role is meaningless.
- ARIA composite widgets impose required owned roles and ordering; a slot that permits
  arbitrary children can break the required parent-child role relationship.

The APG's governing rule applies at exactly this boundary: **no ARIA is better than bad
ARIA**. A composition that produces incorrect ARIA can make the non-visual experience
worse than the same page with no ARIA at all.

### 3.2 Accessible name collision

Names are computed from content and relationships that cross the component boundary, so
assembly can corrupt them.

- Duplicate landmark or region names that were unique in isolation.
- An `aria-label` on a wrapper overriding a meaningful visible label beneath it.
- Twenty repetitions of "Read more" or "Edit" with no distinguishing context, each
  individually passing a name check.
- `aria-labelledby` / `aria-describedby` broken by ID collision when a component is
  instanced more than once on a page, or by ID regeneration on re-render.
- Visible label and accessible name diverging, which breaks speech input users who say
  what they can see, as well as confusing screen reader users.

### 3.3 Focus competition

Each component manages focus correctly; together they fight.

- A dialog traps focus while a combobox inside it also manages focus and wants Escape.
- A route change moves focus to the new `h1` while a toast simultaneously claims focus.
- A disclosure collapses while focus is inside it, dropping focus to `body`.
- A sticky header visually covers the element that has just received focus, so the focus
  indicator exists but is not visible.
- Two roving-tabindex groups nested inside one another share arrow-key handling.
- A virtualised list destroys the focused row on scroll or refetch.
- An async update re-renders the subtree containing the focused element and focus is lost.
- Focus restoration on dialog close targets an element that the underlying page has since
  removed.

Focus is therefore **not solely a component property**. It requires arbitration by an
owner at the containing level.

### 3.4 Keyboard grammar conflict

Keys are contextual and nesting creates ambiguity.

- Arrow keys: move between tabs, move within a menu, move a grid cell, adjust a slider,
  or scroll the page — which wins when a grid is inside a tabpanel inside a dialog?
- Escape: close a popover, cancel inline editing, close the dialog, exit an application
  mode. A single Escape press must resolve to exactly one of these.
- Enter: submit the form versus select the highlighted combobox option.
- Space: activate the button versus scroll the page versus toggle the checkbox.
- Typeahead in a listbox versus application-level or browser-level single-key shortcuts.
- Tab: escape the composite versus move within it.

An AFDS cannot merely assert that each child is keyboard operable. It must state how the
*combined* grammar resolves, and which component is the resolver.

### 3.5 Announcement collision

Independently reasonable live regions become unusable together.

- Validation errors, autosave status and result counts all announce simultaneously.
- A route-change announcement duplicates the new page heading announcement.
- "Loading" is immediately superseded by "42 results", producing either a stutter or a
  swallowed message depending on the screen reader.
- A polite region is starved because an assertive region keeps interrupting.
- Rapid filtering fires an announcement per keystroke.

Assistive technology behaviour for live regions has historically varied sharply between
browser and screen reader combinations, so this is an area where the AFDS must record
*evidence per combination* rather than a single boolean.

### 3.6 Layout and reflow interaction

Components compete for finite space.

- Two independently responsive components impose incompatible minimum widths, producing
  horizontal scrolling at 320 CSS px that neither causes alone.
- Increased text spacing or 200% zoom clips text in a component sized for its demo string.
- A sticky region occludes focused content, or occludes the target of an in-page link.
- Touch targets that meet minimum size individually overlap or fall below spacing
  requirements when packed at narrow widths.
- Tooltips and popovers clipped by an ancestor's `overflow: hidden`, introduced by a
  layout component that knows nothing about them.
- CSS grid or flex `order` diverging visual order from DOM and focus order.
- Two nested container queries producing an unusable intermediate state that neither
  component's own breakpoints anticipated.

This is where the project's use of intrinsic layout (Every Layout) is load-bearing:
components that declare their intrinsic requirements and adapt to available space compose
far more predictably than components that assume a viewport.

### 3.7 Content-dependent failure

Component demos use short, curated, well-formed content. Real assembly does not.

- Long strings, long words, and translations that expand 30–40%.
- Repeated headings and repeated controls.
- Missing images, missing alternatives, missing descriptions.
- Error, empty, loading, partial, stale, offline and permission-denied states.
- User-generated content containing its own headings or markup.
- Density: 5 rows versus 5,000.
- Meaning carried by position or colour that the component cannot express semantically.

This forces the contract distinction that AFDS most needs: **structural guarantees**
versus **author obligations**. A card can guarantee the label-to-control association; it
cannot guarantee that the author supplied a meaningful heading.

### 3.8 Override and escape-hatch invalidation

Every styled library provides escape hatches — `className`, `style`, `as`/`asChild`,
slots, render props, portals, `dangerouslySetInnerHTML`. Each one can silently invalidate
a guarantee:

- Restyling a focus indicator below the non-text contrast threshold.
- Polymorphic `as="div"` on a component whose keyboard behaviour assumed a `button`.
- A slot accepting a child that breaks a required owned-role relationship.
- A portal moving DOM out of the reading order it was tested in.
- CSS `display: contents` removing implicit semantics from a wrapper in some engines.

AFDS must treat overrides as **guarantee-invalidating events** that trigger retest, not as
neutral styling.

---

## 4. Worked examples of composite breakdown

### 4.1 Combobox inside a modal dialog

Both patterns are individually well specified. Composed:

- Escape is claimed by both. Correct behaviour is that Escape first closes the open
  listbox, and only a second Escape closes the dialog. Neither component knows about the
  other, so nothing implements this unless the parent arbitrates.
- The dialog traps Tab; the listbox popover, if portalled to `body`, may sit *outside* the
  trap and become unreachable, or may break the trap.
- Focus restoration on dialog close may target the combobox input, which is correct, or
  the trigger, which may no longer exist.
- `aria-activedescendant` on the input must reference an option that is inside the
  dialog's accessibility subtree.

### 4.2 Clickable card containing a link and a menu button

- Nested interactive controls: the card is `role="link"` or wrapped in an anchor, and
  contains an anchor and a button. The accessibility tree is ambiguous and click targets
  overlap.
- Screen reader users hear the card name, then the same destination again as a link.
- The correct composition is usually the "pseudo-content link" pattern where only the
  title is the link and the card surface is a visual affordance — but the component
  library typically ships both variants and does not prohibit the bad one.

### 4.3 Filter panel plus result list plus result count

- Three components, three plausible live regions. Filtering announces "Filters applied",
  "Loading", and "42 results" in unpredictable order.
- Focus after filtering: staying in the filter is right for a checkbox filter, moving to
  the results heading is right for a submitted search. The components cannot decide; the
  page must.
- If filtering is debounced per keystroke, announcements queue and the user hears stale
  counts.

### 4.4 Data grid inside a tabpanel

- Arrow keys mean "move cell" inside the grid and "change tab" on the tablist. If focus
  handling bubbles, arrowing in the grid changes tabs and destroys the grid.
- The grid's column headers are correct; the tabpanel's accessible name and the grid's
  caption may duplicate.
- Virtualisation: rows outside the viewport are absent from the accessibility tree, so
  `aria-rowcount` must be set explicitly or the grid misreports its size.

### 4.5 Multi-step form (a level 5 case)

- Step 3 validates and returns errors; focus must move to the error summary, and the
  error summary must link to fields — a relationship that spans two components.
- Back-navigation must retain entered data. WCAG's redundant-entry expectations and the
  "complete processes" rule both bite here, and neither is a component property.
- Progress indication, page titles and the browser history must stay coherent across
  steps.
- Session timeout mid-process is an accessibility failure for slower users even though
  every individual page passes.

### 4.6 Responsive navigation

- The same nav is a horizontal menubar at wide widths and a disclosure-driven drawer at
  narrow widths. These are different ARIA patterns with different keyboard grammars.
- If the DOM is shared and only CSS changes, the semantics are wrong at one of the two
  widths. If the DOM is swapped, focus is lost at the breakpoint.
- A user at 400% zoom gets the narrow pattern on a desktop screen — the AFDS must state
  that zoom, not device, selects the pattern.

---

## 5. What this means for AFDS

### 5.1 AFDS is a composition contract

An AFDS is the artefact describing the rendering and interaction rules selected for a
particular interface, driven by user capability, user preference and application need. In
the assembly context, that makes it a **composition contract and decision record**. It
must be able to answer:

1. Which components may be used at all in this instance.
2. Which variant of each has been selected, and why.
3. Which components may contain which others, and which containments are prohibited.
4. What semantics each component owns, and what it delegates upward or to the author.
5. Which component owns focus in each interaction state.
6. How the keyboard grammar resolves when components nest.
7. Which region owns status announcements, at what priority, and which child
   announcements are suppressed.
8. How the components reflow together, not just individually.
9. What obligations remain with the author and the integrator.
10. Which assembled configurations have evidence, and of what kind.
11. Which combinations are prohibited, unsupported, or merely uncertain.
12. What must be retested at region, page and process level.

An AFDS does not make arbitrary assembly safe. It **constrains assembly to combinations
for which the selected rules and the available evidence are sufficient.**

### 5.2 Guarantees do not union

The single most important formal point for the specification:

The guarantees of a parent composition P are not the union of the guarantees of its
children C_i. Instead:

G(P) = V(R(P), C_1,...,C_n, X, E)

where R(P) is the parent's composition rules, X is the context (content,
viewport, language, platform, user profile) and E is the applicable evidence, and
V is validation against the AFDS.

A child guarantee propagates upward **only if all** of the following hold:

- its declared preconditions are still true after assembly;
- the parent has not overridden the relevant semantics, markup or behaviour;
- no sibling conflicts with it (focus, keys, announcements, layout);
- the author obligations it depends on have been satisfied;
- the evidence for it covers the resulting configuration and environment.

Otherwise the guarantee is **suspended** and must be re-established by evidence at the
parent level. Guarantees are conditional and compositional; they are not labels
permanently attached to component names.

### 5.3 Conversely: what AFDS means for component use

The relationship runs both ways, and the second direction is the one usually missed.

- **Components become selections, not defaults.** A component is admissible only if the
  AFDS admits it for this profile and this application need.
- **Variants become profile-bound.** The same requirement may resolve to a menubar for
  one profile and a linear list of links for another. Both are correct AFDS outputs.
- **Escape hatches become declarations.** Any override must be recorded, with the
  guarantees it invalidates and the retest it triggers.
- **Slots become typed.** "Accepts children" is not sufficient; a slot must declare which
  roles it will accept and which it forbids.
- **Component documentation gains a context clause.** "Accessible" is replaced by
  "guarantees X given preconditions Y, with evidence Z".
- **Uncertainty is first class.** A component may honestly declare that its behaviour with
  a particular screen reader is unverified, and that declaration must propagate upward.
- **Third-party components are quarantined.** A component with no AFDS contract enters as
  an unknown and forces evidence at the boundary.

### 5.4 Process change

| Without AFDS | With AFDS |
|---|---|
| Developer picks components | Capability, preference and application need select components and variants |
| Assemble | Assemble within declared composition rules |
| Run automated checks | Validate assembly against the AFDS contract |
| Find problems manually | Propagate surviving guarantees and open obligations upward |
| Remediate after the fact | Test the assembled configuration against its declared acceptance criteria |
| Claim "accessible" | Attach scoped evidence to the configuration, not to the component name |

The shift is from **component certification** to **evidence-based configuration and
composition**.

---

## 6. State propagation in AFDS

State is the mechanism through which most of the failure modes in section 3 actually
occur, so AFDS needs an explicit model rather than relying on framework context, shared
stores or incidental DOM.

### 6.1 Classes of state

- **Intrinsic state** — owned wholly by the component: expanded, checked, selected,
  invalid, busy, current. Expressed in ARIA on the component's own element.
- **Delegated state** — owned by the parent, rendered by the child: which tab is current,
  which step of the process is active, whether the page is in an error state.
- **Ambient state** — page or application scope: route, locale, theme, reduced motion,
  forced colours, zoom/reflow band, offline. Every component may read it; none may own it.
- **Profile state** — from the user's capability and preference model. This is the AFDS
  input that selects variants in the first place.
- **Derived state** — computed from others, e.g. "the form is submittable", which no
  single component can determine.

### 6.2 Propagation rules AFDS should define

- **Downward selection.** Profile and ambient state flow down and may change *which*
  component or variant renders. This must happen at a declared point, not per component,
  or the page becomes internally inconsistent.
- **Upward obligation.** A child that cannot satisfy a guarantee raises an unmet
  obligation to its parent. Unmet obligations aggregate; they do not disappear.
- **Uncertainty propagation.** Child uncertainty propagates upward unless the parent
  bounds it with evidence.
- **Single-owner rule.** For each of focus, keyboard grammar, live-region priority and
  landmark identity, exactly one owner per subtree. Ownership is declared, not inferred.
- **State-to-semantics mapping.** Every state must declare its accessible expression:
  ARIA attribute, live-region message, both, or deliberately neither.
- **Announcement debouncing.** State changes that can fire rapidly declare a coalescing
  policy so the announcement queue is not flooded.
- **Transition contracts.** A state change declares its focus consequence: focus is
  preserved, moved to a named target, or restored to a remembered target.
- **Invalidation on override.** Overriding markup, roles, IDs or handlers marks dependent
  guarantees suspended pending retest.

### 6.3 Contract sketch

```yaml
component: search-results
kind: compound
afdsVersion: 0.x-draft

contains:
  required: [search-form, results-heading, result-list]
  optional: [filters, pagination, status-message]

composition:
  allowedParents: [main, search-page]
  prohibitedDescendants: [main, nested-search-results]
  slots:
    resultItem:
      acceptsRoles: [listitem]
      forbidsRoles: [main, navigation, dialog]

  semanticOwnership:
    heading:      { suppliedBy: consuming-page, requiredLevel: contextual }
    landmark:     { ownedBy: consuming-page }
    resultsStatus:{ ownedBy: search-results }

  focus:
    owner: search-results
    initial: search-input
    afterSubmit: results-heading
    onError: first-invalid-field
    onPaginate: results-heading
    restorePolicy: preserve-user-context

  keyboard:
    resolver: search-results
    escape: close-open-filter-popover-then-defer-to-parent
    enter:   submit-search
    arrowKeys: defer-to-child

  announcements:
    owner: results-status
    priority: polite
    coalesceWindow: 500ms
    suppressChildAnnouncements: [pagination-status, filter-applied]

  layout:
    method: intrinsic
    minInlineSize: 20rem
    reflow:
      - filters-before-results
      - filters-as-disclosure-below-threshold
    minimumTargetSize: token(target.min)

state:
  intrinsic:  [busy, empty, error]
  delegated:  [currentPage, appliedFilters]
  ambient:    [locale, reducedMotion, forcedColors, reflowBand]
  mapping:
    busy:  { aria: "aria-busy", announce: polite, coalesce: true }
    empty: { aria: none, announce: polite }
    error: { aria: "aria-invalid on field", announce: assertive, focus: first-invalid-field }

obligations:
  author:
    - Provide a unique, descriptive page heading
    - Provide meaningful result titles distinguishable out of context
    - Provide an empty-state message
  integrator:
    - Preserve declared DOM order
    - Do not introduce an independent results live region
    - Do not portal the filter popover outside this subtree

evidence:
  isolated:        pass        # axe + keyboard, Storybook
  realisticPage:   required
  completeProcess: required
  assistiveTech:
    - { combo: "NVDA/Firefox",   status: pass,     date: 2026-08 }
    - { combo: "JAWS/Chrome",    status: pass,     date: 2026-08 }
    - { combo: "VoiceOver/Safari", status: unverified }

uncertainties:
  - Announcement timing under rapid filter changes on VoiceOver/iOS
  - Behaviour when result titles are author-supplied HTML
```

The record does not claim `search-results` is universally accessible. It states the
conditions under which this selected composition is expected to hold, and what is not
yet known.

### 6.4 Composition predicates

AFDS should support machine-checkable relations:

- **requires** — a dialog requires a labelled title and a focus-restoration target.
- **contains** — a tablist contains tabs each associated with a tabpanel.
- **excludes** — an interactive card excludes interactive descendants.
- **owns** — the page shell owns the primary landmarks.
- **delegates** — a field delegates label text to the author but owns the association.
- **coordinates** — a page focus controller coordinates dialogs, routing and validation.
- **suppresses** — a parent status system suppresses redundant child live regions.
- **preserves** — a layout transform preserves semantic and focus order.
- **invalidates** — an override invalidates the named guarantees.
- **requiresRetest** — localisation, virtualisation, slot substitution or behavioural
  override triggers a defined suite.

These predicates are what turn AFDS from documentation into an assembly model a validator
can enforce.

---

## 7. Testing across the hierarchy

### 7.1 Evidence must match the claim's level

| Claim | Evidence required |
|---|---|
| Primitive semantics | Accessibility-tree inspection, automated rules |
| Component keyboard behaviour | Manual keyboard walkthrough, scripted key assertions |
| Composite widget operation | APG-derived acceptance tests plus real AT testing |
| Component in context | Realistic-page testing with representative content |
| Region composition | Landmark/heading audit, focus-order audit |
| Page structure and reflow | Page-level automated + manual + 320px/200%/400% + text-spacing |
| Task completion | Usability testing with disabled participants |
| Complete process | End-to-end testing of every page and state in the flow |

GOV.UK's practice combines automated, manual and usability testing, and treats
component-specific accessibility acceptance criteria as a deliverable alongside the
component. That is the model to adopt: never a single undifferentiated "accessible" flag.

### 7.2 Testing multi-page flows

The flow, not the page, is the unit. A workable method:

1. **Model the flow as a state machine** — pages, plus the states within each page
   (pristine, filled, invalid, submitting, error, success, timed-out, offline).
2. **Enumerate transitions**, including back, refresh, deep link, browser back after
   submit, and session expiry.
3. **Drive the flow with a real browser automation harness** (Playwright), running an
   automated rule engine (`@axe-core/playwright`) *after each transition*, not once per
   page load. Axe does not inspect hidden or inactive regions, so dialogs, menus,
   validation summaries and conditional panels must be explicitly activated by the test
   before scanning — this is the single most common cause of false confidence.
4. **Assert focus after every transition.** `expect(page.locator(':focus'))` against a
   declared target, taken from the AFDS transition contract. This is the highest-value
   automated check in flow testing and almost nobody does it.
5. **Assert the announcement**, by snapshotting live-region text content after each
   transition and comparing to the declared message set.
6. **Assert continuity** — re-entering the flow retains data; back navigation does not
   lose state; the page title changes per step.
7. **Snapshot the accessibility tree** per state and diff it in CI, so a composition
   regression shows up as a tree diff rather than as a rule violation.
8. **Run the flow keyboard-only, end to end, manually**, once per release.
9. **Run the flow with at least two screen reader / browser pairs**, and record which.
10. **Run the flow with real users** who use AT, for the tasks that matter.

### 7.3 Tooling map

| Layer | Tools |
|---|---|
| Isolated component states | Storybook + `@storybook/addon-a11y` + Vitest/test-runner, running axe per story |
| Rendered page | axe-core, IBM Equal Access Accessibility Checker, Accessibility Insights |
| Guided manual assessment | Accessibility Insights (assisted/manual steps), WCAG-EM style methods |
| Flow automation | Playwright + `@axe-core/playwright`; Cypress equivalents |
| Focus & keyboard assertions | Playwright locator/focus assertions, custom key-grammar suites |
| Accessibility tree | Browser DevTools a11y panes, Playwright ARIA snapshots |
| AT interoperability | NVDA, JAWS, VoiceOver, TalkBack; ARIA-AT published results |
| Usability | Moderated sessions with disabled participants |

### 7.4 The hard limit

Automated rule engines detect roughly the machine-detectable subset of WCAG — commonly
cited as something like a third to a half of issues, and the exact figure is contested and
depends heavily on the ruleset and the page. What they *cannot* determine is precisely the
set of things composition breaks: whether the focus order is logical, whether an
announcement is appropriate and timely, whether a keyboard grammar is learnable, whether
an accessible name is meaningful out of context, and whether a user can complete the task.

Storybook-level testing is necessary but structurally blind to composition, because a
story renders one component in isolation — which is the exact condition under which every
failure in section 3 is invisible. **Component-level green is not evidence for the page.**
This should be stated as a normative caution in the specification.

---

## 8. Implications for the AFDS specification

Concepts to add or strengthen:

1. **Composition hierarchy** — primitive → component → compound → region → page → process,
   as a normative structure with obligations defined per level.
2. **Composition contracts** — allowed parents, required context, prohibited descendants,
   typed slots.
3. **Accessibility ownership** — single declared owner for semantics, focus, keyboard
   grammar, announcements and layout adaptation within each subtree.
4. **Conditional guarantees** — every guarantee carries preconditions and invalidation
   conditions; nothing is unconditional.
5. **Non-union propagation** — the formal rule of §5.2, stated normatively.
6. **Conflict resolution** — parent-level arbitration policies for focus, keys and
   announcements, with a defined default.
7. **State model** — intrinsic, delegated, ambient, profile, derived; with mapping to
   accessible expression and to focus/announcement consequences.
8. **Evidence scope** — every evidence record states its level (isolated, contextual,
   page, process) and its environment (browser, AT, version, date).
9. **Uncertainty propagation** — unresolved child uncertainty rises unless bounded.
10. **Override accounting** — overrides name the guarantees they suspend.
11. **Content contracts** — author obligations are testable, not advisory.
12. **Profile-selected variants** — one requirement may legitimately resolve to different
    assemblies for different profiles.
13. **Whole-result validation** — the rendered page and the completed task remain the
    final units of accessibility, regardless of component provenance.

### The formulation to carry into the specification

> A component framework supplies reusable possibilities. An AFDS records the components,
> variants, composition rules, ownership assignments and accessibility obligations
> selected for a particular interface. Component guarantees apply only while their
> declared preconditions survive assembly. Accessibility must be evidenced again at each
> higher composition boundary, and the complete process is the final boundary.

---

## 9. Open questions

- Should composition predicates live in the component contract, in a separate composition
  clause of the package, or both? Duplication risks drift; separation risks a contract
  that cannot be validated alone.
- How is ownership expressed when a page uses two design systems? Is there a merge rule,
  or is dual-system use simply out of conformance?
- What is the minimum evidence set for a claim at page level, and can any of it be
  inherited from component level, or is inheritance always unsound?
- Does uncertainty have a severity scale, or is it binary?
- How do profile-selected variants interact with server rendering, where the profile may
  not be known at render time?
- Is there a canonical serialisation for accessibility-tree snapshots that AFDS can cite,
  or must the project define one?

---

## 10. Sources consulted

W3C: WCAG 2.2 and Understanding Conformance (complete processes, conforming alternate
versions); WAI-ARIA 1.2 (composite/managing-container widgets); ARIA Authoring Practices
Guide, including "Read Me First" (no ARIA is better than bad ARIA) and the Modal Dialog
pattern; Design Tokens Community Group (first stable specification, October 2025);
ARIA-AT and CORE-AAM implementation reports.

GOV.UK: Design System components and accessibility pages; the 2023 accessibility strategy
post; `govuk-frontend` guidance on testing components using accessibility acceptance
criteria; Inside GOV.UK on accessibility acceptance criteria; the GDS Way accessibility
manual.

Tooling: axe-core and its API documentation (hidden/inactive regions are not tested);
Playwright accessibility testing and `@axe-core/playwright`; Storybook accessibility
addon and Vitest integration; Accessibility Insights; IBM Equal Access Accessibility
Checker; Slack Engineering on automated accessibility testing at scale.

Design systems surveyed: Open UI design systems catalogue; DesignSystems.one library;
React Aria / React Spectrum; Radix UI; Headless UI; Ariakit; IBM Carbon; USWDS; KoliBri;
Lion; NL Design System.

a11ybob.com: review of the AccDC Enterprise API and "Automatically Accessible
Technologies"; review of WAI-ARIA Live Regions and HTML5 (AT variability); WDFAD;
accessibility statement and colophon; the measure of accessibility and accessibility as a
property of the dialogue.

---

*Draft prepared 2026-09-01. Not committed. Review before pushing to
`bobdodd/accessible-by-design`.*

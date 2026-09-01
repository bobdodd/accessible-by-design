<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# Portable Representations of Design Systems: Standards, Proposals, and Commercial Practice

This research note surveys what can currently be exchanged between tools when a design system moves between organisations, vendors, or platforms.
It asks a narrower question than "how do we export our design system".
It asks which specific facts about a design system have a vendor-neutral representation today, which do not, and what a project should therefore own itself.

The conclusion is stated up front so that the rest of the note can be read as evidence rather than suspense.
There is no single portable file format for a complete design system, and the robust approach is a portable bundle of specialised artefacts joined by a small manifest.

## Framing: portability is not one problem

"Portable design system" sounds like one interoperability problem with one missing file format.
It is not.
A design system contains at least five different kinds of fact, and each kind has its own standards landscape, its own maturity level, and its own characteristic failure mode.

The five kinds are token values, component metadata, implementation contracts, documentation and rationale, and test evidence.

Token values are named platform-neutral constants such as a spacing step or a colour.
Component metadata describes a component's public programmatic surface: its attributes, properties, events, slots, and styling hooks.
Implementation contracts describe what a component guarantees semantically and behaviourally: its role, accessible name, states, keyboard model, focus lifecycle, and response to user preferences.
Documentation and rationale describe why a decision was taken, what was rejected, what the cost was, and what remains uncertain.
Test evidence records what was actually observed, in which browser, with which assistive technology, at which version, on which date.

These five are not variants of one another.
A token value is a datum, a component contract is an assertion, and a piece of evidence is an observation with provenance.
Collapsing them into a single export format loses the distinction between the three, and the distinction is precisely what an accessibility-focused design system depends on.

The failure modes differ too.
A token value that fails to travel produces a visual mismatch that a designer notices within minutes.
A component contract that fails to travel produces a silent accessibility regression that nobody notices until a disabled user is excluded.
An evidence record that fails to travel produces a confident claim with no basis, which is worse than no claim at all.

This note therefore treats portability as a set of related but separate questions, and evaluates each candidate representation against the specific kind of fact it is actually able to carry.

## The central finding

No current standard represents a complete design system.

The representations that do exist are individually good and collectively incomplete.
Design tokens have a stable, published, vendor-neutral format.
Web Component public APIs have a mature community file format.
Component examples have a mature de facto format.
Component anatomy and state vocabulary have an active W3C Community Group incubating them.
Structured design-system documentation has a very new Community Group.
Accessibility contracts and assistive-technology evidence have no complete standard at all.

The robust response is a portable bundle rather than a monolithic format.
A bundle assigns each kind of fact to the representation capable of carrying it, and connects those representations through a small manifest that links artefacts without duplicating their content.

The bundle proposed by this note is composed of the following parts.

- Design Tokens Community Group (DTCG) tokens JSON for token values, aliases, descriptions, themes, and deprecation.
- Custom Elements Manifest (CEM) for the public API of any published Web Components.
- Storybook Component Story Format (CSF) for executable examples, states, visual review, and interaction-test fixtures.
- Markdown prose paired with a structured, schema-validatable component specification for rationale, accessibility contracts, non-guarantees, and usage guidance.
- Structured assistive-technology evidence records carrying engine, browser, version, observation, and date.
- A small manifest that identifies which artefact is canonical for which kind of fact.

The manifest is deliberately thin.
Its job is to say where authority lives, not to restate the content of the artefacts it points at.

## Maturity of the candidate representations

The table below summarises the state of each candidate representation and the role this project assigns to it.
Maturity is stated in terms of the publishing body's own status language wherever that language exists.

| Area | Representation | Maturity | Role for this project |
| --- | --- | --- | --- |
| Token values | [DTCG Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/) | Final Community Group Report, described by its own status section as stable, explicitly not a W3C Standard | Adopt now as the canonical token format |
| Web Component public APIs | [Custom Elements Manifest](https://custom-elements-manifest.open-wc.org/) | Mature community file format with a maintained analyser and a published schema | Adopt if primitives ship as custom elements; generate rather than hand-author |
| Component examples and states | [Storybook Component Story Format](https://storybook.js.org/docs/api/csf/index) | Mature de facto format, described by Storybook as an open standard based on ES6 modules | Adopt for executable fixtures only, never as semantic truth |
| Component anatomy and state vocabulary | [Open UI Community Group](https://open-ui.org/) | Active W3C Community Group incubation | Follow and borrow vocabulary; do not depend on it as a file format |
| UI behaviour, layout, and accessibility schema | [UI Specification Schema Community Group](https://www.w3.org/community/uispec/) | **Closed on 2026-05-21**, proposed 2025-08-11; never chose a chair and produced no output | Treat the charter as a requirements document. It is not a dependency and not an alignment target |
| Structured design-system documentation | [Design System Documentation Community Group](https://www.w3.org/community/designsystemdocs/) | Very new; proposed 2026-07-29, now co-chaired by Ben Callahan and Afyia Smith, no draft published | The live alignment target. Monitor and consider contributing requirements; do not depend on yet |

Two rows in that table correct assumptions that are easy to carry into this research.

The UI Specification Schema Community Group is the closest thing anyone has proposed to the artefact this project needs, and its own W3C page records that the group "was closed on 2026-05-21" ([UI Specification Schema Community Group](https://www.w3.org/community/uispec/)).
It is important to be precise about what closed: the group never chaired itself, its `public-uispec` mailing list holds **zero messages** ([public-uispec archive](https://lists.w3.org/Archives/Public/public-uispec/)), and no report or draft was ever published.
The charter is therefore not the residue of abandoned work; it is the only thing that ever existed.
That makes it useful as a statement of requirements and useless as a vocabulary to align to, because no vocabulary was written.

The Design System Documentation Community Group is newer than it might appear, but it has begun to organise.
Its W3C page records that it "was originally proposed on 2026-07-29 by PJ Onori", and its group page now names Ben Callahan and Afyia Smith as co-chairs ([Design System Documentation Community Group listing](https://www.w3.org/groups/cg/designsystemdocs/)).
Having chairs is the difference between this group and the closed one; its mailing list nonetheless holds a single message ([public-designsystemdocs archive](https://lists.w3.org/Archives/Public/public-designsystemdocs/)).
That is a promising beginning, not a format a project can build on this year.

## Design tokens: DTCG

The Design Tokens Format Module is the one part of this landscape that is genuinely settled.

### Status and standing

The published module is titled Design Tokens Format Module 2025.10 and its status section identifies it as a "Final Community Group Report" ([Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/)).
The same status section states plainly that the document "is not a W3C Standard nor is it on the W3C Standards Track", and that it "was published by the DTCG as a Candidate Recommendation following the definitions provided by the W3C process".
It also states that "this specification is considered stable" and that "further updates will be provided in superseding specifications".

That combination is the correct thing to cite, and it is more useful than a bare version number.
The format is stable enough to adopt and specific enough to validate against, while remaining a Community Group product rather than a W3C Recommendation.
A project that describes DTCG as a W3C standard is overstating its standing; a project that dismisses it as a draft is understating its stability.

The 2025.10 publication is composed of more than one module.
The technical reports index for that version lists Format, Colour, and Resolver modules ([Design Tokens technical reports, 2025.10](https://www.designtokens.org/tr/2025.10/)).
This note is concerned mainly with the Format module, because that is the module that defines the interchange file.

### What the format defines

The Format module states its own scope as "the technical specification for a file format to exchange design tokens between different tools", and notes that "design token files are JSON files that adhere to the structure described in this specification" ([Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/)).
The following capabilities are all defined normatively in that module.

Tokens are JSON objects distinguished by the presence of a `$value` property, and the specification states that "the presence of a `$value` property definitively identifies an object as a token".
Groups are objects without a `$value` property, and the specification is careful to say that "groups are arbitrary and tools SHOULD NOT use them to infer the type or purpose of design tokens".
That warning matters for an accessibility project, because it forbids the tempting shortcut of encoding meaning in folder names.

Types are constrained.
The module states that "this spec defines a number of design-focused types and every design token MUST use one of these types", and the defined types are `color`, `dimension`, `fontFamily`, `fontWeight`, `duration`, `cubicBezier`, `number`, `strokeStyle`, `border`, `transition`, `shadow`, `gradient`, and `typography`.
A group may carry a `$type` that acts as a default for tokens beneath it.

Aliases are first-class.
The module treats "alias" and "reference" as synonyms, and defines a curly-brace syntax that "is specifically designed for referencing complete token values and always resolves to the `$value` property of the target token".
Aliases may reference other aliases, tools "MUST follow each reference until they find a token with an explicit value", references "MUST NOT be circular", and tools "MUST detect and report this as an error affecting all tokens in the circular chain".

JSON Pointer support is also normative, and is more powerful than the curly-brace form.
The module states that "for advanced use cases requiring access to specific properties within token values or other parts of the document structure, tokens MUST support JSON Pointer notation as defined by [rfc6901], using the `$ref` property", and that "tools implementing this specification MUST support JSON Pointer syntax".
Curly braces target complete tokens only; `$ref` can target any document location, including an individual colour component or a token's `$type` metadata.

Descriptions are supported.
The module defines an optional `$description` property as "a plain text description explaining the token's purpose", requires its value to be "a plain JSON string", and lists uses including style-guide previews, IDE tooltips, design-tool tooltips, and generated source-code comments.
Groups may carry a `$description` too.

Deprecation is supported, which is unusual and valuable in an interchange format.
The module states that "the `$deprecated` property MAY be used to mark a token as deprecated, and optionally explain the reason", with `true` meaning deprecated without explanation, a string meaning deprecated with an explanation, and `false` meaning explicitly not deprecated so that a group default can be overridden.
Groups may be deprecated wholesale, and the module states that group deprecation "extends to all child tokens within the group unless explicitly overridden".

Extensions are supported and deliberately fenced off, which is discussed in detail in the next section.

A preferred media type is defined.
The module states that `application/design-tokens+json` "SHOULD be used for design token files", that files "MAY be served using the JSON media type: `application/json`" because every token file is valid JSON, that the more specific type "is preferred and SHOULD be used wherever possible", and that "tools that can open design token files MUST support both media types".

File extensions are recommended rather than required.
The module recommends `.tokens` and `.tokens.json`, and notes that "the former is more succinct".
This project prefers `.tokens.json` because the double extension keeps ordinary JSON editor and validator tooling working without configuration.

### A short token example

The following excerpt shows the features this project actually relies on: typed tokens, a group description, an alias, an explanatory description, and a deprecation with a reason.

```json
{
  "space": {
    "$type": "dimension",
    "$description": "Modular spacing scale. Each step references the previous step.",
    "step-1": { "$value": { "value": 1, "unit": "rem" } },
    "step-2": { "$value": "{space.step-1}" },
    "small": {
      "$value": "{space.step-1}",
      "$description": "Semantic alias for the tightest permitted gap between related controls.",
      "$deprecated": "Use {space.step-1} directly; this alias will be removed in the next major release."
    }
  }
}
```

Read linearly, the excerpt says that `space` is a group of dimension tokens with a stated purpose, that `step-2` is defined by reference to `step-1` rather than by a repeated literal, and that `small` is a semantic alias which is on its way out and says so in machine-readable form.
Nothing in the excerpt asserts anything about contrast, keyboard behaviour, or accessible names, and that is the point of the next section.

## What DTCG cannot express

DTCG solves portable values.
It does not solve portable accessibility contracts, and it does not claim to.

The following facts have no native DTCG representation.

Roles, accessible names, states, and relationships.
There is no token type for "this control exposes role `button`" or "this control's accessible name comes from its visible label".

The keyboard model and focus lifecycle.
There is no way to state that Escape closes a dialog, that Tab is trapped while it is open, that initial focus moves to the first interactive element, or that focus returns to the invoking control on close.

Reflow and forced-colours behaviour.
There is no way to state that a region remains usable at 320 CSS pixels without two-dimensional scrolling, or that a boundary survives forced-colours mode because it is drawn with a transparent outline rather than a background colour.

WCAG criteria and test assertions.
There is no way to attach "this component is responsible for satisfying 2.4.7 Focus Visible" to anything, and no way to express a testable assertion at all.

Assistive-technology evidence.
There is no way to record that a specific screen reader, on a specific browser, at a specific version, on a specific date, announced a specific string.

Non-guarantees and uncertainty.
There is no way to state that a layout primitive provides geometry but deliberately provides no semantics, or that a behaviour is known to vary between engines and has not yet been resolved.

Contrast assertions.
There is no way to say "this foreground token is valid on this background token at 7:1".
This is the sharpest example because it looks like a token concern and is not one.
Contrast is a relationship between two tokens evaluated against a threshold, and DTCG models tokens and references between tokens, not predicates over pairs of tokens.

It is tempting to solve all of this inside `$extensions`.
The specification itself explains why that would be a mistake.
It defines `$extensions` as an object where tools "MAY add proprietary, user-, team- or vendor-specific data to a design token", requires that "tools that process design token files MUST preserve any extension data they do not themselves understand", and then states the governing constraint directly: "in order to maintain interoperability between tools that support this format, teams and tools SHOULD restrict their usage of extension data to optional meta-data that is not crucial to understanding that token's value" ([Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/)).

The preservation rule is exactly what makes extensions unsuitable as a home for accessibility contracts.
A conforming tool is required to carry unknown extension data through untouched, and is not required to understand it, act on it, validate it, or surface it.
An accessibility contract stored only there would round-trip perfectly and mean nothing to anybody.
Silent, lossless, meaningless preservation is the worst possible outcome for a safety-relevant assertion.

The rule for this project follows directly.
Accessibility contracts, WCAG mappings, evidence, non-guarantees, and uncertainty are never stored only in DTCG `$extensions`.
An extension may carry a pointer to the canonical record, because a pointer is genuinely optional metadata that does not change what the token value means.

## Custom Elements Manifest

Custom Elements Manifest is a JSON file format that, in the project's own words, "describes custom elements" so that "tooling and IDEs" can "give rich information about the custom elements in a given project" ([Custom Elements Manifest, getting started](https://custom-elements-manifest.open-wc.org/analyzer/getting-started/)).

### What it carries

A manifest describes a component's programmatic surface.
The documented example fields include attributes with names, types, defaults, and the corresponding class field name; slots with names and descriptions; events with names, types, and descriptions; CSS custom properties with names and descriptions; and CSS parts with names and descriptions ([Custom Elements Manifest, getting started](https://custom-elements-manifest.open-wc.org/analyzer/getting-started/)).
The example manifest also declares a `schemaVersion`, which makes a manifest self-describing about the format it targets.

Manifests are generated rather than written.
The analyser "will scan the source files in your project, and run them through the TypeScript compiler to gather information about your package", proceeding through collect, analyse, module-link, and package-link phases, and it resolves things such as finding a custom element's tag name "by finding its `customElements.define()` call, if present" and "applying inheritance to classes" ([Custom Elements Manifest, getting started](https://custom-elements-manifest.open-wc.org/analyzer/getting-started/)).
The analyser also has "a rich plugin system that allows you to extend its functionality, and add whatever extra metadata you need" ([Custom Elements Manifest analyser plugins](https://github.com/open-wc/custom-elements-manifest/blob/master/packages/analyzer/docs/plugins.md)).

### What it does not carry

A manifest describes the API surface, not the behaviour behind it.
It does not state which ARIA role the component exposes at runtime, how its accessible name is computed, what its keyboard model is, where focus goes when it opens and closes, which WCAG criteria it is responsible for, or what it deliberately does not guarantee.
The plugin system means such information could be attached, but a project-specific plugin field is a private convention, not an interoperable contract.

### Role here

CEM is adopted if and only if this project publishes custom-element primitives, and it is generated from source rather than maintained by hand.
It is the canonical record of the coded API surface, and it is deliberately not the canonical record of the accessibility contract.
Its most valuable governance property is that it is derived: a manifest that disagrees with the code is a build failure rather than a documentation debate.

## Storybook Component Story Format

Component Story Format is described by Storybook as "the recommended way to write stories" and as "an open standard based on ES6 modules that is portable beyond Storybook", in which "stories and component metadata are defined as ES Modules" with "a required default export and one or more named exports" ([Component Story Format](https://storybook.js.org/docs/api/csf/index)).

### What it carries

Every named export "represents a story object by default", and story objects can be annotated with fields for story-level decorators, parameters, and a display name ([Component Story Format](https://storybook.js.org/docs/api/csf/index)).
Stories accept "named inputs called Args", which are "dynamic data that are provided (and possibly updated by) Storybook and its addons", and which Storybook argues make stories "more portable since the code doesn't depend on the actions feature specifically".
Play functions are "small snippets of code executed when the story renders in the UI", and Storybook "executes each step defined in the `play` function and runs the assertions without the need for user interaction".

That is a genuinely useful portability story.
A CSF file is a set of named, parameterised, executable states with optional scripted interactions, expressed in plain ES modules.
For an accessibility project it is close to ideal as a source of test fixtures: each documented state can be rendered, driven, and asserted against automatically.

### What it does not carry, and the warning

CSF is executable fixtures and visual or interaction test material.
It is not a semantic source of truth, and it must never be treated as one.

The reason is that a story is code that produces a rendering.
It can demonstrate that a state exists; it cannot assert why the state exists, which criterion it satisfies, what evidence supports the claim, or what is deliberately not guaranteed.
Worse, a story is trivially able to demonstrate an inaccessible state just as convincingly as an accessible one, because rendering successfully is not the same as being correct.

A design system whose specification is its stories has, in practice, no specification.
It has a gallery.

### Role here

CSF is adopted as the executable layer.
Each state named in a component specification should have a corresponding story, and the direction of authority runs from the specification to the story.
Stories are also the natural place to hang automated checks, including composition tests that render a component inside a realistic page rather than in isolation.

## Open UI

Open UI is a W3C Community Group whose stated purpose is "to allow web developers to style and extend built-in web UI components and controls, such as `<select>` dropdowns, checkboxes, radio buttons, and date/color pickers" ([Open UI](https://open-ui.org/)).
To do that, the group says, "we'll need to fully specify the component parts, states, and behaviors of the built-in controls, as well as necessary accessibility requirements, and provide test suites to ensure compatibility".
The W3C group page describes the same effort as "researching components and controls across the web and also looking to native paradigms to bring interoperability for design systems, frameworks and the web platform" ([Open UI Community Group](https://www.w3.org/community/open-ui/)).

Open UI also states its expectation about design systems explicitly: "we hope to make it unnecessary to reinvent built-in UI controls, but for those who choose to do so, we expect that these design systems will benefit from Open UI's specifications and test suites" ([Open UI](https://open-ui.org/)).

### What it carries and does not carry

Open UI produces specifications, research, and test suites about parts, states, behaviours, and accessibility requirements of controls.
It does not produce a file format in which a third-party design system can serialise its own components.
It is a vocabulary and a body of analysis, not an interchange schema.

### Role here

Open UI is a vocabulary source and an alignment target.
Where Open UI has named a part or a state, this project should use that name rather than inventing a synonym, because shared naming is the cheapest form of interoperability available.
Its accessibility requirements and test suites are also useful prior art for the assertion catalogue this project needs.

## The two most closely aligned W3C Community Groups

Two Community Groups have set out to build something very close to what this project needs.
Their charters are worth reading carefully, and their current status is worth stating honestly.

### UI Specification Schema Community Group

The group's charter is remarkably well aligned with an accessibility-focused design system.
It states that the group "will define a common, implementation-agnostic meta-model for specifying the design, layout, behaviour, and constraints of user interface elements", with the goal "to enable designers, developers, and QA teams to describe any UI component — from buttons to complex composites — in a precise, machine-readable format that can be validated and consumed by tools across web, mobile, desktop, and embedded platforms" ([UI Specification Schema Community Group](https://www.w3.org/groups/cg/uispec/)).

Its stated mission includes defining "the full set of possible specification fields (e.g., geometry rules, responsive behaviours, content constraints, accessibility requirements) that can apply to any UI element", aligning "vocabulary with related W3C efforts such as Open UI (anatomy, states, variants) and the Design Tokens Community Group (styling primitives)", and producing "a formal schema (JSON/JSON Schema) for authoring and validating per-instance specifications of UI elements" ([UI Specification Schema Community Group](https://www.w3.org/groups/cg/uispec/)).
Its deliverables list includes reference example specifications, guidance for integrating with design tokens and component anatomy standards, and "coordination with accessibility, internationalisation, and localisation best practices".

That is, almost line for line, the missing layer identified earlier in this note: a platform-neutral JSON meta-model covering layout, behaviour, constraints, responsive behaviour, and accessibility requirements.

The group's own W3C page, however, records that it "was closed on 2026-05-21", having been "originally proposed on 2025-08-11 by Vasilis Danias" ([UI Specification Schema Community Group](https://www.w3.org/community/uispec/)).

The closure needs to be read carefully, because the obvious reading is wrong.
A group that closes after publishing drafts leaves behind a vocabulary a project can map onto; this group left nothing.
Its launch announcement states that "the UI Specification Schema Community Group has been launched" and is dated August 2025, with no day given ([August 2025 announcement](https://www.w3.org/community/uispec/2025/08/)); the proposal date of 2025-08-11 comes from the group page rather than from the announcement.
Its `public-uispec` mailing list holds zero messages ([public-uispec archive](https://lists.w3.org/Archives/Public/public-uispec/)).
No report, draft, or schema appears in the [W3C Community Group reports index](https://www.w3.org/community/reports/).
The [closed-groups listing](https://www.w3.org/groups/cg/?closed=1) names no successor for it, and it does name successors for other closed groups where one exists, for example directing readers of the W3C Inclusion and Diversity Community Group entry to "join the Positive Work Environment Community Group with which the W3C Inclusion and Diversity Community Group (ID CG) has merged".

One piece of evidence has to be withdrawn here.
An earlier version of this note argued that the page still saying "the group must now choose a chair" was the sentence W3C shows for a group that never organised itself.
That inference does not hold.
The same sentence appears on the [Design System Documentation Community Group page](https://www.w3.org/community/designsystemdocs/), whose W3C listing does name chairs, so the sentence carries no information about whether a group ever organised itself and must not be used as evidence either way.
The empty mailing list and the empty reports index carry the argument on their own.

The charter is therefore the entire output of the group, and it has to be read as a requirements document rather than as a live specification effort.
The practical consequence for this project is narrower than "monitor for alignment" implies: there is no schema to validate against, no field names to adopt, and no mapping table to produce.
What survives is the charter's *scope claim*: that geometry rules, responsive behaviour, content constraints, and accessibility requirements belong in one machine-readable per-element specification. That claim is independent evidence that the gap this project is filling is real and was recognised by someone else at W3C.

No successor group has been announced.
The closed-groups listing records the closure without naming a replacement, unlike other entries there which point readers to the group that took over the work ([Closed Community Groups](https://www.w3.org/groups/cg/?closed=1)).
The nearest new W3C activity in the same broad area is the [Generative UI Community Group](https://www.w3.org/community/gen-ui/), "originally proposed on 2026-01-29 by Ruoxi Ran", but its scope is the runtime synthesis of interfaces (evaluation and performance, validation and testing, intermediate representations, and alignment with the web platform) rather than a portable specification format for authored components.
It is not a successor and should not be recorded as one.

### Design System Documentation Community Group

The second group addresses documentation rather than component semantics.
It states that design-system management "is too often burdensome because institutional knowledge is fragmented and locked into proprietary formats", that this "hurts design system teams, the people who use design systems, and even the people who make tools for design systems", and that these problems "are only becoming more important with agent-driven workflows" ([Design System Documentation Community Group](https://www.w3.org/community/designsystemdocs/)).

Its mission is "to lower the burden of design system management by developing an open format for structuring design system documentation", and it names the facets of openness it cares about: "compatibility with established standards like DTCG and CEM, portability, and providing value to both humans and agents" ([Design System Documentation Community Group](https://www.w3.org/community/designsystemdocs/)).
The launch announcement confirms the same mission statement and that "this group will develop Specifications" ([Proposed Group: Design System Documentation Community Group](https://www.w3.org/community/blog/2026/07/30/proposed-group-design-system-documentation-community-group/)).

The alignment is strong: an open documentation format explicitly designed to compose with DTCG and CEM is the third leg of the bundle this note proposes.

The maturity is low but no longer nominal, and this is the one respect in which it differs decisively from the closed group.
The group page records a proposal date of 2026-07-29, and the group listing now names **Ben Callahan and Afyia Smith as co-chairs** ([Design System Documentation Community Group listing](https://www.w3.org/groups/cg/designsystemdocs/)).
Choosing chairs is precisely the step the UI Specification Schema group never took before it closed.
Activity is nonetheless minimal: `public-designsystemdocs` holds a single message ([public-designsystemdocs archive](https://lists.w3.org/Archives/Public/public-designsystemdocs/)), and no draft has been published.

This is the group to engage with, and engagement means contributing requirements now rather than waiting to consume a format.
The project has something specific to offer it that its charter does not yet mention: assistive-technology evidence, explicit non-guarantees, and recorded uncertainty as first-class documentation fields rather than prose.

### Why these are alignment targets, not dependencies

Neither group currently supplies a schema this project could validate against.
One is closed having published nothing, and the other has chairs but no draft.

The correct posture is therefore to design project-owned formats that are deliberately mappable to these charters' vocabularies, and to treat the charters as a requirements checklist during that design.
That posture keeps two options open at once.
If a standard emerges, the project maps to it and retires its own provisional format.
If no standard emerges, the project still has a validated, documented, portable format rather than a dependency on a group that stalled.

The corollary is that project-specific field names should be chosen to resemble the charter vocabulary of design, layout, behaviour, constraints, responsive behaviour, and accessibility requirements, rather than to be clever.

## Commercial and de facto ecosystem

Standards describe what could be exchanged.
Products determine what actually is exchanged.
This section surveys the tools a real design system will meet, and for each one asks the same two questions: what does it represent portably, and where does the portability stop.

### Figma

Figma's variables are the closest thing the tool has to tokens.
Figma documents variables as "raw values—like color, numbers, and strings—that can change in value depending on the context of a design, such as light and dark modes, or mobile and desktop modes" ([Overview of variables, collections, and modes](https://help.figma.com/hc/en-us/articles/14506821864087-Overview-of-variables-collections-and-modes)).
The same page documents aliasing directly, saying that a variable can reference another variable and that this "gives you the ability to implement design tokens".
Variables come in six documented types (colour, number, string, boolean, timing, and easing), and "any variable can reference another variable of the same type".

Portability stops in several documented places.
The variables overview does not document any file-based import or export format for variables at all.
Programmatic access exists through the Variables REST API, which "includes endpoints for querying, creating, updating, and deleting variables", but Figma states that "to use this API, you must have a Full seat in an Enterprise org; guests cannot use the API" ([Figma Variables REST API](https://developers.figma.com/docs/rest-api/variables/)).
There are also modelling limits: "you can create up to 5,000 variables per collection", and "the number of modes you can create per collection depends on your plan" ([Overview of variables, collections, and modes](https://help.figma.com/hc/en-us/articles/14506821864087-Overview-of-variables-collections-and-modes)).

More importantly, the six variable types are not the thirteen DTCG token types, so a Figma-to-DTCG mapping is a genuine transformation with judgement in it rather than a rename.

### Figma Dev Mode and Code Connect

Code Connect is often mistaken for a component interchange format.
Figma describes it accurately as "a bridge between your codebase and Figma's Dev Mode, connecting components in your repositories directly to components in your design files" ([Code Connect](https://help.figma.com/hc/en-us/articles/23920389749655-Code-Connect)).
Its purpose is that "Figma's Dev Mode will display true-to-production code snippets from your design system instead of autogenerated code examples", and it "also supports mapping properties from code to Figma enabling dynamic and correct examples" ([figma/code-connect](https://github.com/figma/code-connect)).
It supports several implementation targets, illustrated by Figma's own example that "you can connect one Button component to its React, SwiftUI, Jetpack Compose, and Vue implementations".
It is labelled "Available on the **Organization and Enterprise plans**" and "Requires a Full or Dev seat" ([Code Connect](https://help.figma.com/hc/en-us/articles/23920389749655-Code-Connect)).
An earlier version of this note quoted that requirement as "a full Design or Dev Mode seat", which is not what the page says; the wording above is what appears on it.
Figma also documents that once components are mapped, "this information is shared with the Figma MCP server" and is "included in the design context sent to AI agents" ([Code Connect](https://help.figma.com/hc/en-us/articles/23920389749655-Code-Connect)).

That is valuable and it is not a schema.
Code Connect carries a mapping from a Figma component to a code snippet, plus property mappings and instructions.
It does not define a vendor-neutral semantic model of a component, it does not express keyboard contracts or WCAG responsibility, and it is gated by plan and seat.
Treating Code Connect as the component contract would make an accessibility contract readable only inside a paid seat in one vendor's product.

### Tokens Studio

Tokens Studio is the most direct route between Figma and DTCG files.
Its documentation states that "in support of moving towards the W3C Specifications for Design Tokens, as managed by the Design Tokens Community Group (DTCG), you can choose a Design Token Format (how tokens are written in their JSON files) from within the Tokens Studio Plugin", that "the plugin will convert your token JSON files to the format of your choice", and that the DTCG format "prefixes the properties of a design token in the JSON file with the dollar sign (`$`)" ([Tokens Studio token format](https://docs.tokens.studio/manage-settings/token-format)).
It supports tokens stored locally in a Figma file or remotely via a sync provider, and "for Git sync providers, different branches can have different Token Formats".

Portability stops at the format switch.
Tokens Studio documents that "the default is `legacy format`", so a project must actively choose DTCG rather than assume it ([Tokens Studio token format](https://docs.tokens.studio/manage-settings/token-format)).
Format conversion between a legacy model and DTCG is a transformation, and a project should treat the DTCG file in its own repository as canonical rather than the plugin's internal state.

### Penpot

Penpot is the open-source design tool with the strongest explicit standards commitment.
Its documentation states that "Penpot Design Tokens adhere to the Design Tokens Format Module and its definitions, a draft by the W3C DTCG", that "Penpot ensures compatibility across various disciplines, tools, and technologies by following the most standardized approach available for design tokens", and that "tokens can be exported from Penpot or integrated into other tools directly, without conversion" ([Penpot design tokens](https://help.penpot.app/user-guide/design-systems/design-tokens/)).
Import and export work with a single JSON file, multiple JSON files in a folder structure, or a `.zip` archive, and token definitions use `$value`, `$type`, and `$description`.
Penpot also makes the portability argument in governance terms: "the knowledge gained from using Design Tokens in Penpot remains valuable, regardless of whether you continue using Penpot or a different tool or technology".

Portability stops at tokens.
Penpot's token work is genuinely standards-based, but it is still token values rather than component semantics, keyboard contracts, or evidence.
Note also that Penpot's documentation describes the Format Module as a draft, which is a reasonable description of an earlier state but is now behind the published Final Community Group Report status.

### Sketch

Sketch supports token export from its shared styles.
Its changelog records that "in addition to Color Tokens, you can now export Layer Styles and Text Styles as Design Tokens — right from the web app", and that "you can download your design tokens, or create an always-up-to-date public link for them" ([Sketch design tokens export](https://www.sketch.com/changelog/design-tokens/)).
Sketch also markets developer handoff as inviting developers to "inspect designs, download assets and get tokens" ([Sketch developer handoff](https://www.sketch.com/handoff/)).

Portability stops at an unstated format.
The changelog entry does not state which token format the export produces, so a project cannot assume DTCG conformance without testing the output.
Third-party exporters exist and target other conventions entirely; one documents producing "a `design-tokens.json` file compatible with Amazon Style Dictionary" ([Sketch design tokens exporter](https://github.com/icona79/sketch-design-tokens-exporter)).
That is a reminder that "exports design tokens" is a claim about a feature, not about a format.

### Material Design and Material Theme Builder

Material Theme Builder is the clearest example of multi-platform token generation with real adapter losses.
Google describes it as a tool to "visualize Material You's dynamic color and create a custom Material Design 3 theme", and documents that it "exports design tokens directly as a Design Systems Package (DSP), and theming code for our Material 3 libraries on Android Views and Jetpack Compose", with exports "to multiple formats: Android Views (XML), Jetpack Compose (Kotlin) and Design System Package (DSP)" ([Introducing Material Theme Builder](https://m3.material.io/blog/material-theme-builder)).
Material also documents the Figma plugin route for migrating to the Material 3 colour system ([Customising Material](https://m3.material.io/foundations/customization)).

Portability stops in two instructive ways.
The documented export formats are DSP, Android XML, and Kotlin, not DTCG.
And the tool documents an explicit loss: of the surface tonal colours it displays, "these surface tonal colors are not exported in the code" ([Introducing Material Theme Builder](https://m3.material.io/blog/material-theme-builder)).
That is exactly the class of silent adapter loss this project must require adapters to report.

### Salesforce Lightning Design System

SLDS is the longest-running enterprise example of token governance, and it is currently the best available case study in token migration.
Salesforce defines design tokens as "named entities that store visual design attributes, such as margins and spacing values, font sizes and families, or hex values for colors", and documents that "lightning web components can use any SLDS 1 design token marked Global Access" ([SLDS design tokens](https://developer.salesforce.com/docs/platform/lwc/guide/create-components-css-design-tokens.html)).
The migration is documented plainly: "the SLDS design tokens are still present and work normally in SLDS 1 themes, but aren't included in SLDS 2 themes", because "SLDS 2 replaces design tokens with a system of CSS custom variables called global styling hooks", and the older `--lwc-` camelCase reference syntax "works in SLDS 1, but not SLDS 2".
Salesforce also documents an accessibility motive for the change, recommending global colour styling hooks to align with WCAG 2.1 colour-contrast requirements.

Portability stops at the platform boundary.
Global styling hooks are CSS custom properties, which is a fine runtime mechanism and not an interchange format.
The lesson for this project is less about SLDS's format and more about its versioning discipline: a token system needs a documented deprecation and migration path, which is precisely why DTCG `$deprecated` is worth using from the start.

### Adobe Spectrum

Spectrum is notable for publishing structured design data rather than only documentation.
Adobe describes Spectrum Design Data as "API documentation, design tokens, and registry for Spectrum, Adobe's design system", with sections for Components as "component API schemas (properties, types, defaults)", Tokens as "design tokens (color, typography, layout, etc.)", and a Registry of "design system terminology (sizes, states, variants, glossary)" ([Spectrum Design Data](https://opensource.adobe.com/spectrum-design-data/)).
The token documentation describes tokens as "design decisions, translated into data" acting as "a 'source of truth' to help ensure that product experiences feel unified and cohesive" ([Spectrum design tokens](https://spectrum.adobe.com/page/design-tokens/)), and the token registry distinguishes semantic colour aliases from component-specific colour tokens ([Spectrum tokens](https://opensource.adobe.com/spectrum-design-data/tokens/)).

Portability stops at the vendor's own model.
A published component API schema and a terminology registry are more than most vendors offer, and they are still Adobe's schema for Adobe's system rather than a neutral interchange format.
The registry idea is nonetheless worth borrowing: a project-owned vocabulary of states, sizes, and variants is a cheap and effective way to prevent naming drift.

### Zeroheight

Zeroheight is a documentation product that has grown a token manager.
It documents a top-level token area used to "centralise" an organisation's tokens, and states that "zeroheight's token export uses Style Dictionary, a powerful build system to transform tokens into any format", that "exports can be manually downloaded, accessed via an API to allow you to automate this process and integrate zeroheight into your developer workflows", and that "you can export your token set in the W3C format, which can be useful for transferring to other tools" ([Exporting and integrating design tokens into developer pipelines](https://help.zeroheight.com/hc/en-us/articles/35887016596123-Exporting-and-integrating-design-tokens-into-developer-pipelines)).
Import routes include syncing with a code repository and creating tokens from Figma styles or variables ([Importing design tokens](https://help.zeroheight.com/hc/en-us/articles/35887045316507-Importing-design-tokens)).

Portability stops at composite tokens and at prose.
Zeroheight documents that platform-specific export formats do not support composite tokens, which is a real loss for typography and shadow tokens.
And the documentation pages themselves (the guidance, rationale, and accessibility notes that give a design system its value) live in the product's own content model rather than in a portable format.

### Supernova

Supernova positions itself as documentation plus code automation.
It states that users can "export code for any platform that describes design system elements, such as tokens, components, themes, or documentation", that it can "deliver code to multiple platforms at the same time", and that its Pulsar technology lets teams "describe how the code generation should behave in regard to any codebase", with export available automatically through Design Continuous Deployment or "manually and locally within your development environment" ([Supernova guide to code integration](https://learn.supernova-docs.io/latest/code-integration/guide-to-code-integration-n7UChYuk)).
Its onboarding documents connecting Figma files, syncing tokens through a Tokens Studio integration, and importing Figma variables ([Welcome to Supernova](https://learn.supernova.io/latest/getting-started/welcome-to-supernova-Jocg9JuY)).

Portability stops at a generator, not a format.
"Export code for any platform" is an outbound transformation capability; it does not imply that the design system's own semantics are stored in a neutral, re-importable schema.
The documented specific export formats are not enumerated on the code-integration page, which is itself a portability caution.

### Knapsack

Knapsack presents itself as a shared system of record.
Its documentation says Knapsack "gives your team one place to collaborate on design and code", that "designers, developers, product folks, writers, and accessibility specialists all work from the same playbook", and that "our content blocks dynamically display design tokens, variables, and live components exactly as they appear in your products" ([Knapsack documentation](https://docs.knapsack.cloud/)).
Documented import routes include Figma, a Figma variables plugin, Tokens Studio, and Style Dictionary: "bring your design elements from Figma, Tokens Studio, or Style Dictionary into one place".

Portability stops on the way out.
The documentation describes rich import and display, and does not document a corresponding export format for the aggregated model.
A platform that is excellent at consuming everything and quiet about emitting anything is a good consumer and a poor canonical store.

### Backlight

Backlight is the most explicitly exit-friendly product in this survey.
It states that "Backlight promotes 100% standard web development technologies" and, unusually, that "you are free to eject your design system and continue outside of Backlight at any time" ([Backlight features](https://backlight.dev/features)).
It documents Storybook stories, Style Dictionary support that lets teams "define styles once then export to all the places you need them - iOS, Android, CSS, JS, HTML, Figma files, style documentation", documentation authored in Markdown, MDX2, MD Vue, MDsveX, or Nunjucks, publishing to any npm registry, and collaboration through GitHub and GitLab.
Backlight also describes building component libraries "in isolation using the Component Story Format from Storybook" ([Best design system tools](https://backlight.dev/mastery/best-design-system-tools)).

Portability stops, as everywhere, at semantics and evidence.
Backlight's ejectability is a genuine architectural virtue and is the model other vendors should be measured against.
It is achieved by using portable underlying formats (files, stories, Markdown, npm packages), which is the same strategy this note recommends at the repository level.

### Style Dictionary

Style Dictionary is the transformation layer most of these products share, and it deserves a note of its own because it is where DTCG conformance is actually tested.
It describes its purpose as exporting "your Design Tokens to any platform - iOS, Android, CSS, JS, HTML, sketch files, style documentation" ([Style Dictionary](https://styledictionary.com/)).
On DTCG it states that "as of version 4, Style Dictionary has first-class support for the DTCG format", and documents a converter from its own v3 JSON format that renames `value` to `$value`, `type` to `$type`, and `description` to `$description` ([Style Dictionary and the Design Tokens Community Group](https://styledictionary.com/info/dtcg/)).

It also documents a caveat that any project adopting the newest module must plan for: "the latest format 2025.10 does not have full support yet in Style Dictionary", and "this is a work in progress in v5" ([Style Dictionary and the Design Tokens Community Group](https://styledictionary.com/info/dtcg/)).
That single sentence is the practical reason a project must validate its own token files against the published module rather than trusting that a build tool's acceptance implies conformance.

## Governance conclusion

A commercial platform can be an excellent adapter or an excellent consumer.
It must not be the only repository for accessibility contracts, rationale, evidence, or migration information.

The reasoning is not ideological.
It follows from what the products themselves document.
Figma's variables API requires an Enterprise full seat, Code Connect requires an Organization or Enterprise plan and a paid seat, Material Theme Builder silently omits surface tonal colours from its exports, Zeroheight's platform exports drop composite tokens, Style Dictionary does not yet fully support the newest DTCG module, and several documentation platforms document rich import with no documented export of the aggregated model.
Each of those is a reasonable product decision.
Together they mean that any fact stored only inside one of these products has an availability, licensing, and fidelity risk attached to it.

For most design systems that risk is commercial inconvenience.
For an accessibility-focused design system it is a safety problem, because the facts at risk are the ones that determine whether disabled users are excluded.
An accessible name computation, a focus-return rule, a forced-colours behaviour, a non-guarantee, and an engine-qualified screen-reader observation are all assertions someone will need to re-verify, cite, or defend years later, possibly after the vendor relationship has ended.

Figma Code Connect deserves to be named specifically because it is the most frequently over-claimed artefact in this space.
It is a bridge between Figma and a codebase, and Figma's own documentation describes it exactly that way ([Code Connect](https://help.figma.com/hc/en-us/articles/23920389749655-Code-Connect)).
It is not a vendor-neutral semantic component schema, and no amount of property mapping turns it into one.

## The proposed portable bundle

The repository-level layout below is the concrete form of the bundle.
It is deliberately boring: directories of files under source control, each with one clear kind of authority.

```text
design-system.manifest.json   Links canonical artefacts; declares versions and identifiers
tokens/                       DTCG JSON sources (.tokens.json), themes, aliases
components/                   Markdown specs + structured component contracts + stories + tests
manifests/                    Generated Custom Elements Manifest output
patterns/                     Multi-component and page-level specifications
evidence/                     AT matrix, Reflow results, known limitations
adapters/                     CSS, Electron, Figma, Penpot, native targets
docs/                         Colophon, decisions, research
```

Each part has a defined responsibility, and the responsibilities do not overlap.

`design-system.manifest.json` is the index and nothing more.
It declares the system's version, the DTCG version its token files target, the stable identifier of each approved component, and the path to each canonical artefact.
It must not restate token values, contract text, or evidence, because a manifest that duplicates content becomes a second source of truth that drifts.

`tokens/` holds the canonical token values as DTCG files using the `.tokens.json` extension.
Aliases express relationships between scale steps and semantic names, `$description` carries purpose, and `$deprecated` carries migration information.
These files are validated in continuous integration against the declared DTCG version.

`components/` holds, for each approved component, a human-readable Markdown specification and a machine-readable component contract, alongside its stories and tests.
The Markdown is where rationale, cost, and rejected alternatives live, in the same shape used by the colophon.
The contract is where roles, names, states, keyboard model, focus lifecycle, WCAG mapping, assertions, non-guarantees, and uncertainty live in validatable form.

`manifests/` holds generated CEM output.
It is build output under review, not hand-authored source, and a mismatch with the code is a failure rather than a discussion.

`patterns/` holds specifications that span components, because most real accessibility failures are compositional.
Error summaries, focus management across a multi-step flow, and heading structure in a realistic page all belong here rather than in any single component's file.

`evidence/` holds engine-qualified observations.
Each record names the assistive technology, the browser, both versions, the date, the story or fixture used, the observed behaviour, and the resulting status.
Known limitations and unresolved uncertainty live here too, as first-class records rather than as caveats buried in prose.

`adapters/` holds every outbound and inbound transformation, and each adapter is required to emit a report.
The report states what it mapped, what it approximated, what it could not represent, and what it dropped.
An adapter that cannot report its losses is not finished.

`docs/` holds the colophon, decision records, and research notes, including this one.

## The governance rule

No adapter is canonical.

Figma, Penpot, Style Dictionary, framework bindings, and native platform outputs consume or map project-owned sources.
They never become the sole authority for a fact owned by tokens, code APIs, component contracts, or evidence.

Stated as a test that can be applied to any proposed integration: if the vendor's product were unavailable tomorrow, which facts would the project no longer be able to state or defend?
If the answer is any fact about accessibility, the integration is designed wrongly and must be restructured so that the project holds the source and the vendor holds a copy.

The rule cuts in both directions.
An inbound adapter that reads Figma variables must write into `tokens/` through a reviewed change, not become a live read-through dependency.
An outbound adapter that generates CSS custom properties or native resources must be reproducible from `tokens/` alone, so that the generated artefact can always be regenerated and never has to be trusted on its own.

## A provisional component-specification format

The following example shows how an accessibility contract could be expressed in machine-readable form.
It is provisional.
It is a project draft used to test whether the required facts can be expressed at all, and it is explicitly intended to be mapped onto a future standard, or contributed as requirements to one, rather than defended as terminology.

```json
{
  "$schema": "https://example.invalid/afds/component-contract-0.1.json",
  "id": "afds.component.dialog",
  "version": "0.1.0",
  "status": "draft",
  "semanticModel": {
    "role": "dialog",
    "modal": true,
    "accessibleName": {
      "source": "aria-labelledby",
      "target": "the visible dialog heading",
      "fallback": null
    },
    "requiredRelationships": [
      "aria-labelledby references the heading element inside the dialog",
      "aria-describedby references the primary body text when a description is required"
    ],
    "states": ["closed", "opening", "open", "closing"]
  },
  "keyboardContract": [
    { "key": "Escape", "when": "open", "behaviour": "Closes the dialog and returns focus to the invoking control" },
    { "key": "Tab", "when": "open", "behaviour": "Moves focus to the next focusable element within the dialog only" },
    { "key": "Shift+Tab", "when": "open", "behaviour": "Moves focus to the previous focusable element within the dialog only" }
  ],
  "focusLifecycle": {
    "onOpen": "Focus moves to the first focusable element, or to the dialog container if none exists",
    "whileOpen": "Focus is confined to the dialog subtree",
    "onClose": "Focus returns to the element that invoked the dialog",
    "onInvokerRemoved": "Focus moves to a documented fallback container and is announced"
  },
  "wcagMapping": [
    { "criterion": "2.1.2", "name": "No Keyboard Trap", "responsibility": "component" },
    { "criterion": "2.4.3", "name": "Focus Order", "responsibility": "component" },
    { "criterion": "2.4.7", "name": "Focus Visible", "responsibility": "shared", "sharedWith": "tokens and adapters" },
    { "criterion": "1.4.10", "name": "Reflow", "responsibility": "shared", "sharedWith": "layout primitives" }
  ],
  "assertions": [
    { "id": "dialog.role.exposed", "type": "static", "assert": "Computed role is dialog with aria-modal=true" },
    { "id": "dialog.escape.closes", "type": "keyboard", "assert": "Escape closes and focus returns to the invoker" },
    { "id": "dialog.reflow.320", "type": "layout", "assert": "Usable at 320 CSS pixels width without two-dimensional scrolling" },
    { "id": "dialog.forcedcolours.boundary", "type": "layout", "assert": "Dialog boundary remains visible in forced-colours mode" }
  ],
  "nonGuarantees": [
    "Does not provide heading structure for its own content; the consumer supplies headings",
    "Does not guarantee that content inside the dialog meets contrast requirements",
    "Does not manage focus for nested dialogs; nesting is out of scope"
  ],
  "uncertainty": [
    {
      "id": "dialog.name.announcement.variance",
      "description": "Announcement of the accessible name on open varies between screen readers",
      "status": "open",
      "nextAction": "Extend the evidence matrix to a third engine before making a claim"
    }
  ],
  "evidence": [
    {
      "assertion": "dialog.escape.closes",
      "engine": "screen reader X",
      "engineVersion": "0.0.0",
      "browser": "browser Y",
      "browserVersion": "0.0.0",
      "platform": "platform Z",
      "date": "2026-08-29",
      "fixture": "components/dialog/dialog.stories.ts#Modal",
      "observed": "Dialog closed and focus returned to the invoking button",
      "result": "pass"
    }
  ]
}
```

The example is worth reading as a set of deliberate choices rather than as a schema proposal.

The component has a stable identifier and its own version, so that a contract can be cited and diffed independently of the release that contains it.
The semantic model separates the role from the mechanism that produces the accessible name, because "has a name" and "gets its name from `aria-labelledby` pointing at the visible heading" are different claims and only the second is testable.
The keyboard contract is a list of key, state, and behaviour triples rather than prose, so that each row can generate a test.
The focus lifecycle is separated from the keyboard contract because focus movement on open, during, and on close is a different concern from key handling, and because the awkward case (the invoker being removed while the dialog is open) needs somewhere to be stated.

The WCAG mapping assigns responsibility rather than merely listing criteria.
A criterion can be owned by the component, shared with tokens, adapters, or layout primitives, or owned elsewhere entirely, and recording which is what prevents the familiar situation where every layer assumes another layer handled it.

Assertions are typed by the kind of test that settles them: static semantics, keyboard, or layout.
Non-guarantees are a required field rather than an optional note, because an unstated non-guarantee is read as a guarantee by everyone downstream.
Uncertainty is a structured record with a status and a next action, so that an open question is tracked rather than forgotten.

Evidence is engine-qualified and dated, and points at the exact fixture used.
The version numbers in the example are deliberately placeholders, because a fabricated version in an evidence record is worse than an empty one.
An evidence record without an engine, a version, and a date is not evidence; it is a rumour with formatting.

## Anti-patterns

The table below lists the failure modes this note is intended to prevent.
Each row states what the anti-pattern looks like in practice and what specifically breaks as a result.

| Anti-pattern | What it looks like | What breaks |
| --- | --- | --- |
| Design tool as source of truth | The Figma library is the definitive statement of the system; code and docs are described as reflections of it | Accessibility semantics, rationale, and evidence become unreadable without a paid seat in one vendor's product, and cannot be validated, diffed, or defended after the vendor relationship ends |
| Accessibility contracts in token extensions | Roles, keyboard behaviour, or contrast assertions stored under `$extensions` in `.tokens.json` files | DTCG requires conforming tools only to preserve extension data, not to understand or act on it, so the contract round-trips perfectly while meaning nothing to any consumer |
| Stories as specifications | The Storybook instance is the documentation; a state exists because a story renders it | Nothing records why the state exists, which criterion it satisfies, what evidence supports it, or what is not guaranteed, and an inaccessible state renders just as convincingly as an accessible one |
| Flattened one-off JSON export | A single hand-built export bundles resolved token values, component lists, and notes into one bespoke file | Aliases, deprecation, provenance, and the distinction between value, assertion, and observation are all lost, and the file is a snapshot that immediately begins to drift from the sources it summarised |
| Adapters that silently drop meaning | A transform runs cleanly, emits no report, and quietly omits what it could not represent | Losses are discovered by users rather than by continuous integration, and the system claims parity across platforms that it does not have |
| AT evidence in untracked spreadsheets | Screen-reader results live in a shared spreadsheet with no engine versions, dates, or fixture references | Claims cannot be reproduced, regressions cannot be detected, stale results are cited as current, and the project's strongest accessibility evidence becomes its least trustworthy artefact |
| Manifest that duplicates content | The top-level manifest restates token values or contract text "for convenience" | Two sources of truth exist for the same fact and diverge, and consumers cannot tell which one is authoritative |
| Treating a Community Group Report as a Recommendation | Documentation describes DTCG as a W3C standard | Overstated standing invites overconfidence in cross-tool fidelity, when the format's own status section says it is not on the W3C Standards Track |

## Recommendations

1. Adopt DTCG for token files now, citing the published [Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/) and describing it accurately as a stable Final Community Group Report rather than a W3C Recommendation.
2. Use the `.tokens.json` extension, with aliases for scale and semantic relationships, `$description` on every token and group, `$deprecated` with an explanatory string for anything being retired, source control for all token files, and schema validation in continuous integration against the declared DTCG version.
3. Pair a human-readable Markdown specification with a JSON-Schema-validatable component-contract format, so that rationale is readable by people and contracts are checkable by machines, with neither duplicating the other.
4. Generate a Custom Elements Manifest if and when custom-element primitives ship, produce it from source with the analyser rather than by hand, and treat any divergence between manifest and code as a build failure.
5. Use Storybook CSF as executable fixtures and interaction-test material, never as semantic truth, with authority always running from the component specification to the story.
6. Introduce a minimal `design-system.manifest.json` whose only job is to link canonical artefacts and declare versions and identifiers, and refuse any proposal to move content into it.
7. Keep Figma and Penpot integrations behind explicit adapters in `adapters/`, each emitting a report of mappings, approximations, unsupported features, and losses, with no live read-through dependency on a vendor's model.
8. Make engine-qualified assistive-technology evidence, non-guarantees, and uncertainty first-class portable records from the outset, rather than retrofitting them once claims are already being made.
9. Contribute requirements to the [Design System Documentation Community Group](https://www.w3.org/community/designsystemdocs/), follow [Open UI](https://open-ui.org/) for anatomy and state vocabulary, and read the closed [UI Specification Schema Community Group](https://www.w3.org/community/uispec/) charter as a requirements checklist, designing project formats to be mappable onto whatever vocabulary emerges while depending on none of them.

Recommendation 9 changed shape once the UI Specification Schema group's closure was checked properly, and the reasoning is worth keeping visible.
An earlier version of this note told the project to "follow" that group and watch for a successor.
That instruction was unactionable: the group published nothing, no successor has been announced, and "watch for a successor" is a standing task no one can ever complete or close.
It has been replaced by a single live target.
The Design System Documentation Community Group has chairs, an explicit DTCG and CEM compatibility goal, and no draft yet, which is exactly the window in which contributing requirements is more useful than consuming a format.
Open UI remains the only genuinely active vocabulary source in this area.
The closed charter stays in the note as a checklist, not as a dependency.

## Next research tasks

1. Define the component-contract JSON Schema properly, and settle it by validating the Dialog, Disclosure, and Tabs contracts against it with no field left as free prose that a test needs.
2. Design the evidence record format, and settle it by demonstrating that a single assertion tested on two engines produces two comparable, dated, reproducible records that a report can diff across releases.
3. Specify a contrast-assertion representation that expresses a foreground token, a background token, a threshold, and a result, and settle it by deciding whether it lives in the component contract, a separate assertions file, or a proposed DTCG extension, with the reasoning recorded.
4. Test DTCG round-tripping in practice across Tokens Studio, Penpot, and Style Dictionary v4 or v5, and settle it by producing a documented loss report for each path, including whether composite types and the 2025.10 module survive.
5. Prototype the adapter loss report format, and settle it by running one real Figma-variables import and one CSS-custom-property export and confirming that every approximation and omission appears in the report.
6. Map the project's provisional field names onto Open UI's part and state vocabulary and onto the UI Specification Schema charter's section names, and settle it by producing a mapping table with unmapped fields explicitly justified. The charter names scope areas rather than fields, so expect the mapping to be coarse and record where it cannot be made precise.
7. Decide the component-identifier and versioning scheme, and settle it by demonstrating that a contract, a story, an evidence record, and a manifest entry can all be joined by identifier alone, and that a breaking contract change is detectable from version metadata.

## Relationship to the adopted decision

This research is the basis of the adopted colophon decision recorded as "AFDS uses a portable bundle, not a monolithic format" in the project [colophon of decisions](../docs/COLOPHON.md).
That entry states the decision, its reasoning, its cost, the alternatives rejected, and how it is verified.
This note supplies the evidence behind it, and should be updated rather than replaced if the standards landscape moves.
The two changes that would matter most are the Design System Documentation Community Group publishing a draft format, which would turn a contribution target into a mapping target, and a new group chartering the per-element specification work the UI Specification Schema group never started.

The group statuses in this note were last checked on 2026-08-30.
The Code Connect seat requirement, the uispec launch announcement, the closed-groups successor convention, the Tokens Studio default, and the Sketch exporter output were re-checked on 2026-08-31 while writing the companion site page, and the corrections recorded above came out of that pass.

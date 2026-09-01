<!--
SPDX-License-Identifier: CC-BY-SA-4.0
Copyright (c) 2026 Bob Dodd
-->

# AFDS specification, version 1.0.0

This document specifies an Accessibility Focused Design System.
It defines what such a system contains, what each part of it means, what a component is obliged to declare about itself, how the evidence behind those declarations is recorded, and how the whole is serialised as a portable package that another organisation can read.

An AFDS exists so that an accessibility decision, its reasoning, and the evidence for it can be made once and then travel, instead of being rediscovered on every screen that needs it.

## Status of this document

AFDS 1.0.0 is a project draft.
It is not a W3C standard, not a published industry specification, and not on any standards track.
Every identifier and field name defined here is stable within this project and unstable outside it.

The project intends to monitor and seek alignment with the W3C Design System Documentation Community Group, Open UI, and future Design Tokens Community Group work.
The W3C UI Specification Schema Community Group was previously named as an alignment target.
That group closed on 2026-05-21 without publishing a schema, so its charter is now read as a requirements input rather than as a vocabulary to align to.

This document supersedes `AFDS-PACKAGE-FORMAT.md`, which becomes Part IV.
The earlier document remains in the repository until Part IV is complete, and where the two disagree during that period the earlier document governs the package format and this one governs everything else.

### Normative and informative material

Clause 4, clause 5, and Parts II and IV are normative.

Part III is normative only for a package that claims the relevant method profile, and has no force over a package that does not.

Clause 1, clause 2, clause 3, clause 6.2, and the annexes are informative.
They explain why the normative clauses say what they say.
Nothing in them creates a requirement, and a package cannot fail to conform by disagreeing with them.

### Organisation

The document is one specification in four parts.

Part I, clauses 1 to 6, states what an AFDS is, why it exists, the model it assumes, how conformance works, and the terms and references the rest of the document depends on.

Part II defines the component contract: what a component declares, how its semantics and behaviour are constrained, and the records that make a declaration checkable.

Part III defines the method profiles, which carry this project's own choices about layout, reflow, colour, typography, and the component catalogue.

Part IV defines serialisation: the container, the two root artefacts, the verification algorithm, security requirements, adapters, profiles, and versioning.

Clause numbers are global and permanent within a version.
Clause 23 is clause 23 wherever it is rendered, so a citation never has to name a part or a page.
When this document is published as a set of web pages, each clause carries a stable anchor derived from its number, and the split into pages carries no meaning.

## Part I. Purpose and model

### 1. Scope

#### 1.1 What this specification defines

This specification defines:

- the layers a design system is composed of, and what belongs in each;
- what a component declares about itself, including what it refuses to promise;
- the record types that carry evidence, uncertainty, and machine-checkable assertions;
- the keyboard contract model, and the sense in which keyboard operation is not only about keyboards;
- the levels at which conformance is tested, and the difference between a component conforming and a composition conforming;
- a set of named method profiles carrying a layout method, a reflow policy, a colour and typography policy, and an approved component catalogue;
- a container and package hierarchy for carrying all of the above between organisations, with a verification algorithm and security requirements;
- adapter obligations in both directions, and the report an adapter must produce;
- versioning behaviour for the format and for the payload.

#### 1.2 What this specification does not define

This specification does not define the internal schema of a design-token file.
That is the business of the Design Tokens Format Module, and a package declares which version of it applies.

It does not define a visual style, a brand, or a set of palette values, except within a method profile that a package may decline to claim.

It does not define a signature format, a package registry, an update protocol, or an editing tool.

It does not define an implementation language, a component framework, or a rendering engine.
A conforming package may contain an implementation, and may contain none.

It does not make a service accessible.
Clause 2.5 states that limit and its reasons, because a specification that left it implied would be making a claim it cannot support.

#### 1.3 Audience

There are three audiences, and they need different things from the document.

The author of a tool that produces or consumes AFDS packages needs Part IV and the record definitions in Part II.

The designer or engineer adopting the system inside an organisation needs Parts I to III, and will find the obligations that affect daily work in Part II.

The reviewer deciding whether a package conforms needs clause 4, which says what a conformance claim consists of, and the verification algorithm in Part IV.

#### 1.4 Relationship to earlier project documents

The project's research notes, its colophon of decisions, and its register of open questions are not part of this specification.
They record how the decisions here were reached, which decisions were rejected, and what remains unsettled.
A reader who wants to know why a requirement exists will find the argument in clause 2 and the decision record in the colophon.

Where this specification is silent on something the project has not decided, that silence is deliberate and the open-questions register names it.
A silence in a specification is not permission.

### 2. Purpose

This clause is informative.
It states the problem I am trying to solve, because a requirement whose purpose is not stated tends to be obeyed literally and defeated in spirit.

#### 2.1 The problem

Consider how design work happens without a system.

A designer needs a warning message, so they choose an orange, a spacing value, and an icon.
Three weeks later another designer needs a warning message on a different screen, and chooses a slightly different orange and slightly different spacing.
A developer implements both, writing the colour twice.
A tester finds that one of the two oranges fails contrast against its background, files a bug against that one screen, and the other screen keeps its failing orange because nobody knew the two were related.
Six months later the brand changes, and somebody has to find every orange by searching the codebase.

Nothing in that story is incompetence.
It is what happens when a decision has nowhere to live except inside the artefact that used it.

A design system gives each decision a home, a name, and a version.
That is the whole of the mechanism, and everything in this document follows from wanting it to hold for accessibility decisions specifically.

#### 2.2 Why accessibility is the reason this system exists

Most design systems treat accessibility as a quality that components can have.
This specification treats it as the thing the system is for, and that changes what the system has to record.

Accessibility work is commonly retrofitted: build, audit late, patch individual findings, repeat.
That cycle treats symptoms, because a finding fixed on one page recurs on the next page that uses the same component.
Attaching requirements to reusable components and patterns instead means a fix and its reasoning propagate to everything built from them.

There is survey evidence for the shift.
Putnam, Rose and MacDonald analysed 58 interview sessions with user-experience practitioners between 2017 and 2020.
Design systems were the most cited of the four concrete actions the paper identifies, named in 28 sessions (48%), and adoption rose across the fieldwork from 2 of 6 sessions in 2017 (33%) to 22 of 42 between November 2019 and March 2020 (52%).
In the same research, the inclusion of people with disabilities in usability testing was cited in 18 sessions (31%), training in 7 (12%), and code considerations in 5 (8%).

Two findings in that same paper constrain what I may claim from it, and this specification records them rather than quoting only the encouraging half.
The groups most cited as responsible for accessibility were dedicated teams or specialists and engineers or developers, and the paper warns that resting responsibility there can produce an attitude that accessibility is someone else's problem.
A design system can concentrate responsibility in exactly the same way, if it becomes the place where accessibility is assumed to have been dealt with already.
On audit and compliance the paper reads its findings as indicating a need for rigorous regulation, which is not the direction this project's argument runs, and the disagreement is recorded rather than smoothed over.

There is also an honest cost.
An organisation without a design system cannot adopt this method directly, because it must first identify its de facto components.

Accessibility does not sit in one module, which is what makes it easy to lose.
This specification splits it in two.
User technology support covers assistive-technology compatibility: roles, accessible names, states, focus, and keyboard operation.
User layout support covers reflow, measure, spacing, contrast, and reading order.
Every criterion recorded against a component names which branch it belongs to, for a diagnostic reason: a flat list of criteria per component hides whether a failure is geometric or semantic, and those two failures have different owners and different fixes.

The split needs judgement rather than mechanical application.
The clearest case is the reflow exception, which looks like a layout matter and is decided by semantics.
Classification follows what carries meaning, not the visual mechanism that produced the appearance.

#### 2.3 The five gaps

The project surveyed existing practice and recorded five recurring gaps.
Each is the reason a later part of this specification exists, so they are worth reading as a list of problems rather than as criticism of anyone's work.

1. Layout is treated as a visual concern rather than an accessibility concern, despite reflow, resize text, and text spacing being layout criteria.
2. Components are tested in isolation but not in composition.
3. Assistive-technology claims omit engine, browser, version, observed behaviour, and test date.
4. Tokens express values but not constraints or relationships.
5. Documentation does not carry machine-readable assertions, and drifts from the implementation.

A sixth sits slightly apart.
A common readiness model asks whether a component is visually accessible, screen-reader compatible, operable, and understandable.
That is useful and incomplete, because it does not record which engines were tested, and does not address reflow, zoom, text spacing, or forced colours.

#### 2.4 What this specification adds

Against those gaps, this is what the specification contributes.

1. Layout as a first-class accessibility concern inside the system rather than alongside it.
2. Intrinsic primitives that respond to available space rather than to breakpoint guesses.
3. Engine-qualified assistive-technology claims, with uncertainty recorded explicitly rather than omitted.
4. Assertions that travel with specifications, so a claim can be checked mechanically.
5. Composition conformance as well as component conformance.
6. A documented gap in token standards around contrast relationships, stated as a gap rather than papered over.
7. A portable package that carries the accessibility contract, its evidence, and its uncertainty as first-class records, rather than leaving them in a design tool or an untracked spreadsheet.

#### 2.5 What a design system cannot do

A design system is not an accessibility guarantee, and this specification says so in the same plain terms the strongest public example uses.
The GOV.UK Design System states on its accessibility page that using the system does not immediately make a service accessible.
This specification adopts that limit as its own.

The reason is structural rather than a matter of quality.
A design system supplies parts.
It cannot know whether the parts were assembled in an order that makes sense, whether an error message explains anything, or whether the task built from them is one a user can complete.
A perfectly accessible set of components can be assembled into an unusable page, and every component will pass its own tests while that happens.

What a system can do is improve the available user-interface resources and modalities, and record honestly what has and has not been verified.
It cannot replace research with disabled users, assistive-technology testing, content quality, or contextual judgement.

This is why Part II requires non-guarantees.
A component that lists only what it promises invites the reader to assume the rest, and the assumption is where accessibility is lost.

### 3. The design-system model

This clause is informative, and it fixes the vocabulary the normative clauses use.

#### 3.1 The five layers

A design system is treated here as five layers.
When people argue about whether something belongs in the design system, they are almost always arguing across two of these layers without noticing.

| Layer | Contents | Accessibility role |
| --- | --- | --- |
| Principles | Commitments and non-negotiables | Sets the floor and the constraints that may not be traded away |
| Tokens | Named platform-neutral values | Space, type, colour, motion, and contrast-pair candidates |
| Layout primitives | Composable arrangement rules | Reflow, resize, text spacing, reading sequence |
| Components | Interactive elements with semantics and behaviour | Roles, names, states, keyboard, focus |
| Patterns and guidance | Multi-component flows and documentation | Errors, focus management, workflow behaviour |

#### 3.2 Reading the layers

Read the layers from the top down as decreasing generality.

A principle applies everywhere and is not negotiable per screen.
A token is a value with a name.
A layout primitive arranges things and does not know what they mean.
A component is an interactive thing that does know what it means.
A pattern is several components co-operating through a task.

The ordering is not a hierarchy of importance.
It is a hierarchy of scope, and the practical use of it is that it tells you which layer a question belongs to before you try to answer it.

#### 3.3 Placing one decision in the layers

Take the warning message from clause 2.1 and place it.

The commitment that severity is never communicated by colour alone is a principle.
The specific warning colour, and the space around the text, are tokens.
The arrangement of icon, heading, and body text is layout.
The container that announces itself to a screen reader when it appears is a component.
The rule about where focus goes after the user dismisses it is a pattern.

Confusing the layers is the source of many scope disputes, and the size of a question is often mistaken as a result.
Can the warning be red is a token question.
Should the warning steal focus is a pattern question, and it is a far larger one, because the answer changes what happens to the user's place in the page.

#### 3.4 What a design system is not

It is not a component library alone.
A library gives you code.
A system also gives you the reasoning, the tests, and the record of what has and has not been verified, which is what lets somebody else trust the code.

It is not a style guide alone.
A style guide tells you what things look like.
It does not tell you what a component promises, what it refuses to promise, or which keys operate it.

It is not a design-tool file alone.
A mock-up records an outcome without recording the decision that produced it, which is why the outcome drifts as soon as two people need it.

### 4. Conformance

This clause is normative.

#### 4.1 Conformance language

The key words *MUST*, *MUST NOT*, *REQUIRED*, *SHALL*, *SHALL NOT*, *SHOULD*, *SHOULD NOT*, *RECOMMENDED*, *MAY*, and *OPTIONAL* in this document are to be interpreted as described in RFC 2119.

They are used with the following force.

| Keyword | Force in this document |
| --- | --- |
| *MUST*, *REQUIRED*, *SHALL* | An absolute requirement. A package or tool that breaks it does not conform. |
| *MUST NOT*, *SHALL NOT* | An absolute prohibition. |
| *SHOULD*, *RECOMMENDED* | A strong expectation. Departing from it requires a stated reason, and has consequences that the departing party owns. |
| *SHOULD NOT* | A strong expectation against. Doing it anyway requires a stated reason. |
| *MAY*, *OPTIONAL* | Genuinely optional. A consumer *MUST NOT* assume the optional behaviour is present. |

Keywords are written in capitals and are also marked as emphasis.

The capitalisation is the signal.
The emphasis is redundant reinforcement of it, and is deliberately redundant: a reader, a renderer, or an assistive technology that conveys no emphasis loses nothing, because the capitalised word carries the meaning on its own.
No requirement in this document depends on colour, on typographic weight, or on emphasis being perceived.

A reader who encounters one of these words in lower case *MUST* read it as ordinary prose carrying no requirement.
This matters, because the informative clauses use the words must and should in their ordinary English sense.

#### 4.2 Producers and consumers

Two roles carry obligations.

A producer is any tool or person that creates a package.

A consumer is any tool or person that reads a package and relies on its contents.

A single tool *MAY* be both, and when it is, it *MUST* satisfy both sets of obligations independently.
An adapter is always both, which is why Part IV gives it its own clause.

#### 4.3 The core and the method profiles

This specification has a core and a set of named method profiles.

The core is clause 4, clause 5, Part II, and Part IV.
Every AFDS package *MUST* satisfy the core.

A method profile is a named group of requirements carrying a specific way of building interfaces.
Part III defines the profiles.
A package *MUST NOT* be judged against a method profile it does not claim, and a consumer *MUST NOT* treat the absence of a method-profile claim as a defect.

The separation exists because the core describes how to carry an accessibility contract and its evidence, while a method profile describes one way of designing.
An organisation whose brand palette and layout conventions are already fixed can satisfy the core completely.
That organisation gets the contract, the evidence, the uncertainty records, and the portability, and it does not get the layout method.
That is the intended outcome, not a loophole.

#### 4.4 Conformance claims

A conformance claim *MUST* state three things: the format version, the completeness profile, and the set of method profiles claimed, which *MAY* be empty.

A claim *MUST NOT* be expressed as conformance to an informative document, and *MUST NOT* be expressed as conformance to a guide that has no conformance model.
In particular, a package *MUST NOT* claim that a component conforms to the ARIA Authoring Practices Guide, because that guide is informative and has no conformance model to conform to.
The publishable claims about a component are the accessibility criteria met, the semantics used, and the recorded assistive-technology results.

A conformance claim is a claim about a package, not about a service built from it.
A producer *MUST NOT* present a conformance claim as evidence that a service assembled from the package is accessible.

#### 4.5 Method profiles and completeness profiles are independent

Part IV defines completeness profiles, which state how much of a package hierarchy is present.
Part III defines method profiles, which state which design method a package follows.

These are independent axes and they *MUST* be declared separately.
A package containing only tokens *MAY* claim a method profile.
A package containing components, evidence, and fixtures *MAY* claim none.
A consumer *MUST NOT* infer either kind of profile from the other.

### 5. Terms and definitions

This clause is normative.
Where a term defined here is used in a normative clause, it carries this meaning and no other.

**Accessibility Focused Design System (AFDS).** A design system whose accessibility contract, supporting evidence, and recorded uncertainty are first-class parts of the system rather than documentation about it.

**AFDS package.** A single file conforming to Part IV, containing a declared hierarchy of artefacts and the two required root artefacts.

**Container.** The archive format that carries a package.

**Artefact.** Any addressable file inside a package.

**Manifest.** The root artefact declaring the package's identity, versions, profiles, and the location of the inventory.

**Inventory.** The root artefact listing the package's artefacts with their roles and digests.

**Producer.** Any tool or person that creates a package.

**Consumer.** Any tool or person that reads a package and relies on its contents.

**Core.** The clauses every package must satisfy, being clause 4, clause 5, Part II, and Part IV.

**Method profile.** A named group of requirements in Part III carrying one way of designing interfaces, binding only on a package that claims it.

**Completeness profile.** A named group of requirements in Part IV stating how much of a package hierarchy is present.

**Conformance claim.** A statement naming a format version, a completeness profile, and a set of method profiles.

**Principle.** A commitment that applies across the system and is not negotiable for an individual screen.

**Token.** A named, platform-neutral value.

**Canonical token source.** The token file a package declares as authoritative for a given token set, against which any other representation of the same values is derivative.

**Layout primitive.** A composable arrangement rule that positions content without knowing what the content means.

**Component.** An interactive element with declared semantics and behaviour.

**Pattern.** Several components co-operating through a task, together with the guidance governing that co-operation.

**Component contract.** The machine-readable declaration of what a component guarantees, what it does not guarantee, and the assertions that make those statements checkable.

**Component specification.** The human-readable counterpart to a component contract, carrying the reasoning a contract cannot express.

**Guarantee.** A statement of behaviour or property that a component commits to, expressed so that it can be tested.

**Non-guarantee.** An explicit statement of something a component does not commit to, recorded so that a consumer cannot arrive at it by assumption.

**Assertion.** A machine-checkable statement attached to a specification, whose truth can be evaluated against an implementation without human judgement.

**Evidence record.** A record of an observed result for one component in one assistive-technology combination, qualified by engine, browser, versions, observed behaviour, and date.

**Assistive-technology combination.** A named tuple of assistive technology, browser, operating system, and versions, treated as the unit that evidence attaches to.

**Uncertainty record.** A record stating that something is not known, of the same standing as a record stating a result.

**Keyboard contract.** The declared operation of a component across entry, internal movement, activation, exit, state change, restoration, pointer and touch parity, and speech-recognition operation.

**Native baseline.** The behaviour and semantics a component would have if built from platform-native elements without added roles or scripted behaviour.

**Support-dependent pattern.** A pattern whose declared behaviour is known to depend on assistive-technology or engine support that is incomplete, and which therefore carries a reassessment obligation.

**Adapter.** A tool that converts between an AFDS package and some other representation.

**Export adapter.** An adapter producing a non-AFDS representation from a package.

**Import adapter.** An adapter producing a package, or part of one, from a non-AFDS representation.

**Transform report.** The record an adapter produces stating what it carried, what it could not carry, and what a consumer must therefore not assume.

**Measure.** The length of a line of text, treated as a constraint on layout rather than as a stylistic preference.

**User technology support.** The branch of accessibility concerned with assistive-technology compatibility: roles, accessible names, states, focus, and keyboard operation.

**User layout support.** The branch of accessibility concerned with reflow, measure, spacing, contrast, and reading order.

**Composition conformance.** Conformance measured with a component placed inside a realistic page, as distinct from conformance measured with the component in isolation.

### 6. References

#### 6.1 Normative references

The following are cited normatively.
A dated reference means that edition applies.
An undated reference means the current version applies.

- IETF RFC 2119, *Key words for use in RFCs to Indicate Requirement Levels*. <https://www.rfc-editor.org/rfc/rfc2119>
- W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*. <https://www.w3.org/TR/WCAG22/>
- W3C, *Accessible Rich Internet Applications (WAI-ARIA) 1.2*. <https://www.w3.org/TR/wai-aria-1.2/>
- WHATWG, *HTML*, Living Standard. <https://html.spec.whatwg.org/multipage/>
- Design Tokens Community Group, *Design Tokens Format Module 2025.10*. <https://www.designtokens.org/TR/2025.10/format/>
- NIST, *FIPS 180-4, Secure Hash Standard*. <https://csrc.nist.gov/pubs/fips/180-4/upd1/final>
- IANA, *Media Types registry*. <https://www.iana.org/assignments/media-types/media-types.xhtml>

#### 6.2 Informative references

The following inform the document without creating requirements.

- W3C ARIA Working Group, *ARIA Authoring Practices Guide (APG)*. <https://www.w3.org/WAI/ARIA/apg/>
- W3C, *ARIA Authoring Practices Guide, pattern index*. <https://www.w3.org/WAI/ARIA/apg/patterns/>
- Putnam, C., Rose, E. J. and MacDonald, C. M. (2023). "It could be better. It could be much worse": Understanding Accessibility in User Experience Practice with Implications for Industry and Education. *ACM Transactions on Accessible Computing*, 16(1), 1-25. <https://doi.org/10.1145/3575662>
- GOV.UK Design System, *Accessibility*. <https://design-system.service.gov.uk/accessibility/>
- W3C Design System Documentation Community Group. <https://www.w3.org/community/designsystemdocs/>
- Open UI Community Group. <https://www.w3.org/community/open-ui/>
- Pickering, H. and Bell, A. *Every Layout: Relearn CSS layout*. <https://every-layout.dev/>
- Pickering, H. (2014). *Axiomatic CSS and Lobotomized Owls*. A List Apart, 21 October 2014. <https://alistapart.com/article/axiomatic-css-and-lobotomized-owls/>
- W3C WAI, *Understanding Success Criterion 1.4.10: Reflow*. <https://www.w3.org/WAI/WCAG22/Understanding/reflow.html>
- W3C, *Techniques for WCAG 2.2*. Cited in clause 22.6: C31, C33, C34, C38, G206, G224, G225, SCR34. <https://www.w3.org/WAI/WCAG22/Techniques/>
- Braille Institute, *Atkinson Hyperlegible font*. <https://www.brailleinstitute.org/freefont/>

## Part II. The component contract

This part is normative in full.
It applies to every component, layout primitive, and pattern in a package, whatever method profile the package claims.

Part II says what a component declares about itself.
It does not say how a component should be designed, and a reader looking for this project's own opinions about layout, colour, or which patterns to build will find them in Part III, where they bind only a package that asks for them.

The division is deliberate and worth stating once.
Requiring a component to record its native baseline and why a native element was insufficient is a disclosure obligation, and it belongs here.
Requiring the component to prefer a native element is a design rule, and it belongs in Part III.
An organisation can therefore be held to complete disclosure without being held to this project's taste.

### 7. The component specification

#### 7.1 Purpose and form

A component specification is the machine-readable record of what a component is, what it promises, what it refuses to promise, and how each of those statements can be checked.

Every component, layout primitive, and pattern in a package *MUST* have exactly one canonical component specification.
The specification *MUST* be a JSON document.
Where any other artefact in the package states the same fact, the specification governs and the other artefact is derivative.

A specification *MUST NOT* be generated from an implementation by inspection alone.
The reason is that a specification derived from code can only ever record what the code does, and the purpose of the document is to record what the component is obliged to do, so that the two can be compared and found to differ.

#### 7.2 Required fields

A component specification *MUST* contain the following fields.

| Field | Type | Clause |
| --- | --- | --- |
| `afdsSpecVersion` | string | 7.3 |
| `id` | string | 7.3 |
| `name` | string | 7.3 |
| `kind` | string | 7.4 |
| `version` | string | 7.3 |
| `status` | string | 7.4 |
| `summary` | string | 7.3 |
| `semanticModel` | object | 8 |
| `derivation` | object | 9 |
| `keyboardContract` | object | 10 |
| `reflowBehaviour` | object | 11 |
| `wcagMapping` | array | 12 |
| `guarantees` | array | 14 |
| `nonGuarantees` | array | 14 |
| `assertions` | array | 15 |
| `uncertainty` | array | 17 |
| `tests` | object | 18 |

A producer *MUST NOT* omit a field on the grounds that it does not apply.
Where a field does not apply, the specification *MUST* say so explicitly in the form the relevant clause defines.

This is the most important structural rule in Part II, and the reason for it is the argument in clause 2.5.
An omitted field and an inapplicable field look identical to a reader, and the reader will resolve the ambiguity in the direction that flatters the component.
A component that has no keyboard contract *MUST* say that it has none, so that a reviewer cannot mistake absence for oversight.

#### 7.3 Identity fields

`afdsSpecVersion` *MUST* be the version of this specification the document conforms to.

`id` *MUST* be stable for the life of the component and *MUST* be unique within the package.
An `id` *MUST NOT* be reused for a different component after the original is withdrawn.

`name` is the human-readable name.
`summary` *MUST* state what the component does and *SHOULD* state what it does not do, in prose, in no more than a short paragraph.

`version` *MUST* follow the payload versioning rules in Part IV.
A component version is independent of the package version and of `afdsSpecVersion`.

#### 7.4 Kind and status

`kind` *MUST* be one of the following values.

| Value | Meaning |
| --- | --- |
| `layout-primitive` | A composable arrangement rule that positions content without knowing what it means |
| `component` | An interactive or structural element with declared semantics |
| `pattern` | Several components co-operating through a task |

`status` *MUST* be one of the following values.

| Value | Meaning |
| --- | --- |
| `draft` | Under development. A consumer *MUST NOT* rely on any part of it remaining stable. |
| `proposed` | Complete and awaiting review. Stable in shape, not yet in content. |
| `stable` | Reviewed, and subject to the versioning rules in Part IV. |
| `deprecated` | Still present and still supported, with a replacement named. |
| `withdrawn` | No longer supported. Present so that consumers can detect the withdrawal. |

A `deprecated` or `withdrawn` specification *MUST* state the reason and, where one exists, the replacement `id`.

#### 7.5 The human-readable counterpart

Every component specification *SHOULD* have a human-readable counterpart carrying the reasoning the JSON cannot express.

The counterpart *MUST NOT* contradict the specification.
Where the two disagree, the specification governs, and the disagreement is a defect in the package rather than a matter for interpretation.

The counterpart exists because a machine-readable contract records decisions without recording why they were taken, and a decision whose reasoning is lost cannot be safely revisited.

### 8. The semantic model

#### 8.1 Required content

The `semanticModel` object *MUST* record:

- `role`, the ARIA role the component exposes, or `none` where it exposes no role;
- `implicitElement`, the native element the component renders as its own outermost element;
- `accessibleName`, the source of the accessible name, or `none` where the component has no accessible name of its own;
- `rationale`, prose explaining why the semantics are what they are;
- `domOrderIsReadingOrder`, a boolean stating whether the component preserves document order as reading order;
- `consumerObligations`, an array of statements described in clause 8.2.

A component that exposes no role *MUST* record `none` rather than omitting the field, and its `rationale` *MUST* say why no role is correct.
A component with no semantics is making a claim, not declining to make one.

#### 8.2 Consumer obligations

A consumer obligation is a statement of something the consumer *MUST* do for the component to be used correctly.

Every obligation *MUST* be written as a requirement on the consumer rather than as a description of the component.
Every obligation *MUST* use the conformance language of clause 4.1.

Consumer obligations exist because most accessibility failures involving a correct component are failures of the surrounding markup.
A layout primitive that arranges children cannot know whether those children form a list, and the consumer who does know is the only party able to supply the semantics.
Recording that as an obligation moves it from folklore into the contract.

A consumer obligation *MUST NOT* be used to discharge a responsibility the component could reasonably meet itself.
Writing an obligation is not a way of exporting difficulty.

#### 8.3 The native baseline

The `semanticModel` *MUST* record the native baseline: the behaviour and semantics the component would have if built from platform-native elements without added roles or scripted behaviour.

Where the component is not built on that baseline, the specification *MUST* state which native element was considered and why it was insufficient.
An answer of the form that no native element was considered is a valid answer and *MUST* be recorded as such rather than left blank.

This clause requires disclosure and does not require a preference.
A package that always answers this field by saying a native element was rejected for visual reasons conforms to the core, and its reviewers now have something to argue with, which is the point.

### 9. Derivation and the pattern registry

#### 9.1 The registry

A package *MUST* record, for every component, exactly one derivation status.
The set of these records is the pattern registry.

The registry is what stops a policy about external patterns from becoming decorative.
Without it, whether a component follows a recognised interaction model is a property of whoever wrote it first, discoverable only by reading the implementation.

#### 9.2 The five statuses

The `derivation.status` field *MUST* be one of the following values.

| Value | Meaning |
| --- | --- |
| `native-first` | A native element fully supplies the interaction |
| `pattern-derived` | A custom component implements a recognised published pattern |
| `pattern-adjacent` | A similar interaction that intentionally differs from the published pattern |
| `custom` | No mature published pattern applies |
| `prohibited` | The pattern creates more accessibility cost than value and is not to be used |

The statuses are not a quality ranking.
A component is not defective for being `pattern-derived`, and a package whose components are mostly `native-first` is not thereby better.
What the registry records is that the status was decided and reasoned, rather than arrived at.

Two statuses carry extra obligations.

A `pattern-adjacent` entry *MUST* name the pattern it resembles and *MUST* state exactly where and why it departs.
The status exists so that a component is not labelled with a pattern name it does not honour, which would mislead implementers and testers alike.

A `prohibited` entry *MUST* state the cost that motivated the prohibition, and *MUST* be revisitable if the underlying support picture changes.
A prohibition without a stated cost is an opinion that cannot be reviewed.

#### 9.3 Required fields for a derived component

Where `derivation.status` is `pattern-derived` or `pattern-adjacent`, the specification *MUST* additionally record:

1. the pattern name and its source URL;
2. the native alternative considered, and why it was insufficient;
3. every deviation from the published pattern, each with its reason and its cost, and each tagged under clause 13;
4. whether the pattern is support-dependent, and if so the reassessment trigger required by clause 9.5.

A derived component with no deviations *MUST* record that explicitly.
Silence about deviations is never to be read as an absence of them.

#### 9.4 What a derivation may not claim

A specification *MUST NOT* state or imply that a component conforms to an informative document.

Recording that a component is derived from a published pattern is a statement about where the interaction model came from.
It is not a conformance claim, it carries no assurance, and a consumer *MUST NOT* treat it as evidence of anything.
The publishable claims about a component are the criteria in its WCAG mapping, the semantics in its semantic model, and the results in its evidence records.

A specification *MUST NOT* cite a published pattern's own example implementations as evidence for the component.
Such examples are written to demonstrate a pattern legibly, which is a different goal from being production code, and no external example can carry evidence about the code a package actually ships.

#### 9.5 Support-dependent patterns

A pattern is support-dependent where its declared behaviour is known to depend on assistive-technology or engine support that is incomplete.

A support-dependent component *MUST* record a reassessment trigger stating the condition under which its specification is reopened.

The trigger is required because a change in support is the main reason a settled contract silently becomes wrong.
Without a trigger the change is noticed by accident, usually by a user.

### 10. The keyboard contract

#### 10.1 Keyboard means more than a keyboard

The keyboard contract is the load-bearing part of a component specification, and its name understates it.

A keyboard interface is an input pathway rather than a physical device.
WCAG 2.2 defines it narrowly, as an interface used by software to obtain keystroke input.
The breadth comes from what drives that interface, and the Understanding document for Success Criterion 2.1.1 lists speech input software, sip-and-puff software, on-screen keyboards, scanning software, and a variety of assistive technologies and alternate keyboards among keyboard emulators.

The attribution matters and this specification is precise about it, because a reviewer who cites the definition for the emulator list is citing the wrong document and will lose the argument as soon as somebody checks.

The definition also carries an exclusion.
Operation through a keyboard-operated mouse emulator does not qualify as operation through a keyboard interface, because the program is being driven through its pointing-device interface instead.
A component exercised only that way *MUST NOT* be recorded as having been tested for keyboard operation.

The consequence is that a component's keyboard contract is simultaneously its switch-access contract, its scanning contract, and much of its speech-input contract.
Testing with a physical keyboard is necessary and *MUST NOT* be treated as sufficient.

#### 10.2 The eight stages

Where a component has a keyboard contract, the contract *MUST* declare all eight of the following.

| Stage | What it declares |
| --- | --- |
| 1. Entry | What receives focus when the user moves into the component, and what happens on re-entry after leaving |
| 2. Internal movement | Which keys move focus inside the component, whether movement wraps, and whether roving `tabindex` or `aria-activedescendant` is used |
| 3. Activation | Which keys act on the focused item, distinguishing keys that change selection from keys that commit an action |
| 4. Exit | Whether Tab leaves, whether Escape dismisses, and where focus goes in each case |
| 5. State change | What is conveyed after expansion, selection, validation failure, loading, or deletion, and by what mechanism |
| 6. Restoration | Where focus returns when a popup or dialog closes, including when the invoking control no longer exists |
| 7. Pointer and touch parity | Whether all functionality is reachable without hover, without drag, and without a path-dependent pointer movement |
| 8. Speech-recognition operation | Whether every visible interactive control has a stable visible label, and whether visible text is contained in the accessible name |

Stage 3 *MUST* distinguish selection from commitment.
Conflating them is what produces accidental destructive operations, and the risk is greatest exactly where the consequences are worst.

Stage 6 *MUST* name a documented logical successor for the case where the invoker no longer exists.
An action that deletes the row containing its own trigger is common, and a contract that does not answer it is not a contract.

An exit path that depends on the user guessing *MUST NOT* be recorded as satisfying stage 4.

#### 10.3 Declaring the absence of a contract

Where a component has no keyboard contract, `keyboardContract.hasKeyboardContract` *MUST* be `false` and the object *MUST* carry a statement saying so explicitly.

The statement *MUST* be positive rather than empty.
A reviewer reading an empty keyboard contract cannot tell whether the component has none or whether nobody filled it in, and those are opposite findings.

#### 10.4 Focus lifecycle

The contract *MUST* record, as booleans, whether the component receives focus, moves focus, traps focus, and restores focus, together with a note explaining the combination.

These four are recorded separately from the eight stages because they are the properties a consumer needs in order to reason about composition.
A page containing two components that both trap focus has a defect that neither component's own tests can detect.

### 11. Reflow and layout behaviour

#### 11.1 Required content

The `reflowBehaviour` object *MUST* record:

- whether the component is intrinsic, meaning that it responds to available space rather than to a chosen breakpoint;
- whether it uses layout media queries;
- what author-fixed dimensions it declares, or `none`;
- whether it declares fixed heights;
- the mechanism, in prose, by which it reflows;
- whether it operates without JavaScript;
- whether it claims the two-dimensional exception, and the rationale for that claim.

This clause is in the core rather than in a method profile because the declaration is a disclosure, not a design rule.
A package whose components all use media queries and fixed heights conforms to the core, provided it says so.

#### 11.2 The two-dimensional exception

Where the component claims the two-dimensional exception, the specification *MUST* give a rationale resting on semantic two-dimensional structure.

The rationale *MUST NOT* rest on visual appearance, and *MUST NOT* rest on the layout technique used to produce the appearance.
A region that merely looks like a grid does not qualify.

Where the component does not claim the exception, the specification *SHOULD* still record why, because the components most likely to be misused as a basis for the claim are the ones that never had a basis for it.

Adopting a widget role in order to unlock the exception *MUST NOT* be recorded as a rationale.
Doing so abuses both the role and the criterion, and a consumer encountering such a rationale *SHOULD* treat the package as defective.

### 12. WCAG mapping

#### 12.1 Required content

The `wcagMapping` array *MUST* contain one entry for every success criterion the component bears on.

Each entry *MUST* record the criterion number, its name, the level at which WCAG 2.2 assigns it, its branch under clause 12.2, its relationship under clause 12.3, and a note.

The assigned level is a property of the criterion and is fixed by WCAG.
It is not the target level of clause 12.4, which is a property of the package or the component and is chosen by the author.

#### 12.2 The two branches

Every entry *MUST* record a `branch` of either `user technology support` or `user layout support`.

| Branch | Covers |
| --- | --- |
| `user technology support` | Assistive-technology compatibility: roles, accessible names, states, focus, keyboard operation |
| `user layout support` | Reflow, measure, spacing, contrast, reading order |

The split is diagnostic.
A flat list of criteria per component hides whether a failure is geometric or semantic, and those two failures have different owners, different tests, and different fixes.

Classification *MUST* follow what carries meaning rather than the mechanism that produced the appearance.
The clearest case is the two-dimensional exception, which looks like a layout matter and is decided by semantics.

#### 12.3 Relationship vocabulary

Each entry *MUST* record a `relationship` of either `supports` or `does-not-address`.

| Value | Meaning |
| --- | --- |
| `supports` | The component contributes to meeting the criterion |
| `does-not-address` | The component bears on the criterion and does nothing about it, so the consumer owns it |

The vocabulary is closed.
Extending it is a change to this specification and *MUST NOT* be done within a package.

A `does-not-address` entry is not an admission of failure and *MUST NOT* be treated as one.
Recording that a layout primitive conveys no relationships, and that the consumer therefore owns Info and Relationships, is more useful than silence, because silence leaves the consumer to discover the ownership in an audit.

#### 12.4 The target level is declared, not mandated

This specification does not fix a target WCAG conformance level and *MUST NOT* be read as requiring one.

The choice between Level A, Level AA, and Level AAA is the author's.
This specification requires only that the choice be declared, and that a reader be able to determine which level applies to any given component without guessing.

WCAG 2.2 supports leaving the choice open rather than fixing it.
Its Conformance section states that "It is not recommended that Level AAA conformance be required as a general policy for entire sites because it is not possible to satisfy all Level AAA success criteria for some content".
A format that mandated a single level for every package would be imposing exactly the blanket policy WCAG advises against, and would do so across content whose nature it cannot know.

A package *MUST* declare a default target level.

A component *MAY* amend that default.
A component that amends it *MUST* record the amended level and the reason for the amendment.

A method profile *MAY* set a default target level for packages claiming it.
Where a package claims such a profile, that default governs the package, because a profile is claimed whole under clause 20.3.

The effective target level for a component resolves in this order, and the first available declaration governs.

The component's own declaration.
The default set by a claimed method profile, where a claimed profile sets one.
The package default.

An effective level *MUST NOT* be inferred from anything other than these three declarations.
It *MUST NOT* be inferred from a conformance profile, which states completeness and says nothing about level.
It *MUST NOT* be inferred from the presence of evidence recorded at a higher threshold, because measuring a ratio is not the same act as committing to it.

A declared target level is a statement of intent.
It *MUST NOT* be read as evidence that the level is met.
Whether a criterion is met at the declared level is an assertion under clause 15 and is substantiated under clause 16, and clause 4.4 already forbids presenting a package claim as evidence that a service is accessible.

Amending a level downward is permitted, and *MUST* be recorded rather than concealed.
A component targeting Level AA inside a package that defaults to Level AAA is a disclosure, and the disclosure is worth more than a package-wide claim a reviewer would have to disprove component by component.
The reverse case matters as much: a component that can honestly reach Level AAA in a package defaulting to Level AA should be able to say so without the package overstating itself elsewhere.

A level is declared per component and not per criterion.
A package needing to record that one criterion is held to a different threshold than the rest of its component does so as an assertion under clause 15, not as a second target level.

### 13. Kinds of requirement

Every requirement in a component specification *MUST* be tagged with exactly one of five kinds.

| Value | What it means | Consequence if not met |
| --- | --- | --- |
| `required-by-standard` | A normative requirement from a W3C standard | A conformance failure |
| `recommended-by-convention` | An interoperable convention users are likely to expect | A usability and discoverability risk, not a conformance failure |
| `project-convention` | A choice the system has made for internal consistency | An inconsistency to be reconciled or documented |
| `product-deviation` | A deliberate, recorded departure for a product reason | Nothing, provided the record and its reasoning exist |
| `support-limitation` | A gap in browser or assistive-technology behaviour | Uncertainty to be disclosed, not a claim to be made |

Tagging prevents two opposite failures.

The first is presenting every convention as conformance law.
A component may satisfy WCAG with a keyboard model that departs from a widely used convention, provided it is fully operable and its state is correctly conveyed, and a document that denies this loses its authority the moment somebody checks.

The second is dismissing conventions as merely optional, which is how components end up technically conformant and practically unusable by people who already know how the interaction is supposed to work.

The correct handling of a departure is to allow it, label it, and state its cost.
A `product-deviation` *MUST* record its cost as well as its reason.

### 14. Guarantees and non-guarantees

#### 14.1 Guarantees

A guarantee is a declared commitment about the component's behaviour or properties.

The `guarantees` array *MUST* contain one entry per commitment, and each entry *MUST* record:

- `id`, unique within the specification;
- `statement`, the commitment, written so that it can be tested;
- `branch`, under clause 12.2;
- `requirementKind`, under clause 13;
- `assertions`, an array of assertion identifiers, described in clause 14.2.

A guarantee is a design commitment.
It is what the component is obliged to do, and it outlives any particular test run, which is why it is authored rather than computed.

#### 14.2 A guarantee must name its test

Every guarantee *MUST* name at least one assertion, defined in clause 15, that tests it.
A guarantee whose `assertions` array is empty is invalid, and a package containing one does not conform.

This is the rule that stops a guarantee from being a wish.
A commitment that nobody can state a procedure for is not a commitment about the product, it is a sentiment about it, and the distinction is the reason this format exists.

A producer *MUST NOT* satisfy this rule by writing an assertion that restates the guarantee without giving a procedure.
Clause 15.1 requires a procedure for exactly this reason.

#### 14.3 Substantiation is derived, not declared

Every guarantee has a substantiation status.
The status *MUST NOT* be authored.
It is computed from the evidence records that reference the guarantee's assertions, and a producer that writes it into the specification is stating something it is not entitled to state.

| Status | Computed when |
| --- | --- |
| `substantiated` | Every named assertion has at least one evidence record with result `supported`, and none with `partial` or `unsupported` |
| `partially-substantiated` | At least one named assertion has a result of `supported`, and at least one has `partial` or has no record at all |
| `unsubstantiated` | No named assertion has any evidence record other than `not-yet-tested` |
| `contradicted` | Any named assertion has an evidence record with result `unsupported` |

A consumer *MUST NOT* present a guarantee as met without also presenting its substantiation status.

The separation of the promise from the measurement is the point of the design.
A new component with no testing has made commitments and has substantiated none of them, and both halves of that sentence are true and useful.
Collapsing them would either let a package promise what it has not earned, or force it to promise nothing until testing exists, and neither describes the real state of any design system.

A `contradicted` guarantee *MUST* be treated as a defect in the package rather than as a property of the component.
The producer either fixes the component, narrows the guarantee, or withdraws it, and Part IV states what each of those does to the version.

#### 14.4 Non-guarantees

A non-guarantee is an explicit statement of something the component does not commit to.

The `nonGuarantees` array *MUST* be present and *MUST NOT* be empty.
A component that commits to everything has not understood the question.

A non-guarantee *MUST* be specific enough to change what a consumer does.
A statement that the component does not guarantee accessibility is not a non-guarantee, because no consumer can act on it.
A statement that the component provides no grouping role and no accessible name, so that the consumer must supply both, is a non-guarantee, because it tells the consumer what to build.

#### 14.5 Why non-guarantees are mandatory

This clause is the mechanism behind clause 2.5.

A component that lists only its promises invites the reader to assume the rest, and the assumption is where accessibility is lost.
The reader is not being careless when they do this.
A list of guarantees reads as a description of the component, and a description is naturally taken to be complete.

Requiring the opposite list forces the boundary of the contract to be drawn explicitly, by the party that knows where it lies.

### 15. Assertions

#### 15.1 Required content

An assertion is a statement about the component whose truth can be evaluated against an implementation.

Each entry in the `assertions` array *MUST* record:

- `id`, unique within the specification;
- `type`, either `automated` or `manual`;
- `statement`, what is asserted;
- `procedure`, how to evaluate it.

The `procedure` field *MUST* be specific enough that two testers following it independently would agree on the result.
A procedure that restates the statement in the imperative does not satisfy this and *MUST NOT* be used to discharge clause 14.2.

#### 15.2 Automated and manual

An assertion of type `automated` *MUST* be evaluable without human judgement.

An assertion of type `manual` *MUST* record what the tester observes rather than what they conclude.
The distinction matters because a manual assertion phrased as a conclusion invites the tester to supply the answer the specification expects.

A `manual` assertion produces a result that expires, and clause 16.4 governs that.

#### 15.3 What an assertion is not

An assertion *MUST NOT* be a statement about intent, about the design process, or about a standard.

That a component was built following a pattern is not an assertion, because no procedure evaluates it against the running implementation.
That a component meets a success criterion is not an assertion either, because meeting a criterion is a conclusion drawn from observations rather than an observation.
The assertion is the observation.

### 16. Evidence records

#### 16.1 What evidence attaches to

Evidence attaches to a combination, not to a component.

A combination is the tuple of assistive technology, browser, engine, operating system, and their versions.
A result observed in one combination says nothing about another, and a package that records a single undifferentiated result is making a claim it has not tested.

This is the third of the five gaps in clause 2.3, and it is the one that most often survives into otherwise careful documentation.

#### 16.2 Required fields

Each evidence record *MUST* record the following.

| Field | Content |
| --- | --- |
| `id` | Unique within the package |
| `componentId` | The component the record concerns |
| `assertionRef` | The assertion or assertions this record evaluates |
| `claim` | The behaviour that was looked for |
| `engine`, `engineVersion` | The rendering engine and its version |
| `browser`, `browserVersion` | The browser and its version |
| `at`, `atVersion` | The assistive technology and its version, or `none` |
| `platform`, `device` | The operating system and the class of device |
| `startingViewport`, `zoom` | The layout conditions, or `not-applicable` |
| `date` | The date of observation |
| `result` | A value from clause 16.3 |
| `observation` | What was actually observed |
| `tester` | Who made the observation |
| `uncertaintyRef` | The uncertainty record this result bears on, where one exists |

`assertionRef` is what allows clause 14.3 to compute a substantiation status.
A record that evaluates nothing nameable cannot contribute to a guarantee, and a producer *MUST NOT* record one.

`observation` *MUST* record what happened rather than whether it was correct.
The result field carries the judgement, and keeping the two apart is what makes a record re-readable when the expectation later changes.

#### 16.3 Result vocabulary

`result` *MUST* be one of the following values.

| Value | Meaning |
| --- | --- |
| `not-yet-tested` | No observation has been made. The claim it would support is uncertainty, not a guarantee. |
| `supported` | The expected behaviour was observed on the stated versions on the stated date. |
| `partial` | The behaviour was observed but differs materially from the expectation. The difference *MUST* be described. |
| `unsupported` | The expected behaviour was not observed. |
| `not-applicable` | The combination cannot exhibit the behaviour. |

The value `not-applicable` carries a second sense outside the `result` field.
In any other field it means that the field does not apply to that record, such as a zoom level on a record about announcement, or an assistive-technology version on a record whose `at` is `none`.
A package *MUST* use it in only these two senses.

#### 16.4 Results expire

An evidence record is an observation on a date, and *MUST NOT* be treated as a permanent property of the component.

A consumer *SHOULD* treat a record as stale when the stated versions are no longer current, and *MUST NOT* present a stale record as a current result without saying so.

This is why the fourth testing level in clause 18.1 is recorded with a date rather than a tick.
Assistive-technology behaviour changes with releases the package cannot observe, and a format that stores the result without the date stores a claim that quietly becomes false.

### 17. Uncertainty records

#### 17.1 Required content

An uncertainty record states that something is not known.

Each entry in the `uncertainty` array *MUST* record:

- `id`, unique within the specification;
- `subject`, what the uncertainty is about;
- `statement`, what specifically is not known;
- `status`, from clause 17.2;
- `evidenceRef`, pointing to the evidence records that bear on it, where any exist.

#### 17.2 Status vocabulary

`status` *MUST* be one of the following values.

| Value | Meaning |
| --- | --- |
| `not-yet-tested` | No observation has been attempted |
| `results-conflict` | Observations disagree across combinations, and the disagreement is not yet explained |
| `no-known-method` | No procedure is known that would settle the question |
| `awaiting-support` | The question cannot be settled until support changes in a browser or assistive technology |

#### 17.3 Uncertainty is a record, not a failure

An uncertainty record has the same standing as a record stating a result, and a consumer *MUST NOT* treat its presence as a defect.

A package with no uncertainty records is either exhaustively tested across every combination or is concealing something, and the first is not achievable.

An assistive-technology claim without a test record *MUST* be recorded as uncertainty rather than as a guarantee.
This rule does most of the work in the format.
The ordinary way accessibility documentation becomes false is not by lying, it is by stating a reasonable expectation in the same voice as a measured result, and this rule makes the two grammatically distinct.

### 18. Testing levels and fixtures

#### 18.1 The five levels

A package *SHOULD* verify each component at five levels.
Each level catches a class of defect the others miss, so they *MUST NOT* be treated as substitutes for one another.

| Level | What is tested |
| --- | --- |
| 1. Static semantics | Element choice, role validity, accessible name, state, relationships |
| 2. Keyboard contract | Entry, internal movement, activation, exit, restoration |
| 3. Visual and layout | Focus visibility, forced colours, 400 per cent zoom, text spacing, reflow |
| 4. Assistive technology | Actual behaviour by combination, version, and date |
| 5. Composition | Behaviour among landmarks, headings, and realistic content |

Levels 1 to 3 are largely scriptable and *SHOULD* run on every change.
Level 4 is manual, slow, and produces results that expire, which is why clause 16 records it with a date.
Level 5 is the level most often skipped, and it is where component-level correctness turns into page-level failure.

#### 18.2 Isolation and composition are both required

Conformance is measured at two levels: the component in isolation, and the component inside a realistic page.

A package *MUST NOT* claim composition conformance on the strength of isolated testing.

The two levels find different defects, and the composition defects are the ones a component cannot detect about itself.
Two components that each correctly manage focus can produce a page in which focus is managed twice.
A component that correctly contributes a landmark can produce a page with duplicate landmarks.
A dialog that passes every isolated test can open beneath page chrome its own fixture does not contain.

#### 18.3 Fixtures

The `tests` object *MUST* record the location of an isolated fixture and of a realistic-page fixture.

Where a package does not ship a fixture, the `tests` object *MUST* record where it belongs and *MUST* state that it is absent, and a consumer *MUST* treat the fixture as absent rather than as unlocatable.

A recorded path to a fixture that does not exist is a statement about the package's completeness, and a package that quietly omits the field makes the same statement without disclosing it.

### 19. Design-tool annotation

#### 19.1 The eleven fields

Where a package supports a design-tool handoff, it *SHOULD* provide an annotation preset exposing the information a visual mock-up cannot convey.

The preset *SHOULD* carry the following eleven fields.

| Field | What it records |
| --- | --- |
| Pattern identity | Which pattern, if any, the component implements |
| Semantic model | Native element and any ARIA roles |
| Accessible name source | Where the name comes from, and whether visible text is contained in it |
| Relationship model | Controlling, expanding, labelling, describing, and error-message relationships |
| Focus order and initial focus | Reading and focus sequence, and the initial focus target |
| Internal keyboard navigation | Which keys move focus inside the component |
| Close and restore-focus behaviour | How the component is dismissed and where focus returns |
| Hidden versus removed | Whether content is hidden, made inert, or removed from the document |
| Required visible states | Which states must be visible; focus is mandatory and hover is optional |
| Responsive and reflow behaviour | How the component behaves at narrow widths and at high zoom |
| Assistive-technology uncertainty marker | Behaviour known to vary or not yet verified |

These eleven are written for design handoff.
They are not the fields required by clause 9.3, which are written for engineering review, and a count of one is never a count of the other.

The relationship model is the field most often lost, and it is the one that most repays recording.
It is invisible in a mock-up and expensive to reverse-engineer afterwards.
A designer who has decided that a control expands a panel has already decided that an expansion relationship applies, and writing it down costs less than discovering it in an audit.

#### 19.2 The annotation economy rule

An annotation *SHOULD NOT* restate behaviour the coded component already guarantees.

The annotation identifies the selected component and any product-level choices or deviations.
Restating guaranteed behaviour makes annotations long, makes them drift from the code, and trains reviewers to skim them, which defeats the annotations that carry something the code does not.

## Part III. The method profiles

This part is normative only for a package that claims the profile in question.
A package that claims no profile conforms to this specification by satisfying clause 4, clause 5, Part II, and Part IV, and nothing in this part applies to it.

Part II says what a component must declare.
This part says what a component must do, and it exists as a separate part because those are different kinds of obligation with different claims to authority.

The obligation to disclose is general.
Any organisation building an accessible component ought to record its semantic model, its keyboard contract, what it guarantees, what it refuses to guarantee, and what it does not yet know, whatever design opinions it holds.
That is why those obligations sit in the core, where they bind every package.

The obligation to build in a particular way is not general.
The layout method in clause 21 is one defensible answer to intrinsic layout, not the only one.
An organisation with a working breakpoint system, a different reflow policy, or a different component catalogue is not failing at accessibility, and a specification that told it otherwise would be overreaching and would deserve to be ignored.

So the method choices are gathered here, named, given identifiers, and made claimable.
A package that wants them can adopt them and be measured against them.
A package that does not can ignore this part entirely and still conform.
The value of writing them down is that the choices become inspectable and comparable rather than tacit, and that a package claiming a profile is making a statement a reader can check.

The profiles are also where this project's debts are most concentrated, which is why clause 20.5 requires each one to say where its ideas came from.

### 20. Method profiles

#### 20.1 What a profile is

A method profile is a named, versioned set of requirements about how components are built, which a package *MAY* claim and against which it can then be measured.

A profile is not a level.
The profiles defined in this part are not ordered, do not build on one another, and carry no ranking.
A package claiming three profiles is not more conformant than a package claiming one, and a package claiming none is not deficient.

A profile *MUST NOT* restate a core requirement.
Where a profile appears to require something Part II already requires, Part II governs and the profile's restatement has no independent force.
This keeps the core and the profiles from drifting apart, and it means a reader can always determine which requirements survive the removal of a profile claim.

A profile *MUST NOT* weaken a core requirement.
A profile that purported to excuse a package from a Part II obligation would not be a profile, and a package claiming it does not conform to this specification.

A profile *MUST* impose at least one requirement that the core does not.
The two preceding rules leave open a profile that restates nothing, weakens nothing, and requires nothing, and such a profile would be a label rather than a commitment.
A package claiming it would appear to have taken on an obligation while taking on none, which is the kind of unearned claim this specification exists to prevent.
Where the intended content of a profile turns out to be entirely a matter of citing existing work, the correct action is to cite that work directly and define no profile.

#### 20.2 Claiming a profile

A package that claims one or more method profiles *MUST* declare them in a `methodProfiles` array in its manifest.
Each element *MUST* be a profile identifier defined in this part or a profile identifier defined outside it as permitted by clause 20.4.
A package claiming no profile *MUST* either omit the array or supply it empty, and the two forms have identical meaning.

Method adherence and package completeness are separate axes and *MUST NOT* be conflated.

The `conformanceProfile` field defined in Part IV states how complete a package is, using the values `afds-tokens`, `afds-components`, and `afds-full`.
It says nothing whatever about method.
The `methodProfiles` array states which method choices the package has adopted.
It says nothing whatever about completeness.

A package can be complete and claim no method profile.
A package can claim every method profile in this part and contain tokens only.
Software reading a package *MUST NOT* infer a value of either field from the other.

The two axes are separated because they answer different questions.
A consumer asking "is there enough here for me to use?" is asking about completeness.
A consumer asking "was this built the way my system is built?" is asking about method.
A single field would have forced those questions together and made both answers less useful.

#### 20.3 A profile is claimed whole

A package *MUST NOT* claim a profile in part.
A package that satisfies some but not all of a profile's requirements *MUST NOT* list that profile in `methodProfiles`.

Partial claims are prohibited because a partial claim cannot be interpreted.
If a package could claim the layout profile while using layout media queries, the claim would tell a reader nothing about the package, and every consumer would have to re-derive from the component contracts what the claim was supposed to summarise.

Adopting a profile's requirements without claiming the profile is permitted, and is expected to be common.
A package *MAY* satisfy any requirement in this part, cite the clause it came from, and record it with the requirement kind that honestly describes its status under clause 13.
Doing so *MUST NOT* be described as claiming the profile, in the manifest or in any human-readable artefact.

A package that adopts most of a profile and departs from it deliberately is in a well-defined position.
It does not list the profile.
It records the departure as a requirement of kind `product-deviation`, names the clause it departs from, and states why.
That is a more informative statement about the package than a partial claim would have been, because it identifies the specific difference rather than leaving a reader to find it.

#### 20.4 Profile identifiers

This part defines four profiles.

| Identifier | Clause | Subject |
| --- | --- | --- |
| `afds-layout-intrinsic` | 21 | Intrinsic, available-space layout built from composable primitives |
| `afds-reflow-scoped` | 22 | The WCAG 1.4.10 two-dimensional exception, and where scrolling is allowed to reach |
| `afds-typography-colour` | 23 | One modular scale for type and space, and colour that does not carry meaning alone |
| `afds-patterns-native-first` | 24 | Native HTML first, recognised interaction patterns second, and a gated catalogue |

An identifier defined in this part *MUST NOT* be used for any other set of requirements.
The identifiers are stable for the life of this major version.

An organisation *MAY* define its own method profile.
An identifier for a profile not defined in this specification *MUST* be namespaced with a prefix that is not `afds-`, so that no reader can mistake a local profile for one defined here.
A profile defined outside this specification *MUST* satisfy clause 20.1, clause 20.3, and clause 20.5, and a package claiming a local profile that does not satisfy those clauses does not conform.

#### 20.5 Provenance

Every profile *MUST* state its provenance.

The statement *MUST* identify four things.

First, what the profile adopts from work outside this project, described specifically enough that a reader can tell which parts are borrowed.
Second, the source of each adopted idea, identified well enough to be found, which for a published work means author and title.
Third, what the profile changes about an adopted idea, including any place where it is stricter than its source or reaches a different conclusion.
Fourth, what originates in the profile itself and has no external source.

The fourth element is the one most likely to be omitted and the most important to include.
A profile that lists its influences and stays quiet about its own inventions leaves a reader unable to tell borrowed authority from asserted authority.
That is the more damaging error of the two, because it launders an untested opinion as settled practice.
Stating plainly that a rule originates here and rests on nobody else's reasoning is not a weakness in the document.
It tells a reader exactly which rules to argue with, and it prevents the profile from lending an external body's credibility to a decision that body never made.

A provenance statement *MUST NOT* attribute a requirement to an external source that does not support it.
Citing a standards body, specification, or published work as the origin of a rule it does not contain is a defect of the same kind as recording an untested result as a passing one, and a package whose profile does so does not conform.

A provenance statement *MUST NOT* be replaced by a bibliography.
A list of references establishes that a document was read.
It does not establish which idea came from where, which is the only thing that makes provenance traceable.

Each profile in this part carries its provenance in its final subclause.
A package claiming a profile defined here inherits that statement and *MUST NOT* be required to restate it.
A package defining a local profile *MUST* supply its own.

#### 20.6 The provenance object

A local profile's provenance *MUST* be carried as a structured object and *MUST NOT* be carried only as prose.

The object has four members, corresponding to the four elements of clause 20.5.

| Member | Type | Required | Content |
| --- | --- | --- | --- |
| `adopted` | array | Yes, *MAY* be empty | What the profile takes from work outside the package |
| `changed` | array | Yes, *MAY* be empty | What the profile alters about an adopted idea |
| `originates` | array | Yes, *MUST NOT* be empty | What the profile asserts on its own authority |
| `statement` | string | No | Prose accompanying the structured members |

Each entry in `adopted` *MUST* record what is adopted, and *MUST* record its source as an object with `author`, `title`, and, where one exists, `uri`.

Each entry in `changed` *MUST* record what is changed, *MUST* reference the adopted entry it changes, and *MUST* record whether the change is `stricter`, `weaker`, or `different`.

A `weaker` value is permitted here and is not a conformance failure.
A profile may legitimately relax something its source requires, and recording that plainly is the point of the member.
What is not permitted is recording such a change as `stricter` or omitting it.

Each entry in `originates` *MUST* record what originates in the profile and *MUST* reference the clause or requirement it applies to.

`originates` *MUST NOT* be empty.
This follows from clause 20.1, which requires a profile to impose at least one requirement the core does not.
A profile with nothing in `originates` is asserting that it adopts everything and adds nothing, and the two statements cannot both be true of a conforming profile.
A validator can therefore treat an empty `originates` as a defect without reading a word of the content.

An entry *MUST NOT* name a source in `adopted` that does not support the thing adopted from it, which is the clause 20.5 prohibition applied to the serialized form.

The structure exists so that provenance can be checked mechanically for completeness, which prose cannot be.
A validator can determine that every `changed` entry references a real `adopted` entry and that `originates` is non-empty.
It cannot determine that an attribution is truthful, and *MUST NOT* be represented as doing so.
That check is a reading task and remains one.

The binding to a manifest field is specified in Part IV.

### 21. The intrinsic layout profile

Identifier: `afds-layout-intrinsic`.

#### 21.1 Statement

> Layout responds to the space actually available to it, not to the width of the viewport.
> Every dimension is expressed so that it moves with the user's settings.
> Interfaces are composed from single-purpose primitives rather than assembled from bespoke per-screen layouts.

#### 21.2 The axioms

A package claiming this profile *MUST* satisfy the following five axioms in every component it contains.

1. The measure *MUST NOT* exceed 60ch, subject to the exception mechanism in clause 23.3.
2. Every dimension *MUST* be user-relative.
   Author-fixed dimensions *MUST NOT* be used, except for hairline borders.
3. Layout *MUST* respond to available space rather than viewport width.
4. An element *MUST NOT* be given a fixed height.
5. Layout *MUST* be complete with JavaScript disabled.

The axioms are stated as absolutes because each one fails in the presence of a single exception.
One fixed height in a shared primitive reintroduces clipping under text-spacing overrides across every screen that uses it, and the primitive's other correctness does not compensate.

Axiom 2 prohibits values frozen against the user's font-size and zoom settings.
It does not assert that the CSS pixel is a badly designed unit.
A CSS pixel is an angular reference measurement, and the objection here is to author-chosen values that cannot move, not to the unit.
A package claiming this profile *MUST NOT* justify author-fixed dimensions on the grounds that the value is small.

Axiom 5 is a layout requirement and not a general prohibition on JavaScript.
A component *MAY* require JavaScript for its interaction.
Its layout *MUST NOT* require JavaScript to be correct, because a layout that collapses before script executes is a layout that fails intermittently on slow connections and permanently when script errors.

#### 21.3 The primitive set

A package claiming this profile *MUST* build layout from single-purpose primitives, each of which does one thing.

The profile adopts twelve primitives.
Each *MUST*, if present in the package, have a component specification conforming to Part II, and *MUST* declare the semantics it does not supply.

| Primitive | Single purpose | Supplies no |
| --- | --- | --- |
| Stack | Vertical rhythm between adjacent siblings | List semantics, grouping, heading structure |
| Box | Intrinsic surface: padding, border treatment, colour inheritance | Semantic role |
| Center | Constrains the measure, with gutters growing outward | Guarantee of visibility in every zoomed context |
| Cluster | Wraps indeterminate groups the way words wrap | Semantics or grouping |
| Sidebar | Two-element arrangement responding to container width | Semantics or landmark |
| Switcher | Switches axis at a container-width threshold | Semantics |
| Cover | Vertical centring with a minimum height | Semantics |
| Frame | Constrains media by aspect ratio | Alternative text or media semantics |
| Grid | Wraps self-contained items by content-driven measurement | Semantics, and no basis for the clause 22 exception |
| Reel | Horizontally scrolling container that acknowledges its overflow | Guarantee that overflowed content is otherwise reachable |
| Imposter | Overlay geometry that cannot trap its own content | Focus trap, modal semantics, focus return |
| Icon | Sizes an icon relative to the text beside it | Accessible name or meaning |

The right-hand column is the operative one.
A layout primitive that silently omits semantics invites a developer to assume semantics were handled, and the omission is only safe when it is declared.
Stack supplies vertical rhythm and not list semantics, and a consumer stacking list content *MUST* supply the list semantics itself.

Two entries carry additional requirements.

Grid arranges self-contained items and creates no header-to-cell relationship.
Clause 11.2 already forbids every package, profile or not, from resting an exception rationale on a layout technique.
What this profile adds is a named consequence: the Grid primitive *MUST* declare in its own specification that it supplies no basis for the claim.
The core forbids the bad rationale; the profile requires the primitive most likely to invite it to say so in advance.

Reel acknowledges overflow rather than concealing it.
Every item in a Reel *MUST* be independently readable within 320 CSS pixels, so that a user scrolls in one direction to reach an item and not in two directions to read one.
Content that leaves the visible region *MUST* remain reachable.

Composition, rather than increasingly capable individual components, produces the interface.
A package claiming this profile *MUST NOT* resolve a layout need by adding configuration options to an existing primitive where composing two primitives would serve.

#### 21.4 Surface delineation under forced colours

A surface described only by a background colour can vanish in a forced-colours mode, because the mode may replace author backgrounds with system ones.

Every delineated surface in a package claiming this profile *MUST* carry a transparent outline with a negative offset in addition to any background colour.
The outline is invisible in normal rendering, occupies no layout space, and becomes visible when a forced-colours mode assigns it a system colour.

The accepted cost is that `outline` is no longer available for unrelated surface decoration, and that every surface carries a declaration whose purpose is invisible in normal use.

A package claiming this profile *MUST* inspect every delineated surface in a forced-colours mode, and *MUST* record the result as evidence under clause 16 rather than as an assertion believed to pass.

#### 21.5 Media queries

A package claiming this profile *MUST NOT* use layout media queries.

Preference queries are permitted, and are the only permitted queries: `prefers-reduced-motion`, `prefers-color-scheme`, `prefers-contrast`, and `forced-colors`.

The distinction is that a preference query asks what the user has asked for, while a layout media query asks how wide the viewport is and then guesses what that implies.
Viewport width does not reliably indicate available space.
A user at 400% zoom, a user with a raised default font size, and a component nested inside a narrow container can all present a component with far less room than the viewport suggests, and no set of breakpoints anticipates the combinations.

Because designing for the web means designing without seeing the final combination, the profile requires programs that respond to space rather than artefacts tuned to named widths.

This axiom has a known unresolved consequence, recorded in clause 21.7.

#### 21.6 Styling tiers and encapsulation

Styles in a package claiming this profile *MUST* be organised so that reach is inversely proportional to specificity: universal and inherited styles first, layout primitives second, utilities last.

A component *MUST NOT* restate an inherited `font-family`, `color`, or `line-height`.
Restating an inherited value breaks the inheritance chain the user's own settings and stylesheets travel down.

Utilities are final adjustments and *MUST NOT* be introduced before a need exists.

Utility-first, breakpoint-prefixed layout is prohibited under this profile, because it encodes a viewport assumption into each individual element and so contradicts axiom 3.

Layout primitives in a package claiming this profile *MUST NOT* use Shadow DOM.

Three reasons support the prohibition.
A shadow boundary complicates the relationships accessible names and descriptions depend on, including `aria-labelledby`, `aria-describedby`, `aria-controls`, and the `for` attribute.
Encapsulation can prevent a user stylesheet or a forced-colours override from reaching the content inside it.
Light DOM permits build-time primitive styles, which is what allows axiom 5 to hold.

The accepted cost is exposure to global style leakage.
The profile accepts it, on the grounds that inherited and user styles *MUST* be able to reach primitive content, and an encapsulation boundary that blocks a user's own stylesheet has defeated a mechanism the user relies on.

#### 21.7 What this profile does not settle

The profile has one known unresolved conflict and *MUST NOT* be read as having resolved it.

Advisory technique C34 un-fixes a sticky header using media queries, so that sticky content does not obscure focus or consume reading space at high zoom.
Clause 21.5 prohibits layout media queries, so the advisory remedy is unavailable under this profile.

Until a container-driven equivalent is designed, a package claiming this profile *MUST NOT* use `position: sticky` or `position: fixed`.

This is a deferral and not a finding.
The profile does not assert that sticky positioning is inaccessible.
It records that this profile cannot currently implement the published remedy, and declines to ship the pattern without one.
A package needing sticky positioning should not claim this profile, and should record its own approach and evidence.

The profile also does not settle whether the 60ch measure of clause 23.3 applies inside a region claiming the clause 22 exception, is reduced there, or is suspended there.

#### 21.8 Provenance

**Adopted.** The intrinsic-layout argument, the axiomatic framing, the composable single-purpose primitive approach, and the twelve primitives named in clause 21.3 are adopted from *Every Layout: Relearn CSS layout* by Heydon Pickering and Andy Bell, at <https://every-layout.dev/>.
The 60ch measure, the modular scale generated by successive `calc()` from a `1rem` root, the Stack primitive's use of an adjacent-sibling relationship rather than per-element margins, the Switcher primitive's container-width threshold technique, and the transparent-outline treatment for forced colours are adopted from the same work.

The adjacent-sibling selector `* + *` that the Stack primitive rests on was introduced as the "lobotomized owl selector" by Heydon Pickering in *Axiomatic CSS and Lobotomized Owls*, A List Apart, 21 October 2014, at <https://alistapart.com/article/axiomatic-css-and-lobotomized-owls/>.
The reasoning that margin is a relationship between adjacent elements rather than a property of an element belongs to that article.

Every Layout is a commercial publication.
This profile describes the method and attributes it.
It reproduces neither the source text nor the source code, and a reader wanting the original reasoning should consult the authors' work.

The requirement that layout respond to available space rather than viewport width is consistent with W3C sufficient technique C31, which treats a Flexbox-based approach as sufficient for WCAG 2.2 Success Criterion 1.4.10, and with technique SCR34 for sizes and positions that scale with text.

**Changed.** Every Layout names a thirteenth primitive, The Container, which this profile does not adopt.
The prohibition on layout media queries in clause 21.5 is absolute in this profile, which is stricter than the source work requires.
Clause 21.3's requirement that every primitive declare the semantics it does not supply is an application of the Part II disclosure obligation and is not a requirement of the source work.

**Originates here.** The following have no external source and rest on this project's own reasoning.

The prohibition on Shadow DOM in layout primitives, and the three grounds given for it in clause 21.6.
The requirement that every delineated surface be inspected in a forced-colours mode and the result recorded as dated evidence rather than assumed, which is this project's evidence discipline applied to a technique borrowed from elsewhere.
The prohibition in clause 21.3 on a Grid-primitive region founding a two-dimensional exception claim.
The Reel requirement that each item be independently readable within 320 CSS pixels, which is stricter than merely permitting horizontal scrolling; it is this project's reading of technique G225 rather than a restatement of it.
The deferral of sticky and fixed positioning in clause 21.7, which is a project judgement in the face of an unresolved conflict and not a published position of any standards body.
The requirement that primitives be tested at 400% zoom, in forced colours, at a doubled root font size, under text-spacing overrides, and inside realistic pages rather than in isolation alone.

### 22. The scoped reflow profile

Identifier: `afds-reflow-scoped`.

#### 22.1 Statement

> Two-dimensional scrolling is permitted only where the content's meaning genuinely requires two axes, is justified by naming those axes, and is confined to the element that needs it.
> It never reaches the page.

#### 22.2 The exception is semantic

WCAG 2.2 Success Criterion 1.4.10 requires content to be presentable without loss of information or functionality and without two-dimensional scrolling, at a width equivalent to 320 CSS pixels for vertically scrolling content and a height equivalent to 256 CSS pixels for horizontally scrolling content.
A width of 320 CSS pixels corresponds to a 1280 CSS pixel starting viewport at 400% zoom.
The criterion excepts parts of the content that require two-dimensional layout "for usage or meaning", and its cited examples include data tables, qualified as "not individual cells".

That the rationale must rest on semantic structure rather than on visual arrangement is a core requirement, stated in clause 11.2 and binding on every package.
This clause adds no requirement.
It explains how the core test resolves in practice, because the test is easy to state and routinely misapplied.

A region qualifies when a cell's significance depends on its relationship to both a row axis and a column axis, so that flattening the structure would destroy meaning rather than merely rearrange appearance.

A CSS Grid container has no table semantics.
Declaring `display: grid`, or wrapping items with a content-driven measurement, creates no row header, no column header, and no header-to-cell relationship.
Visual grid arrangement therefore *MUST NOT* be offered as a basis for the exception.

The table below records how the test resolves for common cases.

| Content | Basis | Excepted |
| --- | --- | --- |
| Results table with genuine row and column header relationships | A cell's significance depends on both axes | Yes, as a scoped region |
| Programme guide organised by channel and time | Channel and time are both meaning-bearing axes | Yes, as a scoped region |
| Collection of self-contained cards | Arrangement is presentational | No |
| Dashboard laid out in grid areas | Arrangement is presentational | No |
| Filter panel beside a results list | Adjacency is convenience, not meaning | No |

The programme-guide row establishes that a meaning-bearing two-dimensional structure need not be a conventional data table.
It *MUST NOT* be read as extending the exception to visual grids generally.

#### 22.3 Claiming the exception

Clause 11.2 requires a rationale resting on semantic two-dimensional structure.
This profile makes that rationale specific.

A component or region in a package claiming this profile *MUST NOT* claim the two-dimensional exception without recording all of the following in its component specification.

The identification of both meaning-bearing axes.
An explanation of how a cell's significance depends on each axis.
A statement of the semantic structure that carries the relationship, which *MUST* be a table structure or an ARIA grid structure, and *MUST NOT* be a purely presentational arrangement.
The boundary of the excepted region, so that a tester knows what is inside the claim and what is outside it.

"It is displayed as a grid" *MUST NOT* be recorded as a justification, and a specification offering it does not conform.

A region needing the exception needs semantic structure first.
Where the semantic structure is absent, the correct response is to supply it or to abandon the claim.
Changing a role in order to qualify is already forbidden by clause 11.2 and is not restated as a profile requirement here.

#### 22.4 Scoping the scroll

An excepted region *MUST* be placed in its own scrollable container.

Two-dimensional scrolling *MUST NOT* reach the page in a package claiming this profile.

Page-level bidirectional scrolling can conform where the content is genuinely excepted, so this requirement is stricter than the criterion.
The profile adopts it because a page-level horizontal scrollbar tells a user that content exists off-screen everywhere, when in fact it exists in one region, and the user is left searching for material that is not there.
Scoping the scroll also allows every surrounding part of the page to reflow normally, which is what clause 22.5 requires.

#### 22.5 Cells and surrounding content

The exception applies to the excepted region and to nothing else.

A heading introducing an excepted region, its surrounding prose, a search field, filter controls, pagination, and any other adjacent interface *MUST* reflow as ordinary content and *MUST* be tested as ordinary content.

An individual cell *MUST* meet the criterion as ordinary flow content, unless it contains material that independently requires two-dimensional presentation for usage or meaning.
The qualification "not individual cells" marks where the semantic two-dimensional relationship stops: the table needs both axes to mean what it means, and the content inside one cell does not depend on either axis in that way.

In a package claiming this profile, a long selector, a URL, a failure description, and a code excerpt appearing in a cell *MUST* either wrap at 320 CSS pixels or provide a mechanism by which a user can reveal the complete value.

A truncated string *MUST NOT* be the only presentation of a value.
Truncation is permitted only where a user can reveal the complete value or reach a complete alternative presentation.

Content *MUST NOT* disappear on reflow without remaining reachable.

Where indentation carries meaning, as in nested lists and code, it *MUST* be reduced under magnification rather than removed.
Whether a particular code cell may wrap or must preserve non-wrapping indentation is a component-level judgement, and clause 22.7 records that this profile does not settle it.

#### 22.6 Recorded techniques

A package claiming this profile *MUST* record, for every reflow assertion, the device, the browser, the starting viewport, and the zoom level at which the observation was made or is to be made.
A reflow result without those four values is not interpretable, because "no content is clipped" is a different statement at a 320 CSS pixel viewport than at a 1280 by 1024 starting viewport with 400% zoom applied.

The profile relies on the following published techniques.

| Technique | Use under this profile |
| --- | --- |
| C31, Flexbox to reflow content | Primary mechanism for the Cluster, Sidebar, and Switcher primitives |
| C33, Reflow with long URLs and strings | Required in table cells |
| C38, Width, max-width, and Flexbox for labels and inputs | Required for filters and forms |
| SCR34, Sizes and positions scale with text | Satisfied by the modular scale of clause 23.2 |
| G224, Meaningful indentation and Reflow | Required wherever indentation carries meaning |
| G225, Horizontally scrolling panels fit 320 CSS pixels | Required for Reel items, read strictly per clause 21.8 |
| G206, Layout alternative without horizontal scrolling | Permitted enhancement for an excepted region; not required |
| C34, Un-fix sticky headers with media queries | Unavailable under `afds-layout-intrinsic`; see clause 21.7 |

C31 is a sufficient technique for Success Criterion 1.4.10 rather than a statement of compatibility with it.
A package claiming this profile and building composition from Flexbox is therefore implementing a technique the Working Group deems sufficient, which is a stronger position than asserting that the criterion is met.

#### 22.7 What this profile does not settle

Success Criterion 1.4.4 Resize Text requires text to be resizable to at least 200%.
The criterion does not require a specific amount of text enlargement at the test condition of Success Criterion 1.4.10, and a 200% zoom producing a viewport smaller than that test condition is not for that reason alone a failure of 1.4.10.
This profile records the distinction and does not rely on it to excuse anything.

Three questions remain open, and a package claiming this profile *MUST NOT* represent them as answered.

Whether an excepted region should also offer a user-selectable alternative presentation without horizontal scrolling, under technique G206.
When code inside a cell needs preserved non-wrapping indentation and when it must wrap.
Whether the 60ch measure applies inside an excepted region, is reduced there, or is suspended there.

#### 22.8 Provenance

**Adopted.** The criterion, its test conditions, the phrase "for usage or meaning", the cited examples, and the qualification "not individual cells" are from W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*, Success Criterion 1.4.10 Reflow, at <https://www.w3.org/TR/WCAG22/>.
The stated intent of preventing users from scrolling back and forth to read enlarged text line by line, and the correspondence between a 320 CSS pixel width and a 1280 CSS pixel starting viewport at 400% zoom, are from W3C WAI, *Understanding Success Criterion 1.4.10: Reflow*, at <https://www.w3.org/WAI/WCAG22/Understanding/reflow.html>.

The techniques named in clause 22.6 are W3C techniques for WCAG 2.2 and are cited as published.

**Changed.** Clause 22.4 is stricter than the criterion.
Page-level bidirectional scrolling can conform where content is genuinely excepted, and this profile prohibits it anyway.
The reason given in clause 22.4 is a usability argument of this project's own and is not a WCAG requirement.

Clause 22.5's treatment of long strings in cells applies technique C33 as a requirement of this profile, where the technique itself is sufficient rather than required.

**Originates here.** The following have no external source.

The reading in clause 22.2 that the exception rests on a semantic relationship rather than a visual arrangement is this project's analysis of the criterion's wording, specifically of "for usage or meaning" together with "not individual cells".
It is a defensible reading and it is not a W3C ruling.
The resolution table in clause 22.2 is this project's application of that reading to cases, and the Working Group has not adjudicated those cases.

The requirement in clause 22.3 that a claim name both axes, explain the cell-to-axis dependency, identify the carrying semantic structure, and state the region's boundary.
The prohibition on "it is displayed as a grid" as a justification.
The prohibition on a Grid-primitive region founding a claim, shared with clause 21.3.
The requirement that every reflow assertion record device, browser, starting viewport, and zoom.

Two corrections are recorded here because a reader is entitled to know the profile changed its mind.
An earlier position in this project treated wide tables at 400% zoom as an unresolved weakness of its layout method; that was wrong, because a table with genuine two-dimensional semantic relationships is excepted, and the real work is scoping the exception correctly.
An earlier wording claimed the exception "covers grid-based UI generally"; that was wrong, because it conflated semantic grid structure with CSS Grid layout.

### 23. The typography and colour profile

Identifier: `afds-typography-colour`.

#### 23.1 Statement

> Type and space are generated from one scale seeded at the user's own text size, so that changing that size moves the whole interface together.
> Colour reinforces meaning and never carries it alone.

#### 23.2 One scale

A package claiming this profile *MUST* generate font sizes and spacing from a single modular scale.

The scale *MUST* be anchored at `1rem`, so that the user's own root font size is the seed for every derived value.
Each point on the scale *MUST* be derived from the preceding point by calculation rather than chosen independently.
Body text *MUST* use a line height of 1.5.

The largest and smallest text on one surface *MUST NOT* differ by more than 3:1.

A font-size or spacing declaration *MUST* reference a scale value, and a literal value *MUST NOT* be used.

The shared seed is the highest-value accessibility property of this profile.
Because type, gaps, and padding all derive from the same root, a user who raises the default text size gets a proportionally larger interface rather than larger text crammed into unchanged spacing.
One line of body text is the natural denominator for vertical rhythm, which is why the line height and the scale ratio are the same number.

The accepted cost is that available sizes are few and widely separated, and that display typography is constrained.

#### 23.3 The measure

The measure is line length expressed in characters.

A package claiming this profile *MUST NOT* allow the measure to exceed 60ch.

The cap *MUST* be applied exception-based: content is capped broadly, and deliberate exceptions are named per container rather than granted by default.
An exception *MUST* be documented, and an undocumented exception fails review.

The measure *MUST* be expressed in `ch` or another font-relative unit and *MUST NOT* be expressed as an author-fixed width.
A character measure cannot be guaranteed by a pixel width, because the number of characters that fits in a fixed width changes as the font size changes.

Because `1ch` varies with font size, text at different sizes occupies different proportions of the same wide container.
That is a consequence of the axiom and *MUST NOT* be treated as a defect.

The measure axiom and Success Criterion 1.4.10 approach one concern from opposite directions.
The axiom limits line length positively, as a typographic commitment.
The criterion prevents unbounded line length under magnification, as a floor.
Satisfying one does not satisfy the other.

#### 23.4 Colour does not carry meaning alone

In a package claiming this profile, status, severity, and any other meaning conveyed by colour *MUST* also be conveyed by text or by shape.
Colour *MUST* be reinforcement only.

An unlabelled colour-coded severity scheme *MUST NOT* be used.

The requirement holds for two independent reasons, and either alone would justify it.
A colour-only encoding is unavailable to users whose colour vision does not distinguish the chosen hues.
A colour-only encoding is also unavailable to any user in a forced-colours mode, because the mode may replace the author's palette entirely, and a distinction carried only by hue does not survive that replacement.

The accepted cost is that interfaces look plainer.

#### 23.5 Contrast

This profile sets its default target level under clause 12.4 at **Level AA**.

A component in a package claiming this profile *MAY* amend that default under clause 12.4, upward or downward, and amending it *MUST* be recorded with a reason.

This profile *MUST NOT* be read as fixing a contrast ratio independently of the declared level.
The applicable ratios are those WCAG 2.2 attaches to the effective target level, and restating them here would duplicate WCAG and would go stale when WCAG does not.

The reason the default is AA rather than AAA is worth stating, because AAA would look like the more rigorous choice.
A profile-wide AAA default would set a threshold this project has not established is usable across data-dense reporting surfaces, and a default that packages routinely amend downward is a worse instrument than a default they can honestly hold.
AAA remains available and is expected to be the right amendment for many components, which is why clause 12.4 makes amending upward as ordinary an act as amending downward.

What this profile does require, independently of the level, is that the claim be measured per pair.

A package claiming this profile *MUST* record, for each foreground and background token pair it treats as valid, the measured ratio and the effective target level that pair was measured against.

A palette-level claim *MUST NOT* be recorded in place of per-pair records.
Contrast is a property of a pair and not of a set, so a claim about a palette is not checkable, and a palette that satisfies a threshold in most combinations satisfies nothing in particular.

There is a known gap here that this profile cannot close.
Design token formats carry values and have no standard expression for the statement that one foreground token is valid on one background token at a given threshold.
Until such an expression exists, a package claiming this profile *MUST* carry its verified pairs as assertions under clause 15, with evidence under clause 16, rather than expecting the token file to express them.

#### 23.6 Typeface

A typeface is treated the same way as a target level: declared by the author, not mandated by the profile.

This profile *MUST NOT* be read as requiring a particular typeface, and it sets no default typeface.

A package claiming this profile *MUST* declare the typefaces it depends on.
It *MUST* declare whether the interface remains usable when they are unavailable.
A component *MAY* declare a typeface dependency of its own, and one that does *MUST* record why the package default is insufficient for it.

No default is set because this project has not settled one.
Atkinson Hyperlegible, published by the Braille Institute, is under consideration and has not been adopted, and clause 23.8 records what is known about it.
Were it adopted later, the mechanism for adopting it already exists: the profile would name it as its default and packages would remain free to amend.

#### 23.7 What this profile does not settle

This profile sets a default target level of Level AA and sets no default typeface.
Neither is a finding about what is sufficient for users.

Whether this project should raise its own default to Level AAA, and whether the 7:1 ratio that Level AAA attaches to body text remains usable on data-dense reporting surfaces, is open.
What is settled is that the answer is a declaration and not a requirement of this specification, so the question can stay open without blocking a package from conforming.

Whether this profile should name a default typeface, and whether that typeface should be Atkinson Hyperlegible, is open.

Whether the 60ch measure applies inside a region claiming the clause 22 exception is also open, and is recorded identically in clause 21.7 and clause 22.7.

#### 23.8 Provenance

**Adopted.** The 60ch measure, the modular scale generated by successive calculation from a `1rem` root, and the practice of deriving spacing and type from one seed are adopted from *Every Layout: Relearn CSS layout* by Heydon Pickering and Andy Bell, at <https://every-layout.dev/>, as recorded in clause 21.8.

The requirement that sizes and positions scale with text is consistent with W3C technique SCR34 for WCAG 2.2.
A line height of 1.5 for body text corresponds to the line-height value that Success Criterion 1.4.12 Text Spacing requires content to tolerate, at <https://www.w3.org/TR/WCAG22/>.

The reasoning that over-long lines make it harder to track from one line to the next, and that this bears particularly on users with dyslexia, low vision, or attention-related disabilities, is the standard argument for a measure cap in typographic practice.
This profile asserts no research finding of its own on the point and quantifies no benefit.

The conformance levels this profile defaults to, and that components may amend to, are the levels defined by WCAG 2.2, at <https://www.w3.org/TR/WCAG22/>.
The 7:1 ratio referred to in clause 23.7 is the Success Criterion 1.4.6 Contrast (Enhanced) threshold that WCAG attaches to Level AAA for body text.
This profile defines no level, no ratio, and no threshold of its own.

The choice of Level AA as the default is not merely this project's preference.
WCAG 2.2 states in its Conformance section that "It is not recommended that Level AAA conformance be required as a general policy for entire sites because it is not possible to satisfy all Level AAA success criteria for some content", at <https://www.w3.org/TR/WCAG22/>.
A profile-wide AAA default would be the general policy WCAG advises against.
The reasoning about data-dense reporting surfaces in clause 23.5 is this project's own application of that advice to its own subject matter, and is not a finding of the Working Group.

Atkinson Hyperlegible is published by the Braille Institute at <https://www.brailleinstitute.org/freefont/>.
The family is offered in three versions, and the original typeface was introduced in 2019.
The download page and the release announcement of 10 February 2025 differ on the name of the monospaced member, which the download page calls Mono and the announcement calls Monospace, at <https://www.brailleinstitute.org/about-us/news/braille-institute-launches-enhanced-atkinson-hyperlegible-font-to-make-reading-easier/>.
This profile records the discrepancy rather than resolving it, because resolving it is the publisher's to do.

**Changed.** Clause 23.3 requires the measure cap to be applied exception-based with documented per-container exceptions, which is a process requirement of this project and not a requirement of the source work.

**Originates here.** The following have no external source.

The 3:1 limit on the ratio between the largest and smallest text on one surface.
No published source is claimed for this figure.
It rests on the argument that a screen-magnifier user should not have to change zoom repeatedly when moving between a heading and the body copy beneath it, and that argument is this project's own.
A reader who wants to challenge one number in this clause should challenge this one.

The requirement in clause 23.5 that contrast be recorded per foreground and background token pair, and that a palette-level claim not stand in for per-pair records.
WCAG requires a ratio to be met and does not say where the measurement is recorded, so the per-pair record is this project's requirement.

The reasoning in clause 12.4 that amending a level downward is a disclosure worth more than a package-wide claim a reviewer must disprove component by component, and the resolution order that makes a component's own declaration govern over a profile default.
WCAG defines the levels; it does not define a mechanism for declaring a target per component and amending it, and that mechanism is this project's.

The requirement in clause 23.6 that a package declare its typeface dependencies and whether the interface survives their absence, and that a component amending the typeface record why the package default is insufficient.
The observation in clause 23.3 that the measure axiom and Success Criterion 1.4.10 address line length from opposite directions and that satisfying one does not satisfy the other.

### 24. The native-first pattern profile

Identifier: `afds-patterns-native-first`.

#### 24.1 Statement

> WCAG establishes the required outcome.
> Native HTML is preferred.
> ARIA fills genuine semantic gaps.
> A published pattern guide supplies the interaction model for recognised custom patterns.
> The package specifies, tests, versions, and evidences the implementation actually shipped.

Each clause does work.

The first fixes the acceptance criteria in a normative standard, so that a disagreement about behaviour resolves against an outcome rather than against a preference.
The second sets the default engineering answer, because native elements arrive with focus behaviour, activation semantics, disabled-state handling, and forced-colours treatment already implemented and already tested by browser vendors.
The third confines ARIA to the repair role it was designed for.
The fourth admits that some interactions have no native equivalent, and that a custom one should behave the way users already expect.
The fifth locates responsibility, because no external document can carry evidence about the code a package actually ships.

#### 24.2 The registry

Clause 9 already requires every component to declare a `derivation.status` from a fixed set of five values, and already imposes the extra obligations that `pattern-adjacent` and `prohibited` carry.
None of that is restated here, and a package that claims no profile is bound by all of it.

What this profile adds is a package-level artefact.

A package claiming this profile *MUST* carry a registry listing every component and pattern in the package against its status.

The registry *MUST NOT* disagree with any component's own declaration.
Where the registry and a component specification differ, the component specification governs and the package is defective.

The registry *MUST* record a `prohibited` entry for a pattern the package has declined, even though no component implements it.

That last requirement is the reason the artefact is worth having, and it is the one thing a set of per-component declarations cannot supply.
A decision not to build something leaves no component behind to declare it.
Without a package-level registry, a prohibition is invisible: the absence of a menubar component looks identical to nobody having considered a menubar, and the argument gets held again in the next review.
The registry is where a package says no once, in writing, and where a reader can see what was rejected as well as what was built.

#### 24.3 Native first

> Use native HTML when it provides the needed semantics and interaction.
> Adopt a published pattern only when a genuinely custom composite widget is required.

The rule is stated as a restriction rather than as an endorsement, because the likeliest failure mode for a system that admires a pattern guide is to turn every familiar interaction into a custom widget.

| Product need | Preferred response | Why |
| --- | --- | --- |
| Action | Native `<button>` | Activation, focus, disabled state, and keyboard behaviour are already provided |
| Choice between options | Native radio or checkbox inputs | Avoids recreating form semantics |
| Navigation | Links inside a navigation landmark | Do not convert site navigation into a menu widget |
| Reveal supplementary content | Native `<details>`, or a button with controlled content | Often avoids a full custom disclosure implementation |
| Modal confirmation | A dialog component following the published dialog model | A genuine composite interaction with focus-management needs |
| Rich autocomplete | A combobox, only where native controls cannot satisfy the task | High complexity; semantics and keyboard contract must be complete |
| Large interactive results table | A native table first; an ARIA grid only where directional cell navigation is genuinely needed | A visual CSS grid is not a semantic grid and does not justify the clause 22 exception |

The rows are ordered from cheapest to most expensive.
In a package claiming this profile, a component *MUST NOT* be given a `pattern-derived` status where a native element in this table would have supplied the semantics and interaction, unless the component specification records why the native element was insufficient.

That last requirement is the profile's counterpart to the Part II disclosure obligation.
Part II requires a package to record the native baseline it considered.
This profile requires it to prefer that baseline.

#### 24.4 Review checklist for a derived component

This subclause is informative and creates no requirement.

It exists because reviewing a derived component means checking twelve things, and those twelve things are distributed across eight core clauses.
A reviewer working from the core alone has to reassemble the list every time, and in practice reassembles it incompletely.

Every item below is required by the clause named beside it.
Clause 20.1 forbids a profile from restating a core requirement, so nothing here is a requirement of this profile, and removing this profile's claim removes none of these obligations.

| Review item | Required by |
| --- | --- |
| 1. The published pattern it derives from, with its source URL | 9.3 |
| 2. The native alternative considered, and why it was insufficient | 9.3 |
| 3. Every deviation from the pattern, with reason and cost | 9.3 |
| 4. Whether the pattern is support-dependent, and its reassessment trigger | 9.3, 9.5 |
| 5. The semantic model | 8 |
| 6. The keyboard contract | 10 |
| 7. The focus lifecycle | 10.4 |
| 8. Pointer and touch parity, and speech-recognition operation | 10.2 |
| 9. Reflow behaviour, and any two-dimensional exception claim | 11, 11.2 |
| 10. The WCAG success criteria the component affects | 12 |
| 11. Assistive-technology evidence for its claims | 16 |
| 12. Its guarantees, non-guarantees, and recorded uncertainty | 14, 17 |

A specification missing any of the twelve is incomplete under the core, not under this profile.

These twelve review items are written for engineering review.
They are not the eleven design-tool annotation fields of clause 19, which are written for design handoff.
The two lists overlap in subject and differ in audience, count, and purpose, and a count of one is never a count of the other.

#### 24.5 Two cautions

Two cautions are strong enough to belong in the profile itself.

**Menu and menubar are not for ordinary navigation or action lists.**

Accuracy about the pattern's scope comes first, because the temptation is to overstate the case.
The published menu and menubar pattern is not restricted to application menus, and the pattern guide ships a navigation menubar example demonstrating site navigation.
Using a menubar for site navigation is therefore a sanctioned use of that pattern and *MUST NOT* be described as a misuse of it.

The caution stands as a convention of this profile with a stated cost, which is the honest form for it.
Adopting a menubar for ordinary navigation imports the whole composite contract: a roving-focus model, a single tab stop, author-managed arrow-key movement, submenu open and close behaviour, and a role that causes a screen reader to describe the thing as a menu rather than as navigation.
This profile judges that cost unjustified where a list of links inside a navigation landmark already gives users a structure they know and costs nothing to maintain.
A list of buttons is usually an action group, and a toolbar is the cheaper composite where one is genuinely warranted.

A package claiming this profile *MAY* nonetheless adopt a menubar, and if it does, the justification *MUST* appear in the component's specification, tagged as a `product-deviation` under clause 13, with the keyboard contract written out in full.

**An ARIA grid is not a remedy for visual density.**

A grid widget is justified by a need for directional cell navigation and *MUST NOT* be justified by a table looking crowded or by a wish to avoid reflowing content.
Where the underlying difficulty is that a wide table is hard to use at high zoom, the response is a scoped scroll container and a correctly justified exception under clause 22, and *MUST NOT* be a role change.

#### 24.6 The catalogue and its gates

A package claiming this profile *MUST NOT* implement a pattern catalogue larger than the product needs.

The profile defines an ordered catalogue.
Priorities 1 to 5 *MAY* be adopted on judgement.
Priorities 6 to 8 *MUST NOT* be adopted without a recorded justification, and the justification *MUST* be recorded at the time the gate is passed rather than reconstructed later.

| Priority | Pattern or primitive | Gate |
| --- | --- | --- |
| 1 | Native button, link, checkbox, radio, text input, select | None |
| 2 | Disclosure | None |
| 3 | Dialog | None |
| 4 | Alert and status messaging | None |
| 5 | Native table with a scoped scroll container | None |
| 6 | Tabs | Recorded finding that persistent peer views improve a task |
| 7 | Combobox | Recorded finding that a large controlled vocabulary must be searched |
| 8 | Tree, treegrid, or ARIA grid | Recorded user research demonstrating the need |

The ordering is deliberate.
Priorities 1 to 5 consist almost entirely of native elements and one simple composite, and in an audit and remediation product they cover the core work.
Priorities 6 to 8 carry complex keyboard and assistive-technology contracts, and each unused composite adds untested surface.

Visual density *MUST NOT* be recorded as the gate justification for priority 8.

#### 24.7 What this profile does not settle

A package claiming this profile *MUST NOT* claim conformance to any pattern guide, and *MUST NOT* present adherence to this profile as evidence that a service is accessible.
Clause 4.4 states both prohibitions for every package, and they are recalled here because this profile is where the temptation arises.

The catalogue in clause 24.6 is sized for an accessibility audit and remediation product.
It is not a general recommendation, and a package with a different purpose should expect a different catalogue.

Whether the pattern guide this profile leans on should be adopted by reference as a project-wide position, rather than only inside this profile, is an open question in this project and is not settled by this clause.

#### 24.8 Provenance

**Adopted.** The interaction models, keyboard expectations, and pattern definitions this profile refers to as published patterns are those of the W3C ARIA Working Group, *ARIA Authoring Practices Guide (APG)*, at <https://www.w3.org/WAI/ARIA/apg/>, with the pattern index at <https://www.w3.org/WAI/ARIA/apg/patterns/>.

The APG is informative and has no conformance model, which is why clause 24.7 prohibits claiming conformance to it and why the fifth clause of the statement in clause 24.1 places evidence in the shipping layer.

The scope statements in clause 24.5 about the menu and menubar pattern, including the existence of a navigation menubar example demonstrating site navigation, are the APG's own, at <https://www.w3.org/WAI/ARIA/apg/patterns/menubar/>.
The characterisation of the grid pattern as covering both tabular information and layout containers is the APG's own; the pattern is titled "Grid (Interactive Tabular Data and Layout Containers)" in the pattern index.

The required outcomes this profile defers to are W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*, at <https://www.w3.org/TR/WCAG22/>.
The repair role assigned to ARIA in clause 24.1 reflects W3C, *Accessible Rich Internet Applications (WAI-ARIA) 1.2*, at <https://www.w3.org/TR/wai-aria-1.2/>.
The native elements preferred in clause 24.3 are those of WHATWG, *HTML*, Living Standard, at <https://html.spec.whatwg.org/multipage/>.

The judgement that a design system is the right layer at which to hold accessibility responsibility is supported by Putnam, Rose and MacDonald's study of accessibility in user-experience practice, in which design systems were the most frequently reported concrete action, at <https://doi.org/10.1145/3575662>.
That study also warns that concentrating responsibility in specialist teams risks abdication elsewhere, and this profile does not claim the paper endorses its approach.

**Changed.** The five-clause statement in clause 24.1 is this project's formulation.
No external body states it, and it *MUST NOT* be attributed to the W3C or to any working group.

The registry status names in clause 24.2 are deliberately method-neutral.
Earlier drafts in this project named them after the APG specifically, and they were renamed so that the core vocabulary of clause 9 does not presuppose one pattern guide.

**Originates here.** The following have no external source.

The five-status registry vocabulary, the requirement that every component carry exactly one status, and the definitions of `pattern-adjacent` and `prohibited`.
Those originated in this project and have since been moved into the core at clause 9, so they are no longer this profile's to claim; they are recorded here because this is where they were devised.
The package-level registry artefact of clause 24.2, and the requirement that a declined pattern be recorded as a `prohibited` entry even though no component implements it.
The grouping of twelve review items in clause 24.4, which is this project's consolidation and not a list published anywhere else.
The requirement in clause 24.3 that a component *MUST NOT* be derived where a listed native element would have served unless insufficiency is recorded, which is the design rule that Part II deliberately declined to impose.
The caution against menubar for ordinary navigation in clause 24.5, which is a project convention with a stated cost and not a position of the ARIA Working Group; the APG sanctions the use this profile declines.
The caution against adopting an ARIA grid for visual density.
The catalogue in clause 24.6, its ordering, and the gates on priorities 6 to 8.

One correction is recorded because a reader is entitled to know the profile changed its mind.
An earlier framing in this project treated the APG as the component layer of the design system.
That was wrong in kind, because the APG describes patterns while a design system ships versioned artefacts with tests and evidence, and only the latter can be held to account.
The status `pattern-adjacent` was added specifically because the earlier framing left no honest label for a component resembling a pattern without implementing it.

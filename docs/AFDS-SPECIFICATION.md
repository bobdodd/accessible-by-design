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

Each entry *MUST* record the criterion number, its name, its conformance level, its branch under clause 12.2, its relationship under clause 12.3, and a note.

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

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

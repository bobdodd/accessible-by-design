<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# AFDS user guide

A guide to Accessibility Focused Design Systems, for the designers, developers and testers who have to use one.

This guide explains what a design system is, why this project treats accessibility as the reason the system exists rather than a feature it happens to include, and then works through every part of AFDS: how a package claims conformance, what a component declares about itself and refuses to promise, the records that make a claim checkable, the optional method profiles that carry one way of designing, and the `.afds` package that carries all of it from one organisation to another.
It assumes no prior knowledge of design systems, design tokens or WCAG.

## Status of this guide

This guide is informative documentation.
It issues no requirements of its own.

`docs/AFDS-SPECIFICATION.md`, *AFDS specification, version 1.0.0*, is the normative source of truth for all four of its Parts.
Where this guide and the specification disagree, the specification wins and the disagreement is a defect in this guide.

Every statement of obligation here carries the clause it comes from, so that a reader can always get from an instruction in the guide to the normative text behind it.

The project's research notes, its colophon of decisions and its register of open questions are not part of the specification and are not authority for what conforms.
Clause 1.4 places them: they record how the decisions here were reached, which were rejected, and what remains unsettled.
Read them for why a requirement exists.

This guide replaces an earlier version written before the specification was completed.
Where the earlier text said something the specification now contradicts, the correction is noted in place rather than made silently.

## Part 1. Before you start

### Who this guide is for

This guide is written for three readers at once, and it assumes none of them has worked with a design system, with design tokens, or with WCAG before.

A **designer** decides what an interface looks like and how it behaves.
A **developer** builds it.
A **tester or QA engineer** decides whether what was built is acceptable.

The specification names its own audiences slightly differently, and it is worth seeing both lists side by side, because the mapping tells you which parts of the specification you will actually need.
Clause 1.3 names three audiences and what each needs from the document.

| Audience named in clause 1.3 | What that audience needs | Which of this guide's three readers it covers |
| --- | --- | --- |
| The author of a tool that produces or consumes AFDS packages | Part IV, and the record definitions in Part II | Usually a developer, and only one building tooling rather than an interface |
| The designer or engineer adopting the system inside an organisation | Parts I to III, with the obligations that affect daily work in Part II | The designer and the developer |
| The reviewer deciding whether a package conforms | Clause 4, which says what a conformance claim consists of, and the verification algorithm in Part IV | The tester or QA engineer, when the thing under test is a package rather than a screen |

So the three readers this guide addresses are not a fourth and fifth audience added to clause 1.3's list.
They are the same three people, described by the job they do rather than by the part of the document they consult.

Beyond that mapping, here is where each reader will find most of what they need.

A designer needs the design-system layers and the placing exercise below, the token and branding material, the layout method, and the annotation rules that record what a mock-up cannot show.

A developer needs the layout primitives, the component contract and its required fields, the keyboard and focus material, and the whole of the package format, because that is what a build consumes and verifies.

A tester or QA engineer needs the assertions, the testing levels, the assistive-technology evidence records, and the requirement to test inside a realistic page rather than in isolation.

You do not need to read this guide in order.

Its ordering is not the specification's ordering.
The specification is organised as an argument that ends in a serialisation format: purpose, model, conformance, the component contract, the method profiles, then the package (front matter, *Organisation*).
This guide is organised around tasks, so a section that draws on clause 7 may sit next to one that draws on clause 29.
Each section states the problem it addresses before it explains the mechanism, and each section that carries an obligation names the clause behind it, so you can enter anywhere and follow the citation outward.

### How to read this guide alongside the specification

Keep `docs/AFDS-SPECIFICATION.md` open while you read.
This guide is documentation and carries no requirement of its own.
Where the guide and the specification disagree, the specification wins and the disagreement is a defect in the guide.

#### Clause numbers are the citation mechanism

Every instruction in this guide that rests on a requirement cites the clause it rests on, inline, in the form `(clause 7.2)`.
That is possible because clause numbers are global and permanent within a version of the specification: clause 23 is clause 23 wherever it is rendered, so a citation never has to name a part or a page, and when the specification is published as web pages each clause carries a stable anchor derived from its number (front matter, *Organisation*).
If a sentence here tells you to do something and does not cite a clause, treat it as advice rather than as an obligation.

The specification is one document in four parts.
Part I, clauses 1 to 6, states what an AFDS is, why it exists, the model it assumes, how conformance works, and the terms and references the rest depends on.
Part II defines the component contract.
Part III defines the method profiles, which carry this project's own choices about layout, reflow, colour, typography, and the component catalogue.
Part IV defines serialisation: the container, the two root artefacts, the verification algorithm, security requirements, adapters, profiles, and versioning.

Not all of it binds equally.
Clause 4, clause 5, and Parts II and IV are normative.
Part III is normative only for a package that claims the relevant method profile, and has no force over a package that does not.
Clause 1, clause 2, clause 3, clause 6.2, and the annexes are informative: they explain why the normative clauses say what they say, they create no requirement, and a package cannot fail to conform by disagreeing with them (front matter, *Normative and informative material*).
Most of this section of the guide draws on those informative clauses, which is why it argues rather than instructs.

#### What the capitalised keywords mean, and what the lower-case ones do not

The specification uses *MUST*, *MUST NOT*, *REQUIRED*, *SHALL*, *SHALL NOT*, *SHOULD*, *SHOULD NOT*, *RECOMMENDED*, *MAY*, and *OPTIONAL* as defined in RFC 2119 (clause 4.1).
Capitalised, they carry force: an absolute requirement, an absolute prohibition, a strong expectation whose departure needs a stated reason, or a genuine option that a consumer may not assume is present.

Two things follow for a reader of this guide.

The first is that clause 4.1 says a reader who encounters one of those words in lower case must read it as ordinary prose carrying no requirement.
This matters, because the informative clauses — clause 2 and clause 3 among them — use "must" and "should" in their ordinary English sense.
A lower-case "must" in clause 2 is a sentence about how design work tends to go, not a rule you can fail.

The second is that this guide never issues a requirement in its own voice.
It writes "the specification requires that", or "a package that omits this does not conform", and it names the clause.
Where it quotes a capitalised keyword it marks the quotation as a quotation.
The capitalisation is the signal that carries the force; clause 4.1 also marks keywords as emphasis, and says the emphasis is deliberately redundant, so that a reader or an assistive technology conveying no emphasis loses nothing.

#### The reference for a term is clause 5

This guide explains a term before relying on it, but the authoritative wording for every defined term, including *Accessibility Focused Design System* itself, is clause 5, and where a term defined there is used in a normative clause it carries that meaning and no other.

#### The project's other documents are history, not authority

The project's research notes, its colophon of decisions, and its register of open questions are not part of the specification (clause 1.4).
They record how the decisions were reached, which were rejected, and what remains unsettled.
When you want to know why a requirement exists, the argument is in clause 2 and the decision record is in the colophon; when the two are read against each other, the specification governs.
Where the specification is silent on something the project has not decided, clause 1.4 says the silence is deliberate and the open-questions register names it, and that a silence in a specification is not permission.

One further piece of status, because it changes how much weight the identifiers here can carry.
AFDS 1.0.0 is a project draft.
It is not a W3C standard, not a published industry specification, and not on any standards track, and every identifier and field name it defines is stable within this project and unstable outside it (front matter, *Status of this document*).

### What the specification defines, and what it leaves to others (clauses 1.1, 1.2)

The specification opens with a single sentence of purpose worth keeping in view through everything that follows: an AFDS exists so that an accessibility decision, its reasoning, and the evidence for it can be made once and then travel, instead of being rediscovered on every screen that needs it (front matter).

Clause 1.1 lists nine things the specification defines.

1. The layers a design system is composed of, and what belongs in each.
2. What a component declares about itself, including what it refuses to promise.
3. The record types that carry evidence, uncertainty, and machine-checkable assertions.
4. The keyboard contract model, and the sense in which keyboard operation is not only about keyboards.
5. The levels at which conformance is tested, and the difference between a component conforming and a composition conforming.
6. A set of named method profiles carrying a layout method, a reflow policy, a colour and typography policy, and an approved component catalogue.
7. A container and package hierarchy for carrying all of the above between organisations, with a verification algorithm and security requirements.
8. Adapter obligations in both directions, and the report an adapter must produce.
9. Versioning behaviour for the format and for the payload.

Clause 1.2 is as explicit about the other side.
It makes five statements of exclusion, naming twelve things between them.

| What the specification does not define | The reason clause 1.2 gives |
| --- | --- |
| The internal schema of a design-token file | That is the business of the Design Tokens Format Module, and a package declares which version of it applies |
| A visual style, a brand, or a set of palette values | Except within a method profile, which a package may decline to claim |
| A signature format, a package registry, an update protocol, or an editing tool | Not stated; these are ecosystem concerns rather than format concerns |
| An implementation language, a component framework, or a rendering engine | A conforming package may contain an implementation, and may contain none |
| A service being accessible | Clause 2.5 states that limit and its reasons, because a specification that left it implied would be making a claim it cannot support |

The third and fourth rows are the ones that surprise people, and the fourth is worth restating on its own, because it decides what you are allowed to ship.
A conforming package may contain an implementation, and may contain none.
A package of tokens, contracts, evidence, and no code at all can conform.
So can one that carries a working component library.
The format is indifferent to the choice, and the exclusion of the third row's items — signature format, registry, update protocol, editing tool — means an organisation adopting AFDS is expected to bring its own distribution and tooling arrangements.

## Part 2. What a design system is, and why accessibility drives this one

### What a design system is

Consider how design work happens without a system.

A designer needs a warning message, so they choose an orange, a spacing value, and an icon.
Three weeks later another designer needs a warning message on a different screen, and chooses a slightly different orange and slightly different spacing.
A developer implements both, writing the colour twice.
A tester finds that one of the two oranges fails contrast against its background, files a bug against that one screen, and the other screen keeps its failing orange because nobody knew the two were related.
Six months later the brand changes, and somebody has to find every orange by searching the codebase.

Nothing in that story is incompetence.
It is what happens when a decision has nowhere to live except inside the artefact that used it.

A design system gives each decision a home, a name, and a version (clause 2.1).
That is the whole of the mechanism.
Everything in the specification follows from wanting it to hold for accessibility decisions specifically.

### The five layers

The specification treats a design system as five layers, and clause 3.1 makes the observation that gives the model its practical value: when people argue about whether something belongs in the design system, they are almost always arguing across two of these layers without noticing.

The table below is clause 3.1 as the specification gives it.

| Layer | Contents | Accessibility role |
| --- | --- | --- |
| Principles | Commitments and non-negotiables | Sets the floor and the constraints that may not be traded away |
| Tokens | Named platform-neutral values | Space, type, colour, motion, and contrast-pair candidates |
| Layout primitives | Composable arrangement rules | Reflow, resize, text spacing, reading sequence |
| Components | Interactive elements with semantics and behaviour | Roles, names, states, keyboard, focus |
| Patterns and guidance | Multi-component flows and documentation | Errors, focus management, workflow behaviour |

#### Reading the layers

Read them from the top down as decreasing generality (clause 3.2).

A principle applies everywhere and is not negotiable per screen.
A token is a value with a name.
A layout primitive arranges things and does not know what they mean.
A component is an interactive thing that does know what it means.
A pattern is several components co-operating through a task.

The ordering is not a hierarchy of importance.
It is a hierarchy of scope, and the practical use of it is that it tells you which layer a question belongs to before you try to answer it (clause 3.2).
A layer is not more valuable for sitting higher in the table; it is only broader in reach.

#### Placing one decision in the layers

Take the warning message from the story above and place it (clause 3.3).

| The decision | Its layer |
| --- | --- |
| Severity is never communicated by colour alone | Principle |
| The specific warning colour, and the space around the text | Tokens |
| The arrangement of icon, heading, and body text | Layout |
| The container that announces itself to a screen reader when it appears | Component |
| Where focus goes after the user dismisses it | Pattern |

Confusing the layers is the source of many scope disputes, and the size of a question is often mistaken as a result.
Can the warning be red is a token question.
Should the warning steal focus is a pattern question, and it is a far larger one, because the answer changes what happens to the user's place in the page.

If you take one working habit from this section, take that one: name the layer before you argue about the answer.

#### Three things a design system is not (clause 3.4)

Clause 3.4 rules out three things a design system is regularly confused with.

It is not a component library alone.
A library gives you code.
A system also gives you the reasoning, the tests, and the record of what has and has not been verified, which is what lets somebody else trust the code.

It is not a style guide alone.
A style guide tells you what things look like.
It does not tell you what a component promises, what it refuses to promise, or which keys operate it.

It is not a design-tool file alone.
A mock-up records an outcome without recording the decision that produced it, which is why the outcome drifts as soon as two people need it.

The third is the one most often left out, and it is the one that catches designers hardest.
A file that shows the finished warning message shows the orange without showing why that orange, so the next person who needs a warning message has to decide again.

### Why accessibility is the reason this system exists

Most design systems treat accessibility as a quality that components can have.
This specification treats it as the thing the system is for, and clause 2.2 says plainly what follows from that: it changes what the system has to record.
The whole of Part II — the declarations, the evidence records, the recorded uncertainty — exists because of that one shift.

#### The retrofit cycle treats symptoms

Accessibility work is commonly retrofitted: build, audit late, patch individual findings, repeat.

That cycle treats symptoms.
A finding fixed on one page recurs on the next page that uses the same component, because the fix was applied to an instance and the instance is not where the decision lives.
Attaching requirements to reusable components and patterns instead means a fix and its reasoning propagate to everything built from them (clause 2.2).

That is the same mechanism as the warning-message story, applied to a different kind of decision.
A colour with nowhere to live is duplicated by accident.
A contrast fix with nowhere to live is duplicated by hand, once per screen, forever.

#### Accessibility is split two ways, for a diagnostic reason

Accessibility does not sit in one module, which is what makes it easy to lose.
Clause 2.2 splits it in two.

| Branch | What it covers |
| --- | --- |
| User technology support | Assistive-technology compatibility: roles, accessible names, states, focus, and keyboard operation |
| User layout support | Reflow, measure, spacing, contrast, and reading order |

Every criterion recorded against a component names which branch it belongs to.

The reason is diagnostic, and it is worth being precise about it, because the split looks like bureaucracy until you have used it.
A flat list of criteria per component hides whether a failure is geometric or semantic, and those two failures have different owners and different fixes (clause 2.2).
A component whose text collides at 400% zoom and a component whose state is never announced are both "failing", and a single undifferentiated list says so in the same words.
Branch the list and the first goes to whoever owns the layout primitive, the second to whoever owns the semantics.

The split needs judgement rather than mechanical application.
The clearest case is the reflow exception, which looks like a layout matter and is decided by semantics (clause 2.2).
Classification follows what carries meaning, not the visual mechanism that produced the appearance.
The mechanics of that exception belong to clause 11.2 and to the scoped reflow profile at clause 22, which another section of this guide covers.

#### The honest cost

There is a cost, and clause 2.2 records it rather than leaving a reader to discover it.

An organisation without a design system cannot adopt this method directly, because it must first identify its de facto components.

That work is unglamorous and it is not optional.
Requirements attach to components, so an organisation with no named components has nothing for them to attach to, and the first task is to look at what has already been built and give the repeated things names.

### What the survey evidence supports, and what it does not

There is survey evidence for the shift towards design systems, and clause 2.2 gives it with figures.

The source is Putnam, C., Rose, E. J. and MacDonald, C. M. (2023).
"It could be better. It could be much worse": Understanding Accessibility in User Experience Practice with Implications for Industry and Education.
*ACM Transactions on Accessible Computing*, 16(1), 1-25.
<https://doi.org/10.1145/3575662>.
The paper is listed among the specification's informative references at clause 6.2.

The authors analysed 58 interview sessions with user-experience practitioners between 2017 and 2020.

| Finding, as clause 2.2 gives it | Figure |
| --- | --- |
| Design systems, the most cited of the four concrete actions the paper identifies | Named in 28 sessions (48%) |
| Design-system adoption at the start of the fieldwork | 2 of 6 sessions in 2017 (33%) |
| Design-system adoption at the end of the fieldwork | 22 of 42 between November 2019 and March 2020 (52%) |
| Inclusion of people with disabilities in usability testing | Cited in 18 sessions (31%) |
| Training | Cited in 7 sessions (12%) |
| Code considerations | Cited in 5 sessions (8%) |

Those figures are the encouraging half, and quoting only them would misrepresent the paper.
Clause 2.2 records two findings from the same research that constrain what the project may claim from it, and it records them rather than smoothing them over.

**The first is that concentrating responsibility is itself a failure mode.**
The groups most cited as responsible for accessibility were dedicated teams or specialists and engineers or developers, and the paper warns that resting responsibility there can produce an attitude that accessibility is someone else's problem.
A design system can concentrate responsibility in exactly the same way, if it becomes the place where accessibility is assumed to have been dealt with already (clause 2.2).
That is a warning about this project's own mechanism, not about somebody else's, and it is the reason the specification insists a component declare what it refuses to promise rather than only what it promises.

**The second is a recorded disagreement.**
On audit and compliance the paper reads its findings as indicating a need for rigorous regulation, which is not the direction this project's argument runs, and clause 2.2 records the disagreement rather than smoothing it over.
The project's answer is portable evidence and declared limits rather than regulation, and the specification does not pretend the paper endorses that choice.

Read together, the evidence supports the shift and refuses to underwrite it.
A design system is where the project thinks accessibility decisions should live; the same research says that giving decisions a home is not the same as making anyone responsible for them.

### The five gaps the project recorded

The project surveyed existing practice and recorded five recurring gaps (clause 2.3).
Each is the reason a later part of the specification exists, so they are worth reading as a list of problems rather than as criticism of anyone's work.

1. Layout is treated as a visual concern rather than an accessibility concern, despite reflow, resize text, and text spacing being layout criteria.
2. Components are tested in isolation but not in composition.
3. Assistive-technology claims omit engine, browser, version, observed behaviour, and test date.
4. Tokens express values but not constraints or relationships.
5. Documentation does not carry machine-readable assertions, and drifts from the implementation.

A sixth sits slightly apart, and clause 2.3 says so explicitly rather than folding it into the five.

A common readiness model asks whether a component is visually accessible, screen-reader compatible, operable, and understandable.
That is useful and incomplete, because it does not record which engines were tested, and does not address reflow, zoom, text spacing, or forced colours (clause 2.3).
The four-category model of that shape which the project examined is the component scorecard in vendor guidance of the kind Supernova publishes, recorded in the project's design-systems research note as Romero, C., *Accessibility in Design Systems: A Comprehensive Approach Through Documentation and Assets*, Supernova, <https://www.supernova.io/blog/accessibility-in-design-systems-a-comprehensive-approach-through-documentation-and-assets>.

The sixth gap is the one to watch if your organisation already has an accessibility checklist.
A checklist that produces four green ticks and no record of which browser and screen-reader engine produced them has recorded an opinion, not evidence.

### What the specification adds

Against those gaps, clause 2.4 states what the specification contributes.
There are seven items.

1. Layout as a first-class accessibility concern inside the system rather than alongside it.
2. Intrinsic primitives that respond to available space rather than to breakpoint guesses.
3. Engine-qualified assistive-technology claims, with uncertainty recorded explicitly rather than omitted.
4. Assertions that travel with specifications, so a claim can be checked mechanically.
5. Composition conformance as well as component conformance.
6. A documented gap in token standards around contrast relationships, stated as a gap rather than papered over.
7. A portable package that carries the accessibility contract, its evidence, and its uncertainty as first-class records, rather than leaving them in a design tool or an untracked spreadsheet.

Items 1 to 5 answer gaps 1 to 3 and 5 fairly directly.
Item 6 is the odd one, and deliberately so: it is an addition that consists of admitting something is missing.
Item 5 is the one with the most consequence for a tester, and the requirement behind it is clause 18.2, which another section of this guide covers.
The analysis of what goes wrong when accessible parts are assembled — the assembly hierarchy, the compositional failure modes, state propagation, and testing across the hierarchy — is carried by the companion document *Component Design Frameworks and the Assembly Problem* (`research/COMPONENT-FRAMEWORKS.md`).

### What a design system cannot do

A design system is not an accessibility guarantee, and clause 2.5 says so in the same plain terms the strongest public example uses.

The GOV.UK Design System states on its accessibility page that using the system does not immediately make a service accessible ([GOV.UK Design System, *Accessibility*](https://design-system.service.gov.uk/accessibility/)).
The specification adopts that limit as its own (clause 2.5).

The reason is structural rather than a matter of quality.
A design system supplies parts.
It cannot know whether the parts were assembled in an order that makes sense, whether an error message explains anything, or whether the task built from them is one a user can complete.

The consequence is worth stating as bluntly as clause 2.5 states it.
A perfectly accessible set of components can be assembled into an unusable page, and every component will pass its own tests while that happens.
That is not a hypothetical about careless teams; it is a property of composition, examined at length in the companion document *Component Design Frameworks and the Assembly Problem* (`research/COMPONENT-FRAMEWORKS.md`), which treats accessibility as not closed under composition.

What a system can do is improve the available user-interface resources and modalities, and record honestly what has and has not been verified.
It cannot replace research with disabled users, assistive-technology testing, content quality, or contextual judgement (clause 2.5).

This is why Part II requires non-guarantees.
A component that lists only what it promises invites the reader to assume the rest, and the assumption is where accessibility is lost (clause 2.5).
The mechanism that carries that requirement is the non-guarantee record at clause 14, which another section of this guide covers; what matters here is that it exists because of this limit and not as an afterthought to it.

The limit also constrains what you may say about a package you have built.
Clause 4.4 turns it into a prohibition on producers, and the conformance sections of this guide give it in full.

## Part 3. Conformance, claims, and the three axes

### Conformance: what conforms, what a claim means, and the words behind it

This section serves all three readers, and it serves the tool author most of all.
A designer needs it to know which of the project's design methods are optional.
A developer needs it to know which obligations attach to writing a package and which to reading one.
A tester needs it to know what a conformance claim does and does not entitle anyone to say.

Everything here comes from clause 4 (Conformance), clause 5 (Terms and definitions), clause 34 (Completeness profiles) and clause 35 (Versioning).
Clause 4 and clause 5 are normative, and they are part of the core, so nothing in this section is declinable.

#### How to read a requirement, and why this guide never issues one

The specification marks its obligations with capitalised keywords from RFC 2119, and clause 4.1 fixes the force of each one.
The right-hand column below quotes clause 4.1 directly.

| Keyword | Force in the specification (clause 4.1) |
| --- | --- |
| *MUST*, *REQUIRED*, *SHALL* | "An absolute requirement. A package or tool that breaks it does not conform." |
| *MUST NOT*, *SHALL NOT* | "An absolute prohibition." |
| *SHOULD*, *RECOMMENDED* | "A strong expectation. Departing from it requires a stated reason, and has consequences that the departing party owns." |
| *SHOULD NOT* | "A strong expectation against. Doing it anyway requires a stated reason." |
| *MAY*, *OPTIONAL* | "Genuinely optional. A consumer *MUST NOT* assume the optional behaviour is present." |

Two consequences of clause 4.1 matter to a reader more than the table does.

The first is that the capitalisation carries the meaning on its own.
The specification also marks keywords as emphasis, and says so plainly: the emphasis is "deliberately redundant", so a reader, a renderer or an assistive technology that conveys no emphasis loses nothing (clause 4.1).
No requirement in the specification depends on colour, typographic weight, or emphasis being perceived.
That is worth noticing early, because it is the specification applying its own subject matter to itself.

The second is that lower-case "must" and "should" in the specification carry no requirement at all.
Clause 4.1 is explicit that a reader who meets one of the keywords in lower case reads it as ordinary prose, and it gives the reason: the informative clauses use those words in their ordinary English sense.

This guide is informative documentation, not specification.
It therefore never issues a requirement in its own voice.
Where an obligation exists, this guide reports it and cites the clause — "the specification requires that", or "a package that omits this does not conform (clause 34)" — so that you can always get from an instruction here to the normative text behind it.
Capitalised keywords appear in this guide only inside quotations, and quotations are marked as quotations.

#### Who carries the obligations: producers and consumers

Clause 4.2 says two roles carry obligations, and defines both.

A **producer** is any tool or person that creates a package.
A **consumer** is any tool or person that reads a package and relies on its contents.

The rule that matters if you are building tooling is the next sentence of clause 4.2: a single tool may be both, and when it is, the specification requires it to satisfy both sets of obligations independently.
"Independently" is the operative word.
Satisfying the producer obligations does not discharge any consumer obligation, and satisfying the consumer obligations does not discharge any producer obligation.
A build tool that reads an upstream package of tokens and emits a package of its own is held to the reading rules for what it consumed and to the writing rules for what it produced, with no netting off between the two.

Clause 4.2 also settles the case that catches people out: an adapter is always both.
An import adapter reads a non-AFDS representation and produces a package; an export adapter reads a package and produces something else.
Either way it sits on both sides of the boundary, which is why Part IV gives adapters their own clause (clause 33).

Practically, if you are writing tooling, treat the two obligation sets as two separate checklists and satisfy each on its own terms.
The most common way to get this wrong is to write a tool that verifies its own output carefully and reads its input trustingly.

#### What every package must satisfy, and what it may decline

This is the most important part of this section, and it is the part the previous edition of this guide got structurally wrong.

The specification has a core and a set of named method profiles (clause 4.3).

The **core** is clause 4, clause 5, Part II and Part IV.
Every AFDS package has to satisfy the core; clause 4.3 states it without qualification.
So the definitions, the conformance rules, the whole component contract, and the whole serialisation format apply to every package that calls itself an AFDS package.

A **method profile** is something different in kind.
Clause 4.3 defines it as a named group of requirements carrying a specific way of building interfaces, and Part III defines the profiles themselves.
Two rules govern them, and both are prohibitions:

- a package is not to be judged against a method profile it does not claim; and
- a consumer is not to treat the absence of a method-profile claim as a defect (clause 4.3).

Read those twice if you have used a design system that shipped its layout opinions as a condition of entry.
They mean that declining a method profile is a legitimate position, not a partial adoption, and that a tool which flags an unclaimed profile as a shortfall is itself misbehaving.

Clause 4.3 gives the reason for the separation: the core describes how to carry an accessibility contract and its evidence, while a method profile describes one way of designing.
Those are different problems, and the specification declines to make the second a price of the first.

**The worked case.**
Consider an organisation whose brand palette is fixed, whose layout conventions are settled, and which has no appetite to change either.
Perhaps the palette came out of a brand programme that will not be reopened for three years; perhaps the layout conventions are baked into a framework the organisation does not control.

That organisation can satisfy the core completely.
Clause 4.3 spells out what it gets and what it does not:

> "That organisation gets the contract, the evidence, the uncertainty records, and the portability, and it does not get the layout method.
> That is the intended outcome, not a loophole."

So the position is this.
The organisation writes component specifications with their guarantees, non-guarantees and assertions; it records evidence against real assistive-technology combinations; it records what it does not know as uncertainty rather than leaving it to be assumed; it ships all of that in a package another tool can read.
It declares an empty set of method profiles.
It has not cut a corner, and no consumer is entitled to treat it as though it had.

The declinable things are the project's own design methods — the intrinsic layout method, the scoped reflow rule, the typography and colour scale, and the native-first pattern catalogue (clause 20.4).
The non-declinable thing is the honesty machinery: the contract, the evidence, the uncertainty, the serialisation.
If you take one sentence from this section, take that one.

Two supporting rules from Part III are worth knowing here, though the method profiles themselves belong to another section of this guide.
A profile is not a level: the profiles are unordered, do not build on one another, and a package claiming none "is not deficient" (clause 20.1).
And a package may adopt a profile's requirements without claiming the profile, which the specification expects to be common — but it may not then describe itself as claiming that profile (clause 20.3).

#### The three axes, and why they are separate

There are three separate statements a package makes about itself, and none of them may be derived from either of the others.

Clause 4.5 states the rule for two of them: completeness profiles (Part IV) state how much of a package hierarchy is present, method profiles (Part III) state which design method a package follows, these are independent axes, the specification requires them to be declared separately, and a consumer is not to infer either kind of profile from the other.
Clause 4.5 makes the independence concrete in both directions: a package containing only tokens may claim a method profile, and a package containing components, evidence and fixtures may claim none.

Clause 34 adds the third axis and states the rule across all three: the completeness field "states completeness only", it is a different axis from the method-profile array and from the WCAG target level, and "None of the three may be inferred from either of the others: a package may be `afds-full`, claim no method, and target Level A."

| Axis | What it states | Defined in | Declared in the manifest as |
| --- | --- | --- | --- |
| Completeness | How much of the package hierarchy is present | clause 34 | `conformanceProfile` — exactly one identifier |
| Method | Which of the specification's design methods the package follows | clauses 20, 4.5 | `methodProfiles` — an array, which may be empty |
| WCAG target level | The default WCAG level the package targets | clause 12.4 | `targetConformanceLevel` — one of `A`, `AA`, `AAA` |

The manifest field for completeness is named `conformanceProfile`, which is a historical name rather than a description.
Clause 29.1 says so directly: the field name is retained from the first release of the format, and "the value it carries is a completeness profile and nothing else".
This guide uses "completeness profile" for the concept throughout, and names the field only where the field is what you are writing.

Avoid the bare word "conformance" for any one of the three axes.
The specification reserves conformance for a property of a package and its claim (clause 4.4), and using it loosely is how the previous edition of this guide came to imply that a package with no method claim was somehow less conformant than one with three.

##### The completeness profiles themselves

Clause 34 defines three, and the identifiers are exactly these.

| Profile | Identifier | Requires |
| --- | --- | --- |
| Tokens only | `afds-tokens` | Root manifest and inventory, and at least one canonical token file declared in `tokens.canonicalSources` |
| Components | `afds-components` | Everything in `afds-tokens`, plus at least one component with both a component specification and component documentation |
| Full | `afds-full` | Everything in `afds-components`, plus canonical evidence records and a known-limitations artefact, and a declared test fixture for every component |

Three rules govern them (clause 34).

A package has to satisfy every requirement of the profile it declares.
A package may exceed its declared profile, so the specification requires a consumer to treat the declared profile as a floor rather than a description.
And a consumer that needs a higher profile than the package declares has to refuse to treat the package as sufficient — even if inspection suggests the extra artefacts are there — because an undeclared artefact carries no commitment to remain present in the next version.

That third rule is the one that surprises people, and it is the right rule.
Finding evidence records in a package that declares `afds-tokens` tells you what happened to be in this build, not what the producer has undertaken to keep shipping.

One provision of `afds-full` shows the project's attitude more clearly than anything else in Part IV.
The profile requires evidence records but does not require that they contain results, and a record whose result is `not-yet-tested` conforms (clause 34).
Clause 34 gives the reason: recording an untested combination is the mechanism by which uncertainty becomes visible, and a profile that demanded results would create pressure to invent them.

#### What a conformance claim consists of

A conformance claim has three required parts, and clause 4.4 names all three: the format version, the completeness profile, and the set of method profiles claimed, which may be empty.

| Part of the claim | What it says | Manifest field |
| --- | --- | --- |
| Format version | Which version of the package format the package is written to | `afdsVersion` (clause 29.1) |
| Completeness profile | How much of the hierarchy is present | `conformanceProfile` (clauses 34, 29.1) |
| Method profiles claimed | Which design methods the package claims; may be empty | `methodProfiles` (clauses 20.2, 29.1) |

An empty method-profile array is a complete claim, not an incomplete one.
Clause 20.2 treats an omitted array and an empty array as having identical meaning.

Clause 4.4 then sets two prohibitions, and both exist because claims of the forbidden kinds were being made in the wild.

**A claim cannot be a claim of conformance to something that has no conformance model.**
The specification forbids expressing a claim as conformance to an informative document, and forbids expressing it as conformance to a guide that has no conformance model.
It names the case: a package is not to claim that a component conforms to the ARIA Authoring Practices Guide, "because that guide is informative and has no conformance model to conform to" (clause 4.4).
This is not a slight on that guide.
It is a statement about what kind of thing it is.
An informative document explains how something is usually done; it does not define a testable set of obligations, so there is nothing there to conform to, and a claim of conformance to it would be unfalsifiable.

What you can publish about a component instead is stated in the same clause, and it is a short list of three:

- the accessibility criteria met;
- the semantics used; and
- the recorded assistive-technology results.

Each of those is checkable by someone who does not trust you, which is the point.
The relationship between the project and that guide, and the vocabulary for recording that a component was derived from a published pattern, is treated elsewhere in this guide under clauses 9.2 and 24.

**A claim about a package is not a claim about a service.**
Clause 4.4 states that a conformance claim is a claim about a package, not about a service built from it, and it puts the obligation on the producer: a producer is not to present a conformance claim as evidence that a service assembled from the package is accessible.

Note where that obligation sits.
It is not merely advice to a cautious consumer to avoid over-reading a claim.
It is a prohibition on the producer's marketing, procurement responses, and audit submissions.
A package can be `afds-full`, claim every method profile, carry evidence for every component, and be assembled into a service that fails a real user at the first form, because the assembly is where most accessibility failures live.
Clause 12.4 makes the parallel point about target levels: a declared level is a statement of intent and is not to be read as evidence that the level is met.

#### Version behaviour, and when a consumer must refuse

Two versions travel in every package and they move independently (clause 35).

`afdsVersion` is the version of the package format.
`packageVersion` is the version of the design-system payload.
Both use semantic versioning: major for incompatible change, minor for backwards-compatible addition, patch for a correction that changes no meaning (clause 35).

Separating them lets a consumer tell "the format changed" from "the design system changed", which are different problems for whoever has to react to them.

##### Format-version rules, if you produce packages

Clause 35.1 sorts changes to the format into three kinds.
The left column reproduces the specification's wording, so the capitalised keywords in it are quoted from clause 35.1.

| Change to the format | Kind of version change |
| --- | --- |
| Adds an *OPTIONAL* field, an *OPTIONAL* directory, or a new profile | Minor |
| Adds a *REQUIRED* field, removes a field, changes a field's type, or changes the meaning of an existing field | Major |
| Corrects prose without altering a requirement | Patch |

The line to remember is that adding a required field is a major change.
A consumer written against the earlier version would fail on a package it ought to have been able to read, so the format cannot pretend the addition was compatible.

##### Consumer behaviour on an unexpected format version

Clause 35.2 gives a table of six situations and the required behaviour in each.
This is the part a consumer most often gets wrong, and getting it wrong is dangerous precisely because it fails silently: a partial read of a package whose semantics you do not know produces plausible output and a misread accessibility contract.
The table is reproduced faithfully below; the capitalised keywords are the specification's own.

| Situation | Required consumer behaviour (clause 35.2) |
| --- | --- |
| `afdsVersion` major matches, minor is known | "Process normally." |
| `afdsVersion` major matches, minor is higher than the consumer knows | "The consumer *MUST* process the package, *MUST* ignore fields it does not recognise, and *SHOULD* report that it read a newer minor version." |
| `afdsVersion` major matches, minor is lower than the consumer knows | "The consumer *MUST* process the package and *MUST NOT* require a field introduced in a later minor version." |
| `afdsVersion` major is higher than the consumer supports | "The consumer *MUST* refuse to process the package and *MUST* report the unsupported version. It *MUST NOT* attempt a partial read." |
| `afdsVersion` major is lower than the consumer supports | "The consumer *MAY* refuse, or *MAY* process the package in a documented compatibility mode. It *MUST* state which it did." |
| `afdsVersion` is absent or unparseable | "The consumer *MUST* treat the package as non-conforming." |

Four things in that table are easy to implement wrongly.

An unknown minor version is not an error.
The consumer processes the package and drops the fields it does not recognise, rather than refusing.

An older minor version is not an error either, and the consumer may not demand a field that did not exist when the package was written.
A tool that requires a field introduced in a later minor version is rejecting conforming packages.

A higher major version is a refusal, and specifically a refusal without a partial read.
Reading "as much as you can" of a package written to a format you do not know is the failure mode this row exists to prevent.

A lower major version is a choice, but a declared one.
Refusing is permitted and a documented compatibility mode is permitted; what is not permitted is doing either quietly.

Clause 35.2 explains why the two major-version cases are treated differently.
A higher major may rely on semantics the consumer cannot know about, so guessing risks a silent misreading of an accessibility contract.
A lower major is fully knowable, so a compatibility mode is safe as long as it is declared.

These rules are not optional extras at the edge of a verifier.
Clause 31 places them inside the verification algorithm: reading `afdsVersion` and applying the clause 35 rules is a step of verifying a package, not a courtesy afterwards.

##### Payload-version rules, if you publish a design system

`packageVersion` changes when the design system changes (clause 35.3).

| Change to the payload | Kind of version change |
| --- | --- |
| Removing a component, removing a token, renaming an identifier, or narrowing a guarantee | Major |
| Adding a component, adding a token, or adding evidence | Minor |
| Correcting prose or a typographic error | Patch |

Clause 35.3 then settles the two cases that decide whether this scheme is honest.

Withdrawing an assistive-technology guarantee is a major payload change even when nothing else moves, because a consumer may have relied on it.
Someone downstream shipped a service on the strength of that guarantee, and the version number is the only signal they get.

Adding an evidence record that turns a recorded uncertainty into a guarantee is a minor change, because nothing that was relied upon has been taken away.

Those two rules together are the versioning scheme's whole ethic: taking a promise away is a breaking change, and learning something new is not.

#### Terms you need before going further

Clause 5 is normative, and it says how to read itself: where a term defined there is used in a normative clause, "it carries this meaning and no other".
It defines thirty-eight terms.
All thirty-eight are set out in the glossary at the end of this guide, in the specification's own words or a close paraphrase.

Two of them carry more weight than the rest and are worth having before you read any further.

**Accessibility Focused Design System (AFDS).**
"A design system whose accessibility contract, supporting evidence, and recorded uncertainty are first-class parts of the system rather than documentation about it."

The distinguishing move is not that the components are accessible.
It is that the contract, the evidence and the uncertainty are parts of the system — versioned, addressable, shipped — rather than prose written about the system afterwards and left behind when the system travels.

**AFDS package.**
A single file conforming to Part IV, containing a declared hierarchy of artefacts and the two required root artefacts (clause 5).

#### Where to go next

- The method profiles themselves, and what claiming one commits you to: clauses 20 to 24.
- What goes into a component contract, its guarantees, non-guarantees, assertions, evidence and uncertainty: Part II, clauses 7 to 19.
- The package hierarchy, the manifest and inventory fields, artefact roles, and the verification algorithm: Part IV, clauses 25 to 33.

## Part 4. The component contract

### What a component declares about itself

This section is the part of the guide a developer will keep open while working.
It covers Part II of the specification, clauses 7 to 19, which is the core of the format: the record every component carries, whatever design opinions its authors hold.

Part II is normative in full, and it applies to every component, layout primitive and pattern in a package, whatever method profile the package claims (Part II preamble; clause 4.3).
The method profiles of Part III are a separate axis and are covered later in this guide; where a rule below belongs to a profile rather than to the core, it is labelled as such and cross-referenced rather than restated.

One reminder about reading the specification itself.
The capitalised keywords in it carry the force set out in clause 4.1, and a lower-case "must" or "should" in an informative clause carries no requirement at all.
This guide is informative, so it does not issue requirements in its own voice.
Where it says that something is required, the clause named beside it is the requirement, and the specification is what a reviewer will hold you to.

The division Part II draws is worth stating once, because it is the one readers most often get wrong.
Recording which native element you considered and why it was insufficient is a **disclosure** obligation, and it sits in the core.
Preferring the native element is a **design rule**, and it sits in Part III, where it binds only a package that asks for it (Part II preamble; clause 8.3).
An organisation can therefore be held to complete disclosure without being held to this project's taste.

### Declaring a component

**Who this serves:** developers, and testers reading a component to work out what to test.

A component specification is the machine-readable record of what a component is, what it promises, what it refuses to promise, and how each of those statements can be checked (clause 7.1).

Three rules govern the artefact itself before any field is filled in.
Every component, layout primitive and pattern in a package has exactly one canonical specification; the specification is a JSON document; and where any other artefact in the package states the same fact, the specification governs and the other artefact is derivative (clause 7.1).

A fourth rule changes how you work: a specification cannot be generated from an implementation by inspection alone (clause 7.1).
A specification derived from code can only ever record what the code does, and the purpose of the document is to record what the component is *obliged* to do, so that the two can be compared and found to differ.
A generator that reads the DOM and writes the contract makes that comparison impossible by construction.

#### The seventeen required fields

The old guide gave ten fields and scoped them to derived components.
Both halves of that were wrong.
Clause 7.2 requires seventeen fields in **every** component specification, derived or not.

| Field | What it carries | Required | Clause |
| --- | --- | --- | --- |
| `afdsSpecVersion` | The version of the AFDS specification this document conforms to | Required | 7.3 |
| `id` | Stable, unique identifier for the component within the package | Required | 7.3 |
| `name` | The human-readable name | Required | 7.3 |
| `kind` | `layout-primitive`, `component`, or `pattern` | Required | 7.4 |
| `version` | The component's own version, under the Part IV payload rules | Required | 7.3 |
| `status` | `draft`, `proposed`, `stable`, `deprecated`, or `withdrawn` | Required | 7.4 |
| `summary` | What the component does, in prose, in no more than a short paragraph | Required | 7.3 |
| `semanticModel` | Role, native element, accessible-name source, rationale, reading order, consumer obligations | Required | 8 |
| `derivation` | The derivation status, and for a derived component the pattern fields | Required | 9 |
| `keyboardContract` | The eight stages, or an explicit declaration that there is no contract | Required | 10 |
| `reflowBehaviour` | The seven reflow disclosures, including any two-dimensional exception claim | Required | 11 |
| `wcagMapping` | One entry per success criterion the component bears on | Required | 12 |
| `guarantees` | The commitments the component makes, each naming its tests | Required | 14 |
| `nonGuarantees` | What the component explicitly does not commit to | Required | 14 |
| `assertions` | The testable statements, automated and manual, with procedures | Required | 15 |
| `uncertainty` | What is not known, with a status from the closed vocabulary | Required | 17 |
| `tests` | Fixture locations, isolated and realistic-page | Required | 18 |

Nothing in that list is optional.
A producer cannot omit a field on the grounds that it does not apply; where a field does not apply, the specification says so explicitly in the form the relevant clause defines (clause 7.2).

Clause 7.2 calls this the most important structural rule in Part II, and gives the reason plainly.
An omitted field and an inapplicable field look identical to a reader, and the reader will resolve the ambiguity in the direction that flatters the component.
So a component with no keyboard contract records that it has none, in words, so that a reviewer cannot mistake absence for oversight (clauses 7.2, 10.3).

Four fields carry extra obligations for a derived component, additional to the seventeen rather than a replacement for them, and they are covered under derivation below (clause 9.3).
Keep the counts apart: seventeen machine-readable fields in clause 7.2, four extra derivation fields in clause 9.3, twelve engineering review items in clause 24.4, and eleven design-handoff annotation fields in clause 19.1.
A count of one is never a count of another (clauses 19.1, 24.4).

#### Identifiers

`afdsSpecVersion` records the version of the specification the document conforms to (clause 7.3).

`id` is stable for the life of the component and unique within the package, and an `id` is never reused for a different component after the original is withdrawn (clause 7.3).
This is the field that makes withdrawal detectable.
If you recycle `dialog` for a different component two years later, every consumer holding evidence against the old `dialog` now holds evidence about something else, and nothing in the package says so.

`name` is for humans, and `summary` states what the component does and should also state what it does not do (clause 7.3).
`version` follows the payload versioning rules in Part IV, and is independent of both the package version and `afdsSpecVersion` (clause 7.3).

#### Kind and status

`kind` takes one of three values, and these are the same three layers the guide described earlier (clause 7.4).

| Value | Meaning |
| --- | --- |
| `layout-primitive` | A composable arrangement rule that positions content without knowing what it means |
| `component` | An interactive or structural element with declared semantics |
| `pattern` | Several components co-operating through a task |

`status` takes one of five values (clause 7.4).

| Value | Meaning |
| --- | --- |
| `draft` | Under development. Nothing in it can be relied on to remain stable. |
| `proposed` | Complete and awaiting review. Stable in shape, not yet in content. |
| `stable` | Reviewed, and subject to the Part IV versioning rules. |
| `deprecated` | Still present and still supported, with a replacement named. |
| `withdrawn` | No longer supported. Present so that consumers can detect the withdrawal. |

A `deprecated` or `withdrawn` specification states the reason and, where one exists, the replacement `id` (clause 7.4).
That is why withdrawn components stay in the package instead of disappearing from it: a component that vanishes teaches a consumer nothing, while one marked `withdrawn` with a reason and a successor tells them what to do next.

#### Component documentation

Every component specification should have component documentation: a human-readable counterpart carrying the reasoning the JSON cannot express (clause 7.5).
The counterpart does not contradict the specification, and where the two disagree the specification governs and the disagreement is a defect in the package rather than a matter for interpretation (clause 7.5).

Component documentation exists because a component specification records decisions without recording why they were taken, and a decision whose reasoning is lost cannot be safely revisited (clause 7.5).

### The semantic model

**Who this serves:** developers and designers together.
This is the field where a design decision becomes a machine-readable claim.

The commonest accessibility question about any component is the least glamorous one: what is this thing called, what state is it in, and what is it related to.
Most failures of an otherwise correct component are failures of that answer, or of the markup around it that was supposed to supply it.

The `semanticModel` object records six things (clause 8.1).

| Key | What it records |
| --- | --- |
| `role` | The ARIA role the component exposes, or `none` where it exposes no role |
| `implicitElement` | The native element the component renders as its own outermost element |
| `accessibleName` | The source of the accessible name, or `none` where the component has no accessible name of its own |
| `rationale` | Prose explaining why the semantics are what they are |
| `domOrderIsReadingOrder` | A boolean stating whether the component preserves document order as reading order |
| `consumerObligations` | An array of statements, drafted under clause 8.2 |

A component that exposes no role records `none` rather than omitting the field, and its `rationale` says why no role is correct (clause 8.1).
The reasoning is worth carrying in your head: a component with no semantics is making a claim, not declining to make one (clause 8.1).
A layout primitive that carries geometry and no ARIA is the ordinary case here, and its rationale is that the primitive cannot know whether its children form a list, so it does not guess (clauses 8.1, 8.3, 14.4).

#### Consumer obligations

A consumer obligation is a statement of something the consumer has to do for the component to be used correctly (clause 8.2).

Three drafting rules apply.
Every obligation is written as a requirement on the consumer rather than as a description of the component; every obligation uses the conformance language of clause 4.1; and an obligation is never used to discharge a responsibility the component could reasonably meet itself (clause 8.2).
That last rule has a blunt gloss in the specification: writing an obligation is not a way of exporting difficulty (clause 8.2).

The mechanism exists because most accessibility failures involving a correct component are failures of the surrounding markup (clause 8.2).
A primitive that arranges children cannot know whether those children form a list; the consumer who does know is the only party able to supply the semantics, and recording that as an obligation moves it from folklore into the contract.

#### The native baseline

The `semanticModel` also records the native baseline: the behaviour and semantics the component would have if built from platform-native elements without added roles or scripted behaviour (clause 8.3).

Where the component is not built on that baseline, the specification states which native element was considered and why it was insufficient (clause 8.3).
An answer of the form that no native element was considered is a valid answer, and is recorded as such rather than left blank (clause 8.3).

Read the strength of that clause carefully.
Clause 8.3 requires disclosure and does not require a preference (clause 8.3).
A package that always answers this field by saying a native element was rejected for visual reasons conforms to the core, provided it says so — and its reviewers now have something to argue with, which is the point (clause 8.3).
The *preference* for native elements is clause 24.3, and it binds only a package claiming the `afds-patterns-native-first` profile.

### Native HTML first, and deriving from published patterns

**Who this serves:** developers deciding what to build, and reviewers deciding whether the decision was made or merely arrived at.

#### Adopted policy, not a proposal

Native HTML first is this project's adopted position, and the treatment of external pattern guidance is settled.
It is recorded as a colophon decision, marked settled in the open-questions register, and carried normatively as clause 24, the native-first pattern profile, identifier `afds-patterns-native-first`.
The project claims that profile in the packages it publishes.
Anything you may have read describing it as proposed or not yet adopted is out of date.

Clause 24.1 states the position in five clauses, and each does work.

> WCAG establishes the required outcome.
> Native HTML is preferred.
> ARIA fills genuine semantic gaps.
> A published pattern guide supplies the interaction model for recognised custom patterns.
> The package specifies, tests, versions, and evidences the implementation actually shipped.

Each clause does work.
The first fixes the acceptance criteria in a normative standard, so a disagreement about behaviour resolves against an outcome rather than a preference.
The second sets the default engineering answer, because native elements arrive with focus behaviour, activation semantics, disabled-state handling and forced-colours treatment already implemented and already tested by browser vendors.
The third confines ARIA to the repair role it was designed for.
The fourth admits that some interactions have no native equivalent, and that a custom one should behave the way users already expect.
The fifth locates responsibility, because no external document can carry evidence about the code a package actually ships (clause 24.1).
The statement is this project's own formulation and is not attributable to the W3C or to any working group (clause 24.8).

In a package claiming the profile, the preference becomes a rule: a component is not given a `pattern-derived` status where a native element in the clause 24.3 table would have supplied the semantics and interaction, unless the component specification records why the native element was insufficient (clause 24.3).
The table is ordered from cheapest to most expensive, and the order is part of the advice.

| Product need | Preferred response | Why |
| --- | --- | --- |
| Action | Native `<button>` | Activation, focus, disabled state and keyboard behaviour are already provided |
| Choice between options | Native radio or checkbox inputs | Avoids recreating form semantics |
| Navigation | Links inside a navigation landmark | Do not convert site navigation into a menu widget |
| Reveal supplementary content | Native `<details>`, or a button with controlled content | Often avoids a full custom disclosure implementation |
| Modal confirmation | A dialog component following the published dialog model | A genuine composite interaction with focus-management needs |
| Rich autocomplete | A combobox, only where native controls cannot satisfy the task | High complexity; semantics and keyboard contract must be complete |
| Large interactive results table | A native table first; an ARIA grid only where directional cell navigation is genuinely needed | A visual CSS grid is not a semantic grid and does not justify the clause 22 exception |

The rule is deliberately phrased as a restriction rather than as an endorsement, because the likeliest failure mode for a system that admires a pattern guide is to turn every familiar interaction into a custom widget (clause 24.3).

One correction to a common list of mistakes.
Converting site navigation into a menubar is **not** a misuse of the menu and menubar pattern, and the specification says it must not be described as one (clause 24.5).
The published pattern is not restricted to application menus, and its publisher ships a navigation menubar example demonstrating site navigation (clauses 24.5, 24.8).
What clause 24.5 records is a convention of this profile with a stated cost: adopting a menubar for ordinary navigation imports the whole composite contract — a roving-focus model, a single tab stop, author-managed arrow-key movement, submenu behaviour, and a role that causes a screen reader to describe the thing as a menu rather than as navigation.
A package claiming the profile may adopt a menubar anyway, and if it does, the justification appears in the component's specification tagged as a `product-deviation` under clause 13, with the keyboard contract written out in full (clause 24.5).

#### The five derivation statuses

Every component in a package carries exactly one derivation status, and the set of those records is the pattern registry (clause 9.1).
This is a core requirement on every package, not a proposal and not a profile matter.

The `derivation.status` field takes one of five values (clause 9.2).

| Value | Meaning |
| --- | --- |
| `native-first` | A native element fully supplies the interaction |
| `pattern-derived` | A custom component implements a recognised published pattern |
| `pattern-adjacent` | A similar interaction that intentionally differs from the published pattern |
| `custom` | No mature published pattern applies |
| `prohibited` | The pattern creates more accessibility cost than value and is not to be used |

Use those spellings.
Earlier drafts of this project named two of them after the ARIA Authoring Practices Guide specifically — `APG-derived` and `APG-adjacent` — and they were deliberately renamed so that the core vocabulary of clause 9 does not presuppose one pattern guide (clause 24.8).
Anything still using the old names is stale, and a package using them does not carry a valid `derivation.status` at all (clause 9.2).
Throughout the core, the neutral term is "published pattern guide"; the guide this project uses is the APG, and clause 24.8 records that adoption in the profile where it belongs.

The statuses are not a quality ranking: a component is not defective for being `pattern-derived`, and a package whose components are mostly `native-first` is not thereby better.
What the registry records is that the status was decided and reasoned, rather than arrived at (clause 9.2).

Two statuses carry extra obligations.
A `pattern-adjacent` entry names the pattern it resembles and states exactly where and why it departs, so that a component is not labelled with a pattern name it does not honour (clause 9.2).
A `prohibited` entry states the cost that motivated the prohibition, and is revisitable if the underlying support picture changes; a prohibition without a stated cost is an opinion that cannot be reviewed (clause 9.2).

#### What a derived component records in addition

Where `derivation.status` is `pattern-derived` or `pattern-adjacent`, four further things are recorded (clause 9.3).

| # | What is recorded | Notes |
| --- | --- | --- |
| 1 | The pattern name and its source URL | The URL, and not the name alone |
| 2 | The native alternative considered, and why it was insufficient | An insufficiency finding, not an open question |
| 3 | Every deviation from the published pattern, each with its reason **and its cost**, each tagged under clause 13 | Reason alone is not enough |
| 4 | Whether the pattern is support-dependent, and if so the reassessment trigger required by clause 9.5 | See below |

A derived component with no deviations records that explicitly.
Silence about deviations is never to be read as an absence of them (clause 9.3).

The tag on a deviation comes from the clause 13 vocabulary below; in practice most deviations are `product-deviation` or `support-limitation`, and a `product-deviation` carries its cost as well as its reason (clauses 9.3, 13).

#### Support-dependent patterns, and the reassessment trigger

A pattern is support-dependent where its declared behaviour is known to depend on assistive-technology or engine support that is incomplete (clause 9.5).

A support-dependent component records a reassessment trigger stating the condition under which its specification is reopened (clause 9.5).
The trigger is required because a change in support is the main reason a settled contract silently becomes wrong, and without a trigger the change is noticed by accident, usually by a user (clause 9.5).

A usable trigger names a condition, not an intention: "reopen when the recorded `partial` result for JAWS with Chrome becomes `supported` on two consecutive JAWS releases" is a trigger; "revisit periodically" is not.

#### The pattern registry, core and profile

There are two things called a registry and they belong to different axes.

The **core** registry is the set of per-component `derivation.status` records, and every package carries it because every component carries a status; without it, whether a component follows a recognised interaction model is a property of whoever wrote it first, discoverable only by reading the implementation (clause 9.1).

The **package-level registry artefact** is a profile requirement.
A package claiming `afds-patterns-native-first` carries a registry listing every component and pattern in the package against its status; the registry does not disagree with any component's own declaration, and where they differ the component specification governs and the package is defective (clause 24.2).
That profile registry also records a `prohibited` entry for a pattern the package has declined, even though no component implements it (clause 24.2).

That last requirement is the reason the artefact is worth having, and it is the one thing per-component declarations cannot supply, because a decision not to build something leaves no component behind to declare it.
Without a package-level registry, the absence of a menubar component looks identical to nobody having considered a menubar, and the argument gets held again in the next review (clause 24.2).

#### What a derivation may not claim

This is the hard limit, and it is core, binding every package.

A specification does not state or imply that a component conforms to an informative document, and in particular a package does not claim that a component conforms to the ARIA Authoring Practices Guide, "because that guide is informative and has no conformance model to conform to" (clauses 4.4, 9.4).

The reasoning is a distinction beginners are rarely told.
WCAG 2.2 and WAI-ARIA are normative standards with conformance models; the APG is informative guidance.
A component can follow every keystroke recommendation in a published pattern and still fail WCAG, and a component can depart from a pattern's key map and still conform to WCAG.
There is nothing in an informative document for a claim to be measured against, so the sentence "this component conforms to the APG" is not a weak claim, it is not a claim at all.

What you can publish instead is fixed: the accessibility criteria met, the semantics used, and the recorded assistive-technology results (clauses 4.4, 9.4).

Two further prohibitions follow.
Recording that a component is derived from a published pattern is a statement about where the interaction model came from; it is not a conformance claim, it carries no assurance, and a consumer does not treat it as evidence of anything (clause 9.4).
If you are the developer consuming somebody else's package, that is aimed at you: `pattern-derived` tells you nothing about whether the component works.
And a specification does not cite a published pattern's own example implementations as evidence for the component, because such examples are written to demonstrate a pattern legibly, which is a different goal from being production code, and no external example can carry evidence about the code a package actually ships (clause 9.4).

### The keyboard contract

**Who this serves:** developers writing the contract, testers executing it, designers who need to know what they have implicitly specified.

The keyboard contract is the load-bearing part of a component specification, and its name understates it (clause 10.1).

#### "Keyboard" does not mean a keyboard

A keyboard interface is an input pathway rather than a physical device (clause 10.1).

Get the attribution right, because a reviewer who gets it wrong loses the argument.
WCAG 2.2 defines a keyboard interface **narrowly**, as an interface used by software to obtain keystroke input.
The breadth comes from what drives that interface, and it is the *Understanding* document for Success Criterion 2.1.1 that lists speech input software, sip-and-puff software, on-screen keyboards, scanning software, and a variety of assistive technologies and alternate keyboards among keyboard emulators (clause 10.1).
A reviewer who cites the definition for the emulator list is citing the wrong document (clause 10.1).

The definition also carries an exclusion: operation through a keyboard-operated mouse emulator does not qualify, because the program is being driven through its pointing-device interface instead, and a component exercised only that way is not recorded as having been tested for keyboard operation (clause 10.1).

The consequence is the point of the whole clause.
A component's keyboard contract is simultaneously its switch-access contract, its scanning contract, and much of its speech-input contract (clause 10.1).
Testing with a physical keyboard is necessary, and the specification is explicit that it is not to be treated as sufficient (clause 10.1).

#### The eight stages

Where a component has a keyboard contract, the contract declares all eight of the following (clause 10.2).
The conditional matters: it is what makes clause 10.3 coherent for components that have no contract.

| Stage | What it declares |
| --- | --- |
| 1. Entry | What receives focus when the user moves into the component, and what happens on re-entry after leaving |
| 2. Internal movement | Which keys move focus inside the component, whether movement wraps, and whether roving `tabindex` or `aria-activedescendant` is used |
| 3. Activation | Which keys act on the focused item, distinguishing keys that change selection from keys that commit an action |
| 4. Exit | Whether Tab leaves, whether Escape dismisses, and where focus goes in each case |
| 5. State change | What is conveyed after expansion, selection, validation failure, loading or deletion, and by what mechanism |
| 6. Restoration | Where focus returns when a popup or dialog closes, including when the invoking control no longer exists |
| 7. Pointer and touch parity | Whether all functionality is reachable without hover, without drag, and without a path-dependent pointer movement |
| 8. Speech-recognition operation | Whether every visible interactive control has a stable visible label, and whether visible text is contained in the accessible name |

Three rules attach to particular stages.
Stage 3 distinguishes selection from commitment, because conflating them is what produces accidental destructive operations (clause 10.2).
Stage 6 names a documented logical successor for the case where the invoker no longer exists, which is common wherever an action deletes the row containing its own trigger (clause 10.2).
And an exit path that depends on the user guessing is not recorded as satisfying stage 4, so "the user can press Escape" is a satisfactory answer only if Escape is discoverable (clause 10.2).

Note that stage 5 asks what is **conveyed** and by what mechanism, not what a screen reader announces.
Announcement is one mechanism; a visible status region, a validation message tied by `aria-describedby`, or a change of accessible name are others.

#### The keys a contract has to answer for

The specification fixes the stages, not a key map.
Key bindings are conventions, tagged `recommended-by-convention` under clause 13 unless a standard requires them, and a component may depart from them if it labels the departure and states its cost (clause 13).
The table below is the set of bindings a contract normally has to say something about.

| Key | Stage | What the contract has to state |
| --- | --- | --- |
| Tab | 1, 4 | Whether it enters, whether it leaves, and where focus lands in each direction |
| Shift+Tab | 1, 4 | The same, backwards, including re-entry after leaving |
| Arrow keys (Up, Down, Left, Right) | 2 | Whether they move focus inside the component, on which axis, and whether movement wraps |
| Home, End | 2 | Whether they jump to the first and last item |
| Page Up, Page Down | 2 | Whether they move by group, where the component has groups |
| Type-ahead characters | 2 | Whether printable characters move focus, and how a single-character binding avoids colliding with speech-recognition and screen-reader command sets |
| Space | 3 | Whether it changes selection or commits, which is the distinction stage 3 requires |
| Enter | 3 | Whether it commits, and what it commits |
| Escape | 4 | Whether it dismisses, and where focus goes when it does |
| Modifier combinations | 2, 3 | Any custom shortcut, and whether it can be turned off or remapped |

Where roving `tabindex` or `aria-activedescendant` is used, stage 2 requires the contract to say which (clause 10.2).
The two produce different focus behaviour under assistive technology, and a contract that says only "arrow keys move focus" has not answered the stage.

#### Declaring the absence of a contract

A layout primitive that arranges boxes has no keyboard contract, and that is a normal, conforming state.
Where a component has no keyboard contract, `keyboardContract.hasKeyboardContract` is `false` and the object carries a statement saying so explicitly (clause 10.3).

The statement is positive rather than empty, because a reviewer reading an empty keyboard contract cannot tell whether the component has none or whether nobody filled it in, and those are opposite findings (clause 10.3).
"This primitive exposes no interactive controls of its own and receives no focus; keyboard behaviour belongs to the content the consumer places inside it" is a positive statement; an empty object is not.

#### The focus lifecycle

Separately from the eight stages, the contract records four booleans — whether the component receives focus, moves focus, traps focus and restores focus — together with a note explaining the combination (clause 10.4).

These four are recorded separately because they are the properties a consumer needs in order to reason about composition, and the example the specification gives is the one you will meet: a page containing two components that both trap focus has a defect that neither component's own tests can detect (clause 10.4).
That is also why the booleans are worth writing even when they feel obvious from the prose — the prose is not queryable, and the composition question is asked by a tool assembling a page, not by a reader.

#### Related WCAG checks, which are not contract stages

Four checks are worth carrying out and are not part of clause 10; they are WCAG criteria in their own right, and this guide states them as commentary rather than as contract requirements.
Avoid fine pointer paths, which exclude switch and scanning users and often fail Pointer Gestures.
Avoid hover-only discovery, which is unreachable to keyboard-interface users and unstable for magnifier users.
Avoid drag-only movement, because reordering needs a single-pointer and keyboard-interface alternative, which is the substance of Dragging Movements.
Avoid custom single-character shortcuts that cannot be turned off or remapped, because they collide with speech-recognition and screen-reader command sets.
Where these bear on a component, they are recorded in the `wcagMapping` array under clause 12, which is where a criterion belongs.

### Reflow and layout behaviour

**Who this serves:** developers and designers; the tester inherits the claim and has to check its boundary.

#### What a component records about reflow

The `reflowBehaviour` object records seven things (clause 11.1).

| # | What is recorded |
| --- | --- |
| 1 | Whether the component is intrinsic, meaning that it responds to available space rather than to a chosen breakpoint |
| 2 | Whether it uses layout media queries |
| 3 | What author-fixed dimensions it declares, or `none` |
| 4 | Whether it declares fixed heights |
| 5 | The mechanism, in prose, by which it reflows |
| 6 | Whether it operates without JavaScript |
| 7 | Whether it claims the two-dimensional exception, and the rationale for that claim |

Clause 11.1 is in the core rather than in a method profile because the declaration is a disclosure, not a design rule: a package whose components all use media queries and fixed heights conforms to the core, provided it says so (clause 11.1).
If you want the design rules — intrinsic layout, the primitive set, the prohibition on absolute media queries — those are the layout method profile, clause 21, and they bind only a package claiming it.

#### The criterion

WCAG 2.2 Success Criterion 1.4.10 requires content to be presentable without loss of information or functionality and without two-dimensional scrolling, at a width equivalent to 320 CSS pixels for vertically scrolling content and a height equivalent to 256 CSS pixels for horizontally scrolling content.
A width of 320 CSS pixels corresponds to a 1280 CSS pixel starting viewport at 400 per cent zoom.
The criterion excepts parts of the content that require two-dimensional layout "for usage or meaning", and its cited examples include data tables, qualified as "not individual cells" (clause 22.2).

#### The two-dimensional exception

Where a component claims the exception, the specification gives a rationale resting on semantic two-dimensional structure (clause 11.2).
This is core and binds every package.

The rationale does not rest on visual appearance, and does not rest on the layout technique used to produce the appearance; a region that merely looks like a grid does not qualify (clause 11.2).
Where a component does *not* claim the exception, the specification should still record why, because the components most likely to be misused as a basis for the claim are the ones that never had a basis for it (clause 11.2).

And one prohibition worth quoting at a design review: adopting a widget role in order to unlock the exception is not recorded as a rationale, because doing so abuses both the role and the criterion, and a consumer encountering such a rationale should treat the package as defective (clause 11.2).
That is a consumer-side instruction as well as a producer-side one: if you are reviewing somebody else's package and find `role="grid"` justified by a wish to avoid reflowing content, you have found a defect, not a design choice.

The test resolves as follows.
A region qualifies when a cell's significance depends on its relationship to both a row axis and a column axis, so that flattening the structure would destroy meaning rather than merely rearrange appearance (clause 22.2).
Stated as a slogan, which is how it is easiest to remember: cells are semantic content, and grid is a layout technique.
A CSS Grid container has no table semantics; declaring `display: grid`, or wrapping items with a content-driven measurement, creates no row header, no column header and no header-to-cell relationship, so visual grid arrangement is not offered as a basis for the exception (clause 22.2).

#### A decision table

Most disputes are resolved by finding the closest row.
This table records how the core test of clause 11.2 resolves in common cases; clause 22.2 is where the specification sets it out, and it adds no requirement of its own.

| Content | Basis | Excepted |
| --- | --- | --- |
| Results table with genuine row and column header relationships | A cell's significance depends on both axes | Yes, as a scoped region |
| Programme guide organised by channel and time | Channel and time are both meaning-bearing axes | Yes, as a scoped region |
| Collection of self-contained cards | Arrangement is presentational | No |
| Dashboard laid out in grid areas | Arrangement is presentational | No |
| Filter panel beside a results list | Adjacency is convenience, not meaning | No |

Two readings of that table are wrong and worth naming.
The programme-guide row establishes that a meaning-bearing two-dimensional structure need not be a conventional data table, and is not to be read as extending the exception to visual grids generally (clause 22.2).

And the exception is scoped.
It covers the table as a **scoped region**, not individual cells, and it does not spread to the page around it.
The phrase "not individual cells" in the criterion marks where the semantic two-dimensional relationship stops: the relationship holds between a cell and its two axes, so the excepted thing is the structure that carries the axes, and a single cell has no claim of its own.
Scoping is what stops the exception being a licence for a horizontally scrolling page.

Two things follow that belong to Part III rather than here.
Making the rationale specific — naming both meaning-bearing axes, explaining how a cell's significance depends on each, stating the semantic structure that carries the relationship, and stating the boundary of the excepted region — is the scoped reflow profile, `afds-reflow-scoped`, clause 22.3, and so are the profile's rules about surrounding content, truncation and techniques, clauses 22.4 to 22.6.
Section D of this guide covers them as a declarable profile.
Do not present them as universal rules: a package that claims no profile is bound by clauses 11.1 and 11.2 and by nothing in clause 22 (clause 4.3).

### Recording WCAG criteria against a component

**Who this serves:** testers and developers; this is the field an auditor will read first.

The `wcagMapping` array contains one entry for every success criterion the component bears on (clause 12.1).

Each entry records six things (clause 12.1).

| Field | What it records |
| --- | --- |
| Criterion number | For example 2.1.1 |
| Criterion name | For example Keyboard |
| Assigned level | The level at which WCAG 2.2 assigns the criterion |
| `branch` | One of the two values in clause 12.2 |
| `relationship` | One of the two values in clause 12.3 |
| Note | Prose saying what the component does about the criterion |

Keep two kinds of "level" apart.
The assigned level is a property of the criterion and is fixed by WCAG; it is not the target level of clause 12.4, which is a property of the package or the component and is chosen by the author (clause 12.1).

#### The two branches

Every entry records a `branch` of either `user technology support` or `user layout support` (clause 12.2).

| Branch | Covers |
| --- | --- |
| `user technology support` | Assistive-technology compatibility: roles, accessible names, states, focus, keyboard operation |
| `user layout support` | Reflow, measure, spacing, contrast, reading order |

The split is diagnostic (clause 12.2).
A flat list of criteria per component hides whether a failure is geometric or semantic, and those two failures have different owners, different tests and different fixes.
Classification follows what carries meaning rather than the mechanism that produced the appearance, and the clearest case is the two-dimensional exception, which looks like a layout matter and is decided by semantics (clause 12.2).

#### The relationship vocabulary

Each entry records a `relationship` of either `supports` or `does-not-address` (clause 12.3).

| Value | Meaning |
| --- | --- |
| `supports` | The component contributes to meeting the criterion |
| `does-not-address` | The component bears on the criterion and does nothing about it, so the consumer owns it |

The vocabulary is closed, and extending it is a change to the specification rather than something done inside a package (clause 12.3).

A `does-not-address` entry is not an admission of failure and is not to be treated as one (clause 12.3).
Recording that a layout primitive conveys no relationships, and that the consumer therefore owns Info and Relationships, is more useful than silence, because silence leaves the consumer to discover the ownership in an audit (clause 12.3).

#### The target level is declared, not mandated

The specification does not fix a target WCAG conformance level and is not to be read as requiring one (clause 12.4).
A package declares a default target level; a component may amend it, and a component that amends it records the amended level and the reason (clause 12.4).
A method profile may set a default for packages claiming it, and where a package claims such a profile that default governs the package, because a profile is claimed whole (clauses 12.4, 20.3).

The effective level for a component resolves in one order, first available declaration governing: the component's own declaration; the default set by a claimed method profile; the package default (clause 12.4).

Three inferences are forbidden.
An effective level is not inferred from anything other than those three declarations; it is not inferred from a completeness profile, which states completeness and says nothing about level; and it is not inferred from the presence of evidence recorded at a higher threshold, because measuring a ratio is not the same act as committing to it (clause 12.4).

And the declaration is not evidence.
A declared target level is a statement of intent and is not read as evidence that the level is met (clause 12.4).
Whether a criterion is met at the declared level is an assertion under clause 15, substantiated under clause 16.

Amending a level downward is permitted and is recorded rather than concealed (clause 12.4).
A component targeting Level AA inside a package that defaults to Level AAA is a disclosure, and the disclosure is worth more than a package-wide claim a reviewer would have to disprove component by component (clause 12.4).
A level is declared per component and not per criterion; a package needing to hold one criterion to a different threshold does so as an assertion under clause 15, not as a second target level (clause 12.4).

### Kinds of requirement

**Who this serves:** everyone in a review argument.

Every requirement in a component specification is tagged with exactly one of five kinds (clause 13).

| Value | What it means | Consequence if not met |
| --- | --- | --- |
| `required-by-standard` | A normative requirement from a W3C standard | A conformance failure |
| `recommended-by-convention` | An interoperable convention users are likely to expect | A usability and discoverability risk, not a conformance failure |
| `project-convention` | A choice the system has made for internal consistency | An inconsistency to be reconciled or documented |
| `product-deviation` | A deliberate, recorded departure for a product reason | Nothing, provided the record and its reasoning exist |
| `support-limitation` | A gap in browser or assistive-technology behaviour | Uncertainty to be disclosed, not a claim to be made |

Use those spellings.
The second value in particular is `recommended-by-convention`, not "strongly recommended by APG": the core vocabulary does not name one external pattern library, and clause 24.8 records the renaming as deliberate.

Tagging prevents two opposite failures (clause 13).
The first is presenting every convention as conformance law.
A component may satisfy WCAG with a keyboard model that departs from a widely used convention, provided it is fully operable and its state is correctly conveyed, and a document that denies this loses its authority the moment somebody checks (clause 13).
The second is dismissing conventions as merely optional, which is how components end up technically conformant and practically unusable by people who already know how the interaction is supposed to work (clause 13).

The correct handling of a departure is to allow it, label it, and state its cost (clause 13).
That last part is a requirement, not a nicety: a `product-deviation` records its cost as well as its reason (clause 13).
The same tag vocabulary is what clause 9.3 means when it requires each deviation from a published pattern to be tagged (clause 9.3).

### Guarantees, and what a component refuses to promise

**Who this serves:** developers writing the contract, and any developer consuming somebody else's.

#### Guarantees

A guarantee is a declared commitment about the component's behaviour or properties (clause 14.1).

The `guarantees` array contains one entry per commitment, and each entry records five things (clause 14.1).

| Field | What it records |
| --- | --- |
| `id` | Unique within the specification |
| `statement` | The commitment, written so that it can be tested |
| `branch` | Under clause 12.2 |
| `requirementKind` | Under clause 13 |
| `assertions` | An array of assertion identifiers |

A guarantee is a design commitment: it is what the component is obliged to do, and it outlives any particular test run, which is why it is authored rather than computed (clause 14.1).

#### A guarantee has to name its test

Every guarantee names at least one assertion that tests it, and a guarantee whose `assertions` array is empty is invalid — a package containing one does not conform (clause 14.2).

This is the rule that stops a guarantee from being a wish (clause 14.2).
A commitment that nobody can state a procedure for is not a commitment about the product, it is a sentiment about it, and the specification says the distinction is the reason the format exists (clause 14.2).

It is also the rule the old guide's worked Dialog broke seven times over: it listed seven guarantees, none of which named an assertion, which made the guide's own example a non-conforming specification.
The rewritten example later in this section fixes that.

The rule cannot be discharged by writing an assertion that restates the guarantee without giving a procedure (clause 14.2).
Clause 15.1 requires a procedure for exactly this reason.
Note what the rule does *not* require: naming an assertion is not the same as having run it, and a brand-new component with complete guarantees and no evidence is in a perfectly describable state — see substantiation below.

#### Substantiation is computed, not written

Every guarantee has a substantiation status, and the status is not authored (clause 14.3).
It is computed from the evidence records that reference the guarantee's assertions, and a producer that writes it into the specification is stating something it is not entitled to state (clause 14.3).

There are four statuses, not three.

| Status | Computed when |
| --- | --- |
| `substantiated` | Every named assertion has at least one evidence record with result `supported`, and none with `partial` or `unsupported` |
| `partially-substantiated` | At least one named assertion has a result of `supported`, and at least one has `partial` or has no record at all |
| `unsubstantiated` | No named assertion has any evidence record other than `not-yet-tested` |
| `contradicted` | Any named assertion has an evidence record with result `unsupported` |

`partially-substantiated` is the one most often missing from summaries of this format, and it is the status most real components are in.

The separation of the promise from the measurement is the point of the design (clause 14.3).
A new component with no testing has made commitments and has substantiated none of them, and both halves of that sentence are true and useful.
Collapsing them would either let a package promise what it has not earned, or force it to promise nothing until testing exists, and neither describes the real state of any design system (clause 14.3).

Two consequences.
A consumer does not present a guarantee as met without also presenting its substantiation status (clause 14.3) — if you are building a documentation site or a component browser over an AFDS package, that is a requirement on your tooling, not on the package.
And a `contradicted` guarantee is a defect in the package rather than a property of the component: the producer either fixes the component, narrows the guarantee, or withdraws it, and Part IV states what each of those does to the version (clause 14.3).

One caution, from the companion document rather than from the specification.
Guarantees do not union across an assembly boundary.
A child's guarantee propagates into a parent composition only if its preconditions still hold after assembly, the parent has not overridden the relevant semantics or behaviour, no sibling conflicts with it, the author obligations it depends on have been met, and the evidence covers the resulting configuration; otherwise it is suspended and has to be re-established by evidence at the parent level.
That analysis is set out in *Component Design Frameworks and the Assembly Problem* (`research/COMPONENT-FRAMEWORKS.md`, §5.2).
Read a guarantee as conditional, not as a label permanently attached to a component name.

#### What a component refuses to promise

A non-guarantee is an explicit statement of something the component does not commit to (clause 14.4).

The `nonGuarantees` array is present and is not empty (clause 14.4).
A component that commits to everything has not understood the question (clause 14.4).
There is no such thing as a conforming component specification with an empty non-guarantees list, so a review that finds one has found a defect and not a tidy component.

A non-guarantee is specific enough to change what a consumer does (clause 14.4).
The specification gives the contrast worked out.
"The component does not guarantee accessibility" is not a non-guarantee, because no consumer can act on it.
"The component provides no grouping role and no accessible name, so the consumer must supply both" is a non-guarantee, because it tells the consumer what to build (clause 14.4).

#### Why the list is mandatory at all

This is the mechanism behind clause 2.5, and it is the part of the format that most changes how documentation reads.

A component that lists only its promises invites the reader to assume the rest, and the assumption is where accessibility is lost (clause 14.5).
The reader is not being careless when they do this.
A list of guarantees reads as a description of the component, and a description is naturally taken to be complete (clause 14.5).

Requiring the opposite list forces the boundary of the contract to be drawn explicitly, by the party that knows where it lies (clause 14.5).
Honesty about limits is not a hedge here; it is the load-bearing structure.

### Assertions

**Who this serves:** testers above all.

An assertion is a statement about the component whose truth can be evaluated against an implementation (clause 15.1).

Each entry in the `assertions` array records four things (clause 15.1).

| Field | What it records |
| --- | --- |
| `id` | Unique within the specification |
| `type` | Either `automated` or `manual` |
| `statement` | What is asserted |
| `procedure` | How to evaluate it |

The `procedure` field is specific enough that two testers following it independently would agree on the result (clause 15.1).
A procedure that restates the statement in the imperative does not satisfy that, and is not used to discharge clause 14.2 (clause 15.1).
"Check that focus is trapped" is a restatement.
"Load the isolated fixture, open the dialog from the trigger button, press Tab eleven times, and record the accessible name of the focused element after each press" is a procedure.

#### Automated and manual

Both are assertions.
There is no separate category of "manual checks" sitting outside the array; `manual` is an assertion `type` (clauses 15.1, 15.2).

An assertion of type `automated` is evaluable without human judgement (clause 15.2).

An assertion of type `manual` records what the tester observes rather than what they conclude (clause 15.2).
The distinction matters because a manual assertion phrased as a conclusion invites the tester to supply the answer the specification expects (clause 15.2).
"The dialog is correctly announced" is a conclusion.
"On opening, the screen reader speaks the dialog's accessible name followed by its role" is an observation.

A `manual` assertion produces a result that expires, and clause 16.4 governs that (clause 15.2).

#### What an assertion is not

An assertion is not a statement about intent, about the design process, or about a standard (clause 15.3).

That a component was built following a pattern is not an assertion, because no procedure evaluates it against the running implementation (clause 15.3).
That a component meets a success criterion is not an assertion either, because meeting a criterion is a conclusion drawn from observations rather than an observation.
The assertion is the observation (clause 15.3).

This is the rule that keeps the `wcagMapping` array and the `assertions` array doing different jobs.
The mapping records which criteria the component bears on; the assertions record what somebody can go and look at.

### Evidence records

**Who this serves:** testers and QA engineers.

#### What evidence attaches to

Evidence attaches to a combination, not to a component (clause 16.1).

A combination is the tuple of assistive technology, browser, engine, operating system, and their versions (clause 16.1).
A result observed in one combination says nothing about another, and a package that records a single undifferentiated result is making a claim it has not tested (clause 16.1).
The specification calls this the third of its five gaps, and the one that most often survives into otherwise careful documentation (clause 16.1).

#### The fourteen required fields

The old guide described five fields.
Clause 16.2 requires fourteen.

| # | Field | Content |
| --- | --- | --- |
| 1 | `id` | Unique within the package |
| 2 | `componentId` | The component the record concerns |
| 3 | `assertionRef` | The assertion or assertions this record evaluates |
| 4 | `claim` | The behaviour that was looked for |
| 5 | `engine`, `engineVersion` | The rendering engine and its version |
| 6 | `browser`, `browserVersion` | The browser and its version |
| 7 | `at`, `atVersion` | The assistive technology and its version, or `none` |
| 8 | `platform`, `device` | The operating system and the class of device |
| 9 | `startingViewport`, `zoom` | The layout conditions, or `not-applicable` |
| 10 | `date` | The date of observation |
| 11 | `result` | A value from clause 16.3 |
| 12 | `observation` | What was actually observed |
| 13 | `tester` | Who made the observation |
| 14 | `uncertaintyRef` | The uncertainty record this result bears on, where one exists |

Two rules make the record usable.

`assertionRef` is what allows clause 14.3 to compute a substantiation status, and a record that evaluates nothing nameable cannot contribute to a guarantee, so a producer does not record one (clause 16.2).
An evidence record with no assertion reference is not weak evidence; it is not evidence.

`observation` records what happened rather than whether it was correct (clause 16.2).
The result field carries the judgement, and keeping the two apart is what makes a record re-readable when the expectation later changes (clause 16.2).

#### The result vocabulary

`result` takes one of five values (clause 16.3).

| Value | Meaning |
| --- | --- |
| `not-yet-tested` | No observation has been made. The claim it would support is uncertainty, not a guarantee. |
| `supported` | The expected behaviour was observed on the stated versions on the stated date. |
| `partial` | The behaviour was observed but differs materially from the expectation. The difference is described. |
| `unsupported` | The expected behaviour was not observed. |
| `not-applicable` | The combination cannot exhibit the behaviour. |

`not-yet-tested` is the value to use for a planned combination nobody has run yet.
An empty cell, a dash, or the words "to be recorded" are not values in this vocabulary, and a package using them has not recorded a result at all.

The value `not-applicable` carries a second sense outside the `result` field: in any other field it means the field does not apply to that record, such as a zoom level on a record about announcement, or an assistive-technology version on a record whose `at` is `none`.
A package uses it in only those two senses (clause 16.3).

#### Results expire

An evidence record is an observation on a date, and is not treated as a permanent property of the component (clause 16.4).

A consumer should treat a record as stale when the stated versions are no longer current, and does not present a stale record as a current result without saying so (clause 16.4).
That is a requirement on tooling that displays evidence, not only on the package.

This is why the fourth testing level is recorded with a date rather than a tick (clause 16.4).
Assistive-technology behaviour changes with releases the package cannot observe, and a format that stores the result without the date stores a claim that quietly becomes false.

### Uncertainty records

**Who this serves:** everyone; this is the field that most distinguishes an AFDS package from ordinary accessibility documentation.

An uncertainty record states that something is not known (clause 17.1).

Each entry in the `uncertainty` array records five things (clause 17.1).

| Field | What it records |
| --- | --- |
| `id` | Unique within the specification |
| `subject` | What the uncertainty is about |
| `statement` | What specifically is not known |
| `status` | From clause 17.2 |
| `evidenceRef` | The evidence records that bear on it, where any exist |

#### The status vocabulary

`status` takes one of four values (clause 17.2).

| Value | Meaning |
| --- | --- |
| `not-yet-tested` | No observation has been attempted |
| `results-conflict` | Observations disagree across combinations, and the disagreement is not yet explained |
| `no-known-method` | No procedure is known that would settle the question |
| `awaiting-support` | The question cannot be settled until support changes in a browser or assistive technology |

The four are not interchangeable, and choosing between them is a genuine judgement.
`not-yet-tested` says somebody has to go and look.
`results-conflict` says somebody has looked twice and got two answers, which is a different task: explain the divergence.
`no-known-method` is the honest label for a claim nobody knows how to check, and it is the one that most often gets silently downgraded to `not-yet-tested`.
`awaiting-support` says the answer will change when a vendor ships something, and it is the status that pairs with a reassessment trigger.

#### Reassessment triggers and support-dependence

Where a component declares that its pattern is support-dependent under clause 9.3, it records a reassessment trigger stating the condition under which its specification is reopened (clauses 9.3, 9.5).
In practice the trigger and the uncertainty record are two halves of one disclosure: the uncertainty record, usually with status `awaiting-support` or `not-yet-tested`, says what is not known, and the trigger says what would have to happen for the contract to be reopened.

Write the trigger as a condition somebody could notice.
Name the combination, the behaviour, and the change that would matter.
A trigger that names no condition is not a trigger, and a support-dependent component without one is incomplete under clause 9.5.

#### Uncertainty is a record, not a failure

An uncertainty record has the same standing as a record stating a result, and a consumer does not treat its presence as a defect (clause 17.3).

A package with no uncertainty records is either exhaustively tested across every combination or is concealing something, and the specification observes that the first is not achievable (clause 17.3).

The rule that does most of the work in the whole format is here.
An assistive-technology claim without a test record is recorded as uncertainty rather than as a guarantee (clause 17.3).
The reasoning is worth reading twice: the ordinary way accessibility documentation becomes false is not by lying, it is by stating a reasonable expectation in the same voice as a measured result, and this rule makes the two grammatically distinct (clause 17.3).

### Testing levels, and testing in composition

**Who this serves:** testers and QA engineers, and developers deciding what to automate.

#### The five levels

A package should verify each component at five levels, and each level catches a class of defect the others miss, so they are not treated as substitutes for one another (clause 18.1).

| Level | What is tested |
| --- | --- |
| 1. Static semantics | Element choice, role validity, accessible name, state, relationships |
| 2. Keyboard contract | Entry, internal movement, activation, exit, restoration |
| 3. Visual and layout | Focus visibility, forced colours, 400 per cent zoom, text spacing, reflow |
| 4. Assistive technology | Actual behaviour by combination, version, and date |
| 5. Composition | Behaviour among landmarks, headings, and realistic content |

Levels 1 to 3 are largely scriptable and should run on every change.
Level 4 is manual, slow, and produces results that expire, which is why clause 16 records it with a date.
Level 5 is the level most often skipped, and it is where component-level correctness turns into page-level failure (clause 18.1).

Level 4 is recorded by **combination**, version and date — combination being the tuple clause 16.1 defines, not a browser name alone.

#### Component conformance and composition conformance are different claims

Conformance is measured at two levels: the component in isolation, and the component inside a realistic page (clause 18.2).

A package does not claim composition conformance on the strength of isolated testing (clause 18.2).
That is the prohibition to remember, and it is the one an audit will test you against.
A green test suite over isolated fixtures is evidence about isolated fixtures.

The two levels find different defects, and the composition defects are the ones a component cannot detect about itself (clause 18.2).
The specification gives three examples.
Two components that each correctly manage focus can produce a page in which focus is managed twice.
A component that correctly contributes a landmark can produce a page with duplicate landmarks.
A dialog that passes every isolated test can open beneath page chrome its own fixture does not contain (clause 18.2).

Beyond that, the analysis of *why* assembly breaks — the assembly hierarchy from token to process, the eight compositional failure modes, worked composite breakdowns, state propagation and its ownership rules, and testing across multi-page flows — is carried in *Component Design Frameworks and the Assembly Problem* (`research/COMPONENT-FRAMEWORKS.md`).
That document is published ahead of this material, and this guide does not restate it.
Two of its findings bear directly on how you read Part II.
Guarantees do not union across an assembly boundary (§5.2), which is why the guarantee section above treats a guarantee as conditional.
And component-level green is not evidence for the page (§7.4), which is the practical form of the clause 18.2 prohibition.
Where that document and the specification differ in emphasis, the specification governs and the companion carries the detail.

#### Fixtures

The `tests` object records the location of an isolated fixture and of a realistic-page fixture (clause 18.3).

Where a package does not ship a fixture, the `tests` object records where it belongs and states that it is absent, and a consumer treats the fixture as absent rather than as unlocatable (clause 18.3).

The reasoning generalises the clause 7.2 rule.
A recorded path to a fixture that does not exist is a statement about the package's completeness, and a package that quietly omits the field makes the same statement without disclosing it (clause 18.3).

### Annotating a design

**Who this serves:** designers, and the developer receiving a handoff.

A visual mock-up cannot show what a component promises, which keys operate it, where focus goes when a dialog closes, or what happens at high zoom.
In a system, those live in the component's specification, and the mock-up is annotated to say which component was chosen and what product-specific decisions apply.

Where a package supports a design-tool handoff, it should provide an annotation preset exposing the information a visual mock-up cannot convey, and the preset should carry eleven fields (clause 19.1).
Note the strength: this is a conditional expectation, not a requirement on every package.

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

"If any" in the first row is doing work: a `native-first` component implements no pattern, and the honest annotation says so.

These eleven are written for design handoff.
They are not the fields required by clause 9.3, which are written for engineering review, and a count of one is never a count of the other (clause 19.1).
Nor are they the twelve review items of clause 24.4, a third list with a third audience.

The relationship model is the field most often lost and the one that most repays recording, because it is invisible in a mock-up and expensive to reverse-engineer afterwards (clause 19.1).
A designer who has decided that a control expands a panel has already decided that an expansion relationship applies, and writing it down costs less than discovering it in an audit (clause 19.1).

#### The annotation economy rule

An annotation should not restate behaviour the coded component already guarantees (clause 19.2).

The annotation identifies the selected component and any product-level choices or deviations.
Restating guaranteed behaviour makes annotations long, makes them drift from the code, and trains reviewers to skim them, which defeats the annotations that carry something the code does not (clause 19.2).

So the rule in working form: do not annotate what the visual design, the component API or the coded component already guarantees.
The project takes this from GitHub's published design-system annotation practice — Jan Maarten, *Design system annotations, part 1: How accessibility gets left out of components* and *part 2: Advanced methods of annotating components*, The GitHub Blog, at <https://github.blog/engineering/user-experience/design-system-annotations-part-1-how-accessibility-gets-left-out-of-components/> and <https://github.blog/engineering/user-experience/design-system-annotations-part-2-advanced-methods-of-annotating-components/>.
Clause 19.2 states the rule unattributed; the attribution is recorded here because the practice is somebody else's.

### A worked component: Dialog

**Who this serves:** all three readers.
This is the section to copy from.

A modal dialog is the right example because it is genuinely composite, has no complete native equivalent in the shape most products need, and depends on behaviour that varies across assistive technologies.
It is also where the previous version of this guide went wrong, in six ways: an invalid `derivation.status`, seven guarantees naming no assertions, a four-key table standing in for the eight mandatory stages, no semantic model, no reassessment trigger despite declared support-dependence, and evidence cells reading "to be recorded" instead of `not-yet-tested`.
What follows is written to conform.

The specification below is complete against clause 7.2: all seventeen fields are present, and none is omitted on the grounds that it does not apply.
Field values are illustrative; the structure is not.

```json
{
  "afdsSpecVersion": "1.0",
  "id": "dialog",
  "name": "Dialog",
  "kind": "component",
  "version": "1.2.0",
  "status": "proposed",
  "summary": "A modal dialog that interrupts the current task to obtain a decision or show content that must be dealt with before continuing. It manages its own focus while open and restores focus when it closes. It does not supply page-level scroll locking, does not make its own destructive actions reversible, and does not guarantee identical announcement across assistive technologies.",
  "semanticModel": {
    "role": "dialog",
    "implicitElement": "div",
    "accessibleName": "aria-labelledby, referencing the required heading element inside the dialog",
    "rationale": "The dialog role with aria-modal is used because the component must convey to assistive technology that content outside it is unavailable while it is open. The native baseline considered was the HTML dialog element with showModal, which supplies the role, the top layer, inertness of the rest of the document, and Escape-to-close. It was judged insufficient for this package because the product requires a dialog that can be rendered inside a constrained stacking context supplied by the host application shell, which the top layer does not permit, and because the package must record dated evidence for announcement behaviour that varies independently of the element used. The role is therefore authored rather than inherited, and the behaviours the native element would have supplied are declared as guarantees with assertions.",
    "domOrderIsReadingOrder": true,
    "consumerObligations": [
      "The consumer MUST supply a heading element as the first child of the dialog's content region, and MUST NOT remove it, because the accessible name is derived from it.",
      "The consumer MUST render the dialog as a child of the application shell's dialog host element, and MUST NOT render it inside a transformed or clipped ancestor.",
      "The consumer MUST provide a visible control that dismisses the dialog, in addition to Escape.",
      "The consumer MUST NOT open a second dialog while this one is open; nesting is excluded by this component's composition rules.",
      "Where the control that opened the dialog may be removed while the dialog is open, the consumer MUST name the logical successor element required by the keyboard contract's restoration stage."
    ]
  },
  "derivation": {
    "status": "pattern-derived",
    "patternName": "Dialog (Modal)",
    "patternSourceUrl": "https://www.w3.org/WAI/ARIA/apg/patterns/",
    "nativeAlternativeConsidered": "HTML dialog element with showModal()",
    "nativeAlternativeInsufficientBecause": "showModal() promotes the element to the top layer, which the host application shell's constrained stacking context does not permit. The product requires the dialog to be clipped by its host region in one embedded deployment. This is an insufficiency finding, not an open question.",
    "deviations": [
      {
        "id": "dev-1",
        "from": "The published pattern's expectation that the dialog is the only modal surface and that content outside it is inert",
        "deviation": "Inertness is applied to a named application-shell subtree rather than to the whole document.",
        "reason": "The embedded deployment renders the host application inside a third-party frame that the package does not control.",
        "cost": "Content outside the named subtree remains reachable by an assistive technology's virtual cursor in that deployment, so a screen-reader user can read content the sighted user cannot reach. This is disclosed as non-guarantee ng-2 and as uncertainty unc-2.",
        "requirementKind": "product-deviation"
      }
    ],
    "supportDependent": true,
    "reassessmentTrigger": "Reopen this specification when either of the following occurs: the recorded result for assertion a-4 (dialog role and name conveyed on opening) changes from `partial` to `supported` for JAWS with Chrome across two consecutive JAWS releases; or any tested combination's aria-modal handling changes such that content outside the inert subtree stops being reachable by the virtual cursor. The owner named in the package manifest re-runs the level 4 fixtures on each major release of any assistive technology in the recorded matrix."
  },
  "keyboardContract": {
    "hasKeyboardContract": true,
    "stages": {
      "entry": "On opening, focus moves to the first interactive control in the dialog's content region, or to the dialog's own container where the content region contains no interactive control. On re-entry after the dialog has been closed and reopened, the same rule applies; the dialog holds no memory of previous focus position.",
      "internalMovement": "Tab and Shift+Tab cycle through the dialog's interactive controls in document order, wrapping at both ends. Arrow keys are not bound by the dialog and are passed to the focused control. Neither roving tabindex nor aria-activedescendant is used; focus is real DOM focus on each control.",
      "activation": "Enter commits the action of the focused control and nothing else. Space activates the focused button and toggles the focused checkbox. No key changes selection at the dialog level, so selection and commitment do not overlap: the dialog itself has no selectable items, and any selection behaviour belongs to a control the consumer places inside it.",
      "exit": "Tab does not leave the dialog; movement wraps within it while the dialog is open. Escape dismisses the dialog, and dismissal is equivalent to activating the visible cancel control. On Escape, focus returns to the restoration target defined below. The visible cancel control is required by consumer obligation 3 so that the exit path does not depend on the user guessing Escape.",
      "stateChange": "Opening is conveyed by focus moving into the dialog and by the dialog's role and accessible name being exposed at the newly focused element's context; no live region is used for opening. Validation failure inside the dialog is conveyed by the failing control's aria-describedby reference to its error message and by aria-invalid on that control. A loading state in the dialog's content region is conveyed by aria-busy on the content region. Deletion of the dialog's content is not a state this component conveys, and is disclosed as non-guarantee ng-3.",
      "restoration": "On close, focus returns to the element that opened the dialog. Where that element no longer exists, focus returns to the documented logical successor: the nearest preceding interactive sibling of the removed invoker within the same list or toolbar, or, where none exists, the container that held the invoker, which the consumer makes focusable for this purpose. The successor is named in the consumer obligation set and is not left to the user agent.",
      "pointerAndTouchParity": "All functionality is reachable without hover, without drag, and without path-dependent pointer movement. The dialog exposes no hover-only affordance. Dismissal is available by pointer on the visible cancel control, by Escape, and by pointer on the backdrop where the consumer enables that option.",
      "speechRecognitionOperation": "Every visible interactive control in the dialog carries a stable visible label, and each control's accessible name contains its visible text. The cancel control's visible label is Cancel and its accessible name is Cancel. The dialog's own accessible name is the visible heading text."
    },
    "focusLifecycle": {
      "receivesFocus": true,
      "movesFocus": true,
      "trapsFocus": true,
      "restoresFocus": true,
      "note": "This component traps focus for the whole time it is open, and restores focus on close. Two focus-trapping components on one page produce a defect neither component's own tests can detect, so this component's composition rules exclude a nested dialog and exclude any other trapping component inside its content region. A consumer assembling a page checks this combination before composing."
    }
  },
  "reflowBehaviour": {
    "isIntrinsic": true,
    "usesLayoutMediaQueries": false,
    "authorFixedDimensions": "none",
    "declaresFixedHeights": false,
    "mechanism": "The dialog's content region is a single-column flow whose width is bounded by a maximum measure expressed in rem and by the available width of its host, whichever is smaller. At narrow widths the dialog occupies the full host width less its gutter, and its content region scrolls vertically. Nothing in the dialog is positioned by breakpoint.",
    "operatesWithoutJavaScript": false,
    "claimsTwoDimensionalException": false,
    "twoDimensionalExceptionRationale": "The exception is not claimed. The dialog's content has no meaning-bearing second axis: its children are a heading, a flow content region, and an action group, none of whose significance depends on a relationship to both a row axis and a column axis. Where a consumer places a data table inside the dialog, the exception belongs to that table as a scoped region and not to the dialog, and the claim is made in the table's own specification."
  },
  "wcagMapping": [
    {
      "criterion": "1.3.1",
      "name": "Info and Relationships",
      "assignedLevel": "A",
      "branch": "user technology support",
      "relationship": "supports",
      "note": "The dialog exposes the dialog role and derives its accessible name from the required heading, so the interruption is conveyed programmatically."
    },
    {
      "criterion": "1.4.10",
      "name": "Reflow",
      "assignedLevel": "AA",
      "branch": "user layout support",
      "relationship": "supports",
      "note": "The dialog is intrinsic and declares no author-fixed dimensions or fixed heights; it does not claim the two-dimensional exception."
    },
    {
      "criterion": "2.1.1",
      "name": "Keyboard",
      "assignedLevel": "A",
      "branch": "user technology support",
      "relationship": "supports",
      "note": "All eight keyboard-contract stages are declared, and no functionality requires a pointer."
    },
    {
      "criterion": "2.1.2",
      "name": "No Keyboard Trap",
      "assignedLevel": "A",
      "branch": "user technology support",
      "relationship": "supports",
      "note": "Focus is confined while the dialog is open, and Escape plus the required visible cancel control provide a documented exit."
    },
    {
      "criterion": "2.4.7",
      "name": "Focus Visible",
      "assignedLevel": "AA",
      "branch": "user layout support",
      "relationship": "does-not-address",
      "note": "The dialog supplies no focus indicator for the controls a consumer places inside it. The consumer owns focus visibility for those controls."
    },
    {
      "criterion": "4.1.2",
      "name": "Name, Role, Value",
      "assignedLevel": "A",
      "branch": "user technology support",
      "relationship": "supports",
      "note": "Role, name and modal state are exposed; the announcement of the combination is uncertain across combinations and is recorded as unc-1."
    }
  ],
  "guarantees": [
    {
      "id": "g-1",
      "statement": "While open, the dialog exposes role dialog and an accessible name derived from the heading element in its content region.",
      "branch": "user technology support",
      "requirementKind": "required-by-standard",
      "assertions": [
        "a-1",
        "a-4"
      ]
    },
    {
      "id": "g-2",
      "statement": "While open, Tab and Shift+Tab move focus only among the dialog's own interactive controls, wrapping at both ends.",
      "branch": "user technology support",
      "requirementKind": "required-by-standard",
      "assertions": [
        "a-2"
      ]
    },
    {
      "id": "g-3",
      "statement": "Escape closes the dialog, and closing by Escape has the same effect as activating the visible cancel control.",
      "branch": "user technology support",
      "requirementKind": "recommended-by-convention",
      "assertions": [
        "a-3"
      ]
    },
    {
      "id": "g-4",
      "statement": "On close, focus returns to the invoking element, or to the documented logical successor where the invoker no longer exists.",
      "branch": "user technology support",
      "requirementKind": "required-by-standard",
      "assertions": [
        "a-5",
        "a-6"
      ]
    },
    {
      "id": "g-5",
      "statement": "At a 1280 CSS pixel starting viewport at 400 per cent zoom, the dialog presents its content without two-dimensional scrolling and without loss of information or functionality.",
      "branch": "user layout support",
      "requirementKind": "required-by-standard",
      "assertions": [
        "a-7"
      ]
    },
    {
      "id": "g-6",
      "statement": "Every visible interactive control the dialog supplies has an accessible name containing its visible label text.",
      "branch": "user technology support",
      "requirementKind": "required-by-standard",
      "assertions": [
        "a-8"
      ]
    }
  ],
  "nonGuarantees": [
    {
      "id": "ng-1",
      "statement": "The dialog does not prevent the document behind it from scrolling. The consumer must apply scroll locking to the application shell, or accept that background scrolling remains available."
    },
    {
      "id": "ng-2",
      "statement": "In the embedded deployment described in deviation dev-1, the dialog does not make content outside the named application-shell subtree unreachable. A screen-reader user can read content outside the dialog with a virtual cursor. The consumer must not use the embedded deployment where that is unacceptable."
    },
    {
      "id": "ng-3",
      "statement": "The dialog does not convey the deletion or replacement of its own content region while open, and supplies no live region for it. A consumer whose dialog content changes in place must supply the announcement."
    },
    {
      "id": "ng-4",
      "statement": "The dialog does not make destructive actions reversible and supplies no confirmation step of its own. A consumer placing a destructive action in the dialog must supply the confirmation or the undo."
    },
    {
      "id": "ng-5",
      "statement": "The dialog does not guarantee that every browser and assistive-technology combination conveys its role and name in the same words or in the same order. See uncertainty unc-1."
    }
  ],
  "assertions": [
    {
      "id": "a-1",
      "type": "automated",
      "statement": "The dialog's outermost element has role dialog, has aria-modal set to true, and has an aria-labelledby reference resolving to a non-empty accessible name.",
      "procedure": "Load fixtures/dialog/isolated.html. Activate the element with id trigger. Query the element with id dialog. Read its role, aria-modal attribute, and computed accessible name from the accessibility tree exposed by the test driver. Record role, the aria-modal value, and the accessible name string."
    },
    {
      "id": "a-2",
      "type": "automated",
      "statement": "With the dialog open, pressing Tab from the last interactive control moves focus to the first interactive control, and Shift+Tab from the first moves focus to the last.",
      "procedure": "Load fixtures/dialog/isolated.html and open the dialog. Enumerate the interactive controls inside the element with id dialog in document order and record the count n. Press Tab n times from the initially focused control, recording the id of the focused element after each press. Then focus the first control and press Shift+Tab once, recording the id of the focused element. Record the two sequences."
    },
    {
      "id": "a-3",
      "type": "automated",
      "statement": "With the dialog open, pressing Escape removes the dialog from the accessibility tree and fires the same close event as activating the control with id cancel.",
      "procedure": "Load fixtures/dialog/isolated.html and open the dialog. Attach a listener recording close events and their detail. Press Escape. Record the event and whether the element with id dialog is present in the accessibility tree. Reload, open the dialog, activate the control with id cancel, and record the same two observations. Record both event details verbatim."
    },
    {
      "id": "a-4",
      "type": "manual",
      "statement": "On opening the dialog, the assistive technology speaks the dialog's accessible name and conveys that it is a dialog.",
      "procedure": "Load fixtures/dialog/isolated.html in the combination under test with the assistive technology running and speech viewer or braille output captured. With focus on the element with id trigger, activate it with Enter. Transcribe, verbatim, everything spoken or output between activation and the end of speech. Do not interpret; record the words in the order they were produced. Two testers compare transcripts for the presence of the heading text and of a word conveying the dialog role."
    },
    {
      "id": "a-5",
      "type": "automated",
      "statement": "On close, focus is on the element that opened the dialog, where that element is still in the document.",
      "procedure": "Load fixtures/dialog/isolated.html. Record the id of the element with focus, activate it to open the dialog, then press Escape. Record the id of the element with focus after close. Repeat, closing by activating the control with id cancel."
    },
    {
      "id": "a-6",
      "type": "automated",
      "statement": "On close, where the invoking element has been removed from the document while the dialog was open, focus is on the documented logical successor.",
      "procedure": "Load fixtures/dialog/invoker-removed.html, which contains a list of rows each with a delete button. Activate the delete button in the third row to open the dialog. From within the dialog, activate the control with id confirm, which removes the third row and closes the dialog. Record the id of the element with focus after close, and record whether it is the delete button of the second row, which is the documented successor."
    },
    {
      "id": "a-7",
      "type": "manual",
      "statement": "At a 1280 by 1024 CSS pixel starting viewport at 400 per cent zoom, all of the dialog's content and controls can be reached by vertical scrolling alone.",
      "procedure": "Set the browser window to a 1280 by 1024 CSS pixel viewport. Load fixtures/dialog/realistic-page.html and set zoom to 400 per cent. Open the dialog. Attempt to reach each control listed in the fixture's manifest using vertical scrolling only, without horizontal scrolling. Record, for each control, whether it was reached and whether any horizontal scrollbar appeared on the dialog or on the document. Record any text that was clipped or truncated without a means of revealing it."
    },
    {
      "id": "a-8",
      "type": "automated",
      "statement": "Each interactive control the dialog supplies has a computed accessible name that contains its visible label text as a substring.",
      "procedure": "Load fixtures/dialog/isolated.html and open the dialog. For each interactive control inside the element with id dialog, read its visible text content and its computed accessible name from the accessibility tree. Record both strings for each control, and record whether the visible text is a substring of the accessible name after collapsing whitespace."
    }
  ],
  "uncertainty": [
    {
      "id": "unc-1",
      "subject": "Announcement of the dialog role and accessible name on opening, across the recorded combinations",
      "statement": "It is not known whether all four combinations in the package's recorded matrix convey both the dialog role and the accessible name on opening. Observation exists for one combination and is outstanding for three.",
      "status": "not-yet-tested",
      "evidenceRef": [
        "ev-a4-nvda-firefox-win"
      ]
    },
    {
      "id": "unc-2",
      "subject": "Reachability of content outside the inert subtree in the embedded deployment",
      "statement": "It is not known whether any tested combination prevents virtual-cursor access to content outside the named application-shell subtree when aria-modal is set but the document root is not inert. The behaviour is a property of the assistive technology and cannot be settled by this package alone.",
      "status": "awaiting-support",
      "evidenceRef": []
    },
    {
      "id": "unc-3",
      "subject": "Announcement of validation failure inside the dialog on mobile screen readers",
      "statement": "Observations disagree: on one combination the error message referenced by aria-describedby was output on focus, and on another it was not, and the difference is not yet explained.",
      "status": "results-conflict",
      "evidenceRef": [
        "ev-a4-talkback-chrome-android",
        "ev-a4-voiceover-safari-ios"
      ]
    }
  ],
  "tests": {
    "isolatedFixture": "fixtures/dialog/isolated.html",
    "realisticPageFixture": "fixtures/dialog/realistic-page.html",
    "additionalFixtures": [
      {
        "path": "fixtures/dialog/invoker-removed.html",
        "present": true,
        "purpose": "Exercises assertion a-6, the removed-invoker restoration case."
      },
      {
        "path": "fixtures/dialog/embedded-shell.html",
        "present": false,
        "absenceStatement": "This fixture is absent. It belongs at the recorded path and would exercise the embedded deployment described in deviation dev-1. A consumer treats it as absent rather than as unlocatable."
      }
    ]
  }
}
```

#### One evidence record in full

Evidence lives in the package's evidence records rather than in the component specification, and each record carries all fourteen clause 16.2 fields.
Here is one, complete.

```json
{
  "id": "ev-a4-nvda-firefox-win",
  "componentId": "dialog",
  "assertionRef": [
    "a-4"
  ],
  "claim": "On opening the dialog, the assistive technology speaks the dialog's accessible name and conveys that it is a dialog.",
  "engine": "Gecko",
  "engineVersion": "142.0",
  "browser": "Firefox",
  "browserVersion": "142.0",
  "at": "NVDA",
  "atVersion": "2026.2",
  "platform": "Windows 11 26H1",
  "device": "desktop",
  "startingViewport": "1280x1024",
  "zoom": "100%",
  "date": "2026-08-27",
  "result": "partial",
  "observation": "On activating the trigger, speech output was: \"Delete this report, dialog. Cancel, button.\" The accessible name and the word dialog were both output. The aria-modal state was not conveyed in words, and the heading was spoken before the role rather than after it.",
  "tester": "A. Rahman",
  "uncertaintyRef": "unc-1"
}
```

The remaining three combinations in the recorded matrix have records of their own with `result` set to `not-yet-tested` and `observation` recording that no observation has been made.
They are not blank cells and they do not say "to be recorded"; `not-yet-tested` is the value the vocabulary supplies for exactly this state (clause 16.3).

#### What that example does to the guarantees

No substantiation status appears anywhere in the specification above, because the status is computed and a producer that writes it in is stating something it is not entitled to state (clause 14.3).

Computing it from the evidence above: guarantee g-1 names assertions a-1 and a-4, and a-4 has a record with result `partial`, so g-1 computes to `partially-substantiated` rather than `substantiated` (clause 14.3).
That is the honest state of a real component two weeks into testing, and the format has a word for it.

#### Checks run against this example

The example was checked field by field against the clauses that govern it.

| Clause | Check | Result |
| --- | --- | --- |
| 7.2 | All seventeen required fields present, none omitted as inapplicable | Present; `reflowBehaviour.claimsTwoDimensionalException` is `false` with a recorded reason rather than absent |
| 7.3, 7.4 | Identity fields present; `kind` and `status` from the fixed vocabularies | `component`, `proposed` |
| 8.1, 8.2, 8.3 | Six semantic-model keys; obligations written as consumer requirements in clause 4.1 language; native baseline recorded with an insufficiency finding | Present |
| 9.2, 9.3, 9.5 | `derivation.status` is a valid value; pattern name and source URL, native alternative and insufficiency, deviations with reason, cost and clause 13 tag, support-dependence and a reassessment trigger | `pattern-derived`; one deviation with cost, tagged `product-deviation`; trigger names a condition |
| 10.2, 10.3, 10.4 | All eight stages declared; stage 3 distinguishes selection from commitment; stage 4 gives focus destinations and does not depend on guessing; stage 6 names a logical successor; four focus-lifecycle booleans with a note | Present |
| 11.1, 11.2 | Seven reflow items; a recorded reason for not claiming the exception | Present |
| 12.1, 12.2, 12.3 | One entry per criterion, each with number, name, assigned level, `branch`, `relationship` and note | Six entries, one `does-not-address` |
| 13 | Every requirement tagged with exactly one kind; `product-deviation` carries its cost | Present |
| 14.1, 14.2, 14.4 | Five fields per guarantee; every guarantee names at least one assertion; non-guarantees present, non-empty and specific | Six guarantees, all with assertions; five non-guarantees |
| 15.1, 15.2, 15.3 | Four fields per assertion; procedures reproducible by two testers; manual assertions record observation rather than conclusion; no assertion about intent, process or a standard | Eight assertions, five automated and three manual |
| 16.2, 16.3 | Fourteen evidence fields; `result` from the closed vocabulary; `observation` records what happened | One full record shown, `result` `partial` |
| 17.1, 17.2 | Five uncertainty fields; `status` from the four values | Three records, using `not-yet-tested`, `awaiting-support` and `results-conflict` |
| 18.3 | Isolated and realistic-page fixture locations recorded; an absent fixture recorded as absent at its path | Present |

## Part 5. The method profiles

### The method profiles: choosing a way of building, or not

Everything you have read so far applies to every AFDS package; this section does not.

Part III of the specification describes four ways of building interfaces, each packaged as a *method profile*: a named group of requirements that a package may claim, and against which it can then be measured.
A package that claims none of them still conforms.
Clause 4.3 puts it without hedging: an organisation whose brand palette and layout conventions are already fixed "can satisfy the core completely", gets the contract, the evidence, the uncertainty records and the portability, and does not get the layout method — and "That is the intended outcome, not a loophole."
The material below is the most opinionated writing in the specification, and it is also the most optional.

An earlier edition of this guide presented the layout method as *the* project method and described five of its rules as "non-negotiable".
That was wrong structurally rather than in detail: it left a reader with a fixed breakpoint system believing they had already failed, when in fact they had declined a profile, which is a permitted act requiring no explanation.

#### What a method profile is

A method profile is a named, versioned set of requirements about how components are built, which a package may claim and against which it can then be measured (clause 20.1).

A profile is not a level, and this is the point most often misread: the four profiles are not ordered, do not build on one another, and carry no ranking (clause 20.1).
A package claiming three profiles is not more conformant than a package claiming one, and a package claiming none is not deficient.
There is no "highest" profile to aim at, because the profiles are about different subjects, not different degrees of the same subject.

Three rules keep a profile from drifting into the core, and between them they tell you exactly which of your obligations survive if you drop a profile claim (clause 20.1).

A profile does not restate a core requirement: where a profile appears to require something Part II already requires, Part II governs and the profile's restatement has no independent force, so removing a profile claim takes nothing away that Part II required of you.

A profile does not weaken a core requirement, and the specification is blunt about the consequence: a profile that purported to excuse a package from a Part II obligation "would not be a profile, and a package claiming it does not conform".

A profile imposes at least one requirement that the core does not, because without that rule a profile could restate nothing, weaken nothing and require nothing, which would make it a label rather than a commitment — "the kind of unearned claim this specification exists to prevent".
Where the intended content of a profile turns out to be entirely a matter of citing existing work, the specification says the right action is to cite that work directly and define no profile.

Three readers, three consequences.
For a **designer**, a profile is a set of design decisions somebody has already argued out; you can take the argument or make your own.
For a **developer**, it is a set of build-time constraints you either accept for the whole package or do not claim.
For a **tester**, it tells you which extra checks are in scope — and, equally usefully, which are not: a test report that fails a package against `afds-layout-intrinsic` when the manifest does not claim it is a defective report, because clause 4.3 states that a package "*MUST NOT* be judged against a method profile it does not claim" and that a consumer "*MUST NOT* treat the absence of a method-profile claim as a defect".

#### Declaring which profiles a package claims

A package that claims one or more method profiles declares them in a `methodProfiles` array in its manifest, and each element has to be a profile identifier defined in Part III or a local identifier permitted by clause 20.4 (clause 20.2).

A package claiming no profile either omits the array or supplies it empty, and the two forms have identical meaning (clause 20.2).
There is no third state, and an omitted array is not an unanswered question.

```json
{
  "methodProfiles": []
}
```

```json
{
  "methodProfiles": [
    "afds-patterns-native-first"
  ]
}
```

Both are conforming declarations: the first says the package adopts none of Part III's method choices, and the second says it adopts one of them, whole, and none of the other three.

##### Method and completeness are different questions

The manifest carries a second, unrelated field: `conformanceProfile` states how much of the package hierarchy is present, using `afds-tokens`, `afds-components` or `afds-full` (clause 34).
It says nothing whatever about method, and `methodProfiles` says nothing whatever about completeness.

The specification requires that the two axes be declared separately and forbids conflating them (clauses 20.2, 4.5).
A package can be complete and claim no method profile; a package can claim every method profile in Part III and contain tokens only.
Software reading a package "*MUST NOT* infer a value of either field from the other" (clause 20.2), and clause 4.5 repeats the prohibition for consumers generally.
The reason is that the two fields answer different questions: "is there enough here for me to use?" is a completeness question, and "was this built the way my system is built?" is a method question.

Do not use the bare word "conformance" for either axis: say "completeness profile" or "method profile", and say which.
Section B covers `conformanceProfile` and the completeness axis; this section covers method only.

##### A profile is claimed whole

A package does not claim a profile in part, and a package that satisfies some but not all of a profile's requirements does not list that profile in `methodProfiles` (clause 20.3).

The reasoning is practical: a partial claim cannot be interpreted, because if a package could claim the layout profile while using layout media queries, the claim would tell a reader nothing, and every consumer would have to re-derive from the component contracts the very thing the claim was supposed to summarise.

That leaves the question every real team hits: what do you do when you like nine tenths of a profile?
Adopting a profile's requirements without claiming the profile is permitted, and the specification says it is "expected to be common".
You may satisfy any requirement in Part III, cite the clause it came from, and record it with the requirement kind that honestly describes its status under clause 13 — most often `project-convention` — but you may not describe that as claiming the profile, in the manifest or in any human-readable artefact (clause 20.3).

If you adopt most of a profile and depart from it deliberately, clause 20.3 describes a well-defined position: you do not list the profile, you record the departure as a requirement of kind `product-deviation`, you name the clause you depart from, and you state why — with clause 13 requiring a `product-deviation` to record its cost as well as its reason.
The specification judges that more informative than a partial claim would have been, because it identifies the specific difference instead of leaving a reader to hunt for it.

#### The four profiles Part III defines

| Identifier, as it appears in `methodProfiles` | What claiming it commits the package to | Clause |
| --- | --- | --- |
| `afds-layout-intrinsic` | Intrinsic, available-space layout built from composable primitives: five axioms in every component, twelve single-purpose primitives, no layout media queries, no Shadow DOM in primitives, forced-colours surface delineation inspected and evidenced | 21 |
| `afds-reflow-scoped` | The WCAG 1.4.10 two-dimensional exception claimed only on semantic grounds, scoped to its own scrollable container, never reaching the page, with four records per claim and four environment values per reflow assertion | 22 |
| `afds-typography-colour` | One modular scale for type and space anchored at `1rem`, a 60ch measure, colour that never carries meaning alone, a default target level of Level AA, and contrast recorded per token pair | 23 |
| `afds-patterns-native-first` | Native HTML first, published patterns adopted by reference for genuine composites, a package-level pattern registry, and a gated catalogue of eight priorities | 24 |

An identifier defined in Part III is not used for any other set of requirements, and the identifiers are stable for the life of this major version (clause 20.4).

You may also define your own profile, and an identifier for a profile not defined in the specification has to be namespaced with a prefix that is not `afds-`, so that no reader mistakes a local profile for one defined by the project (clause 20.4).
A locally defined profile also has to satisfy clause 20.1, clause 20.3 and clause 20.5, and a package claiming a local profile that does not satisfy those clauses does not conform (clause 20.4).

#### Saying where a profile's ideas came from

Every profile states its provenance, and the statement identifies four things (clause 20.5):

1. what the profile adopts from work outside the project, described specifically enough that a reader can tell which parts are borrowed;
2. the source of each adopted idea, identified well enough to be found, which for a published work means author and title;
3. what the profile changes about an adopted idea, including anywhere it is stricter than its source or reaches a different conclusion;
4. what originates in the profile itself and has no external source.

The fourth element carries the weight.
Clause 20.5 calls it the one most likely to be omitted and the most important to include, because a profile that lists its influences and stays quiet about its own inventions "launders an untested opinion as settled practice"; stating that a rule originates here and rests on nobody else's reasoning is not a weakness, because it tells a reader exactly which rules to argue with.

Two prohibitions follow, both from clause 20.5.
A provenance statement does not attribute a requirement to an external source that does not support it, and a package whose profile does so does not conform; and a provenance statement is not replaced by a bibliography, because a list of references establishes that a document was read, not which idea came from where.

If you claim one of the four profiles defined in Part III, you inherit its provenance statement and are not required to restate it (clause 20.5); if you define a local profile, you supply your own, as a structured object rather than only as prose (clause 20.6).

| Member | Type | Required | Content |
| --- | --- | --- | --- |
| `adopted` | array | Yes, may be empty | What the profile takes from work outside the package |
| `changed` | array | Yes, may be empty | What the profile alters about an adopted idea |
| `originates` | array | Yes, and it may not be empty | What the profile asserts on its own authority |
| `statement` | string | No | Prose accompanying the structured members |

Each `adopted` entry records what is adopted and its source as an object with `author`, `title`, and `uri` where one exists; each `changed` entry records what changed, references the `adopted` entry it changes, and records whether the change is `stricter`, `weaker` or `different`; each `originates` entry records what originates in the profile and references the clause it applies to (clause 20.6).
A `weaker` value is permitted and is not a conformance failure — a profile may legitimately relax something its source requires, and recording that plainly is the point of the member; recording such a change as `stricter`, or omitting it, is what is not permitted.

`originates` may not be empty, and clause 20.6 explains why a validator can treat an empty one as a defect without reading a word of the content: a profile with nothing in `originates` claims to adopt everything and add nothing, and clause 20.1 requires it to add at least one thing.
For tool authors there is a limit alongside that: a validator can check that every `changed` entry references a real `adopted` entry and that `originates` is non-empty, but it cannot determine whether an attribution is truthful, and clause 20.6 states it "*MUST NOT* be represented as doing so".

---

### The intrinsic layout profile — `afds-layout-intrinsic`

Start with the problem the profile is answering, because it is not the problem breakpoints were invented for.
A user at 400% zoom, a user who has raised their default font size, and a component nested inside a narrow sidebar can all present a component with far less room than the viewport suggests, and no set of breakpoints anticipates the combinations (clause 21.5).
Designing for the web means designing without seeing the final combination, so the profile asks for programs that respond to space rather than artefacts tuned to named widths.
Claiming this profile means every component in the package meets what follows; not claiming it means none of what follows applies to your package, and no reviewer may hold you to it.

The profile's own statement is three sentences (clause 21.1):

> Layout responds to the space actually available to it, not to the width of the viewport.
> Every dimension is expressed so that it moves with the user's settings.
> Interfaces are composed from single-purpose primitives rather than assembled from bespoke per-screen layouts.

#### The five axioms

Clause 21.2 opens with the scope: a package claiming this profile "*MUST* satisfy the following five axioms in every component it contains".
These are the specification's own words:

> 1. The measure *MUST NOT* exceed 60ch, subject to the exception mechanism in clause 23.3.
> 2. Every dimension *MUST* be user-relative.
>    Author-fixed dimensions *MUST NOT* be used, except for hairline borders.
> 3. Layout *MUST* respond to available space rather than viewport width.
> 4. An element *MUST NOT* be given a fixed height.
> 5. Layout *MUST* be complete with JavaScript disabled.

Note the qualifier on axiom 1: the 60ch measure is subject to the documented per-container exception mechanism of clause 23.3, which belongs to a different profile (`afds-typography-colour`) and is described in D.7 below.

The axioms are stated as absolutes because each one fails in the presence of a single exception (clause 21.2) — one fixed height in a shared primitive reintroduces clipping under text-spacing overrides across every screen that uses the primitive, and the primitive's other correctness does not compensate.

#### What the "no px" rule actually prohibits

Axiom 2 gets heard as a superstition about pixels, so the clause states it precisely: it prohibits values frozen against the user's font-size and zoom settings.
It does not assert that the CSS pixel is a badly designed unit — a CSS pixel is an angular reference measurement, and the objection is to author-chosen values that cannot move, not to the unit (clause 21.2).

The obvious escape hatch is closed specifically: a package claiming this profile "*MUST NOT* justify author-fixed dimensions on the grounds that the value is small" (clause 21.2), so a 2px gap is as frozen as a 200px one, and the single documented exception is hairline borders, named in axiom 2 itself.

One caution on units: the specification enumerates no list of permitted units, requiring only that dimensions be user-relative (clause 21.2) and that the measure be expressed in `ch` or another font-relative unit (clause 23.3).
`rem`, `em`, `ch`, `cap` and percentages all satisfy that in practice, but treat that as guide guidance rather than a closed list, because the clause does not give one.

#### JavaScript is not prohibited

Axiom 5 is a layout requirement and not a general prohibition on JavaScript, and clause 21.2 says so explicitly.
A component may require JavaScript for its interaction; its layout may not require JavaScript to be correct, "because a layout that collapses before script executes is a layout that fails intermittently on slow connections and permanently when script errors" (clause 21.2), so a developer reading axiom 5 as "no interactive components" has read it too widely.

#### The twelve primitives

A package claiming this profile builds layout from single-purpose primitives, each of which does one thing, and the profile adopts twelve (clause 21.3).
Each one, if present in the package, has a component specification conforming to Part II, and declares the semantics it does not supply (clause 21.3).

| Primitive | What it arranges | Supplies no | Clause |
| --- | --- | --- | --- |
| Stack | Vertical rhythm between adjacent siblings | List semantics, grouping, heading structure | 21.3 |
| Box | Intrinsic surface: padding, border treatment, colour inheritance | Semantic role | 21.3 |
| Center | Constrains the measure, with gutters growing outward | Guarantee of visibility in every zoomed context | 21.3 |
| Cluster | Wraps indeterminate groups the way words wrap | Semantics or grouping | 21.3 |
| Sidebar | Two-element arrangement responding to container width | Semantics or landmark | 21.3 |
| Switcher | Switches axis at a container-width threshold | Semantics | 21.3 |
| Cover | Vertical centring with a minimum height | Semantics | 21.3 |
| Frame | Constrains media by aspect ratio | Alternative text or media semantics | 21.3 |
| Grid | Wraps self-contained items by content-driven measurement | Semantics, and no basis for the clause 22 exception | 21.3 |
| Reel | Horizontally scrolling container that acknowledges its overflow | Guarantee that overflowed content is otherwise reachable | 21.3 |
| Imposter | Overlay geometry that cannot trap its own content | Focus trap, modal semantics, focus return | 21.3 |
| Icon | Sizes an icon relative to the text beside it | Accessible name or meaning | 21.3 |

Clause 21.3 says which column matters: "The right-hand column is the operative one."
A layout primitive that silently omits semantics invites a developer to assume semantics were handled, and the omission is only safe when it is declared — Stack supplies vertical rhythm and not list semantics, so a consumer stacking list content supplies the list semantics itself (clause 21.3).
For a tester, that column is the checklist: for each primitive in the package, open its Part II specification and confirm the non-supply declaration is there before any component that composes it is reviewed.
Two primitives carry additional obligations.

**Grid.** A Grid arranges self-contained items and creates no header-to-cell relationship.
Clause 11.2 already forbids every package, profile or not, from resting an exception rationale on a layout technique, and what the profile adds is a named consequence: the Grid primitive declares in its own specification that it supplies no basis for the claim (clause 21.3).

**Reel.** Every item in a Reel is independently readable within 320 CSS pixels, so that a user scrolls in one direction to reach an item and not in two directions to read one, and content that leaves the visible region remains reachable (clause 21.3).

#### Composition rather than configuration options

Composition, rather than increasingly capable individual components, produces the interface, and a package claiming this profile does not resolve a layout need by adding configuration options to an existing primitive where composing two primitives would serve (clause 21.3).
This is the rule that keeps a primitive set from turning into a widget library; the first time somebody proposes a `variant` prop on Stack, the clause is the answer.

#### Delineating surfaces under forced colours

A surface described only by a background colour can vanish in a forced-colours mode, because the mode may replace author backgrounds with system ones (clause 21.4).
Every delineated surface in a package claiming this profile therefore carries a transparent outline with a negative offset in addition to any background colour (clause 21.4).
The outline is invisible in normal rendering, occupies no layout space, and becomes visible when a forced-colours mode assigns it a system colour.
The accepted cost is stated rather than hidden: `outline` is no longer available for unrelated surface decoration, and every surface carries a declaration whose purpose is invisible in normal use (clause 21.4).
Then the part that is easiest to skip and hardest to fake: a package claiming this profile inspects every delineated surface in a forced-colours mode, and records the result as evidence under clause 16 "rather than as an assertion believed to pass" (clause 21.4).
Applying the technique is not the requirement; looking at the result and dating the observation is the requirement, and Section C covers the shape of a clause 16 evidence record.

#### The media-query policy

A package claiming this profile does not use layout media queries (clause 21.5).

Preference queries are permitted, and clause 21.5 states that these four "are the only permitted queries":

| Query | Status under clause 21.5 |
| --- | --- |
| `prefers-reduced-motion` | Permitted |
| `prefers-color-scheme` | Permitted |
| `prefers-contrast` | Permitted |
| `forced-colors` | Permitted |
| Any layout media query (viewport width, height, orientation, aspect ratio) | Forbidden |

No media query is *required* by clause 21: the four preference queries are permitted, not mandatory, and a package claiming this profile that uses none of them is not thereby deficient, because clause 21.4's forced-colours obligation is a requirement about surfaces and evidence, not a requirement to write a `forced-colors` query.

The distinction the clause draws is that a preference query asks what the user has asked for, while a layout media query asks how wide the viewport is and then guesses what that implies, and viewport width does not reliably indicate available space (clause 21.5).

#### Styling tiers and encapsulation

Styles in a package claiming this profile are organised so that reach is inversely proportional to specificity: universal and inherited styles first, layout primitives second, utilities last (clause 21.6).

Three consequences follow, all from clause 21.6.
A component does not restate an inherited `font-family`, `color` or `line-height`, because restating an inherited value breaks the inheritance chain that the user's own settings and stylesheets travel down.
Utilities are final adjustments and are not introduced before a need exists, and utility-first, breakpoint-prefixed layout is prohibited, because it encodes a viewport assumption into each individual element and so contradicts axiom 3.

##### The no-Shadow-DOM decision

Layout primitives in a package claiming this profile do not use Shadow DOM (clause 21.6).

That is an unusual position for a component library, so the clause records three grounds.
A shadow boundary complicates the relationships accessible names and descriptions depend on, including `aria-labelledby`, `aria-describedby`, `aria-controls` and the `for` attribute; encapsulation can prevent a user stylesheet or a forced-colours override from reaching the content inside it; and light DOM permits build-time primitive styles, which is what allows axiom 5 to hold.
The accepted cost is exposure to global style leakage, and the profile accepts it on the grounds that inherited and user styles have to be able to reach primitive content: "an encapsulation boundary that blocks a user's own stylesheet has defeated a mechanism the user relies on" (clause 21.6).

One correction to the earlier edition of this guide, which said primitives are "native custom elements without Shadow DOM": clause 21.6 prohibits Shadow DOM in layout primitives and says nothing about custom elements, so whether you implement a primitive as a custom element, a class, or a utility is an implementation choice rather than a profile requirement.

#### The eleven checks for this profile

The earlier edition of this guide carried a list of eleven rules whose count matched clause 21 and whose set did not: it omitted the 60ch measure, the Shadow DOM prohibition, the styling-tier ordering, the inherited-property rule, the forced-colours evidence record, the Reel 320-pixel obligation and the composition rule.
It included "DOM order matches visual order", which has no basis in clause 21, and "no spacing or font sizes outside the modular scale", which is clause 23.2 — a *different* profile, claimed separately.
The list below is derived from clauses 21.2 to 21.6, and these are the checks that arrive with a claim of `afds-layout-intrinsic`.

| # | Check | Clause |
| --- | --- | --- |
| 1 | The measure never exceeds 60ch, subject to the documented per-container exception mechanism of clause 23.3 | 21.2 |
| 2 | Every dimension is user-relative; author-fixed dimensions appear nowhere except hairline borders, and smallness is not accepted as a justification | 21.2 |
| 3 | Layout responds to available space rather than viewport width | 21.2 |
| 4 | No element is given a fixed height | 21.2 |
| 5 | Layout is complete with JavaScript disabled, even where interaction requires it | 21.2 |
| 6 | No layout media queries; only the four preference queries appear | 21.5 |
| 7 | Every primitive present has a Part II specification declaring the semantics it does not supply, and the Grid primitive declares in advance that it founds no clause 22 exception claim | 21.3 |
| 8 | Every Reel item is independently readable within 320 CSS pixels, and content leaving the visible region stays reachable | 21.3 |
| 9 | A layout need is met by composing two primitives, not by adding configuration options to one | 21.3 |
| 10 | Every delineated surface carries a transparent outline with a negative offset, is inspected in a forced-colours mode, and the result is recorded as evidence under clause 16 | 21.4 |
| 11 | Styles are ordered so reach is inversely proportional to specificity; no component restates an inherited `font-family`, `color` or `line-height`; utilities come last; layout primitives use no Shadow DOM | 21.6 |

#### What this profile does not settle — `afds-layout-intrinsic`

The profile has one known unresolved conflict and clause 21.7 states it "*MUST NOT* be read as having resolved it".
Advisory technique C34 un-fixes a sticky header using media queries, so that sticky content does not obscure focus or consume reading space at high zoom, and clause 21.5 prohibits layout media queries, so the advisory remedy is unavailable under this profile.
Until a container-driven equivalent is designed, a package claiming this profile uses neither `position: sticky` nor `position: fixed` (clause 21.7).

Read the framing carefully, because it is the difference between a claim and an admission — clause 21.7: "This is a deferral and not a finding."
The profile does not assert that sticky positioning is inaccessible; it records that it cannot currently implement the published remedy, and declines to ship the pattern without one.
There is an explicit way out, which the earlier edition omitted: "A package needing sticky positioning should not claim this profile, and should record its own approach and evidence" (clause 21.7) — so if your product needs a sticky toolbar, decline `afds-layout-intrinsic` and document what you did instead rather than arguing with clause 21.5.

The profile also does not settle whether the 60ch measure applies inside a region claiming the clause 22 exception, is reduced there, or is suspended there, and the same question is recorded identically in clauses 22.7 and 23.7 (clause 21.7).

Do not present the sticky deferral as the profile's answer to Success Criterion 2.4.11 Focus Not Obscured: clause 21 makes no such claim, and turning a deferral into a criterion answer is the kind of overstatement clause 21.7 exists to prevent.

#### Where this profile's ideas came from — `afds-layout-intrinsic`

The intrinsic-layout argument, the axiomatic framing, the composable single-purpose primitive approach, and the twelve primitives are adopted from *Every Layout: Relearn CSS layout* by Heydon Pickering and Andy Bell, at <https://every-layout.dev/> (clause 21.8).
So are the 60ch measure, the modular scale generated by successive `calc()` from a `1rem` root, the Stack primitive's adjacent-sibling relationship, the Switcher primitive's container-width threshold, and the transparent-outline treatment for forced colours.

The adjacent-sibling selector `* + *` that Stack rests on was introduced as the "lobotomized owl selector" by Heydon Pickering in *Axiomatic CSS and Lobotomized Owls*, A List Apart, 21 October 2014, at <https://alistapart.com/article/axiomatic-css-and-lobotomized-owls/>, and the reasoning that margin is a relationship between adjacent elements rather than a property of an element belongs to that article — a point the earlier edition of this guide made while attributing it to nobody.
Every Layout is a commercial publication, and clause 21.8 records that the profile describes the method and attributes it, reproduces neither the source text nor the source code, and directs a reader wanting the original reasoning to the authors' work.

Three things the profile **changed** (clause 21.8).
Every Layout names a thirteenth primitive, The Container, which this profile does not adopt — so if you have read the source work and expect thirteen, twelve is deliberate.
The prohibition on layout media queries is absolute here, which is stricter than the source work requires, and the requirement that every primitive declare the semantics it does not supply is an application of the Part II disclosure obligation rather than a requirement of the source work.

Six things **originate here** and rest on the project's own reasoning (clause 21.8): the Shadow DOM prohibition and its three grounds; the forced-colours inspection-and-evidence requirement; the prohibition on a Grid-primitive region founding a two-dimensional exception claim; the Reel 320-pixel reading of technique G225; the sticky and fixed deferral; and the requirement that primitives be tested at 400% zoom, in forced colours, at a doubled root font size, under text-spacing overrides, and inside realistic pages rather than in isolation alone.

---

### The scoped reflow profile — `afds-reflow-scoped`

The earlier edition of this guide wrote its reflow material as project-wide rules and never named this profile at all, which inverted the structure twice over: it made a declinable profile look universal, and it blurred the line between the parts of reflow that bind every package and the parts that arrive only with a claim.
Get the split right first.

**Core, binding on every package.** The `reflowBehaviour` object of clause 11.1 and its seven required entries, and the rule in clause 11.2 that an exception rationale rests on semantic two-dimensional structure and never on visual appearance or on the layout technique used to produce it.
Section C covers both, and the fields are not repeated here; Success Criterion 1.4.10 Reflow itself, and its test conditions, are WCAG's, described there too.

**This profile, arriving only with the claim.** Everything in clauses 22.3 to 22.6: what a claim has to record, where the scroll is allowed to reach, how cells and their surroundings behave, and which environment values a reflow assertion carries.
Clause 22.2 is explicit about its own status: it explains how the core test resolves in practice, "because the test is easy to state and routinely misapplied", and then says of itself, "This clause adds no requirement."

The profile's statement is two sentences (clause 22.1):

> Two-dimensional scrolling is permitted only where the content's meaning genuinely requires two axes, is justified by naming those axes, and is confined to the element that needs it.
> It never reaches the page.

#### When the exception genuinely applies

A region qualifies when a cell's significance depends on its relationship to both a row axis and a column axis, so that flattening the structure would destroy meaning rather than merely rearrange appearance (clause 22.2).
A CSS Grid container has no table semantics: declaring `display: grid`, or wrapping items with a content-driven measurement, creates no row header, no column header and no header-to-cell relationship, so visual grid arrangement is not offered as a basis for the exception, and the clause records how the test resolves for common cases (clause 22.2).

| Content | Basis | Excepted |
| --- | --- | --- |
| Results table with genuine row and column header relationships | A cell's significance depends on both axes | Yes, as a scoped region |
| Programme guide organised by channel and time | Channel and time are both meaning-bearing axes | Yes, as a scoped region |
| Collection of self-contained cards | Arrangement is presentational | No |
| Dashboard laid out in grid areas | Arrangement is presentational | No |
| Filter panel beside a results list | Adjacency is convenience, not meaning | No |

The programme-guide row establishes that a meaning-bearing two-dimensional structure need not be a conventional data table, and clause 22.2 immediately fences that off: it "*MUST NOT* be read as extending the exception to visual grids generally".

Two limits on this table are worth stating, because clause 22.8 states them.
The reading that the exception rests on a semantic relationship rather than a visual arrangement is this project's analysis of the criterion's wording — "a defensible reading and it is not a W3C ruling" — and the table itself is the project's application of that reading to cases the Working Group has not adjudicated.

#### The four records a claim has to carry

Clause 11.2 requires a rationale resting on semantic two-dimensional structure, and this profile makes that rationale specific: a component or region in a package claiming the profile does not claim the two-dimensional exception without recording all four of the following in its component specification (clause 22.3).

| # | Record | Clause |
| --- | --- | --- |
| 1 | The identification of both meaning-bearing axes | 22.3 |
| 2 | An explanation of how a cell's significance depends on each axis | 22.3 |
| 3 | A statement of the semantic structure that carries the relationship, which has to be a table structure or an ARIA grid structure and may not be a purely presentational arrangement | 22.3 |
| 4 | The boundary of the excepted region, so that a tester knows what is inside the claim and what is outside it | 22.3 |

The earlier edition of this guide covered the first two and dropped the last two, which are the ones a tester actually works from.
"It is displayed as a grid" is not recorded as a justification, and clause 22.3 states that a specification offering it does not conform.
A region needing the exception needs semantic structure first, and where it is absent, clause 22.3 says the correct response is to supply it or to abandon the claim; changing a role in order to qualify is already forbidden by clause 11.2 and is not restated as a profile requirement.

#### Scoping the scroll

An excepted region is placed in its own scrollable container, and two-dimensional scrolling does not reach the page in a package claiming this profile (clause 22.4).

Clause 22.4 labels itself honestly: page-level bidirectional scrolling can conform where the content is genuinely excepted, "so this requirement is stricter than the criterion".
The profile adopts it anyway, on a usability argument of the project's own — a page-level horizontal scrollbar tells a user that content exists off-screen everywhere, when in fact it exists in one region, and the user is left searching for material that is not there — and clause 22.8 confirms that reason "is a usability argument of this project's own and is not a WCAG requirement".
Scoping the scroll also lets every surrounding part of the page reflow normally, which is what clause 22.5 requires.

#### Cells and the content around them

The exception applies to the excepted region and to nothing else (clause 22.5).
A heading introducing an excepted region, its surrounding prose, a search field, filter controls, pagination, and any other adjacent interface reflow as ordinary content and are tested as ordinary content (clause 22.5).

An individual cell meets the criterion as ordinary flow content, unless it contains material that independently requires two-dimensional presentation for usage or meaning (clause 22.5).
The WCAG qualification "not individual cells" marks where the semantic relationship stops: the table needs both axes to mean what it means, and one cell's content does not.

Four obligations follow for cell content, all from clause 22.5.
A long selector, a URL, a failure description, and a code excerpt appearing in a cell either wrap at 320 CSS pixels or provide a mechanism by which a user can reveal the complete value.
A truncated string is not the only presentation of a value, and truncation is permitted only where a user can reveal the complete value or reach a complete alternative presentation — the earlier edition of this guide covered wrapping and never addressed truncation at all, which left the most common real-world shortcut unexamined.
Content does not disappear on reflow without remaining reachable.
Where indentation carries meaning, as in nested lists and code, it is reduced under magnification rather than removed — reduce, not preserve-with-exceptions.
Whether a particular code cell may wrap or must preserve non-wrapping indentation is a component-level judgement, and clause 22.7 records that the profile does not settle it.

#### The four values every reflow assertion carries

A package claiming this profile records, for every reflow assertion, the device, the browser, the starting viewport, and the zoom level at which the observation was made or is to be made (clause 22.6).

Clause 22.6 gives the reason plainly: a reflow result without those four values is not interpretable, because "no content is clipped" is a different statement at a 320 CSS pixel viewport than at a 1280 by 1024 starting viewport with 400% zoom applied.
For a tester this is the single highest-value line in the clause — an assertion missing any of the four is not a weak result but an uninterpretable one.

#### The published techniques this profile relies on

Clause 22.6 names eight W3C techniques for WCAG 2.2 and cites them as published; the techniques index is at <https://www.w3.org/WAI/WCAG22/Techniques/>.

| Technique | Use under this profile | Clause |
| --- | --- | --- |
| C31, Flexbox to reflow content | Primary mechanism for the Cluster, Sidebar and Switcher primitives | 22.6 |
| C33, Reflow with long URLs and strings | Required in table cells | 22.6 |
| C38, Width, max-width, and Flexbox for labels and inputs | Required for filters and forms | 22.6 |
| SCR34, Sizes and positions scale with text | Satisfied by the modular scale of clause 23.2 | 22.6 |
| G224, Meaningful indentation and Reflow | Required wherever indentation carries meaning | 22.6 |
| G225, Horizontally scrolling panels fit 320 CSS pixels | Required for Reel items, read strictly per clause 21.8 | 22.6 |
| G206, Layout alternative without horizontal scrolling | Permitted enhancement for an excepted region; not required | 22.6 |
| C34, Un-fix sticky headers with media queries | Unavailable under `afds-layout-intrinsic`; see clause 21.7 | 22.6 |

Two of those rows carry cross-profile consequences: SCR34 is satisfied by the scale of clause 23.2, which belongs to `afds-typography-colour` — a package claiming `afds-reflow-scoped` alone has to satisfy SCR34 some other way or record that it does not — and C34's unavailability is a consequence of clause 21.5, so it only bites a package that also claims `afds-layout-intrinsic`.

One point of precision about C31: clause 22.6 notes that it is a *sufficient* technique for Success Criterion 1.4.10 rather than a statement of compatibility with it, so a package building composition from Flexbox is implementing a technique the Working Group deems sufficient, which the clause calls "a stronger position than asserting that the criterion is met".

#### What this profile does not settle — `afds-reflow-scoped`

Success Criterion 1.4.4 Resize Text requires text to be resizable to at least 200%, and it does not require a specific amount of text enlargement at the test condition of Success Criterion 1.4.10.
Clause 22.7 records that a 200% zoom producing a viewport smaller than that test condition "is not for that reason alone a failure of 1.4.10" — a distinction the profile records without relying on it to excuse anything.

Three questions remain open, and clause 22.7 states that a package claiming this profile "*MUST NOT* represent them as answered":

1. whether an excepted region should also offer a user-selectable alternative presentation without horizontal scrolling, under technique G206;
2. when code inside a cell needs preserved non-wrapping indentation and when it must wrap;
3. whether the 60ch measure applies inside an excepted region, is reduced there, or is suspended there.

#### Two corrections kept on the record

Clause 22.8 records two changes of mind, "because a reader is entitled to know the profile changed its mind".
An earlier position in this project treated wide tables at 400% zoom as an unresolved weakness of its layout method, which was wrong: a table with genuine two-dimensional semantic relationships is excepted, and the real work is scoping the exception correctly.
An earlier wording claimed the exception "covers grid-based UI generally", which was also wrong, conflating semantic grid structure with CSS Grid layout.
Clause 22.8 also records what originates here: the reading in clause 22.2, the resolution table, the four records of clause 22.3, the prohibition on "it is displayed as a grid", the prohibition on a Grid-primitive region founding a claim, and the requirement that every reflow assertion record device, browser, starting viewport and zoom; it further records that clause 22.5's treatment of long strings in cells applies technique C33 as a requirement of this profile, where the technique itself is sufficient rather than required.

---

### The typography and colour profile — `afds-typography-colour`

The earlier edition of this guide scattered this profile's material through its layout chapter, so a reader who declined the layout method could not tell that the scale, the measure and the contrast obligations were a separate, separately-claimable set — they are: you can claim `afds-typography-colour` and no other profile, or every other profile and not this one.

The statement is two sentences (clause 23.1):

> Type and space are generated from one scale seeded at the user's own text size, so that changing that size moves the whole interface together.
> Colour reinforces meaning and never carries it alone.

#### One scale, anchored at `1rem`

A package claiming this profile generates font sizes and spacing from a single modular scale, and five obligations come with that, all from clause 23.2.
The scale is anchored at `1rem`, so that the user's own root font size is the seed for every derived value.
Each point on the scale is derived from the preceding point by calculation rather than chosen independently.
Body text uses a line height of 1.5.
The largest and smallest text on one surface do not differ by more than 3:1.
A font-size or spacing declaration references a scale value, and a literal value is not used.

Clause 23.2 explains why the shared seed matters more than the individual numbers: because type, gaps and padding all derive from the same root, "a user who raises the default text size gets a proportionally larger interface rather than larger text crammed into unchanged spacing".
One line of body text is the natural denominator for vertical rhythm, which is why the line height and the scale ratio are the same number — 1.5 in both cases.
The accepted cost is stated: available sizes are few and widely separated, and display typography is constrained (clause 23.2).

A worked scale, for illustration only:

```json
{
  "scale": {
    "step--1": "0.75rem",
    "step-0": "1rem",
    "step-1": "1.5rem",
    "step-2": "2.25rem"
  }
}
```

Each step is the previous one multiplied by the ratio, and spacing tokens are aliases of scale steps rather than independent values — which is what "*MUST* reference a scale value" (clause 23.2) means in practice.

##### There is no minimum text size in the specification

Say this plainly, because a 16px floor has been asserted as project policy before.
The specification sets no minimum text size anywhere, and the string `16px` does not occur in `docs/AFDS-SPECIFICATION.md`.
The nearest provisions are the `1rem` scale anchor and the 3:1 on-surface ratio, both in clause 23.2, and neither is a floor in absolute units.
A `1rem` anchor is deliberately *not* a minimum: it defers to whatever the user's root font size is, which is the whole point of anchoring there.
If you want a floor, do not read one into clause 23.2 — raise it against the specification; this guide records the absence as a specification gap in its audit block rather than inventing a number.

#### The measure

The measure is line length expressed in characters, and a package claiming this profile does not allow it to exceed 60ch (clause 23.3).

The cap is applied exception-based: content is capped broadly, and deliberate exceptions are named per container rather than granted by default (clause 23.3).
An exception has to be documented, and clause 23.3 states the consequence in five words: "an undocumented exception fails review".
That is the sentence to put in front of a designer who wants a wider container for one page.

The measure is expressed in `ch` or another font-relative unit and is not expressed as an author-fixed width, because a character measure cannot be guaranteed by a pixel width: the number of characters that fits in a fixed width changes as the font size changes (clause 23.3).
Because `1ch` varies with font size, text at different sizes occupies different proportions of the same wide container, and clause 23.3 says that is a consequence of the axiom rather than a defect.

One relationship to keep straight, because it is easy to assume one obligation discharges the other.
The measure axiom and Success Criterion 1.4.10 approach one concern from opposite directions: the axiom limits line length positively, as a typographic commitment, and the criterion prevents unbounded line length under magnification, as a floor (clause 23.3).
Clause 23.3 adds the sentence the earlier edition of this guide omitted — "Satisfying one does not satisfy the other" — and clause 23.8 records that the observation originates with the project.

#### Colour does not carry meaning alone

In a package claiming this profile, status, severity, and any other meaning conveyed by colour is also conveyed by text or by shape, colour is reinforcement only, and an unlabelled colour-coded severity scheme is not used (clause 23.4).

Clause 23.4 gives two independent reasons, and says either alone would justify the requirement.
A colour-only encoding is unavailable to users whose colour vision does not distinguish the chosen hues, and it is also unavailable to any user in a forced-colours mode, because the mode may replace the author's palette entirely, and a distinction carried only by hue does not survive that replacement.
The accepted cost, in the clause's own words: interfaces look plainer.

For a designer, the practical test is to render the interface in greyscale and then in a forced-colours mode; anything that stops being distinguishable was carrying meaning by colour alone.

#### Contrast: a declared level and per-pair records

This profile sets its default target level under clause 12.4 at **Level AA** (clause 23.5).

A component in a package claiming this profile may amend that default under clause 12.4, upward or downward, and amending it is recorded with a reason (clause 23.5).
Clause 12.4 sets the resolution order: a component's own declaration, then the default set by a claimed method profile, then the package default, with the first available declaration governing.

The profile is not to be read as fixing a contrast ratio independently of the declared level: the applicable ratios are those WCAG 2.2 attaches to the effective target level, and clause 23.5 declines to restate them because doing so "would duplicate WCAG and would go stale when WCAG does not" — so do not look for a number in clause 23.5; there deliberately is not one.

Why AA rather than AAA, when AAA looks more rigorous?
A profile-wide AAA default would set a threshold the project has not established is usable across data-dense reporting surfaces, and "a default that packages routinely amend downward is a worse instrument than a default they can honestly hold" (clause 23.5).
AAA remains available and is expected to be the right amendment for many components, which is why clause 12.4 makes amending upward as ordinary an act as amending downward, and clause 23.8 grounds the choice further: WCAG 2.2's own Conformance section states that "It is not recommended that Level AAA conformance be required as a general policy for entire sites because it is not possible to satisfy all Level AAA success criteria for some content", at <https://www.w3.org/TR/WCAG22/>.

What the profile does require, independently of the level, is that the claim be measured per pair: a package claiming this profile records, for each foreground and background token pair it treats as valid, the measured ratio and the effective target level that pair was measured against (clause 23.5).

A palette-level claim is not recorded in place of per-pair records, because contrast is a property of a pair and not of a set: "a claim about a palette is not checkable, and a palette that satisfies a threshold in most combinations satisfies nothing in particular" (clause 23.5) — a brand palette expressed purely as tokens is a set of pairing candidates, not a set of verified pairs.

There is a gap here the profile cannot close, and it says so: design token formats carry values and have no standard expression for the statement that one foreground token is valid on one background token at a given threshold (clause 23.5).
Until such an expression exists, a package claiming this profile carries its verified pairs as assertions under clause 15, with evidence under clause 16, rather than expecting the token file to express them (clause 23.5) — Section C covers the shape of both records.

Clause 23.8 records that the per-pair requirement and the prohibition on palette-level claims originate with the project: "WCAG requires a ratio to be met and does not say where the measurement is recorded, so the per-pair record is this project's requirement."

#### Declaring the typefaces a package depends on

A typeface is treated the same way as a target level: declared by the author, not mandated by the profile, and the profile is not to be read as requiring a particular typeface or setting a default one (clause 23.6).

Three declarations arrive with the claim (clause 23.6).
A package claiming this profile declares the typefaces it depends on, and declares whether the interface remains usable when they are unavailable.
A component may declare a typeface dependency of its own, and one that does records why the package default is insufficient for it.

The second of those is the one teams skip: "which font do we use" is a design decision; "does the interface still work when the webfont fails to load" is an accessibility disclosure, and clause 23.6 asks for it in writing.

No default is set because the project has not settled one, and Atkinson Hyperlegible, published by the Braille Institute, is under consideration and has not been adopted (clause 23.6).
Clause 23.8 records what is known about it: the family is published at <https://www.brailleinstitute.org/freefont/>, is offered in three versions, and the original typeface was introduced in 2019.
It also records a discrepancy it declines to resolve — the download page and the release announcement of 10 February 2025 differ on the name of the monospaced member, which the download page calls Mono and the announcement calls Monospace, at <https://www.brailleinstitute.org/about-us/news/braille-institute-launches-enhanced-atkinson-hyperlegible-font-to-make-reading-easier/> — and were the typeface adopted later, clause 23.6 notes the mechanism already exists: the profile would name it as its default and packages would remain free to amend.

#### The media-query position for this profile

Clause 23 imposes no media-query policy of its own, and the permitted, forbidden and required queries listed in D.5 come from clause 21.5 and bind only a package claiming `afds-layout-intrinsic`, so a package claiming `afds-typography-colour` and not the layout profile is under no clause-21 restriction on media queries at all.

Forced colours reaches this profile from a different direction: clause 23.4's second reason for the colour-not-alone rule is forced-colours replacement of the author palette, so a package claiming this profile has a stake in forced-colours behaviour even without the surface-delineation obligation of clause 21.4, whose outline, inspection and evidence record arrive only with the layout profile.
If you claim `afds-typography-colour` alone, test in a forced-colours mode anyway — clause 23.4's requirement is unverifiable without it — but do not cite clause 21.4 as your basis.

#### What this profile does not settle — `afds-typography-colour`

The profile sets a default target level of Level AA and sets no default typeface, and clause 23.7 states that neither is a finding about what is sufficient for users.
Three questions are open (clause 23.7).

1. whether the project should raise its own default to Level AAA, and whether the 7:1 ratio Level AAA attaches to body text remains usable on data-dense reporting surfaces — clause 23.7 notes what *is* settled, that the answer is a declaration and not a requirement of the specification, so the question can stay open without blocking a package from conforming;
2. whether the profile should name a default typeface, and whether that typeface should be Atkinson Hyperlegible;
3. whether the 60ch measure applies inside a region claiming the clause 22 exception, recorded identically in clauses 21.7 and 22.7.

#### Where this profile's ideas came from — `afds-typography-colour`

The 60ch measure, the modular scale generated by successive calculation from a `1rem` root, and the practice of deriving spacing and type from one seed are adopted from *Every Layout: Relearn CSS layout* by Heydon Pickering and Andy Bell, at <https://every-layout.dev/> (clause 23.8).

A line height of 1.5 for body text corresponds to the line-height value that Success Criterion 1.4.12 Text Spacing requires content to tolerate, at <https://www.w3.org/TR/WCAG22/>, and that is also the source of the 1.5 text-spacing ratio: the number is WCAG's tolerance figure, adopted here as a positive commitment rather than as a tolerance, and the requirement that sizes and positions scale with text is consistent with W3C technique SCR34 for WCAG 2.2 (clause 23.8).

Clause 23.8 is unusually careful about what the profile does *not* claim.
The reasoning that over-long lines make it harder to track from one line to the next, and that this bears particularly on users with dyslexia, low vision or attention-related disabilities, is described as the standard argument for a measure cap in typographic practice: "This profile asserts no research finding of its own on the point and quantifies no benefit."
The conformance levels are WCAG 2.2's, and "This profile defines no level, no ratio, and no threshold of its own."

One number in the clause has no published source at all.
The 3:1 limit on the ratio between the largest and smallest text on one surface originates with the project, and rests on the argument that a screen-magnifier user should not have to change zoom repeatedly when moving between a heading and the body copy beneath it.
Clause 23.8: "A reader who wants to challenge one number in this clause should challenge this one."
The earlier edition of this guide presented the 3:1 figure without that caveat, which made an asserted opinion look like settled practice.
Clause 23.3's requirement that the measure cap be applied exception-based with documented per-container exceptions is likewise a process requirement of the project and not a requirement of the source work (clause 23.8).

---

### The native-first pattern profile — `afds-patterns-native-first`

This is adopted, normative policy: the open-questions register records G2, "Adopting APG by reference", as **Settled, 2026-09-01** — native HTML first, and published patterns adopted by reference rather than copied.
The specification carries it as the `afds-patterns-native-first` profile at clause 24, and the sample package claims that profile.

The earlier edition of this guide described the policy as "proposed and not yet adopted" and said the five statuses were "proposed", and both statements were stale.
The five-status vocabulary is core, at clause 9.2, and binds every package whether or not it claims this profile; the native-first preference is a normative statement of this profile.

The profile's statement has five clauses (clause 24.1):

> WCAG establishes the required outcome.
> Native HTML is preferred.
> ARIA fills genuine semantic gaps.
> A published pattern guide supplies the interaction model for recognised custom patterns.
> The package specifies, tests, versions, and evidences the implementation actually shipped.

Note the order, and keep it (clause 24.1).
The normative outcome sits first, because a disagreement about behaviour then resolves against an outcome rather than against a preference; the second clause sets the default engineering answer, because native elements arrive with focus behaviour, activation semantics, disabled-state handling and forced-colours treatment already implemented and already tested by browser vendors.
The third confines ARIA to the repair role it was designed for, and the fourth admits that some interactions have no native equivalent and that a custom one should behave the way users already expect.
The fifth locates responsibility, "because no external document can carry evidence about the code a package actually ships".

Clause 24.8 adds a constraint on how you cite the statement: it is this project's formulation, no external body states it, and it "*MUST NOT* be attributed to the W3C or to any working group".

#### The status names changed — use the current ones

Clause 9.2's five values are `native-first`, `pattern-derived`, `pattern-adjacent`, `custom` and `prohibited`.

Earlier drafts in this project named two of them after the ARIA Authoring Practices Guide specifically — `APG-derived` and `APG-adjacent` — and clause 24.8 records that they were renamed "so that the core vocabulary of clause 9 does not presuppose one pattern guide".
The old names are retired: if you have met them in the earlier edition of this guide, in a component specification, or in a registry, they should be updated to `pattern-derived` and `pattern-adjacent`.

There is a related prohibition that reaches every package, profile or not: clause 4.4 states that a package "*MUST NOT* claim that a component conforms to the ARIA Authoring Practices Guide, because that guide is informative and has no conformance model to conform to", and clause 24.7 recalls it informatively because this profile is where the temptation arises.
The publishable claims about a component are the accessibility criteria met, the semantics used, and the recorded assistive-technology results (clause 4.4), and the sentence "this component conforms to the APG" is never published as an accessibility claim.

#### The pattern registry

Clause 9 already requires every component to declare a `derivation.status` from the five values, and already imposes the extra obligations `pattern-adjacent` and `prohibited` carry; none of that is restated in clause 24, and a package that claims no profile is bound by all of it (clause 24.2).

What this profile adds is a package-level artefact: a package claiming this profile carries a registry listing every component and pattern in the package against its status (clause 24.2).
Part IV fixes its location — the registry sits at `patterns/registry.json`, is declared in `patterns.canonicalSources` with role `canonical`, appears in the inventory, and no package uses that path for anything other than a registry satisfying clause 24.2, whether or not it claims the profile (clause 29.4).

Two rules govern its contents.
The registry does not disagree with any component's own declaration, and where the registry and a component specification differ, the component specification governs and the package is defective (clause 24.2) — that is the resolution order to encode in a validator: component first, registry second, and a mismatch is a defect rather than a question.
The registry also records a `prohibited` entry for a pattern the package has declined, even though no component implements it (clause 24.2).

Clause 24.2 says that last requirement is the reason the artefact is worth having, because a decision not to build something leaves no component behind to declare it, and without a package-level registry a prohibition is invisible: "the absence of a menubar component looks identical to nobody having considered a menubar, and the argument gets held again in the next review".
Clause 9.2 adds the shape of that no: a `prohibited` entry states the cost that motivated the prohibition and is revisitable if the underlying support picture changes.

#### Choosing native first

The rule is stated as a restriction rather than as an endorsement, because clause 24.3 identifies the likeliest failure mode for a system that admires a pattern guide: turning every familiar interaction into a custom widget.

> Use native HTML when it provides the needed semantics and interaction.
> Adopt a published pattern only when a genuinely custom composite widget is required.

| Product need | Preferred response | Why |
| --- | --- | --- |
| Action | Native `<button>` | Activation, focus, disabled state, and keyboard behaviour are already provided |
| Choice between options | Native radio or checkbox inputs | Avoids recreating form semantics |
| Navigation | Links inside a navigation landmark | Do not convert site navigation into a menu widget |
| Reveal supplementary content | Native `<details>`, or a button with controlled content | Often avoids a full custom disclosure implementation |
| Modal confirmation | A dialog component following the published dialog model | A genuine composite interaction with focus-management needs |
| Rich autocomplete | A combobox, only where native controls cannot satisfy the task | High complexity; semantics and keyboard contract must be complete |
| Large interactive results table | A native table first; an ARIA grid only where directional cell navigation is genuinely needed | A visual CSS grid is not a semantic grid and does not justify the clause 22 exception |

The rows are ordered from cheapest to most expensive, and that is the only ordering claim the clause makes; the earlier edition of this guide reordered the table and asserted that the first four rows "account for the large majority of interactive surface", a claim that appears nowhere in clause 24.3 and should not be repeated.

The operative obligation is stated at full strength: in a package claiming this profile, a component is not given a `pattern-derived` status where a native element in this table would have supplied the semantics and interaction, unless the component specification records why the native element was insufficient (clause 24.3).
Not "should probably be native-first" — the specification puts this at *MUST NOT* strength, and it is this profile's single operative addition to the Part II disclosure duty, which requires a package to record the native baseline it considered where this profile requires it to prefer that baseline.
Clause 24.8 records that this rule originates here, and describes it as "the design rule that Part II deliberately declined to impose".

#### Reviewing a derived component: twelve items

Clause 24.4 is informative and creates no requirement; it exists because reviewing a derived component means checking twelve things distributed across eight core clauses, and a reviewer working from the core alone reassembles the list every time, in practice incompletely.
Every item below is required by the clause named beside it, not by this profile, and because clause 20.1 forbids a profile from restating a core requirement, removing this profile's claim removes none of these obligations (clause 24.4).

| # | Review item | Required by |
| --- | --- | --- |
| 1 | The published pattern it derives from, with its source URL | 9.3 |
| 2 | The native alternative considered, and why it was insufficient | 9.3 |
| 3 | Every deviation from the pattern, with reason and cost | 9.3 |
| 4 | Whether the pattern is support-dependent, and its reassessment trigger | 9.3, 9.5 |
| 5 | The semantic model | 8 |
| 6 | The keyboard contract | 10 |
| 7 | The focus lifecycle | 10.4 |
| 8 | Pointer and touch parity, and speech-recognition operation | 10.2 |
| 9 | Reflow behaviour, and any two-dimensional exception claim | 11, 11.2 |
| 10 | The WCAG success criteria the component affects | 12 |
| 11 | Assistive-technology evidence for its claims | 16 |
| 12 | Its guarantees, non-guarantees, and recorded uncertainty | 14, 17 |

A specification missing any of the twelve is incomplete under the core, not under this profile (clause 24.4).
The earlier edition of this guide gave ten of these and implied closure, dropping items 3, 4, 9 and 12 — the deviation record, the support dependency, the reflow behaviour and the guarantee set.
One count to keep separate: these twelve review items are written for engineering review, and they are not the eleven design-tool annotation fields of clause 19, which are written for design handoff — clause 24.4 says the two lists "overlap in subject and differ in audience, count, and purpose, and a count of one is never a count of the other".

#### Two cautions, and a correction to the earlier guide

Clause 24.5 carries two cautions the profile judges strong enough to sit in the profile itself, and one of them corrects the earlier edition of this guide.

##### Menu and menubar are not for ordinary navigation or action lists

Read the first half of this caution before the second, because the earlier edition of this guide got the first half wrong.
The published menu and menubar pattern is not restricted to application menus, and the pattern guide ships a navigation menubar example demonstrating site navigation (clause 24.5).
Clause 24.5 draws the conclusion in its own words: "Using a menubar for site navigation is therefore a sanctioned use of that pattern and *MUST NOT* be described as a misuse of it", and clause 24.8 repeats it from the other direction: "the APG sanctions the use this profile declines."

The earlier edition of this guide listed "converting site navigation into a menu widget" as a common mistake; that was a contradiction of clause 24.5, and if you have met that text, treat it as withdrawn.
What clause 24.5 actually says is that the caution "stands as a convention of this profile with a stated cost, which is the honest form for it", and the cost is the whole composite contract: a roving-focus model, a single tab stop, author-managed arrow-key movement, submenu open and close behaviour, and a role that causes a screen reader to describe the thing as a menu rather than as navigation.
The profile judges that cost unjustified where a list of links inside a navigation landmark already gives users a structure they know and costs nothing to maintain, and it notes that a list of buttons is usually an action group, with a toolbar the cheaper composite where one is genuinely warranted (clause 24.5).

There is an explicit route through: a package claiming this profile may nonetheless adopt a menubar, and if it does, the justification appears in the component's specification, tagged as a `product-deviation` under clause 13, with the keyboard contract written out in full (clause 24.5).
Clause 13 requires a `product-deviation` to record its cost as well as its reason, so the roving-focus contract above is the cost you write down.

##### An ARIA grid is not a remedy for visual density

A grid widget is justified by a need for directional cell navigation, and clause 24.5 states it "*MUST NOT* be justified by a table looking crowded or by a wish to avoid reflowing content".
Where the underlying difficulty is that a wide table is hard to use at high zoom, the response is a scoped scroll container and a correctly justified exception under clause 22, and clause 24.5 states that the response "*MUST NOT* be a role change" — which closes a loop with clause 11.2, forbidding the adoption of a widget role in order to unlock the exception and telling a consumer encountering such a rationale to treat the package as defective.

One vocabulary note that saves confusion in review: "Grid" names three different things in this material — the CSS Grid layout module, the Grid layout primitive of clause 21.3, and the ARIA grid widget role — and only the third carries interaction semantics, while none of the three justifies the clause 22 exception on its own.
Clause 24.8 records that the characterisation of the grid pattern as covering both tabular information and layout containers is the APG's own, the pattern being titled "Grid (Interactive Tabular Data and Layout Containers)" in the pattern index at <https://www.w3.org/WAI/ARIA/apg/patterns/>.

#### The approved component catalogue and its gates

A package claiming this profile does not implement a pattern catalogue larger than the product needs, which is a prohibition rather than a preference and the first thing clause 24.6 says.
The profile defines an ordered catalogue: priorities 1 to 5 may be adopted on judgement, and priorities 6 to 8 are not adopted without a recorded justification, recorded at the time the gate is passed rather than reconstructed later (clause 24.6).

| Priority | Pattern or primitive | Gate | Clause |
| --- | --- | --- | --- |
| 1 | Native button, link, checkbox, radio, text input, select | None | 24.6 |
| 2 | Disclosure | None | 24.6 |
| 3 | Dialog | None | 24.6 |
| 4 | Alert and status messaging | None | 24.6 |
| 5 | Native table with a scoped scroll container | None | 24.6 |
| 6 | Tabs | Recorded finding that persistent peer views improve a task | 24.6 |
| 7 | Combobox | Recorded finding that a large controlled vocabulary must be searched | 24.6 |
| 8 | Tree, treegrid, or ARIA grid | Recorded user research demonstrating the need | 24.6 |

The ordering is deliberate: priorities 1 to 5 consist almost entirely of native elements and one simple composite, and in an audit and remediation product they cover the core work, while priorities 6 to 8 carry complex keyboard and assistive-technology contracts, and each unused composite adds untested surface (clause 24.6).

One gate has a named prohibition attached: visual density is not recorded as the gate justification for priority 8 (clause 24.6), which is the same argument as the second caution in clause 24.5, closed off at the point where it would otherwise re-enter as a catalogue decision.

The "recorded at the time the gate is passed" wording matters for testers and auditors, because a justification written six months later, when somebody asks why the treegrid exists, does not satisfy the clause.

#### What this profile does not settle — `afds-patterns-native-first`

Clause 24.7 adds no requirement and recalls two clause 4.4 prohibitions informatively, because this profile is where the temptation to breach them arises: no package claims conformance to a pattern guide, and no producer presents a package claim as evidence that a service assembled from the package is accessible.

The catalogue in clause 24.6 is sized for an accessibility audit and remediation product, and clause 24.7 adds: "It is not a general recommendation, and a package with a different purpose should expect a different catalogue" — so do not read the eight priorities as a recommended component roadmap for an arbitrary product.

Whether any given project adopts this profile as a standing position is a matter for that project and not for the specification (clause 24.7); the profile defines what claiming it commits a package to and does not recommend that a package claim it.
The open-questions register keeps related items live.
G1 asks what user or task evidence admits a pattern to the catalogue and what removes one, noting that the priority order is "reasoned rather than evidenced".
G2, though settled on the native-first policy itself, records as still open how a deviation from a pattern convention is recorded and reviewed: clause 13 gives the deviation a requirement kind and clause 24.5 requires a menubar adoption to be justified in the component specification, but no review process is attached to either; G3 records that no minimum assistive-technology matrix has been fixed per component.

#### Where this profile's ideas came from — `afds-patterns-native-first`

The interaction models, keyboard expectations and pattern definitions this profile refers to as published patterns are those of the W3C ARIA Working Group, *ARIA Authoring Practices Guide (APG)*, at <https://www.w3.org/WAI/ARIA/apg/>, with the pattern index at <https://www.w3.org/WAI/ARIA/apg/patterns/> (clause 24.8).
The APG is informative and has no conformance model, which is why clause 24.7 prohibits claiming conformance to it and why the fifth clause of the statement places evidence in the shipping layer, and the scope statements about menu and menubar, including the navigation menubar example, are the APG's own, at <https://www.w3.org/WAI/ARIA/apg/patterns/menubar/>.
The required outcomes the profile defers to are W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*, at <https://www.w3.org/TR/WCAG22/>; the repair role assigned to ARIA reflects W3C, *Accessible Rich Internet Applications (WAI-ARIA) 1.2*, at <https://www.w3.org/TR/wai-aria-1.2/>; and the native elements preferred in clause 24.3 are those of WHATWG, *HTML*, Living Standard, at <https://html.spec.whatwg.org/multipage/>.

Clause 24.8 also cites Putnam, Rose and MacDonald's study of accessibility in user-experience practice, in which design systems were the most frequently reported concrete action, at <https://doi.org/10.1145/3575662> — and immediately notes that the study warns that concentrating responsibility in specialist teams risks abdication elsewhere, and that "this profile does not claim the paper endorses its approach".

**Originating here** (clause 24.8): the five-status vocabulary and the definitions of `pattern-adjacent` and `prohibited`, which were devised in this profile and have since moved into the core at clause 9 and are no longer this profile's to claim; the package-level registry artefact and the declined-pattern entry; the grouping of twelve review items; the native-preference rule of clause 24.3; the menubar caution as a project convention with a stated cost; the caution against an ARIA grid for visual density; and the catalogue, its ordering and its gates.

One correction is kept on the record (clause 24.8).
An earlier framing in this project treated the APG as the component layer of the design system, which was wrong in kind, because the APG describes patterns while a design system ships versioned artefacts with tests and evidence, and only the latter can be held to account; the status `pattern-adjacent` was added specifically because that framing left no honest label for a component resembling a pattern without implementing it.

---

### Deciding which profiles to claim

A short decision procedure, for a team reading Part III for the first time.
Start from zero claims: an empty `methodProfiles` array is a conforming declaration, and clause 4.3 says a consumer may not treat the absence of a claim as a defect.
Then take each profile in turn and ask whether you can hold *all* of it, because clause 20.3 permits no partial claim.

| If this is true of your organisation | Then |
| --- | --- |
| You have a working breakpoint system you intend to keep | Do not claim `afds-layout-intrinsic`; declare your media-query use in `reflowBehaviour` (clause 11.1) and you satisfy the core |
| You need `position: sticky` | Do not claim `afds-layout-intrinsic`; record your own approach and evidence (clause 21.7) |
| You have a fixed brand palette and a type scale you did not derive from `1rem` | Do not claim `afds-typography-colour`; the core still requires the contrast assertions and evidence |
| You have wide data tables and want the exception scoped rigorously | `afds-reflow-scoped` is likely worth claiming; clause 11.2 binds you either way |
| Your component catalogue is larger than the eight gated priorities and you intend to keep it | Do not claim `afds-patterns-native-first`; clause 24.6 prohibits a catalogue larger than the product needs |
| You like nine tenths of a profile | Adopt the requirements, cite the clauses, record the departure as a `product-deviation` naming the clause, and do not list the profile (clauses 20.3, 13) |

Having decided, declare what you claim separately from your completeness profile, and let neither be inferred from the other (clauses 4.5, 20.2, 34).

## Part 6. The package

### Packaging a design system so that it arrives intact

Everything the earlier sections describe is a set of facts about a design system: what a component promises, what it refuses to promise, which keys operate it, what was observed on which engine, and what nobody has checked yet.
This section is about the last mile.
It answers how those facts get from the team that wrote them to the team that relies on them, without any of them being lost, reordered, or quietly rewritten on the way.

Three readers are served here.
A designer wants to know what a package is and what has to be in one before it can be handed over; a developer wants the field lists, because a producer writes them and a consumer reads them; a tester or QA engineer wants the verification algorithm and the security rules, because those are the parts that can be run as a check.
The field-by-field parts are marked as such, and a designer can skim them.

#### How to read the requirements quoted in this section

The specification uses capitalised *MUST*, *MUST NOT*, *SHOULD*, *MAY* and their relatives in the sense RFC 2119 gives them, and clause 4.1 sets out the force of each: *MUST* is an absolute requirement, *SHOULD* is a strong expectation that a departing party has to justify and owns the consequences of, and *MAY* is genuinely optional, so a consumer cannot assume the optional behaviour is present.
Clause 4.1 also settles a question a reader will otherwise ask: the same words in lower case, in the specification's informative clauses, carry no requirement at all.

This guide is informative and does not issue requirements in its own voice.
Where something is required, the sentence says that the specification requires it and names the clause, so you can read the normative text for yourself.

Two roles carry the obligations, and clause 4.2 defines them.
A producer is any tool or person that creates a package.
A consumer is any tool or person that reads a package and relies on its contents.
A single tool may be both, and clause 4.2 requires that when it is, it satisfies both sets of obligations independently.
An adapter is always both, which is the reason Part IV gives adapters a clause of their own.

#### Why the facts travel as one file

A design system that arrives as a directory to be assembled arrives differently for each recipient.
Files go missing in transfer, relationships between artefacts become ambiguous once a folder has been copied twice, integrity is hard to check, and a consumer cannot reliably tell which folder or which revision was meant to be the complete system.
The Part IV preamble puts the consequence plainly: a contract that is reassembled is a contract that can be reassembled wrongly.

So a package is a single file, and everything in clauses 25 to 33 follows from wanting one file that a consumer can verify before trusting a word of its contents.
The container is a ZIP archive with the `.afds` extension, because ZIP is widely supported, cross-platform, compressible, and inspectable with ordinary tools, and because it keeps several specialised representations together without pretending they are one format.

The costs are worth stating before anyone adopts this.
A package is less convenient for line-by-line collaboration than a live repository, and editing one artefact means unpacking or using package-aware tooling.
An inventory of digests proves that bytes did not change; it proves nothing about who produced them, which clause 32.3 states in terms.
And an archive from somewhere else is an attack surface, which is why clause 32 exists at all.

Part IV also declines to do two things on purpose: it defines no signature format, for the reason clause 32.3 gives, and it defines no adapter for any particular external target, because the moment one adapter is canonical the format has a preferred toolchain and the portability claim is weaker than it looks.

#### The container rules

Clause 25.1 states ten container requirements, and every row of the table below is a *MUST* in that clause.
The wording here is indicative for readability; the normative wording is at clause 25.1.

| Requirement | What a conforming package does (clause 25.1) |
| --- | --- |
| ZIP syntax | Uses ZIP syntax, and is readable by an ordinary ZIP reader |
| Extension | Uses the `.afds` extension |
| No enclosing directory | Does not wrap its contents in a single enclosing top-level directory; `afds-manifest.json` sits at the archive root |
| Root manifest | Includes an entry named exactly `afds-manifest.json` at the archive root |
| Root inventory | Includes an entry named exactly `afds-inventory.json` at the archive root |
| Normalised relative paths | Gives every entry a normalised relative path using `/` as the separator |
| No absolute paths | Has no entry path beginning with `/`, and none containing a drive letter or UNC prefix |
| No traversal | Has no entry path containing a `..` segment or a `.` segment |
| UTF-8 text | Stores text content as UTF-8, and emits no byte-order mark |
| No encryption | Contains no encrypted entries when it is intended for portable interchange |

Clause 25.2 explains four of these, and each note is operational rather than decorative.

The no-enclosing-directory rule exists so that a consumer can find the manifest without guessing.
Many archive tools add a wrapper directory by default, and clause 25.2 requires a producer to check its output rather than trusting the tool — the single most common way a first package fails.

The path restrictions are there for security as much as tidiness, and clause 32 names the attack.
Clause 25.2 requires a consumer to reject a non-conforming path rather than sanitising it, because sanitising silently changes what the package says.

The encryption prohibition applies to portable interchange, which is the only case Part IV specifies.
Clause 25.2 permits a producer to encrypt a package for private transfer by wrapping the conforming `.afds` file in some other envelope, and requires that the `.afds` file inside that envelope is itself unencrypted.

Directory entries are permitted but carry no meaning.
Clause 25.2 states that a consumer "*MUST NOT* rely on the presence of an explicit directory entry, and a producer *SHOULD* omit them", and that directory entries "*MUST NOT* appear in the inventory, because they have no content to digest".
That last rule is what makes the entry arithmetic later in this section come out: an archive's entry count and its inventory's record count differ by exactly one, the inventory itself, and not by however many folder markers the packing tool decided to write.

#### Identifying a package on the wire

The underlying registered media type is `application/zip`, and clause 26 says so.
AFDS has no dedicated IANA media-type registration, and obtaining one is recorded as an open question in the project open-questions register.

The operative half of clause 26 is a prohibition that is easy to miss.
A consumer is required not to rely on a media type of `application/afds+zip` or similar being present, because no such type is registered.
Clause 26 instead recommends that a consumer identify a package by opening it and finding a parseable root manifest whose `afdsFormat` field is `afds-package`.
A producer may advertise `application/afds+zip` in a private context where both ends agree, and clause 26 requires that it not treat that as a registered type.

For a tester, that turns into a concrete check: identification by extension or served type is a smell, and identification by opening the file and reading `afdsFormat` is what the specification asks for.

#### What the container borrows from the Open Packaging Conventions

The obvious question about a ZIP-based container is why AFDS did not reuse one that already exists.
Annex A answers it, and Annex A is informative, so nothing in it is a requirement.

Open Packaging Conventions, standardised as ECMA-376 Part 2 and ISO/IEC 29500-2, is a formal ZIP-based multi-part container.
An OPC package holds *parts*, each with a name and a content type; content types are declared in a `[Content_Types].xml` part at the package root; and relationships between parts are declared in separate XML relationship parts under `_rels` directories, so that a consumer discovers the structure by walking relationships from a package-level root rather than by convention.
OOXML uses that machinery to collect the many related parts of one document into a single logical file, and other formats reuse it: Annex A notes that ECMA-388 states the OpenXPS format requirements "are an extension of the packaging requirements described in the Open Packaging Conventions (OPC) Standard".

Annex A summarises the position in one sentence: "AFDS borrows the principle and rejects the machinery."

What it borrows, at A.1, is the principle that a package is one logical object made of related parts: a consumer receives one file, can identify it, and can enumerate its contents without hunting through a folder tree.
A.1 credits OPC with demonstrating that a ZIP archive is a sound basis for exactly that.

What it rejects, at A.2, is the rest.

| OPC mechanism | AFDS position (A.2) | Reason given |
| --- | --- | --- |
| XML parts as the content model | Rejected | AFDS content is JSON and Markdown centred, and wrapping JSON in XML parts adds a representation nobody needs |
| `[Content_Types].xml` | Rejected | The inventory already carries a media type per entry, in the same file that carries the digest |
| `_rels` relationship parts | Rejected | The manifest already supplies the relationship map, in one place, in the format the rest of the package uses |
| Part-naming grammar | Rejected | Normalised relative ZIP paths are sufficient and are what ordinary tools already show |
| Relationship-walking discovery | Rejected | A consumer reads two known root files, and discovery by convention is simpler and easier to verify |
| Single logical object made of related parts | Adopted | This is the principle worth keeping |

A.2 also states the cost rather than hiding it.
AFDS gains no benefit from existing OPC tooling, and a developer who already knows OPC has to learn a second set of conventions.
The judgement recorded there is that OPC's XML parts and relationship model add complexity without improving a JSON and Markdown centred representation, and that a manifest a person can read in a text editor is worth more to this project than reuse of an XML relationship library.

If you have met OPC before, the two root files are the mapping to hold on to: `afds-inventory.json` does the work of `[Content_Types].xml` and adds digests, and `afds-manifest.json` does the work of `_rels` and adds identity, licensing and profile claims.

#### What is in a package

A package declares a fixed hierarchy, so that a consumer knows where each kind of artefact lives without consulting a directory listing (clause 27).
The full hierarchy is below.
Nothing in it is a suggestion: clause 27.2 attaches a requirement level to every path, and clause 27.3 states what a producer may not do with it.

```text
package root
├── afds-manifest.json        REQUIRED  what the package is, and where its canonical sources are
├── afds-inventory.json       REQUIRED  what the package contains, byte for byte
├── LICENSES.md               RECOMMENDED  licence summary (the only other file the spec defines at root)
├── tokens/                   REQUIRED in every profile
├── components/               REQUIRED in the components and full profiles
│   └── <component>/                    one subdirectory per component: contract plus prose specification
├── patterns/                 OPTIONAL   multi-component flow documentation, and the reserved registry.json
├── manifests/                OPTIONAL   generated interface manifests, for example a Custom Elements Manifest
├── evidence/                 REQUIRED in the full profile
├── adapters/                 OPTIONAL
│   └── <target>/                       declaration, transform report, and for an export adapter its output
├── docs/                     RECOMMENDED  human-readable package documentation
├── schemas/                  OPTIONAL   JSON Schema documents for the package's own machine-readable artefacts
└── stories/                  OPTIONAL   executable examples and test fixtures
```

Two facts about that tree are worth saying out loud, because a reader skimming a folder listing will not infer them.

At the archive root sit exactly two required files (clause 27.1): `afds-manifest.json`, which states what the package is and where its canonical sources are, and `afds-inventory.json`, which states what the package contains, byte for byte.
Beneath the root sit up to nine directories, and clause 27.1 names all nine: `tokens/`, `components/`, `patterns/`, `manifests/`, `evidence/`, `adapters/`, `docs/`, `schemas/`, `stories/`.

A licence summary, `LICENSES.md`, may sit at the root (clause 27.1).
No other root-level file is defined by the specification, and clause 27.1 says a producer "*SHOULD NOT* add one".
That is a *SHOULD NOT* rather than a *MUST NOT*, so adding a root-level `README.md` is a departure you have to be able to justify rather than an automatic failure.

The requirement level of each path, from the clause 27.2 table:

| Path | Kind | Required | Contents |
| --- | --- | --- | --- |
| `afds-manifest.json` | File | *REQUIRED* | Package identity, version, licences, profile, and canonical source declarations |
| `afds-inventory.json` | File | *REQUIRED* | One record per package entry except itself, with length, media type, role, and digest |
| `tokens/` | Directory | *REQUIRED* in every profile | Design-token files validating against the declared Design Tokens Format Module version |
| `components/` | Directory | *REQUIRED* in the components and full profiles | One subdirectory per component |
| `patterns/` | Directory | *OPTIONAL* | Multi-component flow and guidance documentation |
| `manifests/` | Directory | *OPTIONAL* | Generated interface manifests, for example a Custom Elements Manifest |
| `evidence/` | Directory | *REQUIRED* in the full profile | Engine-qualified evidence records and known-limitations prose |
| `adapters/` | Directory | *OPTIONAL* | Adapter declarations, transform reports, and export output |
| `docs/` | Directory | *RECOMMENDED* | Human-readable package documentation |
| `schemas/` | Directory | *OPTIONAL* | JSON Schema documents for the package's machine-readable artefacts |
| `stories/` | Directory | *OPTIONAL* | Executable examples and test fixtures |
| `LICENSES.md` | File | *RECOMMENDED* | Human-readable statement of the licensing arrangement |

The per-profile entries in that column are the only place the hierarchy depends on which completeness profile a package declares.
The profiles themselves, and what each requires, are at clause 34 and are covered elsewhere in this guide.

Clause 27.3 adds three prohibitions and one habit.

A producer may not place a canonical token file outside `tokens/`, may not place a component contract outside `components/`, and may not place adapter output or a transform report outside `adapters/` (clause 27.3).
Each of those is a separate *MUST NOT*, and together they are what allow a consumer to find a kind of artefact without a search.

The habit concerns absence.
An empty optional directory carries no information, so clause 27.3 asks a producer to omit an optional directory rather than shipping it empty, and requires it to "declare the absence in the manifest where the manifest has a corresponding field".
That qualifier matters and is easy to drop: `manifests/` and `docs/` have no corresponding manifest field, so there is nothing to declare for them.
Where a field does exist, clause 27.3 states that an empty array in the manifest is a positive declaration of absence and is preferable to omitting the field.

The distinction is the same one the whole format keeps making: an empty array says somebody considered the question and answered it, and a missing field says nothing at all.

#### Who owns a fact: the artefact roles

Every inventoried entry has exactly one role, and clause 28 gives the role a job: it records who owns the fact the entry carries.
That is the mechanism which keeps the accessibility contract portable rather than leaking into a build output.

Clause 28.1 is headed "The six roles" and defines six.

| Role | Meaning (clause 28.1) |
| --- | --- |
| `canonical` | The authoritative source of the facts it carries. Nothing else in the package may contradict it. |
| `derived` | Generated from one or more canonical artefacts and reproducible from them. |
| `adapter` | Produced by an adapter for a specific external target, and shaped by that target's limits. |
| `evidence` | A record of observation: what was tested, on which engine and assistive technology, on what date, with what result. |
| `documentation` | Human-readable prose explaining canonical artefacts. Explanatory, not authoritative. |
| `schema` | A machine-readable schema that other artefacts in the package validate against. |

Six is the number clause 28.1 gives, and the identifiers are exactly those six lower-case strings.

##### The ownership rule

Clause 28.2 states the rule in one line: a `derived` or `adapter` artefact must not be the only source of a fact owned by a `canonical` artefact.

The rest of the clause is what "owned" means in practice.
A token value is owned by the canonical token file.
A component's semantic model, derivation, keyboard contract, Reflow behaviour, WCAG mapping, guarantees, non-guarantees, assertions, and uncertainty are owned by the canonical component contract — nine things, and clause 28.2 lists all nine.
An observation of assistive-technology behaviour is owned by an evidence record.

A guarantee's substantiation status is owned by neither.
Clause 28.2 states that it "is computed from the two together and *MUST NOT* be written into either, as clause 14.3 requires".
This is a rule a producer breaks by being helpful: caching a computed `substantiated` flag into a contract, or into an evidence record, is prohibited, because the cached value can then disagree with the two artefacts it was computed from.

The reason the rule exists is stated as a failure mode rather than a principle.
If a fact exists only in a generated stylesheet, a design-tool library, or a platform resource bundle, the fact has left the portable bundle, and at that point the package no longer carries the accessibility contract — which clause 28.2 calls "the exact failure the format exists to prevent".

Two consequences are testable, which is why a QA engineer should care about this clause.

The first is that any `derived` or `adapter` artefact must be regenerable from the canonical artefacts in the same package alone (clause 28.2).
If regeneration loses a fact, the fact was only in the derived artefact, and clause 28.2 says the package does not conform.
Clause 33.4 states the single exception, which is an import report.

The second is that a consumer may discard every `derived` and `adapter` entry and still hold a complete design system (clause 28.2).
That is hard to check directly, so clause 28.2 offers an approximation a verifier can implement: confirm that no `canonical` artefact references a `derived` or `adapter` path as its source.
It is the only mechanisable form of the ownership rule, and it is worth building.

##### Documentation is not authoritative

A `documentation` artefact explains a canonical artefact, and clause 28.3 requires that it introduce no normative fact of its own.
Where prose and contract disagree, clause 28.3 states that the contract wins and the prose is a defect to be corrected.

The clause explains why it needed saying: a reader naturally trusts the readable file over the machine-readable one, and in this format that instinct is wrong.
The worked example at the end of this section contains a live instance of exactly this, in a package that is otherwise careful.

#### The manifest, field by field

This subsection is a schema definition.
A designer can read the first three paragraphs and skip the tables; a producer implementer needs all of them.

The manifest states what the package is, who may use it and under what terms, which profile it claims, and where every canonical source lives (clause 29).
Clause 29.1 sets out the fields, shows nesting with dotted paths, and states the reading rule: "A field marked *REQUIRED* *MUST* be present; a field marked *OPTIONAL* *MAY* be omitted, and a consumer *MUST NOT* infer a default beyond the one stated."

There is no implicit default anywhere in this table: if a field is absent and no default is stated, a consumer does not get to guess one.

Clause 29.1 defines twenty-six fields, of which eighteen are required.
Two of those eighteen are required only in particular completeness profiles, and are marked as such below.

| Field | Type | Required | What it carries | Clause |
| --- | --- | --- | --- | --- |
| `afdsFormat` | String | *REQUIRED* | Format identifier; must be the exact string `afds-package` | 29.1 |
| `afdsVersion` | String | *REQUIRED* | Version of the package format, as semantic versioning; `1.0.0` for this specification | 29.1, 35 |
| `packageId` | String | *REQUIRED* | Stable identifier, unique within the publisher's namespace; reverse-DNS form is *RECOMMENDED* | 29.1 |
| `packageVersion` | String | *REQUIRED* | Semantic version of the package payload, independent of `afdsVersion` | 29.1, 35 |
| `title` | String | *REQUIRED* | Human-readable package title | 29.1 |
| `description` | String | *REQUIRED* | Prose description of what the package contains and is for | 29.1 |
| `created` | String | *REQUIRED* | Creation date of this package version, as an ISO 8601 date | 29.1 |
| `conformanceProfile` | String | *REQUIRED* | The declared completeness profile identifier from clause 34, and nothing else | 29.1, 34 |
| `methodProfiles` | Array of strings | *REQUIRED*, may be empty | Method profile identifiers claimed; an empty array declares that no method is claimed | 29.1, 20.2 |
| `targetConformanceLevel` | String | *REQUIRED* | Default target WCAG level, one of `A`, `AA`, `AAA`; not inferable from any other field | 29.1, 12.4 |
| `licences.code` | String | *REQUIRED* | SPDX identifier for code and machine-readable artefacts | 29.1 |
| `licences.documentation` | String | *REQUIRED* | SPDX identifier for prose | 29.1 |
| `publisher.name` | String | *REQUIRED* | Name of the person or organisation publishing the package | 29.1 |
| `publisher.project` | String | *OPTIONAL* | Project the package belongs to | 29.1 |
| `publisher.uri` | String | *OPTIONAL* | Publisher URI; informational only, and it proves nothing about provenance | 29.1 |
| `tokens.dtcgVersion` | String | *REQUIRED* | Version of the Design Tokens Format Module the token files validate against | 29.1 |
| `tokens.canonicalSources` | Array of source objects | *REQUIRED* | Canonical token files; at least one entry in every profile | 29.1 |
| `components.canonicalSources` | Array of component objects | *REQUIRED* in the components and full profiles | Canonical component declarations | 29.1 |
| `patterns.canonicalSources` | Array of source objects | *OPTIONAL* | Canonical pattern documentation, and the registry where clause 29.4 requires one; an empty array declares absence | 29.1, 29.4 |
| `localProfiles` | Array of local profile objects | *OPTIONAL* | Method profiles defined by this package rather than by Part III | 29.1, 29.3 |
| `evidence.canonicalSources` | Array of source objects | *REQUIRED* in the full profile | Canonical evidence records | 29.1 |
| `schemas.canonicalSources` | Array of source objects | *OPTIONAL* | Schema documents shipped in the package | 29.1 |
| `documentation.sources` | Array of source objects | *OPTIONAL* | Documentation artefacts worth enumerating | 29.1 |
| `adapters` | Array of adapter objects | *REQUIRED* | Declared adapters; an empty array declares that the package ships none | 29.1, 33.5 |
| `stories` | Array of source objects | *OPTIONAL* | Executable examples and fixtures | 29.1 |
| `notes` | Array of strings | *OPTIONAL* | Statements a consumer should read before relying on the package | 29.1 |

Note the shape of `adapters`: it is required even in a package that ships no adapter at all, and the empty array is the declaration, which is clause 27.3's positive-declaration rule showing up as a required field.

A **source object** appears wherever the manifest points at a single artefact (clause 29.1).

| Field | Type | Required | What it carries |
| --- | --- | --- | --- |
| `id` | String | *REQUIRED* | Identifier unique within its array |
| `path` | String | *REQUIRED* | Package-relative path to the artefact; it must appear in the inventory |
| `role` | String | *REQUIRED* | One of the six roles in clause 28 |
| `description` | String | *RECOMMENDED* | What the artefact carries |

The `path` rule is a cross-check between the two root files: a source object naming a path that no inventory record covers makes the package non-conforming (clause 29.1).

A **component object** replaces `path` with two paths, because clause 29.1 takes it as given that a component always has both a contract and a prose specification.

| Field | Type | Required | What it carries |
| --- | --- | --- | --- |
| `id` | String | *REQUIRED* | Stable component identifier |
| `name` | String | *REQUIRED* | Human-readable component name |
| `kind` | String | *REQUIRED* | Component kind, for example `layout-primitive` or `interactive-component` |
| `specification` | String | *REQUIRED* | Path to the component specification |
| `documentation` | String | *REQUIRED* | Path to the component documentation |
| `role` | String | *REQUIRED* | Must be `canonical` |

That last row is not decoration: a component object declaring any other role is non-conforming, because a component contract is by definition the authoritative source of the facts it carries (clauses 29.1, 28.2).

An **adapter object** is specified at clause 33.5, and is set out later in this section.

##### Where a conformance claim actually lives

Clause 4.4 requires a conformance claim to state three things: "the format version, the completeness profile, and the set of method profiles claimed, which *MAY* be empty".
All three travel in the manifest, and it is worth knowing which field carries which, because the three are routinely confused.

| Part of the claim (clause 4.4) | Manifest field | Notes |
| --- | --- | --- |
| Format version | `afdsVersion` | The version of the package format, not of the design system |
| Completeness profile | `conformanceProfile` | Exactly one identifier from clause 34; clause 29.1 states that "the value it carries is a completeness profile and nothing else" |
| Method profiles claimed | `methodProfiles` | An array, possibly empty; an empty array is a claim of no method, not an omission |

A fourth field is often mistaken for part of the claim and is not.
`targetConformanceLevel` states the WCAG level the package targets by default (clause 12.4), and clause 29.1 says in terms that it is "not inferable from any other field".
Clause 4.5 requires the completeness axis and the method axis to be declared separately and prohibits a consumer from inferring either from the other, and clause 34 extends the same independence to the target level.
The completeness profiles themselves are covered at clause 34, elsewhere in this guide.

Clause 4.4 also states two prohibitions about how a claim may be worded, and they belong with the manifest because the manifest is where a claim becomes machine-readable.
A claim may not be expressed as conformance to an informative document or to a guide that has no conformance model; in particular, clause 4.4 states that a package "*MUST NOT* claim that a component conforms to the ARIA Authoring Practices Guide, because that guide is informative and has no conformance model to conform to".
What a package may publish about a component is the accessibility criteria met, the semantics used, and the recorded assistive-technology results.
And a conformance claim is a claim about a package, not about a service built from it: clause 4.4 prohibits a producer from presenting one as evidence that an assembled service is accessible.

##### Declaring a method profile the specification does not define

Clause 20.4 defines four method profiles and permits an organisation to define its own, requiring a local identifier to be namespaced with a prefix that is not `afds-`.
Clause 29.3 says how such a profile travels.

A package that lists an identifier in `methodProfiles` which is not defined in clause 20.4 is required to declare that profile in a `localProfiles` array (clause 29.3).
The reverse is prohibited in two directions: a `localProfiles` entry may not use an identifier defined in clause 20.4, because a package cannot redefine a profile the specification defines, and a package may not supply a provenance object for a specification-defined profile either (clause 29.3).

A **local profile object** has five fields (clause 29.3).

| Field | Type | Required | What it carries |
| --- | --- | --- | --- |
| `id` | String | *REQUIRED* | Profile identifier; must not begin with `afds-` |
| `title` | String | *REQUIRED* | Human-readable profile name |
| `statement` | String | *REQUIRED* | The profile's statement, as clause 20.1 requires of every profile |
| `specification` | String | *OPTIONAL* | Package-relative path to the profile's full text; where present it must appear in the inventory |
| `provenance` | Provenance object | *REQUIRED* | The profile's provenance, per clauses 20.6 and 29.3.1 |

The provenance object is where a local profile says what it took from elsewhere and what it invented.
Clause 29.3.1 fixes its serialised form: four members, of which three are required arrays.

| Member | Type | Required | Content |
| --- | --- | --- | --- |
| `adopted` | Array of adopted entries | *REQUIRED*, may be empty | What the profile takes from work outside the package |
| `changed` | Array of changed entries | *REQUIRED*, may be empty | What the profile alters about an adopted idea |
| `originates` | Array of originates entries | *REQUIRED*, must not be empty | What the profile asserts on its own authority |
| `statement` | String | *OPTIONAL* | Prose accompanying the structured members |

`originates` is the one that cannot be empty (clause 29.3.1): a profile that adopts everything and originates nothing is not a profile, it is a citation.

An **adopted entry** carries `id`, `what`, `source.author`, `source.title`, and `source.uri` where one exists, with everything but the URI required unconditionally (clause 29.3.1).
A **changed entry** carries `adoptedRef`, which must match an `id` in the same `adopted` array, `what`, and `direction`, which is one of `stricter`, `weaker`, or `different` (clause 29.3.1).
An **originates entry** carries `what` and `appliesTo`, both required (clause 29.3.1).

Four checks are mechanical, and clause 29.3.1 permits a verifier to run them: every `adoptedRef` resolves within the same `adopted` array, every `direction` is one of the three permitted values, `originates` is not empty, and every adopted entry carries an author and a title.

Then comes the sentence a tool author has to respect.
Clause 29.3.1 states that no check establishes that an attribution is truthful, and that "a tool *MUST NOT* report a passing structural check as a verified provenance".
Clause 20.5 makes attributing a requirement to a source that does not support it a conformance failure, and detecting that failure requires reading the source.
A green tick on a provenance object means the shape is right, not that the citation is honest, and a report implying otherwise is itself a defect.

##### The reserved pattern-registry path

Clause 24.2 requires a package claiming `afds-patterns-native-first` to carry a package-level registry of component and pattern statuses.
Clause 29.4 binds it to a path.

A package claiming that profile is required to carry the registry at `patterns/registry.json`, to declare it in `patterns.canonicalSources` with role `canonical`, and to include it in the inventory (clause 29.4).
The path is reserved: clause 29.4 prohibits using `patterns/registry.json` for anything other than a registry satisfying clause 24.2, whether or not the package claims the profile.

The registry is `canonical` rather than `derived` even though its component entries restate a fact each component contract already carries.
Clause 29.4 gives the reason, and it is the same honesty argument that runs through the format: the registry's prohibition entries record a pattern the package has declined, and no component contract can supply that, "because a decision not to build something leaves no component behind to declare it".

#### The inventory, field by field

The inventory is what makes a package verifiable (clause 30).
It lists every entry with enough information to detect any change between production and consumption.

Clause 30.1 states what it covers: exactly one record for every entry in the archive, with one exception, which is that it must not contain a record for itself.
That exclusion is necessary rather than stylistic, because a record of the inventory inside the inventory could never hold a correct digest — writing the digest would change the bytes it describes.
Directory entries are also excluded, as clause 25.2 states, because they have no content.

Clause 30.1 then places an obligation on the reader of a package, not its writer.
A consumer is required to verify the inventory before relying on any package content, and the clause spells out what that means: "before parsing a token file, before reading a component contract, and before extracting anything to disk".
This is not an affordance a consumer may take up if convenient; parsing a token file first and verifying afterwards does not conform.

Ten top-level fields, from clause 30.2.

| Field | Type | Required | What it carries |
| --- | --- | --- | --- |
| `afdsFormat` | String | *REQUIRED* | Must be the exact string `afds-inventory` |
| `afdsVersion` | String | *REQUIRED* | Package-format version, matching the manifest |
| `packageId` | String | *REQUIRED* | Must match the manifest's `packageId` |
| `packageVersion` | String | *REQUIRED* | Must match the manifest's `packageVersion` |
| `digestAlgorithm` | String | *REQUIRED* | Must be the exact string `SHA-256` |
| `digestEncoding` | String | *REQUIRED* | Must be the exact string `lowercase-hex` |
| `excludesSelf` | Boolean | *REQUIRED* | Must be `true`, stating explicitly that the inventory omits itself |
| `entryCount` | Number | *REQUIRED* | Number of records; must equal the length of `records` |
| `description` | String | *RECOMMENDED* | Prose statement of what the inventory does and does not prove |
| `records` | Array of record objects | *REQUIRED* | One record per inventoried entry |

These are obligations on the producer, not merely things a verifier happens to look at, and four of them are fixed strings or a fixed boolean, which makes them the cheapest possible check on whether a file is an AFDS inventory at all.

Each **record object** has five required fields (clause 30.2).

| Field | Type | Required | What it carries |
| --- | --- | --- | --- |
| `path` | String | *REQUIRED* | Package-relative normalised path of the entry |
| `mediaType` | String | *REQUIRED* | Media type of the entry's content, including a charset parameter for text |
| `byteLength` | Number | *REQUIRED* | Exact uncompressed length of the entry in bytes |
| `role` | String | *REQUIRED* | One of the six roles in clause 28 |
| `sha256` | String | *REQUIRED* | SHA-256 digest of the entry's exact uncompressed bytes, as lowercase hexadecimal |

Clause 30.2 asks that records be sorted by `path` in ascending byte order, as a *SHOULD*, and gives review convenience as the reason: a rebuilt inventory then produces a diff showing only genuine changes rather than a reshuffle.

One rule about digest format is easy to skip and expensive to get wrong.
Clause 30.3 states that a `sha256` value "*MUST* be the full 64 lowercase hexadecimal characters, and a consumer *MUST* reject a truncated, uppercase, or base-64 digest rather than attempting to interpret it".
A consumer that upper-cases and compares is being helpful in a way the specification prohibits, because a package whose digests are the wrong shape is not a package whose integrity has been established.

#### Verifying a package, step by step

Clause 31 gives the procedure a conforming consumer implements, in ten numbered steps.
The order is not editorial.
Clause 31 states that the steps are ordered "so that a cheap check never runs after an expensive one it could have prevented, and so that nothing is parsed before the container is known to be safe".
Implement them in this order, and number your report against these numbers, so that a producer reading a failure can find the clause.

1. **Open as ZIP.**
   Open the file using ZIP syntax.
   If it is not a readable ZIP archive, report a container failure and stop.
2. **Check paths.**
   For every entry, confirm the path is a normalised relative path, contains no `..` or `.` segment, does not begin with `/`, and carries no drive letter or UNC prefix.
   Confirm no single enclosing top-level directory wraps the contents.
   Report each violation and stop, and do not sanitise.
3. **Check encryption and limits.**
   Confirm no entry is encrypted.
   Apply the configured limits from clause 32 for entry count, total compressed size, total uncompressed size, per-entry decompression ratio, nesting depth, and path length.
   Report each violation and stop.
4. **Locate and parse the manifest.**
   Confirm `afds-manifest.json` exists at the archive root, decode it as UTF-8, parse it as JSON, and confirm `afdsFormat` is `afds-package`.
   Read `afdsVersion` and apply the version rules in clause 35.
5. **Locate and parse the inventory.**
   Confirm `afds-inventory.json` exists at the archive root, decode it as UTF-8, and parse it as JSON.
   Confirm `afdsFormat` is `afds-inventory`, `digestAlgorithm` is `SHA-256`, `digestEncoding` is `lowercase-hex`, and `excludesSelf` is `true`.
   Confirm `packageId` and `packageVersion` match the manifest.
6. **Confirm completeness in both directions.**
   Confirm that every archive entry other than the inventory itself and other than directory entries has exactly one inventory record, and that every inventory record names an entry that exists.
   Confirm the inventory holds no record for itself.
   Confirm `entryCount` equals the number of records.
   Report every unmatched name in both directions.
7. **Compare byte lengths.**
   For each record, compare the entry's uncompressed length with `byteLength`.
   Report every mismatch.
8. **Recompute and compare digests.**
   For each record, compute the SHA-256 digest of the entry's exact uncompressed bytes and compare it with `sha256` as lowercase hexadecimal.
   Report every mismatch.
   Clause 31 states that if any digest fails, the consumer "*MUST NOT* rely on any package content".
9. **Validate token files.**
   For each canonical token source named in the manifest, decode it as UTF-8, parse it as JSON, and validate it against the Design Tokens Format Module version declared in `tokens.dtcgVersion`.
   Report every validation failure.
   A consumer that cannot validate against the declared version is required to report that it did not validate, rather than passing the step silently.
10. **Report.**
    Emit a single report giving a pass or fail verdict, the count of entries checked, and every individual problem found.
    Clause 31 requires that a consumer "*MUST NOT* report a pass when any step failed, and *MUST* distinguish 'checked and passed' from 'not checked'".

Step 4 is the one most often written short: reading `afdsVersion` is half of it, and applying the clause 35 version rules is the other half, which decides whether the package may be processed at all.
Clause 35 is covered elsewhere in this guide.

Clause 31 names two properties of the procedure as deliberate, and both are worth preserving in an implementation.

Steps 2 and 3 run before anything is parsed or extracted, so a hostile archive is rejected before its content is touched.
Steps 6 to 9 gather all problems rather than stopping at the first, because a partial report causes a producer to fix one defect at a time.

Step 9 deserves a second look from a tester, because it is the only step whose honest outcome may be "I did not check this": a consumer with no validator for the declared Design Tokens Format Module version cannot pass it quietly, which is the same distinction step 10 requires the report to carry throughout.

#### Security requirements

A package arrives from somewhere else, so clause 32 treats it as untrusted input.
There are three concerns and they are separable.

##### Path traversal

A ZIP archive stores a path for each entry, and clause 32.1 notes that nothing in ZIP syntax prevents that path being absolute or containing `..` segments.
A naive extractor that joins the entry path onto an output directory can therefore be made to write outside that directory, overwriting arbitrary files.

Clause 32.1 states three requirements, and each is separate.
A consumer is required to reject any entry whose path is absolute, contains a `..` or `.` segment, or is not normalised.
A consumer is required to perform this check before extracting anything.
And a consumer is prohibited from rewriting an offending path into a safe one, "because that silently changes what the package says and hides the attack".

The third is the one a developer argues with: sanitising feels like defence, and clause 32.1 treats it as concealment.

##### Decompression limits

A small archive can expand to an enormous volume of data, exhausting memory or disk, and clause 32.2 notes that nesting archives inside archives multiplies the effect.

Clause 32.2 requires a consumer to enforce configured limits and to fail rather than continuing when a limit is reached.
Six limits are named, with suggested defaults.

| Limit | Purpose | Suggested default (clause 32.2) |
| --- | --- | --- |
| Entry count | Bound the number of records and file handles | 5000 entries |
| Total compressed size | Bound the input read | 32 MiB |
| Total uncompressed size | Bound memory and disk consumption | 256 MiB |
| Per-entry decompression ratio | Detect a single highly compressible entry | 200 to 1 |
| Nesting depth | Bound path recursion and nested archives | 16 path segments |
| Path length | Bound filesystem interaction | 255 characters |

Clause 32.2 says the defaults are suggestions, not requirements.
What is required is the mechanism around them: a consumer is required to make its limits configurable and to report which limit was exceeded, "so that a legitimately large package can be handled by raising a named limit rather than by disabling the checks".

There is also an ordering expectation.
Clause 32.2 states that a consumer "*SHOULD* compute the uncompressed total from the archive's own metadata first and reject an over-large package before decompressing anything, then enforce the same limit again during decompression, because the declared metadata may lie" — two passes, because the first is cheap and the second is the one that cannot be fooled.

##### Integrity is not authenticity

Inventory integrity is not a digital signature, and clause 32.3 is unusually direct about it.

SHA-256 digests detect that content changed between the moment the inventory was written and the moment it was verified.
Clause 32.3 grants that this is genuinely useful, because it catches truncated downloads, corrupted media, accidental edits, and careless repackaging.

What it does not do is enumerated, and clause 32.3 states that "a consumer *MUST NOT* claim otherwise".

| Property | Provided by the inventory? (clause 32.3) |
| --- | --- |
| Detects accidental or in-transit change | Yes |
| Detects a change made after the inventory was written | Yes |
| Identifies who produced the package | No |
| Proves the package came from the claimed publisher | No |
| Prevents an attacker rewriting content and rebuilding the inventory | No |
| Establishes a chain of custody | No |

The reason is arithmetic rather than cryptographic.
An attacker who can alter the content can also recompute the digests and rewrite the inventory, and nothing in the package binds it to a key, so nothing in it can be attributed.
Clause 32.3 draws the conclusion that follows for the manifest: "The `publisher` object in the manifest is a claim, not evidence."

A future signature mechanism is therefore needed for trusted distribution, and the project open-questions register records it as open.
Until such a mechanism exists, clause 32.3 requires that "trust in a package *MUST* come from the channel it arrived on rather than from the package itself".

For anyone writing a verification report, that turns into a wording rule: "integrity verified" is accurate, while "package verified" invites the reader to hear authenticity, which clause 32.3 prohibits claiming.

#### Adapters, and honest transforms

An adapter moves information between the canonical artefacts of a package and the representation an external tool or platform uses (clause 33).
Figma, Penpot, CSS custom properties, native platform resources, and Electron shells are all adapter targets.

An adapter reads a package and writes something, or reads something and drafts a package, so it is a consumer and a producer at once.
Clause 4.2 says so directly — "An adapter is always both, which is why Part IV gives it its own clause" — and requires a tool that is both to satisfy both sets of obligations independently.
That is the sentence to keep in mind through the rest of this subsection: an adapter does not get a relaxed version of either role.

An **export** adapter reads canonical artefacts and writes the representation a target expects.
An **import** adapter reads a target's representation and drafts the artefacts an AFDS package requires.

Both directions are in scope, and clause 33 records why: a format that can only export can be adopted only by a design system that began in it, and no established design system did.
An adopter arrives holding a design-tool library, a token file, a component library, and a good deal of knowledge nobody wrote down.
Leaving import undefined would not stop anyone importing; it would push the work into hand transcription and one-off scripts whose output lands in a package with nothing recording which facts were real and which were guessed.

The two directions do not carry the same obligations, and clause 33 explains the asymmetry.
An export knows the full set of facts it is permitted to state, because it reads artefacts that own them, so its whole problem is what the target refuses to accept.
An import does not know, "because the representation it reads was never obliged to carry an accessibility contract at all".

##### Direction

Clause 33.1 requires each element of the manifest's `adapters` array to declare exactly one `direction`, either `export` or `import`.
A target supported in both directions is required to be declared as two adapters sharing a `target` value (clause 33.1).

The reason clause 33.1 gives is about discharge of obligations: the two directions produce different artefacts and different reports, and a single object describing both would leave a consumer unable to determine which obligations had been discharged.

##### What both directions owe

Clause 33.2 requires an adapter to report its mappings and its warnings, and to report whatever it could not carry.
It prohibits silently flattening meaning.

Silent flattening is the more dangerous behaviour of the two, because the output looks complete.
Clause 33.2 gives three examples, and each is a real limit rather than an illustration: a `ch`-based measure has no direct native analogue, a forced-colours boundary has no equivalent in a target that has no concept of a user-forced colour palette, and a keyboard contract has no representation at all in a token pipeline.
In each case, clause 33.2 says the honest output is a recorded finding, not an approximation presented as an equivalent.

No adapter in either direction may produce an artefact with the role `canonical` (clause 33.2), and the reason is the ownership rule at clause 28.2: an artefact shaped by a target's limits cannot own a fact.

##### Export adapters (clause 33.3)

Clause 33.3 is short and entirely operational.
Export output is required to carry the role `adapter` or `derived`, never `canonical`, is required to be regenerable from the canonical artefacts alone as clause 28.2 requires, and a producer is required to place it under `adapters/<target>/out/`.
That path is a real requirement rather than a convention, and it is the one export rule a producer discovers late, after the output has been written somewhere more convenient.

##### What an import may not do

An import adapter is prohibited from writing an artefact with the role `canonical` (clause 33.4).

The output of an import is a draft, and a draft is not a contract.
Clause 33.4 states that a draft becomes canonical only when a person reviews it, supplies what the source could not, and accepts responsibility for the accessibility claims the artefact then makes.
The specification calls that act **promotion**, and requires that promotion be performed by a person and not by a transform, "because a canonical artefact asserts a contract that somebody has to be willing to defend".

Two consequences follow for what may ship.

Import output is not itself a package artefact, and clause 33.4 prohibits a producer from shipping an unpromoted draft in a conforming package, because once a draft is inside a package it is indistinguishable from a contract to whoever relies on it.

What the package retains from an import is the import report, which is the provenance of every artefact promoted from that import.
Clause 33.4 requires an import report to carry the role `adapter`, and exempts it from the regenerability consequence stated in clause 28.2.
The exemption is narrow and structural: an import reads a source that lies outside the package by definition, so no package can regenerate it.
Clause 33.4 notes that the alternative to the exemption is discarding the provenance of every imported artefact, which is a worse outcome than a stated exception.

Clause 33.4 then closes the gap a reader would otherwise find.
Every `gaps` entry in an import report is required to appear in the promoted artefact as an uncertainty record or as a declared non-guarantee.
An import that could not discover a component's keyboard behaviour has not thereby excused the package from declaring that the keyboard behaviour is unknown.

There is also a rule about how an import runs, not only about what it produces.
Clause 33.4 requires an import to be a discrete run that produces a dated report, and prohibits it from being a live read-through dependency on an external tool's model.
A read-through dependency makes the external tool the effective owner of whatever it supplies, which is the failure clause 28.2 exists to prevent, and it leaves no report a reviewer can examine.

##### The adapter declaration

Each element of the manifest's `adapters` array is an adapter object, and clause 33.5 gives it nine fields.

| Field | Type | Required | What it carries |
| --- | --- | --- | --- |
| `id` | String | *REQUIRED* | Adapter identifier, unique within the package |
| `direction` | String | *REQUIRED* | Either `export` or `import` |
| `target` | String | *REQUIRED* | The external tool or platform, for example `figma` or `css-custom-properties` |
| `adapterVersion` | String | *REQUIRED* | Semantic version of the adapter that produced the output |
| `declaration` | String | *REQUIRED* | Path to the adapter's own declaration file |
| `report` | String | *REQUIRED* | Path to the transform report |
| `inputs` | Array of strings | *REQUIRED* | For `export`, paths of the canonical artefacts consumed; for `import`, identifiers of the external sources read, which are not package paths |
| `outputs` | Array of strings | *REQUIRED* | For `export`, paths of the generated artefacts; for `import`, an empty array, because import output is not a package artefact |
| `promoted` | Array of strings | *REQUIRED* for `import` | Paths of the canonical artefacts promoted from this import, and an empty array where nothing has yet been promoted |

`inputs` and `outputs` are where the two directions stop looking alike.
For an export, both are package paths; for an import, `inputs` are external identifiers that no inventory record will ever match, and `outputs` is empty by rule.
A verifier that checks every `inputs` entry against the inventory will therefore report false failures on import declarations, and clause 33.5 is the clause that says why it should not.

##### The transform report

A transform report records what the adapter did, what it could not do, and what it wants a reader to notice (clause 33.6).
It is where the honesty becomes checkable rather than aspirational.

Eight fields are required in both directions (clause 33.6).

| Field | Type | What it carries |
| --- | --- | --- |
| `adapterId` | String | Identifier of the adapter that produced this report |
| `adapterVersion` | String | Version of the adapter |
| `direction` | String | Either `export` or `import`, matching the adapter declaration |
| `target` | String | The external tool or platform |
| `runDate` | String | ISO 8601 date of the transform run |
| `validationStatus` | String | One of `passed`, `passed-with-warnings`, or `failed` |
| `mappings` | Array of mapping objects | One record per fact carried across |
| `warnings` | Array of finding objects | Facts carried across with a caveat; an empty array if none |

An export report additionally requires two arrays (clause 33.6).

| Field | Type | What it carries |
| --- | --- | --- |
| `losses` | Array of finding objects | Facts the target could not accept; an empty array if none |
| `unsupported` | Array of finding objects | Source features the target has no concept of; an empty array if none |

An import report additionally requires the two that face the other way (clause 33.6).

| Field | Type | What it carries |
| --- | --- | --- |
| `gaps` | Array of finding objects | Facts that an AFDS artefact requires and the source could not supply; an empty array if none |
| `unmapped` | Array of finding objects | Source content for which AFDS has no representation; an empty array if none |

A **mapping object** has `source`, `sourceKind`, `targetName`, and `fidelity`, where `fidelity` is one of `exact`, `approximate`, or `partial` (clause 33.6).
A **finding object** has `source`, `severity`, `statement`, and `consumerAction`, where `severity` is one of `info`, `warning`, or `error` and `consumerAction` says plainly what a person consuming the output must do about it (clause 33.6).

Take the literal token values from those lists.
The status vocabulary is `passed`, `passed-with-warnings`, `failed`, hyphenated as shown, and the severity vocabulary is `info`, `warning`, `error` — not "passed with warnings" and not "information", and an adapter emitting the prose forms emits invalid values.

Every array is required even when empty, and clause 33.6 explains why in terms that generalise beyond adapters.
An empty `losses` array is a positive claim that nothing was lost, which a reviewer can challenge; an omitted `losses` field is merely silence.
The same reasoning applies to `gaps`, where clause 33.6 notes that an empty array claims the source supplied every fact an AFDS artefact requires, "which is a strong claim and rarely a true one".

Two status rules are mechanical.
An export report containing a `losses` or `unsupported` entry with severity `error` is required to set `validationStatus` to `failed` (clause 33.6).
An import report containing a `gaps` entry with severity `error` is required to do the same (clause 33.6).

Clause 33.6 then says something a reader will otherwise misread as a bug.
A `failed` import report is not a malfunction, and for most targets it is the expected result: it states that the source cannot yield a conforming artefact without human authorship, which is information a person needs before deciding how much work an adoption will cost.

##### Round-tripping

An export followed by an import is not a round trip in any sense that returns what was sent.

An export is a projection, and a projection discards.
Running it backwards does not restore what it dropped, because the information is not in the target to be read.
A system exported to a token pipeline and imported back is a system with no keyboard contracts, no evidence, and no non-guarantees, because a token pipeline never held any of those.
Clause 33 states the underlying reason: an import reads a representation that "was never obliged to carry an accessibility contract at all".

The value of a defined import path is not that it makes round-tripping work.
It is that the returned system arrives saying so, in a dated report with a `gaps` array, instead of arriving looking complete (clauses 33.4, 33.6).

What survives is whatever the target's representation can hold — token values, usually, and names.
What does not survive is everything Part II adds: the semantic model, the keyboard contract, the Reflow behaviour, the WCAG mapping, the guarantees and non-guarantees, the assertions, the evidence, and the uncertainty.
Those have to be re-authored by a person, which is what promotion means (clause 33.4).

#### A worked example: the sample package

The repository ships a small complete package at `afds-sample/`, and this subsection walks through it, quoting the files as they stand.
The sample is a real work-in-progress package rather than an idealised one.
Where a point in it is known to depart from the specification, the departure is named in the prose here; the full list is kept as a defects register alongside the repository rather than in this guide, so that this guide stays a description of the specification.

The source tree contains eleven files, of which ten become inventory records.

```text
afds-sample/
├── afds-manifest.json
├── afds-inventory.json          not recorded in itself
├── LICENSES.md
├── adapters/README.md
├── components/stack/stack.md
├── components/stack/stack.spec.json
├── docs/PACKAGE.md
├── evidence/at-matrix.json
├── evidence/known-limitations.md
├── patterns/registry.json
├── tokens/core.tokens.json
├── README.md                    repository-side, excluded from the package
└── tools/build-inventory.py     repository-side, excluded from the package
```

The last two are not package entries: `tools/build-inventory.py` excludes them explicitly, with `EXCLUDED_TOP_LEVEL = {"tools", "README.md"}` and the comment "Repository-side helpers that are not part of the distributable package."
That is consistent with clause 27.1, which defines no root-level file beyond the two required ones and `LICENSES.md`.

It is worth being clear about what kind of rule that is.
The specification says nothing about the directory a package is built from, so nothing in it makes those two files excludable and nothing in it would be violated if they were included.
The boundary is the sample's own, stated in a table in its `README.md` that marks every path in the directory as package content or not, and the verify command checks that table against the package it builds so the two cannot drift apart.
If you publish from a working directory that holds more than the package, the same is true of you: the boundary is yours to draw and yours to write down.
Open question H7 records that the specification is silent on the matter.

##### What the manifest says

The specification reproduces this manifest in full at clause 29.2, generated from the file rather than transcribed so that the example cannot drift from what it describes.
The excerpts below are drawn from the same file and are quoted in the order the fields appear, so you can read either against the field table at clause 29.1.

`afds-manifest.json` opens with the four identity fields and then the three-part claim.

```json
{
  "afdsFormat": "afds-package",
  "afdsVersion": "1.0.0",
  "packageId": "com.a11ybob.abd.afds-sample",
  "packageVersion": "1.0.0",
  "title": "AFDS Sample",
  "description": "A minimal but complete Accessibility Focused Design System package demonstrating the declared hierarchy, canonical source declarations, a DTCG token sample, one layout-primitive component contract, structured assistive-technology evidence, adapter guidance, and dual licensing.",
  "created": "2026-08-29",
  "conformanceProfile": "afds-components",
  "methodProfiles": [
    "afds-patterns-native-first"
  ],
  "targetConformanceLevel": "AA"
}
```

Read those last three lines against clause 4.4: the format version is `1.0.0`, the completeness profile is `afds-components`, and the set of method profiles claimed is `["afds-patterns-native-first"]`.
That is the whole conformance claim, and `targetConformanceLevel` of `AA` is a separate statement made under clause 12.4.
`docs/PACKAGE.md` puts the four together in one sentence: "complete at the component level, claiming the pattern method, not claiming the layout method, targeting Level AA."

The licences and publisher blocks carry the two required SPDX identifiers and the required `publisher.name`, plus both optional publisher fields.

```json
{
  "licences": {
    "code": "GPL-3.0-only",
    "documentation": "CC-BY-SA-4.0"
  },
  "publisher": {
    "name": "Bob Dodd",
    "project": "Accessible by Design",
    "uri": "https://a11ybob.com/"
  }
}
```

The `tokens` block carries the required `dtcgVersion` and one source object with all four of its fields.

```json
{
  "tokens": {
    "dtcgVersion": "2025.10",
    "canonicalSources": [
      {
        "id": "core",
        "path": "tokens/core.tokens.json",
        "role": "canonical",
        "description": "Core spacing, typography, measure, and colour tokens for the sample."
      }
    ]
  }
}
```

`dtcgVersion` is the field that makes step 9 of the verification algorithm possible at all, because a validator otherwise has to guess which version of the token format applies (clauses 29.1, 31).

The `components` block carries one component object, and its `role` is `canonical`, as clause 29.1 requires.

```json
{
  "components": {
    "canonicalSources": [
      {
        "id": "stack",
        "name": "Stack",
        "kind": "layout-primitive",
        "specification": "components/stack/stack.spec.json",
        "documentation": "components/stack/stack.md",
        "role": "canonical"
      }
    ]
  }
}
```

The `patterns` block is where the method-profile claim costs something.
Because the package claims `afds-patterns-native-first`, clause 29.4 requires the registry at `patterns/registry.json`, declared in `patterns.canonicalSources` with role `canonical`, and present in the inventory.
All three hold here.

```json
{
  "patterns": {
    "canonicalSources": [
      {
        "id": "pattern-registry",
        "path": "patterns/registry.json",
        "role": "canonical",
        "description": "Package-level pattern registry required of a package claiming afds-patterns-native-first, at specification clause 24.2. Records the status of every component and every pattern this package has declined."
      }
    ]
  }
}
```

The `evidence` block declares one source, the JSON matrix, with role `evidence`.
The package's known-limitations prose sits in the same directory but is declared in `documentation.sources` with role `documentation`, because clause 28.1 defines `evidence` as a record of observation carrying an engine, an assistive technology, a date, and a result, and narrative prose carries none of those.
The directory and the role are independent: clause 27.2 assigns known-limitations prose to `evidence/`, and the role describes what the artefact is rather than where it sits.
Then the empty declarations, which are the part a reader most often misreads.

```json
{
  "schemas": {
    "canonicalSources": []
  }
}
```

That is an object containing an empty array, not an empty array, whereas `adapters` and `stories` are themselves empty arrays.

```json
{
  "adapters": [],
  "stories": []
}
```

`adapters` is required by clause 29.1 even when a package ships none, and the empty array is the declaration that it ships none.
`stories` is optional, and the empty array is clause 27.3's positive declaration of absence in preference to omitting the field.

The `documentation.sources` array enumerates four prose artefacts, and each carries the `id` that clause 29.1 marks as *REQUIRED* of every source object.

```json
{
  "documentation": {
    "sources": [
      {
        "id": "package-doc",
        "path": "docs/PACKAGE.md",
        "role": "documentation",
        "description": "What this sample package demonstrates."
      },
      {
        "id": "licences-doc",
        "path": "LICENSES.md",
        "role": "documentation",
        "description": "Dual licensing arrangement for code and documentation."
      },
      {
        "id": "adapters-readme",
        "path": "adapters/README.md",
        "role": "documentation",
        "description": "Adapter guidance and the no-adapter-is-canonical rule."
      },
      {
        "id": "known-limitations",
        "path": "evidence/known-limitations.md",
        "role": "documentation",
        "description": "Narrative account of known limitations, non-guarantees, and uncertainty. Explanatory only; the records it discusses are canonical."
      }
    ]
  }
}
```

That `id` field is the one most often left out, because a path already looks like an identifier.
It is not one: a path can change when a file is moved without the artefact changing what it is or what role it plays, which is why clause 29.1 requires an identifier that is stable independently of location and unique within its own array.

The `notes` array closes the file with the three statements the package wants read first.

```json
{
  "notes": [
    "AFDS 1.0.0 is a project draft, not a W3C standard.",
    "Inventory integrity is not a digital signature and does not prove provenance.",
    "No assistive-technology test results in this package are real; every result field is marked not-yet-tested."
  ]
}
```

The second of those is clause 32.3 written into the package itself, which is the right place for it: a consumer that reads only the manifest still learns that the digests prove nothing about provenance.

Two things are absent from the manifest and should be, given what this package is.
There is no `localProfiles` array, because the one profile claimed is defined at clause 20.4 and clause 29.3 prohibits declaring a specification-defined profile locally.
And `afds-layout-intrinsic` is not claimed, even though Stack is built the way that profile describes, because clause 21.4 requires forced-colours evidence and this package has no real evidence at all.
`docs/PACKAGE.md` makes the reasoning explicit: "A profile claim asserting a method the package cannot show it followed would be exactly the kind of unearned claim the format exists to prevent."


##### What the inventory says

`afds-inventory.json` carries all ten top-level fields from clause 30.2, and declares ten records.

```json
{
  "afdsFormat": "afds-inventory",
  "afdsVersion": "1.0.0",
  "packageId": "com.a11ybob.abd.afds-sample",
  "packageVersion": "1.0.0",
  "digestAlgorithm": "SHA-256",
  "digestEncoding": "lowercase-hex",
  "excludesSelf": true,
  "entryCount": 10,
  "description": "Inventory of every entry in this package except this inventory itself. A consumer must verify every record before relying on package content. These digests detect transfer changes; they are not a digital signature and do not identify a signer or prove provenance.",
  "records": []
}
```

The arithmetic is worth doing once, because it is the check most easily got wrong: ten records, plus the inventory itself, which clause 30.1 requires the inventory to omit, gives eleven entries in a packed archive.
`entryCount` is 10 and `records` has length 10, as clause 30.2 requires, and `excludesSelf` is `true`.

The first and last records show the shape, and the digests are the full sixty-four lowercase hexadecimal characters clause 30.3 requires.

```json
{
  "path": "LICENSES.md",
  "mediaType": "text/markdown; charset=utf-8",
  "byteLength": 2180,
  "role": "documentation",
  "sha256": "bedd3036d453487186e2f516a70368969d0c6e75466c85eed9a909e322651e35"
}
```

```json
{
  "path": "tokens/core.tokens.json",
  "mediaType": "application/json",
  "byteLength": 3055,
  "role": "canonical",
  "sha256": "b45bb732e28f4c3f906bb37231442e7051fb2ffe34ef6b57753b29dc68c7a29b"
}
```

The ten records run in ascending byte order by `path`: `LICENSES.md`, `adapters/README.md`, `afds-manifest.json`, `components/stack/stack.md`, `components/stack/stack.spec.json`, `docs/PACKAGE.md`, `evidence/at-matrix.json`, `evidence/known-limitations.md`, `patterns/registry.json`, `tokens/core.tokens.json`.
That satisfies the sorting *SHOULD* at clause 30.2.
Note that `afds-manifest.json` appears in the inventory and `afds-inventory.json` does not, which is clause 30.1's one exception in practice.

Note also the roles the sample assigns.
`afds-manifest.json`, the token file, the pattern registry and `stack.spec.json` are `canonical`; the two evidence files are `evidence`; `stack.md`, `docs/PACKAGE.md`, `LICENSES.md` and `adapters/README.md` are `documentation`.
The pairing on the component is the one to notice: the component specification is canonical and its component documentation is documentation, which is clause 28.3's ordering made visible in the inventory.


##### What the tokens say

`tokens/core.tokens.json` is the smallest artefact in the package and the best place to see the alias mechanism.
It declares a modular scale in `rem`, then defines spacing as aliases of scale steps rather than as independent values.

```json
{
  "space": {
    "$type": "dimension",
    "$description": "Spacing tokens are aliases of scale steps rather than independent values, so spacing cannot drift away from the type scale.",
    "tight": {
      "$value": "{scale.step-minus-1}",
      "$description": "Alias reference to the scale step below the seed."
    },
    "default": {
      "$value": "{scale.step-0}",
      "$description": "Alias reference to the seed step. This is the default Stack gap."
    },
    "loose": {
      "$value": "{scale.step-1}",
      "$description": "Alias reference to one step above the seed."
    }
  }
}
```

`space.default` is the token to follow, because it is the one the Stack contract and assertion `stack-a1` both refer to.
It resolves to `scale.step-0`, which is `{ "value": 1, "unit": "rem" }`, seeded on one line of body text.

The colour group carries a warning that matters for anyone expecting tokens to carry accessibility facts.

```json
{
  "colour": {
    "$type": "color",
    "$description": "Colour tokens are candidates for contrast pairing, not guarantees. DTCG carries values, not contrast relationships, so the pairing constraint lives in the component specification."
  }
}
```

That is the ownership rule from clause 28.2 seen from the token side: a contrast relationship is not a value, so it cannot live in a token file, and it lives instead in the contract that owns it.

##### What the component contract says

`components/stack/stack.spec.json` carries seven identity fields — `afdsSpecVersion`, `id`, `name`, `kind`, `version`, `status`, and `summary` — and then ten fields that are the substance: `semanticModel`, `derivation`, `keyboardContract`, `reflowBehaviour`, `wcagMapping`, `guarantees`, `nonGuarantees`, `assertions`, `uncertainty`, and `tests`.

Nine of those ten are the facts clause 28.2 says the canonical component contract owns; `tests` is the tenth, and points at fixtures.

The semantic model is a statement of restraint rather than of capability.

```json
{
  "semanticModel": {
    "role": "none",
    "implicitElement": "div",
    "accessibleName": "none",
    "rationale": "A layout primitive cannot know whether its children form a list, a group, a set of landmarks, or unrelated blocks. Only the consumer knows, so Stack adds no ARIA role, no accessible name, and no state.",
    "domOrderIsReadingOrder": true
  }
}
```

The keyboard contract is declared as absent rather than omitted, and says why.

```json
{
  "keyboardContract": {
    "hasKeyboardContract": false,
    "statement": "Stack has no keyboard contract. It is stated explicitly rather than omitted so that a reviewer cannot mistake absence for oversight."
  }
}
```

The derivation status is `native-first`, with `deviations` empty.

```json
{
  "derivation": {
    "status": "native-first",
    "rationale": "Stack is a flex column on a plain div. No published interaction pattern applies to it, because it has no interaction. The native element and one CSS declaration fully supply the behaviour, so no custom pattern is derived and none is needed.",
    "deviations": [],
    "supportDependent": false
  }
}
```

`guarantees` carries six entries, `stack-g1` to `stack-g6`, each naming the assertions that would substantiate it.
`nonGuarantees` carries seven items, and they are the part a developer should read first, because each one is a responsibility that remains theirs.

```json
{
  "nonGuarantees": [
    "Stack does not provide list semantics.",
    "Stack does not provide a grouping role or an accessible name.",
    "Stack does not provide a heading structure or landmark.",
    "Stack does not enforce the measure; that is the Center primitive's responsibility.",
    "Stack does not manage focus, focus order, focus trapping, or focus return.",
    "Stack does not guarantee contrast between any pair of colour tokens.",
    "Stack does not provide a basis for claiming the WCAG 1.4.10 two-dimensional exception."
  ]
}
```

Seven non-guarantees, so seven responsibilities left with the consumer.

`assertions` carries six entries, `stack-a1` to `stack-a6`, three automated and three manual.
`uncertainty` carries four records, not two, and the four are worth naming because together they are the honest boundary of the component.

| Record | Subject | Status |
| --- | --- | --- |
| `stack-u1` | Screen-reader announcement of a bare grouping container | `not-yet-tested` |
| `stack-u2` | Interaction of rem-anchored gaps with operating-system font scaling in Electron | `not-yet-tested` |
| `stack-u3` | Reflow of a Stack at 320 CSS pixels of available inline size and at 400% zoom | `not-yet-tested` |
| `stack-u4` | Voice-driven targeting of content placed inside a Stack | `not-yet-tested` |

`stack-u3` shows what an uncertainty record is for when an assertion already exists.

```json
{
  "id": "stack-u3",
  "subject": "Reflow of a Stack at 320 CSS pixels of available inline size and at 400% zoom",
  "statement": "Whether a Stack clips content or produces a page-level horizontal scrollbar at 320 CSS pixels of available inline size, or at 400% zoom, has not been tested for this sample. Assertion stack-a4 states the expected behaviour but is manual, and no observation has been recorded against it.",
  "status": "not-yet-tested",
  "evidenceRef": "evidence/at-matrix.json#stack"
}
```

An assertion states what should be true; an uncertainty record states that nobody has looked.
The contract carries both, which is the mechanism by which "nobody has checked" becomes visible rather than absent.

The `tests` field names two fixtures the package does not ship, and says so.

```json
{
  "tests": {
    "isolated": "stories/stack.isolated.md",
    "realisticPage": "stories/stack.in-page.md",
    "note": "This sample does not ship the story fixtures. The paths record where they belong in a complete package and a consumer MUST treat them as absent here."
  }
}
```

##### What the evidence file says

`evidence/at-matrix.json` carries three preamble fields — `afdsEvidenceVersion`, `description`, `resultVocabulary` — and then nine records.

The five-value result vocabulary is carried in the file itself rather than assumed: `not-yet-tested`, `supported`, `partial`, `unsupported`, `not-applicable`.
The description explains that `not-applicable` carries two distinct senses, one as a result value and one in any other field, where it means the field does not apply to that record.

Every record has the same shape.

```json
{
  "id": "stack-nvda-chromium",
  "componentId": "stack",
  "assertionRef": [
    "stack-a3"
  ],
  "claim": "The Stack container element itself is not announced as an additional structural object.",
  "engine": "Blink",
  "engineVersion": "not-yet-tested",
  "browser": "Chrome",
  "browserVersion": "not-yet-tested",
  "at": "NVDA",
  "atVersion": "not-yet-tested",
  "platform": "Windows",
  "device": "desktop",
  "startingViewport": "not-applicable",
  "zoom": "not-applicable",
  "date": "not-yet-tested",
  "result": "not-yet-tested",
  "observation": "not-yet-tested",
  "tester": "not-yet-tested",
  "uncertaintyRef": "stack-u1"
}
```

Two reference fields tie the record into the rest of the package, and their literal names matter: `assertionRef` is an array naming the assertion or assertions the record evaluates, and `uncertaintyRef` names the uncertainty record the observation would resolve.

The nine records cover four screen-reader and engine combinations (`NVDA`/Blink on Windows, `JAWS`/Blink on Windows, `VoiceOver`/WebKit on macOS, `Orca`/Gecko on Linux), one Electron font-scaling record, two Reflow records at a 320 by 640 starting viewport and at 400% zoom, and two voice-control records on Blink and WebKit.

Now do the arithmetic the contract invites.
Across the nine records, `assertionRef` names three of the six assertions — `stack-a3`, `stack-a4`, and `stack-a5` — so `stack-a1`, `stack-a2`, and `stack-a6` have no evidence record at all, and every one of the nine records reads `"result": "not-yet-tested"`.

So all six guarantees compute as unsubstantiated, and none of them is written as such anywhere in the package.
That is clause 28.2 and clause 14.3 working as intended: the status is computed from the contract and the evidence together, and prohibited from being written into either.
The package's own `notes` array says the same thing in prose, and `evidence/known-limitations.md` says why: "Fabricated evidence is worse than absent evidence, because absent evidence is visible as a gap while fabricated evidence looks like a guarantee."

##### What the pattern registry says

`patterns/registry.json` exists because the package claims `afds-patterns-native-first`, and clauses 24.2 and 29.4 require it.
It carries three entries: one for Stack, with status `native-first`, and two prohibitions.

The prohibitions are the reason the artefact is `canonical` rather than `derived`, and the registry says so itself: "This package contains one component, so the registry is mostly prohibitions. That is the expected shape for a small package and is the reason clause 24.2 requires the artefact at all: a decision not to build something leaves no component behind to declare it."

The menubar entry is worth reading for its shape.

```json
{
  "status": "prohibited",
  "notMisuse": "The ARIA Authoring Practices Guide ships a navigation menubar example demonstrating site navigation, so that use is sanctioned by its publisher. This entry is a convention of this package and is not a claim that the pattern is being misused."
}
```

That is clause 24.5 respected in a package artefact: the practice is declined as a local convention with a stated cost, and explicitly not described as a misuse.

##### Rebuilding and verifying the sample

`tools/build-inventory.py` implements the producer and consumer halves of clause 30 and part of clause 31, in about two hundred lines.
It takes three commands.

```text
python3 tools/build-inventory.py build      Regenerate afds-inventory.json.
python3 tools/build-inventory.py verify     Verify afds-inventory.json.
python3 tools/build-inventory.py pack PATH  Write a .afds ZIP to PATH.
```

Running `build` walks the source tree, excludes `tools/`, `README.md` and the inventory itself, sorts the paths, and writes one record per remaining entry with its media type, byte length, role, and SHA-256 digest.
Running `verify` recomputes everything and reports.

```text
inventory: 10 records, 10 entries digest-checked
boundary: README.md agrees with the exclusions
VERIFY PASSED: every entry is inventoried, lengths and SHA-256 digests match
```

The checks it performs map onto steps 5 to 8 of clause 31, with one addition of its own.
The boundary line has no counterpart in clause 31, because the boundary it checks is not a specification rule; an unpacked archive carries no `README.md`, so the check reports that it was skipped and the verification still passes.
It confirms `digestAlgorithm` is `SHA-256` and `excludesSelf` is `true`; it confirms the inventory holds no record for itself; it reports entries present but not inventoried and entries inventoried but not present, in both directions rather than stopping at the first; it compares `byteLength`, `sha256`, `mediaType` and `role` for every entry; and it confirms `entryCount` matches the number of records.
Reporting both directions separately is clause 31 step 6 taken literally, and gathering every problem before reporting is the second of clause 31's two deliberate properties.

`pack` refuses to write the archive inside the source tree, then runs the whole verification and refuses to pack if it fails.

```text
FAIL: refusing to pack an unverified source tree
```

That ordering is the point of the tool: a package is packed from a verified tree or not at all.
The eleven entries it writes are the ten inventoried files plus the inventory, and the archive has no enclosing top-level directory, as clause 25.1 requires.

The tool stops short of a full clause 31 consumer, and honestly so.
It verifies a source tree rather than opening a `.afds` archive and verifying it as delivered; it does not apply the clause 32.2 decompression limits, because it is not decompressing untrusted input; and it does not validate the token file against the declared `dtcgVersion`, which is step 9.
For a tester, those three are the gap between this script and a conforming consumer.


One failure mode is worth naming here, because it is the one the inventory cannot catch and the one this sample has already been through.
A published archive can fall behind the source tree it was built from.
When that happens nothing in the archive is corrupt: its digests still match its own records, so a consumer verifying it reports a pass, and it is entitled to.
What has changed is the source, and no digest inside a package can detect that, because the package has no way to refer to something outside itself.
A package proves that its bytes are the bytes its inventory describes, and clause 32.3 is careful never to claim more.
Detecting the other kind of staleness is a release-process problem rather than a format problem, which is why the packing tool refuses to build from an unverified tree.

## Part 7. Reading paths, mistakes, and what is open

### Reading paths by role

Part 1 said which reader each part serves. This is the same advice as a working order, for someone who has to start today.

#### If you are a designer

Start with the five layers, because most scope disputes are really arguments about which layer a question belongs to.
Then read the typography and colour profile (clause 23) if your organisation claims it, and the annotation rules (clause 19) whether it does or not.

The annotation rules matter more than they look.
A mock-up cannot show what a component promises, which keys operate it, where focus goes when a dialog closes, or what happens at high zoom.
Annotation is how you hand those decisions to a developer without relying on a conversation neither of you will remember.

Read clause 19's economy rule before you start annotating.
Do not annotate what the visual design, the component API, or the coded component already guarantees.

#### If you are a developer

You will consume packages and you will produce them, and clause 4.2 says that a tool doing both must satisfy both sets of obligations independently.

Read Part II in full.
It is where the obligations that affect daily work live: the seventeen fields a component specification carries (clause 7.2), the keyboard contract's eight stages (clause 10), the seven `reflowBehaviour` fields (clause 11.1), and the rule that a guarantee naming no assertion makes the package non-conforming (clause 14.2).

Then read Part IV, and read clause 31 twice.
The verification algorithm is ordered, and a consumer that runs the steps out of order can accept a package it should have refused.

Clause 35.2 is the other one to get right.
A consumer that meets a package whose major version is higher than it understands has one correct behaviour, and guessing is not it.

#### If you are a tester or QA engineer

The five testing levels (clause 18) tell you what a given piece of evidence is actually evidence for.
Evidence gathered at one level does not support a claim at another, which is the point of recording the level at all.

Read clause 16 for what an evidence record must carry — all fourteen fields, including engine, browser, version, observed behaviour and test date.
A claim that omits the engine is not a weaker claim; it is an unverifiable one.

Read clause 17 for uncertainty records.
Recording that something has not been tested, with `not-yet-tested`, is a conforming and useful act.
Leaving it out is not.

Then read the composition material in clause 18.1 to 18.3, and the companion document for the failure modes.
A component can pass every test it has and still break when assembled, and finding that is your job rather than the component author's.

### Common mistakes

These are drawn from the project's own decision record and from defects found in earlier drafts of this guide.

**Treating the layout method as mandatory.**
It is one method profile among those Part III defines, and a package may claim none.
Clause 4.3 calls an organisation satisfying the core while declining the layout method "the intended outcome, not a loophole".

**Inferring one profile axis from the other.**
Completeness profiles say how much of the hierarchy is present; method profiles say which design method is followed; the WCAG level is a third thing again.
Clause 4.5 requires them to be declared separately and prohibits inferring either from the other.

**Claiming APG conformance.**
Clause 4.4 prohibits it outright, because the ARIA Authoring Practices Guide is informative and has no conformance model to conform to.
What you can publish about a component is the accessibility criteria met, the semantics used, and the recorded assistive-technology results.

**Listing guarantees without non-guarantees.**
Clause 2.5 gives the reason: a component that lists only what it promises invites the reader to assume the rest, and the assumption is where accessibility is lost.

**Writing a guarantee that no assertion substantiates.**
Clause 14.2 makes a package containing one non-conforming.
The guarantee is not the claim; the assertion is what makes the claim checkable.

**Recording an assistive-technology result without the engine.**
Clause 16.2 requires engine, browser and version because behaviour differs between them, and a result that does not say what it was observed on cannot be reproduced or retired.

**Reading a silence in the specification as permission.**
Clause 1.2 states what the specification does not define, and clause 1.4 says the omissions the project has not decided are named in the open-questions register.
Clause 1.4 puts it directly: "A silence in a specification is not permission."

**Presenting a conformance claim as evidence that a service is accessible.**
Clause 4.4 prohibits it, and clause 2.5 explains why: a design system supplies parts, and cannot know whether the parts were assembled into a task a user can complete.

**Using the retired status names.**
`pattern-derived` and `pattern-adjacent` replaced the earlier APG-specific names, deliberately, so that the core does not name one external pattern library (clause 24.8).

**Calling a navigation menu widget a misuse.**
Clause 24.5 sanctions it in the cases the APG allows, says it must not be called a misuse, and permits recording it as a `product-deviation`.
An earlier draft of this guide listed it as a mistake, wrongly.

### What this guide does not settle

The project keeps a register of open questions, and this guide does not resolve any of them.
Where the specification is silent on something the project has not decided, clause 1.4 records that the silence is deliberate.

The register is `docs/OPEN-QUESTIONS.md`, organised in nine groups.
The items most likely to affect a reader adopting the system now:

| Register item | Status | What is unresolved |
| --- | --- | --- |
| A1. What the system contains | Partly settled | Whether the project ships components or only component specifications; whether a reference implementation is normative or illustrative; where multi-component patterns live |
| A2. Component inventory | Open | How to identify de facto components and define a useful inventory |
| A3. Composition conformance | Open | Fixture composition, number of fixtures, and attribution of a failure to component or composition |
| B1. Design Tokens as source of truth | Partly settled | DTCG JSON is the canonical portable representation for token values; whether tokens generate CSS or CSS exports tokens is open |
| B2. The `ch` problem | Open | Whether the measure axiom is an explicit web-and-Electron scope limit or needs a native analogue |
| B3. Contrast as a relationship | Open | Whether to propose an interchange representation, and an interim project convention. This is the token-standard gap clause 2.4 records as a gap rather than papering over it |
| C1. Colour system | Open | Palette values, numeric versus perceptual contrast verification, and `prefers-contrast` behaviour |
| C2. Typeface | Partly settled | The monospace companion is closed; the candidate version, its performance at small data-dense sizes, and the effect of seven weights on a discrete step scale are open |
| C3. Conformance target | Partly settled, 2026-09-01 | The mechanism is settled and the value is not: whether the project raises its own default to AAA, and whether 7:1 body contrast stays usable in data-dense reports |
| D1. Container queries | Open | Whether they replace the calc technique while preserving no-JavaScript behaviour |
| D5. Measure inside excepted regions | Open | Whether `--measure` applies, reduces, or suspends inside an excepted region |
| E1. Assistive-technology matrix | Open | Supported combinations, pass criteria, re-test cadence, and stale-result marking |
| E3. Usability testing with disabled people | Open | A feasible participation model, or an explicit limitation statement |
| E4. Naming an assistive technology | Open | Whether `at` carries a vendor-styled display name, a normalised identifier, or both, and whether matching is case-sensitive. Vendors disagree, and each is right about its own product |
| E5. Unchecked manual assertions | Open | How a manual assertion that is not an assistive-technology claim records that nobody has checked it. Clause 17.3 reaches assistive-technology claims only |
| E6. Matrix membership and support | Open | Whether the specification states that a combination's presence in an evidence matrix carries no claim of support for it |
| G1. Which patterns enter the catalogue | Open | What user or task evidence admits a pattern, and what removes one |
| G2. Adopting published patterns by reference | Settled, 2026-09-01 | Native HTML first, patterns adopted by reference rather than copied. Still open: how a deviation is recorded, reviewed, and signed off, and how a discoverability cost is assessed |
| G3. Minimum matrix per component | Open | Which browser, engine and screen-reader pairs are mandatory, and the retest cadence |
| H1. The component-contract schema | Open | The JSON Schema, the stable identifier scheme, and how the vocabulary maps onto external work |
| H3. Package identity and signing | Open | The signature mechanism, what it signs, and how a consumer expresses trust in a publisher. Clause 1.2 confirms the specification defines no signature format |
| H5. Recording a promotion | Open | Whether a promoted artefact carries a provenance field, and whether a reviewer's identity belongs in a package that makes no other identity claim |
| H6. Declaring a known-limitations artefact | Open | Clause 34 requires the artefact of a full-profile package, but no clause says which manifest field declares it |
| H7. How a source directory relates to a package | Open | The specification describes only the archive, so the boundary between a publisher's working directory and the package it produces is undefined |

Three of these deserve a note for anyone reading the guide as an adoption plan.

**A2 is the one that will cost you time.**
Clause 2.2 records the honest version: an organisation without a design system cannot adopt this method directly, because it must first identify its de facto components.
The register has not settled how to do that.

**C3 affects every contrast decision you record.**
Clause 23 sets Level AA as the default and the mechanism for declaring otherwise is settled, but the project has not decided whether to raise its own default.
Record the level you are claiming rather than assuming the project's.

**E6 affects how anyone reads your evidence.**
A matrix row records a combination someone thought worth considering, not a combination observed to work, and the specification does not yet say so.
Until it does, a reader who skims the rows without reading the `result` field can take your matrix for a support table.
The practical protection is the one the sample package uses: state in your own limitations prose what the results are and are not, and keep every `result` field populated from the clause 16.3 vocabulary rather than left blank.

### Where the rest of the material lives

This guide is one document in a set, and the set has an order of authority.

`docs/AFDS-SPECIFICATION.md` is normative for all four Parts.
Where this guide and the specification disagree, the specification wins and the disagreement is a defect in this guide.

`docs/COLOPHON.md` records the decisions and the arguments that produced them, including decisions that were rejected.
`docs/OPEN-QUESTIONS.md` records what is unsettled.
Clause 1.4 is explicit that neither is part of the specification: they record how the decisions were reached, not what conforms.
Read them for why a requirement exists, not for whether it applies.

`research/COMPONENT-FRAMEWORKS.md`, *Component Design Frameworks and the Assembly Problem*, carries the assembly analysis this guide cross-references rather than restates: the assembly hierarchy, the eight compositional failure modes, worked composite breakdowns, state propagation, and testing across the hierarchy.

`research/DESIGN-SYSTEMS.md` and `research/PORTABLE-REPRESENTATIONS.md` carry the survey work behind clauses 2.3 and 2.4.

`afds-sample/` is a working package that the worked example in this guide is taken from, and `afds-sample/tools/build-inventory.py` rebuilds its inventory.

## Appendix A. Glossary

The thirty-eight terms clause 5 defines, which carry these meanings and no other wherever a normative clause uses them.

Clause 5 is normative, and it says how to read itself: where a term defined there is used in a normative clause, "it carries this meaning and no other".
Clause 5 defines thirty-eight terms.
All thirty-eight are below, in the specification's own words or a close paraphrase.

**Accessibility Focused Design System (AFDS).**
"A design system whose accessibility contract, supporting evidence, and recorded uncertainty are first-class parts of the system rather than documentation about it."

That sentence is the whole project in one line.
The distinguishing move is not that the components are accessible.
It is that the contract, the evidence and the uncertainty are parts of the system — versioned, addressable, shipped — rather than prose written about the system afterwards and left behind when the system travels.

**AFDS package.**
A single file conforming to Part IV, containing a declared hierarchy of artefacts and the two required root artefacts.

The rest, in the order clause 5 gives them.

| Term | Definition (clause 5) |
| --- | --- |
| Container | The archive format that carries a package. |
| Artefact | Any addressable file inside a package. |
| Manifest | The root artefact declaring the package's identity, versions, profiles, and the location of the inventory. |
| Inventory | The root artefact listing the package's artefacts with their roles and digests. |
| Producer | Any tool or person that creates a package. |
| Consumer | Any tool or person that reads a package and relies on its contents. |
| Core | The clauses every package must satisfy, being clause 4, clause 5, Part II, and Part IV. |
| Method profile | A named group of requirements in Part III carrying one way of designing interfaces, binding only on a package that claims it. |
| Completeness profile | A named group of requirements in Part IV stating how much of a package hierarchy is present. |
| Conformance claim | A statement naming a format version, a completeness profile, and a set of method profiles. |
| Principle | A commitment that applies across the system and is not negotiable for an individual screen. |
| Token | A named, platform-neutral value. |
| Canonical token source | The token file a package declares as authoritative for a given token set, against which any other representation of the same values is derivative. |
| Layout primitive | A composable arrangement rule that positions content without knowing what the content means. |
| Component | An interactive element with declared semantics and behaviour. |
| Pattern | Several components co-operating through a task, together with the guidance governing that co-operation. |
| Component contract | The whole set of commitments a component makes about itself: what it guarantees, what it does not guarantee, and the assertions that make those statements checkable. Part II defines it, and it is carried by a component specification rather than being a separate artefact. |
| Component specification | The machine-readable record carrying a component contract, whose form and required fields clause 7 defines. A JSON document, and the authoritative source of every fact it carries. |
| Component documentation | The human-readable counterpart to a component specification, carrying the reasoning the specification's fields cannot express. Explanatory, introducing no fact of its own. |
| Guarantee | A statement of behaviour or property that a component commits to, expressed so that it can be tested. |
| Non-guarantee | An explicit statement of something a component does not commit to, recorded so that a consumer cannot arrive at it by assumption. |
| Assertion | A machine-checkable statement attached to a specification, whose truth can be evaluated against an implementation without human judgement. |
| Evidence record | A record of an observed result for one component in one assistive-technology combination, qualified by engine, browser, versions, observed behaviour, and date. |
| Assistive-technology combination | A named tuple of assistive technology, browser, operating system, and versions, treated as the unit that evidence attaches to. |
| Uncertainty record | A record stating that something is not known, of the same standing as a record stating a result. |
| Keyboard contract | The declared operation of a component across entry, internal movement, activation, exit, state change, restoration, pointer and touch parity, and speech-recognition operation. |
| Native baseline | The behaviour and semantics a component would have if built from platform-native elements without added roles or scripted behaviour. |
| Support-dependent pattern | A pattern whose declared behaviour is known to depend on assistive-technology or engine support that is incomplete, and which therefore carries a reassessment obligation. |
| Adapter | A tool that converts between an AFDS package and some other representation. |
| Export adapter | An adapter producing a non-AFDS representation from a package. |
| Import adapter | An adapter producing a package, or part of one, from a non-AFDS representation. |
| Transform report | The record an adapter produces stating what it carried, what it could not carry, and what a consumer must therefore not assume. |
| Measure | The length of a line of text, treated as a constraint on layout rather than as a stylistic preference. |
| User technology support | The branch of accessibility concerned with assistive-technology compatibility: roles, accessible names, states, focus, and keyboard operation. |
| User layout support | The branch of accessibility concerned with reflow, measure, spacing, contrast, and reading order. |
| Composition conformance | Conformance measured with a component placed inside a realistic page, as distinct from conformance measured with the component in isolation. |

Four of these terms are worth pausing on now, because later sections rely on them and a reader who skims the table will not have absorbed them.

*Uncertainty record* is defined as being "of the same standing as a record stating a result".
That standing is deliberate, and clause 17 depends on it.

*Non-guarantee* exists because of an asymmetry in how people read documentation: a component that lists only what it promises invites a reader to assume the rest.
Clause 14 makes the refusals explicit for that reason.

*Native baseline* is a disclosure, not a design preference: it names what the component would have done if built from platform-native elements without added roles or scripted behaviour, so that the cost of not doing so can be seen (clauses 5, 8.3).

*Composition conformance* is a different measurement from component conformance, not a stronger one.
It is conformance measured with the component inside a realistic page.

### A note on "component specification"

This phrase used to mean two different things in the specification, and if you have read an earlier edition of either document you will have met the collision.

Clause 5 defined a component specification as the *human-readable* counterpart to a component contract, while clause 7.1 defined it as the *machine-readable* JSON record — and clause 7.5 compounded it by requiring that "every component specification *SHOULD* have a human-readable counterpart", which under clause 5's definition asked every prose document to have a prose document.

That is settled, and the three terms now name three different things (clause 5).

| Term | What it names |
| --- | --- |
| Component contract | The whole set of commitments a component makes about itself. Part II defines it. It is not a separate artefact. |
| Component specification | The machine-readable JSON record that carries the contract. Clause 7 fixes its form and its seventeen required fields. |
| Component documentation | The prose counterpart to a specification, carrying the reasoning the JSON cannot express. Clause 7.5 recommends it. |

The resolution followed usage rather than the glossary: the manifest already pairs a `specification` path with a `documentation` path, the filename convention is `.spec.json`, and clause 28.1 already had a `documentation` artefact role.
The project's reasoning, and what it cost, are recorded in `docs/COLOPHON.md`.

One consequence is worth carrying with you.
Because the contract is the commitments rather than the file, a clause that speaks of placing or reading a component contract is speaking of the specification that carries it, and both readings are true.

## References

### Normative references

These are cited normatively by the specification (clause 6.1).
A dated reference means that edition applies; an undated reference means the current version applies.

- IETF RFC 2119, *Key words for use in RFCs to Indicate Requirement Levels*. <https://www.rfc-editor.org/rfc/rfc2119>
- W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*. <https://www.w3.org/TR/WCAG22/>
- W3C, *Accessible Rich Internet Applications (WAI-ARIA) 1.2*. <https://www.w3.org/TR/wai-aria-1.2/>
- WHATWG, *HTML*, Living Standard. <https://html.spec.whatwg.org/multipage/>
- Design Tokens Community Group, *Design Tokens Format Module 2025.10*. <https://www.designtokens.org/TR/2025.10/format/>
- NIST, *FIPS 180-4, Secure Hash Standard*. <https://csrc.nist.gov/pubs/fips/180-4/upd1/final>
- IANA, *Media Types registry*. <https://www.iana.org/assignments/media-types/media-types.xhtml>

### Informative references

These inform the specification without creating requirements (clause 6.2).

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
- Ecma International, *ECMA-376, Office Open XML File Formats*. Part 2 is the Open Packaging Conventions, compared in Annex A. <https://ecma-international.org/publications-and-standards/standards/ecma-376/>
- ISO/IEC 29500-2:2021, "Office Open XML file formats — Part 2: Open Packaging Conventions", fourth edition, August 2021. <https://www.iso.org/standard/77818.html>
- Ecma International, *ECMA-388, Open XML Paper Specification*, first edition, June 2009. The source of the statement quoted in Annex A that the OpenXPS packaging requirements extend those of OPC. <https://www.ecma-international.org/wp-content/uploads/ECMA-388_1st_edition_june_2009.pdf>

### Project documents

- *AFDS specification, version 1.0.0* — `docs/AFDS-SPECIFICATION.md`. Normative for all four Parts.
- *Colophon of decisions* — `docs/COLOPHON.md`.
- *Open Questions and Research Agenda* — `docs/OPEN-QUESTIONS.md`.
- *Component Design Frameworks and the Assembly Problem* — `research/COMPONENT-FRAMEWORKS.md`.
- *Design systems research note* — `research/DESIGN-SYSTEMS.md`.
- *Portable representations research note* — `research/PORTABLE-REPRESENTATIONS.md`.
- *Sample package* — `afds-sample/`.

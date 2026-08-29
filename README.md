<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# Accessible by Design

A method and platform for considering, testing, and remediating websites for accessibility, built around an accessibility-focused design system.

**Status: research and planning.** There is no implementation code yet. The repository currently records the method, evidence, decisions, and unresolved research questions that will govern implementation.

## Premise

Most accessibility work is retrofitted: a site is built, audited late, then patched issue by issue, so the same defects reappear in the next release.
If accessibility is expressed once in the design system, components can carry their accessible behaviour with them, testing can target component and composition conformance rather than page-by-page symptoms, and remediation can propagate wherever a component is used.

The limit is explicit: using a design system does not by itself make a service accessible.
A system manages some of the available UI resources and modalities; it cannot replace testing, user research, or judgement in context.

## Start here

| Document | Purpose |
| --- | --- |
| [Research summary](docs/RESEARCH-SUMMARY.md) | Orientation: premise, evidence, decisions, claims, and open questions |
| [Colophon](docs/COLOPHON.md) | Decisions with reasoning, cost, alternatives, and verification |
| [Layout method](docs/LAYOUT-METHOD.md) | Intrinsic layout, primitives, axioms, and WCAG mapping |
| [Reflow and data tables](docs/REFLOW-AND-DATA-TABLES.md) | SC 1.4.10 research and the semantic scope of its exception |
| [Open questions](docs/OPEN-QUESTIONS.md) | Single source of truth for the research agenda |
| [Design systems research](research/DESIGN-SYSTEMS.md) | Scope, prior art, tokens, annotations, and gaps |

## Documentation rule

Every material decision is recorded in five parts: the decision, reasoning, cost, rejected alternatives, and verification.
An entry without a stated cost is incomplete.
When a decision turns out to be wrong, the superseded reasoning is retained in a note rather than silently deleted.

## Licensing

Documentation and written content are licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), as marked by each file's SPDX header.
Code licensing will be added before implementation begins.

## Attribution

The layout method derives from *Every Layout* by Heydon Pickering and Andy Bell.
The method is described here in the project's own words; the commercial source text and source code are not redistributed.

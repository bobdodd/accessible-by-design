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
| [APG support](docs/APG-SUPPORT.md) | How the system adopts ARIA Authoring Practices patterns by reference |
| [AFDS specification](docs/AFDS-SPECIFICATION.md) | The full specification. Part IV carries the `.afds` ZIP container, manifest, inventory, and verification rules |
| [Open questions](docs/OPEN-QUESTIONS.md) | Single source of truth for the research agenda |
| [Design systems research](research/DESIGN-SYSTEMS.md) | Scope, prior art, tokens, annotations, and gaps |
| [Portable representations research](research/PORTABLE-REPRESENTATIONS.md) | Standards, proposals, and commercial formats for portable design systems |
| [AFDS sample package](afds-sample/) | Unpacked sources of a verified sample `.afds` package |
| [Build outputs](dist/) | Derived artefacts published with a tagged release: the packed sample and the Word specification |
| [Word build](tools/docx/) | How the Word specification is generated, and the accessibility properties the build guarantees |

## Documentation rule

Every material decision is recorded in five parts: the decision, reasoning, cost, rejected alternatives, and verification.
An entry without a stated cost is incomplete.
When a decision turns out to be wrong, the superseded reasoning is retained in a note rather than silently deleted.

## The design system representation

The project's base representation is the Accessibility Focused Design System (AFDS), currently at draft version 1.0.0.
AFDS is a portable bundle rather than a single universal file format, because no existing standard carries a complete design system.
It composes DTCG design tokens, structured component contracts, Custom Elements Manifest, Component Story Format stories, engine-qualified assistive-technology evidence, documentation, and explicit adapters, linked by a manifest.

A bundle is distributed as one ZIP-based file with the `.afds` extension, carrying a root manifest and a SHA-256 inventory so a consumer can verify it before relying on its contents.
AFDS 1.0.0 is a project draft and not a W3C standard.

## Licensing

This repository is dual-licensed.

| Material | Licence | SPDX identifier |
| --- | --- | --- |
| Code, scripts, tooling, and components | GNU General Public License v3.0 only | `GPL-3.0-only` |
| Documentation and written content in `docs/` and `research/` | Creative Commons Attribution-ShareAlike 4.0 International | `CC-BY-SA-4.0` |

The full texts are in [LICENSE](LICENSE) and [LICENSE-DOCS](LICENSE-DOCS).
Every file carries an SPDX header so that its licence travels with it when copied out of the repository.

CC BY-SA 4.0 is only one-way compatible with GPLv3: documentation from here may be absorbed into a GPLv3 work, but GPLv3 material may not be relicensed as CC BY-SA.
[CONTRIBUTING.md](CONTRIBUTING.md) explains what this means in practice for anyone contributing.

Copyright (C) 2026 Bob Dodd.

## Attribution

The layout method derives from *Every Layout* by Heydon Pickering and Andy Bell.
The method is described here in the project's own words; the commercial source text and source code are not redistributed.

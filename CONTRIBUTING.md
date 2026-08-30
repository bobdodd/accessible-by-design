<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# Contributing

Thank you for considering a contribution to *Accessible by Design*.

This project is in its research and planning phase.
There is no implementation code yet, so most useful contributions are corrections, evidence, counter-arguments, and research.
The most valuable contribution of all is a demonstration that one of the recorded decisions is wrong.

## What the project is trying to do

The premise is that accessibility should be expressed once, in a design system, rather than retrofitted page by page after a late audit.
The repository records the method, the evidence behind it, the decisions taken, the costs accepted, and the questions still open.

That means the documentation is the product at this stage.
A pull request that improves the accuracy or honesty of a decision record is as substantial as one that adds a new document.

## Where things live

| Path | Contents | Licence |
| --- | --- | --- |
| `docs/` | Method, decisions, and specifications | CC BY-SA 4.0 |
| `research/` | Prior art, standards surveys, and evidence | CC BY-SA 4.0 |
| `afds-sample/` | Sample AFDS package sources (mixed prose and code) | Per-file; see below |
| `tools/` | Scripts, test harnesses, and tooling | GPL-3.0-only |

## Licensing of contributions

This repository is dual-licensed.
Opening a pull request constitutes agreement that your contribution is offered under the licence that applies to the files you touch.
There is no separate contributor licence agreement.

| Contribution type | Licence | SPDX identifier |
| --- | --- | --- |
| Documentation and written prose | Creative Commons Attribution-ShareAlike 4.0 International | `CC-BY-SA-4.0` |
| Code, scripts, test harnesses, design-system components | GNU General Public License v3.0 only | `GPL-3.0-only` |

Add a machine-readable header to every file you create.

For Markdown, an HTML comment keeps the header invisible when the file is rendered:

```markdown
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->
```

For code, use the comment syntax of the language:

```javascript
// SPDX-License-Identifier: GPL-3.0-only
// Copyright (C) 2026 Bob Dodd
```

```python
# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Bob Dodd
```

```css
/* SPDX-License-Identifier: GPL-3.0-only */
/* Copyright (C) 2026 Bob Dodd */
```

Never use the bare `GPL-3.0` identifier.
It was deprecated in version 3.0 of the SPDX License List, and GNU licences must always carry the `-only` or `-or-later` suffix.
The `+` operator is no longer used for GNU licences either.
This project uses `GPL-3.0-only`, which locks code to version 3 with no "any later version" clause.

## The one-way compatibility rule

CC BY-SA 4.0 is one-way compatible with GPLv3.
Someone may take documentation from this repository and redistribute an adaptation under GPLv3.
Nobody may take GPLv3 material and relicense it as CC BY-SA.

The practical instruction is therefore concrete.
Do not paste code out of `tools/` into a document in `docs/` or `research/` without keeping its GPL marking on the snippet.
If a document contains a substantial code sample that is also shipped as tooling, mark that sample `GPL-3.0-only` explicitly rather than letting it inherit the surrounding document's CC licence.
Creative Commons itself discourages using BY-SA for code, because it carries neither source-provision nor patent terms.

The folder boundary is what keeps this manageable, so please keep it disciplined.

## Documentation conventions

These conventions exist because the project is an example of its own subject matter.
A repository arguing for accessible authoring has to be accessibly authored.

- Write one sentence per line.
  This keeps diffs readable and makes a sentence-level change a one-line change.
- Use real heading structure with `#`, `##`, and `###`.
  Never use bold text as a substitute for a heading.
- Give every table a header row, and check that it still makes sense read linearly, one cell after another.
- Never let colour or visual emphasis carry meaning on its own.
  If something matters, say so in words.
- Describe diagrams in prose.
  An image without an equivalent description is incomplete.
- Write link text that survives being read out of context.
  "See the Reflow research" works; "click here" does not.
- Accompany every code block, JSON example, or technical representation with an explanation of what it means.

## Decision records

Every material decision is recorded in [the colophon](docs/COLOPHON.md) in five parts.

| Part | Purpose |
| --- | --- |
| **Decision** | What was chosen, stated plainly |
| **Reasoning** | Who it benefits and by what mechanism |
| **Cost** | What was given up, stated honestly |
| **Rejected** | Alternatives considered and why they lost |
| **Verification** | How the decision is tested |

An entry without a stated cost is incomplete.
Every choice trades something away, and a record that claims otherwise is advocacy rather than documentation.

When a decision turns out to be wrong, the superseded reasoning stays in a **Note** field.
It is not silently deleted.

Unsettled questions belong in [the open questions register](docs/OPEN-QUESTIONS.md), which is the single source of truth for the research agenda.
A resolved question moves to the colophon with its decision record.

## Accessibility of contributions

A contribution is expected to meet the standard the project argues for.

- Provide a text alternative for every image, diagram, or screenshot.
- Do not rely on colour alone to distinguish states, categories, or outcomes.
- Use a real heading hierarchy rather than styling text to look like a heading.
- Write link text that is meaningful when read on its own, out of the surrounding sentence.
- Keep tables genuinely tabular, with header cells, and avoid using them for visual layout.
- If you contribute code, keep it operable by keyboard and by keyboard substitutes such as scanning software, sip-and-puff systems, and speech recognition.

## Claims and evidence

Please do not add a factual claim without a source.

- Cite standards by linking to the specification, not to a summary of it.
- Distinguish clearly between what a standard requires normatively and what a guide recommends informatively.
  This matters especially for the [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/), which is informative, against [WCAG](https://www.w3.org/TR/WCAG22/) and [WAI-ARIA](https://www.w3.org/TR/wai-aria/), which are normative.
- Record assistive-technology results with the browser, engine, screen reader, versions, and date.
  An untagged result is not evidence.
- Do not report a test you did not run.
  A placeholder marked as not yet tested is far better than an invented result.

## Third-party material

Do not paste in text or code from a source whose licence does not permit it.
The layout method in this repository derives from *Every Layout* by Heydon Pickering and Andy Bell, and is described in the project's own words precisely because the commercial source text and source code are not redistributable here.
Follow the same approach for any other commercial or restrictively licensed source: describe, attribute, and link, rather than copy.

## How to contribute

1. Open an issue first for anything substantial, so the discussion is on the record.
   Small corrections can go straight to a pull request.
2. Keep a pull request to one concern.
   A licence-header fix and a rewritten decision record should be two requests.
3. If your change contradicts an existing decision, say so explicitly in the description and propose the replacement decision record rather than editing the reasoning in place.
4. Check that new files carry the correct SPDX header before you submit.

Questions and disagreements are welcome as issues.
A recorded objection is more useful to this project than silent agreement.

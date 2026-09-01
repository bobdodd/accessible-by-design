# Component Design Frameworks — Commercial and Open Source

*Research notes for the Accessibility by Design (System) project.*

## 1. What a component design framework is

A **component design framework** (also called a component library, UI kit, or the implementation layer of a design system) is a codebase of reusable, pre-built interface elements — buttons, form fields, dialogs, tables, navigation bars — that ship with a fixed API, a fixed visual style (or theming layer), and pre-encoded interaction behavior. It is the *engineering* half of a design system: the design system defines the visual language, tokens, and usage guidelines, while the component framework is the working code that implements those decisions [cite:16][cite:19].

Most practitioners distinguish three coupled layers:

- **Design tokens** — the atomic style values (color, spacing, type scale, radii, motion durations) expressed in a platform-neutral format so they can be consumed by CSS, iOS, Android, and design tools alike [cite:24][cite:36].
- **Component library** — the actual reusable UI code (React, Vue, Web Components, Kotlin/Compose, SwiftUI, etc.) that consumes those tokens and exposes properties/variants (size, state, intent) [cite:13][cite:19].
- **Guidelines and documentation** — usage rules, accessibility notes, content style, and "do/don't" patterns that tell teams when and how to use each component [cite:13][cite:24].

A component framework matters for accessibility because it centralizes correctness. If focus management, ARIA roles, and keyboard interaction are encoded once inside a `Button` or `Dialog` component, every consuming team inherits that correctness automatically rather than re-implementing (and potentially getting wrong) the same WAI-ARIA pattern by hand [cite:30]. This is the same philosophy behind Bryan Garaventa's AccDC framework and "Automatically Accessible Technologies" concept from the 2010s — accessibility as a byproduct of the framework rather than a separate audit-and-fix layer — a philosophy now embodied in modern headless component libraries [cite:30].

## 2. How component frameworks work in practice

A typical component framework operates through several mechanisms working together:

- **Token pipeline** — a single source of design tokens (often JSON, increasingly in the new W3C Design Tokens Community Group format) is transformed by build tooling (e.g., Style Dictionary) into CSS custom properties, Sass variables, Android XML resources, or iOS Swift constants, so one change to a brand color propagates everywhere [cite:34][cite:36][cite:39].
- **Component API/props** — each component exposes a constrained set of variants (e.g., `variant="primary"`, `size="small"`, `isDisabled`) rather than open-ended styling, which keeps visual and behavioral consistency intact across an organization [cite:24][cite:25].
- **Encapsulated interaction logic** — keyboard handling, focus trapping, roving tabindex, live-region announcements, and ARIA attribute wiring are implemented once inside the component and are not something the consuming developer needs to re-derive [cite:30][cite:41].
- **Framework bindings** — the same design language is often exposed through multiple technology bindings (React, Vue, Angular, Web Components, Svelte) so it is usable across an organization's varied tech stacks; some systems (e.g., IBM Carbon, Deutsche Telekom Scale, Porsche Design System) explicitly ship parallel React/Vue/Web Component packages from one design core [cite:20][cite:27].
- **Documentation site and Figma parity** — component docs (props tables, usage guidance, accessibility notes) are usually paired with an official Figma library so designers and engineers reference the same named components [cite:24][cite:27].

### Headless vs. styled components

A key architectural split relevant to accessibility work is **headless** (or "unstyled") versus **styled** component libraries:

- **Styled/opinionated libraries** (Material UI, Chakra UI, Ant Design, Bootstrap) ship a complete visual design along with the behavior, so adopting them means adopting their look unless heavily overridden [cite:27][cite:33].
- **Headless/behavior-only libraries** (React Aria, Radix UI, Headless UI, Ariakit) provide only the accessible interaction logic — focus management, keyboard nav, ARIA roles/states, screen-reader announcements — and leave 100% of the markup and CSS to the consumer [cite:30][cite:32][cite:41]. This pattern is especially relevant to an accessibility-first design system because it lets an organization keep its own visual brand while inheriting rigorously tested accessibility behavior for hard patterns like comboboxes, date pickers, and multi-select tables [cite:41].

## 3. Worked example: building an accessible combobox

React Aria Components (Adobe) illustrates how a component framework encodes an entire WAI-ARIA pattern behind a small, declarative API. A combobox that would otherwise require dozens of lines of manual `aria-expanded`, `aria-activedescendant`, roving focus, and typeahead logic becomes:

```jsx
import { ComboBox, Input, Label, ListBox, ListBoxItem, Popover, Button } from 'react-aria-components';

const frameworks = [
  { id: 'next', name: 'Next.js' },
  { id: 'remix', name: 'Remix' },
  { id: 'vite', name: 'Vite + React' },
];

export function FrameworkPicker() {
  return (
    <ComboBox defaultItems={frameworks}>
      <Label>Framework</Label>
      <Input />
      <Button>▼</Button>
      <Popover>
        <ListBox>
          {(item) => <ListBoxItem id={item.id}>{item.name}</ListBoxItem>}
        </ListBox>
      </Popover>
    </ComboBox>
  );
}
```

React Aria supplies the keyboard interaction, focus behavior, and screen-reader semantics for the combobox, list, and popover roles internally; the developer supplies only markup and CSS [cite:41]. This is the same value proposition as GitHub's Primer, Adobe Spectrum, or IBM Carbon's coded component examples, which similarly pair a documented API with pre-verified accessibility behavior, though those are fully styled rather than headless [cite:20][cite:35].

## 4. Commercial (vendor-built, brand-specific) component frameworks

These are design systems built and maintained by a single company primarily for their own product suite, though many publish the code openly:

| System | Owner | Stack | Notes |
|---|---|---|---|
| Material Design / Material Components | Google | Web Components, React (MUI), Android, Flutter | Cross-platform visual language; MUI is the most widely used third-party React implementation [cite:15][cite:17][cite:27]. |
| Fluent Design System | Microsoft | React (Fluent UI), Web Components | Adaptive, "coherent and inclusive" cross-platform guidance [cite:15][cite:27]. |
| Human Interface Guidelines | Apple | Native iOS/macOS/watchOS/tvOS (SwiftUI/UIKit), no public component code | Guidance-only; components are native OS frameworks rather than an open library [cite:15][cite:27]. |
| Lightning Design System | Salesforce | Web Components, React, Style Dictionary | One of the earliest large-scale enterprise design systems; token pipeline heavily influenced the Design Tokens Community Group's founding [cite:15][cite:27][cite:42]. |
| Spectrum / React Spectrum & React Aria | Adobe | React | Spectrum is Adobe's styled system; React Aria is the decoupled, unstyled accessibility layer beneath it, independently reusable in any design system [cite:15][cite:38][cite:41]. |
| Atlassian Design System (Atlaskit) | Atlassian | React | Powers Jira/Confluence/Trello UI consistency [cite:15][cite:20]. |
| Polaris | Shopify | React | Merchant-experience-focused design system [cite:27]. |
| Canvas | Workday | React, Vue | Enterprise data-application focus [cite:27]. |
| SAP Fiori | SAP | Web Components (UI5), React | Enterprise business-application design language [cite:27]. |
| Porsche Design System, Audi UI | Porsche/Audi (VW Group) | Web Components with React/Angular/Vue wrappers | Automotive brand systems, notable for framework-agnostic Web Component cores [cite:27]. |

Commercial systems are typically optimized for one company's brand and product surface, and while several are open source, their governance, roadmap, and breaking-change cadence remain controlled by the vendor rather than a community [cite:16][cite:19].

## 5. Open source and community/standards-driven component frameworks

These are either fully community-governed or explicitly built as general-purpose, brand-neutral tools:

- **Bootstrap** — the most widely deployed CSS-only framework; framework-agnostic, minimal JS, huge ecosystem, but only moderate built-in accessibility unless extended [cite:17][cite:20][cite:27].
- **Ant Design** — enterprise-application-oriented React/Vue library, strong for admin dashboards and data-dense interfaces [cite:15][cite:20][cite:27].
- **shadcn/ui** — a copy-in (not npm-installed) component collection built on Radix UI primitives and Tailwind CSS; popular in 2024–2026 for its "own the code" philosophy rather than dependency-based distribution [cite:14][cite:27].
- **Radix UI / Ariakit / Headless UI** — headless, accessibility-first primitive libraries providing only ARIA-correct behavior and state, meant to be styled from scratch; foundational to the current wave of accessible design systems [cite:27][cite:32][cite:33].
- **React Aria (Adobe)** — open-sourced, framework-level accessible interaction hooks/components, independent from Adobe's own Spectrum brand styling [cite:38][cite:41].
- **Carbon Design System** (IBM) — fully open source, ships React/Vue/Svelte packages plus a Style Dictionary token pipeline and official Figma kit; one of the most complete "system + code + docs + Figma" open examples [cite:17][cite:20][cite:27].
- **Chakra UI, Mantine** — accessible-by-default, themeable React component libraries popular for greenfield product builds [cite:27].
- **PatternFly** (Red Hat) — enterprise console/operator-UI design system, React/Angular/CSS-only, open source [cite:27].
- **KoliBri** (German federal IT agency, Informationstechnikzentrum Bund) — framework-agnostic reference implementation of WCAG/BITV (Germany's accessibility regulation), explicitly built as a generic, themeable presentation layer rather than a branded product, of direct interest for a standards-based accessibility design system [cite:20].
- **Lion** (ING) — "white label accessible Web Components" explicitly designed to be extended and restyled by any consuming organization, another framework-agnostic accessibility-first example [cite:20].
- **WAI-ARIA Authoring Practices** (W3C) — not a component library but the canonical behavioral specification (roles, states, keyboard patterns) that most of the libraries above implement; Open UI (a W3C-adjacent community group) explicitly tracks it alongside vendor design systems as source material for standardizing native HTML controls [cite:20].

### Government and public-sector design systems

Government systems are especially relevant models for this project because accessibility compliance (not just brand consistency) is a first-class, often legally mandated, design constraint:

- **GOV.UK Design System** (UK) — MIT-licensed, WCAG AA baseline, published an explicit "accessibility strategy" grounded in the 7 principles of universal design and progressive enhancement (semantic HTML first, content available without CSS, and functional without JavaScript) [cite:35][cite:40][cite:43].
- **U.S. Web Design System (USWDS)** — federal equivalent, CSS-only/framework-agnostic, built explicitly to make government sites accessible and mobile-friendly [cite:20][cite:27].
- **Designsystemet** (Norway), **DKFDS** (Denmark), **NL Design System** (Netherlands), **New Zealand Government Design System**, **Canada.ca Design System** — a growing cluster of shared, open-source, cross-agency systems; the Dutch model is notable for being an *architecture* that individual agencies build their own component libraries on top of, rather than one single shared library — a governance pattern worth studying for a multi-team accessibility design system [cite:27].

## 6. How commercial and open-source approaches differ

| Dimension | Commercial/vendor systems | Open source/community systems |
|---|---|---|
| Primary goal | Brand consistency for one company's products [cite:16] | Reusability and accessibility across many unrelated products [cite:20][cite:27] |
| Governance | Vendor-controlled roadmap and breaking changes [cite:19] | Public issue trackers, community contribution, sometimes multi-agency governance (e.g., NL Design System) [cite:27] |
| Styling | Usually fully opinionated/branded (Material, Spectrum, Fiori) [cite:27] | Ranges from fully styled (Carbon, Ant Design) to headless/unstyled (Radix, React Aria, Ariakit) [cite:27][cite:33] |
| Accessibility mandate | Often strong but secondary to brand (varies widely by vendor) [cite:27] | Frequently the explicit, primary design constraint, especially for government systems (GOV.UK, USWDS) and accessibility-focused libraries (KoliBri, Lion, React Aria) [cite:20][cite:35][cite:43] |
| Token format | Often proprietary/custom pipelines historically | Converging on the new W3C Design Tokens Community Group JSON specification (stable as of October 2025) for cross-tool interoperability [cite:34][cite:36][cite:39] |

## 7. Relevance to this project

For an accessibility-focused design system and testing platform, the most instructive references are the ones that treat accessibility as an architectural property of the component rather than a documentation add-on: React Aria's separation of "unstyled accessible behavior" from "brand styling" [cite:41], KoliBri's and Lion's "white label, framework-agnostic, standards-first" component philosophy [cite:20], and GOV.UK's explicit progressive-enhancement and universal-design accessibility strategy [cite:35][cite:40][cite:43]. The emerging W3C Design Tokens format is also worth tracking, since a portable, standards-based token format would let an accessibility design system's values (contrast-safe color pairs, minimum touch-target spacing, motion-reduction durations) be consumed consistently across Kotlin/Compose, web, and design tooling [cite:34][cite:36][cite:39].

## Sources

Research compiled from web searches conducted September 1, 2026, drawing on a11ybob.com glossary and research pages, Open UI's design systems catalog, the DesignSystems.one library of 100 real-world systems, the GOV.UK Design System accessibility strategy pages, the W3C Design Tokens Community Group announcements, and documentation/discussion for React Aria, Radix UI, and Headless UI.

# Provenance — Mermaid C4 profile

Sources for [C4/PROFILE.md](../../../skills/system-design/C4/PROFILE.md). Mermaid syntax is first-party documentation; the stricter text limits, metadata header, no-fallback rule, and target list are product decisions for this skill.

## 1. Allowed keywords

| Claim | Source |
|---|---|
| Mermaid C4 supports `Person`, `System`, `SystemDb`, `SystemQueue`, `Container`, `ContainerDb`, and `ContainerQueue`, with `_Ext` variants | [Mermaid C4 syntax](https://mermaid.js.org/syntax/c4.html) (checked 2026-11-12) |
| Boundaries use the block form, and `Boundary` and `Container_Boundary` are not part of this profile | [Mermaid C4 syntax](https://mermaid.js.org/syntax/c4.html) for the syntax; product decision to keep this skill's structure at Context plus Container and forbid nested boundaries. |
| Relationships use `Rel`, the directional variants, and `BiRel`; `Rel_Back` reverses the arrow | [Mermaid C4 syntax](https://mermaid.js.org/syntax/c4.html) (checked 2026-11-12) |
| Prefer two explicit relationships over `BiRel` when direction is load-bearing | Product decision: direction is a design claim and must remain visible to cross-level checks. |
| L2 technology is `<sync|async> <transport>`, with `auth=<posture>` at boundaries | [Mermaid C4 syntax](https://mermaid.js.org/syntax/c4.html) for the technology field; product decision for the closed transport list and auth-posture grammar so failure and trust boundaries stay machine-checkable. |
| Every block carries `%% system-in-scope:`, `%% c4-level:`, and `%% legend:` | Product decision: the first two are the machine-checkable scope and level contract; the legend makes arrow direction and ownership reviewable without guessing. |
| The rendered title is `Context view - <System>` or `Container view - <System> - <Candidate>` | Product decision: level and scope must survive outside the `%%` comments and into the rendered artifact. |
| `accTitle:` and `accDescr:` are recommended and become required only after the target renderer accepts them | Product decision: an accessibility claim must be verified rather than assumed. |
| Styling and layout use `UpdateElementStyle`, `UpdateRelStyle`, and `UpdateLayoutConfig` | [Mermaid C4 syntax](https://mermaid.js.org/syntax/c4.html) (checked 2026-11-12) |
| `UpdateLayoutConfig` is the last statement; `c4ShapeInRow` is 3 at Level 1 and 3–4 at Level 2 | Product decision: the fixed C4 layout engine reads declaration order and the grid width, and the last-statement rule keeps later declarations from overriding it. |

## 2. Text argument rules (why the profile is stricter than Mermaid)

| Claim | Source |
|---|---|
| Quote every text argument | [Mermaid C4 syntax](https://mermaid.js.org/syntax/c4.html) (checked 2026-11-12); quoting is the portable form across renderer versions. |
| Avoid commas, parentheses, and HTML in C4 text | Product decision: some C4 parser and renderer versions treat commas as separators, so the stricter form is the portable one; Mermaid's quoted arguments are not treated as a portability guarantee. |
| Use ASCII only in C4 text | Product decision: non-ASCII widths and dash variants break the C4 auto-wrapper across renderers. |
| Labels are at most four words and forty characters, descriptions at most twenty-four words and one hundred forty characters, and technologies at most forty characters | Product decision: the C4 box auto-wraps, and longer text produces unreadable boxes. The description limit still leaves room for one plain-language state contract on an authoritative store. |

## 3. Unsupported in C4 (never emit)

| Claim | Source |
|---|---|
| `subgraph`, `classDef`, `class`, `style`, `linkStyle`, `click`, `direction`, flowchart arrows, YAML front matter, and C4 theme overrides are not C4 structure syntax | [Mermaid C4 syntax](https://mermaid.js.org/syntax/c4.html) and [Mermaid flowchart syntax](https://mermaid.js.org/syntax/flowchart.html) (checked 2026-11-12); product decision to reject them in this skill's C4 blocks. |
| Sprites and icons that need registered icon packs are not portable | Product decision: the skill ships no icon pack and the document must render on its own. |

## 4. Canonical palette

| Claim | Source |
|---|---|
| C4 has conventional internal, external, person, and container colours | [C4 model — Notation](https://c4model.com/diagrams/notation) and [Mermaid C4 syntax](https://mermaid.js.org/syntax/c4.html) (checked 2026-11-12) |
| Explicit colours must meet a 4.5:1 contrast ratio | [WCAG 2.2 — Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) (checked 2026-11-12) |
| White text on `#438DD5` is about 3.5:1; `#2A6FA8` raises it above 4.5:1 | Calculated from the WCAG relative-luminance formula: white on `#438DD5` is 3.49:1 and white on `#2A6FA8` is 5.33:1. |
| Do not encode meaning in colour alone; use `_Ext` variants and a `%% legend:` line | Product decision: the diagram must remain readable without colour and on monochrome output, and the legend states the arrow convention and ownership rule in every block. |

## 5. Layout tactics (no coordinate control exists)

| Claim | Source |
|---|---|
| C4 layout follows declaration order and the layout engine is fixed | [Mermaid C4 syntax](https://mermaid.js.org/syntax/c4.html) (checked 2026-11-12) |
| Declare people, then the system in scope, then external systems; declare relationships in drawing order; simplify rather than adding a second view | Product decision: these are the controllable inputs under a fixed layout engine, and this SAD keeps one context and one container view per candidate. |
| `c4ShapeInRow` controls grid width and boundaries get their own row budget | [Mermaid C4 syntax](https://mermaid.js.org/syntax/c4.html) (checked 2026-11-12) and product decision for the 3 / 3–4 defaults. |

## 6. No flowchart fallback

| Claim | Source |
|---|---|
| This skill has no flowchart fallback for C4 | Product decision: the document contract is C4-only; a flowchart would be a second structure representation and would bypass the C4 checks. |
| If C4 cannot render, keep the source and record rendering as unknown | Product decision: an uninspected render is unknown, not passed. |

## 7. Known-good rendering targets

| Claim | Source |
|---|---|
| C4 support is experimental and targets Mermaid 10.9 or later, with 11.x recommended | [Mermaid C4 syntax](https://mermaid.js.org/syntax/c4.html) (checked 2026-11-12); the minimum is a product decision for the shipped examples. |
| GitHub, GitLab, Mermaid Live Editor, mermaid-cli 11.x, VS Code Markdown Preview, and Docusaurus/MDX render Mermaid | First-party renderer documentation; the list is a product decision about supported targets, not a guarantee for every version. |
| The repository renders examples with `npx -y @mermaid-js/mermaid-cli` | Product decision: the command is the checked local render path. |

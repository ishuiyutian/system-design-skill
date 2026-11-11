# Mermaid C4 Profile

Mermaid profile for the structure step in [SKILL.md](../SKILL.md). The modeling rules are
[RULES.md](RULES.md).

Target: **Mermaid ≥ 10.9 (11.x recommended)**. C4 support is still flagged *experimental*:
the layout engine is fixed (no dagre/elk options), so we control layout by declaration order
and `UpdateLayoutConfig`, not by positioning hints.

## 1. Allowed keywords

### Elements
| Keyword | Signature | Use |
|---|---|---|
| `Person` / `Person_Ext` | `(alias, "Label", "Descr")` | Human actor; use `_Ext` outside the scope |
| `System` / `System_Ext` | `(alias, "Label", "Descr")` | Software system; `System` **only** for the scope |
| `SystemDb` / `SystemDb_Ext` | `(alias, "Label", "Descr")` | System that is fundamentally a data store; use `_Ext` outside the scope |
| `SystemQueue` / `SystemQueue_Ext` | `(alias, "Label", "Descr")` | System that is fundamentally a queue/bus; use `_Ext` outside the scope |
| `Container` / `Container_Ext` | `(alias, "Label", "Technology", "Descr")` | Separately runnable/deployable unit; use `_Ext` outside the scope |
| `ContainerDb` / `ContainerDb_Ext` | `(alias, "Label", "Technology", "Descr")` | Database / file store / blob store; use `_Ext` outside the scope |
| `ContainerQueue` / `ContainerQueue_Ext` | `(alias, "Label", "Technology", "Descr")` | Queue / topic / bus; use `_Ext` outside the scope |

### Boundaries (block form only)
```text
Enterprise_Boundary(alias, "Label") {
  ...
}
System_Boundary(alias, "Label") {
  ...
}
```
`Boundary` and `Container_Boundary` exist in Mermaid but are **not** part of this profile
(`Container_Boundary` is an L3 grouping device).

### Relationships
`Rel(from, to, "Label", "Technology", "Descr")` — technology must be omitted at L1 and
**required at L2** in this skill. The L2 technology field is `<sync|async> <mechanism>`; a
boundary-crossing relationship adds `; auth=<posture>`.
Directional variants: `Rel_U/D/L/R`, `Rel_Up/Down/Left/Right`, `BiRel`, `BiRel_U/D/L/R`.
`Rel_Back` is allowed but discouraged (it reverses the arrow and confuses roll-up checks).
Prefer two explicit `Rel` statements over `BiRel` when direction is load-bearing.

### Mechanism vocabulary

`[R2]` The mechanism is one value from this closed list. The token is a real transport or, where
the edge is a storage access, a named access path:

```text
HTTPS, HTTP, gRPC, GraphQL, WebSocket, SQL, key read, log read, log append,
log read/append, object read, object write, object read/write, queue, filesystem,
in-process, IPC, AMQP
```

Two mechanism hits in one field is a violation; `sync HTTPS` names one mechanism, `sync object
read/write` names one combined access path. A boundary crossing adds `; auth=<posture>`, where
`none public` is a posture.

### Metadata header

Every C4 block carries:

```text
%% system-in-scope: <scope alias>
%% c4-level: L1|L2
%% legend: arrows show <convention>; <ownership rule>; <abbreviation note>
```

Use the same scope alias in the context and every candidate boundary. The rendered title carries
the level and scope:

```text
title Context view - <System>
title Container view - <System> - <Candidate>
```

`accTitle:` and `accDescr:` are recommended; they become required only if the target renderer
accepts them in a C4 block. An uninspected accessibility claim is not a pass.

### Styling / layout
```text
UpdateElementStyle(alias, $bgColor="#1168BD", $fontColor="#FFFFFF", $borderColor="#0F5BA5", $legendText="System in scope")
UpdateRelStyle(from, to, $textColor="#000000", $lineColor="#707070", $offsetX="10", $offsetY="-10")
UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```
`UpdateLayoutConfig` must be the **last** statement. `$c4ShapeInRow` 3 (L1) / 3–4 (L2).

## 2. Text argument rules (why the profile is stricter than Mermaid)

| Rule | Reason |
|---|---|
| Always double-quote every text argument | Unquoted text breaks on spaces/keywords across versions `[S4]` |
| No `,` inside text | Some C4 parser and renderer versions treat commas as argument separators; avoiding them keeps the text portable `[F6]` |
| No `(` `)` inside text | Parenthesis matching in the C4 grammar is fragile `[F6]` |
| No `<br/>` / HTML | Line breaks render inconsistently in C4; shorten the text instead `[F6]` |
| ASCII only | Non-ASCII widths break the auto-wrapper `[S4][F6]` |
| Label ≤ 4 words and ≤ 40 chars, description ≤ 24 words and ≤ 140 chars, technology ≤ 40 chars | The C4 box auto-wraps; long text produces unreadable boxes. An authoritative store may spend its description on one plain-language state contract `[F4]` |

Rewrites: `"Order API (v2)"` → `"Order API - v2"`; `"Stores users, orders"` → `"Stores users and orders"`;
`"Java 21 (Spring Boot 3)"` → `"Java 21 / Spring Boot 3"`.

## 3. Unsupported in C4 (never emit)

`subgraph`, `classDef`, `class`, `style`, `linkStyle`, `click`, `direction`, `-->`, `---`,
YAML front-matter config, `%%{init}%%` theme overrides for C4 shapes, icons/`$sprite`
(sprites need registered icon packs — not portable).

## 4. Canonical palette

| Role | `$bgColor` | `$fontColor` | `$borderColor` |
|---|---|---|---|
| Person | `#08427B` | `#FFFFFF` | `#073B6F` |
| System in scope | `#1168BD` | `#FFFFFF` | `#0F5BA5` |
| Container | `#438DD5` | `#FFFFFF` | `#3C7FC0` |
| External system / person | `#999999` | `#000000` | `#8A8A8A` |

Defaults already distinguish internal (blue) from external (grey) — explicit styling is optional.
Never encode meaning in colour alone: use the `_Ext` variants and a `%% legend:` line.
Explicit colours must meet WCAG contrast (≥ 4.5:1). Note that white on `#438DD5` is ~3.5:1;
darken to `#2A6FA8` if accessibility matters.

## 5. Layout tactics (no coordinate control exists)

1. Declare in reading order: **people → system in scope → external systems**.
2. Declare relationships in the same order you want them drawn; the first `Rel` anchors the layout.
3. Use `Rel_U` / `Rel_D` sparingly to push actors above and dependencies below.
4. `$c4ShapeInRow` controls the grid width; boundaries get their own row budget.
5. If the diagram is still unreadable, **simplify it** — this SAD keeps one context and one container view per candidate, so do not add a second view.

## 6. No flowchart fallback

This skill has no flowchart fallback. A `flowchart`, `graph`, or `sequenceDiagram` block is not a
C4 structure diagram and must not be used to work around a renderer. If the host cannot render C4,
keep the C4 source, say rendering was not inspected, and claim nothing it would have shown.

## 7. Known-good rendering targets

GitHub / GitLab (recent), Mermaid Live Editor, mermaid-cli 11.x, VS Code Markdown Preview
Mermaid, Docusaurus/MDX with mermaid. This repository renders the shipped examples with:

```bash
npx -y @mermaid-js/mermaid-cli -i <diagram>.mmd -o <diagram>.svg
```

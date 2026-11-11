# Provenance — Design document format

Sources for [DESIGN-FORMAT.md](../../skills/system-design/DESIGN-FORMAT.md). The document contract is a product decision; the diagram claims have external sources.

## The one artifact

| Claim | Source |
|---|---|
| One Markdown document as the source of truth, with no generated copy | Product decision: the artifact a later agent session and a human reviewer both read directly. |
| Legacy `design.json` is a read-only migration input | Backwards-compatibility decision; no new structured source is created. |

## Investigation register

| Claim | Source |
|---|---|
| Freshness is a judgment from re-reading sources, not a byte digest | Explicit trade-off of removing the bundled runtime; the limitation is stated rather than hidden. |
| Missing coverage establishes neither absence nor refutation | [Evidence lifecycle](HEURISTICS.md#evidence-and-uncertainty). |

## Diagram choice

| Claim | Source |
|---|---|
| One diagram kind per design, chosen from context, with user escalation when two are tied | Product decision: a single representation stays legible and comparable; the limitation for what the kind cannot show is stated rather than hidden. |
| Mermaid supports C4 context, container, component, dynamic, and deployment diagrams | [Mermaid C4 documentation](https://mermaid.js.org/syntax/c4.html) |
| C4 layout follows statement order and `RelIndex` ignores its index parameter | [Mermaid C4 documentation](https://mermaid.js.org/syntax/c4.html) |
| Mermaid supports flowcharts with subgraphs, shapes, and labelled edges | [Mermaid flowchart documentation](https://mermaid.js.org/syntax/flowchart.html) |
| Mermaid sequence diagrams support `autonumber`, `alt`/`else`, `par`, `loop`, and notes | [Mermaid sequence diagram documentation](https://mermaid.js.org/syntax/sequenceDiagram.html) |
| Mermaid `architecture-beta` is beta and its syntax may change | [Mermaid architecture documentation](https://mermaid.js.org/syntax/architecture.html) |
| GitHub renders Mermaid in Markdown files, issues, discussions, pull requests, and wikis | [GitHub diagram documentation](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) |
| C4 support depends on the renderer's Mermaid version, so flowchart and sequence are the safer portable forms | Explicit portability limit; GitHub documents Mermaid rendering but does not pin every diagram type. |

## Verification

| Claim | Source |
|---|---|
| Structural validation, semantic review, and diagram rendering establish distinct properties | [Evidence lifecycle](HEURISTICS.md#evidence-and-uncertainty); rendering only inspects presentation. |

## The debt register

| Claim | Source |
|---|---|
| Identity is pattern plus sorted component ids, with aliases and carry-forward of human decisions | [Audit identity and merge](AUDIT.md#identity-and-merge). |
| Severity is looked up from consequence and exposure, never chosen | [Audit severity](AUDIT.md#severity). |

# Provenance — Design document format

Sources for [DESIGN-FORMAT.md](../../skills/system-design/DESIGN-FORMAT.md). The document contract is a product decision; the diagram claims have external sources.

## The one artifact

| Claim | Source |
|---|---|
| One Markdown document as the source of truth, with no generated copy | Product decision: the artifact a later agent session and a human reviewer both read directly. |
| Legacy `design.json` is a read-only migration input | Backwards-compatibility decision; no new structured source is created. |

## Section order

| Claim | Source |
|---|---|
| The unified SAD main body carries business context, security, principles, business impact, scope, solution design, data, decisions, technology impacts, data classifications, next steps, and glossary | Product decision: the document must be reviewable by business, security, and engineering stakeholders, not only by the engineer who wrote it. |
| Evidence, debt, deep dives, and measurements live in appendices | Product decision: keeps the main body readable while preserving the engineering record that makes the design resumable and auditable. |
| The debt appendix is omitted entirely in greenfield | Repository-only audit; an empty heading would claim a survey that never ran. |
| Every required section contains content or `n/a — <reason>` | Empty headings hide missing work; an explicit `n/a` keeps the template honest without forcing irrelevant content. |
| Glossary terms are project-specific and separate from the skill vocabulary | Project terms such as CMDB, ITSM, and SLA are design content; the internal vocabulary governs the agent's language. |

## Document skeleton

| Claim | Source |
|---|---|
| A copy-paste skeleton is the canonical new-document shape | Product decision: reduces heading drift and makes resume and migration deterministic. |

## Required content by section

| Claim | Source |
|---|---|
| Section contracts name required content and the `n/a` rule | Product decision: a SAD needs business, security, impact, and data-classification content that the earlier engineering record did not require. |

## Legacy migration

| Claim | Source |
|---|---|
| A pre-2.1 `DESIGN.md` is migrated in place, preserving `Notes` and never creating a second document | Product decision: changing the template must not fork the source of truth or lose user-owned notes. |
| A pre-2.3 `DESIGN.md` has its `Diagram kind:` line replaced by the two role lines and its structure blocks converted to C4Container | Product decision: the diagram contract changed without forking the document. |

## Appendix — Evidence and open questions

| Claim | Source |
|---|---|
| Freshness is a judgment from re-reading sources, not a byte digest | Explicit trade-off of removing the bundled runtime; the limitation is stated rather than hidden. |
| Missing coverage establishes neither absence nor refutation | [Evidence lifecycle](HEURISTICS.md#evidence-and-uncertainty). |

## Structure diagrams

| Claim | Source |
|---|---|
| Structure uses one C4Context for the document and one C4Container per candidate; critical-flow behavior and dependency contracts live in Key Design Decisions | Product decision: C4 keeps the structure high-level and readable; removing flow diagrams keeps the document simple without losing the contracts. |
| C4Container wraps the business system in `System_Boundary` and does not invent generic `Edge`, `Application`, or `Data` systems | Product decision: generic layers hide ownership and put unrelated concepts in one boundary. |
| C4 container descriptions use plain business language; implementation terms belong in the technology field | Product decision: a structure diagram must stay readable to business and security reviewers. |
| A simple linear flow gets no diagram and no table; it is omitted or summarized | Product decision: a table that restates a trivial flow adds noise and can drift from the diagram. |
| Mermaid supports C4 context, container, component, dynamic, and deployment diagrams | [Mermaid C4 documentation](https://mermaid.js.org/syntax/c4.html) |
| C4 layout follows statement order and `RelIndex` ignores its index parameter | [Mermaid C4 documentation](https://mermaid.js.org/syntax/c4.html) |
| Mermaid `architecture-beta` is beta and its syntax may change | [Mermaid architecture documentation](https://mermaid.js.org/syntax/architecture.html) |
| GitHub renders Mermaid in Markdown files, issues, discussions, pull requests, and wikis | [GitHub diagram documentation](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) |
| C4 support depends on the renderer's Mermaid version | Explicit portability limit; GitHub documents Mermaid rendering but does not pin every diagram type. |

## Component kinds

| Claim | Source |
|---|---|
| `kind` selects the C4 element and the same kind list applies to every candidate | Product decision: one vocabulary keeps candidate structures comparable. |
| Internal services and stores map to `Container`, `ContainerDb`, and `ContainerQueue`; shared external stores and queues map to `SystemDb_Ext` and `SystemQueue_Ext` | [C4 model — Container diagram](https://c4model.com/diagrams/container) and [Mermaid C4 syntax](https://mermaid.js.org/syntax/c4.html) (checked 2026-11-12); the ownership mapping is a product decision. |
| CDN, DNS, and load balancers are not C4 elements | Product decision: they are deployment details recorded in Technology Impacts or Key Design Decisions. |

## Candidate records

| Claim | Source |
|---|---|
| Candidate records use structure diagrams only, with no per-candidate component, edge, flow-step, or flow diagram | Product decision: the tables and flow diagrams duplicated the structure, drifted from it, and made the document harder to read. |
| Only load-bearing component, dependency, and flow facts are shown; the rest is omitted | Product decision: a fact that cannot change topology, failure behavior, cost, or the recommendation is noise. |
| Flow diagrams replace flow step tables; a flow that does not earn a diagram is omitted or summarized | Product decision: diagrams carry step order and branches without a duplicate table that can drift. |
| C4 container descriptions state load-bearing state promises in plain business language; Key Design Decisions carries load-bearing deadline, retry, and backlog contracts | Product decision: the structure stays readable and the contracts remain recorded without a flow diagram. |

## Verification

| Claim | Source |
|---|---|
| Structural validation, semantic review, and diagram rendering establish distinct properties | [Evidence lifecycle](HEURISTICS.md#evidence-and-uncertainty); rendering only inspects presentation. |
| SAD section presence, ordering, and `n/a` reasons are checked separately from semantic quality | Product decision: structural completeness does not prove the architecture, but a missing section or unexplained `n/a` makes the document unreviewable. |
| One C4Context for the document and one C4Container per candidate, with structure-only diagrams, are checked separately from architectural quality | Product decision: the structure contract is the document contract, not a stylistic preference. |
| Every container or external system has at least one relationship | Product decision: an orphan container claims a component the design never connects. |

## Appendix — Architectural debt

| Claim | Source |
|---|---|
| Identity is pattern plus sorted component ids, with aliases and carry-forward of human decisions | [Audit identity and merge](AUDIT.md#identity-and-merge). |
| Severity is looked up from consequence and exposure, never chosen | [Audit severity](AUDIT.md#severity). |

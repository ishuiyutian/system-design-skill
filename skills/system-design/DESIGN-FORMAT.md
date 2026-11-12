# Design document format

The artifact and format contract for [SKILL.md](SKILL.md): the records used from **Establish the current truth** onward, and the one document written at **Write and verify**—`DESIGN.md`, which is the source of truth.

`DESIGN.md` is a Solution Architecture & Design (SAD) document. Its main body is readable by business, security, and engineering stakeholders; the evidence, debt, deep dives, and measurements that justify it live in appendices.

## Contents

- [The one artifact](#the-one-artifact) · [Frontmatter](#frontmatter) · [Section order](#section-order)
- [Document skeleton](#document-skeleton) · [Required content by section](#required-content-by-section)
- [Structure diagrams](#structure-diagrams) — C4Context and C4Container, and renderer limits
- [Component kinds](#component-kinds) — the C4 element vocabulary
- [Candidate records](#candidate-records) — structure diagrams, trade-offs, migration
- [Verification](#verification) · [ADR on decision](#adr-on-decision-repo-mode) · [Vocabulary](#vocabulary)

## The one artifact

| Artifact | Location | Lifecycle |
|---|---|---|
| `DESIGN.md` | `docs/design/<slug>/` (git repo) or `./<slug>/` (no repo) | **DESIGN.md is the source of truth.** Every iteration edits this file in place; there is no JSON, rendered report, or generated copy |

A run writes only `DESIGN.md`, and at **Record the decision** the ADR and docs-index link the user accepts.

`## Notes` is user-owned. Preserve it verbatim on every update, and create it empty on first write.

## Frontmatter

```yaml
---
date: 2026-11-11
mode: greenfield        # repo | greenfield
status: draft           # draft | decided
decided: null           # candidate id once status is "decided"
observed:               # repo mode in git only; omit otherwise
  commit: 9fceb02d0ae598e95dc970b74767f19372d61af8
  uncommittedChanges: false
---
```

`mode`, `status`, `decided`, and `observed` carry the same meaning they carried in the old structured source. The H1 below the frontmatter is the title; the directory name is the slug.

A run creates a draft skeleton with this frontmatter and the headings below at **Locate and resume**, then fills it in place. Resuming reads this file before any new discovery.

## Section order

> **Staged.** Only **Context & Background**, **Scope & Requirements**, and **Solution Design** are confirmed. The remaining sections and appendices are commented out until their turn.

### Main body

1. **Context & Background** — a plain-language summary, business objectives, and constraints. Nothing else, and no technology.
2. **Scope & Requirements** — in scope, out of scope, and an FR table where every requirement names its source. Nothing else.
3. **Solution Design** — current state, future state, high-level solution design, conceptual design, candidate architectures, and a recommended architecture with one comparison table for every option. Opens with `Structure diagram:` and its reason.
<!-- staged, not yet confirmed:
4. **Data Sets & Data Model** — core entities and invariants, consistency model, schemas, data sets, and data impact or migration.
5. **Key Design Decisions** — decision log, interface contracts, integrations, integration details and data mapping, mobile/client details, recommendation, and rejected alternatives.
6. **Technology Impacts** — assumptions, delivery risks and issues, operations and rollout, cost/licensing/team impacts, and what breaks first.
7. **Data Classifications** — data sets and sensitivity, retention and archival, anonymization, normalization, and exemptions or technical debt.
8. **Next Steps** — owned actions with a horizon.
9. **Glossary & References** — project-specific terms and acronyms, plus the documents and sources this design depends on.
-->

### Appendices

<!-- staged, not yet confirmed:
- **Appendix — Evidence and open questions** — the investigation register: evidence, questions, unknowns, and checks.
- **Appendix — Architectural debt** — repository mode only. Omit the heading entirely in greenfield; an empty heading claims a survey that never ran.
- **Appendix — Critical deep dives** — the two or three decisions under the greatest correctness, cost, or operability pressure.
- **Appendix — Measurements that could overturn the decision** — the falsification plan for the load-bearing assumptions.
-->

`## Notes` is last and user-owned.

<!-- staged, not yet confirmed:
Debt sits in an appendix because it describes the system that exists, while the main body describes the one being proposed. Keep it away from Technology Impacts: a delivery risk is a future failure with a horizon, a finding is a present defect with a cost.
-->

## Document skeleton

```markdown
---
date: YYYY-MM-DD
mode: repo | greenfield
status: draft
decided: null
observed:
  commit: <sha>
  uncommittedChanges: false
---

# <Title>

## Context & Background

## Scope & Requirements

## Solution Design

Structure diagram: C4Context + C4Container
Why: <one line>

<!-- staged: Data Sets & Data Model, Key Design Decisions, Technology Impacts, Data Classifications, Next Steps, Glossary & References, and the appendices -->

## Notes
```

<!-- staged, not yet confirmed:
In repository mode, insert `## Appendix — Architectural debt` between the evidence and critical-deep-dives appendices. In greenfield, omit it.
-->

## Required content by section

A confirmed section stays present and contains content or `n/a — <reason>`. Never leave an empty heading.

| Section | Must contain | `n/a` allowed |
|---|---|---|
| Context & Background | problem summary; business objectives; constraints | Business objectives may state `none` with a reason |
| Scope & Requirements | in scope; out of scope; FR table where every requirement names its source | Out-of-scope must state `none` rather than disappear |
| Solution Design | current state; future state; high-level solution design; conceptual design; C4Context high-level view; C4Container per candidate; the recorded structure role; a recommended architecture backed by one comparison table of every option's pros and cons | No |

<!-- staged, not yet confirmed:
| Section | Must contain | `n/a` allowed |
|---|---|---|
| Data Sets & Data Model | core entities and invariants; consistency and conflict resolution; schemas; data sets; data impact and migration | `n/a — no structured state` with a reason |
| Key Design Decisions | decision log; interface contracts; in-scope and out-of-scope integrations; integration details and data mapping; mobile/client details; recommendation and rejected alternatives | Mobile or integrations only when the system has none |
| Technology Impacts | assumptions; delivery risks and issues; operations and rollout; cost, licensing, and team impacts; what breaks first | No |
| Data Classifications | data sets and sensitivity; retention and archival; anonymization; normalization; exemptions and technical debt | `n/a — no data is stored or processed` with a reason |
| Next Steps | owned actions, each with a horizon | No |
| Glossary & References | project terms and acronyms; source documents and links | References may state `none` with a reason |
| Appendix — Evidence and open questions | evidence, questions, unknowns, and checks | No |
| Appendix — Architectural debt | coverage and findings | Omit the heading entirely in greenfield |
| Appendix — Critical deep dives | pressure, decision, rejected alternatives, failure mode, evidence | At least one deep dive, or a reason none is needed |
| Appendix — Measurements that could overturn the decision | measurement, threshold, and action if crossed | At least one measurement, or a reason none is falsifiable |
-->

### Section notes

- **Context & Background** states the problem in plain language, then the business objectives and the constraints that bind the design. It carries nothing else and no technology—those live in Solution Design and Technology Impacts.
- **Scope & Requirements** carries in scope, out of scope, and the FR table. Every FR names its source (a PRD story or requirement), and no requirement is added without one. It carries no NFR table, characteristics, estimates, or conflicts; those are design inputs recorded where they change a decision.
- **Solution Design** carries the candidate architecture records. Structure is C4Context plus C4Container; the structure diagrams are the record. There are no per-candidate component, edge-contract, or flow-step tables. C4 container descriptions carry load-bearing state contracts. Critical-flow behavior and dependency contracts live in Key Design Decisions. The current state is Architecture 0 in repository mode; in greenfield it states that no implementation exists and names the prompt constraints that stand in for it. After the candidates, a **Recommended architecture** subsection names the winner, gives its evidence chain, and carries one comparison table listing every option's pros and cons side by side so the reader compares them without moving between sections.

<!-- staged, not yet confirmed:
- **Data Sets & Data Model** carries the entity, consistency, and schema discipline. For each core entity record its representation in memory and at rest, identity scheme, ordering authority, conflict resolution per field class, durability point, and garbage collection or compaction. For each structured store use a human-readable schema card with keys, indexes, relationships, source-of-truth status, and retention; no executable DDL. Data impact names what moves, whether rollback survives writes in the new format, and which records are authoritative.
- **Key Design Decisions** records the decisions a reviewer would challenge. Each row names the alternative that lost and the evidence or constraint that closed it. For each interface record style and transport, trust boundary, deadline, retry owner, backpressure, consistency and idempotency scope, compatibility direction, and caller-visible failure including `UNKNOWN`. Integration details include data mapping and mobile/client behavior. The recommendation rests on evidence.
- **Technology Impacts** separates delivery assumptions and project risks from the first technical failure. Cost, licensing, skills, and rollout are architecture inputs when they constrain the design.
- **Data Classifications** names each data set, its sensitivity, retention, deletion or anonymization rule, normalization rule, and any exemption. Financial, health, and personal data are named explicitly when present.
- **Glossary & References** is project-specific. It is separate from the skill's internal vocabulary below.
-->

<!-- staged, not yet confirmed:
## Appendix — Evidence and open questions

The register lives in the appendix; there is no separate runtime and no byte-hash checkpoint. Record each load-bearing claim as **observed**, **derived**, or **inferred**, with a source locator, scope, and limitations. A content locator identifies evidence; it does not authenticate the source or prove the claim.

### Evidence

| id | claim | type | scope | sources | limitations | freshness |
|---|---|---|---|---|---|---|
| `ev-order-commit` | The handler writes the order before returning success | observed | `src/orders.py` handler | `src/orders.py` | Static inspection does not prove a runtime commit | current |

### Questions

| id | question | status | evidence | answer |
|---|---|---|---|---|
| `q-durability` | When is an order durable? | answered | `ev-order-commit` | After the handler's write; runtime guarantees need a separate check |

### Unknowns

| id | question | status | evidence | resolution |
|---|---|---|---|---|
| `u-restore` | Can the backup meet the recovery target? | open | — | Run and retain a timed restore |

### Checks

| id | check | status | evidence | detail |
|---|---|---|---|---|
| `c-ack` | Inspect the handler's acknowledgement ordering | pass | `ev-order-commit` | Source ordering matches the stated boundary; durability was not tested |

Question status is `open | partial | answered`; unknown status is `open | resolved`; check status is `pass | fail | unknown`. A completed record cites fresh evidence and nonempty result text; the host still judges whether the evidence is sufficient.

**Freshness is a judgment, not a digest.** On resume, re-read the cited sources, including staged, unstaged, and untracked work, then update `freshness` to `current`, `stale`, or `unknown`. Changed or inaccessible evidence invalidates dependent completed records until it is re-established. There is no automatic invalidation, checkpoint, or recovery command; say what was actually re-read rather than claiming a check that did not run. Missing coverage establishes neither absence nor refutation.
-->

## Structure diagrams

The document uses C4 for structure. The constraint catalogue with severities and check types is
[C4/CONSTRAINTS.md](C4/CONSTRAINTS.md); the modeling rules are [C4/RULES.md](C4/RULES.md) and the
Mermaid syntax profile is [C4/PROFILE.md](C4/PROFILE.md). There is no diagram-kind choice and no
flow diagram.

- **High-level view:** one `C4Context` under High-level solution design.
- **Candidate view:** one `C4Container` per candidate.
- **Recorded before the first diagram:**

  ```markdown
  Structure diagram: C4Context + C4Container
  Why: <one line>
  ```

Critical-flow behavior and dependency contracts live in **Key Design Decisions**. Do not add a flow diagram, a step table, or a second structure representation.

Apply the generation gates in [C4/RULES.md](C4/RULES.md#generation-gates) before drawing: title, container admission, typing, one-hop relationships, completeness, then cross-level and cross-candidate checks. After drawing, run the regression in [C4/CONSTRAINTS.md](C4/CONSTRAINTS.md#4-regression-runbook).

Every C4 block carries the scope, level, and legend header:

```text
%% system-in-scope: ticketing
%% c4-level: L1
%% legend: arrows show initiation; blue owned in scope; grey external; boundary means owned lifecycle and data
```

Use `L2` in a candidate container block. The alias and business label are identical in the context and every candidate boundary. The rendered title carries the level and scope:

```text
title Context view - Ticketing system
title Container view - Ticketing system - Candidate A
```

### C4 Golden Rules

1. First statement is `C4Context` (L1) or `C4Container` (L2). Nothing else, no YAML front-matter. `[S1]`
2. Metadata comment block precedes the diagram type: `%% c4-level:`, `%% system-in-scope: <alias>`,
   and `%% legend:` with the arrow convention and ownership rule. `[S1][B1][R5]`
3. **Every text argument is double-quoted**: `System(alias, "Name", "Description")`. `[S4]`
4. **No `,` `(` `)` `"` inside any text argument.** Use `;`, `and`, `/`, ` - ` instead.
   (Mermaid's C4 parser splits on commas and breaks on parentheses.) `[F6]`
5. Aliases: `[A-Za-z][A-Za-z0-9_]{0,31}`, semantic (`paymentsApi`, not `s1`), never a keyword,
   identical across L1 and L2. `[E1][X2]`
6. Statement order: **elements & boundaries → relationships → `UpdateElementStyle`/`UpdateRelStyle` → `UpdateLayoutConfig` (last)**. `[G3]`
7. One statement per line; 2-space indent; LF; no tabs; no trailing whitespace.
8. L1: exactly one non-external `System` (the scope); every other system uses `*_Ext`;
   **no containers, no protocols/technology, no infrastructure**. `[L1][E3][L7]`
9. L2: exactly one top-level `System_Boundary` whose alias == `system-in-scope`; all containers
   inside it; people and external systems outside it; **every container declares a technology**;
   **every relationship declares `<sync|async> <mechanism>`** and a boundary crossing adds
   `; auth=<posture>`. `[B2][B3][R2][R11]`
10. Relationships are one hop, directed, and labelled with a verb phrase from the initiator's
    viewpoint (`"Reads account data from"`), with no step numbers, duplicates, self-loops, or
    temporal connectives. `[R3][R5][R7][S5]`
11. Every element has ≥1 relationship. No orphans. `[C1]`
12. Budget: L1 ≤ 10 elements and ≤ 12 relationships; L2 ≤ 12 containers, ≤ 18 relationships, and
    ≤ 15 total nodes. Over budget → merge non-distinct containers or simplify; never split this
    SAD's one-view-per-candidate contract. `[G1][G2]`
13. Only these style hooks: `UpdateElementStyle`, `UpdateRelStyle`, `UpdateLayoutConfig`.
    **Never** `classDef`, `style`, `linkStyle`, `click`, `subgraph`, `direction`, `-->`.
14. Add `accTitle:` and `accDescr:` when the renderer accepts them; keep the C4 palette. `[F7]`
15. Every internal store has a read and a write edge, or `%% archiveOnly: <alias>; <reason>`. `[C2]`
16. A `Person` must not connect directly to an internal store or worker. An external system
    writing an internal store needs `%% exception: <from> -> <to>; <reason>`. `[R9][R10]`
17. Shared external aliases, labels, and descriptions do not drift between candidates, and no
    alias flips between internal and external. `[V1][X7]`

Full grammar, palette and Mermaid quirks: [C4/PROFILE.md](C4/PROFILE.md).
Constraint IDs and severities: [C4/CONSTRAINTS.md](C4/CONSTRAINTS.md).
Modeling rules: [C4/RULES.md](C4/RULES.md).

## Component kinds

`kind` selects the C4 element in a structure diagram. The same kind list applies to every candidate.

| kind | C4 element | Use for |
|---|---|---|
| `person` | `Person` / `Person_Ext` | End users, browsers |
| `mobile` | `Container` / `Container_Ext` | Mobile apps |
| `service` | `Container` | Stateless app services, monolith modules |
| `gateway` | `Container` | API gateways, edge auth |
| `ws` | `Container` | Persistent-connection gateways |
| `worker` | `Container` | Async workers, consumers |
| `cron` | `Container` | Schedulers, periodic jobs |
| `db-sql` | `ContainerDb` | Relational stores |
| `db-nosql` | `ContainerDb` | KV, wide-row, document stores |
| `db-graph` | `ContainerDb` | Graph stores |
| `cache` | `ContainerDb` | In-memory caches |
| `queue` | `ContainerQueue` | Queues, task buffers |
| `stream` | `ContainerQueue` | Replayable logs, event streams |
| `blob` | `ContainerDb` | Object storage |
| `search` | `ContainerDb` | Search and inverted indexes |
| `ml` | `Container` | Model inference, ranking |
| `ledger` | `ContainerDb` | Append-only financial records |
| `monitor` | `Container` | Observability |
| `external` | `System_Ext` | Third-party APIs |
| `external-db` | `SystemDb_Ext` | Shared data stores you do not own |
| `external-queue` | `SystemQueue_Ext` | Shared brokers you do not own |

Deployment services such as CDN, DNS, or load balancers are not C4 elements. Record them in **Technology Impacts** or **Key Design Decisions**.

A client-side architecture uses the same kinds: `mobile` or `person` for the shell, `service` for a state owner or sync engine, `db-sql`/`db-nosql` for the on-device store, `cache` for an in-memory tier, `queue` for a mutation outbox, `worker` for background refresh.

## Candidate records

Candidate records live under **Solution Design**. Each candidate carries a C4Container structure diagram and a migration note. There is no per-candidate component table, edge table, flow-step table, or flow diagram.

A fact is **load-bearing** when removing it could change topology, failure behavior, cost, or the recommendation, or when a completion invariant depends on it. Put load-bearing state contracts in the C4 container description and dependency contracts in **Key Design Decisions**. Omit everything else.

### Structure

The C4Container diagram is the component record. Its aliases are the component ids; reuse the same container alias for the same component across candidates. Container descriptions carry:

- the component name;
- its technology only when that explains the design;
- in repository mode, `added`, `removed`, or `modified` when it changed; omit the marker when unchanged;
- a plain-language state promise only when the store or view carries an invariant.

`Rel` technology carries `<sync|async> <transport>`; a boundary crossing adds `; auth=<posture>`. Do not put deadlines, retry owners, or backlog bounds in the C4 diagram; they belong in **Key Design Decisions**.

Do not add a component table, an edge-contract table, or a separate state-contract table.

### State contracts

When a load-bearing authoritative store appears in a C4Container diagram, its container description states in one plain business sentence:

- what it stores;
- which acknowledgement is durable;
- which failure it survives;
- how it recovers, including the recovery point and time.

Put implementation terms such as WAL fsync, synchronous standby, and fenced promotion in the technology field, not the description. Do not paste a semicolon-delimited contract into the description.

A load-bearing derived store's description states what it is rebuilt from and how far it has been applied. If a store or view is not load-bearing, omit it from the diagram. Do not put `UNKNOWN` in authoritative lifecycle state: authoritative operations use `PENDING | RECONCILING | SUCCEEDED | FAILED | CANCELLED`; `UNKNOWN` is only the caller's observation after an ambiguous timeout.

### Comparison table

Every candidate's pros and cons live in one table under **Recommended architecture**, with one row per option and a Recommended column. It compares options on stated strengths and weaknesses, not on a number; a score with no derivation is not evidence. Do not scatter per-candidate trade-off paragraphs through the candidate sections. Each candidate still carries at least one honest weakness, stated in the table's Cons column.

**Migration (repo mode)** stays with the candidate because it describes that option's rollout: `S` = one release, no data migration; `M` = staged across a few releases or one bulk migration; `L` = a compatibility path that runs beside the old one. State what data moves and whether rollback survives once users write the new format.

| Option | Pattern | Pros | Cons | Recommended |
|---|---|---|---|---|
| `a` | service-based | every invariant is local; the burst never reaches a writer | one primary; a failover straddles the payment window | **yes** |

<!-- staged, not yet confirmed:
## Appendix — Architectural debt

Repository mode only. The protocol—what counts as debt, the pipeline, categories, severity, and identity—lives in [AUDIT.md](AUDIT.md). This section is the storage format for the debt register. In greenfield, omit the appendix entirely.

### Coverage

```markdown
### Coverage

- **Checked:** boundaries, data-ownership, coupling, dependency-contracts,
  failure-containment, over-engineering, obsolescence.
- **Unverified:** `change history before 2026-01` — shallow clone; nine months available.
```

`Checked` names every category the audit ran, so a category that produced nothing reads as examined rather than skipped. `Unverified` records every check that wanted evidence the run could not reach.

### Findings

Group by category only when the volume earns it. Order by severity, then confidence. Keep open findings first, then accepted findings, then absent findings in their own subsection.

```markdown
#### `dbt-shared-persistence--billing-svc-orders-db` — Billing and fulfilment both write the orders table

| Field | Value |
|---|---|
| Subject | repo |
| Category | data-ownership |
| Pattern | shared-persistence |
| Components | `billing-svc`, `orders-db` |
| Consequence / exposure | breaking / on-path |
| Severity / confidence | blocking / high |
| Evidence | Both map orders as authoritative — `billing/models.py`; `fulfilment/schema.sql` |
| Why it matters | A column added for billing cannot ship until fulfilment has been read and re-tested. |
| Remedy | `consolidate` — one owner writes orders; the other reads a view it does not migrate. Effort `M`; reversible. |
| Blast radius | every migration touching orders |
| Resolved by | `b` |
| Disconfirming | ADR-0004 records the shared table, but for reads only — writes were never decided. |
| Verification | real pass; live pass; lenses: uncovered not refuted ("ADR-0004 covers reads, not writes"); unstated not refuted ("no trade-off is recorded"); tools: repository, change history; survived 2 |
| Status / justification / accepted until | open / — / — |
| First seen / baseline | 2026-08-11 / new |
```

A `note`-shaped finding—an observation with no remedy—omits severity, consequence, and exposure. Severity is looked up from the two axes and never chosen. A finding never carries a numeric score, a debt index, or an estimate in hours or currency.

Identity is `dbt-<pattern>--<sorted component ids>` and nothing else. Read the prior `DESIGN.md` and index every finding by its id and every alias before the finder runs. Carry forward `status`, `justification`, `acceptedUntil`, `firstSeen`, and `aliases` verbatim; regenerate prose, evidence, remedy text, blast radius, and the disconfirming line. `baselineState` is `new | unchanged | updated | absent`, present on every finding or on none.
-->

## Verification

Before the run is complete, check the document directly:

1. Frontmatter parses as YAML and `mode`, `status`, and `decided` are consistent.
2. The confirmed SAD headings appear in the stated order, `Notes` is present, and every confirmed section has content or `n/a — <reason>`.
<!-- staged, not yet confirmed:
3. The debt appendix is present in repository mode and absent entirely in greenfield.
-->
4. The document records `Structure diagram: C4Context + C4Container`. Every Mermaid block is C4, carries `%% system-in-scope:`, `%% c4-level:`, and `%% legend:`, has a title that names the level and scope, and no flow diagram exists.
5. There is exactly one `C4Context` for the document and one `C4Container` per candidate. The context has one scoped `System` and no CDN, protocol, or deployment element. Each C4Container has one business-named `System_Boundary` with the context alias and label, no `Person` or `Container_Boundary` inside it, and no generic `Edge`, `Application`, or `Data` systems. Every C4 alias is declared in that block, and the same container alias names the same component across candidates.
6. Every C4 block passes the text and rendering rules in [C4/PROFILE.md](C4/PROFILE.md): quoted arguments, no commas, parentheses, or HTML, ASCII titles, length limits, and `<sync|async> <transport>` with auth posture at boundaries.
7. Every L2 person and external system exists in L1 with the same alias, label, and description. Every L2 boundary-crossing relationship rolls up to L1, and every L1 relationship touching the scope is realised by at least one candidate in the same direction. No alias flips between internal and external across candidates.
8. Every element has at least one relationship. Every internal store has a read and a write path or `archiveOnly`, no `Person` connects to an internal store or worker, and no external system writes an internal store without a recorded exception.
<!-- staged, not yet confirmed:
9. Key Design Decisions records each load-bearing dependency's deadline, retry owner, and backlog bound, and each critical flow's named durable or final effect. No candidate carries a component, edge-contract, flow-step, or flow diagram.
10. Every evidence, question, unknown, check, and finding reference resolves.
11. Every debt finding has a stable id and the merge fields.
-->
12. Every C4 alias resolves within its block.
<!-- staged, not yet confirmed:
13. Data classifications and glossary terms are present or marked `n/a` with a reason.
-->
14. The document states what was re-read, what was not verified, and which renderer, if any, was used.

Structural checks do not prove the architecture. Semantic review and diagram rendering remain separate results; missing rendering is unknown, not passed.

## ADR on decision (repo mode)

Offer once, when the user picks a winner: `docs/adr/NNNN-<slug>.md` with Title (numbered noun phrase) · Status (Accepted; and `Superseded by NNNN` written back into any ADR this replaces) · Context (the forces, the rejected candidates by name with the reason each lost, and the documents that previously owned this subject) · Decision (affirmative voice: "We will…") · Consequences (the trade-offs accepted, good and bad). Future runs read `docs/adr/` at **Establish the current truth** and do not re-litigate.

## Vocabulary

**Use exactly:** architecture, candidate, component, flow, step, zone, edge, envelope, estimate, characteristic, trade-off, recommendation, finding, debt, severity, remedy, evidence.

**Never substitute:** box, node, block (for component) · path, journey (for flow) · lane, tier, layer (for zone) · option, variant (for candidate — a variant is what fails the distinctness rule) · issue, problem, violation (for finding — a violation names a rule that was broken, which is only one of the seven things a finding can be) · score, rating, grade (for severity — severity is looked up from two axes, and a number implies a precision nothing here has).

Project terms such as CMDB, ITSM, SLA, or a vendor module name belong in **Glossary & References**, not in this internal vocabulary.

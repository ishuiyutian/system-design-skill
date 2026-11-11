# C4 Model Rules (Level 1 & Level 2)

How to draw C4 structure for [SKILL.md](../SKILL.md). The canonical constraints, severities, and
check types are [CONSTRAINTS.md](CONSTRAINTS.md); the Mermaid syntax is [PROFILE.md](PROFILE.md).
A bracketed tag cites the constraint each rule implements.

## Generation gates

Apply these in order before drawing. The level rules below are the detail behind each gate.

1. **Declare one question and one audience.** Put the level and scope in the rendered title.
   Multiple questions need multiple candidates, not one crowded view. `[S2][S3][S4]`
2. **Admit every L2 container.** A container is a steady-state process or an owned persistent
   store, not a transient invocation. `[L2][L3]`
3. **Type every element.** A `Person` is an actor role. External systems use the `*_Ext` form.
   A store uses `ContainerDb` or `ContainerQueue`. `[E1][E3]`
4. **Draw one-hop relationships from the initiator.** At L2 declare invocation mode and mechanism.
   At a boundary add the auth posture. `[R3][R5][R2][R11]`
5. **Run the completeness gates.** No orphans, no store without a read and write path, no worker
   without a result path. `[C1][C2][C3]`
6. **Run the cross-level and cross-candidate gates.** The context is the union of the candidates;
   every candidate is a projection of the same model. `[X1][X2][X3][X4][V1]`
7. **Validate before rendering.** Repair a blocker with its rule ID, offending object, and concrete
   fix. Stop after two rounds and report the remaining violations instead of inventing an edge.
   `[O6][O7]`

## Level 1 — System Context

**Scope:** one software system. **Audience:** everyone, technical and non-technical.
**Question answered:** "What is this system, who uses it, what does it talk to?"

Rules:
- Exactly one **system in scope**, declared as `System(...)`, named in `%% system-in-scope: <alias>`
  and in the title. Record `%% c4-level: L1` beside it. `[S1][L1]`
- Show **people/roles** (not org charts) and **external software systems** — anything you do not
  build/change: SaaS, legacy, mainframe, partner APIs, shared platforms (Kafka, Auth0, Stripe).
  `[L1][E3]`
- "External" means *external to the scope*, not necessarily external to the company.
  Every non-scope system uses an `*_Ext` variant: `System_Ext`, `SystemDb_Ext`, or `SystemQueue_Ext`.
  `[E3]`
- Relationship labels express **intent** in business language: `"Sends payment instructions to"`.
  `[R4]`
- **No** technology, protocols, ports, containers, databases of other systems, replicas,
  load balancers, CDN, DNS, clusters, regions. Those are L2 or deployment concerns. When they are
  load-bearing, record them in **Technology Impacts** or **Key Design Decisions**, not in C4.
  `[L1][L7]`
- An `Enterprise_Boundary` may group systems owned by the enterprise; keep nesting to one level.
  `[B2]`
- Budget ≤ 10 elements and ≤ 12 relationships. This SAD keeps exactly one `C4Context`; when
  the budget is exceeded, remove the elements that cannot change the design rather than adding
  a second context diagram. `[G1][G2]`

## Level 2 — Container

**Scope:** the same system, zoomed in. **Audience:** technical people inside and outside the team.
**Question answered:** "What are the separately deployable/runnable pieces and how do they talk?"

A **container** is something that must be running/deployed for the system to work, or a data store:
web app, SPA, mobile app, API application, worker, serverless function (if separately deployed),
database, schema-less store, blob/file store, search index, self-hosted broker.
A container is **not** a class, module, package, layer, or a Kubernetes pod/replica.

Rules:
- Exactly one top-level `System_Boundary(alias, "Name")`, alias == L1 scope alias, label == L1 system label.
  Record `%% system-in-scope: <alias>` and `%% c4-level: L2` in the block. `[S1][B2][X3]`
- All containers inside it; all people and external systems outside it. External systems are black
  boxes: use `System_Ext`, `SystemDb_Ext`, or `SystemQueue_Ext` — never their internals. `[B3]`
- Every container: **name + technology + responsibility**. Technology is concrete
  (`"Java 21 and Spring Boot 3"`, `"PostgreSQL 16"`, `"React 18"`), not `"backend"`. `[E1][F2]`
- Every relationship: **intent + `<sync|async> <mechanism>`**
  (`Rel(api, db, "Reads and writes data", "sync SQL")`), with `; auth=<posture>` added when the
  relationship crosses the scope or a named trust boundary. `[R2][R11][D2]`
- Data stores → `ContainerDb`; queues/topics → `ContainerQueue`. A shared broker you do not own
  for this system alone is an external `SystemQueue_Ext`. `[E3]`
- Keep the context relationships from L1 that reach the containers; drop the rest. `[X4]`
- No components, no code, no deployment nodes, no nested boundaries. Do not use
  `Container_Boundary`, `Boundary`, `C4Component`, or `C4Deployment`. Budget ≤ 12 containers,
  ≤ 18 relationships, and ≤ 15 total nodes, with boundary-crossing relationships ≤ 6 as a
  readability target. This SAD keeps one `C4Container` per candidate; when the budget is
  exceeded, merge non-distinct containers or simplify the candidate rather than adding a
  second container diagram. `[L6][L7][B2][G1][G2]`

## Container admission and demotion

A container earns its box with one of two tests: `[L2]`

- a **steady-state process** visible in `ps` while the system is serving; or
- an **owned persistent store** the system depends on.

A transient invocation is not a container: a CLI spawned per call, a bundled binary, a library,
an adapter inside another process, a module, a package, a layer, a pod, or a replica. A scheduler or
resident worker that survives between runs is a process; a one-shot batch job is not. `[L3]`

Cluster data stores by `(technology, volume/root, owner process, lifecycle)`; identical stores are
one container, and splitting one store requires a recorded exception naming the distinguishing
attribute. `[L4]`

If an element fails admission, fold it into its parent container's responsibility or record it in
Key Design Decisions or Technology Impacts. This SAD has no L3 component view, so never demote it to
a `C4Component` or a component table. `[L3]`

## Relationship contract

- **One edge is one hop.** Do not compress a multi-hop path into one arrow; split it. `[R3]`
- **Direction follows initiation or dependency**, declared in the block's `%% legend:` line. Do not
  mix request direction and data-return direction silently. `[R5]`
- At L2 the technology field is `<sync|async> <mechanism>`. The mechanism is one value from the
  closed list in [PROFILE.md](PROFILE.md#mechanism-vocabulary). `[R2]`
- A boundary-crossing relationship adds `; auth=<posture>`. `none public` is a posture; silence is
  not. `[R11][D2]`
- The label is an intent verb phrase plus object. Do not use unqualified `uses`, `talks to`,
  `communicates with`, `interacts with`, `connects to`, `handles`, or `sends data`. `[R4]`
- A `Person` must not connect directly to an internal data store or background worker. An external
  system must not connect directly to an internal data store without a recorded
  `%% exception: <from> -> <to>; <reason>` line. `[R9][R10]`
- No duplicate relationship, no self-loop, no numbered step, and no temporal connective such as
  `then`, `after`, `first`, or `next`. Sequence belongs to Key Design Decisions, not the static view.
  `[R7][S5]`
- Each relationship is backed by Key Design Decisions or the evidence register. Mark an unproven
  relationship as assumed; never add an edge just to satisfy a completeness check. `[R1][P1][P4]`

## Cross-level consistency

This SAD has one `C4Context` and one `C4Container` per candidate. The context is therefore the
union of the context relationships the candidates need, not a claim that every candidate realises
every relationship. `[X1]`

| Contract | Rule |
|---|---|
| Same scope alias and label in the context and every candidate boundary | `[X3]` |
| Every L2 person/external system exists in L1 with the identical alias **and** label | `[X2]` |
| Every L1 relationship touching the scope is realised by ≥1 candidate's L2 boundary-crossing relationship, in the same direction | `[X4]` |
| Every L2 boundary-crossing relationship in any candidate rolls up to an L1 relationship | `[X1]` |

A candidate may omit a context relationship it does not implement. It may not invent a
boundary-crossing relationship that the context does not carry.

## Cross-candidate contract

Every candidate is a projection of one model, not a fresh drawing. `[X1]`

- Shared external elements have the identical alias, label, and description in the context and
  every candidate. Invariant elements do not drift between candidates. `[V1]`
- No alias is internal in one candidate and external in another. `[X7]`
- Every L1 external system that touches the scope appears in at least one candidate. `[X4]`
- Every candidate records the decision-relevant delta against the recommended baseline and passes
  the same constraints. A variant may not relax a correctness rule to look simpler. `[V2][V4]`
- All candidates use the same scope alias and boundary label and stay within the same budgets. `[X3][G1]`

## Completeness gates

- No orphan elements: every element has at least one relationship in its block. `[C1]`
- Every internal data store has at least one inbound read and one inbound write, or a
  `%% archiveOnly: <alias>; <reason>` line. `Reads and writes` on one edge satisfies both. `[C2]`
- Every worker or service with an inbound dispatch has a result path: an outbound result edge, or a
  write to a store that a path back to the user reads. `[C3]`
- Every capability verb in a user-facing element's description maps to at least one edge. `[C4]`
- Every external dependency named in the design appears with at least one edge. If a technical noun
  is deliberately not a C4 element, name it in Key Design Decisions or Technology Impacts rather
  than dropping it silently. `[C5][C6]`
- A store shown in a candidate is source-of-truth or derived; a derived store names its
  reconstruction source and cursor. `[C7]`

## Naming conventions

- Alias: semantic camelCase, stable identifier, never renamed between levels. `[E1]`
- Label: responsibility-based Title Case name, ≤ 4 words and ≤ 40 chars, not a bare technology
  name, no unexplained acronyms. `[E4][F4]`
- Technology: a product, runtime, protocol family, or store type, not a bare role such as
  `service`, `worker`, or `store`. `[F2]`
- Description: one sentence, "who/what + responsibility", ≤ 24 words and ≤ 140 chars, no marketing
  language, schema terms, paths, call mechanisms, or implementation detail. An authoritative store
  may add one plain-language state-contract sentence covering acknowledgement, failure domain,
  RPO/RTO, or reconstruction source. `[F1][F4]`
- Relationship: third-person verb phrase from the initiator's perspective, ≤ 8 words and ≤ 60 chars,
  no numbers (`"1. Submit order"` belongs in Key Design Decisions, not the static view). `[R4][S5]`

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| "API Gateway", "Load Balancer", "Kubernetes" as L1 systems | Remove; deployment concern `[L1][L7]` |
| CDN, DNS, or a load balancer as a C4 element | Record it in Technology Impacts or Key Design Decisions; it is a deployment concern `[L7]` |
| Shared Kafka drawn as a container of your system | External system (`SystemQueue_Ext`) unless you own/run it for this system only `[E3]` |
| L2 boundary contains `Person` | Move outside the boundary `[B3]` |
| Container without technology | Add the 3rd argument `[E1][F2]` |
| L1 arrows labelled `"HTTPS/JSON"` | Move protocol to L2 `[L1]` |
| One diagram with 30 boxes | Simplify the load-bearing set; this SAD keeps one context and one container view per candidate `[G1][G2]` |
| Bidirectional arrow to hide unclear direction | Two explicit, labelled relationships `[R5]` |
| Different names for the same system across levels | Reuse the alias + label from the model `[X2][X3]` |
| Per-call CLI or library drawn as a container | Fold it into the parent process or record it in Key Design Decisions; there is no L3 view `[L3]` |
| `Person` reads an internal database directly | Put a service or read API on the path; people do not connect to internal stores `[R9]` |
| A store with no read or write edge | Draw the missing path or mark it `archiveOnly` with a reason `[C2]` |
| An external system writes an internal store directly | Route it through an owned interface or record a justified exception `[R10]` |
| A boundary-crossing arrow with no auth posture | Add `auth=<posture>` or state `none public` `[R11]` |
| A duplicate or self-loop relationship | One edge per ordered pair; no self-loops `[R7]` |
| A title that names no level or scope | Use the profile title format `[S3][S4]` |

## Review checklist

The L checks cover structure; these questions are the R-checked constraints in
[CONSTRAINTS.md](CONSTRAINTS.md) and cannot be settled by a syntax check.

1. Is the scope really **one** system, or a whole product portfolio? `[S2]`
2. Would a non-technical stakeholder understand L1 without a legend explanation? `[S2]`
3. Is every L2 box independently deployable/runnable, or is it a module in disguise? `[L2]`
4. Does every arrow point in the direction of **intent** (who initiates), not data return flow? `[R5]`
5. Are failure/async paths that matter architecturally visible (queues, retries, callbacks)? `[C7]`
6. Are assumptions explicitly listed rather than silently baked in? `[P3]`
7. Does the L2 diagram change any decision a reader would make from L1? If not, is it needed? `[S2]`
8. Does the legend state the arrow convention and the ownership rule? `[B1]`
9. Is every element and relationship backed by evidence or marked assumed? `[P1][P5]`
10. Does each candidate differ on a load-bearing axis and record its delta? `[V2]`
11. Is every edge label interpretable without external conversation? `[R12]`
12. Did any check get satisfied by inventing an edge or deleting a required read path? `[P4]`

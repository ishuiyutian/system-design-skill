# Provenance — C4 model rules

Sources for [C4/RULES.md](../../../skills/system-design/C4/RULES.md). The modeling rules adapt the C4 model to this skill's single-document, multi-candidate SAD; the thresholds and the multi-candidate rule are product decisions and are recorded as such.

## Generation gates

| Claim | Source |
|---|---|
| Generation is ordered scope/title, container admission, typing, one-hop relationships, completeness, cross-level, then validation | Product decision: the order prevents a later check from being satisfied by inventing an element or edge. |
| A blocker is repaired with its rule ID, offending object, and concrete fix, with at most two repair rounds | Adapted from `C4/CONSTRAINTS.md` O4 and O7; product decision for the skill's contract-test loop. |
| JSON-first output, dynamic views, component views, deployment views, and multi-diagram splitting are out of scope | Product decision and repository invariant: `DESIGN.md` is the only artifact and structure is one C4Context plus one C4Container per candidate. The rejected constraints are recorded in `C4/CONSTRAINTS.md` so they are not quietly reintroduced. |

## Level 1 — System Context

| Claim | Source |
|---|---|
| A system context view has one system in scope, its people, and the external software systems it depends on | [C4 model — System Context diagram](https://c4model.com/diagrams/system-context) (checked 2026-11-12) |
| External systems are black boxes and every non-scope system carries an `*_Ext` variant | [C4 model — System Context diagram](https://c4model.com/diagrams/system-context) (checked 2026-11-12) |
| Context relationships express intent, not protocol or technology | [C4 model — System Context diagram](https://c4model.com/diagrams/system-context) and [Mermaid C4 syntax](https://mermaid.js.org/syntax/c4.html) (checked 2026-11-12) |
| CDN, DNS, load balancers, clusters, regions, and other deployment infrastructure are not context elements | Product decision: deployment detail is recorded in Technology Impacts or Key Design Decisions so the context stays a business view. |
| The context budget is at most ten elements and twelve relationships | Product decision: a wall chart stops being a context view; the load-bearing set is what survives. The stricter limit comes from the source constraint G1 and is enforced by the contract test. |
| This SAD keeps one `C4Context` and simplifies it rather than splitting it | Product decision: the document contract requires one high-level view per SAD. |

## Level 2 — Container

| Claim | Source |
|---|---|
| A container is a separately runnable or deployable unit, or a data store; it is not a module, package, layer, or replica | [C4 model — Container diagram](https://c4model.com/diagrams/container) (checked 2026-11-12) |
| The container view has one top-level `System_Boundary` whose alias and label match the context scope | Product decision: cross-level identity must survive the context-to-container zoom. |
| Containers sit inside the boundary; people and external systems sit outside it as black boxes | [C4 model — Container diagram](https://c4model.com/diagrams/container) (checked 2026-11-12) |
| Every container declares a name, a concrete technology, and a responsibility | [C4 model — Container diagram](https://c4model.com/diagrams/container) (checked 2026-11-12) |
| Every relationship declares intent and `<sync|async> <transport>`, with auth posture at a scope crossing | Product decision: the skill needs the invocation mode and trust boundary to reason about failure and capacity without putting deadlines in the diagram. |
| Shared brokers not owned for this system alone are `SystemQueue_Ext`; shared stores are `SystemDb_Ext` | Product decision: ownership is the boundary the diagram must make visible. |
| The container budget is at most twelve containers, eighteen relationships, and fifteen total nodes, with boundary crossings above six treated as a readability warning | Product decision: a container view beyond that is usually a module inventory or a candidate that needs simplifying. The stricter limits come from the source constraint G1 and are enforced by the contract test. |
| No components, deployment nodes, or nested boundaries | [C4 model — Container diagram](https://c4model.com/diagrams/container) and [Mermaid C4 syntax](https://mermaid.js.org/syntax/c4.html) (checked 2026-11-12); the skill keeps only context plus containers. |
| This SAD keeps one `C4Container` per candidate and simplifies rather than splitting a candidate | Product decision: candidates must remain directly comparable. |

## Container admission and demotion

| Claim | Source |
|---|---|
| A container is a steady-state process or an owned persistent store, and a transient invocation is not a container | [C4 model — Container diagram](https://c4model.com/diagrams/container) for the deployment-unit test; the steady-state process test is a product decision that prevents per-call CLIs and libraries from becoming boxes. |
| Data stores cluster by technology, volume/root, owner process, and lifecycle; splitting one store needs a recorded exception | Product decision: duplicate stores at the same lifecycle point are one container and inflate the view without changing the architecture. |
| A failed admission is folded into its parent or recorded in Key Design Decisions; this SAD has no L3 component view | Product decision: the skill keeps only context and container views, so component demotion would be an out-of-scope representation. |

## Relationship contract

| Claim | Source |
|---|---|
| One relationship is one hop and direction follows initiation or dependency | [C4 model — Notation](https://c4model.com/diagrams/notation) for the relationship semantics; product decision to forbid compressed multi-hop arrows. |
| L2 technology is `<sync|async> <transport>`; boundary crossings add `auth=<posture>` | [C4 model — Container diagram](https://c4model.com/diagrams/container) for technology; product decision for the closed transport list and the auth-posture field so failure and trust boundaries stay testable. |
| A Person must not connect directly to an internal store or worker, and an external system needs an exception to write one | Product decision: a person-to-store edge hides the owned interface that enforces access and failure behavior. |
| Duplicate relationships, self-loops, numbered steps, and temporal connectives are not static-view content | Product decision: sequence belongs in Key Design Decisions and a duplicate edge is a design claim, not formatting noise. |
| Every relationship is backed by Key Design Decisions or the evidence register, and an unproven edge is marked assumed | Adapted from `C4/CONSTRAINTS.md` P1-P5; product decision: a completeness check must never be satisfied by an invented edge. |

## Cross-level consistency

| Claim | Source |
|---|---|
| The context and every candidate boundary share the same scope alias and label | Product decision: X3 makes the zoom traceable. |
| Every L2 person or external system exists in L1 with the same alias and label | Product decision: X2 prevents the container view from inventing context. |
| Every L2 boundary-crossing relationship is represented in L1 | Product decision: X1 prevents a candidate from depending on an unrecorded external interaction. |
| Every L1 relationship touching the scope is realised by at least one candidate, not every candidate | Product decision: this SAD has one context and several candidate containers; the context is their union, so X4 is evaluated at document level. This is the deliberate adaptation of the single-view C4 consistency rule to a multi-candidate design document. |

## Cross-candidate contract

| Claim | Source |
|---|---|
| Shared external elements keep the same alias, label, and description across the context and every candidate | Product decision: a candidate is a projection of one model, and drifting identity makes the comparison unreliable. |
| No alias is internal in one candidate and external in another | Product decision: ownership is a property of the system, not of a candidate. |
| Every L1 external that touches the scope appears in at least one candidate, and every candidate records its delta | Product decision: the context is the union of the candidates, while each candidate still has to explain its load-bearing difference. |

## Completeness gates

| Claim | Source |
|---|---|
| Every element has at least one relationship | [C4 model — Notation](https://c4model.com/diagrams/notation) for connected elements; product decision to make an orphan a blocker. |
| Every internal store has an inbound read and write path or an `archiveOnly` marker | Adapted from `C4/CONSTRAINTS.md` C2; product decision: a store with no write path is dead weight and a store with no read path is not serving the design. |
| Every worker with an inbound dispatch has a result path | Adapted from `C4/CONSTRAINTS.md` C3; product decision: a dispatch with no result is an unobserved failure. |
| Every external dependency named in the design appears, and a deliberately omitted technical noun is recorded in Key Design Decisions or Technology Impacts | Adapted from `C4/CONSTRAINTS.md` C5-C6; product decision: silent drops are how the diagram stops matching the design. |

## Naming conventions

| Claim | Source |
|---|---|
| Aliases are semantic camelCase and stable across levels | Product decision: stable identifiers let cross-level checks and resume logic find the same component. |
| Labels are Title Case and no longer than forty characters | Product decision: Mermaid C4 auto-wraps and long labels make the diagram unreadable. |
| Descriptions are one sentence and no longer than one hundred forty characters | Product decision: the diagram is a map, not a specification. |
| Relationship labels are third-person verb phrases no longer than sixty characters and carry no numbers | [C4 model — Notation](https://c4model.com/diagrams/notation) for intent; product decision for the length and no-number rule so numbering stays in a Dynamic view. |

## Anti-patterns

| Claim | Source |
|---|---|
| API gateways, load balancers, Kubernetes, CDNs, and DNS are deployment concerns, not context systems | [C4 model — System Context diagram](https://c4model.com/diagrams/system-context) and product decision for this SAD's deployment-detail separation. |
| A shared Kafka belongs to the context as an external queue unless this system owns and runs it alone | Product decision: ownership is what makes a queue a container of this system. |
| A `Person` inside the container boundary is a level error | [C4 model — Container diagram](https://c4model.com/diagrams/container) (checked 2026-11-12) |
| A container without technology is under-specified | [C4 model — Container diagram](https://c4model.com/diagrams/container) (checked 2026-11-12) |
| Context arrows labelled with protocols are a level error | [C4 model — System Context diagram](https://c4model.com/diagrams/system-context) (checked 2026-11-12) |
| One diagram with thirty boxes should be simplified | Product decision: the element budgets enforce the simplify point, and this SAD keeps one context and one container view per candidate. |
| A bidirectional arrow hides unclear direction; use two explicit relationships | Product decision: direction is a design claim, and a bidirectional arrow erases it. |
| The same system must use the same alias and label across levels | Product decision: renaming across levels makes the zoom untraceable. |

## Review checklist

| Claim | Source |
|---|---|
| The review questions are the R-checked constraints (S2, B1, B5, R5, R12, C5, C7, D4, G2, P4, P5, V3) plus a few structural probes, and cannot be settled by a syntax check | Product decision: scope, audience comprehension, deployability, direction, failure visibility, assumptions, decision value, legend clarity, provenance, candidate delta, and anti-gaming require a review gate. |

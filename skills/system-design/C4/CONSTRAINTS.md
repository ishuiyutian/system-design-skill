# C4 Constraints

Constraint catalogue for the structure step in [SKILL.md](../SKILL.md). The modeling rules are
[RULES.md](RULES.md); the Mermaid syntax is [PROFILE.md](PROFILE.md).

## Scope in this skill

This skill draws only **Level 1 (context)** and **Level 2 (container)** views as Mermaid
`C4Context` / `C4Container` blocks inside a single `DESIGN.md`. There is no JSON model, no renderer
pipeline, and no component, dynamic, or deployment view. Each constraint below is therefore
**Enforced** (applies as written), **Adapted** (applies, but is realized through a Mermaid or
`DESIGN.md` mechanism named here), or **Retired** (does not apply to this skill's artifact).

| IDs | Status | Realization |
|---|---|---|
| S1, S3, S5, L1, L6, L7, E1, E3, E5, E6, B1, B3, R3, R4, R7, R8, R9, R10, C1, C2, C3, F6, X1, X2, X4, X7, V1, V4 | Enforced | Mermaid block |
| S2, S4, S6, L2, L3, L4, E2, E4, B2, B4, R1, R2, R5, R11, R12, C4, C5, C6, C7, F1, F2, F3, F4, F5, G1, G2, G3, D1, D2, D3, D4, D5, P1, P2, P3, P4, P5, V2, V3, O6, O7 | Adapted | see notes below |
| L5, L8, X5, X6, T1, T2, T3, T4, O1, O2, O3, O5 | Retired | out of scope |

Adapted realization notes:

- **S2** purpose/audience: one question per block, stated in the H1 and the section prose.
- **S4** title: `Context view - <System>` / `Container view - <System> - <Candidate>`, ASCII hyphen (the em dash is non-ASCII and breaks the profile).
- **S6** `accDescr` describes structure; the dynamic half is retired with T.
- **L2** admission: the `admission` field becomes the container admission test plus a Key Design Decisions justification.
- **L3** demotion: fold into the parent container or record in Key Design Decisions; this SAD has no L3 view.
- **L4** store clustering: one container per `(technology, volume/root, owner process, lifecycle)`; the exception is recorded in Key Design Decisions.
- **E2/E4** Person role / responsibility-based names: naming conventions in `RULES.md`.
- **B2/B4** boundary label carries the system name; locality is stated in the `%% legend:` line.
- **R1/P1** provenance: carried by the evidence register and an assumptions list, not a per-edge field.
- **R2** transport: realized as `<sync|async> <mechanism>` with the closed mechanism list in `PROFILE.md`.
- **R5** arrow convention: the `%% legend:` line declares initiation/dependency.
- **R11/D2** auth posture: `; auth=<posture>` on scope-boundary and named trust-boundary crossings.
- **R12** glossary: `DESIGN.md` Glossary & References.
- **C4/C5/C7** capability verbs, external dependencies, producer paths: review-gate checks.
- **C6** coverage ledger: demotions are named in Key Design Decisions or Technology Impacts.
- **F1** description: responsibility verbs plus at most one plain-language state-contract sentence for an authoritative store; no schema, path, or call mechanism.
- **F2** technology: product/runtime or store type plus load-bearing implementation terms; no marketing names.
- **F3** version: omit the version unless a manifest or lockfile proves it.
- **F4** length: label ≤ 4 words/40 chars, edge label ≤ 8 words/60 chars, description ≤ 24 words/140 chars.
- **F5** legend: arrow convention and ownership rule; element types and abbreviations as used.
- **G1** budgets: context ≤ 10 elements/12 edges; container ≤ 12 containers/18 edges/15 nodes; boundary crossings ≤ 6 target.
- **G2** over budget: merge or simplify; this SAD keeps one view per candidate and never splits.
- **G3** layout: declaration order plus `UpdateLayoutConfig` last.
- **D1** PII: the Data Classifications section names each store's data sensitivity.
- **D3** HTTPS on loopback needs a stated certificate mechanism, otherwise HTTP.
- **D4** security controls are not invented; `UNKNOWN` becomes an open question in the evidence register.
- **D5** retention/encryption claims live in notes or an ADR, not element descriptions.
- **P2/P3** unknown facts and assumptions are surfaced in the evidence register.
- **P4** anti-gaming: a completeness check may not be satisfied by inventing an edge.
- **P5** invariants trace to a requirement, not model inference.
- **V2** delta: each candidate's prose states the decision-relevant delta against the baseline.
- **V3** comparison: ratings plus trade-offs prose is the comparison table; ratings are not evidence.
- **O6** unsatisfiable constraints are reported, never silently dropped.
- **O7** repair feedback is rule ID + offending object + concrete fix.

## 1. Notation & Severity

**Check type**

| Tag | Meaning |
|---|---|
| `L` | Machine-checkable by the validator |
| `R` | Requires a review gate (LLM critic or human) |

**Severity**

| Tag | Meaning |
|---|---|
| `B` | Blocker — render forbidden |
| `M` | Major — must fix or file an exception |
| `m` | Minor |

All statements are **MUST** unless explicitly marked **SHOULD**.

---

## 2. Constraint Catalog

### S — Scope & Purpose

| ID | Constraint | Check | Severity |
|---|---|---|---|
| S1 | Exactly one `level ∈ {context, container, component, dynamic, deployment}` and one `systemInScope` per diagram. | L | B |
| S2 | The diagram MUST answer one declared question (`purpose` field) for one declared audience. Multiple questions → multiple diagrams. | R | M |
| S3 | Level and scope MUST appear in the rendered title. Metadata in `%%` comments does not satisfy this. | L | B |
| S4 | Title format: `"<Level> view — <SystemName>[ — <Variant>]"`. | L | M |
| S5 | Static views MUST NOT contain step numbers or temporal connectives (`then`, `after`, `first`, `next`). Sequence belongs to a dynamic view. | L | M |
| S6 | `accDescr` MUST describe structure for static views, flow for dynamic views — not the other way round. | R | m |

### L — Level Purity (admission)

| ID | Constraint | Check | Severity |
|---|---|---|---|
| L1 | **Context:** exactly one internal system box; all other elements are persons or external systems. No containers, components, data stores of the scoped system, technology fields, or protocols on edges. | L | B |
| L2 | **Container admission:** every container declares `admission ∈ {steady_state_process, owned_data_store}` with justification. Test: visible in `ps` at steady state, **or** a persistent store the system depends on. | L | B |
| L3 | Transient invocations (spawned-per-call CLI, bundled binaries, libraries, adapters) are **not** containers → demote to L3 components. | L | B |
| L4 | Data stores cluster by `(technology, volume/root, ownerProcess, lifecycle)`. Identical quadruple → one container. Splitting requires an `exceptions[]` entry naming the distinguishing attribute. | L | B |
| L5 | **Component:** exactly one container in scope, decomposed. Components are non-deployable functional groupings with interfaces. Other containers appear as unexpanded context. | L | B |
| L6 | Code-level artifacts (classes, functions, files, tables, columns) MUST NOT appear at L1–L3. | L | B |
| L7 | Deployment nodes (VM, pod, region, server, device) MUST NOT appear in context/container/component views. | L | B |
| L8 | L4 SHOULD NOT be produced; if produced it MUST be generated from source, never hand-authored. | R | m |

### E — Element Typing & Identity

| ID | Constraint | Check | Severity |
|---|---|---|---|
| E1 | Every element has `id` (stable, unique, machine-safe), `type`, `name`, `description`. IDs are stable across all views and variants. | L | B |
| E2 | `Person` = a human actor **role**, not an organization, not a named individual, not a job title. | L | M |
| E3 | Element type MUST match its C4 semantics: data store → `ContainerDb`/`SystemDb_Ext`; software outside ownership → `System_Ext`. No generic boxes. | L | B |
| E4 | Names are responsibility-based. A name MUST NOT be only a technology name (`React`, `SQLite`); technology goes in the `technology` field. | L | M |
| E5 | No duplicate display names within a diagram. | L | M |
| E6 | The scoped system MUST be decomposed at L2, never shown as a single opaque box inside its own boundary. | L | B |

### B — Boundaries & Ownership

| ID | Constraint | Check | Severity |
|---|---|---|---|
| B1 | Internal vs external is decided by **ownership of lifecycle + data**, and this rule MUST be stated in the legend. Apply it uniformly. | R | B |
| B2 | Exactly one system boundary at L2; nesting depth ≤ 1. Enterprise/deployment/trust nesting belongs to other view types. | L | M |
| B3 | No external element inside the boundary; no internal element outside it. | L | B |
| B4 | Boundary label MUST carry the system name, and MUST state locality if all containers are co-located (e.g. "all containers run on the learner's machine"). | L | M |
| B5 | If containers span machines or trust zones, the diagram MUST reference a deployment view; locality MUST NOT be left ambiguous. | R | B |

### R — Relationships

| ID | Constraint | Check | Severity |
|---|---|---|---|
| R1 | Every relation has `source`, `target`, `label`, `transport`, `provenance`. | L | B |
| R2 | `transport` MUST be a single value from a closed enum `{HTTP, HTTPS, HTTP Range, gRPC, WebSocket, IPC, SQL, filesystem, in-process, AMQP, ...}`. Two enum hits in one label (`HTTP Range over filesystem`) = violation. | L | B |
| R3 | One edge = one hop. Compressed multi-hop paths are forbidden; split them. | L | B |
| R4 | Label = intent verb phrase + object. Banned unqualified verbs: `uses`, `talks to`, `communicates with`, `interacts with`, `connects to`, `handles`, `sends data`. | L | M |
| R5 | Declare one `arrowConvention` (default: **initiation/dependency**) and make every label read correctly source→target under it. Do not silently mix data-flow and request direction. | R | B |
| R6 | Static views: one edge per ordered pair, or `BiRel` when both directions are architecturally significant. Directed request/response pairs belong to dynamic views. | L | m |
| R7 | No semantically duplicate edges; no self-loops at L1/L2. | L | M |
| R8 | Both endpoints MUST exist in the same diagram. | L | B |
| R9 | A `Person` MUST NOT connect directly to an internal data store or background worker. | L | B |
| R10 | An external system MUST NOT connect directly to an internal data store without an explicit, justified integration exception. | L | M |
| R11 | Every boundary-crossing edge MUST declare transport **and** auth posture (`none — loopback only` is acceptable; silence is not). | L | M |
| R12 | Every edge label MUST be interpretable without external conversation. Undefined domain jargon requires a glossary entry. | R | M |

### C — Completeness & Correctness Invariants

| ID | Constraint | Check | Severity |
|---|---|---|---|
| C1 | No orphan elements: degree ≥ 1. | L | B |
| C2 | Every data store has ≥ 1 inbound write **and** ≥ 1 inbound read, or is explicitly marked `archiveOnly` with justification. | L | B |
| C3 | Every worker/service with an inbound dispatch has a result path: an outbound result edge, or a write to a store that is read by a path back to the user. | L | B |
| C4 | Every capability verb in a user-facing element's description maps to ≥ 1 edge. "Shows history" without a read edge = violation. | L | M |
| C5 | Every external dependency mentioned in the source (including model/artifact hosts, license servers, telemetry) appears with ≥ 1 edge. | R | M |
| C6 | **Coverage ledger:** every technical noun in the source appears in `elements[]` or `demoted[]`; each demoted item names a `destination`. No silent drops, no illegal promotions. | L | B |
| C7 | Data consumed by a declared behavior MUST have a declared producer and a reachable path to the consumer. | R | B |

### F — Field Content & Grammar

| ID | Constraint | Check | Severity |
|---|---|---|---|
| F1 | `description` = responsibility verb phrases, or `Stores <data nouns>` for stores. Banned in this field: version numbers, quantization/implementation specs, call mechanisms (`spawn`, `stdout`, `pipe`), schema terms (`column`, `pointer`, `table`), business invariants (`exactly one per line`), directory/path names. | L | B |
| F2 | `technology` = product/runtime name + optional **major** version. No minor/patch, no wrapper-package versions, no marketing names. | L | M |
| F3 | Version claims MUST be verifiable against a manifest/lockfile; otherwise omit the version. Never guess. | L | B |
| F4 | Length caps: name ≤ 4 words, edge label ≤ 8 words, description ≤ 14 words. | L | m |
| F5 | A legend MUST exist covering: element types used, arrow convention, ownership rule, abbreviations. If the renderer cannot draw it, it MUST ship as an adjacent block. | L | M |
| F6 | No secrets, credentials, tokens, real hostnames/IPs, or personal names anywhere in the artifact. | L | B |
| F7 | Accessibility: `accTitle` + `accDescr` present and non-empty. | L | m |

### G — Budget & Readability

| ID | Constraint | Check | Severity |
|---|---|---|---|
| G1 | Context ≤ 10 elements / 12 edges. Container ≤ 12 containers / 18 edges / 15 total nodes. Component ≤ 12 components. Dynamic ≤ 12 steps. | L | M |
| G2 | Over budget → merge or split into multiple views. Reducing semantics or font size to fit is forbidden. | R | M |
| G3 | Layout config MUST be set explicitly; element ordering MUST be deterministic for diffability. | L | m |
| G4 | SHOULD keep boundary-crossing edges ≤ 6; more indicates a missing intermediate view. | R | m |

### X — Cross-View Consistency

| ID | Constraint | Check | Severity |
|---|---|---|---|
| X1 | All views are projections of one canonical model. No view-local ad-hoc elements. | L | B |
| X2 | An element's `id`, `type`, `name`, `technology` are identical across every view. | L | B |
| X3 | L1 system name == L2 boundary label system name. | L | M |
| X4 | Every L1 external system that interacts with the scoped system reappears at L2. | L | M |
| X5 | Each L3 diagram has exactly one parent container that exists at L2. | L | B |
| X6 | **Refinement closure:** any L3 edge crossing container boundaries MUST correspond to an L2 edge between those containers; any dynamic step MUST map to an existing static edge or add it. | L | B |
| X7 | No element is internal in one view and external in another. | L | B |

### D — Deployment, Trust & Security

| ID | Constraint | Check | Severity |
|---|---|---|---|
| D1 | Every store declares `pii ∈ {true,false,unknown}`; `true` requires a data-category note. | L | M |
| D2 | Every edge crossing a process, machine, or ownership boundary declares authn/authz posture. | L | M |
| D3 | `HTTPS` on loopback requires a stated certificate mechanism; otherwise use `HTTP`. | L | M |
| D4 | Security controls MUST NOT be invented; absent evidence, mark `UNKNOWN` and raise an open question. | R | B |
| D5 | Retention/encryption claims belong to notes or ADRs, not to element descriptions. | L | m |

### T — Dynamic Views

| ID | Constraint | Check | Severity |
|---|---|---|---|
| T1 | Steps are numbered, ordered, one initiator each, and reference existing element IDs. | L | B |
| T2 | Every step maps to an edge in a static view, or that edge is added to the static model in the same change. | L | B |
| T3 | Branches and loops MUST use explicit labeled notation, not prose inside a label. | L | M |
| T4 | A dynamic view declares its triggering scenario and terminal outcome(s), including failure paths. | R | M |

### P — Provenance & Anti-Hallucination

| ID | Constraint | Check | Severity |
|---|---|---|---|
| P1 | Every element, edge, and technology claim carries `provenance` (source span/ID) **or** is tagged `assumption` with rationale. | L | B |
| P2 | Unknown facts are `UNKNOWN` + an entry in `openQuestions[]`. Guessing is forbidden. | L | B |
| P3 | Assumptions MUST be surfaced in a visible list, never buried in comments. | L | M |
| P4 | **Anti-gaming:** completeness rules (C2–C4) may only be satisfied by edges with provenance. Inventing an edge to pass the linter is a blocker violation. | R | B |
| P5 | Every declared invariant or constraint in descriptions MUST trace to a requirement, not to model inference. | R | M |

### V — Variant / Candidate Comparison

| ID | Constraint | Check | Severity |
|---|---|---|---|
| V1 | Invariant elements are byte-identical (IDs, names, ordering, layout) across candidates; only the decision-relevant delta varies. | L | M |
| V2 | Each variant declares the decision it addresses and an explicit `delta[]` against the baseline. | L | M |
| V3 | A comparison table of decision criteria MUST accompany the diagrams. Diagrams alone cannot carry a trade-off. | R | M |
| V4 | All variants MUST pass the same constraint set; a variant may not relax correctness rules to look simpler. | L | B |

---

## 3. Conflict Priority

```text
Provenance / Correctness (P, C, R3, R5)
  > Level purity (L)
    > Typing & boundaries (E, B)
      > Cross-view consistency (X)
        > Field grammar & notation (F, S)
          > Budget & aesthetics (G)
```

Lower tiers never override higher tiers.

> **Critical:** G1 (budget) MUST NOT be satisfied by deleting a required read path. This is the most common way a model "fixes" a budget violation and breaks the model.

## 4. Regression runbook

Run this after drawing every C4 block and before recording the document as complete.

1. **Scope first.** Apply only the IDs marked Enforced or Adapted in "Scope in this skill". A retired ID is not a finding; a missing L3/dynamic/deployment view is not a violation.
2. **Validator track (L checks).** Run `python3 scripts/test-skill-contract.py`. Every failure is a finding shaped `{ID, severity, object, evidence, fix}`. Blocker (`B`) forbids render; Major (`M`) must be fixed or recorded as an accepted exception.
3. **Review track (R checks).** A critic evaluates `S2, B1, B5, R5, R12, C5, C7, D4, G2, P4, P5, V3` against the diagram and the `DESIGN.md` evidence, emitting the same finding shape. Answer the constraint in the system's own terms; quoting its wording is not a pass.
4. **Fix loop.** `B` → fix immediately. `M` → fix or record an exception (`ID`, object, reason, accepted by). `m` → fix opportunistically. At most two repair rounds, then surface the remainder. Never invent an edge or delete a required read path to clear a check.
5. **Record.** Add a "C4 regression" row per B/M ID in the `DESIGN.md` evidence register: `pass | fixed | exception | open`. State what was verified and what was not.
6. **Escalate.** A blocker that cannot be fixed is recorded as an open question, never silently relaxed.
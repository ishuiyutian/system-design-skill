---
name: system-design
description: >-
  Designs or evolves a production system from repository evidence, capacity
  math, invariants, and explicit trade-offs, and audits architectural debt in an
  existing repository. Writes one durable DESIGN.md as the source of truth, with
  C4 architecture diagrams.
  USE for: architecture decisions of any size - evolving a repository, greenfield
  systems, scaling or sharding, datastore, consistency, or caching choices,
  capacity and cost sizing, recording an ADR, drift audits, or a single choice
  with workload numbers.
  SKIP for: explaining how a technology or existing code works, debugging, and
  code-level edits such as refactoring.
license: MIT
metadata:
  author: ishuiyutian
  version: "2.6.0"
---

# System Design

## Read this first

The frontmatter description decides whether this skill applies. This file decides the run: step 0 sets the depth, step 1 sets the mode, step 8 adds the debt audit in repository mode, and step 9 writes and verifies the document. A direct answer with no artifacts is a valid completion.

Architecture is decided by invariants, workload numbers, failure modes, and operating constraints—not vibes. Draw the simplest production-viable candidate first, add only evidence-surviving alternatives that differ on a load-bearing axis, recommend one with an evidence chain, and leave a design document another coding-agent session can continue.

The process is identical in repository and greenfield work; interview-grade reasoning falls out of production discipline.

Every recommendation must cite an envelope number, a correctness invariant, a named failure mode, or a principle from [HEURISTICS.md](HEURISTICS.md).

Do not load examples by default. Only if a first-draft recommendation or interface remains generic, consult the matching BAD/GOOD contrast in [EXAMPLES.md](EXAMPLES.md), then replace generic language with the relevant number, invariant, ownership boundary, or failure behavior.

A run writes only its own `DESIGN.md` in the design directory, and, at step 10, the ADR and docs-index link the user accepts. Implementing a candidate or changing code is a separate request.

## Route the ask

Start from what the user brought:

| The user brings | Route |
|---|---|
| A choice a number or a recorded decision may already settle | Step 0. Answer in a paragraph when a gate or decision closes it; otherwise continue |
| An existing design to resume or revise | Step 1 loads it; apply the feedback before any new discovery |
| A change to this codebase, or an audit of its drift from a recorded design | Step 1 resumes a design that covers it; otherwise the full process in repository mode |
| A system with no implementation yet | The full process in greenfield mode; step 8 does not run |
| A pick between candidates already written | Step 1 locates the design, then step 10 |
| An explanation of a technology or existing code, a bug, or a code-level edit | Outside this skill. Answer with ordinary tools and run none of these steps |

## Process

### 0. Size the ask before running the process

This process earns its cost when a decision is hard to reverse, the numbers are load-bearing, or several structurally different designs are genuinely live. Sketch the envelope first. If it lands below the anti-overengineering gates in [HEURISTICS.md](HEURISTICS.md), or one recorded decision already forces the answer, say which gate or decision closed it and answer directly in a paragraph—no artifacts. A false choice rendered as peer sections is worse than no document.

When the process does run, draw the simplest production-viable design first. Add a candidate only when it remains viable after the envelope and invariants and changes a load-bearing axis—for example, the measured scale boundary or the dominant correctness, failure-isolation, cost, or operability risk. Record options closed by a requirement, gate, or named failure as one-line rejections; do not draw, rate, or audit them as peers. Three candidates is the ceiling, not a target.

### 1. Locate and resume

List existing designs—`docs/design/*/DESIGN.md`, or `./*/DESIGN.md` outside a git repo—and read each one's frontmatter `mode`, `status`, and `decided`, plus its H1 title. If one covers this ask, load it and apply the user's feedback before doing new discovery; if two could, name both and ask which.

A loaded design whose frontmatter records `observed.commit` says which code it described. Run `git diff --stat <commit>..HEAD` and inspect current staged, unstaged, and untracked in-scope paths; unchanged HEAD does not identify a changed working tree. At step 2, re-read affected paths and refresh their dependent evidence, questions, and checks using the evidence lifecycle in [HEURISTICS.md](HEURISTICS.md#evidence-and-uncertainty). When the history no longer contains that commit, or the design recorded `uncommittedChanges: true`, the drift is unknown: read the in-scope tree as if nothing had been recorded.

Otherwise derive a kebab-case slug naming the system or subsystem, not the phrasing of the request (`commerce-layer`, not `add-a-commerce-layer`), and choose:

- **Repository mode** when the ask concerns the current codebase. The existing system is Architecture 0.
- **Greenfield mode** when no implementation exists yet.

State the mode, reason, whether you resumed, and the target directory in one line.

For a new artifact-producing run, create a draft `DESIGN.md` with the frontmatter and section skeleton defined in [DESIGN-FORMAT.md](DESIGN-FORMAT.md), then fill it in place. `DESIGN.md` is the working document from this step onward; it is the source of truth, not a summary written at the end. Preserve existing designs. A `DESIGN.md` using the pre-2.1 section order is migrated in place to the SAD skeleton, preserving `## Notes` verbatim; never write a second document. A legacy `design.json` is a read-only migration input: read it to seed the Markdown document, never update it, and never create a new one. Keep the direct-answer route artifact-free. Reuse current records, inspect stale ones, and re-read the sources behind any stale evidence before repeating discovery.

### 2. Establish the current truth

In repository mode, first classify every top-level directory as system code, first-party vendored code under active development, or dependency, sample, and build output. Only the first two are in scope. Directory size is not evidence of importance—the largest tree is usually not the system, and `git log --format=format: --name-only -200 | sed 's#/.*##' | sort | uniq -c | sort -rn` settles most cases. State the classification in one line, including where it contradicts the ask's framing. Record what you are reading as `observed` in the frontmatter: the commit `git rev-parse HEAD` reports, and whether `git status --porcelain` lists changes in the in-scope paths. Outside git, omit it.

Restricted to in-scope paths, read architecture docs, ADRs, domain vocabulary, config, and the hot paths from recent history—plus whatever carries state and effects in this system's shape: schemas, APIs, and queues in a networked service; entry points and lifecycle, state owners, write and flush paths, persisted key namespaces, on-disk formats, entity identity keys, and process or sandbox boundaries in a client, desktop, or embedded codebase. Stop when the flows and invariants below close. Code and schema outrank prose when they disagree—record the divergence under Requirements conflicts, and ask rather than picking a side silently when it changes an invariant.

Settled ADRs are constraints, but an ADR that is a stub, superseded, duplicated, or pointing outside this repository is unavailable evidence rather than a constraint; list what you could not read. These ADRs are also the reference model the audit at step 8 measures against, so record each one's status: a decision that is accepted and quietly violated is a different finding from one that was superseded and never removed. Name the documents that already own this subject—when one already decides part of the ask, say what it settles and aim the run at what it leaves open. Trace the user-facing flows end to end and inventory every component using the kinds in [DESIGN-FORMAT.md](DESIGN-FORMAT.md).

In both modes, define:

- core entities and the invariants that must never break;
- system interfaces and their consistency/idempotency contracts;
- critical end-to-end flows, including failure and recovery flows;
- source-of-truth stores versus derived views.

Record load-bearing observations, derivations, and inferences with source identity, scope, and limitations in the evidence appendix's investigation register; retain unanswered parts of the ask as open questions and missing proof as unknowns. Use the [evidence lifecycle](HEURISTICS.md#evidence-and-uncertainty). A well-formatted record does not prove its claim.

Ask the user only for decisions that cannot be recovered from the repo or prompt.

### 3. Close the requirement frontier

Use [INTERVIEW.md](INTERVIEW.md) to fill only the unresolved frontier. Ask numbered questions in at most three rounds of at most eight, each with a recommended default; with no user present to answer, take the defaults instead of asking. Functional scope, excluded scope, business objectives, stakeholders, security and regulatory obligations, data classifications, numerical non-functional targets, workload shape, team/cost constraints, and the top three characteristics must be explicit. Guiding principles and business-impact KPIs are recorded when they can change a decision. Label every assumption.

### 4. Run and challenge the envelope

Compute the numbers that gate *this* system. For request-serving systems that is average and peak QPS, storage growth, bandwidth, cache footprint, concurrency, and the domain's load-bearing distribution (burst, skew, fan-out, hot keys, object sizes). Where the binding constraint sits on a device, compute it in the units that bind there: bytes and round trips per session, request volume against provider quotas and their cost, memory ceiling in a process the OS can kill, on-device storage growth, cold-start budget, and offline divergence window. Where money crosses a boundary, compute the unit economics of the events the design protects. Record any standard metric that does not apply as `n/a` with a one-line reason; never invent a number to fill a row. Show derivations and verify arithmetic with a shell command.

Run the physics/CAP sanity pass in [INTERVIEW.md](INTERVIEW.md). Use the compact router in [ARCHETYPES.md](ARCHETYPES.md) to select by protected invariant, then load only the selected pack. Do not load every pack by default. Test the envelope against each selected archetype's **Shape**, and its **Numbers anchor** where it has one. An archetype whose **Not when** clause fires is the wrong match—drop it and say so, rather than importing machinery this system does not need. Resolve contradictions before drawing candidates.

### 5. Fix the data and consistency model

Topology that is correct for the wrong data model is not a design. Before drawing anything, state for each core entity: its representation in memory and at rest, its identity scheme, which component holds ordering authority, how conflicts resolve per field class, the point at which a write becomes durable, and the garbage-collection or compaction story. Use the conflict-resolution rule in [HEURISTICS.md](HEURISTICS.md); it is chosen by the coordination available, not by sophistication.

Write this into the Data Sets & Data Model section before candidates exist, including data impact and migration. For every structured store, also generate intuitive database schemas: name each table or collection, list only the fields that explain the design, mark primary, partition, sort, and deduplication keys, and state important indexes, relationships, source-of-truth status, and retention notes. Use human-readable cards like `Ticket — id, eventId, seat, price, status, userId`; no executable DDL. Where candidates disagree on any of these, that disagreement is itself a candidate axis—see step 6.

### 6. Draw the candidates

Fully draw the simplest production-viable architecture. Add another only if it survives the envelope and invariants and differs on a load-bearing structural, data-model, consistency, cost, or operability axis. Useful surviving alternatives often optimize for the measured scale boundary or the dominant correctness, failure-isolation, cost, or operability risk. Keep every closed option as a one-line rejection with the requirement, gate, or failure mode that closed it. Never invent a peer merely to fill a section; stop after three.

In repository mode, each is an evolution of Architecture 0 and migration cost is first-class. Candidates must satisfy the distinctness rule in [DESIGN-FORMAT.md](DESIGN-FORMAT.md#candidate-records). Where the difficulty lives in the data model rather than the component graph—collaborative editing, consensus, ledgers, indexes—generate candidates on the data-model axis and hold topology fixed.

Every distributed mechanism must earn its place with a number, invariant, or named failure mode. Every candidate must state at least one honest weakness, and must clear the **Staff gate** of every archetype it touches in the packs selected through [ARCHETYPES.md](ARCHETYPES.md)—those are the questions a plausible diagram does not answer.

A gate is cleared by answering it in this design's own terms: the component that does it, the number it holds to, or the behaviour it accepts. Repeating the gate's wording is not an answer, and quoting it as evidence for a design that does not implement it is the failure this rule exists to catch. Where an archetype's gate does not apply because you took a different structure, say which structure replaced it and what now covers the failure that gate was guarding—an obligation is discharged or explicitly retired, never dropped. If a candidate deviates from the conventional baseline, name that baseline and prove how the deviation still covers its failure modes.

Draw structure with C4. Use the [C4 constraint catalogue](C4/CONSTRAINTS.md) as the guidance — its IDs and severities are the contract — plus the [generation gates](C4/RULES.md#generation-gates) and [model rules](C4/RULES.md) for Level 1 and Level 2, and the [Mermaid C4 profile](C4/PROFILE.md) for syntax; [DESIGN-FORMAT.md](DESIGN-FORMAT.md#structure-diagrams) says where the diagrams belong and what to record. Add one `C4Context` under High-level solution design, then one `C4Container` per candidate. Record `Structure diagram: C4Context + C4Container` with a one-line reason. Admit each container with the steady-state process or owned-store test; draw one-hop relationships; then run the completeness, cross-level, and cross-candidate gates. Keep CDN, DNS, load balancers, and deployment nodes out of C4; keep protocols out of the context and in the L2 relationship technology field. Record a load-bearing deployment service in Key Design Decisions or Technology Impacts. Do not add a flow diagram, component, edge, or flow-step table. Critical-flow behavior and load-bearing dependency deadline, retry, and backlog facts belong in Key Design Decisions. Omit the rest, and give a closed option no diagram.

### 7. Decide and deep-dive

Rate every candidate using [HEURISTICS.md](HEURISTICS.md), led by the user's top three characteristics. Recommend one with a chained evidence argument. A rating may not appear in that chain—it is a candidate's opinion of itself. The chain rests on an envelope number, an invariant, or a named failure mode.

Record the decisions a reviewer would challenge in the Key Design Decisions section: the decision log, interface contracts, in-scope and out-of-scope integrations, integration details and data mapping, and mobile/client details. Resolve the two or three decisions with the greatest correctness, cost, or operability pressure. Each deep dive must record pressure, decision, rejected alternatives, failure mode, and evidence. State retries, timeouts, idempotency, reconciliation, failover, observability, rollout, what breaks first, and the measurement that would overturn the recommendation.

A design is complete only when:

- every critical flow ends at a named durable or final effect in Key Design Decisions;
- every invariant has one enforcement authority;
- every load-bearing dependency has a deadline, retry owner, and bounded backlog in Key Design Decisions;
- every load-bearing authoritative store has an acknowledgement point, failure domain, RPO, and RTO in a plain-language C4 container description;
- every load-bearing derived view names its reconstruction source and cursor in its C4 container description;
- every candidate has a named first failure;
- every recommendation has a falsifiable evidence chain;
- every unresolved uncertainty is recorded as an assumption or measurement;
- every required SAD section is present or marked `n/a` with a reason;
- all artifacts pass structural, C4-validity, and diagram checks.

Before writing, verify:

- every load-bearing queue/log declares delivery and idempotency semantics in Key Design Decisions;
- every store shown in a C4Container diagram is source-of-truth or derived;
- every load-bearing authoritative store names the recovery path that meets its RPO and RTO in its C4 container description;
- offered load is stated against drain capacity, including the amplification retries add exactly when capacity is lowest;
- every structured store has an intuitive schema whose fields, keys, indexes, and relationships support its stated access patterns and invariants;
- every schema and wire-contract change names its compatibility direction and the order in which readers and writers deploy;
- the design survives its own clients: duplicate submits, reconnect storms, cold caches, and a dependency that slows instead of failing;
- burst, skew, fan-out, hot keys, and partial failure are addressed;
- security, privacy, abuse, retention, and deletion are addressed where relevant;
- no critical deep dive has been deferred into a vague next step.

### 8. Audit the architecture for debt

Repository mode only, and only now: a finding's exposure is measured against the candidate this run recommends, which did not exist until the previous step. Greenfield has no implemented architecture to compare against and skips this step entirely.

Follow [AUDIT.md](AUDIT.md). The order of its stages is the substance, not the ceremony: collect the structural facts—graph, edge contracts, ADR statuses, change history—before forming any verdict; generate candidate findings one category at a time, without showing the finder the previous run's list; put every candidate through the mechanical gates; hand the survivors to a red team that sees the claim but never the argument behind it. Both finders and verifiers can be wrong. Record the check and its evidence; an undecidable check remains unknown rather than becoming refutation or confirmation.

Where a subagent primitive exists, run one finder per category and one verifier per lens. Where it does not, run the same stages inline, restating the brief and discarding the previous stage's reasoning at each boundary. Keep finding and judging separate; separation reduces shared context but does not establish independent accuracy.

Write the result into the Architectural debt appendix of `DESIGN.md`, including what was checked and what could not be established. Findings may seed risks and next steps; they never generate a candidate, and they never become an ADR.

The audit is done when every newly confirmed finding cites evidence and passes all four debt tests, every `blocking` finding names by id the invariant or target it violates, and the coverage list names every category examined. Retain historical findings whose current checks are unknown with that limitation visible; do not present them as newly confirmed. Record every check the run could not establish rather than dropping it.

### 9. Write and verify

`DESIGN.md` is the source of truth, so this step finishes it rather than generating a second artifact from another source. Include the investigation's question outcomes, evidence references, unresolved checks, and freshness limitations. Preserve any user-owned `## Notes` verbatim. Validate all diagram aliases, dependency contracts, evidence references, and finding ids using [DESIGN-FORMAT.md](DESIGN-FORMAT.md#verification).

Diagrams are part of the document, not a separate render. Confirm that there is one `C4Context` under High-level solution design, one `C4Container` per candidate, and every structure block is C4 with `%% system-in-scope:`, `%% c4-level:`, and `%% legend:` metadata, a title that names the level and scope, and a business-named `System_Boundary`. Run the [C4 generation gates](C4/RULES.md#generation-gates), check against [C4/RULES.md](C4/RULES.md) and [C4/PROFILE.md](C4/PROFILE.md), then run the [regression runbook](C4/CONSTRAINTS.md#4-regression-runbook) and fix every blocker (B) and major (M) finding. The checks: no CDN, protocol, or deployment element at Level 1; no `Container_Boundary` or `Person` inside the boundary; every element has at least one relationship; every internal store has a read and write path or `archiveOnly`; no `Person` connects to an internal store or worker; every boundary-crossing relationship declares transport and auth posture; every diagram alias is declared in the same block and reused consistently; every L2 person and external system exists in L1 with the same alias, label, and description; no alias flips between internal and external; every L2 boundary-crossing relationship rolls up to L1; and every L1 relationship touching the scope is realised by at least one candidate. No flow diagram exists. Do not add a second structure representation or a table.

Then confirm the document survived. Check that the frontmatter parses, the required SAD headings appear in order, every required section has content or an explicit `n/a` reason, every diagram alias and dependency contract resolves, and every diagram uses its recorded role. Security and regulatory obligations, business-impact KPIs, data classifications, and glossary terms must be present or marked `n/a` with a reason. If a renderer or Mermaid preview is available, load the document and inspect the diagrams; if not, say that rendering was not inspected and claim nothing it would have shown. A missing diagram or an unresolved reference is unfinished, not a cosmetic defect.

When a check does not go as described, act on what you observe:

| You observe | It means | Next |
|---|---|---|
| A missing heading or frontmatter field | The document cannot be resumed reliably | Add the heading or field from the skeleton in [DESIGN-FORMAT.md](DESIGN-FORMAT.md), then re-check |
| A required SAD section is empty or missing | The document cannot be reviewed against the template | Add the section with real content or `n/a — <reason>`; never leave an empty heading |
| An alias, edge, evidence reference, or finding id that names nothing | A dangling cross-reference | Fix the reference or add the missing alias; do not leave the reader to guess |
| A Mermaid block that uses the wrong role or an undeclared alias | Structure is not C4 or an alias is dangling | Convert the block to C4Container or declare the alias and component |
| No renderer or Mermaid preview | Rendering cannot be inspected | Keep the diagrams, state that rendering was not inspected, and claim nothing it would have shown |
| A legacy `design.json` is the only record | An old design has not been migrated | Read it into `DESIGN.md`, leave it untouched, and say the document is now the source of truth |

Finish by answering the ask, not by listing files written. Go back to what the user asked for and mark each part answered, partly answered, or open, naming what is still missing. Lead with the recommendation and its evidence chain in a few lines; name the `assumed` inputs it rests on and the measurement that would overturn it; state what was not verified, such as an uninspected diagram render or audit checks the run could not establish; then give the `DESIGN.md` path. End with the decision that belongs to the user, which step 10 records.

### 10. Record the decision

When the user chooses, set frontmatter `status: decided` and `decided` to the chosen architecture's id, then update `DESIGN.md` in place. In repository mode, offer an ADR under `docs/adr/` that records the accepted candidate, rejected candidates, evidence, and consequences. Name the owning documents from step 2 in its Context, mark any ADR it replaces as superseded, and link `DESIGN.md` from wherever the repo indexes its docs. Future runs must read it and not re-litigate it without new evidence.

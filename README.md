# System Design

**System design from evidence, not vibes.**

`/system-design` takes you from an incomplete idea or an existing codebase to a defensible architecture decision. It sizes the ask before it starts, and answers small or already-settled questions directly instead of manufacturing a document. When the decision earns the process, it discovers what the repository already proves, asks you only for the requirements it cannot recover, derives the system’s entities, invariants, interfaces, data and consistency model, scale envelope, and critical flows, then fully draws only the candidate architectures the evidence leaves viable. It compares their strengths and weaknesses and recommends one. In an existing repository it also audits what was built against what was intended, and reports the architectural debt between them with a remedy and the evidence behind each finding. Outputs one durable `DESIGN.md` — a Solution Architecture & Design document with business context, security and compliance, guiding principles, business impact, scope, solution design, data sets and model, key decisions, technology impacts, data classifications, and a glossary in the main body, plus evidence, debt, deep dives, and measurements in appendices. It records the reasoning and can be resumed in future agent sessions, with Mermaid C4 architecture diagrams. Designs with structured persistence include intuitive database schemas—essential fields, keys, relationships, and indexes—rather than executable DDL.

## Installation

Pick one path. Both load the same skill, so installing both makes `/system-design` appear twice in the picker.

### Codex, Claude Code, Cursor, and other compatible agents

```bash
npx skills@latest add ishuiyutian/system-design-skill
```

Choose which agent should receive the skill. The files remain editable, and you decide when to pull updates:

```bash
npx skills update
```

### Claude Code plugin

Use the plugin when you want a managed, versioned installation:

```bash
claude plugin marketplace add ishuiyutian/system-design-skill
claude plugin install system-design-skill@ishuiyutian-skills
```

Claude namespaces marketplace skills to prevent collisions. Invoke this installation as:

```text
/system-design-skill:system-design
```

Update it with:

```bash
claude plugin update system-design-skill@ishuiyutian-skills
```

## Quick start

Run the skill with whatever context you already have. It will discover the rest from the repository or ask for the decisions that remain open.

The skill is model-invocable when the intent is to make or evaluate an architecture decision: designing, re-architecting, scaling, sizing, recording an ADR, or choosing among datastore, consistency, partitioning, replication, cache, or queue topologies. A technology explanation is not a trigger, and neither is implementation debugging that merely mentions those mechanisms. A bounded choice whose envelope forces one answer gets a direct answer; competing architecture structures run the full process. Type the command when you want it explicitly.

The examples below use the standalone name `/system-design`. If you installed the Claude plugin, use `/system-design-skill:system-design` instead.

### Evolve an existing system

```text
/system-design Redesign our notification pipeline to support regional failover
```

### Design a new system

```text
/system-design Design a collaborative document editor for 10 million DAU
```

Repository work is the primary path. Greenfield work uses the same process without an existing Architecture 0.

## Examples

- [Evolve an existing repository](docs/demos/repository-evolution.md) — reconstruct Architecture 0 from the code, then compare migration-aware evolutions.
- [Design a greenfield system](docs/demos/greenfield-design.md) — turn a ticket on-sale prompt into measurable requirements, capacity math, and complete architectures.

## The complete journey

### 1. Sizes the ask before running the process

The process is expensive, so the skill spends it only where it pays. It sketches the envelope first and checks it against the anti-overengineering gates. If the ask lands below them, or a recorded decision already forces the answer, the skill names the gate or the decision and answers directly in a paragraph — no artifact is written.

When the process does run, the skill starts with the simplest production-viable candidate. It draws another only when the envelope and invariants leave a genuinely different structure viable on a load-bearing axis. Closed alternatives remain one-line rejections; three is a ceiling, not a target.

### 2. Starts with evidence

In an existing repository, the skill reads the architecture docs, ADRs, domain vocabulary, configuration, schemas, APIs, queues, storage code, and critical user-facing flows before asking anything.

It reconstructs the current system as **Architecture 0**:

- what each component owns;
- where authoritative state lives;
- how requests and events move through the system;
- which decisions are already settled;
- which constraints a redesign must preserve;
- where the current architecture is under pressure.

In greenfield work, it extracts the same starting facts from the prompt.

### 3. Gets the requirements out

The skill turns missing requirements into a focused decision frontier. It never asks you for facts the repository already answers.

Questions are numbered, grouped, and paired with a recommended default, so you can answer precisely or accept the recommendations. It covers only decisions capable of changing the architecture:

- core actors, flows, entities, and excluded scope;
- invariants that must never break;
- latency, availability, durability, and consistency targets;
- DAU, concurrency, peak QPS, payload sizes, growth, burst, skew, and fan-out;
- privacy, retention, abuse, and compliance boundaries;
- team size, budget, hosting, migration, and rollout constraints;
- the characteristics that matter most for this system.

There are at most three short rounds. Anything still unknown becomes a visible assumption rather than a hidden guess.

### 4. Defines the system before drawing it

Before choosing components, the skill makes the system model explicit:

- **Entities** — the durable things the product manages.
- **Invariants** — what must remain true across retries, failures, and concurrency.
- **Interfaces** — each boundary's style and transport, trust boundary, deadline, retryability and owner, backpressure, consistency and idempotency scope, compatibility direction, and failure result.
- **Critical flows** — the happy paths plus failure and recovery paths.
- **Sources of truth** — authoritative stores separated from caches, indexes, and other derived views.

This prevents the design from becoming a fashionable component list with no correctness model.

### 5. Runs the operating envelope

The skill derives the numbers that can change the design:

- average and peak reads and writes;
- storage growth and retention;
- ingress and egress bandwidth;
- concurrent connections and worker demand;
- cache footprint;
- burst ratios, hot keys, uneven tenants, and fan-out.

It shows the derivations, verifies the arithmetic, and challenges physically contradictory requirements before proposing an architecture.

### 6. Fixes the data and consistency model

Topology that is correct for the wrong data model is not a design, so this is settled before anything is drawn. For every core entity the skill states:

- how it is represented in memory and at rest;
- its identity scheme;
- which component holds ordering authority;
- how conflicts resolve, per field class;
- the point at which a write becomes durable;
- the garbage-collection or compaction story.

For every structured store it also draws a readable database schema: the table or collection name, load-bearing fields and human-readable types, primary/foreign/partition/sort keys, important relationships and indexes, and brief authority or retention notes. These are design artifacts, not executable SQL, migrations, or exhaustive physical schemas.

Where the difficulty lives here rather than in the component graph — collaborative editing, consensus, ledgers, indexes — this becomes the axis the candidates differ on.

### 7. Constructs the candidate architectures

A run fully draws the simplest production-viable candidate. It adds a directly comparable candidate only when that candidate survives the envelope and invariants and changes a load-bearing structural, data-model, consistency, cost, or operability axis. An option closed by a requirement, gate, or failure mode remains a one-line rejection instead of a peer section. Three candidates is the ceiling.

Each drawn candidate includes its complete clients, networking, compute, state, queues, external dependencies, connections, flows, operational behavior, migration cost, advantages, and weaknesses. Structure is C4: one C4Context for the high-level view and one C4Container per candidate. C4Container wraps the business system in `System_Boundary`; external systems sit outside it. Deployment services such as a CDN, DNS, or load balancer are recorded in Technology Impacts or Key Design Decisions, not drawn as C4 elements. Each block carries scope, level, and legend metadata with a title that names the level and scope. Container descriptions are plain business sentences that name the responsibility and, when load-bearing, the reliability promise. Critical-flow behavior and dependency deadlines, retry owners, and backlog bounds live in Key Design Decisions. Every element has at least one relationship; every internal store has a read and write path or `archiveOnly`; a Person never connects directly to an internal store; and boundary crossings name transport and auth posture. A fact that cannot change the design is omitted. There are no per-candidate component, edge-contract, or flow-step tables. Swapping one database does not count as a different architecture; swapping the ordering authority or the conflict-resolution model does.

After the envelope identifies the protected invariant, the skill loads only the matching archetype pack. It composes packs only for independent invariants and never loads the full pattern catalog by default.

In repository mode, each candidate is an explicit evolution of Architecture 0 rather than a greenfield rewrite that ignores migration.

### 8. Pressure-tests the trade-offs

The candidates are compared against the priorities established during requirements discovery. Every recommendation must be justified by an envelope number, an invariant, a named failure mode, or an operating constraint.

The highest-pressure decisions receive deeper treatment, including:

- retries, timeouts, duplicates, and partial completion;
- idempotency and reconciliation;
- failover and blast radius;
- observability and rollout;
- what breaks first;
- the measurement that would overturn the recommendation.

A run is complete only when critical flows reach named final effects, invariants and ownership are explicit, load-bearing dependencies and authoritative stores carry bounded failure/recovery contracts, candidates name what fails first, and the recommendation is falsifiable. Unresolved facts remain visible assumptions or measurements, and artifacts must pass structural and diagram checks.

### 9. Audits the architecture that already exists

Repository runs end by grading the system they started from. The audit compares the implemented architecture against the one the repository says it intended — the recorded design and the accepted ADRs — and reports where the two have come apart.

A finding is not raised because something looks unusual. It has to name what it costs, cite the file or decision it rests on, and survive an attempt to disprove it: a model is an unreliable detector of architectural problems and a reliable disprover of them, so findings are generated cheaply and then have to get past verifiers that never see the argument that produced them. The strongest objection a finding survived is recorded beside it.

Each one carries a remedy — cut, consolidate, extract, replace, isolate, or document — with what it costs and whether it can be undone. Severity is looked up from two recorded axes rather than chosen, so you can disagree with an input instead of a verdict. Nothing is scored, and nothing is estimated in hours: those numbers have no calibration behind them.

Greenfield runs skip this entirely. There is no implemented architecture to audit.

### 10. Produces the design document

The skill writes and verifies a single `DESIGN.md`. It carries:

- a SAD main body: context and business objectives, security and compliance, guiding principles, business impact and KPIs, scope, solution design, data sets and data model, key decisions, technology impacts, data classifications, next steps, and glossary and references;
- appendices for evidence and open questions, critical deep dives, and measurements that could overturn the decision, with the debt register in repository mode;
- a C4Context high-level view and one C4Container per candidate, with the recorded structure role and reason;
- tables for schemas, interfaces, estimates, and ratings.

The document is the source of truth. It is plain Markdown with Mermaid blocks, so it renders in GitHub, VS Code, and Obsidian, and a later agent session can resume from it directly.

## What appears on disk

| Artifact | Purpose |
|---|---|
| `docs/design/<slug>/DESIGN.md` | The SAD document and the source of truth: business context, security and compliance, principles, business impact, scope, solution design, data, decisions, technology impacts, data classifications, glossary, and engineering appendices including, in repository mode, the debt register |
| `docs/adr/NNNN-<slug>.md` | Offered in repository mode once you pick a winner, so future sessions do not re-litigate it |

Outside a Git repository, `DESIGN.md` is written under `./<slug>/`. When the ask lands below the anti-overengineering gates, nothing is written at all — you get the answer and the gate that closed it.

Run `/system-design` again for the same system and it resumes from `DESIGN.md` instead of restarting discovery.

## What the skill will not do

- Run the full process, or produce artifacts, for a decision that is small and reversible.
- Ask for information it can recover from the repository.
- Hide missing requirements behind confident prose.
- Recommend distributed machinery without a number, invariant, or failure mode that earns it.
- Present one preferred design and two incomplete straw men.
- Treat caches, indexes, or queues as authoritative without saying so.
- Write a second design source or a generated report behind the document.
- Score architectural debt, or estimate remediation in hours or currency.
- Raise a finding it cannot evidence, or one a recorded decision already settles.
- Recommend a rewrite. Remedies are incremental, and work that is not gets scheduled and named as such.

## How it is built

The skill is plain Markdown; it ships no runtime, renderer, or generated report:

| File | Responsibility |
|---|---|
| [`SKILL.md`](skills/system-design/SKILL.md) | The complete architecture workflow |
| [`INTERVIEW.md`](skills/system-design/INTERVIEW.md) | Requirements frontier and question protocol |
| [`HEURISTICS.md`](skills/system-design/HEURISTICS.md) | Decision rules, capacity references, and comparison characteristics |
| [`ARCHETYPES.md`](skills/system-design/ARCHETYPES.md) | Canonical system patterns and failure modes |
| [`DESIGN-FORMAT.md`](skills/system-design/DESIGN-FORMAT.md) | The SAD `DESIGN.md` contract, section skeleton, investigation and debt appendices, and where C4 diagrams belong |
| [`C4/CONSTRAINTS.md`](skills/system-design/C4/CONSTRAINTS.md) | The canonical C4 constraint catalogue: IDs, severities, scoping in this skill, and the regression runbook |
| [`C4/RULES.md`](skills/system-design/C4/RULES.md) | C4 generation gates, Level 1 and Level 2 modeling rules, completeness checks, cross-level and cross-candidate consistency, naming, anti-patterns, and review checklist |
| [`C4/PROFILE.md`](skills/system-design/C4/PROFILE.md) | Mermaid C4 syntax profile, mechanism vocabulary, text limits, palette, layout, and renderer targets |
| [`EXAMPLES.md`](skills/system-design/EXAMPLES.md) | Conditional BAD/GOOD contrasts for making a generic first draft operationally specific |
| [`AUDIT.md`](skills/system-design/AUDIT.md) | Debt taxonomy, the verification pipeline, and the findings that must not be raised |

Everything is inspectable and editable. The skill sends no repository or design data to a service; investigation freshness is a judgment from the current read rather than a byte-hash checkpoint. [Research and limits](docs/research/2026-10-21-harness-lessons.md).

Whether an agent reaches for the skill is decided by its description alone. The portable gate is the host-agnostic [`scripts/test-skill-contract.py`](scripts/test-skill-contract.py); live discovery is per-host evidence, and [`scripts/eval-invocation.py`](scripts/eval-invocation.py) is one Claude Code adapter. It sends each prompt in [`docs/evaluations/invocation-cases.json`](docs/evaluations/invocation-cases.json) to a headless Claude Code session that loads only this plugin, and reports which prompts invoked the skill:

```bash
python3 scripts/eval-invocation.py --runs 3
```

Each run stops at the first Skill request or reaches a terminal result within its turn budget. A turn-limit failure, timeout, missing result, or other invalid trial blocks the gate. Unknown costs are reported as unknown. Use `--output-dir <new-directory>` to retain attempts and provenance; `--host user` repeats the check against your installed skills and settings. This evaluates discovery only, not design quality or completed delivery.

## Support and security

- Ask usage questions or report bugs through [GitHub Issues](https://github.com/ishuiyutian/system-design-skill/issues).
- Report vulnerabilities privately through [GitHub Security Advisories](https://github.com/ishuiyutian/system-design-skill/security/advisories/new).
- Read the package’s data-handling and review guidance in [`SECURITY.md`](SECURITY.md).

## License

MIT. Use it, adapt it, and make it fit your own engineering process.

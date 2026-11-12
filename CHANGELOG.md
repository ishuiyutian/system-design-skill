# Changelog

All notable changes to this project are documented here.

## 2.6.0 — 2026-11-12

### Changed

- `C4/CONSTRAINTS.md` is now the canonical C4 constraint catalogue: its IDs and severities are the source of truth. `RULES.md`, `PROFILE.md`, and `DESIGN-FORMAT.md` cite those IDs instead of a parallel numbering, and `SKILL.md` links the catalogue at the structure and regression steps.
- Added "Scope in this skill" and "Regression runbook" to `CONSTRAINTS.md`: each ID is marked Enforced, Adapted, or Retired, and every B/M finding is fixed or recorded as an accepted exception through a validator plus review-gate loop.
- `PROFILE.md` defines a single closed mechanism vocabulary that reconciles transports with storage access paths.

### Removed

- The parallel rule-catalogue numbering in `RULES.md` (`S/M/R/L1/L2/P/E/B/C/G/X/PR`); cross-level `P` maps to the `X` series and provenance `PR` to the `P` series.
- The legacy migration path: the pre-2.1 and pre-2.3 `DESIGN.md` migration instructions and the read-only `design.json` migration input. `DESIGN.md` is now created fresh or updated in place, with no migration contract for older artifacts.

## 2.5.0 — 2026-11-12

### Added

- C4 generation gates: declare scope and title, admit containers, type elements, draw one-hop relationships, run completeness, then run cross-level and cross-candidate checks.
- Container admission uses a steady-state process or owned persistent store test. Transient CLIs, libraries, and adapters fold into their parent or move to Key Design Decisions; there is still no L3 view.
- Completeness checks require every store to have an inbound read and write path or `archiveOnly`, every worker to have a result path, and every external dependency to appear.
- Relationship checks require one hop, a closed transport list, intent verbs, no Person-to-store edge, an exception for external-to-store, and auth posture on boundary crossings.
- Cross-candidate checks keep shared external identity stable, prevent internal/external alias flips, and require every L1 external to appear in at least one candidate.
- C4 titles and legends are now required: `Context view - <System>` and `Container view - <System> - <Candidate>`, plus a `%% legend:` line for arrow convention and ownership.
- Contract tests cover the new checks and include a negative write-only-store fixture.

### Changed

- C4 budgets tighten to ten context elements and twelve context relationships, and twelve containers, eighteen relationships, and fifteen total nodes per candidate; boundary crossings above six are a readability warning.
- The ticketing example routes fan availability reads through a reader, adds a draw publisher, closes store read and write paths, and adds transport plus auth posture at boundaries.
- Container technology fields and relationship labels now carry the profile's word limits while still allowing one plain-language state contract in an authoritative store description.

### Rejected

- `C4/CONSTRAINTS.md` remains a source specification, not runtime context. Its JSON-first model, template renderer, dynamic views, component views, and deployment views conflict with this skill's `DESIGN.md`-only, C4Context plus C4Container contract and are recorded as out of scope.

## 2.4.0 — 2026-11-12

### Added

- `C4/RULES.md` is the canonical C4 Level 1 and Level 2 modeling contract: one scoped system, intent-only context relationships, one matching `System_Boundary` per candidate, external `_Ext` systems, naming, anti-patterns, and the rule catalogue.
- `C4/PROFILE.md` is the canonical Mermaid C4 syntax profile: supported keywords, metadata header, text limits, palette, layout, no flowchart fallback, and renderer targets.
- C4 provenance packs mirror both files under `docs/provenance/C4/`.

### Changed

- `DESIGN-FORMAT.md` now places and records C4 diagrams and links the C4 pack instead of restating its rules.
- Cross-level consistency is adapted to this skill's multi-candidate SAD: the context is the union of context relationships, each L1 relationship must be realised by at least one candidate, and every L2 boundary crossing must roll up to L1.
- C4 text is ASCII, quoted, and free of commas, parentheses, and HTML; aliases use semantic camelCase; titles use ASCII hyphens.
- CDN, DNS, load balancers, protocols, and deployment nodes are no longer C4 elements. A load-bearing deployment service is recorded in Technology Impacts or Key Design Decisions.
- `Container_Boundary` is no longer allowed; each candidate has one business-named `System_Boundary`.
- The example uses `seatDb` and `seatLog`, carries the `%% system-in-scope:` and `%% c4-level:` header, and keeps the payment webhook roll-up in Level 1.
- Contract tests enforce Level 1, Level 2, cross-level consistency, metadata, text limits, and rendering.

### Fixed

- Plugin and marketplace descriptions now say C4 architecture diagrams instead of flow diagrams.
- Provenance heading alignment for `DESIGN-FORMAT.md` and the new C4 packs.

## 2.3.0 — 2026-11-11

### Breaking

- Structure uses C4: one `C4Context` under High-level solution design and one `C4Container` per candidate.
- Critical-flow diagrams are removed. Critical-flow behavior and dependency contracts live in Key Design Decisions.
- `Diagram kind:` is replaced by `Structure diagram: C4Context + C4Container`.

### Changed

- C4 structure stays high-level: container descriptions state the business responsibility and a plain-language reliability promise, while `Rel` labels carry only sync/async and protocol.
- Candidate records carry structure, trade-offs, migration, and ratings only. There are no flow diagrams, step tables, or per-candidate component or edge tables.
- AGENTS, README, provenance, tests, and the ticketing example are updated for the C4-only structure.

### Fixed

- C4Container diagrams wrap the business system in `System_Boundary` and no longer invent generic `Edge`, `Application`, or `Data` systems. External services such as the CDN sit outside the boundary.
- Container descriptions are plain business sentences; implementation terms such as WAL fsync, synchronous standby, and fenced promotion sit in the technology field.
- C4 validity is checked: every container has at least one relationship.
- The ticketing example is C4-only; all sequence flow diagrams are removed.

## 2.2.0 — 2026-11-11

### Breaking

- Candidate records no longer use per-candidate Components, Edges and contracts, or flow step tables. The structure and critical-flow diagrams are the record.
- Flow step tables are removed; a critical flow is a diagram of the recorded kind, and a non-critical linear flow is omitted or summarized.
- Dependency, store, and derived-view contracts are now scoped to load-bearing records and live in diagram labels, not tables.

### Changed

- Candidate sections now carry Structure, Critical flows, Trade-offs, Migration, and Ratings.
- Only load-bearing component, dependency, and state-contract facts are recorded; the rest is omitted.
- Candidate records keep one recorded diagram kind; structure stays C4 and critical flows use the recorded kind. Sequence participants are the component inventory when sequence is chosen.
- README, provenance, and verification rules now say the diagram is the record.

### Fixed

- Removed flow step tables that duplicated and drifted from diagrams: Candidate B step 6 and Candidate C step 5 no longer disagree with their diagrams.

## 2.1.0 — 2026-11-11

### Breaking

- `DESIGN.md` now uses a unified Solution Architecture & Design (SAD) section order. Existing documents are migrated in place on resume; `## Notes` is preserved and no second document is created.
- Investigation evidence, architectural debt, critical deep dives, and measurements move to appendices. The debt appendix is repository-only and omitted entirely in greenfield.

### Added

- Main-body sections for Context & Background, Security & Regulatory Compliance, Guiding Principles, Business Function Impact, Scope & Requirements, Solution Design, Data Sets & Data Model, Key Design Decisions, Technology Impacts, Data Classifications, Next Steps, and Glossary & References.
- A skeleton, a per-section required-content table, an `n/a — <reason>` rule, and legacy migration instructions in `DESIGN-FORMAT.md`.
- Business, security, data-classification, principle, KPI, and integration questions in `INTERVIEW.md`.
- Contract tests for SAD heading order, nonempty required sections, `n/a` reasons, and the ten-item completion contract.

### Changed

- The ticketing example is rewritten in the SAD order with business objectives, stakeholders, compliance obligations, principles, KPIs, decision log, integrations, technology impacts, data classifications, and glossary.
- Interface contracts, integration details, and mobile/client decisions now sit under Key Design Decisions; requirements and estimates sit under Scope & Requirements; data model and schemas sit under Data Sets & Data Model.
- Multiple diagrams of the chosen kind are allowed for a SAD; mixing diagram kinds remains a contract defect.
- `README.md` and provenance are updated for the SAD template.

### Fixed

- The example `DESIGN.md` quotes the `Tier allocators (6)` flowchart label. Mermaid treats unquoted parentheses inside square brackets as shape syntax, so the diagram previously failed to parse.

## 2.0.0 — 2026-11-11

### Breaking

- `DESIGN.md` is now the only design artifact and the source of truth. The skill no longer writes `design.json`, an HTML report, or a generated copy. Existing `design.json` files are read-only migration inputs.
- The bundled investigation CLI and report renderer are removed. A run writes and verifies the Markdown document directly; evidence freshness is re-read and recorded in the document rather than enforced by byte hashes and checkpoints.

### Added

- `DESIGN-FORMAT.md` replaces `HTML-REPORT.md` as the document contract: frontmatter, section order, investigation register, component and contract tables, debt register, and verification.
- One diagram kind per design, chosen by the agent from context and recorded with a reason. The agent picks C4 structure, flowchart, or sequence, asks the user only when two are genuinely tied, and uses only that kind; tables carry what the kind cannot express.
- The ticketing example is rewritten in the new format with one recorded diagram kind and all diagrams in that kind.

### Removed

- `skills/system-design/scripts/` (`design_session.py`, `render_report.py`, `session_runtime/`), `assets/report-template.html`, and `RUNTIME.md`.
- `scripts/test-design-session.py`, `scripts/test-report-renderer.py`, and `scripts/test-report-utf8.py`.
- `examples/design-ticketing/design.json` and the HTML report screenshot.

## 1.4.1 — 2026-11-09

### Added

- `render_report.py` derives the default output path from the design's `slug` (`${TMPDIR:-<system temp>}/system-design-<slug>.html`) when `--out` is omitted, and rejects an unsafe slug before writing.

### Changed

- The skill description is a concise summary plus `USE for:` / `SKIP for:` routing blocks; execution detail lives in `SKILL.md`'s opening, and a contract test asserts the routing vocabulary and the absence of execution jargon.
- Invocation validation is host-agnostic: `test-skill-contract.py` is the portable gate, and `eval-invocation.py` is documented as one Claude Code adapter rather than a Claude-only requirement.
- The fork ships as `ishuiyutian/system-design-skill` with its own author, install commands, and support links.

### Fixed

- `SKILL.md` frontmatter is valid YAML again: the unquoted description contained a colon-space, which made `npx skills` fail with "Nested mappings are not allowed in compact mappings".

## 1.4.0 — 2026-10-21

### Added

- Bundled Python CLI for tracked evidence, questions, unknowns, checks, stale-write protection, source freshness, and explicit checkpoint recovery. The installed coding agent supplies reasoning; no model SDK or server is required.
- Additive investigation display in reports, including legacy coverage limitations and separate check outcomes.
- Research provenance for the evidence lifecycle and scoped verification contracts.

### Fixed

- Undecidable audit checks remain unknown instead of becoming refutations or survived attempts.
- Invocation evaluation rejects incomplete/error trials, retains optional attempt evidence, and reports unavailable costs honestly.

## 1.3.4 — 2026-10-21

### Fixed

- Treat timeouts as unknown caller observations in payment and workflow contracts, calculate recovery in time units, and include UUIDv7 as a time-ordered alternative.

## 1.3.3 — 2026-10-21

### Fixed

- Apply conversion once in unit economics, distinguish avoidable loss from gross revenue, and scope package withdrawal rules to npm.

## 1.3.2 — 2026-10-21

### Fixed

- Read and write reports explicitly as UTF-8 and report invalid Unicode through the existing diagnostic.

## 1.3.1 — 2026-10-14

### Added

- `scripts/eval-invocation.py` sends every invocation fixture to a headless Claude Code session that loads only this plugin, and grades whether the skill was invoked. Discovery is decided by the description alone, so a description change is now measured against a live agent before it ships rather than approved by reading it.

### Fixed

- A small architecture choice with numbers attached never reached the skill. The first live run passed 12 of 14 fixtures: both direct-answer cases, sharding at 20 writes per second and cache-aside versus write-through at 10 writes and 500 reads per second, were answered without invoking it in 3 of 3 runs, so the overengineering gates never ran. The description now names that ask, and all 14 cases pass in 3 of 3 runs, the five that must not invoke included.

## 1.3.0 — 2026-10-13

### Added

- A design records the code it describes. Repository runs write `context.observed` into `design.json`: the commit they read, and whether in-scope paths had uncommitted changes. A resumed run diffs from that commit and re-reads only what changed, so a drift audit of a design recorded a year ago starts from what actually moved. A commit the history no longer contains, or one read alongside uncommitted changes, leaves the drift unknown, and the run reads the whole tree.
- The skill states what a run may write: `design.json`, `DESIGN.md`, the rendered report, and at the decision step the ADR and docs-index link the user accepts. Implementing a candidate or changing code is a separate request.

## 1.2.0 — 2026-10-13

### Added

- Every ask has a stated starting point. A routing table maps what the user brings to where the run starts: a choice the numbers may settle, an existing design to resume, a change or a drift audit in the current codebase, a new system, or a pick between rendered candidates. A drift audit or a pick resumes the recorded design first rather than redrawing what was already decided.
- The run ends by answering the ask. Step 9 stopped once the report opened, and nothing said what to tell the user. A run now goes back to the ask, marks each part answered, partly answered, or open, and leads with the recommendation, the assumed inputs it rests on, the measurement that would overturn it, and what was not verified.
- Render failures map to a next step. A table in step 9 quotes the renderer's own messages and gives the meaning and the remedy for each, from a design the page cannot parse to a headless session with no way to open the report.

### Changed

- The description says when not to run. It listed every reason to fire and none to stay out, while five of the invocation fixtures expect no invocation. Explaining a technology or existing code, debugging, and code-level edits are now named as outside the skill.
- Step 7 carried two checklists that restated three of the same checks in different words. The restatements are gone, except for the recovery path, which the completion contract does not name and which stays as its own check. The debt checks, which sat in step 7 under the pre-render list, now close step 8, where the findings are produced.

### Fixed

- The render command failed wherever `TMPDIR` is unset, which includes most Linux shells: `--out "$TMPDIR/..."` became `/system-design-<slug>.html`, which any user who cannot write to `/` cannot create. The command now uses `${TMPDIR:-/tmp}`.
- A `design.json` holding `NaN`, `Infinity`, or a top-level value other than an object rendered with exit 0 and opened as the empty report template, because Python's parser accepts what the page's does not; a top-level list also crashed after writing. The renderer now refuses all of them before writing anything.
- Recording a decision set only `status`, so `decided` stayed empty and `DESIGN.md`'s frontmatter went stale. Step 10 now sets both and regenerates `DESIGN.md`.

## 1.1.1 — 2026-08-12

### Fixed

- The debt panel opened by describing itself. A hardcoded sentence under the heading said the findings were ordered by severity, cited their evidence, and had survived an attempt to disprove them — the ordering is visible, the evidence sits on every row, and the count it opened with was repeated in the live region directly beneath it. It printed on every report and told a reader nothing. The closing caveat now carries both limits a reader cannot see instead of one: that the set of findings does not converge across runs, and that nothing in the report edits the code.

## 1.1.0 — 2026-08-12

### Added

- Repository runs now audit the architecture they started from. The skill drew candidates and never graded the system already in front of it, so a codebase that had come apart from its recorded design got redrawn rather than examined. A new step compares the implemented architecture against the intended one — the recorded design and the accepted ADRs — and reports where the two have separated. Greenfield runs skip it; there is nothing implemented to audit.
- Findings have to survive being disproved. A model is an unreliable detector of architectural problems and a reliable disprover of them, so candidates are generated cheaply per category, put through gates that check whether the repository actually does the thing and whether anyone still touches it, then handed to verifiers that see the claim but never the argument behind it. Deletion is reserved for the two verdicts that make a finding factually wrong; the two that are judgement calls demote and print their objection instead, because a wrong deletion is invisible and a wrong demotion is not.
- `design.json` gains a `debt` register. `status`, `justification`, `acceptedUntil`, `firstSeen`, and `aliases` are carried forward across runs, so a finding you have accepted stays accepted; everything else is regenerated. A finding's identity is its pattern and its components and nothing else — prose is rewritten every run, and a line number moves for reasons that have nothing to do with whether it is the same finding.
- A `#debt` tab, present only when a design carries findings. Findings group by category and sort by severity then confidence, each a native disclosure whose collapsed row carries everything worth searching for. Filtering hides rows that already exist rather than rebuilding the list, so an expanded finding stays expanded, and group counts relabel to `k of N` while a filter is applied. Accepted findings and ones no longer present stay on the page in their own sections.
- The report prints. There was no print stylesheet at all, so a printed report contained whichever tab happened to be open, with every collapsed row still collapsed. Every panel and every disclosure now opens for print, and severity is a bordered text chip rather than a filled badge — browsers drop backgrounds when printing, and colour alone carries no meaning to a reader who cannot see it.

### Fixed

- Any in-page anchor threw the reader to the overview tab and scrolled to the top. The router read the whole hash as a tab name, so `#anything-else` fell through to the fallback. The tab is now the part before the first slash, and the remainder selects and opens a finding.
- The arrow keys were guarded only against text inputs, so moving between buttons on a non-architecture tab flung the reader into the architecture carousel.
- `label-occlusions` has been asserted by the browser test since 1.0.1, but `SKILL.md` and `HTML-REPORT.md` both still told a run to check four diagnostics. The documented `DESIGN.md` section order was also missing `Database schemas`, and the version invariant named two files where the contract test enforces three.

## 1.0.2 — 2026-07-31

### Changed

- The renderer opens the report itself as soon as it is written, so a finished run always ends with the report on screen. Opening was previously a separate instruction a run could skip, which left the artifact on disk for nobody to look at. `--no-open`, or `SYSTEM_DESIGN_NO_OPEN=1`, suppresses it for scripted and headless runs; a failure to open is reported and never fatal, since the file is already written.

## 1.0.1 — 2026-07-31

### Fixed

- The final step lost its own commands. The render path and the open command lived in `HTML-REPORT.md` while the step that needed them lived in `SKILL.md`, so a run that did not re-read the former wrote `design.json` and `DESIGN.md` and stopped without producing a report. Step 8 now carries a runnable block, defines the skill directory where it is used, and states that a design without a report is an unfinished run.
- The post-render check reported a parse failure that had not happened. The report title is set at run time, so the static file keeps the template placeholder; the check now reads the embedded payload instead.
- Edge labels were painted before the components and could be covered by them, and were placed with no collision test. Labels now paint last, and placement searches every segment of a route before escalating perpendicular until the label is clear of components and of other labels.
- Dragging the canvas started a native text selection that highlighted the diagram, the legend, and the sidebar. Panning now suppresses the default, and the page-level guard applies only while a pan is in flight.

### Changed

- The canonical example is a high-demand ticket on-sale: three candidate architectures, seven database schemas, and estimate rows that each reproduce.
- The browser test asserts against whatever design it is given. Component ids, schema field names, and interface contract values were literal strings from the previous example, so no other design could pass.
- New `label-occlusions` diagnostic, asserted at zero alongside the existing four.

## 1.0.0 — 2026-07-31

First public release.

### The process

- Surveys an existing repository and reconstructs its current system as Architecture 0, classifying which directories are system code before reading any of them.
- Sizes the ask before running: when a gate or a recorded decision already closes the question, it answers in a paragraph rather than manufacturing a document.
- Closes unresolved requirements through focused, recommendation-backed question rounds, and proceeds on visible defaults when no one is there to answer.
- Derives the numbers that gate the system — throughput, storage, bandwidth, concurrency, burst, skew, fan-out, availability composition, and unit economics — and verifies the arithmetic before it enters a document.
- Fixes the data and consistency model per entity before drawing anything: representation, identity, ordering authority, conflict resolution, durability point, and garbage collection.
- Draws structurally distinct candidates, three by default, compares them on invariants, numbers, failure modes, migration cost, and operability, and recommends one with a chained evidence argument.
- Resolves the two or three decisions under the greatest pressure, each recording decision, rejected alternatives, failure behaviour, and evidence.

### The reference material

- Decision rules and mechanism ladders for data models, storage engines, schema and encoding evolution, caching, replication and consistency, partitioning, transactions, streaming and time semantics, communication, and scaling.
- Archetypes indexed by the invariant they protect rather than by the product that made one famous, routed through a protected-invariant index into six packs — authoritative state, derived serving, realtime and sync, traffic and work, control and security, data delivery.
- Every archetype carries a `Not when` disqualifier and an `Anti-gate` below which its machinery is unjustified complexity, so a shape is rejected before its moves are imported.
- Provenance for every principle carrying a number lives under `docs/provenance/`, including numbers rejected during verification and the reason, so they are not quietly reintroduced.

### The artifacts

- A structured `design.json` as the source of truth, a durable `DESIGN.md` a later session can resume, and a self-contained interactive HTML report with fitted architecture canvases, conventional component shapes, obstacle-aware connectors, zoom and pan, a permanent flow sidebar, and component inspection.
- Authoritative stores declare acknowledgement, failure domain, recovery objectives, and restore path; derived views declare their source and cursor; every dependency edge declares its deadline, retry owner, and bounded backlog.

### Distribution

- MIT licensed. Works with Claude Code, Codex, Cursor, and other Agent Skills-compatible agents, as both a standalone Agent Skill and a versioned Claude Code plugin.

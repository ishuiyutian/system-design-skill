# Provenance — C4 constraints

Sources for [C4/CONSTRAINTS.md](../../../skills/system-design/C4/CONSTRAINTS.md). The catalogue's
numbered thresholds and severities are recorded here; the scoping and adaptation decisions are
product decisions for this skill.

## Scope in this skill

| Claim | Source |
|---|---|
| Each ID is Enforced, Adapted, or Retired, and the artifact is Mermaid C4Context/C4Container only | Product decision: the skill draws only context and container views with no JSON model, so JSON/dynamic/component/deployment constraints are retired and field-bearing constraints are adapted to a Mermaid or `DESIGN.md` mechanism. |
| Retired set `L5, L8, X5, X6, T1-T4, O1-O3, O5` | Product decision: `DESIGN.md` is the only artifact; there is no component/dynamic/deployment view, no JSON model, and no renderer pipeline. |
| F1/F4 description: responsibility verbs plus at most one state-contract sentence; 24-word/140-char cap | Product decision: the SAD records load-bearing RPO/RTO/failure-domain promises in authoritative store descriptions, so the strict 14-word no-invariant rule is relaxed and recorded here. |
| R2 mechanism vocabulary | Product decision: one closed list covers real transports and storage access paths so the technology field stays machine-checkable. |
| B4 locality stated in the legend | Product decision: the boundary label must stay byte-identical to the L1 system label (X3), so locality moves to the `%% legend:` line. |
| D2 auth scope | Product decision: auth posture is required at scope and named trust-boundary crossings, not on every internal process edge. |

## 1. Notation & Severity

| Claim | Source |
|---|---|
| `L` is machine-checkable, `R` requires a review gate | Product decision: separates the contract test from LLM or human judgement. |
| `B` blocks render, `M` must fix or file an exception, `m` is minor | Product decision: severity maps onto the fix loop in the regression runbook. |
| All statements are MUST unless marked SHOULD | Product decision: default to required so silence is not permission. |

## 2. Constraint Catalog

| Claim | Source |
|---|---|
| Per-ID severity (B/M/m) across S, L, E, B, R, C, F, G, X, D, T, P, V, O | Product decision: calibrated so a blocker is a correctness or render defect and a major is a fixable-or-exceptable defect. |
| Element, relationship, level, and boundary rules | [C4 model](https://c4model.com/) and [Mermaid C4 syntax](https://mermaid.js.org/syntax/c4.html) (checked 2026-11-12). |
| Numeric budgets G1 (10/12 context, 12/18/15 container) | Product decision: a wall-chart context or module-inventory container view is unreadable. |
| P provenance, C completeness, X cross-view, V variant consistency | Product decision: the model must be provably complete and consistent, not just parseable. |

## 3. Conflict Priority

| Claim | Source |
|---|---|
| Provenance/correctness outrank level purity outranks typing/boundaries outranks cross-view outranks grammar outranks budget | Product decision: a lower tier never overrides a higher one. |
| Budget never deletes a required read path | Product decision: the most common way a model "fixes" G1 is to break the model. |

## 4. Regression runbook

| Claim | Source |
|---|---|
| Validator track (L) plus review track (R), two-round fix loop, outcome recorded in the evidence register | Product decision: L checks are the contract test, R checks are a critic, blockers forbid render, and majors must be fixed or excepted. |
| A retired ID is not a finding; a missing L3/dynamic/deployment view is not a violation | Product decision: the runbook starts from the scoping table so out-of-scope constraints do not produce phantom debt. |

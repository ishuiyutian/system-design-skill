# Provenance — System Design

Sources for changed process contracts in [SKILL.md](../../skills/system-design/SKILL.md). Mechanism provenance lives in [HEURISTICS.md](HEURISTICS.md), [AUDIT.md](AUDIT.md), and [DESIGN-FORMAT.md](DESIGN-FORMAT.md).

## Route the ask

| Claim | Source |
|---|---|
| Small routing entry point and conditional reference loading | [Pinned REA router](https://github.com/morluto/rea/blob/705058f3e2df82503f1c601fc464aea7cbb626b8/.agents/skills/reverse-engineer-anything/SKILL.md); adapted to architecture work, which REA itself excludes. |

## Process

### 1. Locate and resume

| Claim | Source |
|---|---|
| Unchanged HEAD does not identify staged, unstaged, or untracked working-tree bytes | Git working-tree/index/commit distinction; runtime hashes the actual scoped source bytes. |
| `DESIGN.md` is the working document from the first step, so a later session resumes by reading the file rather than a separate store | Product decision: one source of truth, no generated copy. |

### 2. Establish the current truth

| Claim | Source |
|---|---|
| Observed, derived, and inferred evidence retains scope and limitations; unanswered questions remain explicit | [Evidence lifecycle](HEURISTICS.md#evidence-and-uncertainty). |

### 3. Close the requirement frontier

| Claim | Source |
|---|---|
| Business objectives, stakeholders, security and regulatory obligations, data classifications, and business-impact KPIs belong in the requirement frontier | Product decision: the SAD main body needs these inputs, and they can change trust boundaries, retention, or candidate viability. |

### 5. Fix the data and consistency model

| Claim | Source |
|---|---|
| Data Sets & Data Model records data impact and migration alongside entities, consistency, and schemas | Product decision: the SAD needs the migration consequence next to the model it changes. |

### 6. Draw the candidates

| Claim | Source |
|---|---|
| Structure uses one C4Context for the document and one C4Container per candidate; critical-flow behavior and dependency contracts live in Key Design Decisions | Product decision: C4 keeps structure high-level and readable, while removing flow diagrams keeps the document simple. |
| C4Container names the business system in `System_Boundary`; external services sit outside it | Product decision: generic `Edge` or `Application` boundaries hide ownership and group unlike concepts. |
| Container descriptions stay in plain business language; implementation terms go in the technology field | Product decision: the structure diagram must remain understandable to business and security reviewers. |
| Candidate records use diagrams only; per-candidate component, edge, and flow-step tables are removed | Product decision: tables duplicated the diagrams and drifted from them. |
| Container descriptions state load-bearing reliability promises in plain business language; edge contracts live in Key Design Decisions | Product decision: the structure stays readable and the contracts remain recorded. |

### 8. Audit the architecture for debt

| Claim | Source |
|---|---|
| Finder and verifier are fallible; uncertainty is neither confirmation nor refutation | [Audit pipeline provenance](AUDIT.md#the-pipeline). |

### 9. Write and verify

| Claim | Source |
|---|---|
| Structural validation, semantic review, and diagram rendering establish distinct properties | [Evidence lifecycle](HEURISTICS.md#evidence-and-uncertainty); diagram rendering only inspects presentation. |
| SAD headings, `n/a` reasons, security, data classifications, KPIs, and glossary are verified separately from architectural quality | Product decision: a complete template is not a correct design, but an incomplete one is not reviewable. |
| C4 aliases are validated in the block that declares them; container aliases are reused across candidate C4Container diagrams | Product decision: removing the component table moves alias identity into the diagrams. |
| Every container has at least one relationship | Product decision: an orphan container claims a component the design never connects. |
| Completion contract scopes dependency contracts to Key Design Decisions and store/derived-view contracts to C4 container descriptions | Product decision: a non-load-bearing detail should not force a table or a crowded diagram. |

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

### 8. Audit the architecture for debt

| Claim | Source |
|---|---|
| Finder and verifier are fallible; uncertainty is neither confirmation nor refutation | [Audit pipeline provenance](AUDIT.md#the-pipeline). |

### 9. Write and verify

| Claim | Source |
|---|---|
| Structural validation, semantic review, and diagram rendering establish distinct properties | [Evidence lifecycle](HEURISTICS.md#evidence-and-uncertainty); diagram rendering only inspects presentation. |

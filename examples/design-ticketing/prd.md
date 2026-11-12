# PRD: High-demand ticket on-sale

**Date:** 2026-11-12
**Status:** Draft

## Problem Statement

### Who has this problem?

A promoter selling tickets for one 60,000-seat venue through a single high-demand
on-sale. Fans arrive all at once — far more than there are seats — and every one of
them must leave with a seat or a definite "no".

### What is the problem?

The moment of the on-sale is a burst the backend cannot absorb at the pace seats can
be committed. Under that burst, two failures become real: the same seat sold to two
people, and a fan charged for a seat they never received. Both are unacceptable, and
today the system has no honest way to tell a fan "no" early instead of leaving them
in a retry loop.

### Why is it painful?

- **User impact:** fans wait in a queue that gives them no terminal answer, then
  discover after the fact that a seat was double-sold or that they were charged for
  nothing.
- **Business impact:** a double-sale or a charged-without-a-seat is a P0 incident
  with contractual and settlement consequences that surface months later in a
  dispute.

### Evidence

- The seat writer commits at a measured ceiling; the on-sale arrival rate exceeds
  that ceiling by more than two orders of magnitude for the first minute.
- Payment authorization and its webhook are slow, duplicated, and arrive out of
  order, so a charge can be ambiguous long after the seat decision.

## User Stories & Requirements

### Functional requirements

| id | Requirement | Priority |
|---|---|---|
| fr-1 | Queue and admit: a fan arrives, receives a draw position, and is admitted to purchase or told no | core |
| fr-2 | Select and hold: an admitted fan holds seats for the fixed hold window | core |
| fr-3 | Pay and finalize: authorize, assign seats atomically, capture, issue entitlement | core |
| fr-4 | Release: explicit release and expiry-driven reaping back to available | core |
| fr-5 | Reconcile: every payment reaches a terminal state and every captured dollar has a seat behind it | core |
| fr-6 | Non-authoritative live availability: seat map plus per-tier counters | core |
| fr-7 | Fan picks a specific seat rather than accepting best-available | stretch |

### Non-functional requirements

| Axis | Target |
|---|---|
| correctness | No seat is sold to two orders; no fan is charged without a seat; no overbooked venue |
| throughput | Survive the measured seat-commit ceiling without assuming it moves |
| elasticity | Absorb the arrival burst and sustained read load while the writer stays at its ceiling |
| latency | The admission decision is a local check; the vast majority of fans get a terminal answer within the first minute |
| durability | No committed transaction lost on one-AZ loss; bounded RPO and RTO for whole-region loss |
| auditability | The admission order is re-derivable months after the on-sale |
| availability | The purchase chain is sized to its real serial availability, not a rounded nines claim |

### Constraints

- The hold duration is fixed by the promoter contract.
- Single region, multi-AZ; no cross-region coordination on the purchase path.
- One team must be able to operate the system.

## Out of Scope

Dynamic and surge pricing · secondary market, resale, and fan-to-fan transfer ·
venue seat-map authoring and CAD · gate scanning hardware and offline turnstile
validation (the entitlement token format is in scope, the scanner is not) · scalper
and bot detection models (the enforcement hooks are in scope: per-account limits,
device-attestation slot, admission-token binding) · refunds, exchanges, and
post-event customer service · multi-currency, tax, and promoter settlement · the
pre-sale and verified-fan qualification funnel that runs days earlier.

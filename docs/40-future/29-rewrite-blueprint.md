---
status: future
scope: product
authority: this
---

# Rewrite Blueprint

> Future authority for whole-project rewrite governance. This file does not
> activate rewrite runtime in the current implementation window.

---

## 29.1 Core Position

`dev_master` should treat whole-project rewrite as a first-class governed
workflow, not as an ad hoc exception.

Rewrite is justified when the product goal remains stable but the current
implementation has become too costly, too risky, or too rigid to evolve safely.

Rewrite is always subordinate to:

- preserved business invariants
- explicit rollback paths
- capability parity evidence
- human approval for red-zone transitions

If a rewrite spans more than 3 slices, it is red-zone work by default.

---

## 29.2 Trigger Criteria

Any of the following can justify a rewrite proposal:

- health stays below 60 for 8 consecutive weeks and targeted refactors do not
  materially improve it
- lead time for a critical feature degrades by more than 50% relative to the
  recent baseline
- compatibility burden blocks core product evolution and patch/refactor cost is
  higher than rewrite cost
- security, compliance, or availability risk can no longer be controlled with
  local repair

These are proposal triggers, not auto-approval conditions.

---

## 29.3 Rewrite Proposal Minimum

A rewrite proposal must include at least:

- `proposal_id`
- `trace_id`
- owner and required human sponsors
- `rewrite_scope`
- `out_of_scope`
- preserved invariants
- success definition
- `capability_matrix`
- `migration_waves`
- `freeze_policy`
- `retirement_gates`
- `knowledge_transfer`

If any of these are missing, the proposal is incomplete and cannot govern a
traffic move.

---

## 29.4 Capability Matrix

Capability parity must be explicit rather than implied.

Minimum shape:

```markdown
# Capability Matrix

| capability_id | capability_name | old_system_status | new_system_status | evidence | gap | severity | owner | target_wave |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAP-001 | Core flow | serving | partial | tests/e2e/flow.md | refund branch missing | blocking | owner | wave-2 |
```

Severity rules:

- `blocking`: must be closed before formal traffic cutover
- `high`: must be closed before full traffic
- `medium`: may move with explicit tracking, but must be closed before
  retirement
- `low`: becomes managed debt after cutover

---

## 29.5 Migration Waves

Rewrite migration should progress through four waves:

| Wave | Goal | Traffic mode | Rollback posture |
|------|------|--------------|------------------|
| `Wave 0: Shadow` | mirror behavior with no user impact | mirrored only | stop mirroring |
| `Wave 1: Internal` | prove internal use and dual-write safety | internal only | switch primary write back |
| `Wave 2: Low-Risk` | prove low-risk real traffic | 5-10% or equivalent low-risk cohort | revert to old primary read/write |
| `Wave 3: Primary` | make new system the main path | 50-100% with guarded fallback | restore old system as primary if needed |

Wave rules:

- no cross-wave hard cut
- each wave must have explicit validation criteria
- each wave must have rollback rehearsal evidence
- blocking capability gaps stop wave promotion

---

## 29.6 Freeze Policy

Rewrite should not coexist with unrelated broad expansion.

Minimum freeze buckets:

- fully frozen: cross-slice feature expansion, unnecessary large data-model
  changes, unrelated major dependency jumps
- conditionally allowed: P0/P1 fixes, compliance/security repairs, compatibility
  work required by the rewrite itself
- normally allowed: documentation, tests, observability improvements

Disputed changes should default to the stricter zone.

---

## 29.7 Retirement Gates

Old-system retirement requires all of the following:

- all `blocking` capability gaps are closed
- key reconciliation error stays below threshold
- 14 consecutive days require no forced rollback
- runbooks, dashboards, alerts, and audit paths point to the new system
- old-system data is read-only or archived
- knowledge transfer is completed and human-signed
- retirement rehearsal is complete

Retirement without these gates is not valid.

---

## 29.8 Knowledge Transfer

Knowledge transfer is part of rewrite completion, not an optional appendix.

Minimum checklist:

- ADRs
- incident postmortems
- boundary exceptions
- security exceptions
- PII special cases
- ignored rule justifications
- dependency replacement history
- runbooks
- historical rollback reasons

Required questions:

- why was the old decision made at the time?
- which assumptions are now invalid?
- which gates were added after incidents?
- which old-system traps must never be repeated?

---

## 29.9 Rewrite Audit Records

Rewrite should emit dedicated audit files:

- `audit/rewrite-decisions.jsonl`
- `audit/rewrite-validation.jsonl`
- `audit/rewrite-cutovers.jsonl`
- `audit/rewrite-retirement.jsonl`

Every wave transition should record at least:

- `trace_id`
- `proposal_id`
- `wave_id`
- `old_system_version`
- `new_system_version`
- `rollback_ready`
- `validation_summary`

If wave transitions are not auditable, the rewrite is not governed.

---

## 29.10 Non-Goals

This blueprint does not authorize:

- current-window rewrite runtime
- auto-cutover without human approval
- bypassing capability parity
- replacing `menmery` governance
- replacing `auto_router` routing or model control-plane behavior

---
status: active
scope: window
authority: this
---

# Autonomy Ratchet

This file defines how `dev_master` may grow with AI capability without freezing
the product at one dated model assumption. It is an active current-window
contract. Changing this file is a red-line governance action.

Ratchet contract edits must be human-initiated and explicitly human-approved.
AI must not initiate, draft, submit, or auto-apply threshold or boundary changes
to this file as an autonomous task. AI may collect evidence or apply an
explicit human-specified edit; it must not use the ratchet to change the
ratchet.

The ratchet may automatically widen green local parameters when evidence is
good enough. It may not cross hard red lines or silently upgrade product tier.
Every promotion or demotion writes an append-only decision record.

---

## 1. Capability Tiers

| Tier | Meaning |
|------|---------|
| `L1` | bounded local artifact or clickable prototype |
| `L1.5` | queued 24/7 execution with async review, cost ceilings, and multi-project scheduling |
| `L2-assisted` | AI prepares PRs, verifier reports, risk labels, and recommendations for real product work; humans decide critical changes |

`L2-full-auto` and `L3-full-auto` are outside the ratchet. They require a new
human-approved product decision, not an automatic promotion.

---

## 2. Metrics

Ratchet decisions must reference a fixed metric window. Minimum metrics:

| Metric | Meaning |
|--------|---------|
| `full_loop_success_rate` | completed runs that satisfied request, checks, verifier, and evidence |
| `self_correction_success_rate` | runs where AI recovered from a bounded failure without widening scope |
| `unattended_stability_minutes_p95` | p95 continuous run time before verifier/human correction was needed |
| `verifier_false_allow_rate` | verifier allowed a run that later evidence marked wrong |
| `verifier_false_block_rate` | verifier blocked a run later confirmed acceptable |
| `risk_misclassification_rate` | risk label disagreed with labeled fixture or human review |
| `evidence_integrity_failure_rate` | missing, mutable, or untied evidence refs |
| `cost_ceiling_violation_rate` | attempts to exceed configured hard budget ceiling |

Metric ownership:

- Execution runner emits per-run `ratchet_metrics_contribution` facts.
- Verifier validates whether the per-run metric contribution is complete,
  explicit `null`, or inconsistent with evidence.
- Ratchet evaluator aggregates append-only metric windows from verified runs.

Every run must either contribute metric facts or record `null` with a reason.
Missing metric contribution is an evidence defect.

Minimum metric window for promotion:

```yaml
minimum_runs: 20
minimum_distinct_days: 3
required_evidence_refs: true
```

---

## 3. Automatic Local Widening

If the metric window satisfies the promotion threshold, the system may widen
only these green local parameters without a new activation proposal:

| Parameter | Initial limit | Max automatic limit |
|-----------|---------------|---------------------|
| `bounded_slice_files` | 3 files | 8 files |
| `bounded_slice_lines_changed` | 200 lines | 600 lines |
| `unattended_run_minutes` | 30 minutes | 90 minutes |
| `green_queue_parallelism` | 1 run | 3 runs |

Promotion threshold:

```yaml
full_loop_success_rate: ">= 0.95"
self_correction_success_rate: ">= 0.80"
verifier_false_allow_rate: "== 0"
risk_misclassification_rate: "< 0.05"
evidence_integrity_failure_rate: "== 0"
cost_ceiling_violation_rate: "== 0"
```

Local widening must still emit an append-only ratchet decision record.

These thresholds are starting calibrations. Adjusting them is a red-line edit
and requires evidence that the new thresholds preserve verifier integrity at
least as well as the old thresholds.

---

## 4. Tier Promotion

Tier promotion does not need a new activation proposal when it stays within
this file, but it must write an append-only decision record before becoming
effective.

Allowed automatic promotions:

- `L1` -> `L1.5` when local artifact/prototype runs meet the promotion
  threshold and the async review inbox plus cost ceilings are active.
- `L1.5` -> `L2-assisted` only for PR preparation and review payloads, never
  merge, deploy, paid action, secrets, permissions, or compliance decisions.

Required record shape:

```yaml
ratchet_id: "ratchet_..."
record_type: "promotion|demotion|local_widening|local_tightening"
from_tier: "L1"
to_tier: "L1.5"
triggered_by_metrics:
  full_loop_success_rate: 0.96
  risk_misclassification_rate: 0.02
metric_window:
  run_ids: ["run_..."]
  started_at: "2026-04-30T00:00:00Z"
  ended_at: "2026-05-03T00:00:00Z"
evidence_refs:
  - "ev_..."
effective_at: "2026-05-03T00:00:00Z"
reversible_by:
  - "verifier_false_allow_rate > 0"
  - "risk_misclassification_rate >= 0.05"
schema_version: "1.0.0"
policy_version: "autonomy-ratchet-v1"
ruleset_version: "ratchet-rules-v1"
```

Records are append-only. A later demotion or correction must add a new record;
it must not mutate the original record.

---

## 5. Hard Red Lines

The ratchet never auto-approves:

- production deploy
- merge to protected branch
- external PR merge
- secrets or credential changes
- permission, authz, tenant isolation, or compliance boundary changes
- payment, procurement, subscription, or paid side effects
- production data migration or deletion
- public release, rollback, or canary promotion
- model routing hard-policy changes owned by `auto_router`

These remain human-governed regardless of model capability.

---

## 6. Demotion

Demotion is automatic and also append-only. Any of these triggers must tighten
the current ratchet level before the next queued run:

```yaml
verifier_false_allow_rate: "> 0"
risk_misclassification_rate: ">= 0.05"
evidence_integrity_failure_rate: "> 0"
cost_ceiling_violation_rate: "> 0"
provider_drift_detected: "> 0"
red_line_attempted: true
human_override: "demote"
```

Demotion records use the same schema as promotion records with
`record_type: "demotion"` or `record_type: "local_tightening"`.

---

## 7. Storage

Ratchet records should be written to an append-only local evidence path before
any optional service writeback:

```text
evidence/ratchet-decisions.jsonl
```

Optional `menmery` writeback may mirror the record, but local append-only
evidence remains required.

---
status: active
scope: window
authority: this
---

# AI Cold Start Base

> Active Core. This file defines the repository-level AI entry path. It is not
> product runtime. It exists so an AI entering the repo can quickly understand
> the current phase, allowed work, required evidence, and stop conditions.

---

## 24.1 Cold Start Goal

The cold start baseline is high enough when a new AI session can answer these
questions without guessing:

- what this repository is and is not
- what phase is active now
- what task is currently allowed
- what files are authoritative
- whether implementation is currently allowed
- what language baseline is only historical/candidate until rewrite approval
- what evidence must be produced before moving on
- when to stop, escalate, or create an activation proposal

The goal is not to pre-decide every future implementation detail. The goal is
to make the next valid action obvious and auditable.

---

## 24.2 Required Entry Sequence

An AI working in this repository must start in this order:

1. Read `AGENTS.md`.
2. Read this file.
3. Read `CONTRACTS.md` when the task touches machine-readable artifacts,
   runner facts, verifier outputs, or version governance.
4. Read `26-design-closure-review.md`.
5. Read `REWRITE-PLAN.md` when the task concerns rewrite planning or future
   implementation reactivation.
6. Read `00-index.md`.
7. Read `20-layered-program-map.md`.
8. Read `23-menmery-integration.md`.
9. Read `27-external-systems-boundary.md`.
10. Read `28-product-principles.md`.
11. Read `recovered/AI-autonomous-dev-pipeline-v3.md` only when mining stale
   historical ideas; do not treat it as current authority.
12. Read `25-implementation-language-baseline.md` as historical baseline only;
   do not implement from it until the rewrite plan is approved.
13. If the task concerns future-only blueprint work, read
   `12-disaster-recovery.md` plus the relevant future authority:
   `29-rewrite-blueprint.md`,
   `30-project-adapter-blueprint.md`, or
   `31-external-model-governance-integration.md`.
14. If executing a docs-only task, read `17-task-templates.md` and
   `18-master-execution-task.md`.

If these files conflict, the stricter boundary wins and the conflict becomes a
drift-check item.

---

## 24.3 Repository AI Base Artifacts

| Artifact | Purpose |
|----------|---------|
| `CONTRACTS.md` | Authority for machine-readable contract/version discipline. |
| `26-design-closure-review.md` | Current docs-only state, closure decisions, and next allowed action. |
| `REWRITE-PLAN.md` | Current draft for the first post-reset executable slice. |
| `recovered/AI-autonomous-dev-pipeline-v3.md` | Outdated historical reference for idea mining only. |
| `25-implementation-language-baseline.md` | Historical/candidate language baseline, not active implementation approval. |

Implementation scaffolding was intentionally deleted on 2026-04-27. Until a
human approves a rewrite slice, this repository is docs-only.

---

## 24.4 Current Decision Model

Use this decision order:

1. If `26-design-closure-review.md` names an active docs-only task, execute only that task.
2. If the task is rewrite planning or implementation-reactivation planning, use
   `REWRITE-PLAN.md` as the current draft and update that artifact rather than
   inventing a parallel plan.
3. If the task is docs-only, use the docs plane and produce local evidence.
4. If the task would recreate non-doc implementation assets, first use the
   `menmery` facade through `entry_turn`; use a message shaped like
   `software_change / dev_master / <target repo> / <goal>` with
   `max_depth="auto"`. Follow its returned recommended call when deeper
   context or governance preview is needed.
5. If the `menmery` facade is unavailable, mark the task as fallback and keep
   the evidence local until writeback is possible.
6. If the requested work activates deferred or future capabilities, create an
   activation proposal instead of implementation.
7. If a gate condition is unclear, run drift-check before continuing.

---

## 24.5 Command Surface

There is no active command surface after the implementation reset. `justfile`
and check scripts were removed intentionally.

Allowed verification before rewrite:

- read files
- inspect `git status`
- list non-markdown files
- write markdown reports only

---

## 24.6 Required End-Of-Turn Record

Every substantive AI session must report:

- `current_phase`
- `task_executed`
- `artifacts_changed`
- `evidence_collected`
- `menmery_context_used`
- `menmery_entry_turn_id` when one exists
- `plane_boundary_check`
- `risk_facts`
- `drift_found`
- `decision`
- `recommendation_for_human`
- `next_allowed_action`

This mirrors `18-master-execution-task.md` and makes cold-start state reusable
by the next AI session.

---

## 24.7 Maintenance Rule

When the repository changes, update these together when applicable:

- `26-design-closure-review.md`
- `REWRITE-PLAN.md`
- `00-index.md` / `20-layered-program-map.md` if active boundaries changed

Do not update cold-start artifacts to make a failing task look successful.
Failures must be represented as drift, correction, hold, or fallback.

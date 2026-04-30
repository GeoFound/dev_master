---
status: active
scope: window
authority: this
---

# AI Cold Start Base

> Active Core. This file defines the repository-level AI entry path for a
> blueprint-driven rebuild program. It is not product runtime. It exists so an
> AI entering the repo can quickly understand the current phase, active build
> slice, required evidence, and stop conditions without mistaking the blueprint
> for the finished product.

---

## 24.1 Cold Start Goal

The cold start baseline is high enough when a new AI session can answer these
questions without guessing:

- what this repository is and is not
- what phase is active now
- what task is currently allowed
- what files are authoritative
- whether implementation is currently allowed
- what language baseline is approved for Phase 1-4
- what evidence must be produced before moving on
- when to stop, escalate, or create an activation proposal

The goal is not to pre-decide every future implementation detail. The goal is
to make the next valid action obvious and auditable.

---

## 24.2 Required Entry Sequence

An AI working in this repository must start in this order:

1. Read `AGENTS.md`.
2. Read this file.
3. Read `docs/00-entry/26-design-closure-review.md`.
4. Read `docs/00-entry/00-index.md`.
5. Read the product identity group:
   `docs/10-product/28-product-principles.md`,
   `docs/10-product/product-architecture-decision.md`,
   `docs/20-current-window/20-layered-program-map.md`, and
   `docs/30-integrations/27-external-systems-boundary.md`.
6. Read `docs/20-current-window/REWRITE-PLAN.md` when the task concerns
   rewrite planning, implementation reactivation, or the Phase 1 executable
   path.
7. Read `docs/10-product/CONTRACTS.md` when the task touches machine-readable
   artifacts, runner facts, verifier outputs, task proposals, or version
   governance.
8. Read the governance and boundary group when relevant:
   `docs/10-product/engineering-execution-boundaries.md`,
   `docs/10-product/task-proposal-contract.md`,
   `docs/20-current-window/autonomy-ratchet.md`,
   `docs/20-current-window/human-review-inbox.md`, and
   `docs/20-current-window/cost-ceilings.md`.
9. Read `docs/20-current-window/25-implementation-language-baseline.md` before
   adding implementation files or changing language ownership.
10. Read `docs/30-integrations/23-menmery-integration.md` when optional
    `menmery` service consumption is relevant.
11. Read `docs/90-reference/durable-ideas-from-v3.md` only when checking where
    old recovered ideas were mapped; do not treat it as current authority.
12. If the task concerns future-only blueprint work, read
   `docs/40-future/12-disaster-recovery.md` plus the relevant future authority:
   `docs/40-future/29-rewrite-blueprint.md`,
   `docs/40-future/30-project-adapter-blueprint.md`, or
   `docs/40-future/31-external-model-governance-integration.md`.
13. Read `docs/20-current-window/17-task-templates.md` and
    `docs/20-current-window/18-master-execution-task.md` before deriving,
    executing, verifying, or closing any task.
14. Read `runtime/current-task.json` and `runtime/program-state.json` to
    see the machine-readable current task and gate state before inventing a new
    task.
15. Read `runtime/implementation-spine.json` when deciding build order, so
    long sessions do not reconstruct the factory spine from memory.

If these files conflict, the stricter boundary wins and the conflict becomes a
drift-check item.

---

## 24.3 Repository AI Base Artifacts

| Artifact | Purpose |
|----------|---------|
| `docs/10-product/CONTRACTS.md` | Authority for machine-readable contract/version discipline. |
| `docs/00-entry/26-design-closure-review.md` | Post-reset rebuild baseline, closure decisions, and next allowed action. |
| `docs/20-current-window/REWRITE-PLAN.md` | Current draft for the first post-reset executable slice. |
| `docs/10-product/product-architecture-decision.md` | Product runtime shape, language split, surfaces, provider strategy, and default deployment. |
| `docs/10-product/task-proposal-contract.md` | Machine-checkable AI proposal to `dev_master` authorization handoff. |
| `docs/10-product/engineering-execution-boundaries.md` | Dynamic implementation boundaries and quality floors. |
| `docs/20-current-window/autonomy-ratchet.md` | Evidence-based autonomy widening, demotion, and hard red lines. |
| `docs/20-current-window/human-review-inbox.md` | Async human review queue and timeout defaults. |
| `docs/20-current-window/cost-ceilings.md` | Current-window hard cost ceilings. |
| `runtime/current-task.json` | Current machine-readable bounded task derived from the active blueprint. |
| `runtime/program-state.json` | Current phase, gate, and task progression state. |
| `runtime/implementation-spine.json` | Persisted implementation spine and anti-drift build order. |
| `docs/90-reference/durable-ideas-from-v3.md` | Short index of old v3 ideas and their current destinations. |
| `docs/20-current-window/25-implementation-language-baseline.md` | Active Phase 1-4 implementation language baseline. |

Implementation scaffolding was intentionally deleted on 2026-04-27. Until
replacement slices are rebuilt, the blueprint docs remain the construction
authority. This must not be read as "the repository exists only to maintain
documentation".

---

## 24.4 Current Decision Model

Use this decision order:

1. Determine the task type from `docs/20-current-window/17-task-templates.md`,
   `docs/20-current-window/18-master-execution-task.md`, and the current phase/gate state.
2. Use `docs/00-entry/26-design-closure-review.md` as a rebuild-boundary file: it defines
   what stale assets are invalid and what constraints still apply, but it does
   not turn the repository into a documentation-maintenance end state.
3. If `docs/20-current-window/REWRITE-PLAN.md`, `docs/20-current-window/14-master-program.md`, and `docs/20-current-window/15-phase-gates.md`
   already define a bounded implementation slice for the current gate, derive
   the next build-task from them and implement that slice with evidence. Prefer
   the existing machine-readable task in `runtime/current-task.json` unless
   drift proves it stale or incomplete.
4. If docs are ambiguous enough to block implementation, repair the blocking
   authority docs first, then return to the build program.
5. If the task would recreate non-doc implementation assets, first decide
   whether it needs optional sibling services. Use the `menmery` facade through
   `entry_turn` only when deeper context or governance preview is useful.
6. If an optional service is unavailable, mark the task as fallback and keep
   the evidence local until service writeback is possible or unnecessary.
7. If the requested work activates deferred or future capabilities, create an
   activation proposal instead of implementation.
8. If a gate condition is unclear, run drift-check before continuing.

---

## 24.5 Command Surface

There is no inherited active command surface after the implementation reset.
`justfile` and earlier check scripts were removed intentionally.

Allowed work before a replacement command surface exists:

- read files and inspect `git status`
- derive tasks from active authority docs
- write code, scripts, and reports required by the current approved slice
- run bounded local checks introduced by the current slice
- produce markdown reports only when the current task or gate requires them

Current rebuilt command surface:

- `python3 bin/derive_next_task.py`
- `python3 bin/complete_task.py --status ... --decision ... --summary ... --recommendation-for-human ...`

---

## 24.6 Required End-Of-Turn Record

Every substantive AI session must report:

- `current_phase`
- `task_executed`
- `artifacts_changed`
- `evidence_collected`
- `service_context_used`
- service request IDs or entry-turn IDs when they exist
- `plane_boundary_check`
- `risk_facts`
- `drift_found`
- `decision`
- `recommendation_for_human`
- `next_allowed_action`

This mirrors `docs/20-current-window/18-master-execution-task.md` and makes cold-start state reusable
by the next AI session.

---

## 24.7 Maintenance Rule

When the repository changes, update these together when applicable:

- `docs/00-entry/26-design-closure-review.md`
- `docs/20-current-window/REWRITE-PLAN.md`
- `docs/00-entry/00-index.md` / `docs/20-current-window/20-layered-program-map.md` if active boundaries changed

Do not update cold-start artifacts to make a failing task look successful.
Failures must be represented as drift, correction, hold, or fallback.

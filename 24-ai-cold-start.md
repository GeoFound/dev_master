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
- what commands validate the repository guardrails
- what language baseline applies to Phase 1 implementation
- what evidence must be produced before moving on
- when to stop, escalate, or create an activation proposal

The goal is not to pre-decide every future implementation detail. The goal is
to make the next valid action obvious and auditable.

---

## 24.2 Required Entry Sequence

An AI working in this repository must start in this order:

1. Read `AGENTS.md`.
2. Read this file.
3. Read `tasks/current.md`.
4. Read `00-index.md`.
5. Read `20-layered-program-map.md`.
6. Read `23-menmery-integration.md`.
7. Read `25-implementation-language-baseline.md` before implementation work.
8. If executing a task, read `17-task-templates.md` and
   `18-master-execution-task.md`.
9. Run `just check` before proposing a gate decision.

If these files conflict, the stricter boundary wins and the conflict becomes a
drift-check item.

---

## 24.3 Repository AI Base Artifacts

| Artifact | Purpose |
|----------|---------|
| `tasks/current.md` | The next allowed task and phase state. |
| `tasks/backlog.md` | Ordered non-binding task backlog. |
| `templates/` | Required report and task shapes. |
| `contracts/software-change-runner-v1.yaml` | Runner facts contract reference. |
| `25-implementation-language-baseline.md` | Phase 1 language and file-format baseline. |
| `reports/` | Local evidence and gate reports. |
| `scripts/check_ai_base.sh` | Repository guardrail validation. |
| `justfile` | Stable command surface for AI sessions. |

These artifacts are repository automation and evidence scaffolding. They do not
create a product runtime, canonical store, approval controller, or model router.

---

## 24.4 Current Decision Model

Use this decision order:

1. If `tasks/current.md` names an active task, execute only that task.
2. If the task is docs-only, use the docs plane and produce local evidence.
3. If the task mutates non-doc implementation assets, first use the `menmery`
   facade: `get_context(...)` then `act(intent="software_change", ...)`.
4. If the `menmery` facade is unavailable, mark the task as fallback and keep
   the evidence local until writeback is possible.
5. If the requested work activates deferred or future capabilities, create an
   activation proposal instead of implementation.
6. If a gate condition is unclear, run drift-check before continuing.

---

## 24.5 Standard Command Surface

```bash
just check
just cold-start
just validate-contract
just drift-check
just gate-a
```

Command meanings:

| Command | Meaning |
|---------|---------|
| `just check` | Validate repo guardrails and required AI base files. |
| `just cold-start` | Print the cold-start path after validation. |
| `just validate-contract` | Validate runner contract references. |
| `just drift-check` | Validate drift-check evidence exists and guardrails pass. |
| `just gate-a` | Validate Gate A report evidence and guardrails. |

---

## 24.6 Required End-Of-Turn Record

Every substantive AI session must report:

- `current_phase`
- `task_executed`
- `artifacts_changed`
- `evidence_collected`
- `menmery_context_used`
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

- `tasks/current.md`
- relevant `templates/`
- relevant `contracts/`
- `reports/` evidence
- `justfile`
- `scripts/check_ai_base.sh`
- `00-index.md` / `20-layered-program-map.md` if active boundaries changed

Do not update cold-start artifacts to make a failing task look successful.
Failures must be represented as drift, correction, hold, or fallback.

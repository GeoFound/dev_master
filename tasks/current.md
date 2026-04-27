# Current Task

> Authoritative local task pointer for AI cold start. This file tells a new AI
> session what it is allowed to do next without re-deriving the program state
> from all architecture docs.

---

## State

```yaml
current_phase: "Phase 0 - Design Freeze"
current_gate: "Gate A"
current_layer: "Active Core"
program_limit: "Phase 0-3 only"
menmery_context_status: "not_called_local_gate_package"
last_completed_task: "phase-0-ai-cold-start-base"
last_completed_task_2: "phase-0-implementation-language-baseline"
last_updated: "2026-04-27"
```

---

## Active Task

```yaml
task_id: "gate-a-design-freeze-review"
task_type: "verify-task"
plane: "verification"
goal: "Verify Gate A evidence and submit the design-freeze recommendation to the human. Do not start Phase 1 until a human promote decision exists."
scope_in:
  - "Gate A report"
  - "AI cold-start base evidence"
  - "implementation language baseline"
  - "drift-check report"
  - "runner contract reference"
  - "repository guardrail commands"
scope_out:
  - "Phase 1 implementation before human promote"
  - "product runtime implementation"
  - "parallel canonical evidence store"
  - "approval controller"
  - "deferred/future capability activation"
dependencies:
  - "AGENTS.md"
  - "00-index.md"
  - "20-layered-program-map.md"
  - "23-menmery-integration.md"
  - "24-ai-cold-start.md"
  - "25-implementation-language-baseline.md"
  - "15-phase-gates.md"
deliverables:
  - "Gate A recommendation to human"
  - "updated tasks/current.md only if human decision changes phase state"
acceptance_checks:
  - "just check passes"
  - "just validate-contract passes"
  - "just drift-check passes"
  - "just gate-a passes"
  - "Phase 1 language baseline is explicit and checked"
rollback_if_failed: "Hold at Gate A and create a correction-task."
side_effects:
  repo_mutation: false
  shell_execution: true
  external_service_calls: false
  evidence_write: "none unless correcting reports"
evidence_outputs:
  - "reports/gate-a-design-freeze.md"
  - "reports/drift/2026-04-27-ai-cold-start-base.md"
risk_facts:
  action_level: 2
  risk_label: "green"
  docs_only: false
  repo_local_ai_scaffold: true
  dependency_changed: false
  secrets_or_permissions_changed: false
  infra_or_deploy_path_changed: false
menmery_context: "No menmery facade call used for this local Gate A package; no canonical evidence writeback claimed."
```

---

## Next Allowed Actions

1. Run `just check`, `just validate-contract`, `just drift-check`, and
   `just gate-a`.
2. Submit Gate A recommendation to the human.
3. Only after a human `promote` decision, replace this file with the Phase 1
   first executable kernel task.

---

## Stop Conditions

Stop and create a correction-task if:

- an active doc implies a parallel truth/governance/evidence runtime
- a deferred or future capability becomes an implementation deliverable
- the runner contract gains dev_master-owned governance or schema authority
- a report claims `menmery` writeback without a real reference
- `just check` fails

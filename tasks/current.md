# Current Task

> Authoritative local task pointer for AI cold start. This file tells a new AI
> session what it is allowed to do next without re-deriving the program state
> from all architecture docs.

---

## State

```yaml
current_phase: "Phase 2 - Green Reliability"
current_gate: "Gate C"
current_layer: "Active Core"
program_limit: "Phase 0-3 only"
menmery_context_status: "mcp_get_context_deep_and_act_supervised"
last_gate_decision: "Gate A promote by human on 2026-04-27"
last_gate_decision_2: "Gate B promote by human on 2026-04-27"
last_completed_task: "phase-0-ai-cold-start-base"
last_completed_task_2: "phase-0-implementation-language-baseline"
last_completed_task_3: "phase-1-first-executable-kernel-slice"
last_completed_task_4: "phase-1-low-risk-loop-probe"
last_completed_task_5: "gate-b-evidence-review"
last_completed_task_6: "gate-b-human-decision-promote"
last_updated: "2026-04-27"
```

---

## Active Task

```yaml
task_id: "phase-2-green-reliability-sample-plan"
task_type: "verify-task"
plane: "verification"
goal: "Define the bounded Phase 2 Green Reliability sample window and metrics before running additional samples. Gate C remains pending."
scope_in:
  - "Gate C pass/fail conditions"
  - "green docs/test-only sample criteria"
  - "full-loop success count"
  - "verifier block rate"
  - "evidence writeback failure count"
  - "risk misclassification count"
scope_out:
  - "Gate C promotion"
  - "yellow task execution"
  - "dependencies, infra, secrets, permissions, deploy, merge, or migrations"
  - "auto-approval"
  - "new orchestration platform"
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
  - "04-pipeline.md"
  - "05-quality.md"
  - "15-phase-gates.md"
  - "reports/phase1/gate-b-evidence-review.md"
  - "reports/phase1/gate-b-promotion.md"
deliverables:
  - "Phase 2 Green Reliability sample plan or report"
  - "metrics definitions aligned with Gate C"
acceptance_checks:
  - "just check passes"
  - "just phase1-check passes"
  - "Gate C remains pending"
rollback_if_failed: "Hold Phase 2 sample execution and create a correction-task."
side_effects:
  repo_mutation: true
  shell_execution: true
  external_service_calls: "menmery get_context/act/remember only"
  evidence_write: "local Phase 2 planning evidence only"
evidence_outputs:
  - "reports/phase1/gate-b-evidence-review.md"
  - "menmery record fct_20260427082346744201_state"
  - "reports/phase1/gate-b-promotion.md"
risk_facts:
  action_level: 1
  risk_label: "green"
  docs_only: false
  repo_local_ai_scaffold: true
  dependency_changed: false
  secrets_or_permissions_changed: false
  infra_or_deploy_path_changed: false
menmery_context: "Gate B promoted by explicit human decision; Phase 2 may begin with Green Reliability sample planning while Gate C remains pending."
```

---

## Next Allowed Actions

1. Create a bounded Phase 2 Green Reliability sample plan.
2. Use only green docs/test-only tasks for sample execution.
3. Track full-loop success count, verifier block rate, evidence writeback
   failure count, and risk misclassification count.
4. Keep Gate C pending until the sample window is complete and reviewed.

---

## Stop Conditions

Stop and create a correction-task if:

- an active doc implies a parallel truth/governance/evidence runtime
- a deferred or future capability becomes an implementation deliverable
- the runner contract gains dev_master-owned governance or schema authority
- a report claims `menmery` writeback without a real reference
- verifier fails to block the forced bad case
- Phase 2 sample work includes dependencies, infra, secrets, permissions,
  deploy, merge, or migrations
- Gate C is promoted without a separate human decision
- `just check` fails

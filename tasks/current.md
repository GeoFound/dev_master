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
last_completed_task_7: "phase-2-green-reliability-sample-plan"
last_updated: "2026-04-27"
```

---

## Active Task

```yaml
task_id: "phase-2-green-sample-01"
task_type: "build-task"
plane: "execution"
goal: "Run the first bounded Phase 2 green sample through get_context -> act -> local runner facts -> verifier -> remember, then record metrics. Gate C remains pending."
scope_in:
  - "one docs-only or test-only bounded change"
  - "Phase 2 sample record shape"
  - "runner facts artifact"
  - "verifier artifact and decision"
  - "menmery evidence writeback"
  - "sample metrics update"
scope_out:
  - "Gate C promotion"
  - "yellow task execution"
  - "dependencies, infra, secrets, permissions, deploy, merge, or migrations"
  - "auto-approval"
  - "new orchestration platform"
  - "parallel canonical evidence store"
  - "approval controller"
  - "new forced-bad fixtures unless a correction-task requires one"
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
  - "reports/phase2/phase2-green-reliability-sample-plan.md"
deliverables:
  - "Phase 2 green sample 01 local evidence report"
  - "runner facts artifact"
  - "verifier artifact"
  - "menmery writeback reference"
acceptance_checks:
  - "just check passes"
  - "just phase1-check passes"
  - "sample remains green under the Phase 2 sample plan"
  - "Gate C remains pending"
rollback_if_failed: "Do not count the sample; create a correction-task or blocked sample report."
side_effects:
  repo_mutation: true
  shell_execution: true
  external_service_calls: "menmery get_context/act/remember only"
  evidence_write: "local Phase 2 sample evidence plus menmery writeback"
evidence_outputs:
  - "reports/phase1/gate-b-evidence-review.md"
  - "menmery record fct_20260427082346744201_state"
  - "reports/phase1/gate-b-promotion.md"
  - "reports/phase2/phase2-green-reliability-sample-plan.md"
risk_facts:
  action_level: 2
  risk_label: "green"
  docs_only: true
  repo_local_ai_scaffold: true
  dependency_changed: false
  secrets_or_permissions_changed: false
  infra_or_deploy_path_changed: false
menmery_context: "Gate B promoted; Phase 2 sample plan complete; next task is first bounded green sample with Gate C pending."
```

---

## Next Allowed Actions

1. Execute `phase-2-green-sample-01` using only docs-only or test-only scope.
2. Reject the sample if it touches dependencies, infra, secrets, permissions,
   deploy, merge, migrations, or external writes beyond `menmery` writeback.
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

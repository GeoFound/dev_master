# Current Task

> Authoritative local task pointer for AI cold start. This file tells a new AI
> session what it is allowed to do next without re-deriving the program state
> from all architecture docs.

---

## State

```yaml
current_phase: "Phase 1 - First Executable Kernel"
current_gate: "Gate B"
current_layer: "Active Core"
program_limit: "Phase 0-3 only"
menmery_context_status: "mcp_get_context_deep_and_act_supervised"
last_gate_decision: "Gate A promote by human on 2026-04-27"
last_completed_task: "phase-0-ai-cold-start-base"
last_completed_task_2: "phase-0-implementation-language-baseline"
last_completed_task_3: "phase-1-first-executable-kernel-slice"
last_completed_task_4: "phase-1-low-risk-loop-probe"
last_completed_task_5: "gate-b-evidence-review"
last_updated: "2026-04-27"
```

---

## Active Task

```yaml
task_id: "gate-b-human-decision"
task_type: "verify-task"
plane: "verification"
goal: "Wait for explicit human Gate B decision: promote, hold, or correct. Do not continue implementation work until that decision is recorded."
scope_in:
  - "Gate B evidence review"
  - "human decision"
  - "promote | hold | correct"
scope_out:
  - "automatic Gate B promotion"
  - "new Phase 1 loops"
  - "new fixtures"
  - "Phase 2 work before explicit promote"
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
deliverables:
  - "recorded human Gate B decision"
  - "updated tasks/current.md after decision"
acceptance_checks:
  - "just check passes"
  - "just phase1-check passes"
  - "Gate B evidence review remains reviewed_not_promoted until human decision"
rollback_if_failed: "Hold at Phase 1 and create a correction-task."
side_effects:
  repo_mutation: false
  shell_execution: true
  external_service_calls: "menmery get_context/act/remember only"
  evidence_write: "none unless recording the human decision"
evidence_outputs:
  - "reports/phase1/gate-b-evidence-review.md"
  - "menmery record fct_20260427082346744201_state"
risk_facts:
  action_level: 1
  risk_label: "green"
  docs_only: false
  repo_local_ai_scaffold: true
  dependency_changed: false
  secrets_or_permissions_changed: false
  infra_or_deploy_path_changed: false
menmery_context: "Gate B evidence review complete; waiting for explicit human promote/hold/correct decision."
```

---

## Next Allowed Actions

1. Ask human for explicit Gate B decision:
   `promote`, `hold`, or `correct`.
2. If `promote`, update phase to Phase 2 Green Reliability.
3. If `hold`, keep Phase 1 and record what additional observation is needed.
4. If `correct`, create a correction-task for the specific invalid evidence or
   judgment.

---

## Stop Conditions

Stop and create a correction-task if:

- an active doc implies a parallel truth/governance/evidence runtime
- a deferred or future capability becomes an implementation deliverable
- the runner contract gains dev_master-owned governance or schema authority
- a report claims `menmery` writeback without a real reference
- verifier fails to block the forced bad case
- Phase 2 work starts before explicit human `promote`
- `just check` fails

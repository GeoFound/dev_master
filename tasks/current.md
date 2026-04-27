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
last_updated: "2026-04-27"
```

---

## Active Task

```yaml
task_id: "phase-1-low-risk-loop-probe"
task_type: "verify-task"
plane: "execution"
goal: "Run one full low-risk software-change loop through get_context -> act -> isolated/local worker -> runner facts -> verifier -> remember, without claiming Gate B promotion."
scope_in:
  - "one bounded docs/test-only repository change"
  - "menmery get_context and act before mutation"
  - "local or isolated worker execution with runner facts"
  - "verifier decision for the produced facts"
  - "remember writeback with concrete evidence id"
  - "local Phase 1 loop report"
scope_out:
  - "Gate B promotion"
  - "general worker orchestration platform"
  - "product runtime platform"
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
deliverables:
  - "bounded repo diff"
  - "runner facts artifact or digest"
  - "verifier report"
  - "menmery remember/canonical evidence id"
  - "reports/phase1/<loop-report>.md"
acceptance_checks:
  - "just check passes"
  - "just phase1-check passes"
  - "verifier allows or escalates based on produced facts"
  - "remember writeback references the exact evidence"
rollback_if_failed: "Hold at Phase 1 and create a correction-task."
side_effects:
  repo_mutation: true
  shell_execution: true
  external_service_calls: "menmery get_context/act/remember only"
  evidence_write: "local report plus remember writeback"
evidence_outputs:
  - "reports/phase1/<loop-report>.md"
  - "menmery record or inbox id for the loop outcome"
risk_facts:
  action_level: 2
  risk_label: "green"
  docs_only: true
  repo_local_ai_scaffold: true
  dependency_changed: false
  secrets_or_permissions_changed: false
  infra_or_deploy_path_changed: false
menmery_context: "mcp get_context depth=deep and act(intent=software_change) used; supervised lane with explicit human start instruction."
```

---

## Next Allowed Actions

1. Select one bounded docs/test-only change that does not activate deferred capabilities.
2. Run `get_context` and `act(intent="software_change")` before mutation.
3. Execute the change through the local worker/runner/verifier path.
4. Write the outcome through `menmery remember` with exact evidence references.
5. Keep Gate B pending until this full low-risk task completes
   `get_context -> act -> isolated worker -> verifier -> remember`.

---

## Stop Conditions

Stop and create a correction-task if:

- an active doc implies a parallel truth/governance/evidence runtime
- a deferred or future capability becomes an implementation deliverable
- the runner contract gains dev_master-owned governance or schema authority
- a report claims `menmery` writeback without a real reference
- verifier fails to block the forced bad case
- `just check` fails

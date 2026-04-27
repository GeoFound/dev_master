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
last_updated: "2026-04-27"
```

---

## Active Task

```yaml
task_id: "phase-1-first-executable-kernel-slice"
task_type: "build-task"
plane: "execution"
goal: "Implement the first Phase 1 executable-kernel slice: Python local runner facts emitter, verifier scaffold, forced bad verifier case, local smoke command, and fallback evidence report."
scope_in:
  - "Python local runner facts emitter"
  - "Python verifier first pass"
  - "forced bad verifier fixture"
  - "just phase1-check command"
  - "local fallback evidence report"
scope_out:
  - "Gate B promotion"
  - "full isolated worktree orchestration"
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
  - "runner/local_worktree_runner.py"
  - "verifier/verifier.py"
  - "scripts/check_phase1_kernel.sh"
  - "tests/fixtures/good_runner_facts.yaml"
  - "tests/fixtures/bad_runner_facts.yaml"
  - "reports/phase1/phase1-first-slice.md"
acceptance_checks:
  - "just check passes"
  - "just phase1-check passes"
  - "verifier allows good fixture"
  - "verifier blocks forced bad fixture"
rollback_if_failed: "Hold at Phase 1 and create a correction-task."
side_effects:
  repo_mutation: true
  shell_execution: true
  external_service_calls: "menmery get_context/act/remember only"
  evidence_write: "local report plus remember writeback"
evidence_outputs:
  - "reports/phase1/phase1-first-slice.md"
  - "menmery record fct_20260427075405845017_state"
risk_facts:
  action_level: 2
  risk_label: "green"
  docs_only: false
  repo_local_ai_scaffold: true
  dependency_changed: false
  secrets_or_permissions_changed: false
  infra_or_deploy_path_changed: false
menmery_context: "mcp get_context depth=deep and act(intent=software_change) used; supervised lane with explicit human start instruction."
```

---

## Next Allowed Actions

1. Complete this Phase 1 slice.
2. Run `just check` and `just phase1-check`.
3. Write outcome through `menmery remember`.
4. Keep Gate B pending until a full low-risk task completes
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

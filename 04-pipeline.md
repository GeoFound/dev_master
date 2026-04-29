---
status: active
scope: product
authority: this
---

# AI Automation Pipeline

> `dev_master` is the product pipeline. The current `software_change`
> runner/verifier loop is the first executable kernel, not the whole product.

---

## 4.1 Product Flow

```text
Intake
  -> Spec
  -> Critique
  -> Plan
  -> Implementation
  -> Test
  -> Security
  -> Result Gate
  -> PR / Release
  -> Canary / Rollback
  -> Operations Feedback
  -> Advisor / TechRadar Signals
  -> Recovery / Improvement
```

Product responsibilities:

- preserve requirements and constraints
- produce implementation slices with acceptance criteria
- challenge gaps and risk before mutation
- mutate repos only through bounded execution workers
- collect tests, security facts, artifact digests, and evidence refs
- gate release and rollback decisions
- feed operations, external sensing, and advisory signals back into planning

---

## 4.2 Current Executable Slice

The current slice proves one governed software-change loop:

```text
Caller / Orchestrator
  -> Execution Worker
  -> Verifier / Governor
  -> evidence writeback
```

Detailed sequence:

1. Caller establishes context through
   `entry_turn(message="software_change / dev_master / <target repo> / <goal>", max_depth="auto")`.
2. Caller follows the returned `recommended_call` and lane/action-level guidance.
   If `menmery` is unavailable, the run must be marked as degraded fallback.
3. If the lane allows execution, an isolated worker prepares a local change.
4. Worker emits runner facts: diff digest, checks, dependency facts, risk facts.
5. Verifier compares request, diff, checks, risk facts, and evidence refs.
6. Caller writes the result back through
   `remember(..., related_to=[entry_turn_id])` or governed canonical write.
7. Human approval is requested only when `menmery` action level / lane requires it.

This is a kernel proof. It must not be read as deleting Spec, Critic, Test,
Security, Ops, Advisor, TechRadar, adapters, model governance, release safety,
or rewrite governance from the product.

Older `get_context -> act` phrasing should not override
`27-external-systems-boundary.md` or `REWRITE-PLAN.md`.

---

## 4.3 Three-Plane Boundary

| Plane | Owns | Must not do |
|-------|------|-------------|
| Orchestration | context, lane, scheduling, approval wait, evidence refs | shell, repo mutation, final self-approval |
| Execution | worktree/sandbox, diff, lint/test/security, artifact digest | governance override, canonical truth writes |
| Evidence | `menmery` record/inbox/audit refs, runner fact snapshot | mutable logs as final proof |

Temporal may later implement long-running orchestration, but Phase 1 must work without a Temporal production cluster.

---

## 4.4 Risk Facts

Runner facts should include:

```yaml
runner_contract_version: "software-change-runner-v2"
artifact_family: "software-change-runner"
schema_version: "2.0.0"
policy_version: "phase1-gate-v1"
ruleset_version: "phase1-core-v1"
trace_id: "tr_..."
repo_ref: "repo@ref"
requested_change: "bounded change"
diff_digest: "sha256:..."
files_changed:
  - "docs/example.md"
checks:
  lint: "pass|fail|not_run"
  tests: "pass|fail|not_run"
  security: "pass|fail|not_run"
risk_facts:
  docs_only: true
  dependency_changed: false
  secrets_or_permissions_changed: false
  infra_or_deploy_path_changed: false
  action_level: 2
  risk_label: "green"
```

The runner family label and contract triplet belong to `dev_master` in this
local runner fact shape. Canonical evidence, approval lane, and action-level
semantics come from `menmery` when available; LLM routing/runtime model
decisions come from `auto_router` when used.

---

## 4.5 Approval Rules

| Change type | Default action level | Default handling |
|-------------|----------------------|------------------|
| analysis / plan only | 0 | no runner needed |
| read-only scan/test/lint | 1 | auto or supervised depending on lane |
| local diff / draft patch | 2 | supervised until evidence supports relaxation |
| create PR / push branch / external write | 3 | supervised or explicit approval |
| merge / deploy / migration / delete / secrets / permissions | 4 | explicit human approval |

`green/yellow/red` are convenience labels only. The source of governance is `menmery` action level and approval lane.

---

## 4.6 Phase 1 Success

Phase 1 succeeds when one low-risk docs/test-only change can complete this loop:

```text
entry_turn -> bounded plan -> isolated worker -> verifier -> remember evidence
```

It does not require auto-merge, production deploy, active Ops/Advisor scans, or generalized adapters.

---

## 4.7 Historical Phase 1 Implementation Slice

The deleted first executable slice was intentionally narrower than Gate B
completion:

- Python local runner facts emitter: `runner/local_worktree_runner.py`
- Python verifier first pass: `verifier/verifier.py`
- forced bad fixture: `tests/fixtures/bad_runner_facts.yaml`
- local smoke command: `just phase1-check`
- fallback evidence: `reports/phase1/phase1-first-slice.md`

These paths are no longer active after the 2026-04-27 implementation reset.
They remain useful design references for the rewrite plan, but they cannot be
used as current Gate B evidence.

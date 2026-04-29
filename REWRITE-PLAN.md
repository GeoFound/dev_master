---
status: active
scope: window
authority: this
---

# Rewrite Plan

> Current draft for the first post-reset executable slice. This file is the
> planning authority for rewrite discussion. It does not authorize
> implementation until a human approves the plan.

---

## 1. Planning Status

- current state: draft
- target: regenerate Gate B from scratch after the 2026-04-27 reset
- implementation permission: not yet granted
- current repo mode: docs-only

This draft answers the eight rewrite questions from
`26-design-closure-review.md` and adds the two integration contracts most
likely to drift again: `menmery` entry-turn usage and `auto_router`
request/result/feedback linkage.

---

## 2. Proposed Decision Summary

1. The first real executable slice should prove one low-risk `software_change`
   loop in this repository itself, starting with docs-only or repo-local
   validation work.
2. The first runtime shape should remain a three-actor kernel:
   Caller / Orchestrator, Execution Worker, Verifier / Governor.
3. The first regenerated runner contract should use
   `software-change-runner-v2` to distinguish it from deleted pre-reset
   artifacts.
4. `menmery` should be `entry_turn` first for non-doc software-change work.
5. `auto_router` should remain optional for the first slice, but when used it
   must receive stable task metadata and return request identifiers that can be
   correlated with verifier outcomes and feedback.
6. Gate B must be regenerated from scratch; no deleted implementation evidence
   is promotable.

---

## 3. First Executable Slice

### Goal

Prove one governed software-change loop end to end:

```text
entry_turn
-> bounded plan
-> isolated worker
-> verifier
-> remember evidence
```

### Initial Scope

In scope for the first slice:

- docs-only changes in `dev_master`
- repo-local validation scaffolding that supports the runner/verifier proof
- forced-bad verifier fixtures
- local evidence fallback
- `menmery` writeback when available

Explicitly out of scope for the first slice:

- generalized project adapters
- application-code mutation in external target repos
- release, PR, deploy, canary, or rollback automation
- background Ops / Advisor / TechRadar runtime
- model-governance runtime
- rewrite-controller runtime

### Success Conditions

The first slice is successful only if it can regenerate fresh Gate B evidence
for all of the following:

- one bounded low-risk task completes through the full loop
- runner facts include diff digest, checks, and risk facts
- verifier blocks at least one forced-bad case
- evidence is written back to `menmery` when available
- local fallback evidence is complete and traceable when `menmery` is not
  available

---

## 4. Runtime Actor Compression

The first rewrite slice should keep the product role model intact while
compressing runtime execution into three actors.

| Runtime actor | Covered product passes in the first slice |
|---------------|--------------------------------------------|
| Caller / Orchestrator | scope freeze, `entry_turn`, context gathering, spec pass, critic pass, task planning, evidence collection |
| Execution Worker | bounded diff, local checks, test pass, security pass, runner facts emission |
| Verifier / Governor | request-fit checks, evidence-fit checks, risk mapping, writeback readiness, escalate/block/allow recommendation |

Not deleted from product architecture:

- Spec
- Critic
- Code
- Test
- Security
- Ops
- Advisor
- TechRadar
- Project Adapter
- Model Governance
- Rewrite Controller

The first slice compresses their execution shape. It does not remove them from
product scope.

---

## 5. `menmery` Integration Contract

### Required Call Path

For non-doc software-change work, the first slice should standardize on:

```text
1. entry_turn(
     message="software_change / dev_master / <target repo> / <goal>",
     max_depth="auto"
   )
2. follow the returned recommended_call when needed and lane-allowed
3. run the bounded worker step
4. verify runner facts against the bounded request
5. remember(content=<structured closure payload>, related_to=[entry_turn_id])
```

### Required Captured Fields

The caller must retain at minimum:

- `entry_turn_id`
- `recommended_call`
- `action_level`
- `approval_lane`
- `objective_panorama` summary or reference
- `loop_status`

### Writeback Shape

The first slice should write back, at minimum:

- bounded request summary
- diff digest
- check results
- risk facts
- verifier decision
- local artifact references
- optional gateway request/result/feedback references when `auto_router` was
  used

The writeback path is observation / review evidence first. Canonical promotion
is a later concern and must not block the first executable slice.

---

## 6. `auto_router` Integration Contract

`dev_master` must not build a local router, failover chain, or learner
publisher. The first slice may operate without routed calls, but any routed call
must follow one stable contract.

### Outbound Metadata

When a stage uses `auto_router`, the request should include or derive these
fields where the interface supports them:

```yaml
tenant: "dev-master"
trace_id: "tr_..."
run_id: "run_..."
step_id: "step_..."
stage: "spec|critic|code|test|security|verifier"
task_class: "structured_analysis|code_gen|test_generation|security_review|policy_review"
risk_label: "green|yellow|red"
quality_expectation: "reasoned|strict|high_recall|high_precision"
cost_mode: "default|conservative"
```

### Returned Data To Preserve

The caller or worker must preserve:

- `request_id`
- final execution model identifier when available
- any returned routing or policy reference that is stable enough to audit
- timestamps and latency if available

### Feedback Linkage

After verifier completion, feedback should be correlated through `request_id`
when the routed stage produced one. The first slice should support at least:

```yaml
request_id: "req_..."
trace_id: "tr_..."
stage: "spec|critic|code|test|security|verifier"
verdict: "pass|fail|block|escalate"
feedback_source: "verifier|qa|human"
notes: "short structured outcome"
```

### Local Degradation Rule

If `auto_router` is unavailable:

- do not build a replacement router inside `dev_master`
- either use an already-approved direct model path with local evidence, or
  delay the routed step and mark the run as degraded

---

## 7. Runner Facts Contract vNext

The first regenerated contract should use a new version marker:

```yaml
runner_contract_version: "software-change-runner-v2"
artifact_family: "software-change-runner"
schema_version: "2.0.0"
policy_version: "phase1-gate-v1"
ruleset_version: "phase1-core-v1"
trace_id: "tr_..."
run_id: "run_..."
step_id: "step_..."
repo: "dev_master"
ref: "working-tree"
requested_change: "bounded change statement"
scope_in:
  - "allowed file or directory"
scope_out:
  - "forbidden area"
entry_turn_id: "turn_..."
gateway_request_id: "req_..."  # optional
diff_digest: "sha256:..."
files_changed:
  - "path/to/file.md"
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
artifact_digests:
  - "sha256:..."
evidence_refs:
  menmery_audit_id: null
  local_evidence_id: "ev_..."
worker:
  implementation: "local-worktree-runner"
  identity: "worker-local"
timestamps:
  started_at: "2026-04-29T00:00:00Z"
  completed_at: "2026-04-29T00:05:00Z"
```

Rules:

- one family label field only
- the contract triplet is mandatory on runner facts
- no mixed `schema_version` majors for the same runner family in one run
- no worker self-approval field
- no final approval field owned by the worker
- gateway fields are optional, but if present they must be auditable

---

## 8. Verifier Blocking Rules

The verifier must block or escalate when any of the following is true:

- the diff exceeds the bounded request
- changed files exceed declared scope
- the diff digest is missing or cannot be tied to the reviewed files
- checks are absent or not tied to the exact diff
- `risk_label` conflicts with changed-file facts or `action_level`
- `schema_version`, `policy_version`, or `ruleset_version` is missing from a
  gating artifact
- the run mixes incompatible schema majors without an explicit adapter boundary
- external side effects occurred without the required lane and approval context
- the worker claims success without evidence refs
- `menmery` writeback is required but missing and no explicit fallback path was
  recorded
- the run attempts to use worker narrative as final approval

The verifier output should stay minimal:

```yaml
decision: "allow|block|escalate"
reasons:
  - "..."
required_writeback: true
schema_version: "1.0.0"
policy_version: "phase1-gate-v1"
ruleset_version: "verifier-core-v1"
runner_contract_version: "software-change-runner-v2"
```

---

## 9. Evidence Writeback And Local Fallback

### Preferred Path When `menmery` Is Available

- use `entry_turn` first
- keep `entry_turn_id` stable through the run
- write the structured closure payload back with `remember(..., related_to=[entry_turn_id])`
- store `menmery` audit / record identifiers inside local runner evidence refs

### Allowed Local Fallback When `menmery` Is Unavailable

The first slice may use a local fallback only if all of the following exist:

- append-only local evidence index
- human-readable gate report
- artifact digest references
- explicit marker that writeback is pending

Proposed local fallback paths:

```text
evidence/index.jsonl
evidence/artifacts/
reports/gate-b/
```

The fallback path is a temporary execution aid. It must not become a parallel
canonical truth or approval system.

---

## 10. Gate B Evidence To Regenerate From Scratch

The rewrite must regenerate all active Gate B evidence. Nothing from deleted
implementation assets is reusable as current proof.

Required regenerated evidence:

- one successful low-risk full-loop run
- one forced-bad verifier block
- one fresh runner facts sample tied to the new contract version
- one fresh writeback example in `menmery`, or one complete local fallback run
- one gate review summary that explicitly states which deleted evidence was
  replaced

---

## 11. Explicitly Deferred Capabilities

The first rewrite slice must not activate:

- Ops AI runtime
- Advisor AI runtime
- TechRadar runtime
- generalized project-adapter runtime
- model-governance runtime
- rewrite-controller runtime
- PR / merge / deploy automation
- canary / rollback automation
- Temporal production cluster
- parallel canonical store
- parallel approval controller
- parallel router, failover, or learner publisher

These remain product-scope capabilities and should be activated only through
later evidence and human decisions.

---

## 12. Open Questions Requiring Human Decision

The current draft proposes answers, but these points still need explicit human
confirmation before code recreation:

1. Should the first Gate B sample be limited to docs-only mutation in this
   repository, or may it include repo-local validation helpers?
2. Is `software-change-runner-v2` the preferred reset marker, or should the
   contract intentionally restart at `v1` with new evidence only?
3. Must the first slice require a live `auto_router` call, or is routed
   execution optional until a later reliability window?
4. Are the proposed local fallback paths acceptable, or should they be renamed
   before implementation?
5. Does the historical Python baseline remain accepted for the first rewrite
   slice, or should the plan revise it before implementation begins?

Until these are approved, this file remains a planning artifact only.

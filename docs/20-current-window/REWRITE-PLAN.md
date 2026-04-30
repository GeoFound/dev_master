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
- current repo mode: blueprint-first rebuild

This draft answers the eight rewrite questions from
`docs/00-entry/26-design-closure-review.md` and adds the two optional service-consumption
contracts most likely to drift again: `menmery` usage and `auto_router`
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
4. `menmery` should remain an optional sibling service for non-doc
   software-change work; use `entry_turn` when the task benefits from long-term
   context or governance preview.
5. `auto_router` should remain optional for the first slice, but when used it
   must receive stable task metadata and return request identifiers that can be
   correlated with verifier outcomes and feedback.
6. Gate B must be regenerated from scratch; no deleted implementation evidence
   is promotable.
7. Phase 1 should be split into `1A` runner/verifier/evidence skeleton and
   `1B` local L1 prototype proof. Phase 1B must use the same governed loop but
   must not introduce external repo mutation, deploy, PR, merge, or paid
   product-service side effects. Budgeted API worker calls are allowed only
   when recorded in cost facts and kept under the current-window ceiling.
8. Autonomy growth should follow `autonomy-ratchet.md`: local green parameters
   may widen from append-only evidence, while hard red lines remain human-owned.
9. `dev_master` owns scheduling, authorization, governance, evidence, cost, and
   review state. Codex, Claude Code, API models, and other agents are worker
   providers. They may propose slices, but dispatch requires a `dev_master`
   decision under `task-proposal-contract.md`.

---

## 3. First Executable Slices

### Phase 1A Goal

Prove one governed software-change loop end to end:

```text
bounded plan
-> isolated worker
-> verifier
-> local evidence
-> optional service writeback
```

### Initial Scope

In scope for Phase 1A:

- docs-only changes in `dev_master`
- repo-local validation scaffolding that supports the runner/verifier proof
- forced-bad verifier fixtures
- local evidence fallback
- optional `menmery` writeback when available

### Phase 1B Goal

Prove one local L1 prototype artifact through the same governed loop.

The prototype must:

- be controlled through the CLI-only Phase 1B surface
- be runnable locally by a human using a documented command such as
  `streamlit run app.py` or `npm run dev`
- produce visible local output on localhost or an equivalent local UI surface
- be authorized through the task proposal / `dev_master` decision handoff
- exercise at least one API-backed or API-compatible worker provider path;
  subscription-tied CLI/SDK providers cannot be the only worker path
- emit runner facts, verifier decision, cost facts, and evidence refs
- avoid external repo mutation, deploy, PR, merge, paid product-service side
  effect, or production side effect

Markdown, JSON, screenshots, and static mock reports do not satisfy Phase 1B.

Explicitly out of scope for the first slice:

- generalized project adapters
- application-code mutation in external target repos
- release, PR, deploy, canary, or rollback automation
- external hosted preview deployment
- external paid product-service usage
- unattended production SaaS/product decisions
- background Ops / Advisor / TechRadar runtime
- model-governance runtime
- rewrite-controller runtime

### Success Conditions

The first slice is successful only if it can regenerate fresh Gate B evidence
for all of the following:

- one bounded low-risk task completes through the full loop
- one local runnable L1 prototype artifact completes through the full loop
- Phase 1B uses the CLI-only product surface and at least one API-backed or
  API-compatible worker provider path
- runner facts include diff digest, checks, and risk facts
- runner facts include `ratchet_metrics_contribution`, or explicitly record
  `null` metric contribution with a reason
- verifier blocks at least one forced-bad case
- evidence is durably preserved locally
- cost ceilings are recorded and not exceeded
- optional service writeback is complete and traceable when that path is used
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
| Verifier / Governor | request-fit checks, evidence-fit checks, risk mapping, evidence persistence readiness, escalate/block/allow recommendation |

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

### Recommended Service Path

When a non-doc software-change task chooses to use `menmery`, the first slice
should standardize on:

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

### Required Captured Fields When Used

The caller must retain at minimum:

- `entry_turn_id`
- `recommended_call`
- `action_level`
- `approval_lane`
- `objective_panorama` summary or reference
- `loop_status`

### Writeback Shape

If `menmery` is used, the first slice should write back, at minimum:

- bounded request summary
- diff digest
- check results
- risk facts
- verifier decision
- local artifact references
- optional gateway request/result/feedback references when `auto_router` was
  used

The default evidence path is local append-only evidence first. Optional
`menmery` writeback should use observation / review evidence first. Canonical
promotion is a later concern and must not block the first executable slice.

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
- an optional service writeback was required by the chosen path but is missing,
  and no explicit fallback path was
  recorded
- the run attempts to use worker narrative as final approval

The verifier output should stay minimal:

```yaml
decision: "allow|block|escalate"
reasons:
  - "..."
required_evidence_persistence: true
schema_version: "1.0.0"
policy_version: "phase1-gate-v1"
ruleset_version: "verifier-core-v1"
runner_contract_version: "software-change-runner-v2"
```

---

## 9. Evidence Writeback And Local Fallback

### Preferred Path When `menmery` Is Available

- use `entry_turn` only for runs that intentionally consume `menmery`
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

## 12. Closed Decisions For Implementation

These points are closed for the current implementation window:

1. Phase 1A may include repo-local validation helpers.
2. `software-change-runner-v2` is the reset marker for regenerated runner facts.
3. Live `auto_router` calls are optional until a later reliability window.
4. Local fallback paths are acceptable when recorded as fallback evidence.
5. Python is the active Phase 1-4 core implementation language; TypeScript is
   reserved for later Web/IDE surfaces.
6. API-backed providers are the default worker path. Subscription-tied CLI/SDK
   providers are optional Phase 2+ paths and require raw-output capture,
   version pinning, drift detection, and current terms/docs review before
   automated use.

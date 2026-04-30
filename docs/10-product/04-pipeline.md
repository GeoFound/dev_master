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

> The following is the long-horizon product flow target. Most stages are not yet
> implemented; the current executable scope is limited to §4.2.

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

Product responsibilities (target):

- should preserve requirements and constraints
- should produce implementation slices with acceptance criteria
- should challenge gaps and risk before mutation
- should mutate repos only through bounded execution workers
- should collect tests, security facts, artifact digests, and evidence refs
- should gate release and rollback decisions
- should feed operations, external sensing, and advisory signals back into planning

Product flow is not the same as full unattended product autonomy. The current
automation target is `L1` and `L1.5`: clickable prototypes, bounded artifacts,
queued execution, verifier/evidence discipline, async human review, and
multi-project operation. `L2` production SaaS/product work remains
semi-automatic: AI may prepare diffs, PRs, verification reports, and risk
recommendations, but humans retain account, payment, multi-tenant, security,
release, business, and autonomy-expansion decisions.

`dev_master` is the control plane. Codex, Claude Code, API models, and other
agents are worker providers. They may propose slices; `dev_master` authorizes
dispatch through [task-proposal-contract.md](task-proposal-contract.md).

---

## 4.2 Current Executable Slice

The current slice proves one governed software-change loop:

```text
Caller / Orchestrator
  -> Execution Worker
  -> Verifier / Governor
  -> local evidence
  -> optional service writeback / feedback
```

Detailed sequence:

1. Caller establishes a bounded request and decides whether optional services
   are needed.
2. Planner/human/integration proposal is validated through the task proposal
   contract before any worker dispatch.
3. If the task benefits from long-term context or governance preview and
   `menmery` is available, call its documented facade. If not, keep the run
   local and mark the fallback explicitly.
4. If risk and approval conditions allow execution, an isolated worker prepares
   a local change.
5. Worker emits runner facts: diff digest, checks, dependency facts, risk facts.
6. Verifier compares request, diff, checks, risk facts, and evidence refs.
7. Caller writes the result into local append-only evidence.
8. If sibling services were used, caller may additionally write structured
   results back to them through their public service surfaces.
9. Human approval is requested when local gate policy or an optional external
   governance preview says it is required.

This is a kernel proof. It must not be read as deleting Spec, Critic, Test,
Security, Ops, Advisor, TechRadar, adapters, model governance, release safety,
or rewrite governance from the product.

Older `get_context -> act` phrasing should not override
`docs/30-integrations/27-external-systems-boundary.md` or `docs/20-current-window/REWRITE-PLAN.md`.

---

## 4.3 Three-Plane Boundary

| Plane | Owns | Must not do |
|-------|------|-------------|
| Orchestration | bounded request, optional service context, scheduling, approval wait, evidence refs | shell, repo mutation, final self-approval |
| Execution | worktree/sandbox, diff, lint/test/security, artifact digest | governance override, canonical truth writes |
| Evidence | local immutable evidence refs, optional service refs, runner fact snapshot | mutable logs as final proof |

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
  risk_label: "green"
service_governance:
  source: "local|menmery"
  action_level: null
```

The runner family label and contract triplet belong to `dev_master` in this
local runner fact shape. Optional service governance or routing facts may be
attached when those services are used.

---

## 4.5 Approval Rules

| Change type | Default action level | Default handling |
|-------------|----------------------|------------------|
| analysis / plan only | 0 | no runner needed |
| read-only scan/test/lint | 1 | auto or supervised depending on lane |
| local diff / draft patch | 2 | supervised until evidence supports relaxation |
| create PR / push branch / external write | 3 | supervised or explicit approval |
| merge / deploy / migration / delete / secrets / permissions | 4 | explicit human approval |

`green/yellow/red` are local pipeline labels. When an optional external service
returns stricter governance guidance, the stricter outcome wins.

---

## 4.6 Phase 1 Success

Phase 1 succeeds when one low-risk docs/test-only change can complete this loop:

```text
bounded request -> isolated worker -> verifier -> local evidence
```

It does not require auto-merge, production deploy, active Ops/Advisor scans, or generalized adapters.

---

## 4.7 Historical Phase 1 Implementation Slice (deleted)

The deleted first executable slice was intentionally narrower than Gate B
completion. The following paths existed before the 2026-04-27 reset and have
since been removed from the repository:

- (deleted) Python local runner facts emitter, formerly at `runner/local_worktree_runner.py`
- (deleted) Python verifier first pass, formerly at `verifier/verifier.py`
- (deleted) forced bad fixture, formerly at `tests/fixtures/bad_runner_facts.yaml`
- (deleted) local smoke command, formerly `just phase1-check`
- (deleted) fallback evidence report, formerly at `reports/phase1/phase1-first-slice.md`

These paths no longer exist. They are listed here only as historical context
for what the prior slice covered. They must not be referenced as design source,
revived as code, or treated as current Gate B evidence. The rewrite must
regenerate any equivalent artifacts from scratch under
`docs/20-current-window/REWRITE-PLAN.md`.

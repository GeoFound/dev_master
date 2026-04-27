# software_change Pipeline

> Phase 1 pipeline is intentionally small. It proves that a software change can pass through `menmery` governance, isolated execution, verifier review, and evidence writeback without creating a new platform.

---

## 4.1 Minimal Flow

```text
Input
  -> Caller / Orchestrator
  -> Execution Worker
  -> Verifier / Governor
  -> menmery evidence writeback
```

Detailed sequence:

1. Caller obtains context:
   `get_context("software_change / <repo> / <goal>")`
2. Caller asks governance preview:
   `act(intent="software_change", details="<bounded request>")`
3. If the lane allows execution, an isolated worker prepares a local change.
4. Worker emits runner facts: diff digest, checks, dependency facts, risk facts.
5. Verifier compares request, diff, checks, risk facts, and evidence refs.
6. Caller writes the result back through `remember(...)` or governed canonical write.
7. Human approval is requested only when `menmery` action level / lane requires it.

---

## 4.2 Three-Plane Boundary

| Plane | Owns | Must not do |
|-------|------|-------------|
| Orchestration | context, lane, scheduling, approval wait, evidence refs | shell, repo mutation, final self-approval |
| Execution | worktree/sandbox, diff, lint/test/security, artifact digest | governance override, canonical truth writes |
| Evidence | `menmery` record/inbox/audit refs, runner fact snapshot | mutable logs as final proof |

Temporal may later implement long-running orchestration, but Phase 1 must work without a Temporal production cluster.

---

## 4.3 Risk Facts

Runner facts should include:

```yaml
runner_contract_version: "software-change-runner-v1"
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

Only `runner_contract_version` belongs to dev_master. Schema and governance versions belong to `menmery` or the underlying tool.

---

## 4.4 Approval Rules

| Change type | Default action level | Default handling |
|-------------|----------------------|------------------|
| analysis / plan only | 0 | no runner needed |
| read-only scan/test/lint | 1 | auto or supervised depending on lane |
| local diff / draft patch | 2 | supervised until evidence supports relaxation |
| create PR / push branch / external write | 3 | supervised or explicit approval |
| merge / deploy / migration / delete / secrets / permissions | 4 | explicit human approval |

`green/yellow/red` are convenience labels only. The source of governance is `menmery` action level and approval lane.

---

## 4.5 Phase 1 Success

Phase 1 succeeds when one low-risk docs/test-only change can complete this loop:

```text
get_context -> act -> isolated worker -> verifier -> remember evidence
```

It does not require auto-merge, production deploy, active Ops/Advisor scans, or generalized adapters.

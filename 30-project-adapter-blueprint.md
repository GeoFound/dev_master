---
status: future
scope: product
authority: this
---

# Project Adapter Blueprint

> Future authority for project-type adapters. This file describes how a general
> governance kernel can map into different project stacks without becoming
> Web-only.

---

## 30.1 Core Position

The governance kernel should not hard-code Web/SaaS assumptions.

Future `dev_master` should separate:

- governance kernel: requirement, spec, critic, test, security, audit,
  proposal, health, trust evolution
- project adapters: stack-specific contract, build, test, release, and runtime
  mapping

Adding a new project type should usually mean adding or refining an adapter,
not rewriting the governance kernel.

---

## 30.2 Required Adapter Responsibilities

Every adapter must define at least:

1. contract formats
2. build commands
3. test matrix
4. release strategy
5. runtime metrics

Minimum spec shape:

```yaml
adapter:
  id: "{adapter_id}"
  display_name: "{human_readable_name}"
  project_types:
    - "{project_type}"
  version: "1.0.0"
  status: "draft"
  contract_formats:
    - "{contract_type}"
  build_commands:
    - "{build_command}"
  test_matrix:
    - "{test_type}"
  release_strategy:
    - "{release_mode}"
  runtime_metrics:
    - "{metric_name}"
  gate_policies:
    result_gate: "{policy_id}"
    canary_or_rollout_gate: "{policy_id}"
    security_gate: "{policy_id}"
  audit_outputs:
    - "audit/{adapter_id}-runs.jsonl"
```

---

## 30.3 Standardized Interface

Adapters should present a consistent interface to the governance kernel.

Minimum conceptual interface:

```text
detectProject
loadContracts
build
runTests
runSecurityChecks
prepareRelease
collectRuntimeMetrics
validateCompatibility
```

Standardized outputs should cover at least:

- `BuildResult`
- `TestResult`
- `SecurityResult`
- `ReleasePlan`
- `RuntimeMetrics`

The kernel should consume normalized results, not raw tool-specific output.

---

## 30.4 Compatibility Rules

Adapter composition rules:

- one project may use 1 primary adapter plus N supporting adapters
- the primary adapter defines default build/test/release/runtime behavior
- supporting adapters may add signals but may not override blocking gates
- when adapter outputs conflict, the stricter gate wins
- different repo subpaths may bind to different adapters

This prevents adapter sprawl from weakening governance.

---

## 30.5 Example Adapter Families

Representative families:

- Web / SaaS
- Mobile
- Backend service
- CLI
- Desktop
- Game
- Embedded

These examples are illustrative; the authority is the normalized adapter
contract, not a closed enum.

---

## 30.6 Acceptance Requirements

Before an adapter is activated, it should prove:

- `detectProject()` correctly identifies the target stack
- normalized build/test/security/release outputs are produced
- the adapter can feed Result Gate inputs
- at least one rollout strategy and one rollback strategy exist
- the adapter can write governed audit output

Minimum smoke checklist:

- local build succeeds
- test matrix runs
- security results are produced
- release plan can be generated
- runtime metrics can be collected
- audit log can be emitted

---

## 30.7 Adapter Audit Format

Adapter runs should emit structured audit events and follow `CONTRACTS.md`.

Example:

```jsonl
{
  "timestamp": "2026-05-03T10:00:00Z",
  "artifact_family": "adapter_run",
  "schema_version": "1.0.0",
  "trace_id": "tr_adapter_20260503x1",
  "adapter_id": "mobile_adapter",
  "version": "1.0.0",
  "project_path": "apps/mobile",
  "event_type": "adapter_run",
  "build_status": "passed",
  "test_status": "passed",
  "security_status": "passed",
  "release_strategy": "testflight",
  "runtime_metric_keys": ["crash_free_sessions", "app_start_p95_ms"],
  "policy_version": "v3.1",
  "ruleset_version": "adapter-v1"
}
```

---

## 30.8 Non-Goals

This blueprint does not authorize:

- current runtime adapter platform
- adapter logic that overrides Result Gate
- local reinvention of external governance ownership
- hidden stack-specific exceptions outside the normalized contract surface

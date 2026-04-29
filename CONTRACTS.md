---
status: active
scope: product
authority: this
---

# Contracts And Version Governance

> This file is the authority for machine-readable contract discipline in
> `dev_master`. It governs structured artifacts and cross-stage compatibility.
> It does not authorize implementation by itself.

---

## 1. Purpose

`dev_master` treats contracts as agent interfaces, not as optional prose.

Any structured artifact that can influence:

- repo mutation
- verifier decisions
- governance or approval mapping
- `menmery` evidence writeback
- `auto_router` feedback correlation

must carry explicit version metadata and remain auditable across stages.

---

## 2. Contract Triplet

Every machine-readable stage artifact that matters for execution, gating, or
audit must carry this triplet:

| Field | Meaning | Minimum rule |
|-------|---------|--------------|
| `schema_version` | Version of the artifact shape and field semantics | Use semver; do not mix incompatible majors in one run |
| `policy_version` | Version of the boundary, gate, approval, or threshold policy used to judge the artifact | Any decision-changing update must be recorded before use |
| `ruleset_version` | Version of the executable rules or evaluator bundle that produced findings or pass/fail results | Findings and decisions must record the exact evaluated ruleset |

`schema_version` is about shape and meaning. `policy_version` is about how the
product decides. `ruleset_version` is about which executable rules actually
ran.

---

## 3. Mandatory Artifact Envelope

The exact payload differs by artifact family, but the envelope should follow
this shape whenever practical:

```yaml
artifact_family: "software-change-runner"
schema_version: "2.0.0"
policy_version: "phase1-gate-v1"
ruleset_version: "phase1-core-v1"
trace_id: "tr_..."
run_id: "run_..."
step_id: "step_..."
stage: "code|test|security|verifier"
producer: "worker-local|verifier-local|adapter-id"
created_at: "2026-04-29T00:00:00Z"
artifact_digest: "sha256:..."  # when the artifact represents concrete content
payload:
  {}
```

If a contract-bearing artifact is passed between agents or stages, record an
`artifact_digest` or equivalent semantic hash whenever the exact reviewed
content matters.

---

## 4. `schema_version` Rules

`schema_version` uses semver with these defaults:

| Change type | Version bump |
|-------------|--------------|
| add optional field | minor |
| add backward-compatible enum/value or metadata | minor |
| documentation/example fix with no payload meaning change | patch |
| producer bug fix with no accepted-payload meaning change | patch |
| add required field | major |
| remove field | major |
| rename field | major |
| change type, units, meaning, or validation semantics in a consumer-visible way | major |

Verifier discipline:

- the same run must not mix different `schema_version` majors for the same
  artifact family
- if a stage transforms one artifact family into another, it must emit a new
  family/schema and keep source references
- if compatibility requires an adapter or normalizer, that adapter must be
  explicit and auditable

---

## 5. `policy_version` Rules

`policy_version` identifies the decision policy in effect for an artifact.

It covers things such as:

- risk label to action-level mapping
- gate pass/fail criteria
- approval-lane thresholds
- rollout or rollback thresholds
- SLO/SLI or quality threshold definitions

Rules:

- if a change can alter `allow|block|escalate` behavior, `policy_version` must
  change
- policy changes must be introduced through an authority doc update, ADR, or
  equivalent governed record before execution relies on them
- a verifier decision without a clear `policy_version` is incomplete

---

## 6. `ruleset_version` Rules

`ruleset_version` identifies the executable rule bundle that produced findings
or classifications.

Typical examples:

- security scanning bundle
- PII or secrets detection bundle
- verifier rules
- rollout or canary checks
- adapter validation bundle
- model-governance evaluation bundle

Rules:

- every finding that can block or downgrade a run must be attributable to a
  concrete `ruleset_version`
- if multiple rule bundles contribute to one decision, either emit a composed
  bundle version or include a structured breakdown in the payload
- changing the rules without changing the recorded `ruleset_version` is a
  verifier failure

---

## 7. Stage Consistency Rules

Structured artifacts must remain coherent across a run.

Minimum consistency requirements:

- `trace_id` must stay stable across all artifacts in the same run
- `run_id` must stay stable unless a new governed run begins
- downstream artifacts must reference the exact upstream artifact or digest they
  evaluated
- verifier outputs must record the `policy_version` and `ruleset_version` they
  actually applied
- `auto_router` feedback artifacts must preserve `request_id` plus the run
  identifiers needed to join them back to verifier outcomes

Block by default when:

- the triplet is missing from a gating artifact
- two majors of the same artifact family appear in one run without an explicit
  adapter boundary
- findings are present but the producing `ruleset_version` is absent
- a decision claims policy evaluation but no `policy_version` is recorded

---

## 8. Current Contract Families

| Family | Current status | Primary authority |
|--------|----------------|-------------------|
| `software_change_request` | active concept | `17-task-templates.md`, `18-master-execution-task.md` |
| `software-change-runner-v2` | rewrite target | `REWRITE-PLAN.md` |
| `verifier_decision` | active concept | `05-quality.md` |
| `evidence_writeback` | active concept | `23-menmery-integration.md`, `27-external-systems-boundary.md` |
| `adapter_run` | deferred/future | `12-disaster-recovery.md` |
| `gateway_request_result_feedback` | future integration audit concept | `12-disaster-recovery.md`, `REWRITE-PLAN.md` |
| `model_rollout` | external reference only | external control plane audit, not `dev_master` authority |

The family label may be textual, but the compatibility contract is enforced
through the version triplet and artifact references.

---

## 9. Rewrite Minimum Enforcement

The first post-reset executable slice should enforce at least this baseline:

- runner facts carry `artifact_family`, `schema_version`, `policy_version`,
  `ruleset_version`
- verifier decisions carry the same triplet
- any blocking finding records its producing `ruleset_version`
- any gate report or evidence writeback can be joined by `trace_id`
- missing triplet metadata is verifier-blocking unless the task is explicitly
  docs-only and no machine-readable gate artifact was produced

This baseline is enough to restart implementation without pretending the full
historical contract surface already exists.

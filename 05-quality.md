---
status: active
scope: product
authority: this
---

# Quality Gates

> Quality in Phase 1 means evidence is sufficient to decide, not that every historical role has run.

---

## 5.1 Result Gate

A Result Gate is a six-assertion check. It passes only if all six assertions
hold:

| ID | Assertion | Minimum evidence |
|----|-----------|------------------|
| RG-01 | the requested change is bounded | bounded request, `scope_in`, `scope_out` |
| RG-02 | the reviewed artifact is exact | diff or artifact digest tied to exact files |
| RG-03 | checks are explicit | `pass|fail|not_run` for relevant checks |
| RG-04 | security/dependency/permission facts are explicit | risk facts tied to the exact diff |
| RG-05 | risk label maps to governed action | `risk_label` plus `menmery` action level or fallback record |
| RG-06 | evidence has been or will be written back | `menmery` ref or explicit local fallback/writeback-pending record |

Any structured artifact used to satisfy these assertions must follow
`CONTRACTS.md`.

Result Gate is not approval. Approval comes from `menmery` governance/action level plus human gate when required.

---

## 5.2 Verifier / Governor

Verifier checks:

| Check | Question |
|-------|----------|
| Request fit | Does the diff implement only the bounded request? |
| Evidence fit | Are tests/security/risk facts tied to the exact diff? |
| Risk fit | Does the risk label match changed files and action level? |
| Version fit | Do machine-readable artifacts carry compatible `schema_version`, `policy_version`, and `ruleset_version` values? |
| Boundary fit | Did execution happen outside orchestration? |
| Writeback fit | Is there a `menmery` evidence ref or pending writeback? |

Verifier output:

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

## 5.3 Spec / Critic Confidence Thresholds

When an explicit Spec/Critic pass is active, confidence thresholds should follow
this durable policy unless a future authority doc replaces it:

- `>= 95`: pass directly
- `85-94`: pass, but record issues and keep them visible
- `70-84`: revise and rerun Critic before Code/Test execution
- `< 70`: escalate to human decision

Phase 1 may compress Spec/Critic into the Caller/Orchestrator path, but any
future separate Critic runtime should preserve thresholded evidence rather than
free-form opinion.

---

## 5.4 Initial Green Definition

Green candidates are limited to:

- docs-only changes
- test-only changes
- local-only lint/format/test fixes with no production path impact
- repo-local AI scaffolding/check scripts in this documentation repo, as long as
  they add no product runtime, external writes, dependencies, secrets,
  permissions, infra, deploy, or migration behavior

Not green:

- dependencies
- infra / deployment paths
- secrets / permissions
- migrations
- external writes
- merge / deploy

---

## 5.5 Metrics

Only these Phase 1 metrics matter:

- tasks completed through full `menmery` loop
- verifier blocks
- risk misclassifications
- evidence writeback failures
- runner boundary violations

Do not add dashboard or active sensing metrics before Phase 1 is proven.

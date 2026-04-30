---
status: active
scope: product
authority: this
---

# Quality Gates

> **文件性質：實現藍圖（target spec）。** 本文件定義 verifier、Result Gate、Spec/Critic 閾值與 Phase 1 指標的目標契約。當前倉庫尚未重建 verifier、Result Gate 與 metrics runtime；以下 YAML、表格、判據都是實現時的目標形態。

> Quality in Phase 1 means evidence should be sufficient to decide, not that every historical role has run.

---

## 5.1 Result Gate

When implemented, a Result Gate should be a six-assertion check. It should
pass only if all six assertions hold:

| ID | Assertion | Minimum evidence |
|----|-----------|------------------|
| RG-01 | the requested change is bounded | bounded request, `scope_in`, `scope_out` |
| RG-02 | the reviewed artifact is exact | diff or artifact digest tied to exact files |
| RG-03 | checks are explicit | `pass|fail|not_run` for relevant checks |
| RG-04 | security/dependency/permission facts are explicit | risk facts tied to the exact diff |
| RG-05 | risk label maps to governed action | `risk_label` plus local gate mapping; optional external governance ref when used |
| RG-06 | evidence is durably recorded | local append-only evidence record; optional service writeback ref when used |

Any structured artifact used to satisfy these assertions must follow
`docs/10-product/CONTRACTS.md`.

Result Gate is not approval. Approval comes from local gate policy plus human review when required. Optional external governance may add a stricter constraint, but it is not the only valid source of approval semantics.

---

## 5.2 Verifier / Governor

When implemented, the verifier should perform the following checks:

| Check | Question |
|-------|----------|
| Request fit | Does the diff implement only the bounded request? |
| Evidence fit | Are tests/security/risk facts tied to the exact diff? |
| Risk fit | Does the risk label match changed files and any declared governance level? |
| Version fit | Do machine-readable artifacts carry compatible `schema_version`, `policy_version`, and `ruleset_version` values? |
| Boundary fit | Did execution happen outside orchestration? |
| Writeback fit | Is there durable local evidence, and are any optional external writebacks complete or explicitly pending? |

Verifier output:

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

When Phase 1 runs, only these metrics should matter:

- tasks completed through the full bounded loop
- verifier blocks
- risk misclassifications
- local evidence integrity failures
- optional service writeback failures
- runner boundary violations

Dashboard and active sensing metrics must not be added before Phase 1 is
proven.

---

## 5.6 Semantic Verifier Baseline

Gate C requires a semantic verifier benchmark, not only structural validation.
The first benchmark may be small, but it must use labeled fixtures:

```yaml
minimum_fixture_count: 20
fixture_types:
  - forced_ok
  - forced_bad
  - risk_boundary
critical_false_allow_count: 0
total_risk_misclassification_rate: "< 5%"
```

The fixture set should include request-fit, scope creep, missing evidence,
risk-label mismatch, cost-ceiling, and human-review timeout cases.

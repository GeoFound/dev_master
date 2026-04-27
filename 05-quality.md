# Quality Gates

> Quality in Phase 1 means evidence is sufficient to decide, not that every historical role has run.

---

## 5.1 Result Gate

A Result Gate passes only if:

- the requested change is bounded
- diff is present and digestable
- checks are reported as `pass|fail|not_run`
- security/dependency/permission facts are explicit
- risk label maps to a `menmery` action level
- evidence has been or will be written back to `menmery`

Result Gate is not approval. Approval comes from `menmery` governance/action level plus human gate when required.

---

## 5.2 Verifier / Governor

Verifier checks:

| Check | Question |
|-------|----------|
| Request fit | Does the diff implement only the bounded request? |
| Evidence fit | Are tests/security/risk facts tied to the exact diff? |
| Risk fit | Does the risk label match changed files and action level? |
| Boundary fit | Did execution happen outside orchestration? |
| Writeback fit | Is there a `menmery` evidence ref or pending writeback? |

Verifier output:

```yaml
decision: "allow|block|escalate"
reasons:
  - "..."
required_writeback: true
runner_contract_version: "software-change-runner-v1"
```

---

## 5.3 Initial Green Definition

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

## 5.4 Metrics

Only these Phase 1 metrics matter:

- tasks completed through full `menmery` loop
- verifier blocks
- risk misclassifications
- evidence writeback failures
- runner boundary violations

Do not add dashboard or active sensing metrics before Phase 1 is proven.

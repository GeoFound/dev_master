---
status: active
scope: repo
authority: ref-only
---

# Appendix

> This appendix only keeps active rules and blueprint pointers. Historical
> blueprint detail is preserved in root markdown files. The recovered v3 source
> is stale historical context only.

---

## Active Rules

| Rule | Content |
|------|---------|
| R-00 | Non-doc software-change work must start with `menmery entry_turn(...)` and follow the returned call path. |
| R-01 | `dev_master` must not create a parallel canonical store. |
| R-02 | `dev_master` must not create a parallel approval controller. |
| R-03 | Execution Worker must not decide final approval. |
| R-04 | Runner facts must be written back to `menmery` evidence path. |
| R-05 | Phase 1 only supports local diff/draft execution, not merge/deploy. |
| R-06 | Only `runner_contract_version` is owned by dev_master in Phase 1. |
| R-07 | Deferred/future capabilities require activation proposal. |

---

## Archive Pointers

| Topic | Location |
|-------|----------|
| Ops / TechRadar blueprint | [10-ops-ai.md](10-ops-ai.md) |
| Advisor blueprint | [11-advisor-ai.md](11-advisor-ai.md) |
| Rewrite / model governance blueprint | [12-disaster-recovery.md](12-disaster-recovery.md) |
| Stale recovered design reference | [recovered/AI-autonomous-dev-pipeline-v3.md](recovered/AI-autonomous-dev-pipeline-v3.md) |

These files are product-scope references. They are not active runtime
implementation approval by themselves.

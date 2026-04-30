---
status: active
scope: repo
authority: ref-only
---

# Appendix

> This appendix only keeps active rules and blueprint pointers. The recovered
> v3 source has been removed from active docs; mined durable ideas are tracked
> as a short mapped index.

---

## Active Rules

| Rule | Content |
|------|---------|
| R-00 | Non-doc software-change work must first decide whether sibling services are needed; if `menmery` is used, follow its returned call path. |
| R-01 | `dev_master` must not create a parallel canonical store. |
| R-02 | `dev_master` must not create a parallel approval controller. |
| R-03 | Execution Worker must not decide final approval. |
| R-04 | Runner facts must be preserved in local append-only evidence; optional external writeback must be explicit. |
| R-05 | Phase 1 must restrict execution to local diff/draft only; merge/deploy is out of scope. |
| R-06 | Only `runner_contract_version` is owned by dev_master in Phase 1. |
| R-07 | Deferred/future capabilities require activation proposal. |
| R-08 | Autonomy widening and demotion require append-only ratchet records. |
| R-09 | Human review defaults to async queue; timeout default must never be approve. |
| R-10 | Current-window cost ceilings are hard verifier blocks. |
| R-11 | Hard red line and mature-library-only cores must not be implemented from scratch. |

---

## Archive Pointers

| Topic | Location |
|-------|----------|
| Ops / TechRadar blueprint | [10-ops-ai.md](../40-future/10-ops-ai.md) |
| Advisor blueprint | [11-advisor-ai.md](../40-future/11-advisor-ai.md) |
| Rewrite / model governance blueprint | [12-disaster-recovery.md](../40-future/12-disaster-recovery.md) |
| Mined v3 durable ideas | [durable-ideas-from-v3.md](durable-ideas-from-v3.md) |

These files are product-scope references. They are not active runtime
implementation approval by themselves.

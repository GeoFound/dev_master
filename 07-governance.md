# Governance Boundary

> `dev_master` does not own governance. It maps software-change facts to `menmery` action levels and approval lanes.

---

## 7.1 Source Of Authority

| Concern | Owner |
|---------|-------|
| canonical truth | `menmery` |
| audit / supersede / evidence lineage | `menmery` |
| action level / approval lane | `menmery` |
| LLM routing/model governance | `auto_router` |
| runner facts / diff / checks | `dev_master` |

---

## 7.2 Software Risk Labels

Risk labels are local convenience labels:

| Label | Typical facts | Required mapping |
|-------|---------------|------------------|
| green | docs/test-only, repo-local validation scaffold, local diff, checks pass | action level 1-2 |
| yellow | application code, dependency, external PR/write | action level 2-3 |
| red | deploy, merge, migration, delete, secrets, permissions | action level 4 |

If label and action level disagree, the higher-risk interpretation wins.

---

## 7.3 Approval

Final approval must include:

- `menmery` governance preview or audit reference
- action level
- runner facts digest
- verifier decision
- human approver if required

Execution Worker cannot approve its own result.

---

## 7.4 Forbidden In Phase 1

- parallel canonical store
- approval controller outside `menmery`
- automatic merge/deploy
- active Ops/Advisor/TechRadar
- model governance rollout
- generic adapter platform

---

## 7.5 Procurement

Any paid service or subscription change is at least yellow. Anything above USD 50/month or with unclear recurring cost is red and requires explicit human approval.

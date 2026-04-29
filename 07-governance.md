---
status: active
scope: product
authority: this
---

# Governance Boundary

> `dev_master` owns product-level governance design for the AI automation
> pipeline. In the current implementation window, it does not own the canonical
> truth/governance runtime. It maps software-change facts to `menmery` action
> levels and approval lanes when that integration is available.
>
> Historical `BOUNDARIES.md` examples are now consolidated here. This file is
> the current authority for zone boundaries, procurement thresholds, and
> escalation rules.

---

## 7.1 Source Of Authority

| Concern | Owner |
|---------|-------|
| canonical truth | `menmery` |
| audit / supersede / evidence lineage | `menmery` |
| action level / approval lane | `menmery` |
| LLM routing execution / runtime planner / model failover | `auto_router` |
| routing feedback / low-risk learner optimization | `auto_router` |
| product-level model requirements and release policy | `dev_master`, coordinated with `auto_router` |
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

## 7.3 Zone Taxonomy

The durable v3 zone detail is still valid at the policy level. Product
capabilities may be deferred, but the boundary categories themselves should
remain explicit.

### Red Zone

Red means AI may prepare material, but execution or final decision remains
human-owned.

Common red-zone examples:

- payment or billing rule changes
- production data deletion or irreversible cleanup
- cross-border or regulated data transfer decisions
- destructive database migration
- new recurring paid service above USD 50/month
- cancellation of an existing paid subscription
- architecture refactor that affects more than 3 slices
- rewrite work that spans more than 3 slices

### Yellow Zone

Yellow means AI may prepare bounded work or proposals, but a human approval
step is required before promotion or execution.

Common yellow-zone examples:

- new API endpoint
- data model change
- major-version dependency upgrade
- new paid service at or below USD 50/month
- subscription upgrade to the next plan
- dependency replacement with behavior compatibility claims
- operational tuning outside a preapproved narrow range

### Green Zone

Green means the work may run automatically when the active phase, evidence, and
tooling support it.

Common green-zone examples:

- documentation update
- style-only or log-only change
- test additions
- low-risk repo-local validation scaffolding
- bounded patch security update with no destructive side effects
- development-only dependency minor/patch update
- preapproved rollback or hygiene action whose only goal is restoring the last
  known good state

Ops-style green examples do not activate Ops runtime in Phase 1. They are
future activation examples only.

When a case is disputed or spans multiple zones, treat it as red until a human
authority narrows it.

---

## 7.4 Approval

Final approval must include:

- `menmery` governance preview or audit reference
- action level
- runner facts digest
- verifier decision
- human approver if required

Execution Worker cannot approve its own result.

---

## 7.5 Procurement Proposal Minimums

Any procurement, subscription, or replacement proposal should include at least:

1. 30-day usage evidence for the current approach when available.
2. Public benchmark, advisory, or user evidence for the proposed replacement.
3. Migration cost estimate, including engineering time and continuity risk.
4. Quantified expected benefit such as savings, risk reduction, or performance
   improvement.
5. Security evidence when the proposal is driven by vulnerability or compliance
   concerns.

Recommended proposal validity windows:

- security: 7 days
- dependency replacement: 30 days
- tool procurement: 14 days
- budget optimization: 30 days
- architecture proposal: 14 days
- model-related proposal: 14 days
- ops proposal: 7 days

Expired proposals should not auto-regenerate immediately; they should be
reevaluated on the next governed scan or human request.

---

## 7.6 Forbidden In Phase 1

- parallel canonical store
- approval controller outside `menmery`
- automatic merge/deploy
- active Ops/Advisor/TechRadar
- model governance rollout that duplicates `auto_router`
- generic adapter platform

---

## 7.7 Procurement

Any paid service or subscription change is at least yellow. Anything above USD 50/month or with unclear recurring cost is red and requires explicit human approval.

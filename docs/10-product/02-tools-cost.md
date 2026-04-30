---
status: active
scope: product
authority: this
---

# Tools And Cost Boundary

> Historical `cost_policy.yaml` details are consolidated here until a rewrite
> restores implementation configuration. Specific model IDs and routing chains
> belong to `auto_router`, not to this file.

---

## Product Tool Boundary

`dev_master` owns the AI automation pipeline product. Tool choices should serve
the pipeline without turning a dependency into the product owner.

| Tool family | Product role |
|-------------|--------------|
| AI coding agents | implementation, review, test generation, analysis |
| local worktree / sandbox / container | repo mutation boundary and isolation |
| test / lint / security scanners | runner facts and result gate inputs |
| release / deploy / rollback tools | later release safety and operations flow |
| observability tools | later health, SLO, incident, and feedback signals |
| `menmery` MCP facade | cognitive context, truth/evidence, governance preview, approval lane |
| `auto_router` | LLM routing control plane, runtime planner, model execution boundary, failover/learner feedback |

Older mined v3 ideas are indexed in
[durable-ideas-from-v3.md](../90-reference/durable-ideas-from-v3.md). Current implementation must still be gated by
[26-design-closure-review.md](../00-entry/26-design-closure-review.md) and a human-approved
rewrite plan.

Concrete current-window ceilings live in
[cost-ceilings.md](../20-current-window/cost-ceilings.md). Those limits are
verifier-enforced hard blocks, not soft alerts.

---

## Current Implementation Window

The deleted Phase 0-3 implementation used a deliberately small tool surface:

- `just` for stable command entry points
- Bash only for small repository checks
- Python for runner / harness / verifier implementation
- local files for fallback reports and sample evidence
- `menmery` for context, governance preview, action level, and evidence
  writeback when available
- `auto_router` for routed LLM calls and model execution when a current task
  needs them

After the 2026-04-27 implementation reset, this list is candidate guidance for
the rewrite plan, not an active command surface.

---

## Cost Rules

- Prefer already-available local and subscription tools for the current window.
- Any paid, recurring, or external side effect must appear in runner facts or
  the relevant evidence report.
- Current-window variable spend starts with
  `per_project_daily_usd: 5`, `global_daily_usd: 30`,
  `soft_alert_at_pct: 80`, and `hard_block: true`.
- Autonomous purchasing, production deploy, active background scanning, and
  model-governance rollout require an activation proposal and human gate.
- `dev_master` must not build a parallel model router, fallback planner, or
  learner publisher. Those belong to `auto_router`.
- Cost policy is product-level: current-window restrictions prevent accidental
  spend, but they do not remove future Ops, Advisor, TechRadar, or model
  governance capabilities from the roadmap.

---

## Rewrite Baseline Cost Policy

The durable structure recovered from v3 is still useful, but it must be adapted
to current boundaries:

- subscription usage should be consumed first because it is already-paid cost
- variable-cost routed execution should be budgeted separately from proactive
  sensing
- model selection and fallback chains belong to `auto_router`
- budget ceilings, degradation thresholds, and approval requirements belong to
  `dev_master`

Suggested rewrite baseline:

```yaml
cost_policy:
  subscriptions:
    primary_execution: "already-paid coding subscriptions"
    secondary_execution: "optional already-paid overflow path"
    fixed_monthly_budget_usd: "<recorded for reporting>"

  routed_execution_budget:
    gateway_owner: "auto_router"
    monthly_budget_usd: "<human-set>"
    alert_threshold: 0.7
    hard_stop: true

  proactive_sensing_budget:
    monthly_budget_usd: "<human-set>"
    alert_threshold: 0.7
    degradation:
      level_1: "reduce TechRadar / sensing frequency"
      level_2: "pause proactive advisory work; keep low-cost core checks only"

  quota_management:
    level_0: "normal"
    level_1: "overflow to secondary already-paid path"
    level_2: "delay non-critical tasks"
    level_3: "critical-only routed overflow; queue the rest"

  procurement_governance:
    auto_approve_max_monthly_usd: 0
    yellow_zone_max_monthly_usd: 50
    red_zone_threshold_usd: 50
```

This keeps the useful budget structure from v3 without reintroducing local
model-routing ownership.

---

## Cost Degradation Rules

Quota or spend pressure should degrade in this order:

| Level | Trigger type | Expected action |
|-------|--------------|-----------------|
| `L0` | normal quota and spend | run normally |
| `L1` | primary subscription quota tight | overflow to secondary already-paid path |
| `L2` | both subscription paths tight | delay non-critical tasks to the next window |
| `L3` | all subscription quota exhausted | only critical tasks may use routed variable-cost execution |
| `S1` | variable-cost budget > 70% | reduce proactive sensing frequency; review routed usage |
| `S2` | variable-cost budget > 90% | pause non-essential sensing/advisory calls; preserve only governed critical paths |

The key rule is that cost pressure should first reduce optional work, then
delay non-critical work, and only last use additional paid overflow.

---

## Cost Evidence Requirements

When a task uses paid or quota-constrained capability, evidence should capture
at least:

- `trace_id`
- tool family or gateway path used
- `cost_mode`
- `quota_state` or degradation level
- estimated or actual cost when measurable
- approval reference when a paid side effect or procurement decision occurred

Machine-readable cost-bearing artifacts should also follow `docs/10-product/CONTRACTS.md`.

---

## Upgrade And Reduction Triggers

The mined v3 trigger logic is still worth keeping at the policy level:

- if primary execution quota repeatedly exhausts before the end of the working
  window, generate a subscription-upgrade proposal instead of silently
  overspending
- if routed variable-cost usage stays above 80% of budget for multiple review
  periods, review whether tasks should move back to subscription paths
- if proactive sensing cost stays above threshold, reduce scan frequency before
  cutting governed execution paths
- if actual usage stays materially below fixed-cost capacity, generate a
  downgrade or consolidation proposal rather than leaving cost drift hidden

Procurement and subscription changes still map through
`docs/10-product/07-governance.md`.

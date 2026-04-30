---
status: active
scope: window
authority: this
---

# Cost Ceilings

This file defines concrete current-window spend ceilings. These numbers are
starting guardrails, not economic truth. Changing them requires an evidence
record and human approval when the change increases spend.

---

## 1. Current Limits

```yaml
cost_ceiling_policy:
  per_project_daily_usd: 5
  global_daily_usd: 30
  soft_alert_at_pct: 80
  hard_block: true
  timeout_default_decision: "hold"
```

The hard block is verifier-enforced. A run that would exceed the ceiling must
not continue as a soft warning.

---

## 2. Required Cost Facts

Every cost-bearing run must emit:

```yaml
project_id: "dev_master"
trace_id: "tr_..."
run_id: "run_..."
estimated_usd: 0.0
actual_usd: null
per_project_daily_spend_usd: 0.0
global_daily_spend_usd: 0.0
ceiling_status: "within_limit|soft_alert|hard_block"
policy_version: "cost-ceilings-v1"
```

---

## 3. Blocking Rules

Verifier must block when:

- `ceiling_status` is `hard_block`
- required cost facts are missing for a paid or quota-constrained action
- spend would exceed `per_project_daily_usd`
- spend would exceed `global_daily_usd`
- a paid side effect lacks the required human approval reference

At `soft_alert_at_pct`, the run may continue only if it remains within the hard
ceiling and records the alert in evidence.

---

## 4. Scope

These ceilings apply to current-window LLM calls, hosted preview services,
paid APIs, background sensing, and any other variable-cost external side
effect. Already-paid local or subscription usage should still report quota
pressure when measurable, but it does not consume these USD ceilings unless it
creates additional variable cost.

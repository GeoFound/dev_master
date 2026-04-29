---
status: future
scope: integration
authority: this
---

# External Model-Governance Integration

> Future authority for how `dev_master` should integrate with an external model
> routing and governance control plane such as `auto_router`.

---

## 31.1 Core Position

`dev_master` must not grow its own local model control plane.

External control plane responsibilities remain external:

- model registry
- benchmark and shadow rollout
- primary/fallback routing
- rollout gates
- model lifecycle audit

`dev_master` is responsible for:

- stage-level requirements
- request/result/feedback linkage
- local degradation when the gateway is unavailable
- governed evidence about the effect on software-delivery work

---

## 31.2 Stable Integration Surface

Future integration should assume a stable external API surface rather than
internal imports.

Minimum categories:

- request execution
- result capture
- feedback submission
- health/availability observation

If the control plane changes its internal strategy, `dev_master` should not
need a redesign as long as the external contract remains stable.

---

## 31.3 Local Responsibilities

For every routed stage, local records should preserve:

- `trace_id`
- `run_id`
- `step_id`
- `request_id` when provided
- stage name
- gateway success/failure state
- verifier or human feedback linkage
- cost or latency observations when available

This is the local accountability layer, not a replacement for gateway audit.

---

## 31.4 Degradation And Recovery

When the external gateway is degraded or unavailable:

- do not build an internal replacement router
- delay gateway-dependent tasks when possible
- preserve already-paid direct/subscription paths only when preapproved
- escalate to human review when the delay breaches the allowed window
- record degradation scope and recovery timing

Future local recovery targets:

- delay decision within 5 minutes
- human escalation within 15 minutes
- normal routing resumes when the external control plane is healthy again

---

## 31.5 Observed Metrics

Useful local integration metrics include:

- `gateway_availability`
- `gateway_latency_p95`
- `gateway_feedback_link_rate`
- `gateway_cost_per_success`
- `gateway_error_rate`

These are local operational observations. They are not substitutes for the
control plane's own rollout metrics.

---

## 31.6 Gateway Audit Event

Local request/result/feedback correlation should emit a structured event and
follow `CONTRACTS.md`.

Example:

```jsonl
{
  "timestamp": "2026-05-02T08:30:00Z",
  "artifact_family": "gateway_request_result_feedback",
  "schema_version": "1.0.0",
  "trace_id": "tr_gateway_20260502a1",
  "event_type": "gateway_request_result_feedback",
  "tenant": "dev-master",
  "request_id": "req_123",
  "stage": "verifier",
  "gateway_status": "success",
  "cost_usd": 0.07,
  "feedback_sent": true,
  "policy_version": "v4.0",
  "ruleset_version": "gateway-link-v1"
}
```

---

## 31.7 Boundary Rules

- external intelligence may propose boundary changes, but it may not directly
  loosen `dev_master` boundaries
- any autonomy expansion still requires governed trust-evolution style review
- local docs may describe integration behavior, but must not reclaim registry,
  rollout, or fallback ownership from the external control plane

---

## 31.8 Non-Goals

This blueprint does not authorize:

- local model registry
- local shadow/primary rollout controller
- local fallback chain publisher
- local model lifecycle system parallel to `auto_router`

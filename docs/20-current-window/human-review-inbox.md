---
status: active
scope: window
authority: this
---

# Human Review Inbox

The default review model is asynchronous queueing. Synchronous blocking is a
special case for red-line operations, not the 24/7 factory default.

Every queued review item must have a timeout policy. The timeout default must
never be `approve`.

---

## 1. Default Policy

```yaml
default_review_mode: "async_queue"
default_decision_after_timeout: "hold"
timeout_must_not_auto_approve: true
```

Synchronous review is allowed only for:

- red-line operations from [autonomy-ratchet.md](autonomy-ratchet.md)
- human-requested live pairing
- emergency correction / rollback decisions

---

## 2. Payload Schema

```yaml
review_id: "review_..."
trace_id: "tr_..."
run_id: "run_..."
project_id: "dev_master"
risk_label: "green|yellow|red"
action_level: 0
requested_decision: "approve|hold|correct|rollback|promote"
default_decision_after_timeout: "hold"
timeout_at: "2026-04-30T00:00:00Z"
summary: "short decision summary"
evidence_refs:
  - "ev_..."
diff_refs:
  - "sha256:..."
verifier_decision: "allow|block|escalate"
cost_facts:
  estimated_usd: 0.0
  cost_ceiling_status: "within_limit|soft_alert|hard_block"
schema_version: "1.0.0"
policy_version: "human-review-inbox-v1"
ruleset_version: "inbox-routing-v1"
```

---

## 3. Timeout Table

| Risk class | Default timeout | Timeout decision |
|------------|-----------------|------------------|
| `green` | 24h | `hold` |
| `yellow` | 24h | `hold` |
| `red` | 4h | `hold` |
| hard red line | no async auto-progress | synchronous human decision required |

Timed-out items remain visible in the inbox. A timeout may stop queued work or
move dependent work to hold; it must not approve the action.

---

## 4. Queue Behavior

- independent green work may continue while an unrelated review item is held
- dependent work must wait for `approve` or `correct`
- blocked or timed-out items must preserve evidence and verifier reasons
- a human decision must be recorded as append-only evidence before execution
  resumes

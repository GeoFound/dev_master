# Gate Report Template

```yaml
gate: "A|B|C|D"
phase: ""
date: ""
status: "pass|fail|hold"
decision_requested: "promote|hold|correct|rollback"
menmery_context_used: "refs or fallback reason"
evidence:
  - ""
pass_conditions:
  - condition: ""
    result: "pass|fail|unknown"
    evidence_ref: ""
fail_conditions:
  - condition: ""
    result: "not_triggered|triggered|unknown"
    evidence_ref: ""
plane_boundary_check:
  orchestration: ""
  execution: ""
  evidence: ""
risk_facts:
  action_level: "0|1|2|3|4"
  risk_label: "green|yellow|red"
drift_found:
  - ""
recommendation_for_human: ""
next_allowed_action: ""
```

# Drift Check Template

```yaml
task_id: ""
task_type: "drift-check-task"
baseline_design:
  - "00-index.md"
  - "20-layered-program-map.md"
  - "23-menmery-integration.md"
current_output:
  - ""
drift_dimensions:
  target_drift: "none|present"
  implementation_drift: "none|present"
  governance_drift: "none|present"
severity_rules:
  low: "wording or local evidence issue"
  medium: "active docs unclear or incomplete"
  high: "active scope expands beyond Phase 0-3 or competes with menmery"
required_decision: "accept|correct|rollback|freeze"
evidence:
  - ""
```

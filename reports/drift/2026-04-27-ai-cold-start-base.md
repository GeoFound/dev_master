# Drift Check - AI Cold Start Base

```yaml
task_id: "phase-0-ai-cold-start-base"
task_type: "drift-check-task"
baseline_design:
  - "00-index.md"
  - "20-layered-program-map.md"
  - "23-menmery-integration.md"
  - "18-master-execution-task.md"
current_output:
  - "24-ai-cold-start.md"
  - "tasks/current.md"
  - "tasks/backlog.md"
  - "templates/"
  - "contracts/software-change-runner-v1.yaml"
  - "reports/gate-a-design-freeze.md"
  - "scripts/check_ai_base.sh"
drift_dimensions:
  target_drift: "none"
  implementation_drift: "none"
  governance_drift: "none"
severity_rules:
  low: "template wording mismatch"
  medium: "AI entry path incomplete"
  high: "new runtime, approval controller, canonical store, or deferred capability activation"
required_decision: "accept"
evidence:
  - "No product runtime added."
  - "No parallel truth/governance/evidence runtime added."
  - "Deferred/future capabilities remain activation-proposal only."
  - "Local reports are explicitly fallback evidence."
  - "Repo-local check scripts are classified as green only because this is a documentation repository and no external writes, dependencies, secrets, infra, deploy, or migration behavior were added."
decision: "accept"
```

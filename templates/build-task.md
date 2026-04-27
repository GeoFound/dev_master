# Build Task Template

```yaml
task_id: ""
task_type: "build-task"
goal: ""
plane: "orchestration | execution | evidence | verification | docs"
scope_in:
  - ""
scope_out:
  - ""
dependencies:
  - ""
deliverables:
  - ""
acceptance_checks:
  - ""
rollback_if_failed: ""
side_effects:
  repo_mutation: false
  shell_execution: false
  external_service_calls: false
  evidence_write: "none | local_report | menmery_remember | governed_canonical_write"
evidence_outputs:
  - ""
risk_facts:
  action_level: "0|1|2|3|4"
  risk_label: "green|yellow|red"
  docs_only: false
  repo_local_ai_scaffold: false
  dependency_changed: false
  secrets_or_permissions_changed: false
  infra_or_deploy_path_changed: false
menmery_context: "get_context/act/remember refs or fallback reason"
```

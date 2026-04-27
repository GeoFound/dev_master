# Repo Structure

> This is the reference layout for a future implementation repo plus the local
> AI cold-start scaffolding for this documentation repository. The scaffolding
> is not product runtime.

---

## Active Implementation Shape

```text
dev_master/
  tasks/
    current.md
    backlog.md
  templates/
    build-task.md
    verify-task.md
    drift-check.md
    gate-report.md
    activation-proposal.md
    runner-facts.yaml
    verification-report.md
  contracts/
    software-change-runner-v1.yaml
  reports/
    gate-a-design-freeze.md
    drift/
  scripts/
    check_ai_base.sh
  docs/
    ADR/
  menmery/
    software_change_mapping.md
    caller_checklist.md
  runner/
    contract.md
    local_worktree_runner.py
  verifier/
    verifier_contract.md
  schemas/
    runner-facts.schema.json
  AGENTS.md
  BOUNDARIES.md
  RULES.md
```

Only one dev_master-owned version is required in Phase 1:

```yaml
runner_contract_version: "software-change-runner-v1"
```

---

## Not Active

Do not create these as active directories before activation:

- `ops/`
- `advisor/`
- `techradar/`
- `rewrite/`
- `model_gov/`
- `adapters/`
- `canonical/`
- `approval-controller/`

---

## Runner Repos

Untrusted or high-permission runners may become separate repos:

```text
codex-worker/
claude-code-worker/
sandbox-worker/
```

They should communicate through runner facts and `menmery` evidence refs, not direct imports.

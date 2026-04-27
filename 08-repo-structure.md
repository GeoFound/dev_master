# Repo Structure

> This is the reference layout for a future implementation repo. This documentation repo itself is not executable code.

---

## Active Implementation Shape

```text
dev_master/
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

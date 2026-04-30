---
status: active
scope: repo
authority: ref-only
---

# Repo Structure

> This is the reference layout for a future implementation repo plus the local
> AI cold-start scaffolding for this documentation repository. The scaffolding
> is not product runtime.

---

## Current Documentation Shape

```text
docs/
  README.md
  00-entry/
    00-index.md
    24-ai-cold-start.md
    26-design-closure-review.md
  10-product/
    02-tools-cost.md
    03-ai-roles.md
    04-pipeline.md
    05-quality.md
    06-observability.md
    07-governance.md
    09-roadmap.md
    28-product-principles.md
    engineering-execution-boundaries.md
    CONTRACTS.md
  20-current-window/
    06b-state-persistence.md
    14-master-program.md
    15-phase-gates.md
    16-drift-control.md
    17-task-templates.md
    18-master-execution-task.md
    19-human-governance-boundary.md
    20-layered-program-map.md
    21-agent-behavior-guidelines.md
    22-three-plane-architecture.md
    25-implementation-language-baseline.md
    autonomy-ratchet.md
    human-review-inbox.md
    cost-ceilings.md
    REWRITE-PLAN.md
  30-integrations/
    23-menmery-integration.md
    27-external-systems-boundary.md
  40-future/
    09b-adaptation-selftest.md
    10-ops-ai.md
    11-advisor-ai.md
    12-disaster-recovery.md
    29-rewrite-blueprint.md
    30-project-adapter-blueprint.md
    31-external-model-governance-integration.md
  90-reference/
    08-repo-structure.md
    13-appendix.md
    durable-ideas-from-v3.md
```

This physical layout is a navigation and authority-boundary aid. It does not
change which documents are active, deferred, future-only, or historical; those
statuses still come from the file front matter, [00-index.md](../00-entry/00-index.md),
and `runtime/doc-registry.json`.

---

## Historical Implementation Shape

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
  25-implementation-language-baseline.md
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

This shape is not active after the 2026-04-27 implementation reset. It remains
as design reference only.

The previous local contract version was:

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

---

## Language Baseline

The previous Phase 1 baseline used Python for runner / harness / verifier code
and `just` plus Bash for repository command wrappers. After the reset, this is
candidate guidance only.

See [25-implementation-language-baseline.md](../20-current-window/25-implementation-language-baseline.md).

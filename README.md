# dev_master

`dev_master` is a design reference repository for the `software_change` capability/harness that works with:

- `menmery` for truth, canonical evidence, governance preview, and action levels
- `auto_router` for LLM routing, model selection, failover, and cost/model governance
- isolated execution workers for repo mutation, tests, scans, and runner facts

Start with [24-ai-cold-start.md](24-ai-cold-start.md) and
[tasks/current.md](tasks/current.md), then read [00-index.md](00-index.md) and
[23-menmery-integration.md](23-menmery-integration.md).

This repo is documentation plus repository-level AI automation scaffolding. It
does not contain runnable product code.

## Current Active Scope

- Phase 0-3 only
- three active roles only
- no parallel canonical store or approval controller
- no active Ops/Advisor/TechRadar/rewrite/model-governance implementation

## Check

```bash
just check
just cold-start
just validate-contract
just drift-check
just gate-a
```

---
status: active
scope: repo
authority: ref-only
---

# Docs

The documentation is physically layered so current authority, active build
program, integrations, future blueprints, and references are not mixed.

| Layer | Directory | Purpose |
|-------|-----------|---------|
| Entry | [00-entry/](00-entry/) | index, AI cold start, current rebuild state pointer |
| Product | [10-product/](10-product/) | product principles, contracts, pipeline, roles, quality, governance, roadmap |
| Current window | [20-current-window/](20-current-window/) | Phase 0-3 program, gates, task rules, rewrite plan, active architecture constraints |
| Integrations | [30-integrations/](30-integrations/) | `menmery` and `auto_router` boundaries and optional service contracts |
| Future | [40-future/](40-future/) | deferred runtime and future-only blueprints |
| Reference | [90-reference/](90-reference/) | supporting references and stale recovered source material |

Key current-window contracts:

- [20-current-window/autonomy-ratchet.md](20-current-window/autonomy-ratchet.md)
- [20-current-window/human-review-inbox.md](20-current-window/human-review-inbox.md)
- [20-current-window/cost-ceilings.md](20-current-window/cost-ceilings.md)

Key implementation policy:

- [10-product/engineering-execution-boundaries.md](10-product/engineering-execution-boundaries.md)
- [10-product/product-architecture-decision.md](10-product/product-architecture-decision.md)
- [10-product/task-proposal-contract.md](10-product/task-proposal-contract.md)

Start with [00-entry/00-index.md](00-entry/00-index.md).

---
status: active
scope: repo
authority: ref-only
---

# dev_master

`dev_master` is a documentation-first repository for an independent AI
automation pipeline product.

## Current State

- The repository is docs-only after the 2026-04-27 implementation reset.
- Deleted implementation assets are not active evidence and cannot be reused as
  Gate B proof.
- Any new implementation work requires a human-approved rewrite plan.
- The recovered v3 document is a historical mining source only.

## Read First

For humans:

1. [README.md](README.md)
2. [27-external-systems-boundary.md](27-external-systems-boundary.md)
3. [28-product-principles.md](28-product-principles.md)
4. [CONTRACTS.md](CONTRACTS.md)
5. [26-design-closure-review.md](26-design-closure-review.md)
6. [REWRITE-PLAN.md](REWRITE-PLAN.md)
7. [00-index.md](00-index.md)

For AI sessions:

1. [AGENTS.md](AGENTS.md)
2. [24-ai-cold-start.md](24-ai-cold-start.md)
3. [CONTRACTS.md](CONTRACTS.md)
4. [26-design-closure-review.md](26-design-closure-review.md)
5. [REWRITE-PLAN.md](REWRITE-PLAN.md)
6. [00-index.md](00-index.md)

## Authority Map

| Topic | File | Role |
|-------|------|------|
| external system boundary | [27-external-systems-boundary.md](27-external-systems-boundary.md) | sole authority for `menmery` / `auto_router` boundaries |
| product principles | [28-product-principles.md](28-product-principles.md) | durable product intent |
| contract governance | [CONTRACTS.md](CONTRACTS.md) | machine-readable artifact and version discipline |
| current docs-only state | [26-design-closure-review.md](26-design-closure-review.md) | current state pointer and allowed work |
| current rewrite draft | [REWRITE-PLAN.md](REWRITE-PLAN.md) | first post-reset executable-slice plan |
| document navigation | [00-index.md](00-index.md) | layer and status map |

## Historical Source

Use [recovered/AI-autonomous-dev-pipeline-v3.md](recovered/AI-autonomous-dev-pipeline-v3.md)
only to recover durable ideas that have not yet been reintroduced into current
modular docs. It must not override the active boundary, principle, or
current-window documents.

---
status: active
scope: repo
authority: ref-only
---

# dev_master

`dev_master` is a blueprint-first engineering repository for an independent AI
automation pipeline product and factory. The markdown files are the rebuild
authority for the post-reset implementation, not the product's end state.

The repository now also contains a first machine-readable progression runtime
under `runtime/`, `runtime_engine/`, and `bin/`. That runtime does not replace
the blueprint; it compiles the active blueprint into current-task state and
next-step transitions.

## Current State

- The pre-reset implementation was removed on 2026-04-27; the repository now
  holds the authoritative blueprint for rebuilding executable slices from
  scratch.
- Deleted implementation assets are not active evidence and cannot be reused as
  Gate B proof.
- New implementation work should be derived from the active blueprint docs,
  phase gates, and rewrite/build plan rather than revived by implication from
  deleted assets.
- The recovered v3 source has been removed from active docs; mined ideas are
  tracked in `docs/90-reference/durable-ideas-from-v3.md`.
- The current machine-readable work pointer is `runtime/current-task.json`.

## Read First

For humans:

1. [README.md](README.md)
2. [docs/30-integrations/27-external-systems-boundary.md](docs/30-integrations/27-external-systems-boundary.md)
3. [docs/10-product/28-product-principles.md](docs/10-product/28-product-principles.md)
4. [docs/10-product/product-architecture-decision.md](docs/10-product/product-architecture-decision.md)
5. [docs/10-product/task-proposal-contract.md](docs/10-product/task-proposal-contract.md)
6. [docs/10-product/CONTRACTS.md](docs/10-product/CONTRACTS.md)
7. [docs/00-entry/26-design-closure-review.md](docs/00-entry/26-design-closure-review.md)
8. [docs/20-current-window/REWRITE-PLAN.md](docs/20-current-window/REWRITE-PLAN.md)
9. [docs/README.md](docs/README.md)
10. [docs/00-entry/00-index.md](docs/00-entry/00-index.md)

For AI sessions:

1. [AGENTS.md](AGENTS.md)
2. [docs/00-entry/24-ai-cold-start.md](docs/00-entry/24-ai-cold-start.md)
3. [docs/10-product/CONTRACTS.md](docs/10-product/CONTRACTS.md)
4. [docs/10-product/product-architecture-decision.md](docs/10-product/product-architecture-decision.md)
5. [docs/10-product/task-proposal-contract.md](docs/10-product/task-proposal-contract.md)
6. [docs/00-entry/26-design-closure-review.md](docs/00-entry/26-design-closure-review.md)
7. [docs/20-current-window/REWRITE-PLAN.md](docs/20-current-window/REWRITE-PLAN.md)
8. [docs/README.md](docs/README.md)
9. [docs/00-entry/00-index.md](docs/00-entry/00-index.md)

## Authority Map

| Topic | File | Role |
|-------|------|------|
| external system boundary | [docs/30-integrations/27-external-systems-boundary.md](docs/30-integrations/27-external-systems-boundary.md) | sole authority for `menmery` / `auto_router` boundaries |
| product principles | [docs/10-product/28-product-principles.md](docs/10-product/28-product-principles.md) | durable product intent |
| product architecture decision | [docs/10-product/product-architecture-decision.md](docs/10-product/product-architecture-decision.md) | runtime shape, language split, surfaces, provider strategy |
| task proposal contract | [docs/10-product/task-proposal-contract.md](docs/10-product/task-proposal-contract.md) | AI proposal to `dev_master` authorization handoff |
| contract governance | [docs/10-product/CONTRACTS.md](docs/10-product/CONTRACTS.md) | machine-readable artifact and version discipline |
| engineering execution boundaries | [docs/10-product/engineering-execution-boundaries.md](docs/10-product/engineering-execution-boundaries.md) | dynamic implementation boundaries and quality floors |
| current rebuild baseline | [docs/00-entry/26-design-closure-review.md](docs/00-entry/26-design-closure-review.md) | current state pointer, rebuild constraints, and allowed work |
| current rewrite draft | [docs/20-current-window/REWRITE-PLAN.md](docs/20-current-window/REWRITE-PLAN.md) | first post-reset executable-slice plan |
| autonomy ratchet | [docs/20-current-window/autonomy-ratchet.md](docs/20-current-window/autonomy-ratchet.md) | evidence-based autonomy widening and demotion |
| human review inbox | [docs/20-current-window/human-review-inbox.md](docs/20-current-window/human-review-inbox.md) | async review queue and timeout defaults |
| cost ceilings | [docs/20-current-window/cost-ceilings.md](docs/20-current-window/cost-ceilings.md) | hard current-window spend limits |
| docs layer entry | [docs/README.md](docs/README.md) | physical documentation layer map |
| document navigation | [docs/00-entry/00-index.md](docs/00-entry/00-index.md) | layer and status map |
| machine-readable task state | `runtime/current-task.json` | current bounded task derived from the active blueprint |
| implementation spine | `runtime/implementation-spine.json` | stable build order and anti-drift construction logic |

## Historical Source

The full recovered v3 source has been removed from active docs. Use
[docs/90-reference/durable-ideas-from-v3.md](docs/90-reference/durable-ideas-from-v3.md)
to see where mined ideas landed. Use git history or archived evidence only if
new historical mining is necessary.

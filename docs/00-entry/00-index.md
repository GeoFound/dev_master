---
status: active
scope: repo
authority: ref-only
---

# dev_master Index

> Navigation by layer and activation state. Use files marked `authority: this`
> as the current specification. Use `ref-only` files as pointers and entry docs.
> These files are blueprint and build-program authority for reconstruction; they
> are not meant to replace the final product runtime.

## L0 Identity And Boundary

- [README.md](../../README.md) — human-facing entry and authority map
- [AGENTS.md](../../AGENTS.md) — AI-facing entry and working guardrails
- [27-external-systems-boundary.md](../30-integrations/27-external-systems-boundary.md) — sole authority for `menmery` / `auto_router` boundaries
- [28-product-principles.md](../10-product/28-product-principles.md) — product North Star and durable principles
- [product-architecture-decision.md](../10-product/product-architecture-decision.md) — product runtime shape, language split, surfaces, provider strategy
- [task-proposal-contract.md](../10-product/task-proposal-contract.md) — AI proposal to `dev_master` authorization contract

## Physical Document Layers

| Directory | Meaning |
|-----------|---------|
| `00-entry/` | cold start, index, current rebuild state pointer |
| `10-product/` | product principles, contracts, pipeline, roles, quality, governance, roadmap |
| `20-current-window/` | Phase 0-4 build program, gates, task rules, rewrite plan, current architecture constraints |
| `30-integrations/` | sibling-system boundaries and optional integration contracts |
| `40-future/` | future-only product blueprints and deferred runtime designs |
| `90-reference/` | supporting references and historical recovery sources |

## L0.5 Runtime Coordination Artifacts

- `runtime/current-task.json` — current machine-readable task
- `runtime/program-state.json` — phase/gate/task progression state
- `runtime/implementation-spine.json` — persisted construction order and anti-drift build spine
- `runtime/task-graph.json` — machine-readable phase/task graph compiled from active docs
- `runtime/doc-registry.json` — active doc classification used by the progression engine
- `bin/derive_next_task.py` — derive next allowed task from docs + state
- `bin/complete_task.py` — complete current task, persist evidence, and advance state

## L1 Product Specification

### Active Product Specs

- [02-tools-cost.md](../10-product/02-tools-cost.md) — tool boundary and cost discipline
- [03-ai-roles.md](../10-product/03-ai-roles.md) — product role model and current kernel compression
- [CONTRACTS.md](../10-product/CONTRACTS.md) — machine-readable contract and version governance authority
- [04-pipeline.md](../10-product/04-pipeline.md) — end-to-end pipeline and kernel loop
- [05-quality.md](../10-product/05-quality.md) — Result Gate, verifier, and evidence expectations
- [06-observability.md](../10-product/06-observability.md) — active observability core plus deferred sensing extensions
- [07-governance.md](../10-product/07-governance.md) — risk labels, approval mapping, and procurement boundary
- [09-roadmap.md](../10-product/09-roadmap.md) — product roadmap versus current implementation window
- [engineering-execution-boundaries.md](../10-product/engineering-execution-boundaries.md) — dynamic implementation boundaries, mature-library-only zones, and quality floors
- [product-architecture-decision.md](../10-product/product-architecture-decision.md) — active language/runtime/surface/provider decision
- [task-proposal-contract.md](../10-product/task-proposal-contract.md) — task proposal and authorization schema

### Deferred Product Specs

- [09b-adaptation-selftest.md](../40-future/09b-adaptation-selftest.md) — project takeover, adapters, and self-test direction
- [10-ops-ai.md](../40-future/10-ops-ai.md) — Ops AI activation design
- [11-advisor-ai.md](../40-future/11-advisor-ai.md) — Advisor AI activation design

### Future Product Blueprints

- [12-disaster-recovery.md](../40-future/12-disaster-recovery.md) — recovery overview and future-blueprint map
- [29-rewrite-blueprint.md](../40-future/29-rewrite-blueprint.md) — future rewrite workflow, waves, retirement, and knowledge transfer
- [30-project-adapter-blueprint.md](../40-future/30-project-adapter-blueprint.md) — future governance-kernel to project-stack mapping
- [31-external-model-governance-integration.md](../40-future/31-external-model-governance-integration.md) — future external gateway/model-governance integration

## L2 Current Window And Rewrite Preparation

- [14-master-program.md](../20-current-window/14-master-program.md) — current phase program
- [15-phase-gates.md](../20-current-window/15-phase-gates.md) — Gate A-J pass/fail conditions
- [16-drift-control.md](../20-current-window/16-drift-control.md) — drift detection and correction discipline
- [17-task-templates.md](../20-current-window/17-task-templates.md) — standard docs/task shapes
- [18-master-execution-task.md](../20-current-window/18-master-execution-task.md) — end-of-turn reporting structure
- [19-human-governance-boundary.md](../20-current-window/19-human-governance-boundary.md) — human decision contract
- [20-layered-program-map.md](../20-current-window/20-layered-program-map.md) — product scope versus active window
- [21-agent-behavior-guidelines.md](../20-current-window/21-agent-behavior-guidelines.md) — agent behavior expectations
- [22-three-plane-architecture.md](../20-current-window/22-three-plane-architecture.md) — orchestration / execution / evidence boundary
- [23-menmery-integration.md](../30-integrations/23-menmery-integration.md) — `menmery` integration contract
- [24-ai-cold-start.md](24-ai-cold-start.md) — AI entry sequence and stop rules
- [25-implementation-language-baseline.md](../20-current-window/25-implementation-language-baseline.md) — active Phase 1-4 implementation language baseline
- [26-design-closure-review.md](26-design-closure-review.md) — post-reset rebuild baseline and rewrite prerequisites
- [autonomy-ratchet.md](../20-current-window/autonomy-ratchet.md) — evidence-based autonomy widening and demotion
- [human-review-inbox.md](../20-current-window/human-review-inbox.md) — async review queue and timeout defaults
- [cost-ceilings.md](../20-current-window/cost-ceilings.md) — current-window hard spend ceilings
- [REWRITE-PLAN.md](../20-current-window/REWRITE-PLAN.md) — current draft for the first post-reset executable slice

## Supporting References

- [06b-state-persistence.md](../20-current-window/06b-state-persistence.md) — local fallback state and evidence-index guidance
- [08-repo-structure.md](../90-reference/08-repo-structure.md) — historical repo shape and future layout reference
- [13-appendix.md](../90-reference/13-appendix.md) — supplemental notes
- [durable-ideas-from-v3.md](../90-reference/durable-ideas-from-v3.md) — short mapped index of mined v3 ideas
- [ai-instructions.md](../../ai-instructions.md) — thin pointer for AI clients that still load it

## Historical Sources

- Full recovered v3 source was removed from active docs. Use git history or
  archived evidence only when new historical mining is necessary.

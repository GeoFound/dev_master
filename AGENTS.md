---
status: active
scope: repo
authority: ref-only
---

# AGENTS.md - dev_master

## What This Is

This is a **blueprint-first engineering repository** for an independent AI
automation pipeline product. The `.md` files define the factory blueprint,
build program, contracts, gates, and operating rules used to rebuild the
product after the reset. Markdown is construction authority here, not the end
state of the product. Code blocks in docs are design references unless they
live in implementation files.

## Quick Navigation

- **AI cold start**: `docs/00-entry/24-ai-cold-start.md` + `docs/00-entry/26-design-closure-review.md` - required entry path and current allowed work
- **Language baseline**: `docs/20-current-window/25-implementation-language-baseline.md` - active Phase 1-3 Python core / JSON contract / TypeScript surface baseline
- **Product architecture decision**: `docs/10-product/product-architecture-decision.md` - runtime shape, language split, surfaces, provider strategy, deployment default
- **Task proposal contract**: `docs/10-product/task-proposal-contract.md` - AI proposal to `dev_master` authorization handoff
- **Docs layers**: `docs/README.md` - physical documentation layer map
- **Start here**: `docs/00-entry/00-index.md` - full file index with Active Core / Deferred Program / Future Blueprint breakdown
- **Layer map**: `docs/20-current-window/20-layered-program-map.md` - separates product scope from current implementation window
- **Tools & costs**: `docs/10-product/02-tools-cost.md` - product tool boundary and current-window cost policy
- **Contracts**: `docs/10-product/CONTRACTS.md` - machine-readable contract/version governance authority
- **Roles**: `docs/10-product/03-ai-roles.md` - product role architecture and current executable kernel roles
- **Three-plane architecture**: `docs/20-current-window/22-three-plane-architecture.md` - boundary guide for orchestration / execution / evidence references
- **menmery integration**: `docs/30-integrations/23-menmery-integration.md` - integration boundary; `menmery` is not the product owner
- **Current closure**: `docs/00-entry/26-design-closure-review.md` - post-reset rebuild baseline, source status, and rewrite prerequisites
- **Rewrite plan**: `docs/20-current-window/REWRITE-PLAN.md` - current draft for the first post-reset executable slice
- **Autonomy ratchet**: `docs/20-current-window/autonomy-ratchet.md` - evidence-based autonomy widening, demotion, and hard red lines
- **Human review inbox**: `docs/20-current-window/human-review-inbox.md` - async review queue and timeout defaults
- **Cost ceilings**: `docs/20-current-window/cost-ceilings.md` - hard current-window spend limits
- **Runtime task state**: `runtime/current-task.json` + `runtime/program-state.json` - machine-readable current task and phase/gate state
- **Implementation spine**: `runtime/implementation-spine.json` - stable build order for the factory itself; read this when context is long or task selection starts drifting
- **Runtime task compiler**: `runtime/task-graph.json`, `runtime/doc-registry.json`, `bin/derive_next_task.py`, `bin/complete_task.py` - docs-to-task progression surface
- **External systems**: `docs/30-integrations/27-external-systems-boundary.md` - checked boundary for `menmery` and `auto_router`
- **Product principles**: `docs/10-product/28-product-principles.md` - current North Star and durable design intent
- **Engineering execution boundaries**: `docs/10-product/engineering-execution-boundaries.md` - dynamic implementation boundaries, mature-library-only zones, and quality floors
- **Future blueprints**: `docs/40-future/12-disaster-recovery.md`, `docs/40-future/29-rewrite-blueprint.md`, `docs/40-future/30-project-adapter-blueprint.md`, `docs/40-future/31-external-model-governance-integration.md` - future-only authority set for recovery, rewrite, adapters, and external gateway integration
- **Mined v3 ideas**: `docs/90-reference/durable-ideas-from-v3.md` - short index of recovered ideas and current destinations

## Critical Context

### Product Scope vs Current Window

- **Product Scope**: the complete AI automation pipeline: intake, spec,
  critique, implementation, testing, security, result gates, release,
  operations, external sensing, advice, adapters, model governance, rewrite
  governance, recovery, and continuous improvement.
- **Current Implementation Window**: the bounded Phase 0-3 program now being
  proven: cold start, runner facts, verifier, evidence writeback, green
  reliability samples, and yellow preparation.
- **Deferred Runtime**: product capabilities that belong to `dev_master` but
  are not active runtime tasks until evidence and a human gate activate them.

### Active Core Definition (from docs/20-current-window/20-layered-program-map.md)
```
Current implementation window:
1. Phase 0: cold start and design recovery
2. Phase 1: first executable kernel
3. Phase 2: Green reliability
4. Phase 3: Yellow preparation

Hard boundary:
- `dev_master` is the independent AI automation pipeline product.
- `menmery` is long-term cognitive infrastructure. `dev_master` may consume its
  public service surfaces for context, durable memory, governance preview,
  audit, and evidence sinks when that helps the current task. It is a sibling
  dependency, not the parent product, and it does not mutate repositories.
- `auto_router` is the LLM routing control plane and runtime model execution
  boundary. It owns routing planner/failover/learner behavior; `dev_master`
  must not reimplement that router. It is a sibling dependency, not the product
  owner.
- `dev_master` is the scheduling/governance/evidence control plane. Codex,
  Claude Code, API models, `auto_router`, and future agent systems are worker
  providers or routing integrations, not queue/approval/evidence owners.
- before non-doc software-change work, decide whether the task needs optional
  sibling services. Use `menmery` `entry_turn` when long-term context or
  governance preview is useful; otherwise keep the run local and record the
  fallback explicitly.
- orchestration plane owns durable workflow state, retries, timers, approvals.
- execution plane owns repo mutation, shell, builds, tests, scans.
- evidence plane owns immutable local evidence references; when `menmery` is
  used, those references may additionally map to `menmery` record / inbox /
  audit IDs.
- StateStore is runtime index/fallback state, not the product's full durable
  orchestration engine.
- Temporal default is self-hosted only if long-running wait/retry/resume
  exceeds the current facade. Phase 0-1 should not require Temporal
  productionization.
- Do not put large evidence artifacts inside Temporal history; store immutable
  evidence in the evidence plane and keep only references in workflow state.
- Current executable kernel has three runtime roles: Caller/Orchestrator,
  Execution Worker, Verifier/Governor. This does not delete Spec, Critic, Code,
  Test, Security, Ops, Advisor, TechRadar, adapters, model governance, or
  rewrite control from the product architecture.

Not current runtime tasks unless a gate activates them:
- parallel canonical store / approval controller / governance schema that
  competes with the selected canonical evidence/governance integration
- Ops AI continuous monitoring
- Advisor AI proactive proposal loop
- TechRadar scheduled scanning
- Argo/Tekton production rollout
- Tekton Chains full provenance rollout
- GUAC metadata graph
- rewrite controller runtime
- model governance runtime
- generalized adapter runtime
```

### External Dependencies

- **menmery**: User cognitive extension / epistemic runtime (Python project at `/home/jade/projects/menmery`)
- dev_master should use menmery through documented caller protocol / MCP facade, not by importing internal modules
- dev_master may map software-change evidence or approvals into `menmery`
  panoramas, observations, audit, or governed records when that integration is
  available and useful
- **auto_router**: External LLM routing gateway (Go project at `/home/jade/projects/auto_router`)
- dev_master delegates model execution routing, failover, feedback, and low-risk
  routing optimization to auto_router. Any future dev_master model-governance
  work must coordinate with auto_router instead of duplicating its control plane

## Working in This Repo

- Read `docs/00-entry/24-ai-cold-start.md` and `docs/00-entry/26-design-closure-review.md` before choosing work
- Read `runtime/current-task.json` after cold start; it is the current machine-readable task authority unless drift proves it stale
- Read `runtime/implementation-spine.json` when deciding construction order; it is the persisted anti-drift build spine for the whole factory
- Read files starting from `docs/00-entry/00-index.md` for navigation
- Check `docs/20-current-window/20-layered-program-map.md` to confirm if a feature is Active/Deferred/Future
- Check `docs/10-product/CONTRACTS.md` before changing machine-readable artifacts, runner facts,
  verifier outputs, or version fields
- Check `docs/10-product/product-architecture-decision.md` before changing
  product runtime shape, language ownership, product surfaces, provider
  strategy, deployment default, or workspace governance.
- Check `docs/10-product/task-proposal-contract.md` before changing task
  intake, AI-planned slices, provider dispatch, or authorization behavior.
- Check `docs/30-integrations/23-menmery-integration.md` before adding or changing optional
  `menmery` service consumption
- Check `docs/30-integrations/27-external-systems-boundary.md` before describing or changing
  `menmery` / `auto_router` boundaries
- Treat `docs/30-integrations/27-external-systems-boundary.md` as the sibling-system boundary
  authority if another file summarizes the same topic
- Check `docs/20-current-window/REWRITE-PLAN.md` before proposing or recreating implementation assets
- Check `docs/20-current-window/25-implementation-language-baseline.md` before adding implementation files
- Check `docs/10-product/engineering-execution-boundaries.md` before writing
  code, adding integrations, implementing algorithms, or changing tests.
- Check `docs/20-current-window/autonomy-ratchet.md` before changing autonomy,
  queue width, slice limits, unattended duration, or tier movement.
- Check `docs/20-current-window/human-review-inbox.md` before changing review
  payloads, timeout behavior, or async queue semantics.
- Check `docs/20-current-window/cost-ceilings.md` before paid,
  quota-constrained, or externally metered work.
- Don't treat design docs as runnable code - they define contracts, not implementations
- There is no inherited active `just` or script command surface from the
  deleted pre-reset implementation. Recreate commands, scripts, and runtime
  assets from the active blueprint and approved build program instead of
  assuming deleted assets still exist.
- The current rebuilt command surface is intentionally small:
  `python3 bin/derive_next_task.py` derives the next task and
  `python3 bin/complete_task.py` completes the current task and advances state.
- When implementing current-window code, base it on `docs/20-current-window/22-three-plane-architecture.md`, `docs/30-integrations/23-menmery-integration.md`, `StateStore` only for local/fallback state, and `gateway_client.py` for LLM gateway calls where such a client exists

## Key Files by Purpose

| Purpose | File |
|---------|------|
| AI cold start | docs/00-entry/24-ai-cold-start.md, docs/00-entry/26-design-closure-review.md |
| Language baseline | docs/20-current-window/25-implementation-language-baseline.md |
| Product architecture decision | docs/10-product/product-architecture-decision.md |
| Task proposal contract | docs/10-product/task-proposal-contract.md |
| Architecture overview | docs/00-entry/00-index.md |
| Build phases & gates | docs/20-current-window/14-master-program.md, docs/20-current-window/15-phase-gates.md |
| Role definitions | docs/10-product/03-ai-roles.md |
| Risk zones (Red/Yellow/Green) | docs/10-product/07-governance.md |
| Cost model | docs/10-product/02-tools-cost.md |
| State persistence | docs/20-current-window/06b-state-persistence.md |
| Three-plane boundaries | docs/20-current-window/22-three-plane-architecture.md |
| menmery integration boundary | docs/30-integrations/23-menmery-integration.md |
| External system boundaries | docs/30-integrations/27-external-systems-boundary.md |
| Product principles | docs/10-product/28-product-principles.md |
| Engineering execution boundaries | docs/10-product/engineering-execution-boundaries.md |
| Current closure / state pointer | docs/00-entry/26-design-closure-review.md |
| Autonomy ratchet | docs/20-current-window/autonomy-ratchet.md |
| Human review inbox | docs/20-current-window/human-review-inbox.md |
| Cost ceilings | docs/20-current-window/cost-ceilings.md |
| Current machine-readable task | runtime/current-task.json |
| Current machine-readable phase state | runtime/program-state.json |
| Current implementation spine | runtime/implementation-spine.json |
| Future rewrite blueprint | docs/40-future/29-rewrite-blueprint.md |
| Future adapter blueprint | docs/40-future/30-project-adapter-blueprint.md |
| Future external gateway integration | docs/40-future/31-external-model-governance-integration.md |
| Mined v3 idea index | docs/90-reference/durable-ideas-from-v3.md |

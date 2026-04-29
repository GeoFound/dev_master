---
status: active
scope: repo
authority: ref-only
---

# AGENTS.md - dev_master

## What This Is

This is a **design reference documentation** repository for an independent AI
automation pipeline product. The `.md` files define product architecture,
current implementation windows, contracts, gates, and operating rules. Code
blocks in docs are design references unless they live in implementation files.

## Quick Navigation

- **AI cold start**: `24-ai-cold-start.md` + `26-design-closure-review.md` - required entry path and current allowed work
- **Language baseline**: `25-implementation-language-baseline.md` - historical/candidate Phase 1 Python / just / YAML / JSON / Markdown baseline
- **Start here**: `00-index.md` - full file index with Active Core / Deferred Program / Future Blueprint breakdown
- **Layer map**: `20-layered-program-map.md` - separates product scope from current implementation window
- **Tools & costs**: `02-tools-cost.md` - product tool boundary and current-window cost policy
- **Contracts**: `CONTRACTS.md` - machine-readable contract/version governance authority
- **Roles**: `03-ai-roles.md` - product role architecture and current executable kernel roles
- **Three-plane architecture**: `22-three-plane-architecture.md` - boundary guide for orchestration / execution / evidence references
- **menmery integration**: `23-menmery-integration.md` - integration boundary; `menmery` is not the product owner
- **Current closure**: `26-design-closure-review.md` - docs-only reset state, source status, and rewrite prerequisites
- **Rewrite plan**: `REWRITE-PLAN.md` - current draft for the first post-reset executable slice
- **External systems**: `27-external-systems-boundary.md` - checked boundary for `menmery` and `auto_router`
- **Product principles**: `28-product-principles.md` - current North Star and durable design intent
- **Future blueprints**: `12-disaster-recovery.md`, `29-rewrite-blueprint.md`, `30-project-adapter-blueprint.md`, `31-external-model-governance-integration.md` - future-only authority set for recovery, rewrite, adapters, and external gateway integration

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

### Active Core Definition (from 20-layered-program-map.md)
```
Current implementation window:
1. Phase 0: cold start and design recovery
2. Phase 1: first executable kernel
3. Phase 2: Green reliability
4. Phase 3: Yellow preparation

Hard boundary:
- `dev_master` is the independent AI automation pipeline product.
- `menmery` is long-term cognitive infrastructure and the default integration
  for context, truth, canonical evidence, governance preview, audit, approval
  lane, and action levels when available. It is a sibling dependency, not the
  parent product, and it does not mutate repositories.
- `auto_router` is the LLM routing control plane and runtime model execution
  boundary. It owns routing planner/failover/learner behavior; `dev_master`
  must not reimplement that router. It is a sibling dependency, not the product
  owner.
- before non-doc software-change work, prefer `menmery` `entry_turn`; use a
  message shaped like `software_change / dev_master / <target repo> / <goal>`
  with `max_depth="auto"`. Follow its returned recommended call when needed,
  and write results back through `remember(..., related_to=[entry_turn_id])`
  or governed canonical write when available.
- orchestration plane owns durable workflow state, retries, timers, approvals.
- execution plane owns repo mutation, shell, builds, tests, scans.
- evidence plane owns immutable evidence references; when `menmery` is
  available, canonical evidence should map to `menmery` record / inbox / audit
  IDs.
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
- dev_master maps software-change evidence and approvals into menmery entry-turn panoramas, observations, canonical records, audit, and action levels when that integration is available
- **auto_router**: External LLM routing gateway (Go project at `/home/jade/projects/auto_router`)
- dev_master delegates model execution routing, failover, feedback, and low-risk
  routing optimization to auto_router. Any future dev_master model-governance
  work must coordinate with auto_router instead of duplicating its control plane

## Working in This Repo

- Read `24-ai-cold-start.md` and `26-design-closure-review.md` before choosing work
- Read files starting from `00-index.md` for navigation
- Check `20-layered-program-map.md` to confirm if a feature is Active/Deferred/Future
- Check `CONTRACTS.md` before changing machine-readable artifacts, runner facts,
  verifier outputs, or version fields
- Check `23-menmery-integration.md` before deciding where truth/evidence/governance integration belongs
- Check `27-external-systems-boundary.md` before describing or changing
  `menmery` / `auto_router` boundaries
- Treat `27-external-systems-boundary.md` as the sibling-system boundary
  authority if another file summarizes the same topic
- Check `REWRITE-PLAN.md` before proposing or recreating implementation assets
- Check `25-implementation-language-baseline.md` before adding implementation files
- Don't treat design docs as runnable code - they define contracts, not implementations
- There is no active `just` command surface after the implementation reset.
  Use file inspection for docs-only status claims until a rewrite plan restores
  commands.
- When implementing current-window code, base it on `22-three-plane-architecture.md`, `23-menmery-integration.md`, `StateStore` only for local/fallback state, and `gateway_client.py` for LLM gateway calls where such a client exists

## Key Files by Purpose

| Purpose | File |
|---------|------|
| AI cold start | 24-ai-cold-start.md, 26-design-closure-review.md |
| Language baseline | 25-implementation-language-baseline.md |
| Architecture overview | 00-index.md |
| Build phases & gates | 14-master-program.md, 15-phase-gates.md |
| Role definitions | 03-ai-roles.md |
| Risk zones (Red/Yellow/Green) | 07-governance.md |
| Cost model | 02-tools-cost.md |
| State persistence | 06b-state-persistence.md |
| Three-plane boundaries | 22-three-plane-architecture.md |
| menmery integration boundary | 23-menmery-integration.md |
| External system boundaries | 27-external-systems-boundary.md |
| Product principles | 28-product-principles.md |
| Current closure / state pointer | 26-design-closure-review.md |
| Future rewrite blueprint | 29-rewrite-blueprint.md |
| Future adapter blueprint | 30-project-adapter-blueprint.md |
| Future external gateway integration | 31-external-model-governance-integration.md |
| Recovered full-design reference | recovered/AI-autonomous-dev-pipeline-v3.md |

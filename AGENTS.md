# AGENTS.md - dev_master

## What This Is

This is a **design reference documentation** repository, not executable code. The `.md` files define an AI autonomous development pipeline architecture. Code blocks in docs are design references, not implementation.

## Quick Navigation

- **AI cold start**: `24-ai-cold-start.md` + `tasks/current.md` - required entry path and current allowed task
- **Start here**: `00-index.md` - full file index with Active Core / Deferred Program / Future Blueprint breakdown
- **Layer map**: `20-layered-program-map.md` - defines what is currently buildable vs deferred vs future
- **Tools & costs**: `02-tools-cost.md` - defines Active Core tool stack (Claude Code, Codex CLI, auto_router)
- **Roles**: `03-ai-roles.md` - three-role model (Caller/Orchestrator, Execution Worker, Verifier/Governor)
- **Three-plane architecture**: `22-three-plane-architecture.md` - boundary guide for orchestration / execution / evidence references
- **menmery integration**: `23-menmery-integration.md` - primary positioning for dev_master as a `menmery` software_change capability

## Critical Context

### Three-Layer Model
- **Active Core**: Currently buildable. Files in this layer directly constrain AI behavior.
- **Deferred Program**: Direction correct, but not currently built. Only interface definitions exist.
- **Future Blueprint**: Long-term演进蓝图, not in current build program.

### Active Core Definition (from 20-layered-program-map.md)
```
Current build program only covers:
1. Phase 0: 文档定稿与边界冻结
2. Phase 1: 最小执行内核
3. Phase 2: Green reliability
4. Phase 3: Yellow preparation

Hard boundary:
- dev_master is a software-change capability / harness on top of menmery, not a peer truth/governance/evidence runtime
- menmery owns canonical truth, supersede, audit, governance preview, and action level 0-4 when available
- before non-doc software-change work, prefer menmery `get_context(...)` and `act(intent="software_change", ...)`; write results back through `remember(...)` or governed canonical write
- orchestration plane owns durable workflow state, retries, timers, approvals
- execution plane owns repo mutation, shell, builds, tests, scans
- evidence plane maps to menmery canonical records / inbox / audit when available; local evidence stores only runner indexes, digests, and fallback artifacts
- StateStore is runtime index/fallback state, not the canonical truth source and not the full durable orchestration engine
- Temporal default is self-hosted only if long-running wait/retry/resume exceeds menmery facade. Phase 0-1 should not require Temporal productionization.
- Do not put large evidence artifacts inside Temporal history; store immutable evidence in the evidence plane and keep only references in workflow state.
- only three roles are active: Caller/Orchestrator, Execution Worker, Verifier/Governor
- dev_master owns only `runner_contract_version`; schema/governance authority belongs to menmery

NOT allowed as main tasks:
- parallel canonical store / approval controller / governance schema that competes with menmery
- Ops AI 持续巡检
- Advisor AI 主动提案
- TechRadar 周期扫描
- Argo/Tekton production rollout
- Tekton Chains full provenance rollout
- GUAC metadata graph
- rewrite controller
- model governance rollout
- 泛化 adapter 体系
```

### External Dependencies

- **menmery**: User cognitive extension / epistemic runtime (Python project at `/home/jade/projects/menmery`)
- dev_master should use menmery through documented caller protocol / MCP facade, not by importing internal modules
- dev_master maps software-change evidence and approvals into menmery observations, canonical records, audit, and action levels
- **auto_router**: External LLM routing gateway (Go project at `/home/jade/projects/auto_router`)
- dev_master does NOT do model routing, model governance, or classification - that's auto_router's job
- dev_master only: sends requests, reads results, sends feedback

## Working in This Repo

- Read `24-ai-cold-start.md` and `tasks/current.md` before choosing work
- Read files starting from `00-index.md` for navigation
- Check `20-layered-program-map.md` to confirm if a feature is Active/Deferred/Future
- Check `23-menmery-integration.md` before treating dev_master as an independent system
- Don't treat design docs as runnable code - they define contracts, not implementations
- Use `just check` before gate decisions or final repo status claims
- When implementing, base code on `23-menmery-integration.md`, `22-three-plane-architecture.md`, `StateStore` only for local/fallback state, and `gateway_client.py` for LLM gateway calls (not copy from docs)

## Key Files by Purpose

| Purpose | File |
|---------|------|
| AI cold start | 24-ai-cold-start.md, tasks/current.md |
| Architecture overview | 00-index.md |
| Build phases & gates | 14-master-program.md, 15-phase-gates.md |
| Role definitions | 03-ai-roles.md |
| Risk zones (Red/Yellow/Green) | 07-governance.md |
| Cost model | 02-tools-cost.md |
| State persistence | 06b-state-persistence.md |
| Three-plane boundaries | 22-three-plane-architecture.md |
| menmery capability mapping | 23-menmery-integration.md |
| Runner contract reference | contracts/software-change-runner-v1.yaml |
| Task/report templates | templates/ |
| Local gate/drift evidence | reports/ |

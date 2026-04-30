---
status: active
scope: product
authority: this
---

# AI Role Architecture

> **文件性質：實現藍圖（target spec）。** Product scope uses a multi-agent
> pipeline. The current executable kernel design may collapse several roles
> into fewer runtime actors, but that is an implementation tactic, not a
> deletion of product roles. 當前倉庫尚未重建這些 runtime，下表
> "Current planning status" 列描述的是**設計層的位置**，不代表代碼層已運行。

---

## 3.1 Product Roles

| Role | Product responsibility | Current planning status |
|------|------------------------|--------------------------|
| Orchestrator AI | Coordinate the pipeline, plan work, manage gates, collect evidence, trigger human decisions | planned as caller/orchestrator discipline; runtime not yet implemented |
| Spec AI | Turn requirements into technical specs, contracts, acceptance criteria, and constraints | planned, currently absorbed into caller manual pass |
| Critic AI | Challenge specs for gaps, contradictions, edge cases, risk, and confidence | planned, currently absorbed into caller review pass |
| Code AI | Implement approved work inside bounded slices | planned execution worker; runtime not yet implemented |
| Test AI | Generate and run test matrices from specs and contracts | planned, currently absorbed into worker manual pass |
| Security AI | Static and semantic security checks, dependency/PII/red-zone detection | planned, currently absorbed into worker manual pass |
| Verifier / Governor | Compare request, diff, checks, risk facts, evidence, and gate fit | planned current-window verifier; runtime not yet implemented |
| Ops AI | Proactive infrastructure monitoring, capacity signals, safe self-heal, operations proposals | product roadmap, not current runtime |
| Advisor AI | Data-backed technical, architecture, procurement, and budget recommendations | product roadmap, not current runtime |
| TechRadar Scanner | External ecosystem sensing: advisories, dependency health, model/pricing changes | product roadmap, not current runtime |
| Project Adapter | Map concrete project stacks into standard build/test/security/release outputs | product roadmap |
| Model Governance | Pipeline-level model requirements, evaluation evidence, rollout policy, and feedback coordination with `auto_router` | product roadmap |
| Rewrite Controller | Rewrite proposals, wave gates, retirement criteria, knowledge transfer | product roadmap |

Older mined role ideas are tracked in
[durable-ideas-from-v3.md](../90-reference/durable-ideas-from-v3.md), but
current files are authoritative. Current files should not describe the product
as "three roles only".

---

## 3.2 Current Executable Kernel Roles

Phase 1-2 execution should use a smaller runtime shape (planned, not yet
implemented):

| Kernel role | Covers |
|-------------|--------|
| Caller / Orchestrator | bounded request prep, optional service context/governance input, task planning, evidence collection |
| Execution Worker | local diff, checks, scans, runner facts |
| Verifier / Governor | request/evidence/risk/boundary/writeback checks |

This small kernel exists to prove the loop. It does not remove Spec, Critic,
Code, Test, Security, Ops, Advisor, TechRadar, adapters, model governance, or
rewrite control from the product architecture. Model governance must coordinate
with `auto_router`; it must not duplicate `auto_router`'s routing control
plane.

---

## 3.3 Role Activation Rule

Roles may be represented in three ways:

| State | Meaning |
|-------|---------|
| product role | belongs to the target product architecture |
| current-window pass | executed manually or inside another actor for the current phase |
| active runtime role | has its own durable workflow, queue, tools, evidence, and controls |

Moving a product role into active runtime requires gate evidence. Describing a
role as not yet active must not be phrased as "not part of dev_master".

---

## 3.4 Minimum Current Loop

```text
1. Caller / Orchestrator:
   define bounded request
   optionally call sibling service surfaces when the task benefits from them

2. Execution Worker:
   create local or isolated worktree
   apply bounded diff
   run lint/test/security checks
   emit runner facts and artifact digests

3. Verifier / Governor:
   compare request, diff, checks, risk facts
   require durable local evidence
   verify optional external writeback status when such a service was used
   return allow/block/escalate recommendation
```

Legacy `get_context -> act` shorthand in older reference docs should be
interpreted through `docs/30-integrations/27-external-systems-boundary.md` and
`docs/20-current-window/REWRITE-PLAN.md`.

Final approval remains a human/local-gate decision, optionally tightened by any
external governance surface that was actually used.

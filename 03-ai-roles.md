---
status: active
scope: product
authority: this
---

# AI Role Architecture

> Product scope uses a multi-agent pipeline. The current executable kernel may
> collapse several roles into fewer runtime actors, but that is an implementation
> tactic, not a deletion of product roles.

---

## 3.1 Product Roles

| Role | Product responsibility | Current status |
|------|------------------------|----------------|
| Orchestrator AI | Coordinate the pipeline, plan work, manage gates, collect evidence, trigger human decisions | active as caller/orchestrator discipline |
| Spec AI | Turn requirements into technical specs, contracts, acceptance criteria, and constraints | current-window planning pass |
| Critic AI | Challenge specs for gaps, contradictions, edge cases, risk, and confidence | current-window review/self-critique pass |
| Code AI | Implement approved work inside bounded slices | current-window execution worker |
| Test AI | Generate and run test matrices from specs and contracts | current-window test/check pass |
| Security AI | Static and semantic security checks, dependency/PII/red-zone detection | current-window risk facts/check pass |
| Verifier / Governor | Compare request, diff, checks, risk facts, evidence, and gate fit | active current-window verifier |
| Ops AI | Proactive infrastructure monitoring, capacity signals, safe self-heal, operations proposals | product roadmap, not current runtime |
| Advisor AI | Data-backed technical, architecture, procurement, and budget recommendations | product roadmap, not current runtime |
| TechRadar Scanner | External ecosystem sensing: advisories, dependency health, model/pricing changes | product roadmap, not current runtime |
| Project Adapter | Map concrete project stacks into standard build/test/security/release outputs | product roadmap |
| Model Governance | Pipeline-level model requirements, evaluation evidence, rollout policy, and feedback coordination with `auto_router` | product roadmap |
| Rewrite Controller | Rewrite proposals, wave gates, retirement criteria, knowledge transfer | product roadmap |

The recovered v3 source contains older role detail that can still inform this
map, but current files are authoritative. Current files should not describe the
product as "three roles only".

---

## 3.2 Current Executable Kernel Roles

Phase 1-2 execution currently uses a smaller runtime shape:

| Kernel role | Covers |
|-------------|--------|
| Caller / Orchestrator | context retrieval, governance preview, task planning, evidence collection |
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
   entry_turn(message="software_change / dev_master / <target repo> / <goal>", max_depth="auto")
   follow returned recommended_call or governed fallback

2. Execution Worker:
   create local or isolated worktree
   apply bounded diff
   run lint/test/security checks
   emit runner facts and artifact digests

3. Verifier / Governor:
   compare request, diff, checks, risk facts
   require evidence writeback
   return allow/block/escalate recommendation
```

Legacy `get_context -> act` shorthand in older reference docs should be
interpreted through `27-external-systems-boundary.md` and
`REWRITE-PLAN.md`.

Final approval remains a human/governance decision when the gate or action level
requires it.

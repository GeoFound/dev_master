---
status: active
scope: product
authority: ref-only
---

# Roadmap

> This roadmap separates product scope from the current implementation window.
> The product is the full AI automation pipeline; the current window is the
> evidence-gathering kernel now being built.

---

## 9.1 Product Roadmap

The product roadmap is defined by the current modular design documents. The
recovered v3 document is an older reference and may contain useful product
signals, but it is not the authority for current decisions.

1. Repository and governance base
   - boundaries, rules, audit, cost policy, cold start, current state pointer
2. Minimum execution loop
   - requirement/spec/code/test/security/result evidence
3. Critic and Test reliability
   - spec challenge, confidence calibration, test generation, failure routing
4. Security and Result Gate maturity
   - static/semantic scans, dependency/PII/red-zone checks, evidence gates
5. Release safety
   - PR creation, feature flags, canary, monitoring, rollback, RCA
6. Observability and trust evolution
   - dashboard, circuit breaker, health scoring, trust engine, boundary changes
7. Ops AI and TechRadar
   - proactive infrastructure health, safe self-heal, external advisories
8. Advisor AI
   - dependency, architecture, procurement, and budget recommendations
9. Project adapters
   - Web/SaaS, mobile, CLI, library, data-pipeline adapter interfaces
10. Model governance
    - product-level model requirements, evaluation evidence, rollout policy,
      and feedback loops coordinated with `auto_router`
11. Rewrite governance and disaster recovery
    - rewrite proposals, wave gates, retirement gates, knowledge transfer

These are product capabilities. They may be unimplemented today, but they are
not outside the project.

---

## 9.2 Current Implementation Window

The current window remains conservative:

| Phase | Gate | Purpose |
|-------|------|---------|
| Phase 0 | Gate A | cold start, repo base, current state pointer |
| Phase 1 | Gate B | first executable kernel |
| Phase 2 | Gate C | green reliability samples |
| Phase 3 | Gate D | yellow preparation and review payloads |

This is a staging plan, not the total roadmap.

---

## 9.3 Current Phase Details

### Phase 1: First Executable Kernel

Goal:

```text
entry_turn -> bounded plan -> local/isolated worker -> verifier -> evidence writeback
```

Build only:

- runner contract
- local runner facts emitter
- verifier checks
- forced-bad cases
- evidence writeback references

### Phase 2: Green Reliability

Goal:

- run enough green samples to measure current-kernel reliability
- track full-loop success count
- track verifier block rate
- track evidence writeback failures
- track risk misclassifications

### Phase 3: Yellow Preparation

Goal:

- define yellow categories
- design review payloads
- collect examples
- keep human approval mandatory for yellow work

---

## 9.4 Not Yet Runtime

The following are product roadmap capabilities, but not current runtime
implementation tasks until evidence and gate decisions support them:

- active Ops AI daemon
- Advisor AI proactive proposal loop
- TechRadar scheduled scanner
- auto-merge and production deploy
- project adapter runtime
- model governance runtime
- rewrite controller
- Temporal/HA orchestration platform
- DSSE/cosign/Tekton/GUAC provenance rollout

They should be discussed as future product capabilities, not erased from the
project.

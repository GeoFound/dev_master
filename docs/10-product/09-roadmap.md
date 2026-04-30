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

## 9.0 Capability Ladder

Read the roadmap through this autonomy ladder:

| Tier | Product meaning | Automation target |
|------|-----------------|-------------------|
| `L1` | idea to clickable prototype or bounded artifact | full automation after verifier/evidence reliability is proven |
| `L1.5` | 24/7 queued execution, async human review inbox, multi-project operation, cost gates | near-term operating model |
| `L2` | real SaaS/product work with auth, payments, multi-tenancy, production security, release, or business impact | semi-automatic assistance only |
| `L2 full-auto` | production product delivery without human approval | explicitly out of target |
| `L3` | high-compliance, high-integration, or incident-heavy work | AI-assisted, human-owned |

The durable product ambition is not "idea to unattended production SaaS". It is
an always-on `L1` incubation factory plus an `L2` assistant that leaves humans
with the critical product, security, release, budget, and autonomy decisions.

---

## 9.1 Product Roadmap

The product roadmap is defined by the current modular design documents. Older
mined v3 ideas are indexed in
[durable-ideas-from-v3.md](../90-reference/durable-ideas-from-v3.md), but that
index is not authority for current decisions.

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
| Phase 4 | Gate E | repo-local operational validation of the completed kernel |
| Post-Phase 4 | Gate F | activate the first local provider adapter kernel slice |
| Phase 5 | Gate G | local provider adapter kernel and generated evidence review |
| Post-Phase 5 | Gate H | activate the first localhost-only devmasterd kernel |
| Phase 6 | Gate I | local devmasterd kernel and API smoke review |
| Phase 7 | Gate J | repeated devmasterd operational validation before UI or real provider work |

This is a staging plan, not the total roadmap.

---

## 9.3 Current Phase Details

### Phase 1: First Executable Kernel

Goal:

```text
bounded plan -> local/isolated worker -> verifier -> local evidence -> optional service writeback
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
- track local evidence integrity failures
- track optional service writeback failures
- track risk misclassifications

### Phase 3: Yellow Preparation

Goal:

- define yellow categories
- design review payloads
- collect examples
- keep human approval mandatory for yellow work

### Phase 4: Operational Validation

Goal:

- use the current kernel instead of stopping at green tests
- run the local prototype through a live localhost surface
- collect repeatable operational observations about evidence integrity,
  provider drift, green reliability, gate state, and prototype reachability
- decide from Gate E whether the next runtime slice may start

### Post-Phase 4: Provider Adapter Activation

Goal:

- convert the provider adapter product requirement into a gated implementation
  slice
- keep the first provider adapter local/API-compatible and stub-backed
- preserve raw+parsed provider evidence, parser versioning, drift detection,
  and cost facts before real providers are attached

### Phase 5: Provider Adapter Kernel

Goal:

- implement the first local provider adapter kernel
- prove ok and forced-drift provider evidence paths
- keep real paid providers and subscription CLI workers out of scope
- review generated provider evidence through Gate G before moving on

### Post-Phase 5: devmasterd Activation

Goal:

- convert the local control-plane requirement into a gated implementation slice
- require localhost bearer token auth from the first daemon slice
- keep Web Console, IDE extension, real providers, and external repo mutation
  out of scope

### Phase 6: devmasterd Local Kernel

Goal:

- implement the first localhost-only daemon kernel
- prove `intake -> authorize -> run-provider -> evidence` through real local
  HTTP calls
- persist local state/evidence under `runtime/devmasterd/`
- review generated state/evidence through Gate I before adding UI or real
  providers

### Phase 7: devmasterd Operational Validation

Goal:

- repeatedly use the daemon through localhost API smoke runs
- collect success/failure counts for auth, intake, authorization, provider
  fixture execution, and evidence
- defer Web Console, IDE extension, and real provider integrations until the
  daemon proves stable under repeated local use

### Post-Phase 7: CLI Control Surface Activation

Goal:

- convert the first product surface into a gated implementation slice
- keep CLI as a thin `devmasterd` client, not a second control plane
- limit the CLI to status, evidence, intake, and localhost smoke commands
- keep Web Console, IDE extension, real providers, external repos, deploys, and
  PR creation out of scope

### Phase 8: CLI Control Surface

Goal:

- implement the first CLI client against the existing localhost daemon API
- prove CLI use through a real localhost daemon smoke run
- write CLI validation evidence before any Web Console or IDE extension work
- preserve `devmasterd` as the only owner of authorization, queue, state,
  provider execution, and evidence policy

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
- fully autonomous `L2` or `L3` product delivery
- autonomous product, pricing, market, security, or release judgment

They should be discussed as future product capabilities, not erased from the
project.

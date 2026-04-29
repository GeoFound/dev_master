---
status: active
scope: window
authority: this
---

# Design Closure Review

> Current state pointer for the post-reset documentation repository.
> Implementation scaffolding was intentionally removed on 2026-04-27. This file
> closes the remaining documentation loop and records what still needs to be
> strengthened before a rewrite starts.

---

## 26.1 Source Status

Available sources:

| Source | Status | How to use it |
|--------|--------|---------------|
| root `*.md` files | current modular documentation set | active design/system specification |
| `recovered/AI-autonomous-dev-pipeline-v3.md` | outdated recovered historical design | stale reference only; mine for durable ideas, do not treat as authority |
| git history | incomplete for the user's final design intent | do not treat as full recovery source |

The recovered v3 document is valuable only where it preserves broad product
signals: independent AI automation pipeline, proactive operations/advisory
capabilities, result gates, cost awareness, project adaptation, and long-term
recovery/rewrite governance. It is stale and must not override the current
modular docs, `menmery` / `auto_router` integration boundaries, or later human
direction.

---

## 26.2 Closed Decisions

These points are now closed across the current docs:

1. `dev_master` is an independent AI automation pipeline product.
2. `menmery` is long-term cognitive infrastructure and the integration for
   context, canonical evidence, audit, governance preview, approval lane, and
   action levels. It is not the parent product and it does not mutate repos.
3. `auto_router` is the LLM routing control plane and runtime model execution
   boundary. It owns routing planner, failover, feedback, learner reports, and
   guarded low-risk routing optimization. It is not the product owner.
4. The current implementation window is not the product ceiling.
5. Product roles are broader than the current three-actor executable kernel.
6. Ops AI, Advisor AI, TechRadar, adapters, model governance, rewrite
   governance, release safety, and recovery remain product-scope capabilities.
7. The repository is currently docs-only. Deleted implementation evidence is no
   longer an active Gate B basis.

---

## 26.3 Current Product Shape

The product loop remains:

```text
requirement intake
-> specification
-> critique
-> plan
-> implementation
-> tests
-> security
-> result gate
-> PR / release
-> canary / rollback
-> operations feedback
-> advisory / external sensing
-> recovery / improvement
```

The role model remains multi-agent:

```text
Orchestrator
Spec
Critic
Code
Test
Security
Verifier / Governor
Ops
Advisor
TechRadar
Project Adapter
Model Governance
Rewrite Controller
```

The current rewrite, when approved, may start with fewer runtime actors, but
that is only an implementation tactic.

---

## 26.4 Stale Reference Mining

Ideas from the stale recovered design that are still worth preserving:

- full independent product identity
- proactive sensing as product scope, not erased scope
- Result Gate and evidence-based approval
- human boundary for yellow/red/high-impact work
- cost awareness and model routing through an external gateway
- project adaptation and self-test direction
- disaster recovery, rewrite governance, and knowledge transfer direction

Current modular docs still need strengthening in these areas:

- current docs have less concrete operational detail for Ops AI and TechRadar
  activation criteria
- Advisor AI is preserved, but its acceptance/rejection learning loop needs a
  future active contract
- model governance is named as product scope, but still needs a dedicated spec
  that coordinates with `auto_router` rather than duplicating it
- rewrite governance is mostly inside disaster-recovery material and should be
  split before implementation
- current docs do not yet contain a fresh end-to-end implementation blueprint
  after the reset
- Gate B evidence from the deleted implementation cannot be reused as active
  executable proof

---

## 26.5 Strengthening Needed Before Rewrite

The current draft rewrite artifact is [REWRITE-PLAN.md](REWRITE-PLAN.md). This
repository should keep one active rewrite-plan draft at a time instead of
splitting rewrite intent across multiple planning files.

Before rebuilding implementation, create a rewrite plan that answers:

1. Which product slice is the first real executable slice?
2. Which roles are collapsed into the first runtime actor, and which remain
   explicit passes?
3. What runner facts contract is reintroduced?
4. What verifier facts must block worker self-reporting errors?
5. What evidence writeback path is required when `menmery` is available?
6. What local fallback evidence is allowed when `menmery` is unavailable?
7. Which Gate B evidence must be regenerated from scratch after the reset?
8. Which product-scope capabilities are explicitly not active in the first
   rewrite slice?

The rewrite plan should be a markdown design artifact first. Implementation
files should only be recreated after the human approves that plan.

---

## 26.6 Next Allowed Action

Current allowed work:

- improve design/system documentation
- prepare and refine [REWRITE-PLAN.md](REWRITE-PLAN.md)
- mine the stale recovered design for durable ideas, then reconcile them with
  current modular docs and integration boundaries
- mark gaps, conflicts, and activation prerequisites

Not allowed without a new human decision:

- recreate runner, verifier, scripts, tests, contracts, reports, or task
  directories as implementation assets outside a human-approved rewrite plan
- claim Gate B is still promoted based on deleted files
- narrow `dev_master` into a `menmery` harness
- collapse product roles into three roles as the final architecture

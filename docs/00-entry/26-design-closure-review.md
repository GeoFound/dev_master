---
status: active
scope: window
authority: this
---

# Design Closure Review

> Current state pointer for the post-reset blueprint repository.
> Implementation scaffolding was intentionally removed on 2026-04-27. This file
> records the rebuild baseline, the invalid stale paths, and what still needs
> to be strengthened before or during reconstruction. It must not be read as a
> claim that the repository exists only to maintain documents.

---

## 26.1 Source Status

Available sources:

| Source | Status | How to use it |
|--------|--------|---------------|
| root entry docs + `docs/*.md` | current modular documentation set | active design/system specification |
| `docs/90-reference/durable-ideas-from-v3.md` | short v3 durable-idea index | reference only; points old ideas to current authority docs |
| `runtime/*.json` + `runtime/session-log.jsonl` | current machine-readable progression state | active task/gate continuity layer compiled from the blueprint |
| git history | incomplete for the user's final design intent | do not treat as full recovery source |

The recovered v3 source has been removed from active docs. Durable ideas that
were mined from it are tracked only as a short idea-to-destination index. If new
historical mining is needed, use git history or archived evidence rather than
restoring the full source as a cold-start dependency.

---

## 26.2 Closed Decisions

These points are now closed across the current docs:

1. `dev_master` is an independent AI automation pipeline product.
2. `menmery` is long-term cognitive infrastructure and an optional sibling
   service for context, durable memory, audit, governance preview, and
   evidence sinks. It is not the parent product and it does not mutate repos.
3. `auto_router` is the LLM routing control plane and runtime model execution
   boundary. It is an optional sibling service, not the product owner.
4. The current implementation window is not the product ceiling.
5. Product roles are broader than the current three-actor executable kernel.
6. Ops AI, Advisor AI, TechRadar, adapters, model governance, rewrite
   governance, release safety, and recovery remain product-scope capabilities.
7. The deleted pre-reset implementation is gone. Deleted implementation
   evidence is no longer an active Gate B basis, and replacement slices must be
   rebuilt from the current blueprint.
8. The current strategic target is a 24/7 `L1` product incubation factory plus
   an `L2` semi-automatic product assistant. It is not fully unattended `L2+`
   production SaaS delivery.
9. Long-running AI work requires external anchors: bounded slices, tests,
   verifier decisions, durable evidence, truth-store context when useful, and
   human gates for high-impact decisions.
10. Autonomy must evolve through append-only ratchet records, with automatic
    demotion and hard red lines that do not relax as model capability improves.
11. The first L1 factory proof is Phase 1B local prototype output, not external
    repo mutation or deploy.
12. `dev_master` is the scheduling/governance/evidence control plane. Codex,
    Claude Code, API models, `auto_router`, and future agent systems are
    worker providers or integrations, not queue/approval/evidence owners.
13. Phase 1-4 core implementation uses Python, JSON Schema/JSON/JSONL
    contracts, and Markdown reports. TypeScript is reserved for Web Console
    and IDE surfaces after the core loop exists.

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

See [durable-ideas-from-v3.md](../90-reference/durable-ideas-from-v3.md) for the
short mapped index. Do not reintroduce the full recovered v3 document into cold
start or active registry.

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
- product docs must preserve the distinction between `L1` / `L1.5`
  automation, `L2` semi-automatic assistance, and out-of-target full `L2+`
  autonomy

---

## 26.5 Strengthening Needed Before Rewrite

The current draft rewrite artifact is [REWRITE-PLAN.md](../20-current-window/REWRITE-PLAN.md). This
repository should keep one active rewrite-plan draft at a time instead of
splitting rewrite intent across multiple planning files.

Before rebuilding implementation, create a rewrite plan that answers:

1. Which product slice is the first real executable slice?
2. Which roles are collapsed into the first runtime actor, and which remain
   explicit passes?
3. What runner facts contract is reintroduced?
4. What verifier facts must block worker self-reporting errors?
5. What optional service writeback path should be preferred when `menmery` is available?
6. What local fallback evidence is allowed when `menmery` is unavailable?
7. Which Gate B evidence must be regenerated from scratch after the reset?
8. Which product-scope capabilities are explicitly not active in the first
   rewrite slice?

The rewrite plan should exist as a markdown design artifact first, but once the
human approves a bounded slice it should drive reconstruction rather than
indefinite documentation expansion. Implementation files must be recreated from
the current blueprint, not copied forward by path or implication.

---

## 26.6 Next Allowed Action

Current allowed work:

- use `runtime/current-task.json` and `runtime/program-state.json` as the
  default machine-readable continuation point
- derive the next bounded build-task from
  [REWRITE-PLAN.md](../20-current-window/REWRITE-PLAN.md),
  [14-master-program.md](../20-current-window/14-master-program.md),
  [15-phase-gates.md](../20-current-window/15-phase-gates.md),
  [17-task-templates.md](../20-current-window/17-task-templates.md), and
  [18-master-execution-task.md](../20-current-window/18-master-execution-task.md)
- implement current-gate slices that are justified by the active blueprint and
  produce fresh evidence
- improve design/system documentation only when ambiguity or drift is blocking
  implementation
- prepare and refine [REWRITE-PLAN.md](../20-current-window/REWRITE-PLAN.md) when the active build
  slice is still underspecified
- mine the stale recovered design for durable ideas, then reconcile them with
  current modular docs and integration boundaries
- mark gaps, conflicts, and activation prerequisites
- keep the task graph / program state / completion records aligned with the
  active blueprint when implementation changes the current slice

Not allowed without a new human decision:

- revive deleted runner, verifier, scripts, tests, contracts, reports, or task
  directories by path or implication only, outside a human-approved rewrite
  slice
- claim Gate B is still promoted based on deleted files
- substitute endless documentation maintenance for implementation once the
  current blueprint already defines the next bounded build slice
- skip task/gate/evidence discipline when rebuilding implementation
- narrow `dev_master` into a `menmery` harness
- make sibling service consumption look like a mandatory runtime prerequisite
- collapse product roles into three roles as the final architecture

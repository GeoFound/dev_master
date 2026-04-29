---
status: active
scope: window
authority: this
---

# Master Program

> The product roadmap is the full AI automation pipeline. The current execution
> program advances through Phase 0-3 until a human gate activates a broader
> runtime slice.

---

## 14.1 Current Phase Graph

```text
Phase 0 Design Freeze
  -> Gate A

Phase 1 First Executable Kernel
  -> Gate B

Phase 2 Green Reliability
  -> Gate C

Phase 3 Yellow Preparation
  -> Gate D
```

No later runtime gate is active in the current implementation window. This is a
control boundary, not a deletion of later product capabilities.

---

## 14.2 Product Program

The full product program includes:

- requirements intake and specification
- critique, confidence, and risk challenge
- code, tests, security, result gate, and evidence
- PR, release, canary, rollback, and RCA
- observability and trust evolution
- Ops AI, TechRadar, and Advisor signals
- project adapters, model governance, rewrite governance, and recovery

Those capabilities remain in product scope. They become runtime work only
through activation proposals and gate decisions.

---

## 14.3 Phase 0

Must freeze:

- product scope vs current implementation window
- `menmery` integration boundary
- `auto_router` routing-control-plane boundary
- checked external system boundaries from `27-external-systems-boundary.md`
- current executable kernel roles
- runner contract v1
- repository AI cold-start entry path
- Phase 1 implementation language baseline
- no parallel canonical/governance store
- archived/deferred docs are non-active runtime, not outside the product

---

## 14.4 Phase 1

Must prove:

```text
menmery entry_turn
-> follow recommended_call / governance preview
-> isolated worker
-> verifier
-> remember evidence related_to=[entry_turn_id]
```

Must not:

- create independent approval controller
- make execution worker approve itself
- use runner logs as final evidence
- duplicate `auto_router` routing / failover / learner publishing
- build active Ops/Advisor/TechRadar runtime
- deploy Temporal production cluster

---

## 14.5 Phase 2

Must collect green reliability evidence:

- docs/test-only tasks
- verifier decisions
- risk classification misses
- evidence writeback failures

---

## 14.6 Phase 3

Must prepare yellow expansion without enabling it:

- define yellow categories
- design review payloads
- collect examples
- keep human approval for all yellow actions

---

## 14.7 Stop Rule

If a task requires a capability outside Phase 0-3, create an activation proposal. Do not implement it as a build-task.

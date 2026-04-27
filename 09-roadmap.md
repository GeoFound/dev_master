# Roadmap: Phase 0-3 Only

> This roadmap intentionally stops at Phase 3. Future sensing, rewrite, adapters, and model governance live in archive/deferred until real evidence justifies activation.

---

## Phase 0: Design Freeze

Goal:

- freeze `menmery` integration boundary
- freeze three-role model
- freeze runner contract v1
- freeze Gate A-D

Exit evidence:

- [23-menmery-integration.md](23-menmery-integration.md) aligns with `menmery` software_change support
- no active doc requires Ops/Advisor/TechRadar
- no active doc requires parallel canonical/governance store

---

## Phase 1: First Executable Kernel

Goal:

```text
get_context -> act(software_change) -> isolated worker -> verifier -> remember evidence
```

Build only:

- minimal runner contract
- local isolated worktree runner
- runner facts emitter
- verifier check
- evidence writeback checklist

Do not build:

- Temporal production deployment
- OPA as highest policy authority
- auto-merge
- active sensing
- generic adapter framework

---

## Phase 2: Green Reliability

Goal:

- run enough docs/test-only tasks to measure reliability
- prove verifier catches obvious scope/risk/evidence failures
- decide whether any green task can proceed with lower human friction

Required metrics:

- full-loop success count
- verifier block rate
- evidence writeback failure count
- risk misclassification count

---

## Phase 3: Yellow Preparation

Goal:

- define yellow candidates
- collect examples
- design human-review payloads

No yellow auto-approval in Phase 3. It is preparation, not expansion.

---

## Activation Later

Anything beyond Phase 3 requires an activation proposal with evidence:

- Ops / Advisor / TechRadar
- rewrite governance
- model governance
- generalized adapters
- Temporal HA/Kubernetes
- DSSE/cosign/Tekton/GUAC rollout

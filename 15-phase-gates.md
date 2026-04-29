---
status: active
scope: window
authority: this
---

# Phase Gates

---

## Gate A: Design Freeze

Pass conditions:

- `dev_master` is explicitly an independent AI automation pipeline product
- `menmery` and `auto_router` are integrations, not product owners
- active docs match `27-external-systems-boundary.md`
- product scope is preserved while current runtime activation is bounded
- current executable kernel roles are explicit
- current phase graph stops at Phase 3
- runner contract has one local version field
- AI cold-start path exists and points to the current docs-only state and
  rewrite prerequisites
- Phase 1 implementation language baseline is explicit
- active docs do not silently activate Ops/Advisor/TechRadar or rewrite/model governance as current runtime tasks

Fail if any active doc implies a parallel truth/governance/evidence runtime.
Fail if any active doc implies a parallel LLM routing control plane competing
with `auto_router`.
Fail if any active doc collapses product scope into the current executable kernel.
Fail if a new AI must infer the current state from free-form architecture docs.

---

## Gate B: First Executable Kernel

Pass conditions:

- at least one low-risk task completes:
  `entry_turn -> bounded plan -> isolated worker -> verifier -> remember`
- runner facts include diff digest and checks
- verifier catches at least one forced bad case
- evidence writeback is visible in `menmery`

Fail if runner logs are the only evidence.
Fail if evidence refers only to implementation files deleted during the
2026-04-27 reset.

---

## Gate C: Green Reliability

Pass conditions:

- enough green samples exist to judge reliability
- risk misclassification is zero for the sample window
- verifier produces actionable block/escalate reasons
- evidence writeback failures are understood

Fail if green includes dependencies, infra, secrets, permissions, deploy, merge, or migrations.

---

## Gate D: Yellow Preparation

Pass conditions:

- yellow categories are defined
- review payload template exists
- human approval remains mandatory
- no yellow auto-approval is enabled

Fail if Phase 3 silently expands autonomy.

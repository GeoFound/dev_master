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
- active docs match `docs/30-integrations/27-external-systems-boundary.md`
- product architecture decision freezes `dev_master` as control plane and
  Codex / Claude / API systems as provider workers
- product scope is preserved while current runtime activation is bounded
- current executable kernel roles are explicit
- current phase graph does not silently activate broader runtime work after
  yellow preparation; Phase 4 is limited to repo-local operational validation
- task proposal contract exists so AI-proposed slices require `dev_master`
  authorization before dispatch
- runner contract has one local version field
- AI cold-start path exists and points to the current rebuild baseline and
  rewrite prerequisites
- Phase 1 implementation language baseline is explicit
- active docs do not silently activate Ops/Advisor/TechRadar or rewrite/model governance as current runtime tasks
- active docs distinguish `L1` / `L1.5` automation from `L2` semi-automatic
  assistance and out-of-target fully unattended `L2+` autonomy
- autonomy ratchet, async review inbox, and current-window cost ceilings are
  defined as active contracts
- engineering execution boundaries distinguish hard red lines,
  mature-library-only areas, ratchetable guardrails, and quality floors

Fail if any active doc implies a parallel truth/governance/evidence runtime.
Fail if any active doc implies a parallel LLM routing control plane competing
with `auto_router`.
Fail if any active doc collapses product scope into the current executable kernel.
Fail if any active doc implies fully unattended `L2` or `L3` product delivery
without a new human autonomy-expansion decision.
Fail if a new AI must infer the current state from free-form architecture docs.

---

## Gate B: First Executable Kernel

Pass conditions:

- Phase 1A: at least one low-risk task completes:
  `bounded request -> isolated worker -> verifier -> local evidence`
- runner facts include diff digest and checks
- runner facts include `ratchet_metrics_contribution`, or explicitly record
  `null` metric contribution with a reason
- verifier catches at least one forced bad case
- evidence is preserved through local append-only records, and any optional
  external writeback is either complete or explicitly pending
- Phase 1B: at least one local L1 prototype artifact completes through the same
  governed loop
- the local prototype is runnable by a human and produces visible local output;
  markdown, JSON, screenshots, and mock reports do not count
- Phase 1B uses the CLI-only product surface
- Phase 1B exercises at least one API-backed or API-compatible worker provider
  path; subscription-tied CLI/SDK providers are optional and cannot be the only
  path
- cost facts are present and respect [cost-ceilings.md](cost-ceilings.md)

Fail if runner logs are the only evidence.
Fail if evidence refers only to implementation files deleted during the
2026-04-27 reset.
Fail if Phase 1B uses external repo mutation, deploy, PR, merge, external paid
deployment/product-service side effect, or production side effect. A budgeted
API worker call is allowed only when recorded in cost facts and kept under the
current-window ceiling.
Fail if subscription-tied provider output is accepted without raw-output
snapshot, adapter version, parse schema version, and drift status.

---

## Gate C: Green Reliability

Pass conditions:

- enough green samples exist to judge reliability
- risk misclassification is zero for the sample window
- semantic verifier exists and has been benchmarked against a labeled fixture
  set of at least 20 forced-ok / forced-bad cases; critical false-allow count
  is zero and total risk misclassification rate is `< 5%`
- verifier produces actionable block/escalate reasons
- local evidence integrity failures and optional service writeback failures are
  understood

Fail if green includes dependencies, infra, secrets, permissions, deploy, merge, or migrations.

---

## Gate D: Yellow Preparation

Pass conditions:

- yellow categories are defined
- review payload template exists
- human approval remains mandatory
- no yellow auto-approval is enabled

Fail if Phase 3 silently expands autonomy.

---

## Gate E: Operational Validation

Pass conditions:

- a machine-readable operational validation report exists
- the report includes at least three validation iterations
- each iteration exercises the local L1 prototype through a live localhost HTTP
  surface
- provider drift count is zero
- local evidence integrity failures are zero
- green reliability artifacts still pass their recorded thresholds
- Gate A-D state is still pass
- validation records no external repo mutation, deploy, PR, merge, paid
  provider call, live service writeback, or production side effect

Fail if Phase 4 validates only by static file inspection or unit tests.
Fail if provider drift is detected.
Fail if the validation report is used to authorize yellow auto-approval,
external repo mutation, or production operation.

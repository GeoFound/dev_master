---
status: active
scope: window
authority: this
---

# Master Program

> The product roadmap is the full AI automation pipeline. The current execution
> program advances through Phase 0-3 until a human gate activates a broader
> runtime slice.
>
> Phase 0-3 is aimed at the `L1` / `L1.5` operating model: bounded work,
> verifier evidence, reliable queued execution, and human review boundaries. It
> does not authorize fully unattended `L2+` product delivery.

---

## 14.1 Current Phase Graph

```text
Phase 0 Design Freeze
  -> Gate A

Phase 1 First Executable Kernel
  -> Phase 1A Runner / verifier / evidence skeleton
  -> Phase 1B Local L1 prototype proof
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

The product program should be calibrated as:

- `L1`: automate prototype and bounded artifact production.
- `L1.5`: automate always-on queued execution with evidence, cost gates, and an
  async human review inbox.
- `L2`: assist real product/SaaS work with PRs, verification, risk labeling,
  and recommendations; keep critical decisions human-governed.
- `L2 full-auto` / `L3 full-auto`: not a current target.

Autonomy should evolve through [autonomy-ratchet.md](autonomy-ratchet.md), not
by silently editing goals after a stronger model appears.

---

## 14.3 Phase 0

Must freeze:

- product scope vs current implementation window
- product architecture decision and default runtime surface sequence
- `menmery` integration boundary
- `auto_router` routing-control-plane boundary
- checked external system boundaries from `docs/30-integrations/27-external-systems-boundary.md`
- current executable kernel roles
- runner contract v1
- repository AI cold-start entry path
- Phase 1 implementation language baseline
- task proposal and authorization contract
- no parallel canonical/governance store
- archived/deferred docs are non-active runtime, not outside the product

---

## 14.4 Phase 1

### Phase 1A: Contract Skeleton

Must prove the governed software-change kernel:

```text
bounded request
-> optional service context / governance preview
-> isolated worker
-> verifier
-> local evidence
-> optional service writeback / feedback
```

This slice is allowed to stay repo-local and docs/test/scaffold focused. It
must prove runner facts, verifier blocking, and append-only evidence before
prototype work expands.

Runner facts must include a `ratchet_metrics_contribution` subset for every run
or explicitly record that the run contributes `null` metrics with a reason. The
runner emits per-run facts; verifier validates them; later ratchet evaluation
aggregates verified windows.

### Phase 1B: Local L1 Prototype Proof

Must prove one local prototype artifact through the same governed loop.

Minimum acceptable prototype:

- controlled through the CLI-only Phase 1B surface
- runnable locally by a human using a documented command such as
  `streamlit run app.py` or `npm run dev`
- produces visible output on localhost or an equivalent local UI surface
- authorized through the task proposal / dev_master decision handoff in
  [task-proposal-contract.md](../10-product/task-proposal-contract.md)
- exercises at least one API-backed or API-compatible worker provider path;
  subscription-tied CLI/SDK providers cannot be the only worker path
- emits runner facts, verifier decision, cost facts, and evidence refs
- remains local; no external repo mutation, deploy, PR, merge, or paid product
  service side effect. Any budgeted API worker call must be recorded in cost
  facts and respect [cost-ceilings.md](cost-ceilings.md)

Markdown, JSON, screenshots, static mock reports, or design-only artifacts do
not satisfy Phase 1B.

Must not:

- create independent approval controller
- make execution worker approve itself
- use runner logs as final evidence
- duplicate `auto_router` routing / failover / learner publishing
- build active Ops/Advisor/TechRadar runtime
- deploy Temporal production cluster
- deploy to external hosting

---

## 14.5 Phase 2

Must collect green reliability evidence and prepare the first external-target
sandbox only after Gate B:

- docs/test-only and local prototype tasks
- Web Console MVP design and implementation may start with queue, inbox, and
  cost dashboard only
- verifier decisions
- risk classification misses
- local evidence integrity failures
- optional service writeback failures
- semantic verifier benchmark results
- external target repo sandbox plan with no production side effects

---

## 14.6 Phase 3

Must prepare yellow expansion without enabling it:

- define yellow categories
- design review payloads
- design deploy-preview payloads for preview-only environments, with no
  production deploy or promotion authority
- integrate async review payloads with [human-review-inbox.md](human-review-inbox.md)
- prepare the full Web Console and IDE extension only after the daemon API
  contract has either been frozen for at least 14 days with no breaking schema
  changes or gained an explicit deprecation/versioning policy
- collect examples
- keep human approval for all yellow actions
- keep the async review inbox as the default queueing model

---

## 14.7 Surface Sequencing

Product surfaces must be sequenced as follows:

1. Phase 1B: CLI-only surface for the first local L1 prototype proof.
2. Phase 2: Web Console MVP with queue, inbox, and cost dashboard. Do not build
   rich diff viewer or IDE extension yet.
3. Phase 3: Full Web Console plus VSCode/Cursor/Windsurf thin extension after
   the daemon API contract has been frozen for at least 14 days with no
   breaking schema changes, or after an explicit deprecation/versioning policy
   has been added to the daemon API contract.

The IDE extension is a protocol client, not a control plane. It must route
governed work through `devmasterd` and must not bypass the task proposal,
provider adapter, verifier, evidence, cost, or human-review contracts.

## 14.8 Stop Rule

If a task requires a capability outside Phase 0-3, create an activation proposal. Do not implement it as a build-task.

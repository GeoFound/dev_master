---
status: active
scope: window
authority: this
---

# Master Program

> The product roadmap is the full AI automation pipeline. The current execution
> program advances through Phase 0-4 before any broader runtime slice is
> activated.
>
> Phase 0-4 is aimed at the `L1` / `L1.5` operating model: bounded work,
> verifier evidence, reliable queued execution, and human review boundaries. It
> does not authorize fully unattended `L2+` product delivery.
>
> Phase 4 is an operational validation window: use the kernel that was built,
> run it locally, collect repeatable data, and decide from evidence whether the
> next runtime slice is ready.

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

Phase 4 Operational Validation
  -> Gate E

Post-Phase 4 Activation
  -> provider adapter kernel activation proposal
  -> Gate F
  -> Phase 5 first local provider adapter kernel only if Gate F passes
  -> Gate G

Post-Phase 5 Activation
  -> devmasterd local control-plane activation proposal
  -> Gate H
  -> Phase 6 first localhost-only devmasterd kernel if Gate H passes
  -> Gate I

Phase 7 devmasterd Operational Validation
  -> repeat localhost daemon smoke runs before UI or real provider activation
  -> Gate J
```

No broader runtime slice is active in the current implementation window. Phase
4 validates what already exists. Post-Phase 4 activation proposals may unlock
the next narrow local slice only through an explicit gate. They do not
authorize external repo mutation, paid provider use, deploy previews, PR
creation, or production side effects.

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

## 14.7 Phase 4

Must operationally validate the completed local kernel before provider adapter,
daemon, Web Console, IDE extension, or external-target work begins:

- run the current repo-local kernel through a repeatable validation command
- exercise the Phase 1B local prototype through a live localhost HTTP surface,
  not only static file checks
- re-read runner, verifier, provider, cost, reliability, and evidence artifacts
- collect at least three validation iterations in a machine-readable report
- record provider drift count, evidence integrity failures, green reliability
  status, gate state, and live prototype reachability
- keep all validation local: no external repo mutation, deploy, PR, merge,
  paid provider call, live `menmery` writeback, or production side effect

Gate E decides only whether the current local kernel is operationally stable
enough to start the next narrow runtime slice. A Gate E pass is not permission
for yellow auto-approval, external repo mutation, or production operation.

---

## 14.8 Post-Phase 4 Activation

The first allowed post-Phase 4 activation candidate is the provider adapter
kernel. It must follow this sequence:

```text
activation proposal
-> Gate F provider adapter activation review
-> local/API-compatible provider adapter kernel implementation
```

The first implementation slice may use only local or API-compatible stub
provider evidence. Real paid provider calls, subscription-tied CLI worker
daemonization, external repo mutation, deploy previews, PR creation, and
production side effects remain out of scope until a later explicit activation
decision.

---

## 14.9 Phase 5

Must implement and use the first local provider adapter kernel:

- consume local/API-compatible provider fixtures only
- store raw output before parsing
- emit raw output ref, digest, size, storage class, parsed output, parser
  schema version, adapter version, drift status, and cost facts
- include at least one forced-drift fixture
- keep real paid providers, subscription-tied CLI workers, live `auto_router`,
  external repo mutation, deploy, PR, and production side effects out of scope

Gate G verifies the provider adapter kernel using its generated evidence, not
only unit tests.

---

## 14.10 Post-Phase 5 Activation

The first allowed post-Phase 5 activation candidate is the local `devmasterd`
control-plane kernel. It must follow this sequence:

```text
activation proposal
-> Gate H devmasterd activation review
-> localhost-only devmasterd kernel implementation
-> Gate I devmasterd evidence review
```

The first implementation slice may expose only localhost HTTP APIs with bearer
token auth. It may persist local queue, state, and evidence artifacts under
`runtime/devmasterd/` and may call only local provider adapter fixtures. Web
Console, IDE extension, real paid provider calls, subscription CLI
daemonization, external repo mutation, deploy, PR creation, and production
side effects remain out of scope.

---

## 14.11 Phase 6

Must implement and use the first local `devmasterd` kernel:

- require bearer token auth on localhost API endpoints
- support local intake, authorization, provider adapter execution, state read,
  and evidence read APIs
- persist repo-local state and daemon evidence
- run provider adapter through local fixtures only
- keep Web Console, IDE extension, real providers, external repos, deploy, PR,
  and production side effects out of scope

Gate I verifies the daemon through real localhost API calls and generated
state/evidence, not only unit tests.

---

## 14.12 Phase 7

Must operationally validate the localhost-only `devmasterd` kernel before any
UI surface or real provider integration begins:

- run repeated daemon smoke iterations
- verify unauthorized requests return 401 every time
- verify `intake -> authorize -> run-provider -> evidence` succeeds every time
- record state/evidence integrity observations
- keep Web Console, IDE extension, real providers, external repos, deploy, PR,
  and production side effects out of scope

Gate J verifies repeated operational validation evidence before any UI or real
provider activation proposal.

---

## 14.13 Surface Sequencing

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

---

## 14.14 Post-Phase 7 Activation

The first allowed post-Phase 7 activation candidate is the CLI control surface.
It must follow this sequence:

```text
activation proposal
-> Gate K CLI activation review
-> localhost-only CLI client implementation
-> Gate L CLI evidence review
```

The CLI must be a thin `devmasterd` API consumer. It may support status,
evidence, intake, and smoke commands against localhost `devmasterd` with bearer
token auth. It must not own queue state, authorization policy, ratchet checks,
cost checks, provider execution policy, or evidence policy.

Web Console, IDE extension, parallel orchestration, real paid provider calls,
subscription CLI daemonization, live `auto_router`, external repo mutation,
deploy preview, PR creation, and production side effects remain out of scope.

---

## 14.15 Phase 8

Must implement and use the first local CLI control surface:

- read daemon URL and bearer token from environment or explicit test-only
  smoke arguments
- call the existing `devmasterd` HTTP APIs instead of writing runtime state
  directly
- support local status and evidence readback commands
- support intake of a local task proposal JSON
- include a smoke command that exercises
  `intake -> authorize -> run-provider -> evidence` against localhost
  `devmasterd`
- write a CLI validation artifact under `runtime/cli-validation/`
- keep Web Console, IDE extension, real providers, external repos, deploy, PR,
  and production side effects out of scope

Gate L verifies the CLI through a real localhost daemon and generated CLI
validation evidence, not only unit tests.

---

## 14.16 Post-Phase 8 Activation

The first allowed post-Phase 8 activation candidate is the local L1 prototype
pipeline. It must follow this sequence:

```text
activation proposal
-> Gate M L1 prototype pipeline activation review
-> local idea-to-runnable-prototype implementation
-> Gate N L1 prototype evidence review
```

The first L1 implementation must use a deterministic local builder. It may
consume a local idea JSON, generate a local prototype artifact, start a
localhost validation surface, and write prototype evidence. Real model
providers, external repos, deploy previews, PR creation, production effects,
accounts, auth, payment, billing, multitenancy, and compliance remain out of
scope.

A runnable prototype is not Markdown, JSON, or a plan. It must be a locally
viewable artifact that can be served over localhost and validated with an HTTP
200 response plus artifact evidence.

---

## 14.17 Phase 9

Must implement and use the first local L1 prototype pipeline:

- read a local idea spec JSON
- produce `runtime/prototypes/<prototype_id>/index.html`, `manifest.json`, and
  `runbook.md`
- start a local validation server or equivalent localhost surface
- verify HTTP 200 and expected prototype content
- write validation evidence under `runtime/prototype-validation/`
- keep real providers, external repos, deploy, PR, production, auth, payment,
  multitenancy, Web Console, and IDE extension out of scope

Gate N verifies generated prototype evidence, not only unit tests.

---

## 14.18 Stop Rule

If a task requires a capability outside Phase 0-4, create an activation
proposal. Do not implement it as a build-task. Phase 4 operational validation
is not an activation proposal; it is the required use-and-measure step after
the first governed kernel has passed Gate D.

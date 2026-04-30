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

---

## Gate F: Provider Adapter Kernel Activation

Pass conditions:

- provider adapter kernel activation proposal exists
- proposal recommends only a local/API-compatible provider adapter kernel
- proposal forbids real paid provider calls
- proposal forbids subscription-tied CLI worker daemonization
- proposal forbids external repo mutation, deploy, PR creation, merge, yellow
  auto-approval, and production side effects
- proposal requires raw provider output refs, raw digest, parsed output, parser
  schema version, adapter version, and drift status
- proposal requires forced-drift fixtures and cost facts even when expected
  cost is zero

Fail if Gate F is used to authorize real provider credentials, live paid calls,
subscription CLI automation, or external target repo mutation.

---

## Gate G: Provider Adapter Kernel Review

Pass conditions:

- provider adapter kernel implementation exists
- CLI produces `runtime/provider-evidence/stub-provider-output.json` from the
  ok local fixture
- generated provider evidence includes raw output ref, raw digest, raw size,
  parsed output, parser schema version, adapter version, drift status, and cost
  facts
- ok fixture has `drift_detected=false`
- forced-drift fixture has `drift_detected=true` and non-empty drift reasons
- validation and tests pass
- no real paid provider call, subscription CLI daemonization, live
  `auto_router` call, external repo mutation, deploy, PR creation, or production
  side effect occurred

Fail if drifted provider output can authorize dispatch, approval, ratchet
widening, or release-sensitive evidence.

---

## Gate H: devmasterd Local Control Plane Activation

Pass conditions:

- devmasterd local control-plane activation proposal exists
- proposal requires bearer token auth even on localhost
- proposal is limited to local queue, state, evidence, and provider adapter
  fixture execution
- proposal forbids Web Console, IDE extension, real paid provider calls,
  subscription CLI daemonization, live `auto_router`, external repo mutation,
  deploy, PR creation, merge, yellow auto-approval, and production side effects
- proposal defines an end-to-end local smoke path:
  `intake -> authorize -> run-provider -> evidence`

Fail if Gate H is used to authorize a public daemon, real provider credentials,
real paid calls, external repo mutation, or UI surface implementation.

---

## Gate I: devmasterd Local Kernel Review

Pass conditions:

- daemon kernel implementation exists
- unauthorized localhost API requests return 401
- authorized localhost API requests can run
  `intake -> authorize -> run-provider -> evidence`
- provider execution uses only local fixtures and writes provider evidence
  through the existing provider adapter kernel
- daemon state and evidence are persisted under `runtime/devmasterd/`
- no Web Console, IDE extension, real paid provider call, subscription CLI
  daemonization, live `auto_router`, external repo mutation, deploy, PR, or
  production side effect occurred

Fail if any endpoint can mutate state without token auth.

---

## Gate J: devmasterd Operational Validation Review

Pass conditions:

- devmasterd operational validation report exists
- at least three daemon smoke iterations ran
- unauthorized requests returned 401 in every iteration
- `intake -> authorize -> run-provider -> evidence` passed in every iteration
- provider execution used only local fixtures
- external side effect count is zero

Fail if Gate J is used to authorize Web Console, IDE extension, real provider
calls, external repo mutation, deploy, PR, or production side effects.

---

## Gate K: CLI Control Surface Activation Review

Pass conditions:

- CLI control-surface activation proposal exists
- proposal keeps CLI as a `devmasterd` API client, not a queue, authorization,
  cost, ratchet, provider, or evidence owner
- proposal limits CLI work to localhost daemon status, evidence, intake, and
  smoke commands
- proposal requires bearer token auth and forbids persisting token values in
  logs, evidence, or state artifacts
- proposal forbids Web Console, IDE extension, real paid provider calls,
  subscription CLI daemonization, live `auto_router`, external repo mutation,
  deploy preview, PR creation, and production side effects

Fail if Gate K is used to authorize a Web/IDE surface, real provider path,
external repo mutation, deploy, PR, or any CLI path that bypasses `devmasterd`.

---

## Gate L: CLI Control Surface Evidence Review

Pass conditions:

- CLI implementation exists
- CLI reads state and evidence through `devmasterd` HTTP APIs
- CLI can submit a local task proposal through `devmasterd`
- CLI smoke runs against a real localhost daemon and records a validation
  artifact under `runtime/cli-validation/`
- CLI smoke proves unauthorized requests remain blocked and the authorized
  path can run `intake -> authorize -> run-provider -> evidence`
- no Web Console, IDE extension, real paid provider call, subscription CLI
  daemonization, live `auto_router`, external repo mutation, deploy preview,
  PR creation, or production side effect occurred

Fail if the CLI writes daemon state/evidence directly or becomes a second
orchestration control plane.

---

## Gate M: L1 Prototype Pipeline Activation Review

Pass conditions:

- L1 prototype pipeline activation proposal exists
- proposal defines a runnable prototype artifact as a locally viewable artifact,
  not Markdown, JSON, provider output, or a plan
- proposal uses deterministic `local_tool` execution for the first pipeline
  implementation
- proposal defines localhost validation and prototype evidence outputs
- proposal forbids real OpenAI/Anthropic/API provider calls, live
  `auto_router`, subscription CLI daemonization, external repo mutation,
  deploy preview, PR creation, production effects, accounts, auth, payment,
  billing, multitenancy, compliance, Web Console, and IDE extension

Fail if Gate M is used to authorize real providers, deploy, external repo
mutation, PR creation, or L2 SaaS implementation.

---

## Gate N: L1 Prototype Pipeline Evidence Review

Pass conditions:

- L1 prototype pipeline implementation exists
- a local idea spec was converted into generated prototype files
- generated prototype includes at least `index.html`, `manifest.json`, and
  `runbook.md`
- validation report proves localhost HTTP 200 for the generated prototype
- validation report includes artifact refs and digests
- no real provider, external repo, deploy, PR, production, account, auth,
  payment, billing, multitenancy, compliance, Web Console, or IDE side effect
  occurred

Fail if Markdown/JSON-only output is accepted as a prototype, or if the pipeline
requires real provider calls to pass.

---

## Gate O: API Provider Activation Review

Pass conditions:

- API provider activation proposal exists
- proposal treats OpenAI API, Anthropic API, and `auto_router` as candidate
  provider paths, not as already-approved runtime calls
- proposal forbids any real provider call before a later gate and human
  credential approval
- proposal defines allowed and forbidden credential sources
- proposal applies [cost-ceilings.md](cost-ceilings.md) as a hard block before
  any paid call
- proposal requires raw+parsed provider evidence, parser schema version, cost
  facts, and drift detection
- proposal keeps subscription CLI daemonization, external repo mutation,
  deploy, PR creation, production, accounts/auth/payments/multitenancy, Web
  Console, and IDE extension out of scope

Fail if Gate O is used to authorize a paid provider call, store credentials, or
enable subscription CLI workers.

---

## Gate P: API Provider Contract Preflight Review

Pass conditions:

- provider request and evidence schemas exist
- provider preflight report records provider and credential source as pending
  human selection
- no credential value is stored in committed artifacts, evidence, logs, or
  fixtures
- preflight records hard cost ceilings and single paid-smoke approval template
- no network call, real provider call, subscription CLI daemonization, external
  repo mutation, deploy, PR creation, production, account/auth/payment, Web
  Console, or IDE side effect occurred

Fail if any secret value is persisted or if preflight makes a real provider
call.

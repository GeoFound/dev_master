# Task Backlog

> Ordered backlog for AI sessions. Only `tasks/current.md` is authoritative for
> the active task. Backlog items are candidates, not permission to skip gates.

---

## Phase 0

1. `phase-0-ai-cold-start-base`
   - Build repository-level AI cold-start artifacts.
   - Required before treating the repo as AI-operable.
   - Status: complete, pending human review through Gate A.

2. `gate-a-design-freeze-report`
   - Confirm design freeze pass/fail against Gate A.
   - Output: `reports/gate-a-design-freeze.md`.
   - Status: complete, pending human promote/hold/correct decision.

3. `phase-0-drift-check`
   - Confirm no active doc leaks deferred/future capability.
   - Output: `reports/drift/<date>-*.md`.
   - Status: complete for `phase-0-ai-cold-start-base`.

4. `phase-0-implementation-language-baseline`
   - Freeze Phase 1 language and file-format baseline.
   - Output: `25-implementation-language-baseline.md`.
   - Status: complete, pending human review through Gate A.

---

## Phase 1 Candidates

Gate A received a human `promote` decision on 2026-04-27.

1. `phase-1-menmery-facade-probe`
   - Verify the narrow caller protocol for `get_context`, `act`, `remember`,
     and `follow_recommended_call`.
   - Status: partially complete for `get_context` and `act`; `remember`
     writeback pending for the first slice outcome.

2. `phase-1-isolated-worker-choice`
   - Choose first local isolation strategy: worktree first unless evidence
     requires a stronger sandbox.

3. `phase-1-runner-facts-emitter`
   - Emit `software-change-runner-v1` facts for one low-risk docs/test task.
   - Status: in progress through `phase-1-first-executable-kernel-slice`.

4. `phase-1-verifier-first-pass`
   - Check request fit, evidence fit, risk fit, boundary fit, and writeback fit.
   - Status: in progress through `phase-1-first-executable-kernel-slice`.

5. `phase-1-forced-bad-case`
   - Create at least one verifier-blocking bad case without expanding scope.
   - Status: in progress through `tests/fixtures/bad_runner_facts.yaml`.

---

## Not Backlog

The following require activation proposals and are not backlog implementation
items:

- Ops AI
- Advisor AI
- TechRadar
- rewrite controller
- model governance
- generalized adapters
- Temporal HA or Kubernetes productionization
- DSSE/cosign/Tekton/GUAC rollout

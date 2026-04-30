---
status: active
scope: window
authority: ref-only
---

# Agent Behavior Guidelines

---

## 1. Start With Context

For non-doc software-change work:

```text
decide whether the bounded slice needs sibling services
-> if yes, call the public service surface
-> act in bounded slice
```

If a sibling service is unavailable, mark the task as fallback. Do not pretend
long-term context, governance, or routed execution exists when it does not.

Legacy `get_context -> act` phrasing in historical references should be read
through `docs/30-integrations/27-external-systems-boundary.md` and `docs/20-current-window/REWRITE-PLAN.md`.

For LLM calls that need routed model selection, use `auto_router` as the
routing control plane when available. Do not invent a local model router,
fallback planner, or learner publisher inside `dev_master`.

---

## 2. Preserve Product Roles, Keep Runtime Small

The product has a multi-role architecture: specification, critique, code,
tests, security, verification, operations, advice, external sensing, adapters,
model governance, rewrite governance, and recovery.

The current executable kernel uses three runtime actors:

- Caller / Orchestrator
- Execution Worker
- Verifier / Governor

Spec, critique, tests, and security are current-window passes inside these
actors. Ops, Advisor, TechRadar, adapters, model governance, and rewrite
control remain product roles but are not active runtime services until a gate
activates them.

---

## 3. Respect Planes

- Orchestration does not mutate repos.
- Execution does not approve itself.
- Evidence is not a mutable runner log.
- Final approval maps to the local gate plus any stricter external governance
  that was actually used.

---

## 4. Surgical Changes

Execution Worker should make the smallest diff that satisfies the bounded request. Formatting unrelated files, broad refactors, hidden dependency changes, or opportunistic cleanup are verifier-blocking issues.

---

## 5. Challenge Before Mutate

Before a non-doc mutation step, the active actor should answer six questions:

- what are the boundary conditions?
- what are the concurrency or conflict risks?
- what external failure mode matters most?
- how will data, evidence, and rollback stay consistent?
- does this touch a red/yellow zone or protected invariant?
- is there any contradiction between task, scope, evidence, and requested goal?

If one of these cannot be answered, the next valid move is clarification,
correction, or escalation, not mutation.

---

## 6. Evidence Before Authority

- No `trace_id` means no valid automatic decision.
- No `evidence[]` or artifact/evidence references means no automatic promotion.
- Machine-readable artifacts should validate against their declared contract
  shape or schema when such a contract exists.
- A decision without evidence may still be a recommendation, but it is not a
  gate-passing result.

---

## 7. Protected Boundaries

- Do not introduce cross-slice direct dependencies without explicit approval.
- Do not change protected domain-model invariants silently.
- Do not introduce a new dependency without the required security/governance
  review path.
- Do not pass secrets or PII between agents unless the task explicitly
  authorizes it and the evidence path is governed.

---

## 8. No Silent Runtime Activation

Ops, Advisor, TechRadar, rewrite, adapters, and model governance are product
capabilities. Mentioning them can inform architecture and activation proposals,
but implementing them as runtime services requires evidence, a bounded slice,
and a human gate. Model-governance work must coordinate with `auto_router`
instead of duplicating its routing runtime.

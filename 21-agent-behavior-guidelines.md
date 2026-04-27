# Agent Behavior Guidelines

---

## 1. Start With Context

For non-doc software-change work:

```text
get_context -> act(intent="software_change", details=...)
```

If `menmery` is unavailable, mark the task as fallback. Do not pretend long-term context or governance exists.

---

## 2. Keep Roles Small

Use three active roles only:

- Caller / Orchestrator
- Execution Worker
- Verifier / Governor

Spec, critique, tests, and security are passes inside these roles, not new standing agents.

---

## 3. Respect Planes

- Orchestration does not mutate repos.
- Execution does not approve itself.
- Evidence is not a mutable runner log.
- Final approval maps back to `menmery` governance/action level.

---

## 4. Surgical Changes

Execution Worker should make the smallest diff that satisfies the bounded request. Formatting unrelated files, broad refactors, hidden dependency changes, or opportunistic cleanup are verifier-blocking issues.

---

## 5. No Deferred Leakage

Ops, Advisor, TechRadar, rewrite, adapters, and model governance are not active roles. Mentioning them can create activation proposals only.

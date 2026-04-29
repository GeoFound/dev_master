# menmery Integration Boundary

> **Layer status: Active Core.** This file defines how `dev_master` integrates
> with `menmery`. It does not redefine `dev_master` as a `menmery` subproject.

---

## 23.1 Core Position

`dev_master` is an independent AI automation pipeline product.

`menmery` is long-term cognitive infrastructure. For `dev_master`, it is the
preferred integration for durable context, truth maintenance, canonical
evidence, audit, governance preview, approval lane, and action levels when that
integration is available.

```text
dev_master
  owns: AI automation pipeline product, software-change contracts,
        execution discipline, verifier facts, release/ops/advisory roadmap

menmery integration
  provides: context, canonical records, inbox/supersede, audit,
            governance preview, action level, evidence writeback
```

The integration boundary exists so `dev_master` does not build a competing
truth/governance/evidence runtime before evidence proves that it is necessary.
That boundary must not be used to shrink `dev_master` into only a runner
harness.

`menmery` does not checkout repositories, run shell commands, mutate code,
merge PRs, or deploy. Those belong to the external execution harness.

---

## 23.2 Current Caller Protocol

For non-doc software-change work, the current preferred call path is
`entry_turn` first. `entry_turn` is the low-friction doorway into `menmery`'s
panorama, provenance, missing-side, and governance scaffold. Direct
`get_context(...)` or `act(...)` calls remain valid only when the caller has
deliberately decided that no long-state scaffold is needed, or when
`entry_turn` recommends them as the next call.

```text
1. entry_turn(
     message="software_change / dev_master / <target repo> / <goal>",
     max_depth="auto"
   )
2. follow the returned recommended_call when it is needed and lane-allowed
3. run the current-window execution worker if the lane allows it
4. verify runner facts, risk facts, checks, diff digest, and evidence refs
5. remember(content=<structured result>, related_to=[entry_turn_id]) or use
   governed canonical writeback with the result
```

If the returned lane is supervised, human approval is required before the
side-effecting step. If `menmery` is unavailable, mark the task as fallback and
keep local evidence until writeback is possible. `structural_status=complete`
from a closure event means the required fields were filled; it does not mean
`menmery` semantically verified the content.

---

## 23.3 What dev_master Owns

`dev_master` owns the product architecture and software-delivery automation
loop:

- requirement intake
- specification and acceptance criteria
- critique and risk challenge
- implementation workers
- test and security facts
- verifier/result gate
- release, canary, rollback, RCA
- operations and external sensing roadmap
- Advisor AI, TechRadar, project adapters, model governance, rewrite
  governance, and recovery roadmap

The current Phase 0-3 implementation window owns only the first executable
kernel:

- runner facts contract
- local runner/verifier mechanics
- forced-bad cases
- evidence writeback references
- green reliability samples
- yellow preparation payloads

---

## 23.4 What menmery Owns In This Integration

When available, `menmery` is the canonical integration point for:

| Area | Integration responsibility |
|------|----------------------------|
| context | retrieve durable user/project context through `entry_turn` and facade tools |
| panorama | provide current subject, evidence, missing sides, unresolved gaps, and governed next step |
| governance preview | return action level and approval lane before execution |
| canonical evidence | hold durable evidence references and supersede chains |
| audit | preserve action and decision lineage |
| writeback | store observations/review evidence after completion, related to the originating `entry_turn_id` when available |

`dev_master` should not import `menmery` internals directly. Use documented MCP
or caller protocol surfaces.

---

## 23.5 Action Level Mapping

| Software-change action | Default action level | Handling |
|------------------------|----------------------|----------|
| read docs/code, generate analysis | 0 | analysis only |
| read-only scan, dependency query, CI status read | 1 | verification |
| local worktree diff, tests, draft patch | 2 | reversible operation |
| external issue/notification/PR write | 3 | controlled external effect |
| merge, deploy, delete, migration, secrets, permissions | 4 | high-stakes approval |

`dev_master` may use green/yellow/red labels for software-delivery risk, but
those labels must map back to the governance/action-level source used by the
current integration.

---

## 23.6 Current Non-Goals

The current implementation window must not silently build:

- a parallel canonical truth store
- an approval controller that competes with the selected governance integration
- a production Temporal cluster
- OPA/Conftest as the highest governance authority
- Ops/Advisor/TechRadar runtime services
- generalized adapter runtime
- model-governance runtime
- rewrite-controller runtime

These remain product-scope capabilities where applicable. They require
activation proposals and human gate decisions before runtime implementation.

---

## 23.7 Invariants

1. `dev_master` is the independent AI automation pipeline product.
2. `menmery` is an integration for truth/evidence/governance, not the product
   owner.
3. The current runner/verifier loop is the first executable kernel, not the
   whole product.
4. Three-plane boundaries are execution discipline, not three new competing
   platforms.
5. Runner logs are never final evidence by themselves.
6. Execution workers produce facts and diffs; they do not approve themselves.
7. Product roadmap capabilities must not be erased to satisfy a current-window
   gate.

---
status: active
scope: product
authority: this
---

# Product Architecture Decision

This decision freezes the product runtime shape for `dev_master`.

Core stance:

```text
dev_master owns scheduling, authorization, governance, evidence, cost, and
review state.

Codex, Claude Code, API models, and future agent systems are worker providers.
They may propose work and execute authorized slices. They do not own the queue,
approval state, ratchet, cost ceilings, or admissible evidence.
```

This file is interpreted with [28-product-principles.md](28-product-principles.md),
[engineering-execution-boundaries.md](engineering-execution-boundaries.md),
[task-proposal-contract.md](task-proposal-contract.md), and
[../20-current-window/14-master-program.md](../20-current-window/14-master-program.md).

---

## 1. Language Allocation

| Product area | Default language / format | Decision |
|--------------|---------------------------|----------|
| Core kernel: runner, verifier, evidence, local policy facts | Python | Approved for Phase 1-3. |
| `devmasterd` daemon / local control plane | Python first | Move to Go only if evidence shows Python blocks reliability or throughput. |
| Web Factory Console | TypeScript / Next.js | Primary human product surface after the core loop exists. |
| VSCode / Cursor / Windsurf extension | TypeScript | Thin client only; not a governance owner. |
| LLM routing gateway | External `auto_router` / Go | `dev_master` does not reimplement routing, failover, or learner control. |
| Contracts, facts, evidence indexes | JSON Schema, JSON, JSONL | Machine-readable, append-only where evidence-bearing. |
| Human reports and decision records | Markdown | Human review and audit readability. |
| Shell / `just` | Thin wrappers only | No complex governance or verifier logic in shell. |

Phase 1-3 implementation must not introduce TypeScript/JavaScript for the core
kernel. TypeScript is reserved for product surfaces and extension clients.

---

## 2. Product Surfaces

The final product is a factory control plane, not a chat window.

Primary surface:

- Web Factory Console

Secondary surfaces:

- CLI for local/admin operation
- IDE extension as a thin client
- optional future issue tracker, GitHub, Slack, or Linear integrations

The Web Factory Console should eventually expose:

- intake queue
- project registry
- run timeline
- human review inbox
- evidence viewer
- cost and autonomy dashboard
- provider/worker status

The CLI and IDE extension must call `devmasterd`; they must not become parallel
orchestration systems.

---

## 3. Surface Sequencing

Surfaces must be built in this order:

1. Phase 1B: CLI-only surface for the first local L1 prototype proof.
2. Phase 2: Web Console MVP with queue, inbox, and cost dashboard. No rich diff
   viewer is required.
3. Phase 3: Web Console completion plus IDE extension after the daemon API
   contract has been frozen for at least 14 days with no breaking schema
   changes, or after an explicit deprecation/versioning policy has been added
   to the daemon API contract.

Building CLI, Web, and IDE surfaces in parallel is out of policy for the
current program. Each surface is a protocol consumer; protocol churn must be
absorbed by one surface first.

---

## 4. Worker Provider Strategy

Default path:

- Phase 1-2 worker providers should use API-backed paths by default:
  OpenAI API, Anthropic API, or `auto_router` when that integration is active.

Subscription-tied providers:

- Codex CLI, Codex app/SDK surfaces, Claude Code CLI, and Claude Code SDK may be
  added as Phase 2+ cost-reduction or local-workflow options.
- They must only be enabled when the provider's current terms and official
  docs allow the intended headless or automated use.
- They must have a drift detector, version pin, and raw-output evidence capture
  before their output is admissible for automated verifier decisions.
- They must not be the only provider path for Phase 1B.

Provider adapters must normalize all worker outputs into `dev_master` runner
facts. Provider claims are not approval decisions.

---

## 5. Provider Evidence Contract

Every provider adapter that calls a CLI, SDK, or API must capture both raw and
parsed output:

```yaml
provider_adapter_version: "provider-name-v0.x"
provider_kind: "api|subscription_cli|subscription_sdk|local_tool"
provider_name: "openai_api|anthropic_api|codex_cli|claude_code_cli|auto_router"
provider_version: "reported-version-or-null"
provider_raw_output_digest: "sha256:..."
provider_raw_output_ref: "evidence/provider/raw/..."
provider_raw_output_size_bytes: 0
provider_raw_output_storage: "artifact_store|inline"
parsed_output: {}
parse_schema_version: "1.0.0"
drift_detected: false
drift_reasons: []
```

Rules:

- raw output must be stored before parsing when feasible
- raw output larger than the local inline threshold must be chunked or stored
  in the evidence artifact store; SQLite / JSONL indexes should keep only
  digest, size, media type, and refs
- parsed output must reference the parser schema version
- parse failure, missing fields, unexpected output shape, unknown version, or
  provider warning must set `drift_detected: true`
- drifted provider output cannot authorize dispatch, approval, ratchet
  widening, or release decisions
- evidence must be replayable from raw output plus parser version

---

## 6. Workspace Governance Rule

In a workspace governed by `dev_master`, all paid AI calls and all repo
mutations intended to produce admissible evidence must route through
`devmasterd`.

Direct Codex, Claude Code, API, or IDE-agent calls that bypass `devmasterd` are
out of policy for governed work. They may be used for informal exploration, but
their output is not admissible evidence unless it is re-run or imported through
a governed adapter that preserves raw output, parser version, cost facts, and
evidence refs.

The IDE extension should warn or block when it detects a governed workspace and
the user attempts direct mutation outside `devmasterd`. Early versions may
enforce this as user-level discipline; later versions should enforce it in the
client and daemon protocol.

---

## 7. Default Deployment

Default deployment for the first 24/7 operating model:

```text
local always-on machine
-> devmasterd
-> local queue and evidence store
-> API-backed providers by default
-> optional subscription providers after drift and ToS checks
```

Examples: NUC, home server, dedicated mini-PC, or another always-on local
machine.

VPS deployment is Phase 3+ unless a human-approved activation decision adds:

- secret-management plan
- daemon API authentication plan
- worker isolation plan
- provider credential refresh plan
- network exposure and firewall plan

The daemon API must require a token even on localhost. The local MVP may store
client tokens in SQLite. Tokens and provider credentials must not be stored in
Markdown docs or runner logs.

---

## 8. Authorization Flow

Canonical flow:

```text
human idea / issue / IDE command
-> dev_master intake
-> planner agent proposes slices
-> dev_master validates task proposal
-> dev_master authorizes bounded slices
-> provider worker executes
-> verifier blocks / escalates / allows
-> evidence is written
-> human review inbox if required
```

AI may propose slice decomposition. Only `dev_master` may authorize dispatch
after checking ratchet bounds, cost ceilings, engineering boundaries, and the
active phase.

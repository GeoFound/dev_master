# Tools And Cost Boundary

---

## Active Tools

| Tool | Role |
|------|------|
| `menmery` MCP facade | context, governance preview, action level, evidence writeback |
| Claude Code / Codex CLI | caller or isolated execution worker |
| local worktree / sandbox | repo mutation boundary |
| semgrep / trufflehog / project tests | runner facts |
| `auto_router` | optional LLM calls for verifier or analysis |

---

## Boundaries

- `menmery` owns truth/governance/evidence.
- `auto_router` owns LLM routing/model selection/cost/failover.
- `dev_master` owns runner contract and software-change evidence shape.

No Phase 1 component may perform model governance, background ops scanning, or autonomous purchasing.

---

## Cost Rule

Phase 1 uses existing local/subscription tools first. Paid or external calls must appear in runner facts and are at least yellow if they create recurring cost.

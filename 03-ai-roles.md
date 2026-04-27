# AI 角色模型：三角色，不再九角色

> Active Core 只允许三个角色。旧的 Spec / Critic / Test / Security / Advisor / Ops / TechRadar 都降级为 pass、tool、deferred blueprint 或 archive 内容，不再是 Phase 1 独立角色。

---

## 3.1 三个角色

| 角色 | Active 职责 | 不负责 |
|------|-------------|--------|
| Caller / Orchestrator | 调用 `menmery get_context` / `act`，组织任务，等待 approval lane，收集 evidence refs | 不改 repo，不运行 shell，不自建 approval |
| Execution Worker | 在隔离 worktree/sandbox 中做 diff、lint、test、security scan，产出 runner facts | 不决定 final approval，不写 canonical truth |
| Verifier / Governor | 检查 request vs diff vs tests vs risk facts vs menmery evidence，给出 allow/block/escalate 建议 | 不替代 human gate，不替代 menmery governance |

---

## 3.2 Passes 而不是角色

Phase 1 中以下内容只是 pass：

| 旧名称 | 新定位 |
|--------|--------|
| Spec AI | Caller 的 planning/spec pass |
| Critic AI | 同一 prompt 内的 self-critique pass |
| Test AI | Execution Worker 的 test generation / test run step |
| Security AI | Execution Worker 的 semgrep/trufflehog/dependency facts step |
| AI Code Review | Verifier 的一个检查项 |

这些 pass 可以用不同模型或工具执行，但不得升级为独立长期角色、独立队列或独立治理主体。

---

## 3.3 最小调用顺序

```text
1. Caller:
   get_context("software_change / repo / goal")
   act(intent="software_change", details=bounded_request)

2. Execution Worker:
   create isolated worktree
   apply minimal diff
   run lint/test/security checks
   emit runner facts + artifact digests

3. Verifier / Governor:
   compare request, diff, checks, risk facts
   require remember/canonical evidence writeback
   return allow/block/escalate recommendation
```

Final approval comes from:

```text
menmery action level + governance preview + runner facts + human gate if required
```

---

## 3.4 External Tools

| Tool | Boundary |
|------|----------|
| Claude Code / Codex CLI | May serve as caller or execution worker, but side effects must stay in execution plane |
| OpenAI Sandbox / container worker | Optional execution plane implementation |
| `auto_router` | Only for LLM routing/cost/failover; dev_master does not classify models |
| semgrep / trufflehog / tests | Runner tools that produce facts |

---

## 3.5 Deferred Names

Ops AI、Advisor AI、TechRadar、rewrite controller、model governance、generic adapters are not active roles. They can only return through activation proposals after Phase 1-3 evidence exists.

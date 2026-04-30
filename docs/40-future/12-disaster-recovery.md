---
status: future
scope: product
authority: ref-only
---

# Disaster Recovery And Future Blueprint Overview

> **文件性質：未來藍圖（future blueprint），不是運行中系統的描述。**
> 本文件描述當執行內核穩定、產生真實 audit / evidence 流之後，DR 應如何構建。
> 當前倉庫尚未重建這些 DR runtime：`audit/*.jsonl` 不存在、CI 未配置、GitHub Actions 未啟用、Supabase 未綁定。
> 所有路徑、workflow、secrets、cron 表達式都是實現時的目標形態，不代表已部署的自動化。

> Overview of disaster recovery and future product blueprints. Detailed future
> authorities now live in separate files so rewrite, adapters, and external
> gateway integration can evolve without one monolithic document.

> 系統實現後將重度依賴 `audit/*.jsonl` 文件和 `inbox/` 文件系統。本部分定義 DR 啟用時的可復原性保障目標和從零恢復步驟。

### 12.1 審計日誌備份策略（目標）

**實現後，審計日誌應作為系統的記憶，不可丟失**。目標備份應分兩層：

```
Layer 1（目標）：Git 倉庫本身（主副本）
  - 實現後，audit/*.jsonl 每次 CI commit 應推送到 Git
  - Git 歷史應提供完整變更回溯
  - 風險：倉庫損毀時丟失全部歷史

Layer 2（目標）：Supabase 結構化備份（離線副本）
  - 實現後，每日 GitHub Actions 應將 audit/*.jsonl 寫入 Supabase 表
  - 應可查詢、可聚合、可導出
  - 風險：Supabase 只是結構化副本，不是唯一真相源
```

> 以下 workflow 是 DR 實現時的目標形態。當前 `.github/workflows/` 無此文件，secrets 未配置，Supabase 未綁定。

```yaml
# .github/workflows/audit-backup.yml
name: Daily Audit Backup to Supabase

on:
  schedule:
    - cron: '30 0 * * *'  # 每日 00:30 UTC
  workflow_dispatch:

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Sync audit logs to Supabase
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_SERVICE_KEY: ${{ secrets.SUPABASE_SERVICE_KEY }}
        run: python scripts/backup_audit_to_supabase.py
```

### 12.2 從零恢復步驟

當倉庫損毀或關鍵文件意外被覆寫時：

```
1. 從 GitHub 遠端 clone 最新版本（Git 歷史未損壞的情況）
   git clone {repo_url} && cd {project-root}

2. 如果 audit/ 目錄丟失，從 Supabase 恢復：
   python scripts/restore_audit_from_supabase.py

3. 熔斷器狀態自動從 audit/circuit-breaker-state.json 恢復
   （該文件丟失時，所有熔斷器重置為 CLOSED，原則上安全但建議人工確認）

4. 重建 TechRadar 狀態：手動觸發 TechRadar 掃描
   python -m techradar.techradar_scanner --full-scan

5. 重建 Ops AI 狀態：下一次 15 分鐘巡檢自動恢復（無狀態設計）

6. 確認 inbox/ 目錄中的待審提案：對照 Supabase 中的提案記錄補回
```

### 12.3 AI 模型服務故障應對

當路由網關整體宕機或特定模型下線時：

```
影響範圍：
  - 執行層（Test AI / Security AI）：流水線暂停，任務排隊
  - 感知層（Ops AI / TechRadar / Advisor AI）：降級為純 API 巡檢（無 LLM 分析）
  - 訂閱層（Claude Code / Codex CLI）：不受影響（獨立服務）

應對機制：
  1. `auto_router` 在其內部完成 classifier / routing / failover 切換
  2. 若網關整體不可用，`dev_master` 僅保留訂閱制路徑，將需要網關的任務延遲到下一個窗口
  3. 延遲超過 2 小時，觸發人工通知（通過通知適配層 §6.5）
  4. `dev_master` 只記錄「網關不可用 / 任務延期 / 人工介入」等本地事件；模型級 fallback 事件以 `auto_router` 審計為準
```

## 12.4 Long-Term Gap Map

> v3 已能支撐高強度交付治理，但若目標是陪項目活很多年、支撐多次架構演進甚至整體重寫，還需要以下 10 個能力。這些能力是系統未來演進的主幹，不是附加功能。

1. **整項目重寫工作流**
   - 支持舊系統/新系統雙軌運行、能力對齊、遷移波次、流量切換、退役判定
2. **非 Web 項目適配層**
   - 將治理內核與 Web/SaaS 實現細節拆開，支持 App、桌面、CLI、遊戲、嵌入式
3. **生命周期階段模型**
   - 區分 0→1、PMF 前、規模化、平台化、退役/重寫期的不同治理策略
4. **領域模型保護層**
   - 保護核心業務概念、不變量、關鍵狀態機與術語兼容性
5. **技術債投資組合管理**
   - 區分高風險債、拖慢迭代的債、阻塞重寫的債與低價值噪聲
6. **架構演進地圖**
   - 明確當前架構站位、目標架構、穩定區、待替換區、待拆除區
7. **數據遷移與兼容性治理**
   - 管理 API 並存、數據模型兼容期、客戶端舊版本支持與事件演進
8. **知識沉澱與決策檢索**
   - 讓 AI 和人能查到歷史決策、事故、門禁變更、提案拒絕原因
9. **組織與協作適配層**
   - 支持多人協作下的角色分層、審批權模型、值班與升級路由
10. **外部模型治理接入層**
   - 對接外部路由控制面（如 `auto_router`）的模型治理結果，而不是在 `dev_master` 內重新實作一套

**設計原則**：
- 不把這 10 項能力一次性做完，而是按項目規模與演進階段逐步接入
- 每新增一項能力，都必須對應一份 `schema`、一份 `ruleset`、一條審計路徑
- 長期演進能力的目標不是“更智能”，而是“更可控、更可回退、更可繼承”

## 12.5 Detailed Future Authorities

The detailed future blueprints now live in separate files:

| Topic | File | Role |
|-------|------|------|
| whole-project rewrite workflow | [29-rewrite-blueprint.md](29-rewrite-blueprint.md) | future authority for rewrite proposal, waves, gates, and retirement |
| project-type adapters | [30-project-adapter-blueprint.md](30-project-adapter-blueprint.md) | future authority for governance-kernel-to-stack mapping |
| external model-governance integration | [31-external-model-governance-integration.md](31-external-model-governance-integration.md) | future authority for gateway request/result/feedback linkage and degradation |

This file remains the recovery and future-overview pointer. New detail should
go into the topic-specific future authority, not back into this overview page.

---

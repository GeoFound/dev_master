---
status: active
scope: window
authority: ref-only
---

## 第六部分 B：跨會話狀態持久化

> **文件性質：實現藍圖（target spec），不是運行中系統的描述。**
> 本文件描述當 `software_change` runner / verifier 實現時，本地 fallback state 與 evidence 索引的目標形態。
> 當前倉庫尚未重建這套 persistence runtime，所有 PostgreSQL 表、JSONL 路徑、`StateStore` 接口、advisory lock 都未實現也未配置。
> 所提到的 `localhost:5432` 開發 DB 是個人工作站的可選試運行後端，不是 dev_master 產品的部署假設；產品實際部署時的持久化後端需另行聲明。

> Claude Code 每次會話獨立啟動，不自動繼承前次會話的運行時狀態。信任引擎、熔斷器、審計追蹤等需要跨會話存活的數據，實現後必須通過持久化層顯式讀寫。

> **v4.1 修正：** 本文件不再把 `StateStore` 定義為完整 durable orchestration engine。長期 workflow state、approval wait、timer、retry 和 replay 語義屬於 [22-three-plane-architecture.md](22-three-plane-architecture.md) 的 orchestration plane，長期目標是 Temporal-style workflow。`StateStore` 只負責本地 runtime index、熔斷器摘要與 fallback state。

> **v4.2 修正：** 當 `menmery` 可用時，canonical truth、governance audit、approval lineage 與長期 evidence 默認由 `menmery` 提供。`StateStore` 只作為 `software_change` runner 的本地索引、artifact digest cache、fallback queue 或短期執行狀態，不得成為與 `menmery` 平行的 truth source。

### 6B.1 狀態分類

| 類別 | 內容 | 寫入頻率 | 不可變性 | 示例 |
|------|------|----------|----------|------|
| **審計記錄** | 流水線決策、安全掃描結果、成本追蹤；若 `menmery` 可用則回寫為 observation / review evidence | 每次流水線執行 | 不可變（只追加） | `menmery audit id` / `audit/ai-decisions.jsonl` |
| **治理狀態** | `menmery` governance preview / action level；本地只保留 runner 所需摘要 | 邊界變更時 | 不可變（版本化） | `menmery governance audit` / `governance/trust-engine-state.json` |
| **熔斷器狀態** | 每個 feature 的連續失敗計數、熔斷觸發時間 | 每次流水線執行 | 可變（最新狀態） | `governance/circuit-breaker-state.json` |
| **提案記錄** | activation proposal | 提案創建和審批時 | 不可變（只追加） | `inbox/proposal-*.md` |
| **執行上下文** | Phase 1 fallback 的當前任務隊列、阻塞狀態 | 每次會話開始/結束 | 可變（最新狀態） | `runtime/session-context.json` |
| **證據索引** | artifact digest、policy snapshot、approval snapshot、簽名 envelope reference；canonical reference 指向 `menmery` record / inbox / audit ID | 每個 stage 完成時 | 不可變（只追加） | `menmery record id` / `audit/evidence-index.jsonl` |

### 6B.2 存儲格式

兩種格式，按用途選擇：

**JSONL（追加型記錄）**：
```jsonl
{"timestamp": "2026-04-06T10:00:00Z", "event": "pipeline_success", "feature": "auth", "duration_s": 120}
{"timestamp": "2026-04-06T11:30:00Z", "event": "pipeline_failure", "feature": "billing", "error": "test_timeout"}
```
- 適用於：審計記錄、成本追蹤、信任引擎的原始事件
- 優點：追加寫入天然原子（Linux 上小於 4KB 的單次 write 是原子的）
- 查詢方式：逐行掃描 + 過濾（數據量小時直接全量載入）

**Markdown + Frontmatter（結構化記錄）**：
```markdown
---
id: proposal-2026-04-06-001
type: dependency_replacement
status: pending_review
created_at: 2026-04-06T10:00:00Z
created_by: advisor_ai
---

## 提案：替換 moment.js → date-fns

### 背景
...
```
- 適用於：提案記錄、邊界定義變更、架構決策記錄（ADR）
- 優點：人類可讀、Git 友好、支持 frontmatter 查詢
- 查詢方式：按目錄掃描 + frontmatter 解析

### 6B.3 會話啟動時的狀態加載

每次會話開始時，Phase 1 caller / lightweight Orchestrator 先完成本地恢復；若本次任務選擇使用 `menmery`，再追加讀取其上下文。當 Temporal-style orchestration plane 啟用後，此序列只作為本地恢復和 evidence index 加載流程，不再作為唯一 workflow source of truth：

```
0. 讀取本地 current task / evidence index / runtime state
   → 建立本輪的 trace、fallback 狀態、最近的 evidence 索引

0b. 若本次任務使用 menmery，再調用其 facade
    `entry_turn("software_change / dev_master / target repo / <goal>", max_depth="auto")`
    → 取得 `entry_turn_id`、`recommended_call`、近期 activity、governance state、
      相關 capability gap

1. 讀取 governance/circuit-breaker-state.json
   → 確認哪些 feature 處於熔斷狀態，跳過它們
   
2. 讀取 governance/trust-engine-state.json
   → 確認當前枷鎖版本和各任務類型的邊界設定

3. 讀取 runtime/session-context.json
   → Phase 1 fallback：恢復上次會話未完成的任務隊列（如果有）

4. 掃描 inbox/ 目錄
   → 發現新需求（requirement-*.md）和待審批提案（proposal-*.md）

5. 讀取 audit/usage-tracking.jsonl 最後 N 條
   → 確認當前成本狀態，決定是否觸發降級

6. 讀取 audit/evidence-index.jsonl 最後 N 條
   → 建立 trace_id / run_id / evidence_id / menmery_record_id 到 artifact digest 的索引
```

這個序列可以封裝為一個 Python 腳本或 Claude Code 自定義命令（`/pipeline-init`），確保每次會話都從一致的狀態開始。

### 6B.4 並發保護

單項目場景下，同時只應有一個活躍的流水線會話。防止並發衝突的機制：

**首選：PostgreSQL Advisory Lock**：
```sql
-- 獲取鎖（非阻塞）
SELECT pg_try_advisory_lock(hashtext('pipeline:' || $project_name));
-- 釋放鎖
SELECT pg_advisory_unlock(hashtext('pipeline:' || $project_name));
```
- 會話級鎖：會話斷開時自動釋放，無需 TTL
- 不存在死鎖風險（進程崩潰 → 連接斷開 → 鎖自動釋放）
- 可通過 `pg_locks` 系統視圖查詢當前鎖持有者

**備選：文件鎖**（PostgreSQL 不可用時）：
```
runtime/pipeline.lock
├── holder: "claude-code-cli-session-2026-04-06T10:00"
├── acquired_at: "2026-04-06T10:00:00Z"
└── ttl_minutes: 120
```
- TTL 防止會話異常退出導致死鎖

**審計記錄的寫入安全性**：
- PostgreSQL 模式：INSERT 事務保證原子性
- 文件模式：JSONL 追加寫入（`open("a")`），每條記錄小於 4KB 保證原子
- 可變狀態：PostgreSQL 使用 `UPDATE ... RETURNING`；文件使用「寫臨時文件 + 原子重命名」

### 6B.5 持久化層接口

流水線代碼通過以下接口與 local state / fallback evidence index 交互，不直接依賴具體實現。長期 workflow 狀態不得只依賴此接口；需要由 orchestration plane 持有。canonical truth / governance / approval lineage 不得只存在於 StateStore；當 `menmery` 可用時必須回寫 `menmery`。

```python
# pipeline/state.py — 持久化層接口

from abc import ABC, abstractmethod
from typing import Any

class StateStore(ABC):
    """流水線狀態持久化接口。"""
    
    @abstractmethod
    def append_record(self, category: str, record: dict) -> None:
        """追加一條不可變記錄（審計、事件）。"""
        ...
    
    @abstractmethod
    def read_records(self, category: str, since: str | None = None, limit: int = 100) -> list[dict]:
        """讀取記錄，支持時間範圍過濾和數量限制。"""
        ...
    
    @abstractmethod
    def get_state(self, key: str) -> dict | None:
        """讀取可變狀態（熔斷器、信任引擎）。"""
        ...
    
    @abstractmethod
    def set_state(self, key: str, value: dict) -> None:
        """寫入可變狀態（原子替換）。"""
        ...

    @abstractmethod
    def acquire_lock(self, lock_id: str, holder: str, ttl_minutes: int) -> bool:
        """嘗試獲取鎖。成功返回 True。"""
        ...

    @abstractmethod
    def release_lock(self, lock_id: str) -> None:
        """釋放鎖。"""
        ...
```

#### 實現優先級

| 優先級 | 後端 | 適用場景 | 說明 |
|--------|------|----------|------|
| **首選** | PostgreSQL（如使用 `localhost:5432` 個人工作站開發實例） | 個人工作站試運行 | 若選擇 PostgreSQL 後端，可優先使用本地開發實例做試運行；產品部署時需另行聲明持久化後端 |
| **備選** | 本地文件系統（JSONL + JSON） | PostgreSQL 不可用或不採用時 | 零依賴 fallback，追加寫入天然原子，但缺少事務和高效查詢 |
| **可選** | MCP 持久化服務 | 需要遠端訪問時 | 接口不變，可通過 MCP server 封裝 PostgreSQL 或其他後端 |

實現時若採用 PostgreSQL，目標表結構建議：
```sql
-- 審計記錄（不可變，只追加）
CREATE TABLE pipeline_audit (
    id BIGSERIAL PRIMARY KEY,
    category TEXT NOT NULL,          -- 'ai-decisions', 'ops-actions', 'recovery-actions' 等
    trace_id TEXT,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_audit_category_time ON pipeline_audit(category, created_at);
CREATE INDEX idx_audit_trace ON pipeline_audit(trace_id) WHERE trace_id IS NOT NULL;

-- 可變狀態（原子替換）
CREATE TABLE pipeline_state (
    key TEXT PRIMARY KEY,            -- 'circuit_breaker', 'trust_engine', 'session_context' 等
    value JSONB NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

實現時，鎖機制也可升級為 PostgreSQL advisory lock，避免文件鎖的 TTL 和死鎖問題。Redis（如使用 `localhost:6379` 個人工作站實例）可作為輔助鎖方案，適用於需要更細粒度超時控制的場景；產品部署時鎖後端需另行聲明。

---

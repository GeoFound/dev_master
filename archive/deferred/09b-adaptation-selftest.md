## 第九部分 B：項目接管、類型適配與流水線自檢

> **分層狀態：Deferred Program。** 本文件保留為單項目穩定後的接管與適配設計，不作為當前 active core 的立即實作承諾。

### 9B.0 流水線接管目標項目

本流水線（dev_master）是一個**獨立倉庫**，目標項目也是一個獨立倉庫。兩者通過配置指向而非代碼依賴關聯。

#### 基本原則

- **一對一**：一個流水線實例只管理一個目標項目。如果需要同時管理多個項目，部署多個流水線實例
- **流水線不入侵目標項目**：流水線的代碼、配置、審計日誌存放在流水線倉庫中，不污染目標項目的目錄結構
- **目標項目無感知**：目標項目不需要知道流水線的存在。流水線通過標準 Git 操作和項目自身的 CI/CD 與目標項目交互

#### 配置指向

流水線倉庫根目錄維護 `target-project.yaml`，描述當前管理的目標項目：

```yaml
# target-project.yaml
target:
  name: my-saas-app
  repo_path: /home/jade/projects/my-saas-app    # 本地路徑
  repo_url: git@github.com:user/my-saas-app.git  # 遠端地址（用於 CI）
  main_branch: main
  
  # 流水線工作區（在目標項目內，但被 .gitignore 排除）
  workspace:
    inbox: .pipeline/inbox/          # 需求和提案放置處
    worktree_root: .pipeline/work/   # Codex CLI 的 git worktree 根目錄
  
  # 可選：覆寫自動檢測的項目類型
  # profile_override: fullstack_saas
```

#### 首次接管流程

當流水線首次指向一個新的目標項目時，Orchestrator 執行以下步驟：

```
步驟 1：驗證可達性
  □ 目標路徑存在且為 Git 倉庫
  □ 可以 checkout、pull、push（權限測試）
  □ main_branch 存在

步驟 2：環境掃描
  □ 掃描項目結構 → 生成 pipeline-profile.yaml（見 9B.1）
  □ 檢測現有 CI/CD 配置（GitHub Actions / Vercel / Docker）
  □ 檢測現有測試框架和覆蓋率工具
  □ 檢測依賴管理工具（package.json / pyproject.toml / go.mod）

步驟 3：工作區初始化
  □ 在目標項目中創建 .pipeline/ 目錄
  □ 將 .pipeline/ 加入目標項目的 .gitignore（如尚未存在）
  □ 初始化 inbox/ 目錄

步驟 4：生成接管報告
  □ 項目類型識別結果
  □ 已檢測到的現有基礎設施（CI、測試、部署）
  □ 流水線模塊激活/停用建議
  □ 識別到的潛在風險（無測試、無 CI、過時依賴）
  □ 報告寫入 audit/onboarding-{project_name}.jsonl

步驟 5：人工確認
  □ 接管報告提交人工審閱
  □ 人工確認後，流水線進入就緒狀態
```

首次接管是**黃區操作**——需要人工確認。後續的會話啟動不需要重新接管。

#### 會話啟動（非首次）

每次新會話開始時，Orchestrator 從 `target-project.yaml` 加載配置，然後：

1. 驗證目標項目路徑可達
2. 加載 `pipeline-profile.yaml`（項目類型配置）
3. 加載流水線狀態（信任引擎、熔斷器、未完成任務）
4. 掃描 `inbox/` 中的新需求或提案
5. 恢復或開始工作

#### 切換目標項目

切換到不同項目時：

1. 保存當前項目的完整狀態快照
2. 更新 `target-project.yaml` 指向新項目
3. 對新項目執行首次接管流程（如果是全新項目）或加載已保存的狀態（如果是回歸項目）

切換是**黃區操作**，需要人工確認。

---

### 9B.1 項目類型適配

本流水線管理**單個項目**，但目標項目不固定——可能是 SaaS、Web 全棧、CLI 工具、庫、或其他類型。不同類型的項目需要不同的模塊組合。

#### 項目類型識別

接管新項目時，Orchestrator 通過掃描以下信號自動識別項目類型：

| 信號 | 檢測方式 | 推斷 |
|------|----------|------|
| `package.json` + `src/` + API routes | 文件存在性 | Web 全棧 |
| `prisma/schema.prisma` 或 ORM 配置 | 文件存在性 | 有數據層 |
| `Dockerfile` + `docker-compose.yml` | 文件存在性 | 容器化部署 |
| `openapi/*.yaml` 或 Swagger 配置 | 文件存在性 | API 項目 |
| CLI 入口（`bin/`、`cmd/`、`__main__.py`） | 文件存在性 + 入口分析 | CLI 工具 |
| 無部署配置、有 `setup.py`/`pyproject.toml` | 文件模式 | 庫 |
| 存在支付相關代碼 | Grep 掃描 | SaaS（紅區觸發） |

識別結果寫入項目根目錄的 `pipeline-profile.yaml`：

```yaml
# pipeline-profile.yaml（由 Orchestrator 生成，人工可覆寫）
project_type: fullstack_saas
detected_at: 2026-04-06T10:00:00Z

features:
  has_api: true
  has_database: true
  has_frontend: true
  has_deployment: true
  has_payment: true        # → 自動標記支付相關切片為紅區
  has_cli: false

modules:
  canary_deployment: active       # 有部署配置時激活
  api_contract_validation: active # 有 openapi 時激活
  database_migration_guard: active # 有 ORM 時激活
  cli_test_matrix: inactive       # 非 CLI 項目停用
  library_publish_guard: inactive  # 非庫項目停用
```

#### 模塊激活/停用

| 模塊 | 激活條件 | 停用時的行為 |
|------|----------|-------------|
| **Canary 部署** | `has_deployment: true` | 跳過 Canary 階段，直接部署（仍走測試門禁） |
| **API 合約驗證** | `has_api: true` | 不強制 OpenAPI spec，Spec AI 生成需求文檔而非 API 契約 |
| **數據庫遷移守衛** | `has_database: true` | 不檢測 breaking migration，不觸發紅區 |
| **CLI 測試矩陣** | `has_cli: true` | 不生成跨平台 CLI 測試 |
| **庫發布守衛** | 項目是庫類型 | 不檢測 semver 破壞性變更 |
| **支付紅區** | `has_payment: true` | 支付相關代碼不標記為紅區 |

人工可以在 `pipeline-profile.yaml` 中覆寫任何自動檢測結果。

---

### 9B.2 流水線自檢（Pipeline Self-Test）

流水線自身也是代碼，需要驗證自身的正確性。

#### 組件級測試（pipeline-tests/）

每個流水線核心組件維護自己的測試：

```
pipeline-tests/
├── test_trust_engine.py          # 信任引擎：給定事件序列 → 預期邊界調整
├── test_circuit_breaker.py       # 熔斷器：模擬連續失敗 → 預期觸發/恢復
├── test_contract_validator.py    # 合約驗證：已知 valid/invalid 樣本 → 預期判定
├── test_state_persistence.py     # 持久化層：寫入/讀取/鎖定 → 預期行為
├── test_project_adaptation.py    # 項目適配：不同項目結構 → 預期 profile
└── fixtures/
    ├── trust_engine_scenarios.json    # 信任引擎測試場景
    ├── valid_contracts/               # 合約驗證正例
    └── invalid_contracts/             # 合約驗證反例
```

這些測試由流水線自身的 Test AI 執行。如果流水線測試失敗，整個流水線暫停並升級為人工介入。

#### 金絲雀需求（End-to-End Health Check）

維護一個標準的測試需求，定期執行完整流水線鏈路：

```markdown
# inbox/canary-requirement.md
---
id: CANARY-001
type: pipeline_health_check
schedule: weekly
auto_cleanup: true
---

## 需求：新增 /health 端點

在 API 層新增一個 GET /health 端點，返回 {"status": "ok", "timestamp": ...}。

## 預期流水線行為

1. Spec AI 生成 OpenAPI spec 片段
2. Critic AI 評估（應通過，置信度 > 90）
3. Code AI 實現端點
4. Test AI 生成測試並執行
5. Security AI 掃描（應無風險）
6. 全部通過 → 自動清理（不合併，只驗證流程）

## 驗收標準

- 流水線在 10 分鐘內完成
- 所有 6 個階段均成功
- 審計日誌完整記錄
- 成本 < $0.50
```

金絲雀需求每週自動執行一次。結果寫入 `audit/pipeline-health.jsonl`。連續兩次失敗觸發人工告警。

#### 配置變更審計

流水線自身的配置變更（信任引擎閾值、熔斷器參數、邊界定義）走與業務代碼相同的治理路徑：

- 配置變更由 AI 提出 → 生成 proposal
- Critic AI 審查配置變更的影響範圍
- 變更記錄寫入 `audit/pipeline-config-changes.jsonl`
- 高風險配置（放寬紅區邊界、提高自動化閾值）標記為紅區，需人工審批

---

## <a name="part6"></a>第六部分：可觀測性

> **分層狀態：Active Core + Deferred 擴展。** 與流水線成敗、審計完整性、gate 證據直接相關的指標屬於 active；Ops AI、TechRadar、主動感知儀表盤屬於 deferred。

> 審計日誌解決「發生了什麼」，可觀測性解決「正在發生什麼」。v3 在此基礎上加入主動感知層的可見性：Ops AI 的健康發現、TechRadar 掃描結果也納入統一 Dashboard。

### 6.1 實時監控指標

**流水線執行指標**（每次流水線完成後更新）：

```python
# observability/pipeline_metrics.py

PIPELINE_METRICS = {
    # 流水線整體
    "pipeline_total": "每個 feature 的流水線執行總次數",
    "pipeline_success_rate": "流水線成功率（滾動 7 天）",
    "pipeline_duration_p50_seconds": "流水線執行時間 p50",
    "pipeline_duration_p99_seconds": "流水線執行時間 p99",
    
    # Agent 執行
    "agent_latency_seconds": "各 Agent 階段的執行延遲（帶 agent 標籤）",
    "agent_token_consumed": "各 Agent 的 token 消耗（帶 agent + model 標籤）",
    "pipeline_trace_coverage_rate": "帶 trace_id 的流水線事件覆蓋率",
    "trace_to_pr_link_rate": "trace_id 成功關聯到 PR 的比例",
    "critic_confidence_score": "Critic AI 每次評分的分佈",
    "critic_iteration_rounds": "Spec → Critic 迭代輪數分佈",
    
    # 熔斷器
    "circuit_breaker_state": "各 feature 熔斷器狀態（0=CLOSED, 1=HALF_OPEN, 2=OPEN）",
    "circuit_breaker_triggered_total": "熔斷器觸發次數（累計）",
    
    # 部署
    "canary_error_rate": "Canary 版本的 error rate",
    "canary_latency_p99_ms": "Canary 版本的 p99 延遲",
    "rollback_total": "自動回滾次數（累計）",
    
    # 成本
    "gateway_cost_usd_total": "路由網關累計成本",
    "subscription_quota_utilization": "訂閱配額使用率（帶 tool 標籤）",
    
    # v3 主動感知指標（新增）
    "ops_ai_findings_total": "Ops AI 發現的問題總數（帶 severity 標籤）",
    "ops_ai_selfheal_success_rate": "Ops AI 自愈操作成功率",
    "techradar_advisories_pending": "TechRadar 待處理的安全公告數",
    "advisor_proposals_pending": "Advisor AI 待審批的提案數",
    "proactive_ops_cost_usd": "主動感知每月路由網關成本",
    "metrics_pipeline_lag_seconds": "metrics.jsonl 寫入到 Dashboard 聚合完成的延遲",
    "audit_backup_success_rate": "審計日誌備份成功率",
}
```

### 6.1.1 Source Of Truth（新增）

| 數據類型 | 唯一事實源 | 聚合頻率 | 缺失處理 |
| --- | --- | --- | --- |
| 流水線事件 | PostgreSQL `pipeline_audit` 表（fallback: `audit/ai-decisions.jsonl`） | 每次流水線完成後 | 缺失則標記 `pipeline_incomplete` |
| 熔斷器狀態 | PostgreSQL `pipeline_state` 表（fallback: `governance/circuit-breaker-state.json`） | 實時 | 讀取失敗視為 `OPEN` |
| Canary 指標 | `observability/metrics.jsonl` + APM 指標源 | 1 分鐘 | 樣本不足禁止自動放量 |
| 提案狀態 | PostgreSQL `pipeline_audit` 表 category='advisor-proposals'（fallback: JSONL） | 每 5 分鐘 | 不可解析記為 `invalid_proposal_record` |
| 備份狀態 | Supabase `audit_backup_runs` 表 | 每日 | 失敗立即 critical 告警 |

---

### 6.2 額度與成本追蹤

**訂閱額度**：Claude Code 的實際配額機制為動態限制，無法精確預測。流水線通過記錄限速事件（throttled / rate_limited）來感知配額壓力，而不是預設一個固定的 token 上限。

```yaml
# observability/quota_signals.yaml
# 基於行為信號而非硬編碼閾值
quota_signals:
  claude_code:
    source: audit/usage-tracking.jsonl
    alert_condition: "throttled_count >= 2 in current window"
    critical_condition: "quota_exhausted == true"
    action_on_alert: "Code AI 任務外溢到 Codex CLI"
    action_on_critical: "啟動降級策略（見 02-tools-cost.md §2.5）"
  
  gateway_calls:
    source: audit/usage-tracking.jsonl
    alert_condition: "month_to_date_usd > budget * 0.7"
    critical_condition: "month_to_date_usd > budget * 0.9"
    action_on_alert: "降低主動感知頻率"
    action_on_critical: "暫停非關鍵按量調用"
```

**按量成本**：流水線記錄每次路由網關調用的 `task_class` 和返回的 `usage.total_cost`。按模型維度的詳細成本分析是路由網關的職責。

---

### 6.3 異常告警規則

```yaml
# observability/alert_rules.yaml
alert_rules:

  # 流水線成功率異常
  - name: PipelineSuccessRateDrop
    condition: |
      rolling_7d_success_rate(feature_id) < 0.6
      AND pipeline_total_7d(feature_id) >= 5
    severity: warning
    message: "Feature {feature_id} 的流水線成功率過去 7 天低於 60%"
    action: include_in_daily_summary

  # 熔斷器觸發
  - name: CircuitBreakerTriggered
    condition: circuit_breaker_state(feature_id) == OPEN
    severity: critical
    message: "Feature {feature_id} 的熔斷器已觸發，流水線已降級為人工模式"
    runbook_url: "runbooks/circuit-breaker.md"
    action: immediate_notification + include_in_daily_summary

  # Canary 異常
  - name: CanaryErrorRateSpike
    condition: |
      canary_error_rate > baseline_error_rate + 0.01
      AND canary_duration_minutes >= 5
      AND canary_requests_total >= 1000
    severity: critical
    message: "Canary 版本 {pr_id} 的 error rate 超過基線 1%，觸發自動回滾"
    runbook_url: "runbooks/canary-rollback.md"
    action: trigger_rollback

  # Critic 置信度持續偏低
  - name: CriticScoreTrend
    condition: rolling_10_runs_avg_confidence(feature_id) < 75
    severity: warning
    message: "Feature {feature_id} 的 Critic AI 平均置信度持續偏低"
    action: include_in_daily_summary

  # 路由網關成本告警
  - name: GatewayCostAlert
    condition: gateway_month_to_date_usd > gateway_monthly_budget * 0.7
    severity: warning
    message: "路由網關月度成本已達預算 70%，預計將在本月末前耗盡"
    action: include_in_daily_summary

  # 訂閱配額緊張
  - name: QuotaCritical
    condition: subscription_quota_utilization(tool) >= 0.9
    severity: warning
    message: "{tool} 訂閱配額剩余不足 10%，已觸發智能降級"
    action: trigger_degradation_level_1 + include_in_daily_summary

  # v3 新增：Ops AI 高危發現
  - name: OpsAIHighSeverityFinding
    condition: ops_ai_finding.severity == "high"
    severity: critical
    message: "Ops AI 發現高危基礎設施問題：{finding.description}"
    runbook_url: "runbooks/ops-high-severity.md"
    action: immediate_notification + include_in_daily_summary

  # v3 新增：TechRadar 安全公告
  - name: TechRadarCriticalAdvisory
    condition: techradar_advisory.cvss_score >= 9.0
    severity: critical
    message: "依賴 {package} 存在 CVSS {cvss_score} 高危漏洞（{cve_id}），建議立即更新"
    runbook_url: "runbooks/security-advisory.md"
    action: immediate_notification + create_proposal

  # v3 新增：主動感知成本超支
  - name: ProactiveOpsCostAlert
    condition: proactive_ops_cost_usd_mtd > 8.0
    severity: warning
    message: "主動感知月度成本已達 $8，接近上限，降低掃描頻率"
    action: reduce_scan_frequency + include_in_daily_summary
```

### 6.3.1 告警治理（新增）

- 去重鍵：`alert_name + trace_id + artifact_id`
- 抑制窗口：同一去重鍵 `30 分鐘` 內只發 1 次即時通知
- 升級路由：
  - `warning`：每日摘要
  - `critical`：即時通知 + 值班路由
  - `critical` 連續 3 次未確認：升級到人工審批頻道
- 每條 critical 告警必須關聯 `runbook_url`
- 沒有 `runbook_url` 的新告警規則不得上線

### 6.3.2 可觀測性自身健康（新增）

- `metrics.jsonl` 10 分鐘未更新：critical
- Dashboard 聚合延遲 > 15 分鐘：warning
- `audit/*.jsonl` 每日備份失敗：critical
- trace 覆蓋率 < 99%：warning；< 95%：critical

---

### 6.4 Dashboard 設計（v3 擴展版）

Dashboard 基於本地 Grafana 實例構建，數據源為 PostgreSQL（流水線審計表）。設計遵循「5 分鐘早晨檢查」的使用場景——人每天只看一次，必須在一眼內看出系統狀態。

**Dashboard 區塊佈局（v3）**：

```
┌─────────────────────────────────────────────────────────────────┐
│  AI 流水線狀態 Dashboard — 2026-04-05                            │
├──────────────┬──────────────┬──────────────┬────────────────────┤
│ 今日流水線   │ 成功率（7d） │ 待處理人工   │ 熔斷器狀態        │
│   12 次      │   91.7%      │   2 項       │  全部 CLOSED      │
│ ✅ 11 成功  │ ▲ +3.2%     │ ⚠ 紅區審批  │                   │
│ ❌ 1 失敗   │              │ 📋 採購提案  │                   │
├──────────────┴──────────────┴──────────────┴────────────────────┤
│  各 Feature 流水線成功率（滾動 7 天）                             │
│  payment    ████████████████████░░░░  85.7%  [CLOSED]          │
│  user-auth  ████████████████████████  100%   [CLOSED]          │
│  billing    ██████████████░░░░░░░░░░  58.3%  [OPEN ⚠]         │
│  analytics  ███████████████████████░  95.2%  [CLOSED]          │
├──────────────────────────────────────────────────────────────────┤
│  🔍 主動感知狀態（v3 新增）                                        │
│  Ops AI 上次巡檢：15 分鐘前  發現：2 低危，0 高危  自愈：1 次    │
│  TechRadar 上次掃描：3 天前  待處理公告：2 個（均為低危）         │
│  Advisor AI 待審提案：1 個（依賴替換建議）                        │
├──────────────────────────────────────────────────────────────────┤
│  Agent 延遲 P50 / P99（今日）                                    │
│  Spec AI    2.1s / 8.4s    Critic AI   4.2s / 12.1s           │
│  Code AI    18.4s / 45.2s  Test AI     31.2s / 78.5s           │
│  Security   3.2s / 9.8s    Total       62.1s / 154.2s          │
├──────────────────────────────────────────────────────────────────┤
│  成本概覽（本月至今）                                             │
│  Claude Code（訂閱）  $20.00 固定  利用率 72%                  │
│  Codex CLI（訂閱）    $20.00 固定  利用率 48%                  │
│  路由網關（執行）     $18.40 / $50 預算  ▓▓▓▓▓▓▓░░░ 36%      │
│  路由網關（感知）     $3.80 / $8 預算    ▓▓▓▓▓░░░░░ 47%       │
│  合計                 $62.20 / $100 預計                        │
└──────────────────────────────────────────────────────────────────┘
```

**每日異常摘要格式（v3 擴展）**：

```markdown
# AI 流水線 · 每日摘要 · 2026-04-05

## 需要你處理的事項（2 項）

### ⚠ 紅區審批
- Feature: billing/payment-retry
- 觸發原因: Security AI 檢測到支付邏輯變更
- 操作: [查看報告] [批准] [拒絕]
- 截止: 24 小時內

### 📋 Advisor AI 採購提案
- 類型: 依賴替換建議
- 內容: 建議將 node-cron 替換為 croner（性能提升 40%，活躍維護）
- 數據: [查看完整比較報告]
- 操作: [批准替換] [拒絕] [延後 7 天]

## 系統狀態
- 今日流水線：12 次（11 成功，1 失敗）
- billing feature 熔斷器已觸發（連續 3 次失敗）→ 需要排查

## 主動感知摘要（v3 新增）
- Ops AI 今日自愈：1 次（清理 Redis 緩存積壓，恢復響應時間）
- TechRadar：2 個依賴有新版本，均為低危，已生成自動更新 PR
- 容量預測：payment 服務在當前增長趨勢下，預計 3 週後達到 CPU 限制

## 本週趨勢
- 整體成功率：91.7%（上週 88.5%）↑
- Critic 平均置信度：87.3（上週 85.1）↑
- 路由網關本月成本：$22.20（預算 $58）正常

## 無需處理的事項（已自動完成）
- ✅ 3 個綠區 PR 自動合並
- ✅ 1 個 Canary 部署成功
- ✅ 2 個依賴 patch 版本安全更新（Ops AI 自動執行）
- ✅ 週度 TechRadar 掃描完畢（無高危發現）
```

---

### 6.5 通知適配層（v3 新增）

審計日誌和 Dashboard 解決「事後查看」和「主動查看」，但 critical 事件需要**即時觸達人類**。通知適配層提供統一的即時推送接口。

```python
# observability/notifier.py

import json
import logging
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class NotificationChannel(Enum):
    CRITICAL = "critical"     # 熔斷器、Canary 回滾、CVSS >= 9.0
    WARNING = "warning"       # 成本告警、健康度下降
    INFO = "info"             # 每日摘要、TechRadar 週報


# ── 適配器配置（優先使用第一個可用的管道）───────────
ADAPTERS = [
    {
        "type": "github_issue",
        "channels": ["critical", "warning"],
        "config": {
            "repo": "{owner}/{repo}",
            "labels": {"critical": ["P0", "ai-escalation"], "warning": ["P1", "ai-alert"]},
        },
    },
    {
        "type": "slack_webhook",
        "channels": ["critical"],
        "config": {
            "webhook_url": "$SLACK_WEBHOOK_URL",  # 從環境變量讀取
        },
    },
    {
        "type": "email",
        "channels": ["critical"],
        "config": {
            "to": "$ALERT_EMAIL",
            "via": "github_notifications",  # 利用 GitHub Issue 的 Email 訂閱
        },
    },
]


def _push_notification(channel: str, title: str, body: str, metadata: dict[str, Any] | None = None):
    """
    統一通知推送。嘗試所有已配置的適配器，至少有一個成功即可。
    失敗時不拋異常（通知失敗不應影響主流程），但記錄到日誌。
    """
    for adapter in ADAPTERS:
        if channel not in adapter["channels"]:
            continue
        try:
            if adapter["type"] == "github_issue":
                _send_github_issue(title, body, adapter["config"], channel)
            elif adapter["type"] == "slack_webhook":
                _send_slack(title, body, adapter["config"])
            logger.info(f"通知已推送 [{adapter['type']}]:{title}")
        except Exception as e:
            logger.warning(f"通知推送失敗 [{adapter['type']}]:{e}")


def _send_github_issue(title: str, body: str, config: dict, channel: str):
    """GitHub Issue 作為主要通知管道（免費 + 自帶 Email 通知）。"""
    import os
    token = os.environ.get("GITHUB_TOKEN", "")
    repo = config["repo"]
    labels = config["labels"].get(channel, [])
    httpx.post(
        f"https://api.github.com/repos/{repo}/issues",
        headers={"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"},
        json={"title": title, "body": body, "labels": labels},
        timeout=10.0,
    )


def _send_slack(title: str, body: str, config: dict):
    """Slack Webhook 推送（可選）。"""
    import os
    url = os.environ.get("SLACK_WEBHOOK_URL", config.get("webhook_url", ""))
    if not url or url.startswith("$"):
        return
    httpx.post(url, json={"text": f"*{title}*\n{body}"}, timeout=10.0)
```

**觸發即時通知的事件**：

| 事件 | 管道 | 原因 |
|------|--------|------|
| 熔斷器觸發 | critical | 流水線已降級為人工，需立即排查 |
| Canary 自動回滾 | critical | 生產異常，需人工根因分析 |
| TechRadar CVSS >= 9.0 | critical | 緊急安全漏洞 |
| Ops AI 高危發現 | critical | 基礎設施可能立即影響服務 |
| 成本超支 | warning | 需人工決策是否繼續 |
| 健康度 < 60 | warning | Feature 已凍結新功能 |
| 每日異常摘要 | info | 常規摘要，不緊急 |

---

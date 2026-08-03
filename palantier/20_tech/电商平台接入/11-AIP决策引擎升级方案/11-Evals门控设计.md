# Evals 门控设计 — 技能成功率评估、验证循环编排、发布门控

> 创建时间：2026-07-29
> 状态：方案设计（先方案后编码）
> 关联：`01-Plan-Mode与TAOR循环设计.md` §六（Verification Loops）· `02-私域管家技能编排.md` 等 5 份数字同事技能编排 · `../13-FDE技能编排方案/04-Reflection自审节点设计.md`
> 参考：Claude Blog — Building verification loops in Claude Code with skills（四种触发模式、Chained Verification）

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 先方案后编码 | 本文档为方案层 |
| 最小更改 | 复用 01 文档已有 Verify 阶段实现，不重写 TAOR 循环；复用 Reflection 规则，不重复造轮子 |
| 不影响现有功能 | Evals 门控为独立模块，未通过门控的技能可通过配置降级为"告警不阻断"，不阻断已有 mock 流程 |
| 自测验证 | 每条 eval 规则需有正反向测试用例 |

---

## 一、问题诊断

### 1.1 现状痛点

`01-Plan-Mode与TAOR循环设计.md` §六 已定义 Verification Loop 机制和四类触发模式，`02-私域管家技能编排.md` ～ `08-数据参谋技能编排.md` 数字同事和 `../13-FDE技能编排方案/04-Reflection自审节点设计.md` FDE 也各自定义了 Verification / Reflection 规则，但存在以下缺口：

| 痛点 | 影响 |
|------|------|
| 无**发布门控** | 新技能上线后失败 40% 才发现（没有上线前的 eval 通过率门槛） |
| 无**成功率看板** | 私域管家话术成功率到底 70% 还是 95%？没有可量化的 metric |
| 无**回归保护** | 改了导购顾问的成分分析逻辑，不知道客服专员会不会受影响 |
| 各技能**验证规则分散** | 私域管家/导购顾问/内容官/FDE 各自的验证规则写在各自文档里，没有集中管理 |
| 无**基线对比** | 模型路由从 private-medium 升级到 private-large，成功率升了还是降了？ |

### 1.2 目标：三层门控

```
┌──────────────────────────────────────────────────────┐
│ Layer 3：发布门控（Release Gate）                     │
│   新技能/模型上线前必须通过 Eval 集，通过率 ≥ 阈值     │
├──────────────────────────────────────────────────────┤
│ Layer 2：运行门控（Runtime Gate）                     │
│   每次 TAOR 循环 Act 后走 Verification Loop           │
│   （复用 01 文档 §六 已有的 Verify 阶段实现）          │
├──────────────────────────────────────────────────────┤
│ Layer 1：Eval 资产层（Asset Layer）                   │
│   集中管理的 Eval 用例库、验证技能定义、metric 看板    │
└──────────────────────────────────────────────────────┘
```

### 1.3 与 Verification Loop / Reflection 的关系

| 概念 | 定义 | 所在层 | 执行时机 |
|------|------|--------|---------|
| **Reflection** | 单步自审（硬规则 + LLM 软判断） | TAOR 内部 | 每轮 Act 后即时执行 |
| **Verification Loop** | 可编排的验证技能链（多技能串联） | TAOR 内部（Verify 阶段） | 每轮 Act 后执行 1-N 个验证技能 |
| **Evals 门控** | 发布 + 运行 + 回归三层门控 + 资产层 | 跨模块（Eval Engine） | ① 上线前跑 eval 集 ② 运行时按策略采样 ③ 回归每夜跑 |

简单说：
- **Reflection** = 单步自检（FDE 04 文档已有 26 条）
- **Verification Loop** = 一组 Reflection 串成链（01 文档 §六 已有实现）
- **Evals 门控** = 管理这些 Reflection/Verification 的**资产库** + **发布门槛** + **成功率看板** + **回归保护**

---

## 二、Eval 资产库（Layer 1）

### 2.1 Eval 用例数据模型

```python
# aip_eval_assets.py（新增）

class EvalCase(BaseModel):
    """单个 Eval 用例。"""
    id: str                          # 如 "ec-private-butler-001"
    name: str                        # "话术长度不超过30字"
    category: str                    # "private_butler" | "shopping_advisor" | ...
    skill_id: str                    # 对应的技能 ID
    priority: str                    # "smoke"（必跑） | "regression"（回归） | "edge"（边缘）

    # 输入
    input: dict                      # 模拟输入
    context: dict = {}               # 上下文（如客户画像、历史记录）

    # 期望输出
    expected: EvalExpectedOutput

    # 评估器（如何判断通过/失败）
    evaluator: EvalEvaluator

    # 元数据
    owner: str                       # 负责人
    created_at: float
    last_pass_rate: float = 0.0
    last_run_at: float | None = None


class EvalExpectedOutput(BaseModel):
    """期望输出（支持多种断言方式）。"""
    # 精确匹配（适合硬规则）
    exact_fields: dict = {}           # 如 {"script_length": {"$lte": 30}}

    # 语义匹配（适合 LLM 判断）
    semantic_assertions: list[str] = []  # 如 ["提到了具体产品名"]

    # 自定义函数（适合复杂逻辑）
    custom_assert_func: str | None = None  # 如 "assert_ingredient_compat(output, context)"


class EvalEvaluator(BaseModel):
    """评估器定义。"""
    type: str                      # "rule_based" | "llm_judge" | "hybrid"
    rules: list[EvalRule] = []     # 规则评估器（rule_based / hybrid）
    llm_judge_config: LLMJudgeConfig | None = None  # LLM 评审配置
```

### 2.2 电商 6 数字同事的 Eval 用例示例

#### 私域管家（private_butler）

```python
PRIVATE_BUTLER_EVALS = [
    # Smoke（上线必跑）
    EvalCase(
        id="ec-pb-smoke-001",
        name="话术长度≤30字且包含产品名",
        category="private_butler",
        skill_id="private_butler_s1_onboarding",
        priority="smoke",
        input={"customer_id": "c-001", "action": "生成破冰话术"},
        context={
            "customer": {"segment": "高价值客户", "recent_purchase": "SKU-A 防晒霜"},
            "product_catalog": [{"name": "SKU-A 防晒霜", "price": 199}]
        },
        expected=EvalExpectedOutput(
            exact_fields={"length": {"$lte": 30}},
            semantic_assertions=["提到 SKU-A 防晒霜 或 相关产品"]
        ),
        evaluator=EvalEvaluator(type="hybrid")
    ),
    EvalCase(
        id="ec-pb-smoke-002",
        name="话术不含敏感词",
        category="private_butler",
        priority="smoke",
        input={"customer_id": "c-002", "action": "生成跟进话术"},
        expected=EvalExpectedOutput(
            custom_assert_func="assert_no_sensitive_words(output)"
        ),
        evaluator=EvalEvaluator(type="rule_based")
    ),
    # Regression（回归集）
    EvalCase(
        id="ec-pb-reg-001",
        name="分层标签准确（高价值客户→VIP）",
        category="private_butler",
        priority="regression",
        input={"customer_id": "c-003", "action": "打客户分层标签"},
        context={"customer": {"total_spent": 50000, "order_count": 35}},
        expected=EvalExpectedOutput(
            exact_fields={"segment": {"$eq": "VIP"}}
        ),
        evaluator=EvalEvaluator(type="rule_based")
    ),
    # Edge（边缘）
    EvalCase(
        id="ec-pb-edge-001",
        name="客户历史为空时生成默认话术",
        category="private_butler",
        priority="edge",
        input={"customer_id": "c-new", "action": "生成破冰话术"},
        context={"customer": {}},
        expected=EvalExpectedOutput(
            semantic_assertions=["不提到具体历史购买产品，用通用问候"]
        ),
        evaluator=EvalEvaluator(type="llm_judge")
    ),
]
```

#### 导购顾问（shopping_advisor）

```python
SHOPPING_ADVISOR_EVALS = [
    EvalCase(
        id="ec-sa-smoke-001",
        name="成分兼容性检查（敏感肌→不含酒精）",
        category="shopping_advisor",
        priority="smoke",
        input={"action": "生成产品推荐", "customer_skin_type": "敏感肌"},
        context={
            "candidates": [
                {"name": "产品X", "ingredients": ["酒精", "烟酰胺"]},
                {"name": "产品Y", "ingredients": ["神经酰胺", "玻尿酸"]},
            ]
        },
        expected=EvalExpectedOutput(
            custom_assert_func="assert_no_alcohol_ingredient(output, '敏感肌')"
        ),
        evaluator=EvalEvaluator(type="hybrid")
    ),
    EvalCase(
        id="ec-sa-smoke-002",
        name="不做虚假宣传（禁止'根治'表述）",
        category="shopping_advisor",
        priority="smoke",
        input={"action": "生成产品推荐话术"},
        expected=EvalExpectedOutput(
            custom_assert_func="assert_no_false_advertising(output)"
        ),
        evaluator=EvalEvaluator(type="rule_based")
    ),
]
```

#### 内容官、客服专员、活动策划师、数据参谋、FDE 的 Eval 用例

结构同上，具体断言不同。总计约 **60+ 条 Smoke + 200+ 条 Regression + 60+ 条 Edge**。

### 2.3 Eval 资产库集中管理

```
【新增模块】aip_eval_assets.py
    ├── EVAL_CASES_REGISTRY  ← 所有 EvalCase 集中注册
    ├── VERIFY_SKILLS_REGISTRY  ← 所有 Verification 技能集中注册（从各文档同步）
    └── REFLECTION_RULES_REGISTRY ← 所有 Reflection 规则集中注册（从各文档同步）
```

**集中注册的收益**：
- 改一条 eval，不用搜 8 个文档
- 发布前跑 Smoke 集，自动拉取所有 category 的 smoke priority 用例
- 回归夜跑自动拉取 regression + edge 用例

---

## 三、运行门控（Layer 2 — 复用 01 文档 Verify 阶段）

### 3.1 四种触发模式的具体实现

Claude Blog 定义四种触发模式，本文档具体落地到电商场景：

| 模式 | 触发时机 | 谁触发 | 电商场景对应 |
|------|---------|-------|------------|
| **Standalone** | 用户手动 | 用户点击"合规检查"按钮 | 客情维护平台区域三的"合规 30/30"检查 |
| **Embedded** | 生产技能结束后自动 | TAOR Verify 阶段 | 私域管家生成话术后自动走话术 3 项检查 |
| **Chained** | 一个验证技能调用下一个 | Eval Engine 编排 | 私域话术 → 长度检查 → 敏感词检查 → 个性化检查 → 全通过交付 |
| **On every PR / Config Change** | 配置变更/技能上线 | CI/CD 或 配置变更 Hook | 改了 Ontology 字段映射，自动跑 FDE eval 集 |

### 3.2 Embedded 模式 — TAOR Verify 阶段

`01 文档 §6.2` 已定义 TAOR 循环升级为 `Think → Act → Verify → Observe`，运行门控就是这个 Verify 阶段，**不重复实现**。本文档补充：

#### 运行采样策略（避免每跑都 eval 拖慢 20%）

```python
class RuntimeEvalSampler:
    """运行时 eval 采样器。

    每次请求都 eval 会增加 10-30% 耗时，按策略采样：
    - P0 技能：100% 采样
    - P1 技能：20% 采样 + 100% 首 N 条（冷启动期）
    - P2 技能：5% 采样
    - 人工投诉的 skill_id：100% 采样 24h
    """

    SAMPLING_STRATEGY = {
        "private_butler": {"rate": 1.0},                    # 私域管家：100%
        "shopping_advisor": {"rate": 1.0},                   # 导购顾问：100%
        "content_officer": {"rate": 0.2, "cold_heads": 100},  # 内容官：20%+冷启动100条全跑
        "service_agent": {"rate": 1.0},                       # 客服：100%
        "event_planner": {"rate": 0.2, "cold_heads": 50},     # 活动策划：20%
        "data_advisor": {"rate": 0.2},                         # 数据参谋：20%
        "fde_ingestion": {"rate": 1.0},                        # FDE：100%（接入链路关键）
    }

    COMPLAINT_SAMPLE_BOOST = {
        # 被人工投诉的 skill_id：24h 内 100% 采样
        "ttl_seconds": 86400,
        "rate": 1.0,
    }
```

#### 运行时验证失败的处理

```python
class RuntimeEvalFailureHandler:
    """运行时 eval 失败的处理策略。"""

    # 严重度 → 处理动作
    SEVERITY_MATRIX = {
        # 致命（合规/安全）→ 阻断交付，转人工
        "critical": {
            "block_delivery": True,
            "alert_channels": ["oncall", "user_confirm"],
            "auto_fix": False,
            "record_incident": True,
        },
        # 高（质量）→ 自动修复最多 3 次，失败转人工
        "high": {
            "block_delivery": True,
            "alert_channels": ["metric_dashboard"],
            "auto_fix": True,
            "max_fix_retries": 3,
        },
        # 中（体验）→ 不阻断，但告警
        "medium": {
            "block_delivery": False,
            "alert_channels": ["metric_dashboard"],
            "auto_fix": True,
            "max_fix_retries": 2,
            "record_incident": False,
        },
        # 低（统计）→ 仅记录 metric
        "low": {
            "block_delivery": False,
            "alert_channels": [],
            "auto_fix": False,
        },
    }
```

### 3.3 Standalone 模式 — 手动触发

```
客情维护平台区域三（产品面板）
    │
    ├─ 合规检查按钮  ← 点击后跑 ec-pb-smoke-001~002 + 自定义用例
    │
    └─ 成分审查按钮  ← 点击后跑导购顾问的 ec-sa-smoke-001（成分兼容）
```

API：
```
POST /v1/aip/evals/run
Body: {
    "mode": "standalone",
    "eval_case_ids": ["ec-pb-smoke-001", "ec-pb-smoke-002"],
    "inputs": {...},  # 手动跑的输入
    "context": {...},
}
→ 返回每条用例的 pass/fail + 失败原因 + 建议修复
```

### 3.4 Chained 模式 — 验证链完整流程

```
私域管家 S1：客户沉淀
  │
  ├─ Act：生成 500 位客户的分层标签 + 破冰话术
  │
  ▼ Verify（Chained 验证链）
  ├─ 验证 1：标签一致性（同分层客户的 RFM 特征应相近）
  │   ├─ pass → 下一验证
  │   └─ fail → 自动修复：重跑异常值过滤
  │
  ├─ 验证 2：话术 3 项检查（长度≤30 + 敏感词 + 提到产品名）
  │   ├─ pass → 下一验证
  │   └─ fail（敏感词）→ 自动修复：替换敏感词 + 重新生成
  │
  ├─ 验证 3：个性化匹配（高价值客户话术应提到具体产品+VIP权益）
  │   ├─ pass → 交付
  │   └─ fail → 严重度 medium → 不阻断，仅告警（个性化体验问题，不影响合规）
  │
  └─ 验证全部通过 → Observe 记录成功率
```

### 3.5 On every PR / Config Change 模式

```
触发事件：
  ├─ 1. 技能 prompt 变更（Git PR）
  ├─ 2. 模型路由切换（medium → large）
  ├─ 3. Ontology 字段映射变更
  ├─ 4. Reflection / Verification 规则变更
  └─ 5. Guardrail / 权限防线规则变更

自动动作：
  1. 拉取 affected 技能对应的 Smoke Eval 集
  2. 批量执行（并行度可配，默认 5）
  3. 输出通过率报告：
     ├─ 通过率 ≥ 95% → 允许变更
     ├─ 通过率 85-95% → 告警 + 需要负责人审批
     └─ 通过率 < 85% → 阻断变更，附带 top-10 失败样例
```

---

## 四、发布门控（Layer 3 — Release Gate）

### 4.1 上线三阶段 + Evals 门槛

| 阶段 | 说明 | Eval 要求 |
|------|------|----------|
| **Canary（金丝雀）** | 1% 流量 / 指定测试商家 | Smoke 集通过率 ≥ 95% |
| **Gradual（逐步放量）** | 5% → 20% → 50% → 100% | ① Smoke ≥ 98% ② Regression ≥ 90% ③ 运行门控成功率（7 天滑窗）稳定 |
| **Full（全量）** | 全量商家 | ①②③ + ④ 无 P0 incident 连续 7 天 |

### 4.2 Eval 基线与对比

```python
class EvalBaseline(BaseModel):
    """Eval 基线（每版本/模型/配置一套）。"""
    id: str
    label: str                     # "v1.2 / private-medium / 默认 prompt"
    created_at: float

    # 各技能的通过率基线
    skill_pass_rates: dict[str, float]
    # 各 Eval Category 的通过率基线
    category_pass_rates: dict[str, float]
    # 全局通过率
    global_pass_rate: float

    # 关联的配置快照（用于对比）
    config_snapshot: dict = {}     # 模型路由 + prompt 版本 + 规则版本
    model_snapshot: dict = {}      # 使用的模型：private-medium / large / ...
    ontology_snapshot: dict = {}   # Ontology schema version


class EvalBaselineComparator:
    """基线对比器。"""

    def compare(self, current_run: EvalRunResult, baseline: EvalBaseline) -> BaselineDiff:
        """当前运行结果 vs 基线。"""
        degraded_skills = []
        for skill_id, rate in current_run.skill_pass_rates.items():
            baseline_rate = baseline.skill_pass_rates.get(skill_id, 0)
            if rate < baseline_rate - 0.05:  # 掉 5% 视为劣化
                degraded_skills.append({
                    "skill_id": skill_id,
                    "baseline": baseline_rate,
                    "current": rate,
                    "delta": rate - baseline_rate
                })

        return BaselineDiff(
            is_regression=len(degraded_skills) > 0,
            degraded_skills=degraded_skills,
            # ...
        )
```

### 4.3 发布审批流程

```
技能/模型/配置变更提交
        │
        ▼
自动跑 Smoke Eval 集（P0 必跑）
        │
        ├─ 通过率 ≥ 95% ──→ 通过，进入 Canary
        │
        ├─ 85-95% ────────→ 生成降级报告 → 负责人审批（可放行可驳回）
        │
        └─ < 85% ─────────→ 阻断变更，附 top-10 失败样例
```

---

## 五、成功率 Metric 看板

### 5.1 核心指标体系

```
【全局指标】
  ├─ global_skill_success_rate     全局技能成功率（所有 skill × 所有请求）
  ├─ global_eval_pass_rate         全局 Eval 通过率（所有 eval 用例 × 所有运行）
  └─ critical_failure_rate         严重失败率（critical 级别 / 总请求）

【按技能维度】
  private_butler_success_rate      私域管家 5 技能的各成功率 + 总体
  shopping_advisor_success_rate    导购顾问 6 技能的各成功率
  content_officer_success_rate     ...
  service_agent_success_rate       ...
  event_planner_success_rate       ...
  data_advisor_success_rate        ...
  fde_ingestion_success_rate       FDE 6 步接入的各步成功率

【按严重度维度】
  critical_failure_count           24h 内严重失败数
  high_failure_count               24h 内高严重度失败数
  medium_failure_count             24h 内中严重度失败数

【按验证类型】
  reflection_pass_rate             单步自审通过率（26 条 FDE + 各数字同事的）
  verification_chain_pass_rate     Verification 链整体通过率

【发布门控】
  smoke_eval_pass_rate             Smoke 用例集通过率（最新一次 run）
  regression_eval_pass_rate        Regression 用例集通过率（每夜跑结果）
  baseline_comparison              当前版本 vs 基线是否劣化
```

### 5.2 数据采集与存储

```python
# aip_eval_metrics.py（新增）

class EvalMetricCollector:
    """Eval metric 收集器。"""

    # 写入时序数据库（InfluxDB / VictoriaMetrics）
    def record_skill_result(self, skill_id: str, passed: bool, severity: str, duration_ms: int):
        metric = {
            "measurement": "aip_skill_result",
            "tags": {"skill_id": skill_id, "severity": severity, "model": current_model()},
            "fields": {"passed": int(passed), "duration_ms": duration_ms},
        }
        self._tsdb.write(metric)

    def record_eval_run(self, eval_case_id: str, passed: bool, category: str, priority: str):
        metric = {
            "measurement": "aip_eval_run",
            "tags": {
                "eval_case_id": eval_case_id,
                "category": category,
                "priority": priority,
                "mode": current_run_mode(),  # standalone / embedded / chained / pr
            },
            "fields": {"passed": int(passed)},
        }
        self._tsdb.write(metric)
```

**最小更改原则**：不改现有 Observability 前端代码，Metric 数据通过现有 `ObservabilityPage` 后端新增数据源接入。

### 5.3 与决策谱系 / 可观测性页面的对接

13-FDE 02 文档提到 Checkpoint 和回滚会在 `ObservabilityPage` 展示。Evals metric 也接入同一页面：

```
ObservabilityPage（已有的页面，不改 UI 结构，新增 Tab）
    ├─ 运行历史 Tab（已有）
    ├─ Trace 详情（已有）
    ├─ Metric 看板（已有，接 mock 数据 → 改为接真实 metric）
    │     └─ 新增卡片组：Evals 成功率（按技能/严重度/验证类型）
    └─ Evals 报告 Tab（新增，轻量实现）
          ├─ 最近一次 Smoke Eval 运行结果
          ├─ 最近一次 Regression Eval 运行结果
          ├─ 基线对比（当前 vs 上一版本）
          └─ Top-10 失败用例（一键看详情 + 跳转修复）
```

---

## 六、LLM Judge 配置（Hybrid Evaluator）

### 6.1 何时用 LLM Judge

| 评估场景 | 适合评估器 | 说明 |
|---------|-----------|------|
| 长度检查 / 敏感词 / 枚举值匹配 | Rule-based | 100% 准确，毫秒级，零成本 |
| "提到产品名" / "语气友好" 等语义判断 | LLM Judge | 规则写不清，交给 LLM |
| 成分兼容 / 肤质匹配等有知识库支撑 | Hybrid（规则+LLM） | 先规则查成分库，再 LLM 确认兜底 |
| "品牌调性是否匹配"等主观判断 | LLM Judge + 人工双审 | LLM 过一遍，人工抽检 10% |

### 6.2 LLM Judge Prompt 设计（极简原则）

参考 Claude Blog "删掉 80% System Prompt" 原则，不给冗长规则，给边界 + 判断接口：

```python
LLM_JUDGE_PROMPT_TEMPLATE = """
你是质量评审员。根据以下信息判断是否通过：

【断言】{assertion}
【实际输出】{actual_output}
【上下文】{context_summary}

请输出 JSON：
{{
  "passed": true/false,
  "confidence": 0.0-1.0,
  "reason": "一句话说明",
  "suggestion": "不通过时，给出修复建议"
}}

判断边界：
1. 涉及合规/安全的默认不过（宁严勿松）
2. 涉及体验/语义相近的默认宽容通过
3. 不确定的给 passed=false + confidence=低，不阻断但触发人工抽检
"""
```

---

## 七、新增模块清单 + 与现有代码对接

### 7.1 新增模块

| 模块 | 路径 | 职责 | 来源章节 |
|------|------|------|---------|
| `aip_eval_assets.py` | `aos-platform-w4/services/aos-api/aos_api/` | EvalCase + VerifySkill + ReflectionRule 集中注册 | §2 |
| `aip_eval_engine.py` | 同上 | Eval Engine（四类触发模式 + 采样器 + 失败处理） | §3 |
| `aip_eval_release_gate.py` | 同上 | 发布门控 + 基线对比 + 审批流程 | §4 |
| `aip_eval_metrics.py` | 同上 | Metric 收集器 + TSDB 写入 | §5 |
| `aip_eval_llm_judge.py` | 同上 | LLM Judge（极简 Prompt） | §6 |
| `routers/phase3_aip_evals.py` | `aos-platform-w4/services/aos-api/aos_api/routers/` | Evals API（run/report/baseline/compare） | §3.2/3.3 |

### 7.2 对接现有代码（最小更改，零修改现有核心逻辑）

| 新增模块 | 对接的现有代码 | 对接方式 |
|---------|-------------|---------|
| `aip_eval_engine.py` | `aip_taor_loop.py::TAORLoopController._verify()` | 不重写，通过 `register_eval_engine()` 注入 Verify 阶段的具体实现 |
| `aip_eval_engine.py` | 各数字同事技能编排中的 Reflection 规则 | 通过 `REFLECTION_RULES_REGISTRY` 同步，不修改原技能定义 |
| `aip_eval_metrics.py` | `ObservabilityPage` 后端 metric 端点 | 新增数据源，不改前端 |
| `aip_eval_release_gate.py` | `DraftInboxPage`（已有 Draft 审批机制） | 发布门控审批走 Draft 引擎的审批链路，不新建审批系统 |
| `aip_eval_llm_judge.py` | `aip_llm_adapter.py`（AIP 层已有） | 复用 LLM Adapter，不新建模型调用链路 |

**零修改的现有核心模块**：
- `aip_logic_engine.py` — 仅通过 `register_eval_engine` 注册
- `aip_taor_loop.py` — `_verify()` 定义不变，注入实现
- `aip_permission_gate.py` — 不改，Eval 失败处理走自己的 SEVERITY_MATRIX
- `aip_drafts_engine.py` — 不改，复用其审批状态机
- 各数字同事的 SkillTemplate（02-08 文档定义）— 不改，Eval 用例通过 skill_id 关联

---

## 八、测试方案与验收标准

### 8.1 自动化测试

```python
# tests/test_aip_evals.py

class TestAIPEvals:

    def test_smoke_eval_run_all_pass(self, eval_engine, sample_context):
        """Smoke 集全过。"""
        result = eval_engine.run(
            category="private_butler",
            priority="smoke",
            context=sample_context
        )
        assert result.pass_rate >= 0.95

    def test_sensitive_words_failure_block(self, eval_engine):
        """含敏感词的输出被 critical 级阻断。"""
        result = eval_engine.run_single(
            eval_case_id="ec-pb-smoke-002",
            inputs={"script": "xx违禁词xxx"}
        )
        assert result.passed == False
        assert result.severity == "high"
        assert result.block_delivery == True

    def test_llm_judge_semantic_assert(self, eval_engine, mock_llm):
        """LLM Judge 语义判断。"""
        mock_llm.set_response({"passed": True, "confidence": 0.9})
        result = eval_engine.run_single("ec-pb-edge-001", inputs={...})
        assert result.passed == True

    def test_release_gate_95_threshold(self, release_gate, baseline):
        """发布门控 95% 门槛。"""
        run_result = EvalRunResult(global_pass_rate=0.96)
        assert release_gate.approve(run_result, baseline).allowed == True

        run_result2 = EvalRunResult(global_pass_rate=0.80)
        decision = release_gate.approve(run_result2, baseline)
        assert decision.allowed == False
        assert decision.block_reason == "smoke_pass_rate_below_threshold"

    def test_baseline_degradation_detected(self, baseline_comparator):
        """基线劣化检测。"""
        current = {"private_butler": 0.85}
        baseline = {"private_butler": 0.95}
        diff = baseline_comparator.compare(current, baseline)
        assert diff.is_regression == True
        assert "private_butler" in diff.degraded_skills

    def test_sampling_strategy_p0_100pct(self, sampler):
        """P0 技能 100% 采样。"""
        for _ in range(100):
            assert sampler.should_sample("private_butler") == True

    def test_runtime_failure_auto_fix(self, eval_engine, mock_skill):
        """运行时 eval 失败自动修复。"""
        mock_skill.set_fail_then_pass(times=2)
        result = eval_engine.run_embedded("private_butler_s1", mock_skill)
        assert result.auto_fix_count == 2
        assert result.final_pass == True
```

### 8.2 验收标准（可追溯）

**§2 Eval 资产层**：
- [ ] 6 数字同事 + FDE 的 Eval 用例全部注册到 `EVAL_CASES_REGISTRY`（Smoke ≥ 10 条/类）
- [ ] 各技能的 Reflection / Verification 规则同步到 REGISTRY

**§3 运行门控**：
- [ ] Embedded 模式：TAOR Verify 阶段执行验证，四种严重度按 SEVERITY_MATRIX 处理
- [ ] Embedded 采样：私域管家/导购/客服/FDE 100%，内容官 20%，与策略一致
- [ ] Standalone 模式：`POST /v1/aip/evals/run` 可用，返回 pass/fail + 原因
- [ ] Chained 模式：验证失败 auto_fix 最多 3 次，正确重试
- [ ] On Config Change 模式：映射规则变更触发 FDE eval 自动跑

**§4 发布门控**：
- [ ] Smoke 通过率 ≥ 95% 允许变更，< 85% 阻断
- [ ] 基线劣化（掉 5%+）被检测到，附劣化详情
- [ ] 发布审批流程走 Draft 引擎（复用现有 UI）

**§5 Metric 看板**：
- [ ] 24h 内按技能的成功率曲线可用
- [ ] 最近一次 Smoke / Regression Eval 报告可查
- [ ] Top-10 失败用例清单可查

**§6 LLM Judge**：
- [ ] 语义断言正确走 LLM Judge，规则断言不走（省 Token）
- [ ] LLM Judge Prompt 极简（≤ 150 字）+ 边界明确

**通用**：
- [ ] `pytest tests/test_aip_evals.py` 全绿
- [ ] 未开启 Evals 时，现有 mock 流程完全不受影响（降级开关）
- [ ] 新增模块零修改现有 8 个核心引擎代码

---

## 九、关键设计决策

| # | 决策 | Why | 影响 |
|---|------|-----|------|
| 1 | **Reflection = 单步自审，Verification = 技能链，Evals = 资产+门控+看板** 三层分层，不合并 | 职责单一，Reflection/Verification 已在其他文档实现，Evals 只做资产管理和编排 | Evals 新模块仅新增，不重写 TAOR 循环 Verify 阶段实现 |
| 2 | Eval 资产集中注册到 `aip_eval_assets.py`，不继续散落在各技能文档 | 散落在 8 个文档改一条要搜全局；集中后发布跑集只需按 category/priority 拉取 | 每次发布/变更改一处 eval 即可，同步成本降低 80% |
| 3 | 运行门控 **按策略采样**，P0 100% / P1 20% / P2 5%，被投诉的 skill_id 24h 内全采样 | 每次请求都 eval 拖慢 10-30%，P0 关键链路牺牲性能换可靠性，P2 节省成本 | 平均运行时 eval overhead 控制在 5% 以内（不是 20%） |
| 4 | 发布门控三档门槛（95%+通过/85-95%审批/<85%阻断）+ 基线劣化检测（掉 5% 报警） | 参考行业发布标准，兼顾质量与效率；基线对比防止"静默劣化" | 模型/配置升级不会偷偷掉成功率没人发现 |
| 5 | Evaluator **Hybrid 模式**（80% rule-based + 20% LLM Judge）+ LLM Prompt 极简原则 | 硬规则毫秒级零成本，LLM 只处理语义模糊场景；参考 Claude Blog 删 80% Prompt | LLM Judge 节省 70%+ Token，总体判断速度快 5× |
| 6 | 严重度四级处理（critical 阻断转人工 / high 自动修复 3 次 / medium 不阻断告警 / low 记录） | 客服话术合规 = 致命问题；数据参谋格式瑕疵 = 小问题；一刀切阻断或放行都不合理 | 合规类 0 漏网 + 体验类 0 过度阻断的平衡 |
| 7 | 发布审批**复用 DraftInbox 状态机**，不新建审批系统 | Draft 引擎已有 draft→approved/rejected 状态机 + UI；再造轮子成本高 | 少写一个审批模块，上线时间缩短 2 周 |
| 8 | Metric 接入**现有 ObservabilityPage 新增 Tab**，不新建页面 | ObservabilityPage 已在 AIP 层 Harness 升级中，挂到该页面减少用户跳转 | 前端零新页面开发，只增一个 API 数据源 |

---

## 十、实施顺序建议

| 阶段 | 内容 | 建议周期 | 依赖 |
|------|------|---------|------|
| Phase 1 | 资产层注册 + Standalone 模式 + 10 条核心 Smoke Eval | 1 周 | AIP 层 Phase 1 完成（TAOR 循环骨架） |
| Phase 2 | Embedded 模式（采样策略 + 严重度处理）+ Chained 模式 + Metric 基础看板 | 1.5 周 | AIP 层 Phase 3 完成（权限防线） |
| Phase 3 | On every PR/Config Change 模式 + 发布门控 + 基线对比 | 1.5 周 | Phase 2 完成 + Draft 引擎可用 |
| Phase 4 | 全量 Eval 用例补齐（60 Smoke + 200 Regression + 60 Edge）+ 看板完善 | 2 周 | 各数字同事技能上线后补充具体断言 |

---

*本文档为方案设计层，实施前需用户确认。*
*关联文档：`01-Plan-Mode与TAOR循环设计.md` §六（Verification Loop 定义）· `../13-FDE技能编排方案/04-Reflection自审节点设计.md`（FDE Reflection 26 条规则）· `02-私域管家技能编排.md` 等 5 份数字同事技能编排（各技能 Verification Loop 定义）*

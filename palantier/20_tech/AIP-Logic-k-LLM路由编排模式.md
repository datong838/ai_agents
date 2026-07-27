# AIP Logic k-LLM 路由编排模式

> **编号**：G-AIP-04（设计模式，非功能缺口）
> **版本**：v1.0
> **日期**：2026-07-23
> **关联**：220plan #71-75（路由基础设施）· #199（AIP Logic 8 Block）· TitanIndustries §Stage 5
> **底层状态**：全部就绪 ✅

---

## 1. 问题背景

AOS 平台有两层模型选择机制：

1. **全局路由层**（`aip-model-router.html`）：SmartRouter(#71) + ScenarioRouter(#72) + FailoverEngine(#73) + EgressPolicyEngine(#74) + CustomLLMRegistry(#75)
2. **局部编排层**（AIP Logic 函数内）：Conditionals 条件分支 Block(#199) + Use LLM Block 指定 `model_id`

开发者经常会问：**什么时候用全局路由，什么时候在 Logic 内手动编排？两者冲突时谁优先？**

本文档回答这些问题，并以 TitanIndustries 信用冻结场景为例展示完整的编排模式。

---

## 2. 三级模型选择优先级

```
┌──────────────────────────────────────────────────────────┐
│                  模型选择决策链                            │
│                                                          │
│  Step 1: 安全策略检查（EgressPolicyEngine #74）           │
│    │ 数据含 PII / 敏感标记？                              │
│    ├─ 是 → 强制使用合规模型（不可被局部覆盖）              │
│    └─ 否 ↓                                               │
│                                                          │
│  Step 2: 局部显式绑定（AIP Logic Use LLM Block）          │
│    │ Block 指定了 model_id？                              │
│    ├─ 是 → 使用局部指定的模型                             │
│    └─ 否 ↓                                               │
│                                                          │
│  Step 3: 全局路由（ScenarioRouter #72）                   │
│    │ 有匹配的场景规则？                                   │
│    ├─ 是 → 使用全局场景路由结果                           │
│    └─ 否 ↓                                               │
│                                                          │
│  Step 4: 系统默认模型（兜底）                             │
│    → 使用 system_default_model                           │
└──────────────────────────────────────────────────────────┘
```

### 2.1 优先级表

| 优先级 | 来源 | 决策者 | 可否覆盖 | 对应组件 |
|--------|------|--------|---------|---------|
| **P0（最高）** | 安全策略 | 平台管理员 | **不可覆盖** | EgressPolicyEngine #74 |
| **P1** | 局部显式绑定 | Logic 函数作者 | 可覆盖 P2/P3 | Use LLM Block `model_id` |
| **P2** | 全局场景路由 | 平台路由策略 | 可覆盖 P3 | ScenarioRouter #72 |
| **P3（最低）** | 系统默认 | 系统配置 | — | system_default_model |

### 2.2 两种策略类型

| 类型 | 含义 | 冲突行为 | 例子 |
|------|------|---------|------|
| **推荐性路由** | 任务→首选模型的默认映射 | 局部可覆盖 | "摘要任务默认用 glm-4-flash" |
| **强制性策略** | 数据安全合规约束 | 局部不可覆盖 | "PII 数据禁止调用境外 API" |

---

## 3. 何时用全局路由 vs 何时在 Logic 内编排

### 3.1 使用全局路由的场景

| 场景 | 原因 |
|------|------|
| **通用 Agent 对话** | 无需针对每次调用选模型，全局路由按任务类型自动匹配 |
| **批量数据处理** | Pipeline 中的 LLM 节点，按数据特征全局路由 |
| **快速原型开发** | 先用全局默认，跑通后再优化 |
| **成本优化** | 全局路由的 SmartRouter 5 维评分自动选性价比最优模型 |
| **安全合规** | 数据出境策略全局强制，不需要开发者手动处理 |

### 3.2 使用 Logic 内编排的场景

| 场景 | 原因 |
|------|------|
| **复杂度自适应** | 先用小模型分类，再按复杂度路由到不同模型 |
| **多模型协同** | 需要多个模型各司其职（如：提取+推理+生成） |
| **条件分支多步** | 根据中间结果决定下一步用哪个模型 |
| **A/B 测试** | 同一输入并行调两个模型，对比输出 |
| **精度优先** | 特定场景需要明确绑定高精度模型，不接受全局路由的折中 |

### 3.3 决策流程图

```
需要选模型？
  │
  ├─ 只是普通调用？ → 用全局路由（什么都不指定）
  │
  ├─ 有明确偏好？ → 在 Use LLM Block 指定 model_id（局部覆盖全局）
  │
  └─ 需要按条件动态选？ → 在 Logic 内编排
       │
       ├─ Block 1: Use LLM 小模型 → 分类
       ├─ Conditionals 条件分支
       │    ├─ 简单 → Apply Action（不调 LLM）
       │    ├─ 中等 → Use LLM 中等模型
       │    └─ 复杂 → Use LLM 大模型
       └─ 输出结果
```

---

## 4. 安全策略护栏规则

### 4.1 EgressPolicyEngine 的不可覆盖性

EgressPolicyEngine(#74) 是**安全护栏**，在模型选择决策链的 **Step 1** 执行。即使 Logic 内明确绑定了某个模型，如果该模型违反安全策略，调用将被**拦截**。

```python
# 伪代码：EgressPolicyEngine 拦截逻辑
def resolve_model(use_llm_block, context):
    # Step 1: 安全检查（不可跳过）
    egress_decision = EgressPolicyEngine.evaluate(
        data_tags=context.sensitive_fields,
        target_model=use_llm_block.model_id
    )
    if egress_decision.decision == "forbidden":
        raise SecurityViolation(
            f"模型 {use_llm_block.model_id} 违反数据出境策略: "
            f"{egress_decision.reason}"
        )
    if egress_decision.decision == "restricted":
        # 强制脱敏后使用
        context.data = EgressPolicyEngine.mask_before_egress(
            context.data, egress_decision.mask_fields
        )
        # 强制使用合规模型，忽略局部绑定
        return egress_decision.override_model
    
    # Step 2: 局部绑定
    if use_llm_block.model_id:
        return use_llm_block.model_id
    
    # Step 3: 全局路由
    return ScenarioRouter.resolve(context.scenario, context.task_type)
```

### 4.2 安全策略配置示例

```yaml
# 全局安全策略（EgressPolicyEngine #74）
egress_policies:
  - name: "PII 数据出境保护"
    sensitive_fields:
      - field: phone
        label: PII
      - field: id_card
        label: PII
      - field: address
        label: SENSITIVE
    rules:
      - condition: "label == PII"
        effect: forbidden
        target_models: ["gpt-4o", "claude-3.5", "gemini-pro"]  # 境外模型
        reason: "PII 数据禁止出境"
      - condition: "label == SENSITIVE"
        effect: restricted
        target_models: ["gpt-4o", "claude-3.5"]
        mask_fields: ["address"]
        override_model: "glm-4"  # 强制使用国产模型
```

---

## 5. TitanIndustries 信用冻结场景完整示例

### 5.1 场景描述

TitanIndustries 的订单到现金（O2C）流程中，当订单金额超过信用额度时触发**信用冻结**。AI 需要评估是否应该解除冻结：

- **输入**：订单对象（金额、客户信用评分、历史付款记录、行业风险）
- **输出**：决策（批准/拒绝/人工审核）+ 理由

### 5.2 Logic 编排（Conditionals + 多 Use LLM Block）

```json
{
  "logic_id": "titan-credit-block-assessment",
  "name": "信用冻结AI评估",
  "description": "根据订单复杂度动态选择模型评估信用冻结",
  "blocks": [
    {
      "type": "Input",
      "name": "订单输入",
      "schema": {
        "order_id": "string",
        "amount": "decimal",
        "customer_id": "string",
        "credit_score": "int",
        "payment_history": "array"
      }
    },
    {
      "type": "Get Object Property",
      "name": "提取客户属性",
      "source": "Customer OT",
      "filter": "customer_id == {{input.customer_id}}",
      "properties": ["industry_risk", "annual_revenue", "payment_reliability"]
    },
    {
      "type": "Use LLM",
      "name": "复杂度分类（小模型）",
      "model_id": "glm-4-flash",
      "prompt": "根据以下信息判断信用评估的复杂度（simple/medium/complex）：金额={{input.amount}}，行业风险={{customer.industry_risk}}",
      "output_schema": {
        "complexity": "string"
      }
    },
    {
      "type": "Conditionals",
      "name": "按复杂度分支",
      "conditions": [
        {
          "when": "{{blocks.复杂度分类.complexity}} == 'simple'",
          "goto": "简单评估"
        },
        {
          "when": "{{blocks.复杂度分类.complexity}} == 'medium'",
          "goto": "中等评估"
        },
        {
          "when": "{{blocks.复杂度分类.complexity}} == 'complex'",
          "goto": "复杂评估"
        }
      ],
      "default": "人工审核"
    },
    {
      "type": "Apply Action",
      "name": "简单评估",
      "action_type": "auto_approve_credit",
      "condition": "amount < 10000 AND credit_score > 700"
    },
    {
      "type": "Use LLM",
      "name": "中等评估",
      "model_id": "glm-4-plus",
      "prompt": "评估信用冻结...金额={{input.amount}}...信用评分={{input.credit_score}}",
      "tools": ["query_customer_history", "calculate_risk_score"],
      "output_schema": {
        "decision": "approve|reject|manual_review",
        "reason": "string"
      }
    },
    {
      "type": "Use LLM",
      "name": "复杂评估",
      "model_id": "gpt-4o",
      "prompt": "深度分析信用风险...行业={{customer.industry_risk}}...历史={{input.payment_history}}",
      "tools": ["query_customer_history", "calculate_risk_score", "industry_benchmark", "cash_flow_analysis"],
      "output_schema": {
        "decision": "approve|reject|manual_review",
        "reason": "string",
        "confidence": "float",
        "risk_factors": "array"
      }
    },
    {
      "type": "Execute",
      "name": "人工审核",
      "function": "create_manual_review_task",
      "params": {
        "order_id": "{{input.order_id}}",
        "reason": "复杂度分类不确定"
      }
    }
  ]
}
```

### 5.3 执行流程

```
Block 1: Input → 订单数据
    ↓
Block 2: Get Object Property → 客户属性（行业/收入/可靠性）
    ↓
Block 3: Use LLM [glm-4-flash] → 复杂度分类（成本低、速度快）
    │  输出: complexity = "medium"
    ↓
Block 4: Conditionals → 按 complexity 分支
    │  "medium" → goto Block 6
    ↓
Block 6: Use LLM [glm-4-plus] → 中等评估
    │  使用工具: query_customer_history + calculate_risk_score
    │  输出: { decision: "approve", reason: "信用评分750，历史付款记录良好" }
    ↓
（最终输出）
```

### 5.4 安全护栏交互

如果该 Logic 运行在中国客户数据上，安全策略会拦截 Block 7（复杂评估）的 `gpt-4o`：

```
Block 7: Use LLM [gpt-4o]
    │
    ↓ EgressPolicyEngine 检查
    │
    ├─ 数据不含 PII？ → 允许使用 gpt-4o ✅
    │
    └─ 数据含 PII（如客户手机号）？
         │
         ├─ 策略 = forbidden → 阻断，抛出 SecurityViolation ❌
         │
         └─ 策略 = restricted → 脱敏后强制改用 glm-4 ⚠️
              （即使 Logic 明确指定了 gpt-4o，安全策略覆盖）
```

### 5.5 成本对比

| 方式 | 模型 | 每次调用成本 | 1000 次/天 |
|------|------|------------|-----------|
| 全用大模型 | gpt-4o | ~$0.06 | ~$60 |
| 全用中等模型 | glm-4-plus | ~$0.01 | ~$10 |
| **k-LLM 编排** | flash 分类(70%) + plus(20%) + gpt-4o(10%) | ~$0.008 | ~**$8** |
| 节省 | — | — | **87%** |

---

## 6. 最佳实践

### 6.1 编排原则

| 原则 | 说明 |
|------|------|
| **先分类后执行** | 用小模型做复杂度/类型分类，再路由到合适的模型 |
| **能用小模型就不用大模型** | 70% 的任务用 flash 级模型就够了 |
| **保留 Apply Action 快速通道** | 简单场景直接走确定性 Action，不调 LLM |
| **人工兜底** | Conditionals 的 default 分支应该走人工审核 |
| **安全优先** | 始终假设安全策略会拦截，不要依赖特定模型 |

### 6.2 反模式

| 反模式 | 问题 | 正确做法 |
|--------|------|---------|
| 每个调用都用大模型 | 成本高、延迟大 | 用 k-LLM 编排按需选模 |
| 不指定 model_id 依赖全局 | 不可控、不可预测 | 关键路径明确绑定模型 |
| 在 Logic 内硬编码绕过安全 | 违规 | 始终通过 EgressPolicyEngine |
| 无 fallback 的单模型编排 | 模型不可用时全链路失败 | 每条分支配置 FailoverEngine 回退 |
| 线性链路无分支 | 等于没用 k-LLM | 至少有一个 Conditionals 分支 |

---

## 7. 与 220plan 的对应关系

| 能力 | 220plan 编号 | 状态 | 在本文中的角色 |
|------|-------------|------|---------------|
| SmartRouter 5 维评分 | #71 | ✅ | 全局路由 P2/P3 层 |
| ScenarioRouter 场景路由 | #72 | ✅ | 全局路由 P2 层 |
| FailoverEngine 熔断 | #73 | ✅ | 模型不可用时回退 |
| EgressPolicyEngine 出境策略 | #74 | ✅ | 安全护栏 P0 层 |
| CustomLLMRegistry 自定义注册 | #75 | ✅ | 模型注册 |
| Logic Conditionals Block | #199 | ✅ | 条件分支编排 |
| Use LLM Block model_id 绑定 | #199 | ✅ | 局部显式绑定 P1 层 |

**结论**：k-LLM 路由编排模式所需的全部底层能力已在 220plan 中完成。本文档是对这些能力的**最佳实践指南**，不是功能缺口。

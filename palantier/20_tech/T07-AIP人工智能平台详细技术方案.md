# T07 · AIP 人工智能平台详细技术方案

> **版本**：v1.0.3 · 2026-07-17  
> **状态**：✅ **方案完成**（含 [25](25-LLM-Wiki启示与L2演进补丁.md) Insight Backfill · [07b](../07b-Capability-Adapter重能力接入.md) Capability）  
> **对齐产品**：[07](../07-AIP引擎k-LLM与AgentStudio产品方案.md) · [07a](../07a-AIP引擎产品设计线框图.md) · [07b](../07b-Capability-Adapter重能力接入.md) · [20 §3.1·§6.6](20-AOS整体技术方案.md) · [25](25-LLM-Wiki启示与L2演进补丁.md) · [T-API](T-API-aos-api稳定契约.md) · [21](21-AOS开源选型与功能清单.md) · [23 军规](23-AOS开源引用与交付军规.md)  
> **口径**：目标态仅 **AIP 人工智能平台**（不写右引擎）

---

## 使用的 Rules

产品对齐 · UI 引用 aip-* · LLM **Provider 插件化** · 熔断/预热/Draft/Evals 必写 · 开源只作参考

---

## 1. 范围

| 做 | 不做 |
| --- | --- |
| k-LLM Model Gateway · Logic · Chatbot Studio · Tools | 把 Dify 当目标内核 |
| Draft / Decision Lineage / Evals 门控 | LLM 直写 Ontology |
| Insight Backfill（高置信结论→Draft→Insight） | 与 Funnel 数据水合混为一谈 |
| L4 熔断 · 模型预热 · Edits 合并 | 无评测的无人值守写回 |

---

## 2. 架构

```text
aip-model-gateway     # 统一 chat/embed；Provider 插件
aip-logic-runtime     # Logic 图执行 · Tool 调用 · Draft 输出
aip-agent-studio      # Chatbot 配置 · 试对话
aip-evals             # 评测集 · 门控状态
aip-lineage           # 决策谱系 · 熔断事件
        ↓
仅经 Action Runtime 写 Ontology（HR-01）
```

---

## 3. Model Gateway（插件化）

### 3.0 自有所需功能（先于开源）

| 功能项 | 我们要什么 | 验收 |
| --- | --- | --- |
| 统一 Facade | 对外仅 `aos-api` `/v1/aip/*`；UI 不直连厂商 SDK | T-API |
| Provider 插件 | 可增删供应商；路由/配额/健康/预热 | 新增插件不改 Facade 核心 |
| 密钥分槽 | 每 Provider Vault ref；禁明文 | SECRET 拒绝 |
| 预热 | 冷模型 warm-up；失败不静默进 L4 | UI 预热态 |
| 熔断联动 | 与成熟度 L4 / Lineage 事件互通 | T07 §6.1 |

### 3.1 契约（对齐 20 §3.1 · Dify 模型供应商体验）

```text
Provider Plugin manifest:
  id, version, authSchema, modelListAPI, chat/embed capabilities
Gateway:
  统一 OpenAI-compatible 对内 API
  路由规则 · 配额 · 健康 · 预热钩子
密钥:
  按插件分槽；明文禁落盘（Vault ref，见 T09）
```

**UI 蓝图：** 接入 [`aip-model-providers.html`](../foundry/html/aip-model-providers.html) · 路由 [`aip-model-router.html`](../foundry/html/aip-model-router.html)（两屏；卡片/类型化表单，不搬 Marketplace）

### 3.2 开源参考（已核对本地）

| 仓 | 路径 | 抄什么 | 不抄什么 |
| --- | --- | --- | --- |
| **LiteLLM** | `C1_ModelRouter/litellm`（含 `litellm/` 包） | 多 Provider 统一接口、路由、失败回退模式 | 默认 SaaS 密钥运营模式；对外品牌 |
| **Dify**（试用树） | `mybuddy-v01/dify` | 「模型供应商」配置/测连通 UX 与插件分包思路 | 目标态永久内核；交付面品牌（10g） |

> **检查结论：** LiteLLM README 明确 Unified API / 100+ providers；适合作为 **Gateway 实现参考或边车**，产品配置面仍走自有 UI。

### 3.2.1 Gateway 部署已决

| 项 | 结论 |
| --- | --- |
| 对外契约 | **仅** `aos-api` `/v1/aip/models|chat|…`（T-API） |
| 对内实现 | **LiteLLM 边车**（进程隔离）承担多 Provider 适配 |
| 自研层 | Model Gateway Facade：路由策略、配额、预热、熔断、审计、插件注册表 |
| 禁止 | UI / Logic 直连 LiteLLM SDK 或上游厂商 SDK |
| 替换 | 未来可换自研适配器，**不改**对外 API |

### 3.3 模型预热（产品补强）

路由选中冷模型前：warm-up 推理或常驻最小实例；UI 显示「预热中/就绪」。失败不得静默进 L4。

---

## 4. Logic Runtime

### 4.0 自有所需功能（先于开源）

| 功能项 | 我们要什么 | 验收 |
| --- | --- | --- |
| Logic 图 | 节点：Get Object · Wiki · LLM · Function · Draft · Action | 可试跑不落库 |
| Edits 合并 | 多 Logic 并发提议合并后再写 | 07 §3.5.1 |
| 写约束 | 写 Ontology 仅经 Action | HR-01 |
| 检查点/重试 | 长图可恢复（实现可借图运行时） | 产品语义自有 |

| 能力 | 说明 |
| --- | --- |
| 节点 | Get Object · Wiki 字段 · Use LLM · Function · Draft · Action(tool) |
| 试跑 | 不落库（产品 A-07 口径） |
| **Edits 合并** | 多 Logic 并发提议 → 合并策略后再写（07 §3.5.1） |
| 输出 | Ontology Edits / Draft Dataset / 建议 Action |

**UI 蓝图：** [`aip-logic.html`](../foundry/html/aip-logic.html)

### 4.1 开源参考

| 仓 | 路径 | 抄 | 不抄 | 选型 |
| --- | --- | --- | --- | --- |
| LangGraph | `C5_AgentOrchestration/langgraph`（`libs/`） | 有状态图、检查点、重试 | 无 Ontology 约束的自由 Agent | **建议**作 Runtime 内核参考 |

---

## 5. Tools 与 Agent

### 5.0 自有所需功能（先于开源）

| 功能项 | 我们要什么 | 验收 |
| --- | --- | --- |
| Tool Registry | 六类+Capability 统一注册；写操作落 Action | 无 UI→厂商 SDK 直连 |
| Chatbot Studio | Agent 配置 · 试对话 · 绑定 Tool | `agents.html` |
| Wiki Tool | **结构化字段优先**，非纯向量 RAG | AIP-003 |
| Capability Registry | Manifest · Job/Session · Facade | 07b · `aip-capabilities.html` |
| L1 供数 | Connector→Dataset/Object 后再供 Tool；禁短路 Ontology | 只读工具化 |

### 5.1 工具六类（产品）

Query Objects · Function · Action · Wiki 字段 · Media · **Capability（重能力）** ·（扩展）外部只读 Tool  

**Wiki Tool：** 结构化字段优先，非纯向量 RAG（AIP-003）。

**Capability Tool：** 短视频 Job / 数字人 Session 等；契约与分级见 [07b](../07b-Capability-Adapter重能力接入.md)。超 FUNC-03 禁注册为普通 Function（CAP-01）。

**UI：** [`aip-tools.html`](../foundry/html/aip-tools.html) · Studio [`agents.html`](../foundry/html/agents.html) · 重能力登记 [`aip-capabilities.html`](../foundry/html/aip-capabilities.html)

### 5.2 L1→AIP 供数（Airbyte Agent 线 · 开源参考）

| 仓 | 本地路径 | 检查结论 | 用法 |
| --- | --- | --- | --- |
| **airbyte-agent-sdk** | `C5_AgentOrchestration/airbyte-agent-sdk` | README：`build_connector_tools` / `@Connector.tool_utils`，可挂 LangChain 等 | **参考**：把 Connector 变成 type-safe Tool 的模式；**产品 Tool 须包进自有 AIP Tool Registry**，禁止 UI 直依赖 SDK |
| airbyte-agent-cli | 同目录 | CLI / Benchmark 配套 | 研发工具 |
| PyAirbyte | `A1_ETL/pyairbyte` | `get_source` 轻量抽数 | 结构化数据入 L1/Dataset 后再供 AIP，不短路 Ontology |

写路径仍走 Action；Agent SDK **只读工具化**。

### 5.3 Capability Registry（重能力）

| 功能项 | 我们要什么 | 验收 |
| --- | --- | --- |
| Registry | Manifest · kind=sync\|job\|session · 版本启用 | 07b §4 |
| Facade | 仅 `aos-api` `/v1/aip/capabilities/*`；禁 UI 直连厂商 SDK | T-API · CAP-04 |
| Job 状态机 | submit/status/cancel/artifact · 回调验签 · DLQ | CAP-05 · ACT-10 |
| Session | open/push/close · 会话 Object · AV 外置 | 07b 旅程 P3 |
| 与 Function | 薄封装可调 Facade；重活不进 ≤60s/2GB 沙箱 | CAP-01 · C-12 |

```text
aip-capability-facade
  → registry (manifest)
  → job-orchestrator | session-gateway
  → Adapter 边车 / 客户前置重服务
  → callback → Action Runtime 写 Object / MediaSet RID
```

---

## 6. Draft · Lineage · Evals · 成熟度

### 6.0 自有所需功能（先于开源）

| 功能项 | 我们要什么 | 验收 |
| --- | --- | --- |
| Draft | 与生产 Dataset 隔离；审批台 | ACT-09 |
| Decision Lineage | 读→模型→输出全谱；熔断事件入谱 | HR-05 |
| Insight Backfill | 高置信结论经 Draft 沉淀为 Insight Object + Link | [25](25-LLM-Wiki启示与L2演进补丁.md) · T06 §7.3 |
| Evals 门控 | L4 须评测绿 | 未绿不可勾 L4 |
| 成熟度楼梯 | L1–L4；L4= Evals+Draft+熔断 | 失败率>5% 降 L3 |

| 能力 | 规则 | UI |
| --- | --- | --- |
| Draft | ACT-09 隔离；审批台；含类型 `InsightBackfill` | [`aip-draft-inbox.html`](../foundry/html/aip-draft-inbox.html) |
| Lineage | 读 Object/Wiki → 模型 → 输出；**熔断事件入谱**；可链 Backfill | [`aip-decision-lineage.html`](../foundry/html/aip-decision-lineage.html) |
| Evals | L4 须绿 | [`aip-evals.html`](../foundry/html/aip-evals.html) |
| 成熟度 L1–L4 | L4 须 Evals+Draft | [`aip-maturity.html`](../foundry/html/aip-maturity.html) |

### 6.0.1 Insight Backfill Pipeline（P0 · 知识复利）

```text
Logic/Agent 高置信结论
    → Draft(InsightBackfill)     # 强制 HITL；禁直写
    → 批准
         ├─ Action/Edits 更新相关 Object 属性（可选）
         └─ 创建 Insight Object + Link 相关实体（推荐）
    → Decision Lineage 记全谱
```

| 规则 | 说明 |
| --- | --- |
| ≠ Funnel | Funnel 是 L1 Dataset 水合；Backfill 是 AIP 结论沉淀 |
| ≠ 仅 Lineage | Lineage 是审计录像；Insight 是可查询、可链接的 Ontology 资产 |
| 护栏 | Constitution `ethics.json` 可要求某类结论必须 Human-Approval |

---

### 6.1 L4 熔断（强制）

| 条件 | 动作 |
| --- | --- |
| 自动化失败率 **>5%**（滑动窗口） | **自动降级 L3**；停无人值守写回 |
| 告警 | Lineage + 运维通知；禁止静默 |

### 6.2 开源参考

| 仓 | 路径 | 抄 | 不抄 | 选型 |
| --- | --- | --- | --- | --- |
| promptfoo | `C2_Evals/promptfoo` | 评测集 / harness 思路 | 替代业务门禁产品 | **建议** Evals harness |
| langfuse | `C3_Trace/langfuse` | Trace · 提示词观测 | 替代 Decision Lineage 产品语义 | **建议** 观测边车 |
| qdrant / milvus | `C8_RightEngine/*` | 向量检索（工具侧 RAG） | 「向量=Ontology」 | 需要 RAG 时 **Qdrant 优先 Lite** |

---

## 7. API 摘要

完整路径见 [T-API §2.3](T-API-aos-api稳定契约.md)。

---

## 8. 验收

| # | 标准 |
| --- | --- |
| A1 | 新增 Provider 插件无需改 Facade 核心（改 LiteLLM 配置/插件包即可） |
| A2 | Eval 未绿无法勾选 L4 |
| A3 | 模拟失败率>5% 触发降级 |
| A4 | Draft 与生产 Dataset 隔离可证 |
| A5 | Tool 写操作最终落 Action；扫描无 UI→LiteLLM 直连 |
| A6 | Insight Backfill 批准后可复盘 Insight + Link；驳回不污染生产 |
| A7 | 超 FUNC-03 能力仅能登记为 Capability job/session；回调写库须经 Action |

---

## 9. 已决结论（原缺口已关闭）

| ID | 结论 |
| --- | --- |
| T07-G1 | **Facade 自有 + LiteLLM 边车**（§3.2.1） |
| T07-G2 | Agents Benchmark 为 **P2 研发工具**；需要时 `clone_airbyte_refs.ps1 -Tier P2`；不阻塞 AIP 主路径 |
| T07-G3 | **Insight Backfill Pipeline** 见 §6.0.1 / [25](25-LLM-Wiki启示与L2演进补丁.md)；与 Funnel 分责 |
| T07-G4 | **Capability Adapter** 见 §5.3 / [07b](../07b-Capability-Adapter重能力接入.md)；重代码外置 |

---

*T07 v1.0.3 · docs/palantier/20_tech*

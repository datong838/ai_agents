# 228-电商增长参谋长 G2 三个核心数字同事与 CustomerLite 实施方案

> 状态：方案稿 · G0/G1 未完成前不授权编码
> 版本：v1.0 · 2026-08-02
> 上游：[G1 每日经营最小闭环](228-电商增长参谋长G1每日经营最小闭环实施方案.md)
> 总纲：[电商增长参谋长与六数字同事协同进化实施方案](228-电商增长参谋长与六数字同事协同进化实施方案.md)

---

## 0. 使用的 Rules

- 先让“内容官 → 导购顾问 → 客服专员 → 效果反馈”形成可追踪闭环，再扩展更多智能体。
- CustomerLite 只保存增长所需的最小、去标识化信息；姓名、手机号、地址、OpenID、聊天原文不进入通用模型。
- 内容、推荐和客服回复均先生成 Draft，由人工确认；G2 不发布、不触达、不修改订单。
- 每次 Handoff 只传任务所需字段、证据引用和授权范围，不传完整客户档案。
- 每个智能体必须使用已发布 Logic、受控 Tool 和可回读 run，禁止旧内存 TAOR 成为生产真源。
- 内容效果、成交反馈和服务反馈都回流给数据参谋，不能把“已生成”当成“有效”。
- 平台专项字段通过映射层接入，不污染通用 CustomerLite 和增长契约。

---

## 1. 业务目标与真实完成定义

G2 解决初创电商最直接的“获客、咨询、成交、售后反馈”问题：

```text
数据参谋批准任务
  → 内容官生成渠道内容 Draft
  → 人工发布/外部手工执行并登记结果
  → LeadSignal/咨询信号进入 CustomerLite
  → 导购顾问生成有依据的推荐 Draft
  → 人工发送并登记成交或未成交原因
  → 客服专员生成服务处置 Draft
  → 服务/成交/内容效果回传数据参谋复盘
```

真实完成必须满足：

1. 三个核心数字同事各自有独立工作台、任务队列、Logic、产物和效果证据。
2. 内容产物能追溯到 GrowthPlan revision、受众、商品事实、渠道约束和证据。
3. 导购推荐只基于真实商品、库存、价格和合规事实；信息不足时拒绝强推。
4. 客服回复区分咨询、履约、退款、投诉与人工升级，不自行承诺平台不存在的政策。
5. CustomerLite 在双租户同 ID、删除/撤回同意、最小披露和小样本抑制测试中通过。
6. 三类产物均保持 Draft-only；生产写回负向测试必须证明没有外部副作用。

非目标：真实社交平台发布、自动私信、自动下单、改价、退款、库存写回、数字人直播和长期记忆晋升。

---

## 2. 当前代码审计结论与前置条件

可复用：

- canonical Logic Graph/Store、DryRun、history、Evals 与 immutable publication。
- G0 的 GrowthPlan、AgentTask、Handoff、Evidence、Artifact 契约和租户门禁。
- G1 的 MetricQuery、Observation、Review 与数据参谋任务编排。
- 数据管道的可信数据集 revision；平台原始表不能由 AIP 任意直查。

禁止复用：

- `aip_task_model.py` 的进程内 Task 不能承载三智能体生产任务。
- 旧 LongMemory 不具备租户、审查和持久化，不保存客户经验。
- `tool_runtime.query.objects` 当前租户过滤不足，不作为客户/商品查询入口。
- 前端 localStorage、样例客户、固定 expected 和 mock 成交不得进入效果口径。

G2 开发前置：G0/G1 退出门全部关闭；商品、库存、订单状态最小数据集已通过新鲜度检查；CustomerLite 隐私评审通过。

---

## 3. CustomerLite 隐私最小对象

### 3.1 通用字段

```yaml
customer_lite_id: cl_...
org_id: org_...
project_id: project_...
pseudonymous_subject_id: hmac_...
source_channel: wechat|douyin|xiaohongshu|toutiao|xianyu|shop|other
consent:
  purpose: consultation|service|marketing
  status: granted|denied|withdrawn|unknown
  captured_at: ...
lifecycle_stage: anonymous|lead|consulting|customer|repeat|inactive
preference_tags: []
aggregate_order:
  paid_count: 0
  paid_amount_band: none|low|medium|high
  last_paid_at: null
service_risk_level: none|low|medium|high
last_interaction_at: ...
revision: 1
markings: []
```

### 3.2 明确禁止

- 不保存姓名、手机号、身份证、地址、银行卡、密码、Cookie、Token、OpenID 明文。
- 不保存完整聊天原文；只保存经审查的意图、摘要、证据 hash 和必要片段引用。
- 不从不同平台自行合并身份；跨渠道关联必须有合法依据和人工确认。
- `marketing=denied/withdrawn/unknown` 时不得生成私域触达任务。
- 删除或撤回同意后，派生画像进入失效队列；审计事件保留但去除可识别内容。

### 3.3 状态与并发

更新使用 `expected_revision`；服务端强制注入 org/project；同一伪匿名主体的并发合并采用 CAS。事件流记录来源、actor、purpose、before/after hash，不记录敏感明文。

---

## 4. 三个核心数字同事的数据契约

| 对象 | 关键字段 | 产出者 | 消费者 |
|---|---|---|---|
| `ContentBrief` | audience、objective、channel、facts、constraints、evidence_refs | 数据参谋/内容官 | 内容官 |
| `ContentAssetDraft` | title、body/script、CTA、claims、channel_variant、risk_flags | 内容官 | 审批人/人工发布 |
| `ContentOutcome` | publication_ref、exposure、engagement、lead_count、window | 人工登记/Connector | 数据参谋 |
| `LeadSignal` | channel、intent、product_refs、consent、confidence | 内容/咨询入口 | CustomerLite/导购 |
| `ConsultationCase` | customer_lite_ref、question_summary、constraints、evidence_refs | 导购 | 推荐 Logic |
| `RecommendationDraft` | ranked_items、reasons、tradeoffs、stock/price revision、disclaimer | 导购 | 人工发送 |
| `ConversionOutcome` | converted、order_ref_token、reason_code、observed_at | 人工/只读数据 | 数据参谋/内容官 |
| `ServiceCase` | category、severity、order_ref_token、policy_refs、SLA | 客服 | 回复/人工升级 |
| `ServiceReplyDraft` | reply、proposed_steps、commitments、risk_flags | 客服 | 人工发送 |
| `ServiceOutcome` | resolved、resolution_code、CSAT band、feedback_tags | 人工/只读数据 | 数据参谋/内容官 |

所有对象必须有 `id/org/project/revision/status/created_by/created_at/markings`，并引用 G0 Evidence；外部订单引用只能使用受控 token。

---

## 5. 内容官 Logic：C01～C08

| Logic | 输入 | 核心节点/Tool | 输出 | 失败或 Handoff |
|---|---|---|---|---|
| C01 机会接收 | approved task、DailyBrief | evidence_validate → audience_transform | ContentBrief Draft | 证据不足退回数据参谋 |
| C02 选题规划 | brief、历史效果 | metric_query → cluster → rank | TopicPlan | 无效果数据标记 cold_start |
| C03 商品事实核验 | topic、product refs | product_read → inventory_read → claim_check | FactPack | 数据不新鲜阻断 |
| C04 文案/种草 | FactPack、channel policy | generate → claim_guard → style_eval | ContentAssetDraft | 高风险 claim 转人工 |
| C05 短视频脚本 | FactPack、时长/镜头约束 | outline → shotlist → safety_eval | VideoScriptDraft | 素材/版权不明阻断 |
| C06 渠道变体 | master draft | channel_transform → length/format_eval | ChannelVariant[] | 不支持平台只导出通用稿 |
| C07 质检提交 | variants | factuality → policy → brand_eval | ApprovalPackage | 任一硬门失败退回 C04/C05 |
| C08 效果复盘 | outcome、plan | attribution_read → compare → summarize | ContentReview | 数据窗口未闭合则 preliminary |

G2 支持微信视频号/朋友圈、抖音、小红书、今日头条、闲鱼的“内容格式模板”，不声称具备这些平台的发布 API。真实 Connector 在 G5。

---

## 6. 导购顾问 Logic：G01～G06

```text
G01 咨询理解
  → G02 需求与约束澄清
  → G03 候选商品检索
  → G04 推荐与比较
  → G05 人工发送包
  → G06 成交/未成交复盘
```

关键规则：

- 检索只使用当前租户的商品、SKU、价格、库存和已批准知识；每条事实附 revision。
- 不得根据敏感属性推断购买力，不得制造虚假稀缺、虚假优惠或绝对化效果。
- 候选少于最低数量、库存过期、价格冲突或问题未澄清时输出 `NEEDS_CLARIFICATION`。
- 推荐必须展示排序原因、替代项、权衡和不确定性；不能只给一个商品链接。
- 订单是否成交来自只读订单事实或人工登记，不由模型猜测。
- 未成交原因使用受控枚举：价格、需求不匹配、库存、信任、时机、服务、未知。

---

## 7. 客服专员 Logic：S01～S06

| Logic | 责任 | 必须门禁 |
|---|---|---|
| S01 工单分类 | 售前、物流、退款、投诉、商品使用、其他 | 低置信度转人工 |
| S02 事实装配 | 只读订单状态、物流、商品和政策 | 数据不新鲜不承诺 |
| S03 回复生成 | 生成清晰、同理、可执行的 Draft | 不暴露内部信息 |
| S04 承诺校验 | 时效、赔付、退款、退换规则 | 超权限承诺阻断 |
| S05 升级与 SLA | 风险、情绪、安全、法律、媒体事件 | 高风险立即人工 |
| S06 服务复盘 | 结果、CSAT band、重复问题、内容缺口 | 回流数据参谋/内容官 |

G2 客服不调用退款、发货、改价或补偿 Action；只输出建议步骤和人工处置包。

---

## 8. Handoff 最小披露

| 从 → 到 | 允许字段 | 禁止字段 |
|---|---|---|
| 数据参谋 → 内容官 | 目标、受众分群摘要、商品/证据 refs、指标目标 | 客户明细、原始订单 |
| 内容官 → 导购 | LeadSignal、内容/商品 refs、同意状态 | 平台账号凭据、完整评论原文 |
| 导购 → 客服 | order ref token、问题摘要、已做动作、风险 | 电话、地址、无关聊天 |
| 客服 → 内容官 | FAQ tag、误解点、退货/投诉聚合 | 个体身份、客服原文 |
| 全员 → 数据参谋 | Artifact/Outcome refs、指标、失败原因 | 未脱敏自由文本 |

服务端按 recipient、purpose、marking 重新授权，不能仅凭前一个智能体已读取而透传。

---

## 9. API 与状态机

新增建议：

```text
POST   /v1/growth/customer-lite
GET    /v1/growth/customer-lite/{id}
PATCH  /v1/growth/customer-lite/{id}
POST   /v1/growth/customer-lite/{id}/consent-events
POST   /v1/growth/content-briefs
POST   /v1/growth/content-assets/{id}/submit
POST   /v1/growth/consultations
POST   /v1/growth/recommendations/{id}/submit
POST   /v1/growth/service-cases
POST   /v1/growth/service-replies/{id}/submit
POST   /v1/growth/outcomes
```

Draft 状态统一为 `draft → validating → ready_for_review → approved_for_manual_use → superseded|rejected`。`approved_for_manual_use` 不是外部已发送；外部结果必须另建 Outcome。所有 POST 使用 Idempotency-Key，PATCH/submit 使用 expected revision/hash。

---

## 10. 计划新增/修改文件

```text
services/aos-api/aos_api/
  growth_customer_contracts.py
  growth_customer_store.py
  growth_content_service.py
  growth_shopping_guide_service.py
  growth_customer_service.py
  growth_handoff_policy.py
  growth_core_agent_logic_templates.py
  routers/growth_customers.py
  routers/growth_core_agents.py

services/aos-api/alembic/versions/
  228growth2_customer_lite_core_agents.py

apps/web/src/pages/s2/growth/
  CoreAgentCommandCenterPage.tsx
  ContentOfficerWorkbench.tsx
  ShoppingGuideWorkbench.tsx
  CustomerServiceWorkbench.tsx
  CustomerLiteDrawer.tsx
  HandoffTracePanel.tsx
```

共享 OpenAPI、router manifest、迁移 head 和导航只由集成负责人修改；三个智能体服务和页面可以按目录并行，但公共契约由 G2 契约负责人冻结。

---

## 11. 数据库与迁移

新增表至少包含 `growth_customer_lite`、`growth_customer_consent_event`、`growth_content_brief`、`growth_content_asset_revision`、`growth_lead_signal`、`growth_consultation_case`、`growth_recommendation_revision`、`growth_service_case`、`growth_service_reply_revision`、`growth_outcome`。

- 所有业务唯一键包含 org/project；伪匿名 subject 使用租户专属 HMAC key version。
- Revision 只追加；删除采用 tombstone 与派生数据失效任务。
- downgrade 仅在无后续 revision/引用时允许；否则保留表并关闭功能旗标。
- migration 不回填真实客户数据；平台专项映射另行迁移和核验。

---

## 12. 工作台体验

- 总控页展示从批准计划到三智能体产物/结果的时间线与阻断点。
- 内容官可查看事实包、渠道变体、风险 claim、质检结果和人工采用状态。
- 导购可查看客户最小上下文、澄清问题、候选比较和库存/价格时间戳。
- 客服可查看工单严重度、只读事实、回复 Draft、承诺风险和人工升级。
- CustomerLite 默认折叠敏感/高风险信息；无 consent 时营销相关按钮禁用并说明原因。
- 空态不能填演示结果；网络/服务失败不能显示“已提交/已发送”。

---

## 13. 分小波实施

| 小波 | 内容 | 退出门 |
|---|---|---|
| G2.1 | CustomerLite、consent、隐私策略和 API | 双租户、撤回、删除、CAS、PII 扫描通过 |
| G2.2 | 内容官 C01～C08 与工作台 | 事实/渠道/Evals、Draft-only 负向门通过 |
| G2.3 | 导购 G01～G06 与工作台 | 推荐真实性、库存过期、澄清和偏见测试通过 |
| G2.4 | 客服 S01～S06 与工作台 | 承诺、升级、政策引用和高风险负向测试通过 |
| G2.5 | Handoff、Outcome 与闭环浏览器回归 | 三智能体链路和 G0～G2 累计回归通过 |

---

## 14. 测试与验收

必须覆盖：

- 单元：状态机、HMAC、consent、revision、推荐排序、承诺校验、Handoff 最小化。
- 契约：OpenAPI 确定性、错误码、Idempotency-Key、expected revision/hash。
- 权限：双租户同 ID、跨角色审批、marking、撤回同意后访问拒绝。
- 真实性：不存在商品、过期库存、价格冲突、缺失政策、外部提示词注入。
- Evals：内容事实性/渠道适配，推荐有用性/安全性，客服正确性/升级率。
- 浏览器：批准任务 → 内容 Draft → 人工结果登记 → 导购 → 客服 → 数据参谋复盘。
- 累计：G0/G1 全量、AIP Logic、数据管道、API/Web 主回归。
- 生产负向：外部平台、订单、退款、库存、消息系统写入计数必须为 0。

---

## 15. 风险、回滚与退出门

主要风险：身份误合并、PII 泄漏、虚假商品事实、过度推荐、客服越权承诺、把人工登记误当系统事实。通过最小对象、证据 revision、职责分离、Evals 和人工审批控制。

功能旗标：`growth_customer_lite_enabled`、`growth_content_officer_enabled`、`growth_shopping_guide_enabled`、`growth_customer_service_enabled`。任一服务异常可单独关闭，数据保留只读；不得删除审计和 revision。

G2 退出门：G2.1～G2.5 全通过；三智能体链路可重放；CustomerLite 隐私评审通过；G0～G2 累计回归通过；对外副作用为 0。未满足前不得进入 G3/G5 的真实渠道能力。

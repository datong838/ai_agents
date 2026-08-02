# 228-电商增长参谋长 G5 社交平台 Connector 与数字人直播实施方案

> 状态：方案稿 · 各平台能力必须在开发当期以官方文档和账号权限重新核验
> 版本：v1.0 · 2026-08-02
> 上游：[G3 私域活动与跨渠道分析](228-电商增长参谋长G3私域活动与跨渠道分析实施方案.md)、[G4 多智能体记忆与协同进化](228-电商增长参谋长G4多智能体记忆与协同进化实施方案.md)
> 总纲：[电商增长参谋长与六数字同事协同进化实施方案](228-电商增长参谋长与六数字同事协同进化实施方案.md)
> 模块边界：[电商领域包、平台适配包与接入实例交付方案](228-电商领域包平台适配包与接入实例交付方案.md)

---

## 0. 使用的 Rules

- 不凭经验假定微信视频号/朋友圈、抖音、小红书、今日头条、闲鱼存在某个开放 API；开发前逐平台核验官方文档、应用类型、账号资质、权限、审核、配额和收费。
- Connector 先统一契约，再做平台插件；平台差异写 capability manifest，不在业务服务里堆条件分支。
- 按“研究/草稿导出 → 人工发布登记 → 官方只读指标 → 受控发布 → 互动/直播”逐级开放。
- 平台 Secret 只用 secret_ref；OAuth state/PKCE、回调签名、重放、租户、审计、幂等是硬门。
- G5 即使具备技术调用能力，也默认 Draft/manual；真实发布或互动还受 G6 Action 审批控制。
- 数字人形象、声音、素材、音乐和商品宣传必须有授权；高风险问题支持人工接管和立即停播。
- 网页、评论和直播弹幕都是不可信输入，不能覆盖 Logic、Tool 权限或记忆治理。
- OAuth/Webhook/Connector Runtime 属于平台；各社交平台实现属于独立 PlatformAdapterPack；内容/直播业务模型属于 `solution.ecommerce.growth`。

---

## 1. 目标与真实完成定义

G5 建立社交流量平台的可插拔接入底座，并为内容官、私域管家、导购和数据参谋提供一致能力：

```text
平台能力/账号权限核验
  → Connector 安装与授权
  → 内容 Draft/媒体资产校验
  → 人工发布或 ActionProposal
  → 官方回执/状态
  → 只读指标、评论和线索事件
  → CustomerLite/Outcome/Review

数字人直播：
直播计划 → 脚本/知识/商品事实 → 安全评测 → 人工批准
        → 会话运行 → 实时问答/人工接管 → 结束 → 效果复盘
```

真实完成必须满足：

1. 每个平台都有有日期的官方能力核验记录和账号级 capability snapshot，不以方案推测代替事实。
2. Connector 的授权、回调、调用、限流、错误、回执和撤销均可审计并按租户隔离。
3. 业务层只依赖统一契约；某平台不支持的能力返回 `UNSUPPORTED`，页面不显示假按钮。
4. 发布与互动不会因为前端成功 toast 被误判；只有平台回执/查询确认才进入 confirmed。
5. 数字人直播具备授权、事实、敏感内容、延迟、人工接管、停播和事故审计门。
6. 断网、Token 失效、限流、重复回调和平台侧成功但本地超时都能安全恢复。

---

## 2. 平台范围与能力状态规则

首批范围：微信视频号、微信朋友圈、抖音、小红书、今日头条、闲鱼。每个平台单独形成 `228-` 前缀核验文档，仍直接放在本目录；核验前统一状态为 `UNKNOWN`，不是 `SUPPORTED`。

### 2.1 当前代码与接口现实

- 当前 `aos-platform m1@bc9711a` 没有可用于上述六平台的 canonical Connector runtime、installation store、capability registry 或生产发布 router。
- 前端出现的 `search_web` 仅为文字映射，不代表存在真实网络研究 Tool，更不代表社交平台能力。
- 现有 RuntimeAdapterRegistry 的显式注入、只读/副作用元数据、超时和并发约束可以复用，但必须新建平台 adapter 并经过安全注册。
- 现有进程内 Tool registry、idempotency 和部分 L4 Automation 不具备完整租户/持久化/职责分离，禁止作为 G5 生产真源。
- 本方案不宣称任何平台当前支持具体开放能力；G5.0 必须在开发当期用官方资料和测试账号回读 OpenAPI/回执后冻结结论。

能力枚举：

```text
account_connect
profile_read
content_draft_export
content_publish
content_status_read
metrics_read
comments_read
comment_reply
direct_message_send
lead_event_receive
product_bind
live_session_create
live_stream_push
live_comments_read
live_reply
```

状态为 `UNKNOWN|UNSUPPORTED|MANUAL_ONLY|READ_ONLY|WRITE_REQUIRES_REVIEW|SUPPORTED`，并保存官方 URL、核验时间、应用/账号类型、权限 scope、审核前提、地区、配额、收费、核验人和证据 hash。

---

## 3. 统一 Connector 契约

### 3.1 安装与账号

```yaml
connector_installation_id: ci_...
connector_type: social.wechat_channels
org_id: ...
project_id: ...
account_ref: opaque-token
secret_ref: secret://...
capability_snapshot_id: cap_...
status: pending_auth|active|degraded|revoked
markings: []
```

### 3.2 调用信封

```yaml
operation: content.publish
installation_id: ci_...
capability_snapshot_id: cap_...
input_ref: content-asset-revision
action_proposal_ref: null
idempotency_key: ...
deadline_at: ...
```

响应统一为 `accepted|confirmed|pending|rejected|unknown`，带 provider request token、provider object token、retryability、rate-limit snapshot、observed_at 和脱敏错误。外部 ID 不作为全局可信主键。

### 3.3 Adapter 元数据

每个 operation 声明 `read_only`、`external_side_effect`、`reversible`、`requires_action_approval`、`timeout`、`max_concurrency`、`rate_limit_bucket`、`pii_level` 和支持的媒体/内容约束。

---

## 4. 授权、安全与回调

- OAuth 使用 state、PKCE（平台支持时）、严格 redirect allowlist 和一次性 nonce；不接受前端传回的 org/project。
- Secret/token 存储在密钥系统；数据库只保存 secret_ref、scope、过期时间和 key version。
- webhook 验证签名、时间窗、nonce/event id 和原始 body hash；验签前不解析为业务事件。
- 回调处理幂等；未知 tenant/account、过期签名、重放和 schema 不兼容进入隔离队列。
- 出站请求使用固定 provider host allowlist、DNS/IP/重定向约束、超时、响应大小上限和脱敏日志。
- Token 刷新使用单飞锁和 CAS；revoked 后立即阻断新调用，排队任务不得继续。
- 账号解绑保留审计与历史回执，但删除/失效凭据引用。

---

## 5. 内容与媒体发布分级

| 级别 | 能力 | 默认策略 |
|---|---|---|
| L0 | 生成渠道格式 Draft、下载/复制 | G5 初始开放 |
| L1 | 人工在平台发布，AOS 登记 URL/回执 | 人工核验后开放 |
| L2 | 官方 API 读取内容状态/指标/评论 | capability+只读授权后开放 |
| L3 | 官方 API 创建发布 Draft/预约 | 需要 ActionProposal 与审批 |
| L4 | 直接发布、回复、私信 | G6 严格 Action 门，默认关闭 |

媒体资产校验：MIME、大小、时长、分辨率、比例、字幕、封面、版权/授权、内容 hash、病毒扫描和平台约束。任何自动转码都生成新 asset revision，不覆盖原文件。

发布状态机：

```text
local_draft → ready_for_action → submitted → provider_pending
  → provider_confirmed|provider_rejected|unknown
provider_confirmed → retracted（仅平台支持且另行批准）
```

超时不能自动视为失败并重发；先按 provider request/idempotency token 查状态，避免重复发布。

---

## 6. 指标、评论与线索回流

- 原始 webhook/API 响应进入隔离层，保存 schema version、hash 和最小必要原文；解析后形成标准事件。
- 指标按平台定义保存原始 metric id、时间粒度、时区、窗口和更新时间，不强行把不同平台指标同名合并。
- 评论/弹幕先做内容安全、PII/Secret、注入与语言检查，再生成受控摘要/意图；不直接晋升记忆。
- LeadSignal 必须有 consent 来源或标记 unknown；unknown 只能进入人工核验，不能触达。
- 删除/隐藏内容或平台修正指标通过 revision/adjustment event 处理，不篡改历史快照。
- 数据参谋的跨渠道报告引用每个平台的 capability 和数据截止时间。

---

## 7. 数字人交互式直播

### 7.1 关键对象

| 对象 | 内容 |
|---|---|
| `DigitalHumanProfileRevision` | 形象/声音/语言/风格、授权证据、禁用范围 |
| `LivePlanRevision` | 目标、平台、时段、商品、脚本、人员、护栏、停止条件 |
| `LiveKnowledgeSnapshot` | 商品/价格/库存/政策 revision 与有效期 |
| `LiveSession` | provider refs、运行状态、operator、Action refs |
| `LiveInteraction` | 脱敏问题、意图、response Draft/结果、延迟、风险 |
| `LiveIncident` | 触发规则、人工接管、停播、影响与复盘 |

### 7.2 运行链路

```text
脚本/素材/商品事实准备
  → factuality/safety/copyright Evals
  → 人工批准 LivePlan revision
  → 创建 ActionProposal
  → G6 批准并启动
  → 弹幕输入清洗与意图分类
  → 只读知识检索
  → 回复 Draft/低风险自动播报（策略允许时）
  → 高风险人工接管/立即静音或停播
  → 会话结束、指标回流、事故与效果复盘
```

硬门：医疗/金融/法律承诺、辱骂冲突、未成年人、个人隐私、价格/库存冲突、平台规则不明、模型/知识不可用均转人工或静默；不得自由调用支付、退款、库存或客户联系方式。

### 7.3 运行指标

端到端响应延迟、超时率、人工接管率、事实错误率、敏感拦截率、停播耗时、互动/咨询/成交/投诉、资源成本。增长指标不能压过安全指标。

---

## 8. API 建议

```text
GET    /v1/connectors/catalog
POST   /v1/connectors/installations
POST   /v1/connectors/installations/{id}/oauth:start
GET    /v1/connectors/oauth/callback/{provider}
GET    /v1/connectors/installations/{id}/capabilities
POST   /v1/connectors/installations/{id}/refresh-capabilities
POST   /v1/connectors/webhooks/{provider}
POST   /v1/connectors/operations:invoke
GET    /v1/connectors/operations/{id}
POST   /v1/domains/ecommerce/growth/live-plans
POST   /v1/domains/ecommerce/growth/live-plans/{id}/evaluate
POST   /v1/domains/ecommerce/growth/live-sessions
POST   /v1/domains/ecommerce/growth/live-sessions/{id}/takeover
POST   /v1/domains/ecommerce/growth/live-sessions/{id}/stop
```

写 operation 在 G6 前统一返回 `ACTION_APPROVAL_REQUIRED`；不能通过直接调用 adapter 绕过服务层。

---

## 9. 计划新增/修改文件

```text
services/aos-api/aos_api/connectors/
  contracts.py
  capability_registry.py
  installation_store.py
  oauth_service.py
  webhook_service.py
  runtime.py
  routers/connectors.py

bundles/platforms/social-<provider>/
  bundle.yaml
  backend/<provider>_adapter/
  capabilities/
  oauth/
  webhooks/
  evals/

services/aos-api/alembic/versions/
  228_connector_runtime_core.py

bundles/solutions/ecommerce-growth/
  backend/ecommerce_growth/g5/
    social_event_service.py
    live_contracts.py
    live_service.py
    live_safety.py
    routes.py
  frontend/growth/connectors/
    ConnectorCatalogPage.tsx
    ConnectorAccountPage.tsx
    CapabilityMatrix.tsx
    OperationTrace.tsx
  frontend/growth/live/
    DigitalHumanProfilePage.tsx
    LivePlanEditor.tsx
    LiveControlRoom.tsx
    LiveIncidentPanel.tsx
  evals/g5/
  migrations/006_growth_g5_social_live.py
```

平台插件各自形成 PlatformAdapterPack；公共 runtime、契约、extension registry 和平台迁移由集成负责人维护；增长业务模型留在 SolutionPack。账号 secret_ref 和 capability snapshot 在 InstanceOverlay/installation 中绑定。

### 9.1 数据库迁移与凭据边界

迁移新增 installation、capability snapshot、OAuth nonce/state、operation/attempt/receipt、webhook event/quarantine、rate-limit、媒体 revision、LivePlan/Profile/Session/Interaction/Incident 等表。Secret/token 不入业务表；只保存 secret_ref、scope、key version 和过期时间。

upgrade 后所有 provider 写旗标保持关闭，先完成授权撤销、签名和回执回读。downgrade 前必须停新 operation、reconcile pending/unknown、revoke 或解绑凭据；历史回执和审计保留只读。媒体派生物按 retention 清理，不删除仍被内容/直播 revision 引用的资产。

---

## 10. 分小波与测试

| 小波 | 内容 | 退出门 |
|---|---|---|
| G5.0 | 六平台官方能力与账号权限核验 | 每个平台 capability snapshot 有官方证据/日期/结论 |
| G5.1 | 通用 Connector/OAuth/Webhook/回执 | 双租户、Secret、SSRF、签名、重放、幂等、限流通过 |
| G5.2 | L0/L1 Draft/人工登记与统一工作台 | 状态诚实、媒体校验、无外部副作用 |
| G5.3 | 获批平台的 L2 只读指标/评论/线索 | schema、延迟、删除修正、注入/PII 通过 |
| G5.4 | L3/L4 Action adapter（默认关闭） | 与 G6 集成前只允许负向测试 |
| G5.5 | 数字人直播沙箱与控制室 | 授权、事实、安全、接管、停播、故障注入通过 |

测试覆盖 OAuth 攻击、错误 tenant、签名伪造、回调重放、Token 竞态、429/5xx、超时未知态、重复发布、断网恢复、平台 schema 漂移、媒体病毒/版权元数据、直播提示词注入和人工接管。

---

## 11. 风险、回滚与退出门

风险：平台政策/接口变化、账号封禁、重复发布、凭据泄漏、评论投毒、版权/肖像/声音争议、数字人事实错误和无法及时停播。通过 capability snapshot、逐级开放、Action 审批、kill switch、账号级限流与人工控制室治理。

每个平台独立旗标和 kill switch；公共旗标为 `growth_connectors_enabled`、`growth_connector_writes_enabled=false`、`growth_digital_human_enabled=false`。回滚撤销新调用、保留回执查询和审计；Token 泄漏时立即 revoke/rotate。

G5 退出门：能力核验不是推测；通用 Connector 安全门通过；L0～L2 在获批平台真实可回读；数字人只在沙箱/批准环境验证；写能力仍受 G6；G0～G5 累计回归通过。

# W7-10 发布 Variant 的 Impact、Action 与 Receipt 预检 ADR

> 日期：2026-08-15；实施复核：2026-08-26  
> 决策：`APPROVED_FOR_READ_ONLY_IMPLEMENTATION / EXTERNAL_EFFECT_BLOCKED / NO_RELEASE`  
> 当前基线：`AOS-000265`、`aos-platform/m1@1bd0857b`；W7-05、W7-06、W7-09 code-contract-browser GREEN

## 1. 当前事实

通用 AIP Action 已有 Proposal、Draft、Approval、ExecutionLease、immutable Receipt、unknown/reconcile 和 maker/approver/executor 分离；Canonical Draft Inbox 能区分 approved、applied、unknown、reconciled，并在命令后回读 authority。定向后端 20 项、前端 9 项测试通过。

这些只证明通用安全骨架。W7-05/06 未 GREEN，W5-00～07 均停在预检/实现阻断；生产 Action Adapter 注册为 0。当前 Adapter 只有 execute/reconcile，无 dryValidate/cancel/webhook/Usage contract；执行服务先 consume/commit Lease 再调用 Provider，存在 crash 无 Receipt 窗口；初始 Receipt evidenceRefs 为空，也无发布专用 observed object/hash schema。不能执行真实发布。

## 2. 决策

### 2.1 发布候选与影响

`PublishCandidateRevision` 固定 selected Variant content hash、family selection、同一 Artifact 四门 GateSet、独立 Approval、license/consent、平台/账号 scope 和 production context。`ImpactPreviewRevision` 由领域 calculator + Adapter dryValidate 生成，包含 diff、risk、reversibility、rate/capacity/budget/kill、平台限制，以及 exact ActionType/Capability/Binding/Account/Adapter/Policy/DryValidation refs。

### 2.2 Action 联合绑定与漂移

candidate、impact 和全部发布依赖计算为 `actionBindingHash`，由 Proposal、Approval、ExecutionLease、Attempt、Receipt、Usage/Settlement、lineage/effect 共同引用。Variant/GateSet/Approval/license/账号/platform schema/Policy/Adapter 任一漂移都使旧 Preview/Approval/Lease stale；Approval 只批准 exact bytes 和 exact destination。

### 2.3 执行、Receipt 与 unknown

生产发布要求 capability `code_green && operational_ready`、production Adapter、账号 probe、allowlist、预算/kill 和独立授权。durable Attempt/outbox 必须先于 submit 持久化。Receipt 记录 submitted/observed hashes、平台对象与状态、request fingerprint、Evidence、Usage refs 和 uncertainty；accepted/2xx 不等于 applied、settled、lineage projected 或 effect matured。unknown/late/partial 通过 reconcile append-only 推进，禁止盲发。

### 2.4 无 API 平台

无批准 API 或 Adapter 不就绪时创建绑定同一 candidate/impact 的人工 Handoff，固定最小披露、目的、expiry、账号、操作/核验清单与完成 Receipt。人工 checkbox 不得直接写 applied，仍需平台观察或明确 unverifiable 状态。

## 3. 验收

- exact Variant 与目标账号不串线，漂移后旧批准失败关闭；
- dryValidate、Preview、Approval、Lease、Attempt/outbox、Receipt/reconcile 同 binding；
- crash-before-submit、crash-after-submit、timeout、late webhook、partial、重复回调不重复发布；
- provider applied、费用结算、lineage、effect 四轴独立；
- kill、rate、budget、permission/marking、license 与恶意资产门可演练；
- 无 API Handoff 可审计但不伪装自动发布；
- `org-org/dev-project` 仅在独立授权下做小流量正向，`dev-org/dev-project` 只做负向隔离。

## 4. 两轮审查

### 第一轮：业务事实与安全边界

- 批准对象固定为 exact Variant bytes、四门结果和 exact destination；
- Impact、Approval、执行、Receipt、Usage、lineage、effect 不互相冒充；
- unknown、partial、late 与人工 Handoff 均有诚实状态；
- 真实发布保留独立授权与 kill/canary 门。

结论：`PASS`。

### 第二轮：复用与防越门

- 复用 canonical Action authority，不建媒体专用 Proposal/Receipt 真源；
- 修复生产 Adapter contract、联合 binding 与 durable outbox 前不进入实现；
- W7-05/06、W5 code-green/operational-ready、UI、双租户和真实 canary 未闭合时不勾选；
- 29 项通用测试不冒充发布成功或真实平台证据。

结论：`PASS_WITH_IMPLEMENTATION_AND_EXTERNAL_EFFECT_BLOCKED`。

## 5. 最终裁决

W7-10 合同已收敛为后续施工基线；实现与一切外部发布仍禁止。本轮未改代码、未做迁移、未访问真实租户、未调用 Provider。预检事实见 `.evidence/workshop/2026-08-15-w7-10-publish-variant-impact-action-receipt-preflight.json`。

## 6. 2026-08-26 实施复核与文件级清单

### 6.1 复核结论

1. W7-05 已提供 Artifact Family、selected Variant 与四门 GateSet authority；W7-06 已提供 review/return；W7-09 已把 frozen context、Stage/TaskRun、Family/GateSet/Issue 聚合为 Media Studio v4。
2. 通用 AIP Action 已提供 `ImpactPreviewRevision`、`ActionProposal/Approval/Lease/Attempt/Receipt` 与 unknown/reconcile 投影；工作台必须消费这些 canonical facts，不复制 Proposal、Receipt 或状态机。
3. W5/W7 的 code-green 仍不是 operational-ready。当前没有独立真实发布授权，因此 W7-10 只实现 GET-only v5 contribution；`publish`、`handoff-complete`、`replay`、`reconcile` 等写命令全部为 `allowed=false`。
4. `PublishCandidate` 在本波是由 exact selected Variant + GateSet + frozen ImpactPreview + canonical Proposal 联合校验得到的工作台贡献，不新建可写 authority。任一 revision/hash/binding 漂移即失败关闭。
5. 无 API 场景只展示受控人工核验要求与缺失事实；不创建外部任务、不暴露敏感载荷、不把人工 checkbox 解释为 applied。

### 6.2 163/164 分层落位

- 原子 Skill：读取 ImpactPreview 的 `CapabilityRevision` 与 `SkillBinding/CapabilityBinding` exact refs；无 exact ref 时保持 blocker。
- Logic 编排：读取 `planRef`、`productionContextRef` 与 proposal `taskId/runId`，不复制编排状态。
- 数字同事绑定：读取 preview `bindingRefs`，仅展示租户内绑定版本；主责仍为内容官，协作者为活动策划师、数据参谋、合规协作者。
- 工作台贡献：Media Studio 只呈现 Candidate → Impact → Action → Receipt → Handoff requirement，真实状态来自 canonical authority。

### 6.3 文件级实施清单

后端最小增量：

- `services/aos-api/aos_api/ecommerce_workshop_media_publish_contracts.py`：定义 v1 发布贡献、exact refs、联合绑定、Receipt 与 Handoff requirement 的严格只读合同。
- `services/aos-api/aos_api/ecommerce_workshop_media_publish.py`：按 tenant scope 聚合 Artifact Family/GateSet、ImpactPreview、Action Proposal/Approval/Execution Receipt；漂移、过期、缺失均输出独立 blocker。
- `services/aos-api/aos_api/aip_action_execution.py`：仅增加 scope-bound canonical read helper，原 principal API 委托该 helper；不改变任何写路径。
- `services/aos-api/aos_api/ecommerce_workshop_media_studio_contracts.py`、`ecommerce_workshop_media_studio.py`、`routers/ecommerce_workshop.py`：Media Studio v5 additive 接线，保留 v1～v4 兼容。
- `services/aos-api/tests/test_ecommerce_workshop_media_publish.py`、既有 router/OpenAPI 测试：覆盖 exact binding、跨租户/漂移、unknown、无 Receipt 与 no-API Handoff 失败关闭。

前端最小增量：

- `apps/web/src/api/ecommerceWorkshop/contracts.ts`、`parser.ts`、`parser.test.ts`、`mediaStudioPublishParser.test.ts`：新增 v5 严格类型与解析，拒绝可执行命令、错序、binding/hash 漂移和敏感载荷。
- `apps/web/src/components/workshop/MediaStudioPage.tsx`、对应测试与样式：展示 Candidate/Impact/Action/Receipt/Handoff 五段贡献，继续明确“无写入口”。

证据与交付：

- 运行后端专项与 W7 累计、OpenAPI 确定性、前端专项/全量、TypeScript、构建、安全扫描。
- 使用内置浏览器在 `org-org/dev-project` fixture 验收五段贡献、空态/blocked/unknown、1280 视口和 0 可执行发布按钮；fixture 只作 UI 合同验收，不冒充真实租户或 Provider 证据。
- 形成 W7-10 evidence、Delivery Receipt、安全提交；最后再串行 CAS 更新 authority、01/06 与 Prime。

### 6.4 实施门与回滚

- 无数据库迁移、无真实 Provider、无真实租户写、无 Action execute/reconcile、无外部发布、无 release。
- 新 v5 字段 additive；删除 v5 接线即可回退到 v4，原 v1～v4 parser/API 保持兼容。
- 若 canonical Action 或 Artifact authority 无法稳定只读，W7-10 必须 `blocked`，不得以 mock、localStorage、手工状态或第二套真源补齐。

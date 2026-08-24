# W4-02 EvidenceCitation、三层披露与 Marking 执行预检 ADR

> 状态：`REVIEWED / IMPLEMENTATION_BLOCKED`
>
> 事实截面：AOS authority `AOS-000024`；证据 `.evidence/workshop/2026-08-14-w4-02-evidence-disclosure-preflight.json`。

## 1. 审查结论

AIP W2-A 已有 EvidenceBundleRevision PostgreSQL authority、Canonical list/get 与严格前端 parser；AIP Memory/Wiki 另有较成熟的 KnowledgeCitation，能校验 marking、freshness、applicability、payload exact ref 和 citation/chunk/token 对齐。这两部分可以复用 Store 和设计原则，但不能混为同一 authority。

W4-02 当前仍被以下事实阻断：

1. Bundle 只返回 exact Evidence refs，没有按 ref 解析受控 Evidence 的 Canonical read/disclosure API。
2. Bundle list/get 只建立登录主体的 TenantScope，没有用 `principal.markings` 执行 Bundle 自带 marking，受限元数据可能越权可见。
3. 没有 server-owned “摘要—引用片段—完整来源”三层披露决策、脱敏 Receipt 和审计事件。
4. Evidence ref 只有 id/revision/hash，尚不是可展示引用；缺 source locator、采集时间、适用性、marking、license、redaction 与安全片段。
5. 当前 licenseSummary 来自调用方，读取时也未按 purpose 重新裁决 license/minimum disclosure。
6. 页面只有 Bundle 摘要卡，没有 EvidenceBundleDrawer、引用跳转和逐级授权交互。

## 2. Authority 划分

| 对象 | 唯一 authority | 说明 |
|---|---|---|
| EvidenceBundleRevision | AIP Production Contract Store | 不可变 manifest；不复制正文 |
| Evidence | AIP Evidence Store | 原始/派生证据及其不可变、撤销事实 |
| EvidenceDisclosureDecision | AIP Policy/Disclosure service | purpose、marking、license、freshness、redaction、level 裁决 |
| EvidenceCitation | AIP Disclosure service | 显示安全且可核验的 citation envelope |
| KnowledgeCitation | AIP Memory authority | 仅用于正式 Memory/Wiki 查询，不能冒充 EvidenceCitation |
| EvidenceBundleDrawer | Workshop 公共 UI | 只消费 read model 和 disclosure commands，不持有 authority |

## 3. 三层披露

### L1：安全摘要

默认只返回 source type/provider、observed/captured time、freshness、applicability、marking 标签、license 状态、content hash 前缀、conflict/revoked 状态和引用计数。即使正文不可见，也要明确显示 blocked reason；不得用空白伪装不存在。

### L2：最小引用片段

调用方提交 exact EvidenceRef、purpose、subject/task context 和 requested level。服务端校验当前 marking/license/revoke/freshness 后返回最小 excerpt、精确 locator、redaction receipt、decision hash 和审计 ref。片段长度与字段按 purpose policy 决定。

### L3：完整来源

仅在独立权限与更高风险门通过后返回短期 scoped source ref/stream；不把正文嵌入分享链接、Bundle 或浏览器长期缓存。下载/导出另走 ActionProposal/Approval/Receipt，不能因已获得 L2 自动升级。

每次升级都重新裁决，L1 allow 不推出 L2/L3 allow。撤销、license 或 marking 变化立即影响新读取；历史 Citation/Receipt 保留当时事实但不得继续充当访问令牌。

## 4. Canonical 契约

建议命令：

```text
POST /v1/aip/evidence/disclosures/resolve
GET  /v1/aip/evidence/disclosures/{decisionId}
```

请求至少包含 exact evidence ref、purpose、requested level、Task/Subject context、Idempotency-Key。响应包含 status=`allowed|blocked|stale|unknown`、stable reasons、Citation、display payload、redaction Receipt、expiresAt 和 decision hash。blocked/unknown 不返回片段或 source ref。

Bundle list/get 本身先执行 bundle-level marking；Drawer 展开每个 item 时再执行 item-level disclosure，不批量预取正文。

## 5. 工作台交互

Drawer 展示 Bundle coverage/missing/conflict/uncertainty，再按 item 展示 L1。用户请求“查看引用”或“查看来源”时明确显示用途、权限、脱敏和有效期；服务端拒绝时展示 reason 与可申请动作。键盘焦点、aria-expanded、loading/blocked/stale/expired 都有稳定语义。

浏览器不得自行：

- 用本地 markings 判断最终权限；
- 从 Evidence payload 生成“安全摘要”；
- 重算 redaction、license 或 citation hash；
- 将完整正文写入 localStorage、URL 或日志。

## 6. 验收门

- Bundle list/get 对缺少 marking 的主体失败关闭且不泄露条目数量、refs 和 subject。
- item disclosure 同时验证 tenant、purpose、marking、license、freshness、revoke 和 exact hash。
- L1/L2/L3 权限互不隐式继承，每次都有 Receipt；blocked/unknown 零正文。
- Citation 与返回片段/hash/locator 精确对齐，篡改或跨租户 ref 失败关闭。
- 撤销或许可变化后新读取立即 blocked/stale，旧 Receipt 仍可审计但不能授权。
- Drawer 完整覆盖 loading/empty/partial/blocked/stale/unknown/expired，页面刷新不丢 authority 状态。

## 7. 明确废弃与禁止

- 废弃“Bundle 有 itemRefs 就能直接打开 Evidence 正文”的假设。
- 禁止用前端 `hasMarkingAccess` 作为服务端访问控制替代品。
- 禁止用 KnowledgeCitation 直接包装基础 Evidence，二者 authority 和生命周期不同。
- 禁止一次 Bundle 请求批量返回所有正文或永久 source URL。
- 禁止把调用方填写的 licenseSummary 当作当前许可裁决。

这些废弃项不减少证据透明度；它们确保用户看到的每一层内容都可解释、可授权、可撤销，而不是用“透明”之名扩大泄露面。

## 8. 2026-08-25 S4 / W4-02 实施增补

### 8.1 当前事实与缺口

- 当前强一致 authority 为 `AOS-000226`；S3 仅已达到代码、测试和浏览器验收闭环，没有因此获得发布、Provider 或外部副作用授权。
- 服务端已有 `POST /v1/aip/evidence/disclosures/resolve`、`GET /v1/aip/evidence/disclosures/{decisionId}`、Bundle marking 过滤和持久化 decision，但用途、许可、时效、citation 对齐仍不完整。
- Web SDK 尚无 Disclosure 严格 parser/operation/client；`EvidenceBundleDrawer` 仅显示 exact ref，没有三层披露交互，也未接入实际工作台页面。
- 本波遵循 163/164 的“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献视图”：Disclosure 作为服务端原子能力，工作台只呈现其精确决策与证据引用，不伪造 Logic 执行、数字同事贡献或运行成功。

### 8.2 本波文件级清单

| 范围 | 文件 | 最小改动 |
|---|---|---|
| 服务端契约 | `services/aos-api/aos_api/aip_production_contracts.py` | 收紧 purpose 与 Disclosure 返回语义，保持现有 API 路径和字段兼容。 |
| 服务端裁决 | `services/aos-api/aos_api/aip_production_contract_store.py` | 每次重新校验 exact ref、tenant、purpose、marking、license、freshness、revoke；blocked/stale/unknown 零正文。 |
| API 验收 | `services/aos-api/tests/test_w_l10_evidence_revoke_disclosure.py` | 补足许可拒绝、过期、purpose 越级、篡改 exact ref、跨租户和 citation/hash 对齐。 |
| Web 契约 | `apps/web/src/api/aip/operations.ts` | 登记 resolve/get Disclosure operation。 |
| Web 严格 SDK | `apps/web/src/api/aipEvidence/contracts.ts`<br/>`apps/web/src/api/aipEvidence/client.ts` | 增加三层决策严格 parser 和 SDK，不在浏览器重算授权或脱敏。 |
| 公共组件 | `apps/web/src/components/workshop/production/EvidenceBundleDrawer.tsx` | 按 item 显式请求 L1/L2/L3，呈现 loading/blocked/stale/unknown/expired，禁止批量正文预取。 |
| 实际页面 | `apps/web/src/pages/s2/ProductionContractsPage.tsx` | 在证据包卡片中接入 Drawer，只传递 authority 返回的 exact refs。 |
| Web 验收 | `apps/web/src/components/workshop/production/production.test.tsx` 及相关 SDK/page tests | 覆盖分层升级、拒绝零正文、过期、焦点恢复和页面接线。 |
| 交付证据 | `.evidence/workshop/2026-08-25-w4-02-evidence-citation-disclosure.json` 及 Task/Delivery Receipt | 记录代码 SHA、专项/累计测试、内置浏览器和未授权边界。 |

### 8.3 实施与发布边界

- 不新增数据库迁移；复用已有 decision JSONB 字段，不在真实租户执行迁移或回放。
- 不在浏览器验收中触发真实 Disclosure 写入、离线队列 flush、下载、导出、Action、Approval、AgentRun 或 Provider 副作用。
- 旧 decision 保持可审计，但不作为新访问令牌；L3 仅返回短期 scoped ref，本波不实现源正文下载。
- 完成仅可声明 `CODE/TEST/BROWSER GREEN`；未经独立发布门不得声明运营、实时数据或发布 GREEN。

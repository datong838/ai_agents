# W4-01 Evidence Build Job、八领域 Required Facts 与 Evidence 治理预检 ADR

> 日期：2026-08-14；实施刷新：2026-08-24
> 项目 authority：`AOS-000213 / S3_W3_03_PREPARE_AGGREGATE_CODE_GREEN_S3_IN_PROGRESS_NO_RELEASE_MIGRATION_NOT_APPLIED`
> 状态：`CODE_CONTROL_GREEN / EARLY_BRIDGE_COMPLETE / NO_RELEASE / MIGRATION_NOT_LIVE_APPLIED`
> 边界：已完成代码、迁移文件、契约与测试；未 live apply 迁移、未修改真实租户业务数据、未发布 Profile/Bundle

## 1. 结论

AIP W2-A 已提供 `EvidenceBundleRevision` PostgreSQL authority、Canonical create/list/get API 和只读 strict SDK，但它只是低层持久化命令，不是 W4-01 所需的 Evidence Build Job。

当前 `CreateEvidenceBundleRequest` 由调用方直接提交 coverage、missing、conflicts、uncertainties、freshness、marking 和 licenseSummary；Store 只核对 frozen Brief 与 Evidence ID/hash，没有根据签名 required-facts profile 选择 Evidence、计算覆盖、处理冲突、裁决许可/标记/最小披露或生成可复核 Build Receipt。仓内也没有八 Module required-facts/evidence-selection profile。

基础 `aip_evidence` 还没有 revision/revoke 生命周期；初始 migration 向 runtime 授予 UPDATE/DELETE，未发现 mutation guard。故在宣称“source revoke/hash drift 产生新 Bundle revision”前，必须先关闭 Evidence 不可变与撤销治理门。

## 2. 当前能力分层

| 能力 | 当前实现 | 判定 |
|---|---|---|
| Bundle PostgreSQL authority | immutable revision row、TenantScope、RLS、Idempotency Receipt | `CODE_PRESENT` |
| Bundle Canonical API/SDK | create/list/get、严格读取 parser | `CODE_PRESENT` |
| Evidence exact ref | 检查同租户 Evidence ID 与 content hash | `CODE_PRESENT` |
| Build Job | 无 Job/状态机/Receipt/恢复入口 | `MISSING` |
| required-facts profiles | 八 Module 0 份 | `MISSING` |
| coverage/missing/conflict/uncertainty | 客户端提交，服务端不计算 | `UNTRUSTED_INPUT` |
| purpose/marking/license/redaction | Bundle Store 不做选择裁决 | `MISSING` |
| Evidence revoke/expiry/revision | 基础表无相应生命周期字段 | `MISSING` |
| Evidence append-only | runtime 仍有 UPDATE/DELETE，未发现 guard | `RED` |

已有 W2-A 持久化测试 `6 passed` 只能证明当前低层合同稳定，不能作为 W4-01 完成证据。

## 3. 四层放置

### L0 AIP

- Evidence immutable/revoke authority；
- 通用 `EvidenceBuildJob`、状态机、幂等、取消/恢复和 Build Receipt；
- 通用 required-facts profile resolver；
- selection、coverage、freshness、conflict、uncertainty、purpose、marking、license、redaction 裁决；
- 只向现有 `EvidenceBundleRevision` 写最终 manifest，不复制 payload。

### L1 电商领域资产包

按八 Module 发布签名 profile，描述 required/optional fact type、允许来源类型、freshness、minimum coverage、conflict policy、marking/license/minimum-disclosure 和降级规则。Profile 使用 stable ID + exact revision/hash，通过 installation lock 解析；不包含租户数据和真实账号。

### L2/L3

Adapter 提供来源 capability、许可与 freshness 事实；租户 overlay 只能在 Schema 允许范围内收紧阈值或禁用来源，不能把缺失事实改成已覆盖。

## 4. 八 Module Profile 最小方向

| Module | required-facts 重点 |
|---|---|
| 日常任务总控 | Task/Run/Stage、阻塞、审批、来源 Module ref |
| 内容与活动 | 商品/人群/Offer、品牌与平台规则、素材许可、预算 |
| 统一运营 | 原始订单/库存/履约/售后事件、政策、金额、SLA |
| 达人邀约 | 来源许可、身份/去重、匹配、频控、合同/履约标准 |
| 多媒体生产 | 素材/肖像/版权、品牌事实、平台规范、技术规格 |
| 经营参谋 | 指标 definition/value/quality/cutoff、归因证据、反证 |
| 价格治理 | 同款依据、报价 originals、freshness、许可、政策 |
| 客户关系 | identity、consent、purpose、retention、旅程/频控规则 |

每个 profile 都必须定义 unknown/partial/blocked 的机器规则，不能由页面文案自由解释。

## 5. 实施门

### Red

1. 客户端提交 `complete` 但缺 required facts 必须失败。
2. Evidence 被更新、删除、撤销、过期、hash 漂移或不满足 purpose/marking/license 时旧 Build 不得继续 ready。
3. 错租户、未安装 profile、错误 hash、Profile rollback、未知来源 capability 均失败关闭。
4. Build 重放、取消、恢复和并发必须守恒，不能生成双 Bundle。

### Green

1. 先补 Evidence append-only/revoke authority；涉及 migration 必须取得唯一 Lease。
2. 发布并 exact 解析八 Module profiles，placeholder=0。
3. Build Job 服务端确定性计算 manifest 与 coverage，输出 Build Receipt。
4. source revoke/hash drift 产生新的 readiness/Bundle revision 或明确 stale，不覆盖历史输入。
5. Workshop 只消费 Job/Bundle refs 和安全摘要，Drawer 按权限延迟取正文。

## 6. W3-04 依赖解环整改

原清单把 W4-01 置于 `W3-14 → W4-01`，同时 W3-04 又要求冻结 EvidenceBundle exact ref；W3-03 只创建 EvidenceBuildRequest 并坚持零 Provider 执行，因而形成 `W3-04 → ... → W3-14 → W4-01 → EvidenceBundle → W3-04` 的循环。该顺序不得靠空 Bundle、客户端上报 complete 或在 prepare 中隐藏执行绕过。

W4-01 现定义为跨波 early bridge：依赖 W3-02 已发布 required-facts/evidence-selection profile、W3-03 EvidenceBuildRequest、DEP-C0 与 Evidence immutable/revoke authority；完成后向 W3-04 提供 canonical EvidenceBundle。它不依赖 W3-14。W4-02～08 仍在 W3-14 后实施和累计验收，不因 bridge 提前而放宽披露、Eval、Wiki、Query 或浏览器安全门。

无环顺序及四合同组合冻结见 `93-W3-04四合同ProductionContext组合冻结与依赖解环ADR.md`。

## 7. 当前门禁

- `DEP-C0-EVIDENCE-BUNDLE-AUTHORITY`：`CODE_CONTROL_GREEN`；
- `DEP-EVIDENCE-BUILD-JOB`：`RED`；
- `DEP-EVIDENCE-REQUIRED-FACTS-PROFILES`：`RED`；
- `DEP-EVIDENCE-IMMUTABILITY-REVOKE`：`RED`；
- `DEP-EVIDENCE-MINIMUM-DISCLOSURE`：`RED`；
- W3-02/W3-03：未完成；
- W3-14：不再是 W4-01 的前置，仅继续阻断 W4-02～08；
- W4-01：`NOT_STARTED / IMPLEMENTATION_BLOCKED`。

机器证据：`aos-platform-w2-workshop/.evidence/workshop/2026-08-14-w4-01-evidence-build-preflight.json`。

## 8. AOS-000213 实施刷新与最小文件清单

2026-08-24 重新反查当前 `m1` 后，原预检有三项事实已过时：

1. W-L9 已将 `BuildEvidenceBundleRequest` 固定为 server-owned coverage，Store 会按 Evidence payload 的 fact ids 计算 complete/partial/blocked、conflict 与 freshness；不再接受客户端提交 coverage。
2. W-L10 已有 append-only Bundle revoke event 与最小披露 decision authority；因此本波复用它们，不重建 Bundle authority 或 disclosure 模型。
3. W3-02 已形成八 Module 的 typed ProductionProfile 候选，`evidenceSelection.requiredFacts` 可作为 required-facts 唯一来源；候选仍 `NO_RELEASE`，默认运行必须因未安装 exact Profile 失败关闭。

当前真实缺口收敛为：基础 `aip_evidence` 仍向 runtime 开放 UPDATE/DELETE 且没有 Evidence 自身 revoke event；现有 Bundle build 仍由调用方直接提交 `requiredFactIds/itemRefs`；W3-03 preparation result 中的 `EvidenceBuildRequest` 没有 canonical early bridge。

### 8.1 本波文件级切片

| 切片 | 文件 | 最小改动 |
|---|---|---|
| W4-01A | `services/aos-api/alembic/versions/w4_001_evidence_governance_build.py` | revoke Evidence 的 runtime UPDATE/DELETE，增加 append-only Evidence revoke event 与 tenant RLS；只交付 migration code，不 live apply |
| W4-01A | `services/aos-api/aos_api/aip_production_contracts.py`、`aip_production_contract_store.py`、`routers/aip_production_contracts.py` | 增加 Evidence exact revoke contract/API；Bundle build 重读 revoke event 并失败关闭，不改变历史 Bundle |
| W4-01B | `services/aos-api/aos_api/ecommerce_workshop_prepare_store.py`、`ecommerce_workshop_evidence_build_service.py`、`routers/ecommerce_workshop.py` | 由 preparation exact result + installed ProductionProfile + canonical Evidence refs 生成唯一 Bundle；required facts 不从请求体接收 |
| W4-01C | `services/aos-api/tests/test_w4_001_evidence_governance_build_migration.py`、`test_ecommerce_workshop_evidence_build.py` 及 OpenAPI | 覆盖租户、revoke/hash/profile drift、同 key replay/conflict、missing/partial/complete、0 Provider/Run/Action/外部写 |
| 证据 | `.evidence/workshop/2026-08-24-w4-01-early-evidence-build.json` | 专项、累计、浏览器、迁移单头、方案一致性与副作用守恒 |

### 8.2 冻结合同与边界

- Workshop build 请求只允许 `preparationId + productionProfileRef`；tenant 只来自 Principal，required facts、Brief ref、Evidence refs、cutoff/purpose/marking 均从 canonical preparation result 重读。
- Build 前必须复验 preparation complete、Profile exact installed/digest、module/profile 一致、draft Brief exact ref；随后由公共 Brief authority在独立显式步骤 freeze，再调用唯一 Bundle builder。不能接收客户端 coverage 或用空 Evidence 冒充 complete。
- Evidence revoke 是新事件，不 UPDATE/DELETE Evidence payload；旧 Bundle 通过 source revoke/readiness 变 stale/blocked，历史内容与 Receipt 不改写。
- 本波不发布/安装 W3-02 Profile，不执行 live migration，不调用 Provider，不创建 TaskRun/AgentRun/Action/Handoff/Approval/Lease，不修改真实业务数据，也不授权 release。

状态更新为 `IN_PROGRESS / W4-01_EARLY_BRIDGE_STARTED / NO_RELEASE / MIGRATION_CODE_ONLY / NO_EXTERNAL_EFFECT`。

### 8.3 累计回归发现后的兼容性整改

- 既有 `aip_evidence_disclosure` 路由文件与 W-L10 测试存在，但未登记进唯一 domain router manifest，导致运行时 404。本波将它登记到 `domain_manifest.json` 并由生成器更新 `domain_aggregates.py`，恢复原设计能力；不新增另一套 Disclosure authority。
- 重新生成聚合时发现既有 `aip_fde` 仅存在于生成物、未进入 manifest；若直接生成会静默丢失三个既有 operation。本波同步补回该 manifest 项，确保确定性生成且功能不倒退。
- Evidence append-only 生效后，旧 W2-A/W-L10 测试夹具不能再直接 DELETE 基础 Evidence。夹具改为保留使用随机 ID 的不可变测试 Evidence，只清理 Bundle、Brief、Receipt 等可清理关联记录；绝不为测试恢复 UPDATE/DELETE 权限。
- 路由恢复会在现有两个 W4-01 路由之外再增加两个既有 Disclosure operation；OpenAPI 路径、Schema 与 operation 总数只能按确定性导出结果同步，不接受未解释漂移。

## 9. 实施验收结论（2026-08-24）

- `w4_001` 成为唯一 migration head；迁移文件关闭 base Evidence 的 UPDATE/DELETE/TRUNCATE，新增 tenant RLS + append-only revoke event，未对任何 live 数据库执行迁移。
- Workshop `build-evidence` 只接收 preparation id 与 exact Profile ref；required facts、Brief、Evidence refs、cutoff 与 marking 全部从 canonical preparation + installed Profile 重读。Profile 未安装、引用漂移、空 Evidence、source revoke 均失败关闭。
- 源 Evidence revoke 具备 exact hash、TenantScope、幂等 Receipt；同 key 重放事件不变，`dev-org/dev-project` canary 无法读取 `org-org/dev-project` Evidence；撤销后新 Build 返回 `422 EVIDENCE_REVOKED`。
- 专项 8 passed；Workshop/W3/W4/AIP 邻接累计 169 passed + 2 subtests；OpenAPI、router manifest、compileall、diff check GREEN。确定性 OpenAPI 为 2569 paths / 2120 schemas / 4337 operations。
- 内置浏览器 `/workshop` 在 1280 宽度下 `scrollWidth=width=1280`、H1=1、active installation=0、API/目录失败明确展示、可执行 Evidence/Bundle 发布按钮=0；未把代码控制面伪装成已发布能力。
- Provider、费用、Run、Action、Handoff、Approval、Lease、外部业务写、live migration apply 均为 0；因此结论仅为 `CODE_CONTROL_GREEN / NO_RELEASE`。

W4-01 early bridge 已关闭 W3-04 的 EvidenceBundle 输入缺口；下一任务回到 `W3-04`，复用既有 W-L11 ProductionContext authority，不重建 L0 合同。

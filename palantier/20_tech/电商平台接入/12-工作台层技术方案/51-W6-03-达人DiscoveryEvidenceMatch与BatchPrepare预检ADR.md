# W6-03 达人 Discovery、Evidence、Match 与 Batch Prepare 预检 ADR

> 初始预检：2026-08-14；施工复审：2026-08-25
> Authority：`AOS-000245`
> 代码基线：`m1@d9b1e58`
> 证据：`.evidence/workshop/2026-08-14-w6-03-creator-discovery-match-batch-prepare-preflight.json`
> 当前结论：`IMPLEMENTATION_AUTHORIZED / PLAN_FROZEN / NO_EXTERNAL_EFFECT / NO_RELEASE`

## 1. 审查结论

当前通用 ResearchJob、TaskBrief、EvidenceBundle、Eval、Impact 与已安装 Module Shell 可复用，定向后端 22 项、前端 18 项通过。但仓内没有达人领域 authority、治理后的 Match、身份去重或 OutreachBatch prepare；Module descriptor 的 view/production/responsibility/impact refs 为空，Eval 仍是 placeholder。因此 W6-03 不得勾选，也不得把通用底座、领域名词清单或静态视觉稿当作已实现。

这不是 Goal 历史 `blocked` 推导出的判断，而是对当前 `AOS-000027`、Git、Bundle、服务、API、页面与测试的重新核验。

## 2. 可复用与不可复用边界

可复用：

- ResearchJob 的 exact provider capability、manifest hash、幂等、事件顺序、Artifact/Delivery Receipt 和 reconcile；
- TaskBrief/EvidenceBundle/Eval/Impact 的 revision、exact ref、CAS/Receipt 基础；
- Workshop active installation、canonical route、readiness/blocker 与失败关闭外壳。

不可冒充：

- generic ResearchJob 不等于 Creator Discovery profile 或合法来源；
- caller-supplied Evidence coverage/licenseSummary 不等于 Evidence Build；
- generic sync `BatchCommand` 不等于 OutreachBatch；
- Bundle 中的 requiredObjects 名称不等于已存在的 schema/store/API；
- Shell pending 页面不等于达人五阶段读模型。

## 3. 决策

W6-03 实现必须按以下顺序，且每步均有独立 test/Receipt：

1. 冻结 CreatorDiscoveryProfile、Creator required-facts、Match policy/feature schema、OutreachBatch schema；
2. 建立 tenant-scoped 领域 authority 与 RLS/append-only/CAS，不复制公共真源；
3. 以 canonical ResearchJob Artifact 进入受控 Normalizer，完成许可/Schema/hash/PII gate；
4. 建立身份 alias/conflict 与稳定去重，保留 originals；
5. 分离 Match Observation 与人工/政策 Decision，低置信度保持 PRELIMINARY；
6. 实现 side-effect-free prepare/freeze、item 数量守恒、频控/容量/预算与漂移 invalidation；
7. 更新 Bundle exact refs、Module API/SDK/五阶段读模型与无障碍；
8. 累计 contract/store/API/frontend/security 验收。W6-04 的 start/触达/寄样/合同/佣金不得提前进入本波。

## 4. 当前阻断事实

| ID | 当前事实 | 解除条件 |
|---|---|---|
| `DEP-W6-CREATOR-DOMAIN-AUTHORITY` | 领域 contract/store/service/API 为 0 | additive authority + tenant/CAS/Receipt 测试 GREEN |
| `DEP-W6-CREATOR-BUNDLE-CONTRACT` | 四类 refs 为空，Eval placeholder | 发布并锁定 exact refs，不保留 placeholder |
| `DEP-W6-CREATOR-DISCOVERY-PROFILE` | 无来源/许可/Schema/最小披露 profile | 签名 profile 与 Adapter contract GREEN |
| `DEP-W6-CREATOR-EVIDENCE-SELECTION` | Evidence facts 由调用方自报 | W4 EvidenceBuildJob + creator required-facts GREEN |
| `DEP-W6-CREATOR-MATCH-AUTHORITY` | 无 Observation/Decision/PRELIMINARY | 同版 feature/model/policy/evidence authority GREEN |
| `DEP-W6-CREATOR-IDENTITY-DEDUPE` | 无 alias/conflict/dedupe authority | originals 守恒和冲突人工门 GREEN |
| `DEP-W6-CREATOR-FREQUENCY-CAPACITY` | 无频控/历史联系/容量/预算快照 | exact policy/snapshot/item eligibility GREEN |
| `DEP-W6-CREATOR-BATCH-PREPARE` | 无 prepare/freeze/CAS/零副作用契约 | 数量守恒、幂等、0 Action/Lease 测试 GREEN |
| `DEP-W6-CREATOR-READ-MODEL` | 仅公共 Shell pending 页 | 五阶段读模型、PRELIMINARY、阻断/a11y GREEN |
| `DEP-W6-CREATOR-UPSTREAM-GATES` | W4-08、W6-01 未勾选 | 两项正式 GREEN 后重新核验 |

## 5. 双轮审查记录

### 第一轮：范围与真源

- PASS：达人领域资产与 AIP/O1/Adapter 公共 authority 分治；
- PASS：Observation/Decision、prepare/start、批次与外部 Action 已拆分；
- PASS：PII、许可、Secret、来源 originals 和真实租户边界明确；
- 整改：原 13 文档没有定义身份冲突、数量守恒、exact freeze refs 和漂移失效，已补齐。

### 第二轮：可施工性与失败关闭

- PASS：每个 P0 缺口均有稳定依赖 ID 和解除条件；
- PASS：`prepare 0 触达`、PRELIMINARY 禁淘汰、输入数量守恒、unknown/reconcile 可测试；
- PASS：未把 W6-04 外部动作或通用 sync batch 混入本波；
- PASS：当前结论仍为 `NOT_STARTED / IMPLEMENTATION_BLOCKED`，没有虚假完成或越门编码。

## 6. 复审结论

产品目标和技术目标完整，W6-03 的可施工目标契约通过本次文档复审；当前实现未通过 W6-03 验收。安全下一步是在上游门释放后按第 3 节顺序编码，不得先造页面或用 placeholder/mock 绕过领域 authority。

## 7. 2026-08-25 施工复审与文件级清单

### 7.1 实时依赖结论

- `W4-08`、`W6-01`、`W6-02` 已有代码、合同与 Delivery Receipt 闭环；`AOS-000245` 的强一致投影均为 CURRENT，memory validate 与 state-change gate 为 GREEN。
- 当前唯一开发者具备跨 AIP、领域与工作台维护权限，原“等待上游交付”不再成立；但来源许可、租户隔离、PII、外部触达、迁移 apply 与发布门仍保持失败关闭。
- W2-04 已存在只读双轴五阶段壳、候选/Match/Batch 的基础领域合同与 append-only reader。本波复用这些资产，不创建第二份 Creator authority。

### 7.2 163/164 组合约束

W6-03 不实现一个新的“大 Skill”。服务端冻结以下组合并将 exact refs 投影到工作台：

```text
frame-recruitment-brief
→ build-evidence-pack
→ segment-entities
→ ecommerce-creator-match
→ compare-alternatives
→ plan-responsibilities
```

- `ecommerce-creator-match` 是领域 Logic；原子 Skill、Logic publication、ResponsibilityPlan 与 Agent/数字同事绑定均消费 canonical exact refs。
- 主责数字同事为导购顾问，数据参谋、内容官、活动策划师为协作角色；页面只展示贡献与 readiness，不本地创建 SkillBinding/AgentRun。
- `CreatorBatch` 只能由 Module Application Service 调用 canonical authority 创建；前端不得串联多个 API 拼出“成功”。

### 7.3 最小文件范围

后端：

- 新增 `services/aos-api/aos_api/ecommerce_workshop_creator_prepare.py`：W6-03 严格合同与应用服务，覆盖 DiscoveryProfile、NormalizerReceipt、IdentityResolution/Conflict、Match Observation/Decision、Batch prepare/freeze 与贡献视图。
- 新增 `services/aos-api/aos_api/ecommerce_workshop_creator_prepare_store.py`：tenant-scoped append-only authority、CAS、幂等、漂移复核与零副作用事务。
- 新增 `services/aos-api/aos_api/routers/ecommerce_workshop_creator_prepare.py` 并仅挂载 prepare/freeze/read API；禁止 start/send/ship/sign/commission endpoint。
- 新增 `services/aos-api/alembic/versions/w6_003_creator_prepare.py`：唯一 head、RLS/FORCE RLS、append-only trigger；本波只验证 migration graph，不 apply 真实数据库。
- 更新 `services/aos-api/aos_api/main.py`、OpenAPI operation inventory 与生成快照。

前端：

- 扩展 `apps/web/src/api/ecommerceWorkshop/creatorGrowth.ts` 与 client：严格解析 W6-03 贡献/准备视图。
- 扩展 `apps/web/src/components/workshop/CreatorGrowthPage.tsx` 和样式：保留五阶段双轴，新增来源许可、PRELIMINARY、数量守恒、原子 Skill→Logic→数字同事→工作台贡献以及 `prepare 0 触达`，不增加动作按钮。

测试与证据：

- 新增后端合同/store/API/migration 测试，覆盖许可/hash/schema/PII、originals 守恒、冲突不自动合并、低置信度 PRELIMINARY、频控/容量/预算、exact ref 漂移、CAS/幂等、跨租户与 0 Action/Lease。
- 更新前端 strict parser/page/a11y 测试；执行 W6 累计后端、Workshop 累计前端、TypeScript、production build、OpenAPI deterministic export、Alembic unique head 与 diff check。
- 使用内置浏览器验收 `/workshop/creator-growth`，保存 W6-03 EvidencePack；完成方案/代码一致性复审后写 Delivery Receipt、关闭 Lease、CAS authority，并自动进入 W6-04。

### 7.4 不回退门

历史 Creator authority 与 W2-04 只读响应保持向后兼容；旧记录缺少 W6-03 exact contribution refs 时必须显式显示 legacy/blocked，不自动补造、不回填真实达人、不降低现有测试。任何外部 provider 调用、邀约、寄样、合同、佣金、Action Proposal 或 ExecutionLease 都不属于本波。

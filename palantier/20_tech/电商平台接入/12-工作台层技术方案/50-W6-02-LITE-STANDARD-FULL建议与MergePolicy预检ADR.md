# W6-02 LITE / STANDARD / FULL 建议与 MergePolicy 预检 ADR

> 日期：2026-08-14  
> 核查基线：历史预检 `w2-workshop@6cc7bb9 / AOS-000027`；实施基线 `m1@c835c9d / AOS-000244`  
> 状态：`IMPLEMENTED_GREEN / CODE_CONTRACT_BROWSER_GREEN / NO_EXTERNAL_EFFECT / NO_RELEASE`
> 边界：只新增 profile 建议、确认、MergePolicy 与 immutable Receipt authority 及其只读消费；不改真实安装、不触发 TaskRun 或 Provider

## 1. 结论

当前 ResponsibilityPlan 能保存 profile、slots 和 merge decisions，并阻止 `independent_review`、`hard_compliance`、`external_publication_approval`、`receipt_reconciliation` 四类硬职责被合并；后端 8 项、前端 13 项专项测试 GREEN。但 profile 只是任意字符串，电商包中没有签名 LITE/STANDARD/FULL 模板，没有建议器、用户确认或版本化 MergePolicy。merge 也未校验槽位图、能力并集、模板覆盖或漂移。

因此现状只是通用数据形状基础。W6-02 不编码本地替代 authority，保持未勾选。

## 2. ProfileRecommendation 与用户确认

建议器输入 frozen Brief/Evidence/Eval refs，以及内容形态、渠道数量、风险/法规、品牌等级、素材授权、预算、交付时限、资产复用、Provider readiness 与组织 policy。它输出不可变 `ProfileRecommendationRevision`：推荐档位、候选模板 exact ref、理由、风险提升规则、可合并/不可合并职责、成本/时长区间、unknown 和 expiry。

建议器只建议，不修改 Brief、不 freeze ResponsibilityPlan、不启动 TaskRun。用户通过 `ProfileConfirmationReceipt` 接受或选择允许的更高档位；降档必须满足 policy floor，给出理由并重新计算覆盖/风险。合规红线、素材授权缺失或 required facts unknown 时不得通过手工备注降档。

## 3. 签名模板

LITE/STANDARD/FULL 不是全行业固定三张表，而是稳定 profile key + VerticalPack 签名 `ResponsibilityTemplateRevision`：

- LITE 可合并相邻策划/创作，但仍保留目标、事实/授权、独立审核、批准与结果对账；
- STANDARD 展开脚本、视觉/分镜、生成/采集、后期与综合审核等常规职责；
- FULL 保留制片、导演、编剧、美术、分镜、摄影/生成、剪辑/后期、评估、发布运营等专业责任，并按任务分配执行者，不冻结 Agent 数量。

模板固定 required/optional slots、responsibility type、input/output contracts、gate/return、merge group、separation rule、minimum profile 和 policy refs。八 Module 通过 installation lock 引用 exact template，不复制到页面或 BFF。

## 4. MergePolicy authority

`MergePolicyRevision` 定义可合并 responsibility pairs/groups、禁止集合、assignee capability union、separation、最大跨度、风险上限、组织覆盖与 expiry。每个 `MergeDecisionReceipt` 至少固定：source/target slot exact refs、policy exact ref、actor、reason、evidence、risk result、assignee binding、capability union、createdAt 和 content hash。

服务端校验：

1. source/target 均存在于 exact template/plan，source 不含 target，合并组不重叠/成环；
2. merged responsibility types 与来源槽一致，target 保存全部 input/output/gate/return 责任；
3. target assignee 对 required capability、权限、容量和 marking 的并集 readiness 为 GREEN；
4. 独立审核、硬合规、外部动作批准和 Receipt 对账永不与其被审核/批准/对账对象的生产职责合并；
5. 未合并职责仍全部 covered，不能靠删除 source slot 获得 complete。

## 5. Freeze、漂移与 UI

ResponsibilityPlan freeze 同时固定 recommendation、confirmation、template、merge policy、merge decisions 与 assignee resolution refs。Brief 风险、渠道、素材许可、预算、Provider readiness、template/policy publication 发生变化时旧 recommendation stale，Plan 回到需确认；系统不得静默重算并沿用旧确认。

UI 先展示建议理由、成本/时长/风险与 unknown，再让用户确认。责任矩阵始终可展开原职责、合并理由、执行者、输入输出、质量门和退回目标；“一个执行者承担多责”不折叠掉责任行。禁用/阻断显示 reasonCode 与修复动作。

## 6. 当前施工门与验收

W6-01 exact assignee readiness、W3-02 签名模板和 W3-07 coverage/reassign 必须先 GREEN。随后：

- 发布至少按八 Module/内容形态覆盖的 LITE/STANDARD/FULL exact templates；
- 同一输入/策略生成确定 recommendation hash，过期/漂移失败关闭；
- 用户接受、升档、允许/禁止降档均有 Receipt；
- merge 的缺槽、假槽、重叠、环、能力不足、职责分离冲突全部拒绝；
- 执行者数量减少不影响 required responsibility coverage；
- `dev-org/dev-project` 无法读取或使用 `org-org/dev-project` 的模板、策略、建议、确认与 merge Receipt。

机器证据见 `.evidence/workshop/2026-08-14-w6-02-profile-merge-policy-preflight.json`。

## 7. 2026-08-25 实时差异复核与文件级施工清单

历史结论中的 W6-01、Router 注入与八 Module template refs 缺口已经关闭；当前真正缺口收敛为：`profile` 仍是任意字符串，`MergeDecision` 只有 loose shape，ResponsibilityPlan 未绑定 recommendation/confirmation/policy/decision Receipt，也没有独立建议与确认 authority。当前 active installation 是否包含某个三档模板仍必须由 installed exact resolver 判定，不能因 Candidate Bundle 存在而宣称可用。

本波采用 additive、失败关闭的最小实现：

- `services/aos-api/aos_api/aip_responsibility_profile.py`
  - 固定稳定 profile key `LITE/STANDARD/FULL`；定义 recommendation、confirmation、MergePolicy、MergeDecisionReceipt 的 exact 合同；
  - 建议由结构化风险/渠道/unknown 输入和 exact candidate template/policy refs确定性生成，不调用模型、不写 Brief、不 freeze Plan。
- `services/aos-api/aos_api/aip_responsibility_profile_store.py`
  - 只在 tenant 内验证 exact installed template 和 published/unexpired policy；按 policy floor 计算档位与 hash；
  - 确认只允许接受推荐档或升档；降档必须满足 policy floor，任何 stale/hash/template drift 失败关闭；
  - merge Receipt 校验 source/target 真实存在、无重叠/自环、保护职责不可合并、能力并集等于目标所需能力，且目标 assignee 的 W6-01 exact fresh Receipt 覆盖并集。
- `services/aos-api/alembic/versions/w6_002_responsibility_profiles.py`
  - additive 创建四类 tenant-scoped authority 表，RLS、append-only Receipt 与 exact hash/expiry 约束；
  - ResponsibilityPlan revision additive 保存 recommendation、confirmation、MergePolicy exact refs 与 MergeDecisionReceipt IDs；历史行 nullable、可读但不可作为新 freeze 依据。
- `services/aos-api/aos_api/aip_production_contracts.py` 与 `aip_production_contract_store.py`
  - profile 收紧为稳定枚举；新建/修订 Plan 可绑定四类 exact authority；freeze 时要求它们同租户、同 recommendation、未过期且完整覆盖 merge decisions；
  - 未合并责任行不删除，“一人多责”不能伪装成责任消失。
- `services/aos-api/aos_api/routers/aip_production_contracts.py`、`main.py` 与 OpenAPI
  - 增加 canonical create/read/confirm/merge-decision 路由，沿用 Principal TenantScope、Idempotency-Key 与 Store authority；不增加执行或发布入口。
- `services/aos-api/tests/aip/test_w6_02_responsibility_profiles.py`、迁移/ProductionPlan/API 测试
  - 覆盖确定性建议、升降档、stale/hash/tenant drift、假槽/重叠/保护职责/能力并集、Receipt replay 与历史兼容。
- `apps/web/src/api/ecommerceWorkshop`、`ProductionContractsPage.tsx` 及测试
  - 只读展示 recommendation→confirmation→merge policy/Receipt 链和阻断原因；页面不自行重算、不把建议等同确认或 freeze。
- `.evidence/workshop/2026-08-25-w6-02-profile-recommendation-merge-policy.json`
  - 固化专项、累计、OpenAPI、迁移、浏览器与无副作用结论。

不回填历史 Plan，不修改 Bundle Candidate 或 active installation，不静默选择/降档，不启动 TaskRun，不调用外部 Provider；涉及页面时必须用内置浏览器验收，未安装路径只能记为失败关闭处置，不能冒充正向 GREEN。

## 8. 2026-08-25 实施与验收结论

W6-02 已按第 7 节完成 additive 实施：三档建议器、用户确认、版本化 MergePolicy、MergeDecisionReceipt、ResponsibilityPlan 治理引用、四个 canonical API、`w6_002` 单迁移头和上线执行审批只读贡献视图均已落地。方案/代码一致性复审额外补齐了 merge group 重叠/成环拒绝、Receipt 对基线 Plan 与 source/target/type shape 的精确匹配，以及 freeze 时重新核验 recommendation、confirmation、policy、merge Receipt 和 assignee readiness。

验收事实：

- 后端专项与累计 `24 passed`，前端专项 `21 passed`；TypeScript、production build、compileall、OpenAPI 双进程确定性检查、`w6_002 (head)`、diff check 全部 GREEN；
- 内置浏览器验收 `http://localhost:5173/aip/production-contracts`：现有历史职责计划明确显示“未固定档位建议与合并策略”，同时提示兼容读取不代表可用于新生产组合；冻结按钮和启动门保持禁用；
- 没有回填真实租户、修改 installation、启动 TaskRun/Agent/Provider、自动改档/合并或发布；
- 代码提交 `aos-platform/m1@bf88eff`；机器证据 `.evidence/workshop/2026-08-25-w6-02-profile-recommendation-merge-policy.json`。

结论：`W6_02_PROFILE_RECOMMENDATION_CONFIRMATION_MERGE_POLICY_CODE_CONTRACT_BROWSER_GREEN / NO_EXTERNAL_EFFECT / NO_RELEASE`。下一串行入口为 W6-03。

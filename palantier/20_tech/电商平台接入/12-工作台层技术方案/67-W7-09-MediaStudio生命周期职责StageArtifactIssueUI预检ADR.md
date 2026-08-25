# W7-09 Media Studio 生命周期、职责、Stage、Artifact 与 Issue UI 预检 ADR

> 日期：2026-08-15；2026-08-26 串行复核
> 决策：`IMPLEMENTATION_ACTIVE / W7_03_TO_W7_08_GREEN / NO_EXTERNAL_EFFECT / NO_RELEASE`
> 当前基线：`AOS-000264`；`m1@d5a185e9`；前置 W7-03～W7-08 已全部代码/合同/浏览器 GREEN

## 1. 当前事实

`ecommerce.media-studio` 的 module identity、路由、所需对象/能力/AIP feature 和 legacy redirect 已进入签名 Bundle；动态目录、安装投影、唯一导航、通用壳、H1/skip-link/readiness/专注模式均已存在。通用 Production Contracts 页能诚实展示 Brief/Evidence/Eval/Responsibility/Stage/Relation/Issue 的真实空态或阻断态，通用 TaskRun 面板能从服务端恢复状态。

但这不是 Media Studio 产品面。当前 manifest 的 `viewRefs`、`productionContractRefs`、`responsibilityTemplateRefs`、`impactCalculatorRefs` 均为空，Eval 仍为 placeholder；Host 没有传入媒体子视图，只显示“业务视图将在 W2 接入”。没有媒体专属 read model、SDK、生命周期、职责矩阵、Stage/Artifact/Issue、费用/结算或 command capability。通用 Logic Graph 面板会从 UI 创建/批准 Task 与 Plan，不能用来绕过媒体 ProductionStart。

## 2. 决策

### 2.1 一个上下文、三个语义 Tab

页面沿用现有 Workshop 壳和视觉层级，不复制视觉稿样例。三个 Tab 固定为“生产上下文”“职责与执行”“交付与复盘”，共享同一 module installation 与 frozen production context。跨 Tab blocker、unknown 与待人工干预数始终可见；切换不按最新时间重新拼接数据。

### 2.2 全生命周期可见与可干预

顶部轨道展示 `prepare → freeze/confirm → compile/approve → start/run → review/return → deliver/publish → reconcile/effect-review`。每个节点显示服务端状态、exact ref/hash、actor/Agent、时间、Evidence/Receipt、阻断和可执行命令；未发生节点明确为 not_started/blocked/not_applicable。新 attempt、返工、接管、取消和迟到 Receipt 都追加到时间线，不覆盖旧事实。

### 2.3 三组信息责任

- 生产上下文：Brief、Evidence、Eval、ProfileRecommendation/Confirmation、ImpactPreview；
- 职责与执行：八专业槽、merge/assignee/capability readiness、Stage DAG/attempt/lease/fence/Checkpoint/暂停/接管/Provider；
- 交付与复盘：Artifact family/Master/Variant、四门同版 Eval、ReviewIssue/ReturnDecision、Approval/Action/Delivery、Usage/Settlement、EffectReview。

八职责槽必须全部可见，但 Agent 和人数按任务动态分配；merge 不吞审核、批准、对账或职责分离。Artifact/Issue/成本视图均展示 exact lineage、unknown 与不确定性。

### 2.4 命令与诚实交互

所有命令能力由服务端返回 `allowed + reasonCode + expectedVersion + requiredExactRefs`。按钮 disabled 时显示具体原因；提交携带 Idempotency-Key/ETag，unknown outcome 时禁止重复，完成后回读 authority。前端不创建第二套 Task/Plan/Stage/Artifact/Issue 状态，不用倒计时、动画或 Mock 数据冒充运行。

页面必须有唯一 H1、语义 tablist/tab/tabpanel、完整键盘操作与焦点恢复、live status/alert、非颜色唯一编码、reduced-motion，以及 stale/partial/forbidden/empty/failed/blocked 的稳定呈现。

## 3. 验收矩阵

1. 生命周期：每个节点及回退、返工、暂停、接管、取消、unknown/reconcile 可追溯；
2. 职责：八槽完整，merge/coverage/assignee/capability/SoD/Handoff 有据；
3. Stage：DAG、attempt、lease/fence、Checkpoint、Provider 与复用/失效事实一致；
4. Artifact/Issue：family topology、冲突/选择、四门同版、Issue→Return→新 attempt 闭环；
5. 成本：Capacity、Budget、Usage、cancel、Settlement 和币种差异分开；
6. 安全：tenant/marking/permission、恶意资产、Secret、外部动作门失败关闭；
7. 状态：loading/empty/blocked/partial/stale/forbidden/failed/unknown 全覆盖；
8. 租户：`org-org/dev-project` 正向和 `dev-org/dev-project` 隔离 canary；
9. 无障碍：H1、tab、键盘、焦点、读屏、非颜色、缩放与 reduced-motion；
10. 浏览器：读模型与每个允许/禁止命令均从服务端回读，不出现 Mock 或视觉稿假数据。

## 4. 两轮审查

### 第一轮：产品目标与信息完整性

- Palantir 式“后台不黑盒完成”落实到完整生命周期、Evidence/Receipt、阻断和干预入口；
- 三 Tab 收敛信息密度但不隐藏职责、Stage、Artifact、Issue 或成本事实；
- 八职责责任保留，Agent 数量和协作方式自适应；
- 与现有页面风格、壳、导航和无障碍基线一致。

结论：`PASS`。

### 第二轮：authority 与越门风险

- MediaStudioView 只组合 canonical refs，不形成第二业务真源；
- 通用 Contracts/TaskRun 只复用展示模式，不复用不符合媒体组合门的写流程；
- W7-03～08、manifest refs、read model、SDK、UI、浏览器与双租户证据未闭合前保持 disabled；
- 48 项基础测试只证明壳/目录/通用页面稳定，不冒充 W7-09 产品验收。

结论：`PASS_WITH_IMPLEMENTATION_BLOCKED`。

## 5. 2026-08-26 文件级实施清单

W7-09 不新增媒体业务 authority 或迁移；它只在同一 tenant/cutoff/context 下组合现有 canonical authority，并继续按 163/164 呈现“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献”。本轮最小写集：

1. `services/aos-api/aos_api/ecommerce_workshop_media_studio_contracts.py`：升级 v4，新增生命周期节点、八职责槽、Stage attempt、Artifact family、四门、Issue/Return 与服务端 command capability 只读合同；旧 v1/v2/v3 保持兼容。
2. `services/aos-api/aos_api/ecommerce_workshop_media_studio_lifecycle.py`：新增 tenant-bound canonical composer，读取 ProductionContext、ResponsibilityPlan、ProductionStart/TaskRun、ProviderJob、ArtifactFamily、MediaGateSet、ReviewIssue/ReturnDecision 与 Finance；所有依赖均有上限并按 exact ref/context 关联，读取失败只降级对应分区。
3. `services/aos-api/aos_api/ecommerce_workshop_media_studio.py`、`routers/ecommerce_workshop.py`：把 v4 生命周期贡献注入既有 GET-only Media Studio view；不创建第二 Task/Stage/Artifact/Issue 状态机。
4. `apps/web/src/api/ecommerceWorkshop/contracts.ts`、`parser.ts`：严格解析 v4 新分区与旧版本兼容；拒绝越界计数、重复职责槽、跨 context 漂移与伪 allowed command。
5. `apps/web/src/components/workshop/MediaStudioPage.tsx`、测试与 scoped CSS：三 Tab 共用 frozen context，展示生命周期、八职责、Stage/attempt、Artifact/四门/Issue/Return/费用；命令只展示 `allowed/reasonCode/requiredExactRefs`，本波不增加执行按钮；补键盘、焦点、非颜色状态、窄屏与 1280px 验收。
6. `services/aos-api/tests/test_ecommerce_workshop_media_studio.py`、新增 W7-09 composer 测试及 OpenAPI/Web 回归：覆盖同 context join、八槽守恒、Stage/Artifact/Issue 归属、unknown/partial/conflict、跨租户、dependency partial failure、稳定 cutoff、刷新恢复和零外部副作用。
7. `.evidence/workshop/2026-08-26-w7-09-*`：固化专项/累计/OpenAPI/安全/内置浏览器证据；不访问真实 Provider、不 live apply migration、不写真实业务数据、不发布。

实施退出仍需满足：同一 frozen context 的三 Tab、八职责 8/8、Stage/Artifact/Issue/成本分轴、服务端命令能力失败关闭、strict SDK、全量回归与内置浏览器均 GREEN。任何正向真实运行、真实 Provider、Action、发布或 Effect 不属于本波授权。

## 6. 最终裁决

W7-09 产品与技术合同继续作为施工基线。AOS-000264 已证明 W7-03～08 前置闭合，因此原 `IMPLEMENTATION_BLOCKED` 解除并进入最小实现；这不提升真实 Provider、外部动作或发布许可。历史预检事实仍保留在 `.evidence/workshop/2026-08-15-w7-09-media-studio-lifecycle-responsibility-stage-artifact-issue-ui-preflight.json`，不得覆盖。

## 7. 2026-08-26 实施与验收闭环

本轮按第 5 节最小写集完成 v4 只读聚合，没有新增迁移或第二套业务真源：

- 服务端从同一 tenant/cutoff/frozen context 聚合八职责、ProductionStart、TaskRun、ProviderJob、ArtifactFamily、GateSet、ReviewIssue、ReturnDecision 与财务引用；上下文为空时返回可信空，多上下文且无 exact selector 时失败关闭。
- 页面三 Tab 共用同一生命周期贡献，展示七节点、八职责、Stage/attempt/Provider、Artifact Family 与 Review Issue；六类 command capability 由服务端返回且全部 `allowed=false`，没有执行按钮。
- 旧 v1/v2/v3 继续由严格 SDK 兼容解析；v4 拒绝职责槽乱序、伪 `allowed=true`、非 canonical 生命周期与漂移 hash。
- 专项后端 `17 passed`，W7-03～09 累计后端 `59 passed`；OpenAPI/domain `22 passed + 2 subtests`，确定性导出为 `2666 paths / 2378 schemas / 4443 unique operations / 4453 route rows`。
- Web 定向 `2 files / 7 tests`，全量 `233 files / 2144 tests`，类型检查与 `344 modules` 生产构建通过。
- 内置浏览器在 `org-org/dev-project` 本地只读 fixture 下完成 1280px 三 Tab 验收：七节点、八职责、TaskRun/Provider Stage、Artifact Family、Review Issue 与六类禁用命令可见；document/body 均为 1280px，无横向溢出、无新增 console error、无业务写入口。
- scoped security `22 files / 0 critical / 0 warning`，scanner 单测 `9 passed`；全仓既有基线仍为 `4910 files / 5 critical / 326 warning`，不得据此发布。

证据固化于 `.evidence/workshop/2026-08-26-w7-09-media-studio-lifecycle-ui.json` 与同日 browser 目录。裁决为 `CODE_CONTRACT_BROWSER_GREEN / SECURITY_SCOPED_GREEN / REPO_BASELINE_RED / NO_REAL_PROVIDER / NO_EXTERNAL_EFFECT / NO_RELEASE`；W7-09 只完成代码、合同和浏览器层闭环，不能冒充真实 Provider、运营或发布就绪。

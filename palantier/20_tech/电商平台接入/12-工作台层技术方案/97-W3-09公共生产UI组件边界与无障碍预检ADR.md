# W3-09 公共生产 UI 组件边界与无障碍预检 ADR

> 日期：2026-08-25
> 状态：`W3-09_CODE_BROWSER_GREEN / NO_RELEASE / NO_EXTERNAL_EFFECT`
> 范围：基于 `AOS-000220`、W3-03～08 已提交合同和当前 m1 页面实施唯一公共生产 UI 包；不修改静态视觉稿、数据库、真实租户或外部系统。

## 1. 结论

公共组件方向成立，但当前 9 个命名组件均未独立实现。已有 `ProductionContractsPage` 能读取 Brief、Evidence、Eval、Responsibility、Stage、ArtifactRelation、ReviewIssue，并证明部分真实空态、blocked reason 与 fail-closed；它同时包含七类 authority 卡片和 freeze/compile/review 命令，不应复制到八 Module。

W3-09 冻结唯一 `apps/web/src/components/workshop/production` 包：组件只显示 canonical DTO/read model、server commandReadiness 并发出 typed intent；页面 orchestrator 才调用 SDK、显示 Receipt、回读 authority。W3-03～08 已形成 code-control 基线但未 release，因此本波只开放纯展示、typed intent seam 与 disabled/blocked 资格，不扩大任何外部副作用权限。

组件公共头必须同时呈现 `原子 Skill exact ref → Logic exact ref → 主责数字同事/实际 assignee → 当前工作台贡献`，缺任一项时显示 unknown/blocked，不用角色名替代 Skill，不把数字同事复制成大 Skill，贯彻 163/164 的组合链。

## 2. 现有可复用底座

- `AsyncStateBoundary`、`CapabilityBlocker`；
- `EcommerceWorkshopCatalogContext/Host/Shell`；
- `InstalledModuleNavigation`；
- `aipProductionContracts` strict parser/client 与 `ProductionContractsPage` 基础测试。

这些只证明 Shell、部分状态和 authority API 可复用，不证明九组件、八 Module 接入、Dialog/Timeline 无障碍或真实 command readiness 已完成。

## 3. 唯一组件包

| 组件 | 输入 | 只允许输出 |
|---|---|---|
| BriefInspector | Brief exact DTO、Diff、blockers | revise/freeze intent |
| EvidenceBundleDrawer | Bundle/Citation/marking read model | select/request-more intent |
| EvalContractBadge/Diff | exact Contract、dependency state、Diff | select/rerun/open-lineage intent |
| ResponsibilityMatrix | slots、coverage、Resolution Receipt/readiness | resolve/reassign/takeover intent |
| StageTimeline | Plan/Run/Step/Stage/Checkpoint projection | inspect/pause/return intent |
| ArtifactRevisionViewer | family/relation/selection projection | compare/select intent |
| ReviewIssuePanel | Issue/Decision/attempt lineage | resolve/return intent |
| ImpactPreviewDialog | frozen Preview、Diff、risk/cost/unknown | confirm/cancel intent |

共享 primitives 为 `ExactRefLink`、`ReadinessBadge`、`BlockerList`、`ReceiptLink`、`AuthorityStateBoundary`。组件不直接实例化 SDK/Store，不创建 idempotency key，不持久业务状态，不猜测 latest ref，不自算 readiness。

## 4. 九态与命令诚实性

loading、empty、partial、stale、blocked、forbidden、unknown、ready、failed 分开。stale/partial 只保留带 cutoff 的旧内容；unknown 不归零；blocked 控件可聚焦并显示 reasonCode/requiredAction。Intent 发出后页面显示 pending，不乐观写 authority；canonical command 返回 Receipt 后再刷新。

## 5. 无障碍与视觉边界

- 页面拥有唯一 H1/nav/main/skip link，组件从 H2/H3 开始；
- Dialog/Drawer 首焦点、trap、Escape、关闭返回触发器；
- Tab 只在真正互斥 panel 使用，并具 tablist/tab/tabpanel、roving tabindex、Home/End；
- Timeline/Diff/图形提供列表、表格或文本摘要；颜色和图标不是唯一编码；
- status/error live region、200% 缩放、visible focus、reduced-motion 全覆盖；
- W3-09 不修改瞬时静态 HTML 视觉稿，只继承现有视觉 token 与布局。

## 6. 依赖与验收

W3-03～07 runtime、公共 read models、ImpactPreview strict SDK 和 accessible dialog/diff primitives 必须 GREEN 后才开放 mutation intent。测试至少覆盖 strict props/未知枚举/坏 ref、九态、键盘/焦点、Intent 与 command 分层、Receipt refresh、八 Module 单一 import identity、0 localStorage/mock/第二 authority。

正式浏览器验收覆盖八 Module × 1280/1440/1920；正向只认 `org-org/dev-project`，`dev-org/dev-project` 只作负向隔离。

## 7. 两轮审查

第一轮发现：原方案列出组件名，但未冻结目录、props/intent ownership，容易从单体页面复制八套状态机。整改后冻结唯一 package、shared primitives 与 page orchestration seam。结论：`PASS_AFTER_REMEDIATION`。

第二轮发现：仅要求“可访问”不足以验证 Dialog、Timeline、Diff 与 blocked controls。整改后冻结九态、焦点、键盘、live region、文本替代、缩放和 reduced-motion 矩阵，并明确不改静态视觉稿。结论：`PASS_AFTER_REMEDIATION`。

## 8. 2026-08-25 文件级实施清单

1. `apps/web/src/components/workshop/production/types.ts`：冻结九态、exact ref、blocker、Receipt、原子 Skill/Logic/数字同事贡献 lineage 与 typed intent 合同；
2. `primitives.tsx`：实现 `ExactRefLink`、`ReadinessBadge`、`BlockerList`、`ReceiptLink`、`AuthorityStateBoundary` 和贡献 lineage 的纯展示；
3. 九个命名组件分别落在 `BriefInspector.tsx`、`EvidenceBundleDrawer.tsx`、`EvalContractBadge.tsx`、`EvalContractDiff.tsx`、`ResponsibilityMatrix.tsx`、`StageTimeline.tsx`、`ArtifactRevisionViewer.tsx`、`ReviewIssuePanel.tsx`、`ImpactPreviewDialog.tsx`；
4. `index.ts` 为唯一 public import identity，`production.css` 只复用现有 token 并覆盖焦点、200% 缩放和 reduced-motion；
5. `production.test.tsx` 覆盖九态、unknown 不归零、blocked 控件可聚焦、typed intent、Dialog/Drawer 首焦点/Escape/return-focus、Timeline/Diff 文本替代及 0 SDK/localStorage；
6. `ProductionContractsPage.tsx` 只消费公共 primitives，页面继续拥有 SDK/刷新/Receipt orchestration，不把调用下沉到组件；
7. 完成专项、Web 累计、build、内置浏览器三视口与方案一致性复审，再形成 Evidence、Delivery Receipt、authority CAS 和 Prime 回读。

## 9. 2026-08-25 实施与验收闭合

唯一 public identity `components/workshop/production/index.ts` 已导出九个命名组件和五个共享 authority primitive。所有组件只接收严格 ViewModel、server 已允许的 intent kind 与 callback；组件目录扫描确认 SDK/client、localStorage/sessionStorage、`randomUUID` 引用均为 0。公共 frame 统一显示原子 Skill exact ref、Logic exact ref、主责数字同事/实际 assignee 和工作台贡献，缺失项保持 unknown。

专项测试覆盖九组件 import identity、九态、unknown 不归零、blocked command 可聚焦但不触发、typed intent、Drawer/Dialog 首焦点/焦点环/Escape/return-focus，以及 Timeline/Diff 文本替代，共 `24 passed`；Web 累计 `221 files / 2084 tests passed`，TypeScript/build GREEN。内置浏览器在固定 1280×720 视口验证 `/aip/production-contracts` 唯一 H1/main、API 不可用失败关闭与无横向溢出，未点击命令；当前工具不提供 1440/1920 视口切换，故不虚构三视口实跑，响应式规则由 CSS/build 覆盖并保留为后续累计浏览器矩阵项。

机器证据：`.evidence/workshop/2026-08-25-w3-09-common-production-ui.json`。结论：`CODE_BROWSER_GREEN / NO_RELEASE / NO_EXTERNAL_EFFECT`，不表示公共组件已在八 Module 全量挂载，也不表示 runtime、运营或发布 GREEN。

## 10. 当前决议

W3-09 目标合同、最小实现、专项/累计测试和 1280px 浏览器失败关闭验收已闭合。继续禁止组件直接调用 SDK/Store、创建幂等键、持久业务状态、推断 readiness 或执行真实命令；Delivery Receipt、authority CAS 与 Prime 回读闭合后进入 W3-10。

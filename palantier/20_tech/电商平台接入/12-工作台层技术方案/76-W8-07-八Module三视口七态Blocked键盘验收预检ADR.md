# W8-07 八 Module 三视口七态、Blocked 与键盘验收预检 ADR

> 日期：2026-08-15
> 状态：`ENGINEERING_ACCEPTANCE_CONTRACT_BROWSER_GREEN / OPERATIONAL_MATRIX_FAIL_CLOSED / NO_EXTERNAL_EFFECT / NO_RELEASE`
> 基线：`AOS-000034`、`w2-workshop@7ada162d4242b9dcc320b4965bfc9c82699346c2`、`m1@4018dd382c169fbed567c633bdbb698e6f26447f`
> 证据：`.evidence/workshop/2026-08-15-w8-07-eight-modules-three-viewports-state-keyboard-preflight.json`

## 1. 决策

W8-07 不是“把八个路由各截一张图”，而是同一 release、active installation 与 exact Module refs 下的可重复浏览器累计门。产品仍未正式封板，且 W1-10、W2-10、W3-14、W4-08、W5-08、W6-10、W7-11 均未 GREEN，所以本轮只冻结验收合同；不运行伪正向矩阵，不修改页面源码，不把现有诚实 blocked 壳记成八业务 Module 完成。

## 2. 唯一矩阵

验收主键固定为 `moduleId + activeInstallationRef + moduleRevision/hash + viewport + state + interactionPath + evidencePackRevision`。八 Module 是 task-cockpit、content-campaign、operations、creator-growth、media-studio、analyst、price-governance、customer；视口宽度固定 1280、1440、1920。

“七态/blocked”含义固定为：

- 七个异步态：`loading / empty / forbidden / stale / partial / failed / unknown`；
- 依赖态：`blocked`，单独验收 blocker、reasonCode、required action 与可聚焦 disabled control；
- 安装边界：`not-installed`；
- 正向内容边界：`ready`，只证明当前响应代表的能力，不推导 Agent、Provider、Action 或其他 Module operational。

若某 Module/状态组合按签名合同不适用，必须写 `not_applicable`、稳定原因与 contract ref，不能删去矩阵格。测试夹具可以触发边界单测，但不能形成生产正向 EvidencePack。

## 3. 键盘与无障碍合同

每页必须恰有一个 H1，具有稳定 nav/main landmark、skip link 和唯一 `aria-current=page`。Tab 组件使用 tablist/tab/tabpanel、`aria-selected/aria-controls` 与 roving tabindex；覆盖方向键、Home/End、Enter/Space、Tab/Shift-Tab 和 Escape。Dialog/Drawer 初始焦点落在摘要或首个安全控件，关闭后回到触发器；导航收纳、Focus Mode、重试与人工接管不得遗失焦点。

状态变化使用恰当 status/alert live region；状态与风险不能只靠颜色或在线圆点。200% 缩放不得遮蔽必需动作或产生键盘陷阱；`prefers-reduced-motion` 关闭非必要动画；图表必须提供文本摘要或表格，并显示 cutoff、假设和 unknown。

## 4. 三视口合同

- 1280：主区至少 70%，右抽屉默认关闭；导航可收纳但当前上下文与展开入口仍可见。
- 1440：左导航、主区和右抽屉可同时使用，焦点顺序与 DOM 阅读顺序一致。
- 1920：允许证据与任务并排，但不能复制同一交互、隐藏 blocker 或改变语义顺序。

视觉像素差异不是唯一门。需同时检查 zoom、长文案、unknown/blocked、最小触达尺寸、可见焦点、横向溢出和抽屉覆盖。

## 5. EvidencePack

每个实际验收格保存：production build SHA、Bundle/Installation/Module exact refs、tenant、data cutoff、URL、viewport、状态触发前提、DOM 断言、键盘步骤与焦点起止、network 请求/响应、console、截图、Receipt/lineage refs、结果与 blocker。刷新、深链、租户切换、晚到响应、stale 保留和 retry 必须有独立路径。

正向只认 `org-org/dev-project`；`dev-org/dev-project` 仅为负向隔离 canary。截图、静态视觉稿、组件测试、离线壳、API 失败关闭或 Mock fixture 均不能单独签发正向 GREEN。

## 6. 当前事实与阻断

现有 `AsyncStateBoundary` 已声明七异步态、blocked、not-installed、ready；`EcommerceWorkshopShell` 具备唯一 H1、skip link、Focus Mode 与焦点恢复；`InstalledModuleNavigation` 只渲染服务端安装投影并提供 aria-current 与文字 readiness。定向 5 文件 22 项测试 GREEN。

这些只证明通用壳基元。八领域 read model、完整生命周期命令、三视口生产 HTTP、全键盘路径、200% 缩放、reduced-motion、正负租户网络证据尚未闭合。故 W8-07 保持未勾选，等待全部七个上游退出门与产品冻结后再执行真实累计矩阵。

## 7. 两轮审查

第一轮纠正了“七态”歧义，明确 blocked、not-installed、ready 不挤入七异步态；同时禁止用一张 blocked 页面覆盖业务正向。第二轮补齐 exact release/installation/module 绑定、not_applicable 规则、键盘全路径、200% 缩放/reduced-motion 和 DOM/network/console/authority 同包证据。结论为验收合同通过，实际验收硬阻断。

## 8. 2026-08-26 串行施工方案（AOS-000276）

### 8.1 新鲜事实与本波裁决

W1～W7 与 W8-01～W8-06 已在 `m1` 形成八 Module 路由、只读 read model、公共生产合同、原子 Skill/Logic/数字同事贡献、多媒体和六场景的工程基座，因此第 1/6 节中“七个上游均未 GREEN”的 2026-08-15 快照不再构成本地工程验收停工理由。

但实时产品审查发现：通用状态测试尚未与八个 exact Module 绑定；Media Studio Tab 尚无 roving tabindex/方向键/Home/End；多个 Tab 视图缺少稳定 `id + aria-controls + aria-labelledby`。本波允许新增一个可执行的累计验收合同、修复这些无障碍回归，并用本地 production build 和内置浏览器生成工程 EvidencePack。无正式生产 HTTP/真实租户正向时，对应格必须标记 `blocked`，不用 Mock、静态壳或本地 fixture 签发 operational/release GREEN。

### 8.2 可执行验收合同

1. 八 Module 固定为 `task-cockpit/content-campaign/operations/creator-growth/media-studio/analyst/price-governance/customer`，每项必须同时绑定 route、Module exact ref 和 active Installation exact ref。
2. 视口固定 `1280/1440/1920`；七异步态为 `loading/empty/forbidden/stale/partial/failed/unknown`，`blocked/not-installed/ready` 单列，应得到 `8 × 3 × 10 = 240` 个稳定格，不得删格。
3. 每格必须是 `passed/blocked/not_applicable`；`not_applicable` 必须有稳定 reason 和 contract ref；ready 格缺 production build SHA、exact refs、HTTP/network/console 或 tenant evidence 任一项即 blocked。
4. 键盘合同统一覆盖 skip link、导航、Focus Mode、Tab roving、Home/End、Dialog/Drawer Escape/焦点返回与 retry；某 Module 无 Tab/Dialog 时使用显式 N/A，不伪造交互。
5. 只允许展示决策摘要、证据链、归因路径、关键假设和不确定性；页面有 Skill 贡献时仍按“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献视图”审计。

### 8.3 文件级施工清单

| 切面 | 文件 | 最小改动 |
| --- | --- | --- |
| 验收合同 | `apps/web/src/components/workshop/workshopAcceptance.ts` | 定义八 Module、三视口、十状态、240 格、键盘路径、exact evidence 校验与失败关闭汇总 |
| 累计测试 | `apps/web/src/components/workshop/workshopAcceptance.test.ts` | 覆盖 240 格不丢失、ready 缺 exact evidence 阻断、N/A 必填 reason；八 Module 壳 H1/skip/main/exact route 由 `EcommerceWorkshopShell.test.tsx` 闭合 |
| Tab 无障碍 | `MediaStudioPage.tsx`、`AnalystPage.tsx`、`PriceGovernancePage.tsx`、`CustomerPage.tsx` 及对应测试 | 补 roving tabindex、方向键/Home/End、稳定 tab/panel id 和 controls/labelledby，不改 read model 或命令边界 |
| 公共壳与样式 | `EcommerceWorkshopShell.tsx`、`EcommerceWorkshopShell.test.tsx`、`apps/web/src/styles/45-ecommerce-workshop.css` | 验证 skip link 焦点、Focus Mode 恢复、visible focus、200%/reduced-motion 与三视口无溢出；只修确认的公共缺口 |
| 证据/上下文 | `.evidence/workshop/w8-07/`、本 ADR、D-waves 总清单、Task/Delivery Receipt、authority/Prime 投影 | 记录生产构建、专项/累计回归、三视口 DOM/console/截图、240 格处置和 `NO_RELEASE` |

### 8.4 验收、证据分级与回退

- 专项：acceptance matrix、Shell/Nav/AsyncState、四个 Tab 页；累计：Workshop Web 全量、TypeScript 与 production build。
- 内置浏览器在新鲜 production build 上验证 1280/1440/1920、八路由、H1/landmark/skip/current nav、Tab 键盘、visible focus、长文案、无水平溢出与 console；本地 fixture 只签发 engineering browser evidence。
- 真实生产 ready 格若无 `org-org/dev-project` 正式 HTTP 和 exact EvidencePack 则保持 blocked；`dev-org/dev-project` 只能是跨租户负向格。
- 回退只移除 acceptance 合同/测试并恢复本波 Tab 无障碍属性；不修改 authority、业务数据、Provider、Action 或发布状态，不需要 migration 或数据回滚。

## 9. 2026-08-26 实施与失败关闭结论

### 9.1 最小实施

- 代码 `m1@6b41a32ba5b012a645fd4d1465258e5853d0af04` 新增八 Module、三视口、十状态的 240 格唯一验收合同，对 route、正向租户、production build SHA、Module/Installation exact ref 和证据包逐项失败关闭。
- Media Studio、Analyst、Price Governance、Customer 四组 Tab 统一补齐 roving tabindex、方向键/Home/End、稳定 tab/panel id、`aria-controls` 和 `aria-labelledby`；不改 read model、命令能力或业务状态。
- 公共工作台样式新增 `prefers-reduced-motion` 收敛；八 Module 公共壳逐项验证唯一 H1、skip link、main 与精确 route。

### 9.2 测试与浏览器

- TDD RED 先证明验收合同缺失且 Media Tab 不符合 roving tabindex；实施后专项 6 文件 39 项全绿。
- Web 累计回归 `242 files / 2193 tests passed`；TypeScript 通过，Vite production build `344 modules transformed`。
- 证据提交 `m1@d338cfffa9ca22ae8494fd28f685c62e709f6e0a` 保存 240 格矩阵、24 个 Module/视口路由事实与 1280/1440/1920 代表截图。内置浏览器确认 24/24 路由均为唯一 H1、状态区可达且无横向溢出；未捕获脚本错误。

### 9.3 证据分级与安全裁决

本地正式构建的 API/Catalog 不可用，也没有 active Installation exact ref 和生产 HTTP，页面因此诚实显示“读取失败 / 正式服务未返回可验证结果”。矩阵中 240/240 格全部保持 `blocked`：24 个 ready 格为 `READY_REQUIRES_PRODUCTION_HTTP`，其余 216 格为 `EXACT_MODULE_INSTALLATION_EVIDENCE_NOT_AVAILABLE`。

因此 W8-07 只闭合“可执行验收合同 + 无障碍回归修复 + 工程浏览器证据”，不签发 operational/release GREEN。本波没有 migration、真实租户写入、Provider/Action、自动重试、外部副作用或发布；结论为 `ENGINEERING_ACCEPTANCE_CONTRACT_BROWSER_GREEN / OPERATIONAL_MATRIX_FAIL_CLOSED / NO_EXTERNAL_EFFECT / NO_RELEASE`。下一串行入口为 W8-08。

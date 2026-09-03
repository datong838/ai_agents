# 工作台八菜单视觉、功能、数据全量缺陷清单与串行修复波次

> 审计日期：2026-08-30
> 状态：`PRODUCT_ACCEPTANCE_REOPENED / R2_4_OF_6 / TOTAL_16_OF_81 / R2_IN_PROGRESS / NO_RELEASE`
> 正向业务租户：仅 `org-org/dev-project`（栖月汇微商城）
> 负向隔离 canary：`dev-org/dev-project`，不得作为正向完成证据
> 与原 96 项关系：原 W0～W8 的 `96/96` 仅表示历史工程合同清单已闭合；本清单是用户浏览器验收重新发现的产品缺陷修复账本，不改写也不合并原 96 个编号。

## 1. 结论与重新开账原因

此前 `AOS-000424～AOS-000434`、`AOS_REMAINING_SIDEBAR_AND_WORKSHOP_CURRENT_OPERABILITY_GREEN_NO_EXTERNAL_EFFECT` 和“八菜单当前可操作”只能视为历史切面。2026-08-30 使用内置浏览器、当前 `m1`、当前运行服务和栖月汇真实只读接口重新核验后，至少存在以下可复现事实：

1. 八个工作台路由都切换到单独硬编码的缩减菜单，每页只有 13 个链接；Buddy 使用完整 canonical 菜单，共 80 个链接，可滚动到底。问题不是用户没有滚动，而是八页根本没有渲染完整菜单源。
2. 八页的折叠按钮能响应，但折叠/展开的是错误的缩减菜单；不能据此判定导航完成。
3. 多数主按钮只显示“已做安全预检/不会创建记录”的提示，没有完成应有的工作台内部业务动作、状态变化、Receipt 或可追溯结果；“有点击反馈”不等于功能可工作。
4. 当前 API 中，统一运营已有 210 条可附着记录，经营参谋已有 12 个经营观察项，但页面仍优先展示阻断切片或空的 Business Investigation Case，真实能力没有被正确呈现。
5. 内容、达人、媒体、价格、客户等页面仍缺 canonical authority 或业务投影；客户源已有 54 条 CustomerLite 输入，但 4 个业务视图均为 0。
6. 页面与正式视觉稿在信息结构、组件数量、操作入口、底部能力带、复盘区、数字同事浮层、业务标签页等方面仍有显著差异，不能再称“1:1 封板”。
7. 统一运营正确视觉基线是 `foundry/html/workshop-app-order.html`；把 `workshop-cop.html` 当成该页基线会造成错误验收。

因此，当前产品结论统一改为：`工程合同历史完成，产品验收重新打开，81 项修复任务待完成`。

## 2. 审计证据

- 当前八页与视觉稿成对截图、DOM 文本：`aos-platform/.evidence/workshop/2026-08-30-eight-page-gap-audit/01～08-*`
- 当前/视觉控件矩阵：`actual-visual-control-matrix.json`
- 八页菜单审计：`eight-page-nav-audit.json`
- Buddy 完整菜单审计：`buddy-full-nav-audit.json`
- 八页滚动容器与滚轮到底审计：`eight-page-scroll-audit.json`、`eight-page-wheel-to-bottom-audit.json`
- 八页当前真实 GET：`task-cockpit-api.json`、`content-campaign-api.json`、`operations-api.json`、`creator-growth-api.json`、`media-studio-api.json`、`analyst-api.json`、`price-governance-api.json`、`customer-api.json`
- 统一运营正确视觉基线：`operations-correct-visual.png`、`operations-correct-visual-controls.json`
- 用户复现截图：八页缩减菜单与 Buddy 完整菜单对照，以及日常总控、经营参谋等视觉/功能差异截图。

## 3. 统一验收定义

每项只能在以下四类证据同时满足后勾选：

1. **视觉**：在 1280×720、1440×900、1920×1080 三档，由内置浏览器逐页与正式视觉稿成对截图；布局、层级、间距、字号、颜色、组件尺寸、状态和溢出逐项对账。
2. **功能**：按钮必须产生与文案一致的工作台内部业务结果，或在缺少安全条件时明确 disabled 并说明缺失条件；仅弹出“预检已打开”不算完成。
3. **数据**：正向只认 `org-org/dev-project`；页面数字、列表、空态、筛选和详情必须能回溯到同租户 exact ref、cutoff、Receipt/lineage。不得用演示数据补空。
4. **安全**：开发阶段允许完成工作台内部 canonical authority、草稿、计划、评审、任务和 Receipt 读写；真实 Provider、消息发送、调价、发布、客户触达和生产副作用仍须走原安全门，不因页面可用而放行。

公共文字规则：业务页面只出现中文业务名称、业务任务和用户可理解的状态；开发 Task 编号、ADR 编号、迁移名、代码原因码不得伪装成业务数据。

## 4. 81 项唯一任务清单

### R0 · 事实重置与精确施工包（4 项）

- [x] `R0-01` 撤销“当前八菜单已经产品验收 GREEN”的产品口径；保留历史工程事实，但在总清单、验收记录和后续 Receipt 中统一标为 `PRODUCT_ACCEPTANCE_REOPENED`。证据：[R0 精确施工包](WORKSHOP-R0-八菜单产品验收重开与精确施工包.md) §1。
- [x] `R0-02` 冻结八页唯一视觉源：日常总控、内容、统一运营、达人、媒体、经营参谋、价格、客户各自只有一个正式 HTML；统一运营固定使用 `workshop-app-order.html`。证据：R0 精确施工包 §2 的逐文件 SHA-256。
- [x] `R0-03` 为八页建立逐组件差异矩阵：视觉元素、业务动作、API/authority、栖月汇数据、权限/副作用门五列逐项映射，禁止只按按钮数量或截图相似度验收。证据：R0 精确施工包 §3。
- [x] `R0-04` 冻结施工文件与回归范围，登记 Task Receipt/Lease；确认不覆盖无关未提交文件，不修改真实业务数据，不绕过外部副作用和发布门。证据：R0 精确施工包 §4；Task Receipt `WORKSHOP-R0-PRODUCT-ACCEPTANCE-REOPEN-EXACT-CONSTRUCTION`。

### R1 · 全局 Shell、完整左侧菜单与公共交互（8 项）

- [x] `R1-01` 删除八页单独硬编码的缩减菜单源；八页、Buddy 与其他 AOS 页面统一消费同一 canonical `navNodes`/权限投影。证据：`f89d4809`，Shell 专项回归 15/15 GREEN。
- [x] `R1-02` 恢复完整菜单树：工作台八菜单、Buddy、应用程序构建工具全部项、AIP 决策引擎全部项及其他有权菜单均不得丢失。证据：`26e0b179` + `f89d4809`，八主入口目录回归 3/3、合并专项回归 18/18 GREEN。
- [x] `R1-03` 逐页用浏览器滚轮滚到菜单底部，验证 8 页与 Buddy 的菜单项、分组、顺序和可达性一致；不得只检查首屏。证据：内置浏览器 8/8 路由逐页真实滚轮，每页 80 个入口、唯一当前项，最末“租户开通”可见。
- [x] `R1-04` 修复折叠/展开：八页都能收起、恢复、保持当前路由高亮，并在刷新/跳页后按统一策略保持状态。证据：`f89d4809`，折叠恢复、焦点、路由切换和唯一当前项回归 GREEN。
- [x] `R1-05` 统一顶部栏、面包屑、租户/工作区、搜索、日期/主操作区域，消除顶部挤压、遮挡和跨页高度漂移。证据：8 页 × 1280/1440/1920 三视口共 24 组几何核验，顶栏 48px，侧栏/主区从顶栏下方对齐，无横向溢出；唯一首次未渲染样本等待后独立复核通过。
- [x] `R1-06` 统一固定区与滚动区：底部能力带、明日预告、抽屉和浮层不得遮挡任务、数字同事或页面主内容。证据：内置浏览器八页 fixed/sticky 审计，仅任务总控中央四列表头为 sticky，其余无覆盖主内容的 fixed 区；公共底部与侧栏独立滚动。
- [x] `R1-07` 统一公共按钮语义：可执行、等待条件、只读、禁止外部副作用四态可辨；移除“看似可点但只弹预检提示”的假可用态。证据：`f89d4809`，已接内部行为可执行，未接行为使用原生 disabled 且不产生伪结果。
- [x] `R1-08` 建立 Shell 自动回归：8 页×完整菜单×滚到底×折叠/展开×当前项高亮×三视口×键盘/焦点，共用一个断言源。证据：Shell/Navigation 专项 18/18 GREEN，Web 累计 270 files / 2412 tests GREEN，production build GREEN，内置浏览器 8 页滚轮 + 24 视口几何组合 GREEN。

### R1 文件级施工包（2026-09-02）

1. `apps/web/src/shell/AppShell.tsx`
   - 删除八页专用 `AnalystVisualNavigation` 与经营参谋专用 `GlobalNav` 旁路；所有页面统一渲染 canonical `navNodes`。
   - 保留八页视觉稿要求的无品牌头布局，但菜单数据源、权限投影、当前项与折叠状态必须只有一套。
   - 顶栏动作仅在已有真实内部行为时可点击；尚未接通正式业务工作流的动作使用原生 disabled 语义，不再用“点击后弹安全预检”伪装可用。
2. `apps/web/src/shell/AppShell.workshop.test.tsx`
   - 将 13 项临时侧栏断言改为 canonical 全菜单、唯一当前项、折叠持久化、路由切换滚动复位与按钮可用态断言。
3. `apps/web/src/shell/AppShell.navigation.test.tsx`
   - 增加八个工作台路由与 Buddy 共用菜单源、菜单末项可达和当前项自动滚入视区的共享回归。
4. `apps/web/src/styles/00-shell.css`
   - 移除只服务临时侧栏/临时全局导航的样式；八页复用 canonical 菜单样式并保持 260/48px 展开折叠尺寸、独立滚动与当前项高亮。
5. `apps/web/src/components/workshop/workshopAcceptance.ts` 与 `InstalledModuleNavigation.tsx`
   - 现有 `WORKSHOP_ACCEPTANCE_MODULES` 是八个主工作台唯一产品路由基线；导航直接消费该基线，不再以不完整的实时安装目录决定主菜单是否存在。
   - 实时目录仅追加非基线动态模块，并继续承担安装、权限与精确引用的事实权威；菜单不把主路由的存在冒充为已安装或已就绪。
   - 目录 loading/failed/empty 不再让八个产品主入口消失；当前路由必须始终存在唯一 `aria-current=page`。
6. `apps/web/src/components/workshop/InstalledModuleNavigation.test.tsx`
   - 回归八个基线入口恒定、动态模块去重追加、空/失败目录不丢主菜单、当前项唯一且不泄露技术 readiness。
7. 验收顺序：专项 Shell 测试 → Web 累计回归/构建 → 内置浏览器八页逐页滚到底、折叠/恢复、当前项、顶部与三视口检查 → 方案/代码一致性复审 → Receipt/CAS/Prime 回读。

### R1 封板核验记录（2026-09-02 19:45 +08:00）

- 已完成：`R1-01`～`R1-08`，代码提交 `26e0b179`、`f89d4809`。
- 自动验证：3 文件 18/18 GREEN；Web 累计 270 files / 2412 tests GREEN；TypeScript/production build GREEN；`git diff --check` GREEN。
- 浏览器验收：8/8 页均为 80 个菜单入口、唯一当前项、滚轮到底末项可见；侧栏 260px → 48px → 刷新保持 → 260px；24 组三视口结构复核最终全部通过。
- 口径边界：R1 只封板公共 Shell/导航/固定区/通用操作语义；八页各自视觉稿 1:1、业务功能和真实数据仍按 R3～R9 闭合，不由 R1 冒充产品全量完成。

### R2 · 栖月汇真实数据与 canonical authority 基座（6 项）

- [x] `R2-01` 固化 `org-org/dev-project` 当前数据快照与同截止时间 SourceReadiness；实时事实为 9/12 ready、3 failed、0 stale，不得写成全绿。证据：`.evidence/workshop/2026-09-02-r2-real-tenant-baseline/source-readiness-summary.json`。
- [x] `R2-02` 建立八页“页面字段→API 字段→领域 authority→真实源/Receipt”追溯表，缺 exact ref 的字段必须诚实为空或禁用。证据：本节 R2 八页追溯矩阵与 `.evidence/workshop/2026-09-02-r2-real-tenant-baseline/eight-page-traceability-summary.json`。
- [x] `R2-03` 补齐工作台内部需要的 canonical authority/Store/reader；已修复 RLS 建立后再设置只读事务导致的 PostgreSQL `ActiveSqlTransaction`，只读连接现于首条 SQL 前固定 `REPEATABLE READ + READ ONLY`，闭合写连接于首条 SQL 前固定 `SERIALIZABLE`；正式空表现在返回可信空而非读取失败。专项与累计回归 75/75、8/8、250/250，五页内置浏览器验收通过，证据：`.evidence/workshop/2026-09-03-r2-canonical-read-transaction/verification.json` 与同目录截图；实现提交 `ee82a6ca`。
- [x] `R2-04` 统一 loading/empty/blocked/partial/ready/conflict 状态；已有真实切片时不得因为另一个切片 blocked 而把整页显示成死页面。已由公共状态推导与首选切片工具覆盖七个业务页；专项 66/66、Web 累计 271 files / 2416 tests、TypeScript、生产构建和八页内置浏览器交互验收 GREEN。证据：`.evidence/workshop/2026-09-03-r2-unified-state-model/verification.json`；实现提交 `9625a416`。
- [x] `R2-05` 为允许的工作台内部写操作建立 preview→confirm→Receipt→readback 闭环和幂等保护；真实外部动作继续失败关闭。后端相关累计 60/60、Web 专项 47/47、Web 累计 271 files / 2419 tests、TypeScript/生产构建、内置浏览器只读验收 GREEN；证据：`.evidence/workshop/2026-09-03-r2-internal-write-receipt/verification.json`。
- [x] `R2-06` 建立 `dev-org/dev-project` 隔离负向回归，证明无跨租户泄漏，但不把负向 canary 当正向业务完成证据。后端 24 项隔离矩阵、前端单请求租户快照与八页响应回显校验、正反租户浏览器验收均已闭合；实现提交 `dc527fab`、`b9d805e2`。

### R2 文件级施工包（2026-09-02）

#### R2-A · 同截止事实与追溯基线（R2-01、R2-02）

1. `aos-platform/.evidence/workshop/2026-09-02-r2-real-tenant-baseline/`
   - 只保存 `org-org/dev-project` 的聚合计数、状态、cutoff、技术引用类型和 Receipt 是否存在；不保存客户明细、凭证或业务敏感字段。
   - 对 `dev-org/dev-project` 只保存 0 数据/租户回显/拒绝结果，不把 canary 当正向完成证据。
2. 本清单文档
   - 固化八页“页面区块→canonical API→authority/reader→真实源/Receipt→当前状态”的追溯矩阵。
   - 实时事实变化必须改写旧口径；不得把 2026-08-30 的 `9 ready / 2 failed / 1 stale` 沿用为当前结论。
3. 只读核验入口
   - `GET /v1/ecommerce-workshop/source-readiness`
   - `GET /v1/ecommerce-workshop/views/task-cockpit|operations|content-campaign|creator-growth|media-studio|analyst|price-governance|customer`
   - 所有正向读取必须使用 `org-org/dev-project`，并校验 tenant echo、cutoff、分页计数、authority refs 与 Receipt。

#### R2-B · canonical authority、统一状态和内部 Receipt（R2-03～R2-06）

##### R2-03 根因复核与精确施工范围（2026-09-02）

1. 已确认不是“无人交付 authority”，而是 canonical Store 的公共只读事务初始化顺序错误：`db.connect(scope)` 已执行客户端编码与租户 RLS 上下文后，部分 reader 再执行 `SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY`，PostgreSQL 会以 `ActiveSqlTransaction` 拒绝，随后被页面聚合器失败关闭为 authority 缺失。
2. 修复必须保留三条边界：事务开始前建立 `REPEATABLE READ + READ ONLY`；进入事务后再设置 `aos_runtime` 与 `org_id/project_id`；写 Store 继续使用原连接路径，禁止把全部租户事务误设为只读。
3. 本子项精确代码范围：
   - `services/aos-api/aos_api/db.py`：增加显式的 `connect_read_only` 和 `connect_serializable` 连接入口，在首条 SQL 之前由 psycopg 设置事务特征；原 `connect` 仍保持可写默认语义。
   - 将已经在八页 canonical GET 及内部 authority 回读路径上的运营对象、库存、售后、OperationCase、内容活动、达人增长/准备/生命周期、价格研究/处置、客户源/生命周期与三模块闭环 Store/Reader 接入正确的事务入口；依赖注入的测试连接继续可控，不改写入行为。
   - 增补公共连接顺序、Store、Service 与 Router 专项测试；真实回读须证明空表返回 `ready + empty`，权限/租户/表异常仍逐切片失败关闭。
4. 本子项只修复内部 canonical 读取与回读，不创建演示业务数据，不触发 Provider、消息、调价、退款、发货、发布或客户触达；栖月汇真实数据只读验证继续使用 `org-org/dev-project`，`dev-org/dev-project` 仅作隔离负向证据。

##### R2-04 统一页面状态模型精确施工范围（2026-09-03）

1. 公共状态模型统一为 `loading / empty / blocked / partial / ready / conflict`：`empty` 与 `blocked` 仍保留可浏览的页面结构，`partial` 必须保留已可用切片，`conflict` 必须显式呈现冲突来源；权限拒绝、读取失败与未安装继续失败关闭。
2. 新增公共切片判定工具，按“有数据的 ready → 任一 ready → conflict → blocked/unknown”的顺序选择初始视图；页面级状态由全部切片共同推导，不得再由单个 blocked 切片覆盖可用事实，也不得把可信空伪装成普通 ready。
3. 本子项精确代码范围：
   - `apps/web/src/components/workshop/AsyncStateBoundary.tsx` 及测试；
   - 新增 `apps/web/src/components/workshop/workshopViewState.ts` 及测试；
   - `OperationsPage.tsx`、`ContentCampaignPage.tsx`、`CreatorGrowthPage.tsx`、`MediaStudioPage.tsx`、`AnalystPage.tsx`、`PriceGovernancePage.tsx`、`CustomerPage.tsx` 的最小状态接入与既有页面测试；任务总控页已有独立 stale/empty 状态机，只做累计回归，不重写其交接命令状态。
4. 验收必须覆盖：混合 ready/blocked 时默认打开真实可用切片并显示 partial；全 ready 且零记录显示可信 empty；全 blocked 显示 blocked 但页面导航仍可操作；conflict 显示来源且不吞掉可浏览内容；八页浏览器回读不得出现死页面或把缺失值伪装为零。
5. 本子项只统一展示与选择策略，不创建业务记录、不放行工作台内部写操作，也不触发 Provider、消息、调价、退款、发货、发布或客户触达。

##### R2-04 封板核验记录（2026-09-03）

- 混合切片默认选择“有数据的 ready → 任一 ready → conflict → 其余”，不再由单个 blocked 切片把整页降级成死页面。
- `empty / blocked / partial / unknown / conflict` 均保留页面结构；`conflict` 单独呈现为告警态，权限拒绝与读取失败仍失败关闭。
- 八页内置浏览器逐页验证完整菜单、租户追溯、重新读取入口和关键页签/卡片交互；没有写入真实业务数据，也没有触发外部动作。

##### R2-05 内部写操作闭环精确施工范围（2026-09-03）

1. 复用现有 Operations canonical Action Proposal / Approval / ExecutionLease / ActionReceipt 与 OperationAuthorityReceipt，不新建第二套任务、审批或回执权威；本子项只补齐工作台缺失的“精确预览”契约和确认绑定。
2. 五类允许的内部 authority 命令（分类事件、创建运营工单、调整工单成员、管理服务时限、停止自动化）先提交同租户 exact 请求做无副作用 preview；服务端返回 canonical preview hash。confirm 必须携带该 hash，且重新计算后完全一致，才能进入现有 exact Action 链。
3. confirm 继续要求有效 Proposal、Approval 与 active ExecutionLease；成功只返回 canonical ActionReceipt + OperationAuthorityReceipt，随后由现有 observation GET 按 proposal/lease readback。相同 Idempotency-Key 只能回放同一结果，不得创建第二份 authority。
4. 退款、发货、库存调整、调价、消息发送、内容发布、客户触达等外部动作不增加 preview/confirm 入口，继续失败关闭；preview 本身不得写业务 authority、取得 Lease、执行 Adapter 或触发 Provider。
5. 本子项精确代码范围：
   - `services/aos-api/aos_api/ecommerce_operation_command_contracts.py`、`ecommerce_operation_command_service.py`、`routers/ecommerce_workshop.py`；
   - `services/aos-api/tests/test_ecommerce_operation_command_service.py`、`test_ecommerce_workshop_api.py` 及必要的命令契约/路由专项测试；
   - `apps/web/src/api/ecommerceWorkshop/contracts.ts`、`parser.ts`、`client.ts` 与对应测试，为后续 R3～R8 页面接入提供同一受控入口；
   - 不改八页视觉结构，不创建栖月汇演示业务记录，不修改真实业务数据。
6. 验收顺序：preview 纯函数/租户/actor/内容漂移测试 → confirm hash/Proposal/Approval/Lease/幂等/Receipt 测试 → refund 无入口与外部动作零调用测试 → Web parser/client 测试 → API/Web 累计回归 → 内置浏览器确认统一运营页面无回退 → Receipt/CAS/Prime 回读。

##### R2-05 封板核验记录（2026-09-03）

- 五类内部 authority 命令均已形成确定性 preview hash；confirm 必须携带完全一致的 hash 和 Idempotency-Key，漂移请求在进入 canonical Action 链前拒绝。
- confirm 仍由既有 Proposal / Approval / active ExecutionLease / ActionReceipt / OperationAuthorityReceipt 权威控制；Web 客户端按 confirm Receipt 再读取 observation，并校验命令与 Receipt 精确对应。
- `refund` 未进入 preview/confirm 命令联合类型和路由；本轮未创建真实业务记录、未取得新 Lease、未调用 Adapter/Provider、未触发退款、发货、调价、发布、消息或客户触达。
- 内置浏览器在 `org-org/dev-project` 只读复核统一运营驾驶舱，确认 7 类正式业务视图、来源 219、已挂接 210、待核对 9、冲突 0，页面和完整侧栏无回退。

##### R2-06 租户隔离负向回归精确施工范围（2026-09-03）

1. `org-org/dev-project` 只作为正向真实业务读取目标；`dev-org/dev-project` 只作为负向隔离 canary。负向结果只证明不可见、拒绝或租户回显隔离，绝不计入八页业务完成量。
2. 八个工作台 canonical GET 必须仅从当前 `Principal` 取得 org/project；URL query/body 注入其他租户一律 `VALIDATION`，返回 envelope 的 tenant 与请求 principal 不一致时一律失败关闭。
3. 五类内部命令的 preview/confirm 同时校验顶层 revision、原对象、成员与迁移对象的 tenant；跨租户请求必须在 Action Control、Store、Adapter、Provider 之前拒绝，Receipt 数量保持 0。
4. Web 八页 parser/client 必须拒绝跨租户 envelope，不得把 `dev-org` 数据并入 `org-org`；缓存键、重新读取和页间上下文不得弱化 tenant identity。
5. 本子项精确代码与证据范围：
   - 新增 `services/aos-api/tests/test_ecommerce_workshop_tenant_isolation_regression.py`，集中覆盖八页 GET、租户注入、命令 preview/confirm 和零副作用；
   - `apps/web/src/api/ecommerceWorkshop/parser.test.ts`、`client.test.ts` 仅在发现矩阵缺口时补最小测试，不重写业务页面；
   - `.evidence/workshop/2026-09-03-r2-tenant-isolation/` 只保存租户回显、状态码、聚合数量与测试结果，不保存客户/订单明细；
   - 若测试暴露生产缺陷，只修改直接责任的 reader/router/parser，先补失败用例再最小修复。
6. 验收顺序：八页 principal scope 矩阵 → query/body 注入矩阵 → command nested-ref 漂移矩阵 → Web parser/client 漂移矩阵 → PostgreSQL/RLS 相关累计回归 → 内置浏览器分别核对正向租户与负向 canary → Receipt/CAS/Prime 回读；全程不产生真实业务写入或外部动作。

##### R2-06B Web 响应租户绑定补充施工范围（2026-09-03）

1. 后端八页 Principal scope 与既有内部命令隔离矩阵已通过；继续审查发现 Web client 虽使用会话租户请求，但调用严格 parser 时未传入同一请求快照的 expected tenant。该缺口必须在 R2-06 内闭合，不能留给单页波次。
2. client 每次请求只读取一次 auth headers，并从同一份 `X-Org-Id` / `X-Project-Id` 快照提取 expected tenant；请求发送与响应 parser 必须绑定同一 tenant，避免会话切换竞态或恶意/错误响应混入。
3. 仅对八个主页面 canonical GET 和 Operations 命令 readiness/preview/confirm/observation 建立该绑定；不改变 URL、不增加租户 query/body、不改变现有认证头，也不修改页面布局和业务状态推导。
4. 自定义 client 若没有完整 tenant headers，继续兼容现有纯 parser/网络测试；生产 `tenantAuthHeaders` 始终提供完整 tenant。半套 tenant header 必须在发请求前失败关闭。
5. 增加 client 回归：八页响应 tenant 漂移全部拒绝；请求期间会话 header provider 只调用一次；命令 preview/confirm/observation 同样拒绝漂移。随后执行 parser/client 专项、Web 累计回归和内置浏览器正向只读复核。

##### R2-06 封板核验记录（2026-09-03）

- 后端新增集中隔离回归，覆盖八页 canonical GET 的 Principal 透传与八条 query tenant 注入拒绝；24/24 GREEN，相关后端累计 83/83 GREEN。
- Web client 以单次请求读取的鉴权头形成 tenant snapshot；半套租户头在网络请求前拒绝，带 tenant 的成功响应与快照不一致时对 GET/POST 统一失败关闭。parser/client 专项 50/50、Workshop 前端矩阵 330/330、Web 累计 2422/2422、TypeScript 与生产构建 GREEN。
- 内置浏览器正向使用 `org-org/dev-project`，统一运营显示 7 个视图、来源 219、已挂接 210、待核对 9、冲突 0；负向切换到 `dev-org/dev-project` 后仅显示“模块未安装”，未出现栖月汇业务数据，随后恢复正向租户。
- 全程未修改真实业务数据，未调用 Adapter/Provider，未触发退款、发货、调价、发布、消息或客户触达。证据位于 `.evidence/workshop/2026-09-03-r2-tenant-isolation/`。

1. 后端候选范围（审计确认缺口后再取最小集合）
   - `services/aos-api/aos_api/ecommerce_workshop_*_contracts.py`
   - `services/aos-api/aos_api/ecommerce_workshop_*_source_reader.py`
   - `services/aos-api/aos_api/ecommerce_workshop_*_store.py`
   - `services/aos-api/aos_api/routers/ecommerce_workshop.py`
   - 对应 `services/aos-api/tests/test_w*_ecommerce_workshop*.py` 与 tenant isolation 测试。
2. Web 候选范围（不跨入单页 1:1 视觉重做）
   - `apps/web/src/api/ecommerceWorkshop/contracts.ts`、`parser.ts`、`client.ts` 与测试。
   - `apps/web/src/components/workshop/` 下公共状态/Receipt 组件及八页最小接入点。
3. 状态规则
   - `loading` 只表示请求进行中；`empty` 表示 authority 已可读且集合为空；`partial` 表示至少一个真实切片可用；`blocked` 只约束缺失切片或动作；`conflict` 必须显示冲突来源；`ready` 必须有 exact refs。
   - 页面级 readiness 不得覆盖切片级可用事实。统一运营的六个 ready 切片、经营参谋的 overview/quality、客户的 54 条输入都必须可见。
4. 内部写规则
   - 仅允许本系统内部草稿、计划、评审、任务、版本和 Receipt；全部按 `preview→confirm→Receipt→readback`，相同 idempotency key 不得产生第二份 authority。
   - Provider、消息发送、调价、退款、发货、发布和客户触达不在 R2 放行。
5. 验收顺序
   - 合同/Store/reader 专项测试 → 路由/租户隔离 → Web parser/状态组件 → 累计 API/Web 回归 → 内置浏览器八页状态与数据追溯 → 方案一致性复审 → Receipt/提交/CAS/Prime 回读。

### R2 当前事实快照（2026-09-02 21:03 +08:00）

- canonical SourceReadiness cutoff：`2026-09-02T13:03:22.840394Z`；总状态 `failed`；当前为 **9 ready / 3 failed / 0 stale**。
- 三个失败流水线：商品、商品 SKU、履约；均为最新运行未成功且质量检查失败，但对账检查通过。该事实替代旧的“2 failed / 1 stale”口径。
- 真实源聚合：店铺 1、商品 57、SKU 62、类目 11、订单 124、订单行 234、履约 19、客户轻量投影 54、小程序 3、系统配置 39、商品评价 5、支付 210。
- 八页读取均为 HTTP 200 且 tenant echo 为 `org-org/dev-project`；页面层仍存在以下差异：任务 3 条；统一运营 210 条且 6 个切片 ready、operationCases blocked；内容/达人/媒体/价格 authority 缺口；经营参谋 overview 与 quality ready；客户 54 条输入存在但 5 类领域 authority 缺失。

### R2 八页追溯矩阵（基线）

| 页面 | canonical API | 当前可追溯 authority/真实源 | 当前业务可见事实 | R2 缺口 |
|---|---|---|---|---|
| 日常任务总控 | `/views/task-cockpit` | Task/Run 当前投影；业务上下文按独立 SourceReadiness cutoff | 3 条任务 | 补 task item exact refs 与 Receipt 追溯，不把独立 cutoff 警告当整页阻断 |
| 内容与活动 | `/views/content-campaign` | 当前无 CampaignRevision/CalendarEntry/MasterContentIntent exact ref | 0 条 | 建立三类内部 authority、reader 与版本 Receipt |
| 统一运营 | `/views/operations` | Order、OrderLine、ProductSku、Shipment、Payment、AfterSales exact refs + Receipt | 210 条；六切片 ready | 建立 OperationCase 内部 authority；页面默认展示 ready 切片 |
| 达人邀约 | `/views/creator-growth` | 当前无 Candidate/Outreach/Contract/Delivery/Relationship exact ref | 0 条 | 建立五阶段内部 authority/reader |
| 多媒体生产 | `/views/media-studio` | EvidencePack 存在；上下文/执行/交付 authority 缺失 | 0 条 | 建立内部生命周期与发布 Proposal authority，不放行 Provider |
| 经营参谋 | `/views/analyst` | SourceReadiness、MetricDefinition/Observation、Quality/Reconciliation refs + Receipt | 10 项；overview/quality ready | 保留真实指标；补 Case/Run/plan/evidence authority，维持非因果边界 |
| 价格治理 | `/views/price-governance` | 当前无 PriceCase/竞品/计划 exact root | 0 条 | 建立内部 PriceCase/观察/计划 authority，不放行调价 |
| 客户关系 | `/views/customer` | CustomerLiteSourceWindow + Receipt | 输入 54，四视图均 blocked | 建立 Consent/Segment/Journey/Dialogue/OutreachBatch authority并保留隐私边界 |

### R3 · 日常任务总控大屏（7 项）

- [x] `R3-01` 按视觉稿恢复 KPI 顶栏、下达区、执行组、中央任务流、策划组、右侧复盘、底部共享能力和明日预告的完整比例与层级。
- [x] `R3-02` 恢复“下达”右侧经营参谋推荐任务；点击推荐项必须自动填入任务输入框，允许用户继续编辑后下达。
- [x] `R3-03` 实现任务输入→安全预检→内部任务草稿/Task→数字同事分派→Receipt→列表回读闭环；无条件时按钮明确禁用，不得只显示提示。
- [x] `R3-04` 完整实现 6 个数字同事卡片及介绍浮层：职责、边界、常用 Agent、当前状态；浮层尺寸、锚点、遮挡、滚动和关闭行为与视觉稿一致。
- [x] `R3-05` 恢复 10 个共享原子能力/Agent 标签，展示真实可用性和“原子 Skill→Logic→数字同事→工作台贡献”关系，不以两个泛化标签代替。
- [x] `R3-06` 恢复右侧三段：今日复盘、AI 改进建议、经验沉淀 Wiki·今日入库；数据来自真实 Task/Run/Eval/Wiki，不能复制视觉稿示例。
- [x] `R3-07` 修复底部能力带与明日预告遮挡、任务列表滚动、数字同事列可见性，并完成真实栖月汇任务的创建、筛选、详情、复盘和回读自验收。

#### R3-01 视觉结构精确施工范围（2026-09-03）

1. 正式视觉源仅使用 `foundry/html/workshop-task-cockpit.html` 及其浏览器审计截图；业务数字、日期和状态只取当前 `org-org/dev-project` 响应，不复制视觉稿示例。
2. 当前实现已具备与 1280×720 视觉源一致的主几何：73px KPI 带、53px 下达带、`120px / 中央任务流 / 120px / 右侧复盘` 四栏、50px 共享能力带和 34px 明日预告。R3-01 不重写已对齐结构，只修正可见标题语义并增加结构回归，避免破坏 R1 完整菜单和 R2 canonical 数据。
3. 文件级范围：
   - `apps/web/src/components/workshop/TaskCockpitPage.tsx`：保留 KPI、下达、两组数字同事、任务流、右侧复盘、能力带和明日预告的单一 DOM 层级；右侧标题恢复为产品语义“复盘 · 经验沉淀”，不把内部 authority 缺口当产品栏目名。
   - `apps/web/src/components/workshop/TaskCockpitPage.test.tsx`：锁定八个可见结构区及顺序，保留真实任务过滤、中文业务文案和零演示数据断言。
   - `apps/web/src/styles/45-ecommerce-workshop.css`：复核固定高度、四栏比例、内部独立滚动和底部非遮挡；只有浏览器测量偏离视觉源时才做最小调整。
   - `.evidence/workshop/2026-09-03-r3-cockpit-visual-structure/`：保存正式视觉参考、三视口截图、结构测量和测试结果。
4. R3-01 只封板布局层次；推荐任务填充、正式下达、六同事浮层内容、10 个能力、三段复盘和真实任务闭环分别由 R3-02～R3-07 接续，不能因结构已有就冒充整页完成。
5. 验收顺序：结构专项测试 → Web 累计回归/构建 → 内置浏览器当前 1280×720 视口的首屏、全页与底部截图及几何测量 → 视觉源并排复审 → Receipt/CAS/Prime 回读 → 自动进入 R3-02。当前内置浏览器不提供任意调整视口的接口，不以外部浏览器或页面内脚本伪造额外视口证据；响应式多尺寸复验统一保留到 R9 累计验收。

#### R3-01 闭合记录（2026-09-03）

- 实现提交：`c27611ef`。右侧产品栏目恢复为“复盘 · 经验沉淀”，首屏八段结构和四栏顺序由组件测试锁定。
- 内置浏览器在 `org-org/dev-project`、`/workshop/cockpit` 实测：KPI 73px、下达区 53px、四栏宽度 `120 / 407 / 120 / 325px`、共享能力 50px、明日预告 34px；页面可视区域 `clientHeight=635`、`scrollHeight=635`，底部能力带和明日预告没有覆盖数字同事列。
- 专项测试 `19/19`、Web 累计回归 `2423/2423`、TypeScript 与生产构建 GREEN；证据位于 `.evidence/workshop/2026-09-03-r3-cockpit-visual-structure/`。
- 结论：`WORKSHOP_R3_01_COCKPIT_VISUAL_STRUCTURE_GREEN`。这只关闭视觉结构，不代表推荐任务、下达、数字同事、十项能力和复盘数据已完成；下一项为 `R3-02`。

#### R3-02 经营参谋推荐任务精确施工范围（2026-09-03）

1. 推荐任务独立读取当前租户 `/v1/ecommerce-workshop/views/analyst`，只消费 `status=ready` 且同时具有 `definitionRef`、`observationRef` 和数值的指标；读取失败或没有精确指标时显示“暂无可验证推荐任务”，不得复制视觉稿中的投诉、滞销品、比价报告等示例。
2. 推荐语句按确定性规则把精确指标聚合为“经营数据异常、订单与商品规模、客户运营机会”三类短标签，保证 1280px 下达带能与视觉稿一样并列显示三项；点击后再回填包含真实数量的完整任务。建议属于“经营参谋指标建议”，不得声称来自尚不存在的 canonical 增长方案；每项保留数据截止与全部精确引用作为可访问说明，页面只展示业务中文。
3. 点击推荐项只把中文任务回填到“任务指令”输入框、聚焦并允许继续编辑；本项不创建 Task、不分派数字同事、不产生外部副作用，正式预检、内部任务与 Receipt 闭环由 R3-03 接续。
4. 文件级范围：
   - `apps/web/src/components/workshop/TaskCockpitPage.tsx`：并行但独立读取经营参谋视图、确定性生成最多三项建议、点击回填和失败关闭。
   - `apps/web/src/components/workshop/TaskCockpitPage.test.tsx`：覆盖精确 ready 指标、点击回填、可编辑性、无精确指标和读取失败。
   - `apps/web/src/styles/45-ecommerce-workshop.css`：在 53px 下达带内恢复下达按钮右侧的横向推荐胶囊，不挤压 KPI 或四栏主工作区。
   - `.evidence/workshop/2026-09-03-r3-cockpit-recommendation-fill/`：保存专项测试、累计回归、构建、浏览器点击前后与几何证据。
5. 验收顺序：专项测试 → Web 累计回归与生产构建 → 内置浏览器核对真实推荐内容、点击回填、继续编辑、重读和下达带几何 → 方案一致性复审 → Receipt/CAS/Prime 回读 → 自动进入 R3-03。

#### R3-02 闭合记录（2026-09-03）

- 实现提交：`2a843238`。任务总控独立读取经营参谋视图，仅以精确 ready 指标生成“经营数据异常、订单与商品规模、客户运营机会”三类中文建议；完整任务文本保留当前租户名称、真实数量和全部指标引用。
- 内置浏览器在 `org-org/dev-project`、`/workshop/cockpit` 实测三项推荐均位于“下达”按钮右侧且同时可见；点击“复盘订单与商品规模”回填“复盘栖月汇微商城的57 个商品、5 条商品评价的经营表现并整理问题清单”，继续追加“按渠道拆分”成功。下达带保持 53px，四栏和底部区未被挤压。
- 专项测试 `21/21`、Web 累计回归 `2425/2425`、TypeScript 与生产构建 GREEN；证据位于 `.evidence/workshop/2026-09-03-r3-cockpit-recommendation-fill/`。
- 结论：`WORKSHOP_R3_02_COCKPIT_RECOMMENDATION_FILL_GREEN`。本项没有创建 Task、数字同事分派或外部副作用；下一项为 `R3-03` 内部任务闭环。

#### R3-03 内部业务任务闭环精确施工范围（2026-09-03）

1. 继续复用 `/v1/aip/tasks` 与 PostgreSQL `aip_task` 作为唯一 Task 权威，不新增工作台本地任务表、不把页面状态或 `localStorage` 当权威；新任务类型固定为 `ecommerce.workshop.business_task`，标题只能使用用户输入的中文业务表达。
2. “下达”必须是两阶段显式流程：首次点击完成标题清理、长度与业务语义校验，并给出建议承接数字同事；再次点击才携带唯一 `Idempotency-Key` 创建内部 `pending` Task。空输入、纯开发编号或重复提交不得创建任务；canonical Task API 对工作台业务任务再次校验任务类型、中文业务标题和 `goal.workshopAssignment`，不能只信任浏览器预检。
3. 建议承接角色按业务关键词确定，并写入 Task `goal.workshopAssignment`；它只表示 `requested` 的建议绑定，不宣称 AgentInstance 已解析、已取得 Lease、已启动或已完成。经营参谋推荐携带的定义、观测与数据截止精确引用同时写入 `goal.sourceEvidence`，用户编辑后的普通任务允许该引用为空。
4. 服务端返回的 canonical `TaskSnapshot` 组成任务受理回执，页面至少展示 Task ID、版本、状态、建议承接数字同事与受理时间；回执出现后必须重新读取 Task Cockpit，并以新 Task 在当前租户列表中可见作为闭环完成条件。创建成功但列表暂未可见时明确显示“正在核对”，不能冒充闭环。
5. 本波只创建内部 Task，不创建 Plan/TaskRun，不派发外部渠道，不发送、不发布、不改价、不调用 Provider；所有租户范围继续仅由当前 Principal 决定。
6. 文件级范围：`services/aos-api/aos_api/aip_task_models.py` 与新增定向合同测试负责服务端二次校验；`apps/web/src/api/aipTasks/client.ts`、`apps/web/src/api/aipTasks/contracts.ts`、`apps/web/src/components/workshop/TaskCockpitPage.tsx` 及对应测试负责两阶段预检、幂等创建、Receipt 呈现和列表回读；必要样式仅追加到 `apps/web/src/styles/45-ecommerce-workshop.css`，不改动当前存在未提交工作的 `ecommerceWorkshop/parser.ts` 与其测试。
7. 验收顺序：AIP Tasks SDK 契约测试与 Task Cockpit 专项测试 → Web 累计回归与生产构建 → 内置浏览器用 `org-org/dev-project` 完成真实内部业务任务的预检、确认、回执和列表回读 → 方案一致性复审 → Delivery Receipt、authority CAS、memory sync/validate/gate 与 Prime 回读 → 自动进入 R3-04。

#### R3-03 闭合记录（2026-09-03）

- 工作台复用 canonical `/v1/aip/tasks`，以两阶段显式确认创建 `ecommerce.workshop.business_task`；浏览器与服务端共同拒绝空白、非中文、开发编号和技术实施任务，受控六数字同事只记录为 `requested` 建议承接。
- 内置浏览器在 `org-org/dev-project` 创建 `task-3243ee1e1ee54acc8845`：版本 1、`pending`、建议导购顾问承接；创建后重新读取任务总控，任务流和明日预告均回读成功。受理提示位于下达带内，不再覆盖 KPI 或任务区。
- 后端合同 `8/8`、前端专项 `26/26`、后端相关回归 `20/20`、Web 累计回归 `2428/2428`、TypeScript 与生产构建 GREEN；证据位于 `.evidence/workshop/2026-09-03-r3-cockpit-internal-task-loop/`。
- 结论：`WORKSHOP_R3_03_COCKPIT_INTERNAL_TASK_LOOP_GREEN`。本项没有创建 Plan/TaskRun，也没有派发、发送、发布、改价或 Provider 调用；下一项为 `R3-04` 六数字同事卡片与介绍浮层。

#### R3-04 六数字同事卡片与介绍浮层精确施工范围（2026-09-03）

1. 正式视觉源仍以 `foundry/html/workshop-task-cockpit.html` 为准：执行组与策划组各三张 120px 窄卡，卡片只保留 32px 图标、姓名和可证实状态，不把长职责挤进窄栏；完整职责在 304px 信息浮层中展示。
2. 六张卡必须逐一提供姓名、职责摘要、专业能力、工作边界、常用 Agent 和当前状态；“当前状态”只能来自本页可见的 canonical Task/Run 归因。当前接口没有个人归因时统一显示“尚无个人级归因”，不得复制视觉稿中的在线、执行中或派发数量。
3. 浮层以触发卡为锚点，执行组向右、策划组向左展开；顶部不得越过下达带，底部不得进入共享能力带或明日预告，内容过长时只在浮层内部滚动。窄视口无法放在侧边时夹在当前工作区可见范围内，不推动四栏布局。
4. 悬停/键盘聚焦提供临时预览；点击固定，再次点击、关闭按钮、Escape 或点击浮层外部关闭。固定后鼠标经过其他卡片不得偷换内容，关闭后焦点回到原卡片；从数字同事目录深链进入时也必须找到对应卡片并完成锚定，不能以未定位的 fixed 元素漂在页面上。
5. 文件级范围：
   - `apps/web/src/components/workshop/TaskCockpitPage.tsx`：卡片精简、稳定角色锚点、六角色内容、固定/临时状态和关闭焦点管理。
   - `apps/web/src/components/workshop/TaskCockpitPage.test.tsx`：逐卡内容、无伪状态、固定防偷换、外部/Escape/按钮关闭、深链锚定回归。
   - `apps/web/src/styles/45-ecommerce-workshop.css`：按视觉源锁定 304px、内部滚动、层级、边界和窄卡比例。
   - `.evidence/workshop/2026-09-03-r3-cockpit-colleague-popovers/`：保存内置浏览器六入口点击、上下边界、滚动与关闭证据。
6. 验收顺序：专项组件测试 → Web 累计回归与生产构建 → 内置浏览器逐一点击六张卡并检查锚点、遮挡、滚动、关闭和深链 → 方案/实现一致性复审 → Delivery Receipt、authority CAS、memory sync/validate/gate 与 Prime 回读 → 自动进入 R3-05。

#### R3-04 闭合记录（2026-09-03）

- 实现提交：`49e93ddf`。六张窄卡仅保留角色名和中性状态；304px 介绍浮层完整展示职责、能力、边界、常用 Agent 与可证实状态，并支持悬停、焦点、点击固定、重复点击、关闭按钮、Escape、外部点击和焦点恢复。
- 内置浏览器在 `org-org/dev-project`、`/workshop/cockpit` 逐一打开客服专员、私域管家、导购顾问、数据参谋、内容官与活动策划师；496px 窄视口中浮层在任务区内部滚动，没有覆盖共享业务能力和明日预告。`?colleague=shopping_advisor&focus=contribution` 深链自动展开导购顾问且完成角色锚定。
- 专项测试 `23/23`、Web 累计回归 `2428/2428`、生产构建 GREEN；证据位于 `.evidence/workshop/2026-09-03-r3-cockpit-colleague-popovers/`。
- 结论：`WORKSHOP_R3_04_COCKPIT_COLLEAGUE_POPOVERS_GREEN`。本项没有创建 Plan/TaskRun、派发、发送、发布、改价或 Provider 调用；下一项为 `R3-05` 十项共享原子能力与贡献链。

#### R3-05 十项共享原子能力与贡献链精确施工范围（2026-09-03）

1. 正式能力集合固定为已评审的十个 canonical Capability ID：`material.collect`、`strategy.plan`、`copy.generate`、`script.compose`、`speech.synthesize`、`video.compose`、`content.review`、`live.orchestrate`、`platform.adapt`、`performance.review`；产品名称依次为素材采集、策略规划、文案生成、脚本撰写、语音合成、视频合成、内容审核、直播编排、平台适配、数据复盘。十项是跨工作台复用的 capability 分类，不伪造十个固定运行实例。
2. 页面必须独立读取当前租户 `/v1/aip/capability-catalog` 和 `/v1/aip/agent-registry`：能力状态来自 canonical CapabilityRevision；Skill、Logic 和数字同事关系只由 SkillTemplate 的 `requiredCapabilities`、`canonicalLogicId` 与 AgentTemplate/Instance 组合。不得再用 Task blocker dependency 推导能力，也不得把两个泛化依赖标签冒充十项能力。
3. 能力带保持视觉稿单行十胶囊和内部横向滚动；每项以颜色和中文状态区分可用、能力受限、暂停使用、暂不可用、待核对。点击胶囊打开可访问详情，展示 exact Capability revision、关联 Skill、Logic、数字同事及“任务总控贡献”说明；没有 canonical 关系时明确显示没有可验证关系，不补造引用。
4. 读取能力或数字同事目录失败时，十项产品名称仍作为固定产品目录可见，但状态统一为待核对且详情说明权威读取失败；失败不能回退为 blocker dependency，也不能影响任务总控、下达、筛选和六数字同事浮层。
5. 文件级范围：
   - `apps/web/src/components/workshop/TaskCockpitPage.tsx`：并行读取 capability/agent catalog、十项确定性关联、能力胶囊与详情交互。
   - `apps/web/src/components/workshop/TaskCockpitPage.test.tsx`：覆盖十项顺序、真实状态、Skill/Logic/数字同事关系、无关系、读取失败、点击/关闭和零外部副作用。
   - `apps/web/src/styles/45-ecommerce-workshop.css`：恢复视觉稿单行十胶囊、状态色、横向滚动及不抬高底部能力带。
   - `.evidence/workshop/2026-09-03-r3-cockpit-shared-capability-chain/`：保存专项、累计、构建和内置浏览器十项点击证据。
6. 验收顺序：能力目录与组件专项测试 → Web 累计回归与生产构建 → 内置浏览器在 `org-org/dev-project` 核对十项状态并点击查看贡献链 → 方案/实现一致性复审 → Delivery Receipt、authority CAS、memory sync/validate/gate 与 Prime 回读 → 自动进入 R3-06。

#### R3-05 闭合记录（2026-09-03）

- 实现提交：`512d2a18`。底部能力带固定呈现十项 canonical Capability；状态来自 CapabilityRevision，详情关系只由 SkillTemplate、Logic 与 AgentTemplate 组成，目录失败和无关系均保持可信空态。
- 内置浏览器在 `org-org/dev-project`、`/workshop/cockpit` 逐一点击十项：十个 CapabilityRevision 均可回读，其中七项具有 exact Skill→Logic→数字同事贡献链；语音合成、视频合成、直播编排当前没有 canonical 关系，页面明确不补造。单行横向滚动、详情关闭和 Escape 均可工作，未覆盖明日预告。
- 专项测试 `25/25`、Web 累计回归 `271 files / 2430 tests`、生产构建 `369 modules` GREEN；证据位于 `.evidence/workshop/2026-09-03-r3-cockpit-shared-capability-chain/`。
- 结论：`WORKSHOP_R3_05_COCKPIT_SHARED_CAPABILITY_CHAIN_GREEN`。本项没有修改业务数据或触发外部副作用；下一项自动进入 `R3-06` 右侧今日复盘、AI 改进建议与 Wiki 今日入库。
- 封板补记（2026-09-03 23:32，接续执行者）：原执行者在第 7/8 步中断，第 8/8 步由接续执行者完成。接续前独立重跑专项 `25/25`、Web 累计回归 `271 files / 2430 tests`、TypeScript 与生产构建，全部 GREEN，未采信上一执行者报数。Delivery Receipt 已落 `WORKSHOP-R3-05-COCKPIT-SHARED-CAPABILITY-CHAIN.json`，authority CAS 至 `AOS-000462`，`memory sync --apply --prime` 后七条强一致投影均 CURRENT，R3-05 租约已释放。

#### R3-06 右侧复盘三段精确施工范围（2026-09-03）

1. 正式视觉源仍以 `docs/palantier/foundry/html/workshop-task-cockpit.html` 右 1/3 栏为准，恢复三段固定结构：`今日复盘`、`AI 改进建议`、`经验沉淀 Wiki · 今日入库`。视觉稿中的「有效 6 · 待定 1 · 有害 1」、`CN-05 朋友圈3条内容`、`AFT-03 过敏投诉误判`、`VIP3过敏处理SOP · v3` 等全部是示例文案，**一律不得复制到实现**。
2. 三段数据只来自 canonical 权威，各自独立读取、独立失败关闭，任一段失败不得影响 KPI、下达带、任务流、六数字同事浮层与十项能力带：
   - `今日复盘`：复用已解析的 Task Cockpit core `items` 与 `taskCutoff`，按 `taskCutoff` 当日筛选处于终态的业务任务（`completed`/`failed`/`cancelled`/`rolled_back`），并以 `run.status` 与 `run.finishedAt` 作为执行记录归因。**效果结论（有效/无结论/有害）属于 EffectReview/Eval 语义，当前 core 响应不提供逐任务 EffectReview，因此一律显示「尚无可验证效果结论」，不得用 `run.status=succeeded` 冒充「有效」，也不得用 `failed` 冒充「有害」。**
   - `AI 改进建议`：独立读取 `GET /v1/aip/memory-authority/improvement-observations`，消费 `ImprovementObservation` 的 `conclusion`（`improved`/`unchanged`/`regressed`/`insufficient_evidence`）、`metrics`、`quality`（`measured`/`estimated`/`unknown`）、`limitations`、`cutoffAt`、`observationHash` 与 `agentInstanceRef`。`quality != measured` 或 `conclusion = insufficient_evidence` 时必须显式标注证据不足，不得把观察写成结论。
   - `经验沉淀 Wiki · 今日入库`：独立读取 `GET /v1/aip/memory-authority/candidates` 与 `GET /v1/aip/memory-authority/memories`，按 `createdAt` 当日统计 `MemoryCandidate`（`pending`/`quarantined`/`rejected`/`approved`/`promoted`）与 `MemoryAuthorityItem`（`item` + `revision`）。隔离项必须显示 `quarantine_reasons`，不得只报总数。
3. 三段均为只读呈现。不得提交 `MemoryCandidate`、不得审批或 promote、不得写 Wiki、不创建 Plan/TaskRun、不派发、不发送、不发布、不改价、不调用 Provider。canonical 侧 `submitCandidate`/`approveCandidate`/`promoteCandidate`/`publishWiki` 一律不接线。
4. 空态与失败态必须可信：三段标题作为固定产品结构始终可见；无当日数据时显示「今日没有可回读的复盘/改进观察/入库记录」；读取失败时显示权威读取失败并保留段落，不回退到 blocker 列表、不补造条目。当前 `task-cockpit-visual-review` 仅渲染 blockers 的单段实现被三段结构取代，blockers 降为「复盘所需数据缺口」的可展开明细，不占据整段。
5. 文件级范围（严格限定，禁止扩散）：
   - `apps/web/src/components/workshop/TaskCockpitPage.tsx`：三段结构、并行独立读取、当日筛选、失败关闭与可访问详情。
   - `apps/web/src/components/workshop/TaskCockpitPage.test.tsx`：覆盖三段顺序与固定可见、当日筛选、无效果结论不冒充、观察证据不足标注、隔离原因可见、三段各自读取失败、零外部副作用。
   - **不新增 SDK**：`apps/web/src/api/aipMemory/client.ts` 的 `AipMemorySdk` 已提供 `improvementObservations()`、`candidates()`、`memories()` 三个只读方法，契约类型 `MemoryImprovementObservation`、`MemoryCandidate`、`MemoryAuthorityItem` 已存在于同目录 `contracts.ts`。R3-06 直接复用，按 R3-05 的 `capabilityClient` 注入模式新增可选 `memoryClient` prop，不重复造客户端。
   - `apps/web/src/styles/45-ecommerce-workshop.css`：按视觉源恢复右 1/3 栏三段纵向分区与段内独立滚动，不抬高或覆盖共享能力带与明日预告。
   - `.evidence/workshop/2026-09-03-r3-cockpit-review-advice-wiki/`：保存专项、累计回归、构建与内置浏览器三段证据。
   - **明确排除**：`apps/web/src/api/ecommerceWorkshop/parser.ts` 及其测试（含用户未提交内容，禁止读改）；`apps/web/src/pages/s2/ModelRuntimePage.test.tsx` 与 `services/aos-api/tests/test_ecommerce_*operations*.py`（非本门未提交改动，保留不动）。
6. 验收顺序（固定八步节拍）：复习上位方案 → 细化本节文件级清单 → 最小改动实现 → 专项组件与 SDK 测试 → Web 累计回归与生产构建 → 内置浏览器在 `org-org/dev-project` 逐段核对三段结构、当日筛选、证据标注与失败态 → 方案/代码一致性复审 → Delivery Receipt、authority CAS、`memory sync --apply --prime`、validate/gate 与 Prime 长记忆回读 → 自动进入 `R3-07`。

#### R3-06 闭合记录（2026-09-04）

- 实现提交：`4dd02d82`。右侧恢复视觉稿三段固定结构（今日复盘 / AI 改进建议 / 经验沉淀 Wiki · 今日入库），三段各自独立读取 canonical 权威、独立失败关闭，任一段失败不影响 KPI、下达带、任务流、六数字同事浮层与十项能力带。
- 关键口径：因 core 响应不按任务暴露 EffectReview/Eval，今日复盘一律显示「尚无可验证效果结论」，未用 `run.status=succeeded` 冒充「有效」、未用 `failed` 冒充「有害」；改进观察对 `insufficient_evidence` 或 `quality != measured` 显式标注证据不足并展开 `limitations`；隔离候选必显 `quarantineReasons`。原先占据整段的 blockers 降为「复盘所需数据缺口 N 项」可展开明细。
- 未新增 SDK：复用既有 `AipMemorySdk` 的 `improvementObservations()`／`candidates()`／`memories()`，按 R3-05 模式注入可选 `memoryClient` prop。复审中另发现并修正 Run 状态误套任务状态词表的问题（新增 `RUN_STATUS_LABELS`）。
- 内置浏览器（CDP 只读）在 `org-org/dev-project`、`/workshop/cockpit` 实测：三段标题与 `aria-label` 一致且顺序正确，示例文案检测为空，写入控件为零，KPI 带与十项能力带无回归；三个 canonical 接口均 `GET 200` 返回 `[]`，证明当前三段空态属实而非静默失败。
- 专项测试 `31/31`（含 6 项新增，先 RED 后 GREEN）、Web 累计回归 `271 files / 2436 tests`、`tsc` 无错误、生产构建 GREEN；证据位于 `.evidence/workshop/2026-09-03-r3-cockpit-review-advice-wiki/`。
- 数据说明：本租户今日无改进观察与入库记录，有数据分支由专项测试覆盖；任务卡片 Run 状态已统一使用 `RUN_STATUS_LABELS`，不再泄露英文状态或误套任务状态词表。
- 结论：`WORKSHOP_R3_06_COCKPIT_REVIEW_ADVICE_WIKI_GREEN`。本项没有修改业务数据或触发外部副作用；下一项进入 `R3-07`。

#### R3-07 第 1/8 步调研结论（2026-09-04）

内置浏览器（CDP 只读）在 `org-org/dev-project`、`/workshop/cockpit`、1280×720 实测几何，证据 `.evidence/workshop/2026-09-04-r3-cockpit-layout-and-task-loop/layout-report.json`：

1. **当前不存在遮挡**：`skills × taskColumn`、`skills × roleColumn`、`skills × review`、`tomorrow × skills`、`tomorrow × taskColumn` 五项重叠检测全部为 `false`。能力带 `599→649`、明日预告 `649→683`、三列 `174→598`，纵向严格相邻不重叠；`surface` 底 `683` 在视口 `720` 内。
2. **数字同事列完整可见**：6 张卡片，最后一张底边 `526`，低于能力带顶边 `599`，`lastColleagueCardFullyVisible = true`；`roleColumn` 未溢出（`scrollHeight = clientHeight = 424`）。
3. **滚动容器已就位但未被触发**：`roleColumn`、`taskColumn`、`review` 的 `overflow-y` 均为 `auto`，但当前内容都未溢出（`verticallyScrollable = false`），`documentScrollable = false`，页面无外层滚动。
4. **当前数据事实**：任务流只有 4 张卡片，`taskColumn` 424px 恰好装下；因此生产页面只能证明当前数据下无重叠，不能单靠增加真实业务任务来压测布局。
5. **继续施工口径**：不为视觉压测补造业务数据。组件层以不少于 8 条 canonical 形状任务构造确定性溢出场景，验证任务列独立滚动、六数字同事列和底部两带保持固定且互不遮挡；内置浏览器在 `org-org/dev-project` 使用当前真实任务验证筛选、详情、复盘、回读与布局几何。创建链路沿用 R3-03 已闭合的专项测试和 Receipt 证据，本项不重复写入真实业务数据，也不把真实数据量不足作为停止施工条件。

#### R3-07 布局与真实任务回读精确施工范围（2026-09-04）

1. **固定层级**：主面板必须由指标带、下达带、四列任务板、十项共享能力带、明日预告依次组成；任务板独占剩余高度，底部两带参与正常 Flex 布局，不得用 fixed/absolute 覆盖任务或数字同事。
2. **独立滚动**：任务流、数字同事列与右侧复盘列各自 `min-height: 0; overflow-y: auto`；用溢出组件场景断言任务列可滚动且滚动不改变页面外层、数字同事列、能力带和明日预告的位置。
3. **真实回读**：内置浏览器只在 `org-org/dev-project` 操作当前 canonical 任务，逐项验证状态筛选、任务卡详情、今日复盘、重新读取及 URL/租户保持；不得以开发编号或方案文本补造业务项。
4. **创建链复核**：复用 R3-03 的 `createTask` 契约、Receipt 与错误回读测试，重新跑专项回归；本波不为压测新增真实业务任务，不触发发布、发送、退款、调价或 Provider 外部副作用。
5. **文件级范围**：优先只改 `apps/web/src/components/workshop/TaskCockpitPage.test.tsx` 补充溢出与交互回归；仅当测试证明布局实现有缺陷时，才最小修改 `TaskCockpitPage.tsx` 或 `apps/web/src/styles/45-ecommerce-workshop.css`。证据写入 `.evidence/workshop/2026-09-04-r3-cockpit-layout-and-task-loop/`。
6. **验收顺序**：专项测试 → Web 累计回归与生产构建 → 内置浏览器真实租户逐项点击与三视口几何 → 方案/代码一致性复审 → Delivery Receipt、authority CAS、Prime memory sync/validate/gate → 自动进入 `R4-C01`。

#### R3-07 闭合记录（2026-09-04）

- 证据提交：`e16d6ef5`。生产实现沿用 R3-01～R3-06 已形成的 Flex 正常流、列内滚动、六数字同事、推荐填充、任务创建契约、十项能力和复盘三段；本项复审未发现必须改动生产代码的缺陷，避免无目的变更。
- 专项测试 31/31、Web 累计回归 271 文件 / 2436 测试、TypeScript 与 Vite 生产构建全部通过。
- 内置浏览器在 `org-org/dev-project` 完成推荐填充、状态筛选、导购顾问浮层、策略规划贡献链、右侧三段与重新回读验收；当前 canonical 任务为 4 项。
- 1280×720、1440×900、1920×1080 三视口均无任务板/能力带/明日预告重叠。临时 12 卡 DOM 溢出探针证明任务列独立滚动，数字同事列和底部两带不移动；探针同表达式恢复，未写业务数据。
- 结论：`WORKSHOP_R3_07_COCKPIT_LAYOUT_TASK_LOOP_GREEN`。R3 七项全部闭合；下一项自动进入 `R4-C01` 内容与活动工作台视觉结构。

### R4 · 内容与活动 + 统一运营（12 项）

#### 内容与活动工作台（6 项）

- [ ] `R4-C01` 按视觉稿恢复活动策划、内容日历、日常模板等标签页、三栏布局、AI 策划助手、证据/风险侧栏和底部审批栏。
- [ ] `R4-C02` 补齐 CampaignRevision、CalendarEntry、MasterContentIntent、ContentVariant/ArtifactRelation 的 canonical authority、Store、reader 和 same-cutoff 组合。
- [ ] `R4-C03` 实现活动选择/新建、目标输入、生成方案、保存草稿、重新生成、批准并发布前审批的内部业务闭环；外部发布仍受门控。
- [ ] `R4-C04` 实现折扣/库存等风险决策、约束录入与方案重算；每次决策形成版本和 Receipt，可撤销/回读。
- [ ] `R4-C05` 内容日历、主内容与渠道变体必须显示栖月汇真实商品/库存/活动输入及来源，不得用开发编号或演示案例填充。
- [ ] `R4-C06` 逐个点击标签、列表、展开/编辑、生成、保存、风险选择、审批入口，并在三视口对比正式视觉稿和后端状态。

#### 统一运营驾驶舱（6 项）

- [ ] `R4-O01` 以 `workshop-app-order.html` 重做视觉对账，恢复订单/告警主列表、详情区、证据/建议侧栏和退款处理操作层级。
- [ ] `R4-O02` 修复默认切片选择：当前已有订单 50、订单行 50、库存附着 41/源 50、履约 19、支付 50 时，不能默认落到空的 `operationCases` 阻断页。
- [ ] `R4-O03` 补齐 operation case 的内部 authority/Store/reader，把订单、库存、履约、售后和支付事实组合成可处理但不自动外部执行的运营工单。
- [ ] `R4-O04` 实现筛选、新建内部处理、查看原订单、日志、驳回/修改/批准预览、建议采纳、SOP 等按钮的真实内部状态与 Receipt。
- [ ] `R4-O05` 对账 sourceTotal 219、attached 210、inventory unmatched 9 等当前事实；页面必须显示差异归因和截止时间，不能把 210 误写成全部源记录。
- [ ] `R4-O06` 以栖月汇订单完成切片切换、筛选、详情、处理草稿、审批前预览、证据链和回读浏览器自验收，禁止真实退款/发货等外部副作用。

### R5 · 达人邀约 + 多媒体内容生产（11 项）

#### 达人邀约驾驶舱（5 项）

- [ ] `R5-D01` 恢复视觉稿中的候选、邀约、合作、交付、关系等业务标签/阶段和对应三栏工作区。
- [ ] `R5-D02` 补齐 Candidate/Outreach/Contract/Delivery/Relationship canonical authority、Store、reader 与同租户关联。
- [ ] `R5-D03` 实现导入/新建批次、编写邀约、新建合作、编辑、审批、历史回读的内部闭环；真实发送继续审批后门控。
- [ ] `R5-D04` 将栖月汇商品、达人候选条件、预算/权益、交付物和证据映射为中文业务数据，缺数据时给出可执行的补录入口。
- [ ] `R5-D05` 逐标签、逐按钮、逐列表和滚动区完成三视口浏览器自验收，验证版本、Receipt、幂等和隔离。

#### 多媒体内容生产（6 项）

- [ ] `R5-M01` 恢复视觉稿的媒体类型标签、任务列表、生产中心、证据/版本/发布侧栏和底部批量操作区。
- [ ] `R5-M02` 补齐媒体生命周期 authority/reader，使 provider job、finance、素材、版本、评审和发布贡献能组合成真实可见任务。
- [ ] `R5-M03` 实现新建生产任务、输入/证据、暂停、退回、改派、批量生产、样片、模板、排期和直播控制的内部状态机。
- [ ] `R5-M04` 实现版本历史、导出、评审与发布 Proposal；真实 Provider 生成和外部发布仍必须取得 exact Health/Secret/Approval/Lease。
- [ ] `R5-M05` 空数据时允许创建可工作的内部草稿/计划，不得只显示 `MEDIA_LIFECYCLE_AUTHORITY_NOT_AVAILABLE` 而没有修复入口。
- [ ] `R5-M06` 用栖月汇商品与活动素材完成前后端、版本、评审、Receipt 和三视口视觉自验收，不执行真实外部发布。

### R6 · 经营参谋 / 生意探究（9 项）

- [ ] `R6-01` 将渠道视觉绑定到真实“栖月汇微商城”，不再显示“渠道未知/未选择经营实体”。
- [ ] `R6-02` 把现有 order 124、product 57、customer 54 等 exact 指标水合到经营实体、BusinessInvestigationCase/Run 与经营画像，不另建第二套经营事实权威。
- [ ] `R6-03` 实现 Case/Run 创建或选择、分析记录、计划与定时、继续分析等按钮的内部业务闭环与 Receipt。
- [ ] `R6-04` 恢复并实现经营总览、驱动因素、问题诊断、增长计划、效果复盘、证据链、数据质量等完整标签和状态。
- [ ] `R6-05` 实现三阶段“经营画像→问题与机会→方案设计”推进、checkpoint、暂停/继续和状态回读。
- [ ] `R6-06` 实现提交 DataRequirement、人工确认、证据查看、增长任务/DAG、评审通过/驳回/历史等工作台内部操作。
- [ ] `R6-07` 保持非因果边界：没有 exact 模型和 Eval 时只能呈现观察与假设，不得把相关性写成归因结论；同时不能隐藏已经存在的真实指标。
- [ ] `R6-08` 贯通“原子 Skill→Logic 编排→数字同事绑定→工作台贡献”，显示决策摘要、证据链、归因路径、关键假设和不确定性。
- [ ] `R6-09` 使用栖月汇真实数据完成一次只读生意探究：经营实体→Case/Run→画像→问题/机会→方案草稿→任务建议→证据/评价/回读，全程无外部副作用。

### R7 · 价格治理 + 客户关系（11 项）

#### 价格治理驾驶舱（5 项）

- [ ] `R7-P01` 恢复视觉稿的价格监控/策略/执行或相应三标签、指标、异常列表、竞品卡和右侧策略区。
- [ ] `R7-P02` 补齐价格治理、竞品观察、采集计划、处置建议的 canonical authority/Store/reader 与 exact source refs。
- [ ] `R7-P03` 实现导出、新建策略、刷新、通知草稿、竞品价值卡、人工立即采集等内部动作；真实抓取/调价保持门控。
- [ ] `R7-P04` 栖月汇商品、当前价、库存、竞品观察和策略建议必须能对账；无竞品数据时提供计划/补录而不是死空态。
- [ ] `R7-P05` 完成筛选、策略版本、预览、审批、Receipt、回读和三视口视觉验收，不执行真实改价。

#### 客户关系工作台（6 项）

- [ ] `R7-C01` 恢复视觉稿的客户/分群/旅程/对话或相应视图、名单区、详情区、洞察/动作侧栏。
- [ ] `R7-C02` 补齐 Consent、Segment、Journey、Dialogue、OutreachBatch canonical authority/Store/reader，并执行 purpose/retention/PII 约束。
- [ ] `R7-C03` 现有 CustomerLite 输入 54 条时，至少展示合法汇总、未知/排除计数和修复入口；不能让四个视图全部显示 0 且无可操作路径。
- [ ] `R7-C04` 实现导入/建分群/新建触达草稿、暂停、重试、话术与审批的内部闭环；真实消息发送必须有 consent 和执行门。
- [ ] `R7-C05` 页面只呈现允许披露的字段和聚合，验证脱敏、purpose、retention、跨租户隔离和导出边界。
- [ ] `R7-C06` 用栖月汇 CustomerLite 完成合法分群→旅程→对话/触达草稿→审批前预览→Receipt→回读自验收，不真实发送。

### R8 · 跨页面业务闭环（5 项）

- [ ] `R8-01` 经营参谋输出的任务建议可一键带入日常总控输入框，保留来源 Case/Run/证据 refs，用户确认后生成内部任务。
- [ ] `R8-02` 日常总控任务可跳转到内容、运营、达人、媒体、价格、客户的对应工作区，并带入同租户、同业务对象上下文。
- [ ] `R8-03` 各页处理结果回流日常总控复盘、AI 改进建议和 Wiki 入库区，不丢 Task/Run/Eval/Artifact/Receipt 链路。
- [ ] `R8-04` 统一搜索、筛选、日期、详情抽屉、通知、空态、错误态、返回路径和中文业务文案，清理开发编号进入业务 UI 的情况。
- [ ] `R8-05` 建立八页端到端幂等、并发、刷新恢复、历史版本、失败补偿和跨租户负向回归。

### R9 · 累计产品验收与封板（8 项）

- [ ] `R9-01` 日常总控按正式视觉稿逐组件 1:1 复审，完成所有可见按钮、浮层、滚动和栖月汇数据功能验收。
- [ ] `R9-02` 内容与活动按正式视觉稿逐组件 1:1 复审，完成所有标签、按钮、滚动和栖月汇数据功能验收。
- [ ] `R9-03` 统一运营按 `workshop-app-order.html` 逐组件 1:1 复审，完成所有切片、按钮、滚动和栖月汇数据功能验收。
- [ ] `R9-04` 达人邀约与多媒体分别逐组件 1:1 复审，完成所有标签、按钮、滚动和栖月汇数据功能验收。
- [ ] `R9-05` 经营参谋按正式视觉稿逐组件 1:1 复审，完成渠道/实体/Case/Run、全部标签、按钮和真实数据闭环验收。
- [ ] `R9-06` 价格治理与客户关系分别逐组件 1:1 复审，完成所有标签、按钮、滚动和栖月汇数据功能验收。
- [ ] `R9-07` 执行八页×三视口×展开/折叠×滚到底×键盘×刷新×网络失败×空/部分/ready/conflict 状态累计回归，并保存成对截图、交互轨迹、API/Receipt 对账。
- [ ] `R9-08` 完成方案/代码一致性复审、Delivery Receipt、authority CAS、memory sync/validate/gate 与 Prime 回读；只有 81/81 且用户浏览器验收通过，才允许恢复“产品封板完成”口径，发布仍由独立门决定。

## 5. 串行修复波次

| 顺序 | 波次 | 内容 | Task 数 | 退出条件 |
|---:|---|---|---:|---|
| 1 | R0 | 事实重置、视觉源、差异矩阵、施工包 | 4 | `COMPLETED_GREEN / 4_OF_4` |
| 2 | R1 | 全局 Shell、完整菜单、折叠滚动、公共交互 | 8 | 八页与 Buddy 同一完整菜单源 |
| 3 | R2 | 栖月汇数据、authority、状态与内部 Receipt | 6 | 八页真实数据和状态有统一追溯底座 |
| 4 | R3 | 日常任务总控 | 7 | 视觉、六数字同事、推荐下达、复盘闭环 |
| 5 | R4 | 内容与活动 + 统一运营 | 12 | 两页视觉、内部功能、真实数据闭合 |
| 6 | R5 | 达人邀约 + 多媒体生产 | 11 | 两页内部生命周期与视觉闭合 |
| 7 | R6 | 经营参谋 / 生意探究 | 9 | 栖月汇 Case/Run 只读分析闭环 |
| 8 | R7 | 价格治理 + 客户关系 | 11 | 两页内部功能、合规数据、视觉闭合 |
| 9 | R8 | 跨页任务、复盘、Wiki 与上下文 | 5 | 八页之间形成可追溯业务闭环 |
| 10 | R9 | 累计浏览器、功能、数据、Receipt/Prime 验收 | 8 | 81/81，用户产品验收；发布门另判 |
| **合计** |  |  | **81** | 当前 **22/81**；R0～R2、R3-01～R3-04 已闭合，继续 R3-05 |

## 6. 候选施工文件

公共 Shell：

- `apps/web/src/shell/AppShell.tsx`
- `apps/web/src/shell/AppShell.workshop.test.tsx`
- `apps/web/src/components/workshop/EcommerceWorkshopShell.tsx`
- `apps/web/src/components/workshop/EcommerceWorkshopShell.test.tsx`
- `apps/web/src/styles/45-ecommerce-workshop.css`

八页 Web：

- `apps/web/src/components/workshop/TaskCockpitPage.tsx`
- `apps/web/src/components/workshop/ContentCampaignPage.tsx`
- `apps/web/src/components/workshop/OperationsPage.tsx`
- `apps/web/src/components/workshop/CreatorGrowthPage.tsx`
- `apps/web/src/components/workshop/MediaStudioPage.tsx`
- `apps/web/src/components/workshop/AnalystPage.tsx`
- `apps/web/src/components/workshop/BusinessInvestigationTab.tsx`
- `apps/web/src/components/workshop/PriceGovernancePage.tsx`
- `apps/web/src/components/workshop/CustomerPage.tsx`
- 对应同目录 `*.test.tsx` 与 `apps/web/src/api/ecommerceWorkshop/*`

后端候选范围：

- `services/aos-api/aos_api/ecommerce_workshop_task_cockpit*.py`
- `services/aos-api/aos_api/ecommerce_workshop_content_campaign*.py`
- `services/aos-api/aos_api/ecommerce_workshop_operations*.py`
- `services/aos-api/aos_api/ecommerce_workshop_creator_growth*.py`
- `services/aos-api/aos_api/ecommerce_workshop_media_studio*.py`
- `services/aos-api/aos_api/ecommerce_workshop_analyst*.py`
- `services/aos-api/aos_api/ecommerce_workshop_price_governance*.py`
- `services/aos-api/aos_api/ecommerce_workshop_customer*.py`
- `services/aos-api/aos_api/ecommerce_workshop_source_readiness.py`
- `services/aos-api/aos_api/ecommerce_workshop_shared_context*.py`
- `services/aos-api/aos_api/routers/ecommerce_workshop.py`
- 对应 `services/aos-api/tests/test_ecommerce_workshop_*.py`

正式视觉源：

- `docs/palantier/foundry/html/workshop-task-cockpit.html`
- `docs/palantier/foundry/html/workshop-content-campaign.html`
- `docs/palantier/foundry/html/workshop-app-order.html`
- `docs/palantier/foundry/html/workshop-creator-outreach.html`
- `docs/palantier/foundry/html/workshop-media-studio.html`
- `docs/palantier/foundry/html/workshop-analyst.html`
- `docs/palantier/foundry/html/workshop-price-governance.html`
- `docs/palantier/foundry/html/workshop-customer.html`

## 7. 当前不应再使用的完成判据

- “有按钮且点击后出现提示”不等于功能完成。
- “API 返回 200”不等于页面正确消费真实数据。
- “截图无溢出”不等于与视觉稿 1:1。
- “代码测试 GREEN”不等于栖月汇真实业务功能 GREEN。
- “一个切片 blocked”不应遮蔽同页其他 ready 切片。
- “96/96 工程清单完成”不等于 81 项产品缺陷已修复。
- “负向租户没有数据”不等于正向租户已完成。
- “内部工作台可写”不等于允许 Provider、消息、调价、发布或其他真实外部副作用。

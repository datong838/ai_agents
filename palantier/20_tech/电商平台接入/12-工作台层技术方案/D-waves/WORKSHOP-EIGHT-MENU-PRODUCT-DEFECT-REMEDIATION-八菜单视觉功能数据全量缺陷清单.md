# 工作台八菜单视觉、功能、数据全量缺陷清单与串行修复波次

> 审计日期：2026-08-30
> 状态：`PRODUCT_ACCEPTANCE_REOPENED / R2_3_OF_6 / TOTAL_15_OF_81 / R2_IN_PROGRESS / NO_RELEASE`
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
- [ ] `R2-04` 统一 loading/empty/blocked/partial/ready/conflict 状态；已有真实切片时不得因为另一个切片 blocked 而把整页显示成死页面。
- [ ] `R2-05` 为允许的工作台内部写操作建立 preview→confirm→Receipt→readback 闭环和幂等保护；真实外部动作继续失败关闭。
- [ ] `R2-06` 建立 `dev-org/dev-project` 隔离负向回归，证明无跨租户泄漏，但不把负向 canary 当正向业务完成证据。

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

- [ ] `R3-01` 按视觉稿恢复 KPI 顶栏、下达区、执行组、中央任务流、策划组、右侧复盘、底部共享能力和明日预告的完整比例与层级。
- [ ] `R3-02` 恢复“下达”右侧经营参谋推荐任务；点击推荐项必须自动填入任务输入框，允许用户继续编辑后下达。
- [ ] `R3-03` 实现任务输入→安全预检→内部任务草稿/Task→数字同事分派→Receipt→列表回读闭环；无条件时按钮明确禁用，不得只显示提示。
- [ ] `R3-04` 完整实现 6 个数字同事卡片及介绍浮层：职责、边界、常用 Agent、当前状态；浮层尺寸、锚点、遮挡、滚动和关闭行为与视觉稿一致。
- [ ] `R3-05` 恢复 10 个共享原子能力/Agent 标签，展示真实可用性和“原子 Skill→Logic→数字同事→工作台贡献”关系，不以两个泛化标签代替。
- [ ] `R3-06` 恢复右侧三段：今日复盘、AI 改进建议、经验沉淀 Wiki·今日入库；数据来自真实 Task/Run/Eval/Wiki，不能复制视觉稿示例。
- [ ] `R3-07` 修复底部能力带与明日预告遮挡、任务列表滚动、数字同事列可见性，并完成真实栖月汇任务的创建、筛选、详情、复盘和回读自验收。

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
| **合计** |  |  | **81** | 当前 **15/81**；R2-01/02/03 已闭合，继续 R2-04～06 |

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

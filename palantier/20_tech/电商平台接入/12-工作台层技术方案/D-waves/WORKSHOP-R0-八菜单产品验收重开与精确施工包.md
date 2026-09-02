# WORKSHOP R0 八菜单产品验收重开与精确施工包

> 日期：2026-09-02
> Task：`WORKSHOP-R0-PRODUCT-ACCEPTANCE-REOPEN-EXACT-CONSTRUCTION`
> 基线 revision：`AOS-000448`
> 状态：`R0_4_OF_4 / PRODUCT_ACCEPTANCE_REOPENED / TOTAL_4_OF_81 / NO_EXTERNAL_EFFECT / NO_RELEASE`

## 1. 事实裁决

1. AIP P0～P8 的 `132/132` 是已经闭合的 AIP 菜单产品整改事实，继续保留。
2. Workshop 原 W0～W8 的 `96/96` 是工程合同历史完成事实，继续保留。
3. 用户当前浏览器验收重新发现的八菜单视觉、功能、真实数据问题属于独立产品缺陷账本；当前只完成 R0 施工准备，产品进度为 `4/81`，不得称八菜单已经产品封板。
4. 后续只在 `m1` 由唯一开发者串行执行 R1～R9。能在 AOS 四层内解决的缺口直接维护；真实 Provider、消息发送、退款/发货、调价、发布、生产迁移仍必须经过原安全门。

## 2. 八页唯一视觉源冻结

| 工作台页面 | 路由 | 唯一正式视觉源 | SHA-256 |
|---|---|---|---|
| 日常任务总控 | `/workshop/cockpit` | `foundry/html/workshop-task-cockpit.html` | `7bb381743d1a68e65a7455e292ee19d6330e6559baad6a444b4bbe0f64d8942f` |
| 内容与活动 | `/workshop/content-campaign` | `foundry/html/workshop-content-campaign.html` | `795ba48c94b7e1adc5bfe8420ad4bf226f3092ce2d9eb34af163dd4346b92567` |
| 统一运营 | `/workshop/operations` | `foundry/html/workshop-app-order.html` | `96f0bf5fe7682b990bc85f9caf6dc8c254ae37cf43d0010d94097b5457b786c6` |
| 达人邀约 | `/workshop/creator-growth` | `foundry/html/workshop-creator-outreach.html` | `70ac7ad6b92579353b42aaaf17c728fb0a55ea884dd1a717bbda3de075344f37` |
| 多媒体生产 | `/workshop/media-studio` | `foundry/html/workshop-media-studio.html` | `428fe0230f9577b3c7329ee320dd31036c3f2b38a8784e0c8f9dbd6e41341daf` |
| 经营参谋 | `/workshop/analyst` | `foundry/html/workshop-analyst.html` | `d8cc491f03f12c84614ac1ddf900633d503efc4f406e4e60216cdb31e1458043` |
| 价格治理 | `/workshop/price-governance` | `foundry/html/workshop-price-governance.html` | `cb1cc38b995b937965cd60e62b770a2281b7788195d198fdc6327e2b86ae0355` |
| 客户关系 | `/workshop/customer` | `foundry/html/workshop-customer.html` | `0f0668e5644ecfb2f97ac6f4d2b8eb8c38f873278751625233a145c6a6695b7c` |

统一运营不得改用 `workshop-cop.html`。视觉验收必须使用内置浏览器在 1280×720、1440×900、1920×1080 三档逐页对照，而不是只比较控件数量。

## 3. 五列逐组件施工矩阵

| 页面与组件组 | 视觉元素 | 工作台内部业务动作 | API / canonical authority | 栖月汇真实数据 | 权限与副作用门 |
|---|---|---|---|---|---|
| 日常总控 | KPI、推荐下达、六数字同事、中央任务流、十项能力、三段复盘、明日预告 | 推荐回填、任务草稿、预检、分派、Receipt、筛选、复盘回读 | Task/Run/Eval/Wiki/Receipt 与六同事绑定 | `org-org/dev-project` 的真实经营任务、订单/内容/客户切片 | 允许内部任务写；禁止外部发送、发布和业务源修改 |
| 内容与活动 | 三标签、活动列表、策划助手、方案主体、风险侧栏、底部审批 | 选择/新建活动、生成内部方案、保存/重算、风险决策、审批预览 | CampaignRevision、CalendarEntry、MasterContentIntent、ContentVariant | 栖月汇商品、库存、活动和内容输入 | 允许内部草稿/版本；真实渠道发布仍门控 |
| 统一运营 | 订单/告警列表、详情、证据建议、处置操作 | 筛选、内部工单、日志、建议采纳、审批预览、Receipt | OperationCase 与 Order/OrderLine/Inventory/Fulfillment/Payment 组合 | 当前订单 50、订单行 50、库存附着 41/源 50、履约 19、支付 50 | 禁止真实退款、发货与支付操作 |
| 达人邀约 | 候选、邀约、合作、交付、关系阶段与三栏工作区 | 批次、邀约草稿、合作草稿、编辑、审批和历史 | Candidate/Outreach/Contract/Delivery/Relationship | 栖月汇商品、候选条件、预算权益、交付物 | 允许内部草稿；真实消息发送需独立 consent/approval |
| 多媒体生产 | 媒体标签、任务、生产中心、版本/证据/发布侧栏、批量栏 | 新建、暂停、退回、改派、样片、模板、排期、评审/发布 Proposal | MediaJob/Artifact/Version/Review/Provider contribution | 栖月汇商品、活动与可审计素材 | 禁止未授权 Provider 调用和外部发布 |
| 经营参谋 | 渠道/实体、Case/Run、三阶段、八标签、数据与运行门 | 选择/创建 Case/Run、继续分析、计划、checkpoint、证据与方案草稿 | BusinessInvestigationCase/Run、DataRequirement/Fulfillment、Evidence/Eval | 栖月汇订单 124、商品 57、客户 54 等 exact 只读指标 | 只读探究与内部方案；无 exact 模型不得宣称因果或执行外部动作 |
| 价格治理 | 价格监控、策略、执行标签，异常、竞品、策略侧栏 | 筛选、内部策略版本、采集计划、预览、审批、Receipt | PriceObservation/Policy/CollectionPlan/Disposition | 栖月汇商品当前价、库存和已有竞品观察 | 禁止真实抓取和调价 |
| 客户关系 | 客户、分群、旅程、对话，名单、详情、洞察动作 | 合法汇总、分群、旅程、触达草稿、暂停/重试、审批预览 | CustomerLite/Consent/Segment/Journey/Dialogue/OutreachBatch | 栖月汇 CustomerLite 54 条及合法聚合 | purpose/retention/PII/consent 必须通过；禁止真实发送 |

矩阵中的每个后续条目都必须同时关闭视觉、动作、authority、真实数据和安全门；任何一列缺失均不能勾选产品任务。

## 4. 精确施工与保护范围

### R1 首批文件

- `apps/web/src/shell/AppShell.tsx`
- `apps/web/src/shell/AppShell.workshop.test.tsx`
- `apps/web/src/components/workshop/EcommerceWorkshopShell.tsx`
- `apps/web/src/components/workshop/EcommerceWorkshopShell.test.tsx`
- `apps/web/src/components/workshop/*Page.tsx` 中重复菜单壳的最小删除范围
- `apps/web/src/styles/45-ecommerce-workshop.css`

### R1 回归

- 八路由与 Buddy 消费同一 canonical 菜单源，分组、顺序、权限过滤一致。
- 八页逐一滚轮到底，折叠、展开、刷新、跳页、高亮和焦点恢复可用。
- 三视口检查顶部挤压、固定区遮挡、底部能力带、明日预告、抽屉和数字同事浮层。
- 既有路由、租户隔离与 AIP P0～P8 132/132 回归不倒退。

### 受保护范围

- 不触碰当前工作树中无关的 `.evidence/aip/**`、`ModelRuntimePage.test.tsx`、`plugins/ops/**` 等既有未提交内容。
- 不 reset、rebase、force-push、clean，不覆盖其他历史证据。
- 不修改真实业务数据，不读取或覆盖旧 `w1-aip` 未提交工作区。

## 5. R0 退出条件

- [x] 产品口径已重开，历史工程事实与当前产品事实分离。
- [x] 八页唯一视觉源及 SHA-256 已冻结。
- [x] 八页五列逐组件施工矩阵已建立。
- [x] Task Receipt/Lease、候选文件、回归和保护范围已冻结。

下一任务：`WORKSHOP-R1-GLOBAL-SHELL-FULL-NAVIGATION`。

# O1-UX8：对象业务展示名与图谱中文语义执行清单

> **版本**：v1.0 · 2026-08-10
> **状态**：GREEN · 已实现并完成浏览器验收
> **目标范围**：`org-org` · `dev-project`（栖月汇商贸有限公司 · 默认工作区）
> **上位方案**：`O1-UX7-对象探索真实有效对象与字段语义修复清单.md`、`O1-UX4-统一知识图谱画布执行清单.md`

## 0. Rules

1. 只修展示语义，不修改 canonical `objectId`、GraphSnapshot 节点 key、Link 端点、URL 引用、数据库或源商城数据。
2. 展示名由服务端基于当前租户已脱敏的真实对象属性计算；前端不得从 `niushop:1:20` 猜业务名称。
3. `org-org/dev-project` 是唯一真实正向范围；`dev-org` 只用于负向隔离 canary。
4. Order/Product 等业务名称优先，缺少名称时回退为“中文对象类型 + 源记录号”；不得回退成英文类型加完整内部 ID 作为主标题。
5. 表格、对象详情、图谱节点、图谱列表和图例使用同一套中文类型词典；关系类型只做只读中文解释，不改变 relationType。
6. 先补失败测试，再做最小实现；完成后必须用内置浏览器验证真实订单、商品和领域知识图谱。

## 1. 问题与语义说明

`niushop:1:20` 是稳定外部身份，不是业务标题：

| 分段 | 含义 | 展示策略 |
|---|---|---|
| `niushop` | 来源平台 | 详情或悬浮说明显示“Niushop 微商城” |
| `1` | 来源站点 `site_id=1` | 详情或悬浮说明显示“站点 1” |
| `20` | 源表主键 | 次级显示“源记录 #20” |

当前表格把完整 external ID 放在首列，图谱节点和图例还显示 `Order · niushop:1:20`、`Payment` 等工程词，用户无法快速识别真实业务对象。

## 2. 冻结展示规则

### 2.1 对象类型中文词典

| Object Type | 中文名称 |
|---|---|
| `Order` | 订单 |
| `OrderLine` | 订单明细 |
| `Payment` | 支付记录 |
| `Product` | 商品 |
| `ProductSku` | 商品 SKU |
| `Shipment` | 发货记录 |
| `Shop` | 店铺 |
| `Weapp` | 小程序 |
| `CustomerLite` | 会员 |
| `Category` | 商品类目 |
| `ProductReview` | 商品评价 |
| `SystemConfig` | 系统配置 |

未知类型保留原始类型名，避免错误翻译。

### 2.2 业务展示名优先级

| Object Type | 首选安全字段 | 无首选字段时 |
|---|---|---|
| Order | `orderNo` | `订单 · 源记录 #<source_pk>` |
| Product | `title` | `商品 · 源记录 #<source_pk>` |
| Category | `name` | `商品类目 · 源记录 #<source_pk>` |
| Shop | `name` | `店铺 · 源记录 #<source_pk>` |
| Weapp | `name` | `小程序 · 源记录 #<source_pk>` |
| Payment | `outTradeNo` | `支付记录 · 源记录 #<source_pk>` |
| Shipment | `trackingNo` 不作为主标题，避免扩大物流标识暴露 | `发货记录 · 源记录 #<source_pk>` |
| ProductSku/OrderLine/CustomerLite/ProductReview/SystemConfig | 不拼接可能敏感或难懂的复合字段 | `<中文类型> · 源记录 #<source_pk>` |

服务端只从完成字段级脱敏后的属性生成 `_displayLabel`；空值、对象、数组和过长值不得进入标题。

### 2.3 页面显示

- 表格首列从“订单 ID/商品 ID”改为“订单/商品”，主行显示 `_displayLabel`，次行显示“源记录 #20”。
- 完整 `niushop:1:20` 保留在 `title`/对象详情的“系统标识”中，不改变选中、搜索参数或对象集引用。
- 对象详情标题使用 `_displayLabel`；系统标识放在次级信息。
- GraphSnapshot 的 `objectId/key/edge source/target` 保持不变，`label` 改为业务展示名。
- 图谱节点、邻居列表、图例、ARIA 文案使用中文对象类型；节点次行只显示“订单 · 源记录 #20 · 第 0 层”。
- relationType 原值保持不变，画布显示词典化中文，如 `Order.fromWeapp -> 订单来源于小程序`；未知关系显示原值。

## 3. 文件级实施清单

### 后端

- [x] 新增 `services/aos-api/aos_api/ontology_display_names.py`：中文类型、relationType、external ID 解析和安全展示名解析。
- [x] 修改 `services/aos-api/aos_api/routers/ontology.py`：对象 list/detail 在字段脱敏后追加 `_displayLabel`、`_sourceRecordLabel`、`_sourceIdentityLabel` 展示投影。
- [x] 修改 `services/aos-api/aos_api/ontology_graph_query.py`：领域图读取 `properties` 并复用展示名解析；不改变稳定节点身份和边。
- [x] 新增/修改后端测试：覆盖真实 Order/Product、无名称 fallback、复杂值、PII 不进入标题、GraphSnapshot identity 不变。

### 前端

- [x] 新增 `apps/web/src/components/ontology/ontologyDisplayNames.ts`：只负责中文类型/关系显示和安全消费服务端展示投影，不自行改 objectId。
- [x] 修改 `apps/web/src/components/ontology/ObjectExplorerWorkspace.tsx`：Order/Product 首列语义从 ID 改为业务对象。
- [x] 修改 `apps/web/src/pages/s2/workshop.tsx`：表格、详情、邻居、筛选项和 toast 使用展示投影；系统引用仍用 objectId。
- [x] 修改 `apps/web/src/components/ontology/OntologyGraphCanvas.tsx`：图例、节点次行、关系标签和 ARIA 中文化。
- [x] 修改必要 CSS：主标题/次级来源信息两行层级清晰，不扩大列宽破坏现有布局。
- [x] 修改前端测试：表格不再把 `niushop:1:20` 作为主标题；图谱显示中文业务名但选中回调仍返回原 objectId。

## 4. 测试与浏览器验收

### 后端定向门

- 展示名解析纯函数测试。
- `/v1/objects/Order` 与详情响应包含安全 `_displayLabel`，原 `id` 完全不变。
- GraphSnapshot 节点 label 为业务中文，key/objectId/edge source/target 与修改前完全一致。
- `dev-org/dev-project` 不可读取栖月汇对象。

### 前端定向门

- `workshop.test.ts` 覆盖订单号主标题、商品名称主标题和无名称 fallback。
- `ontologyGraph.test.ts`、画布交互测试覆盖中文图例/关系/ARIA，身份不变。
- TypeScript、production build 和相关 Vitest 通过。

### 内置浏览器

1. Order 表格：首列显示“订单 + 真实订单号”，不再以 `niushop:1:*` 为主标题。
2. Product 表格：首列显示“商品 + 真实商品名”。
3. 点击订单：详情标题可读，URL 与对象引用仍保留 canonical ID。
4. 切换图谱：Order/Payment/Shipment/Weapp 等节点和图例中文可读。
5. 双击/选择图谱节点：仍能打开正确对象，不因展示名改变 identity。
6. Network/API 对账：返回真实 `org-org/dev-project` 数据，无 Mock/fallback。

## 5. 退出门与回滚

### 退出门

- [x] 用户主视图不再需要理解 `niushop:1:20` 才能识别订单或商品。
- [x] 表格、详情、图谱展示名一致；canonical identity、Link 和 GraphSnapshot authority 未变化。
- [x] 没有 PII、物流单号、手机号等因展示名拼装扩大暴露。
- [x] 定向测试、类型检查、构建和真实租户浏览器验证通过并保存新鲜证据；租户边界沿用 O1-UX3 权威图定向回归。

### 回滚

- 回退展示投影、前端消费与文案映射即可；不需要数据库回滚。
- 回滚不得删除本波前后的浏览器、测试和 API 证据。
- 若某业务字段不可靠，回退为“中文类型 + 源记录号”，不得回退为伪造业务名称。

## 6. 实施与复审结论

- 代码提交：`aos-platform@m1@2fc361d`，已推送 `origin/m1`。
- 后端定向验证：`9 passed`；前端定向验证：`3 files / 20 tests passed`；TypeScript 与 production build 通过。
- 真实 Order：61 条；`niushop:1:20` 主显示为“订单 · 2026030723225001”，次显示“源记录 #20”，订单号搜索得到 1 条并打开同一 canonical 对象。
- 真实 Product：39 条实际上架商品；首列显示“商品 · <真实商品名>”，完整 internal ID 不再占据主视觉。
- 图谱：Order/Payment/Shipment/Weapp 等节点、图例、关系标签、筛选项与 ARIA 已中文化；节点 key、objectId 和 edge source/target 未变化。
- 安全复审：业务标题只读取 allow-list 字段；Shipment trackingNo、CustomerLite mobile 等不进入标题；未知对象回退到中文类型与源记录号。
- 证据：`palantier/20_tech/evidence/o1-ux/ux8/2026-08-10T1028+0800/`。
- 结论：本清单实现与方案一致，自洽性复审通过，状态 **GREEN**。

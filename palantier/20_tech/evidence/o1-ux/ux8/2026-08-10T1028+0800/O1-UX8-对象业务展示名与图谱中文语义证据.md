# O1-UX8 对象业务展示名与图谱中文语义证据

> 时间：2026-08-10 10:28—11:10 +08:00
> 正向租户：`org-org / dev-project`（栖月汇商贸有限公司 / 默认工作区）
> 代码：`aos-platform@m1@2fc361d`
> 结论：**GREEN**

## 结果

| 门 | 结果 |
|---|---|
| 后端展示名与权威图定向测试 | 9 passed |
| 前端展示名、对象探索、图布局测试 | 3 files / 20 tests passed |
| TypeScript | passed |
| production build | passed，254 modules transformed |
| Order 真实页面 | 61 条；订单号为主标题，source record 为次标题 |
| Product 真实页面 | 39 条实际上架商品；真实商品名为主标题 |
| 订单搜索 | `2026030723225001` 返回 1 条并保持 `niushop:1:20` canonical 引用 |
| 领域知识图谱 | 70 节点 / 73 边；类型、节点、关系与筛选项中文可读 |

## 浏览器证据

1. `browser-before/01-product-table-internal-id.png`：整改前 Product 首列以 internal ID 为主。
2. `browser-after/01-order-business-labels.png`：Order 首列为“订单 · 真实订单号”，次行为“源记录 #N”。
3. `browser-after/02-order-graph-business-labels.png`：对象详情与嵌入图谱使用相同业务展示名。
4. `browser-after/04-order-graph-zoomed-business-labels.png`：放大后可见订单、商品、支付、会员等中文节点名。
5. `browser-after/05-order-search-detail-business-labels.png`：订单号搜索、表格与详情一致，canonical ID 仍在详情属性中。
6. `browser-after/06-product-business-labels.png`：39 条真实上架商品使用真实商品名称。

## 身份与安全对账

- `_displayLabel` 只在字段脱敏后生成；GraphSnapshot 直读也只读取安全字段 allow-list。
- `objectId/key/Link endpoint/URL/ObjectSet reference` 完全不变。
- Shipment 不使用 trackingNo，CustomerLite 不使用 mobile；无安全业务名时回退为“中文类型 · 源记录 #N”。
- 本波未写商城源数据、未迁移数据库、未改变租户或工作区归属。

## 已知后续项

70 节点两跳图在“适配”后仍偏小，属于既有图谱密度与布局任务，不影响本波中文展示名 GREEN；应留在后续图谱聚类、按关系折叠和语义缩放清单中处理。

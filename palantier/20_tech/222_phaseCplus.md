# 222 Phase C+ 技术方案 · 订单管理应用实例

> **版本**：v1.0 · 2026-07-25
> **关联**：[222plan-分阶段开发与里程碑计划.md](222plan-分阶段开发与里程碑计划.md)
> **对应章节**：222 第 12 章 · 视觉稿 `workshop-app-order.html`
> **目标**：实现视觉稿中「工作台 → 订单管理」的完整前后端，作为 Workshop 画布编辑器的**首个真实业务应用实例**
> **状态**：✅ 已完成

---

## 一、背景

视觉稿侧栏「工作台」分区有 `订单管理(workshop-app-order)` 菜单项，但 React 前端 `nav.ts` 中缺失。后端有 `WorkOrder`（工单）但没有 `Order`（电商订单）。需要补齐完整的订单管理应用。

## 二、后端现有基础设施审计

后端已有完整的 Ontology + Action 基础设施，Phase C+ **不需要新建引擎**：

| 基础设施 | 文件 | 说明 |
|----------|------|------|
| ObjectType CRUD | `routers/ontology.py` | `meta_object_type` 表 + `/v1/ontology/object-types` API |
| Object 实例 CRUD | `routers/ontology.py` | `obj_instance` 表 + `/v1/objects/{type}` API (GET 列表/详情) |
| Object Set 查询 | `routers/object_sets.py` | `POST /v1/object-sets/query` 支持 filters/分页 |
| LinkType CRUD | `routers/ontology.py` | `meta_link_type` 表 + graph_edge 邻接表 |
| Action Type CRUD | `routers/actions.py` | `meta_action_type` 表 + `/v1/actions/types` API |
| Action 执行 | `routers/runtime_write.py` | `POST /v1/actions/execute` → Draft 审批写回 |
| 种子注入 | `db.py` `seed_if_empty()` | 启动时自动注入种子 |
| Action 插件 | `plugins/actions/*/manifest.json` | 磁盘插件 + `action_template_registry.py` 自动扫描注册 |

**结论**：现有后端 100% 覆盖 Phase C+ 需求。工作全部集中在**种子数据 + Action 插件 manifest + 前端 React**。

## 三、实施策略：3 批

| 批次 | 内容 | 文件 |
|------|------|------|
| **C+-1** | Order/OrderItem ObjectType 定义 + 种子数据（20 条订单）+ LinkType + 3 个 Action 插件 manifest + 测试 | `order_seed.py`, `plugins/actions/*/manifest.json`, `test_phase_cp_orders.py` |
| **C+-2** | 前端 OrderManagementPage.tsx — 对齐视觉稿 | `apps/web/src/pages/s2/OrderManagementPage.tsx` |
| **C+-3** | nav.ts 注册 + routes.tsx 路由 | `nav.ts`, `routes.tsx` |

## 四、C+-1 详细方案

### Order ObjectType 定义（properties JSONB 数组）

```python
_ORDER_PROPS = json.dumps([
    {"name": "order_no", "type": "string"},
    {"name": "customer_id", "type": "string"},
    {"name": "customer_name", "type": "string"},
    {"name": "order_date", "type": "string"},
    {"name": "total_amount", "type": "number"},
    {"name": "status", "type": "string"},  # pending/paid/shipped/delivered/cancelled/refunded
    {"name": "shipping_address", "type": "string"},
    {"name": "items", "type": "json"},     # JSONB 数组
    {"name": "tracking_no", "type": "string"},
    {"name": "remark", "type": "string"},
])
```

### 种子数据 20 条订单

覆盖 6 种状态（pending/paid/shipped/delivered/cancelled/refunded），客户名使用中文，金额 76~5880 元。

### 3 个 Action 插件（manifest.json + inproc runtime）

- `confirm-shipment`: status→shipped + 记录 tracking_no
- `cancel-order`: status→cancelled + 记录 remark
- `refund-order`: status→refunded + 记录退款金额

## 五、C+-2 前端方案

`OrderManagementPage.tsx` 对齐视觉稿 `workshop-app-order.html`：

- **统计卡片行**：4 张 stat card（总订单 / 待处理 / 已完成 / 总收入）
- **订单列表表格**：订单号 / 客户 / 日期 / 金额 / 状态徽章
- **状态筛选 Tab**：全部 / 待付款 / 已付款 / 已发货 / 已签收 / 已取消 / 已退款
- **搜索框**：按订单号 / 客户名搜索
- **订单详情侧栏**：选中行 → 展开详情面板 + 3 个 Action 按钮
- **趋势图**：近 7 天折线图（SVG 内联）
- 数据源：`GET /v1/objects/Order` + `POST /v1/object-sets/query`

## 六、验收标准

- [x] 订单列表 API 支持分页 + 状态筛选 + 搜索
- [x] 订单详情 API 可展开 OrderItem 子对象
- [x] 3 个 Action（发货/取消/退款）可正常执行并修改订单状态
- [x] 订单管理页面与视觉稿 `workshop-app-order.html` 对齐
- [x] 列表表格状态徽章颜色正确（待付款灰/已付款蓝/已发货黄/已签收绿/已取消红/已退款紫）
- [x] nav.ts 侧边栏「工作台 → 订单管理」可点击进入
- [x] 11 个单元测试全部 PASS

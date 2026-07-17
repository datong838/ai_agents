# 06a · Ontology Mapping 产品设计线框图

## Ontology Manager · Funnel Pipeline · OKF 映射器

> **文档性质**：`[06 产品方案](06-语义本体Ontology-Mapping产品方案.md)` 的 **UI/UX 线框规格** · 研发可直接对照实现  
> **版本**：v1.2 · 2026-07-14  
> **v1.2**：WF-OM-05/06 对齐 06b Criteria / Side Effects / 类型安全  
> **v1.1**：链 [HTML Demo v1.2](foundry/html/ontology.html)（OM-01~08 · 旅程 E）  
> **绘制原则**：布局对齐官方 OMA / Funnel；镜像补爬 `scrape_foundry_docs.py --ontology`  
> **对标在线**：[Ontology Overview](https://www.palantir.com/docs/foundry/ontology/overview) · [Ontology Manager](https://www.palantir.com/docs/foundry/ontology-manager/overview) · [Object Indexing / Funnel](https://www.palantir.com/docs/foundry/object-indexing/overview)  
> **关联**：[05a WF-FN-01](05a-数据集成Connectors-Pipeline-Dataset产品设计线框图.md) · [03 PRD §3.2](03-对标Palantir-AOS-PRD框架.md) · [HTML Demo](foundry/html/README.md)

---

## 使用的 Rules


| Rule     | 应用                                               |
| -------- | ------------------------------------------------ |
| 中文       | 线框内按钮、标签、Tab 一律中文                                |
| 先方案后代码   | 仅文档；不改业务代码                                       |
| 优先官方 UI  | OMA 六视图 · Overview 7 Tab · Funnel 四节点纵向流水线       |
| 通用线框     | 占位符 `{Object Type}` `{Property}` `{Dataset RID}` |
| 覆盖 06 节点 | 映射 §11 Backlog · §9 OMA 布局 · §5 Funnel 四阶段       |


---

## 1. 信息架构（IA）

### 1.1 应用地图 · L2 层

```text
┌─ Foundry 工作区 ─────────────────────────────────────────────────────────────┐
│  [≡ 应用门户]  工作区 ▾   🔍 搜索   [通知]  [用户]                              │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  本体（Ontology）  基座应用群                                                  │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐                │
│  │ Ontology Manager│ │ Pipeline Builder│ │ 搭建 / Builds   │                │
│  │ (OMA)           │ │ Native 映射入口 │ │ Funnel Job 监控 │                │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘                │
│                                                                               │
│  谛听增强（06 §6 · 05 §2.4）                                                   │
│  ┌─────────────────┐                                                          │
│  │ OKF Funnel 映射器 │  ← Curated Dataset → Property 自动映射 + Lint          │
│  └─────────────────┘                                                          │
└───────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 页面对照表（06 §11 → 本文线框）


| 06 ID | 线框 ID        | 应用                   | 对标官方                   |
| ----- | ------------ | -------------------- | ---------------------- |
| OM-01 | **WF-OM-01** | Discover 首页          | Discover 视图            |
| OM-02 | **WF-OM-02** | Object Type Overview | Object type 视图 · 7 Tab |
| OM-03 | **WF-OM-03** | Property Editor      | Property editor 视图     |
| OM-04 | **WF-OM-04** | Link Type 编辑器        | Link type 视图           |
| OM-05 | **WF-OM-05** | Action Type 编辑器      | Action type 视图         |
| OM-06 | **WF-OM-06** | Function Type 编辑器    | Function type 视图       |
| OM-07 | **WF-OM-07** | Funnel Pipeline 状态   | Data/Datasources Tab   |
| OM-08 | **WF-OM-08** | Branch / 版本          | Ontology branching     |
| OM-09 | **WF-OM-09** | 图谱健康度              | 悬空 Link · 冲突 · 僵尸 · 规则 · 归档候选 |
| —     | **WF-FN-01** | OKF Funnel 映射器       | 05a · 谛听增强             |


### 1.3 OMA 全局壳（Shell）

> 持久化：**左侧边栏** + **顶栏搜索** · 对标 OMA 整体布局

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ [☰]  本体管理器          🔍 搜索 Object / Link / Action…    🔔  👤 用户 ▾    │
├──────────┬───────────────────────────────────────────────────────────────────┤
│ 侧栏     │  面包屑：本体 / {Object Type 名称} / {Tab 或子页}                    │
│          ├───────────────────────────────────────────────────────────────────┤
│ Discover │                                                                   │
│ ─────    │                    <<  主内容区  >>                                 │
│ Object   │                                                                   │
│  types   │                                                                   │
│  └ {树}  │                                                                   │
│ Links    │                                                                   │
│ Actions  │                                                                   │
│ Functions│                                                                   │
│ ─────    │                                                                   │
│ 分支     │                                                                   │
│  └ master│                                                                   │
└──────────┴───────────────────────────────────────────────────────────────────┘
```

**共用控件**：Object Type 树 · RID · 分支选择器 `[分支: master ▾]` · `[+ 新建]` · 状态徽章（Indexed / Error / Schema drift）

---

## 2. 线框图例


| 符号       | 含义                |
| -------- | ----------------- |
| `[ 按钮 ]` | 可点击按钮             |
| `{占位符}`  | 动态字段              |
| `▾`      | 下拉                |
| `● / ○`  | Tab 选中 / 未选       |
| `🔵`     | 平台共用能力（Funnel 托管） |
| `🟣`     | 谛听 OKF 增强         |


---

## 3. WF-OM-01 · Discover 首页

**路由**：`/ontology`  
**用户目标**：快速进入常用 Object · 发现最近变更

```text
┌─ Ontology Manager · Discover ────────────────────────────────────────────────┐
│  🔍 搜索 Object types…                                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│  ⭐ 收藏                                                                      │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                          │
│  │ {Order}      │ │ {Customer}   │ │ {Device}     │                          │
│  │ 12.4k 实例   │ │ 8.1k 实例    │ │ 342 实例     │                          │
│  └──────────────┘ └──────────────┘ └──────────────┘                          │
│                                                                               │
│  🕐 最近查看                                                                  │
│  · {Order} · 2 分钟前   · {Link: Order→Customer} · 1 小时前                   │
│                                                                               │
│  📌 重要 / 最近修改（新人引导）                                                │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │ {Object Type}  │ 修改人 │ 修改时间 │ Funnel 状态 │ [打开 Overview]       │ │
│  │ Order          │ 张三   │ 10:32    │ ✅ Indexed  │ [打开]                │ │
│  │ Device         │ 李四   │ 昨天     │ ⚠ Error     │ [打开]                │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. WF-OM-02 · Object Type Overview

**路由**：`/ontology/object-types/:rid`  
**用户目标**：一屏掌握 Object 元数据 · 跳转 Properties / Funnel 状态

```text
┌─ Ontology Manager: {Order} ──────────────────────────────────────────────────┐
│  ← 返回 Discover   [🔍]  [+ 新建 Property]  [分支: master ▾]  [保存]         │
├──────────────────────────────────────────────────────────────────────────────┤
│ [Overview●] [Properties] [Action types] [Link type graph]                     │
│ [Dependents] [Data] [Usage]                                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│ ① Metadata                                                                    │
│ ┌──────────────────────────────────────────────────────────────────────────┐ │
│ │ 图标 [📦]  显示名: 订单   API: order   RID: ri.ontology.main.order        │ │
│ │ Title Key: order_no   Primary Key: order_id   Storage: OSv2 ✅            │ │
│ │ 状态: [Indexed]  最后水合: 2026-07-13 10:45:02                            │ │
│ └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│ ② Properties（摘要 · 完整列表见 Properties Tab）                              │
│ ┌──────────────────┬──────────┬─────────────────┬──────────┐               │
│ │ Property         │ 类型     │ Backing Column  │ Title?   │               │
│ │ order_id         │ String   │ order_id        │          │               │
│ │ order_no         │ String   │ order_no        │ ★        │               │
│ │ amount           │ Double   │ amount          │          │               │
│ └──────────────────┴──────────┴─────────────────┴──────────┘               │
│ [查看全部 Properties →]                                                        │
│                                                                               │
│ ③ Action types          ④ Link type graph                                     │
│ · 取消订单              Order ──places──► Customer                             │
│ · 派单维修              Order ──contains──► OrderItem                          │
│                                                                               │
│ ⑤ Dependents              ⑥ Data（摘要）                                       │
│ · Workshop: 订单看板      Backing: curated_orders [Dataset RID]               │
│ · Pipeline: order_sync    Funnel: Live ✅ · [查看 Pipeline 详情 →]            │
│                                                                               │
│ ⑦ Usage（30 天）                                                              │
│ 读: 12.4M  写(Action): 842  活跃用户: 23                                      │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. WF-OM-03 · Property Editor

**路由**：嵌 OM-02 · `/ontology/object-types/:rid/properties/:propId`  
**用户目标**：配置 backing column · title key · 时间序列属性

```text
┌─ Property: {amount} ─────────────────────────────────────────────────────────┐
│  ← 返回 Overview                                                                │
├──────────────────────────────────────────────────────────────────────────────┤
│  基本信息                                                                       │
│  显示名: [订单金额________]   API 名: [amount________]   类型: [Double ▾]       │
│                                                                               │
│  数据绑定（Funnel Mapping）                                                    │
│  Backing Dataset: curated_orders (只读 · 在 Data Tab 修改)                     │
│  Backing Column:  [amount ▾]     ☐ 设为 Title Key     ☐ 设为 Primary Key       │
│                                                                               │
│  时间序列（可选 · TSP）                                                         │
│  ☐ 启用时间序列属性   时间列: [event_time ▾]   聚合: [最新值 ▾]                 │
│                                                                               │
│  校验预览 🟣 OKF                                                                │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │ ✅ L1 列 amount (double) ↔ L2 Property Double 类型一致                    │ │
│  │ ⚠ 样本 3 行含 "N/A" — Funnel 将丢弃并记入 Data Health                    │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│  [取消]  [保存 Property]                                                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. WF-OM-04 · Link Type 编辑器

**路由**：嵌 OM-02  
**用户目标**：定义左/右 Object · 基数 · FK 映射

```text
┌─ Link Type: {Order → Customer} ──────────────────────────────────────────────┐
│  ← 返回 Overview                                                                │
├──────────────────────────────────────────────────────────────────────────────┤
│  左 Object (From)     [Order ▾]          右 Object (To)    [Customer ▾]        │
│  基数:  ○ 1:1  ● N:1  ○ N:M                                                   │
│                                                                               │
│  外键映射                                                                       │
│  Order Property [customer_id ▾]  ──►  Customer Primary Key [customer_id ▾]   │
│                                                                               │
│  关系图预览                                                                     │
│      [Customer] ◄──── places ──── [Order]                                      │
│                                                                               │
│  [取消]  [保存 Link]                                                           │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. WF-OM-05 · Action Type 编辑器

**路由**：嵌 OM-02  
**用户目标**：配置 Action Logic · **Submission Criteria** · **Side Effects** · Observability  
**对齐**：[06b ACT-SPEC](06b-Action与Function产品设计.md)

```text
┌─ Action Type: {审核订单} ──────────────────────────────────────────────────────┐
│  [Overview●] [Logic] [Criteria] [Side Effects] [Observability]               │
├──────────────────────────────────────────────────────────────────────────────┤
│  Overview                                                                     │
│  绑定 Object: Order   权限: order:approve   写回: writeback_orders Dataset     │
│  壳核: Logic → Function calculate_tax                                         │
│                                                                               │
│  Logic Tab                                                                    │
│  ┌─ 参数 ─────────────────────────────────────────────────────────────────┐  │
│  │ tax_exempt (Boolean)   note (String, 可选)                              │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│  [调用 Function: calculate_tax →]                                             │
│                                                                               │
│  Criteria Tab（官方：提交标准 / Submission Criteria）★ ACT-02                   │
│  · 当前用户 ∈ 财务组                                                           │
│  · amount > 0                                                                 │
│  · （类比）验收单附件非空才允许「已完成」                                         │
│                                                                               │
│  Side Effects Tab ★ ACT-04                                                    │
│  · Notification: 邮件 → 风控组                                                 │
│  · Webhook: 外部系统 API                                                       │
│                                                                               │
│  Observability · 乐观 UI                                                      │
│  前端先改态；失败回滚 · 近 30 天调用 / 失败率                                    │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. WF-OM-06 · Function Type 编辑器

**路由**：嵌 OM-02  
**用户目标**：类型安全配置 · Code Repo · 被 Action 引用  
**对齐**：[06b FUNC-SPEC](06b-Action与Function产品设计.md)

```text
┌─ Function Type: {calculate_tax} ───────────────────────────────────────────────┐
│  [Overview●] [Configuration] [Observability] [Usage History]                  │
├──────────────────────────────────────────────────────────────────────────────┤
│  Overview                                                                     │
│  输入: Order.amount (Double)   输出: Double                                    │
│  Schema→TS 接口 · 保存时类型校验 ★ FUNC-01                                     │
│  Ontology 只读 · 超时 60s ★ FUNC-02/03                                        │
│  被引用: Action「审核订单」                                                     │
│  [打开 Code Repository →]                                                     │
│                                                                               │
│  Configuration                                                                │
│  运行时: Foundry Functions (TS) · 沙箱 · 无 UI                                 │
│  ⚠ TS Function 不直接调外部 HTTP；写/通知走 Action Webhook ★ C-10            │
│                                                                               │
│  Usage History（近 7 天）                                                       │
│  ┌────────────┬──────────┬─────────┐                                          │
│  │ 日期       │ 调用次数 │ P99 延迟│                                          │
│  │ 07-14      │ 4,201    │ 12ms    │                                          │
│  └────────────┴──────────┴─────────┘                                          │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. WF-OM-07 · Funnel Pipeline 状态（Data / Datasources Tab）

**路由**：OM-02 → `[Data]` Tab → Datasources  
**用户目标**：监控四阶段进度 · Live/Replacement · 报错定位

```text
┌─ Data · Datasources: {Order} ────────────────────────────────────────────────┐
│  [Datasources●] [Schema] [Edits]                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  Backing Dataset: curated_orders   RID: ri.foundry.main.dataset.xxx           │
│  Primary Key Column: order_id   [更换 backing → 触发 Replacement Pipeline]    │
│                                                                               │
│  管道类型:  ● Live pipeline   ○ Replacement pipeline (后台重建中 67%)         │
│                                                                               │
│  Funnel Batch Pipeline 🔵                                                       │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │ ① Changelog      ✅ 完成   Txn #891 · 12,042 rows · 2m 14s               │ │
│  │       ↓                                                                  │ │
│  │ ② Merge Changes  ✅ 完成   + 用户编辑 6h 周期 · 847 edits merged         │ │
│  │       ↓                                                                  │ │
│  │ ③ Indexing       🔄 进行中  分片 3/8 · Object DB shard-02                │ │
│  │       ↓                                                                  │ │
│  │ ④ Hydration      ⏳ 等待     index → OSv2 search nodes                   │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│  最近错误                                                                       │
│  ⚠ 2026-07-13 09:12  Type Coherence: row pk=ORD-9921 amount="N/A" → 已丢弃    │
│  [查看完整日志 → Builds]   [重新运行 Replacement]                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. WF-OM-08 · Branch / 版本

**路由**：`/ontology/branches`  
**用户目标**：Object Type 分支开发与合并 · 对齐 Dataset 分支

```text
┌─ Ontology Branches ──────────────────────────────────────────────────────────┐
│  [+ 新建分支]   当前: master ▾                                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│  分支名          │ 基于     │ Object 变更数 │ 状态      │ 操作                │
│  master          │ —        │ —             │ 生产      │ —                   │
│  feature/order-v2│ master   │ 3 Object types│ 开发中    │ [合并] [对比]       │
│                                                                               │
│  与 L1 Dataset 分支对齐提示                                                    │
│  ⚠ feature/order-v2 的 backing dataset 在分支 dev-orders · 建议同步合并       │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 11. WF-FN-01 · OKF Funnel 映射器（增强）

> 完整线框见 **[05a §10 WF-FN-01](05a-数据集成Connectors-Pipeline-Dataset产品设计线框图.md)** · 本节为 L2 入口摘要

**路由**：`/okf-funnel` 或从 OM-02 Data Tab `[OKF 自动映射]` 跳入  
**用户目标**：Column → Property 自动推荐 · Lint · 一键 Publish 到 OM

```text
┌─ OKF Funnel 映射器 🟣 ───────────────────────────────────────────────────────┐
│  输入 Dataset: [curated_orders ▾]   目标 Object: [Order ▾] 或 [+ 新建]       │
├──────────────────────────────────────────────────────────────────────────────┤
│  L1 Column          建议 Property      置信度    类型      操作               │
│  order_id           order_id (PK)      98%       String    ☑                  │
│  order_no           order_no (Title)   95%       String    ☑                  │
│  amt                amount             82%       Double    ☑  [修正列名]       │
│  user_id            customer_id (Link) 76%       String    ☐  [改为 Link]      │
│                                                                               │
│  Lint: ✅ PK 唯一  ⚠ 2 列未映射  ❌ amount 样本含非数值                          │
│  Constitution: ✅ 语义契约  ✅ 推理边界  ⚠ 伦理护栏（FinancialRecord 须 HITL）   │
│  [导出映射 JSON]  [Publish 到 Ontology Manager →]                             │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 11b. WF-OM-09 · 图谱健康度（对齐 25）

**路由**：`/ontology/graph-health` · Demo：`ontology-graph-health.html`  
**用户目标**：扫描 GH-01～04；与 L1 `health.html` 分责；展示 TTL 归档候选（P2）

```text
┌─ 图谱健康度 ─────────────────────────────────────────────────────────────────┐
│  悬空 Link 12 · 属性冲突 3 · 孤立 Object 47 · 规则冲突 1 · 归档候选 8           │
│  [仅严重] [导出]   链 → L1 数据健康（连通/新鲜度）                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  GH-01 悬空  Batch→Equipment#E-99  目标不存在  [开 Draft 修复]                 │
│  GH-02 冲突  Order#8842.amount  L1A=120 / L1B=118  [看 Merge 策略]            │
│  GH-03 僵尸  Insight#…  91 天无访问  [加入归档候选]                             │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 12. 用户旅程线框串联

### 12.1 旅程 E · 标准水合（对照 06 §12.1）

```text
WF-FN-01 OKF 映射  →  WF-OM-02 Overview 确认  →  WF-OM-07 Funnel 四阶段  →  Workshop
     ↑                      ↑                           ↑
  05 curated_orders    Publish Property            Live pipeline ✅
```

### 12.2 旅程 F · PB Native

```text
WF-PB-02 画布 Ontology 输出节点  →  部署  →  WF-OM-07 自动挂 backing  →  Hydration
```

### 12.3 旅程 G · Action 闭环

```text
Workshop Action  →  写回 L1 Dataset  →  WF-OM-07 Changelog 触发  →  Object 属性更新
```

---

## 13. 组件清单（研发）


| 组件 ID             | 名称                 | 出现页面        | 说明                              |
| ----------------- | ------------------ | ----------- | ------------------------------- |
| CMP-OM-TABS       | Overview 7 Tab 栏   | OM-02       | Overview/Properties/…/Usage     |
| CMP-FUNNEL-PIPE   | 四阶段纵向流水线           | OM-07       | Changelog→Merge→Index→Hydration |
| CMP-LINK-GRAPH    | Link 关系图           | OM-02/04    | 可点击跳转 Link Editor               |
| CMP-PROP-MAP      | Column↔Property 表格 | OM-03/FN-01 | 含类型 Lint 徽章                     |
| CMP-BRANCH-PICKER | 分支选择器              | Shell/OM-08 | 与 Dataset 分支联动提示                |
| CMP-FUNNEL-STATUS | Indexed/Error 徽章   | OM-01/02/07 | 来自 Builds Job 状态                |


---

## 14. 变更记录


| 版本   | 日期         | 变更                                             |
| ---- | ---------- | ---------------------------------------------- |
| v1.0 | 2026-07-13 | 初稿：WF-OM-01~08 · WF-FN-01 摘要 · 旅程 E/F/G · 组件清单 |
| v1.1 | 2026-07-14 | HTML Demo 落地对照 · 链 foundry/html/ontology*.html |
| v1.2 | 2026-07-14 | WF-OM-05/06 按 06b 增强 Submission Criteria / 壳核 |
| v1.3 | 2026-07-17 | WF-OM-09 图谱健康；FN-01 Constitution；对齐 [25](20_tech/25-LLM-Wiki启示与L2演进补丁.md) |


---

*v1.0 · docs/palantier/06a · L2 Ontology Manager + Funnel 线框*
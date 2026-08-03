# 223-deep-checklist-3 — 详情页/弹出页深度检查（9 页）

> 版本：v1.1（2026-07-29 功能完整度复审）
> 原生成：2026-07-26
> 范围：不在侧栏的 9 个二级详情页/弹出页（从一级页面点击进入）
> 检查标准：每页 7 项 — 页面结构 / 组件盘点 / 数据驱动 / 交互 / 主题样式 / 系统现状 / 风险依赖
> 配套：[`223-deep-checklist.md`](./223-deep-checklist.md) §1.1 · [`223-deep-checklist-2.md`](./223-deep-checklist-2.md) · [`227-未完成项补齐计划.md`](./227-未完成项补齐计划.md)

---

## 总览（2026-07-29 最新）

| # | 页面 | 视觉稿 | React 实现 | 路由 | 旧% | **现%** | 工作量(剩) |
|---|------|--------|-----------|------|-----|--------|-----------|
| 1 | 对象类型详情 | `../foundry/html/ontology-object.html` | `ObjectTypeDetailPage.tsx` + `objectTypeDetail.tsx` | `/ontology/object-types/:typeId` | ~65 | **65** | M |
| 2 | 链接类型详情 | `../foundry/html/ontology-link.html` | `LinkTypeEditorPage.tsx` | `/ontology/link-types/:linkId` | ~35 | **50** | L |
| 3 | Action 详情 | `../foundry/html/ontology-action.html` | `ActionTypeEditorPage.tsx` | `/ontology/action-types/:actionId` | ~40 | **55** | L |
| 4 | 属性类型详情 | `../foundry/html/ontology-property.html` | `PropertyEditorPage.tsx` | `/ontology/properties/:typeId` | 0（误） | **50** | M–L |
| 5 | Function 详情 | `../foundry/html/ontology-function.html` | `FunctionEditorPage.tsx` | `/ontology/functions` | 0（误） | **45** | M |
| 6 | Wiki 详情 | `../foundry/html/ontology-wiki.html` | `WikiDetailPage.tsx` | `/ontology/wiki/:wikiId` | ~20 / 0 | **35** | XL |
| 7 | Wiki 差异 | `../foundry/html/ontology-wiki-diff.html` | `WikiDiffPage.tsx` | `/ontology/wiki/:wikiId/diff` | 0（误） | **40** | M |
| 8 | 管道详情（画布） | `../foundry/html/pipeline.html` | `pipelineCanvas.tsx` | `/data/pipelines/:pipelineId` | ~45 | **55** | L |
| 9 | 数据源详情 | `../foundry/html/source-detail.html` | `sourceDetailPage.tsx` | `/data/sources/:sourceId` | ~35 | **50** | L |

**关键变化（相对 07-26）**：#4/#5/#6/#7 **均已有路由与页面**，不再是「从零新建」；剩余工作是视觉保真 + API 闭环。
**合计剩余工作量估算：约 18–30 人天**（低于旧估 26–42，因页面已存在）。

### 阅读说明

- 下文各页「🔴 缺失」叙述若仍出现，**以本总览现% 为准**。
- 详细组件差距清单仍可用于改造；排期见 227 计划。

---

## 建议实施顺序（复审后）

| 优先级 | 页面 | 理由 |
|--------|------|------|
| **P0** | #6 Wiki 详情 | 现%最低且视觉差距最大（非完整富文本） |
| **P0** | #1 对象类型详情 | 已有基础，补链接图+元数据即可抬高体验 |
| **P1** | #8 管道详情画布 | DAG 变换/历史未满 |
| **P1** | #9 数据源详情 | ER/Schema 树相对视觉仍弱 |
| **P1** | #4 属性类型详情 | 页已有，对齐双栏+列映射 |
| **P1** | #2/#3 链接·Action | CRUD 有，补可视化与布局 |
| **P2** | #7 Wiki 差异 | 依赖版本 API |
| **P2** | #5 Function 详情 | 列表+编辑器有，对齐视觉即可 |

---

## 详细检查报告

> 以下章节保留 07-26 组件级差距；每节开头已加 **现完整度** 标注。

---

### 页面 1: 对象类型详情 (`ontology-object`)

> **现完整度（2026-07-29）：65%** · `/ontology/object-types/:typeId` ✅

**视觉稿**: `foundry/html/ontology-object.html`
**React**: `ObjectTypeDetailPage.tsx` (176行) + `objectTypeDetail.tsx` (700行)
**路由**: `/ontology/object-types/:typeId` ✅ 已注册

#### 1. 页面结构检查

| 维度 | 视觉稿 | 系统 | 差距 |
|------|--------|------|------|
| 布局 | 左导航+右卡片纵向流（双栏） | 7-Tab 切换 | 模式不同 |
| 顶部 | 面包屑 + `Indexed`/`12,847 实例` 徽章 + "Object Explorer 打开"/"编辑"按钮 | BpToolbar（返回+分支选择+LLM Wiki+Funnel） | 缺面包屑、实例徽章 |
| 主内容 | 6 个卡片纵向排列（元数据/属性/操作/链接图/数据/使用） | 7 Tab 分页（Overview/Properties/Actions/Links/Dependents/Data/Usage） | 信息组织方式不同 |
| 左栏 | PAGES 导航（Overview/Data/Usage）+ RELATED 链接（属性12/操作5/链接3/函数2） | 无左栏 | 缺左栏导航 |
| 底部 | 无 | 无 | — |

#### 2. 组件级盘点

| 组件 | 视觉稿 | 系统 | 需新建/改造 |
|------|--------|------|------------|
| 元数据网格（12 项 KV） | RID/API名/PK/TitleKey/显示名/plural/BackingDataset/Sync策略/存储类型/创建人/分支/可见性 | `BpPropGrid` 仅 5 项 | **改造**：扩展到 12 项 |
| 属性表格（8行5列） | 属性名/类型/必填/可搜索/显示名 | Properties Tab 内 input 表单（name+type 两列） | **改造**：表格化 + 补 3 列 |
| 操作类型表格（5行3列） | 操作名/类型徽章(Create/Modify/Delete/Action)/说明 | Actions Tab 内 card-list（仅 name+id） | **改造**：补类型徽章+说明 |
| 链接类型可视化图 | 中央 Order 节点 + 3 条边连到 Customer/OrderItem/Shipment，基数标签 1:N | `<pre>` 纯文本 ASCII 图 | **新建**：节点+连线图组件 |
| 数据信息列表 | BackingDataset/实例数/最近同步/数据质量99.6%/异常监控 | Data Tab 内 BpBanner + 实例列表 | **改造**：补数据质量+异常监控 |
| 使用统计表格 | 应用/类型/最近访问 | Usage Tab 用 BpScoreGrid + BpMetricGrid | **改造**：补具体应用列表表 |
| 多色 Badge | green/gray/amber/red/blue | bp-tag ok/warn 两种色 | **新建**：多色 Badge |

#### 3. 数据驱动检查

**视觉稿数据**: RID `ri.ontology.main.object-type.order`、12 属性、5 操作、3 链接、12847 实例、数据质量 99.6%

**当前 API**:
- `GET /v1/ontology/object-types` — OT 列表
- `getOntologyClient().listObjects(typeId, {branch})` — 实例列表
- `GET /v1/funnel/${typeId}/status` — Funnel 状态
- `GET /v1/ontology/link-types` / `GET /v1/actions/types` — 链接/操作

**缺失 API**:
- `GET /v1/ontology/object-types/:typeId` — 单 OT 详情（含 PK/TitleKey/BackingDataset/Sync策略/可见性）
- `GET /v1/ontology/object-types/:typeId/data-quality` — 数据质量指标
- `GET /v1/ontology/object-types/:typeId/usage` — 使用统计

**缺失字段**: `primary_key_field`, `title_key`, `backing_dataset`, `sync_strategy`, `storage_type`, `visibility_markings`, `display_name_plural`

#### 4. 交互检查

| 交互 | 视觉稿 | 系统 | 缺失 |
|------|--------|------|------|
| Discard / Save to branch | 有 | 有 Save，无 Discard | 缺 Discard |
| 左栏 PAGES 导航切换 | 有 | Tab 导航替代 | 功能等价 |
| "+ 添加属性"/"+ 添加操作" | 有 | 有 | ✅ |
| "在 Object Explorer 打开" | 有 | 无 | **缺失** |
| 函数入口（RELATED 函数2） | 有 | 无 | **缺失** |

#### 5. 主题与样式检查

- 视觉稿：浅色主题，`p-card` 卡片式带圆角和边框，`p-mono` 等宽字体用于 RID/字段名，`p-meta-grid` 3-4 列网格
- 系统：暗色主题（`--aos-surface`, `--aos-border`, `--aos-accent`），无卡片圆角
- 差距：布局模式+主题体系不同，系统处于开发中可大改

#### 6. 系统现状对比

**完整度: ~65%**

核心差距 Top 5:
1. 布局模式差异：左导航+右卡片 vs 7-Tab → 需重构 Overview 布局
2. 链接图可视化缺失：ASCII 文本 → 需新建图组件
3. 元数据字段缺失 7 项 → 需后端 API 扩展
4. 属性/操作表格列不完整 → 需前端补列
5. 函数 Tab 缺失 → 需新建

**工作量: M (1-2 天)** | **优先级: P1**

#### 7. 风险与依赖

- 技术风险：链接图可视化需引入图渲染库（reactflow/d3）或 SVG 手绘
- 后端依赖：`GET /v1/ontology/object-types/:typeId` 需扩展返回完整元数据
- 数据依赖：种子数据需含 PK/TitleKey/BackingDataset 等字段
- 导航入口：从本体管理页 OT 列表点击进入 ✅ 已就绪

---

### 页面 2: 链接类型详情 (`ontology-link`)

> **现完整度（2026-07-29）：50%** · `/ontology/link-types/:linkId` ✅

**视觉稿**: `foundry/html/ontology-link.html`
**React**: `LinkTypeEditorPage.tsx` (222行)
**路由**: `/ontology/link-types/:linkId` ✅ 已注册

#### 1. 页面结构检查

| 维度 | 视觉稿 | 系统 | 差距 |
|------|--------|------|------|
| 布局 | 左导航+右配置卡（双栏 `p-oma-type`） | 纯表单网格 `ont-form-grid` | **完全不同** |
| 左栏 | 返回 Link types + 类型名称 + 4 导航项（Overview/Security/Datasources/Usage） | 无 | **缺失** |
| 主内容 | 标题行 + 3 信息卡（Ontology/Status + ID/RID + Configuration）+ Properties 卡 | 8 input 字段 + 2 checkbox 表单 | **完全不同** |
| Configuration 区 | Join method 3 选卡片 + 可视化连线图 + 类型属性选择器两栏 | 无 | **缺失** |

#### 2. 组件级盘点

| 组件 | 视觉稿 | 系统 | 需新建/改造 |
|------|--------|------|------------|
| 左侧导航栏 | Overview/Security/Datasources/Usage | 无 | **新建** |
| Join method 卡片选择器 | Foreign key/Dataset/Object type 三选一 | 无 | **新建** |
| 可视化连线图 | 左右两列 icon + 中间 SVG 连线 | 无 | **新建** |
| Object type A/B 选择器 | 下拉 + PK 标注 + 互换按钮 | 无（手动 input srcType/dstType） | **新建** |
| Ontology/Status 信息卡 | Status 下拉（Active/Deprecated/Experimental） | 无 | **新建** |
| ID/RID 信息卡 | `p-mono` 等宽显示 | 无 | **新建** |
| Properties 卡 | 空态 "No properties defined" | 无 | **新建** |
| Cardinality 选择器 | 无 | 有（select 4 选项） | 系统多出 |

#### 3. 数据驱动检查

**视觉稿数据**: Aircraft ✈️ 🏢 Airline（Many-to-one）、Status=Active、Join=Foreign key、PK=Carrier Code/Code

**当前 API**: `GET/POST/PUT/DELETE /v1/ontology/link-types`

**缺失字段**: `joinMethod`, `foreignKeyFieldA`, `foreignKeyFieldB`, `status`, `rid`, `properties[]`

#### 4. 交互检查

| 交互 | 视觉稿 | 系统 | 缺失 |
|------|--------|------|------|
| Join method 三选一切换 | 有 | 无 | **缺失** |
| Object type A/B 下拉选择 | 有 | 无（手动 input） | **缺失** |
| A/B 互换按钮 | 有 | 无 | **缺失** |
| 标题旁编辑图标 | 有 | 无 | **缺失** |
| Actions 下拉按钮 | 有 | 无 | **缺失** |
| 删除 | 无 | 有（confirm 弹窗） | 系统多出 |
| expectedEdges 规模红线警告 | 无 | 有（>100k 时 warn） | 系统多出 |

#### 5. 主题与样式检查

- 视觉稿：浅色主题，`p-oma-type-card` 分区卡（header+body），`p-link-join-card` 选中态蓝色边框高亮，`p-link-row` 行式含 icon+select+badge
- 系统：暗色主题，`ont-form-grid` 表单网格
- 差距：整体视觉完全不同，系统可大改

#### 6. 系统现状对比

**完整度: ~35%**

核心差距 Top 5:
1. 布局完全不同 → 需完全重构
2. Join method 选择器缺失
3. 可视化连线图缺失
4. Object type 选择器缺失
5. 左侧导航栏缺失

**工作量: L (3-5 天)** | **优先级: P2**（CRUD 功能可用，视觉差距大但非阻塞）

#### 7. 风险与依赖

- 技术风险：Join method 切换影响后续配置 UI 联动逻辑
- 后端依赖：LinkType 模型需扩展 joinMethod/status/rid/properties
- 数据依赖：需 Aircraft-Airline 示例种子数据
- 导航入口：从 OT 详情页 Links Tab / 本体管理页 ✅ 已就绪

---

### 页面 3: Action 详情 (`ontology-action`)

> **现完整度（2026-07-29）：55%** · `/ontology/action-types/:actionId` ✅

**视觉稿**: `foundry/html/ontology-action.html`
**React**: `ActionTypeEditorPage.tsx` (285行)
**路由**: `/ontology/action-types/:actionId` ✅ 已注册

#### 1. 页面结构检查

| 维度 | 视觉稿 | 系统 | 差距 |
|------|--------|------|------|
| 布局 | 左导航 9 项 + 右多区域配置 | 纯表单网格 | **完全不同** |
| 左栏 | Overview/Rules/Parameters/User Interface/Capabilities/Security&Submission Criteria/Automations/History/Observability | 无 | **缺失** |
| 主内容 | 描述信息表 + Status/RID 右栏 + Action overview 卡（Input+Rules 双列）+ Dependents 卡 | 4 input + 3 JSON textarea | **完全不同** |
| Action overview | Input 列（3 参数）+ Rules 列（Modify/Create 操作+字段） | 无 | **缺失** |
| Dependents 卡 | 7 类依赖（Automation/Workshop/Dev Console/Object View/Process/Quiver/Use cases）含计数 | 无 | **缺失** |

#### 2. 组件级盘点

| 组件 | 视觉稿 | 系统 | 需新建/改造 |
|------|--------|------|------------|
| 左侧 9 项导航栏 | 有 | 无 | **新建** |
| 描述信息表 | Description/Tool desc/Contributors/Ontology/API name（含复制/编辑 icon） | 无（仅 name input） | **新建** |
| Status 下拉 | Experimental 等状态 | 无 | **新建** |
| RID 显示 | `ri.actions.main.action-type.e…` | 无 | **新建** |
| Action overview 可视化 | Input 列 + Rules 列（icon+描述+OT badge） | 无 | **新建** |
| 工具栏（搜索/缩放） | 有 | 无 | **新建** |
| Dependents 卡 | 7 类依赖 | 无 | **新建** |
| Parameters JSON 编辑器 | 无（可视化列表） | 有（textarea JSON） | 模式不同 |
| 试跑校验 | 无 | 有（payload+validate） | 系统多出 |
| Last edited 时间 | 有 | 无 | **新建** |

#### 3. 数据驱动检查

**视觉稿数据**: `Escalate Patient Care`、Input 3 参数（Patient/Care Recommendation/Escalation Reason）、Rules（Modify Patient + Create Alert）、Dependents（Automation 1 + Workshop 1）

**当前 API**: `GET/POST/PUT /v1/actions/types` + `POST /v1/actions/validate`

**缺失字段**: `description`, `toolDescription`, `contributors`, `status`, `rid`, `rules[]`, `dependents[]`

**缺失 API**: `GET /v1/actions/types/:id/dependents`

#### 4. 交互检查

| 交互 | 视觉稿 | 系统 | 缺失 |
|------|--------|------|------|
| 左侧 9 导航切换 | 有 | 无 | **缺失** |
| 标题编辑图标 | 有 | 无 | **缺失** |
| Actions/Open in 下拉 | 有 | 无 | **缺失** |
| API name 复制按钮 | 有 | 无 | **缺失** |
| Action overview 工具栏 | 有 | 无 | **缺失** |
| 试跑校验 | 无 | 有 | 系统多出 |
| 所属 OT 跳转 | 无 | 有 | 系统多出 |

#### 5. 主题与样式检查

- 视觉稿：浅色卡片式分区，`p-action-col` 双列（Input 左、Rules 右），`p-action-item-icon` + `p-action-item-body`
- 系统：暗色表单网格
- 特殊：Rule 项含 badge 标注 Object Type（[O1LV] Patient 等）

#### 6. 系统现状对比

**完整度: ~40%**

核心差距 Top 5:
1. 左侧 9 项导航栏缺失
2. Action overview 可视化（Input+Rules 双列）缺失
3. 描述信息表缺失（Description/Tool desc/Contributors/API name）
4. Dependents 卡缺失（7 类依赖）
5. Parameters 从 JSON textarea 改为可视化列表

**工作量: L (3-5 天)** | **优先级: P2**（试跑校验核心功能已实现）

#### 7. 风险与依赖

- 技术风险：Rules 可视化需解析 submissionCriteria 结构为 Modify/Create 操作+字段映射
- 后端依赖：ActionType 模型需扩展 description/rules/dependents
- 数据依赖：需 `Escalate Patient Care` 示例
- 导航入口：从 OT 详情页 Actions Tab ✅ 已就绪

---

### 页面 4: 属性类型详情 (`ontology-property`) — 🔴 需从零新建

> **现完整度（2026-07-29）：50%** · `/ontology/properties/:typeId` ✅ — **不再缺失**

**视觉稿**: `foundry/html/ontology-property.html`
**React**: 无（无路由无页面文件）

#### 1. 页面结构检查

**视觉稿结构**（三区域 `p-ped`）:
- **主区域**: 顶部标题行（"Properties" + "9 of 9 Columns mapped"）+ Tab（Properties 13 / Column mapping）+ 数据源控制条（Dataset 下拉 + "Show mapped columns" 开关 + Automap all 按钮 + 搜索/过滤）+ 左右分栏（属性表 + 属性详情面板）+ 底部数据预览表
- **左侧属性表**: 表头（全选 checkbox + Properties count + Create property + 搜索/过滤）+ 表格 8 行（checkbox + 属性名 icon badge + Status + Visibility + Base formatter + Column 映射）
- **右侧详情面板**: 属性名 + PK badge + 删除 + Tab（General/Display/Interaction/Details/Advanced）+ 表单（Name/Description/Base type 下拉/Allow multiple 开关/Value type/Status/Title key 开关/Primary key 开关）
- **底部数据预览**: Dataset 选择 + 6 行真实数据（id/airport/city/country/IATA/ICAO/latitude）

#### 2. 组件级盘点

需新建组件:

| 组件 | 说明 |
|------|------|
| `PropertyTable` | 属性列表表格（全选 checkbox + icon + Status/Visibility/Formatter/Column 列） |
| `PropertyDetailPanel` | 右侧详情面板（5 Tab: General/Display/Interaction/Details/Advanced） |
| `BaseTypeSelector` | Base type 下拉（Integer/String/Double/Boolean/Date/Timestamp/Geo） |
| `ToggleSwitch` | 自定义开关（Allow multiple / Title key / Primary key / Show mapped） |
| `ColumnMappingIndicator` | Column 映射显示（已映射=列名，未映射=`—`） |
| `DataPreviewTable` | 底部数据预览（列类型 + PK/Title 标注 + 真实数据行） |
| `DatasetSelector` | Dataset 下拉选择器 |
| `StatusBadge` | Experimental/Active/Deprecated 状态徽章 |

系统可复用: `BpTable`（通用表格）、`BpTabs`（Tab）、`BpToolbar`

#### 3. 数据驱动检查

**视觉稿数据**: OT=Order、Dataset=`orders_ontology_2`、13 属性（8 行可见：id Integer PK / ICAO String Title / Airport / City / Country / Geohash Geo / IATA）、底部预览 6 行真实数据

**需新建 API**:
| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/v1/ontology/object-types/:typeId/properties` | 属性列表（含 status/visibility/formatter/column） |
| POST | `/v1/ontology/object-types/:typeId/properties` | 创建属性 |
| PUT | `/v1/ontology/object-types/:typeId/properties/:propId` | 更新属性 |
| DELETE | `/v1/ontology/object-types/:typeId/properties/:propId` | 删除属性 |
| POST | `/v1/ontology/object-types/:typeId/properties/automap` | 自动映射所有列 |

**需新建数据库表**: `property` — id, object_type_id, name, base_type, description, status, visibility, base_formatter, allow_multiple, value_type, is_title_key, is_primary_key, mapped_column, display_name

**种子数据**: 13 个 Order 属性 + Airport 示例数据集

#### 4. 交互检查

- Tab 切换: Properties / Column mapping
- Dataset 下拉切换
- "Show mapped columns" 开关过滤
- Automap all 按钮（批量自动映射）
- 表格行 checkbox 全选/单选
- 点击属性行 → 右侧详情面板联动
- 详情面板 5 Tab 切换
- Base type 下拉选择
- Allow multiple / Title key / Primary key 开关
- 删除属性按钮

#### 5. 主题与样式检查

- 视觉稿：浅色三区域布局（左表格 + 右详情 + 底预览），紧凑表格（行高 ~36px），选中行蓝色边框，`p-ped-toggle` 自定义开关
- 系统差距：需全新实现

#### 6. 系统现状对比

**完整度: 0%** — 需从零新建

**工作量: XL (5-8 天)** — 7 个详情页中最复杂的，涉及属性 CRUD + 列映射 + 数据预览 + 多 Tab 详情面板

**优先级: P1**（属性管理是本体管理核心功能）

#### 7. 风险与依赖

- 技术风险：列映射逻辑复杂（属性↔数据集列的自动/手动映射）；数据预览需对接 Dataset API
- 后端依赖：Property 模型需新建完整 CRUD API
- 数据依赖：需种子数据含 13 个属性 + Airport 数据集
- 组件依赖：ToggleSwitch / BaseTypeSelector 等需新建
- 导航入口：从 OT 详情页属性表格点击属性名 → 路由需新建

---

### 页面 5: Function 详情 (`ontology-function`) — 🔴 需从零新建

> **现完整度（2026-07-29）：45%** · `/ontology/functions` ✅ — **不再缺失**

**视觉稿**: `foundry/html/ontology-function.html`
**React**: 无（无路由无页面文件）

#### 1. 页面结构检查

**视觉稿结构**（双栏 `p-oma-type` + 顶部只读提示条）:
- **只读提示条**: "Functions in the Ontology Manager are read-only. You can write and modify the function in the Code Repositories application." + "Open in Code Repositories" 链接
- **左栏**: 返回 Home + 函数名+紫色 `fx` 图标 + 版本号（`1.1.2 Latent`）+ 3 导航项（Overview/Configuration/Observability）
- **右栏**: 标题行（函数名+编辑图标+右栏 Visibility/Type/Published Date KV）+ 主信息卡（左: Name+Documentation，右: Implementation 含仓库链接+文件路径+Class Name）+ RID 行 + Code Preview 卡（行号语法高亮代码 + "Edit in Code Repositories" 链接）+ Inputs 卡（1 参数）+ Output type 卡（返回类型+Struct badge）

#### 2. 组件级盘点

需新建组件:

| 组件 | 说明 |
|------|------|
| `ReadOnlyNotice` | 顶部只读提示条（含跳转 Code Repositories 链接） |
| `FunctionSidebar` | 左侧导航（含版本号选择器） |
| `CodePreviewBlock` | 代码预览块（行号 + 语法高亮：keyword蓝色/class紫色/function绿色/string橙色/comment灰色/number橙色） |
| `FunctionParamList` | Inputs/Output 参数列表（icon+名称+类型 badge） |
| `ImplementationCard` | Implementation 信息卡（代码仓库链接+文件路径+Class Name） |

#### 3. 数据驱动检查

**视觉稿数据**: `getAgeBasedVitalThresholds` v1.1.2、TypeScript 代码（36-59行，含 `@Function()` 装饰器）、Inputs: patient（[O1LV] Patient）、Output: VitalThresholds（Struct）

**需新建 API**:
| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/v1/ontology/function-types/:funcId` | 函数详情（documentation/implementation/code/inputs/output） |
| GET | `/v1/ontology/function-types/:funcId/code` | 代码预览 |

**需新建数据库表**: `function_type` — id, name, version, visibility, type, published_date, documentation, repo_id, file_path, class_name, rid, code_preview, inputs[], output_type

#### 4. 交互检查

- "Open in Code Repositories" 链接
- "Edit in Code Repositories" 链接（Code Preview 卡内）
- 版本号下拉
- 左侧 3 导航项切换
- 代码预览块（只读）

#### 5. 主题与样式检查

- 代码语法高亮 CSS class: `.p-fn-kw`(蓝) / `.p-fn-cls`(紫) / `.p-fn-fn`(绿) / `.p-fn-str`(橙) / `.p-fn-com`(灰) / `.p-fn-num`(橙)
- Implementation 区用浅灰背景区分
- 只读提示条浅色背景 + info icon

#### 6. 系统现状对比

**完整度: 0%** — 需从零新建

**工作量: L (3-5 天)** | **优先级: P3**（只读页面，优先级最低）

#### 7. 风险与依赖

- 技术风险：代码语法高亮需集成渲染库（`prism-react-renderer` / `shiki`）或手动 CSS class
- 后端依赖：Function 模型需新建只读 API
- 数据依赖：需 `getAgeBasedVitalThresholds` 函数 + 代码仓库/文件路径种子
- 组件依赖：依赖 Code Repositories 页面（已有 `/data/code-repos`）
- 导航入口：从 OT 详情页 RELATED "函数(2)" — 但 OT 详情页当前无函数 Tab，需先补入口

---

### 页面 6: Wiki 详情 (`ontology-wiki`) — 需大幅改造

> **现完整度（2026-07-29）：35%** · `/ontology/wiki/:wikiId` ✅ — **不再缺失**；远低于视觉 Slate

**视觉稿**: `foundry/html/ontology-wiki.html` (794行，最复杂的视觉稿)
**React**: `ontology.tsx` 中 `WikiPage` 函数（line 334-696），路由 `/ontology/wiki`

#### 1. 页面结构检查

**视觉稿结构**（全屏 Slate 编辑器 `p-slate-app`）:
- **顶部栏**: 面包屑（COVID > 标题+星标）+ 4 Tab（文件/帮助/版本对比/Page 1 v9）+ 操作按钮
- **工具栏**: 3 模式切换（微件/工作流/预览）+ 9 Tab（仪表盘/查询/函数/对象/事件/数据/依赖/样式/变量）
- **主编辑区**: 三栏（左侧 Widget 树 + 中央画布 + 右侧属性面板）
- **Object Set 构建器覆盖层**: 对象集列表 + 筛选器 + 预览表
- **工作流模式覆盖层**: 左节点模板面板 + 中央画布（节点+SVG连线）+ 右节点属性配置
- **运行时预览覆盖层**: 变量解析 + 真实数据渲染

**React 实现结构**:
- `S2Chrome` 外壳（标题+描述）+ `BpToolbar`（刷新/保存并建 Draft/审批台/Agent 工具面板/返回本体管理）
- 4 Tab: 知识卡片 / 双向绑定 / Agent 读字段 / 版本
- 知识卡片 Tab: summary textarea + fields JSON textarea
- 保存逻辑: 通过 `createDraft` 提交 Draft

**差距**: 视觉稿是全屏 Slate 可视化编辑器（Widget 树+画布+属性面板+Object Set 构建器+工作流编排+运行时预览），系统是简单知识卡片表单编辑器。复杂度差距巨大。

#### 2. 组件级盘点

| 组件 | 视觉稿 | 系统 | 需新建/改造 |
|------|--------|------|------------|
| Slate 顶部栏 | 有 | 无 | **新建** |
| 模式切换（微件/工作流/预览） | 有（3 覆盖层切换） | 无 | **新建** |
| Widget 树（搜索+层级树+折叠+删除） | 有 | 无 | **新建** |
| 中央画布（Widget 预览渲染） | 有 | 无 | **新建** |
| 右侧属性面板（Widget 名称+Markdown/HTML 编辑） | 有 | 无 | **新建** |
| Object Set 构建器 | 有（对象集列表+筛选器+预览表） | 无 | **新建** |
| 工作流编排画布 | 有（节点模板+SVG 连线+属性配置） | 无 | **新建** |
| 运行时预览 | 有（变量解析+真实数据渲染） | 无 | **新建** |
| 知识卡片编辑 | 无 | 有（summary+fields） | 系统不同功能 |
| Draft 提交 | 无 | 有 | 系统有不同功能 |
| 版本 | 有（Page 1 v9） | 有（Tab"版本"） | 部分实现 |

#### 3. 数据驱动检查

**视觉稿数据**: COVID-19 Homepage Skeleton v9、Widget 树 5 级、Object Set（covid-patients 筛选 已康复=是）、工作流 4 节点（触发器→条件→动作→AIP Agent）、运行时 $user→李明

**当前 API**: `/v1/wiki/${objectType}/${objectId}` + `getOntologyClient().createDraft()`

**缺失 API**:
- `GET /v1/wiki/pages/:pageId` — 完整页面定义（Widget 树+属性+内容）
- `PUT /v1/wiki/pages/:pageId` — 保存
- `GET /v1/wiki/pages/:pageId/versions` — 版本列表
- `GET /v1/wiki/pages/:pageId/preview` — 运行时预览数据
- `POST /v1/ontology/object-sets/query` — Object Set 筛选查询

#### 4. 交互检查

| 交互 | 视觉稿 | 系统 | 缺失 |
|------|--------|------|------|
| 微件/工作流/预览三模式切换 | 有 | 无 | **缺失** |
| Widget 树展开/折叠/搜索/选择/删除 | 有 | 无 | **缺失** |
| Object Set 筛选器构建 | 有 | 无 | **缺失** |
| 工作流节点拖拽+连线 | 有 | 无 | **缺失** |
| 运行时变量解析预览 | 有 | 无 | **缺失** |
| 保存 | 有 | 有（Draft） | 模式不同 |

#### 5. 主题与样式检查

- 全屏 IDE 式布局（类似 Figma/VS Code），无 padding
- 工作流画布用点阵背景（`radial-gradient(#E5E7EB 1px, transparent 1px); background-size: 20px 20px`）
- 节点用彩色边框区分类型（黄=触发器、蓝=条件、绿=动作、紫=AIP Agent）
- 运行时预览用灰色顶栏（`#1F2937`）

#### 6. 系统现状对比

**完整度: ~20%**（仅知识卡片表单+Draft 提交）

核心差距 Top 5:
1. Slate 全屏编辑器完全缺失 — Widget 树+画布+属性面板三栏
2. Object Set 构建器缺失
3. 工作流编排画布缺失
4. 运行时预览缺失
5. 多模式切换缺失

**工作量: XXL (10-15 天)** | **优先级: P2**（建议分 3 期：先 Widget 树+画布，再 Object Set，再工作流）

#### 7. 风险与依赖

- 技术风险：Slate 编辑器需完整 Widget 拖拽+渲染引擎（`react-dnd`/`dnd-kit`）；工作流画布需 `reactflow`；运行时预览需服务端变量解析
- 后端依赖：Wiki 页面模型需完全重构
- 数据依赖：需 COVID-19 Homepage Skeleton 页面 + Widget 树定义 + Object Set 配置种子数据
- 组件依赖：依赖 Object Explorer（Object Set 选择器）
- 导航入口：从 Wiki 索引页点击 ✅ 已有路由

---

### 页面 7: Wiki 差异 (`ontology-wiki-diff`) — 🔴 需从零新建

> **现完整度（2026-07-29）：40%** · `/ontology/wiki/:wikiId/diff` ✅ — **不再缺失**

**视觉稿**: `foundry/html/ontology-wiki-diff.html`
**React**: 无（无路由无页面文件）

#### 1. 页面结构检查

**视觉稿结构**（单栏内容区 `p-content`）:
- **顶部标题行**: "版本对比" + "订单风险分诊规范 · main 分支" + 版本选择器（v9 vs v8 下拉）+ 视图切换（并排/行内/统一 3 按钮）
- **变更摘要面板**: 新增 4 + 删除 2 + 修改 3 + 提交信息（v8→v9, 大同, 2h前, "新增跨境发货因子和新客首单判定"）
- **Diff 对比区**: 左右两栏（v8 左 / v9 右），含版本头部（版本号+时间+作者）+ diff 内容块（等宽字体，行号+颜色标注）
- **版本历史时间线**: 5 版本（v9/v8/v7/v6/v5），含版本号+提交信息+作者+时间+当前标注
- **恢复确认 Modal**: 警告框（将丢弃变更列表）+ 取消/确认恢复

#### 2. 组件级盘点

需新建组件:

| 组件 | 说明 |
|------|------|
| `DiffVersionSelector` | 版本 A/B 下拉选择器 |
| `DiffViewModeToggle` | 视图切换（并排/行内/统一 3 按钮组） |
| `DiffSummaryBar` | 变更摘要（新增 N / 删除 N / 修改 N + 提交信息） |
| `DiffBlock` | diff 内容块（行号 + diff-add 绿/del 红/mod 黄/same 灰） |
| `VersionTimeline` | 版本历史时间线 |
| `RestoreConfirmModal` | 恢复确认弹窗 |

#### 3. 数据驱动检查

**视觉稿数据**: "订单风险分诊规范"、v9 vs v8、diff 内容（删除 medium 阈值旧版→新增新版含跨境发货+新客首单）、版本历史 5 条

**需新建 API**:
| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/v1/wiki/pages/:pageId/versions` | 版本列表 |
| GET | `/v1/wiki/pages/:pageId/diff?from=v8&to=v9` | diff 结果 |
| POST | `/v1/wiki/pages/:pageId/restore` | 恢复到指定版本 |

**需新建数据库表**: `wiki_page_version` — id, page_id, version, content, commit_message, author, created_at, parent_version

#### 4. 交互检查

- 版本 A/B 下拉切换
- 视图模式切换（并排/行内/统一）
- "返回编辑"按钮
- "恢复到 v8"按钮 → 确认 Modal
- 版本历史时间线点击

#### 5. 主题与样式检查

- 自定义 diff CSS:
  - `.diff-add`: 绿色背景 + 左侧绿色边框（`#dcfce7` + `#22c55e`）
  - `.diff-del`: 红色背景 + 左侧红色边框 + 删除线 + 半透明（`#fee2e2` + `#ef4444`）
  - `.diff-mod`: 黄色背景 + 左侧黄色边框（`#fef3c7` + `#f59e0b`）
  - `.diff-same`: 半透明（`opacity: 0.5`）
- Menlo/Monaco 等宽字体, 11px, 行高 1.7
- 右栏(v9) 有紫色高亮边框

#### 6. 系统现状对比

**完整度: 0%** — 需从零新建

**工作量: M (2-3 天)** | **优先级: P2**（diff 渲染可使用 `diff` npm 包计算差异）

#### 7. 风险与依赖

- 技术风险：Diff 算法需引入 diff 库（`diff` npm 包）或后端返回计算好的 diff
- 后端依赖：Wiki 版本管理 API 需新建
- 数据依赖：需 5 个版本的 Wiki 页面种子数据
- 组件依赖：依赖 Wiki 详情页（页面 6）需先完成
- 导航入口：从 Wiki 详情页顶部栏"版本对比"Tab

---

### 页面 8: 管道详情/画布 (`pipeline`)

> **现完整度（2026-07-29）：55%** · `/data/pipelines/:pipelineId` ✅

**视觉稿**: `foundry/html/pipeline.html`
**React**: `pipelineCanvas.tsx`
**路由**: `/data/pipelines/:pipelineId` ✅ 已注册

#### 1. 页面结构检查

| 维度 | 视觉稿 | 系统 | 差距 |
|------|--------|------|------|
| 顶栏 | 三段式（左：撤销/重做/分支/保存 / 中：视图Tab 编辑/提案/历史 / 右：Build徽标/检查/设置/分享/详情） | 单行 BpToolbar（返回/分支 disabled/管道类型/保存/提议/计划编辑器/部署） | 缺中间视图 Tab、缺撤销重做 |
| 画布工具栏 | 在画布内部顶部（变换算子 + 添加数据集 + 参数） | 在 BpToolbar 下方独立行（15 算子分 3 组） | 位置不同，功能等价（系统更强：支持拖拽） |
| 画布主区 | 左右两栏（画布+预览 + 右输出侧栏） | 左右两栏（画布+预览 + 右检查器） | 右栏结构不同 |
| DAG 节点 | 5 节点（2数据源+Join+Expression+输出）多源汇入 | 固定 3 节点（input→transform→output）线性 | **拓扑能力不同** |
| 底部预览 | 有搜索 + 相关链接（计划/沿袭/代码库） | 有预览表（6列5行），无搜索无链接 | 缺搜索+链接 |
| 右侧栏 | 输出区（数据集/Object/链接类型）+ 协作者 + 详情 | 检查器（节点属性+格式/写入模式+Schema） | **结构完全不同** |

#### 2. 组件级盘点

| 组件 | 视觉稿 | 系统 | 需新建/改造 |
|------|--------|------|------------|
| DAG 缩放控制器（缩小/100%/放大/适应） | 有 | 无 | **新建** |
| 画布图例（数据集/变换/输出三色） | 有 | 无 | **新建** |
| 视图切换 Tab（编辑/提案/历史） | 有 | 无 | **新建** |
| 多源 Join DAG（2输入→Join→Expression→输出） | 有 | 固定 3 节点线性 | **改造** |
| 输出分区侧栏（数据集输出/Object输出/链接输出） | 有 | 节点属性检查器 | **改造** |
| 协作者头像组 | 有 | 无 | **新建** |
| 预览区列搜索框 | 有 | 无 | **新建** |
| 预览区相关链接条 | 有 | 无 | **新建** |
| 撤销/重做 | 有 | 无 | **新建** |
| 算子拖拽 | 无 | 有（系统增强） | 系统更强 |
| 双击删除节点 | 无 | 有（系统增强） | 系统更强 |
| 管道类型选择器 | 无 | 有（批量/增量/流式） | 系统多出 |

#### 3. 数据驱动检查

**视觉稿数据**: orders_raw(12847行14列)+customers(8102行9列)→Join on customer_id→enrich_order→Order输出、预览表 7列3行、输出 3 类（orders_enriched APPEND/Order Update by PK/Order→Customer 1:N）

**当前 API**: `/v1/pipelines`（列表 find by id）+ `/v1/analytics/datasets/preview`

**缺失 API**:
- `GET /v1/pipelines/:id/graph` — 节点+连线拓扑
- `GET /v1/pipelines/:id/outputs` — 输出配置列表
- `GET /v1/pipelines/:id/collaborators` — 协作者
- `GET /v1/pipelines/:id/proposals` / `/history` — 提案/历史
- `GET /v1/pipelines/:id/checks` — 检查状态

**缺失数据库表**: `pipeline_nodes`, `pipeline_edges`, `pipeline_outputs`, `pipeline_collaborators`
当前 `PipelineMeta` 只有 id/sourceId/target/datasetRid/name/displayName/objectTypeHint/lastBuild

#### 4. 交互检查

| 交互 | 视觉稿 | 系统 | 缺失 |
|------|--------|------|------|
| 拖拽节点移动 | 隐含 | 有（已实现） | ✅ |
| 工具栏拖入算子 | 隐含 | 有（系统增强：比视觉稿更完善） | ✅ 系统更强 |
| 双击删除节点 | 无 | 有（系统增强） | ✅ 系统更强 |
| 撤销/重做 | 有 | 无 | **缺失** |
| 视图切换（编辑/提案/历史） | 有 | 无 | **缺失** |
| 缩放/适应画布 | 有 | 无 | **缺失** |
| 分支切换 | 有 | 有但 disabled | 需启用 |
| 节点选中高亮 | 有 | 有 | ✅ |
| 输出项添加/折叠 | 有 | 无 | **缺失** |
| 分享/详情 | 有 | 无 | **缺失** |

#### 5. 主题与样式检查

- 视觉稿：浅色（`#fff` 背景），节点 4 色区分（黄=数据集/蓝=变换/紫=Expression/绿=输出），`p-pb-*` CSS 前缀
- 系统：暗色（`--aos-*` 变量），节点 3 色（amber/cyan/emerald），`bp-pipe-*` CSS 前缀，`grid-pattern` 暗色网格背景
- 系统有暗色支持 + 响应式断点（窄屏变纵向），视觉稿无响应式

#### 6. 系统现状对比

**完整度: ~45%**

核心差距 Top 7（按影响排序）:
1. DAG 拓扑固定为线性 3 节点 — 视觉稿是多源 Join DAG → 需后端 API + 前端任意拓扑渲染
2. 右侧栏架构完全不同 — 视觉稿"输出配置" vs 系统"节点属性检查器"
3. 缺缩放/平移/图例 — 画布核心交互
4. 缺视图 Tab（编辑/提案/历史）
5. 缺撤销/重做
6. 缺协作者/详情区
7. 预览面板简化 — 缺列搜索+相关链接

**工作量: L (3-5 天)** | **优先级: P1**

改造优先级:
- P0: DAG 拓扑动态化（后端 graph API + 前端任意节点渲染）
- P1: 缩放/平移 + 图例
- P1: 右侧输出配置侧栏
- P2: 视图 Tab + 预览增强

#### 7. 风险与依赖

- 技术风险：DAG 任意拓扑渲染需自动连线算法（计算节点端口位置+贝塞尔路径）；画布缩放需处理 SVG viewBox/transform 与节点绝对定位的坐标系统一
- 后端依赖：`GET /v1/pipelines/:id/graph` + `/outputs` + `/collaborators` + `/proposals` + `/history`
- 数据依赖：需多节点 Join 管道测试数据
- 组件依赖：缩放控件可复用 LogicCanvasPage 画布缩放逻辑
- 导航入口：从管道列表页点击进入 ✅ 已就绪

---

### 页面 9: 数据源详情/DB Explorer (`source-detail`)

> **现完整度（2026-07-29）：50%** · `/data/sources/:sourceId` ✅

**视觉稿**: `foundry/html/source-detail.html`
**React**: `sourceDetailPage.tsx`
**路由**: `/data/sources/:sourceId` ✅ 已注册

#### 1. 页面结构检查

| 维度 | 视觉稿 | 系统 | 差距 |
|------|--------|------|------|
| 页面定位 | 纯"数据库浏览器/DB Explorer" | "数据源详情"含 4 Tab | 系统更宽泛 |
| 顶栏 | 标题"探索 · prod-postgresql-orders" + PostgreSQL 徽标 + Refresh/Filter | BpToolbar（返回/连接器标签/存储标签/管道链接/刷新）+ 状态指示 | 不同 |
| 主体布局 | 三栏（左 Schema 树 + 中 ER 图+预览 + 右已选表） | 三栏（左表列表 + 中预览 + 右源信息）+ 4 Tab | 结构不同 |
| 左栏 | 数据库 Schema 树（public 8表/analytics 3表），含列定义 PK/FK/类型 | 管道派生的扁平表列表（仅表名） | **数据来源不同** |
| 中栏 | 上 ER 图（4表+FK连线）+ 下数据预览（48291行） | 表标题 + 采样预览（50行） | **缺 ER 图** |
| 右栏 | 已选表列表（3表卡片）+ 创建同步 | 数据源元信息 + 同步任务 | **功能不同** |

#### 2. 组件级盘点

| 组件 | 视觉稿 | 系统 | 需新建/改造 |
|------|--------|------|------------|
| Schema 树（多级折叠 schema→表→列） | 有（含 PK/FK/类型标注） | 扁平表列表 | **改造为多级树** |
| ER 图（表节点 + FK 虚线连线） | 有（4 表 + 紫色 FK 连线） | 无 | **新建** |
| FK 连线 | 有（紫色虚线 + 字段标注） | 无 | **新建** |
| 列类型标签（BIGINT PK / DECIMAL(10,2)） | 有 | 无（仅列名） | **新建** |
| 已选表卡片列表 | 有（3 表卡片 + 移除按钮 + Clear） | 无 | **新建** |
| 预览表头类型标注 | 有（FK 列紫色 + 🔗 icon） | 无 | **新建** |
| 预览数据状态着色 | 有（completed 绿/pending 橙/cancelled 红） | 无 | **新建** |
| Filter 按钮 | 有 | 无 | **新建** |
| 4 Tab（概览/探索/同步/凭证） | 无 | 有 | 系统多出 |

#### 3. 数据驱动检查

**视觉稿数据**: PostgreSQL `prod-postgresql-orders`、public 8 表、orders 6 列（order_id BIGINT PK / customer_id BIGINT FK / amount DECIMAL / status VARCHAR）、ER 图 4 表 + 3 FK 关系、预览 5 行

**当前 API**: `/v1/sources` + `/v1/pipelines`（派生表列表）+ `/v1/datasets` + `/v1/syncs`

**缺失 API**:
- `GET /v1/sources/:id/schemas` — schema + 表 + 列定义
- `GET /v1/sources/:id/tables/:table/columns` — 列名/类型/PK/FK
- `GET /v1/sources/:id/relationships` — 表间 FK 关系
- `GET /v1/sources/:id/tables/:table/count` — 行数统计

**缺失数据库表**: `source_schemas`, `source_tables`, `source_columns`
当前 `SourceRow` 只有 id/type/status/runtimeMode/pluginId

**关键差距**: 表列表从 pipelines 间接派生，不是从数据库 schema 直接获取

#### 4. 交互检查

| 交互 | 视觉稿 | 系统 | 缺失 |
|------|--------|------|------|
| 搜索表 | 有 | 有（但未接线 onChange） | 需接线 |
| 展开/折叠 Schema | 有 | 无（无 schema 分组） | **缺失** |
| 点击表切换预览 | 有 | 有（setActiveTable） | ✅ |
| 查看列定义 | 有 | 无 | **缺失** |
| ER 图节点点击 | 有 | 无 | **缺失** |
| 预览状态着色 | 有 | 无 | **缺失** |
| 选择/移除表 | 有 | 无 | **缺失** |
| Clear 全部 | 有 | 无 | **缺失** |
| 创建同步 | 有 | 有（跳计划编辑器） | ✅ |
| Filter | 有 | 无 | **缺失** |

#### 5. 主题与样式检查

- 视觉稿：浅色，选中蓝 `#3B82F6`，FK 紫 `#7C3AED`，FK 连线 `#A78BFA` 虚线，三栏固定宽（左 260px / 中 flex / 右 280px）
- 系统：暗色，`bp-src-detail-*` 类，有暗色适配 + 响应式断点

#### 6. 系统现状对比

**完整度: ~35%**

核心差距 Top 5（按影响排序）:
1. **缺 ER 图/表关系图** — 视觉稿中栏核心组件，系统完全没有
2. **左栏不是真正的 Schema 树** — 只有管道派生的扁平表名，无 schema 分组、无列定义
3. **数据来源错位** — 视觉稿直连数据库 schema，系统从 pipelines 间接推导
4. **缺列类型/PK/FK 元数据** — 视觉稿核心信息维度
5. **右栏功能不同** — 视觉稿"已选表待同步" vs 系统"数据源元信息"

**工作量: L (3-5 天)** | **优先级: P1**

改造优先级:
- P0: Schema 树 + 后端 schema API（数据库浏览器的基础）
- P0: ER 图组件（核心差异化组件）
- P1: 列定义/PK/FK 元数据展示
- P1: 右栏改造为"已选表"模式
- P2: 预览着色 + Filter

#### 7. 风险与依赖

- 技术风险：ER 图自动布局需根据 FK 关系自动计算表节点位置，避免连线交叉；Schema 树性能（大数据库需虚拟滚动）；直连数据库 schema 查询可能有性能/权限问题
- 后端依赖：`GET /v1/sources/:id/schemas` + `/relationships` + `/tables/:table/columns` — 当前后端无 schema 浏览能力
- 数据依赖：需 JDBC metadata 查询获取真实 schema 信息 + FK 关系元数据
- 组件依赖：ER 图可参考 LogicCanvasPage 或 pipelineCanvas 的 SVG 节点+连线模式
- 导航入口：从数据连接列表页 `ConnectorTagLink` / `SourceNameLink` 点击 ✅ 已通

---

## 附录 A: 后端 API 缺失总清单

### 本体管理 API

| API | 用途 | 页面 |
|-----|------|------|
| `GET /v1/ontology/object-types/:typeId` | OT 完整详情（PK/TitleKey/BackingDataset/Sync策略/可见性） | 页1 |
| `GET /v1/ontology/object-types/:typeId/data-quality` | 数据质量指标 | 页1 |
| `GET /v1/ontology/object-types/:typeId/usage` | 使用统计 | 页1 |
| LinkType 扩展字段 | joinMethod/status/rid/properties | 页2 |
| ActionType 扩展字段 | description/toolDescription/contributors/status/rid/rules/dependents | 页3 |
| `GET /v1/actions/types/:id/dependents` | 依赖列表 | 页3 |
| Property CRUD | 4 个 API（列表/创建/更新/删除/automap） | 页4 |
| Function 只读 | `GET /function-types/:id` + `/code` | 页5 |
| Wiki 页面管理 | 5 个 API（页面定义/保存/版本/预览/Object Set查询） | 页6 |
| Wiki 版本管理 | 3 个 API（版本列表/diff/恢复） | 页7 |

### 管道与数据源 API

| API | 用途 | 页面 |
|-----|------|------|
| `GET /v1/pipelines/:id/graph` | DAG 节点+连线拓扑 | 页8 |
| `GET /v1/pipelines/:id/outputs` | 输出配置列表 | 页8 |
| `GET /v1/pipelines/:id/collaborators` | 协作者 | 页8 |
| `GET /v1/pipelines/:id/proposals` `/history` | 提案/历史 | 页8 |
| `GET /v1/sources/:id/schemas` | Schema + 表 + 列定义 | 页9 |
| `GET /v1/sources/:id/tables/:table/columns` | 列名/类型/PK/FK | 页9 |
| `GET /v1/sources/:id/relationships` | FK 关系图 | 页9 |
| `GET /v1/sources/:id/tables/:table/count` | 表行数 | 页9 |

**合计缺失 API: ~22 个**

---

## 附录 B: 数据库表缺失总清单

| 表 | 用途 | 页面 |
|----|------|------|
| `property` | 属性定义（含 base_type/status/formatter/column 映射） | 页4 |
| `function_type` | 函数元数据（含 code_preview/inputs/output） | 页5 |
| `wiki_page` | Wiki 页面定义（Widget 树+工作流定义+Object Set 配置） | 页6 |
| `wiki_page_version` | Wiki 版本历史 | 页6,7 |
| `pipeline_nodes` | 管道 DAG 节点 | 页8 |
| `pipeline_edges` | 管道 DAG 连线 | 页8 |
| `pipeline_outputs` | 管道输出配置 | 页8 |
| `pipeline_collaborators` | 管道协作者 | 页8 |
| `source_schemas` | 数据源 Schema | 页9 |
| `source_tables` | 数据源表（含行数/列数/类型） | 页9 |
| `source_columns` | 数据源列（含 PK/FK 标记） | 页9 |

**合计缺失表: ~11 张**

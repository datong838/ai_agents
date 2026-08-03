# 223 全站 UI 对齐开发计划

> 版本：v2.6（2026-07-27）
> **⚠️ 2026-07-29**：完整度与「缺失页」清单已过时。请改用：
> - [`223-deep-checklist.md`](./223-deep-checklist.md) §1.1
> - [`223-deep-checklist-2.md`](./223-deep-checklist-2.md) / [`-3`](./223-deep-checklist-3.md) v1.1
> - **新排期** [`227-未完成项补齐计划.md`](./227-未完成项补齐计划.md)
> v2.6 变更：Phase 2 全部完成 ✅ 并合并 — 模型管理后端(10API+54种子) + 对话机器人(4步向导+HITL) + P0列表页(3页) + 运维审批4页
> v2.5 变更：Phase 1 全部完成 ✅ 并合并 — 4 Worker 并行交付 56 文件 / 8395 行新增代码
> v2.4 变更：新增多 Agent 协作编排（1 Planner + 4 Worker），Phase 0 深度理解验证已完成 ✅
> 状态：基于 P0/P1/P2 + 详情页共四份深度检查的完整结果重写；v2.1 新增附录 H；v2.2 补入 223-deep-checklist-3 并修正本体工作量；v2.3 新增附录 I（独立任务清单，明确另一开发可移交范围）
> 范围：全站 9 大分区，66 个视觉稿页面（含 9 个详情页/弹出页），按视觉稿对齐
> 配套文档：
> - [223-deep-checklist.md](./223-deep-checklist.md)（P0+P2 共 35 页）
> - [223-deep-checklist-2.md](./223-deep-checklist-2.md)（P1 共 31 页）
> - [223-deep-checklist-3.md](./223-deep-checklist-3.md)（详情页/弹出页共 9 页）
> - [223-full-ui-gap-analysis.md](./223-full-ui-gap-analysis.md)（全量差距盘点）
> - [223-menu-alignment-full.md](./223-menu-alignment-full.md)（菜单对照）

---

## 0. 前置决策（已确认）

| 问题 | 用户决策 |
|---|---|
| 改造范围 | 全站对齐，66 个页面 |
| 缺失页面处理 | **直接做真实页面**，严格按照视觉稿 |
| 名字统一 | **全部按视觉稿改**（8 处名字差异） |
| 后端改造 | 可以大改，按需加字段 |
| 测试数据 | 可以任意写，不做限制 |
| 品牌色 | 全局推广 `#0F6E56`（深绿） |
| 实施顺序 | **后续专门写计划**（本文档） |

---

## 1. 全局汇总

### 1.1 总工作量

| 优先级 | 分区 | 页面数 | 完全缺失 | 部分实现 | 估算工作量 |
|---|---|---|---|---|---|
| P0 | 工作台 + 构建工具 | 9 | 3 | 6 | 22-32 人天 |
| P1 | AIP + 模型 + 本体 | 31 | 10 | 21 | 63-95 人天（v2.2 上调，本体 Wiki 详情 XXL）|
| P2 | 管道 + 数据源 + 运维 | 26 | 3 | 23 | 65-85 人天 |
| **总计** | | **66** | **16** | **50** | **150-212 人天** |

> **v2.2 调整说明**：P1 本体小计从 18-25 天上调到 30-48 天（来源：223-deep-checklist-3 揭示 Wiki 详情是 XXL 10-15d 而非 M 2d、属性详情是 XL 5-8d 而非 L 3-5d、Link/Action 详情从 M 上调到 L）。总工作量相应从 138-189 上调到 150-212 人天。

### 1.2 完全缺失的 16 个页面

| # | 页面 | 分区 | 工作量 |
|---|---|---|---|
| 1 | 组件注册表 | P0 工作台 | M（3-4 天）|
| 2 | 变量管理器 | P0 工作台 | M（3-4 天）|
| 3 | 主题与样式 | P0 工作台 | M（2-3 天）|
| 4 | AIP 助手 | P1 AIP | L（3-5 天）|
| 5 | AIP 分析师 | P1 AIP | L（5 天+）|
| 6 | 智能体插件 | P1 AIP | M（2 天）|
| 7 | Draft 审批台 | P1 AIP | L（3-5 天）|
| 8 | 模型目录 | P1 模型 | L（3-5 天）|
| 9 | 容量管理 | P1 模型 | M（1-2 天）|
| 10 | 属性类型详情 | P1 本体 | L（3-5 天）|
| 11 | Function 详情 | P1 本体 | M（2 天）|
| 12 | Wiki 详情 | P1 本体 | M（2 天）|
| 13 | Wiki 差异 | P1 本体 | M（1-2 天）|
| 14 | DocIntel 管道 | P2 管道 | M（3-4 天）|
| 15 | 文档智能 | P2 数据源 | M（3-4 天）|
| 16 | 数据源新建 | P2 数据源 | M（2-3 天）|

---

## 2. 双人分工策略（核心目标：减少交叉依赖）

### 2.1 分工原则

1. **后端表归属**：每个数据库表只能由一方创建 + 维护，避免冲突
2. **前端组件归属**：每个目录只能由一方修改，避免 merge 冲突
3. **API 契约先于实现**：跨方调用的 API 先约定 schema，再并行实现
4. **共享组件抽取**：双方都用到的组件（如 BpArchitectureBar、表格、徽章）由 owner 抽取到共享层
5. **种子数据统一管理**：所有测试数据写入 `services/aos-api/aos_api/demo/` 目录，由后端 owner 统一管理

### 2.2 依赖关系图

```
┌─────────────────────────────────────────────────────────┐
│  Buddy（B）后端 + 数据层 + 复杂交互页                    │
│                                                          │
│  • 后端所有新表 + 种子数据                               │
│  • 所有 API 实现                                         │
│  • 画布编辑器类（Canvas/Pipeline/Lineage）               │
│  • 复杂三栏交互页（DB Browser/Decision Draft）           │
│  • Workflow 引擎（事件/逻辑/审批）                       │
└─────────────────────────────────────────────────────────┘
                          ↑
                   【API 契约层】
                          ↑
┌─────────────────────────────────────────────────────────┐
│  我（A）前端组件 + 列表/详情页 + 配置页                  │
│                                                          │
│  • 名字统一 + 路由骨架                                   │
│  • 列表/表格/卡片网格页                                  │
│  • 多 Tab 配置页                                         │
│  • 简单 CRUD 表单                                        │
│  • 步骤向导类页面                                        │
│  • 全局共享组件（BpArchitectureBar/BpBadge 等）          │
└─────────────────────────────────────────────────────────┘
```

### 2.3 分工方案 A：按"页面类型 + 后端/前端"切分

#### **我（A）负责 — 前端为主，约 80-100 人天**

| 类别 | 页面 | 工作量 | 关键依赖 |
|---|---|---|---|
| **Phase 0** | 名字统一 + 路由骨架 | 0.5 天 | 无 |
| **Phase 0** | 14 个缺失页路由注册 + 最小页面 | 2 天 | 无 |
| **P0 列表/网格** | 应用列表、模块管理、对象探索 | 5 天 | B 提供 module API |
| **P0 配置表单** | 事件配置（向导式）、发布入口 | 3 天 | B 提供 events API |
| **P0 简单 CRUD** | 组件注册表、变量管理器、主题与样式 | 8 天 | B 提供 widget/theme API |
| **P1 列表/卡片** | 智能体目录（改卡片网格）、Evals、成熟度楼梯 | 5 天 | B 提供 registry/evals API |
| **P1 多 Tab** | 模型路由、模型供应商（补健康检查卡）、AIP 逻辑画布（前端）| 5 天 | B 提供 router/providers API |
| **P1 配置向导** | 智能体导入（补 Adapter）、能力导入（补 C0/C1/C2）| 4 天 | B 提供 scan API |
| **P1 简单 CRUD** | 容量管理、Agent 工具面板（补质量评分）| 3 天 | B 提供 capacity/quality API |
| **P2 列表/表格** | 数据链接器、同步路由、FDE 资产包、变更审批 | 6 天 | B 提供 connectors/assets API |
| **P2 配置表单** | 同步配置（多 Tab）、媒体集（3 Tab）、配置与密钥 | 5 天 | B 提供 syncs/media API |
| **P2 步骤向导** | 数据源新建（4 步向导）、Ferry 摆渡（4 步向导）| 4 天 | B 提供 source/ferry API |
| **P2 多 Tab** | 数据集预览（5 Tab）、数据健康（4 Tab + 直方图）| 7 天 | B 提供 dataset/health API |
| **P2 代码视图** | 代码库（4 栏 IDE）| 3 天 | B 提供 repos API |
| **P2 接入案例** | 接入案例（信息密度高）| 4 天 | B 提供 cases API |
| **P2 简单运维** | Hub 舰队、Release 通道、Spoke 详情 | 5 天 | B 提供 hub/spokes API |
| **全局** | 品牌色统一 + 共享组件抽取 | 3 天 | — |
| **小计** | | **~72-80 天** | |

#### **Buddy（B）负责 — 后端 + 复杂前端，约 80-100 人天**

| 类别 | 任务 | 工作量 | 关键产出 |
|---|---|---|---|
| **后端基础** | 所有 47+ 张新表 + schema 迁移 | 5 天 | 表结构 + 迁移脚本 |
| **后端基础** | 所有 60+ 个新 API 实现 | 15 天 | API endpoint + 测试 |
| **种子数据** | 全部分区测试数据（写入 demo 目录）| 5 天 | demo/seed_*.py |
| **P0 画布编辑器** | workshop-canvas（最复杂，三栏+9 pop-panel）| 8 天 | Canvas 编辑器 |
| **P0 画布编辑器** | 模块接口（嵌套 Loop 示意图）| 1 天 | — |
| **P1 画布/三栏** | AIP 助手（聊天+流式）、AIP 分析师（聊天+地图）| 7 天 | 流式 API + 地图集成 |
| **P1 三栏审批** | Draft 审批台（三栏+审批流+timeline）| 4 天 | 三栏交互 |
| **P1 编辑器** | 可观测性（代码编辑器 Monaco）| 2 天 | 代码组件 |
| **P1 模型入口** | 模型目录（三层架构条 + Tab 系统）| 4 天 | BpArchitectureBar |
| **P1 本体编辑** | 属性类型详情（属性编辑器 + 列映射 + Automap）| 4 天 | Property Editor |
| **P1 本体详情** | Function 详情（代码编辑器 + 参数 + 测试）| 2 天 | Function Editor |
| **P1 本体 Wiki** | Wiki 详情（富文本 + 关联 + 版本）| 2 天 | Wiki Editor |
| **P1 本体 Wiki** | Wiki 差异（diff 渲染）| 2 天 | Diff Engine |
| **P2 画布编辑器** | pipeline.html（两栏 Pipeline Builder + 10 变换工具）| 5 天 | Pipeline Builder |
| **P2 画布编辑器** | pipeline-list.html（三栏 SVG 节点图）| 3 天 | 节点图 |
| **P2 沿袭图** | lineage.html（全局沿袭图 + 节点展开）| 3 天 | Lineage Graph |
| **P2 三栏浏览** | source-detail.html（DB Browser + 表关系图）| 4 天 | DB Explorer |
| **P2 调度联动** | schedules.html（沿袭图 + 详情联动 + Cron）| 3 天 | — |
| **P2 LLM 配置** | DocIntel 管道（LLM 配置面板 + 5 Tab）| 3 天 | LLM Node Config |
| **P2 文档智能** | document-intelligence.html（OCR + LLM 提取）| 3 天 | Extract Engine |
| **P2 复杂运维** | 边缘代理（指标卡 + sparkline + Tab）| 3 天 | Metrics + Sparkline |
| **小计** | | **~88-100 天** | |

---

## 3. 13 周开发计划（按依赖关系排序）

### 3.1 总体时间线

```
W1-W2:  Phase 0 + 后端基础（表 + API 契约 + 种子数据）
W3-W4:  P0 工作台 + 构建工具（最复杂，先打基础）
W5-W6:  P0 收尾 + P1 模型管理（三层架构 + 入口页）
W7-W8:  P1 AIP 核心（对话机器人 + 逻辑画布 + Draft 审批）
W9-W10: P1 AIP 收尾 + P1 本体编辑器（属性/Function/Wiki）
W11:    P2 运维交付（最简单的分区，快速出成果）
W12:    P2 数据源与同步
W13:    P2 管道与数据治理（含 2 个复杂画布编辑器）
```

### 3.2 详细周计划

#### **W1: Phase 0 + 后端基础启动**

| 谁 | 任务 | 产出 |
|---|---|---|
| A | Phase 0：名字统一（8 处）+ nav 改造 | nav.ts 更新 |
| A | Phase 0：14 个缺失页路由注册 + 最小页面骨架 | 14 个 .tsx 占位 |
| B | 后端：设计所有 47 张表的 schema | schema.sql |
| B | 后端：API 契约文档（OpenAPI spec）| contracts.yaml |
| **协作** | API 契约 review + 调整 | 双方对齐 |

#### **W2: 后端表 + 种子数据 + 简单页面**

| 谁 | 任务 | 产出 |
|---|---|---|
| A | P2 简单运维：Hub 舰队、Release 通道、Spoke 详情、FDE 资产包 | 4 个页面 |
| A | 全局：品牌色统一 + 共享组件抽取（BpBadge/BpCard）| 共享组件 |
| B | 后端：创建所有表 + 迁移脚本 | migration scripts |
| B | 后端：种子数据 1（module/widget/theme/connectors）| seed_*.py |
| B | 后端：基础 API 实现（CRUD 类）| 30 个 API |

#### **W3: P0 工作台核心**

| 谁 | 任务 | 产出 |
|---|---|---|
| A | 应用列表（最近使用 + 全部应用 + 分类筛选）| WorkshopListPage |
| A | 风险告警管理（Top bar + Filter + 活动日志）| InboxPage |
| A | 创建应用（左侧垂直步骤 + 各种选择器）| CreateAppPage |
| B | workshop-canvas（三栏 + 9 pop-panel + 工作流模式）| CanvasPage（核心）|
| B | 后端：画布相关 API（widgets/events/queries/variables）| 8 个 API |

#### **W4: P0 构建工具**

| 谁 | 任务 | 产出 |
|---|---|---|
| A | 组件注册表（3 列卡片网格 + 4 来源筛选）| WidgetRegistryPage |
| A | 变量管理器（两栏 + 类型动态表单）| VariablesPage |
| A | 主题与样式（两栏 + 主题编辑器 + 实时预览）| StylesPage |
| A | 事件配置（向导式 5 步）| EventsPage |
| A | 发布入口（发布流程 + 环境卡片）| PublishPage |
| B | workshop-canvas 收尾（拖拽 + 工作流模式）| CanvasPage 完善 |
| B | 模块接口（嵌套 Loop 示意图）| ModuleInterfacePage |
| B | 后端：种子数据 2（订单/风控/对象实例）| seed_orders.py |

#### **W5: P1 模型管理（B 主导）**

| 谁 | 任务 | 产出 |
|---|---|---|
| A | 模型路由（补三层架构条）| ModelRouterPage 完善 |
| A | 容量管理（3 Tab + Info Banner）| CapacityPage |
| A | 共享组件：BpArchitectureBar（三层架构条）| 共享组件 |
| B | 模型目录（三层架构条 + Tab 系统 + 注册流程）| ModelCatalogPage |
| B | 模型供应商（补健康检查 4 卡）| ProvidersPage 完善 |
| B | 后端：模型相关 API（catalog/registered/health/capacity）| 8 个 API |

#### **W6: P1 AIP 核心启动**

| 谁 | 任务 | 产出 |
|---|---|---|
| A | 智能体目录（表格改卡片网格 + 来源 Tab + 统计）| AgentRegistryPage |
| A | 智能体插件（4 已接入卡 + 4 类型卡 + 配置表单）| CapabilitiesPage |
| A | 成熟度楼梯（视觉细节对齐）| MaturityPage 完善 |
| B | AIP 助手（聊天 UI + 流式 SSE + 建议卡片）| AipAssistPage |
| B | 后端：流式 API + LLM 集成 | /v1/aip/assist/chat |

#### **W7: P1 AIP 交互页**

| 谁 | 任务 | 产出 |
|---|---|---|
| A | 对话机器人（两栏 + 4 Tab + 4 步向导）| AgentsPage 改造 |
| A | Agent 工具面板（补 Agent 上下文 + 质量评分）| ToolsPage 完善 |
| A | Evals 门控（数据丰富度对齐）| EvalsPage 完善 |
| B | AIP 逻辑画布（分支 Block + 汇聚 Handoff + 预览面板）| LogicCanvasPage 完善 |
| B | 后端：LogicEngine 支持 DAG 分支 | API 扩展 |

#### **W8: P1 Draft 审批 + 决策谱系**

| 谁 | 任务 | 产出 |
|---|---|---|
| A | 智能体导入（补 5 种 Adapter + 扫描结果）| AgentImportPage 完善 |
| A | 能力导入（补 C0/C1/C2 + YAML 预览）| CapabilityImportPage 完善 |
| A | 决策谱系（补检索/推理/熔断/回填阶段）| DecisionLineagePage 完善 |
| B | Draft 审批台（三栏 + 4 Tab + 审批流 + timeline）| DraftInboxPage（核心）|
| B | 后端：Draft 完整 API（5 个）+ 审批状态机 | /v1/aip/drafts/* |

#### **W9: P1 可观测性 + AIP 分析师**

| 谁 | 任务 | 产出 |
|---|---|---|
| A | 共享组件：代码编辑器封装（Monaco/CodeMirror）| BpCodeEditor |
| A | 共享组件：diff 渲染引擎 | BpDiffViewer |
| B | 可观测性（代码编辑器 + 安全约束 + 删除依赖）| ObservabilityPage |
| B | AIP 分析师（聊天 + Object 检索 + 地图可视化）| AipAnalystPage |
| B | 后端：NL2Query + 地图数据 API | /v1/aip/analyst/* |

#### **W10: P1 本体编辑器（B 主导）**

| 谁 | 任务 | 产出 |
|---|---|---|
| A | 本体管理 Discover（收藏网格 + 最近查看）| OntologyDiscoverPage |
| A | 对象探索、分支管理、图谱健康度（视觉对齐）| 3 个页面完善 |
| A | OKF funnel、OKF 概览、活知识 Wiki 索引（视觉对齐）| 3 个页面完善 |
| B | 属性类型详情（属性编辑器 + 列映射 + Automap）| PropertyDetailPage |
| B | Function 详情（代码编辑器 + 参数 + 测试 + 版本）| FunctionDetailPage |

#### **W11: P1 本体 Wiki（①期）+ P2 运维启动**

| 谁 | 任务 | 产出 |
|---|---|---|
| A | P2 运维：Hub 舰队、Release 通道、Spoke 详情（视觉对齐）| 3 个页面 |
| A | P2 运维：FDE 资产包、变更审批（双栏联动）| 2 个页面 |
| A | P2 运维：配置与密钥、接入案例（信息密度高）| 2 个页面 |
| B | Wiki 详情 ①期（Widget 树+画布+属性面板三栏基础）| WikiDetailPage ① |
| B | Wiki 差异（diff 渲染 + 变更高亮）| WikiDiffPage |
| B | Action 详情、Link 详情、Object 详情（视觉对齐）| 3 个页面 |

#### **W12: 数据源 + Wiki（②期）并行**

> Wiki ②期与 P2 数据源同期，B 主力放数据源，Wiki ②期作为副线

| 谁 | 任务 | 产出 |
|---|---|---|
| A | 数据链接器、同步路由、同步配置、媒体集、数据源新建 | 5 个页面 |
| A | 共享组件：BpSparkline + BpCronInput（W12 第 1 天抽取）| 共享组件 |
| B | 数据源详情 DB Browser（三栏 + Schema 树 + ER 图）| SourceDetailPage |
| B | 边缘代理（指标卡 + sparkline + 3 Tab）| AgentsPage |
| B | 文档智能（OCR + LLM 提取 + 4 态状态）| DocIntelligencePage |
| B | Wiki 详情 ②期（Object Set 构建器）— **副线，可推迟到 W13 缓冲** | WikiDetailPage ② |

#### **W13: 管道 + Wiki（③期）+ 收尾**

| 谁 | 任务 | 产出 |
|---|---|---|
| A | 管道提案、数据集预览、数据健康、搭建弹窗 | 4 个页面 |
| B | pipeline.html（两栏 Pipeline Builder + 10 变换工具）| PipelineBuilderPage |
| B | pipeline-list.html、lineage.html、schedules.html | 3 个页面 |
| B | DocIntel 管道、代码库（4 栏 IDE）| 2 个页面 |
| B | Wiki 详情 ③期（工作流编排+运行时预览）— **如②期未完则缓冲** | WikiDetailPage ③ |

---

## 4. API 契约层（关键协作点）

### 4.1 契约先行原则

跨方调用的 API 必须先约定 schema，写在 `services/aos-api/contracts/` 目录下：

```
services/aos-api/contracts/
├── modules.yaml          # module 相关 API
├── widgets.yaml          # 组件注册表 API
├── themes.yaml           # 主题 API
├── aip.yaml              # AIP 相关 API
├── models.yaml           # 模型管理 API
├── ontology.yaml         # 本体 API
├── pipelines.yaml        # 管道 API
├── sources.yaml          # 数据源 API
└── apollo.yaml           # 运维 API
```

### 4.2 第一周必须对齐的契约

| 契约 | 谁用 | 谁实现 | 优先级 |
|---|---|---|---|
| modules.yaml | A 用 | B 实现 | P0 |
| widgets.yaml | A 用 | B 实现 | P0 |
| themes.yaml | A 用 | B 实现 | P0 |
| aip/agents.yaml | A 用 | B 实现 | P1 |
| aip/drafts.yaml | A 用 | B 实现 | P1 |
| models/catalog.yaml | A 用 | B 实现 | P1 |
| ontology/properties.yaml | A 用 | B 实现 | P1 |
| sources/connectors.yaml | A 用 | B 实现 | P2 |
| pipelines/list.yaml | A 用 | B 实现 | P2 |

---

## 5. 共享组件抽取清单

双方都需要、必须先抽取的组件：

| 组件 | 用途 | 谁抽取 | 完成周 |
|---|---|---|---|
| `BpBadge` | 统一徽章（状态/优先级/来源）| A | W2 |
| `BpCard` | 统一卡片容器 | A | W2 |
| `BpArchitectureBar` | 三层架构定位条（L1→L2→L3→AIP）| A | W5 |
| `BpCodeEditor` | Monaco/CodeMirror 封装 | A | W9 |
| `BpDiffViewer` | diff 渲染引擎 | A | W9 |
| `BpSparkline` | 迷你折线图 | A | W12 |
| `BpStepper` | 步骤向导组件 | A | W4 |
| `BpCronInput` | Cron 表达式输入 | A | W12（提前，详见附录 H.4）|
| `BpToolbar` | 通用工具栏 | A | W2 |
| `BpEmpty` | 空状态 | A | W2 |

---

## 6. 数据库表归属

### 6.1 后端 owner（Buddy）

所有表由 B 设计 + 创建 + 维护，但 A 在写前端时如果发现缺字段，**必须通过 PR 提交给 B**，不能直接改表。

### 6.2 表分组（按分区）

| 分区 | 表数量 | 主要表 |
|---|---|---|
| 工作台 | 10 | module_widgets/events/queries/variables/interfaces/deployments/widget_registry/widget_categories/themes/module_themes |
| AIP | 12 | agents/agent_tools/agent_prompts/capabilities/drafts/draft_changes/draft_activities/evals/decision_traces/agent_imports/capability_imports/logic_flows |
| 模型 | 6 | model_catalog/registered_models/model_routes/provider_health/capacity_limits/capacity_usage |
| 本体 | 8 | object_types/object_instances/properties/column_mapping/functions/function_tests/wikis/wiki_versions/links |
| 数据源 | 13 | connectors/protocol_sources/agents/agent_metrics/syncs/sync_runs/media_sets/media_files/documents/extracted_fields/extraction_templates/sources/source_tables/source_columns |
| 运维 | 9 | hub/spokes/releases/asset_bundles/change_orders/config_overrides/integration_cases/integration_blockers/ferry_bundles |

**总计约 58 张表**

---

## 7. 风险与缓解

### 7.1 关键风险

| 风险 | 影响 | 缓解措施 |
|---|---|---|
| API 契约不对齐导致返工 | 高 | W1 必须完成所有契约 review |
| 画布编辑器（Canvas/Pipeline）延期 | 高 | W3-W4 集中攻坚，不并行其他复杂页 |
| 后端表设计返工 | 中 | W1 集中设计，W2 才落地 |
| 品牌色统一影响视觉一致性 | 中 | W2 先做共享组件层 |
| 种子数据质量影响验收 | 中 | 每周末做种子数据 review |

### 7.2 并行冲突点

| 冲突点 | 解决方案 |
|---|---|
| 同时改 `nav.ts` | W1 由 A 一次性改完，之后不再动 |
| 同时改 `App.tsx` 路由 | W1 由 A 一次性改完 |
| 共享组件修改 | 只允许 A 修改 `apps/web/src/components/bp/` |
| 后端 schema | 只允许 B 修改 `services/aos-api/aos_api/` 下的 store 文件 |
| 种子数据 | 只允许 B 修改 `services/aos-api/aos_api/demo/` |

---

## 8. 验收标准

### 8.1 每周验收

每周末双方进行以下检查：

- [ ] 视觉对齐（页面布局与视觉稿一致）
- [ ] 功能完整（所有交互可用）
- [ ] 数据驱动（内容从 API 拉取，不写死）
- [ ] 路由可达（所有 nav 项可点击进入）
- [ ] 主题切换（暗色/浅色都正常）
- [ ] 错误处理（API 失败时的降级）

### 8.2 最终验收（W13 末）

- [ ] 66 个页面全部按视觉稿对齐
- [ ] 16 个缺失页面全部实现
- [ ] 所有 API 联调通过
- [ ] 所有种子数据写入数据库
- [ ] 全站品牌色统一
- [ ] 全站回归测试通过

---

## 9. 备选分工方案

### 9.2 备选方案：按"分区"切分（不推荐）

**思路**：A 做某些分区，B 做其他分区

**问题**：
- 后端 API 没人统一管，schema 容易冲突
- 复杂画布编辑器分散到多方，无法集中攻坚
- 共享组件没人统一抽取

**结论**：❌ 不推荐，交叉依赖太多

### 9.3 备选方案：按"前后端"切分（不推荐）

**思路**：A 做所有前端，B 做所有后端

**问题**：
- A 工作量过大（前端 130+ 天）
- B 工作量过小（后端 50 天）
- 画布编辑器等复杂前端需要 B 级别的后端理解

**结论**：❌ 不推荐，工作量严重失衡

---

## 10. 待确认事项

1. **分工方案**：是否同意"按页面类型 + 后端/前端"切分（推荐方案 A）？
2. **时间周期**：13 周是否合理？是否需要压缩到 10 周？
3. **API 契约**：是否同意 W1 集中完成所有契约对齐？
4. **共享组件**：是否同意由 A 统一抽取和维护？
5. **种子数据**：是否同意由 B 统一管理？
6. **并行起点**：W3 开始双方是否可以完全并行？

---

## 附录 A：完整页面分工清单（66 页）

### A. 我（A）负责的页面（35 页）

| # | 页面 | 分区 | 周次 |
|---|---|---|---|
| 1 | 应用列表 | P0 工作台 | W3 |
| 2 | 风险告警管理 | P0 工作台 | W3 |
| 3 | 创建应用 | P0 工作台 | W3 |
| 4 | 组件注册表 | P0 构建工具 | W4 |
| 5 | 变量管理器 | P0 构建工具 | W4 |
| 6 | 主题与样式 | P0 构建工具 | W4 |
| 7 | 事件配置 | P0 构建工具 | W4 |
| 8 | 发布入口 | P0 构建工具 | W4 |
| 9 | 模块管理 | P0 工作台 | W4 |
| 10 | 智能体目录 | P1 AIP | W6 |
| 11 | 智能体插件 | P1 AIP | W6 |
| 12 | 成熟度楼梯 | P1 AIP | W6 |
| 13 | 对话机器人 | P1 AIP | W7 |
| 14 | Agent 工具面板 | P1 AIP | W7 |
| 15 | Evals 门控 | P1 AIP | W7 |
| 16 | 智能体导入 | P1 AIP | W8 |
| 17 | 能力导入 | P1 AIP | W8 |
| 18 | 决策谱系 | P1 AIP | W8 |
| 19 | 模型路由 | P1 模型 | W5 |
| 20 | 容量管理 | P1 模型 | W5 |
| 21 | 本体管理 Discover | P1 本体 | W10 |
| 22 | 对象探索 | P1 本体 | W10 |
| 23 | 分支管理 | P1 本体 | W10 |
| 24 | 图谱健康度 | P1 本体 | W10 |
| 25 | OKF funnel | P1 本体 | W10 |
| 26 | OKF 概览 | P1 本体 | W10 |
| 27 | 活知识 Wiki 索引 | P1 本体 | W10 |
| 28 | Hub 舰队 | P2 运维 | W11 |
| 29 | Release 通道 | P2 运维 | W11 |
| 30 | Spoke 详情 | P2 运维 | W11 |
| 31 | FDE 资产包 | P2 运维 | W11 |
| 32 | 变更审批 | P2 运维 | W11 |
| 33 | 配置与密钥 | P2 运维 | W11 |
| 34 | 接入案例 | P2 运维 | W11 |
| 35 | 数据链接器 | P2 数据源 | W12 |
| 36 | 同步路由 | P2 数据源 | W12 |
| 37 | 同步配置 | P2 数据源 | W12 |
| 38 | 媒体集 | P2 数据源 | W12 |
| 39 | 数据源新建 | P2 数据源 | W12 |
| 40 | 管道提案 | P2 管道 | W13 |
| 41 | 数据集预览 | P2 管道 | W13 |
| 42 | 数据健康 | P2 管道 | W13 |
| 43 | 搭建弹窗 | P2 管道 | W13 |

### B. Buddy（B）负责的页面（31 页）

| # | 页面 | 分区 | 周次 |
|---|---|---|---|
| 1 | 画布编辑 workshop-canvas | P0 工作台 | W3-W4 |
| 2 | 模块接口 | P0 工作台 | W4 |
| 3 | AIP 助手 | P1 AIP | W6 |
| 4 | AIP 分析师 | P1 AIP | W9 |
| 5 | AIP 逻辑画布 | P1 AIP | W7 |
| 6 | Draft 审批台 | P1 AIP | W8 |
| 7 | 可观测性 | P1 AIP | W9 |
| 8 | 模型目录 | P1 模型 | W5 |
| 9 | 模型供应商 | P1 模型 | W5 |
| 10 | 属性类型详情 | P1 本体 | W10 |
| 11 | Function 详情 | P1 本体 | W10 |
| 12 | Wiki 详情 | P1 本体 | W11 |
| 13 | Wiki 差异 | P1 本体 | W11 |
| 14 | Action 详情 | P1 本体 | W11 |
| 15 | Link 详情 | P1 本体 | W11 |
| 16 | Object 详情 | P1 本体 | W11 |
| 17 | 本体提案/漏斗管道 | P1 本体 | W10 |
| 18 | pipeline.html | P2 管道 | W13 |
| 19 | pipeline-list.html | P2 管道 | W13 |
| 20 | lineage.html | P2 管道 | W13 |
| 21 | schedules.html | P2 管道 | W13 |
| 22 | DocIntel 管道 | P2 管道 | W13 |
| 23 | 代码库 | P2 管道 | W13 |
| 24 | 数据源详情 DB Browser | P2 数据源 | W12 |
| 25 | 边缘代理 | P2 数据源 | W12 |
| 26 | 文档智能 | P2 数据源 | W12 |
| 27 | Ferry 摆渡 | P2 运维 | W11 |

### C. 后端任务（B 全权负责）

| 任务 | 工作量 | 周次 |
|---|---|---|
| 47 张表 schema 设计 + 迁移 | 5 天 | W1-W2 |
| 60+ 个 API 实现 | 15 天 | W2-W13 持续 |
| 流式 SSE（AIP 助手）| 2 天 | W6 |
| LogicEngine DAG 分支 | 2 天 | W7 |
| Draft 审批状态机 | 2 天 | W8 |
| NL2Query 引擎 | 3 天 | W9 |
| Automap 算法 | 2 天 | W10 |
| 种子数据（全分区）| 5 天 | W2-W13 持续 |

---

## 附录 B：每页核心改造点清单（按分区归并）

> 数据来源：`223-deep-checklist.md`（P0+P2 共 35 页）+ `223-deep-checklist-2.md`（P1 共 31 页）+ `223-deep-checklist-3.md`（详情页/弹出页共 9 页，作为 B.4 详情页工作量与字段需求的权威来源）
> 工作量标号：S=0.5-1 天 / M=1-2 天 / L=3-5 天 / XL=5-8 天 / XXL=10 天+
> 完整度=系统当前实现 vs 视觉稿的百分比

### B.1 P0 工作台 + 应用程序构建工具（9 页）

| # | 页面 | 视觉稿 | 完整度 | 核心改造点 | 工作量 | Owner |
|---|---|---|---|---|---|---|
| 1 | 画布编辑 workshop-canvas | workshop-canvas.html | 30% | 三栏（左组件树 280/中画布/右属性 320）+ 9 pop-panel + 工作流模式三栏 + 6 拖拽组件面板 | XL 8-10 天 | B |
| 2 | 模块接口 | workshop-module-interface.html | 10% | 单栏 5xl 居中 + input/output 接口卡 + 嵌套 Loop 示意图 + 蓝色提示条 | S 1-2 天 | B |
| 3 | 事件配置 | workshop-events.html | 20% | 上列表+下5步向导 + 6 触发器卡片 + 5 动作卡片 + 动态参数表单 + 预览卡 | M 3-4 天 | A |
| 4 | 对象探索 | workshop-object-view.html | 40% | 三栏（左对象树/中列表/右详情）+ 表格/卡片视图切换 | M 2-3 天 | A |
| 5 | 发布入口 | workshop-publish.html | 20% | 4 步骤条（开发→测试→预发布→生产）+ 环境卡片 + 发布/回滚操作 | S 1-2 天 | A |
| 6 | 组件注册表 | workshop-widget-registry.html | 0% | 4 来源 Tab（全部/内置/市场/代码）+ 3 列卡片网格 + 详情弹层 + 搜索 | M 3-4 天 | A |
| 7 | 变量管理器 | workshop-variables.html | 0% | 两栏 + 5 类型分组 + 类型动态表单 + 使用位置列表 | M 3-4 天 | A |
| 8 | 主题与样式 | workshop-styles.html | 0% | 两栏 + 主题编辑器（颜色/字体/间距 Tab）+ 颜色选择器 + 实时预览 | M 2-3 天 | A |
| 9 | 模块管理（系统多出） | — | 60% | 视觉稿无此项；系统保留，不进侧栏主菜单，可从其他页跳转 | S 0.5 天 | A |
| | **小计** | | | | **22-32 天** | |

**关键依赖**：组件注册表 / 变量管理器 / 主题与样式 / 事件配置 → 画布编辑器（组件/变量/样式/事件 4 个 Tab 依赖这些页面的数据）

### B.2 P1 AIP 决策引擎（14 页）

| # | 页面 | 完整度 | 核心改造点 | 工作量 | Owner |
|---|---|---|---|---|---|
| 1 | AIP 助手 aip-assist | 0% | 单栏 720px 聊天 + AI 气泡紫蓝渐变 + 2 列建议卡 + 权限感知标签 + 流式 SSE | L 3-5 天 | B |
| 2 | 对话机器人 agents | 25% | 改单栏网格→两栏（左 256 Agent 列表+右 4 Tab）+ 4 步创建向导 Modal + HITL 标签 | L 3-5 天 | A |
| 3 | AIP 分析师 aip-analyst | 0% | 三栏全屏（Tab + 聊天 + 右 256 本体面板）+ 思考过程折叠卡 + Object 卡 + 结果表 + 地图可视化 | XL 5+ 天 | B |
| 4 | AIP 逻辑画布 aip-logic | 60% | 缺分支 Block（双路红/绿）+ 汇聚 Handoff 节点 + 决策摘要/产物/开放问题配置区 + 预览面板 | M 2 天 | B |
| 5 | Agent 工具面板 aip-tools | 70% | 缺 Agent 上下文选择器（顶栏）+ 质量评分面板（总分+3 子分+改进建议+版本趋势） | M 1-2 天 | A |
| 6 | 成熟度楼梯 aip-maturity | 85% | 视觉细节对齐（L2 黄色边框/L4 红色熔断） | S 0.5 天 | A |
| 7 | 智能体目录 agent-registry | 30% | 表格→3 列卡片网格 + 来源 Tab（全部/平台/插件/外部）+ 统计数字 + 三方来源说明 + source/tags/calls 字段 | M 2 天 | A |
| 8 | 智能体插件 aip-capabilities | 0% | 4 已接入能力卡 + 4 可接入类型卡（Media Job/Script/Avatar/HTTP）+ 配置表单 + 连通测试 | M 2 天 | A |
| 9 | 智能体导入 aip-agent-import | 40% | 5 种 Adapter 类型说明卡 + 5 步导航（系统现 4 步）+ 仓库扫描结果表（框架/入口/依赖/模型/运行模式/外部服务）+ 详细 Adapter 配置 | M 2 天 | A |
| 10 | 能力导入 aip-capability-import | 35% | C0/C1/C2 选择卡（运行时/资源/示例）+ YAML 实时预览面板（语法高亮） | M 2 天 | A |
| 11 | Evals 门控 aip-evals | 75% | 分项结果表数据丰富（4 行带详细百分比+评级） | S 0.5 天 | A |
| 12 | Draft 审批台 aip-draft-inbox | 0% | 三栏（左任务列表+中详情+右 timeline）+ 4 Tab（概览/变更/评论/审查记录）+ 影响面卡 + 5 步活动 timeline + 批准/驳回 | L 3-5 天 | B |
| 13 | 决策谱系 aip-decision-lineage | 55% | 补 6 段独立阶段（输入/检索/推理/熔断事件/输出/回填）+ 熔断红高亮 + 回填紫高亮 + Token 统计 | M 1-2 天 | A |
| 14 | 可观测性 aip-observability | 50% | 代码编辑器（暗色 Monaco/CodeMirror）+ 安全约束/黑名单/TS 签名 3 卡 + 删除依赖检查（级联 5 项）+ 函数元数据 + 版本历史 | M 2-3 天 | B |
| | **小计** | | | **25-35 天** | |

### B.3 P1 模型管理（4 页）

| # | 页面 | 完整度 | 核心改造点 | 工作量 | Owner |
|---|---|---|---|---|---|
| 1 | 模型目录 aip-model-catalog | 0% | **三层架构定位条**（L1 供应商→L2 路由→L3 目录→AIP，L3 当前蓝高亮）+ 3 Tab（AIP 状态/目录/已注册）+ 目录表格 + 注册流程 | L 3-5 天 | B |
| 2 | 模型供应商 aip-model-providers | 65% | 补三层架构条（L1 高亮）+ **4 健康检查总览卡**（深度求索/Azure/vLLM/Anthropic，p50 + 可用率） | M 1-2 天 | B |
| 3 | 模型路由 aip-model-router | 75% | 补三层架构条（L2 高亮）+ 出境管控列（禁公网/审批后） | S 0.5 天 | A |
| 4 | 容量管理 aip-capacity-management | 0% | 3 Tab（查看使用量/管理速率限制/预留容量）+ Info Banner（20% 保留）+ 项目/用户速率限制双卡 | M 1-2 天 | A |
| | **小计** | | | **8-12 天** | |

### B.4 P1 本体·数字孪生（视觉稿 13 个独立文件；下表按 15 行展开，含与工作台共用的对象探索 + 7 个详情子页）

| # | 页面 | 完整度 | 核心改造点 | 工作量 | Owner |
|---|---|---|---|---|---|
| 1 | 本体管理 Discover ontology | 0% | 窄内容居中 + 收藏 Object 类型网格 + 最近查看列表（4 行）+ 类型分区 + 自定义主页按钮 | M 1-2 天 | A |
| 2 | 对象探索 workshop-object-view | 70% | 视觉细节对齐 | M 1-2 天 | A |
| 3 | 本体提案/漏斗管道 ontology-funnel | 60% | **需求确认**：视觉稿是"提案审核"还是"管道监控"？两者定位不同 | M 1-2 天 | B |
| 4 | 图谱健康度 ontology-graph-health | 80% | 视觉细节对齐 | S 0.5 天 | A |
| 5 | 活知识 Wiki 索引 ontology-wiki-index | 65% | 视觉细节对齐 | M 1 天 | A |
| 6 | OKF funnel funnel | 60% | 视觉细节对齐（视觉稿名"OKF funnel"，系统"OKF 行业漏斗"按视觉稿改） | M 1 天 | A |
| 7 | OKF 概览 okf-funnel | 60% | 视觉细节对齐 | M 1 天 | A |
| 8 | 分支管理 ontology-branches | 70% | 视觉细节对齐 | S-M 0.5-1 天 | A |
| 9 | 对象类型详情 ontology-object | 65% | **重构**：左导航+右卡片纵向流（替代 7-Tab）+ 元数据网格 5→12 项 + 链接可视化图（替代 ASCII）+ 数据质量/异常监控 + 多色 Badge（green/gray/amber/red/blue）| M 1-2 天 | B |
| 10 | 链接类型详情 ontology-link | 35% | **重构**：左侧 4 导航栏 + Join method 三选卡片（FK/Dataset/OT）+ 可视化连线图 + OT A/B 选择器+互换 + Ontology/Status/ID/RID 信息卡 + 扩展字段 joinMethod/foreignKeyFieldA/B/status/rid/properties | L 3-5 天 | B |
| 11 | 属性类型详情 ontology-property | 0% | **属性编辑器**（Properties 13 / Column mapping 双 Tab）+ 数据源控制条（dataset + Show mapped + Automap）+ 属性表+详情面板（5 Tab：General/Display/Interaction/Details/Advanced）+数据预览；新建 property 表 + 5 个 CRUD API | XL 5-8 天 | B |
| 12 | Action 详情 ontology-action | 40% | **重构**：左侧 9 导航栏（Overview/Rules/Parameters/UI/Capabilities/Security/Submission/Automations/History/Observability）+ 描述信息表 + Action overview（Input+Rules 双列）+ Dependents 卡（7 类依赖）+ 扩展字段 description/toolDescription/contributors/status/rid/rules/dependents | L 3-5 天 | B |
| 13 | Function 详情 ontology-function | 0% | 只读提示条 + 左栏（函数名+fx 图标+版本号+3 导航）+ Implementation 卡（仓库链接+文件路径+Class Name）+ Code Preview（行号+语法高亮 6 色）+ Inputs/Output 参数列表；新建 function_type 表 + 2 个只读 API | L 3-5 天 | B |
| 14 | Wiki 详情 ontology-wiki | 20% | 🔴 **视觉稿是全屏 Slate 可视化编辑器**（非简单富文本）：Widget 树+中央画布+右侧属性面板 + Object Set 构建器 + 工作流编排画布（节点+SVG 连线）+ 运行时预览（变量解析）+ 9 Tab 工具栏 + 3 模式切换。**分 3 期实施**：①Widget 树+画布+属性面板 ②Object Set 构建器 ③工作流编排+运行时预览 | **XXL 10-15 天**（分 3 期：4-5d + 3-4d + 3-6d）| B |
| 15 | Wiki 差异 ontology-wiki-diff | 0% | 版本 A/B 选择器 + 视图切换（并排/行内/统一）+ 变更摘要（增 N/删 N/改 N）+ diff 块（diff-add 绿/del 红/mod 黄/same 灰）+ 版本历史时间线 + 恢复确认 Modal；新建 wiki_page_version 表 + 3 个 API | M 2-3 天 | B |
| | **小计** | | | **30-48 天**（v2.2 从 18-25 天上调，主要因 Wiki 详情 XXL + 属性/Action/Link 详情工作量修正）| |

### B.5 P2 管道与数据治理（10 页）

| # | 页面 | 完整度 | 核心改造点 | 工作量 | Owner |
|---|---|---|---|---|---|
| 1 | 管道构建 pipeline-list | 30% | 三栏（左图例 180/中画布/右文件树 280）+ SVG 节点图 + 颜色分组图例 + 文件树联动 + 分支切换 | M 4-5 天 | B |
| 2 | 管道提案 pipeline-proposals | 10% | 3 Tab（Edit/Proposals/History）+ 状态过滤下拉 + 提案卡片列表 + 作者头像 + Discard/Save | S 1-2 天 | A |
| 3 | 计划编辑器 schedules | 30% | 两栏（左沿袭图/右详情 420）+ 运行历史条形图（20 条）+ Cron 表达式 + 时区 + Run/Edit/Pause | M 3-4 天 | B |
| 4 | 搭建 builds | 0% | **注意：视觉稿实际是单个 build status check 配置弹窗**，非列表页；含规则/阈值/严重级别/自动创建问题 | S 1-2 天 | A |
| 5 | 数据集预览 dataset | 40% | 两栏（主区+右信息面板 320）+ 5 Tab（预览/历史/详情/健康/比较）+ 4 统计卡 + 数据表（带类型徽章）+ 右信息面板 | M 3-4 天 | A |
| 6 | 代码库 code-repositories | 10% | 四栏 IDE（仓库列表 256/文件树 208/代码/元数据 224）+ 语法高亮 + 关联资源 + 提案链接 | M 3-4 天 | A |
| 7 | 数据沿袭 lineage | 20% | 两栏（左搜索/属性 280/右主区）+ 全局沿袭图（5 种节点类型）+ 节点展开上下游 + 底部详情条 + 工具条 | M 3-4 天 | B |
| 8 | 数据健康 health | 20% | 4 Tab（全部/检查组/监测中/问题）+ 4 统计卡 + 多维过滤 + 15 行检查表 + 直方图 + 未解决问题卡 | M 4-5 天 | A |
| 9 | DocIntel 管道 pipeline-doc-intel | 0% | 两栏（迷你画布/右配置面板）+ 5 Tab（Configure/Preview/Trial/Input/Output）+ 6 模板卡 + 标签输入 + 可折叠配置区 | M 3-4 天 | B |
| 10 | 管道详情 pipeline | 45% | **DAG 拓扑动态化**（多源 Join，替代固定 3 节点线性）+ 全宽工具栏（撤销/重做/分支/部署）+ 10 变换按钮 + 视图 Tab（编辑/提案/历史）+ 缩放控制（缩小/100%/放大/适应）+ 画布图例（数据集/变换/输出三色）+ 底部预览（含列搜索+相关链接）+ 右 3 类输出（Dataset/Object/Link）+ 协作者头像；新建 pipeline_nodes/pipeline_edges/pipeline_outputs/pipeline_collaborators 表 + 5 个 API | L 5-6 天 | B |
| | **小计** | | | **28-36 天** | |

### B.6 P2 数据源与同步（8 页）

| # | 页面 | 完整度 | 核心改造点 | 工作量 | Owner |
|---|---|---|---|---|---|
| 1 | 数据链接器 data-connection | 40% | 两栏（左分组导航/右主区）+ Sources/Protocol 分组 + 连接器卡片网格 + 能力标签（Batch/Streaming/Virtual/Code） | S 2-3 天 | A |
| 2 | 边缘代理 data-connection-agents | 20% | 两栏（左代理列表 320/右详情）+ 3 列指标卡（内存/CPU/磁盘）+ sparkline + 3 Tab（Sources/Health/Config） | M 3-4 天 | B |
| 3 | 同步配置 sync | 30% | 4 Tab（配置/调度/历史/高级）+ 源/目标选择器 + 字段映射表 + Cron + 增量列 + 重试策略 | M 3-4 天 | A |
| 4 | 同步路由 sync-routing | 20% | 数据源头部 + 4 能力卡片网格 + 现有同步列表 + 文档资源卡片 | S 2-3 天 | A |
| 5 | 媒体集 media-sets | 10% | 3 Tab（浏览/同步/变换）+ 文件网格 + 同步表单 + 变换卡片（含跳转 Pipeline） | S 2-3 天 | A |
| 6 | 文档智能 document-intelligence | 0% | 两栏（左文档卡片网格/右提取字段面板）+ 4 态状态徽章（已提取绿/处理中黄/失败红/待处理灰）+ 导入/模板操作 | M 3-4 天 | B |
| 7 | 数据源新建 source-new | 0% | 4 步向导（连接器→连接方式→基础信息→配置）+ 步骤指示器三态 + 连接器网格 + Agent/Direct 选择 + 双列表单 | S 2-3 天 | A |
| 8 | 数据源详情 source-detail | 35% | 三栏（左 Schema 树 260/中 ER 图+预览/右已选表 280）+ **多级 Schema 树**（schema→表→列，含 PK/FK/类型标注，替代扁平表列表）+ **ER 关系图**（表节点+紫色 FK 虚线连线）+ 数据预览（FK 列紫色+状态着色）+ 已选表清单（含移除/Clear）；新建 source_schemas/source_tables/source_columns 表 + 4 个 schema API；**关键**：表列表从 pipelines 间接派生改为直连 schema | M 4-5 天 | B |
| | **小计** | | | **21-29 天** | |

### B.7 P2 运维交付（8 页）

| # | 页面 | 完整度 | 核心改造点 | 工作量 | Owner |
|---|---|---|---|---|---|
| 1 | Hub 舰队 apollo-hub | 30% | 单栏 6xl + 绿色状态条 Banner（区域+在线 Spoke+最近 Probe）+ Spoke 卡片网格（3 列 5+1 占位）+ Probe/通道/Bundle/形态 | S 2-3 天 | A |
| 2 | Release 通道 apollo-release | 20% | 单栏 4xl + 三段 Pipeline 卡（rc→beta→stable，SVG 箭头）+ Hotfix 卡（红色）+ Recall 卡 + 底部三向导航 | S 2-3 天 | A |
| 3 | Spoke 详情 apollo-spoke | 20% | 单栏 4xl + Callout（轮询间隔+最近同步）+ Full/Lite Tab 切换 + 形态对比双卡 + 部署计划清单 3 行 + Plan Diff | S 2-3 天 | A |
| 4 | Ferry 摆渡 apollo-ferry | 10% | 单栏 3xl（最窄）+ 4 步指示器（Bundle→签名→导出→导入）+ Bundle radio + 气隙说明。**注意：步骤 2-4 视觉稿缺失，B 补设计** | S 2-3 天 | A |
| 5 | FDE 资产包 apollo-assets | 20% | 单栏 5xl + 资产包表格（5 列）+ 4 行示例 + 通道徽章（stable 绿/beta 黄/rc 灰）+ 底部双链接 | S 1-2 天 | A |
| 6 | 变更审批 apollo-change-mgmt | 10% | 双栏（左列表 288/右详情）+ 3 变更单 + 详情卡（4 KV）+ 审批流（3 步流水）+ 批准/驳回按钮 | S 2-3 天 | A |
| 7 | 配置与密钥 apollo-config | 10% | 单栏 3xl + 维护窗口卡（amber，2 列 readonly）+ 覆盖项列表（3 行）+ 安全 Callout（禁明文密钥）+ 保存按钮 | S 2 天 | A |
| 8 | 接入案例 integration-cases | 10% | 单栏 + Header + 6 统计卡 + 端到端链路流水（6 节点）+ 9 平台案例卡（每张含 6 步 mini flow + 5 指标）+ 10 G1-G10 阻塞项。**注意：使用独立 `p-ic-*` 样式前缀，迁移时统一** | M 4-5 天 | A |
| | **小计** | | | **17-22 天** | |

### B.8 工作量汇总（按 owner）

| Owner | 页面工作量 | 后端工作量 | 总计 |
|---|---|---|---|
| A（我） | ~72-80 天 | — | ~72-80 天 |
| B（Buddy） | ~49-73 天（v2.2 上调，因本体 Wiki/属性/Link/Action 详情工作量修正）| ~25-30 天（表+API+种子+引擎）| ~74-103 天 |
| **合计** | ~121-153 天 | ~25-30 天 | **~146-183 天** |

> **口径说明**：
> - 正文 §1.1 "150-212 人天" 是**纯页面工作量**（含设计+开发+联调，未单独算后端），与上表"页面工作量 121-153 天"的差异来自估算上下限取法（B.1-B.7 各分区取上限时合计偏大）。
> - 上表 B 的"后端工作量 25-30 天"拆解：5 天表设计 + 15 天 API 实现（167 个 endpoint）+ 5 天种子数据（~1092 条）。
> - 实际项目周期还包含联调、测试、修复缓冲（约 20%），因此 13 周计划（按 5 工作日/周 = 65 工作日/人，双人 130 工作日）与 146-183 天工作量 + 缓冲基本对齐；如 Wiki 详情 ②③期延期可顺延到 Wave 2。
> - **v2.2 调整**：B 页面工作量从 37-50 天上调到 49-73 天（增量 12-23 天），主要来自 223-deep-checklist-3 揭示的本体详情页真实复杂度。

---

## 附录 C：后端 API 完整清单及周排期

> Owner：全部由 B 实现，A 通过 contracts/*.yaml 调用
> 命名规范：`/v1/{domain}/{resource}`，所有列表支持 `?page=&size=&q=&status=` 通用查询
> 数据隔离：所有写操作按 `org_id + workspace_id` 过滤，从 auth context 获取

### C.1 工作台 + 构建工具（W1-W4）

| API | 方法 | 用途 | 周次 | 依赖表 |
|---|---|---|---|---|
| `/v1/modules` | GET | 模块列表（含 category/last_opened_at） | W1 | modules |
| `/v1/modules/:id` | GET/PUT | 模块详情+元数据 | W1 | modules |
| `/v1/modules/:id/config` | GET/PUT | 画布完整配置 | W3 | module_widgets |
| `/v1/modules/:id/widgets` | GET/POST/PUT/DELETE | 组件实例 CRUD | W3 | module_widgets |
| `/v1/modules/:id/events` | GET/POST/PUT/DELETE | 事件 CRUD | W4 | module_events |
| `/v1/modules/:id/queries` | GET | 查询函数 | W3 | module_queries |
| `/v1/modules/:id/variables` | GET/POST/PUT/DELETE | 变量 CRUD | W4 | module_variables |
| `/v1/modules/:id/variables/:vid/usage` | GET | 变量使用位置 | W4 | module_widgets, module_events |
| `/v1/modules/:id/interface` | GET/PUT | 模块接口定义 | W4 | module_interfaces |
| `/v1/modules/:id/deployments` | GET | 发布历史 | W4 | module_deployments |
| `/v1/modules/:id/deploy` | POST | 发布到指定环境 | W4 | module_deployments |
| `/v1/modules/:id/rollback` | POST | 回滚 | W4 | module_deployments |
| `/v1/widgets` | GET/POST | 组件注册表（按来源筛选） | W4 | widget_registry |
| `/v1/widgets/:id` | GET | 组件详情 | W4 | widget_registry |
| `/v1/themes` | GET/POST | 主题列表/新建 | W4 | themes |
| `/v1/themes/:id` | GET/PUT/DELETE | 主题详情 | W4 | themes |

**合计：16 个 API**

### C.2 AIP 决策引擎（W6-W9）

| API | 方法 | 用途 | 周次 | 依赖表 |
|---|---|---|---|---|
| `/v1/aip/assist/welcome` | GET | AIP 助手欢迎语 | W6 | — |
| `/v1/aip/assist/suggestions` | GET | 建议问题 | W6 | — |
| `/v1/aip/assist/conversations` | GET | 对话历史 | W6 | aip_conversations |
| `/v1/aip/assist/chat` | POST（SSE） | 流式对话 | W6 | — |
| `/v1/aip/agents` | GET | Agent 列表（补 source/tags/calls） | W6 | agents |
| `/v1/aip/agents/:id` | GET/PUT | Agent 详情 | W6 | agents |
| `/v1/aip/agents/:id/prompt` | GET/PUT | Agent 系统提示词 | W7 | agent_prompts |
| `/v1/aip/agents/:id/tools` | GET | Agent 工具列表 | W7 | agent_tools |
| `/v1/aip/agents/:id/guardrails` | GET/PUT | 安全护栏 | W7 | agents |
| `/v1/aip/agent-registry` | GET | 注册表（含统计） | W6 | agents |
| `/v1/aip/agent-import/scan` | POST | 仓库扫描 | W8 | — |
| `/v1/aip/capabilities` | GET | 能力列表 | W6 | capabilities |
| `/v1/aip/capabilities/:id` | PUT | 能力配置 | W6 | capabilities |
| `/v1/aip/capabilities/test` | POST | 能力连通测试 | W6 | — |
| `/v1/aip/capabilities/import/scan` | POST | 能力 Manifest 扫描 | W8 | — |
| `/v1/aip/analyst/query` | POST | NL2Query | W9 | — |
| `/v1/aip/analyst/objects` | GET | Object 检索 | W9 | object_instances |
| `/v1/aip/logic/execute` | POST | 逻辑执行（支持 DAG 分支/汇聚） | W7 | logic_flows |
| `/v1/aip/logic/automations` | GET/POST | 自动化触发器 | W7 | logic_flows |
| `/v1/aip/tools` | GET | 工具目录（7 类） | W7 | — |
| `/v1/aip/tools/config` | GET/PUT | 工具配置 | W7 | agent_tools |
| `/v1/aip/tools/:id/quality` | GET | 工具质量评分（总分+3 子分） | W7 | — |
| `/v1/aip/evals` | GET | Eval 状态（含 l4_allowed） | W7 | evals |
| `/v1/aip/evals/run` | POST | 运行 Eval | W7 | evals |
| `/v1/aip/drafts` | GET | Draft 审查任务列表 | W8 | drafts |
| `/v1/aip/drafts/:id/changes` | GET | Draft 变更内容 | W8 | draft_changes |
| `/v1/aip/drafts/:id/impact` | GET | Draft 影响面（聚合） | W8 | — |
| `/v1/aip/drafts/:id/activity` | GET | Draft 活动历史 | W8 | draft_activities |
| `/v1/aip/drafts/:id/approve` | POST | 批准（状态机） | W8 | drafts |
| `/v1/aip/drafts/:id/reject` | POST | 驳回 | W8 | drafts |
| `/v1/aip/lineage/:id` | GET | Trace（含 6 段：输入/检索/推理/熔断/输出/回填） | W8 | decision_traces |
| `/v1/aip/circuit/trip` | POST | 模拟熔断 | W7 | — |
| `/v1/oma/function-types/:name` | GET | Function 源码+元数据 | W9 | functions |
| `/v1/oma/function-types/:name/tests` | GET | 测试用例 | W9 | function_tests |
| `/v1/oma/function-types/:name/usage` | GET | 依赖引用 | W9 | — |

**合计：35 个 API**

### C.3 模型管理（W5）

| API | 方法 | 用途 | 周次 | 依赖表 |
|---|---|---|---|---|
| `/v1/aip/model-catalog` | GET | 模型目录（可发现） | W5 | model_catalog |
| `/v1/aip/registered-models` | GET | 已注册模型（配额/状态） | W5 | registered_models |
| `/v1/aip/model-catalog/:id/register` | POST | 注册（含配额配置） | W5 | registered_models |
| `/v1/aip/providers` | GET | 供应商列表 | W5 | — |
| `/v1/aip/providers/:id/health` | GET | 健康检查（p50+可用率） | W5 | provider_health |
| `/v1/aip/models` | GET | 模型列表 | W5 | registered_models |
| `/v1/aip/model-routes` | GET/PUT | 路由规则 | W5 | model_routes |
| `/v1/aip/capacity/project-limits` | GET/PUT | 项目速率限制 | W5 | capacity_limits |
| `/v1/aip/capacity/user-limits` | GET/PUT | 用户速率限制 | W5 | capacity_limits |
| `/v1/aip/capacity/usage` | GET | 容量使用量 | W5 | capacity_usage |

**合计：10 个 API**

### C.4 本体·数字孪生（W10-W11）

| API | 方法 | 用途 | 周次 | 依赖表 |
|---|---|---|---|---|
| `/v1/ontology/object-types` | GET | 对象类型列表 | W10 | object_types |
| `/v1/ontology/object-types/:id` | GET/PUT | 对象类型详情 | W10 | object_types |
| `/v1/ontology/object-types/:id/count` | GET | 实例计数 | W10 | object_instances |
| `/v1/ontology/recent` | GET | 最近查看（用户偏好） | W10 | — |
| `/v1/ontology/objects` | GET | 对象列表（支持筛选） | W10 | object_instances |
| `/v1/ontology/objects/:id` | GET | 对象详情 | W10 | object_instances |
| `/v1/ontology/object-types/:id/properties` | GET/POST | 属性 CRUD | W10 | properties |
| `/v1/ontology/object-types/:id/column-mapping` | GET | 列映射 | W10 | column_mapping |
| `/v1/ontology/object-types/:id/automap` | POST | Automap | W10 | — |
| `/v1/ontology/object-types/:id/preview` | GET | 数据预览 | W10 | — |
| `/v1/ontology/branches` | GET/POST | 分支管理 | W10 | — |
| `/v1/ontology/graph-health` | GET | 图谱健康 | W10 | — |
| `/v1/ontology/wikis` | GET | Wiki 索引 | W11 | wikis |
| `/v1/ontology/wikis/:id` | GET/PUT | Wiki 详情 | W11 | wikis |
| `/v1/ontology/wikis/:id/versions` | GET | Wiki 版本历史 | W11 | wiki_versions |
| `/v1/ontology/wikis/:id/diff` | GET | Wiki 版本 diff | W11 | wiki_versions |
| `/v1/ontology/functions/:id` | GET/PUT | Function 详情 | W10 | functions |
| `/v1/ontology/functions/:id/tests` | GET/POST | Function 测试 | W10 | function_tests |
| `/v1/ontology/actions/:id` | GET/PUT | Action 详情 | W11 | — |
| `/v1/ontology/links/:id` | GET/PUT | Link 详情 | W11 | links |

**合计：20 个 API**

### C.5 管道与数据治理（W12-W13）

| API | 方法 | 用途 | 周次 | 依赖表 |
|---|---|---|---|---|
| `/v1/pipelines` | GET | 管道列表 | W13 | pipelines |
| `/v1/pipelines/:id` | GET/PUT | 管道详情 | W13 | pipelines |
| `/v1/pipelines/:id/graph` | GET | 管道节点图 | W13 | pipeline_nodes |
| `/v1/pipelines/:id/files` | GET | 文件树 | W13 | pipeline_nodes |
| `/v1/pipelines/:id/nodes/:nid/preview` | GET | 节点数据预览 | W13 | — |
| `/v1/pipelines/:id/proposals` | GET/POST | 管道提案 | W13 | pipeline_proposals |
| `/v1/pipelines/:id/proposals/:pid/discard` | POST | Discard | W13 | pipeline_proposals |
| `/v1/pipelines/:id/proposals/:pid/merge` | POST | Merge | W13 | pipeline_proposals |
| `/v1/pipelines/:id/history` | GET | 管道历史 | W13 | pipelines |
| `/v1/pipelines/:id/nodes/:nid/config` | GET/PUT | LLM 节点配置 | W13 | llm_node_configs |
| `/v1/pipelines/:id/nodes/:nid/trial-run` | POST | 试运行 | W13 | — |
| `/v1/schedules` | GET/POST | 计划列表 | W13 | schedules |
| `/v1/schedules/:id` | GET/PUT | 计划详情 | W13 | schedules |
| `/v1/schedules/:id/run` | POST | 立即运行 | W13 | schedule_runs |
| `/v1/schedules/:id/pause` | POST | 暂停 | W13 | schedules |
| `/v1/datasets/:id` | GET | 元数据+统计+schema | W13 | datasets |
| `/v1/datasets/:id/preview` | GET | 前 N 行预览 | W13 | — |
| `/v1/datasets/:id/builds` | GET | 构建历史 | W13 | dataset_builds |
| `/v1/datasets/:id/health` | GET | 健康检查 | W13 | health_checks |
| `/v1/datasets/:id/sync-config` | GET | 同步配置 | W13 | syncs |
| `/v1/builds/:id/checks/:cid` | GET/PUT | 搭建状态检查配置 | W13 | — |
| `/v1/repos` | GET | 仓库列表（按语言筛选） | W13 | code_repositories |
| `/v1/repos/:id` | GET | 仓库详情+元数据 | W13 | code_repositories |
| `/v1/repos/:id/files` | GET | 文件树 | W13 | code_files |
| `/v1/repos/:id/files/:path` | GET | 文件内容 | W13 | code_files |
| `/v1/repos/:id/commits` | GET | 提交历史 | W13 | code_repositories |
| `/v1/lineage/search` | GET | 全局搜索 | W13 | lineage_graph |
| `/v1/lineage/graph` | GET | 沿袭图（按节点展开） | W13 | lineage_graph |
| `/v1/lineage/nodes/:id` | GET | 节点属性 | W13 | lineage_graph |
| `/v1/health/checks` | GET | 健康检查（多维筛选） | W13 | health_checks |
| `/v1/health/stats` | GET | 4 统计聚合 | W13 | health_checks |
| `/v1/health/histogram` | GET | 直方图（7 天） | W13 | health_checks |
| `/v1/health/issues` | GET | 未解决问题 | W13 | health_issues |
| `/v1/health/groups` | GET | 检查组 | W13 | health_groups |
| `/v1/models` | GET | 可用模型（LLM 节点用） | W13 | model_catalog |

**合计：34 个 API**

### C.6 数据源与同步（W12）

| API | 方法 | 用途 | 周次 | 依赖表 |
|---|---|---|---|---|
| `/v1/connectors` | GET | 连接器列表（Sources） | W12 | connectors |
| `/v1/protocol-sources` | GET | 协议源列表 | W12 | protocol_sources |
| `/v1/sources` | GET/POST | 数据源列表/新建 | W12 | sources |
| `/v1/sources/:id` | GET/PUT | 数据源详情 | W12 | sources |
| `/v1/sources/test-connection` | POST | 连接测试 | W12 | — |
| `/v1/sources/:id/schemas` | GET | Schema 列表 | W12 | source_tables |
| `/v1/sources/:id/schemas/:s/tables` | GET | 表清单 | W12 | source_tables |
| `/v1/sources/:id/tables/:t/columns` | GET | 列定义（含 PK/FK） | W12 | source_columns |
| `/v1/sources/:id/tables/:t/foreign-keys` | GET | 外键关系 | W12 | source_columns |
| `/v1/sources/:id/tables/:t/preview` | GET | 表数据预览 | W12 | — |
| `/v1/sources/:id/capabilities` | GET | 可用能力 | W12 | connectors |
| `/v1/sources/:id/syncs` | GET | 已配置同步 | W12 | syncs |
| `/v1/sources/:id/documents` | GET | 关联文档 | W12 | documents |
| `/v1/agents` | GET | 边缘代理列表 | W12 | agents |
| `/v1/agents/:id` | GET | 代理详情 | W12 | agents |
| `/v1/agents/:id/metrics` | GET | 实时指标+时序 | W12 | agent_metrics |
| `/v1/agents/:id/sources` | GET | 关联数据源 | W12 | agents |
| `/v1/agents/:id/health` | GET | 健康检查 | W12 | agents |
| `/v1/agents/:id/config` | GET | 配置详情 | W12 | agents |
| `/v1/syncs/:id` | GET/PUT | 同步任务详情 | W12 | syncs |
| `/v1/syncs/:id/runs` | GET | 运行历史 | W12 | sync_runs |
| `/v1/syncs/:id/run` | POST | 立即运行 | W12 | sync_runs |
| `/v1/media-sets/:id` | GET | 媒体集详情 | W12 | media_sets |
| `/v1/media-sets/:id/files` | GET | 文件列表 | W12 | media_files |
| `/v1/media-sets/:id/transformations` | GET | 可用变换 | W12 | — |
| `/v1/documents` | GET | 文档列表（含 status/size） | W12 | documents |
| `/v1/documents/:id/extracted-fields` | GET | 提取字段 | W12 | extracted_fields |
| `/v1/documents/import` | POST | 导入文档 | W12 | documents |
| `/v1/extraction-templates` | GET | 提取模板 | W12 | extraction_templates |
| `/v1/projects` | GET | 项目列表（向导用） | W12 | — |

**合计：30 个 API**

### C.7 运维交付（W11）

| API | 方法 | 用途 | 周次 | 依赖表 |
|---|---|---|---|---|
| `/v1/hub` | GET | Hub 元数据 | W11 | hub |
| `/v1/spokes` | GET | Spoke 列表 | W11 | spokes |
| `/v1/spokes/:id` | GET | Spoke 详情 | W11 | spokes |
| `/v1/spokes/:id/plan` | GET | 部署计划 | W11 | spokes |
| `/v1/spokes/:id/plan-diff` | GET | Plan Diff | W11 | — |
| `/v1/spokes/:id/config` | GET/PUT | 配置覆盖 | W11 | config_overrides |
| `/v1/spokes/:id/maintenance-window` | GET | 维护窗口 | W11 | config_overrides |
| `/v1/releases` | GET | 三段状态（rc/beta/stable） | W11 | releases |
| `/v1/releases/hotfix` | GET | Hotfix 信息 | W11 | releases |
| `/v1/releases/hotfix/push` | POST | 推送 Hotfix | W11 | releases |
| `/v1/releases/recall` | GET | 回滚历史 | W11 | releases |
| `/v1/releases/recall/execute` | POST | 执行回滚 | W11 | releases |
| `/v1/assets` | GET | 资产包列表 | W11 | asset_bundles |
| `/v1/ferry/bundles` | GET | 可 Ferry 的 Bundle | W11 | asset_bundles |
| `/v1/ferry/submit` | POST | Ferry 提交 | W11 | — |
| `/v1/changes` | GET | 变更单列表 | W11 | change_orders |
| `/v1/changes/:id` | GET | 变更单详情+审批流 | W11 | change_orders |
| `/v1/changes/:id/approve` | POST | 批准 | W11 | change_orders |
| `/v1/changes/:id/reject` | POST | 驳回 | W11 | change_orders |
| `/v1/integration-cases/stats` | GET | 6 统计聚合 | W11 | integration_cases |
| `/v1/integration-cases` | GET | 案例列表 | W11 | integration_cases |
| `/v1/integration-cases/blockers` | GET | G1-G10 阻塞项 | W11 | integration_blockers |

**合计：22 个 API**

### C.8 API 数量汇总

| 分区 | 数量 | 周次 |
|---|---|---|
| 工作台 + 构建工具 | 16 | W1-W4 |
| AIP 决策引擎 | 35 | W6-W9 |
| 模型管理 | 10 | W5 |
| 本体 | 20 | W10-W11 |
| 管道与数据治理 | 34 | W12-W13 |
| 数据源与同步 | 30 | W12 |
| 运维交付 | 22 | W11 |
| **总计** | **167** | **13 周分布** |

> 与正文 §6.2 表数量一致；正文 §3.2 "60+ API" 是低估，实际 167 个 endpoint（含 CRUD 展开），W2-W13 持续实现，平均每周 ~13 个 API。

---

## 附录 D：种子数据完整清单及周排期

> Owner：全部由 B 写入 `services/aos-api/aos_api/demo/` 目录
> 数据隔离：所有种子数据写入 `dev-org` 组织 + `dev-project` 工作区，与生产数据完全隔离
> 触发方式：系统启动后单独执行 `python -m aos_api.demo.seed_all`，不与启动流程耦合
> 验收标准：每条数据都能被对应 API 读出，且覆盖视觉稿中出现的所有状态/类型

### D.0 命名规范

- 文件：`seed_{domain}.py`（如 `seed_modules.py`、`seed_aip_agents.py`）
- 函数：`seed_{resource}_{count}()`（如 `seed_widgets_16()`）
- 幂等：所有 seed 函数支持重复执行（先 delete by org_id 再 insert）
- ID 规则：用 `dev-{domain}-{n}` 形式（如 `dev-module-order`），避免与生产 ID 冲突

### D.1 工作台 + 构建工具（W2-W4）

| 种子 | 数量 | 关键字段 | 周次 | 文件 |
|---|---|---|---|---|
| 模块（订单/风控/客户/资产/分析/工单/库存/财务/营销） | 9 | category, last_opened_at, theme | W2 | seed_modules.py |
| 组件注册（12 内置+3 市场+1 自定义） | 16 | source, version, usage_count, icon | W4 | seed_widgets.py |
| 主题预设（浅色/暗色/高对比度） | 3 | config（颜色/字体/间距 JSON）| W4 | seed_themes.py |
| 画布配置（每模块 10+ 组件） | 9 | widget tree, parent_id, sort_order | W3 | seed_module_widgets.py |
| 事件配置（6 触发器×5 模块） | 30 | trigger_type, action_type, idempotency_key | W4 | seed_module_events.py |
| 查询函数（每模块 2-3 条） | 20 | sql/template | W3 | seed_module_queries.py |
| 变量（5 类型分组） | 50 | type, default_value, scope | W4 | seed_module_variables.py |
| 模块接口（每模块 1 条） | 9 | input_schema, output_schema | W4 | seed_module_interfaces.py |
| 发布历史（3 环境×9 模块） | 27 | environment, version, deployed_by | W4 | seed_module_deployments.py |

**合计：173 条 + 9 套画布配置**

### D.2 AIP 决策引擎（W6-W9）

| 种子 | 数量 | 关键字段 | 周次 | 文件 |
|---|---|---|---|---|
| AIP 助手对话 | 3-5 | messages, suggestions | W6 | seed_aip_assist.py |
| Agent 完整配置（提示词+5 工具+护栏） | 11（5 平台+4 插件+2 外部） | source, tags, calls, prompt, guardrails | W6 | seed_aip_agents.py |
| Agent 工具配置（每 Agent 5 工具） | 55 | hitl_status, kind | W7 | seed_agent_tools.py |
| Capabilities 已接入（短视频/直播/电商/教育） | 4 | kind, health, quota, endpoint | W6 | seed_capabilities.py |
| Capabilities 类型说明 | 4 | Media Job/Script Engine/Avatar/HTTP Adapter | W6 | seed_capabilities.py |
| Evals 历史结果 | 42 | pass_rate, l4_allowed, detail_4_rows | W7 | seed_evals.py |
| Draft 审查任务（含变更+影响面+活动） | 4 | status, changes, impact, activity_timeline | W8 | seed_drafts.py |
| 决策 Trace（含检索/推理/熔断/回填） | 5 | stages, tokens, breaker_event, backfill | W8 | seed_decision_traces.py |
| Agent 导入扫描结果 | 3 | framework, entrypoint, deps, runtime, services | W8 | seed_agent_imports.py |
| Capability Manifest 模板（C0/C1/C2） | 3 | runtime, quota, example | W8 | seed_capability_imports.py |
| Function（含源码+测试+依赖） | 5 | source, params, tests, usage | W9 | seed_functions.py |

**合计：~137 条**

### D.3 模型管理（W5）

| 种子 | 数量 | 关键字段 | 周次 | 文件 |
|---|---|---|---|---|
| 模型目录（可发现） | 12 | provider, model, capabilities, context_window, price, status | W5 | seed_model_catalog.py |
| 已注册模型（含配额） | 4 | quota, status, enabled | W5 | seed_registered_models.py |
| 供应商（含健康检查） | 4（深度求索/Azure/vLLM/Anthropic） | name, p50, availability, status（normal/warming/disabled）| W5 | seed_providers.py |
| 路由规则 | 4 | task_type, primary, fallback, outbound（禁公网/审批后）| W5 | seed_model_routes.py |
| 容量使用量统计（30 天） | 30 | date, usage_data | W5 | seed_capacity_usage.py |

**合计：54 条**

### D.4 本体·数字孪生（W10-W11）

| 种子 | 数量 | 关键字段 | 周次 | 文件 |
|---|---|---|---|---|
| Object 类型（Order/Customer/Device/Product/Employee） | 5+ | name, instance_count, indexed, theme_color | W10 | seed_object_types.py |
| Object 实例（每类型 20+） | 100+ | properties, links | W10 | seed_object_instances.py |
| Properties（每类型 10-15） | 50+ | name, type, mapping, format, constraint | W10 | seed_properties.py |
| 列映射（每属性 1 条） | 50+ | source_column, mapped_property, status | W10 | seed_column_mapping.py |
| 分支 | 3-5 | name, parent, status | W10 | seed_branches.py |
| Wiki 卡片 | 10 | object_type, content, version_count | W11 | seed_wikis.py |
| Wiki 版本（每 Wiki 3+） | 30+ | version, diff, author | W11 | seed_wiki_versions.py |
| Function（含参数+测试） | 5 | source, params, tests, version | W10 | seed_ontology_functions.py |
| Action 类型 | 5 | params, submission_criteria, required_markings | W10 | seed_action_types.py |
| Link 类型 | 5 | predicate, cardinality（1:1/1:N/N:M）| W10 | seed_link_types.py |

**合计：~260 条**

### D.5 管道与数据治理（W12-W13）

| 种子 | 数量 | 关键字段 | 周次 | 文件 |
|---|---|---|---|---|
| Pipelines（含节点图） | 5（每含 10+ 节点） | nodes, edges, branches | W13 | seed_pipelines.py |
| Pipeline 提案（3 状态×5 管道） | 15 | status（open/merged/closed）, author | W13 | seed_pipeline_proposals.py |
| Schedules（含运行历史） | 5（每含 20 运行） | cron, last_run, run_history | W13 | seed_schedules.py |
| Datasets（含 schema+预览） | 3 | columns, preview_rows, format | W13 | seed_datasets.py |
| Dataset 构建历史 | 15（每 DS 5 次） | version, status, built_at | W13 | seed_dataset_builds.py |
| Health checks（4 状态分布） | 15 | type, severity（pass/warn/critical/snoozed） | W13 | seed_health_checks.py |
| Health issues | 3 | status, severity | W13 | seed_health_issues.py |
| Health groups | 4 | name, check_ids | W13 | seed_health_groups.py |
| Code repositories | 3 | language, branch, linked_pipeline | W13 | seed_code_repos.py |
| Code files（每仓库 5+） | 15+ | path, content, size | W13 | seed_code_files.py |
| Lineage 节点（5 类型） | 10+ | type（source/dataset/pipeline/object/funnel）, edges | W13 | seed_lineage_graph.py |
| LLM 节点配置 | 1 完整 | template, fields, categories | W13 | seed_llm_node_configs.py |

**合计：~95 条 + 节点图数据**

### D.6 数据源与同步（W12）

| 种子 | 数量 | 关键字段 | 周次 | 文件 |
|---|---|---|---|---|
| Connectors（Sources） | 15 | capabilities, icon, type | W12 | seed_connectors.py |
| Protocol sources | 5 | capabilities | W12 | seed_protocol_sources.py |
| Sources | 5 | type, status（connected/error） | W12 | seed_sources.py |
| Source schemas | 10（每 Source 2 schema） | name | W12 | seed_source_tables.py |
| Source tables | 50（每 Schema 5 表） | columns, FK | W12 | seed_source_tables.py |
| Source 表预览数据 | 40 行（每表 8 行） | — | W12 | seed_source_preview.py |
| Agents（边缘代理） | 3 | status, version, ip, resource_summary | W12 | seed_agents.py |
| Agent metrics 时序 | 90（3 Agent×30 天） | cpu, mem, disk, sparkline | W12 | seed_agent_metrics.py |
| Syncs | 5 | source, target, mapping, schedule | W12 | seed_syncs.py |
| Sync runs | 25（每 Sync 5 次） | status, duration, started_at | W12 | seed_sync_runs.py |
| Media sets | 2 | files_count, transformations | W12 | seed_media_sets.py |
| Media files | 20（每 MS 10 文件） | thumbnail, size, type | W12 | seed_media_files.py |
| Documents（4 态覆盖） | 10（已提取/处理中/失败/待处理 各覆盖）| status, size, title | W12 | seed_documents.py |
| Extracted fields | 50+（每文档 5+） | name, type, value | W12 | seed_extracted_fields.py |
| Extraction templates | 3 | name, fields_schema | W12 | seed_extraction_templates.py |

**合计：~330 条 + 时序数据**

### D.7 运维交付（W11）

| 种子 | 数量 | 关键字段 | 周次 | 文件 |
|---|---|---|---|---|
| Hub | 1 | region, online_spokes, last_probe | W11 | seed_hub.py |
| Spokes（覆盖各健康状态） | 5 | health（online/degraded/offline）, probe, channel, bundle, spoke_type | W11 | seed_spokes.py |
| Releases 三段 | 3（rc/beta/stable） | version, status | W11 | seed_releases.py |
| Hotfix | 1 | patch_version, cve, description | W11 | seed_releases.py |
| Recall 历史 | 1 | from_version, to_version | W11 | seed_releases.py |
| Asset bundles（覆盖各通道） | 4 | semver, channel（stable/beta/rc）, content_types, status | W11 | seed_asset_bundles.py |
| Change orders（覆盖各状态） | 3 | type, status（pending/approved/rejected）, approval_steps | W11 | seed_change_orders.py |
| Config overrides | 3 | key（aip.model.default/db.connection.poolSize/integration.apiKey）, value | W11 | seed_config_overrides.py |
| Maintenance window | 1 | start, end | W11 | seed_config_overrides.py |
| Integration cases（9 平台） | 9（微商城/淘宝/拼多多/京东/抖音/Shopify/跨境/Amazon/天猫）| tag, connector, steps（6）, metrics（5）, status | W11 | seed_integration_cases.py |
| Integration blockers G1-G10 | 10 | title, severity, owner | W11 | seed_integration_blockers.py |
| Ferry bundles | 2 | name, size, signable | W11 | seed_ferry_bundles.py |

**合计：43 条**

### D.8 种子数据汇总

| 分区 | 条数 | 周次 |
|---|---|---|
| 工作台 + 构建工具 | 173 + 9 套画布 | W2-W4 |
| AIP 决策引擎 | ~137 | W6-W9 |
| 模型管理 | 54 | W5 |
| 本体 | ~260 | W10-W11 |
| 管道与数据治理 | ~95 + 节点图 | W12-W13 |
| 数据源与同步 | ~330 + 时序 | W12 |
| 运维交付 | 43 | W11 |
| **总计** | **~1092 条 + 画布/节点图/时序** | **13 周持续** |

> 平均每周 ~85 条种子，B 在 W2/W5/W6/W8/W10/W11/W12/W13 各有种子产出，与 §3.2 周计划一致。

---

## 附录 E：每页验收 checklist

> 每页必须 6 项全 ✅ 才算完成；P0/P1 重点页另有专项验收点

### E.1 通用验收维度（每页必做）

- [ ] **视觉对齐**：与视觉稿 1:1 还原（布局/间距/色值/字体/圆角）
- [ ] **功能完整**：所有交互可用（点击/切换/弹窗/筛选/拖拽/保存）
- [ ] **数据驱动**：内容从 API 拉取，无写死字符串/数组
- [ ] **路由可达**：nav 项可点击进入，不跳首页、不白屏
- [ ] **主题适配**：暗色/浅色都正常（包括 hover/选中/禁用态）
- [ ] **错误降级**：API 失败有 fallback（空状态/重试按钮），不白屏不卡死

### E.2 P0 重点页（必须 100% 对齐）

| 页面 | 关键验收点 |
|---|---|
| 画布编辑 workshop-canvas | 三栏布局 + 9 pop-panel 全部可展开 + 拖拽组件到画布 + 4 Tab 属性面板（内容/样式/事件/数据）+ 工作流模式切换 + 保存生效 |
| 组件注册表 | 4 来源 Tab 切换 + 3 列卡片网格 + 点击卡片弹出详情 + 使用数动态（与画布实例数一致）|
| 变量管理器 | 两栏联动 + 5 类型分组（string/number/boolean/object/array）+ 类型动态表单（不同类型不同控件）+ 使用位置联动 |
| 主题与样式 | 两栏 + 主题编辑器 3 Tab（颜色/字体/间距）+ 颜色选择器（取色器+色板）+ 实时预览生效（改色立即更新）|
| 事件配置 | 上列表展示 + 下 5 步向导 + 6 触发器卡片单选 + 5 动作卡片单选 + 动态参数表单 + 预览卡片 |
| 模块接口 | input/output 接口卡 + 嵌套 Loop 示意图（父 Module→子 Loop→子 Module）+ 蓝色提示条 |
| 发布入口 | 4 环境步骤条（开发→测试→预发布→生产）+ 环境卡片状态实时 + 发布/回滚按钮可用 |
| 应用列表 | 最近使用区 + 全部应用区 + 9 分类筛选联动 + 模块卡片点击进入画布 |

### E.3 P1 重点页

| 页面 | 关键验收点 |
|---|---|
| AIP 助手 | 流式 SSE 渐进渲染（字符级流式）+ 建议卡点击填入输入框 + 权限感知标签显示 + 取消/保存到分支可用 |
| 对话机器人 | 左 256 Agent 列表 + 右 4 Tab（提示词/工具箱/试运行/发布）+ 4 步创建向导 Modal + HITL 标签（确认中黄）+ 工具颜色（已开启绿/推荐橙）|
| AIP 逻辑画布 | 分支 Block（双路：红高风险/绿低风险）+ 汇聚 Handoff 节点 + 决策摘要/产物列表/开放问题配置区 + 预览运行结果 |
| 智能体目录 | 表格改 3 列卡片网格 + 来源 Tab（全部/平台/插件/外部）+ 4 统计数字 + source/tags/calls 字段显示 |
| 智能体插件 | 4 已接入能力卡（绿色边框）+ 4 可接入类型卡 + 点击配置弹表单 + 连通测试按钮 |
| Draft 审批台 | 三栏（任务列表+详情+timeline）+ 4 Tab（概览/变更/评论/审查记录）+ 影响面卡片 + 5 步活动 timeline + 批准/驳回状态转移 |
| 模型目录 | 三层架构定位条（L3 当前蓝高亮，可跳转 L1/L2/AIP）+ 3 Tab 切换 + 目录表格（供应商/模型/能力/上下文/价格/状态）+ 注册流程弹窗 |
| 属性类型详情 | Properties/Column mapping 双 Tab + 数据源控制条（dataset + Show mapped + Automap）+ 属性表行选中联动详情面板 + Automap 按钮可用 + 数据预览 |
| Wiki 详情/差异 | 富文本编辑（粗体/斜体/链接/列表）+ 属性关联 + 版本历史时间线 + diff 视图左右对比 + 变更高亮 |

### E.4 P2 重点页

| 页面 | 关键验收点 |
|---|---|
| 管道构建 pipeline-list | 三栏 + SVG 节点图（矩形+连线）+ 颜色图例 + 文件树联动（点击节点高亮文件）+ 分支切换 |
| 管道详情 pipeline | 两栏 + 10 变换工具按钮（Filter/Join/Aggregate/Explode/Cast/Union/Sort/Distinct/Expression/Window）+ SVG 画布节点可选中 + 缩放控制 + 右侧 3 类输出（Dataset/Object/Link）|
| 数据沿袭 lineage | 全局沿袭图（5 种节点类型）+ 节点展开上下游（箭头按钮）+ 底部详情条 + 左侧 4 Tab 侧栏（搜索/属性/搭建/计划）|
| 数据源详情 source-detail | 三栏 + Schema 树折叠展开 + 表关系图 SVG（FK 紫色高亮）+ 数据预览（粘性表头）+ 已选表清单联动 |
| 数据健康 health | 4 Tab + 4 统计卡（通过/告警/严重/打盹中）+ 多维过滤（状态/类型/严重性）+ 15 行检查表 + 直方图（7 天）+ 未解决问题卡 |
| 边缘代理 | 两栏 + 3 列指标卡（内存/CPU/磁盘）+ sparkline 迷你图 + 3 Tab（Sources/Health/Config）|
| 接入案例 | 6 统计卡 + 端到端链路流水（6 节点）+ 9 平台案例卡（每张 6 步 mini flow + 5 指标）+ 10 阻塞项网格 |

### E.5 最终验收（W13 末）

- [ ] 66 个页面全部按视觉稿对齐（含 16 个缺失页）
- [ ] 167 个 API 全部联调通过
- [ ] ~1092 条种子数据全部写入并校验
- [ ] 8 处名字差异全部按视觉稿统一
- [ ] 全站品牌色 `#0F6E56` 推广完成
- [ ] 全站回归测试通过（前端单测 + 后端 pytest + E2E）
- [ ] 暗色/浅色主题切换全站无异常

---

## 附录 F：技术风险与缓解详细表

### F.1 高风险（H 级，可能阻塞）

| # | 风险 | 影响范围 | 触发条件 | 缓解措施 | Owner |
|---|---|---|---|---|---|
| H1 | workshop-canvas 拖拽编辑器延期 | 阻塞 P0 全部 | 复杂度高（三栏+9 pop-panel+工作流模式）| W3-W4 集中攻坚，不并行其他复杂页；先做组件树+画布+属性面板三件套 MVP，9 pop-panel 用 lazy mount 按需加载 | B |
| H2 | pipeline.html 两栏画布编辑器延期 | 阻塞 P2 管道 | 10 变换工具+SVG 节点 | W13 单独排期；**复用 workshop-canvas 抽出的 `BpCanvasEditor` 共享组件**；变换工具先做静态按钮，DAG 拖拽后续迭代 | B |
| H3 | AIP 助手流式 SSE 不稳定 | 阻塞 AIP-01 | LLM 长连接+断线重连+Nginx buffer | 用 `fetch + ReadableStream` 实现（不用 EventSource，避免 GET 限制）；封装 `BpStreamChat` 组件含自动重连；服务端 Nginx `proxy_buffering off` | B |
| H4 | Draft 审批三栏交互复杂 | 阻塞 AIP-12 | 三栏联动+审批状态机+diff 渲染 | 后端先做状态机（draft→review→approved/rejected）+ 幂等键；前端拆 3 个独立组件（DraftList/DraftDetail/ActivityTimeline），分别 storybook 测试再合并 | B |
| H5 | 属性 Automap 算法不准 | 影响 ONT-11 准确率 | 列名匹配模糊（中英文/缩写/同义词）| V1 先做基于精确匹配 + 别名表（hardcoded mapping）的规则引擎；V2 引入 ML 模型迭代；前端始终显示"待确认"状态供人工修订 | B |
| H6 | API 契约不对齐返工 | 全局影响 | schema 漂移、字段命名不一致 | W1 必须完成所有契约 review；`services/aos-api/contracts/*.yaml` 进 git；CI 加 OpenAPI spec 校验；契约变更必须 PR 双人 review | A+B |
| H7 | 后端表设计返工 | 全局影响 | 字段缺失、索引不足、外键设计错 | W1 集中设计；所有表强制四件套（`created_at/updated_at/org_id/workspace_id`）；用 PR 模板 review（含字段说明+索引+迁移脚本）| B |
| H8 | 品牌色 `#0F6E56` 推广影响视觉一致性 | 全局影响 | 视觉稿用 indigo `#4F46E5`，系统需统一品牌色 | W2 先做共享组件层（BpBadge/BpCard/BpToolbar）统一 brand tokens；视觉稿不改但系统统一引用 `var(--bp-brand)`；过渡期允许两色共存，W13 末统一 | A |

### F.2 中风险（M 级，需关注）

| # | 风险 | 影响范围 | 缓解措施 | Owner |
|---|---|---|---|---|
| M1 | AIP 分析师地图集成延期 | AIP-03 | 用 Leaflet 开源版（无需 token）；先做静态 marker + cluster，地图样式后续迭代；Mapbox 作为 V2 升级 | B |
| M2 | 代码编辑器 Monaco 体积大（~2MB）| 影响首屏 LCP | lazy import + 单独 chunk；评估用 CodeMirror 6 替代（更轻 ~600KB）；封装 `BpCodeEditor` 统一接口 | A |
| M3 | sparkline 性能（多代理×多指标）| 边缘代理 | 用 SVG 手绘 mini chart（不引图表库）；数据按分钟聚合，前端 60s 轮询一次；最多展示 30 个点 | A |
| M4 | Cron 输入组件 | schedules/同步配置 | 抽 `BpCronInput` 共享组件（W13 完成）；支持可视化选择 + 手动输入 + 校验 + 下次运行时间预测 | A |
| M5 | Diff 渲染（Wiki 版本对比）| Wiki 差异 | 用 `diff-match-patch` 库（Google 出品，体积小）；先做行级 diff，字级 diff 作为 V2 | A |
| M6 | YAML 实时预览 | 能力导入 | 用 `js-yaml` 序列化 + 自写高亮（基于 prismjs）；表单字段 change → YAML 实时更新 | A |
| M7 | 状态机测试覆盖不足 | Draft/变更审批 | 后端单测覆盖所有状态转移路径；前端用 storybook 验证每个状态 UI；E2E 测试 happy path | B |
| M8 | 实时指标时序数据量大 | 边缘代理 | 后端按分钟聚合存 `agent_metrics` 表；保留 30 天，超出归档；前端 sparkline 只取最近 30 点 | B |
| M9 | Ferry 步骤 2-4 无视觉稿 | Ferry 摆渡 | W11 B 补设计稿（参考 4 步向导通用模板）；步骤 2（签名校验）+ 步骤 3（导出介质）+ 步骤 4（目标 Spoke 导入）UI 简化 | B |
| M10 | builds.html 实际是配置弹窗 | 搭建页 | **与产品确认**是否需要补"搭建历史列表页"视觉稿；当前按配置弹窗实现，列表页作为 V2 | A |
| M11 | 接入案例样式前缀独立（`p-ic-*`）| 接入案例 | 迁移时统一为 `bp-ic-*` 前缀，遵循 BEM 规范；保留原结构，仅替换 class 名 | A |
| M12 | 表关系图 SVG 复杂度（source-detail）| 数据源详情 | 用 `<svg>` + 简单矩形+连线（不引 react-flow）；FK 连线紫色高亮；表节点可拖拽重排 | B |

### F.3 并行冲突缓解（强约束）

| 冲突点 | 解决方案 | 强制度 |
|---|---|---|
| 同时改 `apps/web/src/nav.ts` | W1 由 A 一次性改完（含 14 个缺失路由注册），之后冻结，任何改动走 PR | 🔴 必须 |
| 同时改 `apps/web/src/App.tsx` 路由 | W1 由 A 一次性改完；路由按分区拆分（`aipRoutes.ts`/`ontologyRoutes.ts`/`dataRoutes.ts`/`apolloRoutes.ts`），各自维护 | 🔴 必须 |
| 改共享组件 `apps/web/src/components/bp/` | **只允许 A 修改**；B 如需新组件提 issue 给 A | 🔴 必须 |
| 改后端 schema `services/aos-api/aos_api/store/` | **只允许 B 修改**；A 如需新字段提 PR 给 B（含字段说明+迁移脚本）| 🔴 必须 |
| 改种子数据 `services/aos-api/aos_api/demo/` | **只允许 B 修改**；A 如需测试数据提 issue 给 B（含数据规格）| 🔴 必须 |
| 改 API 契约 `services/aos-api/contracts/` | **A+B 共同 review**，进 git，CI 校验 OpenAPI spec | 🟡 必须 |
| 改 i18n 文件 | 由 A 统一维护（避免 key 冲突）| 🟡 推荐 |
| 改 `package.json` 加新依赖 | 必须提 PR 说明用途+体积评估；超过 200KB 需评估替代方案 | 🟡 必须 |

### F.4 风险监控节奏

| 时间点 | 检查项 | 责任人 |
|---|---|---|
| 每周末 | 风险表 review，新增风险登记 | A+B |
| W2 末 | 契约层 review（H6 验收）| A+B |
| W4 末 | workshop-canvas MVP demo（H1 验收）| B |
| W6 末 | AIP 助手 SSE 联调（H3 验收）| B |
| W8 末 | Draft 状态机单测覆盖（H4 验收）| B |
| W10 末 | Automap 准确率（H5 验收，目标 ≥80%）| B |
| W13 末 | 全量回归 + 品牌色统一（H8 验收）| A+B |

---

## 附录 G：全文一致性核对

> 用途：自检全文数字、口径、周排期是否自洽；每次更新文档后必须复核
> 核对日期：2026-07-26

### G.1 页数核对

| 分区 | §1.1 总表 | 附录 B 实际行数 | 备注 |
|---|---|---|---|
| P0 工作台 + 构建工具 | 9 | 9（B.1）| ✅ 一致（含模块管理系统多出项） |
| P1 AIP 决策引擎 | 14 | 14（B.2）| ✅ 一致 |
| P1 模型管理 | 4 | 4（B.3）| ✅ 一致 |
| P1 本体 | 13 | 15 行（B.4）| ⚠️ 视觉稿 13 个独立文件，B.4 按 15 行展开（含 1 个与工作台共用 + 7 个详情子页）|
| P2 管道 | 10 | 10（B.5）| ✅ 一致（含 pipeline 详情）|
| P2 数据源 | 8 | 8（B.6）| ✅ 一致（含 source-detail 详情）|
| P2 运维 | 8 | 8（B.7）| ✅ 一致（不含 3 个系统多出项）|
| **总计** | **66** | **66-68**（按行计略有差异）| ✅ 总数与 §1.1 一致 |

### G.2 工作量核对

| 分区 | §1.1 估算 | 附录 B 小计 | 差异说明 |
|---|---|---|---|
| P0 | 22-32 天 | 22-32 天（B.1）| ✅ 完全一致 |
| P1 AIP | 25-35 天（含在 P1 合计）| 25-35 天（B.2）| ✅ 一致 |
| P1 模型 | 8-12 天（含在 P1 合计）| 8-12 天（B.3）| ✅ 一致 |
| P1 本体 | 30-48 天（含在 P1 合计）| 30-48 天（B.4）| ✅ 一致（v2.2 已按 223-deep-checklist-3 上调）|
| P1 合计 | 63-95 天 | 63-95 天 | ✅ 一致（v2.2）|
| P2 管道 | 28-36 天（含在 P2 合计）| 28-36 天（B.5）| ✅ 一致 |
| P2 数据源 | 21-29 天（含在 P2 合计）| 21-29 天（B.6）| ✅ 一致 |
| P2 运维 | 17-22 天（含在 P2 合计）| 17-22 天（B.7）| ✅ 一致 |
| P2 合计 | 65-85 天 | 66-87 天 | ⚠️ 误差 ±1-2 天（四舍五入）|
| **总计** | **150-212 天** | **151-214 天** | ✅ 误差范围内一致（v2.2）|

### G.3 API 数量核对

| 分区 | 附录 C | §3.2 周计划描述 | 备注 |
|---|---|---|---|
| 工作台 + 构建工具 | 16 | — | W1-W4 |
| AIP 决策引擎 | 35 | — | W6-W9 |
| 模型管理 | 10 | — | W5 |
| 本体 | 20 | — | W10-W11 |
| 管道与数据治理 | 34 | — | W12-W13 |
| 数据源与同步 | 30 | — | W12 |
| 运维交付 | 22 | — | W11 |
| **总计** | **167** | "60+ 个新 API"（§2.3 + §6）| ⚠️ §2.3/§6 "60+" 是低估，附录 C 实际 167（含 CRUD 展开），以附录 C 为准 |

### G.4 种子数据核对

| 分区 | 附录 D 条数 | §3.2 周计划描述 | 备注 |
|---|---|---|---|
| 工作台 + 构建工具 | 173 + 9 套画布 | "种子数据 1（module/widget/theme/connectors）"（W2）+ "种子数据 2（订单/风控/对象实例）"（W4）| ✅ W2 + W4 分批 |
| AIP 决策引擎 | ~137 | 未明确数量 | W6-W9 持续 |
| 模型管理 | 54 | 未明确 | W5 |
| 本体 | ~260 | 未明确 | W10-W11 |
| 管道与数据治理 | ~95 + 节点图 | 未明确 | W12-W13 |
| 数据源与同步 | ~330 + 时序 | 未明确 | W12 |
| 运维交付 | 43 | 未明确 | W11 |
| **总计** | **~1092** | "5 天"（§2.3 B 任务）| ✅ 5 天写 ~1092 条可行（每条约 2-3 分钟）|

### G.5 周排期核对

| 周 | §3.2 A 任务 | §3.2 B 任务 | 附录 B/C/D 对应 |
|---|---|---|---|
| W1 | 名字统一 + 路由骨架 + 14 缺失页 | 表设计 + 契约文档 | B.1（P0 启动）+ C.1（W1 部分）|
| W2 | P2 运维简单页 + 共享组件 | 建表 + 种子 1 + 基础 API | B.7（运维）+ D.1（部分）|
| W3 | 应用列表 + 风险告警 + 创建应用 | workshop-canvas + 画布 API | B.1（画布）+ C.1（W3）|
| W4 | 组件/变量/主题/事件/发布 | canvas 收尾 + 模块接口 + 种子 2 | B.1（剩余）+ D.1（W4）|
| W5 | 模型路由 + 容量 + BpArchBar | 模型目录 + 供应商 + 模型 API | B.3 + C.3 + D.3 |
| W6 | 智能体目录/插件/成熟度 | AIP 助手 + 流式 API | B.2（部分）+ C.2（W6）+ D.2（W6）|
| W7 | 对话机器人/工具/Evals | 逻辑画布 + LogicEngine | B.2（部分）+ C.2（W7）+ D.2（W7）|
| W8 | 智能体导入/能力导入/决策谱系 | Draft 审批台 + Draft API | B.2（部分）+ C.2（W8）+ D.2（W8）|
| W9 | 代码/diff 共享组件 | 可观测性 + AIP 分析师 + NL2Query | B.2（剩余）+ C.2（W9）+ D.2（W9）|
| W10 | 本体 Discover/对象探索/分支等 | 属性详情 + Function 详情 | B.4 + C.4（W10）+ D.4（W10）|
| W11 | P2 运维 8 页 | Wiki 详情 ①期 + Wiki 差异 + Action/Link/Object 详情 | B.7 + C.4（W11）+ C.7 + D.4（W11）+ D.7 |
| W12 | 数据源 5 页（A）+ BpSparkline/BpCronInput | 数据源详情 + 边缘代理 + 文档智能 + Wiki ②期（副线）| B.6 + C.6 + D.6 |
| W13 | 管道提案/数据集/健康/搭建 | pipeline/pipeline-list/lineage/schedules/DocIntel/代码库 + Wiki ③期（缓冲）| B.5 + C.5 + D.5 |

> ✅ 周排期与附录 B/C/D 对应正确；A 与 B 在 W3 之后基本完全并行。
> ⚠️ v2.2 Wiki 详情分 3 期跨 W11/W12/W13，②期③期为副线/缓冲，如延期可顺延到 Wave 2 不影响主线验收。

### G.6 Owner 分工核对

| 维度 | A 负责 | B 负责 | 共同 |
|---|---|---|---|
| 页面（附录 A） | 35 页（W3-W13）| 31 页（W3-W13）| — |
| 后端表（§6.2） | — | 58 张表 | — |
| 后端 API（附录 C） | — | 167 个 | — |
| 种子数据（附录 D） | — | ~1092 条 | — |
| 共享组件（§5） | 10 个 | — | — |
| API 契约（§4） | — | — | W1 共同 review |
| 品牌色统一 | 实施 | — | — |
| 名字统一（8 处） | 实施 | — | — |

### G.7 关键约束自检

| 约束 | 状态 | 出处 |
|---|---|---|
| 每个数据库表只一方维护 | ✅ 全部 B | §6.1 + 附录 F.3 |
| 每个前端目录只一方修改 | ✅ 按 owner 分（A: 列表/详情/配置；B: 画布/三栏/编辑器）| §2.3 |
| API 契约先于实现 | ✅ W1 完成所有契约 review | §4.2 + 附录 F.1 H6 |
| 共享组件由 owner 抽取 | ✅ A 抽取 10 个 | §5 |
| 种子数据统一管理 | ✅ B 写入 demo/ 目录 | §2.1 + 附录 D |
| nav.ts/App.tsx 谁改 | ✅ A 一次性改完（W1）| 附录 F.3 |
| 14 缺失页路由注册 | ✅ A 在 W1 注册 | §3.2 W1 |

### G.8 待确认事项（沿用 §10）

| # | 事项 | 默认假设 | 确认状态 |
|---|---|---|---|
| 1 | 分工方案（A 页面前端 + B 后端/复杂前端）| 同意 | ⏳ 待用户确认 |
| 2 | 13 周周期 | 同意 | ⏳ 待用户确认 |
| 3 | W1 集中契约 review | 同意 | ⏳ 待用户确认 |
| 4 | 共享组件 A 统一维护 | 同意 | ⏳ 待用户确认 |
| 5 | 种子数据 B 统一管理 | 同意 | ⏳ 待用户确认 |
| 6 | W3 起双方完全并行 | 同意 | ⏳ 待用户确认 |
| 7 | 本体提案 vs 漏斗管道 是否同义页 | 同义，按视觉稿统一改名 | ⏳ 待用户确认（B.4 #3）|
| 8 | builds.html 是否需要补列表页 | 当前按配置弹窗实现 | ⏳ 待产品确认（F.2 M10）|
| 9 | Ferry 步骤 2-4 视觉稿 | B 在 W11 补设计 | ⏳ 待用户确认（F.2 M9）|
| 10 | AIP 助手品牌色（紫蓝渐变 `#6366f1→#8b5cf6`）是否统一为品牌深绿 | 视觉稿原文保留紫蓝（与品牌色 H8 冲突），建议助手气泡保留紫蓝作为 AI 强调色，其余统一品牌绿 | ⏳ 待用户确认（H3 + 223-deep-checklist-2 AIP-01）|
| 11 | AIP 逻辑画布 KIND_COLORS 色值与视觉稿不完全一致 | 系统已有颜色映射，但色值与视觉稿存在偏差；建议按视觉稿（蓝输入/紫取属性/黄 LLM/红高分/绿低分）统一 | ⏳ 待用户确认（223-deep-checklist-2 AIP-04 §5）|
| 12 | 接入案例 `p-ic-*` 样式前缀是否在本期统一迁移 | 默认迁移为 `bp-ic-*`（BEM 规范），但接入案例 9 平台卡片信息密度极高，迁移存在视觉回归风险 | ⏳ 待用户确认（F.2 M11）|
| 13 | Wiki 详情 XXL 10-15d 是否同意分 3 期跨 W11/W12/W13 实施 | v2.2 已拆 3 期，②③期作为副线/缓冲；如不同意可降级为简单富文本编辑器（M 2d），后续 Wave 再补 Slate 编辑器 | ⏳ 待用户确认（B.4 #14 + W11/W12/W13）|

---

## 附录 H：跨页面依赖矩阵与关键路径

> 数据来源：`223-deep-checklist.md` §7 + `223-deep-checklist-2.md` 各页"组件依赖/其他依赖" + `223-deep-checklist-3.md` 各页"风险与依赖"
> 用途：双人并行开发时**避免阻塞**的强约束；任何依赖项必须先于被依赖项完成
> 强度图例：🔴 强依赖（被依赖项未完成则本页无法验收）/ 🟡 弱依赖（可临时 mock，后续联调）

### H.1 P0 内部依赖（W3-W4）

| 依赖项（先完成） | 被依赖页（后完成） | 强度 | 说明 | 出处 |
|---|---|---|---|---|
| 组件注册表（A，W4）| 画布编辑器-组件面板（B，W3-W4）| 🔴 | 画布的"组件 Tab"数据来源；B 在 W3 先用 mock，W4 末联调真实数据 | 223-deep-checklist §7.1 + §7.7 |
| 变量管理器（A，W4）| 画布编辑器-变量 Tab（B，W3-W4）| 🔴 | 画布的"变量 Tab"数据来源；同上 mock 策略 | 223-deep-checklist §7.1 + §7.8 |
| 主题与样式（A，W4）| 画布编辑器-样式 Tab（B，W3-W4）| 🔴 | 画布的"样式 Tab"数据来源；同上 mock 策略 | 223-deep-checklist §7.1 + §7.9 |
| 事件配置（A，W4）| 画布编辑器-事件 Tab（B，W3-W4）| 🟡 | 画布的"事件 Tab"数据来源；事件相对独立可后联调 | 223-deep-checklist §7.1 + §7.3 |
| 画布编辑器 MVP（B，W3 末）| 应用列表"打开应用"入口（A，W3）| 🟡 | 应用列表点击进入画布；MVP 完成即可联调 | 223-deep-checklist §7.1 |

**关键路径**：W3 由 B 集中攻坚画布 MVP，A 同步做应用列表/风险告警/创建应用；W4 A 集中做组件/变量/主题/事件 4 页，B 收尾画布并做模块接口。

### H.2 P1 内部依赖（W5-W11）

| 依赖项（先完成） | 被依赖页（后完成） | 强度 | 说明 | 周次 |
|---|---|---|---|---|
| `BpArchitectureBar` 共享组件（A，W5 初）| 模型供应商（B，W5）| 🔴 | 三层架构条 L1 高亮 | W5 |
| `BpArchitectureBar` 共享组件（A，W5 初）| 模型路由（A，W5）| 🔴 | 三层架构条 L2 高亮 | W5 |
| `BpArchitectureBar` 共享组件（A，W5 初）| 模型目录（B，W5）| 🔴 | 三层架构条 L3 高亮；**3 页必须用同一组件**，否则视觉不一致 | W5 |
| 模型供应商 + 路由（W5）| 模型目录三层架构跳转（W5）| 🟡 | 模型目录的三层架构条点击可跳 L1/L2，需对方页面就绪 | W5 |
| Agent 工具面板（A，W7）| 对话机器人"工具箱 Tab"（A，W7）| 🟡 | 同 owner，无并行风险，仅顺序约束 | W7 |
| Evals 门控（A，W7）| 对话机器人"发布 Tab"（A，W7）| 🟡 | 同 owner，仅顺序约束 | W7 |
| 能力导入（A，W8）| 智能体插件（A，W6）| 🔴 | **顺序倒置**：智能体插件依赖能力导入的扫描结果；但 W6 早于 W8 → **需调整**：智能体插件先用静态 mock 数据，W8 能力导入完成后联调 | W6 + W8 |
| `BpCodeEditor` 共享组件（A，W9 初）| 可观测性（B，W9）| 🔴 | 可观测性的代码编辑器必须用 `BpCodeEditor` | W9 |
| `BpCodeEditor` 共享组件（A，W9 初）| Function 详情（B，W10）| 🔴 | Function 详情的代码编辑器必须用 `BpCodeEditor` | W9-W10 |
| `BpDiffViewer` 共享组件（A，W9 初）| Wiki 差异（B，W11）| 🔴 | Wiki 差异的 diff 渲染必须用 `BpDiffViewer` | W9-W11 |
| AIP 助手流式 SSE API（B，W6）| AIP 分析师聊天区（B，W9）| 🟡 | 同 owner，复用 SSE 实现；可并行 | W6 + W9 |
| LogicEngine DAG 分支（B，W7）| AIP 逻辑画布分支 Block（B，W7）| 🔴 | 同 owner，后端先行前端跟进 | W7 |

**关键路径**：W5 第一天 A 必须先抽 `BpArchitectureBar`（3 个模型页强依赖）；W9 第一天 A 必须先抽 `BpCodeEditor` + `BpDiffViewer`（可观测性/Function 详情/Wiki 差异 3 页强依赖）。

### H.3 P2 内部依赖（W11-W13）

| 依赖项（先完成） | 被依赖页（后完成） | 强度 | 说明 | 周次 |
|---|---|---|---|---|
| `BpSparkline` 共享组件（A，W12 初）| 边缘代理指标卡（B，W12）| 🔴 | sparkline 迷你图必须用 `BpSparkline` | W12 |
| `BpCronInput` 共享组件（A，W13 初）| schedules（B，W13）| 🔴 | Cron 表达式输入必须用 `BpCronInput` | W13 |
| `BpCronInput` 共享组件（A，W13 初）| 同步配置-调度 Tab（A，W12）| 🔴 | **顺序倒置**：W12 早于 W13 → **需调整**：BpCronInput 提前到 W12 抽取 | W12-W13 |
| workshop-canvas 编辑器（B，W3-W4）| pipeline.html 画布（B，W13）| 🟡 | 同 owner，复用 `BpCanvasEditor`；非阻塞但建议复用 | W3 + W13 |
| workshop-canvas 编辑器（B，W3-W4）| pipeline-list 节点图（B，W13）| 🟡 | 同上，节点图渲染可复用画布基础能力 | W3 + W13 |
| 数据源详情 DB Browser（B，W12）| 数据源新建-连接测试（A，W12）| 🟡 | 同 owner 不冲突，但都依赖 schemas API | W12 |
| 健康检查 API（B，W13）| 数据健康直方图（A，W13）| 🔴 | 直方图数据来自 `/v1/health/histogram` | W13 |
| Lineage 图 API（B，W13）| 数据沿袭节点展开（B，W13）| 🔴 | 同 owner，API 先行 | W13 |

**关键路径**：W12 第一天 A 必须先抽 `BpSparkline` + `BpCronInput`（W12 边缘代理 + 同步配置强依赖）。

### H.4 共享组件抽取时间表（强约束）

> 共享组件是减少交叉依赖的**核心枢纽**，抽取时间必须先于所有被依赖页

| 组件 | 抽取周 | 抽取 Owner | 被依赖页（Owner） | 被依赖周 |
|---|---|---|---|---|
| BpBadge / BpCard / BpToolbar / BpEmpty | W2 | A | 全站 | W3+ |
| BpStepper | W4 | A | 事件配置/数据源新建/Ferry 摆渡 | W4 / W12 / W11 |
| BpArchitectureBar | **W5 第 1 天** | A | 模型供应商/路由/目录（B+A+A）| W5 |
| BpCodeEditor | **W9 第 1 天** | A | 可观测性/Function 详情（B+B）| W9 / W10 |
| BpDiffViewer | **W9 第 1 天** | A | Wiki 差异（B）| W11 |
| BpSparkline | **W12 第 1 天** | A | 边缘代理（B）| W12 |
| BpCronInput | **W12 第 1 天**（提前 from W13）| A | schedules/同步配置（B+A）| W12 / W13 |
| BpCanvasEditor（从 workshop-canvas 抽出）| W4 末 | B | pipeline.html / pipeline-list（B）| W13 |

### H.5 顺序倒置预警（必须调整的项）

| # | 现状 | 问题 | 调整方案 |
|---|---|---|---|
| 1 | 智能体插件（W6）依赖 能力导入（W8）| 被依赖项晚于依赖项 | 智能体插件 W6 先用静态 mock（4 已接入能力卡 + 4 类型卡），W8 能力导入完成后联调"接入新能力"入口 |
| 2 | 同步配置-调度 Tab（W12）依赖 BpCronInput（原 W13）| 被依赖项晚于依赖项 | **BpCronInput 抽取时间从 W13 提前到 W12 第 1 天**（已更新 H.4）|
| 3 | AIP 分析师（W9）依赖 AIP 助手 SSE（W6）| 同 owner 但跨周 | 无需调整，W6 完成的 SSE 实现可在 W9 直接复用 |

### H.6 跨 owner 协作节点（必须同步对齐的时间点）

| 时间点 | 协作内容 | A 产出 | B 产出 |
|---|---|---|---|
| W1 末 | API 契约 review | 列出 35 页所需的 API 字段 | 列出 167 个 API 的 schema |
| W2 末 | 共享组件 v0 + 种子数据 1 验收 | BpBadge/BpCard/BpToolbar/BpEmpty | module/widget/theme 种子 |
| W4 末 | workshop-canvas MVP demo + 画布周边 4 页联调 | 组件/变量/主题/事件 4 页 | canvas MVP + BpCanvasEditor 抽出 |
| W5 第 1 天 | **BpArchitectureBar 评审**（3 页强依赖）| 组件代码 + Storybook | 3 模型页接入计划 |
| W5 末 | 模型管理 4 页联调 | 路由/容量 + 共享组件 | 目录/供应商 + 10 个 API |
| W9 第 1 天 | **BpCodeEditor + BpDiffViewer 评审** | 组件代码 + Storybook | 可观测性/Function 详情接入计划 |
| W12 第 1 天 | **BpSparkline + BpCronInput 评审** | 组件代码 + Storybook | 边缘代理/schedules 接入计划 |
| W13 末 | 全量回归 | 前端 E2E | 后端 pytest + 种子数据校验 |

### H.7 双人完全并行可行性结论

基于上述依赖矩阵，**W3 起双人可基本完全并行**，但有以下硬约束：

1. **共享组件抽取日**（W5/W9/W12 第 1 天）：A 必须在当天完成组件抽取 + Storybook，否则阻塞 B 当周任务
2. **API 契约冻结**（W1 末）：任何契约变更走 PR + 双人 review
3. **顺序倒置 2 项**（H.5）：按调整方案执行
4. **画布周边联调**（W4 末）：A 的 4 个周边页与 B 的画布 MVP 必须当周末联调通过

满足以上 4 条，W3-W13 共 11 周可完全并行，无双人间阻塞。

---

## 附录 I：独立任务清单（可移交另一开发）

> 用途：明确"另一开发（B/Buddy）可独立推进、对 A（我）零依赖或弱依赖"的任务范围
> 数据来源：附录 A（页面分工）+ 附录 B（核心改造点）+ 附录 H（跨页面依赖矩阵）
> 独立度图例：🟢 零依赖（可完全独立推进）/ 🟡 弱依赖（可 mock 启动，约定时间联调）/ 🔴 强依赖（必须等 A 交付组件，列入协作点）

### I.1 后端纯独立任务（🟢 零前端依赖，~25-30 人天）

> 整个后端域完全不依赖前端，另一开发可从 W1 起完全独立推进，仅需在 W1 末与 A 共同 review API 契约。

| 类别 | 任务 | 工作量 | 周次 | 独立度 | 备注 |
|---|---|---|---|---|---|
| **后端表** | 58 张表 schema 设计 + 迁移脚本（含 v2.2 新增 11 张：property/function_type/wiki_page/wiki_page_version/pipeline_nodes/pipeline_edges/pipeline_outputs/pipeline_collaborators/source_schemas/source_tables/source_columns）| 5 天 | W1-W2 | 🟢 | 表结构 + 迁移脚本完全独立 |
| **后端 API** | 167 个 endpoint 实现（CRUD + 业务逻辑）| 15 天 | W2-W13 持续 | 🟢 | 仅需 W1 末与 A review contracts/*.yaml |
| **后端 API** | AIP 助手流式 SSE（fetch + ReadableStream + 自动重连）| 2 天 | W6 | 🟢 | Nginx 配置独立 |
| **后端引擎** | LogicEngine DAG 分支/汇聚 | 2 天 | W7 | 🟢 | 算法实现独立 |
| **后端引擎** | Draft 审批状态机（draft→review→approved/rejected + 幂等键）| 2 天 | W8 | 🟢 | 状态机独立 |
| **后端引擎** | NL2Query 引擎（AIP 分析师）| 3 天 | W9 | 🟢 | 算法实现独立 |
| **后端引擎** | Automap 算法（V1 精确匹配 + 别名表）| 2 天 | W10 | 🟢 | 算法实现独立 |
| **种子数据** | ~1092 条 demo 数据（按附录 D 分批写入）| 5 天 | W2-W13 持续 | 🟢 | 完全独立 |
| **小计** | | **~36 天**（含缓冲）| | | |

**协作约束**：
- W1 末 API 契约 review（A+B 共同）
- 任何契约变更走 PR + 双人 review
- 后端 schema 变更 A 不能直接改，必须提 PR 给 B

### I.2 前端独立任务（🟢 零共享组件依赖，~35-45 人天）

> 这些前端页面对 A 抽取的共享组件**零依赖**，另一开发可完全独立完成。

| 页面/任务 | Owner | 工作量 | 周次 | 独立度 | 说明 |
|---|---|---|---|---|---|
| workshop-canvas 画布编辑器（B）| B | XL 8-10 天 | W3-W4 | 🟢 | 自抽 BpCanvasEditor，无 A 共享组件依赖；W4 末与 A 4 个周边页联调（可用 mock 启动）|
| 模块接口（B）| B | S 1-2 天 | W4 | 🟢 | 单栏 5xl 居中，零共享组件 |
| AIP 助手（B）| B | L 3-5 天 | W6 | 🟢 | 聊天 UI + 流式 SSE 自实现 |
| AIP 分析师（B）| B | XL 5+ 天 | W9 | 🟢 | 三栏全屏 + 聊天复用 SSE + 地图（Leaflet）|
| Draft 审批台（B）| B | L 3-5 天 | W8 | 🟢 | 三栏 + 4 Tab + 状态机 + timeline 全自实现 |
| 文档智能（B）| B | M 3-4 天 | W12 | 🟢 | OCR + LLM 提取 + 4 态状态，无共享组件 |
| 数据源详情 DB Browser（B）| B | M 4-5 天 | W12 | 🟢 | Schema 树 + ER 图 + 表格全自实现（SVG 手绘）|
| pipeline.html（B）| B | L 5-6 天 | W13 | 🟢 | 复用自抽 BpCanvasEditor + BpCronInput（W12 已抽）|
| pipeline-list.html（B）| B | M 4-5 天 | W13 | 🟢 | 三栏 SVG 节点图，全自实现 |
| lineage.html（B）| B | M 3-4 天 | W13 | 🟢 | 全局沿袭图全自实现 |
| schedules.html（B）| B | M 3-4 天 | W13 | 🟢 | Cron 输入用 BpCronInput（W12 已抽，无强依赖）|
| AIP 逻辑画布（B）| B | M 2 天 | W7 | 🟢 | 分支 Block + Handoff 自实现 |
| Wiki 详情 ①②③ 期（B）| B | XXL 10-15 天 | W11-W13 | 🟢（① 期）/ 🟡（③ 期）| ① Widget 树+画布独立；③ 期工作流编排复用 SSE |
| **小计** | | **~55-70 天** | | | |

### I.3 需协调的强依赖任务（🔴 A 必须按点交付组件）

> 这些任务在 A 抽取对应共享组件前**无法启动前端开发**，但后端可独立先做。**建议把这些任务的"后端部分"先交给另一开发，前端等 A 抽组件。**

| 页面 | Owner | 强依赖组件 | A 抽取时间 | 被阻塞的前端工作 | 可独立先做的后端工作 |
|---|---|---|---|---|---|
| 模型目录（B）| B | BpArchitectureBar | W5 第 1 天 | 三层架构条 UI | 10 个模型 API + 12 条种子 |
| 模型供应商（B）| B | BpArchitectureBar | W5 第 1 天 | 三层架构条 + 健康检查卡 | 健康检查 API |
| 可观测性（B）| B | BpCodeEditor | W9 第 1 天 | 代码编辑器 UI | Function 元数据 API |
| Function 详情（B）| B | BpCodeEditor | W9 第 1 天 | 代码编辑器 UI | function_type 表 + 2 API |
| Wiki 差异（B）| B | BpDiffViewer | W9 第 1 天 | diff 渲染 UI | wiki_page_version 表 + 3 API |
| 属性类型详情（B）| B | 无强依赖（独立）| — | — | property 表 + 5 CRUD API |
| 边缘代理（B）| B | BpSparkline | W12 第 1 天 | 指标卡 sparkline UI | agent_metrics 时序 API |
| 对象/链接/Action 详情（B）| B | 无强依赖（独立）| — | — | OT/LinkType/ActionType 扩展字段 |

**协作约束**：
- A 必须在抽取日**当天**完成组件代码 + Storybook，否则阻塞 B 当周任务
- B 在等待 A 抽组件期间，先做对应页面的**后端表/API/种子数据**
- 任何一方延期 1 天内提前同步

### I.4 推荐移交方案（最小交叉依赖）

**给另一开发（Buddy/B）的任务包** = I.1 + I.2 + I.3 后端部分，合计：

| 维度 | 工作量 | 周期 |
|---|---|---|
| 后端全套（表+API+种子+引擎）| ~36 天 | W1-W13 持续 |
| 前端独立页（画布/聊天/三栏/编辑器/Wiki 等 14 页）| ~55-70 天 | W3-W13 |
| 强依赖页的后端部分（5 页的后端表/API/种子）| ~10-12 天 | 与对应周并行 |
| **合计** | **~101-118 天** | **13 周（65 工作日）** |

> 与 §B.8 B 总计 74-103 天 + 后端 25-30 天 = 99-133 天基本吻合；13 周 × 5 工作日 = 65 工作日，B 需适度加班或延后部分页面（如 Wiki ③期、接入案例样式迁移）到 Wave 2。
> **与 B.8 的口径差异说明**：本表"~101-118 天"略高于 B.8 的"74-103 天 + 25-30 天"，差异来自：(a) I.1 后端 36 天比 B.8 后端 25-30 天多了 5 类引擎共 11 天（B.8 引擎工作量归入"页面工作量"）；(b) I.3 强依赖页后端 10-12 天与 B.8 后端有重叠计算。**以 B.8 为权威口径**，本表用于展示移交任务覆盖面。

### I.5 A 自留任务（最小化，~72-80 人天）

| 类别 | 任务 | 工作量 |
|---|---|---|
| Phase 0 | 名字统一（8 处）+ nav 改造 + 14 缺失页路由 | 2.5 天 |
| 共享组件 | 10 个组件抽取（BpBadge/BpCard/BpToolbar/BpEmpty/BpStepper/BpArchitectureBar/BpCodeEditor/BpDiffViewer/BpSparkline/BpCronInput）| ~10 天 |
| P0 前端 | 应用列表 + 风险告警 + 创建应用 + 组件注册表 + 变量管理器 + 主题与样式 + 事件配置 + 发布入口 + 模块管理 + 对象探索 | ~22 天 |
| P1 前端 | 智能体目录/插件/成熟度/对话机器人/工具/Evals/导入/能力导入/决策谱系/模型路由/容量管理 + 本体 Discover/对象探索/分支/图谱健康/OKF 等 | ~25 天 |
| P2 前端 | 运维 8 页 + 数据链接器/同步路由/同步配置/媒体集/数据源新建 + 管道提案/数据集/健康/搭建 | ~25 天 |
| **合计** | | **~72-80 天** |

**A 的硬交付节点**（不可延期，否则阻塞 B）：
- W2 末：BpBadge / BpCard / BpToolbar / BpEmpty
- W4 末：BpStepper
- **W5 第 1 天：BpArchitectureBar**（阻塞 B 3 个模型页）
- **W9 第 1 天：BpCodeEditor + BpDiffViewer**（阻塞 B 3 个详情页）
- **W12 第 1 天：BpSparkline + BpCronInput**（阻塞 B 边缘代理 + schedules）

### I.6 双人任务包对比

| 维度 | A（我）| B（另一开发）|
|---|---|---|
| 总工作量 | 72-80 天 | 101-118 天 |
| 前端页面数 | 35 页 | 31 页（含 9 个详情页 + Wiki XXL）|
| 后端表 | — | 58 张 |
| 后端 API | — | 167 个 |
| 种子数据 | — | ~1092 条 |
| 共享组件 | 10 个（抽取）| 0（仅使用）|
| 阻塞对方节点 | 3 个抽取日 | 0（B 不抽组件给 A）|

> B 工作量略高（101-118 vs 72-80），主要因后端 36 天归 B；如需平衡可把"P2 运维 8 页"或"接入案例"从 A 划给 B。

---

## 配套文档

- [223-deep-checklist.md](./223-deep-checklist.md)（P0+P2 共 35 页深度检查）
- [223-deep-checklist-2.md](./223-deep-checklist-2.md)（P1 共 31 页深度检查）
- [223-full-ui-gap-analysis.md](./223-full-ui-gap-analysis.md)（全量差距盘点）
- [223-menu-alignment-full.md](./223-menu-alignment-full.md)（菜单对照）
- [223-ui-alignment-plan.md](./223-ui-alignment-plan.md)（工作台深度方案）
- [223-seed-data-consolidation-plan.md](./223-seed-data-consolidation-plan.md)（种子数据整合）

# 223 多Agent协作编排方案（1 Planner + 4 Worker）

> 版本：v2.1（2026-07-27 Phase 0 修正版）
> v2.1 修正：新增 Phase 0 深度理解验证阶段——所有 Agent 必须先读懂技术方案和 9fa44a4 代码基线，通过理解报告后才能动手
> v2.0 修正内容：① 基线改为 9fa44a4（含 Tare 已提交代码）② 区分已完成/未完成任务 ③ 画布编辑排除（Tare 独立分支处理）
> 范围：将 223 全站 UI 对齐计划剩余任务拆分为 5 个 Agent 并行执行
> 基础设施：4 个 git worktree + 共享任务看板 + SendMessage 消息通道 + 2分钟轮询

---

## 0. 架构总览

```
                    ┌──────────────────────────┐
                    │     Planner Agent         │
                    │  · 读取 223-plan.md       │
                    │  · 拆分 Phase 任务         │
                    │  · 分配给 4 个 Worker     │
                    │  · 每 2 分钟轮询进度       │
                    │  · Phase 末合并代码        │
                    │  · 回答 Worker 提问        │
                    └─────────┬────────────────┘
                              │ TaskCreate + SendMessage
              ┌───────────────┼───────────────┐
              │               │               │
     ┌────────▼───┐  ┌───────▼────┐  ┌───────▼────┐  ┌───────────┐
     │ Worker-1   │  │ Worker-2   │  │ Worker-3   │  │ Worker-4  │
     │ 后端引擎   │  │ AIP交互页  │  │ 列表配置页  │  │ 运维+管道  │
     │ worktree:  │  │ worktree:  │  │ worktree:  │  │ worktree: │
     │  -w1       │  │  -w2       │  │  -w3       │  │  -w4      │
     └────────────┘  └────────────┘  └────────────┘  └───────────┘
```

> **v2.0 修正说明**：Worker-2 原来负责"画布编辑器"，但 **画布编辑（workshop-canvas）由 Tare 在独立分支处理**，已从本方案排除。Worker-2 改为负责"AIP 复杂交互页"（聊天/审批/分析/逻辑画布）。

---

## 1. 基线状态（9fa44a4 提交后的实际盘点）

### 1.1 已完成的任务（不需要再做）

| 223-plan 原周次 | 任务 | 状态 | 实际产出 |
|----------------|------|------|---------|
| W1 Phase 0 | 名字统一（8 处） | ✅ 已完成 | nav.ts 已包含新名字 |
| W1 Phase 0 | 14 个缺失页路由注册 + 骨架 | ✅ 已完成 | s2/ 目录下 19 个新 .tsx 页面 |
| W1 Phase 0 | bp 共享组件库 | ✅ 已完成 | 10 个 Bp* 组件（BpArchitectureBar/BpBadge/BpCard/BpCodeEditor/BpCronInput/BpDiffViewer/BpEmpty/BpSparkline/BpStepper/BpToolbar） |
| W2 | 种子数据基础 | ✅ 部分完成 | demo/ 目录 8 个文件（seed.py + org/order/module/workorder/action/demo_story） |
| W2 | widget 插件 | ✅ 已完成 | 5 个 manifest.json（detail-drawer/filter-bar/page-header/stat-card/trend-chart） |
| W2 | ComponentRenderer | ✅ 已完成 | ComponentRenderer.tsx + test |

### 1.2 已有骨架但需完善的页面（骨架已存在，可补功能、可重构、可推翻——测试兜底）

> **原则**：骨架是快速搭建的起点，不是最终形态。Worker 充分理解后，如果觉得骨架方向不对，可以重构甚至推翻重写，只要单元测试覆盖 + Phase 合并回归全绿。项目未发布，不怕改坏。

| 页面 | s2 文件 | 当前行数 | 需求 |
|------|---------|---------|------|
| 组件注册表 | WidgetRegistryPage.tsx | 292 | 补 4 来源筛选 + 卡片详情弹窗 |
| 变量管理器 | VariablesPage.tsx | 267 | 补类型动态表单 |
| 主题与样式 | StylesPage.tsx | 299 | 补主题编辑器 + 实时预览 |
| 事件配置 | EventsPage.tsx | 547 | 补 5 步向导 |
| 模型目录 | ModelCatalogPage.tsx | 314 | 补三层架构条 + Tab 系统 |
| 容量管理 | CapacityPage.tsx | 184 | 补 3 Tab + Info Banner |
| 智能体目录 | AgentRegistryPage.tsx | 701 | 表格改卡片网格 + 来源 Tab |
| 对话机器人 | AgentsPage.tsx | 1348 | 补 4 步创建向导 |
| 智能体导入 | AgentImportPage.tsx | 1612 | 补 5 种 Adapter |
| 能力导入 | CapabilityImportPage.tsx | 685 | 补 C0/C1/C2 + YAML |
| AIP 助手 | AipAssistPage.tsx | 652 | 补流式 SSE |
| AIP 分析师 | AipAnalystPage.tsx | 1101 | 补地图可视化 |
| 可观测性 | ObservabilityPage.tsx | 421 | 补代码编辑器 |
| 文档智能 | DocumentIntelligencePage.tsx | 415 | 补 OCR + LLM 提取 |
| Wiki 索引 | WikiIndexPage.tsx | 215 | 视觉对齐 |
| 创建应用 | WorkshopCreatePage.tsx | 634 | 视觉对齐 |
| 模块接口 | WorkshopModulePage.tsx | 186 | 补嵌套 Loop 示意图 |

### 1.3 完全缺失需新建的页面

| 页面 | 优先级 | 工作量 |
|------|--------|--------|
| Wiki 详情（富文本编辑器） | P1 | XXL 10-15d |
| Wiki 差异（diff 渲染） | P1 | M 2-3d |
| 属性类型详情 | P1 | XL 5-8d |
| Function 详情 | P1 | L 3-5d |
| pipeline.html | P2 | L 5-6d |
| pipeline-list.html | P2 | M 4-5d |
| lineage.html | P2 | M 3-4d |
| schedules.html | P2 | M 3-4d |
| source-detail.html | P2 | M 4-5d |
| 运维 8 页（Hub/Release/Spoke/FDE/变更/配置/接入案例） | P2 | 17-22d |
| 数据源 5 页 | P2 | 21-29d |

### 1.4 从方案中排除的任务（Tare 独立处理）

| 任务 | 原因 | 处理方式 |
|------|------|---------|
| workshop-canvas 画布编辑器改造 | Tare 正在独立分支改造 | **完全排除** — Worker 不碰 canvas 相关文件 |
| 模块接口（workshop-module-interface） | 与画布编辑耦合 | 排除，Tare 一并处理 |
| CanvasPage.tsx / LogicCanvasPage.tsx | 画布编辑核心文件 | **冻结** — 所有 Worker 不得修改 |

---

## 2. 四路 Worker 分工（v2.0 修正版）

### Worker-1：后端引擎（🟢 完全独立）

**worktree**: `/Users/ddt/work/projects/ai_agent/aos-platform-w1`
**分支**: `feature/223-worker-1`

| 维度 | 内容 |
|------|------|
| 核心职责 | 所有后端 Engine + Router + 种子数据扩展 |
| 文件域 | `services/aos-api/aos_api/engines/`, `routers/`, `demo/`, `store/` |
| 产出 | 补全 167 个 API + ~1092 条种子数据 |
| 依赖 | 无（完全独立）|
| 基线 | demo/ 已有 8 个种子文件，需补全到全分区覆盖 |

**Phase 任务序列**：
- Phase 1: 工作台后端补全（widgets/events/themes API 完善 + 种子扩展）
- Phase 2: 模型管理后端（catalog/registered/health/capacity API + 种子54条）
- Phase 3: AIP 后端（assist SSE 逻辑画布 Draft 审批 API + 种子137条）
- Phase 4: 本体后端（property/function_type/wiki_page API + 种子260条）
- Phase 5: 管道后端（pipeline_nodes/edges/outputs API + 种子95条）
- Phase 6: 数据源后端（source_schemas/tables/columns API + 种子330条）
- Phase 7: 运维后端（hub/spokes/ferry API + 种子43条）

### Worker-2：AIP 复杂交互页（🟡 依赖 Worker-1 API + Worker-3 组件）

> **v2.0 修正**：画布编辑已排除。Worker-2 改为聚焦 AIP 交互 + 本体详情 + 管道编辑器

**worktree**: `/Users/ddt/work/projects/ai_agent/aos-platform-w2`
**分支**: `feature/223-worker-2`

| 维度 | 内容 |
|------|------|
| 核心职责 | AIP 交互页（聊天/审批/分析/逻辑画布）+ 本体详情页 + 管道编辑器 |
| 文件域 | `apps/web/src/pages/s2/AipAssistPage.tsx` 等已有 .tsx 的深度完善 + 新建详情页 |
| **禁止修改** | `CanvasPage.tsx`, `LogicCanvasPage.tsx`, `WorkshopModulePage.tsx`（Tare 的域）|
| 依赖 | Worker-1 的 API + Worker-3 的 Bp* 组件（就绪时机由 Planner 动态协调）|

**Phase 任务序列**：
- Phase 1: AIP 助手深度完善（流式 SSE + 建议卡 + 权限感知）
- Phase 2: 对话机器人完善（4 步向导 + 工具箱面板）
- Phase 3: AIP 逻辑画布完善（分支 Block + Handoff + 预览）— 注意：LogicCanvasPage 只做 Block 增强，不改画布基础结构
- Phase 4: Draft 审批台（三栏 + 4 Tab + timeline + 审批流）
- Phase 5: 可观测性 + AIP 分析师（代码编辑器 + 三栏全屏 + 地图）
- Phase 6: 本体详情 6 页（属性/Function/Wiki详情/Wiki差异/Action/Link）
- Phase 7: 管道编辑器 3 页（pipeline.html + pipeline-list + lineage + schedules）

### Worker-3：列表/配置页 + 共享组件（🟢 大部分独立）

**worktree**: `/Users/ddt/work/projects/ai_agent/aos-platform-w3`
**分支**: `feature/223-worker-3`

| 维度 | 内容 |
|------|------|
| 核心职责 | 列表/网格/表单/向导页深度完善 + 共享组件增强 |
| 文件域 | `apps/web/src/pages/s2/` 中的列表/配置类 + `apps/web/src/components/bp/` |
| 产出 | ~20 页深度完善（已有骨架的）+ Bp* 组件功能补全 |
| 依赖 | Worker-1 的 API |
| 基线 | 已有 10 个 Bp* 组件骨架 + 17 个页面骨架，需深度完善到视觉稿标准 |

**Phase 任务序列**：
- Phase 1: 共享组件增强（BpArchitectureBar 补全三层架构 + BpBadge 多色 + BpCard 阴影/圆角）
- Phase 2: P0 配置页完善（WidgetRegistry + Variables + Styles + Events）
- Phase 3: P0 列表页完善（WorkshopCreate + 应用列表 + 风险告警）
- Phase 4: P1 AIP 列表页完善（AgentRegistry + AgentImport + CapabilityImport）
- Phase 5: P1 模型页完善（ModelCatalog 三层架构 + Capacity + 模型路由）
- Phase 6: P2 数据源列表页（数据链接器/同步路由/同步配置/媒体集/数据源新建）
- Phase 7: P2 其他列表页（数据集预览/数据健康/代码库/搭建弹窗）

### Worker-4：运维分区 + 接入案例 + 测试（🟢 完全独立）

**worktree**: `/Users/ddt/work/projects/ai_agent/aos-platform-w4`
**分支**: `feature/223-worker-4`

| 维度 | 内容 |
|------|------|
| 核心职责 | 运维分区 8 页 + 接入案例 + 全量回归测试 |
| 文件域 | `apps/web/src/pages/apollo.tsx` 等运维页面 + `__tests__/` |
| 产出 | 8 页新建 + 接入案例 + 回归测试套件 |
| 依赖 | Worker-1 的 API |

**Phase 任务序列**：
- Phase 1: 运维基础 3 页（Hub 舰队/Release 通道/Spoke 详情）
- Phase 2: 运维审批 4 页（Ferry 摆渡/FDE 资产包/变更审批/配置与密钥）
- Phase 3: 接入案例（9 平台案例卡 + 6 统计 + 10 阻塞项 + 端到端链路）
- Phase 4: 文档智能深度完善（OCR + LLM 提取 + 4 态状态）
- Phase 5: 回归测试编写（前端组件测试 + 后端 pytest 覆盖）
- Phase 6: 品牌色统一推广 + 暗色/浅色主题切换全站验证
- Phase 7: 全量回归 + 缺陷修复 + E2E 关键路径

---

## Phase 0：深度理解验证（所有 Agent 必须先通过，才能动手）

> **铁律**：不论 Planner 还是 Worker，开干前必须深刻理解 223 技术方案和 9fa44a4 代码基线。
> 没有"大概知道"，必须精确到"能复述出每页要改什么、现有代码什么模式、API 契约长什么样"。
> Phase 0 不产出一行业务代码，只产出 5 份理解报告。5 份都通过后，Planner 才宣布 Phase 1 开始。

### 0.1 Planner 的理解清单（启动时第一时间完成）

| 序号 | 阅读对象 | 路径 | 要回答的问题 |
|------|---------|------|------------|
| P-1 | 223-plan.md 全文 | `20_tech/223-plan.md`（1570 行）| 13 周排期怎么走？附录 A/B/C/D 分别管什么？§3.2 的 A/B 双线是什么？ |
| P-2 | 编排方案（本文件）§1-§2 | 本文件 | 4 个 Worker 的文件域怎么切？哪些页面已有骨架？哪些要新建？ |
| P-3 | 代码基线提交 | `git show 9fa44a4 --stat` | 这个 commit 包含了哪 98 个文件？Tare 做了什么？ |
| P-4 | 现有路由注册模式 | `services/aos-api/aos_api/main.py`（473 个 include_router）| Worker-1 新增的 API 要往哪里加？现有命名规范是什么？ |
| P-5 | 现有种子数据模式 | `services/aos-api/aos_api/demo/seed.py` + `seed_test_org()` | 种子数据的幂等模式是什么？org_id 隔离怎么做？ |
| P-6 | 223-deep-checklist.md §0 | `20_tech/223-deep-checklist.md` 前 60 行 | 每页必做的 7 项检查标准是什么？ |
| P-7 | foundry/html 目录 | `ls foundry/html/*.html`（73 个）| 每页的视觉稿叫什么名字？Worker-2/3/4 各自对应哪些？ |

**Planner 理解报告**（SendMessage 发给用户）必须包含：
- ① 7 个 Phase 各自要做哪些事（一句话/Phase）
- ② 4 个 Worker 的文件域边界（精确到目录）
- ③ 冻结文件清单（4 个）
- ④ 附录 A/B/C/D 在 plan.md 的行号范围
- ⑤ P0 已完成项清单（§1.1）

### 0.2 Worker-1（后端引擎）的理解清单

| 序号 | 阅读对象 | 路径 | 要回答的问题 |
|------|---------|------|------------|
| W1-1 | 223-plan.md 附录 C | 行 704-942 | 你要实现的 167 个 API 清单，每个 API 的路径/方法/入参出参 |
| W1-2 | 223-plan.md 附录 D | 行 944-1120 | 你要写的 ~1092 条种子数据，按分区怎么排期 |
| W1-3 | 现有 router 模式 | `services/aos-api/aos_api/routers/actions.py`（头 40 行）| APIRouter 怎么定义？Pydantic model 怎么写？ensure_schema 怎么做？ |
| W1-4 | 现有种子数据模式 | `services/aos-api/aos_api/demo/seed.py` + `order_seed.py` | seed_test_org 入口怎么组织？幂等怎么保证（ON CONFLICT DO NOTHING）？ |
| W1-5 | 现有 demo/ 8 个文件 | `ls services/aos-api/aos_api/demo/` | 已有哪些种子？缺哪些分区？ |
| W1-6 | main.py 注册位置 | `services/aos-api/aos_api/main.py` 的 include_router 区块 | 你的新 router 加在哪个位置？ |
| W1-7 | 现有测试模式 | `services/aos-api/tests/test_action_*.py` 任选一个 | pytest 怎么组织？conftest 怎么用？≥9 用例怎么写？ |

**Worker-1 理解报告**（SendMessage 给 Planner）必须回答：
- ① 你的 API 清单分几个分区？每区多少个？（引用附录 C 行号）
- ② 现有 demo/ 有哪些文件？还缺哪几个分区的种子？
- ③ 一个完整的"Engine+Router+Test"三件套长什么样？（用自己的话描述，不抄代码）
- ④ 种子数据的幂等模式是什么？为什么 org_id 隔离很重要？

### 0.3 Worker-2（AIP 交互页）的理解清单

| 序号 | 阅读对象 | 路径 | 要回答的问题 |
|------|---------|------|------------|
| W2-1 | 223-plan.md 附录 A 你负责的页面 | 行 473-568 | 你要做哪几个 AIP/本体/管道页面？每个的核心改造点是什么？ |
| W2-2 | 223-plan.md 附录 B AIP/本体/管道部分 | 行 570-703 | 每页具体改什么（加 SSE？加三栏？加编辑器？）|
| W2-3 | 223-deep-checklist-2.md AIP 部分 | `20_tech/223-deep-checklist-2.md` 第一部分（14 页）| AIP-01 到 AIP-14 每页的 7 项检查结果 |
| W2-4 | 223-deep-checklist-3.md | `20_tech/223-deep-checklist-3.md`（9 页详情）| 属性/Function/Wiki详情/Wiki差异 各要怎么建？|
| W2-5 | 现有 AIP 骨架代码 | `apps/web/src/pages/s2/AipAssistPage.tsx`（652行）+ `AgentsPage.tsx`（1348行）+ `AipAnalystPage.tsx`（1101行）| 已有骨架做了什么？还缺什么？编码风格是什么？ |
| W2-6 | 对应视觉稿 | `foundry/html/aip-assist.html` + `agents.html` + `aip-analyst.html` + `aip-draft-inbox.html` + `aip-observability.html` | 视觉稿的页面结构？三栏？Tab？交互？ |
| W2-7 | Worker-1 的 API 契约 | 223-plan.md 附录 C 的 AIP/本体/管道 API | 你调 Worker-1 的哪些接口？入参出参？ |

**Worker-2 理解报告**（SendMessage 给 Planner）必须回答：
- ① 你在 7 个 Phase 中各自负责哪些页面？（列页面名 + 视觉稿文件名）
- ② AipAssistPage 已有 652 行，视觉稿要求什么？还差什么？
- ③ 你依赖 Worker-3 的哪些 Bp* 组件？依赖 Worker-1 的哪些 API？
- ④ 冻结文件有哪些？你为什么不能碰 LogicCanvasPage？

### 0.4 Worker-3（列表/配置页 + 共享组件）的理解清单

| 序号 | 阅读对象 | 路径 | 要回答的问题 |
|------|---------|------|------------|
| W3-1 | 223-plan.md 附录 A 你负责的页面 | 行 473-568 | 你要做哪几个列表/配置/向导页面？ |
| W3-2 | 223-plan.md 附录 B 工作台/模型/数据源部分 | 行 570-703 | 每页核心改造点？|
| W3-3 | 223-deep-checklist.md P0 工作台部分 | `20_tech/223-deep-checklist.md` §7（9 页检查结果）| WidgetRegistry/Variables/Styles/Events 各缺什么？|
| W3-4 | 223-deep-checklist-2.md 模型管理部分 | `20_tech/223-deep-checklist-2.md` 第二部分（4 页）| 模型目录三层架构是什么？容量管理 3 Tab？|
| W3-5 | 现有骨架代码 | `WidgetRegistryPage.tsx`(292行) + `VariablesPage.tsx`(267行) + `StylesPage.tsx`(299行) + `EventsPage.tsx`(547行) + `ModelCatalogPage.tsx`(314行) | 骨架做了什么？缺什么？|
| W3-6 | 现有 bp 组件骨架 | `apps/web/src/components/bp/` 全部 10 个文件 | 每个 Bp* 组件现在几行？做什么？还差什么？|
| W3-7 | 对应视觉稿 | `foundry/html/workshop-widget-registry.html` + `workshop-variables.html` + `workshop-styles.html` + `workshop-events.html` + `aip-model-catalog.html` | 每页的卡片/网格/表单长什么样？|

**Worker-3 理解报告**（SendMessage 给 Planner）必须回答：
- ① 你在 7 个 Phase 中各自负责哪些页面？（列页面名 + 视觉稿文件名）
- ② BpArchitectureBar 现在 29 行，视觉稿要求什么？还差什么？
- ③ BpCodeEditor 现在 37 行，要支撑哪些场景？需要引入什么库？
- ④ 你的页面调 Worker-1 的哪些 API？

### 0.5 Worker-4（运维 + 管道 + 测试）的理解清单

| 序号 | 阅读对象 | 路径 | 要回答的问题 |
|------|---------|------|------------|
| W4-1 | 223-plan.md 附录 A 运维/管道/数据源部分 | 行 473-568 | 你要做哪几个运维/管道/数据源/文档智能页面？|
| W4-2 | 223-plan.md 附录 B 运维/管道部分 | 行 570-703 | 每页核心改造点？|
| W4-3 | 223-deep-checklist.md P2 运维部分 | `20_tech/223-deep-checklist.md` §3.3（运维 26 页清单）| 运维 8 页分别是什么？|
| W4-4 | 223-deep-checklist-3.md 管道部分 | `20_tech/223-deep-checklist-3.md` 页面 8-9（管道/数据源详情）| 管道编辑器和数据源详情要怎么做？|
| W4-5 | 现有运维骨架 | `apps/web/src/pages/s2/DocumentIntelligencePage.tsx`(415行) + `WikiIndexPage.tsx`(215行) | 已有什么？缺什么？|
| W4-6 | 对应视觉稿 | `foundry/html/apollo-hub.html` + `apollo-release.html` + `apollo-spoke.html` + `apollo-ferry.html` + `apollo-change-mgmt.html` + `apollo-config.html` + `integration-cases.html` + `pipeline.html` + `pipeline-list.html` | 运维和管道的视觉稿长什么样？|
| W4-7 | 现有测试模式 | `services/aos-api/tests/` 目录结构 + `conftest.py` | 回归测试怎么组织？现有多少测试？|

**Worker-4 理解报告**（SendMessage 给 Planner）必须回答：
- ① 运维 8 页分别是哪 8 个？每个的视觉稿文件名？
- ② 接入案例页要展示什么（9 平台案例卡 + 6 统计 + 10 阻塞项）？
- ③ 文档智能已有 415 行，OCR + LLM 提取 + 4 态状态分别是什么？
- ④ 你负责的回归测试要覆盖哪些模块？现有测试基线是多少？

### 0.6 Phase 0 的执行流程

```
Step 1: Planner 启动后第一时间执行 §0.1 的 7 项阅读
Step 2: Planner 完成后，发理解报告给用户审核
        → 用户确认"Planner 理解到位"后才启动 Worker
Step 3: 4 个 Worker 启动后，各自执行 §0.2-§0.5 的阅读清单
Step 4: 每个 Worker 完成后，发理解报告给 Planner
Step 5: Planner 审核 4 份报告：
        · 全部到位 → 宣布 Phase 0 完成，进入 Phase 1
        · 某个 Worker 不到位 → SendMessage 指出"你没提到 X，回去重读 Y"
        · 2 轮后仍不到位 → 转发给用户
Step 6: 5 份理解报告全部通过 → Planner 创建 Phase 1 任务
```

> **关键原则**：Phase 0 不赶时间。宁可多花时间读懂，也不要带着理解偏差动手。
> 理解报告里回答不上来的，就是还没读懂，必须重读。

---

## 3. Planner Agent 操作指南

### 3.1 Planner 的 6 条核心规则（铁律）

```
规则 0：【Phase 0 验证】在分配任何业务任务之前，Planner 必须确保：
       ① 自己已完成 §0.1 的阅读并通过用户审核
       ② 4 个 Worker 各自完成 §0.2-§0.5 的阅读并提交理解报告
       ③ 5 份理解报告全部通过后，才创建 Phase 1 任务
       ④ 绝不跳过 Phase 0 直接开工

规则 1：【先文档后代码】每个 Phase 开始前，Planner 必须先更新 223-plan.md 中对应 Phase 的任务状态，
       然后才通过 TaskCreate 分配任务给 Worker。

规则 2：【2分钟轮询】Planner 每 2 分钟执行一次进度检查：
       ① TaskList 查看所有任务状态
       ② 读取每个 worktree 的 git log --oneline -5 查看新增提交
       ③ 读取 223-plan.md 检查 Worker 更新的进度标记
       ④ 检查是否有 Worker 通过 SendMessage 发来的提问
       ⑤ 【动态协调】检查跨 Worker 依赖（§5.2.1），实时决定谁先做、谁等待、谁用 mock

规则 3：【Phase 合并】一个 Phase 的所有 Worker 任务都标记 completed 后，Planner 执行：
       ① 依次 merge 4 个 worktree 分支到 m1
       ② 在 m1 上运行回归测试（pytest + npm test）
       ③ 如果测试通过，git commit + 进入下一 Phase
       ④ 如果测试失败，通过 SendMessage 通知相关 Worker 修复
       ⑤ 注意：合并前先检查 Tare 是否有新的 m1 提交，如有先 rebase worker 分支

规则 4：【回答提问】Worker 通过 SendMessage 提问时，Planner 必须在下一轮轮询周期内回复：
       ① 技术问题（API schema/字段命名）：基于 223-plan.md 附录 C 的 API 清单回复
       ② 设计问题（视觉稿细节）：基于 foundry/html/ 对应 HTML 文件回复
       ③ 依赖问题（等另一个 Worker 的组件/API）：Planner 主动协调——检查对方进度，
          如果对方快完成了→让请求方先做其他部分；如果对方刚开始→让请求方用 mock 先行；
          如果依赖关系复杂→Planner 调整 Phase 内任务顺序
       ④ 架构问题（文件归属/冲突）：基于本方案 §2 的文件域划分回复
       ⑤ 画布相关问题：直接回复"画布编辑由 Tare 独立处理，不要碰 CanvasPage/LogicCanvasPage"
       ⑥ 无法确定的：通过 SendMessage 转发给用户

规则 5：【动态排期】Planner 的核心价值是实时协调，不机械执行预设排期：
       ① 每个 Phase 内部，Planner 根据 Worker 实际进度动态调整任务分配
       ② 如果 Worker-3 的组件提前完成，立即通知 Worker-2 可以联调（不等 Phase 结束）
       ③ 如果 Worker-2 被阻塞，Planner 让它先做不依赖组件的其他页面
       ④ 如果某 Worker 明显比其他快，Planner 可以从其他 Worker 的任务池调任务给它
       ⑤ Planner 每轮轮询都在做"谁该做什么"的重新决策

规则 6：【不写代码】Planner 不直接写业务代码，只做：制定计划、分配任务、轮询进度、
       合并代码、回答提问、更新文档。代码全部由 Worker 完成。

规则 7：【鼓励大胆改】当 Worker 提问"这个骨架能不能改/推翻/重构"时，Planner 的默认立场是：
       ① 只要 Worker 已通过 Phase 0 理解验证 → 信任他的判断
       ② 只要改动有测试覆盖（单元测试 + Phase 合并回归） → 允许大改
       ③ 我们没发布、线上没东西——不怕改坏，怕的是不敢改导致代码永远停留在骨架质量
       ④ 回复模板："充分理解 + 测试兜底 = 大胆改。改完确保测试全绿即可"
```

> 规则编号：v2.1 新增规则 0（Phase 0 验证）+ 规则 7（鼓励大胆改），共 8 条。

### 3.2 Planner 单 Phase 执行流程

> 注意：Phase 0 已在 §0.6 定义。以下流程适用于 Phase 1 及之后。

```
┌─ Phase N 开始（N ≥ 1）──────────────────────────────────────┐
│                                                              │
│  Step 1: 读取 223-plan.md，确定本 Phase 各 Worker 的任务范围   │
│          对照 §1.2（已有骨架）和 §1.3（缺失页面），不重复分配  │
│                                                              │
│  Step 2: 为每个 Worker 创建 Task（TaskCreate）                │
│          · subject: "Phase N - Worker-X - <任务名>"          │
│          · description: 包含具体页面/API/种子数据清单          │
│          · owner: "worker-1"/"worker-2"/"worker-3"/"worker-4"│
│                                                              │
│  Step 3: SendMessage 通知每个 Worker 开始执行                 │
│          · 附上 Task ID                                      │
│          · 附上本 Phase 的关键约束（依赖关系/冻结文件）        │
│                                                              │
│  Step 4: 进入 2 分钟轮询循环 ←────────────────────────┐      │
│          ① TaskList 检查状态                          │      │
│          ② git log 检查代码产出                       │      │
│          ③ 处理 Worker 提问（SendMessage 回复）        │      │
│          ④ 如果全部 completed → 跳出循环              │      │
│          ⑤ 如果有 Worker 卡住 → 给出指导              │      │
│          ⑥ sleep 120s → 回到 ④ ──────────────────────┘      │
│                                                              │
│  Step 5: 全部 completed 后，执行 Phase 合并                  │
│          ① 检查 m1 是否有 Tare 新提交（git log m1）          │
│          ② 如有，先在各 worktree 执行 git merge m1           │
│          ③ git -C aos-platform merge worker-1/2/3/4         │
│          ④ cd aos-platform && pytest && npm test            │
│          ⑤ 测试通过 → git commit → 更新 223-plan.md 进度     │
│          ⑥ SendMessage 通知所有 Worker 进入 Phase N+1        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 3.3 Planner 回答提问的标准格式

```
@worker-X 回复：

【问题类型】技术/设计/依赖/架构/画布排除

【回答】
<具体回答内容>

【依据】
<223-plan.md 章节号 / foundry/html/ 文件名 / 代码文件路径>

【行动建议】
<Worker 应该怎么做>
```

---

## 4. Worker Agent 操作指南

### 4.1 Worker 的 6 条核心规则（铁律）

```
规则 0：【Phase 0 深度理解】启动后第一时间执行 §0.2-§0.5（根据自己是哪个 Worker）的
       精确阅读清单，完成后向 Planner 提交理解报告。报告回答不上来的问题，
       就是还没读懂的，必须重读。理解报告未通过的 Worker 不会收到 Phase 1 任务。

规则 1：【先理解后动手】每个具体任务接到后，也要先完成针对性阅读：
       ① 通读 223-plan.md 中与本任务相关的章节
       ② 通读对应的 223-deep-checklist*.md 检查报告
       ③ 打开对应的 foundry/html/*.html 视觉稿，理解页面结构
       ④ 阅读现有代码中同类页面的实现（了解编码模式）
       ⑤ 确认 API 契约（Worker-1 的 contracts/*.yaml 或附录 C）
       ⑥ 检查 s2/ 目录是否已有骨架代码（如有，在骨架基础上完善，不重写）

规则 2：【先方案后代码】理解需求后，先写简要实现方案（100-200字），
       通过 SendMessage 发给 Planner 审核。Planner 确认后才开始写代码。
       方案模板：
       "Worker-X Phase N 方案：
        · 要改的文件：...
        · 要新建的文件：...
        · 实现步骤：1... 2... 3...
        · 预计产出：... 个文件 / ... 行代码 / ... 个测试
        · 已有骨架：s2/XxxPage.tsx 已有 N 行骨架，在此基础上完善"

规则 3：【编码模式】严格沿用 220plan2/221plan 的编码模式：
       后端：Engine(Pydantic+Singleton+threading.Lock) + Router(FastAPI APIRouter) + Test(pytest ≥9用例)
       前端：React + TypeScript + Bp* 共享组件
       种子数据：seed_*.py（幂等，先 delete by org_id 再 insert）

规则 4：【每功能点写测试】每个 Engine/Router/组件开发完立即写单元测试，
       全部通过才标记 Task completed。测试不通过的 Task 不能标 completed。

规则 5：【大胆改，测试兜底】在充分理解（Phase 0 已验证）的前提下，大胆改动现有代码：
       ① 我们没发布，线上没东西，不影响任何用户——不怕改坏
       ② 骨架代码不是最终形态，可以重构、可以推翻、可以合并——只要结果更好
       ③ 大改的底气来自测试：单元测试覆盖你改的逻辑 + Phase 合并时跑全量回归
       ④ 如果改动后测试全绿，就放心提交；如果测试红了，修到绿为止
       ⑤ 不要因为"这是 Tare 写的骨架"就畏手畏脚——他也是在快速搭骨架，你负责让它真正可用

规则 6：【提问时机】遇到以下情况必须通过 SendMessage 问 Planner，不能自己猜：
       ① 223-plan.md 附录 C 的 API schema 不明确
       ② 视觉稿与现有代码冲突，不确定听谁的
       ③ 需要的 API 还没被 Worker-1 实现（跨 Worker 依赖）
       ④ 文件归属不确定（怕和别的 Worker 冲突）
       ⑤ 发现 223-plan.md 本身有矛盾或遗漏
       ⑥ 需要修改 CanvasPage/LogicCanvasPage/WorkshopModulePage（这些是 Tare 的域，必须先问）
```

> 规则编号：v2.1 新增规则 0（Phase 0 深度理解）+ 规则 5（大胆改测试兜底），共 7 条。

### 4.2 Worker 单任务执行流程

```
┌─ Worker-X 接到 Task ────────────────────────────────────────┐
│                                                              │
│  Step 1: TaskGet(taskId) — 读取完整任务描述                   │
│                                                              │
│  Step 2: 【理解阶段】                                         │
│          ① Read 223-plan.md 相关章节                         │
│          ② Read 223-deep-checklist*.md 对应页                │
│          ③ Read foundry/html/<对应视觉稿>.html               │
│          ④ Read 现有 s2/ 骨架代码（如已有）                   │
│          ⑤ Read contracts/*.yaml（如存在）                    │
│                                                              │
│  Step 3: 【方案阶段】                                         │
│          写简要方案 → SendMessage 给 Planner                  │
│          等待 Planner 回复（一般 <4 分钟 = 2 轮轮询）         │
│                                                              │
│  Step 4: 【编码阶段】                                         │
│          ① 在自己的 worktree 分支上开发                       │
│          ② 每完成一个功能点立即写测试                         │
│          ③ pytest/npm test 全部通过                          │
│          ④ git add + git commit（在自己的 worktree）          │
│                                                              │
│  Step 5: 【更新文档】                                         │
│          更新 223-plan.md 中对应任务的进度标记                 │
│                                                              │
│  Step 6: 【标记完成】                                         │
│          TaskUpdate(taskId, status="completed")              │
│          SendMessage 通知 Planner "Worker-X Phase N 完成"    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 4.3 Worker 代码提交规范

```
feat: 223 Phase N Worker-X — <任务简述>

- <具体改动 1>
- <具体改动 2>
- <测试：N passed>

Worktree: aos-platform-wX
Phase: N
```

---

## 5. Phase 排期与依赖关系

### 5.1 全局 Phase 时间线（v2.1 修正：新增 Phase 0）

| Phase | Worker-1 (后端) | Worker-2 (AIP交互) | Worker-3 (列表配置) | Worker-4 (运维管道) | 合并后验证 |
|-------|-----------------|---------------------|---------------------|---------------------|-----------|
| **P0** | 读附录C/D + 现有router/demo/test | 读AIP页A/B + checklist-2/3 + 骨架+html | 读列表页A/B + checklist + bp骨架+html | 读运维页A/B + checklist + 骨架+html | **5份理解报告全通过** |
| **P1** | 工作台API补全 | AIP助手(SSE) | 共享组件增强 | 运维基础3页 | 后端可用 |
| **P2** | 模型API | 对话机器人完善 | P0配置页4个 | 运维审批4页 | 前端可跑 |
| **P3** | AIP API | 逻辑画布Block+Draft审批 | P0列表页3个 | 接入案例 | P0基本可用 |
| **P4** | 本体API | 可观测性+分析师 | P1 AIP列表3个 | 文档智能完善 | P0完整 |
| **P5** | 管道API | 本体详情6页 | P1模型页3个 | 回归测试 | P1基本可用 |
| **P6** | 数据源API | 管道编辑器4页 | P2数据源列表5个 | 品牌色统一 | P2基本可用 |
| **P7** | 运维API+种子收尾 | 管道收尾 | P2其他列表4个 | 全量回归 | **全量完成** |

### 5.2 Phase 间依赖

```
P0 ──→ P1 ──→ P2 ──→ P3 ──→ P4 ──→ P5 ──→ P6 ──→ P7
(理解)
```

> P0 不产代码，只产理解报告。5 份全通过后才进 P1。

### 5.2.1 跨 Worker 组件依赖（Planner 动态协调，非硬编码约束）

Worker-2 的部分页面依赖 Worker-3 的 Bp* 共享组件。**但谁先做、谁等待、是否用 mock 先行——这些都由 Planner 根据实时进度动态决定，不预设"第1天必须完成"的死规则。**

| 被依赖组件 | Owner | 依赖方 | Planner 协调策略（三选一）|
|-----------|-------|--------|-------------------------|
| BpArchitectureBar | Worker-3 | Worker-2 的模型页/本体详情页 | ① Worker-3 先行 → Worker-2 等组件就绪 ② Worker-2 用 mock 先行 → 后续联调 ③ 两者同步推进，Worker-3 优先提交组件 |
| BpCodeEditor/BpDiffViewer | Worker-3 | Worker-2 的可观测性/Function详情 | 同上，Planner 根据 P4 时两人的进度决定 |
| BpSparkline/BpCronInput | Worker-3 | Worker-2 的管道 schedules | 同上 |

> **设计原则**：Planner 的核心价值就是动态协调。每轮 2 分钟轮询时，Planner 评估跨 Worker 依赖状态，实时决定：谁先推进、谁暂停等待、谁先用 mock、什么时候联调。方案文档只提供"依赖关系信息"，不预设"谁必须在哪天完成"——那是 Planner 的职责。

### 5.3 冻结文件清单（所有 Worker 禁止修改）

以下文件由 Tare 在独立分支处理画布编辑改造，**所有 Worker 禁止修改**：

| 文件 | 原因 |
|------|------|
| `apps/web/src/pages/CanvasPage.tsx` | 画布编辑核心 |
| `apps/web/src/pages/s2/LogicCanvasPage.tsx` | 逻辑画布核心 |
| `apps/web/src/pages/s2/WorkshopModulePage.tsx` | 模块接口（与画布耦合）|
| `apps/web/src/pages/WorkshopListPage.tsx` | 应用列表（与画布入口耦合）|

> Worker-2 做 LogicCanvasPage 时只做"分支 Block + Handoff 增强"，不动画布基础结构。

### 5.4 每 Phase 合并检查清单

Planner 在合并前必须确认：

- [ ] Worker-1 的后端 pytest 全部通过
- [ ] Worker-2 的前端页面可渲染（无白屏）
- [ ] Worker-3 的共享组件有测试
- [ ] Worker-4 的测试套件通过
- [ ] 4 个分支无合并冲突（由 Planner 用 test merge 验证）
- [ ] 没有修改冻结文件（git diff 检查 CanvasPage/LogicCanvasPage/WorkshopModulePage）
- [ ] 223-plan.md 中本 Phase 任务全部标记 [x]

---

## 6. 启动配置

### 6.1 Worktree 已创建（基于 9fa44a4）

```bash
# 已执行（2026-07-27 v2.0）
cd /Users/ddt/work/projects/ai_agent/aos-platform
git worktree add ../aos-platform-w1 -b feature/223-worker-1
git worktree add ../aos-platform-w2 -b feature/223-worker-2
git worktree add ../aos-platform-w3 -b feature/223-worker-3
git worktree add ../aos-platform-w4 -b feature/223-worker-4
```

### 6.2 Worktree 路径映射

| Agent | Worktree 路径 | 分支 |
|-------|---------------|------|
| Planner | `/Users/ddt/work/projects/ai_agent/aos-platform` (m1 主仓库) | m1 |
| Worker-1 | `/Users/ddt/work/projects/ai_agent/aos-platform-w1` | feature/223-worker-1 |
| Worker-2 | `/Users/ddt/work/projects/ai_agent/aos-platform-w2` | feature/223-worker-2 |
| Worker-3 | `/Users/ddt/work/projects/ai_agent/aos-platform-w3` | feature/223-worker-3 |
| Worker-4 | `/Users/ddt/work/projects/ai_agent/aos-platform-w4` | feature/223-worker-4 |

### 6.3 Phase 合并命令（Planner 执行）

```bash
# 在 m1 主仓库执行
cd /Users/ddt/work/projects/ai_agent/aos-platform

# 0. 先检查 Tare 是否有新提交
git log --oneline m1 -3
# 如果有新提交（commit hash 不是 9fa44a4），先通知 Worker rebase

# 1. 依次合并 4 个 worktree 分支
git merge feature/223-worker-1 --no-edit
git merge feature/223-worker-2 --no-edit
git merge feature/223-worker-3 --no-edit
git merge feature/223-worker-4 --no-edit

# 2. 检查冻结文件未被修改
git diff HEAD~4..HEAD -- apps/web/src/pages/CanvasPage.tsx apps/web/src/pages/s2/LogicCanvasPage.tsx apps/web/src/pages/s2/WorkshopModulePage.tsx
# 如果有变更，通知 Worker 回滚

# 3. 回归测试
cd services/aos-api && python -m pytest tests/ -x -q
cd ../../apps/web && npm test -- --passWithNoTests

# 4. 提交（如果 merge 自动生成了 commit 就跳过）
cd /Users/ddt/work/projects/ai_agent/aos-platform
git add -A && git commit -m "feat: 223 Phase N merge — 4-worker 合并"

# 5. 通知所有 Worker 从 m1 拉取最新（为下一 Phase 准备）
# 各 Worker 执行：
# cd <worktree> && git merge m1 --no-edit
```

---

## 7. 异常处理

### 7.1 Worker 卡住超过 10 分钟

Planner 检测到某 Worker 连续 5 轮轮询（10 分钟）无新提交且 Task 未 completed：

1. SendMessage 询问卡住原因
2. 如果是技术问题 → Planner 给出指导
3. 如果是依赖问题 → 检查被依赖方进度，必要时暂停该 Worker 等待
4. 如果是理解偏差 → 重新解释任务要求
5. 如果 15 分钟仍无进展 → 转发给用户

### 7.2 合并冲突

```bash
# 如果 merge 出现冲突：
git merge feature/223-worker-X

# CONFLICT 时的处理：
# 1. Planner 检查冲突文件
# 2. 判断归属（谁的文件域谁优先）
# 3. SendMessage 通知冲突双方协调
# 4. 由文件域 Owner 手动解决冲突
# 5. 解决后 git add + git commit
```

**冲突预防**：
- Worker-1 独占 `services/aos-api/` 后端目录
- Worker-2 独占 `apps/web/src/pages/s2/` 中的 AIP/本体/管道页面
- Worker-3 独占 `apps/web/src/pages/s2/` 中的列表/配置页面 + `components/bp/`
- Worker-4 独占 `apps/web/src/pages/s2/` 中的运维/管道页面 + 测试
- **共享文件**（nav.ts, App.tsx, main.py）：P0 已由 Tare 改完，之后冻结
- **冻结文件**（CanvasPage, LogicCanvasPage, WorkshopModulePage）：Tare 的域

### 7.3 测试失败

Phase 合并后测试失败：
1. Planner 识别失败测试所属域
2. SendMessage 通知对应 Worker 修复
3. Worker 在自己 worktree 修复 → 重新提交
4. Planner 重新合并 → 重新测试
5. 通过后才进入下一 Phase

### 7.4 Tare 提交了新代码到 m1

如果 Planner 在 Phase 合并前发现 m1 有 Tare 的新提交（hash ≠ 9fa44a4）：

1. 通知所有 Worker 暂停提交
2. 在各 worktree 执行 `git merge m1 --no-edit` 同步 Tare 的改动
3. 如果 Tare 改了冻结文件（CanvasPage 等），正常，不影响
4. 如果 Tare 改了其他文件导致冲突，协调解决
5. 同步完成后，Worker 继续 Phase 开发
6. Planner 合并时基于新的 m1 HEAD

---

## 8. 配套文件

| 文件 | 用途 |
|------|------|
| 本文件 | 5 Agent 协作编排方案（v2.0 修正版） |
| `223-plan.md` | 原始 13 周开发计划（任务来源） |
| `223-deep-checklist.md` | P0+P2 共 35 页深度检查 |
| `223-deep-checklist-2.md` | P1 共 31 页深度检查 |
| `223-deep-checklist-3.md` | 详情页/弹出页 9 页深度检查 |
| `foundry/html/*.html` | 73 个视觉稿参考文件 |
| `services/aos-api/contracts/*.yaml` | API 契约 |
| `223-orchestration-launch.md` | 启动指南（Planner + Worker prompt 模板） |

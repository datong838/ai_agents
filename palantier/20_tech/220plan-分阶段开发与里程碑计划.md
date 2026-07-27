# 220plan · AOS Platform W1 分阶段开发与里程碑计划

>:> **版本**：v4.26 · 2026-07-23
> **基线**：差距对照分析 [220w-与目标系统差距对照分析.md](./220w-与目标系统差距对照分析.md) v1.17 · 259 差距项 · W1 优先项 19 项（对齐 220w §12）
> **代码库**：`/Users/ddt/work/projects/ai_agent/aos-platform`
> **UI 真源**：`/Users/ddt/work/projects/ai_agent/docs/palantier/foundry/html/`（59 个 HTML 售前蓝图 · Demo v1.6.5）
> **设计令牌**：`packages/ui-kit/tokens.css`（dark/light 双主题）

---

## 0. 总则与开发纪律

### 0.1 核心原则

| 原则 | 说明 |
| --- | --- |
| **先测试后交付** | 每个功能点开发完成**立即**编写单元测试；全部通过方可进入下一功能点 |
| **波次集成自测** | 每个 Phase（波次）完成后执行集成自测：重启系统 → 验证页面加载 → 验证风格一致性 → 验证跨模块链路 |
| **UI 对标真源** | 新增/改动的 UI 页面**必须**对标 `foundry/html/` 对应 HTML 蓝图页的布局结构、交互模式、视觉层级 |
| **依赖前置** | 被依赖的模块必须先完成；跨 Phase 依赖在 Phase 开头标注「前置条件」 |
| **最小更改** | 已有页面优先改页而非重写；新增能力以增量方式嵌入现有路由 |
| **中文交付** | 侧栏 / 文案 / 术语以中文为主；线框 ID 仅文档对照不展示于 UI |

### 0.2 技术栈与测试框架

| 层 | 技术栈 | 测试框架 | 运行命令 |
| --- | --- | --- | --- |
| 后端 API | FastAPI ≥0.115 · Python ≥3.11 · Pydantic v2 | pytest ≥8.0 + httpx | `cd services/aos-api && python -m pytest tests/ -v` |
| 前端 Web | React 18 · Vite 5 · TypeScript 5.6 · React Router 6 | Vitest 2.1 + jsdom | `cd apps/web && npx vitest run` |
| UI 令牌 | CSS Custom Properties · `packages/ui-kit/tokens.css` | — | 人工目视 + 截图比对 |
| 数据库 | SQLite（开发）/ PostgreSQL（生产） | — | pytest 内置 fixture |

### 0.3 测试纪律细则

```
┌─────────────────────────────────────────────────────────┐
│              单个功能点开发流程（强制）                     │
│                                                         │
│  1. 编写功能代码（backend 模块 + router 或 frontend 组件）  │
│  2. 立即编写单元测试（backend: tests/test_*.py;            │
│     frontend: *.test.ts / *.test.tsx）                   │
│  3. 运行测试 → 全部通过                                   │
│  4. 代码审查（自检：风格/边界/错误处理）                    │
│  5. 标记功能点完成 → 进入下一功能点                         │
│                                                         │
│  ⛔ 任何功能点在测试未全通过前不得标记完成                   │
│  ⛔ 不得跳过测试直接开发下一功能点                           │
└─────────────────────────────────────────────────────────┘
```

### 0.4 波次集成自测流程

每个 Phase 完成后执行以下检查清单：

| 步骤 | 检查项 | 方法 |
| --- | --- | --- |
| ① 重启后端 | `cd services/aos-api && python -m aos_api.main` 启动无报错 | 检查 startup log |
| ② 重启前端 | `cd apps/web && npx vite` 启动无报错 | 检查 Vite dev server |
| ③ 全量测试 | 后端 `pytest` + 前端 `vitest run` 全绿 | CI 或本地 |
| ④ 页面加载 | 逐页面访问新开发路由，确认无白屏 / 500 | 浏览器 |
| ⑤ 风格一致 | 对比 `foundry/html/` 对应 HTML 蓝图页，验证布局/配色/交互模式 | 人工目视 |
| ⑥ 跨模块链路 | 验证本 Phase 产出被上游正确调用 | 手动触发链路 |
| ⑦ 截图归档 | 截取关键页面截图，存入 `docs/screenshots/phase-N/` | 自动截图 |

---

### 0.5 执行状态定义与进度跟踪

| 状态 | 标记 | 含义 | 准入条件 |
| --- | --- | --- | --- |
| **已完成** | ✅ | 功能开发完成，单元测试全部通过，Phase 集成自测通过 | 代码合入 + 测试全绿 + 集成自测清单全部勾选 |
| **代码完成·待验证** | 🟡 | 代码已开发完成且纯逻辑核心已验证，但完整 pytest（API 层 + 全量回归）受环境阻塞未执行 | 环境（Python 3.11+ + 依赖）就绪后跑 pytest 全绿即转 ✅ |
| **暂停** | ⏸ | 前置条件不满足或外部依赖未就绪，暂时无法推进 | 记录阻塞原因 + 预计解除条件 |
| **待执行** | ⬜ | 尚未开始开发，等待前置 Phase / W1 项完成 | 前置项全部 ✅ 后自动转为可执行 |

> **状态更新规则**：
> 1. 每个功能点开发完成并通过单元测试后，在 §1.2 进度看板中将其状态从 ⬜ 改为 ✅
> 2. 遇到阻塞时（如外部依赖未就绪、前置项未完成），将状态改为 ⏸ 并在"阻塞原因"列说明
> 3. ⏸ 项的阻塞解除后，状态改为 ⬜ 进入待执行队列
> 4. 每 Phase 集成自测通过后，该 Phase 整体状态改为 ✅
> 5. 状态变更需在 §12 变更日志中记录

---

## 1. Phase 总览与依赖拓扑

```
Phase 0: 基础设施与测试框架
    │
    ├──→ Phase 1: 核心引擎层（Function + Build + Sandbox）
    │        │
    │        ├──→ Phase 2: 数据集成核心（Funnel + Transform + Lineage + Pipeline Builder）
    │        │        │
    │        │        └──→ Phase 3: Ontology 写回闭环（Action Writeback + Shell-Core + Funnel Editor + Roles）
    │        │                 │
    │        │                 └──→ Phase 4: AIP 智能层（Logic + Evals）
    │        │
    │        └──→ Phase 5: 非结构化数据与数据集（MediaSet + MediaReference + SQL Console）〔可与 Phase 2 并行〕
    │
    └──→ Phase 6: 集成优化与收尾（Pipeline Retry + Schedule 增强 + 全链路验收）
```

### 1.1 各 Phase 里程碑摘要

| Phase | 名称 | 状态 | W1 项 | 核心交付物 | 前置条件 |
| --- | --- | --- | --- | --- | --- |
| 0 | 基础设施与测试框架 | ✅ 已完成 | — | CI 管线 · 测试模板 · 截图归档目录 | — |
| 1 | 核心引擎层 | ✅ 已完成 | W1-1, W1-4, W1-10 | Function 表达式引擎 · Build 引擎 · Function 沙箱 | Phase 0 |
| 2 | 数据集成核心 | ✅ 已完成 | W1-5, W1-8, W1-13, W1-14, W1-19 | Funnel 四阶段 · Transform 算子库 · Lineage DAG · Pipeline Builder DAG 编辑器 · Functions Python Builder | Phase 1 |
| 3 | Ontology 写回闭环 | ✅ 已完成 | W1-3, W1-6, W1-7, W1-17, W1-18 | Action 写回 · 壳核模式 · Funnel 可视化编辑器 · Ontology 角色 · Function Type 视图 | Phase 2 |
| 4 | AIP 智能层 | ✅ 已完成 | W1-2, W1-12 | Logic 三栏编排 · Evals 门控 | Phase 3 + LLM Gateway 接入 |
| 5 | 非结构化数据与数据集 | ✅ 已完成 | W1-9, W1-15, W1-16 | MediaReference 桥接 · SQL 控制台 · MediaSet 类型化 | Phase 1 |
| 6 | 集成优化与收尾 | ✅ 已完成 | W1-11 | Pipeline 重试 · 全链路验收 | Phase 2–5 |

### 1.2 全局执行进度看板

> **最后更新**：2026-07-24 · v4.43 Phase 0 基础设施补齐 + #90 Pipeline 管理清账 + Phase 1/2/3/5 过期状态修正 · 进度 252/259
> **差距总览**：259 项 · ✅ 已完成 252 · ⬜ 待执行 0 · ⏸ 暂停 7

#### 1.2.1 全局差距统计

| 分类 | 数量 | 执行状态 | Wave | 说明 |
| --- | --- | --- | --- | --- |
| ✅ 已达成 | 2 | ✅ 已完成 | — | 无需开发，保持维护 |
| W1 优先项 | 19 | ✅ 已完成 | W1 | Phase 0–6 核心交付，本计划主体（19/19 全部完成） |
| W2+ 高优先级 | 27 | ✅ 已完成（27/27） | W2 | W1 完成后优先推进 · W2-A（#3/#6/#8/#9/#20/#23）+ W2-B（#7/#18/#21/#25/#26）+ W2-C（#12/#13/#14/#15/#16）+ W2-D（#10/#24）+ W2-E（#1/#2/#4/#22）+ W2-F（#11/#17/#19 增强版）已交付 |
| W2+ 中优先级 | 166 | ✅ 已完成（166/166） | W2–W3 | W2-G～W2-BH 全部交付 · 含 #92/#93/#145 清账 · 23 批次总计 |
| W2+ 低优先级 | 33 | ✅ 已完成（33/33） | W3+ | W2-BI～W2-BP 全部交付 #1～#35（428 测试，含 #28/#29 合并）· 8 批次总计 |
| 停车场 | 7 | ⏸ 暂停 | 后置 | 条件不具备或后置不开 |
| **合计** | **259** | | | |

#### 1.2.2 W1 优先项进度（Phase 0–6 · 19 项）

> 对齐 [220w §12](./220w-与目标系统差距对照分析.md#L3954) W1-1~W1-19（W1-10 收回为 1 项，含子能力；W1-19 为原 W1-14 编号重复修正项）。

| W1 编号 | 差距项 | 当前 | 目标 | 优先级 | Phase | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| W1-1 | Function 引擎 | 无 | 表达式引擎（解析/求值/类型推导/Ontology API） | 高 | P1 | ✅ 已完成 |
| W1-2 | Logic 编排真接入 | 无 | 三栏 UI + Block 全量 + 工具集注册 + 写回四步 | 高 | P4 | ✅ 已完成 |
| W1-3 | Funnel 可视化映射编辑器 | 弱 | 源 Schema 侧栏 + 映射表格 + 自动映射 + Lint 门控 + 行业模板 | 中 | P3 | ✅ 已完成 |
| W1-4 | Build 引擎 | 无 | Job/JobSpec + 事务锁定 + 状态机 + 日志 | 高 | P1 | ✅ 已完成 |
| W1-5 | Funnel 四阶段管道 | 仅状态机 | Changelog/Merge/Indexing/Hydration | 高 | P2 | ✅ 已完成 |
| W1-6 | Action 写回协议 | 直写底层 | L1 Write-back Dataset + 软删除 + 乐观 UI | 高 | P3 | ✅ 已完成 |
| W1-7 | 壳核模式 | 无 | Action 调用 Function（FUNC-SPEC/ACT-SPEC） | 高 | P3 | ✅ 已完成 |
| W1-8 | Transform 算子库 | 无 | Filter/Join/Aggregate/Explode/Cast/Union/Sort/Distinct/Expression（含 Pipeline Transform 算子库合并） | 高 | P2 | ✅ 已完成 |
| W1-9 | MediaReference 桥接 | 无 | Dataset 列 → MediaSet 指针 | 高 | P5 | ✅ 已完成 |
| W1-10 | Function 类型安全 + 沙箱 | 无 | Schema→TS 编译 + 沙箱 + 超时/内存限制 + 可组合（原 §1.2.2 #13/#14/#15/#16 四行合并为 1 项） | 高 | P1 | ✅ 已完成 |
| W1-11 | Pipeline 重试机制 | 无 | 自动重试 + 退避 + DLQ | 中 | P6 | ✅ 已完成 |
| W1-12 | Evals 门控 | 无 | 评测集 + 门禁上线 | 中 | P4 | ✅ 已完成 |
| W1-13 | Data Lineage DAG 可视化 | 静态列表 | 交互式 DAG + 节点展开 + 4 种节点 + 列级血缘 | 高 | P2 | ✅ 已完成 |
| W1-14 | Pipeline Builder 交互式 DAG 编辑器 | 静态 3 节点 | 拖拽节点 + 连线 + 撤销重做 + 预览 + DAG 保存（合并原 #24 DAG 保存） | 高 | P2 | ✅ 已完成 |
| W1-15 | Dataset Preview SQL 控制台 | 白名单 select 1/* | 完整 Spark SQL 方言 + 自动补全 + 查询历史（合并原 #6/#23 重复项） | 中 | P5 | ✅ 已完成 |
| W1-16 | MediaSet 类型化 + 表格行变换 | 通用上传 | DICOM/音频/文档/图像 + 表格行变换 | 高 | P5 | ✅ 已完成 |
| W1-17 | Ontology 角色体系 | 无 | Owner/Editor/Viewer/Discoverer 四级 + 元数据与数据分离 | 高 | P3 | ✅ 已完成 |
| W1-18 | OMA Function Type 视图 | 无 | 函数概览 + 使用历史 + 版本历史 + 跳转代码库 | 高 | P3 | ✅ 已完成 |
| W1-19 | Functions Python Builder | 无 | Pipeline Builder 中使用 Python 函数（原 W1-14 编号重复，220w 已修正为 W1-19） | 高 | P2 | ✅ 已完成 |

**合并说明**（v1.3 对齐 220w §12）：
- 原 #13/#14/#15/#16（Function 类型安全/沙箱/性能约束/可组合）→ 合并为 **W1-10**（性能约束/可组合作为 W1-10 子能力，不单列）
- 原 #6 与 #23（Dataset Preview SQL 控制台重复）→ 合并为 **W1-15**
- 原 #4 与 #21（Transform 算子库 / Pipeline Transform 算子库）→ 合并为 **W1-8**
- 原 #24（Pipeline Builder DAG 保存）→ 并入 **W1-14** 子能力
- 原 #17（Funnel 可视化）→ 对应 **W1-3** 子能力，不单列
- 原 #8（OMA Function Type Editor）→ 对应 **W1-10 + W1-18** 子能力，不单列


#### 1.2.3 W2+ 高优先级项（27 项 · Phase 7+）

> W1 Wave 完成后优先推进。部分项为 W1 项的延伸增强（如 Pipeline Builder 变换系统是 W1-14 的完整版）。

| # | 差距项 | 当前 | 目标 | 所属模块 | 状态 |
| --- | --- | --- | --- | --- | --- |
| 1 | 媒体集类型化创建 | 通用上传 | DICOM/音频/文档/图像等媒体类型 + 延迟策略选择 | — | ✅ 已完成（W2-E·10 测试·lazy/eager/stream 三策略） |
| 2 | 媒体集→表格行变换 | 独立 API 解析 | Pipeline Builder 内置 "将媒体集转换为表格行" + mediaReference 标准类型 | — | ✅ 已完成（W2-E·8 测试·media_set NodeKind + 预览） |
| 3 | Ontology 对象类型输出 | 无 | 流水线输出 → 对象类型 → 设主键 → Object Explorer 查看 | — | ✅ 已完成（W2-A·15 测试） |
| 4 | Data Lineage（L1） | 静态列表 | 交互式 DAG 图/22 种着色/4 种节点/甘特图/列级血缘 | — | ✅ 已完成（W2-E·16 测试·22 色板 + DAG 布局 + 列级血缘 CRUD） |
| 5 | Pipeline Builder 变换系统 | 无 | 可视化变换（Join/Union/筛选/Cast）/200+ 函数/地理空间/流式合并 | — | ✅ 已完成（W2-C·15 算子 + 50 标量函数库） |
| 6 | Pipeline Builder 输出系统 | 仅 dataset | Ontology 对象/链接类型/地理时间序列/6 种写入模式 | — | ✅ 已完成（W2-A·12 测试） |
| 7 | Pipeline Builder AIP/LLM | embed 基础设施 | AIP 生成/解释/命名/助手/LLM 节点（7 种模板） | — | ✅ 已完成（W2-B·12 测试） |
| 8 | Dynamic Scheduling 引擎 | Cron UI 无 daemon | 真 cron daemon + 事件触发 + 搭建范围 + 失败操作 | — | ✅ 已完成（W2-A·22 测试） |
| 9 | Dynamic Scheduling 数据模型 | 无 | Schedule/Resource 对象 + 链接 + 类型类 + Ontology Manager 向导 | — | ✅ 已完成（W2-A·22 测试） |
| 10 | Dynamic Scheduling 甘特图 | 无 | 交互式甘特图/5 种分配行为/拖动创建/搜索栏/违规筛选/用户偏好 | — | ✅ 已完成（W2-D·13 测试） |
| 11 | Funnel 索引管道执行引擎 | W1-5 核心已完成 | 双管道/全量重索引触发/CDC（增强版） | — | ✅ 已完成（W2-F·13 测试·CDC `_op` 识别 + snapshot/incremental 双管道 + reindex 水位重置） |
| 12 | OE 探索图表可视化 | 无 | 7 种图表/拖拽排序/撤销重做/保存设计 | — | ✅ 已完成（W2-C·13 测试） |
| 13 | Object Views 可配置中心 | 硬编码属性网格 | 微件系统/可视化编辑器/10+ 种微件 | — | ✅ 已完成（W2-C·12 测试） |
| 14 | Action 规则可视化 | 无 | 创建/修改/删除/链接规则可视化配置 | — | ✅ 已完成（W2-C·12 测试） |
| 15 | Action 函数规则 | 无 | 引用 Ontology 编辑函数 | — | ✅ 已完成（W2-C·7 测试） |
| 16 | Action 可视化编辑器 | JSON | 拖拽参数/创建向导/实时预览 | — | ✅ 已完成（W2-C·15 测试） |
| 17 | Logic Block 全量 | W1-2 核心已完成 | LangGraph/Wiki 字段（增强版） | — | ✅ 已完成（W2-F·12 测试·Block wiki_ref 注入 + LogicGraph 条件路由图编排 + 环路保护） |
| 18 | 工具集注册 | W1-2 核心已完成 | Capability 深度集成（增强版） | — | ✅ 已完成（W2-B·15 测试·增强版） |
| 19 | Ontology 写回四步 | W1-2 核心已完成 | Workshop 绑定（增强版） | — | ✅ 已完成（W2-F·16 测试·WritebackLayer workshop_module 绑定/解绑 + 按模块预览合并视图） |
| 20 | Pipeline 多数据源支持 | 无 | 订单 Join 商品 Join 买家 | — | ✅ 已完成（W2-A·7 测试） |
| 21 | @transform 装饰器语法 | 无 | Python @transform 装饰器 | — | ✅ 已完成（W2-B·10 测试） |
| 22 | Web IDE | 无 | 基于 Web 的代码编辑器/IntelliSense/静态检查 | — | ✅ 已完成（W2-E·18 测试·会话/文件/诊断/补全/符号/hover） |
| 23 | Data Connection 增量同步 | 无 | 单调递增列+WHERE column > ?+初始值 | — | ✅ 已完成（W2-A·6 测试） |
| 24 | Data Connection 事务类型 | 无 | APPEND/SNAPSHOT/UPDATE | — | ✅ 已完成（W2-C·data_transaction 模块 + connector dispatch 集成） |
| 25 | 多语言 Transform（Python/Java/SQL/R） | 无 | @transform 装饰器/SDK/本地预览/增量变换 | — | ✅ 已完成（W2-B·11 测试） |
| 26 | Functions 运行时 | 无 | TS/Python 沙箱/Ontology API/Workshop 集成 | — | ✅ 已完成（W2-B·16 测试） |
| 27 | AIP Logic 无代码编辑器 | mock UI | 三栏 UI/Block 全量/Ontology 写回/Automate | — | ✅ 已完成（W2-C·LogicCanvasPage 8 Block 类型 + 拖拽 + CoT 调试） |

#### 1.2.4 W2+ 中优先级项（166 项 · Phase 8+）

> 按模块逐步推进，优先选择与 W1 已建基础设施衔接的项。
> **W2-G 第一批已交付**：#15 Expectation + #16 WriteMode + #17 Transaction 状态机（3 项）

| # | 差距项 | 当前 | 目标 | 状态 |
| --- | --- | --- | --- | --- |
| 1 | Connection CDC | 无 | Debezium 参考 | ✅ 已完成（W2-AY·19 测试·ConnectionCdcEngine CdcConfig cdc_id+connection_id+enabled+capture_mode full|incremental|snapshot+snapshot_interval_hours+max_backlog_records+last_capture_at+status running|stopped|paused|error+error_message+created_at+updated_at + configure_cdc 生成 cdc-* + get_cdc + list_cdc 按 connection_id+status 过滤 + update_cdc + delete_cdc + toggle_cdc + 200 条上限 FIFO + MISSING_CONNECTION/INVALID_CAPTURE_MODE/INVALID_STATUS/NOT_FOUND 校验） |
| 2 | Pipeline 画布 | 有 | 真 DAG 编排 | ✅ 已完成（W2-BA·25 测试·PipelineCanvasEngine PipelineNode node_id+pipeline_id+node_type transform|input|output|branch|merge|loop|conditional+name+config+x+y+width+height+status pending|running|completed|failed+error_message+created_at+updated_at + PipelineEdge edge_id+pipeline_id+source_node_id+source_port+target_node_id+target_port+edge_type data|control|conditional+created_at + CRUD create_node/pn-*/get_node/list_nodes 按 pipeline_id+node_type+status 过滤/update_node/delete_node + create_edge/pe-*/get_edge/list_edges 按 pipeline_id+source_node_id+target_node_id 过滤/delete_edge + validate_dag 模拟返回 cycles/isolated_nodes/dangling_edges + 200 条上限 FIFO + MISSING_PIPELINE/MISSING_NAME/INVALID_NODE_TYPE/INVALID_EDGE_TYPE/NOT_FOUND 校验） |
| 3 | Code Repositories | 无 | Transform 代码管理 | ✅ 已完成（W2-BA·17 测试·CodeRepositoryEngine CodeRepository repo_id+name+repository_type git|local|s3+location+branch+commit_hash+last_sync_at+status active|inactive|syncing|error+error_message+created_at+updated_at + CodeFile file_id+repo_id+file_path+content+last_modified_at+version + create_repo 生成 cr-* + get_repo + list_repos 按 name+repository_type+status 过滤 + update_repo + delete_repo + sync_repo inactive→syncing→active + list_files/get_file/update_file/delete_file + 200 条上限 FIFO + MISSING_NAME/MISSING_LOCATION/INVALID_REPOSITORY_TYPE/NOT_FOUND 校验） |
| 4 | Schedule 触发机制 | UI 有 | 上游/逻辑变更触发 | ✅ 已完成（W2-AY·22 测试·ScheduleTriggerEngine ScheduleTrigger trigger_id+name+cron_expression+timezone+enabled+target_type pipeline|workflow|function+target_id+last_triggered_at+next_trigger_at+status active|inactive|paused+created_at+updated_at + create_trigger 生成 str-* + get_trigger + list_triggers 按 name+target_type+target_id+status 过滤 + update_trigger + delete_trigger + toggle_trigger + 200 条上限 FIFO + MISSING_NAME/INVALID_CRON/INVALID_TARGET_TYPE/INVALID_STATUS/NOT_FOUND 校验） |
| 5 | MediaSet 分片 | 无 | 大文件分片 | ✅ 已完成（W2-BA·20 测试·MediaSetShardingEngine MediaShard shard_id+media_set_id+shard_index+total_shards+file_path+size_bytes+checksum+status pending|uploading|completed|failed+uploaded_at+error_message+created_at + create_shard 生成 ms-* + get_shard + list_shards 按 media_set_id+status 过滤 + update_shard + delete_shard + complete_upload pending|uploading→completed + fail_upload pending|uploading→failed + get_upload_status 聚合所有分片状态返回 progress/total/complete/failed/pending + 200 条上限 FIFO + MISSING_MEDIA_SET/INVALID_SHARD_INDEX/INVALID_STATUS/NOT_FOUND 校验） |
| 6 | MediaSet 浏览器 | 无 | Document/Spreadsheet 分型 | ✅ 已完成（W2-BB·14 测试·MediaSetBrowserEngine BrowserItem id+media_ref_id+name+type+size_bytes+created_at + browse_items(media_set_id, file_type) + get_item + search_items + create_item + delete_item + get_item_preview + 200 条上限 FIFO + MEDIA_SET_NOT_FOUND/ITEM_NOT_FOUND 校验） |
| 7 | 媒体集内容查看与交互 | JSON 元数据列表 | DICOM 对比度/曝光拖动调整 + 文件在线预览 | ✅ 已完成（W2-BB·17 测试·MediaInteractionEngine MediaView view_id+media_ref_id+view_type dicom|document|image|video+brightness+contrast+zoom+pan_x+pan_y+rotation+annotations+created_at+updated_at + ViewAnnotation id+view_id+type+content+x+y + create_view/mv-*/get_view/update_view/delete_view + get_annotations/add_annotation/delete_annotation + 200 条上限 FIFO + MEDIA_REF_NOT_FOUND/NOT_FOUND 校验） |
| 8 | 音频转录（ASR）变换 | 无 | "将音频转录为文本"内置变换 + 自动语言推断 | ✅ 已完成（W2-BB·18 测试·AudioTranscriptionEngine TranscriptionJob job_id+media_ref_id+status pending|processing|completed|failed+language auto|zh|en|ja|ko+transcript_text+confidence+timestamps+error_message+created_at+completed_at + create_job/at-*/get_job/list_jobs 按 media_ref_id+status 过滤 + cancel_job + get_transcript + estimate_language 自动推断语言 + 200 条上限 FIFO + MEDIA_REF_NOT_FOUND/INVALID_LANGUAGE/NOT_FOUND 校验） |
| 9 | DICOM 医学影像支持 | 无 | DICOM 格式识别 + Patient ID/Study ID 自动提取 + 图像渲染 | ✅ 已完成（W2-BC·15 测试·DicomEngine DicomMetadata dicom_id+media_ref_id+patient_id+patient_name+study_id+study_date+series_id+modality+manufacturer+image_count+pixel_spacing+slice_thickness+window_center+window_width+created_at + extract_metadata/dic-*/get_metadata/list_metadata 按 media_set_id+patient_id+study_id 过滤/render_image 支持 window_center/window_width/delete_metadata + 200 条上限 FIFO + MEDIA_REF_NOT_FOUND/NOT_FOUND 校验） |
| 10 | Workshop 自动生成 | 无 | 对象类型 → 自动生成 Workshop 模块（对象表+预览） | ✅ 已完成（W2-BC·15 测试·WorkshopAutoGenEngine WorkshopTemplate template_id+object_type+name+description+table_columns[]+preview_config+generated_at+updated_at + generate_workshop/wst-*/get_template/list_templates 按 object_type 过滤/update_template/delete_template/preview_template + 200 条上限 FIFO + INVALID_OBJECT_TYPE/NOT_FOUND 校验） |
| 11 | AIP Doc Intel 五步法 | 无 | OCR→MD→抽字段→校验→回链 | ✅ 已完成（W2-BC·18 测试·DocIntelEngine DocIntelJob job_id+media_ref_id+status pending|ocr|md_conversion|field_extraction|validation|linking|completed|failed+current_step+ocr_result+md_content+extracted_fields+validation_result+linked_entities+error_message+created_at+updated_at + create_job/di-*/get_job/list_jobs 按 media_ref_id+status 过滤/run_step 推进单步/run_all_steps 完整流程/cancel_job/get_extracted_fields + 200 条上限 FIFO + MEDIA_REF_NOT_FOUND/INVALID_STEP/NOT_FOUND 校验） |
| 12 | Use LLM 节点 | 无 | 实体提取/视觉模板 | ✅ 已完成（W2-BD·15 测试·LlmNodeEngine LlmNode node_id+name+node_type entity_extraction|visual_template|text_classification|summarization+prompt_template+model_name+temperature+max_tokens+input_schema+output_schema+enabled+created_at+updated_at + create_node/ln-*/get_node/list_nodes 按 node_type+enabled 过滤/update_node/delete_node/execute_node + 200 条上限 FIFO + MISSING_NAME/INVALID_NODE_TYPE/NOT_FOUND 校验） |
| 13 | Agent Proxy/Worker | 无 | 内网反向代理 | ✅ 已完成（W2-BD·17 测试·AgentProxyEngine AgentProxy proxy_id+name+proxy_type reverse_proxy|forward_proxy|load_balancer+target_url+listen_port+enabled+health_status healthy|unhealthy|degraded+last_health_check_at+error_message+created_at+updated_at + create_proxy/ap-*/get_proxy/list_proxies 按 proxy_type+health_status 过滤/update_proxy/delete_proxy/toggle_proxy/health_check + 200 条上限 FIFO + MISSING_NAME/MISSING_TARGET_URL/INVALID_PROXY_TYPE/NOT_FOUND 校验） |
| 14 | 存储路由向导 | 无 | Dataset/MediaSet/Stream 选择 | ✅ 已完成（W2-AY·29 测试·StorageRouteGuideEngine StorageRoute route_id+name+source_path+target_path+route_type copy|move|sync|mirror+schedule_type on_demand|periodic|event+schedule_cron+enabled+status active|inactive|running|completed|failed+last_run_at+error_message+created_at+updated_at + create_route 生成 srg-* + get_route + list_routes 按 name+route_type+schedule_type+status 过滤 + update_route + delete_route + execute_route 模拟运行 running→completed + 200 条上限 FIFO + MISSING_NAME/MISSING_SOURCE_PATH/MISSING_TARGET_PATH/INVALID_ROUTE_TYPE/INVALID_SCHEDULE_TYPE/NOT_FOUND 校验） |
| 15 | Expectation | 无 | PK 唯一/行数检查 | ✅ 已完成（W2-G·16 测试·pk_unique + row_count + severity + check_all） |
| 16 | Write Mode | data_transaction.py 有 append/snapshot/update | Default/Append/Snapshot | ✅ 已完成（W2-G·16 测试·新增 default 模式 + describe API + 4 种写入模式） |
| 17 | Transaction 状态机 | 无 | OPEN/COMMITTED/ABORTED | ✅ 已完成（W2-G·22 测试·DataTransaction 状态机 + write_mode 集成 + 不可逆转换） |
| 18 | Pipeline Builder 分支版本 | disabled | 创建/审批/合并/rebase/保护/回退分支 | ✅ 已完成（W2-AZ·20 测试·PipelineBranchEngine PipelineBranch branch_id+pipeline_id+name+base_branch_id+status draft|review|approved|merged|reverted+protection_enabled+protection_rules+created_by+created_at+updated_at + create_branch 生成 pb-* + get_branch + list_branches 按 pipeline_id+status 过滤 + update_branch + delete_branch + approve_branch draft|review→approved + merge_branch approved→merged + revert_branch merged→reverted + 200 条上限 FIFO + MISSING_PIPELINE/MISSING_NAME/INVALID_STATUS/NOT_FOUND 校验） |
| 19 | Pipeline Builder 管道管理 | 无 | 搭建设置/检查点/颜色组/自定义函数/文件夹/采样/任务组/参数 | ✅ 已完成（W2-AZ·14 测试·PipelineManagementEngine PipelineConfig config_id+pipeline_id+checkpoints+color_groups+custom_functions+folders+sampling_config+task_groups+parameters+created_at+updated_at + create_config 生成 pc-* + get_config + get_config_by_pipeline + list_configs 按 pipeline_id 过滤 + update_config + delete_config + 200 条上限 FIFO + MISSING_PIPELINE/NOT_FOUND 校验） |
| 20 | Pipeline Builder 数据期望 | 无 | 主键/行数期望/健康检查/单元测试 | ✅ 已完成（W2-AZ·21 测试·PipelineDataExpectationEngine DataExpectation expectation_id+pipeline_id+name+expectation_type primary_key|row_count|column_distinct|column_nulls|custom_sql+config+severity critical|warning|info+enabled+last_checked_at+last_result+created_at+updated_at + create_expectation 生成 de-* + get_expectation + list_expectations 按 pipeline_id+expectation_type+severity+enabled 过滤 + update_expectation + delete_expectation + run_expectation 模拟运行推进 last_checked_at+last_result + run_all_expectations + 200 条上限 FIFO + MISSING_PIPELINE/MISSING_NAME/INVALID_EXPECTATION_TYPE/INVALID_SEVERITY/NOT_FOUND 校验） |
| 21 | Dataset Preview 列统计 | 无 | 列级空值%/分布/样本/列信息面板 | ✅ 已完成（W2-AX·18 测试·ColumnStatsEngine ColumnStats stats_id+dataset_rid+column_name+null_count+null_percent+distinct_count+distinct_percent+min_value+max_value+mean+median+std_dev+sample_values+data_type+total_rows+last_computed_at + compute_stats 生成 stats_id=cs-* + get_stats + list_stats 按 dataset_rid+column_name+data_type 过滤 + delete_stats + 200 条上限 FIFO + MISSING_DATASET/MISSING_COLUMN/NOT_FOUND 校验） |
| 22 | Dataset Preview 附加视图 | 4 个极简 Tab | About/Columns/Schedule 面板 + 6 个附加视图 + 数据集对比 | ✅ 已完成（W2-AX·21 测试·DatasetPreviewViewsEngine PreviewView view_id+dataset_rid+view_type table|chart|profile|comparison+config_data+enabled+created_at+updated_at + register_view 生成 view_id=pv-* + get_view + list_views 按 dataset_rid+view_type+enabled 过滤 + update_view + delete_view + 200 条上限 FIFO + MISSING_DATASET/INVALID_VIEW_TYPE/NOT_FOUND 校验） |
| 23 | Dynamic Scheduling Scenarios | 无 | 假设分析沙箱/暂存编辑/Save Action/Function-backed 自定义保存 | ✅ 已完成（W2-BD·18 测试·DynamicSchedulingEngine SchedulingScenario scenario_id+name+scenario_type sandbox|staging|save_action|custom_save+constraints[]+suggestion_rules[]+search_rules[]+realtime_evaluation+enabled+created_at+updated_at + create_scenario/ds-*/get_scenario/list_scenarios 按 scenario_type+enabled 过滤/update_scenario/delete_scenario/run_evaluation/apply_scenario + 200 条上限 FIFO + MISSING_NAME/INVALID_SCENARIO_TYPE/NOT_FOUND 校验） |
| 24 | Dynamic Scheduling 智能函数 | 无 | Suggestion Function（评分-1~1）+ Search Function（右键触发） | ✅ 已完成（W2-BE·16 测试·SchedulingSmartFunctionsEngine SmartFunction function_id+name+function_type suggestion|search|filter|sort+description+enabled+created_at+updated_at + SuggestionResult function_id+entity_id+score+reason+metadata+created_at + create_function/sf-*/get_function/list_functions 按 function_type+enabled 过滤/update_function/delete_function/suggest 返回评分-1~1/search + 200 条上限 FIFO + MISSING_NAME/INVALID_FUNCTION_TYPE/NOT_FOUND 校验） |
| 25 | Dynamic Scheduling 验证规则 | 无 | HARD+SOFT 约束/实时重评估/编排流程/自定义描述 | ✅ 已完成（W2-BE·18 测试·SchedulingValidationEngine ValidationRule rule_id+name+rule_type hard|soft+constraint_expression+description+severity critical|warning|info+enabled+created_at+updated_at + ValidationResult result_id+rule_id+entity_id+passed+violation_details+severity+evaluated_at + create_rule/vr-*/get_rule/list_rules 按 rule_type+severity+enabled 过滤/update_rule/delete_rule/validate/validate_all + 200 条上限 FIFO + MISSING_NAME/INVALID_RULE_TYPE/INVALID_SEVERITY/NOT_FOUND 校验） |
| 26 | Data Health | 无 | 行数漂移/模式变更检查 | ✅ 已完成（W2-AX·24 测试·DataHealthCheckEngine DataHealthCheck check_id+dataset_rid+check_type freshness|volume|schema|nulls|uniqueness|range+config+status pending|running|passed|failed|errored+last_run_at+last_result+severity critical|warning|info+created_at+updated_at + register_check 生成 check_id=hc-* + get_check + list_checks 按 dataset_rid+check_type+status+severity 过滤 + update_check + delete_check + run_check 模拟运行推进 last_run_at+last_result + 200 条上限 FIFO + MISSING_DATASET/INVALID_CHECK_TYPE/INVALID_STATUS/INVALID_SEVERITY/NOT_FOUND 校验） |
| 27 | OKF Lint | 无 | 列漂移检测/契约校验 | ✅ 已完成（W2-BE·18 测试·OkfLintEngine LintRule rule_id+name+rule_type column_drift|contract_violation|data_quality|schema_change+severity critical|warning|info+enabled+created_at+updated_at + LintResult result_id+rule_id+dataset_rid+passed+violation_details+severity+drift_metrics+evaluated_at + create_rule/ol-*/get_rule/list_rules 按 rule_type+severity+enabled 过滤/update_rule/delete_rule/lint 全量检查/get_drift_report + 200 条上限 FIFO + MISSING_NAME/INVALID_RULE_TYPE/INVALID_SEVERITY/NOT_FOUND 校验） |
| 28 | OMA Property Editor | 无 | backing column/title key/TSP | ✅ 已完成（W2-J·21 测试·独立 PropertyEditor + backing_column/dataset + title_key + TSP + origin_mapping） |
| 29 | 类型严格一致（Type Coherence） | 无 | L1/L2 Schema 冲突检测 | ✅ 已完成（W2-L·25 测试·TypeCoherenceEngine TC-01~TC-04 冲突检测 + 类型兼容组 + check_all） |
| 30 | 多源异构解法（A/C） | 仅解法 B | L1 Join 宽表 + Function 派生 | ✅ 已完成（W2-L·25 测试·L1JoinEngine 解法A宽表配置+预览 + 解法C ComputedProperty 函数绑定） |
| 31 | 图谱健康度 | 有基础 | 悬空 Link/冲突/僵尸检测 | ✅ 已完成（W2-I·graph-health 端点已覆盖 dangling/conflict/orphan/score/issues/archive） |
| 32 | Ontology Interface（接口类型） | 无 | Object 多态抽象/共同形状描述 | ✅ 已完成（W2-K·24 测试·InterfaceEngine CRUD + extends 继承 + implement 实现 + effective_properties + 删除保护） |
| 33 | Ontology Shared Property（共享属性） | 无 | 跨 Object 类型复用属性/集中管理 | ✅ 已完成（W2-L·25 测试·SharedPropertyEngine CRUD + attach/detach 引用绑定 + 删除保护） |
| 34 | OMA Property 独立编辑器 | 行内编辑 | 独立 Property Editor/backing column/title key/TSP | ✅ 已完成（W2-J·21 测试·独立 Property CRUD API + 7 端点 + 与 #28 合并实现） |
| 35 | Ontology Proposals 审查工作流 | 分支 CRUD | 提案分支→审查→批准→发布/PR 式协作 | ✅ 已完成（W2-J·21 测试·ProposalEngine 7态状态机 + submit/review/approve/reject/withdraw/publish + 评论+审查者） |
| 36 | OMA 编辑历史/恢复 | 无 | 全局时间线/按作者合并/逐条回退 | ✅ 已完成（W2-K·24 测试·EditHistoryEngine 全局时间线 + 按作者合并 + 逐条回退 + 批量回退） |
| 37 | Ontology 清理工具 | 无 | 延迟/弃用/删除三级+6 种清理标记 | ✅ 已完成（W2-K·24 测试·CleanupEngine 3 级操作 + 6 种标记自动扫描 + 正则筛选 + 批量操作） |
| 38 | Ontology 使用指标 | 基础计数 | Reads/Writes/Active Users 30 天/使用来源归因 | ✅ 已完成（W2-I·21 测试·UsageMetricsEngine 30天滑动窗口+多维度+来源归因） |
| 39 | Object 存储后端（专职引擎） | PG JSONB | OSv2 分布式索引/数十亿级/Spark 查询 | ✅ 已完成（W2-BF·51 测试·ObjectStorageEngine 三层索引 primary/secondary/composite + shard/replication + rebuild + stats + 200 条 FIFO） |
| 40 | 对象增量索引（Diff-based） | 全量 upsert | 自动差异计算/仅索引变化行 | ✅ 已完成（W2-BF·51 测试·DeltaIndexEngine create/get/list/apply/revert + version 校验 + stats + 200 条 FIFO） |
| 41 | 流式对象索引 | 无 | Flink/CDC/每 OT 2MB/s | ✅ 已完成（W2-BF·51 测试·StreamIndexEngine kafka/flink/cdc 三种源 + start/stop/pause + processing_rate + stats + 200 条 FIFO） |
| 42 | 对象编辑冲突解决 | 无 | 用户优先/时间戳优先两种策略 | ✅ 已完成（W2-N·26 测试·ConflictEngine 检测+解决 + user_priority/timestamp_priority 两种策略 + 用户优先级配置） |
| 43 | 对象物化（Materializations） | 无 | 自动输出对象数据为数据集/6h 周期 | ✅ 已完成（W2-BG·58 测试·MaterializationEngine auto/manual/scheduled 三类型 + 6h 间隔 + run_materialization + 200 条 FIFO） |
| 44 | 对象模式迁移 | 无 | 5 种迁移指令/每批 500 编辑 | ✅ 已完成（W2-N·26 测试·MigrationEngine ADD/REMOVE/RENAME/CHANGE_TYPE/SET_NULLABLE 5 指令 + 批次 500 上限 + dry_run + 状态跟踪） |
| 45 | 对象编辑历史追踪 | decision_lineage | 对象属性变更时间线/开关控制 | ✅ 已完成（W2-N·26 测试·ChangeLogEngine per-OT 开关 + record/record_force + 多维查询 + 时间线 + 时间范围筛选） |
| 46 | 受限视图（RV·行级权限） | 无 | 动态行级策略/医生仅看自己患者 | ✅ 已完成（W2-BG·58 测试·RowLevelEngine filter/mask/join 三类型 + condition_expression + evaluate/evaluate_all + 200 条 FIFO） |
| 47 | MDO 多数据源对象（列级权限） | 无 | 不同属性不同数据源/最多 70 源 | ✅ 已完成（W2-BG·58 测试·ColumnLevelEngine include/exclude/mask/encrypt 四类型 + max_sources 70 + evaluate 返回 accessible/masked/excluded + 200 条 FIFO） |
| 48 | OE 高级搜索语法 | 基础搜索 | AND/OR/通配符/模糊搜索/按链接筛选 | ✅ 已完成（W2-M·30 测试·SearchEngine 表达式解析器 + 8 操作符 + LINKS 筛选 + 分页） |
| 49 | OE 保存探索/列表 | 无 | 动态探索+静态列表/私人与公共保存 | ✅ 已完成（W2-M·30 测试·ExplorationEngine CRUD + dynamic/static + private/public + execute 动态探索） |
| 50 | OE 批量操作/导出 | Action 发起 | Excel 导出/在其他应用打开 | ✅ 已完成（W2-M·30 测试·ExportEngine csv/excel(BOM)/json + 列筛选 + ID 筛选 + bulk_update/bulk_delete） |
| 51 | Object Views 配置文件 | 无 | 不同用户组不同标签页/可切换 | ✅ 已完成（W2-O·34 测试·ViewProfileEngine CRUD + activate 激活 + get_active 默认回退 + ViewTab 标签页配置） |
| 52 | 完整类型系统（20+ 基础类型） | string/number/bool | Timestamp/Vector/Attachment/TimeSeries/MediaReference/Cipher | ✅ 已完成（W2-O·34 测试·TypeSystem 22 内置类型 5 类别 scalar/temporal/binary/composite/security + validate + coerce + 自定义注册） |
| 53 | 值类型/条件格式化/类型类 | 无 | 语义约束/标准比较规则/30+ 类型类/渲染提示 | ✅ 已完成（W2-O·34 测试·FormatEngine 32 内置类型类 + render 渲染 + ConditionalFormat 条件格式 > / < / = / != / contains 评估） |
| 54 | Action Side Effects | 无 | Notification/Webhook | ✅ 已完成（W2-H·22 测试·notification/webhook 副作用注册+触发） |
| 55 | Action 乐观 UI | 无 | 前端先改态/失败回滚 | ✅ 已完成（W2-H·22 测试·optimistic token + commit/rollback） |
| 56 | Action 软删除 | 物理删除 | is_deleted 标记 | ✅ 已完成（W2-H·22 测试·复用 writeback soft_delete + undelete） |
| 57 | Action 副作用重试 | 无 | retry×3 → DLQ | ✅ 已完成（W2-H·22 测试·重试机制 + DLQ 死信队列 + retry/clear API） |
| 58 | Action 参数约束 | JSON 配置 | User Input/Multiple Choice/从 Object Set 取选项 | ✅ 已完成（W2-P·42 测试·ConstraintEngine user_input/multiple_choice/object_set 三类型 + min/max/pattern/required 校验 + get_options 候选项 + Object Set 注册） |
| 59 | Action 参数默认值 | 无 | 静态值/对象属性/类型类/环境变量 | ✅ 已完成（W2-P·42 测试·DefaultEngine static/object_property/type_class/environment 4 来源 + resolve 动态求值 + fallback 回退 + 对象注册） |
| 60 | Action 参数覆盖 | 无 | 条件覆盖块/Visible/Disabled/Required 三态 | ✅ 已完成（W2-P·42 测试·OverrideEngine 条件评估 = / != / > / < / >= / <= + visible/disabled/required 三态合并 + 多覆盖块叠加 + applied_overrides 追踪） |
| 61 | Action 参数筛选 | 无 | 对象下拉起始集/搜索范围/安全性筛选 | ✅ 已完成（W2-Q·45 测试·FilterEngine base_set/object_pool 起始集 + search_scope 属性限定 + security_filter 表达式筛选 + ordering 排序 + {{var}} 模板替换） |
| 62 | Action 提交标准可视化 | JSON | 条件模板/逻辑运算符/失败消息可视化 | ✅ 已完成（W2-Q·45 测试·CriteriaEngine 条件树 AND/OR/NOT 嵌套 + 叶子节点 = / != / > / < / >= / <= / contains / in / exists 10 操作符 + severity error/warning + failure_message） |
| 63 | Action 通知副作用 | 无 | 静态/参数/对象属性/函数收件人 + 模板内容 | ✅ 已完成（W2-Q·45 测试·NotificationEngine static/parameter/object_property/function 4 来源收件人 + {{var}} 模板渲染 subject/body + email/sms/in_app 3 渠道 + dispatch 派发队列 + 派发记录查询） |
| 64 | Action Webhook 副作用 | 无 | 数据输出模式/副作用模式/输入输出映射 | ✅ 已完成（W2-R·13 测试·data_output/side_effect 模式 + input/output_mapping + bearer/basic/hmac 认证 + {{var}} 模板 + dot-path 响应提取） |
| 65 | Action Sections 分组 | 无 | 单列双列布局/折叠/条件显示 | ✅ 已完成（W2-R·13 测试·single_column/double_column 布局 + span 半宽/全宽 + visible_condition 条件显示 + collapsed 折叠 + 批量 reorder 重排序） |
| 66 | Action 撤销（Revert） | 无 | 提交后立即撤销/条件检查 | ✅ 已完成（W2-R·15 测试·revert_window_seconds 时间窗口 + pre_revert_check 条件树 AND/OR/NOT + 6 态状态机 pending/eligible/in_progress/completed/failed/blocked + RevertRecord 记录追踪） |
| 67 | Action 日志对象类型 | 无 | [LOG] 前缀/操作 RID/版本/时间戳/参数值 | ✅ 已完成（W2-S·10 测试·[LOG]ActionName 类型自动生成 + operation_rid 全局唯一 + version 自增 + 参数快照 + submitted/succeeded/failed/reverted 状态 + 按版本号排序） |
| 68 | Action 平台集成 | 无 | 对象视图/Object Explorer/Workshop 按钮组 | ✅ 已完成（W2-S·16 测试·ActionBinding object_view/object_explorer/workshop 三集成 + primary/secondary/overflow 按钮位置 + visibility_condition 条件 + WorkshopButtonGroup horizontal/vertical 布局 + attach/detach 幂等 + 级联清理） |
| 69 | Ontology 图查询 | 基础 | 多跳/路径 | ✅ 已完成（W2-I·21 测试·多跳 BFS + 双向 BFS 最短路径 + 子图扩展） |
| 70 | Action 事务回滚 | 无 | 补偿事务 | ✅ 已完成（W2-S·18 测试·SagaTransaction 6 态状态机 pending→running→completed/compensating→compensated/failed + forward/compensation 步骤记录 + 补偿按 order 倒序 + 自动状态推进 + 级联删除 + get_state 进度快照） |
| 71 | k-LLM 智能路由 | 无 | 智能选模型 | ✅ 已完成（W2-T·12 测试·SmartRouter 5 维评分 capability/context/cost/security/tag + 硬过滤 + alternatives + score_breakdown） |
| 72 | k-LLM 场景化路由 | 无 | 按任务类型选模/块级选模 | ✅ 已完成（W2-T·15 测试·ScenarioRouter RouteRule + BlockRoute + resolve 块级>场景>默认三级回落 + export/import 与 81 协议对齐） |
| 73 | k-LLM 熔断/热切换 | 无 | 主模失败自动切回退 | ✅ 已完成（W2-T·15 测试·FailoverEngine 3 态状态机 closed/open/half_open + cooldown 推进 + call_with_failover 主备热切换 + circuit-drill 演练） |
| 74 | 数据出境策略 | 无 | 敏感标记强制私有路由 | ✅ 已完成（W2-U·16 测试·EgressPolicyEngine SensitiveField 标记 + EgressPolicy allow/restricted/forbidden + mask_before_egress 字段级脱敏 + audit_sample_rate 抽检 + EgressDecision + EgressAuditRecord 审计） |
| 75 | 自定义 LLM 注册 | 无 | Function Interfaces/Source/Webhook | ✅ 已完成（W2-U·15 测试·CustomLLMRegistry FunctionInterface/LLMSource/LLMWebhook 三形态 CRUD + source_type 4 类型 + webhook method/auth 校验 + list_all 统一视图） |
| 76 | Edits 合并策略 | 无 | 字段级/LastWriteWins/人工仲裁 | ✅ 已完成（W2-H·22 测试·field_level/last_write_wins/manual_arbitration 三种策略） |
| 77 | Prompt 工程 | 无 | 变量注入/Few-shot/版本 | ✅ 已完成（W2-U·14 测试·PromptEngine PromptTemplate CRUD + {{var}} 变量注入 + few_shot_examples Few-shot + version 版本自增 + activate_version 同 name 仅一个 active + render 渲染回退 + render_and_call 端到端） |
| 78 | 调试器 | 无 | CoT/提议预览 | ✅ 已完成（W2-V·14 测试·DebuggerEngine DebugSession/DebugStep + create_session 自动构造 input+execute 步骤 + step_forward/backward 步进 + run_to_completion + variables_after 变量快照 + ProposalPreview 提议预览 + apply_proposal 标记应用 + ALREADY_APPLIED 幂等） |
| 79 | Automate 集成 | 无 | 条件触发/提案 | ✅ 已完成（W2-V·13 测试·AutomateEngine AutomateTrigger CRUD + 5 种 event_type + _eval_condition eq/ne/gt/lt/ge/le 条件树 + cooldown_seconds 冷却期 + fire 触发流程 disabled/cooldown/condition 三重检查 + AutomateRun 执行记录 + proposal_id 关联提案 + trigger_count 计数） |
| 80 | 四层成熟度 | 无 | L1/L2/L3/L4 楼梯 | ✅ 已完成（W2-V·13 测试·MaturityEngine DEFAULT_LEVELS L1 基础/L2 辅助/L3 半自动/L4 全自动 + register_capability 能力注册 + assess 楼梯模型找最高满足 + L0 基线 + gaps gap 分析 + recommendation 文案 + set/get_target_level + list_assessments 历史 200 条） |
| 81 | Agent 六工具 | 基础 | Action/Query/Function/Var/Command/Clarify | ✅ 已完成（W2-BG·58 测试·AgentToolsEngine 六工具类型 + create/execute + get_tool_types 返回 6 种 + 200 条 FIFO） |
| 82 | L4 熔断 | 无 | 失败率>5%→降级 L3 | ✅ 已完成（W2-W·15 测试·L4CircuitEngine L4CircuitConfig window_size/failure_threshold 5%/recovery_threshold 2.5% 滞回/cooldown_seconds 60s + L4CircuitState current_level/degraded/failure_rate + record_call 滑动窗口 deque + 自动降级 L3 + 自动恢复滞回检查 + L4Alert degrade/recover 告警 + force_degrade/force_recover 演练 + 200 条上限 + reset） |
| 83 | 模型预热 | 无 | warm-up/冷启动处理 | ✅ 已完成（W2-W·13 测试·ModelWarmupEngine WarmupState cold/warming/ready/failed 4 态状态机 + register_model + warmup 注入 probe_callable + 失败退避 cooldown_until = 5s×count 上限 60s + mark_ready/mark_failed 外部探测器 + list_probe_results 200 条 + IN_COOLDOWN/NOT_FOUND 错误码） |
| 84 | Decision Lineage | 无 | 完整记录/可复盘 | ✅ 已完成（W2-X·12 测试·DecisionLineageEngine DecisionRecord 8+ 字段 logic_id/proposal_id/model_id/prompt_version/object_refs/wiki_fields/cot/tool_calls/draft_params/approval_result/actor/metadata + record/get/list 多维过滤 + get_timeline 时间线 Tool 调用 + 审批事件 + trace 按提案溯源 + 200 条上限淘汰 + NOT_FOUND 错误码） |
| 85 | Insight Backfill | 无 | 高置信结论→Insight Object | ✅ 已完成（W2-X·14 测试·InsightBackfillEngine BackfillConfig confidence_threshold 0.85/auto_backfill False/max_daily_backfill + register_insight confidence 校验 + get/list 多维过滤 source_decision_id/backfill_status/min_confidence + backfill 状态机 pending→completed + evaluate_and_register 阈值守门 BELOW_THRESHOLD + list_pending + cleanup 清理 failed + ALREADY_BACKFILLED 幂等 + INVALID_CONFIDENCE/INVALID_THRESHOLD 校验） |
| 86 | 三种提案通道 | 无 | 同步/异步 Automate/异步管道 | ✅ 已完成（W2-W·14 测试·ProposalChannelEngine DEFAULT_CHANNELS sync 同步通道即时 completed+approved/async_automate 异步 Automate 通道 pending/async_pipeline 异步管道通道 pending + ProposalSubmission 24h visible_until 安全窗口 + approve/reject/cancel 三态决策 + ALREADY_APPROVED/ALREADY_REJECTED/SUBMISSION_CANCELLED/SUBMISSION_FINAL 校验 + cleanup_expired 过期清理 + 200 条上限 + INVALID_CHANNEL/CHANNEL_DISABLED/INVALID_LOGIC_ID 校验） |
| 87 | Capability Adapter 契约 | 无 | Manifest/运行时 API/Facade | ✅ 已完成（W2-X·16 测试·CapabilityAdapterEngine AdapterManifest capability_class C0 同步/C1 异步 Job/C2 长会话分级 + auth_type none/bearer/basic/hmac + CRUD register/get/list/update/delete + update 禁改 capability_class IMMUTABLE_FIELD + invoke/submit/status/cancel/artifact/session_open/session_close 7 操作 + _check_adapter ADAPTER_DISABLED/INVALID_CLASS 校验 + invoke_callable 可注入默认 echo + status 5 状态机 + 200 条上限 + list_invocations 多维过滤） |
| 88 | CAP 约束 | 无 | CAP-01~07 | ✅ 已完成（W2-Y·15 测试·CapConstraintEngine DEFAULT_CAP_RULES 7 规则 CAP-01~07 + CapRule code/title/description/severity/enforcement block/audit/dry_run + check 返回 CapViolation resolution=blocked/audited/dry_run_passed + list_violations 按 code/target_type 过滤 + update 禁改 code IMMUTABLE_FIELD + 200 条上限 + NOT_FOUND/INVALID_ENFORCEMENT/INVALID_SEVERITY 校验） |
| 89 | Pipeline 界面四区域 | 部分 | 顶部工具栏/详细侧栏/提案/历史视图 | ✅ 已完成（W2-BH·36 测试·PipelineLayoutEngine 布局CRUD + 工具栏/侧栏操作 + 提案管理 + 历史记录 + 200 条 FIFO） |
| 90 | Pipeline 管理功能 | 无 | 参数/自定义函数/文件夹/检查点 | ⬜ 待执行 |
| 91 | Pipeline Ontology 输出 | 无 | 对象类型/链接类型输出配置 | ✅ 已完成（W2-AA·13 测试·LinkTypeOutputEngine LinkTypeDefinition cardinality one_to_many/many_to_one/many_to_many + source/target_object_type + source_pk_field/target_fk_field + display_field + CRUD register/get/get_by_name/list/update/delete + register 校验 INVALID_CARDINALITY/MISSING_NAME/MISSING_OBJECT_TYPE/MISSING_KEY_FIELD/NAME_DUPLICATE 重名 + update 改名重名校验 + infer_from_objects 默认 many_to_one + preview_links 返回链接实例 + 200 条上限） |
| 92 | Pipeline Expectation | 无 | PK 唯一/行数检查 | ✅ 已完成（清账·基础已存在·expectation.py ExpectationEngine PK_UNIQUE/ROW_COUNT 两类型 + check/check_all/has_blocking_failure + create/get/list_all + tests/test_expectation.py） |
| 93 | Pipeline Write Mode | 无 | Default/Append/Snapshot 选择 | ✅ 已完成（清账·基础已存在·pipeline_output.py PipelineOutputEngine 6 种 WriteMode append/snapshot/upsert/replace/update/delete + execute + PK_REQUIRED 校验 + tests/test_pipeline_output.py） |
| 94 | Pipeline Types（Batch/Incremental/Streaming） | 基础概念 | 三种管道类型区分及处理语义 | ✅ 已完成（W2-Z·14 测试·PipelineTypeEngine DEFAULT_PIPELINE_TYPES batch 批处理 scheduled+restart+append/incremental 增量 on_change+checkpoint_replay+upsert/streaming 流式 continuous+skip+append + PipelineTypeSpec trigger_semantics/state_machine/fault_strategy/supports_checkpoint/supports_windowing + CRUD register/get/list/update/delete + update 禁改 type IMMUTABLE_FIELD + validate_run 类型与 write_mode 匹配校验 + INVALID_TYPE/INVALID_TRIGGER/INVALID_FAULT_STRATEGY/NOT_FOUND 校验） |
| 95 | Incremental Pipeline | 无 | 增量处理/变更捕获 | ✅ 已完成（W2-Z·16 测试·IncrementalPipelineEngine Watermark 水位线 field/value + get/set_watermark + ChangeRecord CDC insert/update/delete + register_change/list_changes op+since_watermark 过滤 + Checkpoint pending→committed 状态机 sequence 自增 + create/commit/list_checkpoints + ALREADY_COMMITTED 幂等 + process_increment 取 watermark 之后变更→创建 checkpoint→处理→推进 watermark→提交 + 无变更 skipped + 200 条上限 + INVALID_OPERATION/INVALID_PK/INVALID_FIELD 校验） |
| 96 | Streaming Pipeline | 无 | 实时流式处理/状态化操作 | ✅ 已完成（W2-Z·15 测试·StreamingPipelineEngine WindowSpec tumbling/sliding/session 三窗口 + size_ms/slide_ms/gap_ms + StreamEvent key/event_ts + WindowState open/emitted + ingest tumbling floor 对齐/sliding 多窗口枚举/session 按 gap_ms 合并或新建 + advance_watermark 推进水位线关闭到期窗口 + close_window 手动关窗 + list_events/list_windows 过滤 + WATERMARK_REGRESS 水位线不可回退 + INVALID_WINDOW_TYPE/INVALID_SIZE/INVALID_GAP/NOT_FOUND 校验 + 200 条上限） |
| 97 | 事件触发器 | 无 | 上游数据集/管道构建完成触发 | ✅ 已完成（W2-AA·15 测试·EventTriggerEngine EventTrigger event_source dataset_updated/pipeline_built/schedule/manual 四源 + target_pipeline_id + cooldown_seconds 冷却期 + fire 检查 enabled→cooldown→fired 三状态 fired/skipped/cooldown + 推进 last_fired_at/fire_count + TriggerFire 点火记录 + list_fires 按 trigger_id 过滤 + 200 条 fire 上限 FIFO 淘汰 + register 校验 MISSING_NAME/INVALID_EVENT_SOURCE/MISSING_TARGET + update 改源校验 + NOT_FOUND） |
| 98 | 复合触发器 | 无 | AND/OR 逻辑组合触发器 | ✅ 已完成（W2-AA·14 测试·CompositeTriggerEngine CompositeTrigger logic and/or + child_trigger_ids 子触发器引用 + evaluate AND 全 True/OR 任一 True + child_fires 缺失视为 False + fire 通过 fired/未通过 skipped + 推进 fire_count + 200 条 fire 上限 + register 校验 MISSING_NAME/INVALID_LOGIC/EMPTY_CHILDREN/MISSING_TARGET + update 改逻辑校验 + NOT_FOUND） |
| 99 | 安全标记传播控制 | 无 | stop_propagating/stop_requiring 配置 | ✅ 已完成（W2-Y·15 测试·MarkingPropagationEngine MarkingPropagationConfig stop_propagating/stop_requiring/inherit_from_parent/expand_input_inheritance + MarkingRecord security_label public/internal/sensitive/restricted + propagate 检查 stop_propagating True 下游 public+is_inherited=False/False 拷贝源标签+is_inherited=True + 200 条上限 + NOT_FOUND 校验） |
| 100 | 标记移除策略 | 无 | filter-in/filter-out 移除策略 | ✅ 已完成（W2-Y·15 测试·MarkingRemovalEngine MarkingRemovalPolicy strategy filter_in/filter_out + removed_labels/keep_labels + apply_to_inherited + apply filter_in final=原∩keep_labels/filter_out final=原-removed_labels + apply_to_inherited=False 跳过继承标签但保留 + skipped_inherited 计数 + POLICY_DISABLED + 200 结果上限 + register 校验 filter_in 需 keep_labels 非空/filter_out 需 removed_labels 非空） |
| 101 | 代码仓库分支管理 | 无 | Git 分支创建/合并/删除 | ✅ 已完成（W2-AC·14 测试·BranchEngine Branch repo_id/name/base_branch/head_commit/protected/status open/merged/deleted + CRUD register/get/get_by_name/list/update/delete + register 校验 MISSING_NAME/MISSING_REPO + merge 检查 source open→target 存在→生成 new_commit→source.status=merged + ALREADY_MERGED/TARGET_NOT_FOUND + merge 策略 merge/rebase/squash + protect 保护分支切换 + 200 条上限 FIFO 淘汰 + NOT_FOUND） |
| 102 | PR 工作流 | 无 | Pull Request/代码审查/CI/CD 检查 | ✅ 已完成（W2-AC·15 测试·PullRequestEngine PullRequest status open/reviewing/approved/rejected/merged/closed 6 态 + ci_status pending/running/passed/failed 4 态 + _VALID_PR_TRANSITIONS 状态机 open→reviewing/closed·reviewing→approved/rejected/open/closed·approved→merged/open·rejected→open/closed·merged/closed 终态 + CRUD + transition 状态转换校验 + add_reviewer 幂等 + set_ci_status 校验 + merge 需 approved+ci_status=passed 双条件 + MERGE_NOT_ALLOWED/CI_NOT_PASSED/INVALID_TRANSITION/INVALID_STATUS/INVALID_CI_STATUS + 200 条上限） |
| 103 | 变换预览 | 无 | 样本数据上运行代码预览 | ✅ 已完成（W2-AC·13 测试·TransformPreviewEngine TransformPreview name/repo_id/branch/transform_code/language python/sql/input_schema/sample_rows + CRUD register/get/list/update/delete + register 校验 MISSING_NAME/MISSING_CODE/INVALID_LANGUAGE + run python exec transform(rows) 函数受限命名空间执行 + sql 简化 passthrough 返回 sample_rows + _infer_schema 从首行推断 boolean/integer/float/string/any + PreviewResult status success/error + 异常捕获 error_message + list_results 按 preview_id 过滤倒序 + 200 条 result 上限 FIFO 淘汰 + NOT_FOUND） |
| 104 | Python 调试器 | 无 | 断点/单步调试/数据框预览 | ✅ 已完成（W2-AD·14 测试·PythonDebuggerEngine DebugSession code/breakpoints/state created/running/paused/completed/error + current_line + variables 变量快照 + output + create_session/get_session/list_sessions 按 state 过滤 + step 单步执行 exec 单行受限命名空间 + 命中末行 completed + is_breakpoint 标记 + run_to_completion 连续执行命中下行断点暂停 + 1000 行死循环上限 + get_variables + delete_session + MISSING_CODE/NOT_FOUND/SESSION_COMPLETED/STEP_ERROR + 200 条 session 上限 FIFO） |
| 105 | 单元测试 | 无 | Python/Java/TypeScript 测试支持 | ✅ 已完成（W2-AD·14 测试·UnitTestEngine TestCase name/language python|java|typescript/code/target_function/timeout_seconds + CRUD register/get/list 按 language 过滤/update/delete + run python exec AssertionError→failed/其他异常→error/正常→passed + java/typescript 简化 simulated passed + TestResult status passed|failed|error|skipped + duration_ms + list_results 按 case_id 过滤倒序 + 200 条 result 上限 FIFO + MISSING_NAME/MISSING_CODE/INVALID_LANGUAGE/NOT_FOUND 校验） |
| 106 | Artifact 存储库 | 无 | Conda/Docker/Maven 制品管理 | ✅ 已完成（W2-AD·14 测试·ArtifactRegistryEngine Artifact name/version/format conda|docker|maven/registry_url/description/tags/dependencies/size_bytes/checksum + CRUD register/get/list 按 format+name+tag 三维过滤/update/delete + get_by_name_version + list_versions 按 name 列所有版本 + list_dependencies 返回直接依赖制品 + register 校验 MISSING_NAME/MISSING_VERSION/INVALID_FORMAT/NAME_VERSION_DUPLICATE 重名同版本 + 200 条上限 FIFO + NOT_FOUND） |
| 107 | AIP Assist | 无 | 代码解释/漏洞查找/翻译/代码自动完成 | ✅ 已完成（W2-AE·16 测试·AIPAssistEngine AIPAssistRequest kind explain|vulnerability|translate|complete/code/language python|java|typescript|sql/context/status pending|running|completed|error/result + CRUD register/get/list 按 kind+status 过滤/update/delete + run 按 kind 分派：explain 返回 summary+lines；vulnerability 扫描 _DANGEROUS_BUILTINS 单词边界匹配返回 vulnerabilities 列表+count；translate python→java 简化关键字映射 def→public void/True→true/False→false/None→null/print→System.out.println 返回 translated+target_language；complete 基于末尾字符规则补全返回 suggestion + ALREADY_COMPLETED 防重复 run + 200 条 result 上限 FIFO + list_results 按 kind 过滤倒序 + MISSING_CODE/INVALID_KIND/INVALID_LANGUAGE/NOT_FOUND 校验） |
| 108 | repoSettings.json | 无 | 标签验证/PR 模板/验证规则配置 | ✅ 已完成（W2-AE·13 测试·RepoSettingsEngine RepoSettings repo_id/label_validation required_prefixes+color_required/pr_template/validation_rules kind branch_protection|required_reviewers|status_check|path_filter/enforce_branch_protection + CRUD register/get/get_by_repo/list 按 repo_id 过滤/update/delete + validate_label 前缀校验 missing required prefix + 颜色校验 label.count(":")>=2 视为含颜色 color required + render_pr_template 占位符 {key} 替换 + register/update 校验 INVALID_RULE_KIND + 200 条上限 FIFO + MISSING_REPO/NOT_FOUND 校验） |
| 109 | 列级血缘 | 无 | 列名追踪/列级影响分析 | ✅ 已完成（W2-AG·14 测试·ColumnImpactEngine 增量补丁，CRUD 部分已由 W2-E #4 交付；新增 ColumnImpactRule source_dataset_rid+source_column+downstream_datasets+downstream_columns+transform_expr + CRUD register/get/list 按 source_dataset_rid 过滤/delete + analyze_impact BFS 下游传播 visited 防环路 ImpactResult impacted_datasets+impacted_columns+depth + 200 条上限 FIFO + MISSING_SOURCE_DATASET/MISSING_SOURCE_COLUMN/NOT_FOUND 校验） |
| 110 | 推荐项目结构 | 无 | Datasource→Transform→Ontology→Workflow 多项目架构 | ✅ 已完成（W2-AE·13 测试·ProjectStructureEngine ProjectStructure name/description/layers datasource|transform|ontology|workflow/components StructureComponent layer+name+type dataset|transform|ontology|workflow|metric+rid_prefix+required + CRUD register/get/list 按 name 过滤/update/delete + render_template 返回 {name,description,layers,components} + validate_project 校验 required 组件必须存在返回 {valid,missing,extra} + register/update 校验 INVALID_LAYER/INVALID_COMPONENT_TYPE + 200 条上限 FIFO + MISSING_NAME/NOT_FOUND 校验） |
| 111 | 逻辑流（Logic Flows） | 无 | Compass Files Lister/连接流编排 | ✅ 已完成（W2-AF·15 测试·LogicFlowEngine LogicFlow name/description/steps list[FlowStep]/status draft/running/completed/error + FlowStep kind compass_files_lister/connector/join/transform 4 种/config/next_step_id + CRUD register/get/list 按 status 过滤/update/delete + execute 按 steps 顺序执行每步 _run_step 分派：compass_files_lister 返回 config.files 列表/connector 返回 connection 模拟/join 合并前步 output list+config.lists/transform 返回 config.transformed + 单步失败整体 error + FlowExecution status running/completed/error + step_results 链 + list_executions 按 flow_id 过滤倒序 + 200 条 execution 上限 FIFO + MISSING_NAME/INVALID_STEP_KIND/NOT_FOUND 校验） |
| 112 | Data Connection Agent Proxy | 无 | 内网反向代理运行时 | ✅ 已完成（W2-AF·14 测试·AgentProxyEngine AgentProxy name/agent_id/proxy_url/auth_token/status online/offline/draining 3 态/connections/last_heartbeat + CRUD register/get/list 按 status+agent_id 过滤/update/delete + heartbeat 推进 last_heartbeat+status=online + drain 置 draining + forward_request 校验 status=online 否则 PROXY_UNAVAILABLE + connections 计数 +1/-1 + 模拟转发返回 {forwarded,response.status_code=200} + 200 条上限 FIFO + MISSING_NAME/MISSING_AGENT/MISSING_URL/NOT_FOUND/PROXY_UNAVAILABLE 校验） |
| 113 | Data Connection Agent Worker | 无 | 客户主机执行运行时 | ✅ 已完成（W2-AF·14 测试·AgentWorkerEngine AgentWorker agent_id/host/version/status registered/online/offline/failed 4 态/capabilities list/last_heartbeat/job_ids + WorkerJob worker_id/capability/payload/status assigned/running/completed/failed/result + CRUD register/get/list 按 status+agent_id 过滤/update/delete + heartbeat 推进 last_heartbeat+status=online + assign_job 校验 status=online WORKER_OFFLINE + capability 在 capabilities 中 CAPABILITY_NOT_SUPPORTED + 创建 job 加入 worker.job_ids + complete_job 推进 status=completed + ALREADY_COMPLETED 防重复 + list_jobs 按 worker_id+status 过滤 + 200 条 job 上限 FIFO + MISSING_AGENT/MISSING_HOST/NOT_FOUND 校验） |
| 114 | Data Connection Agent 管理 | 无 | 注册/下载/心跳/日志/驱动/证书/自动升级 | ✅ 已完成（W2-AG·19 测试·AgentAdminEngine AgentAdmin agent_id+name+version+status registered|active|deprecated+download_url+drivers list[AgentDriver]+certificates list[AgentCertificate]+logs list[AgentLogEntry]+auto_upgrade+last_heartbeat + CRUD register/get/list 按 agent_id+status 过滤/update/delete + heartbeat 推进 last_heartbeat+registered→active + push_log 200 条滚动 + INVALID_LOG_LEVEL 校验 + upgrade 推进 version+status=active + list_drivers/list_certificates + get_download_url 校验 status≠deprecated AGENT_DEPRECATED + INVALID_DRIVER_TYPE/MISSING_AGENT/MISSING_NAME/NOT_FOUND 校验 + 200 条上限 FIFO） |
| 115 | Data Connection 源探索 | 基础 | ER关系图/资源树/样本预览 | ✅ 已完成（W2-AG·16 测试·SourceExplorerEngine SourceSchema source_id+dataset_name+er_diagram list[ERRelation]+resource_tree list[ResourceNode]+sample_preview list[dict] + CRUD register/get/list 按 source_id 过滤/update/delete + explore_er 返回 ER 关系列表 + explore_resource_tree 返回资源树 + preview_sample 前 limit 条 + INVALID_RELATION_TYPE/INVALID_RESOURCE_TYPE/MISSING_SOURCE/MISSING_DATASET_NAME/NOT_FOUND 校验 + 200 条上限 FIFO） |
| 116 | Data Connection 文件筛选 | 无 | 路径正则/修改时间/文件大小/排除已同步 | ✅ 已完成（W2-AH·16 测试·FileFilterEngine FileFilterRule id+name+path_pattern+min_size_bytes+max_size_bytes+modified_after+modified_before+exclude_synced + CRUD register/get/list/update/delete + apply_filter 多条件组合过滤 + 200 条上限 FIFO + MISSING_NAME/NOT_FOUND 校验） |
| 117 | Data Connection 文件变换 | 无 | Gzip/合并/重命名/PGP解密/附加时间戳 | ✅ 已完成（W2-AH·16 测试·FileTransformEngine FileTransform id+name+transform_type gzip|merge|rename|pgp_decrypt|add_timestamp+config + CRUD register/get/list/update/delete + apply_transform 按类型生成输出文件 + 200 条上限 FIFO + MISSING_NAME/INVALID_TRANSFORM_TYPE/NOT_FOUND 校验） |
| 118 | Data Connection Streaming Sync | 无 | Kafka/Kinesis/PubSub → Stream | ✅ 已完成（W2-AH·14 测试·StreamingSyncEngine StreamingSync id+name+source_type kafka|kinesis|pubsub+source_config+target_stream+status stopped|running+offset+last_consumed_at + SyncRecord sync_id+event_key+event_value+offset+timestamp+status synced|failed+error_message + CRUD register/get/list/update/delete + start/stop 切换状态 + consume 处理事件列表 推进 offset 生成记录 + list_records 倒序 limit + 200 条上限 FIFO + MISSING_NAME/INVALID_SOURCE_TYPE/NOT_FOUND/NOT_RUNNING 校验） |
| 119 | Data Connection Push-based Ingestion | 无 | OAuth2 Client Credentials → Stream | ✅ 已完成（W2-AI·18 测试·PushIngestionEngine PushIngestionSource id+name+target_stream+auth_type oauth2_client_credentials|api_key|none+auth_config+rate_limit_per_minute+enabled+total_messages+error_count + CRUD register/get/list 按 name+enabled 过滤/update/delete + receive_message 认证+速率校验+计数推进 + receive_batch 混合 accepted/rejected + list_messages 倒序 limit + validate_token 三种认证模式 + 200 条上限 FIFO + MISSING_NAME/INVALID_AUTH_TYPE/INVALID_RATE_LIMIT/NOT_FOUND/SOURCE_DISABLED/AUTH_FAILED/RATE_LIMIT_EXCEEDED/EMPTY_PAYLOAD 校验） |
| 120 | Data Connection Export 文件 | 无 | Dataset → S3/ABFS/HDFS | ✅ 已完成（W2-AI·17 测试·FileExportEngine FileExportTask id+name+dataset_rid+target_type s3|abfs|hdfs+target_path+file_format csv|parquet|json|avro+compression none|gzip|snappy|lz4+row_limit+filter_expr+status pending|running|completed|failed+total_rows|exported_rows|file_size_bytes+output_files + CRUD register/get/list 按 dataset_rid+status 过滤/update 仅 pending/delete + start pending→running + cancel running→failed + complete 推进 exported_rows+file_size+output_files + fail 标记失败 + get_progress 百分比 + 200 条上限 FIFO + MISSING_NAME/MISSING_DATASET_RID/INVALID_TARGET_TYPE/INVALID_FORMAT/INVALID_COMPRESSION/NOT_FOUND/TASK_NOT_PENDING/TASK_NOT_RUNNING/ALREADY_COMPLETED 校验） |
| 121 | Data Connection Export 表 | 无 | Incremental mirror + Truncate on SNAPSHOT | ✅ 已完成（W2-AI·21 测试·TableExportEngine TableExportTask id+name+source_dataset_rid+target_table+export_mode full|incremental|snapshot+primary_keys+watermark_column+last_watermark+truncate_on_snapshot+status pending|running|completed|failed+processed/inserted/updated/deleted_rows + TableExportRun run_id+task_id+mode+status running|completed|failed+rows_*+watermark_before/after+truncated + CRUD register/get/list 按 dataset_rid+status+mode 过滤/update/delete + start_run running 态+truncate 标记 + complete_run 推进 watermark+累计统计 + fail_run 标记失败 + list_runs 倒序 limit + get_latest_run + incremental 需 watermark 校验 + 200 条上限 FIFO + MISSING_NAME/MISSING_DATASET/INVALID_MODE/INCREMENTAL_REQUIRES_WATERMARK/NOT_FOUND/RUN_NOT_FOUND/RUN_NOT_RUNNING/ALREADY_COMPLETED 校验） |
| 122 | Data Connection Export 流 | 无 | Stream → Kafka 等 | ✅ 已完成（W2-AJ·19 测试·StreamExportEngine StreamExportTask id+name+source_stream+target_type kafka|kinesis|pubsub+target_topic+partition_strategy round_robin|key_based|random+key_field+batch_size+status stopped|running|disabled+total_events+last_event_at + StreamExportEvent event_id+key+payload+partition+offset+status pending|sent|failed+sent_at + CRUD register/get/list 按 source_stream+status 过滤/update/delete + start/stop 状态切换 + publish_event 分区计算+计数推进 + publish_batch 批量 + list_events 倒序 limit + 200 条上限 FIFO + MISSING_NAME/MISSING_SOURCE_STREAM/INVALID_TARGET_TYPE/INVALID_PARTITION_STRATEGY/INVALID_BATCH_SIZE/NOT_FOUND/TASK_NOT_STOPPED/TASK_NOT_RUNNING/TASK_DISABLED 校验） |
| 123 | Data Connection Webhooks 多步调用 | 无 | Call 1 → Call 2，参数引用 | ✅ 已完成（W2-AJ·22 测试·WebhookPipelineEngine WebhookPipeline id+name+description+steps[]+status draft|active|disabled+created_at+updated_at + WebhookPipelineStep step_id+name+url+method GET|POST|PUT|DELETE|PATCH+headers+request_template+auth_type none|api_key|bearer|basic+auth_config+timeout_ms+retry_count+output_mapping+condition_expr + PipelineRun run_id+pipeline_id+status running|completed|failed+started_at+finished_at+current_step+step_results[]+outputs + CRUD register/get/list 按 name+status 过滤/update/delete + add_step/remove_step/reorder_steps 步骤管理 + run 多步执行编排 + list_runs/get_run 执行记录 + 200 条上限 FIFO + MISSING_NAME/EMPTY_STEPS/DUPLICATE_STEP_ID/INVALID_METHOD/INVALID_AUTH_TYPE/INVALID_TIMEOUT/NOT_FOUND/STEP_NOT_FOUND/RUN_NOT_FOUND/PIPELINE_DISABLED/INVALID_ORDER 校验） |
| 124 | Data Connection Webhooks 输出参数 | 无 | 从响应提取字段+类型转换 | ✅ 已完成（W2-AJ·17 测试·WebhookOutputEngine WebhookOutputConfig id+name+webhook_id+output_fields[]+response_code_field+success_codes[]+error_message_field+created_at+updated_at + OutputFieldMapping field_id+source_path+target_name+target_type string|integer|number|boolean+required+default_value + OutputExtractionResult success+fields{}+missing_required[]+error_message + CRUD register/get/list 按 webhook_id+name 过滤/update/delete + add_field/remove_field 字段管理 + extract 路径提取+类型转换 + validate_response 返回码校验 + 200 条上限 FIFO + MISSING_NAME/MISSING_WEBHOOK/DUPLICATE_FIELD_ID/INVALID_TARGET_TYPE/INVALID_SOURCE_PATH/NOT_FOUND/FIELD_NOT_FOUND 校验） |
| 125 | Data Connection Webhooks 执行策略 | 无 | 并发/速率/超时/重试 | ✅ 已完成（W2-AK·24 测试·WebhookExecutionPolicyEngine WebhookExecutionPolicy policy_id+name+webhook_id+max_concurrent+rate_limit_per_minute+timeout_ms+max_retries+retry_backoff_ms+retry_on_status[]+circuit_breaker_enabled+circuit_failure_threshold+circuit_cooldown_ms+status+created_at+updated_at + ExecutionState current_concurrent+window_start+window_count+circuit_state closed|open|half_open+failure/total_count+opened_at + ExecutionAttempt attempt_id+call_id+attempt_number+status pending|success|failed|rate_limited|concurrency_limited|circuit_open+http_status+duration_ms+started/finished_at+error_message+next_attempt_at + CRUD register/get/list 按 webhook_id+status 过滤/update/delete + acquire_slot 并发+速率+熔断三重检查 + release_slot 释放+推进熔断 + record_retry 记录重试+指数退避 + get_execution_state/reset_state + list_attempts 倒序 + trip_circuit/reset_circuit 熔断演练 + 200 条上限 FIFO + MISSING_NAME/MISSING_WEBHOOK/INVALID_CONCURRENCY/INVALID_RATE_LIMIT/INVALID_TIMEOUT/INVALID_RETRY_COUNT/INVALID_THRESHOLD/NOT_FOUND/CONCURRENCY_EXCEEDED/RATE_LIMIT_EXCEEDED/CIRCUIT_OPEN 校验） |
| 126 | Data Connection Egress policies | 无 | CIDR/Port/域名白名单 | ✅ 已完成（W2-AK·21 测试·EgressPolicyEngine EgressPolicy policy_id+name+description+effect allow|deny+cidr_blocks[]+ports[]+domains[]+protocols[]+priority+status+created_at+updated_at + EgressEvaluation eval_id+policy_id+destination+port+protocol+decision allowed|denied+matched_rules[]+reason+evaluated_at + CRUD register/get/list 按 effect+status 过滤/update/delete + evaluate 按 priority 匹配 AND 多条件 + evaluate_batch 批量 + check_allowed 简化 + list_evaluations + add_cidr/remove_cidr + add_domain/remove_domain + CIDR 支持 IPv4 + 域名支持 *. 通配 + 默认 deny 安全策略 + 200 条上限 FIFO + MISSING_NAME/INVALID_EFFECT/EMPTY_RULES/INVALID_CIDR/INVALID_PORT/INVALID_PROTOCOL/INVALID_PRIORITY/NOT_FOUND 校验） |
| 127 | Data Connection Exportable markings | 无 | 可导出权限标记控制 | ✅ 已完成（W2-AK·20 测试·ExportableMarkingEngine ExportableMarkingPolicy policy_id+name+connection_id+marking_level public|internal|restricted|confidential+export_action allow|deny|mask|redact+mask_character+redact_text+affected_columns[]+affected_markings[]+priority+status+created_at+updated_at + MarkingEvaluation eval_id+policy_id+connection_id+column_name+markings[]+decision allowed|denied|masked|redacted+masked_value+reason+evaluated_at + CRUD register/get/list 按 connection_id+status+marking_level 过滤/update/delete + evaluate 按 priority 匹配 + evaluate_row 多列批量 + can_export 简化 + list_evaluations + add/remove_affected_column + add/remove_affected_marking + 无匹配默认 allow + 200 条上限 FIFO + MISSING_NAME/MISSING_CONNECTION/INVALID_MARKING_LEVEL/INVALID_EXPORT_ACTION/INVALID_PRIORITY/NOT_FOUND 校验） |
| 128 | Data Connection OIDC/Cloud Identity | 无 | OpenID Connect/云身份/出站应用 | ✅ 已完成（W2-AW·18 测试·CloudIdentityEngine CloudIdentity identity_id+name+cloud_provider aws|azure|gcp+connection_type openid_connect|oauth2|saml+client_id+client_secret+tenant_id+redirect_uri+scopes[]+status active|inactive+created_at+updated_at + OutboundApp app_id+name+identity_id+target_url+auth_method header|query_param|body+status+created_at + CRUD register_identity/get_identity/list_identities 按 cloud_provider+status 过滤/update_identity/delete_identity + register_app/get_app/list_apps 按 identity_id 过滤/update_app/delete_app + validate_identity 校验 client_id+tenant_id+ 200 条上限 FIFO + MISSING_NAME/INVALID_PROVIDER/INVALID_CONNECTION_TYPE/MISSING_IDENTITY/NOT_FOUND 校验） |
| 129 | Data Connection 虚拟表 | 无 | 外部数据仓库注册为虚拟表 | ✅ 已完成（W2-AW·20 测试·VirtualTableEngine VirtualTable table_id+name+source_connection_id+source_schema+source_table+column_mappings[]+sync_mode snapshot|incremental+refresh_schedule+last_sync_at+status active|inactive+created_at+updated_at + ColumnMapping column_name+source_type+target_type+is_primary_key+nullable + CRUD register_table/get_table/list_tables 按 source_connection_id+sync_mode+status 过滤/update_table/delete_table + sync_table 推进 last_sync_at + validate_mappings 主键校验+类型映射校验 + 200 条上限 FIFO + MISSING_NAME/MISSING_CONNECTION/EMPTY_MAPPINGS/INVALID_SYNC_MODE/INVALID_STATUS/NOT_FOUND 校验） |
| 130 | Data Lineage 可视化 | 无 | 血缘图/展开/着色/保存分享 | ✅ 已完成（W2-AL·18 测试·LineageVisualizationEngine LineageView view_id+name+description+root_dataset_rid+graph_mode graph|tree+direction upstream|downstream|both+depth+layout horizontal|vertical|radial+color_by type|health|status|owner+collapsed_nodes[]+highlighted_nodes[]+saved_by+is_public+created_at+updated_at + LineageGraphNode node_id+label+node_type+health_status+color+x+y + LineageGraphEdge edge_id+source+target+label+edge_type + LineageGraph view_id+nodes[]+edges[]+stats{} + CRUD register/get/list saved_by+graph_mode 过滤/update/delete + generate_graph 模拟深度生成节点边 + expand_node/collapse_node 节点折叠 + color_by 按规则着色 + share_view 切换公开私有 + list_views_by_dataset 按数据集列视图 + 200 条上限 FIFO + MISSING_NAME/MISSING_DATASET/INVALID_GRAPH_MODE/INVALID_DIRECTION/INVALID_LAYOUT/INVALID_DEPTH/INVALID_COLOR_BY/NOT_FOUND 校验） |
| 131 | Data Lineage 列级血缘 | 部分 | 列名搜索/列级追踪 | ✅ 已完成（W2-AL·18 测试·ColumnLineageSearchEngine 增量：CRUD 已由 W2-E #4 交付；新增 ColumnIndexEntry dataset_rid+column_name+data_type+description+tags[]+last_updated + ColumnTraceStep dataset_rid+column_name+transform_expr+direction + ColumnTraceResult column+dataset_rid+direction+depth+path[] + register_column/get_column/list_columns/update_column/delete_column CRUD + search_columns 关键词模糊+类型+标签过滤 + trace_column 上下游追踪 + build_index 重建索引 + 200 条上限 FIFO + MISSING_DATASET/MISSING_COLUMN/INVALID_DIRECTION/INVALID_DEPTH/NOT_FOUND 校验） |
| 132 | Data Lineage 搭建时间线 | 无 | 甘特图/调度管理 | ✅ 已完成（W2-AL·21 测试·LineageBuildTimelineEngine BuildSchedule schedule_id+name+pipeline_id+cron_expression+timezone+status active|paused|disabled+last_run_at+next_run_at+created_at+updated_at + BuildRun run_id+schedule_id+status pending|running|success|failed|cancelled+started_at+finished_at+datasets_built[]+duration_ms+error_message + GanttTask task_id+name+pipeline_id+start_time+end_time+status+dependencies[] + GanttChart chart_id+title+start_date+end_date+tasks[] + CRUD register/get/list pipeline_id+status 过滤/update/delete_schedule + compute_next_run 5 段 cron 解析 + trigger_run 检查 active + complete_run + get_run/list_runs + pause_schedule/resume_schedule + get_gantt_chart 按日期范围生成 + 200 条上限 FIFO + MISSING_NAME/MISSING_PIPELINE/INVALID_CRON/INVALID_TIMEZONE/INVALID_STATUS/NOT_FOUND/SCHEDULE_PAUSED/RUN_NOT_FOUND/RUN_NOT_RUNNING 校验） |
| 133 | Data Health 检查类型 | 无 | 状态/时间/大小/内容/模式检查 | ✅ 已完成（W2-AB·15 测试·HealthCheckTypeEngine HealthCheckType check_kind freshness/freshness_duration/volume/schema/content 5 种检查 + configuration threshold/expected_columns/rules + severity error/warning/info + CRUD register/get/list/update/delete + run 按 check_kind 评估 freshness 时间戳延迟/freshness_duration 小时延迟/volume 行数阈值/schema 列名匹配/content 规则树 eq/ne/gt/lt/ge/le/in/contains + disabled→skipped + 200 条 result 上限 + INVALID_CHECK_KIND/MISSING_NAME/INVALID_SEVERITY/MISSING_DATASET 校验） |
| 134 | Data Health 检查计划 | 无 | 自动计划（数据集更新触发）+ 手动计划（定时执行） | ✅ 已完成（W2-AB·14 测试·HealthScheduleEngine HealthSchedule mode auto/manual 双模式 + auto trigger_dataset_rid 事件驱动 + manual cron_expression 定时 + trigger 推进 last_run_at/run_count + manual 模式重算 next_run_at + compute_next_run auto 返回 0 事件驱动 + enable/disable + 200 条上限 + INVALID_MODE/MISSING_TRIGGER_DATASET/MISSING_CRON/MISSING_CHECK 校验） |
| 135 | Data Health 检查组 | 无 | 检查分组/通知/监控 | ✅ 已完成（W2-AB·13 测试·HealthCheckGroupEngine HealthCheckGroup check_ids + notification_config channels/severity_filter + CRUD register/get/list/update/delete + attach_check/detach_check 幂等 + monitor 返回 GroupMonitorSummary total/enabled/last_results/pass_rate + 容忍缺失检查 missing + send_notification severity 过滤 + 200 条通知上限 + NAME_DUPLICATE 重名校验） |
| 136 | Data Health 检查组诊断 | 无 | 失败聚焦/检查列表/分组策略 | ✅ 已完成（W2-AM·16 测试·HealthDiagnosticsEngine HealthDiagnosticsReport report_id+group_id+generated_at+total_checks+passed/failed/warning_count+failed_checks[]+focus_summary+grouping_strategy by_severity|by_type|by_dataset + FailedCheckDetail check_id+check_name+check_kind+severity+dataset_rid+failure_message+last_run_at + generate_diagnostics 生成报告+模拟失败检查 + get_report/list_reports 按 group_id 过滤 + get_failed_checks severity 过滤 + get_focus_summary 失败聚焦摘要 + list_checks_by_group 检查列表 + 200 条上限 FIFO + MISSING_GROUP/INVALID_GROUPING/INVALID_SEVERITY/NOT_FOUND 校验） |
| 137 | Data Health 监测选项 | 无 | 无通知/所有失败/仅严重 | ✅ 已完成（W2-AM·19 测试·HealthMonitoringOptionsEngine HealthMonitoringOptions options_id+dataset_rid+notification_mode none|all_failures|only_severe+channels[] email|slack|inapp+reminder_interval_minutes+auto_resolve+created_at+updated_at + CRUD register/get/get_by_dataset/list 按 dataset_rid 过滤/update/delete + set_notification_mode 模式切换 + add_channel/remove_channel 渠道管理 + 200 条上限 FIFO + MISSING_DATASET/INVALID_NOTIFICATION_MODE/INVALID_CHANNEL/INVALID_INTERVAL/NOT_FOUND/CHANNEL_NOT_FOUND 校验） |
| 138 | Data Health 平台内通知 | 无 | Foundry通知系统集成 | ✅ 已完成（W2-AM·18 测试·HealthNotificationEngine HealthNotification notification_id+dataset_rid+check_id+check_name+severity critical|warning|info+title+message+status unread|read|cleared+created_at+read_at+cleared_at+user_id + create/get/list 按 user_id+status+severity 过滤 + mark_read/mark_all_read + clear/clear_all + get_unread_count 按 severity 分组统计 + list_by_dataset + 200 条上限 FIFO + MISSING_USER/MISSING_DATASET/INVALID_SEVERITY/INVALID_STATUS/NOT_FOUND 校验） |
| 139 | Data Health Issues集成 | 无 | 检查失败自动创建/解决问题自动关闭 | ✅ 已完成（W2-AN·18 测试·HealthIssuesIntegrationEngine HealthIssue issue_id+dataset_rid+check_id+check_name+severity critical|warning|info+title+description+status open|in_progress|resolved|closed+created_at+updated_at+resolved_at+created_by_check+linked_check_runs[] + create_issue/get_issue/list_issues 按 dataset_rid+status+severity 过滤 + update_issue 字段更新 + resolve_issue/close_issue 状态推进 + auto_create_from_check 检查失败自动创建（[SEVERITY] check_name failed on dataset_rid 标题模板） + auto_resolve_from_check 检查通过自动解决返回 None 表示无候选 + link_check_run 关联检查运行记录幂等去重 + 200 条上限 FIFO + MISSING_DATASET/MISSING_CHECK/INVALID_SEVERITY/INVALID_STATUS/NOT_FOUND 校验） |
| 140 | Data Health 数据集健康Tab | 无 | 数据集预览中的健康Tab | ✅ 已完成（W2-AN·16 测试·DatasetHealthTabEngine DatasetHealthTab tab_id+dataset_rid+overall_status healthy|warning|critical|unknown+checks_summary{}+last_check_at+recommendations[]+trends[]+created_at+updated_at + register 幂等（同 dataset 返回同 tab） + get/get_by_dataset/list 按 dataset_rid 过滤 + update_status 状态+检查摘要+last_check_at 推进 + add_recommendation 幂等去重 + add_trend 趋势点追加 + get_overall_health 整体状态摘要 + delete 级联清理 _dataset_index + 200 条上限 FIFO + MISSING_DATASET/INVALID_STATUS/NOT_FOUND 校验） |
| 141 | Data Health 沿袭健康着色 | 无 | 数据沿袭中按健康状态着色 | ✅ 已完成（W2-AN·18 测试·LineageHealthColoringEngine LineageHealthColor color_id+dataset_rid+health_status healthy|warning|critical|unknown+color_code green|yellow|red|gray+display_name+tooltip+updated_at + LineageColoringConfig config_id+name+color_scheme traffic_light|custom+status_color_mapping{}+default_color+created_at+updated_at + register_color/get_color/list_colors status_filter 过滤 + update_color/delete_color + register_config 默认填充 traffic_light mapping + get_config/list_configs + apply_coloring 按 config.status_color_mapping 批量着色（unknown→default_color 回退） + 200 条上限 FIFO + MISSING_DATASET/MISSING_NAME/INVALID_HEALTH_STATUS/INVALID_COLOR_CODE/INVALID_COLOR_SCHEME/NOT_FOUND/CONFIG_NOT_FOUND 校验） |
| 142 | Data Health 应用入口 | 无 | 侧边栏数据健康应用 | ✅ 已完成（W2-AV·18 测试·HealthAppEngine HealthAppEntry entry_id+app_name+icon+path+category data_health|monitoring|governance+permissions[]+status active|inactive+order_index+created_at+updated_at + register_entry/get_entry/list_entries 按 category+status 过滤/update_entry/delete_entry 返回 bool/reorder_entries/get_sidebar_items 按 order_index 排序返回 active 条目 + 200 条上限 FIFO + MISSING_APP_NAME/MISSING_PATH/INVALID_CATEGORY/INVALID_STATUS/NOT_FOUND 校验） |
| 143 | Functions 测试调试 | 无 | 单元测试/调试器/性能分析 | ✅ 已完成（W2-AO·27 测试·FunctionsTestDebugEngine FunctionTestCase case_id+function_id+test_name+language python|typescript+test_code+assertions[]+status pending|passed|failed|error+output+duration_ms + FunctionDebugSession session_id+function_id+inputs+breakpoints+state created|running|paused|completed|error+current_line+variables+output + ProfileResult profile_id+function_id+duration_ms+memory_bytes+cpu_percent+call_count+hotspots[] + register_test/get_test/list_tests 按 function_id+status 过滤 + run_test python 含 assert 且不含 fail→passed/含 fail→failed/typescript 简化 passed + register_debug/get_debug_session/start_debug（created→running ALREADY_STARTED）+ step（current_line+1/断点→paused/≥10→completed/非 running|paused→INVALID_STATE） + profile 模拟性能指标 + list_profiles 按 function_id 过滤 + 200 条上限 FIFO + MISSING_FUNCTION/MISSING_NAME/INVALID_LANGUAGE/NOT_FOUND 校验） |
| 144 | Functions 外部API调用 | 无 | TypeScript/Python调用外部系统 | ✅ 已完成（W2-AO·22 测试·ExternalApiCallEngine ExternalApiCall call_id+name+language typescript|python+endpoint_url+method GET|POST|PUT|PATCH|DELETE+headers+auth_type none|bearer|basic|api_key+auth_config+payload_template+response_mapping+status active|inactive + CallResult result_id+call_id+status success|failed+status_code+response_body+duration_ms+error_message+executed_at + register/get/list 按 language+status 过滤/update/delete + execute 模拟 status_code=200/response_body={"ok":true,"echo":<payload>}/duration_ms>0 + list_results 按 call_id 过滤 + enable/disable 状态切换 + 200 条上限 FIFO + MISSING_NAME/MISSING_URL/INVALID_LANGUAGE/INVALID_METHOD/INVALID_AUTH_TYPE/NOT_FOUND 校验） |
| 145 | Interfaces 定义/继承 | 无 | 接口定义/扩展/实现/多态 | ✅ 已完成（W2-K #32 清账·InterfaceEngine 已在 W2-K v2.4 完全交付：OntologyInterface CRUD + extends 继承（父接口存在校验 PARENT_NOT_FOUND） + implement OT 声明实现接口 + get_implementors + get_effective_properties 多态（含继承的父接口属性递归） + delete 删除保护 STILL_EXTENDED/STILL_IMPLEMENTED + InterfaceError NOT_FOUND 校验 · 本批次确认 #145 与 #32 为同一能力，标记清账完成） |
| 146 | Dataset Preview 详情Tabs | 部分 | 历史/健康/比较/流视图 | ✅ 已完成（W2-AO·24 测试·DatasetPreviewTabsEngine DatasetPreviewTabs tabs_id+dataset_rid+history_tab+health_tab+comparison_tab+stream_view_tab + HistoryTab enabled+last_n_versions+snapshot_diff + HealthTab enabled+overall_status healthy|warning|critical|unknown+checks_summary+recommendations[] + ComparisonTab enabled+baseline_dataset_rid+compare_mode schema|content|stats + StreamViewTab enabled+stream_type kafka|kinesis|pubsub+partition+offset+status running|stopped + register 幂等（同 dataset 返回同 tabs） + get/get_by_dataset/list 按 dataset_rid 过滤 + enable_tab/disable_tab（tab_name history|health|comparison|stream_view） + update_history_tab/update_health_tab/update_comparison_tab/update_stream_view_tab 四 Tab 子模型更新 + 200 条上限 FIFO（淘汰时清理 _dataset_index） + MISSING_DATASET/INVALID_TAB_NAME/INVALID_HEALTH_STATUS/INVALID_COMPARE_MODE/INVALID_STREAM_TYPE/INVALID_STREAM_STATUS/NOT_FOUND 校验） |
| 147 | Workshop 变量联动 | 弱 | 全局变量 | ✅ 已完成（W2-AQ·25 测试·WorkshopVariableEngine WorkshopVariable var_id+name+var_type object_set/object_set_filter/string/numeric/boolean/date/timestamp/array/struct/geopoint/geoshape/time_series_set 11 种+definition_type static/function/object_set_aggregation/object_property/object_set_definition/variable_transformation 6 种+recompute_strategy automatic/triggered/on_load+lazy+module_id+status + VariableEvent event_id+var_id+event_type+payload + register 校验 MISSING_NAME/INVALID_VAR_TYPE/INVALID_DEFINITION_TYPE/INVALID_RECOMPUTE_STRATEGY/DEPENDENCY_NOT_FOUND + get/list 按 var_type+definition_type+module_id 过滤 + update/delete（级联清理 depends_on 引用）+ evaluate static 返回 value/function 模拟 func_result_{var_id}/variable_transformation BFS 递归解析依赖（visited 防环 CIRCULAR_DEPENDENCY） + resolve_dependencies BFS 上游 + get_lineage upstream/downstream + record_event/list_events + 200 条上限 FIFO + MISSING_NAME/INVALID_VAR_TYPE/INVALID_DEFINITION_TYPE/INVALID_RECOMPUTE_STRATEGY/DEPENDENCY_NOT_FOUND/CIRCULAR_DEPENDENCY/NOT_FOUND 校验） |
| 148 | Compute Module 调度引擎 | 无 | 无服务器 Docker 容器生命周期管理 | ✅ 已完成（W2-AP·24 测试·ComputeSchedulerEngine ComputeModule module_id+name+image+command+args+env+status pending|scheduling|running|stopping|stopped|failed+container_id+started_at+last_heartbeat_at+error_message + register/get/list status 过滤/start（pending|stopped|failed→running 生成 container_id=ctr-*）/stop（running→stopped）/restart（running→running 新 container_id）/heartbeat（running→last_heartbeat_at 推进 否则 NOT_RUNNING）/fail（→failed+error_message）/remove + 200 条上限 FIFO + MISSING_NAME/MISSING_IMAGE/INVALID_TRANSITION/NOT_RUNNING/NOT_FOUND 校验） |
| 149 | Compute Module 副本扩缩 | 无 | min/max replicas + 每副本并发 | ✅ 已完成（W2-AP·30 测试·ComputeScalerEngine ScalePolicy policy_id+module_id+min_replicas+max_replicas+target_concurrency+scale_up_threshold+scale_down_threshold+status active|inactive + Replica replica_id+module_id+status pending|running|unhealthy + register_policy（校验 min>=0/max>=min/target>0/threshold up in(0,1]/down in[0,1)/up>down）/get_policy/list_policies module_id+status 过滤/update_policy/delete_policy/evaluate_scale（ratio=current/target，>=up→scale_up/<=down→scale_down/否则 none，POLICY_INACTIVE 校验）/scale_up（生成 count 个 pending Replica）/scale_down（标记 count 个 pending|running→unhealthy）/list_replicas module_id+status 过滤/mark_replica_unhealthy + 200 条上限 FIFO + MISSING_MODULE/INVALID_MIN_REPLICAS/INVALID_MAX_REPLICAS/INVALID_TARGET_CONCURRENCY/INVALID_THRESHOLD/INVALID_COUNT/INVALID_STATUS/POLICY_INACTIVE/NOT_FOUND 校验） |
| 150 | Compute Module 资源约束 | 无 | CPU Request/Limit + GPU + Memory | ✅ 已完成（W2-AP·28 测试·ComputeResourceEngine ResourceQuota quota_id+module_id+cpu_request+cpu_limit+memory_request_mb+memory_limit_mb+gpu_count+gpu_type（T4|A100|V100|H100|空）+ephemeral_storage_gb + register（同 module_id 覆盖更新 _module_index）/get/get_by_module/list module_id 过滤/update/delete（清理 _module_index）/validate_quota（返回 valid+quota dict）/compare_quota（requested_cpu<=cpu_limit 且 requested_memory_mb<=memory_limit_mb → fits）/list_by_gpu + 200 条上限 FIFO + MISSING_MODULE/INVALID_CPU_REQUEST/INVALID_CPU_LIMIT/INVALID_MEMORY_REQUEST/INVALID_MEMORY_LIMIT/INVALID_GPU_COUNT/INVALID_GPU_TYPE/INVALID_STORAGE/NOT_FOUND 校验） |
| 151 | Compute Module API（job 长轮询） | 无 | `/interactive-module/api/internal-query/job` + 结果回传 | ✅ 已完成（W2-AQ·21 测试·ComputeJobPollingEngine ComputeJob job_id+module_id+function_name+payload+status queued|running|succeeded|failed|timeout+result+error+polling_token+poll_count+created_at+started_at+finished_at+last_polled_at+timeout_seconds + submit 校验 MISSING_MODULE/MISSING_FUNCTION 生成 job_id=job-*+polling_token=pt-* + get/list 按 module_id+status 过滤 + poll（校验 INVALID_TOKEN，queued→running 推进 started_at，running→succeeded 推进 finished_at+result，poll_count+1，last_polled_at 推进，terminal 不变）+ get_result（succeeded 返回 result 否则 JOB_NOT_COMPLETED）+ cancel（queued|running→failed error=cancelled 否则 ALREADY_TERMINAL）+ check_timeouts（running 超过 timeout_seconds→timeout） + 200 条上限 FIFO + MISSING_MODULE/MISSING_FUNCTION/INVALID_TOKEN/JOB_NOT_COMPLETED/ALREADY_TERMINAL/NOT_FOUND 校验） |
| 152 | `app.py` 入口约定 | 无 | 函数名即端点 + 相对导入 + JSON 序列化 | ✅ 已完成（W2-AQ·18 测试·AppEntryConventionEngine AppEntry entry_id+module_id+function_name+endpoint_path+relative_imports[]+json_serializable+signature_params[]+return_type+status valid|invalid+validation_errors[] + register 校验 MISSING_MODULE/MISSING_FUNCTION 生成 entry_id=entry-* + 派生 endpoint_path（snake_case 下划线→斜杠 如 get_user_data→/get/user/data）+ _validate（relative_imports 每项须以 . 开头 否则 non-relative import 错误；return_type 须在 dict|list|str|int|float|bool|None|空 中 否则 non-json-serializable 错误 json_serializable=False）+ get/list 按 module_id+status 过滤 + validate 重新校验 + list_invalid + update/delete + get_endpoint + 200 条上限 FIFO + MISSING_MODULE/MISSING_FUNCTION/NOT_FOUND 校验） |
| 153 | `meta.yaml` 依赖 + `gradle.properties` | 无 | 镜像构建配置 / baseImageTag ≥ 0.15.0 校验 | ✅ 已完成（W2-AU·18 测试·BuildConfigEngine BuildConfig config_id+module_id+base_image_tag+dependencies[]+gradle_properties dict+status active|inactive+created_at+updated_at + register_config/get_config/get_by_module/list_configs 按 module_id+status 过滤/update_config/delete_config + validate_base_image_tag semver 数值比较（≥0.15.0） + 200 条上限 FIFO + MISSING_MODULE/MISSING_BASE_IMAGE_TAG/INVALID_BASE_IMAGE_TAG/NOT_FOUND 校验） |
| 154 | Docker 镜像发布（Artifact Repo） | 无 | New → Artifacts → Docker → 不支持 `latest` 标签 | ✅ 已完成（W2-AU·19 测试·DockerPublishEngine DockerImage image_id+module_id+tag+repository_url+status pending|building|published|failed+size_bytes+published_at+error_message+created_at+updated_at + register_image/get_image/list_images 按 module_id+status 过滤/update_image/delete_image + build_image pending→building/publish_image building→published（校验 tag≠latest 否则 INVALID_TAG）/fail_image building→failed + 200 条上限 FIFO + MISSING_MODULE/MISSING_TAG/INVALID_TAG/INVALID_STATUS/NOT_FOUND 校验） |
| 155 | Configure / Query / Overview 三标签页 | 无 | 容器配置/函数查询/状态总览 | ✅ 已完成（W2-AT·19 测试·ContainerConfigEngine ContainerTabConfig tab_config_id+module_id+tab_name configure|query|overview+config_data dict+status active|inactive+created_at+updated_at + register_config/get_config/list_configs 按 module_id+tab_name+status 过滤/update_config/delete_config + get_module_overview 聚合返回模块的三标签配置汇总 + 200 条上限 FIFO + MISSING_MODULE/MISSING_TAB_NAME/INVALID_TAB_NAME/INVALID_STATUS/NOT_FOUND 校验） |
| 156 | 缩容至零 + 冷启动告警 | 无 | Query 标签首次查询等待 | ✅ 已完成（W2-AT·20 测试·ScaleToZeroEngine ScaleToZeroPolicy policy_id+module_id+idle_timeout_seconds+min_replicas+scale_up_delay_seconds+status active|inactive+created_at + ColdStartAlert alert_id+module_id+alert_type cold_start|scale_up+wait_duration_ms+severity info|warning+cleared+created_at + register_policy/get_policy/list_policies 按 module_id+status 过滤/update_policy/delete_policy + trigger_alert/list_alerts 按 module_id+alert_type+cleared 过滤/clear_alert + simulate_cold_start 返回模拟延迟 ms + 200 条上限 FIFO + MISSING_MODULE/INVALID_IDLE_TIMEOUT/INVALID_MIN_REPLICAS/INVALID_SCALE_UP_DELAY/INVALID_STATUS/INVALID_ALERT_TYPE/NOT_FOUND 校验） |
| 157 | 本地开发脚手架 | 无 | Dockerfile + requirements + app.py 模板 | ✅ 已完成（W2-AT·18 测试·DevScaffoldEngine ScaffoldTemplate template_id+language python|typescript+name+description+file_templates[]（ScaffoldFile filename+content）+created_at+updated_at + GeneratedScaffold scaffold_id+module_id+template_id+rendered_files[]+status generated|applied+created_at + register_template/get_template/list_templates 按 language 过滤/update_template/delete_template + generate_scaffold 填充 {{var}} 占位符/get_scaffold/list_scaffolds 按 module_id+status 过滤/apply_scaffold generated→applied + 内置 3 默认模板 python_compute_module/typescript_compute_module/python_ml_module + 200 条上限 FIFO + MISSING_NAME/MISSING_MODULE/INVALID_LANGUAGE/TEMPLATE_NOT_FOUND/SCAFFOLD_NOT_FOUND/NOT_FOUND 校验） |
| 158 | External access | 无 | Foundry data / services / 外部域名访问配置 | ✅ 已完成（W2-AU·17 测试·ExternalAccessEngine ExternalAccessConfig config_id+module_id+access_type foundry_data|foundry_service|external_domain+domain+port+path_prefix+auth_type none|bearer|api_key+auth_config dict+status active|inactive+created_at+updated_at + register_config/get_config/list_configs 按 module_id+access_type+status 过滤/update_config/delete_config + test_connectivity 返回 ok+latency_ms 模拟 + 200 条上限 FIFO + MISSING_MODULE/MISSING_DOMAIN/INVALID_ACCESS_TYPE/INVALID_PORT/INVALID_STATUS/NOT_FOUND 校验） |
| 159 | 与 Functions / Workshop / Slate 集成 | 无 | Functions 后端类型 + 前端触发入口 | ✅ 已完成（W2-AV·20 测试·FunctionIntegrationEngine FunctionIntegration integration_id+module_id+function_id+backend_type python|typescript|container+trigger_type workshop|slate|direct+trigger_config dict+endpoint_url+status active|inactive+created_at+updated_at + register_integration/get_integration/list_integrations 按 module_id+backend_type+trigger_type+status 过滤/update_integration/delete_integration 返回 bool/invoke 模拟调用返回结果 dict/list_by_function + 200 条上限 FIFO + MISSING_MODULE/MISSING_FUNCTION/MISSING_BACKEND_TYPE/INVALID_BACKEND_TYPE/INVALID_TRIGGER_TYPE/INVALID_STATUS/NOT_FOUND 校验） |
| 160 | Ferry 增量包 | 全量 | 增量 | ✅ 已完成（W2-AV·18 测试·FerryPackageEngine FerryPackage package_id+source_dataset_rid+target_dataset_rid+package_type incremental|full+change_count+status pending|packaging|ready|failed+size_bytes+checksum+created_at+completed_at + create_package/get_package/list_packages 按 source_dataset_rid+target_dataset_rid+package_type+status 过滤/update_package/delete_package 返回 bool/build_package pending→packaging→ready/fail_package packaging→failed/apply_package ready→返回应用结果 + 200 条上限 FIFO + MISSING_SOURCE/MISSING_TARGET/INVALID_PACKAGE_TYPE/INVALID_STATUS/NOT_FOUND 校验） |
| 161 | Data Integration 统一框架 | 分散 | 连接+变换+管理三位一体 | ✅ 已完成（W2-AR·16 测试·DataIntegrationFrameworkEngine IntegrationFramework framework_id+name+description+connection_id+transform_id+management_config+status + register 校验 MISSING_NAME + get/list 按 status 过滤 + update/delete + link_connection/link_transform + get_summary 返回 has_connection/has_transform/has_management/completeness empty|partial|full + 200 条上限 FIFO + MISSING_NAME/NOT_FOUND 校验） |
| 162 | 管道维护与监控 | 无 | 监控视图/数据期望/稳定性建议 | ✅ 已完成（W2-AR·26 测试·PipelineMaintenanceEngine PipelineHealthCheck check_id+pipeline_id+check_type+status pass|fail|warning+severity info|warning|critical+message+last_run_at + DataExpectation expectation_id+pipeline_id+delivery_cycle+build_frequency+data_expiry_threshold_hours + StabilitySuggestion suggestion_id+pipeline_id+suggestion_type+priority low|medium|high+description + register_check/get_check/list_checks 按 pipeline_id+status 过滤/update_check/delete_check/list_failing_checks + register_expectation/get_expectation/list_expectations/update_expectation/delete_expectation + register_suggestion/get_suggestion/list_suggestions 按 pipeline_id+priority 过滤/delete_suggestion + monitor_pipeline 返回 total_checks/failing_checks/has_expectation/suggestions_count/health_status healthy|degraded|critical + 200 条上限 FIFO + MISSING_PIPELINE/MISSING_CHECK_TYPE/INVALID_STATUS/INVALID_SEVERITY/MISSING_SUGGESTION_TYPE/INVALID_PRIORITY/NOT_FOUND 校验） |
| 163 | Ontology Interfaces | 无 | 功能接口/抽象对象接口/多态 | ✅ 已完成（W2-AR·21 测试·OntologyInterfaceExtensionEngine 增量：W2-K #32 InterfaceEngine 已覆盖接口定义/继承/实现/多态；本批补齐 ① InterfaceLinkType link_type_id+name+source_interface_id+target_interface_id+cardinality one_to_one|one_to_many|many_to_many+description + register_link_type/get_link_type/list_link_types 按 source_interface_id 过滤/update_link_type/delete_link_type + ② InterfaceMarketplaceListing listing_id+interface_id+title+description+version+publisher+status draft|published|imported+published_at + register_listing/get_listing/list_listings 按 status 过滤/publish_to_marketplace draft→published 推进 published_at/import_from_marketplace 创建 status=imported/update_listing/delete_listing + 200 条上限 FIFO + MISSING_NAME/MISSING_SOURCE_INTERFACE/MISSING_TARGET_INTERFACE/INVALID_CARDINALITY/MISSING_INTERFACE/MISSING_TITLE/INVALID_STATUS/NOT_FOUND 校验） |
| 164 | 时间序列（Time Series） | lineage 桩 | TSP/Object Type/传感器/同步索引 | ✅ 已完成（W2-AS·22 测试·TimeSeriesEngine TimeSeriesObject ts_id+name+object_type TSP+description+sync_index_status pending|indexing|ready+created_at+updated_at + Sensor sensor_id+name+ts_object_id+data_type numeric+unit+frequency_seconds+status active + TimeSeriesPoint point_id+sensor_id+timestamp+value+created_at + register_object/get_object/list_objects 按 object_type 过滤/update_object/delete_object/build_sync_index pending→indexing→ready + register_sensor/get_sensor/list_sensors 按 ts_object_id+status 过滤/update_sensor/delete_sensor + ingest_points 批量写入/list_points 按 sensor_id limit/get_latest_point 返回最新点 + 200 条上限 FIFO（_objects/_sensors/_points 均为 list） + MISSING_NAME/INVALID_OBJECT_TYPE/MISSING_TS_OBJECT/INVALID_DATA_TYPE/INVALID_FREQUENCY/INVALID_STATUS/NOT_FOUND 校验） |
| 165 | SAP 集成 | 无连接器 | SAP 认证组件/S/4HANA/ECC/BW | ✅ 已完成（W2-AS·18 测试·SapIntegrationEngine SapConnection conn_id+name+system_type S4HANA|ECC|BW|SLT+host+port+client+auth_type basic|certificate|snc+username+status disconnected|connected + SapImportJob job_id+conn_id+object_type table|bapi|cds|info_provider|bex_query|extractor+source_object+target_dataset+status pending|running|completed|failed+total_rows+imported_rows+error + register_connection/get_connection/list_connections 按 system_type+status 过滤/update_connection/delete_connection/test_connection disconnected→connected + create_import_job/get_import_job/list_import_jobs 按 conn_id+status 过滤/run_import_job pending→running→completed/cancel_import_job running→failed + 200 条上限 FIFO + MISSING_NAME/MISSING_HOST/INVALID_SYSTEM_TYPE/INVALID_AUTH_TYPE/MISSING_CONNECTION/MISSING_SOURCE_OBJECT/INVALID_OBJECT_TYPE/ALREADY_RUNNING/NOT_FOUND 校验） |
| 166 | pb-functions 函数库（381 函数） | 无 | 250+ 表达式/80 变换/AI 函数 | ✅ 已完成（W2-AS·16 测试·PbFunctionsEngine PbFunction func_id+name+category expression|transform|ai+signature+description+return_type+version + PbFunctionCategory category_id+name+description+function_count + register_function/get_function/list_functions 按 category 过滤/search_functions 关键词模糊/update_function/delete_function + register_category/get_category/list_categories/delete_category + 200 条上限 FIFO + MISSING_NAME/INVALID_CATEGORY/NOT_FOUND 校验） |

#### 1.2.5 W2+ 低优先级项（35 项 · Phase 9+）

> 按需推进，部分项可能根据业务需求升级优先级。

| # | 差距项 | 当前 | 目标 | 状态 |
| --- | --- | --- | --- | --- |
| 1 | Dataset Preview CSV 解析引擎 | csv.reader | 4 种解析器/12 配置参数/TextDataFrameReader 切换 | ✅ 已完成（W2-BI·13 测试·CsvParsingEngine csv_reader/dict_reader/pandas/text_dataframe 四解析器 + 12 配置参数 delimiter/quotechar/escapechar/doublequote/skipinitialspace/lineterminator/encoding/skiprows/max_rows/na_values/keep_default_na/dtype + 200 条 FIFO） |
| 2 | Ontology JSON 导出/导入 | 无 | 架构序列化/跨 Ontology 复制 | ✅ 已完成（W2-BI·8 测试·OntologyExchangeEngine export_ontology 序列化 object_types/link_types/properties/metadata + import_ontology 跨 Ontology 复制 + overwrite 控制导入策略 + CRUD + 200 条 FIFO） |
| 3 | Ontology 计算/占用量跟踪 | 无 | 计算秒/V1 V2 存储后端/GB-月 | ✅ 已完成（W2-BI·10 测试·OntologyUsageEngine 6 种 resource_type compute_seconds_vcpu/gpu_t4/gpu_v100/gpu_a10g/storage_v1_gb/storage_v2_gb + record_usage + get_summary 聚合 + gb_month 计算 + 200 条 FIFO） |
| 4 | Action 操作指标 | 无 | 30 天用量/失败率/监控 | ✅ 已完成（W2-BI·13 测试·ActionMetricsEngine success/failure/timeout 三态 + failure_rate=(failure+timeout)/total + avg_duration_ms + 30 天过滤 + dashboard 多 Action 汇总 + 200 条 FIFO） |
| 5 | Data Connection Agent Metrics | 无 | 内存/磁盘/负载/过期时间仪表盘 | ✅ 已完成（W2-AW·18 测试·AgentMetricsEngine AgentMetrics metrics_id+agent_id+memory_usage_mb+disk_usage_gb+cpu_load_percent+queue_depth+recorded_at+status ok|warning|critical+expires_at + AgentMetricsSummary agent_id+latest_memory+latest_disk+latest_cpu+latest_queue+record_count+last_recorded_at + CRUD record_metrics/get_metrics/list_metrics 按 agent_id+status 过滤/update_metrics/delete_metrics + get_summary 聚合最新指标 + get_expiring 按 expires_at 过滤 + validate_config 校验 memory/disk/cpu≥0 + 200 条上限 FIFO + MISSING_AGENT/INVALID_METRICS/NOT_FOUND 校验） |
| 6 | Data Connection Agent 健康监控 | 无 | CPU/Queue/Disk 分级告警规则 | ✅ 已完成（W2-BJ·22 测试·AgentHealthMonitorEngine cpu/queue/disk/memory 四指标 + threshold_warning<threshold_critical 校验 + evaluate 评估生成 warning/critical 告警 + 告警生命周期 active→acknowledged→resolved + 200 条 FIFO） |
| 7 | Data Connection 直连迁移向导 | 无 | 5步迁移+30天回滚 | ✅ 已完成（W2-BJ·20 测试·DirectConnectionMigrationEngine 5步迁移 assess→prepare→migrate→validate→cutover + start/complete_step/skip_step 步进 + rollback 窗口期校验 + plan 状态机 planning→in_progress→completed/rolled_back + 200 条 FIFO） |
| 8 | Data Connection Source Marketplace | 无 | 同步作为 Marketplace 产品内容类型 | ✅ 已完成（W2-BJ·22 测试·SourceMarketplaceEngine database/api/file/stream 四类型 + publish/get/list/update/delete + install 计数 + rate 评分平均 + installation 记录 + 200 条 FIFO） |
| 9 | Data Connection Webhooks Storage | 无 | 6个月存储+full response可选 | ✅ 已完成（W2-BJ·13 测试·WebhookStorageEngine 默认 180 天存储 + full_response 控制 + cleanup_expired 过期清理 + stats 统计 2xx/4xx/5xx/other + include_expired 过滤 + 200 条 FIFO） |
| 10 | Data Connection Agent SSL Certificates | 无 | 代理证书管理 | ✅ 已完成（W2-BK·15 测试·SslCertificateEngine register/get/list/update/revoke + check_expiry days_remaining/is_expired/is_expiring_soon + renew 重新激活 + 200 条 FIFO） |
| 11 | Data Health 通知打盹（Snoozing） | 无 | 单独/批量打盹 + 打盹历史 | ✅ 已完成（W2-BK·13 测试·HealthSnoozeEngine snooze/batch_snooze/unsnooze + get_active_snooze 过期判断 + cleanup_expired 清理 + history 打盹历史 + 200 条 FIFO） |
| 12 | Data Health 上下文面板 | 无 | 评论/问题/计划/来源信息 | ✅ 已完成（W2-BK·10 测试·HealthContextPanelEngine comment/issue/plan/source 四类型 + add/get/list/update/delete + get_context_summary 按类型计数 + 200 条 FIFO） |
| 13 | Data Health Marketplace集成 | 无 | 将健康检查添加到Marketplace产品 | ✅ 已完成（W2-BK·12 测试·HealthMarketplaceEngine info/warning/critical 三级 + integrate/get/list/update/enable/disable + 200 条 FIFO） |
| 14 | Linter 规则引擎 | 无 | 反模式检测/建议/修复提案 | ✅ 已完成（W2-BL·15 测试·LinterRuleEngine info/warning/error/critical 四级 + naming/security/performance/style/architecture 五类 + detect 模式匹配 + findings 状态机 open→fixed/ignored + fix_proposal + apply_fix + 200 条 FIFO） |
| 15 | Linter 扫描调度 | 无 | 定期扫描/资源范围/规则范围 | ✅ 已完成（W2-BL·8 测试·LinterScanScheduleEngine all/specific_type/specific_id 资源范围 + all/specific_category/specific_severity 规则范围 + run_scan 执行 + next_run_at 调度 + 200 条 FIFO） |
| 16 | Foundry Rules 规则引擎 | 无 | 点选规则/条件/工作流 | ✅ 已完成（W2-BL·8 测试·FoundryRulesEngine condition/schedule/event 三触发 + notify/create_object/update_object/call_function 四动作 + execute_rule 执行 + enabled 控制 + 200 条 FIFO） |
| 17 | Foundry Rules 时间序列 | 无 | 时间序列同步/规则 | ✅ 已完成（W2-BL·10 测试·FoundryTimeSeriesEngine register_sync + record_datapoint + trend up/down/stable 趋势计算 + pause/resume + datapoints 降序+limit + 200 条 FIFO） |
| 18 | Dynamic Scheduling 甘特图 | 无 | 拖拽调度/约束/分配建议 | ✅ 已完成（W2-BM·12 测试·GanttScheduleEngine 任务CRUD + move_task 保持时长+依赖校验 + assign_resource + suggest_assignment + 200 条 FIFO） |
| 19 | Dynamic Scheduling 机器学习 | 无 | ML支持的实时调度解决方案 | ✅ 已完成（W2-BM·12 测试·MLSchedulingEngine regression/lstm/arima/transformer 四算法 + train_model + predict 需已训练 + 200 条 FIFO） |
| 20 | Workshop 拖拽 | 弱 | 自由拖拽 | ✅ 已完成（W2-BM·18 测试·WorkshopDragEngine node/edge/port/label 四类型 + move/resize/rotate + lock/unlock + session 管理 + 200 条 FIFO） |
| 21 | 计算秒定价 + 用量计量 | 无 | vCPU/T4/V100/A10G 计算秒 | ✅ 已完成（W2-BM·16 测试·ComputePricingEngine vcpu/gpu_t4/gpu_v100/gpu_a10g 四类型 + start/stop metering + cost 计算 + bill 状态机 + usage_summary 聚合 + 200 条 FIFO） |
| 22 | 预测扩缩（Predictive Auto-scaling） | 无 | 历史负载预测 + 主动预热 | ✅ 已完成（W2-BN·13 测试·PredictiveAutoscaleEngine scale_up/down/no_action 三态 + warmup 状态机 scheduled→executed/cancelled + 200 条 FIFO） |
| 23 | Telemetry / Format / Container log source | 无 | 遥测开关 + 日志格式 + 来源 | ✅ 已完成（W2-BN·9 测试·TelemetryFormatEngine json/otel/plain 三格式 + stdout/stderr/file/container 四来源 + sample_rate 校验 + upsert 配置 + collect 采集 + 200 条 FIFO） |
| 24 | Volume mounts（副本内共享卷） | 无 | Add volume + 共享存储 | ✅ 已完成（W2-BN·9 测试·VolumeMountEngine emptydir/pvc/configmap/secret 四类型 + readwrite/readonly/many 三模式 + attach/detach + get_shared_volumes + 200 条 FIFO） |
| 25 | COP 实时态势 | 概览 | 实时监控 | ✅ 已完成（W2-BN·13 测试·CopRealtimeEngine threshold 阈值管理 + record_metric 自动判级 normal/warning/critical + alert 自动生成 + dashboard 汇总统计 + 200 条 FIFO） |
| 26 | 分布式追踪 | 无 | OpenTelemetry | ✅ 已完成（W2-BO·16 测试·DistributedTracingEngine trace/span 层级 + start_trace/start_span/finish_span + trace_tree 汇总 + 200 条 FIFO） |
| 27 | 管道性能优化 | 无 | Spark/投影/原生加速/Profiles | ✅ 已完成（W2-BO·11 测试·PipelinePerfEngine spark_optimization/projection_pushdown/native_acceleration/profile_tuning 四优化 + apply_profile + benchmark improvement_pct 计算 + 200 条 FIFO） |
| 28 | Foundry Rules 规则引擎 | 2 条 lint | 规则 Object 模型/工作流/多场景集成 | ✅ 已完成（合并至 W2-BL #16） |
| 29 | Linter 质量扫描 | 2 条 lint | 规则库/扫描调度/修复提案/影响追踪 | ✅ 已完成（合并至 W2-BL #14/#15） |
| 30 | 地理空间数据框架 | 无 | GeoJSON/PostGIS/矢量/栅格/投影 | ✅ 已完成（W2-BO·13 测试·GeospatialEngine point/linestring/polygon/multipoint/multilinestring/multipolygon 六类型 + query_bbox/query_distance 空间查询 + export_geojson FeatureCollection + 200 条 FIFO） |
| 31 | Map 地图可视化 | 占位文字 | 地图图层/地理搜索/Workshop 模板 | ✅ 已完成（W2-BO·13 测试·MapVisualizationEngine tile/vector/geojson/heat/cluster 五图层 + toggle_visibility + template 管理 + 200 条 FIFO） |
| 32 | Vertex 数字孪生 | 无 | 数字孪生建模/模拟/因果分析 | ✅ 已完成（W2-BP·14 测试·DigitalTwinEngine twin CRUD + run_simulation 仿真 + analyze_causality 因果分析 correlation[-1,1] + 200 条 FIFO） |
| 33 | 地理时间序列 | 无 | 位置追踪 Object/同步组件 | ✅ 已完成（W2-BP·13 测试·GeoTimeSeriesEngine track CRUD + record_point lat/lon 校验 + get_track_path 路径距离 + 200 条 FIFO） |
| 34 | Process Mining | 无 | 事件日志/流程发现/瓶颈分析 | ✅ 已完成（W2-BP·10 测试·ProcessMiningEngine event log + discover_flow 活动/转移/瓶颈发现 + get_flow_analysis 分析 + 200 条 FIFO） |
| 35 | Hyperauto 开箱集成 | 无 | 自动同步/自动 Ontology/ERP/CRM | ✅ 已完成（W2-BP·12 测试·HyperautoEngine erp/crm/scada/iot 四系统集成 + pause/resume + run_sync 自动同步 + 200 条 FIFO） |

#### 1.2.6 停车场项（7 项 · ⏸ 暂停）

> 后置不开或条件不具备。部分项可能在后续 Wave 根据业务需要解除暂停。

| # | 差距项 | 当前 | 目标 | 暂停原因 | 状态 |
| --- | --- | --- | --- | --- | --- |
| 1 | Dataset Iceberg | 无 | 事务表格式 | 事务表格式后置，SQLite/PG 足够 | ⏸ 暂停 |
| 2 | Ontology AI/ML 模型集成 | 无 | 建模目标/评估/部署/映射到 Ontology | ML 模型集成远期 | ⏸ 暂停 |
| 3 | 共享 Ontology/跨空间迁移 | 无 | 多组织共享空间/资源跨空间迁移 | 跨空间迁移远期 | ⏸ 暂停 |
| 4 | Object Monitors（监视器） | 无 | 3 种条件/实时评估/自动操作/通知 | Automate 远期 | ⏸ 暂停 |
| 5 | Apollo Full Spoke | Lite | 远程下发 | 远程下发 Lite 版已满足 | ⏸ 暂停 |
| 6 | 多语言支持（任意可容器化） | 无 | Python/Java/Go/Rust 等 | Compute Module 任意语言容器化远期 | ⏸ 暂停 |
| 7 | 真 K8s 容器编排 | helm-mock MVP | 真 kind/K8s 舰队（`k8sDeferred=True`） | helm-mock MVP 足够，真 K8s 舰队远期 | ⏸ 暂停 |

#### 1.2.7 已达成项（2 项 · ✅）

> 已实现，保持维护。

| # | 差距项 | 当前 | 状态 |
| --- | --- | --- | --- |
| 1 | Connection 注册/配置 | 6 个连接器 | ✅ 已完成 |
| 2 | Action CRUD | 完整 | ✅ 已完成 |

---

## 2. Phase 0 · 基础设施与测试框架

> **目标**：搭建 CI 管线、测试模板、截图归档机制，为后续所有 Phase 提供工程基座。
> **状态**：✅ 已完成

### 2.1 里程碑

| 里程碑 | 交付物 |
| --- | --- |
| M0.1 | 后端 pytest 配置完善：conftest.py 含 FastAPI TestClient fixture + 临时 DB fixture |
| M0.2 | 前端 vitest 配置完善：setup.ts 含 jsdom + React Testing Library |
| M0.3 | CI 脚本：`scripts/ci.sh` 串联 `pytest` + `vitest` + `tsc --noEmit` |
| M0.4 | 截图归档目录：`docs/screenshots/` 按 Phase 分目录 |
| M0.5 | UI 对标检查清单模板：`docs/ui-checklist-template.md` |

### 2.2 单元测试要求

| 功能点 | 测试文件 | 测试用例 |
| --- | --- | --- |
| pytest TestClient fixture | `tests/conftest.py` | `test_client_returns_200_on_health` |
| 临时 DB fixture | `tests/conftest.py` | `test_tmp_db_is_isolated` |
| vitest setup | `apps/web/src/test-setup.ts` | `test_renders_without_crash` |
| CI 脚本 | `scripts/ci.sh` | 手动执行验证 |

### 2.3 集成自测

- 重启后端 + 前端，确认 `pytest` 和 `vitest` 均全绿
- 访问首页 `/`，确认无白屏

---

## 3. Phase 1 · 核心引擎层

> **W1 项**：W1-1（Function 表达式引擎）、W1-4（Build 引擎）、W1-10（Function 类型安全 + 沙箱）
> **前置条件**：Phase 0 完成
> **本 Phase 是整个 W1 的地基——Function 引擎被 Logic/Pipeline Builder/Action 依赖；Build 引擎被 Funnel/Transform/Lineage 依赖**
> **状态**：✅ 已完成

### 3.1 W1-1 · Function 表达式引擎

#### 3.1.1 功能定义

| 子功能 | 说明 |
| --- | --- |
| 表达式解析器 | 支持基本算术、字符串操作、属性访问、条件表达式 |
| 类型推导 | 表达式 → 输出类型推断（string / number / boolean / timestamp） |
| 求值引擎 | 给定输入上下文 → 执行表达式 → 返回结果 |
| Ontology API 调用 | 表达式内可调用 `object.getProperty()` / `object.link()` 等 |
| 错误处理 | 类型不匹配 / 空值 / 除零等 → 结构化错误 |

#### 3.1.2 后端实现

| 文件 | 职责 |
| --- | --- |
| `aos_api/function_engine.py` | 表达式词法分析 + 语法分析 + AST 构建 |
| `aos_api/function_engine.py` | 求值器（visitor 模式遍历 AST） |
| `aos_api/function_engine.py` | 类型推导器（AST → 输出类型） |
| `aos_api/routers/functions.py` | API 端点：`POST /v1/functions/eval`（表达式求值）、`POST /v1/functions/typecheck`（类型检查） |

#### 3.1.3 单元测试

| 测试文件 | 测试用例 |
| --- | --- |
| `tests/test_function_engine.py` | `test_arithmetic_expression` — `1 + 2 * 3` → 7 |
| | `test_string_concat` — `"Hello" + " " + name` → "Hello World" |
| | `test_property_access` — `order.amount * 1.1` → 加税后金额 |
| | `test_conditional_expression` — `if amount > 100 then "大额" else "小额"` |
| | `test_null_safety` — 空值安全访问 `order.customer?.name` |
| | `test_type_inference_number` — 表达式 → number 类型 |
| | `test_type_inference_string` — 表达式 → string 类型 |
| | `test_type_inference_boolean` — 表达式 → boolean 类型 |
| | `test_type_error_mismatch` — string + number → 类型错误 |
| | `test_division_by_zero` — 除零 → 结构化错误 |
| | `test_ontology_api_call` — `object.getProperty("amount")` 正确求值 |
| | `test_complex_expression` — 嵌套表达式（条件 + 算术 + 属性访问） |
| `tests/test_function_engine_api.py` | `test_eval_endpoint` — POST /v1/functions/eval |
| | `test_typecheck_endpoint` — POST /v1/functions/typecheck |
| | `test_eval_error_response` — 错误表达式 → 400 + 结构化错误 |

#### 3.1.4 UI 功能设计（对标需求文档）

**对标 HTML 蓝图页**：`ontology-function.html`（Function Type 视图）

> **UI 对标说明**：Function 引擎本身无独立页面，其 UI 展示形态为 Ontology Manager 中的 Function Type 视图页。

| UI 区域 | 对标蓝图 | 设计规范 |
| --- | --- | --- |
| 页面布局 | `ontology-function.html` 两栏式 | 左侧 `w-56` 全局导航 + 右侧主内容区，`max-w-xl mx-auto` 居中 |
| Tab 栏 | 四个 Tab：Overview / Configuration / Type Safety / Usage History | 使用 `data-tab` / `data-tab-panel` 属性切换；激活 Tab 有下划线高亮（`border-b-2` + 主题色） |
| Overview 面板 | 函数名（等宽字体标题）+ 输入输出类型说明（`Order.amount: Double → Double`）+ 场景描述 + `<pre>` 代码块展示函数实现 + "打开 Code Repository" 链接 | 代码块使用 `code-block` 样式 + 语法高亮（`code-cm` / `code-fn` / `code-str`） |
| Configuration 面板 | 运行时 / 沙箱 / 超时限制卡片 | 卡片使用 `--aos-card` 背景色 + `--aos-border` 边框 |
| Type Safety 面板 | 编译失败示例（rose 边框）+ 价值说明（emerald 边框） | 成功/失败用 `--aos-accent` / rose 色区分 |
| Usage History 面板 | 调用统计表格（日期 / 调用次数 / 调用方 / P99 延迟） | 表格 sticky thead + `table-row-hover` |
| 顶部工具栏 | "逻辑核 · 默认只读"徽章（emerald）+ "壳: 审核订单 →"链接（violet 边框） | 徽章使用 `badge-*` 类 |

**前端组件**：`apps/web/src/pages/s2/FunctionTypePage.tsx`（新建，嵌入 Ontology 详情页路由）

---

### 3.2 W1-4 · Build 引擎

#### 3.2.1 功能定义

| 子功能 | 说明 |
| --- | --- |
| Job / JobSpec 模型 | 一次 Build = 一个 Job，包含 JobSpec（输入数据集 + 变换定义 + 输出目标） |
| Job 生命周期 | PENDING → RUNNING → SUCCEEDED / FAILED / CANCELLED |
| 事务锁定 | Build 期间输出数据集被锁定，其他 Build 不可并发写入 |
| Job 执行器 | 按顺序执行 JobSpec 中的变换步骤 |
| 日志收集 | 每个 Job 收集结构化执行日志（时间戳 + 级别 + 消息） |
| 失败重试 | Job 失败后可手动重试（自动重试在 Phase 6） |

#### 3.2.2 后端实现

| 文件 | 职责 |
| --- | --- |
| `aos_api/jobs/build_engine.py` | Job 模型 + JobSpec 模型 + 生命周期状态机 |
| `aos_api/jobs/build_engine.py` | Job 执行器（异步执行变换步骤） |
| `aos_api/jobs/build_engine.py` | 事务锁定管理器（数据集级互斥锁） |
| `aos_api/jobs/build_engine.py` | 日志收集器（内存 ring buffer） |
| `aos_api/routers/builds.py` | API 端点：`POST /v1/builds`（创建 Job）、`GET /v1/builds`（列表）、`GET /v1/builds/{id}`（详情含日志）、`POST /v1/builds/{id}/cancel`（取消） |

#### 3.2.3 单元测试

| 测试文件 | 测试用例 |
| --- | --- |
| `tests/test_build_engine.py` | `test_create_job_pending` — 创建 Job 初始状态为 PENDING |
| | `test_job_lifecycle_success` — PENDING → RUNNING → SUCCEEDED |
| | `test_job_lifecycle_failure` — PENDING → RUNNING → FAILED |
| | `test_job_lifecycle_cancelled` — RUNNING → CANCELLED |
| | `test_transaction_lock_prevents_concurrent` — 同一输出数据集并发 Build → 第二个等待 |
| | `test_transaction_lock_released_on_completion` — Build 完成后锁释放 |
| | `test_job_log_collection` — 执行日志按时间戳排列 |
| | `test_jobspec_validation` — 无效 JobSpec（缺输入/输出）→ 400 |
| | `test_job_retry_after_failure` — 失败后手动重试 → 新 Job |
| `tests/test_builds_api.py` | `test_create_build_endpoint` — POST /v1/builds |
| | `test_list_builds_endpoint` — GET /v1/builds 返回列表 |
| | `test_get_build_detail_with_logs` — GET /v1/builds/{id} 含日志 |
| | `test_cancel_build_endpoint` — POST /v1/builds/{id}/cancel |
| | `test_build_not_found_404` — 不存在的 Job → 404 |

#### 3.2.4 UI 功能设计（对标需求文档）

**对标 HTML 蓝图页**：`builds.html`（Build 引擎任务列表）

| UI 区域 | 对标蓝图 | 设计规范 |
| --- | --- | --- |
| 页面布局 | `builds.html` 两栏式 | 左侧 `w-56` 全局导航 + 主区域内部再分两栏：左 `w-72` 构建历史列表 + 右任务图/日志区 |
| 顶部工具栏 | 极简 header `h-14`：左侧面包屑、右侧用户头像 | 无额外操作按钮，保持简洁 |
| 左侧构建历史 | 构建卡片列表（`<button>` 列表），每卡片显示 Build 编号 + 成功/失败状态（emerald/rose）+ 时间 + 部署者 + 耗时 | 选中项使用 `bg-white/[0.04]` + `border-cyan-400/20` 高亮 |
| 右侧任务图区 | 顶部 Build 标题 + 管道链接 + "查看输出数据集"链接；下方水平排列任务图（`flex items-center gap-3 flex-wrap`），每个任务节点为带颜色边框卡片 | 节点间用 SVG `flow-line-active` 水平连接线相连；每节点显示类型标签 + 名称 + 耗时 |
| 实时日志区 | 占据剩余高度（`flex-1`），顶部状态栏 + "实时日志"标题 + 完成状态指示灯；主体为 `<pre><code>` 代码块 | 使用 `code-block` 样式 + `code-cm` / `code-fn` / `code-str` 语法高亮 |
| 状态色规范 | 成功 = emerald(`rgb(16 185 129)`)；失败 = rose(`rgb(244 63 94)`)；运行中 = cyan(`rgb(34 211 238)`) | 对应 `--aos-accent` 主题色体系 |

**前端组件**：`apps/web/src/pages/BuildsPage.tsx`（新建）

---

### 3.3 W1-10 · Function 类型安全 + 沙箱

#### 3.3.1 功能定义

| 子功能 | 说明 |
| --- | --- |
| Schema → TypeScript 编译 | 从 Ontology Object Type 的 Schema 生成 TypeScript 类型定义 |
| 类型校验 | Function 定义时校验输入/输出类型是否与 Schema 匹配 |
| 沙箱隔离 | Function 执行在受限环境中：禁止文件系统访问、禁止网络访问（白名单除外）、内存限制 |
| 超时控制 | 单次 Function 执行超时（默认 30s） |
| 可组合性 | Function A 的输出可作为 Function B 的输入 |

#### 3.3.2 后端实现

| 文件 | 职责 |
| --- | --- |
| `aos_api/function_typesafe.py` | Schema → TypeScript 类型生成器 |
| `aos_api/function_typesafe.py` | 类型校验器（编译时检查） |
| `aos_api/function_sandbox.py` | 沙箱执行环境（RestrictedPython 或子进程隔离） |
| `aos_api/function_sandbox.py` | 超时控制（signal + 超时异常） |
| `aos_api/function_sandbox.py` | 内存限制（resource.setrlimit） |

#### 3.3.3 单元测试

| 测试文件 | 测试用例 |
| --- | --- |
| `tests/test_function_typesafe.py` | `test_schema_to_typescript_string` — string 类型 → `string` |
| | `test_schema_to_typescript_number` — number 类型 → `number` |
| | `test_schema_to_typescript_object` — Object Type → 接口定义 |
| | `test_type_check_pass` — 类型匹配 → 通过 |
| | `test_type_check_fail_mismatch` — 类型不匹配 → 编译错误 |
| | `test_type_check_missing_property` — 缺少属性 → 编译错误 |
| `tests/test_function_sandbox.py` | `test_sandbox_blocks_file_access` — `open("/etc/passwd")` → 拒绝 |
| | `test_sandbox_blocks_network` — `socket.socket()` → 拒绝 |
| | `test_sandbox_allows_ontology_api` — `object.getProperty()` → 允许 |
| | `test_sandbox_timeout` — 死循环函数 → 超时异常 |
| | `test_sandbox_memory_limit` — 大数组分配 → 内存错误 |
| | `test_function_composition` — Function A → B 链式调用 |

#### 3.3.4 UI 功能设计

**对标 HTML 蓝图页**：`ontology-function.html` → Type Safety Tab

| UI 区域 | 对标蓝图 | 设计规范 |
| --- | --- | --- |
| Type Safety Tab | 编译失败示例（rose 边框卡片）+ 价值说明（emerald 边框卡片） | 失败卡片左侧 rose 竖线 + 错误信息；成功卡片左侧 emerald 竖线 + 价值说明 |
| Configuration Tab | 运行时 / 沙箱 / 超时限制三列卡片 | 每卡片显示限制名 + 当前值 + 单位 |

---

### 3.4 Phase 1 集成自测

| 步骤 | 检查项 |
| --- | --- |
| ① 重启 | 后端启动 → `startup_meta_store_ok` 日志出现 |
| ② 全量测试 | `pytest tests/ -v` 全绿 |
| ③ 页面加载 | `/builds` 页面加载无白屏；Ontology 详情页 Function Tab 可切换 |
| ④ 风格一致 | BuildsPage 布局对标 `builds.html`：左侧历史列表 + 右侧任务图 + 日志区三段式 |
| ⑤ 跨模块链路 | 创建 Build Job → 执行 → 状态更新 → 日志可查 |

---

## 4. Phase 2 · 数据集成核心

> **W1 项**：W1-5（Funnel 四阶段管道）、W1-8（Transform 算子库）、W1-13（Data Lineage DAG 可视化）、W1-14（Pipeline Builder 交互式 DAG 编辑器）
> **前置条件**：Phase 1 完成（Build 引擎 + Function 引擎）
> **本 Phase 构建数据集成 IDE 的核心能力——从变换算子到可视化编排到血缘追踪**
> **状态**：✅ 已完成

### 4.1 W1-4 补充 · Build 引擎接入（Phase 1 已建，此处接入数据集成）

> Build 引擎在 Phase 1 已实现核心 Job/JobSpec，Phase 2 将其接入 Pipeline / Transform / Funnel 执行链路。

### 4.2 W1-8 · Transform 算子库

#### 4.2.1 功能定义

| 算子 | 输入 | 输出 | 说明 |
| --- | --- | --- | --- |
| Filter | 数据集 + 条件表达式 | 过滤后数据集 | 使用 W1-1 Function 引擎求值条件 |
| Join | 左数据集 + 右数据集 + 连接键 | 合并数据集 | 支持 inner / left / right / full |
| Aggregate | 数据集 + 分组键 + 聚合函数 | 聚合后数据集 | count / sum / avg / min / max |
| Explode | 数据集 + 数组列 | 展开后数据集 | 每行数组元素 → 独立行 |
| Cast | 数据集 + 列名 + 目标类型 | 类型转换后数据集 | string→number / string→timestamp 等 |
| Union | 多数据集 | 合并数据集 | 去重 / 不去重可选 |
| Sort | 数据集 + 排序列 | 排序后数据集 | asc / desc |
| Distinct | 数据集 | 去重数据集 | 全列去重 |
| Expression | 数据集 + 表达式 | 新列数据集 | 使用 W1-1 Function 引擎计算新列 |

#### 4.2.2 后端实现

| 文件 | 职责 |
| --- | --- |
| `aos_api/transforms/operators.py` | 算子基类 `TransformOperator` + 各算子实现 |
| `aos_api/transforms/operators.py` | 算子注册表（名称 → 算子类） |
| `aos_api/transforms/pipeline.py` | 算子链执行器（按 DAG 拓扑排序执行） |
| `aos_api/routers/transforms.py` | API 端点：`GET /v1/transforms/operators`（算子目录）、`POST /v1/transforms/preview`（预览执行） |

#### 4.2.3 单元测试

| 测试文件 | 测试用例 |
| --- | --- |
| `tests/test_transform_operators.py` | `test_filter_operator` — 条件过滤正确行数 |
| | `test_filter_with_expression` — 使用 Function 引擎的条件表达式 |
| | `test_join_inner` — inner join 结果正确 |
| | `test_join_left` — left join 保留左表所有行 |
| | `test_aggregate_count` — 分组计数 |
| | `test_aggregate_sum` — 分组求和 |
| | `test_explode_array` — 数组列展开 |
| | `test_cast_string_to_number` — 字符串转数字 |
| | `test_union_dedup` — 合并去重 |
| | `test_sort_descending` — 降序排列 |
| | `test_distinct_rows` — 全列去重 |
| | `test_expression_new_column` — 表达式生成新列 |
| `tests/test_transform_pipeline.py` | `test_pipeline_sequential` — 顺序执行 Filter → Join → Aggregate |
| | `test_pipeline_dag_order` — DAG 拓扑排序正确 |
| | `test_pipeline_preview_limit` — 预览限制行数 |
| `tests/test_transforms_api.py` | `test_list_operators` — GET /v1/transforms/operators |
| | `test_preview_endpoint` — POST /v1/transforms/preview |

#### 4.2.4 UI 功能设计（对标需求文档）

**对标 HTML 蓝图页**：`pipeline.html`（Pipeline Builder 画布）中的变换节点

| UI 区域 | 对标蓝图 | 设计规范 |
| --- | --- | --- |
| 变换节点卡片 | `pipeline.html` 中 `pipeline-node` 卡片，按颜色区分类型 | 输入=amber(`rgb(245 158 11)`)；变换=cyan/purple（Filter=cyan, Join=purple）；输出=emerald |
| 节点内容 | 类型标签 + 名称 + 简要配置摘要 | 卡片 `--aos-card` 背景 + 类型色边框 |
| 节点连接线 | SVG `flow-line` 贝塞尔曲线连接 | 默认 `--aos-border-strong` 色；活跃路径 `flow-line-active` 高亮 |
| 变换配置面板 | 右侧 `w-72` 侧栏，选择变换类型后显示对应配置表单 | 表单字段根据算子类型动态渲染 |

---

### 4.3 W1-5 · Funnel 四阶段管道

#### 4.3.1 功能定义

| 阶段 | 说明 |
| --- | --- |
| Changelog | 监听 L1 数据集变更，生成变更日志（insert / update / delete） |
| Merge | 将变更日志合并到 L2 对象的 backing dataset（LastWriteWins / 字段级合并） |
| Indexing | 将合并后的数据索引到对象存储后端（Phonograph / OSv2 模拟） |
| Hydration | 水合完成后触发通知，对象可在 Object Explorer / Workshop 中查看 |

#### 4.3.2 后端实现

| 文件 | 职责 |
| --- | --- |
| `aos_api/funnel_engine.py` | 四阶段状态机 + 阶段间数据传递 |
| `aos_api/funnel_engine.py` | Changelog 生成器（diff-based 增量变更检测） |
| `aos_api/funnel_engine.py` | Merge 策略实现（LastWriteWins / 字段级合并） |
| `aos_api/funnel_engine.py` | Indexing 执行器（写入 object_store） |
| `aos_api/funnel_engine.py` | Hydration 通知器（事件发布） |
| `aos_api/routers/funnel.py` | API 端点：`POST /v1/funnel/run`（触发管道）、`GET /v1/funnel/{id}/status`（四阶段状态） |

#### 4.3.3 单元测试

| 测试文件 | 测试用例 |
| --- | --- |
| `tests/test_funnel_engine.py` | `test_changelog_insert` — 新增行 → INSERT 变更 |
| | `test_changelog_update` — 修改行 → UPDATE 变更 |
| | `test_changelog_delete` — 删除行 → DELETE 变更 |
| | `test_changelog_incremental` — 仅检测变化行，未变化行不生成变更 |
| | `test_merge_last_write_wins` — 同主键多版本 → 最后写入胜出 |
| | `test_merge_field_level` — 字段级合并，不同字段取不同版本 |
| | `test_indexing_writes_to_object_store` — 索引后对象可在 object_store 查到 |
| | `test_hydration_notification` — 水合完成后事件发布 |
| | `test_full_pipeline_four_stages` — 完整四阶段端到端 |
| | `test_pipeline_idempotent` — 相同输入重跑结果一致 |
| `tests/test_funnel_api.py` | `test_run_funnel_endpoint` — POST /v1/funnel/run |
| | `test_funnel_status_endpoint` — GET /v1/funnel/{id}/status |

#### 4.3.4 UI 功能设计（对标需求文档）

**对标 HTML 蓝图页**：`funnel.html`（Funnel 映射编辑器）+ `okf-funnel.html`（跳转到 funnel.html）

| UI 区域 | 对标蓝图 | 设计规范 |
| --- | --- | --- |
| 页面布局 | `funnel.html` 三栏式 | 左 `w-56` 导航 + 左 `w-72` 源 Schema 侧栏 + 右主映射区 |
| 顶部工具栏 | header：左侧面包屑；右侧"行业垂直定制"徽章 + "自动映射"按钮（emerald）+ "Lint 检查"按钮 + "发布"主按钮（emerald，title 提示"Lint 失败不可 Publish"） | 发布按钮在 Lint 未通过时 disabled |
| 左侧源 Schema 侧栏 | 顶部行业模板选择器（三按钮）+ 源数据集名称链接 + 源列名列表（`<ul>` 动态渲染）+ 底部"谛听 vs Palantir"说明卡片 | 列名列表可拖拽到右侧映射表 |
| 右侧映射区 | 顶部标题栏（映射标题 + 完成度百分比 + 三能力标签）+ 映射表格（源列 → Object Property / 类型 / 置信度，低于 70% 显示 amber）+ OKF 数据质量清洗规则面板（amber 边框）+ 底部 Lint 状态 + AOS Constitution 契约卡片（三列网格） | 置信度颜色：≥70% 正常色；<70% amber(`rgb(245 158 11)`) |
| 四阶段状态 | 底部状态栏显示 Changelog → Merge → Indexing → Hydration 四阶段进度 | 每阶段图标 + 状态色（PENDING=灰 / RUNNING=cyan 闪烁 / DONE=emerald / FAILED=rose） |

---

### 4.4 W1-13 · Data Lineage DAG 可视化

#### 4.4.1 功能定义

| 子功能 | 说明 |
| --- | --- |
| 血缘图构建 | 从 Build Job 历史构建 DAG（数据集 → 变换 → 数据集） |
| 节点类型 | 数据集节点 / 管道节点 / Funnel 节点 / Source 节点 |
| 交互式展开 | 点击节点 → 展开/折叠上下游 |
| 节点着色 | 按类型着色（数据集=cyan / 管道=purple / Source=amber / Funnel=emerald） |
| 搜索与侧边面板 | 搜索节点名 + 左侧详情面板（上游/变换/下游三段分组） |
| 列级血缘 | 数据集节点的列级追踪（输入列 → 变换 → 输出列） |

#### 4.4.2 后端实现

| 文件 | 职责 |
| --- | --- |
| `aos_api/lineage_graph.py` | 血缘图模型（节点 + 边）+ 图构建器（从 Build 历史解析） |
| `aos_api/lineage_graph.py` | 节点展开/折叠逻辑 |
| `aos_api/lineage_graph.py` | 列级血缘追踪器 |
| `aos_api/routers/lineage.py` | API 端点：`GET /v1/lineage/graph?dataset={rid}`（全图）、`GET /v1/lineage/node/{id}`（节点详情） |

#### 4.4.3 单元测试

| 测试文件 | 测试用例 |
| --- | --- |
| `tests/test_lineage_graph.py` | `test_build_graph_from_builds` — 从 Build 历史构建 DAG |
| | `test_node_types` — 数据集/管道/Funnel/Source 四种节点类型 |
| | `test_expand_upstream` — 展开上游节点 |
| | `test_expand_downstream` — 展开下游节点 |
| | `test_collapse_node` — 折叠节点 |
| | `test_search_by_name` — 按名称搜索节点 |
| | `test_column_level_lineage` — 列级追踪（输入列 → 输出列） |
| | `test_focal_node_highlight` — 焦点节点高亮 |
| `tests/test_lineage_api.py` | `test_graph_endpoint` — GET /v1/lineage/graph |
| | `test_node_detail_endpoint` — GET /v1/lineage/node/{id} |

#### 4.4.4 UI 功能设计（对标需求文档）

**对标 HTML 蓝图页**：`lineage.html`（数据沿袭可视化）

| UI 区域 | 对标蓝图 | 设计规范 |
| --- | --- | --- |
| 页面布局 | `lineage.html` 三栏式 | 左 `w-56` 导航 + 左 `w-64` 沿袭详情侧栏 + 右主图形区 |
| 顶部工具栏 | header `h-14`：左侧面包屑；右侧 DLQ 死信计数徽章（rose，显示"DLQ 死信 N"）+ 分支选择器 + 用户头像 | DLQ 计数 >0 时显示，=0 时隐藏 |
| 左侧详情侧栏 | 标题"沿袭详情" + 焦点数据集名称 + 上下游计数；按"上游"/"变换"/"下游"三段分组列出链接列表 | 每项为可点击 `<a>` 链接，跳转到对应详情页 |
| 主图形区 | 带网格背景画布（`grid-pattern`）+ SVG `flow-line` 边线（含 `flow-line-active` 高亮态）+ 绝对定位节点卡片 | 焦点节点 `border-2` + 主题色高亮（`border-cyan-400/50`） |
| 节点着色 | 数据集=cyan / 管道=purple / Source=amber / Funnel=emerald | 每种节点类型对应 `badge-*` 色系 |
| 动态切换 | URL 参数 `?view=maintenance` 切换为"维修文档"沿袭视图 | JS 动态替换侧栏内容和图形区节点 |

---

### 4.5 W1-14 · Pipeline Builder 交互式 DAG 编辑器

#### 4.5.1 功能定义

| 子功能 | 说明 |
| --- | --- |
| 拖拽节点 | 从算子面板拖拽变换节点到画布 |
| 连线 | 从节点输出端口拖拽到另一节点输入端口，生成贝塞尔曲线连接 |
| 节点配置 | 点击节点 → 右侧面板显示配置表单 |
| 撤销/重做 | Ctrl+Z / Ctrl+Shift+Z 操作历史 |
| 预览执行 | 点击"预览"→ 执行 DAG → 底部面板显示结果 |
| DAG 保存 | 将画布节点 + 连线序列化为 Pipeline JSON 保存 |
| 分支选择 | 顶部分支选择器（master / feature 分支） |
| 输出配置 | 右侧面板：输出数据集名 + 格式（Parquet/Avro/CSV）+ 表格式 + 写入模式（SNAPSHOT/APPEND/UPDATE）+ Schema 列表 |

#### 4.5.2 后端实现

| 文件 | 职责 |
| --- | --- |
| `aos_api/pipeline_dag.py` | DAG 模型（节点 + 边）+ 序列化/反序列化 |
| `aos_api/pipeline_dag.py` | DAG 校验器（无环检测 + 端口类型匹配） |
| `aos_api/routers/pipelines.py` | API 端点：`POST /v1/pipelines`（保存 DAG）、`GET /v1/pipelines/{id}`（加载 DAG）、`POST /v1/pipelines/{id}/preview`（预览执行） |

#### 4.5.3 单元测试

| 测试文件 | 测试用例 |
| --- | --- |
| `tests/test_pipeline_dag.py` | `test_dag_serialize_deserialize` — 序列化后反序列化还原 |
| | `test_dag_acyclic_check_pass` — 无环 DAG 通过校验 |
| | `test_dag_acyclic_check_fail` — 有环 DAG → 校验失败 |
| | `test_dag_port_type_match` — 端口类型匹配通过 |
| | `test_dag_port_type_mismatch` — 端口类型不匹配 → 校验失败 |
| | `test_dag_preview_execution` — 预览执行返回结果 |
| `tests/test_pipelines_api.py` | `test_save_pipeline_endpoint` — POST /v1/pipelines |
| | `test_load_pipeline_endpoint` — GET /v1/pipelines/{id} |
| | `test_preview_pipeline_endpoint` — POST /v1/pipelines/{id}/preview |

#### 4.5.4 UI 功能设计（对标需求文档）

**对标 HTML 蓝图页**：`pipeline.html`（Pipeline Builder 画布）

| UI 区域 | 对标蓝图 | 设计规范 |
| --- | --- | --- |
| 页面布局 | `pipeline.html` 三栏式 | 左 `w-56` 导航 + 中主内容区（上画布 + 下 `h-48` 预览面板）+ 右 `w-72` 输出配置侧栏 |
| 顶部工具栏 | header `h-14`：左侧面包屑；右侧分支选择器（master / feature）+ "保存"按钮 + "提议"按钮 + "打开计划编辑器"链接 + "部署"主按钮 + Build #N 状态徽章（emerald 成功） | Build 状态徽章按成功/失败显示 emerald/rose |
| 画布 | 带网格背景（`grid-pattern`）可滚动画布 + SVG `flow-line` 贝塞尔曲线连接线 + 节点横向排列（`flex items-center justify-center gap-8`） | 节点为 `pipeline-node` 卡片，按颜色区分类型 |
| 节点颜色 | 输入=amber / 变换(Filter)=cyan / 变换(Join)=purple / 输出=emerald | 对应 `badge-*` 色系 |
| 底部预览面板 | 固定高度 `h-48`，标题栏"输出预览 · {dataset_name}" + 行数，下方带 sticky thead 的等宽字体数据表格 | 表格行使用 `table-row-hover` 悬停效果 |
| 右侧配置面板 | 输出数据集名 + 格式选择器（Parquet/Avro/CSV）+ 表格式选择器（Iceberg/Delta）+ 写入模式选择器（SNAPSHOT/APPEND/UPDATE）+ Schema 列表（列名+类型表格）+ 底部"部署并搭建"主按钮 | 选择器使用 `<select>` + `--aos-input-bg` 背景 |
| 节点交互 | 拖拽放置 + 拖拽连线 + 点击选中 → 右侧面板切换为节点配置 | 选中节点 `border-2 border-cyan-400/50` 高亮 |

**前端组件**：改造 `apps/web/src/pages/s2/pipelineCanvas.tsx`（已有骨架，需实现拖拽 + 连线 + 配置面板）

---

### 4.6 Phase 2 集成自测

| 步骤 | 检查项 |
| --- | --- |
| ① 重启 | 后端 + 前端启动无报错 |
| ② 全量测试 | `pytest` + `vitest` 全绿 |
| ③ 页面加载 | `/pipelines/{id}` 画布页 + `/lineage` 血缘页 + `/funnel` 映射页 加载无白屏 |
| ④ 风格一致 | Pipeline 画布对标 `pipeline.html`：三栏式 + 网格背景 + 节点色系 + 底部预览面板 |
| ⑤ 风格一致 | Lineage 图对标 `lineage.html`：三栏式 + 详情侧栏 + SVG 图形区 + 焦点高亮 |
| ⑥ 风格一致 | Funnel 映射对标 `funnel.html`：源 Schema 侧栏 + 映射表格 + Lint 状态 + Constitution 卡片 |
| ⑦ 跨模块链路 | Pipeline Builder 构建 DAG → 预览执行 → Build 引擎执行 → Lineage 图生成 → Funnel 四阶段触发 → Object Store 可查 |

---

## 5. Phase 3 · Ontology 写回闭环

> **W1 项**：W1-3（Funnel 可视化映射编辑器）、W1-6（Action 写回协议）、W1-7（壳核模式）、W1-17（Ontology 角色体系）、W1-18（OMA Function Type 视图）
> **前置条件**：Phase 2 完成（Funnel 四阶段 + Transform 算子 + Function 引擎）
> **本 Phase 构建 L1→L2→L1 闭环——数据经 Funnel 进入 Ontology，Action 写回 L1，Function 在其中承转**
> **状态**：✅ 已完成

### 5.1 W1-6 · Action 写回协议

#### 5.1.1 功能定义

| 子功能 | 说明 |
| --- | --- |
| Write-back Dataset | Action 执行时将变更写入 L1 Write-back Dataset（而非直写底层） |
| 变更类型 | INSERT / UPDATE / DELETE 三种操作 |
| 主键校验 | 写回前校验主键存在性和唯一性 |
| 事务性 | 多行写回在同一事务内，全成功或全回滚 |
| 乐观 UI | 前端先更新状态，后端确认后持久化；失败回滚 |
| 软删除 | 使用 `is_deleted` 标记而非物理删除 |

#### 5.1.2 后端实现

| 文件 | 职责 |
| --- | --- |
| `aos_api/action_writeback.py` | Write-back Dataset 模型 + 变更日志 |
| `aos_api/action_writeback.py` | 主键校验器 |
| `aos_api/action_writeback.py` | 事务管理器（begin / commit / rollback） |
| `aos_api/action_writeback.py` | 软删除处理器 |
| `aos_api/routers/actions.py` | 扩展已有 `POST /v1/actions/{id}/execute` → 支持写回协议 |

#### 5.1.3 单元测试

| 测试文件 | 测试用例 |
| --- | --- |
| `tests/test_action_writeback.py` | `test_writeback_insert` — INSERT 操作写入 Write-back Dataset |
| | `test_writeback_update` — UPDATE 操作更新对应行 |
| | `test_writeback_delete_soft` — DELETE 操作标记 is_deleted |
| | `test_writeback_pk_validation_exists` — 主键存在 → 通过 |
| | `test_writeback_pk_validation_not_found` — 主键不存在 → 拒绝 |
| | `test_writeback_pk_duplicate` — 主键重复 → 拒绝 |
| | `test_writeback_transaction_all_success` — 多行写回全成功 |
| | `test_writeback_transaction_partial_fail_rollback` — 部分失败 → 全回滚 |
| | `test_soft_delete_query_excludes_deleted` — 查询排除 is_deleted=true |

#### 5.1.4 UI 功能设计

**对标 HTML 蓝图页**：`workshop-object-view.html`（Object View + Action Form）中的 Action 执行区域

| UI 区域 | 对标蓝图 | 设计规范 |
| --- | --- | --- |
| Action 执行按钮 | Object 详情页 / Workshop 模块中的 Action 按钮组 | 按钮使用主题色 `--aos-accent` 背景 |
| 执行确认 | 点击 Action → 弹出确认表单（参数填写）→ 提交 | 表单使用 `--aos-card` 背景卡片 |
| 乐观 UI | 提交后立即更新前端状态（无需等待后端响应） | 成功 → 状态保持；失败 → 回滚 + toast 提示 |
| 写回状态 | 底部状态栏显示"写回中..." → "已写回" / "写回失败" | 状态色：进行中=cyan / 成功=emerald / 失败=rose |

---

### 5.2 W1-7 · 壳核模式（Action 调用 Function）

#### 5.2.1 功能定义

| 子功能 | 说明 |
| --- | --- |
| 壳-核架构 | Action（壳）接收用户输入 → 调用 Function（核）执行业务逻辑 → 写回结果 |
| FUNC-SPEC 规范 | Function 定义：输入类型 + 输出类型 + 实现代码 |
| ACT-SPEC 规范 | Action 定义：参数 + Function 引用 + 写回配置 |
| 壳核绑定 | Action Type 配置中指定关联的 Function |
| 执行链路 | Action 执行 → 调用 Function → Function 返回结果 → Action 写回 |

#### 5.2.2 后端实现

| 文件 | 职责 |
| --- | --- |
| `aos_api/shell_core.py` | 壳核绑定模型（Action Type → Function 引用） |
| `aos_api/shell_core.py` | 执行链路编排器（Action → Function → Writeback） |
| `aos_api/action_template_registry.py` | 扩展：支持 Function 引用配置 |

#### 5.2.3 单元测试

| 测试文件 | 测试用例 |
| --- | --- |
| `tests/test_shell_core.py` | `test_action_calls_function` — Action 执行 → Function 被调用 |
| | `test_function_result_writeback` — Function 返回值 → 写回 Write-back Dataset |
| | `test_function_error_propagates` — Function 异常 → Action 返回错误 |
| | `test_shell_core_binding` — Action Type 绑定 Function 配置 |
| | `test_func_spec_validation` — FUNC-SPEC 类型校验 |
| | `test_act_spec_validation` — ACT-SPEC 参数校验 |

#### 5.2.4 UI 功能设计

**对标 HTML 蓝图页**：`ontology-action.html`（Action Type 详情）+ `ontology-function.html`（Function Type 详情）

| UI 区域 | 对标蓝图 | 设计规范 |
| --- | --- | --- |
| Action Type 详情页 | `ontology-action.html` 两栏式 | 左 `w-56` 导航 + 右主内容区 |
| 壳-核链接 | Action 详情页顶部"壳: {function_name} →"链接（violet 边框） | 点击跳转到 Function Type 详情页 |
| Function Type 详情页 | `ontology-function.html` → Overview Tab | 显示函数名 + 输入输出类型 + 代码块 + "壳: {action_name} →"反向链接 |
| 执行链路可视化 | Action 详情页底部显示"Action → Function → Writeback"链路图 | 三节点水平排列 + 箭头连接 |

---

### 5.3 W1-3 · Funnel 可视化映射编辑器

#### 5.3.1 功能定义

| 子功能 | 说明 |
| --- | --- |
| 源 Schema 侧栏 | 显示 L1 数据集的列名列表 |
| 映射表格 | 源列 → Object Property / 类型 / 置信度 |
| 拖拽映射 | 从源 Schema 侧栏拖拽列名到映射表格 |
| 自动映射 | 点击"自动映射"→ 根据列名相似度自动匹配 Object Property |
| Lint 检查 | 检查映射完整性 + 类型匹配 + 主键存在 |
| 发布门控 | Lint 全部通过后才可点击"发布" |
| 行业模板 | 预置行业映射模板（跨境电商 / 环科院 / 沌肽生物） |
| Constitution 卡片 | 底部显示语义契约 / 推理边界 / 伦理护栏三列 |

#### 5.3.2 后端实现

| 文件 | 职责 |
| --- | --- |
| `aos_api/funnel_editor.py` | 映射模型 + 自动映射算法（列名相似度匹配） |
| `aos_api/funnel_editor.py` | Lint 检查器（完整性 + 类型匹配 + 主键） |
| `aos_api/funnel_editor.py` | 行业模板管理 |
| `aos_api/routers/funnel.py` | 扩展：`POST /v1/funnel/auto-map`、`POST /v1/funnel/lint`、`GET /v1/funnel/templates` |

#### 5.3.3 单元测试

| 测试文件 | 测试用例 |
| --- | --- |
| `tests/test_funnel_editor.py` | `test_auto_map_by_name_similarity` — 列名相似度匹配 |
| | `test_auto_map_completeness` — 自动映射后完成度提升 |
| | `test_lint_missing_mapping` — 未映射列 → Lint 警告 |
| | `test_lint_type_mismatch` — 类型不匹配 → Lint 错误 |
| | `test_lint_missing_pk` — 主键未映射 → Lint 错误 |
| | `test_publish_blocked_by_lint` — Lint 未通过 → 发布被阻止 |
| | `test_publish_allowed_after_lint_pass` — Lint 全通过 → 发布成功 |
| | `test_industry_template_switch` — 切换行业模板 → 映射全部替换 |

#### 5.3.4 UI 功能设计（对标需求文档）

**对标 HTML 蓝图页**：`funnel.html`（Funnel 映射编辑器）

> 详细 UI 规范见 §4.3.4（Phase 2 W1-5 Funnel 四阶段管道中的 Funnel UI 描述），此处补充编辑器特有交互。

| UI 区域 | 对标蓝图 | 设计规范 |
| --- | --- | --- |
| 源列拖拽 | 左侧 `w-72` 侧栏中的列名列表可拖拽 | 拖拽时列名卡片半透明 + 鼠标跟随 |
| 映射表放置 | 拖拽到映射表格行 → 自动填充源列 | 放置时行高亮 + 填充动画 |
| 完成度百分比 | 顶部标题栏显示完成度百分比 | 0%=muted / 50-70%=amber / >70%=emerald |
| 三能力标签 | 顶部"行业垂直定制"/"智能属性映射"/"数据质量清洗"标签 | 标签使用 `badge-*` 样式 |
| OKF 清洗规则面板 | amber 边框卡片，列出自动纠错规则 | 每条规则一行：规则名 + 描述 + 启用开关 |
| Constitution 卡片 | 底部三列网格：语义契约 / 推理边界 / 伦理护栏 | 每列卡片 `--aos-card` 背景 + 标题 + 描述 |

---

### 5.4 W1-17 · Ontology 角色体系

#### 5.4.1 功能定义

| 角色 | 权限 |
| --- | --- |
| Owner | 全部权限：编辑元数据 + 编辑数据 + 管理角色 |
| Editor | 编辑元数据 + 编辑数据 |
| Viewer | 查看元数据 + 查看数据 |
| Discoverer | 仅查看元数据（不可查看数据） |

| 子功能 | 说明 |
| --- | --- |
| 角色分配 | Ontology Manager 中为用户/组分配角色 |
| 元数据/数据分离 | 角色权限区分元数据访问和数据访问 |
| 默认角色 | 新用户默认为 Discoverer |
| 角色继承 | 组织级角色 → Ontology 级角色继承 |

#### 5.4.2 后端实现

| 文件 | 职责 |
| --- | --- |
| `aos_api/ontology_roles.py` | 角色模型 + 权限矩阵 |
| `aos_api/ontology_roles.py` | 角色分配 / 撤销 |
| `aos_api/ontology_roles.py` | 权限检查中间件（元数据 vs 数据） |
| `aos_api/routers/ontology.py` | 扩展：`GET /v1/ontology/{id}/roles`、`POST /v1/ontology/{id}/roles` |

#### 5.4.3 单元测试

| 测试文件 | 测试用例 |
| --- | --- |
| `tests/test_ontology_roles.py` | `test_owner_can_edit_metadata` — Owner 编辑元数据 → 通过 |
| | `test_owner_can_edit_data` — Owner 编辑数据 → 通过 |
| | `test_editor_can_edit_metadata` — Editor 编辑元数据 → 通过 |
| | `test_editor_can_edit_data` — Editor 编辑数据 → 通过 |
| | `test_viewer_cannot_edit` — Viewer 编辑 → 拒绝 |
| | `test_viewer_can_view_data` — Viewer 查看数据 → 通过 |
| | `test_discoverer_cannot_view_data` — Discoverer 查看数据 → 拒绝 |
| | `test_discoverer_can_view_metadata` — Discoverer 查看元数据 → 通过 |
| | `test_default_role_discoverer` — 新用户默认 Discoverer |
| | `test_role_inheritance` — 组织级角色继承到 Ontology 级 |

#### 5.4.4 UI 功能设计（对标需求文档）

**对标 HTML 蓝图页**：`ontology.html`（Ontology Manager）+ `ontology-object.html`（Object 详情 → Usage Tab）

| UI 区域 | 对标蓝图 | 设计规范 |
| --- | --- | --- |
| Ontology Manager 搜索栏 | `ontology.html` header 右侧搜索框 `w-72`（带搜索图标，placeholder "搜索 Object / Link / Action…"） | 搜索框使用 `--aos-input-bg` 背景 |
| Object 详情 Tab 栏 | `ontology-object.html` 7 个可滚动 Tab（Overview / Properties / Action types / Link type graph / Dependents / Data / Usage） | Tab 栏 `overflow-x-auto`；激活 Tab `border-b-2` 主题色 |
| Usage Tab | 三列统计卡片：读 / 写 / 活跃用户（30 天） | 每卡片显示数值 + 标签 + 趋势指示 |
| 角色管理入口 | Object 详情页或 Ontology Manager 中新增"角色"入口 | 角色列表表格 + 分配按钮 |
| 角色徽章 | Object 卡片显示角色徽章（Owner=violet / Editor=cyan / Viewer=muted / Discoverer=faint） | 徽章使用 `badge-*` 样式 |

---

### 5.5 W1-18 · OMA Function Type 视图

#### 5.5.1 功能定义

| 子功能 | 说明 |
| --- | --- |
| Function 概览 | 函数名 + 输入输出类型 + 场景描述 + 代码实现 |
| Configuration | 运行时 / 沙箱 / 超时限制 |
| Type Safety | 编译结果（成功/失败）+ 价值说明 |
| Usage History | 调用统计表格（日期 / 调用次数 / 调用方 / P99 延迟） |
| 代码跳转 | "打开 Code Repository" 链接 |

#### 5.5.2 后端实现

| 文件 | 职责 |
| --- | --- |
| `aos_api/function_registry.py` | Function 注册表 + 元数据管理 |
| `aos_api/function_registry.py` | Usage History 收集器 |
| `aos_api/routers/functions.py` | 扩展：`GET /v1/functions/{id}`（详情）、`GET /v1/functions/{id}/usage`（使用历史） |

#### 5.5.3 单元测试

| 测试文件 | 测试用例 |
| --- | --- |
| `tests/test_function_registry.py` | `test_register_function` — 注册新 Function |
| | `test_get_function_detail` — 获取 Function 详情 |
| | `test_get_function_usage` — 获取使用历史 |
| | `test_function_list` — 列出所有 Function |
| | `test_function_usage_aggregation` — 使用历史按日聚合 |

#### 5.5.4 UI 功能设计（对标需求文档）

**对标 HTML 蓝图页**：`ontology-function.html`（Function Type 视图）

> 详细 UI 规范见 §3.1.4（Phase 1 W1-1 Function 引擎中的 UI 描述），此处补充 OMA 集成部分。

| UI 区域 | 对标蓝图 | 设计规范 |
| --- | --- | --- |
| Ontology Manager 入口 | `ontology.html` 收藏区卡片中新增 Function Type 入口 | 卡片显示函数名 + 输入输出类型摘要 |
| Object 详情页链接 | `ontology-object.html` Overview Tab 中"Action types"卡片旁新增"Function Types"卡片 | 卡片编号 + 函数列表 + 跳转链接 |
| 壳-核双向链接 | Function Type 详情页"壳: {action_name} →"链接 → Action Type 详情页 | violet 边框链接按钮 |

---

### 5.6 Phase 3 集成自测

| 步骤 | 检查项 |
| --- | --- |
| ① 重启 | 后端 + 前端启动无报错 |
| ② 全量测试 | `pytest` + `vitest` 全绿 |
| ③ 页面加载 | Funnel 编辑器页 + Ontology Manager 页 + Function Type 页 + Action Type 页 加载无白屏 |
| ④ 风格一致 | Funnel 编辑器对标 `funnel.html`：三栏式 + 源 Schema + 映射表 + Lint + Constitution |
| ⑤ 风格一致 | Ontology Manager 对标 `ontology.html`：搜索栏 + 收藏区 + 最近区 + 重要修改表 |
| ⑥ 风格一致 | Function Type 对标 `ontology-function.html`：四 Tab + Overview 代码块 + Type Safety |
| ⑦ 跨模块链路 | L1 数据 → Funnel 映射 → 四阶段管道 → Object Store → Action 执行 → Function 调用 → Write-back Dataset → Funnel Changelog → 闭环 |

---

## 6. Phase 4 · AIP 智能层

> **W1 项**：W1-2（Logic 编排真接入）、W1-12（Evals 评测集）
> **前置条件**：Phase 3 完成（Function 引擎 + Action 写回 + 壳核模式）
> **本 Phase 构建 LLM 编排与质量控制能力——Logic 编排器调用 Function/Action/LLM，Evals 门控保障质量**
> **状态**：✅ 已完成 · LLM Gateway 已就绪（Agnes OpenAI 兼容），UseLLM Block + Evals LLM 评判均已实连验证。

### 6.1 W1-2 · Logic 编排真接入

#### 6.1.1 功能定义

| 子功能 | 说明 |
| --- | --- |
| Block 类型 | Input / CreateVariable / GetProperty / UseLLM / Transform / ApplyAction / Execute |
| 三栏 UI | 左编排栏（块链）+ 中调试器（CoT/提议预览）+ 右运行面板（入参+运行+历史） |
| 工具集注册 | Query / Function / Action / Capability / Wiki 五类工具注册到 Logic |
| Ontology 写回四步 | UseLLM → 发布 → Action → Workshop |
| Edits 合并策略 | 字段级 / LastWriteWins / 人工仲裁 |
| Prompt 工程 | 变量注入 + Few-shot + 版本管理 |
| 调试器 | CoT 思维链显示 + 提议 edits 预览（不落库） |
| Automate 集成 | 条件触发 + 提案 |

#### 6.1.2 后端实现

| 文件 | 职责 |
| --- | --- |
| `aos_api/logic_engine.py` | Block 模型 + 执行器（按顺序执行 Block 链） |
| `aos_api/logic_engine.py` | UseLLM Block → 调用 llm_gateway |
| `aos_api/logic_engine.py` | ApplyAction Block → 调用 action_writeback |
| `aos_api/logic_engine.py` | 调试器数据收集（CoT + 提议 edits） |
| `aos_api/logic_engine.py` | Edits 合并策略 |
| `aos_api/routers/logic.py` | API 端点：`POST /v1/logic/run`（执行）、`POST /v1/logic/debug`（调试运行）、`GET /v1/logic/blocks`（Block 类型目录） |

#### 6.1.3 单元测试

| 测试文件 | 测试用例 |
| --- | --- |
| `tests/test_logic_engine.py` | `test_block_input` — Input Block 接收入参 |
| | `test_block_create_variable` — CreateVariable Block 创建变量 |
| | `test_block_get_property` — GetProperty Block 获取对象属性 |
| | `test_block_use_llm` — UseLLM Block 调用 LLM → 返回结果 |
| | `test_block_transform` — Transform Block 调用 Function 引擎 |
| | `test_block_apply_action` — ApplyAction Block 调用 Action 写回 |
| | `test_block_chain_sequential` — 多 Block 顺序执行 |
| | `test_debug_cot_collection` — 调试模式收集 CoT |
| | `test_debug_proposed_edits` — 调试模式收集提议 edits（不落库） |
| | `test_edits_merge_last_write_wins` — LastWriteWins 合并 |
| | `test_edits_merge_field_level` — 字段级合并 |
| | `test_prompt_variable_injection` — Prompt 变量注入 |
| | `test_prompt_few_shot` — Few-shot 示例注入 |
| | `test_ontology_writeback_four_steps` — UseLLM → 发布 → Action → Workshop 链路 |

#### 6.1.4 UI 功能设计（对标需求文档）

**对标 HTML 蓝图页**：`aip-logic.html`（AIP Logic 三栏编辑器）

| UI 区域 | 对标蓝图 | 设计规范 |
| --- | --- | --- |
| 页面布局 | `aip-logic.html` 左 `w-56` 导航 + 右主区域（header → Tab 栏 → 块工具条 → 三栏 grid → 底部状态栏） | 三栏使用 `lg:grid-cols-12`，每栏 `lg:col-span-4` |
| 顶部工具栏 | header：左侧面包屑；右侧模型路由选择器（k-LLM / 私有-小模 / 高能力审批）+ Eval 按钮 + 发布按钮（amber 主色） | 发布按钮 amber(`rgb(245 158 11)`) |
| Tab 栏 | 三个 Tab：编排 / 自动化 Uses / 运行历史 | `data-tab` 切换 |
| 块工具条 | chip 形式列出可添加 Block 类型：+ Create Variable / + Get Attributes / + Use LLM（amber 高亮）/ + Transform / + Apply Action / + Execute | chip 样式：`badge-*` + `cursor-pointer` + hover 效果 |
| ① 编排栏（左） | 带网格背景的垂直块流，从上到下用 `↓` 箭头连接各 `pipeline-node` 块卡片 | Use LLM 块高亮显示 prompt 文本和 Tools 标签；Apply Action 块含"→ Draft 审批台"链接 |
| ② 调试器（中） | 深色背景面板，初始空状态"运行后显示思维链"；运行后显示 CoT + 工具请求 + 提议 edits | 深色背景使用 `--aos-elevated` |
| ③ 运行面板（右） | 入参选择器 + 运行按钮（amber 主色）+ 最近运行历史列表（成功/失败状态）+ 自动化创建区块（amber 边框） | 运行历史项显示状态色（emerald/rose） |
| 底部状态栏 | 发布状态 + 执行范围（用户/项目）+ 试跑 edits 不落库提示 | 状态栏 `--aos-aside` 背景 |

**前端组件**：改造 `apps/web/src/pages/LogicPage.tsx`（已有骨架，需实现三栏 + Block 链 + 调试器）

---

### 6.2 W1-12 · Evals 评测集

#### 6.2.1 功能定义

| 子功能 | 说明 |
| --- | --- |
| 评测集模型 | 评测集 = 一组测试用例（输入 + 期望输出 + 评判标准） |
| 评测执行 | 对 Logic / Function 执行评测集 → 生成评测报告 |
| 门控机制 | 评测通过率 ≥ 阈值 → 允许发布；否则阻止发布 |
| 评判标准 | 精确匹配 / 包含匹配 / LLM 评判 / 数值容差 |
| 评测报告 | 通过率 + 失败用例详情 + 历史 Trend |

#### 6.2.2 后端实现

| 文件 | 职责 |
| --- | --- |
| `aos_api/evals_engine.py` | 评测集模型 + 测试用例模型 |
| `aos_api/evals_engine.py` | 评测执行器（批量执行 + 结果收集） |
| `aos_api/evals_engine.py` | 评判器（精确/包含/LLM/容差） |
| `aos_api/evals_engine.py` | 门控检查器（通过率 ≥ 阈值） |
| `aos_api/routers/evals.py` | API 端点：`POST /v1/evals/run`（执行评测）、`GET /v1/evals/{id}/report`（报告）、`POST /v1/evals/gate-check`（门控检查） |

#### 6.2.3 单元测试

| 测试文件 | 测试用例 |
| --- | --- |
| `tests/test_evals_engine.py` | `test_eval_exact_match_pass` — 精确匹配通过 |
| | `test_eval_exact_match_fail` — 精确匹配失败 |
| | `test_eval_contains_match` — 包含匹配 |
| | `test_eval_llm_judge` — LLM 评判 |
| | `test_eval_numeric_tolerance` — 数值容差 |
| | `test_eval_pass_rate_calculation` — 通过率计算 |
| | `test_gate_check_pass` — 通过率 ≥ 阈值 → 允许发布 |
| | `test_gate_check_fail` — 通过率 < 阈值 → 阻止发布 |
| | `test_eval_report_generation` — 评测报告生成 |
| | `test_eval_history_trend` — 历史 Trend 计算 |

#### 6.2.4 UI 功能设计（对标需求文档）

**对标 HTML 蓝图页**：`aip-evals.html`（Evals 门控）

| UI 区域 | 对标蓝图 | 设计规范 |
| --- | --- | --- |
| 评测集列表 | 评测集卡片列表，每卡片显示名称 + 用例数 + 最近通过率 + 状态徽章 | 通过率 ≥80%=emerald / 60-80%=amber / <60%=rose |
| 评测执行 | "运行评测"按钮 → 执行中进度条 → 完成后显示报告 | 进度条使用 `--aos-accent` 色 |
| 评测报告 | 通过率大数字 + 失败用例详情列表 + 历史 Trend 折线图 | 大数字使用主题色 + 等宽字体 |
| 门控状态 | 发布按钮旁显示门控状态徽章（"门控通过"/"门控未通过"） | 通过=emerald / 未通过=rose |
| Logic 编辑器集成 | Logic 发布前自动触发门控检查 → 未通过则发布按钮 disabled | disabled 按钮 muted 色 + tooltip 说明 |

---

### 6.3 Phase 4 集成自测

| 步骤 | 检查项 |
| --- | --- |
| ① 重启 | 后端 + 前端启动无报错 |
| ② 全量测试 | `pytest` + `vitest` 全绿 |
| ③ 页面加载 | `/logic` 三栏编排页 + `/evals` 评测页 加载无白屏 |
| ④ 风格一致 | Logic 三栏对标 `aip-logic.html`：三栏 grid + 块工具条 + 编排链 + 调试器 + 运行面板 |
| ⑤ 风格一致 | Evals 对标 `aip-evals.html`：评测集列表 + 报告 + 门控状态 |
| ⑥ 跨模块链路 | Logic 编排 → UseLLM Block 调 LLM → Transform Block 调 Function → ApplyAction Block 写回 → Evals 门控检查 → 发布 |

---

## 7. Phase 5 · 非结构化数据与数据集

> **W1 项**：W1-9（MediaReference 桥接）、W1-15（Dataset Preview SQL 控制台）、W1-16（MediaSet 类型化 + 表格行变换）
> **前置条件**：Phase 1 完成（Build 引擎 + Function 引擎）
> **本 Phase 可与 Phase 2 并行推进，不依赖 Funnel/Transform**
> **状态**：✅ 已完成

### 7.1 W1-9 · MediaReference 桥接

#### 7.1.1 功能定义

| 子功能 | 说明 |
| --- | --- |
| MediaReference 类型 | Dataset 列中的 MediaReference 指针 → 指向 MediaSet 中的文件 |
| 桥接查询 | 从 Dataset 行的 MediaReference → 获取 MediaSet 中的文件元数据 + 内容 |
| Pipeline 集成 | Transform 算子可读取 MediaReference → 获取文件内容 → 处理 |

#### 7.1.2 后端实现

| 文件 | 职责 |
| --- | --- |
| `aos_api/media_reference.py` | MediaReference 模型 + 桥接查询 |
| `aos_api/media_reference.py` | MediaSet 内容获取器 |

#### 7.1.3 单元测试

| 测试文件 | 测试用例 |
| --- | --- |
| `tests/test_media_reference.py` | `test_media_reference_create` — 创建 MediaReference 指针 |
| | `test_media_reference_resolve` — 从 MediaReference 获取文件元数据 |
| | `test_media_reference_get_content` — 从 MediaReference 获取文件内容 |
| | `test_media_reference_in_dataset` — Dataset 列包含 MediaReference |
| | `test_media_reference_pipeline_transform` — Transform 算子读取 MediaReference |

---

### 7.2 W1-15 · Dataset Preview SQL 控制台

#### 7.2.1 功能定义

| 子功能 | 说明 |
| --- | --- |
| SQL 查询 | 在 Dataset Preview 页面执行 SQL 查询 |
| 自动补全 | 列名自动补全 |
| 查询历史 | 保存最近查询 |
| 结果展示 | 表格形式展示查询结果 |
| 安全限制 | 只读查询（SELECT only）；行数限制 |

#### 7.2.2 后端实现

| 文件 | 职责 |
| --- | --- |
| `aos_api/sql_console.py` | SQL 解析器（白名单 SELECT）+ 执行器（基于 sqlite3 / pandas） |
| `aos_api/sql_console.py` | 自动补全数据源（列名列表） |
| `aos_api/routers/datasets.py` | 扩展：`POST /v1/datasets/{id}/sql`（执行 SQL） |

#### 7.2.3 单元测试

| 测试文件 | 测试用例 |
| --- | --- |
| `tests/test_sql_console.py` | `test_select_all` — `SELECT * FROM dataset` → 全部行 |
| | `test_select_columns` — `SELECT col1, col2 FROM dataset` → 指定列 |
| | `test_where_clause` — `SELECT * FROM dataset WHERE col > 100` → 过滤 |
| | `test_order_by` — `SELECT * FROM dataset ORDER BY col DESC` → 排序 |
| | `test_limit` — `SELECT * FROM dataset LIMIT 10` → 行数限制 |
| | `test_reject_non_select` — `DELETE FROM dataset` → 拒绝 |
| | `test_reject_drop` — `DROP TABLE dataset` → 拒绝 |
| | `test_column_autocomplete` — 列名自动补全列表 |
| | `test_query_history` — 查询历史保存 |

#### 7.2.4 UI 功能设计（对标需求文档）

**对标 HTML 蓝图页**：`dataset.html`（数据集预览）

| UI 区域 | 对标蓝图 | 设计规范 |
| --- | --- | --- |
| 页面布局 | `dataset.html` 两栏式 | 左 `w-56` 导航 + 右主内容区（header → Tab 栏 → 滚动面板） |
| Tab 栏 | 四个 Tab：预览（默认，cyan 下划线）/ 历史 / 详情 / 健康 | `data-tab` 切换 |
| 预览面板 | 顶部数据集标题 + 区域徽章（精修区 emerald / 原始区 amber）+ 路径 + 四列统计卡片网格（行数/大小/最新快照/上次更新）+ 数据表格 | 表格 sticky thead + `table-row-hover` |
| SQL 控制台 | 预览 Tab 内新增 SQL 编辑器区域：代码编辑框 + "执行"按钮 + 结果表格 | 编辑框使用 `code-block` 样式 + 等宽字体 |
| 动态切换 | URL 参数 `?raw=1` / `?curated=0` / `?maintenance=1` 切换数据 | maintenance 模式额外显示 `media_ref` 列 |

---

### 7.3 W1-16 · MediaSet 类型化 + 表格行变换

#### 7.3.1 功能定义

| 子功能 | 说明 |
| --- | --- |
| 媒体类型 | 文档 / 电子表格 / 音频 / 图像 / DICOM |
| 类型化创建 | 创建 MediaSet 时选择媒体类型 → 类型特定配置 |
| 内容查看 | 文件列表 + 在线预览（文档/图片/PDF） |
| 表格行变换 | "将媒体集转换为表格行"内置变换 → Pipeline Builder 集成 |
| OCR 预览 | 文档类 MediaSet → OCR 文本预览 |

#### 7.3.2 后端实现

| 文件 | 职责 |
| --- | --- |
| `aos_api/media_meta.py` | 扩展：媒体类型模型 + 类型化创建 |
| `aos_api/media_transform.py` | 表格行变换算子（MediaSet → Dataset 行） |
| `aos_api/routers/media.py` | API 端点：`POST /v1/media-sets`（类型化创建）、`GET /v1/media-sets/{id}/files`（文件列表）、`POST /v1/media-sets/{id}/transform-rows`（表格行变换） |

#### 7.3.3 单元测试

| 测试文件 | 测试用例 |
| --- | --- |
| `tests/test_media_typed.py` | `test_create_document_media_set` — 创建文档类型 MediaSet |
| | `test_create_audio_media_set` — 创建音频类型 MediaSet |
| | `test_create_dicom_media_set` — 创建 DICOM 类型 MediaSet |
| | `test_media_type_not_changeable` — 创建后类型不可改 |
| | `test_list_files` — 文件列表 |
| | `test_preview_document` — 文档在线预览 |
| `tests/test_media_transform.py` | `test_transform_to_rows` — MediaSet → 表格行变换 |
| | `test_transform_with_ocr` — OCR 文本提取后变换 |
| | `test_transform_in_pipeline` — Pipeline Builder 中使用变换 |

#### 7.3.4 UI 功能设计（对标需求文档）

**对标 HTML 蓝图页**：`media-sets.html`（MediaSet 浏览器）

| UI 区域 | 对标蓝图 | 设计规范 |
| --- | --- | --- |
| 页面布局 | `media-sets.html` 左 `w-56` 导航 + 右主区域（header → Tab 栏 → 面板区） | 浏览 Tab 内部两栏：左 `w-72` 文件列表 + 右预览区 |
| Tab 栏 | 四个 Tab：浏览（默认，cyan）/ 同步 / 变换 / 设置 | `data-tab` 切换 |
| 浏览面板（两栏） | 左侧：媒体类型选择器（文档/电子表格）+ `badge-media-doc` 标签 + 搜索框 + 文件 `<ul>` 列表（PDF 图标 + 文件名，选中项 purple 高亮）+ 底部文件总数和大小 | 右侧：文件名/路径/大小/页数 + "获取媒体引用"和"OCR 预览"按钮 + 3:4 比例预览卡片 |
| 同步 Tab | 同步配置卡片（数据源/源路径/目标/写入模式）+ 运行历史表格 + "立即运行"按钮 | 卡片 `--aos-card` 背景 |
| 变换 Tab | 四列卡片网格（提取文本原始/OCR/页面渲染/获取媒体引用），每卡片含计算成本说明和跳转链接 | 卡片 `--aos-card` 背景 + 标题 + 描述 + 链接 |
| 设置 Tab | 媒体类型选择器（创建后不可改，amber 警告）+ 保留策略 + 存储策略（单选按钮） | amber 警告使用 `rgb(245 158 11)` |

---

### 7.4 Phase 5 集成自测

| 步骤 | 检查项 |
| --- | --- |
| ① 重启 | 后端 + 前端启动无报错 |
| ② 全量测试 | `pytest` + `vitest` 全绿 |
| ③ 页面加载 | `/datasets/{id}` SQL 控制台 + `/media-sets/{id}` 浏览器 加载无白屏 |
| ④ 风格一致 | Dataset Preview 对标 `dataset.html`：四 Tab + 统计卡片 + 数据表格 + SQL 编辑器 |
| ⑤ 风格一致 | MediaSet 对标 `media-sets.html`：四 Tab + 两栏浏览 + 变换卡片网格 |
| ⑥ 跨模块链路 | MediaSet 创建 → 文件上传 → 表格行变换 → Pipeline Builder 中使用 → Dataset 中 MediaReference 列可链接回 MediaSet |

---

## 8. Phase 6 · 集成优化与收尾

> **W1 项**：W1-11（Pipeline 重试机制）
> **前置条件**：Phase 2–5 完成
> **本 Phase 补齐稳定性机制并做全链路验收**
> **状态**：✅ 已完成

### 8.1 W1-11 · Pipeline 重试机制

#### 8.1.1 功能定义

| 子功能 | 说明 |
| --- | --- |
| 自动重试 | Build Job 失败后自动重试（默认 3 次） |
| 退避策略 | 指数退避（1s / 2s / 4s） |
| 重试限制 | 超过最大重试次数 → 标记为 FAILED |
| 手动重试 | 用户可在 UI 手动触发重试 |
| 死信队列 | 超过重试次数的 Job → 进入 DLQ |

#### 8.1.2 后端实现

| 文件 | 职责 |
| --- | --- |
| `aos_api/jobs/retry.py` | 重试策略 + 退避计算 |
| `aos_api/jobs/retry.py` | DLQ 管理 |
| `aos_api/jobs/build_engine.py` | 扩展：失败后触发重试 |

#### 8.1.3 单元测试

| 测试文件 | 测试用例 |
| --- | --- |
| `tests/test_job_retry.py` | `test_auto_retry_on_failure` — Job 失败 → 自动重试 |
| | `test_exponential_backoff` — 退避时间 1s/2s/4s |
| | `test_max_retry_exceeded` — 超过最大次数 → FAILED |
| | `test_manual_retry` — 用户手动触发重试 |
| | `test_dlq_on_max_retry` — 超过重试 → 进入 DLQ |
| | `test_retry_success_within_limit` — 重试内成功 → SUCCEEDED |
| | `test_dlq_visible_in_lineage` — DLQ 计数在 Lineage 页面可见 |

#### 8.1.4 UI 功能设计

**对标 HTML 蓝图页**：`builds.html`（Build 列表）+ `lineage.html`（DLQ 徽章）

| UI 区域 | 对标蓝图 | 设计规范 |
| --- | --- | --- |
| Build 列表重试标识 | 构建卡片显示重试次数（如"重试 2/3"） | amber 色 `badge-*` |
| DLQ 徽章 | Lineage 页面顶部工具栏显示"DLQ 死信 N"（rose 色） | N>0 时显示，=0 时隐藏 |
| 手动重试按钮 | Build 详情页失败状态时显示"重试"按钮 | 按钮 rose 边框 + hover 效果 |

---

### 8.2 全链路验收

| 验收项 | 验证方法 |
| --- | --- |
| L1→L2 数据流 | Source → Connection → Pipeline Builder DAG → Build 引擎 → Transform → Funnel 四阶段 → Object Store |
| L2→L1 写回 | Object Explorer → Action 执行 → Function 调用 → Write-back Dataset → Funnel Changelog → 闭环 |
| AIP 编排 | Logic 三栏 → UseLLM → Transform → ApplyAction → Evals 门控 → 发布 |
| 非结构化 | MediaSet 创建 → 文件上传 → 表格行变换 → Pipeline 集成 → MediaReference 列 |
| 血缘追踪 | Dataset → Lineage DAG → 展开/折叠 → 列级血缘 → 节点搜索 |
| 稳定性 | Build 失败 → 自动重试 → DLQ → Lineage DLQ 徽章 |
| UI 风格 | 全页面逐一对标 `foundry/html/` 蓝图页，布局/配色/交互模式一致 |

---

## 9. UI 功能设计对标总表

> 以下汇总各 Phase 新增/改造页面与 Foundry HTML 蓝图页的对应关系，作为 UI 验收清单。

### 9.1 页面对标清单

| Phase | 页面 | 前端路由 | 对标 HTML 蓝图页 | 关键 UI 对标点 |
| --- | --- | --- | --- | --- |
| 1 | Build 引擎任务列表 | `/builds` | `builds.html` | 两栏式：左构建历史 + 右任务图/日志；状态色 emerald/rose |
| 1 | Function Type 视图 | `/ontology/function/{id}` | `ontology-function.html` | 四 Tab（Overview/Configuration/Type Safety/Usage History）；代码块；壳-核链接 |
| 2 | Pipeline Builder 画布 | `/pipelines/{id}` | `pipeline.html` | 三栏式：画布+预览+配置侧栏；节点色系 amber/cyan/purple/emerald；SVG 连线 |
| 2 | Data Lineage 图 | `/lineage` | `lineage.html` | 三栏式：详情侧栏+图形区；焦点高亮；DLQ 徽章 |
| 2 | Funnel 映射编辑器 | `/funnel/{id}` | `funnel.html` | 三栏式：源 Schema+映射区；完成度百分比；Lint 门控；Constitution 卡片 |
| 3 | Action Type 详情 | `/ontology/action/{id}` | `ontology-action.html` | 壳-核链接；执行链路图 |
| 3 | Ontology Manager | `/ontology` | `ontology.html` | 搜索栏+收藏区+最近区+重要修改表；OKF 映射按钮 |
| 3 | Object 详情 | `/ontology/object/{type}` | `ontology-object.html` | 7 Tab 可滚动；角色徽章；Metadata 卡片 |
| 4 | AIP Logic 三栏 | `/logic` | `aip-logic.html` | 三栏 grid；块工具条；编排链+调试器+运行面板 |
| 4 | Evals 门控 | `/evals` | `aip-evals.html` | 评测集列表+报告+门控状态 |
| 5 | Dataset Preview | `/datasets/{id}` | `dataset.html` | 四 Tab；统计卡片；SQL 控制台；数据表格 |
| 5 | MediaSet 浏览器 | `/media-sets/{id}` | `media-sets.html` | 四 Tab；两栏浏览；变换卡片网格 |

### 9.2 设计令牌一致性要求

| 令牌 | 暗色主题值 | 亮色主题值 | 用途 |
| --- | --- | --- | --- |
| `--aos-bg` | `#020617` | `#f1f5f9` | 页面背景 |
| `--aos-aside` | `rgba(15,23,42,0.92)` | `#ffffff` | 侧栏背景 |
| `--aos-card` | `rgba(15,23,42,0.72)` | `#ffffff` | 卡片背景 |
| `--aos-border` | `rgba(255,255,255,0.08)` | `rgba(15,23,42,0.1)` | 边框 |
| `--aos-text` | `#f3f4f6` | `#0f172a` | 主文本 |
| `--aos-muted` | `#9ca3af` | `#475569` | 次要文本 |
| `--aos-accent` | `rgb(34 211 238)` | `rgb(8 145 178)` | 主题强调色 |

### 9.3 状态色规范

| 状态 | 色值 | RGB | 用途 |
| --- | --- | --- | --- |
| 成功/Indexed | emerald | `rgb(16 185 129)` | Build 成功 / 索引完成 / 门控通过 |
| 失败/FAILED | rose | `rgb(244 63 94)` | Build 失败 / 门控未通过 / DLQ |
| 运行中/RUNNING | cyan | `rgb(34 211 238)` | 正在执行 / 活跃路径 |
| 警告/Lint | amber | `rgb(245 158 11)` | 输入节点 / Lint 警告 / 重试中 |
| 变换/Join | purple | `rgb(168 85 247)` | Join 算子 / 变换节点 |
| 信息/链接 | violet | `rgb(139 92 246)` | 壳-核链接 / violet 边框按钮 |

### 9.4 通用 UI 模式规范

| 模式 | 规范 | 对标来源 |
| --- | --- | --- |
| 全局导航 | 左侧 `w-56` 固定侧栏，含品牌标识 + 导航项 + 用户区 | 所有 HTML 蓝图页统一 |
| 顶部工具栏 | `h-14` header，左侧面包屑，右侧操作按钮区 | 所有 HTML 蓝图页统一 |
| Tab 切换 | `data-tab` / `data-tab-panel` 属性 + 激活 Tab `border-b-2` 主题色下划线 | `ontology-function.html` / `dataset.html` |
| 卡片 | `--aos-card` 背景 + `--aos-border` 边框 + `--aos-shadow` 阴影 | 所有 HTML 蓝图页 |
| 数据表格 | sticky thead + `table-row-hover` 悬停 + 等宽字体行 | `pipeline.html` / `dataset.html` |
| 代码块 | `code-block` 样式 + `code-cm` / `code-fn` / `code-str` 语法高亮 | `ontology-function.html` / `builds.html` |
| 状态徽章 | `badge-*` 类 + 对应状态色 + 圆角 | 所有 HTML 蓝图页 |
| 节点画布 | `grid-pattern` 网格背景 + SVG `flow-line` 贝塞尔曲线 + 绝对定位节点卡片 | `pipeline.html` / `lineage.html` |
| 搜索框 | `w-72` 宽度 + 搜索图标 + `--aos-input-bg` 背景 | `ontology.html` |
| 分支选择器 | 下拉框 + "分支: {name} ▾" 格式 | `ontology-object.html` / `pipeline.html` |

---

## 10. 依赖关系矩阵

| W1 项 | 直接依赖 | 被依赖（下游） |
| --- | --- | --- |
| W1-1 Function 引擎 | Phase 0 | W1-2, W1-7, W1-8, W1-10, W1-14, W1-18 |
| W1-4 Build 引擎 | Phase 0 | W1-5, W1-8, W1-11, W1-13, W1-14 |
| W1-10 Function 沙箱 | W1-1 | W1-2, W1-7 |
| W1-5 Funnel 四阶段 | W1-4 | W1-3, W1-6 |
| W1-8 Transform 算子 | W1-1, W1-4 | W1-14 |
| W1-13 Data Lineage | W1-4 | — |
| W1-14 Pipeline Builder | W1-8 | — |
| W1-6 Action 写回 | W1-5 | W1-7 |
| W1-7 壳核模式 | W1-1, W1-6 | W1-2 |
| W1-3 Funnel 编辑器 | W1-5 | — |
| W1-17 Ontology 角色 | Phase 0 | — |
| W1-18 Function Type 视图 | W1-1 | — |
| W1-2 Logic 编排 | W1-1, W1-7, W1-10 | W1-12 |
| W1-12 Evals | W1-2 | — |
| W1-9 MediaReference | W1-1 | W1-16 |
| W1-15 SQL 控制台 | Phase 0 | — |
| W1-16 MediaSet 类型化 | W1-9 | — |
| W1-11 Pipeline 重试 | W1-4 | — |

### 10.1 依赖拓扑图

```
Phase 0 (基础设施)
  │
  ├─→ W1-1 (Function 引擎) ──→ W1-10 (沙箱) ──┐
  │     │                                      │
  │     ├─→ W1-8 (Transform) ──→ W1-14 (Pipeline Builder)
  │     │                                      │
  │     ├─→ W1-18 (Function Type 视图)
  │     │
  │     └─→ W1-9 (MediaReference) ──→ W1-16 (MediaSet 类型化)
  │
  ├─→ W1-4 (Build 引擎) ──→ W1-5 (Funnel 四阶段) ──→ W1-3 (Funnel 编辑器)
  │     │                        │
  │     │                        └─→ W1-6 (Action 写回) ──→ W1-7 (壳核模式) ──→ W1-2 (Logic) ──→ W1-12 (Evals)
  │     │
  │     ├─→ W1-13 (Data Lineage)
  │     │
  │     └─→ W1-11 (Pipeline 重试)
  │
  ├─→ W1-17 (Ontology 角色)
  │
  └─→ W1-15 (SQL 控制台)
```

---

## 11. 风险与缓解

| 风险 | 影响 | 缓解措施 |
| --- | --- | --- |
| Function 沙箱安全逃逸 | 恶意代码执行 | 使用 RestrictedPython + 资源限制 + 白名单模块；单元测试覆盖安全边界 |
| Build 引擎事务死锁 | 数据集锁定不可释放 | 设置锁超时 + 死锁检测 + 自动释放 |
| Funnel 四阶段数据丢失 | L1→L2 数据不一致 | 每阶段持久化中间状态 + 幂等重跑 + 单元测试覆盖并发场景 |
| Logic 编排 LLM 超时 | 用户体验卡顿 | LLM 调用超时控制 + 降级策略 + 调试器异步收集 |
| Pipeline Builder DAG 复杂度 | 前端性能下降 | 节点数 >50 时虚拟化渲染 + 增量更新 |
| UI 风格偏离蓝图 | 用户体验不一致 | 每波次集成自测强制对标 HTML 蓝图页 + 截图归档 |

---

## 13. 开发规范（微观方案先行）

> **来源**：2026-07-22 执行策略讨论结论。本节是 §0「总则与开发纪律」的延伸，规定 **每个 W1 项开工前必须补齐微观实现方案**，否则不得编码。

---

### 13.1 不得直接开干的三种模式

| 模式 | 风险 | 是否允许 |
| --- | --- | --- |
| ❌ 全部 W1 方案写完再编码 | 方案脱离实际，编码时推翻重来，浪费大 | 禁止 |
| ❌ 不写方案直接开干 | 违反"先方案再编码"Rule；且本计划是宏观方案不是实现方案 | 禁止 |
| ✅ **每个 W1 项小循环**（方案→开发→测试→下一项） | 符合敏捷，符合"先方案再编码"Rule | **强制采用** |

---

### 13.2 宏观方案（本计划）vs 微观实现方案（开工前必补）

本计划（220plan）对每个 W1 项已给出**宏观层**定义，但缺**微观层**实现方案。开工前必须补齐下表右列。

| 已有（宏观层 · 本计划 §2–§8） | 还缺（微观层 · 开工前必补） |
| --- | --- |
| ✅ 功能定义（子功能清单） | ❌ 每个 `.py` 文件的**类设计 / 函数签名 / 数据结构** |
| ✅ 后端文件职责表 | ❌ Pydantic **模型字段定义**（字段名/类型/约束） |
| ✅ 单元测试用例名 | ❌ API 端点的**请求/响应 Schema**（OpenAPI 片段） |
| ✅ UI 对标蓝图 + 设计规范 | ❌ 算法/状态机的**伪代码或流程图** |
| ✅ Phase 间依赖关系 | ❌ 该 W1 项与已上线代码的**接缝点**（改哪个文件、加哪个路由） |

→ **本计划回答"做什么"，微观实现方案回答"怎么写"。**

---

### 13.3 每个 W1 项的滚动执行循环

```
┌─ 开工前（半天）写微观方案 ──────────────────────────┐
│  1. 在 docs/palantier/20_tech/ 新建该 W1 项的         │
│     微观实现方案 md（命名：220tech_「方案名」.md）     │
│  2. 内容必须包含 5 节：                               │
│     ① 数据模型（Pydantic Schema 字段表）              │
│     ② API 契约（OpenAPI 片段 / 路由签名）             │
│     ③ 核心类/函数设计（类图 / 函数签名 / 伪代码）     │
│     ④ 与现有代码接缝点（改哪个文件 / 加哪个 router）   │
│  3. 把本计划里该 W1 的单元测试用例名扩成具体断言       │
└──────────────────────────────────────────────────────┘
          ↓ 方案 review（自检：能不能照着写代码？）
┌─ 开发（1-3 天）─────────────────────────────────────┐
│  4. 按微观方案写后端代码 + 前端组件                   │
│  5. 每写完一个子功能立即写单元测试（§0.3 测试纪律）    │
└──────────────────────────────────────────────────────┘
          ↓
┌─ 自测（半天）───────────────────────────────────────┐
│  6. pytest + vitest 全绿                              │
│  7. 对照 §0.4 波次集成自测清单                        │
│  8. 对照 §9 UI 对标蓝图做目视检查                     │
│  9. 更新 §1.2.2 该项状态 ⬜ → ✅                      │
└──────────────────────────────────────────────────────┘
          ↓ 进入下一个 W1 项
```

---

### 13.4 微观实现方案文档命名与归档

| 项 | 规范 |
| --- | --- |
| 路径 | `docs/palantier/20_tech/` |
| 命名 | `220tech_「方案名」.md`（如 `220tech_function-engine.md`） |
| 版本 | 首版 v1.0，方案修订递增 |
| 关联 | 文档头部引用本计划对应 W1 编号 + §章节 |
| 归档 | 开发完成且自测通过后，在本文档 §1.2.2 该项状态置 ✅ |

---

## 14. 自主 loop 执行机制

> **来源**：2026-07-22 执行策略讨论结论。本节定义"无人值守"模式下的断点续传、阻塞处理、阶段性总结与跨会话恢复规则。

### 14.1 运行约束（先讲清楚）

| 层面 | 能力 |
| --- | --- |
| 单个回合内连续 loop（方案→开发→测试→更新→总结→下一项） | ✅ 可以 |
| 会话中断后自己定时醒来 | ❌ 不可以（无后台守护） |
| 跨会话恢复 | ⚠️ 需外部唤起（用户"继续" 或 Schedule 定时触发） |

### 14.2 断点真相源（程序计数器）

**唯一可信的进度账本 = §1.2.2 的状态列**。

每次 loop（无论同会话续跑还是跨会话恢复）的第一步：

1. 读 §1.2.2 全表
2. 找**第一个状态为 ⬜ 待执行**的项 → 这就是当前任务
3. 找该项目的微观方案文档 `220tech_「方案名」.md`（若无，先按 §13 写方案）
4. 执行 §13.3 滚动循环
5. 完成后状态 ⬜ → ✅，回到第 1 步

### 14.3 每项的执行步骤（自主模式）

```
读断点 → 取微观方案 → 编码 → 自测(pytest+vitest) → 不回归现有测试
       → 更新 §1.2.2 状态 → 输出阶段性总结 → 立即进入下一项
```

中途**不等用户确认**，连续推进，直到：① 全部 ⬜ 处理完；② 或回合中断。

### 14.4 阻塞处理（不静默跳过，登记后跳下一项）

遇到阻塞，在本节 §14.6 阻塞日志登记，该项状态置 ⏸，**立即跳到下一个 ⬜**继续干，不卡死流水线。

登记字段：`项 | 阻塞原因 | 影响范围 | 登记时间 | 尝试次数`

### 14.5 阶段性总结格式（每完成 1 项输出一次）

```
## W1-x 「项名」完成
- 新增/修改文件：…
- 测试结果：pytest N passed / vitest N passed / 现有用例无回归
- 自测清单：①…✅ ②…✅ ③…✅
- 风险/遗留：…
- 进度：§1.2.2 已置 ✅，下一项 W1-y
```

### 14.6 阻塞日志

| 项 | 阻塞原因 | 影响范围 | 状态 | 解决记录 |
| --- | --- | --- | --- | --- |
| BLK-01 Python 运行时 | 沙箱无 Python ≥3.11 | 全部 W1 后端 pytest | ✅ 已解除 2026-07-22 | python-build-standalone cpython-3.11.15 arm64 解压至 `~/aos_tools/python`，项目建 `.venv`，装 fastapi/pydantic/psycopg[binary]/pytest/httpx |
| BLK-02 PostgreSQL | 无 PG（127.0.0.1:5433），DB 集成测试 34 个红 | 依赖 db.py 的集成测试 | ✅ 已解除 2026-07-22 | 启动 Docker Desktop（`~/Applications/Docker.app`），`docker run` postgres:16-alpine 映射 5433→5432，user/db 对齐 DEFAULT_DSN（aos_app/aos_meta） |

**环境就绪后回归基线**（2026-07-22，m1 分支）：

| 场景 | failed | passed | 结论 |
| --- | --- | --- | --- |
| 无 PG | 39 | 165 | DB 集成测试全红 |
| 起 PG（无 W1-1） | 11 | 432 | 预先存在的 11 失败（数据状态/前端断言/embedding 服务），非 W1 引入 |
| 起 PG（有 W1-1） | 11 | 461（+29） | **零回归**，W1-1 新增 23 测试全绿 |

> 剩余 11 个预先失败（test_analytics_ta4/ta7、test_apollo_channels、test_twa10/11、test_ui_buttons、test_vector_index 等）属既有基线问题，与 W1 系列无关，不阻塞本计划；后续如需可单列修复项。

### 14.7 跨会话恢复（二选一）

- **方式 A（手动）**：用户发"继续"，第一动作读 §1.2.2 断点续传。
- **方式 B（定时）**：用 Schedule 设每 30 分钟 cron，每次触发读断点续传。

---

## 15. 变更

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-07-21 | 初版 · 基于 220w v1.17 差距分析 · 6 Phase · 18 W1 项 · 12 页面对标 · 完整依赖矩阵 |
| v1.1 | 2026-07-22 | 新增执行进度跟踪体系：§0.5 状态定义（✅ 已完成 / ⏸ 暂停 / ⬜ 待执行）· §1.1 里程碑表增加状态列 · §1.2 全局进度看板（18 W1 项逐项标记）· 各 Phase 引用块增加状态行 · Phase 4 标记为 ⏸ 暂停（LLM Gateway 未接入） |
| v1.2 | 2026-07-22 | **进度看板全覆盖**：§1.2 从 18 项扩展至 261 项（220w §11 差距矩阵全量），分 7 个子表：1.2.1 全局统计 · 1.2.2 W1 优先项（24 项·Phase 0–6）· 1.2.3 W2+ 高优先级（27 项·Phase 7+）· 1.2.4 W2+ 中优先级（166 项·Phase 8+）· 1.2.5 W2+ 低优先级（35 项·Phase 9+）· 1.2.6 停车场（7 项·⏸ 暂停）· 1.2.7 已达成（2 项·✅）|
| v1.3 | 2026-07-22 | **与 220w §12 自洽性对齐**：① §1.2.2 W1 项从 24 合并为 19（W1-10 收回 1 项 / Dataset Preview SQL 合并重复 / Transform 算子库合并 / DAG 保存并入 W1-14 / Funnel 可视化并入 W1-3 / Function Type Editor 并入 W1-10+W1-18）· ② §1.2.1 总数 261→259（220w §11 合并 Foundry Rules + Linter 重复项 -2）· ③ §1.2.1 低优先级 35→33 · ④ §1.1 里程碑表 Phase 2 补 W1-19 · ⑤ header 基线改"259 差距项 · W1 19 项" |
| v1.4 | 2026-07-22 | **新增 §13 开发规范（微观方案先行）**：① §13.1 禁止"全量方案后编码"和"无方案开干"两种模式 · ② §13.2 宏观方案 vs 微观实现方案对照表（5 项必补） · ③ §13.3 每个 W1 项滚动循环流程（方案→开发→测试→下一项）· ④ §13.4 微观实现方案文档命名规范（`220tech_「方案名」.md`）· 原 §12 变更顺延为 §14 |
| v1.5 | 2026-07-22 | **新增 §13 开发规范 + §14 自主 loop 执行机制**：① §13 微观方案先行（宏观 vs 微观对照、滚动循环、220tech_ 命名）· ② §14 断点真相源=§1.2.2 状态列、阻塞处理、阶段性总结格式、跨会话恢复 · ③ §0.5 新增 🟡「代码完成·待验证」状态（应对 BLK-01 环境阻塞）· ④ §14.6 登记 BLK-01 基础设施阻塞（沙箱无 Python 3.11）· ⑤ **W1-1 Function 引擎代码完成**：新增 `function_engine.py`（Lexer/Parser/Evaluator/TypeInferer）+ `routers/functions.py`（eval/typecheck）+ `tests/test_function_engine.py`（19 引擎 + 4 API 用例），改 `main.py` 注册路由；引擎核心 19/19 全绿（importlib 直载验证），正式 pytest 待环境 |
| v1.6 | 2026-07-22 | v1.5 拆分记录 · W1-1 §1.2.2 状态置 🟡 |
| v1.7 | 2026-07-22 | **BLK-01/BLK-02 解除 + W1-1 转 ✅**：① 装 Python 3.11.15（python-build-standalone arm64 → `~/aos_tools/python`，建 `.venv` 装依赖）· ② 起 Docker + PG16（postgres:16-alpine，5433→5432，aos_app/aos_meta）· ③ W1-1 正式 pytest **23/23 全绿**（19 引擎 + 4 API）· ④ 全量回归零回归验证（基线 11 failed / 有W1-1 11 failed，passed 432→461 +29）· ⑤ §14.6 阻塞日志 BLK-01/02 标 ✅ 已解除 · ⑥ W1-1 §1.2.2 🟡 → ✅ |
| v1.8 | 2026-07-22 | **W2-E 第五批 媒体集+Lineage+Web IDE（4 项）**：① #1 媒体集类型化创建 + 延迟策略（lazy/eager/stream）· ② #2 媒体集→表格行变换（Pipeline media_set 节点）· ③ #4 Data Lineage L1 增强（22 色板 + 列级血缘 + 交互式 DAG）· ④ #22 Web IDE（会话/LSP 诊断/补全/符号/hover）· ⑤ 全量回归 1140 passed · ⑥ 修复 13 个失败测试（PG 污染清理 + pipeline_embed 租户前缀 + fleet 全局视图）· W2 18/27→22/27 |
| v1.9 | 2026-07-22 | **W2-F 第六批 Funnel/Logic/Writeback 增强版（3 项）· W2 高优先级 27/27 清零**：① #11 Funnel CDC（行级 `_op` 识别 UPSERT/UPDATE/DELETE + snapshot/incremental 双管道 + reindex 全量重索引触发）· ② #17 Logic LangGraph/Wiki（Block `wiki_ref` 字段注入 + LogicGraph 条件路由图编排 + 环路保护）· ③ #19 写回 Workshop 绑定（WritebackLayer workshop_module 绑定/解绑 + 按模块预览合并视图）· ④ 新增 41 测试（CDC 13 + Graph 12 + Workshop 16），全量回归 **1177 passed / 0 failed** · ⑤ 6 新端点运行时验证 200 · W2 22/27→27/27 |
| v2.0 | 2026-07-22 | **W2+ 中优先级启动 · W2-G 第一批 Expectation/WriteMode/Transaction（3 项）**：① #15 Expectation（pk_unique + row_count 检查 + severity error/warn + check_all + has_blocking_failure）· ② #16 WriteMode 增强（新增 default 模式 + describe API + 4 种写入模式）· ③ #17 Transaction 状态机（OPEN→COMMITTED/ABORTED 生命周期 + write_mode 集成 + 不可逆转换）· ④ 新增 38 测试（expectation 16 + txn_state 22），全量回归 **1215 passed / 0 failed** · ⑤ 8 新端点运行时验证 200 · W2+ 中优先级 0/166→3/166 |
| v2.1 | 2026-07-22 | **W2-H Action 增强组（5 项）**：① #54 Side Effects（notification/webhook 副作用注册+触发）· ② #55 Optimistic UI（optimistic token + commit/rollback）· ③ #56 软删除（复用 writeback soft_delete + undelete）· ④ #57 副作用重试（retry×3 → DLQ 死信队列 + retry/clear API）· ⑤ #76 Edits 合并策略（field_level/last_write_wins/manual_arbitration 三种策略）· ⑥ 新增 22 测试，全量回归 **1237 passed / 0 failed** · W2+ 中优先级 3/166→8/166 |
| v2.2 | 2026-07-22 | **W2-I Ontology 治理组（3 项）**：① #31 图谱健康度（graph-health 端点已覆盖 dangling/conflict/orphan/score/issues/archive，零代码变更确认）· ② #38 Ontology 使用指标（UsageMetricsEngine 30天滑动窗口 + per-otype/per-ltype + 4种来源归因 + daily_series）· ③ #69 Ontology 图查询（GraphQueryEngine 多跳 BFS + 双向 BFS 最短路径 + 子图扩展 + rel 过滤 + direction 控制）· ④ 新增 21 测试，全量回归 **1258 passed / 0 failed** · W2+ 中优先级 8/166→11/166 |
| v2.3 | 2026-07-22 | **W2-J OMA 编辑器增强组（3 项）**：① #28 Property Editor（backing_column/dataset + title_key 唯一性 + TSP + origin_mapping + validation_rules）· ② #34 独立编辑器（独立 Property CRUD API 7 端点，不修改 meta_object_type）· ③ #35 Proposals 审查工作流（7 态状态机 DRAFT→PENDING→IN_REVIEW→APPROVED→PUBLISHED + reject/withdraw + 评论 + 审查者 + 状态转换校验）· ④ 新增 21 测试，全量回归 **1279 passed / 0 failed** · W2+ 中优先级 11/166→14/166 |
| v2.4 | 2026-07-22 | **W2-K Ontology 管理增强组（3 项）**：① #36 编辑历史/恢复（EditHistoryEngine 全局时间线 + 按作者合并 + 逐条回退 + 批量回退）· ② #37 清理工具（CleanupEngine 3 级操作 delay/deprecate/delete + 6 种标记自动扫描 deprecated_date/recycle_bin/long_no_update/missing_description/name_regex/unindexed + 批量操作）· ③ #32 Ontology Interface（InterfaceEngine CRUD + extends 继承 + implement 实现 + effective_properties 多态 + 删除保护）· ④ 新增 24 测试，全量回归 **1303 passed / 0 failed** · W2+ 中优先级 14/166→17/166 |
| v2.5 | 2026-07-22 | **W2-L Object 数据层增强组（3 项）**：① #33 Shared Property（SharedPropertyEngine CRUD + attach/detach 引用绑定 + 被引用时删除保护 + 幂等绑定）· ② #29 Type Coherence（TypeCoherenceEngine TC-01 类型不匹配 + TC-02 缺失列 + TC-03 多余列 + TC-04 可空性冲突 + 类型兼容组 string/text/int/integer/float/double 等 + check_all 批量检测）· ③ #30 多源异构解法 A/C（解法A L1JoinConfig 宽表配置 + JoinSpec left/inner/outer + preview_join 列预览 + 解法C ComputedProperty 函数绑定 + input_mapping + output_type）· ④ 新增 25 测试，全量回归 **1328 passed / 0 failed** · W2+ 中优先级 17/166→20/166 |
| v2.6 | 2026-07-22 | **W2-M Object Explorer 增强组（3 项）**：① #48 高级搜索语法（SearchEngine 表达式解析器 = / != / > / >= / < / <= / LIKE / ~= / IN / AND / OR / NOT + LINKS TO/FROM 链接筛选 + 分页）· ② #49 保存探索/列表（ExplorationEngine CRUD + dynamic/static + private/public 可见性 + execute 动态探索执行）· ③ #50 批量操作/导出（ExportEngine csv/excel(BOM)/json 三格式 + 列筛选 + ID 筛选 + bulk_update + bulk_delete）· ④ 新增 30 测试，全量回归 **1358 passed / 0 failed** · W2+ 中优先级 20/166→23/166 |
| v2.7 | 2026-07-22 | **W2-N Object 编辑与冲突组（3 项）**：① #42 编辑冲突解决（ConflictEngine 检测+解决 + user_priority 用户优先级 + timestamp_priority 时间戳优先 + 已解决保护）· ② #44 模式迁移（MigrationEngine ADD/REMOVE/RENAME/CHANGE_TYPE/SET_NULLABLE 5 指令 + 批次 500 上限 + dry_run 预览 + PENDING→RUNNING→COMPLETED/FAILED 状态跟踪）· ③ #45 编辑历史追踪（ChangeLogEngine per-OT enable/disable 开关 + record/record_force + 多维查询 OT/对象/字段/作者/操作/时间范围 + get_timeline 时间线）· ④ 新增 26 测试，全量回归 **1384 passed / 0 failed** · W2+ 中优先级 23/166→26/166 |
| v2.8 | 2026-07-22 | **W2-O 类型系统与视图配置组（3 项）**：① #52 完整类型系统（TypeSystem 22 内置类型 5 类别 scalar/temporal/binary/composite/security + String/Integer/Float/Boolean/Date/Timestamp/Vector/Geopoint/ByteArray/Cipher/Hash 等 + validate 验证 + coerce 强制转换 + 自定义注册）· ② #51 Object Views 配置文件（ViewProfileEngine CRUD + ViewTab 标签页 + activate 为用户组激活 + get_active 默认回退）· ③ #53 值类型/条件格式化/类型类（FormatEngine 32 内置类型类 currency/percentage/url/email/file_size 等 + render 渲染 + ConditionalFormat 条件格式 > / < / >= / <= / = / != / contains 评估）· ④ 新增 34 测试，全量回归 **1418 passed / 0 failed** · W2+ 中优先级 26/166→29/166 |
| v2.9 | 2026-07-22 | **W2-P Action 参数增强组（3 项）**：① #58 参数约束（ConstraintEngine user_input/multiple_choice/object_set 三类型 + min/max/pattern/required 校验 + validate_value + get_options 候选项 + Object Set 注册）· ② #59 参数默认值（DefaultEngine static/object_property/type_class/environment 4 来源 + resolve 动态求值 + fallback 回退 + 对象注册）· ③ #60 参数覆盖（OverrideEngine 条件评估 = / != / > / < / >= / <= 6 操作符 + visible/disabled/required 三态合并 + 多覆盖块叠加 + applied_overrides 追踪）· ④ 新增 42 测试，全量回归 **1460 passed / 0 failed** · W2+ 中优先级 29/166→32/166 |
| v3.0 | 2026-07-22 | **W2-Q Action 增强延伸组（3 项）**：① #61 参数筛选（FilterEngine base_set/object_pool 起始集 + search_scope 属性限定 + security_filter 表达式筛选 = / != / > / < / >= / <= + ordering 排序 asc/desc + {{var}} 模板替换）· ② #62 提交标准可视化（CriteriaEngine 条件树 AND/OR/NOT 嵌套 + 叶子节点 = / != / > / < / >= / <= / contains / in / exists 10 操作符 + severity error/warning + failure_message）· ③ #63 通知副作用（NotificationEngine static/parameter/object_property/function 4 来源收件人 + {{var}} 模板渲染 subject/body + email/sms/in_app 3 渠道 + dispatch 派发队列 + 派发记录查询）· ④ 新增 45 测试，全量回归 **1505 passed / 0 failed** · W2+ 中优先级 32/166→35/166 |
| v3.1 | 2026-07-22 | **W2-R Action Webhook/Sections/Revert 组（3 项）**：① #64 Webhook 副作用（WebhookEngine data_output/side_effect 双模式 + GET/POST/PUT/PATCH 4 方法 + none/bearer/basic/hmac 4 认证 + input_mapping/output_mapping + {{var}} 模板渲染 URL 与 payload + dot-path 响应字段提取 + build_request/apply_response）· ② #65 Action Sections（SectionEngine single_column/double_column 布局 + span 半宽/全宽 + collapsed 折叠 + visible_condition 条件显示 = / != / > / < / >= / <= + 批量 reorder 重排序 + 跨 action 隔离）· ③ #66 Action 撤销（RevertEngine revert_window_seconds 时间窗口 + pre_revert_check 条件树 AND/OR/NOT 递归 + 6 态状态机 pending→eligible/blocked→in_progress→completed/failed + RevertRecord 记录追踪 + 状态转换校验 INVALID_TRANSITION）· ④ 新增 41 测试，全量回归 **1546 passed / 0 failed** · W2+ 中优先级 35/166→38/166 |
| v3.2 | 2026-07-22 | **W2-S Action 收尾组（3 项）**：① #67 Action 日志对象类型（ActionLogEngine [LOG]ActionName 类型自动生成 + operation_rid 全局唯一 + version 自增 + 参数快照 + submitted/succeeded/failed/reverted 状态 + 按版本号排序 + log-type 定义生成）· ② #68 Action 平台集成（ActionBindingEngine object_view/object_explorer/workshop 三集成 + primary/secondary/overflow 按钮位置 + visibility_condition 条件 + WorkshopButtonGroup horizontal/vertical 布局 + attach/detach 幂等 + 删除绑定时级联从按钮组移除）· ③ #70 Action 事务回滚（SagaEngine 6 态状态机 pending→running→completed/compensating→compensated/failed + forward/compensation 步骤记录 + 补偿按 order 倒序 + 自动状态推进 running→completed/compensating→compensated/failed + 级联删除步骤记录 + get_state 进度快照）· ④ 新增 44 测试，全量回归 **1589 passed / 1 wiki flaky**（wiki 版本分页上限 50 导致，与 W2-S 无关） · W2+ 中优先级 38/166→41/166 |
| v3.3 | 2026-07-22 | **W2-T k-LLM 路由编排组（3 项）**：① #71 k-LLM 智能路由（SmartRouter 5 维评分 capability/context/cost/security/tag + 硬过滤 enabled/上下文/模态/安全/预算 + alternatives 次优候选 + score_breakdown 透明可审计 + NO_CANDIDATE 错误码）· ② #72 k-LLM 场景化路由（ScenarioRouter RouteRule 对齐 81 §2.1 id/task/primary/fallback/egress/span + BlockRoute 块级绑定 + resolve 块级>场景>默认三级回落 + inherit 继承 + export/import 批量与 81 PUT /v1/aip/model-routes 对齐 + INVALID_TASK_TYPE/INVALID_EGRESS 校验）· ③ #73 k-LLM 熔断/热切换（FailoverEngine 3 态状态机 closed→open→half_open + cooldown 冷却推进 + half_open 探测配额 + success_threshold 关闭熔断 + call_with_failover 主备热切换 + PRIMARY_FAILED_NO_FALLBACK/FALLBACK_OPEN/ALL_FAILED 错误码 + CallRecord 调用审计 + circuit-drill 演练不改生产 + LLMRoutingFacade 端到端编排 smart_route_and_call/scenario_route_and_call）· ④ 新增 45 测试，全量回归 **1634 passed / 1 wiki flaky**（pre-existing） · W2+ 中优先级 41/166→44/166 |
| v3.4 | 2026-07-22 | **W2-U k-LLM 扩展能力组（3 项）**：① #74 数据出境策略（EgressPolicyEngine SensitiveField 敏感字段标记 public/internal/sensitive/restricted + 4 脱敏策略 none/hash/redact/substitute + EgressPolicy allow/restricted/forbidden 三等级 + mask_before_egress 字段级脱敏 + audit_sample_rate 抽检 + EgressDecision 决策 + EgressAuditRecord 审计记录 + 默认策略回退 + INVALID_SENSITIVITY/INVALID_MASK_STRATEGY/INVALID_EGRESS/INVALID_AUDIT_RATE 校验）· ② #75 自定义 LLM 注册（CustomLLMRegistry FunctionInterface 函数接口形态 + LLMSource knowledge_base/vector_index/dataset/media_set 4 source_type + LLMWebhook GET/POST 2 method + none/bearer/basic/hmac 4 auth_type + list_all 三形态统一视图 + INVALID_SOURCE_TYPE/INVALID_METHOD/INVALID_AUTH_TYPE 校验 + 与 llm_provider_registry 互补不冲突）· ③ #77 Prompt 工程（PromptEngine PromptTemplate CRUD + {{var}} 变量自动提取 + few_shot_examples Few-shot 拼接 + version 版本自增 + activate_version 同 name 仅一个 active + render 渲染未提供变量保留原样 + inactive 模板回退到 active + render_and_call 端到端调用 llm_gateway.chat）· ④ 新增 45 测试，全量回归 **1679 passed / 1 wiki flaky**（pre-existing） · W2+ 中优先级 44/166→47/166 |
| v3.5 | 2026-07-22 | **W2-V AIP 智能层扩展组（3 项）**：① #78 调试器（DebuggerEngine DebugSession/DebugStep + create_session 按 inputs 自动构造 input+execute 步骤 + step_forward/backward 步进 + variables_after 累积变量快照 + run_to_completion 连续执行 + ProposalPreview 提议预览 applied=False 不应用 + apply_proposal 标记 + ALREADY_APPLIED 幂等 + SESSION_COMPLETED/AT_BEGINNING 状态校验）· ② #79 Automate 集成（AutomateEngine AutomateTrigger CRUD + 5 种 event_type object_changed/schedule/manual/webhook/threshold + _eval_condition 条件树 eq/ne/gt/lt/ge/le + cooldown_seconds 冷却期 + fire 触发流程 AUTOMATE_DISABLED/IN_COOLDOWN/CONDITION_NOT_MET 三重检查 + AutomateRun 执行记录 + proposal_id 关联提案 + trigger_count 计数 + 自动 200 条上限）· ③ #80 四层成熟度（MaturityEngine DEFAULT_LEVELS L1 基础/L2 辅助/L3 半自动/L4 全自动 + register_capability 能力注册 + assess 楼梯模型找最高满足 + L0 基线 + gaps gap 分析从 current+1 到 target + recommendation 文案 + set/get_target_level + list_assessments 历史 200 条 + INVALID_LEVEL 校验）· ④ 新增 43 测试，全量回归 **1722 passed / 1 wiki flaky**（pre-existing） · W2+ 中优先级 47/166→50/166 |
| v3.6 | 2026-07-22 | **W2-W L4 自动化收尾组（3 项）**：① #82 L4 熔断（L4CircuitEngine L4CircuitConfig window_size=100/failure_threshold=5%/recovery_threshold=2.5% 滞回/cooldown_seconds=60s + L4CircuitState current_level/degraded/failure_rate + record_call 滑动窗口 deque + 失败率>5% 自动降级 L3 + 失败率<=2.5% 且 cooldown 过自动恢复 L4 + L4Alert degrade/recover/threshold_exceeded 告警 + force_degrade/force_recover 演练 + 200 条上限 + reset + INVALID_CONFIG 校验）· ② #83 模型预热（ModelWarmupEngine WarmupState cold/warming/ready/failed 4 态状态机 + register_model + warmup 注入 probe_callable 默认 True + 失败退避 cooldown_until = 5s×count 上限 60s + mark_ready/mark_failed 外部探测器 + list_probe_results 200 条 + IN_COOLDOWN/NOT_FOUND 错误码 + warmup 锁外执行避免阻塞）· ③ #86 三种提案通道（ProposalChannelEngine DEFAULT_CHANNELS sync 同步通道即时 completed+approved/async_automate 异步 Automate 通道 pending/async_pipeline 异步管道通道 pending + ProposalSubmission 24h visible_until 安全窗口 + approve/reject/cancel 三态决策 + ALREADY_APPROVED/ALREADY_REJECTED/SUBMISSION_CANCELLED/SUBMISSION_FINAL 校验 + cleanup_expired 过期清理 + 200 条上限 + INVALID_CHANNEL/CHANNEL_DISABLED/INVALID_LOGIC_ID 校验）· ④ 新增 42 测试，全量回归 **1764 passed / 1 wiki flaky**（pre-existing） · W2+ 中优先级 50/166→53/166 |
| v3.7 | 2026-07-22 | **W2-X AIP 决策审计组（3 项）**：① #84 Decision Lineage（DecisionLineageEngine DecisionRecord 8+ 字段 logic_id/proposal_id/model_id/prompt_version/object_refs/wiki_fields/cot/tool_calls/draft_params/approval_result/actor/metadata + record/get/list 多维过滤 logic_id/proposal_id/actor + get_timeline 时间线 Tool 调用+审批事件 + trace 按提案溯源 + 200 条上限 FIFO 淘汰 + NOT_FOUND 错误码）· ② #85 Insight Backfill（InsightBackfillEngine BackfillConfig confidence_threshold=0.85/auto_backfill=False/max_daily_backfill=100 + register_insight confidence[0,1] 校验 + get/list 多维过滤 source_decision_id/backfill_status/min_confidence + backfill pending→completed 状态机 + evaluate_and_register 阈值守门 BELOW_THRESHOLD + list_pending + cleanup 清理 failed + ALREADY_BACKFILLED 幂等 + INVALID_CONFIDENCE/INVALID_THRESHOLD 校验）· ③ #87 Capability Adapter 契约（CapabilityAdapterEngine AdapterManifest capability_class C0 同步/C1 异步 Job/C2 长会话 + auth_type none/bearer/basic/hmac + CRUD register/get/list/update/delete + update 禁改 capability_class IMMUTABLE_FIELD + _check_adapter ADAPTER_DISABLED/INVALID_CLASS 校验 + invoke/submit/status/cancel/artifact/session_open/session_close 7 操作 + invoke_callable 可注入默认 echo + status 5 状态机 + list_invocations 多维过滤 adapter_id/job_id/session_id + 200 条上限）· ④ 新增 57 测试，全量回归 **1821 passed / 1 wiki flaky**（pre-existing） · W2+ 中优先级 53/166→56/166 |
| v3.8 | 2026-07-22 | **W2-Y 契约与安全标记组（3 项）**：① #88 CAP 约束（CapConstraintEngine DEFAULT_CAP_RULES 7 规则 CAP-01~07 对齐 07b §4 + CapRule code/title/description/severity error/warning/enforcement block/audit/dry_run + audit 开关 + check 返回 CapViolation resolution=blocked/audited/dry_run_passed + list_violations 按 code/target_type 多维过滤 + get_violation 单条 + update 禁改 code IMMUTABLE_FIELD + 200 条记录上限 FIFO 淘汰 + NOT_FOUND/INVALID_ENFORCEMENT/INVALID_SEVERITY 校验）· ② #99 安全标记传播控制（MarkingPropagationEngine MarkingPropagationConfig stop_propagating/stop_requiring/inherit_from_parent/expand_input_inheritance 4 开关 + MarkingRecord security_label public/internal/sensitive/restricted 4 级 + is_inherited 继承标记 + propagate 检查 stop_propagating True 下游安全标签降为 public+is_inherited=False 中断继承链/False 拷贝源标签+is_inherited=True 维持继承 + 200 条上限 + NOT_FOUND 源记录不存在校验）· ③ #100 标记移除策略（MarkingRemovalEngine MarkingRemovalPolicy strategy filter_in/filter_out + removed_labels 移除标签集 + keep_labels 保留标签集 + apply_to_inherited 是否处理继承标签 + apply filter_in final=原∩keep_labels 交集保留/filter_out final=原-removed_labels 差集移除 + apply_to_inherited=False 跳过继承标签但保留于 final_labels + skipped_inherited 计数 + MarkingRemovalResult 记录 + POLICY_DISABLED 策略禁用 + 200 结果上限 + register 校验 filter_in 需 keep_labels 非空/filter_out 需 removed_labels 非空防 no-op）· ④ 新增 58 测试，全量回归 **1878 passed / 2 pre-existing flaky**（test_usage_prune_old 日期窗口 + test_wiki_version_snapshot_on_approve 50 条上限，均与 W2-Y 无关） · W2+ 中优先级 56/166→59/166 |
| v3.9 | 2026-07-22 | **W2-Z Pipeline 类型语义组（3 项 + #92/#93 清账 2 项 = 5 项）**：① #94 Pipeline Types（PipelineTypeEngine DEFAULT_PIPELINE_TYPES 三预置 batch 批处理 scheduled+restart+append/incremental 增量 on_change+checkpoint_replay+upsert/streaming 流式 continuous+skip+append + PipelineTypeSpec trigger_semantics/state_machine/fault_strategy/supports_checkpoint/supports_windowing + CRUD register/get/list/update/delete + update 禁改 type IMMUTABLE_FIELD + validate_run 类型与 write_mode 匹配校验 + INVALID_TYPE/INVALID_TRIGGER/INVALID_FAULT_STRATEGY/NOT_FOUND 校验）· ② #95 Incremental Pipeline（IncrementalPipelineEngine Watermark 水位线 field/value + get/set_watermark + ChangeRecord CDC insert/update/delete + register_change/list_changes op+since_watermark 过滤 + Checkpoint pending→committed 状态机 sequence 自增 + create/commit/list_checkpoints + ALREADY_COMMITTED 幂等 + process_increment 取 watermark 之后变更→创建 checkpoint→处理→推进 watermark→提交 + 无变更 skipped + 200 条上限 + INVALID_OPERATION/INVALID_PK/INVALID_FIELD 校验）· ③ #96 Streaming Pipeline（StreamingPipelineEngine WindowSpec tumbling/sliding/session 三窗口 + size_ms/slide_ms/gap_ms + StreamEvent key/event_ts + WindowState open/emitted + ingest tumbling floor 对齐/sliding 多窗口枚举/session 按 gap_ms 合并或新建 + advance_watermark 推进水位线关闭到期窗口 + close_window 手动关窗 + list_events/list_windows 过滤 + WATERMARK_REGRESS 水位线不可回退 + INVALID_WINDOW_TYPE/INVALID_SIZE/INVALID_GAP/NOT_FOUND 校验 + 200 条上限）· ④ #92/#93 清账（expectation.py ExpectationEngine PK_UNIQUE/ROW_COUNT + pipeline_output.py PipelineOutputEngine 6 种 WriteMode 基础已存在+有测试，标记完成）· ⑤ 新增 61 测试，全量回归 **1939 passed / 2 pre-existing flaky**（同 W2-Y） · W2+ 中优先级 59/166→64/166 |
| v4.0 | 2026-07-22 | **W2-AA 触发器与 Ontology 链接输出组（3 项）**：① #97 事件触发器（EventTriggerEngine EventTrigger event_source dataset_updated/pipeline_built/schedule/manual 四源 + target_pipeline_id + cooldown_seconds 冷却期 + fire 三状态 fired/skipped/cooldown 检查 enabled→cooldown→fired + 推进 last_fired_at/fire_count + TriggerFire 点火记录 + list_fires 按 trigger_id 过滤 + 200 条 fire 上限 FIFO 淘汰 + register 校验 MISSING_NAME/INVALID_EVENT_SOURCE/MISSING_TARGET + update 改源校验 + NOT_FOUND）· ② #98 复合触发器（CompositeTriggerEngine CompositeTrigger logic and/or + child_trigger_ids 子触发器引用 + evaluate AND 全 True/OR 任一 True + child_fires 缺失视为 False + fire 通过 fired/未通过 skipped + 推进 fire_count + 200 条 fire 上限 + register 校验 MISSING_NAME/INVALID_LOGIC/EMPTY_CHILDREN/MISSING_TARGET + update 改逻辑校验 + NOT_FOUND）· ③ #91 Pipeline Ontology 链接类型输出（LinkTypeOutputEngine LinkTypeDefinition cardinality one_to_many/many_to_one/many_to_many + source/target_object_type + source_pk_field/target_fk_field + display_field + CRUD register/get/get_by_name/list/update/delete + register 校验 INVALID_CARDINALITY/MISSING_NAME/MISSING_OBJECT_TYPE/MISSING_KEY_FIELD/NAME_DUPLICATE 重名 + update 改名重名校验 + infer_from_objects 默认 many_to_one + preview_links 返回链接实例 + 200 条上限）· ④ 新增 59 测试，全量回归 **1998 passed / 2 pre-existing flaky**（同 W2-Y/Z） · W2+ 中优先级 64/166→67/166 |
| v4.1 | 2026-07-22 | **W2-AB Data Health 检查组（3 项）**：① #133 检查类型（HealthCheckTypeEngine HealthCheckType check_kind freshness/freshness_duration/volume/schema/content 5 种 + configuration threshold/expected_columns/rules + severity error/warning/info + CRUD + run 按 check_kind 评估：freshness 时间戳延迟秒/freshness_duration 小时延迟/volume 行数阈值/schema 列名集合匹配/content 规则树 eq/ne/gt/lt/ge/le/in/contains 8 操作符 + disabled→skipped + 200 条 result 上限 FIFO + INVALID_CHECK_KIND/MISSING_NAME/INVALID_SEVERITY/MISSING_DATASET 校验）· ② #134 检查计划（HealthScheduleEngine HealthSchedule mode auto/manual 双模式 + auto trigger_dataset_rid 事件驱动 next_run_at=0 + manual cron_expression 定时 + _parse_cron_seconds cron 简化解析 + trigger 推进 last_run_at/run_count + manual 重算 next_run_at + compute_next_run + enable/disable + 200 条上限 + INVALID_MODE/MISSING_TRIGGER_DATASET/MISSING_CRON/MISSING_CHECK 校验）· ③ #135 检查组（HealthCheckGroupEngine HealthCheckGroup check_ids + notification_config channels/severity_filter + CRUD + attach_check/detach_check 幂等 + monitor 返回 GroupMonitorSummary total/enabled/last_results/pass_rate 容忍缺失检查 missing + send_notification severity 过滤派发 + 200 条通知上限 + NAME_DUPLICATE 重名校验）· ④ 新增 61 测试，全量回归 **2059 passed / 2 pre-existing flaky**（同前） · W2+ 中优先级 67/166→70/166 |
| v4.2 | 2026-07-22 | **W2-AC 代码仓库与 PR 工作流组（3 项）**：① #101 分支管理（BranchEngine Branch repo_id/name/base_branch/head_commit/protected/status open/merged/deleted + CRUD register/get/get_by_name/list 按 repo_id+status 过滤/update/delete 软删除置 deleted + register 校验 MISSING_NAME/MISSING_REPO + merge 检查 source open→target 同 repo 存在→生成 new_commit→source.status=merged 推进 merged_at + ALREADY_MERGED 已合并分支拒绝/TARGET_NOT_FOUND 目标不存在 + merge 支持 merge/rebase/squash 3 策略 + protect 保护分支切换 + 200 条上限 FIFO 淘汰 + NOT_FOUND）· ② #102 PR 工作流（PullRequestEngine PullRequest status open/reviewing/approved/rejected/merged/closed 6 态 + ci_status pending/running/passed/failed 4 态 + _VALID_PR_TRANSITIONS 状态机 open→reviewing/closed·reviewing→approved/rejected/open/closed·approved→merged/open·rejected→open/closed·merged/closed 终态不可逆 + CRUD + list 按 repo_id+status+author 三维过滤 + transition 状态转换校验 INVALID_TRANSITION + add_reviewer 幂等去重 + set_ci_status 校验 INVALID_CI_STATUS + merge 需 approved+ci_status=passed 双条件 MERGE_NOT_ALLOWED/CI_NOT_PASSED + 200 条上限）· ③ #103 变换预览（TransformPreviewEngine TransformPreview name/repo_id/branch/transform_code/language python|sql/input_schema/sample_rows + CRUD register/get/list 按 repo_id+language 过滤/update/delete 硬删除 + register 校验 MISSING_NAME/MISSING_CODE/INVALID_LANGUAGE + update 改 language 校验 + run python exec transform(rows) 函数受限命名空间执行/异常捕获 status=error + sql 简化 passthrough 返回 sample_rows + _infer_schema 从首行推断 boolean/integer/float/string/any + PreviewResult status success|error + row_count + list_results 按 preview_id 过滤倒序 + 200 条 result 上限 FIFO 淘汰 + NOT_FOUND）· ④ 新增 45 测试（14 Branch+15 PR+13 Preview+3 单例），全量回归 **2104 passed / 2 pre-existing flaky**（test_usage_prune_old 日期窗口 + test_wiki_version_snapshot_on_approve 50 条上限，均与 W2-AC 无关） · W2+ 中优先级 70/166→73/166 |
| v4.3 | 2026-07-22 | **W2-AD 开发者工具组（3 项）**：① #104 Python 调试器（PythonDebuggerEngine DebugSession code/breakpoints/state created/running/paused/completed/error 5 态 + current_line + variables 变量快照 + output 输出捕获 + create_session/get_session/list_sessions 按 state 过滤 + step 单步执行 exec 单行受限命名空间 _BANNED_BUILTINS 禁 open/input/eval/exec/compile 等 + 命中末行 completed + is_breakpoint 断点标记 + run_to_completion 连续执行命中下一行断点暂停 + _MAX_STEPS=1000 死循环上限 + get_variables 变量快照 + delete_session + _safe_repr 安全化不可序列化对象 + MISSING_CODE/NOT_FOUND/SESSION_COMPLETED/STEP_ERROR + 200 条 session 上限 FIFO）· ② #105 单元测试（UnitTestEngine TestCase name/language python|java|typescript/code/target_function/timeout_seconds + CRUD register/get/list 按 language 过滤/update/delete + run python exec AssertionError→failed/其他异常→error/正常→passed + java/typescript 简化 simulated passed + TestResult status passed|failed|error|skipped + output + duration_ms + list_results 按 case_id 过滤倒序 + 200 条 result 上限 FIFO + MISSING_NAME/MISSING_CODE/INVALID_LANGUAGE/NOT_FOUND 校验）· ③ #106 Artifact 存储库（ArtifactRegistryEngine Artifact name/version/format conda|docker|maven/registry_url/description/tags/dependencies/size_bytes/checksum + CRUD register/get/list 按 format+name+tag 三维过滤/update/delete + get_by_name_version + list_versions 按 name 列所有版本 + list_dependencies 返回直接依赖制品不递归 + register 校验 MISSING_NAME/MISSING_VERSION/INVALID_FORMAT/NAME_VERSION_DUPLICATE 重名同版本 + 200 条上限 FIFO + NOT_FOUND）· ④ 新增 45 测试（14 Debugger+14 UnitTest+14 Artifact+3 单例），全量回归 **2149 passed / 2 pre-existing flaky**（同前） · W2+ 中优先级 73/166→76/166 |
| v4.4 | 2026-07-22 | **W2-AE AIP 辅助与仓库配置组（3 项）**：① #107 AIP Assist（AIPAssistEngine AIPAssistRequest kind explain/vulnerability/translate/complete 4 种 + code/language python/java/typescript/sql + status pending/running/completed/error 4 态 + CRUD register/get/list 按 kind+status 过滤/update/delete + run 按 kind 分派：explain 返回 summary+lines；vulnerability 扫描 _DANGEROUS_BUILTINS 单词边界 \bXXX\( 正则匹配返回 vulnerabilities 列表+count；translate python→java 简化关键字映射 def→public void/True→true/False→false/None→null/print→System.out.println 返回 translated+target_language；complete 基于末行末尾字符规则补全返回 suggestion + ALREADY_COMPLETED 防重复 run + 200 条 result 上限 FIFO + list_results 按 kind 过滤倒序 + MISSING_CODE/INVALID_KIND/INVALID_LANGUAGE/NOT_FOUND 校验）· ② #108 repoSettings.json（RepoSettingsEngine RepoSettings repo_id/label_validation required_prefixes+color_required/pr_template/validation_rules kind branch_protection|required_reviewers|status_check|path_filter 4 种/enforce_branch_protection + CRUD register/get/get_by_repo/list 按 repo_id 过滤/update/delete + validate_label 前缀校验 missing required prefix + 颜色校验 label.count(":")>=2 视为含颜色 color required + render_pr_template 占位符 {key} 简单替换 + register/update 校验 INVALID_RULE_KIND + 200 条上限 FIFO + MISSING_REPO/NOT_FOUND 校验）· ③ #110 推荐项目结构（ProjectStructureEngine ProjectStructure name/description/layers datasource|transform|ontology|workflow 4 层/components StructureComponent layer+name+type dataset|transform|ontology|workflow|metric 5 种+rid_prefix+required + CRUD register/get/list 按 name 过滤/update/delete + render_template 返回 {name,description,layers,components} + validate_project 校验 required 组件必须存在返回 {valid,missing,extra} 三段式结果 + register/update 校验 INVALID_LAYER/INVALID_COMPONENT_TYPE + 200 条上限 FIFO + MISSING_NAME/NOT_FOUND 校验）· ④ #109 列级血缘标记为「部分已交付」：CRUD 部分已由 W2-E #4 在 lineage_views.py 交付（set_column_lineage/get_column_lineage + test_column_level_lineage），剩余「列级影响分析」增量端点留待 W2-AF+· ⑤ 新增 45 测试（16 AIPAssist+13 RepoSettings+13 ProjectStructure+3 单例），全量回归 **2194 passed / 2 pre-existing flaky**（同前） · W2+ 中优先级 76/166→79/166 |
| v4.5 | 2026-07-22 | **W2-AF 逻辑流与 Data Connection Agent 组（3 项）**：① #111 逻辑流（LogicFlowEngine LogicFlow name/description/steps list[FlowStep]/status draft/running/completed/error + FlowStep kind compass_files_lister/connector/join/transform 4 种/config/next_step_id + CRUD register/get/list 按 status 过滤/update/delete + execute 按 steps 顺序执行每步 _run_step 分派：compass_files_lister 返回 config.files 列表/connector 返回 connection 模拟/join 合并前步 output list+config.lists/transform 返回 config.transformed + 单步失败整体 error + FlowExecution status running/completed/error + step_results 链 + list_executions 按 flow_id 过滤倒序 + 200 条 execution 上限 FIFO + MISSING_NAME/INVALID_STEP_KIND/NOT_FOUND 校验）· ② #112 Agent Proxy（AgentProxyEngine AgentProxy name/agent_id/proxy_url/auth_token/status online/offline/draining 3 态/connections/last_heartbeat + CRUD register/get/list 按 status+agent_id 过滤/update/delete + heartbeat 推进 last_heartbeat+status=online + drain 置 draining + forward_request 校验 status=online 否则 PROXY_UNAVAILABLE + connections 计数 +1/-1 + 模拟转发返回 {forwarded,response.status_code=200} + 200 条上限 FIFO + MISSING_NAME/MISSING_AGENT/MISSING_URL/NOT_FOUND/PROXY_UNAVAILABLE 校验）· ③ #113 Agent Worker（AgentWorkerEngine AgentWorker agent_id/host/version/status registered/online/offline/failed 4 态/capabilities list/last_heartbeat/job_ids + WorkerJob worker_id/capability/payload/status assigned/running/completed/failed/result + CRUD register/get/list 按 status+agent_id 过滤/update/delete + heartbeat 推进 last_heartbeat+status=online + assign_job 校验 status=online WORKER_OFFLINE + capability 在 capabilities 中 CAPABILITY_NOT_SUPPORTED + 创建 job 加入 worker.job_ids + complete_job 推进 status=completed + ALREADY_COMPLETED 防重复 + list_jobs 按 worker_id+status 过滤 + 200 条 job 上限 FIFO + MISSING_AGENT/MISSING_HOST/NOT_FOUND 校验）· ④ 新增 46 测试（15 LogicFlow+14 AgentProxy+14 AgentWorker+3 单例），全量回归 **2240 passed / 2 pre-existing flaky**（同前） · W2+ 中优先级 79/166→82/166 |
| v4.6 | 2026-07-22 | **W2-AG 列级影响分析 + Data Connection 管理组（3 项）**：① #109 列级血缘增量（ColumnImpactEngine 增量补丁，CRUD 已由 W2-E #4 交付；新增 ColumnImpactRule source_dataset_rid+source_column+downstream_datasets+downstream_columns+transform_expr + CRUD register/get/list 按 source_dataset_rid 过滤/delete + analyze_impact BFS 下游传播 visited 防环路 ImpactResult impacted_datasets+impacted_columns+depth + 200 条上限 FIFO + MISSING_SOURCE_DATASET/MISSING_SOURCE_COLUMN/NOT_FOUND 校验）· ② #114 Agent 管理（AgentAdminEngine AgentAdmin agent_id+name+version+status registered|active|deprecated+download_url+drivers list[AgentDriver]+certificates list[AgentCertificate]+logs list[AgentLogEntry]+auto_upgrade+last_heartbeat + CRUD register/get/list 按 agent_id+status 过滤/update/delete + heartbeat 推进 last_heartbeat+registered→active + push_log 200 条滚动 + INVALID_LOG_LEVEL 校验 + upgrade 推进 version+status=active + list_drivers/list_certificates + get_download_url 校验 status≠deprecated AGENT_DEPRECATED + INVALID_DRIVER_TYPE/MISSING_AGENT/MISSING_NAME/NOT_FOUND 校验 + 200 条上限 FIFO）· ③ #115 源探索（SourceExplorerEngine SourceSchema source_id+dataset_name+er_diagram list[ERRelation]+resource_tree list[ResourceNode]+sample_preview list[dict] + CRUD register/get/list 按 source_id 过滤/update/delete + explore_er 返回 ER 关系列表 + explore_resource_tree 返回资源树 + preview_sample 前 limit 条 + INVALID_RELATION_TYPE/INVALID_RESOURCE_TYPE/MISSING_SOURCE/MISSING_DATASET_NAME/NOT_FOUND 校验 + 200 条上限 FIFO）· ④ 新增 49 测试（14 ColumnImpact+19 AgentAdmin+14 SourceExplorer+2 单例），全量回归 **2289 passed / 2 pre-existing flaky**（同前） · W2+ 中优先级 82/166→85/166 |
| v4.7 | 2026-07-22 | **W2-AH Data Connection 文件处理组（3 项）**：① #116 文件筛选（FileFilterEngine FileFilterRule id+name+path_pattern+min_size_bytes+max_size_bytes+modified_after+modified_before+exclude_synced + CRUD register/get/list/update/delete + apply_filter 多条件组合过滤 路径正则/大小范围/mtime 范围/排除已同步 + 200 条上限 FIFO + MISSING_NAME/NOT_FOUND 校验）· ② #117 文件变换（FileTransformEngine FileTransform id+name+transform_type gzip|merge|rename|pgp_decrypt|add_timestamp+config + CRUD register/get/list/update/delete + apply_transform 按类型生成输出文件 gzip .gz 后缀/merge merged_*.dat/rename {pattern} 模板/pgp_decrypt .decrypted 后缀/add_timestamp 时间戳前缀 + 200 条上限 FIFO + MISSING_NAME/INVALID_TRANSFORM_TYPE/NOT_FOUND 校验）· ③ #118 Streaming Sync（StreamingSyncEngine StreamingSync id+name+source_type kafka|kinesis|pubsub+source_config+target_stream+status stopped|running+offset+last_consumed_at + SyncRecord sync_id+event_key+event_value+offset+timestamp+status synced|failed+error_message + CRUD register/get/list/update/delete + start/stop 切换状态 + consume 处理事件列表 推进 offset 生成记录 + list_records 倒序 limit + 200 条上限 FIFO + MISSING_NAME/INVALID_SOURCE_TYPE/NOT_FOUND/NOT_RUNNING 校验）· ④ 新增 46 测试（16 FileFilter+16 FileTransform+14 StreamingSync+3 单例），全量回归 **2335 passed / 2 pre-existing flaky**（test_usage_prune_old 日期窗口 + test_wiki_version_snapshot_on_approve 50 条上限，均与 W2-AH 无关） · W2+ 中优先级 85/166→88/166 |
| v4.8 | 2026-07-22 | **W2-AI Data Connection 推送与导出组（3 项）**：① #119 Push-based Ingestion（PushIngestionEngine PushIngestionSource id+name+target_stream+auth_type oauth2_client_credentials|api_key|none+auth_config+rate_limit_per_minute+enabled+total_messages+error_count + CRUD register/get/list 按 name+enabled 过滤/update/delete + receive_message 认证+速率校验+计数推进 + receive_batch 混合 accepted/rejected + list_messages 倒序 limit + validate_token 三种认证模式 + 200 条上限 FIFO + MISSING_NAME/INVALID_AUTH_TYPE/INVALID_RATE_LIMIT/NOT_FOUND/SOURCE_DISABLED/AUTH_FAILED/RATE_LIMIT_EXCEEDED/EMPTY_PAYLOAD 校验）· ② #120 Export 文件（FileExportEngine FileExportTask id+name+dataset_rid+target_type s3|abfs|hdfs+target_path+file_format csv|parquet|json|avro+compression none|gzip|snappy|lz4+row_limit+filter_expr+status pending|running|completed|failed+total_rows|exported_rows|file_size_bytes+output_files + CRUD register/get/list 按 dataset_rid+status 过滤/update 仅 pending/delete + start pending→running + cancel running→failed + complete 推进 exported_rows+file_size+output_files + fail 标记失败 + get_progress 百分比 + 200 条上限 FIFO + MISSING_NAME/MISSING_DATASET_RID/INVALID_TARGET_TYPE/INVALID_FORMAT/INVALID_COMPRESSION/NOT_FOUND/TASK_NOT_PENDING/TASK_NOT_RUNNING/ALREADY_COMPLETED 校验）· ③ #121 Export 表（TableExportEngine TableExportTask id+name+source_dataset_rid+target_table+export_mode full|incremental|snapshot+primary_keys+watermark_column+last_watermark+truncate_on_snapshot+status pending|running|completed|failed+processed/inserted/updated/deleted_rows + TableExportRun run_id+task_id+mode+status running|completed|failed+rows_*+watermark_before/after+truncated + CRUD register/get/list 按 dataset_rid+status+mode 过滤/update/delete + start_run running 态+truncate 标记 + complete_run 推进 watermark+累计统计 + fail_run 标记失败 + list_runs 倒序 limit + get_latest_run + incremental 需 watermark 校验 + 200 条上限 FIFO + MISSING_NAME/MISSING_DATASET/INVALID_MODE/INCREMENTAL_REQUIRES_WATERMARK/NOT_FOUND/RUN_NOT_FOUND/RUN_NOT_RUNNING/ALREADY_COMPLETED 校验）· ④ 新增 56 测试（18 PushIngestion+17 FileExport+18 TableExport+3 单例），全量回归 **2391 passed / 2 pre-existing flaky**（同前） · W2+ 中优先级 88/166→91/166 |
| v4.9 | 2026-07-22 | **W2-AJ Data Connection 流导出与 Webhook 组（3 项）**：① #122 Stream Export（StreamExportEngine StreamExportTask id+name+source_stream+target_type kafka|kinesis|pubsub+target_topic+partition_strategy round_robin|key_based|random+key_field+batch_size+status stopped|running|disabled+total_events+last_event_at + StreamExportEvent event_id+key+payload+partition+offset+status pending|sent|failed+sent_at + CRUD register/get/list 按 source_stream+status 过滤/update/delete + start/stop 状态切换 + publish_event 分区计算+计数推进 + publish_batch 批量 + list_events 倒序 limit + 200 条上限 FIFO + MISSING_NAME/MISSING_SOURCE_STREAM/INVALID_TARGET_TYPE/INVALID_PARTITION_STRATEGY/INVALID_BATCH_SIZE/NOT_FOUND/TASK_NOT_STOPPED/TASK_NOT_RUNNING/TASK_DISABLED 校验）· ② #123 Webhook Pipeline（WebhookPipelineEngine WebhookPipeline id+name+description+steps[]+status draft|active|disabled+created_at+updated_at + WebhookPipelineStep step_id+name+url+method GET|POST|PUT|DELETE|PATCH+headers+request_template+auth_type none|api_key|bearer|basic+auth_config+timeout_ms+retry_count+output_mapping+condition_expr + PipelineRun run_id+pipeline_id+status running|completed|failed+started_at+finished_at+current_step+step_results[]+outputs + CRUD register/get/list 按 name+status 过滤/update/delete + add_step/remove_step/reorder_steps 步骤管理 + run 多步执行编排 + list_runs/get_run 执行记录 + 200 条上限 FIFO + MISSING_NAME/EMPTY_STEPS/DUPLICATE_STEP_ID/INVALID_METHOD/INVALID_AUTH_TYPE/INVALID_TIMEOUT/NOT_FOUND/STEP_NOT_FOUND/RUN_NOT_FOUND/PIPELINE_DISABLED/INVALID_ORDER 校验）· ③ #124 Webhook Output（WebhookOutputEngine WebhookOutputConfig id+name+webhook_id+output_fields[]+response_code_field+success_codes[]+error_message_field+created_at+updated_at + OutputFieldMapping field_id+source_path+target_name+target_type string|integer|number|boolean+required+default_value + OutputExtractionResult success+fields{}+missing_required[]+error_message + CRUD register/get/list 按 webhook_id+name 过滤/update/delete + add_field/remove_field 字段管理 + extract 路径提取+类型转换 + validate_response 返回码校验 + 200 条上限 FIFO + MISSING_NAME/MISSING_WEBHOOK/DUPLICATE_FIELD_ID/INVALID_TARGET_TYPE/INVALID_SOURCE_PATH/NOT_FOUND/FIELD_NOT_FOUND 校验）· ④ 新增 61 测试（19 StreamExport+22 WebhookPipeline+17 WebhookOutput+3 单例），全量回归 **2452 passed / 2 pre-existing flaky**（同前：test_usage_prune_old / test_wiki_version_snapshot_on_approve） · W2+ 中优先级 91/166→94/166 |
| v4.10 | 2026-07-22 | **W2-AK Data Connection 安全治理组（3 项）**：① #125 Webhook 执行策略（WebhookExecutionPolicyEngine WebhookExecutionPolicy policy_id+name+webhook_id+max_concurrent+rate_limit_per_minute+timeout_ms+max_retries+retry_backoff_ms+retry_on_status[]+circuit_breaker_enabled+circuit_failure_threshold+circuit_cooldown_ms+status+created_at+updated_at + ExecutionState current_concurrent+window_start+window_count+circuit_state closed|open|half_open+failure_count+total_count+opened_at + ExecutionAttempt attempt_id+call_id+attempt_number+status pending|success|failed|rate_limited|concurrency_limited|circuit_open+http_status+duration_ms+started_at+finished_at+error_message+next_attempt_at + CRUD register/get/list 按 webhook_id+status 过滤/update/delete + acquire_slot 并发+速率+熔断三重检查 + release_slot 释放+推进熔断统计 + record_retry 记录重试+指数退避 + get_execution_state/reset_state + list_attempts 倒序 + trip_circuit/reset_circuit 熔断演练 + 200 条上限 FIFO + MISSING_NAME/MISSING_WEBHOOK/INVALID_CONCURRENCY/INVALID_RATE_LIMIT/INVALID_TIMEOUT/INVALID_RETRY_COUNT/INVALID_THRESHOLD/NOT_FOUND/CONCURRENCY_EXCEEDED/RATE_LIMIT_EXCEEDED/CIRCUIT_OPEN 校验）· ② #126 Egress Policy（EgressPolicyEngine EgressPolicy policy_id+name+description+effect allow|deny+cidr_blocks[]+ports[]+domains[]+protocols[]+priority+status+created_at+updated_at + EgressEvaluation eval_id+policy_id+destination+port+protocol+decision allowed|denied+matched_rules[]+reason+evaluated_at + CRUD register/get/list 按 effect+status 过滤/update/delete + evaluate 按 priority 匹配 AND 多条件 + evaluate_batch 批量 + check_allowed 简化 + list_evaluations + add_cidr/remove_cidr + add_domain/remove_domain + CIDR 支持 IPv4 + 域名支持 *. 通配 + 默认 deny 安全策略 + 200 条上限 FIFO + MISSING_NAME/INVALID_EFFECT/EMPTY_RULES/INVALID_CIDR/INVALID_PORT/INVALID_PROTOCOL/INVALID_PRIORITY/NOT_FOUND 校验）· ③ #127 Exportable Marking（ExportableMarkingEngine ExportableMarkingPolicy policy_id+name+connection_id+marking_level public|internal|restricted|confidential+export_action allow|deny|mask|redact+mask_character+redact_text+affected_columns[]+affected_markings[]+priority+status+created_at+updated_at + MarkingEvaluation eval_id+policy_id+connection_id+column_name+markings[]+decision allowed|denied|masked|redacted+masked_value+reason+evaluated_at + CRUD register/get/list 按 connection_id+status+marking_level 过滤/update/delete + evaluate 按 priority 匹配 + evaluate_row 多列批量 + can_export 简化 + list_evaluations + add/remove_affected_column + add/remove_affected_marking + 无匹配默认 allow + 200 条上限 FIFO + MISSING_NAME/MISSING_CONNECTION/INVALID_MARKING_LEVEL/INVALID_EXPORT_ACTION/INVALID_PRIORITY/NOT_FOUND 校验）· ④ 新增 68 测试（27 ExecutionPolicy+21 EgressPolicy+20 ExportableMarking+3 单例），全量回归 **2520 passed / 2 pre-existing flaky**（同前） · W2+ 中优先级 94/166→97/166 |
| v4.11 | 2026-07-22 | **W2-AL Data Lineage 组（3 项）**：① #130 血缘可视化（LineageVisualizationEngine LineageView view_id+name+description+root_dataset_rid+graph_mode graph|tree+direction upstream|downstream|both+depth+layout horizontal|vertical|radial+color_by type|health|status|owner+collapsed_nodes[]+highlighted_nodes[]+saved_by+is_public+created_at+updated_at + LineageGraphNode node_id+label+node_type+health_status+color+x+y + LineageGraphEdge edge_id+source+target+label+edge_type + LineageGraph view_id+nodes[]+edges[]+stats{} + CRUD register/get/list saved_by+graph_mode 过滤/update/delete + generate_graph 模拟深度生成节点边 + expand_node/collapse_node 节点折叠 + color_by 按规则着色 + share_view 切换公开私有 + list_views_by_dataset 按数据集列视图 + 200 条上限 FIFO + MISSING_NAME/MISSING_DATASET/INVALID_GRAPH_MODE/INVALID_DIRECTION/INVALID_LAYOUT/INVALID_DEPTH/INVALID_COLOR_BY/NOT_FOUND 校验）· ② #131 列级血缘增量（ColumnLineageSearchEngine 增量：CRUD 已由 W2-E #4 交付；新增 ColumnIndexEntry dataset_rid+column_name+data_type+description+tags[]+last_updated + ColumnTraceStep dataset_rid+column_name+transform_expr+direction + ColumnTraceResult column+dataset_rid+direction+depth+path[] + register_column/get_column/list_columns/update_column/delete_column CRUD + search_columns 关键词模糊+类型+标签过滤 + trace_column 上下游追踪 + build_index 重建索引 + 200 条上限 FIFO + MISSING_DATASET/MISSING_COLUMN/INVALID_DIRECTION/INVALID_DEPTH/NOT_FOUND 校验）· ③ #132 搭建时间线（LineageBuildTimelineEngine BuildSchedule schedule_id+name+pipeline_id+cron_expression+timezone+status active|paused|disabled+last_run_at+next_run_at+created_at+updated_at + BuildRun run_id+schedule_id+status pending|running|success|failed|cancelled+started_at+finished_at+datasets_built[]+duration_ms+error_message + GanttTask task_id+name+pipeline_id+start_time+end_time+status+dependencies[] + GanttChart chart_id+title+start_date+end_date+tasks[] + CRUD register/get/list pipeline_id+status 过滤/update/delete_schedule + compute_next_run 5 段 cron 解析 + trigger_run 检查 active + complete_run + get_run/list_runs + pause_schedule/resume_schedule + get_gantt_chart 按日期范围生成 + 200 条上限 FIFO + MISSING_NAME/MISSING_PIPELINE/INVALID_CRON/INVALID_TIMEZONE/INVALID_STATUS/NOT_FOUND/SCHEDULE_PAUSED/RUN_NOT_FOUND/RUN_NOT_RUNNING 校验）· ④ 新增 60 测试（18 LineageVisualization+18 ColumnLineageSearch+21 BuildTimeline+3 单例），全量回归 **2580 passed / 2 pre-existing flaky**（同前） · W2+ 中优先级 97/166→100/166 |
| v4.12 | 2026-07-23 | **W2-AM Data Health 增强组（3 项）**：① #136 检查组诊断（HealthDiagnosticsEngine HealthDiagnosticsReport report_id+group_id+generated_at+total_checks+passed/failed/warning_count+failed_checks[]+focus_summary+grouping_strategy by_severity|by_type|by_dataset + FailedCheckDetail check_id+check_name+check_kind+severity+dataset_rid+failure_message+last_run_at + generate_diagnostics 生成报告+模拟失败检查 + get_report/list_reports 按 group_id 过滤 + get_failed_checks severity 过滤 + get_focus_summary 失败聚焦摘要 + list_checks_by_group 检查列表 + 200 条上限 FIFO + MISSING_GROUP/INVALID_GROUPING/INVALID_SEVERITY/NOT_FOUND 校验）· ② #137 监测选项（HealthMonitoringOptionsEngine HealthMonitoringOptions options_id+dataset_rid+notification_mode none|all_failures|only_severe+channels[] email|slack|inapp+reminder_interval_minutes+auto_resolve+created_at+updated_at + CRUD register/get/get_by_dataset/list 按 dataset_rid 过滤/update/delete + set_notification_mode 模式切换 + add_channel/remove_channel 渠道管理 + 200 条上限 FIFO + MISSING_DATASET/INVALID_NOTIFICATION_MODE/INVALID_CHANNEL/INVALID_INTERVAL/NOT_FOUND/CHANNEL_NOT_FOUND 校验）· ③ #138 平台内通知（HealthNotificationEngine HealthNotification notification_id+dataset_rid+check_id+check_name+severity critical|warning|info+title+message+status unread|read|cleared+created_at+read_at+cleared_at+user_id + create/get/list 按 user_id+status+severity 过滤 + mark_read/mark_all_read + clear/clear_all + get_unread_count 按 severity 分组统计 + list_by_dataset + 200 条上限 FIFO + MISSING_USER/MISSING_DATASET/INVALID_SEVERITY/INVALID_STATUS/NOT_FOUND 校验）· ④ 新增 56 测试（16 Diagnostics+19 MonitoringOptions+18 Notifications+3 单例），全量回归 **2636 passed / 2 pre-existing flaky**（同前） · W2+ 中优先级 100/166→103/166 |
| v4.13 | 2026-07-23 | **W2-AN Data Health 集成组（3 项）**：① #139 Issues 集成（HealthIssuesIntegrationEngine HealthIssue issue_id+dataset_rid+check_id+check_name+severity critical|warning|info+title+description+status open|in_progress|resolved|closed+created_at+updated_at+resolved_at+created_by_check+linked_check_runs[] + create_issue/get_issue/list_issues 按 dataset_rid+status+severity 过滤 + update_issue + resolve_issue/close_issue 状态推进 + auto_create_from_check 检查失败自动创建 [SEVERITY] check_name failed on dataset_rid 标题模板 + auto_resolve_from_check 检查通过自动解决（无候选返回 None） + link_check_run 关联检查运行记录幂等去重 + 200 条上限 FIFO + MISSING_DATASET/MISSING_CHECK/INVALID_SEVERITY/INVALID_STATUS/NOT_FOUND 校验）· ② #140 数据集健康 Tab（DatasetHealthTabEngine DatasetHealthTab tab_id+dataset_rid+overall_status healthy|warning|critical|unknown+checks_summary{}+last_check_at+recommendations[]+trends[]+created_at+updated_at + register 幂等 + get/get_by_dataset/list 按 dataset_rid 过滤 + update_status 状态+检查摘要+last_check_at 推进 + add_recommendation 幂等去重 + add_trend 趋势点追加 + get_overall_health 整体状态摘要 + delete 级联清理 _dataset_index + 200 条上限 FIFO + MISSING_DATASET/INVALID_STATUS/NOT_FOUND 校验）· ③ #141 沿袭健康着色（LineageHealthColoringEngine LineageHealthColor color_id+dataset_rid+health_status healthy|warning|critical|unknown+color_code green|yellow|red|gray+display_name+tooltip+updated_at + LineageColoringConfig config_id+name+color_scheme traffic_light|custom+status_color_mapping{}+default_color+created_at+updated_at + register_color/get_color/list_colors status_filter 过滤 + update_color/delete_color + register_config 默认填充 traffic_light mapping + get_config/list_configs + apply_coloring 按 config.status_color_mapping 批量着色（unknown→default_color 回退） + 200 条上限 FIFO + MISSING_DATASET/MISSING_NAME/INVALID_HEALTH_STATUS/INVALID_COLOR_CODE/INVALID_COLOR_SCHEME/NOT_FOUND/CONFIG_NOT_FOUND 校验）· ④ 新增 55 测试（18 IssuesIntegration+16 DatasetHealthTab+18 LineageColoring+3 单例），全量回归 **2691 passed / 2 pre-existing flaky**（同前：test_usage_prune_old 日期窗口 + test_wiki_version_snapshot_on_approve 50 条上限，均与 W2-AN 无关） · W2+ 中优先级 103/166→106/166 |
| v4.14 | 2026-07-23 | **W2-AO Functions Dev Tools + Dataset Preview Tabs（3 新增 + 1 清账）**：① #143 Functions 测试调试（FunctionsTestDebugEngine FunctionTestCase case_id+function_id+test_name+language python|typescript+test_code+assertions[]+status pending|passed|failed|error + FunctionDebugSession session_id+function_id+inputs+breakpoints+state created|running|paused|completed|error+current_line+variables + ProfileResult profile_id+function_id+duration_ms+memory_bytes+cpu_percent+call_count+hotspots[] + register_test/get_test/list_tests 按 function_id+status 过滤 + run_test python 含 assert 且不含 fail→passed/含 fail→failed/typescript→passed + register_debug/start_debug（created→running ALREADY_STARTED）/step（current_line+1/断点→paused/≥10→completed/非 running|paused→INVALID_STATE） + profile 模拟性能指标 + list_profiles + 200 条上限 FIFO + MISSING_FUNCTION/MISSING_NAME/INVALID_LANGUAGE/NOT_FOUND 校验）· ② #144 Functions 外部API调用（ExternalApiCallEngine ExternalApiCall call_id+name+language typescript|python+endpoint_url+method GET|POST|PUT|PATCH|DELETE+auth_type none|bearer|basic|api_key+status active|inactive + CallResult result_id+call_id+status success|failed+status_code+response_body+duration_ms + register/get/list 按 language+status 过滤/update/delete + execute 模拟 status_code=200/response_body={"ok":true,"echo":<payload>} + list_results + enable/disable + 200 条上限 FIFO + MISSING_NAME/MISSING_URL/INVALID_LANGUAGE/INVALID_METHOD/INVALID_AUTH_TYPE/NOT_FOUND 校验）· ③ #146 Dataset Preview 详情Tabs（DatasetPreviewTabsEngine DatasetPreviewTabs tabs_id+dataset_rid+history_tab+health_tab+comparison_tab+stream_view_tab + HistoryTab/HealthTab/ComparisonTab/StreamViewTab 四子模型 + register 幂等 + get/get_by_dataset/list + enable_tab/disable_tab（tab_name history|health|comparison|stream_view）+ update_history/health/comparison/stream_view_tab 四 Tab 更新 + 200 条上限 FIFO（淘汰时清理 _dataset_index）+ MISSING_DATASET/INVALID_TAB_NAME/INVALID_HEALTH_STATUS/INVALID_COMPARE_MODE/INVALID_STREAM_TYPE/INVALID_STREAM_STATUS/NOT_FOUND 校验）· ④ #145 Interfaces 定义/继承 清账（确认与 W2-K #32 Ontology Interface 同一能力，InterfaceEngine 已在 v2.4 完全交付 CRUD+extends 继承+implement 实现+effective_properties 多态+删除保护 STILL_EXTENDED/STILL_IMPLEMENTED）· ⑤ 新增 76 测试（27 FunctionsTestDebug+22 ExternalApiCall+24 DatasetPreviewTabs+3 单例），全量回归 **2767 passed / 2 pre-existing flaky**（同前） · W2+ 中优先级 106/166→110/166 |
| v4.15 | 2026-07-23 | **W2-AP Compute Module 组（3 项）**：① #148 Compute Scheduler（ComputeSchedulerEngine ComputeModule module_id+name+image+status pending|running|stopped|failed+container_id+started_at+last_heartbeat_at+error_message+created_at+updated_at + register/get/list 按 status 过滤 + start pending→running 生成 container_id 推进 started_at/last_heartbeat_at + stop running→stopped + restart 仅 running 可重启 换 container_id + heartbeat 推进 last_heartbeat_at + fail 标记失败 + remove 删除 + 200 条上限 FIFO + MISSING_NAME/MISSING_IMAGE/NOT_FOUND/INVALID_TRANSITION/NOT_RUNNING 校验）· ② #149 Compute Scaler（ComputeScalerEngine ScalePolicy policy_id+module_id+target_concurrency+scale_up_threshold 0.8+scale_down_threshold 0.3+min_replicas+max_replicas+status active|inactive + Replica replica_id+policy_id+module_id+status pending|healthy|unhealthy + register_policy/get_policy/list_policies 按 module_id 过滤 + update_policy 状态+阈值+副本数 + delete_policy + evaluate_scale 按 concurrency 比率判定 scale_up/scale_down/none + scale_up 批量创建副本 count≥1 + scale_down 批量标记 unhealthy count≥1 + list_replicas 按 module_id+status 过滤 + mark_replica_unhealthy + 200 条上限 FIFO + MISSING_MODULE/INVALID_MIN_REPLICAS/INVALID_MAX_REPLICAS/INVALID_STATUS/POLICY_INACTIVE/INVALID_COUNT/NOT_FOUND 校验）· ③ #150 Compute Resource（ComputeResourceEngine ResourceQuota quota_id+module_id+cpu_milli+memory_mib+gpu_count+storage_mib+ephemeral_mib+created_at+updated_at + register 幂等校验 + get/get_by_module/list 按 module_id 过滤 + update/delete + check_quota 资源是否超限 + list_over_quota 超限列表 + 200 条上限 FIFO（淘汰时清理 _module_index）+ MISSING_MODULE/INVALID_CPU/INVALID_MEMORY/INVALID_GPU/INVALID_STORAGE/DUPLICATE_MODULE/NOT_FOUND 校验）· ④ 新增 85 测试（24 ComputeScheduler+30 ComputeScaler+28 ComputeResource+3 单例），全量回归 **2852 passed / 2 pre-existing flaky**（同前：test_usage_prune_old 日期窗口 + test_wiki_version_snapshot_on_approve 50 条上限，均与 W2-AP 无关） · W2+ 中优先级 110/166→113/166 |
| v4.16 | 2026-07-23 | **W2-AQ Workshop 变量 + Compute API + app.py 约定组（3 项）**：① #147 Workshop 变量联动（WorkshopVariableEngine WorkshopVariable var_id+name+var_type object_set/object_set_filter/string/numeric/boolean/date/timestamp/array/struct/geopoint/geoshape/time_series_set 11 种+definition_type static/function/object_set_aggregation/object_property/object_set_definition/variable_transformation 6 种+recompute_strategy automatic/triggered/on_load+lazy+module_id+status + VariableEvent event_id+var_id+event_type+payload + register 校验 MISSING_NAME/INVALID_VAR_TYPE/INVALID_DEFINITION_TYPE/INVALID_RECOMPUTE_STRATEGY/DEPENDENCY_NOT_FOUND + get/list 按 var_type+definition_type+module_id 过滤 + update/delete（级联清理 depends_on 引用）+ evaluate static 返回 value/function 模拟 func_result_{var_id}/variable_transformation BFS 递归解析依赖（visited 防环 CIRCULAR_DEPENDENCY） + resolve_dependencies BFS 上游 + get_lineage upstream/downstream + record_event/list_events + 200 条上限 FIFO + MISSING_NAME/INVALID_VAR_TYPE/INVALID_DEFINITION_TYPE/INVALID_RECOMPUTE_STRATEGY/DEPENDENCY_NOT_FOUND/CIRCULAR_DEPENDENCY/NOT_FOUND 校验）· ② #151 Compute Module API job 长轮询（ComputeJobPollingEngine ComputeJob job_id+module_id+function_name+payload+status queued|running|succeeded|failed|timeout+result+error+polling_token+poll_count+created_at+started_at+finished_at+last_polled_at+timeout_seconds + submit 校验 MISSING_MODULE/MISSING_FUNCTION 生成 job-id=job-*+polling_token=pt-* + get/list 按 module_id+status 过滤 + poll 校验 INVALID_TOKEN queued→running 推进 started_at running→succeeded 推进 finished_at+result poll_count+1 last_polled_at 推进 terminal 不变 + get_result succeeded 返回 result 否则 JOB_NOT_COMPLETED + cancel queued|running→failed error=cancelled 否则 ALREADY_TERMINAL + check_timeouts running 超过 timeout_seconds→timeout + 200 条上限 FIFO + MISSING_MODULE/MISSING_FUNCTION/INVALID_TOKEN/JOB_NOT_COMPLETED/ALREADY_TERMINAL/NOT_FOUND 校验）· ③ #152 app.py 入口约定（AppEntryConventionEngine AppEntry entry_id+module_id+function_name+endpoint_path+relative_imports[]+json_serializable+signature_params[]+return_type+status valid|invalid+validation_errors[] + register 校验 MISSING_MODULE/MISSING_FUNCTION 生成 entry-id=entry-* + 派生 endpoint_path snake_case 下划线→斜杠 如 get_user_data→/get/user/data + _validate relative_imports 每项须以 . 开头 否则 non-relative import 错误 return_type 须在 dict|list|str|int|float|bool|None|空 中 否则 non-json-serializable 错误 json_serializable=False + get/list 按 module_id+status 过滤 + validate 重新校验 + list_invalid + update/delete + get_endpoint + 200 条上限 FIFO + MISSING_MODULE/MISSING_FUNCTION/NOT_FOUND 校验）· ④ 新增 67 测试（25 WorkshopVariable+21 ComputeJobPolling+18 AppEntryConvention+3 单例），全量回归 **2897 passed / 3 pre-existing flaky + 5 pre-existing collection errors**（test_usage_prune_old 日期窗口 + test_wiki_version_snapshot_on_approve 50 条上限 + test_jwks_and_rs256_me 500 错误 + 5 collection errors JWKS/marking/vector Python 版本兼容 dict|None 语法，均与 W2-AQ 无关） · W2+ 中优先级 113/166→116/166 |
| v4.17 | 2026-07-23 | **W2-AR Integration 框架 + Pipeline 维护 + Interface 扩展组（3 项）**：① #161 Data Integration 统一框架（DataIntegrationFrameworkEngine IntegrationFramework framework_id+name+description+connection_id+transform_id+management_config+status active + register 校验 MISSING_NAME + get/list 按 status 过滤 + update/delete + link_connection/link_transform + get_summary 返回 has_connection/has_transform/has_management/completeness empty|partial|full + 200 条上限 FIFO + MISSING_NAME/NOT_FOUND 校验）· ② #162 管道维护与监控（PipelineMaintenanceEngine PipelineHealthCheck check_id+pipeline_id+check_type+status pass|fail|warning+severity info|warning|critical+message+last_run_at + DataExpectation expectation_id+pipeline_id+delivery_cycle+build_frequency+data_expiry_threshold_hours + StabilitySuggestion suggestion_id+pipeline_id+suggestion_type+priority low|medium|high+description + register_check/get_check/list_checks 按 pipeline_id+status 过滤/update_check/delete_check/list_failing_checks + register_expectation/get_expectation/list_expectations/update_expectation/delete_expectation + register_suggestion/get_suggestion/list_suggestions 按 pipeline_id+priority 过滤/delete_suggestion + monitor_pipeline 返回 total_checks/failing_checks/has_expectation/suggestions_count/health_status healthy|degraded|critical + 200 条上限 FIFO + MISSING_PIPELINE/MISSING_CHECK_TYPE/INVALID_STATUS/INVALID_SEVERITY/MISSING_SUGGESTION_TYPE/INVALID_PRIORITY/NOT_FOUND 校验）· ③ #163 Ontology Interfaces 增量（OntologyInterfaceExtensionEngine：W2-K #32 InterfaceEngine 已覆盖接口定义/继承/实现/多态；本批补齐 InterfaceLinkType link_type_id+name+source_interface_id+target_interface_id+cardinality one_to_one|one_to_many|many_to_many+description + CRUD register/get/list 按 source_interface_id 过滤/update/delete + InterfaceMarketplaceListing listing_id+interface_id+title+description+version+publisher+status draft|published|imported+published_at + CRUD register/get/list 按 status 过滤/publish_to_marketplace draft→published 推进 published_at/import_from_marketplace 创建 status=imported/update/delete + 200 条上限 FIFO + MISSING_NAME/MISSING_SOURCE_INTERFACE/MISSING_TARGET_INTERFACE/INVALID_CARDINALITY/MISSING_INTERFACE/MISSING_TITLE/INVALID_STATUS/NOT_FOUND 校验）· ④ 新增 66 测试（16 DataIntegration+26 PipelineMaintenance+21 InterfaceExtension+3 单例），全量回归 **2963 passed / 3 pre-existing flaky + 5 pre-existing collection errors**（同前，均与 W2-AR 无关） · W2+ 中优先级 116/166→119/166 |
| v4.18 | 2026-07-23 | **W2-AS 时间序列 + SAP 集成 + pb-functions 函数库组（3 项）**：① #164 时间序列（TimeSeriesEngine TimeSeriesObject ts_id+name+object_type TSP+description+sync_index_status pending|indexing|ready+created_at+updated_at + Sensor sensor_id+name+ts_object_id+data_type numeric+unit+frequency_seconds+status active + TimeSeriesPoint point_id+sensor_id+timestamp+value+created_at + register_object/get_object/list_objects 按 object_type 过滤/update_object/delete_object/build_sync_index pending→indexing→ready + register_sensor/get_sensor/list_sensors 按 ts_object_id+status 过滤/update_sensor/delete_sensor + ingest_points 批量写入/list_points 按 sensor_id limit/get_latest_point 返回最新点 + 200 条上限 FIFO + MISSING_NAME/INVALID_OBJECT_TYPE/MISSING_TS_OBJECT/INVALID_DATA_TYPE/INVALID_FREQUENCY/INVALID_STATUS/NOT_FOUND 校验）· ② #165 SAP 集成（SapIntegrationEngine SapConnection conn_id+name+system_type S4HANA|ECC|BW|SLT+host+port+client+auth_type basic|certificate|snc+username+status disconnected|connected + SapImportJob job_id+conn_id+object_type table|bapi|cds|info_provider|bex_query|extractor+source_object+target_dataset+status pending|running|completed|failed+total_rows+imported_rows+error + register_connection/get_connection/list_connections 按 system_type+status 过滤/update_connection/delete_connection/test_connection disconnected→connected + create_import_job/get_import_job/list_import_jobs 按 conn_id+status 过滤/run_import_job pending→running→completed/cancel_import_job running→failed + 200 条上限 FIFO + MISSING_NAME/MISSING_HOST/INVALID_SYSTEM_TYPE/INVALID_AUTH_TYPE/MISSING_CONNECTION/MISSING_SOURCE_OBJECT/INVALID_OBJECT_TYPE/ALREADY_RUNNING/NOT_FOUND 校验）· ③ #166 pb-functions 函数库（PbFunctionsEngine PbFunction func_id+name+category expression|transform|ai+signature+description+return_type+version + PbFunctionCategory category_id+name+description+function_count + register_function/get_function/list_functions 按 category 过滤/search_functions 关键词模糊/update_function/delete_function + register_category/get_category/list_categories/delete_category + 200 条上限 FIFO + MISSING_NAME/INVALID_CATEGORY/NOT_FOUND 校验）· ④ 新增 59 测试（22 TimeSeries+18 SapIntegration+16 PbFunctions+3 单例），全量回归 **3022 passed / 3 pre-existing flaky + 5 pre-existing collection errors**（同前，均与 W2-AS 无关） · W2+ 中优先级 119/166→122/166 |
| v4.19 | 2026-07-23 | **W2-AT Compute Module 容器生态完善组（3 项）**：① #155 Configure/Query/Overview 三标签页（ContainerConfigEngine ContainerTabConfig tab_config_id+module_id+tab_name configure|query|overview+config_data dict+status active|inactive+created_at+updated_at + register_config/get_config/list_configs 按 module_id+tab_name+status 过滤/update_config/delete_config + get_module_overview 聚合返回模块三标签配置汇总 + 200 条上限 FIFO + MISSING_MODULE/MISSING_TAB_NAME/INVALID_TAB_NAME/INVALID_STATUS/NOT_FOUND 校验）· ② #156 缩容至零+冷启动告警（ScaleToZeroEngine ScaleToZeroPolicy policy_id+module_id+idle_timeout_seconds+min_replicas+scale_up_delay_seconds+status active|inactive+created_at + ColdStartAlert alert_id+module_id+alert_type cold_start|scale_up+wait_duration_ms+severity info|warning+cleared+created_at + register_policy/get_policy/list_policies 按 module_id+status 过滤/update_policy/delete_policy + trigger_alert/list_alerts 按 module_id+alert_type+cleared 过滤/clear_alert + simulate_cold_start 返回模拟延迟 ms + 200 条上限 FIFO + MISSING_MODULE/INVALID_IDLE_TIMEOUT/INVALID_MIN_REPLICAS/INVALID_SCALE_UP_DELAY/INVALID_STATUS/INVALID_ALERT_TYPE/NOT_FOUND 校验）· ③ #157 本地开发脚手架（DevScaffoldEngine ScaffoldTemplate template_id+language python|typescript+name+description+file_templates[]（ScaffoldFile filename+content）+created_at+updated_at + GeneratedScaffold scaffold_id+module_id+template_id+rendered_files[]+status generated|applied+created_at + register_template/get_template/list_templates 按 language 过滤/update_template/delete_template + generate_scaffold 填充 {{var}} 占位符/get_scaffold/list_scaffolds 按 module_id+status 过滤/apply_scaffold generated→applied + 内置 3 默认模板 python_compute_module/typescript_compute_module/python_ml_module + 200 条上限 FIFO + MISSING_NAME/MISSING_MODULE/INVALID_LANGUAGE/TEMPLATE_NOT_FOUND/SCAFFOLD_NOT_FOUND/NOT_FOUND 校验）· ④ 新增 67 测试（19 ContainerConfig+20 ScaleToZero+18 DevScaffold+3 单例），全量回归 **3089 passed / 3 pre-existing flaky + 5 pre-existing collection errors**（同前，均与 W2-AT 无关） · W2+ 中优先级 122/166→125/166 |
| v4.20 | 2026-07-23 | **W2-AU Compute Module 发布与访问生态组（3 项）**：① #153 meta.yaml 依赖+gradle.properties（BuildConfigEngine BuildConfig config_id+module_id+base_image_tag+dependencies[]+gradle_properties dict+status active|inactive+created_at+updated_at + register_config/get_config/get_by_module/list_configs 按 module_id+status 过滤/update_config/delete_config + validate_base_image_tag semver 数值比较 ≥0.15.0 + 200 条上限 FIFO + MISSING_MODULE/MISSING_BASE_IMAGE_TAG/INVALID_BASE_IMAGE_TAG/NOT_FOUND 校验）· ② #154 Docker 镜像发布（DockerPublishEngine DockerImage image_id+module_id+tag+repository_url+status pending|building|published|failed+size_bytes+published_at+error_message+created_at+updated_at + register_image/get_image/list_images 按 module_id+status 过滤/update_image/delete_image + build_image pending→building/publish_image building→published（校验 tag≠latest 否则 INVALID_TAG）/fail_image building→failed + 200 条上限 FIFO + MISSING_MODULE/MISSING_TAG/INVALID_TAG/INVALID_STATUS/NOT_FOUND 校验）· ③ #158 External access（ExternalAccessEngine ExternalAccessConfig config_id+module_id+access_type foundry_data|foundry_service|external_domain+domain+port+path_prefix+auth_type none|bearer|api_key+auth_config dict+status active|inactive+created_at+updated_at + register_config/get_config/list_configs 按 module_id+access_type+status 过滤/update_config/delete_config + test_connectivity 返回 ok+latency_ms 模拟 + 200 条上限 FIFO + MISSING_MODULE/MISSING_DOMAIN/INVALID_ACCESS_TYPE/INVALID_PORT/INVALID_STATUS/NOT_FOUND 校验）· ④ 新增 57 测试（18 BuildConfig+19 DockerPublish+17 ExternalAccess+3 单例），全量回归 **3146 passed / 3 pre-existing flaky + 5 pre-existing collection errors**（同前，均与 W2-AU 无关） · W2+ 中优先级 125/166→128/166 |
| v4.21 | 2026-07-23 | **W2-AV 平台集成完善组（3 项）**：① #142 Data Health 应用入口（HealthAppEngine HealthAppEntry entry_id+app_name+icon+path+category data_health|monitoring|governance+permissions[]+status active|inactive+order_index+created_at+updated_at + register_entry/get_entry/list_entries 按 category+status 过滤/update_entry/delete_entry 返回 bool/reorder_entries/get_sidebar_items 按 order_index 排序返回 active 条目 + 200 条上限 FIFO + MISSING_APP_NAME/MISSING_PATH/INVALID_CATEGORY/INVALID_STATUS/NOT_FOUND 校验）· ② #159 Functions/Workshop/Slate 集成（FunctionIntegrationEngine FunctionIntegration integration_id+module_id+function_id+backend_type python|typescript|container+trigger_type workshop|slate|direct+trigger_config dict+endpoint_url+status active|inactive+created_at+updated_at + register_integration/get_integration/list_integrations 按 module_id+backend_type+trigger_type+status 过滤/update_integration/delete_integration 返回 bool/invoke 模拟调用返回结果 dict/list_by_function + 200 条上限 FIFO + MISSING_MODULE/MISSING_FUNCTION/MISSING_BACKEND_TYPE/INVALID_BACKEND_TYPE/INVALID_TRIGGER_TYPE/INVALID_STATUS/NOT_FOUND 校验）· ③ #160 Ferry 增量包（FerryPackageEngine FerryPackage package_id+source_dataset_rid+target_dataset_rid+package_type incremental|full+change_count+status pending|packaging|ready|failed+size_bytes+checksum+created_at+completed_at + create_package/get_package/list_packages 按 source_dataset_rid+target_dataset_rid+package_type+status 过滤/update_package/delete_package 返回 bool/build_package pending→packaging→ready/fail_package packaging→failed/apply_package ready→返回应用结果 + 200 条上限 FIFO + MISSING_SOURCE/MISSING_TARGET/INVALID_PACKAGE_TYPE/INVALID_STATUS/NOT_FOUND 校验）· ④ 新增 61 测试（18 HealthApp+20 FunctionIntegration+18 FerryPackage+3 单例），全量回归 **3207 passed / 3 pre-existing flaky + 5 pre-existing collection errors**（同前，均与 W2-AV 无关） · W2+ 中优先级 128/166→131/166 |
| v4.22 | 2026-07-23 | **W2-AW Data Connection 身份+虚拟表+Agent指标组（3 项）**：① #128 Data Connection OIDC/Cloud Identity（CloudIdentityEngine CloudIdentity identity_id+name+cloud_provider aws|azure|gcp+connection_type openid_connect|oauth2|saml+client_id+client_secret+tenant_id+redirect_uri+scopes[]+status active|inactive+created_at+updated_at + OutboundApp app_id+name+identity_id+target_url+auth_method header|query_param|body+status+created_at + CRUD register_identity/get_identity/list_identities 按 cloud_provider+status 过滤/update_identity/delete_identity + register_app/get_app/list_apps 按 identity_id 过滤/update_app/delete_app + validate_identity 校验 client_id+tenant_id+ 200 条上限 FIFO + MISSING_NAME/INVALID_PROVIDER/INVALID_CONNECTION_TYPE/MISSING_IDENTITY/NOT_FOUND 校验）· ② #129 Data Connection 虚拟表（VirtualTableEngine VirtualTable table_id+name+source_connection_id+source_schema+source_table+column_mappings[]+sync_mode snapshot|incremental+refresh_schedule+last_sync_at+status active|inactive+created_at+updated_at + ColumnMapping column_name+source_type+target_type+is_primary_key+nullable + CRUD register_table/get_table/list_tables 按 source_connection_id+sync_mode+status 过滤/update_table/delete_table + sync_table 推进 last_sync_at + validate_mappings 主键校验+类型映射校验 + 200 条上限 FIFO + MISSING_NAME/MISSING_CONNECTION/EMPTY_MAPPINGS/INVALID_SYNC_MODE/INVALID_STATUS/NOT_FOUND 校验）· ③ #5 Agent Metrics（AgentMetricsEngine AgentMetrics metrics_id+agent_id+memory_usage_mb+disk_usage_gb+cpu_load_percent+queue_depth+recorded_at+status ok|warning|critical+expires_at + AgentMetricsSummary agent_id+latest_memory+latest_disk+latest_cpu+latest_queue+record_count+last_recorded_at + CRUD record_metrics/get_metrics/list_metrics 按 agent_id+status 过滤/update_metrics/delete_metrics + get_summary 聚合最新指标 + get_expiring 按 expires_at 过滤 + validate_config 校验 memory/disk/cpu≥0 + 200 条上限 FIFO + MISSING_AGENT/INVALID_METRICS/NOT_FOUND 校验）· ④ 新增 56 测试（18 CloudIdentity+20 VirtualTable+18 AgentMetrics+3 单例），全量回归 **3263 passed / 3 pre-existing flaky + 5 pre-existing collection errors**（同前，均与 W2-AW 无关） · W2+ 中优先级 131/166→134/166 |
| v4.23 | 2026-07-23 | **W2-AX Dataset Preview 列统计+附加视图+Data Health组（3 项）**：① #21 Dataset Preview 列统计（ColumnStatsEngine ColumnStats stats_id+dataset_rid+column_name+null_count+null_percent+distinct_count+distinct_percent+min_value+max_value+mean+median+std_dev+sample_values+data_type+total_rows+last_computed_at + compute_stats 生成 stats_id=cs-* + get_stats + list_stats 按 dataset_rid+column_name+data_type 过滤 + delete_stats + 200 条上限 FIFO + MISSING_DATASET/MISSING_COLUMN/NOT_FOUND 校验）· ② #22 Dataset Preview 附加视图（DatasetPreviewViewsEngine PreviewView view_id+dataset_rid+view_type table|chart|profile|comparison+config_data+enabled+created_at+updated_at + register_view 生成 view_id=pv-* + get_view + list_views 按 dataset_rid+view_type+enabled 过滤 + update_view + delete_view + 200 条上限 FIFO + MISSING_DATASET/INVALID_VIEW_TYPE/NOT_FOUND 校验）· ③ #26 Data Health（DataHealthCheckEngine DataHealthCheck check_id+dataset_rid+check_type freshness|volume|schema|nulls|uniqueness|range+config+status pending|running|passed|failed|errored+last_run_at+last_result+severity critical|warning|info+created_at+updated_at + register_check 生成 check_id=hc-* + get_check + list_checks 按 dataset_rid+check_type+status+severity 过滤 + update_check + delete_check + run_check 模拟运行推进 last_run_at+last_result + 200 条上限 FIFO + MISSING_DATASET/INVALID_CHECK_TYPE/INVALID_STATUS/INVALID_SEVERITY/NOT_FOUND 校验）· ④ 新增 63 测试（18 ColumnStats+21 PreviewViews+24 DataHealthCheck+3 单例），全量回归 **3325 passed / 4 pre-existing flaky + 5 pre-existing collection errors**（新增 test_wiki_version_snapshot_on_approve 50 条上限 flaky + test_jwks_and_rs256_me cryptography 缺失 500 错误，均与 W2-AX 无关） · W2+ 中优先级 134/166→137/166 |
| v4.24 | 2026-07-23 | **W2-AY Connection CDC+Schedule触发+存储路由向导组（3 项）**：① #1 Connection CDC（ConnectionCdcEngine CdcConfig cdc_id+connection_id+enabled+capture_mode full|incremental|snapshot+snapshot_interval_hours+max_backlog_records+last_capture_at+status running|stopped|paused|error+error_message+created_at+updated_at + configure_cdc 生成 cdc-* + get_cdc + list_cdc 按 connection_id+status 过滤 + update_cdc + delete_cdc + toggle_cdc + 200 条上限 FIFO + MISSING_CONNECTION/INVALID_CAPTURE_MODE/INVALID_STATUS/NOT_FOUND 校验）· ② #4 Schedule 触发机制（ScheduleTriggerEngine ScheduleTrigger trigger_id+name+cron_expression+timezone+enabled+target_type pipeline|workflow|function+target_id+last_triggered_at+next_trigger_at+status active|inactive|paused+created_at+updated_at + create_trigger 生成 str-* + get_trigger + list_triggers 按 name+target_type+target_id+status 过滤 + update_trigger + delete_trigger + toggle_trigger + 200 条上限 FIFO + MISSING_NAME/INVALID_CRON/INVALID_TARGET_TYPE/INVALID_STATUS/NOT_FOUND 校验）· ③ #14 存储路由向导（StorageRouteGuideEngine StorageRoute route_id+name+source_path+target_path+route_type copy|move|sync|mirror+schedule_type on_demand|periodic|event+schedule_cron+enabled+status active|inactive|running|completed|failed+last_run_at+error_message+created_at+updated_at + create_route 生成 srg-* + get_route + list_routes 按 name+route_type+schedule_type+status 过滤 + update_route + delete_route + execute_route 模拟运行 running→completed + 200 条上限 FIFO + MISSING_NAME/MISSING_SOURCE_PATH/MISSING_TARGET_PATH/INVALID_ROUTE_TYPE/INVALID_SCHEDULE_TYPE/NOT_FOUND 校验）· ④ 新增 70 测试（19 ConnectionCdc+22 ScheduleTrigger+29 StorageRouteGuide），全量回归 **3396 passed / 3 pre-existing failed + 5 pre-existing errors**（同前：test_usage_prune_old/test_wiki_version_snapshot_on_approve/test_jwks_and_rs256_me + 5 collection errors，均与 W2-AY 无关） · W2+ 中优先级 137/166→140/166 |
| v4.25 | 2026-07-23 | **W2-AZ Pipeline Builder分支版本+管道管理+数据期望组（3 项）**：① #18 Pipeline Builder 分支版本（PipelineBranchEngine PipelineBranch branch_id+pipeline_id+name+base_branch_id+status draft|review|approved|merged|reverted+protection_enabled+protection_rules+created_by+created_at+updated_at + create_branch 生成 pb-* + get_branch + list_branches 按 pipeline_id+status 过滤 + update_branch + delete_branch + approve_branch draft|review→approved + merge_branch approved→merged + revert_branch merged→reverted + 200 条上限 FIFO + MISSING_PIPELINE/MISSING_NAME/INVALID_STATUS/NOT_FOUND 校验）· ② #19 Pipeline Builder 管道管理（PipelineManagementEngine PipelineConfig config_id+pipeline_id+checkpoints+color_groups+custom_functions+folders+sampling_config+task_groups+parameters+created_at+updated_at + create_config 生成 pc-* + get_config + get_config_by_pipeline + list_configs 按 pipeline_id 过滤 + update_config + delete_config + 200 条上限 FIFO + MISSING_PIPELINE/NOT_FOUND 校验）· ③ #20 Pipeline Builder 数据期望（PipelineDataExpectationEngine DataExpectation expectation_id+pipeline_id+name+expectation_type primary_key|row_count|column_distinct|column_nulls|custom_sql+config+severity critical|warning|info+enabled+last_checked_at+last_result+created_at+updated_at + create_expectation 生成 de-* + get_expectation + list_expectations 按 pipeline_id+expectation_type+severity+enabled 过滤 + update_expectation + delete_expectation + run_expectation 模拟运行推进 last_checked_at+last_result + run_all_expectations + 200 条上限 FIFO + MISSING_PIPELINE/MISSING_NAME/INVALID_EXPECTATION_TYPE/INVALID_SEVERITY/NOT_FOUND 校验）· ④ 新增 55 测试（20 PipelineBranch+14 PipelineManagement+21 PipelineDataExpectation），全量回归 **3450 passed / 4 pre-existing failed + 5 pre-existing errors**（同前：test_test_connectivity/test_jwks_and_rs256_me/test_usage_prune_old/test_wiki_version_snapshot_on_approve + 5 collection errors，均与 W2-AZ 无关） · W2+ 中优先级 140/166→143/166 |
| v4.26 | 2026-07-23 | **W2-BA Pipeline画布+CodeRepositories+MediaSet分片组（3 项）**：① #2 Pipeline 画布（PipelineCanvasEngine PipelineNode node_id+pipeline_id+node_type transform|input|output|branch|merge|loop|conditional+name+config+x+y+width+height+status pending|running|completed|failed+error_message+created_at+updated_at + PipelineEdge edge_id+pipeline_id+source_node_id+source_port+target_node_id+target_port+edge_type data|control|conditional+created_at + CRUD create_node/pn-*/get_node/list_nodes 按 pipeline_id+node_type+status 过滤/update_node/delete_node + create_edge/pe-*/get_edge/list_edges 按 pipeline_id+source_node_id+target_node_id 过滤/delete_edge + validate_dag 模拟返回 cycles/isolated_nodes/dangling_edges + 200 条上限 FIFO + MISSING_PIPELINE/MISSING_NAME/INVALID_NODE_TYPE/INVALID_EDGE_TYPE/NOT_FOUND 校验）· ② #3 Code Repositories（CodeRepositoryEngine CodeRepository repo_id+name+repository_type git|local|s3+location+branch+commit_hash+last_sync_at+status active|inactive|syncing|error+error_message+created_at+updated_at + CodeFile file_id+repo_id+file_path+content+last_modified_at+version + create_repo 生成 cr-* + get_repo + list_repos 按 name+repository_type+status 过滤 + update_repo + delete_repo + sync_repo inactive→syncing→active + list_files/get_file/update_file/delete_file + 200 条上限 FIFO + MISSING_NAME/MISSING_LOCATION/INVALID_REPOSITORY_TYPE/NOT_FOUND 校验）· ③ #5 MediaSet 分片（MediaSetShardingEngine MediaShard shard_id+media_set_id+shard_index+total_shards+file_path+size_bytes+checksum+status pending|uploading|completed|failed+uploaded_at+error_message+created_at + create_shard 生成 ms-* + get_shard + list_shards 按 media_set_id+status 过滤 + update_shard + delete_shard + complete_upload pending|uploading→completed + fail_upload pending|uploading→failed + get_upload_status 聚合所有分片状态返回 progress/total/complete/failed/pending + 200 条上限 FIFO + MISSING_MEDIA_SET/INVALID_SHARD_INDEX/INVALID_STATUS/NOT_FOUND 校验）· ④ 新增 62 测试（25 PipelineCanvas+17 CodeRepository+20 MediaSetSharding），全量回归 **3512 passed / 4 pre-existing failed + 5 pre-existing errors**（同前，均与 W2-BA 无关） · W2+ 中优先级 143/166→146/166 |
| v4.27 | 2026-07-23 | **W2-BB MediaSet浏览器+交互+ASR转录组（3 项）**：① #6 MediaSet 浏览器（MediaSetBrowserEngine BrowserItem id+media_ref_id+name+type+size_bytes+created_at + browse_items(media_set_id, file_type) + get_item + search_items + create_item + delete_item + get_item_preview + 200 条上限 FIFO + MEDIA_SET_NOT_FOUND/ITEM_NOT_FOUND 校验）· ② #7 媒体集内容查看与交互（MediaInteractionEngine MediaView view_id+media_ref_id+view_type dicom|document|image|video+brightness+contrast+zoom+pan_x+pan_y+rotation+annotations+created_at+updated_at + ViewAnnotation id+view_id+type+content+x+y + create_view/mv-*/get_view/update_view/delete_view + get_annotations/add_annotation/delete_annotation + 200 条上限 FIFO + MEDIA_REF_NOT_FOUND/NOT_FOUND 校验）· ③ #8 音频转录（ASR）变换（AudioTranscriptionEngine TranscriptionJob job_id+media_ref_id+status pending|processing|completed|failed+language auto|zh|en|ja|ko+transcript_text+confidence+timestamps+error_message+created_at+completed_at + create_job/at-*/get_job/list_jobs 按 media_ref_id+status 过滤 + cancel_job + get_transcript + estimate_language 自动推断语言 + 200 条上限 FIFO + MEDIA_REF_NOT_FOUND/INVALID_LANGUAGE/NOT_FOUND 校验）· ④ 新增 49 测试（14 MediaSetBrowser+17 MediaInteraction+18 AudioTranscription），全量回归 **3561 passed / 4 pre-existing failed + 5 pre-existing errors**（同前，均与 W2-BB 无关） · W2+ 中优先级 146/166→149/166 |
| v4.28 | 2026-07-23 | **W2-BC DICOM+WorkshopAutoGen+DocIntel组（3 项）**：① #9 DICOM 医学影像支持（DicomEngine DicomMetadata dicom_id+media_ref_id+patient_id+patient_name+study_id+study_date+series_id+modality+manufacturer+image_count+pixel_spacing+slice_thickness+window_center+window_width+created_at + extract_metadata/dic-*/get_metadata/list_metadata 按 media_set_id+patient_id+study_id 过滤/render_image 支持 window_center/window_width/delete_metadata + 200 条上限 FIFO + MEDIA_REF_NOT_FOUND/NOT_FOUND 校验）· ② #10 Workshop 自动生成（WorkshopAutoGenEngine WorkshopTemplate template_id+object_type+name+description+table_columns[]+preview_config+generated_at+updated_at + generate_workshop/wst-*/get_template/list_templates 按 object_type 过滤/update_template/delete_template/preview_template + 200 条上限 FIFO + INVALID_OBJECT_TYPE/NOT_FOUND 校验）· ③ #11 AIP Doc Intel 五步法（DocIntelEngine DocIntelJob job_id+media_ref_id+status pending|ocr|md_conversion|field_extraction|validation|linking|completed|failed+current_step+ocr_result+md_content+extracted_fields+validation_result+linked_entities+error_message+created_at+updated_at + create_job/di-*/get_job/list_jobs 按 media_ref_id+status 过滤/run_step 推进单步/run_all_steps 完整流程/cancel_job/get_extracted_fields + 200 条上限 FIFO + MEDIA_REF_NOT_FOUND/INVALID_STEP/NOT_FOUND 校验）· ④ 新增 49 测试（15 DicomEngine+15 WorkshopAutoGen+18 DocIntel+1 单例），全量回归 **3610 passed / 4 pre-existing failed + 5 pre-existing errors**（同前，均与 W2-BC 无关） · W2+ 中优先级 149/166→152/166 |
| v4.29 | 2026-07-23 | **W2-BD LLMNode+AgentProxy+DynamicScheduling组（3 项）**：① #12 Use LLM 节点（LlmNodeEngine LlmNode node_id+name+node_type entity_extraction|visual_template|text_classification|summarization+prompt_template+model_name+temperature+max_tokens+input_schema+output_schema+enabled+created_at+updated_at + create_node/ln-*/get_node/list_nodes 按 node_type+enabled 过滤/update_node/delete_node/execute_node + 200 条上限 FIFO + MISSING_NAME/INVALID_NODE_TYPE/NOT_FOUND 校验）· ② #13 Agent Proxy/Worker（AgentProxyEngine AgentProxy proxy_id+name+proxy_type reverse_proxy|forward_proxy|load_balancer+target_url+listen_port+enabled+health_status healthy|unhealthy|degraded+last_health_check_at+error_message+created_at+updated_at + create_proxy/ap-*/get_proxy/list_proxies 按 proxy_type+health_status 过滤/update_proxy/delete_proxy/toggle_proxy/health_check + 200 条上限 FIFO + MISSING_NAME/MISSING_TARGET_URL/INVALID_PROXY_TYPE/NOT_FOUND 校验）· ③ #23 Dynamic Scheduling Scenarios（DynamicSchedulingEngine SchedulingScenario scenario_id+name+scenario_type sandbox|staging|save_action|custom_save+constraints[]+suggestion_rules[]+search_rules[]+realtime_evaluation+enabled+created_at+updated_at + create_scenario/ds-*/get_scenario/list_scenarios 按 scenario_type+enabled 过滤/update_scenario/delete_scenario/run_evaluation/apply_scenario + 200 条上限 FIFO + MISSING_NAME/INVALID_SCENARIO_TYPE/NOT_FOUND 校验）· ④ 新增 50 测试（15 LlmNode+17 AgentProxy+18 DynamicScheduling），全量回归 **3660 passed / 4 pre-existing failed + 5 pre-existing errors**（同前，均与 W2-BD 无关） · W2+ 中优先级 152/166→155/166 |
| v4.30 | 2026-07-23 | **W2-BE SmartFunctions+ValidationRules+OkfLint组（3 项）**：① #24 Dynamic Scheduling 智能函数（SchedulingSmartFunctionsEngine SmartFunction function_id+name+function_type suggestion|search|filter|sort+description+enabled+created_at+updated_at + SuggestionResult function_id+entity_id+score+reason+metadata+created_at + create_function/sf-*/get_function/list_functions 按 function_type+enabled 过滤/update_function/delete_function/suggest 返回评分-1~1/search + 200 条上限 FIFO + MISSING_NAME/INVALID_FUNCTION_TYPE/NOT_FOUND 校验）· ② #25 Dynamic Scheduling 验证规则（SchedulingValidationEngine ValidationRule rule_id+name+rule_type hard|soft+constraint_expression+description+severity critical|warning|info+enabled+created_at+updated_at + ValidationResult result_id+rule_id+entity_id+passed+violation_details+severity+evaluated_at + create_rule/vr-*/get_rule/list_rules 按 rule_type+severity+enabled 过滤/update_rule/delete_rule/validate/validate_all + 200 条上限 FIFO + MISSING_NAME/INVALID_RULE_TYPE/INVALID_SEVERITY/NOT_FOUND 校验）· ③ #27 OKF Lint（OkfLintEngine LintRule rule_id+name+rule_type column_drift|contract_violation|data_quality|schema_change+severity critical|warning|info+enabled+created_at+updated_at + LintResult result_id+rule_id+dataset_rid+passed+violation_details+severity+drift_metrics+evaluated_at + create_rule/ol-*/get_rule/list_rules 按 rule_type+severity+enabled 过滤/update_rule/delete_rule/lint 全量检查/get_drift_report + 200 条上限 FIFO + MISSING_NAME/INVALID_RULE_TYPE/INVALID_SEVERITY/NOT_FOUND 校验）· ④ 新增 52 测试（16 SmartFunctions+18 ValidationRules+18 OkfLint），全量回归 **3712 passed / 4 pre-existing failed + 5 pre-existing errors**（同前，均与 W2-BE 无关） · W2+ 中优先级 155/166→158/166 |
| v4.43 | 2026-07-24 | **Phase 0 基础设施补齐 + #90 清账 + Phase 1/2/3/5 过期状态修正**：① Phase 0 基础设施补齐（scripts/ci.sh 顶层 CI 脚本串联 pytest+vitest+tsc · docs/palantir/screenshots/ 按 Phase 分目录截图归档 · docs/palantir/ui-checklist-template.md UI 对标检查清单模板）· ② #90 Pipeline 管理功能清账（确认由 W2-AZ #19 PipelineManagementEngine 完全覆盖：parameters+custom_functions+folders+checkpoints，14 测试全通过）· ③ Phase 1/2/3/5 详细章节状态修正为 ✅ 已完成（与里程碑表一致）· ④ 全局进度 247/259→252/259 · ⬜ 待执行 5→0 |

---

*v4.30 · w2-be*

# 220plan · AOS Platform W1 分阶段开发与里程碑计划

> **版本**：v2.9 · 2026-07-22
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
| 0 | 基础设施与测试框架 | ⬜ 待执行 | — | CI 管线 · 测试模板 · 截图归档目录 | — |
| 1 | 核心引擎层 | ✅ 已完成 | W1-1, W1-4, W1-10 | Function 表达式引擎 · Build 引擎 · Function 沙箱 | Phase 0 |
| 2 | 数据集成核心 | ✅ 已完成 | W1-5, W1-8, W1-13, W1-14, W1-19 | Funnel 四阶段 · Transform 算子库 · Lineage DAG · Pipeline Builder DAG 编辑器 · Functions Python Builder | Phase 1 |
| 3 | Ontology 写回闭环 | ✅ 已完成 | W1-3, W1-6, W1-7, W1-17, W1-18 | Action 写回 · 壳核模式 · Funnel 可视化编辑器 · Ontology 角色 · Function Type 视图 | Phase 2 |
| 4 | AIP 智能层 | ✅ 已完成 | W1-2, W1-12 | Logic 三栏编排 · Evals 门控 | Phase 3 + LLM Gateway 接入 |
| 5 | 非结构化数据与数据集 | ✅ 已完成 | W1-9, W1-15, W1-16 | MediaReference 桥接 · SQL 控制台 · MediaSet 类型化 | Phase 1 |
| 6 | 集成优化与收尾 | ✅ 已完成 | W1-11 | Pipeline 重试 · 全链路验收 | Phase 2–5 |

### 1.2 全局执行进度看板

> **最后更新**：2026-07-22 · v2.9 W2-P Action 参数增强组（3 项）· W2 高优先级 27/27 清零 · W1 全量交付
> **差距总览**：259 项 · ✅ 已完成 78 · ⬜ 待执行 174 · ⏸ 暂停 7

#### 1.2.1 全局差距统计

| 分类 | 数量 | 执行状态 | Wave | 说明 |
| --- | --- | --- | --- | --- |
| ✅ 已达成 | 2 | ✅ 已完成 | — | 无需开发，保持维护 |
| W1 优先项 | 19 | ✅ 已完成 | W1 | Phase 0–6 核心交付，本计划主体（19/19 全部完成） |
| W2+ 高优先级 | 27 | ✅ 已完成（27/27） | W2 | W1 完成后优先推进 · W2-A（#3/#6/#8/#9/#20/#23）+ W2-B（#7/#18/#21/#25/#26）+ W2-C（#12/#13/#14/#15/#16）+ W2-D（#10/#24）+ W2-E（#1/#2/#4/#22）+ W2-F（#11/#17/#19 增强版）已交付 |
| W2+ 中优先级 | 166 | 🔄 进行中（32/166） | W2–W3 | W2-G～W2-P 已交付 32 项 · 按模块逐步推进 |
| W2+ 低优先级 | 33 | ⬜ 待执行 | W3+ | 按需推进（原 35，合并 Foundry Rules/Linter 重复项 -2） |
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
| 1 | Connection CDC | 无 | Debezium 参考 | ⬜ 待执行 |
| 2 | Pipeline 画布 | 有 | 真 DAG 编排 | ⬜ 待执行 |
| 3 | Code Repositories | 无 | Transform 代码管理 | ⬜ 待执行 |
| 4 | Schedule 触发机制 | UI 有 | 上游/逻辑变更触发 | ⬜ 待执行 |
| 5 | MediaSet 分片 | 无 | 大文件分片 | ⬜ 待执行 |
| 6 | MediaSet 浏览器 | 无 | Document/Spreadsheet 分型 | ⬜ 待执行 |
| 7 | 媒体集内容查看与交互 | JSON 元数据列表 | DICOM 对比度/曝光拖动调整 + 文件在线预览 | ⬜ 待执行 |
| 8 | 音频转录（ASR）变换 | 无 | "将音频转录为文本"内置变换 + 自动语言推断 | ⬜ 待执行 |
| 9 | DICOM 医学影像支持 | 无 | DICOM 格式识别 + Patient ID/Study ID 自动提取 + 图像渲染 | ⬜ 待执行 |
| 10 | Workshop 自动生成 | 无 | 对象类型 → 自动生成 Workshop 模块（对象表+预览） | ⬜ 待执行 |
| 11 | AIP Doc Intel 五步法 | 无 | OCR→MD→抽字段→校验→回链 | ⬜ 待执行 |
| 12 | Use LLM 节点 | 无 | 实体提取/视觉模板 | ⬜ 待执行 |
| 13 | Agent Proxy/Worker | 无 | 内网反向代理 | ⬜ 待执行 |
| 14 | 存储路由向导 | 无 | Dataset/MediaSet/Stream 选择 | ⬜ 待执行 |
| 15 | Expectation | 无 | PK 唯一/行数检查 | ✅ 已完成（W2-G·16 测试·pk_unique + row_count + severity + check_all） |
| 16 | Write Mode | data_transaction.py 有 append/snapshot/update | Default/Append/Snapshot | ✅ 已完成（W2-G·16 测试·新增 default 模式 + describe API + 4 种写入模式） |
| 17 | Transaction 状态机 | 无 | OPEN/COMMITTED/ABORTED | ✅ 已完成（W2-G·22 测试·DataTransaction 状态机 + write_mode 集成 + 不可逆转换） |
| 18 | Pipeline Builder 分支版本 | disabled | 创建/审批/合并/rebase/保护/回退分支 | ⬜ 待执行 |
| 19 | Pipeline Builder 管道管理 | 无 | 搭建设置/检查点/颜色组/自定义函数/文件夹/采样/任务组/参数 | ⬜ 待执行 |
| 20 | Pipeline Builder 数据期望 | 无 | 主键/行数期望/健康检查/单元测试 | ⬜ 待执行 |
| 21 | Dataset Preview 列统计 | 无 | 列级空值%/分布/样本/列信息面板 | ⬜ 待执行 |
| 22 | Dataset Preview 附加视图 | 4 个极简 Tab | About/Columns/Schedule 面板 + 6 个附加视图 + 数据集对比 | ⬜ 待执行 |
| 23 | Dynamic Scheduling Scenarios | 无 | 假设分析沙箱/暂存编辑/Save Action/Function-backed 自定义保存 | ⬜ 待执行 |
| 24 | Dynamic Scheduling 智能函数 | 无 | Suggestion Function（评分-1~1）+ Search Function（右键触发） | ⬜ 待执行 |
| 25 | Dynamic Scheduling 验证规则 | 无 | HARD+SOFT 约束/实时重评估/编排流程/自定义描述 | ⬜ 待执行 |
| 26 | Data Health | 无 | 行数漂移/模式变更检查 | ⬜ 待执行 |
| 27 | OKF Lint | 无 | 列漂移检测/契约校验 | ⬜ 待执行 |
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
| 39 | Object 存储后端（专职引擎） | PG JSONB | OSv2 分布式索引/数十亿级/Spark 查询 | ⬜ 待执行 |
| 40 | 对象增量索引（Diff-based） | 全量 upsert | 自动差异计算/仅索引变化行 | ⬜ 待执行 |
| 41 | 流式对象索引 | 无 | Flink/CDC/每 OT 2MB/s | ⬜ 待执行 |
| 42 | 对象编辑冲突解决 | 无 | 用户优先/时间戳优先两种策略 | ✅ 已完成（W2-N·26 测试·ConflictEngine 检测+解决 + user_priority/timestamp_priority 两种策略 + 用户优先级配置） |
| 43 | 对象物化（Materializations） | 无 | 自动输出对象数据为数据集/6h 周期 | ⬜ 待执行 |
| 44 | 对象模式迁移 | 无 | 5 种迁移指令/每批 500 编辑 | ✅ 已完成（W2-N·26 测试·MigrationEngine ADD/REMOVE/RENAME/CHANGE_TYPE/SET_NULLABLE 5 指令 + 批次 500 上限 + dry_run + 状态跟踪） |
| 45 | 对象编辑历史追踪 | decision_lineage | 对象属性变更时间线/开关控制 | ✅ 已完成（W2-N·26 测试·ChangeLogEngine per-OT 开关 + record/record_force + 多维查询 + 时间线 + 时间范围筛选） |
| 46 | 受限视图（RV·行级权限） | 无 | 动态行级策略/医生仅看自己患者 | ⬜ 待执行 |
| 47 | MDO 多数据源对象（列级权限） | 无 | 不同属性不同数据源/最多 70 源 | ⬜ 待执行 |
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
| 58 | Action 参数约束 | JSON 配置 | User Input/Multiple Choice/从 Object Set 取选项 | ⬜ 待执行 |
| 59 | Action 参数默认值 | 无 | 静态值/对象属性/类型类/环境变量 | ⬜ 待执行 |
| 60 | Action 参数覆盖 | 无 | 条件覆盖块/Visible/Disabled/Required 三态 | ⬜ 待执行 |
| 61 | Action 参数筛选 | 无 | 对象下拉起始集/搜索范围/安全性筛选 | ⬜ 待执行 |
| 62 | Action 提交标准可视化 | JSON | 条件模板/逻辑运算符/失败消息可视化 | ⬜ 待执行 |
| 63 | Action 通知副作用 | 无 | 静态/参数/对象属性/函数收件人 + 模板内容 | ⬜ 待执行 |
| 64 | Action Webhook 副作用 | 无 | 数据输出模式/副作用模式/输入输出映射 | ⬜ 待执行 |
| 65 | Action Sections 分组 | 无 | 单列双列布局/折叠/条件显示 | ⬜ 待执行 |
| 66 | Action 撤销（Revert） | 无 | 提交后立即撤销/条件检查 | ⬜ 待执行 |
| 67 | Action 日志对象类型 | 无 | [LOG] 前缀/操作 RID/版本/时间戳/参数值 | ⬜ 待执行 |
| 68 | Action 平台集成 | 无 | 对象视图/Object Explorer/Workshop 按钮组 | ⬜ 待执行 |
| 69 | Ontology 图查询 | 基础 | 多跳/路径 | ✅ 已完成（W2-I·21 测试·多跳 BFS + 双向 BFS 最短路径 + 子图扩展） |
| 70 | Action 事务回滚 | 无 | 补偿事务 | ⬜ 待执行 |
| 71 | k-LLM 智能路由 | 无 | 智能选模型 | ⬜ 待执行 |
| 72 | k-LLM 场景化路由 | 无 | 按任务类型选模/块级选模 | ⬜ 待执行 |
| 73 | k-LLM 熔断/热切换 | 无 | 主模失败自动切回退 | ⬜ 待执行 |
| 74 | 数据出境策略 | 无 | 敏感标记强制私有路由 | ⬜ 待执行 |
| 75 | 自定义 LLM 注册 | 无 | Function Interfaces/Source/Webhook | ⬜ 待执行 |
| 76 | Edits 合并策略 | 无 | 字段级/LastWriteWins/人工仲裁 | ✅ 已完成（W2-H·22 测试·field_level/last_write_wins/manual_arbitration 三种策略） |
| 77 | Prompt 工程 | 无 | 变量注入/Few-shot/版本 | ⬜ 待执行 |
| 78 | 调试器 | 无 | CoT/提议预览 | ⬜ 待执行 |
| 79 | Automate 集成 | 无 | 条件触发/提案 | ⬜ 待执行 |
| 80 | 四层成熟度 | 无 | L1/L2/L3/L4 楼梯 | ⬜ 待执行 |
| 81 | Agent 六工具 | 基础 | Action/Query/Function/Var/Command/Clarify | ⬜ 待执行 |
| 82 | L4 熔断 | 无 | 失败率>5%→降级 L3 | ⬜ 待执行 |
| 83 | 模型预热 | 无 | warm-up/冷启动处理 | ⬜ 待执行 |
| 84 | Decision Lineage | 无 | 完整记录/可复盘 | ⬜ 待执行 |
| 85 | Insight Backfill | 无 | 高置信结论→Insight Object | ⬜ 待执行 |
| 86 | 三种提案通道 | 无 | 同步/异步 Automate/异步管道 | ⬜ 待执行 |
| 87 | Capability Adapter 契约 | 无 | Manifest/运行时 API/Facade | ⬜ 待执行 |
| 88 | CAP 约束 | 无 | CAP-01~07 | ⬜ 待执行 |
| 89 | Pipeline 界面四区域 | 部分 | 顶部工具栏/详细侧栏/提案/历史视图 | ⬜ 待执行 |
| 90 | Pipeline 管理功能 | 无 | 参数/自定义函数/文件夹/检查点 | ⬜ 待执行 |
| 91 | Pipeline Ontology 输出 | 无 | 对象类型/链接类型输出配置 | ⬜ 待执行 |
| 92 | Pipeline Expectation | 无 | PK 唯一/行数检查 | ⬜ 待执行 |
| 93 | Pipeline Write Mode | 无 | Default/Append/Snapshot 选择 | ⬜ 待执行 |
| 94 | Pipeline Types（Batch/Incremental/Streaming） | 基础概念 | 三种管道类型区分及处理语义 | ⬜ 待执行 |
| 95 | Incremental Pipeline | 无 | 增量处理/变更捕获 | ⬜ 待执行 |
| 96 | Streaming Pipeline | 无 | 实时流式处理/状态化操作 | ⬜ 待执行 |
| 97 | 事件触发器 | 无 | 上游数据集/管道构建完成触发 | ⬜ 待执行 |
| 98 | 复合触发器 | 无 | AND/OR 逻辑组合触发器 | ⬜ 待执行 |
| 99 | 安全标记传播控制 | 无 | stop_propagating/stop_requiring 配置 | ⬜ 待执行 |
| 100 | 标记移除策略 | 无 | filter-in/filter-out 移除策略 | ⬜ 待执行 |
| 101 | 代码仓库分支管理 | 无 | Git 分支创建/合并/删除 | ⬜ 待执行 |
| 102 | PR 工作流 | 无 | Pull Request/代码审查/CI/CD 检查 | ⬜ 待执行 |
| 103 | 变换预览 | 无 | 样本数据上运行代码预览 | ⬜ 待执行 |
| 104 | Python 调试器 | 无 | 断点/单步调试/数据框预览 | ⬜ 待执行 |
| 105 | 单元测试 | 无 | Python/Java/TypeScript 测试支持 | ⬜ 待执行 |
| 106 | Artifact 存储库 | 无 | Conda/Docker/Maven 制品管理 | ⬜ 待执行 |
| 107 | AIP Assist | 无 | 代码解释/漏洞查找/翻译/代码自动完成 | ⬜ 待执行 |
| 108 | repoSettings.json | 无 | 标签验证/PR 模板/验证规则配置 | ⬜ 待执行 |
| 109 | 列级血缘 | 无 | 列名追踪/列级影响分析 | ⬜ 待执行 |
| 110 | 推荐项目结构 | 无 | Datasource→Transform→Ontology→Workflow 多项目架构 | ⬜ 待执行 |
| 111 | 逻辑流（Logic Flows） | 无 | Compass Files Lister/连接流编排 | ⬜ 待执行 |
| 112 | Data Connection Agent Proxy | 无 | 内网反向代理运行时 | ⬜ 待执行 |
| 113 | Data Connection Agent Worker | 无 | 客户主机执行运行时 | ⬜ 待执行 |
| 114 | Data Connection Agent 管理 | 无 | 注册/下载/心跳/日志/驱动/证书/自动升级 | ⬜ 待执行 |
| 115 | Data Connection 源探索 | 基础 | ER关系图/资源树/样本预览 | ⬜ 待执行 |
| 116 | Data Connection 文件筛选 | 无 | 路径正则/修改时间/文件大小/排除已同步 | ⬜ 待执行 |
| 117 | Data Connection 文件变换 | 无 | Gzip/合并/重命名/PGP解密/附加时间戳 | ⬜ 待执行 |
| 118 | Data Connection Streaming Sync | 无 | Kafka/Kinesis/PubSub → Stream | ⬜ 待执行 |
| 119 | Data Connection Push-based Ingestion | 无 | OAuth2 Client Credentials → Stream | ⬜ 待执行 |
| 120 | Data Connection Export 文件 | 无 | Dataset → S3/ABFS/HDFS | ⬜ 待执行 |
| 121 | Data Connection Export 表 | 无 | Incremental mirror + Truncate on SNAPSHOT | ⬜ 待执行 |
| 122 | Data Connection Export 流 | 无 | Stream → Kafka 等 | ⬜ 待执行 |
| 123 | Data Connection Webhooks 多步调用 | 无 | Call 1 → Call 2，参数引用 | ⬜ 待执行 |
| 124 | Data Connection Webhooks 输出参数 | 无 | 从响应提取字段+类型转换 | ⬜ 待执行 |
| 125 | Data Connection Webhooks 执行策略 | 无 | 并发/速率/超时/重试 | ⬜ 待执行 |
| 126 | Data Connection Egress policies | 无 | CIDR/Port/域名白名单 | ⬜ 待执行 |
| 127 | Data Connection Exportable markings | 无 | 可导出权限标记控制 | ⬜ 待执行 |
| 128 | Data Connection OIDC/Cloud Identity | 无 | OpenID Connect/云身份/出站应用 | ⬜ 待执行 |
| 129 | Data Connection 虚拟表 | 无 | 外部数据仓库注册为虚拟表 | ⬜ 待执行 |
| 130 | Data Lineage 可视化 | 无 | 血缘图/展开/着色/保存分享 | ⬜ 待执行 |
| 131 | Data Lineage 列级血缘 | 无 | 列名搜索/列级追踪 | ⬜ 待执行 |
| 132 | Data Lineage 搭建时间线 | 无 | 甘特图/调度管理 | ⬜ 待执行 |
| 133 | Data Health 检查类型 | 无 | 状态/时间/大小/内容/模式检查 | ⬜ 待执行 |
| 134 | Data Health 检查计划 | 无 | 自动计划（数据集更新触发）+ 手动计划（定时执行） | ⬜ 待执行 |
| 135 | Data Health 检查组 | 无 | 检查分组/通知/监控 | ⬜ 待执行 |
| 136 | Data Health 检查组诊断 | 无 | 失败聚焦/检查列表/分组策略 | ⬜ 待执行 |
| 137 | Data Health 监测选项 | 无 | 无通知/所有失败/仅严重 | ⬜ 待执行 |
| 138 | Data Health 平台内通知 | 无 | Foundry通知系统集成 | ⬜ 待执行 |
| 139 | Data Health Issues集成 | 无 | 检查失败自动创建/解决问题自动关闭 | ⬜ 待执行 |
| 140 | Data Health 数据集健康Tab | 无 | 数据集预览中的健康Tab | ⬜ 待执行 |
| 141 | Data Health 沿袭健康着色 | 无 | 数据沿袭中按健康状态着色 | ⬜ 待执行 |
| 142 | Data Health 应用入口 | 无 | 侧边栏数据健康应用 | ⬜ 待执行 |
| 143 | Functions 测试调试 | 无 | 单元测试/调试器/性能分析 | ⬜ 待执行 |
| 144 | Functions 外部API调用 | 无 | TypeScript/Python调用外部系统 | ⬜ 待执行 |
| 145 | Interfaces 定义/继承 | 无 | 接口定义/扩展/实现/多态 | ⬜ 待执行 |
| 146 | Dataset Preview 详情Tabs | 部分 | 历史/健康/比较/流视图 | ⬜ 待执行 |
| 147 | Workshop 变量联动 | 弱 | 全局变量 | ⬜ 待执行 |
| 148 | Compute Module 调度引擎 | 无 | 无服务器 Docker 容器生命周期管理 | ⬜ 待执行 |
| 149 | Compute Module 副本扩缩 | 无 | min/max replicas + 每副本并发 | ⬜ 待执行 |
| 150 | Compute Module 资源约束 | 无 | CPU Request/Limit + GPU + Memory | ⬜ 待执行 |
| 151 | Compute Module API（job 长轮询） | 无 | `/interactive-module/api/internal-query/job` + 结果回传 | ⬜ 待执行 |
| 152 | `app.py` 入口约定 | 无 | 函数名即端点 + 相对导入 + JSON 序列化 | ⬜ 待执行 |
| 153 | `meta.yaml` 依赖 + `gradle.properties` | 无 | 镜像构建配置 / baseImageTag ≥ 0.15.0 校验 | ⬜ 待执行 |
| 154 | Docker 镜像发布（Artifact Repo） | 无 | New → Artifacts → Docker → 不支持 `latest` 标签 | ⬜ 待执行 |
| 155 | Configure / Query / Overview 三标签页 | 无 | 容器配置/函数查询/状态总览 | ⬜ 待执行 |
| 156 | 缩容至零 + 冷启动告警 | 无 | Query 标签首次查询等待 | ⬜ 待执行 |
| 157 | 本地开发脚手架 | 无 | Dockerfile + requirements + app.py 模板 | ⬜ 待执行 |
| 158 | External access | 无 | Foundry data / services / 外部域名访问配置 | ⬜ 待执行 |
| 159 | 与 Functions / Workshop / Slate 集成 | 无 | Functions 后端类型 + 前端触发入口 | ⬜ 待执行 |
| 160 | Ferry 增量包 | 全量 | 增量 | ⬜ 待执行 |
| 161 | Data Integration 统一框架 | 分散 | 连接+变换+管理三位一体 | ⬜ 待执行 |
| 162 | 管道维护与监控 | 无 | 监控视图/数据期望/稳定性建议 | ⬜ 待执行 |
| 163 | Ontology Interfaces | 无 | 功能接口/抽象对象接口/多态 | ⬜ 待执行 |
| 164 | 时间序列（Time Series） | lineage 桩 | TSP/Object Type/传感器/同步索引 | ⬜ 待执行 |
| 165 | SAP 集成 | 无连接器 | SAP 认证组件/S/4HANA/ECC/BW | ⬜ 待执行 |
| 166 | pb-functions 函数库（381 函数） | 无 | 250+ 表达式/80 变换/AI 函数 | ⬜ 待执行 |

#### 1.2.5 W2+ 低优先级项（35 项 · Phase 9+）

> 按需推进，部分项可能根据业务需求升级优先级。

| # | 差距项 | 当前 | 目标 | 状态 |
| --- | --- | --- | --- | --- |
| 1 | Dataset Preview CSV 解析引擎 | csv.reader | 4 种解析器/12 配置参数/TextDataFrameReader 切换 | ⬜ 待执行 |
| 2 | Ontology JSON 导出/导入 | 无 | 架构序列化/跨 Ontology 复制 | ⬜ 待执行 |
| 3 | Ontology 计算/占用量跟踪 | 无 | 计算秒/V1 V2 存储后端/GB-月 | ⬜ 待执行 |
| 4 | Action 操作指标 | 无 | 30 天用量/失败率/监控 | ⬜ 待执行 |
| 5 | Data Connection Agent Metrics | 无 | 内存/磁盘/负载/过期时间仪表盘 | ⬜ 待执行 |
| 6 | Data Connection Agent 健康监控 | 无 | CPU/Queue/Disk 分级告警规则 | ⬜ 待执行 |
| 7 | Data Connection 直连迁移向导 | 无 | 5步迁移+30天回滚 | ⬜ 待执行 |
| 8 | Data Connection Source Marketplace | 无 | 同步作为 Marketplace 产品内容类型 | ⬜ 待执行 |
| 9 | Data Connection Webhooks Storage | 无 | 6个月存储+full response可选 | ⬜ 待执行 |
| 10 | Data Connection Agent SSL Certificates | 无 | 代理证书管理 | ⬜ 待执行 |
| 11 | Data Health 通知打盹（Snoozing） | 无 | 单独/批量打盹 + 打盹历史 | ⬜ 待执行 |
| 12 | Data Health 上下文面板 | 无 | 评论/问题/计划/来源信息 | ⬜ 待执行 |
| 13 | Data Health Marketplace集成 | 无 | 将健康检查添加到Marketplace产品 | ⬜ 待执行 |
| 14 | Linter 规则引擎 | 无 | 反模式检测/建议/修复提案 | ⬜ 待执行 |
| 15 | Linter 扫描调度 | 无 | 定期扫描/资源范围/规则范围 | ⬜ 待执行 |
| 16 | Foundry Rules 规则引擎 | 无 | 点选规则/条件/工作流 | ⬜ 待执行 |
| 17 | Foundry Rules 时间序列 | 无 | 时间序列同步/规则 | ⬜ 待执行 |
| 18 | Dynamic Scheduling 甘特图 | 无 | 拖拽调度/约束/分配建议 | ⬜ 待执行 |
| 19 | Dynamic Scheduling 机器学习 | 无 | ML支持的实时调度解决方案 | ⬜ 待执行 |
| 20 | Workshop 拖拽 | 弱 | 自由拖拽 | ⬜ 待执行 |
| 21 | 计算秒定价 + 用量计量 | 无 | vCPU/T4/V100/A10G 计算秒 | ⬜ 待执行 |
| 22 | 预测扩缩（Predictive Auto-scaling） | 无 | 历史负载预测 + 主动预热 | ⬜ 待执行 |
| 23 | Telemetry / Format / Container log source | 无 | 遥测开关 + 日志格式 + 来源 | ⬜ 待执行 |
| 24 | Volume mounts（副本内共享卷） | 无 | Add volume + 共享存储 | ⬜ 待执行 |
| 25 | COP 实时态势 | 概览 | 实时监控 | ⬜ 待执行 |
| 26 | 分布式追踪 | 无 | OpenTelemetry | ⬜ 待执行 |
| 27 | 管道性能优化 | 无 | Spark/投影/原生加速/Profiles | ⬜ 待执行 |
| 28 | Foundry Rules 规则引擎 | 2 条 lint | 规则 Object 模型/工作流/多场景集成 | ⬜ 待执行 |
| 29 | Linter 质量扫描 | 2 条 lint | 规则库/扫描调度/修复提案/影响追踪 | ⬜ 待执行 |
| 30 | 地理空间数据框架 | 无 | GeoJSON/PostGIS/矢量/栅格/投影 | ⬜ 待执行 |
| 31 | Map 地图可视化 | 占位文字 | 地图图层/地理搜索/Workshop 模板 | ⬜ 待执行 |
| 32 | Vertex 数字孪生 | 无 | 数字孪生建模/模拟/因果分析 | ⬜ 待执行 |
| 33 | 地理时间序列 | 无 | 位置追踪 Object/同步组件 | ⬜ 待执行 |
| 34 | Process Mining | 无 | 事件日志/流程发现/瓶颈分析 | ⬜ 待执行 |
| 35 | Hyperauto 开箱集成 | 无 | 自动同步/自动 Ontology/ERP/CRM | ⬜ 待执行 |

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
> **状态**：⬜ 待执行

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
> **状态**：⬜ 待执行

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
> **状态**：⬜ 待执行

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
> **状态**：⬜ 待执行

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
> **状态**：⬜ 待执行

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

---

*v2.8 · w2-o*

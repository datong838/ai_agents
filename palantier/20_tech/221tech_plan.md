# 221tech · AIP 决策引擎技术方案

> **版本**：v1.0 · 2026-07-24
> **分支**：feature/221plan
> **关联**：[221plan](221plan-分阶段开发与里程碑计划.md) · [221m](221m-与目标系统差距对照分析.md)
> **模式**：Engine(Pydantic+Singleton+threading.Lock) + Router(FastAPI APIRouter) + Test(pytest 9用例/模块)

---

## 概述

33 项 AIP 决策引擎增强任务，分 3 Phase：
- **Phase 1**（7 项）：基础增强 — Logic 运行时/ProposeEdits/Wiki/状态版本/调试器
- **Phase 2**（12 项）：生产安全 — Evals 门控/L4 熔断/AppState/RAG/记忆
- **Phase 3**（14 项）：能力扩展 — 可观测性/Model Catalog/Assist/Analyst/DocIntel

**统一文件命名**：`aip_<module>.py`（引擎）+ `aip_<module>_router.py`（路由）+ `test_aip_<module>.py`（测试）

---

## Phase 1 · 基础增强（7 项）

| # | 模块 | 引擎文件 | Model 类 | Engine 方法 |
|---|------|---------|----------|------------|
| 1 | LangGraph 运行时 | aip_langgraph_runtime | LangGraphConfig, LangGraphRun | register/start/stop/get_status |
| 2 | ProposeEdits Block | aip_propose_edits | ProposedEdit, EditPreview | propose/preview/apply/reject |
| 3 | Wiki 字段支持 | aip_wiki_field | WikiField, WikiBinding | bind/unbind/resolve/list_bindings |
| 4 | Logic 状态管理 | aip_logic_state | LogicState (draft/published/deprecated) | transition/list/filter |
| 5 | Logic 版本管理 | aip_logic_version | LogicVersion, VersionDiff | create/rollback/diff/list_versions |
| 6 | 调试器 CoT 增强 | aip_debug_cot | CotStep, CotTrace | expand/collapse/get_trace/annotate |
| 7 | 调试器工具追踪 | aip_debug_tools | ToolCall, ToolCallChain | record/trace/get_chain/filter |

---

## Phase 2 · 生产安全（12 项）

| # | 模块 | 引擎文件 | Model 类 | Engine 方法 |
|---|------|---------|----------|------------|
| 8 | Evals 评测集 CRUD | aip_eval_crud | EvalSuiteItem, EvalCase | create/read/update/delete/list |
| 9 | Evals 门控上线 | aip_eval_gate | GateConfig, GateResult | configure/check/block_release/get_status |
| 10 | 跨模型对比 | aip_eval_cross_model | ModelComparison, ComparisonResult | compare/get_report/rank |
| 11 | 评测仪表盘 | aip_eval_dashboard | DashboardMetrics, MetricPoint | collect/aggregate/get_dashboard |
| 12 | RAG 评测类型 | aip_eval_rag | RagEvalCase, RagEvalResult | create/evaluate/get_recall |
| 13 | 生成评测类型 | aip_eval_gen | GenEvalCase, GenEvalResult | create/evaluate/get_quality |
| 14 | 工具调用评测 | aip_eval_tool | ToolEvalCase, ToolEvalResult | create/evaluate/get_accuracy |
| 15 | L4 门控检查 | aip_l4_gate | L4GateCheck, L4GateResult | check/verify/list_blocking |
| 16 | L4 自动化熔断 | aip_l4_circuit | CircuitState, CircuitConfig | trip/recover/get_state/configure |
| 17 | Application State | aip_app_state | AppStateVar, AppState | set/get/delete/list/clear |
| 18 | RAG 检索增强 | aip_rag_context | RagContext, RetrievalResult | build_context/retrieve/rank |
| 19 | 长期记忆管理 | aip_long_memory | LongMemory, MemoryEntry | store/recall/search/forget |

---

## Phase 3 · 能力扩展（14 项）

| # | 模块 | 引擎文件 | Model 类 | Engine 方法 |
|---|------|---------|----------|------------|
| 20 | Logic 链路追踪 | aip_trace_logic | LogicTrace, TraceSpan | start_span/end_span/get_trace |
| 21 | 指标监控 | aip_metrics | MetricRecord, MetricSummary | record/query/aggregate |
| 22 | 可观测性仪表盘 | aip_obs_dashboard | ObsDashboard, ObsPanel | create/update/render/get_data |
| 23 | 告警系统 | aip_alerts | AlertRule, AlertEvent | create/evaluate/list/acknowledge |
| 24 | Model Catalog 登记 | aip_model_catalog | ModelEntry, ModelVersion | register/list/get/update |
| 25 | 模型容量管理 | aip_model_capacity | CapacityConfig, CapacityUsage | set_limits/check_usage/reserve |
| 26 | 模型生命周期 | aip_model_lifecycle | ModelLifecycle, LifecycleEvent | transition/list/get_history |
| 27 | Assist 全局上下文 | aip_assist_context | GlobalContext, ContextEntry | build/inject/clear/get |
| 28 | Assist 权限感知 | aip_assist_perms | PermFilter, PermRule | register/check/filter |
| 29 | Analyst NL→Chart | aip_analyst_chart | ChartSpec, NLQuery | parse_query/generate/preview |
| 30 | Analyst 数据探索 | aip_analyst_explore | Exploration, Insight | explore/discover/report |
| 31 | DocIntel 文档解析 | aip_docintel_parse | ParsedDoc, ParseResult | parse/validate/get_structure |
| 32 | DocIntel 信息提取 | aip_docintel_extract | ExtractionRule, ExtractedTable | extract/validate/list |
| 33 | DocIntel 语义理解 | aip_docintel_semantic | SemanticQuery, DocQA | ask/summarize/index |

---

## 编码规范

1. **引擎文件**（`aip_<module>.py`）：
   - Pydantic Model 定义字段
   - Engine 类 Singleton + threading.Lock
   - CRUD + 业务方法
   - 容量限制常量（MAX_*）

2. **路由文件**（`aip_<module>_router.py`）：
   - `router = APIRouter(prefix="/api/aip/<module>")`
   - GET / POST / PUT / DELETE 映射 Engine 方法
   - Pydantic 请求/响应 Model

3. **测试文件**（`test_aip_<module>.py`）：
   - `@pytest.fixture` 初始化引擎
   - 9 个测试：CRUD(4) + 业务(2) + 边界(2) + 容量(1)
   - 重置 fixture 确保测试隔离

---

## 验收标准

- main.py 加载无错误，路由总数 = 119 + 33 = 152+
- 33 × 9 = 297 新增测试全 PASS
- 全量回归零新增失败

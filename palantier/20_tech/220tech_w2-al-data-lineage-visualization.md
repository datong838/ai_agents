# W2-AL · Data Lineage 组微规约

> **版本**：v1.0 · 2026-07-22
> **关联计划**：220plan v4.10 · W2+ 中优先级 #130/#131/#132
> **基线代码**：`aos_api/lineage_views.py`（W2-E #4 已交付列级血缘 CRUD）· `aos_api/lineage_graph.py`（W2-E #4 已交付图视图）
> **增量范围**：血缘可视化（着色/展开/保存分享）· 列名搜索与列级追踪 · 搭建时间线（甘特图/调度）

---

## §1 范围与目标

| 编号 | 功能 | 说明 | 交付物 |
|------|------|------|--------|
| #130 | Data Lineage 可视化 | 血缘图/展开/着色/保存分享 | LineageVisualizationEngine + REST API |
| #131 | Data Lineage 列级血缘 | 列名搜索/列级追踪（增量：搜索 + 追踪，CRUD 已存在） | ColumnLineageSearchEngine（增量） + REST API |
| #132 | Data Lineage 搭建时间线 | 甘特图/调度管理 | LineageBuildTimelineEngine + REST API |

---

## §2 数据模型

### 2.1 LineageVisualizationEngine · 血缘可视化

```python
class LineageView(BaseModel):
    view_id: str
    name: str
    description: str = ""
    root_dataset_rid: str
    graph_mode: Literal["graph", "tree"] = "graph"
    direction: Literal["upstream", "downstream", "both"] = "both"
    depth: int = 3
    layout: Literal["horizontal", "vertical", "radial"] = "horizontal"
    color_by: Literal["type", "health", "status", "owner"] = "type"
    collapsed_nodes: list[str] = []
    highlighted_nodes: list[str] = []
    saved_by: str = ""
    is_public: bool = False
    created_at: datetime
    updated_at: datetime

class LineageGraphNode(BaseModel):
    node_id: str
    label: str
    node_type: str  # dataset / transform / ontology / pipeline
    health_status: str = "healthy"  # healthy / warning / critical / unknown
    color: str = ""
    x: float = 0.0
    y: float = 0.0

class LineageGraphEdge(BaseModel):
    edge_id: str
    source: str
    target: str
    label: str = ""
    edge_type: str = "reads"  # reads / produces / impacts

class LineageGraph(BaseModel):
    view_id: str
    nodes: list[LineageGraphNode]
    edges: list[LineageGraphEdge]
    stats: dict[str, int] = {}  # node_count / edge_count / types{} / health{}

_MAX_VIEWS = 200
```

### 2.2 ColumnLineageSearchEngine · 列级血缘搜索（增量）

> 注：CRUD (`set_column_lineage` / `get_column_lineage`) 已由 W2-E #4 在 `lineage_views.py` 交付。
> 本批次增量交付「列名搜索」与「列级追踪」。

```python
class ColumnIndexEntry(BaseModel):
    dataset_rid: str
    column_name: str
    data_type: str = "string"
    description: str = ""
    tags: list[str] = []
    last_updated: datetime

class ColumnTraceStep(BaseModel):
    dataset_rid: str
    column_name: str
    transform_expr: str = ""
    direction: str  # upstream / downstream

class ColumnTraceResult(BaseModel):
    column: str
    dataset_rid: str
    direction: str
    depth: int
    path: list[ColumnTraceStep]

_MAX_COLUMN_INDEX = 200
```

### 2.3 LineageBuildTimelineEngine · 搭建时间线

```python
class BuildSchedule(BaseModel):
    schedule_id: str
    name: str
    pipeline_id: str
    cron_expression: str
    timezone: str = "UTC"
    status: Literal["active", "paused", "disabled"] = "active"
    last_run_at: datetime | None = None
    next_run_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

class BuildRun(BaseModel):
    run_id: str
    schedule_id: str
    status: Literal["pending", "running", "success", "failed", "cancelled"]
    started_at: datetime
    finished_at: datetime | None = None
    datasets_built: list[str] = []
    duration_ms: int = 0
    error_message: str = ""

class GanttTask(BaseModel):
    task_id: str
    name: str
    pipeline_id: str = ""
    start_time: datetime
    end_time: datetime
    status: str = "scheduled"  # scheduled / running / success / failed
    dependencies: list[str] = []

class GanttChart(BaseModel):
    chart_id: str
    title: str
    start_date: date
    end_date: date
    tasks: list[GanttTask] = []

_MAX_SCHEDULES = 200
_MAX_RUNS = 200
```

---

## §3 引擎接口

### 3.1 LineageVisualizationEngine

| 方法 | 签名 | 说明 |
|------|------|------|
| `register` | `(view: LineageView) -> LineageView` | 保存视图 |
| `get` | `(view_id: str) -> LineageView` | 获取视图 |
| `list` | `(saved_by: str \| None, graph_mode: str \| None) -> list[LineageView]` | 列出视图，多维过滤 |
| `update` | `(view_id: str, updates: dict) -> LineageView` | 更新视图 |
| `delete` | `(view_id: str) -> None` | 删除视图 |
| `generate_graph` | `(view_id: str) -> LineageGraph` | 生成血缘图 |
| `expand_node` | `(view_id: str, node_id: str) -> LineageGraph` | 展开节点 |
| `collapse_node` | `(view_id: str, node_id: str) -> LineageGraph` | 折叠节点 |
| `color_by` | `(view_id: str, color_scheme: str) -> LineageGraph` | 按规则着色 |
| `share_view` | `(view_id: str, make_public: bool) -> LineageView` | 切换公开/私有 |
| `list_views_by_dataset` | `(dataset_rid: str) -> list[LineageView]` | 按数据集列视图 |

**错误码**：
- `MISSING_NAME`：名称为空
- `MISSING_DATASET`：缺少根数据集
- `INVALID_GRAPH_MODE`：graph_mode 非法
- `INVALID_DIRECTION`：direction 非法
- `INVALID_LAYOUT`：layout 非法
- `INVALID_DEPTH`：depth 不在 [1, 10]
- `INVALID_COLOR_BY`：color_by 非法
- `NOT_FOUND`：视图不存在

**FIFO 淘汰**：视图数 > `_MAX_VIEWS`（200）时，淘汰最早创建的视图。

---

### 3.2 ColumnLineageSearchEngine（增量）

| 方法 | 签名 | 说明 |
|------|------|------|
| `register_column` | `(dataset_rid: str, column_name: str, data_type: str, description: str, tags: list[str]) -> ColumnIndexEntry` | 注册列索引 |
| `get_column` | `(dataset_rid: str, column_name: str) -> ColumnIndexEntry` | 获取列信息 |
| `list_columns` | `(dataset_rid: str) -> list[ColumnIndexEntry]` | 列出数据集所有列 |
| `update_column` | `(dataset_rid: str, column_name: str, updates: dict) -> ColumnIndexEntry` | 更新列信息 |
| `delete_column` | `(dataset_rid: str, column_name: str) -> None` | 删除列索引 |
| `search_columns` | `(keyword: str, data_type: str \| None, tag: str \| None) -> list[ColumnIndexEntry]` | 搜索列（名称模糊匹配 + 类型/标签过滤） |
| `trace_column` | `(dataset_rid: str, column_name: str, direction: str, max_depth: int) -> ColumnTraceResult` | 列级血缘追踪 |
| `build_index` | `(dataset_rid: str) -> int` | 从 lineage_views 数据重建索引，返回索引列数 |

**错误码**：
- `MISSING_DATASET`：数据集为空
- `MISSING_COLUMN`：列名为空
- `INVALID_DIRECTION`：direction 非 upstream/downstream
- `INVALID_DEPTH`：max_depth 不在 [1, 10]
- `NOT_FOUND`：列不存在

**FIFO 淘汰**：索引条目 > `_MAX_COLUMN_INDEX`（200）时，淘汰最早更新的列。

---

### 3.3 LineageBuildTimelineEngine

| 方法 | 签名 | 说明 |
|------|------|------|
| `register_schedule` | `(schedule: BuildSchedule) -> BuildSchedule` | 注册搭建调度 |
| `get_schedule` | `(schedule_id: str) -> BuildSchedule` | 获取调度 |
| `list_schedules` | `(pipeline_id: str \| None, status: str \| None) -> list[BuildSchedule]` | 列出调度，多维过滤 |
| `update_schedule` | `(schedule_id: str, updates: dict) -> BuildSchedule` | 更新调度 |
| `delete_schedule` | `(schedule_id: str) -> None` | 删除调度 |
| `compute_next_run` | `(schedule_id: str) -> datetime` | 计算下次运行时间（基于 cron） |
| `trigger_run` | `(schedule_id: str) -> BuildRun` | 手动触发运行 |
| `complete_run` | `(run_id: str, success: bool, datasets_built: list[str], error_message: str) -> BuildRun` | 完成运行 |
| `get_run` | `(run_id: str) -> BuildRun` | 获取运行记录 |
| `list_runs` | `(schedule_id: str, limit: int) -> list[BuildRun]` | 列运行记录，倒序 |
| `pause_schedule` | `(schedule_id: str) -> BuildSchedule` | 暂停调度 |
| `resume_schedule` | `(schedule_id: str) -> BuildSchedule` | 恢复调度 |
| `get_gantt_chart` | `(start_date: date, end_date: date, pipeline_id: str \| None) -> GanttChart` | 获取甘特图 |

**错误码**：
- `MISSING_NAME`：名称为空
- `MISSING_PIPELINE`：pipeline_id 为空
- `INVALID_CRON`：cron 表达式非法（5 段式校验）
- `INVALID_TIMEZONE`：时区非法（简化：仅校验非空字符串）
- `INVALID_STATUS`：status 非法
- `NOT_FOUND`：调度/运行不存在
- `SCHEDULE_PAUSED`：调度已暂停，触发失败
- `RUN_NOT_FOUND`：运行记录不存在
- `RUN_NOT_RUNNING`：运行不在 running 状态，无法完成

**FIFO 淘汰**：
- 调度数 > `_MAX_SCHEDULES`（200）时，淘汰最早创建的调度
- 运行记录 > `_MAX_RUNS`（200）时，淘汰最早的运行记录

---

## §4 API 端点（FastAPI Router）

Router 文件：`aos_api/routers/lineage_visualization.py`

### 4.1 血缘可视化（10 端点）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/lineage/views` | 注册视图 |
| GET | `/lineage/views/{view_id}` | 获取视图 |
| GET | `/lineage/views` | 列出视图（saved_by / graph_mode 过滤） |
| PUT | `/lineage/views/{view_id}` | 更新视图 |
| DELETE | `/lineage/views/{view_id}` | 删除视图 |
| POST | `/lineage/views/{view_id}/graph` | 生成血缘图 |
| POST | `/lineage/views/{view_id}/nodes/{node_id}/expand` | 展开节点 |
| POST | `/lineage/views/{view_id}/nodes/{node_id}/collapse` | 折叠节点 |
| POST | `/lineage/views/{view_id}/color` | 切换着色方案 |
| POST | `/lineage/views/{view_id}/share` | 切换公开分享 |

### 4.2 列级血缘搜索（6 端点）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/lineage/columns/{dataset_rid}/{column_name}` | 注册列索引 |
| GET | `/lineage/columns/{dataset_rid}/{column_name}` | 获取列信息 |
| GET | `/lineage/columns/{dataset_rid}` | 列出数据集所有列 |
| PUT | `/lineage/columns/{dataset_rid}/{column_name}` | 更新列信息 |
| DELETE | `/lineage/columns/{dataset_rid}/{column_name}` | 删除列索引 |
| GET | `/lineage/columns/search` | 搜索列（keyword / data_type / tag） |
| GET | `/lineage/columns/trace` | 列级追踪（dataset_rid / column_name / direction / max_depth） |
| POST | `/lineage/columns/index/{dataset_rid}` | 重建索引 |

### 4.3 搭建时间线（12 端点）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/lineage/build/schedules` | 注册调度 |
| GET | `/lineage/build/schedules/{schedule_id}` | 获取调度 |
| GET | `/lineage/build/schedules` | 列出调度（pipeline_id / status 过滤） |
| PUT | `/lineage/build/schedules/{schedule_id}` | 更新调度 |
| DELETE | `/lineage/build/schedules/{schedule_id}` | 删除调度 |
| POST | `/lineage/build/schedules/{schedule_id}/next-run` | 计算下次运行 |
| POST | `/lineage/build/schedules/{schedule_id}/trigger` | 手动触发 |
| GET | `/lineage/build/runs/{run_id}` | 获取运行记录 |
| GET | `/lineage/build/runs` | 列出运行记录（schedule_id 过滤） |
| POST | `/lineage/build/schedules/{schedule_id}/pause` | 暂停调度 |
| POST | `/lineage/build/schedules/{schedule_id}/resume` | 恢复调度 |
| GET | `/lineage/build/gantt` | 获取甘特图（start_date / end_date / pipeline_id） |

---

## §5 单元测试计划

总测试数约 55 个：
- LineageVisualizationEngine：~18 测试（CRUD 5 + generate 2 + expand/collapse 2 + color 2 + share 1 + list 过滤 2 + eviction 1 + search 2 + 单例 1）
- ColumnLineageSearchEngine：~18 测试（CRUD 5 + search 4 + trace 3 + build_index 2 + 过滤 2 + eviction 1 + 单例 1）
- LineageBuildTimelineEngine：~20 测试（CRUD 5 + cron 计算 2 + trigger/complete 3 + run 查询 2 + pause/resume 2 + gantt 2 + 过滤 2 + eviction 1 + 单例 1）

---

## §6 技术约束

1. **Singleton 模式**：所有引擎使用 DCL 单例，提供 `get_*()` getter
2. **200 条 FIFO 淘汰**：内存存储上限
3. **FastAPI 路由**：`require_principal` 依赖鉴权
4. **错误映射**：引擎错误 → ApiError，400/404/409 映射
5. **时间**：UTC datetime，ISO 格式
6. **增量原则**：不破坏 W2-E #4 已交付的 lineage_views 接口

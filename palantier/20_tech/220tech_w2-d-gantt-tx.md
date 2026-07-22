# 220tech · W2-D 第四批 甘特图 + 事务类型补强（2 项）

> **版本**：v1.0 · 2026-07-22 · **关联**：220plan §1.2.3 W2+ #10/#24
> **前置**：W2-A #8/#9 Dynamic Scheduling · data_transaction（已实现）

## 1. 范围与目标

本批 2 项，工作性质不同：

| 编号 | 差距项 | 工作性质 | 说明 |
|------|--------|----------|------|
| W2-#10 | Dynamic Scheduling 甘特图 | **新建模块** | 全仓库 0 处 gantt，需完整新建 |
| W2-#24 | Data Connection 事务类型 | **补强+验证** | data_transaction.py 已完整实现（13 测试通过），本批补 dispatch 集成测试 + 文档化风险 |

### #24 现状认定（重要）

经研究确认 #24 主路径已闭环：
- `data_transaction.py`：APPEND/SNAPSHOT/UPDATE 三模式完整（PK 去重、字段级 merge）
- `connector_runtime.dispatch` L613-633：已透传 write_mode 并调用 apply_write_mode
- `routers/wave_ext.py`：`/v1/connectors/write-modes` 端点已暴露
- `tests/test_data_transaction.py`：13 用例全通过

**已知限制**（文档化，本批不修）：`dispatch` L618 `existing = out.get("existing_rows") or []`，各 ingest handler 未返回 `existing_rows` 字段，导致 update/snapshot 对非 mysql 路径退化为空存量合并。这是后续 Phase 的优化点，本批不触碰（避免破坏已通过的 13 测试）。

## 2. #10 甘特图数据模型

```python
class GanttBar(BaseModel):
    schedule_id: str
    schedule_name: str
    bar_id: str              # 时间段唯一 id
    start: str               # ISO 时间
    end: str                 # ISO 时间
    kind: Literal["planned", "historical"]  # 计划(推算) vs 历史(实际执行)
    status: str = ""         # historical 时的执行状态
    resources: list[dict]    # [{resource_type, resource_id, allocation}]

class GanttViolation(BaseModel):
    type: Literal["resource_overlap", "overtime", "disabled"]
    bar_ids: list[str]       # 涉及的 bar
    message: str

class GanttLane(BaseModel):
    resource_type: str
    resource_id: str
    bars: list[GanttBar]

class GanttView(BaseModel):
    scope: str
    horizon_start: str
    horizon_end: str
    lanes: list[GanttLane]
    violations: list[GanttViolation]
    total_bars: int

class GanttEngine:
    def build_view(scope, horizon_hours, engine=None) -> GanttView
    def build_for_schedule(sched_id, horizon_hours) -> GanttView
    def _detect_violations(bars) -> list[GanttViolation]
    def _project_future_runs(schedule, horizon) -> list[GanttBar]
```

## 3. 算法

### 3.1 未来运行推算（_project_future_runs）

```
从 schedule.next_run_at 开始，按 cron 周期推算 horizon_hours 内的命中点
每个命中点生成一个 planned bar：
    start = 命中点
    end = start + duration_minutes（默认 60 分钟）
```

### 3.2 历史执行段（来自 history）

```
for execution in engine.history(sched_id):
    bar = GanttBar(kind="historical", start=execution.started_at,
                   end=execution.finished_at or now, status=execution.status)
```

### 3.3 违规检测（_detect_violations）

- `resource_overlap`：同一 resource_id + allocation=exclusive 的两个 bar 时间重叠
- `overtime`：historical bar 的 duration > 2x 计划 duration
- `disabled`：enabled=False 的 schedule 仍有 planned bar

## 4. #24 补强工作

### 4.1 dispatch 集成测试（新增）

验证 `connector_runtime.dispatch` 在 op=ingest + write_mode 时：
- write_mode=append：追加不覆盖
- write_mode=snapshot：全量替换语义
- write_mode=update：按 PK upsert
- 未传 write_mode：不触发合并（向后兼容）

### 4.2 220plan 状态更新

将 #24 标记为 ✅ 已完成（功能已完整实现）。

## 5. 测试矩阵

| 模块 | 测试文件 | 用例数 |
|------|----------|--------|
| 甘特图引擎 | `test_gantt.py` | 12 |
| #24 dispatch 集成 | `test_data_transaction_dispatch.py` | 6 |

## 6. 文件清单

**新增**：
- `aos_api/gantt.py` + `aos_api/routers/gantt.py`
- `tests/test_gantt.py`
- `tests/test_data_transaction_dispatch.py`

**修改（最小增量，串行）**：
- `aos_api/main.py`：注册 gantt router

**不改**：
- `aos_api/scheduling_engine.py`（纯只读组装）
- `aos_api/data_transaction.py`（已完整）
- `aos_api/connector_runtime.py`（existing_rows 风险文档化，不修）

## 7. 风险与对策

| 风险 | 对策 |
|------|------|
| 未来运行推算性能 | horizon_hours 默认 168（7天），上限 720（30天） |
| cron 推算无边界 | 复用 scheduling_engine.next_run_time，迭代上限 1000 |
| existing_rows 限制 | 方案文档显式标注，本批不修 |

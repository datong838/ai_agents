# 220tech · W2-Z · Pipeline 类型语义组（#94 / #95 / #96）

> **版本**：v1.0 · 2026-07-22
> **状态**：✅ 方案定稿 · 可编码
> **对齐**：
> - 差距分析 [220w](./220w-与目标系统差距对照分析.md) §4.2 #94/#95/#96 + §3.2 输出系统
> - 产品方案 [06](../06-数据管道Pipeline-Builder产品方案.md) §3（管道类型）· [06a](../06a-增量与流式管道产品方案.md) §2（Incremental/Streaming）
> - 技术方案 [T06](./T06-数据管道详细技术方案.md) §4（管道类型语义）
> - 上游 W1-5 Pipeline 四阶段管道 · W2-6 PipelineOutputEngine（6 种 WriteMode）
> **范围**：W2-Z 收口 Pipeline 类型区分与增量/流式处理语义三件 — Pipeline Types（Batch/Incremental/Streaming 三类型 + 处理语义）/ Incremental Pipeline（watermark + 变更捕获 + checkpoint）/ Streaming Pipeline（窗口 + 状态化操作）
> **不替换底层**：本组是管道类型语义层，不重写 PipelineEditor/PipelineOutputEngine/Funnel 四阶段

---

## 0. 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文回答 | 文档与代码注释均中文 |
| 先方案后编码 | 本文先定稿，再写引擎/路由/测试 |
| 最小更改 | 仅新增 `aos_api/pipeline_type_semantics.py` + `aos_api/routers/pipeline_type_semantics.py` + `tests/test_pipeline_type_semantics.py`；`main.py` 加 2 行 |
| 不影响已有功能 | 三引擎纯新增；不改动 pipelines/pipeline_output/expectation 现有逻辑 |
| 自测验证 | 单测全绿 + 全量回归 + 方案对照 |
| 符合方案军规 | 三类型语义与 220w §4.2 一致；Incremental watermark/CDC 与 06a §2 一致；Streaming 窗口与 T06 §4 一致 |

---

## 1. 背景与边界

### 1.1 现状

| 能力 | 现状 | 缺口 |
| --- | --- | --- |
| Pipeline Types | 有基础概念（pipeline_kind 字段）；无三种类型的处理语义区分 | 🔴 缺 |
| Incremental Pipeline | 无增量处理；无变更捕获；无 checkpoint | 🔴 缺 |
| Streaming Pipeline | 无流式处理；无窗口；无状态化操作 | 🔴 缺 |

### 1.2 边界

- ✅ 本组做：
  - #94 Pipeline Types：Batch/Incremental/Streaming 三类型定义 + 处理语义（触发/状态机/容错）+ CRUD
  - #95 Incremental Pipeline：watermark 水位线 + CDC 变更捕获 + checkpoint 检查点 + 增量窗口执行
  - #96 Streaming Pipeline：tumbling/sliding/session 三种窗口 + watermark + 状态化操作 + 事件处理
- ❌ 本组不做：
  - 实际数据源连接（属数据连接层）
  - 真实流式引擎接入（Kafka/Flink 等属 Phase 5）
  - 管道编辑器 UI（属前端）

---

## 2. 数据模型

### 2.1 #94 Pipeline Types

```python
class PipelineTypeSpec(BaseModel):
    """管道类型定义。"""
    type: str                          # batch / incremental / streaming
    name: str
    description: str = ""
    trigger_semantics: str             # scheduled / on_change / continuous
    state_machine: list[str]           # 状态序列 e.g. ["pending","running","succeeded","failed"]
    fault_strategy: str                # restart / skip / checkpoint_replay
    default_write_mode: str = "append" # 默认 WriteMode
    supports_checkpoint: bool = False
    supports_windowing: bool = False
    enabled: bool = True


_VALID_PIPELINE_TYPES = {"batch", "incremental", "streaming"}
_VALID_TRIGGER_SEMANTICS = {"scheduled", "on_change", "continuous"}
_VALID_FAULT_STRATEGIES = {"restart", "skip", "checkpoint_replay"}
```

### 2.2 #95 Incremental Pipeline

```python
class Watermark(BaseModel):
    """水位线。"""
    pipeline_id: str
    field: str                         # watermark 字段（如 updated_at）
    value: str = ""                    # 当前水位值
    updated_at: float = 0.0


class Checkpoint(BaseModel):
    """增量检查点。"""
    id: str
    pipeline_id: str
    sequence: int = 0                  # 序列号
    watermark_value: str = ""
    rows_processed: int = 0
    status: str = "pending"            # pending / committed / failed
    created_at: float = 0.0
    committed_at: float = 0.0


class ChangeRecord(BaseModel):
    """变更捕获记录。"""
    id: str
    pipeline_id: str
    operation: str                     # insert / update / delete
    pk: str
    payload: dict[str, Any] = {}
    watermark_value: str = ""
    captured_at: float = 0.0


class IncrementalRunResult(BaseModel):
    """增量运行结果。"""
    run_id: str
    pipeline_id: str
    changes: list[ChangeRecord] = []
    rows_processed: int = 0
    new_watermark: str = ""
    checkpoint_id: str = ""
    status: str = "completed"          # completed / skipped / failed
```

### 2.3 #96 Streaming Pipeline

```python
class WindowSpec(BaseModel):
    """窗口规格。"""
    type: str                          # tumbling / sliding / session
    size_ms: int = 0                   # 窗口大小（毫秒）
    slide_ms: int = 0                  # sliding 滑动步长
    gap_ms: int = 0                    # session 会话间隔
    watermark_field: str = "event_ts"


_VALID_WINDOW_TYPES = {"tumbling", "sliding", "session"}


class StreamEvent(BaseModel):
    """流事件。"""
    id: str
    pipeline_id: str
    key: str                           # 分区键
    event_ts: float = 0.0              # 事件时间
    payload: dict[str, Any] = {}
    processed: bool = False


class WindowState(BaseModel):
    """窗口状态。"""
    window_id: str
    pipeline_id: str
    spec: WindowSpec
    start_ts: float = 0.0
    end_ts: float = 0.0
    events: list[StreamEvent] = []
    open: bool = True
    emitted: bool = False


class StreamProcessResult(BaseModel):
    """流处理结果。"""
    pipeline_id: str
    processed: int = 0
    windows_opened: int = 0
    windows_closed: int = 0
    watermark_advanced: float = 0.0
```

---

## 3. 引擎设计

文件：`aos_api/pipeline_type_semantics.py`（新增，3 个引擎）

### 3.1 PipelineTypeEngine（#94）

```python
class PipelineTypeEngine:
    def register(self, spec: PipelineTypeSpec) -> PipelineTypeSpec: ...
    def get(self, ptype: str) -> PipelineTypeSpec: ...
    def list(self, enabled_only: bool = False) -> list[PipelineTypeSpec]: ...
    def update(self, ptype: str, updates: dict[str, Any]) -> PipelineTypeSpec: ...
    def delete(self, ptype: str) -> bool: ...
    def validate_run(self, ptype: str, write_mode: str) -> dict[str, Any]: ...
    """校验运行：返回 type/write_mode 是否匹配 + 处理语义提示"""
```

**register 流程**：
1. 校验 type/trigger_semantics/fault_strategy 在白名单
2. 默认 batch→scheduled+append、incremental→on_change+upsert、streaming→continuous+append
3. update 禁改 type（IMMUTABLE_FIELD）
4. 三类型预置：DEFAULT_PIPELINE_TYPES 含 batch/incremental/streaming 三条

### 3.2 IncrementalPipelineEngine（#95）

```python
class IncrementalPipelineEngine:
    def get_watermark(self, pipeline_id: str) -> Watermark: ...
    def set_watermark(self, pipeline_id: str, field: str, value: str) -> Watermark: ...
    def register_change(self, rec: ChangeRecord) -> ChangeRecord: ...
    """注册一条变更捕获记录（insert/update/delete）"""
    def list_changes(
        self, pipeline_id: str, op: str | None = None,
        since_watermark: str | None = None, limit: int = 50,
    ) -> list[ChangeRecord]: ...
    def create_checkpoint(self, pipeline_id: str) -> Checkpoint: ...
    def commit_checkpoint(self, checkpoint_id: str) -> Checkpoint: ...
    def list_checkpoints(self, pipeline_id: str) -> list[Checkpoint]: ...
    def process_increment(
        self, pipeline_id: str,
        changes: list[ChangeRecord] | None = None,
    ) -> IncrementalRunResult: ...
    """增量执行：取 watermark 之后的变更 → 处理 → 提交 checkpoint → 推进 watermark"""
```

**process_increment 流程**：
1. 取当前 watermark
2. 收集 watermark 之后的变更（注册的或传入的）
3. 创建 checkpoint(pending)
4. 处理变更（计数）
5. 提交 checkpoint(committed)
6. 推进 watermark 到最新变更的 watermark_value
7. 若无变更 → status=skipped

### 3.3 StreamingPipelineEngine（#96）

```python
class StreamingPipelineEngine:
    def register_window(self, pipeline_id: str, spec: WindowSpec) -> WindowSpec: ...
    def get_window(self, pipeline_id: str) -> WindowSpec: ...
    def ingest(self, event: StreamEvent) -> StreamEvent: ...
    """摄入事件 → 按窗口分配 → 更新窗口状态"""
    def list_events(
        self, pipeline_id: str, processed_only: bool = False, limit: int = 50,
    ) -> list[StreamEvent]: ...
    def list_windows(
        self, pipeline_id: str, open_only: bool = False, limit: int = 50,
    ) -> list[WindowState]: ...
    def advance_watermark(
        self, pipeline_id: str, new_watermark: float,
    ) -> StreamProcessResult: ...
    """推进水位线 → 关闭并发射到期窗口 → 返回处理结果"""
    def close_window(self, window_id: str) -> WindowState: ...
    """手动关闭窗口"""
```

**ingest + advance_watermark 流程**：
1. ingest：按 event_ts + window spec 计算所属窗口
   - tumbling：窗口 = floor(event_ts / size) * size
   - sliding：可能落入多个窗口
   - session：按 gap_ms 合并/新建会话
2. advance_watermark：关闭 end_ts <= watermark 的窗口，标记 emitted=True
3. 窗口关闭后不可再摄入事件（WINDOW_CLOSED）

### 3.4 单例与持久化

- 3 个引擎均用**双重检查锁单例**
- 内存态为主，各 200 条上限（types/changes/checkpoints/windows/events）

---

## 4. API 设计

文件：`aos_api/routers/pipeline_type_semantics.py`（新增）

### 4.1 #94 Pipeline Types

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/pipeline-types` | 注册管道类型 |
| GET | `/v1/pipeline-types` | 列表 |
| GET | `/v1/pipeline-types/{ptype}` | 单条 |
| PUT | `/v1/pipeline-types/{ptype}` | 更新 |
| DELETE | `/v1/pipeline-types/{ptype}` | 删除 |
| POST | `/v1/pipeline-types/{ptype}/validate-run` | 校验运行 |

### 4.2 #95 Incremental Pipeline

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/v1/pipelines/{pipeline_id}/watermark` | 获取水位线 |
| PUT | `/v1/pipelines/{pipeline_id}/watermark` | 设置水位线 |
| POST | `/v1/pipelines/{pipeline_id}/changes` | 注册变更 |
| GET | `/v1/pipelines/{pipeline_id}/changes` | 变更列表 |
| POST | `/v1/pipelines/{pipeline_id}/checkpoints` | 创建检查点 |
| POST | `/v1/pipelines/checkpoints/{checkpoint_id}/commit` | 提交检查点 |
| GET | `/v1/pipelines/{pipeline_id}/checkpoints` | 检查点列表 |
| POST | `/v1/pipelines/{pipeline_id}/process-increment` | 增量执行 |

### 4.3 #96 Streaming Pipeline

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/pipelines/{pipeline_id}/windows` | 注册窗口 |
| GET | `/v1/pipelines/{pipeline_id}/windows` | 窗口列表 |
| POST | `/v1/pipelines/{pipeline_id}/events` | 摄入事件 |
| GET | `/v1/pipelines/{pipeline_id}/events` | 事件列表 |
| POST | `/v1/pipelines/{pipeline_id}/advance-watermark` | 推进水位线 |
| POST | `/v1/pipelines/windows/{window_id}/close` | 手动关窗 |

---

## 5. 集成点

### 5.1 main.py（最小更改）

```python
from aos_api.routers import (..., pipeline_type_semantics, ...)
application.include_router(pipeline_type_semantics.router)
```

### 5.2 与 W2-6 协同

- `PipelineTypeEngine.validate_run` 可校验 PipelineOutputEngine 的 write_mode 是否匹配管道类型
- `IncrementalPipelineEngine.process_increment` 可调用 PipelineOutputEngine.execute(upsert)
- `StreamingPipelineEngine.advance_watermark` 发射的窗口可触发 PipelineOutputEngine.execute(append)

### 5.3 与 06a §2 对齐

- Incremental：watermark 推进式增量 + checkpoint 断点续传 + CDC insert/update/delete
- Streaming：事件时间 watermark + 三种窗口 + 状态化窗口管理

---

## 6. 测试计划

文件：`tests/test_pipeline_type_semantics.py`（新增，约 45 个用例）

### 6.1 PipelineTypeEngine（14）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | list 默认 | 返回 3 类型（batch/incremental/streaming） |
| 2 | get batch | 返回 batch 规格 |
| 3 | get 未找到 | NOT_FOUND |
| 4 | register 自定义 | 返回带 type |
| 5 | register 未知 type | INVALID_TYPE |
| 6 | register 未知 trigger | INVALID_TRIGGER |
| 7 | register 未知 fault | INVALID_FAULT_STRATEGY |
| 8 | update | 修改后 get 返回新值 |
| 9 | update 禁改 type | IMMUTABLE_FIELD |
| 10 | delete | 删除成功 |
| 11 | list enabled_only | 过滤禁用 |
| 12 | validate_run 匹配 | ok=True |
| 13 | validate_run 不匹配 | ok=False + 提示 |
| 14 | get 未注册自定义 | NOT_FOUND |

### 6.2 IncrementalPipelineEngine（16）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | set_watermark | 返回设置值 |
| 2 | get_watermark 未设置 | 返回空 value |
| 3 | register_change insert | 返回带 id |
| 4 | register_change update | operation=update |
| 5 | register_change delete | operation=delete |
| 6 | register_change 未知 op | INVALID_OPERATION |
| 7 | list_changes 默认 | 列表 |
| 8 | list_changes 按 op 过滤 | 仅匹配 |
| 9 | list_changes since_watermark | 仅水位之后 |
| 10 | create_checkpoint | status=pending |
| 11 | commit_checkpoint | status=committed |
| 12 | commit_checkpoint 未找到 | NOT_FOUND |
| 13 | list_checkpoints | 列表 |
| 14 | process_increment 有变更 | status=completed + watermark 推进 |
| 15 | process_increment 无变更 | status=skipped |
| 16 | process_increment 创建+提交 checkpoint | checkpoint_id 非空 |

### 6.3 StreamingPipelineEngine（15）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register_window tumbling | 返回规格 |
| 2 | register_window sliding | slide_ms 设置 |
| 3 | register_window session | gap_ms 设置 |
| 4 | register_window 未知类型 | INVALID_WINDOW_TYPE |
| 5 | get_window | 返回规格 |
| 6 | ingest tumbling 事件 | 分配到窗口 |
| 7 | ingest sliding 事件 | 可能多窗口 |
| 8 | ingest session 事件合并 | 同 key 合并 |
| 9 | list_events | 列表 |
| 10 | list_events processed_only | 过滤 |
| 11 | list_windows open_only | 仅开窗 |
| 12 | advance_watermark | 关闭到期窗口 |
| 13 | advance_watermark 推进 watermark | 返回处理结果 |
| 14 | close_window 手动 | open=False |
| 15 | close_window 未找到 | NOT_FOUND |

---

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 窗口计算复杂导致事件分配错误 | tumbling 用 floor 公式；sliding 枚举所有覆盖窗口；session 按 gap 合并 |
| watermark 推进过快导致窗口丢失 | advance_watermark 仅关闭 end_ts <= watermark 的窗口，未到期保留 |
| 增量 checkpoint 失败 | checkpoint pending→committed 状态机；失败保留 pending 可重试 |
| 变更捕获顺序乱 | since_watermark 过滤 + watermark_value 单调递进 |
| 三类型预置被误删 | delete 允许删自定义；预置三条可在 register 重建 |

---

## 8. 交付物清单

| 路径 | 状态 | 说明 |
| --- | --- | --- |
| `docs/palantier/20_tech/220tech_w2-z-pipeline-type-semantics.md` | ✅ 本文件 | 微规约 |
| `aos_api/pipeline_type_semantics.py` | ⬜ 待编码 | 3 引擎 |
| `aos_api/routers/pipeline_type_semantics.py` | ⬜ 待编码 | ~20 端点 |
| `tests/test_pipeline_type_semantics.py` | ⬜ 待编码 | ~45 用例 |
| `aos_api/main.py` | ⬜ +2 行 | import + include_router |

---

## 9. 顺手清账

W2-Z 编码同时，确认 #92/#93 基础已存在（`expectation.py` + `pipeline_output.py` 均有实现+测试），在看板更新阶段标记为已完成。

---

*v1.0 · w2-z*

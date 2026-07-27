# W2-AI · Data Connection 推送与导出组（#119 #120 #121）

> **所属阶段**：Phase 8 · W2+ 中优先级
> **批次编号**：W2-AI（v4.8）
> **对应需求**：#119 Push-based Ingestion · #120 Export 文件 · #121 Export 表
> **设计原则**：与 W2-AH Streaming Sync / FileProcessing 保持一致的引擎+路由+单测模式，200 条 FIFO 上限。

---

## 1. 模块总览

| 子项 | 引擎类 | 路由前缀 | 核心能力 |
|------|--------|----------|----------|
| #119 | PushIngestionEngine | `/v1/push-ingestion` | OAuth2 Client Credentials 认证 + 推送端点 + 消息校验 + 速率限制 |
| #120 | FileExportEngine | `/v1/file-exports` | Dataset → S3/ABFS/HDFS 文件导出 + 格式 + 压缩 + 导出任务状态 |
| #121 | TableExportEngine | `/v1/table-exports` | 增量镜像 + SNAPSHOT 截断 + 导出任务（full/incremental/snapshot 三模式） |

---

## 2. #119 Push-based Ingestion

### 2.1 数据模型

```python
class PushIngestionSource(BaseModel):
    id: str                          # pis-xxx
    name: str
    description: str = ""
    target_stream: str
    auth_type: str                   # oauth2_client_credentials | api_key | none
    auth_config: dict = {}           # token_url / client_id / client_secret / scope
    rate_limit_per_minute: int = 60
    enabled: bool = True
    created_at: float
    last_received_at: float = 0.0
    total_messages: int = 0
    error_count: int = 0

class PushIngestionMessage(BaseModel):
    message_id: str
    source_id: str
    payload: dict
    received_at: float
    status: str                      # accepted | rejected | forwarded
    error_message: str = ""

class PushIngestionResult(BaseModel):
    accepted: int
    rejected: int
    messages: list[PushIngestionMessage]
```

### 2.2 引擎接口（PushIngestionEngine）

- `register(source: PushIngestionSource) -> PushIngestionSource` — 注册推送源，生成 id
- `get(source_id: str) -> PushIngestionSource` — 按 id 获取
- `list(name: str = None, enabled: bool = None) -> list[PushIngestionSource]` — 列表过滤
- `update(source_id: str, updates: dict) -> PushIngestionSource` — 更新
- `delete(source_id: str) -> bool` — 删除
- `receive_message(source_id: str, payload: dict, auth_token: str = None) -> PushIngestionMessage` — 接收单条消息，校验认证+速率
- `receive_batch(source_id: str, payloads: list[dict]) -> PushIngestionResult` — 批量接收
- `list_messages(source_id: str, limit: int = 50) -> list[PushIngestionMessage]` — 历史消息倒序
- `validate_token(source_id: str, token: str) -> bool` — OAuth2 token 校验（简化模式）

### 2.3 API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/v1/push-ingestion/sources` | 注册推送源 |
| GET | `/v1/push-ingestion/sources` | 列表 |
| GET | `/v1/push-ingestion/sources/{source_id}` | 获取详情 |
| PATCH | `/v1/push-ingestion/sources/{source_id}` | 更新 |
| DELETE | `/v1/push-ingestion/sources/{source_id}` | 删除 |
| POST | `/v1/push-ingestion/sources/{source_id}/receive` | 接收单条消息 |
| POST | `/v1/push-ingestion/sources/{source_id}/receive-batch` | 批量接收 |
| GET | `/v1/push-ingestion/sources/{source_id}/messages` | 消息历史 |

### 2.4 错误码

- `MISSING_NAME` — name 为空
- `INVALID_AUTH_TYPE` — 不支持的认证类型
- `INVALID_RATE_LIMIT` — rate_limit <= 0
- `NOT_FOUND` — source 不存在
- `SOURCE_DISABLED` — 推送源已禁用
- `AUTH_FAILED` — 认证失败
- `RATE_LIMIT_EXCEEDED` — 超出速率限制
- `EMPTY_PAYLOAD` — payload 为空

### 2.5 存储上限

- 推送源：200 条 FIFO
- 每个 source 消息记录：200 条 FIFO

---

## 3. #120 Export 文件

### 3.1 数据模型

```python
class FileExportTask(BaseModel):
    id: str                          # fex-xxx
    name: str
    dataset_rid: str
    target_type: str                 # s3 | abfs | hdfs
    target_path: str
    file_format: str                 # csv | parquet | json | avro
    compression: str = "none"        # none | gzip | snappy | lz4
    row_limit: int = 0               # 0 = 无限制
    filter_expr: str = ""
    status: str                      # pending | running | completed | failed
    total_rows: int = 0
    exported_rows: int = 0
    file_size_bytes: int = 0
    error_message: str = ""
    created_at: float
    started_at: float = 0.0
    completed_at: float = 0.0
    output_files: list[str] = []
```

### 3.2 引擎接口（FileExportEngine）

- `register(task: FileExportTask) -> FileExportTask` — 创建导出任务
- `get(task_id: str) -> FileExportTask` — 按 id 获取
- `list(dataset_rid: str = None, status: str = None) -> list[FileExportTask]` — 列表过滤
- `update(task_id: str, updates: dict) -> FileExportTask` — 更新配置（仅 pending 态可改）
- `delete(task_id: str) -> bool` — 删除
- `start(task_id: str) -> FileExportTask` — 启动导出（pending → running）
- `cancel(task_id: str) -> FileExportTask` — 取消（running → failed）
- `complete(task_id: str, exported_rows: int, file_size: int, output_files: list[str]) -> FileExportTask` — 标记完成
- `fail(task_id: str, error_message: str) -> FileExportTask` — 标记失败
- `get_progress(task_id: str) -> dict` — 进度信息 {status, total_rows, exported_rows, pct}

### 3.3 API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/v1/file-exports` | 创建导出任务 |
| GET | `/v1/file-exports` | 列表 |
| GET | `/v1/file-exports/{task_id}` | 获取详情 |
| PATCH | `/v1/file-exports/{task_id}` | 更新配置 |
| DELETE | `/v1/file-exports/{task_id}` | 删除 |
| POST | `/v1/file-exports/{task_id}/start` | 启动 |
| POST | `/v1/file-exports/{task_id}/cancel` | 取消 |
| GET | `/v1/file-exports/{task_id}/progress` | 进度 |

### 3.4 错误码

- `MISSING_NAME` — name 为空
- `MISSING_DATASET_RID` — dataset_rid 为空
- `INVALID_TARGET_TYPE` — 不支持的目标类型
- `INVALID_FORMAT` — 不支持的文件格式
- `INVALID_COMPRESSION` — 不支持的压缩方式
- `NOT_FOUND` — task 不存在
- `TASK_NOT_PENDING` — 非 pending 态不可更新/启动
- `TASK_NOT_RUNNING` — 非 running 态不可取消/完成
- `ALREADY_COMPLETED` — 已完成任务不可重复操作

### 3.5 存储上限

- 导出任务：200 条 FIFO

---

## 4. #121 Export 表

### 4.1 数据模型

```python
class TableExportTask(BaseModel):
    id: str                          # tex-xxx
    name: str
    source_dataset_rid: str
    target_table: str
    export_mode: str                 # full | incremental | snapshot
    primary_keys: list[str] = []
    watermark_column: str = ""       # 增量模式用
    last_watermark: str = ""
    truncate_on_snapshot: bool = True  # snapshot 模式是否先截断
    status: str                      # pending | running | completed | failed
    total_rows: int = 0
    processed_rows: int = 0
    inserted_rows: int = 0
    updated_rows: int = 0
    deleted_rows: int = 0
    error_message: str = ""
    created_at: float
    started_at: float = 0.0
    completed_at: float = 0.0

class TableExportRun(BaseModel):
    run_id: str
    task_id: str
    mode: str
    status: str
    started_at: float
    completed_at: float = 0.0
    rows_processed: int = 0
    rows_inserted: int = 0
    rows_updated: int = 0
    rows_deleted: int = 0
    error_message: str = ""
```

### 4.2 引擎接口（TableExportEngine）

- `register(task: TableExportTask) -> TableExportTask` — 注册表导出任务
- `get(task_id: str) -> TableExportTask` — 按 id 获取
- `list(dataset_rid: str = None, status: str = None, mode: str = None) -> list[TableExportTask]` — 列表过滤
- `update(task_id: str, updates: dict) -> TableExportTask` — 更新配置
- `delete(task_id: str) -> bool` — 删除
- `start_run(task_id: str) -> TableExportRun` — 启动一次执行
- `complete_run(run_id: str, stats: dict) -> TableExportRun` — 完成执行，推进 watermark
- `fail_run(run_id: str, error_message: str) -> TableExportRun` — 标记执行失败
- `list_runs(task_id: str, limit: int = 20) -> list[TableExportRun]` — 执行历史倒序
- `get_latest_run(task_id: str) -> TableExportRun | None` — 最近一次执行

### 4.3 API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/v1/table-exports` | 创表导出任务 |
| GET | `/v1/table-exports` | 列表 |
| GET | `/v1/table-exports/{task_id}` | 获取详情 |
| PATCH | `/v1/table-exports/{task_id}` | 更新配置 |
| DELETE | `/v1/table-exports/{task_id}` | 删除 |
| POST | `/v1/table-exports/{task_id}/runs` | 启动一次执行 |
| GET | `/v1/table-exports/{task_id}/runs` | 执行历史 |
| GET | `/v1/table-exports/{task_id}/runs/latest` | 最近执行 |
| POST | `/v1/table-exports/runs/{run_id}/complete` | 完成执行 |
| POST | `/v1/table-exports/runs/{run_id}/fail` | 标记失败 |

### 4.4 错误码

- `MISSING_NAME` — name 为空
- `MISSING_DATASET` — source_dataset_rid 为空
- `INVALID_MODE` — 不支持的导出模式
- `INCREMENTAL_REQUIRES_WATERMARK` — incremental 模式必须指定 watermark_column
- `SNAPSHOT_REQUIRES_PK` — snapshot 模式建议有 PK（warning 级别，不阻断）
- `NOT_FOUND` — task 不存在
- `RUN_NOT_FOUND` — run 不存在
- `TASK_NOT_PENDING` — 非 pending 不可改配置
- `RUN_NOT_RUNNING` — 非 running 态不可完成/失败
- `ALREADY_COMPLETED` — 已完成 run 不可重复操作

### 4.5 存储上限

- 表导出任务：200 条 FIFO
- 每个 task 的 run 记录：200 条 FIFO

---

## 5. 测试计划

### 5.1 PushIngestionEngine（~16 个）
- register / get / list / update / delete 基础 CRUD（5）
- 认证类型校验 + 速率限制校验（3）
- receive_message 成功 / 认证失败 / 速率超限（3）
- receive_batch 混合结果（1）
- list_messages 倒序 + limit（2）
- validate_token oauth2 / api_key / none（2）

### 5.2 FileExportEngine（~15 个）
- register / get / list / update / delete 基础 CRUD（5）
- 类型/格式/压缩校验（3）
- start / complete / fail 状态机（3）
- cancel running → failed（1）
- get_progress 计算百分比（1）
- 非 pending 不可更新（1）
- 200 条上限（1）

### 5.3 TableExportEngine（~15 个）
- register / get / list / update / delete 基础 CRUD（5）
- 模式校验 + incremental 需要 watermark（3）
- start_run + complete_run 推进 watermark（2）
- fail_run（1）
- list_runs 倒序 + limit（1）
- get_latest_run（1）
- snapshot truncate 行为（1）
- 200 条上限（1）

### 5.4 单例（3 个）
- 三个引擎单例各一个

**合计：~49 个测试**

---

## 6. 文件清单

| 文件 | 说明 |
|------|------|
| `aos_api/data_connection_export.py` | 三引擎 + 数据模型 + 错误类 |
| `aos_api/routers/data_connection_export.py` | 三路由 + 端点 + 错误映射 |
| `tests/test_data_connection_export.py` | ~49 个单元测试 |
| `aos_api/main.py` | 新增 import + include_router |

---

*W2-AI · #119 #120 #121 · v4.8*

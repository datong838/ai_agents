# W2-AJ · Data Connection 流导出与 Webhook 组（#122 #123 #124）

> **所属阶段**：Phase 8 · W2+ 中优先级
> **批次编号**：W2-AJ（v4.9）
> **对应需求**：#122 Export 流 · #123 Webhooks 多步调用 · #124 Webhooks 输出参数
> **设计原则**：与 W2-AI Export 保持一致的引擎+路由+单测模式，200 条 FIFO 上限。

---

## 1. 模块总览

| 子项 | 引擎类 | 路由前缀 | 核心能力 |
|------|--------|----------|----------|
| #122 | StreamExportEngine | `/v1/stream-exports` | Stream → Kafka/Kinesis/PubSub 流式导出 + 分区策略 + 状态 |
| #123 | WebhookPipelineEngine | `/v1/webhook-pipelines` | 多步 Webhook 调用编排 Call1→Call2，参数引用传递 |
| #124 | WebhookOutputEngine | `/v1/webhook-outputs` | 从响应提取字段 + 类型转换 + 输出映射 |

---

## 2. #122 Export 流

### 2.1 数据模型

```python
class StreamExportTask(BaseModel):
    id: str                          # sex-xxx
    name: str
    source_stream: str
    target_type: str                 # kafka | kinesis | pubsub
    target_config: dict              # brokers / stream_name / topic / region
    partition_strategy: str = "round_robin"  # round_robin | key_hash | random
    key_field: str = ""
    batch_size: int = 100
    enabled: bool = True
    status: str                      # stopped | running | error
    total_events: int = 0
    last_event_at: float = 0.0
    error_message: str = ""
    created_at: float

class StreamExportEvent(BaseModel):
    event_id: str
    task_id: str
    payload: dict
    key: str = ""
    partition: int = 0
    status: str                      # pending | sent | failed
    sent_at: float = 0.0
    error_message: str = ""
```

### 2.2 引擎接口（StreamExportEngine）

- `register(task: StreamExportTask) -> StreamExportTask` — 创建流导出任务
- `get(task_id: str) -> StreamExportTask` — 按 id 获取
- `list(source_stream: str = None, status: str = None) -> list[StreamExportTask]` — 列表过滤
- `update(task_id: str, updates: dict) -> StreamExportTask` — 更新配置
- `delete(task_id: str) -> bool` — 删除
- `start(task_id: str) -> StreamExportTask` — 启动导出
- `stop(task_id: str) -> StreamExportTask` — 停止导出
- `publish_event(task_id: str, payload: dict, key: str = "") -> StreamExportEvent` — 发布单条事件
- `publish_batch(task_id: str, events: list[dict]) -> list[StreamExportEvent]` — 批量发布
- `list_events(task_id: str, limit: int = 50) -> list[StreamExportEvent]` — 事件历史倒序

### 2.3 错误码

- `MISSING_NAME` — name 为空
- `MISSING_SOURCE_STREAM` — source_stream 为空
- `INVALID_TARGET_TYPE` — 不支持的目标类型
- `INVALID_PARTITION_STRATEGY` — 不支持的分区策略
- `INVALID_BATCH_SIZE` — batch_size <= 0
- `NOT_FOUND` — task 不存在
- `TASK_NOT_STOPPED` — 非 stopped 态不可启动
- `TASK_NOT_RUNNING` — 非 running 态不可停止/发布

### 2.4 存储上限

- 流导出任务：200 条 FIFO
- 每个 task 事件记录：200 条 FIFO

---

## 3. #123 Webhooks 多步调用

### 3.1 数据模型

```python
class WebhookPipelineStep(BaseModel):
    step_id: str
    name: str
    url: str
    method: str = "POST"              # GET | POST | PUT | PATCH | DELETE
    auth_type: str = "none"           # none | bearer | basic | api_key | hmac
    auth_config: dict = {}
    request_template: dict = {}       # 支持 {{step1.response.data.id}} 引用
    headers: dict = {}
    timeout_ms: int = 30000
    retry_count: int = 0
    condition: str = ""               # 条件表达式，满足才执行
    output_mapping: dict = {}         # 输出变量名 -> 响应路径

class WebhookPipeline(BaseModel):
    id: str                           # wpl-xxx
    name: str
    description: str = ""
    steps: list[WebhookPipelineStep]
    status: str                       # draft | active | disabled
    created_at: float
    total_runs: int = 0

class PipelineRun(BaseModel):
    run_id: str
    pipeline_id: str
    status: str                       # running | completed | failed
    started_at: float
    completed_at: float = 0.0
    current_step: int = 0
    step_results: list[dict] = []     # 每步结果
    error_message: str = ""
    outputs: dict = {}                # 最终输出
```

### 3.2 引擎接口（WebhookPipelineEngine）

- `register(pipeline: WebhookPipeline) -> WebhookPipeline` — 创建管道
- `get(pipeline_id: str) -> WebhookPipeline` — 按 id 获取
- `list(name: str = None, status: str = None) -> list[WebhookPipeline]` — 列表过滤
- `update(pipeline_id: str, updates: dict) -> WebhookPipeline` — 更新
- `delete(pipeline_id: str) -> bool` — 删除
- `add_step(pipeline_id: str, step: WebhookPipelineStep) -> WebhookPipeline` — 添加步骤
- `remove_step(pipeline_id: str, step_id: str) -> WebhookPipeline` — 移除步骤
- `reorder_steps(pipeline_id: str, step_order: list[str]) -> WebhookPipeline` — 重排序
- `run(pipeline_id: str, initial_input: dict) -> PipelineRun` — 执行管道
- `list_runs(pipeline_id: str, limit: int = 20) -> list[PipelineRun]` — 执行历史倒序
- `get_run(run_id: str) -> PipelineRun` — 获取执行详情

### 3.3 错误码

- `MISSING_NAME` — name 为空
- `EMPTY_STEPS` — steps 为空
- `DUPLICATE_STEP_ID` — step_id 重复
- `INVALID_METHOD` — 不支持的 HTTP 方法
- `INVALID_AUTH_TYPE` — 不支持的认证类型
- `INVALID_TIMEOUT` — timeout <= 0
- `NOT_FOUND` — pipeline 不存在
- `STEP_NOT_FOUND` — step 不存在
- `RUN_NOT_FOUND` — run 不存在
- `PIPELINE_DISABLED` — 管道已禁用

### 3.4 存储上限

- 管道：200 条 FIFO
- 每个管道 run 记录：200 条 FIFO

---

## 4. #124 Webhooks 输出参数

### 4.1 数据模型

```python
class OutputFieldMapping(BaseModel):
    field_id: str
    source_path: str                  # 响应 JSON 路径，如 data.user.id
    target_name: str                  # 输出变量名
    target_type: str = "string"       # string | integer | float | boolean | json
    required: bool = False
    default_value: object = None

class WebhookOutputConfig(BaseModel):
    id: str                           # woc-xxx
    name: str
    description: str = ""
    webhook_id: str                   # 关联的 webhook
    output_fields: list[OutputFieldMapping]
    response_code_field: str = ""     # 业务码字段路径
    success_codes: list[str] = []     # 成功码列表
    error_message_field: str = ""     # 错误消息字段路径
    created_at: float

class OutputExtractionResult(BaseModel):
    success: bool
    fields: dict                      # 提取的字段
    missing_required: list[str]
    errors: list[str]
    raw_response: dict
```

### 4.2 引擎接口（WebhookOutputEngine）

- `register(config: WebhookOutputConfig) -> WebhookOutputConfig` — 注册输出配置
- `get(config_id: str) -> WebhookOutputConfig` — 按 id 获取
- `list(webhook_id: str = None, name: str = None) -> list[WebhookOutputConfig]` — 列表过滤
- `update(config_id: str, updates: dict) -> WebhookOutputConfig` — 更新
- `delete(config_id: str) -> bool` — 删除
- `add_field(config_id: str, field: OutputFieldMapping) -> WebhookOutputConfig` — 添加字段
- `remove_field(config_id: str, field_id: str) -> WebhookOutputConfig` — 移除字段
- `extract(config_id: str, response: dict) -> OutputExtractionResult` — 从响应提取输出
- `validate_response(config_id: str, response: dict) -> dict` — 校验响应是否成功

### 4.3 错误码

- `MISSING_NAME` — name 为空
- `MISSING_WEBHOOK` — webhook_id 为空
- `DUPLICATE_FIELD_ID` — field_id 重复
- `INVALID_TARGET_TYPE` — 不支持的目标类型
- `INVALID_SOURCE_PATH` — 源路径格式错误
- `NOT_FOUND` — config 不存在
- `FIELD_NOT_FOUND` — field 不存在

### 4.4 存储上限

- 输出配置：200 条 FIFO

---

## 5. 测试计划

### 5.1 StreamExportEngine（~16 个）
- register / get / list / update / delete 基础 CRUD（5）
- 类型/分区策略/批量大小校验（3）
- start / stop 状态机（2）
- publish_event 成功 + key_hash 分区（2）
- publish_batch（1）
- list_events 倒序（1）
- 运行态校验（1）
- 200 条上限（1）

### 5.2 WebhookPipelineEngine（~18 个）
- register / get / list / update / delete 基础 CRUD（5）
- 空 steps 校验 + 方法/认证校验（3）
- add_step / remove_step / reorder_steps（3）
- run 单步成功 + 多步参数引用传递（2）
- run 失败中断（1）
- list_runs / get_run（2）
- disabled 管道不可运行（1）
- 200 条上限（1）

### 5.3 WebhookOutputEngine（~16 个）
- register / get / list / update / delete 基础 CRUD（5）
- 类型/路径/重名校验（3）
- add_field / remove_field（2）
- extract 成功提取多字段（2）
- extract 类型转换 string→integer/float/boolean（2）
- extract 缺失必填字段（1）
- validate_response 成功/失败码（1）
- 200 条上限（1）

### 5.4 单例（3 个）
- 三个引擎单例各一个

**合计：~53 个测试**

---

## 6. 文件清单

| 文件 | 说明 |
|------|------|
| `aos_api/data_connection_webhook.py` | 三引擎 + 数据模型 + 错误类 |
| `aos_api/routers/data_connection_webhook.py` | 三路由 + 端点 + 错误映射 |
| `tests/test_data_connection_webhook.py` | ~53 个单元测试 |
| `aos_api/main.py` | 新增 import + include_router |

---

*W2-AJ · #122 #123 #124 · v4.9*

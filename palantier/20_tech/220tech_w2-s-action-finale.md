# W2-S · Action 收尾组微规格（#67 / #68 / #70）

> **版本**：v1.0 · 2026-07-22
> **所属 Wave**：W2+ 中优先级
> **关联差距**：#67 Action 日志对象类型 / #68 Action 平台集成 / #70 Action 事务回滚

---

## 1. 范围与目标

| 编号 | 差距项 | 当前状态 | 本批目标 |
|------|--------|----------|----------|
| #67 | Action 日志对象类型 | 无 | [LOG] 前缀自动生成 / 操作 RID / 版本号 / 时间戳 / 参数值快照 |
| #68 | Action 平台集成 | 无 | 对象视图按钮 / Object Explorer 入口 / Workshop 按钮组绑定 |
| #70 | Action 事务回滚 | 无 | 补偿事务 / Saga 模式 / 失败回滚链 |

---

## 2. #67 Action 日志对象类型

### 2.1 模型

```python
class ActionLog(BaseModel):
    id: str                          # LOG-{action_id}-{seq}
    action_id: str
    operation_rid: str               # 操作 RID（全局唯一）
    version: int                     # 第几次执行
    timestamp: str                   # ISO8601
    actor: str                       # 执行者
    parameters: dict                 # 参数值快照
    submission_id: str = ""          # 关联提交
    status: str = "submitted"        # submitted / succeeded / failed / reverted
    metadata: dict = {}
```

### 2.2 命名约定

- 日志对象类型的 object_type 名称以 `[LOG]` 前缀 + Action 名称，例如 `[LOG]CreateOrder`
- 日志记录的 title key 为 `operation_rid`
- 主键为 `id`

### 2.3 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/actions/logs` | 列出日志（支持 action_id / status 过滤） |
| POST | `/v1/actions/logs` | 手动创建日志（通常由提交触发） |
| GET | `/v1/actions/logs/{log_id}` | 获取日志详情 |
| GET | `/v1/actions/{action_id}/logs` | 按 action 列出日志 |
| POST | `/v1/actions/logs/{log_id}/status` | 更新日志状态（成功/失败/reverted） |
| GET | `/v1/actions/{action_id}/log-type` | 获取/生成日志对象类型定义 |

---

## 3. #68 Action 平台集成

### 3.1 模型

```python
class ActionBinding(BaseModel):
    id: str
    action_id: str
    integration_type: str            # object_view / object_explorer / workshop
    target_type: str                 # object_type / workshop_module
    target_id: str
    button_label: str
    button_location: str = "primary" # primary / secondary / overflow
    visibility_condition: str = ""   # 条件表达式
    order: int = 0
    enabled: bool = True

class WorkshopButtonGroup(BaseModel):
    id: str
    workshop_module: str
    name: str
    action_bindings: list[str] = []  # ActionBinding IDs
    layout: str = "horizontal"       # horizontal / vertical
    order: int = 0
```

### 3.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | `/v1/actions/bindings` | 列出/创建绑定 |
| GET/PUT/DELETE | `/v1/actions/bindings/{id}` | CRUD |
| POST | `/v1/actions/bindings/{id}/evaluate` | 评估绑定可见性 |
| GET/POST | `/v1/actions/workshop-button-groups` | 列出/创建按钮组 |
| GET/PUT/DELETE | `/v1/actions/workshop-button-groups/{id}` | CRUD |
| GET | `/v1/actions/workshop-button-groups/by-module/{module}` | 按模块列出按钮组 |
| POST | `/v1/actions/workshop-button-groups/{id}/attach` | 绑定 Action 到按钮组 |
| POST | `/v1/actions/workshop-button-groups/{id}/detach` | 从按钮组解绑 Action |

---

## 4. #70 Action 事务回滚（补偿事务）

### 4.1 模型

```python
class CompensationStep(BaseModel):
    step_id: str
    action_id: str                   # 补偿 Action
    order: int                       # 执行顺序
    parameters: dict = {}            # 补偿参数模板

class SagaTransaction(BaseModel):
    id: str
    name: str
    forward_steps: list[dict]        # 正向步骤 [{action_id, parameters, step_id}]
    compensation_steps: list[CompensationStep]
    status: str = "pending"          # pending / running / completed / compensating / compensated / failed
    started_at: str = ""
    completed_at: str = ""
    context: dict = {}               # 步骤间共享上下文

class SagaStepRecord(BaseModel):
    id: str
    saga_id: str
    step_id: str
    direction: str                   # forward / compensation
    status: str                      # pending / running / succeeded / failed / skipped
    started_at: str
    completed_at: str = ""
    result: dict = {}
    error: str = ""
```

### 4.2 状态机

```
pending → running → completed
              ↓ (forward 失败)
         compensating → compensated
              ↓ (compensation 失败)
              failed
```

### 4.3 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | `/v1/actions/sagas` | 列出/创建 Saga |
| GET/PUT/DELETE | `/v1/actions/sagas/{id}` | CRUD |
| POST | `/v1/actions/sagas/{id}/start` | 启动 Saga |
| POST | `/v1/actions/sagas/{id}/compensate` | 触发补偿 |
| GET | `/v1/actions/sagas/{id}/records` | 列出步骤记录 |
| POST | `/v1/actions/sagas/{id}/records/{record_id}/status` | 更新步骤状态 |
| GET | `/v1/actions/sagas/{id}/state` | 获取 Saga 当前状态快照 |

---

## 5. 实现计划

### 5.1 新增文件

| 文件 | 用途 |
|------|------|
| `aos_api/action_finale.py` | 核心引擎（3 引擎：ActionLogEngine / ActionBindingEngine / SagaEngine） |
| `aos_api/routers/action_finale.py` | API 路由 |
| `tests/test_action_finale.py` | 单元测试 |

### 5.2 测试计划（约 33 测试）

- #67 ActionLog：CRUD（5）+ 状态更新（2）+ 日志类型生成（2）+ 多版本追踪（1）= 10
- #68 ActionBinding：CRUD（5）+ 可见性评估（2）+ 按钮组 CRUD（4）+ attach/detach（3）+ 按模块查询（1）= 15
- #70 Saga：CRUD（5）+ start 状态机（3）+ compensate（2）+ 步骤记录查询（2）+ 状态快照（1）= 13

合计 38 测试（10 + 15 + 13），略多于预估的 33。

# W2-R · Action Webhook 与组织/撤销组微规格（#64 / #65 / #66）

> **版本**：v1.0 · 2026-07-22
> **所属 Wave**：W2+ 中优先级
> **关联差距**：#64 Action Webhook 副作用 / #65 Action Sections 分组 / #66 Action 撤销（Revert）

---

## 1. 范围与目标

| 编号 | 差距项 | 当前状态 | 本批目标 |
|------|--------|----------|----------|
| #64 | Action Webhook 副作用 | 无 | 数据输出模式 / 副作用模式 / 输入输出映射 |
| #65 | Action Sections 分组 | 无 | 单列双列布局 / 折叠 / 条件显示 |
| #66 | Action 撤销（Revert） | 无 | 提交后立即撤销 / 条件检查 |

---

## 2. #64 Action Webhook 副作用

### 2.1 模型

```python
class WebhookSideEffect(BaseModel):
    id: str
    action_id: str
    name: str
    url: str
    mode: str = "data_output"        # data_output / side_effect
    method: str = "POST"             # GET/POST/PUT/PATCH
    headers: dict[str, str] = {}
    input_mapping: dict = {}         # Action 参数 → Webhook 请求字段
    output_mapping: dict = {}        # Webhook 响应 → Action 输出字段（仅 data_output 模式）
    auth_type: str = "none"          # none / bearer / basic / hmac
    auth_config: dict = {}
    retry_policy: dict = {}          # {max_attempts, backoff_seconds}
```

### 2.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/actions/webhook-effects` | 列出 Webhook 副作用 |
| POST | `/v1/actions/webhook-effects` | 创建 Webhook 副作用 |
| GET/PUT/DELETE | `/v1/actions/webhook-effects/{id}` | CRUD |
| POST | `/v1/actions/webhook-effects/{id}/build-request` | 根据 Action 参数构建请求 payload |
| POST | `/v1/actions/webhook-effects/{id}/apply-response` | 将响应按 output_mapping 写回 Action 输出 |

---

## 3. #65 Action Sections 分组

### 3.1 模型

```python
class ActionSection(BaseModel):
    id: str
    action_id: str
    name: str
    display_name: str = ""
    layout: str = "single_column"    # single_column / double_column
    collapsed: bool = False
    visible_condition: str = ""      # 条件表达式，空=恒显示
    fields: list[SectionField] = []  # 字段顺序
    order: int = 0

class SectionField(BaseModel):
    param_name: str
    span: int = 1                    # 1=半宽（双列时）, 2=全宽
```

### 3.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/actions/sections` | 列出 Section（按 action_id 分组） |
| POST | `/v1/actions/sections` | 创建 Section |
| GET/PUT/DELETE | `/v1/actions/sections/{id}` | CRUD |
| POST | `/v1/actions/sections/{id}/visibility` | 评估可见性（基于上下文） |
| POST | `/v1/actions/{action_id}/sections/reorder` | 批量重排序 |

---

## 4. #66 Action 撤销（Revert）

### 4.1 模型

```python
class RevertRule(BaseModel):
    id: str
    action_id: str
    name: str
    revert_window_seconds: int = 0   # 0=不限时
    pre_revert_check: dict = {}      # 条件树（同 SubmissionCriteria）
    on_revert_action_id: str = ""    # 撤销时调用的反向 Action
    requires_confirmation: bool = True

class RevertRecord(BaseModel):
    id: str
    original_action_id: str
    original_submission_id: str
    revert_rule_id: str
    status: str = "pending"          # pending / eligible / in_progress / completed / failed / blocked
    reason: str = ""
    created_at: str
    completed_at: str = ""
```

### 4.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/actions/revert-rules` | 列出撤销规则 |
| POST | `/v1/actions/revert-rules` | 创建撤销规则 |
| GET/PUT/DELETE | `/v1/actions/revert-rules/{id}` | CRUD |
| POST | `/v1/actions/revert-rules/{id}/check` | 检查指定提交是否符合撤销条件 |
| POST | `/v1/actions/revert-rules/{id}/execute` | 执行撤销，生成 RevertRecord |
| GET | `/v1/actions/revert-records` | 列出撤销记录 |
| GET | `/v1/actions/revert-records/{record_id}` | 获取撤销记录详情 |

---

## 5. 实现计划

### 5.1 新增文件

| 文件 | 用途 |
|------|------|
| `aos_api/action_webhook.py` | 核心引擎（3 引擎） |
| `aos_api/routers/action_webhook.py` | API 路由 |
| `tests/test_action_webhook.py` | 单元测试 |

### 5.2 测试计划（约 32 测试）

- #64 WebhookSideEffect：CRUD（5）+ build_request（input_mapping + 模板替换）（3）+ apply_response（output_mapping）（2）+ auth_type 校验（2）+ mode 校验（1）
- #65 ActionSection：CRUD（5）+ visibility 评估（3）+ reorder（2）+ layout/double_column span（2）
- #66 RevertRule：CRUD（5）+ check（窗口/条件检查）（4）+ execute 状态机（3）+ RevertRecord 查询（2）

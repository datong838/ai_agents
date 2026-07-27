# W2-Q · Action 增强延伸组微规格（#61 / #62 / #63）

> **版本**：v1.0 · 2026-07-22
> **所属 Wave**：W2+ 中优先级
> **关联差距**：#61 Action 参数筛选 / #62 Action 提交标准可视化 / #63 Action 通知副作用

---

## 1. 范围与目标

| 编号 | 差距项 | 当前状态 | 本批目标 |
|------|--------|----------|----------|
| #61 | Action 参数筛选 | 无 | 对象下拉起始集 / 搜索范围 / 安全性筛选 |
| #62 | Action 提交标准可视化 | JSON | 条件模板 / 逻辑运算符 / 失败消息可视化 |
| #63 | Action 通知副作用 | 无 | 静态 / 参数 / 对象属性 / 函数收件人 + 模板内容 |

---

## 2. #61 Action 参数筛选

### 2.1 模型

```python
class ParameterFilter(BaseModel):
    id: str
    action_id: str
    param_name: str
    target_object_type: str           # 筛选目标对象类型
    base_set: str = ""                # 起始集 ID（Object Set）
    search_scope: dict = {}           # 搜索范围（限定属性/限定值）
    security_filter: str = ""         # 安全性筛选表达式（RV / MDO 等前置条件）
    ordering: list[dict] = []         # 排序规则
```

### 2.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/actions/parameter-filters` | 列出筛选配置 |
| POST | `/v1/actions/parameter-filters` | 创建筛选配置 |
| GET/PUT/DELETE | `/v1/actions/parameter-filters/{id}` | CRUD |
| POST | `/v1/actions/parameter-filters/{id}/apply` | 应用筛选，返回符合条件的对象列表 |

---

## 3. #62 Action 提交标准可视化

### 3.1 模型

```python
class SubmissionCriteria(BaseModel):
    id: str
    action_id: str
    name: str
    condition_tree: dict              # 条件树（嵌套 AND/OR/NOT + 叶子节点）
    failure_message: str = ""
    severity: str = "error"           # error / warning
```

条件树节点格式：
- 复合节点：`{"op": "AND"/"OR"/"NOT", "children": [...]}`
- 叶子节点：`{"field": "...", "op": "=", "value": "..."}`

### 3.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/actions/submission-criteria` | 列出提交标准 |
| POST | `/v1/actions/submission-criteria` | 创建提交标准 |
| GET/PUT/DELETE | `/v1/actions/submission-criteria/{id}` | CRUD |
| POST | `/v1/actions/submission-criteria/{id}/evaluate` | 评估条件树，返回通过/失败 |

---

## 4. #63 Action 通知副作用

### 4.1 模型

```python
class NotificationSideEffect(BaseModel):
    id: str
    action_id: str
    name: str
    recipient_source: str             # static / parameter / object_property / function
    recipients: list[str] = []        # 静态收件人（source=static）
    recipient_ref: str = ""           # 引用键（parameter/object_property）或函数名（function）
    subject_template: str = ""
    body_template: str = ""
    channel: str = "email"            # email / sms / in_app
```

### 4.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/actions/notification-effects` | 列出通知副作用 |
| POST | `/v1/actions/notification-effects` | 创建通知副作用 |
| GET/PUT/DELETE | `/v1/actions/notification-effects/{id}` | CRUD |
| POST | `/v1/actions/notification-effects/{id}/render` | 渲染通知（subject/body/resolved_recipients） |
| POST | `/v1/actions/notification-effects/{id}/dispatch` | 触发派发（记录到发送队列） |

---

## 5. 实现计划

### 5.1 新增文件

| 文件 | 用途 |
|------|------|
| `aos_api/action_further.py` | 核心引擎（3 引擎） |
| `aos_api/routers/action_further.py` | API 路由 |
| `tests/test_action_further.py` | 单元测试 |

### 5.2 测试计划（约 30 测试）

- #61 ParameterFilter：CRUD（5）+ apply 筛选（base_set/search_scope/security/ordering）（5）+ 错误用例（2）
- #62 SubmissionCriteria：CRUD（5）+ evaluate 条件树（AND/OR/NOT/叶子/嵌套）（6）+ severity + failure_message（2）
- #63 NotificationSideEffect：CRUD（5）+ render 模板（变量替换）（4）+ 4 种收件人来源（4）+ dispatch（2）

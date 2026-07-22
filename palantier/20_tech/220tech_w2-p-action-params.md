# W2-P · Action 参数增强组微规格（#58 / #59 / #60）

> **版本**：v1.0 · 2026-07-22
> **所属 Wave**：W2+ 中优先级
> **关联差距**：#58 Action 参数约束 / #59 Action 参数默认值 / #60 Action 参数覆盖

---

## 1. 范围与目标

| 编号 | 差距项 | 当前状态 | 本批目标 |
|------|--------|----------|----------|
| #58 | Action 参数约束 | JSON 配置 | User Input/Multiple Choice/从 Object Set 取选项 |
| #59 | Action 参数默认值 | 无 | 静态值/对象属性/类型类/环境变量 |
| #60 | Action 参数覆盖 | 无 | 条件覆盖块/Visible/Disabled/Required 三态 |

---

## 2. #58 Action 参数约束

### 2.1 约束类型

| 类型 | 说明 |
|------|------|
| `user_input` | 用户手动输入，支持 min/max/pattern 校验 |
| `multiple_choice` | 多选，从固定选项列表中选择 |
| `object_set` | 从 Object Set 取选项 |

### 2.2 模型

```python
class ParameterConstraint(BaseModel):
    id: str
    action_id: str
    param_name: str
    constraint_type: str  # user_input / multiple_choice / object_set
    config: dict          # 类型特定配置
```

---

## 3. #59 Action 参数默认值

### 3.1 默认值来源

| 来源 | 说明 |
|------|------|
| `static` | 静态值 |
| `object_property` | 对象属性引用 |
| `type_class` | 类型类默认值 |
| `environment` | 环境变量 |

### 3.2 模型

```python
class ParameterDefault(BaseModel):
    id: str
    action_id: str
    param_name: str
    source: str           # static / object_property / type_class / environment
    value: Any            # 静态值或引用键
    fallback: Any = None  # 解析失败时的回退值
```

---

## 4. #60 Action 参数覆盖

### 4.1 覆盖三态

| 状态 | 说明 |
|------|------|
| `visible` | 参数是否可见 |
| `disabled` | 参数是否禁用 |
| `required` | 参数是否必填 |

### 4.2 条件覆盖块

```python
class ParameterOverride(BaseModel):
    id: str
    action_id: str
    param_name: str
    condition: str        # 触发条件表达式
    overrides: dict       # {visible: bool, disabled: bool, required: bool}
```

---

## 5. 实现计划

### 5.1 新增文件

| 文件 | 用途 |
|------|------|
| `aos_api/action_params.py` | 核心引擎 |
| `aos_api/routers/action_params.py` | API 路由 |
| `tests/test_action_params.py` | 单元测试 |

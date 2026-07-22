# W2-N · Object 编辑与冲突组微规格（#42 / #44 / #45）

> **版本**：v1.0 · 2026-07-22
> **所属 Wave**：W2+ 中优先级
> **关联差距**：#42 对象编辑冲突解决 / #44 对象模式迁移 / #45 对象编辑历史追踪

---

## 1. 范围与目标

| 编号 | 差距项 | 当前状态 | 本批目标 |
|------|--------|----------|----------|
| #42 | 对象编辑冲突解决 | 无 | 用户优先/时间戳优先两种策略 |
| #44 | 对象模式迁移 | 无 | 5 种迁移指令/每批 500 编辑 |
| #45 | 对象编辑历史追踪 | decision_lineage | 对象属性变更时间线/开关控制 |

---

## 2. #42 对象编辑冲突解决

### 2.1 冲突检测

当两个并发编辑修改同一对象同一字段时检测冲突。

### 2.2 解决策略

| 策略 | 说明 |
|------|------|
| `user_priority` | 指定用户优先级高的编辑胜出 |
| `timestamp_priority` | 时间戳晚的编辑胜出（LastWriteWins） |

### 2.3 模型

```python
class EditConflict(BaseModel):
    id: str
    object_type: str
    object_id: str
    field: str
    edit_a: dict   # {user, value, timestamp}
    edit_b: dict   # {user, value, timestamp}
    resolution: dict | None = None  # 解决结果

class ConflictResolution(BaseModel):
    strategy: str   # user_priority / timestamp_priority
    winner: str     # "a" / "b"
    resolved_value: Any
    reason: str
```

---

## 3. #44 对象模式迁移

### 3.1 迁移指令

| 指令 | 说明 |
|------|------|
| `ADD_PROPERTY` | 新增属性 |
| `REMOVE_PROPERTY` | 删除属性 |
| `RENAME_PROPERTY` | 重命名属性 |
| `CHANGE_TYPE` | 修改属性类型 |
| `SET_NULLABLE` | 设置可空性 |

### 3.2 批量处理

- 每批最多 500 个编辑
- 支持 dry-run 预览
- 迁移状态跟踪（PENDING→RUNNING→COMPLETED/FAILED）

### 3.3 模型

```python
class MigrationCommand(BaseModel):
    id: str
    object_type: str
    instruction: str   # ADD_PROPERTY 等
    field: str
    params: dict
    status: str = "PENDING"
    batch_size: int = 500

class MigrationBatch(BaseModel):
    id: str
    object_type: str
    commands: list[MigrationCommand]
    total: int
    processed: int = 0
    failed: int = 0
    status: str = "PENDING"
    dry_run: bool = False
```

---

## 4. #45 对象编辑历史追踪

### 4.1 功能

- 记录对象属性变更时间线
- 支持开关控制（per-OT 启用/禁用）
- 按 OT/对象/字段/时间范围查询

### 4.2 模型

```python
class ObjectChangeLog(BaseModel):
    id: str
    object_type: str
    object_id: str
    field: str
    old_value: Any
    new_value: Any
    author: str
    timestamp: str
    operation: str  # create / update / delete
```

---

## 5. 实现计划

### 5.1 新增文件

| 文件 | 用途 |
|------|------|
| `aos_api/object_editing.py` | 核心引擎（ConflictEngine + MigrationEngine + ChangeLogEngine） |
| `aos_api/routers/object_editing.py` | API 路由 |
| `tests/test_object_editing.py` | 单元测试 |

### 5.2 修改文件

| 文件 | 修改内容 |
|------|----------|
| `aos_api/main.py` | 注册新路由 |

### 5.3 测试计划

| 测试类 | 用例数 |
|--------|--------|
| 冲突解决 | ~8 |
| 模式迁移 | ~9 |
| 编辑历史追踪 | ~7 |
| 合计 | ~24 |

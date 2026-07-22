# 220tech · W2-H 第八批 Action 增强组（5 项）

> **版本**：v1.0 · 2026-07-22 · **关联**：220plan §1.2.4 W2+ 中优先级 #54/#55/#56/#57/#76
> **前置**：W1-6 Writeback（已有 soft_delete）· W1-2 Logic · W2-C Action Rules
> **目标**：Action 系统增强，支持副作用、乐观 UI、软删除、重试、合并策略

## 1. 范围与目标

| 编号 | 差距项 | 现状 | 本批交付 | 主文件 |
|------|--------|------|----------|--------|
| W2-#54 | Action Side Effects | 无 | Notification/Webhook 副作用注册与触发 | `action_enhancements.py`（新建） |
| W2-#55 | Action 乐观 UI | 无 | 前端先改态 token + 失败回滚标记 | `action_enhancements.py`（新建） |
| W2-#56 | Action 软删除 | writeback.py 有 soft_delete op | Action 层面暴露软删除 API + is_deleted 标记 | `action_enhancements.py` + 复用 writeback |
| W2-#57 | Action 副作用重试 | 无 | retry×3 → DLQ（死信队列）机制 | `action_enhancements.py`（新建） |
| W2-#76 | Edits 合并策略 | 无 | 字段级合并/LastWriteWins/人工仲裁三种策略 | `action_enhancements.py`（新建） |

## 2. 数据模型

### 2.1 Side Effects（#54）

```python
class EffectType(str, Enum):
    NOTIFICATION = "notification"
    WEBHOOK = "webhook"

class ActionEffect(BaseModel):
    id: str
    action_type_id: str
    type: EffectType
    config: dict[str, Any]       # webhook: url/method/headers/body_template; notification: recipients/template
    retry: int = 3               # #57 副作用重试次数
    enabled: bool = True

class EffectResult(BaseModel):
    effect_id: str
    status: Literal["success", "failed", "pending", "dlq"]
    message: str = ""
    attempt: int = 0
```

### 2.2 Optimistic UI（#55）

```python
class OptimisticToken(BaseModel):
    token: str
    action_type_id: str
    payload: dict[str, Any]
    timestamp: str
    rollback_key: str | None = None   # 失败时用于回滚的键

class OptimisticResult(BaseModel):
    ok: bool
    token: str
    rollback_required: bool = False
    rollback_payload: dict[str, Any] | None = None
```

### 2.3 Soft Delete（#56）

复用 writeback.py 的 `soft_delete` op，新增 Action 层 API。

### 2.4 DLQ（#57）

```python
class DLQEntry(BaseModel):
    id: str
    effect_id: str
    action_type_id: str
    payload: dict[str, Any]
    attempts: int
    max_attempts: int
    last_error: str = ""
    enqueued_at: str
    next_retry_at: str | None = None
```

### 2.5 Merge Strategy（#76）

```python
class MergeStrategy(str, Enum):
    FIELD_LEVEL = "field_level"       # 字段级合并（新字段覆盖，旧字段保留）
    LAST_WRITE_WINS = "last_write_wins" # 最后写入者获胜（完整替换）
    MANUAL_ARBITRATION = "manual_arbitration" # 人工仲裁（标记冲突，等待人工处理）

class MergeResult(BaseModel):
    merged: dict[str, Any]
    strategy: MergeStrategy
    conflicts: list[dict[str, Any]] = []  # 人工仲裁时的冲突列表
```

## 3. API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/v1/actions/effects` | 创建副作用（#54） |
| POST | `/v1/actions/{action_type_id}/effects/{effect_id}/trigger` | 触发副作用（#54） |
| POST | `/v1/actions/optimistic` | 乐观 UI 前置提交（#55） |
| POST | `/v1/actions/{action_type_id}/soft-delete` | 软删除（#56） |
| GET | `/v1/actions/dlq` | 查询死信队列（#57） |
| POST | `/v1/actions/dlq/{entry_id}/retry` | 重试 DLQ 条目（#57） |
| POST | `/v1/actions/merge` | 编辑合并策略（#76） |

## 4. 测试计划

| 文件 | 覆盖 | 用例数 |
|------|------|--------|
| `test_action_enhancements.py` | Side Effects(notification/webhook)、乐观UI、软删除、DLQ重试、三种合并策略、API | ~20 |

## 5. 风险与最小更改保证

1. **#56 复用现有**：soft_delete 直接调用 writeback.py 的 soft_delete op，不重复实现
2. **#55 向后兼容**：乐观 UI 为独立路径，不影响现有 action 提交流程
3. **#54/#57 全新模块**：不触碰现有代码
4. **#76 向后兼容**：默认策略为 FIELD_LEVEL（与现有 writeback upsert 行为一致）

## 6. 完成标准（DoD）

- [ ] 新测试文件全绿
- [ ] 全量回归 0 failed
- [ ] 220plan 面板：#54/#55/#56/#57/#76 标记 ✅
- [ ] 服务重启验证新端点 200

# 220tech · W1-6 Action 写回协议（L1 Write-back Dataset）

> **版本**：v1.0 · 2026-07-22
> **关联**：220plan §1.2.2 W1-6 · Phase 3 · 高优先级
> **依赖**：无新增（独立模块）；未来 W1-7 壳核模式会调用本协议
> **范围**：L1 Write-back Dataset 覆盖层 + 软删除 + 乐观 UI 视图合并 + 事务（begin/apply/commit/rollback）

---

## 1. 目标与差距

| 维度 | 当前 | 目标 |
| --- | --- | --- |
| 写回路径 | Action 直接改底层 dataset | L1 覆盖层（WritebackLayer）+ L0 基础数据合并 |
| 删除语义 | 物理删除 | 软删除（`deleted=True` 标记，可恢复） |
| 事务 | 无 | begin → apply(ops) → commit/rollback |
| UI 一致性 | 异步刷新 | 乐观 UI：apply 立即返回最新合并视图 |
| 乐观锁 | 无 | 每条记录 version，冲突检测 |

## 2. 数据模型

```python
class WritebackOp(BaseModel):
    op: Literal["upsert", "soft_delete", "undelete"]
    pk: str                       # 主键值（字符串化）
    row: dict[str, Any] = {}      # op=upsert 时的字段（必须含 pk_field）

class WritebackEntry(BaseModel):
    pk: str
    row: dict[str, Any]
    deleted: bool = False
    version: int = 1              # 每次更新 +1，乐观锁
    created_at: str
    updated_at: str

class WritebackLayer(BaseModel):
    dataset_rid: str
    entries: dict[str, WritebackEntry] = {}
    status: Literal["open", "committed", "rolled_back"] = "open"
    opened_at: str
    committed_at: str | None = None
```

## 3. 三种操作语义

| op | 行为 |
| --- | --- |
| `upsert` | 若 pk 不存在 → 新建 entry；存在 → 合并字段（row 覆盖旧字段），version+1 |
| `soft_delete` | 标记 deleted=True，version+1（保留 row 用于恢复） |
| `undelete` | 标记 deleted=False，version+1 |

### 3.1 冲突检测

apply 时若 entry 已 committed/rolled_back → 拒绝（status must be open）。

## 4. WritebackStore 类

```python
class WritebackStore:
    def begin(self, dataset_rid: str) -> str               # 返回 txn_id
    def apply(self, txn_id: str, ops: list[WritebackOp]) -> WritebackLayer
    def commit(self, txn_id: str) -> WritebackLayer
    def rollback(self, txn_id: str) -> WritebackLayer
    def get_layer(self, dataset_rid: str) -> WritebackLayer | None
    def view(self, dataset_rid: str, base_rows: list[dict], pk_field: str) -> list[dict]
        # 合并 L0 + L1：base 按 pk_field 索引；L1 覆盖；过滤 deleted；返回最新视图
```

### 4.1 view 合并算法

```
1. base_map = {str(r[pk_field]): r for r in base_rows}
2. for pk, entry in layer.entries.items():
   a. if entry.deleted: 从 base_map 删除该 pk（软删除生效）
   b. else: base_map[pk] = {**base_map.get(pk, {}), **entry.row}  # L1 覆盖 L0
3. return list(base_map.values())
```

### 4.2 乐观 UI

`apply` 和 `commit` 直接返回最新 `WritebackLayer`，前端立即拿到 entries 状态。
`view` 端点接收 base_rows，返回合并后的实际可见行，用于 UI 刷新。

## 5. REST API

> 命名空间 `/v1/writeback`（避免与 `actions.py` 的 `/v1/actions/types` 和 `runtime_write.py` 的 `/v1/actions/execute` 冲突）。

| 方法 | 路径 | 功能 |
| --- | --- | --- |
| POST | `/v1/writeback/begin` | 开启事务（body: {dataset_rid}） |
| POST | `/v1/writeback/{txn_id}/apply` | 应用操作（body: {ops: [...]}） |
| POST | `/v1/writeback/{txn_id}/commit` | 提交 |
| POST | `/v1/writeback/{txn_id}/rollback` | 回滚 |
| GET  | `/v1/writeback/datasets/{dataset_rid}` | 查询当前 L1 状态 |
| POST | `/v1/writeback/datasets/{dataset_rid}/view` | 合并视图（body: {base_rows, pk_field}） |

## 6. 测试用例（≥ 16）

### 6.1 引擎（≥ 10）

1. begin 返回 txn_id
2. apply upsert 新建 entry
3. apply upsert 已存在 → 字段合并 + version+1
4. apply soft_delete → deleted=True
5. apply undelete → deleted=False
6. apply 后 commit → status=committed
7. commit 后再 apply → 拒绝（status 错误）
8. rollback → status=rolled_back，entries 保留但不可再用
9. view 合并：L0 + L1 upsert
10. view 软删除：deleted pk 不出现在结果
11. view 仅 L0（无 L1）→ 返回原 base_rows
12. 不存在的 txn_id apply → NOT_FOUND
13. 不存在的 dataset_rid view → 返回 base_rows 原样

### 6.2 API（≥ 6）

14. POST /begin → 200 + txn_id
15. POST /apply → 200 + layer
16. POST /commit → 200
17. POST /view → 合并结果
18. GET /datasets/{rid} → 当前 L1
19. POST /rollback → 200
20. 不存在 txn_id commit → 404
21. 重复 commit → 400

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 内存爆炸 | 单 dataset entries 上限 10000（超出截断 + 警告） |
| 并发修改 | 本期内存单实例；事务级别互斥（apply 时 lock） |
| 事务悬挂 | 文档约定 30s 超时（Phase 6 实现 reaper） |
| L0/L1 pk 类型不一致 | view 内统一 `str(r[pk_field])` 索引 |

## 8. 文件清单

| 路径 | 类型 | 说明 |
| --- | --- | --- |
| `aos_api/writeback.py` | 新增 | WritebackOp/Entry/Layer + WritebackStore |
| `aos_api/routers/writeback.py` | 新增 | 6 个 REST 端点 |
| `aos_api/main.py` | 修改 | 注册 writeback router |
| `tests/test_writeback.py` | 新增 | 21 个测试 |

## 9. 不做的事

- ❌ 持久化（DB 在 Phase 6）
- ❌ 多用户协作冲突（CRDT/OT，Phase 6）
- ❌ 真实 L0 dataset 读取（前端传 base_rows，避免耦合 dataset 模块）
- ❌ 事务 reaper（Phase 6 定时清理）

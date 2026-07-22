# 220tech · W2-G 第七批 Expectation + WriteMode 增强 + Transaction 状态机（3 项）

> **版本**：v1.0 · 2026-07-22 · **关联**：220plan §1.2.4 W2+ 中优先级 #15/#16/#17
> **前置**：W1-5 Funnel · W1-14 Pipeline Builder · W2-#24 Data Transaction（write_mode 已有）
> **目标**：W2+ 中优先级 166 项开始模块化推进，第一批交付 3 项

## 1. 范围与目标

| 编号 | 差距项 | 现状 | 本批交付 | 主文件 |
|------|--------|------|----------|--------|
| W2-#15 | Expectation | 无 | PK 唯一检查 + 行数范围(min/max)检查 + Pipeline/Funnel 执行时可选触发 | `expectation.py`（新建）+ `routers/expectation.py`（新建） |
| W2-#16 | Write Mode | data_transaction.py 有 append/snapshot/update | 补 "default" 语义 + Pipeline Builder 集成 write_mode + describe API | `data_transaction.py`（增量）+ `routers/data_transaction.py`（新建） |
| W2-#17 | Transaction 状态机 | 无显式数据事务 | OPEN→COMMITTED/ABORTED 生命周期 + 与 write_mode 集成 | `data_transaction.py`（增量）+ `routers/data_transaction.py`（增量） |

## 2. 数据模型

### 2.1 Expectation（#15）— 新建

```python
class ExpectationType(str, Enum):
    PK_UNIQUE = "pk_unique"       # 主键唯一
    ROW_COUNT = "row_count"       # 行数范围

class Expectation(BaseModel):
    id: str
    name: str
    type: ExpectationType
    config: dict[str, Any]        # pk_unique: {"primary_key": "id"}; row_count: {"min": 0, "max": 1000}
    severity: Literal["error", "warn"] = "error"
    enabled: bool = True

class ExpectationResult(BaseModel):
    expectation_id: str
    passed: bool
    message: str
    violations: list[dict[str, Any]] = []  # 具体违规行/计数

class ExpectationEngine:
    def check(self, expectation: Expectation, rows: list[dict]) -> ExpectationResult
    def check_all(self, expectations: list[Expectation], rows: list[dict]) -> list[ExpectationResult]
```

**检查逻辑**：
- `pk_unique`：统计 pk 重复值，violations 含重复 pk 列表
- `row_count`：检查 len(rows) 是否在 [min, max] 范围内
- `severity="error"` 且未通过 → 调用方应中止管道；`severity="warn"` → 记录但继续

### 2.2 WriteMode 增强（#16）— 增量

现有 `data_transaction.py` 已有 append/snapshot/update。增强：
- 新增 `WRITE_MODE_DEFAULT = "default"`，`resolve_write_mode(None)` 返回 `"default"` 而非 `"append"`
- `apply_write_mode` 中 `default` 等同 `append`（向后兼容）
- Pipeline Builder 的 `OutputConfig.write_mode` 增加 `"default"` 选项
- 新增 API 端点 `GET /v1/data-transactions/write-modes` 返回 describe_write_modes() + default 说明

### 2.3 Transaction 状态机（#17）— 增量

```python
class TransactionStatus(str, Enum):
    OPEN = "open"
    COMMITTED = "committed"
    ABORTED = "aborted"

class DataTransaction(BaseModel):
    id: str
    dataset_rid: str
    write_mode: str = "default"
    status: TransactionStatus = TransactionStatus.OPEN
    opened_at: str
    committed_at: str | None = None
    aborted_at: str | None = None
    rows: list[dict[str, Any]] = []        # 暂存数据
    expectations: list[str] = []            # 关联的 expectation id

class TransactionStore:
    def begin(self, dataset_rid, write_mode="default", expectations=[]) -> DataTransaction
    def write(self, txn_id, rows) -> DataTransaction              # 写入暂存
    def commit(self, txn_id) -> DataTransaction                   # OPEN→COMMITTED
    def abort(self, txn_id) -> DataTransaction                    # OPEN→ABORTED
    def get(self, txn_id) -> DataTransaction | None
    def list(self, dataset_rid=None) -> list[DataTransaction]
```

**状态转换规则**：
- OPEN → COMMITTED（commit）：提交暂存数据，应用 write_mode 合并
- OPEN → ABORTED（abort）：丢弃暂存数据
- COMMITTED/ABORTED → 不可逆（二次 commit/abort 返回错误）

## 3. API 端点

### 3.1 Expectation（#15）
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/v1/expectations` | 创建 Expectation |
| GET | `/v1/expectations` | 列出所有 |
| POST | `/v1/expectations/{eid}/check` | 执行检查（传入 rows） |

### 3.2 WriteMode（#16）
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/data-transactions/write-modes` | 返回所有写入模式说明 |

### 3.3 Transaction（#17）
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/v1/data-transactions/begin` | 开启事务 |
| POST | `/v1/data-transactions/{txn_id}/write` | 写入暂存数据 |
| POST | `/v1/data-transactions/{txn_id}/commit` | 提交 |
| POST | `/v1/data-transactions/{txn_id}/abort` | 中止 |
| GET | `/v1/data-transactions/{txn_id}` | 查询事务详情 |

## 4. 测试计划

| 文件 | 覆盖 | 用例数 |
|------|------|--------|
| `test_expectation.py` | PK 唯一检查（通过/失败/空 PK）、行数检查（min/max/边界）、severity、check_all、API | ~12 |
| `test_data_transaction_state.py` | begin/write/commit/abort、状态转换、不可逆、write_mode 集成、default 模式、API | ~12 |

## 5. 风险与最小更改保证

1. **#16 向后兼容**：`resolve_write_mode` 仍接受 None，返回值从 "append" 改为 "default"，但 `apply_write_mode` 中 "default" 等同 "append"；现有 test_data_transaction.py 的 `test_resolve_default` 需同步更新
2. **#15 全新模块**：不触碰现有代码
3. **#17 全新 Store**：不冲突 writeback.py 的 WritebackStore
4. **同文件串行编辑**：data_transaction.py 多处修改串行执行

## 6. 完成标准（DoD）

- [ ] 2 个新测试文件全绿
- [ ] 现有 test_data_transaction.py 更新后全绿
- [ ] 全量回归 0 failed
- [ ] 220plan 面板：#15/#16/#17 标记 ✅
- [ ] 服务重启验证新端点 200

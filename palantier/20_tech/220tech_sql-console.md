# 220tech · W1-15 Dataset Preview SQL Console

> **版本**：v1.0 · 2026-07-22 · **关联**：220plan §1.2.2 W1-15 · Phase 5 · 中优先级
> **依赖**：Python 标准库 sqlite3（内存库，实现完整 SQL 方言，无需 Spark）
> **范围**：SQL 查询执行（SELECT 白名单）+ 自动补全 + 查询历史

## 1. 目标
- 对内存中的 dataset（list[dict]）执行 SQL 查询
- **核心技巧**：把 rows 灌入 sqlite3 :memory: 表，用 sqlite 原生执行（支持完整 SQL 子集：SELECT/WHERE/GROUP BY/ORDER BY/LIMIT/JOIN/聚合/子查询）
- 安全：白名单只允许 SELECT，禁止 DDL/DML
- 自动补全：基于 schema 字段名
- 查询历史：记录每次查询

## 2. 为什么用 sqlite3 而非自写解释器
- sqlite3 是 Python 标准库，零依赖
- 支持完整 SQL 方言（Spark SQL 子集完全覆盖）
- 性能好（C 实现）
- 避免自己写 SQL parser 的 bug

## 3. 安全白名单
```
允许：SELECT
禁止：INSERT/UPDATE/DELETE/DROP/ALTER/CREATE/ATTACH/DETACH/PRAGMA/REPLACE/MERGE
```
校验：sql.strip().upper().startswith("SELECT") 且不包含禁止关键词。

## 4. 数据模型
```python
class QueryResult(BaseModel):
    sql: str
    columns: list[str]
    rows: list[dict]
    row_count: int
    duration_ms: float
    error: str | None = None

class QueryHistory(BaseModel):
    id: str
    sql: str
    row_count: int
    duration_ms: float
    executed_at: str
    success: bool
    error: str = ""

class ColumnSuggestion(BaseModel):
    text: str
    kind: Literal["column","table","keyword"]
    description: str = ""
```

## 5. SqlConsole 类
```python
class SqlConsole:
    def validate(self, sql) -> list[str]           # 白名单检查
    def execute(self, rows, table_name, sql) -> QueryResult
        # 1. validate → 若失败返回 error
        # 2. sqlite3 :memory: → CREATE TABLE → INSERT rows
        # 3. execute(sql) → fetchall → dict
    def autocomplete(self, schema_columns, prefix) -> list[ColumnSuggestion]
    def record_history(self, sql, result) -> QueryHistory
    def list_history(self, limit=50) -> list[QueryHistory]
```

### 5.1 execute 算法
```
1. errors = validate(sql); if errors: return QueryResult(error=...)
2. conn = sqlite3.connect(":memory:"); conn.row_factory = sqlite3.Row
3. 从 rows 推断 schema（第一行的 keys + 类型）
4. CREATE TABLE t (col1 TYPE1, col2 TYPE2, ...)
5. INSERT INTO t VALUES (?, ?, ...)  -- 参数化防注入
6. cursor.execute(sql)
7. rows = [dict(r) for r in cursor.fetchall()]
8. columns = [d[0] for d in cursor.description]
9. return QueryResult
```

### 5.2 autocomplete
- schema_columns → ColumnSuggestion(kind="column")
- 内置关键字（SELECT/FROM/WHERE/ORDER BY/GROUP BY/LIMIT/AND/OR）→ kind="keyword"
- 按 prefix 过滤

## 6. REST API (`/v1/sql-console`)
| POST | `/v1/sql-console/execute` | 执行（body: {rows, table_name, sql}） |
| POST | `/v1/sql-console/validate` | 校验（body: {sql}） |
| POST | `/v1/sql-console/autocomplete` | 补全（body: {columns, prefix}） |
| GET | `/v1/sql-console/history` | 查询历史 |

## 7. 测试 ≥ 16
引擎：validate（合法/非法关键词/空）/execute（select */where/order/limit/聚合 count/group by/子查询/类型推断）/autocomplete/history/空 rows 等 ≥10；API ≥6。

## 8. 文件清单
| `aos_api/sql_console.py` | 新增 |
| `aos_api/routers/sql_console.py` | 新增 |
| `aos_api/main.py` | 修改 |
| `tests/test_sql_console.py` | 新增 |

## 9. 不做的事
- ❌ 真实 Spark SQL（Phase 6 接 Spark Connect）
- ❌ 跨表 JOIN（需多 dataset，Phase 6）
- ❌ SQL 语法高亮（前端）
- ❌ 查询计划/EXPLAIN（Phase 6）

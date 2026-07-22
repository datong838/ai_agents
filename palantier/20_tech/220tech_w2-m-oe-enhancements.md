# W2-M · Object Explorer 增强组微规格（#48 / #49 / #50）

> **版本**：v1.0 · 2026-07-22
> **所属 Wave**：W2+ 中优先级
> **关联差距**：#48 OE 高级搜索语法 / #49 OE 保存探索与列表 / #50 OE 批量操作与导出

---

## 1. 范围与目标

| 编号 | 差距项 | 当前状态 | 本批目标 |
|------|--------|----------|----------|
| #48 | OE 高级搜索语法 | 基础搜索 | AND/OR/通配符/模糊搜索/按链接筛选 |
| #49 | OE 保存探索/列表 | 无 | 动态探索 + 静态列表 / 私人与公共保存 |
| #50 | OE 批量操作/导出 | Action 发起 | Excel/CSV 导出 + 在其他应用打开 |

---

## 2. #48 高级搜索语法

### 2.1 查询语法

支持类 SQL 风格的简化查询表达式：

```
name: "Alice" AND age > 30
department = "Engineering" OR title LIKE "%Manager%"
email ~= ".*@example.com"
```

### 2.2 支持的操作符

| 操作符 | 说明 | 示例 |
|--------|------|------|
| `=` / `==` | 精确匹配 | `name = "Alice"` |
| `!=` | 不等于 | `status != "closed"` |
| `>` / `>=` / `<` / `<=` | 数值比较 | `age > 30` |
| `LIKE` | 通配符匹配（% 通配） | `name LIKE "Al%"` |
| `~=` | 正则匹配 | `email ~= ".*@example.com"` |
| `IN` | 集合包含 | `status IN ("open", "pending")` |
| `AND` / `OR` / `NOT` | 逻辑组合 | `A AND (B OR C)` |

### 2.3 按链接筛选

支持通过链接关系筛选对象：

```
LINKS TO Employee WHERE name = "Alice"
LINKS FROM Department WHERE code = "ENG"
```

### 2.4 模型

```python
class SearchQuery(BaseModel):
    object_type: str
    expression: str           # 查询表达式
    limit: int = 100
    offset: int = 0

class SearchResponse(BaseModel):
    object_type: str
    total: int
    objects: list[dict]
    parsed_expression: dict   # 解析后的 AST
```

---

## 3. #49 保存探索与列表

### 3.1 探索类型

| 类型 | 说明 |
|------|------|
| `dynamic` | 动态探索：保存查询条件，每次打开实时执行 |
| `static` | 静态列表：保存对象 ID 快照，不随数据变化 |

### 3.2 可见性

| 可见性 | 说明 |
|--------|------|
| `private` | 仅创建者可见 |
| `public` | 所有用户可见 |

### 3.3 模型

```python
class SavedExploration(BaseModel):
    id: str
    name: str
    object_type: str
    kind: str = "dynamic"       # dynamic / static
    visibility: str = "private" # private / public
    owner: str
    query: dict                 # 动态：保存的查询条件
    object_ids: list[str]       # 静态：对象 ID 快照
    created_at: str
    updated_at: str
```

### 3.4 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/ontology/explorations` | 列出保存的探索 |
| POST | `/v1/ontology/explorations` | 创建保存的探索 |
| GET | `/v1/ontology/explorations/{id}` | 获取探索详情 |
| PUT | `/v1/ontology/explorations/{id}` | 更新探索 |
| DELETE | `/v1/ontology/explorations/{id}` | 删除探索 |
| POST | `/v1/ontology/explorations/{id}/execute` | 执行动态探索 |

---

## 4. #50 批量操作与导出

### 4.1 导出格式

| 格式 | 说明 |
|------|------|
| `csv` | CSV 文件 |
| `excel` | Excel（.xlsx 兼容 CSV 表头） |
| `json` | JSON 数组 |

### 4.2 模型

```python
class ExportRequest(BaseModel):
    object_type: str
    object_ids: list[str]       # 指定对象，空=全量
    format: str = "csv"         # csv / excel / json
    columns: list[str]          # 指定列，空=全部
    filters: dict               # 额外筛选条件

class ExportResult(BaseModel):
    object_type: str
    format: str
    total_rows: int
    columns: list[str]
    rows: list[list]            # 数据行
    download_url: str           # 可选下载链接
```

### 4.3 API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/v1/ontology/object-explorer/export` | 导出对象数据 |
| POST | `/v1/ontology/object-explorer/bulk-update` | 批量更新 |
| POST | `/v1/ontology/object-explorer/bulk-delete` | 批量删除 |

---

## 5. 实现计划

### 5.1 新增文件

| 文件 | 用途 |
|------|------|
| `aos_api/oe_enhancements.py` | 核心引擎（SearchEngine + ExplorationEngine + ExportEngine） |
| `aos_api/routers/oe_enhancements.py` | API 路由 |
| `tests/test_oe_enhancements.py` | 单元测试 |

### 5.2 修改文件

| 文件 | 修改内容 |
|------|----------|
| `aos_api/main.py` | 注册新路由 |

### 5.3 测试计划

| 测试类 | 用例数 |
|--------|--------|
| 高级搜索（解析 + 执行） | ~9 |
| 保存探索（CRUD + 执行） | ~8 |
| 批量导出（3 种格式 + 批量操作） | ~7 |
| 合计 | ~24 |

# 220tech · W2-E 第五批 媒体集 + Lineage + Web IDE（4 项）

> **版本**：v1.0 · 2026-07-22 · **关联**：220plan §1.2.3 W2+ #1/#2/#4/#22
> **注**：#27 Logic 无代码编辑器已在 W2-C 完成，本批不含
> **前置**：W2-A 媒体集基础设施 · W1-13 Lineage DAG · W1-1 Function 引擎

## 1. 范围与目标

| 编号 | 差距项 | 核心交付 | 主文件 |
|------|--------|----------|--------|
| W2-#1 | 媒体集类型化创建 + 延迟策略 | load_strategy(lazy/eager/stream) + 4 类型创建 | `media_set.py`（增量） |
| W2-#2 | 媒体集→表格行变换 | Pipeline 新 NodeKind `media_set` + mediaReference 标准类型 | `pipeline_builder.py`（增量） |
| W2-#4 | Data Lineage（L1）增强 | 列级血缘 + 22 种着色 + 交互式 DAG 布局 | `lineage_graph.py`（增量）+ `lineage_views.py`（新） |
| W2-#22 | Web IDE | 会话管理 + LSP 诊断 + IntelliSense + 静态检查 | `web_ide.py`（新） |

## 2. 数据模型

### 2.1 媒体集延迟策略（#1）

```python
LoadStrategy = Literal["lazy", "eager", "stream"]  # 新增

class MediaSet(BaseModel):
    # ... 现有字段
    load_strategy: LoadStrategy = "eager"  # 新增，向后兼容
```

`MediaSetStore.get_rows` 行为分支：
- `eager`（默认，现状）：即时返回 list
- `lazy`：返回带游标的分页结构
- `stream`：返回 generator（在 transform 边界物化为 list）

### 2.2 媒体集节点（#2）

```python
class PipelineNode(BaseModel):
    kind: Literal["dataset", "transform", "llm", "media_set"] = "dataset"  # 扩展
    # ... 现有字段
    media_set_id: str | None = None  # 新增
```

preview 中 `media_set` 节点：调 `media_set.get_store().get_rows(media_set_id)`。

### 2.3 列级血缘 + 着色（#4）

```python
class ColumnLineage(BaseModel):
    source_columns: list[str]
    target_column: str
    transform_expr: str = ""

class LineageEdge(BaseModel):
    source: str
    target: str
    columns: list[ColumnLineage] = []  # 新增，向后兼容

PALETTE_22: dict[str, str]  # 22 种着色映射（type→color + depth→shade）
```

### 2.4 Web IDE（#22）

```python
class IdeSession(BaseModel):
    id: str
    files: dict[str, str]       # 虚拟文件系统
    open_file: str = ""
    cursor: dict = {}

class IdeDiagnostic(BaseModel):
    file: str
    line: int
    column: int = 0
    severity: Literal["error", "warning", "info"]
    code: str
    message: str

class IdeCompletion(BaseModel):
    label: str
    kind: str
    detail: str = ""
    insert_text: str = ""

class WebIdeEngine:
    def create_session/get/open_file/write_file/list_sessions/delete
    def diagnostics(session_id) -> list[IdeDiagnostic]   # 复用 _check_code
    def completions(session_id, prefix) -> list[IdeCompletion]
    def symbols(session_id) -> list[dict]                 # 复用 FunctionRegistry
    def hover(session_id, position) -> dict
```

## 3. 算法与接缝点

### 3.1 媒体集延迟加载（#1）

```
get_rows(set_id, strategy=None):
    ms = get(set_id)
    strategy = strategy or ms.load_strategy
    refs = [media_reference.get(r_id) for r_id in ms.media_ref_ids]
    if strategy == "stream":
        return _stream_rows(refs)   # generator
    if strategy == "lazy":
        return {"rows": [...], "cursor": ..., "has_more": False}
    return [...ref.to_row()...]     # eager 现状
```

### 3.2 Lineage 交互式布局（#4，只读视图）

```
compute_layout(graph):
    layers = topological_layers(graph)  # 按入度分层
    for layer_idx, nodes in enumerate(layers):
        for col_idx, node in enumerate(nodes):
            layout[node.id] = {x: col_idx*180, y: layer_idx*120, layer: layer_idx}
    return layout
```

### 3.3 Web IDE 诊断（#22，复用现有）

```
diagnostics(session_id):
    code = session.files[session.open_file]
    errors = PythonBuilder.validate_code(code)  # 复用 _check_code
    return [IdeDiagnostic.from_error(e) for e in errors]
```

## 4. 测试矩阵

| 模块 | 测试文件 | 用例数 |
|------|----------|--------|
| 媒体集延迟策略 | `test_media_set_strategy.py` | 10 |
| 媒体集节点 | `test_media_set_node.py` | 8 |
| Lineage 增强 | `test_lineage_enhanced.py` | 12 |
| Web IDE | `test_web_ide.py` | 12 |

合计 42 用例。

## 5. 文件清单

**新增**：
- `aos_api/lineage_views.py` + `aos_api/routers/lineage_views.py`
- `aos_api/web_ide.py` + `aos_api/routers/web_ide.py`
- `tests/test_media_set_strategy.py`
- `tests/test_media_set_node.py`
- `tests/test_lineage_enhanced.py`
- `tests/test_web_ide.py`

**修改（最小增量，串行）**：
- `aos_api/media_set.py`：加 `load_strategy` 字段 + get_rows 分支
- `aos_api/pipeline_builder.py`：kind 加 `"media_set"` + media_set_id 字段 + validate/preview 分支
- `aos_api/lineage_graph.py`：LineageEdge 加 `columns` 字段
- `aos_api/main.py`：注册 lineage_views + web_ide router（串行 + 验证 routes 数量）

## 6. 风险与对策

| 风险 | 对策 |
|------|------|
| get_rows 返回类型不一致 | stream/lazy 在 transform 边界物化为 list |
| NodeKind 扩展遗漏分支 | validate + preview + _apply_node_op 三处同步 |
| 列级血缘向后兼容 | columns 默认空 list，旧边不受影响 |
| Web IDE 无真实 LSP | 复用 _check_code 做诊断，IntelliSense 用 AST 简易补全 |
| main.py 编辑覆盖 | 每次编辑后验证 app.routes 数量 |

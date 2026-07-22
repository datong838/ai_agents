# 220tech · W1-14 Pipeline Builder 交互式 DAG 编辑器

> **版本**：v1.0 · 2026-07-22
> **关联**：220plan §1.2.2 W1-14 · Phase 2 · 高优先级
> **依赖**：W1-8 transform_ops（`apply_transform` / `apply_pipeline`）、W1-13 lineage_graph（`LineageGraph.topological_sort` / `has_cycle`）
> **范围**：后端 DAG 模型 + 编辑器（撤销/重做）+ 校验 + 预览执行 + REST API；前端拖拽 UI 在后续 Phase 集成

---

## 1. 目标与差距

| 维度 | 当前 | 目标 |
| --- | --- | --- |
| 数据模型 | 无 Pipeline DAG 模型 | PipelineNode/Edge/Pipeline 完整模型 |
| 编辑能力 | 静态 3 节点写死 | 命令式增删改 + undo/redo 栈 |
| 校验 | 无 | 环检测（复用 W1-13）+ 必填字段 + 节点存在性 |
| 预览 | 无 | 沿拓扑序执行 transform_ops，输出每节点 rows |
| 持久化 | 无 | 内存存储 + 版本号（前端 localStorage 持久化在后续 Phase） |

## 2. 核心数据结构

### 2.1 节点（PipelineNode）

```python
class PipelineNode(BaseModel):
    id: str                       # 唯一 id（用户给或自动生成）
    kind: Literal["dataset", "transform"]  # 复用 W1-13 节点类型前两种
    label: str                    # 显示名
    op: str | None = None         # kind=transform 时必填，必须是 TRANSFORM_REGISTRY key
    config: dict = {}             # 算子配置（透传给 apply_transform）
    dataset_rid: str | None = None  # kind=dataset 时的输入数据源 rid
```

### 2.2 边（PipelineEdge）

```python
class PipelineEdge(BaseModel):
    src: str   # 上游节点 id
    dst: str   # 下游节点 id
```

### 2.3 快照（Pipeline）

```python
class Pipeline(BaseModel):
    id: str
    name: str
    nodes: list[PipelineNode] = []
    edges: list[PipelineEdge] = []
    version: int = 1              # 每次 apply 成功 +1
    created_at: str
    updated_at: str
```

### 2.4 编辑命令（EditCommand）

JSON 命令格式（前端 → 后端）：

```jsonc
// 增删改节点
{ "action": "add_node",    "node": { "id": "n1", "kind": "dataset", "label": "users" } }
{ "action": "remove_node", "node_id": "n1" }
{ "action": "update_node", "node_id": "n1", "patch": { "label": "users-v2" } }
// 增删边
{ "action": "add_edge",    "edge": { "src": "n1", "dst": "n2" } }
{ "action": "remove_edge", "edge": { "src": "n1", "dst": "n2" } }
// 批量
{ "action": "batch", "commands": [ ... ] }
```

## 3. PipelineEditor 类

```python
class PipelineEditor:
    def __init__(self, pipeline: Pipeline): ...
    def apply(self, command: dict) -> Pipeline: ...  # 执行命令，入 undo 栈，清空 redo 栈
    def undo(self) -> Pipeline: ...                  # 弹 undo 栈，压 redo 栈
    def redo(self) -> Pipeline: ...                  # 弹 redo 栈，压 undo 栈
    def validate(self) -> list[str]: ...             # 校验：环、必填、悬空边
    def preview(self, inputs: dict[str, list[dict]]) -> dict[str, list[dict]]: ...
        # inputs: dataset 节点 id → rows；输出：每个 transform 节点 id → 处理后 rows
```

### 3.1 撤销/重做设计

- 每次 `apply` 前，把当前 Pipeline 深拷贝压入 `_undo_stack`
- `undo`：把当前状态压入 `_redo_stack`，从 `_undo_stack` 弹一个恢复
- `redo`：把当前状态压入 `_undo_stack`，从 `_redo_stack` 弹一个恢复
- 新 `apply` 清空 `_redo_stack`（标准编辑器语义）
- 上限 50 步（防止内存爆炸）

### 3.2 校验规则（validate 返回错误列表）

| 规则 | 触发条件 |
| --- | --- |
| EDGE_SRC_MISSING | 边的 src 节点不存在 |
| EDGE_DST_MISSING | 边的 dst 节点不存在 |
| EDGE_SELF_LOOP | src == dst |
| NODE_DUP_ID | add_node 时 id 已存在 |
| NODE_NOT_FOUND | update/remove 时节点不存在 |
| TRANSFORM_NO_OP | kind=transform 但 op 为空 |
| TRANSFORM_BAD_OP | op 不在 TRANSFORM_REGISTRY |
| DATASET_NO_RID | kind=dataset 但 dataset_rid 为空 |
| CYCLE_DETECTED | DAG 有环（用 LineageGraph.has_cycle） |

### 3.3 preview 执行算法

```
1. 复用 LineageGraph 构建 DAG → topological_sort 得到执行顺序
2. 对每个 dataset 节点：rows = inputs[node.id]（缺失则空列表）
3. 对每个 transform 节点（按拓扑序）：
   a. 收集所有上游节点的 rows，按 edge 顺序合并（多上游 = 多输入）
   b. merged_rows = functools.reduce(operator.add, upstream_rows_list)
   c. node_rows = apply_transform(node.op, merged_rows, node.config)
   d. 输出[node.id] = node_rows
4. 返回 outputs dict
```

> 单上游时 merged_rows 就是上游 rows；多上游时 list 相加（语义等价于 union 但保留顺序）。

## 4. REST API

> 路径前缀 `/v1/pipeline-builder`（避免与 `wave_ext.py` 已有的 `/v1/pipelines` 路由冲突，遵循"最小更改，不影响已有功能"原则）。

| 方法 | 路径 | 功能 |
| --- | --- | --- |
| POST | `/v1/pipeline-builder` | 创建空 pipeline（body: {name}） |
| GET  | `/v1/pipeline-builder` | 列出所有 |
| GET  | `/v1/pipeline-builder/{pid}` | 获取详情 |
| POST | `/v1/pipeline-builder/{pid}/apply` | 执行编辑命令（body: EditCommand） |
| POST | `/v1/pipeline-builder/{pid}/undo` | 撤销 |
| POST | `/v1/pipeline-builder/{pid}/redo` | 重做 |
| POST | `/v1/pipeline-builder/{pid}/validate` | 返回错误列表 |
| POST | `/v1/pipeline-builder/{pid}/preview` | 预览执行（body: {inputs: {node_id: rows}}） |
| DELETE | `/v1/pipeline-builder/{pid}` | 删除 |

## 5. 测试用例（≥ 16）

### 5.1 引擎（≥ 10）

1. 创建空 pipeline + apply add_node → 节点存在
2. add_node 重复 id → NODE_DUP_ID
3. update_node 不存在 → NODE_NOT_FOUND
4. remove_node 同时移除关联边
5. add_edge 成功
6. add_edge src 不存在 → EDGE_SRC_MISSING
7. add_edge self-loop → EDGE_SELF_LOOP
8. add_edge 形成环 → CYCLE_DETECTED
9. undo 恢复上一步
10. redo 重做
11. 新 apply 后 redo 栈清空
12. validate 全通过
13. preview 单链：dataset → transform filter → 输出过滤后 rows
14. preview 多上游 merge：两个 dataset → 一个 transform union → 合并
15. preview 空输入 → 空输出
16. undo 栈上限 50

### 5.2 API（≥ 6）

17. POST /v1/pipelines 创建
18. GET /v1/pipelines 列表
19. POST /apply 后节点存在
20. POST /undo 后回退
21. POST /preview 返回执行结果
22. POST /validate 返回错误
23. DELETE 删除
24. 404 不存在的 pid

## 6. 风险与边界

| 风险 | 缓解 |
| --- | --- |
| 大 DAG 拖慢 preview | 拓扑序 + 单次遍历，O(V+E) |
| undo 栈内存 | 上限 50 |
| 多用户并发 | 本期内存存储单实例，多租户隔离在 Phase 6 |
| transform 算子异常 | preview 中 try/except，异常转成节点错误行 |
| 环检测性能 | 复用 W1-13 Kahn 算法 O(V+E) |

## 7. 文件清单

| 路径 | 类型 | 说明 |
| --- | --- | --- |
| `aos_api/pipeline_builder.py` | 新增 | 模型 + PipelineEditor + 内存存储 |
| `aos_api/routers/pipelines.py` | 新增 | 9 个 REST 端点 |
| `aos_api/main.py` | 修改 | 注册 pipelines router |
| `tests/test_pipeline_builder.py` | 新增 | 24 个测试 |

## 8. 不做的事（明确边界）

- ❌ 前端拖拽 UI（Phase 3 集成）
- ❌ 持久化到 DB（Phase 6，本期内存）
- ❌ 多用户协作冲突解决（Phase 6）
- ❌ Python/SQL/Java 多语言 transform（W1-19 + W2+）
- ❌ Schedule / Build 集成（W1-11 + Phase 6）

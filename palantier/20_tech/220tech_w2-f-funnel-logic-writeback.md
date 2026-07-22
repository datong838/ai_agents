# 220tech · W2-F 第六批 Funnel 双管道/CDC + Logic LangGraph/Wiki + 写回 Workshop 绑定（3 项）

> **版本**：v1.0 · 2026-07-22 · **关联**：220plan §1.2.3 W2+ #11/#17/#19（3 项 🔶 增强版）
> **性质**：核心引擎已在 W1（W1-5/W1-2/W1-6）完成，本批为"增强版"能力补齐
> **前置**：W1-5 Funnel 四阶段 · W1-2 Logic 编排 · W1-6 Action 写回协议
> **目标**：W2 高优先级 27 项彻底清零（22/27 → 27/27）

## 1. 范围与目标

| 编号 | 差距项 | 核心交付 | 主文件 |
|------|--------|----------|--------|
| W2-#11 | Funnel 索引管道执行引擎 | 双管道(snapshot/incremental) + CDC 行级 `_op` 识别 + 全量重索引触发 | `funnel_engine.py`（增量）+ `routers/funnel.py`（增量） |
| W2-#17 | Logic Block 全量 | Block `wiki_ref` 字段注入上下文 + LogicGraph 条件路由图编排(LangGraph 风格) | `logic_engine.py`（增量）+ `routers/logic.py`（增量） |
| W2-#19 | Ontology 写回四步 | WritebackLayer `workshop_module` 绑定 + bind/unbind + Workshop 预览合并视图 | `writeback.py`（增量）+ `routers/writeback.py`（增量） |

## 2. 数据模型（全部向后兼容，新增字段带默认值）

### 2.1 Funnel 双管道 / CDC（#11）

```python
PipelineMode = Literal["snapshot", "incremental"]  # 新增

class StageResult(BaseModel):
    # ... 现有字段
    op_counts: dict[str, int] = Field(default_factory=dict)  # 新增：{"UPSERT":n,"DELETE":n,"UPDATE":n}

class FunnelPipeline(BaseModel):
    # ... 现有字段
    mode: PipelineMode = "snapshot"          # 新增，默认等价现状全量
    watermark: str | None = None             # 新增：增量水位（上次变更位点）
```

**CDC 行级 `_op` 识别**（`_run_changelog`）：
- 行已有 `_op` / `_change_type` / `_changeType` 字段 → 尊重原值（归一为大写 UPSERT/UPDATE/DELETE）
- 行无该字段 → 默认 `"UPSERT"`（**现状行为不变**）
- 统计写入 `stage.op_counts`

**双管道行为**：
- `mode="snapshot"`（默认）：全量重算，merge 按 pk 去重（现状）
- `mode="incremental"`：CDC 增量，changelog 尊重 DELETE（merge 阶段剔除被删除 pk），完成后推进 watermark

**全量重索引触发**：
```python
def reindex(self, source_dataset, target_object_type, primary_key, input_rows) -> FunnelPipeline:
    """触发 snapshot 全量重索引：mode=snapshot + 重置增量水位。"""
```

### 2.2 Logic Wiki 字段 + LangGraph 图编排（#17）

```python
class Block(BaseModel):
    # ... 现有字段
    wiki_ref: str | None = None  # 新增：关联 Wiki 文档 token，执行时注入上下文

class GraphEdge(BaseModel):       # 新增
    source: str                   # 源节点 block_id
    target: str                   # 目标节点 block_id
    condition: str = ""           # 条件表达式（空=无条件/默认边）

class LogicGraph(BaseModel):      # 新增
    nodes: list[Block]
    edges: list[GraphEdge]
    entry: str                    # 入口节点 block_id
```

**Wiki 注入**：Block 执行前，若 `wiki_ref` 非空，从 `wiki_store`（KV）读取文档摘要注入到 `ctx.variables["_wiki_{block_id}"]`；无文档时静默跳过（不报错）。

**LogicGraph 执行**（`LogicEngine.run_graph`）：
- 从 `entry` 出发，拓扑执行节点
- 节点完成后求值其出边的 `condition`（复用 Function 引擎，变量来自 ctx）
- 首个 `condition` 为真（或无条件默认边）的出边决定下一节点
- 支持条件分支（多出边）与跳过（无匹配边即终止该分支）
- 环路保护：单节点最多执行 1 次（防止无限循环）

### 2.3 写回 Workshop 绑定（#19）

```python
class WritebackLayer(BaseModel):
    # ... 现有字段
    workshop_module: str | None = None   # 新增：绑定的 Workshop 模块 id
    workshop_bound_at: str | None = None # 新增：绑定时间
```

**绑定方法**（`WritebackStore`）：
```python
def bind_workshop(self, dataset_rid, module_id) -> WritebackLayer   # 绑定
def unbind_workshop(self, dataset_rid) -> WritebackLayer            # 解绑
def list_by_workshop(self, module_id) -> list[WritebackLayer]       # 按模块反查
```

**Workshop 预览**：layer 绑定 module 后，`view()` 合并结果带 `workshop_module` 标记，便于 Workshop 模块直接渲染"待提交"覆盖层。

## 3. API 端点（全部新增，不修改现有端点签名）

### 3.1 Funnel（#11）
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/v1/funnel/run` | 现有，请求体新增可选 `mode` 字段（默认 snapshot） |
| POST | `/v1/funnel/reindex` | **新增** 全量重索引触发 |

### 3.2 Logic（#17）
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/v1/logic/run-graph` | **新增** LogicGraph 图编排执行 |
| POST | `/v1/logic/debug-graph` | **新增** 图编排调试（收集 proposed_edits + cot） |

### 3.3 Writeback（#19）
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/v1/writeback/datasets/{dataset_rid}/bind-workshop` | **新增** 绑定 Workshop 模块 |
| POST | `/v1/writeback/datasets/{dataset_rid}/unbind-workshop` | **新增** 解绑 |
| GET  | `/v1/writeback/workshop/{module_id}/preview` | **新增** 按模块预览合并视图 |

## 4. 测试计划（3 个新测试文件，目标 ~30 测试）

| 文件 | 覆盖 | 用例数 |
|------|------|--------|
| `test_funnel_engine_cdc.py` | CDC `_op` 识别、op_counts、incremental DELETE 剔除、reindex 水位重置、API reindex | ~10 |
| `test_logic_graph.py` | wiki_ref 注入、LogicGraph 条件分支、环路保护、默认边、run-graph API | ~10 |
| `test_writeback_workshop.py` | bind/unbind、list_by_workshop、preview 合并、向后兼容(无绑定行为不变) | ~10 |

## 5. 风险与最小更改保证

1. **向后兼容**：所有新增字段带默认值；现有 `run()`/`begin()`/`apply()` 签名不变；现有 1140 测试零回归
2. **CDC 安全**：`_op` 识别"已有则尊重、否则默认 UPSERT"，现有 changelog 行为不变
3. **图编排隔离**：`LogicGraph`/`run_graph` 为新增独立路径，不触碰现有线性 `run()`
4. **Workshop 绑定可选**：`workshop_module=None` 时 layer 行为与现状完全一致
5. **同文件串行编辑**：每个核心文件的多处修改串行执行，避免并发覆盖（W2-B 教训）
6. **Wiki 读取容错**：wiki_ref 指向的文档不存在时静默跳过，不中断执行

## 6. 完成标准（DoD）

- [ ] 3 个新测试文件全绿
- [ ] 全量回归 `1140 + 新增 ≈ 1170 passed, 0 failed`
- [ ] 220plan 面板：#11/#17/#19 标记 ✅，W2 27/27
- [ ] 服务重启验证新端点 200

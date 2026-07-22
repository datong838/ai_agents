# 220tech · W2-B 第二批 AIP/Functions 运行时（5 项）

> **版本**：v1.0 · 2026-07-22 · **关联**：220plan §1.2.3 W2+ #7/#18/#21/#25/#26
> **前置**：W1-1 Function 引擎 · W1-2 Logic 编排 · W1-8 Transform 算子库 · W1-14 Pipeline Builder · W2-A 全量交付
> **依赖**：llm_gateway（Agnes 已接入，不写死模型）· transform_ops · functions_python_builder

## 1. 范围与目标

本批交付 5 项 AIP/Functions 运行时能力，统一遵循「注册表 + 装饰器 + 弱 config」范式，复用 W1 已建基础设施，最小侵入现有模块。

| 编号 | 差距项 | 核心交付 | 主文件 |
|------|--------|----------|--------|
| W2-#7 | AIP/LLM 节点 | 7 种 AIP 模板 + Pipeline `llm` 节点类型 | `aip_nodes.py` |
| W2-#18 | 工具集注册增强 | Tool/Capability 注册表 + Logic `use_tool` Block | `tool_registry.py` |
| W2-#21 | @transform 装饰器 | `register_transform` 装饰器 + `OP_CATALOG` 元信息 | `transform_ops.py`（增量） |
| W2-#25 | 多语言 Transform | Python/SQL/Java/R 运行时分发 | `multi_language_transform.py` |
| W2-#26 | Functions 运行时 | 统一注册表 + Ontology API + Workshop 绑定 | `functions_runtime.py` |

## 2. 数据模型

### 2.1 AIP 节点（#7）

```python
AipTemplateKind = Literal[
    "generate", "explain", "name", "assistant",
    "extract", "sentiment", "summarize",
]  # 7 种模板

class AipTemplate(BaseModel):
    kind: AipTemplateKind
    name: str
    description: str
    default_prompt: str        # 含 {{input}} 占位

AIP_TEMPLATE_REGISTRY: dict[str, AipTemplate]  # 7 个预置模板

def render_template(kind, row, user_prompt=None) -> str
def execute_llm_node(rows, config, chat_fn) -> list[dict]  # 逐行渲染→chat→写 output_column
```

Pipeline 接缝：`PipelineNode.kind` 扩展为 `Literal["dataset","transform","llm"]`，`config = {template, prompt, input_column, output_column, model}`。

### 2.2 工具集注册（#18）

```python
class ToolDef(BaseModel):
    id: str
    name: str
    description: str = ""
    parameters_schema: dict[str, Any] = {}   # JSON-Schema 风格

class ToolRegistry:
    def register(self, tool: ToolDef, handler: Callable) -> None
    def get(self, tool_id) -> ToolDef | None
    def list_all(self) -> list[ToolDef]
    def invoke(self, tool_id, args: dict) -> Any

class Capability(BaseModel):
    id: str
    name: str
    tool_ids: list[str]      # 工具分组

class CapabilityStore:
    def define/get/list/add_tool/remove_tool
```

Logic 接缝：`BlockKind` 增加 `"use_tool"`，`_blk_use_tool` handler：`config={tool_id, args, output_var}` → `ToolRegistry.invoke` → 写 `ctx.variables[output_var]`。

### 2.3 @transform 装饰器（#21）

```python
class TransformOpMeta(BaseModel):
    name: str
    description: str = ""
    config_schema: dict[str, Any] = {}

_OP_META: dict[str, TransformOpMeta] = {}   # 元信息侧
TRANSFORM_REGISTRY: dict[str, TransformOp]   # 已有，保持向后兼容

def register_transform(name: str, description="", config_schema=None):
    """装饰器：注册算子到 TRANSFORM_REGISTRY + _OP_META"""
    def deco(fn: TransformOp) -> TransformOp:
        TRANSFORM_REGISTRY[name] = fn
        _OP_META[name] = TransformOpMeta(name=name, description=description, config_schema=config_schema or {})
        return fn
    return deco

def list_op_catalog() -> list[TransformOpMeta]   # 替代裸 keys()
```

**向后兼容**：现有 9 个内建算子保持 `TRANSFORM_REGISTRY = {...}` 字面量注册，启动时同步补 `_OP_META`，不强制改写为装饰器形式（最小改动）。

### 2.4 多语言 Transform（#25）

```python
LanguageKind = Literal["python", "sql", "java", "r"]

class LanguageRuntime(BaseModel):
    language: LanguageKind
    available: bool          # Java/R 标记为 stub

class MultiLanguageTransform:
    def register(language, source, name) -> str   # 返回 transform_id
    def list_all(self) -> list[RuntimeTransform]
    def invoke(self, transform_id, rows) -> list[dict]
    # python: 复用 functions_python_builder
    # sql: 内置轻量 SELECT/WHERE 解释器（list[dict] → list[dict]）
    # java/r: stub，invoke 抛 NOT_IMPLEMENTED
```

### 2.5 Functions 运行时（#26）

```python
class RuntimeFunction(BaseModel):
    id: str
    name: str
    language: LanguageKind          # 复用 #25
    source: str                      # 代码文本
    ontology_refs: list[str] = []    # 引用的对象类型
    workshop_binding: str | None     # 绑定的 Workshop 模块

class FunctionsRuntime:
    def register/get/list/delete
    def invoke(self, fn_id, payload) -> Any
    def bind_workshop(self, fn_id, workshop_module) -> None
    # python: 经 functions_python_builder 执行
    # 其他语言: 复用 MultiLanguageTransform

class OntologyApi:
    """函数运行时可调用的只读 Ontology 接口"""
    def list_objects(self, otd_id, limit) -> list[dict]
    def get_object(self, otd_id, object_id) -> dict | None
    # 复用 W2-3 ontology_output.OntologyOutputStore.preview_objects
```

## 3. 算法与接缝点

### 3.1 AIP LLM 节点执行流（逐行）

```
for row in rows:
    prompt = render_template(template, row, user_prompt)
    resp = chat_fn(prompt, model=config.get("model"))   # 经 llm_gateway 路由，不写死模型
    row[output_column] = resp.get("answer", "")
return rows
```

Pipeline 集成 3 处同步（研究报告已识别）：
1. `PipelineNode.kind` Literal 加 `"llm"`
2. `_validate_node` 加 `elif node.kind == "llm":` 校验 config.template
3. `_apply_node_op` 加 `if node.kind == "llm":` 调 `execute_llm_node`
4. `preview` 拓扑循环加 `elif node.kind == "llm":` 分支

### 3.2 use_tool Block 执行流

```
config = {tool_id, args: dict, output_var}
result = ToolRegistry.invoke(tool_id, args)
ctx.variables[output_var or f"tool_{block.id}"] = result
cot: [f"调用工具 {tool_id} 参数 {args} → {result}"]
```

同步点：BlockKind Literal + `_exec_block` handler dict + `BLOCK_CATALOG`（**三处必须同步**，研究报告已警示）。

### 3.3 SQL 轻量解释器（#25）

仅支持 `SELECT cols FROM <rows> WHERE expr`，作用于 `list[dict]`：
- 列名 → dict key
- WHERE 表达式复用 `function_engine.evaluate(parse(expr), row)`（与 filter op 同源）
- 不支持 JOIN/子查询/聚合（聚合走 aggregate op）

## 4. 测试矩阵

| 模块 | 测试文件 | 用例数 | 关键用例 |
|------|----------|--------|----------|
| AIP 节点 | `test_aip_nodes.py` | 12 | 7 模板渲染、LLM 节点执行(mock chat)、缺模板报错、逐行输出列 |
| 工具集 | `test_tool_registry.py` | 12 | register/invoke/list、Capability 分组、use_tool Block、未知工具报错 |
| @transform | `test_transform_deco.py` | 10 | 装饰器注册、catalog 元信息、自定义算子执行、向后兼容内建 9 算子 |
| 多语言 | `test_multi_language_transform.py` | 10 | Python 执行、SQL SELECT/WHERE、Java/R stub 注册+NOT_IMPLEMENTED、list |
| Functions 运行时 | `test_functions_runtime.py` | 12 | register/invoke Python、TS 类型生成、Ontology API 读、Workshop 绑定、删除 |

合计 56 用例。每项完成后独立 pytest，全部完成后全量回归。

## 5. 文件清单

**新增**：
- `aos_api/aip_nodes.py`
- `aos_api/tool_registry.py`
- `aos_api/multi_language_transform.py`
- `aos_api/functions_runtime.py`
- `aos_api/routers/aip_nodes.py`
- `aos_api/routers/tool_registry.py`
- `aos_api/routers/multi_language.py`
- `aos_api/routers/functions_runtime.py`
- `tests/test_aip_nodes.py`
- `tests/test_tool_registry.py`
- `tests/test_transform_deco.py`
- `tests/test_multi_language_transform.py`
- `tests/test_functions_runtime.py`

**修改（最小增量）**：
- `aos_api/transform_ops.py`：加 `register_transform` 装饰器 + `_OP_META` + `list_op_catalog`（不改动现有 9 算子注册方式）
- `aos_api/pipeline_builder.py`：NodeKind 加 `"llm"` + 3 处分支
- `aos_api/logic_engine.py`：BlockKind 加 `"use_tool"` + handler + BLOCK_CATALOG 同步
- `aos_api/routers/transforms.py`：`list_transforms` 改用 `list_op_catalog` 返回元信息
- `aos_api/main.py`：注册 4 个新 router

## 6. 风险与对策

| 风险 | 对策 |
|------|------|
| NodeKind/BlockKind Literal 扩展遗漏分支 | 每处加 `# W2-B sync` 注释 + 测试覆盖每种 kind |
| BLOCK_CATALOG 与 handler 双源不同步 | use_tool 同步两处；测试断言 catalog 包含 use_tool |
| SQL 解释器越界 | 仅支持白名单语法，复用 function_engine 表达式，禁裸 eval |
| Java/R 无真实运行时 | 明确 stub + NOT_IMPLEMENTED 错误码，不假装支持 |
| 不写死模型 | 所有 chat 经 chat_fn 注入或 llm_gateway，model 参数可选 |

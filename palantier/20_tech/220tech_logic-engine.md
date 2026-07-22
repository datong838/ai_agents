# 220tech · W1-2 Logic 编排引擎

> **版本**：v1.0 · 2026-07-22 · **关联**：220plan §6.1 W1-2 · Phase 4 · 高优先级
> **依赖**：W1-1（Function 引擎）、W1-7（壳核模式）、llm_gateway.py（已就绪）
> **范围**：7 种 Block + 块链执行器 + 调试器（CoT/Edits）+ Edits 合并策略 + Prompt 工程

## 1. 目标
- 实现 7 种 Logic Block：Input / CreateVariable / GetProperty / UseLLM / Transform / ApplyAction / Execute
- Block 链按顺序执行，上下文在 Block 间传递（变量作用域）
- UseLLM Block 调用 `llm_gateway.chat()`（不写死模型，由 gateway 路由）
- ApplyAction Block 调用 W1-7 ShellCore 执行写回
- 调试器：收集 CoT 思维链 + 提议 edits（不落库）
- Edits 合并：LastWriteWins / FieldLevel / ManualReview
- Prompt 工程：`{{var}}` 变量注入 + Few-shot 示例

## 2. 设计原则
- **不写死模型**：UseLLM Block 的 `model` 参数为可选，留空时由 `llm_gateway` 走平台默认网关
- **依赖注入**：`LogicEngine(chat_fn=llm_gateway.chat)` 允许测试注入 mock
- **调试不落库**：`debug=True` 时收集 CoT + proposed_edits，但不执行真实写回
- **复用现有**：UseLLM → `llm_gateway.chat()`；Transform → W1-1 `evaluate()`；ApplyAction → W1-7 `ShellCore`

## 3. 数据模型

### 3.1 Block 类型
```python
BlockKind = Literal[
    "input",           # 接收入参
    "create_variable", # 创建变量（表达式）
    "get_property",    # 获取对象属性
    "use_llm",         # 调用 LLM
    "transform",       # 调用 Function 引擎
    "apply_action",    # 调用 Action 写回
    "execute",         # 执行子流程/语义搜索
]

class Block(BaseModel):
    id: str
    kind: BlockKind
    name: str = ""
    config: dict[str, Any] = {}  # 各 kind 特定配置
```

### 3.2 UseLLM Block 配置
```python
config = {
    "prompt": "请分析 {{input_text}}",   # {{var}} 变量注入
    "model": "",                          # 空=走默认网关；不写死
    "system_prompt": "",                  # 可选 system prompt
    "few_shot": [],                       # Few-shot 示例列表
    "tools": [],                          # 工具集 id 列表
}
```

### 3.3 执行上下文 + 调试数据
```python
class BlockResult(BaseModel):
    block_id: str
    output: Any
    cot: list[str] = []              # CoT 思维链片段
    proposed_edits: list[dict] = []  # 提议 edits（调试模式）

class ExecutionContext(BaseModel):
    variables: dict[str, Any] = {}
    results: list[BlockResult] = []
    cot: list[str] = []              # 全局 CoT 收集
    proposed_edits: list[dict] = []  # 全局提议 edits
```

### 3.4 Edits 合并
```python
MergeStrategy = Literal["last_write_wins", "field_level", "manual_review"]

class EditEntry(BaseModel):
    pk: str
    field: str
    value: Any
    source_block_id: str

def merge_edits(edits: list[EditEntry], strategy) -> list[EditEntry]
```

## 4. 执行算法
```
def run(blocks, inputs, debug=False):
    ctx = ExecutionContext(variables=inputs)
    for block in blocks:
        result = _exec_block(block, ctx, debug)
        ctx.results.append(result)
        ctx.cot.extend(result.cot)
        ctx.proposed_edits.extend(result.proposed_edits)
    return ctx
```

### 4.1 各 Block 执行逻辑
| Kind | 逻辑 |
|------|------|
| input | 将 inputs 注入 ctx.variables |
| create_variable | `evaluate(config["expr"], ctx.variables)` → 存入 variables |
| get_property | 从 variables 中取 `config["source"]` 的 `config["property"]` |
| use_llm | 渲染 prompt（变量注入）→ `chat_fn(prompt, model=config.get("model"))` → 存入 variables |
| transform | `evaluate(config["expr"], ctx.variables)` → 存入 variables |
| apply_action | 收集 edits → debug 模式存 proposed_edits；非 debug 调用 ShellCore 写回 |
| execute | 执行子流程或语义搜索（Phase 4 MVP：占位返回 variables） |

### 4.2 Prompt 变量注入
```python
def _render_prompt(template: str, variables: dict) -> str:
    # {{var}} → variables["var"]
    for key, val in variables.items():
        template = template.replace(f"{{{{{key}}}}}", str(val))
    return template
```

## 5. REST API (`/v1/logic`)
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/v1/logic/run` | 执行 Block 链（body: {blocks, inputs}） |
| POST | `/v1/logic/debug` | 调试运行（收集 CoT + proposed_edits，不写回） |
| GET | `/v1/logic/blocks` | Block 类型目录 |

## 6. 测试矩阵（≥ 14）
| 测试 | 说明 |
|------|------|
| `test_block_input` | Input Block 接收入参 |
| `test_block_create_variable` | CreateVariable 创建变量 |
| `test_block_get_property` | GetProperty 获取属性 |
| `test_block_use_llm_mock` | UseLLM 调用（mock chat_fn） |
| `test_block_transform` | Transform 调用 Function 引擎 |
| `test_block_apply_action` | ApplyAction 写回 |
| `test_block_chain_sequential` | 多 Block 顺序执行 |
| `test_debug_cot_collection` | 调试收集 CoT |
| `test_debug_proposed_edits` | 调试收集 proposed_edits |
| `test_edits_merge_last_write_wins` | LastWriteWins |
| `test_edits_merge_field_level` | 字段级合并 |
| `test_prompt_variable_injection` | `{{var}}` 注入 |
| `test_prompt_few_shot` | Few-shot 注入 |
| `test_ontology_writeback_four_steps` | UseLLM→发布→Action→Workshop |
| `test_use_llm_with_agnes` | Agnes 实连（读 .env，可选 skip） |

## 7. 文件清单
| 文件 | 动作 |
|------|------|
| `aos_api/logic_engine.py` | 新增 |
| `aos_api/routers/logic.py` | 新增 |
| `aos_api/main.py` | 修改（注册 router） |
| `tests/test_logic_engine.py` | 新增 |
| `scripts/smoke_agnes_logic.sh` | 新增（Agnes 实连 smoke） |

## 8. 不做的事
- ❌ 前端三栏 UI（前端独立交付）
- ❌ LangGraph 运行时内核（Phase 5+ 评估）
- ❌ 真异步并发执行（MVP 同步顺序执行）
- ❌ Automate 集成（Phase 5+）

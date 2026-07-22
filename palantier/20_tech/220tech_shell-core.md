# 220tech · W1-7 壳核模式（Shell-Core Pattern）

> **版本**：v1.0 · 2026-07-22
> **关联**：220plan §1.2.2 W1-7 · Phase 3 · 高优先级
> **依赖**：W1-1 function_engine（表达式求值）、W1-19 functions_python_builder（`python:` 执行）、W1-6 writeback（L1 写回）
> **范围**：ACT-SPEC（壳：声明性 Action 规格）+ FUNC-SPEC（核：函数实现引用）+ ShellCore 编排器

---

## 1. 目标与差距

| 维度 | 当前 | 目标 |
| --- | --- | --- |
| Action-Function 关系 | Action 直接硬编码逻辑 | Action 声明性规格（ACT-SPEC）引用函数实现（FUNC-SPEC） |
| 关注点分离 | 逻辑混在 Action 里 | 壳（协议：校验/权限/写回）vs 核（计算：纯函数） |
| 函数来源 | 无统一抽象 | 表达式（W1-1）或 Python（W1-19）均可作为核 |
| 写回触发 | 手动调 writeback | ACT-SPEC 声明 writeback_target，自动触发 |

## 2. 核心数据结构

### 2.1 FuncSpec（核）

```python
class FuncSpec(BaseModel):
    name: str                              # 唯一函数规格名
    kind: Literal["expression", "python"]  # 核类型
    ref: str                               # kind=expression: 表达式文本；kind=python: python 函数名
    description: str = ""
```

### 2.2 ActSpec（壳）

```python
class ActSpec(BaseModel):
    name: str                              # Action 名
    func_ref: str                          # 引用的 FuncSpec.name
    input_schema: dict[str, str] = {}      # 参数名 → 类型（"string"/"number"/"boolean"/"list"/"object"）
    output_mapping: dict[str, str] = {}    # 输出字段 → 表达式（基于 result 求值，空则原样返回 result）
    writeback: WritebackTarget | None = None
    description: str = ""

class WritebackTarget(BaseModel):
    dataset_rid: str
    pk_field: str = "id"
    op: Literal["upsert", "soft_delete"] = "upsert"
    row_from: str = "result"               # 取 result 还是 params 作为 row 源
```

### 2.3 执行结果

```python
class ShellExecution(BaseModel):
    action: str
    func_result: Any                       # 核返回的原始结果
    mapped: dict[str, Any]                 # output_mapping 后的结构化输出
    writeback_txn: str | None              # 若触发写回
    duration_ms: float
```

## 3. ShellCore 编排器

```python
class ShellCore:
    def register_func(self, spec: FuncSpec) -> FuncSpec
    def register_action(self, spec: ActSpec) -> ActSpec
    def get_func(self, name) -> FuncSpec
    def get_action(self, name) -> ActSpec
    def list_funcs() / list_actions()
    def execute(self, action_name: str, params: dict) -> ShellExecution
```

### 3.1 execute 流程

```
1. 取 ActSpec；不存在 → ACT_NOT_FOUND
2. 取 FuncSpec via act.func_ref；不存在 → FUNC_NOT_FOUND
3. 校验 params vs input_schema：
   - 必填字段缺失 → INPUT_MISSING
   - 类型不符 → INPUT_TYPE_MISMATCH
4. 执行核（core）：
   - kind=expression: result = Evaluator.evaluate(parse(ref), params)
   - kind=python: result = PythonBuilder.call_raw(ref, [params])[0]（单行模式）
   - 异常 → FUNC_EXEC_ERROR
5. output_mapping：
   - 对每个 (field, expr)：mapped[field] = Evaluator.evaluate(parse(expr), {"result": result, "params": params})
   - mapping 为空：mapped = {"result": result}
6. writeback（若声明）：
   - row 源 = mapped if row_from=="result" else params
   - 调 WritebackStore：begin → apply(op, pk, row) → commit
   - txn_id 记入 ShellExecution
7. 返回 ShellExecution
```

## 4. 类型校验规则

| 声明类型 | 接受 |
| --- | --- |
| `string` | str |
| `number` | int/float |
| `boolean` | bool |
| `list` | list |
| `object` | dict |

缺失字段若不在 input_schema 必填集中（即所有 schema 字段都必填）→ INPUT_MISSING。

## 5. REST API

> 命名空间 `/v1/shell-core`。

| 方法 | 路径 | 功能 |
| --- | --- | --- |
| POST | `/v1/shell-core/funcs` | 注册 FuncSpec |
| GET  | `/v1/shell-core/funcs` | 列表 |
| POST | `/v1/shell-core/actions` | 注册 ActSpec |
| GET  | `/v1/shell-core/actions` | 列表 |
| POST | `/v1/shell-core/actions/{name}/execute` | 执行（body: {params: {...}}） |
| GET  | `/v1/shell-core/funcs/{name}` | 详情 |
| GET  | `/v1/shell-core/actions/{name}` | 详情 |

## 6. 测试用例（≥ 16）

### 6.1 引擎（≥ 10）

1. register_func + get_func
2. register_action + get_action
3. execute expression 核：params={a:2,b:3}, ref="a + b" → 5
4. execute python 核：注册 doubler，params={x:10} → 20
5. execute output_mapping：result → {double: result * 2}
6. execute writeback upsert：mapped 写入 L1
7. execute writeback soft_delete
8. INPUT_MISSING：缺必填字段
9. INPUT_TYPE_MISMATCH：string 传 number
10. ACT_NOT_FOUND
11. FUNC_NOT_FOUND（act 引用不存在的 func）
12. FUNC_EXEC_ERROR：表达式语法错误

### 6.2 API（≥ 6）

13. POST /funcs 注册
14. POST /actions 注册
15. POST /execute → 返回 ShellExecution
16. GET /funcs 列表
17. GET /actions 列表
18. execute 404（action 不存在）
19. execute + writeback 联动验证

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 表达式异常 | try/except 转 FUNC_EXEC_ERROR |
| 循环引用 | act.func_ref 不存在时立即失败 |
| writeback 失败 | 捕获 WritebackError，记入 ShellExecution.writeback_txn=None + 错误备注 |
| 类型宽松 | 仅做 isinstance 检查，不做深层 schema 校验（Phase 6 强化） |

## 8. 文件清单

| 路径 | 类型 | 说明 |
| --- | --- | --- |
| `aos_api/shell_core.py` | 新增 | FuncSpec/ActSpec/ShellCore |
| `aos_api/routers/shell_core.py` | 新增 | 7 个 REST 端点 |
| `aos_api/main.py` | 修改 | 注册 router |
| `tests/test_shell_core.py` | 新增 | 19 个测试 |

## 9. 不做的事

- ❌ ACT-SPEC 持久化（DB 在 Phase 6）
- ❌ 权限模型（W1-17 角色体系负责）
- ❌ 多核组合（一个 ActSpec 一个 FuncSpec，多核在 Phase 6）
- ❌ 异步执行（本期同步，异步在 W1-11 Pipeline 重试）

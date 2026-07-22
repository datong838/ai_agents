# 220tech · W1-19 Functions Python Builder

> **版本**：v1.0 · 2026-07-22
> **关联**：220plan §1.2.2 W1-19 · Phase 2 · 高优先级
> **依赖**：W1-14 PipelineEditor（Python 函数可作为 transform 节点的 op）、Python 内建 ast/signal
> **范围**：用户提交 Python 代码 → 受限 namespace 编译执行 → 注册为可用 transform 函数；REST API + Pipeline Builder 集成

---

## 1. 目标与差距

| 维度 | 当前 | 目标 |
| --- | --- | --- |
| 函数来源 | 仅 9 个内置 transform 算子 | 用户可提交自定义 Python `transform(rows) -> rows` |
| 执行隔离 | 无 | ast 黑名单 + 行数/节点数上限 + SIGALRM 软超时 |
| Pipeline 集成 | 仅 `op="filter"` 等内置 op | `op="python:my_func"` 引用用户注册函数 |
| 代码安全 | 无 | 禁止 import os/sys/subprocess/socket；禁止 eval/exec/__import__ |

## 2. 数据模型

```python
class PythonFunction(BaseModel):
    name: str                    # 唯一函数名（[a-zA-Z_][a-zA-Z0-9_]*）
    code: str                    # Python 源码，必须定义 def transform(rows): ...
    description: str = ""
    created_at: str
    updated_at: str

class ExecutionResult(BaseModel):
    name: str
    input_count: int
    output_count: int
    duration_ms: float
    rows: list[dict]             # 实际输出（受 MAX_RETURN_ROWS 限制）
```

## 3. 安全限制

### 3.1 代码静态检查（ast）

| 规则 | 触发 | 错误码 |
| --- | --- | --- |
| 语法错误 | `ast.parse(code)` 失败 | CODE_PARSE_ERROR |
| 黑名单 import | Import/ImportFrom 模块在 `_BLOCKED_MODULES` | CODE_BLOCKED_IMPORT |
| 危险内建调用 | Call 节点 func.id 在 `_BLOCKED_BUILTINS` | CODE_BLOCKED_BUILTIN |
| 危险属性访问 | Attribute 节点 attr 以 `__` 开头（访问 dunder） | CODE_BLOCKED_DUNDER |
| 代码过大 | len(code) > MAX_CODE_SIZE (5KB) | CODE_TOO_LARGE |
| AST 节点过多 | ast 节点总数 > MAX_AST_NODES (1000) | CODE_TOO_COMPLEX |
| 缺少 transform 函数 | namespace 中无 `transform` 可调用对象 | CODE_NO_TRANSFORM |
| transform 签名错误 | transform 不是 callable 或参数数 ≠ 1 | CODE_BAD_SIGNATURE |

`_BLOCKED_MODULES = {"os", "sys", "subprocess", "socket", "shutil", "pickle", "ctypes", "multiprocessing"}`
`_BLOCKED_BUILTINS = {"eval", "exec", "compile", "__import__", "globals", "locals", "vars", "open", "input"}`

### 3.2 运行时限制

| 限制 | 值 | 实现 |
| --- | --- | --- |
| 超时 | 5 秒 | `signal.SIGALRM`（主线程），子线程退化为无超时但保留其他保护 |
| 输入行数上限 | 10000 | execute 入口检查 |
| 输出行数上限 | 10000 | execute 出口截断 |
| 安全 namespace | 仅白名单内建 | `_SAFE_BUILTINS` dict |

### 3.3 安全 namespace

```python
_SAFE_BUILTINS = {
    "len": len, "sum": sum, "min": min, "max": max,
    "sorted": sorted, "reversed": reversed, "filter": filter, "map": map,
    "range": range, "abs": abs, "round": round, "any": any, "all": all,
    "zip": zip, "enumerate": enumerate,
    "dict": dict, "list": list, "tuple": tuple, "set": set, "frozenset": frozenset,
    "str": str, "int": int, "float": float, "bool": bool,
    "True": True, "False": False, "None": None,
}
```

执行时：
```python
ns = {"__builtins__": _SAFE_BUILTINS}
exec(code, ns)
transform_fn = ns["transform"]
```

## 4. PythonBuilder 类

```python
class PythonBuilder:
    def register(self, name: str, code: str, description: str = "") -> PythonFunction
    def get(self, name: str) -> PythonFunction
    def list_all(self) -> list[PythonFunction]
    def delete(self, name: str) -> None
    def validate_code(self, code: str) -> list[str]    # 返回错误列表
    def execute(self, name: str, rows: list[dict], timeout: float = 5.0) -> ExecutionResult
```

## 5. Pipeline Builder 集成

W1-14 的 PipelineEditor 在 preview 时如果遇到 `op="python:my_func"`：
- 路径 1（推荐）：在 `apply_transform` 之前，由 PipelineEditor 检测 `op` 前缀 `python:`，从 PythonBuilder 取出函数直接调用（绕过 TRANSFORM_REGISTRY）
- 路径 2：PythonBuilder.register 时把函数也注入 TRANSFORM_REGISTRY（会污染全局，不推荐）

**采用路径 1**：在 `pipeline_builder.py` 的 `preview` 中加一段：
```python
if node.op.startswith("python:"):
    fn_name = node.op[len("python:"):]
    from .functions_python_builder import get_builder
    result = get_builder().call_raw(fn_name, merged_rows)
else:
    result = apply_transform(node.op, merged_rows, node.config)
```

## 6. REST API

| 方法 | 路径 | 功能 |
| --- | --- | --- |
| POST | `/v1/python-functions` | 注册/更新函数（body: {name, code, description}） |
| GET  | `/v1/python-functions` | 列表 |
| GET  | `/v1/python-functions/{name}` | 详情 |
| POST | `/v1/python-functions/{name}/execute` | 执行（body: {rows}） |
| POST | `/v1/python-functions/validate` | 校验代码（body: {code}） |
| DELETE | `/v1/python-functions/{name}` | 删除 |

## 7. 测试用例（≥ 16）

### 7.1 引擎（≥ 10）

1. register + get + list + delete 基本生命周期
2. validate_code 干净代码 → []
3. validate_code 缺 transform → CODE_NO_TRANSFORM
4. validate_code 黑名单 import os → CODE_BLOCKED_IMPORT
5. validate_code eval 调用 → CODE_BLOCKED_BUILTIN
6. validate_code dunder 访问 → CODE_BLOCKED_DUNDER
7. validate_code 语法错误 → CODE_PARSE_ERROR
8. validate_code 代码过大 → CODE_TOO_LARGE
9. execute 简单变换（每行 +1）→ 正确结果
10. execute 行数上限（>10000）→ 截断
11. execute transform 返回非 list → CODE_BAD_RETURN
12. execute 安全性：代码里读 `__import__("os")` → 失败（namespace 限制）

### 7.2 API（≥ 6）

13. POST 注册 → 200
14. GET 列表 → 含已注册
15. POST execute → 返回结果
16. POST validate → 返回错误列表
17. DELETE → 删除成功
18. 重复注册 → 更新（upsert 语义）
19. GET 不存在 → 404

## 8. Pipeline 集成测试

20. PipelineBuilder 加 python: 节点 → preview 执行正确
21. PipelineBuilder python: 引用不存在的函数 → 错误

## 9. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 代码执行逃逸 | 多层防护：ast 静态扫描 + namespace 限制 + 黑名单 |
| 死循环耗 CPU | SIGALRM（主线程）+ 行数/节点数上限 |
| GIL 限制子线程中断 | 文档明确：生产环境建议用 subprocess + seccomp 隔离；本期仅做软限制 |
| 大内存 | 输入输出行数双重上限 |
| 代码注入到主进程 | exec 在受限 ns 内，主进程变量不可见 |

## 10. 文件清单

| 路径 | 类型 | 说明 |
| --- | --- | --- |
| `aos_api/functions_python_builder.py` | 新增 | PythonBuilder + 安全检查 + 执行 |
| `aos_api/routers/python_functions.py` | 新增 | 6 个 REST 端点 |
| `aos_api/pipeline_builder.py` | 修改 | preview 支持 `python:` 前缀 op |
| `aos_api/main.py` | 修改 | 注册 python_functions router |
| `tests/test_functions_python_builder.py` | 新增 | 21 个测试 |

## 11. 不做的事

- ❌ 真正的容器/subprocess 隔离（生产期 Phase 6 用 Docker 或 nsjail）
- ❌ @transform 装饰器语法糖（W2+ #21）
- ❌ 多语言（Java/SQL/R）（W2+ #25）
- ❌ 持久化（本期内存，DB 在 Phase 6）
- ❌ Web IDE / IntelliSense（W2+ #22）

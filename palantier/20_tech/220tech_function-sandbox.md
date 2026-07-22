# 220tech · W1-10 Function 类型安全+沙箱 · 微观实现方案

> **版本**：v1.0 · 2026-07-22 · **关联**：[220plan](./220plan-分阶段开发与里程碑计划.md) §3.3 W1-10

## 1. 功能边界
| 子功能 | 本期 |
| --- | --- |
| 沙箱求值（超时+递归深度+AST 节点数限制） | ✅ |
| Function 可组合（注册→链式调用求值） | ✅ |
| TypeScript 类型生成（从表达式类型推导→TS） | ✅ |
| 内存限制 | ⚠️ 后置（Python 无原生 API，标注 TODO） |

## 2. 数据模型
```python
class FunctionDef(BaseModel):
    name: str
    expression: str
    params: dict[str, str] = {}      # 参数名→类型声明

class ComposeRequest(BaseModel):
    functions: list[FunctionDef]
    entry: str                        # 入口函数名
    context: dict[str, Any] = {}

class TypeScriptRequest(BaseModel):
    expression: str
    context_schema: dict[str, str] = {}
```

## 3. API 契约
| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | /v1/functions/sandbox/eval | 带超时的求值 |
| POST | /v1/functions/compose | 可组合 Function 链求值 |
| POST | /v1/functions/typescript | 生成 TS 类型定义 |

## 4. 核心类
```python
class SandboxedEvaluator:
    MAX_NODES = 1000
    MAX_DEPTH = 50
    TIMEOUT_SEC = 5.0
    def eval(expr, context) -> Any            # threading + timeout

class FunctionComposer:
    def register(defs: list[FunctionDef])     # 注册函数表
    def call(entry, context) -> Any           # 链式调用求值

_TS_MAP = {"number":"number","string":"string","boolean":"boolean","null":"null","any":"any","object":"Record<string, any>"}
class TypeGenerator:
    def generate(expr, context_schema) -> str # → TS 类型字符串
```

## 5. 接缝点
| 动作 | 文件 |
| --- | --- |
| 🆕 新建 | `aos_api/function_sandbox.py` |
| ✏️ 改 | `aos_api/routers/functions.py`（加 3 端点） |
| 🆕 新建 | `tests/test_function_sandbox.py` |

## 6. 测试细化（12 用例）
sandbox 超时成功/超时失败/节点超限/深度超限；compose 链式调用/未注册函数/循环依赖；TS 类型生成 number/string/boolean/property；API 3 端点冒烟。

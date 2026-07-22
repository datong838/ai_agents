# 220tech · W1-1 Function 表达式引擎 · 微观实现方案

> **版本**：v1.0 · 2026-07-22
> **关联宏观方案**：[220plan-分阶段开发与里程碑计划.md](./220plan-分阶段开发与里程碑计划.md) §3.1（W1-1）
> **关联差距分析**：[220w-与目标系统差距对照分析.md](./220w-与目标系统差距对照分析.md) §11 / §12 W1-1
> **开发规范**：遵循 [220plan §13](./220plan-分阶段开发与里程碑计划.md) 微观方案先行
> **代码库**：`/Users/ddt/work/projects/ai_agent/aos-platform`
> **状态**：⬜ 方案待 review → ⬜ 开发 → ⬜ 自测

---

## 0. 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案再编码 | 本文档为微观实现方案，review 通过后方可编码 |
| 优先查看 Rules | 已核对 220plan §3.1 宏观定义与现有代码约定 |
| 最小更改 | 新增 3 个文件，仅改 main.py 2 行注册路由 |
| 中文回答 | 文档全中文，代码注释按现有约定 |
| 涉及新增代码输出具体文件目录 | 见 §5 接缝点清单 |
| 代码开发完成后自测验证 | 见 §6 测试细化 + §7 自测清单 |

---

## 1. 功能边界（复述宏观方案，无新增无删减）

| 子功能 | 说明 | 本期范围 |
| --- | --- | --- |
| 表达式解析器 | 算术 / 字符串 / 属性访问 / 条件表达式 → AST | ✅ |
| 类型推导 | AST → 输出类型（string / number / boolean / timestamp / null） | ✅ |
| 求值引擎 | 输入上下文 + AST → 执行 → 结果 | ✅ |
| Ontology API 调用 | `object.getProperty("x")` / `object.link("y")` | ✅（接 object_store 读路径） |
| 错误处理 | 类型不匹配 / 空值 / 除零 → 结构化错误 | ✅ |

**不做**（属 W1-10 沙箱 / 后续项）：沙箱隔离、超时控制、内存限制、Function 可组合链式调用。

---

## 2. 数据模型（Pydantic Schema 字段表）

### 2.1 AST 节点类型联合（`function_engine.py` 内定义，非 Pydantic，用 dataclass）

| 节点类型 | 字段 | 说明 |
| --- | --- | --- |
| `Literal(value: Any, type: str)` | value / type | 字面量：数字/字符串/布尔/null |
| `Identifier(name: str)` | name | 变量引用，如 `amount` |
| `PropertyAccess(obj: Expr, attr: str, safe: bool)` | obj / attr / safe | `a.b` 或 `a?.b`（safe=True 为空安全） |
| `FunctionCall(name: str, args: list[Expr])` | name / args | `getProperty("x")` / 内置函数 |
| `BinaryOp(op: str, left: Expr, right: Expr)` | op / left / right | `+ - * / > < >= <= == != && \|\|` |
| `UnaryOp(op: str, operand: Expr)` | op / operand | `! -` |
| `Conditional(cond: Expr, then: Expr, else_: Expr)` | cond / then / else_ | `if ... then ... else ...` |

> `Expr = Literal \| Identifier \| PropertyAccess \| FunctionCall \| BinaryOp \| UnaryOp \| Conditional`

### 2.2 API 请求/响应模型（Pydantic v2）

**`POST /v1/functions/eval`**

```python
class EvalRequest(BaseModel):
    expression: str                          # 表达式文本，如 "order.amount * 1.1"
    context: dict[str, Any] = Field(default_factory=dict)  # 变量绑定，如 {"order": {"amount": 100}}

class EvalResponse(BaseModel):
    result: Any                              # 求值结果（可为 number/string/bool/null）
    type: str                                # 结果类型："number"|"string"|"boolean"|"null"|"object"
```

**`POST /v1/functions/typecheck`**

```python
class TypeCheckRequest(BaseModel):
    expression: str
    context_schema: dict[str, str] = Field(default_factory=dict)  # 变量类型声明，如 {"order": "object", "amount": "number"}

class TypeCheckResponse(BaseModel):
    ok: bool
    inferred_type: str | None = None         # ok=True 时给出推导类型
    errors: list[TypeError] = Field(default_factory=list)  # ok=False 时给出错误列表
```

### 2.3 错误模型

```python
class FunctionError(BaseModel):
    code: str                                # "TYPE_MISMATCH"|"DIVISION_BY_ZERO"|"NULL_DEREF"|"UNDEFINED_VAR"|"PARSE_ERROR"
    message: str
    position: int | None = None              # 表达式文本中的字符偏移（解析阶段错误）
    detail: dict[str, Any] | None = None
```

---

## 3. API 契约（OpenAPI 片段）

```yaml
paths:
  /v1/functions/eval:
    post:
      tags: [functions]
      summary: 求值表达式
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [expression]
              properties:
                expression: { type: string }
                context: { type: object, additionalProperties: true }
      responses:
        "200":
          description: 求值成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  result: {}
                  type: { type: string }
        "400":
          description: 表达式错误（类型不匹配/除零/空值/未定义变量/解析失败）
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/FunctionError"

  /v1/functions/typecheck:
    post:
      tags: [functions]
      summary: 类型检查（不求值）
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [expression]
              properties:
                expression: { type: string }
                context_schema: { type: object, additionalProperties: { type: string } }
      responses:
        "200":
          description: 类型检查结果（不论 ok 值都返回 200）
          content:
            application/json:
              schema:
                type: object
                properties:
                  ok: { type: boolean }
                  inferred_type: { type: string, nullable: true }
                  errors:
                    type: array
                    items: { $ref: "#/components/schemas/FunctionError" }

components:
  schemas:
    FunctionError:
      type: object
      required: [code, message]
      properties:
        code: { type: string }
        message: { type: string }
        position: { type: integer, nullable: true }
        detail: { type: object, nullable: true }
```

---

## 4. 核心类 / 函数设计

### 4.1 文件结构（3 个新文件）

```
services/aos-api/aos_api/
├── function_engine.py      ← 引擎核心（词法/语法/求值/类型推导）
└── routers/
    └── functions.py        ← API 路由（eval / typecheck）
services/aos-api/tests/
└── test_function_engine.py ← 单元测试
```

### 4.2 `function_engine.py` 核心类设计

```python
# === 词法分析 ===
class Token:
    type: str        # "NUMBER"|"STRING"|"IDENT"|"OP"|"LPAREN"|"RPAREN"|"DOT"|"COMMA"|"EOF"
    value: str
    position: int

class Lexer:
    def __init__(self, text: str) -> None
    def tokenize(self) -> list[Token]
    # 逐字符扫描，数字支持小数，字符串支持双引号，标识符支持字母数字下划线
    # 运算符：+ - * / > < >= <= == != ! && ||
    # 关键字：if then else true false null（在 IDENT 基础上识别）

# === 语法分析（递归下降）===
class Parser:
    def __init__(self, tokens: list[Token]) -> None
    def parse(self) -> Expr
    # 文法优先级（从低到高）：
    #   conditional  := "if" or_expr "then" conditional "else" conditional
    #   or_expr      := and_expr ("||" and_expr)*
    #   and_expr     := equality ("&&" equality)*
    #   equality     := comparison (("=="|"!=") comparison)*
    #   comparison   := additive ((">"|"<"|">="|"<=") additive)*
    #   additive     := multiplicative (("+"|"-") multiplicative)*
    #   multiplicative := unary (("*"|"/") unary)*
    #   unary        := ("!"|"-") unary | postfix
    #   postfix      := primary ("." ident | "(" args ")")*
    #   primary      := NUMBER | STRING | "true" | "false" | "null"
    #                 | IDENT | "(" conditional ")"
    # 报错时抛 ParseError(position, message)

# === 求值 ===
class Evaluator:
    def __init__(self, object_resolver: Callable[[str], Any] | None = None) -> None
    def eval(self, expr: Expr, context: dict[str, Any]) -> Any
    # visitor 模式：按节点类型分发
    #   Literal → 返回 value
    #   Identifier → context[name]，不存在抛 FunctionError(UNDEFINED_VAR)
    #   PropertyAccess →
    #     safe=False 时 obj 为 None → FunctionError(NULL_DEREF)
    #     safe=True 时 obj 为 None → 返回 None
    #     特判：obj 是 dict → obj.get(attr)；obj 是 OntologyObject → object_resolver
    #   FunctionCall → 内置函数表 + Ontology API（getProperty/link）
    #   BinaryOp →
    #     算术：number ± number → number；string + string → string（拼接）
    #     字符串 + number → FunctionError(TYPE_MISMATCH)
    #     除零 → FunctionError(DIVISION_BY_ZERO)
    #     比较：同类型比较；跨类型 → TYPE_MISMATCH
    #     逻辑：&& || 短路求值
    #   UnaryOp → ! boolean → boolean；- number → number
    #   Conditional → cond 求值为 truthy → then，否则 else_

# === 类型推导 ===
class TypeInferer:
    def __init__(self, context_schema: dict[str, str]) -> None
    def infer(self, expr: Expr) -> str
    # 与 Evaluator 同构的 visitor，但不求值只推类型
    #   Literal → type 字段
    #   Identifier → context_schema[name]，缺省推 "any"
    #   BinaryOp 算术 → number ± number → number；string + string → string
    #   BinaryOp 比较 → "boolean"
    #   BinaryOp 逻辑 → "boolean"
    #   Conditional → then/else_ 类型一致 → 该类型；不一致 → TYPE_MISMATCH
```

### 4.3 内置函数表（`FunctionCall` 节点处理）

| 函数名 | 参数 | 返回 | 说明 |
| --- | --- | --- | --- |
| `getProperty` | (obj, name: str) | Any | Ontology API：从对象取属性 |
| `link` | (obj, link_name: str) | list | Ontology API：取关联对象 |
| `len` | (str \| list) | number | 长度 |
| `upper` / `lower` | (str) | str | 大小写转换 |
| `toString` | (Any) | str | 转字符串 |

> 内置函数表为 `dict[str, Callable]`，后续 W1 项可扩展。

### 4.4 `routers/functions.py` 路由签名

```python
from fastapi import APIRouter, HTTPException
from aos_api.function_engine import Lexer, Parser, Evaluator, TypeInferer, FunctionError

router = APIRouter(tags=["functions"])

@router.post("/v1/functions/eval")
def eval_expression(req: EvalRequest) -> EvalResponse: ...

@router.post("/v1/functions/typecheck")
def typecheck_expression(req: TypeCheckRequest) -> TypeCheckResponse: ...
```

---

## 5. 与现有代码接缝点（改哪个文件 / 加哪个路由）

| 动作 | 文件 | 说明 |
| --- | --- | --- |
| 🆕 新建 | `services/aos-api/aos_api/function_engine.py` | 引擎核心（Lexer/Parser/Evaluator/TypeInferer + AST dataclass + 错误模型） |
| 🆕 新建 | `services/aos-api/aos_api/routers/functions.py` | 两个 POST 端点，依赖 function_engine |
| ✏️ 改 | `services/aos-api/aos_api/main.py` | ① import 块（第 14 行 `from aos_api.routers import (...)`）加 `functions` · ② include_router 区（第 122 行后）加 `application.include_router(functions.router)` |
| 🆕 新建 | `services/aos-api/tests/test_function_engine.py` | 单元测试（见 §6） |

**不动**：`object_store.py`（本期 Ontology API 走 object_resolver 回调注入，不改 object_store 接口）、`errors.py`（用本模块自定义 FunctionError，不污染全局错误体系）。

---

## 6. 测试细化（220plan §3.1.3 用例名 → 具体断言）

### 6.1 `test_function_engine.py`（引擎核心，13 个用例）

| 用例名 | 表达式 | 上下文 | 断言 |
| --- | --- | --- | --- |
| `test_arithmetic_expression` | `1 + 2 * 3` | {} | `result == 7` |
| `test_arithmetic_precedence` | `(1 + 2) * 3` | {} | `result == 9` |
| `test_string_concat` | `"Hello" + " " + name` | {name: "World"} | `result == "Hello World"` |
| `test_property_access` | `order.amount * 1.1` | {order: {amount: 100}} | `result == 110.0` |
| `test_safe_property_access` | `order?.customer?.name` | {order: None} | `result is None`（不抛错） |
| `test_unsafe_property_access_null` | `order.customer.name` | {order: None} | 抛 `FunctionError(code="NULL_DEREF")` |
| `test_conditional_expression_true` | `if amount > 100 then "大额" else "小额"` | {amount: 200} | `result == "大额"` |
| `test_conditional_expression_false` | 同上 | {amount: 50} | `result == "小额"` |
| `test_logical_and_short_circuit` | `false && undefined_var` | {} | `result == False`（短路，不报 UNDEFINED_VAR） |
| `test_type_inference_number` | `1 + 2` | 推导 | `inferred_type == "number"` |
| `test_type_inference_string` | `"a" + "b"` | 推导 | `inferred_type == "string"` |
| `test_type_inference_boolean` | `1 > 2` | 推导 | `inferred_type == "boolean"` |
| `test_type_error_mismatch` | `"a" + 1` | 求值 | 抛 `FunctionError(code="TYPE_MISMATCH")` |
| `test_division_by_zero` | `1 / 0` | {} | 抛 `FunctionError(code="DIVISION_BY_ZERO")` |
| `test_undefined_variable` | `undefined_var` | {} | 抛 `FunctionError(code="UNDEFINED_VAR")` |
| `test_parse_error_unexpected` | `1 +` | {} | 抛 `FunctionError(code="PARSE_ERROR")` |
| `test_ontology_get_property` | `order.getProperty("amount")` | {order: OntologyObjectStub} | `result == 100` |
| `test_builtin_len` | `len(name)` | {name: "abc"} | `result == 3` |
| `test_complex_expression` | `if order.amount * 1.1 > 110 then "大额" else "小额"` | {order: {amount: 100}} | `result == "小额"` |

> `OntologyObjectStub`：测试桩对象，实现 `get_property(name)` 方法返回预设值，模拟 object_store 读路径。

### 6.2 API 层测试（4 个用例，可并入 `test_function_engine.py` 或单独 `test_functions_api.py`）

| 用例名 | 请求 | 断言 |
| --- | --- | --- |
| `test_eval_endpoint` | POST /v1/functions/eval {expression: "1+2"} | 200, {result: 3, type: "number"} |
| `test_typecheck_endpoint` | POST /v1/functions/typecheck {expression: "1>2"} | 200, {ok: true, inferred_type: "boolean"} |
| `test_eval_error_400` | POST /v1/functions/eval {expression: "1/0"} | 400, body.code == "DIVISION_BY_ZERO" |
| `test_eval_parse_error_400` | POST /v1/functions/eval {expression: "1 +"} | 400, body.code == "PARSE_ERROR" |

---

## 7. 自测清单（对照 220plan §0.4 波次集成自测）

| # | 检查项 | 方法 | 通过标准 |
| --- | --- | --- | --- |
| ① | 后端重启 | `cd services/aos-api && python -m aos_api.main` | startup log 无报错 |
| ② | 全量测试 | `cd services/aos-api && python -m pytest tests/test_function_engine.py -v` | 全绿（17+4 用例） |
| ③ | 不破坏现有测试 | `python -m pytest tests/ -v` | 现有用例不回归 |
| ④ | API 冒烟 | curl POST /v1/functions/eval + typecheck | 返回符合 §3 契约 |
| ⑤ | 更新进度 | 220plan §1.2.2 W1-1 ⬜ → ✅ | 状态已置 ✅ |

**本期无 UI 改动**（W1-1 无独立页面，UI 展示形态属 W1-18 OMA Function Type 视图，不在本期）。

---

## 8. 风险与缓解

| 风险 | 影响 | 缓解 |
| --- | --- | --- |
| 递归下降解析器边界 case 多（嵌套括号/运算符优先级） | 解析 bug | 文法优先级表（§4.2）先写死，逐级单测覆盖 |
| Ontology API 与 object_store 耦合 | 引擎被业务逻辑污染 | 用 object_resolver 回调注入，引擎不直接 import object_store |
| 字符串拼接 vs 算术加法的 `+` 歧义 | 类型推断错误 | BinaryOp `+` 先检查左右类型：string+string→拼接，number+number→算术，其余 TYPE_MISMATCH |
| 表达式注入（恶意超长表达式） | 性能 / 栈溢出 | 本期不做沙箱（属 W1-10），但限制表达式长度上限 4096 字符 |

---

## 9. 不在本期范围（明确边界）

| 项 | 归属 |
| --- | --- |
| 沙箱隔离 / 超时 / 内存限制 | W1-10 Function 沙箱 |
| Function 可组合（A→B 链式调用） | W1-10 子能力 |
| Schema → TypeScript 类型生成 | W1-10 子能力 |
| Function Type 视图 UI（Overview/Configuration/Type Safety/Usage History Tab） | W1-18 |
| 多语言函数（Python/Java） | 远期停车场 |

---

## 10. 变更

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-07-22 | 初版 · 对齐 220plan §3.1 W1-1 宏观定义 · 含 AST/API/核心类/接缝点/19 用例 |

---

*v1.0 · w1*

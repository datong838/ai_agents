# 220tech · W1-18 OMA Function Type 视图

> **版本**：v1.0 · 2026-07-22
> **关联**：220plan §1.2.2 W1-18 · Phase 3 · 高优先级
> **依赖**：W1-7 shell_core.FuncSpec（表达式函数）、W1-19 functions_python_builder.PythonFunction（Python 函数）
> **范围**：Function 作为 Object Type 的管理视图（概览 + 使用历史 + 版本历史 + 跳转代码库）

---

## 1. 目标与差距

| 维度 | 当前 | 目标 |
| --- | --- | --- |
| 函数概览 | 散在 shell_core / python_builder 各自模块 | 统一 FunctionTypeView 聚合 |
| 使用历史 | 无 | 记录被哪些 ActSpec / Pipeline node 引用 |
| 版本历史 | 仅 updated_at | 每次更新留 VersionRecord 快照 |
| 跳转代码库 | 无 | CodeLocation（repo / path / line） |

## 2. 核心数据结构

```python
class FunctionTypeView(BaseModel):
    name: str
    kind: Literal["expression", "python"]   # 来自 W1-7 FuncSpec.kind
    description: str = ""
    signature: str                           # 可读签名
    created_at: str
    updated_at: str
    usage_count: int
    version_count: int
    latest_code_location: CodeLocation | None = None

class UsageRecord(BaseModel):
    function_name: str
    used_in: str                             # "action:sum" / "pipeline:p1/node:flt"
    used_in_kind: Literal["action", "pipeline_node"]
    recorded_at: str

class VersionRecord(BaseModel):
    function_name: str
    version: int
    snapshot: dict                           # 当时的 spec/code/description
    recorded_at: str
    recorded_by: str = ""

class CodeLocation(BaseModel):
    repo: str = ""
    path: str = ""
    line: int = 0
    url: str = ""                            # 可点击跳转的完整 URL
```

## 3. FunctionRegistry 类

```python
class FunctionRegistry:
    def aggregate_all(self) -> list[FunctionTypeView]
        # 从 ShellCore.list_funcs() + PythonBuilder.list_all() 聚合
    def get_view(self, name: str) -> FunctionTypeView
    def get_usage(self, name: str) -> list[UsageRecord]
    def get_versions(self, name: str) -> list[VersionRecord]
    def record_usage(self, name, used_in, kind) -> UsageRecord
    def record_version(self, name, snapshot, recorded_by="") -> VersionRecord
    def set_code_location(self, name, location) -> None
```

### 3.1 聚合算法

```
1. funcs = ShellCore.list_funcs()  # W1-7
2. py_funcs = PythonBuilder.list_all()  # W1-19
3. 对每个 func：
   - kind 来自 func.kind
   - description / created_at / updated_at 来自原对象
   - signature：
     * expression: f(params) -> <expr>
     * python: transform(rows: list) -> list
   - usage_count / version_count 来自 Registry 内部追踪
   - latest_code_location 来自 Registry
```

### 3.2 版本追踪

- `record_version` 在函数注册/更新时调用（由 ShellCore/PythonBuilder 的调用方负责触发）
- 每次 version+1，保留 snapshot dict

## 4. REST API

> 命名空间 `/v1/oma/function-types`。

| 方法 | 路径 | 功能 |
| --- | --- | --- |
| GET | `/v1/oma/function-types` | 聚合所有函数概览 |
| GET | `/v1/oma/function-types/{name}` | 单个函数详情 |
| GET | `/v1/oma/function-types/{name}/usage` | 使用历史 |
| GET | `/v1/oma/function-types/{name}/versions` | 版本历史 |
| POST | `/v1/oma/function-types/{name}/code-location` | 设置代码位置 |
| POST | `/v1/oma/function-types/{name}/record-usage` | 记录使用 |

## 5. 测试用例（≥ 16）

### 5.1 引擎（≥ 10）

1. aggregate_all 空时返回 []
2. 注册 expression func → aggregate_all 含
3. 注册 python func → aggregate_all 含
4. 两者混合 → 全部聚合
5. get_view expression → signature 正确
6. get_view python → signature 正确
7. get_view 不存在 → NOT_FOUND
8. record_usage → get_usage 返回
9. record_version 多次 → get_versions 长度递增
10. set_code_location → get_view 含 location
11. usage_count 聚合正确
12. version_count 聚合正确

### 5.2 API（≥ 6）

13. GET / 聚合列表
14. GET /{name} 详情
15. GET /{name}/usage
16. GET /{name}/versions
17. POST /{name}/code-location
18. POST /{name}/record-usage
19. GET /{name} 不存在 → 404

## 6. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 函数被删后历史残留 | get_view 404，但 usage/versions 仍可查（历史不丢） |
| 聚合性能 | 本期内存，函数数量 <1000；Phase 6 加缓存 |
| 版本爆炸 | 上限 100 版本/函数，超出滚动删除最旧 |
| 并发 record | threading.Lock |

## 7. 文件清单

| 路径 | 类型 | 说明 |
| --- | --- | --- |
| `aos_api/function_type_view.py` | 新增 | FunctionRegistry + 视图模型 |
| `aos_api/routers/function_types.py` | 新增 | 6 个 REST 端点 |
| `aos_api/main.py` | 修改 | 注册 router |
| `tests/test_function_type_view.py` | 新增 | 19 个测试 |

## 8. 不做的事

- ❌ 自动 hook ShellCore/PythonBuilder 的 register（本期手动 record_version，自动 hook 在 Phase 6）
- ❌ Git 集成（真实代码位置在 Phase 6 接 Code Repositories）
- ❌ 函数搜索/过滤（Phase 6）

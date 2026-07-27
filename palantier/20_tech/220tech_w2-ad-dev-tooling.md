# 220tech · W2-AD · 开发者工具组（#104 / #105 / #106）

> **版本**：v1.0 · 2026-07-22
> **状态**：✅ 方案定稿 · 可编码
> **对齐**：
> - 差距分析 [220w](./220w-与目标系统差距对照分析.md) §11 #104/#105/#106
> - 上游 W2-AC 代码仓库与 PR 工作流（分支/PR/变换预览）
> **范围**：W2-AD 收口开发者工具三件 — Python Debugger（代码级调试器）/ Unit Test Runner（单元测试运行器）/ Artifact Registry（制品仓库）
> **不替换底层**：本组是开发工具层，不重写 functions_python_builder 沙箱 · 不重写 aip_extras.DebuggerEngine（AIP 逻辑调试器）
> **与 W2-V #78 区别**：#78 是 AIP Logic CoT 步进调试；#104 是 Python 代码断点/单步/数据框预览

---

## 0. 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文回答 | 文档与代码注释均中文 |
| 先方案后编码 | 本文先定稿，再写引擎/路由/测试 |
| 最小更改 | 仅新增 `aos_api/dev_tooling.py` + `aos_api/routers/dev_tooling.py` + `tests/test_dev_tooling.py`；`main.py` 加 2 行 |
| 不影响已有功能 | 三引擎纯新增；aip_extras.DebuggerEngine 保留；functions_python_builder 沙箱不动 |
| 自测验证 | 单测全绿 + 全量回归 + 方案对照 |
| 符合方案军规 | 调试器断点/单步与 220w §11 一致；单元测试 Python/Java/TypeScript 三语言；制品仓库 Conda/Docker/Maven 三格式 |

---

## 1. 背景与边界

### 1.1 现状

| 能力 | 现状 | 缺口 |
| --- | --- | --- |
| Python 代码调试器 | aip_extras.DebuggerEngine 是 AIP 逻辑 CoT 调试，非代码级 | 🔴 缺 |
| 单元测试运行器 | 无 | 🔴 缺 |
| 制品仓库 | 无 | 🔴 缺 |

### 1.2 边界

- ✅ 本组做：
  - #104 Python Debugger：断点设置/单步执行/变量快照/数据框预览（基于受限 exec）
  - #105 Unit Test Runner：Python/Java/TypeScript 三语言测试用例注册 + run 执行 + 结果收集
  - #106 Artifact Registry：Conda/Docker/Maven 三格式制品 CRUD + 版本管理 + 依赖查询
- ❌ 本组不做：
  - 实际 JVM/Node 运行时（Java/TS 测试仅记录结果状态）
  - 实际 Docker registry 推送（仅元数据管理）
  - IDE 集成 UI（属前端）

---

## 2. 数据模型

### 2.1 #104 Python Debugger

```python
class DebugSession(BaseModel):
    """调试会话。"""
    id: str
    code: str                      # 待调试 Python 代码
    breakpoints: list[int] = []    # 断点行号列表
    state: str = "created"         # created / running / paused / completed / error
    current_line: int = 0
    variables: dict[str, Any] = {} # 变量快照
    output: list[str] = []         # 输出行
    error_message: str = ""
    created_at: float = 0.0


class DebugStep(BaseModel):
    """单步执行记录。"""
    line: int
    variables: dict[str, Any] = {}
    output: str = ""
    is_breakpoint: bool = False


_VALID_DEBUG_STATES = {"created", "running", "paused", "completed", "error"}
```

### 2.2 #105 Unit Test Runner

```python
class TestCase(BaseModel):
    """单元测试用例。"""
    id: str
    name: str
    language: str                  # python / java / typescript
    code: str                      # 测试代码
    target_function: str = ""      # 被测函数
    timeout_seconds: float = 30.0
    created_at: float = 0.0


class TestResult(BaseModel):
    """测试执行结果。"""
    id: str
    case_id: str
    status: str                    # passed / failed / error / skipped
    output: str = ""
    error_message: str = ""
    duration_ms: float = 0.0
    executed_at: float = 0.0


_VALID_TEST_LANGUAGES = {"python", "java", "typescript"}
_VALID_TEST_STATUSES = {"passed", "failed", "error", "skipped"}
```

### 2.3 #106 Artifact Registry

```python
class Artifact(BaseModel):
    """制品。"""
    id: str
    name: str
    version: str
    format: str                    # conda / docker / maven
    registry_url: str = ""
    description: str = ""
    tags: list[str] = []
    dependencies: list[str] = []   # 依赖制品 ID 列表
    size_bytes: int = 0
    checksum: str = ""
    created_at: float = 0.0


_VALID_ARTIFACT_FORMATS = {"conda", "docker", "maven"}
```

---

## 3. 引擎设计

文件：`aos_api/dev_tooling.py`（新增，3 个引擎）

### 3.1 PythonDebuggerEngine（#104）

```python
class PythonDebuggerEngine:
    def create_session(self, code: str, breakpoints: list[int] | None = None) -> DebugSession: ...
    def get_session(self, session_id: str) -> DebugSession: ...
    def list_sessions(self, state: str | None = None) -> list[DebugSession]: ...
    def step(self, session_id: str) -> DebugStep: ...
    """单步：执行下一行，命中断点暂停，捕获变量快照"""
    def run_to_completion(self, session_id: str) -> DebugSession: ...
    """连续执行直到完成或命中断点"""
    def get_variables(self, session_id: str) -> dict[str, Any]: ...
    def delete_session(self, session_id: str) -> bool: ...
```

**step 流程**：
1. 取 session，校验 state in {created, paused}
2. 按行拆分 code，从 current_line 开始执行下一行
3. exec 单行在受限命名空间，捕获变量快照
4. 若下一行在 breakpoints → state=paused；否则继续
5. 全部行执行完 → state=completed
6. 异常 → state=error + error_message

### 3.2 UnitTestEngine（#105）

```python
class UnitTestEngine:
    def register(self, case: TestCase) -> TestCase: ...
    def get(self, case_id: str) -> TestCase: ...
    def list(self, language: str | None = None) -> list[TestCase]: ...
    def update(self, case_id: str, updates: dict[str, Any]) -> TestCase: ...
    def delete(self, case_id: str) -> bool: ...
    def run(self, case_id: str) -> TestResult: ...
    """执行测试：python exec + assert 捕获；java/ts 记录 simulated"""
    def list_results(self, case_id: str | None = None, limit: int = 50) -> list[TestResult]: ...
```

**run 流程**：
1. 取 case，python：exec 代码，捕获 AssertionError→failed，其他异常→error，正常→passed
2. java/typescript：简化为 simulated passed（无实际运行时）
3. 记录 TestResult，200 条上限

### 3.3 ArtifactRegistryEngine（#106）

```python
class ArtifactRegistryEngine:
    def register(self, artifact: Artifact) -> Artifact: ...
    def get(self, artifact_id: str) -> Artifact: ...
    def get_by_name_version(self, name: str, version: str) -> Artifact | None: ...
    def list(self, format: str | None = None, name: str | None = None, tag: str | None = None) -> list[Artifact]: ...
    def update(self, artifact_id: str, updates: dict[str, Any]) -> Artifact: ...
    def delete(self, artifact_id: str) -> bool: ...
    def list_versions(self, name: str) -> list[Artifact]: ...
    """列出某 name 的所有版本"""
    def list_dependencies(self, artifact_id: str) -> list[Artifact]: ...
    """解析依赖图，返回直接依赖的制品列表"""
```

### 3.4 单例与持久化

- 3 个引擎均用**双重检查锁单例**
- 内存态为主，各 200 条上限

---

## 4. API 设计

文件：`aos_api/routers/dev_tooling.py`（新增）

### 4.1 #104 Python Debugger

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/dev-tooling/debug-sessions` | 创建调试会话 |
| GET | `/v1/dev-tooling/debug-sessions` | 列表 |
| GET | `/v1/dev-tooling/debug-sessions/{session_id}` | 单条 |
| POST | `/v1/dev-tooling/debug-sessions/{session_id}/step` | 单步 |
| POST | `/v1/dev-tooling/debug-sessions/{session_id}/run` | 运行到完成 |
| GET | `/v1/dev-tooling/debug-sessions/{session_id}/variables` | 变量快照 |
| DELETE | `/v1/dev-tooling/debug-sessions/{session_id}` | 删除 |

### 4.2 #105 Unit Test Runner

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/dev-tooling/test-cases` | 注册测试用例 |
| GET | `/v1/dev-tooling/test-cases` | 列表 |
| GET | `/v1/dev-tooling/test-cases/{case_id}` | 单条 |
| PUT | `/v1/dev-tooling/test-cases/{case_id}` | 更新 |
| DELETE | `/v1/dev-tooling/test-cases/{case_id}` | 删除 |
| POST | `/v1/dev-tooling/test-cases/{case_id}/run` | 执行 |
| GET | `/v1/dev-tooling/test-results` | 结果列表 |

### 4.3 #106 Artifact Registry

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/dev-tooling/artifacts` | 注册制品 |
| GET | `/v1/dev-tooling/artifacts` | 列表 |
| GET | `/v1/dev-tooling/artifacts/{artifact_id}` | 单条 |
| PUT | `/v1/dev-tooling/artifacts/{artifact_id}` | 更新 |
| DELETE | `/v1/dev-tooling/artifacts/{artifact_id}` | 删除 |
| GET | `/v1/dev-tooling/artifacts/by-name/{name}/versions` | 版本列表 |
| GET | `/v1/dev-tooling/artifacts/{artifact_id}/dependencies` | 依赖列表 |

---

## 5. 集成点

### 5.1 main.py（最小更改）

```python
from aos_api.routers import (..., dev_tooling, ...)
application.include_router(dev_tooling.router)
```

### 5.2 与 W2-AC 协同

- DebugSession.code 可关联 W2-AC TransformPreview.transform_code
- TestCase 可针对 W2-AC Branch 上的代码
- Artifact 可关联 W2-AC repo_id

---

## 6. 测试计划

文件：`tests/test_dev_tooling.py`（新增，约 42 个用例）

### 6.1 PythonDebuggerEngine（14）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | create_session | 返回带 id，state=created |
| 2 | create_session 空 code | MISSING_CODE |
| 3 | get 未找到 | NOT_FOUND |
| 4 | list 默认 | 列表 |
| 5 | list 按 state 过滤 | 仅匹配 |
| 6 | step 单步 | current_line 推进 |
| 7 | step 命中断点 | state=paused |
| 8 | step 已完成 | SESSION_COMPLETED |
| 9 | run_to_completion | state=completed |
| 10 | run_to_completion 命中断点 | state=paused |
| 11 | get_variables | 返回变量快照 |
| 12 | step 异常 | state=error |
| 13 | delete | 删除成功 |
| 14 | 200 条 session 上限 | 旧记录淘汰 |

### 6.2 UnitTestEngine（14）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 缺 name | MISSING_NAME |
| 3 | register 未知 language | INVALID_LANGUAGE |
| 4 | get 未找到 | NOT_FOUND |
| 5 | list 默认 | 列表 |
| 6 | list 按 language 过滤 | 仅匹配 |
| 7 | update | 修改后返回新值 |
| 8 | delete | 删除成功 |
| 9 | run python passed | status=passed |
| 10 | run python failed | status=failed（AssertionError） |
| 11 | run python error | status=error（其他异常） |
| 12 | run java simulated | status=passed |
| 13 | list_results | 列表 |
| 14 | 200 条 result 上限 | 旧记录淘汰 |

### 6.3 ArtifactRegistryEngine（14）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 缺 name | MISSING_NAME |
| 3 | register 未知 format | INVALID_FORMAT |
| 4 | register 重名同版本 | NAME_VERSION_DUPLICATE |
| 5 | get 未找到 | NOT_FOUND |
| 6 | get_by_name_version | 返回匹配 |
| 7 | list 默认 | 列表 |
| 8 | list 按 format 过滤 | 仅匹配 |
| 9 | list 按 tag 过滤 | 仅匹配 |
| 10 | update | 修改后返回新值 |
| 11 | delete | 删除成功 |
| 12 | list_versions | 按 name 返回所有版本 |
| 13 | list_dependencies | 返回依赖制品 |
| 14 | 200 条上限 | 旧记录淘汰 |

---

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 调试器代码执行注入 | exec 在受限命名空间，禁用 open/input/eval 等 |
| 单步执行死循环 | run_to_completion 设最大行数上限（如 1000 行） |
| Java/TS 测试无法真实执行 | 简化为 simulated passed，明确标注 |
| 制品依赖循环 | list_dependencies 仅返回直接依赖，不递归 |
| 制品版本冲突 | register 检查 NAME_VERSION_DUPLICATE |

---

## 8. 交付物清单

| 路径 | 状态 | 说明 |
| --- | --- | --- |
| `docs/palantier/20_tech/220tech_w2-ad-dev-tooling.md` | ✅ 本文件 | 微规约 |
| `aos_api/dev_tooling.py` | ⬜ 待编码 | 3 引擎 |
| `aos_api/routers/dev_tooling.py` | ⬜ 待编码 | ~21 端点 |
| `tests/test_dev_tooling.py` | ⬜ 待编码 | ~42 用例 |
| `aos_api/main.py` | ⬜ +2 行 | import + include_router |

---

*v1.0 · w2-ad*

# 220tech · W2-AE · AIP 辅助与仓库配置组（#107 / #108 / #110）

> **版本**：v1.0 · 2026-07-22
> **状态**：✅ 方案定稿 · 可编码
> **对齐**：
> - 差距分析 [220w](./220w-与目标系统差距对照分析.md) §11 #107/#108/#110
> - 220plan v4.3 已交付 76/166，本批收口 3 项 → 79/166
> **范围**：W2-AE 收口代码辅助三件 — AIP Assist（代码解释/漏洞/翻译/补全）+ repoSettings.json（仓库配置）+ 推荐项目结构
> **不替换底层**：本组是辅助/配置层，不重写 AIP Logic CoT debugger（属 W2-V #78）或 wave_ext code-repos

---

## 0. 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文回答 | 文档与代码注释均中文 |
| 先方案后编码 | 本文先定稿，再写引擎/路由/测试 |
| 最小更改 | 仅新增 `aos_api/aip_assist.py` + `aos_api/routers/aip_assist.py` + `tests/test_aip_assist.py`；`main.py` 加 2 行 |
| 不影响已有功能 | 三引擎纯新增；aip_extras.py 与 wave_ext code-repos 列表保留 |
| 自测验证 | 单测全绿 + 全量回归 + 方案对照 |
| 编码前复习方案 | 已核对 W2-AC/W2-AD 引擎模式（单例 + 200 条 FIFO） |

---

## 1. 背景与边界

### 1.1 现状

| 能力 | 现状 | 缺口 |
| --- | --- | --- |
| AIP 代码辅助 | aip_extras.DebuggerEngine 是 CoT 调试器（W2-V #78），无 explain/vulnerability/translate/complete | 🔴 缺 |
| 仓库配置文件 | 无 repoSettings.json 管理 | 🔴 缺 |
| 推荐项目结构 | 无 Datasource→Transform→Ontology→Workflow 模板 | 🔴 缺 |

### 1.2 边界

- ✅ 本组做：
  - #107 AIP Assist：4 种 kind（explain/vulnerability/translate/complete）请求记录 + run（模拟返回）
  - #108 repoSettings.json：标签验证规则 / PR 模板 / 验证规则配置 + validate_label + render_pr_template
  - #110 推荐项目结构：模板 CRUD + render_template + validate_project（按层校验组件）
- ❌ 本组不做：
  - 真实 LLM 调用（run 用规则模拟返回）
  - 实际 Git 仓库写文件（仅配置记录）
  - 项目脚手架生成（仅返回模板结构）

### 1.3 与 #109 的关系

#109「列级血缘」的 CRUD 部分已由 W2-E #4 在 `aos-platform/services/aos-api/aos_api/routers/lineage_views.py:65-78` 交付（set_column_lineage / get_column_lineage + `test_column_level_lineage`）。本批不重复开发 #109，留待 W2-AF+ 处理「列级影响分析」增量端点。

---

## 2. 数据模型

### 2.1 #107 AIPAssistRequest

```python
class AIPAssistRequest(BaseModel):
    """AIP 代码辅助请求。"""
    id: str
    kind: str                       # explain / vulnerability / translate / complete
    code: str
    language: str = "python"        # python / java / typescript / sql
    context: str = ""
    status: str = "pending"         # pending / running / completed / error
    result: dict[str, Any] = {}
    created_at: float = 0.0
    completed_at: float = 0.0


_VALID_ASSIST_KINDS = {"explain", "vulnerability", "translate", "complete"}
_VALID_ASSIST_LANGUAGES = {"python", "java", "typescript", "sql"}
_VALID_ASSIST_STATUSES = {"pending", "running", "completed", "error"}
```

### 2.2 #108 RepoSettings

```python
class RepoSettings(BaseModel):
    """仓库配置文件（repoSettings.json）。"""
    id: str
    repo_id: str
    label_validation: dict[str, Any] = {}      # {"required_prefixes": [...], "color_required": bool}
    pr_template: str = ""                       # PR 模板正文
    validation_rules: list[dict[str, Any]] = []  # [{"kind": "branch_protection", "config": {...}}]
    enforce_branch_protection: bool = False
    created_at: float = 0.0
    updated_at: float = 0.0


_VALID_RULE_KINDS = {"branch_protection", "required_reviewers", "status_check", "path_filter"}
```

### 2.3 #110 ProjectStructure

```python
class StructureComponent(BaseModel):
    """结构组件。"""
    layer: str                    # datasource / transform / ontology / workflow
    name: str
    type: str                     # dataset / transform / ontology / workflow / metric
    rid_prefix: str = ""          # 资源 ID 前缀（如 "ds."）
    required: bool = False


class ProjectStructure(BaseModel):
    """推荐项目结构模板。"""
    id: str
    name: str
    description: str = ""
    layers: list[str] = []        # ["datasource", "transform", "ontology", "workflow"]
    components: list[StructureComponent] = []
    created_at: float = 0.0


_VALID_LAYERS = {"datasource", "transform", "ontology", "workflow"}
_VALID_COMPONENT_TYPES = {"dataset", "transform", "ontology", "workflow", "metric"}
```

---

## 3. 引擎设计

文件：`aos_api/aip_assist.py`（新增，3 个引擎）

### 3.1 AIPAssistEngine（#107）

```python
class AIPAssistEngine:
    def register(self, req: AIPAssistRequest) -> AIPAssistRequest: ...
    def get(self, req_id: str) -> AIPAssistRequest: ...
    def list(self, kind: str | None = None, status: str | None = None) -> list[AIPAssistRequest]: ...
    def update(self, req_id: str, updates: dict[str, Any]) -> AIPAssistRequest: ...
    def delete(self, req_id: str) -> bool: ...
    def run(self, req_id: str) -> AIPAssistRequest: ...
    """根据 kind 执行辅助，写回 result + status=completed"""
    def list_results(self, kind: str | None = None, limit: int = 50) -> list[AIPAssistRequest]: ...
```

**run 流程**：
1. 取 req，校验 status≠completed（不可重复 run；若重复则抛 ALREADY_COMPLETED）
2. status=running
3. 按 kind 分支：
   - explain：result = {"summary": f"代码共 {len(lines)} 行，语言 {language}", "lines": len(lines)}
   - vulnerability：扫描 dangerous builtins（open/eval/exec/compile/__import__），result = {"vulnerabilities": [...], "count": N}
   - translate：python→java 简化映射，result = {"translated": "...", "target_language": "java"}
   - complete：基于 code 末尾字符简单补全，result = {"suggestion": "..."}
4. 捕获异常 → status=error, result={"error": str(e)}
5. 200 条 result 上限（list_results）

### 3.2 RepoSettingsEngine（#108）

```python
class RepoSettingsEngine:
    def register(self, settings: RepoSettings) -> RepoSettings: ...
    def get(self, settings_id: str) -> RepoSettings: ...
    def get_by_repo(self, repo_id: str) -> RepoSettings | None: ...
    def list(self, repo_id: str | None = None) -> list[RepoSettings]: ...
    def update(self, settings_id: str, updates: dict[str, Any]) -> RepoSettings: ...
    def delete(self, settings_id: str) -> bool: ...
    def validate_label(self, settings_id: str, label: str) -> dict[str, Any]: ...
    """检查标签是否符合 label_validation.required_prefixes；返回 {valid, reason}"""
    def render_pr_template(self, settings_id: str, context: dict[str, Any]) -> str: ...
    """用 context 简单替换模板中的 {key} 占位符"""
```

**validate_label 流程**：
1. 取 settings，取 label_validation.required_prefixes
2. 若 label 不以任一 prefix 开头 → valid=False, reason="missing required prefix"
3. 若 color_required=True 且 label 无 color → valid=False, reason="color required"
4. 否则 valid=True

### 3.3 ProjectStructureEngine（#110）

```python
class ProjectStructureEngine:
    def register(self, structure: ProjectStructure) -> ProjectStructure: ...
    def get(self, struct_id: str) -> ProjectStructure: ...
    def list(self, name: str | None = None) -> list[ProjectStructure]: ...
    def update(self, struct_id: str, updates: dict[str, Any]) -> ProjectStructure: ...
    def delete(self, struct_id: str) -> bool: ...
    def render_template(self, struct_id: str) -> dict[str, Any]: ...
    """返回结构 JSON：{name, layers, components}"""
    def validate_project(self, struct_id: str, project_components: list[dict[str, Any]]) -> dict[str, Any]: ...
    """校验项目组件是否符合模板：required 组件必须存在；layer/type 必须合法"""
```

**validate_project 流程**：
1. 取 structure，遍历 components 中 required=True 的项
2. 对每个 required 组件，检查 project_components 中是否存在同 (layer, name) 的项
3. 缺失 → missing 列表
4. 多余 → extra 列表
5. 返回 {valid, missing, extra}

### 3.4 单例与持久化

- 3 个引擎均用**双重检查锁单例**
- 内存态为主，各 200 条上限（aip assist 200 results）

---

## 4. API 设计

文件：`aos_api/routers/aip_assist.py`（新增）

### 4.1 #107 AIP Assist

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/aip-assist/requests` | 注册辅助请求 |
| GET | `/v1/aip-assist/requests` | 列表 |
| GET | `/v1/aip-assist/requests/{req_id}` | 单条 |
| PUT | `/v1/aip-assist/requests/{req_id}` | 更新 |
| DELETE | `/v1/aip-assist/requests/{req_id}` | 删除 |
| POST | `/v1/aip-assist/requests/{req_id}/run` | 执行辅助 |
| GET | `/v1/aip-assist/results` | 结果列表 |

### 4.2 #108 repoSettings.json

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/aip-assist/repo-settings` | 注册配置 |
| GET | `/v1/aip-assist/repo-settings` | 列表 |
| GET | `/v1/aip-assist/repo-settings/{settings_id}` | 单条 |
| PUT | `/v1/aip-assist/repo-settings/{settings_id}` | 更新 |
| DELETE | `/v1/aip-assist/repo-settings/{settings_id}` | 删除 |
| POST | `/v1/aip-assist/repo-settings/{settings_id}/validate-label` | 标签验证 |
| POST | `/v1/aip-assist/repo-settings/{settings_id}/render-pr-template` | 渲染 PR 模板 |

### 4.3 #110 推荐项目结构

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/aip-assist/project-structures` | 注册结构 |
| GET | `/v1/aip-assist/project-structures` | 列表 |
| GET | `/v1/aip-assist/project-structures/{struct_id}` | 单条 |
| PUT | `/v1/aip-assist/project-structures/{struct_id}` | 更新 |
| DELETE | `/v1/aip-assist/project-structures/{struct_id}` | 删除 |
| GET | `/v1/aip-assist/project-structures/{struct_id}/render` | 渲染模板 |
| POST | `/v1/aip-assist/project-structures/{struct_id}/validate-project` | 校验项目 |

---

## 5. 集成点

### 5.1 main.py（最小更改）

```python
from aos_api.routers import (..., aip_assist, ...)
application.include_router(aip_assist.router)
```

---

## 6. 测试计划

文件：`tests/test_aip_assist.py`（新增，约 42 个用例）

### 6.1 AIPAssistEngine（14）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 缺 code | MISSING_CODE |
| 3 | register 未知 kind | INVALID_KIND |
| 4 | register 未知 language | INVALID_LANGUAGE |
| 5 | get 未找到 | NOT_FOUND |
| 6 | list 默认 | 列表 |
| 7 | list 按 kind 过滤 | 仅匹配 |
| 8 | list 按 status 过滤 | 仅匹配 |
| 9 | update | 修改后返回新值 |
| 10 | delete | 删除成功 |
| 11 | run explain | status=completed, result.summary 含行数 |
| 12 | run vulnerability | 返回 vulnerabilities 列表 |
| 13 | run translate | 返回 translated 字符串 |
| 14 | run complete | 返回 suggestion |
| 15 | run 重复 | ALREADY_COMPLETED |
| 16 | list_results 200 条上限 | 旧记录淘汰 |

### 6.2 RepoSettingsEngine（13）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 缺 repo_id | MISSING_REPO |
| 3 | get 未找到 | NOT_FOUND |
| 4 | get_by_repo | 返回匹配 |
| 5 | list 默认 | 列表 |
| 6 | list 按 repo_id 过滤 | 仅匹配 |
| 7 | update | 修改后返回新值 |
| 8 | delete | 删除成功 |
| 9 | validate_label 通过 | valid=True |
| 10 | validate_label 缺前缀 | valid=False, reason 含 prefix |
| 11 | validate_label 缺颜色 | valid=False, reason 含 color |
| 12 | render_pr_template | 占位符替换成功 |
| 13 | update 未知 rule_kind | INVALID_RULE_KIND |

### 6.3 ProjectStructureEngine（13）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 缺 name | MISSING_NAME |
| 3 | register 未知 layer | INVALID_LAYER |
| 4 | register 未知 component type | INVALID_COMPONENT_TYPE |
| 5 | get 未找到 | NOT_FOUND |
| 6 | list 默认 | 列表 |
| 7 | list 按 name 过滤 | 仅匹配 |
| 8 | update | 修改后返回新值 |
| 9 | delete | 删除成功 |
| 10 | render_template | 返回 JSON 含 layers + components |
| 11 | validate_project 通过 | valid=True |
| 12 | validate_project 缺 required | missing 非空 |
| 13 | validate_project 多余组件 | extra 非空 |

### 6.4 单例（3）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | assist 单例 | 同一实例 |
| 2 | settings 单例 | 同一实例 |
| 3 | structure 单例 | 同一实例 |

---

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| AIP run 异常 | try/except 捕获 → status=error |
| 仓库配置误删 | 仅记录删除，不真删文件 |
| 项目结构模板与实际项目不符 | validate_project 返回 missing/extra 列表，由调用方决策 |
| 重复 run | ALREADY_COMPLETED 错误码拦截 |
| 标签规则空 | label_validation 为空时 validate_label 直接 valid=True |

---

## 8. 交付物清单

| 路径 | 状态 | 说明 |
| --- | --- | --- |
| `docs/palantier/20_tech/220tech_w2-ae-aip-assist.md` | ✅ 本文件 | 微规约 |
| `aos_api/aip_assist.py` | ⬜ 待编码 | 3 引擎 |
| `aos_api/routers/aip_assist.py` | ⬜ 待编码 | ~21 端点 |
| `tests/test_aip_assist.py` | ⬜ 待编码 | ~42 用例 |
| `aos_api/main.py` | ⬜ +2 行 | import + include_router |

---

*v1.0 · w2-ae*

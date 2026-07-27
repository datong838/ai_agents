# 220tech · W2-AC · 代码仓库与 PR 工作流组（#101 / #102 / #103）

> **版本**：v1.0 · 2026-07-22
> **状态**：✅ 方案定稿 · 可编码
> **对齐**：
> - 差距分析 [220w](./220w-与目标系统差距对照分析.md) §11 #101/#102/#103
> - 上游 W2-3 Ontology 输出 · wave_ext 简易 code-repos 列表
> **范围**：W2-AC 收口代码协作三件 — Branch（分支管理）/ PullRequest（PR 工作流）/ Transform Preview（变换预览）
> **不替换底层**：本组是代码协作层，不重写 wave_ext code-repos 列表

---

## 0. 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文回答 | 文档与代码注释均中文 |
| 先方案后编码 | 本文先定稿，再写引擎/路由/测试 |
| 最小更改 | 仅新增 `aos_api/code_collaboration.py` + `aos_api/routers/code_collaboration.py` + `tests/test_code_collaboration.py`；`main.py` 加 2 行 |
| 不影响已有功能 | 三引擎纯新增；wave_ext code-repos 列表保留 |
| 自测验证 | 单测全绿 + 全量回归 + 方案对照 |

---

## 1. 背景与边界

### 1.1 现状

| 能力 | 现状 | 缺口 |
| --- | --- | --- |
| 分支管理 | 无 | 🔴 缺 |
| PR 工作流 | 无 | 🔴 缺 |
| 变换预览 | 无 | 🔴 缺 |

### 1.2 边界

- ✅ 本组做：
  - #101 Branch：create/merge/delete/rebase + 保护分支 + 状态机 open/merged/deleted
  - #102 PullRequest：create/review/approve/reject/merge + CI 检查状态 + 5 态状态机
  - #103 Transform Preview：register_preview/run_preview/get_result + 样本数据执行
- ❌ 本组不做：
  - 实际 Git 操作（属底层 VCS）
  - CI/CD pipeline 执行（属 Build 引擎）
  - 代码 Diff 解析

---

## 2. 数据模型

### 2.1 #101 Branch

```python
class Branch(BaseModel):
    """代码分支。"""
    id: str
    repo_id: str
    name: str
    base_branch: str = "main"
    head_commit: str = ""
    protected: bool = False
    status: str = "open"          # open / merged / deleted
    created_at: float = 0.0
    merged_at: float = 0.0


class BranchMergeResult(BaseModel):
    """分支合并结果。"""
    source_branch: str
    target_branch: str
    strategy: str                 # merge / rebase / squash
    success: bool
    new_commit: str = ""
    conflicts: list[str] = []
    merged_at: float = 0.0


_VALID_BRANCH_STATUSES = {"open", "merged", "deleted"}
_VALID_MERGE_STRATEGIES = {"merge", "rebase", "squash"}
```

### 2.2 #102 PullRequest

```python
class PullRequest(BaseModel):
    """Pull Request。"""
    id: str
    repo_id: str
    title: str
    description: str = ""
    source_branch: str
    target_branch: str
    author: str
    reviewers: list[str] = []
    status: str = "open"          # open / reviewing / approved / rejected / merged / closed
    ci_status: str = "pending"    # pending / running / passed / failed
    commits: list[str] = []
    created_at: float = 0.0
    updated_at: float = 0.0
    merged_at: float = 0.0


_VALID_PR_STATUSES = {"open", "reviewing", "approved", "rejected", "merged", "closed"}
_VALID_CI_STATUSES = {"pending", "running", "passed", "failed"}
_VALID_PR_TRANSITIONS = {
    "open": {"reviewing", "closed"},
    "reviewing": {"approved", "rejected", "open", "closed"},
    "approved": {"merged", "open"},
    "rejected": {"open", "closed"},
    "merged": set(),
    "closed": set(),
}
```

### 2.3 #103 Transform Preview

```python
class TransformPreview(BaseModel):
    """变换预览定义。"""
    id: str
    name: str
    repo_id: str = ""
    branch: str = "main"
    transform_code: str           # Python/SQL 代码片段
    language: str = "python"      # python / sql
    input_schema: dict[str, str] = {}  # 列名 -> 类型
    sample_rows: list[dict[str, Any]] = []
    created_at: float = 0.0


class PreviewResult(BaseModel):
    """变换预览结果。"""
    id: str
    preview_id: str
    status: str                   # success / error / timeout
    output_rows: list[dict[str, Any]] = []
    output_schema: dict[str, str] = {}
    error_message: str = ""
    row_count: int = 0
    executed_at: float = 0.0


_VALID_PREVIEW_LANGUAGES = {"python", "sql"}
_VALID_PREVIEW_STATUSES = {"success", "error", "timeout"}
```

---

## 3. 引擎设计

文件：`aos_api/code_collaboration.py`（新增，3 个引擎）

### 3.1 BranchEngine（#101）

```python
class BranchEngine:
    def register(self, branch: Branch) -> Branch: ...
    def get(self, branch_id: str) -> Branch: ...
    def get_by_name(self, repo_id: str, name: str) -> Branch | None: ...
    def list(self, repo_id: str | None = None, status: str | None = None) -> list[Branch]: ...
    def update(self, branch_id: str, updates: dict[str, Any]) -> Branch: ...
    def delete(self, branch_id: str) -> bool: ...
    def merge(self, source_id: str, target_name: str, strategy: str = "merge") -> BranchMergeResult: ...
    """合并分支：检查 source 状态→检查 target 存在→推进 source merged"""
    def protect(self, branch_id: str, protected: bool = True) -> Branch: ...
```

**merge 流程**：
1. 取 source branch，校验 status=open
2. 检查 target branch 存在（同 repo_id）
3. 生成 new_commit（uuid）
4. source.status=merged, source.merged_at=now
5. 返回 BranchMergeResult

### 3.2 PullRequestEngine（#102）

```python
class PullRequestEngine:
    def register(self, pr: PullRequest) -> PullRequest: ...
    def get(self, pr_id: str) -> PullRequest: ...
    def list(self, repo_id: str | None = None, status: str | None = None, author: str | None = None) -> list[PullRequest]: ...
    def update(self, pr_id: str, updates: dict[str, Any]) -> PullRequest: ...
    def transition(self, pr_id: str, new_status: str) -> PullRequest: ...
    """状态转换：校验 _VALID_PR_TRANSITIONS"""
    def add_reviewer(self, pr_id: str, reviewer: str) -> PullRequest: ...
    def set_ci_status(self, pr_id: str, ci_status: str) -> PullRequest: ...
    def merge(self, pr_id: str) -> PullRequest: ...
    """合并 PR：需 status=approved + ci_status=passed"""
```

### 3.3 TransformPreviewEngine（#103）

```python
class TransformPreviewEngine:
    def register(self, preview: TransformPreview) -> TransformPreview: ...
    def get(self, preview_id: str) -> TransformPreview: ...
    def list(self, repo_id: str | None = None, language: str | None = None) -> list[TransformPreview]: ...
    def update(self, preview_id: str, updates: dict[str, Any]) -> TransformPreview: ...
    def delete(self, preview_id: str) -> bool: ...
    def run(self, preview_id: str) -> PreviewResult: ...
    """执行预览：对 sample_rows 应用 transform_code"""
    def list_results(self, preview_id: str | None = None, limit: int = 50) -> list[PreviewResult]: ...
```

**run 流程**：
1. 取 preview，取 sample_rows
2. python：exec transform_code 中的 `transform(rows)` 函数
3. sql：简化为直接返回 sample_rows（无实际 SQL 引擎）
4. 捕获异常 → status=error
5. 200 条 result 上限

### 3.4 单例与持久化

- 3 个引擎均用**双重检查锁单例**
- 内存态为主，各 200 条上限

---

## 4. API 设计

文件：`aos_api/routers/code_collaboration.py`（新增）

### 4.1 #101 Branch

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/code-collaboration/branches` | 注册分支 |
| GET | `/v1/code-collaboration/branches` | 列表 |
| GET | `/v1/code-collaboration/branches/{branch_id}` | 单条 |
| PUT | `/v1/code-collaboration/branches/{branch_id}` | 更新 |
| DELETE | `/v1/code-collaboration/branches/{branch_id}` | 删除 |
| POST | `/v1/code-collaboration/branches/{branch_id}/merge` | 合并 |
| POST | `/v1/code-collaboration/branches/{branch_id}/protect` | 保护/取消 |

### 4.2 #102 PullRequest

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/code-collaboration/pull-requests` | 注册 PR |
| GET | `/v1/code-collaboration/pull-requests` | 列表 |
| GET | `/v1/code-collaboration/pull-requests/{pr_id}` | 单条 |
| PUT | `/v1/code-collaboration/pull-requests/{pr_id}` | 更新 |
| POST | `/v1/code-collaboration/pull-requests/{pr_id}/transition` | 状态转换 |
| POST | `/v1/code-collaboration/pull-requests/{pr_id}/reviewers` | 添加审查者 |
| POST | `/v1/code-collaboration/pull-requests/{pr_id}/ci-status` | 设置 CI 状态 |
| POST | `/v1/code-collaboration/pull-requests/{pr_id}/merge` | 合并 PR |

### 4.3 #103 Transform Preview

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/code-collaboration/previews` | 注册预览 |
| GET | `/v1/code-collaboration/previews` | 列表 |
| GET | `/v1/code-collaboration/previews/{preview_id}` | 单条 |
| PUT | `/v1/code-collaboration/previews/{preview_id}` | 更新 |
| DELETE | `/v1/code-collaboration/previews/{preview_id}` | 删除 |
| POST | `/v1/code-collaboration/previews/{preview_id}/run` | 执行预览 |
| GET | `/v1/code-collaboration/preview-results` | 结果列表 |

---

## 5. 集成点

### 5.1 main.py（最小更改）

```python
from aos_api.routers import (..., code_collaboration, ...)
application.include_router(code_collaboration.router)
```

---

## 6. 测试计划

文件：`tests/test_code_collaboration.py`（新增，约 42 个用例）

### 6.1 BranchEngine（14）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 缺 name | MISSING_NAME |
| 3 | get 未找到 | NOT_FOUND |
| 4 | get_by_name | 返回匹配 |
| 5 | list 默认 | 列表 |
| 6 | list 按 repo_id 过滤 | 仅匹配 |
| 7 | list 按 status 过滤 | 仅匹配 |
| 8 | update | 修改后返回新值 |
| 9 | delete | 删除成功 |
| 10 | merge 成功 | source.status=merged |
| 11 | merge 已合并分支 | ALREADY_MERGED |
| 12 | merge target 不存在 | TARGET_NOT_FOUND |
| 13 | protect | protected=True |
| 14 | merge rebase 策略 | strategy=rebase |

### 6.2 PullRequestEngine（15）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 缺 title | MISSING_TITLE |
| 3 | get 未找到 | NOT_FOUND |
| 4 | list 默认 | 列表 |
| 5 | list 按 repo_id 过滤 | 仅匹配 |
| 6 | list 按 status 过滤 | 仅匹配 |
| 7 | list 按 author 过滤 | 仅匹配 |
| 8 | update | 修改后返回新值 |
| 9 | transition open→reviewing | 成功 |
| 10 | transition 非法转换 | INVALID_TRANSITION |
| 11 | add_reviewer | reviewers 增长 |
| 12 | set_ci_status | ci_status 更新 |
| 13 | merge 成功 | status=merged（需 approved+ci passed） |
| 14 | merge 未 approved | MERGE_NOT_ALLOWED |
| 15 | merge ci failed | CI_NOT_PASSED |

### 6.3 TransformPreviewEngine（13）

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
| 9 | run python 成功 | status=success |
| 10 | run python 异常 | status=error |
| 11 | run sql | status=success（返回原 rows） |
| 12 | list_results | 列表 |
| 13 | 200 条 result 上限 | 旧记录淘汰 |

---

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 分支误合并 | status 白名单 + merge 前检查 open |
| PR 非法状态跳转 | _VALID_PR_TRANSITIONS 白名单 |
| PR 合并条件不足 | merge 需 approved + ci_status=passed |
| 预览代码执行异常 | try/except 捕获 → status=error |
| 预览代码注入 | 仅内存执行 sample_rows，不访问文件系统 |

---

## 8. 交付物清单

| 路径 | 状态 | 说明 |
| --- | --- | --- |
| `docs/palantier/20_tech/220tech_w2-ac-code-collaboration.md` | ✅ 本文件 | 微规约 |
| `aos_api/code_collaboration.py` | ⬜ 待编码 | 3 引擎 |
| `aos_api/routers/code_collaboration.py` | ⬜ 待编码 | ~22 端点 |
| `tests/test_code_collaboration.py` | ⬜ 待编码 | ~42 用例 |
| `aos_api/main.py` | ⬜ +2 行 | import + include_router |

---

*v1.0 · w2-ac*

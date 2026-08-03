# Checkpoint 与回滚设计 — 分段确认 + 版本追溯

> 创建时间：2026-07-28
> 状态：方案设计（先方案后编码）
> 关联：`00-总览-从静态文档到可编排技能链.md` §六 · `01-电商FDE技能链设计.md` §二
> 对接：AIP 层 `aip_checkpoint_store.py`（新增）

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 先方案后编码 | 本文档为方案层 |
| 最小更改 | Checkpoint 存储为新增模块，不影响现有数据接入流程 |
| 不影响现有功能 | 失败回滚不影响其他正在运行的任务 |
| 自测验证 | 每个回滚场景需有对应的自动化测试 |

---

## 一、设计目标

### 1.1 问题诊断

当前 FDE 数据接入流程（静态文档版）的痛点：

| 痛点 | 影响 |
|------|------|
| 中途断了从头开始 | 接入淘宝到第 5 步失败，要从第 1 步重新理解需求 |
| 无法回滚到指定步 | 字段映射错了，必须重新跑整个流程 |
| 没有版本追溯 | 改了认证配置后无法回到上一版本 |
| 用户无法介入暂停 | 接入流程开始后无法暂停确认 |

### 1.2 目标

| 目标 | 验收标准 |
|------|---------|
| 每步保存 Checkpoint | 6 步完成后有 6 个检查点 |
| 支持任意步回滚 | 字段映射失败可回滚到 CP3（API 探索） |
| 支持暂停/恢复 | 用户可主动暂停，恢复后从最近 CP 继续 |
| 版本追溯 | 每次修改认证配置生成新版本，可查看历史 |
| 失败自动回滚 | 技能 5 失败自动回滚到 CP4 |

---

## 二、Checkpoint 数据模型

### 2.1 核心结构

```python
# aip_checkpoint_store.py（新增）

class Checkpoint(BaseModel):
    """检查点。"""
    id: str                          # 如 "cp-{task_id}-3"
    task_id: str                      # FDE Task ID
    skill_id: str                     # 如 "fde-skill-3-api-explore"
    step_index: int                   # 1-6
    status: str                      # "active" | "superseded" | "rolled_back"

    # 上下文快照（指针引用，不存大对象）
    context_snapshot: ContextSnapshot

    # 产物引用
    artifacts: list[ArtifactRef]      # 如 mapping_diff_id, validation_report_id

    # 元数据
    created_at: float
    created_by: str                  # "system" | "user:{user_id}"
    can_rollback_to: bool = True     # 是否可作为回滚目标
    parent_checkpoint_id: str | None  # 上一版本的 CP ID（版本追溯）

    # 失败信息（仅当此 CP 是失败时）
    failure_info: FailureInfo | None = None


class ContextSnapshot(BaseModel):
    """上下文快照（指针引用，不存大对象）。"""
    working_memory_refs: dict[str, str]   # {field_name: working_memory_id}
    episodic_memory_refs: list[str]        # 写入的 Episodic Memory ID
    persisted_refs: dict[str, str]         # {resource_type: persisted_id}，如 {"auth_config": "ac-xxx"}


class ArtifactRef(BaseModel):
    """产物引用。"""
    artifact_id: str
    artifact_type: str               # "diff" | "report" | "config" | "snapshot"
    title: str


class FailureInfo(BaseModel):
    """失败信息。"""
    error_code: str
    error_message: str
    failed_at: float
    retry_count: int
    stack_trace: str | None = None
```

### 2.2 Checkpoint 链表结构

每个 Task 的 Checkpoint 形成链表，支持版本追溯：

```
Task: fde-task-001（接入淘宝）

CP1-v1 ─→ CP2-v1 ─→ CP3-v1 ─→ CP4-v1（失败：coverage < 0.8）
                                      │
                                      └─→ rollback → CP3-v1（重新探索 API）
                                                       │
                                                       └─→ CP3-v2 ─→ CP4-v2（成功）

版本追溯：
- CP3-v1.parent_checkpoint_id = CP2-v1.id
- CP3-v2.parent_checkpoint_id = CP2-v1.id（同一父级）
- CP3-v2 是 CP3-v1 的"修正版"
```

### 2.3 与 AIP Task 的关系

FDE 的 Checkpoint 是 AIP 层 `Task.checkpoints` 的具体实例：

```python
# AIP 层 Task 模型（已存在）
class Task(BaseModel):
    id: str
    type: str  # "data_ingestion" 表示 FDE 任务
    status: str  # pending → planning → executing → reviewing → completed / failed / paused
    checkpoints: list[Checkpoint]  # ← FDE 写入的 6 个 CP

# FDE 层创建 CP 时调用 AIP 层的 CheckpointStore
class FDECheckpointManager:
    def __init__(self, aip_checkpoint_store: CheckpointStore):
        self._store = aip_checkpoint_store

    async def save_checkpoint(self, task: Task, step_index: int, skill_result: SkillResult) -> Checkpoint:
        cp = Checkpoint(
            id=f"cp-{task.id}-{step_index}",
            task_id=task.id,
            skill_id=f"fde-skill-{step_index}",
            step_index=step_index,
            context_snapshot=self._snapshot_context(skill_result),
            artifacts=skill_result.artifacts,
            created_at=time.time(),
            created_by="system",
        )
        return await self._store.save(cp)
```

---

## 三、分段确认机制

### 3.1 必须用户确认的检查点

并非所有 CP 都需要用户确认，仅以下场景：

| 检查点 | 触发确认的条件 | 确认内容 |
|-------|--------------|---------|
| CP1 | 缺失必填参数 | 补全参数 |
| CP2 | 认证配置写入前 | credentials 是否正确 |
| CP4 | 映射置信度 < 0.8 | 待确认的映射规则 |
| CP5 | 首次同步前 | 同步策略是否合理 |
| CP6 | 数据质量 < 0.7 | 是否接受当前数据质量 |

### 3.2 自动放行的检查点

| 检查点 | 放行条件 |
|-------|---------|
| CP1 | 必填参数齐全 + confidence ≥ 0.8 |
| CP2 | 认证测试通过 + 非敏感环境 |
| CP3 | 必需 API 全部可用 |
| CP4 | coverage ≥ 0.8 + avg_confidence ≥ 0.7 |
| CP5 | 首次同步成功 + 记录数符合预期 |
| CP6 | 数据质量评分 ≥ 0.7 |

### 3.3 暂停/恢复流程

```
技能4 字段映射执行中
    │
    ▼
置信度 < 0.8 → 暂停 Task（status="paused"）
    │
    ▼
保存 CP4（status="paused"，带 failure_info）
    │
    ▼
通知用户："字段映射置信度 0.65，请确认以下规则"
    │
    ▼
用户介入（前端 Draft Inbox 展示 Diff）
    │
    ├─ 用户批准 → 恢复 Task，从 CP4 继续到技能5
    ├─ 用户编辑 → 生成 CP4-v2，从 CP4-v2 继续到技能5
    └─ 用户拒绝 → 终止 Task，回滚到 CP3
```

### 3.4 用户介入 API

```python
# 新增端点（不修改现有端点）

POST /v1/fde/tasks/{task_id}/checkpoints/{cp_id}/confirm
# 用户确认检查点，恢复执行
Body: {
    "action": "approve" | "reject" | "edit",
    "edits": {...}  # 仅 action=edit 时
}

POST /v1/fde/tasks/{task_id}/pause
# 用户主动暂停

POST /v1/fde/tasks/{task_id}/resume
# 用户主动恢复（从最近 active CP 继续）

POST /v1/fde/tasks/{task_id}/rollback
# 用户主动回滚
Body: {
    "to_checkpoint_id": "cp-{task_id}-3",
    "reason": "字段映射错误"
}

GET /v1/fde/tasks/{task_id}/checkpoints
# 查看所有检查点（含版本历史）
```

---

## 四、回滚策略

### 4.1 自动回滚触发条件

| 触发条件 | 自动回滚到 | 处理 |
|---------|----------|------|
| 技能2 认证失败（重试3次） | CP1 | 重新理解需求（可能用户输错参数） |
| 技能3 API 不可达（重试3次） | CP2 | 重新配置认证 |
| 技能4 覆盖率 < 0.5 | CP3 | 重新探索 API，补充字段 |
| 技能4 置信度 < 0.5 | 暂停 | 不回滚，等待用户介入 |
| 技能5 同步首跑失败（重试3次） | CP4 | 重新生成映射方案 |
| 技能5 Ontology 物化失败 | CP4 | 检查映射规则 |
| 技能6 Schema 漂移 | CP5 | 调整同步配置 |

### 4.2 回滚操作清单

回滚到指定 CP 时，需要清理该 CP 之后产生的资源：

```python
# aip_fde_rollback.py

class FDERollbackManager:
    """回滚管理器。"""

    ROLLBACK_ACTIONS = {
        # 回滚到 CP6：清理验证报告（无副作用）
        6: ["delete_artifact:validation_report"],

        # 回滚到 CP5：删除 Pipeline + Ontology 物化结果
        5: [
            "delete_pipeline",
            "delete_ontology_objects:materialized",
            "delete_artifact:mapping_diff",
            "delete_artifact:sync_config",
        ],

        # 回滚到 CP4：清理映射规则（OKF Funnel 中的）
        4: [
            "delete_funnel_rules",
            "delete_artifact:mapping_diff",
            "delete_episodic:mapping_experience",
        ],

        # 回滚到 CP3：清理 API Schema 缓存
        3: [
            "delete_working_memory:api_schema",
            "delete_episodic:api_schema_experience",
        ],

        # 回滚到 CP2：清理认证配置（敏感，需用户确认）
        2: [
            "delete_auth_config",  # 调用现有 Writeback 回滚
            "delete_persisted:credentials",
        ],

        # 回滚到 CP1：清理对话理解结果（基本无副作用）
        1: ["delete_working_memory:dialog_result"],
    }

    async def rollback_to(self, task: Task, target_cp_id: str, reason: str) -> RollbackResult:
        target_cp = await self._store.get(target_cp_id)
        current_step = self._get_current_step(task)

        # 从当前步反向清理到目标步
        for step in range(current_step, target_cp.step_index, -1):
            await self._execute_cleanup(task, step)

        # 标记被回滚的 CP 为 "rolled_back"
        await self._mark_rolled_back(task, target_cp.step_index + 1, current_step)

        # 将 Task 状态恢复到目标 CP 的下一步
        task.status = "executing"
        task.current_step = target_cp.step_index
        task.context = await self._restore_context(target_cp)

        return RollbackResult(
            task_id=task.id,
            rolled_back_to=target_cp_id,
            cleaned_resources=[...],
            reason=reason,
        )

    async def _execute_cleanup(self, task: Task, step: int):
        """执行单步清理。"""
        actions = self.ROLLBACK_ACTIONS[step]
        for action in actions:
            await self._execute_action(task, action)
```

### 4.3 回滚的安全性约束

| 资源类型 | 是否可回滚 | 约束 |
|---------|----------|------|
| Working Memory | ✅ 直接删除 | 无副作用 |
| Episodic Memory | ⚠️ 标记 deprecated | 不删除（保留历史经验） |
| Ontology 对象 | ⚠️ 需用户确认 | 已物化的对象可能被其他业务使用 |
| Pipeline 配置 | ✅ 调用现有 DELETE API | Pipeline Builder 支持级联删除 |
| 认证配置 | ❌ 仅标记失效 | credentials 不删除（审计要求） |
| 同步数据 | ❌ 不回滚 | 已同步的数据不删除 |

### 4.4 部分回滚 vs 全量回滚

| 场景 | 类型 | 操作 |
|------|------|------|
| 字段映射错误 | 部分回滚 | 回滚到 CP3，重新探索 API |
| 整个接入方向错误 | 全量回滚 | 回滚到 CP1，重新理解需求 |
| 认证配置改了又改 | 版本切换 | 不回滚，切换到 CP2-v2 |
| 测试数据脏 | 不回滚 | 生成质量报告，标记 known_issues |

---

## 五、存储设计

### 5.1 存储分层

| 数据类型 | 存储位置 | TTL | 说明 |
|---------|---------|-----|------|
| Checkpoint 元数据 | Redis + PostgreSQL | Redis 7天 / PG 永久 | 元数据持久化，Redis 缓存 |
| ContextSnapshot 引用 | Redis | 7天 | Working Memory 指针 |
| Artifact 内容 | PostgreSQL（ArtifactStore） | 永久 | Diff/报告等大对象 |
| credentials | Vault（加密） | 永久 | 不存 Redis（敏感） |

### 5.2 Redis Key 设计

```
fde:task:{task_id}:checkpoints          # ZSET，score=step_index, member=cp_id
fde:task:{task_id}:cp:{cp_id}            # HASH，CP 元数据
fde:task:{task_id}:current_cp             # STRING，当前活跃 CP ID
fde:task:{task_id}:rollback_history       # LIST，回滚历史
```

### 5.3 PostgreSQL Schema

```sql
-- 新增表（不修改现有表）
CREATE TABLE fde_checkpoints (
    id VARCHAR(64) PRIMARY KEY,
    task_id VARCHAR(64) NOT NULL,
    skill_id VARCHAR(64) NOT NULL,
    step_index INT NOT NULL,
    status VARCHAR(32) NOT NULL,  -- active | superseded | rolled_back | paused

    context_snapshot JSONB NOT NULL,
    artifacts JSONB NOT NULL,

    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(64) NOT NULL,
    parent_checkpoint_id VARCHAR(64),

    failure_info JSONB,

    INDEX idx_task_step (task_id, step_index),
    INDEX idx_parent (parent_checkpoint_id)
);

CREATE TABLE fde_rollback_log (
    id VARCHAR(64) PRIMARY KEY,
    task_id VARCHAR(64) NOT NULL,
    from_step INT NOT NULL,
    to_step INT NOT NULL,
    reason TEXT,
    cleaned_resources JSONB,
    rolled_back_at TIMESTAMP DEFAULT NOW(),
    rolled_back_by VARCHAR(64) NOT NULL
);
```

---

## 六、版本追溯

### 6.1 版本链表

每次修改同一检查点会生成新版本，形成链表：

```
CP4-v1 (coverage=0.65, status=superseded)
  │
  └─→ CP4-v2 (coverage=0.78, status=superseded)
        │
        └─→ CP4-v3 (coverage=0.85, status=active)

查询版本历史：
GET /v1/fde/tasks/{task_id}/checkpoints/cp-xxx-4/versions
→ [CP4-v1, CP4-v2, CP4-v3]
```

### 6.2 版本切换

```python
POST /v1/fde/tasks/{task_id}/checkpoints/cp-xxx-4/switch
Body: { "to_version": "v2" }

# 后端操作：
# 1. 将当前 active CP 标记为 superseded
# 2. 将目标版本标记为 active
# 3. 重新加载上下文
# 4. 从该 CP 继续执行
```

### 6.3 审计日志

所有 Checkpoint 操作（创建/确认/回滚/切换）记录到审计日志：

```python
# aip_audit_log.py（已有，复用）

audit_log.record(
    action="fde.checkpoint.rollback",
    actor=user_id,
    target=f"task:{task_id}/cp:{cp_id}",
    details={
        "from_step": 5,
        "to_step": 3,
        "reason": "字段映射覆盖率不足",
        "cleaned_resources": ["pipeline:p-xxx", "ontology:Order:mat-xxx"],
    }
)
```

---

## 七、失败恢复流程

### 7.1 自动失败恢复

```
技能5 同步配置执行
    │
    ▼
首次同步失败（重试3次）
    │
    ▼
1. 保存 CP5（status=failed, failure_info={error_code, ...}）
2. 自动触发回滚到 CP4
3. 清理 CP5 产生的资源（Pipeline, Ontology 物化结果）
4. 重新执行技能4（重新生成映射方案）
5. 重新执行技能5
    │
    ├─ 成功 → 保存 CP4-v2 + CP5-v2
    └─ 失败 → 标记 Task=failed，通知用户
```

### 7.2 用户主动恢复

```python
# 用户从前端 Draft Inbox 看到失败 Task
GET /v1/fde/tasks/{task_id}
→ {
    "status": "paused",
    "current_checkpoint": "cp-xxx-4",
    "pause_reason": "字段映射置信度 0.65，请确认",
    "pending_review_mappings": [...],
    "diff_view_url": "/v1/artifacts/{diff_id}"
}

# 用户选择"编辑并继续"
POST /v1/fde/tasks/{task_id}/checkpoints/cp-xxx-4/confirm
Body: {
    "action": "edit",
    "edits": {
        "mapping_rules": [
            {"source": "tid", "target": "order_id", "transform": "string", "confidence": 0.95}
        ]
    }
}

# 后端：
# 1. 应用用户编辑 → 生成 CP4-v2
# 2. 恢复 Task，从 CP4-v2 继续到技能5
```

---

## 八、与现有代码的对接

| 新增模块 | 对接的现有代码 | 改动方式 |
|---------|-------------|---------|
| `aip_checkpoint_store.py` | 无（全新） | Redis + PostgreSQL 实现 |
| `aip_fde_rollback.py` | Pipeline Builder（DELETE API） | 通过 HTTP 调用现有 DELETE |
| `aip_fde_rollback.py` | Ontology Manager（DELETE API） | 通过 HTTP 调用 |
| `aip_fde_rollback.py` | OKF Funnel（DELETE rules API） | 通过 HTTP 调用 |
| `aip_audit_log.py` | 已有审计日志 | 复用，新增 action 类型 |

**不修改的现有模块**：
- `pipeline_builder_engine.py` — 仅调用 DELETE API
- `ontology_action_engine.py` — 仅调用 DELETE API
- `okf_funnel_engine.py` — 仅调用 DELETE API
- `aip_drafts_engine.py` — 复用其状态机，不修改

---

## 九、测试方案

### 9.1 自动化测试用例

```python
# tests/test_fde_checkpoint.py

class TestFDECheckpoint:

    async def test_save_six_checkpoints(self, fde_orchestrator, mock_platform):
        """6 步全部完成后有 6 个 Checkpoint。"""
        task = create_test_task(platform="taobao")
        await fde_orchestrator.run_chain(task)

        cps = await checkpoint_store.list_by_task(task.id)
        assert len(cps) == 6
        assert all(cp.status == "active" for cp in cps)

    async def test_rollback_to_cp3(self, fde_orchestrator, mock_platform):
        """技能4 失败后自动回滚到 CP3。"""
        mock_platform.set_low_coverage_mapping()  # coverage=0.4

        task = create_test_task(platform="taobao")
        result = await fde_orchestrator.run_chain(task)

        # 验证回滚
        assert result.rolled_back_to == "cp-xxx-3"
        assert result.cleaned_resources includes "funnel_rules"

        # 验证版本
        cps = await checkpoint_store.list_by_task(task.id, step_index=3)
        assert len(cps) == 2  # CP3-v1 + CP3-v2

    async def test_user_pause_resume(self, fde_orchestrator):
        """用户主动暂停后恢复。"""
        task = create_test_task(platform="taobao")

        # 执行到技能4 后暂停
        await fde_orchestrator.run_until_step(task.id, step=4)
        await fde_orchestrator.pause(task.id)

        assert task.status == "paused"

        # 用户恢复
        await fde_orchestrator.resume(task.id)
        assert task.status == "executing"

    async def test_version_switch(self, fde_orchestrator, mock_platform):
        """版本切换功能。"""
        # 先执行完成
        task = create_test_task(platform="taobao")
        await fde_orchestrator.run_chain(task)

        # 切换 CP4 到 v1
        await fde_orchestrator.switch_checkpoint_version(
            task.id, step=4, version="v1"
        )

        # 验证 Task 上下文恢复
        assert task.context["mapping_rules"] == original_v1_rules
```

### 9.2 验收标准

- [ ] 6 步全部完成后有 6 个 active Checkpoint
- [ ] 技能4 失败（coverage < 0.5）自动回滚到 CP3
- [ ] 技能5 失败（重试3次）自动回滚到 CP4
- [ ] 用户可主动暂停/恢复
- [ ] 用户可编辑低置信度映射，生成新版本 CP
- [ ] 版本切换功能正常，可查看历史版本
- [ ] 回滚清理的资源符合 §四.3 安全约束
- [ ] 审计日志记录所有 CP 操作
- [ ] `pytest tests/test_fde_checkpoint.py` 全部通过

---

## 十、新增模块清单

| 模块 | 路径 | 职责 |
|------|------|------|
| `aip_checkpoint_store.py` | `aos-platform-w4/services/aos-api/aos_api/` | Checkpoint 存储（Redis + PG） |
| `aip_fde_rollback.py` | 同上 | 回滚管理器 |
| `aip_fde_checkpoint_api.py` | 同上 | HTTP API（pause/resume/rollback/switch） |
| `tests/test_fde_checkpoint.py` | `aos-platform-w4/services/aos-api/tests/` | 自动化测试 |

**新增 API 端点**：
- `POST /v1/fde/tasks/{id}/pause`
- `POST /v1/fde/tasks/{id}/resume`
- `POST /v1/fde/tasks/{id}/rollback`
- `POST /v1/fde/tasks/{id}/checkpoints/{cp_id}/confirm`
- `POST /v1/fde/tasks/{id}/checkpoints/{cp_id}/switch`
- `GET /v1/fde/tasks/{id}/checkpoints`

---

*本文档为方案设计层，实施前需用户确认。*
*关联文档：`00-总览-从静态文档到可编排技能链.md` · `01-电商FDE技能链设计.md` · `03-六层权限防线设计.md` · `04-Reflection自审节点设计.md`*

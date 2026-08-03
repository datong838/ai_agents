# 电商 FDE 技能链设计 — 6 步接入流程的技能拆解

> 创建时间：2026-07-28
> 状态：方案设计（先方案后编码）
> 关联：`00-总览-从静态文档到可编排技能链.md`（技能链架构）· `../11-AIP决策引擎升级方案/01-Plan-Mode与TAOR循环设计.md`
> 对接现有：Pipeline Builder · OKF Funnel · Ontology Manager · Writeback 事务

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 先方案后编码 | 本文档为方案层 |
| 最小更改 | 复用现有 Pipeline Builder / OKF Funnel / Ontology Manager 接口 |
| 不影响现有功能 | 技能链编排器为新增模块，不修改现有数据接入流程 |
| 自测验证 | 每个技能完成后跑端到端测试，详见 §六 |

---

## 一、设计目标

### 1.1 总览文档已定义的内容

`00-总览-从静态文档到可编排技能链.md` 已给出：
- 6 个技能的 TAOR 循环骨架（Think/Act/Reflect/Observe）
- 平台适配层基本配置
- 记忆复用思路
- Checkpoint 触发点

### 1.2 本文档补全的内容

| 主题 | 本文档章节 |
|------|----------|
| 技能链编排器（Skill Chain Orchestrator）整体架构 | §二 |
| 技能间数据传递契约（输入/输出 Schema） | §三 |
| 与 AIP 层 TAOR 循环控制器的对接 | §四 |
| 与现有工具层（Pipeline Builder 等）的对接 | §五 |
| 端到端测试方案 | §六 |
| 关键边界条件与失败处理 | §七 |

---

## 二、技能链编排器架构

### 2.1 整体结构

```
┌──────────────────────────────────────────────────────────────┐
│                  FDESkillChainOrchestrator                  │
│                                                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Plan Mode 入口                                      │    │
│  │  - 澄清问题 → 生成 6 步执行计划 → 用户确认            │    │
│  └────────────────────┬────────────────────────────────┘    │
│                       ▼                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  SkillChainRunner（顺序执行 + 失败分支）              │    │
│  │                                                     │    │
│  │  Skill1 → Skill2 → Skill3 → Skill4 → Skill5 → Skill6│    │
│  │     │       │       │       │       │       │      │    │
│  │     ▼       ▼       ▼       ▼       ▼       ▼      │    │
│  │   CP1     CP2     CP3     CP4     CP5     CP6      │    │
│  └────────────────────┬────────────────────────────────┘    │
│                       ▼                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  ContextBus（上下文总线）                            │    │
│  │  - Working Memory（指针引用，避免大对象传递）         │    │
│  │  - HandoffEnvelope（技能间结构化交接）                │    │
│  └────────────────────┬────────────────────────────────┘    │
│                       ▼                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  PermissionGate（六层权限防线，详见 03-六层权限防线）   │    │
│  └────────────────────┬────────────────────────────────┘    │
│                       ▼                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  MemoryBus（三层记忆总线，详见 04-Reflection §三）   │    │
│  │  - Semantic（RAG 检索平台 API 文档）                 │    │
│  │  - Episodic（检索历史接入会话经验）                   │    │
│  │  - Working（当前接入任务上下文）                     │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

### 2.2 与 AIP 层的关系

FDE 技能链是 AIP 层 TAOR 循环的"预置技能组"，不重复实现 TAOR 控制器，而是通过注册 SkillTemplate 给 AIP 的 `LogicEngine` 调用：

| AIP 层 | FDE 层 | 关系 |
|--------|--------|------|
| `TAORLoopController` | `FDESkillChainOrchestrator` | AIP 调用 FDE 注册的 SkillTemplate |
| `TaskStateMachine` | FDE Task（接入任务） | FDE Task 是 AIP Task 的一个 `type="data_ingestion"` |
| `Checkpoint` | FDE CP1~CP6 | FDE 自有 6 个检查点，AIP 检查点统一存储 |
| `PermissionGate` | FDE Action 风险矩阵 | FDE 注册自己的 `risk_level` 配置 |
| `Memory` | FDE 三层记忆 | FDE 写入 Episodic 的"映射经验"可被其他数字同事复用 |

### 2.3 SkillTemplate 注册

```python
# aip_fde_skills.py（新增模块）

FDE_SKILL_TEMPLATES = [
    SkillTemplate(
        id="fde-skill-1-dialog",
        name="FDE技能1-对话理解",
        category="data_ingestion",
        step_index=1,
        taor_spec=FDE_SKILL_1_DIALOG,  # 详见 00-总览 §三
        input_schema=FDE_SKILL_1_INPUT,  # 详见本文档 §三
        output_schema=FDE_SKILL_1_OUTPUT,
    ),
    SkillTemplate(
        id="fde-skill-2-auth",
        name="FDE技能2-认证配置",
        step_index=2,
        taor_spec=FDE_SKILL_2_AUTH,
        # ...
    ),
    # ... 技能 3-6
]

# 注册到 AIP LogicEngine
def register_fde_skills(logic_engine: LogicEngine):
    for template in FDE_SKILL_TEMPLATES:
        logic_engine.register_skill_template(template)
```

---

## 三、技能间数据传递契约

### 3.1 设计原则

**避免大对象在技能间传递**：采用 HandoffEnvelope 模式，传递的是引用（pointer），而非完整数据。

```python
# aip_fde_handoff.py

class HandoffEnvelope(BaseModel):
    """技能间交接信封。"""
    from_skill: str       # 如 "fde-skill-1-dialog"
    to_skill: str          # 如 "fde-skill-2-auth"
    task_id: str
    pointer_refs: dict[str, str]  # Working Memory 中的引用 ID
    summary: str           # 摘要（< 200 字）
    required_fields: list[str]  # 下游技能必须读取的字段
```

### 3.2 各技能输入/输出契约

#### 技能1：对话理解

```python
class FDE_SKILL_1_INPUT(BaseModel):
    user_input: str        # 用户原始输入
    context: dict = {}     # 上下文（如来自前序会话）

class FDE_SKILL_1_OUTPUT(BaseModel):
    platform: str                       # "taobao" | "pinduoduo" | ...
    merchant_id: str
    data_types: list[str]               # ["orders", "products", ...]
    sync_frequency: str                 # "realtime" | "hourly" | "daily"
    confidence: float
    missing_required: list[str]         # 缺失的必填参数
    understanding_artifact_id: str      # Working Memory 引用
```

#### 技能2：认证配置

```python
class FDE_SKILL_2_INPUT(BaseModel):
    platform: str                        # 来自技能1
    merchant_id: str
    credentials_ref: str                 # Working Memory 引用（不直接传值）

class FDE_SKILL_2_OUTPUT(BaseModel):
    auth_type: str                       # "hmac_sha256" | "oauth2" | ...
    auth_config_id: str                  # 认证配置 ID（持久化后的）
    connectivity_test_passed: bool
    token_expiry: int | None             # Token 过期时间戳（秒）
    failure_reason: str | None = None
```

#### 技能3：API 探索

```python
class FDE_SKILL_3_INPUT(BaseModel):
    platform: str
    auth_config_id: str
    data_types: list[str]                # 来自技能1

class FDE_SKILL_3_OUTPUT(BaseModel):
    discovered_apis: dict[str, APISpec]   # {"orders": APISpec, "products": APISpec, ...}
    required_apis_available: dict[str, bool]
    missing_apis: list[str]
    api_schema_ref: str                  # Episodic Memory 引用（可跨平台复用）
    rate_limit_info: RateLimit | None
```

#### 技能4：字段映射

```python
class FDE_SKILL_4_INPUT(BaseModel):
    platform: str
    source_schema_ref: str               # 技能3产出的 API Schema 引用
    target_ontology_id: str              # 统一 Ontology ID
    episodic_memory_hits: list[MappingExperience]  # 检索到的历史映射经验

class FDE_SKILL_4_OUTPUT(BaseModel):
    mapping_rules: list[MappingRule]     # [{source, target, transform, confidence}, ...]
    coverage: float                      # 映射覆盖率
    avg_confidence: float
    pending_review: list[MappingRule]    # 低置信度，待人工确认
    mapping_artifact_id: str             # Diff 视图产物 ID
    episodic_record_id: str               # 写入 Episodic 的经验 ID
```

#### 技能5：同步配置

```python
class FDE_SKILL_5_INPUT(BaseModel):
    platform: str
    auth_config_id: str
    mapping_artifact_id: str             # 技能4 产物
    data_types: list[str]
    sync_frequency: str

class FDE_SKILL_5_OUTPUT(BaseModel):
    pipeline_id: str                     # 创建的 Pipeline ID
    sync_config: SyncConfig
    first_sync_succeeded: bool
    first_sync_record_count: int
    ontology_materialized: bool          # 是否已物化到 Ontology
    failure_reason: str | None = None
```

#### 技能6：测试验证

```python
class FDE_SKILL_6_INPUT(BaseModel):
    pipeline_id: str
    ontology_object_types: list[str]     # 待验证的 OT 列表

class FDE_SKILL_6_OUTPUT(BaseModel):
    test_cases_passed: int
    test_cases_failed: int
    data_quality_score: float            # 0.0-1.0
    quality_issues: list[QualityIssue]
    validation_report_artifact_id: str   # 验证报告产物
    snapshot_artifact_id: str            # 接入配置快照（用于回滚）
```

### 3.3 数据流图

```
用户输入
  │
  ▼
[技能1] ──→ WorkingMemory(dialog_result)
  │           │
  │           └─→ EpisodicMemory.write(understanding_session)
  ▼
[技能2] ──→ WorkingMemory(auth_config)
  │           │
  │           └─→ PersistedStore(auth_credentials)  ← 加密存储
  ▼
[技能3] ──→ WorkingMemory(api_schema)
  │           │
  │           └─→ EpisodicMemory.write(api_schema_experience)  ← 跨平台复用
  ▼
[技能4] ──→ WorkingMemory(mapping_rules)
  │           │
  │           ├─→ EpisodicMemory.write(mapping_experience)  ← 跨平台复用
  │           └─→ ArtifactStore(mapping_diff)  ← Diff 视图
  ▼
[技能5] ──→ PersistedStore(pipeline_config)
  │           │
  │           └─→ OntologyMaterialize(objects)  ← 物化结果
  ▼
[技能6] ──→ ArtifactStore(validation_report)
              │
              └─→ EpisodicMemory.write(lessons_learned)
```

---

## 四、与 AIP 层 TAOR 循环控制器对接

### 4.1 调用契约

FDE 技能链不自己跑 TAOR 循环，而是把每个 SkillTemplate 注册给 AIP 的 `TAORLoopController`，由 AIP 统一调度：

```python
# AIP 层（aip_taor_loop.py）
class TAORLoopController:
    async def run_skill(self, skill_template: SkillTemplate, context: dict) -> SkillResult:
        # 1. Think
        plan = await self._think(skill_template.taor_spec.think, context)

        # 2. Act
        action_result = await self._act(skill_template.taor_spec.act, context, plan)

        # 3. Reflect（详见 04-Reflection 自审节点设计）
        reflection = await self._reflect(skill_template.taor_spec.reflect, action_result)
        if reflection.should_retry:
            return await self.run_skill(skill_template, reflection.updated_context)

        # 4. Observe
        await self._observe(skill_template.taor_spec.observe, action_result, context)

        # 5. Permission Gate（详见 03-六层权限防线）
        if action_result.requires_approval:
            await self._pause_for_approval(action_result)

        return SkillResult(...)


# FDE 层（aip_fde_orchestrator.py）
class FDESkillChainOrchestrator:
    def __init__(self, taor_controller: TAORLoopController):
        self._taor = taor_controller
        self._skills = {s.id: s for s in FDE_SKILL_TEMPLATES}

    async def run_chain(self, task: FDETask) -> FDEChainResult:
        context = task.initial_context

        for step_index in range(1, 7):
            skill = self._get_skill_by_step(step_index)

            # 执行单个技能
            skill_result = await self._taor.run_skill(skill, context)

            # 保存 Checkpoint（详见 02-Checkpoint 与回滚设计）
            await self._save_checkpoint(task, step_index, skill_result)

            # 构造 HandoffEnvelope 给下一技能
            context = self._build_handoff(skill, skill_result, context)

            # 失败处理
            if not skill_result.success:
                return await self._handle_failure(task, step_index, skill_result)

        return FDEChainResult(task_id=task.id, status="completed")
```

### 4.2 Plan Mode 集成

FDE 技能链的 Plan Mode 由 AIP 层的 `PlanGenerator` 统一负责，但 FDE 注册自己的 `ClarificationQuestions`：

```python
# FDE Plan Mode 配置
FDE_PLAN_CONFIG = {
    "task_type": "data_ingestion",
    "clarification_questions": [
        # 来自技能1 的澄清问题
        {"field": "platform", "question": "要接入哪个电商平台？", "required": True},
        {"field": "merchant_id", "question": "商家ID是什么？", "required": True},
        {"field": "api_credentials", "question": "API密钥是什么？", "required": True, "sensitive": True},
        {"field": "data_types", "question": "需要同步哪些数据？", "required": False, "default": ["orders", "products"]},
        {"field": "sync_frequency", "question": "同步频率？", "required": False, "default": "hourly"},
    ],
    "plan_template": """
        ## FDE 数据接入方案
        1. 理解需求：接入 {platform}，同步 {data_types}
        2. 配置认证：使用 {auth_type} 方式
        3. 探索 API：预计发现 {expected_api_count} 个接口
        4. 字段映射：将源 Schema 映射到统一 Ontology
        5. 同步配置：{sync_frequency} 频率，订单用 APPEND，商品用 SNAPSHOT
        6. 测试验证：拉取 100 条测试数据，验证端到端链路

        预计耗时：{estimated_minutes} 分钟
        预计 Token 消耗：{estimated_tokens}
    """,
    "confidence_threshold": 0.8,
}
```

---

## 五、与现有工具层对接

### 5.1 对接清单

| FDE 技能 | 调用的现有工具 | 端点 | 模式 |
|---------|-------------|------|------|
| 技能2 认证 | Writeback 事务 | `POST /v1/writeback/transactions` | Write Back |
| 技能3 API 探索 | Platform Adapter（新增） | `POST /v1/platforms/{platform}/explore-apis` | Side Effect |
| 技能4 字段映射 | OKF Funnel | `POST /v1/funnel/mappings/{spec_id}/rules` | Write Back |
| 技能5 同步配置 | Pipeline Builder | `POST /v1/pipelines`<br>`POST /v1/sync`<br>`POST /v1/funnel/run` | Write Back |
| 技能5 Ontology 物化 | Ontology Manager | `POST /v1/objects/{type}` | Write Back |
| 技能6 测试验证 | Dataset Preview | `GET /v1/datasets/{id}/preview` | Read |
| 技能6 数据健康 | Data Health | `GET /v1/health/checks` | Read |
| 技能6 Ontology 验证 | Ontology Manager | `GET /v1/objects/{type}` | Read |

### 5.2 工具调用封装

FDE 不直接调用工具，而是通过 AIP 的 `ToolExecutor` 调用，享受权限防线保护：

```python
# FDE 通过 ToolExecutor 调用 OKF Funnel
async def execute_field_mapping(input: FDE_SKILL_4_INPUT) -> FDE_SKILL_4_OUTPUT:
    tool_request = ToolRequest(
        tool_name="okf_funnel",
        endpoint="POST /v1/funnel/mappings/{spec_id}/rules",
        params={
            "spec_id": input.target_ontology_id,
            "rules": input.mapping_rules,
        },
        risk_level="medium",  # 配置变更为中风险
        requires_approval=False,  # 由 PermissionGate 自动判断
    )

    # 经过六层权限防线
    result = await tool_executor.execute(tool_request, task=task)

    return FDE_SKILL_4_OUTPUT(
        mapping_rules=result.mapping_rules,
        coverage=result.coverage,
        # ...
    )
```

### 5.3 与现有 Pipeline Builder 的契约

FDE 技能5 创建的 Pipeline 必须遵循现有 Pipeline Builder 的契约：

```python
# 复用现有 Pipeline Builder 端点（不修改）
# POST /v1/pipelines — 创建管道
# POST /v1/sync — 配置同步
# POST /v1/funnel/run — 执行物化

# FDE 的封装层（新增）
class FDESyncConfigurator:
    async def configure_pipeline(self, input: FDE_SKILL_5_INPUT) -> FDE_SKILL_5_OUTPUT:
        # 1. 创建 Pipeline
        pipeline = await self._pipeline_builder.create_pipeline(
            name=f"fde-{input.platform}-{input.merchant_id}",
            source=input.auth_config_id,
            target=f"ontology:{input.target_ontology_id}",
        )

        # 2. 配置同步策略
        sync_config = await self._pipeline_builder.configure_sync(
            pipeline_id=pipeline.id,
            strategy=self._recommend_strategy(input.data_types, input.sync_frequency),
        )

        # 3. 执行首次同步（小批量测试）
        first_run = await self._pipeline_builder.run_funnel(
            pipeline_id=pipeline.id,
            mode="test",  # 小批量模式
            limit=100,
        )

        return FDE_SKILL_5_OUTPUT(
            pipeline_id=pipeline.id,
            sync_config=sync_config,
            first_sync_succeeded=first_run.success,
            first_sync_record_count=first_run.record_count,
            ontology_materialized=first_run.materialized,
        )

    def _recommend_strategy(self, data_types: list[str], frequency: str) -> dict:
        """根据数据特性推荐同步策略。"""
        strategy = {}
        for dt in data_types:
            if dt == "orders":
                strategy[dt] = {"mode": "APPEND", "frequency": frequency}
            elif dt == "products":
                strategy[dt] = {"mode": "SNAPSHOT", "frequency": "daily"}
            elif dt == "customers":
                strategy[dt] = {"mode": "APPEND", "frequency": frequency}
            elif dt == "logistics":
                strategy[dt] = {"mode": "APPEND", "frequency": "realtime"}
        return strategy
```

---

## 六、端到端测试方案

### 6.1 测试用例矩阵

| 场景 | 输入 | 预期输出 | 验证点 |
|------|------|---------|--------|
| 正常接入 | "接入淘宝天猫" + 完整参数 | 6 步全部通过，生成验证报告 | Pipeline 创建成功，Ontology 物化 |
| 缺失必填参数 | "接入淘宝"（缺 merchant_id） | 技能1 暂停，询问用户 | Plan Mode 澄清问题触发 |
| 认证失败 | 错误的 app_secret | 技能2 失败，回滚到 CP1 | 重试 3 次后告警 |
| API 不可用 | 平台 API 维护中 | 技能3 报告 missing_apis | 不进入技能4，等待用户介入 |
| 映射覆盖率低 | 平台 Schema 与 Ontology 差异大 | 技能4 coverage < 0.8 | 标记 pending_review，暂停 |
| 同步首跑失败 | 网络抖动 | 技能5 自动重试 | 重试 3 次失败后回滚到 CP4 |
| 数据质量差 | null_rate > 5% | 技能6 报告 quality_issues | 生成质量报告，不阻断接入 |

### 6.2 自动化测试

```python
# tests/test_fde_skill_chain.py

class TestFDESkillChain:

    async def test_full_chain_happy_path(self, fde_orchestrator, mock_platform):
        """完整链路正常路径。"""
        task = FDETask(
            user_input="接入淘宝天猫",
            initial_context={
                "platform": "taobao",
                "merchant_id": "test_merchant",
                "api_credentials": {"app_key": "xxx", "app_secret": "xxx"},
                "data_types": ["orders", "products"],
                "sync_frequency": "hourly",
            }
        )

        result = await fde_orchestrator.run_chain(task)

        assert result.status == "completed"
        assert len(result.checkpoints) == 6
        assert result.validation_report_artifact_id is not None

    async def test_skill_2_auth_failure_rollback(self, fde_orchestrator, mock_platform):
        """认证失败时回滚到 CP1。"""
        mock_platform.set_auth_failure()  # 模拟认证失败

        task = FDETask(initial_context={...})
        result = await fde_orchestrator.run_chain(task)

        assert result.status == "failed"
        assert result.failure_step == 2
        assert result.rollback_to == "CP1"

    async def test_skill_4_low_confidence_pause(self, fde_orchestrator, mock_platform):
        """字段映射低置信度时暂停。"""
        mock_platform.set_low_confidence_mapping()  # 模拟映射置信度 0.5

        task = FDETask(initial_context={...})
        result = await fde_orchestrator.run_chain(task)

        assert result.status == "paused"
        assert result.pause_reason == "low_confidence"
        assert len(result.pending_review_mappings) > 0
```

### 6.3 验收标准

- [ ] 输入"接入淘宝天猫" + 完整参数 → 6 步全部通过
- [ ] 每步生成 Checkpoint，可独立回滚
- [ ] 技能1 缺失必填参数 → 触发 Plan Mode 澄清
- [ ] 技能2 认证失败 → 重试 3 次后告警
- [ ] 技能4 映射置信度 < 0.7 → 标记 pending_review 并暂停
- [ ] 技能5 同步首跑失败 → 回滚到 CP4 重新生成映射
- [ ] 技能6 数据质量差 → 生成报告但不阻断接入
- [ ] 换平台接入时从 Episodic Memory 检索历史经验
- [ ] `pytest tests/test_fde_skill_chain.py` 全部通过

---

## 七、边界条件与失败处理

### 7.1 失败处理矩阵

| 失败场景 | 失败步 | 处理策略 | 回滚到 |
|---------|-------|---------|--------|
| 必填参数缺失 | 技能1 | Plan Mode 澄清问题 | 不回滚，等待用户补充 |
| 认证失败 | 技能2 | 重试 3 次，每次间隔 5s | CP1（重新理解需求） |
| API 不可达 | 技能3 | 重试 3 次后告警 | CP2（重新配置认证） |
| 必需 API 缺失 | 技能3 | 报告 missing_apis，暂停 | 不回滚，等待用户介入 |
| 字段映射覆盖率不足 | 技能4 | 标记 pending_review | CP3（重新探索 API） |
| 映射置信度过低 | 技能4 | 暂停，等待人工确认 | 不回滚 |
| 同步首跑失败 | 技能5 | 重试 3 次后回滚 | CP4（重新生成映射） |
| Ontology 物化失败 | 技能5 | 检查 OT 定义 | CP4 |
| 数据质量差 | 技能6 | 生成报告，不阻断 | 不回滚 |
| Schema 漂移 | 技能6 | 报告 schema_drift | CP5（调整同步配置） |

### 7.2 超时策略

| 技能 | 超时阈值 | 超时处理 |
|------|---------|---------|
| 技能1 对话理解 | 30s | 取消 LLM 调用，提示用户重试 |
| 技能2 认证配置 | 60s | 超时视为认证失败 |
| 技能3 API 探索 | 120s | 超时视为 API 不可达 |
| 技能4 字段映射 | 90s | 超时使用 fallback 模板 |
| 技能5 同步配置 | 300s | 超时取消 Pipeline 创建 |
| 技能6 测试验证 | 180s | 超时生成不完整报告 |

### 7.3 重试策略

```python
RETRY_POLICY = {
    "skill_2_auth": {"max_retries": 3, "backoff_seconds": 5, "strategy": "fixed"},
    "skill_3_api_explore": {"max_retries": 3, "backoff_seconds": 10, "strategy": "exponential"},
    "skill_5_sync": {"max_retries": 3, "backoff_seconds": 30, "strategy": "exponential"},
    "skill_6_test": {"max_retries": 1, "backoff_seconds": 0, "strategy": "none"},
}
```

---

## 八、新增模块清单

| 模块 | 路径 | 职责 |
|------|------|------|
| `aip_fde_orchestrator.py` | `aos-platform-w4/services/aos-api/aos_api/` | FDE 技能链编排器 |
| `aip_fde_skills.py` | 同上 | 6 个 SkillTemplate 定义 |
| `aip_fde_handoff.py` | 同上 | HandoffEnvelope 数据契约 |
| `aip_fde_platform_adapters.py` | 同上 | 8 平台适配器（详见 10-FDE 技能编排总览） |
| `tests/test_fde_skill_chain.py` | `aos-platform-w4/services/aos-api/tests/` | 端到端测试 |

**不修改的现有模块**（最小更改原则）：
- `aip_logic_engine.py` — 仅通过 `register_skill_template` 接口注册
- `aip_taor_loop.py` — AIP 层 TAOR 控制器
- `pipeline_builder_engine.py` — 通过 HTTP API 调用
- `okf_funnel_engine.py` — 通过 HTTP API 调用
- `ontology_action_engine.py` — 通过 HTTP API 调用

---

*本文档为方案设计层，实施前需用户确认。*
*关联文档：`00-总览-从静态文档到可编排技能链.md` · `02-Checkpoint与回滚设计.md` · `03-六层权限防线设计.md` · `04-Reflection自审节点设计.md` · `10-FDE技能编排总览.md`*

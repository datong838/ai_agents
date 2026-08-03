# Plan Mode 与 TAOR 循环设计

> 创建时间：2026-07-28
> 状态：方案设计（先方案后编码）
> 关联代码：`aip_logic_engine.py::LogicEngine.execute_flow()` · `routers/phase3_aip_logic.py`
> 参考：Claude Code TAOR 循环 + Plan Mode 机制

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 先方案后编码 | 本文档为方案层 |
| 最小更改 | 保留现有 `execute_flow()` 方法签名，内部替换实现 |
| 不影响现有功能 | 旧接口 `POST /v1/aip/logic/execute` 保持兼容，新增 `POST /v1/aip/tasks` |
| 自测验证 | 新增 `test_aip_taor_loop.py` 测试 |

---

## 一、Plan Mode — 执行前生成方案

### 1.1 核心理念

参考 Claude Code 的 Plan Mode：

> 执行前生成方案，用户可编辑。Plan Mode 是只读分析模式，先探索再规划，**不做任何修改**。

当前 AIP 的 `execute_flow` 是"立即执行"模式 — 用户提交 blocks 后直接跑，没有"先出方案再确认"的环节。

### 1.2 Plan Mode 数据模型

```python
# aip_task_model.py

class TaskStep(BaseModel):
    """执行计划中的一个步骤。"""
    id: str = Field(default_factory=lambda: "step-" + uuid.uuid4().hex[:6])
    index: int  # 执行顺序
    title: str  # 步骤标题
    description: str  # 步骤描述
    action_type: str  # llm_call | tool_call | action_writeback | ontology_query | branch
    action_config: dict[str, Any]  # 动作配置（prompt / tool_name / action_id / query / condition）
    expected_output: str  # 预期输出描述
    risk_level: str = "low"  # low | medium | high | critical
    requires_approval: bool = False  # 是否需要人工确认
    depends_on: list[str] = Field(default_factory=list)  # 依赖的前置步骤 ID


class ExecutionPlan(BaseModel):
    """Plan Mode 的产物 — 执行计划。"""
    id: str = Field(default_factory=lambda: "plan-" + uuid.uuid4().hex[:8])
    task_id: str  # 关联的 Task ID
    steps: list[TaskStep]
    summary: str  # 计划摘要
    estimated_tokens: int = 0  # 预估 token 消耗
    estimated_duration: int = 0  # 预估耗时（秒）
    risk_assessment: str = "low"  # low | medium | high
    created_at: float = Field(default_factory=lambda: time.time())
    status: str = "draft"  # draft → approved → executing → completed
    approved_by: str = ""
    approved_at: float | None = None
```

### 1.3 Plan Mode 流程

```
用户输入任务描述
        │
        ▼
┌──────────────────────────────────┐
│  1. Clarification Gate           │  ← 澄清门：信息不足时反问
│  检查：必填参数是否齐全？           │
│  低置信度 → 暂停问用户              │
│  高置信度 → 直接进入规划            │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│  2. Task Understanding           │  ← LLM 理解任务
│  输入：用户描述 + 上下文 + 记忆      │
│  输出：任务类型 + 关键实体 + 约束    │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│  3. Plan Generation              │  ← LLM 生成执行计划
│  输入：任务理解 + 可用工具列表        │
│  输出：ExecutionPlan（步骤列表）     │
│  每步标注：risk_level + approval    │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│  4. Plan Review（用户确认）        │  ← Checkpoint
│  前端展示计划，用户可：              │
│  - 直接批准                        │
│  - 编辑步骤（增/删/改顺序）          │
│  - 拒绝（终止）                     │
└──────────────┬───────────────────┘
               │
        ┌──────┴──────┐
        ▼              ▼
     批准             拒绝/编辑
        │              │
        ▼              └→ 回到步骤 3 重新生成
┌──────────────────────────────────┐
│  5. Begin TAOR Execution         │  → 进入 TAOR 循环
└──────────────────────────────────┘
```

### 1.4 新增 API 接口

```python
# 新增路由（不替换现有 /v1/aip/logic/execute）

# 1. 创建任务（触发 Plan Mode）
POST /v1/aip/tasks
Body: {
    "description": "帮我接入淘宝天猫商家",
    "context": {
        "platform": "taobao",
        "merchant_id": "123456",
        "data_types": ["orders", "products", "customers"]
    },
    "agent_id": "aip-agent-xxx"  # 可选，指定执行 Agent
}
Response: {
    "task_id": "task-xxx",
    "status": "planning",
    "clarification_needed": [  # 需要澄清的问题
        {
            "field": "api_key",
            "question": "请提供淘宝开放平台的 App Key",
            "required": true
        }
    ]
}

# 2. 获取执行计划
GET /v1/aip/tasks/{task_id}/plan
Response: {
    "plan_id": "plan-xxx",
    "steps": [...],
    "summary": "将分6步完成淘宝商家数据接入...",
    "estimated_tokens": 5000,
    "risk_assessment": "medium"
}

# 3. 批准/编辑/拒绝计划
POST /v1/aip/tasks/{task_id}/plan/approve
Body: { "plan_id": "plan-xxx", "approved_by": "user-xxx" }

POST /v1/aip/tasks/{task_id}/plan/edit
Body: { "steps": [...修改后的步骤...] }

POST /v1/aip/tasks/{task_id}/cancel
Body: { "reason": "用户取消" }
```

---

## 二、TAOR 循环控制器

### 2.1 核心循环

参考 Claude Code 的 TAOR 循环：Think → Act → Observe → Repeat

```python
# aip_taor_loop.py

class TAORLoopController:
    """TAOR 循环控制器。

    替换 aip_logic_engine.py 中 execute_flow 的 mock 实现。
    保留 execute_flow 方法签名，内部改为调用 TAOR 循环。
    """

    def __init__(
        self,
        llm_adapter: "LLMAdapter",
        tool_executor: "ToolExecutor",
        memory: "MemorySystem",
        permission_gate: "PermissionGate",
        checkpoint_store: "CheckpointStore",
    ):
        self._llm = llm_adapter
        self._tools = tool_executor
        self._memory = memory
        self._perm = permission_gate
        self._ckpt = checkpoint_store
        self._hooks: list[Hook] = []

    async def run(self, plan: ExecutionPlan, context: dict) -> TaskResult:
        """执行 TAOR 循环。"""
        task = self._init_task(plan, context)

        for step in plan.steps:
            # ── Think ──
            # 根据步骤配置和当前上下文，生成具体的执行指令
            think_result = await self._think(task, step)
            await self._fire_hook("post_think", task, think_result)

            # ── Act ──
            # 执行动作（LLM 调用 / Tool 调用 / Action 写回）
            act_result = await self._act(task, step, think_result)
            await self._fire_hook("post_act", task, act_result)

            # ── Reflect ──
            # 自审：检查执行结果是否符合预期
            reflection = await self._reflect(task, step, act_result)
            if reflection.should_retry and step.retry_count < step.max_retries:
                step.retry_count += 1
                continue  # 重新执行本步骤

            if reflection.is_fatal:
                task.status = "failed"
                await self._fire_hook("on_fail", task, reflection)
                break

            # ── Permission Gate ──
            # 高风险操作暂停等待确认
            if step.requires_approval and not step.approved:
                task.status = "awaiting_approval"
                await self._fire_hook("on_checkpoint", task, step)
                # 暂停循环，等待用户在前端确认
                # 用户确认后调用 POST /v1/aip/tasks/{id}/resume 继续
                return TaskResult(
                    task_id=task.id,
                    status="awaiting_approval",
                    pending_step=step.id,
                    artifact=self._render_diff(task, step, act_result),
                )

            # ── Observe ──
            # 更新上下文，记录观察结果
            task = self._observe(task, step, act_result, reflection)
            await self._fire_hook("post_observe", task)

            # ── Checkpoint ──
            # 保存检查点（支持回滚）
            await self._ckpt.save(task)

        task.status = "completed"
        await self._fire_hook("on_success", task)
        return self._build_result(task)
```

### 2.2 Think 阶段 — 生成执行指令

```python
async def _think(self, task: Task, step: TaskStep) -> ThinkResult:
    """Think 阶段：根据步骤配置和上下文，生成具体执行指令。

    当前 mock 实现：直接返回 step.action_config
    升级后：调用 LLM 理解上下文，生成精确的执行指令
    """
    # 从记忆中检索相关经验
    memory_hits = await self._memory.retrieve(
        query=f"task_type={task.type} step={step.action_type}",
        layer="semantic",  # 从 Semantic 层检索行业知识
        top_k=3
    )

    # 从 Episodic 层检索历史经验
    episodic_hits = await self._memory.retrieve(
        query=f"similar past tasks",
        layer="episodic",
        top_k=2
    )

    # 构造 Think Prompt
    prompt = self._build_think_prompt(task, step, memory_hits, episodic_hits)

    # 调用 LLM 生成执行指令
    llm_response = await self._llm.chat(
        messages=[
            {"role": "system", "content": THINK_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        model="private-medium",  # 模型路由
        temperature=0.3,  # 低温度保证确定性
        max_tokens=512
    )

    return ThinkResult(
        instruction=llm_response.content,
        memory_used=[m.id for m in memory_hits + episodic_hits],
        confidence=llm_response.confidence
    )
```

### 2.3 Act 阶段 — 执行动作

```python
async def _act(self, task: Task, step: TaskStep, think: ThinkResult) -> ActResult:
    """Act 阶段：执行具体动作。

    当前 mock 实现：
    - kind=="llm" → 返回 "[LLM response for: ...]"
    - kind=="tool" → 返回 "[Tool {name} executed]"

    升级后：根据 action_type 分发到真实执行器
    """
    if step.action_type == "llm_call":
        # 真实调用 LLM（通过 LLM Adapter）
        result = await self._llm.chat(
            messages=[
                {"role": "system", "content": step.action_config.get("system_prompt", "")},
                {"role": "user", "content": think.instruction}
            ],
            model=step.action_config.get("model", "private-medium"),
            temperature=step.action_config.get("temperature", 0.3),
            max_tokens=step.action_config.get("max_tokens", 1024)
        )
        return ActResult(
            output=result.content,
            tokens_used=result.usage.total_tokens,
            latency_ms=result.latency_ms
        )

    elif step.action_type == "tool_call":
        # 调用现有 Tool Executor（接入 Action Engine / Function Engine）
        result = await self._tools.execute(
            tool_name=step.action_config["tool_name"],
            params=step.action_config.get("params", {}),
            context=task.context
        )
        return ActResult(
            output=result.output,
            tokens_used=0,
            latency_ms=result.latency_ms,
            side_effects=result.side_effects  # 记录副作用
        )

    elif step.action_type == "action_writeback":
        # 调用 Ontology Action Engine（已有 49+ endpoint）
        # POST /v1/actions/execute → ActionEngine.execute()
        result = await self._tools.execute_action(
            action_type=step.action_config["action_type"],
            object_id=step.action_config["object_id"],
            params=step.action_config.get("params", {})
        )
        return ActResult(
            output=result.output,
            tokens_used=0,
            latency_ms=result.latency_ms,
            side_effects=[{"type": "writeback", "detail": result.detail}],
            requires_approval=step.requires_approval
        )

    elif step.action_type == "ontology_query":
        # 查询 Ontology 对象
        # GET /v1/objects/{objectType} → 已有 80+ endpoint
        result = await self._tools.query_ontology(
            object_type=step.action_config["object_type"],
            filter=step.action_config.get("filter", {}),
            limit=step.action_config.get("limit", 50)
        )
        return ActResult(
            output=result.data,
            tokens_used=0,
            latency_ms=result.latency_ms
        )

    elif step.action_type == "branch":
        # 分支评估（升级：用 LLM 判断，不再做字符串匹配）
        result = await self._llm.chat(
            messages=[
                {"role": "system", "content": "你是条件评估助手。根据上下文判断应走哪条分支。"},
                {"role": "user", "content": f"条件: {step.action_config['condition']}\n上下文: {json.dumps(task.context, ensure_ascii=False)}\n可选分支: {step.action_config['paths']}"}
            ],
            model="private-small",  # 分支判断用小模型
            temperature=0.0,
            max_tokens=64
        )
        chosen_path = self._parse_branch_result(result.content, step.action_config["paths"])
        return ActResult(
            output={"branch_path": chosen_path},
            tokens_used=result.usage.total_tokens,
            latency_ms=result.latency_ms
        )
```

### 2.4 Reflect 阶段 — 自审

```python
async def _reflect(self, task: Task, step: TaskStep, act_result: ActResult) -> ReflectionResult:
    """Reflect 阶段：自审执行结果。

    参考 Claude Code Reflection 机制：
    每轮 Act 后自审 — 成功率 60% → 85%（成本是多一轮模型调用）
    """
    # 对比预期输出和实际输出
    prompt = f"""你是任务自审助手。请检查执行结果是否符合预期。

步骤预期：{step.expected_output}
实际输出：{act_result.output[:500]}

请判断：
1. 结果是否符合预期？(yes/no/partial)
2. 如果不符合，问题出在哪里？
3. 是否应该重试？(yes/no)
4. 是否是致命错误？(yes/no)

请以 JSON 格式返回。"""

    result = await self._llm.chat(
        messages=[{"role": "user", "content": prompt}],
        model="private-small",
        temperature=0.0,
        max_tokens=256
    )

    return self._parse_reflection(result.content)
```

### 2.5 Observe 阶段 — 更新上下文

```python
def _observe(self, task: Task, step: TaskStep, act_result: ActResult, reflection: ReflectionResult) -> Task:
    """Observe 阶段：更新上下文，记录观察结果。"""
    # 将执行结果写入 Working Memory
    task.context[f"step_{step.id}_output"] = act_result.output
    task.context[f"step_{step.id}_reflection"] = reflection.dict()

    # 记录 Action 历史
    task.actions.append(ActionRecord(
        step_id=step.id,
        action_type=step.action_type,
        input=step.action_config,
        output=act_result.output,
        tokens_used=act_result.tokens_used,
        latency_ms=act_result.latency_ms,
        success=reflection.is_success,
        timestamp=time.time()
    ))

    # 如果有副作用，记录到 Artifact
    if act_result.side_effects:
        for se in act_result.side_effects:
            task.artifacts.append(Artifact(
                type="side_effect",
                content=json.dumps(se, ensure_ascii=False),
                status="applied"  # 副作用已发生
            ))

    # 检查 Working Memory 是否超限（参考 Claude Code 指针策略）
    if self._context_size(task) > self._max_context_tokens:
        task = self._compress_context(task)  # 超限时用指针代替内容

    return task
```

---

## 三、与现有代码的对接

### 3.1 execute_flow 兼容方案

```python
# aip_logic_engine.py — 修改后

class LogicEngine:
    # ... 保留现有 Singleton 和 CRUD 方法 ...

    def execute_flow(self, blocks: list[LogicBlock], context: dict | None = None) -> dict[str, Any]:
        """执行 DAG。

        兼容策略：
        - 如果环境变量 AIP_HARNESS_MODE=1，走真实 TAOR 循环
        - 否则走原有 mock 逻辑（保留向后兼容）
        """
        import os
        if os.environ.get("AIP_HARNESS_MODE") == "1":
            return self._execute_harness(blocks, context or {})
        else:
            return self._execute_mock(blocks, context or {})  # 原 mock 逻辑

    def _execute_mock(self, blocks, context):
        # 原 execute_flow 逻辑完整保留，仅改名
        ...

    def _execute_harness(self, blocks, context):
        """走真实 TAOR 循环。"""
        from aos_api.aip_taor_loop import TAORLoopController
        controller = self._get_harness_controller()

        # 将 LogicBlock 转为 ExecutionPlan
        plan = self._blocks_to_plan(blocks)

        # 运行 TAOR 循环
        import asyncio
        result = asyncio.run(controller.run(plan, context))

        # 转换为原有返回格式（保持兼容）
        return {
            "results": result.actions,
            "total_tokens": result.total_tokens,
            "elapsed_ms": result.total_latency_ms,
            "final_context_keys": list(result.context.keys()),
            # 新增字段（前端可选消费）
            "task_id": result.task_id,
            "checkpoints": result.checkpoint_ids,
            "reflections": result.reflections,
        }
```

### 3.2 前端兼容方案

前端 `LogicCanvasPage.tsx` 当前调用 `POST /v1/aip/logic/execute`，返回 `{results, total_tokens, elapsed_ms, final_context_keys}`。

升级后：
- **旧接口保持不变**：返回结构兼容，新增字段前端可忽略
- **新增 Task 接口**：`POST /v1/aip/tasks` 创建任务 → `GET /v1/aip/tasks/{id}/plan` 获取计划 → `POST /v1/aip/tasks/{id}/plan/approve` 批准 → `GET /v1/aip/tasks/{id}/status` 查看进度

前端分两种模式：
- **快速模式**（现有）：直接调 `/logic/execute`，适合简单测试
- **Plan Mode**（新增）：调 `/tasks` 走完整 Plan → Approve → Execute 流程

---

## 四、Hook 系统

```python
# aip_hooks.py

class Hook(BaseModel):
    id: str
    event: str  # pre_think | post_think | pre_act | post_act | pre_observe | post_observe | on_checkpoint | on_fail | on_success
    handler: str  # handler 函数名
    config: dict[str, Any] = {}
    enabled: bool = True
    priority: int = 0  # 执行优先级


class HookSystem:
    """Hook 系统：在 TAOR 循环各阶段插入自定义逻辑。"""

    # 电商场景的内置 Hook
    BUILTIN_HOOKS = [
        # pre_act: 执行前检查是否在营业时间
        Hook(
            id="hook-business-hours",
            event="pre_act",
            handler="check_business_hours",
            config={"allowed_hours": "09:00-22:00"},
            priority=100  # 高优先级
        ),
        # post_act: 执行后自动记录到行业 Wiki（管道2：自学习）
        Hook(
            id="hook-wiki-learn",
            event="post_act",
            handler="record_to_wiki",
            config={"confidence_threshold": 0.8},
            priority=50
        ),
        # on_checkpoint: 检查点时发送通知
        Hook(
            id="hook-notify",
            event="on_checkpoint",
            handler="send_notification",
            config={"channels": ["wechat", "email"]},
            priority=10
        ),
    ]
```

---

## 五、测试方案

```python
# tests/test_aip_taor_loop.py

import pytest
from aos_api.aip_taor_loop import TAORLoopController
from aos_api.aip_task_model import ExecutionPlan, TaskStep

class TestTAORLoop:
    """TAOR 循环控制器测试。"""

    @pytest.fixture
    def mock_controller(self):
        """使用 mock LLM 和 Tool 的控制器（不依赖外部服务）。"""
        return TAORLoopController(
            llm_adapter=MockLLMAdapter(),
            tool_executor=MockToolExecutor(),
            memory=MockMemory(),
            permission_gate=MockPermissionGate(),
            checkpoint_store=MockCheckpointStore(),
        )

    def test_plan_generation(self, mock_controller):
        """测试 Plan Mode 生成执行计划。"""
        plan = mock_controller.generate_plan(
            description="接入淘宝天猫商家",
            context={"platform": "taobao", "merchant_id": "123456"}
        )
        assert plan.status == "draft"
        assert len(plan.steps) > 0
        assert all(s.risk_level in ["low", "medium", "high", "critical"] for s in plan.steps)

    def test_taor_loop_basic(self, mock_controller):
        """测试基本 TAOR 循环。"""
        plan = ExecutionPlan(steps=[
            TaskStep(index=0, title="查询客户", action_type="ontology_query", ...)
            TaskStep(index=1, title="生成推荐", action_type="llm_call", ...)
        ])
        result = mock_controller.run(plan, context={})
        assert result.status == "completed"
        assert len(result.actions) == 2

    def test_checkpoint_rollback(self, mock_controller):
        """测试检查点回滚。"""
        result = mock_controller.run(plan_with_3_steps, context={})
        # 回滚到第1步
        rolled = mock_controller.rollback(result.task_id, to_step=1)
        assert rolled.status == "executing"
        assert rolled.current_step == 1

    def test_permission_gate_pause(self, mock_controller):
        """测试权限门控暂停。"""
        plan = ExecutionPlan(steps=[
            TaskStep(index=0, title="退款", action_type="action_writeback",
                     risk_level="high", requires_approval=True, ...)
        ])
        result = mock_controller.run(plan, context={})
        assert result.status == "awaiting_approval"
        assert result.artifact is not None  # Diff 视图
```

---

## 六、Verification Loops — 验证循环升级

> **来源**：Claude Blog — [Building verification loops in Claude Code with skills](https://claude.com/blog/building-verification-loops-in-claude-code-with-skills)
> **更新时间**：2026-07-28

### 6.1 从 Reflection 到 Verification Loop

前文 §2.4 的 Reflection 自审是单步检查。Claude Blog 揭示了更系统化的 **Verification Loop** 机制：

```
生产技能（执行动作） → 验证技能（检查结果） → 失败？→ 自动修复 + 重新验证 → 通过？→ 交付
```

这不是简单的"自审"，而是**可编排的验证技能链**，有以下四种触发模式：

| 模式 | 说明 | 适用场景 | 电商数字同事应用 |
|------|------|---------|----------------|
| **Standalone** | 手动触发 | 跨领域检查 | 安全扫描、合规审计、敏感词检查 |
| **Embedded** | 嵌入生产技能自动触发 | 单工作流内置检查 | 私域管家生成话术后自动检查长度/敏感词 |
| **Chained** | 一个技能调用另一个，形成链 | 端到端验证 | 生产→验证→修复→交付的完整循环 |
| **On every PR** | CI/CD 级别全员门控 | 团队基础设施 | 每次配置变更自动验证数据质量 |

### 6.2 TAOR 循环升级 — 嵌入 Verification

```python
# aip_taor_loop.py — 升级后的 TAOR 循环

class TAORLoopController:

    async def run(self, plan: ExecutionPlan, context: dict) -> TaskResult:
        task = self._init_task(plan, context)

        for step in plan.steps:
            # Think
            think_result = await self._think(task, step)

            # Act
            act_result = await self._act(task, step, think_result)

            # ── Verify（替代原 Reflection）──
            verify_result = await self._verify(task, step, act_result)
            if verify_result.should_retry and step.retry_count < step.max_retries:
                step.retry_count += 1
                continue

            if verify_result.is_fatal:
                task.status = "failed"
                break

            # Observe
            task = self._observe(task, step, act_result, verify_result)

            # Checkpoint
            await self._ckpt.save(task)

        return self._build_result(task)

    async def _verify(self, task: Task, step: TaskStep, act_result: ActResult) -> VerifyResult:
        """Verify 阶段：执行验证技能链。

        参考 Claude Code 的 verification skill 机制：
        - 每个 Action Type 可配置对应的 verification skill
        - 验证失败自动修复 + 重新验证（最多 max_retries 次）
        - 支持 Chained 模式（一个验证技能调用另一个）
        """
        # 获取该步骤的验证技能配置
        verify_skills = self._get_verify_skills(step.action_type)

        for skill in verify_skills:
            result = await self._execute_verify_skill(skill, task, step, act_result)

            if not result.passed:
                # 尝试自动修复
                if result.auto_fix:
                    fixed = await self._auto_fix(task, step, act_result, result)
                    if fixed:
                        continue  # 修复后重新验证

                # 无法自动修复，返回失败
                return VerifyResult(
                    passed=False,
                    should_retry=True,
                    is_fatal=result.severity == "critical",
                    issues=result.issues
                )

        return VerifyResult(passed=True)
```

### 6.3 验证技能配置

```python
# aip_verify_skills.py — 验证技能定义

VERIFY_SKILLS = {
    # 私域管家：话术验证
    "customer_onboarding": [
        VerifySkill(
            id="verify-script-length",
            name="话术长度检查",
            check="len(script) <= 30",
            auto_fix="truncate_and_regenerate",
            severity="medium"
        ),
        VerifySkill(
            id="verify-sensitive-words",
            name="敏感词检查",
            check="not contains_sensitive_words(script)",
            auto_fix="regenerate_without_sensitive",
            severity="high",
            max_retries=3
        ),
        VerifySkill(
            id="verify-personalization",
            name="个性化检查",
            check="mentions_product(script, customer.history)",
            auto_fix="regenerate_with_product_mention",
            severity="medium"
        ),
    ],
    # 导购顾问：推荐验证
    "product_recommendation": [
        VerifySkill(
            id="verify-ingredient-compat",
            name="成分兼容性检查",
            check="check_ingredient_compatibility(products)",
            auto_fix=None,  # 无法自动修复，需人工
            severity="critical"
        ),
        VerifySkill(
            id="verify-skin-type-match",
            name="肤质匹配检查",
            check="check_skin_type_match(customer.skin_type, products)",
            auto_fix="filter_by_skin_type",
            severity="high"
        ),
    ],
    # 内容官：文案验证
    "content_generation": [
        VerifySkill(
            id="verify-platform-rules",
            name="平台规则检查",
            check="check_platform_compliance(content, platform)",
            auto_fix="adjust_for_platform",
            severity="high"
        ),
        VerifySkill(
            id="verify-brand-tone",
            name="品牌调性检查",
            check="check_brand_tone(content)",
            auto_fix=None,
            severity="medium"
        ),
    ],
}
```

### 6.4 Chained 验证链

```
生产技能                    验证技能链
─────────                  ──────────────────────────────
私域管家·生成话术    →      verify-script-length
                           → verify-sensitive-words
                           → verify-personalization
                           → 全通过？交付
                           → 失败？自动修复+重新验证

导购顾问·生成推荐    →      verify-ingredient-compat
                           → verify-skin-type-match
                           → 全通过？交付
                           → 失败？人工介入（critical级别）

内容官·生成文案      →      verify-platform-rules
                           → verify-brand-tone
                           → 全通过？交付
                           → 失败？自动调整+重新验证
```

---

## 七、实施清单（更新）

| 序号 | 文件 | 动作 | 说明 |
|------|------|------|------|
| 1 | `aip_task_model.py` | 新增 | Task + Artifact + Action + Checkpoint + ExecutionPlan 数据模型 |
| 2 | `aip_taor_loop.py` | 新增 | TAORLoopController — Think/Act/**Verify**/Observe 循环 |
| 3 | `aip_llm_adapter.py` | 新增 | LLM 适配器（对接模型路由模块） |
| 4 | `aip_tool_executor.py` | 新增 | 工具执行器（接入 Action Engine + Function Engine + Ontology 查询） |
| 5 | `aip_hooks.py` | 新增 | Hook 系统 |
| 6 | **`aip_verify_skills.py`** | **新增** | **验证技能定义 + 自动修复逻辑** |
| 7 | `aip_logic_engine.py` | 修改 | `execute_flow` 增加 Harness 模式分支 |
| 8 | `routers/phase3_aip_logic.py` | 修改 | 新增 `/tasks` `/tasks/{id}/plan` `/tasks/{id}/plan/approve` 路由 |
| 9 | `tests/test_aip_taor_loop.py` | 新增 | TAOR 循环测试（含验证技能链测试） |

---

*本文档为方案设计层，实施前需用户确认。*
*更新记录：2026-07-28 新增 §六 Verification Loops（来源 Claude Blog），将 Reflection 升级为验证技能链。*

# AIP 决策引擎升级方案 — 从 Mock 到真实 Harness

> **2026-08-02 基线说明：** 本目录的 TAOR/数字同事内容是目标设计。当前权威节点契约是 Logic 自由画布 + 可信 dryRun + 运行历史 + Evals + 发布治理；外部 LLM/Tool/Action 适配器必须显式注册。微商城具体 6 条 Logic 及可发布边界见 [228 微商城 FDE 规格](../微商城电商接入方案/228-微商城专项实施准备与FDE全链路规格.md#6-aip-logic6-条业务链路)。

> 创建时间：2026-07-28
> 状态：方案设计（先方案后编码）
> 关联代码：`aos-platform-w4/services/aos-api/aos_api/aip_logic_engine.py` · `aip_drafts_engine.py` · `aip_agents_engine.py`
> 关联前端：`aos-platform-w4/apps/web/src/pages/s2/LogicCanvasPage.tsx` · `DraftInboxPage.tsx` · `ObservabilityPage.tsx`

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 先方案后编码 | 本文档为方案层，通过前不写实现码 |
| 最小更改 | 升级路径分阶段，每阶段不破坏现有功能 |
| 不影响现有功能 | 现有 Singleton+内存存储 保留为"内存模式"，新增"持久化模式" |
| 自测验证 | 每阶段完成后跑 `pytest tests/test_aip_*.py` 验证不回归 |

---

## 一、当前状态诊断

### 1.1 三个引擎的现状

| 引擎 | 文件 | 模式 | 真实逻辑？ | 关键问题 |
|------|------|------|-----------|---------|
| LogicEngine | `aip_logic_engine.py` (202行) | Singleton + threading.Lock + dict 内存 | ❌ mock | LLM 调用返回 `f"[LLM response for: {prompt[:50]}]"`；Tool 调用返回 `f"[Tool {tool_name} executed]"`；branch 评估只做字符串匹配 |
| DraftsEngine | `aip_drafts_engine.py` (136行) | Singleton + threading.Lock + dict 内存 | ⚠️ 状态机真实 | 状态机 `draft→approved/rejected` 校验可用，但数据在内存，重启丢失 |
| AgentsEngine | `aip_agents_engine.py` (140行) | Singleton + threading.Lock + dict 内存 | ❌ 无执行 | Agent 有 prompt/tools/guardrails 配置，但从未被调用过；calls/success_rate/avg_latency 全为初始值 |

### 1.2 execute_flow 的 mock 实现详解

```python
# 当前 aip_logic_engine.py 第 98-152 行 execute_flow 方法：
# - block.kind == "llm" → 返回固定字符串 "[LLM response for: ...]"
# - block.kind == "tool" → 返回 "[Tool {name} executed]"
# - block.kind == "branch" → _eval_branch 只做 "success"/"true" 字符串匹配
# - total_tokens 全部硬编码（llm=120, tool=20, task=15）
# - elapsed_ms = total_tokens * 3
# - 无网络调用、无模型调用、无 Action 写回
```

### 1.3 前端页面对接现状

| 前端页面 | 对接后端 | 数据来源 |
|---------|---------|---------|
| `LogicCanvasPage.tsx` | `POST /v1/aip/logic/execute` | 后端返回 mock results，前端渲染 COT（Chain of Thought）步骤 |
| `DraftInboxPage.tsx` | `GET/POST /v1/aip/drafts` | 后端状态机可用，数据内存 |
| `ObservabilityPage.tsx` | 无独立后端 | 纯前端 MOCK_TRACES / MOCK_METRICS 常量 |
| `AgentsPage.tsx` | `GET/POST /v1/aip/agents` | CRUD 可用，无真实 Agent 执行 |

---

## 二、升级目标 — 从"对话产品"到"工作流产品"

### 2.1 核心认知转变

参考 Claude 产品哲学深度解析：

> **Agent 是同事，不是工具/自动售货机** — 能干活、会犯错、需要被监督但值得被信任。

当前 AIP 是"对话产品"（聊天框 + 工具调用），需要升级为"工作流产品"（任务执行框架）：

| 维度 | 当前（对话产品） | 升级后（工作流产品） |
|------|----------------|---------------------|
| 核心数据模型 | LogicFlow + Block | **Task + Artifact + Action** |
| 执行模型 | 一次性 execute_flow | **TAOR 循环（Think→Act→Observe→Repeat）** |
| 变更呈现 | 全量返回 | **Diff 视图（精确呈现变更）** |
| 权限控制 | Draft 审批（单点） | **六层权限防线（纵深防御）** |
| 自我修正 | 无 | **Reflection 自审（每轮 Act 后自检）** |
| 记忆 | 无 | **三层记忆（Semantic + Episodic + Working）** |
| 产品 metric | DAU | **任务成功率、单任务时长** |

### 2.2 升级不破坏现有功能的原则

```
现有代码                        升级后
══════════                      ════════════
LogicEngine (Singleton+内存)  →  保留为"内存模式"（开发/测试用）
                                新增"Harness 模式"（生产用，接真实 LLM + DB）

DraftsEngine (状态机)         →  保留状态机逻辑
                                新增持久化层（Redis/PostgreSQL）
                                新增多级审批（不只 draft→approved）

AgentsEngine (CRUD)           →  保留 CRUD
                                新增 execute_agent() 真实调用
                                新增 Guardrail 运行时拦截
```

---

## 三、升级架构 — 五层 Harness

### 3.1 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    入口层（已有，不改）                        │
│  LogicCanvasPage → POST /v1/aip/logic/execute               │
│  DraftInboxPage  → /v1/aip/drafts/*                         │
│  AgentsPage     → /v1/aip/agents/*                          │
│  ChatbotPage    → /v1/aip/chat/*                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              运行层（NEW — TAOR 循环 + 状态机）                │
│                                                             │
│  ┌─────────────────────────────────────────┐                │
│  │         TAORLoopController             │                │
│  │  Think → Act → Observe → Repeat       │                │
│  │  每轮插入 Reflection 自审节点            │                │
│  │  支持 interrupt（人机协同中断点）         │                │
│  └──────────────┬──────────────────────────┘                │
│                 │                                           │
│  ┌──────────────▼──────────────────────────┐                │
│  │         TaskStateMachine                │                │
│  │  pending → planning → executing         │                │
│  │  → reviewing → completed / failed       │                │
│  │  + checkpoint（每步可暂停/回滚）          │                │
│  └──────────────┬──────────────────────────┘                │
│                 │                                           │
│  ┌──────────────▼──────────────────────────┐                │
│  │         HookSystem                      │                │
│  │  pre_act / post_act / pre_observe       │                │
│  │  / on_checkpoint / on_fail / on_success │                │
│  └─────────────────────────────────────────┘                │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              引擎层（UPGRADE — 替换 mock 调用）               │
│                                                             │
│  ┌─────────────────────────────────────────┐                │
│  │         QueryEngine（参考 Claude Code）  │                │
│  │  动态拼装 Prompt（碎片化提示词）           │                │
│  │  安全守则注入（不可绕过）                  │                │
│  │  模型路由（私有-中/私有-大/外部）          │                │
│  └──────────────┬──────────────────────────┘                │
│                 │                                           │
│  ┌──────────────▼──────────────────────────┐                │
│  │    LLM Adapter（新增）                   │                │
│  │  支持：OpenAI / Anthropic / 私有模型      │                │
│  │  接口：chat() / stream() / embed()       │                │
│  │  重试 + 超时 + token 计量                 │                │
│  └──────────────┬──────────────────────────┘                │
│                 │                                           │
│  ┌──────────────▼──────────────────────────┐                │
│  │    Tool Executor（新增）                 │                │
│  │  接入现有 Action Engine（ontology_action）│                │
│  │  接入现有 Function Engine（ontology_function）│            │
│  │  接入 Ontology 查询（/v1/objects/*）       │                │
│  │  接入 Workshop 写回（/v1/writeback/*）     │                │
│  └─────────────────────────────────────────┘                │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              工具层（已有，复用）                               │
│  Ontology Action Engine（49+ endpoint，生产可用）             │
│  Ontology Function Engine（SQL/PYTHON 双模式，沙箱求值）       │
│  Pipeline Builder（52+ endpoint，DAG + 提案工作流）           │
│  Writeback 事务（begin/apply/commit/rollback）                │
│  Dataset 查询（80+ endpoint）                                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              基础设施层（NEW — 持久化 + 记忆 + 可观测）          │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ 检查点    │  │ 三层记忆  │  │ 权限防线  │  │ 可观测    │    │
│  │ Redis     │  │ Semantic │  │ 6层纵深   │  │ 真实trace │    │
│  │ 持久化    │  │ Episodic  │  │ 防御      │  │ +metrics  │    │
│  │          │  │ Working   │  │          │  │          │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 与现有代码的对接点

| 新增组件 | 对接的现有代码 | 对接方式 |
|---------|--------------|---------|
| TAORLoopController | `aip_logic_engine.py::LogicEngine.execute_flow()` | 替换 execute_flow 内部实现，保留方法签名和返回结构 |
| TaskStateMachine | `aip_drafts_engine.py::VALID_TRANSITIONS` | 扩展状态机：draft→planning→executing→reviewing→completed |
| HookSystem | 无（全新） | 新增 `aip_hooks.py` |
| QueryEngine | 无（全新） | 新增 `aip_query_engine.py`，参考 Claude Code 的碎片化提示词拼装 |
| LLM Adapter | 无（全新） | 新增 `aip_llm_adapter.py`，对接模型路由（已有模型管理模块） |
| Tool Executor | `ontology_action_engine.py` + `ontology_function_engine.py` | 调用现有 `ActionEngine.execute()` 和 `FunctionEngine.eval()` |
| Checkpoint 持久化 | 无（全新） | 新增 `aip_checkpoint_store.py`，Redis 实现 |
| 三层记忆 | 无（全新） | 新增 `aip_memory.py`，Semantic 用 RAG，Episodic 用时间索引，Working 用指针 |
| 权限防线 | `aip_drafts_engine.py`（单点 Draft 审批） | 扩展为六层（详见 03-六层权限防线设计.md） |
| 可观测 | `ObservabilityPage.tsx`（纯前端 mock） | 新增后端 trace 收集 + metrics 聚合 |

---

## 四、升级路径 — 四阶段

### Phase 1：TAOR 循环骨架（替换 mock 调用）

**目标**：将 `execute_flow` 从 mock 升级为真实 TAOR 循环

**改动文件**：
- `aip_logic_engine.py` — 重写 `execute_flow()` 方法
- 新增 `aip_taor_loop.py` — TAOR 循环控制器
- 新增 `aip_llm_adapter.py` — LLM 适配器
- 新增 `aip_tool_executor.py` — 工具执行器

**关键设计**：
```python
# aip_taor_loop.py 核心结构
class TAORLoopController:
    """Think → Act → Observe → Repeat 循环控制器。"""

    async def run(self, flow: LogicFlow, context: dict) -> TaskResult:
        task = self._create_task(flow, context)  # 创建 Task

        while not task.is_complete:
            # Think：生成下一步计划
            plan = await self._think(task)

            # Act：执行计划（LLM 调用 / Tool 调用 / Action 写回）
            action_result = await self._act(task, plan)

            # Reflect：自审（参考 Claude Code Reflection 机制）
            reflection = await self._reflect(task, action_result)
            if reflection.should_retry:
                continue

            # Observe：观察结果，更新上下文
            task = self._observe(task, action_result, reflection)

            # Checkpoint：保存检查点（支持回滚）
            await self._save_checkpoint(task)

            # Permission Gate：高风险操作暂停等待确认
            if action_result.requires_approval:
                task = await self._pause_for_approval(task, action_result)

        return task.result
```

**验收标准**：
- [ ] `execute_flow` 返回真实 LLM 响应（不再返回 `[LLM response for: ...]`）
- [ ] `execute_flow` 返回真实 Tool 执行结果（调用 Action Engine）
- [ ] branch 评估使用 LLM 判断（不再做字符串匹配）
- [ ] token 计量真实（从 LLM Adapter 获取）
- [ ] `pytest tests/test_aip_logic.py` 全部通过

### Phase 2：Task 数据模型 + 检查点持久化

**目标**：从内存模式升级为持久化模式，支持暂停/恢复/回滚

**改动文件**：
- 新增 `aip_task_model.py` — Task + Artifact + Action 数据模型
- 新增 `aip_checkpoint_store.py` — Redis 检查点存储
- 修改 `aip_drafts_engine.py` — 扩展状态机

**关键设计**：
```python
# aip_task_model.py 核心结构
class Task(BaseModel):
    id: str
    type: str  # data_ingestion | customer_outreach | content_generation ...
    status: str  # pending → planning → executing → reviewing → completed / failed
    plan: list[TaskStep]  # 执行计划（Plan Mode 产物）
    artifacts: list[Artifact]  # 产物（Diff / 报告 / 配置变更）
    actions: list[ActionRecord]  # 执行记录
    checkpoints: list[Checkpoint]  # 检查点列表
    context: dict  # Working Memory
    memory_refs: list[str]  # Semantic + Episodic 记忆引用

class Artifact(BaseModel):
    id: str
    type: str  # diff | report | config | dataset
    content: str  # 变更内容（Diff 格式）
    status: str  # draft → proposed → approved → applied

class Checkpoint(BaseModel):
    id: str
    task_id: str
    step_index: int
    snapshot: dict  # 完整上下文快照
    created_at: float
    can_rollback: bool = True
```

**验收标准**：
- [ ] Task 创建后持久化到 Redis（重启不丢失）
- [ ] 每个 TAOR 循环步保存 Checkpoint
- [ ] 支持 `POST /v1/aip/tasks/{id}/rollback?to_checkpoint={cp_id}` 回滚
- [ ] 支持 `POST /v1/aip/tasks/{id}/pause` 和 `/resume`
- [ ] `pytest tests/test_aip_task_model.py` 全部通过

### Phase 3：六层权限防线 + Diff 视图

**目标**：从单点 Draft 审批升级为纵深防御

**改动文件**：
- 新增 `aip_permission_gate.py` — 六层权限防线
- 修改 `aip_drafts_engine.py` — 集成权限防线
- 新增 `aip_diff_renderer.py` — Diff 视图渲染
- 修改前端 `DraftInboxPage.tsx` — 展示 Diff 视图

**验收标准**：
- [ ] 白名单配置可跳过低风险操作
- [ ] 自动模式分类器判断"无人值守是否安全"
- [ ] 高风险操作（退款/取消订单/配置变更）必须人工确认
- [ ] Diff 视图精确呈现"将要做什么"（不是全文件覆盖）
- [ ] `pytest tests/test_aip_permission.py` 全部通过

### Phase 4：三层记忆 + 可观测性

**目标**：行业 Wiki 基础设施 + 真实 trace 收集

**改动文件**：
- 新增 `aip_memory.py` — 三层记忆系统
- 新增 `aip_trace_collector.py` — 真实 trace 收集
- 修改前端 `ObservabilityPage.tsx` — 对接真实后端

**验收标准**：
- [ ] Semantic 层支持 RAG 检索行业 Wiki
- [ ] Episodic 层按时间索引历史会话
- [ ] Working 层超出限制时用指针代替内容
- [ ] ObservabilityPage 展示真实 trace 数据
- [ ] `pytest tests/test_aip_memory.py` 全部通过

---

## 五、数字同事技能编排概览

6 个数字同事将作为 AIP Logic 的"技能组"实现，每个技能组是一组预定义的 LogicFlow 模板：

| 数字同事 | 优先级 | 核心技能 | Plan Mode 设计 |
|---------|--------|---------|---------------|
| **私域管家** | P0 | 客户沉淀→打标→主动提醒→跟进排期 | 详见 `02-私域管家技能编排.md` |
| **导购顾问** | P0 | 画像匹配→搭配建议→话术生成→破冰钩子 | 详见 `04-导购顾问技能编排.md` |
| **数据参谋** | P1 | 看板→异常检测→归因分析→决策支持 | 详见 `08-数据参谋技能编排.md` |
| **客服专员** | P1 | 售前咨询→售后回访→消耗计算→差评预警 | 详见 `06-客服专员技能编排.md` |
| **内容官** | P2 | 多平台文案→短视频脚本→内容日历→素材库 | 详见 `05-内容官技能编排.md` |
| **活动策划师** | P2 | 时机推荐→方案生成→效果预测→活动复盘 | 详见 `07-活动策划师技能编排.md` |

每个数字同事的技能编排文档包含：
1. **技能链定义**：输入参数 → Plan Mode 生成 → TAOR 循环执行 → Checkpoint 确认 → 产物输出
2. **工具依赖**：调用的 Action / Function / Ontology 查询
3. **记忆依赖**：Semantic（行业知识）+ Episodic（历史经验）+ Working（当前任务）
4. **权限门控**：哪些操作需要人工确认
5. **Reflection 规则**：自审的判断标准

---

## 六、开放问题

1. **LLM Adapter 对接哪个模型路由？** — 需对接平台已有的模型管理模块（模型目录 → 模型供应商 → 模型路由）
2. **Redis 部署方案？** — 开发环境可用内存模式，生产环境需要 Redis 实例
3. **行业 Wiki 存储层？** — 用 Foundry Wiki 还是独立向量数据库？
4. **Guardrail 运行时？** — 参考现有 `aip_agents_engine.py::GuardrailRule`，但需要增加运行时拦截能力

---

## 七、文档索引

| 文档 | 说明 |
|------|------|
| `00-总览-从Mock到真实Harness.md` | 本文档 — 整体升级路径 |
| `01-Plan-Mode与TAOR循环设计.md` | TAOR 循环控制器详细设计 |
| `02-私域管家技能编排.md` | 第一个数字同事的完整技能链 |
| `03-六层权限防线设计.md` | 权限纵深防御详细设计 |

---

*本文档为方案设计层，持续迭代中。实施前需用户确认。*

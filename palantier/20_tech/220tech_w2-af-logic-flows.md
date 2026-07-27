# 220tech · W2-AF · 逻辑流与 Data Connection Agent 组（#111 / #112 / #113）

> **版本**：v1.0 · 2026-07-22
> **状态**：✅ 方案定稿 · 可编码
> **对齐**：
> - 差距分析 [220w](./220w-与目标系统差距分析.md) §11 #111/#112/#113
> - 220plan v4.4 已交付 79/166，本批收口 3 项 → 82/166
> **范围**：W2-AF 收口编排与代理三件 — Logic Flows（逻辑流编排）+ Agent Proxy（反向代理运行时）+ Agent Worker（客户主机执行运行时）
> **不替换底层**：本组是编排/代理层，不重写 wave_ext 或 functions 引擎

---

## 0. 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文回答 | 文档与代码注释均中文 |
| 先方案后编码 | 本文先定稿，再写引擎/路由/测试 |
| 最小更改 | 仅新增 `aos_api/logic_flows.py` + `aos_api/routers/logic_flows.py` + `tests/test_logic_flows.py`；`main.py` 加 2 行 |
| 不影响已有功能 | 三引擎纯新增；wave_ext 与 functions 模块保留 |
| 自测验证 | 单测全绿 + 全量回归 + 方案对照 |
| 编码前复习方案 | 已核对 W2-AE 引擎模式（单例 + 200 条 FIFO） |

---

## 1. 背景与边界

### 1.1 现状

| 能力 | 现状 | 缺口 |
| --- | --- | --- |
| 逻辑流编排 | 无 Compass Files Lister/连接流编排 | 🔴 缺 |
| Agent Proxy | 无内网反向代理运行时 | 🔴 缺 |
| Agent Worker | 无客户主机执行运行时 | 🔴 缺 |

### 1.2 边界

- ✅ 本组做：
  - #111 Logic Flows：FlowStep 4 种 kind（compass_files_lister/connector/join/transform）+ 顺序执行 + 步骤结果链
  - #112 Agent Proxy：online/offline/draining 3 态 + heartbeat + drain + forward_request（模拟转发）
  - #113 Agent Worker：registered/online/offline/failed 4 态 + heartbeat + assign_job（capability 匹配）+ complete_job
- ❌ 本组不做：
  - 真实网络代理转发（forward_request 模拟）
  - 实际客户主机命令执行（assign_job 仅记录）
  - 跨 Agent 路由（每 Agent 独立）

---

## 2. 数据模型

### 2.1 #111 LogicFlow

```python
class FlowStep(BaseModel):
    """逻辑流步骤。"""
    id: str
    kind: str                # compass_files_lister / connector / join / transform
    name: str = ""
    config: dict[str, Any] = {}
    next_step_id: str = ""   # 顺序执行时可空


class LogicFlow(BaseModel):
    """逻辑流定义。"""
    id: str
    name: str
    description: str = ""
    steps: list[FlowStep] = []
    status: str = "draft"    # draft / running / completed / error
    created_at: float = 0.0


class FlowExecution(BaseModel):
    """逻辑流执行记录。"""
    id: str
    flow_id: str
    status: str              # running / completed / error
    step_results: list[dict[str, Any]] = []   # 每步结果 [{step_id, kind, status, output, error}]
    started_at: float = 0.0
    completed_at: float = 0.0


_VALID_STEP_KINDS = {"compass_files_lister", "connector", "join", "transform"}
_VALID_FLOW_STATUSES = {"draft", "running", "completed", "error"}
_VALID_EXEC_STATUSES = {"running", "completed", "error"}
```

### 2.2 #112 AgentProxy

```python
class AgentProxy(BaseModel):
    """内网反向代理运行时。"""
    id: str
    name: str
    agent_id: str
    proxy_url: str
    auth_token: str = ""
    status: str = "offline"           # online / offline / draining
    connections: int = 0
    last_heartbeat: float = 0.0
    created_at: float = 0.0


_VALID_PROXY_STATUSES = {"online", "offline", "draining"}
```

### 2.3 #113 AgentWorker

```python
class AgentWorker(BaseModel):
    """客户主机执行运行时。"""
    id: str
    agent_id: str
    host: str
    version: str = "1.0.0"
    status: str = "registered"        # registered / online / offline / failed
    capabilities: list[str] = []      # ["sql", "python", "shell", "java"]
    last_heartbeat: float = 0.0
    job_ids: list[str] = []
    created_at: float = 0.0


class WorkerJob(BaseModel):
    """Worker 任务。"""
    id: str
    worker_id: str
    capability: str                   # 必须在 worker.capabilities 中
    payload: dict[str, Any] = {}
    status: str = "assigned"          # assigned / running / completed / failed
    result: dict[str, Any] = {}
    created_at: float = 0.0
    completed_at: float = 0.0


_VALID_WORKER_STATUSES = {"registered", "online", "offline", "failed"}
_VALID_JOB_STATUSES = {"assigned", "running", "completed", "failed"}
```

---

## 3. 引擎设计

文件：`aos_api/logic_flows.py`（新增，3 个引擎）

### 3.1 LogicFlowEngine（#111）

```python
class LogicFlowEngine:
    def register(self, flow: LogicFlow) -> LogicFlow: ...
    def get(self, flow_id: str) -> LogicFlow: ...
    def list(self, status: str | None = None) -> list[LogicFlow]: ...
    def update(self, flow_id: str, updates: dict[str, Any]) -> LogicFlow: ...
    def delete(self, flow_id: str) -> bool: ...
    def execute(self, flow_id: str) -> FlowExecution: ...
    """按 steps 顺序执行；每步成功推进；任意步失败整体 error"""
    def list_executions(self, flow_id: str | None = None, limit: int = 50) -> list[FlowExecution]: ...
```

**execute 流程**：
1. 取 flow，按 steps 顺序执行
2. 每步按 kind 分派：
   - compass_files_lister：返回 config.get("files", []) 列表
   - connector：返回 config.get("connection", "ok") 模拟连接
   - join：合并前步结果 list
   - transform：返回 config.get("transformed", "ok")
3. 步成功 → step_result.status=completed，步失败 → step_result.status=error + 整体 error
4. 200 条 execution 上限

### 3.2 AgentProxyEngine（#112）

```python
class AgentProxyEngine:
    def register(self, proxy: AgentProxy) -> AgentProxy: ...
    def get(self, proxy_id: str) -> AgentProxy: ...
    def list(self, status: str | None = None, agent_id: str | None = None) -> list[AgentProxy]: ...
    def update(self, proxy_id: str, updates: dict[str, Any]) -> AgentProxy: ...
    def delete(self, proxy_id: str) -> bool: ...
    def heartbeat(self, proxy_id: str) -> AgentProxy: ...
    """推进 last_heartbeat，status=online"""
    def drain(self, proxy_id: str) -> AgentProxy: ...
    """status=draining，拒绝新连接"""
    def forward_request(self, proxy_id: str, request: dict[str, Any]) -> dict[str, Any]: ...
    """检查 status=online，否则抛 PROXY_UNAVAILABLE；模拟转发返回 {forwarded, response}"""
```

**forward_request 流程**：
1. 取 proxy，校验 status=online
2. connections += 1
3. 模拟返回 {forwarded: True, response: {...}}
4. connections -= 1

### 3.3 AgentWorkerEngine（#113）

```python
class AgentWorkerEngine:
    def register(self, worker: AgentWorker) -> AgentWorker: ...
    def get(self, worker_id: str) -> AgentWorker: ...
    def list(self, status: str | None = None, agent_id: str | None = None) -> list[AgentWorker]: ...
    def update(self, worker_id: str, updates: dict[str, Any]) -> AgentWorker: ...
    def delete(self, worker_id: str) -> bool: ...
    def heartbeat(self, worker_id: str) -> AgentWorker: ...
    """推进 last_heartbeat，status=online"""
    def assign_job(self, worker_id: str, capability: str, payload: dict[str, Any]) -> WorkerJob: ...
    """校验 status=online + capability 在 capabilities 中 + 创建 WorkerJob"""
    def complete_job(self, job_id: str, result: dict[str, Any]) -> WorkerJob: ...
    """推进 status=completed"""
    def list_jobs(self, worker_id: str | None = None, status: str | None = None) -> list[WorkerJob]: ...
```

**assign_job 流程**：
1. 取 worker，校验 status=online，否则 WORKER_OFFLINE
2. 校验 capability in worker.capabilities，否则 CAPABILITY_NOT_SUPPORTED
3. 创建 WorkerJob，加入 worker.job_ids
4. 200 条 job 上限

### 3.4 单例与持久化

- 3 个引擎均用**双重检查锁单例**
- 内存态为主，各 200 条上限（logic flow 200 executions）

---

## 4. API 设计

文件：`aos_api/routers/logic_flows.py`（新增）

### 4.1 #111 Logic Flow

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/logic-flows` | 注册逻辑流 |
| GET | `/v1/logic-flows` | 列表 |
| GET | `/v1/logic-flows/{flow_id}` | 单条 |
| PUT | `/v1/logic-flows/{flow_id}` | 更新 |
| DELETE | `/v1/logic-flows/{flow_id}` | 删除 |
| POST | `/v1/logic-flows/{flow_id}/execute` | 执行 |
| GET | `/v1/logic-flows/executions` | 执行列表 |

### 4.2 #112 Agent Proxy

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/agent-proxies` | 注册代理 |
| GET | `/v1/agent-proxies` | 列表 |
| GET | `/v1/agent-proxies/{proxy_id}` | 单条 |
| PUT | `/v1/agent-proxies/{proxy_id}` | 更新 |
| DELETE | `/v1/agent-proxies/{proxy_id}` | 删除 |
| POST | `/v1/agent-proxies/{proxy_id}/heartbeat` | 心跳 |
| POST | `/v1/agent-proxies/{proxy_id}/drain` | 排空 |
| POST | `/v1/agent-proxies/{proxy_id}/forward` | 转发请求 |

### 4.3 #113 Agent Worker

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/agent-workers` | 注册 Worker |
| GET | `/v1/agent-workers` | 列表 |
| GET | `/v1/agent-workers/{worker_id}` | 单条 |
| PUT | `/v1/agent-workers/{worker_id}` | 更新 |
| DELETE | `/v1/agent-workers/{worker_id}` | 删除 |
| POST | `/v1/agent-workers/{worker_id}/heartbeat` | 心跳 |
| POST | `/v1/agent-workers/{worker_id}/jobs` | 分配任务 |
| POST | `/v1/agent-workers/jobs/{job_id}/complete` | 完成任务 |
| GET | `/v1/agent-workers/jobs` | 任务列表 |

---

## 5. 集成点

### 5.1 main.py（最小更改）

```python
from aos_api.routers import (..., logic_flows, ...)
application.include_router(logic_flows.router)
```

---

## 6. 测试计划

文件：`tests/test_logic_flows.py`（新增，约 45 个用例）

### 6.1 LogicFlowEngine（15）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 缺 name | MISSING_NAME |
| 3 | register 未知 step kind | INVALID_STEP_KIND |
| 4 | get 未找到 | NOT_FOUND |
| 5 | list 默认 | 列表 |
| 6 | list 按 status 过滤 | 仅匹配 |
| 7 | update | 修改后返回新值 |
| 8 | delete | 删除成功 |
| 9 | execute compass_files_lister | status=completed, step_results 含 files |
| 10 | execute connector | status=completed |
| 11 | execute join | status=completed |
| 12 | execute transform | status=completed |
| 13 | execute 多步链 | status=completed, 步骤数正确 |
| 14 | execute 步骤异常 | status=error |
| 15 | list_executions 200 条上限 | 旧记录淘汰 |

### 6.2 AgentProxyEngine（14）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 缺 name | MISSING_NAME |
| 3 | register 缺 agent_id | MISSING_AGENT |
| 4 | get 未找到 | NOT_FOUND |
| 5 | list 默认 | 列表 |
| 6 | list 按 status 过滤 | 仅匹配 |
| 7 | update | 修改后返回新值 |
| 8 | delete | 删除成功 |
| 9 | heartbeat | status=online, last_heartbeat 推进 |
| 10 | drain | status=draining |
| 11 | forward_request online | forwarded=True |
| 12 | forward_request offline | PROXY_UNAVAILABLE |
| 13 | forward_request draining | PROXY_UNAVAILABLE |
| 14 | list 按 agent_id 过滤 | 仅匹配 |

### 6.3 AgentWorkerEngine（14）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 缺 agent_id | MISSING_AGENT |
| 3 | get 未找到 | NOT_FOUND |
| 4 | list 默认 | 列表 |
| 5 | list 按 status 过滤 | 仅匹配 |
| 6 | update | 修改后返回新值 |
| 7 | delete | 删除成功 |
| 8 | heartbeat | status=online |
| 9 | assign_job 成功 | job_id 加入 worker.job_ids |
| 10 | assign_job offline | WORKER_OFFLINE |
| 11 | assign_job capability 不匹配 | CAPABILITY_NOT_SUPPORTED |
| 12 | complete_job | status=completed |
| 13 | complete_job 已完成 | ALREADY_COMPLETED |
| 14 | list_jobs 按 worker_id 过滤 | 仅匹配 |

### 6.4 单例（3）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | flow 单例 | 同一实例 |
| 2 | proxy 单例 | 同一实例 |
| 3 | worker 单例 | 同一实例 |

---

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 逻辑流步骤异常 | 单步失败 → 整体 error，记录 step_results |
| 代理状态漂移 | heartbeat 推进 status=online |
| Worker 误分配 | assign_job 校验 status=online + capability 匹配 |
| 重复 complete_job | ALREADY_COMPLETED 错误码拦截 |
| 代理转发失败 | forward_request 检查 status，非 online 抛 PROXY_UNAVAILABLE |

---

## 8. 交付物清单

| 路径 | 状态 | 说明 |
| --- | --- | --- |
| `docs/palantier/20_tech/220tech_w2-af-logic-flows.md` | ✅ 本文件 | 微规约 |
| `aos_api/logic_flows.py` | ⬜ 待编码 | 3 引擎 |
| `aos_api/routers/logic_flows.py` | ⬜ 待编码 | ~24 端点 |
| `tests/test_logic_flows.py` | ⬜ 待编码 | ~45 用例 |
| `aos_api/main.py` | ⬜ +2 行 | import + include_router |

---

*v1.0 · w2-af*

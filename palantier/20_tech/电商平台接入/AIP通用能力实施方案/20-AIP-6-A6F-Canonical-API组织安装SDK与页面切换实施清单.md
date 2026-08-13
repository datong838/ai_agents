# AIP-6 A6F Canonical API、组织安装、SDK 与页面切换实施清单

> 状态：`APPROVED_FOR_IMPLEMENTATION`
> 日期：2026-08-13
> 唯一代码分支：`aos-platform/m1`
> 上位门：A6E `IMPLEMENTED_GREEN / DEFINITION_AUTHORITY_READY / RUNTIME_READINESS_BLOCKED`
> 唯一真实业务范围：`org-org / dev-project`
> 负向隔离 canary：`dev-org / dev-project`

## 1. 使用的 Rules

1. 先方案、评审、整改、复审，再编码；页面必须经内置浏览器真实点击验收。
2. PostgreSQL revision、tenant instance、binding、receipt 是唯一权威；Bundle 和前端不得成为第二真源。
3. A6F 只安装六个组织级 AgentInstance；37 个 SkillTemplate 仍为 `evaluated`、10 个 Capability 仍为 `blocked`，不得伪造 SkillBinding、CapabilityBinding、在线状态或调用量。
4. 所有 API 必须使用 `Principal` 派生 `org_id/project_id/actor`；禁止接受客户端覆盖租户。
5. 安装必须幂等、可审计、失败关闭。六实例必须逐个产生既有 durable RegistryReceipt；同 key 漂移必须冲突。
6. 旧进程内 singleton 只允许在明确的兼容边界内保留；目录、实例、readiness 的正式页面不得再读取它。
7. 只做 additive、最小改动，不提前实现 AIP-7 Route、E7 记忆投影、W0B 公共生产对象或 AIP-9 内容生产。

## 2. 实时代码差异

| 能力 | 当前事实 | A6F 裁决 |
|---|---|---|
| Agent/Skill/Capability 定义 | PostgreSQL 已精确发布 6/37/10 | 只读 exact revision/hash，禁止读 Bundle 运行 |
| AgentInstance | Store 已有 create/get/list/update 与 Receipt | 新增六角色安装服务；不另造安装表 |
| Skill/Capability Binding | Store 已存在；Skill 非 published、Capability blocked | 不创建，UI 明示阻断 |
| `/v1/aip/agents` | 无 Principal，读写 `aip_agents_engine` singleton | 切换为 tenant AgentInstance Canonical API |
| `/v1/aip/agent-registry` | 虽有 Principal，仍读 `aip_capabilities_engine` singleton | 切换为全局定义 + 当前 tenant 实例/readiness 聚合投影 |
| 能力页面 | 静态四卡 + 可写 singleton/本地存储路径 | A6F 只提供 10 类 canonical 只读目录；配置动作失败关闭 |
| 前端数据访问 | 页面各自松散解析 | 新增唯一严格 SDK，禁止 silent fallback/mock |

## 3. A6F Canonical 资源与 API

### 3.1 只读目录

- `GET /v1/aip/agent-registry`
  - 返回 6 个已发布 `AgentTemplate`；每项附当前租户对应 `AgentInstance`（若有）、角色、37 Logic 子集、required capability、template exact ref/hash、instance 状态和 blocker。
  - 汇总必须区分 `definitionCount`、`installedCount`、`runnableCount`；本波预期 6/6/0。
- `GET /v1/aip/capability-catalog`
  - 返回 10 个 `CapabilityRevision` 及 alias/readiness/reasons；本波预期 10/0 available。

### 3.2 组织实例

- `GET /v1/aip/agents`
  - 只返回 Principal tenant 的 AgentInstance；支持稳定排序，不返回 singleton 指标。
- `GET /v1/aip/agents/{instance_id}`
  - 返回 exact instance/template refs、overlay、状态、技能/能力 readiness；跨租户按 not-found 失败关闭。
- `POST /v1/aip/agents/install-ecommerce`
  - Header `Idempotency-Key` 必填；只安装 `solution.ecommerce.growth@1.2.0` 发布的六角色 revision 1。
  - 稳定 instance ID：`ecommerce.data_advisor.default`、`ecommerce.content_officer.default`、`ecommerce.shopping_advisor.default`、`ecommerce.customer_service.default`、`ecommerce.private_domain_manager.default`、`ecommerce.campaign_planner.default`。
  - overlay 仅写中文 display name 和空 capability allowlist；初态 `provisioning`。没有 Skill/Capability binding 时不得转 active。
  - 每个 instance 使用派生子 key `{Idempotency-Key}:{templateId}` 调既有 Store；重放返回相同 Receipt。

### 3.3 旧写入口

- `POST /v1/aip/agents` 以及 prompt/tools/guardrails 写入口在本波返回稳定 `409 AIP_LEGACY_AGENT_WRITE_RETIRED`，不得再写 singleton。
- 旧 prompt/tools/guardrails 读入口返回 `409 AIP_CANONICAL_OVERLAY_NOT_IMPLEMENTED`，不得把历史 singleton 值冒充组织配置。
- `PUT /v1/aip/capabilities/{id}`、`POST /v1/aip/capabilities/test` 返回 `409 AIP_CAPABILITY_BINDING_REQUIRED`；A6F 不允许绕开 CapabilityBinding/secretRef/provider readiness。

## 4. Store 与聚合服务

1. `AipAgentRegistryStore.list_templates(...)`：按 source resource/version、lifecycle、limit 稳定排序，返回全局 immutable revision。
2. `AipSkillRegistry.list_skills(...)`：按 source 和 lifecycle 列出 37 definition；只用于目录投影。
3. `AipCapabilityRegistry.list_capabilities(...)`：稳定返回 10 definition 与 readiness。
4. `AipEcommerceAgentInstaller`：
   - 从 PostgreSQL 模板 source exact ref 发现六角色；校验 ID 集合、revision/hash、published lifecycle；
   - 在当前 tenant 内逐一 get/create；已存在但 template/hash/overlay 不符时冲突，不静默覆盖；
   - 返回六个 instance 与六个 receipt/replay 状态；任一异常整批不宣称完成。
5. `AipAgentCatalogService`：聚合 template、skill、capability 与 tenant instance；只计算 readiness，不持久化派生状态。

## 5. 唯一 TypeScript SDK 与页面

新增 `apps/web/src/api/aipAgentControl/`：

- 严格 DTO 与 runtime parser；未知必填字段、非法状态、缺 tenant/ref/hash 均失败；
- `listCatalog()`、`listInstances()`、`getInstance()`、`installEcommerce()`、`listCapabilities()`；
- 所有写请求显式携带 idempotency key；无本地 mock、localStorage authority 或默认假数据。

页面切换：

1. `智能体目录`：展示六个 definition、当前组织安装状态、Logic 数、required capability 与 blocker；提供“安装电商六数字同事”一次动作。
2. `智能体列表/对话机器人`：展示当前 tenant 六实例及 `provisioning / blocked`；旧试运行、提示词、工具和护栏修改入口禁用并说明后续门。
3. `能力目录`：替换四张静态能力卡为 10 类 canonical capability；展示 published definition 与 blocked readiness，配置/连通测试禁用。
4. 不展示静态“调用量、成功率、活跃 Agent、护栏覆盖率”；没有 AgentRun 真数据时明确为未运行。

## 6. 开发任务

| ID | 任务 | 主要文件 | 验收 |
|---|---|---|---|
| A6F-01 | Store list 能力 | `aip_*_registry*.py` | source/lifecycle/filter/排序/失败关闭 |
| A6F-02 | 安装与聚合契约 | `aip_agent_control_contracts.py` | 严格 DTO、6/37/10、readiness 分层 |
| A6F-03 | 六角色安装服务 | `aip_ecommerce_agent_installer.py` | 六 Receipt、重放、漂移冲突、无 Binding |
| A6F-04 | Canonical 路由 | `phase3_aip_agents.py`、`phase3_aip_capabilities.py` | Principal tenant、错误码、OpenAPI 唯一 |
| A6F-05 | 后端测试 | `tests/test_aip6_*` | 正向、重放、跨租户、旧入口失败关闭 |
| A6F-06 | 唯一前端 SDK | `apps/web/src/api/aipAgentControl/` | parser、错误、idempotency 定向测试 |
| A6F-07 | 三页面切换 | `AgentRegistryPage.tsx`、`AgentsPage.tsx`、`CapabilityPage.tsx` | 无 mock/singleton，状态诚实，按钮有效或禁用有因 |
| A6F-08 | 浏览器与封板 | evidence + 01/06/16 | `org-org` 正向、`dev-org` canary、console 0 error |

## 7. 测试与证据矩阵

### 7.1 后端

- 空 tenant 为 0 instance；模板目录仍是全局 6 definition；
- `org-org/dev-project` 首装为 6 create、重放为 6 replay，实例 exact ref/hash 一致；
- `dev-org/dev-project` 仍为 0，不能读取 org-org 实例；
- 缺/复用漂移 Idempotency-Key、模板缺失/非 published、DB 漂移均稳定失败；
- 安装后 SkillBinding=0、CapabilityBinding=0、AgentRun=0；runnableCount=0；
- legacy write/test 不再改变 singleton；OpenAPI 没有重复 operation/path。

### 7.2 前端与浏览器

- SDK parser/tenant/ref/readiness/错误回归；TypeScript 与 production build GREEN；
- `org-org/dev-project` 安装前后目录与实例页面一致，安装按钮重放无重复；
- 6 个中文角色可见，37 Logic 总数和各角色计数正确，10 capability 均显示真实 blocker；
- 所有不可执行动作禁用且有原因；刷新后状态来自后端；控制台 0 error；
- `dev-org/dev-project` canary 为 0 instance，不展示 org-org 数据。

## 8. 风险、回滚与非目标

- **原子性风险**：既有 Store 每实例独立事务。A6F 返回逐项结果；若中途失败，重放继续完成，但在六项全齐前整体状态为 `partial/blocked`，不得宣称 installed。后续如需数据库单事务安装，独立 ADR 处理。
- **前端旧功能回退**：旧 singleton 编辑被关停是 authority 修复；如仍有消费方，显示明确迁移提示，不恢复隐式写。
- **真实租户副作用**：本波唯一授权业务写是 `org-org/dev-project` 六个 provisioning AgentInstance 及 Receipt；不写订单、知识正文、Binding、Run。
- **不在本波**：Skill/Capability 激活、Provider/secret、AIP-7 Route、E7 记忆、TaskBrief/W0B、真实对话运行。
- 回滚代码不删除已创建实例；实例属于审计数据。必要时经独立受控状态迁移到 deleted，不做物理删除。

## 9. 评审—整改—复审

### 9.1 首轮评审发现

| ID | 发现 | 初判 |
|---|---|---|
| R1 | 若 A6F 同时创建 37 SkillBinding，会绕过 `evaluated → published` 门 | BLOCKER |
| R2 | “安装成功”若只按请求返回，六个独立事务可能出现 partial | BLOCKER |
| R3 | 旧 singleton 写入口与新 authority 并存会形成双写 | BLOCKER |
| R4 | 前端若继续展示调用量/在线率会把 0 Run 伪装成 operational | BLOCKER |
| R5 | 直接读 Bundle 安装会使运行绕开 PostgreSQL revision authority | BLOCKER |
| R6 | dev-org 若被自动安装会污染隔离 canary | BLOCKER |

### 9.2 整改

- 安装范围收窄为六个 provisioning AgentInstance，Binding/Run 全部为 0；
- 明确逐项 Receipt、partial/blocked 与可恢复重放语义；
- 旧 singleton 写和 capability test 失败关闭；
- 页面删除静态运行指标，定义状态与运行 readiness 分栏；
- 安装器只读 PostgreSQL exact source/revision/hash；
- 真实安装只对 `org-org/dev-project` 执行，`dev-org` 仅做 0 数据 canary。

### 9.3 第二轮复审

| 退出门 | 结果 |
|---|---|
| Authority 唯一且不读 Bundle 运行 | PASS |
| 6 definition / 6 instance / 37 evaluated / 10 blocked 状态不混淆 | PASS |
| Principal tenant 与 canary 边界明确 | PASS |
| 幂等、Receipt、partial 和漂移失败关闭 | PASS |
| singleton 双写和假运行指标消除 | PASS |
| SDK/UI/浏览器验收可执行 | PASS |
| 未越过 AIP-7/E7/W0B/AIP-9 | PASS |

最终评审结论：`APPROVED_FOR_IMPLEMENTATION`。

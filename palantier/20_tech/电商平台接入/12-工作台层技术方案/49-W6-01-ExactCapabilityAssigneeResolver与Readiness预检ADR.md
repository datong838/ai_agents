# W6-01 Exact Capability、Assignee Resolver 与 Readiness 预检 ADR

> 日期：2026-08-14
> 核查基线：Workshop `w2-workshop@b368821`，authority `AOS-000027`
> 状态：`IMPLEMENTATION_IN_PROGRESS / UPSTREAM_GAPS_RECHECKED / NO_EXTERNAL_EFFECT`
> 边界：只读代码、资产、专项测试与方案整改；未修改 AIP/Workshop 源码、迁移、真实租户或外部 Provider

## 1. 结论

六数字同事 6/6、Logic 37/37、共享 Capability 10/10 的定义目录与 crosswalk 完整，Logic 的 Agent/Capability 引用 0 缺失；ResponsibilityPlan、AgentInstance、SkillBinding、CapabilityBinding 也有可信的 PostgreSQL authority 基础。但“目录存在”不等于“职责可分配”：正式生产 Router 未注入 ResponsibilityTemplateResolver，八 Module 的 `responsibilityTemplateRefs` 全为空，也没有 canonical assignee resolver。

专项测试进一步发现 `solution.ecommerce.growth` 已升级为 1.3.0，而 AIP publisher 仍硬编码只接受 1.2.0，导致当前目录安装 API 自身回归失败。后端结果为 25 passed / 1 failed，前端 16 tests GREEN。因此 W6-01 保持未勾选。

## 2. 唯一职责解析链

W6-01 不创建领域本地 Agent roster 或“六人固定排班”。输入是 frozen `ResponsibilityTemplateRevision`、职责槽、required exact Capability refs、TenantScope、任务 purpose/marking、组织策略、候选 binding 与当前运行健康；输出为不可变 `AssigneeResolutionReceipt`：

```text
ResponsibilitySlot exact ref
  + CapabilityRevision exact refs
  + candidate Assignee exact refs
  + candidate Binding exact refs
  + policy/freshness/capacity snapshot
  -> selected AssigneeBinding exact ref | uncovered/blocked
```

Resolver 必须确定性排序并记录候选集合、拒绝 reasonCodes、选择依据、policy revisions、observedAt/expiry 与内容 hash。调用者只能提供业务约束，不能直接指定一个 assignee 后让服务端补盖 readiness。

## 3. 四类 Assignee

统一支持并各有 authority resolver：

| kind | 必须验证 |
|---|---|
| HumanPrincipal | tenant membership、角色/ABAC、值班/容量、职责分离、有效期 |
| DigitalColleague/AgentInstance | active exact instance/template、SkillBinding、CapabilityBinding、policy、model/route/provider、health/freshness/capacity |
| ToolBinding | 工具 revision、permission/purpose、input/output schema、网络/Secret、health/capacity |
| ProviderCapabilityBinding | provider/account/capability/Adapter exact refs、quota/rate/budget、network/Secret、health/freshness |

当前 DTO 虽公开 human/tool/provider 类型，后端却对非 `agent_instance` 全部返回 `ASSIGNEE_AUTHORITY_UNAVAILABLE`。目标实现要么完整支持上述 kind，要么从当前发布合同中移除未实现类型；不得前端声称支持、后端永久拒绝。

## 4. Exact capability 与归属

readiness 不能把 Capability ref 降成裸字符串 ID。每个 required capability 必须绑定 `CapabilityRevision + CapabilityBinding + AssigneeBinding + policy revisions`，并复验 revision/hash/lifecycle/readiness/health/observedAt/expiry。

租户内存在任意 active healthy CapabilityBinding，不代表每个 Agent 都能使用它。Binding 必须明确授权给 assignee/账号/工具/Provider，并受 purpose、marking、网络、Secret、quota、预算、并发和地域约束。SkillBinding 声明“需要什么”，CapabilityBinding/AssigneeBinding 证明“该执行者当前可以用什么”，二者不能靠同名 ID 猜交集。

## 5. Freeze、执行与变更

ResponsibilityPlan draft 可展示 unresolved candidates；freeze 必须做到全部 required slot 在结构上 covered，独立审核/合规/批准/结果对账职责满足 separation policy，且 template/assignee/capability/binding 全部 exact。但 `coverage=complete` 不是 operational-ready：执行前必须由独立 `AssigneeResolutionReceipt` 固定候选、拒绝 reasonCodes、选中 AssigneeBinding、policy、health、capacity、observedAt 与 expiry；任一 drift 使 Stage blocked，不静默换人、换账号或换 Provider。

reassign 与人工接管不能合并为一个“修改 owner”动作。TaskRun 创建前，reassign 创建显式 successor ResponsibilityPlanRevision，保存 supersedes、Diff、来源/目标 binding、原因、actor 与 CAS；冻结版本不可原地修改。TaskRun/Stage attempt 创建后，人工接管创建独立 TakeoverDecisionReceipt 与新的 execution assignment lease/fence，保存 Handoff/Checkpoint、未完成输入输出、审批、Provider unknown/reconcile 状态与影响范围。Generic Handoff 只传上下文，不自动改写 Responsibility 或 execution ownership authority。W3-07 的冻结边界见 `95-W3-07职责覆盖Readiness改派与人工接管分层预检ADR.md`。

## 6. 当前缺口与施工顺序

1. 先解决 `solution.ecommerce.growth@1.3.0` 与 publisher 1.2.0 的版本漂移，并重跑目录发布/安装/隔离测试；该文件属于 AIP owner，不在 W2 Workshop 分支跨线修复。
2. W3-02 发布八 Module 签名 ResponsibilityTemplate refs，并由 installation lock exact resolver 装配正式 Router。
3. W3-07 实现 canonical assignee resolver、coverage、reassign 与人工接管 authority。
4. W6-01 只在前述依赖 GREEN 后补充电商职责模板与候选约束，不复制 L0 Store。

## 7. 验收

- 6/37/10 与八 Module crosswalk 精确，alias 不生成第二 capability identity；
- 四类 assignee 的正/负向 authority、exactness、tenant、permission、freshness 与 capacity 测试齐全；
- tenant-wide unrelated binding 不能错误点亮某个 assignee；
- suspended/revoked/stale Agent、Skill、Capability、Binding 在 freeze 和 execute 均失败关闭；
- 同输入/同 snapshot 解析结果确定且 Receipt hash 一致；并发 reassign 用 CAS；
- `dev-org/dev-project` 对 `org-org/dev-project` 的 template、candidate、binding 与 Receipt 0 可见；
- 当前 1.3.0 Bundle 的 canonical publish/install/readback 重新 GREEN。

机器证据见 `.evidence/workshop/2026-08-14-w6-01-exact-capability-assignee-readiness-preflight.json`。

## 8. 2026-08-25 实时差异复核与实施清单

旧预检冻结的是 `2026-08-14@AOS-000027` 事实，不能继续作为当前阻断结论。以 `m1@696b3f5`、authority `AOS-000243` 重新核验后：

1. `AipSolutionPackPublisher` 已接受 `solution.ecommerce.growth@1.3.0`，定义源版本与 Bundle 版本已经解耦；
2. 正式 Production Contract Router 已注入 `resolve_responsibility_template`，并通过租户 active installation、composition lock、签名、artifact digest 与 immutable release mirror 解析 exact artifact；
3. `solution.ecommerce.growth@1.4.0` 与 `solution.ecommerce.operations-base@1.2.0` Candidate 已让八个正式 Module 各引用一个 production profile / responsibility template artifact；Candidate 存在不等于已安装或 operational；
4. `aip13_001` 已有 tenant-scoped `ToolBinding` 与 `AssigneeResolutionReceipt`，`w3_016` 已有 CAS successor plan、人工接管与 resolution receipt 前置门；
5. 仍未闭合的真实缺口是：现有 `/resolutions` 由调用方指定单个 assignee；Receipt 未固化 required exact Capability、candidate/rejection、binding/policy/freshness snapshot；HumanPrincipal 只检查非空；AgentInstance 未检查 active、template、SkillBinding、exact CapabilityBinding 与 freshness；Production ResponsibilityPlan 仍拒绝非 `agent_instance`。

因此本波不重复创建第二套 Registry、Responsibility 或 Takeover authority，采用兼容增强：保留旧单候选请求与 Receipt 字段，新增 canonical candidate resolver 和不可变 snapshot 字段；旧消费者继续可读，新消费者只以服务端选出的 `selectedAssignee` 与 snapshot hash 判断 readiness。

### 8.1 文件级最小改动

- `services/aos-api/aos_api/aip_assignee_resolution.py`
  - 新增 exact capability、候选约束、候选判定和 resolution snapshot DTO；
  - 兼容旧 `ResolveAssigneeRequest.assignee`，新增 `candidates` 时禁止空集合和重复 exact ref。
- `services/aos-api/aos_api/aip_assignee_resolution_store.py`
  - 服务端逐候选读取 tenant authority，按 `kind/resourceId/version` 确定性排序；
  - Agent 必须 active，并以其 active SkillBinding 指向的 CapabilityBinding 覆盖 required exact Capability；
  - Tool 必须 instance-scoped；Provider Binding 必须 active、healthy、operational 且 readiness 未过期；Human 必须是当前 workspace 成员；
  - Receipt 固化全部候选、拒绝 reasonCodes、选中 binding、policy refs、observedAt/expiresAt 与 snapshot hash；无候选可用时只产 blocked Receipt。
- `services/aos-api/aos_api/aip_production_contract_store.py`
  - 创建/修订 ResponsibilityPlan 时复用四类 authority 检查；不得再把公开合同中的三类 assignee 永久拒绝；
  - coverage 继续失败关闭，非 Agent 类不伪造 SkillBinding readiness，必须依赖 canonical resolved Receipt。
- `services/aos-api/alembic/versions/w6_001_exact_assignee_resolution.py`
  - 仅 additive 增加 Receipt snapshot JSON/hash 与 freshness 列，保持单 Alembic head、RLS 与不可变 Receipt 语义。
- `services/aos-api/tests/aip/test_w6_01_exact_assignee_resolution.py`
  - 覆盖四类正负向、确定性排序、exact capability/hash、stale/disabled、tenant isolation 与稳定 snapshot hash。
- `services/aos-api/tests/test_w2b_production_contract_store.py`
  - 覆盖非 Agent assignee 必须有 canonical Receipt，且 unrelated tenant-wide binding 不得点亮职责槽。
- `.evidence/workshop/2026-08-25-w6-01-exact-capability-assignee-readiness.json`
  - 固化专项、累计、迁移、OpenAPI、租户隔离和无外部副作用结果。

### 8.2 兼容与安全门

- 旧 Receipt 字段不删除；新增字段只 additive，旧 Task Cockpit parser 不因新增字段失败；
- 不迁移历史 Receipt 内容，不回填猜测 snapshot；旧 Receipt 仅保留历史可读性，不能冒充新 exact readiness；
- 不激活任何 Agent/Skill/Capability/Tool/Provider Binding，不写真实租户业务数据，不调用 Provider；
- Candidate Bundle 只做静态/测试解析，不发布、不安装、不升级；
- 相同 tenant、subject、required capabilities、candidate authority snapshot 必须得到相同 selected ref 与 snapshot hash；任何 freshness、version、hash、status 或 tenant 漂移均失败关闭。

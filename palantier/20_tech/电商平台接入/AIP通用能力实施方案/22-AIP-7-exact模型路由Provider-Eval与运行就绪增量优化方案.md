# AIP-7 exact 模型路由、Provider、Eval 与运行就绪增量优化方案

> 版本：v1.0
> 评审日期：2026-08-13
> 状态：`APPROVED_FOR_INCREMENTAL_IMPLEMENTATION / EXTERNAL_PROVIDER_GATE_RETAINED`
> 适用分支：`aos-platform/m1`
> 唯一真实业务范围：`org-org / dev-project`
> 负向隔离 canary：`dev-org / dev-project`
> 性质：对 09 号 AIP-7 基线的 additive authority 与实施顺序补强；不重设计 AIP，不授权读取、复制或启用其他租户的 Provider/模型/凭据。

## 0. 使用的 Rules

1. 代码、迁移、数据库回读、HTTP、浏览器和不可变 Receipt 才是完成证据；旧页面、默认配置、测试种子和历史 mutable 表不是运行权威。
2. 复用 AIP-4 Eval/Usage、AIP-6 Agent/Skill/Capability/Run 与现有租户隔离底座，不复制 Eval、Usage、AgentRun 或 Secret 真源。
3. 新能力只做 additive migration；旧 mutable Provider/Catalog/Route 保留为兼容发现或迁移输入，不再作为 AgentRun exact authority。
4. 凭据只允许 `secretRef + version`，不得把明文、masked key、进程环境或 Prime/AGNES 本机凭据转成 AOS 生产凭据。
5. `org-org/dev-project` 当前模型链真实为空；不得从 `dev-org/dev-project` 自动回填 4 Provider、12 Catalog、6 RegisteredModel、5 Route。
6. Provider、Eval、Policy、容量、价格任一 unknown 都失败关闭；不得用默认模型、静态在线、0 成本或 fallback 冒充 readiness。
7. 每个子波独立完成 DTO、migration、Store、API、SDK、测试、双租户 canary、浏览器和提交；没有真实外部 Provider 时允许 `CODE/CONTROL_GREEN + PROVIDER_BLOCKED`，不伪造 operational GREEN。

## 1. 评审结论

### 1.1 总体判断

AIP 主架构不需要重设计。09 号方案的 Provider → Model → Route → AgentRun → Usage/Cost 主链正确；当前缺口是其尚未适配 AIP-4/AIP-6 已冻结的 exact revision/hash 合同，也没有把 `PolicyRevision` 作为 AgentRun 的共同运行门。

因此采用以下最小裁决：

- 旧表负责兼容发现和历史只读；
- 新增不可变 exact authority 负责新运行；
- AIP-4 继续拥有 Eval/Usage/Lineage；
- AIP-6 继续拥有 AgentRun/Binding；
- AIP-7 只拥有 Provider/RegisteredModel/Route/RuntimePolicy 的模型运行权威、解析与容量预留；
- 外部调用通过统一 adapter，结果回写 AIP-4 Receipt/Usage/Lineage。

### 1.2 实时事实

| 事实 | `org-org/dev-project` | `dev-org/dev-project` | 裁决 |
|---|---:|---:|---|
| `model_provider` | 0 | 4 | 后者仅历史测试数据，不迁移 |
| `model_catalog` | 0 | 12 | 只作旧发现目录，不是 exact authority |
| `registered_models` | 0 | 6 | mutable，不可被 AgentRun 引用 |
| `model_route` | 0 | 5 | mutable，不可被 AgentRun 引用 |
| `provider_health` | 0 | 4 | 探测记录不等于 Eval/运行就绪 |
| `aip_eval_suite_revision` | 0 | 0 | 复用 AIP-4 authority，真实 Eval 仍 blocked |
| Skill/Capability Binding/AgentRun | 0/0/0 | 0/0/0 | 运行未开始 |

### 1.3 现有实现的四个 blocker

1. `model_route` 可原地 upsert/delete，只有 ID，没有 immutable revision/content hash。
2. `model_router_v2` 存在全局 `meta_aip_kv`，并能从默认规则迁移；它不是 Principal tenant authority。
3. `model_provider`/`registered_models` 可原地覆盖，Provider 还保留 `api_key_masked` 旧字段；无法证明 secret version、模型能力和撤销时点。
4. `AgentRun` 已要求 exact `ModelRouteRevision` 与 `PolicyRevision`，但 transition 到 `running` 当前固定失败关闭；这正是正确保护，不得绕过。

## 2. 唯一 ownership 与真源裁决

| 对象 | 唯一 owner | 本方案形态 | 禁止事项 |
|---|---|---|---|
| Provider 插件 manifest | Apollo/FDE 全局资产 | exact global ref，只读引用 | AIP 复制插件包 |
| ProviderInstanceRevision | AIP-7 | 新增租户不可变 revision + head | 原地改 base URL/secret |
| ProviderHealthObservation | AIP-7 | append-only observation | 探测成功等于质量通过 |
| ModelCatalogItem | Provider manifest/发现源 | 兼容发现投影 | 直接作为运行模型 |
| RegisteredModelRevision | AIP-7 | 新增租户不可变 revision + head | mutable quota/status 作为 exact ref |
| ModelRouteRevision | AIP-7 | 新增工作区不可变 revision + alias/head | KV 默认规则、旧 route 成为真源 |
| RuntimePolicyRevision | AIP-7/L0 policy | 新增不可变运行 policy | 字符串 policy_revision 冒充 exact ref |
| EvalSuite/Run/Report/Gate | AIP-4 | 直接复用 exact authority | AIP-7 另建 Eval 表/结果 |
| CapabilityBinding/SkillBinding/AgentRun | AIP-6 | 直接复用 | Router 创建第二 Run/Binding |
| UsageReceipt/Adjustment/Lineage | AIP-4 | 直接复用 | Provider usage 覆盖原 Receipt |
| Secret payload | Secret backend | AIP 仅存 secretRef/version | DB、日志、页面、Receipt 保存明文 |

## 3. Canonical exact 合同

### 3.1 ProviderInstanceRevision

必须包含：

- `providerInstanceId/revision/contentHash`；
- exact `pluginRef`；
- `endpointProfile`，只允许受审字段，不含 secret；
- `secretRef/secretVersion`；
- `egressPolicyRef/dataClassificationPolicyRef`；
- lifecycle：`draft → validated → active → suspended/revoked`；
- revision 不可变，状态改变追加 revision；head 用 expected revision CAS 推进。

### 3.2 RegisteredModelRevision

必须包含：

- exact ProviderInstanceRevision；
- provider model ID、能力集合、输入/输出 modality、context window；
- 数据出境、PII、region、license；
- quota/budget/price snapshot exact refs；
- exact AIP-4 Eval gate ref；
- lifecycle 与 content hash。

没有真实模型发现或人工核准时不得创建 active revision。

### 3.3 ModelRouteRevision

必须包含：

- `routeId/revision/contentHash`；
- task/skill/capability applicability；
- ordered candidate refs，每个候选为 exact RegisteredModelRevision；
- strategy、deadline、fallback 条件、kill switch；
- exact RuntimePolicyRevision；
- exact Eval gate 下限；
- capacity/budget policy refs；
- route lifecycle 与 alias/head。

安全拒绝、数据出境不符、PII 不符、能力/质量下限不符不可 fallback。

### 3.4 RuntimePolicyRevision

作为 AgentRun `policy` 的 L0 exact authority，至少包含：

- network/egress/data classification；
- quota/budget/deadline/max attempts；
- allowed fallback reasons；
- unknown usage/price/provider state 的处理；
- kill switch 与人工审批门；
- revision/hash/lifecycle。

Memory/Handoff/License/Budget 等领域细分 Policy 仍由原 owner 管理；本对象只把一次模型运行需要的 policy exact 冻结成统一引用，不复制它们的正文。

## 4. 运行解析与状态机

```text
AgentRun queued
  → 校验 Task/Plan/Instance/Skill/Logic exact refs（AIP-6）
  → 校验 ModelRouteRevision + RuntimePolicyRevision exact refs（AIP-7）
  → 解析 candidate RegisteredModelRevision
  → 校验 Provider active + health freshness + Eval gate + egress/PII
  → 原子 capacity reservation
  → queued → running
  → provider adapter 调用
  → AIP-4 UsageReceipt + Lineage + CapabilityReceipt
  → consume/release/late adjustment
  → AgentRun terminal/unknown/reconcile
```

任一步 unknown 或 drift 均保持 queued/blocked，不允许“先运行再补证据”。

## 5. 旧实现的迁移与退役边界

### 5.1 保留

- `model_catalog`：只读发现投影；
- `model_provider`、`registered_models`、`model_route`：历史兼容读取和显式人工迁移输入；
- `model_router_v2/meta_aip_kv`：旧页面兼容投影，标记 deprecated；
- 既有 capacity 页面：逐步切换新聚合，不重做视觉骨架。

### 5.2 禁止自动升级

旧行没有 secret exact version、Eval gate、policy hash 和审批证据，不能批量升级为 active exact revision。仅允许用户在当前租户显式选择一条旧配置，经过校验/预览/审批后产生新 revision 和 Receipt。

### 5.3 正式路由收口

- Canonical API 只读写新 authority；
- 旧写 API 返回稳定 `AIP_MODEL_LEGACY_WRITE_DISABLED`，不得双写；
- 旧页面可显示 migration-required，但不能显示 runnable；
- SDK、AgentRun resolver、试聊、TAOR、Logic DryRun、Eval、ResearchJob 共用一个 resolver。

## 6. 实施波次

### A7-0 · Authority ADR 与合同冻结

文件：

```text
services/aos-api/aos_api/aip_model_runtime_contracts.py
services/aos-api/tests/aip/test_aip_model_runtime_contracts.py
```

只冻结 DTO/校验/错误码，不注册路由、不写库。

### A7-1 · PostgreSQL exact authority

文件：

```text
services/aos-api/alembic/versions/aip7_001_model_runtime_authority.py
services/aos-api/aos_api/aip_model_runtime_store.py
services/aos-api/tests/aip/test_aip7_model_runtime_migration.py
services/aos-api/tests/aip/test_aip_model_runtime_store.py
```

新增 Provider/Model/Route/Policy revision/head、health observation、command receipt；租户表 RLS/FORCE RLS、复合 FK、append-only、CAS、幂等。不得修改 `228ti5b1models` 历史迁移。

### A7-2 · Eval/readiness resolver

文件：

```text
services/aos-api/aos_api/aip_model_runtime_resolver.py
services/aos-api/tests/aip/test_aip_model_runtime_resolver.py
```

复用 AIP-4 suite/report/gate/publication、Provider health freshness、model capability、egress/PII 和 policy；输出 resolved/blocked/unknown 及机器可读原因，不调用模型。

### A7-3 · Canonical API 与旧写失败关闭

文件：

```text
services/aos-api/aos_api/routers/aip_model_runtime.py
services/aos-api/aos_api/routers/domain_aggregates.py
services/aos-api/aos_api/routers/model_routes.py
services/aos-api/aos_api/model_router_config_router.py
services/aos-api/tests/aip/test_aip_model_runtime_api.py
```

所有 scope 来自 Principal；写命令要求 Idempotency-Key/If-Match；旧写关闭但旧读兼容。

### A7-4 · AgentRun 与统一 adapter 接通

文件：

```text
services/aos-api/aos_api/aip_agent_run_service.py
services/aos-api/aos_api/aip_llm_adapter.py
services/aos-api/tests/aip/test_aip7_agent_run_transition.py
services/aos-api/tests/aip/test_aip7_llm_adapter.py
```

只有 resolver 返回 exact resolved 且 capacity reservation 成功，才允许 queued→running。Provider 调用、usage/lineage/reconcile 复用 AIP-4，不在 adapter 保存 Route 真源。

### A7-5 · Capacity/Usage/Cost

复用 AIP-4 UsageReceipt；新增 reservation/consume/release ledger 和版本化价格快照引用。100 并发不得超卖；usage/price 缺失为 unknown，迟到 usage 追加 Adjustment，不覆盖原值。

### A7-6 · SDK/UI/browser 封板

文件：

```text
apps/web/src/api/aipModelRuntime/
apps/web/src/pages/s2/ModelRuntimePage.tsx
apps/web/src/App.tsx
apps/web/src/navigation/*
```

页面按 Provider/Model/Route/Policy/Eval/Capacity/Runtime readiness 分层展示 loading/empty/blocked/failed/ready；不回显 secret，不从旧 KV 或静态默认模型补数据。

## 7. 外部门与真实数据策略

### 7.1 当前允许完成

- exact authority、Store、API、SDK/UI；
- 真实空态、blocked 原因、旧配置迁移预览；
- 双租户隔离、revision drift、撤销、unknown、容量并发和失败关闭测试；
- 不触发外部调用的 resolver 与 AgentRun blocked 路径。

### 7.2 未经额外条件不得宣告完成

- Provider operational；
- 真实模型调用、质量 Eval GREEN；
- 栖月汇默认路由启用；
- 10 capability readiness available；
- 六数字同事 runnable；
- Token/费用真实对账 GREEN。

这些需要经批准的 Provider 插件、secretRef、网络/数据出境策略、真实 EvalPack/GoldSet、价格来源和预算。

## 8. 测试与验收矩阵

| 门 | 正向 | 负向 |
|---|---|---|
| 合同 | canonical hash 稳定、alias 唯一 | secret 字段、非 exact ref、重复候选拒绝 |
| Store | revision append、head CAS、Receipt replay | hash 漂移、跨租户、撤销后新绑定拒绝 |
| Resolver | exact route/model/provider/policy/eval 全部满足 | health stale、Eval 缺失、egress/PII/能力不符、unknown price blocked |
| AgentRun | resolved + reservation 才 running | 旧 mutable route、KV 默认、policy drift、capacity unknown 拒绝 |
| Fallback | 同政策同能力下允许并记 lineage | 安全拒绝、跨境变化、质量低于门禁不得 fallback |
| Usage | provider usage → AIP-4 Receipt，迟到追加 adjustment | 缺 usage/价格不得记 0 |
| UI | 栖月汇真实空态/blocked；刷新恢复 | 测试组织 4/12/6/5 不可见；secret 永不显示 |

## 9. 首轮评审问题与整改

| ID | 首轮问题 | 整改 |
|---|---|---|
| R1 | 只补 RouteRevision 会留下 mutable Provider/Model | 一并冻结 ProviderInstanceRevision、RegisteredModelRevision |
| R2 | AgentRun 还要求 PolicyRevision | 新增 RuntimePolicyRevision exact authority |
| R3 | 可能复制 AIP-4 Eval/Usage | 明确直接复用，仅保存 exact ref |
| R4 | 历史 4/12/6/5 行可能被误迁移 | 禁止自动回填与跨租户复制，只允许本租户显式迁移 |
| R5 | 代码完成可能被误报 runnable | 拆分 code/control 与 Provider/Eval/operational 外部门 |
| R6 | 旧 Router 与新 Router 双写风险 | Canonical 新写唯一，旧写稳定失败关闭，旧读仅兼容投影 |
| R7 | Provider health 可能冒充质量门 | health 与 AIP-4 Eval 分离且都必须满足 |
| R8 | adapter 可能成为 Route 真源 | adapter 只接收 resolved envelope，authority 留在 Store/resolver |

## 10. 最终复审结论

第二轮逐项复审结果：

- ownership 单一：PASS；
- 不重做 AIP-4/AIP-6：PASS；
- exact revision/hash/CAS/Receipt：PASS；
- secretRef-only：PASS；
- 双租户与零自动回填：PASS；
- code/control 与 operational 状态分离：PASS；
- 旧写退役和单 resolver：PASS；
- 外部 Provider/Eval/预算门保留：PASS。

结论：`APPROVED_FOR_INCREMENTAL_IMPLEMENTATION`。实施顺序为 A7-0→A7-6；允许在外部门未满足时封板为 `CODE/CONTROL_GREEN + PROVIDER/EVAL_BLOCKED`，禁止将其升级为 runnable。

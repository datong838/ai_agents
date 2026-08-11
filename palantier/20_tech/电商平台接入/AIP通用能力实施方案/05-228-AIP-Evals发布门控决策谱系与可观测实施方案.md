# 228-AIP Evals、发布门控、决策谱系与可观测实施方案

> 状态：**IMPLEMENTING · v2.4 · E0A/E0B/E1A/E1B/E1C/E2/E3A/E3B/E3C/E3D/E4A IMPLEMENTED_GREEN / E4B APPROVED_TO_IMPLEMENT（已获用户全量编码授权）**
> 对应阶段：AIP-4、AIP-7（观测侧）。
>
> 2026-08-11 补充：外部 ResearchJob Eval/Lineage v1.2 已评审通过，不改变当前编码门禁。

## 0. 2026-08-11 实时代码与数据裁决

1. AIP-0～AIP-3 已封板；AIP-4 E0A 已从 `aip3b_002` 线性新增单 head `aip4_001`，已完成 downgrade/upgrade 回演。
2. 现有 Eval 不是全空白：`aip_eval_suite`、`aip_eval_report` 已是租户范围 PostgreSQL 真值，真实库当前有 1 个 Suite、2 个 immutable Report；但 Suite 缺 revision/hash/dataset/judge，Report 只支持 `logic_graph`，不能冒充完整 AIP-4。
3. 现有 Logic Publication 已把 graph revision/hash、dry-run 和 Eval report 绑定在单事务内，真实库有 1 条 immutable Publication；本轮扩展为通用 ReleaseGate/PublicationEvent，不重写这条正常链。
4. `decision_lineage` 已有 631 条组织/工作区隔离的历史 Action lineage，必须保留；但 `/v1/aip/lineage` 仍读取进程内 `aip_lineage_engine.py`，页面还保留固定六段 trace，二者不是真实 Task/Run 谱系。
5. `aip_observability.py` 仍把请求数乘 230 估算 Token，并生成合成趋势/采样 trace；这些只能标 `estimated/sampled`，必须退出硬门和真实成本口径。
6. 基线定向测试为 33 passed / 6 failed：4 项是 Publication API 测试身份未带当前发布权限，属于测试夹具漂移；2 项是历史 TI-5 全库 schema lint 报告包含早期迁移遗留问题，不能写成 AIP-4 GREEN，也不得借 AIP-4 破坏性修改历史表。

### 0.1 保留、扩展、下线

- 保留并扩展：`aip_eval_suite/report`、`aip_logic_publication`、`decision_lineage` 历史数据和现有 Logic 发布事务。
- 新增：精确资产引用、Dataset/Judge、EvalRun、ReleaseGateDecision、PublicationEvent、LineageEvent、UsageReceipt/AdjustmentEvent、MetricDefinition 的版本化/不可变契约。
- 下线：内存 `LineageEngine` 生产读取、固定六段 trace、合成趋势、Token=`request_count×230` 作为确定值、页面手工 GREEN。
- 暂缓绑定：AIP-6 尚未发布的 Agent/Skill revision 只冻结引用契约，不伪造资产；其 EvalCatalog 在 AIP-6 后补齐。

## 1. 目标

对同一个不可变 `AgentInstance + Skill + Logic revision/hash + ModelRoute revision + Policy revision` 建立可复验的 Eval、发布和运行证据，消除固定 trace、手工绿灯和估算指标冒充真值。

## 2. 三层门控

1. 资产门：EvalCase 数据集、来源、租户/脱敏、expected/judge revision。
2. 运行门：smoke、contract、safety、quality、cost/latency，失败不得吞掉。
3. 发布门：绑定精确 revision/hash 的报告、审批和 publication receipt。

六数字同事每个 Skill 首批至少具备：正常 5、边界 3、负向/安全 5、租户 2、工具失败 2 条用例；高风险 Skill 追加注入、PII、越权、回执乱序和模型降级。

## 3. Lineage 主链

```text
Task/Plan
 -> input Object/Selection/Wiki refs
 -> model route + prompt revision
 -> tool/action calls
 -> artifact/evidence
 -> eval report
 -> draft/approval/receipt
 -> effect review/memory candidate
```

Lineage 只引用真实 run 事件；移除“默认 6 段 trace”作为真实页面数据源。

外部 ResearchJob 还必须记录：provider/CapabilityBinding version、external execution id、不可变 input/output schema hash、事件序列摘要、网络策略、模型/工具/子任务摘要、Artifact hash、Delivery Receipt 和 reconcile 事件。外部 provider 自报 succeeded 不是 AOS Eval 或 ReleaseGate 通过。

## 4. 可观测真值

| 指标 | 当前 | 目标 |
|---|---|---|
| HTTP 请求/延迟/错误 | 进程采样 | 保留，并带 source/sample window |
| Token | 请求数×230 估算 | provider/route usage receipt |
| 趋势 | 合成波形 | 持久化 time-series/event rollup |
| Trace | 路由聚合 | Task/Logic/Agent span |
| Dashboard | 静态 widget | 组织级持久化 Dashboard revision |
| 成本 | 不完整 | model/tool/capability/task/agent 归因 |

估算值可保留但必须标 `estimated`，不得参与预算硬门或 SLA 判定。

## 5. 文件边界

```text
services/aos-api/aos_api/aip_eval_*.py
services/aos-api/aos_api/aip_logic_publication_store.py
services/aos-api/aos_api/aip_decision_lineage_store.py
services/aos-api/aos_api/aip_runtime_telemetry.py
services/aos-api/aos_api/aip_observability.py
services/aos-api/alembic/versions/*_aip_telemetry.py
apps/web/src/pages/s2/aip.tsx
apps/web/src/pages/s2/ObservabilityPage.tsx
apps/web/src/pages/s2/LogicPublicationPanel.tsx
```

## 6. 开发波次

- E0A：冻结 AssetRevisionRef、Dataset/Judge、EvalRun/Report、ReleaseGate、PublicationEvent、LineageEvent、UsageReceipt/AdjustmentEvent 与 MetricDefinition；做 additive migration、FORCE RLS、append-only 约束和历史兼容，不开放新写页面。
- E0B：建立唯一 scoped store/service/API，修正 Publication API 权限测试夹具；完成 OpenAPI、迁移、双租户与 immutable 证据门。
- E1：EvalPack registry、runner、真实数据来源/脱敏；先支持现有 Logic revision，六同事/37 Logic 在 AIP-6 资产发布后绑定，不生成假目录。
- E2：通用 ReleaseGate、Logic PublicationEvent/revoke；Agent/Skill publication 只在其 registry 存在后启用。
- E3：真实 LineageEvent、span、UsageReceipt、成本和 Capability Receipt；缺失显示 unknown，估算值不得过门。
- E4：Lineage/Observability/Publication 页面切换唯一 SDK 与服务端真值，移除固定六段和合成趋势，完成浏览器验收。
- E5：Dashboard revision、Alert/Ack/Silence Receipt；再接 ResearchJob、37 Logic、SC01～SC09、Wiki/FDE/Content 和 G0～G6 累计专项门。

### 6.1 E0A 计划修改文件

```text
services/aos-api/alembic/versions/aip4_001_eval_lineage_observability_contract.py
services/aos-api/aos_api/aip_eval_contracts.py
services/aos-api/tests/aip/test_aip4_contracts.py
services/aos-api/tests/aip/test_aip4_migration.py
```

E0A 只做兼容扩展：不得删除/覆盖 1 个 Suite、2 个 Report、1 个 Publication 或 631 条历史 lineage；不得向 `org-org/dev-project` 写验收业务数据。

### 6.2 E0A 实施结论（2026-08-11）

- 代码基线：`aos-platform/m1@2c02d1f`。
- 新增 9 组权威表，全部启用 `RLS + FORCE RLS`；除可转移的 `aip_eval_run` 外均为 append-only。
- 定向验证 26 passed；单 head、迁移回演和历史计数守恒通过。
- 历史 Suite=1、Report=2、Publication=1、lineage=631 均属于 `dev-org/dev-project`，仅作兼容基线，不作真实租户 GREEN 证据。
- `org-org/dev-project` 本波新增业务记录为 0；未开放新 API/页面，未执行 Eval、Publication 或外部 Adapter。

### 6.3 E0B 实施边界

E0B 分为 E0B1/E0B2：E0B1 先建立唯一 tenant-scoped store 与不可变语义；E0B2 再开放最小 API/OpenAPI，校正 Logic Publication 测试夹具的权限身份。不在 E0B 构造虚假 EvalRun、ReleaseGate 或 UsageReceipt。

E0B1 已以 `aos-platform/m1@4f9f471` 实施：新增唯一 authority store，补齐 EvalRunAuthorityRecord/Event，对 Dataset/Run/Gate/Publication/Lineage/Usage/Adjustment/MetricDefinition 建立 scoped persistence。31 项定向回归通过，真实库仅双租户空读，业务写入为 0。

E0B2 只开放三个只读入口：Dataset revision、EvalRun snapshot、Lineage events。不开放 Gate/Publication/Usage 手工写 API，不让页面越过 E1/E2 服务直写绿灯或用量事实。

E0B2 已以 `aos-platform/m1@0996704` 实施，文档证据 `docs/m1@d718b78`。冻结范围 55 passed + 2 subtests，真实租户和负向 canary 只读冒烟通过，AIP-4 业务写入为 0。历史 `tests/test_evals_engine.py` FORCE RLS 夹具缺 tenant GUC 的 7 项 RED 已登记并转入 E1，不冒充全后端 GREEN。

### 6.4 E1 实施裁决与文件边界（2026-08-11）

E1 不把旧 `aip_eval_suite/report` 直接包装成新 Registry。E0A 只有版本化 DTO，尚缺版本化 Suite/Report 数据表；若跳过该缺口，dataset/judge 漂移后仍可能复用旧报告。因此拆为：

- E1A：新增 append-only `aip_eval_suite_revision`，实现 tenant-scoped EvalPack Registry；Dataset manifest 只接受可复验 source reference/hash、字段 allowlist 和脱敏证明，不复制 PII 到 Registry。
- E1B：新增 append-only `aip_eval_report_revision`，实现 runner、judge adapter 和不可变报告；精确绑定 suite/target/dataset/judge revision+hash，任一引用漂移均拒绝复用旧报告。
- E1C：迁移旧 Logic Eval API 到新服务或明确 compatibility adapter，并修正 FORCE RLS 测试夹具；旧内存 `EvalsEngine` 不再作为生产 Suite/Report 真源。

E1A 计划修改文件：

```text
services/aos-api/alembic/versions/aip4_002_eval_pack_registry.py
services/aos-api/aos_api/aip_eval_contracts.py
services/aos-api/aos_api/aip_eval_pack_registry.py
services/aos-api/tests/aip/test_aip4_eval_pack_registry_migration.py
services/aos-api/tests/aip/test_aip_eval_pack_registry.py
```

E1A 退出门：

- 同一租户内 `suite_id + revision` immutable/idempotent，hash 或内容不同必须冲突；跨租户不可见。
- Suite 的 target、dataset、judge 都是 exact revision/hash，Dataset 必须已存在于同租户 authority store。
- Dataset manifest 必须有真实 source kind/id/revision/hash、字段 allowlist、redaction receipt/hash、case count；出现内联业务行、明文 PII、Mock/synthetic 标记时失败关闭。
- 在 AIP-6 的 Agent/Skill revision 发布前，不生成六同事或 37 Logic 的假 EvalPack。

E1A 已以 `aos-platform/m1@134b7e8` 实施：真实库单 head 为 `aip4_002`；20 项组合回归通过；`org-org/dev-project` 与 `dev-org/dev-project` 的 Suite revision 均为 0，没有用测试 EvalPack 污染业务数据。E1B 获准进入不可变 report 与 runner 实施。

E1B 已以 `aos-platform/m1@7e255ed` 实施：真实库单 head 为 `aip4_003`；28 项组合回归通过。Report 仅保存 case/result hash、结构化 detail code、计数和 exact refs，不保存输入/期望/输出业务明文。Resolver 内容、Artifact ref、target 或 judge 任一漂移都会将 Run 置为 failed，且不生成报告。E1C 获准迁移旧 Logic Eval API/夹具；不得以删除测试或放松 RLS 方式消红。

E1C 已以 `aos-platform/m1@f359534` 实施：旧 Logic Eval API 保留为 compatibility surface，生产真值仍由 PostgreSQL Suite/Report 与 E1 Registry/Runner 承担。隔离测试 schema 仅向 `aos_runtime` 授予 USAGE 和表级最小 DML 权限，并设置 transaction-local tenant GUC；未关闭 FORCE RLS、未恢复进程内生产真源。旧 Eval 文件 17 passed / 1 个显式 Agnes 实连 skipped；E0A～E1C、旧 Publication 与 OpenAPI 组合收集 80 项并以退出码 0 完成。伪造未知租户请求按当前认证契约返回 `403 AUTH_TENANT_UNKNOWN`。E2 获准进入 ReleaseGate 与 PublicationEvent/revoke 实施。

### 6.5 E2 实施边界（编码前冻结）

E2 复用 `aip4_001` 已有的 `aip_release_gate_decision`、`aip_publication_event`、RLS/FORCE RLS 和 append-only 触发器，不新增第二套门控或发布表。新增唯一权威服务，在单事务内完成以下步骤：

1. 读取 `aip_eval_report_revision` exact `report_id/revision/hash`，重新计算内容 hash；读取其 `aip_eval_run` 与 `aip_eval_suite_revision`，要求 Run=`succeeded`，Suite/Target/Dataset/Judge 引用全部一致。
2. ReleaseGate 状态只能由不可变 Report 和 Suite threshold 推导；请求不得携带 `passed/GREEN` 字段。未通过的 Report 可形成 `failed` 决策，但绝不能追加 `published` 事件。
3. E2 仅开放 `logic_graph` 发布：必须在 `aip_logic_graph_revision` 找到 exact revision/hash。`agent_template/agent_instance/skill_template` 等 registry 尚未落地的资产一律以明确错误失败关闭。
4. 发布与撤销都是追加 `PublicationEvent`；撤销要求同 publication 已存在 `published` 且尚无 `revoked`，不得 UPDATE/DELETE 历史发布、Report、Gate 或 Lineage。
5. 幂等键只用于确定性生成 decision/event 标识；同键同请求回放返回同一事实，同键异请求冲突。所有读取和写入均带 `org_id/project_id`，负向租户只能得到 scoped not found。

E2 计划修改文件：

- 新增 `services/aos-api/aos_api/aip_release_publication_models.py`
- 新增 `services/aos-api/aos_api/aip_release_publication_service.py`
- 新增 `services/aos-api/aos_api/routers/aip_release_publications.py`
- 修改 `services/aos-api/aos_api/routers/domain_aggregates.py` 注册 canonical API
- 新增 `services/aos-api/tests/aip/test_aip_release_publication_service.py`
- 新增 `services/aos-api/tests/aip/test_aip_release_publication_api.py`

本波不修改页面、不执行真实线上 Eval/Publication，不向 `org-org/dev-project` 或 canary 写业务事实；以隔离 PostgreSQL 正向/负向、跨租户、幂等、hash 漂移、失败报告、重复撤销和 append-only 测试封板。

E2 已以 `aos-platform/m1@fb525cc` 实施：ReleaseGate 只接受 E1B exact report revision/hash，并在同一 scoped transaction 复验 succeeded Run、Suite threshold、Target/Dataset/Judge 和当前 Logic revision/hash；请求契约不存在手工 GREEN/status 字段。`published/revoked` 均为 append-only `PublicationEvent`，撤销后同一 exact target 的新 Eval Run 失败关闭，历史 Report/Gate/Event 不改写。Agent/Skill registry 未落地类型保持 unsupported。AIP-4 E0A～E2 合并回归 95 passed / 1 个显式 Agnes 集成项 skipped / 2 subtests passed；OpenAPI 为 2335 paths、1569 schemas、4100 route rows、4090 unique operation pairs。真实库保持单 head `aip4_003`，`org-org/dev-project` 与 `dev-org/dev-project` 的新 Suite/Report/Gate/Event 均为 0。E3 获准进入真实 Lineage/Telemetry/Usage/Cost 实施。

### 6.6 E3 实施裁决与子波冻结（2026-08-11）

E3 不得直接把现有 `aip_lineage_engine.py`、`tracing_perf_geo_map.py` 或 `aip_observability.py` 包装成真值。实时代码复核确认：固定六段 Trace、内存 span、`request_count×230` Token 和合成趋势都不具备发布门证据资格；现有 `UsageReceipt.quality=unknown` 仍要求数值，也会把未知误写为 0。E3 拆为四个可独立回滚的子波：

| 子波 | 范围 | 退出门 |
|---|---|---|
| E3A | TaskRun、Action、Eval、Publication 权威源事件投影到 append-only `LineageEvent`；建立唯一 canonical 查询 | 每个事件带 source kind/id/hash；同源幂等、异载荷冲突、跨租户不可见；不生成固定六段 |
| E3B | 持久化 span 与 provider UsageReceipt/Adjustment；纠正 unknown 数量语义 | 乱序/迟到/时钟偏差保留 producer 与 observed 时间；unknown 的 quantity 为空；重复 provider receipt 不重复计量 |
| E3C | model/tool/capability/task/agent 成本归因与 Capability Receipt | 仅 measured receipt 可进入硬预算门；estimated 单独展示；缺失为 unknown；调整事件可复算且不覆盖原收据 |
| E3D | E3 总回归、ResearchJob provider/artifact/delivery/reconcile 契约与失败关闭 | provider 未注册、回调重放、Artifact hash 错或 capability 漂移均阻断；不伪造外部 Job 成功事实 |

E3A 计划修改文件：

```text
services/aos-api/alembic/versions/aip4_004_lineage_source_authority.py
services/aos-api/aos_api/aip_eval_contracts.py
services/aos-api/aos_api/aip_lineage_service.py
services/aos-api/aos_api/routers/aip_lineage_authority.py
services/aos-api/aos_api/routers/domain_manifest.json
services/aos-api/tests/aip/test_aip4_lineage_source_migration.py
services/aos-api/tests/aip/test_aip_lineage_service.py
services/aos-api/tests/aip/test_aip_lineage_authority_api.py
```

E3A 先覆盖已经存在且可复验的源事实：`aip_task_run/aip_step_run/aip_checkpoint/aip_artifact/aip_evidence`、`aip_action_event/aip_action_receipt`、`aip_eval_run_event/aip_eval_report_revision`、`aip_publication_event`。事件标识由 scope + source kind + source id + source hash 确定性生成；投影只保存引用、结构化事件类型和哈希，不复制输入、Action payload、模型提示词、业务对象字段或 PII。历史 `decision_lineage` 仅通过 `legacy_decision_lineage` root 兼容读取，不倒灌为新运行真值。

E3A API 只允许读取谱系和由受信运行角色触发“按 root 对账投影”；普通页面不能 POST 任意事件。若源事实不存在、跨租户、hash 漂移或 root/source 不匹配必须失败关闭。投影事务失败不得伪装运行已具备完整谱系；页面在 E4 前仍不得使用旧固定六段作为回退。

E3A 已以 `aos-platform/m1@16aed87` 实施：`aip4_004` 为 `aip_lineage_event` 增加完整 source tuple、租户内同源唯一索引和 root timeline 索引，并保留原有 RLS/FORCE RLS 与 append-only 触发器。唯一 `AipLineageService` 只从 PostgreSQL TaskRun/Step/Checkpoint/Artifact/Evidence、ActionEvent/Receipt、EvalRun/Event/Report 和 PublicationEvent 生成确定性事件；普通 API 只能查询，受信运行角色只能选择 root 触发对账，不能提交手工事件或 GREEN。累计 107 项测试退出码 0，静态检查、编译、路由/OpenAPI 固定契约通过；OpenAPI 更新为 2337 paths、1570 schemas、4102 route rows、4092 unique operation pairs。开发库已线性升级到单 head `aip4_004`，`org-org/dev-project` 与 canary 的新谱系记录均为 0，未伪造验收事实。下一门为 E3B 持久化 spans、provider UsageReceipt/Adjustment 与 unknown 数量语义。

E3B 已以 `aos-platform/m1@ea1f1c5` 实施：`aip4_005` 新增 tenant-scoped `aip_telemetry_span`，区分 producer/observed/ingested 时间并保留原始时钟偏差；`UsageReceipt` 将 unknown 数量纠正为 `NULL`，measured/estimated 强制非负数值。span 与 usage 均以 scope + provider + provider receipt 唯一，同载荷重放幂等、异载荷冲突；Adjustment 继续只追加且不覆盖原收据。canonical API 只允许受信运行角色写入并要求既有 lineage，PII attribute 只接受哈希。39 项 E3B 定向测试、95 项 `tests/aip` 累计回归、ruff、compileall、OpenAPI 双进程确定性检查和路由固定契约均退出码 0；OpenAPI 为 2343 paths、1579 schemas、4108 route rows、4098 unique operation pairs。开发库单 head 为 `aip4_005`；`org-org/dev-project` 与 canary 的 span/usage/adjustment 均为 0。

E3C 编码边界冻结为：新增 `aip4_006_cost_attribution_capability_receipt.py`、`aip_cost_attribution_service.py`、`routers/aip_cost_attribution.py` 及对应迁移/service/API 测试，并兼容扩展 `aip_eval_contracts.py`、`aip_eval_authority_store.py`、`aip_telemetry_usage_service.py`。本波建立 append-only UsageAttribution 与 CapabilityReceipt，不改写 E3B 原始 span/usage；成本聚合必须按 currency 和 measured/estimated/unknown 分桶，Adjustment 继承原 Receipt 质量并参与复算，复算后不得为负。CapabilityReceipt 只能引用同租户 TaskRun 已批准 PlanStep 中 exact revision 的 `capabilityRef`，且必须与 lineage root 一致；AIP-6/AIP-7 尚无权威 registry 的 model/tool/agent 引用不得冒充 measured 归因，只能 unknown/estimated 或明确失败关闭。硬预算读模型仅在 measured、币种单一、无 unknown/estimated 缺口时标记 eligible；缺收据、缺价格或缺权威归因一律 unknown，不把 0 当真值。

E3C 已以 `aos-platform/m1@f7179ce` 实施：`aip4_006` 新增 tenant-scoped、RLS/FORCE RLS、append-only 的 `aip_usage_attribution` 与 `aip_capability_receipt`；UsageAttribution 引用原 UsageReceipt 与同一 lineage，并限制同一收据/维度权重总和不超过 1。CapabilityReceipt 只接受同租户已批准 PlanStep 的 exact capability revision，provider receipt 同载荷重放幂等、异载荷冲突。成本按币种与 measured/estimated/unknown 分桶，Adjustment 在锁定原 Receipt 后追加，禁止把有效用量调成负数；只有无估算、无未知缺口的 measured 单币种汇总才可进入硬预算。AIP-6/AIP-7 权威 registry 未落地前，model/tool/agent measured 归因明确失败关闭。20 项 E3C/路由定向测试、105 项 `tests/aip` 累计回归、ruff、compileall、OpenAPI 确定性与固定路由契约均完成；OpenAPI 为 2347 paths、1586 schemas、4112 route rows、4102 unique operation pairs。开发库已线性升级至单 head `aip4_006`；`org-org/dev-project` 与 canary 的两张新增表均为 0，未写入虚假验收事实。

E3D 编码前门禁冻结为：只收口外部 ResearchJob provider/artifact/delivery/reconcile 契约和 E3 总回归，不把内存 Job 状态或回调到达等同于成功。Provider 必须来自租户范围、版本化且已启用的权威注册；提交请求绑定 exact provider/capability/plan/lineage，外部 job id 只由受信 Adapter 回写。回调必须验签、nonce 防重放、事件序列单调；Artifact 必须保存 immutable URI/hash/media type/producer receipt，交付前复验 hash 与 capability revision。timeout/网络断开进入 unknown/reconcile，不自动重试外部副作用；只有 reconcile receipt 可推进最终状态。实现前先复核现有 `aip_research_job.py`、TAOR ResearchJob 兼容链和已评审 v1.2 方案，优先兼容扩展，禁止再建第二套 Job 真源。

E3D 实时代码复核确认：`aip_research_job.py` 只有 v1.2 DTO、纯函数事件合并和 HMAC 验签，nonce 仍由调用方进程内 `set` 保存；仓库没有 tenant-scoped Provider Registry、不可变 Job Manifest/Submission Receipt、持久化 provider event、Artifact/Delivery/Reconcile Receipt 或 canonical API。现有 `aip_task_run/aip_plan_revision` 已是 Task/Run 权威，`aip_artifact` 已是通用产物真源，因此 E3D 只增加外部 Adapter 事实层并复用上述外键，不创建第二套 Task 状态机或平行 Artifact 库。

E3D 计划文件边界固定为：

```text
services/aos-api/alembic/versions/aip4_007_research_job_authority.py
services/aos-api/aos_api/aip_research_job.py
services/aos-api/aos_api/aip_research_job_store.py
services/aos-api/aos_api/aip_research_job_service.py
services/aos-api/aos_api/routers/aip_research_jobs.py
services/aos-api/aos_api/routers/domain_manifest.json
services/aos-api/tests/aip/test_aip4_research_job_migration.py
services/aos-api/tests/aip/test_aip_research_job_store.py
services/aos-api/tests/aip/test_aip_research_job_api.py
```

`aip4_007` 仅新增 append-only ProviderRevision、JobManifest、SubmissionReceipt、ProviderEventReceipt、CallbackNonce、ArtifactReceipt、Delivery/Reconcile Receipt。Job 当前观察由持久化事件推导；sequence gap 可保存并显示 `has_gap`，但不得推进 canonical 成功。Provider disable 通过追加更高 revision 的 disabled 记录实现，提交时 exact revision 必须同时是当前最高且 enabled。Callback 只记录验签后的 nonce/body hash 并触发主动回读，不接受 body 自报状态。ArtifactReceipt 必须与既有 `aip_artifact` 同事务绑定并复验 content hash；Delivery succeeded 需要无 gap 的 provider succeeded 观察、全部 Artifact hash 有效和 exact capability 未漂移。unknown 只能由追加 Reconcile Receipt 收敛，不覆盖历史。

E3D 最终方案一致性复审发现：`aip4_007` 已绑定 TaskRun、PlanRevision、PlanStep 和 capability，但尚未把同一 TaskRun 根的 exact lineage event 固化到 JobManifest。该缺口不得带入封板。补强采用线性追加迁移 `aip4_008_research_job_lineage_binding.py`，不改写已推送/已执行的 `aip4_007`：为 JobManifest 增加 `lineage_id + lineage_sequence + lineage_event_id`，以 `(org_id, project_id, lineage_id, sequence)` 外键引用 `aip_lineage_event`。创建 Job 必须提交 `lineageRef(resourceType=aip.lineage, authority=aos.lineage, revision=sequence)`，且该事件必须是当前 lineage 最新序列、root_type=`task_run`、root_id=当前 run；跨 run、跨租户、旧序列或不存在事件全部失败关闭。`aip4_008` 若发现既有 ResearchJob 行则拒绝无证据回填；当前开发库七表均为 0，可安全线性升级。

E3D 实施结论：核心事实层、Canonical API 与 exact lineage 补强分别提交 `849f40d`、`e7542db`、`a88cad1`。JobManifest 以 `(org_id, project_id, lineage_id, sequence, event_id)` 五列外键绑定唯一谱系事件；缺失、旧 sequence、跨 Run/跨 scope 均失败关闭。13 项补强定向门、118 项 `tests/aip` 累计回归、Ruff、compile、OpenAPI 确定性导出全部通过。开发库单 head/current 均为 `aip4_008`；`org-org/dev-project` 与 canary 的七张 ResearchJob 权威表均为 0，RLS/FORCE RLS/双 append-only guard 全部有效。E3D 可封板为 `IMPLEMENTED_GREEN`，下一门为 E4 三页面真实 SDK 消费。

### 6.7 E4 页面真实化实施裁决（2026-08-12）

E4 代码复核确认，服务端权威读模型已具备，但三个消费面仍未统一：

- 决策谱系页仍调用历史 `/v1/aip/lineage/{id}`，并在空响应时展示固定六段 `defaultSteps`、固定 Trace ID 与固定标题；这不构成 E3A 权威谱系证据。
- 可观测页仍调用 `/v1/aip/observability/summary|traces`；该旧实现包含 `request_count × 230` Token、合成趋势和采样路由 Trace，页面还初始化 `MOCK_WIDGETS`，不得继续标为确定性真实数据。
- Evals 门控页已有真实 Suite/Run/Report/Gate 兼容链，Logic Publication Panel 也已有严格 revision/hash 重读，但二者仍各自直接调用 API；E4 必须统一到一个强类型 SDK，且不得新增页面手工 GREEN 或 Publication 写真源。

“三页面”在本轮固定为导航中的 `Evals 门控`、`决策谱系`、`可观测性`。Publication 的写动作仍留在现有 Logic Canvas/Publication Panel；Evals 门控页承担发布前 Gate/Report 证据面，不再新建第二个 Publication 页面或第二套发布状态机。

E4 分为三个独立安全提交：

| 子步 | 范围 | 退出门 |
|---|---|---|
| E4A | 新建唯一 `aipEvidence` SDK；决策谱系页切换 `/v1/aip/lineage-authority/roots/{root_type}/{root_id}` | 无固定 Trace/六段回退；真实 idle/loading/empty/error/partial；跨租户由现有认证 scope 失败关闭 |
| E4B | 可观测页切换 `/v1/aip/telemetry-authority/lineages/{lineage_id}/spans|usage-receipts` | Overview 只聚合权威事实；measured/estimated/unknown 分桶；无合成趋势、伪 Token、生产 Mock Widget |
| E4C | Evals 门控读链与 Logic Publication 严格读链统一经 SDK；三页回归和内置浏览器验收 | 页面不可手工 GREEN；revision/hash/readback 不弱化；真实租户诚实空态，canary 不作正向证据 |

E4 计划修改文件：

```text
apps/web/src/api/aipEvidence/contracts.ts
apps/web/src/api/aipEvidence/client.ts
apps/web/src/api/aipEvidence/index.ts
apps/web/src/api/aipEvidence/client.test.ts
apps/web/src/pages/s2/aip.tsx
apps/web/src/pages/s2/ObservabilityPage.tsx
apps/web/src/pages/s2/EvalsPage.test.tsx
apps/web/src/pages/s2/ObservabilityPage.test.ts
apps/web/src/pages/W3BPageInteraction.test.tsx
apps/web/src/interactionHonestyManifest.ts
```

若 E4C 复核发现现有服务端缺少只读 Gate/Publication 查询，只允许对 `aip_release_publication_service.py` 和 `routers/aip_release_publications.py` 做 additive GET 扩展并补 OpenAPI/隔离测试；不得为了页面展示写入真实业务记录。页面验收只使用 `org-org/dev-project`，`dev-org/dev-project` 只做负向 canary。

E4A 已以 `aos-platform/m1@84dac50` 实施：新增唯一 `aipEvidence` contracts/client/index，对 LineageEvent 的 root、连续 sequence、source tuple、sha256 与 quality 做前端失败关闭解析；决策谱系页改为 root type + root id 查询 canonical `/v1/aip/lineage-authority/roots/...`，删除固定 Trace ID、固定六段和失效治理探针。9 项 SDK/页面定向测试与 TypeScript 通过；内置浏览器在 `org-org/dev-project` 验证 idle 和 API 错误态均不注入示例谱系。当前本机 API health=500，因此本步浏览器证据只声明页面渲染/失败关闭 GREEN，不冒充真实事件正向回包已验收。下一子步 E4B。

## 7. 发布、撤回与数据治理

- EvalCase、Judge、数据集、报告和 Publication 都是带 version/hash 的独立资产；重新运行不得覆盖旧报告。
- ReleaseGate 只接受同一资产组合生成的报告；任一 Template/Skill/Logic/ModelRoute/Policy revision 变化都使旧门控失效。
- 发布后的 revoke/deprecate 创建新 PublicationEvent，阻止新 Run，不修改历史运行事实。
- Trace 与 UsageReceipt 按租户分区；PII 默认不写 span attribute，ObjectReference 和 secretRef 只记录不可逆标识。
- 指标定义包含 name、unit、source、window、aggregation、quality；estimated 与 measured 不得聚合成同一确定值。
- retention、导出、删除请求必须区分可删除 payload 与依法/审计需保留的不可变哈希和事件引用。

## 8. 验收

- 页面不能手工设置 GREEN。
- 运行 revision 与报告 revision 不一致时发布拒绝。
- 模型 fallback、工具失败、Draft 驳回、unknown external state 均出现在同一谱系。
- 真实 Token/成本缺失时显示 unknown，不用估算补成确定值。
- 双租户查询和导出均隔离；导出脱敏且保留 source metadata。
- Publication revoke 后新 Run 被阻断，历史报告和 Lineage 仍可复验。
- 时钟偏差、乱序 span、重复 UsageReceipt 和迟到事件不会造成重复成本或错误 GREEN。
- 外部 Job 的 callback 重放、事件乱序/重复、引用失效、Artifact hash 不符、provider 漂移和脱敏失败均有负向 EvalCase，且不能进入 ReleaseGate。
- DeerFlow 停用后历史 Lineage 可完整解析，原生 AIP Eval/发布主链不受影响。

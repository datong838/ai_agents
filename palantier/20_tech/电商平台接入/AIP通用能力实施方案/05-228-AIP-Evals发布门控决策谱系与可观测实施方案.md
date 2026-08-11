# 228-AIP Evals、发布门控、决策谱系与可观测实施方案

> 状态：**IMPLEMENTING · v1.2 · E0A IMPLEMENTED_GREEN / E0B 待实施（已获用户全量编码授权）**
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

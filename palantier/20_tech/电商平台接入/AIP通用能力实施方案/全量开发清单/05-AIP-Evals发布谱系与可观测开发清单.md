# 05 AIP Evals、发布门、决策谱系与可观测开发清单

> 状态：**v1.2 · AIP-4 IMPLEMENTING · E0A 方案复核通过（已获用户全量编码授权）**
> 上位依据：`../05-228-AIP-Evals发布门控决策谱系与可观测实施方案.md`
> 对应阶段：AIP-4、AIP-7 观测侧；前置：02、04 GREEN。

## 1. 工作包

| ID | 任务 | 文件边界 | 验收 |
|---|---|---|---|
| 05-01 | 冻结 EvalCase/Suite/Run/Report/ReleaseGate/Publication DTO | eval contracts | 全部绑定 exact revision/hash |
| 05-02 | 建 Eval/Publication/Lineage/Telemetry 表及 RLS | migrations/stores | 报告不可覆盖，撤回追加事件 |
| 05-03 | 实现六同事 EvalPack Registry | `aip_eval_*` | 每 Skill 正常/边界/负向/租户/故障齐备 |
| 05-04 | 实现 Eval runner、judge version、数据集来源/脱敏 | eval service | judge/数据变更使旧门失效 |
| 05-05 | 实现 ReleaseGate 与 Logic/Agent publication | publication store | 页面不能手工 GREEN |
| 05-06 | 实现 DecisionLineage 真实 run 事件聚合 | lineage store | 删除固定 6 段 trace |
| 05-07 | 接 OpenTelemetry spans 与 task/agent/logic 关联 | telemetry | 乱序/迟到/时钟偏差可处理 |
| 05-08 | 接真实 UsageReceipt、Token、成本、AdjustmentEvent | observability | 缺失为 unknown，不用估算过门 |
| 05-09 | Dashboard revision、Alert/Ack/Silence Receipt | observability UI/store | 无静态 widget 冒充持久化 |
| 05-10 | 外部 ResearchJob provider/artifact/delivery/reconcile 谱系 | lineage/evals | callback 重放、hash 错、漂移均阻断 |
| 05-11 | Lineage/Observability/Publication 页面真实化 | web pages/SDK | API 空/错/partial/unknown 诚实显示 |
| 05-12 | 建 37 Logic EvalCatalog 与发布门 | eval manifests/runner | 每条含正向、边界、缺字段、越权、下游失败、注入 |
| 05-13 | 建 SC01～SC09 组合 Eval 与 Handoff/EffectReview 回归 | scenario evals | 单 Logic 通过不代替场景通过 |
| 05-14 | 建 Wiki/FDE/Content 专项量化门 | eval packs | 冷启动/RAG、26 Reflection、14 Harness、视频/直播分别验收 |
| 05-15 | 建 G0～G6 累计发布与回滚门 | release policy | 上游未 GREEN、平台能力 unknown 或专项 deferred 时不可发布 |

## 1.1 实施子波与依赖裁决（2026-08-11）

| 子波 | 工作包 | 当前状态 | 退出门 |
|---|---|---|---|
| E0A | 05-01、05-02 的公共契约与 additive migration | `APPROVED_TO_IMPLEMENT` | 单 head、历史计数不减、FORCE RLS、append-only、契约测试 |
| E0B | 05-02 scoped store/API + Publication 权限测试校正 | `PENDING` | OpenAPI/route/双租户/重启回读 |
| E1 | 05-03、05-04 | `PENDING` | 真实数据来源、judge/dataset 漂移使旧门失效 |
| E2 | 05-05 | `PENDING` | gate 不可手工改绿、revoke 追加事件 |
| E3 | 05-06～05-10 | `PENDING` | 真实事件/usage；unknown/乱序/重复可收敛 |
| E4 | 05-11 | `PENDING` | 三页面唯一 SDK、无固定 trace/Mock/合成趋势 |
| E5 | 05-12～05-15 | `PENDING` | 37 Logic、场景和专项门在其真实资产存在后逐项封板 |

E0A 文件边界固定为：

- 新增 `services/aos-api/alembic/versions/aip4_001_eval_lineage_observability_contract.py`
- 新增 `services/aos-api/aos_api/aip_eval_contracts.py`
- 新增 `services/aos-api/tests/aip/test_aip4_contracts.py`
- 新增 `services/aos-api/tests/aip/test_aip4_migration.py`

E0A 不修改页面、不触发 Eval/Publication/外部 Adapter，不写真实业务记录。真实库基线计数必须保持 Suite=1、Report=2、Publication=1、历史 lineage=631。

## 2. 退出门

- [ ] 任一 Agent/Skill/Logic/Model/Policy revision 变化，旧 ReleaseGate 自动失效。
- [ ] fallback、工具失败、Draft 驳回、unknown、reconcile、撤回出现在同一谱系。
- [ ] measured/estimated/unknown 不混算；重复 usage 不重复成本。
- [ ] 37/37 Logic 均有独立 EvalPack 和 exact revision 绑定；工具未注册/数据过期必须失败关闭。
- [ ] SC01～SC09、G0～G6、七管道、26 Reflection、14 Harness 和直播 L0～L5 可分别查看通过/阻断/延期证据。
- [ ] 沙箱、Draft、Proposal、平台真实执行四种结果在发布门和谱系中不会混淆。
- [ ] 双租户查询/导出隔离，PII 不进 span；历史发布与撤回可复验。

# 05 AIP Evals、发布门、决策谱系与可观测开发清单

> 状态：**v1.8 · AIP-4 IMPLEMENTING · E0A/E0B/E1A/E1B IMPLEMENTED_GREEN / E1C APPROVED_TO_IMPLEMENT（已获用户全量编码授权）**
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
| E0A | 05-01、05-02 的公共契约与 additive migration | `IMPLEMENTED_GREEN` | `2c02d1f`；26 passed；单 head/守恒/FORCE RLS/append-only 通过 |
| E0B1 | 05-02 tenant-scoped store + immutable semantics | `IMPLEMENTED_GREEN` | `4f9f471`；31 passed；双租户/幂等/冲突/重启回读通过 |
| E0B2 | 05-02 最小只读 API/OpenAPI + Publication 权限测试校正 | `IMPLEMENTED_GREEN` | `0996704`；55 passed + 2 subtests；真实租户与 canary 只读负向冒烟通过 |
| E1A | 05-03 Registry + 真实 Dataset manifest 门 | `IMPLEMENTED_GREEN` | `134b7e8`；20 passed；单 head `aip4_002`；双租户真实库空读 |
| E1B | 05-04 runner + 不可变 report | `IMPLEMENTED_GREEN` | `7e255ed`；28 passed；exact ref/content drift 全部失败关闭 |
| E1C | 旧 Logic Eval compatibility 收口 | `APPROVED_TO_IMPLEMENT` | 旧内存真源退出生产；FORCE RLS 夹具恢复或明确替代 |
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

E0B1 计划文件边界：

- 新增 `services/aos-api/aos_api/aip_eval_authority_store.py`
- 新增 `services/aos-api/tests/aip/test_aip_eval_authority_store.py`
- 如需对契约做兼容修正，仅允许修改 `aip_eval_contracts.py` 及其定向测试。

E0B1 只实现 Dataset revision、EvalRun/event、Gate decision、Publication/Lineage event、Usage/Adjustment 和 MetricDefinition 的 scoped persistence；不开放路由、不写 `org-org/dev-project` 验收数据。

E0B2 计划文件边界：

- 新增 `services/aos-api/aos_api/routers/aip_eval_authority.py`
- 新增 `services/aos-api/tests/aip/test_aip_eval_authority_api.py`
- 修改 `services/aos-api/aos_api/routers/domain_aggregates.py`
- 修改 `services/aos-api/tests/test_aip_logic_publication_api.py`，仅校正测试 principal/scope，不放宽生产鉴权。
- 如 route/OpenAPI inventory 为确定性快照，按实际新路由精确更新对应测试基线。

E0B2 仅允许 GET Dataset revision、GET EvalRun snapshot、GET Lineage events；不开放手工写 Gate/Publication/Usage 事实的 API。

E0B2 封板说明：

- OpenAPI 固定为 2332 paths、1562 schemas、4097 route rows、4087 unique operation pairs；domain manifest 固定为 514 routers。
- `org-org/dev-project` 与 `dev-org/dev-project` 对不存在的 Run 均返回 scoped 404、对不存在的 Lineage 均返回 scoped 空列表；没有写入 AIP-4 业务记录。
- 历史 `tests/test_evals_engine.py` API 夹具在当前 FORCE RLS 数据库下未设置 tenant GUC，独立扩展回归为 7 failed / 65 passed / 1 skipped / 2 subtests passed；该 RED 不属于 E0B2 只读路由回归，也不得隐藏，纳入 E1 旧引擎迁移与测试夹具收口。

E1A 文件边界和门禁：

- 新增 `aip4_002_eval_pack_registry.py`、`aip_eval_pack_registry.py` 及其迁移/store 测试；仅兼容扩展，不覆盖旧 Suite/Report。
- Registry 写入前必须验证同租户 Dataset revision 已存在；Suite/target/dataset/judge 全部绑定 exact revision/hash。
- Dataset manifest 禁止内联业务记录、明文 PII、`mock/synthetic/demo` 来源；必须包含 source reference/hash、字段 allowlist、redaction receipt/hash 和 case count。
- 六同事/37 Logic 等待 AIP-6 真实资产 revision，不生成占位目录。

E1B 计划边界：新增 `aip4_003_eval_report_revision.py`、`aip_eval_runner.py` 及定向测试；Report 只保存 case/result hash 和结构化 detail code，不保存业务明文。Runner 必须从 Registry 读取 Suite，并逐项复验 target/dataset/judge/artifact exact refs；任何漂移、解析失败或 judge 错误使 Run failed，不生成可过门报告。

E1C 禁止通过删除旧测试、关闭 FORCE RLS 或恢复进程内 Suite/Report 真源消红。优先将旧夹具的 scoped connection 设置 tenant GUC，使兼容 API 在当前 RLS 军规下恢复；随后明确旧 API 仅为 compatibility surface，新写链进入 E1 Registry/Runner。

## 2. 退出门

- [ ] 任一 Agent/Skill/Logic/Model/Policy revision 变化，旧 ReleaseGate 自动失效。
- [ ] fallback、工具失败、Draft 驳回、unknown、reconcile、撤回出现在同一谱系。
- [ ] measured/estimated/unknown 不混算；重复 usage 不重复成本。
- [ ] 37/37 Logic 均有独立 EvalPack 和 exact revision 绑定；工具未注册/数据过期必须失败关闭。
- [ ] SC01～SC09、G0～G6、七管道、26 Reflection、14 Harness 和直播 L0～L5 可分别查看通过/阻断/延期证据。
- [ ] 沙箱、Draft、Proposal、平台真实执行四种结果在发布门和谱系中不会混淆。
- [ ] 双租户查询/导出隔离，PII 不进 span；历史发布与撤回可复验。

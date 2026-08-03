# 228-EC Pipeline 诚实执行与负向验收方案

> 版本：v1.1 · 2026-08-01
> 状态：诚实执行与证据门已完成并合入 `m1`；生产执行器/resolver 仍未注册
> 边界：修复 Phase5 占位成功语义；不实现 Join、自定义 SQL 或具体平台管道

## 使用的 Rules

1. 先方案后编码，只做最小语义修复，不重写 Pipeline Builder。
2. 没有执行器、数据落盘和证据时必须返回 unsupported/failed，不得成功。
3. 显式 demo 继续可用，但响应必须带 `mode=demo` 且不能生成 production success 记录。
4. W4 不修改 Connector、OAuth、Ontology、一致性 store、Router manifest、OpenAPI 生成物或 CI。

## 一、已确认风险

- `run_schedule()` 固定生成 success、1000 rows、30 秒。
- `trial_run()` 固定返回 3 条高置信结果和 120ms。
- node/dataset preview 与 health check 固定生成样例/healthy。
-未知 pipeline 的 router fallback 生成 demo graph/history/trial success，容易被消费方误认 live。

## 二、冻结执行证据契约

所有运行结果必须包含：`mode`、`status`、`started_at`、`finished_at`、`duration_ms`、`executor_id`、`input_ref`、`output_ref`、`rows_read`、`rows_written`、`lineage_ref`、`quality_ref`、`error_code`、`error_message`。

- `mode`：`live|demo`；生产运行只接受 live executor。
- `status`：`pending|running|succeeded|failed|unsupported|cancelled`。
- `succeeded` 必须同时具备真实 executor、开始/完成时间、输出引用及非负计数；不能由调用方直接传入。
- 未注册执行器、Join/SQL 节点、demo pipeline、暂停 schedule 均不得成功。
- error_message 使用公共脱敏器；不记录输入数据正文、凭据或 PII。

## 三、最小实现

- 在 `phase5_pipeline_engine.py` 引入可注入的 executor registry 和 execution evidence；默认无 live executor。
- `run_schedule()` 查 schedule→pipeline→executor；缺失、暂停、demo 或不支持节点时记录 `unsupported/failed`，不伪造行数。
- `trial_run()` 仅在显式提供受支持执行器/输入时执行；旧 demo fallback 明确 `mode=demo,status=unsupported`。
- preview/health 的合成结果加 `mode=demo,synthetic=true`，不得作为落盘、血缘或质量证明。
- 保持既有查询/编辑 API 主结构；必要的旧 `success|ok` 读取兼容只用于历史展示，不再产生新旧值。

## 四、独占文件与验收

- 修改 `aos_api/phase5_pipeline_engine.py`、`routers/phase5_pipelines.py`、对应 schedule/dataset router（如必要）。
- 新增 `tests/test_ec_pipeline_honesty.py`；更新只与错误旧断言相关的 `test_phase5_pipelines.py`。
- 不接入真实 DB/Connector；使用合成 executor 证明成功路径的证据来自实际回调。

负向验收：无 executor、未知 pipeline、demo、暂停 schedule、Join、SQL、executor 异常/超时、缺输出证据、敏感错误。正向验收：合成 executor 实际被调用、计数/引用可追溯、失败不变成功、历史记录一致。阶段回归必须覆盖 Pipeline Builder 和 Phase5 全套既有测试。

## 五、实施结果（2026-08-01）

`2a1e2a3`、`3db47f3`、`84dbb54` 已经总控合并为 `cda42f3`，并由 `f883adf` 更新确定性 OpenAPI。专项 56 passed / 1 skipped；Wave2 最终 full 12/12。生产 resolver 缺失时保持 fail-closed；超时取消为协作式的残余风险继续保留。

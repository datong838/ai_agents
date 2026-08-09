# 228-AIP Evals、发布门控、决策谱系与可观测实施方案

> 状态：**待评审 · 不授权编码**
> 对应阶段：AIP-4、AIP-7（观测侧）。

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

- E0：Eval/OpenTelemetry/Lineage 公共 envelope 冻结。
- E1：六同事 EvalPack registry 与真实数据夹具。
- E2：Logic/Agent publication gate。
- E3：真实 span、token、cost、capability receipt。
- E4：Lineage 页面由真实 run 查询驱动。
- E5：Dashboard persistence、alert ack/silence receipt。

## 7. 验收

- 页面不能手工设置 GREEN。
- 运行 revision 与报告 revision 不一致时发布拒绝。
- 模型 fallback、工具失败、Draft 驳回、unknown external state 均出现在同一谱系。
- 真实 Token/成本缺失时显示 unknown，不用估算补成确定值。
- 双租户查询和导出均隔离；导出脱敏且保留 source metadata。

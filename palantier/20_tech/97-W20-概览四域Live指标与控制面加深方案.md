# 97 · W20 概览四域 Live 指标与控制面加深

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[92](92-W15-概览控制面bp-ui与死代码清理方案.md) · [94](94-W17-Agnes默认接入与LLM回归方案.md)  
> **约束**：无业务主链区块 · Apollo 仅静态后置文案

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 UI |
| 先方案后代码 | 本文 → OverviewPage/DomainGrid |
| 最小更改 | 只读 API 聚合 · 不改 BFF |
| Apollo 延后 | Apollo 面板无 live 舰队指标 |

---

## 1. 范围

| API | 指标 |
| --- | --- |
| `/v1/health` | API 状态 |
| `/v1/aip/models` | sidecar · defaultTextModel · 模型数 |
| `/v1/modules` · `/v1/plugins` · `/v1/aip/tools` | 控制面计数 |
| `/v1/demo/story` | WorkOrder 数 · 待审 Draft · OT 已发布 |
| `/v1/datasets` · `/v1/builds` | L1 数据条数 |
| `/v1/aip/evals/status` | Evals 绿/红 |

UI：`OverviewPage` 聚合 fetch + 刷新；`OverviewDomainGrid` 四域 `BpMetricGrid`；无对象时 Banner 链 `/data`。

---

## 2. 验收

1. `/` 四域面板显示 live 数字 ✅  
2. ensure-seed 后 WorkOrder ≥ 1 ✅  
3. Agnes 配置时 LLM 指标显示 agnes 模型 id ✅  
4. `npm test` + `run-rehearsal-smoke.sh` 绿 ✅  

---

*v1.0*

# 74 · 蓝图深页补齐（非 Apollo）· 运营台 Action / 数据 Router / 计划编辑

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 方案 · 可编码  
> **对齐**：[foundry/html](../foundry/html/) · [43](43-T-UI-S2业务深页按域方案.md) · [70](70-业务平台可演示优先计划.md) · 差距分析（本轮）  
> **工程**：`aos-platform/apps/web` · `services/aos-api`（schedules PATCH 最小）  
> **硬规则**：Apollo 运维 **later**；不动 `*.ps1`；UI 只打 aos-api

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| 最小更改 | 加深现有页；能复用 API 不新建服务 |
| Win/Mac/Linux 分轨 | 不改 Windows 启停打包脚本 |

---

## 1. 目标 / 非目标

| 目标 | 非目标 |
| --- | --- |
| 运营台：行选 → `POST /v1/actions/execute`（HITL Draft） | 像素级复刻 html 动效 |
| 数据连接：Storage Router（`<128KB`）+ 创建 source/sync | Apollo / Ferry |
| 计划编辑器：Cron 表单 + `PATCH /v1/schedules/{id}` | 全量调度引擎 |

---

## 2. 落点

| # | 改动 | API |
| --- | --- | --- |
| A | `InboxPage.tsx` 行选 + 发起申诉/关闭 | 已有 `execute`；需 `Idempotency-Key` |
| B | `DataPage.tsx` Router 向导区 | 已有 `POST /v1/sync-routing` · sources · syncs |
| C | `wave_ext.py` + `SchedulesPage` | **新增** `GET/PATCH /v1/schedules/{id}`；OpenAPI 补一行 |
| D | `api/client.ts` 可选 `apiPost` 额外 headers（或页内 fetch，对齐 DraftInbox） | — |

---

## 3. 验收

1. `/workshop/inbox` 勾选工单 →「提议关闭」→ Draft 出现 → `/aip/drafts` 可批准  
2. `/data` 输入 size → 路由建议正确；可一键建 source+sync  
3. `/data/schedules` 新建/改 Cron → 刷新一致  
4. vitest / 相关 API 单测绿；`health-check` 仍 OK  

---

## 4. 完成判定

- [x] A/B/C 落地  
- [x] 自测：sync-routing · schedules PATCH · actions/execute HITL · vitest 15 绿 · DEMO HEALTH OK  
- [x] 00 索引挂本文  

---

*74 · 蓝图差补三刀 · Apollo later · v1.0 已落地*

# 95 · W18 Buddy 运行态 API 数据与彩排聚合脚本

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[91](91-W14-Workshop运行态链路与Apollo延后方案.md) · [94](94-W17-Agnes默认接入与LLM回归方案.md) · [93](93-W16-Data子页与Graph-Buddy与可演示DoD方案.md)  
> **约束**：Apollo 不深化 · 禁 JSON 主面板 · Buddy 侧栏日志可保留

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 UI |
| 先方案后代码 | 本文 → `BuddyPage` · scripts |
| 最小更改 | 仅 Buddy 页 + 彩排脚本 + 索引 |
| 运行态一致 | 与 Inbox 同 `object-sets/query` · `?order=wo-*` |

---

## 1. 问题

`BuddyPage` 仍用硬编码 `ORD-8821` 演示行，与 Inbox/Graph 的 `wo-1001` 种子不一致；`?order=` 参数被错误映射为 `ORD-*`，导致上下文与 API 对象 id 错位。

---

## 2. 范围

| 项 | 文件 | 动作 |
| --- | --- | --- |
| 工单表 | `apps/web/src/pages/BuddyPage.tsx` | `POST /v1/object-sets/query` 加载 WorkOrder |
| URL 上下文 | 同上 | `?order=wo-*` 原样选中 · 预填提问 |
| objectId | 同上 | `context.objectId = selectedId`（不再 ORD↔wo 转换） |
| 导航 | 同上 | 链 Inbox / Graph · 空表提示去 `/data` 种子 |
| 彩排脚本 | `scripts/demo/run-rehearsal-smoke.sh` | demo-smoke + agnes-smoke（有 .env 时） |

---

## 3. 故事链（S5 · 93 §3.2）

```text
/workshop/inbox → 选中 wo-* → /workshop/buddy?order=wo-*&assist=1
/workshop/graph  → @Buddy 带 order → 同上
Buddy 页表格与 Inbox 同一批 WorkOrder
```

---

## 4. 验收

1. ensure-seed 后 Buddy 表显示 `wo-1001` 等真实行 ✅  
2. 从 Graph/Inbox 带 `?order=` 进入时选中对应行 ✅  
3. `POST /v1/buddy/ask` context.objectId 与选中行一致 ✅  
4. `run-rehearsal-smoke.sh` 绿 ✅  
5. `npm test` 绿 ✅  

---

## 变更日志

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-07-18 | W18 Buddy API 数据 + 彩排脚本 |

---

*v1.0*

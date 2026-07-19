# 218m · Workshop Channel outbox UI

> **版本**：v1.1 · 2026-07-20 · **已编码**（M1-W13b）  
> **对齐**：[212m](212m-Channel-outbox列表与失败重投方案.md) · [101](101-通知通道运行时方案.md)  
> **点名**：用户「按你建议继续干完」→ W13 · 不改 212m API 语义

## 已决

Events 页：列出 `/v1/channels/outbox`；行上「重投」→ `POST …/retry`；刷新可见。

## 落地

| 路径 | 说明 |
| --- | --- |
| `workshop.tsx` `EventsPage` / `formatOutboxRow` | 列表 · 重投 |
| `workshopOutbox.test.ts` | vitest |

## 自检

- [x] vitest：outbox 行渲染助手  
- [x] 重投调用路径可测  

---

*v1.1 · 218m*

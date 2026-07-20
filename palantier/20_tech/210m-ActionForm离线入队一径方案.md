# 210m · Action Form 离线入队一径

> **版本**：v1.1 · 2026-07-20 · **已编码**（M1-W10c）  
> **对齐**：[137](137-TWC8-离线只读待同步方案.md) · [187m](187m-桌面离线Tauri-SQLite方案.md)  
> **点名**：用户「继续」→ W10 · ≠ 全站 Action 编排

## 已决

`ActionFormWidget` 提交 Draft 时若 `OfflineQueuedError` → 提示「已入待同步」而非失败红错；在线路径不变。

## 落地

| 路径 | 说明 |
| --- | --- |
| `canvasWidgets.formatActionSubmitCatch` | queued vs error |
| `ActionFormWidget.runSubmitDraft` | queued → `msg`；error → `err` |
| `wave1.test.ts` | 210m vitest |

## 自检

- [x] vitest：queued 文案  
- [x] 在线错误仍走 error  

---

*v1.1 · 210m*

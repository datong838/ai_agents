# 140 · TWC.11 Buddy 经典三栏并存（UI-13）

> **版本**：v1.0.1 · 2026-07-19  
> **状态**：✅ 方案定稿 · ✅ 已编码 · ✅ 已自测  
> **对齐**：[20c](20c-AOS桌面端详细技术方案.md) §6.13 · UI-13 · [26 §14 TWC.11](26-AOS目标态开发计划.md)

## 目标

| 项 | 规格 |
| --- | --- |
| 默认首页 | 仍为业务座舱 `/`（概览），**不是**三栏 Buddy |
| 并存 | 桌面可开「Buddy 经典三栏」全屏模式（`BuddyLegacyApp`） |
| 入口 | 丝带 + 托盘「Buddy 经典三栏」；可返回座舱 |
| 契约 | 仍走既有 Buddy ask/health URL（v0.1 兼容） |

## 落点

- `apps/desktop/src/App.tsx` · 模式切换  
- `desktop_shell.rs` 托盘项  
- `buddyMode.test.ts`：默认非经典三栏  

## 硬规则

- 禁止把 Buddy 三栏设为安装后默认首页  
- 不删减 Web `/workshop/buddy`  

## 自测

```bash
cd apps/desktop && npm test -- --run src/buddyMode.test.ts src/lib/buddy.test.ts
```

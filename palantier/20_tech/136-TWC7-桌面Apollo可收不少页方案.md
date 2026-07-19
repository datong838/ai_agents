# 136 · TWC.7 桌面 Apollo 可收不少页

> **版本**：v1.0.1 · 2026-07-19  
> **状态**：✅ 方案定稿 · ✅ 已编码 · ✅ 已自测  
> **对齐**：[20c](20c-AOS桌面端详细技术方案.md) §5.4.3 / UI-14 · TWB.2 · [26 §14 TWC.7](26-AOS目标态开发计划.md)

## 目标

| 角色 | 侧栏「运维交付」 | 路由 |
| --- | --- | --- |
| 普通用户 | **默认折叠** | 七页路由仍在，深链可开 |
| `platform_admin` / `developer` / `admin` | **默认展开**（可手收） | 与 Web 同序同全 |
| UI-14 | 桌面丝带「平台管理」→ 展开 + 进 `/apollo` | 非一级推销 |

## 落点（已实现）

| 路径 | 改动 |
| --- | --- |
| `apps/web/src/lib/opsNav.ts` | 角色默认 + `localStorage` 偏好 + `expandOpsNav` |
| `apps/web/src/api/tenant.ts` | `roles`；`aos-tenant-updated` |
| `apps/web/src/shell/AppShell.tsx` | 听 expand / tenant；持久化折叠 |
| `apps/desktop/src/App.tsx` | 丝带「平台管理」`data-ui="UI-14"` |
| `opsNav.test.ts` / `parity.test.ts` | 七页 · collapseDefault · 角色策略 |

## 硬规则

- **禁止**删 Apollo 路由或改 501 空壳  
- 业务座舱仍不以 Apollo 为一级推销

## 自测

```bash
cd aos-platform/apps/web && npm test -- --run src/lib/opsNav.test.ts
cd aos-platform/apps/desktop && npm test -- --run src/parity.test.ts
```

期望：桌面壳 + developer → 默认展开；Web 无壳 → 默认折叠；手点偏好覆盖；Apollo 七 path 齐全。

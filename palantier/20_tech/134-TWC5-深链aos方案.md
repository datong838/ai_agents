# 134 · TWC.5 深链 aos://

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 已编码 · 已自测  
> **对齐**：[20c](20c-AOS桌面端详细技术方案.md) UI-15 §8 · [26 §14 TWC.5](26-AOS目标态开发计划.md)

## 落点

- `deepLink.ts` 白名单解析 · 未登录排队  
- `tauri-plugin-deep-link` · scheme `aos`  
- Toast UI-15  

## 自测

- vitest `deepLink.test.ts` 6 passed


## 目标

| 项 | DoD |
| --- | --- |
| 协议 | `aos://open/<path>` · `aos://auth/callback?...` |
| 白名单 | path 必须落在 `nav.ts` 登记路由（或 open 前缀合法） |
| 未登录 | 先排队 → UI-03 → 再消费 |
| 壳 | `tauri-plugin-deep-link` 注册 scheme `aos` |

## 落点

- `apps/desktop/src/deepLink.ts` 解析/校验/排队  
- App 接入 `onOpenUrl` + Toast  
- `tauri.conf.json` plugins.deep-link

# 128 · TWB.1 Web 可配 API Base

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 已编码 · 已自测  
> **对齐**：[20b](20b-AOS端云分离与交付形态方案.md) C3/C4 · [26 §14 TWB.1](26-AOS目标态开发计划.md)

## 落点

| 项 | 路径 |
| --- | --- |
| Base 门面 | `apps/web/src/api/apiBase.ts` |
| client | `client.ts` → `getApiBase()` |
| UI | `PlatformBaseSwitcher` 顶栏「平台」 |
| 测试 | `apiBase.test.ts` |

## 自测

- vitest 3 passed


## 目标

Web 只调 `aos-api`；API Base 可环境变量默认 + **运行时覆盖**（localStorage），切换私有化/SaaS 域名无需改业务代码。

## 方案

| 项 | 落点 |
| --- | --- |
| 真源 | `apps/web/src/api/apiBase.ts`：`getApiBase` / `setApiBase` / `resolveDefaultApiBase` |
| 默认 | `VITE_AOS_API_BASE` → `http://127.0.0.1:8080` |
| 覆盖 | `localStorage aos-api-base-v1` |
| 消费 | `client.ts` 全部走 `getApiBase()`；`PublishPage` 去散落 |
| UI | 顶栏「平台」轻量输入（不新增 demo 壳） |

## 硬规则

- 禁止页面直连引擎/LLM/Vault  
- Base 变更记 `console.info`（含新 base，无密钥）

## 自测

- vitest `apiBase.test.ts`  
- 改 Base 后 `probeApiHealth` 打到新地址（单测 mock fetch 可选）

# 147 · Web 迁用 ontology-sdk（首刀）

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 方案定稿 · 已编码 · 已测试  
> **对齐**：[146](146-目标态收口与ontology-sdk方案.md) · [69](69-与目标态差距台账.md) · [26](26-AOS目标态开发计划.md) v1.77

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| 最小更改 | 只迁 **读对象 + Draft 列表/创建** 主路径；approve/reject 暂留 `api/client` |
| 不破坏 | 离线队列 / `apiGet` 其它路径不动 |
| R-ARCH | SDK → 仅 aos-api |

## 1. 目标（DoD）

| 项 | 验收 |
| --- | --- |
| 依赖 | `@aos/web` → `@aos/ontology-sdk`（file: 或 alias） |
| 适配层 | `apps/web/src/api/ontologyClient.ts` 接 `getApiBase` + tenant token/org/project |
| SDK 扩展 | `listObjects`/`getObject` 可选 `branch` query |
| 迁页 | `DraftInboxPage` list/create；`OntologyPage` 对象读；`GraphExplorerPage` 对象读 |
| 自测 | web vitest + ontology-sdk vitest 绿 |

## 2. 非目标

- 全站所有 `/v1/objects` 调用一次迁完  
- approve/reject 进 SDK（下一刀可点名）  
- 桌面端同步迁（可跟进，非本刀必须）  

## 3. 落点

| 路径 | 改动 |
| --- | --- |
| `packages/ontology-sdk/src/client.ts` | query `branch` |
| `apps/web/package.json` + `vite.config.ts` | 依赖 / alias |
| `apps/web/src/api/ontologyClient.ts` | 新建 |
| `DraftInboxPage.tsx` · `OntologyPage.tsx` · `s2/workshop.tsx` | 改用 SDK |
| `ontologyClient.test.ts` | mock |

## 4. 风险

| 风险 | 缓解 |
| --- | --- |
| 双轨 | 适配层单一出口；新对象读优先 SDK |
| branch 丢参 | SDK 显式支持 `opts.branch` |

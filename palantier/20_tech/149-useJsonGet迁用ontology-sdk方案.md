# 149 · useJsonGet 钩子页迁用 ontology-sdk

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 方案定稿 · 已编码 · 已测试  
> **对齐**：[148](148-SDK-approve与余页迁用方案.md) · [147](147-Web迁用ontology-sdk方案.md) · [26](26-AOS目标态开发计划.md) v1.79

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| 最小更改 | 只迁仍残留的 objects/drafts `useJsonGet`；不改通用 `useJsonGet` 实现 |
| 不破坏 | wiki / apollo channels / fleet 等非 SDK 路径仍用 `useJsonGet` |

## 1. DoD

| 项 | 验收 |
| --- | --- |
| 钩子 | `useOntologyObject` · `useOntologyDrafts`（`api/ontologyHooks.ts`） |
| WikiPage | 对象读改钩子；wiki 正文仍 `useJsonGet` |
| ApolloChangePage | Drafts 列表改钩子 |
| 清零 | web 内 **无** `/v1/objects/` · `/v1/aip/drafts` 字面路径（含钩子） |
| 自测 | web vitest 绿 + 钩子单测 |

## 2. 非目标

- 把所有 `useJsonGet` 改成 SDK  
- 桌面端 · 停车场项  

## 3. 落点

| 路径 | 改动 |
| --- | --- |
| `apps/web/src/api/ontologyHooks.ts` | 新建 |
| `ontology.tsx` WikiPage | 用 `useOntologyObject` |
| `remainder.tsx` ApolloChangePage | 用 `useOntologyDrafts` |
| `ontologyHooks.test.ts` | mock SDK |

## 4. 自测

```bash
cd apps/web && npm test
rg '/v1/objects/|/v1/aip/drafts' apps/web/src
```

# 148 · ontology-sdk 第二刀 · approve/reject + 余页迁用

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 方案定稿 · 已编码 · 已测试  
> **对齐**：[147](147-Web迁用ontology-sdk方案.md) · [146](146-目标态收口与ontology-sdk方案.md) · [26](26-AOS目标态开发计划.md) v1.78

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| 最小更改 | 补 SDK 写回审批；迁仍用 `apiGet/apiPut/apiPost` 的对象路径 |
| 不破坏 | `useJsonGet` 钩子页（Wiki 读、ApolloChange 草稿列表）本刀不改 |
| 写回 | approve 仍走 HITL；带 Idempotency-Key |

## 1. DoD

| 项 | 验收 |
| --- | --- |
| SDK | `approveDraft` · `rejectDraft` · `putObject`（可选 branch） |
| DraftInbox | approve/reject 走 SDK |
| 余页读/写 | `ObjectTypeDetailPage` · `objectTypeDetail` put · `canvasWidgets` neighbors · Wiki `createDraft` |
| 自测 | sdk + web vitest 绿 |

## 2. 非目标

- 重写 `useJsonGet` 全站  
- 桌面端同步迁  
- 生产 IdP / 真 Notebook  

## 3. 落点

| 路径 | 改动 |
| --- | --- |
| `packages/ontology-sdk/src/client.ts` | extraHeaders · put/approve/reject |
| `DraftInboxPage.tsx` | 去裸 fetch approve |
| `ObjectTypeDetailPage.tsx` · `objectTypeDetail.tsx` · `canvasWidgets.tsx` · `ontology.tsx` Wiki | SDK |

## 4. 自测

```bash
cd packages/ontology-sdk && npm test
cd apps/web && npm test
```

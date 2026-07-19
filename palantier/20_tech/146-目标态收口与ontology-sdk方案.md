# 146 · 目标态主节点收口 · ontology-sdk 最小包

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 方案定稿 · 已编码 · 已测试  
> **对齐**：[20 §3](20-AOS整体技术方案.md) · [69](69-与目标态差距台账.md) · [26](26-AOS目标态开发计划.md) v1.76 · [118](118-产品1.3分析建模阶段退出收口.md) · [31 §9.5](31-波次交付结果台账.md)

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| 主链已齐不瞎开刀 | TB/TA/§14 ✅；停车场（真 Jupyter / Full Spoke / BI 全集）**须人点名** |
| 差距台账「中」可开 | `packages/ontology-sdk` 目标态目录缺口 |
| 最小更改 | 只立薄 SDK；**不**批量改写 `apps/web` 调用点 |
| R-ARCH-01 | SDK 只调 `aos-api` `/v1/*`；无上游 Jupyter/LLM SDK |

## 1. 背景与决策

| 主链 | 状态 |
| --- | --- |
| Wave-0～5 / TB.* / TA.0～8 | ✅ |
| §14 TWA/TWB/TWC（含后置 6/7） | ✅ |
| 蓝图 UI 抛光 | ✅ 冻结 |

**下一刀（本方案自荐、可编码）：** 立 `packages/ontology-sdk` 最小 TypeScript 客户端（20 §3 缺口）。

**仍须人点名（不自动开）：** 真 Notebook 7 · Contour/BI 全集 · Full Spoke/Helm · 生产 IdP 现场联调加深。

## 2. 目标（DoD）

| 项 | 验收 |
| --- | --- |
| 包存在 | `aos-platform/packages/ontology-sdk` |
| 客户端 | `createOntologyClient({ baseUrl, token, orgId, projectId })` |
| 读路径 | `listObjects` · `getObject` · `neighbors` |
| Draft | `listDrafts` · `createDraft`（写回仍走 Draft，禁直写生产旁路） |
| 自测 | vitest mock fetch 绿；日志仅 org/project，无 token 明文 |
| 文档 | 26/69/00 回写；话术「SDK MVP」≠ 多服务拆仓完成 |

## 3. 非目标

- 把 `apps/web` 全部迁到 SDK（可后续点名）  
- Python SDK / 生成 OpenAPI 全量 codegen  
- 拆 `services/ontology` 独立进程  

## 4. 落点

| 路径 | 内容 |
| --- | --- |
| `packages/ontology-sdk/package.json` | `@aos/ontology-sdk` |
| `packages/ontology-sdk/src/client.ts` | fetch + 双头 `X-Org-Id` / `X-Project-Id` |
| `packages/ontology-sdk/src/index.ts` | 导出 |
| `packages/ontology-sdk/src/client.test.ts` | mock 自测 |
| `docs/.../146-…` | 本文 |
| `26` / `69` / `00` | 进度与缺口更新 |

## 5. API 面（首刀）

```text
GET  /v1/objects/{objectType}
GET  /v1/objects/{objectType}/{objectId}
GET  /v1/objects/{objectType}/{objectId}/neighbors
GET  /v1/aip/drafts
POST /v1/aip/drafts
```

## 6. 自测

```bash
cd aos-platform/packages/ontology-sdk && npm test
```

## 7. 风险

| 风险 | 缓解 |
| --- | --- |
| Web 双轨调用 | 首刀不强制迁；README 标明「新代码优先 SDK」 |
| Token 泄漏日志 | 禁止 log Authorization |

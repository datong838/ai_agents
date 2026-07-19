# 150 · 桌面迁用 ontology-sdk（同构座舱）

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 方案定稿 · 已编码 · 已测试  
> **对齐**：[149](149-useJsonGet迁用ontology-sdk方案.md) · [131](131-TWC2-桌面同构主壳方案.md) · [26](26-AOS目标态开发计划.md) v1.80 · R-PARITY-01

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| ≥ Web | 桌面嵌 WebApp；须能解析 `@aos/ontology-sdk`，禁止缩水旁路 |
| 最小更改 | 只补 alias/依赖 + 解析冒烟；不另写桌面对象页 |
| R-ARCH | 仍只调 aos-api |

## 1. 背景

桌面 `App.tsx` → `@aos-web/App`；Web 已迁 objects/drafts 至 SDK。桌面 Vite 若无 `@aos/ontology-sdk` alias，**运行/打包会断**。

## 2. DoD

| 项 | 验收 |
| --- | --- |
| alias | `vite.config.ts` + `tsconfig` paths 指向 `packages/ontology-sdk/src` |
| 依赖 | `package.json` `file:../../packages/ontology-sdk` |
| 冒烟 | 桌面测试可 `import { getOntologyClient } from "@aos-web/api/ontologyClient"` 且 mock 调通 |
| 不双轨 | 无桌面专用 objects/drafts client |

## 3. 非目标

- Buddy 经典三栏另接 SDK  
- 真 Jupyter / Full Spoke  

## 4. 落点

| 路径 | 改动 |
| --- | --- |
| `apps/desktop/vite.config.ts` | alias |
| `apps/desktop/tsconfig.json` | paths |
| `apps/desktop/package.json` | file 依赖 |
| `apps/desktop/src/ontologySdk.desktop.test.ts` | 冒烟 |

## 5. 自测

```bash
cd apps/desktop && npm install && npm test
```

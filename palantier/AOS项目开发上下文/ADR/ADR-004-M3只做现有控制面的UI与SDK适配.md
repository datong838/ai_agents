# ADR-004：M3 只做现有控制面的 UI 与 SDK 适配

- 状态：Accepted
- 日期：2026-08-03

## 决策

M3 在现有 Registry、Composition、Installation Canonical API 之上增加专用 TypeScript adapter 和 FDE 管理 UI。M3 不新增后端表、状态、状态迁移、hash、权限模型、升级 API或真实 Bundle 执行。

## 影响

- 资产页从 `/v1/assets` 切换到 `/v1/asset-bundles`，移除隐式 Mock fallback。
- SDK 映射现有 11 个控制面 operation；不并入 Ontology SDK，不修改通用 client 返回类型。
- 页面只展示服务端 lock/diff/revision/decision/event/evidence。
- 后端缺少的体验能力先以现有 API 组合解决；确属契约缺口时暂停 M3 编码并回到方案/ADR 评审。

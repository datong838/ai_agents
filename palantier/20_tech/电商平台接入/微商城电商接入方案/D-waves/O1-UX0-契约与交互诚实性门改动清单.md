# O1-UX0：契约与交互诚实性门改动清单

> **日期**：2026-08-09
> **状态**：GREEN（2026-08-09，代码 `aos-platform@m1@71f97ea`）
> **目标租户**：`org-org` · `dev-project`（默认工作区）
> **上位方案**：`O1-UX-本体数字孪生九菜单与知识图谱补强方案.md` v1.3

## 1. 本波边界

本波只冻结未来 Exploration/ObjectSet/GraphSnapshot 契约，并修复当前对象探索的明确错误和假成功。不得提前建设 UX1 全宽布局、UX2 PostgreSQL 持久化或 UX4 图渲染画布。

## 2. 代码改动清单

### 2.1 契约

- [x] 新增后端 Exploration、ObjectSet、GraphSnapshot DTO 与冻结错误码；DTO 不允许客户端提交 `org_id/workspace_id`。
- [x] 新增前端对应 TypeScript 契约，字段与后端命名一一对应。
- [x] 增加契约测试：合法 DTO、未知字段拒绝、hops/maxNodes 上限、跨类型 ObjectSet 拒绝、错误码集合冻结。

### 2.2 对象探索

- [x] 保留邻居 `type`，节点 key 使用 `type + id + rel`，跨类型点击读取正确 Object Type。
- [x] 修复跨类型跳转后类型选择器、URL、详情和对象列表上下文一致性；补充 `niushop:<site>:<source_pk>` 稳定引用到列表对象 ID 的解析。
- [x] 移除多标签、新建对象集、高级筛选图标、列设置、注释、展开、更多等未实现主工具栏控件。
- [x] 移除“共享/保存”地址栏 Toast 假成功；UX2 真持久化完成前不展示主按钮。
- [x] 为图谱节点构建和跨类型选择补前端失败测试。

### 2.3 九页面交互诚实性

- [x] 为 `/workshop/graph`、`/ontology/funnel`、`/ontology/okf-funnel`、`/ontology/okf-overview`、`/ontology/wiki`、`/ontology/wiki-index`、`/ontology/branches` 补 `interactionHonestyManifest`。
- [x] 保留既有 `/ontology`、`/ontology/graph-health` 登记并核对描述。
- [x] 增加清单唯一性、九路由覆盖及测试文件存在性验证。

## 3. 预计文件

### AOS 代码

- `apps/web/src/pages/s2/workshop.tsx`
- `apps/web/src/pages/s2/workshop.test.ts`
- `apps/web/src/api/ontologyExplorerContracts.ts`
- `apps/web/src/api/ontologyExplorerContracts.test.ts`
- `apps/web/src/interactionHonestyManifest.ts`
- `apps/web/src/interactionHonestyManifest.test.ts`
- `services/aos-api/aos_api/ontology_explorer_contracts.py`
- `services/aos-api/tests/test_ontology_explorer_contracts.py`

### 文档

- 本清单
- `O1-UX-本体数字孪生九菜单与知识图谱补强方案.md`
- `AOS项目开发上下文/09-2026-08-09-O1-UX0执行对账.md`

## 4. 验证门

- [x] 后端契约及既有对象路由测试通过：`15 passed`。
- [x] 前端对象探索/契约/Manifest 针对性测试通过；全量前端为 `154 files / 2012 tests`。
- [x] TypeScript `--noEmit` 通过。
- [x] 内置浏览器确认 `org-org/dev-project`，真实 `Order/1 → OrderLine/2` 跨类型邻居可正确打开。
- [x] 对象探索主工具栏不存在假成功和不可用占位按钮。
- [x] 页面刷新后 URL、类型和对象选择保持一致。
- [x] Git diff 只包含本波文件，用户 `services/aos-api/uv.lock` 未触碰。

## 5. 退出条件

以上门禁全部通过后，本波才可标记 GREEN。下一波只能建议 O1-UX1，不在本波隐式实施。

## 6. 完成结论

O1-UX0 已达到退出条件并标记 GREEN。代码已提交并推送至 `m1@71f97ea`。本波只冻结契约、修复跨类型选择和清理假功能，没有实现探索资产持久化、全宽布局或新图画布。下一波为 O1-UX1：专用全宽只读探索布局与详情抽屉。

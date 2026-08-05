# TI-5 C2-A 关键 Singleton 隔离证据

> 日期：2026-08-04
> 代码：`m1@a302544`
> 结论：C2-A GREEN；C2 总门未完成，下一门 C2-B

## 1. 实施范围

- `aip_model_catalog.ModelCatalogEngine`：CRUD、list、容量与 reset 使用 `(org_id,project_id,item_id)`。
- `phase5_pipeline_engine`：Dataset、Build、Health、SyncConfig 四组容器使用 `(org_id,project_id,resource_id)`。
- `aip_model_catalog_router.py` 与 `routers/phase5_datasets.py` 从认证 Principal 构造 TenantScope，每次调用显式传入。
- `seed_phase5_pipeline(scope)` 不再隐式写全局 Dataset；测试专用全清方法命名为 `reset_all_for_tests()`，未暴露给生产路由。
- 未新增数据库表，公开响应 DTO 未改变。

## 2. 负向证明

- Model Catalog 同一 item ID 可在两个 scope 共存，详情与更新按 scope 命中。
- Model Catalog 容量限制按 scope 单独计算；A 满额不阻断 B。
- Phase5 同一 Dataset/Build ID 可跨 scope 共存，Build、Health 与 SyncConfig 不串租户。
- A scope reset 后，B scope 的 Dataset 与 Build 仍存在。
- 两组路由未认证均返回 401；A 创建的资源在 B scope 详情返回 404，B 列表不出现 A 数据。

## 3. 验证结果

- C2-A 专项与 AIP Catalog、Phase5、诚实执行相关回归：77 passed。
- Tenant Isolation 累计：206 passed / 8 skipped。
- 全量测试收集：9,199 collected，零收集错误。
- 静态语法/未使用符号门：修改文件 `ruff --select F,E9` GREEN。
- `m1` 与 W1/W2/W3/W4：HEAD `a302544`，tree `4481f57d1011138138ac5094e68468e59f55fa8b`；四个 worker clean，主工作树仅保留用户掘金文档改动。

## 4. 已登记剩余风险

- `/v1/datasets` GET 存在 Phase5 与 `wave_ext` 重复路由；当前有效响应来自 wave_ext，不能仅凭 Phase5 Router scoped 就宣告 URL 真源已统一。
- `wave_ext` 的 `_datasets/_media/_media_bytes` 仍需在 C2-B 按 scope 分桶，并覆盖关联 analytics/read/delete/clear。
- Phase5 的 Pipeline/Node/Schedule 等非本子波进程态需进入剩余 finding 分类，不能被 C2-A 结果自动标绿。

## 5. 2026-08-05 接续复验

- 执行：`pytest tests/tenant_isolation/test_ti5_c2a_singleton_scope.py tests/test_aip_model_catalog.py tests/test_phase5_pipelines.py tests/test_ec_pipeline_honesty.py` → **77 passed**。
- 执行：`pytest tests/tenant_isolation` → **206 passed / 8 skipped**。
- Git：`aos-platform` 与 w1–w4 均为 `a302544` / tree `4481f57d1011138138ac5094e68468e59f55fa8b`；四 Worker clean；主工作树仅保留用户 `docs/toutiao-series/*`。
- 结论：维持 C2-A GREEN；下一门仍为 C2-B，未授权前不启动。

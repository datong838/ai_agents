# TI-2 E2-C Deployment/Theme/Widget Catalog 显式 TenantScope 证据

> 日期：2026-08-04
> 代码基线：`aos-platform m1@87d6ef5`
> 结论：GREEN

## 本波范围

- Module Deployment list/deploy/get/rollback 同时约束 TenantScope、module_id 与 deployment_id，记录实际 Principal subject。
- Theme list/get/create/update/delete 全链 TenantScope；跨租户全局 ID 冲突失败关闭。
- Widget Catalog list/get/create 全链 TenantScope；跨租户全局 ID 冲突失败关闭。
- Variable usage/ref 扫描复用已显式隔离的 Widget Instance 与 Query Store。

## 修改文件

- `services/aos-api/aos_api/module_deployments.py`
- `services/aos-api/aos_api/routers/modules_deployments.py`
- `services/aos-api/aos_api/themes.py`
- `services/aos-api/aos_api/routers/themes.py`
- `services/aos-api/aos_api/widget_catalog.py`
- `services/aos-api/aos_api/routers/widgets_registry.py`
- `services/aos-api/tests/tenant_isolation/test_ti2_e2a_module_scope.py`
- `services/aos-api/tests/test_phase5_regression.py`

## 验证结果

| 门禁 | 结果 |
|---|---|
| E2-C + Workshop + 相关 Phase 5 | 46 passed，7 个既有 warning |
| 租户隔离 + Module Event 累计 | 91 passed，7 个既有 warning |
| Ruff（本波生产文件与租户测试） | GREEN |
| Python compileall / `git diff --check` | GREEN |
| 五分支 | 本地/远端均为 `87d6ef5`，tree `d2c91ef1...` |

## 已知测试债务

扩展运行整个 `test_phase5_regression.py` 时，独立临时数据库中 2 项 Model Catalog 测试因其自身未显式 seed 而失败；失败不涉及本波文件或 TenantScope。相关 Widget/Theme 4 项已在 Workshop seed 同一会话中单独通过。本证据不把这 2 项旧种子依赖写成 GREEN，也不为本波扩大修复范围。

## 风险与下一门

- 当前 Theme/Widget Catalog 是租户目录，尚未完成 Platform Template 与租户安装实例的最终拆分。
- 遗留全局 ID 通过失败关闭防串写，不等于同 ID 双租户复用已完成。
- 下一门为 E2-D：Module aggregate、静态默认常量门和 APP-01～APP-05 基础。

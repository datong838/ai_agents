# TI-2 E2-B Query/Event/Interface 显式 TenantScope 证据

> 日期：2026-08-04  
> 代码基线：`aos-platform m1@5df9b5e`  
> 结论：GREEN

## 本波范围

- Query 创建、单查、删除按 `TenantScope + module_id + query_id` 定位；列表沿用 E2-A 已完成的 TenantScope。
- Event seed/list/create/get/update/delete 全链由 Router Principal 显式传入 TenantScope。
- Interface get/put 按 TenantScope 定位；遗留全局 `module_id` 被其他租户占用时失败关闭，不覆盖原租户。
- 不回填 `module_pk`，不启用 RLS，不改变 Installation/M2-B 架构，不连接真实微商城。

## 修改文件

- `services/aos-api/aos_api/module_queries.py`
- `services/aos-api/aos_api/module_events.py`
- `services/aos-api/aos_api/module_events_router.py`
- `services/aos-api/aos_api/module_interfaces.py`
- `services/aos-api/aos_api/routers/modules_interface.py`
- `services/aos-api/tests/tenant_isolation/test_ti2_e2a_module_scope.py`

## 验证结果

| 门禁 | 结果 |
|---|---|
| Query/Event/Interface + Workshop/Phase C 累计 | 47 passed，7 个既有 warning |
| `tests/tenant_isolation` 全量 | 80 passed，7 个既有 warning |
| Python compileall | GREEN |
| `git diff --check` | GREEN |
| 五分支 | 本地/远端均为 `5df9b5e`，tree `1f784ca6...`；四 Worker clean，主树仅保留用户掘金文档 |

## 风险与边界

- 遗留表仍以全局资源 ID/module_id 为主键；本波通过失败关闭阻止串写，但尚不能让两个租户创建同名同 ID 实例。
- `module_pk` 回填、复合键切换、RLS 与 Contract 属于后续 E3～E7，不得将本波描述为 Module 全域隔离完成。
- TI-1 的 59 条逻辑 QUARANTINE 仍存在，E4 继续 BLOCKED。

## 下一门

进入 E2-C：Deployment、Theme、Widget Catalog 与 usage/ref 扫描显式 TenantScope；完成后继续 E2-D 聚合路径与默认常量门。

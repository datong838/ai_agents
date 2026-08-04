# TI-2 E2-D Module Aggregate 与默认租户静态门证据

> 日期：2026-08-04
> 代码基线：`aos-platform m1@472728e`
> 结论：GREEN（E2 总体 GREEN；APP-04/05 未完成）

## 本波范围

- Module seed/list/get/create/update/touch/publish/runtime 统一以 TenantScope 为首参。
- Router 只从已验证 Principal 构造 TenantScope，Store 不接受 body 租户字段。
- 10 个 E2 运行时 Store 禁止 `_DEFAULT_ORG/_DEFAULT_PROJECT` 标识重新进入。
- 测试组织种子显式指定 `dev-org/dev-project`，栖月汇/其他组织不被隐式灌入。

## 修改文件

- `services/aos-api/aos_api/module_store.py`
- `services/aos-api/aos_api/routers/modules.py`
- `services/aos-api/aos_api/main.py`
- `services/aos-api/aos_api/demo/module_seed.py`
- `services/aos-api/tests/conftest.py`
- `services/aos-api/tests/test_phase5_regression.py`
- `services/aos-api/tests/tenant_isolation/test_ti2_e2d_module_aggregate_scope.py`

## 验证结果

| 门禁 | 结果 |
|---|---|
| Module aggregate/API/幂等/Workshop | 56 passed，7 个既有 warning |
| `tests/tenant_isolation` | 87 passed，7 个既有 warning |
| 10 Store 默认租户标识静态门 | 0 命中，GREEN |
| Ruff（忽略目标文件既有 B008/BLE001） | GREEN |
| compileall / `git diff --check` | GREEN |
| 五分支 | 本地/远端均为 `472728e`，tree `70121cef...` |

## APP-01～APP-05 对账

| 验收 | 当前结论 |
|---|---|
| APP-01 测试组织应用 | 基础 GREEN：显式种子后可见 |
| APP-02 栖月汇空态 | Module 基础 GREEN：不会被测试组织种子灌入；全域空证明仍 YELLOW |
| APP-03 栖月汇安装订单管理 | 基础 GREEN：随机实例 ID 下创建只进入当前 Scope；正式模板安装仍走后续 Installation/Module 绑定 |
| APP-04 两组织同 module_id | 未完成：遗留全局主键仍阻止同 ID 共存，等待 E3～E7 |
| APP-05 删除订单管理 | 未完成：尚无 Module 软删除/卸载 API，等待读切换后的删除能力 |

## 下一门

进入 TI-2 E3：为既有 `meta_module` 与子资源生成稳定 module_pk/module_id 身份映射，采用可审计、可恢复、可回滚的非生产回填；不得直接改主键或启用 RLS。

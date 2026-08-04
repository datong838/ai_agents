# 228 · TI-2 E5 Module 实例键读切换实施方案

> 版本：v1.0 · 2026-08-04  
> 状态：评审通过 / 执行中  
> 前置：TI-2 E4 `129d438` GREEN；共享非生产 11/11 Module 身份 FK validated

## Rules

先方案后代码；只把 Module aggregate 与 7 张直属子表的内部寻址从遗留 `module_id` 切到 `(org_id, project_id, module_pk)`，外部路径参数和响应 `moduleId` 保持不变。不改表结构、主键、业务行和 OpenAPI，不启用 RLS，不处理模板/Overlay Contract。对读不一致必须失败关闭，不能静默回退到遗留键。

## 目标与非目标

目标：

1. API `module_id` 经稳定 UUIDv5 解析为租户内 `module_pk`。
2. 父 Module 新键读与遗留 scoped 读做影子对读；缺失、错绑或不一致抛出明确 drift，禁止跨租户降级。
3. Canvas、Deployment、Event、Interface、Query、Variable、Widget Instance 的 list/get/update/delete/seed/read-after-write 使用 `module_pk + TenantScope`。
4. 两条无父 Event 继续 quarantine，并在新读路径中不可见。
5. 响应与 Router 合约不变；现有调用者无需感知 UUID。

非目标：

- E5 不解决遗留全局 PK/unique 对相同业务 ID 的写入冲突；APP-04 需在 E7 Contract/主键收口后 GREEN。
- E5 不实现组织卸载或物理删除；APP-05 保持未完成。
- 不把 Theme/Widget Catalog 平台模板目录误并入 Module 实例身份。

## 实现范围

| 文件 | 变更 |
|---|---|
| `aos_api/module_identity.py` | 新键解析、遗留影子对读、drift 失败关闭 |
| `aos_api/module_store.py` | get/update/touch 改按稳定 module_pk + scope 寻址 |
| `aos_api/canvas_config.py` | Canvas 读与 upsert 后回读按 module_pk |
| `aos_api/module_deployments.py` | list/get/rollback 目标按 module_pk |
| `aos_api/module_events.py` | seed/CRUD 按 module_pk；孤儿事件不可见 |
| `aos_api/module_interfaces.py` | get/upsert 后回读按 module_pk |
| `aos_api/module_queries.py` | list/get/delete 按 module_pk |
| `aos_api/module_variables.py` | list/get/update/delete/usage 链按 module_pk |
| `aos_api/widget_instances.py` | list/get/update/delete 按 module_pk |
| `tests/tenant_isolation/test_ti2_e5_module_read_switch.py` | 新键读取、跨租户、drift、孤儿隐藏、无 legacy child predicate |

## 影子对读规则

对同一 `(scope, module_id)` 同时检查：

- 新键：`module_pk = stable_module_pk(scope, module_id)`；
- 遗留键：`id = module_id`，仍附带同一 scope。

两者均不存在时返回 not found；两者必须指向同一行且 `module_id/id/module_pk` 自洽。任何单边存在或字段不一致均抛 `ModuleIdentityDriftError`，记录脱敏 scope 与 module ID，不返回另一租户数据。

## 回滚

E5 为代码读切换，不含 DDL/DML。回滚只需回退本波代码提交；E3 身份和 E4 validated FK 保持不变。禁止通过删除 module_pk 或撤销 E4 FK 代替代码回滚。

## 退出门

1. 新键/遗留键影子对读一致，负向 drift 失败关闭。
2. 7 张直属子表的业务读改删 SQL 不再以 `module_id` 作为父身份谓词。
3. 跨组织、跨工作区读取均为 not found/空；两条 orphan Event 新读不可见。
4. Router/OpenAPI 响应保持 `moduleId`，不泄漏内部 UUID。
5. Tenant Isolation + Workshop 累计回归 GREEN；共享库只读核对 160/462/2 守恒、栖月汇 Module 0、RLS 0。
6. m1 与四 Worker 同步后进入 E6 RLS；APP-04/05 仍不得标绿。

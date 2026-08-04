# 228 · TI-3 E5 Object Runtime 租户读切换与旁路收口实施方案

> 版本：v1.0 · 2026-08-04  
> 状态：执行中  
> 前置：TI-3 E4 `c268062` GREEN；9/9 workspace FK validated；1,030 行中 37 条 NULL quarantine

## Rules

先方案后代码；E5 只把 Object Runtime 的所有可达读路径统一切到 `(org_id, project_id, 业务键)`，并补齐测试组织 seed/clear 与向量自动取样旁路的显式 scope。外部对象 ID、Router、OpenAPI 和响应不变。不改 DDL、主键、历史业务行，不启用 RLS，不把 37 条 quarantine 默认归属测试组织。发现其他组织或 NULL scope 的同业务键时只隐藏/失败关闭，禁止无 scope 回退。

## 当前事实与缺口

TI-3 E2 已完成主要生产 Router/Store 的显式 TenantScope，E4 已验证 workspace FK；全包静态审计仍发现三类旁路：

1. `vector_index` 的 `autoSample` 从 `obj_instance` 全局取 WorkOrder，虽然 collection 已加租户前缀，样本来源仍可能串租户。
2. `demo_story` 与 `order_seed` 的对象读取未限定测试组织工作区。
3. `demo/workorder_seed.py`、`demo/seed.py` 的测试数据写入/清理仍有无 scope SQL；若只切读，会造成新 seed 不可见或误清其他组织。

Connector 的无 scope Object 写入另属 TI-4；TI-3 E5 不伪装其已完成，但必须在门禁中显式列为 deferred，并保证当前真实平台连接继续暂停。

## 实施范围

| 文件 | 动作 |
|---|---|
| `aos_api/vector_index.py` | autoSample 强制传入 TenantScope，PG 取样双租户过滤 |
| `aos_api/routers/wave_ext.py` | 从 Principal 向 vector upsert/embed 传 TenantScope |
| `aos_api/demo/demo_story.py` | 所有 Object/Draft 演示读取固定显式测试 TenantScope |
| `aos_api/demo/order_seed.py` | Order count/insert 显式测试 scope，禁止生成 NULL scope 新数据 |
| `aos_api/demo/workorder_seed.py` | Object/Graph/Funnel 测试 seed 写入显式测试 scope |
| `aos_api/demo/seed.py` | clear 仅删除 `dev-org/dev-project`，不触碰其他工作区 |
| `tests/tenant_isolation/test_ti3_e5_object_runtime_read_switch.py` | 双租户 autoSample、demo/seed 静态门、quarantine 不可见、TI-4 deferred 清单 |

## 读切换与失败关闭规则

1. 业务读必须同时出现 org/project 谓词；只按业务 ID、只按 org 或默认无 scope 均视为门禁失败。
2. `autoSample` 没有 TenantScope 时直接拒绝，不能用 collection 前缀代替数据源 scope。
3. 测试演示只能显式使用 `dev-org/dev-project`；清理必须同样双条件约束。
4. NULL quarantine 与其他租户同键数据均不可见；E5 不提供遗留全局 fallback。
5. Connector 写路径保留为 TI-4 明确阻断项，不因 E5 GREEN 而解除真实平台连接禁令。

## 回滚

E5 不含数据库迁移和历史 DML。回滚只回退本波代码；E4 validated FK 保持不变。不得以撤销 E4、给 quarantine 填默认 scope 或放宽静态门作为回滚手段。

## 退出门

1. vector autoSample 在相同 Object ID/类型的跨租户夹具中只取得当前 scope 数据；缺 scope 失败关闭。
2. demo story、Order/WorkOrder seed 与 clear 的目标 SQL 全部含 org/project；跨租户 hash/计数不变。
3. 37 条 NULL quarantine 继续不可见且行数不变；共享开发库只读核对 1,030/37/0 守恒。
4. 生产 Object Runtime SELECT 静态门覆盖全 `aos_api`；TI-4 Connector deferred 清单精确、不可静默扩大。
5. Tenant Isolation 与相关 vector/demo 专项累计 GREEN；五分支同步。
6. 下一门为 TI-3 E6 RLS；不提前修改主键/NOT NULL/Contract，不开始真实微商城接入。

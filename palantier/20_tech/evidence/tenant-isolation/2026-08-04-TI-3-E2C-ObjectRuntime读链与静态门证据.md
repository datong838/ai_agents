# 228 · TI-3 E2-C Object Runtime 读链与静态门证据

> 日期：2026-08-04
> 结论：GREEN；TI-3 E2 总收口
> 代码基线：`m1@5e58768`

## 1. 交付

- Object/Branch effective view、Object Set、Tool、Marking、Graph、Funnel 与 Analytics 对象读取统一 TenantScope。
- Branch list/diff/change-count 和 merge/checkout 事务使用同一 scope。
- Graph health 聚合只统计当前组织/工作区的实例、边、孤儿、悬空边和属性冲突。
- 删除请求期 `ensure_overlay_table` DDL；Schema 只由启动与迁移创建。
- 增加 tenant-owned SQL 静态门，并对 TI-4/TI-5 deferred 资源做注册表存在性阻断检查。

## 2. 负向证明

| 场景 | 结果 |
|---|---|
| A/B scope 各有不同 Object | Object Set 与 Tool 各自只返回本 scope |
| A scope 有 Graph edge，B 查询同 source | B 返回空列表 |
| A scope 有 Funnel status，B 查询 | B 返回 404 |
| Branch Store 调用缺 scope | 公共签名无默认值，调用期失败 |
| 目标运行 SQL 缺 org 或 project 条件 | 静态测试失败 |
| 降权运行角色执行请求期 DDL | 路径已移除，不再触发 schema 权限错误 |

## 3. 验证

- E2-C 专项：2 passed。
- E2-A/B/C + Object/Graph/Branch/Marking/Tool 累计：144 passed、40 skipped、0 failed。
- Python 编译、Ruff `E9/F/I`（本波目标文件，不含既有 `wave_ext` 全文件历史债务）与 `git diff --check`：GREEN。
- 五分支本地/远端：`5e58768`。

## 4. 未越界项

- `mssql_connector.py`、`pg_connector.py`、`mysql_connector.py`、`connector_runtime.py` 的 Object 写入归 TI-4；E2-C 只登记阻断，不提前改 Connector。
- `vector_index.py` 的 Object sample 与 tenant-vector-records 归 TI-4/TI-5。
- `decision_lineage` 631 条历史归属及 Analytics lineage 读取归 TI-5。
- Demo seed/repair 仅是测试组织维护路径，需在 TI-3 E3 后按确定性归属处理，不作为生产读取 fallback。
- 具体微商城 API、Schema、凭据和数据仍未接入。

## 5. 下一门

先形成并评审 TI-3 E3 Object/Graph/Draft/Wiki 历史归属隔离与可逆回填方案；任何无法证明归属的行进入隔离，不按默认组织、创建时间或 ID 猜测。

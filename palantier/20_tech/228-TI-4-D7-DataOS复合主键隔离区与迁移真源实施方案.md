# 228 · TI-4 D7 Data OS 复合主键、隔离区与迁移真源实施方案

> 版本：v1.0 · 2026-08-04
> 状态：评审授权链内，待执行
> 前置：TI-4 D6 GREEN；代码 `m1@3e9677f`；Alembic `228ti4d6rls`

## Rules

先方案后代码；只收口 D1～D6 已验证的 Data OS 租户身份，不重设计 Source、Pipeline、Dataset、Sync、Schedule 或 Graph。293 条未知归属历史不得猜测归属或删除，必须在完整备份、逐表行数和 payload 哈希守恒下原样迁入运行角色不可访问的不可变维护隔离区。升级与降级必须可验证、碰撞时失败关闭；现有外部业务 ID 和 API 字段保持不变。具体微商城 Connector 继续禁止开始。

## 1. 现状与边界

共享开发库 7 表共 297 行：`meta_source` 4 行已有 scope，其余 293 行均缺少完整 TenantScope。D3 已逐条形成 `NO_ACTION=4 / QUARANTINE=293` 的不可变控制账本；D4 已验证 7 个 workspace FK；D5 已切严格 scope 读取；D6 已启用 7/7 FORCE RLS。

剩余结构风险：

1. 293 条逻辑隔离数据仍位于活跃表，scope 可空；owner 维护连接仍可直接看到。
2. 7 表仍以 `id/rid/pipeline_id` 等全局键为主键，同一业务 ID 无法在两个工作区共存。
3. `data_os_store.ensure_data_os_schema()` 仍包含运行时 `CREATE TABLE IF NOT EXISTS`，与 Alembic 真源并存。
4. Source→Pipeline→Dataset→History/Sync/Schedule/Graph 的父子关系尚未由 scoped 复合 FK 固化。

## 2. 目标 Contract

### 2.1 scoped 主键

| 表 | D7 主键 |
|---|---|
| `meta_source` | `(org_id, project_id, id)` |
| `meta_pipeline` | `(org_id, project_id, id)` |
| `meta_dataset` | `(org_id, project_id, rid)` |
| `meta_dataset_history` | `(org_id, project_id, id)` |
| `meta_sync` | `(org_id, project_id, id)` |
| `meta_schedule` | `(org_id, project_id, id)` |
| `phase5_pipeline_graph` | `(org_id, project_id, pipeline_id)` |

7 表的 `org_id/project_id` 全部 `NOT NULL`。API 中 `id/rid/pipelineId` 继续是当前租户内业务标识，不改外部协议。

### 2.2 scoped 父子关系

- Pipeline 的非空 `source_id` → 同 scope Source。
- Dataset 的可选 `source_id`、`pipeline_id` → 同 scope Source/Pipeline。
- Dataset History 的 `dataset_rid` → 同 scope Dataset。
- Sync 的 `source_id` → 同 scope Source。
- Schedule 的可选 `pipeline_id` → 同 scope Pipeline。
- Pipeline Graph 的 `pipeline_id` → 同 scope Pipeline。

新增父子 FK 前必须验证 4 条 active scoped 记录无断链；历史未知行先进入隔离区。删除语义保持现有服务层显式顺序，不在本波擅自引入级联删除。

### 2.3 不可变维护隔离区

新增 `data_os_orphan_quarantine`，保存 `source_table`、稳定 `source_key`、原始整行 JSONB `payload`、`payload_hash`、`reason_code`、D3 batch/decision 证据引用、`source_revision` 与时间戳。

- 只从 D3 已判定 `QUARANTINE` 的 293 条记录迁入；逐条核对稳定 key 与 before hash。
- `REVOKE ALL ... FROM aos_runtime`；UPDATE、DELETE、TRUNCATE 由 guard 阻断。
- 升级必须满足：迁入数 = 从活跃表移出数 = 293，且活跃 4 + 隔离 293 = 原总量 297，payload hash mismatch=0。
- 降级只在旧全局键未被 D7 后数据占用时原样恢复；有碰撞即 BLOCKED，转完整备份恢复，不覆盖新数据。

## 3. 现有代码能力映射

| 能力 | 当前代码 | D7 最小改动 |
|---|---|---|
| Source/Pipeline/Dataset/Sync/Schedule persist | `aos_api/data_os_store.py` | `ON CONFLICT` 改为 scoped 复合键，保留 TenantScope 与返回语义 |
| Graph persist | `aos_api/data_os_store.py` | conflict target 改 `(org_id, project_id, pipeline_id)` |
| Dataset History replace | `aos_api/data_os_store.py` | 维持 scoped delete/insert，主键由数据库序列生成 |
| scoped read/delete | `data_os_store.py`、`routers/wave_ext.py` | 保持 D5 已完成的双 scope 条件，不重新设计缓存 |
| runtime schema | `ensure_data_os_schema()` | 应用运行期只做迁移 revision/schema readiness 检查，不再执行建表 DDL |
| fresh database migration | Alembic D1/D7 | 由迁移链负责创建/收紧 Data OS 基表；测试夹具不得作为生产 schema 真源 |
| schema lint | `tenant_schema_lint.py` | 冻结 PK、NOT NULL、父子 FK、隔离区权限/guard 和 Alembic revision |

## 4. 实施拆分

### D7-A 只读预检与备份

1. 冻结 `228ti4d6rls`、297/293/4、D3 batch 和 7 表哈希。
2. 检查 scoped 键重复、父子断链、旧 FK 引用和降级冲突。
3. 生成 mode 0600 的完整 PostgreSQL custom-format 备份，记录 bytes 与 SHA-256。

### D7-B Migration Contract

1. 新 revision `228ti4d7contract`，down revision `228ti4d6rls`。
2. 新建不可变隔离表和 guard；按 D3 决策原样迁移 293 条。
3. 删除未知行后将 7 表 scope 收紧为 NOT NULL。
4. 替换 7 个旧全局主键为 scoped 主键。
5. 新增并验证 scoped 父子 FK。
6. 实现带碰撞 precheck 的可逆 downgrade。

### D7-C 应用映射与迁移真源

1. 将 6 类 persist/Graph 的 conflict target 映射到 scoped Contract。
2. 把运行时建表替换为 schema/revision readiness 检查；启动不得 ALTER/CREATE 业务表。
3. 补充 fresh DB migration、双租户同 ID、父子跨 scope 拒绝、隔离不可变和 downgrade collision 测试。

### D7-D 验证与收口

1. 隔离测试库执行 `upgrade → downgrade → upgrade`，验证原样往返。
2. 共享开发库在备份后执行同等演练，最终保持 D7。
3. 两个 scope 使用相同 Source/Pipeline/Dataset/Sync/Schedule/Graph ID，互不覆盖。
4. D7 专项、Data OS、Connector、Tenant Isolation 累计回归全部 GREEN。
5. 证据、总方案、AOS 上下文与五分支同步。

## 5. 退出门

1. 活跃 4 + 隔离 293 = 297，hash mismatch=0；D3 决策引用完整。
2. 7 表 scope NOT NULL、7 个 scoped 主键、目标 scoped 父子 FK 全部有效。
3. 7/7 FORCE RLS 保持；`aos_runtime` 无隔离区权限，隔离记录不可改删截断。
4. 同 ID 双租户可共存，跨 scope 父子引用和写入失败关闭。
5. 应用运行期不再建 Data OS 表；fresh database 只靠迁移链得到目标结构。
6. 降级在无碰撞时原样恢复；有碰撞明确 BLOCKED。
7. 五分支和远端同 HEAD/tree，文档与代码一致后 D7 才可 GREEN。

## 6. 风险与回滚

| 风险 | 等级 | 控制 |
|---|---|---|
| 293 条历史丢失或错误归属 | P0 | D3 决策绑定、完整备份、原始 payload/hash、守恒与可逆演练 |
| PK 变化导致 upsert 失效 | P0 | 同波修改全部 Data OS conflict target，双租户同 ID 回归 |
| scoped 父子 FK 误阻断合法写 | P1 | 先校验实际父子语义，可选引用保留 NULL，跨 scope 负向测试 |
| 移除 runtime DDL 后空库不能启动 | P0 | fresh DB Alembic head 测试；启动只在 revision 不足时明确失败 |
| D7 后同 ID 导致旧全局键不可恢复 | P1 | downgrade collision precheck；冲突时停止并使用完整备份 |

## 7. D7 后边界

D7 只完成 Data OS Contract。完成后仍需对 5 张电商 Connector 真源表补齐 Validate/RLS/数据库 Contract，并完成 TI-5 非表资源及 AIP/Analytics 边界和 TI-6 空数据证明；全部 GREEN 后才达到“可开始微商城接入”的前期条件。

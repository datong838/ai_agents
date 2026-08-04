# 2026-08-04 · TI-3 E7 Object Runtime 复合主键与隔离区 Contract 证据

> 状态：GREEN / TI-3 E1～E7 总收口完成
> 代码：`aos-platform m1@fd2a124`
> 文档方案：`228-TI-3-E7-ObjectRuntime复合主键与隔离区Contract实施方案.md`
> 最终 Alembic：`228ti3e7contract`

## 1. 交付结论

1. 9 张 Object Runtime 活跃表的 `org_id/project_id` 全部 NOT NULL，主键全部收口为 TenantScope 复合主键。
2. `obj_branch_overlay` 到 `meta_branch` 的旧全局外键已替换为 `(org_id, project_id, branch_id)` scoped 复合外键。
3. 37 条未知归属历史记录未删除、未默认归测试组织或栖月汇；已原样进入 `object_runtime_orphan_quarantine`：`obj_instance 31 / meta_branch 3 / graph_edge 2 / funnel_status 1`。
4. 隔离表保存原始 JSONB payload 与可复核 MD5，hash mismatch=0；UPDATE/DELETE/TRUNCATE guard 为 2，`aos_runtime` 无 SELECT/INSERT/UPDATE/DELETE 权限。
5. Object、Wiki、Graph、Branch、Overlay、Funnel、Lifecycle 与测试组织 seed 的既有写路径已映射到 scoped conflict target；API 与外部业务 ID 未改变。
6. 两个 TenantScope 可复用相同 Object/Branch/Funnel/Wiki/Draft/Lifecycle 业务 ID，RLS 下互相不可见；overlay 不能跨 scope 引用 branch。
7. 历史 E3 ownership 工具的 keyHash 已补入 TenantScope，避免 Contract 后同业务 ID 跨租户导致账本键碰撞。

## 2. 数据守恒与可逆演练

### 2.1 变更前

| 项 | 值 |
|---|---:|
| Alembic | `228ti3e6rls` |
| Object Runtime 总行数 | 1,030 |
| 明确归属活跃行 | 993 |
| 未知归属行 | 37 |
| scoped 复合键重复 | 0 |
| validated workspace FK | 9/9 |

### 2.2 备份

| 项 | 值 |
|---|---|
| 文件 | `/private/var/tmp/aos-ti3-e7.2KpfGG/aos-meta-before.dump` |
| 格式 | PostgreSQL custom dump |
| 大小 | 1,799,139 bytes |
| mode | `600` |
| SHA-256 | `dc9d17f18efb789b893b676cde27702ee4e79009e623526b7a1e580cba569d10` |
| 可读性 | PostgreSQL 16 容器 `pg_restore -l` 成功 |

备份位于 Git 外，仅用于本地开发库恢复；不代表客户或生产备份。

### 2.3 往返

| 步骤 | revision | 活跃 | 隔离 | 活跃 NULL | 结论 |
|---|---|---:|---:|---:|---|
| 首次升级 | `228ti3e7contract` | 993 | 37 | 0 | GREEN |
| 降级恢复 | `228ti3e6rls` | 1,030 | 无表 | 37 | GREEN，原样恢复 |
| 再升级 | `228ti3e7contract` | 993 | 37 | 0 | GREEN |

最终 schema lint：invalid PK=0、nullable scope=0、scoped branch FK=true、runtime quarantine access=false、issues=[]。

## 3. 自动化验证

| 验证 | 结果 |
|---|---|
| E7 专项 | 5 passed |
| Tenant Isolation 全量 | 123 passed，8 skipped |
| Branch/Draft/Wiki/Runtime/Retention/Demo 相关 | 37 passed，18 skipped |
| 最终合并执行 | 160 passed，26 skipped，零失败 |
| Python compileall | GREEN |
| diff check | GREEN |

8 个 Tenant Isolation skip 中新增 1 个是 E7 NOT NULL 后历史 NULL 注入用例不再合法，由 E7 隔离区迁移与可逆往返测试替代；其余为既有环境/历史门。相关 18 个 skip 延续临时测试库缺少部分 legacy `meta_aip_kv` 夹具的既有现状，不冒充通过。

## 4. 分支证据

`m1`、`feature/228-m3-w1-contract-types`、`feature/228-m3-w2-registry-contract`、`feature/228-m3-w3-openapi-contract`、`feature/228-m3-w4-operation-map` 本地与远端均同步至：

- HEAD：`fd2a124`
- tree：`09b896a07d8dcead7f9b64fe24f87018063175be`

四个 Worker 工作树 clean。主工作树保留用户 `docs/toutiao-series/` 修改和未跟踪文档，未暂存、未夹带 E7 提交。

## 5. 剩余风险与下一门

1. `connector_runtime.py`、`mssql_connector.py`、`mysql_connector.py`、`pg_connector.py` 仍使用不携带 TenantScope 的 owner writer 与旧 conflict target；E7 后继续失败关闭，尚不可真实接入微商城。
2. TI-1 公共底座仍有 59 条逻辑 quarantine，公共 E4 保持 BLOCKED。
3. `decision_lineage` 历史归属与 Data OS/AIP/Analytics/非数据库资源仍待 TI-4/TI-5。
4. 下一执行域为 TI-4 Data OS 与 Connector：先方案和资源/异步 Envelope 审计，再改通用 Connector scope；不得开始具体微商城 Connector。

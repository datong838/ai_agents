# 228 · TI-3 E7 Object Runtime 复合主键与隔离区 Contract 实施方案

> 版本：v1.0 · 2026-08-04  
> 状态：GREEN / 已完成
> 授权：用户已明确授权连续执行 TI-1 E3 全链路前置工作，直至具备接入微商城条件  
> 前置：TI-3 E6 `8dfa626` GREEN；共享库 Alembic `228ti3e6rls`

## Rules

先方案后代码；E7 只收口 E1～E6 已验证的 Object Runtime 租户身份，不重设计对象、图、Draft、Wiki、分支和 Action Runtime 架构。执行前必须完成数据库全量备份、行数与哈希基线、复合键重复检查、旧外键引用检查和降级阻断检查。37 条未知归属历史记录不得伪造归属或丢弃，必须先原样迁入运行角色不可访问、禁止修改和截断的维护隔离表，再从活跃表移出并收紧 NOT NULL。4 个仍使用 owner 连接且不携带 TenantScope 的 Connector writer 属于 TI-4，本波保持失败关闭，不提前接入具体商城。

## 一、现状与结论

共享库当前共有 1,030 条 Object Runtime 记录，其中 993 条已有明确组织与工作区，37 条为 `org_id/project_id IS NULL` 的历史未知归属：

| 表 | 总数 | 未知归属 | E7 动作 |
|---|---:|---:|---|
| `funnel_status` | 1 | 1 | 原样隔离，活跃表收紧 |
| `graph_edge` | 2 | 2 | 原样隔离，活跃表收紧 |
| `meta_branch` | 3 | 3 | 原样隔离，活跃表收紧 |
| `obj_branch_overlay` | 0 | 0 | 收紧，并改 scoped branch FK |
| `obj_instance` | 31 | 31 | 原样隔离，活跃表收紧 |
| `object_lifecycle` | 2 | 0 | 收紧 |
| `draft_dataset` | 925 | 0 | 收紧 |
| `wiki_page` | 1 | 0 | 收紧 |
| `wiki_page_version` | 65 | 0 | 收紧 |

9 个 workspace FK 均已 Validate，明确归属记录的 workspace orphan 为 0。E6 已使 9 表对 `aos_runtime` 执行 ENABLE+FORCE RLS；E7 负责把数据库身份 Contract 从“旧全局键 + nullable TenantScope”收口为“TenantScope 复合键 + 非空 TenantScope”。

## 二、目标 Contract

### 2.1 复合主键

| 表 | E7 主键 |
|---|---|
| `funnel_status` | `(org_id, project_id, object_type)` |
| `graph_edge` | `(org_id, project_id, src_type, src_id, rel, dst_type, dst_id)` |
| `meta_branch` | `(org_id, project_id, id)` |
| `obj_branch_overlay` | `(org_id, project_id, branch_id, object_type, object_id)` |
| `obj_instance` | `(org_id, project_id, object_type, object_id)` |
| `object_lifecycle` | `(org_id, project_id, object_type, object_id)` |
| `draft_dataset` | `(org_id, project_id, id)` |
| `wiki_page` | `(org_id, project_id, object_type, object_id)` |
| `wiki_page_version` | `(org_id, project_id, id)` |

对外 `objectType/objectId/branchId/draftId` 保持不变；它们是租户 scope 内业务标识，不再承担平台全局唯一性。

### 2.2 分支父子外键

删除 `obj_branch_overlay(branch_id) -> meta_branch(id)` 旧全局外键，新增：

```text
obj_branch_overlay(org_id, project_id, branch_id)
  -> meta_branch(org_id, project_id, id) ON DELETE CASCADE
```

从数据库层阻断 overlay 跨组织或跨工作区挂接同名分支。

### 2.3 维护隔离表

新增 `object_runtime_orphan_quarantine`，保存：

- `quarantine_id`、`source_table`、`source_key`；
- 原始整行 `payload` 与可复核 `payload_hash`；
- `reason_code=UNKNOWN_TENANT_SCOPE`、`source_revision=228ti3e6rls`；
- `quarantined_at`。

隔离表只允许迁移维护角色访问，显式 `REVOKE ALL ... FROM aos_runtime`，并通过 UPDATE/DELETE/TRUNCATE guard 保持追加后不可变。升级必须验证“写入隔离表数 = 从活跃表移出数 = 37”；降级必须先验证旧全局键未被 E7 后的新数据复用，才可按原始 JSONB payload 逐表原样恢复。

## 三、现有代码能力映射

E7 不新增业务 API，只把既有写能力的 conflict target 映射到新 Contract：

| 现有能力 | 代码位置 | E7 映射 |
|---|---|---|
| Draft 审批写 Object/Wiki | `routers/runtime_write.py` | Object/Wiki upsert 改为 scoped 复合键；Wiki Version 保留同 scope |
| 图关系写入 | `routers/ontology.py` | Edge conflict target 加 TenantScope |
| 分支创建、overlay、merge | `routers/ontology.py`、`branch_store.py` | Branch/Overlay/Object conflict target 加 TenantScope |
| Funnel 重跑 | `routers/ontology.py` | Funnel conflict target 加 TenantScope |
| 生命周期归档 | `retention_jobs.py` | Lifecycle conflict target 加 TenantScope |
| 测试组织样例 | `db.py`、`demo/workorder_seed.py`、`demo/order_seed.py` | 仅改 conflict target，不改变样例内容或归属 |
| Connector 导入 | 4 个 Connector writer | 不改；保持 TI-4 阻断，缺 scope/旧键均失败关闭 |

`branch_store`、`retention_jobs` 等迁移后才可能执行的叶子兼容 DDL 同步表达 E7 复合主键；`db.py`/Draft 的历史 bootstrap DDL 继续作为 E1～E7 迁移输入，不能提前改成 E7 结构，否则空库会在 E1 重复加列。最终 Contract 只以 managed migration 与 schema lint 为真源；任何运行时 DDL 都不得执行 ALTER 或绕过迁移链。

## 四、实施拆分

### E7-A 数据库 Contract

1. 只读 precheck：revision、37 条未知归属、复合键重复、父子 FK、运行角色权限。
2. 完整数据库备份并记录 mode、bytes、SHA-256。
3. 新建不可变维护隔离表，原样迁移 37 条未知归属并验证守恒。
4. 9 表 `org_id/project_id SET NOT NULL`。
5. 删除旧主键并建立 9 个 scoped 复合主键。
6. 将 overlay→branch 改为 scoped 复合 FK。
7. 提供有碰撞即停止的可逆 downgrade。

### E7-B 代码 Contract

1. 修改 Object、Wiki、Edge、Branch、Overlay、Funnel、Lifecycle 和 demo seed 的 conflict target。
2. 保持全部查询、更新、删除继续同时约束 `org_id/project_id`。
3. 不给 Connector 写入器补默认组织，不允许借 E7 绕过 TI-4。
4. 更新 schema lint，冻结 9 表 PK、NOT NULL、scoped branch FK、隔离表不可见性。

### E7-C 验证与收口

1. 独立数据库执行 `upgrade → downgrade → upgrade`，验证 37 条原样往返。
2. 共享库执行同等可逆演练，最终保持 E7 revision。
3. 验证两个 TenantScope 可复用相同 Object/Branch/Edge/Funnel/Wiki/Draft/Lifecycle 业务 ID，互相不可见且互不覆盖。
4. 全量 Tenant Isolation 与相关 Runtime/Demo 回归 GREEN。
5. 形成证据文档，更新总方案和 AOS 项目开发上下文，五分支同步。

## 五、退出门

1. 备份证据完整，升级前后总行数守恒：活跃 993 + 隔离 37 = 1,030。
2. 9 表 TenantScope 全部 NOT NULL，主键精确匹配目标 Contract；scoped branch FK 有效。
3. 隔离表 37 行，payload 哈希可复核，UPDATE/DELETE/TRUNCATE 被拒绝，`aos_runtime` 无访问权。
4. 两个组织/工作区可使用相同业务 ID；scope A 的改、删、分支 merge、生命周期和 Wiki 更新不影响 scope B。
5. downgrade 在无新旧键碰撞时原样恢复；出现跨租户同 ID 后明确 BLOCKED，不做破坏性猜测。
6. 4 个 Connector owner writer 仍明确列为 TI-4 阻断；不得宣告已可真实接入微商城。
7. 测试、真实数据库、文档一致性和五分支对齐全部 GREEN 后，TI-3 E1～E7 才可总收口。

## 六、风险与回滚

| 风险 | 等级 | 控制 |
|---|---|---|
| 隔离历史行丢失 | P0 | 完整备份、JSONB 原样副本、行数/哈希守恒、可逆演练 |
| 仅改 PK 导致现有 upsert 失效 | P0 | 同波修改全部非 Connector 活跃写路径并回归 |
| overlay 跨 scope 引用 branch | P0 | scoped 复合 FK + 负向测试 |
| E7 后出现同 ID 多租户导致旧 Contract 无法恢复 | P1 | downgrade collision precheck，冲突时 fail closed，改用备份或显式迁移 |
| Connector 被误认为可用 | P0 | 保持 4 writer 阻断并在证据、状态和 TI-4 计划中持续列明 |

回滚以 Alembic downgrade 为首选，但只在碰撞检查通过时允许；否则停止自动降级，以执行前完整备份恢复。任何回滚均不得把隔离数据伪造到测试组织或栖月汇组织。

## 七、执行结果

- 代码基线：`m1@fd2a124`；最终 Alembic：`228ti3e7contract`。
- 9 表复合主键、scope NOT NULL、scoped branch FK 全部生效；37 条历史未知归属原样隔离，活跃 993 + 隔离 37 = 1,030。
- 共享开发库 `upgrade → downgrade → upgrade` GREEN；降级恢复 1,030/37，再升级回到 993/37/0。
- 隔离 payload hash mismatch=0，两个 guard trigger 生效，`aos_runtime` 无访问权。
- 最终累计 `160 passed, 26 skipped`，零失败；五分支同步至 `fd2a124`，tree `09b896a07d8dcead7f9b64fe24f87018063175be`。
- TI-3 E1～E7 最终 GREEN；下一执行域为 TI-4 Data OS 与 Connector，4 个通用 Connector writer 仍失败关闭，尚未开始具体商城接入。

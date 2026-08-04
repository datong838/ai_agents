# 228 · TI-3 E4 Object Runtime 工作区外键验证实施方案

> 版本：v1.0 · 2026-08-04
> 状态：GREEN（已完成）
> 前置：TI-3 E3 `21f8803` GREEN；993 行完整 scope、37 行逻辑 quarantine

## Rules

E4 只 Validate E1 已建立的 9 个 workspace FK；不回填 NULL scope、不设 NOT NULL、不改 PK、不切读、不启用 RLS。先逐表反连接 precheck；任一非 NULL scope 找不到 `twa_workspace` 父记录即阻断。37 条 NULL scope 按 PostgreSQL FK 语义不参与验证，继续由 E3 quarantine 管理。

## 约束集合

`fk_{table}_workspace_ti3`，table 为：`funnel_status`、`graph_edge`、`meta_branch`、`obj_branch_overlay`、`obj_instance`、`object_lifecycle`、`draft_dataset`、`wiki_page`、`wiki_page_version`。

## 文件范围

| 文件 | 动作 |
|---|---|
| `alembic/versions/228ti3e4_validate_workspace_fks.py` | upgrade 逐项 VALIDATE；downgrade 重建同名 NOT VALID |
| `tests/tenant_isolation/test_ti3_e4_object_runtime_fk_validate.py` | precheck、升降级、零 DML、NULL quarantine 保留 |

## 退出门

1. 九表非 NULL scope 父断链为 0；完整 scope=993、NULL/quarantine=37。
2. `228ti3e1expand → 228ti3e4validate → downgrade → upgrade` GREEN。
3. upgrade 后 9/9 validated；downgrade 后 9/9 同名 FK 为 NOT VALID。
4. 九表逐表行数、scope 分布与业务 hash 不变；Alembic 最终 `228ti3e4validate`。
5. Tenant Isolation/Object Runtime 累计 GREEN，五分支同步；下一门 E5 Read Switch。

## 执行结果

- 代码提交：`ec6fff4`（Validate 迁移与专项测试）、`c268062`（历史 schema gate 对 E4 后继版本兼容）。
- 真实开发库 precheck：9 表共 1,030 行，完整 scope 993、NULL/quarantine 37、非 NULL workspace orphan 0。
- 可逆演练：`228ti3e1expand → 228ti3e4validate → 228ti3e1expand → 228ti3e4validate` GREEN；约束状态依次为 9/9、0/9、9/9 validated。
- 守恒：最终仍为 1,030 行、37 条 NULL quarantine、0 条非 NULL orphan；本波业务 DML=0。
- 回归：Tenant Isolation `111 passed, 7 skipped`，零失败。
- 备份：Git 外 `/private/var/tmp/aos-ti3-e4.FiUMVN/aos-meta-before.dump`，1,791,186 bytes，mode 600，SHA-256 `765ddded81e46f991c73af3bd218aa59a4ca17d79e9d479cc921131d59bd79e4`。
- 最终 Alembic：`228ti3e4validate`；下一门为 TI-3 E5 Read Switch。

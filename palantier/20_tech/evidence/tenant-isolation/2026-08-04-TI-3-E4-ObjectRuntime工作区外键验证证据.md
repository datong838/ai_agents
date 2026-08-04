# TI-3 E4 Object Runtime 工作区外键验证证据

> 日期：2026-08-04  
> 结论：GREEN  
> 代码：`ec6fff4`、`c268062`

## 范围与 Rules

本波只验证 TI-3 E1 已创建的 9 个 `fk_{table}_workspace_ti3`。不回填 NULL scope、不设置 NOT NULL、不改主键、不切读、不启用新 RLS、不修改业务行。37 条未知归属继续保留在逻辑 quarantine。

## 数据与迁移证据

| 检查 | 结果 |
|---|---|
| 迁移前 revision | `228ti3e1expand` |
| 九表行数 | 1,030 |
| 完整 scope / NULL quarantine | 993 / 37 |
| 非 NULL workspace orphan | 0 |
| 首次 upgrade | `228ti3e4validate`，9/9 validated |
| downgrade | `228ti3e1expand`，9/9 同名约束回到 NOT VALID |
| 最终 upgrade | `228ti3e4validate`，9/9 validated |
| 最终数据 | 1,030 行、37 条 NULL quarantine、非 NULL orphan 0 |
| 业务 DML | 0 |

## 备份与恢复边界

- Git 外备份：`/private/var/tmp/aos-ti3-e4.FiUMVN/aos-meta-before.dump`
- 大小：1,791,186 bytes；权限：600。
- SHA-256：`765ddded81e46f991c73af3bd218aa59a4ca17d79e9d479cc921131d59bd79e4`。
- 该备份仅属于本地非生产演练；生产/客户环境仍须独立备份、审批和恢复验证。

## 自动化验证

- `services/aos-api/tests/tenant_isolation`：111 passed、7 skipped、零失败。
- E4 专项覆盖非 NULL orphan precheck、升级/降级/再升级、行数与 quarantine 守恒。
- 历史 TI-1/TI-2/TI-3 E1 schema gate 已显式承认 E4 是兼容后继，但未放宽原阶段约束。

## 分支与下一门

`m1` 与四个历史 M3 worker 分支本地/远端均同步至 `c268062`，tree `a11462c0f7582e3853a831bfd70ba3e285039db8`。主工作树的用户头条/掘金文档未暂存、未夹带。

下一门为 TI-3 E5 Read Switch；E4 GREEN 不代表 RLS、复合键 Contract 或具体电商平台连接已完成。

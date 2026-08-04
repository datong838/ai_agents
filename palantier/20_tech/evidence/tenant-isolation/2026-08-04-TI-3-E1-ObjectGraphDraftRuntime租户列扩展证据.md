# TI-3 E1 Object/Graph/Draft Runtime 租户列扩展证据

## 结论

TI-3 E1 GREEN。代码 `7f7d48a`，共享库最终 revision `228ti3e1expand`，五分支同 HEAD。E1 仅完成 nullable Expand 与 NOT VALID 关系，未回填、未切读、未启用新 RLS。

## 基线与备份

- 9 表行数：Draft 925、Funnel 1、Graph 2、Branch 3、Overlay 0、Object 31、Lifecycle 2、Wiki 1、Wiki Version 65，总计 1,030。
- 备份：`/private/var/tmp/aos-ti3-e1.DtUvou/aos-meta-before.dump`，1,652,153 bytes，mode 600，SHA-256 `441e714a8d39fda97059af51ebb21712e156aab7d228e8acd723d1f20d1f3cc9`。

## 迁移证据

- 5 张原 NO_TENANT 表新增 `org_id/project_id` 共 10 列，全部 nullable。
- 9 张租户资源建立工作区 FK，9/9 `convalidated=false`。
- `meta_action_type/meta_link_type/meta_object_type` 保持平台模板，无 tenant scope 列。
- downgrade 后 TI-3 FK=0、扩展列=0；再 upgrade 后 FK=9、validated=0、扩展列=10；行数仍为 1,030。
- 干净测试库暴露 `draft_dataset` 过去依赖 Router 运行时建表，测试初始化已在 TI 迁移前显式创建既有 Draft 表，未修改业务 Schema。

## 验证

- TI-3 E1/Registry/TI-2 前序门：13 passed，2 historical skips。
- Tenant Isolation：100 passed，7 skipped。
- Object/Graph/Draft/Wiki 扩大回归：705 passed，45 skipped；2 个 `test_field_marking_fga` 失败为既有 seed 漂移，单文件重跑仍失败，与 E1 DDL 无关。
- Compile、Ruff F/I、diff check：GREEN。

## 分支

`m1` 与 w1～w4 本地/远端均同步至 `7f7d48a`。

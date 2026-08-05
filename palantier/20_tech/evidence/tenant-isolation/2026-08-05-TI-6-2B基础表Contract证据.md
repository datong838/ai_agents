# TI-6-2B 基础表 Contract 证据

## 结论

TI-6-2B GREEN。代码 `e1e3d7b`，共享开发库 revision `228ti6bcontract`。

## Contract

- `theme`、`widget_catalog`：`(org_id, project_id, id)` 主键，已验证 `meta_workspace` FK，ENABLE/FORCE RLS。
- `twa_audit`、`twa_join_request`：`(org_id, project_id, id)` 主键，已验证 `twa_workspace` FK。
- `twa_invite`：`(org_id, project_id, token)` 主键，已验证 `twa_workspace` FK。
- TWA 的历史 token/id 唯一约束保留兼容；Theme/Widget 同逻辑 ID 可跨组织分别存在且互不可见。

## 可逆与守恒

- 临时数据库真实 downgrade 到 `228ti5b1models`、upgrade 到 head，5 表 count/hash 不变。
- 共享库升级前创建 `/tmp/aos-ti6-2b-before.dump`，仅升级不降级。
- 共享升级前后：Theme 3、Widget 17、三张 TWA 表均 0，逐行 hash 完全一致。
- 实库 audit 101/101、drift=0；状态 80 STRONG / 3 WEAK / 18 NO_TENANT。

## 验证与保留门

- TI-6-2B/相关专项：16 passed。
- Tenant Isolation：224 passed，8 skipped。
- 全量：9,217 collected。
- 五分支同步 `e1e3d7b`。

`authz_tuple` 的 8 条空 scope、`meta_membership` 53 条投影断链、3 个未知对象和外部后端未配置继续显式阻断；本波未修改这些历史数据。

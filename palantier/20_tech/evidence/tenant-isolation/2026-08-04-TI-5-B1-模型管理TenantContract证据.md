# TI-5 B1 模型管理 Tenant Contract 证据

> 日期：2026-08-04
> 代码：`044f5a5`，tree `3adfc7f7812005b657c103ccc649f8ae7670512e`
> Alembic：`228ti5b1models`

## 1. 结果

- `capacity_limits=4`、`capacity_usage=30`、`model_catalog=12`、`model_provider=4`、`model_route=5`、`provider_health=4`、`registered_models=6`，共 65 行，全部位于测试组织。
- 七表主键均为 `(org_id,project_id,id)`，workspace FK validated，ENABLE/FORCE RLS 与双 GUC policy 完整。
- `provider_health` 只能引用同 scope Provider；`registered_models` 只能引用同 scope Catalog Model。
- Router 从认证 Principal 取得 scope，Store 不再写死测试组织；无 runtime scope 时不能借业务 query/body 越权。

## 2. 可逆性与守恒

备份 `/private/var/tmp/aos-ti5-b1.0If0El/aos-meta-before.dump`，1,944,971 bytes，mode `0600`，SHA-256 `ebdcbe71e0b020465873a7f29fff96e031310e336ee449f22ed53479aa31b3f4`。

共享库从 B1 降到 A3，再升级到 B1；七表 count/hash 逐表完全一致：

| 表 | 行数 | hash |
|---|---:|---|
| capacity_limits | 4 | `44b9c2aa0e2ee87d176c131410478fe1` |
| capacity_usage | 30 | `70a6d2f9febe1e0b2d6b30d762bd7749` |
| model_catalog | 12 | `f4ca5b1e7978042813e04fa80df4b500` |
| model_provider | 4 | `3f3e11aaa75843ef87542ac7cc8e6e39` |
| model_route | 5 | `6913c98182b94edf04c37313dd82c18f` |
| provider_health | 4 | `c52ee684e034dce79cdacdb66a789e7f` |
| registered_models | 6 | `db433aed668ad965fbcde3ea930a2554` |

## 3. 验证

- 模型管理 API：33 passed。
- B1 Contract：4 passed。
- Tenant Isolation：199 passed / 7 skipped。
- Python compile、目标文件 lint、diff check：GREEN。
- 全量收集：9,191 tests，无 collection error。
- 五分支及五远端同为 `044f5a5` / tree `3adfc7f...`；四 Worker clean，主工作树只保留用户头条文档改动。

## 4. 风险边界

- 本波未连接真实模型供应商、未写客户凭据、未连接商城。
- 磁盘 LLM Provider manifest 与 scoped 安装/配置实例的模板分离由 B2 继续验证。
- `aip_model_catalog` 进程内 Singleton 尚未隔离，归 TI-5 C，不影响 B1 PostgreSQL Contract，但阻止 TI-5 总 GREEN。

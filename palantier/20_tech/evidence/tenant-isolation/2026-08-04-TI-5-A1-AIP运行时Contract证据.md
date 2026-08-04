# TI-5 A1 AIP 运行时 Contract 证据

> 日期：2026-08-04
> 结论：GREEN
> 代码：`d381578`，tree `bee586f2546f0ae904d2f5c0a3deb9ecc37d888b`

## 1. 实施结果

- 7 张 AIP 运行表均具备 validated workspace FK、ENABLE/FORCE RLS 与 public 双 GUC policy。
- Graph、Run、Eval、Publication 四类 Store 的生产连接使用 `db_connect(TenantScope)`；测试注入连接接口保持兼容。
- 既有 scoped 主键、父子 FK、不可变 Revision/Publication Contract 不重设计、不改 API 业务 ID。
- 无 scope 的 `aos_runtime` 可见 0；同 graph ID 在两个工作区可共存、互不可见、删除互不影响。

## 2. 数据库与可逆性

- 前置 Git 外备份复用 TI-4 A1 收口备份：`/private/var/tmp/aos-ti4-a1.Tp6Zb6/aos-meta-before.dump`，SHA-256 `883e668cbde3b2d0fa255fd51a6e598a8b6c243d6d4c31cdacb8d3d4f22ea7bd`。
- 共享库执行 `228ti4a1apollo → 228ti5a1aip → 228ti4a1apollo → 228ti5a1aip`。
- 最终行数守恒：Graph 4、Revision 7、Run 3、RunNode 9、Suite 1、Report 2、Publication 1，共 27 行。
- 降级后 7 个 policy 与 7 个 TI-5 FK 均撤销；再升级后 schema report `ok=true`、workspace orphan=0。

## 3. 验证

- AIP 新旧 Store/API 专项：83 passed。
- Tenant Isolation：181 passed / 11 skipped。
- Ruff 目标规则、diff check、TI-5 A1 schema report：GREEN。
- 五分支与五远端均为 `d381578`，tree 一致；用户 `docs/toutiao-series/*` 未夹带。

## 4. 边界

本波不处理 `meta_aip_kv`、`decision_lineage`、Analytics/模型目录或非 PostgreSQL 资源；不连接真实商城或真实模型供应商。下一门为 TI-5 A2。

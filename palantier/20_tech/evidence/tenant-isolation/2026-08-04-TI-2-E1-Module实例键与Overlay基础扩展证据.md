# TI-2 E1 Module 实例键与 Overlay 基础扩展证据

> 日期：2026-08-04  
> 代码基线：`m1@e95ae45`  
> Alembic：`228ti2e1expand`  
> 结论：**GREEN（Expand only）**

## 1. 交付

- `meta_module` 新增 nullable `module_pk/module_id/template_id/template_version/installation_id/active_overlay_revision/effective_config_hash/deleted_at`。
- 7 张 Module 子资源新增 nullable `module_pk`，建立到 Module 候选复合键的 NOT VALID FK。
- 新增空表 `module_organization_profile/module_instance_overlay/module_user_view_preference`，revision history 由 UPDATE/DELETE/TRUNCATE trigger 保护。
- Module 可映射现有 Bundle/Installation/Overlay revision，不新增第二套资产模板架构。
- 注册表更新为 95 张 PostgreSQL 表、102 个全资源，TI-2 执行组仍是唯一分组真源。
- pytest 临时数据库补齐当前运行期 Module legacy schema 后再执行 E1～E3/TI-2 migration，继续保持共享开发库零测试污染。

## 2. 真实库验证

| 验证 | 结果 |
|---|---|
| 备份 | PostgreSQL custom dump，882,671 bytes，mode 600 |
| 备份 SHA-256 | `41fd787c6690ea11f43ecbbf2981d66db9a20737171742afce4aabd82db05957` |
| 升降级 | `228ti1e3exec → 228ti2e1expand → 228ti1e3exec → 228ti2e1expand` GREEN |
| schema lint | revision `228ti2e1expand`，`issues=[]`，`ok=true` |
| 既有行守恒 | 10 张 Module 表逐表 before/after 完全一致，总计 644 行 |
| 新表 | Profile/Overlay/Preference 均 0 行 |
| 栖月汇 | 10 张 Module 资源合计 0 行 |
| RLS | E1 未提前开启，仍留到 E6 |

## 3. 自动化验证

- `services/aos-api/tests/tenant_isolation`：`74 passed`，7 个既有 warning。
- Module/Workshop/Widget/Canvas 相关累计：`492 passed`，7 个既有 warning。
- migration 静态门确认没有历史 `INSERT/UPDATE/DELETE`、没有 `VALIDATE CONSTRAINT`、没有 E1 destructive contract。
- `git diff --check` GREEN。

## 4. 边界与风险

- 现有 644 行没有生成 `module_pk`、没有绑定模板或 Installation；E1 只准备结构。
- 旧全局 PK 与数据库默认 `dev-org/dev-project` 仍存在；运行时子 Store 仍有默认租户常量，因此不能宣称 Module 已隔离。
- 当前 clean database 的 Alembic baseline 不创建全部 legacy Module 表；真实部署长期应把这些运行期 DDL 收归 migration。本波临时数据库按现有部署顺序显式初始化 legacy schema 后升级，不掩盖该债务。
- 59 条 TI-1 QUARANTINE 与 E4 BLOCKED 不变；本波没有清理或认领历史数据。

## 5. 下一门

TI-2 E2：将 Canvas/Widget/Variable/Query/Event/Interface/Deployment Store 改为显式 TenantScope，Router 从 Principal 注入 scope；get/update/delete 全部 scope 过滤并对跨租户统一 404。完成前不安装或连接真实微商城。

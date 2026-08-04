# 228 · TI-2 E1 Module 实例键与 Overlay 基础扩展实施方案

> 版本：v1.0 · 2026-08-04  
> 状态：GREEN（Expand only，代码 `e95ae45`）  
> 上位方案：`228-组织与工作区租户隔离全量补强实施方案.md`  
> 前置基线：`m1@0ae62bc`；TI-1 E3 非生产可逆性 GREEN；TI-PRE-1 GREEN

## 0. 使用的 Rules

1. 先方案、后编码；本文件冻结 E1 文件范围和退出门。
2. 不重设计 M2-B/M3 资产安装架构；平台模板继续由 Bundle/Registry 表达，Module 只增加租户实例绑定。
3. E1 只做可逆 Expand：新增 nullable 列、唯一候选键、NOT VALID FK 和空表；不回填、不切换 Store、不删除默认值或旧主键。
4. 保护栖月汇空态；任何历史 Module 归属仍按 E3 证据处理，不默认认领给客户组织。
5. 未知归属不猜测；没有 `module_pk` 的旧行在 E1 后继续按旧路径运行。
6. 开发完成后执行迁移升降级、schema lint、行数守恒和租户专项回归；证据与 AOS 开发上下文同步。

## 1. 现状结论

真实开发库的 TI-2 Module 资源共 644 行，栖月汇对应行均为 0：

| 资源 | 行数 |
|---|---:|
| `meta_module` | 160 |
| `module_canvas_config` | 9 |
| `module_deployment` | 29 |
| `module_events` | 262 |
| `module_interface` | 9 |
| `module_query` | 22 |
| `module_variable` | 25 |
| `module_widget_instance` | 108 |
| `theme` | 3 |
| `widget_catalog` | 17 |

这 10 张表已有 `org_id/project_id`，但主键仍是全局 `id` 或 `module_id`，没有 Module 复合外键；除 `module_store` 主链外，Canvas、Widget、Variable、Query、Event、Interface、Deployment 的业务方法仍使用 `_DEFAULT_ORG/_DEFAULT_PROJECT`，且 get/update/delete 多数只按全局 ID 定位。Router 只挂了鉴权依赖，没有把 Principal 传入 Store。因此当前只能证明“入口需登录”，不能证明同 ID 双租户、跨租户 404 或删除隔离。

当前 synthetic `instance-overlay-v1alpha1` 只是 M5 文件契约；生产数据库没有 `module_instance_overlay`、active revision 或 Effective Config hash。该能力必须映射现有 `bundle_installation.overlayRevision` 与 Module 实例，不另造平台分支。

## 2. TI-2 分门

| 门 | 内容 | 本次是否执行 |
|---|---|---|
| E1 Expand | `module_pk`、模板/Installation 绑定、active overlay、子资源 module_pk、候选唯一键/NOT VALID FK、空 Overlay/Profile/Preference 表 | 是 |
| E2 Dual Write | Router 注入 Principal/TenantScope；Store 新写同时写 module_pk 和 scope；默认常量仅留显式种子 | 后续 |
| E3 Backfill | 只对证据确定的测试组织 Module 建 module_pk/绑定；未知进入 quarantine | 后续，单独批次 |
| E4 Validate | 校验 Module/子资源复合 FK 和守恒 | 后续 |
| E5 Read Switch | 所有 get/update/delete 按 scope + module_id/module_pk；跨租户统一 404 | 后续 |
| E6 RLS | Module 实例、Overlay、Profile/Preference、子资源启用并 FORCE RLS | 后续 |
| E7 Contract | 切复合主键、删除数据库默认租户、冻结 API/SDK 和 APP-01～APP-15 | 后续 |

## 3. E1 数据模型

### 3.1 `meta_module` nullable 扩展

- `module_pk UUID NULL`
- `module_id TEXT NULL`：E1 兼容复制目标，旧 `id` 暂不改名、不回填
- `template_id TEXT NULL`
- `template_version TEXT NULL`
- `installation_id UUID NULL`
- `active_overlay_revision BIGINT NULL`
- `effective_config_hash TEXT NULL`
- `deleted_at TIMESTAMPTZ NULL`

增加候选唯一约束 `(org_id, project_id, module_pk)` 与 `(org_id, project_id, module_id)`；NULL 行不冲突。旧 `PRIMARY KEY(id)` 保留到 E7。

### 3.2 子资源扩展

`module_canvas_config/module_deployment/module_events/module_interface/module_query/module_variable/module_widget_instance` 新增 `module_pk UUID NULL`，并增加 `(org_id, project_id, module_pk) -> meta_module` 的 NOT VALID FK。E1 不把旧 `module_id` 猜测映射到 module_pk。

### 3.3 新空表

- `module_organization_profile`：组织品牌、术语和默认策略 revision；只含 `org_id`，不得放工作区业务事实。
- `module_instance_overlay`：`org_id/project_id/module_pk/overlay_revision` 复合主键，保存 base template 坐标、差异 patch、canonical hash 和 actor。
- `module_user_view_preference`：`org_id/project_id/module_pk/subject/preference_key/revision`，只允许体验偏好。

三表在 E1 创建为空；Overlay/Profile revision 采用 append-only trigger，禁止 UPDATE/DELETE/TRUNCATE。`meta_module.active_overlay_revision` 的 FK 在 module_pk 回填前保持 NOT VALID。

## 4. 文件范围

| 文件 | 动作 |
|---|---|
| `alembic/versions/228ti2e1_module_instance_expand.py` | 唯一 E1 migration，纯 DDL、可 downgrade |
| `aos_api/tenant_resources.yaml` | 注册 3 张新表；TI-2 执行组保持唯一真源 |
| `aos_api/tenant_schema_lint.py` | 新增 TI-2 E1 schema report；TI-1 lint 接受后继 revision |
| `tests/tenant_isolation/test_ti2_e1_migration.py` | revision/down_revision、列、约束、空表、无 DML 静态门 |
| `tests/tenant_isolation/test_ti2_e1_schema_lint.py` | 缺列、FK 提前验证、append-only trigger 等负向测试 |

E1 明确不修改 Router、Store、前端页面、现有 644 行或栖月汇数据。

## 5. 验收与回滚

1. Alembic `228ti1e3exec → 228ti2e1expand → downgrade → upgrade` GREEN，single head/current。
2. 10 张既有 Module 表行数逐表不变；栖月汇 Module 资源仍为 0。
3. 所有新增列 nullable；旧 PK、默认值和读写路径不变。
4. 新三表为 0 行；append-only trigger 齐全。
5. Module 子资源 FK 全部 `NOT VALID`；E1 禁止 `VALIDATE CONSTRAINT`、UPDATE、DELETE、INSERT 历史数据。
6. `tests/tenant_isolation` 与 Module 相关既有测试 GREEN。
7. downgrade 只在新表为空、新列未被 E2/E3 使用时允许；一旦产生 Profile/Overlay/Preference，必须归档后走受控 contract，不得直接丢表。

## 6. E1 后下一波

进入 TI-2 E2：先改 Module Store 方法签名为显式 `TenantScope`，再改 Router 从 Principal 构造 scope；按 Canvas/Widget/Variable/Query/Event/Interface/Deployment 逐族切换。E2 仍不安装微商城、不调用任何平台 API。

## 7. 完成记录

- 真实库升降级往返 GREEN，最终 single head/current=`228ti2e1expand`。
- 10 张既有 Module 表总计 644 行逐表守恒；三张新表与栖月汇 Module 数据均为 0。
- schema lint GREEN；租户专项 74 passed；Module/Workshop 累计 492 passed。
- 详细证据：`evidence/tenant-isolation/2026-08-04-TI-2-E1-Module实例键与Overlay基础扩展证据.md`。

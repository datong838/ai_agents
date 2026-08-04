# 228 · TI-2 E7 Module 复合主键与卸载 Contract 实施方案

> 版本：v1.0 · 2026-08-04
> 状态：GREEN / 已完成
> 前置：TI-2 E6 `846b49a` GREEN；共享库 Alembic `228ti2e6rls`

## Rules

先方案后代码；E7 只收口 E1～E6 已验证的 Module 实例身份，不重设计 API/资产安装架构。执行前必须完整备份并做重复/空值/FK/隔离区 precheck。对外继续使用 `moduleId`，内部 Contract 使用 TenantScope + module_pk。两条孤儿 Event 不删除证据、不伪造父记录，先可逆迁入专用隔离表再收紧 NOT NULL。

## 目标

1. `meta_module` 正式主键切为 `(org_id, project_id, module_pk)`，`module_pk/module_id` NOT NULL；保留 scoped module_id unique。
2. 7 张直属子表 `module_pk` NOT NULL，并把遗留全局 PK 改成租户复合 PK：
   - Canvas/Interface：`(org_id, project_id, module_pk)`；
   - Deployment/Event/Query/Variable/Widget Instance：`(org_id, project_id, id)`。
3. seed、Canvas upsert、Interface upsert 的 conflict target 改为复合 Contract，使两个组织可复用同一 `moduleId` 和相同子资源 ID。
4. 两条 orphan Event 原样迁入 `module_event_orphan_quarantine`，该表只归维护角色、运行角色无权限；downgrade 可原样放回。
5. 增加工作区内软卸载：停止 Event、设置 Module `status=uninstalled/deleted_at`，不删除 Order 等独立业务对象；list/get/子资源运行路径不再显示已卸载实例。
6. 新增 `DELETE /v1/modules/{module_id}`，要求 admin/owner 与 `If-Match`；GET 返回当前 ETag。重复卸载返回 not found/幂等不可见，不影响其他组织。

## 非目标

- 不物理删除业务对象、订单、客户、达人、控价记录或资产安装证据。
- 不删除外部兼容字段 `id/module_id`；它们继续服务 URL、响应和审计，不再承担全局唯一性。
- 不在 E7 实现具体微信小店/抖音 Connector。
- Theme/Widget Catalog 的平台模板 Contract 另由模板资产边界管理，不混入 Module 实例 PK。

## 文件范围

| 文件 | 变更 |
|---|---|
| `alembic/versions/228ti2e7_module_contract.py` | orphan 可逆隔离、NOT NULL、8 表复合 PK、downgrade 重复阻断 |
| `aos_api/module_identity.py` | 默认只解析未卸载实例 |
| `aos_api/module_store.py` | 复合 upsert、ETag、scope 内软卸载、list/get 隐藏卸载 |
| `aos_api/canvas_config.py`、`module_interfaces.py` | 复合 conflict target |
| `aos_api/routers/modules.py` | GET ETag 与 DELETE If-Match/admin 门 |
| `aos_api/tenant_schema_lint.py` | E7 NOT NULL/PK/quarantine/Revision 报告 |
| `tests/tenant_isolation/test_ti2_e7_module_contract.py` | APP-04/05、迁移、隔离区、API/负向门 |

## Orphan 隔离规则

升级先把 `module_events.module_pk IS NULL` 行完整复制到隔离表，记录原始字段、`MISSING_PARENT_MODULE`、时间和来源 revision，再从活跃表删除。隔离表撤销 runtime grant，不参与业务读取。只有复制行数=删除行数且活跃 NULL=0 才继续 NOT NULL。downgrade 先确认原 ID 未被复用，再把隔离行原样插回并删除隔离表。

## 回滚

降级前检查所有 8 表是否出现跨 scope 重复遗留 ID；一旦 E7 后已真实使用同 ID 多租户能力，自动 downgrade 必须 BLOCKED，改用完整备份恢复或先迁移冲突。无重复时恢复旧全局 PK、放宽 module_pk/module_id、把 orphan Event 原样放回；E6 RLS 保持。软卸载数据的回滚不由 schema downgrade猜测，按审计/专用恢复动作处理。

## 退出门

1. precheck：父/子 NULL 除两条 orphan 外为 0；新复合键重复 0；FK mismatch 0；栖月汇 Module 0。
2. 共享库 upgrade/downgrade/upgrade 与备份恢复演练 GREEN；最终 revision `228ti2e7contract`。
3. 8 张活跃表 module_pk NOT NULL、复合 PK 正确；隔离表 2 行且 runtime 无权限。
4. APP-04：两个 scope 创建相同 moduleId、相同 Canvas/Interface 和子 ID，读写互不影响。
5. APP-05：scope A 卸载后 A 不可见/事件停止，scope B 同名实例保持可用，独立业务对象计数不变。
6. Router/OpenAPI、Tenant Isolation、Workshop 累计 GREEN；五分支同步后 TI-2 才可最终 GREEN。

## 执行结果

- 代码基线：`m1@4004170`；最终 Alembic：`228ti2e7contract`。
- 共享库 8 张活跃表复合主键与 `module_pk` 非空 Contract 生效；2 条孤儿 Event 进入维护隔离表，runtime 无访问权。
- APP-04 已证明两个 scope 可创建相同 Module/Canvas/Interface/子资源 ID；APP-05 已证明带 ETag 的软卸载只影响当前 scope，独立业务对象计数不变。
- 真实 `upgrade → downgrade → upgrade` GREEN：降级恢复 2 条 orphan、旧主键与 nullable；再升级重新隔离且活跃 NULL=0。
- Tenant Isolation + Workshop 累计 `272 passed, 3 skipped`；3 个 skip 是 E7 已由 NOT NULL 拒绝的 E3/E5 历史非法注入测试，替代门由 E7 quarantine/contract 测试覆盖。
- `m1` 与 w1～w4 已同步至 `4004170`。TI-2 E1～E7 最终 GREEN，下一执行域为 TI-3 Object/Graph/Draft/Action Runtime，仍不接具体商城。

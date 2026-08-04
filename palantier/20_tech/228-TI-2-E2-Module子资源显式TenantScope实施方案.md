# 228 · TI-2 E2 Module 子资源显式 TenantScope 实施方案

> 版本：v1.0 · 2026-08-04  
> 状态：执行中（E2-A GREEN，代码 `b7cfb34`）  
> 前置：TI-2 E1 `e95ae45` GREEN

## Rules

先方案后代码；复用 `Principal.org_id/project_id → TenantScope`；不改变 M2-B/Installation 架构；Store 禁止从 body 接收租户；所有 get/update/delete 同时按 scope、module_id 和资源 ID 定位；跨租户统一 404；E2 不回填 module_pk、不启用 RLS、不接微商城。

## 现状与目标

`module_store` 主链已经接收 org/project，但 Canvas、Widget、Variable、Query、Event、Interface、Deployment 仍使用 `_DEFAULT_ORG/_DEFAULT_PROJECT` 或只按全局 ID 修改。E2 将 Router 的 Principal 显式传入 Store，并用 `TenantScope` 完成 SQL 过滤和 transaction-local GUC。

## 分片

| 分片 | Store/Router | 退出门 |
|---|---|---|
| E2-A | Canvas、Widget、Variable | 同 ID 双租户、跨租户 get/update/delete 404、测试组织不变 |
| E2-B | Query、Event、Interface | 相同安全矩阵 |
| E2-C | Deployment、Theme、Widget Catalog 与 usage 链 | 部署/回滚、目录读取和引用扫描不跨租户 |
| E2-D | Module aggregate、静态默认常量门、APP-01～APP-05 基础 | 业务方法默认常量 0 命中，累计回归 GREEN |

E2-A 完成记录：Canvas/Widget/Variable 和 Query list 已显式接收 TenantScope；53 项分片累计与 77 项租户累计 GREEN。详细证据见 `evidence/tenant-isolation/2026-08-04-TI-2-E2A-CanvasWidgetVariable显式TenantScope证据.md`。

## 固定方法规则

1. 所有业务方法第一个关键词参数为 `scope: TenantScope`，数据库连接使用 `connect(scope)`。
2. 资源 ID 查询必须附加 `org_id=%s AND project_id=%s`；嵌套路由还必须验证 `module_id`。
3. 创建的 org/project 只能取 `scope.key`；更新不得修改租户列。
4. Router 必须显式 `principal: Principal = Depends(require_principal)`；仅 Router 级 dependencies 不足以向 Store 传租户。
5. 测试种子可以显式构造测试组织 scope，但 Store 内不得保留隐式 fallback。

## 验证

每片先跑专项负向测试，再跑 Module/Workshop 累计和 `tests/tenant_isolation`。共享库测试快照必须不变。E2 全部完成后才允许 E3 对既有 Module 生成 module_pk。

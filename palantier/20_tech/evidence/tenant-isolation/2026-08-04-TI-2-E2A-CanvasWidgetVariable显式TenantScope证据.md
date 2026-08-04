# TI-2 E2-A Canvas / Widget / Variable 显式 TenantScope 证据

> 代码：`m1@b7cfb34`  
> 结论：GREEN（E2-A 分片）

## 交付

- Canvas、Widget、Variable Store 业务方法改为显式 `TenantScope`，连接设置 transaction-local GUC。
- Router 从已认证 Principal 构造 scope，不从 body 接收 org/project。
- Widget/Variable 的 get/update/delete 同时按 `org_id + project_id + module_id + resource_id` 定位，跨租户和错 Module 均返回未找到。
- Canvas 在旧全局 `module_id` 主键尚未 Contract 前，对另一租户同 ID 写入失败关闭，不覆盖原租户配置。
- Variable usage 的 Widget 与 Query 扫描均使用当前 scope；Query list 入口同步显式 scope。

## 验证

- 新增三组真实 PostgreSQL 负向测试：Canvas 同 legacy ID 覆盖阻断、Widget 跨租户/错 Module、Variable 跨租户/错 Module。
- E2-A + Workshop + 鉴权门：`53 passed`。
- 租户隔离累计：`77 passed`。
- 7 个 warning 均为既有 Pydantic/Starlette warning。

## 未完成

Query 写路径、Event、Interface、Deployment、Theme 与 Widget Catalog 仍待 E2-B/E2-C；旧数据库全局 PK 与默认租户仍待 E7。当前不得宣称 TI-2 全部 GREEN。

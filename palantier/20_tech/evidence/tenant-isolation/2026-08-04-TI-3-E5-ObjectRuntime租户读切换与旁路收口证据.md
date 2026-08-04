# TI-3 E5 Object Runtime 租户读切换与旁路收口证据

> 日期：2026-08-04  
> 结论：GREEN  
> 代码：`3d53105`

## 关键结论

- Object Runtime 全包 SELECT 无 org/project 命中为 0。
- vector autoSample 从 Principal 接收 TenantScope；双租户动态夹具只取得当前 scope，缺 scope 失败关闭。
- demo story、Order/WorkOrder seed 与 clear 均固定双租户边界；清理不再删除共享 Object/Link 模板，也不无 scope 删除 `decision_lineage`。
- 系统启动不再创建无 scope `main/sandbox` Branch；既有 37 条 quarantine 保持原样。
- 无 scope Object writer 只剩 4 个 TI-4 文件：`connector_runtime.py`、`mssql_connector.py`、`mysql_connector.py`、`pg_connector.py`。该清单被静态测试冻结，真实平台连接继续暂停。

## 验证

| 门禁 | 结果 |
|---|---|
| E5 专项 | 3 passed |
| Tenant Isolation + vector/demo 相关 | 115 passed、18 skipped、零失败 |
| 关键 lint/compile | GREEN |
| 共享库 | `228ti3e4validate`；1,030 行、37 quarantine、0 非 NULL orphan |
| 测试组织 autoSample | 0；未读取 NULL quarantine |
| 业务/历史 DML | 0 |

8 个既有 demo/vector HTTP 用例因一次性测试库缺 `meta_aip_kv` 而明确 skip；新的动态隔离测试不依赖该缺口并已通过。此项记录为测试基础设施债务，不冒充已执行用例。

## 分支与下一门

五个代码分支与五远端同步至 `3d53105`，tree `7e271e8be2ade100b5e8859359e3f2261504b342`。用户头条/掘金文档未暂存、未夹带。

下一门为 TI-3 E6 RLS；E5 不改变主键、NOT NULL、OpenAPI 或历史 quarantine，也不授权真实微商城连接。

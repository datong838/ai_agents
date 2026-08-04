# TI-3 E2-A Object/Graph/Branch 显式 TenantScope 证据

## 结论

E2-A GREEN，功能提交 `f5f0b7c`，格式收口后五分支最终 `5cdafea`。本波仅收新写和 mutation，不回填历史行、不改主键、不切 RLS。

## 实现

- Graph Edge 与 Funnel Status insert/upsert 写入 Principal org/project；全局旧键跨 scope 冲突返回 `TENANT_KEY_CONFLICT` 409。
- Branch 创建写入 scope；自定义 base 只能引用同 scope branch。
- Overlay upsert、checkout、merge、对象 delete/upsert、overlay 清理均透传同一 TenantScope 并约束 scope。
- 既有全局 PK 暂不允许同 ID 双租户共存；E7 Contract 前保持失败关闭。

## 验证

- 专项：2 passed，覆盖 Graph/Funnel 冲突失败关闭和 Branch/Overlay scope 继承。
- Branch/Ontology/Funnel/Tenant Isolation 累计：185 passed，15 skipped，7 warnings。
- Compile、Ruff F/I、diff check：GREEN。

## 下一门

E2-B 收 Draft/Wiki/Lifecycle；历史 NULL scope 继续不动，具体商城 Connector 继续暂停。

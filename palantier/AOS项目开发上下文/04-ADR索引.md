# ADR 索引

以下决策均来自已冻结并完成回归的 M1/M2 设计。M3 只消费这些决策，不重新讨论其基础架构。

| ADR | 状态 | 决策 |
|---|---|---|
| [ADR-001](ADR/ADR-001-PostgreSQL与不可变记录为唯一真源.md) | Accepted | PostgreSQL 与不可变记录是安装事实唯一真源 |
| [ADR-002](ADR/ADR-002-Receipt-First幂等与强ETag-CAS.md) | Accepted | 写操作使用 receipt-first 幂等和强 ETag/CAS |
| [ADR-003](ADR/ADR-003-权限与职责分离失败关闭.md) | Accepted | tenant/role/marking/maker-checker 由服务端失败关闭 |
| [ADR-004](ADR/ADR-004-M3只做现有控制面的UI与SDK适配.md) | Accepted | M3 不重画架构，只做现有 API 的 UI/SDK 适配 |

新增或反转决策必须：先更新上位方案，新增 ADR 记录上下文、取舍和迁移影响，再编码与回归；不得静默覆盖历史 ADR。

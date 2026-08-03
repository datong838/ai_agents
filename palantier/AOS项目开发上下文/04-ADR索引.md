# ADR 索引

以下决策来自已冻结并完成回归的 M1～M4 设计及 M5 组合验证边界。M5 不重新讨论或替换基础架构。

| ADR | 状态 | 决策 |
|---|---|---|
| [ADR-001](ADR/ADR-001-PostgreSQL与不可变记录为唯一真源.md) | Accepted | PostgreSQL 与不可变记录是安装事实唯一真源 |
| [ADR-002](ADR/ADR-002-Receipt-First幂等与强ETag-CAS.md) | Accepted | 写操作使用 receipt-first 幂等和强 ETag/CAS |
| [ADR-003](ADR/ADR-003-权限与职责分离失败关闭.md) | Accepted | tenant/role/marking/maker-checker 由服务端失败关闭 |
| [ADR-004](ADR/ADR-004-M3只做现有控制面的UI与SDK适配.md) | Accepted | M3 不重画架构，只做现有 API 的 UI/SDK 适配 |
| [ADR-005](ADR/ADR-005-M4证据不可变与服务端阶段投影.md) | Accepted | M4 Evidence 不可变，阶段与统计只由服务端连续证据门投影 |
| [ADR-006](ADR/ADR-006-M5无业务骨架与Overlay文件契约边界.md) | Accepted | M5 电商包只做 test-only 无业务组合验证，Overlay 只以文件契约和 opaque hash 接入现有安装控制面 |

新增或反转决策必须：先更新上位方案，新增 ADR 记录上下文、取舍和迁移影响，再编码与回归；不得静默覆盖历史 ADR。

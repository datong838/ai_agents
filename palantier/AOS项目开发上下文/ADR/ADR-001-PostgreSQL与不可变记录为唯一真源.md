# ADR-001：PostgreSQL 与不可变记录为唯一真源

- 状态：Accepted
- 日期：2026-08-03

## 决策

Registry、Composition lock、Installation revision/decision/event、receipt 和 active pointer 以 PostgreSQL 持久化状态为唯一真源。lock、revision、decision、event 保持不可变；内存、浏览器缓存、Mock 和 UI 推导不得成为正确性前提。

## 影响

- 刷新后必须从 Canonical API 回读。
- UI 不得自行宣布“已发布、已批准、已验证、已激活”。
- M3 可缓存展示数据，但冲突、权限和最终状态必须服从服务端响应。

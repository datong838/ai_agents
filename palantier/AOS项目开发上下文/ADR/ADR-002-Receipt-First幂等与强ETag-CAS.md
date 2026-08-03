# ADR-002：Receipt-first 幂等与强 ETag/CAS

- 状态：Accepted
- 日期：2026-08-03

## 决策

所有 M2 POST 使用严格、单值 `Idempotency-Key`；Installation action 同时使用严格强 `If-Match`。服务端以持久化 receipt 处理幂等，并在回放时重新授权；并发状态迁移由 PostgreSQL CAS 裁决。

## 影响

- M3 SDK 为每次用户命令生成稳定幂等键，网络重试复用同一个键。
- action 使用最新 body `etagVersion` 构造 `If-Match: "N"`。
- 412/409 后回读详情并显式提示冲突，不在前端强行覆盖。
- 不修改通用 `api/client.ts` 的返回形状来获取 ETag。

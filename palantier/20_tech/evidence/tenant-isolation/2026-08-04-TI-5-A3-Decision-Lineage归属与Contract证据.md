# TI-5 A3 Decision Lineage 归属与 Contract 证据

> 日期：2026-08-04
> 结论：GREEN
> 代码：`68974ed`，tree `a37b08281f4846eeb0292e6940af0af175cff13a`

## 1. 归属证据与实施结果

- precheck 确认 631/631 满足 `lineage.id = 'lin-' || draft_id`，631/631 唯一命中 Draft，631/631 action/object 字段与父 Draft 一致，无 NULL scope、无一对多命中。
- 631 条均逐记录决策为 `ASSIGN_FROM_DRAFT`，归属父 Draft 的 `dev-org/dev-project`；未按时间、payload 或 ID 名称猜测。
- `decision_lineage_orphan_quarantine` 作为不可变可逆安全网；本次 quarantine=0，不等于删除隔离能力。
- 活跃表已冻结 `(org_id, project_id, id)` 主键、workspace FK、Draft 复合 FK、scope NOT NULL 及 ENABLE/FORCE RLS。
- Draft approval、lineage get、Analytics lineage/Quiver 和 Demo governance 均按完整 TenantScope 读写；无 scope 的 `aos_runtime` 可见 0。

## 2. 备份与真实可逆往返

- Git 外备份：`/private/var/tmp/aos-ti5-a3.OAHNwn/aos-meta-before.dump`，1,907,663 bytes，mode `0600`，SHA-256 `3c6ed2195abc836cbede6c8e809a73cb7fb8bd20cf95d95281694157d78b9b0a`。
- 共享库执行 `228ti5a2kv → 228ti5a3lineage → 228ti5a2kv → 228ti5a3lineage`。
- 降级到 A2 时原始 7 列聚合 hash 恢复为 `e0e211357213b2211e7c27c0032e7c4a`，与 precheck 基线一致；行数仍为 631。
- 再升级后活跃 631、ownership ledger 631、quarantine 0、parent orphan 0、ledger orphan 0，schema report `ok=true`。

## 3. 验证

- A3/Action/Draft/Analytics 核心：32 passed。
- Tenant Isolation 累计：195 passed / 7 skipped。
- 后端全量收集：9,204 tests collected，零 collection error。
- 目标静态致命错误、import 顺序和 diff check：GREEN。
- 五分支与五远端均为 `68974ed`，tree 一致；四 Worker clean，用户 `docs/toutiao-series/*` 未夹带。

## 4. 一致性纠正与剩余风险

- 原方案仅看到 `obj_instance` 直接匹配为 0，曾预计 631 条全部 quarantine；A3 只读取证找到了更强的唯一 Draft 父记录证据，因此依证据改为可审计归属，不丢失可恢复信息。
- A2 ContextVar 暴露的同步路由降权 DDL 问题已在本波修复：Action/Draft 建表移入 bootstrap，请求期不再 CREATE/ALTER。
- Demo 的跨请求内存 Dataset scope 尚未总收口，已列入 TI-5 C；不影响 A3 PostgreSQL lineage Contract，但阻止 TI-5 总 GREEN。
- 本波未连接真实商城、真实模型供应商或客户凭据。下一门为 TI-5 B1/B2。

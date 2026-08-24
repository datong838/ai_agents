# W4-06 SavedExploration 唯一 Store、分享生命周期与旧入口收敛 ADR

> 日期：2026-08-14  
> 核查基线：`w2-workshop@3e94339`，项目 authority `AOS-000023`  
> 状态：`AOS-000231_REVIEWED / IMPLEMENTATION_AUTHORIZED / CONSUMER_CLOSURE_IN_PROGRESS`  
> 边界：只读审查与实施包冻结；未修改源代码、迁移、数据库、真实租户或视觉稿

## 1. 结论

SavedExploration 当前不是“两套正式真源并行”：生产路由、前端唯一 SDK 与 Object Explorer 页面已经统一指向 `ontology_exploration_assets.py` 的 PostgreSQL authority；旧 `oe_enhancements.ExplorationEngine/SavedExploration` 没有被生产 Router 引用，只剩进程内代码与直接单元测试残留。

但 `DEP-O1` 仍不能标记 GREEN。现有实现只具备保存、列表、读取、CAS 更新、归档、恢复及按可见性读取，尚未具备产品方案要求的显式分享授权、opaque scoped ref、到期、撤销与相应审计语义。`visibility=workspace` 是工作区可见范围，不等于一个可到期、可撤销、可精确授权的分享生命周期。

因此 W4-06 的正确状态是：**唯一运行时 Store 基本成立，分享生命周期与旧残留收口未完成；W4 总开工门尚未满足，不提前编码。**

## 2. 当前实现事实

| 检查项 | 当前事实 | 判定 |
|---|---|---|
| PostgreSQL authority | `ontology_exploration_assets.py` 使用 head/revision/receipt 表、TenantScope、CAS、幂等键和 payload hash | `CODE_PRESENT` |
| Canonical API | `/v1/ontology/explorations` 的 list/create/get/update/archive/restore/execute 只调用 PostgreSQL authority | `UNIQUE_RUNTIME_PATH` |
| 前端唯一 SDK | `ontologyExplorationAssets.ts` 调 Canonical API，并在 create 后服务端重读比对 revision/hash | `CODE_PRESENT` |
| 工作台消费 | Object Explorer 只保存服务端资产；URL 仅携带 `viewRef`，不携带 payload | `REFERENCE_ONLY` |
| 旧内存实现 | `ExplorationEngine/SavedExploration/get_exploration_engine` 仍存在，但生产 Router 引用数为 0；旧测试仍直接覆盖它 | `DEAD_RESIDUE` |
| 双写 | 未发现正式路径同时写 PostgreSQL 与旧内存引擎 | `NOT_FOUND` |
| localStorage authority | 未发现 SavedExploration 写入 localStorage | `NOT_FOUND` |
| 分享生命周期 | 没有 share grant、opaque share ref、expiresAt、revokedAt 或 revoke Receipt | `MISSING` |

本次后端定向与邻接测试 `35 passed`。前端专项测试因当前执行环境没有 `node` 未运行，不能把它写成 GREEN；已有代码和历史测试只能作为线索，后续实施波仍须在具备 Node 的标准环境补跑。

## 3. 唯一 Authority 裁决

1. 唯一运行真源继续是 O1 PostgreSQL `ontology_*_asset_head/revision` 与 immutable receipt；不得在 AIP 或 Workshop 新建 SavedExploration Store。
2. Workshop 只持有 `SavedExplorationRef`，按 Principal、TenantScope、purpose 与授权状态回读；不缓存服务端授权结论。
3. URL 只允许 opaque ref，不允许 query、列定义、对象 ID 集、分享主体或授权 payload 进入 URL。
4. `workspace` visibility 仅表达资产可见范围；分享必须是独立、可审计、可到期和可撤销的 grant authority。
5. 旧内存类型不得再被新代码引用。实现波中删除或隔离旧类与测试；如发现历史数据入口，只允许单向、可对账迁移，不允许双写。

## 4. 分享生命周期最小合同

通用 O1 层应提供领域无关的不可变分享授权，不包含电商字段。建议最小合同：

```text
SavedExplorationShareGrant
  grantId / opaqueRef
  tenantScope
  explorationRef = assetId + exact revision/hash
  grantorSubject
  granteeScope = subject | workspace-role | link
  purpose / markings
  issuedAt / expiresAt / revokedAt
  status = active | expired | revoked
  receiptRef / version
```

硬约束：

- 创建、撤销均需 Idempotency-Key、CAS/版本校验和 immutable Receipt；
- 服务端每次解析 ref 时复验 tenant、exact revision/hash、purpose、marking、expiry、revoke；
- revoke/expiry 后旧 URL 立即失败关闭，不能依赖前端隐藏；
- link grant 不得扩大原资产 owner/visibility 权限，不得跨租户；
- 返回最小必要字段，不因分享泄露完整 query、PII 或对象集合；
- 归档资产、撤销源证据或 hash 漂移时，分享读取必须返回稳定 blocker。

## 5. 精确实施包

### 5.1 Red

1. 旧内存 `SavedExploration` 被正式 Router/Service 新引用时测试失败。
2. 没有 grant、错误租户、错误 purpose、过期、撤销、hash 漂移、归档资产均失败关闭。
3. 相同幂等键不同请求、旧 ETag、并发 revoke/create 返回稳定冲突。
4. URL 出现 payload 或 localStorage 被当作 authority 时测试失败。

### 5.2 Green

1. 在 O1 唯一 authority 上 additive 增加通用 share grant/receipt；如需迁移，必须单独取得唯一 migration Lease。
2. Canonical API 提供 create/list/revoke/resolve，不提供客户端租户注入。
3. 前端唯一 SDK 严格解析 share 状态与 blocker；页面只用 opaque ref。
4. 删除或隔离旧进程内模型、singleton 与旧测试，生产引用和双写扫描均为 0。
5. 重启回读、跨租户、expiry/revoke、归档、CAS、幂等、RLS/FORCE RLS、历史 revision 和浏览器刷新恢复全部 GREEN。

## 6. 文件边界与副作用

候选实现范围仅在正式授权时确认，预计涉及 O1 migration/authority、Canonical Router、唯一前端 SDK、Object Explorer 消费和邻接测试。禁止：

- 在 Workshop/AIP 新建第二张 SavedExploration 主表；
- 直接更新或删除 immutable revision/receipt；
- 把 `workspace` visibility 冒充分享生命周期；
- 通过 localStorage、URL payload 或前端判断实现授权；
- 未取得 migration Lease 时修改 Alembic；
- 使用真实租户对象或分享记录证明单元测试成功。

## 7. 门禁与下一步

- `DEP-O1-RUNTIME-UNIQUE-STORE`：`CODE_CONTROL_GREEN`；
- `DEP-O1-SHARE-LIFECYCLE`：`RED`；
- `DEP-O1-LEGACY-RESIDUE`：`RED`；
- W3 退出门：未通过；
- W4-06：`NOT_STARTED / IMPLEMENTATION_BLOCKED`。

只有 W3 GREEN，且分享生命周期、旧残留、重启/跨租户/撤销/到期验证全部通过后，才能勾选 W4-06。机器证据见 `aos-platform-w2-workshop/.evidence/workshop/2026-08-14-w4-06-saved-exploration-preflight.json`。

## 8. AOS-000231 实施前复审（2026-08-25）

### 8.1 过时结论更正

2026-08-14 的预检结论已被后续代码事实部分覆盖：

1. PostgreSQL authority 已增加 `ontology_exploration_share_grant` 与 immutable receipt，并具备 RLS/FORCE RLS、tenant scope、opaque ref、expiry、revoke、CAS/version、idempotency 和 exact revision/hash 复验。
2. Canonical Router 已提供 create/resolve/revoke；已有后端专项测试覆盖创建、解析、撤销、到期和 HTTP 合同。
3. 旧 `ExplorationEngine` 仍保留为兼容符号，但构造与 getter 均显式失败关闭，生产引用为 0；本波不为“形式删代码”破坏旧 import 兼容。
4. 当前真实缺口在消费侧：唯一 Web SDK 未严格解析 share grant，Object Explorer 未从 URL opaque `shareRef` 恢复 exact exploration，刷新、到期、撤销和 hash drift 不能在工作台层形成可见的失败关闭。

### 8.2 本波文件级清单

| 顺序 | 文件 | 最小改动 |
|---|---|---|
| 1 | `services/aos-api/aos_api/ontology_exploration_share.py` | 在原有 grant authority 上增加 purpose/markings 复验与 exact shared asset 组合读；不绕过 tenant/RLS。 |
| 2 | `services/aos-api/aos_api/routers/oe_enhancements.py` | 增加服务端验证后的 shareRef → exact exploration 只读端点，并传入 Principal markings。 |
| 3 | `services/aos-api/tests/aip/test_w_l16_saved_exploration_share.py` | 补充私有资产组合读、markings/purpose/hash/revoke/expiry 失败关闭。 |
| 3a | `packages/contracts/openapi/v1.yaml` 与 `v1.inventory.json` | 按确定性导出器同步新的只读路由合同，不手工编辑生成物。 |
| 4 | `apps/web/src/api/client.ts` | 增加不读写离线快照的 authoritative GET；撤销/到期 grant 不得被旧缓存复活。 |
| 5 | `apps/web/src/api/ontologyExplorationAssets.ts` | 增加 strict `ShareGrantView` parser 和 resolve API；拒绝多字段、非 active、租户/引用/哈希矛盾。 |
| 6 | `apps/web/src/api/ontologyExplorationAssets.test.ts` | 补充 active 正向与 malformed/status/hash/revision 失败关闭。 |
| 7 | `apps/web/src/pages/s2/workshop.tsx` | 仅消费 URL opaque `shareRef`，成功后用 exact asset 恢复工作台；不把 URL/localStorage 当 authority，不自动创建/撤销 grant。 |
| 8 | `apps/web/src/components/ontology/ObjectExplorerWorkspace.tsx` 及相关测试 | 对页内跳转保留经过字符白名单的 opaque `shareRef`，不保留 payload。 |
| 9 | `.evidence/workshop/2026-08-25-w4-06-saved-exploration-lifecycle.json` | 记录专项/累计/浏览器/一致性证据，不包含 opaque ref 实值。 |

### 8.3 安全与产品裁决

- 遵循 163/164：SavedExploration 是原子能力的 exact 上下文引用，由 Logic/数字同事组合，工作台只展示贡献视图，不复制 authority 或治理状态机。
- 本波不修改迁移，不执行真实 grant 创建/撤销，不发布；浏览器验收使用本地固定 fixture，不作为运营就绪证据。
- `viewRef` 继续用于当前 Principal 可直接读取的已保存视图；`shareRef` 只是服务端验证的 opaque capability ref，两者不互换、不在客户端扩权。
- 组合读只允许 `purpose=exploration_read`，要求 grant markings 是 Principal markings 的子集，且返回资产必须与 grant 的 assetId/revision/hash 完全相同；任一不符均不降级到普通 GET 或缓存。

# 228-M2 Installation 活跃指针历史一致性补强方案

## 1. 背景与问题

M2 冻结方案规定 installation revision 全量不可变，`current_revision`、`active_revision`、`previous_active_revision` 由数据库延迟一致性 trigger 关闭验证。当 current state 为 `active` 时，现有函数只要求 `active_revision = current_revision`，并要求非空 `previous_active_revision` 指向一条 `active` revision，但没有要求该历史指针早于 current revision。

这会允许 `previous_active_revision = current_revision` 的伪历史状态通过提交时检查，使“当前活跃版本”同时被冒充为“上一个活跃版本”，破坏 rollback 指针的历史语义。

## 2. 修复目标与非目标

目标：

1. current state 为 `active` 时，继续强制 `active_revision = current_revision`。
2. `previous_active_revision` 为非空时，必须指向同 installation 的 `active` revision，且严格满足 `previous_active_revision < current_revision`。
3. current state 为 `rolled_back` 时，继续严格强制 `active_revision IS NOT DISTINCT FROM previous_active_revision`，两者可同为 null；两者非空时都不得等于 `current_revision`。
4. 在真实 PostgreSQL 上覆盖非空 previous 的合法 active 与 rollback 路径，以及两类伪指针反例。

非目标：不修改 API/DTO，不改变状态机边，不改变 revision/event/etag 连续性规则，不改动已生效的数据表结构或用户数据。

## 3. 冻结不变式

| current state | `active_revision` | `previous_active_revision` |
|---|---|---|
| `draft/submitted/approved/rejected/applied` | null | null |
| `active` | 等于 `current_revision` | null，或指向状态为 `active` 且 revision 严格小于 current 的历史版本 |
| `rolled_back` | 与 `previous_active_revision` 严格相等（允许同为 null） | 非空时指向状态为 `active` 的历史版本，且与 active 一样不得等于 current |

`rolled_back` 的 current immutable revision 本身状态是 `rolled_back`，因此任一指向 current 的 active/previous pointer 都与上述状态引用规则冲突；仍在 `rolled_back` 分支显式关闭验证两指针不等于 current，避免未来改动指针状态校验时退化。

## 4. 最小实现

1. 在 Alembic migration 内 `assert_bundle_installation_consistency` 的 `active` 分支增加非空 previous 必须严格小于 current 的判定。
2. 在 `rolled_back` 分支保留 active/previous 的 null-safe 相等判定，并显式拒绝任一指针等于 current。
3. 扩展测试 helper，允许分别设置 active/previous，不改变默认生命周期用例。
4. 不重写已提交历史，以独立 commit 交付。

## 5. 真实 PostgreSQL 验证矩阵

| 用例 | 指针 | 期望 |
|---|---|---|
| 合法 active | current=10 active=10 previous=5，revision 5/10 均为 active | commit 成功 |
| 合法 rollback | current=11 rolled_back，active=5 previous=5 | commit 成功 |
| 伪 active 历史 | current=5 active=5 previous=5 | 延迟约束在 commit/`SET CONSTRAINTS ... IMMEDIATE` 失败关闭 |
| 伪 rollback 指针 | current=11 rolled_back，active=11 previous=11 | 延迟约束失败关闭 |
| 回归基线 | 现有 previous=null 的 active → rollback | 保持通过 |

实际测试 revision 可使用更小的连续序列，但必须同时满足 revision、event sequence、etag 连续性和 decision lineage，保证测到的是真实数据库不变式，而不是脱离其他约束的伪单元测试。

## 6. 风险、兼容与回滚

- 兼容性：修复只拒绝无法表示真实历史的指针组合，不影响合法 active/rollback 数据。
- 风险：若现有测试 helper 在每次 advance 时无条件清空 previous，新正例无法表达真实升级历史；仅扩展 helper 入参，默认值保持原行为。
- 回滚：代码层可独立 revert 本小修 commit；无 DDL 列或表变更，不需要删除用户数据。已存在的伪历史数据不应被静默接受，后续数据迁移必须先单独审计。

## 7. 退出门

1. 新增的真实 PostgreSQL 正负用例全绿。
2. 现有 composition/installation migration 专项全绿。
3. Asset Registry 相关回归全绿，无新 lint/format 问题。
4. 代码不变式、测试矩阵与本方案表达一致，无未说明的状态机扩展。

# W7-05 ArtifactFamily、Master、Variant 与 Supersedes 预检 ADR

> 状态：`IN_PROGRESS / DEPENDENCIES_GREEN / NO_EXTERNAL_EFFECT / NO_RELEASE`  
> 当前事实：`AOS-000259`，`m1@3e364b59`

## 1. 裁决

W7-05 不创建媒体 payload、媒体 lineage 或可变“当前版本”第二真源。Artifact 正文继续使用 canonical `aip_artifact` 与对象存储；家族 manifest 作为 typed immutable Artifact；关系继续使用 W2-C canonical `ArtifactRelation`。现有四类通用边是必要基座，但没有关闭媒体 family 语义和 Artifact 本体不可变门。

关系方向固定为“新/子 → 旧/父”：member → family manifest、Variant → Master、新 revision → 被 supersede 的旧 revision、派生产物 → source。每个成员只属一个 family，每个 Variant 只指向一个同族 Master；supersedes 只允许同族、同角色、同 artifact type 与兼容 profile/platform/rendition spec。关系、Artifact、Approval 和 Receipt 均不可覆盖。

并发形成多个未被 supersede 候选时返回 `conflict`，禁止按 `created_at` 猜当前版本。显式 `FamilySelectionDecision` 固定 expected family revision、candidate exact hashes、actor、reason、policy 与 CAS 结果。它选择未来消费候选，不删除分叉和历史执行事实。

## 2. 生命周期与真源分离

`preview`、`draft`、`master`、`variant` 是 Artifact 创建时冻结的角色；`approved` 是 Approval authority 对 exact Artifact hash 的决定；`executed` 是 Action/Delivery Receipt 对同一 approved hash 的外部事实。ProductionStart 不能代替外部发布 Approval/Lease，UI 不能通过修改 Artifact 状态宣称已批准或已执行。

新 Variant、supersedes 或 selection decision 不重写旧 Approval/Receipt。未来执行旧批准版本时，Action 门重验 family selection、policy、license、平台 spec、ImpactPreview 和 exact hash；历史已执行版本仍按 Receipt 原样可追。

## 3. 当前已验证基座

- W2-C 的 `ArtifactRelation` 支持 `family_member`、`variant_of`、`supersedes`、`derived_from`；
- Store/API 按 tenant scope 运行，创建命令幂等并重验两端 content hash；
- Store 与数据库拒绝 self relation、hash drift 和有向环；relation 行 append-only；
- canonical API、严格 SDK 与 AIP 控制面已存在；W2-C focused contract/API `8 passed`；
- W2-D ImpactPreview/ProductionStart 已进入当前 m1，但不等于媒体 Artifact family 已实现。

## 4. 实现阻断

1. W7-04 未 GREEN，尚无可信媒体 Stage 输出可进入 family；
2. `aip_artifact` 无数据库 append-only 防护，且 content hash 仍可为空；
3. 无 typed family manifest 校验、family revision 或冲突/选择 authority；
4. 无 role/cardinality、同族/同类/spec compatible supersedes 约束；
5. 无 Stage/attempt/template/capability/provider/policy/license/Eval/Evidence exact lineage 闭合；
6. 无 Artifact → ImpactPreview → Approval → Start/Action → Receipt 的同 hash 绑定；
7. tenant-wide list 不提供稳定 family topology、family filter、分页与 current/conflict 语义；
8. 无媒体工作台 family timeline、选择干预、批准/执行分离视图；
9. 无 `org-org/dev-project` 正向 family 与 `dev-org/dev-project` 隔离 canary。

## 5. 退出门

- Artifact 本体、family manifest 与关系均有数据库级不可变保护和 exact hash；
- family/member/Variant/Master/supersedes 的方向、基数、类型、同族与并发分叉测试 GREEN；
- family 读取稳定重建历史、current/conflict、选择决定、批准和 Receipt，重启后不变；
- preview/draft/approved/executed 不混，旧 Variant 与旧 Receipt 永不覆盖；
- Store/API/SDK/UI、RLS/FORCE RLS、幂等/CAS、双租户、浏览器与安全证据齐全；
- W7-04 以及本项所消费的 W2-C/D exact authority 均在开工时重新核验 GREEN。

## 6. 两轮审查

第一轮产品与生命周期审查：家族关系和用户可干预选择可见，Master/Variant 不混，批准与执行分离，旧版本与历史 Receipt 保留；`PASS`。

第二轮技术与安全审查：复用唯一 Artifact/Relation authority，typed manifest 不复制 payload，关系方向/基数/同族约束、并发 conflict、CAS、exact refs、RLS 与 fail-closed 边界完整；9 项实现缺口如实保留，无代码、迁移、真实租户或外部动作；`PASS`。

结论：W7-05 产品—技术合同可以作为后续实现基线，但依赖和代码证据未闭合，清单保持未勾选。

## 7. 2026-08-25 独立现状复核

W7-04 已由 `3e364b59` 完成并投影为 `AOS-000259`，原依赖阻断解除。当前继续复用 W2-C 的唯一 `aip_artifact_relation`，并在 canonical `aip_artifact` 上补强 family identity/role/spec/lineage，不建立媒体 payload、媒体 lineage 或 Workshop Artifact 第二真源。

现状复核确认：`aip_artifact` 仍允许空 content hash 且允许 UPDATE/DELETE；通用 relation 只有 hash/cycle 校验；无 family head、typed member contract、同族 role/cardinality/spec 约束、current/conflict 判定或 immutable selection decision；Production Contracts 页面只能列通用 relation。以上均转为本波实施项，不再写作等待其他人交付。

本波继续遵循 163/164：Artifact family 是 Logic 产出与交付 authority，不冒充 Skill；Artifact lineage 引用 exact Stage/attempt/template/capability/assignee/provider/policy/license/Eval/Evidence，工作台只投影“原子 Skill → Logic 编排 → 数字同事绑定 → 当前 Artifact 贡献”，缺失 exact ref 时诚实失败关闭。

## 8. 文件级实施清单

1. 新增 `w7_003` 迁移：对 `aip_artifact` 增加 family/role/revision/profile/platform/rendition/lineage 字段和数据库 append-only 防护；对既有空 hash 在升级前失败关闭，不静默补造；新增 tenant RLS/FORCE RLS 的 family head 与 append-only selection revision。
2. 扩展 Production Contract：typed family manifest/member、Master/Variant、family topology、current/conflict、candidate exact hash snapshot、CAS selection decision；preview/draft/master/variant 只作创建时冻结角色，approved/executed 继续由独立 Approval/Receipt 判定。
3. Store/API 在一个事务中验证 exact Artifact hash、family manifest、单 family membership、Variant 单 Master、同族同 role/type/profile/platform/rendition 的 supersedes、并发 candidate conflict 与 selection CAS；只写 canonical ArtifactRelation 和 immutable decision。
4. `AipTaskStore.record_artifact` 仅在显式 typed family metadata 完整时写入新 canonical 列；普通 Artifact 路径保持兼容，不从 UI 或字符串猜 family 健康。
5. strict Web SDK 与 Production Contracts 页面新增 family topology/timeline、current/conflict、Master/Variant、批准/执行分离和选择干预只读视图；本波不点击任何副作用按钮。
6. 补齐专项、W2-C/D 与 W7-04 累计回归、OpenAPI/Alembic、安全、双租户和内置浏览器三视口证据；不 apply migration、不写真实业务数据、不调用 Provider、不发布。

开工 Task Receipt/Lease：`workshop-w7-05-artifact-family-master-variant-supersedes-20260825`。第一轮产品复审保持家族分叉与选择可见、角色/批准/执行分离；第二轮技术复审保持单一 Artifact/Relation authority、append-only、CAS、RLS 与 exact hash，允许进入最小实现。

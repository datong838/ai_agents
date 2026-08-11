# AIP-4 E3D 外部 ResearchJob 权威链对账

> 日期：2026-08-12
> 结论：**IMPLEMENTED_GREEN**
> 真实范围：`org-org / dev-project`
> 隔离 canary：`dev-org / dev-project`

## 1. 本波目标

在既有 Task/Run、Plan、Lineage 与 Artifact 真源之上，为 DeerFlow 等外部研究适配器增加可审计、可重放、失败关闭的事实层；不建立第二套 Task 状态机，不把 callback 到达或进程内状态当作成功。

## 2. 已完成

- 版本化、租户范围 ProviderRevision；仅当前最高且 enabled 的 exact revision 可提交。
- 不可变 JobManifest 绑定 TaskRun、PlanRevision、PlanStep、capability、provider 与 exact lineage event。
- Submission、ProviderEvent、CallbackNonce、Artifact、Delivery/Reconcile 全部使用 append-only Receipt。
- callback HMAC、持久 nonce、防重放、event sequence gap、Artifact hash/capability 漂移、unknown/reconcile 均失败关闭。
- `aip4_008` 线性补强 exact lineage；若已有 Job 行则拒绝猜测式回填。
- Canonical API、错误映射、角色权限、路由聚合与 OpenAPI 契约已冻结。

## 3. 代码提交

- `849f40d feat(aip): persist external research job authority`
- `e7542db feat(aip): expose research job authority api`
- `a88cad1 feat(aip): bind research jobs to exact lineage`

三者均位于并已推送 `aos-platform/m1`。

## 4. 验证结果

- exact lineage migration/store/API 定向门：13 passed。
- AIP 累计回归：118 passed，7 个既有 warning，零失败。
- Ruff、compileall：GREEN。
- OpenAPI：确定性导出与契约测试 GREEN。
- Alembic：`aip4_008 (head)`，current/head 一致。
- `org-org/dev-project`：七张 ResearchJob 权威表全部 0，未伪造外部成功或产物事实。
- `dev-org/dev-project` canary：同样空读，不能越 scope 访问测试事实。
- 七表均 `RLS=true`、`FORCE=true`、两枚 append-only/truncate guard；JobManifest 三个 lineage 列均 NOT NULL。

## 5. 关键裁决

1. ResearchJob 当前状态只能从持久化 Receipt 推导。
2. `lineageRef` 必须是当前 TaskRun 根的最新 sequence；缺失、旧 sequence、跨 Run 或跨 scope 一律阻断。
3. 外部副作用超时保持 `unknown`；禁止盲重试，只有 Reconcile Receipt 可收敛。
4. 外部 Artifact 继续复用 `aip_artifact` 真源；ResearchJob 只追加绑定 Receipt。

## 6. 当前风险

- E3D 只交付通用外部研究权威链，没有生成真实外部 ResearchJob；真实租户空表是正确证据，不是缺数。
- Provider 的真实适配器配置、凭据和外部调用属于后续具体平台/知识研究任务，不能用 fixture 冒充。
- 7 个测试告警为既有 Pydantic/Starlette 警告，不是本波失败。

## 7. 下一门

进入 E4 前先复核 05-11 三页面的现有代码与 SDK：页面必须只消费 Canonical API/唯一 SDK，禁止固定 trace、Mock、静态数组和合成趋势；涉及页面必须使用内置浏览器逐项验收。

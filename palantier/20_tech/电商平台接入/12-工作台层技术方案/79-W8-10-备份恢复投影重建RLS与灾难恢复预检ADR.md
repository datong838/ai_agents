# W8-10 备份恢复、投影重建、RLS 与灾难恢复预检 ADR

> 日期：2026-08-15  
> 状态：`ENGINEERING_DR_CONTRACT_BROWSER_GREEN / REAL_RESTORE_AND_DRILLS_BLOCKED / NO_DATA_OPERATION / NO_EXTERNAL_EFFECT / NO_RELEASE`
> 基线：`AOS-000279`、代码 `d7eed3fee0915733d40cd1872493bdf486fdb844`、证据 `2b720d484988bcd678778204f3cd53d6e66668b8`
> 证据：`.evidence/workshop/w8-10/`；历史预检 `.evidence/workshop/2026-08-15-w8-10-backup-projection-rebuild-rls-disaster-recovery-preflight.json`

## 1. 决策

W8-10 是全 authority、对象存储、投影、安全边界和外部事实共同恢复门。历史上的七项上游工程依赖现已闭合，但仍没有批准的隔离 DR target、真实备份集、RPO/RTO、恢复角色分离与全量演练证据；本轮实现只读、失败关闭的工程判定与贡献视图，不读取或恢复真实数据。

## 2. 备份与恢复顺序

备份 inventory 覆盖 Registry/Installation、领域 revision/event、Task/Run/Handoff、Evidence/Artifact/Eval、Action/Receipt/Usage/Lineage、Memory/Wiki/SavedExploration、Adapter/Account/Policy/Alert/Reconcile 及对象 manifest。每份备份固定 log position、schema/app/Bundle hash、加密密钥 revision、retention 与 restore dependencies；Secret 内容不进入 EvidencePack。

恢复严格按 identity/tenant/policy/key/Registry → immutable authority → integrity checks → FORCE RLS negatives → disposable projections → external reconcile → read-only API/browser → approved phased mutation。缺 hash、ref、Receipt、RLS 或兼容性即停，不用缓存/索引补 authority。

## 3. 投影、RLS 与外部事实

投影重建必须 tenant-scoped、幂等、checkpointed、可恢复、限速，并报告 missing/extra/revision mismatch/conflict/unknown；重建不改变 authority revision。恢复角色不是 RLS 默认 bypass；覆盖 no-scope、wrong-scope、后台 finally reset、`org-org` 正向与 `dev-org` 负向。

数据库回档不能撤销外部效果。Provider late result、unknown、Webhook gap、Usage/Settlement、预算/频控敞口与 in-flight Lease 必须按原 fingerprint/Receipt reconcile；禁止重新发消息、调价、退款、发布或收费 Job。

## 4. 演练与证据

演练覆盖 PITR、损坏最新备份回退、对象缺失/hash 漂移、投影崩溃续建、密钥不可用/轮换、RLS/GUC 泄漏、旧应用/Bundle 不兼容、Provider 迟到/重复、区域依赖故障与 failback。EvidencePack 保存每阶段耗时、RPO/RTO 实测、行/hash/revision 对账、RLS、浏览器、external reconcile、RecoveryDecision Receipt 与 residual unknown。

## 5. 两轮审查

第一轮把 authority restore 与 disposable projection rebuild 分开，并把 RLS 验证前移到投影之前。第二轮补齐 key/PII/retention、外部事实不随数据库回档、分阶段恢复写入、failback 与 RPO/RTO 实测要求。合同通过；当前只允许实现无数据操作的证据判定，实际恢复和演练仍硬阻断。

## 6. 2026-08-26 串行实施范围与文件级清单

本波只消费调用方提供的结构化 EvidencePack，不主动读取数据库、对象存储、备份介质、密钥、Provider 或真实租户。实现文件如下：

1. `apps/web/src/components/workshop/workshopDisasterRecoveryReadiness.ts`：新增纯计算 DR 就绪判定。它校验 exact release/Bundle/Installation/DR plan roots、authority inventory、backup manifest、恢复依赖顺序、加密/retention 元数据、RPO/RTO 批准与实测、隔离 target、角色分离、RLS no-scope/wrong-scope/finally-reset/双租户负向证据、投影重建守恒、external reconcile、分阶段恢复与 failback Receipt，以及完整 drill EvidencePack。
2. `apps/web/src/components/workshop/workshopDisasterRecoveryReadiness.test.ts`：覆盖无证据、backup hash/ref 缺失、authority/projection 混淆、RLS 未先验、投影改变 authority revision、external unknown 未对账、角色未分离、RPO/RTO 未批准/未实测、drill 缺失和完整证据纯计算 GREEN。
3. `apps/web/src/components/workshop/WorkshopDisasterRecoveryCard.tsx` 与测试：提供只读贡献视图，按“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献”显示 backup、RLS、projection、external reconcile、RPO/RTO 与 drill 状态；缺权威数据时显示 unknown/blocked，不显示虚构 0、成功率或恢复完成。
4. `apps/web/src/components/workshop/TaskCockpitPage.tsx` 与现有测试：将 DR 卡片作为独立只读门挂入 Task Cockpit，Task API 失败不删除卡片，既有任务/交接功能不回退。
5. `.evidence/workshop/w8-10/`：保存专项、累计、构建与内置浏览器验收；视觉 fixture 只用于布局和失败关闭，不作为真实备份、RLS、DR 或 operational 证据。

所有 `inspectBackup`、`restore`、`rebuildProjection`、`changeRls`、`reconcileExternal`、`failover`、`failback` 命令保持 false。不得新增后端写 API、迁移、真实数据探针、连接字符串、Secret 或可执行恢复脚本。

## 7. 验收与停止条件

- 缺 exact ref/hash/cutoff、批准 RPO/RTO、隔离 target、角色分离、RLS 四类负向证据、authority 守恒、external reconcile、RecoveryDecision Receipt、drill EvidencePack 任一项即失败关闭。
- authority restore 与 projection rebuild 必须分轴显示；投影重建不得改变 authority revision，数据库回档不得把 Provider late/duplicate/unknown、Usage 或 in-flight Lease 推断为已撤销。
- 专项测试、Task Cockpit 既有测试、Web 全量、TypeScript 与生产构建不得回退；页面必须用内置浏览器确认唯一主标题、无横向溢出、unknown 不归零、无恢复按钮或其他数据操作入口。
- 任一真实数据操作、迁移、RLS 变更、Provider/Action、外部副作用或发布入口出现，立即停止闭合。
- 本波最多签发 `ENGINEERING_DR_CONTRACT_BROWSER_GREEN / REAL_RESTORE_AND_DRILLS_BLOCKED / NO_DATA_OPERATION / NO_EXTERNAL_EFFECT / NO_RELEASE`；它不等于备份可恢复、RPO/RTO 达标、灾备 ready 或 release GREEN。

## 8. 2026-08-26 实施与验收闭环

W8-10 已按第 6 节的文件级清单完成最小实现。纯计算 evaluator 将 authority inventory、backup manifest、十二阶段恢复顺序、RPO/RTO、隔离 target、职责分离、四类 RLS 负向证明、投影守恒、五类外部事实、恢复/failback Receipt 与十类 drill 分轴判定；所有数据操作命令恒为 false。只读卡片已挂入 Task Cockpit，并保持“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献”产品链路。

验收结果：

- 专项：`3 files / 23 tests` GREEN；其中 evaluator 8 项、卡片 1 项、Task Cockpit 14 项。
- 累计：Web `247 files / 2228 tests` GREEN；TypeScript `tsc --noEmit` GREEN；生产构建 `349 modules` GREEN。既有 React act/Router 与 chunk warning 未扩大为失败。
- 内置浏览器：正式无 API 路径保持失败关闭；只读视觉夹具下唯一 H1、唯一 main、1280×720 无横向溢出，卡片显示“灾备失败关闭”和 34 个 blocker，authority `0/8`、RLS `0/4`、external `0/5`、drill `0/10`，未知 backup/projection/RPO-RTO 没有伪装成 0，卡片按钮为 0，未出现可用数据操作入口。视觉夹具不构成真实 authority、备份、RLS 或 DR 证据。
- 代码提交：`d7eed3fee0915733d40cd1872493bdf486fdb844`；证据提交：`2b720d484988bcd678778204f3cd53d6e66668b8`；证据目录：`.evidence/workshop/w8-10/`。

方案/代码一致性复审通过：没有 migration、真实数据读取/恢复、RLS 变更、Provider/Action、外部副作用或发布入口。真实备份、隔离恢复、RPO/RTO 实测与全量演练仍无权威正向证据，因此结论严格为 `ENGINEERING_DR_CONTRACT_BROWSER_GREEN / REAL_RESTORE_AND_DRILLS_BLOCKED / NO_DATA_OPERATION / NO_EXTERNAL_EFFECT / NO_RELEASE`，不提升为 operational 或 release GREEN。下一波按串行 Loop 进入 W8-11 累计门。

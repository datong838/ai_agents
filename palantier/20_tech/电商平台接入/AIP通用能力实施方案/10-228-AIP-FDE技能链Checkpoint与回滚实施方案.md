# 228-AIP FDE 技能链、Checkpoint 与回滚实施方案

> 状态：**评审通过 · v1.0 方案基线（仍不授权编码）**
> 对应阶段：AIP-10（FDE 侧）。

## 1. 纠偏

13-* 是目标架构，不代表代码已完成。微商城 FDE 已形成不可变 bundle、D0-D4、7 Pipeline、6 Logic、4 Workshop 的专项规范；本方案只抽取通用 FDE 能力，不重跑旧 bootstrap，不把平台账号接入提前到本波。

## 2. 六步 Skill Chain

1. 需求与平台能力澄清。
2. 认证方案与 secretRef 配置草稿。
3. API/Schema 探索与 capability probe。
4. 字段映射/OKF 提案与冲突检查。
5. Pipeline/同步/调度配置草稿。
6. 只读测试、质量检查、证据封板。

每步产生 PlanStep、Artifact/Evidence 和 Checkpoint；高风险步骤进入 Draft，不能由“Reflection 自审”代替人工批准。

## 3. Bundle 与实例化

- `SkillBundle` 不可变，包含 manifest、schemas、Logic refs、EvalPack、migration、rollback descriptor。
- `AdapterPack` 只放平台能力、认证、字段和限流差异。
- `InstanceOverlay` 只放组织策略、对象选择、调度和工作台定制。
- 安装通过现有 M1～M5 Asset/Resolver/Lock/Installation/Evidence 主链。

## 4. Checkpoint/回滚

- Checkpoint 引用状态快照和已创建资源，不复制凭据。
- 回滚只清理由本 run 创建且 receipt 可证明所有权的资源。
- 外部系统 unknown 状态先 reconcile，不盲目补偿。
- Pipeline/Logic/Workshop/Overlay 分别有 rollback descriptor。
- O1 Waves 1～10 及历史 D4/D5 已封板；本方案只读取其 authority 与证据，不创建同名阶段、不修改其 GREEN 结论。

## 5. 文件边界

```text
solution-packs/ecommerce-fde/*
services/aos-api/aos_api/aip_fde_orchestrator.py
services/aos-api/aos_api/aip_fde_skill_registry.py
services/aos-api/aos_api/aip_fde_handoff.py
services/aos-api/aos_api/aip_fde_checkpoint.py
services/aos-api/aos_api/aip_fde_rollback.py
apps/web/src/pages/fde/FdeTaskPage.tsx
apps/web/src/pages/fde/FdeCheckpointPage.tsx
```

SolutionPack 和 FDE orchestrator/page 均为新增候选；Skill Registry、Handoff、Checkpoint 必须复用 AIP-1/AIP-6 公共服务，不能在 `ecommerce-fde` 下再建一套运行数据库。

## 6. 阶段门与失败处置

- FDE-0 冻结 SkillBundle/AdapterPack/InstanceOverlay schema 与 M1～M5 安装主链映射。
- FDE-1 只读 capability probe 与 schema discovery；凭据未就绪时保持 blocked。
- FDE-2 生成 Pipeline/Logic/Workshop/Overlay Draft 和 diff，不直接安装。
- FDE-3 审批后安装到隔离实例并运行 contract/quality/tenant tests。
- FDE-4 生成独立 AIP-FDE EvidencePack，完成回滚演练后才可供 AIP-10 场景消费。

失败时保留 Checkpoint、已创建资源清单和下一步建议；不得自动改用浏览器抓取、Mock API 或默认租户数据。外部状态 unknown 时整个相关阶段保持 blocked，直到 reconcile。

## 7. 验收

- 每个步骤可暂停、恢复、回读；重启不丢。
- 平台 capability 不足时生成阻断，不用浏览器/Mock 自动补成功。
- 字段映射与 O1 canonical schema 冲突时不创建第二对象。
- 回滚不删除预存资源或其他租户资源。
- 完成 AIP-FDE 独立 EvidencePack 和回滚演练前不得标记“可接平台生产”。
- 同一 SkillBundle 在两个组织实例化时 Overlay 可不同，但模板 hash、安装 Receipt 和租户数据互不污染。

# 228-AIP FDE 技能链、Checkpoint 与回滚实施方案

> 状态：**待评审 · 不授权编码**
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

## 6. 验收

- 每个步骤可暂停、恢复、回读；重启不丢。
- 平台 capability 不足时生成阻断，不用浏览器/Mock 自动补成功。
- 字段映射与 O1 canonical schema 冲突时不创建第二对象。
- 回滚不删除预存资源或其他租户资源。
- 完成 D4/D5 独立证据前不得标记“可接平台生产”。

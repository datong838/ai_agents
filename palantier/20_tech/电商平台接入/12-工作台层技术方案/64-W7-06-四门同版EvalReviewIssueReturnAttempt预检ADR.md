# W7-06 四门同版 Eval、ReviewIssue、ReturnDecision 与新 Attempt 预检 ADR

> 状态：`COMPLETED_CODE_CONTRACT_BROWSER_GREEN / SECURITY_SCOPED_GREEN / REPO_BASELINE_RED / NO_EXTERNAL_EFFECT / NO_RELEASE`
> 当前事实：以 `AOS-000261` 为开工基线，代码提交 `m1@7787fcc1`、证据路径对齐提交 `m1@1c79d07f`；任务 `workshop-w7-06-four-gate-eval-review-return-attempt-20260825` 已形成 Delivery Receipt 并释放 Lease。

## 1. 裁决

W7-06 复用 AIP canonical EvalContract/EvalRun/EvalReport、ReviewIssue/Event、ReturnDecision、StepRun attempt 和 ArtifactRelation，不创建媒体专用 Eval、Issue 或返工状态机。媒体层只贡献签名四门 profile 与可重建投影。

四门固定为 `fact`、`brand`、`copyright`、`platform`，由 immutable `MediaGateSetDecision` 证明同一 Artifact hash、EvalContract revision、policy/cutoff、dataset/judge、Stage attempt 与 review cycle。missing、stale、conflict、unknown 失败关闭；四个不同版本的单项通过不能拼成 4/4。平台门必须针对待交付的 exact Variant/platform spec。

## 2. Issue、返工与复评

blocking finding 必须引用 exact EvalRule、EvalReport、Evidence、Artifact/location 和 server-resolved return stage。ReturnDecision 计算 invalidation set/reuse decisions；新 StepRun attempt 输入显式引用 Issue、Decision、源 Artifact、修复 Evidence/Artifact 与原 EvalContract。执行器按 Stage 最大 attempt 判定，禁止旧 succeeded 遮蔽新 queued。

未受影响且输入、规则、合同、policy/license/provider 等依赖 hash 一致的收费 Stage 或 gate 才可复用，并留下 reuse proof；历史 Usage/unknown 不删除。替代 Artifact 产生后对受影响 gate 重跑，并为新 Artifact 形成完整 GateSet。合同若变更，使用 `ContractMigrationDecision` 开新周期，不静默改用 latest。

完整 4/4 仅允许进入独立 Approval。Issue resolved、ReturnDecision、queued/succeeded attempt 或单门通过均不能冒充批准。

## 3. 2026-08-25 实时基座复核

- W4-03 已 GREEN：EvalContract → EvalRun/EvalReport exact lineage、当前 publication/release transitive invalidation 与服务端 Diff 已闭合；
- W4-04 已 GREEN：ReviewRuleRevision、ReviewIssue/Event、ReturnDecision、latest attempt、server-owned invalidation/reuse、角色门与 Task Cockpit 读模型已闭合；
- W7-05 已 GREEN：canonical Artifact/ArtifactRelation 之上已有 immutable Family、Master、Variant、supersedes、并发 conflict 与显式 exact selection；
- W7-04 已保证执行器只消费 latest attempt，旧 succeeded 不遮蔽新 queued；
- 现有通用 EvalReport 仍未保存媒体 subject Artifact 与 Stage attempt exact ref，现有 ReviewIssue 也尚未被四门 GateSet 聚合 authority 约束，这是本波必须最小补齐的真实缺口。

## 4. 本波文件级实现清单

1. `services/aos-api/alembic/versions/w7_004_media_four_gate_review.py`：为 EvalRun/EvalReport 增加兼容可空、W7 使用时必填的 subject Artifact/Stage attempt exact snapshot；新增 append-only MediaGateProfile、MediaGateSet、ContractMigrationDecision，启用 RLS/FORCE RLS 和运行角色最小权限；
2. `aip_eval_contracts.py`、`aip_eval_authority_store.py`、`aip_eval_runner.py`：保留历史普通 Eval 兼容，新增成对精确绑定和回读；W7 媒体评价必须验证 Artifact hash 与 latest StepRun attempt；
3. `aip_production_contracts.py`、`aip_production_contract_store.py`：实现固定 `fact/brand/copyright/platform` profile、四门同 Artifact/Contract/Policy/Cutoff/Dataset/Judge/Attempt 聚合、missing/stale/conflict/unknown 失败关闭、hard-block 不可 override、平台门 exact Variant/spec 校验；失败门必须绑定 exact Rule/Report/Issue 和合同映射的 server-owned return stage；
4. 同一 Store 增加 ContractMigrationDecision：合同变化只能显式开新 review cycle，禁止把不同合同 revision 的单门结果拼成 4/4；替代 Artifact 必须形成新 GateSet，历史报告、Issue、Usage 和 ReturnDecision 不删除；
5. `routers/aip_production_contracts.py` 与 OpenAPI：只开放 tenant-scoped canonical API；写操作沿用 review/control 角色、Idempotency-Key 与 append-only/CAS；
6. `apps/web/src/api/aipProductionContracts/` 与 `ProductionContractsPage`：strict parser/SDK 只读展示四门、阻断、Issue/Return/new attempt/replacement lineage、approval eligibility 和“原子 Skill → Logic 编排 → 数字同事 → 工作台贡献”上下文，不创建第二状态机；
7. `test_w7_06_media_four_gate.py` 与邻接累计测试：覆盖 4/4、missing/unknown/conflict、跨 Artifact/Contract/Policy/Cutoff/Attempt 拼接、平台 Variant 漂移、hard-block override、older succeeded + newer queued、invalidation/reuse、替代 Artifact 复评、contract migration、幂等/CAS、RLS 与双租户；
8. 生成 evidence、执行 OpenAPI/Router/compileall/Web 全量、内置浏览器三视口、定向安全扫描与方案一致性复审。迁移只在一次性测试库验证，不 apply 到共享或真实环境。

## 5. 退出门

- 四门 4/4 同版、缺失/unknown、平台 Variant、hard-block override 负向测试 GREEN；
- older succeeded + newer queued return 必须执行新 attempt；
- invalidation/reuse、收费 Stage 不重复与 Usage 保留证据闭合；
- Issue/Decision/attempt/replacement Artifact/rerun GateSet/Approval 全谱系可回读；
- Store/API/SDK/UI、RLS、权限、幂等/CAS、双租户、浏览器与安全证据齐全；
- W4-03/04 与 W7-05 在开工时重新核验 GREEN。

## 6. 两轮审查

第一轮产品与生命周期审查：四门状态同版可见，Issue 到 Stage 到新 Artifact 全过程可干预，未受影响工作可解释复用，批准与评估分离；`PASS`。

第二轮技术与安全审查：唯一 Eval/Issue/Task/Artifact authority、exact GateSet、latest attempt、invalidation/reuse、合同迁移、hard block 与 fail-closed 完整；10 项实现缺口未误写为完成，无代码、迁移、真实租户或外部动作；`PASS`。

结论：旧依赖阻断已经解除，W7-06 已按唯一开发者串行实施完成；代码、合同、测试、内置浏览器、安全与 Delivery Receipt 已闭合，authority CAS/Prime 回读完成后进入 W7-07。

## 7. 开工边界与 163/164 一致性

- 四门评价复用 `review-output-quality`、`verify-claims` 等原子 Skill 的 canonical Eval/Review 产物，由 Logic 固定四门组合与 return mapping；数字同事只绑定职责，工作台只消费贡献投影；
- 工作台不复制 Eval、Issue、Task、Artifact 或 Approval authority，不用 UI 状态、旧 succeeded、单门通过或 Issue resolved 冒充 4/4 或批准；
- 本波不调用 Provider、不生成媒体、不提交真实评价/Issue/Return、不写 `org-org/dev-project` 业务数据、不发布；`dev-org/dev-project` 只用于隔离负向测试。

## 8. 实施与验收闭环

- 代码：`7787fcc1` 新增兼容可空的媒体 Eval subject/attempt/policy/cutoff exact binding、签名四门 profile、同版 GateSet、ReviewIssue return-stage 校验和显式 ContractMigrationDecision；`1c79d07f` 仅把证据文件名对齐 Task Receipt 的冻结 scope。
- 后端：W7-06 专项 `4 passed`；W4/W7 累计 `44 passed`；OpenAPI 合同 `14 passed`；Domain Router `8 passed + 2 subtests`；compileall 与 diff check GREEN。OpenAPI 为 `2651 paths / 2344 schemas / 4426 operations`，inventory/runtime route 为 `4436/4440`，runtime hash 为 `22ea804fc4135987161d0a04f69eade53be01818cd9d8bc88ea6fe6a796ee5b1`。
- Web：ProductionContractsPage 定向 `17 passed`，全量 `232 files / 2137 tests`，build `344 modules` GREEN；工作台按“原子 Eval Skill → Logic 四门编排 → 媒体数字同事 → 贡献视图”展示，不复制 Eval/Issue/Approval authority。
- 数据库：Alembic 单头 `w7_004`；只在 disposable database 验证 upgrade/downgrade、RLS/FORCE RLS 与 append-only，不 apply 到共享或真实数据库。
- 浏览器：内置浏览器在受控 fixture 的实际 `1280x720` 视口显示四门、`issue-copyright-browser@v1`、`MEDIA_GATE_COPYRIGHT_FAILED` 与禁用生产启动，无横向溢出，本轮刷新新增 console error 为 `0`。浏览器临时 viewport override 未生效，因此不声称 768/1440/1920 三档通过。
- 安全：本波 18 个 scope 文件扫描 `0 critical / 0 warning`；全仓仍是既有 `5 critical / 326 warning` RED 基线，未把局部 GREEN 冒充仓库 GREEN。

退出结论：`W7_06_MEDIA_FOUR_GATE_SAME_ARTIFACT_EVAL_REVIEW_RETURN_ATTEMPT_CODE_CONTRACT_BROWSER_GREEN_SECURITY_SCOPED_GREEN_REPO_BASELINE_RED_NO_EXTERNAL_EFFECT_NO_RELEASE`。证据：`.evidence/workshop/2026-08-25-w7-06-four-gate-eval-review-return-attempt.json`；未写真实租户、未 apply 共享迁移、未调用 Provider、未生成媒体、未执行 Review Return/合同迁移、未发布。下一串行入口为 W7-07。

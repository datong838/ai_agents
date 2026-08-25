# W8-09 SLO、告警、Unknown Backlog、Reconcile Age、Usage 与 Runbook 预检 ADR

> 日期：2026-08-15  
> 状态：`OPERATING_CONTRACT_APPROVED / IMPLEMENTATION_BLOCKED / NO_EXTERNAL_EFFECT`  
> 基线：`AOS-000034`、`w2-workshop@0510a77b56442a6348f9f13c4da76f7e277f5f41`  
> 证据：`.evidence/workshop/2026-08-15-w8-09-slo-alert-unknown-reconcile-usage-runbook-preflight.json`

## 1. 决策

运营就绪不是“有 Dashboard 和告警”。W8-09 必须以同一 release、Bundle、Installation 和 canonical authority refs 形成可复算的 SLI/SLO、告警 Receipt、unknown/reconcile 队列、Usage 质量与演练过的 runbook。W5-08、W6-10、W7-11 未 GREEN，本轮只冻结合同，不编造数值目标或运行生产处置。

## 2. SLI/SLO

SLI 至少覆盖 view availability、freshness lag、P50/P95/P99、partial ratio、unknown ratio、unknown backlog/age、reconcile age、各轴 Receipt closure、Usage quality 与 Effect maturity。维度包含 module/view/command/adapter/provider/risk/tenant/release；缺 cutoff 或样本是 unknown，不是 0。

每个 SLO 声明 owner、population、eligibility、event clock、window、target、error budget 与 source revision。数值 target 只能由实测 baseline 与风险决策产生；之前保持 TBD/blocked。unknown、partial、forbidden、policy block、timeout 不能从分母消失。

## 3. 告警与对账

告警同时使用 burn rate 与绝对量；backlog 同时使用 count、oldest age、age buckets 与风险敞口。Alert/Ack/Silence/Escalation/Resolution 均是带 actor/reason/expiry/scope 的 append-only Receipt。解决必须 canonical reread 后确认指标回到策略内，不能由 ack 或页面消失推断。

unknown 从首次歧义边界计龄，并固定原 request fingerprint、账号、Adapter、Policy、Lease 与风险敞口。自动 reconcile 使用稳定 provider ref；manual reconcile 创建 typed maker-checker Case。restart、队列延迟与再次查询不重置 age；resolved 与 applied/failed/partial/refunded/disputed 分开。

Usage 按 measured/estimated/unknown/adjustment/refund/dispute/unattributed 与 currency 分桶；missing、duplicate、hash/currency drift 独立告警。Action、Usage、lineage、Effect、Handoff 五轴独立 closure，禁止压成单一 success。

## 4. Runbook 与演练

Runbook 包含 trigger/reasonCode、owner/severity、只读 authority/tenant 核验、containment、批准/Lease/幂等/stop condition、provider reread/reconcile、Usage/预算/谱系/Effect 守恒、rollback/roll-forward/compensation、恢复验证和事后 Receipt。

必须演练 mass unknown、provider timeout/rate/webhook gap、Action backlog/kill、Usage 缺失重复币种漂移、Stage lease/capacity、Installation drift、RLS/GUC、PII/share、Effect late data 与监控静默。定义文档只得 `RUNBOOK_DEFINED`；真实 drill EvidencePack 闭合后才可 operational ready。

## 5. 两轮审查与阻断

第一轮删除预设数值目标，补齐分母、event clock、风险/age backlog 和五轴 closure。第二轮补齐告警 Receipt、manual reconcile 职责分离、Usage 质量维度、监控静默与恢复验证。合同通过；因产品未封板、三项上游累计门、实测 baseline、运营投影和 drill EvidencePack 均缺失，实际 W8-09 保持未勾选。

## 6. 2026-08-26 串行实施复核与文件级清单

W5-08、W6-10、W7-11 的工程合同已经闭合，旧的“等待上游开发”原因不再成立。当前仍缺的是真实 baseline、批准后的数值目标、同 release 运营投影、append-only 告警 Receipt 与 drill EvidencePack；这些缺口应由失败关闭判定诚实暴露，不再阻止 W8-09 的工程实现。

本波采用最小、只读实现，不创建真实告警、Ack/Silence/Escalation/Resolution，不执行 reconcile、Provider 回读、业务写入或演练：

1. `apps/web/src/components/workshop/workshopOperatingReadiness.ts`：新增可复算运营就绪判定，校验 release/cutoff/source revision、SLI/SLO 完整性、unknown backlog 年龄连续性、Usage 分桶、五轴 closure、告警 Receipt 与 runbook/drill 证据；任何缺失均返回明确 blocker，unknown 不归零。
2. `apps/web/src/components/workshop/workshopOperatingReadiness.test.ts`：覆盖缺样本、缺 target、unknown 计龄未被重启重置、Ack 不等于 Resolution、五轴独立、Usage 数量/币种漂移与 drill 缺失等失败关闭路径，以及完整证据的纯计算 GREEN 路径。
3. `apps/web/src/components/workshop/WorkshopOperatingReadinessCard.tsx` 与测试：提供只读工作台贡献视图，按“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献”展示证据缺口；无权威输入时只显示 unknown/blocked，不渲染伪造百分比、0 backlog 或处置按钮。
4. `apps/web/src/components/workshop/TaskCockpitPage.tsx` 与现有测试：把运营就绪卡片挂入 Task Cockpit；当前正式 API 未提供 W8-09 同 release EvidencePack，因此默认诚实显示失败关闭，同时保留原任务、批次、派发与交接功能。
5. `.evidence/workshop/w8-09/`：记录专项测试、累计回归、生产构建、内置浏览器视口与无障碍验收摘要；不把工程 GREEN 写成 operational/release GREEN。

## 7. 验收与停止条件

- 专项必须证明缺 cutoff/样本/baseline/target/source revision/Receipt/drill 任一项时不能成为 ready；unknown quantity 不能为 0，restart/requery 时间不能覆盖首次歧义时间。
- Web 累计测试与生产构建不得回退；涉及页面必须用内置浏览器确认唯一主标题、只读失败关闭、无伪造指标、无处置入口和无横向溢出。
- 任一既有测试、浏览器入口或合同守恒失败，立即停止闭合，不更新 W8-09 完成状态。
- 本波最多签发 `ENGINEERING_OPERATING_CONTRACT_BROWSER_GREEN / REAL_BASELINE_AND_DRILLS_BLOCKED / NO_EXTERNAL_EFFECT / NO_RELEASE`；真实 operational ready 仍必须由批准目标、同版真实 EvidencePack 和演练闭合另行证明。

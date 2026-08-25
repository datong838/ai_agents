# W8-02 价格异常→运营 Case→客户补救同链预检 ADR

> 日期：2026-08-15
> 决策：`NOT_STARTED / SCENARIO_CONTRACT_APPROVED / HARD_GATE_BLOCKED / NO_EXTERNAL_EFFECT`
> 前置：产品正式封板；W2-10、W4-08、W5-08、W6-10 当前 release 全 GREEN；每类真实动作另有 exact 授权

## 1. 当前事实

价格、统一运营和客户技术方案已经明确 Observation/Match/PriceCase、OperationCase、CustomerLite/Consent/Journey/Batch 与 Action 边界，但领域 runtime 与正向页面链尚未实现。产品仍待正式审查封板；四个 W8-02 累计依赖未 GREEN。客户 P08 专项仍有 6 个失败，共享 canary 组合测试仍有 1 个失败；生产调价、消息、退款/补偿 Adapter 与真实授权均不存在。

因此本轮只冻结 E2E 合同；不使用 Mock 订单/客户、示例页面或测试 Adapter冒充真实补救。

## 2. 同链合同

exact `PriceCaseRevision` 是场景根，`remedyBindingHash` 覆盖：

1. PriceObservation/ComparisonSnapshot originals、cutoff、币种/单位/税费/运费/优惠口径；
2. ProductMatchObservation 与显式 MatchDecision；
3. MonitoringPolicy/Eval/Evidence 与异常 calculation hash；
4. 受影响 Order/OrderLine exact target set；
5. OperationCase/DecisionBrief/Evidence/Eval；
6. Customer Handoff、CustomerLite、Consent/Preference、purpose/retention/频控；
7. ContactExecutionPermit 与 protected contact resolver；
8. 价格、退款/补偿、消息三类 Proposal/Impact/Approval/Lease/Attempt/Receipt/reconcile；
9. EffectReview 与完整 lineage。

跨 Module 只传 scoped refs、purpose 和 requestedOutcome，禁止复制竞品原文、支付 payload、客户 PII、联系方式或成员列表。

## 3. 独立动作与守恒

- 低置信/不可比 Match 不得产生自动异常或调价；
- PriceCase 不授权调价、退款、补偿或消息；
- 三类动作分别审批、租约、幂等、Receipt 和补偿，互不借权；
- exact Order/Case/customer/purpose/action fingerprint 防止双补救与双通知；
- Consent 撤回与发送在同一线性化边界裁决，未获 Permit 不解析 contact；
- message accepted、refund submitted、price applied、Case resolved、Effect mature 是独立轴；
- unknown 保留频控和资金风险敞口，只能 reread/webhook/人工 Case/reconcile；
- 外部效果不以数据库回滚或覆盖 Receipt 撤销。

## 4. 验收门

负向至少覆盖：stale/not-comparable/wrong-currency/revoked originals、preliminary/conflicting Match、floor/margin/MAP/inventory/budget、target set 外或已补救订单、Consent unknown/withdraw race、frequency/retention/purpose/marking/k-anonymity/contact block、退款/消息 timeout/unknown/late/duplicate/partial、kill/account/capability/policy drift 和跨租户 ref。

正式正向只认 `org-org/dev-project`，`dev-org/dev-project` 只作隔离 canary。任何真实调价、触达、退款或补偿都必须有固定对象、账号、预算、时窗、停止条件的独立授权。

## 5. 两轮审查

### 第一轮：业务与隐私边界

- PriceCase→OperationCase→Customer 补救同链且只传最小 refs；
- 价格、资金、消息三动作独立，无批准级联；
- Consent/频控/contact 与订单防重在执行边界生效；
- unknown、partial、settlement 与客户结果不被压成单一成功。

结论：`PASS`。

### 第二轮：执行资格与高风险副作用

- 产品封板和四项依赖是硬门；
- P08/canary 测试红项不得清理数据或放宽 fail-closed 规避；
- Mock/fixture/test Adapter 不构成真实补救；
- 当前无价格、客户、资金或浏览器写入。

结论：`PASS_WITH_HARD_GATE_BLOCKED`。

## 6. 最终裁决

W8-02 场景合同可以作为未来施工与验收基线；当前不得运行或勾选。预检事实见 `.evidence/workshop/2026-08-15-w8-02-price-anomaly-operation-case-customer-remedy-preflight.json`。

## 7. 2026-08-26 串行施工更新（编码前方案）

### 7.1 基线复核与实施裁决

当前 authority 为 `AOS-000268`，W8-01 工程清单已闭合，Prime 强一致投影为 CURRENT。价格治理、OperationCase 与客户生命周期已有各自 authority/只读投影，但还没有一个可证明“同一 PriceCase 根、同一 cutoff、同一 binding”的跨 Module 贡献；现有 PriceCase、OperationCase、客户联系与 Action 命令不得被聚合页面自动调用。本波只新增 GET-only 场景贡献，并把缺失的真实订单集合、Consent/Permit、价格/资金/消息执行 Receipt 诚实标为 blocked。

### 7.2 163/164 分层与同链合同

- 原子 Skill：只声明价格观测/匹配、Case 编译、客户资格/Consent、Permit 评估、三动作 gate 和 EffectReview 所需的 canonical Skill refs；页面不复制 Skill 定义；
- Logic 编排：exact `PriceCaseRevision` 是唯一根，`remedyBindingHash` 覆盖九阶段 exact refs，不选择“最新 Case/客户/订单”补洞；
- 数字同事绑定：数据参谋主责判断与 Case，运营管家、客户运营专员只在 exact Binding/AgentRun 可验证时显示，名称本身不构成运行 authority；
- 工作台贡献：Price Governance v2 展示 PriceCase 根、九阶段、受影响对象/动作结果守恒，以及 repricing、refund/compensation、customer message、Case resolution、Effect maturity 五独立轴；写入口继续为 0。

跨域只传 tenant-bound exact refs、purpose、requested outcome 与计数。合同与 parser 必须拒绝 `mobile/openid/email/address/contactValue/paymentPayload/providerPayload` 等 PII/支付/Provider 正文键；CustomerLite、Consent、Permit 和 protected contact 只允许引用，不在贡献中展开。

### 7.3 文件级实施清单

后端：

1. 新增 `services/aos-api/aos_api/ecommerce_workshop_remedy_scenario_contracts.py`，冻结 `PriceCaseRevision` 根、九阶段、五结果轴、对象/动作守恒 ledger、blocker、最小披露与全部 false 命令；
2. 新增 `services/aos-api/aos_api/ecommerce_workshop_remedy_scenario.py`，定义 bounded canonical reader；缺根、跨租户/cutoff/binding、root-stage 漂移、数量不守恒或全 ready 运营伪状态均返回结构化 blocked，不制造订单、客户、Consent、Permit、Action 或 Receipt；
3. additive 扩展 `ecommerce_workshop_price_governance_contracts.py`、`ecommerce_workshop_price_governance.py` 与现有 GET router，使 Price Governance v2 携带 remedy scenario；v1 继续兼容；
4. 新增专项测试并扩展 Price Governance/Workshop API/OpenAPI 回归，覆盖币种/可比性、root-stage、跨租户/cutoff/binding、Consent/Permit 缺失、三动作独立、unknown/late/duplicate 与 PII 禁止字段。

前端：

1. additive 扩展 `apps/web/src/api/ecommerceWorkshop/contracts.ts` 与 `parser.ts`，严格解析九阶段、五结果轴和两份守恒账本，拒绝多余字段、PII 键、可执行命令和全 ready 伪状态；
2. 新增 parser 测试，扩展 `PriceGovernancePage.tsx` 与测试，展示“价格异常 → PriceCase → OperationCase → 客户补救”与“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献”，不新增调价、退款/补偿或发送按钮；
3. 更新 OpenAPI 生成物，执行专项、相邻、Web 全量、TypeScript/build/security，再用内置浏览器验证 1280/1440/1920、三 Tab 键盘、刷新与无写入口。

证据与记忆：形成独立 evidence、Delivery Receipt 和安全提交；完成后才串行 CAS 更新 authority、01/06 与 Prime，并自动进入 W8-03。

### 7.4 不变式与回滚

- 不 apply 共享迁移，不写 `org-org/dev-project`，不读取/解析 protected contact，不调用真实 Provider/Action/消息/退款/补偿/调价；
- PriceCase 不等于动作授权；message accepted、refund submitted、price applied、Case resolved、Effect mature 五轴不得互相推导；
- unknown/partial/late/duplicate 保留风险敞口，不通过重试或数据库回滚伪造成功；
- 回滚仅移除 Price Governance v2 的 remedy scenario 字段和 UI，v1 三视图、价格调研、处分分门与 W8-01 保持不变。

## 8. 2026-08-26 工程实现与验收结论

W8-02 已完成 GET-only Price Governance v2 同链贡献。新增严格 `RemedyScenarioContribution`：exact `PriceCaseRevision` 与 `price_case` 阶段必须完全一致，固定九阶段顺序，并把调价应用、退款/补偿提交、客户消息接受、OperationCase 解决、Effect 成熟保持为五个独立结果轴。缺根、租户/cutoff/binding/root-stage 漂移、数量不守恒、PII/支付/Provider 正文键、任何命令开放或全 ready 运营伪状态均失败关闭；v1 三视图仍保持兼容。

专项后端 Price/Scenario/API/OpenAPI `33 passed`，Web 定向 `3 files / 12 tests`，Web 全量 `237 files / 2161 tests`，TypeScript 与生产 build `344 modules transformed`，OpenAPI 为 `2666 paths / 2407 schemas` 且 deterministic check 通过，安全 scanner `9 tests`、scoped `16 files / 0 critical / 0 warning`。内置浏览器在实际 `1280x720` 视口确认九阶段、五轴、三 Tab、方向键切换与 aria-selected、受保护联系正文未解析及零业务写按钮；未把该证据误标成未实际取得的 1440/1920 截图。

浏览器 fixture 准备期间曾误启动完整本地 `aos-api` 约 12 秒；观察到既有 JDBC SSH tunnel 启动，发现后立即终止，shutdown 日志确认 tunnel cache 已清理。期间没有调用 W8-02 业务 endpoint，也没有执行调价、退款/补偿、客户消息、Case 关闭、发布或 release；但由于启动日志包含幂等 schema/seed 检查，本 ADR 不把该次完整 runtime 启动当作“已证明零 bootstrap 写”的证据。正式浏览器验收已改用纯 loopback GET-only fixture 重跑，后续禁止为页面验收启动完整 runtime。

代码提交 `55306606`；证据包为 `.evidence/workshop/2026-08-26-w8-02-price-remedy-scenario.json`，浏览器图为 `.evidence/workshop/2026-08-26-w8-02-browser/price-remedy-scenario-viewport.png`。工程退出裁决：`W8_02_PRICE_REMEDY_EXACT_BINDING_CODE_CONTRACT_BROWSER_GREEN_SECURITY_SCOPED_GREEN_OPERATIONAL_FAIL_CLOSED_NO_RELEASE`。这只关闭 W8-02 工程清单，不签发真实 PriceCase、订单集合、Consent/Permit、Provider/Action、外部效果或 release；下一串行入口为 W8-03。

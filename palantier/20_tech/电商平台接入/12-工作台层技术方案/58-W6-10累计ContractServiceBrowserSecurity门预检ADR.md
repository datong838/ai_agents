# W6-10 累计 Contract、Service、Browser、Security 门预检 ADR

> 日期：2026-08-14
> Authority：`AOS-000029`
> 代码基线：`w2-workshop@4151aeda5a26e7568eefd48d6fb473075c486126`
> 证据：`.evidence/workshop/2026-08-14-w6-10-cumulative-contract-service-browser-security-preflight.json`
> 结论：`TARGET_CONTRACT_REVIEWED / IMPLEMENTATION_BLOCKED / NO_EXTERNAL_EFFECT`

## 1. 审查结论

W6-01～09 均已有实时预检与收敛后的目标契约，但九项实现均未 GREEN，因此 W6-10 不能进入累计签发。通用 ResearchJob、Production Contract、Action、Handoff、Usage 和 Workshop Shell 是可复用底座；它们不构成达人、价格、客户三领域的 runtime authority、服务闭环、正向浏览器或领域安全证明。

本轮前端累计 15 文件/59 项通过；后端在 30 项通过后遇到共享 canary 隔离失败，`dev-org/dev-project` 保留两条 ResponsibilityPlan，未执行清理。内置浏览器到达 `/workshop/customer`，页面诚实显示离线、API health 500 和目录读取失败；这证明失败关闭，不证明客户工作台正向可用。

## 2. 累计门裁决

| 子门 | 必须消费的事实 | 当前状态 |
|---|---|---|
| Contract | W6-01～09 Receipt；同一 release/bundle；三领域 authority、item algebra、Usage/Effect/Handoff runtime；OpenAPI/SDK strict | `BLOCKED`：领域 runtime 为 0，Bundle/readiness 仍红 |
| Service | prepare 0 副作用、显式 start、durable item attempt、partial/unknown/reconcile、Usage/Effect/Handoff 可重建 | `BLOCKED`：仅通用 primitive GREEN |
| Browser | 三 Module 已安装；正向链、刷新、三视口、键盘、七态、network/console、canary 负向 | `BLOCKED`：仅 Shell/API 500/目录失败路径可见 |
| Security | 领域 RLS/无 scope/跨租户、PII、ProtectedContact、Consent race、频控、spoof/replay、Lease/补偿 | `BLOCKED`：领域合同与负向测试未实现 |
| Operational | 真实 Provider/账号/样本/效果成熟窗口与外部动作专项 GREEN | `BLOCKED`：W5/W6 前置未满足 |

## 3. 不可伪绿规则

1. W6-01～09 任一未有当前 revision/hash 的 Delivery Receipt，W6-10 直接失败；
2. 通用底座测试数不能替代领域合同、服务或安全测试；
3. 离线页、API 500、静态 fixture、视觉稿或 disabled 控件只能证明失败态；
4. 不删除 `dev-org/dev-project` 留存数据以满足空库断言，必须让测试拥有独立 scope/fixture；
5. item outcome、Action outcome、Usage settlement、Effect maturity、Handoff decision 五轴独立，unknown/immature/pending 不计成功；
6. `EffectReviewRef`、Schema、目录 definition 或 generic Handoff consume 不等于 runtime EffectReview、业务决定或闭环；
7. 浏览器需真实 HTTP 与正式服务正向回包，且 `org-org/dev-project` 是唯一真实目标，`dev-org/dev-project` 只作负向 canary；
8. 累计签发只由可回读 EvidencePack/Receipt 触发，不由计划、commit、页面标题或 Goal 标签触发。

## 4. 阻断与解除条件

| ID | 当前事实 | 解除条件 |
|---|---|---|
| `DEP-W6-10-UPSTREAM-NOT-GREEN` | W6-01～09 全未勾选 | 九项依次实现、复审并签发 Receipt |
| `DEP-W6-10-CONTRACT-COVERAGE` | 三领域 runtime authority 缺失 | contracts/store/API/RLS/OpenAPI/SDK 全 GREEN |
| `DEP-W6-10-SERVICE-COVERAGE` | 无三领域 prepare/start/reconcile 闭环 | service + durable attempt + reducer + readback GREEN |
| `DEP-W6-10-BACKEND-ISOLATION-RED` | canary 留存两条 Plan 使测试失败 | 独立 fixture/scope，不清真实或共享数据，累计复跑 GREEN |
| `DEP-W6-10-CUSTOMER-PIPELINE-RED` | CustomerLite/P08 为 27 passed/6 failed | JDBC mock 与 source_id fail-closed 契约对齐后 GREEN |
| `DEP-W6-10-CAPABILITY-READINESS-RED` | 1.3.0 Bundle 与 1.2.0 publisher 不一致 | publisher/manifest/exact readback/current install GREEN |
| `DEP-W6-10-BROWSER-POSITIVE-PATH-BLOCKED` | API 500、目录失败 | 正式 API 正向回包与三 Module 全流程 evidence |
| `DEP-W6-10-BROWSER-NAVIGATION-NOT-INSTALLED` | 安装目录失败关闭 | active installation、唯一导航/route/focus 与三视口 GREEN |
| `DEP-W6-10-DOMAIN-SECURITY-NOT-PROVEN` | 只有 generic 安全基础 | 三领域安全矩阵与负向测试 GREEN |
| `DEP-W6-10-EFFECT-AND-USAGE-CLOSURE` | 无三领域自动绑定/成熟闭环 | Usage/EffectReview/Handoff business Receipt 全 GREEN |

## 5. 双轮审查记录

### 第一轮：依赖和证据真实性

- PASS：九项未实现状态没有被通用底座测试掩盖；
- PASS：浏览器失败关闭与正向能力严格分开；
- PASS：共享 canary 留存数据未被删除；
- 整改：原清单只有“累计门”一句话，缺少子门、证据消费、五轴状态与不可伪绿条件，已补齐。

### 第二轮：安全与可施工性

- PASS：Contract、Service、Browser、Security、Operational 五门可分别失败和回读；
- PASS：每项阻断具有稳定 ID 和解除条件，可直接转成后续实现/测试任务；
- PASS：当前没有代码、迁移、真实租户或外部渠道副作用；
- PASS：W6-10 保持未勾选，结论与证据、方案和 D-waves 一致。

## 6. 复审结论

W6-10 的目标产品/技术契约通过两轮文档复审，当前实现门未通过。安全施工顺序仍是 W6-01→02，随后达人/价格/客户的 read/prepare 可按无冲突范围推进，三领域 start/action 在对应 W5 capability GREEN 后串行开闸，再完成 W6-09，最后才运行 W6-10 累计签发。任何旧 Goal `blocked` 标记只作线索；是否继续施工以实时 authority、Lease、Receipt、Git、测试与依赖事实决定。

## 7. 2026-08-25 实时复审与 W6-10 施工清单

### 7.1 旧阻断事实对账

- Authority 已推进到 `AOS-000253`，W6-01～W6-09 均已有独立 Delivery Receipt、固定代码提交与 EvidencePack；第 4 节的 `DEP-W6-10-UPSTREAM-NOT-GREEN` 不再成立。
- W6-03～W6-09 已分别补齐达人、价格、客户三领域的 typed authority、prepare/start/reconcile、Usage/Effect/Handoff 五轴和 163/164 的“原子 Skill → Logic → 数字同事 → 工作台贡献”消费视图。
- 2026-08-14 的 `30 passed / 1 shared-canary isolation failed`、CustomerLite 6 failures、API 500 与未安装导航均是历史预检事实，不能继续当作当前阻断，也不能直接视作已解除；本波必须以当前固定提交重新运行。
- W6-10 只签发代码、合同、服务、浏览器和安全累计门。真实 Provider、ProtectedContact 解析、发送、Handoff consume、迁移 apply、Canary、外部 Effect、Memory promotion 与 release 仍是独立运营门，不由本波制造。

### 7.2 文件级施工范围

1. 合同/服务：复跑 W6-01～W6-09 DTO、Store、Router、OpenAPI 与 CustomerLite/P08/JDBC 邻接测试；如失败，仅在对应唯一 authority 文件做最小整改。
2. 安全：复跑无 Principal、跨租户、RLS、PII/ProtectedContact、Consent/频控、version/hash、replay/idempotency、partial/unknown/reconcile 与 Handoff/Usage/Effect 分轴断言。
3. 浏览器：使用正式前端与受控 canonical HTTP fixture 验收达人、价格、客户三页；覆盖 1280/1440/1920、键盘、七态、五轴、163/164 贡献链、零动作入口、network/console。fixture 只证明代码/交互，不冒充真实业务运行。
4. 确定性：复跑 TypeScript、production build、OpenAPI 双进程计数、Alembic single head、diff/security scan，并产出 `.evidence/workshop/2026-08-25-w6-10-cumulative-contract-service-browser-security.json`。
5. 交付：只有所有当前门 GREEN 后才更新 D-waves、写 Delivery Receipt、推进 authority/Prime；否则按具体失败项保持 W6-10 未勾选。

### 7.3 当前裁决

`AUTHORIZED_FOR_CUMULATIVE_VERIFICATION / OPERATIONAL_EXTERNAL_EFFECT_GATE_RETAINED / NO_RELEASE`

## 8. 2026-08-25 累计门封板

### 8.1 唯一整改

累计路由门发现 `domain_manifest.json` 漏登记已经处于 runtime 聚合中的 `aip_action_canary` 与 `aip_action_webhooks`。整改仅把两组现有安全路由登记到 `aip_actions` 后并顺延 manifest ordinal；没有新增 API、业务逻辑、数据库写或外部副作用。生成聚合与 OpenAPI inventory 保持当前发布顺序和内容不漂移。

### 8.2 当前证据

- 后端 W6-01～09 与 API/OpenAPI/Router 合并复跑 `103 passed / 2 subtests passed`；其中 W6 专项累计 `76 passed`，Router/API/OpenAPI `27 passed / 2 subtests passed`。
- Web 全量 `232 files / 2130 tests passed`；TypeScript 与 production build `344 modules` GREEN。
- Router manifest `541 entries`，runtime `4422 routes`，OpenAPI `2639 paths / 2307 schemas / 4418 route rows / 4408 unique operations`；双进程 deterministic check GREEN。
- Alembic 唯一 head `w6_009`；Python compile、diff check GREEN。仓库 security gate scanner tests GREEN；W6/manifest/Workshop UI/Web build 定向扫描 `239 files / critical=0 / warning=16`。
- 内置浏览器以受控 canonical fixture 验收达人、价格、客户三页 × 1280/1440/1920：九格均无横向溢出，原子 Skill→Logic→数字同事→工作台贡献和五轴均可见，禁用动作按钮为 0，console error 为 0；skip link 为可聚焦 `#ecommerce-workshop-main` 锚点。

### 8.3 边界与结论

fixture 只证明当前代码、合同和交互，不证明真实业务数据或运营可用。迁移 apply、Provider、ProtectedContact、发送、真实业务 mutation、Handoff consume、Canary、外部 Effect、Memory promotion 与 release 均为 0，仍需后续独立门。

代码提交：`aos-platform/m1@7388a8cf`；证据：`.evidence/workshop/2026-08-25-w6-10-cumulative-contract-service-browser-security.json`。

结论：`CUMULATIVE_CODE_CONTRACT_SERVICE_BROWSER_SECURITY_GREEN / OPERATIONAL_EXTERNAL_EFFECT_GATE_RETAINED / NO_RELEASE`。

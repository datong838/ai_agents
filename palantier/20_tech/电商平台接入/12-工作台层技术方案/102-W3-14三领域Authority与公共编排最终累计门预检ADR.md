# W3-14 三领域 Authority 与公共编排最终累计门预检 ADR

> 日期：2026-08-15
> 状态：`CUMULATIVE_CODE_BROWSER_GREEN / NO_RELEASE / NO_EXTERNAL_EFFECT`
> 实施基线：`AOS-000225`、`m1@99716c5`
> 证据：`.evidence/workshop/2026-08-25-w3-14-three-domain-cumulative.json`

## 1. 决策

W3-14 不是第四套领域实现，也不是把 W3-10～W3-13 的四张绿灯截图相加。它是 W3 的最终 fail-closed 累计门：公共生产编排、内容/活动、统一运营、经营参谋必须在**同一不可变 release identity** 上形成一个可复核 EvidencePack，才能 GREEN。

当前 W3-10～W3-13 runtime 全部 `NOT_STARTED`。四项预检和方案整改已经闭合，但方案、Receipt、单测、静态视觉稿、Mock、blocked-only 页面或未来投影都不是运行时证据，因此 W3-14 保持 RED，不编码、不勾选。

## 2. 同一 Release Identity

EvidencePack 必须同时固定 Git commit、应用 release、schema/migration 或 no-migration proof、OpenAPI、strict SDK、SolutionPack/Bundle artifact、active installation lock、八 Module route/navigation/component revision、`org-org/dev-project` evidence cutoff 与 Delivery Receipt 集合。任一轴来自不同 release、已漂移、unknown 或仅是 eventual projection，累计门失败。

## 3. 七轴累计矩阵

| 轴 | 必须闭合的事实 |
|---|---|
| Contract | 公共编排与三领域合同 exact、兼容、无第二真源 |
| Store | authority row、RLS、CAS、幂等、lineage、重启回读与投影重建 |
| API / strict SDK | canonical operation、稳定错误、严格 DTO、拒绝未知字段/枚举 |
| Web | 八 Module 只用唯一公共生产组件包，展示真实 lifecycle/readiness/blocked/unknown |
| Browser | 正式 HTTP、1280/1440/1920、键盘/焦点、console/network、刷新恢复 |
| Security / Tenant | `org-org/dev-project` 正向、`dev-org/dev-project` 负向、最小披露、跨租户 0 泄漏 |
| Recovery / Replay | 重复/乱序、partial failure、unknown outcome、restart/rebuild、successor correction |

七轴必须在同一 EvidencePack 同时 GREEN；不能用一个领域的成功替代另一个领域，也不能用负向阻断页替代正向业务链路。

## 4. 跨领域所有权与恢复

- Campaign、OperationCase、GrowthPlan 等仍由各自领域 authority 拥有；公共层只拥有 canonical Task/Handoff/Action/Approval/Receipt，不得复制。
- 跨领域协调通过 exact refs、Task/Handoff/Action 与 Receipt 完成，不构造隐藏的分布式事务或“万能 Workflow 真源”。
- 部分成功、提供方 unknown、用户拒绝、kill、撤销或超时必须作为可见状态保留并进入 reconcile；重试不得抹掉既有 Attempt/Receipt。
- 内容排期、运营 Case、计划 TaskGraph 的 predecessor/successor 与 originals 必须持续可达；投影重建不改变 authority 数量与历史。

## 5. 通过与失败规则

通过条件：W3-10、W3-11、W3-12、W3-13 均在同一 release runtime GREEN，七轴矩阵全部 GREEN，并有 `org-org/dev-project` 正向与 `dev-org/dev-project` 隔离负向证据。

失败条件：任一依赖未开始、只完成方案、跨 release 拼接、缺少正向、仅有 synthetic canary、出现 stale/unknown 未解释、第二真源、跨租户可见或恢复后数量/lineage 不守恒，均保持 `CUMULATIVE_GATE_RED`。

## 6. 两轮审查

第一轮发现原 W3-14 只有“三领域 authority + 公共编排共同 EvidencePack”一句，无法阻止从不同 release 拼装假绿。整改后冻结同一 release identity 与 Contract、Store、API/SDK、Web、Browser、Security/Tenant、Recovery/Replay 七轴。

第二轮发现原验收没有规定跨领域部分失败、unknown、重放、重启重建和第二真源负向。整改后冻结 exact-ref 协调、无隐藏分布式事务、partial/unknown 可见、successor/originals 可达与数量守恒。方案复审通过；runtime 仍 RED。

## 7. 2026-08-25 执行方案与文件级清单

### 7.1 当前事实与验收口径

- 当前 authority 为 `AOS-000225`，W3-10～W3-13 已分别形成代码、专项/累计测试、内置浏览器、Evidence 与 Delivery Receipt；W3-14 不新增第四套 authority。
- 本累计门重新在当前 `m1` 单一 HEAD 运行全套验证并生成一个新的不可变 EvidencePack，不把四个历史 cutoff 的测试数字拼成同版 GREEN。
- 本地正式 HTTP、数据库测试事务与浏览器可以证明 code/browser/security/recovery 控制面；没有执行 release、live migration 或真实外部副作用，因此通过状态只能是 `CUMULATIVE_CODE_BROWSER_GREEN / NO_RELEASE`，不得写成 production runtime/release GREEN。
- S3 实现门闭合后自动进入 S4 W4-02；发布与真实运行门继续独立失败关闭。

### 7.2 本波最小文件清单

- `services/aos-api/aos_api/ecommerce_w3_cumulative_gate.py`：七轴累计门执行器；强制同一 release identity、W3-10～W3-13 四张 exact Receipt、`org-org/dev-project` 正向与 `dev-org/dev-project` 隔离角色、非空 evidence refs，并把未发布状态明确归类为 code/browser GREEN 而非 runtime GREEN。
- `services/aos-api/tests/test_w3_three_domain_cumulative_gate.py`：以当前源码为输入，校验公共编排、Campaign、OperationCase、Analyst authority 的唯一所有权、strict contract、RLS/CAS/append-only、exact refs、unknown/partial/replay/correction 边界，并拒绝第二真源。
- `.evidence/workshop/2026-08-25-w3-14-three-domain-cumulative.json`：固定 Git HEAD、schema/OpenAPI/Web build/migration head/hash、四项 Delivery Receipt、七轴同版结果、租户正负向、恢复重放与浏览器证据。
- 本 ADR 与 `D-waves/00-工作台长任务开发计划总清单.md`：记录实施结论和下一波路由。
- Delivery Receipt、authority/01/06/投影：仅在专项、累计、浏览器、方案一致性全部闭合后由 CAS 推进并同步 Prime。

### 7.3 执行顺序与失败关闭

先增加累计门测试并确认它能捕获缺模块、第二真源、迁移 head 漂移和跨租户泄漏，再运行 W3 后端全量、Web 全量、TypeScript、production build、OpenAPI deterministic/contract、compileall、Alembic 单 head。最后用内置浏览器在 `org-org/dev-project` 依次复验内容、运营、经营参谋与公共编排贡献视图的 1280/1440/1920 视口、刷新恢复、键盘焦点、console/network；负租户只通过自动化隔离测试验证，不把 `dev-org/dev-project` 当正向业务租户。

任一轴失败则 W3-14 保持 RED，且不得通过发布、迁移、冲洗离线队列、真实 Task/Action/Handoff 或业务写来“补证据”。

## 8. 2026-08-25 实施结论

- 新增 W3 同版累计门执行器，固定七轴、四张 exact Delivery Receipt、单 release identity、四个互不重叠 authority owner 与正负租户角色；缺轴、跨版本、UNKNOWN、缺 Receipt、第二真源、外部副作用、partial release 和无授权 runtime 声明全部失败关闭。
- 当前 EvidencePack 固定代码 `99716c56e9d3741cb2a4d12f267113b9792a4eb2`，并记录 schema/OpenAPI/SDK/Web build/Bundle/route hashes 与 migration head `w3_018`；W3-10～W3-13 的实现 commit 均已验证为该 HEAD 的祖先，未把历史测试数字当作当前同版结果。
- 验证通过：累计门专项 `9 passed`、W3 当前 HEAD 后端累计 `133 passed`、Web 全量 `775 suites / 2084 tests`、TypeScript、Vite build、compileall、OpenAPI deterministic/contract `13 passed`、Alembic 单 head 与 diff-check。
- 内置浏览器在内容与活动、日常总控、统一运营、经营参谋四页面完成 1280×720、1440×900、1920×1080 同标签复验；body/main 无横向溢出，刷新后标题恢复，菜单焦点轮廓可见，console error 为 0。既有待同步写入 `1` 未冲洗，浏览器写操作为 0。
- 当前页面仍报告 SourceReadiness failed/stale，Campaign、OperationCase、Analyst 正向 authority reader 仍 blocked/unknown；这是当前运行事实。因此本波只闭合 S3 的实现与失败关闭累计门，不宣称 production runtime、release、live migration 或业务运行 GREEN。

结论：W3-14 达到 `CUMULATIVE_CODE_BROWSER_GREEN / NO_RELEASE / NO_EXTERNAL_EFFECT`，S3 开发验收完成；允许自动进入 S4 W4-02，所有 operational/release 门继续独立失败关闭。

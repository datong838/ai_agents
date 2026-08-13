# 03 AIP 智能体、Skill Registry 与 Handoff 开发清单

> 状态：**v1.2 · A6D IMPLEMENTED_GREEN / A6E 前置 W0A 待执行**
> 上位依据：`../03-228-AIP智能体SkillRegistry与Handoff实施方案.md`
> 对应阶段：AIP-6；前置：02、04、05 公共契约 GREEN。

## 1. 工作包

| ID | 任务 | 主要文件边界 | 验收 |
|---|---|---|---|
| 03-01 | 冻结 Template/Instance/Skill/Binding/Run/Handoff DTO | contracts/OpenAPI | 只使用 `HandoffEnvelope` |
| 03-02 | 建 Registry 表、组织实例/工作区运行表、RLS/FK | migration/store | 模板共享、实例隔离、运行双 scope |
| 03-03 | 实现 AgentTemplate/SkillTemplate 不可变版本发布 | registry store | publish 后不可原地改写 |
| 03-04 | 实现组织 AgentInstance 与 Overlay allowlist | instance service | 两组织定制互不影响 |
| 03-05 | 实现 CapabilityBinding secretRef/health/quota/network | binding service | 无明文凭据，撤权阻止新 Run |
| 03-06 | 实现 SkillBinding 与 exact revision 解析 | skill registry | Run 可追溯全部版本 |
| 03-07 | 实现 SkillScan 确定性扫描与 ScanArtifact | import service | 扫描异常失败关闭，不执行 Skill |
| 03-08 | 实现 ImportJob parse/license/SBOM/probe/eval/approval/receipt | import router | 页面不预填成功结果 |
| 03-09 | 实现 Handoff 最小披露、expiry、一次性授权 | handoff service | 跨租户/过期/超字段拒绝 |
| 03-10 | 注册六数字同事模板与首批只读 Skill | solution pack | 不复制六套代码；无静态冒充 |
| 03-11 | 实现 revoke/deprecate/suspend/uninstall | lifecycle service | 阻止新 Run，历史仍可解析 |
| 03-12 | 迁移/关闭 singleton 与 `MOCK_AGENTS` | engine/pages | API 空即真实空态 |
| 03-13 | 建立六角色、37 Logic 的唯一版本化目录 | `solution.ecommerce.growth` manifest | D6+C8+G6+S6+P5+A6=37，禁止第二目录 |
| 03-14 | 为 37 Logic 冻结 input/output Schema、Tool allowlist、risk 和 required capabilities | SkillTemplate metadata | 缺工具/数据/权限时为 blocked，不 fallback |
| 03-15 | 建立旧 35 Skill 到 37 Logic 的 alias/crosswalk | compatibility manifest/ADR | 历史引用可解析但不产生重复 SkillTemplate |
| 03-16 | 为每条 Logic 绑定 EvalPack、Memory policy、Handoff policy 和 EffectReview schema | binding manifests | 37/37 均能追溯 exact revision |
| 03-17 | 注册内容总监与专业 Agent 团队的职责模板 | solution pack | Coordinator 不直接调用专业媒体/发布工具 |
| 03-18 | 建立能力成熟度与发布状态 | registry/release | draft/eval_passed/published/suspended/deprecated 可回读 |

### 1.1 电商域 37 Logic 唯一目录

| 角色 | Logic ID | 数量 | 权威能力范围 |
|---|---|---:|---|
| 数据参谋 | D01～D06 | 6 | 健康、研究、计划、拆解、监控、归因 |
| 内容官 | C01～C08 | 8 | 机会、策略、文案、短视频、平台适配、审核、线索、归因 |
| 导购顾问 | G01～G06 | 6 | 诊断、检索推荐、属性解释、对比、异议、成交 Handoff |
| 客服专员 | S01～S06 | 6 | 意图、订单、物流、售后、投诉、反馈 |
| 私域管家 | P01～P05 | 5 | 身份、标签、排期、复购、关系反馈 |
| 活动策划师 | A01～A06 | 6 | 机会、机制、预算、编排、止损、复盘 |

目录只声明能力和依赖；业务实现、页面和真实闭环由 11-G0～G6 分波交付。

## 2. 页面工作包

- Agent Registry：真实列表、版本、来源、许可证、安装/撤销状态。
- Agent List：实例、绑定、预算、健康、暂停/删除回执。
- Agent/Capability Import：异步 Job 时间线、扫描/探测/Eval 证据、失败/取消/部分成功。
- Studio：只允许选择真实 AgentInstance/Skill/ModelRoute；未满足门禁明确禁用。
- Logic Catalog：按角色查看 37 条 Logic 的版本、Schema、工具、风险、Eval、成熟度和 blocked 原因。
- Agent Team：展示内容总监/专业 Agent 等职责关系；页面不得暗示未发布 Skill 已可执行。

## 3. 测试与退出门

- [x] A6B/A6C 已验证模板在两组织形成隔离实例，一方不可读取另一方。
- [ ] SkillScan 覆盖恶意脚本、越权文件、网络、secret、提示注入、许可证和扫描器错误。
- [x] A6D 已验证 Handoff 只传 refs/白名单字段；一次性 token 仅首发返回、库内只存 hash，接收方按当前 exact identity 与权限重新授权解析。
- [ ] C1/C2 具备真实 submit/status/artifact 或 open/push/close 回执。
- [ ] API/UI 无静态 fallback；卸载、revoke、凭据失效与活动 Run 状态一致。
- [ ] 37/37 Logic 只有一个 canonical ID；旧 35 Skill 引用通过 alias 解析，不重复注册。
- [ ] 每条 Logic 均绑定正向、缺字段、越权、下游失败和提示词注入 EvalPack。
- [ ] 内容总监只编排；策略、脚本、标题、配音、合成、审核、直播、平台适配、复盘职责可独立授权和撤销。

## 4. A6D 实施封板（2026-08-13）

- 代码 `aos-platform/m1@650981c`：`aip6_003`、CapabilityBinding、AgentRun、Handoff authority。
- AgentRun 固化 canonical Task/TaskRun/Plan exact revision、AgentInstance exact ref 与不可变 Overlay 快照、SkillBinding 和已发布 Logic exact hash；当前 AIP-7 尚无版本化 ModelRouteRevision/PolicyRevision 真源，因此允许创建 `queued`，进入 `running` 诚实失败关闭。
- Handoff 固化 Task/TaskRun 与 sender/receiver exact refs；最小披露、expiry、revoke、重复消费、错误 token、receiver drift 和跨租户均失败关闭。有 object/artifact/evidence refs 而未装配接收方当前权限解析器时拒绝消费。
- 28 项 A6A～A6D 累计定向测试、compileall、迁移降升级、真实 Logic publication exact 查询、唯一 `aip6_003 (head)` 和 `git diff --check` 均 GREEN。
- A6D 未注册 HTTP 路由、未切换旧 singleton、未创建领域六角色或真实 Provider；这些仍归 A6E/A6F 与 AIP-7。

下一安全步骤：先执行 W0A 十 capability catalog/alias/crosswalk 文档门，再进入 A6E 六角色/37 Logic/职责模板领域包；不得跳过 W0A 直接硬编码名称。

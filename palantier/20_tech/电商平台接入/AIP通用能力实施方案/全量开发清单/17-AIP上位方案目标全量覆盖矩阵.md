# 17 AIP 上位方案目标全量覆盖矩阵

> 状态：**v1.2 · 38 份历史基线 + W0A delta 统一复审通过**
> 审计日期：2026-08-11
> 目的：证明 38 份上位方案中的目标均已进入明确清单、延期项或冲突裁决，不再用“主题已提及”代替“任务已覆盖”。

> 2026-08-13 增量：38 份是 2026-08-11 历史基线。229、工作台产品 v3、产品吸收矩阵、技术 22/23 和正式开发清单的新增目标由 `../18-AIP-W0A十类共享专业Capability目录别名与六角色职责Crosswalk.md` 的 DS-01～DS-06 承接；当前“全量覆盖”结论必须同时引用两份矩阵。

## 1. Rules 与权威顺序

1. 后续开发只使用 `m1` 单分支，由一个执行者串行推进；不创建 w1～w4、worker branch 或 worker worktree。
2. 本文件只补清单，不授权修改 `aos-platform`。
3. 运行事实/Receipt → 当前代码与契约 → 已冻结 228 母方案 → 平台专项方案 → 旧设计稿，依次作为冲突裁决顺序。
4. AIP 通用底座进入平台；电商 37 Logic、CustomerLite、增长对象进入 `solution.ecommerce.growth`；平台协议和字段进入 PlatformAdapterPack；栖月汇配置进入 InstanceOverlay。
5. “已映射”必须同时具有任务 ID、前置、实现边界、测试/浏览器验收和 EvidencePack；只有关键词或章节引用不算覆盖。
6. 具体平台 API、发布、私信、投流、改价、退款和直播开播，在官方能力、账号权限和专项安全评审前保持 `DEFERRED/BLOCKED`。

## 2. 审计范围（38 份）

| 来源组 | 文件数 | 目标范围 | 承接清单 |
|---|---:|---|---|
| `11-AIP决策引擎升级方案/` | 13 | Plan/TAOR、六角色技能、权限、协作、Evals、DeerFlow | 02～07、09、11～13 |
| `13-FDE技能编排方案/` | 6 | 六步 Skill Chain、Checkpoint、权限、26 Reflection、平台适配 | 10、12 |
| `14-行业Wiki基础设施方案/` | 6 | 三层运行记忆、七条知识管道、治理、美妆冷启动 | 06、12 |
| `内容官-*` | 4 | 短视频、数字人直播、四平台 Harness、成本治理 | 08、09、12 |
| `228-电商增长参谋长*` | 9 | G0～G6、37 Logic、CustomerLite、协同记忆、Connector/Action | 03～11、12 |

文件级登记如下，新增或改名必须同步更新本表：

- 11：`00`、`01`、`02`、`03`、`04`、`05`、`06`、`07`、`08`、`10`、`11`、DeerFlow 方案及其评审封板记录。
- 13：`00`、`01`、`02`、`03`、`04`、`10`。
- 14：`00`、`01`、`02`、`03`、`04`、`10`。
- 内容官：短视频、交互式数字人直播、平台专属 Harness、直播成本备忘。
- 增长参谋长：母方案、索引/路线图、G0、G1、G2、G3、G4、G5、G6。

## 3. 能力目标覆盖矩阵

| 目标域 | 权威目标 | 清单任务 | 状态/裁决 | 完成证据 |
|---|---|---|---|---|
| Plan/TAOR | Task/Plan/Run、Think/Act/Observe/Reflect、Verification、Checkpoint | 02 | REQUIRED | 状态机、API、重启恢复、timeline、失败/暂停/恢复浏览器证据 |
| Agent Registry | Template/Instance/Binding/Capability/Handoff | 03-01～03-12 | REQUIRED | 双租户实例、exact revision、最小披露、生命周期 Receipt |
| 37 Logic 目录 | D01～D06、C01～C08、G01～G06、S01～S06、P01～P05、A01～A06 | 03-13～03-18、11-L0～L6 | REQUIRED | 37/37 manifest、Schema、allowlist、EvalPack、Run/Handoff/EffectReview |
| 六层安全/Action | marking、purpose、risk、审批、Lease、Receipt、补偿 | 04、11-G6 | REQUIRED | 未批准、越权、重放、超时、unknown/reconcile 负向证据 |
| Evals/发布 | 单项 Eval、组合 Eval、发布门、回归、谱系 | 05、11-L0/各 Logic | REQUIRED | 37 Logic 正向/边界/缺字段/越权/下游失败/注入矩阵 |
| 三层运行记忆 | Working/Episodic/Semantic | 06-01～06-07 | REQUIRED | 隔离、TTL、晋升、撤回、引用、新鲜度、索引重建 |
| Procedural | 版本化 Skill/Logic/Policy/Playbook，不建第四运行库 | 06-01、12 ADR | REQUIRED | ADR、发布门、版本与回滚；无第四套 Memory store |
| 七条知识管道 | 种子、自学习、网络、竞品、专业库、客户反哺、人工经验 | 06-08～06-18 | REQUIRED | 七管道独立 Schedule/Run/Receipt/status/治理结果 |
| 美妆冷启动 | ≥300 知识、≥200 成分、≥50 话术、≥30 平台规则、Top-1≥80% | 06-19～06-21 | REQUIRED | 种子 manifest、许可证/来源、50 条标注集、六角色覆盖 100% |
| 助手/分析师 | Knowledge/Metric/Semantic Query、Plan、Draft、工作台 | 07 | REQUIRED | 真实查询、来源/时间窗、七态页面、无任意 SQL/示例 fallback |
| 内容官通用链 | 策略、文案、标题、审核、归因 | 08-C0/C1、11-C01～C08 | REQUIRED | 真实商品引用、ContentBrief/Variant、审核、线索和 EffectReview |
| 离线短视频 | 脚本→TTS/字幕/BGM→FFmpeg，30～60 秒 | 08-V0～V3 | REQUIRED | mp4/manifest/hash/license/质量门/失败恢复 |
| 数字人直播 | 5 Agent、控制/智能/引擎三层、L0～L5 | 08-L0～L5 | L0～L3 REQUIRED；L4/L5 条件开放 | 沙箱 5 分钟演示、延迟/接管/安全；真实平台直播需专项授权 |
| 平台 Harness | DY01～05、KS01～03、SPH01～03、XHS01～03 | 08-H0～H4 | Draft/规则/探测 REQUIRED；写操作 DEFERRED | 14/14 Skill manifest；官方能力快照；未授权动作不可达 |
| 模型/容量/成本 | Provider/Route/Usage/预算/降级 | 09、08-COST | REQUIRED | measured/estimated/unknown 分离、预算和熔断、成本看板 |
| FDE 六技能 | 理解、认证、探索、映射、同步、验证 | 10-S1～S6 | REQUIRED | 六个输入输出 Schema、六 Checkpoint、恢复/回滚 |
| FDE Reflection | 26 条规则、retry/rollback/pause、硬软规则分离 | 10-R0～R3 | REQUIRED | 26/26 规则测试；禁止执行任意字符串表达式 |
| FDE 平台适配 | CapabilitySnapshot、API 优先、授权浏览器兜底、跨平台经验 | 10-P0～P4 | 抽象 REQUIRED；具体平台 DEFERRED | Adapter Protocol 与 blocked 证据；每个平台专项 EvidencePack |
| 增长 G0 | Evidence/Plan/Task/Handoff/Review 通用 envelope + 电商 spec | 11-G0 | REQUIRED | 不可变 revision/CAS/RLS/职责分离/只读页面 |
| 增长 G1 | D01～D06、每日经营、外部研究、GrowthPlan Draft | 11-G1 | REQUIRED | 真实 OT 新鲜度、引用、无动作结论、完整回放 |
| 增长 G2 | CustomerLite、内容/导购/客服、20 条业务 Logic | 11-G2 | REQUIRED | PII 最小化、三角色工作台、Draft-only、三链路回归 |
| 增长 G3 | 私域/活动/跨渠道、11 条 Logic、实验/归因、consent | 11-G3 | REQUIRED | 退订/频控/静默时段、预算/毛利/库存、归因可复现 |
| 增长 G4 | MemoryCandidate→治理→MemoryItem、个人/共享投影 | 11-G4、06 | REQUIRED | 跨角色最小披露、提升/撤回、效果证据、无跨租户经验泄漏 |
| 增长 G5 | Connector、OAuth/Webhook、平台回执、数字人直播 | 11-G5、08 | 通用连接器 REQUIRED；平台写 DEFERRED | capability snapshot、签名/重放/限流、沙箱；无暗含平台能力 |
| 增长 G6 | ActionProposal、职责分离、预算、频控、kill、补偿 | 11-G6、04 | REQUIRED | maker-checker、Lease、Receipt、unknown/reconcile、补偿演练 |

## 4. 场景覆盖矩阵

| 场景族 | 来源 | 承接 | 裁决 |
|---|---|---|---|
| 新客获客与成交 | 增长母方案核心闭环 | 11-SC01 | 必验收 |
| 老客复购 | 增长母方案 + 旧 AIP | 11-SC02 | 必验收 |
| 客户问题反哺产品/内容 | 增长母方案 | 11-SC03 | 必验收 |
| 大促活动 | 旧 AIP 六场景 | 11-SC04 | 必验收；复用 G3 活动/实验 |
| 新品上架 | 旧 AIP 六场景 | 11-SC05 | 必验收；发布只到 Draft |
| 日常运营巡检 | 旧 AIP + G1 | 11-SC06 | 必验收 |
| 达人寻找、邀约、签约、复盘、长期维护 | 客户共创方案 | 11-SC07 | 必验收；默认 Draft-only |
| 同款控价与同类目比价 | 客户共创方案 | 11-SC08 | 必验收；禁止恶意下单/自动投诉/自动改价 |
| 客户投诉处理 | 旧 AIP | 11-SC09 | 必验收；与 SC03 区分单案处置和聚合反哺 |

每个场景必须列明触发、真实输入、涉及 Logic、Task DAG、Handoff、审批点、停止条件、业务结果、EffectReview、MemoryCandidate 和浏览器验收；不得用一个成功场景代替其它场景。

## 5. 延期不等于遗漏

以下目标已登记但保持不可执行：

- 抖音 Dou+、精选联盟、评论/私信写操作。
- 快手磁力金牛、真实直播和外部触达。
- 视频号/企微/小程序联动中的真实账号写操作。
- 小红书发布、评论和私信写操作。
- 六平台 Connector 的具体官方 API 能力。
- 真实公开直播、自动退款、改价、库存、支付和不可逆操作。

解除 `DEFERRED` 必须满足：官方资料当期核验、测试账号权限、Platform CapabilitySnapshot、G5 Connector 专项评审、G6 Action 安全门、预算与回滚、用户单独授权。

## 6. 冲突裁决

1. 旧“35 个技能”与当前“37 条 Logic”冲突：以增长母方案的 37 条为电商域权威；旧技能名称保留 alias/crosswalk，不作为第二目录。
2. “三层记忆”与“四层记忆”冲突：Working/Episodic/Semantic 是运行记忆；Procedural 是版本化资产，不建第四 Memory store。
3. 旧 FDE 示例中的 Python `eval` 仅作规则表达示意：实现必须使用类型化规则或受控表达式解释器，禁止任意代码执行。
4. 旧平台能力矩阵不代表当前官方能力：开发当期重新联网核验；未核验状态为 `unknown/blocked`。
5. 旧多 worker 章节全部由本轮“m1 单分支、单执行者”决策取代。

## 7. 复审退出门

- [x] 38/38 来源文件均在范围登记中。
- [x] 37/37 Logic 均有唯一 ID、Schema、Tool allowlist、EvalPack、页面/调用入口和证据要求。
- [x] 七知识管道、26 Reflection、14 Harness Skill、G0～G6、9 场景均可定位清单任务。
- [x] 所有平台专项均明确 REQUIRED/DEFERRED/BLOCKED，不存在“看似可用”的无契约按钮。
- [x] 00、03、05、06、08、10、11、12、13、16 与本矩阵一致。
- [x] 单分支规则、租户规则、真实数据规则、证据规则无冲突。

上述门已全部关闭，恢复“全量开发清单统一评审通过”；仍然不自动授权编码。

## 附录 A：38 份来源文件逐份登记

| # | 来源文件 | 主要承接 |
|---:|---|---|
| 1 | `11-AIP决策引擎升级方案/00-总览-从Mock到真实Harness.md` | 01～05、07、11 |
| 2 | `11-AIP决策引擎升级方案/01-Plan-Mode与TAOR循环设计.md` | 02 |
| 3 | `11-AIP决策引擎升级方案/02-私域管家技能编排.md` | 03、11-P01～P05 |
| 4 | `11-AIP决策引擎升级方案/03-六层权限防线设计.md` | 04、05、12 |
| 5 | `11-AIP决策引擎升级方案/04-导购顾问技能编排.md` | 03、11-G01～G06 |
| 6 | `11-AIP决策引擎升级方案/05-内容官技能编排.md` | 03、05、08、11-C01～C08 |
| 7 | `11-AIP决策引擎升级方案/06-客服专员技能编排.md` | 03、11-S01～S06 |
| 8 | `11-AIP决策引擎升级方案/07-活动策划师技能编排.md` | 03、11-A01～A06 |
| 9 | `11-AIP决策引擎升级方案/08-数据参谋技能编排.md` | 03、07、11-D01～D06 |
| 10 | `11-AIP决策引擎升级方案/10-AIP-Logic电商场景编排总览.md` | 03、11-SC01～SC09、12 crosswalk |
| 11 | `11-AIP决策引擎升级方案/11-Evals门控设计.md` | 05 |
| 12 | `11-AIP决策引擎升级方案/DeerFlow-开源成分接入AOS最小适配方案.md` | 02、03、05、06、07、09、10、12 |
| 13 | `11-AIP决策引擎升级方案/DeerFlow-开源成分接入AOS最小适配方案评审记录与封板结论.md` | 12、13 |
| 14 | `13-FDE技能编排方案/00-总览-从静态文档到可编排技能链.md` | 10-S1～S6 |
| 15 | `13-FDE技能编排方案/01-电商FDE技能链设计.md` | 10-S1～S6、Handoff |
| 16 | `13-FDE技能编排方案/02-Checkpoint与回滚设计.md` | 10 CP1～CP6、rollback |
| 17 | `13-FDE技能编排方案/03-六层权限防线设计.md` | 04、10、12 |
| 18 | `13-FDE技能编排方案/04-Reflection自审节点设计.md` | 10-R0～R3 |
| 19 | `13-FDE技能编排方案/10-FDE技能编排总览.md` | 10-P0～P4、12 |
| 20 | `14-行业Wiki基础设施方案/00-总览-三层记忆系统.md` | 06-01～06-07 |
| 21 | `14-行业Wiki基础设施方案/01-三层记忆系统设计.md` | 06-01～06-07、06-22～06-24 |
| 22 | `14-行业Wiki基础设施方案/02-七条知识管道设计.md` | 06-13～06-19 |
| 23 | `14-行业Wiki基础设施方案/03-知识治理三层过滤.md` | 06-02～06-05、12 |
| 24 | `14-行业Wiki基础设施方案/04-美妆行业Wiki冷启动方案.md` | 06-20～06-21 |
| 25 | `14-行业Wiki基础设施方案/10-行业Wiki架构总览.md` | 06、12 |
| 26 | `内容官-短视频生产实现方案.md` | 08-V0～V3 |
| 27 | `内容官-交互式数字人直播实现方案.md` | 08-L0～L5 |
| 28 | `内容官-平台专属HarnessSkills.md` | 08-H0～H4 |
| 29 | `内容官-数字人直播成本备忘.md` | 08-COST、09 |
| 30 | `228-电商增长参谋长与六数字同事协同进化实施方案.md` | 03、06、08、11-G0～G6/37 Logic/SC01～SC09 |
| 31 | `228-电商增长参谋长实施文档索引与分波路线图.md` | 00、11、13 |
| 32 | `228-电商增长参谋长G0契约与安全底座实施方案.md` | 04、05、11-G0 |
| 33 | `228-电商增长参谋长G1每日经营最小闭环实施方案.md` | 07、11-G1/SC06 |
| 34 | `228-电商增长参谋长G2三个核心数字同事与CustomerLite实施方案.md` | 03、06、08、11-G2/SC01/SC03/SC09 |
| 35 | `228-电商增长参谋长G3私域活动与跨渠道分析实施方案.md` | 11-G3/SC02/SC04 |
| 36 | `228-电商增长参谋长G4多智能体记忆与协同进化实施方案.md` | 06、11-G4、12 |
| 37 | `228-电商增长参谋长G5社交平台Connector与数字人直播实施方案.md` | 08、10、11-G5 |
| 38 | `228-电商增长参谋长G6受控生产Action与经营自动化实施方案.md` | 04、05、11-G6 |

# W3-11 内容活动 Campaign / Calendar / Intent / Artifact 与排期预检 ADR

> 日期：2026-08-15  
> 状态：`IMPLEMENTATION_REAUDIT_IN_PROGRESS / AOS-000222 / NO_RELEASE / NO_EXTERNAL_EFFECT`  
> 基线：`AOS-000222`、`m1@da5c42109685b6c2143bee26b2f85d204bb32c23`  
> 证据：`.evidence/workshop/2026-08-15-w3-11-content-campaign-authority-preflight.json`

## 1. 决策

W3-11 只在公共生产合同之上增加内容活动领域 authority、领域服务与可重建投影，不复制 TaskBrief、Artifact、ArtifactRelation、Action、Approval、Lease 或 Receipt 真源。当前代码尚无 CampaignRevision、CalendarEntry、MasterContentIntent authority，也无 content-campaign Store/API/strict SDK；W3-10 与 W2-03 未运行 GREEN，因此只允许方案闭合，不进入实现。

唯一命名裁决为 `ContentVariant`。它沿用已发布 Module manifest，表示由 exact Intent、master Artifact、channel Artifact 与 ArtifactRelation 重建的渠道变体读模型；“渠道变体”和旧称 `ChannelVariant` 仅是兼容 alias。不得新建 ContentVariant 正文表、双 head、双 Store 或双 API。

## 2. Authority 与命令

| 对象 | 唯一 authority | 写入口 | 不得代替 |
|---|---|---|---|
| 活动计划 | append-only CampaignRevision | create；revise(expectedVersion) | TaskBrief、TaskGraph、页面 draft |
| 排期 | append-only CalendarEntry revision/decision | create；reschedule/cancel(expectedVersion) | 前端日历位置、Task dueAt、发布 Action |
| 创作意图 | append-only MasterContentIntent | create；revise(expectedVersion) | Prompt、母稿正文、TaskBrief spec |
| 母稿/渠道产物 | canonical Artifact revision | attach exact relation | ContentVariant 读模型、页面缓存 |
| 渠道关系 | canonical ArtifactRelation | attach master/variant exact refs | 复制正文、另建 variant lineage |
| 发布 | Action Proposal/Approval/Lease/Receipt | 独立 publish command | CalendarEntry due/ready、TaskRun succeeded |

所有首次创建以 Idempotency-Key 去重；所有修订、改期与取消必须带 expectedVersion。服务端只从 Principal 获取 TenantScope，回读同租户 canonical Receipt；重复 key 同 hash 返回同结果，不同 hash 冲突。跨租户、未知 ref、hash/revision 漂移一律失败关闭。

## 3. 排期、改期、取消与发布分离

CalendarEntry 同时固化 timezone、localStart/localEnd、resolved UTC instants、解析规则、exact CampaignRevision、exact Content Artifact refs、冲突判断及 actor/reason。DST 歧义或不存在的本地时刻必须要求显式 resolution，不能由浏览器时区静默修正。

改期与取消生成 successor revision/Decision 并保留 prior ref；取消不撤销已经发生的发布，改期不重写历史 Receipt。冲突 override 是独立、可审计决定，不允许用拖拽覆盖冲突。排期只声明意图与窗口：到期、ready 或无冲突都不会创建 Proposal、获取 Lease 或调用 Provider。

发布必须经过独立 Action Proposal → Approval → Lease → Attempt/Receipt。provider unknown 保持 unknown 并进入 reconcile；不得通过再次排期、自动重试或页面乐观态把 unknown 改成成功。

## 4. Drift 与数量守恒

- CampaignRevision 漂移使引用旧 revision 的未执行 CalendarEntry stale；历史排期仍可读。
- MasterContentIntent 或 master Artifact 漂移使下游 ContentVariant 与未执行排期 stale；已批准/已发布 Artifact 不被覆盖。
- ContentVariant exact Artifact/relation 漂移时阻断 readiness，必须显式接受 successor 后才能恢复。
- plan/calendar/content 使用同一 cutoff、时区和 eligible denominator；partial/stale/blocked/unknown 不计 completed/published。
- 每个 CalendarEntry 绑定一个 exact CampaignRevision；每个 ContentVariant 只有一个 exact master lineage root，relation graph 不得成环。

## 5. 依赖与实现边界

硬依赖为 W3-10、W2-03、DEP-C0、`DEP-CONTENT-CANONICAL-NAMING`、`DEP-CAMPAIGN-CALENDAR-AUTHORITY`、`DEP-CONTENT-INTENT-ARTIFACT-BRIDGE`、`DEP-SCHEDULE-CONFLICT-POLICY` 与 `DEP-PUBLICATION-ACTION-ADAPTER`。W3-11 只能贡献 L1 typed profile/service/projection；公共 Task/production/Action authority 仍由 AIP 持有。

实现验收必须在同一 release identity 覆盖 Contract、Store、API、strict SDK、Web、browser、安全与租户：幂等/CAS、跨租户、DST、冲突 override、改期/取消、drift、图环/orphan、排期与发布分离、unknown/reconcile、刷新恢复和数量守恒。正向只认 `org-org/dev-project`，`dev-org/dev-project` 只作负向隔离 canary。

## 6. 两轮审查

第一轮发现旧方案未裁决 `ContentVariant`/`ChannelVariant`，并可能把 ContentVariant 写成第四类正文 authority。整改后冻结唯一名称，并明确实际母稿和渠道产物只归 Artifact authority。

第二轮发现旧方案仅说 create/revise/schedule，未完整规定改期/取消 successor、DST、冲突 override、排期与发布分离、unknown reconcile 和 drift 传播。补齐后方案复审通过；但代码、Store、API、SDK、页面与浏览器证据均不存在，故 W3-11 仍为 `RUNTIME_NOT_STARTED / HARD_GATE_BLOCKED`，不得勾选。

## 7. 2026-08-25 AOS-000222 现场重核与实施清单

### 7.1 旧结论已过期

当前 `m1` 已存在且可追溯到代码提交的 Campaign/Calendar/Intent strict contract、tenant-bound append-only Store、`w3_011` RLS migration、ContentVariant exact ArtifactRelation 投影、GET-only Workshop View、strict Web SDK 与 Content Campaign 只读页。因此第 1、5、6 节中“代码不存在”只保留为 2026-08-15 历史截面，不再是本次实施事实。W3-10 已于 `AOS-000222` 前闭合五层累计门，W3-11 已解除代码开工阻断。

### 7.2 163/164 分层裁决

- CampaignRevision、CalendarEntryRevision、MasterContentIntentRevision 和 ContentVariant 是 Domain authority/读模型，不冒充原子 Skill。
- 排期、改期、取消是受控 Domain Command/Tool，不冒充“内容生产大 Skill”；发布仍属独立 Action 链。
- 业务 Logic 应由 `frame-content-brief`、`content-strategy`、`channel-content-adaptation`、`verify-claims`、`review-output-quality` 等原子 Skill 与人工门编排，本域 Store 不复制 Logic。
- 页面只复用 W3-09 公共 `ContributionLineage`，当前无 exact AgentRun/SkillBinding/LogicRevision 时必须显示 `unknown`，不用六角色静态卡片或样例绑定补齐。
- 未来 canonical AgentRun 贡献仍经 S2.5 `SkillContributionView` 和严格 SDK 读取，本页不建第二 Skill/Agent/Binding authority。

### 7.3 本波文件级清单

1. 复核并封板 `ecommerce_content_campaign_authority_contracts.py`、`ecommerce_content_campaign_authority_store.py`、`ecommerce_workshop_content_campaign*.py` 和 `w3_011` migration，不重写现有 authority。
2. 在 `ContentCampaignPage.tsx` 复用公共 `ContributionLineage`，仅表达专业贡献边界；没有 exact refs 时保持 unknown。
3. 补充 `ContentCampaignPage.test.tsx` 的公共组件复用、unknown 诚实性和零写入回归；累计跑后端 contract/store/view/API、OpenAPI、Web 全量和生产构建。
4. 内置浏览器在 `org-org/dev-project` 完成 1280/1440/1920、键盘、失败关闭、数量守恒、ContentVariant lineage 与贡献路径验收；`dev-org/dev-project` 仅作负向隔离 canary。
5. 生成同一 candidate identity 的 evidence/Receipt，然后仅在 m1 串行 CAS authority 与 Prime 回读。

### 7.4 不变边界

本波不 live apply migration，不对真实业务表执行排期/改期/取消，不创建 Provider/AgentRun/Action/Approval/Handoff/Lease，不发布内容。Store 的写路径只通过合同与 fake-connection/offline migration 验证；Workshop 页面继续 GET-only。因此本波 GREEN 最多表示 code/control/browser GREEN，不等于 operational 或 release GREEN。

## 8. 2026-08-25 实施与验收结论

本次没有建立第二套领域 authority，也没有把 Campaign、Calendar、Intent 或 ContentVariant 错标为原子 Skill。页面复用公共 `ContributionLineage`，将领域 authority 解释为 Logic 的业务输入；由于当前 View 没有 exact AgentRun、SkillBinding 或 LogicRevision，原子 Skill、Logic 编排和数字同事均保持 `unknown`，只陈述工作台对当前切片的可验证贡献。

专项测试为后端 `36 passed`、Web `17 passed`，累计回归为后端 `181 passed`、Web `221 files / 2084 tests`，OpenAPI 确定性导出、TypeScript 与 production build 均 GREEN。内置浏览器连接当前 `m1` API，在 `org-org/dev-project` 的 1280×720、1440×900、1920×1080 三档无横向溢出；三切片、结构化 blocker 和专业贡献路径可见，未暴露批准、发布、保存、排期编辑或自动拆解入口。未应用 live migration，未执行真实业务写、Provider、AgentRun、Action、Approval、Handoff、发布或离线队列冲刷。

结论：`W3_11_CODE_BROWSER_GREEN / NO_RELEASE / NO_EXTERNAL_EFFECT`。该结论只允许进入 W3-12 闭合审查，不代表生产发布或运营 GREEN。

# W4-05 KnowledgeQuery 与 Memory 治理生产装配预检 ADR

> 状态：`RE-REVIEWED / AUTHORIZED_IN_PROGRESS`
>
> 初始事实截面：AOS authority `AOS-000024`；证据 `.evidence/workshop/2026-08-14-w4-05-knowledge-memory-governance-preflight.json`。
>
> 2026-08-25 重审截面：AOS authority `AOS-000229`；Task `workshop-w4-05-knowledge-memory-governance-20260825`。

## 1. 审查结论

AIP-5 的 MemoryCandidate、CandidateEvent、MemoryItemRevision、治理服务、KnowledgeQuery/Search、Citation、Readiness、严格 SDK 和治理页面均已存在，治理/检索相关 35 项测试通过。Candidate 由可信知识管道提交，approve/promote 有 reviewer/admin 角色门，Query/Search 有角色、marking、freshness、applicability 与 citation-content 对齐规则。

这些事实仍不足以宣称 W4-05 可用：正式 Router 的 governance、retrieval、search dependencies 当前固定返回 `None`。因此 approve/promote/query/search 在生产装配下按设计返回 503；现有服务 GREEN 和测试替身不能替代真实 provider。真实 `org-org/dev-project` 的 Candidate、Memory、Readiness 和完整 Citation 查询也尚未在本任务中验证。

W4-05 保持 `NOT_STARTED / IMPLEMENTATION_BLOCKED`。当前 503 是正确的安全状态，不得用 demo resolver、静态知识或前端 fallback 消除。

## 1.1 2026-08-25 重审与变更授权

旧结论中“正式 Router 固定返回 `None`”已过时：`aip_memory_production_factory.py` 已从租户内 PostgreSQL authority 装配 governance、retrieval 与 search，Router 三个 getter 均返回真实服务。但 factory 存在不等于 provider 可用；当前 readiness 仅以 search service 是否为 `None` 填充 `providerConfigured`，会在 fulltext capability 仍 unbuilt/blocked 时给出误导性 `true`。

本次只授权以下最小改动：

1. `services/aos-api/aos_api/aip_memory_readiness.py`：将可用 provider 判定与租户内 exact SearchCapability 对齐；fulltext 未 ready 时 `providerConfigured=false` 并保留稳定 blocker。
2. `services/aos-api/aos_api/routers/aip_memory_authority.py`：Router 只传入“factory 已装配”事实，最终 readiness 由 capability authority 裁决；不执行索引重建、Candidate 提交或 promotion。
3. `apps/web/src/pages/s2/MemoryGovernancePage.tsx`：消费 exact `subjectType/subjectId/taskId/skillId/view` 深链，显示“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献”的当前上下文，但不在前端生成或提升 MemoryCandidate。
4. 对应 backend/Web 合同测试、累计回归、内置浏览器真实租户只读验收和证据封存。

明确不在本次改动中伪造的事实：KnowledgePackage 安装 authority 和 GoldSet registry 当前仍无可计数的专用权威映射，继续显示 `authority_unavailable`；真实租户无 Candidate/Memory/Citation 样本时保留空态，不插入测试数据。

因此 W4-05 从“整体实现阻断”转为“可执行代码闭环，运营正向仍由真实 authority/readiness 决定”。验收结论最高只能是 `CODE_BROWSER_GREEN / NO_RELEASE / NO_EXTERNAL_EFFECT`。

## 2. 唯一 authority

- Candidate 只由 AIP Memory Store 持久化，提交来源为受信 KnowledgePipeline 或有 Task/Run/Receipt/Eval 证据的 EffectReview/Observation。
- approve/promote 只由 AIP Governance service 裁决；工作台不直接改 status。
- 正式 Memory 与 revision 只由 promotion transaction 产生。
- Query/Search/Citation 只由 AIP Retrieval/Search service 产生；工作台不拼接检索结果或补写引用。
- KnowledgeReadiness 是生产可用性门；类、路由、测试、页面任一单项均不能代替 readiness。

## 3. 生产装配门

必须以显式 factory 装配并验证：

1. exact Artifact payload resolver 与 PII/redaction inspection；
2. current license policy resolver；
3. EvalReport/Draft/ApprovalEvent governance authority resolver；
4. Memory payload resolver；
5. Search index/provider 与 authority-scan degradation 语义；
6. tenant/marking/applicability/freshness/revoke 全链；
7. timeout/unknown/failure 的稳定 reason code 和零无引用 fallback。

provider 未齐时继续返回 503；部分 provider 就绪时由 KnowledgeReadiness 分项显示 blocked/degraded/ready，不允许单一绿色总灯掩盖依赖。

## 4. 工作台消费

八 Module 只增加 context-scoped projection/deep link：以 exact Candidate/Memory/Subject ref 跳转通用治理页面，展示来源、治理证据、事件、适用范围和 Citation。通用页面负责 approve/promote 等命令；Module 不复制状态机。

若产品需要模块内处置，仍复用同一 SDK/command，并在按钮前展示服务端 Impact/permission/readiness；命令后回读 authority。没有完整治理表单时宁可只读，不提供“快速批准”。

## 5. 验收门

- production factory 不再返回 None，且使用的每个 resolver 都有固定 authority 和失败关闭测试。
- reviewer/admin 可 approve/promote；其他角色 403，角色检查先于 provider 可用性泄露。
- Query 对 marking/applicability/freshness/license/revoke/hash 任一失败返回 blocked/degraded 与稳定 reasons，零伪 Citation。
- Search provider 不可用时 readiness 与 query/search 行为一致，不用静态结果兜底。
- `org-org/dev-project` 只读验证至少一个真实 Candidate timeline、一个正式 Memory 和一次 citation-content 对齐的完整查询；`dev-org/dev-project` 保持隔离 canary。
- Module deep link 保留 exact context，返回后状态由 authority 回读；无 localStorage authority。

## 6. 明确废弃与禁止

- 废弃“服务类存在或单测通过即代表生产可用”的判断。
- 禁止将 `get_*_service() -> None` 临时替换成无可信 resolver 的默认实例。
- 禁止 Workshop 提供绕过 pipeline 的自由 Candidate 提交表单。
- 禁止用 Wiki 示例、静态候选或无引用生成文本填充空态。
- 禁止在八 Module 各复制一套 Candidate/Memory 审批状态机。

这些禁止项保护的是治理真实性；不会减少用户可见性，反而要求每个不可用状态和具体依赖都透明展示。

## 7. 2026-08-25 实施与验收闭环

### 7.1 实施事实

- 代码提交：`m1@70b9a19`；证据提交：`m1@7b3fb57`。
- Backend 将 `providerConfigured` 改为“factory 已装配 且租户 fulltext SearchCapability 为 ready 且具有 exact provider/revision”的合取；仅服务对象存在不再冒充 provider ready。
- Web 严格 SDK 拒绝 `providerConfigured=true` 但 fulltext 非 ready 的矛盾响应。
- 治理页消费 `subjectType/subjectId/taskId/skillId/logicId/coworkerId/moduleId` 受限 exact 深链，展示“原子 Skill → Logic 编排 → 数字同事 → 工作台模块”贡献上下文；不新增 Candidate 提交或快速晋升入口。

### 7.2 验收事实

- Backend 专项 `21 passed`，Memory 领域累计 `73 passed`。
- Web 专项 `23 passed`，全量 `221 files / 2093 tests passed`，TypeScript 与 production build GREEN。
- OpenAPI 确定性校验通过，合同 `13 passed`；compileall 与 `git diff --check` GREEN。
- 内置浏览器在 `/aip/memory-governance?view=query...` 确认 Subject/Task/Skill 预填、完整贡献链及刷新保留；矛盾 readiness fixture 被 strict SDK 拒绝。该 fixture 只是 UI 验收传输，不是生产运行就绪证据。
- 全程未发起 KnowledgeQuery POST、pipeline command、Candidate governance command，未做迁移、发布或真实业务写入。

### 7.3 结论与剩余边界

W4-05 结论为 `W4_05_GOVERNED_MEMORY_ASSEMBLY_CODE_BROWSER_GREEN_NO_RELEASE_NO_EXTERNAL_EFFECT`。KnowledgePackage installation authority、GoldSet registry authority 和真实租户正向 Candidate/Memory/Citation 样本仍以 readiness 事实为准；缺失时保持 blocked/empty，不影响 W4-06 继续做可开发的 Wiki 消费闭环，也不构成运营或发布 GREEN。

证据：`.evidence/workshop/2026-08-25-w4-05-knowledge-memory-governance.json`。

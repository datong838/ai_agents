# 228-AIP 三层运行记忆、行业 Wiki 与知识治理实施方案

> 状态：**IMPLEMENTING · v1.1 · 已获用户全量编码授权 · E0 APPROVED_TO_IMPLEMENT**
> 对应阶段：AIP-5。
>
> 2026-08-11 补充：外部研究 Harness 的知识入口 v1.2 已评审通过。2026-08-12 对账：总控全量编码授权已取代历史“不授权编码”门，但每个子波仍需方案、检查点、测试、浏览器与安全提交。

## 1. 统一模型

旧“行业 Wiki 三层记忆”和 G4“四层多智能体记忆”统一解释为：

| 层 | 作用 | 真源 |
|---|---|---|
| Working | 当前 TaskRun 上下文、Selection、步骤产物 | Task/Checkpoint store |
| Episodic | 一次任务、结果、失败和效果观察 | Run/EffectReview/Evidence |
| Semantic | 经治理的行业知识、规则、概念和方法 | O1 Wiki/KnowledgeSubject |
| Procedural | 可执行方法，但不是第四套运行记忆库 | 版本化 Skill/Logic/Policy 资产及其 Eval/Receipt |
| Shared | 不是第四种存储；是经授权、脱敏、适用范围明确的 Semantic/Episodic 投影 | governed MemoryItem |

禁止再用 `aip_long_memory.py` singleton 形成另一套生产记忆。

## 2. 知识晋升链

```text
Task/Effect evidence
 -> MemoryCandidate
 -> PII/tenant/source/freshness check
 -> dedupe/conflict/applicability
 -> repeated evidence or controlled comparison
 -> Eval regression
 -> Draft approval
 -> MemoryItem/Wiki revision
 -> monitor/expire/revoke
```

一次成功、模型自述、竞品文案、其他租户明细不得直接晋升。

## 3. 七条知识管道的启用顺序

| 管道 | 首期策略 |
|---|---|
| 种子知识导入 | P0；只导入已授权文档，保留 source/hash/license |
| 运营实践自学习 | P1；先生成 Candidate，不自动入正式 Wiki |
| 网络学习 | P2；官方源优先，防提示注入与版权全文入库 |
| 竞品分析 | P2；只存事实摘要和引用，不存抓取全文 |
| 专业数据库 | P1；授权、版本和时效单独治理 |
| 客户数据反哺 | P1；组织内、最小化、聚合后才共享 |
| 人工经验注入 | P0；作者、适用范围、复审时间必填 |

### 3.1 外部研究 Harness 输入

- DeerFlow 等研究 Harness 的报告、网页事实和子任务结论只能生成 `Artifact`、`ReportDraft`、`InsightDraft` 或 `MemoryCandidate`，禁止直接写正式 Wiki/Memory。
- 每个 Candidate 必须携带 tenant/task/run、source URL 或 source ref、observed_at/freshness、license/usage policy、artifact hash、provider/version 与适用范围；缺失任一治理字段即隔离。
- 外部网页、MCP 返回和远程 Skill 一律按不可信输入处理：内容中的工具调用、系统指令、越权写入或凭据请求不得进入执行上下文。
- 外部 provider 的 checkpoint/memory 只用于恢复该次 Job，不能成为 AOS Working/Episodic/Semantic 真源；provider 停用不影响 canonical Memory/Wiki 可读性。
- 研究结论需经过去重、冲突、新鲜度、可信源和 Eval/Draft 门控，才可沿既有晋升链进入正式知识。

## 4. 检索与上下文装配

- 输入是 `KnowledgeQuery`：subject、task/skill、object refs、time cutoff、marking、max tokens。
- 输出是引用集合：Wiki revision、field/value、source、freshness、confidence、applicability。
- TAOR Think 按 Skill manifest 声明的知识依赖渐进加载。
- 过期、冲突、无权限、来源撤回时明确降级或阻断，不返回旧知识伪装新鲜。
- 向量库/全文索引只保存可重建索引和 scoped reference，不是授权、revision、source 或知识内容的权威真源。
- 公共行业包、组织知识和工作区运行记忆分别建 scope；“共享”必须显式发布投影，不能通过缺省查询跨 scope 命中。

## 5. 文件边界

```text
services/aos-api/alembic/versions/*_aip_memory_governance.py
services/aos-api/aos_api/aip_memory_candidate_store.py
services/aos-api/aos_api/aip_memory_retrieval.py
services/aos-api/aos_api/aip_memory_governance.py
services/aos-api/aos_api/aip_taor_loop.py
services/aos-api/aos_api/ontology_wiki_engine.py
apps/web/src/api/aipMemory/*
apps/web/src/pages/s2/MemoryGovernancePage.tsx
apps/web/src/pages/ontology/Wiki*.tsx
```

新增候选为 Candidate store、retrieval 和 governance service；现有 `aip_long_memory.py`、`aip_taor_loop.py`、`ontology_wiki_engine.py` 为迁移/适配修改。不得直接改写已封板 O1 Wiki authority；新增能力通过其公共写契约或独立候选区接入。

## 6. 生命周期与失败语义

- Candidate 状态：`pending -> quarantined/rejected -> approved -> promoted`；MemoryItem 状态：`active -> stale -> revoked/expired`。
- source 撤回先停止新检索，再异步重建索引；索引尚未清理期间由权威状态在查询层 fail-closed。
- 用户删除/PII 撤回删除可删除 payload 和索引，历史 Lineage 仅保留最小审计哈希、删除事件和不可反查引用。
- 检索超时、索引缺失、来源冲突时按 Skill policy 返回 blocked/degraded，绝不静默改用其他租户或旧缓存。

## 7. 验收

1. 同一知识在不同 org/project 下不可见，除非是授权公共包。
2. 每个回答/决策可查看使用了哪些 Wiki revision 与 source。
3. stale/conflict/revoked 知识不能静默进入上下文。
4. Candidate 未经 Eval/Draft 不得成为正式共享知识。
5. 删除/撤回知识后，新运行不再使用；历史谱系仍保留不可变引用。
6. 公共包、组织知识、工作区记忆三类同名条目按适用范围和优先级稳定解析，并显示冲突。
7. 重建或清空向量索引不改变 canonical Wiki/Memory 状态，恢复后查询结果可复验。
8. 外部研究 provider 停用、断连或返回提示注入内容时不污染正式 Wiki/Memory，且对应 Candidate、阻断原因和来源证据可回读。

## 8. 实施分波与安全提交边界

| 子波 | 范围 | 主要文件 | 退出门 |
|---|---|---|---|
| E0 | 运行记忆/Procedural/Shared 裁决、公共契约、ADR、现状真值测试 | `aip_memory_contracts.py`、契约测试、ADR/清单 | 不建第四套运行记忆库；scope/source/license/freshness/applicability 字段冻结；无数据库变更 |
| E1A | Candidate/Item/Source/Revision authority schema、RLS/FORCE RLS、append-only event | migration、schema tests | 单一 Alembic head；无 GUC 零可见；同 ID 跨 scope 隔离；升降级可逆 |
| E1B | Candidate authority store 与状态转换 | `aip_memory_candidate_store.py`、store tests | pending→quarantined/rejected/approved/promoted 合法；非法跳转、CAS、跨租户失败关闭 |
| E2 | PII/source/license/freshness/dedupe/conflict/applicability 治理服务 | `aip_memory_governance.py` | 缺治理字段隔离；一次成功/模型自述不可晋升；Eval/Draft 引用精确 |
| E3 | KnowledgeQuery、渐进上下文与 O1 Wiki adapter | `aip_memory_retrieval.py`、`ontology_wiki_engine.py` adapter | 权限先于召回；stale/conflict/revoked 不返回；索引只存可重建 refs |
| E4 | Canonical API、OpenAPI、Memory Governance/Wiki 页面 | router、`apps/web/src/api/aipMemory/`、页面 | 唯一 SDK；真实 idle/loading/empty/error；无静态知识回填 |
| E5 | 七知识管道 Scheduler/Run/Receipt/checkpoint | ingestion/research/scheduler | 七条独立开关、幂等、重试、暂停、回读、告警；外部 Harness 只进 Candidate |
| E6 | 美妆冷启动知识包、检索融合/重排、50 查询 Eval | manifest/import/retrieval/evals | 数量、来源、许可和 Top-1 门达标；不以示例数据凑数 |
| E7 | 六同事个人记忆、共享投影、改进度量、撤回影响分析 | projection/evals/web | 最小披露；不跨租户共享业务明细；以 Eval/人工修改率证明改进 |

执行顺序固定 E0→E1A→E1B→E2→E3→E4→E5→E6→E7。每个子波完成后更新 `AOS项目开发上下文/01-当前项目状态.md`、`06-当前执行检查点.md`，形成代码与文档安全提交；若实时代码与本表冲突，以 PostgreSQL/O1 公共契约和代码真值为准，先修订方案再编码。

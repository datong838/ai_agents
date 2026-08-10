# 228-AIP 三层运行记忆、行业 Wiki 与知识治理实施方案

> 状态：**评审通过 · v1.0 方案基线（仍不授权编码）**
> 对应阶段：AIP-5。

## 1. 统一模型

旧“行业 Wiki 三层记忆”和 G4“四层多智能体记忆”统一解释为：

| 层 | 作用 | 真源 |
|---|---|---|
| Working | 当前 TaskRun 上下文、Selection、步骤产物 | Task/Checkpoint store |
| Episodic | 一次任务、结果、失败和效果观察 | Run/EffectReview/Evidence |
| Semantic | 经治理的行业知识、规则、概念和方法 | O1 Wiki/KnowledgeSubject |
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

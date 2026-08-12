# 06 AIP 三层运行记忆、行业 Wiki 与知识治理开发清单

> 状态：**v1.3 · 已获用户全量编码授权 · E0 IMPLEMENTED_GREEN · E1A APPROVED_TO_IMPLEMENT**
> 上位依据：`../06-228-AIP三层记忆行业Wiki与知识治理实施方案.md`
> 对应阶段：AIP-5；前置：02、04、05 GREEN。

## 1. 工作包

| ID | 任务 | 文件边界 | 验收 |
|---|---|---|---|
| 06-01 | 冻结 Working/Episodic/Semantic、Shared 投影和 Procedural 资产边界 | contracts/ADR | 不建第四套运行记忆库 |
| 06-02 | 建 MemoryCandidate/MemoryItem/source/revision/governance 表与 RLS | migration/store | scope、状态、来源、新鲜度完整 |
| 06-03 | 实现 Candidate 提交、隔离、拒绝、批准、晋升 | governance service | 未经 Eval/Draft 不进正式 Wiki |
| 06-04 | 实现 PII/tenant/source/license/freshness/dedupe/conflict/applicability 门 | governance | 一次成功/模型自述不可晋升 |
| 06-05 | 实现 KnowledgeQuery 与渐进上下文装配 | retrieval | token 预算、marking、time cutoff 生效 |
| 06-06 | 复用 O1 Wiki/KnowledgeSubject authority | ontology wiki adapter | 不直接改写封板 authority |
| 06-07 | 建全文/向量可重建索引与 scoped refs | index adapters | 清空索引不改变 canonical 状态 |
| 06-08 | 启用种子导入与人工经验 P0 管道 | ingestion jobs | source/hash/license/复审时间完整 |
| 06-09 | 启用运营反哺/客户聚合/专业库 P1 管道 | candidate jobs | 组织内最小化，跨组织只发布投影 |
| 06-10 | 启用网络/竞品 P2 管道 | research adapter | 防提示注入，不存未授权全文 |
| 06-11 | 外部 DeerFlow 研究只接 Artifact/Draft/Candidate | research input | provider memory 不成为 AOS 真源 |
| 06-12 | Memory Governance/Wiki 页面与引用解释 | API/web | stale/conflict/revoked 可见且阻断 |
| 06-13 | 管道1 种子知识导入 | ingestion/manifest | 方案、SOP、平台规则均有 source/hash/license |
| 06-14 | 管道2 运营实践自学习 | task completion candidate job | 只生成 Candidate，一次成功不能晋升 |
| 06-15 | 管道3 网络学习 | scheduled ResearchJob | 防注入、限量、引用、时效、L4 门控 |
| 06-16 | 管道4 竞品分析 | scheduled ResearchJob | 只存允许摘要/事实，不复制未授权全文 |
| 06-17 | 管道5 专业知识库 | professional adapter | CosDNA/NMPA 等来源先过授权、许可与版本核验 |
| 06-18 | 管道6 客户反哺、管道7 人工经验 | event/manual candidate jobs | 聚合/去敏；人工经验也需冲突与适用范围治理 |
| 06-19 | 建七管道 Scheduler、Run、Receipt、checkpoint 和状态看板 | scheduler/API/web | 七条独立开关、重试、暂停、回读、告警 |
| 06-20 | 建美妆知识包冷启动 manifest、导入与回滚 | vertical knowledge bundle | ≥300 总量、≥200 成分、≥50 话术、≥30 规则 |
| 06-21 | 建冷启动标注集和检索/角色覆盖 Eval | evals/retrieval | 50 查询 Top-1≥80%，六角色依赖覆盖 100% |
| 06-22 | 实现全文+向量召回、融合、重排和引用装配 | retrieval adapters | 权限先于召回；索引空/坏时诚实降级 |
| 06-23 | 建个人记忆、共享投影和跨角色最小披露 | memory projection | 不共享工作记忆/敏感会话；共享项有治理 revision |
| 06-24 | 建记忆改进度量与撤回影响分析 | evals/governance | 用 Eval/人工修改率/事实率证明改进，不以文本量代替 |

## 2. 七条知识管道冻结表

| 管道 | 触发 | 默认级别 | 当前清单状态 |
|---|---|---|---|
| 种子知识 | 手动冷启动 | P0/L1 | REQUIRED |
| 运营实践自学习 | Task 完成事件 | P2/L3 | REQUIRED，先 Candidate |
| 网络学习 | 定时 ResearchJob | P2/L4 | REQUIRED，来源未核验则 blocked |
| 竞品分析 | 定时 ResearchJob | P3/L4 | REQUIRED，外部全文受限 |
| 专业知识库 | 定时/版本事件 | P0/L1-L2 | REQUIRED，适配器/许可未就绪则 blocked |
| 客户数据反哺 | 订单/评价/服务事件 | P1/L3 | REQUIRED，只允许聚合去敏事实 |
| 人工经验 | 人工提交 | P0/L2 | REQUIRED，不能绕过治理 |

原 06-08～06-10 的 P0/P1/P2 分组只是优先级视图，本表才是七条管道的完整交付目录。

## 3. 三层运行记忆与 Procedural 裁决

- Working：任务级 TTL，上下文和中间结果。
- Episodic：有条件、结果、EffectReview 的经历，可过期/撤回。
- Semantic：稳定事实和经验证知识，版本化治理。
- Procedural：Skill/Logic/Policy/Playbook 的版本化发布资产；不创建第四套运行时 Memory store。

所有跨角色共享只发布经治理的最小投影；跨租户最多复用脱敏、抽象、获授权的方法资产，不复用租户业务数据。

## 4. 删除、撤回与失败语义

- source 撤回先阻止新检索，再重建索引；payload 删除只保留最小不可反查审计哈希。
- 检索超时、索引缺失、来源冲突返回 blocked/degraded，不跨租户或静默用旧缓存。
- provider 临时 memory/checkpoint 有 TTL 和清理 Receipt，不影响 canonical Wiki/Memory。

## 5. 退出门

- [ ] 每次回答可查看 Wiki revision、source、freshness、confidence、applicability。
- [ ] 同名公共包/组织知识/工作区记忆解析稳定并显示冲突。
- [ ] stale/revoked/撤回来源不进入新上下文；向量索引不是授权真源。
- [ ] 外部研究、客户数据、人工经验均经过统一 Candidate 晋升链。
- [ ] 七条管道分别具有 Schedule/Run/Receipt/checkpoint、状态页和失败/恢复证据。
- [ ] 美妆冷启动达到量化门；来源和许可证不满足时保持 blocked，不用示例知识凑数。
- [ ] 检索 Eval 包含关键词、语义、混合、重排、权限、新鲜度、冲突和引用正确性。
- [ ] 六数字同事各有个人记忆策略，共享投影不暴露另一同事的工作记忆或客户敏感会话。

## 6. 当前执行顺序

- [x] E0：冻结公共契约与 ADR；复核 `aip_long_memory.py`/TAOR/O1 Wiki 现状，证明没有平行生产真源。代码 `bb84fc3`；新旧兼容记忆回归 15 passed，compile/diff check GREEN。
- [ ] E1A：Candidate/Item/Source/Revision/Event authority migration、RLS/FORCE RLS、升降级与隔离测试。
- [ ] E1B：Candidate store、CAS 和合法状态机。
- [ ] E2：七类治理门与统一晋升服务。
- [ ] E3：KnowledgeQuery、渐进上下文、O1 Wiki adapter 和可重建索引。
- [ ] E4：Canonical API/SDK/治理页面与浏览器验收。
- [ ] E5：七知识管道的 Schedule/Run/Receipt/checkpoint。
- [ ] E6：美妆知识包冷启动、混合检索与量化 Eval。
- [ ] E7：六同事个人记忆/共享投影、撤回影响与改进度量。

本清单中的全量授权不允许跨波偷跑；每个子波必须更新 `01-当前项目状态.md` 和 `06-当前执行检查点.md` 并形成安全提交。

E0 实施结论：运行层只允许 Working/Episodic/Semantic；Procedural 继续作为版本化 Skill/Logic/Policy/Playbook，Shared 只作治理投影。Working 不进入 Candidate 晋升链；写请求 DTO 不接受租户字段；Semantic Candidate 必须保留精确来源、hash、新鲜度、适用范围，并在批准/晋升前绑定 Eval report、Draft 和 ApprovalEvent。旧 `aip_long_memory.py` 与 `ontology_wiki_engine.py` singleton 明确降级为兼容层，不是生产权威。

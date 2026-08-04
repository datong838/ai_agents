# 228 · TI-3 E2 Object/Graph/Draft Runtime 显式 TenantScope 实施方案

> 版本：v1.0 · 2026-08-04
> 状态：GREEN；E2-A/E2-B/E2-C 全部完成
> 前置：TI-3 E1 `7f7d48a` GREEN；Alembic `228ti3e1expand`

## Rules

E2 只处理新请求和新写的显式 TenantScope，不回填 1,030 条历史行、不切换为复合主键、不 Validate FK、不启用 TI-3 RLS。Router 从已鉴权 Principal 构造 scope；Store 首参必须为 TenantScope；所有 insert/update/delete 同时带 org/project。遗留全局键冲突失败关闭，不通过覆盖另一组织记录来“兼容”。

## 分波

### E2-A Object/Graph/Branch

- `obj_instance`、`graph_edge`、`meta_branch`、`obj_branch_overlay`、`funnel_status` 的业务 Store/Router 新写携带 scope。
- Object/Graph/Branch 的 update/delete 必须同时约束 scope；无 scope 的旧行不因任意租户 mutation 被认领。
- Marking 继承、Branch merge、Object Set 等内部调用必须透传同一 scope。
- Connector 自身的 Source/Pipeline/Job 属 TI-4；E2-A 只冻结其调用 Object runtime 时必须传 scope，不扩展具体平台代码。

### E2-B Draft/Wiki/Lifecycle

- `draft_dataset/wiki_page/wiki_page_version/object_lifecycle` 的全部读写统一 TenantScope。
- Wiki 当前虽有 scope 列，但旧 PK 仍全局；跨 scope 同 ID 冲突必须失败关闭，不能 UPDATE 改写 org/project。
- Draft approval/runtime write 事务内沿用 Principal scope，版本链必须同 scope。

### E2-C Aggregate/静态门

- 收口 Object/Graph/Branch/Draft/Wiki/Lifecycle 的全部 Router、工具运行时和后台调用签名。
- 静态测试禁止目标业务方法新增无参 `connect()`、只按对象 ID mutation、`org_id/project_id` 默认常量。
- 对仍属后续 TI-4/TI-5 的 Connector、Vector、Tool Runtime 建阻断清单，不在 E2 偷改范围。

## 兼容读策略

E2 的新写必须精确 scope；读取优先精确 scope。历史 NULL scope 行仅允许进入显式 shadow/audit 路径，不得作为任意租户正常结果返回。为维持测试组织既有演示数据，E3 必须先按证据完成归属回填后才能完成 E5 Read Switch；E2 回归不得以开放 NULL fallback 伪造 GREEN。

## 关键文件

| 分波 | 文件 |
|---|---|
| A | `branch_store.py`、`routers/ontology.py`、`routers/object_sets.py`、`routers/runtime_write.py`、`marking.py` 及相关 Object/Graph Store |
| B | `routers/drafts.py`、`routers/runtime_write.py`、`retention_jobs.py`、Wiki/Lifecycle 相关 Router/Store |
| C | `tool_runtime.py`、后台调用点、静态审计与 `tests/tenant_isolation/test_ti3_e2_*` |

## 退出门

1. E2-A/B/C 各自专项与跨 scope 负向门 GREEN。
2. 新增或修改的 9 资源写操作全部写入 Principal 的 org/project；跨 scope update/delete 为 404/0/403。
3. 历史 NULL 行计数不变，E2 不执行 UPDATE backfill。
4. 三张平台模板表继续共享，未被错误租户化。
5. Tenant Isolation 与 Object/Graph/Draft/Wiki 累计回归保持 GREEN；既有 OpenFGA seed 漂移单列，不得掩盖。
6. 五分支同步后进入 TI-3 E3 历史归属与隔离方案；具体商城仍暂停。

## E2-A 执行结果

- 代码功能提交 `f5f0b7c`，格式收口 `5cdafea`；五分支同步至 `5cdafea`。
- Graph/Funnel 新写显式写入 Principal scope；遗留全局键被另一 scope 重用时返回 409，不覆盖原归属。
- Branch/Overlay 新写继承 Principal scope；checkout/merge 的对象 mutation 和 overlay 清理同时约束 org/project。
- E2-A 专项 2 passed；Branch/Ontology/Funnel + Tenant Isolation 累计 185 passed、15 skipped。
- E2-A 未回填历史 NULL scope，读取全面切换仍留给 E2-C/E3/E5；下一波为 E2-B Draft/Wiki/Lifecycle。

## E2-B 执行结果

- 代码提交 `561148f`；`m1/w1/w2/w3/w4` 本地与远端同步至同一提交。
- Draft approval 读取、更新 `obj_instance` 及更新 Draft 状态均约束 Principal 的 org/project；遗留全局 Object 键被其他 scope 占用时返回 409，不接管原对象。
- Wiki upsert 只允许同 scope 更新；跨 scope 同键返回 409，事务回滚后原 Wiki、版本链和 Draft 状态均不变。
- Lifecycle 候选、归档、计数、HTTP Ops 与 CLI 全部要求显式 TenantScope；CLI 必须给出 `--org-id/--project-id`，不再隐式扫描全库。
- 内存 Insight key 扩展为 `(org_id, project_id, id)`，同一 Insight ID 可在不同 scope 独立存在，TTL 状态和候选互不可见。
- E2-B 专项 3 passed；Tenant Isolation + Draft/Object/Action/TTL 累计 137 passed、17 skipped。17 条 skip 为既有环境/历史条件门，不是本波断言失败。
- `decision_lineage` 的 631 条历史归属仍缺证据，按总方案保留给 TI-5，E2-B 不新增猜测回填或默认归属；下一波 E2-C 收口目标域全部读路径、内部调用签名与静态阻断门。

## E2-C 执行结果

- 代码提交 `5e58768`；五个代码分支与远端同步至同一提交。
- Object/Branch effective view、Object Set、Tool、Marking 继承、Graph neighbors/health、Funnel、Analytics 对象浏览均从 Principal 构造或显式接收 TenantScope。
- Branch Store 的 effective/list/diff/change-count 公共签名强制 scope；Branch 请求期不再执行 DDL，建表职责只属于迁移/启动阶段。
- Graph health 的实例、边、孤儿、悬空边与属性冲突全部在当前 scope 内聚合，跨租户对象不再影响健康分。
- Branch merge 对遗留全局 Object 键增加 rowcount 失败关闭，不能清理 overlay 后假报合并成功。
- 静态门扫描 8 个目标运行文件的 tenant-owned SQL，要求读写同时出现 org_id/project_id；并确认 TI-4 Connector/Vector/Scheduler 与 TI-5 `decision_lineage` 阻断项仍在资源注册表。
- E2-C 专项 2 passed；Object/Graph/Branch/Marking/Tool/Tenant Isolation 累计 144 passed、40 skipped、零失败。
- E2 全阶段未运行历史 DML，未认领 1,030 条历史行，未 Validate FK、未启用 RLS、未连接具体商城；下一门为 TI-3 E3 历史归属与隔离方案。

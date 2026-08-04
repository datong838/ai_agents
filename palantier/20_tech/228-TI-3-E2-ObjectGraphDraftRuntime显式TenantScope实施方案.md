# 228 · TI-3 E2 Object/Graph/Draft Runtime 显式 TenantScope 实施方案

> 版本：v1.0 · 2026-08-04
> 状态：连续执行授权下评审通过 / 待实施
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

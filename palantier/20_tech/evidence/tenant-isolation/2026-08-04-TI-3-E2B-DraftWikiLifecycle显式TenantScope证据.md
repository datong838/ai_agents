# 228 · TI-3 E2-B Draft/Wiki/Lifecycle 显式 TenantScope 证据

> 日期：2026-08-04
> 结论：GREEN
> 代码基线：`m1@561148f`

## 1. 实施范围

- Draft approval 的 Draft、Object、Wiki 与 Wiki version 写链沿用同一 Principal scope。
- `object_lifecycle` 候选、归档、计数、HTTP Ops 与 CLI 显式接收 TenantScope。
- 进程内 Insight Store 使用组织、工作区和 Insight ID 三元键。
- 本波不执行历史回填、复合主键切换、FK Validate、RLS 或具体商城连接。

## 2. 失败关闭证明

| 场景 | 结果 |
|---|---|
| B scope 审批与 A scope 同键 Wiki | 409；A 的 body/归属不变；B Draft 保持 proposed |
| B scope 审批与 A scope 同键 Object | 409；A 的 props/归属不变 |
| A/B scope 各自扫描 Retention 候选 | 各自只返回本 scope 对象 |
| Lifecycle 写入 | org/project 由调用 scope 写入；跨 scope 旧全局键不覆盖 |
| A/B scope 使用同一 Insight ID | 独立存储、独立读取、独立 TTL 状态 |
| Retention CLI 缺 scope | 参数解析失败关闭，不执行全库任务 |

## 3. 验证结果

- `test_ti3_e2b_draft_wiki_lifecycle_scope.py`：3 passed。
- E2-B 首轮专项（含 Retention、TTL、Wiki）：7 passed、2 skipped；2 条 Wiki skip 原因为既有测试夹具缺少 `meta_aip_kv`，不是功能断言失败。
- Tenant Isolation + Draft/Object/Action/Retention/TTL 累计：137 passed、17 skipped，零失败。
- Python 编译与 `git diff --check`：GREEN。

## 4. 数据与兼容性

- 未运行历史 DML，未认领 NULL scope 行。
- 未修改公共 Ontology 模板或 Module 模板数据。
- Wiki/Object/Lifecycle 仍受遗留全局主键限制；E2-B 的兼容策略是跨 scope 同键失败关闭，复合主键留给后续 Contract 波次。
- `decision_lineage` 历史 631 行无可靠归属，继续按 TI-5 隔离/取证路线处理，不在 E2-B 写入虚假默认租户。

## 5. 分支证据

`m1`、`feature/228-m3-w1-contract-types`、`feature/228-m3-w2-registry-contract`、`feature/228-m3-w3-openapi-contract`、`feature/228-m3-w4-operation-map` 已 fast-forward 并推送至 `561148f`。主工作树中的用户头条/掘金文档保持未暂存、未夹带。

## 6. 下一门

进入 TI-3 E2-C：收口 Object/Graph/Branch/Draft/Wiki/Lifecycle 的剩余读路径与内部调用，建立静态门，登记并阻断 TI-4/TI-5 后续资源，不开始具体微商城 Connector。

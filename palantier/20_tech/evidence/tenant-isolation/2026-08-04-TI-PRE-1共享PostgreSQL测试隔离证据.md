# TI-PRE-1 共享 PostgreSQL 测试隔离证据

> 日期：2026-08-04  
> 代码基线：`m1@0ae62bc`  
> 结论：**GREEN**。普通测试不再读写共享 `aos_meta`；每次 pytest 会话使用临时数据库并在结束后销毁。

## 1. 触发原因

TI-1 E3 扩大回归中，`test_enter_org_ok`、`test_invite_accept_by_outsider` 与 `test_delete_workspace_blocked_when_not_empty` 出现执行顺序相关失败。根因不是 E3 回填逻辑，而是：

1. TWA 测试使用固定组织、工作区和 subject；
2. `AOS_TWA_STORE=memory` 时，旧实现仍会把组织、工作区和成员写入共享 `meta_*` 表；
3. FastAPI 启动又从共享 PostgreSQL 重载进程内 Store；
4. 旧 autouse/teardown 使用固定 ID 或宽泛条件删除共享开发库数据；
5. OpenFGA 两个单测提交测试 tuple，持续增加 `authz_tuple` 残留。

## 2. 实施内容

- `tenant_catalog.persistence_enabled()` 将 `AOS_TWA_STORE=memory` 固化为真正的进程内边界；memory 模式不建表、不加载、不持久化或删除共享 `meta_*`。
- pytest session 默认创建 `aos_test_<随机后缀>` 临时数据库；先迁移到资产控制面基线，再初始化运行期兼容表，最后升级到唯一 head `228ti1e3exec`。
- 测试结束终止临时库连接并删除数据库；显式 `AOS_TEST_USE_SHARED_DATABASE=1` 才允许人工选择共享库。
- 删除 TWA 用例中针对共享 `aos_meta` 的固定/宽泛清理 SQL。
- OpenFGA 测试 tuple 改为同事务验证后 rollback。
- 增加 memory 边界专项测试，主动把数据库连接替换为失败函数，证明 memory mutation 和 boot 均不访问 PostgreSQL。

## 3. 验证结果

| 验证 | 结果 |
|---|---|
| 原失败组合 + memory 边界 | `17 passed` |
| authz/TWA 扩大回归 | `99 passed` |
| `tests/tenant_isolation` | `71 passed` |
| 共享库快照守卫 | `meta_org/meta_workspace/meta_membership/authz_tuple` 前后 count+内容 hash 完全一致 |
| 临时数据库清理 | 结束后 `aos_test_%` 数据库计数为 `0` |
| 迁移 | 临时库从 baseline 升至唯一 head `228ti1e3exec` |
| 代码格式 | `git diff --check` GREEN |

共享库最终守卫值（只记录数量和内容摘要，不记录业务正文）：

| 资源 | 行数 | MD5 摘要 |
|---|---:|---|
| `authz_tuple` | 8 | `cf75759cdf0898bb81801dada1e47d27` |
| `meta_membership` | 87 | `1ba2f08e70f5f420926efb4788b77e90` |
| `meta_org` | 16 | `5f76ffdb771be198ff16bd7036f8235b` |
| `meta_workspace` | 20 | `ece2c174bfffd1a0c28aceccf02affd0` |

上述摘要仅证明本波测试没有继续污染共享库，不代表 8/87/16/20 行均已完成租户归属。E3 的 59 条逻辑 QUARANTINE、历史连续性风险接受和 E4 BLOCKED 结论均保持不变。

## 4. 失败尝试与风险

- 首次临时库迁移直接执行 head，暴露 E1 migration 对运行期 `meta_workspace/twa_workspace` 前置表的隐式依赖；未修改历史 migration，而是在测试夹具中按真实部署顺序执行“资产基线 → 运行期兼容 schema → E1～E3”。
- 本波不会清理由历史测试已写入共享库的 8 条 authz tuple 或其他残留；它们继续由 E3 quarantine/后续可审计清理处理。
- CI/开发 PostgreSQL 账号需要 `CREATEDB` 权限。没有该权限时测试应失败关闭，由 CI 提供专用 test database；不得自动退回共享库。

## 5. 下一门

TI-PRE-1 解除“测试证据不可复现”阻断。下一步按总方案进入 TI-2 Module 与四应用闭环，先完成现状审计和 E1 Expand 方案，不自动执行历史回填，也不连接真实微商城。

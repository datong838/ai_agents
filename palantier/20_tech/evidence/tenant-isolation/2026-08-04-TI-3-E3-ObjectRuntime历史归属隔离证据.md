# 228 · TI-3 E3 Object Runtime 历史归属隔离证据

> 日期：2026-08-04
> 结论：GREEN
> 代码：`m1@21f8803`

## 1. 决策结果

九张目标业务表共 1,030 行：993 行已有完整 org/project 且工作区父记录存在，记为 `NO_ACTION/A`；37 行 scope 不可证明，记为 `QUARANTINE/X`；`ASSIGN=0`、`BLOCKED=0`。未知行分布为 Funnel 1、Graph 2、Branch 3、Object 31。

## 2. 不变性

- 未修改九张业务表的任何行，`businessRowsUpdated=0`。
- 37 行仅写入 append-only ownership/quarantine ledger，原业务行保留 NULL scope，并因 E2 读路径失败关闭而对正常租户不可见。
- 不把未知行归入测试组织或栖月汇，不创建假工作区、不删除数据。
- Alembic 保持 `228ti3e1expand`；FK 仍 NOT VALID；RLS 未开启；模板表未改。

## 3. 可逆演练

- 备份：`/private/var/tmp/aos-ti3-e3.ZH8MTl/aos-meta-before.dump`。
- 大小/权限：1,656,851 bytes / `-rw-------`。
- SHA256：`5ed0331c02b3181faabdd7dde17656945fe05479a05eb1626ea66c62cf108915`。
- 恢复库 batch：`75da9e3e-601e-590a-acb2-13487d2c636e`。
- plan/approve/apply/verify/rollback：全部 GREEN；verified=1,030、quarantine=37、业务 DML=0。
- 临时恢复数据库已删除；备份按审计需要保留在 Git 外。

## 4. 共享非生产最终执行

- batch：`7c82803d-1b18-5df0-9a52-46b8f831f376`。
- source snapshot：`efbc1fc768af789d7abf263b0d125217b89d7f6e9f5c083bc63c1dfc44e1fcde`。
- decision summary：`395b3f42f94deb80747c7c190682fef9ab99cf617279efa3c3bdb7558191ae55`。
- Planner、Approver、Executor、Verifier 使用不同 actor hash。
- apply/verify：GREEN；verified=1,030、quarantine=37、businessRowsUpdated=0。

## 5. 测试与分支

- `test_ti3_e3_object_runtime_ownership.py`：2 passed，覆盖零 ASSIGN、职责分离、零业务 DML、快照漂移整批阻断和 rollback。
- Tenant Isolation：109 passed、7 skipped、零失败。
- 五个代码分支及远端同步到 `21f8803`；用户头条/掘金文档未暂存、未夹带。

## 6. 下一门

进入 TI-3 E4：验证九个 workspace FK 前先证明 993 条非 NULL scope 零父断链；37 条 NULL scope 对 FK 合法但继续隔离。E4 不改变历史归属结论。

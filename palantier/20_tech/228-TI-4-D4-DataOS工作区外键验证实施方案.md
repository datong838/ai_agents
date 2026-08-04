# 228 · TI-4 D4 Data OS 工作区外键验证实施方案

> 版本：v1.0 · 2026-08-04
> 状态：评审授权链内，待执行
> 前置：TI-4 D3 GREEN；代码 `m1@78e16a7`；Alembic `228ti4d1expand`

## Rules

本波只把 D1 建立的 7 个 NOT VALID workspace FK 切为 validated。先证明全部非 NULL scope 均有 `twa_workspace` 父记录；保留 293 条 NULL 历史记录及 D3 逻辑隔离账本，不回填、不物理隔离、不启用 RLS、不改主键。

## 1. 目标约束

`meta_source`、`meta_pipeline`、`meta_dataset`、`meta_dataset_history`、`meta_sync`、`meta_schedule`、`phase5_pipeline_graph` 的 `fk_<table>_workspace_ti4d1`。

## 2. 迁移

- 新 revision：`228ti4d4validate`，down revision `228ti4d1expand`。
- upgrade：逐表 `VALIDATE CONSTRAINT`。
- downgrade：逐表 drop 后按原名重建 `NOT VALID` FK；不改变列、行和 D3 账本。
- 执行真实 `D1 → D4 → D1 → D4` 往返；每一步核对 297 行、293 条 NULL、293 条逻辑 quarantine 和非 NULL orphan=0。

## 3. 退出门

- 7/7 FK validated；downgrade 后 0/7，re-upgrade 后 7/7。
- 非 NULL orphan 始终为 0；297 行与逐表数量守恒。
- 293 条 NULL 和对应 D3 quarantine 守恒，不宣称其已归属。
- D4 专项、Tenant Isolation 累计 GREEN；五分支同 HEAD/tree；证据与上下文同步。

## 4. 后续边界

D4 后仍不能启用 tenant-scoped 全量读取：当前 `load_all/boot_data_os` 会把 293 条无 scope 数据放入全局内存 Map。下一门 D5 必须先按 Principal/TenantScope 切换读取与启动装载，并让 NULL/quarantine 记录默认不可见。

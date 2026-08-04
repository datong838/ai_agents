# 228 · TI-2 E4 Module 外键验证实施方案

> 版本：v1.0 · 2026-08-04
> 状态：执行中
> 前置：TI-2 E3 `8e57c8a` GREEN；共享非生产 parent 160、matched child 462 已有 module_pk

## Rules

先方案后代码；E4 只 Validate E1 已建立的 11 个 TI-2 FK；不新增/回填业务数据、不设 NOT NULL、不改 PK、不切读、不启用 RLS。先做逐约束反连接 precheck；失败时停止。downgrade 通过 drop/recreate 同名 NOT VALID FK 恢复 E3 元数据状态，不清理 E3 身份。

## 验证集合

- `fk_meta_module_installation_ti2`
- `fk_meta_module_active_overlay_ti2`
- 7 个 `fk_module_*_module_ti2`
- `fk_module_instance_overlay_module_ti2`
- `fk_module_user_view_preference_module_ti2`

两条 orphan `module_events` 的 module_pk 保持 NULL；PostgreSQL FK 对 NULL 不校验，因此它们继续由 quarantine 管理，不是伪造父记录的理由。

## 文件范围

| 文件 | 动作 |
|---|---|
| `alembic/versions/228ti2e4_validate_module_fks.py` | upgrade 逐项 VALIDATE；downgrade 精确重建 NOT VALID |
| `tenant_schema_lint.py` | 新增 E4 report：11 FK 全 validated，身份计数与 orphan 数正确 |
| `tests/tenant_isolation/test_ti2_e4_module_fk_validate.py` | revision、无 DML、升降级、负向 drift |

## 退出门

1. precheck 11 项 violation=0；identity parent=160、child=462、orphan null=2。
2. `228ti2e1expand → 228ti2e4validate → downgrade → upgrade` GREEN。
3. upgrade 后 11 FK `convalidated=true`；downgrade 后同名 FK 存在且 false。
4. 8 表行数与非身份 hash 不变；栖月汇 Module=0；RLS=0。
5. 租户/Module/Workshop 回归和五分支收口 GREEN。

E4 后进入 E5 Read Switch；APP-04/05 仍不得标绿。

# TI-2 E7 Module 复合主键与卸载 Contract 证据

## 结论

TI-2 E7 GREEN。代码提交 `4004170`，共享库最终 revision `228ti2e7contract`，五个代码分支同 HEAD。Module 实例身份已从兼容期收口为 TenantScope 复合 Contract，APP-04/05 完成。

## 数据与迁移证据

- 升级前：`meta_module=160`；Canvas/Deployment/Event/Interface/Query/Variable/Widget 为 `9/29/262/9/22/25/108`；新复合键重复均为 0。
- 历史异常：Event 仅 2 条 `module_pk IS NULL`，未删除、未伪造父记录。
- 备份：`/private/var/tmp/aos-ti2-e7.8C61V8/aos-meta-before.dump`，1,649,734 bytes，SHA-256 `85ed783417c0496ce407605a552f5725033c875f917c5beb90e393376d75f343`。
- 升级后：8 张活跃表均为组织/工作区复合主键；活跃空归属 0；隔离表 2 行；`aos_runtime` 无隔离表权限。
- 往返：降级至 E6 后 2 条 orphan 原样恢复、隔离表消失、旧主键恢复；再次升级后隔离表 2 行、活跃空归属 0。

## 应用证据

- APP-04：两个 TenantScope 使用相同 moduleId 与相同 child id，Module、Canvas、Interface、Widget、Variable、Query、Event 分别读回各自值。
- APP-05：GET 返回 ETag；无 `If-Match` 为 428，旧 ETag 为 412；admin/owner 正确 ETag 卸载后当前 scope 为 404，另一 scope 保持 200；Event 被停用，`obj_instance` 计数不变。
- Workshop 旧种子已按确定性 `module_pk` 和复合 conflict target 写入，不再依赖全局 ID。

## 验证

- E7 专项：4 passed。
- Tenant Isolation + Workshop：272 passed，3 skipped，7 warnings。
- 3 个 skip 仅针对 E3/E5 时代主动写入 NULL module_pk 的历史演练；E7 的 NOT NULL、隔离迁移和 runtime 无权限测试已覆盖其最终 Contract。
- Python compile、Ruff F/I、diff check：GREEN。

## 分支

`m1`、`feature/228-m3-w1-contract-types`、`feature/228-m3-w2-registry-contract`、`feature/228-m3-w3-openapi-contract`、`feature/228-m3-w4-operation-map` 均为 `4004170`，远端已推送。

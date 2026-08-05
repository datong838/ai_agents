# TI-5 C1 对象与向量 Namespace 证据

> 日期：2026-08-04
> 代码：`m1@bb0773c`
> 结论：GREEN；外部 Qdrant 保持 `EXTERNAL_BACKEND_UNVERIFIED`

## 1. 代码收口

- `file-object-store` Connector probe 由认证 Principal 构造完整 TenantScope，只允许列出 `tenant_key_prefix(scope)`。
- probe 缺少 `org_id` 或 `project_id` 时失败关闭，不再以空 prefix 扫描整个 bucket。
- local vector collection 继续使用 `org_id__project_id__logical_collection`，状态写入已受 A2 scoped KV、复合主键与 FORCE RLS 保护。

## 2. 数据盘点与可逆维护隔离

- MinIO bucket `aos-media` 操作前共 75 个对象：73 个位于 `dev-org/dev-project/`，栖月汇组织 prefix 为 0。
- 两个历史探针 `dev-probe.txt`、`dev-probes/aos-t42-probe.txt` 无可证明租户归属，未默认认领给测试组织或客户组织。
- Git 外本地备份：`/private/var/tmp/aos-ti5-c1-bzbep_4o`；目录权限 `0700`，文件与 manifest 权限 `0600`。
- `dev-probe.txt`：5 bytes，SHA-256 `ba9c736f19e7f60b7f6764adb0b7908c0a2b394e09b6c09863528c7f2bc86095`。
- `dev-probes/aos-t42-probe.txt`：13 bytes，SHA-256 `d7d45202cbba0c508fc2f9be4f3d1f8a1ac4e40829e6c73af7845510b8b91616`。
- 两个对象先复制到 `_maintenance/quarantine/unowned/<sha256>`，读回 hash 一致后才删除旧 key。操作后仍为 75 个对象：canonical 73、maintenance quarantine 2、栖月汇 0。
- 回滚可从本地备份或 maintenance key 恢复原 key，未删除 payload。

## 3. 验证结果

- `tests/tenant_isolation/test_ti5_c1_object_vector_namespace.py`：3 passed。
- 相关 Connector probe/runtime 回归：18 passed。
- local vector 共 1 条测试 KV，数据库 scope 为 `dev-org/dev-project`，collection 为 `dev-org__dev-project__demo-pipe-wo`；未发现无 scope 或栖月汇数据。
- Qdrant 未配置，因此只验证命名契约和本地实现，不把未连接的外部后端标成 GREEN。

## 4. 风险与下一门

- `_maintenance` 是管理员维护空间，租户 API、list 与 probe 必须持续不可见。
- 对象 adapter 的 raw-key 能力仅可用于受控维护逻辑，不得直接暴露给租户路由。
- 下一门 TI-5 C2 收口可变进程内 Singleton，首批为 AIP Model Catalog 与 Phase5 Dataset 链。

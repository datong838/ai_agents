# TI-6-3A 微商城本地 Readiness 证据

## 结论

TI-6-3A GREEN。代码 `f9f3917`，共享开发库 revision `228ti6edirectory`。栖月汇达到“本地微商城 Connector 开发准备”空基线，但生产部署门继续失败关闭。

## 目录与空基线

- `dev-org` 在 `twa_org/meta_org` 均显示“测试组织”，技术 ID 未变。
- `org-org/dev-project` 在权威 `twa_*` 与兼容 `meta_*` 均存在；本波只补 1 个权威工作区控制面投影，不复制成员、应用或业务数据。
- 栖月汇 BUSINESS_DATA=0、active Module=0、目标非 PostgreSQL item=0；控制面计数=3。
- `scripts/tenant_isolation_precheck.py` 新增 `ti6-microshop-readiness.json`，同时输出 local 与 production 两套结论。

## 双门结论

- `localDevelopmentReady=true`，`localBlockers=[]`。
- `productionDeploymentReady=false`。
- 生产 blocker：8 条 PostgreSQL 空 scope/未归属、3 个未知对象前缀、非表后端未配置/仅静态分析、TI-1 E4 历史 quarantine。
- 本结论只允许继续 synthetic 四模板/实例闭环，不允许连接真实微商城、凭据或客户数据。

## 可逆与验证

- 共享升级前备份 `/tmp/aos-ti6-3a-before.dump`。
- 独立恢复库完成 `6D→3A→6D→3A`，目录专项 4 passed；演练库已删除。
- Tenant Isolation 234 passed / 8 skipped；全量 9,228 collected；Ruff/diff check GREEN。
- 五工作树同线 `f9f3917`，tree `80a22faaea0a472861818a29d4cc8de98460973f`；四 Worker clean，主树 26 个用户文档改动未夹带。

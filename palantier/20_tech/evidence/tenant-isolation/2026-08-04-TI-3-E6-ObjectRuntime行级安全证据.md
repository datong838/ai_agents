# TI-3 E6 Object Runtime 行级安全证据

> 日期：2026-08-04  
> 结论：GREEN  
> 代码：`8dfa626`

## 实施结论

9 张 Object Runtime 工作区表复用 `aos_runtime`，每表一个 `FOR ALL` policy，同时包含 org/project 的 USING 与 WITH CHECK，并 ENABLE/FORCE RLS。没有新增角色体系、业务 DML、主键/NOT NULL 或 API 改动。

## 验证结果

| 门禁 | 结果 |
|---|---|
| Runtime role | NOLOGIN/NOSUPERUSER/NOBYPASSRLS，非表 owner |
| Policy / RLS | 9/9；ENABLE+FORCE 9/9 |
| 无 GUC | 9 表合计可见 0；写入拒绝 |
| 跨 scope | A 仅见 A；B 不见 A；伪造 B payload 被 WITH CHECK 拒绝 |
| Quarantine | NULL scope 在 runtime 不可见 |
| 可逆演练 | E4→E6→E4→E6 GREEN；降级 policy/RLS=0，最终 9/9 |
| 数据 | 1,030 行、37 quarantine、0 orphan；业务 DML=0 |
| 自动化 | 119 passed、7 skipped、零失败；lint/compile GREEN |

## 备份

`/private/var/tmp/aos-ti3-e6.QWSrwy/aos-meta-before.dump`，1,791,098 bytes，mode 600，SHA-256 `21f45853fe6cb7e891b7186c59b584c3efc848320ae6ac1aaa1bd6dc26ec84a7`。备份在 Git 外；客户/生产仍需独立审批和恢复演练。

## 边界

4 个 Connector writer 仍通过无 scope owner 路径，精确延后 TI-4；E6 不将它们冒充 RLS 保护对象，真实平台连接仍暂停。下一门为 TI-3 E7 Contract。

五分支与五远端同步至 `8dfa626`，tree `0a0dd922a0b114ecab84527c67e6ce34f707b9b4`；用户头条/掘金文档未夹带。

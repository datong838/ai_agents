# ADR-008：O1 权威写入、单一 Projector 与安装绑定组织 Overlay

> 状态：Accepted
> 日期：2026-08-09
> 适用范围：AOS 电商本体数字孪生层，目标租户 `org-org/dev-project`

## 背景

复审发现执行器直接写兼容本体表、事后补 Outbox、旧分支表承载组织定制等多真源问题。这会破坏重放、审计、租户隔离以及“平台模板与实例分离后仍可千人千面”的产品边界。

## 决策

1. `ecom_object/ecom_link` 是电商规范化对象与关系真源；同一事务写入权威 Outbox。
2. `ecom-projector-v1` 是电商 owned OT/Link 写入兼容 `obj_instance/graph_edge` 的唯一 actor；数据库 trigger 对其他 actor 失败关闭。
3. 平台模板、Installation 和组织定制 Overlay 三层分离。Overlay 必须绑定 Installation 与 TenantScope，采用不可变修订、强 ETag/CAS、Receipt 和 reset-to-inherit。
4. ObjectType/LinkType 的列表和单体读取统一执行模板 + Installation + 当前组织 Overlay 合成；前端不得自行维护第二套合成状态机。
5. Wiki、分析和图谱健康读取必须使用真实对象上下文并在服务端执行 PII 脱敏；页面不得以 Mock 或硬编码对象完成验收。

## 结果与取舍

- 获得可重放、可审计、可并发保护的单一写入链，以及按组织定制但不污染平台模板的“千人千面”。
- 兼容图成为可重建投影，不再是权威写入入口；旧 `obj_branch_overlay` 仅保留兼容读取/迁移边界，不承载新的组织定制。
- Installation/lock 不存在或 ETag 过期时写入失败关闭，牺牲部分宽松易用性以换取确定性和证据完整性。

## 验证

- 后端 O1/D5-E0 针对性回归：126 项通过。
- 前端：151 个测试文件、2007 项测试通过；TypeScript 全量检查通过。
- 内置浏览器：九页面 9/9 非空、目标租户正确、无页面级异常；权威图谱为 511 对象、590 边。
- D5 门禁仍独立判断：G17 当前 RED，本 ADR 的 Accepted 不等于 D5 总体 GREEN。

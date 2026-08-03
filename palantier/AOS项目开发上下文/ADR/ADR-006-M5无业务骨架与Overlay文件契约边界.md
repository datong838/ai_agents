# ADR-006：M5 无业务骨架与 Overlay 文件契约边界

> 状态：Accepted
> 日期：2026-08-04
> 实现进度：M5-0 已在 `aos-platform m1@4fd9c7f` GREEN

## 背景

M1～M4 已提供通用 Registry、Resolver、Composition、Installation、Evidence、API 与 UI/SDK。进入具体电商平台前，需要先证明这些能力能承载领域包组合，同时避免把测试坐标、客户数据或平台实现偷渡进通用内核。

## 决策

1. M5 只提交四个 unsigned、无业务实现的 Bundle source 骨架；三个叶子包只依赖 `domain.ecommerce.core`。
2. `platform.ecommerce.niushop` 仅是 test-only 架构坐标，不代表 Niushop 已接入。
3. InstanceOverlay 只冻结 strict synthetic JSON 文件契约；其外部 canonical hash 作为现有 Installation DTO 的 opaque `overlayRevision`。
4. M5 不新增 Overlay Store/API、生产 Router、数据库表、Connector、SQL、Mapping、Pipeline 或页面。
5. 后续签名私钥只在测试运行时生成；仓库不保存固定签名、私钥、真实 trust root 或客户引用。

## 结果

- 通用内核保持领域无关，不 import 或特判电商 Bundle。
- M5 可以沿用现有生产 Service/Store 做发布、解析、安装和回滚证明。
- 任何真实平台 schema、连接器或写回实现都必须在 M5 最终 GREEN 后单独评审，并在开始前暂停向用户汇报。

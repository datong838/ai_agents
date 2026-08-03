# 微信小店 AOS 对接方案

> 状态：**平台适配方案 v0.1 · capability 待核验 · 未开发**
> Bundle：`platform.ecommerce.wechat-shop`
> 关联产品方案：[新电商达人增长与控价任务产品方案](../228-新电商达人增长与控价任务产品方案.md)
> 注意：本目录的“微信小店”不是现有“微商城”SaaS/Niushop 接入，两者账号、数据源、API 和业务生态不同

## 0. 使用的 Rules

1. 微信小店只作为 PlatformAdapterPack，不进入 AOS 内核和通用电商本体。
2. 首先做 capability probe；只有官方/服务商文档、应用权限和沙箱实测共同确认后才冻结 API 清单。
3. 达人、联系方式、粉丝画像和订单数据按最小授权、marking、保留期和审计处理。
4. 首期只读/草稿；邀约、佣金、挂品、消息、退款等写操作等待 G6 和平台批准。
5. 不以 RPA 绕过接口权限、验证码、限流或平台规则。

## 1. 平台定位

微信小店是微信生态内的电商平台，达人合作重点围绕视频号/直播和优选联盟场景。AOS 首期目标不是复制微信小店后台，而是把授权数据映射为统一的 Shop/Product/Order/Creator/Commission 事实，并支持达人增长任务的发现、短名单、合作跟踪和效果复盘。

现有 `微商城电商接入方案/` 面向独立 SaaS 微商城与 Niushop，不得复用其平台身份或把微信小店写成一个 Niushop 渠道。

## 2. Bundle 所有权

`platform.ecommerce.wechat-shop` 包含：

- OAuth/服务商授权、token secret_ref、回调验签与 capability snapshot。
- 微信小店 shop/product/order/after-sale 等授权字段映射。
- 优选联盟/达人合作相关 capability 映射（以最终官方权限为准）。
- 平台枚举、分页、限流、幂等、错误和回执适配。
- Webhook/事件到统一事件的映射。
- 脱敏、marking、数据新鲜度和 Connector Evals。

不包含：

- 通用 Creator、Commission、GrowthPlan、AgentTask 定义。
- 达人评分、邀约策略、价格治理策略和六数字同事 Logic。
- 客户阈值、真实 app secret、达人联系方式或店铺数据。

## 3. 首期 capability probe

| 能力域 | 需要核验 | 未确认时降级 |
|---|---|---|
| 店铺/授权 | 商家、服务商、应用关系与 token 生命周期 | 人工配置 capability snapshot |
| 商品 | 商品、SKU、状态、价格、佣金/跟佣信息 | CSV/受控人工导入 |
| 订单/售后 | 增量、回调、买家标识、退款状态 | 只读定时导入 |
| 达人发现 | 搜索范围、筛选字段、分页、画像聚合 | 平台后台人工导出/录入 |
| 达人合作 | 邀请、状态、合作商品、有效期 | 只生成任务与草稿，不自动发送 |
| 佣金 | 通用/定向佣金、结算、退款回退 | 人工录入并标记来源 |
| 直播/效果 | 开播、场次、GMV、订单、转化 | unavailable，不以 0 代替 |
| 消息/联系 | 平台内联系能力、频控、回执 | 人工平台内操作 |
| 价格 | 店内价格构成、优惠、活动信息 | 公开/人工证据，明确口径 |

每项 capability 记录 `status/source/permission/verifiedAt/expiresAt/rateLimit/readWrite/evidenceRef`。不写死会议中的“API 友好”为 GREEN。

## 4. Ontology 映射

复用 `domain.ecommerce.core` 及增长解决方案模型：

| 微信小店事实 | 统一模型 |
|---|---|
| 店铺 | `Shop` |
| 商品/规格 | `Product` / `ProductSku` |
| 订单/订单行/售后 | `Order` / `OrderLine` / 后续 `Refund` |
| 达人/视频号主体 | `Creator` + 平台 identity |
| 达人合作 | `CreatorCollaborationCase` |
| 商品佣金/结算 | `Commission` |
| 直播场次 | `LiveSession`（在相应领域版本可用后） |

微信昵称、视频号、达人 ID、微信号、手机号不能互相猜测为同一人。跨平台身份合并必须有可审计 evidence link。

## 5. 达人增长任务映射

```text
CreatorDiscoveryBrief
 → WeChatShop creator capability/manual import
 → CandidateSnapshot
 → dedupe + score
 → CreatorShortlistRevision
 → approval
 → outreach draft
 → 人工/受控平台邀请
 → collaboration case
 → 商品、佣金、直播、订单效果回读
```

首期重点支持：

- KOC/腰部/头部分层，而非单一粉丝阈值。
- 粉丝数量、活跃/开播、受众年龄、品类、佣金和风险条件的可用性标记。
- 邀请中、已接受、已拒绝、已过期、合作中、已结束等平台状态映射。
- 合作商品、佣金、直播/订单/退款效果的证据化复盘。

受众年龄等画像只有在平台授权、聚合并满足隐私阈值时才能用于筛选。

## 6. 价格治理映射

微信小店 Connector 提供授权商品、SKU、标价、活动/优惠和店铺事实；跨平台低价识别由 `solution.ecommerce.growth` 统一任务处理。平台包不判断“违规”，只提供可验证事实与价格构成。

## 7. 安全与合规

- token、app secret、回调密钥只存 secret_ref，不进入 Bundle、日志或任务 Artifact。
- 买家、达人和联系人标识按字段分级；展示、导出和保留需单独权限。
- 达人搜索、邀请和消息受平台频控与用途限制；禁止批量骚扰。
- 未获得写权限时 UI 必须显示“人工执行”，不能以浏览器自动化伪装成功。
- 所有邀请、佣金、挂品、退款及消息操作都需要 G6 ActionProposal、批准、幂等、回执和 kill switch。

## 8. 实施分波

### WX0：官方能力与资质核验

- 官方/服务商文档、应用类型、权限申请、沙箱、限流和回调核验。
- 输出 capability matrix 和最小脱敏响应样例。

### WX1：只读 Connector

- shop/product/order/after-sale 及可用达人/合作只读同步。
- 字段映射、增量、回调、错误、数据新鲜度和双租户测试。

### WX2：达人任务接入

- 候选、去重、评分、短名单、人工批准、合作状态和绩效回读。
- 不发送自动邀约。

### WX3：受控写操作

- 仅在 G6 与平台权限完成后实现邀请、佣金/合作商品等明确获准 action。
- 每项 action 独立 flag、频控、幂等、回执、补偿和人工接管。

## 9. 退出门

- capability matrix 的每个 GREEN 能力都有官方来源、权限和实测证据。
- 与微商城/Niushop 边界无混淆，内核不 import 微信小店实现。
- 两租户、token 轮换、回调重放、限流、撤权和数据删除测试通过。
- API 缺失时真实显示 manual/unavailable，不伪造结果。
- 达人增长只读闭环可刷新回读，联系方式与画像访问受控。
- 写操作在 G6 前不可达。

## 10. 当前下一步

先完成 WX0，不直接写 Connector。WX0 需要客户提供应用/服务商身份、可申请权限截图或官方文档入口、脱敏响应样例和一个测试店铺；完成后再冻结 `01-微信小店API能力清单.md`。

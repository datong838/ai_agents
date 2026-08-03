# 微信小店 API 能力清单

> 状态：**WX0 文档核验完成 · YELLOW · 客户账号实测待完成 · 未开发**
> 核验日期：2026-08-03
> 适配包：`platform.ecommerce.wechat-shop`
> 上位方案：[00-微信小店AOS对接方案](00-微信小店AOS对接方案.md)

## 0. 使用的 Rules

1. 只把微信/腾讯官方文档明确描述的接口标记为 `DOC_VERIFIED`；会议口述、第三方文章和后台截图不能替代官方证据。
2. `DOC_VERIFIED` 不等于客户可调用；未用授权测试店铺完成最小请求前一律同时标记 `ACCOUNT_REQUIRED`。
3. 达人联系方式、受众画像和订单身份数据按最小授权、脱敏、保留期与审计处理，凭据只能进入 secret manager。
4. 首轮实测只允许读操作；邀请、消息、佣金、挂品、退款和黑名单等写操作继续受 G6 门禁。
5. 找不到官方接口时标记 `MANUAL` 或 `UNVERIFIED`，不得用 RPA、抓包或绕过平台限制伪装为开放能力。

## 1. 状态词典与 WX0 结论

| 状态 | 含义 |
|---|---|
| `DOC_VERIFIED` | 已核对官方文档、接口路径、请求方向和主要字段 |
| `ACCOUNT_REQUIRED` | 官方文档存在，但客户账号、权限集、联盟开通状态和真实响应尚未验证 |
| `LIVE_VERIFIED` | 已用授权测试店铺完成脱敏实测并保存 evidence；本轮尚无此状态 |
| `MANUAL` | 当前只能通过平台后台、受控导入或人工操作完成 |
| `UNVERIFIED` | 尚无足够官方证据证明存在所需能力 |
| `FORBIDDEN` | 因安全、合规或范围约束不得实现 |

WX0 已完成官方文档层面的能力盘点，但尚未取得客户测试店铺、应用身份和权限证据，因此整体保持 **YELLOW**，不能进入 Connector 编码。当前官方能力足以支撑“商家已有带货者同步、已知达人补全、商品/订单/售后和部分效果复盘”的只读实测，不足以宣称已经支持“全平台达人发现、按粉丝画像筛选、读取联系方式或自动邀约”。

## 2. 官方接口证据台账

| 能力 | 官方接口 | 关键权限/语义 | 当前状态 |
|---|---|---|---|
| 稳定 token | `POST /cgi-bin/stable_token` | 获取稳定接口调用凭证；密钥不得进入文档和日志 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 店铺基本信息 | `POST /channels/ec/basics/info/get` | 读取授权微信小店基本信息 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 商品列表 | `POST /channels/ec/product/list/get` | 商品分页与状态事实 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 商品详情 | `POST /channels/ec/product/get` | 商品/SKU/价格等详情 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 订单列表 | `POST /channels/ec/order/list/get` | 订单分页读取；包含潜在个人信息 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 订单详情 | `POST /channels/ec/order/get` | 单订单详情；需字段级 marking | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 售后列表 | `POST /channels/ec/aftersale/getaftersalelist` | 售后/退款状态读取 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 商家带货者列表 | `POST /channels/ec/league/promoter/list/get` | 权限集 141；返回商家已有带货者，`page_size <= 20` | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 带货者详情 | `POST /channels/ec/league/promoter/get` | 权限集 141；用 `talent_appid` 或 `finder_id` 查询已知达人 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 带货者商品数据 | `POST /channels/ec/league/talent/getproductdatalist` | 权限集 141；近 30 日商品成交/订单及佣金比例 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 商品推广带货者 | `POST /channels/ec/league/promotion/talent/list` | 权限集 141；按商品与推广计划读取带货者，不是全平台发现 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 编辑带货者 | `POST /channels/ec/league/talent/update` | 权限集 141；官方语义仅拉黑/取消拉黑 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` + G6 |
| 联盟商品列表 | `POST /channels/ec/league/item/list/get` | 读取联盟商品/计划事实 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 罗盘达人商品数据 | `POST /channels/ec/compass/shop/finder/product/list/get` | 服务商权限集 175；按视频号/达人主体读取商品成交事实 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 橱窗商品详情 | `POST /channels/ec/window/product/get` | 服务商权限集 133 或 177；价格、销量、库存、CPS 计划等事实 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 文件下载 URL | `POST /channels/ec/open/get_download_url` | 获取平台文件下载地址 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 消息推送 | 微信小店消息推送配置 | 已确认官方消息推送入口；事件类型、验签和重放仍需逐项实测 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |

### 2.1 官方来源

- [获取稳定版接口调用凭据](https://developers.weixin.qq.com/doc/store/shop/API/apimgnt/common/api_getstableaccesstoken.html)
- [获取店铺基本信息](https://developers.weixin.qq.com/doc/store/shop/API/storemanage/api_mmecapi_basicinfo.html)
- [获取商品列表](https://developers.weixin.qq.com/doc/store/shop/API/channels-shop-product/shop/api_getproductlist.html) / [获取商品](https://developers.weixin.qq.com/doc/store/API/product/get.html)
- [获取订单列表](https://developers.weixin.qq.com/doc/store/shop/API/channels-shop-order/api_getorderlist.html) / [获取订单](https://developers.weixin.qq.com/doc/store/shop/API/channels-shop-order/api_getorder.html)
- [获取售后单列表](https://developers.weixin.qq.com/doc/store/shop/API/channels-shop-aftersale/aftersale/api_getaftersalelist.html)
- [获取带货者列表](https://developers.weixin.qq.com/doc/store/shop/API/league/promoter/api_getpromoterlist.html) / [获取带货者详情](https://developers.weixin.qq.com/doc/store/shop/API/league/promoter/api_getpromoter.html)
- [获取带货者商品数据](https://developers.weixin.qq.com/doc/store/shop/API/league/promoter/api_gettalentproductdata.html) / [编辑带货者](https://developers.weixin.qq.com/doc/store/shop/API/league/promoter/api_updatetalent.html)
- [获取联盟商品列表](https://developers.weixin.qq.com/doc/store/shop/API/league/item/api_getitemlist.html) / [获取商品推广带货者列表](https://developers.weixin.qq.com/doc/store/shop/API/league/item/api_listspupromotiontalents.html)
- [获取罗盘达人商品列表](https://developers.weixin.qq.com/doc/store/shop/API/compass/api_getshopfinderproductlist.html)
- [获取橱窗商品](https://developers.weixin.qq.com/doc/channels/API/windowproduct/get.html)
- [获取文件下载链接](https://developers.weixin.qq.com/doc/store/API/miniandstore/get_download_url.html) / [微信小店消息推送](https://developers.weixin.qq.com/doc/store/shop/dev_before/message_push.html)

## 3. 达人增长 capability 矩阵

| 任务能力 | 官方证据结论 | AOS 首期处理 | 状态 |
|---|---|---|---|
| 同步商家已有带货者 | 官方列表接口存在；语义是“商家带货者列表” | 进入 `CreatorCandidateSnapshot`，保留平台 ID 与来源 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 补全已知达人 | 可用 `talent_appid` 或 `finder_id` 获取昵称、头像、等级、成交/订单等部分事实 | 由人工导入、平台后台导出或既有合作记录提供种子 ID | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 查看达人商品表现 | 可读近 30 日商品成交、订单、佣金类型和比例 | 进入 `CreatorPerformanceReview`，保留时间窗口 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 查看推广计划达人 | 可按商品和推广计划读取带货者 | 用于既有计划复盘，不解释为全网候选池 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED` |
| 全平台达人广场搜索 | 当前官方证据未发现任意候选池搜索接口 | 平台后台人工筛选/受控导入 | `UNVERIFIED` / `MANUAL` |
| 按粉丝数筛选 | 已核验响应未证明提供粉丝数字段 | 显示 `unavailable`，不得以等级推算粉丝数 | `UNVERIFIED` |
| 按 50 岁以上受众筛选 | 已核验响应未证明提供受众年龄分布 | 仅接受平台授权聚合报表或人工 evidence | `UNVERIFIED` |
| 按开播率筛选 | 已核验响应未证明提供开播率/开播场次 | 只可使用另有合法来源且带统计窗口的事实 | `UNVERIFIED` |
| 手机号/微信号 | 已核验响应未提供联系方式 | 不采集、不猜测、不跨平台拼接 | `UNVERIFIED`，敏感 |
| 自动发送邀约/消息 | 当前官方证据未发现相应开放接口 | 只生成草稿和人工任务 | `UNVERIFIED` / `MANUAL`，G6 |
| 配置佣金/挂品 | 已确认可读部分佣金事实，未完成相应写接口核验 | 只读展示；写操作不可达 | `UNVERIFIED`，G6 |
| 拉黑/取消拉黑 | 官方 `talent/update` 仅确认这两类写操作 | WX0/WX1 不调用；以后单独风险评审 | `DOC_VERIFIED` + `ACCOUNT_REQUIRED`，G6 |

关键约束：`promoter/list/get` 不能被命名为“达人发现 API”；`promoter/get` 需要已知标识，适合候选补全而不是无种子搜索。UI 和任务结果必须把候选来源标成 `merchant_promoter`、`promotion_plan`、`manual_import` 或其他真实来源。

## 4. 统一模型与字段分级

| 微信小店事实 | 建议映射 | 数据分级/约束 |
|---|---|---|
| 店铺主体与状态 | `Shop` | 租户隔离；授权关系不可跨租户复用 |
| 商品、SKU、价格、库存 | `Product` / `ProductSku` | 价格需保留币种、口径与采集时间 |
| 订单、订单行、售后 | `Order` / `OrderLine` / `Refund` | 买家、收货与售后信息按 PII 标记和最小展示 |
| `talent_appid`、`finder_id` | `CreatorPlatformIdentity` | 平台标识不是手机号/微信号，不自动跨平台合并 |
| 昵称、头像、联盟等级、黑名单状态 | `CreatorCandidateSnapshot` | 快照带来源、`observedAt` 与可见范围 |
| GMV、订单数、商品数 | `CreatorPerformanceReview` | 保留 30 日/累计等统计窗口，不混口径 |
| 佣金类型、佣金比例 | `Commission` 事实 | 比例按官方精度换算，保留原始值和计划类型 |

## 5. 客户账号实测前置清单

客户或实施方需要通过受控渠道提供以下证据；不得把 secret 发到聊天或 Markdown：

1. 接入身份：商家自研应用或第三方服务商，以及对应 AppID/授权链路说明。
2. 一个非生产或低风险测试店铺，并确认已经开通优选联盟；未开通时官方可能返回 `10023007`。
3. 应用权限集截图或导出，至少核对 141；如使用罗盘/橱窗能力，再核对 175、133/177。
4. secret manager 中的测试凭据引用、token 获取责任方、轮换与撤权流程。
5. 一组已知 `talent_appid` 或 `finder_id`、测试商品、测试推广计划，避免无目标扫描。
6. 回调地址、验签配置、允许的事件类型，以及一份脱敏回调样例。
7. 达人身份、订单 PII 的用途、可见角色、保留期、删除和导出政策。

## 6. 最小只读实测计划

| 顺序 | 实测 | 成功证据 | 禁止事项 |
|---|---|---|---|
| 1 | 获取/轮换测试 token | 状态码、scope、过期时间、secret_ref；响应脱敏 | 不记录 secret/token 原值 |
| 2 | 读取店铺基本信息 | 店铺身份与租户绑定 evidence | 不接生产店铺写权限 |
| 3 | 商品列表 → 商品详情 | 分页、状态、SKU/价格字段和限流 | 不更新商品 |
| 4 | 订单列表 → 订单详情 → 售后列表 | 时间游标、增量、PII marking、退款状态 | 不发货、不退款 |
| 5 | 商家带货者列表 → 已知达人详情 | 分页、字段缺失语义、错误码和联盟状态 | 不扫描未知达人 |
| 6 | 达人商品数据 → 推广计划达人 → 罗盘数据 | 统计窗口、佣金精度、商品关联 | 不把缺失字段填 0 |
| 7 | 回调验签与重放 | 签名、幂等、乱序、重复和撤权处理证据 | 不触发业务写动作 |

每次调用记录 `tenantId/capability/permissionSet/requestShape/statusCode/rateLimit/fieldPresence/verifiedAt/evidenceRef`；请求和响应必须脱敏。实测过程中若发现账号类型或字段与官方文档不一致，降级为 `ACCOUNT_REQUIRED`，不以猜测补齐。

## 7. WX0 退出门

只有以下条件同时满足，WX0 才能由 YELLOW 转 GREEN 并允许起草 WX1 Connector 编码方案：

- 客户接入身份、测试店铺、优选联盟状态和权限集证据齐全。
- 最小只读实测 1～7 完成，保存脱敏响应、限流、错误和回调证据。
- 每个拟进入 WX1 的 capability 都达到 `LIVE_VERIFIED`；其余明确降级为 `MANUAL` 或 `UNAVAILABLE`。
- 字段映射、PII marking、保留期、撤权和删除策略经过安全评审。
- 明确接受首期不能通过官方 API 完成全平台达人发现和自动邀约，或另行提供可核验的官方能力证据。
- 未修改 AOS 内核、未新增写操作，且 G6 前写路径仍不可达。

## 8. 下一步

当前下一步不是编码，而是由客户/实施方补齐第 5 节材料，并按第 6 节完成授权测试店铺的只读实测。实测通过后更新本清单状态与 evidenceRef，再形成 WX1 只读 Connector 实施方案；不得直接从 `DOC_VERIFIED` 跳到开发完成。

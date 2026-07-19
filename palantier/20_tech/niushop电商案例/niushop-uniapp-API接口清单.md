# Niushop ↔ UniApp（栖月汇）API 接口清单

> **依据**  
> - 服务端：`niushop/app/api/controller/*` + `niushop/addon/*/api/controller/*`  
> - 使用方：`uniapp/`（主工程；统一经 `uniapp/common/js/http.js` → `$api.sendRequest`）  
> - 扫描结果：服务端约 **341** 个 action；uniapp 源码引用约 **315** 条路径（含插件前缀）  
> **范围**：以 **uniapp 实际调用** 为主；服务端有但前端未用的接口见附录 B。  
> **关联文档**：`docs/niushop-数据表与核心对象关系.md`

---

## 1. 调用约定（必读）

### 1.1 URL 形态

```
最终 URL = Config.baseUrl + params.url
```

| 端 | baseUrl | 示例 |
|----|---------|------|
| 微信小程序 | `https://yanpanji.com`（见 `uniapp/common/js/config.js`） | `https://yanpanji.com/api/goodssku/detail` |
| H5 | `''`（同源相对路径） | `/api/goodssku/detail` |

路径风格（ThinkPHP）：

| 类型 | 格式 | 示例 |
|------|------|------|
| 核心 API | `/api/{controller}/{action}` | `/api/order/detail` |
| 插件 API | `/{addon}/api/{controller}/{action}` | `/coupon/api/coupon/receive` |

控制器/方法名 **不区分大小写**（服务端路由会归一）；文档统一小写。

### 1.2 HTTP Method

`http.js` 约定：

```text
传了 data（含 data: {}）→ POST
未传 data → GET
```

业务几乎全部为 **POST**（`application/x-www-form-urlencoded`）。

### 1.3 公共参数（每次自动合并）

| 字段 | 来源 | 说明 |
|------|------|------|
| `app_type` | 编译端 | `weapp` / `h5` / `wechat` / `aliapp` 等 |
| `app_type_name` | 编译端 | 中文名 |
| `token` | `store.state.token` | 会员登录态；需登录接口必填有效值 |
| `store_id` | 默认门店 / 全局门店 | 有则带上 |

**不传 `site_id`**：服务端 `BaseApi` 用 `request()->siteid()` 注入。

### 1.4 公共 Header

| Header | 条件 | 作用 |
|--------|------|------|
| `content-type` | 固定 | `application/x-www-form-urlencoded;application/json` |
| `X-App-Id` | `Config.appid` 有值 | 小程序 AppId |
| `X-Weapp-Id` | `Config.weapp_id > 0` | 多小程序端 id（init 后写入） |

服务端 `WeappContext` 据此解析 `weapp_id`；**交易类**（如 `Ordercreate`）在 `app_type=weapp` 时要求能解析出端。

### 1.5 栖月汇额外注入（http.js）

| 场景 | 自动附加字段 |
|------|----------------|
| 登录/注册相关 URL | `source_member`、`_qyh_sm_trace` |
| `/api/goodssku/*`、`/api/cart/*` | `source_member` |
| `/api/goodssku/*` | `share_member`（及 detail 的 `_share_member_debug`） |
| `/api/ordercreate/*` | `share_member`、`_share_member_debug` |

### 1.6 鉴权

- 服务端：`$this->checkToken()` 通过则填充 `$this->member_id`。  
- 下表 **需登录** 列：`Y` = 控制器内显式 `checkToken`；`N` = 可不登录；`?` = 视业务（有 token 更好）。

### 1.7 统一响应形态

```json
{ "code": 0, "message": "…", "data": { } }
```

`code < 0` 为失败；登录失效等由前端 `http.js` 统一处理跳转。

---

## 2. 核心交易主路径（最常用）

```text
config/init
  → login/auth 或 tripartite/mobileauth（得 token）
  → goodssku/detail + cart/*
  → ordercreate/payment → calculate → create（得 out_trade_no）
  → pay/info → pay/type → pay/pay → pay/status
  → order/lists | order/detail
```

创单三板斧公共大字段见 **§4.7**。

---

## 3. 配置 / DIY / 站点 / 门店

| 路径 | 需登录 | 必要/关键参数 | 说明 |
|------|--------|----------------|------|
| `/api/config/init` | N | （公共字段即可） | 启动：主题、默认门店、**回写 weapp_id** |
| `/api/config/getCaptchaConfig` | N | — | 验证码开关 |
| `/api/config/getApiConfig` | N | — | 上传等 API 配置 |
| `/api/config/geMapConfig` | N | — | 地图 key（前端拼写 geMap） |
| `/api/config/promotionZoneConfig` | N | `name` | 营销专区 |
| `/api/diyview/info` | N | `id` 或 `name`；可选 `weapp_id` | DIY 页面 |
| `/api/site/status` | N | — | 站点开关 |
| `/api/site/shopcontact` | N | — | 客服联系方式 |
| `/api/adv/detail` | N | `keyword` | 广告位 |
| `/api/notice/page` | N | `page`,`page_size` | 公告列表 |
| `/api/notice/info` | N | `id` | 公告详情 |
| `/api/article/category` | N | — | 文章分类 |
| `/api/article/page` | N | `page`,`page_size`；可选 `category_id` | 文章分页 |
| `/api/article/lists` | N | 可选 `category_id`,`num` | 文章列表 |
| `/api/article/info` | N | `article_id` | 文章详情 |
| `/api/helpclass/lists` | N | — | 帮助分类 |
| `/api/help/info` | N | `id` | 帮助详情 |
| `/api/captcha/captcha` | N | — | 图形验证码 |
| `/api/store/info` | N | `store_id`；可选经纬度 | 门店详情 |
| `/api/store/page` | N | 可选 `keyword`,`store_ids`,经纬度 | 门店列表 |
| `/api/store/getStorePage` | N | `page`,`page_size`；可选经纬度/`type`/`store_ids` | 分页门店 |
| `/api/store/nearestStore` | N | `latitude`,`longitude` | 最近门店 |
| `/api/store/getLocation` | N | `latitude`,`longitude` | 定位辅助 |
| `/store/api/config/config` | N | — | 门店插件配置 |
| `/store/api/store/labelPage` | N | — | 门店标签 |

---

## 4. 登录 / 注册 / 三方

| 路径 | 需登录 | 必要/关键参数 | 说明 |
|------|--------|----------------|------|
| `/api/login/auth` | N | 授权字段（如 `code`/`weapp_openid` 等，随端）；可选 `source_member` | 授权登录（可注册） |
| `/api/login/authonlylogin` | N | 同授权字段 | 仅登录不注册 |
| `/api/login/login` | N | 账号密码类字段 | 账号登录 |
| `/api/login/mobile` | N | `mobile`,`code`,`key` | 手机验证码登录 |
| `/api/login/mobileCode` | N | 手机号/图形验证相关 | 发登录短信 |
| `/api/register/config` | N | — | 注册开关 |
| `/api/register/aggrement` | N | `type` | 协议 |
| `/api/register/mobile` | N | `mobile`,`code` 等 | 手机注册 |
| `/api/register/mobileCode` | N | — | 注册短信 |
| `/api/register/username` | N | 用户名密码等 | 用户名注册 |
| `/api/tripartite/mobileauth` | N | 手机授权相关；可选 `source_member` | 绑定手机并登录 |
| `/api/tripartite/mobile` | N | `mobile` | 三方绑手机 |
| `/api/tripartite/mobileCode` | N | — | 发码 |
| `/api/tripartite/getPhoneNumber` | N | 微信 `code` 等 | 小程序取号 |
| `/api/findpassword/mobile` | N | 手机+验证码+新密码 | 找回密码 |
| `/api/findpassword/mobilecode` | N | — | 找回短信 |
| `/weapp/api/weapp/authcodetoopenid` | N | `code` | code→openid |
| `/weapp/api/weapp/messagetmplids` | N | — | 订阅消息模板 |
| `/weapp/api/weapp/share` | N | 分享场景参数 | 小程序分享图/配置 |
| `/wechat/api/wechat/authcode` | N | — | 公众号授权 |
| `/wechat/api/wechat/authcodetoopenid` | N | `code` | 公众号 openid |
| `/wechat/api/wechat/jssdkconfig` | N | url 等 | JSSDK |
| `/wechat/api/wechat/share` | N | — | 公众号分享 |
| `/wechat/api/wechat/followqrcode` | N | — | 关注二维码 |
| `/aliapp/api/aliapp/authcodetouserid` | N | — | 支付宝 |
| `/aliapp/api/aliapp/messagetmplids` | N | — | 支付宝订阅 |
| `/memberregister/api/Config/Config` | N | — | 注册有礼 |

成功登录响应核心：`data.token`（后续所有需登录接口携带）。

---

## 5. 会员 / 账户 / 店铺 / 超级卡

| 路径 | 需登录 | 必要/关键参数 | 说明 |
|------|--------|----------------|------|
| `/api/member/info` | Y | — | 会员资料 |
| `/api/member/modifynickname` | Y | `nickname` | |
| `/api/member/modifyheadimg` | Y | `headimg` | |
| `/api/member/modifyusername` | Y | `username` | |
| `/api/member/modifyrealname` | Y | `realname` | |
| `/api/member/modifysex` | Y | `sex` | |
| `/api/member/modifybirthday` | Y | `birthday` | |
| `/api/member/modifyaddress` | Y | 地址字段 | |
| `/api/member/modifymobile` | Y | `mobile`,`code` | |
| `/api/member/modifypassword` | Y | `old_password`,`new_password` | |
| `/api/member/modifypaypassword` | Y | `code` 等 | 支付密码 |
| `/api/member/checkmobile` | Y | `mobile` | |
| `/api/member/bindmobliecode` | Y | — | 绑定手机短信（拼写历史遗留） |
| `/api/member/pwdmobliecode` | Y | — | 改密短信 |
| `/api/member/mobileauth` | Y | `mobile` | |
| `/api/member/paypwdcode` | Y | — | 支付密码验证码 |
| `/api/member/verifypaypwdcode` | Y | `code` | |
| `/api/member/membereqrcode` | Y | — | 会员码 |
| `/api/member/accountrule` | ? | — | 成长值规则 |
| `/api/Member/alterShareRelation` | Y | 分享关系参数 | 改分享关系 |
| `/api/member/logShareBind` | Y | `sharer_member_id`；可选 `from_page`,`goods_id`,`share_path`,`share_type` | 分享绑定日志 |
| `/api/memberlevel/lists` | N | — | 等级列表 |
| `/api/memberaccount/info` | Y | `account_type` | 账户概要 |
| `/api/memberaccount/point` | Y | — | 积分 |
| `/api/memberaccount/page` | Y | `page`,`page_size`；可选 `account_type`,`from_type` | 流水 |
| `/api/memberaccount/sum` | Y | — | 汇总 |
| `/api/memberaccount/fromType` | Y | — | 流水类型 |
| `/api/memberaccount/monthData` | Y | — | 按月 |
| `/api/memberaccount/usablebalance` | Y | — | 可用余额 |
| `/api/membersignin/getSignStatus` | Y | — | 签到状态 |
| `/api/membersignin/award` | Y | — | 奖励说明 |
| `/api/membersignin/issign` | Y | — | 是否已签 |
| `/api/membersignin/signin` | Y | — | 签到 |
| `/api/membershop/shopTitle` | Y | 可选 `member_id` | 本人店铺标题 |
| `/api/membershop/customerList` | Y | `page`,`page_size` | 客户列表 |
| `/api/membershop/commissionIncome` | Y | `page`,`page_size` | 分润收入 |
| `/api/membershop/commissionWxConfirmPackage` | Y | `id`/`commission_log_id`；可选 `income_type` | 微信确认收款包 |
| `/api/membershop/qrcode` | Y | 可选 `member_id`,`weapp_id`,`env_version`,`width` | 店铺码 |
| `/api/membernotice/page` | Y | `page`,`page_size` | 站内信 |
| `/api/membernotice/info` | Y | `id` | |
| `/api/memberwithdraw/config` | Y | — | 提现配置 |
| `/api/memberwithdraw/info` | Y | — | |
| `/api/memberwithdraw/apply` | Y | `apply_money`,`transfer_type`；账户类字段 | 申请提现 |
| `/api/memberwithdraw/page` | Y | `page`,`page_size` | |
| `/api/memberwithdraw/detail` | Y | `id` | |
| `/api/memberwithdraw/transferType` | Y | — | 转账方式 |
| `/api/memberbankaccount/page` | Y | `page`,`page_size` | 提现账户 |
| `/api/memberbankaccount/info` | Y | `id` | |
| `/api/memberbankaccount/add` | Y | `realname`,`mobile`,`withdraw_type`,`bank_account` 等 | |
| `/api/memberbankaccount/edit` | Y | `id` + 同上 | |
| `/api/memberbankaccount/delete` | Y | `id` | |
| `/api/memberbankaccount/setdefault` | Y | `id` | |
| `/api/memberbankaccount/defaultinfo` | Y | — | |
| `/wechatpay/api/transfer/getWithdrawConfig` | Y | — | 商家转账配置 |
| `/wechatpay/api/transfer/inprocess` | Y | `from_type`,`relate_tag` | 进行中 |
| `/wechatpay/api/transfer/transfer` | Y | `id`,`transfer_type` | 发起转账 |
| `/api/supercard/levelList` | ? | — | 超级卡等级 |
| `/api/supercard/createOrder` | Y | `level_id`；可选 `card_share_member*` | 购卡创单 |
| `/api/supercard/myHoldings` | Y | — | 持卡 |
| `/api/supercard/myCardOrders` | Y | — | 购卡订单 |
| `/api/supercard/cardOrderBrief` | Y | `order_id` | |
| `/api/supercardevaluate/summary` | N | 可选 `level_id` | 评价汇总 |
| `/api/supercardevaluate/page` | N | `page`,`page_size` | |
| `/api/supercardevaluate/add` | Y | `order_id`,`content`,`scores` 等 | |
| `/api/supercardevaluate/detailByOrder` | Y | `order_id` | |
| `/api/financecost/myList` | Y | `page`,`page_size` | 费用确认列表 |
| `/api/financecost/pendingConfirmCount` | Y | — | 待确认数 |
| `/api/financecost/wxConfirmPackage` | Y | `id`/`expense_id` | 确认收款包 |
| `/supermember/api/membercard/lists` | ? | — | 付费会员卡 |
| `/supermember/api/membercard/firstcard` | ? | — | |
| `/supermember/api/membercard/agreement` | N | — | |
| `/supermember/api/ordercreate/create` | Y | 购卡创单参数 | |
| `/membercancel/api/membercancel/config` | Y | — | 注销 |
| `/membercancel/api/membercancel/info` | Y | — | |
| `/membercancel/api/membercancel/agreement` | N | — | |
| `/membercancel/api/membercancel/accountInfo` | Y | — | |
| `/membercancel/api/membercancel/apply` | Y | — | |
| `/membercancel/api/membercancel/cancelApply` | Y | — | |
| `/memberrecommend/api/memberrecommend/lists` | Y | — | 邀请 |
| `/memberrecommend/api/memberrecommend/info` | Y | — | |
| `/memberrecommend/api/memberrecommend/poster` | Y | — | |
| `/memberrecharge/api/memberrecharge/config` | ? | — | 充值 |
| `/memberrecharge/api/memberrecharge/page` | ? | — | |
| `/memberrecharge/api/ordercreate/create` | Y | 充值金额等 | |
| `/memberrecharge/api/order/page` | Y | — | |
| `/birthdaygift/api/Config/config` | ? | — | 生日礼 |
| `/birthdaygift/api/Config/receive` | Y | — | |
| `/scenefestival/api/config/config` | ? | — | 节日礼 |
| `/scenefestival/api/config/receive` | Y | — | |
| `/memberconsume/api/config/info` | ? | 可选 `out_trade_no` | 消费送积分 |

---

## 6. 地址

| 路径 | 需登录 | 必要/关键参数 |
|------|--------|----------------|
| `/api/memberaddress/page` | Y | `page`,`page_size`；可选 `type`,`store_id` |
| `/api/memberaddress/info` | Y | `id` |
| `/api/memberaddress/add` | Y | 姓名/手机/省市区/详细地址等 |
| `/api/memberaddress/edit` | Y | `id` + 同上 |
| `/api/memberaddress/delete` | Y | `id` |
| `/api/memberaddress/setdefault` | Y | `id` |
| `/api/memberaddress/addthreeparties` | Y | 微信地址结构 |
| `/api/memberaddress/tranAddressInfo` | ? | 经纬度/`latlng` |
| `/api/address/lists` | N | 可选 `pid` | 省市区 |
| `/api/address/analysesAddress` | N | `address` | 智能解析 |

前端动态：`'/api/memberaddress/' + (add|edit)`。

---

## 7. 商品 / 购物车

| 路径 | 需登录 | 必要/关键参数 | 说明 |
|------|--------|----------------|------|
| `/api/goodssku/detail` | N | **`sku_id` 或 `goods_id`**；自动带 `share_member`/`source_member` | 详情 |
| `/api/goodssku/page` | N | `page`,`page_size`；筛选 `category_id`,`order`,`sort`,价格区间等 | 列表 |
| `/api/goodssku/pageByCategory` | N | `page`,`page_size`；`category_id(s)` | 分类商品 |
| `/api/goodssku/pageComponents` | N | DIY 组件参数 | 装修商品 |
| `/api/goodssku/components` | N | `num` 等 | |
| `/api/goodssku/recommend` | N | `page`,`page_size`；可选 `route` | 推荐 |
| `/api/goodssku/getInfoForCategory` | N | `sku_id` | 分类页 SKU |
| `/api/goodssku/goodsSku` | N | `goods_id` | SKU 弹层 |
| `/api/goodssku/goodsSkuByCategory` | N | `goods_id` | |
| `/api/goodscategory/tree` | N | 可选 `level`,`category_id` | 分类树（按 weapp 过滤） |
| `/api/goodsbrand/page` | N | 分页 | 品牌 |
| `/api/goods/modifyclicks` | N | `sku_id` | 点击 |
| `/api/goods/goodsbarrage` | N | `goods_id` | 弹幕 |
| `/api/goods/aftersale` | N | — | 售后说明 |
| `/api/goods/shareimg` | ? | 分享图参数 | |
| `/api/goods/poster` | ? | — | 海报 |
| `/api/goods/hotSearchWords` | N | — | |
| `/api/goods/defaultSearchWords` | N | — | |
| `/api/goodsbrowse/add` | Y | `goods_id`,`sku_id` | 足迹 |
| `/api/goodsbrowse/page` | Y | `page`,`page_size` | |
| `/api/goodsbrowse/delete` | Y | `id` | |
| `/api/goodscollect/add` | Y | `goods_id`,`sku_id` 等 | 收藏 |
| `/api/goodscollect/delete` | Y | `goods_id` | |
| `/api/goodscollect/page` | Y | `page`,`page_size` | |
| `/api/goodsevaluate/page` | N | `goods_id`,`page`,`page_size` | 评价 |
| `/api/goodsevaluate/getgoodsevaluate` | N | `goods_id` | |
| `/api/goodsevaluate/config` | N | — | |
| `/api/goodsevaluate/add` | Y | `order_id`,`goods_evaluate`(JSON) 等 | |
| `/api/goodsevaluate/again` | Y | `order_id`,`goods_evaluate` | 追评 |
| `/api/cart/lists` | Y | — | 角标列表 |
| `/api/cart/goodslists` | Y | — | 购物车页 |
| `/api/cart/add` | Y | **`sku_id`,`num`**；可选 `form_data` | |
| `/api/cart/edit` | Y | **`cart_id`,`num`** | |
| `/api/cart/delete` | Y | **`cart_id`** | |
| `/api/cart/editcartsku` | Y | `cart_id`,`sku_id`,`num` | 改规格 |
| `/api/cart/goodsnum` | Y | sku 相关 | 单 SKU 数量 |
| `/api/cartcalculate/calculate` | Y | `sku_ids`（常为 JSON 字符串） | 计价 |
| `/cardservice/api/card/getRelationCardGoods` | ? | — | 关联卡商品 |
| `/form/api/form/goodsform` | ? | — | 商品表单 |
| `/form/api/form/info` | ? | — | |
| `/form/api/form/create` | Y | — | |
| `/goodscircle/api/goods/sync` | ? | — | 好物圈 |

---

## 8. 订单创建 / 订单 / 售后 / 支付

### 8.1 订单创建（核心）

| 路径 | 需登录 | 必要参数 | 常用可选 |
|------|--------|----------|----------|
| `/api/ordercreate/payment` | Y | **`cart_ids` 或 `sku_id`+`num` 二选一** | `store_id`,`member_goods_card`,`jielong_id`,`is_open_card`,`delivery`,`member_address`,经纬度,`is_self_shop`,`share_member` |
| `/api/ordercreate/calculate` | Y | **`order_key`**（payment 返回） | `is_balance`,`is_point`,`coupon`(JSON),`delivery`,`member_address`,`member_card_unit`,`super_card_pricing` |
| `/api/ordercreate/create` | Y | **`order_key`** | 同 calculate + `buyer_message`,`form_data`,发票字段,`share_member*` |
| `/api/ordercreate/getcouponlist` | Y | `order_key`；`delivery` | `store_id` |

**`getCommonParam` 注入（服务端）**：`site_id`,`member_id`,`weapp_id`,`weapp_appid`,`weapp_openid`,`order_from`←`app_type`,`is_self_shop`,`share_member`,`share_member_ts`,`share_bind_source`。

**配送**：`delivery`、`member_address` 多为 **JSON 字符串**（小程序 form 编码限制）。

活动创单替换前缀（参数形态类似）：

- `/bargain/api/ordercreate/{payment,calculate,create}` — payment 需 `launch_id`
- `/bundling/api/ordercreate/{payment,calculate,create}` — payment 需 `bl_id`,`num`

### 8.2 订单

| 路径 | 需登录 | 必要/关键参数 |
|------|--------|----------------|
| `/api/order/lists` | Y | `page`,`page_size`；可选 `order_status`,`searchText` |
| `/api/order/detail` | Y | **`order_id`**（或 `merchant_trade_no`） |
| `/api/order/num` | Y | — | 各状态数量 |
| `/api/order/pay` | Y | **`order_ids`** | 取支付用 out_trade_no |
| `/api/order/close` | Y | `order_id` | |
| `/api/order/delete` | Y | `order_id` | |
| `/api/order/takedelivery` | Y | `order_id` | 确认收货 |
| `/api/order/membervirtualtakedelivery` | Y | 虚拟收货相关 | |
| `/api/order/package` | Y | `order_id` | 物流包裹 |
| `/api/order/tracepluginclicklog` | Y | `order_id`；可选 `package_id`,`trace_plugin_token` | |
| `/api/order/evluateinfo` | Y | `order_id` | 评价前信息（拼写历史遗留） |
| `/api/order/transactionagreement` | N | — | 交易协议 |

### 8.3 售后

| 路径 | 需登录 | 必要/关键参数 |
|------|--------|----------------|
| `/api/orderrefund/lists` | Y | `page`,`page_size`；可选 `refund_status` |
| `/api/orderrefund/detail` | Y | `order_goods_id` |
| `/api/orderrefund/refundData` | Y | `order_goods_id` |
| `/api/orderrefund/refundDataBatch` | Y | `order_goods_ids` |
| `/api/orderrefund/refund` | Y | 申请售后大对象（原因/金额/图片等） |
| `/api/orderrefund/cancel` | Y | `order_goods_id` |
| `/api/orderrefund/delivery` | Y | `order_goods_id`,`refund_delivery_name`,`refund_delivery_no` |

### 8.4 支付

| 路径 | 需登录 | 必要/关键参数 |
|------|--------|----------------|
| `/api/pay/info` | ? | **`out_trade_no`** |
| `/api/pay/type` | ? | 随 `app_type` 等 | 可用支付方式 |
| `/api/pay/pay` | Y | **`out_trade_no`,`pay_type`**；可选 `return_url`,`scene`,`is_balance`,`is_matched` |
| `/api/pay/status` | ? | `out_trade_no` | 轮询 |
| `/api/pay/resetpay` | Y | `out_trade_no` | 重置支付单 |
| `/api/pay/getBalanceConfig` | ? | — | 余额支付开关 |
| `/api/pay/memberpaycode` | Y | — | 付款码 |
| `/api/pay/outTradeNoToOrderDetailPath` | ? | `out_trade_no` | 跳转路径 |
| `/offlinepay/api/pay/config` | ? | — | 线下付 |
| `/offlinepay/api/pay/info` | ? | `out_trade_no` | |
| `/offlinepay/api/pay/pay` | Y | `out_trade_no`；可选 `desc`,`imgs` | |
| `/offlinepay/api/pay/uploadimg` | Y | 文件上传 | |
| `/shopcomponent/api/weapp/scenecheck` | ? | — | 交易组件场景 |

---

## 9. 分享体验（栖月汇定制）

| 路径 | 需登录 | 必要参数 | 可选 |
|------|--------|----------|------|
| `/api/shareexperience/resolve` | N | **`share_token`**（勿与会员 `token` 混淆；兼容旧参 `token`） | — |
| `/api/shareexperience/submit` | Y | **`share_token`** | `delivery_mode`,`member_address_json`（推荐）/`member_address`,`order_type` |
| `/api/shareexperience/ownerList` | Y | — | `page`,`page_size`(≤50) |
| `/api/shareexperience/ownerQrcode` | Y | **`instance_id`** | `weapp_id`,`refresh`,`env_version` |
| `/api/shareexperience/ownerGiftOrderList` | Y | — | `page`,`page_size` |
| `/api/shareexperience/ownerGiftShip` | Y | **`order_id`** | `delivery_type`,`delivery_no`,`express_company_id`,`template_id` |

---

## 10. 优惠券（addon: coupon）

| 路径 | 需登录 | 必要/关键参数 |
|------|--------|----------------|
| `/coupon/api/coupon/typelists` | N | — |
| `/coupon/api/coupon/typepagelists` | N | 分页 |
| `/coupon/api/coupon/typeinfo` | N | 券类型 id |
| `/coupon/api/coupon/receive` | Y | **`coupon_type_id`**；可选 `get_type` |
| `/coupon/api/coupon/memberpage` | Y | 分页 |
| `/coupon/api/coupon/num` | Y | — |
| `/coupon/api/coupon/receivedNum` | Y | — |
| `/coupon/api/coupon/couponbyid` | Y | 券 id |
| `/coupon/api/coupon/giftCreate` | Y | `coupon_id`；可选 `gift_mode`,`to_member_id`,`mobile` |
| `/coupon/api/coupon/giftCancel` | Y | `gift_id` |
| `/coupon/api/coupon/giftDetail` | ? | `gift_token` |
| `/coupon/api/coupon/giftClaim` | Y | `gift_token` |
| `/coupon/api/coupon/giftSentPage` | Y | `page`,`page_size` |
| `/coupon/api/coupon/giftReceivedPage` | Y | `page`,`page_size` |
| `/coupon/api/coupon/giftResolveMember` | Y | `mobile` |

---

## 11. 营销活动插件（uniapp 有调用）

参数列仅标扫描到的关键字段；创单类共性见 §8.1。

| 域 | 路径 | 关键参数 |
|----|------|----------|
| 砍价 | `/bargain/api/bargain/{detail,launch,bargain,browse,record,share,launchpage}` | 活动/发起 id |
| 砍价商品 | `/bargain/api/goods/{lists,page,goodssku,bargaininglist,poster,shareimg}` | `goods_id` 等 |
| 砍价创单 | `/bargain/api/ordercreate/payment` | **`launch_id`** |
| 套餐 | `/bundling/api/bundling/{lists,detail}` | `sku_id` / **`bl_id`** |
| 套餐创单 | `/bundling/api/ordercreate/payment` | **`bl_id`,`num`** |
| 秒杀 | `/seckill/api/seckill/lists`；`/seckill/api/seckillgoods/{lists,goodsSku}` | — |
| 拼团 | `/pintuan/api/goods/{lists,goodsSku}`；`/pintuan/api/order/pintuanmember` | `goods_id` |
| 拼团返 | `/pinfan/api/goods/{lists,goodsSku}` | |
| 团购 | `/groupbuy/api/goods/{lists,goodsSku}` | |
| 预售 | `/presale/api/goods/{lists,goodsSku}` | |
| 积分兑换 | `/pointexchange/api/goods/goodsSku`；`/pointexchange/api/order/{info,close}` | `order_id`(close) |
| 专题 | `/topic/api/topicgoods/goodsSku` | |
| 分销 | `/fenxiao/api/config/words`；`/fenxiao/api/goods/page`；`goodscollect/*`；`withdraw/transferType` | |
| 笔记 | `/notes/api/notes/lists`；`/notes/api/record/{add,delete}` | |
| 直播 | `/live/api/live/{info,modifyLiveStatus}` | |

---

## 12. 核销 / 客服 / 上传

| 路径 | 需登录 | 必要/关键参数 |
|------|--------|----------------|
| `/api/verify/checkisverifier` | Y | — |
| `/api/verify/verifyInfo` | Y | `verify_code` |
| `/api/verify/verify` | Y | `verify_code` |
| `/api/verify/lists` | Y | `page`,`page_size`；可选 `verify_type` |
| `/api/verify/getVerifyType` | Y | — |
| `/servicer/api/chat/bind` | Y | 会话绑定 |
| `/servicer/api/chat/bye` | Y | — |
| `/servicer/api/chat/dialogs` | Y | — |
| `/servicer/api/chat/say` | Y | 消息体 |
| `/servicer/api/chat/keyword` | ? | — |
| `/servicer/api/chat/chatimg` | Y | 图片 |
| `/api/upload/` | Y | `uni.uploadFile` | 通用上传 |
| `/api/upload/headimg` | Y | 头像文件 |
| `/api/upload/headimgBase64` | Y | `images` | Base64 |
| `/api/upload/headimgPull` | ? | `path` | 拉取头像 |

---

## 13. 服务端控制器索引（核心 `/api`）

物理目录：`niushop/app/api/controller/`

| 控制器文件 | URL 前缀 | 职责 |
|------------|----------|------|
| `Config.php` | `/api/config/*` | 初始化与各类配置 |
| `Diyview.php` | `/api/diyview/*` | 装修 |
| `Login.php` / `Register.php` / `Tripartite.php` / `Findpassword.php` | `/api/login|register|tripartite|findpassword/*` | 账号体系 |
| `Member*.php` | `/api/member*` | 会员与资产 |
| `Membershop.php` | `/api/membershop/*` | 本人店铺/分润 |
| `Goodssku.php` / `Goods.php` / `Goodscategory.php` … | `/api/goods*` | 商品 |
| `Cart.php` / `Cartcalculate.php` | `/api/cart*` | 购物车 |
| `Ordercreate.php` | `/api/ordercreate/*` | 创单 |
| `Order.php` / `Orderrefund.php` | `/api/order*` | 订单/售后 |
| `Pay.php` | `/api/pay/*` | 支付 |
| `Shareexperience.php` | `/api/shareexperience/*` | 体验码 |
| `Supercard.php` / `Supercardevaluate.php` | `/api/supercard*` | 超级卡 |
| `Store.php` / `Site.php` / `Address.php` | `/api/store|site|address/*` | 门店站点地址 |
| `Verify.php` / `Upload.php` | `/api/verify|upload/*` | 核销上传 |
| `Financecost.php` | `/api/financecost/*` | 费用确认 |

插件控制器：`niushop/addon/{名}/api/controller/` → URL `/{名}/api/...`。

---

## 附录 A. UniApp 路径全表（机器可读）

**文件**：`docs/niushop-uniapp-API路径与参数全表.tsv`（约 **308** 行）

| 列 | 含义 |
|----|------|
| `path` | uniapp 源码中的请求路径（小写归一） |
| `server_params_scanned` | 服务端同名 action 中扫描到的 `$this->params[...]` 键（**非完备必填清单**；必填以正文各节为准） |

正文 §3–§12 已按域标注**必要参数**与登录要求；TSV 用于检索与对账。

---

## 附录 B. 说明与维护

| 项 | 说明 |
|----|------|
| 参数完备性 | 「必要」来自控制器显式校验 + uniapp 主路径；可选字段随版本增减，以 PHP `$this->params[...]` 为准 |
| 大小写 | 路由不敏感；uniapp 里偶有 `Member`/`getSignStatus` 等驼峰，与小写等价 |
| 三端工程 | 本文仅 **`uniapp/`**；`uniapp_yuancangji/`、`uniapp_catering/` 可能另有差异路径 |
| 更新方式 | 改接口后：搜 uniapp `url:` + 对控制器 `public function`；或重跑扫描脚本 |
| 非改码排障 | 先确认 `token`、`X-Weapp-Id`、`out_trade_no`/`order_key` 是否齐全 |

---

*文档版本：按 2026-07 仓库扫描生成；不包含后台 shop 模块接口。*

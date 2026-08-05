# frozen/01 — Schema Fingerprint (D0 只读发现)

> 生成方式：qyh_discover_readonly 只读连接 recommend_ro@niushop_b2c_v5
> 生成时间：2026-08-05T08:16:51.688314+00:00
> 基线：aos-platform；上位方案：228-微商城专项 第 5 节
> 约束：只聚合不取值；PII_DIRECT 字段不出库

## 1. 七表结构与计数

### ns_site（P01 Shop，count=1，pk=site_id）

| 列名 | 类型 | 可空 | 键 | PII 等级 |
|---|---|---|---|---|
| site_id | int(11) unsigned | NO | PRI | NON_PII |
| site_type | varchar(255) | NO |  | NON_PII |
| site_domain | varchar(255) | NO |  | NON_PII |
| create_time | int(11) | NO |  | NON_PII |
| site_name | varchar(255) | NO |  | NON_PII |
| username | varchar(255) | NO |  | NON_PII |
| logo | varchar(255) | NO |  | NON_PII |
| seo_keywords | varchar(255) | NO |  | NON_PII |
| seo_description | varchar(255) | NO |  | NON_PII |
| site_tel | varchar(255) | NO |  | PII_DIRECT |
| logo_square | varchar(255) | NO |  | NON_PII |
| seo_title | varchar(255) | NO |  | NON_PII |

**索引：**
- `PRIMARY` (UNIQUE): site_id

### ns_goods（P02 Product，count=65，pk=goods_id）

| 列名 | 类型 | 可空 | 键 | PII 等级 |
|---|---|---|---|---|
| goods_id | int(11) unsigned | NO | PRI | NON_PII |
| goods_name | varchar(255) | NO | MUL | NON_PII |
| goods_class | int(11) | NO | MUL | NON_PII |
| goods_class_name | varchar(25) | NO |  | NON_PII |
| goods_attr_class | int(11) | NO |  | NON_PII |
| goods_attr_name | varchar(255) | NO |  | NON_PII |
| site_id | int(11) | NO | MUL | NON_PII |
| site_name | varchar(255) | NO |  | NON_PII |
| goods_image | varchar(2000) | NO |  | NON_PII |
| goods_content | text | YES |  | NON_PII |
| goods_state | tinyint(4) | NO | MUL | NON_PII |
| category_id | varchar(255) | NO | MUL | NON_PII |
| category_json | varchar(500) | NO |  | NON_PII |
| brand_id | int(11) | NO | MUL | NON_PII |
| brand_name | varchar(255) | NO |  | NON_PII |
| price | decimal(10,2) | NO | MUL | NON_PII |
| market_price | decimal(10,2) | NO |  | NON_PII |
| cost_price | decimal(10,2) | NO |  | NON_PII |
| goods_stock | decimal(12,3) | NO |  | NON_PII |
| goods_stock_alarm | int(11) | NO |  | NON_PII |
| is_virtual | tinyint(4) | NO | MUL | NON_PII |
| virtual_indate | int(11) | NO |  | NON_PII |
| is_free_shipping | tinyint(4) | NO |  | NON_PII |
| shipping_template | int(11) | NO |  | NON_PII |
| goods_spec_format | text | YES |  | NON_PII |
| goods_attr_format | text | YES |  | NON_PII |
| is_delete | tinyint(4) | NO | MUL | NON_PII |
| introduction | varchar(255) | NO |  | NON_PII |
| keywords | varchar(255) | NO |  | NON_PII |
| unit | varchar(255) | NO |  | NON_PII |
| sort | int(11) | NO | MUL | NON_PII |
| create_time | int(11) | NO |  | NON_PII |
| modify_time | int(11) | NO |  | NON_PII |
| share_experience_quota | int(11) | NO |  | NON_PII |
| share_lead_goods_id | int(11) unsigned | NO |  | NON_PII |
| share_lead_goods_quantity | int(11) | NO |  | NON_PII |
| video_url | varchar(555) | NO |  | NON_PII |
| sale_num | decimal(12,3) | NO |  | NON_PII |
| evaluate | int(11) | NO |  | NON_PII |
| evaluate_shaitu | int(11) | NO |  | NON_PII |
| evaluate_shipin | int(11) | NO |  | NON_PII |
| evaluate_zhuiping | int(11) | NO |  | NON_PII |
| evaluate_haoping | int(11) | NO |  | NON_PII |
| evaluate_zhongping | int(11) | NO |  | NON_PII |
| evaluate_chaping | int(11) | NO |  | NON_PII |
| is_fenxiao | tinyint(4) | NO |  | NON_PII |
| fenxiao_type | tinyint(4) | NO |  | NON_PII |
| supplier_id | int(11) | NO |  | NON_PII |
| is_consume_discount | tinyint(4) | NO |  | NON_PII |
| pay_grant_member_level_id | int(11) | NO |  | NON_PII |
| pay_send_coupon_json | text | YES |  | NON_PII |
| discount_config | tinyint(4) | NO |  | NON_PII |
| discount_method | varchar(20) | NO |  | NON_PII |
| sku_id | int(11) | NO | MUL | NON_PII |
| promotion_addon | varchar(255) | NO |  | NON_PII |
| goods_service_ids | varchar(255) | NO |  | NON_PII |
| label_id | int(11) | NO |  | NON_PII |
| label_name | varchar(50) | NO |  | NON_PII |
| virtual_sale | decimal(12,3) | NO |  | NON_PII |
| max_buy | int(11) | NO |  | NON_PII |
| min_buy | int(11) | NO |  | NON_PII |
| recommend_way | int(11) | NO |  | NON_PII |
| timer_on | int(11) | NO |  | NON_PII |
| timer_off | int(11) | NO |  | NON_PII |
| is_need_verify | int(11) | NO |  | NON_PII |
| verify_validity_type | int(11) | NO |  | NON_PII |
| is_limit | int(11) | NO |  | NON_PII |
| limit_type | int(11) | NO |  | NON_PII |
| qr_id | int(11) | NO |  | NON_PII |
| template_id | int(11) | NO |  | NON_PII |
| success_evaluate_num | int(11) | NO |  | NON_PII |
| fail_evaluate_num | int(11) | NO |  | NON_PII |
| wait_evaluate_num | int(11) | NO |  | NON_PII |
| sale_show | int(11) | NO |  | NON_PII |
| stock_show | int(11) | NO |  | NON_PII |
| virtual_deliver_type | varchar(20) | NO |  | NON_PII |
| virtual_receive_type | varchar(20) | NO |  | NON_PII |
| barrage_show | int(11) | NO |  | NON_PII |
| market_price_show | int(11) | NO |  | NON_PII |
| form_id | int(11) | NO |  | NON_PII |
| support_trade_type | varchar(255) | NO |  | NON_PII |
| sale_channel | varchar(50) | NO | MUL | NON_PII |
| sale_store | varchar(5000) | NO | MUL | NON_PII |
| service_category | varchar(2000) | NO |  | NON_PII |
| is_unify_price | int(11) | NO |  | NON_PII |
| real_stock | decimal(12,3) | NO | MUL | NON_PII |
| pricing_type | varchar(10) | NO |  | NON_PII |
| is_reserve | int(11) | NO |  | NON_PII |
| service_mode | varchar(255) | NO |  | NON_PII |
| service_price_way | varchar(255) | NO |  | NON_PII |

**索引：**
- `IDX_ns_goods_brand` (INDEX): brand_id
- `IDX_ns_goods_category_id` (INDEX): category_id
- `IDX_ns_goods_goods_class` (INDEX): goods_class
- `IDX_ns_goods_is_delete` (INDEX): is_delete
- `IDX_ns_goods_name` (INDEX): goods_name
- `IDX_ns_goods_price` (INDEX): price
- `IDX_ns_goods_real_stock` (INDEX): real_stock
- `IDX_ns_goods_sale_channel` (INDEX): sale_channel
- `IDX_ns_goods_sale_store` (INDEX): sale_store
- `IDX_ns_goods_site_id` (INDEX): site_id
- `IDX_ns_goods_si_virtual` (INDEX): is_virtual
- `IDX_ns_goods_sku_id` (INDEX): sku_id
- `IDX_ns_goods_sort` (INDEX): sort
- `IDX_ns_goods_state` (INDEX): goods_state
- `PRIMARY` (UNIQUE): goods_id

### ns_goods_sku（P03 ProductSku，count=73，pk=sku_id）

| 列名 | 类型 | 可空 | 键 | PII 等级 |
|---|---|---|---|---|
| sku_id | int(11) unsigned | NO | PRI | NON_PII |
| site_id | int(11) | NO | MUL | NON_PII |
| goods_id | int(11) | NO |  | NON_PII |
| sku_name | varchar(255) | NO |  | NON_PII |
| sku_no | varchar(255) | NO |  | NON_PII |
| sku_spec_format | text | YES |  | NON_PII |
| price | decimal(10,2) | NO |  | NON_PII |
| market_price | decimal(10,2) | NO |  | NON_PII |
| cost_price | decimal(10,2) | NO |  | NON_PII |
| discount_price | decimal(10,2) | NO |  | NON_PII |
| promotion_type | tinyint(4) | NO |  | NON_PII |
| start_time | int(11) | NO |  | NON_PII |
| end_time | int(11) | NO |  | NON_PII |
| stock | decimal(12,3) | NO |  | NON_PII |
| weight | decimal(12,3) | NO |  | NON_PII |
| volume | decimal(12,3) | NO |  | NON_PII |
| click_num | int(11) | NO |  | NON_PII |
| sale_num | decimal(12,3) | NO |  | NON_PII |
| collect_num | int(11) | NO |  | NON_PII |
| sku_image | varchar(255) | NO |  | NON_PII |
| sku_images | varchar(2000) | NO |  | NON_PII |
| goods_class | int(11) | NO | MUL | NON_PII |
| goods_class_name | varchar(25) | NO |  | NON_PII |
| goods_attr_class | int(11) | NO |  | NON_PII |
| goods_attr_name | varchar(255) | NO |  | NON_PII |
| goods_name | varchar(255) | NO |  | NON_PII |
| goods_content | text | YES |  | NON_PII |
| goods_state | tinyint(4) | NO |  | NON_PII |
| goods_stock_alarm | int(11) | NO |  | NON_PII |
| is_virtual | tinyint(4) | NO |  | NON_PII |
| virtual_indate | int(11) | NO |  | NON_PII |
| is_free_shipping | tinyint(4) | NO |  | NON_PII |
| shipping_template | int(11) | NO |  | NON_PII |
| goods_spec_format | text | YES |  | NON_PII |
| goods_attr_format | text | YES |  | NON_PII |
| is_delete | tinyint(4) | NO | MUL | NON_PII |
| introduction | varchar(255) | NO |  | NON_PII |
| keywords | varchar(255) | NO |  | NON_PII |
| unit | varchar(255) | NO |  | NON_PII |
| sort | int(11) | NO | MUL | NON_PII |
| create_time | int(11) | NO |  | NON_PII |
| modify_time | int(11) | NO |  | NON_PII |
| video_url | varchar(555) | NO |  | NON_PII |
| evaluate | int(11) | NO |  | NON_PII |
| evaluate_shaitu | int(11) | NO |  | NON_PII |
| evaluate_shipin | int(11) | NO |  | NON_PII |
| evaluate_zhuiping | int(11) | NO |  | NON_PII |
| evaluate_haoping | int(11) | NO |  | NON_PII |
| evaluate_zhongping | int(11) | NO |  | NON_PII |
| evaluate_chaping | int(11) | NO |  | NON_PII |
| spec_name | varchar(255) | NO |  | NON_PII |
| supplier_id | int(11) | NO |  | NON_PII |
| is_consume_discount | tinyint(4) | NO |  | NON_PII |
| discount_config | tinyint(4) | NO |  | NON_PII |
| discount_method | varchar(20) | NO |  | NON_PII |
| member_price | varchar(255) | NO |  | NON_PII |
| self_shop_special_price | decimal(10,2) | NO |  | NON_PII |
| allow_use_coupon | tinyint(1) unsigned | NO |  | NON_PII |
| allow_use_balance | tinyint(1) unsigned | NO |  | NON_PII |
| goods_service_ids | varchar(255) | NO |  | NON_PII |
| virtual_sale | decimal(12,3) | NO |  | NON_PII |
| max_buy | int(11) | NO |  | NON_PII |
| min_buy | int(11) | NO |  | NON_PII |
| recommend_way | int(11) | NO |  | NON_PII |
| fenxiao_price | decimal(10,2) | NO |  | NON_PII |
| stock_alarm | int(11) | NO |  | NON_PII |
| sale_sort | int(11) | NO |  | NON_PII |
| is_default | tinyint(4) | NO |  | NON_PII |
| verify_num | int(11) | NO |  | NON_PII |
| is_limit | int(11) | NO |  | NON_PII |
| limit_type | int(11) | NO |  | NON_PII |
| qr_id | int(11) | NO |  | NON_PII |
| template_id | int(11) | NO |  | NON_PII |
| success_evaluate_num | int(11) | NO |  | NON_PII |
| fail_evaluate_num | int(11) | NO |  | NON_PII |
| wait_evaluate_num | int(11) | NO |  | NON_PII |
| brand_id | int(11) | NO |  | NON_PII |
| brand_name | varchar(255) | NO |  | NON_PII |
| form_id | int(11) | NO |  | NON_PII |
| support_trade_type | varchar(255) | NO |  | NON_PII |
| sale_channel | varchar(50) | NO |  | NON_PII |
| sale_store | varchar(5000) | NO |  | NON_PII |
| service_length | int(11) | YES |  | NON_PII |
| real_stock | decimal(12,3) | NO |  | NON_PII |
| is_unify_price | int(11) | NO |  | NON_PII |
| plu | varchar(4) | NO |  | NON_PII |
| pricing_type | varchar(10) | NO |  | NON_PII |

**索引：**
- `IDX_ns_goods_goods_class` (INDEX): goods_class
- `IDX_ns_goods_is_delete` (INDEX): is_delete
- `IDX_ns_goods_site_id` (INDEX): site_id
- `IDX_ns_goods_sort` (INDEX): sort
- `PRIMARY` (UNIQUE): sku_id

### ns_goods_category（P04 Category，count=11，pk=category_id）

| 列名 | 类型 | 可空 | 键 | PII 等级 |
|---|---|---|---|---|
| category_id | int(11) | NO | PRI | NON_PII |
| site_id | int(11) | NO |  | NON_PII |
| category_name | varchar(50) | NO |  | NON_PII |
| short_name | varchar(50) | NO |  | NON_PII |
| pid | int(11) | NO | MUL | NON_PII |
| level | int(11) | NO |  | NON_PII |
| is_show | int(11) | NO |  | NON_PII |
| sort | int(11) | NO |  | NON_PII |
| image | varchar(255) | NO |  | NON_PII |
| keywords | varchar(255) | NO |  | NON_PII |
| description | varchar(255) | NO |  | NON_PII |
| attr_class_id | int(11) | NO |  | NON_PII |
| attr_class_name | varchar(255) | NO |  | NON_PII |
| category_id_1 | int(11) | NO |  | NON_PII |
| category_id_2 | int(11) | NO |  | NON_PII |
| category_id_3 | int(11) | NO |  | NON_PII |
| category_full_name | varchar(255) | NO |  | NON_PII |
| image_adv | varchar(255) | NO |  | NON_PII |
| commission_rate | decimal(10,2) | NO |  | NON_PII |
| link_url | varchar(2000) | NO |  | NON_PII |
| is_recommend | int(11) | NO |  | NON_PII |
| icon | varchar(255) | NO |  | NON_PII |

**索引：**
- `pid_level` (INDEX): pid,level
- `PRIMARY` (UNIQUE): category_id

### ns_order（P05 Order，count=177，pk=order_id）

| 列名 | 类型 | 可空 | 键 | PII 等级 |
|---|---|---|---|---|
| order_id | int(11) | NO | PRI | NON_PII |
| order_no | varchar(50) | NO |  | NON_PII |
| site_id | int(11) | NO | MUL | NON_PII |
| site_name | varchar(50) | NO |  | NON_PII |
| website_id | int(11) | NO |  | NON_PII |
| order_name | varchar(1000) | NO |  | NON_PII |
| order_from | varchar(55) | NO | MUL | NON_PII |
| weapp_id | int(11) | NO |  | NON_PII |
| weapp_appid | varchar(32) | NO |  | NON_PII |
| weapp_openid | varchar(64) | NO |  | NON_PII |
| delivery_platform | varchar(32) | NO |  | NON_PII |
| third_delivery_no | varchar(64) | NO |  | NON_PII |
| order_from_name | varchar(50) | NO |  | NON_PII |
| order_type | int(11) | NO | MUL | NON_PII |
| order_type_name | varchar(50) | NO |  | NON_PII |
| order_promotion_type | int(11) | NO |  | NON_PII |
| order_promotion_name | varchar(50) | NO |  | NON_PII |
| promotion_id | int(11) | NO | MUL | NON_PII |
| out_trade_no | varchar(50) | NO |  | NON_PII |
| out_trade_no_2 | varchar(50) | NO |  | NON_PII |
| delivery_code | varchar(50) | NO |  | NON_PII |
| order_status | int(11) | NO | MUL | NON_PII |
| order_status_name | varchar(50) | NO |  | NON_PII |
| order_status_action | varchar(1000) | NO |  | NON_PII |
| pay_status | int(11) | NO | MUL | NON_PII |
| delivery_status | int(11) | NO |  | NON_PII |
| refund_status | int(11) | NO |  | NON_PII |
| pay_type | varchar(55) | NO |  | NON_PII |
| pay_type_name | varchar(50) | NO |  | NON_PII |
| delivery_type | varchar(50) | NO |  | NON_PII |
| delivery_type_name | varchar(50) | NO |  | NON_PII |
| member_id | int(11) | NO | MUL | NON_PII |
| share_member_id | int(11) unsigned | NO |  | NON_PII |
| share_bind_time | int(11) unsigned | NO |  | NON_PII |
| commission_risk_flag | tinyint(1) | NO |  | NON_PII |
| commission_risk_reason | varchar(500) | NO |  | NON_PII |
| share_bind_source | varchar(32) | NO |  | NON_PII |
| share_bind_weapp | int(11) | NO |  | NON_PII |
| name | varchar(50) | NO |  | NON_PII |
| mobile | varchar(255) | NO |  | PII_DIRECT |
| telephone | varchar(255) | NO |  | PII_DIRECT |
| province_id | int(11) | NO |  | NON_PII |
| city_id | int(11) | NO |  | NON_PII |
| district_id | int(11) | NO |  | NON_PII |
| community_id | int(11) | NO |  | NON_PII |
| address | varchar(255) | NO |  | PII_DIRECT |
| full_address | varchar(255) | NO |  | PII_DIRECT |
| longitude | varchar(50) | NO |  | NON_PII |
| latitude | varchar(50) | NO |  | NON_PII |
| buyer_ip | varchar(20) | NO |  | NON_PII |
| buyer_ask_delivery_time | varchar(50) | NO |  | NON_PII |
| buyer_message | varchar(50) | NO |  | NON_PII |
| goods_money | decimal(10,2) | NO |  | NON_PII |
| delivery_money | decimal(10,2) | NO |  | NON_PII |
| promotion_money | decimal(10,2) | NO |  | NON_PII |
| coupon_id | int(11) | NO |  | NON_PII |
| coupon_money | decimal(10,2) | NO |  | NON_PII |
| invoice_money | decimal(10,2) | NO |  | NON_PII |
| order_money | decimal(10,2) | NO |  | NON_PII |
| adjust_money | decimal(10,2) | NO |  | NON_PII |
| balance_money | decimal(10,2) | NO |  | NON_PII |
| pay_money | decimal(10,2) | NO |  | NON_PII |
| create_time | int(11) | NO | MUL | NON_PII |
| pay_time | int(11) | NO |  | NON_PII |
| delivery_time | int(11) | NO |  | NON_PII |
| sign_time | int(11) | NO |  | NON_PII |
| finish_time | int(11) | NO | MUL | NON_PII |
| close_time | int(11) | NO |  | NON_PII |
| is_lock | int(11) | NO |  | NON_PII |
| is_evaluate | int(11) | NO |  | NON_PII |
| is_delete | int(11) | NO |  | NON_PII |
| is_enable_refund | int(11) | NO |  | NON_PII |
| remark | varchar(255) | NO |  | NON_PII |
| goods_num | decimal(12,3) | NO |  | NON_PII |
| delivery_store_id | int(11) | NO |  | NON_PII |
| delivery_status_name | varchar(50) | NO |  | NON_PII |
| is_settlement | tinyint(4) | NO |  | NON_PII |
| store_settlement_id | int(11) | NO |  | NON_PII |
| delivery_store_name | varchar(255) | NO |  | NON_PII |
| promotion_type | varchar(255) | NO |  | NON_PII |
| promotion_type_name | varchar(255) | NO |  | NON_PII |
| promotion_status_name | varchar(255) | NO |  | NON_PII |
| delivery_store_info | text | YES |  | NON_PII |
| virtual_code | varchar(255) | NO |  | NON_PII |
| evaluate_status | int(11) | NO |  | NON_PII |
| evaluate_status_name | varchar(20) | NO |  | NON_PII |
| refund_money | decimal(10,2) | NO |  | NON_PII |
| commission | decimal(10,2) | NO |  | NON_PII |
| is_invoice | int(11) | NO |  | NON_PII |
| invoice_type | int(11) | NO |  | NON_PII |
| invoice_title | varchar(255) | NO |  | NON_PII |
| taxpayer_number | varchar(255) | NO |  | NON_PII |
| invoice_rate | decimal(10,2) | NO |  | NON_PII |
| invoice_content | varchar(255) | NO |  | NON_PII |
| invoice_delivery_money | decimal(10,2) | NO |  | NON_PII |
| invoice_full_address | varchar(255) | NO |  | PII_DIRECT |
| is_tax_invoice | int(11) | NO | MUL | NON_PII |
| invoice_email | varchar(255) | NO |  | PII_QUASI |
| invoice_title_type | int(11) | NO |  | NON_PII |
| is_fenxiao | int(11) | NO |  | NON_PII |
| point_money | decimal(10,2) | NO |  | NON_PII |
| member_card_money | decimal(10,2) | NO |  | NON_PII |
| member_card_order | int(11) | NO |  | NON_PII |
| invoice_status | tinyint(4) | NO |  | NON_PII |
| invoice_remark | text | YES |  | NON_PII |
| invoice_code | varchar(255) | NO |  | NON_PII |
| invoice_image | varchar(255) | NO |  | NON_PII |
| invoice_time | int(11) | NO |  | NON_PII |
| predict_delivery_time | int(11) | NO |  | NON_PII |
| is_video_number | int(11) | NO |  | NON_PII |
| close_cause | varchar(255) | NO |  | NON_PII |
| cashier_order_type | varchar(50) | NO |  | NON_PII |
| cashier_sell_time | int(11) | NO |  | NON_PII |
| cashier_operator_id | int(11) unsigned | NO |  | NON_PII |
| cashier_operator_name | varchar(255) | NO |  | NON_PII |
| balance | decimal(10,2) | NO |  | NON_PII |
| total_balance | decimal(10,2) | NO |  | NON_PII |
| store_id | int(11) | NO |  | NON_PII |
| reduction | decimal(10,2) | NO |  | NON_PII |
| round_money | decimal(10,0) | NO |  | NON_PII |
| order_scene | varchar(50) | NO |  | NON_PII |
| store_commission_rate | decimal(10,2) | NO |  | NON_PII |
| store_commission | decimal(10,2) | NO |  | NON_PII |
| delivery_start_time | int(11) | NO |  | NON_PII |
| delivery_end_time | int(11) | NO |  | NON_PII |
| order_biz_type | varchar(50) | NO |  | NON_PII |
| share_instance_id | int(11) unsigned | NO | MUL | NON_PII |
| share_owner_member_id | int(11) | NO |  | NON_PII |
| is_self_shop_special_price | tinyint(1) | NO |  | NON_PII |
| is_self_shop_order | tinyint(1) | NO |  | NON_PII |

**索引：**
- `IDX_ns_order_create_time` (INDEX): create_time
- `IDX_ns_order_finish_time` (INDEX): finish_time
- `IDX_ns_order_is_tax_invoice` (INDEX): is_tax_invoice
- `IDX_ns_order_member_id` (INDEX): member_id
- `IDX_ns_order_order_from` (INDEX): order_from
- `IDX_ns_order_order_status` (INDEX): order_status
- `IDX_ns_order_order_type` (INDEX): order_type
- `IDX_ns_order_pay_status` (INDEX): pay_status
- `IDX_ns_order_promotion_id` (INDEX): promotion_id
- `idx_order_biz_type` (INDEX): site_id,order_biz_type
- `idx_share_instance` (INDEX): share_instance_id
- `idx_share_member_id` (INDEX): site_id,share_member_id
- `idx_site_weapp_id` (INDEX): site_id,weapp_id
- `PRIMARY` (UNIQUE): order_id

### ns_order_goods（P06 OrderLine，count=227，pk=order_goods_id）

| 列名 | 类型 | 可空 | 键 | PII 等级 |
|---|---|---|---|---|
| order_goods_id | int(11) | NO | PRI | NON_PII |
| order_id | int(11) | NO | MUL | NON_PII |
| order_no | varchar(20) | NO |  | NON_PII |
| site_id | int(11) | NO |  | NON_PII |
| member_id | int(11) | NO | MUL | NON_PII |
| goods_id | int(11) | NO | MUL | NON_PII |
| sku_id | int(11) | NO | MUL | NON_PII |
| sku_name | varchar(255) | NO |  | NON_PII |
| sku_image | varchar(2000) | NO |  | NON_PII |
| sku_no | varchar(255) | NO |  | NON_PII |
| is_virtual | int(11) | NO | MUL | NON_PII |
| goods_class | varchar(50) | NO |  | NON_PII |
| goods_class_name | varchar(50) | NO |  | NON_PII |
| price | decimal(10,2) | NO |  | NON_PII |
| cost_price | decimal(10,2) | NO |  | NON_PII |
| num | decimal(12,3) | NO |  | NON_PII |
| goods_money | decimal(10,2) | NO |  | NON_PII |
| cost_money | decimal(10,2) | NO |  | NON_PII |
| delivery_status | int(11) | NO |  | NON_PII |
| delivery_status_name | varchar(50) | NO |  | NON_PII |
| delivery_no | varchar(50) | NO |  | NON_PII |
| gift_flag | int(11) | NO |  | NON_PII |
| refund_no | varchar(50) | NO |  | NON_PII |
| refund_status | int(11) | NO | MUL | NON_PII |
| refund_status_name | varchar(50) | NO |  | NON_PII |
| refund_status_action | varchar(1000) | NO |  | NON_PII |
| refund_type | int(11) | NO |  | NON_PII |
| refund_apply_money | decimal(10,2) | NO |  | NON_PII |
| refund_reason | varchar(255) | NO |  | NON_PII |
| refund_real_money | decimal(10,2) | NO |  | NON_PII |
| refund_delivery_name | varchar(50) | NO |  | NON_PII |
| refund_delivery_no | varchar(20) | NO |  | NON_PII |
| refund_time | int(11) | NO |  | NON_PII |
| refund_refuse_reason | varchar(255) | NO |  | NON_PII |
| refund_action_time | int(11) | NO |  | NON_PII |
| real_goods_money | decimal(10,2) | NO |  | NON_PII |
| refund_remark | varchar(255) | NO |  | NON_PII |
| refund_images | varchar(3000) | NO |  | NON_PII |
| refund_delivery_remark | varchar(255) | NO |  | NON_PII |
| refund_address | varchar(255) | NO |  | PII_DIRECT |
| is_refund_stock | tinyint(1) | NO |  | NON_PII |
| refund_money_type | int(11) | NO |  | NON_PII |
| shop_refund_remark | varchar(255) | NO |  | NON_PII |
| shop_active_refund | tinyint(4) | NO |  | NON_PII |
| shop_active_refund_no | varchar(50) | NO |  | NON_PII |
| shop_active_refund_remark | varchar(255) | NO |  | NON_PII |
| shop_active_refund_money | decimal(10,2) | NO |  | NON_PII |
| shop_active_refund_money_type | int(11) | NO |  | NON_PII |
| refund_mode | int(11) | NO |  | NON_PII |
| promotion_money | decimal(10,2) | NO |  | NON_PII |
| coupon_money | decimal(10,2) | NO |  | NON_PII |
| adjust_money | decimal(10,2) | NO |  | NON_PII |
| goods_name | varchar(400) | NO |  | NON_PII |
| sku_spec_format | varchar(1000) | NO |  | NON_PII |
| is_fenxiao | int(11) | NO | MUL | NON_PII |
| use_point | int(11) | NO |  | NON_PII |
| point_money | decimal(10,2) | NO |  | NON_PII |
| refund_delivery_money | decimal(10,2) | NO |  | NON_PII |
| create_time | int(11) | NO |  | NON_PII |
| out_aftersale_id | varchar(255) | NO |  | NON_PII |
| refund_address_id | int(11) | NO |  | PII_DIRECT |
| refund_pay_money | decimal(10,2) | NO |  | NON_PII |
| refund_channel_status | tinyint(4) | NO |  | NON_PII |
| store_id | int(11) | NO |  | NON_PII |
| card_item_id | int(11) | NO |  | NON_PII |
| card_promotion_money | decimal(10,2) | NO |  | NON_PII |
| supplier_id | int(11) | NO |  | NON_PII |
| is_adjust_price | int(11) | NO |  | NON_PII |
| price_tier | varchar(16) | NO |  | NON_PII |
| card_holding_id | int(11) unsigned | NO |  | NON_PII |
| price_level_id | int(11) | NO |  | NON_PII |

**索引：**
- `IDX_ns_order_goods_goods_id` (INDEX): goods_id
- `IDX_ns_order_goods_is_fenxiao` (INDEX): is_fenxiao
- `IDX_ns_order_goods_is_virtual` (INDEX): is_virtual
- `IDX_ns_order_goods_member_id` (INDEX): member_id
- `IDX_ns_order_goods_order_id` (INDEX): order_id
- `IDX_ns_order_goods_refund_status` (INDEX): refund_status
- `IDX_ns_order_goods_sku_id` (INDEX): sku_id
- `idx_price_tier` (INDEX): order_id,price_tier
- `PRIMARY` (UNIQUE): order_goods_id

### ns_express_delivery_package（P07 Shipment，count=19，pk=id）

| 列名 | 类型 | 可空 | 键 | PII 等级 |
|---|---|---|---|---|
| id | int(11) | NO | PRI | NON_PII |
| site_id | int(11) | NO | MUL | NON_PII |
| order_id | int(11) | NO | MUL | NON_PII |
| order_goods_id_array | varchar(1000) | NO |  | NON_PII |
| goods_id_array | text | YES |  | NON_PII |
| package_name | varchar(50) | NO |  | NON_PII |
| delivery_type | tinyint(4) | NO |  | NON_PII |
| express_company_id | int(11) | NO |  | NON_PII |
| express_company_name | varchar(255) | NO |  | NON_PII |
| delivery_no | varchar(50) | NO |  | NON_PII |
| delivery_time | int(11) | NO |  | NON_PII |
| member_id | int(11) | NO |  | NON_PII |
| member_name | varchar(50) | NO |  | NON_PII |
| express_company_image | varchar(255) | NO |  | NON_PII |
| type | varchar(20) | NO |  | NON_PII |
| template_id | int(11) | NO |  | NON_PII |
| template_name | varchar(255) | NO |  | NON_PII |
| trace | text | YES |  | NON_PII |
| follow_waybill_token | varchar(255) | NO |  | NON_PII |
| follow_waybill_status | tinyint(1) | NO |  | NON_PII |
| follow_waybill_time | int(11) | NO |  | NON_PII |
| follow_waybill_err | varchar(500) | NO |  | NON_PII |
| upload_shipping_status | tinyint(1) | NO |  | NON_PII |
| upload_shipping_err | varchar(500) | NO |  | NON_PII |
| upload_shipping_retry | int(11) | NO |  | NON_PII |
| follow_delivery_id | varchar(32) | NO |  | NON_PII |
| trace_plugin_token | varchar(255) | NO |  | NON_PII |
| trace_plugin_status | tinyint(1) | NO |  | NON_PII |
| trace_plugin_time | int(11) | NO |  | NON_PII |
| trace_plugin_err | varchar(500) | NO |  | NON_PII |
| trace_plugin_delivery_id | varchar(32) | NO |  | NON_PII |

**索引：**
- `IDX_ns_express_delivery_package_order_id` (INDEX): order_id
- `IDX_ns_express_delivery_package_site_id` (INDEX): site_id
- `PRIMARY` (UNIQUE): id

## 2. PII 字段分类汇总（7 表范围内）

- **ns_site**: [('site_tel', 'PII_DIRECT')]
- **ns_order**: [('mobile', 'PII_DIRECT'), ('telephone', 'PII_DIRECT'), ('address', 'PII_DIRECT'), ('full_address', 'PII_DIRECT'), ('invoice_full_address', 'PII_DIRECT'), ('invoice_email', 'PII_QUASI')]
- **ns_order_goods**: [('refund_address', 'PII_DIRECT'), ('refund_address_id', 'PII_DIRECT')]

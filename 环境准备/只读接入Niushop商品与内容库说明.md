# 外部系统 · 只读接入 Niushop 商品 / 文章 / 评价库说明

> **版本**：v1.0 · 2026-06-16  
> **适用**：微信聊天分析、目标客户识别、商品/内容精准推荐等 **外部 AI 系统**  
> **项目**：`niushop_b2c_v5`（栖月汇 site_id=1）  
> **原则**：**只读 SELECT**，禁止 INSERT/UPDATE/DELETE；不读会员隐私与支付配置

---

## 一、文档目的

让外部系统能够：

1. 以 **MySQL 只读账号** 连接线上库（或经 SSH 隧道连库）；
2. 理解 **商品库、商品分类、文章分类、商品评价、超级卡评价** 的表结构与关联；
3. 拉取 **栖月汇小程序（weapp_id=11）** 可售商品与可展示内容，用于聊天场景下的精准推荐；
4. 用 **示例 SQL** 快速落地，无需读 PHP 源码。

完整 DDL 可参考：`docs/niushop_b2c_v5.sql`（物理表均带 `ns`_ 前缀）。

---

## 二、数据库连接

### 2.1 与商城相同的连接参数（参考）

商城 PHP 配置：`niushop/config/database.php`（**含密码，勿提交、勿明文转发给第三方**）。


| 参数  | 线上典型值            | 说明                            |
| --- | ---------------- | ----------------------------- |
| 类型  | MySQL / MariaDB  |                               |
| 主机  | `127.0.0.1`      | 线上 MySQL 仅本机监听；外网须 **SSH 隧道** |
| 端口  | `3306`           |                               |
| 库名  | `niushop_b2c_v5` | 以线上实际为准                       |
| 表前缀 | `ns_`            | ThinkPHP 物理表名均带此前缀            |
| 字符集 | `utf8mb4`        | 连接务必指定                        |


**SSH 隧道示例（外部系统在本机开发时）**：

```bash
 ssh -4 -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -N -L 127.0.0.1:13306:127.0.0.1:3306 root@118.195.194.208
# 外部系统连 127.0.0.1:13306
```

### 2.2 建议：专用只读账号（在 MySQL 执行一次）

```sql
-- 请替换 YOUR_STRONG_PASSWORD
CREATE USER IF NOT EXISTS 'recommend_ro'@'%' IDENTIFIED BY 'YOUR_STRONG_PASSWORD';

GRANT SELECT ON niushop_b2c_v5.ns_goods TO 'recommend_ro'@'%';
GRANT SELECT ON niushop_b2c_v5.ns_goods_sku TO 'recommend_ro'@'%';
GRANT SELECT ON niushop_b2c_v5.ns_goods_category TO 'recommend_ro'@'%';
GRANT SELECT ON niushop_b2c_v5.ns_goods_weapp TO 'recommend_ro'@'%';
GRANT SELECT ON niushop_b2c_v5.ns_goods_evaluate TO 'recommend_ro'@'%';
GRANT SELECT ON niushop_b2c_v5.ns_goods_evaluate_append TO 'recommend_ro'@'%';
GRANT SELECT ON niushop_b2c_v5.ns_article TO 'recommend_ro'@'%';
GRANT SELECT ON niushop_b2c_v5.ns_article_category TO 'recommend_ro'@'%';
GRANT SELECT ON niushop_b2c_v5.ns_member_super_card_evaluate TO 'recommend_ro'@'%';
GRANT SELECT ON niushop_b2c_v5.ns_weapp TO 'recommend_ro'@'%';

FLUSH PRIVILEGES;
```

若需超级卡档位名称，可额外：`GRANT SELECT ON niushop_b2c_v5.ns_member_level`。

**禁止**授予：`ns_member`、`ns_pay`、`ns_config`、`ns_order` 等（含手机号、openid、支付配置）。

### 2.3 连接字符串示例

**Python（pymysql）**：

```python
import pymysql
conn = pymysql.connect(
    host="127.0.0.1",
    port=13306,
    user="recommend_ro",
    password="YOUR_STRONG_PASSWORD",
    database="niushop_b2c_v5",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
)
```

---

关于链接库表用的 用户名 密码 做成 配置项 放配置文件里

## 三、业务常量（推荐系统必用）


| 常量             | 值                               | 说明                                   |
| -------------- | ------------------------------- | ------------------------------------ |
| `site_id`      | **1**                           | 当前单站点                                |
| `weapp_id` 栖月汇 | **11**                          | AppID `wxcfdbf13a14f27b97`，**默认推荐端** |
| `weapp_id` 源仓集 | 10                              | 未全上线前聊天推荐可暂不推                        |
| `weapp_id` 聚味台 | 9                               | 同上                                   |
| 商品上架           | `goods_state=1` 且 `is_delete=0` |                                      |
| 文章发布           | `status=1`                      | 0=草稿                                 |
| 评价展示           | `is_show=1` 且 `is_audit=1`      | 1=审核通过                               |


**图片域名**：`https://yanpanji.com/` + 库内相对路径（如 `upload/1/common/images/...`）。

**小程序商品详情路径**：

```text
/pages_sub/goods/detail?goods_id={goods_id}
```

---

## 四、表关系总览

```text
ns_goods ──< ns_goods_sku          (goods_id)
ns_goods ──< ns_goods_weapp        (goods_id, weapp_id)  ← C 端必过滤
ns_goods ──< ns_goods_evaluate     (goods_id)
ns_goods_evaluate ──< ns_goods_evaluate_append (evaluate_id)
ns_goods.category_id ── ns_goods_category (逗号分隔 ID)
ns_article ── ns_article_category   (category_id)
ns_member_level ──< ns_member_super_card_evaluate (level_id)
```

---

## 五、商品库

### 5.1 核心表


| 物理表                 | 用途                         |
| ------------------- | -------------------------- |
| `ns_goods`          | 商品 SPU：名称、主图、详情、分类、销量、评价汇总 |
| `ns_goods_sku`      | SKU：规格、价格、库存               |
| `ns_goods_category` | 商品分类（最多三级）                 |
| `ns_goods_weapp`    | **按小程序可见**（列表必须 JOIN）      |


### 5.2 `ns_goods` 推荐字段


| 字段                          | 说明          |
| --------------------------- | ----------- |
| `goods_id`                  | 主键          |
| `goods_name`                | 商品名         |
| `introduction`              | 促销语         |
| `keywords`                  | 关键词（NLP 匹配） |
| `goods_content`             | 详情 HTML     |
| `goods_image`               | 主图（逗号分隔）    |
| `category_id`               | 分类 ID，逗号分隔  |
| `price` / `market_price`    | 展示价 / 划线价   |
| `goods_state`               | 1=上架        |
| `is_delete`                 | 0=正常        |
| `sale_num` + `virtual_sale` | 销量展示        |
| `evaluate_haoping` 等        | 好/中/差评数     |
| `label_name`                | 商品分组        |
| `recommend_way`             | 1新品 2精品 3推荐 |


### 5.3 `ns_goods_sku` 推荐字段


| 字段                        | 说明                                    |
| ------------------------- | ------------------------------------- |
| `sku_id`                  | SKU 主键（默认 SKU 与 `ns_goods.sku_id` 一致） |
| `discount_price`          | 活动价                                   |
| `self_shop_special_price` | 栖月汇专享价                                |
| `stock`                   | 库存                                    |


### 5.4 `ns_goods_category`


| 字段                   | 说明                     |
| -------------------- | ---------------------- |
| `category_id`        | 主键                     |
| `category_name`      | 分类名                    |
| `category_full_name` | 全路径，如 `明星品/调肤`         |
| `is_show`            | **0=显示，-1=不显示**（与直觉相反） |


### 5.5 `ns_goods_weapp`（必过滤）

```sql
INNER JOIN ns_goods_weapp gw
  ON gw.goods_id = g.goods_id
 AND gw.weapp_id = 11
 AND gw.is_show = 1
```

---

## 六、文章与类目

### 6.1 表


| 物理表                   | 用途               |
| --------------------- | ---------------- |
| `ns_article`          | 文章（HTML，常内嵌商品链接） |
| `ns_article_category` | 文章栏目             |


### 6.2 `ns_article` 推荐字段


| 字段                                   | 说明             |
| ------------------------------------ | -------------- |
| `article_id`                         | 主键             |
| `weapp_id`                           | 按端可见（栖月汇多为 11） |
| `article_title` / `article_abstract` | 标题 / 摘要（推荐语料）  |
| `article_content`                    | 正文 HTML        |
| `category_id`                        | 栏目             |
| `status`                             | 1=已发布          |
| `create_time`                        | Unix 时间戳       |


### 6.3 文章 ↔ 商品

正文 HTML 中常见：

```text
/pages_sub/goods/detail?goods_id=41
```

可用正则抽取 `goods_id`，用于「聊功效 → 推对应商品」。

---

## 七、评价库

### 7.1 商品评价


| 物理表                        | 用途      |
| -------------------------- | ------- |
| `ns_goods_evaluate`        | 首评      |
| `ns_goods_evaluate_append` | 追评（可多条） |


关键字段：`goods_id`、`content`、`scores`（1~5）、`explain_type`（1好2中3差）、`is_show`、`is_audit`、`create_time`。

### 7.2 超级会员卡评价


| 物理表                             | 说明                              |
| ------------------------------- | ------------------------------- |
| `ns_member_super_card_evaluate` | 购卡评价，**不在** `ns_goods_evaluate` |


---

## 八、示例 SQL

### 8.1 栖月汇可售商品清单

```sql
SELECT
  g.goods_id,
  g.goods_name,
  g.introduction,
  g.keywords,
  g.price,
  g.goods_image,
  g.category_id,
  gs.discount_price,
  gs.stock
FROM ns_goods g
INNER JOIN ns_goods_weapp gw
  ON gw.goods_id = g.goods_id AND gw.weapp_id = 11 AND gw.is_show = 1
INNER JOIN ns_goods_sku gs
  ON gs.sku_id = g.sku_id AND gs.is_delete = 0
WHERE g.site_id = 1
  AND g.goods_state = 1
  AND g.is_delete = 0
ORDER BY g.sort DESC, g.goods_id DESC;
```

### 8.2 商品分类

```sql
SELECT category_id, pid, level, category_name, category_full_name
FROM ns_goods_category
WHERE site_id = 1 AND is_show = 0
ORDER BY level, sort;
```

### 8.3 已发布文章

```sql
SELECT a.article_id, a.article_title, a.article_abstract,
       c.category_name, a.cover_img, a.create_time
FROM ns_article a
LEFT JOIN ns_article_category c ON c.category_id = a.category_id
WHERE a.site_id = 1 AND a.status = 1
ORDER BY a.sort DESC, a.article_id DESC;
```

### 8.4 某商品好评语料

```sql
SELECT content, scores, create_time
FROM ns_goods_evaluate
WHERE site_id = 1 AND goods_id = ?
  AND is_show = 1 AND is_audit = 1 AND explain_type = 1
  AND content <> ''
ORDER BY create_time DESC
LIMIT 20;
```

---

## 九、聊天推荐输出模板

```json
{
  "goods_id": 41,
  "goods_name": "重组胶原蛋白紧致淡纹精华水",
  "price": "128.00",
  "cover_url": "https://yanpanji.com/upload/1/common/images/...",
  "mini_path": "/pages_sub/goods/detail?goods_id=41",
  "one_line_pitch": "促销语或文章摘要",
  "social_proof": "打卡第五天，皮肤越来越亮…"
}
```

---

## 十、安全与合规

1. 只读账号仅 `SELECT`；禁止读 `ns_config`（支付密钥）。
2. 不批量导出会员手机号、完整 openid。
3. 大字段（`goods_content`、`article_content`）建议定时同步到外部向量库，避免高频全表扫。
4. 聊天主推 **weapp_id=11**；10/9 需确认 `goods_weapp` 已配置。

---

## 十一、相关文档


| 文档                                                              | 内容                      |
| --------------------------------------------------------------- | ----------------------- |
| `docs/site1-三小程序并存-技术实现与实施方案.md`                                | 三端 weapp_id、goods_weapp |
| `docs/niushop_b2c_v5.sql`                                       | 全库 DDL                  |
| `docs/sql/site1_goods_weapp_schema_and_historical_backfill.sql` | goods_weapp 说明          |


---

## 十二、变更记录


| 版本   | 日期         | 说明  |
| ---- | ---------- | --- |
| v1.0 | 2026-06-16 | 首版  |



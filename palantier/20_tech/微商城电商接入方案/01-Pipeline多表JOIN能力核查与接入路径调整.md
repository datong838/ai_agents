# Niushop 案例 · Pipeline 多表 JOIN 能力核查与接入路径调整

| 字段 | 内容 |
|------|------|
| 状态 | **方案 only · 暂不编码** |
| 版本 | **v1.0** · 2026-07-19 |
| 目录 | `docs/palantier/20_tech/niushop电商案例/` |
| 关联 | [00 整体孪生主方案 v2.0](00-Niushop微商城AOS对接方案.md) · [05 产品](../../05-数据集成Connectors-Pipeline-Dataset产品方案.md) · [T05](../T05-L1数据集成详细技术方案.md) · [36](../36-T4.6-MySQL去stub方案.md) · [39](../39-T4.4b-文件解析插件方案.md) |
| 目的 | ① 核实 Pipeline Builder 多表 JOIN；② 支撑栖月汇 **整体孪生** 中商品多子表接入；③ 缺口回馈平台 |

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 中文 | 全文中文 |
| 先方案后代码 | 只出文档；不改 Host/Pipeline 实现 |
| 零行业定制码 | 缺 Join → 记平台缺口；临时用库侧 VIEW / 分表+Link |
| 新文档落点 | **仅本电商案例目录** |
| 上线态诚实 | 产品页有 Join 蓝图叙事 ≠ live 能力 |

---

## 1. 核查结论（直接回答）

### 1.1 Pipeline Builder 多表 JOIN —— **当前不可用（非 live）**

| 层 | 现状 |
|----|------|
| 产品目标 / 蓝图 | [05](../../05-数据集成Connectors-Pipeline-Dataset产品方案.md) Transform 含 **Filter · Join · Aggregate**；foundry HTML 有 Join 节点示意 |
| `/data/pipelines` UI | 列表壳 + sourceId 过滤 + 试跑壳；**无 DAG、无 Join 算子编辑** |
| API `POST /v1/pipelines` | 内存 CRUD；create 即假 SUCCEEDED；**无 transforms / nodes / SQL** |
| `jdbc-mysql` | **单表** `SELECT * FROM table`（env/`AOS_MYSQL_TABLE`）；**无多表、无自定义 JOIN SQL 面** |

**判定：** 多表 JOIN 是 **目标态能力点**，本案例正好用来 **检验并暴露缺口**；**不能**把首波孪生建立在「PB 里拖 Join」上。

### 1.2 对「商品 JDBC + 订单 Excel」的评价（纳入整体孪生 v2.0）

| 想法 | 结论 |
|------|------|
| 商品多子表要 Join | JDBC ✅；Join 用 VIEW 或分表+Link（PB Join 非 live） |
| 订单 Excel | ✅ **全字段孪生包**（非抽样）；运行态感知仍要 **JDBC Schedule** |
| 整体孪生 | 见 [00 v2.0](00-Niushop微商城AOS对接方案.md)：T0～T6 均以 JDBC 为主，Excel/Media 为辅 |

---

## 2. 商品族：有哪些「子表」（JDBC 采集范围）

> 交易落点永远是 **SKU**。首波 JOIN/VIEW 只需 **主链**；评价/购物车等可后置。

### 2.1 P0（必须进 JDBC）

| 角色 | 表 | 与主表关系 |
|------|-----|------------|
| SPU 主表 | `ns_goods` | PK `goods_id` |
| SKU 子表 | `ns_goods_sku` | `goods_id` → goods |
| 端可见 | `ns_goods_weapp` | `goods_id` + `weapp_id` |
| 分类（维） | `ns_goods_category` | `goods.category_id` 引用 |

### 2.2 P1（有门店/体验再加）

| 角色 | 表 |
|------|-----|
| 引流槽位 | `ns_goods_share_lead` |
| 门店 SKU | `ns_store_goods` / `ns_store_goods_sku` |
| 分类×端 | `ns_goods_category_weapp` |

### 2.3 首波不做 JDBC 宽表的

`goods_cart`、`goods_evaluate*`、`goods_collect`、`goods_browse`、次卡全套 —— 行为/卫星域，不挡商品主数据孪生。

---

## 3. 在「无 PB Join」前提下怎么用好多表（配置态）

### 3.1 路径 A（推荐 · 检验 Ontology Link）

```text
jdbc-mysql Source（SSH 隧道）
  → Sync ns_goods        → Dataset goods
  → Sync ns_goods_sku    → Dataset sku
  → Sync ns_goods_weapp  → Dataset goods_weapp
  → Sync ns_goods_category → Dataset category
        │
        ▼
  Ontology Link：GoodsSku.ofGoods / Goods.onWeapp / …
```

**优点：** 完全走现有 live 能力；直接检验「分表 + Link」是否好用。  
**缺点：** 运营一屏宽表要自己拼（Inbox/COP 用 ObjectSet）。

### 3.2 路径 B（推荐 · 检验「宽表采集」而不假装 PB Join）

在 **线上只读库**（或隧道可达库）建 **只读 VIEW**（运维/DBA 配，非 AOS 业务码）：

```sql
-- 示意：商品主链宽表（只读账号可 SELECT）
CREATE OR REPLACE VIEW v_aos_goods_sku_flat AS
SELECT
  g.goods_id,
  g.goods_name,
  g.goods_state,
  g.category_id,
  g.weapp_id AS goods_default_weapp,  -- 若列不存在则删
  s.sku_id,
  s.price,
  s.stock,
  s.self_shop_special_price,
  w.weapp_id AS visible_weapp_id
FROM ns_goods g
JOIN ns_goods_sku s ON s.goods_id = g.goods_id
LEFT JOIN ns_goods_weapp w ON w.goods_id = g.goods_id
WHERE g.is_delete = 0;
```

然后 `jdbc-mysql` 仍按 **单表/单 VIEW** 采集 → 一个 Dataset。

**优点：** 用真实多表 Join 语义检验「宽表入湖」；**不伪造** PB Join。  
**平台债：** 「本该在 Pipeline Builder 配 Join」→ 记入 §5 缺口。

### 3.3 路径 C（明确后置）

等平台补齐：**Pipeline DAG + Join 算子** 或 **Sync 自定义 SQL** 后，把 VIEW 迁回 PB 配置 —— 案例不写死 Niushop Join 插件。

---

## 4. 订单走 Excel：怎么选、怎么验

### 4.1 建议工作簿（孪生全字段 · 见 [02](02-Excel与Word-PDF夹具清单.md)）

| 文件 | Sheet | 用途 |
|------|-------|------|
| `mall-order.xlsx` | `orders`（`ns_order` **全列**）+ `order_lines`（`ns_order_goods` **全列**） | 订单数字孪生主数据 |
| `mall-goods.xlsx` | goods/sku/… 全列 | 与 JDBC 对照 / 离线包 |

导出原则：线上真实行、**不加 LIMIT**、**不砍列**；文件私有 gitignore。

> 曾用「抽样 10 列」是错误口径，已废止。

### 4.2 与商品 JDBC 的故事怎么讲

| 分钟 | 动作 |
|------|------|
| 1 | `/data`：jdbc-mysql 探活；商品分表或 VIEW Dataset 绿 |
| 2 | Ontology：Goods↔Sku Link（或宽表属性） |
| 3 | 上传订单 Excel → media-sets / parsers → 预览行 |
| 4 | （可选）订单 JDBC Sync 一条，与 Excel 同 `order_id` 对照 |
| 5 | 话术：「主数据实时库采；交易抽样文件采；PB Join 缺口已登记」 |

### 4.3 态势感知口径（与 00 §9 对齐）

- **仅 Excel 订单：** 感知 =「重新导出并上传后」才更新 —— 可接受为 **文件路径检验**，不可宣称分钟级态势。  
- **要分钟级：** 订单必须加 JDBC Schedule（商品仍 JDBC；Excel 仍保留作解析夹具）。

---

## 5. 平台缺口台账（本案例回馈）

| ID | 现象 | 期望通用能力 | 优先级 | 对本案例影响 |
|----|------|--------------|--------|--------------|
| **G-PB-01** | Pipeline 无 Join 算子 / 无 DAG | Pipeline Builder：等值 Join（内/左）、预览、产出 Dataset | **P0** | 商品多子表无法在 PB 内合并 |
| **G-PB-02** | Pipeline 无自定义 SQL Transform | SQL 节点或 Sync query 面 | P0 | 无法在 AOS 内写 JOIN |
| **G-JDBC-01** | jdbc-mysql 仅单表 env | Source 级多表/多 query 配置 | P0 | 多 Dataset 要多次绑表或靠 VIEW |
| **G-PB-03** | `/data/pipelines` 画布壳 | 真编辑器 | P1 | 易用性差 |

> 关闭方式：平台波次补通用能力；**禁止** `niushop-join` 专用包。

---

## 6. 调整后的接入总表（覆盖 00 方案 §5）

| 域 | 接入方式 | 形态 | 必测 |
|----|----------|------|------|
| 商品 SPU/SKU/可见/分类 | **JDBC** | 路径 A 分表+Link **或** 路径 B VIEW | ✅ |
| 门店商品等 | JDBC | P1 | ○ |
| 订单头/行 | **Excel** | `mall-order-sample.xlsx` → parsers + MediaSet | ✅ |
| 订单运行态（态势） | JDBC Schedule | 可选；要 §9 必达则升 ✅ | ○→按目标 |
| 协议/文章/帮助 | Word | 另存 docx | ✅（NS.D） |
| 商品介绍/客服 | PDF | MediaSet | ✅（NS.D） |
| SKU 主数据对照 | Excel（可选） | `mall-sku-master.xlsx` 与 JDBC 对照 | ○ |

---

## 7. 验收（本专项）

- [ ] 评审知悉：**PB 多表 JOIN 非 live**；缺口 G-PB-01/02、G-JDBC-01 已登记  
- [ ] 商品：至少 `goods`+`sku` JDBC 可预览；Link 或 VIEW 宽表二选一可讲清  
- [ ] 订单：Excel 上传解析 `ok`，中文列可见  
- [ ] 未引入 Niushop 专用 Join 代码  
- [ ] 若宣称态势感知分钟级 → 订单 JDBC Schedule 已配，否则话术降级为文件路径  

---

## 8. 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-07-19 | 初版：JOIN 核查；商品 JDBC / 订单 Excel；平台缺口 |

---

*v1.0 · 放在 `niushop电商案例/` · 方案 only*

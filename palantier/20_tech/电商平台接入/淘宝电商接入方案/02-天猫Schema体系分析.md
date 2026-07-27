# 02 · 天猫 Schema 体系分析

> **版本**：v1.0 · 2026-07-22
> **状态**：P1 调研完成 · 天猫商品发布/更新的 Schema XML 体系深度分析
> **关联**：[00-总体分析计划](./00-淘宝天猫AOS对接方案-总体分析计划.md) · [01-TOP-API接口清单](./01-TOP-API接口清单.md)

---

## 1. 为什么需要 Schema 分析

天猫（品牌旗舰店）与淘宝 C 店的核心差异在于「商品发布」环节：

| 平台 | 商品发布方式 | 特点 |
|------|------------|------|
| 淘宝 C 店 | field-level API：`taobao.item.add` / `taobao.item.update` | 参数写死，类目属性平铺 |
| 天猫品牌店 | **Schema XML 体系**：`tmall.item.add.schema.get` → 组装 XML → `tmall.item.schema.add` | 规则动态下发，类目属性动态变化 |

**对 AOS 的影响**：
- 读操作（Source Sync）淘宝和天猫完全一致 → **无差异**
- 写回 Action 中，天猫商品创建/更新需要 **动态解析 Schema XML** → **需要独立的 Schema 适配模块**

---

## 2. 天猫商品发布完整链路

```
步骤一：准备工作                        步骤二：产品匹配（天猫必做）
─────────────                       ─────────────────────
taobao.user.seller.get              tmall.product.match.schema.get
  └─ 判断店铺类型（天猫）               └─ 获取产品匹配规则 XML
                                     tmall.product.schema.match
taobao.itemcats.authorize.get          └─ 执行产品匹配 → product_id
  └─ 获取授权类目 + 品牌              tmall.product.schema.get
                                        └─ 检查 can_publish_item=true
taobao.itemcats.get                  ─ OR ─
  └─ 获取叶子类目 cid               tmall.product.add.schema.get
                                        └─ 无匹配：获取产品发布规则
                                     tmall.product.schema.add
                                        └─ 发布新产品 → product_id

步骤三：商品发布                       步骤四：图片上传（异步）
─────────────                       ─────────────────
tmall.item.add.schema.get           taobao.picture.upload
  ├─ category_id=xxx                  └─ 获取图片 URL
  ├─ product_id=xxx
  └─ isv_init=false                tmall.item.schema.add
  └─ 返回：Schema XML（规则）          ├─ category_id=xxx
                                       ├─ product_id=xxx
组装商品 XML（按规则填充）              └─ xml_data=<组装好的商品XML>
  └─ 每个 field 的 value 必填         └─ 返回：item_id
```

**关键流程节点**（AOS 需要处理的）：
1. 动态获取类目规则（不可硬编码）
2. 产品匹配/创建（天猫特有步骤，淘宝不需要）
3. Schema XML 解析 → 商品 XML 生成（核心能力）
4. 图片先上传 → URL 再填入 XML

---

## 3. Schema XML 结构详解

### 3.1 整体结构

```xml
<rules>
  <field id="title" name="商品标题" type="input">
    <rules>
      <rule name="requiredRule" value="true"/>
      <rule name="maxLengthRule" value="30"/>
      <rule name="minLengthRule" value="1"/>
      <rule name="valueTypeRule" value="text"/>
    </rules>
    <value type="text"/>
  </field>
  
  <field id="price" name="一口价" type="input">
    <rules>
      <rule name="requiredRule" value="true"/>
      <rule name="valueTypeRule" value="decimal"/>
      <rule name="minValueRule" value="0.01" exProperty="include"/>
      <rule name="maxValueRule" value="99999999.00" exProperty="include"/>
      <rule name="tipRule" value="一口价应在销售属性表中所填最高与最低价格范围区间内"/>
    </rules>
    <value type="decimal"/>
  </field>
  
  <field id="prop_20000" name="品牌" type="singleCheck">
    <rules>
      <rule name="requiredRule" value="true"/>
    </rules>
    <options>
      <option displayName="Apple/苹果" value="3245678"/>
      <option displayName="Huawei/华为" value="3245679"/>
    </options>
    <value type="single"/>
  </field>
  
  <field id="sku" name="销售属性" type="multiComplex">
    <!-- 可重复的复合结构，每个实例为一个 SKU -->
    <complex-values>
      <complex-value>
        <field id="prop_xxx" name="颜色" type="singleCheck">
          <options>...</options>
        </field>
        <field id="prop_yyy" name="尺寸" type="singleCheck">
          <options>...</options>
        </field>
        <field id="price" name="价格" type="input">...</field>
        <field id="quantity" name="库存" type="input">...</field>
        <field id="barcode" name="条形码" type="input">...</field>
      </complex-value>
    </complex-values>
  </field>
</rules>
```

### 3.2 Field Type（7 种）

| Type | 说明 | HTML 类比 | 典型场景 | AOS 表单控件 |
|------|------|----------|---------|-------------|
| `input` | 文本输入 | `<input type="text">` | 商品标题、价格、货号 | TextInput / NumberInput |
| `multiInput` | 多行文本 | `<textarea>` | 商品描述、卖点 | TextArea |
| `singleCheck` | 单选 | `<input type="radio">` | 品牌、性别、是否保修 | RadioGroup / Select |
| `multiCheck` | 多选 | `<input type="checkbox">` | 适用人群、特色服务 | CheckboxGroup |
| `complex` | 复合结构 | 嵌套字段组 | 特定业务的聚合信息 | FieldGroup 组件 |
| `multiComplex` | 可重复复合结构 | 可增删行 | **SKU 列表**（最重要的类型） | DynamicTable / Repeater |
| `label` | 纯说明信息 | `<p>` / `<span>` | 温馨提示、合规说明 | Text 只读展示 |

### 3.3 Rule 类型（18 种）

| Rule | 作用 | 支持 type | AOS 校验映射 |
|------|------|----------|------------|
| `valueTypeRule` | 值类型：text / decimal / integer / date / long / url / textarea / html | input, multiInput | Prop 类型定义 |
| `requiredRule` | 是否必填 | 全部 | `required` 标记 |
| `disableRule` | 根据依赖条件，field 是否禁用（跳过校验） | 全部 | 条件可见性 |
| `maxLengthRule` | 最大长度 | input, multiInput | `maxLength` 校验 |
| `minLengthRule` | 最小长度 | input, multiInput | `minLength` 校验 |
| `maxValueRule` | 最大值（支持开闭区间 `exProperty`） | input, multiInput | `max` 校验 |
| `minValueRule` | 最小值（支持开闭区间 `exProperty`） | input, multiInput | `min` 校验 |
| `maxInputNumRule` | 最多可选数 | input, multiInput, singleCheck, multiCheck | 多选数量上限 |
| `minInputNumRule` | 至少选数 | input, multiInput, singleCheck, multiCheck | 多选数量下限 |
| `maxTargetSizeRule` | 最大文件大小（kb/mb/gb） | input, multiInput, singleCheck, multiCheck | 文件大小校验 |
| `minTargetSizeRule` | 最小文件大小 | input, multiInput, singleCheck, multiCheck | 文件大小校验 |
| `readOnlyRule` | 只读 | 全部 | `readonly` / `disabled` |
| `regxRule` | 正则表达式 | input, multiInput | `pattern` 校验 |
| `tipRule` | **提示信息**（必须透出给用户） | 全部 | 前端 Tooltip / Alert |
| `devTipRule` | 开发者提示（不展示给用户） | 全部 | 后端日志 |
| `maxImageSizeRule` | 最大图片分辨率 | input, multiInput, singleCheck, multiCheck | 图片尺寸校验 |
| `minImageSizeRule` | 最小图片分辨率 | input, multiInput, singleCheck, multiCheck | 图片尺寸校验 |
| `—` | `depend-group` + `depend-express` | 全部 | 条件依赖逻辑 |

### 3.4 依赖关系（depend-group）

```
depend-group
├── operator: "and" | "or"    ← 逻辑组合
└── depend-express[]
    ├── fieldId                ← 依赖哪个 field
    ├── value                  ← 依赖的值
    └── symbol                 ← 比较符号
        ├── is null
        ├── == / !=
        ├── > / < / >= / <=
        ├── contains / not contains
        ├── this field's value in fieldOptions
        └── this field's value not in fieldOptions
```

**示例**：`item_status` 为 "定时上架"（值=1）时才需要填写 `list_time`：
```xml
<field id="list_time" name="开始时间">
  <rules>
    <rule name="disableRule" value="true"/>
  </rules>
  <depend-group operator="and">
    <depend-express fieldId="item_status" value="1" symbol="!="/>
  </depend-group>
</field>
```

---

## 4. 版本变更：旧 Schema → 新 Schema

> **重要提示**：淘宝旧版 Schema 接口（`taobao.item.add.schema.get` 等）已逐步下线。

| 阶段 | 旧 Schema（已下线/逐步下线） | 新 Schema（当前维护） |
|------|---------------------------|---------------------|
| 商品规则获取 | `taobao.item.add.schema.get` | `alibaba.item.publish.schema.get` |
| 级联属性获取 | — | `alibaba.item.publish.props.get` |
| 商品发布 | `taobao.item.schema.add` | `alibaba.item.publish.submit` |
| 商品编辑（Schema） | `taobao.item.update.schema.get` + `taobao.item.schema.update` | **仍为** `tmall.item.update.schema.get` + `tmall.item.schema.update` |
| 增量更新 | `tmall.item.increment.update.schema.get` | **不变** |

> **AOS 应对策略**：优先对接天猫 Schema 体系（`tmall.*`），淘宝 C 店用 field-level API（`taobao.item.add`/`taobao.item.update`）；如果新 Schema 体系稳定后再评估迁移。

---

## 5. 增量更新 vs 全量更新

| 维度 | 增量更新 | 全量更新 |
|------|---------|---------|
| **适用场景** | 标题、子标题、描述、竖图等 9 种元素 | 除增量字段外的所有其他信息 |
| **规则获取** | `tmall.item.increment.update.schema.get(item_id, update_fields)` | `tmall.item.update.schema.get(item_id)` |
| **执行 API** | `tmall.item.schema.increment.update` | `tmall.item.schema.update` |
| **XML 构造** | 仅传需更新的 field | 所有 field 的 default-value 全部回传（即使不修改） |
| **支持元素** | TITLE / SUBTITLE / SHORT_TITLE / DESC / WAP_DESC / FENQIGOU / VERTICAL_IMAGE / DRESS_ONLY_FOR_TMALL / SHOP_SAME_STYLE | 全部 |
| **价格/库存** | 独立接口：`tmall.item.price.update` / `taobao.item.quantity.update` | — |
| **AOS 实现难度** | 低（按需构造小 XML） | 高（需全量规则解析 + 全部 field 回传） |

**AOS 推荐策略**：
- Phase 1（当前阶段）：仅支持增量更新（标题/描述修改 + 价格更新 + 库存同步）
- Phase 2（平台成熟后）：全量更新（需要完整 Schema 解析器）

---

## 6. AOS 对接 Schema 体系的核心挑战

### 6.1 "动态映射" 是最大难点

| 传统方式 | 天猫 Schema 方式 |
|---------|---------------|
| 参数写死在代码里：`req.title = "xxx"` | 动态解析 XML 规则 → 动态生成表单 → 用户填写 → 动态生成商品 XML |
| 类目变更 → 改代码 | 类目变更 → 规则 XML 自动变化 → 表单随规则变化 |
| 前端硬编码校验 | 前端根据 `requiredRule` / `maxLengthRule` 等动态生成校验 |

### 6.2 AOS 需要的 Schema 能力

```
AOS 系统                          天猫 TOP
────────                          ────────

┌──────────────────┐     ┌─────────────────────────┐
│ Schema 解析器     │────▶│ tmall.item.add.schema    │
│ （通用平台）       │     │ .get → Schema XML         │
│                  │     └─────────────────────────┘
│ ├ Field 解析      │     ┌─────────────────────────┐
│ ├ Rule 解析       │     │ tmall.item.schema.add    │
│ ├ Depend 解析     │     │ ← 商品 XML               │
│ └ Default 填充    │     └─────────────────────────┘
│                  │
│ Schema → 表单映射  │     ┌─────────────────────────┐
│ （前端组件工厂）    │     │ 生成的商品 XML            │
│ ├ input→TextInput │     │ <item>                  │
│ ├ singleCheck→Sel │     │   <title>...</title>     │
│ ├ multiComplex→   │     │   <price>99.00</price>  │
│ │   DynamicTable  │     │   <sku>...</sku>         │
│ └ rule→validator  │     │ </item>                 │
└──────────────────┘     └─────────────────────────┘
```

### 6.3 四大对接原则

| # | 原则 | AOS 实现 |
|----|------|---------|
| 1 | **变更检测** | 每天 `isv_init=true` 拉取类目规则 → 对比 XML 差异 → 告警通知 |
| 2 | **动态映射** | 不写死参数映射，运行时根据 Schema XML 生成表单 |
| 3 | **关注 Type** | 基于 Field Type 选择前端组件，业务字段由动态映射处理 |
| 4 | **增量优先** | Phase 1 只做增量更新（成本低），Phase 2 再补全量更新 |

---

## 7. 回馈通用平台的需求

接入天猫 Schema 体系暴露的通用平台缺口：

| # | 需求 | 说明 | 优先级 |
|----|------|------|-------|
| G1 | **动态 Schema 解析引擎** | 通用的 XML Schema → 表单 映射引擎（不限于天猫，可复用到京东/拼多多等平台的属性动态化场景） | 🟡 W2 |
| G2 | **Depend-Group 表达式引擎** | 条件依赖的解析和校验（`depend-express` → 前端条件显示/隐藏逻辑） | 🟡 W2 |
| G3 | **MultiComplex 动态表格组件** | 可增删行的复合结构表单组件（SKU 矩阵是电商通用模式） | 🟡 W2 |
| G4 | **Rule→Validator 自动映射** | 18 种 Schema Rule → 前端/后端校验器的自动生成 | 🟢 W3 |

---

> **版本**：v1.0 · 2026-07-22 · P1 调研完成
>
> **变更日志**：
>
> | 版本 | 日期 | 说明 |
> | --- | --- | --- |
> | v1.0 | 2026-07-22 | 初版 · Schema 7 种 Type · 18 种 Rule · Depend-Group 机制 · 新/旧版本变更 · AOS 对接挑战 |

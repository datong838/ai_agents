# TitanIndustries · 端到端接入详解

> **版本**：v1.0 · 2026-07-23
> **参照**：`../000-电商平台接入总方案.md` Stage 1-6 框架
> **定位**：Palantir 官方 O2C（订单到现金）最佳实践，全部电商/零售平台接入的架构蓝本
> **源系统**：SAP S/4HANA（CDS View 模式）
> **核心场景**：流程挖掘 + AI 信用冻结决策 + BAPI 写回闭环

---

## Stage 1 · 数据接入（HyperAuto SDDI）

### 1.1 连接架构

与电商平台完全不同——TitanIndustries 走 **HyperAuto（SDDI）** 路径，而非手写 Connector。

```
SAP S/4HANA
  │
  ├── 透明表（EKKO / EKPO / VBAK / VBAP / MARA / KNA1 / KNKK …）
  ├── CDS View（I_SalesOrder / I_PurchaseOrder / I_Material …）
  └── HANA View / BW Extractor
  │
  ▼
[HyperAuto · 三层编排器]
  │
  ├── Layer 1 · Data Syncs      → 自动推导同步方式
  ├── Layer 2 · Builder Pipelines → 自动重命名 + 自动 Join + 清洗
  └── Layer 3 · Ontology         → 自动生成 OT + Property + Link Type
  │
  ▼
[Foundry Datasets + Ontology Objects]  ← 分钟级、零人工干预
```



### 1.2 连接器配置


| 项     | 配置                                             |
| ----- | ---------------------------------------------- |
| 连接器类型 | **SAP ERP Connector**（Foundry 内置）              |
| 连接方式  | Direct 或 Remote (via Gateway)                  |
| 目标系统  | SAP S/4HANA（CDS View 模式推荐）                     |
| 认证    | SAP 用户名/密码 或 SAML SSO                          |
| Agent | 如 SAP 在内网：部署 Agent Worker + Agent Proxy Egress |




### 1.3 Source 创建

```
Step 1 · Data Connection → + New Source → SAP ERP
Step 2 · Connection type: Direct（同网络）或 Remote (via Gateway)
Step 3 · 命名: titan-s4-prod
Step 4 · 配置:
  SAP Host: s4hana.titanindustries.com
  Client: 100
  User: FOUNDRY_RO
  Password: ****
Step 5 · 启用 HyperAuto → Source Explorer 浏览 SAP 模块
```



### 1.4 HyperAuto 自动四步

HyperAuto 不是 ETL 工具，它是 **SDDI（Software-Defined Data Integration）**——用源系统的 metadata 来"推导"整条管道。


| 步骤                  | HyperAuto 自动行为                 | TitanIndustries 场景实例                                          |
| ------------------- | ------------------------------ | ------------------------------------------------------------- |
| **① 源表探查**          | 读取 SAP 元数据，实时查询源系统             | 识别 VBAK/VBAP/KNA1/MARA/KNKK 等表结构                              |
| **② 自动重命名**         | 用 SAP 元数据翻译技术列名                | `EKPO~NETPR` → "Net Price"；`VBAP~NETWR` → "Net Order Value"   |
| **③ 自动 Join**       | 理解 SAP 数据模型，规范化分表 join 成宽表     | VBAK(头) ⋈ VBAP(行) ⋈ KNA1(客户) ⋈ MARA(物料)                       |
| **④ 自动生成 Ontology** | 动态创建 OT + Property + Link Type | Sales Order / Sales Order Item / Customer / Product + 自动 Link |


> **核心价值**：传统 ETL 团队数周才能理解的 SAP 表结构，HyperAuto 在**分钟级**完成从 source 到 Ontology 的映射。



### 1.5 SAP 表 → Ontology 对象映射

基于 SAP 标准数据模型 + HyperAuto 工作机制的推断映射（实际以 HyperAuto 自动生成结果为准）。

#### 销售与分销（SD）模块


| SAP 表         | 表含义   | 推断的 Ontology 对象      | 关键属性映射                                                                |
| ------------- | ----- | -------------------- | --------------------------------------------------------------------- |
| **VBAK**      | 销售文档头 | **Sales Order**      | VBELN→order_id, KUNNR→customer_id, VDATU→delivery_date                |
| **VBAP**      | 销售文档项 | **Sales Order Item** | POSNR→line_no, MATNR→material_id, NETWR→net_value, EDATU→created_date |
| **KNA1**      | 客户主数据 | **Customer**         | KUNNR→customer_id, NAME1→name, KTOKD→classification                   |
| **MARA**      | 物料主数据 | **Product**          | MATNR→material_id, MTART→type, MEINS→uom                              |
| **LIKP/LIPS** | 交货头/项 | **Delivery**         | VBELN→delivery_id, WADAT→actual_ship_date                             |
| **VBRK/VBRP** | 开票头/项 | **Invoice**          | VBELN→invoice_id, NETWR→amount                                        |


> **流程挖掘关键**：Process Object Dataset 选用 **VBAP**（销售订单行），这是官方 Demo 确认的。



#### 信用与财务


| SAP 表             | 推断的 Ontology 对象     | 关键属性            |
| ----------------- | ------------------- | --------------- |
| **KNKK**（客户信用主数据） | **Customer Credit** | 信用额度、信用冻结状态、风险类 |
| **BSID/BSAD**     | **Payment History** | 用于计算 12 个月按时付款率 |




#### 采购（MM）模块


| SAP 表 | 推断的 Ontology 对象   |
| ----- | ----------------- |
| EKKO  | Purchase Order    |
| EKPO  | PO Item           |
| LFA1  | Vendor / Supplier |
| EKBE  | PO History        |




### 1.6 CDS View 模式（S/4HANA 推荐）

CDS View 是 S/4HANA 的语义层，已对底层透明表做业务封装：


| CDS View             | Ontology 对象        | 映射机制           |
| -------------------- | ------------------ | -------------- |
| **I_SalesOrder**     | Sales Order        | 自动重命名 + 属性映射   |
| **I_SalesOrderItem** | Sales Order Item   | 自动 Join 相关 CDS |
| **I_Product**        | Product / Material | 属性映射           |
| **I_Customer**       | Customer           | 属性映射           |
| **I_Supplier**       | Vendor             | 属性映射           |


> **CDS View 优势**：HyperAuto 读取 CDS 元数据后，跳过"透明表 → 业务实体"的转换环节，直接生成业务对象。



### 1.7 自动生成的 Link Type

HyperAuto 的真正价值在于自动构建的关系网：

```
Sales Order Item → Customer          (通过 KUNNR 外键)
Sales Order Item → Product           (通过 MATNR 外键)
Sales Order → Sales Order Item       (一对多父子)
Sales Order Item → Delivery          (履约链路)
Delivery → Invoice                   (开票链路)
```

这些 Link 是后续 AIP Logic 能让 LLM "顺着关系追溯"的基础。

---



## Stage 2 · 数据同步（Sync）



### 2.1 增量同步策略

TitanIndustries 场景下有两条增量路径，选型决策树：

```
需要捕获每一笔变更（含 UPDATE 前后值、DELETE）？
  ├─ Yes → SLT 模式（触发器级 CDC，近实时）
  └─ No → 只需要"新行/新值"？
        ├─ Yes → CDS View + APPEND + Multiple fields
        └─ No → 全量快照（SNAPSHOT）
```



### 2.2 方案一：CDS View APPEND 增量（推荐默认）


| 数据集              | SAP 对象                   | 事务类型     | 增量模式            | 增量字段                | 调度       |
| ---------------- | ------------------------ | -------- | --------------- | ------------------- | -------- |
| Sales Order      | I_SalesOrder (CDS)       | APPEND   | Multiple fields | LastChangedDateTime | 每 5 分钟   |
| Sales Order Item | I_SalesOrderItem (CDS)   | APPEND   | Multiple fields | LastChangedDateTime | 每 5 分钟   |
| Customer         | I_Customer (CDS)         | SNAPSHOT | —               | —                   | 每日 02:00 |
| Product          | I_Product (CDS)          | SNAPSHOT | —               | —                   | 每日 03:00 |
| Delivery         | I_DeliveryDocument (CDS) | APPEND   | Multiple fields | LastChangedDateTime | 每 15 分钟  |


**Multiple fields 语义**：记录已抽取的最大字段值，下次只拉取 ≥ 该值的行（多字段用逗号分隔，逻辑为 OR）。

### 2.3 方案二：SLT 触发器级 CDC（高实时性场景）

适用场景：需要捕获每一笔 INSERT/UPDATE/DELETE，包括中间变更状态。

```
SAP S/4HANA 数据库
  ↓ 数据库触发器（DB Trigger）
SLT 捕获队列
  ↓ ODP (Operational Data Provisioning)
SLT Server Queue
  ↓ Foundry 定时轮询
Foundry Dataset
```


| 项               | 配置                                                                  |
| --------------- | ------------------------------------------------------------------- |
| 前置条件            | Connector 2.34 (SP34)+, SAP_BASIS 7.50 SP09+, DMIS 2011_1_730 SP15+ |
| SAP Object Type | **SLT**（而非 CDS View）                                                |
| Context         | SLT queue alias                                                     |
| 首次运行            | 全量加载                                                                |
| 后续              | 只拉增量                                                                |


**SLT 适用对象**：


| 数据集                 | 模式         | 理由             |
| ------------------- | ---------- | -------------- |
| I_MaterialStock（库存） | SLT        | 高频变动，需近实时      |
| KNKK（信用主数据）         | SLT        | 变更影响决策，需触发器级捕获 |
| I_SalesOrder（订单头）   | CDS APPEND | 量适中，5 分钟延迟可接受  |




### 2.4 HyperAuto 与增量的关系

HyperAuto 的自动管道生成基于**首次全量同步**的元数据推导。后续增量同步时：

- HyperAuto 生成的管道结构保持不变
- 新增量数据流入同一数据集
- Pipeline Builder 转换逻辑自动应用
- Ontology 对象实时反映最新状态

---



## Stage 3 · 管道清洗（Pipeline Builder）



### 3.1 流程挖掘双表构造

TitanIndustries 的 Pipeline Builder 产出两张标准表——这是流程挖掘算法的输入。

#### Process Object Dataset

描述"在流程中移动的那个东西"。


| 列名                               | 类型      | 说明         | Titan 场景实例                        |
| -------------------------------- | ------- | ---------- | --------------------------------- |
| `object_id`                      | STRING  | 对象主键       | Sales Order Item ID (VBAP 主键)     |
| `order_value`                    | DECIMAL | 订单金额       | NETWR                             |
| `customer_id`                    | STRING  | 客户编号       | KUNNR                             |
| `material_id`                    | STRING  | 物料编号       | MATNR                             |
| `credit_status`                  | ENUM    | 信用状态       | `ACTIVE` / `RELEASED` / `BLOCKED` |
| `customer_credit_limit`          | DECIMAL | 信用额度       | KNKK.KLIMK                        |
| `12_month_historic_order_volume` | DECIMAL | 12 个月历史订单量 | BSID/BSAD 聚合                      |
| `12_month_paid_on_time_rate`     | FLOAT   | 12 个月按时付款率 | 0.0–1.0                           |




#### Log Object Dataset

描述流程对象经过的每个步骤。只需 3 列：


| 列名               | 类型       | 说明                              |
| ---------------- | -------- | ------------------------------- |
| `object_id`      | STRING   | 关联 Process Object 主键            |
| `current_status` | ENUM     | 当前状态（如 "已创建"/"已冻结"/"已发货"/"已开票"） |
| `timestamp`      | DATETIME | 进入该状态的时间戳                       |


> **流程挖掘算法只需"对象+状态+时间"三元组**。把复杂 SAP 订单表降维到这个最小结构，是 Machinery 流程可视化的前提。



### 3.2 管道清洗算子链

```
HyperAuto 宽表（已自动 Join + 自动重命名）
  │
  ├── Filter    → 过滤已删除订单 / 测试订单
  ├── Cast      → NETPR: VARCHAR → DECIMAL(12,2)
  │              EDATU: VARCHAR → DATETIME
  │              KLIMK: VARCHAR → DECIMAL
  ├── Aggregate → 按 KUNNR 聚合 BSID/BSAD 计算按时付款率
  │              SUM(CASE WHEN pay_date <= due_date THEN 1 ELSE 0 END) / COUNT(*)
  ├── Join      → VBAP ⋈ KNKK（补信用额度）
  ├── Join      → VBAP ⋈ 聚合付款率（补历史指标）
  ├── Explode   → 多行交货计划展开
  ├── Sort      → 按 timestamp 排序（Log Object）
  └── Distinct  → 按主键去重（增量合并）
  │
  ▼
Process Object Dataset + Log Object Dataset
```



### 3.3 自动 vs 手动管道分工


| 管道环节        | 负责方                         | 说明              |
| ----------- | --------------------------- | --------------- |
| 原始同步        | HyperAuto Data Syncs        | 自动推导 sync 方式    |
| 列重命名        | HyperAuto Builder Pipelines | 自动翻译技术列名        |
| 自动 Join     | HyperAuto Builder Pipelines | 理解 SAP 模型自动关联   |
| **流程双表构造**  | **Pipeline Builder（手动）**    | 拖拽算子构造标准 schema |
| **付款率聚合**   | **Pipeline Builder（手动）**    | 需业务逻辑           |
| **状态枚举标准化** | **Pipeline Builder（手动）**    | SAP 状态码 → 可读枚举  |


---



## Stage 4 · OKF 映射（Funnel）



### 4.1 Ontology 对象建模

TitanIndustries 的 Ontology 是 Palantir 官方最完整的公开建模范例。

#### 核心 Object Type


| OT 名称                | 主键          | 来源                      | 核心属性                                                        | 说明                       |
| -------------------- | ----------- | ----------------------- | ----------------------------------------------------------- | ------------------------ |
| **Sales Order**      | VBELN       | VBAK / I_SalesOrder     | order_type, created_date, status, sales_org, sold_to_party  | 销售订单头                    |
| **Sales Order Item** | VBELN+POSNR | VBAP / I_SalesOrderItem | line_no, material_id, net_value, credit_status, order_value | **流程挖掘的 Process Object** |
| **Customer**         | KUNNR       | KNA1 / I_Customer       | name, classification, credit_limit, risk_class              | 客户主数据                    |
| **Product**          | MATNR       | MARA / I_Product        | type, uom, description, weight                              | 物料主数据                    |
| **Credit Block**     | case_id     | 派生                      | block_type, block_reason, blocked_amount, activated_at      | **AI 决策的核心对象**           |
| **Delivery**         | VBELN       | LIKP/LIPS               | ship_date, items, status                                    | 交货单                      |
| **Invoice**          | VBELN       | VBRK/VBRP               | amount, billing_date, paid_status                           | 发票                       |




#### 自动生成的 Link Type


| Link 名称            | From → To                       | 基数  | 自动依据       |
| ------------------ | ------------------------------- | --- | ---------- |
| `placed_by`        | Sales Order Item → Customer     | N:1 | KUNNR 外键   |
| `of_product`       | Sales Order Item → Product      | N:1 | MATNR 外键   |
| `parent_order`     | Sales Order Item → Sales Order  | N:1 | VBELN 父子关系 |
| `has_credit_block` | Sales Order Item → Credit Block | 1:1 | 信用冻结状态     |
| `fulfilled_by`     | Sales Order → Delivery          | 1:N | 单据流        |
| `billed_by`        | Delivery → Invoice              | 1:N | 单据流        |


> **关键认知**：Ontology 建得越完整，AIP Logic 里的 LLM 能拿到的上下文就越丰富。Palantir 官方原话："这个决策模型越忠实于企业日常运营的真实情况，AI 工具就越能有效运作"。



#### 新增派生属性（Pipeline 计算后回填）


| 属性                               | 类型      | 计算逻辑                            | 重要性 |
| -------------------------------- | ------- | ------------------------------- | --- |
| `customer_credit_limit`          | DECIMAL | KNKK.KLIMK 直接映射                 | ⭐⭐⭐ |
| `12_month_historic_order_volume` | DECIMAL | SUM(VBAP.NETWR) WHERE 创建日近 12 月 | ⭐⭐⭐ |
| `12_month_paid_on_time_rate`     | FLOAT   | COUNT(按时付款) / COUNT(总付款) 近 12 月 | ⭐⭐⭐ |
| `order_value`                    | DECIMAL | VBAP.NETWR                      | ⭐⭐⭐ |




### 4.2 Funnel 状态机（O2C 流程）

```
Order Created ──→ Credit Check ──→ Credit Released ──→ Delivery Created ──→ Goods Issued ──→ Invoice Created ──→ Payment Received
                      │                                                                                    │
                      ↓ BLOCKED                                                                             ↓ Overdue
               Credit Block Activated ──→ AI Evaluation ──→ Human Review ──→ Release / Maintain      Dunning
```



#### 状态枚举映射


| SAP 状态码 | 可读枚举                 | 说明   |
| ------- | -------------------- | ---- |
| `A`     | `BLOCKED`            | 信用冻结 |
| `B`     | `PARTIALLY_RELEASED` | 部分释放 |
| `C`     | `RELEASED`           | 已释放  |
| `` (空)  | `NOT_CHECKED`        | 未检查  |




### 4.3 流程挖掘指标

Machinery 从 Log Object Dataset 自动计算：


| 指标       | Titan 官方数据 | 说明        |
| -------- | ---------- | --------- |
| 总销售订单行数  | 3,709      | 流程对象总量    |
| 顺利通过率    | 99%        | 无信用冻结     |
| 活跃冻结数    | 57         | 当前被冻结的订单行 |
| 冻结金额     | $25M       | 被锁资金      |
| 平均冻结处理周期 | 9 天（改进前）   | 人工处理耗时    |


---



## Stage 5 · AI 决策（AIP Logic + OAG）



### 5.1 OAG vs 传统 RAG

TitanIndustries 的 AIP Logic 使用 **OAG（Ontology-Augmented Generation）**，不走传统 RAG：


| 维度       | 传统 RAG      | Palantir OAG                                    |
| -------- | ----------- | ----------------------------------------------- |
| 数据来源     | 向量库（文档嵌入）   | **Ontology 对象**（结构化业务数据）                        |
| LLM 调用方式 | 检索文档 → 生成回答 | **通过 Tools 查询 Ontology → 推理 → Apply action 写回** |
| 准确性      | 依赖向量检索质量    | **"高质量本体(Data) + 确定性工具(Logic) + 全链路溯源(Audit)"** |
| 执行能力     | 只读建议        | **可闭环写回 ERP**                                   |


> **反幻觉关键**：LLM 不直接"回忆"，而是"去查"——通过 Query objects tool 查询 Ontology 拿到真实数据。



### 5.2 AIP Logic 信用冻结函数设计



#### 输入

```yaml
Input: Credit Block 对象
  - sales_order_item: Sales Order Item
```



#### Use LLM Block 配置

**Prompt（三段式黄金结构）**：

```
[第一段：角色与任务概述]
You are a credit risk analyst agent for Titan Industries.
Your task is to decide whether the credit block on the given
Sales Order Item should be MAINTAINED or RELEASED.
Success looks like: accurate decision that matches experienced analyst judgment.

[第二段：可用数据与上下文]
You have access to the Sales Order Item's properties:
- credit_status
- order_value
- customer_credit_limit
- 12_month_historic_order_volume
- 12_month_paid_on_time_rate

[第三段：决策 Rubric + 工具使用时机]
Decision rubric:
- If order_value significantly exceeds customer_credit_limit AND
  12_month_paid_on_time_rate < 0.7 → MAINTAIN the block
- If order_value is within credit_limit AND
  12_month_paid_on_time_rate >= 0.9 → RELEASE the block
- Otherwise → MAINTAIN but flag for human review

When you need customer's full payment history, use the Query objects tool.
When you need precise calculations, use the Calculator tool.
You MUST show your chain-of-thought reasoning before giving the final answer.

Your final output MUST be in the following JSON structure:
{
  "decision": "maintain_block | release_block",
  "confidence": 0.0-1.0,
  "reasoning": "step-by-step explanation referencing specific object properties",
  "proposed_action": "description of the action to execute"
}
```

**Tools 配置**：


| Tool 类型           | 用途                                      | 配置                      |
| ----------------- | --------------------------------------- | ----------------------- |
| **Query objects** | 查询客户付款历史、关联订单                           | 指定属性，不开放整个对象            |
| **Calculator**    | 精确数学（信用利用率、金额对比）                        | 添加即可用                   |
| **Call function** | 调用预测函数（如 "Forecasting Customer Orders"） | 需有 JSDoc 注释             |
| **Apply action**  | 记录决策到 Ontology                          | 不自动执行，Human-in-the-loop |




#### 输出

```json
{
  "decision": "release_block",
  "confidence": 0.87,
  "reasoning": "Order value $12,500 is within credit limit $50,000.
    Customer's 12-month paid on time rate is 0.94 (above 0.9 threshold).
    Historic order volume shows stable growth. Recommend release.",
  "proposed_action": "Release credit block for SO item VBAP-00123"
}
```



### 5.3 反幻觉的双层防护

**第一层：数据工具（确定性逻辑）**

LLM 不直接回答"哪个配送中心最近"，而是调用 Ontology 里的 Function（如 Haversine 公式计算距离），把计算委托给确定性逻辑。

**第二层：人工审查队列（Human-AI Teaming）**

AIP Logic 不直接把"解除冻结"的 Action 写回 SAP，而是把建议放进审查队列等专家审批：

```
AIP Logic 输出建议
  → 存入 Ontology 的 Credit Block.ai_recommendation 属性
  → Workshop 显示建议 + 推理过程 + "批准"/"拒绝" 按钮
  → 人工点击批准 → Apply action 写回 SAP
```



### 5.4 AIP Logic 多轮编排范式



#### 范式 A：串行多 LLM Block

```
Input: Sales Order Item
  ↓
[Block 1: Use LLM - "信用评估"]
  Prompt: 评估信用风险，输出 maintain/release 建议
  Tools: Query objects (读客户历史)
  Output: credit_decision
  ↓
[Block 2: Create variable]
  打包 credit_decision + 原始订单属性
  ↓
[Block 3: Use LLM - "生成客户沟通文本"]
  Prompt: 基于信用决策，生成给客户的邮件草稿
  Input: 引用 Block 2 的变量
  Output: email_draft
  ↓
[Block 4: Apply action - 确定性写回]
  更新 credit_status + 创建 Email 对象
```



#### 范式 B：分类器 + 分支 LLM（k-LLM 模型路由）

```
[Block 1: Use LLM (Llama 8B 本地) - "复杂度分类器"]
  Output: route_type ("A" | "B" | "C")
  ↓
[Conditionals]
  If "A" 常规 → Block 2A: Apply action (直接释放，无需 LLM)
  If "B" 高风险 → Block 2B: Use LLM (Claude Haiku) - 深度评估
                   Block 3B: Apply action
  If "C" 异常 → Block 2C: Use LLM (GPT-4) - 生成审查工单
                Block 3C: Apply action
```

> **成本优化**：分类器用小模型（<100ms），70-80% 简单请求导流到小模型，整体成本下降 60-80%。



#### 范式 C：k-LLM Consensus（多模型共识）

```
关键决策（如信用释放）分发到 K 个 LLM：
  Block 1: GPT-4 视角 → gpt4_decision
  Block 2: Claude Opus 视角 → claude_decision
  Block 3: Llama 70B 视角 → llama_decision
  Block 4: Synthesizer 共识器 → 比较三者推理质量 → final_decision
  Block 5: Apply action
```

> 适用于关键决策场景，用交叉验证降低单一模型的幻觉风险。代价是成本线性乘以 K。



### 5.5 Compute 成本管理


| 操作                | Compute 消耗        |
| ----------------- | ----------------- |
| 每个 LLM Block 执行   | 4 compute-seconds |
| 每个 LLM Block 调用工具 | 8 compute-seconds |
| 多轮编排              | 线性累加              |


> **工程要点**：避免无意义的多轮循环；分类器用小模型；关键决策才用 Consensus。

---



## Stage 6 · 应用层与自动化



### 6.1 Workshop 应用

TitanIndustries 的 Workshop 应用集成四类组件：


| 组件             | 数据源                                 | 交互                      |
| -------------- | ----------------------------------- | ----------------------- |
| **流程图 Widget** | Machinery 生成的 O2C 流程图               | 点击节点下钻到具体订单             |
| **信用冻结列表**     | Credit Block OT (status=ACTIVE)     | 表格筛选、排序                 |
| **AI 建议面板**    | Credit Block.ai_recommendation      | 展示 decision + reasoning |
| **执行按钮**       | Action Type "Apply Credit Decision" | 点击 → 人工确认 → BAPI 写回 SAP |




#### Workshop 应用核心特征

- **Ontology-aware**：直接绑定 Ontology 对象，属性变界面实时变
- **Action 驱动**：按钮映射到 Action Type，点击即写回
- **AIP 集成**：AIP Logic 函数作为组件嵌入



#### 关键展示指标

```
总销售订单行: 3,709
活跃冻结: 57
冻结金额: $25M
AIP 建议: [Release: 23] [Maintain: 28] [Human Review: 6]
```



### 6.2 Automate 编排

将信用冻结处理编排为自动化：

#### Step 1: Condition 配置

```
Condition Type: Objects modified in set
Object Set: Sales Order Items where credit_status == "BLOCKED"
Expose effect input: Modified objects (单个对象)
Check frequency: Real-time 或 Every 5 minutes
```

> **生产优化**：高频更新对象（每天 100+ 更新）必须组合时间条件封顶评估频率。加上 5 分钟时间条件后，评估次数从每天 100,000 次降至 288 次（减少 340 倍）。



#### Step 2: Effect 配置

```
Effect Type: Action
Selected Action: "Evaluate Credit Block Decision"
  (预先定义的 Action，背后调用 AIP Logic 函数)
Parameter mapping:
  sales_order_item: 绑定到 condition 暴露的 Modified object
  decision: 由 AIP Logic 函数输出
  reasoning: 由 AIP Logic 函数输出
Execution mode: Per-object (每个冻结独立 AI 评估)
```



#### Step 3: Human-in-the-loop 通知

```
Effect Type: Notification
Recipients: 信贷分析师团队
Message: "New credit block evaluated for SO {{order_id}}.
          AI suggests: {{decision}}. Reasoning: {{reasoning}}.
          Click to approve/reject."
```



#### Step 4: 写回 SAP

```
Effect Type: Action
Selected Action: "Apply Credit Release" 或 "Maintain Credit Block"
Trigger: 人工在 Workshop 点击批准按钮时
→ BAPI 写回 SAP → Ontology 同步刷新
```



### 6.3 Action + Webhook 写回 SAP



#### Writeback 模式（强一致）

```
Action: "Apply Credit Decision"
  Logic tab:
    Rule 1: Webhook (Writeback) → "SAP Credit Block Update"
      Input mapping: Use Function → buildSAPWebhookInput(order, decision)
      函数逻辑:
        if decision == "MAINTAIN": return undefined (不写回)
        if order.creditBlockType != "AUTO": return undefined (手动冻结不自动处理)
        return { salesOrderId: order.id, action: "RELEASE", timestamp: now() }
      → decision=="RELEASE" 且自动冻结 → 触发 BAPI
      → 否则跳过 Webhook，仍执行 Rule 2

    Rule 2: Ontology Edit
      更新 Sales Order.credit_status = decision
      更新 Sales Order.last_decision_time = now()

    Rule 3: Webhook (Side effect) → "Risk Team Notification"
      Input mapping: Use Function → buildRiskTeamNotification(order, decision)
      函数逻辑:
        if order.riskLevel != "CRITICAL": return undefined
        return { orderId: order.id, message: "Credit decision: ${decision}" }
      → 高危订单发通知；否则跳过
```



#### Writeback vs Side effect 选型


| 场景         | 模式              | 理由                   |
| ---------- | --------------- | -------------------- |
| 信用释放写回 SAP | **Writeback**   | 保证"外部失败→本体不变"        |
| 风险团队通知     | **Side effect** | Best-effort，失败不影响主流程 |
| 邮件通知客户     | **Side effect** | 可配多个，并行无序            |




### 6.4 条件触发机制

**核心**：Function 返回 `undefined` 即不触发 Webhook。

```typescript
@Function()
public buildWebhookInput(
    order: SalesOrder,
    decision: string
): WebhookInput | undefined {
    // 条件1: 只有 RELEASE 才写回 SAP
    if (decision !== "RELEASE") return undefined;
    // 条件2: 只有自动冻结才自动处理
    if (order.creditBlockType !== "AUTO") return undefined;
    // 通过条件 → 触发
    return {
        salesOrderId: order.id,
        action: "RELEASE",
        timestamp: new Date().toISOString()
    };
}
```



### 6.5 链式 Webhook + 部分失败处理

复杂订单履约需调用多个外部系统（ERP/WMS/TMS），用 External Function 编排：

```typescript
@OntologyEditFunction()
public async fulfillOrder(order: SalesOrder): Promise<void> {
    // Step 1: 调用 ERP 释放信用冻结（Writeback 语义）
    const erpResult = await ERP_Source.webhooks.ReleaseCreditBlock.call({
        salesOrderId: order.id, action: "RELEASE"
    });
    if (isErr(erpResult)) {
        // ERP 失败 → 创建错误对象，终止
        this.createErrorObject({ orderId: order.id, failedSystem: "ERP", ... });
        return;
    }
    // Step 2: 并发调用 WMS + TMS
    const [wmsResult, tmsResult] = await Promise.all([
        WMS_Source.webhooks.CreateOutboundDelivery.call({ ... }),
        TMS_Source.webhooks.CreateShipment.call({ ... })
    ]);
    // Step 3: 部分失败处理
    const failures = [];
    if (isErr(wmsResult)) failures.push({ system: "WMS", ... });
    if (isErr(tmsResult)) failures.push({ system: "TMS", ... });
    if (failures.length > 0) {
        this.createErrorObject({ ... });
        // Saga 补偿: WMS 成功但 TMS 失败 → 取消 WMS 出库单
        if (isOk(wmsResult) && isErr(tmsResult)) {
            await WMS_Source.webhooks.CancelOutboundDelivery.call({ ... });
        }
    } else {
        order.status = "FULFILLED";
    }
}
```



#### 补偿模式


| 模式              | 机制                                                                              |
| --------------- | ------------------------------------------------------------------------------- |
| **错误对象 + 定时重试** | 失败 → 创建 WebhookError OT → Automate 每 5 分钟扫描 retryable=true 且 retryCount<3 的对象重试 |
| **Saga 补偿**     | Step 3 失败 → 撤销 Step 2（取消 WMS 出库）→ 撤销 Step 1（ERP 重新冻结）                           |


---



## 7. 闭环：决策回写与安全治理



### 7.1 完整闭环

```
[业务用户在 Workshop 点击 "解除信用冻结"]
  ↓
Action Service 应用编辑
  ↓
Funnel 校验治理策略、MAC/DAC 安全、schema 约束
  ↓
写回 SAP（通过 HyperAuto 反向通道 / BAPI）
  ↓
Ontology 中 Credit Block 对象状态更新
  ↓
"AI 建议 + 人类确认"经验作为结构化数据沉淀回 Ontology
  ↓
优化后续 AI 推荐质量
```



### 7.2 安全治理

安全在 Ontology 层统一定义：


| 权限模型            | 说明                                    |
| --------------- | ------------------------------------- |
| **MAC**（强制访问控制） | 对象级别的安全标签                             |
| **DAC**（自主访问控制） | 行列级权限                                 |
| **分层权限**        | "生产团队能看全球机器遥测、仓储人员按区域受限、供应链分析师有行列级权限" |
| **AI 继承**       | 所有 AI 智能体的权限要么继承自人类用户，要么继承自项目权限结构     |


---



## 8. 生产部署铁律

来自 Palantir 官方最佳实践：


| #   | 铁律                                 | 说明                                                        |
| --- | ---------------------------------- | --------------------------------------------------------- |
| 1   | **高频对象必加时间条件封顶**                   | 1000 对象 × 100 更新/天 = 100K 评估；加 5 分钟条件降至 288 次/天（减少 340 倍） |
| 2   | **默认 Single execution**            | 100 个触发告警 → 1 次批量处理；Per-object 仅用于需隔离失败的场景                |
| 3   | **Human-in-the-loop 不可省**          | AIP Logic 的 Apply action 在无人值守场景必须配合审批队列                  |
| 4   | **关键写回用 Writeback**                | 保证"外部失败→本体不变"；通知类用 Side effect                            |
| 5   | **Function 返回 undefined 做条件触发**    | 不满足条件时不触发 Webhook，其他 Rule 仍执行                             |
| 6   | **链式 Webhook 用 External Function** | 单个 Webhook 不支持动态数量请求                                      |
| 7   | **部分失败创建错误对象**                     | HTTP 错误码无法配置为"成功"，必须创建 WebhookError OT 供 Automate 重试      |
| 8   | **分类器用小模型**                        | Llama 8B 本地做复杂度分类（<100ms），70-80% 请求导流到小模型                 |


---



## 9. 与电商平台接入方案的对照矩阵


| Stage      | 电商平台（淘宝/京东/Shopify…）  | TitanIndustries（SAP O2C）                  |
| ---------- | --------------------- | ----------------------------------------- |
| **S1 接入**  | 手写 Connector + API 签名 | **HyperAuto SDDI 自动管道**                   |
| **S2 同步**  | API 增量游标 / Webhook    | **CDS APPEND / SLT CDC**                  |
| **S3 管道**  | 手动 Join 订单关系网         | **自动 Join + 手动构造流程双表**                    |
| **S4 OKF** | OT 映射 + Funnel 状态机    | **同 + 流程挖掘 Process/Log Object**           |
| **S5 本体**  | OT + Link + Action    | **同 + Credit Block 决策对象**                 |
| **S6 消费**  | COP 态势 + Workshop 列表  | **同 + Machinery 流程图 + AI 决策面板 + BAPI 写回** |
| **AI 决策**  | 态势预警                  | **AIP Logic OAG 信用冻结评估**                  |
| **写回**     | 平台 API 调用             | **BAPI 写回 SAP**                           |
| **自动化**    | 调度任务                  | **Automate 条件触发 + Human-in-the-loop**     |


---



## 10. 平台缺口（TitanIndustries 暴露的 AOS 能力需求）


| 缺口 ID         | 描述                                                                   | 优先级 | 对应电商平台缺口            |
| ------------- | -------------------------------------------------------------------- | --- | ------------------- |
| **G-HA-01**   | HyperAuto SDDI 自动管道（元数据驱动）                                           | P1  | 所有平台的 Stage 1-3 自动化 |
| **G-PM-01**   | Machinery 流程挖掘（Process/Log Object → 可视化流程图）                          | P1  | 订单生命周期分析            |
| **G-AIP-01**  | AIP Logic 无代码 LLM 函数编辑器（Block 编排）                                    | P0  | 所有 AI 决策场景          |
| **G-AIP-02**  | OAG Tools（Query objects / Calculator / Call function / Apply action） | P0  | AI 反幻觉机制            |
| **G-AIP-03**  | k-LLM 模型路由（Conditionals + 多 Use LLM Block）                           | P1  | 成本优化                |
| **G-ACT-01**  | Action Webhook（Writeback / Side effect）                              | P0  | 写回外部系统              |
| **G-ACT-02**  | External Function 链式 Webhook + 部分失败处理                                | P1  | 多系统履约编排             |
| **G-AUTO-01** | Automate 条件触发（Objects modified / Threshold crossed）                  | P0  | 自动化编排               |
| **G-AUTO-02** | Automate 性能优化（时间条件封顶 + Single execution）                             | P1  | 生产部署                |
| **G-SEC-01**  | Ontology 层 MAC/DAC 安全治理                                              | P1  | 数据权限                |


---



## 附录 · 全链路 ASCII 图

```
[SAP S/4HANA: VBAK/VBAP/KNA1/MARA/KNKK/BSID]
    ↓ [HyperAuto V2] 读取元数据 → 自动 sync + 自动管道 + 自动生成 Ontology
[Foundry Datasets: Sales Order, Sales Order Item, Customer, Credit Block]
    ↓ [Pipeline Builder] 低代码构造 Process Object + Log Object 双表
[流程挖掘数据集]
    ↓ [Ontology Manager] 创建对象 + 配置权限 + 链接到企业已有对象
[Ontology: Sales Order Item + Credit Block + Customer + Product + Links]
    ↓ [Machinery] 点击式生成可视化流程图
[流程洞察: 3709 订单行 / 57 冻结 / $25M]
    ↓ [AIP Logic] Use LLM Block
    ↓   Prompt(角色+任务+rubric) + Tools(Query/Calculator/Call function/Apply action)
    ↓   输出: { decision, confidence, reasoning, proposed_action }
    ↓ [Logic 函数发布]
[Action: "AI Credit Decision"]
    ↓ [Action Logic tab]
    ↓   Rule 1: Webhook (Writeback) → SAP BAPI 信用释放
    ↓            Input mapping: Function buildSAPWebhookInput()
    ↓            → decision=="RELEASE" 且自动冻结 → 触发 BAPI
    ↓   Rule 2: Ontology Edit → 更新 credit_status
    ↓   Rule 3: Webhook (Side effect) → 风险团队通知（仅高危）
    ↓ [Automate 编排]
    ↓   Condition: Sales Order Item modified + credit_status = BLOCKED
    ↓   Effect: Submit Action "AI Credit Decision"
    ↓   + 5 分钟时间条件封顶（减少 340 倍评估）
    ↓ [Workshop]
    ↓   Machinery 流程图 Widget + 冻结列表 + AI 建议面板 + 执行按钮
    ↓ [Human-in-the-loop]
    业务用户点击 "批准" → Apply action → BAPI 写回 SAP
    ↓ Ontology 同步刷新 → 经验沉淀 → 优化后续推荐
[SAP S/4HANA 信用状态更新 + Foundry Ontology 闭环]
```

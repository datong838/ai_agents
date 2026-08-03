# 差评管理运营场景 · 全链路执行过程

> 以**差评管理运营场景**为例：一位会员留下 1 星差评（"用了过敏/刺痛"）。这条差评从被系统发现，到最终处理完成、写回业务系统的**一次完整执行链路**——涉及 **6 个智能体协作**（数据参谋、售后客服、内容官、导购顾问、活动策划师、客户管家）、跨 4 组电商本体查询/写入、3 个 Action 写回、1 次人工审批。

---

## 一、总链路流程图

### 三列布局说明

| 左侧：AOS 平台支撑能力 | 中间：一次执行的 9 步主链路（6 个智能体协作） | 右侧：电商本体 |
|---|---|---|

### 左侧：AOS 平台支撑能力（3 个能力块）

#### 🤖 在线制作智能体（造人）
- 本链路涉及 **6 个智能体**：数据参谋·售后客服·内容官·导购顾问·活动策划师·客户管家，均通过此能力在线创建
- →② 数据参谋智能体
- →③ 售后客服智能体（主协调）
- →④⑤⑥ 其他 4 个智能体协作
- →⑥ 注入 Prompt+模型+上下文
- →⑦ 安全等级触发 Draft

#### 🧠 AIP 逻辑画布（健脑）
- →② 编排「监控→阈值→告警」
- →④ 声明 Block 链走哪个 Action
- →⑤ 编排 Function 顺序分支
- →⑥ 声明 Use LLM 节点
- →⑧ Action 执行+失败回滚

#### 🔧 智能体工具面板（配枪）
- →② 配置数据查询 Function
- →④ 定义 Action Schema
- →⑤ 定义 Function 实现
- →⑥ 敏感词质量门控
- →⑦ 工具级安全策略
- →⑧ 3 个 Action 实现

### 中间：9 步主链路

#### 智能体图例
| 智能体 | 颜色 | 角色 |
|---|---|---|
| 🤖 数据参谋 | 蓝 | 监控巡检 |
| 🤖 售后客服 | 绿 | 主协调 |
| 🤖 内容官 | 紫 | 详情页 |
| 🤖 导购顾问 | 青 | 替代推荐 |
| 🤖 活动策划师 | 黄 | 赠品补偿 |
| 🤖 客户管家 | 蓝绿 | 后续跟进 |

#### 9 步主链路详细

**🏢 业务工作台**（入口）
- 接收业务事件 · 发起 AIP 执行

**① 差评产生**
- 10:00 会员留 1 星差评：「产品用了过敏/刺痛」

**② 数据参谋检测异常**
- 10:01 差评率 2%→3.5%，触发告警广播
- 🤖 数据参谋：监控巡检
- 支撑能力：A（在线制作智能体）+ L（AIP逻辑画布）+ T（智能体工具面板）

**③ 意图理解 · 任务分派**
- 识别「差评危机」→ 提取关键信息 → 分派给 5 个同事
- 🤖 售后客服：主协调
- 🤖 活动策划师：赠品
- 🤖 导购顾问：替代推荐
- 🤖 内容官：详情页
- 支撑能力：A（在线制作智能体）

**④ Action 请求 · 拆解任务**
- 确定 3 个 Action 执行方案
- 🤖 售后客服：退款+道歉
- 🤖 活动策划师：赠送小样
- 🤖 导购顾问：推荐替代产品
- 支撑能力：L（AIP逻辑画布）+ T（智能体工具面板）

**⑤ Function 工具调用 · 数据查询**
- 并行查询所需数据
- 🤖 售后客服：查会员/订单
- 🤖 导购顾问：查成分/肤质
- 🤖 活动策划师：查活动规则
- 支撑能力：L（AIP逻辑画布）+ T（智能体工具面板）

**⑥ LLM 大模型建议 · 生成内容**
- 生成个性化内容，供人工审批
- 🤖 售后客服：生成安抚话术
- 🤖 内容官：品牌合规审核
- 🤖 导购顾问：替代产品推荐
- 支撑能力：A（在线制作智能体）+ L（AIP逻辑画布）+ T（智能体工具面板）

**⑦ 人工确认 · Draft 审批**
- 退款金额 >200 元 → 客服主管审批
- 🤖 售后客服：触发安全策略
- 支撑能力：A（在线制作智能体）+ T（智能体工具面板）

**⑧ 写回业务系统 · 执行 Action**
- 执行 3 个 Action，写回业务系统
- 🤖 售后客服：退款/旺旺道歉
- 🤖 内容官：修改详情页
- 🤖 活动策划师：登记小样
- 支撑能力：L（AIP逻辑画布）+ T（智能体工具面板）

**⑨ 结果返回工作台**
- 差评率恢复 · 客户改评 · 后续回访
- 🤖 客户管家：3天后回访
- 🤖 客户管家：14天后跟进

**🏢 业务工作台**（出口）
- 展示处理结果 · 等待人工确认

### 右侧：电商本体

| 步骤 | 本体对象 | 操作 |
|---|---|---|
| ① | order_review（差评记录）· 实时同步 | 写入 |
| ② | product（商品SKU）· order_review（差评率指标） | 读取 |
| ⑤ | member（会员档案）· order（订单详情）· product_ingredient（成分表）· member_skin_profile（肤质标签） | 读取 |
| ⑧ | refund（退款记录）· order_gift（赠品登记）· product_detail（商品详情页）· chat_message（旺旺消息） | 写入 |

---

## 二、6 个智能体工作分布

| 智能体 | 参与步骤 | 具体工作 |
|---|---|---|
| 🤖 数据参谋 | ② | 监控差评率 → 触发告警 |
| 🤖 售后客服 | ③④⑤⑥⑦⑧ | 主协调+退款+道歉+话术生成 |
| 🤖 内容官 | ③⑥⑧ | 品牌合规审核+修改详情页 |
| 🤖 导购顾问 | ③④⑤⑥ | 成分查询+肤质匹配+替代推荐 |
| 🤖 活动策划师 | ③④⑤⑧ | 制定补偿方案+登记赠品 |
| 🤖 客户管家 | ⑨ | 后续回访+客户维护 |

---

## 三、6 个智能体标准定义

### 3.1 数据参谋

| 配置项 | 值 |
|---|---|
| 角色定位 | 差评监控巡检智能体 |
| 核心职责 | 定时扫描差评率指标，超过阈值时触发告警广播 |
| 系统提示词 | 你是数据参谋智能体。你的职责是监控差评率指标，当差评率超过阈值时触发告警。优先读取 order_review 对象的统计数据，禁止臆造数据。 |
| 模型选择 | 私有-轻量（低延迟优先） |
| 安全等级 | L1 Draft 暂存 |
| 本体上下文 | order_review（差评记录）、product（商品SKU） |
| 触发方式 | 定时触发（每5分钟巡检）+ 事件触发（新差评入库） |
| 工具配置 | Object Query（查询差评率）、trigger_alert（触发告警） |
| 逻辑画布 | Input → Get Property（差评率）→ Transform（计算）→ Branch（阈值判断）→ Apply Action（告警） |

### 3.2 售后客服

| 配置项 | 值 |
|---|---|
| 角色定位 | 售后客诉处理主协调智能体 |
| 核心职责 | 接收告警、分析差评意图、分派任务给其他智能体、执行退款和道歉 |
| 系统提示词 | 你是售后客服智能体。你的职责是接收差评告警，分析客户意图，协调其他智能体处理。涉及退款操作必须走 Draft 审批。优先读取 Order 与 member 结构化字段，禁止臆造字段。 |
| 模型选择 | 私有-旗舰（128K 上下文） |
| 安全等级 | L2 HITL 人机协同 |
| 本体上下文 | order（订单详情）、member（会员档案）、order_review（差评记录） |
| 触发方式 | 事件触发（告警事件） |
| 工具配置 | Object Query（查询订单/会员）、Action: refund（退款）、Action: send_message（旺旺道歉）、Request Clarification（追问） |
| 逻辑画布 | Input → Get Property → Use LLM（意图分析）→ Branch（意图路由）→ Handoff → Apply Action（创建工单） |

### 3.3 内容官

| 配置项 | 值 |
|---|---|
| 角色定位 | 商品详情页与评价管理智能体 |
| 核心职责 | 品牌合规审核、详情页优化建议、评价关键词回复 |
| 系统提示词 | 你是内容官智能体。你的职责是基于差评关键词生成详情页优化建议，确保内容品牌合规。所有修改提案需走 Draft 审批。 |
| 模型选择 | 私有-旗舰（128K 上下文） |
| 安全等级 | L1 Draft 暂存 |
| 本体上下文 | product（商品SKU）、product_detail（商品详情页）、order_review（差评记录） |
| 触发方式 | 事件触发（工单分派） |
| 工具配置 | Object Query（查询商品详情）、Action: propose_content_edit（提交内容修改提案） |
| 逻辑画布 | Input → Get Property → Use LLM（生成建议）→ Transform（格式化）→ Apply Action（提交提案） |

### 3.4 导购顾问

| 配置项 | 值 |
|---|---|
| 角色定位 | 替代商品推荐智能体 |
| 核心职责 | 基于差评商品和客户偏好推荐替代产品、发放优惠券 |
| 系统提示词 | 你是导购顾问智能体。你的职责是基于客户肤质和差评商品，推荐合适的替代产品。优先读取 product_ingredient 和 member_skin_profile，禁止臆造推荐。 |
| 模型选择 | 私有-中（平衡速度与质量） |
| 安全等级 | L2 HITL 人机协同 |
| 本体上下文 | product（商品SKU）、product_ingredient（成分表）、member_skin_profile（肤质标签）、order（订单详情） |
| 触发方式 | 事件触发（工单分派） |
| 工具配置 | Object Query（查询成分/肤质）、Use Tool: product_recommend_engine（推荐引擎）、Action: apply_coupon_discount（优惠券） |
| 逻辑画布 | Input → Get Property → Use Tool（推荐引擎）→ Branch（置信度判断）→ Apply Action（推荐/优惠券） |

### 3.5 活动策划师

| 配置项 | 值 |
|---|---|
| 角色定位 | 赠品补偿与活动策划智能体 |
| 核心职责 | 制定补偿方案、发放赠品、登记赠品记录 |
| 系统提示词 | 你是活动策划师智能体。你的职责是基于客户等级和订单金额制定赠品补偿方案。所有赠品发放需走 Draft 审批。 |
| 模型选择 | 私有-中（平衡速度与质量） |
| 安全等级 | L1 Draft 暂存 |
| 本体上下文 | member（会员档案）、order（订单详情）、order_gift（赠品登记） |
| 触发方式 | 事件触发（工单分派） |
| 工具配置 | Object Query（查询活动规则/客户等级）、Action: grant_gift（发放赠品） |
| 逻辑画布 | Input → Get Property → Use LLM（生成方案）→ Create Variable（存储方案）→ Branch（分级策略）→ Apply Action（发放赠品） |

### 3.6 客户管家

| 配置项 | 值 |
|---|---|
| 角色定位 | 客户关系维护智能体 |
| 核心职责 | 后续回访、满意度调查、长期关系维护 |
| 系统提示词 | 你是客户管家智能体。你的职责是在差评处理完成后进行后续回访，记录客户反馈，维护长期关系。 |
| 模型选择 | 私有-轻量（低延迟优先） |
| 安全等级 | L0 只读问答 |
| 本体上下文 | member（会员档案）、order（订单详情）、order_review（差评记录） |
| 触发方式 | 事件触发（工单完成）+ 定时触发（3天后/14天后） |
| 工具配置 | Object Query（查询客户/订单状态）、Execute: send_wechat_message（发送微信消息） |
| 逻辑画布 | Input → Get Property → Use LLM（生成话术）→ Execute（发送消息）→ Handoff（记录日志） |

---

## 四、核心模块协作关系

### 造人 · 健脑 · 配枪 —— 三位一体的智能体生产流水线

AIP 决策引擎的三大核心模块不是孤立的功能点，而是一条完整的"智能体生产流水线"：

1. **在线制作智能体**（造人）：定义"谁"在干活。给智能体起名字、写系统 Prompt、选择底层模型、配置本体上下文、设定安全等级（L0-L4）。产出一份《智能体出生证明》——包含身份、性格、能力边界和权限红线。
2. **AIP 逻辑画布**（健脑）：定义"怎么干"。用 10 种 Block 把 LLM 调用、变量处理、条件判断、工具执行编排成可运行的 Pipeline。让智能体拿到任务后先做什么、再做什么、什么条件下走分支。
3. **智能体工具面板**（配枪）：定义"用什么干"。为智能体配备工具箱：对象查询（读数据）、动作（写数据）、函数（计算）、请求澄清（反问用户）。设定每个工具的安全策略——谁审批、什么条件下自动执行。让智能体从"只会聊天"变成"能查能写能调系统"。

### 协作关系：配置 → 编排 → 赋能 → 运行

```
Step 1: Agent Builder（造人）→ 输出：智能体定义（Identity + Context + Safety）
Step 2: AIP Logic（健脑）→ 输出：可执行 Block 链（Pipeline）
Step 3: AIP Tools（配枪）→ 输出：工具授权策略 + 执行代理
Result: 可运行智能体（上岗）
```

---

## 五、关键设计要点

1. **松耦合的事件驱动协作**：每个智能体的逻辑链都可以独立调试、独立版本管理，通过 Input/Handoff 实现智能体间的松耦合协作。
2. **安全等级分级管控**：从 L0 只读到 L4 无人值守，每个智能体根据职责选择不同安全等级，写操作必须走 Draft 审批或 HITL 确认。
3. **本体驱动的数据读写**：所有数据操作基于电商本体对象（order、product、member 等），不直接操作数据库表，确保数据一致性和权限控制。
4. **全链路可观测**：从差评产生到结果返回，每一步都有 A/L/T 标签标注支撑能力，便于追踪和审计。

---

## 六、AIP 逻辑画布全链路编排

> 将 6 个智能体的工作流程，用 AIP 逻辑画布的 10 种 Block（输入 / 创建变量 / 获取属性 / 使用 LLM / 使用工具 / 数据变换 / 应用动作 / 执行 / 分支 / 汇聚）编排出来。

### 6.1 数据参谋（监控巡检）

**职责**：监控差评率指标、异常告警触发

```
编排链：
① Input → ② Get Property → ③ Transform → ④ Branch → ⑤ Apply Action
```

| Block | 属性填写 | 说明 |
|-------|---------|------|
| **Input** | Object: `order_review`，触发器：定时（每15分钟） | 定时扫描差评记录 |
| **Get Property** | 读取：`rating`, `product_id`, `created_at` | 获取每条差评的关键字段 |
| **Transform** | DSL: `count(rating < 3) / count(*) as bad_rate` | 计算差评率 |
| **Branch** | 条件：`bad_rate > 3%` → 告警分支；`bad_rate ≤ 3%` → 静默分支 | 阈值判断 |
| **Apply Action** | Action: `trigger_alert`，参数：`level: 高` | 触发告警广播 |

### 6.2 售后客服（主协调）

**职责**：接收告警、协调分派、主协调角色

```
编排链：
① Input → ② Get Property → ③ Use LLM → ④ Branch → ⑤ Handoff → ⑥ Apply Action
```

| Block | 属性填写 | 说明 |
|-------|---------|------|
| **Input** | 触发器：告警事件（来自数据参谋），Object: `alert` | 接收上游告警 |
| **Get Property** | 读取：`order.status`, `customer.level`, `review.content` | 获取订单+客户+评价详情 |
| **Use LLM** | Prompt: `分析差评原因，提取关键词，判断客户等级`，模型: `私有-中` | 理解差评意图 |
| **Branch** | 3 路分支：`情绪愤怒` → 升级主管；`物流投诉` → 物流团队；`产品问题` → 内容官 | 意图路由 |
| **Handoff** | 汇聚到：`customer_service_handoff`，产物：`intent_analysis.json` | 交接给下游智能体 |
| **Apply Action** | Action: `create_ticket`，参数：`assign_to: 对应团队` | 创建工单分派 |

### 6.3 内容官（详情页优化）

**职责**：详情页、评价管理、关键词回复

```
编排链：
① Input → ② Get Property → ③ Use LLM → ④ Transform → ⑤ Apply Action
```

| Block | 属性填写 | 说明 |
|-------|---------|------|
| **Input** | 触发器：工单事件（来自售后客服），Object: `ticket` | 接收分派的工单 |
| **Get Property** | 读取：`product.description`, `review.keywords`, `product.images` | 获取商品详情 |
| **Use LLM** | Prompt: `基于差评关键词，生成详情页优化建议` | 生成内容建议 |
| **Transform** | 格式化为 Markdown：`# 详情页优化建议\n## 关键词：{keywords}\n## 建议：{llm_output}` | 格式化输出 |
| **Apply Action** | Action: `propose_content_edit`，目标：`product.description` | 提交内容修改提案 |

### 6.4 导购顾问（替代推荐）

**职责**：替代商品推荐、降价券发放

```
编排链：
① Input → ② Get Property → ③ Use Tool → ④ Branch → ⑤ Apply Action
```

| Block | 属性填写 | 说明 |
|-------|---------|------|
| **Input** | 触发器：工单事件，Object: `ticket` | 接收分派的工单 |
| **Get Property** | 读取：`order.product_id`, `customer.preferences`, `product_category` | 获取客户偏好+商品品类 |
| **Use Tool** | Tool: `product_recommend_engine`，参数：`category={品类}, exclude={差评商品}` | 调用推荐引擎 |
| **Branch** | 条件：`recommendation.confidence > 0.8` → 直接推荐；否则 → 生成优惠券补偿 | 置信度判断 |
| **Apply Action** | 分支1: `send_recommendation_email`；分支2: `apply_coupon_discount` | 两种动作 |

### 6.5 活动策划师（赠品补偿）

**职责**：赠品策划、补偿方案、优惠策略

```
编排链：
① Input → ② Get Property → ③ Use LLM → ④ Create Variable → ⑤ Branch → ⑥ Apply Action
```

| Block | 属性填写 | 说明 |
|-------|---------|------|
| **Input** | 触发器：工单事件，Object: `ticket` | 接收分派的工单 |
| **Get Property** | 读取：`customer.tier`, `order.amount`, `campaign.budget` | 获取客户等级+订单金额+活动预算 |
| **Use LLM** | Prompt: `基于客户等级和订单金额，生成赠品方案` | 生成补偿方案 |
| **Create Variable** | 变量：`compensation_plan`，值：`llm_output` | 存储方案 |
| **Branch** | 条件：`customer.tier == "VIP"` → 高价值赠品；`customer.tier == "Normal"` → 普通赠品 | 分级策略 |
| **Apply Action** | 分支1: `grant_gift: {gift_type: "优惠券", amount: 100}`；分支2: `grant_gift: {gift_type: "积分", points: 500}` | 发放赠品 |

### 6.6 客户管家（后续跟进）

**职责**：后续回访、满意度调查、长期关系维护

```
编排链：
① Input → ② Get Property → ③ Use LLM → ④ Execute → ⑤ Handoff
```

| Block | 属性填写 | 说明 |
|-------|---------|------|
| **Input** | 触发器：工单完成事件，Object: `ticket` | 接收已处理工单 |
| **Get Property** | 读取：`customer.last_contact`, `order.status`, `compensation_given` | 获取客户+订单+补偿记录 |
| **Use LLM** | Prompt: `生成个性化回访话术，包含补偿说明和感谢` | 生成话术 |
| **Execute** | 执行：`send_wechat_message`，参数：`content={llm_output}, customer_id={id}` | 发送微信消息 |
| **Handoff** | 汇聚到：`customer_relation_log`，记录：`回访时间`, `话术`, `客户回应` | 记录客户关系日志 |

### 6.7 整体协作 · 总编排链

将 6 个智能体串成一个总链路，协调流程：

```
主编排链：
① Input（差评事件）→ ② 数据参谋链 → ③ Handoff（汇聚结果）
→ ④ 售后客服链 → ⑤ Branch（按原因分流）
→ ⑥ 3 条并行链（内容官 / 导购顾问 / 活动策划师）
→ ⑦ Handoff（多路汇聚）→ ⑧ 客户管家链
```

其中涉及的关键 Block 用法：
- **Branch**：实现多路分流（按差评原因、客户等级分流）
- **Handoff**：实现多路汇聚（汇聚到统一出口、记录上下文交接）
- **Execute**：调用外部通知 / 消息服务
- **Use Tool**：调用推荐引擎、风控引擎等注册工具

### 6.8 设计要点

每个智能体的逻辑链都可以**独立调试、独立版本管理**，同时通过 Input / Handoff 实现**松耦合的事件驱动协作**。

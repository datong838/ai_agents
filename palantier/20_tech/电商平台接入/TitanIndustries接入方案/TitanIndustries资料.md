Palantir 自己在官方博客里用"Titan Industries"这家虚构公司做过订单到现金（Order-to-Cash）的端到端演示，从 SAP 连接 → Pipeline → Ontology → AIP Logic → Workshop 一路打通，这是目前公开资料里最接近你想要的"全链路详细过程"的范本。

下面我把"官方端到端范式 + 零售/电商行业真实案例的效果印证 + 架构机制"拼起来，给你一条可复用的全链路地图。

先说结论：公开资料的"完整度边界"
真正逐环节开源的端到端 Demo：Palantir 官方 Blog 的 "Building with Palantir AIP: AI-Powered Process Mining"（以 Titan Industries 订单到现金流程为例）和 "Data Tools for RAG / OAG"（以 Titan 医药用品仓库火灾应急为例）——这两个是目前最接近"从数据连接到 Workshop"全链路的公开材料 。
零售/电商真实客户：Wendy's（6500 家餐厅实时订单库存 ）、Heineken USA（25 个分销商预警、$4.9M 防缺货价值 ）、Lowe's（供应链数字孪生，POC 到生产不到 4 个月 ）——这些有"接入了哪些系统+业务效果"，但没披露具体的 Ontology 对象建模细节。
架构底层：Palantir 官方 Ontology 文档 + 若干技术解读，可以拼出 Foundry/AIP 的后端服务骨架 。
所以下面我用 Titan 的官方 Demo 作为"全链路骨架"，用 Wendy's/Heineken/Lowe's 作为"零售电商行业的真实佐证"，给你还原这条路。

🔗 第一环：数据连接（Data Connection）——HyperAuto / SDDI

对应工具：HyperAuto（Software-Defined Data Integration, SDDI）

Palantir 的思路不是让你手写 ETL，而是用元数据驱动的方式自动生成数据管道：
HyperAuto 直接连接企业常见的 ERP / CRM 系统，包括 SAP、Salesforce、Oracle NetSuite、Hubspot​ 等
它读取数据源的 metadata，自动推导​ sync 方式、transformation 逻辑、以及 Ontology 的初步设计方案
在 Titan 的订单到现金场景中，源系统就是 SAP，HyperAuto 开箱即用地部署了一条 pipeline，并且自动做了三件事 ：
自动生成 join（销售订单头/行/客户/信用数据之间的关联）
自动生成主键和外键
把数据库列名翻译成人类可读的格式（比如 EKPO~NETPR → "Net Price"）
💡 这一步的价值：传统 ETL 团队要花数周理解的 SAP 表结构，HyperAuto 在分钟内完成从 source 到 Ontology 的映射 。

🔧 第二环：数据清洗与建模（Pipeline Builder）

对应工具：Pipeline Builder（低代码/无代码数据管道工具）

光把数据同步过来还不够，要为"流程挖掘"准备特定 schema。Titan 的场景里需要造两类数据集 ：
数据集类型    |   作用     |   Titan 订单场景中的实例
Process Object Dataset​ | 描述"在流程中移动的那个东西" | Sales Order Item（销售订单行）
Log Object Dataset​  |  描述流程对象经过的每个步骤  |  只需要 3 列：对象主键、当前状态、时间戳

Pipeline Builder 把 HyperAuto 同步过来的 SAP 数据，低代码拖拽成上面两种 schema。这一步产出的就是干净的、可供 Ontology 消费的数据集。

🧬 第三环：Ontology 本体建模（核心中的核心）

这是 Palantir 区别于所有其他数据平台的关键一层。​

根据 Palantir 官方定义，Ontology 是"组织的运营层"，坐在数据集/虚拟表/模型之上，同时包含语义元素（对象、属性、链接）和动力元素（动作、函数、动态安全）​ 。

在 Titan 的场景中，订单到现金流程被建模为一组相互关联的对象：
Customer（客户）
Sales Order / Sales Order Item（销售订单/订单行）
Credit Block（信用冻结——这是本案例的核心决策点）
它们通过 Link Type​ 互相连接，形成一张反映真实业务的知识图谱
Ontology 后端不是单一数据库，而是一组微服务​ ：
OMS（Ontology Metadata Service）：schema 的唯一真相源，定义所有对象类型、链接类型、动作类型
OSS（Object Set Service）：高吞吐读取层，应用和 LLM 都通过它查询
Funnel（Object Data Funnel）：编排所有写入操作，在变更底层数据前校验治理策略和安全规则
Object Databases：存储索引后的对象数据，保证读取性能
📌 关键点：Ontology 不只是"语义层"，它是带动词的语义层——不仅能读，还能通过 Action Type 写回 ERP。这就是后面 AIP 能"执行决策"而不是"只给建议"的根本原因。

🤖 第四环：AIP Logic——把 LLM 接入 Ontology

对应工具：AIP Logic（无代码 LLM 函数开发环境）+ OAG（Ontology-Augmented Generation）

传统的 RAG 是"LLM + 向量库"，Palantir 玩的是 OAG（本体增强生成）——LLM 不只是检索文档，而是直接调用 Ontology 里的确定性逻辑工具和 Action​ 。

Titan 信用冻结场景里的 AIP Logic 函数设计（官方 Demo 里的真实做法）：
输入：一个 Credit Block 案例
LLM 通过 OSS 读取该客户的历史付款记录、订单上下文等 Ontology 对象
LLM 输出："维持冻结"或"解除冻结"的建议 + 详细推理过程
作者 Ruben 的比喻是——"像教一个聪明但没背景知识的实习生"
如果是 Heineken 那种供应链场景，AIP 智能体就能主动执行库存调配、港口提箱等操作，测试两天处置 25 个分销商紧急预警，挽回 $300K 潜在损失 。

OAG 相比 RAG 的本质差异：LLM 不仅能"引用来源"，还能通过 Action Type 闭环写回源系统——比如建议解除信用冻结后，直接触发 ERP 里的释放动作。

🖥️ 第五环：Workshop——搭建端到端应用

对应工具：Workshop（Foundry 内的无代码/低代码应用构建器）

Pipeline 跑通了、Ontology 建好了、AIP Logic 函数写好了，最后需要业务用户能用的界面。

在 Titan 的案例中 ：
用 Machinery（流程挖掘工具）把 Ontology 对象转成可视化流程图
Machinery 生成的流程模型本身就是一个可嵌入 Workshop 的 widget
在 Workshop 里拖拽组件，迅速搭出端到端流程挖掘应用
业务用户在同一个界面看到：所有信用冻结相关信息 + AI 给出的决策建议 + 一键执行按钮
Workshop 应用的核心特征 ：
Ontology-aware：直接绑定 Ontology 对象，对象属性变界面实时变
Action 驱动：界面上的按钮直接映射到 Action Type，点击即从 Ontology 写回 ERP
AIP 集成：AIP Logic 函数作为组件嵌入，实现"AI 建议 + 人工确认 + 一键执行"
🔄 闭环：决策回写与安全治理

整个链路的最后一环往往被忽略，但 Palantir 认为这是最关键的：

当业务用户在 Workshop 点击"解除信用冻结"按钮时：
Action Service 应用编辑
Funnel​ 校验治理策略、MAC/DAC 安全、schema 约束
写回 SAP（通过 HyperAuto 的反向通道）
Ontology 中的 Credit Block 对象状态更新
这次"AI 建议 + 人类确认"的经验作为结构化数据沉淀回 Ontology，优化后续推荐
安全是在 Ontology 层统一定义的——"生产团队能看到全球机器遥测、仓储人员按区域受限、供应链分析师有行列级权限" ，所有 AI 智能体的权限要么继承自人类用户，要么继承自项目权限结构 。

🛒 零售/电商行业的真实落地形态

把上面这套骨架套到真实零售客户身上，你能看到的是这样的"效果侧"全链路：

Wendy's QSCC（6500 家餐厅）：
数据连接：餐厅 POS、库存系统、配送中心
Ontology：餐厅、订单、库存、配送资源作为对象
AIP：自动化库存管理和资源分配的决策
效果：原本要几周的库存问题 → 5 分钟修复；8 个月内从 10 家试点店扩展到 4000 家店​
Heineken USA：
数据连接： brewery、warehouse、customer data + 实时船舶监控
AIP：算法预测供应链需求，AI 检测潜在缺货事件并自动调整配送计划
效果：测试 2 天处置 25 个分销商预警（价值 $300K），$4.9M 防缺货价值解锁
Lowe's（与 NVIDIA 合作）：
构建涵盖全球供应链的"数字孪生"
AI 实时模拟物流变化与中断场景
POC 到生产 不到 4 个月​
🎯 给你的"全链路还原"总结

如果你要在内部汇报或者自己搭一套类似体系，可复用的全链路模板是这样的：
纯文本
源系统 (SAP/Salesforce/定制系统)
    ↓ [HyperAuto / SDDI] 自动连接 + 元数据驱动管道生成
原始数据集
    ↓ [Pipeline Builder] 低代码清洗、标准化
业务数据集
    ↓ [Ontology 建模] 映射为 Object / Property / Link / Action
企业数字孪生 (OMS 管 schema, OSS 管读, Funnel 管写)
    ↓ [AIP Logic + OAG] LLM 基于 Ontology 推理，调用 Action
AI 决策建议
    ↓ [Workshop] 无代码应用搭建，绑定 Ontology 对象
业务用户交互界面
    ↓ [Action 执行] 经 Funnel 校验后写回 ERP / CRM
源系统状态更新 → Ontology 同步刷新 → 闭环
⚠️ 关于"电商详细案例"的实话：目前公开渠道没有一个电商客户把上面每一环的具体配置（哪张表、哪个对象、哪个 Action）完整披露。Palantir 的商业模式决定了客户案例更多是"效果叙事"。如果你想看真正的逐字段、逐对象的细节，只有两条路：① 成为 Palantir 客户走 POC，② 仔细研究 Titan Industries 的官方 Demo（这是目前最接近"电商订单场景"的开源范本）。

接着上一轮的全链路骨架，这一轮我直接下钻到每一步 Palantir 在官方 Demo（Titan Industries 订单到现金）里到底做了什么操作——这是目前公开渠道能拿到的、最接近"逐环节还原"的材料。同时把 Wendy's / Heineken / Lowe's 这几个零售/餐饮/快消真实客户作为"行业佐证"嵌进去，让你看到这套范式在电商/零售供应链里长什么样。

📌 先校准预期：Palantir 官方愿意公开"操作范式"，但不会披露真实客户的具体表名→对象名→Action 映射（这是商业机密）。所以下面 Titan 的部分是"操作级细节"，零售客户的部分是"效果级细节"——两者拼起来，就是你能在公开网络挖到的全部。

一、数据连接层：HyperAuto 到底"自动"了什么

对应官方文档：HyperAuto V2 Architecture

很多人以为 HyperAuto 只是个连接器，其实它是一个三层编排器：Data Syncs → Builder Pipelines → Ontology，一次性自动生成可用输出 。

具体到 Titan 的 SAP 订单到现金场景，HyperAuto 干了这四件事 ：
源表探查与同步：利用 SAP 的元数据（metadata），实时查询源系统，自动推导 sync 方式
自动重命名：把 SAP 的天书列名（如 EKPO~NETPR）翻译成人类可读的业务术语（如 "Net Price"）——利用源的元数据做 renaming
自动 Join：根据对源数据模型的理解，把规范化存储的关联表自动 join 成一张宽表
自动生成 Ontology：利用源的数据模型，动态生成 Ontology 对象和它们之间的语义链接——从新源到完整定义的 Ontology，"几分钟、零人工干预"
💡 关键认知：HyperAuto 不是 ETL 工具，它是 SDDI（Software-Defined Data Integration）——用源代码系统的 metadata 来"推导"整条管道 。这就是为什么 Palantir 实施周期能从传统的"数月"压缩到"数天"。

零售行业的对应形态：Wendy's QSCC 接入的是 6400+ 家餐厅的 POS、库存、配送中心数据 ；Heineken USA 接入的是 brewery + warehouse + customer + 实时船舶监控 ；Lowe's 则是全球供应链的网络数据 。这些源系统的 connector 层走的都是同一套 HyperAuto 机制。

二、数据转换层：Pipeline Builder 构造"流程挖掘双表"

对应官方文档：Building with Palantir AIP: AI-Powered Process Mining

原始 SAP 数据不能直接用于流程挖掘。Pipeline Builder（低代码/无代码生产级管道工具）在这里构造两个标准数据集：

数据集 | 作用 | Titan 场景的实例
Process Object Dataset​|描述在流程中"移动的东西"| Sales Order Item（销售订单行）|Log Object Dataset​|描述流程对象经过的每个步骤| 只需 3 列：①对象主键（关联销售订单行）②当前状态（如"已创建"、"已冻结"、"已发货"）③进入该状态的时间戳

Pipeline Builder 从数百个函数的库里拖拽转换逻辑，把 HyperAuto 同步过来的 SAP 数据快速转换成这两种 schema 。

📌 这一步的"为什么"：流程挖掘算法只需要"对象+状态+时间"三元组。把复杂的 SAP 订单表降维到这个最小结构，是后面 Machinery 能做流程可视化的前提。

三、Ontology 层：把"订单到现金"缝进企业数字孪生

对应官方文档：同上 + Platform Overview

这是 Palantir 区别于所有数据中台的关键一层。Ontology 不是"语义层"，它是决策中心模型（decision-centric model）——把数据、逻辑、动作统一封装 。

Titan 场景下的具体操作 ：
在 Pipeline Builder 的数据预览界面直接创建 Ontology 对象（如 Sales Order Item、Credit Block）
在 Ontology Manager 里定义对象：命名、配置访问管理、校准属性元数据
链接到 Titan 已有的 Ontology 对象：比如 Sales Order Item 一定要 link 到 Customer、Product、Production Line——因为"一个销售订单会影响哪条生产线"这种跨域关系，正是 AI 能做智能决策的基础
为什么这一步决定 AI 的成败？Palantir 的原话："这个决策模型越忠实于企业日常运营的真实情况，AI 工具就越能有效运作" 。换句话说，Ontology 建得越完整，AIP Logic 里的 LLM 能拿到的上下文就越丰富。

零售行业的 Ontology 形态（基于公开效果反推）：
Wendy's：Restaurant、Inventory、Distribution Center、Production Line 作为核心对象，支持"配送中心级别的建模"
Heineken：Brewery、Warehouse、Distributor、Vessel 作为核心对象，加上实时船舶位置
Lowe's：构建的是"全球供应链的数字孪生"——这意味着 Supplier、Distribution Hub、Store、Shipment 等都是 Ontology 对象
四、流程洞察层：Machinery 把 Ontology 变成可视化流程图

对应官方文档：Building with Palantir AIP

Machinery 提供一个点击式界面，把上一步建好的 Ontology 对象自动解释成可交互的流程图​ 。

Titan 的场景产出：一张展示"订单创建 → 信用冻结激活 → 发货单创建 → 交货"的真实流程路径图，其中：
99% 的订单顺利走完
2% 的订单被 Credit Block 卡住
总共 3709 个销售订单行中，有 57 个活跃订单冻结，冻结金额 $25M​
业务用户可以在这张图上同时看宏观趋势和微观个例——比如下钻到某一个具体被冻结的订单，看它的客户历史、信用额度、订单金额 。

五、AI 决策层：AIP Logic 的"教实习生"范式

对应官方文档：Building with Palantir AIP + Reducing Hallucinations with the Ontology

这是最精彩的部分。AIP Logic 是一个无代码 LLM 函数开发环境，Palantir 的部署策略师 Ruben 用了一个比喻："就像教一个聪明但缺乏背景知识的实习生" 。

具体操作步骤（Titan 信用冻结场景）：

1. 选定 Ontology 对象：告诉 AIP Logic 要处理的是 Sales Order Item 这个对象

2. 提取参数：从该对象抽取具体属性作为 LLM 可用的参数，例如：
credit_status（信用状态）
order_id（订单 ID）
customer_credit_limit（客户信用额度）
12_month_historic_order_volume（12 个月历史订单量）
12_month_paid_on_time_rate（12 个月按时付款率，0-1 之间的值）
3. 用自然语言写"评分标准"（Rubric）：

"如果订单金额大幅高于信用额度和历史订单值，且客户按时付款率低 → 建议维持信用冻结"

4. 要求 LLM 输出推理过程：不仅输出"维持/解除"的决定，还要输出推理理由，存到变量里

5. 把决策和理由写回 Ontology：最终建议 + 推理过程都回写到 Titan 的 Ontology 中

6. 用 Debugger 验证：AIP Logic 的调试器能透明展示 LLM 如何理解每条指令，确保它按预期工作

反幻觉机制（这是 Palantir 企业级 AI 的核心壁垒）：

在另一个 Titan 场景（库存短缺支持工单）里，Palantir 展示了 OAG 的两层防幻觉 ：
数据工具：LLM 不直接回答"哪个配送中心最近"，而是调用 Ontology 里的自定义 Function（用 Haversine 公式计算距离），把计算委托给确定性逻辑
人工审查队列：AIP Logic 不直接把"重新分配库存"的 Action 写回外部系统，而是把建议放进队列等专家审批​ ——"Human-AI teaming"模式
六、应用层：Workshop 组装端到端界面

对应官方文档：Building with Palantir AIP + Palantir Learn

Workshop 是 Foundry 的无代码/低代码应用构建器 。Titan 场景里：
Machinery 生成的流程图本身就是一个 Workshop Widget——可以直接嵌入
拖拽其他组件（表格、图表、按钮）快速搭建端到端流程挖掘应用
业务用户在一个界面看到：所有信用冻结信息 + AI 建议 + 推理过程 + 执行按钮
界面上展示的关键指标：3709 个总销售订单行 / 57 个活跃冻结 / $25M 冻结金额 / AIP 建议升级或解除​
💡 Workshop 应用是 Ontology-aware​ 的——绑定的对象属性变了，界面实时变。

七、自动化层：Automate 实现无人值守

对应官方文档：Building with Palantir AIP

最后一步，用 Automate 把上述工作流编排成自动化：
触发器：Last Stop is Credit Block Activated（最后一个状态是"信用冻结已激活"）
条件：Sales Order Item (OOC) Process Mining 对象集
动作：Machinery OZC Run Credit Block Logic（运行信用冻结逻辑）
即：每当一个新订单被信用冻结，Automate 自动触发 AIP Logic 函数，生成"维持/解除"建议，在人环（human-in-the-loop）模式下让业务用户秒级决策，而不是原来的 9 天 。

🛒 零售/电商行业的真实落地对照

把上面 Titan 的"操作级范式"映射到三个零售/餐饮/快消客户：

Wendy's QSCC（6400+ 餐厅）
全链路形态：Foundry + AIP 做供应链数字孪生
核心 Ontology 对象：Restaurant、Inventory、Distribution Center
AIP 作用：Dynamic Inventory Management（动态库存管理）、Variance and Gain Information（偏差与收益信息）、Demand Deviation and Allocation（需求偏差与分配）
效果：原本要几周的问题 → 5 分钟修复；8 个月内从 10 家试点店扩展到 4000 家店​
Heineken USA
全链路形态：brewery + warehouse + customer + 实时船舶监控 全部接入 Ontology
AIP 作用：先进算法预测供应链需求 + AI 检测潜在缺货事件 + 自动调整配送计划
效果：测试 2 天处置 25 个分销商预警（价值 $300K）；$4.9M 防缺货价值解锁；"3 个月构建了之前需要 3 年的东西"
Lowe's（与 NVIDIA 合作）
全链路形态：构建全球供应链的"数字孪生"（digital replica）
Ontology 作用：把复杂数据和逻辑组织成相互关联的虚拟对象、链接和动作
效果：POC 到生产不到 4 个月​
🎯 全链路"操作级"总结（这才是你要的还原）

如果你要在内部汇报或者自己搭一套类似体系，可复用的全链路模板是这样的：
纯文本
源系统 (SAP/Salesforce/定制系统)
    ↓ [HyperAuto] 自动连接 + 元数据驱动管道生成 + 自动重命名/Join/生成 Ontology 对象
原始数据集
    ↓ [Pipeline Builder] 低代码构造 Process Object + Log Object 双表
流程挖掘数据集
    ↓ [Ontology Manager] 创建对象 + 配置权限 + 链接到企业已有对象
企业数字孪生（决策中心模型）
    ↓ [Machinery] 点击式生成可视化流程图
流程洞察
    ↓ [AIP Logic] 选定对象 + 提取参数 + 自然语言 Rubric + 输出推理 + 写回 Ontology
AI 决策建议（带 Human-in-the-loop 审查队列）
    ↓ [Workshop] 拖拽组件组装端到端应用（Machinery 流程图作为 Widget 嵌入）
业务用户交互界面
    ↓ [Automate] 条件触发（如"信用冻结激活"）→ 自动运行 AIP Logic 函数
持续优化的决策飞轮
⚠️ 关于"电商详细案例"的实话（续）：目前公开渠道仍没有一个电商客户把上面每一环的具体配置（哪张表、哪个对象、哪个 Action 的字段级映射）完整披露。Palantir 的商业模式决定了客户案例更多是"效果叙事"。如果你想看真正的逐字段、逐对象的细节，只有两条路：① 成为 Palantir 客户走 POC，② 把 Titan Industries 的官方 Demo 吃透（这是目前最接近"电商订单场景"的开源范本）。

一、AIP Logic "教实习生" prompt 的写法范式

Palantir 官方对 AIP Logic 的定位很清晰：Logic 函数由 Block 组成，每个 Block 有明确的输入/输出；其中 Use LLM Block 是核心，由 Prompt + Tools + Output 三部分构成​ 。所谓"教实习生"，本质是用 Prompt 框定角色与任务，用 Tools 限制 LLM 的能力边界，用 Output 强制结构化返回。

1. Prompt 的"三段式"黄金结构

官方文档明确建议 ：先用最重要的信息开头（任务概述），再给 LLM 需要用到的数据，最后指导它何时使用工具。可抄写的模板如下：
纯文本
[第一段：角色与任务概述]
You are my {领域} expert agent. 
Your task is to {具体任务，一句话}.
Success looks like: {可衡量的成功标准}.

[第二段：可用数据与上下文]
You have access to the following Ontology objects and their properties:
- {对象A}: {属性1}, {属性2}, {属性3}
- {对象B}: {属性1}, {属性2}
(这些通过 "/" 引用变量注入，不要硬编码)

[第三段：工具使用时机与推理要求]
When you need to {查询类操作}, use the Query objects tool.
When you need to {计算类操作}, use the Calculator tool or Call function.
When you have made a final decision, use the Apply action tool to {写回动作}.

You MUST show your chain-of-thought reasoning before giving the final answer.
Your final output MUST be in the following JSON structure:
{
  "decision": "maintain_block | release_block",
  "confidence": 0.0-1.0,
  "reasoning": "step-by-step explanation referencing specific object properties",
  "proposed_action": "description of the action to be executed"
}
2. Titan Industries 信用冻结场景的"真实 prompt"还原

基于官方 OAG 文档与流程挖掘案例 ，这个场景的 prompt 大致是这样写的（这是我根据官方描述还原的范式，不是逐字原文）：
纯文本
You are a credit risk analyst agent for Titan Industries.
For the Sales Order Item provided, decide whether the credit block 
should be MAINTAINED or RELEASED.

You can access the Sales Order Item's properties:
/credit_status/, /order_value/, /customer_credit_limit/, 
/12_month_historic_order_volume/, /12_month_paid_on_time_rate/

Decision rubric:
- If order_value significantly exceeds customer_credit_limit AND 
  12_month_paid_on_time_rate < 0.7 → MAINTAIN the block
- If order_value is within credit_limit AND 
  12_month_paid_on_time_rate >= 0.9 → RELEASE the block
- Otherwise → MAINTAIN but flag for human review

First use Query objects to pull the customer's payment history,
then provide your reasoning, then call Apply action to record 
your decision (but do NOT auto-execute without human approval).
3. 反幻觉的关键：让 LLM "去查"而不是"去回忆"

这是 Palantir 反复强调的核心原则 。官方反幻觉文章里有一个经典例子：问 LLM "Titan Industries 的美国配送中心在哪些城市"，LLM 会一本正经地列出纽约、洛杉矶、芝加哥——全是幻觉，因为 Titan 是虚构公司，这些信息只在本体里 。

正确的做法：在 AIP Logic 里挂上 Query objects tool，让 LLM 通过工具查询 Ontology 拿到真实数据 。这就是为什么 Palantir 说"准确性 = 高质量本体(Data) + 确定性工具(Logic) + 全链路溯源(Audit)"。

Tools 的四类配置（这是"教实习生"的能力边界）：

Tool 类型	作用	何时给 LLM 用
Query objects​	查询本体对象	LLM 需要读取业务数据时
Call function​	调用确定性函数	需要做精确计算/预测/优化时
Calculator​	精确数学计算	LLM 不擅长的算术
Apply action​	写回本体/触发动作	做出决策需要执行时

关键认知：LLM 没有直接工具访问权，它只能"请求"使用工具，工具调用由 AIP Logic 在调用用户的权限范围内执行 。这就是"教实习生"的安全边界——实习生可以建议，但每次操作都要在你的权限下执行。

4. prompt 生效的 5 条工程经验

基于官方文档提炼 ：
任务概述放最前面——LLM 对 prompt 开头和结尾的注意力最强
数据用 "/" 引用变量注入，不要硬编码到 prompt 文本里（保证 token 效率）
Query objects 时指定具体属性，不要开放整个对象——既省 token 又降噪
要求输出 Chain-of-Thought——官方 OAG demo 里明确展示了 LLM 的推理步骤和访问的对象，提供透明度
用 Debugger 验证——AIP Logic 的调试器能透明展示 LLM 如何理解每条指令
二、HyperAuto 自动生成的 Ontology 对象 ↔ SAP 表映射

1. HyperAuto 的工作机制（官方口径）

HyperAuto V2 架构明确 ：利用源系统的元数据，实时查询源系统，自动推导​ sync 方式、transformation 逻辑、以及合适的 Ontology 设计。具体做四件事 ：
Cleaning：修复数据类型、null/空值、字符串空格等问题
Renaming：用 SAP 元数据把 EKPO~NETPR 这种列名翻译成人类可读形式
Joining：理解 SAP 数据模型，把规范化的分表 join 成宽表
Ontology 生成：动态生成映射到现实概念的对象类型，预定义属性和关系
AWS 联合发布的 HyperAuto 文档进一步确认：自动管道生成器会动态生成一组对象类型，映射到现实世界概念如 materials、customers、sales orders，并预定义属性和关系​ 。

2. SAP 表 → Ontology 对象的合理映射（基于 SAP 标准模型推断）

下面是订单到现金（O2C）和采购到付款（P2P）场景下的常见映射。注意：这是基于 SAP 标准数据模型和 HyperAuto 工作机制的合理推断，实际 POC 中以 HyperAuto 自动生成结果为准。

销售与分销（SD）模块
SAP 表	表含义	推断的 Ontology 对象	关键属性映射
VBAK​	销售文档头	Sales Order	VBELN→订单号, KUNNR→客户ID, VDATU→交付日期
VBAP​	销售文档项	Sales Order Item	POSNR→行号, MATNR→物料编号, NETWR→净订单价值, EDATU→创建日期
KNA1​	客户主数据	Customer	KUNNR→客户ID, NAME1→客户名称, KTOKD→客户分类
MARA​	物料主数据	Product / Material	MATNR→物料编号, MTART→物料类型, MEINS→计量单位
LIKP / LIPS​	交货头/项	Delivery	VBELN→交货单号, WADAT→实际发货日期
VBRK / VBRP​	开票头/项	Invoice	VBELN→发票号, NETWR→发票金额, 

流程挖掘案例的中文拆解材料明确提到：Process Object Dataset 在订单到现金中是 sales order item，源数据表选用 VBAP 表（销售文档项数据表）​ ——这印证了 VBAP → Sales Order Item 的映射。

采购（MM）模块
SAP 表	表含义	推断的 Ontology 对象
EKKO​	采购订单头	Purchase Order
EKPO​	采购订单项	PO Item
LFA1​	供应商主数据	Vendor / Supplier
EKBE​	采购凭证历史	PO History

Palantir 开发者社区的 MCP 脚本示例里，明确出现了 EKKO→Purchase Orders、EKPO→PO Items、KNA1→Customers 的映射代码 ，可作旁证。

信用与财务

SAP 表	推断的 Ontology 对象
KNKK​ (客户信用主数据)	Customer Credit → 属性含信用额度、信用冻结状态
BSAD / BSID​	Customer Payment History → 用于计算按时付款率


3. HyperAuto 自动生成的"增值"部分

光有表映射还不够，HyperAuto 的真正价值在于自动构建的关系​ ：
Sales Order Item → Customer：通过 KUNNR 外键自动建立 link
Sales Order Item → Product：通过 MATNR 自动建立 link
Sales Order → Sales Order Item：一对多父子关系
跨模块 link：如 Sales Order Item → Delivery → Invoice 的履约链路
这些 link 在 Ontology 里表现为 Link Type，是后续 AIP Logic 能让 LLM "看到关联关系"的基础——比如 LLM 判断信用冻结时，能顺着 link 追溯到该客户的所有历史订单和付款记录。

4. 写回（Write-back）的 SAP 侧机制

这是 Palantir 的"杀手锏"——决策不只是建议，而是通过 BAPI（远程启用函数模块）写回 SAP​ 。在信用冻结场景里：
纯文本
AIP Logic 决策 "RELEASE" 
  → Apply action (Release Credit Block)
  → Action 调用 BAPI_CREDITORDER_RELEASE 或类似的 BAPI
  → SAP 侧 EKKO-EBELN 状态更新
  → Ontology 中 Sales Order Item 的 credit_status 同步刷新
三、Automate 生产环境的触发器与 Action 配置

1. Automate 的核心模型

官方定义 ：Automate 是条件（Conditions）连续或定时检查 + 效果（Effects）自动执行的业务自动化工具。条件可以是时间-based、对象数据-based、或两者组合。

可用的条件类型​ ：
条件类型	触发时机	典型场景
Time​	到达指定时间（如每周一 9 点）	定时报表发送
Objects added to set​	预定义对象集中出现新对象	新告警/新订单出现
Objects removed from set​	对象离开对象集	工单关闭
Objects modified in set​	对象集中对象被修改	订单状态变更
Run on all objects​	周期性对集合中所有对象运行	批量重算
Metric changed​	聚合指标变化	总量突破阈值
Threshold crossed​	指标越过阈值	温度超过 120°

可用的效果类型​ ：
Submit Foundry actions（提交本体动作——最核心的生产级效果）
Trigger AIP Logic functions（触发 AIP Logic 函数）
Execute Foundry functions（执行 Foundry 函数）
Send platform and email notifications（发送通知，支持附件）
2. 信用冻结场景的生产级配置范例

结合官方文档 ，这是一个真实的 Automate 配置：

Step 1: 创建 Automation
打开 Automate 应用 → + New automation
Step 2: 配置 Condition
纯文本
Condition Type: Objects modified in set
Object Set: Sales Order Items where credit_status == "BLOCKED"
Expose effect input: Modified objects (单个对象)
Check frequency: Real-time (实时) 或 Every 5 minutes (高频场景)
Step 3: 配置 Effect（Action）
纯文本
Effect Type: Action
Selected Action: "Evaluate Credit Block Decision" 
  （这是一个预先定义的 Action，背后调用 AIP Logic 函数）
Parameter mapping:
  - sales_order_item: 绑定到 condition 暴露的 Modified object
  - decision: 由 AIP Logic 函数输出
  - reasoning: 由 AIP Logic 函数输出
Execution mode: Per-object（因为每个信用冻结需独立 AI 评估）
Step 4: 配置第二个 Effect（Human-in-the-loop）
纯文本
Effect Type: Notification
Recipients: 信贷分析师团队
Message: "New credit block evaluated for SO {{order_id}}. 
          AI suggests: {{decision}}. Reasoning: {{reasoning}}.
          Click to approve/reject."
Step 5: 配置第三个 Effect（写回 SAP）
纯文本
Effect Type: Action
Selected Action: "Apply Credit Release" 或 "Maintain Credit Block"
Trigger condition: 当 human 在 Workshop 中点击批准按钮时
（这一步通常通过一个独立的 Action 触发，而非 Automate 直接执行，
确保 human-in-the-loop）
3. 生产环境性能最佳实践（官方硬性要求）

这是生产部署最容易踩坑的地方，Palantir 官方给出了明确的资源优化杠杆 ：

杠杆一：条件配置（最重要）

⚠️ 官方原话 ：对于一个每天更新 100 次的 1000 对象类型，仅用 "on object update" 条件可能导致每天最多 100,000 次自动化评估（100 次更新 × 1000 对象）。加上 5 分钟的时间条件后，评估次数上限降至每天 288 次（1440÷5），最高减少 340 倍。

配置规则：
高频更新对象（每天 100+ 更新）：必须组合时间条件 + 对象集条件，用时间条件封顶评估频率
低频更新对象：单独使用对象更新条件即可
杠杆二：执行模式

官方建议 ：默认使用 Single execution（单执行），而非 Per-object execution——前者对所有触发对象一次性执行效果，后者逐个执行。
纯文本
✅ 推荐：Single execution
   100 个被触发的告警 → 1 次执行 → 批量处理

❌ 不推荐：Per-object execution  
   100 个被触发的告警 → 100 次执行 → 逐个处理
例外情况用 Per-object：当你需要隔离失败、或不同对象需要不同配置处理时。

杠杆三：效果设计

动作效果需要支持批量处理 。最佳实践是用 Object Set 作为参数类型——这样可以高效传递超大规模对象集（甚至 1000 万个对象）。

4. 真实生产配置范例（基于官方最佳实践反推）

以"设备温度超过 120° 触发告警"为例（来自 Palantir 开发者社区） ：
纯文本
Condition:
  Type: Threshold crossed
  Object: Machine
  Property: temperature  
  Threshold: > 120°
  Check frequency: Live（实时流式）或 Scheduled

Effects:
  1. Notification → 发送给运维团队（邮件+平台通知）
  2. Action "Create Alarm Ticket" → 参数 machine: 绑定的触发对象
  3. (可选) Trigger AIP Logic function → 调用诊断函数
🎯 三块拼起来的生产级全链路

把上面三块串起来，一个生产就绪的信用冻结自动化长这样：
纯文本
[SAP EKKO/EKPO/VBAK/KNA1/KNKK]
    ↓ HyperAuto 自动 sync + rename + join + 生成 Ontology 对象
[Foundry Datasets: Sales Order, Sales Order Item, Customer, Customer Credit]
    ↓ Ontology Manager 建立 Link Type
[Ontology Objects + Links + Actions]
    ↓ AIP Logic: Use LLM Block
      Prompt(角色+任务+rubric) + Tools(Query objects, Call function, Apply action)
      输出: {decision, confidence, reasoning}
    ↓ Automate 编排
      Condition: Sales Order Item modified + credit_status=BLOCKED
      Effect 1: Action "Record AI Evaluation" （写回本体）
      Effect 2: Notification → 信贷分析师
      Effect 3: 人工在 Workshop 点击批准 → Action "Apply Credit Release" 
                → BAPI 写回 SAP → Ontology 同步刷新
💡 生产部署的三个铁律（来自官方最佳实践）：
高频对象必加时间条件封顶——否则资源消耗爆炸
默认单执行模式 + Object Set 参数——批量处理才能 scale
Human-in-the-loop 不可省略——AIP Logic 的 Apply action 在无人值守场景必须配合审批队列
关于"公开资料边界"的最后说明

需要诚实告诉你：
AIP Logic 的 prompt 模板：上面给的是基于官方 Blocks 文档 的最佳实践范式，Titan 案例的真实 prompt 原文 Palantir 未完全公开
SAP 表映射：EKKO/EKPO/VBAK/MARA 等映射是基于 SAP 标准模型和社区实践 的合理推断，Palantir 官方只确认 HyperAuto 会"动态生成映射到 materials/customers/sales orders 等现实概念的对象类型"​ ，未公开完整映射表
Automate 配置：这部分是官方文档明确支持的​ ，上面的范例可以直接照抄到 Foundry 环境
接着上一轮的三个下钻点，我直接给你"截图级"的操作路径。需要提前说明：Palantir 官方文档提供了完整的配置字段和机制描述，但没有公开真实截图——下面的内容是依据官方文档还原的"点击路径+配置项"，你可以直接在 Foundry/AIP 环境中对照操作。

一、AIP Logic 里 Calculator 与 Call function 的配置路径

1. 先理解 AIP Logic 的界面布局

打开 AIP Logic 后，界面从左到右分为三块 ：
左侧面板：Inputs（输入）、Blocks（逻辑块）、Outputs（输出）的配置区
中间/调试区：Debugger，展示 LLM 的 Chain-of-Thought（CoT）
右侧面板：Run 面板，运行和查看历史
一个 Logic 函数就是由若干 Block​ 串联组成的，每个 Block 有输入、输出，前一个 Block 的输出可以作为后一个 Block 的输入 。

2. Calculator 工具的配置（精确数学计算）

Calculator 在官方文档里被定义为："enable you to perform accurate mathematical calculations with an LLM"​ ——即让 LLM 能做精确数学计算 。

配置路径（截图级步骤）：
纯文本
Step 1: 在 AIP Logic 编辑器画布上，添加一个 "Use LLM" Block
Step 2: 选中该 Block，在右侧配置面板找到 "Tools" 区域
Step 3: 点击 "Add tool" → 选择 "Calculator tool"
Step 4: Calculator 工具无需额外参数配置，添加即可用
Step 5: 在 Prompt 中明确指示 LLM 何时使用计算器
Prompt 中引导使用 Calculator 的写法（基于 Titan 供应链预测场景的官方范例 ）：
纯文本
You are my supply chain analyst. 
When calculating the total forecasted demand across multiple 
distribution centers, use the Calculator tool to ensure accuracy.
Do not compute large sums in your head.
官方 RAG/OAG 视频里 Titan 场景的真实做法是：在 Use LLM Block 中同时添加 Calculator tool + 一个 "Forecasting Customer Orders" 的 Logic 函数，Prompt 写成"像给新分析师的逐步指导"，明确告诉 LLM 何时调用预测工具 。Debugger 里能看到 LLM 真的调用了计算器做精确数学运算。

💡 Calculator 的使用要点：它专门承载 LLM 不擅长的精确算术。Palantir 的设计哲学是——LLM 负责推理和决策，确定性计算交给工具。

3. Call function 工具的配置（调用 Functions on Objects）

Call function 允许 LLM 调用两种函数 ：
代码定义的函数（在 Functions 仓库里用 TypeScript 写的）
已有的 Logic 函数（其他 AIP Logic 函数）
前置条件：必须先有一个已发布的 Function。函数定义时必须有明确的入参和返回值，且文档注释（JSDoc）是关键——LLM 看不懂代码逻辑，只能通过注释理解函数的用途和参数格式 。

配置路径（截图级步骤）：
            纯文本
            Step 1: 在 Functions 仓库发布一个带有清晰 JSDoc 注释的函数
                    /**
                    * Searches for employees based on department and role.
                    * @param department The department code (e.g., 'IT', 'HR')
                    * @param role The job title
                    */
                    @Function()
                    public searchEmployees(department: string, role: string): Promise<...>

            Step 2: 在 AIP Logic 画布添加 "Use LLM" Block
            Step 3: 右侧配置面板 → Tools → Add tool → 选择 "Call function"
            Step 4: 在搜索框输入函数名，选中目标函数
            Step 5: 配置参数映射（核心步骤）
Step 5 参数映射的三种模式：

模式	适用场景	配置方法
LLM Generated​	希望 LLM 从自然语言中提取参数	保持默认，LLM 读取函数签名自动生成
Fixed/Static Value​	参数恒为固定值	在参数配置中硬编码，如 status = "Active"
Variable​	使用上一步 Block 的输出变量	绑定 Logic 流程中的既有变量


配置函数执行后的行为：
纯文本
- Feedback to LLM（默认）：函数返回值作为上下文回喂 LLM，LLM 生成最终回复
- Pass to Logic Output：函数结果直接作为整个 Logic 的输出，LLM 不再加工
⚠️ Call function 的三个工程要点：
Description is King——函数名和 JSDoc 注释必须清晰，LLM 靠这个决定要不要调用
尽量用简单类型——String / Number / Boolean / Date 最稳定，避免让 LLM 构造复杂 JSON
函数内需有错误处理——查不到数据时返回清晰字符串（如 "No order found with ID 123"），避免抛异常
4. Apply action Block（确定性调用，不走 LLM）

除了在 Use LLM 里作为 Tool，AIP Logic 还提供一个独立的 Apply action Block​ ：
纯文本
用途：确定性地调用 Action，精确控制参数填充，加速执行
与 Use LLM 中 Apply actions Tool 的区别：
  - Apply action Block：直接、确定地调用，不经过 LLM 推理
  - Use LLM 中的 Apply actions Tool：LLM 自主决定是否调用

关键限制：要通过 Action 写回 Ontology，必须从 Action 或 Automation 调用 Logic 函数
完整配置流程（基于官方入门文档 ）：
纯文本
1. 在 Use LLM Block 中配置 Apply actions Tool，描述何时使用
2. 迭代调试 Logic 函数（Debugger 中看到的是"拟议的 Ontology 编辑"，不会真执行）
3. 点击 "Publish" 发布 Logic 函数
4. 创建一个新的 Action，backend 选择刚发布的 Logic 函数
5. 在 Workshop 中调用该 Action，或使用 Automate 触发
二、HyperAuto 针对 S/4HANA CDS View 映射为 Ontology 的机制

1. 先厘清 S/4HANA 的三种数据源形态

根据 Palantir 官方 SAP 对象类型文档 ，Foundry 的 SAP 连接器支持多种数据源形态，且不同形态的增量同步策略不同：
数据源类型	增量模式支持
ERP Table（如 EKKO, VKPO）	Multiple fields / Concatenate fields / Change document table / Twin table
CDS View​	Multiple fields / Concatenate fields
HANA View​	Multiple fields / Concatenate fields
BW Content Extractor​	Multiple fields / Concatenate fields / SAP built-in delta

2. HyperAuto V2 对 CDS View 的处理流程

HyperAuto V2 架构明确 ：利用数据源的元数据，实时查询源以推断同步方式、变换逻辑和 Ontology 设计。整个管道包含三个主要组件 ：
纯文本
CDS View (S/4HANA)
    ↓ [数据同步层]
Foundry Dataset（原始同步）
    ↓ [构建器管道层 - 自动生成]
    - Source-specific preprocessing（元数据数据集生成）
    - Cleaning libraries（标准化数据清洗）
    - Core generation（数据丰富、列重命名、去重、合并）
    - Derived elements（Join 表、时间序列、丰富列）
    ↓ [Ontology 层 - 自动生成]
Ontology Object Types + Properties + Link Types
3. CDS View → Ontology 的具体映射机制

基于 AWS 官方博客的技术描述 ，HyperAuto 对 SAP 源的处理包含：

Step 1: 源探索（Source Explorer）
浏览 SAP 模块（Material Management / Sales Distribution 等）
下钻发现关联对象（Material、Vendor、Purchase Order 等）
检查 CDS View 的 schema 并预览数据
利用源系统元数据，消除对 SAP 专业知识的依赖​
Step 2: 自动管道生成（Automatic Pipeline Generator）
读取 CDS View 的元数据
自动重命名：把技术性字段名转为人类可读名称
自动 Join：根据 SAP 数据模型理解，把规范化分表 join 成宽表
自动生成 Ontology 对象类型
Step 3: 写回机制
通过 SAP 的 远程启用函数模块（Remote-enabled Function Modules）​ 实现写回
通常使用 BAPI（Business Application Programming Interface）functions​
4. CDS View 场景的典型对象映射（基于 SAP 标准模型推断）

虽然 Palantir 官方未公开完整的 CDS View → Ontology 映射表，但基于 AWS 博客确认的"自动生成映射到 materials, customers, sales orders 等现实概念的对象类型" ，可以推断典型映射：

S/4HANA CDS View 类别
推断生成的 Ontology 对象
映射机制
I_PurchaseOrder（采购订单 CDS）
Purchase Order 对象
自动重命名 + 属性映射
I_SalesOrder（销售订单 CDS）
Sales Order 对象
自动 Join 相关 CDS
I_Product（产品主数据 CDS）
Product / Material 对象
属性映射
I_Customer（客户 CDS）
Customer 对象
属性映射
I_Supplier（供应商 CDS）
Vendor / Supplier 对象
属性映射
关键认知：

CDS View 在 S/4HANA 里本身就是语义层——它已经把底层的 EKKO/EKPO 等透明表做了一次业务封装。HyperAuto 读取 CDS View 的元数据后，直接映射到业务概念对象，跳过了"透明表 → 业务实体"的转换环节，这是 CDS View 相比直接读透明表的优势 。

5. 在 Foundry 中查看 HyperAuto 生成结果的方法

实际操作中，你可以在以下位置检视映射：
Data Connection​ → 查看自动生成的 Sync 配置
Pipeline Builder​ → 查看自动生成的清洗/Join 管道
Ontology Manager​ → 查看自动生成的对象类型、属性、Link Type
三、Automate / Action 中 Webhook 调用外部系统 API

1. 整体架构

Webhook 在 Foundry 里有两层配置 ：
Data Connection 中定义 Webhook（定义对外部系统的 HTTP 请求）
Action 中引用 Webhook（将 Action 参数映射到 Webhook 输入参数）
当终端用户在 Foundry 中执行 Action 时，触发对外部系统的 HTTP 请求 。

2. Data Connection 中创建 Webhook（截图级步骤）

Step 1: 创建 REST API Source​
纯文本
导航：Data Connection → Sources tab → New source → REST API
在 Source Editor 中填写：
  - 基础 URL（如 https://api.external-system.com）
  - 认证信息（Secrets）
Step 2: 创建 Webhook​
纯文本
在 Source 页面 → Webhooks tab → New webhook
New webhook wizard 配置：
  - Name: "Modify Ticket Priority"
  - Description: "Sends priority update to external ticketing system"
  - Source: 选择上一步创建的 REST API Source
  - Method: POST
  - Path: /api/v1/tickets/{ticketId}/priority
  - Body: Raw JSON
    {
      "priority": "{priority}",
      "updatedBy": "{user}"
    }
Step 3: 配置输入参数​

Webhook 支持多种参数类型 ：
参数类型	说明
Boolean	true / false
Integer / Long / Double	数值
String	文本（可约束只允许特定值）
Date / Timestamp	时间数据
List	有序集合
Record	键值对
Optional	可选输入
Attachment	文件上传

Step 4: 测试 Webhook​
纯文本
保存后 → Test Connection 侧边栏
发送测试请求 → 查看响应
从响应中提取输出参数（如新记录的 ID）
提取嵌套响应值的配置范例​ ：
纯文本
假设第一个 Webhook 调用返回：
{ "results": { "unique_id": "ID4567" } }

在第二个 Webhook 的 Headers tab：
  输入 @ 触发菜单 → From a call → 选择第一个调用
  提取方式：Extract by key
  配置 keys：results → unique_id（通过 Add nested key）
3. Action 中引用 Webhook（关键：Writeback vs Side effect）

这是生产环境最容易配错的地方。官方文档明确区分了两种模式 ：

模式
执行时机
失败后行为
用户感知
数量限制
Writeback​
在 Ontology 对象变更之前​
整个 Action 失败，Ontology 不变更
看到错误
只能配 1 个
Side effect​
在 Ontology 对象变更之后​
Ontology 已变更，Webhook 失败不影响
看到成功
可配多个
Writeback 模式配置步骤​ ：
纯文本
Step 1: 导航到 Action → Logic tab → Add new rule → Webhook
Step 2: 默认是 Side effect，点击切换为 "Writeback"
Step 3: 选择目标 Webhook（如 "Modify Ticket Priority"）
Step 4: 配置输入参数映射：
        - 默认：为每个 Webhook 输入参数生成对应的 Action 参数
        - 手动：将 Webhook 输入的 "priority" 映射到 Action 参数 "Ticket Priority"
Step 5: Save
⚠️ Writeback 的事务语义：它保证了"外部系统调用失败 → Foundry Ontology 不变更"的程度原子性。但存在边缘情况：外部请求成功但 Ontology 变更失败仍可能发生 。因此严格来说它不是真正的分布式事务，而是"best effort 的事务性保证"。

Side effect 模式的生产用法​ ：
纯文本
场景：需要调用多个外部系统，或 best-effort 通知
配置：可添加多个 Side effect Webhook
执行：并行执行，无顺序保证
特殊用法：Webhook 输入参数接受 List 类型时，
         一次 Action 可触发多次 Webhook 调用（如批量通知）
4. 与 Automate 的集成

根据 AIP Logic 入门文档 ，有两种方式触发：

方式一：Action-backed Logic + Automate
纯文本
Automate Condition: 如 "Objects modified in set"
Automate Effect: Submit Foundry Action
                 → Action backend 是发布的 Logic 函数
                 → Logic 函数中包含 Apply action Block 或 Use LLM Block
                 → 链式触发 Webhook
方式二：Automate 直接调用 Logic 函数
纯文本
在 Logic 函数的右侧栏 → Automations → 创建新 Automation
Condition 触发 → 执行 Logic 函数 → Logic 函数内调用 Apply action
             → Action 触发 Webhook → 外部系统 API 被调用
5. 生产环境配置范例：跨系统工单优先级同步
纯文本
[Foundry Ontology: Ticket 对象]
    ↓ 用户在某 Workshop 应用中修改 Ticket Priority
[Action: "Update Ticket Priority"]
    ↓ Logic tab 配置：
    ↓   Rule 1: Webhook (Writeback) → "Modify Ticket Priority"
    ↓           输入映射: priority → Action parameter "Ticket Priority"
    ↓           Webhook 执行: POST https://external-system/api/v1/tickets/{id}/priority
    ↓           失败处理: 整个 Action 失败，Ontology 不变更
    ↓   Rule 2: Ontology Edit → 更新 Foundry 中 Ticket 对象的 priority 属性
    ↓           （仅在 Rule 1 成功后执行）
[外部系统：工单优先级被更新]
    ↓ Webhook 响应返回新记录的 ID
[输出参数捕获：将外部系统返回的 ID 写回 Foundry Ticket 对象]
6. 安全与网络配置要点

官方文档特别提示 ：

⚠️ 网络可达性：
如果外部系统不在 Foundry 网络可达范围，必须使用 Agent Worker Source + Agent Proxy Egress 策略
如果系统只能用 IP 地址而非域名引用，使用 Agent Proxy Runtime
建议为 Webhook 配置专用的 Agent，避免短运行的 Webhook 任务排在长运行的批量同步后面
认证配置：
REST API Source 中存储密钥（Secrets）
支持 Bearer Token、Basic Auth、API Key 等多种认证方式
可在 Header 中引用 Source 中配置的密钥
🎯 三块拼起来的生产级全链路

把上面三块串起来，一个生产就绪的"AI 决策 → 写回外部系统"全链路长这样：
纯文本
[SAP S/4HANA CDS View: I_SalesOrder, I_PurchaseOrder]
    ↓ [HyperAuto V2] 读取元数据 → 自动 sync + 自动管道 + 自动生成 Ontology
[Foundry Ontology: Sales Order, Purchase Order, Customer, Product]
    ↓ [AIP Logic] Use LLM Block
       - Tools: Query objects (读取本体)
       - Tools: Calculator (精确计算)
       - Tools: Call function (调用 TypeScript 函数做预测/优化)
       - Tools: Apply actions (LLM 决策后调用 Action)
    ↓ [Logic 函数发布]
[Action: "AI Credit Decision"]
    ↓ [Action Logic tab 配置]
       - Rule 1: Webhook (Writeback) → 调用 SAP BAPI 写回信用冻结状态
       - Rule 2: Ontology Edit → 更新 Foundry 中 Sales Order 的状态
    ↓ [Automate 编排]
       Condition: Sales Order Item modified + credit_status = BLOCKED
       Effect: Submit Action "AI Credit Decision"
[外部系统 SAP S/4HANA 信用状态被更新 + Foundry Ontology 同步刷新]
💡 生产部署的三个关键认知：
Calculator 和 Call function 是 LLM 的"确定性武器"——LLM 负责推理调用时机，工具负责精确执行
CDS View 是 HyperAuto 的"最佳拍档"——CDS 已经是语义层，HyperAuto 读取其元数据后能直接生成业务对象，跳过透明表到业务实体的转换
Webhook 的 Writeback vs Side effect 选择决定数据一致性——与外部系统强一致用 Writeback，best-effort 通知用 Side effect
关于"截图级"的诚实说明

需要坦白告诉你：
AIP Logic 的 Calculator / Call function 配置：官方文档确认了工具的存在、用途和配置入口 ，但未公开真实界面截图。上面的"截图级步骤"是基于文档描述还原的操作路径
CDS View → Ontology 的完整映射表：Palantir 官方从未公开过完整映射表（这是实施服务的核心价值）。上面给的是基于 AWS 官方博客 和 HyperAuto V2 架构文档 推断的典型形态
Webhook 配置：这部分官方文档非常详尽 ，上面的步骤可以直接对照 Foundry 界面操作

Palantir 官方文档确认了 Blocks 的类型和能力（包括 Loops、Conditionals、Use LLM、Apply action、Execute function 等），但未公开真实界面截图——下面的"路径"是基于官方 Blocks 文档和入门文档还原的操作范式，你可以直接在 AIP Logic / Ontology Manager / Action 配置界面中对照。

一、AIP Logic 多轮 LLM Block 的 Loops 与 Conditionals

1. 先理解 AIP Logic 的"块编排"本质

Palantir 官方明确定义 ：Logic 函数由 Block 组成，每个 Block 接受输入、返回输出，执行一个离散的数据交互。Block 的类型包括：
Use LLM：核心 AI 调用单元（prompt + tools + output）
Apply action：确定性执行 Ontology 编辑
Execute function：调用已有的 TypeScript / Python / 其他 Logic 函数
Transform：纯确定性转换（不消耗 token）
Conditionals：if/else 分支控制
Loops：对集合逐项迭代
Create variable：创建中间变量
最关键的机制：一个 Block 的输出可以作为后续 Block 的输入——这就是多轮编排的基础 。而且 LLM 没有直接工具访问权，它只能"请求"使用工具，工具调用由 AIP Logic 在调用用户的权限范围内执行​ 。

⚠️ 关键边界：即使 Logic 函数包含 Apply action Block，只要不是从 Action 执行，Ontology 就不会被编辑​ 。这意味着你可以在 Debugger 里无限次"dry run"多轮 LLM，而不会真的写坏数据。

2. 多轮 LLM 的标准编排范式

范式 A：串行多 LLM Block（Sequential LLM Chaining）
纯文本
Input: Sales Order Item 对象
  ↓
[Block 1: Use LLM - "信用评估"]
  Prompt: "评估该订单的信用风险，输出 maintain/release 建议"
  Tools: Query objects (读客户历史)
  Output: credit_decision (变量)
  ↓
[Block 2: Create variable - 构造上下文]
  把 Block 1 的 credit_decision + 原始订单属性打包
  ↓
[Block 3: Use LLM - "生成客户沟通文本"]
  Prompt: "基于信用决策，生成给客户的邮件草稿"
  Input: 引用 Block 2 的变量
  Output: email_draft (变量)
  ↓
[Block 4: Apply action - 确定性写回]
  参数映射: credit_decision → Action 参数
            email_draft → Action 参数
  Ontology 编辑: 更新 Sales Order Item 的 credit_status
               创建 Email 对象
范式 B：LLM + Conditionals + 分支 LLM
纯文本
Input: Sales Order Item
  ↓
[Block 1: Use LLM - "分类器"]
  Prompt: "判断该订单属于哪种处理路径: 
           A) 常规订单 → 走快速通道
           B) 高风险订单 → 走信用评估
           C) 异常订单 → 走人工审查"
  Output: route_type (枚举: "A" | "B" | "C")
  ↓
[Conditionals Block]
  If route_type == "A":
    → [Block 2A: Apply action - 直接释放, 无需 LLM]
  If route_type == "B":
    → [Block 2B: Use LLM - "深度信用评估"]
        Prompt: "对该高风险订单做多维度信用分析..."
        Tools: Query objects, Calculator
        Output: decision
    → [Block 3B: Apply action - 按 decision 写回]
  If route_type == "C":
    → [Block 2C: Use LLM - "生成人工审查工单"]
    → [Block 3C: Apply action - 创建 Review Task 对象]
官方文档对 Conditionals 的定义 ："评估一个条件，根据真假执行不同路径，类似传统编程的 if-then-else"。在 then/else 分支里可以定义返回值，也可以嵌套新的 Block。

3. Loops Block 的实战用法

虽然官方 Blocks 文档确认了 Loops 块的存在 ，但未公开其详细 UI 配置。基于 Palantir 的产品逻辑，Loops 的典型用法是：

用法 1：对对象集合逐项 LLM 处理
纯文本
Input: Object Set (如 "所有被信用冻结的 Sales Order Item")
  ↓
[Loops Block]
  Iteration variable: current_item
  Body:
    [Use LLM - "逐项评估"]
      Prompt: "对 current_item 做信用决策"
      Tools: Query objects (current_item 的客户历史)
      Output: decision_for_current
    [Apply action - 写回单个对象]
      参数: current_item 主键 + decision_for_current
  ↓
Output: "处理完成 X 个订单"
用法 2：LLM 自循环（Agentic Loop）

这是更激进的用法——让 LLM 自己决定要不要继续循环：
纯文本
[Use LLM Block - "迭代推理"]
  Prompt: "你需要解决 X 问题。
           如果信息不足，调用 Query objects 获取更多数据后再次推理。
           如果已足够，输出 FINAL_ANSWER。
           最多迭代 5 次。"
  Tools: Query objects, Calculator, Call function
  Output: result
💡 多轮编排的工程要点（来自官方 Compute Usage 文档 ）：
每个 LLM Block 执行消耗 4 compute-seconds
每个 LLM Block 调用工具消耗 8 compute-seconds
多轮编排的成本是线性累加的，避免无意义的多轮循环
4. 调试多轮 LLM

AIP Logic 的 Debugger 会透明展示每一轮 LLM 的 Chain-of-Thought、工具调用、token 使用量​ 。这是多轮编排能落地的关键——你可以看到：
Block 1 的 LLM 看到了什么 prompt、调用了什么工具、输出了什么
变量如何传递到 Block 2
Block 2 的 LLM 如何基于 Block 1 的输出继续推理
二、HyperAuto 针对 I_Material / I_SalesOrder 的字段级映射还原

1. 先校准：Palantir 官方的口径

HyperAuto 官方页面明确 ：Source Explorer 提供引导式界面浏览 ERP/CRM 模块和对象，Automatic Pipeline Generator 自动生成管道并"创建所有的对象类型、属性和关系"。

但 Palantir 从未公开过​ "I_SalesOrder 的哪个字段映射到 Ontology 的哪个属性"这样的完整映射表——这是实施服务的核心价值。下面我基于 SAP 官方 CDS View 定义​ + SAP 社区对 ECC 表→CDS View 的替代关系​ + HyperAuto 的工作机制，给你一套合理的字段级还原。

2. I_SalesOrder 的字段级映射还原

SAP 官方文档确认 I_SalesOrder 的关键字段 ：SalesOrganization、SoldToParty、SalesOrderType、SalesOrderDate、ReferenceSDDocument、OverallSDProcessStatus，主键是 SalesOrder 。

结合 SAP 社区确认的 ECC→CDS 替代关系 ：VBAK → I_SalesDocument（在最新 S/4HANA 中 I_SalesOrder 是 I_SalesDocument 的销售订单专用视图）。

推断的 Ontology 映射：
SAP I_SalesOrder 字段	字段含义	推断的 Ontology 对象.属性
SalesOrder​ (PK)	销售订单号	Sales Order.id
SalesOrganization​	销售组织	Sales Order.sales_org → Link to Sales Org 对象
SoldToParty​	售达方	Sales Order.sold_to_party → Link to Customer 对象
SalesOrderType​	订单类型	Sales Order.order_type (枚举: OR=标准订单)
SalesOrderDate​	订单日期	Sales Order.created_date
OverallSDProcessStatus​	总体处理状态	Sales Order.status
ReferenceSDDocument​	参考单据	Sales Order.reference_doc → Link to 上游单据

配套的 Item 层 CDS（来自 Onibex 的 Sales Order CDS 套件文档 ）：
CDS View	含义	推断的 Ontology 对象
I_SalesOrderItem​	订单行	Sales Order Item
I_SalesOrderPartner​	订单合作伙伴	关系: Sales Order → Customer (Bill-To, Ship-To)
I_SDDocumentProcessFlow​	单据流	关系: Sales Order → Delivery → Billing Document
I_SalesOrderItemPricingElement​	定价元素	Sales Order Item.price_details (嵌入结构)
I_SalesOrderScheduleLine​	计划行	Sales Order Item.schedule_lines (嵌入结构)

3. I_Material 的字段级映射还原

虽然这次搜索没有直接拿到 I_Material 的官方字段清单，但基于 SAP S/4HANA 的标准数据模型，结合 HyperAuto 的工作机制，推断的映射如下：

SAP I_Material / MARA 字段	含义	推断的 Ontology 对象.属性
Material​ (PK)	物料编号	Product.id
MaterialType​ (MTART)	物料类型	Product.type (枚举: FERT=成品, HALB=半成品)
BaseUnitOfMeasure​ (MEINS)	基本计量单位	Product.uom
MaterialDescription​	物料描述	Product.name
GrossWeight / NetWeight​	毛重/净重	Product.physical_attributes (嵌入结构)
Volume​	体积	Product.physical_attributes.volume

配套 CDS（基于 S/4HANA 标准模型）：
I_MaterialStock​ → Product Stock 对象（库存水平）
I_MaterialValuation​ → Product Valuation 对象（估值）
I_ProductPlant​ → Product 与 Plant 的 Link
4. HyperAuto 自动生成的"增值"部分

光有字段映射不够，HyperAuto 的真正价值在于 自动构建的关系​ ：
纯文本
自动生成的 Link Types（以销售订单场景为例）：
  Sales Order → Customer (通过 SoldToParty)
  Sales Order → Sales Organization
  Sales Order → Sales Order Item (1:N)
  Sales Order Item → Material (通过 Material 外键)
  Sales Order Item → Delivery (通过单据流)
  Delivery → Billing Document
这些 Link 是后续 AIP Logic 能让 LLM "顺着关系追溯"的基础——比如 LLM 评估信用冻结时，能沿着 Sales Order Item → Material → Product Stock 查到该物料的库存水平，辅助决策。

5. 写回机制的字段映射

HyperAuto 支持双向集成 。从 Foundry 写回 S/4HANA 时：
通过 BAPI（Remote-enabled Function Module）​ 实现
典型场景：信用冻结释放 → 调用 BAPI 更新 Sales Order 的状态字段
Ontology 中的 Sales Order.credit_status 变更 → 映射到 BAPI 的输入参数
6. 实施时的验证路径

由于 HyperAuto 自动生成的结果是"黑盒"，建议在实施时：
纯文本
1. Data Connection → 查看自动生成的 Sync 配置，确认 CDS View 选择
2. Pipeline Builder → 查看自动管道，确认字段重命名映射
3. Ontology Manager → 导出 Object Type 的 schema，逐项核对属性
4. 写回测试 → 用一个非生产订单验证 BAPI 调用
三、Webhook 在 Action 中用 Function 做条件触发

这是这次搜索材料最硬的一块——Palantir 官方文档把机制讲得非常清楚。

1. 核心机制：Function 返回 undefined 即可不触发

Palantir 官方文档明确 ：

"If you want to use Functions on Objects to map from Action parameters to webhook inputs, you can also conditionally not fire the webhook at all if your function to map inputs returns undefined. For example, WebhookInput | undefined."

这是条件触发的关键——你的映射函数返回 WebhookInput 就触发，返回 undefined 就不触发。

2. Writeback vs Side effect 的事务语义
类型	执行时机	失败可见性	数量限制	典型用途
Writeback​	对象变更前​	用户看到错误	仅 1 个	强一致性写回
Side effect​	对象变更后​	用户可能已看到成功	多个	Best-effort 通知


官方原话 ：Writeback 保证"如果外部系统请求失败，Foundry Ontology 不发生任何变更"——但这仍是"某种程度的事务性"，因为存在边缘情况"外部请求成功但 Ontology 变更失败"。

3. 条件触发的标准实现路径

Step 1: 在 Functions 仓库写一个映射函数
typescript
@Function()
public function buildWebhookInput(
    order: SalesOrder,
    newPriority: string
): WebhookInput | undefined {
    
    // 条件1: 只有高危订单才同步外部系统
    if (order.riskLevel !== "HIGH") {
        return undefined;  // ← 不触发 Webhook
    }
    
    // 条件2: priority 未变化则不触发
    if (order.priority === newPriority) {
        return undefined;
    }
    
    // 条件3: 外部系统只处理特定订单类型
    if (!["OR", "RE"].includes(order.orderType)) {
        return undefined;
    }
    
    // 通过所有条件 → 构造 Webhook 输入，触发
    return {
        priority: newPriority,
        orderId: order.id,
        timestamp: new Date().toISOString()
    };
}
Step 2: 在 Action 的 Logic tab 配置 Webhook
纯文本
1. 导航到 Action → Logic tab → Add new rule → Webhook
2. 选择 Webhook (如 "Modify Ticket Priority")
3. 切换为 Writeback 或 Side effect
4. 在 Input Parameters 配置中选择 "Use a Function"
5. 选择 Step 1 定义的 buildWebhookInput 函数
6. 函数参数映射:
   - order → Action 的 Sales Order 参数
   - newPriority → Action 的 Priority 参数
7. Save
Step 3: 函数返回 undefined 时，该 Webhook 规则被跳过——Action 的其他规则（如 Ontology Edit）仍正常执行。

4. 更复杂的场景：用 External Function 包装 Webhook

官方 External Functions 文档 给出了更高级的模式：

"Wrap a webhook call with custom pre- and post-processing logic"

适用场景：
需要在 Webhook 调用前做复杂数据转换
需要处理 Webhook 响应后再做 Ontology 编辑
需要链式调用多个外部系统
实现路径：
纯文本
1. Data Connection → 创建 REST API Source → 配置 Webhook
2. Functions 仓库 → 导入该 Source
3. 写一个 @OntologyEditFunction:

@OntologyEditFunction()
public async function processOrderWithExternalSystem(
    order: SalesOrder,
    decision: string
): Promise<void> {
    
    // 前置逻辑: 条件判断
    if (order.riskLevel !== "HIGH") return;
    
    // 调用 Webhook
    const webhookResult = await this.mySource.webhooks.modifyPriority({
        priority: decision,
        orderId: order.id
    });
    
    // 后置逻辑: 处理响应
    if (webhookResult.unique_id) {
        // 写回 Ontology
        order.externalRef = webhookResult.unique_id;
    }
    
    // 链式调用第二个外部系统
    if (decision === "ESCALATE") {
        await this.anotherSource.webhooks.createEscalationTicket({
            orderId: order.id
        });
    }
}

4. 创建 Function-backed Action，backend 选择该函数
5. 在 Workshop / Automate 中调用该 Action
5. 生产环境配置范例：条件性信用冻结写回
纯文本
[Scenario: 销售订单信用决策写回 S/4HANA]

Action: "Apply Credit Decision"
  Parameters: 
    - order: Sales Order (对象)
    - decision: String ("MAINTAIN" | "RELEASE")
  
  Rules:
    Rule 1: Webhook (Writeback) - "SAP Credit Block Update"
      Input mapping: Use Function → buildSAPWebhookInput(order, decision)
      函数逻辑:
        if (decision == "MAINTAIN") return undefined;  // 维持冻结无需写回
        if (order.creditBlockType != "AUTO") return undefined;  // 手动冻结不自动处理
        return {
          salesOrderId: order.id,
          action: "RELEASE",
          timestamp: now()
        }
      Result: decision=="RELEASE" 且是自动冻结 → 触发 BAPI 写回
              否则 → 跳过 Webhook，但仍执行 Rule 2
    
    Rule 2: Ontology Edit
      更新 Sales Order.credit_status = decision
      更新 Sales Order.last_decision_time = now()
    
    Rule 3: Webhook (Side effect) - "Notify Risk Team"
      Input mapping: Use Function → buildRiskTeamNotification(order, decision)
      函数逻辑:
        if (order.riskLevel != "CRITICAL") return undefined;  // 仅通知高危
        return {
          orderId: order.id,
          message: `Credit decision: ${decision}`
        }
      Result: 高危订单 → 发送通知; 否则跳过
⚠️ 生产部署的三个关键认知（综合官方文档）：
Function 返回 undefined 是条件不触发的标准机制​
Writeback 保证"外部失败→本体不变"，但反向不保证 ——关键决策用 Writeback
Side effect 可配多个且无序执行——best-effort 通知用 Side effect
🎯 三块拼起来的生产级范式

把上面三块串起来，一个生产就绪的"AI 多轮决策 + 条件写回"全链路：
纯文本
[S/4HANA CDS Views: I_SalesOrder, I_SalesOrderItem, I_Material]
    ↓ [HyperAuto] Source Explorer 浏览 + Automatic Pipeline Generator
    ↓ 自动生成: Object Types + Properties + Link Types
[Foundry Ontology: Sales Order, Sales Order Item, Product, Customer]
    ↓ [AIP Logic 多轮编排]
    ↓   Block 1: Use LLM - 分类路由
    ↓   Conditionals: 
    ↓     if 常规 → Block 2A: Apply action (直接释放)
    ↓     if 高风险 → Block 2B: Use LLM - 深度评估
    ↓                  Tools: Query objects, Calculator, Call function
    ↓                Block 3B: Apply action (按决策写回)
    ↓     if 异常 → Block 2C: Use LLM - 生成审查工单
    ↓   Loops: 对批量订单逐项处理
    ↓ [Logic 函数发布]
[Action: "AI Credit Decision"]
    ↓ [Logic tab 配置]
    ↓   Rule 1: Webhook (Writeback) - "SAP Credit Block Update"
    ↓            Input mapping: Function buildSAPWebhookInput()
    ↓            → 返回 undefined 则不触发
    ↓   Rule 2: Ontology Edit - 更新 Foundry 中 Sales Order 状态
    ↓   Rule 3: Webhook (Side effect) - "Risk Team Notification"
    ↓            Input mapping: Function buildRiskTeamNotification()
    ↓            → 返回 undefined 则跳过
    ↓ [Automate 编排]
    ↓   Condition: Sales Order Item modified + credit_status = BLOCKED
    ↓   Effect: Submit Action "AI Credit Decision"
[SAP S/4HANA 信用状态被条件性更新 + Foundry Ontology 同步刷新 + 选择性通知]
关于"公开资料边界"的最后说明

诚实校准：
AIP Logic 的 Loops/Conditionals 具体 UI：官方确认了块类型的存在和能力 ，但未公开真实界面截图。上面的"配置路径"是基于文档描述还原的操作范式
I_Material / I_SalesOrder 的字段级映射：Palantir 官方从未公开过完整映射表。上面的映射是基于 SAP 官方 CDS 定义 、SAP 社区 ECC→CDS 替代关系 、Onibex 销售订单 CDS 套件 和 HyperAuto 工作机制 的合理推断——真实 POC 中以 HyperAuto 自动生成结果为准
Webhook 条件触发：这部分是官方文档明确支持的机制​ ，上面的代码和配置可以直接对照 Foundry 环境操作

一、k-LLM 哲学与 AIP Logic 中的模型路由

1. 先校准：k-LLM 在官方文档里的真实定位

Palantir 官方 Blocks 文档明确 ：

"The Use LLM block supports any available LLM in the platform, in keeping with Palantir's k-LLM philosophy. To replace the model used across multiple Logic functions at once, you can bulk replace models in Workflow Lineage."

这句话包含两个关键信息：
Use LLM 块可以使用平台内任意可用 LLM——这就是 k-LLM 的"模型不可知"本质
可以通过 Workflow Lineage 批量替换模型——这是平台级的模型管理能力的体现
二手解读文章里提到的"K-LLM 内核自动根据任务属性、数据保密等级、运行表现要求适配最佳模型" ，目前在 AIP Logic 的官方文档中并未发现这样一个全自动的"智能路由器"开关。实际上 k-LLM 的"路由"能力，需要通过架构师在 AIP Logic 中用 Conditionals + 多个 Use LLM 块编排出来。

2. 生产级"模型路由"的三层范式

第一层：平台级模型管理（Workflow Lineage 批量替换）

这是最粗粒度的路由——一次性把所有 Logic 函数里的模型换成另一个​ 。适用场景：
GPT-4 涨价了 → 批量换到 Claude
某个模型下线 → 批量迁移
新模型评测通过 → 批量升级
操作路径：Workflow Lineage → 选中目标模型 → Bulk replace

第二层：单函数内"分类 + 多模型"路由（核心范式）

这是生产环境最常用的路由模式。结合 Conditionals 块 + 多个 Use LLM 块 ：
纯文本
Input: 用户请求 / 业务对象
  ↓
[Block 1: Use LLM - "复杂度分类器"]
  Model: 小模型（如 Llama 8B 本地部署）
  Prompt: "判断该任务的复杂度:
           A) 简单检索/格式化 → 小模型可处理
           B) 中等推理/多步分析 → 中等模型
           C) 高阶逻辑推导/跨域综合 → 强模型"
  Output: complexity_level (枚举)
  ↓
[Conditionals Block]
  ├─ If complexity_level == "A":
  │    ↓
  │    [Block 2A: Use LLM - "轻量处理"]
  │    Model: 本地 Llama / 小参数开源模型
  │    Tools: Query objects（只读）
  │    ↓
  │    [Block 3A: Apply action / Transform]
  │
  ├─ If complexity_level == "B":
  │    ↓
  │    [Block 2B: Use LLM - "标准处理"]
  │    Model: Claude Haiku / GPT-4o-mini
  │    Tools: Query objects, Calculator, Call function
  │    ↓
  │    [Block 3B: Apply action]
  │
  └─ If complexity_level == "C":
       ↓
       [Block 2C: Use LLM - "深度推理"]
       Model: Claude Opus / GPT-4
       Tools: Query objects, Calculator, Call function, Apply actions
       ↓
       [Block 3C: Apply action]
成本视角（这是为什么要路由的核心原因）：
每个 LLM 块执行消耗 4 compute-seconds​
每个 LLM 块调用工具消耗 8 compute-seconds​
如果所有请求都用 GPT-4，成本是 Llama 的 10-50 倍
用"分类器 + 路由"的模式，可以把 70-80% 的简单请求导流到小模型，整体成本下降 60-80%​ 的同时，复杂请求仍由最强模型处理。

第三层：k-LLM Consensus（多模型共识）

这是 Shyam Sankar 在 AIPCon 上演示过的范式 ：同一个 prompt 分发到 K 个 LLM，各自的回答送到 Synthesizer 进行理解、评级、比较，产生最可能的正确答案。

在 AIP Logic 中的实现方式：
纯文本
Input: 关键决策请求（如"是否释放信用冻结"）
  ↓
[Block 1: Use LLM - "GPT-4 视角"]
  Model: GPT-4
  Output: gpt4_decision + gpt4_reasoning
  ↓
[Block 2: Use LLM - "Claude 视角"]  
  Model: Claude Opus
  Output: claude_decision + claude_reasoning
  ↓
[Block 3: Use LLM - "Llama 视角"]
  Model: Llama 70B
  Output: llama_decision + llama_reasoning
  ↓
[Block 4: Use LLM - "Synthesizer 共识器"]
  Model: 任一强模型
  Prompt: "以下是三个模型对该决策的判断:
           GPT-4: {gpt4_decision} - {gpt4_reasoning}
           Claude: {claude_decision} - {claude_reasoning}
           Llama: {llama_decision} - {llama_reasoning}
           请比较三者推理质量，输出最终决策。"
  Output: final_decision
  ↓
[Block 5: Apply action - 写回 Ontology]
💡 这种模式适用于关键决策场景（如信用释放、军事情报研判 、医疗诊断），用多个模型的"交叉验证"降低单一模型的幻觉风险。代价是成本线性乘以 K。

3. 模型路由的工程要点

要点 1：分类器本身要用小模型

分类器的任务是"判断复杂度"，不需要强推理能力。用 Llama 8B 本地部署做分类器，延迟 <100ms，成本接近于零 。

要点 2：安全边界的模型隔离

Palantir 在军事场景中的实践 ：涉密数据用本地部署的 Llama 处理，非涉密数据才上云模型。在 AIP Logic 中可以用 Conditionals 实现：
纯文本
[Conditionals]
  If data_classification == "TOP_SECRET":
    → Use LLM with 本地 Llama（数据不出域）
  Else:
    → Use LLM with GPT-4 / Claude（云端强模型）
要点 3：模型能力的持续评估

k-LLM 哲学的一个核心优势是模型可替换​ 。建议定期：
在 Workflow Lineage 中查看各 Logic 函数的模型使用情况
用 A/B 测试评估新模型的业务指标
通过批量替换升级模型
二、HyperAuto / SAP Connector 针对 S/4HANA 的 CDC 增量同步

1. 先厘清：两种"增量"的本质区别

Palantir 官方文档明确了两套不同的增量机制​ ：

机制	适用对象	增量原理	实时性
APPEND + Incremental Mode​	ERP Table, CDS View, HANA View, BW Content Extractor	基于字段值（时间戳/递增 ID）过滤新行	取决于调度频率
SLT (SAP Landscape Transformation)​	SLT object type	数据库触发器捕获变更 → ODP 队列 → Foundry 拉取	近实时

关键认知：
CDS View 本身不支持 SLT 触发器级 CDC——CDS View 的增量只能用 Multiple fields / Concatenate fields 模式
真正的 CDC（数据库触发器级）必须通过 SAP SLT​ 配合 Foundry Connector 实现
2. 方案一：CDS View 的 APPEND 增量配置（字段级）

适用场景：不需要真正的"变更数据捕获"，只需"增量抽取"

配置路径（基于官方文档 ）：
纯文本
Step 1: Data Connection → + New Source → SAP ERP
        选择 Connection type: Direct 或 Remote (via Gateway)

Step 2: 创建 Batch Sync → + New
        Name: "I_SalesOrder Incremental"
        Target dataset: /sap/exports/i_salesorder
        Schedule: 每 5 分钟 / Cron 表达式
        
Step 3: Transaction type: APPEND  ← 关键！选 APPEND 而非 SNAPSHOT
        
Step 4: SAP Object Type: CDS View
        Object name: I_SalesOrder
        
Step 5: Incremental Mode: Multiple fields
        Incremental Field: "LastChangedDateTime,CreatedDateTime"
        （多个字段用逗号分隔，逻辑为 OR）
        
Step 6: Extras tab（可选）:
        - Filter: 如 "SalesOrganization = 1000"
        - Timestamp: On（添加抓取时间戳和行序号）
        - Drop columns: 敏感字段剔除
Multiple fields 模式的语义​ ：

"Import rows where any of the specified fields is greater than or equal to the largest value already imported."

即：系统记录已抽取的最大字段值，下次同步只拉取字段值 ≥ 该最大值的行。

Concatenate fields 模式​ （适用于日期和时间分两个字段存储的场景）：

"Same as multiple fields, but concatenates field values together rather than combining with OR."

即：把 LastChangedDate + LastChangedTime 拼接成一个字符串再比较。

CDS View 增量的局限性：
只能捕获"插入和新值"，不能捕获"删除"（除非 CDS View 本身有删除标记字段）
不能捕获"历史变更"——如果一行被更新 3 次，增量同步只能拿到最新值，中间的 2 次变更丢失
需要配合 Foundry 管道中的去重逻辑（基于主键）
3. 方案二：SLT 真正的 CDC 配置（触发器级）

适用场景：需要捕获每一笔 INSERT/UPDATE/DELETE，包括中间变更状态

架构原理（官方文档 ）：
纯文本
[SAP S/4HANA 数据库]
    ↓ 数据库触发器（DB Trigger）
[SLT 捕获队列]
    ↓ ODP (Operational Data Provisioning) 
[SLT Server 中的 Queue]
    ↓ 定时轮询（Foundry 侧调度）
[Foundry Dataset]
前置条件​ ：
组件	版本要求
Connector 版本	2.34 (SP34)+ 推荐，使用 ODP via OData
SAP_BASIS	7.50 SP09+（ODP via OData 模式）
DMIS	2011_1_730 SP15+（SLT 侧）
关键 SAP Notes	2854759, 2878969, 3062232, 3023446, 2888122 等

配置路径：
纯文本
Step 1: SAP SLT 侧配置
        - 创建 SLT 配置，指定 Context（Queue Alias）
        - 为要复制的表创建 Mass Transfer ID (MTID)
        - SLT 在源表上创建数据库触发器
        - 初始全量加载到 SLT 队列

Step 2: Data Connection → + New Source → SAP ERP
        Connection type: Remote (via Gateway)
        Enable "Connect via Gateway" 
        Context: 填入 SLT 的 queue alias
        
Step 3: 创建 Batch Sync → + New
        Transaction type: APPEND
        SAP Object Type: SLT  ← 关键！选 SLT 而非 CDS View
        Context: 自动继承 source 配置
        Object name: 选择要抽取的表/对象
        
Step 4: 首次运行 → SLT 执行全量加载
        后续运行 → Foundry 轮询 SLT 队列，只拉取增量
SLT 模式的关键特性​ ：
首抽全量，后续增量：第一次 sync 时 SLT 做 full load，后续 triggers 只抓变化
SLT 队列的清理由 SLT 自己管理——Foundry 不参与
资源密集型：官方警告"Using the Connector with SLT can be resource-intensive"，建议先评审 SLT 的 SAP sizing 文档
DMIS 2018 SP4+ 取消了消费者数量限制——老版本 DMIS 一张表最多注册 4 个消费者
4. CDS View vs SLT：选型决策树
纯文本
需要捕获每一笔变更（含 UPDATE 前后值、DELETE）？
  ├─ Yes → 用 SLT 模式（Transaction type: APPEND, Object Type: SLT）
  └─ No → 只需要"新行/新值"？
        ├─ Yes → 用 CDS View + APPEND + Multiple fields
        │         增量字段选 LastChangedDateTime
        └─ No → 全量快照
              → CDS View + SNAPSHOT
生产环境推荐组合：
纯文本
I_SalesOrder（订单头）
  → CDS View + APPEND + Multiple fields
  → Incremental Field: "LastChangedDateTime"

I_SalesOrderItem（订单行）
  → CDS View + APPEND + Multiple fields  
  → Incremental Field: "LastChangedDateTime"

I_Material（物料主数据，变更少但重要）
  → SLT 模式（真正的 CDC）
  → 捕获每一笔字段级变更

I_MaterialStock（库存，高频变动）
  → SLT 模式
  → 近实时同步到 Foundry
5. HyperAuto 与 CDC 的关系

需要澄清一个常见误解：HyperAuto 的自动管道生成是基于首次全量同步的元数据推导​ 。当后续增量同步运行时：
HyperAuto 生成的管道保持结构不变
新的增量数据流入同一个数据集
Pipeline Builder 中的转换逻辑自动应用于新数据
Ontology 对象实时反映最新状态
如果你的场景需要"HyperAuto 自动生成 + SLT 级 CDC"，目前的路径是：
先通过 SLT 配置近实时同步到 Foundry Dataset
在此基础上使用 HyperAuto / Pipeline Builder 构建管道
Ontology 对象自动获得近实时更新能力
三、External Function 链式调用多个 Webhook 与部分失败处理

1. 官方机制：External Functions 是 Webhook 编排的正确位置

Palantir 官方 External Functions 文档明确 ：

"Chain together multiple external webhook requests and Ontology edits with intermediate processing logic. A single webhook cannot perform a dynamic number of external requests, but this can be accomplished using external Functions."

也就是说：单个 Webhook 本身不支持动态数量的请求编排，必须用 External Function 包一层。

2. 前置配置：将 REST API Source 导入 Function 仓库

Step 1: 在 Source 侧启用代码导入​
纯文本
Data Connection → 选择 REST API Source 
  → Enable code imports 菜单
  → 勾选 "Allow the source to be imported into Code Repositories"
  → Enable exports 菜单
  → 勾选 "Enable exports to the source without Marking validations"
Step 2: 在 Function 仓库导入 Source​
纯文本
Code Repositories → 打开 Functions 仓库
  → Resource imports 面板（左侧）
  → Add → Sources
  → 搜索并选择目标 Source
  → Commit
Step 3: 确认 functions.json 配置​
json
{
  "enableExternalSystems": true
}
提交后系统会自动安装 @foundry/external-systems 包。

3. 链式调用多个 Webhook 的标准范式

基于官方文档的 TypeScript v1 范例 ，链式调用的核心是用 Promise.all 并发执行 + isOk 判断结果：
typescript
import { OntologyEditFunction, isOk } from "@foundry/functions-api";
import { MyDictionarySource } from "@foundry/external-systems/sources";

export class MyFunctions {
    @OntologyEditFunction()
    public async defineWords(words: string[]): Promise<void> {
        
        // 核心：Promise.all 并发调用多个 Webhook
        const results = await Promise.all(words.map(word => 
            MyDictionarySource.webhooks.GetDefinition.call({
                wordToDefine: word
            })
        ));
        
        // 核心：用 isOk 判断每个调用的成功/失败
        results.forEach((result, i) => {
            if (isOk(result)) {
                const output = result.value.output;
                // 处理成功结果...
                output.dictionary_definitions.forEach(...);
            }
            // 失败的 result 在这里被静默跳过
        });
    }
}
4. 生产级"部分失败处理"范式

官方社区明确答复 ："目前不支持在 Webhook 遇到 HTTP 错误码时仍标记为成功"。推荐的范式是：

"wrap the webhook in a typescript function, and create error result ontology objects that can be actioned on later"

即：把 Webhook 调用包在 TypeScript Function 中，创建"错误结果本体对象"供后续处理。

完整生产范例：订单下发多系统
typescript
import { OntologyEditFunction, isOk, isErr } from "@foundry/functions-api";
import { ERP_Source, WMS_Source, TMS_Source } from "@foundry/external-systems/sources";
import { SalesOrder } from "@foundry/ontology-api";

export class OrderFulfillmentFunctions {
    
    @OntologyEditFunction()
    public async fulfillOrder(order: SalesOrder): Promise<void> {
        
        // Step 1: 调用 ERP 释放信用冻结
        const erpResult = await ERP_Source.webhooks.ReleaseCreditBlock.call({
            salesOrderId: order.id,
            action: "RELEASE"
        });
        
        if (isErr(erpResult)) {
            // ERP 调用失败 → 创建错误对象，终止流程
            this.createErrorObject({
                orderId: order.id,
                failedSystem: "ERP",
                errorStage: "CREDIT_RELEASE",
                errorMessage: this.extractError(erpResult),
                retryable: true
            });
            // 不继续执行后续 Webhook
            return;
        }
        
        // Step 2: 并发调用 WMS（仓储）和 TMS（运输）
        const [wmsResult, tmsResult] = await Promise.all([
            WMS_Source.webhooks.CreateOutboundDelivery.call({
                salesOrderId: order.id,
                items: order.items.map(i => ({
                    material: i.materialId,
                    quantity: i.quantity
                }))
            }),
            TMS_Source.webhooks.CreateShipment.call({
                salesOrderId: order.id,
                shipTo: order.shipToAddress
            })
        ]);
        
        // Step 3: 部分失败处理
        const failures = [];
        
        if (isErr(wmsResult)) {
            failures.push({
                system: "WMS",
                error: this.extractError(wmsResult)
            });
        }
        
        if (isErr(tmsResult)) {
            failures.push({
                system: "TMS", 
                error: this.extractError(tmsResult)
            });
        }
        
        // Step 4: 根据失败情况决策
        if (failures.length > 0) {
            // 创建错误对象供后续补偿处理
            this.createErrorObject({
                orderId: order.id,
                failedSystem: failures.map(f => f.system).join(","),
                errorStage: "WAREHOUSE_AND_TRANSPORT",
                errorMessage: JSON.stringify(failures),
                retryable: true
            });
            
            // 部分成功的系统做补偿
            if (isOk(wmsResult) && isErr(tmsResult)) {
                // WMS 成功了但 TMS 失败 → 取消 WMS 的出库单
                await WMS_Source.webhooks.CancelOutboundDelivery.call({
                    salesOrderId: order.id
                });
            }
        } else {
            // 全部成功 → 更新订单状态
            order.status = "FULFILLED";
            order.fulfilledAt = new Date();
        }
        
        // Step 5: 写回 Ontology
        // （@OntologyEditFunction 中对 order 对象的修改会自动写回）
    }
    
    private createErrorObject(errorData: {
        orderId: string,
        failedSystem: string,
        errorStage: string,
        errorMessage: string,
        retryable: boolean
    }): void {
        // 创建一个 "WebhookError" 本体对象
        // 后续可由 Automate 定时扫描这些错误对象并重试
    }
    
    private extractError(result: any): string {
        // 从 Err result 中提取错误信息
        return result.err.message || "Unknown error";
    }
}
5. 补偿事务与重试机制

基于官方社区推荐模式 ，生产环境的部分失败处理应该包含：

模式 A：错误对象 + 定时重试
纯文本
1. External Function 调用多个 Webhook
2. 失败的调用 → 创建 WebhookError 本体对象（含 orderId, failedSystem, retryCount）
3. Automate 定时扫描 WebhookError 对象（如每 5 分钟）
4. 对 retryable=true 且 retryCount < 3 的错误对象
5. 重新调用对应的 External Function 做补偿
模式 B：Saga 补偿
纯文本
Step 1: ERP credit release → Success
Step 2: WMS outbound delivery → Success  
Step 3: TMS shipment → Failed
  ↓ 补偿
Step 3': WMS cancel outbound delivery → 撤销 Step 2
Step 2': ERP re-block credit → 撤销 Step 1
模式 C：Writeback vs Side effect 的分工

Webhook 类型
模式选择
理由
关键写回（信用释放、订单创建）
Writeback​
保证"外部失败→本体不变"
通知类（邮件、IM、审计日志）
Side effect​
Best-effort，失败不影响主流程
6. 与 Action / Automate 的集成

External Function → Function-backed Action：
纯文本
1. 发布上面的 @OntologyEditFunction
2. 创建 Action → Backend 选择 "Function"
3. 选择 fulfillOrder 函数
4. 配置 Action 参数映射：order → Sales Order 对象
5. 在 Workshop 中调用该 Action，或用 Automate 触发
Automate 编排：
纯文本
Condition: Sales Order modified + status = "APPROVED"
Effect: Submit Foundry Action → fulfillOrder
  ↓ 自动链式调用 ERP/WMS/TMS 三个 Webhook
  ↓ 部分失败时创建 WebhookError 对象
  ↓ Automate 定时扫描 WebhookError 并重试
7. 生产环境配置要点

⚠️ 三个关键认知（综合官方文档）：
单个 Webhook 不支持动态数量请求——必须用 External Function 包一层
HTTP 错误码无法配置为"成功"——必须创建错误对象供后续处理
Promise.all 并发 + isOk/isErr 判断是官方推荐范式​
性能与资源：
External Function 中的 Webhook 调用消耗 Foundry compute-seconds
并发调用（Promise.all）比串行快 N 倍，但消耗相同的总 compute
建议在函数中对失败做有限重试（如最多 2 次），避免无限循环消耗资源
🎯 三块拼起来的生产级全链路

把上面三块串起来，一个生产就绪的"多模型智能路由 + SLT 级 CDC + 链式 Webhook 容错"全链路：
纯文本
[S/4HANA 数据库]
    ↓ [SLT 触发器] 捕获每一笔变更
[SLT 队列]
    ↓ [Foundry Connector 2.34+] ODP via OData, 定时轮询
[Foundry Dataset: I_SalesOrder, I_SalesOrderItem, I_MaterialStock]
    ↓ [HyperAuto V2] 自动生成 Ontology
[Foundry Ontology: Sales Order, Sales Order Item, Material, Customer]
    ↓ [AIP Logic - k-LLM 路由范式]
    ↓   Block 1: Use LLM (Llama 8B 本地) - 复杂度分类
    ↓   Conditionals:
    ↓     If 简单 → Block 2A: Use LLM (Llama) - 轻量处理
    ↓     If 中等 → Block 2B: Use LLM (Claude Haiku) - 标准处理  
    ↓     If 复杂 → Block 2C: Use LLM (GPT-4) - 深度推理
    ↓              Tools: Query objects, Calculator, Call function
    ↓   Block 3: Use LLM (Consensus) - k-LLM 多模型共识（关键决策）
    ↓   Block 4: Apply action
    ↓ [Logic 函数发布]
[Action: "AI 订单履约决策"]
    ↓ [Logic tab]
    ↓   Rule 1: Webhook (Writeback) - ERP credit release
    ↓   Rule 2: External Function - fulfillOrder
    ↓            ↓ [链式调用]
    ↓            ↓   ERP_Source.webhooks.ReleaseCreditBlock
    ↓            ↓   Promise.all([
    ↓            ↓     WMS_Source.webhooks.CreateOutboundDelivery,
    ↓            ↓     TMS_Source.webhooks.CreateShipment
    ↓            ↓   ])
    ↓            ↓   部分失败 → 创建 WebhookError 对象
    ↓            ↓   补偿逻辑 → 撤销已成功的调用
    ↓ [Automate 编排]
    ↓   Condition: Sales Order modified + credit_status = BLOCKED
    ↓   Effect: Submit Action "AI 订单履约决策"
    ↓ [Automate 重试编排]  
    ↓   Condition: WebhookError objects where retryable=true
    ↓   Effect: Re-submit fulfillOrder for error.orderId
[SAP S/4HANA 信用状态更新 + WMS 出库单 + TMS 运单 + Foundry Ontology 同步 + 错误对象供重试]
关于"公开资料边界"的最后说明

诚实校准：
k-LLM 的"自动路由"：Palantir 官方确认 Use LLM 块支持任意 LLM 且符合 k-LLM 哲学 ，但全自动的"按复杂度智能路由"开关并未在官方文档中出现。上面给的是基于 Conditionals + 多 Use LLM 块的生产级编排范式
S/4HANA CDC：这部分是官方文档非常详尽的​ ——CDS View 用 APPEND + Multiple fields，真正触发器级 CDC 用 SLT，配置路径可以直接对照操作
链式 Webhook 与部分失败：这也是官方明确支持的机制​ ——External Function + Promise.all + isOk/isErr + 错误对象模式，可以直接用于生产

# 摘录 · Palantir 官方文档解读：如何实现 AI 赋能（代理、逻辑与模型集成）

> **来源**：微信公号本地归档 HTML  
> C:/work/palantir/Palantir官方文档—如何实现AI赋能：代理、逻辑与模型集成.html  
> 原文链接：https://mp.weixin.qq.com/s?__biz=Mzg5NzczNjk4MQ==&mid=2247484154&idx=1&sn=f903ae841b5f82f164db5bd6d39475cb  
> **性质**：作者基于 Palantir 官方文档整理 · 供 07 方案对照 · 非平台一手 HTML  
> **抽取日期**：2026-07-14

---

1 引言

Palantir 人工智能平台（AIP）提供了一套完整的工具链，用于构建、训练和部署大语言模型（LLM）。其核心设计理念在于，将 AI 能力“锚定”在 Palantir 的本体（Ontology）之上——本体作为企业的业务语义层与数据模型中心，不仅描述业务的静态结构，更承载了动态的业务运行逻辑。

AIP 的三大支柱——代理（Agents） 、逻辑（Logic） 与模型集成（Model Integration）——分别对应了AI应用的不同层次：从面向终端用户的交互式智能代理，到可编排、可复用的自动化逻辑单元，再到模型本身的接入与全生命周期管理。三者共同构成了一个从“模型接入”到“逻辑编排”再到“代理交互”的完整AI赋能闭环。

[IMG]
本文将逐一深入解析这三个核心模块，帮助读者理解Palantir如何将AI从概念验证转化为可治理、可审计的业务生产力。

2 代理（Agents）：构建企业级智能交互代理

2.1 什么是 AIP Agent

AIP Agents 是构建在AIP Agent Studio中的交互式智能代理，它们配备企业专属信息和工具，可在平台内部部署，也可通过Ontology SDK和平台API实现外部集成。

AIP Agents 由大语言模型、本体（Ontology）、文档和自定义工具共同驱动。它们可以被集成到各类应用中，实现动态的、上下文感知的读写工作流，帮助用户自动完成任务、减少手动操作。

关键特征：AIP Agents 运行在与企业人力资源相同的安全、治理和审计要求之下——每一次动作都可追溯，每一个决策都可解释。代理运行在企业的私有环境中，专有信息始终受企业控制，不会外泄。

2.2 Agent 的核心概念

理解 AIP Agent 需要掌握以下核心概念：

核心概念说明AIP Agents配备企业专属信息和工具的交互式智能代理应用状态（Application State）提示词中的应用变量，用于定制和控制 LLM 行为，支持动态输入指令与描述编译为 LLM 的系统提示词，教会 LLM 如何使用可用上下文完成任务RAG（检索增强生成）利用外部数据源为 LLM 动态提供相关信息，确保回答基于最新、最相关的数据检索上下文根据用户消息从配置数据源中获取的相关内容，用于生成回答工具（Tools）LLM 可调用的外部功能或 API，用于执行特定操作或获取信息向量嵌入文本的数值化语义表示，用于高效比较和检索相似文本上下文窗口LLM 单次可处理的文本量（以 Token 计），包含系统提示、对话历史和注入信息Agent 即函数Agent 可发布为 Function，在平台任何支持 Function 的地方使用2.3 Agent 的四层成熟度框架

Palantir 推荐采用四层成熟度框架来构建 Agent，逐层提升复杂度与自动化程度：

[IMG]
第1层：临时分析（Ad-hoc Analysis） ——适合刚接触AIP或LLM的用户。通过AIP Threads拖拽文档即可获得LLM驱动的答案。

第2层：任务专用Agent（Task-specific Agent） ——将临时分析升级为可复用的Agent，支持本体（Ontology）、文档或自定义函数上下文，实现更精准的交互。

第3层：Agentic 应用（Agentic Application） ——将Agent集成到Workshop应用（使用AIP Agent组件）或第三方OSDK应用中。

第4层：自动化Agent（Automated Agent） ——将Agent发布为 Function，实现复杂工作流的自主处理。

2.4 Agent 的工具系统

工具是Agent能力边界扩展的关键。AIP Agent Studio提供六种工具类型：

工具类型功能说明Action（动作）执行本体编辑，可配置为自动运行或需用户确认Object Query（对象查询）指定LLM可访问的对象类型和属性，支持过滤、聚合、检视和链接遍历Function（函数）调用任何Foundry函数，包括已发布的AIP Logic函数Update Application Variable（更新应用变量）更新应用状态中配置的变量值Command（命令）触发其他Palantir应用中的操作Request Clarification（请求澄清）暂停执行，向用户请求澄清信息工具支持两种调用模式：

- 提示词工具调用（Prompted Tool Calling）：通过提示词注入工具指令，LLM单次只能调用一个工具。兼容所有工具类型和模型。

- 原生工具调用（Native Tool Calling）：利用支持模型的內建能力直接调用工具，支持并行调用多个工具，速度和性能更优。目前仅支持部分 Palantir 内置模型和特定工具类型。

2.5 Agent 的部署与集成

AIP Agents 可通过多种方式部署：

- 平台内部：直接部署在Palantir平台中使用

- Workshop 应用：通过 AIP Agent 组件嵌入

- OSDK 应用：使用 Ontology SDK（支持 Python/Java/TypeScript）集成

- 第三方应用：通过 Palantir 平台 API 集成到外部应用

3 逻辑（Logic）：无代码的 AI 自动化编排引擎

3.1 什么是 AIP Logic

AIP Logic 是一个无代码开发环境，用于构建、测试和发布由 LLM 驱动的函数。它让应用构建者能够以点选式（point-and-click） 的方式使用 LLM 的强大能力，并依托本体中的数据完成复杂的业务逻辑。

AIP Logic 的核心价值在于：将 AI 能力转化为可复用、可编排、可治理的业务函数，而无需编写复杂的代码或处理 API 调用。

3.2 Logic 的核心概念

核心概念说明Logic 函数接收本体对象或文本字符串等输入，返回数值、对象或本体编辑等输出块（Blocks）Logic 函数的组成单元，可执行本体读写、计算、聚合、调用其他函数或与 LLM 交互评估（Evaluations）发布后配置的测试，用于调试和优化 Logic 函数调试器（Debugger）运行函数时展示 LLM 的链式思维（Chain-of-Thought），便于逐步骤排查3.3 Logic 的工作机制

AIP Logic 函数的工作流程如下：

[IMG]
块（Blocks） 是 Logic 函数的基本构建单元。“Use LLM”块是整个 Logic 的核心，它由提示词、工具和输出三部分构成，支持平台中任何可用的 LLM，体现了 Palantir 的“k-LLM”理念——根据具体用例选择最合适的模型。

一个 AIP Logic 资源由一个或多个 Logic 块组成，运行该资源将依次执行所需的块以达成期望的输出。

3.4 Logic 的应用场景

AIP Logic 可应用于广泛的业务场景：

- 将非结构化输入中的关键信息连接到本体

- 解决调度冲突

- 通过寻找最优分配来优化资产性能

- 应对供应链中断

- 分类和跟进高优先级事件

Logic 函数还可以通过 Automate 实现自动化——本体编辑可被自动应用或暂存供人工审核。

3.5 Logic 的安全与执行模式

AIP Logic 构建在与 Palantir 平台其他部分相同的严格安全模型之上：

- 权限控制：LLM 仅被授予完成任务所必需的最小权限

- 执行模式：支持用户范围执行（默认）和项目范围执行两种模式

4 模型集成：AI 能力的统一接入与管理

4.1 统一模型接口

Palantir 提供统一接口来集成来自不同来源的模型。所有模型都可以通过 Modeling Objectives 应用投入生产并连接到业务应用。

[IMG]
4.2 模型的构成

Palantir 中的模型由两个核心组件构成：

组件说明模型制品（Model Artifacts）训练好的模型文件、参数、权重、容器或凭证模型适配器（Model Adapter）描述 Foundry 如何与模型制品交互的逻辑和环境依赖——包括加载、初始化和执行推理4.3 模型集成方式

Palantir 支持从多种来源集成模型：

集成方式具体来源模型文件pickle、bin、onnx 格式容器化模型Docker 镜像（Flask/Python、Plumber/R、Spring Boot/Java）外部托管模型Vertex AI、Azure ML、OpenAI、SageMaker 等平台内置训练Code Repositories、Jupyter NotebookPalantir 开箱即支持一系列商用和开源语言模型，包括嵌入模型（Embedding Models）。

4.4 自定义模型注册

用户可以通过函数接口（Function Interfaces） 注册和利用自己的大语言模型。这包括：

- 创建 Source 定义 LLM 的 API 端点

- 通过 Webhook 从 TypeScript 函数中调用模型

- 发布函数供整个平台使用

无论是托管在本地、自有云还是经过微调的模型，都可以无缝集成到 Foundry 中。注册后的模型可直接用于 AIP Logic，增强工作流的 AI 能力。

4.5 模型操作化（Operationalization）

模型集成后的全生命周期管理包括：

- 模型开发与集成：通过 Code Repositories 和 Jupyter Notebook 训练，或从外部导入

- 模型评估与管理：提交多个模型候选进行评估、发布和部署（实时或批量）

- 模型操作化：通过 Ontology SDK 和 Platform SDK 在模型中查询函数、对象和 LLM

5 三位一体：代理、逻辑与模型的协同机制

AIP 的三大模块构成了一个有机的整体，其协作关系如下：

[IMG]
各层职责划分如下：

层级模块核心定位关键交付物模型层模型集成AI 能力的统一接入与管理模型适配器、统一接口逻辑层AIP LogicAI 能力的无代码编排与复用Logic 函数、块（Blocks）代理层AIP AgentsAI 能力的交互式封装与交付Agent 实例、工具链应用层Workshop/OSDK/API最终用户界面与集成业务应用
- 模型层负责解决“用什么模型”的问题——通过统一接口接入各类模型，屏蔽底层差异；

- 逻辑层负责解决“如何用模型”的问题——通过无代码方式将模型能力编排为可复用的业务函数；

- 代理层负责解决“谁用模型”的问题——将逻辑和模型封装为面向特定业务场景的智能代理；

- 应用层负责解决“在哪用模型”的问题——将代理嵌入到具体的业务应用界面中。

四层架构共同构成了从 AI 技术能力到业务价值的完整转化链路。

6 总结

Palantir AIP 通过代理（Agents）、逻辑（Logic）与模型集成三大模块，为企业提供了一个完整、安全、可治理的 AI 赋能平台：

模块核心定位关键能力模型集成AI 能力的接入与管理层统一接口接入各类模型，支持自定义模型注册与全生命周期管理AIP LogicAI 能力的编排与复用层无代码构建 LLM 驱动的业务函数，可测试、可调试、可自动化AIP AgentsAI 能力的交互与交付层构建企业专属智能代理，支持多级成熟度和多渠道部署三者共同构建的核心理念可以概括为：让 AI 模型“锚定”在企业的本体（Ontology）之上，在严格的安全与治理框架内，将 AI 能力转化为可复用、可交互、可自动化的业务价值。通过这一架构，企业能够将大语言模型从实验性工具升级为支撑核心业务流程的可信生产力组件。

本文内容基于 Palantir 官方文档（https://www.palantir.com/docs）整理而成。

# AOS Platform 技术架构总览

> **版本**：v1.5 · 2026-07-26 · 重画 §1.1 架构总览，体现 L1-L4 产品分层
> **定位**：AOS（AI Ontology System）平台总技术架构文档，基于代码实现 + 技术方案文档提炼
> **数据来源**：1005 个 Python 后端文件（153,810 行）+ 126 个前端 TS/TSX 文件（31,064 行）+ 570 个测试文件（71,909 行）+ 55 个技术方案 MD 文档

---

## 一、云端分离职责

### 1.1 架构总览

AOS 采用 **四层产品分层 + 核心引擎编排 + 插件化扩展** 的架构。核心原则：

> **产品层做业务编排，核心引擎做流程调度，重计算与外部接入隔离在插件/容器中。**

```
┌─────────────────────────────────────────────────────────────────────┐
│  L1 · 客户端层                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                           │
│  │ Web SPA  │  │ Tauri    │  │ 浏览器    │                           │
│  │ React 18 │  │ Desktop  │  │ 直连      │                           │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                           │
└───────┼──────────────┼──────────────┼──────────────────────────────┘
        │              │              │
        ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  L2 · Core API 编排层 · FastAPI · Python 3.11+                       │
│                                                                      │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────┐ ┌────────┐│
│  │工作台       │ │ AIP 决策    │ │ 本体引擎    │ │数据操作 │ │运维交付 ││
│  │Workshop    │ │ 引擎        │ │Ontology    │ │系统 OS │ │Apollo  ││
│  │Module/     │ │ LLM×Action │ │Object/     │ │Pipeline│ │Hub/    ││
│  │Widget      │ │ ×Evals     │ │Link/Action │ │Dataset │ │Ferry   ││
│  └─────┬──────┘ └─────┬──────┘ └─────┬──────┘ └───┬────┘ └───┬────┘│
│        └──────────────┴──────────────┴────────────┘        │      │
│                          │                                 │      │
│  ┌───────────────────────▼─────────────────────────────────▼────┐ │
│  │  L2.5 · 核心引擎层（Engines & Gateways）                       │ │
│  │  插件注册表 (70 个插件 · 7 大域)                                │ │
│  │  Connector Registry · Funnel Engine · Scheduling Engine       │ │
│  │  LLM Gateway · Evals Engine · Logic Engine · Smart Router     │ │
│  │  Embedding Runtime · Function Engine                          │ │
│  └──┬───────────────┬───────────────────┬────────────────┬──────┘ │
└─────┼───────────────┼───────────────────┼────────────────┼────────┘
      │               │                   │                │
      ▼               ▼                   ▼                ▼
┌─────────────────────────────┐ ┌────────────────────────────────────┐
│  L3 · AOS 自有存储            │ │  L4 · 外部接入层（不在 AOS 包内）     │
│  ┌──────────┐ ┌──────────┐  │ │                                    │
│  │PostgreSQL│ │ MinIO    │  │ │  ┌──────────────────────────────┐  │
│  │ :5433    │ │ S3 :9000 │  │ │  │ 外部数据真相源（只读）           │  │
│  │ 元数据    │ │ 对象存储  │  │ │  │ MySQL · Oracle · SQL Server  │  │
│  └──────────┘ └──────────┘  │ │  │ REST API · GraphQL           │  │
│  ┌──────────┐               │ │  │  ↓ Connector 映射 → 物化      │  │
│  │ Qdrant   │               │ │  └──────────────────────────────┘  │
│  │ (可选)    │               │ │  ┌──────────────────────────────┐  │
│  │ 向量索引  │               │ │  │ AI 推理容器                    │  │
│  └──────────┘               │ │  │ ┌─────────┐ ┌──────────────┐ │  │
│                             │ │  │ │ LiteLLM │ │ Jupyter      │ │  │
│  ※ 本体物化数据均落盘于此      │ │  │ │ 多模型   │ │ Notebook 7   │ │  │
│                             │ │  │ │ 代理     │ │ 交互分析     │ │  │
│                             │ │  │ │ :4001   │ │ :8084/:8888  │ │  │
│                             │ │  │ └─────────┘ └──────────────┘ │  │
│                             │ │  │ ┌─────────┐ ┌──────────────┐ │  │
│                             │ │  │ │ LLM Echo│ │ PaddleOCR    │ │  │
│                             │ │  │ │ :8081   │ │ 文档智能解析  │ │  │
│                             │ │  │ │ Dev Mock│ │ :8082        │ │  │
│                             │ │  │ └─────────┘ └──────────────┘ │  │
│                             │ │  └──────────────────────────────┘  │
└─────────────────────────────┘ └────────────────────────────────────┘

  ※ L3 是 AOS 部署时自带的存储；L4 全部是外部接入——数据源用 Connector 只读映射，
    AI 推理用容器 HTTP 调用。Core API 对两者的调用逻辑完全一致，不区分单机/集群部署。
```

三类客户端的平行对比（内部开发必看）


| **维度**      | **Web SPA**              | **Tauri Desktop**             | **浏览器直连（HTTP直连）**                           |
| ----------- | ------------------------ | ----------------------------- | ------------------------------------------- |
| **核心受众**​   | 业务用户（运营/设计师/产品经理）        | 重度用户（需离线/本地文件处理）              | 开发/运维/第三方集成商/自动化脚本                          |
| **访问路径**​   | 加载前端资源→前端API客户端→Core API | 复用Web SPA资源→前端API客户端→Core API | 直接调用Core API HTTP端点                         |
| **UI渲染**​   | 必须渲染React界面              | 复用Web SPA的React界面             | 无UI渲染，仅返回JSON/纯文本                           |
| **鉴权逻辑**​   | OIDC前端登录（Session/Cookie） | OIDC前端登录（Session/Cookie）      | API Key/Client Credentials/内网IP白名单          |
| **典型场景**​   | 日常工作台操作、数据查看             | 离线编辑、本地素材导入                   | 健康检查、接口调试、ERP对接、自动化部署                       |
| **代码归属**​   | `apps/web/`目录            | `apps/desktop/`目录             | Core API端点（`apps/api/src/routes/`）          |
| **公网暴露**​   | 允许（需鉴权）                  | 允许（需鉴权）                       | 仅允许内网/[localhost](http://localhost)（运维接口除外） |
| **依赖前端状态**​ | 是（依赖前端生成的Session/Token）  | 是（同Web SPA）                   | 否（仅依赖请求头中的鉴权信息）                             |




### 1.2 职责分离矩阵


| 层 | 角色 | 职责 | 技术/产品 | 部署 |
|---|---|---|---|---|
| **L1** | 客户端 | UI 渲染 + 用户交互 | React 18 + TypeScript 5.6 | 浏览器 / Tauri 桌面 |
| **L2** | Core API | 五大产品模块业务编排 + 权限 + 事务 | FastAPI + Pydantic 2 + psycopg 3 | 单进程（可水平扩展） |
| **L2.5** | 核心引擎 | 流程调度、路由、插件管理 | 内嵌引擎层（70 插件 · 7 大域） | Core API 进程内 |
| **L3** | AOS 自有存储 | 元数据 / 对象 / 向量 | PG 16 + MinIO + Qdrant | 随 AOS 部署的独立容器 |
| **L4·数据** | 外部数据真相源 | 客户业务数据库（只读接入） | MySQL / Oracle / SQL Server / REST / GraphQL | 客户机房，Connector 远程只读 |
| **L4·AI** | AI 推理容器 | LLM 调用 / 文档解析 / 交互分析 | LiteLLM + LLM Echo / PaddleOCR / Jupyter Notebook 7 | 独立容器，HTTP 调用 |




### 1.3 独立容器健康探测机制

所有独立容器服务通过统一的探测模式管理：HTTP GET 健康端点 → 返回 `{ok, mode, url, status}` → 超时或不可达时返回降级标记。使用标准库 HTTP（无第三方 SDK 依赖）。

**关键设计**：PaddleOCR / Jupyter Notebook 7 / LiteLLM 不可用时，核心 API 自动降级到 fallback 模式（mock/off），系统不中断。

---



## 二、四大平台层架构



### 2.1 层间关系图

```
                    ┌─────────────────────────────────┐
                    │       工作台 (Workshop)          │
                    │  应用层 · 用户交互入口             │
                    │  Module / Widget / Dashboard     │
                    └────────┬───────────────┬────────┘
                             │               │
                    ┌────────▼──────┐ ┌──────▼─────────┐
                    │ AIP 决策引擎   │ │ 本体·数字孪生   │
                    │ LLM × Action  │ │ Ontology Graph │
                    │ × Evals × Logic│ │ Object/Link/   │
                    └────────┬──────┘ │ Action         │
                             │        └──────┬─────────┘
                             │               │
                    ┌────────▼───────────────▼────────┐
                    │    数据操作系统 (Data OS)         │
                    │  Pipeline · Dataset · Connection │
                    │  Schedule · Build · Lineage      │
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │    运维交付 (Apollo)             │
                    │  Hub/Spoke · Ferry · Release    │
                    └─────────────────────────────────┘
```



### 2.2 数据操作系统（Data OS）

**定位**：整个平台的数据底座，管理数据从采集→清洗→建模→分发的全链路。


| 模块               | 功能            |
| ---------------- | ------------- |
| Pipeline Builder | 可视化 DAG 管道构建  |
| Dataset 管理       | 数据集 CRUD + 预览 |
| Data Connection  | 连接器注册 + 数据接入  |
| Scheduling       | 调度计划 + 增量同步   |
| Build Engine     | 数据构建 + 回写     |
| Data Lineage     | 血缘追踪          |
| Data Health      | 数据质量监控        |


**连接器支持**：


| 类型      | 插件                                          | 数据结构                      |
| ------- | ------------------------------------------- | ------------------------- |
| JDBC    | jdbc-postgres / jdbc-mysql / jdbc-sqlserver | schema → table → column   |
| File    | file-local / file-object-store              | 目录 → 文件                   |
| REST    | rest-generic                                | endpoint → JSON           |
| GraphQL | （规划中：Shopify）                               | query/mutation → response |


> **关键概念**：MySQL、PostgreSQL 外部库、REST API、GraphQL 这些**不属于 AOS 存储层**——它们是 Connector Registry 接入的外部真相源（Source of Truth）。AOS 对它们只读，通过映射→物化将数据投影到 AOS 自有的 PostgreSQL 中。详见 §3.4「外部数据源 → 映射 → 物化」。



### 2.3 AIP 决策引擎（AI Platform）

**定位**：AI 能力层，将 LLM 接入企业决策链路，实现"推理→评估→行动"闭环。

**核心公式**：`AIP = LLM × Ontology × Actions × Evals`


| 模块                | 功能                       |
| ----------------- | ------------------------ |
| LLM Gateway       | 统一 LLM 调用入口（OpenAI 兼容协议） |
| Smart Router      | 智能模型路由 + 熔断 + Fallback   |
| Model Provider    | 41 个 LLM 供应商插件管理         |
| LangGraph Runtime | AIP Logic 可视化逻辑编排运行时     |
| Evals Engine      | 模型评测 + 门控（Gate）          |
| L4 Automation     | L4 级自动化 + 熔断保护           |
| RAG               | 检索增强 + 向量检索              |
| DocIntel          | 文档智能（解析/提取/语义）           |
| Decision Lineage  | 决策谱系 + 审计                |


**三层模型栈**：

```
L1 · 供应商层 (Model Providers)
     41 个插件：OpenAI / Anthropic / DeepSeek / 通义 / 文心 / GLM ...
     ↓
L2 · 路由层 (Smart Router · llm_routing.py)
     智能选模：能力 30% + 上下文 25% + 成本 15% + 安全 20% + 标签 10%
     熔断器：主备热切换 + 指数退避
     ↓
L3 · 网关层 (LLM Gateway · llm_gateway.py)
     统一 OpenAI 兼容 chat/completions 协议
     三级路由：显式模型 → 平台默认 → Agnes 直连 → Mock Fallback
```

**AIP Logic 编排**：

```
用户输入 → [LangGraph Runtime] → LLM 推理 → [Evals Gate] → 通过？
                                    ↓                    ↓ 是
                              [RAG 检索]           [Action 执行]
                                    ↓                    ↓
                              [长期记忆]           [结果回写本体]
```



### 2.4 工作台（Workshop）

**定位**：应用构建层，让非技术用户通过 Module + Widget 配置搭建企业应用。


| 模块           | 功能                   |
| ------------ | -------------------- |
| Module 系统    | 应用模块 CRUD（JSON 配置驱动） |
| Widget 引擎    | 11 种 Widget 组件动态渲染   |
| Canvas 画布    | 可视化拖拽编辑器             |
| Workshop App | 应用列表 + Module 定制     |
| 事件系统         | 事件配置 + 触发器           |


**Module 低代码架构**：

```
Module JSON 配置
{
  "id": "order-management",
  "widgets": [
    { "type": "object-table", "objectType": "Order", ... },
    { "type": "metric-card", "source": "count(Order)", ... },
    { "type": "graph-view", "nodes": [...], ... }
  ]
}
     ↓
WidgetRenderer 组件
     ↓
运行态渲染（从 API 拉数据 → 填充 Widget → 渲染到画布）
```

**11 种 Widget**：


| Widget                     | 用途      |
| -------------------------- | ------- |
| `object-table`             | 对象数据表格  |
| `metric-card`              | KPI 指标卡 |
| `graph-view`               | 关系图谱    |
| `action-form`              | 动作表单    |
| `filter-list`              | 筛选器列表   |
| `buddy-chip`               | AI 助手入口 |
| `chart-bar` / `chart-line` | 图表      |
| `kpi-board`                | KPI 看板  |
| `map-view`                 | 地图视图    |
| `events-stream`            | 事件流     |




### 2.5 本体·数字孪生（Ontology）

**定位**：企业的语义中枢，定义"业务世界里的实体和关系"。

**核心数据结构**：


| 数据                     | 用途                  |
| ---------------------- | ------------------- |
| 对象类型 (Object Type)     | "订单""客户""产品"的类型定义   |
| 对象实例 (Object Instance) | 每个对象的具体数据（JSONB 属性） |
| 链接关系 (Graph Edge)      | 实体间的关系边             |
| 链接类型 (Link Type)       | 关系的定义（基数/方向）        |
| 分支 (Branch)            | 数据的版本分支管理           |
| 分支覆盖层 (Branch Overlay) | 分支上的增量修改            |
| 漏斗状态 (Funnel Status)   | 提案→评审→合并的生命周期       |
| 授权策略 (Authz Tuple)     | 关系型权限控制             |
| Wiki                   | 实体关联的知识文档           |


**四要素**：

```
ObjectType（对象类型）
  │ "订单""客户""产品"的类型定义
  ├── PropertyType（属性类型）
  │     订单.amount / 订单.status / 订单.created_at
  ├── LinkType（链接类型）
  │     订单—包含→订单明细 / 订单—属于→客户
  └── ActionType（动作类型）
        创建订单 / 取消订单 / 确认发货

Funnel（漏斗）── 提案→评审→合并的生命周期管理
  └── 提案 → 评审 → 测试 → 合并 → 发布
```



### 2.6 运维交付（Apollo）

**定位**：确保平台从开发到客户现场的全链路交付能力。


| 模块         | 功能                        |
| ---------- | ------------------------- |
| Hub/Spoke  | 中心仓库 ↔ 边缘节点舰队管理           |
| Ferry 摆渡   | 气隙环境镜像同步（Skopeo + Cosign） |
| Release 通道 | 渐进式发布（canary → stable）    |
| 变更审批       | 变更审批流程                    |
| 配置密钥       | 配置中心 + 密钥引用               |


---



## 三、数据架构



### 3.0 数据流动黄金路径

理解 AOS 数据流向的关键是牢记以下两条路径：

**读路径（查询 Object）**：

```
HTTP Request → API Router（权限校验）→ Service Layer（业务逻辑）
→ Ontology Layer（读取 obj_instance）→ PostgreSQL（返回 JSONB）→ API Response
```

> 查询不经过 Dataset 层——Dataset 仅是 ETL 中间态，物化后的对象直接从 PG 读取。

**写路径（Action / 增量物化）**：

```
HTTP Request（Action）或 Cron Job（增量物化）
→ API Router → Service Layer → Funnel Engine（生成 Changelog）
→ Ontology Layer → PostgreSQL（Upsert obj_instance）
→ （异步）刷新 Search Index / Vector DB
```

> 外部数据源的变更通过 Connector 增量拉取，周期性触发此流程。



### 3.1 存储分工

> **重要**：以下三个是 AOS **自有存储**（随平台部署）。MySQL / 外部数据库不在其中——它们是 Connector Registry 接入的外部数据源，地位类比 PaddleOCR（外部能力接入），详见 §2.2 Data OS 连接器部分。

```
┌──────────────────────────────────────────────────────┐
│                AOS 自有存储全景                         │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ PostgreSQL   │  │ MinIO (S3)   │  │ Qdrant(可选)│ │
│  │ :5433        │  │ :9000        │  │ 向量索引    │ │
│  │              │  │              │  │              │ │
│  │ • 本体元数据  │  │ • 媒体文件    │  │ RAG 嵌入向量  │ │
│  │ • 对象实例    │  │ • 附件       │  │ 语义检索     │ │
│  │ • 图谱关系    │  │ • 文档       │  │              │ │
│  │ • Wiki 内容   │  │ • 图片       │  │              │ │
│  │ • 分支覆盖    │  │ • 导出包     │  │              │ │
│  │ • 授权策略    │  │              │  │              │ │
│  │ • 租户/工作区 │  │ bucket:      │  │              │ │
│  │ • Pipeline   │  │ aos-media    │  │              │ │
│  └──────────────┘  └──────────────┘  └────────────┘ │
│                                                      │
│  ┌──────────────┐                                   │
│  │ 内存缓存      │                                   │
│  │ threading    │                                   │
│  │ .Lock+单例    │                                   │
│  │ LangGraph    │                                   │
│  │ Runtime      │                                   │
│  └──────────────┘                                   │
└──────────────────────────────────────────────────────┘

外部（不在 AOS 环境内）：Connector 只读接入，映射→物化到 PG
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │ MySQL        │  │ REST API     │  │ GraphQL API  │
  │ 企业业务库    │  │ 第三方系统    │  │ Shopify 等   │
  │ (客户自带)    │  │ (客户自带)    │  │ (客户自带)   │
  └──────────────┘  └──────────────┘  └──────────────┘
        ↑ 不在 AOS 内运行
```



### 3.2 PostgreSQL — 主存储

**连接**：psycopg 3，连接池模式

**存储内容**：


| 数据                     | 用途                    |
| ---------------------- | --------------------- |
| 对象类型 (Object Type)     | "订单""客户""产品"的类型定义     |
| 对象实例 (Object Instance) | 每个对象的具体数据（JSONB 属性）   |
| 链接关系 (Graph Edge)      | 实体间的关系边               |
| 链接类型 (Link Type)       | 关系定义（基数/方向）           |
| Wiki 页面 + 版本           | 实体关联的知识文档             |
| 分支 + 覆盖层               | 数据版本管理                |
| 漏斗状态                   | 提案→评审→合并的生命周期         |
| 授权策略                   | 关系型权限控制               |
| Data OS 元数据            | 数据源 / 管道 / 数据集 / 同步任务 |
| 租户/工作区                 | 多组织隔离                 |
| 运维目录                   | 发布管理 / 配置密钥           |




### 3.3 MinIO — 对象存储

**关键设计**：自实现 AWS Signature V4（不依赖 boto3 SDK），支持多端点候选重试。

**存储内容**：


| 类型     | 路径模式                          | 示例                          |
| ------ | ----------------------------- | --------------------------- |
| 媒体文件   | `media/{media_id}/{filename}` | `media/abc123/order_q1.csv` |
| 文档附件   | `docs/{doc_id}/{filename}`    | `docs/def456/report.pdf`    |
| 导出包    | `exports/{export_id}/`        | `exports/ghi789/data.zip`   |
| OCR 结果 | `ocr/{task_id}/output.json`   |                             |




### 3.4 外部数据源 → 映射 → 物化

> **设计基准**：本节对齐 Palantir Foundry Object Storage V2 + Funnel 索引管道的标准做法。



#### 3.4.1 核心理念——映射而非搬迁

AOS 的数据孪生理念是：**外部系统是权威真相源（Source of Truth），AOS 做语义映射与物化，不做数据搬迁。**

完整的数据链路分四层：

```
Layer 0  外部真相源          MySQL / PostgreSQL / REST API / GraphQL / File
         (Source of Truth)   ← 企业现有系统的业务库（核电站ERP / 电商MySQL / 设计公司PDM）
         │
         │  ① Connector 读取（JDBC / REST / GraphQL / File Parser）
         ▼
Layer 1  Dataset 层          AOS 内部的数据集（存储在 PG / MinIO）
         (数据集)             ← 数据进入 AOS 的最基本表示形式
         │                    ← 提供：权限管理 / 模式管理 / 版本控制 / 事务更新
         │
         │  ② Property Mapping（属性映射：哪列 → 哪个属性）
         ▼
Layer 2  Ontology 层          Object Type / Link Type / Action Type
         (本体映射)            ← 按业务语义建模，不是 1:1 复制表
         │                    ← 一个 OT 可由 1~70 个 Dataset 支撑（MDO 多数据源对象）
         │
         │  ③ Funnel 物化（数据灌注到 Object Store）
         ▼
Layer 3  Object Store         PostgreSQL obj_instance 表
         (物化结果)            ← 每个对象实例的最新状态（properties JSONB）
                              ← Action 编辑、查询、关联遍历都在此层完成
```

**关键区别**：

- **Layer 1 Dataset** 是可选的——并非所有外部表都要进 Dataset。只有需要在 Ontology 中建模的业务对象，其底层数据才需要进入 Dataset。
- **Layer 2 Ontology** 是按业务语义建模——302 张 MySQL 表可能只映射出 ~20 个 Object Type（Order / Member / Goods...），其余表可选择只进 Dataset 用于分析，或不进。
- **Layer 3 物化** 是 Foundry OSv2 的标准行为——Object Store 中的数据是外部真相源的物化视图，由 Funnel 管道定期刷新保持新鲜度。



#### 3.4.2 通用性——不限于微商城

这套架构是**通用的**，适用于所有企业数据源场景：


| 企业类型            | 真相源类型                             | Connector                        | 典型 OT 示例                          |
| --------------- | --------------------------------- | -------------------------------- | --------------------------------- |
| 电商平台（微商城/淘宝/京东） | MySQL / REST API                  | jdbc-mysql / rest-sign-hmac      | Order, Member, Goods, Shop        |
| 核电站             | 实时数据库 (PI / eDNA)                 | opc-ua / modbus                  | Reactor, Sensor, Alert, WorkOrder |
| 设计公司            | PDM / PLM（Windchill / TeamCenter） | rest-generic / jdbc-sqlserver    | Drawing, Part, BOM, Change        |
| 跨境电商            | Shopify GraphQL / Amazon SP-API   | graphql / sp-api                 | Product, Order, Fulfillment       |
| 通用企业            | PostgreSQL / SQL Server / Oracle  | jdbc-postgresql / jdbc-sqlserver | Employee, Department, Contract    |
| 文件类             | CSV / Excel / Parquet / JSON      | file-parser                      | 视文件内容动态建模                         |


**AOS 的 Connector 插件体系**（`plugins/connectors/`）已覆盖上述类型：

```
plugins/connectors/
├── jdbc-mysql/          # MySQL（微商城、企业自有系统）
├── jdbc-postgresql/     # PostgreSQL（外部 PG 库）
├── jdbc-sqlserver/      # SQL Server（设计公司 PDM / 企业 ERP）
├── rest-generic/        # 通用 REST API（设计公司 PLM、第三方系统）
├── rest-sign-hmac/      # 淘宝/天猫 REST（HMAC 签名）
├── rest-sign-md5/       # 拼多多 REST（MD5 签名）
├── graphql/             # Shopify GraphQL
├── sp-api/              # Amazon SP-API（AWS4 多区域）
├── file-parser/         # CSV / Excel / JSON / Parquet
└── stream-kafka/        # Kafka 流式（实时传感器 / 日志）
```

每个 Connector 统一通过标准接口接入：`probe()`（连接探测） → `ingest()`（数据采集） → `test_connection()`（健康检查），上层透明。

#### 3.4.3 物化机制（对齐 Foundry Funnel）

Foundry 用 **Funnel 服务** 管理 Dataset → Object Store 的索引管道。AOS 对应实现：

```
                 Funnel 等效管道（AOS 实现）
                 ─────────────────────────────

 ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
 │  更改记录    │ →  │  合并更改    │ →  │   索引      │ →  │  数据灌注    │
 │ Changelog   │    │ Merge       │    │  Index      │    │ Hydration   │
 └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
 计算外部源         合并数据源        转换为 Object        灌注到
 新旧数据差异        + Action 编辑      Store 格式           obj_instance
```


| Funnel 阶段            | Foundry 行为                 | AOS 对应实现                           |
| -------------------- | -------------------------- | ---------------------------------- |
| **更改记录 (Changelog)** | 计算数据源新旧差异，生成 changelog 数据集 | 同步任务表记录每次采集的行数和游标位置                |
| **合并更改 (Merge)**     | 合并数据源数据 + 用户 Action 编辑     | 对象实例表的 JSONB 属性，Action 编辑直接 UPSERT |
| **索引 (Index)**       | 转换为 Object Store 兼容格式      | Property Mapping 配置驱动列→属性转换        |
| **数据灌注 (Hydration)** | 将索引加载到查询节点                 | 对象实例表直接写入（即时灌注，未来可改批处理）            |


**物化的两种模式**（对齐 Foundry OSv2）：


| 模式       | 机制                                | 适用场景              | AOS 状态                                           |
| -------- | --------------------------------- | ----------------- | ------------------------------------------------ |
| **自动传播** | Action 编辑立即写 `obj_instance`，分钟级延迟 | 高频编辑对象（订单审批、工单更新） | ✅ 已实现（Action → UPSERT obj_instance）              |
| **定期重建** | 按计划从 Dataset 全量重建 Object Store    | 低频更新 / 大批量初始化     | 🔄 规划中（`scripts/demo/seed-test-org.sh` 的手动灌入即原型） |




#### 3.4.4 冲突解决——用户编辑 vs 真相源更新

对齐 Foundry 的两种冲突解决策略：


| 策略                  | Foundry 行为                    | AOS 实现                                                       |
| ------------------- | ----------------------------- | ------------------------------------------------------------ |
| **策略 1：用户编辑优先**（默认） | Action 编辑一旦应用，真相源后续更新不覆盖已编辑属性 | `obj_instance.branch_name = 'main'` + Action UPSERT 优先于 Sync |
| **策略 2：最新值优先**      | 比较时间戳，新者胜出                    | `meta_object_type.conflict_strategy` 字段预留，按 OT 粒度配置          |




#### 3.4.5 多数据源对象（MDO）

对齐 Foundry MDO（Multi-Datasource Object）机制：

一个 Object Type 最多可由 **70 个 Dataset** 支撑（Foundry 上限），每个 Dataset 负责映射一组属性子集。

每个属性通过 **属性映射 (Property Mapping)** 定义来源：`来源列名 (backing_column)` + `来源数据集 (backing_dataset)`，标识该属性值从哪个外部表的哪一列获取。

**示例——电商 Order OT 的多数据源支撑**：

```
Object Type: Order
├── Dataset: ds_niushop_order_main (MySQL: ns_order)     → 订单主表属性
│   ├── order_id     → backing_column: order_id          (PK)
│   ├── order_status → backing_column: status
│   └── total_amount → backing_column: total_fee
│
├── Dataset: ds_niushop_order_member (MySQL: ns_member)   → 会员信息属性
│   ├── member_name  → backing_column: nickname
│   └── member_level → backing_column: level_id
│
└── Dataset: ds_aos_edit (Action 编辑)                    → 用户编辑属性
    ├── approval_note → backing_column: _user_edit
    └── risk_flag     → backing_column: _user_edit
```



### 3.5 Qdrant — 向量索引（可选）

**定位**：为 AIP 决策引擎提供语义检索能力，让 AI Agent 能"按意思找内容"而非"按关键词匹配"。

**双后端模式**：


| 后端             | 模式              | 适用场景         |
| -------------- | --------------- | ------------ |
| `local-kv`（默认） | 内存余弦相似度，≤32 文档  | Dev / 小规模原型  |
| `qdrant`（可选）   | 专业向量数据库，支持百万级向量 | 生产 / 大规模 RAG |


**切换**：环境变量 `AOS_VECTOR_BACKEND=local-kv|qdrant`

**支撑的产品功能**：


| 功能                       | 说明                                      |
| ------------------------ | --------------------------------------- |
| **AIP Logic — RAG 检索增强** | Agent 执行逻辑时，从知识库中检索语义相关上下文注入 LLM Prompt |
| **AIP Evals — RAG 评测**   | 专项评测 RAG 管道的召回质量、准确率、幻觉率                |
| **文档智能 — 语义搜索**          | OCR/文档解析后的文本切片转为向量存储，支持跨文档语义检索          |
| **Agent 长期记忆**           | AIP Agent 的长期记忆检索，按语义相似度回忆历史交互          |


**数据流**：

```
文本（文档/Wiki/知识）
    ↓ Embedding 插件（默认 text-embedding-3-small）
向量
    ↓ 存入 Qdrant / local-kv
检索：用户 Query → 向量化 → 余弦相似度 Top-K → 注入 LLM 上下文
```

> **核心价值**：Qdrant 是 AIP 从"关键词搜索"升级到"语义理解"的基础设施。Dev 环境无需 Qdrant 容器，生产环境按需启用。

---



## 四、核心技术栈详解



### 4.1 后端技术栈


| 技术                 | 版本     | 用途      | 设计原则                |
| ------------------ | ------ | ------- | ------------------- |
| **Python**         | 3.11+  | 后端语言    | 全量类型注解              |
| **FastAPI**        | 0.115+ | HTTP 框架 | 异步 + OpenAPI 自动生成   |
| **Pydantic**       | 2.x    | 数据校验    | BaseModel 全量使用      |
| **urllib**         | 标准库    | HTTP 调用 | 禁止第三方 HTTP SDK（军规）  |
| **threading.Lock** | 标准库    | 并发安全    | Singleton + Lock 模式 |


**后端规模**：


| 指标           | 数值            |
| ------------ | ------------- |
| Python 源文件   | **1,005 个**   |
| 代码总行         | **153,810 行** |
| APIRouter 定义 | **473 个**     |
| HTTP 端点      | **3,792 个**   |
| Python class | **2,732 个**   |




### 4.2 前端技术栈


| 技术               | 版本     | 用途                      |
| ---------------- | ------ | ----------------------- |
| **React**        | 18.3.1 | UI 框架                   |
| **React Router** | 6.28.0 | 路由（lazy + Suspense 懒加载） |
| **TypeScript**   | 5.6.3  | 类型安全                    |
| **Vite**         | 5.4.11 | 构建工具                    |
| **Vitest**       | 2.1.8  | 测试框架                    |


**前端规模**：


| 指标        | 数值           |
| --------- | ------------ |
| TS/TSX 文件 | **126 个**    |
| 代码总行      | **31,064 行** |
| 前端路由      | **55 条**     |
| 页面组件      | **59 个**     |
| API 客户端   | 11 个文件       |
| 共享组件      | 20 个文件       |


**状态管理**：无 Redux/Zustan，使用 React Context + 自定义 Hooks + 离线队列

### 4.3 LiteLLM — 多模型代理

**架构**：LiteLLM 作为独立 Docker 容器运行，代理上游所有 LLM 供应商。

```
AOS Core API
    ↓ (OpenAI 兼容 chat/completions)
LiteLLM :4001
    ↓ (master key: aos_dev_litellm_master)
    ├── OpenAI (gpt-4o / gpt-4o-mini)
    ├── Anthropic (claude-3.5-sonnet)
    ├── DeepSeek (deepseek-chat / deepseek-reasoner)
    ├── 通义千问 (qwen-max / qwen-turbo)
    ├── 文心一言 (ernie-bot-4)
    ├── 智谱 GLM (glm-4 / glm-4-flash)
    ├── Moonshot (moonshot-v1)
    ├── ... (41 个供应商)
    └── LLM Echo :8081 (Dev Mock)
```

**Gateway 三级路由策略**：

1. **显式模型优先** — 调用方指定模型时直接路由
2. **平台默认网关** — 按任务类型（chat/embed/vision）分发到 LiteLLM 或 Agnes
3. **Fallback Mock** — 所有路由失败时返回 Mock 响应，保证链路不中断



### 4.4 LLM Echo — Dev Mock

- Dev 环境的假 LLM 后端，端口 `:8081`
- 模拟 OpenAI chat/completions 接口
- 被 LiteLLM 容器作为默认上游
- 确保无真实 API Key 时端到端链路可用



### 4.5 Jupyter Notebook 7 — 嵌入式交互式分析引擎

**定位**：不是独立 BI 工具，是 AOS 内置的轻量级数据分析与算法验证环境——业务用户做数据探索和可视化，开发/算法同学调试 Evals 评测和 RAG 召回脚本。

**双端口架构**：


| 端口      | 用途                      | 可见性          |
| ------- | ----------------------- | ------------ |
| `:8084` | Ticket Facade API（鉴权入口） | Core API 可调用 |
| `:8888` | Jupyter Notebook 7 UI   | 仅内部访问，禁止直接暴露 |


**能力**：

- 数据集探索（读数 / Draft / 探索三 Tab）
- 时序分析
- 甘特图
- KPI 聚合
- NL2Chart（自然语言转图表）
- Evals 评测脚本调试 / RAG 召回验证（开发同学专用）

> 详细交互流程（Ticket 鉴权 → Notebook 会话 → 降级规则）见 [03-部署架构与通信矩阵 §九](03-aos-deployment-architecture.md)。



### 4.6 PaddleOCR — 文档智能解析引擎

**容器**：`aos-dev-ocr`（Dev）/ `aos-prod-ocr`（Prod），端口 `:8082`

**核心定位**：不是单纯文字识别工具，是 AOS 三层文档智能 Pipeline 的执行载体——负责把非结构化文档（PDF / Office / 图片）转换为 AOS 可理解的半结构化数据，是本体建模、RAG 检索、知识图谱构建的前置依赖。

**三层 Pipeline**：

```
原始文档 → PaddleOCR 解析 → 结构化字段提取 → 本体语义映射

Layer 1 · 解析 (Parse)
  PDF → 文本 / OCR → 文本
  解析器：parser-pdf-text / parser-pdf-ocr / parser-office-word / parser-office-sheet

Layer 2 · 提取 (Extract)
  文本 → 结构化字段（实体/金额/日期/地址...）

Layer 3 · 语义 (Semantic)
  结构化字段 → 本体映射 → 知识图谱节点
```

> 详细交互流程（上传 → 解析 → 清洗 → 降级规则）见 [03-部署架构与通信矩阵 §八](03-aos-deployment-architecture.md)。



### 4.7 Smart Router — 智能模型路由

**三引擎协作**：


| 引擎                 | 策略          | 评分维度                                        |
| ------------------ | ----------- | ------------------------------------------- |
| **SmartRouter**    | 按请求特征自动选模型  | 能力 30% + 上下文 25% + 成本 15% + 安全 20% + 标签 10% |
| **ScenarioRouter** | 按任务类型/块级选模  | 分类/摘要/翻译/代码/推理 → 不同模型                       |
| **FailoverEngine** | 熔断器 + 主备热切换 | 熔断阈值 + 指数退避 + 自动恢复                          |


**路由流程**：SmartRouter 评分 → ScenarioRouter 场景过滤 → FailoverEngine 熔断检查 → 返回最优可用模型

---



## 五、插件系统



### 5.1 七大插件域


| 域                 | 插件数    | 清单                                                                                                                          |
| ----------------- | ------ | --------------------------------------------------------------------------------------------------------------------------- |
| **LLM Providers** | 41     | OpenAI / Anthropic / DeepSeek / 通义 / 文心 / GLM / Moonshot / Cohere / Groq / Mistral / xAI / Perplexity / vLLM / Ollama / ... |
| **Connectors**    | 6      | jdbc-postgres / jdbc-mysql / jdbc-sqlserver / rest-generic / file-local / file-object-store                                 |
| **Parsers**       | 5      | pdf-text / pdf-ocr / office-word / office-sheet / text                                                                      |
| **Actions**       | 6      | assign-work-order / cancel-order / close-work-order / confirm-shipment / refund-order / update-wiki-card                    |
| **Widgets**       | 7      | action-form / buddy-chip / filter-list / graph-view / metric-card / object-table / object-view                              |
| **Embeddings**    | 2      | embed-openai-compatible / rerank-cohere                                                                                     |
| **Channels**      | 3      | channel-email / channel-sms / channel-webhook                                                                               |
| **合计**            | **70** |                                                                                                                             |




### 5.2 插件 Manifest 结构

每个插件包含 `manifest.json`：

```json
{
  "id": "deepseek",
  "name": "DeepSeek",
  "nameZh": "深度求索",
  "description": "DeepSeek Chat / Reasoner · OpenAI 兼容",
  "tier": "free",
  "modalities": ["text"],
  "capabilities": ["llm", "chat"],
  "formFamily": "openai_compatible",
  "defaultModels": ["deepseek-chat", "deepseek-reasoner"],
  "litellmPrefix": "deepseek/",
  "version": "0.1.0",
  "configSchema": {
    "type": "object",
    "properties": {
      "apiKeyRef": { "type": "string" },
      "models": { "type": "array" },
      "baseUrl": { "type": "string" }
    }
  }
}
```



### 5.3 插件生命周期

```
磁盘扫描 → manifest.json → 注册表 → 运行时分发
                                ↓
                         probe() → 连接测试
                         ingest() → 数据采集
                         health() → 健康检查
```

> **CI 要求**：所有插件 `manifest.json` 必须在 CI 流水线中进行 Schema 校验，防止无效插件导致 Core API 启动异常。

---



## 六、安全与多租户



### 6.1 认证体系


| 方案          | 实现                      | 用途       |
| ----------- | ----------------------- | -------- |
| **OIDC**    | Keycloak 26（`:8083`）    | 企业 SSO   |
| **OTP**     | 内置                      | 短信/邮箱验证码 |
| **JWT**     | FastAPI 内置              | Token 验签 |
| **OpenFGA** | openfga:v1.8.4（`:8085`） | 关系型授权    |




### 6.2 多租户隔离

**TWA 体系**（Tenant / Workspace / Account）：

```
Organization (组织)
  └── Workspace (工作区)
        └── Project (项目)
              └── Resource (资源)
                    ├── ObjectType
                    ├── Pipeline
                    ├── Dataset
                    └── Module
```

- 持久化：支持 PG 持久化或内存模式
- 每条数据携带 `org_id` + `project_id`，中间件自动注入租户上下文



### 6.3 授权模型

**OpenFGA 关系授权**：

```
定义关系：
  viewer: [user, group]
  editor: [user, group]
  admin: [user, group]

授权元组 (authz_tuple)：
  (principal="alice", relation="editor", object_type="ObjectType", object_id="Order")
  (principal="bob",   relation="viewer", object_type="Dataset",    object_id="sales_q1")
```

**字段级 Marking**：敏感字段可标注安全标签（如 `CONFIDENTIAL`），查询时自动过滤。

> **运维提示**：OpenFGA 授权元组会随业务增长膨胀，需定期清理过期策略，否则关系解析延迟会上升。

---



## 七、部署架构



### 7.1 Dev 环境（Docker Compose）

**文件**：`deploy/dev/docker-compose.yml`（320 行）

**11 个服务**：


| 服务                   | 镜像                       | 端口        | 用途                   | Profile |
| -------------------- | ------------------------ | --------- | -------------------- | ------- |
| `aos-dev-pg`         | postgres:16-alpine       | 5433      | PostgreSQL 元数据       | 默认      |
| `aos-dev-minio`      | minio:RELEASE.2025-04-22 | 9000/9001 | S3 对象存储              | 默认      |
| `aos-dev-minio-init` | minio/mc                 | -         | Bucket 初始化           | 默认      |
| `aos-dev-llm-echo`   | 自构建                      | 8081      | LLM Mock             | 默认      |
| `aos-dev-litellm`    | 自构建                      | 4001      | LLM 代理               | 默认      |
| `aos-dev-ocr`        | 自构建                      | 8082      | OCR 侧边车              | 默认      |
| `aos-dev-analytics`  | 自构建                      | 8084/8888 | 分析运行时                | 默认      |
| `aos-dev-mysql`      | mysql:8.4                | 3307      | ⚠️ 外部数据源模拟（生产中为客户自带） | 默认      |
| `aos-dev-keycloak`   | keycloak:26.0.2          | 8083      | OIDC IdP             | oidc    |
| `aos-dev-openfga`    | openfga:v1.8.4           | 8085/8086 | 授权存储                 | openfga |


> **注意**：Dev 环境的 `aos-dev-mysql` 仅用于模拟客户外部数据库，生产环境中 MySQL 不在 AOS 包内（`# customer brings own DB in prod; not in customer AOS package`）。它是 Connector 的接入对象，不是 AOS 自有存储。



### 7.2 生产部署（Ferry 离线交付）

```
Hub（中心仓库）
  ↓ Ferry 摆渡（Skopeo 镜像同步 + Cosign 签名验证）
Spoke（客户现场）
  ↓ Helm Chart 部署
  ├── AOS Core API
  ├── PostgreSQL
  ├── MinIO
  ├── LiteLLM
  ├── PaddleOCR
  └── Jupyter Notebook 7
```

**关键特性**：

- 支持气隙（air-gapped）环境
- HMAC 签名保证镜像完整性
- Cosign 签名验证防篡改
- 渐进式发布（canary → stable）



### 7.3 桌面应用（Tauri）

**目录**：`apps/desktop/`

- **Tauri 2**：Rust 后端 + WebView 前端
- 复用 Web SPA 全部代码
- 离线运行能力（`lib/offlineQueue.ts` + `lib/offlineStore.ts`）
- 打包脚本：`scripts/pack/`

---



## 八、测试体系



### 8.1 测试规模


| 指标     | 数值                          |
| ------ | --------------------------- |
| 测试文件   | **570 个**                   |
| 测试代码行  | **71,909 行**                |
| 测试/源码比 | **46.7%**                   |
| 当前基线   | **7,550 passed / 0 failed** |




### 8.2 测试框架


| 层   | 框架                      | 用途       |
| --- | ----------------------- | -------- |
| 后端  | pytest 8.0 + httpx 0.27 | API 集成测试 |
| 前端  | Vitest 2.1.8 + jsdom    | 组件单元测试   |
| 端到端 | （手动）                    | 烟雾测试脚本   |




### 8.3 测试模式

每个功能标准 9 用例覆盖：创建 / 列表 / 获取 / 更新 / 删除 / 校验失败 / 404 / 401 / 并发安全

> **合并门槛**：所有新增 Engine 必须包含并发安全测试（验证 Singleton + Lock 模式），否则拒绝合并。

---



## 九、环境变量管理

**117 个** `AOS_` **前缀环境变量**，按功能域分组：


| 前缀                            | 数量  | 用途             |
| ----------------------------- | --- | -------------- |
| `AOS_DATABASE_URL`            | 1   | PostgreSQL 连接串 |
| `AOS_LLM_*` / `AOS_LITELLM_*` | ~15 | LLM 网关配置       |
| `AGNES_*`                     | ~5  | Agnes 大模型配置    |
| `AOS_S3_*` / `MINIO_*`        | ~8  | 对象存储           |
| `AOS_MYSQL_*`                 | ~5  | MySQL 数据源      |
| `AOS_OCR_*`                   | ~4  | OCR 侧边车        |
| `AOS_OIDC_*`                  | ~6  | OIDC 认证        |
| `AOS_FERRY_*`                 | ~14 | Ferry 离线交付     |
| `AOS_OPENFGA_*`               | ~4  | OpenFGA 授权     |
| `AOS_OTP_*`                   | ~3  | OTP 验证码        |
| `AOS_TWA_STORE`               | 1   | 租户持久化模式        |
| `AOS_VECTOR_BACKEND`          | 1   | 向量库后端          |


**加载顺序**：`aos-platform/.env` → `deploy/dev/.env` → `deploy/dev/.secrets.env` → `cwd/.env`

---



## 十、架构设计原则



### 10.1 六大军规


| 军规            | 内容         | 实现验证                                                                              |
| ------------- | ---------- | --------------------------------------------------------------------------------- |
| **R-ARCH-01** | 禁止上游 SDK   | LLM 调用用 urllib（非 openai-python），S3 用自实现 AWS V4（非 boto3），HTTP 用 urllib（非 requests） |
| **R-ARCH-02** | Mock-First | 所有外部依赖（LLM/OCR/S3/MySQL）均有 fallback mock，Dev 无密钥可运行                               |
| **R-ARCH-03** | 重计算隔离      | LLM / PaddleOCR / Jupyter Notebook 7 为独立容器，核心 API 通过 probe 探测                     |
| **R-ARCH-04** | 插件化        | 70 个插件覆盖 7 大域，新能力通过 manifest.json 注册                                              |
| **R-ARCH-05** | 多租户隔离      | TWA 体系 + org_id/project_id + OpenFGA                                              |
| **R-ARCH-06** | 离线交付       | Ferry 支持气隙环境镜像同步                                                                  |




### 10.2 编码模式

- **Engine 模式**：所有核心引擎统一使用 Singleton + threading.Lock 线程安全模式，提供 create/get/list/update/delete 标准 CRUD 接口
- **Router 模式**：所有 HTTP 路由统一使用 FastAPI APIRouter，通过 Depends 注入权限校验
- **Test 模式**：每个功能标准 9 用例（创建/列表/获取/更新/删除/校验失败/404/401/并发安全）



### 10.3 代码组织结构（Coding Map）

为避免业务逻辑泄露到错误的层次，请遵守以下映射关系：


| 如果你想写…            | 应该放在                                        | 绝对禁止                        |
| ----------------- | ------------------------------------------- | --------------------------- |
| **HTTP API 接口**   | `routers/` 目录（APIRouter）                    | 在 Route 里写业务逻辑              |
| **业务逻辑编排**        | `*_engine.py`（Singleton + Lock）             | 在 Engine 里直接调外部 API         |
| **LLM / RAG 调用**  | AIP 层 + LLM Gateway                         | 绕过 Gateway 直接调 SDK          |
| **数据 CRUD**       | Engine → `db.py`（PG）/ `object_store.py`（S3） | 手写裸 SQL（需走统一连接管理）           |
| **外部系统对接**        | `plugins/connectors/`（插件化）                  | 在 Core API 里硬编码 JDBC 连接     |
| **前端状态 / API 调用** | `lib/api/` 层                                | 在 React Component 里直接 fetch |
| **UI 组件**         | `components/` 目录                            | 包含业务逻辑（应只做渲染）               |


> **核心原则**：Core API 是编排层，不是计算层。重计算和 IO 密集型操作必须下沉到独立容器（PaddleOCR / Jupyter Notebook 7）或通过 Plugin 隔离。



### 10.4 关键架构决策（ADR）



#### ADR-001：禁止第三方 SDK（自实现 AWS V4 + HTTP Client）

- **决策**：S3 用自实现 AWS Signature V4（非 boto3），HTTP 用 urllib（非 requests），LLM 用 urllib（非 openai-python）
- **背景**：R-ARCH-01 军规
- **后果**：✅ 消除 GPL/Apache 传染性 License 风险 · ✅ 二进制体积更小 · ❌ 维护成本增加（需跟进行业标准变更）
- **状态**：已冻结。除非 License 政策重大变化，否则不引入第三方 SDK



#### ADR-002：MySQL 等外部库是 Connector 数据源，不是存储层

- **决策**：外部数据库仅通过 Connector Registry 只读接入，不打包进 AOS 部署
- **背景**：客户数据主权要求——AOS 不占有客户业务数据
- **后果**：✅ 客户接受度高（数据不离库）· ✅ 合规风险低 · ❌ 实时性受限（依赖增量物化频率）
- **状态**：核心原则，不可动摇



#### ADR-003：LLM 调用通过 LiteLLM 独立容器代理

- **决策**：LLM 调用经独立容器代理，Core API 不直连模型供应商
- **背景**：需支持 41+ 供应商动态切换、熔断和计量
- **后果**：✅ Core API 无需重启即可切换模型 · ✅ 可在网络层统一流量控制和安全审计 · ❌ 增加网络跳数（~5-10ms 延迟）
- **状态**：有效。高频小模型可考虑下沉 Core API 内联以优化延迟



#### ADR-004：Qdrant 可选，默认 local-kv

- **决策**：Dev 环境默认使用 local-kv 内存向量（≤32 文档），Qdrant 按需启用
- **背景**：降低 Dev 环境部署门槛
- **后果**：✅ `docker-compose up` 即可启动，无需额外容器 · ✅ 小规模场景性能足够 · ❌ 大规模 RAG 必须切换 Qdrant
- **状态**：有效。生产环境强制启用 Qdrant

---



## 附录 A：规模指标汇总


| 维度       | 指标           | 数值             |
| -------- | ------------ | -------------- |
| **后端**   | Python 源文件   | 1,005 个        |
|          | 代码行          | 153,810 行      |
|          | HTTP 端点      | 3,792 个        |
|          | APIRouter    | 473 个          |
|          | Python class | 2,732 个        |
| **前端**   | TS/TSX 文件    | 126 个          |
|          | 代码行          | 31,064 行       |
|          | 路由           | 55 条           |
|          | 页面组件         | 59 个           |
| **测试**   | 测试文件         | 570 个          |
|          | 测试行          | 71,909 行       |
|          | 当前基线         | 7,550 passed   |
| **插件**   | 插件总数         | 70 个           |
|          | LLM 供应商      | 41 个           |
|          | 连接器          | 6 个            |
| **部署**   | Docker 服务    | 11 个           |
|          | 环境变量         | 117 个          |
| **总代码量** | 后端+前端+测试     | **~257,000 行** |


---


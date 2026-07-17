# 09 · Apollo 交付引擎产品方案

## 持续交付操作系统 · Hub-Spoke · Ferry · 产品化 + FDE 双轨

> **文档性质**：对标 Palantir **Apollo** 的产品设计 · 固化为 PRD 子章 · **商业化交付模式专题**  
> **版本**：v1.2.2 · 2026-07-17（Backlog：09a 线框 ✅）  
> **状态**：可直接作为 [03 PRD §3.5 / §3.6](03-对标Palantir-AOS-PRD框架.md) 详稿 · 研发 / 销售 / FDE 素材 · 线框 [09a](09a-Apollo交付引擎产品设计线框图.md)  
> **对标在线 / 白皮书**：  
> · [Apollo Core · Overview](https://www.palantir.com/docs/apollo/core/overview/)（Hub/Spoke · Catalog · Orchestration · Change Management）  
> · [How Apollo works](https://www.palantir.com/docs/apollo/core/how-apollo-works/)（Plan · Constraints · Channel promotion · Recall · Rollback）  
> · [Apollo docs 首页](https://www.palantir.com/docs/apollo/)（Environments · Products · Release Channels · Change Management · Teams）  
> · [Apollo CLI](https://www.palantir.com/docs/apollo/apollo-getting-started/apollo-cli-getting-started/)（Product Release / Manifest / Helm）  
> · [Config overrides](https://www.palantir.com/docs/apollo/managing-entities/set-config-overrides/)  
> · [Maintenance windows](https://www.palantir.com/docs/apollo/apollo-getting-started/introduction-maintenance/)  
> · [Apollo: Powering SaaS…](https://blog.palantir.com/palantir-apollo-powering-saas-where-no-saas-has-gone-before-7be3e565c379)  
> · [Deploying Across Security Domains](https://blog.palantir.com/deploying-across-security-domains-449c786d92c0)（Remote Hub · Bundle · BTS）  
> · 本地深挖：[docs/ref/Palantir-Apollo-深度解析.md](../ref/Palantir-Apollo-深度解析.md)  
> **关联**：[03 §3.5/§3.6](03-对标Palantir-AOS-PRD框架.md) · [05~08 产品层](00-索引.md) · [08 工作台](08-Workshop产品方案.md)（造应用）· 本篇（发软件+发实施资产）

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 中文 | 全文中文；UI 对外称「工作台」，官方对标保留 Workshop |
| 先方案后代码 | 本期交付方案；线框见 [09a](09a-Apollo交付引擎产品设计线框图.md)；HTML Demo 已齐 |
| 照抄官方 | Hub / Spoke / Remote Hub / Bundle / Catalog / Manifest 以官方为准 |
| 商业模式先讲清 | native 软件 ≠ 业务自助；工具产品化 + 内容 FDE 化 |
| 最小变更 | Apollo 深挖从 08 迁出；08 只留「造/发」一句指针 |
| 行业定制不黑盒 | OKF 预制菜 / 模板 **交付给客户**（差异化），非 Palantir 式黑盒行业 Ontology |

---

## 0. 一页读懂：为什么 Apollo 值一个「第四金刚」位

Foundry / AIP / 工作台再强，**发不到客户气隙内网、发出去升级崩了，全是白搭**。

官方把 Apollo 视为 **第三平台**（Gotham + Foundry 之下）：

> *Apollo has been so critical to our success, we consider it to be our third platform.*  
> *…bring our SaaS — and the SaaS economics that come with it — to environments where no SaaS has gone before.*  
> 来源：[Palantir Blog · Apollo](https://blog.palantir.com/palantir-apollo-powering-saas-where-no-saas-has-gone-before-7be3e565c379)

**slogan 产品化口径：Run Anywhere** —— 同一套平台代码：公有云 → 私有云 → 气隙 → 边缘，零停机滚上去。

| 分层 | 管什么 | 不管什么 |
| --- | --- | --- |
| **Kubernetes** | 容器在**本集群**怎么跑 | 跨信任域 / 跨气隙 / 全球舰队 |
| **Apollo** | 同一套软件包怎么从总部发到**几千客户环境且不崩** | 业务 Object 该长什么样（那是 FDE + Ontology） |

---

## 1. 商业化交付模式（先纠认知 · 再谈管道）

### 1.1 认知纠偏：「大客户 native 交付」≠「客户全自助」

| 说法 | 准确含义 |
| --- | --- |
| **native 交付** | 软件是**标准化安装包**，经 Apollo 发到客户私有化环境——**不是**为每个客户定制开发 Java/React |
| **软件能用** | 客户 IT 打开 Pipeline Builder / Ontology Manager / 工作台 / AIP Chat / Apollo Hub |
| **业务能用** | 靠 **FDE（Forward Deployed Engineer）** 驻场，用上述工具**配置** Ontology / Pipeline / Agent / Module |

**商业精髓（老板口径）：**

```text
License（标准化软件 · Apollo native 发）
    +
FDE 人天（业务建模 · 实施资产）
    =
双收费 · PS 倍数的底座
```

### 1.2 产品 vs 实施（两刀切开）

#### 🟢 纯产品化 · Native 交付（客户 IT/业务方可打开）

> 这些是**软件功能本身**，装完就能用；界面权限给客户。

| 层 | 产品组件 | 谁用 | 说明 |
| --- | --- | --- | --- |
| L1 | Data Connection UI · Pipeline Builder | 客户数据工程师 | 初期复杂映射可 FDE 先做，再移交 |
| L1 | Dataset / 文件浏览 | 客户数据工程师 | 纯产品能力 |
| L2 | Ontology Manager（OMA） | 客户业务架构师 | Object/Action/Link 初期常由 FDE 搭 |
| L2 | Funnel 四阶段状态页 | 客户运维 | 监控进度 |
| L2 | Function 编辑器（Code Repo） | 客户数据科学家 | TS / Python |
| L3 | **工作台**（对标 Workshop · 拖 Widget 搭应用） | 客户业务人员 | 业务自助「杀手锏」 |
| L3 | AIP Chat / Assist（业务 Agent） | 客户业务人员 | Agent 配好后可自助对话 |
| OPS | Apollo Hub / Spoke | 客户 IT | 发布 · 升级 · 舰队 |

#### 🟠 内容层 · FDE 实施（初期驻场，再梯度移交）

| 层 | 组件 | FDE 做什么 | 何时移交客户 |
| --- | --- | --- | --- |
| L1 | Pipeline Builder（工具已交付） | 配 Connector、清洗逻辑、Joined 宽表 | Phase 1 后期 → 客户数据团队 |
| L2 | Ontology Manager | 建 Object / Link / Action / Function | Phase 1 中期 → 客户业务架构师 |
| L2 | **OKF 预制菜**（行业定制增强） | **改模板**而非从零（相对纯 Palantir 加速） | **上线即可客户自助** |
| L2 | LLM Wiki | 初始挂载 | **上线即可**业务日常编辑 |
| L3 | 工作台 Module | 首搭（如「跨境选品台」） | Phase 1 → 业务方复制自助 |
| AIP | Logic / Chatbot Studio | 首配 Agent（如「导购 Buddy」） | Phase 1 → Prompt/微调移交 |

#### 🔴 Palantir 常黑盒 · 我们刻意不学的部分

| 资产 | Palantir 常见做法 | 我们 |
| --- | --- | --- |
| 行业 Ontology 模板 | FDE 内部复用，**不交客户** | **OKF 预制菜交付客户**（差异化卖点） |
| 核心 Function 机密段 | 部分长期 FDE 托管 | 可托管，但模板与字段映射尽量产品化 |
| Evals 评测集 + 调优策略 | FDE 攥着，客户只看通过率 | 报表给客户；策略可分期开放 |

### 1.3 核心 FAQ

**Q1：L1/L2/AIP/L3 是不是全部产品化交付？**  
不是全部，是 **「工具产品化 + 内容 FDE 化」** 混合：工具层全部 native；某客户的具体建模内容初期 FDE 配，再梯度移交。

**Q2：Pipeline「现场实施」也给客户吗？**  
- **Builder 界面** → 给客户（native）。  
- **「这个客户 PDF 怎么洗成 Object」的逻辑** → 初期 FDE（+ OKF 加速）→ Phase 1 后期移交；极复杂多源 Join/CDC 可长期托管。

**评审金句：**  
*软件钱照收，FDE 人天还能靠 OKF+Wiki 比纯 Palantir 复制更短、更便宜——Phase 1 后业务方就能自助搭工作台。*

---

## 2. Apollo 官方定位：不是「部署工具」，是持续交付操作系统

### 2.1 定义（综合 Blog + White Paper）

> *Palantir Apollo is a continuous delivery system that powers our software platforms… a layer that sits between our applications and the underlying infrastructure.*  
> 来源：[Apollo Blog](https://blog.palantir.com/palantir-apollo-powering-saas-where-no-saas-has-gone-before-7be3e565c379)

产品化三件事：

| 能力 | 含义 |
| --- | --- |
| **Orchestration** | 哪些 payload（Foundry/AIP/工作台…）跑在哪些环境 |
| **Continuous Delivery** | 一次 build，多环境发布；灰度 / 回滚 |
| **Operations** | 健康检查、自愈、升级管道、舰队观测 |

### 2.2 White Paper 构件名（照抄）

| 官方构件 | 职责 |
| --- | --- |
| **Apollo Hub** | 中央：环境状态 · 提出部署 Plan |
| **Apollo Spoke Control Plane** | 每环境控制面；常坐 K8s 之上（亦支持 container-less） |
| **Product Release Manifest** | 被管软件的元数据框架（尽量**不改业务代码**即可入管） |
| **Apollo Catalog** | 产品/版本/配置目录 |
| **Remote Hub** | 气隙/隔离网内的 Hub；用 **Apollo Bundle** 与 Main Hub 同步 |
| **Bundle / BTS** | 跨安全域软件与元数据投递（物理 / CDS / Binary Transfer Service） |

### 2.3 官方核心概念对照（docs 术语 → 产品话）

> 来源：[Overview](https://www.palantir.com/docs/apollo/core/overview/) · [How Apollo works](https://www.palantir.com/docs/apollo/core/how-apollo-works/)

| 官方术语 | 含义 | 本文落点 |
| --- | --- | --- |
| **Environment** | Hub 或 Spoke 环境；Hub 可管多 Spoke，**也可自管（self-manage）** | OPS-001 |
| **Product** | 可被管理的软件单元（Maven 坐标等标识） | Catalog |
| **Product Release** | 某 Product 的一个版本发布 | Artifact |
| **Release Channel** | 发布订阅轨道；Entity 订「产品+通道」而非固定版本号 | OPS-004 |
| **Entity** | 环境里已安装/托管的 Product 实例 | Spoke 上的运行单元 |
| **Product Catalog** | 可用 Release、通道归属、依赖、DB schema、**是否被 Recall** | Hub Catalog |
| **Environment settings** | 已装 Product、通道订阅、其它约束；变更走 **Change Management** | Hub 环境配置 |
| **Reported State** | Spoke Agent 回报：版本、配置、**Probe**、Telemetry、日志元数据 | OPS-009 |
| **Orchestration Engine** | 据 Catalog + Settings + Reported State **提 Plan**；做通道晋升评判 | Hub 大脑 |
| **Plan** | 一次可执行变更（安装/升级/降级/配变/回滚…） | OPS-002/003 |
| **Constraint** | Plan 执行前置条件（维护窗口、依赖、合规等） | OPS-003 扩展 |
| **Change Management** | 环境设定变更审批 · 必填审批人 · 合规审计 | OPS-009 |
| **Config Override** | 按 Product 版本区间的环境级配置覆盖（Helm values 等） | OPS-005 扩展 |
| **Recall** | 通道健康晋升失败 → **自动召回**该 Release，环境滚离坏版本 | OPS-003/004 |
| **Apollo CLI** | `product-release` 发布 Manifest/Helm 入 Catalog | 发布工程链 |

**官方硬口径（必须写进方案）：**

> *There is no single target state for an Environment… rather than targeting a specific version… defined with a product and a Release Channel.*  
> 来源：[Overview](https://www.palantir.com/docs/apollo/core/overview/)

⟹ 我们对外说「灰度 / 多轨道」时，准确模型是：**订通道，不钉死版本号**；具体版本由编排引擎按约束求解。

### 2.4 官网能力地图 vs 本文覆盖（补缺索引）

| 官网章节（[docs/apollo](https://www.palantir.com/docs/apollo/)） | v1.0 是否够 | v1.1 补法 |
| --- | --- | --- |
| Environments / Hub·Spoke | ✅ | §3 加深 |
| Products / Releases / Versions | △ 只写了 artifact | §2.3 + §4.1 |
| Recalling releases | ❌ | §4.3 |
| Release Channels / Promotion | △ 只有稳定/beta 名 | §4.2 |
| Plans / Constraints | ❌ | §4.1 |
| Change Management / Approvers | △ 并在审计 | §4.5 |
| Config overrides | ❌ | §4.4 |
| Maintenance windows | ❌ | §4.4 |
| Teams / Authorization | ❌ | §4.5 简述 |
| Apollo CLI / Helm Manifest | ❌ | §4.1 |
| Air-gap Bundle / Remote Hub | ✅ | §3.3 |
| Observability（Central + Probe） | △ | §3.2 / §4.1 |

---

## 3. Hub-Spoke 拓扑（Run Anywhere 骨架）

```text
                    ┌─────────────────────────────┐
                    │  总部 / 区域 · Apollo Hub   │
                    │  Artifact Registry/Catalog  │
                    │  L1~L3 软件包               │
                    │  + FDE 实施资产包（OKF 等）  │
                    └──────────┬──────────────────┘
                               │ HTTPS（公网）或 Bundle
               ┌───────────────┼───────────────┐
               ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────────┐
        │ 客户 A    │   │ 客户 B    │   │ 客户 C        │
        │ Spoke     │   │ Spoke     │   │ Spoke + 气隙  │
        │ 公有云    │   │ 私有云     │   │ Ferry/Bundle │
        └──────────┘   └──────────┘   └──────────────┘
```

### 3.1 Hub（总部侧）

| 能力 | 官方对应 | 说明 |
| --- | --- | --- |
| Product Catalog | Catalog | Release · Channel 归属 · 依赖 · schema · Recall 标记 |
| Orchestration Engine | Orchestration Engine | 三输入求解 → 发 Plan；兼通道晋升评判 |
| Release Channel + Promotion | Release Channels | rc→beta→stable… 或自定义；健康达标再晋级 |
| Change Management | Change Management | Environment settings 变更审批 |
| Fleet / Central Observability | Central Observability | Spoke Reported State 汇聚 · 舰队一张玻璃 |
| Artifact / 实施资产 | Catalog + 自定义包 | 软件包 + OPS-008 FDE 资产 |

**编排三输入（官方）：**

```text
Product Catalog（有哪些 Release / 依赖 / 是否 Recall）
        +
Environment Settings（订了哪些 Product+Channel / 约束）
        +
Reported State（Spoke 现在实际跑啥 / Probe 是否绿）
        ↓
Orchestration Engine 提出 Plan（满足全部 Constraint 才下发）
```

### 3.2 Spoke（客户侧）

| 能力 | 官方对应 | 说明 |
| --- | --- | --- |
| Spoke Control Plane + Agent | Spoke Agents | **主动出站轮询** Hub 拉 Plan/制品并执行；回报 Reported State |
| Reported State | Entity Reported State | 部署版本 · 当前配置 · **liveness/readiness Probe** · Telemetry |
| 本地执行 | Helm / K8s（常见）或 Lite 单节点 | 官方文档明确常借 Helm API 改集群；**也可 container-less / Compose** |
| Registry Mirror / 本地缓存 | （气隙/边缘实践） | Bundle/Delta 落地后本地装升 |
| Rollback 配合 | Plan 失败回路 | 执行失败且状态漂移 → Engine 发 **rollback Plan** |

#### 3.2.1 连接模型（安全团队必读 · 写准）

```text
正确：Spoke Agent ──出站 HTTPS──► Hub（轮询拉 Plan / 拉制品 / 上报状态）
错误：Hub ──入站推送──► Spoke（要求客户开放入站端口）
```

| 澄清 | 说明 |
| --- | --- |
| **不是「Hub 常驻推送进程」** | Spoke **主动出站轮询**；边缘/气隙侧 **无需** 给 Hub 开放入站端口 |
| Agent 角色 | 客户环境内的控制面组件：定时 poll → 下载 Plan/Artifact → 本地执行 → 回报 |
| 客户安全应答 | 「你们要不要我们开端口给你们推？」→ **不要**；只需允许 Spoke **出站**访问 Hub（或 Ferry 摆渡） |

> 连接模型：Spoke **主动出站**轮询（官方博客与深挖文一致）。下文凡写「Spoke Agent」均指此 **出站轮询执行器**，勿理解成 Hub 侧常驻推送服务。

### 3.3 气隙：Ferry / Bundle / Remote Hub

官方路径（[Deploying Across Security Domains](https://blog.palantir.com/deploying-across-security-domains-449c786d92c0)）：

1. **Remote Hub** 落在隔离网内，管理网内 Spoke；  
2. 用 **Apollo Bundle** 从 Main Hub 灌 Catalog/镜像/配置（可含 sneakernet）；  
3. 进一步可用 **BTS / CDS** 自动化跨域；物理介质是兜底。

产品叙事可将人工摆渡统称 **Ferry**（加密 U 盘/光盘/专用机）：

```text
Hub 打 Ferry Package（加密+签名）
  → 人工带入气隙
  → Spoke/Remote Hub 校验 → rollout
  → 结果写回 Ferry → 人工带回（可单向）
```

**客户必问应答：** 环科院 / 药企 / 军工「完全断网能发吗」→ **能，走 Ferry/Bundle，不靠常驻 HTTPS。**

---

## 4. Run Anywhere 机制全集（官网对齐 + OPS 映射）

### 4.0 六大机制速查（对外口径保留）

| # | 机制 | 产品含义 | OPS |
| --- | --- | --- | --- |
| 1 | **环境解耦** | 同一 Product 跨云/私有/气隙；差异在 Spoke 适配 | OPS-001/002 |
| 2 | **Delta 增量** | 低带宽 / Ferry U 盘友好 | OPS-006 |
| 3 | **安全升级 + 自动 rollback** | Probe 过再切流；Plan 失败回滚；博客亦述 blue-green / staged | OPS-003 |
| 4 | **多轨道 Channel + 自动晋升/召回** | 订通道不钉版本；健康晋级；失败 **Recall** | OPS-004 |
| 5 | **配置/密钥分离 + Config Override** | 密钥本地注入；版本区间 overrides | OPS-005 |
| 6 | **FDE 实施资产通道** | 模板包走同一管道 | OPS-008 |

Fleet 审计 / Change Management / Probe 遥测 → **OPS-009**。

### 4.1 产品入管：Manifest · Helm · CLI（官网补缺）

官方发布路径（[Apollo CLI](https://www.palantir.com/docs/apollo/apollo-getting-started/apollo-cli-getting-started/)）：

```text
Helm Chart（或其它发行形态）
  → apollo-cli product-release … 生成 / 附带 Manifest
  → 写入 Product Catalog（元数据 + Manifest）
  → 落入某 Release Channel（自动晋升管道或人工 Contributor）
  → Orchestration 按 Environment 订阅发 Plan
```

| 要点 | 说明 |
| --- | --- |
| **Product Release Manifest** | 被管软件的元数据框架；目标：**少改/不改业务代码**即可入 Apollo |
| **Helm** | 公开文档以 Helm chart Entity 为常见形态；排障仍可用 `helm` / `kubectl` |
| **依赖与 schema** | Catalog 可带跨 Product 依赖、支持的 DB schema——编排时当硬约束 |
| **对我们** | L1~L3 平台服务 + OPS-008 资产包都应能「Manifest 化」进 Catalog |

### 4.2 Release Channel 晋升与自动召回（官网补缺）

> [How Apollo works](https://www.palantir.com/docs/apollo/core/how-apollo-works/)：Orchestration Engine **持续**用 Reported State 评估健康晋升条件。

```text
新 Release 进入管道（如 rc）
        ↓ 健康晋升准则通过？
    ┌───是───→ 写入下一 Channel（beta → stable…）
    └───否───→ Automatic Recall：环境滚离该坏版本
```

| 产品化建议频道名 | 用途 |
| --- | --- |
| rc | 回归 / 内部 |
| beta | Pilot / 早期客户 |
| stable | 默认全量 |
| custom | 大客户 Hotfix（如「马帮定制轨」） |

**对外勿说成「人手挑版本号」**——正确说法：环境订阅 **Product + Channel**；引擎在约束内选可部署 Release。

### 4.3 Plan · Constraint · Rollback（官网补缺）

```text
Agent 轮询 Hub
  → Engine 候选 Plan
  → 全部 Constraint 满足？
        是 → 下发执行 → Agent 回报成功/失败
        否 → 等待（如维护窗口未开）/ 拆分 Plan
  → 若失败且环境已偏离执行前状态 → 自动发 Rollback Plan
```

| 约束类型（实践分类） | 示例 |
| --- | --- |
| Product 硬约束 | A 依赖 B≥x；schema migration 顺序 |
| Environment 硬约束 | 节点资源、合规标记、出口管制 |
| 软约束 | **Maintenance window**、业务高峰禁升 |

维护窗口官方能力：Product 与 Environment 均可声明；实体取**交集后的 resolved window** 才允许动作（[Maintenance windows](https://www.palantir.com/docs/apollo/apollo-getting-started/introduction-maintenance/)）。  
→ 并入 **OPS-003** 验收：「升级可绑维护窗口；窗口外不强制升」。

### 4.4 Config Override（官网补缺 · 扩 OPS-005）

> [Config overrides](https://www.palantir.com/docs/apollo/managing-entities/set-config-overrides/)：按 Product **版本区间**声明 override；**没有适用 override 的 Release，Apollo 不会部署**。

| 规则 | 产品含义 |
| --- | --- |
| 版本区间覆盖 | 升/降级时选最精确区间，与升级 Plan **同时**决议，避免配错竞态 |
| 空 override 也可 | 至少声明「支持该 major」才能部署 |
| 与密钥分离叠加 | Override 里是非密钥配置；密钥仍 Spoke 本地 Vault/KMS 注入 |

#### 4.4.1 敏感配置加密（强制 · 对齐 05/06 密钥分离）

| 规则 | 说明 |
| --- | --- |
| **禁止明文** | 数据库密码、API Key、证书私钥、Webhook Secret **不得**以明文写入 Config Override / Manifest / Git |
| **密钥槽** | 配置中只存 **secret ref**（如 `vault:kv/aos/db#password`）；运行时由 Spoke 侧注入 |
| **对接** | **HashiCorp Vault** 或 **客户自有 KMS**（云厂商 KMS / 国密机）；Lite Spoke 可用本机密封文件 + 启动解锁，但仍禁止明文落盘可复制配置 |
| **审计** | 密钥读取事件进 OPS-009；轮换不强制改业务配置文件 |
| **与产品对齐** | 同 05 连接器凭证槽、06 Ontology 外部系统密钥；Apollo 只负责「发非密配置 + 注入点」 |
| Helm | override 注入 chart values；平台可注入 `apollo.*` 环境/实体元数据 |

### 4.5 Change Management · Teams · 授权（官网补缺 · 扩 OPS-009）

官网独立成章：**Change requests · Required approvers · Compliance · Teams · Authorization**。

| 能力 | 做啥 | 我们 |
| --- | --- | --- |
| Change request | 改 Environment settings / 通道订阅等要进审批 | OPS-009 + 交付流程 |
| Required approvers | 生产变更 N 人复核 | 私有化默认开 |
| Teams | 产品责任团队 / 环境责任团队 | FDE vs 客户 IT 权限分离 |
| Audit | Plan 生命周期可追溯 | OPS-009 审计日志 |

#### 4.5.1 紧急发布（P0 故障 · 生产必备）

| 项 | 规则 |
| --- | --- |
| **触发** | 生产 P0（大面积不可用 / 数据写坏风险）由值班 Owner 发起 **Emergency Change** |
| **跳过审批** | 可跳过常规 Required Approvers，**最短路径**下发到指定 Channel/Spoke |
| **事后审计** | 必须自动生成审计单：谁、何时、何制品、何原因；**72h 内**补齐复核签字（OPS-009） |
| **护栏** | 仍须通过 Probe 健康门槛；失败自动 rollback；禁止跳过签名校验 |
| **与常规通道** | 紧急包进入 `hotfix` Channel；事后合并回 `stable` 晋升流水 |

博客侧佐证：自动升级可 **staged / blue-green**，异常则 rollback 并通知责任团队——对应 OPS-003 + OPS-009 通知面。

### 4.6 与 GitOps / 裸 K8s 的官方边界（补一句）

| | 单集群 GitOps (如 Argo) | Apollo |
| --- | --- | --- |
| 收敛目标 | 常钉 Manifest/版本 | **无单一目标态**；订 Channel + 约束求解 |
| 范围 | 一集群 | 跨云 / 气隙 / 舰队产品级依赖 |
| 合规 | 多靠外挂 | Change Management 内建 |

---

## 5. 与 03 §3.5 对齐的 OPS 表（权威）

> **替换** 旧 OPS-001~005 编号语义；详稿以本表 + 架构图为准。

| ID | 描述 | 优先级 | 对标 Apollo |
| --- | --- | --- | --- |
| **OPS-001** | Hub-Spoke 拓扑（Hub 可自管；Remote Hub 管气隙） | P0 | Hub / Spoke / Remote Hub |
| **OPS-002** | 私有化一键部署（Spoke Agent 拉 Plan/artifact） | P0 | Spoke Agent · Plan 执行 |
| **OPS-003** | 安全升级：Probe · 维护窗口 · 自动 rollback ·（可选蓝绿） | P1 | Plan · Constraints · Rollback |
| **OPS-004** | 多轨道 Channel + 健康晋升；失败 **Recall** | P2 | Release Channel · Promotion |
| **OPS-005** | 密钥分离 + **Config Override**（版本区间） | P0 | Secrets · Config overrides |
| **OPS-006** | Delta 增量发布（Ferry / 低带宽必需） | P1 | Delta / opportunistic update |
| **OPS-007** | Ferry / Bundle 气隙摆渡（含 CDS/BTS 路径叙事） | P1 | Bundle · Remote Hub · BTS |
| **OPS-008** | FDE 实施资产发布（OKF / 工作台 Module / Agent → **Asset Bundle**） | **P0 · 行业定制增强** | Catalog 扩展资产 |
| **OPS-009** | 审计 + Reported State/Telemetry + **Change Management** + **紧急发布事后审计** | P0 | Observability · Change Mgmt |
| **OPS-010** | **Lite Spoke**（单节点 Docker/Compose · 无专职 K8s 团队） | P0 · 降准入 | Container-less / Compose |

### 5.1 编号迁移说明（避免研发串号）

| 旧 ID（v1.3） | 旧含义 | 新落点 |
| --- | --- | --- |
| OPS-001 | 私有化一键部署 | **OPS-002** |
| OPS-002 | 滚动升级 + 健康检查 | **OPS-003** |
| OPS-003 | 多租户发布通道 | **OPS-004**（升级为多轨道 Channel） |
| OPS-004 | 配置/密钥管理 | **OPS-005** |
| OPS-005 | 审计日志 | **OPS-009** |
| — | （新增） | OPS-001 Hub-Spoke · OPS-006 Delta · OPS-007 Ferry · OPS-008 实施资产 |

---

## 6. 行业定制增强（相对纯 Apollo/Palantir 复制）

### 6.1 增强 1：OKF + FDE 资产包（OPS-008 · 与 03 OKF 预制菜联动）

Artifact 除 L1~L3 **软件**外，必须支持 **实施内容同发**，否则「FDE 资产同发」逻辑不通。

#### 6.1.1 Asset Bundle 定义

| 包内物 | 说明 | 联动 |
| --- | --- | --- |
| OKF / 行业 Ontology 模板 | Schema · 映射菜谱 | [03 §3.2 OKF](03-对标Palantir-AOS-PRD框架.md) |
| 工作台 Module 模板 | Layout / Widget / 变量骨架 | 08 |
| Agent / Logic / Chatbot 配置 | Prompt · 工具绑定 · Evals 快照 | 07 |
| 版本元数据 | `assetSemVer` · 兼容的 **平台 Release Channel** 区间 | 与 OPS-004 绑定 |

#### 6.1.2 发布与拉取流程

```text
FDE 在 Hub 侧打包 Asset Bundle
  → 上传 Hub Catalog（与软件制品并列）
  → 绑定目标 Release Channel（如 customer-A/stable）
  → Spoke 出站轮询拉到「平台版本 + 绑定资产版本」
  → 自动解压部署（Ontology 导入 / Module 安装 / Agent 注册）
  → Reported State 回报资产版本号
```

| 规则 | 说明 |
| --- | --- |
| **版本同绑** | 平台 Channel 晋升时，绑定的 Asset Bundle 版本一并决议；禁止「平台升了、资产仍指旧 breaking Schema」无校验放行 |
| **大版本护栏** | Object Schema 破坏性变更（新增必填等）→ 资产与平台须经 **Beta Channel** 验证后才能进生产（见 03 高风险护栏） |
| **客户可改** | 解压后允许客户/FDE 微调；微调结果可回传为客户私有 Bundle 版本 |

到客户 Spoke 后：FDE 选型材 → 微调约 20% → 交付（相对从零 Ontology，目标压到 **1–2 月**量级叙事）。

### 6.2 增强 2：Lite Spoke（降准入 · OPS-010）

> **共识场景：** 如马帮等客户 **没有专职 K8s 团队**，不能以「全量多节点 K8s」为唯一准入。

| 档位 | 目标环境 | 能力取舍 |
| --- | --- | --- |
| Full Spoke | 标准 K8s | 全 OPS 能力 · 舰队 / Delta / Ferry 完整 |
| **Lite Spoke** | **单节点 Docker Compose**（或等价容器运行时） | **部署 + 升级 + 出站轮询 + 密钥注入** 保留；舰队视图 / Delta / Ferry **分期**；仍走同一 Catalog 契约 |

#### 6.2.1 Lite Spoke 定义与流程

```text
Hub Catalog（同一套 Product + Asset Bundle）
        │  Spoke 出站轮询（同 Full，无入站）
        ▼
Lite Spoke（单机 Compose）
  · aos-api / 核心服务容器
  · 本地卷（数据与密钥密封）
  · Agent：poll → apply compose/helm-lite → probe → report
```

| 项 | Full Spoke | Lite Spoke |
| --- | --- | --- |
| 编排 | K8s + Helm | Compose / 单节点编排器 |
| 扩缩容 | 多节点 | **单节点**；垂直扩容为主 |
| 气隙 | Ferry/Bundle 完整 | 可先 U 盘装包；自动化 Ferry **P1** |
| 目标客户 | 有平台团队 | **无 K8s 团队的中小/ISV**（马帮类） |
| 升级 | Plan + Probe + rollback | **同契约**；失败回滚到上一 Compose 快照 |

**验收：** 无 K8s 专家的情况下，客户 IT 能按文档完成 Lite Spoke 安装，并能从 Hub 拉到一次平台升级 + 一次 Asset Bundle。

---

## 7. 交付分工总表（产品化组件 × FDE × 移交）

| 层 | 产品化组件（给客户） | FDE 实施内容 | 移交节奏 |
| --- | --- | --- | --- |
| L1 | Data Connection / PB 画布 | 配 Connector / 清洗 / OKF 映射 | Phase 1 → 客户数据团队 |
| L2 | OMA / Funnel 状态 | Object/Link/Action + Wiki 挂载 | Phase 1 → 业务架构师 |
| L2 增强 | OKF 预制菜 / Wiki 双向绑定 | 选行业模板微调（叙事：约 80% 提效） | **上线即自助（核心差异）** |
| L3 | 工作台 / AIP Chat | 首 Module + 首 Agent | Phase 1 → 业务人员复制 |
| OPS | Apollo Hub | 私有化部署 + 升级管道 + 资产包 | 长期 IT 自助 |

### 7.1 梯度移交（与里程碑对齐）

```text
Phase 0：FDE 主导（如 50 SKU）
Phase 1：客户业务方自助抬头（OKF + Wiki 降门槛）
Phase 2：以 native 为主；FDE 转难例/CDC/定制 Channel
```

---

## 8. 与上层产品边界

| 产品 | 职责 | Apollo 职责 |
| --- | --- | --- |
| 05 Pipeline | 造数据管道（工具 + 内容） | 发平台软件；发 Pipeline **模板资产** |
| 06/06b Ontology | 造名词动词 | 发 OMA；发行业模板资产 |
| 07 AIP | 造 Agent / Logic | 发 AIP；发 Agent 模板资产 |
| 08 工作台 | **造** Module / 应用 | **发** Module 与平台；灰度到 Spoke |
| **09 Apollo** | — | 舰队、升级、气隙、密钥注入、实施资产通道 |

**金句（从 08 迁入）：** *工作台造应用，Apollo 发应用；AIP 把决策嵌进应用；FDE 用工具造内容，Apollo 把内容包发到 Spoke。*

---

## 9. Backlog

| 交付物 | 内容 | 状态 |
| --- | --- | --- |
| **09a-Apollo 线框图** | WF-AP-01~07：舰队 / Release / Spoke / Ferry / FDE 资产库 / Change / Config | ✅ [09a](09a-Apollo交付引擎产品设计线框图.md) **v1.0** |
| **HTML Demo** | `apollo-hub` · `apollo-release` · `apollo-spoke` · `apollo-ferry` · `apollo-assets` · `apollo-change-mgmt` · `apollo-config` | ✅ **已齐**（foundry/html v1.6 · 映射见 09a §1.2） |

线框 ID（权威在 09a）：

| ID | 画面 |
| --- | --- |
| WF-AP-01 | Hub 舰队视图（Spoke 健康度 / Probe） |
| WF-AP-02 | Release Channel 晋升管道 + Recall 标记 |
| WF-AP-03 | Spoke / Entity 详情（版本 · Plan · rollback） |
| WF-AP-04 | Ferry / Bundle 向导 |
| WF-AP-05 | FDE 资产包管理（OPS-008） |
| WF-AP-06 | Change Management 审批单（环境设定变更） |
| WF-AP-07 | Config Override / 维护窗口编辑 |
---

## 10. 一致性自检

| 检查项 | 结论 |
| --- | --- |
| 是否把 Apollo 写成「只是私有化安装脚本」？ | **否** · 持续交付 OS + 舰队 |
| 是否钉死目标版本号？ | **否** · 官方：订 Product+Channel，无单一目标态 |
| native = 全自助？ | **否** · 工具 native + 内容 FDE |
| OKF 是否黑盒？ | **否** · 交付客户（vs Palantir 行业模板常不交） |
| Plan / Constraint / Recall / Override 是否写入？ | **是** · §2.3–§4.5（v1.1 补） |
| Change Management 是否只剩「日志」？ | **否** · OPS-009 含审批 + Reported State |
| 工作台发布细节是否仍堆在 08？ | **否** · 深挖在 09；08 仅指针 |
| OPS 编号是否与旧表冲突？ | **有意替换** · 见 §5.1 迁移表 |
| Spoke 是否要求客户开入站？ | **否** · §3.2.1 出站轮询 |
| Lite Spoke / 敏感配置加密 / 紧急发布 / Asset Bundle？ | **是** · §6.2 · §4.4.1 · §4.5.1 · §6.1（v1.2） |

---

## 11. 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-07-15 | 首版：商业双轨 · Hub-Spoke · Ferry · 六机制 · OPS-001~009 · 从 08 迁入 |
| v1.1 | 2026-07-15 | **对照官网补缺**：编排三输入/无目标态 · Plan·Constraint·Probe · Channel 晋升/Recall · Config Override · Change Management · CLI/Helm/Manifest · 能力地图 §2.4 |
| v1.2 | 2026-07-16 | **漏错补强**：Lite Spoke 专节(OPS-010) · Vault/KMS 敏感配置 · 紧急发布 · FDE Asset Bundle 流程 · Spoke 出站轮询澄清 |
| v1.2.1 | 2026-07-17 | Backlog：HTML Demo 与 html v1.6 / T09 对齐为 ✅；09a 线框 Markdown 仍可后补 |
| v1.2.2 | 2026-07-17 | Backlog：09a 线框图 ✅ 已开（WF-AP-01～07 · 对齐官网 Core） |

---

*09 · Apollo · Run Anywhere · 卖软件 + 卖 FDE · 发软件 + 发实施资产*

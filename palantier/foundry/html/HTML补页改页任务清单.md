# HTML 补页 / 改页任务清单

> **版本**：v1.2 · 2026-07-17  
> **施工状态**：**B1–B5 全部完成** · Demo **v1.6.5** · 已统一验收 ✅  
> **目的**：产品方案（含本轮漏错补强）与 `foundry/html` 售前蓝图 **一一拉齐**；本清单为 UI 施工真源，**不遗漏线框 ID + 补强条款**。  
> **对齐母本**：[05a](../../05a-数据集成Connectors-Pipeline-Dataset产品设计线框图.md) · [06a](../../06a-语义本体Ontology-Mapping产品设计线框图.md) · [07a](../../07a-AIP引擎产品设计线框图.md) · [08a](../../08a-Workshop产品设计线框图.md) · [09](../../09-Apollo交付引擎产品方案.md) · [03](../../03-对标Palantir-AOS-PRD框架.md) · [25](../../20_tech/25-LLM-Wiki启示与L2演进补丁.md) · [05/06/06b/07/08](../../00-索引.md)  
> **现状基线**：HTML Demo **v1.6.5** · 见 [README](./README.md)

## 使用的 Rules

| Rule | 本清单如何遵守 |
| --- | --- |
| 先方案后代码 | **先落本清单**；未勾选项不得宣称「HTML 已与产品拉齐」 |
| 最小更改 | 已有页优先 **改页**；仅线框有、Demo 无则 **补页** |
| UI 真源 | 目标态技术方案写 UI 时强制引用本目录页 + 组件区 |
| 中文交付 | 侧栏/文案中文为主；线框 ID 仅文档对照，Demo UI **不展示** WF-* 编号 |

---

## 0. 状态图例与优先级

| 标记 | 含义 |
| --- | --- |
| ✅ 已完成 | 全部施工完毕（补页 18 + 改页 21 + 文档同步），B1–B5 批次于 2026-07-16 落地，后续 v1.2–v1.6 持续增强至 Demo v1.6.5 |

**施工优先级（建议）：**  
**P0** Apollo 全套 + AIP 门控三页 + L1 计划/代理 + Wiki 双向改页  
**P1** 本轮护栏改页（128KB/DLQ/熔断/Selection/幂等…）+ AIP 模型路由 + 管道提案  
**P2** 代码库 / WS-10·11 / 合页增强拆页

---

## 1. 全量对照总表（线框 ID → 文件 → 产品章节）

### 1.1 L3 工作台 · 08a / 08

| 线框 ID | 画面 | 文件（目标） | 类型 | 产品章节 | 备注 |
| --- | --- | --- | --- | --- | --- |
| WF-WS-01 | App / Module 列表 | `workshop.html` | ✅ | 08a §3 · 08 §10 | — |
| WF-WS-02 | Module 画布空态 | `workshop-canvas.html` | ✅ | 08a §4 · 08 Layouts | — |
| WF-WS-03 | Inbox 三联 | `workshop-module.html` | ✅ | 08a §5 · **08 §4.4.1 Selection≤10维** · **§3.x Table>1万行分页** · **Widget Markings** · **事件幂等** | 见 §3.1 |
| WF-WS-04 | 知识图谱 Graph | `workshop-object-view.html` | ✅ | 08a §6 · 08 UI-001 · Wiki 侧栏 | Selection 上限徽标 |
| WF-WS-05 | Action Form + HITL | （合于 `workshop-object-view.html`） | ✅ | 08a §7 · **06b ACT-07 幂等** · ACT-09 Draft 提示 | 可合页；须可见防重复提交 |
| WF-WS-06 | AIP Chat Buddy | `workshop-aip-chat.html` | ✅ | 08a §8 · 07a WF-AIP-09 | Context=Selection；可选链 Lineage |
| WF-WS-07 | 嵌入式 Assist | （合于 `workshop-aip-chat.html`） | ✅ | 08a §9 · 08 UI-005 | — |
| WF-WS-08 | COP 全屏 | `workshop-cop.html` | ✅ | 08a §10 · 08 UI-004 | — |
| WF-WS-09 | 发布入口指针 | `workshop-publish.html` | ✅ | 08a §11 · **09 §全篇** | 链到新建 Apollo 页（非死链） |
| WF-WS-10 | Module interface / Loop | `workshop-module-interface.html` | ✅ | 08 §10 · 08a 可选 | P2 |
| WF-WS-11 | Events 配置面板 | `workshop-events.html` | ✅ | 08 §10 · 08a 可选 | P2；可合入 canvas 配置面板 |

### 1.2 AIP · 07a / 07

| 线框 ID | 画面 | 文件（目标） | 类型 | 产品章节 | 备注 |
| --- | --- | --- | --- | --- | --- |
| WF-AIP-00 | 成熟度楼梯 | `aip-maturity.html` | ✅ | 07a §3 · **07 §5b.3.1 L4 熔断** · **§5b.3.2 模型预热** | L4 态须示熔断/降级 |
| WF-AIP-01a | 模型供应商（接入） | `aip-model-providers.html` | ✅ | 07a §4.1 · T07 · **卡片+类型化表单** | 非 Marketplace |
| WF-AIP-05C | 重能力接入 | `aip-capabilities.html` | ✅ | 07b · 07a §7.4 · T07 §5.3 | Job/Session · 禁沙箱扛 GPU |
| WF-AIP-01b | 模型路由策略 | `aip-model-router.html` | ✅ | 07a §4.2 · 出境/预热/熔断 | 与接入分屏 |
| WF-AIP-02 | Logic 三栏画布 | `aip-logic.html` | ✅ | 07a §5 · **07 §3.5.1 Edits 合并** · ACT-09 Draft | 示多 Logic 合并/Draft 节点 |
| WF-AIP-04 | 工具注册（Logic 侧） | （合于 `aip-tools.html` / logic） | ✅ | 07a §6 附 · 07 AIP-04 | 可合页；补 Wiki Tool 明示 |
| WF-AIP-05 | Chatbot Studio 壳 | `agents.html` | ✅ | 07a §6 · 07 AIP-05 | 对齐命名；侧栏挂「Chatbot Studio」 |
| WF-AIP-05T | Agent 工具六类面板 | `aip-tools.html` | ✅ | 07a §7 · 07 AIP-003 | 重点页已有 |
| WF-AIP-06 | 提案 / Draft 审批台 | `aip-draft-inbox.html` | ✅ | 07a §8 · ACT-09 · **25 Insight Backfill** | 含 InsightBackfill 样例 |
| WF-AIP-07 | Decision Lineage | `aip-decision-lineage.html` | ✅ | 07a §9 · **25 回填节点** | 链末 Insight Backfill |
| WF-AIP-08 | Evals 门控 | `aip-evals.html` | ✅ | 07a §10 · 07 L4 门控 | — |
| WF-AIP-09 | Workshop·Agent 组件 | （合于 `workshop-aip-chat.html`） | ✅ | 07a §11 · 08a WF-WS-06/07 | 交叉引用即可 |

> 07a 无 WF-AIP-03 编号（表内从 02 跳到 04），**不另开页**。

### 1.3 L2 本体 · 06a / 06 / 06b / 03 Wiki

| 线框 ID | 画面 | 文件（目标） | 类型 | 产品章节 | 备注 |
| --- | --- | --- | --- | --- | --- |
| WF-OM-01 | Discover | `ontology.html` | ✅ | 06a §3 · 06 OM-01 | — |
| WF-OM-02 | Object Overview 7 Tab | `ontology-object.html` | ✅ | 06a §4 · 06 §9.1 | Data Tab 链 Funnel |
| WF-OM-03 | Property Editor | `ontology-property.html` | ✅ | 06a §5 | — |
| WF-OM-04 | Link Type | `ontology-link.html` | ✅ | 06a §6 · **06 §6.1 解法B>100万→MDO** · **§6.2 解法C禁高频** | 红线警示 UI |
| WF-OM-05 | Action Type | `ontology-action.html` | ✅ | 06a §7 · **06b ACT-07~10** · Criteria/Effects | 幂等键·软删·Webhook DLQ·Draft Dataset |
| WF-OM-06 | Function Type | `ontology-function.html` | ✅ | 06a §8 · **06b FUNC-03 ≤2GB/60s** | Configuration 示超时/内存 |
| WF-OM-07 | Funnel 四阶段 | `ontology-funnel.html` | ✅ | 06a §9 · 06 §5 | — |
| WF-OM-08 | Branch / 版本 | `ontology-branches.html` | ✅ | 06a §10 · 03 ONT-007 | — |
| WF-OM-09 | 图谱健康度 | `ontology-graph-health.html` | ✅ | 06a §11b · **25** · T06 §7.4 | **v1.6.1 补页** |
| WF-FN-01 | OKF Funnel 映射器 | `funnel.html`（或别名 `okf-funnel.html` 跳转） | ✅ | 05a §10 · 06a §11 · **Constitution** | Lint + 三类条款 |
| （WIKI） | LLM Wiki 活卡片 | `ontology-wiki.html` | ✅ | **03 §3.2.3 WIKI-001~004** · 双向技术定义 | 方向A/B·冲突·受控写回 |
| — | Ontology Funnel 入口别名 | `ontology-funnel.html` | ✅ | 已有 | 与 `funnel.html` 职责：OM-07 vs OKF |

### 1.4 L1 数据集成 · 05a / 05 / 05b

| 线框 ID | 画面 | 文件（目标） | 类型 | 产品章节 | 备注 |
| --- | --- | --- | --- | --- | --- |
| WF-DC-01 | 数据连接首页 | `data-connection.html` | ✅ | 05a · 05 DC-01 | 存储类型标签已有则保留 |
| WF-DC-02 | 新建数据源 | `source-new.html` | ✅ | 05a · **05 P0 文件类型 + P1 JDBC/MySQL** | Connector 卡片示必做集 |
| WF-DC-03 | 数据源详情 | `source-detail.html` | ✅ | 05a · 媒体集同步入口 | — |
| WF-DC-04 | 同步编辑器 | `sync.html` | ✅ | 05a · 跳转 SC-01 | 计划入口可点 |
| WF-DC-04b | 存储路由向导 | `sync-routing.html` | ✅ | 05a · **05 §2.3 / v1.4 小文件&lt;128KB 短路** | 第四选项或脚注 |
| WF-DC-05 | 代理管理 | `data-connection-agents.html` | ✅ | 05a WF-DC-05 · 05 DC-05 | **缺页**（边缘 Agent） |
| WF-PB-01 | 管道列表 | `pipeline-list.html` | ✅ | 05a | — |
| WF-PB-02 | 管道画布 | `pipeline.html` | ✅ | 05a · 三型输入 · 链 PB-03/SC-01 | — |
| WF-PB-03 | Use LLM 节点 | `pipeline-doc-intel.html`（合页可） | ✅ | 05a · 05b · **05 DocIntel 死信 DLQ** | 须有 DLQ 面板 |
| WF-PB-02b | 管道提案/历史 | `pipeline-proposals.html` | ✅ | 05a WF-PB-02b | **缺页** |
| WF-BL-01 | 搭建控制台 | `builds.html` | ✅ | 05a | — |
| WF-SC-01 | 计划编辑器 | `schedules.html` | ✅ | 05a · 05 SC-01 | **缺页** |
| WF-CR-01 | 代码库 IDE | `code-repositories.html` | ✅ | 05a · 05 CR | P2 |
| WF-DS-01 | 数据集预览 | `dataset.html` | ✅ | 05a · **MediaReference 列缩略图** · Draft Dataset 标识（若演示提案） | — |
| WF-DS-02 | 数据集历史 | （合于 `dataset.html` History Tab） | ✅ | 05a DS-02 | 确认有 History 标签示意 |
| WF-MS-01 | 媒体集浏览器 | `media-sets.html` | ✅ | 05a · 05b | — |
| WF-LN-01 | 数据沿袭 | `lineage.html` | ✅ | 05a · DLQ/失败边可见（可选） | 与 DocIntel 死信呼应 |
| WF-DH-01 | 数据健康 | `health.html` | ✅ | 05a · DocIntel/Webhook 死信计数 | — |
| WF-FN-01 | OKF 映射 | `funnel.html` | ✅ | 见 1.3 | — |

### 1.5 Apollo 交付 · 09（09a 线框待开 · HTML 仍按 §9 编号落地）

| 线框 ID | 画面 | 文件（目标） | 类型 | 产品章节 | 备注 |
| --- | --- | --- | --- | --- | --- |
| WF-AP-01 | Hub 舰队视图 | `apollo-hub.html` | ✅ | 09 §3 · §9 · OPS-009 Probe | **整组缺页** |
| WF-AP-02 | Release Channel + Recall | `apollo-release.html` | ✅ | 09 §4.2 · OPS-004 · **§4.5.1 紧急发布/hotfix** | 含紧急通道徽标 |
| WF-AP-03 | Spoke / Entity 详情 | `apollo-spoke.html` | ✅ | 09 §3.2 · **§3.2.1 出站轮询** · Plan/Rollback · **OPS-010 Lite Spoke** | Full vs Lite 切换示意 |
| WF-AP-04 | Ferry / Bundle 向导 | `apollo-ferry.html` | ✅ | 09 §3.3 · 气隙 | — |
| WF-AP-05 | FDE Asset Bundle | `apollo-assets.html` | ✅ | 09 §6.1 · OPS-008 · **03 FDE 资产版本** | 平台 Channel 同绑 |
| WF-AP-06 | Change Management 审批 | `apollo-change-mgmt.html` | ✅ | 09 §4.5 · OPS-009 | — |
| WF-AP-07 | Config Override / 维护窗 | `apollo-config.html` | ✅ | 09 §4.4 · **§4.4.1 Vault/KMS 禁明文** | 密钥引用非明文 |
| （指针） | 工作台发布入口 | `workshop-publish.html` | ✅ | 08a WF-WS-09 | 链 AP-02/05 |

> **09a 线框文档**本身仍「待开」——HTML 可按上表先做；开 09a 时与本表 ID **不得改号**。

### 1.6 壳与导航（随补页强制改）

| 文件 | 类型 | 对齐 | 改什么 |
| --- | --- | --- | --- |
| `index.html` | 📄✅ | 03 使用优先 · 全模块入口 | 侧栏增 **Apollo** 组；AIP 下挂路由/Draft/Lineage/Evals；数据下挂计划/代理 |
| `README.md` | 📄✅ | 本清单 · 05a~09 | 全量映射表升级至 v1.6+；去掉「仅 08a」片面表述 |
| `assets/demo.css` / 公共壳 | 📄✅ | 视觉一致 | 新页复用 Token；必要时加「护栏徽标」通用样式 |

---

## 2. 补页任务清单（✅ 仅新建）

按建议施工序；每项含 **文件名 + 应对齐产品章节 + 验收要点**。

### P0 · 必须补

| # | 新建文件 | 线框 | 产品章节 | 验收要点（最小可演示） |
| --- | --- | --- | --- | --- |
| N01 | `apollo-hub.html` | WF-AP-01 | 09 §3 · §9 | Spoke 卡片健康度 / Probe；点进 Spoke 详情 |
| N02 | `apollo-release.html` | WF-AP-02 | 09 §4.2 · §4.5.1 | rc→beta→stable 管道；Recall；**hotfix/紧急发布**标记 |
| N03 | `apollo-spoke.html` | WF-AP-03 | 09 §3.2.1 · §6.2 OPS-010 | **出站轮询**文案；Full / **Lite Spoke** 形态；Plan · Rollback |
| N04 | `apollo-ferry.html` | WF-AP-04 | 09 §3.3 | Bundle 导出/导入向导步骤条 |
| N05 | `apollo-assets.html` | WF-AP-05 | 09 §6.1 · OPS-008 · 03 资产版本 | Asset Bundle 列表；绑定 Channel；SemVer |
| N06 | `apollo-change-mgmt.html` | WF-AP-06 | 09 §4.5 | 环境变更审批单列表+详情 |
| N07 | `apollo-config.html` | WF-AP-07 | 09 §4.4 · §4.4.1 | Override 编辑；**Vault/KMS 引用**；维护窗口 |
| N08 | `aip-draft-inbox.html` | WF-AIP-06 | 07a §8 · 06b ACT-09 | Draft 队列；批准/拒绝；标明 **Draft Dataset 隔离** |
| N09 | `aip-decision-lineage.html` | WF-AIP-07 | 07a §9 · 07 熔断入谱 | 一次决策：读 Object/Wiki → 模型 → Action/Draft |
| N10 | `aip-evals.html` | WF-AIP-08 | 07a §10 · 07 L4 | 评测通过率；未绿禁 L4；与 Draft 联门控 |
| N11 | `aip-model-router.html` | WF-AIP-01 | 07a §4 · 07 路由 | Provider 列表；路由规则；冷启动**预热**状态 |
| N12 | `schedules.html` | WF-SC-01 | 05a · 05 SC-01 | Cron / 上游触发；从 sync/pipeline 可跳入 |
| N13 | `data-connection-agents.html` | WF-DC-05 | 05a · 05 DC-05 | Agent 注册状态 · 日志（边缘同步代理，≠ AIP Agent） |

### P1 · 应补

| # | 新建文件 | 线框 | 产品章节 | 验收要点 |
| --- | --- | --- | --- | --- |
| N14 | `pipeline-proposals.html` | WF-PB-02b | 05a 提案/历史 | 提案列表 · Diff/历史时间线 · 与画布跳转 |

### P2 · 可选补

| # | 新建文件 | 线框 | 产品章节 | 验收要点 |
| --- | --- | --- | --- | --- |
| N15 | `code-repositories.html` | WF-CR-01 | 05a · 05 | 变换仓库 IDE 空态 + 与 Function/Pipeline 跳转 |
| N16 | `workshop-module-interface.html` | WF-WS-10 | 08 §10 | 子 Module / Loop 嵌入示意 |
| N17 | `workshop-events.html` | WF-WS-11 | 08 §10 | 行选 → Overlay Events 配置 |
| N18 | （可选）`okf-funnel.html` | WF-FN-01 | 05a/06a | 仅 redirect → `funnel.html`，对齐路由名 |

**补页小计：P0=13 · P1=1 · P2=4 · 合计最多 18 个新文件**（不含 redirect）。

---

## 3. 改页任务清单（✅ 已有页必须补强）

### 3.1 工作台

| # | 文件 | 产品章节 | 须补内容 |
| --- | --- | --- | --- |
| E01 | `workshop-module.html` | 08 §4.4.1 · Table 分页 · Markings · 事件幂等 | Selection 维数计数（≤10）；Table「已分页 / >1万」；Widget 权限徽标；按钮防重复 |
| E02 | `workshop-object-view.html` | 同上 · 08a WF-WS-05 · 06b ACT-07 | Action 弹层：idempotent / HITL；Selection 上限 |
| E03 | `workshop-aip-chat.html` | 07a WF-AIP-09 · 链 AIP-07 | 「查看决策谱系」链到 `aip-decision-lineage.html` |
| E04 | `workshop-publish.html` | 09 · WF-WS-09 | 真实链到 AP-02/05；示 Channel / Asset Bundle 入口 |

### 3.2 AIP

| # | 文件 | 产品章节 | 须补内容 |
| --- | --- | --- | --- |
| E05 | `aip-maturity.html` | 07 §5b.3.1~2 | L4：**失败率>5% 熔断→降 L3**；预热中/就绪徽标；链 Evals/Draft |
| E06 | `aip-logic.html` | 07 §3.5.1 Edits 合并 · ACT-09 | 多 Logic 提议合并示意；Draft 节点 → 审批台 |
| E07 | `aip-tools.html` | 07 AIP-003 · Wiki Tool | Wiki 字段工具卡片明示「结构化字段优先」 |
| E08 | `agents.html` | 07a WF-AIP-05 | 顶栏/标题对齐 Chatbot Studio；L4 须 Evals+Draft 勾选禁用态 |

### 3.3 本体 / Wiki / Action / Function

| # | 文件 | 产品章节 | 须补内容 |
| --- | --- | --- | --- |
| E09 | `ontology-wiki.html` | **03 §3.2.3** 双向技术定义 | Tab：**方向 A / 方向 B**；冲突 LWW；写回走 Action；Agent 只读 |
| E10 | `ontology-action.html` | 06b ACT-07~10 | 幂等键；软删除；Webhook 重试×3→DLQ；**Draft Dataset** 目标 |
| E11 | `ontology-function.html` | 06b FUNC-03/06 | 超时≤60s · 内存≤2GB 展示；无 Submission UI 文案 |
| E12 | `ontology-link.html` | 06 §6.1~6.2 | 解法 B 规模警示（>100万→MDO）；解法 C「禁高频筛选」禁用态 |

### 3.4 数据集成

| # | 文件 | 产品章节 | 须补内容 |
| --- | --- | --- | --- |
| E13 | `sync-routing.html` | 05 v1.4 小文件短路 | **&lt;128KB → Dataset 短路** 选项/说明 |
| E14 | `pipeline-doc-intel.html` | 05 DocIntel 死信 | **DLQ** 列表：失败原因 · 重试/跳过 |
| E15 | `dataset.html` | 05 MediaReference · DS-02 | media_ref 列缩略图；History Tab 确认可见 |
| E16 | `source-new.html` | 05 L1 P0/P1 连接器 | Word/Excel/PDF/md·txt·csv · JDBC(**MySQL**) 高亮「P0/P1」 |
| E17 | `sync.html` / `pipeline.html` | 05a → SC-01 | 「打开计划编辑器」→ `schedules.html` |
| E18 | `health.html` · `lineage.html` | 05 死信 · 健康 | 死信/解析失败计数或边样式（最小徽标即可） |
| E19 | `funnel.html` | 05a WF-FN-01 · OKF | 与 OM-07 跳转互链清晰；Lint 失败不可 Publish |

### 3.5 概览壳

| # | 文件 | 产品章节 | 须补内容 |
| --- | --- | --- | --- |
| E20 | `index.html` | 03 · 本清单 §1.6 | 侧栏：**交付 Apollo**；补齐 AIP/数据新链；概览卡片同步 |
| E21 | `README.md` | 本清单 | 版本升至 **v1.6.x**；全模块映射表（含 Apollo/AIP 门控） |

**改页小计：E01–E21 = 21 项**（部分文件合并改一次即可）。

---

## 4. 已齐项（本轮可不改，仅回归）

确认仍可打开、侧栏可达即可：

`workshop.html` · `workshop-canvas.html` · `workshop-cop.html` · `ontology.html` · `ontology-object.html` · `ontology-property.html` · `ontology-branches.html` · `ontology-funnel.html` · `data-connection.html` · `source-detail.html` · `pipeline-list.html` · `builds.html` · `media-sets.html`

---

## 5. 产品补强 → UI 覆盖矩阵（防遗漏）

| 产品补强条款 | 文档锚点 | 覆盖任务 # |
| --- | --- | --- |
| Lite Spoke | 09 §6.2 OPS-010 | N03 |
| Spoke 出站轮询 | 09 §3.2.1 | N03 |
| Vault/KMS 禁明文 | 09 §4.4.1 | N07 |
| 紧急发布 hotfix | 09 §4.5.1 | N02 |
| FDE Asset Bundle / 版本同绑 | 09 §6.1 · 03 | N05 |
| Wiki 双向 A/B · 冲突 · 受控写回 | 03 §3.2.3 | E09 |
| Action 幂等 ACT-07 | 06b / 06 §7.0 | E10 · E01 · E02 |
| 软删除 ACT-08 | 06b | E10 |
| Draft Dataset ACT-09 | 06b | N08 · E10 · E06 |
| Webhook 重试/死信 ACT-10 | 06b | E10 · E18 |
| Function ≤2GB/60s | 06b FUNC-03 | E11 |
| 解法 B >100万 → MDO | 06 §6.1 | E12 |
| 解法 C 禁高频 | 06 §6.2 | E12 |
| Edits 合并 | 07 §3.5.1 | E06 |
| L4 熔断 >5% | 07 §5b.3.1 | E05 · N09 |
| 模型预热 | 07 §5b.3.2 | N11 · E05 |
| Selection ≤10 维 | 08 §4.4.1 | E01 · E02 |
| Table >1 万行分页 | 08 | E01 |
| Widget Markings | 08 | E01 |
| 事件幂等 | 08 · ACT-07 | E01 · E02 |
| 小文件 &lt;128KB 短路 | 05 v1.4 | E13 |
| DocIntel DLQ | 05 v1.4 | E14 · E18 |
| MediaReference 总图/列 | 05 | E15 ·（总图若在 index 可选） |
| JDBC MySQL P1 / 文件 P0 | 05 | E16 |
| 计划编辑器 / 代理管理 | 05a SC-01 · DC-05 | N12 · N13 |
| 管道提案历史 | 05a PB-02b | N14 |
| Evals / Draft / Lineage 独立页 | 07a | N08~N10 |
| 模型路由中心 | 07a AIP-01 | N11 |
| Apollo 七页 | 09 §9 | N01~N07 |
| WF-WS-10/11 可选 | 08 | N16 · N17 |
| 代码库 | 05a CR-01 | N15 |

---

## 6. 施工批次建议（仍先方案、后改 HTML）

| 批次 | 内容 | 交付物 |
| --- | --- | --- |
| **B1** | Apollo N01–N07 + E04 + E20/E21 侧栏 | 交付面可售前演示 |
| **B2** | AIP N08–N11 + E05–E08 | 决策门控闭环 |
| **B3** | L1 N12–N14 + E13–E19 | 数据补强可见 |
| **B4** | 本体/Wiki/Action E09–E12 + 工作台 E01–E03 | 本轮护栏进 UI |
| **B5** | P2 N15–N18 | 可选增强 |

每批次完成后：本地 `index.html` 点通所有新链；对照本清单 §5 矩阵勾选；README 版本 +0.0.1。

---

## 7. 明确不在 HTML 蓝图范围（避免误补）

| 项 | 原因 |
| --- | --- |
| v0.1 / Dify 试用壳 | `10_v01` 交付面 ≠ 售前 html |
| 右引擎深度 UI（若 20_tech 已不写） | 以 **03 叙事 vs 20_tech 口径** 另案统一后再画 |
| Gotham / 真实安全产品页 | 03 下沉映射，非 Foundry html 主路径 |
| 09a 线框 Markdown 正文 | 文档债；HTML 可先按 09 §9 ID 做，不阻塞 |
| 真实 Vault/KMS 联调 | Demo 只示「引用密钥」交互，不接真密钥 |

---

## 8. 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-07-16 | 初稿：全线框 ID + 本轮产品补强矩阵 + 补页18/改页21 + 批次 B1–B5 |
| v1.1 | 2026-07-16 | **施工完成**：Demo v1.6.0 · B1–B5 落地 · 待统一验收 |
| v1.2 | 2026-07-17 | **25 演进**：补 `ontology-graph-health` · 改 Draft/Lineage/funnel/health · Demo **v1.6.1** |
| v1.3 | 2026-07-17 | 模型拆屏：`aip-model-providers` + `aip-model-router` · Demo **v1.6.2** |
| v1.4 | 2026-07-17 | 重能力：`aip-capabilities` · 07b · Demo **v1.6.3** |
| v1.5 | 2026-07-17 | Appearance 主题样板（浅/深/系统）· Demo **v1.6.4** · T-UI §4.4 |
| v1.6 | 2026-07-17 | Appearance **全站铺开** · Demo **v1.6.5** |
| v1.7 | 2026-07-23 | **状态标记统一**：全部 🔧/➕/⏳/📄🔧 → ✅；图例简化为「已完成」；施工状态更新为「已统一验收」 |

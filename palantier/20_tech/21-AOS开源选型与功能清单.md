# 21 · AOS 开源选型与功能清单（总表）

> **文档性质**：目标态 AOS **全部功能项** × **自有需求** × **开源候选** × **选型结论**；并盘点 `mybuddy-v01` 已下载仓是否够用  
> **版本**：v1.0.3 · 2026-07-17（增 **X-06 App Log** · 对齐 T-CROSS §3.2）
> **状态**：可评审 · 可指导补拉仓与实现排期  
> **依据**：[T05](T05-L1数据集成详细技术方案.md)～[T09](T09-Apollo交付引擎详细技术方案.md) · [T-CROSS](T-CROSS-横切能力详细技术方案.md) · [T-UI](T-UI-前端工程与foundry-html落地规范.md) · [20](20-AOS整体技术方案.md) · [11 缺口清单](../10_v01/11-目标态开源缺口清单.md)  
> **仓址/License**：**[22](22-AOS开源产品维护清单.md)** · 补拉 `[clone_aos_deps.ps1](../../../mybuddy-v01/clone_aos_deps.ps1)`  
> **强制军规**：**[23](23-AOS开源引用与交付军规.md)** · **客户先装 SOP**：**[24](24-AOS客户侧前置组件安装SOP.md)** · 示例 `[docs/examples/customer-prereq/](../../examples/customer-prereq/)`  
> **本地树**：`mybuddy-v01/`（`clone_mybuddy_repos.ps1` + `clone_airbyte_refs.ps1` + `**clone_aos_deps.ps1`**）· `ClaudeSkills/`（≠ 产品运行时）

---

## 使用的 Rules


| Rule     | 应用                            |
| -------- | ----------------------------- |
| 中文       | 全文中文                          |
| 先自有后开源   | 每项先写 AOS 功能，再写候选与选型           |
| 开源=参考    | 禁止「基于 XXX 二次开发」话术；产品壳自有       |
| 最小补拉     | 只标缺口；不强制一次拉齐全部备选              |
| 与 T0x 自洽 | 建议选型不得推翻 T05～T09 / T-CROSS 已决 |


---

## 0. 总判定（够不够用）


| 判定               | 说明                                                                                                                   |
| ---------------- | -------------------------------------------------------------------------------------------------------------------- |
| **主链路参考仓：基本够用**  | L1 ETL/CDC/Iceberg · L2 图/Wiki/编排 · AIP Gateway/Logic/Evals · L3 低代码参考 · Apollo GitOps/密钥/气隙镜像 · 横切 IdP/Authz 均已落地本地 |
| **P0 硬缺口参考仓**    | ✅ **已拉齐**（2026-07-17）：`refs/ocr/PaddleOCR` · `refs/objstore/minio` · `refs/objstore-sdk/minio-py`                    |
| **细项仍缺（P1/P2）**  | 见 §1.2：Grafana / Redis / cosign / CDC 总线 / MCP 等（不阻塞 Facade；按需 `-Tier P1,P2`）                                        |
| **脚本未落地仓**       | `fastmcp-airbyte`、`fastmcp-extensions`、`airbyte-agents-benchmark`（P2）                                                |
| **ClaudeSkills** | **工程加速技能库**（Prompt/评测/安全/协作方法），**不是** AOS 运行时组件；不计入「开源够不够」的产品判定                                                      |
| **试用版**          | `dify` / `openocta` 仅 v0.1；目标态禁止当永久内核（T-EVO）                                                                         |


```text
够用（模式参考）──→ 可开工实现 Facade / Host / Runtime
缺细项（实现依赖）──→ 补拉或装发行包后再接插件
多方案 ──→ 以本表「建议选型」为准；详稿 T0x 已决优先
```

---

## 1. 本地仓盘点

### 1.1 已下载（按缺口目录）


| 目录                       | 仓                                                 | 服务域                    |
| ------------------------ | ------------------------------------------------- | ---------------------- |
| `A1_ETL/`                | meltano · pyairbyte · **airbyte-python-cdk**      | L1 Connector           |
| `A3_CDC/`                | debezium                                          | L1 CDC                 |
| `A4_Lakehouse/`          | iceberg · duckdb                                  | Dataset                |
| `B1_GraphStore/`         | age · nebula · memgraph                           | L2 Graph               |
| `B3_GraphViz/`           | G6 · cytoscape.js                                 | L3 图谱                  |
| `B4_Metadata/`           | linkml                                            | L2 Meta DSL            |
| `B5_Workflow/`           | temporal · conductor                              | Funnel/Action/Pipeline |
| `B7_Wiki/`               | outline · wiki                                    | L2 Wiki UX             |
| `C1_ModelRouter/`        | litellm                                           | AIP Gateway            |
| `C2_Evals/`              | promptfoo                                         | AIP Evals              |
| `C3_Trace/`              | langfuse                                          | Trace                  |
| `C5_AgentOrchestration/` | langgraph · airbyte-agent-sdk · airbyte-agent-cli | Logic / Tool           |
| `C8_RightEngine/`        | qdrant · milvus                                   | 向量（工具侧；非右引擎产品）         |
| `D1_WorkshopFactory/`    | ToolJet · appsmith                                | L3 画布参考                |
| `D3_HighPerfGrid/`       | ag-grid                                           | 大表                     |
| `D4_Map/`                | kepler.gl                                         | COP 地图                 |
| `E1_GitOps/`             | argo-cd · terraform-provider-airbyte              | Apollo 参考              |
| `E3_Secrets/`            | vault                                             | 密钥                     |
| `E4_AirGap/`             | skopeo                                            | Ferry 镜像               |
| `E7_Observability/`      | prometheus                                        | 指标                     |
| `F1_Identity/`           | keycloak                                          | IdP                    |
| `F2_Authz/`              | openfga                                           | Authz                  |
| 试用                       | dify · openocta · desktop/adapter                 | v0.1 only              |
| `**refs/ocr/`**          | **PaddleOCR**                                     | L1 OCR 参考 ✅            |
| `**refs/objstore/`**     | **minio**（AGPL·仅参考）                               | MediaSet Dev 参考 ✅      |
| `**refs/objstore-sdk/`** | **minio-py**                                      | S3Adapter SDK 参考 ✅     |


### 1.2 细项缺口（标记）


| 缺口                                       | 为何需要                 | 优先级    | 本地状态                   | 建议动作                    |
| ---------------------------------------- | -------------------- | ------ | ---------------------- | ----------------------- |
| **PaddleOCR**                            | T05 扫描件 OCR          | P0     | ✅ `refs/ocr/PaddleOCR` | 接 `parser-pdf-ocr` 独立进程 |
| **MinIO** + **minio-py**                 | MediaSet / S3Adapter | P0     | ✅ `refs/objstore`*     | **客户先装**服务端（24）；交付不捆    |
| Tesseract（可选备选）                          | 轻量 OCR 备选            | P0-opt | ✅ `refs/tesseract`     | 英文/轻量；默认仍 PaddleOCR     |
| SeaweedFS（可选备选）                          | 大规模对象仓备选             | P0-opt | ✅ `refs/seaweedfs`     | Apache；与 MinIO 对照       |
| **Grafana**                              | 运维看板深链               | P1     | ❌                      | `-Tier P1` 或发行包         |
| **Redis**                                | 缓存/限流/会话             | P1     | ❌                      | `-Tier P1` 或发行包         |
| **cosign**                               | Ferry 签验             | P1     | ❌                      | `-Tier P1`              |
| **Kafka / Redpanda**                     | CDC 下游               | P1     | ❌（设计跳过整仓）              | 有 CDC 时用发行包             |
| **Helm**                                 | Full Spoke           | P1     | ❌（设计不拉整仓）              | CI 用 helm CLI           |
| **OpenSearch**                           | L2 全文附属              | P2     | ❌                      | 按需                      |
| **OTel Collector**                       | 统一采集                 | P2     | ❌                      | 可选                      |
| `fastmcp-airbyte` + `fastmcp-extensions` | MCP 附录               | P2     | ❌                      | `-Tier P2`              |
| `airbyte-agents-benchmark`               | Agent 评测             | P2     | ❌                      | `-Tier P2`              |
| React/Vite/Playwright                    | 前端工程                 | P0 工程  | npm                    | **不必**整仓 clone          |


### 1.3 ClaudeSkills 定位


| 项      | 结论                                                                    |
| ------ | --------------------------------------------------------------------- |
| 路径     | 仓库平级 `ClaudeSkills/`                                                  |
| 内容     | engineering / product-team / research / compliance 等 **Agent Skills** |
| 用途     | 研发方法、评审、Prompt、安全扫描等加速                                                |
| **不是** | Connector / Ontology / Workshop / Apollo 的替代实现                        |
| 交付     | **不进**客户安装包                                                           |


---

## 2. 功能总表（权威 List）

> 列说明：**自有功能** = AOS 必须交付的产品能力；**候选开源** = 可参考/可边车；**本地** = ✅已拉 / ❌缺 / 试用；**建议选型** = 工程默认。

### 2.A L1 数据集成（T05）


| #     | 功能项             | 功能描述（自有）                               | 可参考开源                                        | 优劣与建议选型                                                                                                                       | 本地                               |
| ----- | --------------- | -------------------------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| L1-01 | Connector Host  | 插件注册、配置、discover、sync、health；密钥 ref    | Meltano · PyAirbyte · airbyte-python-cdk     | **Meltano** 插件协议/状态成熟；**CDK** 自研连接器；**PyAirbyte** 轻量抽数。**不**用 Airbyte monorepo 当产品。**建议：Host 自研 + Meltano 协议思路 + CDK 写客户连接器** | ✅                                |
| L1-02 | JDBC MySQL Sync | P1 必做结构化入湖                             | PyAirbyte / JDBC 自研                          | 示例路径可抄 PyAirbyte；生产插件自有。**建议：自研 jdbc-mysql 插件**                                                                               | ✅参考                              |
| L1-03 | 文件接入            | Word/Excel/PDF/md/csv→Dataset/MediaSet | （解析库）+ OCR 见下                                | 契约自有。**建议：parser 插件化**                                                                                                        | ✅参考齐；插件待实现                       |
| L1-04 | OCR             | 扫描件 PDF 抽文本                            | **PaddleOCR** vs Tesseract                   | **建议：默认 PaddleOCR**；`parser-pdf-ocr` **独立进程**。仓址 [22](22-AOS开源产品维护清单.md)                                                      | ✅ PaddleOCR · ✅ `refs/tesseract` |
| L1-05 | 存储路由            | Dataset / MediaSet / Stream；<128KB 短路  | —                                            | **纯自研**（产品护栏）                                                                                                                 | —                                |
| L1-06 | MediaSet 对象仓    | 原件存储与预览                                | **MinIO** vs SeaweedFS / 客户 S3               | Dev 参考 MinIO；大规模/License 友好可评 **SeaweedFS**；生产换客户 S3（`S3Adapter`）。**MinIO AGPL → 客户先装、交付不捆**（23/24）                           | ✅ minio* · ✅ `refs/seaweedfs`    |
| L1-07 | Dataset 表格式     | 事务表、时间旅行、Preview                       | **Iceberg** + DuckDB                         | Iceberg 生产表格式；DuckDB 开发/小规模查询。**建议：Iceberg 主存 + DuckDB 辅助**                                                                   | ✅                                |
| L1-08 | CDC             | 位点流式同步                                 | Debezium（± Kafka/Redpanda）                   | Debezium 成熟但常绑消息总线。**建议：有 CDC 需求再上；总线补 Kafka/Redpanda**                                                                       | ✅/缺总线                            |
| L1-09 | Pipeline DAG    | 变换 · Use LLM · DocIntel · DLQ          | Temporal（编排）                                 | 画布产品自有；长任务借 Temporal。**建议：壳自研 + Temporal 编排**                                                                                 | ✅                                |
| L1-10 | Schedule        | Cron / 上游触发                            | Meltano schedule 思路                          | **建议：自研调度面**，状态机可参考 Meltano                                                                                                   | ✅参考                              |
| L1-11 | 边缘 Agent        | 出站拉 Sync、回报                            | —（模式对齐 Spoke）                                | **自研**；≠ AIP Agent                                                                                                            | —                                |
| L1-12 | MCP 供数（可选）      | 研发侧只读通道                                | **fastmcp-airbyte** + **fastmcp-extensions** | 非主路径；MCP Server **自研**。触发/红线见 [22 §2.3](22-AOS开源产品维护清单.md)                                                                    | ❌                                |


### 2.B L2 Ontology / Action / Function / Wiki（T06）


| #     | 功能项              | 功能描述（自有）                                        | 可参考开源                         | 优劣与建议选型                                                                                                                        | 本地  |
| ----- | ---------------- | ----------------------------------------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | --- |
| L2-01 | Meta Store       | Object/Link/Property/Action/Function 元数据 + 发布门禁 | LinkML                        | LinkML 适合 Schema DSL/校验。**建议：Meta 自研，DSL 思路抄 LinkML**                                                                          | ✅   |
| L2-02 | Funnel           | Changelog→Merge→Index→Hydration                 | Temporal / Conductor          | Temporal 云原生/多语言；Conductor Java DSL。**建议：Temporal**                                                                            | ✅   |
| L2-03 | Graph 实例存储       | Object/Link 读写；API 不绑方言                         | **AGE** vs Nebula vs Memgraph | AGE：与 PG 同运维、v1 简单；Nebula：大规模分布式；Memgraph：低延迟内存。**建议：v1=PG+AGE；规模切换 Nebula（Adapter）**                                          | ✅   |
| L2-04 | Action Runtime   | Criteria·幂等·Draft·Webhook·DLQ                   | Temporal（异步）                  | 产品语义自有。**建议：Runtime 自研 + Temporal 跑长副作用**                                                                                      | ✅   |
| L2-05 | Function Runtime | 沙箱·超时·只读默认                                      | —                             | **自研**（语言运行时可选容器隔离）                                                                                                            | —   |
| L2-06 | Wiki 双向          | A 系统→人；B 人→Action；字段与 Object 同源                 | Outline vs Wiki.js            | Outline 协作 UX 更现代；Wiki.js 偏站点。**建议：UX 参考 Outline；数据模型自研**。**License：Outline=BSL、Wiki.js=AGPL → 只参考 UX，不嵌代码、不进交付包**（宜放 `refs/`） | ✅参考 |
| L2-07 | OKF Bundle       | tar.gz+manifest；Channel 同绑                      | —                             | **自研格式**（与 Apollo 资产同族）                                                                                                        | —   |
| L2-08 | 全文附属（可选）         | 过滤/搜索加速                                         | OpenSearch                    | 不替代图主存。**P2 默认不拉**；触发与红线见 [22 §2.3](22-AOS开源产品维护清单.md)                                                                         | ❌   |


### 2.C AIP（T07）


| #      | 功能项                  | 功能描述（自有）                   | 可参考开源                 | 优劣与建议选型                                                       | 本地  |
| ------ | -------------------- | -------------------------- | --------------------- | ------------------------------------------------------------- | --- |
| AIP-01 | Model Gateway Facade | `/v1/aip/`*；路由·配额·预热·熔断·审计 | LiteLLM ·（Dify 仅 UX）  | LiteLLM 多 Provider 强；不可当品牌。**建议：Facade 自有 + LiteLLM 边车**      | ✅   |
| AIP-02 | Logic Runtime        | 有状态图·Tool·Draft·Edits 合并   | LangGraph             | 检查点/重试成熟；须加 Ontology 约束。**建议：LangGraph 作内核参考**                | ✅   |
| AIP-03 | Tool Registry        | 六类工具；写落 Action             | airbyte-agent-sdk（模式） | SDK 把 Connector 变 Tool 的模式可抄；**禁止 UI 直依赖**。**建议：Registry 自研** | ✅   |
| AIP-04 | Chatbot Studio       | Agent 配置与试对话               | Dify/OpenOcta（仅 v0.1） | 试用脑可抄 UX，目标态替换。**建议：产品自研；v0.1 过渡**                            | 试用  |
| AIP-05 | Draft / HITL         | 审批隔离生产                     | —                     | **自研**                                                        | —   |
| AIP-06 | Decision Lineage     | 决策谱系 + 熔断事件                | langfuse（观测）          | Langfuse≠产品谱系。**建议：谱系自研 + Langfuse Trace**                    | ✅   |
| AIP-07 | Evals 门控             | L4 须绿                      | promptfoo             | harness 成熟。**建议：promptfoo 作评测引擎参考**                           | ✅   |
| AIP-08 | 向量检索（工具侧）            | RAG/Media 检索，≠ Ontology    | **Qdrant** vs Milvus  | Qdrant 运维轻、Lite 友好；Milvus 大规模。**建议：需要时 Qdrant 优先**            | ✅   |
| AIP-09 | 右引擎产品                | —                          | milvus/qdrant         | **目标态不做**（备忘）；向量仅工具侧                                          | 仓可留 |


### 2.D L3 工作台（T08）+ 前端（T-UI）


| #     | 功能项            | 功能描述（自有）                          | 可参考开源               | 优劣与建议选型                                                                                                                    | 本地  |
| ----- | -------------- | --------------------------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------- | --- |
| L3-01 | Module Runtime | Layout/Variables/Events/发布        | ToolJet vs Appsmith | ToolJet 更近 React 组件化。**建议：交互抄 ToolJet；视觉=foundry/html**。**License：ToolJet=AGPL v3 → 只参考交互，禁止 submodule 进产品工程**（宜放 `refs/`） | ✅参考 |
| L3-02 | Object Table   | 大表虚拟滚动 + 服务端分页                    | ag-grid             | 性能强；注意社区/企业许可。**建议：ag-grid 社区版起步**                                                                                         | ✅   |
| L3-03 | 知识图谱 Widget    | Object+Link 可视化                   | **G6** vs cytoscape | G6 中文生态/布局丰富；cytoscape 经典。**建议：G6**                                                                                        | ✅   |
| L3-04 | COP 地图         | 态势地图层                             | kepler.gl           | 分析地图强。**建议：COP 需要时嵌入**                                                                                                     | ✅   |
| L3-05 | Buddy 嵌入       | Selection Context → AIP Chat      | —                   | **自研**（调 aos-api）                                                                                                          | —   |
| L3-06 | 前端工程           | React18+TS · Tailwind · 契约 client | —（npm）              | **已决 React**；不必克隆框架整仓                                                                                                      | npm |
| L3-07 | 桌面壳            | Tauri 三端                          | mybuddy-v01/desktop | 保留壳，内容区换同构 Web                                                                                                             | ✅工程 |
| L3-08 | 视觉回归           | 关键页截图门禁                           | Playwright（npm）     | **建议 S2 CI**                                                                                                               | npm |


### 2.E Apollo（T09）


| #     | 功能项          | 功能描述（自有）                           | 可参考开源                      | 优劣与建议选型                                                                    | 本地       |
| ----- | ------------ | ---------------------------------- | -------------------------- | -------------------------------------------------------------------------- | -------- |
| AP-01 | Hub Control  | Catalog·Plan·Channel·Recall·Change | Argo CD（模式）                | Argo=单集群 GitOps；Apollo=跨域舰队+Channel。**建议：控制面自研；同步/健康思路抄 Argo**             | ✅        |
| AP-02 | Lite Spoke   | Compose · 出站轮询 · Probe             | —                          | **自研 Agent**                                                               | —        |
| AP-03 | Full Spoke   | K8s/Helm 执行                        | Argo + Helm                | **建议：P1 再上；Helm 用发行版**                                                     | 缺 Helm 仓 |
| AP-04 | 密钥注入         | 配置只存 ref                           | **Vault** vs 客户 KMS / SOPS | Vault 动态密钥强；KMS 客户已有则对接；SOPS 偏 Git 密文。**建议：Vault 默认，KMS 适配器**              | ✅        |
| AP-05 | Ferry        | 签名 tar.gz 摆渡                       | Skopeo + cosign            | Skopeo 镜像拷贝；cosign 签名生态。**建议：Skopeo（已有）+ 补 cosign**                        | 部分缺      |
| AP-06 | Asset Bundle | OKF/Module/Agent 同绑 Channel        | —                          | **自研**                                                                     | —        |
| AP-07 | Probe 指标     | Reported State + 指标                | Prometheus · Grafana       | Prom 采集；Grafana 看板。**建议：Prom 已有；Grafana AGPL → 发行包装 + 只交付 Dashboard JSON** | 部分缺      |


### 2.F 横切（T-CROSS）


| #    | 功能项           | 功能描述（自有）            | 可参考开源                           | 优劣与建议选型                                                 | 本地          |
| ---- | ------------- | ------------------- | ------------------------------- | ------------------------------------------------------- | ----------- |
| X-01 | IdP           | OIDC 统一登录           | **Keycloak**（vs Authentik）      | Keycloak 生态大、已拉；Authentik 更轻。**建议：Keycloak**            | ✅           |
| X-02 | Authz         | 关系元组 + Markings     | **OpenFGA**（vs Casbin）          | OpenFGA 关系模型贴 Object；Casbin 更通用 ACL。**建议：OpenFGA 边车**   | ✅           |
| X-03 | 多租户           | org_id + project_id | —                               | **自研字段与中间件**                                            | —           |
| X-04 | Audit         | 不可关审计               | —                               | **自研**                                                  | —           |
| X-05 | Trace/Metrics | 全链路 + RED           | langfuse · prometheus · grafana | 见上                                                      | 部分缺 Grafana |
| X-06 | App Log       | 分级·环境开关·结构化·脱敏      | —                               | **自研 Logger 门面**（[T-CROSS §3.2](T-CROSS-横切能力详细技术方案.md)） | —           |


### 2.G 工程辅助（非产品）


| #      | 功能项          | 功能描述           | 可参考              | 建议               | 本地  |
| ------ | ------------ | -------------- | ---------------- | ---------------- | --- |
| ENG-01 | Agent Skills | 研发/评审/安全方法     | **ClaudeSkills** | 按需引用 Skill；不进交付包 | ✅   |
| ENG-02 | v0.1 问答脑     | 试用 Local-First | dify · openocta  | 仅过渡；目标态替换（T-EVO） | ✅试用 |


---

## 3. 多方案选型速查（决策卡）


| 域            | 候选                                 | 建议                    | 一句话原因                |
| ------------ | ---------------------------------- | --------------------- | -------------------- |
| Connector 协议 | Meltano / PyAirbyte / Airbyte mono | **Meltano 协议 + CDK**  | 插件化清晰；禁 monorepo 当壳  |
| 图存储          | AGE / Nebula / Memgraph            | **AGE**               | 与 PG 同运维；规模再迁 Nebula |
| 工作流          | Temporal / Conductor               | **Temporal**          | 多语言、重试模型清晰           |
| Wiki UX      | Outline / Wiki.js                  | **Outline**           | 协作与权限更贴近业务 Wiki      |
| LLM 网关       | LiteLLM / 自研全量适配                   | **Facade+LiteLLM 边车** | 速度与可替换平衡             |
| Logic 图      | LangGraph / 自研                     | **参考 LangGraph**      | 检查点成熟；约束自加           |
| Evals        | promptfoo / 其它                     | **promptfoo**         | harness 现成           |
| 向量           | Qdrant / Milvus                    | **Qdrant（按需）**        | Lite 友好              |
| 低代码参考        | ToolJet / Appsmith                 | **ToolJet 思路**        | 近 React；视觉仍 html     |
| 大表           | ag-grid / 自研虚拟表                    | **ag-grid**           | 性能与列模型               |
| 图谱           | G6 / cytoscape                     | **G6**                | 布局与中文生态              |
| IdP          | Keycloak / Authentik               | **Keycloak**          | 已拉、企业常见              |
| Authz        | OpenFGA / Casbin                   | **OpenFGA**           | 关系元组贴 Object         |
| 密钥           | Vault / KMS / SOPS                 | **Vault + KMS 适配**    | 动态密钥与客户合规            |
| GitOps 参考    | Argo / Flux                        | **Argo（仅参考）**         | 已拉；≠ Apollo 产品       |
| OCR          | PaddleOCR / Tesseract              | **PaddleOCR**         | 中文场景                 |
| 对象仓          | MinIO / Seaweed / 客户 S3            | **MinIO（Dev）**        | S3 API、私有化快          |
| CDC 总线       | Kafka / Redpanda                   | **有需求再选**             | Lite 可暂缓             |


---

## 4. 补拉优先级清单（给脚本/运维）


| 优先级    | 补什么                                                      | 用途                                                 |
| ------ | -------------------------------------------------------- | -------------------------------------------------- |
| **P0** | PaddleOCR · MinIO(+minio-py)                             | ✅ **已 clone**（2026-07-17）· 下一程：接插件/Adapter         |
| **P1** | Grafana · Redis · cosign ·（CDC 时）发行包 · Helm CLI          | `.\clone_aos_deps.ps1 -Tier P1`；Helm/Kafka **不**整仓 |
| **P2** | OpenSearch · OTel · fastmcp-* · airbyte-agents-benchmark | `-Tier P2` 或 `All`                                 |


> 仓址 / License / 红线见 [22](22-AOS开源产品维护清单.md)。AGPL 服务端（MinIO/Grafana）**禁止捆进客户交付包**。

---

## 5. 与详稿交叉引用


| 详稿                                           | 自有功能节（新增/强化）              | 开源节                       |
| -------------------------------------------- | ------------------------- | ------------------------- |
| [T05](T05-L1数据集成详细技术方案.md)                   | §3.1 · §4.0 · §5.1        | §3.2 · §4.4.1 · §5.2      |
| [T06](T06-Ontology与Action-Function详细技术方案.md) | §4.0 · §5.0 · §6.0 · §7.0 | §4.2 · §6.1 · §7.0.1      |
| [T07](T07-AIP人工智能平台详细技术方案.md)                | §3.0 · §4.0 · §5.0 · §6.0 | §3.2 · §4.1 · §5.2 · §6.2 |
| [T08](T08-Workshop工作台详细技术方案.md)              | §4.0                      | §4.3                      |
| [T09](T09-Apollo交付引擎详细技术方案.md)               | §5.0                      | §5.2                      |
| [T-CROSS](T-CROSS-横切能力详细技术方案.md)             | §1.0 · §2.0 · §3.0        | §1.1 · §2.1 · §3.1        |
| [T-UI](T-UI-前端工程与foundry-html落地规范.md)        | §1～3 自有工程                 | §5                        |


---

## 6. 修订记录


| 版本     | 日期         | 说明                                                                                           |
| ------ | ---------- | -------------------------------------------------------------------------------------------- |
| v1.0   | 2026-07-17 | 首版：本地仓盘点 · 缺口标记 · 全功能选型总表 · 与 T05～T09/T-CROSS 对齐                                             |
| v1.0.1 | 2026-07-17 | 挂 [22](22-AOS开源产品维护清单.md)；补 L1-12 fastmcp-extensions；L2-06/L3-01/L1-06 License 红线；OCR 独立进程口径 |
| v1.0.2 | 2026-07-17 | 核盘：P0 三仓已入 `refs/`；§0/§1.2/L1-04/06 状态改为 ✅；剩余缺口仅 P1/P2                                       |


---

*21 · 先自有功能，后开源参考 · 开源够主链路，细项按 P0 补齐*
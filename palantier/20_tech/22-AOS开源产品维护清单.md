# 22 · AOS 开源产品维护清单

> **文档性质**：**开源上游产品注册表**（SSH · License · AOS 落点 · 交付红线 · 本地目录 · 补拉脚本）  
> **版本**：v1.6 · 2026-07-17（§2.3 P2 四组件详解）  
> **状态**：维护真源 · 与 [21 选型总表](21-AOS开源选型与功能清单.md) 配套（21=选型决策；**本篇=仓址/证照/怎么放**）  
> **军规（强制）**：**[23 开源引用与交付军规](23-AOS开源引用与交付军规.md)**  
> **安装 SOP（活文档）**：**[24 客户侧前置组件安装 SOP](24-AOS客户侧前置组件安装SOP.md)** · 示例 `[docs/examples/customer-prereq/](../../examples/customer-prereq/)`  
> **本地根**：`mybuddy-v01/`  
> **补拉脚本**：`[clone_aos_deps.ps1](../../../mybuddy-v01/clone_aos_deps.ps1)`（P0/P1/P2）· 另见 `clone_mybuddy_repos.ps1` · `clone_airbyte_refs.ps1`

---

## 使用的 Rules


| Rule           | 应用                          |
| -------------- | --------------------------- |
| 中文             | 全文中文                        |
| 先自有后开源         | AOS 功能 ID 对齐 21；本篇不重复改选型结论  |
| License 红线先于便利 | AGPL/BSL **不捆进交付包、不进产品编译链** |
| refs vs 可引用    | 见 §0 目录归位                   |
| 最小补拉           | §2 只列**未拉**项；已拉一律进 §3       |


---

## 0. 目录归位（维护约定）

```text
mybuddy-v01/
├── desktop/ · adapter/ · openocta-overlay/   # 产品运行时 / 自研
├── dify/ · openocta/                        # 仅 v0.1 试用脑（非目标内核）
├── A1_ETL/ … F2_Authz/                      # Apache2/MIT 等：可留作参考 submodule 区
├── refs/                                    # 参考/二开时看；BSL·AGPL 与补拉依赖优先放此
│   ├── ocr/ · objstore/ · objstore-sdk/ · seaweedfs/ · tesseract/ · cache/ · ferry/ · obs/ · mcp/ · eval/ …
└── ClaudeSkills/（仓库平级）                 # 工程技能；不进交付包
```


| 区                     | 放什么                    | 能否进产品编译/交付包            |
| --------------------- | ---------------------- | ---------------------- |
| **产品运行时**             | 自研模块 + adapter/desktop | ✅                      |
| `**A*_/B*_/…`（宽松许可）** | Apache 2.0 / MIT 等参考实现 | 仅模式/边车；禁「基于 XXX 发行」    |
| `**refs/`**           | BSL/AGPL、补拉依赖、纯 UX 参考  | **否**（看源码 / 本地 Dev 自装） |
| **ClaudeSkills**      | Agent Skills           | **否**                  |


**归位建议（已有仓）：** Outline / Wiki.js / ToolJet 等 AGPL·BSL → 长期应视为 `**refs/` 纯参考**，勿 `submodule` 进产品工程；短期可仍留在 `B7_Wiki/`·`D1_WorkshopFactory/`，但 **CI/构建禁止依赖其路径**（军规 **R-DIR-03**）。

### 0.1 与 23/24 的分工


| 文档                                  | 管什么                              |
| ----------------------------------- | -------------------------------- |
| **22（本篇）**                          | 仓 SSH · License · 本地目录 · 补拉脚本    |
| **[23 军规](23-AOS开源引用与交付军规.md)**     | 禁止项 / CI 门禁 / 违规处理（**强制**）       |
| **[24 SOP](24-AOS客户侧前置组件安装SOP.md)** | **客户先装**前置组件的步骤、总检、交接文件（**活文档**） |


---

## 1. License 红线总表（二开必避）


| 风险级 | 产品                                                                                       | License               | 交付策略                                              |
| --- | ---------------------------------------------------------------------------------------- | --------------------- | ------------------------------------------------- |
| 🔴  | **MinIO 服务端**                                                                            | AGPL v3               | **交付包不捆二进制**；安装指引 + `S3Adapter`；客户自装 MinIO 或自有 S3 |
| 🔴  | **Grafana**                                                                              | AGPL v3               | 只装发行包、不二开；交付只放 **Dashboard JSON**（配置≠衍生作品）        |
| 🔴  | **ToolJet**                                                                              | AGPL v3               | 只参考交互；不嵌代码、不 submodule 进产品                        |
| 🔴  | **Wiki.js**                                                                              | AGPL v3               | 只参考；数据模型自研                                        |
| 🟡  | **Outline**                                                                              | BSL                   | 只参考 UX；不嵌交付包                                      |
| 🟡  | **Vault**                                                                                | BSL                   | 发行包装 / 客户侧部署；不嵌源码                                 |
| 🟡  | **Memgraph**                                                                             | BSL                   | 同上；图默认用 AGE，Memgraph 仅备选评测                        |
| 🟡  | **Redpanda**                                                                             | BSL                   | 有 CDC 时优先 **发行包**；商用条款另核                          |
| ✅   | PaddleOCR / Tesseract / Redis / cosign / Kafka / Helm / OpenSearch / OTel / Keycloak / … | Apache2 / MIT / BSD 等 | 见各行；仍遵守「开源=参考」产品话术                                |


---

## 2. 补拉缺口（仅未拉项 · P0-opt → P2）

> **规则：** 一旦 clone 成功并核盘，条目从本节 **删除**，迁入 **§3 已拉仓一览表**。  
> P0 主三项、SeaweedFS、**Tesseract** 已迁 §3；本节不再重复。  
> **当前 §2.1 无 P0-opt 未拉项。**

### 2.2 🟡 P1 · 观测 / 缓存 / Ferry / CDC / Full Spoke（未拉）


| #   | 产品           | SSH                                         | License        | AOS              | 目标路径 / 动作               | 红线或说明               |
| --- | ------------ | ------------------------------------------- | -------------- | ---------------- | ----------------------- | ------------------- |
| 3   | **Grafana**  | `git@github.com:grafana/grafana.git`        | AGPL v3 ⚠️     | AP-07 / X-05     | `refs/obs/grafana` 或发行包 | 交付只放 Dashboard JSON |
| 4   | **Redis**    | `git@github.com:redis/redis.git`            | BSD 3-Clause ✅ | 限流/缓存/会话         | `refs/cache/redis`      | 或客户 Cluster         |
| 5   | **cosign**   | `git@github.com:sigstore/cosign.git`        | Apache 2.0 ✅   | AP-05 Ferry 签验   | `refs/ferry/cosign`     | 配已拉 Skopeo（§3）      |
| 6a  | **Redpanda** | `git@github.com:redpanda-data/redpanda.git` | BSL ⚠️         | L1-08 CDC        | **优先发行包**；可不 clone      | 有 CDC 再上            |
| 6b  | **Kafka**    | `git@github.com:apache/kafka.git`           | Apache 2.0 ✅   | 同上               | 一般不拉整仓                  | Lite 可暂缓            |
| 7   | **Helm**     | `git@github.com:helm/helm.git`              | Apache 2.0 ✅   | AP-03 Full Spoke | **不必 clone**；helm CLI   | 脚本默认跳过              |


### 2.3 🟢 P2 · 检索 / MCP / 评测（未拉 · 非核心）

> **总原则：** 下列组件均为 **「非核心、按需启用、仅作参考/旁路」**，**不阻塞** AOS 主链路（L1～L3 + AIP + Apollo）落地。  
> 默认：**只 star / 文档登记，不强制 clone**；触发条件满足后再 `clone_aos_deps.ps1 -Tier P2` 或按需单仓，并仍放 `refs/`（**禁止 submodule 进产品主工程**）。

#### 2.3.0 一览表（启用 / 红线 / 验收）

| 组件 | P2 定位 | 启用触发（满足任一） | 前置依赖 | 目标路径 | 二开红线（摘要） | 验收要点 | 对齐 21 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **OpenSearch** | 全文检索备胎；**不替代 AGE 主存** | 文档量 ≥10 万且 RAG 准确率 &lt;85%；或要同义词/拼音/高亮；或向第三方开放 Object 检索 | AGE 在线；Langfuse 可选 | `refs/search/opensearch`（参考）· 可独立部署、**不进交付主包** | ❌ 禁存核心业务属性；✅ 仅同步文本副本字段 | 模糊命中 ≥90%；检索延迟 ≤200ms | L2-08 |
| **OTel Collector** | 统一采集管道；**不存储、不可视化** | 跨组件排障；客户要全链路 SLA；或对接客户监控 | Langfuse + Prometheus 已部署 | `refs/otel/collector` · 独立部署、不进交付主包 | ❌ 不存业务/观测数据；✅ 只转发；生产默认采样 10% | Trace/Metrics 覆盖约定路径；无静默丢数 | X-05 |
| **fastmcp-airbyte**（+ **fastmcp-extensions**） | MCP 参考实现；**非 AOS 内核依赖** | 客户要 MCP；或把 Connector/Action 开放给第三方 MCP 客户端 | airbyte-agent-sdk 可参考；extensions 同拉 | `refs/mcp/fastmcp-airbyte` · `refs/mcp/fastmcp-extensions` | ❌ 禁直接依赖进产品；✅ MCP Server **自研**；只抄 Schema/流式 | 符合 MCP 标准；第三方客户端可调 AOS Tool | L1-12 / C5 |
| **airbyte-agents-benchmark** | Agent **性能**评测旁路；内部用 | 要 Agent 性能 SLA；优化 Tool/路由需基准；第三方审计 | promptfoo 主评测在线；AIP Logic 在线 | `refs/eval/airbyte-agents-benchmark` | ❌ 禁嵌客户包；❌ Elv2 改后勿闭源分发；✅ 仅内部基准 | 指标对齐 AOS SLA；可定位瓶颈 | AIP-07 |

SSH（登记用）：

| # | 仓 | SSH | License |
| --- | --- | --- | --- |
| 8 | OpenSearch | `git@github.com:opensearch-project/OpenSearch.git` | Apache 2.0 ✅ |
| 9 | OTel Collector | `git@github.com:open-telemetry/opentelemetry-collector.git` | Apache 2.0 ✅ |
| 10a | fastmcp-airbyte | `git@github.com:airbytehq/fastmcp-airbyte.git` | MIT ✅ |
| 10b | fastmcp-extensions | `git@github.com:airbytehq/fastmcp-extensions.git` | MIT ✅ |
| 11 | airbyte-agents-benchmark | `git@github.com:airbytehq/airbyte-agents-benchmark.git` | MIT/Elv2 ⚠️ |

---

#### 8 · OpenSearch（Object 全文附属检索）

**一句话定位：** 全文检索备胎；**绝不碰 Object 主存**；只做模糊/关键词加速。

**在 AOS 的价值：** 补 AGE（图主存，§3.2 已拉）短板——AGE 擅关联遍历；OpenSearch 擅模糊/同义词/高亮。协议 Apache 2.0（Elastic fork），避开 SSPL。

**链路位置：**

```text
用户关键词 → OpenSearch（name/description/remark/wiki_content 文本副本）
                 ↓ 命中 Object ID
AGE 主存 ← 按 ID 取完整属性 + Link
                 ↓
Workshop / 工作台渲染
```

**与已有组件边界：**

| 组件 | 边界 |
| --- | --- |
| **AGE + Iceberg** | **主存**永远在此；OpenSearch 只做检索副本 |
| **Langfuse** | 可选把 Trace 文本同步到 OpenSearch 做「搜历史决策」；Trace **主存仍 Langfuse** |
| **L1 Pipeline** | 索引数据由 Pipeline **主动推送**；禁止 OpenSearch 回写 Object |

**启用触发（P2→可排 P1）：** 满足任一即可考虑拉取/部署——① 企业文档量 ≥10 万且现有 RAG 准确率 &lt;85%；② 客户明确要同义词/拼音/高亮等；③ 需向 OA 等第三方开放 Object 检索。

**二开注意：** 只读索引；字段精简仅 `name`/`description`/`remark`/`wiki_content`，单条 ≤10KB；禁止索引纯度/设备状态等核心属性。

---

#### 9 · OpenTelemetry Collector（统一可观测采集）

**一句话定位：** 全链路采集管道；降低各组件对接 Langfuse/Prometheus 的 SDK 侵入。

**在 AOS 的价值：** Funnel / AIP Logic / Workshop 后端 / Apollo Spoke /（可选）消息总线 → 统一 OTel 协议 → Collector → Trace→Langfuse · Metrics→Prometheus · Logs→OpenSearch（可选）。对齐 T-CROSS **X-05**。

**与已有组件边界：**

| 组件 | 边界 |
| --- | --- |
| **Langfuse / Prometheus** | **存储与产品语义**在彼；OTel **不存数据** |
| **Grafana** | 只读 Prom；OTel **不参与可视化** |
| 各业务服务 | 只接 OTel SDK/Agent，不各自硬绑多家后端 SDK |

**启用触发：** ① 需排跨组件延迟（如 Funnel 慢在 CDC 还是总线）；② 客户要全链路 SLA 报告；③ 需对接客户自研监控后端。

**二开注意：** 采集规则宜热更新；生产默认 Trace 采样 **10%**，排障临时 100%；Apache 2.0 可商用。

---

#### 10 · fastmcp-airbyte（+ fastmcp-extensions）

**一句话定位：** Airbyte 官方 MCP Server 封装；AOS 做 MCP 兼容时的 **参考范本**，非主路径。

**关系：** `fastmcp-extensions` = FastMCP 企业向基础能力（认证/流式/多租户等）；`fastmcp-airbyte` = 在其上把 Connector 封成 MCP Tool。二者 **配套**，拉参考时同拉。

**在 AOS 的价值：** 主路径 Tool Registry **自研**（Ontology Object / Action / Connector → Agent Tool）。若客户已用 Claude Desktop / Cursor 等 MCP 客户端要直连 AOS，则参考本仓把自有 Registry **适配 MCP**，而非从零发明协议细节。

**启用触发：** ① 客户明确要求 AOS 作 MCP 数据接入层；② 需向第三方 MCP 客户端开放 Connector/Action。

**二开注意：** **禁止**产品代码直接依赖本仓逻辑；MCP Server 必须自研；只对齐 Tool Schema / 流式返回；MIT 可参考。

---

#### 11 · airbyte-agents-benchmark（Agent 评测旁路）

**一句话定位：** Agent **性能**基准工具；是 **promptfoo（§3.2 已拉）业务 Evals 的旁路补充**。

**分工：**

| 工具 | 管什么 |
| --- | --- |
| **promptfoo** | 业务门控：推荐是否合规、答案是否达 SOP（AIP-07 主路径） |
| **airbyte-agents-benchmark** | 性能旁路：Tool 成功率、延迟、Token；模型/路由对比 |

**启用触发：** ① 需出具 Agent 性能 SLA；② 优化 Tool/模型路由需基准数据；③ 客户要求性能第三方审计。

**二开注意：** **仅内部**；**禁止**嵌入客户交付包；Elv2 限制「修改后闭源分发」——内部评测不分发则风险可控；指标与 AOS SLA 对齐（成功率/延迟/Token）。

---

#### 2.3.1 P2 整体使用原则（与 21 选型自洽）

1. **默认只登记/star，不强制拉取**；即使拉了也只进 `refs/`，不 submodule 进主工程。  
2. **触发式启用：** 有明确业务需求再升排期（可记为 P2→P1），再做适配。  
3. **非核心依赖：** 不得成为 L1～L3 / AIP / Apollo **主路径**硬依赖，避免被上游迭代绑死。  
4. **军规：** 仍遵守 [23](23-AOS开源引用与交付军规.md)；AGPL/BSL 规则不变；P2 参考仓同样禁止进客户包编译链。

---

## 3. 已拉仓一览表（目录 · SSH · License）

> 与 `mybuddy-v01/` 现网目录对齐；**含全部已 clone 仓**（A*/B*/… + `refs/`）。

### 3.1 `refs/`（clone_aos_deps · 已拉）


| 目录                   | 仓             | SSH                                         | License        | 维护备注                                          |
| -------------------- | ------------- | ------------------------------------------- | -------------- | --------------------------------------------- |
| `refs/ocr/` | **PaddleOCR** | `git@github.com:PaddlePaddle/PaddleOCR.git` | Apache 2.0 | L1-04；`parser-pdf-ocr` **独立进程**；2026-07-17 核盘 |
| `refs/objstore/` | **minio** | `git@github.com:minio/minio.git` | **AGPL v3** ⚠️ | L1-06 参考；**交付不捆**；客户先装见 24 |
| `refs/objstore-sdk/` | **minio-py** | `git@github.com:minio/minio-py.git` | Apache 2.0 | S3Adapter SDK 参考 |
| `refs/seaweedfs/` | **seaweedfs** | `git@github.com:seaweedfs/seaweedfs.git` | Apache 2.0 | L1-06 大规模对象仓备选；Apache 友好于 MinIO AGPL；2026-07-17 核盘 |
| `refs/tesseract/` | **tesseract** | `git@github.com:tesseract-ocr/tesseract.git` | Apache 2.0 | L1-04 轻量/英文 OCR 备选插件；2026-07-17 核盘 |


### 3.2 `A1`～`F2`（clone_mybuddy_repos / airbyte_refs · 已拉）


| 目录                       | 仓                          | SSH                                                       | License        | 维护备注                |
| ------------------------ | -------------------------- | --------------------------------------------------------- | -------------- | ------------------- |
| `A1_ETL/`                | meltano                    | `git@github.com:meltano/meltano.git`                      | Apache 2.0     | 插件协议参考              |
| `A1_ETL/`                | pyairbyte                  | `git@github.com:airbytehq/pyairbyte.git`                  | MIT/Elv2       | 轻量抽数                |
| `A1_ETL/`                | airbyte-python-cdk         | `git@github.com:airbytehq/airbyte-python-cdk.git`         | MIT/Elv2       | 自研连接器 CDK           |
| `A3_CDC/`                | debezium                   | `git@github.com:debezium/debezium.git`                    | Apache 2.0     | CDC；总线见 §2.2        |
| `A4_Lakehouse/`          | iceberg                    | `git@github.com:apache/iceberg.git`                       | Apache 2.0     | Dataset 表格式         |
| `A4_Lakehouse/`          | duckdb                     | `git@github.com:duckdb/duckdb.git`                        | MIT            | 开发/小规模查询            |
| `B1_GraphStore/`         | age                        | `git@github.com:apache/age.git`                           | Apache 2.0     | **v1 默认图**          |
| `B1_GraphStore/`         | nebula                     | `git@github.com:vesoft-inc/nebula.git`                    | Apache 2.0     | 规模备选                |
| `B1_GraphStore/`         | memgraph                   | `git@github.com:memgraph/memgraph.git`                    | **BSL** ⚠️     | 发行包装；不嵌代码           |
| `B3_GraphViz/`           | G6                         | `git@github.com:antvis/G6.git`                            | MIT            | 知识图谱建议              |
| `B3_GraphViz/`           | cytoscape.js               | `git@github.com:cytoscape/cytoscape.js.git`               | MIT            | 备选                  |
| `B4_Metadata/`           | linkml                     | `git@github.com:linkml/linkml.git`                        | Apache 2.0     | Meta DSL 思路         |
| `B5_Workflow/`           | temporal                   | `git@github.com:temporalio/temporal.git`                  | MIT            | 编排建议                |
| `B5_Workflow/`           | conductor                  | `git@github.com:Netflix/conductor.git`                    | Apache 2.0     | 备选                  |
| `B7_Wiki/`               | outline                    | `git@github.com:outline/outline.git`                      | **BSL** ⚠️     | **只参考 UX**；宜视作 refs |
| `B7_Wiki/`               | wiki                       | `git@github.com:Requarks/wiki.git`                        | **AGPL v3** ⚠️ | 只参考；不嵌              |
| `C1_ModelRouter/`        | litellm                    | `git@github.com:BerriAI/litellm.git`                      | MIT            | Gateway 边车          |
| `C2_Evals/`              | promptfoo                  | `git@github.com:promptfoo/promptfoo.git`                  | MIT            | Evals harness       |
| `C3_Trace/`              | langfuse                   | `git@github.com:langfuse/langfuse.git`                    | Apache 2.0     | Trace 边车            |
| `C5_AgentOrchestration/` | langgraph                  | `git@github.com:langchain-ai/langgraph.git`               | MIT            | Logic 参考            |
| `C5_AgentOrchestration/` | airbyte-agent-sdk          | `git@github.com:airbytehq/airbyte-agent-sdk.git`          | MIT/Elv2       | Tool 模式参考           |
| `C5_AgentOrchestration/` | airbyte-agent-cli          | `git@github.com:airbytehq/airbyte-agent-cli.git`          | MIT/Elv2       | 研发工具                |
| `C8_RightEngine/`        | qdrant                     | `git@github.com:qdrant/qdrant.git`                        | Apache 2.0     | 向量按需                |
| `C8_RightEngine/`        | milvus                     | `git@github.com:milvus-io/milvus.git`                     | Apache 2.0     | 大规模向量               |
| `D1_WorkshopFactory/`    | ToolJet                    | `git@github.com:ToolJet/ToolJet.git`                      | **AGPL v3** ⚠️ | **只参考交互**           |
| `D1_WorkshopFactory/`    | appsmith                   | `git@github.com:appsmithorg/appsmith.git`                 | Apache 2.0     | Widget 思路备选         |
| `D3_HighPerfGrid/`       | ag-grid                    | `git@github.com:ag-grid/ag-grid.git`                      | MIT / 企业版付费    | 社区版起步               |
| `D4_Map/`                | kepler.gl                  | `git@github.com:keplergl/kepler.gl.git`                   | MIT            | COP 地图              |
| `E1_GitOps/`             | argo-cd                    | `git@github.com:argoproj/argo-cd.git`                     | Apache 2.0     | ≠ Apollo 产品         |
| `E1_GitOps/`             | terraform-provider-airbyte | `git@github.com:airbytehq/terraform-provider-airbyte.git` | MIT/Elv2       | IaC 远期              |
| `E3_Secrets/`            | vault                      | `git@github.com:hashicorp/vault.git`                      | **BSL** ⚠️     | 发行包装；不嵌源码           |
| `E4_AirGap/`             | skopeo                     | `git@github.com:containers/skopeo.git`                    | Apache 2.0     | Ferry 镜像            |
| `E7_Observability/`      | prometheus                 | `git@github.com:prometheus/prometheus.git`                | Apache 2.0     | Probe 指标            |
| `F1_Identity/`           | keycloak                   | `git@github.com:keycloak/keycloak.git`                    | Apache 2.0     | IdP                 |
| `F2_Authz/`              | openfga                    | `git@github.com:openfga/openfga.git`                      | Apache 2.0     | Authz 边车            |


**刻意不拉：** `airbytehq/airbyte` monorepo · `airbyte-cdk-java` · `airbyte-api-java-client`（见 `clone_airbyte_refs.ps1`）。

---

## 4. 补拉脚本用法

```powershell
cd c:\work\projects\wchat\mybuddy-v01

# P0 主三项已在 §3；再跑会 SKIP exists
.\clone_aos_deps.ps1 -Tier P0

# 未拉：Grafana / Redis / cosign
.\clone_aos_deps.ps1 -Tier P1

# 未拉：MCP / benchmark
.\clone_aos_deps.ps1 -Tier P2

# P0 主项 + 可选（Tesseract/SeaweedFS）已在 §3；再跑会 SKIP
.\clone_aos_deps.ps1 -Tier P0 -IncludeOptional
```


| 脚本                        | 职责                           |
| ------------------------- | ---------------------------- |
| `clone_mybuddy_repos.ps1` | A1～F2 主参考树                   |
| `clone_airbyte_refs.ps1`  | Airbyte 轻量仓（禁 monorepo）      |
| `**clone_aos_deps.ps1**`  | §2 未拉项 → `refs/`；成功后维护人迁入 §3 |


---

## 5. 与 21 / T05 交叉钉


| 主题         | 钉                                                    |
| ---------- | ---------------------------------------------------- |
| OCR        | 默认 PaddleOCR（§3.1）；备选 **Tesseract**（§3.1 已拉）；`parser-pdf-ocr` **独立进程**（T05） |
| MediaSet   | minio/minio-py + **SeaweedFS**（§3.1 已拉）；交付不捆 MinIO 服务端；`S3Adapter`；客户先装见 24 |
| MCP / P2 | 详见 **§2.3**（OpenSearch / OTel / fastmcp* / agents-benchmark）；默认不阻塞主链路 |
| Wiki / 低代码 | Outline BSL · ToolJet AGPL → 只参考（§3.2） |
| Ferry | Skopeo（§3.2 已拉）+ cosign（仍 §2.2） |


---

## 6. 修订记录


| 版本   | 日期         | 说明                                                   |
| ---- | ---------- | ---------------------------------------------------- |
| v1.0 | 2026-07-17 | 首版：P0～P2 缺口 · 全量 SSH/License · refs · clone_aos_deps |
| v1.1 | 2026-07-17 | 挂 23 军规 · 24 客户前置 SOP · examples/customer-prereq     |
| v1.2 | 2026-07-17 | 核盘：P0 三仓已入 refs/                                     |
| v1.3 | 2026-07-17 | 结构调整：已拉项迁 §3.1；§2 仅保留未拉 |
| v1.4 | 2026-07-17 | SeaweedFS ✅ `refs/seaweedfs` 迁入 §3.1 |
| v1.5 | 2026-07-17 | Tesseract ✅ `refs/tesseract` 迁入 §3.1；§2.1 清空 |
| v1.6 | 2026-07-17 | §2.3 扩写 P2 四组件：定位/链路/边界/触发/二开红线/验收；配套 principles |

---

*22 · 已拉进 §3 · 缺口只留 §2 · P2 非核心按需 · 强制见 23 · 客户先装见 24*
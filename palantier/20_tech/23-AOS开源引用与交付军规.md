# 23 · AOS 开源引用与交付军规

> **文档性质**：**强制军规**（违反即阻断合并 / 阻断发版 / 阻断现场打包）  
> **版本**：v1.0 · 2026-07-17  
> **状态**：已生效 · 研发 / CI / 实施 / 法务共用  
> **配套**：[22 开源产品维护清单](22-AOS开源产品维护清单.md)（仓址证照）· [24 客户侧前置 SOP](24-AOS客户侧前置组件安装SOP.md)（客户先装）· [21 选型总表](21-AOS开源选型与功能清单.md)  
> **原则来源**：开源=参考；产品壳自有；AGPL/BSL 不进交付包；客户环境先就绪再装 AOS

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 中文 | 军规条文中文；CI 可用英文日志 |
| 军规优先于便利 | 现场「顺手打包」一律否决 |
| 可执行 | 每条对应检查方式（人工或 CI） |
| 与 22/24 一致 | 仓址看 22；安装顺序看 24 |

---

## 0. 一句话军规

```text
客户环境先装「前置组件」（按 24 SOP）；
AOS 交付包只含自有软件 + 适配配置 + 安装/对接指引；
禁止把 AGPL/BSL 服务端源码或二进制捆进 AOS 客户包；
产品代码禁止依赖 refs/ 与 AGPL UX 参考仓路径。
```

---

## 1. 目录与依赖军规（研发）

| ID | 军规 | 检查 |
| --- | --- | --- |
| **R-DIR-01** | 产品运行时仅 `aos-*` / `apps/` / `services/` / `packages/` / `mybuddy-v01/desktop|adapter|openocta-overlay`（目标态以自有仓为准） | 目录评审 |
| **R-DIR-02** | `refs/` = 只读参考；**禁止**被产品编译、打包、Docker `COPY` 进运行镜像 | CI 路径扫描 |
| **R-DIR-03** | AGPL/BSL 上游（ToolJet / Wiki.js / Outline / MinIO 服务端源码 / Grafana 源码等）视为 **refs 语义**；即使物理仍在 `B7_Wiki/`·`D1_*`，也 **禁止** 作为构建依赖 | CI 黑名单（见 §5） |
| **R-DIR-04** | Apache2/MIT 参考仓（`A1_*`…`F2_*`）允许「读模式 / 边车进程」；**禁止**「基于 XXX 二次开发」对外话术与发行壳 | 发布文案审查 |
| **R-DIR-05** | `ClaudeSkills/` 永不进交付包 | 打包清单 |

**黑名单路径（产品工程 import / COPY 禁止）：**

```text
**/refs/**
**/B7_Wiki/outline/**
**/B7_Wiki/wiki/**
**/D1_WorkshopFactory/ToolJet/**
**/D1_WorkshopFactory/appsmith/**   # 即使 Apache，也不作产品壳依赖；仅允许本地对照
```

> Appsmith 许可宽松，但仍 **不得** 当 AOS 发行壳；军规按「低代码参考仓」一视同仁进黑名单，避免壳漂移。

---

## 2. License / 分发军规（交付）

| ID | 军规 | 适用 |
| --- | --- | --- |
| **R-LIC-01** | **AGPL 服务端**（MinIO Server、Grafana 等）**不得**进入 AOS 客户交付包（含镜像、安装器、离线包） | 发版门禁 |
| **R-LIC-02** | AGPL 组件采用：**客户自装发行包** + AOS **适配层/配置**；交付物可含安装指引与 Dashboard JSON（配置≠衍生作品） | 24 SOP |
| **R-LIC-03** | **BSL**（Vault、Outline、Memgraph、Redpanda 等）：不嵌源码进产品；生产用发行包/客户侧部署；商用条款法务备案后再签合同 | 法务 |
| **R-LIC-04** | 允许链路：Apache2 / MIT / BSD 等组件作 **边车或库依赖** 时，须登记进 [22](22-AOS开源产品维护清单.md) 并做 SBOM | 发版 |
| **R-LIC-05** | 「顺手把 MinIO/Grafana 打进 AOS 包方便客户」= **违规**；一律改为 24 SOP 前置安装 | 实施 |

---

## 3. 架构引用军规（代码）

| ID | 军规 | 检查 |
| --- | --- | --- |
| **R-ARCH-01** | UI / Desktop **只**调 `aos-api`；禁止直连 LiteLLM / Airbyte / 厂商 LLM SDK / OpenFGA / Vault API（经自有 Facade） | import 扫描 |
| **R-ARCH-02** | OCR：`parser-pdf-ocr` **独立进程**；禁止把 Paddle 重依赖链入 aos-api 主进程 | 架构评审 + 进程清单 |
| **R-ARCH-03** | 对象存储：只依赖自有 **`S3Adapter`**；Dev 可指 MinIO endpoint；Prod 可指客户 S3/兼容仓 | 配置契约 |
| **R-ARCH-04** | Wiki / 低代码：只抄交互到自有 UI（foundry/html）；**禁止** cherry-pick AGPL 仓文件进产品树 | CODEOWNERS / diff 审查 |
| **R-ARCH-05** | 试用脑 `dify`/`openocta` 仅 v0.1 Adapter 路径；目标态新功能不得扩大对其 UI 依赖 | T-EVO |

---

## 4. 安装顺序军规（实施）

| ID | 军规 | 说明 |
| --- | --- | --- |
| **R-INST-01** | **先客户前置，后 AOS**。未完成 [24 SOP](24-AOS客户侧前置组件安装SOP.md) 检查清单，不得开始 AOS 安装 | 实施门禁 |
| **R-INST-02** | 前置组件的安装、升级、备份、高可用 **默认客户 IT 责任**；AOS 提供版本矩阵与验收探针 | 24 |
| **R-INST-03** | AOS 安装程序只做：连通性探测 → 写入 endpoint/secret-ref → 拉起自有服务；**不**静默安装 MinIO/Grafana/Vault 服务端进客户包 | 安装器设计 |
| **R-INST-04** | Lite / Full / 气隙 三套前置矩阵分表维护（见 24）；现场变更必须回写 24「变更日志」 | 活文档 |

---

## 5. CI / 发版门禁（必须落地）

> 下列门禁在目标态工程仓启用；v0.1 过渡期至少启用 **扫描告警**，v0.5+ **失败即阻断**。

| 门禁 | 动作 | 阻断级 |
| --- | --- | --- |
| **路径黑名单** | PR 若新增对 §1 黑名单路径的引用/COPY | v0.5+ 失败 |
| **SBOM** | 发版产物生成 SBOM；命中 AGPL **服务端**组件名/镜像 | 失败 |
| **镜像扫描** | 客户交付镜像禁止 `minio/minio`、`grafana/grafana` 等作为 **必选层**（文档示例 Compose 可放 `docs/examples`，标注「客户侧」） | 失败 |
| **import 扫描** | 禁止 UI 直连上游 SDK（R-ARCH-01） | v0.3+ 失败 |
| **文案扫描** | 发布说明禁止「基于 ToolJet/MinIO/Dify 的平台」类表述 | 人工+关键词 |

**允许的例外（须书面注明）：**

- 内部 Dev Compose 可起 MinIO/Grafana，文件路径限定 `deploy/dev/` 或 `docs/examples/customer-prereq/`，**不得**打进 `dist/customer/`。
- 客户已购买商业许可的特例：法务邮件存档后，可在 SOP 该客户附录放宽，**不得**改全球默认军规。

---

## 6. 角色责任

| 角色 | 必须遵守 |
| --- | --- |
| 研发 | R-DIR / R-ARCH；不把 refs 当库 |
| CI 维护 | §5 门禁脚本与基线 |
| 实施 / FDE | R-INST；先跑 24 检查单再装 AOS |
| 产品 / 销售 | 不承诺「一体包含 MinIO/Grafana」 |
| 法务 | BSL/AGPL 合同与例外备案 |

---

## 7. 违规处理

| 级别 | 示例 | 处理 |
| --- | --- | --- |
| P0 | 客户包内含 MinIO/Grafana 服务端 | 停发版；剔除后重打；复盘 |
| P1 | 产品代码 import ToolJet 路径 | PR 拒绝；限期清理 |
| P2 | 文档话术「基于 XXX」 | 改文案；记一次评审债 |

---

## 8. 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-07-17 | 首版军规：目录/License/架构/安装顺序/CI 门禁 |

---

*23 · 军规生效 · 先前置后 AOS · AGPL 不进包 · refs 不进编译*

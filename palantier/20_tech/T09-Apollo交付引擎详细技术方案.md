# T09 · Apollo 交付引擎详细技术方案

> **版本**：v1.0.2 · 2026-07-17  
> **状态**：✅ **方案完成**  
> **对齐产品**：[09](../09-Apollo交付引擎产品方案.md) · [09a](../09a-Apollo交付引擎产品设计线框图.md) · [20 §6.6](20-AOS整体技术方案.md) · OPS-001～**010** · [T-API](T-API-aos-api稳定契约.md) · [T-CROSS](T-CROSS-横切能力详细技术方案.md) · [21](21-AOS开源选型与功能清单.md) · [23 军规](23-AOS开源引用与交付军规.md) · [24 前置 SOP](24-AOS客户侧前置组件安装SOP.md)  
> **UI**：`apollo-*.html` + `workshop-publish.html`（v1.6 已齐）

---

## 使用的 Rules

产品对齐 · UI 引用 apollo-* · 密钥禁明文 · Lite Spoke 优先于 Full 舰队膨胀 · 开源=GitOps/密钥参考 · **先前置后 AOS**（24）· **AGPL 不进包**（23）

---

## 0. 安装顺序（强制 · 对齐 24）

```text
客户按 24 SOP 完成前置总检并签署
  → AOS / Lite Spoke 安装器：只读探针 + 写 secret-ref
  → 拉起自有服务（Catalog / Agent / Probe）
  → 禁止安装器静默安装 MinIO / Grafana / Vault 服务端进「AOS 包」
```

交接文件示例：[`docs/examples/customer-prereq/prereq-handoff.example.yaml`](../../examples/customer-prereq/prereq-handoff.example.yaml)

---

## 1. 范围与分期

| 阶段 | 做 | 说明 |
| --- | --- | --- |
| **P0** | Lite Spoke（OPS-010）· 出站轮询 · Catalog 最小 · Asset Bundle · Vault/KMS 注入 · 紧急 hotfix | 无 K8s 专家可装 |
| **P1** | Full Spoke · Release Channel 晋升/Recall · Change Management | 多环境 |
| **P2** | Ferry 气隙 · 舰队大盘增强 | 专网/断网 |

**非目标：** 「装了 Argo CD = Apollo 产品」。

---

## 2. 架构

```text
apollo-control (Hub)
├── Catalog / Products / Channels
├── Plan / Constraints / Promotion / Recall
├── Asset Bundle Registry
├── Change Management
└── Config Override (non-secret) + Secret refs

Spoke Agent (客户侧)
├── 出站 HTTPS 轮询 Hub
├── 拉 Plan / Artifact / Asset Bundle
├── 本地执行（Compose 或 Helm）
└── Probe + Reported State
```

**连接模型（强制文案）：** Spoke **主动出站**；**不要求**客户给 Hub 开入站端口。

---

## 3. OPS 映射（实现要点）

| OPS | 能力 | 实现要点 | UI |
| --- | --- | --- | --- |
| 001 | 制品入库 | Manifest/镜像进 Catalog | assets/release |
| 002 | 私有化部署 | Spoke 拉 Plan 执行 | spoke |
| 003 | 配置下发 | Override 非密钥 | config |
| 004 | Channel + Recall | 健康达标晋级；失败召回 | release |
| 005 | 配置覆盖 | 与密钥分离 | config |
| 008 | **Asset Bundle** | OKF/Module/Agent 打包；**与平台 Channel 版本同绑** | assets |
| 009 | 审计 + Change Mgmt + 紧急发布事后审计 | 审批单 · hotfix 标记 | change-mgmt / release |
| **010** | **Lite Spoke** | Docker Compose 单节点；同 Catalog 契约 | spoke（Full/Lite 切换） |

---

## 4. Lite Spoke vs Full

| 项 | Lite | Full |
| --- | --- | --- |
| 运行时 | Compose | K8s/Helm |
| 轮询/密钥注入/升级 | ✅ | ✅ |
| 舰队/Delta/Ferry | 分期 | ✅ |

验收：无 K8s 专家能完成一次平台升级 + 一次 Asset Bundle。

---

## 5. 密钥与交付底座

### 5.0 自有所需功能（先于开源）

| 功能项 | 我们要什么 | 验收 |
| --- | --- | --- |
| Hub Catalog | Product / Channel / Artifact / Asset Bundle 入库 | OPS-001 |
| Plan / Constraints | 出站轮询拉 Plan；维护窗/依赖约束 | 窗外非紧急不强制升 |
| Channel / Recall | 健康晋升；失败自动召回 | OPS-004 |
| Lite Spoke | Compose 单节点；同 Catalog 契约 | 无 K8s 可装可升 |
| Full Spoke | K8s/Helm（分期） | P1 |
| Config Override | 非密钥覆盖；与密钥分离 | 只显示 ref |
| 密钥注入 | Vault/KMS ref；Lite 密封文件解锁 | 禁明文扫描通过 |
| Change Mgmt | 环境设定/紧急发布审批 + 审计 | OPS-009 |
| Asset Bundle | OKF/Module/Agent 与 Channel 同绑 | HR-03 |
| Ferry | 签名 tar.gz + manifest 气隙摆渡 | 缺签名拒导入 |
| Probe / Reported State | 版本·健康·遥测回报 | 舰队可见 |

### 5.1 密钥规则

| 规则 | 实现 |
| --- | --- |
| 禁明文 | Override/Manifest/Git 不得出现密码/Key |
| 注入 | HashiCorp Vault 或客户 KMS；Lite 可用密封文件+启动解锁 |
| UI | 只显示 ref |

### 5.2 开源参考（已核对）

| 仓 | 路径 | 抄 | 不抄 | 选型 |
| --- | --- | --- | --- | --- |
| Vault | `E3_Secrets/vault` | 密钥引擎、租约、动态密钥 | Vault UI=Apollo | **建议**密钥引擎 |
| Argo CD | `E1_GitOps/argo-cd` | 同步/健康/回滚思路 | 「Argo=Apollo」 | Full Spoke **参考**；产品控制面自有 |
| Skopeo | `E4_AirGap/skopeo` | 镜像拷贝/气隙 | 产品壳 | **建议** Ferry 镜像层 |
| Prometheus | `E7_Observability/prometheus` | Spoke Probe 指标 | 替代 Reported State 产品语义 | **建议**指标 |
| terraform-provider-airbyte | `E1_GitOps/terraform-provider-airbyte` | IaC 管 Connection 远期参考 | 绑 Airbyte 云 | P2 可选 |
| （缺）cosign / notation | — | 制品签名校验 | — | **建议补拉** 配合 Ferry 签名 |
| （缺）Helm | — | Full Spoke 包格式参考 | Helm 当产品 | Full 阶段再拉 |

---

## 6. 紧急发布

- `hotfix` Channel；事后合并回 `stable`  
- 须进 Change Management / 审计（OPS-009）  
- **UI：** [`apollo-release.html`](../foundry/html/apollo-release.html)

---

## 7. Asset Bundle

| 内容 | 来源 |
| --- | --- |
| OKF / Ontology 片段 | L2 |
| Module | L3 |
| Agent/Logic/Evals 快照 | AIP |
| `assetSemVer` + 兼容 Channel 区间 | 元数据 |

平台晋升时绑定资产版本一并决议（HR-03）。

**UI：** [`apollo-assets.html`](../foundry/html/apollo-assets.html)

---

## 8. UI 蓝图全表

| 能力 | html |
| --- | --- |
| Hub 舰队 | [`apollo-hub.html`](../foundry/html/apollo-hub.html) |
| Release / hotfix | [`apollo-release.html`](../foundry/html/apollo-release.html) |
| Spoke / Lite / 出站 | [`apollo-spoke.html`](../foundry/html/apollo-spoke.html) |
| Ferry | [`apollo-ferry.html`](../foundry/html/apollo-ferry.html) |
| Asset Bundle | [`apollo-assets.html`](../foundry/html/apollo-assets.html) |
| Change Mgmt | [`apollo-change-mgmt.html`](../foundry/html/apollo-change-mgmt.html) |
| Config / Vault ref | [`apollo-config.html`](../foundry/html/apollo-config.html) |
| 工作台入口 | [`workshop-publish.html`](../foundry/html/workshop-publish.html) |

> UI 线框规格见 [09a](../09a-Apollo交付引擎产品设计线框图.md) **v1.0**；**实现以 09a + html + 本文为准**。

---

## 9. IdP 与多租户

身份 / 授权 / Org·Project 见 **[T-CROSS](T-CROSS-横切能力详细技术方案.md)**（已定稿）。Apollo 资源一律带 `org_id`。

### 9.1 Ferry 介质格式（已决）

```text
ferry-bundle-{env}-{timestamp}.tar.gz
├── manifest.json     # version, channel, artifacts[], signatures[], createdAt
├── artifacts/        # 镜像 archive 或 helm chart tgz
├── assets/           # 可选 Asset Bundle
├── checksums.sha256
└── signature.sig     # 对 manifest 的签名（客户侧校验公钥）
```

| 规则 | 说明 |
| --- | --- |
| 传输 | 物理介质 / 单向摆渡网；Hub 与 Spoke 均可 export/import |
| 校验 | 先签名后校验和；失败拒导入 |
| UI | [`apollo-ferry.html`](../foundry/html/apollo-ferry.html) |

---

## 10. 验收

| # | 标准 |
| --- | --- |
| A1 | Lite Spoke 文档化安装成功并回报 Probe |
| A2 | 配置中无明文密钥（扫描） |
| A3 | hotfix 通道可发并留审计 |
| A4 | Asset Bundle 与 Channel 同绑校验失败则拒升 |
| A5 | 安全问答：不要求客户开入站 |
| A6 | Ferry 包缺签名不可导入 |

---

## 11. 已决结论（原缺口已关闭）

| ID | 结论 |
| --- | --- |
| T09-G1 | Ferry = **签名 tar.gz + manifest**（§9.1） |
| T09-G2 | 多租户 = **Org/Project**（T-CROSS §5）；Apollo 全资源带 org_id |

---

*T09 v1.0 · docs/palantier/20_tech*

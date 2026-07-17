# AI操作系统 · AOS 企业AI转型方案

> **侧栏品牌**  
> 第一行：**AI操作系统**  
> 第二行：**AOS 企业AI转型方案**  
> **覆盖**：工作台 L3 → AIP 决策引擎 → 本体数字孪生 → 数据操作系统 → **交付 Apollo**  
> **概览叙事**：使用优先（工作台置顶，底座在下）；分区卡片顺序与侧栏一致，**Apollo 在数据集成之后**（运维发布，不插业务链中间）。  
> 对齐 [05a](../../05a-数据集成Connectors-Pipeline-Dataset产品设计线框图.md) · [06a](../../06a-语义本体Ontology-Mapping产品设计线框图.md) · [07a](../../07a-AIP引擎产品设计线框图.md) · [08a](../../08a-Workshop产品设计线框图.md) · [09](../../09-Apollo交付引擎产品方案.md) · [09a](../../09a-Apollo交付引擎产品设计线框图.md) · [03 AOS PRD](../../03-对标Palantir-AOS-PRD框架.md)  
> **施工真源**：[HTML补页改页任务清单.md](./HTML补页改页任务清单.md)

## 如何本地打开

1. 进入：`c:\work\projects\wchat\docs\palantier\foundry\html\`
2. 双击 `index.html`（Chrome / Edge）。
3. 侧栏顺序：**概览** → **工作台 L3** → **AIP** → **本体** → **数据集成** → **交付 Apollo**。

```bash
cd c:\work\projects\wchat\docs\palantier\foundry\html
python -m http.server 8080
```

访问：**http://localhost:8080/index.html**

## 版本

**v1.6.5** · Appearance **全站**：浅色 / 深色 / 跟随系统（顶栏「外观」）


## 模块映射（线框 → Demo）

### 工作台 · 08a

| 线框 | Demo | 状态 |
| --- | --- | --- |
| WF-WS-01 | `workshop.html` | ✅ |
| WF-WS-02 | `workshop-canvas.html` | ✅ |
| WF-WS-03 | `workshop-module.html` | ✅ 含 Selection≤10 / 分页 / Marking / 幂等 |
| WF-WS-04/05 | `workshop-object-view.html` | ✅ |
| WF-WS-06/07 | `workshop-aip-chat.html` | ✅ 含决策谱系链 |
| WF-WS-08 | `workshop-cop.html` | ✅ |
| WF-WS-09 | `workshop-publish.html` | ✅ → Apollo |
| WF-WS-10 | `workshop-module-interface.html` | ✅ P2 |
| WF-WS-11 | `workshop-events.html` | ✅ P2 |

### AIP · 07a

| 线框 | Demo | 状态 |
| --- | --- | --- |
| WF-AIP-00 | `aip-maturity.html` | ✅ 熔断 / 预热 |
| WF-AIP-01 | `aip-model-router.html` | ✅ 路由策略 |
| WF-AIP-01a | `aip-model-providers.html` | ✅ **v1.6.2** 供应商接入（卡片+类型化表单） |
| WF-AIP-05C | `aip-capabilities.html` | ✅ **v1.6.3** 重能力接入（07b） |
| WF-AIP-02 | `aip-logic.html` | ✅ Edits 合并 / Draft |
| WF-AIP-05 | `agents.html` | ✅ Chatbot Studio |
| WF-AIP-05T | `aip-tools.html` | ✅ Wiki Tool |
| WF-AIP-06 | `aip-draft-inbox.html` | ✅ 含 **Insight Backfill** |
| WF-AIP-07 | `aip-decision-lineage.html` | ✅ 含回填节点 |
| WF-AIP-08 | `aip-evals.html` | ✅ |
| WF-AIP-09 | `workshop-aip-chat.html` | ✅ 合页 |

### 本体 · 06a / Wiki

| 线框 | Demo | 状态 |
| --- | --- | --- |
| WF-OM-01~08 | `ontology*.html` | ✅ 含 Action/Function/Link 护栏 |
| WF-OM-09 | `ontology-graph-health.html` | ✅ **v1.6.1 补页** |
| WF-FN-01 | `funnel.html` · `okf-funnel.html` | ✅ 含 **Constitution** |
| WIKI-001~004 | `ontology-wiki.html` | ✅ 双向 A/B |

### 数据集成 · 05a

| 线框 | Demo | 状态 |
| --- | --- | --- |
| WF-DC-01~04b | `data-connection` / `source-*` / `sync*` | ✅ 含 128KB 短路 |
| WF-DC-05 | `data-connection-agents.html` | ✅ 边缘代理 |
| WF-PB-01~03 | `pipeline*` / `pipeline-doc-intel` | ✅ 含 DLQ |
| WF-PB-02b | `pipeline-proposals.html` | ✅ |
| WF-SC-01 | `schedules.html` | ✅ |
| WF-CR-01 | `code-repositories.html` | ✅ P2 |
| WF-BL/DS/MS/LN/DH | `builds` / `dataset` / `media-sets` / `lineage` / `health` | ✅ |

### Apollo · 09a

| 线框 | Demo | 状态 |
| --- | --- | --- |
| WF-AP-01 | `apollo-hub.html` | ✅ |
| WF-AP-02 | `apollo-release.html` | ✅ hotfix |
| WF-AP-03 | `apollo-spoke.html` | ✅ 出站 / Lite |
| WF-AP-04 | `apollo-ferry.html` | ✅ |
| WF-AP-05 | `apollo-assets.html` | ✅ |
| WF-AP-06 | `apollo-change-mgmt.html` | ✅ |
| WF-AP-07 | `apollo-config.html` | ✅ Vault/KMS |

## 关联文档

- [HTML 补页改页任务清单](./HTML补页改页任务清单.md)
- [03 PRD](../../03-对标Palantir-AOS-PRD框架.md)
- [09 Apollo](../../09-Apollo交付引擎产品方案.md)
- [09a Apollo 线框](../../09a-Apollo交付引擎产品设计线框图.md)

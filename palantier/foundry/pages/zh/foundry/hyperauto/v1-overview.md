---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/hyperauto/v1-overview/",
  "title": "HyperAuto V1 概述",
  "page_id": "v1-overview",
  "category_id": "data-integration",
  "section_id": "hyperauto",
  "previous": "/zh/foundry/hyperauto/aip/",
  "next": "/zh/foundry/hyperauto/v1-getting-started/",
  "scraped_at": "2026-07-13T05:34:28.484683+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# HyperAuto V1 概述

HyperAuto V1（也称为 SDDI 或 Bellhop）是 Palantir 的源到价值自动化套件的第一个版本。虽然 [HyperAuto V2](/zh/foundry/hyperauto/overview/) 已经为 SAP 发布，并且强烈推荐用于该数据源，但 HyperAuto V1 仍然支持多种源类型，包括：

* Salesforce
* Oracle NetSuite
* SAP（不推荐使用 V1，请使用 [V2](/zh/foundry/hyperauto/overview/)）

HyperAuto V1 的详细文档可在平台内查看。您可以在其中查看 **软件定义数据集成** 以了解各种配置选项。

## 架构

HyperAuto V1 由三个组件组成，旨在以最小的努力将数据从原始来源集成到 Ontology：

1. **连接器** 以安全和优化的方式在源系统之间传输大规模数据。
2. **源探索** 允许以引导方式快速发现数据，并提供“购物车”体验以快速创建和配置批量数据同步。
3. **自动化管道生成** 使用自动生成的数据管道将原始数据转换为在 [Ontology](/zh/foundry/ontology/overview/) 中策划的 Foundry 数据集和 Object 类型。

![架构图](../../../images/foundry/hyperauto/v1-sddi-overall-architecture.png)

## 管道生成

**自动化管道生成** 为集成常见源系统创建开箱即用的数据管道。这些管道准备数据，以便它们可以被 Ontology 和工作流使用。由于管道生成包含关于每个源系统的嵌入式知识，使用此功能可以提高效率，并消除了对每个底层源系统的复杂性进行全面了解的需求。

![管道生成器架构图](../../../images/foundry/hyperauto/v1-sddi-pipeline-generator-architecture.png)

生成的管道包括四个主要步骤：

* *源特定预处理* 生成具有预定义模式的元数据集。这些元数据包含理解源系统数据所需的信息。
* *清理库* 对所有数据集应用标准化的数据清理步骤，确保每一条流入系统的数据都遵循最佳实践。
* *核心生成* 执行数据丰富、列重命名、去重和数据合并，以生成可用于 Ontology 中的分析、报告和工作流的可用数据。
* *派生元素* 提供对高级工作流的预定义支持，包括生成合并表、时间序列数据集和提供丰富派生信息的丰富列，这些信息也会反馈到 Ontology 中。

![管道数据沿袭图](../../../images/foundry/hyperauto/v1-sddi-pipeline-generator-data-lineage.png)

## Ontology 创建

在管道自动生成后，HyperAuto V1 还支持自动生成 [Ontology](/zh/foundry/ontology/overview/)。这完成了数据集成过程，使您可以立即开始搜索、分析，甚至在数据之上搭建应用程序，得益于 Foundry 中一系列 [Ontology 感知应用程序](/zh/foundry/ontology/applications/)。

![批量 Ontology 生成](../../../images/foundry/hyperauto/v1-sddi-cockpit-batch-ontology-generation.png)

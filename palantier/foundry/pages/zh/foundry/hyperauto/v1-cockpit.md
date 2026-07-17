---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/hyperauto/v1-cockpit/",
  "title": "SDDI 控制台",
  "page_id": "v1-cockpit",
  "category_id": "data-integration",
  "section_id": "hyperauto",
  "previous": "/zh/foundry/hyperauto/v1-source-exploration/",
  "next": "/zh/foundry/hyperauto/v1-configuration-reference/",
  "scraped_at": "2026-07-13T05:34:29.398070+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# SDDI 控制台

**SDDI 控制台**是配置和执行 SDDI 流程的中心位置，指导您从同步创建和配置到数据管道生成和 Ontology 创建。

控制台的左侧面板列出了各个 SDDI 流程步骤以及这些步骤的状态。点击每个步骤时，右侧主区域会显示您可以对该特定 SDDI 流程步骤执行的不同操作。

## 初始状态

在开始之前，需要将控制台与一个功能齐全的 SDDI 实例连接。
要配置您的第一个 SDDI 实例，请参阅[入门](/zh/foundry/hyperauto/v1-getting-started/)。

## 访问现有控制台

要查看已配置的 SDDI 实例，请导航到数据连接中附加源的**源概览**页面，并选择**编辑管道生成器设置**。

![SDDI 源概览 编辑管道生成器设置](../../../images/foundry/hyperauto/v1-sddi-source-exploration.png)

## 控制台控件

控制台的左侧面板列出了三个阶段：

1. [同步数据](#sync-data)
2. [管道生成](#pipeline-generation)
3. [Ontology 更改](#ontology-changes)

### 同步数据

在同步数据阶段，您可以探索来自源的数据并创建新的同步到 Foundry。它还会自动配置 Foundry 中所需的元数据表，以确保 SDDI 正确运行。最后，它允许您触发将这些数据摄入到 Foundry。

![SDDI 控制台 同步数据](../../../images/foundry/hyperauto/v1-sddi-cockpit-sync-data.png)

### 管道生成

管道生成阶段允许您通过点选与 SDDI 自动管道生成器库进行交互，以生成和搭建数据管道，并导航到 SDDI 数据沿袭。

:::callout{theme="neutral" title="注意"}
管道配置仅适用于非 SAP 源。对于 SAP 源，管道配置是在 SDDI SAP 源浏览器中设置的。
:::

![SDDI 控制台 管道生成](../../../images/foundry/hyperauto/v1-sddi-cockpit-pipeline-generation.png)

### Ontology 更改

在 Ontology 更改步骤中，您可以预览可以基于正在指定和处理的数据集批量进行的 Ontology 更改。

![批量 Ontology 生成](../../../images/foundry/hyperauto/v1-sddi-cockpit-batch-ontology-generation.png)

## 访问故障排除

从工作区导航栏下的**软件定义数据集成**中访问控制台。

权限可以通过控制面板的**应用程序访问**页面进行配置。如果您没有访问 SDDI 控制台的权限，请联系您的 Foundry 平台 IT 管理员或 Palantir 支持。

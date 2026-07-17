---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/time-series-setup/",
  "title": "设置",
  "page_id": "time-series-setup",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/time-series/time-series-concepts-glossary/",
  "next": "/zh/foundry/time-series/create-or-select-ts-ot/",
  "scraped_at": "2026-07-13T06:09:48.584577+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 设置

以下文档旨在指导您创建和配置时间序列Object类型及其属性，以便在Foundry应用程序中进行分析。

:::callout{theme="warning"}
在继续设置之前，请查看并理解[在Ontology中设置时间序列](/zh/foundry/time-series/time-series-overview/#store-time-series-in-the-ontology)的两个可用选项。如果您已经开始设置过程但不确定停在哪一步，请查看下面的[设置检查点](#setup-checkpoints)部分，以了解从哪里继续。
:::

![设置过程概览](../../../images/foundry/time-series/time-series-general-overview.png)

## 起始

在您开始设置可用于分析的时间序列Object类型和属性之前，您需要在Foundry中拥有一个或多个包含您的[时间序列](/zh/foundry/time-series/time-series-concepts-glossary/#time-series)的数据集。如果您有多个数据集，一个序列的所有值应包含在同一个数据集中。请参阅[设置检查点](#setup-checkpoints)以获取常见起始点的示例。

首先，导航到包含时间戳列的[数据集预览](/zh/foundry/dataset-preview/overview/)，然后从**分析数据**操作菜单中选择**设置时间序列**。

![设置时间序列操作项](../../../images/foundry/time-series/time-series-set-up-time-series-action-item.png)

这将启动一个概览，引导您进入我们的时间序列设置助手。以下文档将提供更深入的解释，以便在助手引导您完成以下过程时，可能需要进行的数据变换。

:::callout{theme="neutral"}
您也可以通过直接导航到`https://<domain>/workspace/ontology/home/overview/time-series-setup`启动设置助手。
:::

## 设置检查点

使用以下决策树来确定您的起始点或继续进行时间序列设置过程。

* 您的原始时间序列数据是否已在Foundry中？
  * **没有**：使用[数据连接](/zh/foundry/data-connection/overview/)将您的数据同步到Foundry中。
* 您的原始时间序列数据是否有仅为时间戳类型的时间戳列？
  * **没有**：在数据集应用中编辑架构。
* 您的原始数据是否如下示例？
  * 单个数据集包含一个Object键、时间戳列和多个列，每个列都有该时间点的值。

    ![单个数据集示例](../../../images/foundry/time-series/time-series-setup-single-dataset-example.png)

  * 一个数据集包含关于Objects的信息，以及多个数据集，每个数据集包含一个键、时间戳列和单个序列的值。

    ![多个数据集示例](../../../images/foundry/time-series/time-series-setup-multiple-datasets-example.png)

  * **没有**：您可能需要变换您的数据，使其具有类似的架构。如果不是，您仍然可以继续，但您需要知道如何自己变换数据以生成有效的[时间序列Object类型支持数据集](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-object-type-backing-dataset)和[时间序列同步](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-sync)。
* 我如何启动设置助手？
  * 查看一个时间序列数据集（即，具有时间戳列的数据集），并从**分析数据**操作菜单下选择**设置时间序列**（参见[起始](#get-started)）。这将显示逐步对话框，随后是我们的设置助手。

    ![设置时间序列操作项](../../../images/foundry/time-series/time-series-set-up-time-series-action-item.png)

  * 或者，通过直接导航到`https://<domain>/workspace/ontology/home/overview/time-series-setup`直接启动设置助手。
* 您的Object类型是否已经存在？
  * **是的**：启动设置助手并选择**选择现有Object**。
  * **没有**：启动设置助手并选择**创建新Object类型**。
* 您是否有一个Object类型支持数据集？
  * **是的**：在**创建新Object类型**对话框中选择它。
  * **没有**：导航到Pipeline Builder，将数据从通用形状变换为时间序列Object类型支持数据集的形状（参见[创建或选择时间序列Object类型](/zh/foundry/time-series/create-or-select-ts-ot/)）。
* 您是否已为您的Object类型添加了时间序列属性（TSPs）？
  * **是的**：您已准备好使用时间序列Object类型。参见[在Foundry中使用时间序列](/zh/foundry/time-series/time-series-usage/)以了解您可以在Foundry应用程序中使用时间序列的不同方式。
  * **没有**：参见[配置时间序列属性](/zh/foundry/time-series/time-series-properties/#time-series-property-setup)以获取下一步。
* 您有时间序列同步吗？
  * **是的**：完成[配置时间序列属性](/zh/foundry/time-series/time-series-properties/#time-series-property-setup)并在对话框的第二步选择您的同步。
  * **没有**：按照[配置时间序列属性](/zh/foundry/time-series/time-series-properties/#time-series-property-setup)下的说明创建时间序列同步。
    * 确保时间序列同步的系列ID与Object类型支持数据集的系列ID匹配。
* 我如何使用刚刚设置的时间序列属性？
  * 查看[在Foundry中使用时间序列](/zh/foundry/time-series/time-series-usage/)，探索您可以如何在Foundry中分析时间序列。

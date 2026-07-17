---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/create-or-select-ts-ot/",
  "title": "创建或选择时间序列Object类型",
  "page_id": "create-or-select-ts-ot",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/time-series/time-series-setup/",
  "next": "/zh/foundry/time-series/time-series-properties/",
  "scraped_at": "2026-07-13T06:09:58.521947+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 创建或选择时间序列Object类型

要将[时间序列属性](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-property-tsp)添加到现有Object类型，请在设置助手中选择**选择现有Object类型**路径。继续查看如何[设置时间序列属性](/zh/foundry/time-series/time-series-properties/#time-series-property-setup)的部分以了解下一步。

要创建新的Object类型，您必须首先拥有一个[时间序列Object类型基础数据集](/zh/foundry/time-series/time-series-concepts-glossary/)。如果您尚未拥有符合此所需模式的数据集，则需要在[Pipeline Builder](/zh/foundry/pipeline-builder/overview/)中创建一个。

虽然可以在[Pipeline Builder中作为Ontology输出创建新的Object类型](/zh/foundry/pipeline-builder/outputs-add-ontology-output/)，但我们建议在Pipeline Builder中创建时间序列Object类型基础数据集，然后按照设置助手创建新的Object类型。按照以下步骤在Pipeline Builder中准备数据集。

## 准备时间序列Object类型基础数据集

在创建新的时间序列Object类型之前，您必须首先拥有一个时间序列Object类型基础数据集。以下说明描述了如何在Pipeline Builder中创建时间序列Object类型基础数据集。

![时间序列Object类型基础数据集示例](../../../images/foundry/time-series/time-series-setup-machine-object-type-backing-dataset.png)

1. 首先，专注于创建一个数据集，其中每一行代表新Object类型的单个Object。此数据集需要一个可用于唯一标识Object的主键列，以及每个Object上的非时间序列[属性](/zh/foundry/ontology/core-concepts/#property)的列。
2. 接下来，通过为每个[时间序列属性](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-property-tsp)添加一个[系列ID](/zh/foundry/time-series/time-series-concepts-glossary/#series-id)，使此Object类型基础数据集支持时间序列。您可能会通过以下在Pipeline Builder中的一种变换来添加此项，具体取决于您的数据形状：

* [您的不同测量/传感器类型的时间序列数据存储在不同的数据集中，您希望手动创建新的系列ID列。](#multiple-datasets-manual-creation-of-new-series-id-columns)
* [您有一个单一数据集用于所有测量和/或大量系列。](#single-dataset-or-large-number-of-series)
* [您有多个数据集用于单一测量/传感器类型。](#multiple-datasets-for-a-single-measurement-type)

### 多个数据集（手动创建新的系列ID列）

从包含Object信息的数据集开始（例如，下图中的机器信息）：

![多个数据集示例](../../../images/foundry/time-series/time-series-setup-multiple-datasets-example.png)

1. 在[Pipeline Builder](/zh/foundry/pipeline-builder/transforms-transform-data/)中添加一个`连接字符串`变换。
   1. 选择一个常用分隔符，例如下划线（`_`）。
   2. 配置您的表达式：
      1. 输入一个**值**类型输入，并将此值设置为您的系列名称（例如，`temperature`）。
      2. 输入一个**列**类型输入，并将其设置为您的主键/Object键。
2. 为此特定系列命名这个新列，以便轻松识别它作为系列ID（例如，`temperature`或`temperature_series_id`）。

   ![连接字符串示例1](../../../images/foundry/time-series/time-series-setup-concatenate-1.png)

### 单个数据集或大量系列

通过创建一个通过合并将每个系列名称作为列名的数据集，避免手动创建每个新的系列ID列。一旦您有了这个单一数据集，请按照以下说明操作：

![单个数据集示例](../../../images/foundry/time-series/time-series-setup-single-dataset-example.png)

1. 添加一个`透视变换`。

   1. 设置**输出透视列名**为`series_name`。
   2. 设置**透视值输出列名**为`series_value`。
   3. 在**要透视的列**字段中，选择所有具有系列名称的列。

   ![透视变换示例1](../../../images/foundry/time-series/time-series-setup-unpivot-1.png)

2. 添加一个`连接字符串`变换以生成系列ID。
   1. 选择一个常用分隔符，例如下划线（`_`）。
   2. 配置您的表达式：
      1. 输入`series_name`作为第一个输入。
      2. 输入Object键作为第二个输入（截图中的`machine_id`）。

3. 将这个新的输出命名为`series_id`。

   ![添加系列ID示例](../../../images/foundry/time-series/time-series-concatenate-for-series-id.png)

4. 将系列ID列重新合并到您的Object类型基础数据集中。

### 单一测量类型的多个数据集

:::callout{theme="warning"}
您的Object类型必须在[Object Storage V2](/zh/foundry/object-backend/overview/#object-storage-v2-architecture)中以支持具有多个时间序列同步的时间序列属性。
:::

由于传感器数据通常由多个数据源提供，因此在一个数据集中规范化和变换所有传感器数据可能具有挑战性。有时，由于某些传感器持有分类数据而其他传感器包含数值数据，无法做到这一点；不同的数据类型不能存在于一个[时间序列同步](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-sync)中。为了避免需要将所有传感器数据变换并统一到一个时间序列数据集中，您可以将一个[时间序列属性](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-property-tsp)链接到多个时间序列同步。为此，您必须在您的Object类型基础数据集中有一个[合格系列ID](/zh/foundry/time-series/time-series-concepts-glossary/#qualified-series-id)列。按照以下步骤创建一个合格系列ID。请注意，您需要在遵循这些步骤之前[创建您的时间序列同步](/zh/foundry/time-series/time-series-syncs/)。

1. 通过在Pipeline Builder中选择**添加数据**，将支持您的时间序列属性的每个时间序列同步的基础数据添加到您的管道中。
2. 对于每个时间序列同步数据集，仅选择系列ID列并对结果的单列数据集进行去重。
3. 添加一个`创建时间序列参考值`变换。使用系列ID列作为**系列标识符**并选择适当的时间序列同步作为**时间序列同步RID**。将新列命名为`qualified_time_series_id`或类似名称。

![创建时间序列参考值](../../../images/foundry/time-series/create-ts-reference-values.png)

4. 将合格系列ID列重新合并到您的Object类型基础数据集中。此步骤要求您的Object类型基础数据集中的系列ID是唯一的。

生成的数据集应如以下示例所示。`seriesId`对应于同步数据集中的系列标识符，而`syncRid`对应于存储该系列的同步的RID。

![时间序列多同步基础数据集。](../../../images/foundry/time-series/time-series-multisync-data.png)

## 创建新的时间序列Object类型

一旦您准备好了您的时间序列Object类型基础数据集，按照设置助手中的路径**创建新Object类型**。此路径将重定向您到[Ontology Manager Object创建设置助手](/zh/foundry/object-link-types/create-object-type/)，在这里您将选择新的数据集作为您的基础数据源。完成助手对话框后，您将准备好[设置时间序列属性](/zh/foundry/time-series/time-series-properties/#time-series-property-setup)。

:::callout{theme="warning"}
如果您直接从Ontology Manager主页启动Object创建设置助手（即，不是从时间序列设置助手），则助手在完成后不会重定向您到新Object类型的**功能**标签。
:::

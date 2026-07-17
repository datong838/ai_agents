---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/transforms-join-data/",
  "title": "合并数据",
  "page_id": "transforms-join-data",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/transforms-transform-data/",
  "next": "/zh/foundry/pipeline-builder/transforms-union-data/",
  "scraped_at": "2026-07-13T05:46:57.130119+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 合并数据

除了[变换单个数据集](/zh/foundry/pipeline-builder/transforms-transform-data/)之外，Pipeline Builder还允许您通过合并和并集将数据集结合在一起。

合并将两个具有至少一个匹配列的数据集结合在一起。根据您配置的合并类型，您的合并输出可以结合匹配行并排除不匹配行。

## 选择数据集

要将两个数据集合并在一起，请在图中选择第一个数据集节点并点击**合并**。

![合并数据的截图](../../../images/foundry/pipeline-builder/transforms-join-data@2x.png)

第一个选择的数据集是**左**侧数据集。选择另一个数据集节点作为**右**侧数据集。点击**开始**以配置合并。

![合并两个表的截图](../../../images/foundry/pipeline-builder/transforms-join-two-tables@2x.png)

## 配置合并

在合并表单中，您可以编辑合并类型、选择匹配条件，并预览输出表。

* **合并类型：** 选择创建左、右、内或外合并。
  * **左：** 保留左表中的所有行以及右表中的匹配行。
  * **右：** 保留右表中的所有行以及左表中的匹配行。
  * **内：** 仅保留两个表之间的匹配行。
  * **外：** 保留两个表中的所有行，对于不匹配行的列填充`null`。
* **匹配条件：** 选择左数据集中的一列，将其标记为等于右数据集中的一列。例如，左侧`Clean Facility Data`数据集中的`city`列等于右侧`Facility Person`数据集中的`CITY`列。
* **预览：** 查看来自右和左输入数据集的预览数据。应用合并后，查看输出表的预览数据。如果应用合并时出错，请在**出错**标签中查看。

![配置变换的截图](../../../images/foundry/pipeline-builder/transforms-join-configure@2x.png)

以上和以下示例中的所有数据都是随机生成的，并不具代表性。

您可以决定在合并中包含特定列，并为右表添加前缀。选择**显示高级**以展开前缀和列字段，为右表输入前缀，并选择要在合并中包含的列。在下面的示例中，我们保留了左数据集中的所有列，仅包含右数据集中的`STATE`和`population`列。

![高级配置变换的截图](../../../images/foundry/pipeline-builder/transforms-show-advanced@2x.png)

## 应用合并

完成合并配置后，点击**应用**将合并添加到您的工作流中。您将在图中看到连接到两个合并数据集的合并节点。我们将新的合并命名为`合并人员数据`，它是原始`Clean Facility Data`和`Facility Person`数据集的直接输出。

![完成合并人员数据的截图](../../../images/foundry/pipeline-builder/transforms-join-person-data@2x.png)

点击合并节点并选择**编辑**以重命名或编辑合并。

:::callout{theme="neutral"}
拖动节点上的白色或灰色圆圈以更改连接并移除图中的链接。
:::

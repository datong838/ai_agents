---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/transforms-union-data/",
  "title": "合并数据",
  "page_id": "transforms-union-data",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/transforms-join-data/",
  "next": "/zh/foundry/pipeline-builder/transforms-geospatial/",
  "scraped_at": "2026-07-13T05:46:46.430174+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 合并数据

在Pipeline Builder中，另一种变换和结构化数据的方法是应用合并。合并将两个数据集组合在一起，以包括每个数据集中的所有行。在Pipeline Builder中，合并保留所有行，包括重复行。

## 选择数据集

要将两个数据集合并在一起，请在您的工作区中选择第一个数据集节点并点击**合并**。

![合并选择的截图](../../../images/foundry/pipeline-builder/transforms-union@2x.png)

第一个选择的数据集是**左**侧数据集。选择另一个数据集节点作为**右**侧数据集。点击**开始**以导航到合并输出预览页面。

![合并选择的截图](../../../images/foundry/pipeline-builder/transforms-union@2x.png)

## 预览合并

在预览窗格中，点击**创建合并**，然后查看输出数据集预览。

![合并选择的截图](../../../images/foundry/pipeline-builder/transforms-union-preview@2x.png)

合并要求所有输入具有相同的模式。如果输入模式不完全匹配，合并将显示出错消息并列出缺失的列。

要解决此问题，请删除对缺失列的引用或检查您的输入。

## 应用合并

一旦完成创建合并，点击**应用**以将合并添加到您的工作流程中。您将在图中看到合并节点连接到两个已合并的数据集。我们将新的合并命名为`Union`，它是原始`Correct columns`和`Vendor Cut 2 - demo data`数据集的直接输出。

![合并选择的截图](../../../images/foundry/pipeline-builder/transform-union-complete@2x.png)

您可以通过点击合并节点并选择**编辑**来重命名或编辑合并。

:::callout{theme="neutral"}
拖动节点上的白色或灰色圆圈以更改连接并移除图中的链接。点击合并节点上的灰色椭圆以移除多个连接。
:::

请记住，合并保留来自右侧和左侧数据集的所有行，包括重复行。要移除重复行，请在您的合并输出中添加一个`删除重复`变换。

[了解更多关于变换的信息。](/zh/foundry/pipeline-builder/transforms-overview/)

---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-lineage/find-column/",
  "title": "查找具有指定列的数据集",
  "page_id": "find-column",
  "category_id": "data-integration",
  "section_id": "data-lineage",
  "previous": "/zh/foundry/data-lineage/stale-datasets/",
  "next": "/zh/foundry/data-lineage/build-datasets/",
  "scraped_at": "2026-07-13T06:03:40.601541+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 查找具有指定列的数据集

您可以在您的数据沿袭图中轻松搜索特定数据集列：

* 首先，确保您已将管道中所有感兴趣的数据集添加到您的沿袭图中。

* 接下来，使用应用程序左上角工具切换中的**拖拽选择模式**选择所有感兴趣的数据集。您也可以按住 `Ctrl / Command` 一次选择多个节点，或使用 `Ctrl / Command + A` 选择所有节点。

  ![使用选择模式选择数据集](../../../images/foundry/data-lineage/select-mode.png)

* 然后，从数据沿袭侧边栏中选择**查看选择属性的直方图**。

  ![查看选择属性的直方图](../../../images/foundry/data-lineage/view-histogram.png)

* 在**常见列**部分，您可以看到选择中按名称排列的最常见列。

* 点击其中一个列以突出显示选择中包含该列的数据集。

  ![在直方图中查看常见列](../../../images/foundry/data-lineage/column-search-dataset.png)

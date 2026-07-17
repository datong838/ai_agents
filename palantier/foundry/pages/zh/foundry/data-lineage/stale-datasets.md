---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-lineage/stale-datasets/",
  "title": "了解过时的数据集",
  "page_id": "stale-datasets",
  "category_id": "data-integration",
  "section_id": "data-lineage",
  "previous": "/zh/foundry/data-lineage/build-timeline/",
  "next": "/zh/foundry/data-lineage/find-column/",
  "scraped_at": "2026-07-13T06:03:24.351538+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 了解过时的数据集

您的数据集可能未更新的原因有几个。常见的场景包括：

* 我的数据集搭建是否失败？
* 是否有上游数据集未搭建且未更新？
* 我们是否从源接收到最新数据？

您可以通过使用数据沿袭轻松解答这些问题。

* 首先，通过在数据沿袭中打开感兴趣的数据集并右键单击节点，验证管道中每个资源的状态。

![展开选定节点](../../../images/foundry/data-lineage/expand-node-data-lineage.png)

* 然后，选择**展开节点**。您可以通过点击**展开父节点**上方的双左箭头来查看该数据集的所有祖先节点。

![在展开节点后展开父节点](../../../images/foundry/data-lineage/parent-node.png)

* 接下来，在数据沿袭右上角的**节点颜色选项**下拉菜单中选择**搭建状态**选项，以查看管道中每个资源的搭建状态。此视图将使诊断过时的数据集变得更加容易。

![选择搭建状态节点颜色](../../../images/foundry/data-lineage/node-color-build-status.png)

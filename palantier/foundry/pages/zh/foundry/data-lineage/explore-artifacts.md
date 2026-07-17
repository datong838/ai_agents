---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-lineage/explore-artifacts/",
  "title": "探索工件和Ontology实体",
  "page_id": "explore-artifacts",
  "category_id": "data-integration",
  "section_id": "data-lineage",
  "previous": "/zh/foundry/data-lineage/explore-lineage/",
  "next": "/zh/foundry/data-lineage/save-share-graph/",
  "scraped_at": "2026-07-13T06:03:31.872676+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 探索工件和Ontology实体

您可以在数据沿袭中找到与您的数据集相关的Foundry工件和Ontology实体。数据沿袭界面允许您直接导航到这些资源，并查看它们如何融入您的Ontology。

## 查找相关工件

在您的数据沿袭图中，选择一个数据集。然后，在右侧边栏中选择**相关项**以展开**相关工件**面板。**相关项**图标将显示一个徽章，其中包含与所选数据集相关的工件数量。在工件面板中，您可以看到整个Foundry中相关资源的列表，包括Contour可视化和Slate应用程序。

![查找相关数据集工件](../../../images/foundry/data-lineage/related-artifacts.png)

单击资源旁边的节点图标以放大相关数据集，或单击资源以在新标签中打开相应应用程序。您可以筛选相关工件的列表以包含不同的项目类型，并按最旧、最新、名称、路径或最后修改时间排序列表。

## 查找Ontology实体

通过选择数据集并在右侧边栏中打开**查看节点属性**面板，在您的沿袭图中查找由数据集定义的Object类型。

![在数据沿袭中查看节点属性](../../../images/foundry/data-lineage/view-node-properties.png)

在**关于**选项卡中，您将看到使用所选数据集创建的任何Object类型。单击Object类型旁边的**设置**图标以在新的Ontology管理器标签中查看其配置。

![在数据沿袭中查看Ontology实体](../../../images/foundry/data-lineage/ontology-entity.png)

您还可以使用右侧边栏中的**搜索Foundry**工具将Object类型添加到您的数据沿袭中。使用基本或高级搜索查找Object类型，并从列表中选择它以将其添加到您的图表中。然后，您可以查看与Object类型相关的链接类型，并使用图表可视化您的数据集与新添加的Object类型之间的连接。

![查看Object类型和数据集连接](../../../images/foundry/data-lineage/object-type-dataset-flow.gif)

[了解有关创建Ontology的更多信息。](/zh/foundry/ontology/overview/)

---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-lineage/elements-reference/",
  "title": "图元素参考",
  "page_id": "elements-reference",
  "category_id": "data-integration",
  "section_id": "data-lineage",
  "previous": "/zh/foundry/data-lineage/node-coloring/",
  "next": "/zh/foundry/data-lineage/dataset-preview-logic/",
  "scraped_at": "2026-07-13T06:02:58.960207+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 图元素参考

## 节点类型

| 节点                                        | 类型 | 描述 |
| --- | --- | --- |
![数据源](../../../images/foundry/data-lineage/data-lineage-node-data-source.png) | **数据源** | 这是数据源在[数据连接](/zh/foundry/data-connection/overview/)中显示的名称。[了解更多关于不同源类型的信息。](/zh/foundry/data-integration/source-type-overview/)
![数据集节点](../../../images/foundry/data-lineage/data-lineage-node-dataset.png) | **数据集** | Foundry数据集及其之间的沿袭。数据集节点的颜色取决于[用户选择](/zh/foundry/data-lineage/node-coloring/)。虚线边框表示非结构化数据集。
![Object类型节点](../../../images/foundry/data-lineage/data-lineage-node-object-type.png) | **Object类型** | Ontology [Object类型](/zh/foundry/object-link-types/object-types-overview/)。节点的图标和颜色取决于每种Object类型的定义。当点击Object类型名称旁边的“链接”图标时，数据沿袭显示此Object类型与其他Object类型之间的关系。
![工件节点](../../../images/foundry/data-lineage/data-lineage-node-artifact.png) | **工件** | 数据沿袭展示不同的Foundry工件，如：[Contour](/zh/foundry/contour/overview/)分析，[报告](/zh/foundry/reports/overview/)等。节点的颜色取决于工件类型，工件类型在节点顶部标示。

## 节点指示器

节点指示器出现在数据集节点的顶部，并提供有关资源的附加信息。

| 指示器 | 类型 | 描述 |
| --- | --- | --- |
![问题图标](../../../images/foundry/data-lineage/data-lineage-icon-issues-reported.png)  | **打开的问题** | 此指示器表示图中与节点相关的当前打开的问题。悬停在此信号上会显示打开问题的数量。
![链接的Object图标](../../../images/foundry/data-lineage/data-lineage-icon-linked-objects.png) | **定义Object类型** | 此指示器出现在用于定义Ontology Object类型的数据集上。悬停在右箭头上可以显示那些链接的Object类型。[了解更多关于Object类型的信息。](/zh/foundry/object-link-types/object-types-overview/)
![同步图标](../../../images/foundry/data-lineage/data-lineage-icon-syncs.png) | **同步** | 带有此指示器的数据集与其他数据库或系统同步。您可以通过选择节点并打开属性面板，或在数据集预览中打开“详细信息”选项卡（右键单击节点并点击**打开**）来查看这些同步。
![回收站图标](../../../images/foundry/data-lineage/data-lineage-icon-trashed.png) | **回收站** | 此指示器出现在表示已删除数据集或工件的节点上。删除的节点也会被局部淡化，并且它们的名称被划掉。

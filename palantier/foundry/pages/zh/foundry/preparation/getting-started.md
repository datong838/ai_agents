---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/preparation/getting-started/",
  "title": "入门",
  "page_id": "getting-started",
  "category_id": "data-integration",
  "section_id": "preparation",
  "previous": "/zh/foundry/preparation/overview/",
  "next": "/zh/foundry/preparation/preparation-tutorial/",
  "scraped_at": "2026-07-13T06:05:31.884011+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 入门

:::callout{theme="warning"}
Preparation已被[Pipeline Builder](/zh/foundry/pipeline-builder/overview/)取代，因此不再是清洗和准备数据的推荐方法。Pipeline Builder使清洗和准备您的数据以用于管道变得简单，同时也提供[Marketplace](/zh/foundry/marketplace/overview/)支持。
:::

本页面将帮助您了解用于清洗和准备数据集的Preparation界面。

## 打开数据集进行清洗和准备

### 从数据集开始

从任何数据集的**操作**菜单中选择**在Preparation中清洗**，以创建该数据集的新[准备](/zh/foundry/preparation/overview/#terminology)。

### 从Preparation界面

点击\*\*选择数据集...\*\*按钮，并选择要清洗/准备的数据集。

## 清洗和准备您的数据

1. 点击列以查看该列中数据的概述，并应用清洗和准备操作。
   * 有两种准备视图：**表格**（看起来像电子表格）和**列**（为每列显示更紧凑的卡片）。
2. 查看[基础示例](/zh/foundry/preparation/basic-examples/)页面，了解清洗和准备数据的各种方法。

### 在Contour中分析同时清洗/准备

1. 点击**分析**按钮，在Contour中打开当前准备。
2. 当您对准备进行更改时，Contour将提示更新。点击Contour中的**更新数据**按钮，根据准备刷新分析。

## 保存已清洗或准备好的数据集副本

1. 点击标题栏中的**保存为数据集**按钮。
   * 默认情况下，此操作将创建一个更新数据集，该数据集可以根据底层数据集或准备的更改进行重建。要保存一次性数据集，点击**保存为数据集**按钮旁的箭头，选择**保存一次性数据集**。
2. 选择您希望保存数据集的位置，然后点击**保存**。数据集将开始搭建，并将在准备好时通知您。

    <img src="../../foundry-docs/preparation/media/tutorial_building.png" style="max-height: 95.5px;" />

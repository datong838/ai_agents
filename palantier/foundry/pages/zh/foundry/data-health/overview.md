---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-health/overview/",
  "title": "概述",
  "page_id": "overview",
  "category_id": "data-integration",
  "section_id": "data-health",
  "previous": "/zh/foundry/data-lineage/see-impact-marking-changes/",
  "next": "/zh/foundry/data-health/builds-checks-faq/",
  "scraped_at": "2026-07-13T06:03:53.104137+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

**数据健康** 是一个Foundry服务，用于监测和提醒数据集中常见的问题。数据健康自带预构建检查，用于检测数据集状态、时间、大小、内容和模式的潜在问题。如果检查失败，数据健康会在平台内发送通知和电子邮件来提醒您这个失败。

本节文档提供了关于数据健康可用选项的详细参考。关于如何设置有效的健康检查的高级指导，请阅读[维护管道](/zh/foundry/maintaining-pipelines/overview/)部分。特别是，[推荐的健康检查](/zh/foundry/maintaining-pipelines/recommended-health-checks/)页面可能会有所帮助。

![数据健康概述](/resources/foundry/data-health/overview.png)

## 访问数据健康

在Foundry中，有四种方式可以查看健康检查。

### 数据集的健康状况

在[数据集预览](/zh/foundry/dataset-preview/overview/)中查看数据集时，您可以导航到 **健康** 标签页来添加新检查，修改现有检查并查看历史检查结果。

### 项目中的健康状况

在每个**项目目录**标签页中，项目维护的第一个部分显示了应用于项目中任何数据集的所有健康检查，并附有通过或失败的检查摘要。

### 管道中的健康状况

在[数据沿袭](/zh/foundry/data-lineage/overview/)中，数据集可以根据它们的健康检查状态进行着色。此外，页面底部的数据健康标签（在设置中切换开启）显示了沿袭图中所有数据集的健康检查及其状态。

### 平台中的健康状况

要查看所有数据集的健康检查概述，请从侧边栏选择**数据健康**应用。在这里，您可以按状态或名称筛选或排序数据集。您还可以切换显示仅您监测的数据集。此页面还允许您通过点击右上角的 **添加健康检查** 来添加新的健康检查。

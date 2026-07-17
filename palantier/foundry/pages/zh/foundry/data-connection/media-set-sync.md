---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-connection/media-set-sync/",
  "title": "媒体集同步",
  "page_id": "media-set-sync",
  "category_id": "data-integration",
  "section_id": "data-connection",
  "previous": "/zh/foundry/data-connection/file-based-syncs/",
  "next": "/zh/foundry/data-connection/optimize-jdbc-syncs/",
  "scraped_at": "2026-07-13T05:31:06.753598+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 媒体集同步

本页面讨论如何通过Data Connection设置媒体集源并同步到Foundry。

支持媒体同步的源列表不断增长。然而，如果您想要的基于文件的源尚不支持，您可以在数据集中摄取文件并通过[Python变换](/zh/foundry/data-integration/media-sets/#upload-from-a-filesystem-catalog-dataset)将其转换为媒体集。

Data Connection支持以下源用于媒体同步：

* Azure Blob Filesystem (ABFS)
* Amazon S3
* 外部变换

## 设置媒体集源和同步

1. 通过\*\*+ 新建源**导航到**源**页面找到支持的源。然后，搜索**媒体同步\*\*以找到所有支持的源。

![媒体同步。](../../../images/foundry/data-connection/media-syncs.png)

2. 确保您有权限导入任何必要的网络策略，然后按照以下适当的说明设置支持的源：

* [Amazon S3](/zh/foundry/available-connectors/amazon-s3/)
* [Azure Blob Filesystem (ABFS)](/zh/foundry/available-connectors/azure-blob-filesystem/)

3. 添加一个媒体集同步。在源的**概览**页面，找到**媒体同步**部分以创建媒体同步。

![媒体同步部分](/resources/foundry/data-connection/media-sync-section.png)

4. 通过选择所需的媒体文件类型和源中的相关文件路径来设置媒体集同步。如果您的媒体文件在根路径下，则无需添加路径配置。
   ![媒体同步文件配置](/resources/foundry/data-connection/set-up-media-sync-files-to-add.png)

5. 创建所需的媒体同步摄取搭建计划。您可以在初始配置后编辑计划。
   ![媒体同步计划](/resources/foundry/data-connection/set-up-media-sync-schedule.png)

6. 设置您的延迟和存储配置。
   ![媒体同步延迟和存储](/resources/foundry/data-connection/set-up-media-sync-latency-and-storage.png)

7. 当您选择了初始配置后，**保存媒体集同步**。

8. 选择**运行**以触发您的首次同步以查看您的媒体同步。
   ![运行初始媒体同步](/resources/foundry/data-connection/set-up-media-sync-run-initial-sync.png)

设置好媒体同步后，学习如何通过[变换或Pipeline Builder](/zh/foundry/data-integration/media-sets/#transform-media-in-foundry)利用您的媒体集。

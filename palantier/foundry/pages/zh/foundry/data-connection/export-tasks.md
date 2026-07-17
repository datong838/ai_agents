---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-connection/export-tasks/",
  "title": "导出任务（旧版）",
  "page_id": "export-tasks",
  "category_id": "data-integration",
  "section_id": "data-connection",
  "previous": "/zh/foundry/data-connection/export-overview/",
  "next": "/zh/foundry/data-connection/webhooks-overview/",
  "scraped_at": "2026-07-13T05:31:34.248700+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 导出任务（旧版）

:::callout{theme="warning"}
我们通常不建议使用导出任务将数据写回到外部源。然而，根据您在Foundry中的注册情况，某些源类型可能可以使用并支持导出任务。

以下导出任务文档是为尚未过渡到我们[推荐的导出工作流](/zh/foundry/data-connection/export-overview/)的导出任务用户提供的。
:::

Data Connection导出任务支持写入广泛的常见企业系统，包括：

* [Amazon S3](/zh/foundry/available-connectors/amazon-s3/)
* [Azure Blob Filesystem (ABFS)](/zh/foundry/available-connectors/azure-blob-filesystem/)
* [HDFS](/zh/foundry/available-connectors/hdfs/)
* [JDBC兼容系统](/zh/foundry/available-connectors/custom-jdbc-sources/)，包括：
  * 关系数据库
    * [PostgreSQL](/zh/foundry/available-connectors/postgresql/)
    * [Microsoft SQL Server](/zh/foundry/available-connectors/microsoft-sql-server/)
    * MySQL
  * 数据仓库
    * Teradata
    * [Snowflake](/zh/foundry/available-connectors/snowflake/)
    * Vertica
* 文件系统，包括[挂载在中介代理上的网络文件系统](/zh/foundry/available-connectors/filesystem/)
* [SFTP](/zh/foundry/available-connectors/sftp/)

## 平台内文档

详细的导出任务文档可在Foundry平台中查看。导航到平台导航侧边栏左下角的 **Help & support** 标签中的 **Custom Documentation**。然后，导航到 **Data Connection** > **Sources** > **Export Tasks** 以查看配置选项的范围。

## 已知导出任务限制

* 导出任务未与权限标记和导出控制集成。通过导出任务导出的数据不需要导出数据集或流的取消标记权限。
* 导出任务未针对性能进行优化。导出大量数据可能导致长时间运行的任务或任务无法完成。
* 导出任务没有用户界面进行配置，必须使用YAML提供所需的配置选项进行配置。并非所有导出任务选项都记录供自助使用；在某些情况下，导出任务只能通过Palantir的支持进行配置。

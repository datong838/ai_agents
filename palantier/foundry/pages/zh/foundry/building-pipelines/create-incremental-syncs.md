---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/building-pipelines/create-incremental-syncs/",
  "title": "创建增量同步",
  "page_id": "create-incremental-syncs",
  "category_id": "data-integration",
  "section_id": "building-pipelines",
  "previous": "/zh/foundry/building-pipelines/incremental-overview/",
  "next": "/zh/foundry/building-pipelines/maintaining-incremental-performance/",
  "scraped_at": "2026-07-13T05:40:43.610627+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 创建增量同步

虽然可以从配置为`SNAPSHOT`事务的数据连接同步中在管道中派生仅限`APPEND`的数据集，但增量管道的主要好处来自于端到端地应用增量。这意味着数据同步到Foundry应由仅将新数据带入系统的`APPEND`事务组成。配置增量同步的另一个好处是，它们可以最大限度地减少对源系统的负载，并可以减少数据存储需求。

从源系统同步的大多数数据集包括从文件系统同步的文件，或使用JDBC源类型配置的数据库或数据仓库的提取。以下指南将引导您如何为这些源类型配置增量同步：

* [优化基于文件的追加同步](/zh/foundry/data-connection/file-based-syncs/)
* [增量JDBC同步](/zh/foundry/data-connection/optimize-jdbc-syncs/#incremental-syncs)

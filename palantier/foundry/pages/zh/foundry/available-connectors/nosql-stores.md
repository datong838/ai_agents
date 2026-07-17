---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/nosql-stores/",
  "title": "NoSQL 存储",
  "page_id": "nosql-stores",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/myob/",
  "next": "/zh/foundry/available-connectors/odata/",
  "scraped_at": "2026-07-13T05:36:34.758029+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# NoSQL 存储

数据连接可以配置为从各种 NoSQL 数据库同步数据。之前集成的一些 NoSQL 存储示例包括：

* **Amazon DynamoDB**
* **Apache HBase**
* **Azure Cosmos DB**
* **Cassandra**
* **Cockroach DB**
* **CouchDB**
* **Elasticsearch**
* **InfluxDB**
* **MarkLogic**
* **MongoDB**
* **Neo4j**
* **OrientDB**
* **Redis**

:::callout{theme="neutral"}
推荐的配置方法可能会因 NoSQL 数据库而异：

* 一些系统有专用的连接器，可以直接在新源页面上选择。当有专用连接器时，我们建议直接选择它。
* 一些系统有一个 REST API，可以从[外部变换](/zh/foundry/data-integration/external-transforms/)和/或[REST API 源](/zh/foundry/available-connectors/rest-apis/)使用。
* 一些系统提供一个 JDBC 驱动程序，可以与通用[JDBC 连接器](/zh/foundry/available-connectors/custom-jdbc-sources/)一起使用。
* 对于不属于上述类别的系统，请联系 Palantir 客服支持。
:::

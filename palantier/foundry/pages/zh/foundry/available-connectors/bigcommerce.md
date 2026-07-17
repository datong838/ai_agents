---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/bigcommerce/",
  "title": "BigCommerce",
  "page_id": "bigcommerce",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/basecamp/",
  "next": "/zh/foundry/available-connectors/bigquery/",
  "scraped_at": "2026-07-13T05:35:13.537084+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# BigCommerce

BigCommerce连接器是一个[Palantir提供的驱动](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。该驱动的官方文档可以在[这里 ↗](https://cdn.cdata.com/help/UBJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，代理必须被允许连接到您选择的系统。这意味着代理必须能够访问目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域名  | 必需 |
|--- |--- |
| login.bigcommerce.com | 始终需要。认证和词元端点 |
| api.bigcommerce.com | 始终需要 |
| store-{STORE\_ID}.mybigcommerce.com | 始终需要。在某些情况下，您插入/更新数据时似乎会使用 |

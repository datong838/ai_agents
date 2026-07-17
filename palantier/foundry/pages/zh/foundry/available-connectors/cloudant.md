---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/cloudant/",
  "title": "Cloudant",
  "page_id": "cloudant",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/certinia/",
  "next": "/zh/foundry/available-connectors/cockroachdb/",
  "scraped_at": "2026-07-13T05:35:27.932736+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Cloudant

Cloudant连接器是一个[Palantir提供的驱动程序](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。该驱动程序的官方文档可以在[此处 ↗](https://cdn.cdata.com/help/EWJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则代理必须被允许连接到您选择的系统。这意味着代理必须能够到达目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保向连接器添加以下出口策略：

| 域名  | 必需 |
|--- |--- |
| \<URL> | 仅当`AuthScheme=OAuth`或使用本地实例（本地实例格式为\<Server>:\<Port>） |
| \<User>.cloudant.com | 仅当`AuthScheme=Basic` |

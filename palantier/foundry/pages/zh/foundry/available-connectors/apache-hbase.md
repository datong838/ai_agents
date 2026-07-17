---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/apache-hbase/",
  "title": "Apache HBase",
  "page_id": "apache-hbase",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/apache-couchdb/",
  "next": "/zh/foundry/available-connectors/apache-hive/",
  "scraped_at": "2026-07-13T05:34:45.536194+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Apache HBase

Apache HBase连接器是[由Palantir提供的驱动](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。此驱动的官方文档可以在[此处 ↗](https://cdn.cdata.com/help/RHJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够到达目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保向连接器添加以下出口策略：

| 域  | 必需 |
|--- |--- |
| \<Server>:\<Port> | 始终 |
| \<KerberosKDC>:88 | 仅当`AuthScheme=Negotiate`时 |
| \<KerberosServiceKDC>:88 | 仅当`AuthScheme=Negotiate`且Kerberos拓扑使用多个领域时 |

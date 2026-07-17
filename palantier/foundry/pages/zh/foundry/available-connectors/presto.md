---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/presto/",
  "title": "Presto",
  "page_id": "presto",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/postgresql/",
  "next": "/zh/foundry/available-connectors/quickbase/",
  "scraped_at": "2026-07-13T05:37:16.929027+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Presto

Presto连接器是一个[Palantir提供的驱动程序](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。该驱动程序的官方文档可以在[这里 ↗](https://cdn.cdata.com/help/ORJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够到达目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域  | 必需 |
|--- |--- |
| \<Server>:\<Port> | 始终。服务器和端口连接属性。默认 `Port=8080` |
| \<KerberosKDC>:88 | 仅当 `AuthScheme=Kerberos` |
| \<KerberosServiceKDC>:88 | 仅当 `AuthScheme=Kerberos` 且 Kerberos 拓扑使用多个领域 |

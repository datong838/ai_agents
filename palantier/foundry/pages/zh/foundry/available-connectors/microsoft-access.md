---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/microsoft-access/",
  "title": "Microsoft Access",
  "page_id": "microsoft-access",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/marklogic/",
  "next": "/zh/foundry/available-connectors/microsoft-ads/",
  "scraped_at": "2026-07-13T05:36:13.750983+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Microsoft Access

Microsoft Access 连接器是一个[由 Palantir 提供的驱动程序](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。此驱动程序的官方文档可以在[此处 ↗](https://cdn.cdata.com/help/DCJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够到达目标 IP 地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域  | 必需 |
|--- |--- |
| \<Server> | 始终。对于 Exchange Online，使用 `Server='https://outlook.office365.com/EWS/Exchange.asmx'` |
| outlook.office365.com | 仅当 `Platform=Exchange_Online` 并且 `Schema=EWS` 时 |
| graph.microsoft.com | 仅当 `Platform=Exchange_Online` 并且 `Schema=MSGraph` 时 |
| login.microsoftonline.com | 仅当 `Platform=Exchange_Online`（默认）并且 `AuthScheme=AzureAD`、AzureServicePrincipal 或 AzureServicePrincipalCert 时 |
| \<KerberosKDC>:88 | 仅当 `AuthScheme=Negotiate` 时 |
| \<KerberosServiceKDC>:88 | 仅当 `AuthScheme=Negotiate` 并且 Kerberos 拓扑使用多个领域时 |

---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/microsoft-onedrive/",
  "title": "Microsoft OneDrive",
  "page_id": "microsoft-onedrive",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/microsoft-office-365/",
  "next": "/zh/foundry/available-connectors/microsoft-onenote/",
  "scraped_at": "2026-07-13T05:36:21.322768+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Microsoft OneDrive

Microsoft OneDrive连接器是[Palantir提供的驱动程序](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。该驱动程序的官方文档可以在[这里 ↗](https://cdn.cdata.com/help/UOJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够访问目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域名  | 必须 |
|--- |--- |
| graph.microsoft.com | 仅当`AzureEnvironment=GLOBAL`（默认）时 |
| login.microsoftonline.com | 仅当`AuthScheme=AzureAD`（默认）、AzureServicePrincipal、AzureServicePrincipalCert且`AzureEnvironment=GLOBAL`时 |
| microsoftgraph.chinacloudapi.cn | 仅当`AzureEnvironment=CHINA`时 |
| login.chinacloudapi.cn | 仅当`AuthScheme=AzureAD`（默认）、AzureServicePrincipal、AzureServicePrincipalCert且`AzureEnvironment=CHINA`时 |
| graph.microsoft.us | 仅当`AzureEnvironment=USGOVT`时 |
| login.microsoftonline.us | 仅当`AuthScheme=AzureAD`（默认）、AzureServicePrincipal、AzureServicePrincipalCert且`AzureEnvironment=USGOVT`或USGOVTDOD时 |
| dod-graph.microsoft.us | 仅当`AzureEnvironment=USGOVTDOD`时 |

---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/azure-synapse/",
  "title": "Azure Synapse",
  "page_id": "azure-synapse",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/azure-devops/",
  "next": "/zh/foundry/available-connectors/azure-table-storage/",
  "scraped_at": "2026-07-13T05:35:10.704147+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Azure Synapse

Azure Synapse连接器是一个[Palantir提供的驱动程序](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。该驱动程序的官方文档可以在[这里 ↗](https://cdn.cdata.com/help/HEJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够访问目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出站策略添加到连接器中：

| 域  | 必须 |
|--- |--- |
| \<Server>:\<Port> | 始终。服务器连接属性 |
| None | 始终。端口连接属性 |
| \<StorageAccountLocation> | 仅用于在COPY模式下暂存数据 |
| login.microsoftonline.com | 仅在`AuthScheme=AzureAD,` AzureServicePrincipal, AzureServicePrincipalCert, AzurePassword 并且 `AzureEnvironment=GLOBAL`（默认）时使用 |
| login.chinacloudapi.cn | 仅在`AuthScheme=AzureAD,` AzureServicePrincipal , AzureServicePrincipalCert, AzurePassword 并且 `AzureEnvironment=CHINA`时使用 |
| login.microsoftonline.us | 仅在`AuthScheme=AzureAD,` AzureServicePrincipal, AzureServicePrincipalCert, AzurePassword 并且 `AzureEnvironment=USGOVT` 或 USGOVTDOD时使用 |

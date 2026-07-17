---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/azure-cosmos-db/",
  "title": "Azure Cosmos DB",
  "page_id": "azure-cosmos-db",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/azure-blob-filesystem/",
  "next": "/zh/foundry/available-connectors/azure-data-catalog/",
  "scraped_at": "2026-07-13T05:35:06.274688+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Azure Cosmos DB

Azure Cosmos DB连接器是一个[Palantir提供的驱动](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。此驱动的官方文档可以在[这里 ↗](https://cdn.cdata.com/help/EHJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够到达目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域名  | 必需 |
|--- |--- |
| \<AccountEndpoint> | 始终。AccountEndpoint连接属性（可能是https://\<Server>:\<Port>格式，也可能是完整URL） |
| login.microsoftonline.com | 仅当`AuthScheme=AzureAD,` AzureServicePrincipal, AzureServicePrincipalCert 且 `AzureEnvironment=GLOBAL`（默认）时 |
| login.chinacloudapi.cn | 仅当`AuthScheme=AzureAD,` AzureServicePrincipal, AzureServicePrincipalCert 且 `AzureEnvironment=CHINA`时 |
| login.microsoftonline.us | 仅当`AuthScheme=AzureAD,` AzureServicePrincipal, AzureServicePrincipalCert 且 `AzureEnvironment=USGOVT`或USGOVTDOD时 |

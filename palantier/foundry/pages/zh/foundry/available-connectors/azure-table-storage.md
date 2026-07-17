---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/azure-table-storage/",
  "title": "Azure Table Storage",
  "page_id": "azure-table-storage",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/azure-synapse/",
  "next": "/zh/foundry/available-connectors/basecamp/",
  "scraped_at": "2026-07-13T05:35:26.387496+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Azure Table Storage

Azure Table Storage 连接器是一个[由Palantir提供的驱动程序](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。该驱动程序的官方文档可以在[这里 ↗](https://cdn.cdata.com/help/CAJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够访问目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域  | 必需 |
|--- |--- |
| \<Account>.table.core.windows.net | 仅当 `Backend=Storage`（默认） |
| \<Account>.table.cosmosdb.azure.com | 仅当 `Backend=CosmosDB` |
| \<Account> | 仅当 `Backend=AzureStack` 或 Emulator，需在 Account 中指定完整URL |
| login.microsoftonline.com | 仅当 `AuthScheme=AzureAD` 且 `AzureEnvironment=GLOBAL`（默认） |
| login.chinacloudapi.cn | 仅当 `AuthScheme=AzureAD` 且 `AzureEnvironment=CHINA` |
| login.microsoftonline.us | 仅当 `AuthScheme=AzureAD` 且 `AzureEnvironment=USGOVT` 或 USGOVTDOD |

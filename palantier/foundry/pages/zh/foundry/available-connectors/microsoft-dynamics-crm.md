---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/microsoft-dynamics-crm/",
  "title": "Microsoft Dynamics CRM",
  "page_id": "microsoft-dynamics-crm",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/microsoft-dynamics-365/",
  "next": "/zh/foundry/available-connectors/microsoft-dynamics-nav/",
  "scraped_at": "2026-07-13T05:36:16.453731+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Microsoft Dynamics CRM

Microsoft Dynamics CRM 连接器是一个[Palantir 提供的驱动程序](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。此驱动程序的官方文档可以在[此处 ↗](https://cdn.cdata.com/help/RMJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够访问目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保向连接器添加以下出口策略：

| 域名  | 必需 |
|--- |--- |
| \<URL> | 始终。URL 连接属性 |
| \<ADFSServer> | 仅当 `CRMVersion='CRM2011+'`（默认）且 `AuthScheme=AzureAD` 时 |
| login.microsoftonline.com | 仅当 `CRMVersion=CRMOnline` 且 `AuthScheme=AzureAD,` AzureServicePrincipal, AzureServicePrincipalCert 且 `AzureEnvironment=GLOBAL`（默认）时 |
| login.chinacloudapi.cn | 仅当 `CRMVersion=CRMOnline` 且 `AuthScheme=AzureAD,` AzureServicePrincipal , AzureServicePrincipalCert 且 `AzureEnvironment=CHINA` 时 |
| login.microsoftonline.us | 仅当 `CRMVersion=CRMOnline` 且 `AuthScheme=AzureAD,` AzureServicePrincipal, AzureServicePrincipalCert 且 `AzureEnvironment=USGOVT` 或 USGOVTDOD 时 |

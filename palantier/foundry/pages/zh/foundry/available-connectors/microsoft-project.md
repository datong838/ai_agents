---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/microsoft-project/",
  "title": "Microsoft Project",
  "page_id": "microsoft-project",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/microsoft-power-bi-xmla/",
  "next": "/zh/foundry/available-connectors/microsoft-sql-server/",
  "scraped_at": "2026-07-13T05:36:26.319181+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Microsoft Project

Microsoft Project连接器是一个[Palantir提供的驱动程序](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。该驱动程序的官方文档可以在[这里 ↗](https://cdn.cdata.com/help/COH/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，代理必须被允许连接到您选择的系统。这意味着代理必须能够到达目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器：

| 域 | 必需 |
|--- |--- |
| \<URL> | 始终 |
| \<SSOLoginURL> | 仅当`AuthScheme=ADFS,` OKTA |
| login.microsoftonline.com | 仅当`AuthScheme=AzureAD,` OAuth且`AzureEnvironment=GLOBAL`（默认） |
| login.chinacloudapi.cn | 仅当`AuthScheme=AzureAD,` OAuth且`AzureEnvironment=CHINA` |
| login.microsoftonline.us | 仅当`AuthScheme=AzureAD,` OAuth且`AzureEnvironment=USGOVT`或USGOVTDOD |
| \<Subdomain>.onelogin.com | 仅当`AuthScheme=OneLogin,`在SSOProperties中设置 |

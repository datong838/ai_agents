---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/veeva-vault/",
  "title": "Veeva Vault",
  "page_id": "veeva-vault",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/twitter-ads/",
  "next": "/zh/foundry/available-connectors/wave-financial/",
  "scraped_at": "2026-07-13T05:39:32.569431+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Veeva Vault

Veeva Vault连接器是一个[Palantir提供的驱动程序](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。该驱动程序的官方文档可以在[此处 ↗](https://cdn.cdata.com/help/SVJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够访问目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域名  | 必需 |
|--- |--- |
| \<URL> | 始终。URL连接属性 |
| login.microsoftonline.com | 仅当`AuthScheme=AzureADOpenID`时 |

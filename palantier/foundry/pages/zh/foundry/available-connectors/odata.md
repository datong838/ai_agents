---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/odata/",
  "title": "OData",
  "page_id": "odata",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/nosql-stores/",
  "next": "/zh/foundry/available-connectors/odoo/",
  "scraped_at": "2026-07-13T05:36:45.681411+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# OData

OData 连接器是一个[Palantir 提供的驱动](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。此驱动的官方文档可以在[此处 ↗](https://cdn.cdata.com/help/RDJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够访问目标 IP 地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域名  | 必需 |
|--- |--- |
| \<URL> | 始终。URL 连接属性 |
| \<FeedURL> | 仅 FeedURL 连接属性 |
| login.microsoftonline.com | 仅当 `AuthScheme=AzureAD` 或 SharePointOnline 且 `SharePointUseSSO=FALSE` 时 |
| \<SharePointSSODomain> | 仅当 `SharePointUseSSO=TRUE` 且 `AuthScheme=SharePointOnline` 且用户的域与 SSO 服务的域不同时 |
| \<KerberosKDC>:88 | 仅当 `AuthScheme=Negotiate` 时 |
| \<KerberosServiceKDC>:88 | 仅当 `AuthScheme=Negotiate` 且 Kerberos 拓扑使用多个领域时 |
| \<OAuthAuthorizationURL> | 仅当 `AuthScheme=OAuth` 时 |
| \<OAuthAccessTokenURL> | 仅当 `AuthScheme=OAuth` 时 |
| \<OAuthRefreshTokenURL> | 仅当 `AuthScheme=OAuth` 时 |
| \<OAuthRequestTokenURL> | 仅当 `AuthScheme=OAuth` 时 |

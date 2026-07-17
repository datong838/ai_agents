---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/certinia/",
  "title": "Certinia",
  "page_id": "certinia",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/cassandra/",
  "next": "/zh/foundry/available-connectors/cloudant/",
  "scraped_at": "2026-07-13T05:35:34.176437+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Certinia

Certinia 连接器是一个[由Palantir提供的驱动程序](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。该驱动程序的官方文档可以在[这里 ↗](https://cdn.cdata.com/help/HFJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够访问目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请务必向连接器添加以下出口策略：

| 域  | 必需 |
|--- |--- |
| test.salesforce.com  | 仅当 `UseSandbox=TRUE` 时 |
| \<Site>.my.salesforce.com | 仅在通过Salesforce进行身份验证时返回 |
| login.salesforce.com | 仅默认 LoginURL，可被 LoginURL 属性覆盖。LoginURL 在 `AuthScheme=Basic,` OAuth, OAuthPassword, OAuthJWT, OAuthPKCE 时使用 |
| \<LoginURL> | 用于替代 login.salesforce.com |
| \<SSOLoginURL> | 仅当 `AuthScheme=Okta,` PingFederate, ADFS 时 |
| \<Subdomain>.onelogin.com | 仅当 `AuthScheme=OneLogin.` \<Subdomain> 在 SSOProperties 中设置 |
| \<SSOExchangeURL> | 仅当 `AuthScheme=Okta,` PingFederate, ADFS, OneLogin, AzureAD 时 |
| \<Resource> | 仅当 `AuthScheme=AzureAD.` \<Resource> 在 SSOProperties 中设置 |
| \<RelyingParty> | 仅当 `AuthScheme=ADFS.` \<RelyingParty> 在 SSOProperties 中设置 |

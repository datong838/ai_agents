---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/sap-concur/",
  "title": "SAP Concur",
  "page_id": "sap-concur",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/sap-cloud-for-customer/",
  "next": "/zh/foundry/available-connectors/sap-fieldglass/",
  "scraped_at": "2026-07-13T05:37:32.465162+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# SAP Concur

SAP Concur 连接器是一个[Palantir 提供的驱动程序](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。该驱动程序的官方文档可以在[这里 ↗](https://cdn.cdata.com/help/FNH/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够访问目标 IP 地址，并且目标系统必须被配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域名  | 必须 |
|--- |--- |
| developer.concur.com | 总是 |
| us2.api.concursolutions.com | 仅在 `UseSandbox=FALSE`（默认）且 `Region=US`（默认）时 |
| www-us2.api.concursolutions.com | 仅在 `UseSandbox=FALSE`（默认）且 `Region=US`（默认）时 - OAuth 授权 URL |
| eu2.api.concursolutions.com | 仅在 `UseSandbox=FALSE`（默认）且 `Region=EU` 时 |
| www-eu2.api.concursolutions.com | 仅在 `UseSandbox=FALSE`（默认）且 `Region=EU` 时 - OAuth 授权 URL |
| cn.api.concurcdc.cn | 仅在 `UseSandbox=FALSE`（默认）且 `Region=CN` 时 |
| www-cn.api.concurcdc.cn | 仅在 `UseSandbox=FALSE`（默认）且 `Region=CN` 时 - OAuth 授权 URL |
| us-impl.api.concursolutions.com | 仅在 `UseSandbox=TRUE` 且 `Region=US`（默认）时 |
| www-us-impl.api.concursolutions.com | 仅在 `UseSandbox=TRUE` 且 `Region=US`（默认）时 - OAuth 授权 URL |
| emea-impl.api.concursolutions.com | 仅在 `UseSandbox=TRUE` 且 `Region=EU` 时 |
| www-emea-impl.api.concursolutions.com | 仅在 `UseSandbox=TRUE` 且 `Region=EU` 时 - OAuth 授权 URL |
| \<GeoLocation> | 仅在 `UseNewOAuthVersion=FALSE` 时 - GeoLocation 属性（除非设置了 OAuthAccessToken，否则自动检索） |
| \<ConcurInstanceURL> | 仅用于较旧的 API 版本（API v1-3） |
| concursolutions.com | 仅在 `UseNewOAuthVersion=FALSE` 且 GeoLocation 为空且 ConcurInstanceURL 为空时 |

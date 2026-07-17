---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/zuora/",
  "title": "Zuora",
  "page_id": "zuora",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/zoho-projects/",
  "next": "/zh/foundry/available-connectors/other-source-types/",
  "scraped_at": "2026-07-13T05:38:22.024376+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Zuora

Zuora连接器是一个[Palantir提供的驱动程序](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。此驱动程序的官方文档可以在[此处 ↗](https://cdn.cdata.com/help/HZJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，代理必须被允许连接到您选择的系统。这意味着代理必须能够到达目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器：

| 域名  | 必需 |
|--- |--- |
| rest.zuora.com | 仅当 `Tet=USProduction` (默认) |
| rest.apisandbox.zuora.com | 仅当 `Tet=USAPISandbox` |
| rest.pt1.zuora.com | 仅当 `Tet=USPerformanceTest` |
| rest.eu.zuora.com | 仅当 `Tet=EUProduction` |
| rest.sandbox.eu.zuora.com | 仅当 `Tet=EUSandbox` |
| rest.na.zuora.com | 仅当 `Tet=USCloudProduction` |
| rest.sandbox.na.zuora.com | 仅当 `Tet=USCloudAPISandbox` |
| rest.test.zuora.com | 仅当 `Tet=USCentralSandbox` |
| rest.test.eu.zuora.com | 仅当 `Tet=EUCentralSandbox` |
| \<URL> | 仅用于US Production复制环境的URL连接属性 |

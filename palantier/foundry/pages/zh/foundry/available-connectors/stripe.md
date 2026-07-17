---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/stripe/",
  "title": "Stripe",
  "page_id": "stripe",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/streak/",
  "next": "/zh/foundry/available-connectors/sugarcrm/",
  "scraped_at": "2026-07-13T05:37:52.533374+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Stripe

Stripe 连接器是一个[由 Palantir 提供的驱动](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。该驱动的官方文档可以在[这里 ↗](https://cdn.cdata.com/help/BOJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够到达目标 IP 地址，目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域名  | 必需 |
|--- |--- |
| api.stripe.com | 始终 |
| files.stripe.com | 仅用于 DownloadQuote、DownloadFile 和 UploadFile 存储过程 |
| connect.stripe.com | 仅当 `AuthScheme=OAuth` 时 |

---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/google-campaign-manager/",
  "title": "Google Campaign Manager",
  "page_id": "google-campaign-manager",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/gmail/",
  "next": "/zh/foundry/available-connectors/google-cloud-storage/",
  "scraped_at": "2026-07-13T05:35:44.551611+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Google Campaign Manager

Google Campaign Manager连接器是一个[由Palantir提供的驱动](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。此驱动的官方文档可在[此处 ↗](https://cdn.cdata.com/help/EPJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，必须允许代理连接到您选择的系统。这意味着代理必须能够到达目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域名  | 是否必需 |
|--- |--- |
| ads.google.com | 总是 |
| admanager.google.com | 总是 |
| accounts.google.com | 总是。用于OAuth |

---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/facebook-ads/",
  "title": "Facebook 广告",
  "page_id": "facebook-ads",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/facebook/",
  "next": "/zh/foundry/available-connectors/freshbooks/",
  "scraped_at": "2026-07-13T05:35:40.972025+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Facebook 广告

Facebook 广告连接器是一个[Palantir 提供的驱动](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。该驱动的官方文档可以在[此处 ↗](https://cdn.cdata.com/help/HRJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够到达目标 IP 地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请务必将以下出口策略添加到连接器中：

| 域名  | 必须 |
|--- |--- |
| graph.facebook.com | 始终 |

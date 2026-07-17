---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/zoho-creator/",
  "title": "Zoho Creator",
  "page_id": "zoho-creator",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/zoho-books/",
  "next": "/zh/foundry/available-connectors/zoho-crm/",
  "scraped_at": "2026-07-13T05:38:18.718412+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Zoho Creator

Zoho Creator 连接器是一个[由Palantir提供的驱动程序](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。此驱动程序的官方文档可以在[这里 ↗](https://cdn.cdata.com/help/KCJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，必须允许代理连接到您选择的系统。这意味着代理必须能够到达目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域  | 必需 |
|--- |--- |
| \<APIDomain> - 默认: creatorapp.zoho.\<Region> | 总是。区域连接属性映射到顶级域名（默认 `Region=US` --> .com）；在手动设置OAuthAccessToken时可以使用APIDomain |
| \<AccountsServer> - 默认: accounts.zoho.\<Region> | 总是。通过OAuth流程自动检索；在手动提供OAuthAccessToken时设置于AccountsServer连接属性中 |

### 区域映射

使用以下区域映射完成域URL：

| 区域  | 终端 |
|--- |--- |
| 美国 | .com |
| 欧洲 | .eu |
| 印度 | .in |
| 澳大利亚 | .com.au |
| 日本 | .jp |
| 中国 | .com.cn |

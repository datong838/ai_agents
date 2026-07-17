---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/sap/create-sap-rfc-connection/",
  "title": "创建RFC连接",
  "page_id": "create-sap-rfc-connection",
  "category_id": "data-integration",
  "section_id": "sap",
  "previous": "/zh/foundry/sap/configure-sap-slt/",
  "next": "/zh/foundry/sap/uninstall-sap/",
  "scraped_at": "2026-07-13T05:38:39.547686+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 创建RFC连接

在本节中，将创建一个RFC目标连接，以用于从远程SAP系统提取数据。

1. 要创建RFC连接，输入`SM59`事务代码。
2. 创建一个新的ABAP连接，并选择`3`作为连接类型。
3. 在**技术设置**选项卡中，根据SAP源系统（如ECC实例）的值填写**目标主机**和**系统编号**。
4. 在**登录与安全**选项卡中，填写登录凭证和客户端号码（三位数）。SAP在同一张表中存储测试和生产数据，并使用一个**客户端 (MANDT)** 列来使不同的客户端（例如，测试和生产）仅检索相关的客户端数据。对于生产环境，输入生产客户端的客户端号码。
5. 保存连接配置。
6. 从应用工具栏授权测试并测试连接。

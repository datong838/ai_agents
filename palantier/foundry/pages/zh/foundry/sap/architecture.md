---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/sap/architecture/",
  "title": "架构",
  "page_id": "architecture",
  "category_id": "data-integration",
  "section_id": "sap",
  "previous": "/zh/foundry/sap/overview/",
  "next": "/zh/foundry/sap/download-sap-addon/",
  "scraped_at": "2026-07-13T05:38:29.667263+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 架构

连接Foundry到SAP系统有三种主要的架构模式。所有三种模式都遵循标准的[数据连接架构](/zh/foundry/data-connection/architecture/)并使用[数据连接代理](/zh/foundry/data-connection/core-concepts/#agents)。

## 直接连接到SAP ERP或BW系统

在这种情况下，Palantir Foundry 以 SAP 应用程序的连接器2.0（“连接器”）直接安装在包含要读取的数据或托管要执行的函数/查询的SAP ERP或业务仓库（BW）系统上。

![直接连接](../../../images/foundry/sap/sap-architecture-direct-connection.png)

## 通过SAP SLT复制服务器连接到SAP ERP系统

在这种情况下，连接器安装在SAP SLT复制服务器上，并在该服务器与源ERP系统之间建立远程函数调用（RFC）连接。根据数据库触发器，将数据从每个源ERP表复制到SLT系统中的相应操作增量队列（ODQ）。

![SLT连接](../../../images/foundry/sap/sap-architecture-slt-connection.png)

## 通过网关连接到远程SAP ERP系统

当源ERP系统不满足安装连接器的最低要求（SAP NetWeaver版本7.4 SP5或以上）时，此场景适用。在这里，连接器的主要组件安装在满足最低要求的“网关”应用服务器上，并在该服务器与源ERP系统之间建立RFC连接。连接器的远程代理组件安装在源ERP系统上，促进数据读取或函数/查询的执行。

![远程连接](../../../images/foundry/sap/sap-architecture-remote-connection.png)

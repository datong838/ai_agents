---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/sap/uninstall-sap/",
  "title": "卸载 Palantir Foundry Connector 2.0 for SAP Applications 或远程代理",
  "page_id": "uninstall-sap",
  "category_id": "data-integration",
  "section_id": "sap",
  "previous": "/zh/foundry/sap/create-sap-rfc-connection/",
  "next": "/zh/foundry/sap/sap-cockpit/",
  "scraped_at": "2026-07-13T05:38:38.787341+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 卸载 Palantir Foundry Connector 2.0 for SAP Applications 或远程代理

:::callout{theme="neutral"}
在卸载之前，运行 `SA38`，然后运行 `/PALANTIR/UNINSTALL_CORR` 程序，以更正 Palantir Foundry Connector 2.0 for SAP Applications（“Connector”）组件（**PALANTIR**、**PALCONN**、**PALAGENT**）的目录条目。
:::

使用 `SAINT`（SAP 附加组件安装工具）卸载 Connector。请注意，根据您的具体情况，**PALAGENT** 可能在 Connector 安装中不可用。

先卸载 **PALCONN** 和 **PALAGENT**，或者一起卸载所有组件。如果您尝试单独卸载 **PALANTIR**（Palantir Foundry Foundation）组件，`SAINT` 将会出错，因为 **PALAGENT** 和 **PALCONN** 依赖于 **PALANTIR**。

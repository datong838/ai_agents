---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/sap/install-sap-support-package/",
  "title": "安装支持包",
  "page_id": "install-sap-support-package",
  "category_id": "data-integration",
  "section_id": "sap",
  "previous": "/zh/foundry/sap/install-sap-remote-agent-620/",
  "next": "/zh/foundry/sap/install-sap-fixpack/",
  "scraped_at": "2026-07-13T05:38:31.521994+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 安装支持包

支持包是初始安装包后提供的错误修复和新功能的集合。每个支持包都需要以前的支持包作为前提条件，或在SP01的情况下，前提条件是初始安装。

对于Palantir Foundry Connector 2.0以用于SAP应用程序（“Connector”），应通过SPAM（Support Package Manager）遵循标准支持包安装程序。

:::callout{theme="warning"}
在支持包安装期间，暂停后台任务调度和所有使用Connector的Foundry数据同步。不这样做可能会导致由于后台进程持有的数据库锁而导致安装失败。
:::

使用SAR格式的安装文件（`FOUNDRY-SAPCONN-INST-SP00SPXX.SAR`）。`XX`代表支持包级别。根据系统上安装的支持包级别，SPAM将加载必要的文件以执行升级。

1. [下载安装包](/zh/foundry/sap/download-sap-addon/)。
2. 使用有权使用SPAM的用户登录到SAP系统客户端000。
3. 运行SPAM事务。
4. 从应用程序服务器导入包。
5. 要导入，请从工具栏菜单中选择**安装包** > **加载包** > **从前端**。
6. 定义支持包安装的队列。

:::callout{theme="neutral"}
所有Connector组件应一起升级。一起升级`PALCONN`和`PALANTIR`或`PALANTIR`和`PALAGENT`组件。
:::

7. 选择应用程序组件。要一起升级PALANTIR组件，请选择**所有组件**，然后仅选择PALANTIR组件到所需的支持包级别。确保未选择其他组件进行升级过程。
8. 在**SPAM: Import: Queue**对话框中，将**准备**设置为*在对话框中启动*，其他所有步骤设置为*在后台继续*。

:::callout{theme="neutral"}
如果在安装过程中出现警告，请按照警告信息中描述的步骤进行解决。在大多数情况下，安装Connector和远程代理时可以忽略警告信息。特别是，标题为“打开数据提取请求”的警告信息可以安全地忽略。
:::

9. 导入成功完成后，确认队列。

保持`SPAM/SAINT` SP级别和`tp/R3Trans`补丁的更新非常重要。如果在`DDIC_ACTIVATION`期间出现问题，请使用SAP的批量激活程序（`RADMASG0`）并启用**强制激活标志**。

:::callout{theme="danger"}
支持包之间可能会有SAP安全更新，导致添加新的授权对象。因此，如果使用自定义角色，强烈建议比较`/PALANTIR/*`角色与自定义角色的内容。如果使用`/PALANTIR/*`角色，确保所有用户比较已完成，授权配置文件已生成并为绿色。
:::

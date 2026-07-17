---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-connection/webhooks-overview/",
  "title": "概述",
  "page_id": "webhooks-overview",
  "category_id": "data-integration",
  "section_id": "data-connection",
  "previous": "/zh/foundry/data-connection/export-tasks/",
  "next": "/zh/foundry/data-connection/webhooks-setup/",
  "scraped_at": "2026-07-13T05:32:00.052823+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

您可以使用Data Connection配置**Webhooks**，以将Foundry连接到Foundry之外的系统和工作流。

每个Webhook提供了一种向Palantir Foundry外部系统发出请求的方法。例如，您可以创建一个Webhook，当用户在Foundry应用程序中选择一个按钮时，它会对外部服务器执行一个HTTP请求，从而将该应用程序连接到现有工作流和源系统。

每个Webhook在Data Connection中与单个[源](/zh/foundry/data-connection/core-concepts/#sources)相关联。源存储连接到外部系统所需的凭据。根据Webhook关联的源的类型，某些任务类型可供使用。例如，在使用[REST](/zh/foundry/available-connectors/rest-apis/)时，您可以灵活地配置应向外部服务发出的HTTP调用。

可以灵活配置Webhooks以接受特定输入并捕获外部系统请求的输出。此外，您可以设置Webhook执行的时间、并发性和速率限制。有关详细的配置选项，请参阅[Webhooks参考](/zh/foundry/data-connection/webhooks-reference/)。

请参阅文档的以下部分以了解有关Webhooks的更多信息：

* 按照教程[设置Webhook](/zh/foundry/data-connection/webhooks-setup/)。
* 查看[Webhooks参考](/zh/foundry/data-connection/webhooks-reference/)以了解更多关于配置、限制和权限的信息。
* 查看[操作文档](/zh/foundry/action-types/webhooks/)以了解如何为终端用户应用程序配置Webhooks。
* 了解如何从[外部函数](/zh/foundry/data-integration/external-functions/)调用webhooks，以编写自定义代码与外部系统交互。

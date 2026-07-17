---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-connection/webhooks-setup/",
  "title": "设置 Webhook",
  "page_id": "webhooks-setup",
  "category_id": "data-integration",
  "section_id": "data-connection",
  "previous": "/zh/foundry/data-connection/webhooks-overview/",
  "next": "/zh/foundry/data-connection/webhooks-reference/",
  "scraped_at": "2026-07-13T05:32:03.810242+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 设置 Webhook

本教程指导您如何设置 webhooks 以发送 HTTP 请求到外部系统。

## 前提条件

本教程将逐步讲解如何创建 REST API 源以及与该源相关联的 webhook。如果您已经创建了一个源，可以直接跳到[创建 webhook](#create-a-webhook)步骤。

:::callout{theme="warning"}
如果您尝试连接到无法从互联网访问的系统，则必须按照额外的步骤来配置代理代理或代理工作器运行时并添加证书。代理运行时是一个高级概念，配置和管理起来比较复杂。在可能的情况下，我们建议使用直接连接。

有关如何开始使用代理运行时的更多信息，请参考以下指南：

* [设置代理](/zh/foundry/data-connection/set-up-agent/)
* [添加证书](/zh/foundry/data-connection/agent-configuration-reference/#certificates)

在生产环境中使用代理运行时的 webhooks 时，我们建议为 webhooks 提供专用代理。代理按接收顺序执行任务，如果批量同步和 webhooks 在同一代理上执行，短时间运行的 webhook 任务可能会排队等待长时间运行的批量同步。
:::

确保您拥有一个[项目](/zh/foundry/getting-started/projects-and-resources/)来管理将在本教程中创建的源的权限。如果您尚未创建项目，请在[项目文档](/zh/foundry/projects/create/)中了解如何创建。

## 教程

本教程假定您将使用开放互联网系统上的 REST API。

:::callout{theme="neutral"}
一些源，包括 SAP、旧版 Salesforce 和旧版 `magritte-rest-v2` 使用更复杂的任务配置。有关配置 webhook 任务的更多信息，请参阅[webhooks 参考](/zh/foundry/data-connection/webhooks-reference/)。
:::

### 创建源

首先导航到**数据连接**并选择**源**选项卡。然后，选择**新建源**和**REST API**。

![新建 REST API 源](../../../images/foundry/data-connection/webhooks-rest-api-new-source.png)

使用源编辑器填写您要连接的 REST API 的配置详情。有关 REST API 源类型的更多详细信息，请参阅[源类型参考](/zh/foundry/available-connectors/rest-apis/)。

该源旨在包含建立连接所需的最小秘密和连接详细信息。在使用此源配置单个 webhooks 时，您将有机会添加附加请求详细信息，包括相对路径、查询参数、头信息和正文内容。

#### 其他源类型

其他一些源类型也支持 webhooks。有关更多详细信息，请查看特定源类型的[参考页面](/zh/foundry/data-integration/source-type-overview/)。

### 创建 webhook

一旦创建了源，选择**Webhooks**选项卡并选择**新建 webhook**。

![新建 webhook](../../../images/foundry/data-connection/webhooks-new-webhook.png)

按照**新建 webhook 向导**中的步骤创建一个发出外部请求的 webhook。下面的示例展示了一个 `POST` 请求到我们的示例域名上的 `/api/v1/createItem` 端点。正文构建为原始 JSON，在此情况下，配置为接受两个字符串输入参数。

![新建 webhook](../../../images/foundry/data-connection/webhooks-setup-wizard-example.png)

### 配置选项

1. 输入 webhook 的名称，并根据需要添加描述。
2. 选择您在本教程的上一步中创建的源。如果您直接从源页面进入向导，源将会被预先选择。
3. 添加您希望在外部请求中使用的任何输入参数。
4. 填写请求配置中的任何必填部分。您可以在路径、查询参数、头信息和正文配置部分引用输入参数。
5. 非必填地，设置您希望应用于 webhook 的任何**限制**。有关详细信息，请参阅[限制参考](/zh/foundry/data-connection/webhooks-reference/#limits)。
6. 点击**创建**以完成 webhook 的创建。

#### 从 cURL 命令直接导入

或者，您也可以通过直接导入 cURL 命令来创建请求操作。为此，请选择**从 cURL 导入**选项并将您的 cURL 命令放入文本区域。如果您的 cURL 使用支持的选项并与源中已存在的域相关，选择**导入 cURL** 将创建一个新操作。

### 测试 webhook

保存后，您可以运行测试请求以查看您的配置是否正确。这可以随时通过使用**测试连接**侧面板完成。

在进行测试请求后，您可以使用响应解析输出参数。有关输出参数的更多信息，请参阅[webhooks 参考页面](/zh/foundry/data-connection/webhooks-reference/#output-parameters)。

### 下一步

在本教程中，您学习了如何创建源以及创建与该源相关联的 Webhook。以下是我们推荐的学习更多内容的资源：

* 查看[操作类型教程](/zh/foundry/action-types/set-up-webhook/)以了解如何配置 Webhook 以供最终用户应用程序使用。
* 阅读[Webhooks 参考](/zh/foundry/data-connection/webhooks-reference/)，查看有关配置 Webhooks 可用选项的详细信息。

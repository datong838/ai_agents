---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-integration/external-functions/",
  "title": "外部函数",
  "page_id": "external-functions",
  "category_id": "data-integration",
  "section_id": null,
  "previous": "/zh/foundry/data-integration/external-transforms-source-based/",
  "next": "/zh/foundry/data-integration/source-type-overview/",
  "scraped_at": "2026-07-13T05:35:37.579549+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 外部函数

外部函数允许您从一个函数调用[webhooks](/zh/foundry/data-connection/webhooks-overview/)，并使用它们与外部系统交互。您可以从使用[Workshop](/zh/foundry/workshop/overview/)、[操作](/zh/foundry/action-types/overview/)和[函数](/zh/foundry/functions/overview/)构建的应用程序中调用这些系统。

要在函数中使用webhook，您必须首先配置支持webhooks功能的[数据连接源](/zh/foundry/data-connection/set-up-source/)。通常这将是一个[REST API源](/zh/foundry/available-connectors/rest-apis/#rest-api-source)。一旦您有了配置了webhooks的源，您可以将该源导入到您的[函数库](/zh/foundry/functions/getting-started/)中，并创建调用webhooks和其他逻辑的函数。

您可以将外部函数应用于各种应用案例，包括以下内容：

* 使用一个单一函数向外部服务器发出HTTP请求并创建记录，然后将匹配的记录写入Ontology。
* 将webhook调用包裹在自定义前后处理逻辑中。如果需要从函数输入到所需webhook请求输入参数的自定义逻辑，或者在进行Ontology编辑之前需要对webhook响应进行后处理，这将特别有用。
* 使用中间处理逻辑将多个外部webhook请求和Ontology编辑连接在一起。单个webhook无法执行动态数量的外部请求，但可以使用外部函数来实现。
* 使用只读请求查询外部系统，以在Workshop应用程序中暂时呈现数据。

:::callout{theme="neutral"}
目前外部函数可能无法直接从TypeScript代码中进行任意API调用，而不首先在数据连接中将请求定义为webhook。
:::

## 概念

* [数据连接源](/zh/foundry/data-connection/set-up-source/)表示与外部系统的连接，包括如何到达该系统的任何配置（例如网络详细信息），以及安全存储的凭据。
* [Webhooks](/zh/foundry/data-connection/webhooks-overview/)是某些源类型支持的一项功能，允许您构建结构化请求以交互方式运行并向该系统发送请求。
* [Ontology编辑函数](/zh/foundry/functions/api-ontology-edits/)是一个[函数](/zh/foundry/functions/overview/)，可以稍后配置为[基于函数的操作](/zh/foundry/action-types/function-actions-overview/)以写回到一个对象。它使用`@OntologyEditFunction()`装饰器进行注释。
* [查询函数](/zh/foundry/functions/query-functions/)是一个只读函数，不能有任何副作用，比如改变外部系统。它使用`@Query()`装饰器进行注释。

## 设置指南

在以下设置指南中，我们将逐步创建一个调用[免费公共词典API ↗](https://dictionaryapi.dev/)的webhook。如果您已经有一个配置了webhooks的现有源，请继续前往[函数中的外部源](/zh/foundry/functions/external-sources/)以从函数中调用webhooks。

:::callout{theme="neutral"}
此处说明的词典API与Palantir无关，可能随时更改。本教程不构成对生产应用案例使用此API的认可、推荐或建议。
:::

### 创建数据连接源

要从函数连接到外部系统，您必须具有一个可以连接到所需外部API的REST API源。您可以按照以下说明配置新的REST API源。

1. 导航到Foundry中的数据连接应用程序并选择**新建源**。从选项列表中选择**REST API**。

![数据连接新源页面，红色框选中的REST API卡片](../../../images/foundry/data-integration/external-functions-choose-rest-api-source.png)

2. 查看**概览**页面，然后选择右下角的**继续**。系统将提示您选择连接运行时：直接连接，通过代理或通过代理代理。直接连接是与互联网可访问的任何事物交互时的首选方法，我们将使用它连接到我们的免费词典API。

3. 为您的源选择一个名称，并选择应保存到的项目。

4. 在**域**部分填写API源的连接信息。我们的免费词典API示例的配置如下所示：

![REST API源创建页面，显示连接到api.dictionaryapi.dev的配置，无需任何身份验证](../../../images/foundry/data-integration/external-functions-configure-dictionary-api-source.png)

5. 对于此示例，我们还需要创建必要的出口策略。如果您完成了上一步，策略将在**网络连接**部分中自动建议：

![建议出口面板，显示针对api.dictionaryapi.dev端口443的建议策略](../../../images/foundry/data-integration/external-functions-suggested-egress-for-dictionary-api.png)

6. 选择**保存**，然后选择**保存并继续**以完成源设置。在我们配置要在此源上使用的webhook之前，请返回源的**概览**页面并确保设置了API名称。此名称用于在代码中引用源。

![设置源API名称的对话框，显示API名称为MyDictionarySource](../../../images/foundry/data-integration/external-functions-set-api-name-for-source.png)

### 在数据连接源上创建webhook

现在，您必须在之前配置的REST API源上设置webhook。在您可以从函数中调用webhook之前，您必须配置webhook并为其指派API名称。一个数据连接源可能有多个与之关联的webhooks。请注意，您的源API名称在命名空间中应是唯一的，并且webhook API名称在源中必须是唯一的。

请按照以下步骤配置一个webhook，以请求词典API来获取单个单词的定义。

1. 在源的**概览**页面上，选择**创建webhook**。为webhook命名、描述并指定API名称。与API源一样，我们将在代码中引用webhook。

![新webhook页面，显示名为getDefinition的webhook](../../../images/foundry/data-integration/external-functions-create-dictionary-api-webhook.png)

2. 定义一个在执行webhook时传入的参数。在我们的示例中，我们将使用一个单一字符串输入参数`wordToDefine`。

![API源中的webhook配置屏幕](../../../images/foundry/data-integration/external-functions-create-dictionary-api-webhook-input.png)

3. 现在，在URL中填入词典资源路径，并在最后引用输入参数，如下所示：

![词典API资源路径，添加输入参数以返回正确的数据。](../../../images/foundry/data-integration/external-functions-create-dictionary-api-webhook-call.png)

在我们的示例中，API是一个不修改任何数据的GET请求。因此，我们将保留默认设置`Read API`，允许webhook在两种类型的函数中使用：`@Query()`和`@OntologyEditFunction()`。标记为`Write API`的webhooks可能只能在`@OntologyEditFunction()`中使用。

4. 在下一页面，您将看到一个面板，允许您以当前配置执行webhook。如果您运行webhook，您将看到未解析的响应：

![API源webhook响应测试。](../../../images/foundry/data-integration/external-functions-dictionary-api-webhook-test-connection.png)

5. Webhooks允许从外部系统返回的响应对象中提取字段，并根据类型化模式解析字段。在此示例中，我们将提取每个返回词性的一组定义。运行webhook以确保对常见单词（例如“technology”）返回一些输出。

一旦保存了webhook，它便可在整个平台上使用。

[了解更多关于webhook配置选项和用法的信息。](/zh/foundry/data-connection/webhooks-reference/)。

### 下一步

要开始在函数中使用此源，请继续查看[函数中的外部源指南](/zh/foundry/functions/external-sources/)。

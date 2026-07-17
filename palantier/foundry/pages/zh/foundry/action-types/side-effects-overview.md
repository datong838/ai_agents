---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/action-types/side-effects-overview/",
  "title": "概述",
  "page_id": "side-effects-overview",
  "category_id": "ontology",
  "section_id": "action-types",
  "previous": "/zh/foundry/action-types/function-actions-getting-started/",
  "next": "/zh/foundry/action-types/notifications/",
  "scraped_at": "2026-07-14T04:28:13.188495+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

操作类型旨在支持组织内的全范围决策过程。当Ontology作为决策过程的记录系统时，使用[规则](/zh/foundry/action-types/rules/)定义Object修改可以让您灵活地表达业务流程。为了支持全范围的组织流程，操作类型支持一些额外的功能：

* 对于实时流程，您可能需要*通知*用户系统中正在发生的更改，以便他们可以采取相应的操作。
* 在Foundry之外的系统是您组织的真实数据源的情况下，您可能需要与其他系统*集成*以支持现有的业务流程。这种模式有时被称为"决策编排"。

操作类型中的**副作用**使您能够将数据从Foundry发送出去，以集成现有的组织流程。副作用主要有两种类型：

* [通知](/zh/foundry/action-types/notifications/)允许您灵活配置在应用操作时如何通知用户。这包括向平台上的用户发送电子邮件的能力。
* [Webhooks](/zh/foundry/action-types/webhooks/)允许您以高度灵活的方式连接到Foundry外部的系统，包括向REST API或ERP系统发送请求。这使您能够写入组织中的其他源系统，或者通过与消息传递系统集成更灵活地向用户发送通知。

您可以使用上面的链接了解更多关于通知和Webhooks的信息，或查看这些指南以开始：

* [设置通知](/zh/foundry/action-types/set-up-notification/)
* [设置Webhook](/zh/foundry/action-types/set-up-webhook/)

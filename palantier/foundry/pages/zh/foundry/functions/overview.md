---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/functions/overview/",
  "title": "概述",
  "page_id": "overview",
  "category_id": "ontology",
  "section_id": "functions",
  "previous": "/zh/foundry/action-types/marketplace-action-types/",
  "next": "/zh/foundry/functions/getting-started/",
  "scraped_at": "2026-07-14T04:28:49.078480+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

**函数**使代码作者能够编写可以在操作环境中快速执行的逻辑，例如仪表盘和应用程序，旨在支持决策过程。此逻辑在服务器端的隔离环境中执行。

值得注意的是，函数包括对基于Foundry Ontology编写逻辑的一流支持。这包括支持读取各种Object类型的属性、遍历链接以及灵活进行Ontology编辑。

函数的常见应用案例包括：

* 返回对象集或变量值以在[Workshop](/zh/foundry/workshop/functions-use/)中使用。
* 使用[Workshop的函数支持列](/zh/foundry/workshop/widgets-object-table/#derived-properties-or-functions-backed-columns)在派生表列中显示变换值。
* 聚合Object类型值以显示为[Workshop图表](/zh/foundry/workshop/widgets-chart/#function-aggregations-function-backed-layers)。
* 通过[函数支持操作](/zh/foundry/action-types/function-actions-overview/)表达对Ontology的复杂编辑，以更新多个Object。
* 在后端运行逻辑以返回信息在[Slate](/zh/foundry/slate/overview/)的前端显示。
* 计算自定义指标或聚合以在[Quiver](/zh/foundry/quiver/overview/)中显示。
* 通过[外部函数](/zh/foundry/functions/external-sources/)查询外部系统以丰富Ontology中的Object。

函数支持的语言为[TypeScript ↗](https://www.typescriptlang.org/docs/handbook/basic-types.html)和[Python (Beta)↗](https://www.python.org/)。

要在Foundry中开始使用函数，我们推荐以下教程：

* [TypeScript入门](/zh/foundry/functions/getting-started/)
* [(Beta) Python入门](/zh/foundry/functions/python-getting-started/)

## 函数功能支持的语言

:::callout{theme="warning"}
并非所有功能都支持这两种语言。请参阅下表以了解特定功能的语言支持。
:::

| 函数功能                          | 支持于TypeScript | 支持于Python | 描述                                                                                         |
|-----------------------------------|-----------------|--------------|---------------------------------------------------------------------------------------------|
| Ontology Object支持               | 是              | 是           | 在函数中[访问Ontology Object](/zh/foundry/functions/foo-getting-started/)的能力。                             |
| Ontology编辑支持                  | 是              | 是           | 在函数中[编辑Ontology Object](/zh/foundry/functions/edits-overview/)的能力。                                  |
| 可在Workshop中查询                 | 是              | 是           | 从[Workshop应用](/zh/foundry/workshop/functions-use/)调用函数。                                     |
| 可在Pipeline Builder中使用       | 否              | 是           | 从[Pipeline Builder管道](/zh/foundry/functions/python-functions-builder/)调用函数。                            |
| 对模型的函数支持                   | 是              | 否           | 编写可以[嵌入模型中的函数](/zh/foundry/functions/model-functions/)。                                           |
| 语义搜索支持                      | 是              | 否           | 使用函数创建向量以进行[语义搜索](/zh/foundry/functions/overview-semantic-search/)。                            |
| 外部API调用支持                   | 是              | 否           | 从[函数内部查询外部服务](/zh/foundry/functions/external-sources/)。                                            |
| 无服务器执行支持                  | 是              | 否           | 无服务器函数将在调用时按需启动。                                                             |
| 部署执行支持                      | 否              | 是           | 部署的函数将分配专用资源，准备好处理请求。                                                  |
| 从API网关调用函数支持             | 是              | 是           | 可以从API网关命中[查询函数](/zh/foundry/functions/query-functions/)。                                         |
| Marketplace支持                  | 是              | 否           | 能够通过[Marketplace](/zh/foundry/marketplace/overview/)打包和发布函数。                           |

## 无服务器函数超时

目前，每个无服务器函数分配了总共60秒的墙时运行时间。这包括30秒的CPU时间和30秒的网络延迟缓冲。如果超时，函数将失败。

## 部署函数超时

目前，每个部署函数分配了总共60秒的墙时运行时间。如果超时，函数将失败。

---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/object-edits/overview/",
  "title": "Object编辑和物化",
  "page_id": "overview",
  "category_id": "ontology",
  "section_id": "object-edits",
  "previous": "/zh/foundry/object-indexing/faq/",
  "next": "/zh/foundry/object-edits/how-edits-applied/",
  "scraped_at": "2026-07-14T05:09:12.375164+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Object编辑和物化

Foundry Ontology通过结合来自各种数据源的数据和用户驱动的Object编辑，支持操作流程，帮助生成洞察，并维护对您重要事物的最新表示。在Foundry Ontology中，用户可以通过应用[操作](/zh/foundry/action-types/overview/)编辑属性值、添加和删除链接以及创建和删除Object。

Foundry中的操作是一个单一事务，根据用户定义的逻辑更改一个或多个Object的属性。操作使您能够在思考整体目标的同时使用和管理数据，而不是追逐特定的属性编辑。操作可以从Foundry应用程序（如[Workshop](/zh/foundry/workshop/actions-use/)和[Object视图](/zh/foundry/object-views/overview/)）或通过[Foundry APIs](/zh/foundry/action-types/use-actions/)从外部应用程序触发。有关如何配置和应用操作的更多信息，请参见[操作文档](/zh/foundry/action-types/overview/)。

本节的其他页面讨论了启用操作所需的Object类型和链接类型配置，以及Ontology中支持用户驱动编辑的基础机制。

:::callout{theme="warning"}
[具有Foundry流数据源的Object类型](/zh/foundry/object-permissioning/managing-object-security/#object-input-datasources)尚不支持操作
:::

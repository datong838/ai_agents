---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/object-views/generate-urls/",
  "title": "生成Object视图URL",
  "page_id": "generate-urls",
  "category_id": "ontology",
  "section_id": "object-views",
  "previous": "/zh/foundry/object-views/widgets-apps-files/",
  "next": "/zh/foundry/object-views/comment-on-objects/",
  "scraped_at": "2026-07-14T04:37:39.686242+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 生成Object视图URL

在开发Object视图的过程中，您可能需要生成指向特定Object或搜索Object的URL。

如果您是在iframe中嵌入这些视图而不是将它们作为链接提供，请附加URL查询参数`embedded=true`，这将加载没有Workspace侧边栏的视图。

:::callout{theme="neutral"}
要了解如何创建指向搜索或Exploration的URL，请参阅[生成Object Explorer URL](/zh/foundry/object-explorer/generate-urls/)。
:::

## 生成Object链接

有两种方法可以链接到URL。

**选项1**

`/workspace/hubble/external/object/v0/<object-type-id>?<primary-key-property-id>=<primary-key-property-value>`

例如：

`/workspace/hubble/external/object/v0/aircraft?aircraftId=1234`

**选项2**

`/workspace/hubble/external/search/v2/?objectId=<objectRid>`

当主键属性值可能包含特殊字符时，推荐使用这种方式。

此URL在Object Explorer的上下文中加载Object视图。要加载没有额外包装的Object视图（例如，用于iframe中），请创建类似`/workspace/hubble/objects/<objectRid>`的URL。

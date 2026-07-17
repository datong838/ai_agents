---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/object-edits/user-edit-history/",
  "title": "启用用户编辑历史",
  "page_id": "user-edit-history",
  "category_id": "ontology",
  "section_id": "object-edits",
  "previous": "/zh/foundry/object-edits/how-edits-applied/",
  "next": "/zh/foundry/object-edits/permission-checks/",
  "scraped_at": "2026-07-14T05:09:34.140664+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 启用用户编辑历史

追踪用户对索引到Object Storage V2中的Objects的编辑历史。可以在Ontology Manager的**数据源**选项卡中使用**跟踪用户编辑历史**切换按钮启用或禁用此功能，如下图所示。

![跟踪用户编辑历史切换按钮](../../../images/foundry/object-edits/track-user-edits-history.png)

为了允许用户编辑，必须启用[编辑切换](/zh/foundry/object-edits/how-edits-applied/)。

## 常见问题和注意事项

* 编辑历史反映启用**跟踪用户编辑历史**后对Objects所做的更改。启用此功能之前的任何更改都不会被跟踪。
* 一旦启用**跟踪用户编辑历史**，需要几分钟的时间来初始化。在这段短时间内，用户无法对这些Objects执行操作。
* 目前，不支持从Object Storage V1迁移用户编辑历史到Object Storage V2。因此，Object Storage V1中跟踪的任何编辑历史在过渡到Object Storage V2后将丢失。
* 当前不支持跟踪对权限标记属性的用户编辑。
* 拥有Object当前状态访问权限的用户（具有相同主键的Object）可以访问Object的整个历史。这意味着如果一个Object被删除并重新创建，用户仍然可以看到删除操作前发生的历史。

启用**跟踪用户编辑历史**后，可以将[编辑历史微件](/zh/foundry/workshop/widgets-edits-history/)添加到Workshop模块或Workshop支持的Object视图中，以显示编辑历史。

## 禁用编辑历史

禁用**跟踪用户编辑历史**将永久删除该Object类型的所有现有编辑历史。在保存Ontology之前，用户将收到警告，并且必须确认编辑历史将被删除的声明。

![禁用用户编辑历史切换按钮](../../../images/foundry/object-edits/disable-edits-history.png)

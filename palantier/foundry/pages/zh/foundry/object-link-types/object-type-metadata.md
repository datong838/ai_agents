---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/object-link-types/object-type-metadata/",
  "title": "元数据参考",
  "page_id": "object-type-metadata",
  "category_id": "ontology",
  "section_id": "object-link-types",
  "previous": "/zh/foundry/object-link-types/enable-gotham-integration/",
  "next": "/zh/foundry/object-link-types/properties-overview/",
  "scraped_at": "2026-07-14T04:25:09.003264+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 元数据参考

在Ontology中，一个Object类型由以下元数据表示：

* **ID：** Object类型的唯一标识符，主要用于在配置应用程序时引用此类型的对象。例如，`employee`可能是`Employee` Object类型的ID。
* **RID：** Foundry中每个资源自动生成的唯一标识符。Object类型的RID将在平台上的错误消息中引用。
* **图标：** 用于作为Object类型的视觉标识符的图片和颜色，当用户查看此类型的对象时将在用户应用程序中出现。例如，人物图标可能用于描绘`Employee` Object类型。
* **显示名称：** 在用户应用程序中访问此类型对象的任何人显示的名称。例如，`Employee` Object类型的显示名称可能是`Employee`。
* **复数显示名称：** 在用户应用程序中访问多个此类型对象的任何人显示的名称。例如，`Employee` Object类型的复数显示名称可能是`Employees`。
* **描述：** 关于Object类型的解释性文本，任何人都可以在用户应用程序中阅读。例如，`Employee` Object类型的描述可能是`Organization X的所有全职和兼职员工`。
* **组：** 组是帮助您对Object类型进行分类的标签。例如，`Employee` Object类型可能属于组`HR`和`Employee 360`。
* **API名称：** 在代码中以编程方式引用Object类型时使用的名称。例如，`Employee` Object类型的API名称可能是`Employee`。阅读更多关于[API名称](/zh/foundry/functions/api-objects-links/)。
* **可见性：** 向用户应用程序指示如何重要地显示Object类型。一个`重要`的Object类型将使应用程序首先向用户显示此Object类型。一个`隐藏`的Object类型将不会出现在用户应用程序中。默认情况下，`Employee` Object类型的可见性为`normal`。
* **状态：** 向用户和其他Ontology构建者发出Object类型在开发过程中的位置的信号。它可以是`active`，`experimental`或`deprecated`。默认情况下，`Employee` Object类型的状态为`experimental`。阅读更多关于[状态](/zh/foundry/object-link-types/metadata-statuses/)。
* **索引状态：** Object类型及其支持数据源的最后一次重新索引状态。它可以是`success`，`失败`或`not started`。阅读更多关于[索引状态](/zh/foundry/object-databases/object-storage-v1/)。
* **数据输出：** 指示Object类型是否生成了数据输出数据集，以及是否允许最终用户对这种类型的对象进行编辑是`enabled`还是`disabled`。阅读更多关于[数据输出数据集](/zh/foundry/object-link-types/allow-editing/)。

[了解更多关于在Ontology中创建和配置Object类型以及Object类型元数据的验证要求。](/zh/foundry/object-link-types/create-object-type/)

[了解更多关于属性（Object类型的特征）。](/zh/foundry/object-link-types/properties-overview/)

---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/object-link-types/use-value-type/",
  "title": "使用值类型",
  "page_id": "use-value-type",
  "category_id": "ontology",
  "section_id": "object-link-types",
  "previous": "/zh/foundry/object-link-types/create-value-type/",
  "next": "/zh/foundry/object-link-types/value-types-versions/",
  "scraped_at": "2026-07-14T04:26:03.636465+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 使用值类型

一旦[创建了一个值类型](/zh/foundry/object-link-types/create-value-type/)，您可以在Foundry中将其用作数据类型。值类型可以支持以下应用案例。

* 将值类型指派给Object类型属性。
* 将值类型指派给共享属性。
* 将值类型指派给Pipeline Builder管道属性，作为逻辑类型，使用`logical type cast`表达式，并在写入对象目标时在属性上选择值类型。

要将值类型指派给属性，在属性配置期间从下拉菜单中选择值类型。

<img src="../../foundry-docs/object-link-types/media/value-type-use.png" alt="约束更新警告" width="500" />

:::callout{theme="warning"}
如果您将值类型应用于包含出错验证的属性值的Object属性，该Object类型将无法索引。您可以在Ontology Manager中的Object类型健康状态中查看此类索引失败，您可以在其中更正数据或更新值类型以解决问题。
:::

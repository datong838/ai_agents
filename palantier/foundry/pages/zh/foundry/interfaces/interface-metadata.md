---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/interfaces/interface-metadata/",
  "title": "元数据参考",
  "page_id": "interface-metadata",
  "category_id": "ontology",
  "section_id": "interfaces",
  "previous": "/zh/foundry/interfaces/extend-interface/",
  "next": "/zh/foundry/logic/overview/",
  "scraped_at": "2026-07-14T04:31:15.740020+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 元数据参考

一个接口在Ontology中通过以下元数据表示：

* **RID:** 每个Palantir资源自动生成的唯一标识符。接口的RID将在平台上的出错信息中被引用。
* **图标:** 用作视觉标识的图片和颜色，当用户查看此接口时将在应用程序中出现。接口的图标周围有虚线，以在视觉上将其与对象类型图标区分开。例如，周围有虚线的建筑图标可能被用于描绘`Facility`接口。
* **显示名称:** 在用户应用程序中访问此接口时显示给任何人的名称。例如，`Facility`接口的显示名称可能是"Facility"。
* **描述:** 用户应用程序中任何人都可以阅读的关于接口的说明文本。例如，`Facility`接口的描述可能是"一个用于表示航空设施的抽象对象类型接口"。
* **API名称:** 在代码中以编程方式引用接口时使用的名称。例如，`Facility`接口的API名称可能是`facility`。
* **状态:** 向用户和Ontology搭建者传达接口在开发过程中的位置的信号。可以是`active`、`experimental`或`deprecated`。默认情况下，`Facility`接口将具有`experimental`状态。了解更多关于[状态](/zh/foundry/object-link-types/metadata-statuses/)。

---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/preparation/faq/",
  "title": "数据准备常见问题解答",
  "page_id": "faq",
  "category_id": "data-integration",
  "section_id": "preparation",
  "previous": "/zh/foundry/preparation/advanced-examples/",
  "next": "/zh/foundry/recipes/overview/",
  "scraped_at": "2026-07-13T06:06:17.297768+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

## 数据准备常见问题解答

以下是有关Preparation的一些常见问题。

有关一般信息，请查看我们的[数据Preparation文档](/zh/foundry/preparation/overview/)。

* [数据准备问题](#data-preparation-questions)
* [什么是Preparation？](#what-is-preparation)
* [谁应该使用Preparation？](#who-is-preparation-meant-for)
* [我可以用Preparation做什么？](#what-can-i-do-with-preparation)
* [我可以更改Preparation中的输入数据集吗？](#can-i-change-input-dataset-in-preparation)

***

## 什么是Preparation？

Preparation是一个用于清理和准备数据的应用程序，由Contour后端提供支持。

[返回顶部](#data-preparation-faq)

***

## 谁应该使用Preparation？

我们旨在使其可以被所有注册用户直接使用，或仅需最少的培训。在初次加载时，用户可以立即了解其数据的形状（行和列信息）及其整洁程度。例如，质量标志如多余的空白或高空值百分比将逐步指导用户修复或忽略这些标志。

也就是说，像仅消费记事本文档的人，可能不需要使用Preparation。然而，某些代码库流程可能会通过Preparation简化。

[返回顶部](#data-preparation-faq)

***

## 我可以用Preparation做什么？

以下是一些Preparation可以轻松清理或准备真实数据的示例：

* 将邮政编码标准化为五位数字。
* 识别并将纬度/经度的0值设为空。
* 通过将ID列附加到URL来创建超链接。
* 通过删除前导和尾随空白来标准化值。
* 将货币列（例如：“USD 1000”）拆分为单独的货币代码和金额列。

[返回顶部](#data-preparation-faq)

***

## 我可以更改Preparation中的输入数据集吗？

可以。在右侧的**更改日志**面板中，向下滚动到最底部并编辑起始数据集。如果您想将相同的逻辑应用于不同的数据集但保留原始数据集，您可以在此之前通过选择其名称旁边的小下拉菜单来复制您的准备。

[返回顶部](#data-preparation-faq)

---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/object-link-types/value-types-overview/",
  "title": "概述",
  "page_id": "value-types-overview",
  "category_id": "ontology",
  "section_id": "object-link-types",
  "previous": "/zh/foundry/object-link-types/allow-editing/",
  "next": "/zh/foundry/object-link-types/create-value-type/",
  "scraped_at": "2026-07-14T04:25:47.854151+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

:::callout{theme="warning" title="Beta"}
Value types处于测试阶段，必须先在[**应用访问**页面的控制面板](/zh/foundry/administration/configure-application-access/)中启用后才能使用。
:::

**Value types** 是围绕[field type](/zh/foundry/data-integration/datasets/#supported-field-types)的语义包装器，包含元数据和约束，可以增强类型安全性，提高表达能力，并提供附加的上下文。Value types 封装了特定领域的数据类型，并以一种可在平台上重复使用的方式强制执行数据验证。与定义和搭建Ontology的Object类型、属性、link types或其他类型不同，value types与平台中的[空间](/zh/foundry/security/orgs-and-spaces/#spaces)相关联。一个空间可以容纳一个Ontology。

数据集[field types](/zh/foundry/object-link-types/type-reference/#field-types)和属性[base types](/zh/foundry/object-link-types/type-reference/#base-types)反映了编程语言中的原始类型。这些类型是领域无关的，并不提供领域上下文。相比之下，value types捕获数据的上下文和语义意义，并集中数据验证。用户直接从value type定义和获取意义，而不是依赖于诸如列名或属性描述等周边信息。Value types还在Builder管道和Ontology上强制其验证约束，因此数据集成商和Ontology管理者可以确保数据流和模型中正确的语义类型。

例如，用户可以定义一个“email”值类型，其中包含正则表达式约束，以确保任何使用该值类型的属性表示有效的电子邮件地址。然后，这个值类型可以在多个Object类型和管道中重复使用，而无需为每个此类属性重复验证逻辑。此外，使用此值类型的每个属性都被明确理解为包含电子邮件地址。

由于value types旨在跨多个管道和Object类型重复使用，它们被[授权](/zh/foundry/object-link-types/value-types-permissions/)以确保用户可以在需要的地方应用它们，并且被[版本化](/zh/foundry/object-link-types/value-types-versions/)以处理破坏性和非破坏性编辑。

通过学习如何[创建新的value type](/zh/foundry/object-link-types/create-value-type/)或在属性上[使用现有的value type](/zh/foundry/object-link-types/use-value-type/)来开始。

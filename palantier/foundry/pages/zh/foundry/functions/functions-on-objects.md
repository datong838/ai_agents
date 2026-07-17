---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/functions/functions-on-objects/",
  "title": "概述",
  "page_id": "functions-on-objects",
  "category_id": "ontology",
  "section_id": "functions",
  "previous": "/zh/foundry/functions/external-sources/",
  "next": "/zh/foundry/functions/foo-getting-started/",
  "scraped_at": "2026-07-14T04:29:51.555328+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

Foundry中的函数原生支持从Ontology中的Objects和链接访问和修改数据。在Ontology中定义了Object和链接类型后，可以将这些类型导入到函数库中，以自动生成代码绑定。这些代码绑定包括对以下内容的支持：

* 将Object和对象集类型作为[参数](/zh/foundry/functions/input-output-types/#ontology-types-objects-and-object-sets)传递给函数
* 使用[对象集API](/zh/foundry/functions/api-object-sets/)按需搜索对象集
* 使用[OntologyEditFunctions](/zh/foundry/functions/edits-overview/)修改对象

由于对Ontology的这种原生支持，Foundry中的函数远远超越了常用的函数即服务（FaaS）平台，提供了对数据存储、检索和修改的原生支持——所有这些都受Foundry的数据安全、沿袭和透明性保证的约束。

[了解如何从Objects开始使用函数。](/zh/foundry/functions/foo-getting-started/)

:::callout{theme="neutral"}
术语“Functions on Objects”（有时简称为“FoO”或“FOO”）被宽泛地用于指代读取Object数据的函数，无论是作为参数还是使用Object搜索，但在Foundry中并没有“Functions on Objects”在本质上与其他函数有所区别的正式概念。
:::

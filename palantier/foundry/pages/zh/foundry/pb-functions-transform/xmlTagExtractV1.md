---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/xmlTagExtractV1/",
  "title": "从XML文件中提取行",
  "page_id": "xmlTagExtractV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/parseTextFileV1/",
  "next": "/zh/foundry/pb-functions-transform/parseExcelV1/",
  "scraped_at": "2026-07-13T05:58:24.484811+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 从XML文件中提取行

> 支持于: 批处理

读取一个文件数据集，并将每个XML文件解析为行。

**变换类别**: 文件

## 声明的参数

* **数据集** - 要处理的文件数据集。<br>*文件*
* **模式** - 解析xml文件时使用的模式定义。<br>*类型\<Struct>*
* **XML标签** - 用作每个标签生成一行的基础的XML标签。<br>*字面值<字符串>*
* *非必填* **属性前缀** - 标签属性的前缀。<br>*字面值<字符串>*
* *非必填* **编码** - 输入文件的编码类型（字符集）。<br>*枚举\<ISO\_8859\_1, UTF\_8>*
* *非必填* **值标签** - 当元素中有属性而没有子元素时用于值的标签。<br>*字面值<字符串>*

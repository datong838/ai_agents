---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/extractEmailDataAsRowsV1/",
  "title": "从电子邮件文件的数据集中提取行",
  "page_id": "extractEmailDataAsRowsV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/parseJsonV1/",
  "next": "/zh/foundry/pb-functions-transform/parseTextFileV1/",
  "scraped_at": "2026-07-13T05:58:21.959006+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 从电子邮件文件的数据集中提取行

> 支持于: 批处理

读取电子邮件文件的数据集，并将每个文件解析为一行。支持的文件扩展名：.eml、.emltpl 和 .msg。

**变换类别**: 文件, 媒体

## 声明的参数

* **数据集** - 要处理的电子邮件文件数据集。<br>*文件*
* **要提取的电子邮件信息** - 要包含的元数据列。<br>*集合<枚举<附件, 密件抄送, 正文 (HTML), 正文 (纯文本), 抄送, 文件名, 发件人, 头信息, ID, 发送时间戳, 以及更多 ...>>*

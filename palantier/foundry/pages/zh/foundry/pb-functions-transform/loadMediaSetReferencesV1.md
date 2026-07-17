---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/loadMediaSetReferencesV1/",
  "title": "将媒体集转换为表格行",
  "page_id": "loadMediaSetReferencesV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/computeExpressionIfAbsentV1/",
  "next": "/zh/foundry/pb-functions-transform/complexCrossJoinV1/",
  "scraped_at": "2026-07-13T05:58:11.773164+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 将媒体集转换为表格行

> 支持于：批处理

生成一个包含媒体引用和媒体项基本元数据的数据集。首先使用此变换来应用其他媒体变换。

**变换类别**：文件，媒体

## 声明的参数

* **按路径去重** - 按路径去重媒体项。仅支持于快照模式。<br>*Literal\<Boolean>*
* **包括时间戳** - 包括添加媒体项时的时间戳。<br>*Literal\<Boolean>*
* **媒体集** - 加载媒体引用的媒体集。<br>*Media*

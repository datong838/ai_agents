---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/sortV2/",
  "title": "排序",
  "page_id": "sortV2",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/complexSemiJoinV1/",
  "next": "/zh/foundry/pb-functions-transform/filesTextBlockV1/",
  "scraped_at": "2026-07-13T05:59:03.609707+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 排序

> 支持于：批处理

通过选择列或对列应用函数来变换输入数据集。

**变换类别**：其他

## 声明的参数

* **数据集** - 要排序的数据集。<br>*表格*
* **排序规范** - 数据集的排序规范。<br>*列表<元组<列<可比较类型>, 枚举<升序, 降序>>>*

## 示例

### 示例 1：基本情况

**参数值：**

* **数据集**: ri.foundry.main.dataset.a
* **排序规范**: \[(`b`, `DESCENDING`)]

**输入：**

| a | b |
| ----- | ----- |
| 1 | 2 |
| 3 | 4 |
| 5 | 6 |

**输出：**

| a | b |
| ----- | ----- |
| 5 | 6 |
| 3 | 4 |
| 1 | 2 |

***

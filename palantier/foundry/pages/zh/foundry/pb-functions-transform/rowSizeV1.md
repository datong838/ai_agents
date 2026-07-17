---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/rowSizeV1/",
  "title": "行大小",
  "page_id": "rowSizeV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/rollUpV1/",
  "next": "/zh/foundry/pb-functions-transform/selectV1/",
  "scraped_at": "2026-07-13T05:58:55.534788+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 行大小

> 支持于: 批处理

估算JVM中单行的大小。

**变换类别**: 其他

## 声明的参数

* **数据集** - 用于计算单行大小的数据集。<br>*表*
* *非必填* **行大小列别名** - 行估算大小值（以字节为单位）的列名，默认为 'size'。<br>*字面值<字符串>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **数据集**: ri.foundry.main.dataset.a
* **行大小列别名**: size

**输入:**

| a |
| ----- |
| 1 |

**输出:**

| a | size |
| ----- | ----- |
| 1 | 16 |

***

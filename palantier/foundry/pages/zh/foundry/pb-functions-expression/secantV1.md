---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/secantV1/",
  "title": "正割",
  "page_id": "secantV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/sampleVarianceV1/",
  "next": "/zh/foundry/pb-functions-expression/sentenceCaseV1/",
  "scraped_at": "2026-07-13T05:57:13.461222+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 正割

> 支持于: 批处理, 流处理

计算一个角度的正割。

**表达式类别**: 数值

## 声明的参数

* **角度单位** - 角度单位，可以是度或弧度。<br>*枚举<度, 弧度>*
* **角度值** - 角度值，以弧度或度为单位。<br>*表达式<确定数值>*

**输出类型:** *双精度*

## 示例

### 示例 1: 基本案例

**参数值:**

* **角度单位**: `degrees`
* **角度值**: `angle`

| angle | **输出** |
| ----- | ----- |
| 0.0 | 1.0 |
| 90.0 | 1.633123935319537E16 |
| 180.0 | -1.0 |

***

### 示例 2: 空值案例

**参数值:**

* **角度单位**: `radians`
* **角度值**: *null*

**输出:** *null*

***

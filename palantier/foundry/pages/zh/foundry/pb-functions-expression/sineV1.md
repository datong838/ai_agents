---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/sineV1/",
  "title": "正弦",
  "page_id": "sineV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/simplifyGeometryV1/",
  "next": "/zh/foundry/pb-functions-expression/skipBytesV1/",
  "scraped_at": "2026-07-13T05:57:22.801692+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 正弦

> 支持于: 批处理, 流处理

计算角度的正弦值。

**表达式类别**: 数值

## 声明的参数

* **角度单位** - 角度单位可以是度或弧度。<br>*枚举<度, 弧度>*
* **角度值** - 角度值可以是弧度或度。<br>*表达式<确定数值>*

**输出类型:** *双精度*

## 示例

### 示例 1: 基本情况

**参数值:**

* **角度单位**: `degrees`
* **角度值**: `angle`

| angle | **输出** |
| ----- | ----- |
| 0.0 | 0.0 |
| 90.0 | 1.0 |
| 180.0 | 0.0 |

***

### 示例 2: 基本情况

**参数值:**

* **角度单位**: `radians`
* **角度值**: *null*

**输出:** *null*

***

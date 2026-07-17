---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/arctan2V1/",
  "title": "Arctan2",
  "page_id": "arctan2V1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/arctanV1/",
  "next": "/zh/foundry/pb-functions-expression/areaV1/",
  "scraped_at": "2026-07-13T05:52:23.537129+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Arctan2

> 支持于: 批处理, 流处理

返回从原点到点 (x, y) 的射线与正 x 轴之间的角度 θ，范围限定为 −π<θ<=π。

**表达式类别**: 数值

## 声明的参数

* **角度单位** - 输出角度单位，可以是度或弧度。<br>*枚举\<Degrees, Radians>*
* **X** - X 坐标值。<br>*表达式\<Double | Float>*
* **Y** - Y 坐标值。<br>*表达式\<Double | Float>*

**输出类型:** *Double*

## 示例

### 示例 1: 基本案例

**参数值:**

* **角度单位**: `degrees`
* **X**: `x`
* **Y**: `y`

| y | x | **输出** |
| ----- | ----- | ----- |
| 0.0 | 0.0 | 0.0 |
| 1.0 | 0.0 | 90.0 |
| 0.0 | -1.0 | 180.0 |
| -1.0 | 0.0 | -90.0 |

***

### 示例 2: 空值案例

**参数值:**

* **角度单位**: `radians`
* **X**: *null*
* **Y**: 0.0

**输出:** *null*

***

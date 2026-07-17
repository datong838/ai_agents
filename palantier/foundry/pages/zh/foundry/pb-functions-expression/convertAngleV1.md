---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/convertAngleV1/",
  "title": "转换角度单位",
  "page_id": "convertAngleV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/convertBaseV1/",
  "next": "/zh/foundry/pb-functions-expression/convertDistanceV1/",
  "scraped_at": "2026-07-13T05:53:45.682373+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 转换角度单位

> 支持于: 批处理, 流式处理

**表达式类别**: 地理空间, 数值

## 声明的参数

* **当前单位的数量** - *无描述*<br>*Expression\<DefiniteNumeric>*
* **当前单位** - 转换前的单位。<br>*Enum\<Degrees, Minutes, Radians, Seconds>*
* **目标单位** - 转换后的期望单位。<br>*Enum\<Degrees, Minutes, Radians, Seconds>*

**输出类型:** *Double*

## 示例

### 示例 1: 基本情况

**参数值:**

* **当前单位的数量**: `degrees`
* **当前单位**: `degrees`
* **目标单位**: `radians`

| degrees | **输出** |
| ----- | ----- |
| 180 | 3.141592653589793 |

***

### 示例 2: 基本情况

**参数值:**

* **当前单位的数量**: `radians`
* **当前单位**: `radians`
* **目标单位**: `degrees`

| radians | **输出** |
| ----- | ----- |
| 3.141592653589793 | 180.0 |

***

### 示例 3: 空值情况

**参数值:**

* **当前单位的数量**: `radians`
* **当前单位**: `radians`
* **目标单位**: `degrees`

| radians | **输出** |
| ----- | ----- |
| *null* | *null* |

***

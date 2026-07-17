---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/convertDistanceV1/",
  "title": "在距离单位之间转换",
  "page_id": "convertDistanceV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/convertAngleV1/",
  "next": "/zh/foundry/pb-functions-expression/convertTimeV1/",
  "scraped_at": "2026-07-13T05:53:38.951483+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 在距离单位之间转换

> 支持于: 批处理, 流处理

**表达式类别**: 数值

## 声明的参数

* **当前单位的数量** - *无描述*<br>*表达式\<DefiniteNumeric>*
* **当前单位** - 转换前的单位。<br>*枚举<厘米, 数据英里, 十米, 分米, 英尺, 百米, 英寸, 公里, 米, 英里, 等...>*
* **目标单位** - 转换后的期望单位。<br>*枚举<厘米, 数据英里, 十米, 分米, 英尺, 百米, 英寸, 公里, 米, 英里, 等...>*

**输出类型:** *双精度*

## 示例

### 示例 1: 基本情况

**参数值:**

* **当前单位的数量**: `kilometers`
* **当前单位**: `kilometer`
* **目标单位**: `meter`

| kilometers | **输出** |
| ----- | ----- |
| 1 | 1000.0 |

***

### 示例 2: 空值情况

**参数值:**

* **当前单位的数量**: `kilometers`
* **当前单位**: `kilometer`
* **目标单位**: `meter`

| kilometers | **输出** |
| ----- | ----- |
| *null* | *null* |

***

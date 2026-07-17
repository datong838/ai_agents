---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/convertTimeV1/",
  "title": "时间单位转换",
  "page_id": "convertTimeV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/convertDistanceV1/",
  "next": "/zh/foundry/pb-functions-expression/convertWeightV1/",
  "scraped_at": "2026-07-13T05:53:42.787761+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 时间单位转换

> 支持于: 批处理, 流处理

**表达式类别**: 日期时间

## 声明的参数

* **当前单位的数量** - *无描述*<br>*表达式\<DefiniteNumeric>*
* **当前单位** - 转换前的单位。<br>*枚举<天, 小时, 毫秒, 分钟, 秒, 周>*
* **目标单位** - 转换后的期望单位。<br>*枚举<天, 小时, 毫秒, 分钟, 秒, 周>*

**输出类型:** *双精度*

## 示例

### 示例 1: 基本案例

**参数值:**

* **当前单位的数量**: `days`
* **当前单位**: `days`
* **目标单位**: `minutes`

| 天 | **输出** |
| ----- | ----- |
| 12 | 17280.0 |

***

### 示例 2: 空值案例

**参数值:**

* **当前单位的数量**: `days`
* **当前单位**: `days`
* **目标单位**: `minutes`

| 天 | **输出** |
| ----- | ----- |
| *null* | *null* |

***

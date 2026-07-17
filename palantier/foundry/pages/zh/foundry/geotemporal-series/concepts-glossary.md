---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/geotemporal-series/concepts-glossary/",
  "title": "概念词汇表",
  "page_id": "concepts-glossary",
  "category_id": "data-integration",
  "section_id": "geotemporal-series",
  "previous": "/zh/foundry/geotemporal-series/overview/",
  "next": "/zh/foundry/geotemporal-series/data-modeling/",
  "scraped_at": "2026-07-13T06:22:07.443756+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概念词汇表

本页定义了在 Foundry 中使用地理时间序列的关键术语和概念。我们建议查看这些概念，以便更好地理解如何在您的组织中使用地理时间序列。

## 地理时间序列

表示实体随时间变化的位置的位置信息和时间戳数据序列。每个序列被称为**地理时间序列**，并由[序列ID](#series-id)标识。序列中的单个点被称为[观测](#observation)。例如，从旧金山到纽约市的航班可以表示为地理时间序列，其中飞机在飞行过程中报告的每个位置都是一次观测。

地理时间数据也被称为时空数据、“地理时间”或“轨迹”数据。

## 序列ID

将多个地理时间观测分组为单个序列的标识符。序列ID在给定的地理时间序列集成中必须是唯一的。例如，航班号、起点、终点和日期的连接可以用于唯一标识单个航班。

## 地理时间序列对象类型

一种对象类型，包含一个或多个[地理时间序列引用](#geotemporal-series-reference-gtsr)属性，并且非必填地包含有关被引用地理时间序列的其他属性。例如，表示航班的对象类型可以包括起始和目的机场作为字符串属性，以及航线作为地理时间序列引用。

## 地理时间序列引用 (GTSR)

一种属性类型，用于从地理时间序列集成中引用特定的地理时间序列。Foundry 应用程序使用此引用来获取序列的支持地理时间数据。

## 地理时间序列同步

将地理时间序列数据索引到 Foundry 的地理时间序列数据库中。索引后，地理时间数据可以从对象上的 GTSR 访问。一个序列ID的所有值应包含在同一个同步中。可以使用[Pipeline Builder](/zh/foundry/pipeline-builder/outputs-overview/)中的地理时间序列同步输出来创建同步。

## 观测

地理时间序列中的单个点，由序列ID、时间戳、位置和其他集成定义的属性组成。例如，来自飞机的单个 GPS 信号将是地理时间序列中的一次观测。这些也可以称为“ticks”。

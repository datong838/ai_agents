---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/pyspark-aggregation/",
  "title": "聚合和数据透视表",
  "page_id": "pyspark-aggregation",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/pyspark-joins/",
  "next": "/zh/foundry/transforms-python/pyspark-window/",
  "scraped_at": "2026-07-13T06:08:21.182384+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 聚合和数据透视表

## 聚合语法

**在PySpark中有多种方式可以进行聚合。我们推荐这种语法作为最可靠的方式。**

```python
aggregated_df = df.groupBy('state').agg(
    F.max('city_population').alias('largest_city_in_state')
)
```

```plaintext
# 这段代码对数据框 `df` 进行分组操作，根据 `state` 列对数据进行分组。
# 使用 `F.max('city_population')` 来计算每个州中人口最多的城市。
# 使用 `.alias('largest_city_in_state')` 将结果列命名为 `largest_city_in_state`。
```

### 示例

在`DataFrame`上使用`.groupBy()`方法时，可以指定任意数量的列来执行聚合操作。或者，如果希望在整个`DataFrame`上进行聚合，则不包括任何列。

```python
# 按照 'state' 和 'county' 分组，计算每个州和县中人口最多的城市
aggregated_df = df.groupBy('state', 'county').agg(
    F.max('city_population').alias('largest_city_in_state_county') # 使用 max 函数获取最大城市人口
)

# 计算所有数据中人口最多的城市
aggregated_df = df.groupBy().agg(
    F.max('city_population').alias('largest_city_overall') # 使用 max 函数获取最大城市人口
)
```

分组的 `DataFrame` 上的 `.agg()` 方法接受任意数量的聚合函数。

```python
aggregated_df = df.groupBy('state').agg(
    # 获取每个州人口最多的城市人口数，并将其命名为 'largest_city_in_state'
    F.max('city_population').alias('largest_city_in_state'),
    # 计算每个州的城市人口平均数，并将其命名为 'average_population_in_state'
    F.avg('city_population').alias('average_population_in_state')
)
```

> 默认情况下，聚合会生成形式为 `aggregation_name(target_column)` 的列。然而，Foundry 中的列名不能包含括号或其他非字母数字字符。因此，为每个聚合指定一个别名。

## 透视表

PySpark 中的透视表的工作方式与普通分组聚合非常相似。

```python
pivoted_df = df.groupBy('equipment').pivot('sensor').mean('value')
# 这段代码对DataFrame `df`进行操作，首先按照'equipment'列进行分组，
# 然后对'sensor'列进行透视操作，最后计算每组中'value'列的平均值。
```

| 设备      | 传感器      | 值    |
| --------- | ----------- | ----- |
| A         | 温度        | 60    |
| A         | 温度        | 40    |
| B         | 速度        | 6     |
| A         | 速度        | 3     |

| 设备      | 温度        | 速度  |
| --------- | ----------- | ----- |
| A         | 50          | 3     |
| B         | null        | 7     |

## 聚合函数

[了解更多关于 PySpark 聚合函数的信息。↗](https://sparkbyexamples.com/pyspark/pyspark-aggregate-functions/)

#### `avg(column)` / `mean(column)`

#### `collect_list(column)`

* 将所有值合并到一个数组中

#### `collect_set(column)`

* 将所有值合并到一个数组中，并去除重复项

#### `count(column)`

#### `corr(x, y)`

* 列 `x` 和 `y` 的 Pearson 相关系数。

#### `covar_pop(col1, col2)`

#### `covar_samp(col1, col2)`

#### `countDistinct(column, *cols)`

#### `first(column, ignorenulls=False)`

* 组内列的第一个值。对于我们期望仅存在一个值但必须选择聚合的透视表非常有用。

#### `grouping(column)`

#### `grouping_id(*cols)`

#### `kurtosis(column)`

#### `last(column, ignorenulls=False)`

#### `max(column)`

#### `min(column)`

#### `skewness(column)`

#### `stddev(column)`

#### `stddev_pop(column)`

* 总体标准差

#### `stddev_samp(column)`

* 无偏样本标准差

#### `sum(column)`

#### `sumDistinct(column)`

#### `var_pop(column)`

* 总体方差

#### `var_samp(column)`

* 无偏样本方差

#### `variance(column)`

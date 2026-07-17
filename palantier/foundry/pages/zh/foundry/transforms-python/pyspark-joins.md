---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/pyspark-joins/",
  "title": "合并",
  "page_id": "pyspark-joins",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/pyspark-math/",
  "next": "/zh/foundry/transforms-python/pyspark-aggregation/",
  "scraped_at": "2026-07-13T06:08:33.006354+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 合并

在 PySpark 中，`DataFrame` 可以合并到另一个 dataframe 或合并到自身，就像 SQL 中的表可以合并一样。Dataframe 使用 `.join()` 方法合并到其他 dataframe。它需要一个 `DataFrame`，一个合并约束，例如要合并的列名，以及一种方法（`left`、`right`、`inner` 等）

## 简单左合并

```python
df_joined = df_left.join(df_right, 'key', 'left')
# 在这里，我们使用DataFrame的join方法来连接两个DataFrame：df_left和df_right
# 'key'是连接键，即用于匹配的列名
# 'left'表示这是一个左连接（left join），即保留左表df_left中的所有行
```

`df_joined` 现在是 `df_left.key == df_right.key` 上的`left`合并的结果。PySpark 会自动删除其中一个 `key` 列的副本，因此 `df_joined` 仅包含一个名为 `key` 的列。

:::callout{theme="neutral"}
如果 `df_left` 和 `df_right` 中要合并的键(key)不具有相同的名称，建议在执行合并之前先重命名它们。
:::

### 名称冲突

请确保重命名或删除任何未明确用于合并的同名字段，因为一旦合并完成，这些字段将发生冲突。可以通过循环将`DataFrame`中的所有列重命名以添加某个前缀，如下所示，

```python
for column in df.columns:
    # 为每一列添加前缀'some_prefix_'
	df = df.withColumnRenamed(column, 'some_prefix_' + column)
```

## 基于多个字段进行合并

`.join()` 方法可以接受一个字段列表来进行合并，而不是单个字段。

```python
# 通过指定的列 ['column1', 'column2', 'column3'] 将 df_left 和 df_right 数据框进行左连接
df_joined = df_left.join(df_right, ['column1', 'column2', 'column3'], 'left')
```

`df_joined` 现在是 `column1`、`column2` 和 `column3` 的合并。这假设 `df_left` 和 `df_right` 之间的列名是一致的。

## 高级任意合并约束

PySpark 支持使用任意表达式通过逻辑运算符进行合并。假设我们想要在左侧 `DataFrame` 的列 `ID` 上进行合并，左侧 `DataFrame` 中的日期 `start` 早于右侧 `DataFrame` 中的日期 `end`，并且根据某个字段 `X` 的内容，可能需要或不需要右侧 `DataFrame` 中的 `Y` 包含另一个值。

```python
key_constraint = df_left.ID == df_right.ID  # ID键约束：左表和右表的ID字段相等
date_constraint = df_left.start < df_right.end  # 日期约束：左表的start字段小于右表的end字段
case_constraint = F.when(df_left.X == 'some_value', df_right.Y == 'some_other_value')\
	.otherwise(True)  # 条件约束：当左表的X字段为'some_value'时，右表的Y字段必须为'some_other_value'，否则为True
combined_constraints = key_constraint & date_constraint & case_constraint  # 合并所有约束条件
df_joined = df_left.join(df_right, combined_constraints, 'left')  # 使用左连接（left join）合并左表和右表
```

## 笛卡尔积（Cross join）

使用笛卡尔积合并生成两个数据框之间所有行的组合，也称为笛卡尔积，不需要通过键或其他约束进行匹配。应尽量避免使用笛卡尔积，因为它可能引入内存和性能问题。

:::callout{theme="warning" title="警告"}
如果您打算立即筛选结果，请不要使用笛卡尔积。相反，将您的筛选条件嵌入到合并约束中，以获得更高效的解决方案（请参阅上面的[高级任意合并约束](#advanced-arbitrary-join-constraints)）。
:::

您必须在代码库中显式[导入配置文件](/zh/foundry/code-repositories/spark-profiles/) `CROSS_JOIN_ENABLED` 以使用笛卡尔积。

```python
from transforms.api import configure

# 使用 configure 装饰器来设置配置文件，其中启用了 CROSS_JOIN
@configure(profile=["CROSS_JOIN_ENABLED"])
@transform_df(
	...
)
def my_compute_function(input_a, input_b):
    # 执行两个DataFrame的交叉连接操作
    return input_a.crossJoin(input_b)

```

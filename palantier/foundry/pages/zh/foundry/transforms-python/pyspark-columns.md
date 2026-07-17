---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/pyspark-columns/",
  "title": "概念: 列",
  "page_id": "pyspark-columns",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/pyspark-style-guide/",
  "next": "/zh/foundry/transforms-python/pyspark-queries/",
  "scraped_at": "2026-07-13T06:08:21.225546+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概念: 列

要遵循本文档中的示例，请添加：`from pyspark.sql import functions as F`。

列由 PySpark 类管理：`pyspark.sql.Column`。每当您直接引用或从现有列派生表达式时，都会创建列实例。您可以通过以下任意方式引用列：

* `F.col("column_name") `
* `F.column("column_name")`

:::callout{theme="neutral"}
引用列不等同于执行`选择`，因为“选择”列是指子集化（和重新排序）您希望出现在结果数据集中的列。
:::

## 目录

* [获取模式](#getting-the-schema)
* [选择](#select)：选择要保留的列
* [创建，更新](#create-update)
* [重命名，别名](#rename-alias)
* [删除](#drop)：移除列
* [转换](#cast)
* [当...否则](#when-otherwise)

## 获取模式

### `DataFrame.columns`

返回所有列名作为一个 Python 列表。

```python
columns = df.columns # ['age', 'name']
# 这行代码用于获取DataFrame对象df的所有列名。
```

## `DataFrame.dtypes`

返回所有列名及其数据类型作为元组列表

```python
dtypes = df.dtypes # 获取数据框每列的数据类型，例如： [('age', 'int'), ('name', 'string')]
```

## 选择

### `DataFrame.select(*cols)`

返回一个新的`DataFrame`，其中包含源`DataFrame`的一部分列。

例如，我们有一个包含6个命名列的DataFrame：`id`，`first_name`，`last_name`，`phone_number`，`address`，`is_active_member`

| id   | first\_name | last\_name | phone\_number   | zip\_code | is\_active\_member |
| ---- | ---------- | --------- | -------------- | -------- | ---------------- |
| 1    | John       | Doe       | (123) 456-7890 | 10014    | `true`           |
| 2    | Jane       | Eyre      | (213) 555-1234 | 90007    | `true`           |
| ...  | ...        | ...       | ...            | ...      | ...              |

您可能希望将DataFrame变换为仅包含您关心的命名列（可用的一部分）。假设您只想要一个仅包含单列`phone_number`的表：

```python
df = df.select("phone_number")  # 选择数据框中的“phone_number”列
```

或者您可能只需要 `id`、`first_name` 和 `last_name`（至少有3种不同的方法可以完成相同的任务）：

1. 直接传入列名:
   ```python
   df = df.select("id", "first_name", "last_name")
   ```
   或传入列实例:
   ```python
   df = df.select(F.col("id"), F.col("first_name"), F.col("last_name"))
   ```
2. 传入列名数组:
   ```python
   select_columns = ["id", "first_name", "last_name"]
   df = df.select(select_columns)
   ```
3. 传入“解包”的数组:

   ```python
   select_columns = ["id", "first_name", "last_name"]
   df = df.select(*select_columns)
   # 等同于: df = df.select("id", "first_name", "last_name")
   ```

   | id   | first\_name | last\_name |
   | ---- | ---------- | --------- |
   | 1    | John       | Doe       |
   | 2    | Jane       | Eyre      |
   | ...  | ...        | ...       |

   `select_columns` 前的 `*` *解包*了数组，使其在功能上与 `#1` 相同（见注释）。这使您可以执行以下操作：

   ```python
   select_columns = ["id", "first_name", "last_name"]
   return df.select(*select_columns, "phone_number")
   # 等同于: df = df.select("id", "first_name", "last_name", "phone_number")
   ```

   | id   | first\_name | last\_name | phone\_number   |
   | ---- | ---------- | --------- | -------------- |
   | 1    | John       | Doe       | (123) 456-7890 |
   | 2    | Jane       | Eyre      | (213) 555-1234 |
   | ...  | ...        | ...       | ...            |

请记住，您的输出数据集将**仅包含您选择的列**，并且**按照选择的顺序排列**，而不是保留原始列的顺序。名称是唯一且区分大小写的，并且必须已经存在于您选择的数据集中的列。

该规则的一个例外是，您可以派生一个新列并立即以它进行选择。您需要为新派生的列提供一个 `alias` 或名称：

```python
derived_column = F.concat_ws(":", F.col("string1"), F.col("string2"))
# 使用concat_ws函数将"string1"和"string2"两列的值用":"连接起来，并生成一个新的列derived_column
return df.select("string3", derived_column.alias("derived"))
# 从数据框中选择"string3"列和新的derived_column列，并将derived_column重命名为"derived"
```

| string3 | derived      |
| ------- | ------------ |
| 第三    | first:second |
| 三      | one:two      |

## 创建，更新

### `DataFrame.withColumn(name, column)`

```python
new_df = old_df.withColumn("column_name", derived_column)
# 使用withColumn方法在old_df数据框中添加或替换名为"column_name"的新列
# derived_column是计算得到的新列的值
```

* `new_df`: 结果数据框，包含`old_df`中的所有列，但添加了`new_column_name`。
* `old_df`: 我们想要应用新列的数据框
* `column_name`: 您要创建（如果在`old_df`中不存在）或更新（如果在`old_df`中已存在）的列的名称。
* `derived_column`: 导出列的表达式，应用于`column_name`（或您为列指定的任何名称）下的每一行。

给定一个现有的DataFrame，您可以使用`withColumn`方法创建新列或更新现有列的新值或修改值。这对于以下目标特别有用：

1. 基于现有值导出新值

   ```python
   df = df.withColumn("times_two", F.col("number") * 2) # times_two = number * 2
   ```

   ```python
   df = df.withColumn("concat", F.concat(F.col("string1"), F.col("string2")))
   ```

2. 将值从一种类型转换为另一种类型

   ```python
   # 将`start_timestamp`转换为DateType并将新值存储在`start_date`中
   df = df.withColumn("start_date", F.col("start_timestamp").cast("date"))
   ```

3. 更新列

   ```python
   # 使用其全小写版本更新列`string`
   df = df.withColumn("string", F.lower(F.col("string")))
   ```

## 重命名, 别名

### `DataFrame.withColumnRenamed(name, rename)`

使用`.withColumnRenamed()`重命名列：

```python
df = df.withColumnRenamed("old_name", "new_name")  # 将DataFrame中列名"old_name"重命名为"new_name"
```

查看重命名列任务的另一种方式，可以让您深入了解PySpark如何优化变换语句，是：

```python
df = df.withColumn("new_name", F.col("old_name")).drop("old_name")
# 将DataFrame中的“old_name”列重命名为“new_name”列，并删除原来的“old_name”列
```

但是在某些情况下，您可以在不使用`withColumn`的情况下派生一个新列，并且仍然需要为其命名。这时，`alias`（或其方法别名，`name`）就派上用场了。以下是一些用法示例：

```python
df = df.select(derived_column.alias("new_name"))  # 使用别名来重命名列为"new_name"
df = df.select(derived_column.name("new_name"))  # 等同于.alias("new_name")
df = df.groupBy("group") \  # 按"group"列进行分组
	.agg(F.sum("number").alias("sum_of_numbers"), F.count("*").alias("count"))  # 聚合操作：计算"number"列的总和并计数
```

我们还可以同时重命名多个列：

```python
renames = {
    "column": "column_renamed",  # 将"column"列重命名为"column_renamed"
    "data": "data_renamed",      # 将"data"列重命名为"data_renamed"
}

for colname, rename in renames.items():
    df = df.withColumnRenamed(colname, rename)  # 遍历字典，将DataFrame中的列名进行重命名
```

## 删除

### `DataFrame.drop(*cols)`

返回一个新的 `DataFrame`，其列为原始 `DataFrame` 的子集，并删除指定的列。（如果模式不包含给定的列名，则此操作失败。）

有两种删除列的方法：直接方式和间接方式。间接方式是使用 `select`，选择您想*保留*的列的子集。直接方式是使用 `drop`，提供您想*丢弃*的列的子集。两者的使用语法相似，只是这里的顺序无关紧要。以下是几个示例：

| id   | first\_name | last\_name | phone\_number   | zip\_code | is\_active\_member |
| ---- | ---------- | --------- | -------------- | -------- | ---------------- |
| 1    | John       | Doe       | (123) 456-7890 | 10014    | `true`           |
| 2    | Jane       | Eyre      | (213) 555-1234 | 90007    | `true`           |
| ...  | ...        | ...       | ...            | ...      | ...              |

假设您只想删除一列，`phone_number`：

```python
df = df.drop("phone_number")  # 删除名为 "phone_number" 的列
```

或者您可能想要删除 `id`、`first_name` 和 `last_name`（至少有三种不同的方法可以完成相同的任务）：

1. 直接传入列名：
   ```python
   df = df.drop("id", "first_name", "last_name")
   ```
   或者
   ```python
   df = df.drop(F.col("id"), F.col("first_name"), F.col("last_name"))
   ```
2. 传入一个数组：
   ```python
   drop_columns = ["id", "first_name", "last_name"]
   df = df.drop(drop_columns)
   ```
3. 传入一个“解包”的数组：

   ```python
   drop_columns = ["id", "first_name", "last_name"]
   df = df.drop(*drop_columns)
   # 同上: df = df.drop("id", "first_name", "last_name")
   ```

   | phone\_number   | zip\_code | is\_active\_member |
   | -------------- | -------- | ---------------- |
   | (123) 456-7890 | 10014    | `true`           |
   | (213) 555-1234 | 90007    | `true`           |
   | ...            | ...      | ...              |

   `drop_columns` 前的 `*` *解包* 数组，使其在功能上表现得与 `#1` 相同（见注释）。这使您可以执行以下操作：

   ```python
   drop_columns = ["id", "first_name", "last_name"]
   df = df.drop(*drop_columns, "phone_number")
   # 同上: df = df.drop("id", "first_name", "last_name", "phone_number")
   ```

   | zip\_code | is\_active\_member |
   | -------- | ---------------- |
   | 10014    | `true`           |
   | 90007    | `true`           |
   | ...      | ...              |

## 转换

### `Column.cast(type)`

以下是所有存在的数据类型：`NullType`、`StringType`、`BinaryType`、`BooleanType`、`DateType`、`TimestampType`、`DecimalType`、`DoubleType`、`FloatType`、`ByteType`、`IntegerType`、`LongType`、`ShortType`、`ArrayType`、`MapType`、`StructType`、`StructField`

通常，您可以使用列上的 `cast` 方法将大多数数据类型从一种转换为另一种：

```python
from pyspark.sql.types import StringType
df.select(df.age.cast(StringType()).alias("age"))
# 假设 df.age 是 IntegerType 类型
# 将 df.age 列从整型转换为字符串类型，并重命名为 "age"
```

或

```python
df.select(df.age.cast("string").alias("age"))
# 将 age 列的数据类型转换为字符串类型，并将其别名为 "age"
# 效果上与使用 StringType() 相同
```

| 年龄  |
| ---- |
| "2"  |
| "5"  |

强制转换本质上是创建一个新的派生列，您可以直接在其上执行 `select`、`withColumn`、`筛选`等操作。"向下转换" 和 "向上转换" 的概念也适用于PySpark，因此您可能会失去以前数据类型中存储的更细粒度的信息，或获得垃圾信息。

## 当...否则

`F.when(condition, value).otherwise(value2)`

参数：

* **condition** - 布尔列表达式
* **value** - 字面值或列表达式

评估为与 `value` 或 `value2` 参数相同的列表达式。如果未调用 `Column.otherwise()`，则为不匹配的条件返回 `None` (null) 的列表达式。

`when`、`otherwise` 操作符提供了类似于 `if-else` 语句的功能，用于计算新的列值。基本用法是：

```python
# CASE WHEN (age >= 21) THEN true ELSE false END
# 如果年龄大于或等于21，则返回True；否则返回False
at_least_21 = F.when(F.col("age") >= 21, True).otherwise(False)

# CASE WHEN (last_name != "") THEN last_name ELSE null
# 如果last_name不为空，则返回last_name；否则返回None（空值）
last_name = F.when(F.col("last_name") != "", F.col("last_name")).otherwise(None)

# 选择列并为其设置别名
df = df.select(at_least_21.alias("at_least_21"), last_name.alias("last_name"))
```

您可以根据需要多次链接`when`语句：

```python
# 根据年龄对数据进行分类：
# 如果年龄大于等于 35，则分为 "A" 类；
# 如果年龄大于等于 21 且小于 35，则分为 "B" 类；
# 否则分为 "C" 类。
switch = F.when(F.col("age") >= 35, "A").when(F.col("age") >= 21, "B").otherwise("C")
```

这些评估可以指派到列中，或用于筛选：

```python
df = df.withColumn("switch", switch) # 在数据框中添加一个名为 "switch" 的列，值为 A、B 或 C
df = df.where(~F.isnull(last_name)) # 过滤掉 last_name 为 null 的行（空字符串已被视为 null 值）
```

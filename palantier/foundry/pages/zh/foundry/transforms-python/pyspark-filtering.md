---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/pyspark-filtering/",
  "title": "筛选",
  "page_id": "pyspark-filtering",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/pyspark-udfs/",
  "next": "/zh/foundry/transforms-python/pyspark-dates/",
  "scraped_at": "2026-07-13T06:08:16.548474+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 筛选

## 筛选，条件

### `DataFrame.filter(expression)`

返回一个新的`DataFrame`，其中包含由布尔表达式确定的行的子集。`expression`参数是一个布尔列表达式，可以通过多种方式派生。

:::callout{theme="neutral"}
在变换的起始处进行`筛选`，而不是在末尾，以减少不必要的计算工作并提高搭建时间性能。
:::

如果您的数据集中包含大量条目，但您只关心基于某个标准存在的行的子集。

```python
df = df.filter(F.col("age") >= 21) # 限制数据集为仅包含年龄超过21岁的人
```

`where` 是 `筛选` 的别名，并执行完全相同的操作（选择取决于您或您团队的偏好，以确定哪个方法名称更清晰易读）：

```python
df = df.where(F.col("age") >= 21) # 将数据集限制为仅包含年龄大于或等于21岁的人
```

您还可以通过几种不同的方式链接筛选：

```python
df = df.filter(F.col("age") >= 21).filter(F.col("age") < 35)
# 使用链式调用过滤数据，年龄在21岁（含）到35岁（不含）之间

df = df.filter((F.col("age") >= 21) & (F.col("age") < 35))
# 使用括号将条件组合在一起，确保正确的运算顺序，过滤年龄在21岁（含）到35岁（不含）之间的数据
```

### 常量（字面量）

每当您将列与常量或“字面量”进行比较时，例如单个硬编码的字符串、日期或数字，PySpark实际上将此基本Python数据类型评估为“字面量”（与声明`F.lit(value)`相同）。字面量只是一个具有静态值的列表达式。这是一个在我们继续之前需要了解的重要区别，因为这意味着所有与字面量的比较（无论是隐式还是显式）都可以替换为一个命名列。这意味着您可以轻松地进行依赖于同一行中其他列的动态比较。

在某些上下文中，字面量可能无法被正确解释。例如，当与字符串进行比较时，可能会模糊您是打算引用一个以该字符串命名的列还是字符串本身。

```python
df = df.filter("X" == "Y") # X 和 Y 是指列名还是字面量?
dff = df.filter(F.col("X") == F.lit("Y")) # 清楚明了，F.col("X") 指的是列名，而 F.lit("Y") 指的是字面量。
```

## 逻辑操作

PySpark 有许多二元逻辑操作。这些操作总是被评估为布尔列表达式的实例，并且可以用于组合条件。

:::callout{theme="neutral"}
由于我们逻辑操作符的参数是整个列，而不是 Python 基元，我们不能使用熟悉的 `and` 或 `or` Python 操作符。这些操作符期望两个参数都已经评估为单个布尔值。PySpark 能够解释 `&`（按位与）、`|`（按位或）操作符和 `~`（取反）符号来搭建一个在所有行上高效运行的 SQL 查询。
:::

这对我们有帮助的一种方式是，它允许引用二元操作值的命名变量。因此，为了提高可读性和清晰度，特别是当您筛选多个属性时，您可以描述性地命名每个比较:

```python
# 筛选出年龄在 [21, 35) 区间的用户，或者名字是 "John"，或者姓氏为空（null）的记录
at_least_21 = F.col("age") >= 21  # 年龄至少为21
younger_than_35 = F.col("age") < 35  # 年龄小于35
within_age_range = at_least_21 & younger_than_35  # 年龄在21到35岁之间
name_is_john = F.col("first_name") == "John"  # 名字为 "John"
last_name_is_null = F.isnull(F.col("last_name"))  # 姓氏为空（null）
df = df.where(within_age_range | name_is_john | last_name_is_null)  # 筛选符合条件的记录
return df
```

另一种帮助我们的方式是，我们可以利用逻辑运算来提供筛选逻辑：

* `&`: 和

  ```python
  df = df.filter(condition_a & condition_b)
  ```

* `|`: 或

  ```python
  df = df.filter(condition_a | condition_b)
  ```

* `^`: 异或

  ```python
  df = df.filter(condition_a ^ condition_b)
  ```

* `~`: 非

  ```python
  df = df.filter(~condition_a)
  ```

可以随意使用python的for循环来生成条件，但务必复习[布尔代数 ↗](https://en.wikipedia.org/wiki/Boolean_algebra)以避免不必要的出错。以下是如何利用这一点的示例：

```python
def custom_func(col, value):
    # 基本逻辑或用户定义函数（UDF）
    return output # True/False

values = ["a", "b", "c", "d"]
condition = F.lit(False)  # 初始化条件为False
for x in values:
    condition = condition | custom_func(F.col("column"), x)  # 如果自定义函数返回True，则更新条件
df = df.filter(condition)  # 根据条件过滤数据框
return df  # 返回过滤后的数据框
```

## Like, rlike

`like` 和 `rlike` 方法分别允许使用 SQL LIKE 和正则表达式语法进行模式匹配。

> * 对于简单的子字符串搜索，使用 `like`。
> * 对于更复杂的模式匹配，使用 `rlike`。

### `Column.like(sql_like)`

基于 SQL LIKE 匹配返回一个布尔列，该匹配由字面字符串或列提供：

```python
# 过滤DataFrame中的数据，选择'name'列的值以'Al'开头的记录
df = df.filter(F.col('name').like('Al%'))
```

| age  | name    |
| ---- | ------- |
| 2    | "Alice" |

SQL LIKE 通配符：

* `%`：表示≥0个字符
* `_`：表示单个字符

示例（来自[w3schools ↗](https://www.w3schools.com/sql/sql_wildcards.asp)）：

| LIKE 运算符               | 描述                                              |
| ---------------------- | -------------------------------------------------------- |
| `Column.like('a%')`    | 查找任何以"a"开头的值                    |
| `Column.like('%a')`    | 查找任何以"a"结尾的值                      |
| `Column.like('%or%')`  | 查找任何在任意位置包含"or"的值          |
| `Column.like('_r%')`   | 查找任何在第二个位置包含"r"的值    |
| `Column.like('a_%_%')` | 查找任何以"a"开头且≥3个字符的值 |
| `Column.like('a%o')`   | 查找任何以"a"开头且以"o"结尾的值  |

### `Column.rlike(regex)`

返回一个基于正则表达式匹配的布尔列表达式，由字符串字面量或列提供：

```python
df = df.filter(F.col('phone').rlike('[0-9]{3}(?:.+)?[0-9]{3}(?:.+)?[0-9]{4}'))
# 过滤数据框中的行，其中 'phone' 列的值匹配正则表达式。
# 正则表达式 '[0-9]{3}(?:.+)?[0-9]{3}(?:.+)?[0-9]{4}' 用于匹配格式为 3 位数字 - 任意字符（可选） - 3 位数字 - 任意字符（可选） - 4 位数字 的字符串。
# 这通常用于匹配美国电话号码，格式可能是 "123-456-7890" 或 "123 456 7890" 等。
```

如果正确利用，正则表达式非常强大。以下是一些帮助您入门的资源：

* [正则表达式备忘单 ↗](https://medium.com/factory-mind/regex-tutorial-a-simple-cheatsheet-by-examples-649dc1c3f285)，包含示例
* [正则表达式练习板 ↗](https://regexr.com/)，用于测试正则表达式

## 起始为，结尾为，包含

### `Column.startswith(string)`

返回一个布尔列表达式，指示列的字符串值是否以参数中提供的字符串（字面量或其他列）起始。

```python
df = df.filter(F.col("id").startswith("prefix-"))
# 过滤数据框 df，使得仅保留 "id" 列以 "prefix-" 开头的行
```

### `Column.endswith(string)`

返回一个布尔型列表达式，表示列的字符串值是否以参数中提供的字符串（字面量或其他列）结尾。

```python
# 过滤数据框中的行，其中"id"列的值以"-suffix"结尾
df = df.filter(F.col("id").endswith("-suffix"))
```

### `Column.contains(string)`

返回一个布尔列表达式，指示列的字符串值是否包含参数中提供的字符串（字面量或其他列）。

```python
df = df.filter(F.col("id").contains("string"))
# 过滤数据框中的行，只保留 "id" 列包含 "string" 的行
```

## 子字符串

### `Column.substr(startPos, length)`

返回一个字符串列表达式，该表达式计算列值的子字符串。

参数：

* **startPos** - 起始位置，从1开始计数（int 或 Column）
* **length** - 子字符串的长度（int 或 Column）

1. 创建子字符串列

   ```python
   df = df.select(F.col("name").substr(1, 3).alias("col"))
   ```

   | col   |
   | ----- |
   | "Ali" |
   | "Bob" |

2. 筛选子字符串

   ```python
   df = df.filter(F.col("phone").substr(5, 3) == "555")
   ```

   | phone          |
   | -------------- |
   | "323-555-1234" |
   | "897-555-4126" |
   | ...            |

## 等于其中之一

### `Column.isin(*cols)`

返回一个布尔表达式，如果列的值包含在参数的评估值中（以参数列表或列或文字的数组形式），则评估为 `True`。

```python
df = df.filter(F.col("name").isin("Bob", "Mike"))
# 过滤DataFrame，保留"name"列中值为"Bob"或"Mike"的行
```

| age  | name  |
| ---- | ----- |
| 5    | "Bob" |
| ...  | ...   |

```python
# 筛选出 age 列中值为 1, 2 或 3 的行
df = df.filter(F.col("age").isin([1, 2, 3]))
```

## Between

### `Column.between(lowerBound, upperBound)`

返回一个布尔表达式，如果表达式的值在 lowerBound 和 upperBound 字面值或列之间（包括边界），则该表达式将评估为 `True`。

```python
# 创建一个列 within_range，判断 age 是否在 10 到 upperBound 之间，并将其作为别名 age_within_range
within_range = F.col("age").between(10, df.upperBound).alias("age_within_range")

# 从 DataFrame df 中选择 name, upperBound, age 和 age_within_range 这四个列
df = df.select(df.name, df.upperBound, df.age, within_range)
```

| 名字     | 上限       | 年龄  | 年龄是否在范围内 |
| -------- | ---------- | ---- | ---------------- |
| "Taylor" | 30         | 35   | `False`          |
| "Sally"  | 40         | 34   | `True`           |
| "Lucy"   | 28         | 28   | `True`           |

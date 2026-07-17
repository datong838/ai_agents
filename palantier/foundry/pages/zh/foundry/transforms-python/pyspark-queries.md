---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/pyspark-queries/",
  "title": "概念: 查询",
  "page_id": "pyspark-queries",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/pyspark-columns/",
  "next": "/zh/foundry/transforms-python/pyspark-udfs/",
  "scraped_at": "2026-07-13T06:08:13.490563+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概念: 查询

### 去重，删除重复项

#### `DataFrame.distinct()`

返回一个新的`DataFrame`，其中包含源`DataFrame`中的不同行。

```python
df = df.distinct()
# 删除 DataFrame 中的重复行
```

#### `DataFrame.drop_duplicates(subset=None)`

返回一个新的`DataFrame`，其中重复行已被删除，非必填时仅考虑某些列。

```python
# 删除DataFrame中的重复行
df = df.drop_duplicates()

# 删除DataFrame中基于"firstname"和"lastname"列的重复行
df = df.drop_duplicates(["firstname", "lastname"])
```

### 删除空值

#### `DataFrame.dropna(how='any', thresh=None, subset=None)`

别名: `DataFrame.na.dropna(how='any', thresh=None, subset=None)`

返回一个新的 `DataFrame`，省略包含空值的行。`DataFrame.dropna()` 和 `DataFrameNaFunctions.drop()` 是彼此的别名。

参数：

* **how** – `'any'` 或 `'all'`。
  * 如果为 `'any'`，则如果行中包含任何空值，则删除该行。
  * 如果为 `'all'`，则仅当行中所有值都为空时才删除该行。
* **thresh** – 整数，默认 `None`。如果指定，则删除非空值少于thresh的行。（这将覆盖how参数）。
* **subset** – 非必填列名列表以考虑。

### 限制行数

#### `DataFrame.limit(number)`

### 排序

#### `DataFrame.sort(*cols, **kwargs)`

别名: `DataFrame.orderBy(*cols, **kwargs)`

* `Column.asc()` 或 `F.asc(col)`
* `Column.desc()` 或 `F.desc(col)`

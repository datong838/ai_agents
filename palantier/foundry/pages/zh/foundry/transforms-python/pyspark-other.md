---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/pyspark-other/",
  "title": "其他",
  "page_id": "pyspark-other",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/pyspark-logging/",
  "next": "/zh/foundry/transforms-java/overview/",
  "scraped_at": "2026-07-13T06:08:30.319887+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 其他

## 集合

* `array(*cols)`
* `array_contains(col, value)`
* `size(col)`
* `sort_array(col, asc=True)`
* `struct(*cols)`

## 排序

* `asc(col)`
* `desc(col)`

## 二进制

* `bitwiseNOT(col)`
* `shiftLeft(col, numBits)`
* `shiftRight(col, numBits)`
* `shiftRightUnsigned(col, numBits)`

## 处理空值

* `coalesce(*cols)`
* `isnan(col)`
* `isnull(col)`

## 列

* `col(col) or column(col)`
* `create_map(*cols)`
* `explode(col)`
* `expr(str)`
* `hash(*cols)`
* `input_file_name()`
* `posexplode(col)`
* `sha1(col)`
* `sha2(col, numBits)`
* `soundex(col)`
* `spark_partition_id()`

## JSON

* `from_json(col, schema, options={})`
* `get_json_object(col, path)`
* `json_tuple(col, *fields)`
* `to_json(col, options={})`

## 检查点

* `checkpoint(eager=True)`
  * 您可以通过在Spark上下文中使用`setCheckpointDir(dir)`函数设置自定义检查点目录，该上下文可以通过`ctx.spark_session.sparkContext`访问。确保将`ctx`作为输入参数包含在变换的`compute()`函数中。
  * 请记住，您只需要设置一次检查点目录。任何后续尝试将检查点设置为相同目录的操作都会导致RDD错误。
* `localCheckpoint(eager=True)`

:::callout{theme="neutral"}
`checkpoint()`函数用于将DataFrame临时存储在磁盘上，而`localCheckpoint()`将它们存储在执行器内存中。使用`localCheckpoint()`时，您无需设置目录。使用`eager`参数值来设置DataFrame是否立即进行检查点（默认值为`True`）。
:::

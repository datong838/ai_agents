---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/transforms-python-api-classes/",
  "title": "变换类",
  "page_id": "transforms-python-api-classes",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/transforms-python-api/",
  "next": "/zh/foundry/transforms-python/transforms-python-foundry-connectors/",
  "scraped_at": "2026-07-13T06:08:04.458365+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 变换类

| 类 | 描述 |
|---|---|
| [`Check`](#check) | 封装一个期望，以便可以在数据健康中注册。 |
| [`FileStatus`](#filestatus) | 一个collections.namedtuple，捕获关于FoundryFS文件的详细信息。 |
| [`FileSystem(foundry_fs[, read_only])`](#filesystem) | 用于读取和写入数据集文件的文件系统对象。 |
| [`IncrementalTransformContext`(ctx, is\_incremental)](#incrementaltransformcontext) | 增强了增量计算功能的TransformContext。 |
| [`IncrementalTransformInput`(tinput\[, prev\_txrid\])](#incrementaltransforminput) | 增强了增量计算功能的TransformInput。 |
| [`IncrementalTransformOutput`(toutput\[, …\])](#incrementaltransformoutput) | 增强了增量计算功能的TransformOutput。 |
| [`Input`(alias)](#input) | 变换输入的规范。 |
| [`Output`(alias\[, sever\_permissions\])](#output) | 变换输出的规范。 |
| [`Pipeline`()](#pipeline) | 用于分组一组Transform对象的对象。 |
| [`Transform`(compute\_func\[, inputs, outputs, ...\])](#transform) | 描述计算单步骤的可调用对象。 |
| [`TransformContext`(foundry\_connector\[, parameters\])](#transformcontext) | 可以选择注入到变换的计算函数中的上下文对象。 |
| [`TransformInput`(rid, branch, txrange, …)](#transforminput) | 在运行时传递给Transform对象的输入对象。 |
| [`LightweightInput`(alias)](#lightweightinput) | 在运行时传递给轻量级变换对象的输入对象。 |
| [`IncrementalLightweightInput`(alias)](#incrementallightweightinput) | 在运行时传递给增量轻量级变换对象的输入对象。 |
| [`TransformOutput`(rid, branch, txrid, …)](#transformoutput) | 在运行时传递给Transform对象的输出对象。 |
| [`LightweightOutput`(alias)](#lightweightoutput) | 在运行时传递给轻量级变换对象的输入对象。 |

## `Check`

### *class* `transforms.api.Check`

封装一个期望，以便可以在数据健康中注册。

* **`expectation`**
  * *Expectation* – 要评估的期望。
* **`name`**
  * *str* – 检查的名称，用作稳定的标识符。
* **`is_incremental`**
  * *bool* – 如果变换是增量运行的。
* **`on_error`**
  * *(str, 非必填)* – 如果期望不符合，采取的操作。目前有 'WARN', 'FAIL'。
* **`description`**
  * *(str, 非必填)* – 检查的描述。

***

## `FileStatus`

***class* `transforms.api.FileStatus`**

一个`collections.namedtuple`，捕获关于FoundryFS文件的详细信息。

创建FileStatus(path, size, modified)的新实例

* **`count`(*value*) → integer -- 返回值的出现次数**
* **`index`(*value*\[, *start*\[, *stop*]]) → integer -- 返回值的第一个索引**
  * 如果值不存在则引发ValueError
* **`modified`**
  * 字段编号2的别名
* **`path`**
  * 字段编号0的别名
* **`size`**
  * 字段编号1的别名

***

## `FileSystem`

***class* `transforms.api.FileSystem`(*foundry\_fs*, *read\_only=False*)**

用于读取和写入数据集文件的文件系统对象。

* **`files`(*glob=None*, *regex='.\*'*, *show\_hidden=False*, *packing\_heuristic=None*)**
  * 创建一个[`DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html) ，包含此数据集中可访问的路径。
  * [`DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html) 按文件大小分区，每个分区包含总大小最多为`spark.files.maxPartitionBytes`字节的文件路径，或者如果单个文件大于`spark.files.maxPartitionBytes`则按单个文件分区。文件的大小计算为其磁盘文件大小加上`spark.files.openCostInBytes`。
  * **参数**
    * **glob** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)*, 非必填\_) – Unix文件匹配模式。支持globstar；要递归搜索文件（例如`pdf`），请使用`**/*.pdf`。
    * **regex** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)*, 非必填\_) – 匹配文件名的正则表达式模式。
    * **show\_hidden** (*[bool ↗](https://docs.python.org/3/library/stdtypes.html#boolean-values)*, 非必填\_) – 包括隐藏文件，即以`.`或`_`开头的文件。
    * **packing\_heuristic** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)*, 非必填\_) – 指定用于将文件打包到Spark分区中的启发式。可能的选择有`ffd`（First Fit Decreasing）或`wfd`（Worst Fit Decreasing）。虽然`wfd`产生的分布不均匀，但速度更快，因此推荐用于包含大量文件的数据集。如果未指定启发式，将自动选择一个。
  * **返回**
    * 包含(path, size, modified)的DataFrame
  * **返回类型**
    * pyspark.sql.DataFrame
* **`ls`(*glob=None*, *regex='.\*'*, *show\_hidden=False*)**
  * 递归遍历所有目录，并列出从数据集根目录起匹配给定模式的所有文件。
  * **参数**
    * **glob** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)*, 非必填\_) – Unix文件匹配模式。支持globstar；要递归搜索文件（例如`pdf`），请使用`**/*.pdf`。
    * **regex** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)*, 非必填\_) – 匹配文件名的正则表达式模式。
    * **show\_hidden** (*[bool ↗](https://docs.python.org/3/library/stdtypes.html#boolean-values)*, 非必填\_) – 包括隐藏文件，即以`.`或`_`开头的文件。
  * **生成**
    * `FileStatus` - 逻辑路径、文件大小（字节）、修改时间戳（自1970年1月1日UTC以来的毫秒数）。
* **`open`(\_path, *mode='r'*, *kwargs*)**
  * 以给定模式打开FoundryFS文件。`kwargs`是关键字参数。
  * **参数**
    * **path** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)*) – 数据集中文件的逻辑路径。
    * **kwargs** – 剩余的关键字参数传递给[`io.open()` ↗](https://docs.python.org/3/library/io.html#io.open)
    * **show\_hidden** (*[bool ↗](https://docs.python.org/3/library/stdtypes.html#boolean-values)*, 非必填\_) – 包括隐藏文件，即以`.`或`_`开头的文件。
  * **返回**
    * 连接到流的Python文件对象。
  * **返回类型**
    * 文件

***

## `IncrementalTransformContext`

### *class* `transforms.api.IncrementalTransformContext`(*ctx*, *is\_incremental*)

带有增量计算功能的[TransformContext](#transformcontext)。

* **`auth_header`**
  * *str* – 用于运行变换的身份验证头。
* **`fallback_branches`**
  * *List\[str]* – 运行变换时配置的回退分支。
* **`is_incremental`**
  * *bool* – 如果变换是增量运行的。
* **`parameters`**
  * *dict of (str, any)* – 变换参数。
* **`spark_session`**
  * *pyspark.sql.SparkSession* – 用于运行变换的Spark会话。

***

## `IncrementalTransformInput`

### *class* `transforms.api.IncrementalTransformInput`(*tinput*, *prev\_txrid=None*)

具有增量计算功能的[TransformInput](#transforminput)。

* **`dataframe`(*mode='added'*)**
  * 返回给定读取模式的`pyspark.sql.DataFrame`。
  * 仅支持\_current\_，\_previous\_和\_added\_模式。
  * **参数**
    * **mode** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*) – 读取模式之一，*current*，*previous*，*added*，*modified*，*removed*。默认\_added\_
  * **返回**
    * 数据集的DataFrame。
  * **返回类型**
    * [`Dataframe` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)
* **`filesystem`(*mode='added'*)**
  * 为给定读取模式从\_FoundryFS\_构建一个\_FileSystem\_对象。
  * 仅支持\_current\_，\_previous\_和\_added\_模式。
  * **参数**
    * **mode** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*) – 读取模式之一，*current*，*previous*，*added*，*modified*，*removed*。默认\_added\_
  * **返回**
    * 给定视图的文件系统对象。
  * **返回类型**
    * [`FileSystem`](#filesystem)
* **`pandas()`**
  * [pandas.DataFrame ↗](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html#pandas.DataFrame): 包含输入数据集完整视图的Pandas DataFrame。
* **`branch`**
  * *str* – 输入数据集的分支。
* **`path`**
  * *str* – 输入数据集的项目路径。
* **`rid`**
  * *str* – 数据集的资源标识符。

***

## `IncrementalTransformOutput`

**class `transforms.api.IncrementalTransformOutput`(*toutput*, *prev\_txrid=None*, *mode='replace'*)**

具有增量计算功能的[TransformOutput](#transformoutput)。

* **`abort()`**
  * 中止事务，允许任务成功完成而不写入任何数据。有关更多详细信息，请参见[Python Abort](/zh/foundry/transforms-python/abort-transactions/)。
* **`dataframe`(*mode='current'*, *schema=None*)**
  * 返回给定读取模式的[pyspark.sql.DataFrame ↗](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame)。
  * **参数**
    * **mode** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*) – 读取模式之一，*current*，*previous*，*added*，*modified*，*removed*。默认\_current\_。
    * **schema** (*pyspark.types.StructType, 非必填*) - 构建空DataFrame时使用的PySpark模式。使用读取模式‘previous’时必须提供。
  * **返回**
    * 数据集的DataFrame。
  * **返回类型**
    * [`DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)
  * **引发**
    * [`ValueError` ↗](https://docs.python.org/3/library/exceptions.html#ValueError) - 如果使用模式‘previous’时未传递任何模式
* **`filesystem`(*mode='current'*)**
  * 构建一个用于写入\_FoundryFS\_的\_FileSystem\_对象。
  * **参数**
    * **mode** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*) – 读取模式之一，*added*，*current\_或\_previous*。默认值为current\_。仅可写入当前文件系统。
  * **引发**
    * [`NotImplementedError` ↗](https://docs.python.org/3/library/exceptions.html#NotImplementedError) – 当前不支持。
* **`pandas`(*mode='current'*)**
  * [pandas.DataFrame ↗](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html): 给定读取模式的Pandas DataFrame。
* **`set_mode`(*mode*)**
  * 更改数据集的写入模式。
  * **参数**
    * **mode** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)*) – 写入模式之一‘replace’或‘modify’。在modify模式下，写入输出的任何内容都会追加到数据集中。在replace模式下，写入输出的任何内容都会替换数据集。

:::callout{theme="neutral"}
数据写入后无法更改写入模式。
:::

* **`write_dataframe`(*df*, *partition\_cols=None*, *bucket\_cols=None*, *bucket\_count=None*, *sort\_by=None*, *output\_format=None*, *options=None*)**
  * 将给定的[DataFrame ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)写入输出数据集。
  * **参数**
    * **df** (\_[pyspark.sql.DataFrame ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)) – 要写入的PySpark DataFrame。
    * **partition\_cols** (*List\[[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)], 非必填*) - 写入数据时使用的列分区。
    * **bucket\_cols** (*List\[[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)], 非必填*) – 数据分桶的列。如果指定了bucket\_count，则必须指定。
    * **bucket\_count** (*[int ↗](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex), 非必填*) – 桶的数量。如果指定了bucket\_cols，则必须指定。
    * **sort\_by** (*List\[[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)], 非必填*) – 按哪个列对分桶数据进行排序。
    * **output\_format** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*) – 输出文件格式，默认为‘parquet’。
    * **options** (*[dict ↗](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict), 非必填*) – 传递给`org.apache.spark.sql.DataFrameWriter#option(String, String)`的其他选项。
* **`write_pandas`(*pandas\_df*)**
  * 将给定的[pandas.DataFrame ↗](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)写入输出数据集。
  * **参数**
    * **pandas\_df** (*[pandas.DataFrame ↗](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)*) – 要写入的DataFrame。
* **`branch`**
  * *str* – 数据集的分支。
* **`path`**
  * *str* – 数据集的项目路径。
* **`rid`**
  * *str* – 数据集的资源标识符。

***

## `Input`

***class* `transforms.api.Input`(*alias*, *branch*, *stop\_propagating*, *stop\_requiring*, *checks*)**

变换输入的规范。

* **参数**
  * **alias** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*) – 数据集的rid或数据集的绝对项目路径。如果未指定，参数未绑定。
  * **branch** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*)：解决输入数据集的分支名称。如果未指定，在搭建时解决。
  * **stop\_propagating** (*Markings, 非必填*)：要停止从此传播的安全权限标记。请参阅[权限标记](/zh/foundry/platform-security-management/manage-markings/#remove-an-inherited-marking)和[删除继承的权限标记](/zh/foundry/building-pipelines/remove-inherited-markings/)文档。
  * **stop\_requiring** (*OrgMarkings, 非必填*)：在此输入上假定的组织权限标记。
  * **checks** (*List\[Check], Check, 非必填*)：一个或多个\:class:`Check`对象。
  * **failure\_strategy** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*)：输入更新失败时的策略。必须是`continue`或`fail`之一。如果未指定，默认为`fail`。

## `Output`

***class* `transforms.api.Output`(*alias=None*, *sever\_permissions=False*, *checks=None*)**

变换输出的规范。

* **参数**
  * **alias** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*) - 数据集的rid或数据集的绝对项目路径。如果未指定，参数未绑定。
  * **sever\_permissions** (*[bool ↗](https://docs.python.org/3/library/stdtypes.html#boolean-values), 非必填*) - 如果为true，则将数据集的权限与其输入的权限分离。如果参数未绑定，则忽略
  * **checks** (*List\[Check], Check, 非必填*) - 一个或多个\:class:`Check`对象。

***

## `Pipeline`

***class* `transforms.api.Pipeline`**

用于分组一组[Transform](#transform)对象的对象。

* **`add_transforms`(*\*transforms*)**
  * 将给定的Transform对象注册到\_Pipeline\_实例。
  * **参数**
    * **transforms** (*[Transform](#transform)*) – 要注册的变换。
  * **引发**
    * [`ValueError` ↗](https://docs.python.org/3/library/exceptions.html#ValueError) – 如果多个`Transform`对象写入相同的[`Output`](#output)别名。
* **`discover_transforms`(*\*modules*)**
  * 递归查找并导入模块，注册每个模块级变换。
  * 此方法递归查找并导入从给定模块的\_\_\_路径\_\_\_开始的模块。每个找到的模块都会被导入，并且任何作为[`Transform`](#transform)实例的属性（通过变换装饰器构造）都将被注册到管道。
  * **参数**
    * **modules** (*module*) – 开始搜索的模块。

```python
>>> import myproject
>>> p = Pipeline()
>>> p.discover_transforms(myproject)
# 该代码导入了一个名为 myproject 的模块。
# 然后创建了一个 Pipeline 对象实例 p。
# 接着调用 p 的 discover_transforms 方法，传入 myproject 模块。
# 这个方法可能用于在 myproject 中发现或注册一些数据转换操作。
```

:::callout{theme="neutral"}
找到的每个模块都会被导入。尽量避免在模块级别执行代码。
:::

* **`transforms`**
  * *List\[Transform]* – 注册到管道中的变换列表。

***

## `Transform`

***class* `transforms.api.Transform`(*compute\_func*, *inputs=None*, *outputs=None*, *profile=None*)**

一个描述计算单步骤的可调用对象。

一个变换由若干[`Input`](#input)规格、若干[`Output`](#output)规格和一个计算函数组成。

使用提供的装饰器构建Transform对象是惯用的： [`transform()`](/zh/foundry/transforms-python/transforms-python-api/#transform), [`transform_df()`](/zh/foundry/transforms-python/transforms-python-api/#transform_df), 和 [`transform_pandas()`](/zh/foundry/transforms-python/transforms-python-api/#transform_pandas)。

注意：原始的计算函数通过Transform的`__call__`方法暴露。

* **参数**
  * **compute\_func** (*Callable*) –  用于包装的计算函数。
  * **inputs** (*Dict\[[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), [Input](#input)]*) - 映射输入名称到[`Input`](#input)规格的字典。
  * **outputs** (*Dict\[[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), [Output](#output)]*) - 映射输入名称到[`Output`](#output)规格的字典。
  * **profile** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*) – 在运行时使用的变换配置文件名称。

* **`compute`(*ctx=None*, \_**&#x6B;wargs\_)\*\*
  * 使用上下文及一组输入和输出计算变换。
  * **参数**
    * **ctx** (*[TransformContext](#transformcontext), 非必填*) – 如果请求，传递给变换的上下文对象。
    * **kwargs** (*[TransformInput](#transforminput) 或 [TransformOutput](#transformoutput)*) - 映射输入名称到[`Input`](#input)规格的字典。*kwarg*是关键字参数的缩写。
    * **outputs** (*Dict\[[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), [Output](#output)]*) - 传递给计算函数的输入、输出和上下文对象。
  * **返回**
    * 运行变换后的输出对象。
  * **返回类型**
    * dict of ([str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), [TransformOutput](#transformoutput))

* **`version`**
  * *str* – 一个用于比较两个变换版本的字符串，用于考虑逻辑陈旧性。
  * 例如，一个SQL变换可能会获取SQL查询的哈希值。理想情况下，SQL查询应被转换为一个格式，以便对语义上等效的变换产生相同的版本。即SQL查询`select A, B from foo;`应该与`SQL查询 select A, B from (select * from foo);`具有相同的版本。
  * 如果没有指定版本，将使用存储库的版本。
  * **引发**
    * [`ValueError` ↗](https://docs.python.org/3/library/exceptions.html#ValueError) – 如果计算函数的对象哈希失败

***

## `TransformContext`

**class `transforms.api.TransformContext`(*foundry\_connector*, *parameters=None*)**
可以选择注入到变换计算函数中的上下文对象。

* **`auth_header`**
  * *str* – 用于运行变换的授权头。此授权头具有有限的范围，并且只有运行任务所需的权限。它不应用于API调用。
* **`fallback_branches`**
  * *List\[str]* – 在运行变换时配置的回退分支。
* **`parameters`**
  * *dict of (str, any)* – 变换参数。
* **`spark_session`**
  * *pyspark.sql.SparkSession* – 用于运行变换的Spark会话。

***

## `TransformInput`

***class* `transforms.api.TransformInput`(*rid*, *branch*, *txrange*, *dfreader*, *fsbuilder*)**

在运行时传递给Transform对象的输入对象。

* **`dataframe()`**
  * 返回给定读取模式的[pyspark.sql.DataFrame ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)。
  * **返回**
    * 数据集的数据框。
  * **返回类型**
    * [pyspark.sql.DataFrame ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)
* **`filesystem()`**
  * 构建一个用于从\_FoundryFS\_读取的\_FileSystem\_对象。
  * **返回**
    * 一个用于从Foundry读取的\_FileSystem\_对象。
  * **返回类型**
    * [FileSystem](#filesystem)
* **`pandas()`**
  * [pandas.DataFrame ↗](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html): 包含输入数据集全视图的Pandas数据框。
* **`branch`**
  * *str* – 输入数据集的分支。
* **`path`**
  * *str* – 输入数据集的项目路径。
* **`rid`**
  * *str* – 数据集的资源标识符。
* **`column_descriptions`**
  * *Dict\<str, str>* – 数据集的列描述。
* **`column_typeclasses`**
  * *Dict\<str, str>* – 数据集的列类型类。

***

## `LightweightInput`

***class* `transforms.api.LightweightInput`(*alias*)**

其目的是通过委托给Foundry Data Sidecar模仿[`TransformInput`](#transforminput)的API子集，同时通过支持各种数据格式进行扩展。

* **`dataframe()`**
  * 返回一个包含数据集的[pandas.DataFrame ↗](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)。它是`pandas()`的别名。
  * **返回**
    * 数据集的数据框。
  * **返回类型**
    * [pandas.DataFrame ↗](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
* **`filesystem()`**
  * 构建一个用于从\_FoundryFS\_读取的\_FileSystem\_对象。
  * **返回**
    * 一个用于从Foundry读取的\_FileSystem\_对象。
  * **返回类型**
    * [FileSystem](#filesystem)
* **`pandas()`**
  * 返回一个包含数据集的[pandas.DataFrame ↗](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)。
  * **返回**
    * 数据集的数据框。
  * **返回类型**
    * [pandas.DataFrame ↗](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
* **`arrow()`**
  * 返回一个包含数据集的[pyarrow.Table ↗](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html)。
  * **返回**
    * 数据集的表。
  * **返回类型**
    * [pyarrow.Table ↗](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html)
* **`polars(lazy: Optional[bool]=False)`**
  * 根据`lazy`参数的值返回一个[polars.DataFrame ↗](https://docs.pola.rs/api/python/stable/reference/dataframe/index.html)或[polars.LazyFrame ↗](https://docs.pola.rs/api/python/stable/reference/lazyframe/index.html)。
  * **返回**
    * 数据集的数据框。
  * **返回类型**
    * [polars.DataFrame ↗](https://docs.pola.rs/api/python/stable/reference/dataframe/index.html) 或 [polars.LazyFrame ↗](https://docs.pola.rs/api/python/stable/reference/lazyframe/index.html)
* **`path()`**
  * 返回一个包含下载的数据集文件路径的[str ↗](https://docs.python.org/3/library/string.html)，这些文件可能是CSV、Parquet或Avro文件。
  * **返回**
    * 包含数据集文件的目录路径。
  * **返回类型**
    * [str ↗](https://docs.python.org/3/library/string.html)

***

## `IncrementalLightweightInput`

***class* `transforms.api.IncrementalLightweightInput`(*alias*)**

其目的是通过委托给Foundry Data Sidecar模仿[`IncrementalTransformInput`](#incrementaltransforminput)的API子集，同时通过支持各种数据格式进行扩展。它是[`LightweightInput`](#lightweightinput)的增量对应物。

* **`dataframe`(*mode*)**
  * 返回一个包含数据集的[pandas.DataFrame ↗](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)。它是`pandas()`的别名。
  * **参数**
    * **mode** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*) – 读取模式之一，*current*、*previous*、*added*、*modified*、*removed*。默认为\_added\_。
  * **返回**
    * 数据集的数据框。
  * **返回类型**
    * [pandas.DataFrame ↗](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
* **`filesystem()`**
  * 构建一个用于从\_FoundryFS\_读取的\_FileSystem\_对象。
  * **返回**
    * 一个用于从Foundry读取的\_FileSystem\_对象。
  * **返回类型**
    * [FileSystem](#filesystem)
* **`pandas()`(*mode*)**
  * 返回一个包含数据集的[pandas.DataFrame ↗](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)。
  * **参数**
    * **mode** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*) – 读取模式之一，*current*、*previous*、*added*、*modified*、*removed*。默认为\_added\_。
  * **返回**
    * 数据集的数据框。
  * **返回类型**
    * [pandas.DataFrame ↗](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
* **`arrow()`(*mode*)**
  * 返回一个包含数据集的[pyarrow.Table ↗](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html)。
  * **参数**
    * **mode** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*) – 读取模式之一，*current*、*previous*、*added*、*modified*、*removed*。默认为\_added\_。
  * **返回**
    * 数据集的表。
  * **返回类型**
    * [pyarrow.Table ↗](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html)
* **`polars`(*lazy=False*, *mode*)**
  * 根据`lazy`参数的值返回一个[polars.DataFrame ↗](https://docs.pola.rs/api/python/stable/reference/dataframe/index.html)或[polars.LazyFrame ↗](https://docs.pola.rs/api/python/stable/reference/lazyframe/index.html)。
  * **参数**
    * **lazy** (*Optional\[bool]*) – 选择惰性或急切的Polars数据框。
    * **mode** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*) – 读取模式之一，*current*、*previous*、*added*、*modified*、*removed*。默认为\_added\_。
  * **返回**
    * 数据集的数据框。
  * **返回类型**
    * [polars.DataFrame ↗](https://docs.pola.rs/api/python/stable/reference/dataframe/index.html) 或 [polars.LazyFrame ↗](https://docs.pola.rs/api/python/stable/reference/lazyframe/index.html)。
* **`path`(*mode*)**
  * 返回一个包含下载的数据集文件路径的[str ↗](https://docs.python.org/3/library/string.html)，这些文件可能是CSV、Parquet或Avro文件。
  * **参数**
    * **mode** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*) – 读取模式之一，*current*、*previous*、*added*、*modified*、*removed*。默认为\_added\_
  * **返回**
    * 包含数据集文件的目录路径。
  * **返回类型**
    * [str ↗](https://docs.python.org/3/library/string.html)

***

## `TransformOutput`

**class `transforms.api.TransformOutput`(*rid*, *branch*, *txrid*, *dfreader*, *dfwriter*, *fsbuilder*)**

在运行时传递给Transform对象的输出对象。

* **`abort()`**
  * 中止事务，允许任务成功完成而不写入任何数据。有关更多详细信息，请参见[Python Abort](/zh/foundry/transforms-python/abort-transactions/)。
* **`dataframe()`**
  * 返回一个包含输出数据集全视图的[pyspark.sql.DataFrame ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)。
  * **返回**
    * 数据集的数据框。
  * **返回类型**
    * *[pyspark.sql.DataFrame ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)*
* **`filesystem()`**
  * 构建一个用于写入到\_FoundryFS\_的\_FileSystem\_对象。
  * **返回**
    * 一个用于写入到Foundry的\_FileSystem\_对象。
* **返回类型**
  * *[FileSystem](#filesystem)*
* **`pandas()`**
  * [pandas.DataFrame ↗](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html): 包含输出数据集全视图的Pandas数据框。
* **`set_mode`(*mode*)**
  * 更改数据集的写入模式。
  * **参数**
    * **mode** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)*) – 写入模式之一，‘replace’或‘modify’。在修改模式下，写入到输出的任何内容都会追加到数据集中。在替换模式下，写入到输出的任何内容都会替换数据集。
* **`write_dataframe`(*df*, *partition\_cols=None*, *bucket\_cols=None*, *bucket\_count=None*, *sort\_by=None*, *output\_format=None*, *options=None*, *column\_descriptions=None*, *column\_typeclasses=None*)**
  * 将给定的[DataFrame ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)写入到输出数据集中。
  * **参数**
    * **df** (*[pyspark.sql.DataFrame ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)*) – 要写入的PySpark数据框。
    * **partition\_cols** (*List\[[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)], 非必填*) - 写入数据时要使用的列分区。
    * **bucket\_cols** (*List\[[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)], 非必填*) - 用于对数据进行分桶的列。如果指定了`bucket_count`，则必须指定。
    * **bucket\_count** (*[int ↗](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex), 非必填*) – 桶的数量。如果指定了`bucket_cols`，则必须指定。
    * **sort\_by** (*List\[[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)], 非必填*) - 用于对分桶数据进行排序的列。
    * **output\_format** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*) - 输出文件格式，默认为'parquet'。文件格式基于Spark的[DataFrameWriter ↗](https://spark.apache.org/docs/latest/api/java/org/apache/spark/sql/DataFrameWriter.html)及其他类型，包括'csv'、'json'、'orc'和'text'。
    * **options** (*[dict ↗](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict), 非必填*) - 传递给`org.apache.spark.sql.DataFrameWriter#option(String, String)`的额外选项。
    * **column\_descriptions** (*Dict\[[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), [str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)], 非必填*) - 列名称到其字符串描述的映射。此映射与DataFrame的列相交，必须包含描述（最多800个字符）。
    * **column\_typeclasses** (*Dict\[[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), List\[Dict\[[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), [str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)]], 非必填*) - 列名称到其列类型类的映射。列表中的每个类型类是一个\_Dict\[[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), [str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)]\_，其中只有两个键是有效的："name"和"kind"。这些键中的每一个都映射到用户想要的相应字符串。
* **`write_pandas`(*pandas\_df*)**
  * 将给定的[pandas.DataFrame ↗](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)写入到输出数据集中。
  * **参数**
    * **pandas\_df** (*[pandas.DataFrame ↗](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)*) – 要写入的数据框。
* **`branch`**
  * *str* – 数据集的分支。
* **`path`**
  * *str* – 数据集的项目路径。
* **`rid`**
  * *str* – 数据集的资源标识符。

***

## `LightweightOutput`

***class* `transforms.api.LightweightInput`(*alias*)**

其目的是通过委托给Foundry Data Sidecar模仿[`TransformOutput`](#transformoutput)的API子集。

* **`filesystem()`**
  * 构建一个用于从\_FoundryFS\_读取的\_FileSystem\_对象。
  * **返回**
    * 一个用于从Foundry读取的\_FileSystem\_对象。
  * **返回类型**
    * [FileSystem](#filesystem)
* **`dataframe()`**
  * 返回一个包含数据集的[pandas.DataFrame ↗](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)。它是`pandas()`的别名。
  * **返回**
    * 数据集的数据框。
  * **返回类型**
    * [pandas.DataFrame ↗](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
* **`pandas()`**
  * 返回一个包含数据集的[pandas.DataFrame ↗](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)。
  * **返回**
    * 数据集的数据框。
  * **返回类型**
    * [pandas.DataFrame ↗](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
* **`arrow()`**
  * 返回一个包含数据集的[pyarrow.Table ↗](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html)。
  * **返回**
    * 数据集的表。
  * **返回类型**
    * [pyarrow.Table ↗](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html)
* **`polars(lazy: Optional[bool]=False)`**
  * 根据`lazy`参数的值返回一个[polars.DataFrame ↗](https://docs.pola.rs/api/python/stable/reference/dataframe/index.html)或[polars.LazyFrame ↗](https://docs.pola.rs/api/python/stable/reference/lazyframe/index.html)。
  * **返回**
    * 数据集的数据框。
  * **返回类型**
    * [polars.DataFrame ↗](https://docs.pola.rs/api/python/stable/reference/dataframe/index.html) 或 [polars.LazyFrame ↗](https://docs.pola.rs/api/python/stable/reference/lazyframe/index.html)
* **`path()`**
  * 返回一个包含下载的数据集文件路径的[str ↗](https://docs.python.org/3/library/string.html)，这些文件可能是CSV、Parquet或Avro文件。
  * **返回**
    * 包含数据集文件的目录路径。
  * **返回类型**
    * [str ↗](https://docs.python.org/3/library/string.html)
* **`write_pandas`(*pandas\_df*)**
  * 将给定的[pandas.DataFrame ↗](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)写入到输出数据集中。它委托给`write_table`。
  * **参数**
    * **pandas\_df** (*[pandas.DataFrame ↗](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)*) – 要写入的数据框。
* **`write_table`(*df*)**
  * 将给定的[pandas.DataFrame ↗](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)、[pyarrow.Table ↗](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html)、[polars.DataFrame ↗](https://docs.pola.rs/api/python/stable/reference/dataframe/index.html)或[polars.LazyFrame ↗](https://docs.pola.rs/api/python/stable/reference/lazyframe/index.html)，或`path`写入到输出数据集中。如果给定`path`（无论是`str`还是`pathlib.Path`），其值必须与`path_for_write_table`返回的值匹配。
  * **参数**
    * ***df*** (*[pandas.DataFrame ↗](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html), [pyarrow.Table ↗](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html), [polars.DataFrame ↗](https://docs.pola.rs/api/python/stable/reference/dataframe/index.html) 或 [polars.LazyFrame ↗](https://docs.pola.rs/api/python/stable/reference/lazyframe/index.html), 或 `path`*) – 要写入的数据框。
* **`path_for_write_table`**
  * 用于与`write_table`一起使用的数据集文件的路径。
  * **返回类型**
    * [str ↗](https://docs.python.org/3/library/string.html)
* **`set_mode`(*mode*)**
  * 更改数据集的写入模式。
  * **参数**
    * **mode** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)*) – 写入模式之一，‘replace’或‘modify’。在修改模式下，写入到输出的任何内容都会追加到数据集中。在替换模式下，写入到输出的任何内容都会替换数据集。

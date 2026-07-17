---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/transforms-python-foundry-connectors/",
  "title": "Foundry 连接器",
  "page_id": "transforms-python-foundry-connectors",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/transforms-python-api-classes/",
  "next": "/zh/foundry/transforms-python/media-sets/",
  "scraped_at": "2026-07-13T06:08:09.929952+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Foundry 连接器

用于从变换API与Foundry交互的连接器。

连接器可以交互式地构建 [`TransformInput`](/zh/foundry/transforms-python/transforms-python-api-classes/#transforminput) 和 [`TransformOutput`](/zh/foundry/transforms-python/transforms-python-api-classes/#transformoutput) 对象，还可以运行 [`Transform`](/zh/foundry/transforms-python/transforms-python-api-classes/#transform)。

## FoundryConnector

### *class* `transforms.foundry.connectors.FoundryConnector`(*service\_config*, *auth\_header*, *filesystem\_id=None*, *fallback\_branches=None*, *resolver=None*)

* 访问 *Foundry* 服务的入口点。
* *Foundry* 对象通过提供用于操作数据集的API来管理与Foundry服务的交互。

#### 参数

* **service\_config** (*[dict ↗](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)*)
  * 一个符合Java类com.palantir.remoting.api.config.service.ServicesConfigBlock中的JSON规范的配置字典。
* **auth\_header** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)*)
  * 连接到Foundry服务时使用的授权字符串。
* **filesystem\_id** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*)
  * 使用的支持文件系统。
* **fallback\_branches** (*List\[[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)], 非必填*)
  * 回退分支。
* **resolver** (*Callable\[\[[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)], [str ↗](https://docs.python.org/3/library/stdtypes.html#textseq)], 非必填*)
  * 用于将数据集别名解析为rid的函数。默认情况下，将别名解析为项目路径。

***

### `input`(*alias=None*, *rid=None*, *branch=None*, *end\_txrid=None*, *start\_txrid=None*, *schema\_version=None*)

* 从给定参数构建一个 [`TransformInput`](/zh/foundry/transforms-python/transforms-python-api-classes/#transforminput)。
* 用于构建 [`TransformInput`](/zh/foundry/transforms-python/transforms-python-api-classes/#transforminput) 的 *资源标识符* 将从给定的 `alias` 解析，除非传递了 `rid` 参数。

#### 参数

* **alias** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*)
  * 数据集的别名。
* **rid** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*)
  * 数据集的资源标识符。
* **branch** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*)
  * 从中读取数据集的分支。如果未设置，则选择 *Catalog* 中存在的 *fallbacks* 列表中的第一个分支。
* **end\_txrid** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*)
  * 视图的结束事务，如果未设置，则默认为给定分支上的最新事务。
* **start\_txrid** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*)
  * 视图的起始事务。
* **schema\_version** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*)
  * 读取时使用的架构版本，如果未设置，则默认为给定分支上的最新架构版本。

#### 返回

* 表示请求数据集的输入对象。

#### 返回类型

* [`transforms.api.TransformInput`](/zh/foundry/transforms-python/transforms-python-api-classes/#transforminput)

#### 抛出

* [`ValueError` ↗](https://docs.python.org/3/library/exceptions.html#ValueError)
  * 如果未指定 *alias* 或 *rid*（但不是同时）。
* [`ValueError` ↗](https://docs.python.org/3/library/exceptions.html#ValueError)
  * 如果未指定分支，并且在 *Catalog* 中找不到回退分支。

***

### `output`(*alias=None*, *rid=None*, *branch=None*, *txrid=None*, *filesystem\_id=None*)

* 从给定的别名或rid构建一个 [TransformOutput](/zh/foundry/transforms-python/transforms-python-api-classes/#transformoutput)。
* 用于构建 [`transforms.api.TransformOutput`](/zh/foundry/transforms-python/transforms-python-api-classes/#transformoutput) 的 *资源标识符* 将从给定的 `alias` 解析，除非传递了 `rid` 参数。

#### 参数

* **alias** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*)
  * 数据集的别名。
* **rid** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*)
  * 数据集的资源标识符。
* **branch** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*)
  * 将数据集写入的分支。如果未设置，则选择 *fallbacks* 列表中的第一个分支。
* **txrid** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*)
  * 应写入数据的事务。
* **filesystem\_id** (*[str ↗](https://docs.python.org/3/library/stdtypes.html#textseq), 非必填*)
  * 如果数据集尚不存在，则在其上创建数据集的文件系统。

#### 返回

* 表示请求数据集的输出对象。

#### 返回类型

* [`transforms.api.TransformOutput`](/zh/foundry/transforms-python/transforms-python-api-classes/#transformoutput)

#### 抛出

* [`ValueError` ↗](https://docs.python.org/3/library/exceptions.html#ValueError)
  * 如果未指定 *alias* 或 *rid*（但不是同时）。

***

### `run`(transform)

* 使用最新的输入和输出运行给定的 [Transform](/zh/foundry/transforms-python/transforms-python-api-classes/#transform)。

#### 参数

* **transform** ([transforms.api.Transform](/zh/foundry/transforms-python/transforms-python-api-classes/#transform))
  * 要运行的变换。

***

### `auth_header`

* *str*
  * 用于联系Foundry的授权头。

***

### `fallback_branches`

* *List\[str]*
  * 用于检索数据集的回退分支。

***

### `spark_session`

* [`pyspark.sql.SparkSession` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.html)
  * 理解由 *FoundrySparkManager* 创建的 *SparkSession*。

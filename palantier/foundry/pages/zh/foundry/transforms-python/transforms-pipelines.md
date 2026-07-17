---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/transforms-pipelines/",
  "title": "变换和管道",
  "page_id": "transforms-pipelines",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/python-versions/",
  "next": "/zh/foundry/transforms-python/project-structure/",
  "scraped_at": "2026-07-13T06:06:30.605096+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 变换和管道

在 Python 中，`transforms.api.Transform` 是如何计算数据集的描述。它描述了以下内容：

* 输入和输出数据集
* 用于将输入数据集变换为输出数据集的代码（我们称之为计算函数），以及
* 由 `configure()` 装饰器定义的任何额外配置（这包括在运行时使用的自定义变换配置文件）

输入和输出数据集以及变换代码被封装在一个 `Transform` Object中，然后注册到一个 `Pipeline`。您不应该手动构建一个 `Transform` Object。相反，您应该使用下面描述的装饰器之一。

需要牢记的是，数据变换可以通过[`pyspark.sql.DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html) Object以及文件来表达。对于依赖于[`DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html) Object的变换，您可以使用[transform 装饰器](#transforms-decorator)并显式调用一个方法来访问包含您的输入数据集的[`DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)，或者您可以简单地使用[DataFrame 变换装饰器](#dataframe-transform-decorator))。对于依赖于文件的变换，您可以使用[transform 装饰器](#transform-decorator)并[在您的数据集中访问文件](/zh/foundry/transforms-python/unstructured-files/)。如果您的数据变换将专门使用 Pandas 库，您可以使用[Pandas 变换装饰器](#pandas-transform-decorator)。

:::callout{theme="neutral"}
您可以在一个 Python 文件中定义多个 `Transform` Object。此外，所有变换目前都以事务类型 SNAPSHOT 运行。
:::

## 变换

### 装饰器

如果您正在编写依赖于[`DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html) Object或文件的数据变换，可以使用`transforms.api.transform()`装饰器。此装饰器接受许多`transforms.api.Input`和`transforms.api.Output`规范作为关键字参数。在 Foundry 构建过程中，这些规范将分别解析为`transforms.api.TransformInput`和`transforms.api.TransformOutput` Object。这些`TransformInput`和`TransformOutput` Object在计算函数中提供对数据集的访问。

用于输入和输出的关键字名称必须对应于包装的计算函数的参数名称。

让我们通过一个简单的示例来创建一个使用`transform()`装饰器的`Transform` Object。我们将使用一个名为`/examples/students_hair_eye_color`的小样本数据集。以下是数据集的预览：

```python
from transforms.api import transform, Input, Output

# 使用transform装饰器定义数据转换
@transform(
    hair_eye_color=Input('/examples/students_hair_eye_color'),  # 输入数据集路径
    processed=Output('/examples/hair_eye_color_processed')  # 输出数据集路径
)
def filter_hair_color(hair_eye_color, processed):
    # type: (TransformInput, TransformOutput) -> None
    # 过滤出头发颜色为棕色的数据行
    filtered_df = hair_eye_color.dataframe().filter(hair_eye_color.dataframe().hair == 'Brown')
    # 将过滤后的数据写入输出数据集
    processed.write_dataframe(filtered_df)
```

请注意，“hair\_eye\_color”的输入名称和“processed”的输出名称用作`filter_hair_color`计算函数中的参数名称。
此外，`filter_hair_color`使用`dataframe()`方法从`TransformInput`读取一个[`DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)。然后使用[`filter()` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.filter.html)（这是一个常规的PySpark函数）对`DataFrame`进行筛选。筛选后的[`DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)随后使用`write_dataframe()`方法写入名为“processed”的输出。

:::callout{theme="neutral"}
由`TransformInput`返回的[`DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)对象是常规的PySpark DataFrame。有关使用PySpark的更多信息，可以参考在线提供的[Spark Python API文档 ↗](https://spark.apache.org/docs/latest/api/python/index.html)。
:::

如果您的数据变换依赖于访问文件，而不是[`DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)对象，请参考[文件访问](/zh/foundry/transforms-python/unstructured-files/)部分。

### 多重输出

当需要将单个输入数据集拆分成多个部分时，多重输出变换非常有用。**多重输出变换仅支持** `transforms.api.transform()` **装饰器。**
回想一下`/examples/students_hair_eye_color`数据集：
我们现在可以将多个`Output`规范传递给`transform()`装饰器，以便拆分输入：

```python
from transforms.api import transform, Input, Output

@transform(
    hair_eye_color=Input('/examples/students_hair_eye_color'),
    males=Output('/examples/hair_eye_color_males'),
    females=Output('/examples/hair_eye_color_females'),
)
def brown_hair_by_sex(hair_eye_color, males, females):
    # type: (TransformInput, TransformOutput, TransformOutput) -> None
    # 过滤出头发颜色为棕色的记录
    brown_hair_df = hair_eye_color.dataframe().filter(hair_eye_color.dataframe().hair == 'Brown')
    # 将头发颜色为棕色且性别为男性的记录写入males输出
    males.write_dataframe(brown_hair_df.filter(brown_hair_df.sex == 'Male'))
    # 将头发颜色为棕色且性别为女性的记录写入females输出
    females.write_dataframe(brown_hair_df.filter(brown_hair_df.sex == 'Female'))
```

请注意，我们只需筛选一次棕色头发，然后我们可以共享筛选后的数据集以生成多个输出数据集。

### DataFrame 变换装饰器

在Python中进行数据变换时，通常会读取、处理和写入[`DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)对象。如果您的数据变换依赖于[`DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)对象，您可以使用`transforms.api.transform_df()`装饰器。此装饰器注入[`DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)对象，并期望计算函数返回一个[`DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)。
或者，您可以使用更通用的`transform()`装饰器，并显式调用`dataframe()`方法来访问包含输入数据集的[`DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)。回想一下，`transform()`装饰器注入了功能更强大的`transforms.api.TransformInput`和`transforms.api.TransformOutput`对象，而不是[`DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)对象。
`transform_df()`装饰器接受多个`transforms.api.Input`规范作为关键字参数，并接受单个`transforms.api.Output`规范作为位置参数。根据Python的要求，位置`Output`参数必须首先出现，然后是关键字`Input`参数。
让我们通过一个简单的例子来创建一个使用`transform_df()`装饰器的`Transform`对象。我们将使用上面的一个小样本数据集，名为`/examples/students_hair_eye_color`。以下是数据集的预览：

```
>>> students_input = foundry.input('/examples/students_hair_eye_color')
>>> students_input.dataframe().sort('id').show(n=3)
# 读取学生头发和眼睛颜色的数据，并按id排序后显示前3行
+---+-----+-----+----+
| id| hair|  eye| sex|
+---+-----+-----+----+
|  1|Black|Brown|Male|
|  2|Brown|Brown|Male|
|  3|  Red|Brown|Male|
+---+-----+-----+----+
only showing top 3 rows
```

现在，我们将更改上面[变换装饰器](#transforms-decorator)部分中的示例，以使用`transform_df()`装饰器。我们定义一个`变换`，以`/examples/students_hair_eye_color`作为输入，并创建`/examples/hair_eye_color_processed`作为输出：

```python
from transforms.api import transform_df, Input, Output

@transform_df(
    Output('/examples/hair_eye_color_processed'),
    hair_eye_color=Input('/examples/students_hair_eye_color')
)
def filter_hair_color(hair_eye_color):
    # type: (pyspark.sql.DataFrame) -> pyspark.sql.DataFrame
    # 过滤头发颜色为棕色的记录
    return hair_eye_color.filter(hair_eye_color.hair == 'Brown')
```

注意，“hair\_eye\_color”的输入名称被用作`filter_hair_color`计算函数中的参数名称。此外，由于Python要求位置参数要在关键字参数之前，`Output`参数出现在任何`Input`参数之前。

### Pandas变换装饰器

:::callout{theme="warning" title="警告"}
`transform_pandas`装饰器应仅用于可以放入内存的数据集。否则，您应该使用`transform_df`装饰器编写您的数据变换，并在将其转换为Pandas DataFrame之前筛选输入数据集，使用[`toPandas` ↗](https://spark.apache.org/docs/1.3.0/api/python/pyspark.sql.html#pyspark.sql.DataFrame.toPandas)方法。

我们建议在`meta.yaml`中添加PyArrow作为依赖项，并使用[`toPandas` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.toPandas.html)方法。这使得[Pandas DataFrame转换优化与Arrow ↗](https://spark.apache.org/docs/latest/api/python/user_guide/sql/arrow_pandas.html#enabling-for-conversion-to-from-pandas)成为可能。
:::

如果您的数据变换完全依赖于Pandas库，您可以使用`transforms.api.transform_pandas()`装饰器。要使用Pandas库，必须在您的`meta.yml`文件中添加`pandas`作为**运行**依赖项。有关更多信息，请参阅[描述meta.yml文件的部分](/zh/foundry/transforms-python/project-structure/#metayaml)。

`transform_pandas()`装饰器类似于`transform_df()`装饰器，但`transform_pandas()`将输入数据集转换为[`pandas.DataFrame` ↗](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)对象，并接受返回类型为[`pandas.DataFrame` ↗](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)。

`transform_pandas()`装饰器接受若干`transforms.api.Input`规范作为关键字参数，并接受一个单一的`transforms.api.Output`规范作为位置参数。根据Python的要求，位置`Output`参数必须首先出现，然后是关键字`Input`参数。

让我们通过一个简单的示例来创建一个`Transform`对象，使用`transform_pandas()`装饰器。我们将使用上面的示例数据集，名为`/examples/students_hair_eye_color`。以下是数据集的预览：
现在，我们可以定义一个`变换`，将`/examples/students_hair_eye_color`作为输入，并创建`/examples/hair_eye_color_processed`作为输出：

```python
from transforms.api import transform_pandas, Input, Output

@transform_pandas(
    Output('/examples/hair_eye_color_processed'),
    hair_eye_color=Input('/examples/students_hair_eye_color')
)
def filter_hair_color(hair_eye_color):
    # type: (pandas.DataFrame) -> pandas.DataFrame
    # 筛选头发颜色为棕色的学生记录
    return hair_eye_color[hair_eye_color['hair'] == 'Brown']
```

注意，“hair\_eye\_color”的输入名称被用作`filter_hair_color`计算函数中的参数名称。此外，由于Python要求位置参数必须在关键字参数之前，`Output`参数出现在任何`Input`参数之前。 这个示例从一个计算函数创建了一个`变换`，该函数接受和返回[`pandas.DataFrame` ↗](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)，而不是像上面[DataFrame变换装饰器](#dataframe-transform-decorator)部分中的示例那样返回[`pyspark.sql.DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)对象。请注意，您可以使用[`createDataFrame()` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.createDataFrame.html)方法将Pandas DataFrames转换为PySpark DataFrames——在您的[变换上下文](#transform-context)的`spark_session`属性上调用此方法。

### 变换上下文

在某些情况下，数据变换可能依赖于其输入数据集以外的因素。例如，可能需要变换来访问当前的Spark会话或联系外部服务。在这种情况下，您可以将一个`transforms.api.TransformContext`对象注入到变换中。

要注入一个`TransformContext`对象，您的计算函数必须接受一个名为`ctx`的参数。请注意，这也意味着没有输入或输出可以命名为`ctx`。例如，如果您想从Python数据结构创建一个[`DataFrame` ↗](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)，您可以使用一个`TransformContext`对象：

```python
from transforms.api import transform, Output

@transform(
    out=Output('/examples/context')
)
def generate_dataframe(ctx, out):
    # type: (TransformContext) -> pyspark.sql.DataFrame
    # 创建一个DataFrame，包含两列：'letter' 和 'number'
    df = ctx.spark_session.createDataFrame([
        ['a', 1], ['b', 2], ['c', 3]
    ], schema=['letter', 'number'])
    # 将DataFrame写入到指定的输出路径
    out.write_dataframe(df)
```

### 变换逻辑级别版本管理

:::callout{theme="warning" title="警告"}
为使TLLV正常工作，您的代码必须在模块级别声明所有导入，并且不应尝试修补或以其他方式修改另一个模块中的Object。如果您的项目中不是这种情况，**您必须禁用TLLV**。有关更多信息，请参阅下面的代码示例。
**TLLV默认启用。** 要禁用TLLV，请在transformsPython配置中将tllv设置为**false**。此配置位于Transforms Python子项目中的`build.gradle`文件内。

```
// 这段代码似乎是一个标记结构，不是标准的Python代码
// `transformsPython` 可能是一个自定义的标记或配置对象
// `tllv false` 可能是一个配置项，将其设置为false
transformsPython {
    tllv false
}
```
:::

变换的版本是一个字符串，用于在考虑逻辑过时时比较两个变换的版本。如果变换的输入未更改且变换的版本未更改，则变换的输出是最新的。如果版本更改，变换的输出将被作废并重新计算。

默认情况下，变换的版本包括以下内容：

* 定义变换的模块，
* 变换依赖的所有模块，以及
* 任何项目依赖项

如果其中任何一项更改，版本字符串将会更改。
如果您希望在未列出的文件部分发生更改时使输出失效，请在transformsPython配置中设置tllvFiles。示例用例是如果您正在读取文件的配置，并且希望在配置更改时使输出失效。

```
// 包含要包含在项目目录中的文件路径
transformsPython {
    tllvFiles = [
        'path/to/file/you/want/to/include/relative/to/project/directory' // 文件相对于项目目录的路径
    ]
}
```

如果您希望避免在任何项目依赖项版本更改时使输出无效，请将 tllvIncludeDeps 设置为 **false**。

```
// 设置 transformsPython 的配置，其中 tllvIncludeDeps 参数为 false
transformsPython {
    tllvIncludeDeps false // 不包括依赖项
}
```

请参考以下有效和无效导入的代码示例：

```python
# 如果你只在模块顶部导入，那么你不必担心。
from transforms.api import transform_df, Input, Output
from myproject.datasets import utils
from myproject.testing import test_mock as tmock
import importlib

# 在模块范围内使用 `importlib` 的 `__import__` 是可以的。
logging = __import__('logging')
my_compute = importlib.import_module('myproject.compute')

def helper(x):
    # 这是无效的，如果你在函数或类方法中导入，必须禁用 TLLV。
    # 所有的导入必须在模块范围内进行。
    import myproject.helpers as myhelp
    return myhelp.round(x)

@transform_df(
    Output("/path/to/output/dataset"),
    my_input=Input("/path/to/input/dataset"),
)
def my_compute_function(my_input):
    # 这是无效的，如果你想在函数中使用任何导入方式，必须禁用 TLLV！
    ihelper = __import__('myproject.init_helper')
    my_functions = importlib.import_module('myproject.functions')
    return my_input
```

### 代码说明

1. **模块范围内的导入**：在模块顶层进行导入是完全可以接受的，这样的导入在代码中并不会引发问题。
2. **`__import__` 和 `importlib`**：在模块范围内使用 `__import__` 和 `importlib.import_module` 是允许的。
3. **函数内部的导入**：在函数内部进行导入是无效的，如果需要在函数或类方法中进行导入，必须禁用 TLLV（Transform Lifecycle Limitation Verification）。
4. **代码最佳实践**：确保所有的导入语句都在模块的顶层，以避免运行时的导入错误，并提高代码的可维护性和可读性。
   如果您使用[扩展模块 ↗](https://docs.python.org/3/extending/extending.html)，必须禁用TLLV。

## 流水线

每个仓库中的Transforms Python子项目都会暴露一个`transforms.api.Pipeline`对象。这个`Pipeline`对象用于：

1. 在Foundry中注册数据集，并提供如何搭建它们的指令，
2. 在Foundry搭建过程中，定位并执行负责搭建给定数据集的`transforms.api.Transform`对象。

### 入口点

负责执行Python变换的运行时需要能够找到项目的`Pipeline`。要导出一个`Pipeline`，需要将其添加到Transforms Python子项目中的`setup.py`文件的`entry_points`参数中。有关入口点的更多信息，您可以参考[setuptools库文档 ↗](https://setuptools.readthedocs.io/en/latest/pkg_resources.html#entry-points)。
默认情况下，每个Python子项目都需要导出一个名为`root`的`transforms.pipelines`入口点。请记住，入口点是在位于Python子项目根目录的`setup.py`文件中定义的。入口点引用模块名称以及`Pipeline`属性。
例如，假设您有一个定义在`myproject/pipeline.py`中的名为“my\_pipeline”的`Pipeline`：

```python
from transforms.api import Pipeline

# 创建一个新的管道实例
my_pipeline = Pipeline()
```

您可以通过以下方式在`setup.py`中注册此`Pipeline`：

```python
import os
from setuptools import find_packages, setup

setup(
        entry_points={
        'transforms.pipelines': [
            'root = myproject.pipeline:my_pipeline'  # 在'transforms.pipelines'入口点定义一个管道，指向myproject.pipeline模块中的my_pipeline函数
        ]
    }
)
```

在上面的代码中，`root` 指代您正在导出的 `Pipeline` 的名称，`myproject.pipeline` 指代包含您 `Pipeline` 的模块，而 `my_pipeline` 指代在该模块中定义的 `Pipeline` 属性。

### 为管道添加变换

一旦与项目的 Pipeline 关联的 `Transform` 对象将数据集声明为 `Output`，您可以在 Foundry 中搭建此数据集。向 `Pipeline` 添加 `Transform` 对象的两种推荐方法是[手动注册](#manual-registration)和[自动注册](#automatic-registration)。

:::callout{theme="success" title="提示"}
如果您有更复杂的工作流程和/或想要明确地将每个 `Transform` 对象添加到项目的 Pipeline，您可以使用手动注册。否则，强烈推荐使用自动注册以确保您的注册代码简洁且集中。通过自动注册，`discover_transforms` 方法会递归地发现任何在模块级别定义的 `Transform` 对象。有关更多信息，请参阅以下部分。
:::

### 自动注册

:::callout{theme="warning" title="警告"}
`discover_transforms` 方法会导入它找到的每个模块。因此，任何在您导入的模块中的代码都会被执行。
:::

随着项目复杂度的增加，手动向 `Pipeline` 添加 `Transform` 对象可能会变得麻烦。因此，`Pipeline` 对象提供了 `discover_transforms()` 方法，用于递归地发现 Python 模块或包中的所有 `Transform` 对象。

```python
from transforms.api import Pipeline

import my_module
my_pipeline = Pipeline()  # 创建一个Pipeline对象
my_pipeline.discover_transforms(my_module)  # 从my_module中发现并注册转换
```

### 手动注册

可以使用`add_transforms()`函数将`变换`对象手动添加到`Pipeline`中。此函数接收任意数量的`变换`对象并将其添加到Pipeline中。它还会检查是否有两个`变换`对象声明相同的输出数据集。

```python
from transforms.api import transform_df, Pipeline, Input, Output

@transform_df(
    Output('/path/to/output/dataset'),  # 指定输出数据集路径
    my_input=Input('/path/to/input/dataset')  # 指定输入数据集路径
)
def my_compute_function(my_input):
    # 直接返回输入数据集，不进行任何变换
    return my_input

my_pipeline = Pipeline()
my_pipeline.add_transforms(my_compute_function)  # 将计算函数添加到管道中
```

### 变换生成

:::callout{theme="warning" title="警告"}
如果您想定义一个生成多个输出的数据变换，您可以使用变换生成或[定义一个多输出变换](#multiple-outputs)。使用变换生成时，可能需要为每个输出读取和处理一次相同的输入。而使用多输出变换时，可以只读取和处理一次输入。
:::

您可能希望在多个变换对象中重用相同的数据变换逻辑。例如，考虑以下场景：

* 您有一个包含各种状态信息的输入数据集。您有代码可以按状态筛选输入，然后计算各种统计数据。
* 您有多个可能包含空值的输入数据集。您有代码可以删除任何空值。

在这两种情况下，在多个变换中使用相同的数据变换代码是有用的。您可以使用for循环生成变换对象，然后批量将它们注册到项目的管道中，而不是为每个输出单独定义变换对象。以下是生成变换的示例：

```python
from transforms.api import transform_df, Input, Output

def transform_generator(sources):
    # type: (List[str]) -> List[transforms.api.Transform]
    transforms = []
        # 这个例子使用了多个输入数据集。你也可以从单个输入数据集中生成多个输出。
    for source in sources:
        @transform_df(
            Output('/sources/{source}/output'.format(source=source)),  # 定义输出路径
            my_input=Input('/sources/{source}/input'.format(source=source))  # 定义输入路径
        )
        def compute_function(my_input, source=source):
            # 为了在函数中捕获source变量，将其作为默认关键字参数传递。
            return my_input.filter(my_input.source == source)  # 过滤输入数据集，使其只包含匹配当前source的行
        transforms.append(compute_function)
    return transforms

TRANSFORMS = transform_generator(['src1', 'src2', 'src3'])  # 生成针对每个source的变换函数
```

:::callout{theme="warning" title="警告"}
要在函数中捕获源变量，您必须将其作为默认关键字参数 `source` 传递到您的计算函数中。
:::

:::callout{theme="warning" title="警告"}
在使用循环生成变换时，用于生成变换对象的循环必须在函数内，因为Python的for循环不会创建新作用域。如果不使用函数，自动注册将错误地只发现for循环中定义的最后一个变换对象。该函数应返回生成的变换对象的列表，并应将返回值设置为一个变量。遵循这些条件并在一个设置为通过[自动注册](#automatic-registration)发现的模块中使用，将允许您使用自动注册生成的变换。或者，您可以使用[手动注册](#manual-registration)。
:::

:::callout{theme="warning" title="警告"}
如果输入数据集的列表在搭建之间更改（例如，如果输入数据集的列表从一个在搭建之间更改的文件中读取），搭建将失败，因为在搭建的任务规范中找不到新的数据集引用。
:::

:::callout{theme="neutral"}
在变换中不可能动态命名输入或输出。当CI任务运行时，确定了所有输入和输出之间的关系，包括唯一标识符与数据集名称之间的链接。不存在的输出数据集将被创建，并在其中添加一个[JobSpec](/zh/foundry/data-integration/builds/#jobs-and-jobspecs)。

每当数据集被搭建时，从JobSpec中获取对存储库、源文件和创建数据集的函数入口点的引用。随后，启动搭建过程并调用您的函数以生成最终结果。因此，如果您的输入或输出发生更改并启动搭建过程，将导致出错，因为JobSpec不再有效。这会破坏唯一标识符与数据集名称之间的连接。
:::

如果使用手动注册，您可以将生成的变换添加到管道中。如果您不熟悉`*`语法，请参考<a href="https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists">本教程</a>。

```python
import my_module

# 创建一个新的数据处理管道
my_pipeline = Pipeline()

# 将模块中的所有转换函数添加到管道中
my_pipeline.add_transforms(*my_module.TRANSFORMS)
```

:::callout{theme="warning" title="警告"}
请注意，代码仓库中的搭建按钮可能无法用于手动注册，并且会出现*在请求的文件中未发现变换*的出错。您仍然可以使用[数据沿袭](/zh/foundry/data-lineage/overview/)或数据集预览应用程序来搭建这些数据集。
:::

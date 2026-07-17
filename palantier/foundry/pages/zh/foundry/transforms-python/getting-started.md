---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/getting-started/",
  "title": "入门指南",
  "page_id": "getting-started",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/overview/",
  "next": "/zh/foundry/transforms-python/python-versions/",
  "scraped_at": "2026-07-13T06:06:18.828095+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 入门指南

:::callout{theme="success" title="提示"}
以下说明逐步介绍了一个简单的Python数据变换。如果您刚刚开始进行数据变换，建议先通过[Pipeline Builder](/zh/foundry/building-pipelines/create-batch-pipeline-pb/)或[代码仓库](/zh/foundry/building-pipelines/create-batch-pipeline-cr/)学习批量管道教程。
:::

本教程介绍如何使用Transforms Python将最近陨石发现的电子表格变换为可用于分析的数据集。

## 关于数据集

本教程使用来自[NASA开放数据门户 ↗](https://data.nasa.gov/)的数据。您可以在自己的代码仓库中使用此示例数据集进行操作：

[`下载 meteorite_landings`](../../foundry-docs/transforms-python/media/meteorite_landings.csv)

此数据集包含在地球上发现的陨石数据。请注意，数据已被清理以便于使用。

数据集包括每颗陨石的名称、质量、分类和其他识别信息，以及其被发现的年份和发现地点的坐标。在将数据上传到Foundry之前，建议先打开CSV文件查看数据。

## 设置Python代码仓库

起始步骤是创建一个Python代码仓库。

1. 导航到一个项目，选择 **+ New > Code repository**。
2. 在**仓库类型**部分，选择**数据变换**。
3. 选择**Python**作为**语言模板**。
4. 选择**初始化仓库**。

### 使用本地Python仓库

或者，您可以通过以下步骤将本地Python仓库复制到代码仓库中：

1. 按上述步骤创建一个新的Python代码仓库。
2. 在本地仓库中，移除之前的Git源（例如，如果您是从GitHub克隆的）：`git remote remove origin`
3. 添加您的代码仓库的Git远程URL：`git remote add origin <repository_url>`

您可以在GitHub界面的右上角找到代码仓库URL。选择绿色的**Clone**按钮，然后复制Git远程URL。

通过运行`git remote -v`确认这一点，以返回代码仓库URL。

4. 将代码仓库中的当前`master`分支（或您选择的其他分支）合并到本地分支中：`git merge master`

如果出现关于`拒绝合并不相关的历史记录`的错误，请运行命令：`git merge master --allow-unrelated-histories`。这将移除与您之前的远程GitHub仓库相关联的当前Git历史记录。

此合并将把在代码仓库中进行提交和更改所需的重要文件带到您的本地仓库。

5. 创建一个新分支并命名（例如`testbranch`）：`git checkout -b testbranch`。
6. 进行更改并提交到您的分支。
7. 执行`git push`，并确认新分支出现在代码仓库界面中。验证检查是否成功。

了解更多关于代码仓库中的[本地开发](/zh/foundry/transforms-python/local-development/)。

## 编写Python数据变换

导航到您的Transforms Python仓库。默认的`examples.py`文件包含示例代码帮助您起步。首先在`src/myproject/datasets`中创建一个新文件，并将其命名为`meteor_analysis.py`以组织您的分析。确保导入所需的函数和类。定义一个变换，将`meteor_landings`数据集作为输入，并创建`meteor_landings_cleaned`作为输出：

```python
from transforms.api import transform_df, Input, Output
from pyspark.sql import functions as F

@transform_df(
    # 将此替换为您的输出数据集路径
    Output("/Users/jsmith/meteorite_landings_cleaned"),
    # 将此替换为您的输入数据集路径
    meteorite_landings=Input("/Users/jsmith/meteorite_landings"),
)
def clean(meteorite_landings):
    # <在这里添加您的数据转换逻辑>
    pass  # 使用pass作为占位符，表示此处需要实际的数据转换逻辑
```

在代码中，`transform_df` 是一个装饰器，用于将输入数据集应用到特定的清理或转换逻辑上，并输出到指定路径。`Output` 和 `Input` 都是路径参数，需要根据实际数据集的位置进行替换。
现在，假设您想将输入数据集筛选为1950年之后发生的任何“有效”流星。更新您的数据变换逻辑以按`nametype`和`year`筛选流星：

```python
def clean(meteorite_landings):
    # 过滤出“nametype”字段值为“Valid”的陨石记录
    return meteorite_landings.filter(
        meteorite_landings.nametype == 'Valid'
    ).filter(
        # 过滤出年份大于等于1950年的陨石记录
        meteorite_landings.year >= 1950
    )
```

## 搭建输出数据集

要搭建结果数据集，请提交更改并选择右上角的**搭建**。有关在代码库中搭建数据集的更多信息，请查看[创建一个简单的批处理管道](/zh/foundry/building-pipelines/create-batch-pipeline-cr/)教程。

## 添加到你的数据变换

:::callout{theme="neutral"}
使用Python变换，你可以在单个Python文件中创建多个输出数据集。
:::

假设你想进一步筛选出特定陨石类型中特别大的陨石。为此，你需要：

1. 找到每种陨石类型的平均质量，和
2. 将每个陨石的质量与其陨石类型的平均质量进行比较。

首先，在`meteor_analysis.py`中添加一个数据变换，以找到每种陨石类型的平均质量。此变换将`meteor_landings`数据集作为输入，并创建`meteorite_stats`作为输出：

```python
@transform_df(
    # output dataset name must be unique
    Output("/Users/jsmith/meteorite_stats"),
    meteorite_landings=Input("/Users/jsmith/meteorite_landings"),
)
def stats(meteorite_landings):
    # 对陨石降落数据按类别分组，并计算每个类别的平均质量
    return meteorite_landings.groupBy("class").agg(
        F.mean("mass").alias("avg_mass_per_class")  # 计算质量的平均值并命名为 avg_mass_per_class
    )
```

接下来，创建一个数据变换，将每颗陨石的质量与其陨石类型的平均质量进行比较。该变换所需的信息分布在您在本教程中迄今为止创建的`meteorite_landings`和`meteorite_stats`表中。您必须合并这两个数据集，然后筛选出质量大于平均值的陨石：

```python
# 此数据转换基于两个输入数据集
@transform_df(
    Output("/Users/jsmith/meteorite_enriched"),
    meteorite_landings=Input("/Users/jsmith/meteorite_landings"),
    meteorite_stats=Input("/Users/jsmith/meteorite_stats")
)
def enriched(meteorite_landings, meteorite_stats):
    # 将两个数据集根据"class"字段进行连接
    enriched_together = meteorite_landings.join(
        meteorite_stats, "class"
    )
    # 添加新列'greater_mass'，判断'mass'是否大于'avg_mass_per_class'
    greater_mass = enriched_together.withColumn(
        'greater_mass', (enriched_together.mass > enriched_together.avg_mass_per_class)
    )
    # 过滤出'greater_mass'为True的记录
    return greater_mass.filter("greater_mass")
```

现在，您可以通过在 Contour 中探索来进一步分析您的 `meteorite_enriched` 数据集。

## 将数据变换应用于多个输入

到目前为止，您已经创建了一个包含质量大于平均值的所有类型陨石的数据集。假设您想为每种陨石类型创建单独的数据集。使用 Transforms Python，您可以使用 for 循环对每种类型的陨石应用相同的数据变换。有关将相同数据变换应用于不同输入的更多信息，请参阅[变换生成](/zh/foundry/transforms-python/transforms-pipelines/#transform-generation)部分。

在 `src/myproject/datasets` 中创建一个新文件，并将其命名为 `meteor_class.py`。请注意，您可以继续在 `meteor_analysis.py` 文件中编写您的数据变换代码，但本教程使用新文件来分离数据变换逻辑。

要为每种陨石类型创建单独的数据集，您需要按类别筛选 `meteorite_enriched` 数据集。定义一个 `transform_generator` 函数，将相同的数据变换逻辑应用于您想要分析的每种陨石类型：

```python
from transforms.api import transform_df, Input, Output

def transform_generator(sources):
    transforms = []
    for source in sources:
        @transform_df(
            # 这将为每种陨石类型创建一个不同的输出数据集
            Output('/Users/jsmith/meteorite_{source}'.format(source=source)),
            my_input=Input('/Users/jsmith/meteorite_enriched')
        )
        # "source=source" 捕获该函数作用域中的 source 变量的值
        def filter_by_source(my_input, source=source):
            return my_input.filter(my_input["class"] == source)

        transforms.append(filter_by_source)

    return transforms
    # 这将应用上面的数据转换逻辑到提供的三种陨石类型
TRANSFORMS = transform_generator(["L6", "H5", "H4"])
```

这将创建一个变换，以筛选出我们的陨石数据集的类别。请注意，我们必须将 `source=source` 传递给 `filter_by_source` 函数，以捕获函数范围内的 `source` 参数。

:::callout{theme="success" title="提示"}
对于在 `meteor_analysis.py` 文件中创建的初始数据变换，您无需进行任何额外配置即可将变换添加到项目的管道中。这是因为默认的 Python 项目结构使用自动注册来发现 `datasets` 文件夹中的所有变换对象。

要使用自动注册将该最终变换添加到项目的管道中，您必须将生成的变换作为列表添加到一个变量中。在上面的示例中，我们使用了变量 `TRANSFORMS`。有关自动注册和变换生成器的更多信息，请参阅变换 Python 文档中的[变换生成](/zh/foundry/transforms-python/transforms-pipelines/#transform-generation)部分。
:::

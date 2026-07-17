---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/lightweight-overview/",
  "title": "概述",
  "page_id": "lightweight-overview",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/velox-overview/",
  "next": "/zh/foundry/transforms-python/lightweight-api/",
  "scraped_at": "2026-07-13T06:07:46.599746+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

轻量级变换代表了一种新的后端，用于运行您的Python数据处理管道，同时允许您使用大部分您已熟悉的[变换API](/zh/foundry/transforms-python/transforms-python-api/)。

随着单个计算机变得更强大，越来越多的数据变换可以在单个节点上运行。这意味着，对于中小型数据集，可以不依赖于分布式并行处理来执行变换。这种方法可以减少与Spark执行器分布式编排相关的开销，并使得可以使用单节点替代方案来编写数据管道，例如 [Polars ↗](https://www.pola.rs) 或 [DuckDB ↗](https://duckdb.org)。

随着我们继续扩展轻量级变换的功能，我们建议您始终将您的库升级到`foundry-transforms-lib-python`的5.400.0或类似版本，以保持最新的功能：

* [自带容器（BYOC）](/zh/foundry/transforms-python/lightweight-examples/#bring-your-own-container-workflows) 工作流
* [增量变换](/zh/foundry/transforms-python/lightweight-examples/#incremental-workflows)（在v0.556.0中添加）

## 快速开始

:::callout{theme="warning" title="兼容性"}
轻量级变换构建于容器编排基础设施之上，使用其功能时必须在您的Foundry注册中存在。
:::

此示例展示了如何在[Python变换管道](/zh/foundry/transforms-python/transforms-pipelines/)中使用轻量级变换。假设我们有以下通过`@transform_pandas`使用pandas的Spark管道：

```python
from transforms.api import transform_pandas, Input, Output

@transform_pandas(
    Output('/Project/folder/output'),
    df=Input('/Project/folder/input'),
)
def compute(df):
    # 筛选出名字以"A"开头的行，并选取"Name"和"Age"两列，最后按"Age"列进行排序
    return (
        df[df['Name'].str.startswith("A")]
            .loc[:, ['Name', 'Age']]
            .sort_values(by="Age")
    )
```

要将其转换为轻量级变换，您需要：

1. [升级您的Python代码库](/zh/foundry/code-repositories/repository-upgrades/)到最新版本。
2. 从[库选项卡](/zh/foundry/transforms-python/use-python-libraries/)安装 `foundry-transforms-lib-python`。
3. 导入并在现有装饰器上应用 `@lightweight`，如下代码片段所示：

```python
from transforms.api import transform_pandas, Input, Output, lightweight

@lightweight
@transform_pandas(
    Output('/Project/folder/output'),
    df=Input('/Project/folder/input'),
)
def compute(df):
    return (
        df[df['Name'].str.startswith("A")]  # 过滤出名字以“A”开头的行
            .loc[:, ['Name', 'Age']]  # 选择“Name”和“Age”两列
            .sort_values(by="Age")  # 按“Age”列进行排序
    )
```

移动到轻量级变换，如上所示，可以将小数据上的变换速度提高一倍。

:::callout{theme="neutral"}
如上所示，`@lightweight` 仅与 `@transform_pandas` 或仅依赖 `.pandas()` 方法的 `@transform` 管道兼容。
:::

接下来，我们可以启用我们的变换以使用Polars，以提高可扩展性。

```python
import polars as pl
from transforms.api import transform, Input, Output, lightweight

@lightweight
@transform(  # 已从 @transform_pandas 更改为 @transform
    output=Output('/Project/folder/output'),
    dataset=Input('/Project/folder/input'),
)
def compute(output, dataset):
    output.write_table(dataset
        .polars()  # 将输入数据转换为 Polars DataFrame
        .filter(pl.col('Name').str.starts_with('A'))  # 过滤掉名字不以'A'开头的记录
        .select(['Name', 'Age'])  # 选择'Name'和'Age'列
        .sort(by='Age')  # 按'Age'列排序
    )
```

这个代码片段使用了 `polars` 库对数据进行处理，并使用 `transforms` 框架进行数据输入和输出。
这个管道现在使用您所有可用的CPU核心，并配备了Polars的查询优化引擎，可以消除不必要的操作，并找到比Pandas更有效的算法来执行您的操作。

## 下一步

要了解有关轻量级变换的更多信息，请继续查看[轻量级变换API](/zh/foundry/transforms-python/lightweight-api/)文档。

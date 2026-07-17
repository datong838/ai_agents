---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/lightweight-api/",
  "title": "轻量级变换API",
  "page_id": "lightweight-api",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/lightweight-overview/",
  "next": "/zh/foundry/transforms-python/lightweight-examples/",
  "scraped_at": "2026-07-13T06:07:49.185967+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 轻量级变换API

:::callout{theme="warning"}
轻量级变换不支持执行PySpark查询。相反，查询必须使用替代API编写。
:::

Spark变换提供了强大的平台能力，特别是在数据已经本地可用时，可以跨多个节点扩展计算。然而，许多数据变换可能由单台机器管理。在单台机器足以进行数据处理的情况下，可以选择不使用Spark，从而通过使用更适合单节点应用案例的计算引擎来减少基础设施开销。

本文件描述了变换API的`@lightweight`装饰器，可以将其放置在`@transform`、`@transform_pandas`和`@external_systems`之上，以选择不使用Spark并请求更适合处理最多约1000万行数据集的基础设施。`@lightweight`还提供了与[Polars ↗](https://pola-rs.github.io/polars/py-polars/html/reference/)的一流集成，这是一个现代计算引擎，专为单节点变换优化。

实际性能取决于管道和数据的复杂性。因此，建议您比较变换在使用和不使用`@lightweight`后端时的运行时间。

:::callout{theme="natural"}
当使用轻量级后端运行时，Spark DataFrames和Spark上下文不可用。
:::

使用`@lightweight`时，许多现有的变换功能仍然可用。您可以在同一代码库中混合使用常规和轻量级变换，[预览](/zh/foundry/code-repositories/preview-transforms/)它们，并通过[Marketplace](/zh/foundry/code-repositories/marketplace-dataset-transformation/)打包和安装轻量级变换。但是，也有一些不支持的功能，您可以在[下文](#limitations-of-lightweight-transforms)中详细了解。

## API亮点

以下部分展示了轻量级变换API。要查看与不同数据处理引擎交互的API具体示例，请查看[轻量级示例](/zh/foundry/transforms-python/lightweight-examples/)。

在使用`@lightweight`之前，请确保您已执行以下必要步骤：

1. [升级您的Python代码库](/zh/foundry/code-repositories/repository-upgrades/)到最新版本。
2. 从[库选项卡](/zh/foundry/transforms-python/use-python-libraries/)安装`foundry-transforms-lib-python`。

### 资源供应

不再依赖Spark配置文件请求资源，而是在调用装饰器时可以通过`cpu_cores`和`memory_gb`或`memory_mb`关键字参数更细粒度地请求资源。默认情况下，允许的最大值为8核和32 GB内存。如需增加这些限制，请联系Palantir支持。

```python
import polars as pl
from transforms.api import transform, Input, Output, lightweight

# 使用轻量级装饰器，指定使用的CPU核数和内存量
@lightweight(cpu_cores=3.4, memory_gb=16)
# 数据转换装饰器，定义输入和输出数据集的位置
@transform(output=Output('/Project/folder/output'), dataset=Input('/Project/folder/input'))
def compute(output, dataset):
    # 使用Polars库的惰性计算模式，过滤Name列中以'A'开头的记录
    out.write_table(dataset.polars(lazy=True).filter(pl.col('Name').str.starts_with('A')))
```

这个代码使用了Polars库进行数据处理，使用了惰性计算模式以提高性能，并通过Transform API来进行数据输入输出的管理。

:::callout{theme="neutral"}
您可以通过将资源请求作为参数传递给`@lightweight()`来微调您的变换所需的资源。代码片段中的值反映了Spark变换的常用默认值。
:::

资源配置API的一个额外好处是，您现在能够以简化的方式请求GPU：

```python
import torch  # 不要忘记在你的 meta.yaml 文件中添加 pytorch 和 pytorch-gpu
import logging
from transforms.api import transform, Output, lightweight

# 使用轻量级装饰器并指定 GPU 类型为 NVIDIA_T4
@lightweight(gpu_type='NVIDIA_T4')
# 定义一个 transform 函数，输出到指定路径
@transform(out=Output('/Project/folder/output'))
def compute(out):
    # 记录当前使用的 GPU 设备名称
    logging.info(torch.cuda.get_device_name(0))
```

:::callout{theme="normal"}
以上代码片段假设您的Foundry注册配备了NVIDIA T4 GPU，并且[项目可用](/zh/foundry/resource-management/resource-queues/#use-gpus)。
:::

### 数据格式

在`@transform_pandas`上使用`@lightweight`时，您可以使用与不使用`@lightweight`时相同的API。在`@transform`上使用`@lightweight`为您的用户函数的输入和输出提供了额外的方法。

```python
@lightweight
@transform(output=Output('/Project/folder/output'), dataset=Input('/Project/folder/input'))
def compute(output, dataset):
    polars_df = dataset.polars()         # polars_df 是一个 polars.DataFrame 对象
    lazy_df = dataset.polars(lazy=True)  # 激活流模式，lazy_df 是一个 polars.LazyFrame 对象
    pandas_df = dataset.pandas()         # pandas_df 是一个 pandas.DataFrame 对象
    arrow_table = dataset.arrow()        # arrow_table 是一个 pyarrow.Table 对象
    out.write_table(lazy_df)             # 任何上述格式都可以传递给 write_table
```

请参考上面的代码片段以查看可用的数据集格式。请注意，调用`dataset.pandas()`需要在您的环境中安装Pandas。同样地，`dataset.polars(...)`需要确保Polars已可用。

### 访问文件

轻量级输入和输出也公开了众所周知的方法，例如`.filesystem()`。下面的代码片段显示[非结构化文件](/zh/foundry/transforms-python/unstructured-files/)可以像没有`@lightweight`一样处理。

```python
@lightweight
@transform(my_output=Output('/Project/folder/output'), my_input=Input('/Project/folder/input'))
def files(my_input, my_output):
    # 遍历输入目录中的每个文件
    for file in my_input.filesystem().ls():
        # 以二进制方式读取输入文件
        with my_input.filesystem().open(file.path, "rb") as f1:
            # 以二进制方式写入输出文件
            with my_output.filesystem().open(file.path, "wb") as f2:
                # 将输入文件内容读出并写入输出文件
                f2.write(f1.read())
```

### 变换生成器

轻量级变换也支持使用[变换生成器](/zh/foundry/transforms-python/transforms-pipelines/#transform-generation)。

```python
def create_transforms():
    results = []

    # 对于每个指定的大小，创建一个轻量级转换函数
    for size in [10, 20]:
        @lightweight
        @transform(
            output=Output(f"{root_folder}/demo-outputs/lightweight-polars-{size}"),  # 输出路径
            df=Input(f"{root_folder}/demo-inputs/people-{size}")  # 输入路径
        )
        def lightweight_polars(output, df):
            # 使用 Polars 库的惰性执行来处理数据，并将结果写入输出
            output.write_table(polars_implementation(df.polars(lazy=True)))
        results.append(lightweight_polars)

    return results

TRANSFORMS = create_transforms()
```

## 轻量级变换的限制

轻量级变换尚不支持以下功能：

* 某些类型的数据期望
* 建模工作流
* 媒体集

## Polars

[Polars ↗](https://pola-rs.github.io/polars/py-polars/html/reference/) 是一个现代计算引擎，针对单节点变换进行了优化。Polars 由 Rust 编写，并提供一个精简的 Python 封装，使您可以在 Python 中编写代码，同时在管道执行期间利用本地加速。

例如，这是 Palantir 用于基准测试轻量级变换的 Polars 管道：

```python
def polars_implementation(polars_df):
    polars_df = polars_df.with_columns(
        pl.col("id").cast(pl.Int64).alias("id")  # 将 "id" 列转换为 Int64 类型
    )

    reciprocated_follows = (
        polars_df
        .explode("follows")  # 将 "follows" 列进行展开操作
        .select([
            pl.col("id").alias("id1"),  # 选取 "id" 列并重命名为 "id1"
            pl.col("follows").cast(pl.Int64).alias("id2"),  # 将 "follows" 列转换为 Int64 类型并重命名为 "id2"
        ])
    )

    return (
        polars_df
        .join(
            reciprocated_follows
            .join(
                reciprocated_follows,
                left_on=["id1", "id2"],  # 进行内部连接，条件是左表的 "id1" 对应右表的 "id2"
                right_on=["id2", "id1"],  # 条件是左表的 "id2" 对应右表的 "id1"
                how="inner"
            )
            .group_by("id1")
            .agg(pl.count("id2").alias("reciprocated_follows_count")),  # 聚合操作，计算每个 "id1" 的互相关注数
            left_on="id",
            right_on="id1",
            how="left",  # 左连接，保留左表的所有行
        )
        .drop(["email", "dob", "id1", "follows"])  # 删除不需要的列
    )
```

此代码使用 `polars` 数据库库来计算互相关注的数量。首先，将 `id` 列转换为 `Int64` 类型。然后，展开 `follows` 列并选择重命名后的 `id` 和 `follows` 列。接着，通过两次内部连接来找出互相关注的用户对，并计算每个用户的互相关注数，最后返回结果并删除不需要的列。

### Polars 流模式

建议将 Polars 用作编写轻量级变换的数据处理库。在可能的情况下，我们建议以流模式使用 Polars，该模式逐块加载数据，并允许处理大于可用内存的数据集。您可以通过调用 `.polars(lazy=True)` 方法访问流模式。目前，流模式下不完全支持 UDF、诸如 `GROUP BY` 操作的聚合以及排序。

鉴于您的变换运行在由编排层管理的容器中，如果容器的内存限制被超出，容器可能会被终止。在流模式下，Polars 无法感知这一限制，并可能超出限制。如果您遇到内存不足 (OOM) 出错，请通过设置 `@lightweight(memory_gb=32)` 或其他适当的值来增加容器的内存限制。

## 下一步

在[变换 API 参考](/zh/foundry/transforms-python/transforms-python-api/)中了解更多关于轻量级 API 的信息，或在[轻量级示例](/zh/foundry/transforms-python/lightweight-examples/)中考虑一些实际案例。

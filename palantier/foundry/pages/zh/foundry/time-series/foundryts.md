---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/foundryts/",
  "title": "在 FoundryTS 中使用时间序列",
  "page_id": "foundryts",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/time-series/time-series-in-functions/",
  "next": "/zh/foundry/time-series/time-series-properties-use-case/",
  "scraped_at": "2026-07-13T06:11:40.382321+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 在 FoundryTS 中使用时间序列

FoundryTS 是一个用于对时间序列数据运行查询的 Python 库，并且它与[代码仓库](/zh/foundry/code-repositories/overview/)和[代码工作簿](/zh/foundry/code-workbook/overview/)集成。

查看[时间序列文档](/zh/foundry/time-series/time-series-overview/)以了解更多详情。

## 在代码仓库中开始

首先，确保您已经[设置了一个 Python 代码仓库](/zh/foundry/transforms-python/getting-started/#set-up-a-python-code-repository)。

使用**库**窗格将 `foundryts`、`transforms-timeseries` 和 `transforms-objects` 库添加到您的仓库中。

![您可以在库窗格中将库添加到代码仓库。](../../../images/foundry/time-series/libraries-pane.png)

然后，按照以下说明将要查询的 Object 类型导入仓库并更新项目引用：

1. 转到仓库中的**设置**选项卡。
2. 选择 **Ontology**。
3. 添加您的 Object 类型。

### 导入资源

项目引用授予 FoundryTS 访问项目外部资源的权限。本节将指导您导入位于项目外部的资源。

如果您通过时间序列属性访问系列，则必须导入以下资源：

* 支持 Object 类型的数据集

如果您通过系列 ID 或搜索查询访问系列，则必须导入以下资源：

* 时间序列同步（此资源的 RID 看起来像：ri.time-series-catalog.main.sync.<UUID>）
* 支持时间序列同步的数据集

## 在代码工作簿中开始

在代码工作簿中，通过选择右上工具栏中的**环境**，然后选择**配置环境**，将 `foundryts` 包添加到您的环境中。

在**Conda 环境**下，选择**自定义配置文件**，搜索并添加 **foundryts**。选择**更新环境**以保存更改。

![将 foundryts 包添加到您的环境中。](../../../images/foundry/time-series/add-foundryts-package.png)

了解更多关于代码工作簿中的[环境配置](/zh/foundry/code-workbook/environment-overview/)。

### 设置工作簿输入

任何查询的 Object 类型（通过时间序列属性访问）或时间序列目录同步（通过系列 ID 或搜索查询访问）必须从左侧**内容**面板添加为工作簿输入。

![将工作簿输入添加到代码工作簿。](../../../images/foundry/time-series/add-workbook-inputs.png)

作为工作簿输入添加的 Object 类型或时间序列目录同步还必须导入到与工作簿相同的项目中，包括它们的支持数据集。如果不这样做，在使用 foundryts 编写变换时会出错。如果任何工作簿输入不在项目范围内，它们将在工作簿工具栏右上角的设置下拉菜单中的**项目范围设置**对话框中显示。

![项目范围设置对话框中显示的项目缺少工作簿输入。](../../../images/foundry/time-series/workbook-inputs-psj.png)

## 示例：股票数据

在此示例中，我们从具有 `Ticker name` 属性的 `Stock series` Object 类型开始。我们的目标是找到 `Technology` 部门中的所有系列并计算它们的时间范围。

首先定义变换的输入和输出。我们将 `Stock series` Object 类型声明为一个 Object 输入，将时间序列同步声明为一个时间序列输入。

```python
@transform(
    # 定义输出路径为 "/Users/jdoe/foundryts-test-technology-sector"
    output=Output("/Users/jdoe/foundryts-test-technology-sector"),

    # 定义时间序列输入，使用指定的时间序列资源ID
    ts=TimeSeriesInput('ri.time-series-catalog.main.sync.6bdbda27-29...'),

    # 定义对象输入，包括对象类型资源ID、本体资源ID和本体分支资源ID
    objects=ObjectInput(
        object_type_rid='ri.ontology.main.object-type.4168ed49-00...',
        ontology_rid='ri.ontology.main.ontology.00000000-00...',
        ontology_branch_rid='ri.ontology.main.branch.00000000-00...'
    )
)
```

现在，我们定义变换函数并初始化FoundryTS的实例。请注意，此函数以Object类型、时间序列同步和输出作为参数。

```python
def compute(ctx, ts, objects, output):
    # 实例化一个FoundryTS对象
    fts = FoundryTS()
```

接下来，我们在`Technology`领域中搜索`timeseries-demo-stock-series`对象。对于每个搜索结果，我们将该系列映射到其时间范围（最早和最新点的时间戳）。

```python
    search_result = fts.search.series(
        (ontology('sector') == 'Technology'),  # 使用本体过滤出行业为“技术”的数据
        object_types=['timeseries-demo-stock-series']  # 指定对象类型为“timeseries-demo-stock-series”
    ).map(F.time_extent())  # 映射时间范围
```

最后，我们将数据框写入我们的输出数据集。

```python
    df = search_result.to_dataframe()  # 将搜索结果转换为DataFrame
    output.write_dataframe(df)         # 将DataFrame写入输出
```

将所有内容整合在一起，完整的变换如下所示：

```python
from transforms.api import transform, Output
from transforms.timeseries import TimeSeriesInput
from foundryts import FoundryTS
from foundryts.search import ontology
import foundryts.functions as F
from transforms.objects import ObjectInput

# 定义数据转换函数
@transform(
    output=Output("/Users/jdoe/foundryts-test-technology-sector"),  # 输出路径
    ts=TimeSeriesInput('ri.time-series-catalog.main.sync.6bdbda27-29...'),  # 输入时间序列数据
    objects=ObjectInput(
        object_type_rid='ri.ontology.main.object-type.4168ed49-00...',  # 对象类型资源ID
        ontology_rid='ri.ontology.main.ontology.00000000-00...',  # 本体资源ID
        ontology_branch_rid='ri.ontology.main.branch.00000000-00...'  # 本体分支资源ID
    )
)
def compute(ctx, ts, objects, output):
    fts = FoundryTS()  # 创建FoundryTS实例

    # 搜索技术行业的时间序列数据
    search_result = fts.search.series(
        (ontology('sector') == 'Technology'),  # 条件：行业为“Technology”
        object_types=['timeseries-demo-stock-series']  # 对象类型为“timeseries-demo-stock-series”
    ).map(F.time_extent())  # 获取时间范围

    df = search_result.to_dataframe()  # 将搜索结果转换为DataFrame
    output.write_dataframe(df)  # 写入输出
```

输出数据集如下所示：

![运行FoundryTS变换后的数据集输出。](../../../images/foundry/time-series/output-dataset.png)

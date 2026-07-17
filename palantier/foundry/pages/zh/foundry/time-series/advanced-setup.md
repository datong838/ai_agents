---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/advanced-setup/",
  "title": "高级设置",
  "page_id": "advanced-setup",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/time-series/time-series-permissions/",
  "next": "/zh/foundry/time-series/derived-series-overview/",
  "scraped_at": "2026-07-13T06:10:06.875475+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 高级设置

:::callout{theme="warning"}
我们建议按照[时间序列设置](/zh/foundry/time-series/time-series-setup/)页面中的说明，使用[Pipeline Builder](/zh/foundry/pipeline-builder/overview/)搭建您的时间序列管道。这样做将自动应用下面描述的变换优化。

在进行高级设置配置之前，请联系您的Palantir代表。
:::

如果您需要低级变换控制或Pipeline Builder尚未提供的高级功能，本页将描述如何使用[代码库](/zh/foundry/code-repositories/overview/)手动设置您的时间序列管道以进行数据变换。

使用代码库设置时间序列，您必须完成以下步骤：

1. [创建时间序列数据集](#1-create-and-optimize-the-time-series-input-data)。
2. [优化时间序列数据集](#1-create-and-optimize-the-time-series-input-data)。
3. [手动设置时间序列同步](#2-set-up-a-time-series-sync)。
4. [创建时间序列对象类型支持数据集](#3-create-the-time-series-object-type-backing-dataset)。
5. [设置时间序列对象类型](#4-set-up-the-time-series-object-type)。

## 1. 创建时间序列数据集

当您使用[Pipeline Builder](/zh/foundry/pipeline-builder/outputs-overview/)的时间序列输出创建时间序列同步时，时间序列数据集会自动生成，并且时间序列数据集和同步都会为您正确配置。当您手动设置管道时，必须明确生成包含您格式化的[时间序列](/zh/foundry/time-series/time-series-concepts-glossary/#time-series)数据的时间序列数据集，这是创建时间序列同步所必需的。数据集必须包含**Series ID**、**Value**和**Timestamp**列，如[术语表](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-sync)中所指定，以便它们可以在时间序列同步中映射。

一个系列ID的所有值应包含在同一数据集中。由于值是通过其系列ID获取的，单个时间序列数据集可以包含多个系列ID的所有值。例如：

```
+------------------------+---------------------+---------+
| series_id              | timestamp           | value   |
+------------------------+---------------------+---------+
| Machine123_temperature | 01/01/2023 12:00:00 | 100     |  // 机器123的温度在2023年1月1日12:00:00的读数为100
| Machine123_temperature | 01/01/2023 12:01:00 | 99      |  // 机器123的温度在2023年1月1日12:01:00的读数为99
| Machine123_temperature | 01/01/2023 12:02:00 | 101     |  // 机器123的温度在2023年1月1日12:02:00的读数为101
| Machine463_temperature | 01/01/2023 12:00:00 | 105     |  // 机器463的温度在2023年1月1日12:00:00的读数为105
| Machine123_pressure    | 01/01/2023 12:00:00 | 3       |  // 机器123的压力在2023年1月1日12:00:00的读数为3
| ...                    | ...                 | ...     |  // 省略其他数据
+------------------------+---------------------+---------+
```

时间序列数据集通常配置为在有实时数据时进行[增量](/zh/foundry/transforms-python/incremental-overview/)搭建。增量搭建可以节省计算成本，并在原始数据被摄取到最新数据可读取之间实现更短的延迟。

:::callout{theme="neutral"}
有关增量时间序列搭建的更多优点，请参阅[常见问题文档](/zh/foundry/time-series/faqs/#why-is-my-time-series-taking-a-long-time-to-load)。
:::

## 2. 优化时间序列数据集

在代码中生成时间序列数据集时，请在写入之前按如下方式格式化数据集：

### Python

```python
from transforms.api import transform, Input, Output

@transform(
    output_dataset=Output("/path/to/output/dataset"),
    input_dataset=Input("/path/to/input/dataset")
)
def my_compute_function(output_dataset, input_dataset):
    # 读取输入数据集并转换为DataFrame
    output_dataframe = (
        input_dataset
        .dataframe()
        # 按照'seriesId'字段对数据进行分区
        .repartitionByRange('seriesId')
        # 在每个分区内按照'seriesId'和'timestamp'排序
        .sortWithinPartitions('seriesId', 'timestamp')
    )

    # 将输出的DataFrame写入指定格式的输出数据集
    output_dataset.write_dataframe(output_dataframe, output_format='soho')
```

### Java

```java
package myproject.datasets;

import com.palantir.transforms.lang.java.api.Compute;
import com.palantir.transforms.lang.java.api.FoundryInput;
import com.palantir.transforms.lang.java.api.FoundryOutput;
import com.palantir.transforms.lang.java.api.Input;
import com.palantir.transforms.lang.java.api.Output;
import com.palantir.foundry.spark.api.DatasetFormatSettings;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;

import java.util.Collections;

public final class TimeSeriesWriter {
    @Compute
    public void writePartitioned(
            @Input("/path/to/input/dataset") FoundryInput inputDataset, // 输入数据集路径
            @Output("/path/to/output/dataset") FoundryOutput outputDataset) { // 输出数据集路径
        Dataset<Row> inputDataframe = inputDataset.asDataFrame().read(); // 读取输入数据集到DataFrame

        Dataset<Row> outputDataframe = inputDataframe
            .repartitionByRange(inputDataframe.col('seriesId')) // 通过seriesId列进行范围分区
            .sortWithinPartitions('seriesId', 'timestamp'); // 在分区内根据seriesId和timestamp排序

        outputDataset.getDataFrameWriter(outputDataframe)
            .setFormatSettings(DatasetFormatSettings.builder()
                .format('soho') // 设置数据集格式为'soho'
                .build())
            .write(); // 写入输出数据集
    }
}
```

在这段代码中，我们定义了一个名为 `TimeSeriesWriter` 的 Java 类，用于处理时间序列数据集的分区和排序。通过 Spark 的 DataFrame API，我们首先读取输入数据集，然后根据 `seriesId` 列对数据集进行范围分区，并在每个分区内依据 `seriesId` 和 `timestamp` 进行排序。最终，我们将处理好的数据集写入到指定的输出路径，并设置数据格式为 `soho`。
运行此重新分区和排序将优化您的数据集，以便作为时间序列高效使用。至少，您的数据集还应按\_Soho\_格式化（如所示），以便在[尚未投影](/zh/foundry/optimizing-pipelines/projections-advanced/#projection-builds)时，新数据能够索引到时间序列数据库中。您还应根据以下指南，为您的管道配置由[`repartitionByRange()` ↗](https://spark.apache.org/docs/3.1.1/api/python/reference/api/pyspark.sql.DataFrame.repartitionByRange.html)写入的分区数量：

* 尽量写入尽可能少的分区。
* 分区应大于128 MB。
* 一般来说，分区应少于50亿行。

:::callout{theme="neutral"}
您可以写入的最少分区数量的限制是由写入足够小的分区来决定的，这些分区适合[执行器](/zh/foundry/optimizing-pipelines/spark-concepts/)，但分区数量足够多以使您的任务能够充分并行化，达到所需的管道延迟。写入更多分区会导致分区较小且任务更快，但不如较大分区那样最优。
:::

## 3. 手动设置时间序列同步

要创建新的时间序列同步，直接导航到`https://<domain>/workspace/time-series-catalog-app/new`。系统会提示您选择保存同步的位置，该位置必须位于包含您的时间序列数据集的[项目](/zh/foundry/projects/overview/)中或将其作为引用导入。

![时间序列同步列字段](../../../images/foundry/time-series/time-series-setup-time-series-sync-column-mapping.png)

选择您的时间序列数据集作为输入，然后完成将数据集列映射到时间序列同步的**系列ID**、**值**和**时间戳**。如果您的**时间戳**列是`Long`类型，请指定它是`SECONDS`、`MILLISECONDS`、`MICROSECONDS`还是`NANOSECONDS`单位。

当时间序列同步构建时，它会同步时间序列数据集的元数据，使Foundry能够按需索引您的时间序列数据到其时间序列数据库中。

### 使用受限视图支持的对象类型

[受限视图](/zh/foundry/security/restricted-views/)将数据集访问限制为用户有权限查看的行。当使用受限视图支持的对象类型时，您必须配置您的时间序列同步以停止继承[权限标记](/zh/foundry/security/markings/)。

![管理权限标记](/resources/foundry/time-series/time-series-advanced-setup-manage-markings.png)

通过选择权限标记旁的**停止继承**来停止继承时间序列数据集上的每个权限标记。

完成后，选择页面顶部的**保存**。

### 高级时间序列同步配置

![高级时间序列同步选项](/resources/foundry/time-series/time-series-advanced-setup-sync-advanced.png)

虽然可以为时间序列同步构建配置[Spark配置文件](/zh/foundry/code-repositories/spark-profiles/)，但这很少是必要的。

默认情况下，当输入时间序列数据集更新时，同步将计划运行。我们建议使用此设置以确保您的时间序列数据保持最新。

如果您在另一个时间序列同步中写入了相交的系列ID，并希望用新的同步替换该同步，您可以在**显示高级选项** > **覆盖其他数据集支持的其他同步中的系列**中指定旧同步。这样做会导致旧同步失败，然后应将其移至回收站。

## 4. 创建时间序列对象类型支持的数据集

您可以通过首选的方法生成时间序列对象类型支持的数据集，并且它应符合[术语表](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-object-type-backing-dataset)中指定的模式。

要自动生成时间序列对象类型支持的数据集，您可以在与时间序列数据集相同的变换中生成它，您可以在其中获取系列ID的不同集合并从中提取/映射元数据。在增量管道中，您可以使用[合并和追加](/zh/foundry/transforms-python/incremental-examples/#merge-and-append)模式来实现这一点。

## 5. 设置时间序列对象类型

按照[标准流程](/zh/foundry/object-link-types/create-object-type/)在您的时间序列对象类型支持的数据集上创建对象类型。还可以通过在[数据集预览](/zh/foundry/dataset-preview/overview/)中选择**所有操作** > **创建对象类型**，直接从数据集中生成对象类型。创建对象类型时，通过指定哪些属性应为[时间序列属性](/zh/foundry/time-series/time-series-properties/)来配置它以用于时间序列。

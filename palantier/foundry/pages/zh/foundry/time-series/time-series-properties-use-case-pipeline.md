---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/time-series-properties-use-case-pipeline/",
  "title": "使用Pipeline Builder创建时间序列数据",
  "page_id": "time-series-properties-use-case-pipeline",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/time-series/time-series-properties-use-case/",
  "next": "/zh/foundry/time-series/time-series-properties-use-case-ontology/",
  "scraped_at": "2026-07-13T06:12:43.057269+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 使用Pipeline Builder创建时间序列数据

您将使用本指南创建的管道将生成支持[时间序列同步](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-sync)的[时间序列数据](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-object-type-backing-dataset)，用于与`Carrier`、`Route`和`Airport`对象类型上的[时间序列属性](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-property-tsp)相关联，以创建新的[时间序列对象](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-object-type)。此管道涉及比标准从时间序列数据集到时间序列属性的映射更复杂的设置，因为我们将对非时间序列数据进行计算以生成时间序列数据。请查看我们的[Pipeline Builder文档](/zh/foundry/pipeline-builder/overview/)以获取有关常规管道指导的信息。

我们正在处理的航班数据集包括以下用于创建时间序列属性的列：

* **flight\_id:** `字符串` | 用于标识航班和数据集中每一行的唯一字符串。
* **date:** `date` | 航班发生的日期。
* **destination\_airport\_id:** `字符串` | 用于标识目的地机场的字符串。
* **airline\_id:** `字符串` | 航空承运人的ID。
* **origin\_airport\_id:** `字符串` | 始发机场的ID。
* **dep\_delay:** `integer` | 起飞延误的分钟数。
* **arr\_delay:** `integer` | 到达延误的分钟数。
* **route\_id:** `字符串`| 用于标识航线的唯一字符串。

本指南末尾的管道将如下所示：

![最终时间序列管道概览](../../../images/foundry/time-series/time-series-properties-pipeline-final-output.png)

## 第一部分：生成时间序列数据

使用用于支持`Flights`对象类型的相同航班数据集，我们可以执行一些聚合变换并基于航班指标生成时间序列数据。请注意，如果您已经有时间序列数据从历史记录器或边缘传感器进入Foundry，则此步骤不是必需的。您可以继续[生成时间序列同步](#part-ii-create-the-time-series-sync)。

### 1. 对`Carrier`和`Route`对象类型应用变换

从航班数据集中，按照以下步骤应用变换。您将对`Carrier`和`Route`对象类型都执行此操作。

#### 聚合数据

使用聚合变换按日期和对象的ID进行分组（在这种情况下，使用`Route`对象类型的`route_id`；您需要单独使用`airline_id`对`Carrier`对象类型进行相同操作），并计算平均到达延误、平均起飞延误和每日航班计数。

![Pipeline Builder中的聚合变换面板](../../../images/foundry/time-series/time-series-properties-pipeline-aggregate.png)

聚合后，数据集应以以下模式预览：

| route\_id   | date       | daily\_avg\_dep\_delay | daily\_avg\_arr\_delay | daily\_count\_of\_flights |
| --------   | ---------- | ------------------- | ------------------- | ---------------------- |
| ATL -> SFO | 2023-06-12 | 33.4545454545450000 | 40.0000000000000000 | 11                     |
| ATL -> FLL | 2023-08-24 | 29.7272727272720000 | 19.4090909090909100 | 22                     |
| ATL -> TVC | 2023-07-05 | -8.0000000000000000 | -8.0000000000000000 | 1                      |

#### 转换为新数据类型

要将此新数据用作时间序列，我们必须创建一个时间戳类型的列。为此，使用转换变换将`date`列转换为时间戳类型的列。我们还将很快应用一个反透视变换来合并`daily_avg_dep_delay`、`daily_avg_arr_delay`和`daily_count_of_flights`值为一个列。由于此函数要求所有值为相同的数据类型，因此我们还必须将我们的每日航班计数指标转换为双精度类型（与平均延误指标的数据类型相同）。

![Pipeline Builder中的转换面板，显示了转换为时间戳和转换为双精度](../../../images/foundry/time-series/time-series-properties-cast-to-new-datatype.png)

#### 反透视以合并时间序列值

由于此数据集中包含不同列中的时间序列数据，我们必须使用反透视变换将其合并为一个值列，以便数据可以匹配时间序列同步所需的模式，如下所示：

* **系列ID:** `字符串` | TSP所引用的时间戳和值对集合的系列ID，必须与TSP的系列ID匹配。
* **时间戳:** `timestamp`或`long` | 测量数量的时间。
* **值:** `integer`、`float`、`double`、`字符串` | 在测量点的数量值。字符串类型表示分类时间序列；每个分类时间序列最多可以有10,000个唯一变体。

下面显示的反透视变换将`daily_avg_dep_delay`、`daily_avg_arr_delay`和`daily_count_of_flights`的值放入同一个`series_value`列中。那些原始列名输出到将在系列ID中使用的新`series_name`列中。

![Pipeline Builder中的反透视变换面板](../../../images/foundry/time-series/time-series-properties-pipeline-unpivot.png)

数据集的模式现在应如下所示：

| series\_name            | series\_value        | route\_id   | date                     |
| ---------------------- | ------------------- | ---------- | ------------------------ |
| daily\_avg\_dep\_delay    | 33.4545454545450000 | ATL -> SFO | 2023-06-12T00:00:00.000Z |
| daily\_avg\_arr\_delay    | 40.0000000000000000 | ATL -> SFO | 2023-06-12T00:00:00.000Z |
| daily\_count\_of\_flights | 11.0000000000000000 | ATL -> SFO | 2023-06-12T00:00:00.000Z |

#### 拼接字符串值以创建系列ID

现在，我们可以使用拼接字符串变换来创建系列ID（关联时间序列值的标识符）。使用变换将`series_name`（每个传感器代表的内容）与每个对象的主键结合起来。

![Pipeline Builder中的拼接字符串变换面板](../../../images/foundry/time-series/time-series-properties-pipeline-series-id.png)

| series\_id                        | series\_name            | series\_value        | route\_id   | date                     |
| -------------------------------- | ---------------------- | ------------------- | ---------- | ------------------------ |
| CMH -> IAH\_daily\_avg\_dep\_delay   | daily\_avg\_dep\_delay    | 33.4545454545450000 | ATL -> SFO | 2023-06-12T00:00:00.000Z |
| CMH -> IAH\_daily\_avg\_arr\_delay   | daily\_avg\_arr\_delay    | 40.0000000000000000 | ATL -> SFO | 2023-06-12T00:00:00.000Z |
| CMH -> IAH\_daily\_count\_of\_flights| daily\_count\_of\_flights | 11.0000000000000000 | ATL -> SFO | 2023-06-12T00:00:00.000Z |

#### 选择必要的列

使用选择列变换，我们将只保留时间序列同步所需的列：`series_id`、`series_value`和`date`。航班支持数据集将持有所有系列的时间序列值，无论它们测量的是什么。为`airline_carrier_id`列（来自航班数据集）重复此操作。

![Pipeline Builder中的选择列变换面板](../../../images/foundry/time-series/time-series-properties-pipeline-select-columns.png)

| series\_id                        | series\_value        | date                     |
| -------------------------------- | ------------------- | ------------------------ |
| CMH -> IAH\_daily\_avg\_dep\_delay   | 33.4545454545450000 | 2023-06-12T00:00:00.000Z |
| CMH -> IAH\_daily\_avg\_arr\_delay   | 40.0000000000000000 | 2023-06-12T00:00:00.000Z |
| CMH -> IAH\_daily\_count\_of\_flights| 11.0000000000000000 | 2023-06-12T00:00:00.000Z |

### 2. 添加变换以聚合和生成始发和目的地机场的数据

现在，您必须为始发机场和目的地机场重复聚合和转换变换步骤。

#### 聚合每日每条航线的航班数量

使用聚合变换按`date`和`origin_airport_id`进行分组，然后计算平均到达和起飞时间。每组中的总行数等于每日每条航线的航班数量。

![Pipeline Builder中的聚合变换面板，用于聚合每日航班数量](../../../images/foundry/time-series/time-series-properties-pipeline-aggregate-origin-airport.png)

| date       | origin\_airport\_id | daily\_avg\_dep\_delay | daily\_count\_of\_departing\_flights |
| ---------- | ----------------- | ------------------- | -------------------------------- |
| 2023-07-02 | 10299             | 9.34375000000000000 | 33                               |
| 2023-09-06 | 10431             | -2.3333333333333333 | 6                                |
| 2023-01-12 | 10620             | -7.0000000000000000 | 2                                |

#### 转换为时间戳

要将此新数据用作时间序列，我们必须创建一个时间戳列。为此，使用转换变换将`date`列转换为时间戳类型的列。

![Pipeline Builder中的转换变换面板，用于将数据转换为时间戳类型](../../../images/foundry/time-series/time-series-properties-cast-to-timestamp.png)

### 3. 创建合并始发和目的地机场的合并

使用合并面板，创建一个左合并，将目的地机场和始发机场的数据合并，结果是完整的机场数据时间序列属性。确保为您的合并设置以下配置：

* 匹配日期和`origin_airport_id`到`dest_airport_id`。
* 自动选择左侧数据集的列。
* 作为右侧列，选择代表日均延误和每日航班计数的两列。

![Pipeline Builder中的合并面板，配置为创建机场数据的左合并。](../../../images/foundry/time-series/time-series-properties-pipeline-join.png)

| date       | origin\_airport\_id | daily\_avg\_dep\_delay | daily\_count\_of\_departing\_flights | daily\_avg\_arr\_delay | daily\_count\_of\_arriving\_flights |
| ---------- | ----------------- | ------------------- | -------------------------------- | ------------------- | ------------------------------- |
| 2023-07-02 | 10299             | 9.34375000000000000 | 33                               | 18.5294117647058840 | 34                              |
| 2023-09-06 | 10431             | -2.3333333333333333 | 6                                | -8.0000000000000000 | 6                               |
| 2023-01-12 | 10620             | -7.0000000000000000 | 2                                | 56.5000000000000000 | 2                               |

### 4. 应用变换以格式化数据以进行时间序列同步

#### 重命名列

现在我们已将始发机场数据与目的地机场数据合并，我们拥有了所有机场的到达和起飞指标。我们不再需要区分始发和目的地，因此我们可以使用重命名列变换将`origin_airport_id`更改为简单的`airport_id`。

![Pipeline Builder中的重命名列变换面板](../../../images/foundry/time-series/time-series-properties-pipeline-rename-column.png)

数据应以重命名的列如下预览：

| date       | airport\_id | daily\_avg\_dep\_delay | daily\_count\_of\_departing\_flights | daily\_avg\_arr\_delay | daily\_count\_of\_arriving\_flights |
| ---------- | ---------- | ------------------- | -------------------------------- | ------------------- | ------------------------------- |
| 2023-07-02 | 10299      | 9.34375000000000000 | 33                               | 18.5294117647058840 | 34                              |
| 2023-09-06 | 10431      | -2.3333333333333333 | 6                                | -8.0000000000000000 | 6                               |
| 2023-01-12 | 10620      | -7.0000000000000000 | 2                                | 56.5000000000000000 | 2                               |

#### 转换为双精度

我们将很快应用一个反透视变换。此函数要求所有值为相同的数据类型，因此我们必须再次使用转换面板将我们的每日航班计数指标转换为双精度数据类型，以便它们与平均延误指标的数据类型相同。

#### 添加航班数量

要计算完整的每日航班计数，我们将使用加法变换将每日到达航班计数和每日起飞航班计数相加，如下所示。

![Pipeline Builder中的转换和加法变换面板](../../../images/foundry/time-series/time-series-properties-pipeline-cast-tsps.png)

| daily\_count\_of\_flights | date       | airport\_id | daily\_avg\_dep\_delay | daily\_count\_of\_departing\_flights | daily\_avg\_arr\_delay | daily\_count\_of\_arriving\_flights |
| ---------------------- | ---------- | ---------- | ------------------- | -------------------------------- | ------------------- | ------------------------------- |
| 77                     | 2023-07-02 | 10299      | 9.34375000000000000 | 33                               | 18.5294117647058840 | 34                              |
| 12                     | 2023-09-06 | 10431      | -2.3333333333333333 | 6                                | -8.0000000000000000 | 6                               |
| 4                      | 2023-01-12 | 10620      | -7.0000000000000000 | 2                                | 56.5000000000000000 | 2                               |

#### 反透视以合并系列值

由于此数据集中包含不同列中的时间序列数据，我们必须使用反透视变换将其合并为一个值列，以便数据可以匹配时间序列同步所需的模式，如下所示：

* **系列ID:** `字符串` | TSP所引用的时间戳和值对集合的系列ID，必须与TSP的系列ID匹配。
* **时间戳:** `timestamp`或`long` | 测量数量的时间。
* **值:** `integer`、`float`、`double`、`字符串` | 在测量点的数量值。字符串类型表示分类时间序列；每个分类时间序列最多可以有10,000个唯一变体。

下面显示的反透视变换将`daily_avg_dep_delay`、`daily_avg_arr_delay`和`daily_count_of_flights`的值放入同一个`series_value`列中。那些原始列名输出到将在系列ID中使用的新`series_name`列中。

![Pipeline Builder中的反透视变换面板，配置为创建series\_name列输出](../../../images/foundry/time-series/time-series-properties-pipeline-unpivot-merge-series.png)

数据应以以下模式进行预览：

| series\_name                      | series\_value        | date                     | airport\_id |
| -------------------------------- | ------------------- | ------------------------ | ---------- |
| daily\_count\_of\_flights           | 77                  | 2023-07-02T00:00:00.000Z | 10299      |
| daily\_avg\_dep\_delay              | 9.34375000000000000 | 2023-07-02T00:00:00.000Z | 10299      |
| daily\_avg\_arr\_delay              | 18.5294117647058840 | 2023-07-02T00:00:00.000Z | 10299      |

#### 拼接字符串值以创建系列ID

现在，我们可以使用拼接字符串变换来创建系列ID（关联时间序列值的标识符）。使用变换将`series_name`（每个传感器代表的内容）与`Airport`对象的主键（`airport_id`）结合起来。

![Pipeline Builder中的拼接字符串面板，配置为将series\_name与airport\_id结合](../../../images/foundry/time-series/time-series-properties-pipeline-create-series-id.png)

| series\_id                    | series\_name                      | series\_value        | date                     | airport\_id |
| ---------------------------- | -------------------------------- | ------------------- | ------------------------ | ---------- |
| 12099\_daily\_count\_of\_flights | daily\_count\_of\_flights           | 77                  | 2023-07-02T00:00:00.000Z | 10299      |
| 12099\_daily\_avg\_dep\_delay    | daily\_avg\_dep\_delay              | 9.34375000000000000 | 2023-07-02T00:00:00.000Z | 10299      |
| 12099\_daily\_avg\_arr\_delay    | daily\_avg\_arr\_delay              | 18.5294117647058840 | 2023-07-02T00:00:00.000Z | 10299      |

#### 选择必要的列

使用选择列变换，我们将只保留时间序列同步所需的列：`series_id`、`series_value`和`date`。航班支持数据集将持有所有系列的时间序列值，无论它们测量的是什么。

![Pipeline Builder中的选择列面板](../../../images/foundry/time-series/time-series-properties-pipeline-select-sync-column.png)

结果数据集应如下所示：

| series\_id                    | series\_value        | date                     |
| ---------------------------- | ------------------- | ------------------------ |
| 12099\_daily\_count\_of\_flights | 77                  | 2023-07-02T00:00:00.000Z |
| 12099\_daily\_avg\_dep\_delay    | 9.34375000000000000 | 2023-07-02T00:00:00.000Z |
| 12099\_daily\_avg\_arr\_delay    | 18.5294117647058840 | 2023-07-02T00:00:00.000Z |

### 5. 将时间序列属性合并到支持数据集中

创建一个类型为`按名称合并`的合并，使用代表`Carrier`、`Route`和`Airport`时间序列属性的变换。

![Pipeline Builder图中选择用于合并的三个时间序列属性节点](../../../images/foundry/time-series/time-series-properties-pipeline-union-graph.png)

![Pipeline Builder中的合并面板，配置为按名称合并三个TSP属性集](../../../images/foundry/time-series/time-series-properties-pipeline-union-by-name.png)

| series\_id                      | series\_value        | date                     |
| ------------------------------ | ------------------- | ------------------------ |
| 12099\_daily\_count\_of\_flights   | 77                  | 2023-07-02T00:00:00.000Z |
| 12099\_daily\_avg\_dep\_delay      | 9.34375000000000000 | 2023-07-02T00:00:00.000Z |
| 12099\_daily\_avg\_arr\_delay      | 18.5294117647058840 | 2023-07-02T00:00:00.000Z |
| CMH -> IAH\_daily\_avg\_dep\_delay | -8.0000000000000000 | 2023-03-21T00:00:00.000Z |
| 20304\_daily\_avg\_arr\_delay      | 9.12500000000000000 | 2023-08-13T00:00:00.000Z |

## 第二部分：创建时间序列同步

### 1. 删除空值

在结果数据集上应用筛选变换以删除任何`null`值。

![Pipeline Builder中的筛选变换面板，配置为删除空值。](../../../images/foundry/time-series/time-series-properties-pipeline-remove-null-values.png)

### 2. 配置时间序列同步

现在，通过从屏幕右侧的管道输出部分选择**添加**来创建[时间序列同步](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-sync)。然后，选择**时间序列同步**。填写新时间序列同步的必要数据，并考虑以下事项：

* 标题“\[示例] 时间序列同步 | 事件”将对应于您的Palantir文件系统文件夹中的结果资源。
* 为[**系列ID**](/zh/foundry/time-series/time-series-concepts-glossary/#series-id)字段选择`series_id`列。
* 在**时间**字段中添加创建的`date`时间戳列。
* 将`series_value`添加到**值**字段中。

现在，[保存并搭建](/zh/foundry/pipeline-builder/outputs-deliver-pipeline/#save)管道。输出将创建在与管道相同的文件夹中。

### 3. 使用时间序列同步向对象类型添加属性

现在您已创建具有时间序列同步的管道，您已准备好使用同步将时间序列属性添加到`Route`、`Carrier`和`Airport`对象类型。继续查看我们的文档以获取有关[将时间序列属性添加到对象类型](/zh/foundry/time-series/time-series-properties-use-case-ontology/)的更多指导。

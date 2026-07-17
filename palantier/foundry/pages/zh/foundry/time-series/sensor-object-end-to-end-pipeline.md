---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/sensor-object-end-to-end-pipeline/",
  "title": "在Pipeline Builder中创建传感器对象类型数据",
  "page_id": "sensor-object-end-to-end-pipeline",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/time-series/sensor-object-end-to-end/",
  "next": "/zh/foundry/time-series/sensor-object-end-to-end-ontology/",
  "scraped_at": "2026-07-13T06:13:33.330935+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 在Pipeline Builder中创建传感器对象类型数据

使用本指南创建的管道将对导入的飞行传感器读数数据集进行变换，以创建传感器对象类型的支持数据集，然后将传感器读数转换为时间序列格式，以创建时间序列同步输出。然后将这些数据用于在平台中创建传感器对象类型。最终管道的样子如下图所示：

![Pipeline builder final output](../../../images/foundry/time-series/sensor-object-pipeline-overview.png)

此应用案例中提供的示例展示了一种将传感器数据从源数据集转换的方法。虽然传感器读数有各种不同的形式和多种可能的模式，但我们的示例使用了一个常见的模式；每行代表多个传感器的单一传感器读数（例如速度或高度），这些传感器与飞行相关（因此，`flight_ID`作为`Flight`对象的外键）。

![Sample starting data from a sensor reading dataset](../../../images/foundry/time-series/sensor-object-pipeline-starting-data.png)

| timestamp        | flight\_id     | heading | altitude | speed | latitude | longitude | vertical\_speed | flight\_ title |
| ---------------- | ------------- | ------- | -------- | ----- | -------- | --------- | -------------- | ------------- |
| 2023-01-11T23... | 021fcdbsd ... | 211     | 134      | 50    | 40.78354 | -73.87231 | -320           | YX4472...     |

本指南假设您对Pipeline Builder有基本的了解。查看我们的[Pipeline Builder文档](/zh/foundry/pipeline-builder/overview/)以获取关于一般管道指导的信息。本应用案例还假设飞行传感器读数数据已[导入到管道](/zh/foundry/pipeline-builder/datasets-add/)中。

## 第一部分：丰富传感器读数数据

一旦将传感器读数数据集添加到新管道中，您需要添加一些元数据。

### 1. 应用变换以重新格式化传感器读数

从传感器读数数据集中，按照以下步骤应用变换。

#### 取消透视数据以合并序列值

由于此数据集包含在不同列中的时间序列数据，您必须使用取消透视变换将其合并到一个值列中，以便数据可以匹配时间序列同步所需的模式，如下所示：

* **series ID:** `string` | TSP引用的一组时间戳和值对的系列ID，必须与TSP的系列ID匹配。
* **timestamp:** `timestamp`或`long` | 测量数量的时间。
* **value:** `integer`、`float`、`double`、`string` | 在测量时的数量值。字符串类型表示分类时间序列；每个分类时间序列最多可以有10,000种唯一变体。

如下所示的取消透视变换将`altitude`和`speed`的值放入相同的`series_value`列中。这些原始列名输出到新的`series_name`列中，以便父根对象可以识别每个传感器代表的内容（例如，高度）。

![The unpivot transform board in Pipeline Builder, merging sensor data into one column](../../../images/foundry/time-series/sensor-object-pipeline-unpivot.png)

变换后的数据集应预览新`series_value`和`series_id`列：

| series\_name | series\_value | timestamp        | flight\_id    | flight\_ title |
| ---------   | ------------ | ---------------- | ------------ | ------------- |
| altitude    | 134          | 2023-01-11T23... | 021fcdbsd... | YX4472...     |
| speed       | 114.00       | 2023-01-11T23... | 021fcdbsd... | YX4472...     |

#### 连接主键以创建系列ID

现在，您可以使用连接字符串变换创建系列ID（关联时间序列值的标识符）。使用变换将`series_name`（每个传感器代表的内容）与每个对象的主键组合。

![The concatenate strings transform board in Pipeline Builder](../../../images/foundry/time-series/sensor-object-pipeline-create-series-id.png)

| flight\_sensor\_series\_id | series\_name | series\_value | timestamp        | flight\_id    | flight\_ title |
| ----------------------- | ---------   | ------------ | ---------------- | ------------ | ------------- |
| altitude\_021fcdbsd...   | altitude    | 134          | 2023-01-11T23... | 021fcdbsd... | YX4472...     |
| speed\_021fcdbsd...      | speed       | 114.00       | 2023-01-11T23... | 021fcdbsd... | YX4472...     |

#### 删除空值

应用筛选变换以删除包含`null`值的任何行，这些行不会用于我们的时间序列计算。

![A filter transform board in Pipeline Builder, configured to filter out rows containing null values.](../../../images/foundry/time-series/sensor-object-pipeline-drop-null-series-values.png)

### 2. 向数据集添加单位

#### 手动上传单位数据集

由于原始示例传感器读数数据集不包括单位，您必须添加生成的数据集以将单位映射到系列名称。从Pipeline Builder图的左上角，选择**添加数据**，然后选择**手动输入数据**。创建一个名为`series_name`的列和另一个名为`units`的列。如有必要，您可以为内部插值重复此步骤（尽管我们的示例不需要）。

**内部插值**用于使[Quiver](/zh/foundry/quiver/overview/)推断相邻数据点之间的系列值。内部插值列将为Ontology提供一个属性，以保存每个传感器对象的插值设置。Quiver在可视化时间序列数据时将依赖于该属性。查看[我们的插值文档](/zh/foundry/quiver/timeseries-visualize/#interpolation-options)以获取更多信息。

:::callout{theme="neutral"}
一些传感器读数数据集确实包括单位；在这些情况下，您可以跳过此步骤并继续[创建传感器对象类型支持数据集](#3-concatenate-strings-to-create-title-properties-for-objects)。
:::

![Manually create a units dataset in Pipeline Builder](../../../images/foundry/time-series/sensor-object-pipeline-units-dataset.png)

#### 创建合并单位和传感器数据集的连接

使用合并面板，创建一个将单位和传感器数据合并的数据集连接。确保设置以下配置：

* 添加一个**左连接**并按`series_name`匹配。
* 自动选择来自左数据集的列。
* 仅选择`units`列作为右列。

![Use the join board to combine units and sensor datasets](../../../images/foundry/time-series/sensor-object-pipeline-join.png)

数据应预览新`units`列，如下所示：

| flight\_sensor\_series\_id | series\_name | series\_value | timestamp        | flight\_id    | flight\_ title | units |
| ----------------------- | ---------   | ------------ | ---------------- | ------------ | ------------- | ----- |
| altitude\_021fcdbsd...   | altitude    | 134          | 2023-01-11T23... | 021fcdbsd... | YX4472...     | ft    |
| altitude\_021fcdbsd...   | altitude    | 155          | 2023-01-11T23... | 021fcdbsd... | YX4472...     | ft    |
| speed\_021fcdbsd...      | speed       | 114.00       | 2023-01-11T23... | 021fcdbsd... | YX4472...     | mph   |
| speed\_021fcdbsd...      | speed       | 135.00       | 2023-01-11T23... | 021fcdbsd... | YX4472...     | mph   |

## 第二部分：创建传感器对象类型支持数据集

现在，您可以创建传感器对象类型了。按照以下步骤对连接输出应用变换，以创建最终支持传感器对象类型的数据集。

### 1. 删除重复数据以创建每个传感器的一行数据

一个传感器对象代表一个且仅一个相关时间序列数据集合（例如，某次飞行的`altitude`）。由于每个相关时间序列集合由`flight_sensor_series_id`唯一标识，您可以假设保留每个唯一飞行传感器系列ID的只有一行对应于一个传感器对象。使用生成的`flight_sensor_series_id`应用删除重复变换，您可以为每个传感器对象创建一行数据。稍后步骤中，您将删除其余的系列数据（时间戳和值）。

![The drop duplicates transform board in Pipeline Builder](../../../images/foundry/time-series/sensor-object-pipeline-drop-duplications.png)

数据集应如下所示：

| flight\_sensor\_series\_id | series\_name | series\_value | timestamp        | flight\_id    | flight\_ title | units |
| ----------------------- | ---------   | ------------ | ---------------- | ------------ | ------------- | ----- |
| altitude\_021fcdbsd...   | altitude    | 134          | 2023-01-11T23... | 021fcdbsd... | YX4472...     | ft    |
| speed\_021fcdbsd...      | speed       | 114.00       | 2023-01-11T23... | 021fcdbsd... | YX4472...     | mph   |

### 2. 哈希系列ID以创建主键

由于每个传感器对象必须唯一可识别，您必须使用哈希sha256变换为每个对象创建一个主键。您可以重复使用`series_id`，因为它应该在所有这些传感器对象中唯一，但哈希更直接地表明`series_id`应该仅用作唯一标识符。

![The hash sha256 transform board in Pipeline Builder, used to create a primary key from a series ID.](../../../images/foundry/time-series/sensor-object-pipeline-create-primary-key.png)

数据集应预览如下：

| unique\_sensor\_flight\_id  | flight\_sensor\_series\_id | series\_name | series\_value | timestamp        | flight\_id    | flight\_ title | units |
| ------------------------ | ----------------------- | ---------   | ------------ | ---------------- | ------------ | ------------- | ----- |
| 2492af5a2fe62c78ad8d...  | altitude\_021fcdbsd...   | altitude    | 134.00       | 2023-01-11T23... | 021fcdbsd... | YX4472...     | ft    |
| ec4808668f4b48cc5104...  | altitude\_011794756...   | altitude    | 0.0000       | 2023-01-22T17... | 011794756... | UA1878...     | ft    |

### 3. 连接字符串以创建对象的标题属性

现在，您应使用连接字符串变换为我们的传感器对象创建人类可读的标题属性。即使传感器对象将嵌入到另一个`Flight`对象的对象视图中，为传感器对象创建一个专门的名称将使用户在平台中搭建和分析传感器时更加直观。

![The concatenate strings transform board, used to create a new title for sensor objects.](../../../images/foundry/time-series/sensor-object-pipeline-create-title.png)

数据集应预览如下：

| title                         | unique\_sensor\_flight\_id  | flight\_sensor\_series\_id | series\_name | series\_value | timestamp        | flight\_id    | flight\_ title | units |
| ----------------------------- | ------------------------ | ----------------------- | ---------   | ------------ | ---------------- | ------------ | ------------- | ----- |
| Altitude sensor for YX4472... | 2492af5a2fe62c78ad8d...  | altitude\_021fcdbsd...   | altitude    | 134.00       | 2023-01-11T23... | 021fcdbsd... | YX4472...     | ft    |
| Altitude sensor for UA1878... | ec4808668f4b48cc5104...  | altitude\_011794756...   | altitude    | 0.0000       | 2023-01-22T17... | 011794756... | UA1878...     | ft    |

### 4. 删除不必要的列

由于我们的传感器对象仅代表传感器本身，您可以使用删除列变换删除剩余的`series_value`和`timestamp`列。这些列在时间序列属性中表示，并将基于`flight_sensor_series`值链接到Ontology中的传感器。此外，您将删除`flight_title`列，因为我们的传感器对象类型不需要它。

您将保留`flight_id`，以便传感器对象（`Flight Sensors`）可以链接到其根对象（`Flights`）。

![Drop timestamp and series value columns](../../../images/foundry/time-series/sensor-object-pipeline-drop-timestamp-values.png)

数据集应预览如下：

| title                         | unique\_sensor\_flight\_id  | flight\_sensor\_series\_id | series\_name | flight\_id    | units |
| ----------------------------- | ------------------------ | ----------------------- | ---------   | ------------ | ----- |
| Altitude sensor for YX4472... | 2492af5a2fe62c78ad8d...  | altitude\_021fcdbsd...   | altitude    | 021fcdbsd... | ft    |
| Altitude sensor for UA1878... | ec4808668f4b48cc5104...  | altitude\_011794756...   | altitude    | 011794756... | ft    |

### 5. 添加数据集输出以支持传感器对象类型

选择`添加输出`，然后选择`添加数据集`。生成的数据集应镜像变换中创建的模式。任何新的更改可能需要更新生成数据集中的模式。

## 第三部分：创建传感器对象类型时间序列同步

### 1. 将传感器读数转换为时间序列同步格式

使用选择列变换，您将仅保留时间序列同步所需的列：`series_id`、`timestamp`和`value`。支持数据集将保存所有传感器的值，而不管它们测量什么（例如，`altitude`和`speed`）。您可以使用生成的`flight_sensor_series_id`作为`series_id`，它是特定传感器数据集的唯一标识符。例如，从LGA到LAX的Flight A445B将有一个链接的传感器对象用于`speed`，它将保存该飞行的速度传感器数据。同样，它还将有一个链接的传感器对象用于`altitude`。

![Pipeline select columns for sensor data](../../../images/foundry/time-series/sensor-object-pipeline-transform-select-columns.png)

数据集输出应预览如下：

| flight\_sensor\_series\_id | series\_value | timestamp        |
| ----------------------- | ------------ | ---------------- |
| altitude\_021fcdbsd...   | 134.00       | 2023-01-11T23... |
| altitude\_011794756...   | 0.0000       | 2023-01-22T17... |

## 第三部分：创建时间序列同步

### 1. 配置时间序列同步

现在，选择屏幕右侧的管道输出部分中的**添加**，然后选择**时间序列同步**，创建一个[时间序列同步](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-sync)。填写新的时间序列同步所需的数据，考虑以下事项：

* 为[**系列ID**](/zh/foundry/time-series/time-series-concepts-glossary/#series-id)字段选择`flight_sensor_series_id`列。
* 在**时间**字段中添加创建的`timestamp`列。
* 在**值**字段中添加`series_value`。

![Configure a time series sync output in Pipeline Builder.](../../../images/foundry/time-series/sensor-object-pipeline-time-series-sync-output.png)

现在，[保存并搭建](/zh/foundry/pipeline-builder/outputs-deliver-pipeline/#save)管道。输出将创建在与管道相同的文件夹中。

### 2. 使用时间序列同步向传感器对象类型添加属性

现在，您已创建带有时间序列同步的管道，可以使用同步向传感器对象类型添加时间序列属性。继续查看我们的文档[向传感器对象类型添加时间序列属性](/zh/foundry/time-series/sensor-object-end-to-end-ontology/)以获取更多指导。

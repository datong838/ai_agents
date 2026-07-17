---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-integration/datasets/",
  "title": "数据集",
  "page_id": "datasets",
  "category_id": "data-integration",
  "section_id": null,
  "previous": "/zh/foundry/data-integration/application-reference/",
  "next": "/zh/foundry/data-integration/streams/",
  "scraped_at": "2026-07-13T05:30:15.144745+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数据集

**数据集**是数据从进入Foundry到映射到[Ontology](/zh/foundry/ontology/overview/)时最基本的表示形式。从根本上说，数据集是围绕存储在[支持文件系统](#backing-filesystem)中的一组**文件**的包装。使用Foundry数据集的好处在于它们提供了权限管理、模式管理、版本控制和随时间更新的集成支持。我们将在本文档的其余部分探讨此功能的基本概念。

在Foundry的数据集成层中，数据集用于存储和表示所有类型的数据——结构化、非结构化和半结构化：

* *结构化*（表格）数据由包含表格数据的开源格式（如[Parquet ↗](https://parquet.apache.org/)）的文件组成，以及关于数据集中的列的元数据。此元数据与数据集一起存储为[模式](#schemas)。
* *非结构化*数据集包括图像、视频或PDF等文件，但没有关联的模式。
* *半结构化*数据集包含XML或JSON等文件格式。虽然可以将模式应用于这些文件格式，但更倾向于在下游数据变换中[推断表格模式](/zh/foundry/building-pipelines/infer-schema/)，以提高性能和易用性。

## 事务

数据集被设计为随时间更改。当您在Foundry中打开数据集并看到行和列时，您实际上看到的是最新的[*数据集视图*](#dataset-views)。

作为终端用户，您通常会使用[搭建](/zh/foundry/data-integration/builds/)来修改数据集，允许您根据指定的逻辑更新数据集的内容。然而，在幕后，数据集是通过**事务**随时间更新的，这些事务代表数据集中文件的修改。事务具有简单的生命周期：

* 事务*开始*后，它处于`OPEN`状态。在此状态下，可以在数据集的支持文件系统中打开和写入文件。
* 事务可以*提交*，使其进入`COMMITTED`状态，任何已写入的文件现在都在最新的数据集视图中。
* 事务可以*中止*，使其进入`ABORTED`状态。在事务期间写入的任何文件都将被忽略。

如果您是一名软件工程师，您可能熟悉Git。数据集事务是Foundry对数据版本控制的支持基础，有时被称为“数据的Git”。事务类似于Git中的*提交*：对数据集内容的原子更改。

### 事务类型

在事务中修改数据集文件的方式取决于事务类型。有四种可能的事务类型：`SNAPSHOT`、`APPEND`、`UPDATE`和`DELETE`。

### `SNAPSHOT`

`SNAPSHOT`事务用全新的一组文件替换数据集的当前视图。

`SNAPSHOT`事务是最简单的事务类型，是[批处理管道](/zh/foundry/building-pipelines/pipeline-types/#batch)的基础。

### `APPEND`

`APPEND`事务向当前数据集视图添加新文件。

`APPEND`事务不能修改当前数据集视图中的现有文件。如果打开了`APPEND`事务并覆盖了现有文件，则尝试提交事务将会失败。

`APPEND`事务是[增量管道](/zh/foundry/building-pipelines/pipeline-types/#incremental)的基础。通过仅将新数据同步到Foundry并在整个管道中仅处理这些新数据，可以以高效的方式处理对大型数据集的更改。然而，构建和维护增量管道伴随着额外的复杂性。[了解有关增量管道的更多信息。](/zh/foundry/building-pipelines/incremental-overview/)

### `UPDATE`

`UPDATE`事务与`APPEND`类似，向数据集视图添加新文件，但也可能覆盖现有文件的内容。

### `DELETE`

`DELETE`事务删除当前数据集视图中的文件。

请注意，提交`DELETE`事务不会从支持文件系统中删除底层文件——它只是从数据集视图中删除文件引用。

实际上，`DELETE`事务主要用于实现数据保留工作流。通过根据保留策略（通常基于文件的年龄）在数据集中删除文件，可以从Foundry中删除数据，以同时降低存储成本和符合数据治理要求。

### 事务类型示例

想象一下数据集分支的以下事务历史记录，从最旧的开始：

1. `SNAPSHOT` 包含文件 `A` 和 `B`
2. `APPEND` 添加文件 `C`
3. `UPDATE` 修改文件 `A` 的内容为 `A'`
4. `DELETE` 删除文件 `B`

此时，当前数据集视图将包含 `A'` 和 `C`。如果我们添加第五个包含文件 `D` 的`SNAPSHOT`事务，那么当前数据集视图将仅包含 `D`（因为`SNAPSHOT`事务开始新视图），而前四个事务将在旧视图中。

### 保留

由于`DELETE`事务实际上不会从[支持文件系统](#backing-filesystem)中删除旧数据，您可以使用[保留策略](/zh/foundry/retention/overview/)删除不再需要的事务中的数据。

### 查看数据集的保留策略 \[Beta]

:::callout{theme="neutral" title="Beta功能"}
这是一个Beta功能，可能在您的Foundry实例中不可用。请联系您的Palantir代表获取更多信息。
:::

要查看当前应用于给定数据集的保留策略，请导航到[数据集详细信息页面](/zh/foundry/dataset-preview/overview/#details)。

![保留策略部分截图](../../../images/foundry/data-integration/retention-policies.png)

## 分支

虽然数据集事务被设计为使数据集的内容随时间变化，但需要额外的功能来实现*协作*——让多个用户同时对数据集进行更改实验。数据集中的**分支**旨在实现这些工作流。

要了解Foundry中的分支，无论是单个数据集还是整个管道，请参阅[分支](/zh/foundry/data-integration/branching/)概念页面。

## 数据集视图

数据集视图表示在某个时间点分支的数据集的有效文件内容。历史视图类似于数据集的历史版本。要计算视图中的文件：

1. 从一组空文件开始。
2. 给定时间的视图从该时间点之前的最新`SNAPSHOT`事务开始。如果没有`SNAPSHOT`事务，则取数据集的最早事务。
3. 对于视图中的第一个事务和每个后续事务，执行以下操作：
   * 对于`SNAPSHOT`（只能是第一个事务）或`APPEND`事务，将所有事务的文件添加到集合中。
   * 对于`UPDATE`事务，将所有事务的文件添加到集合中并替换现有文件。
   * 对于`DELETE`事务，从集合中删除事务中的所有文件。

结果文件集构成了数据集视图。

如果数据集仅包含`SNAPSHOT`事务，则视图的数量等于事务的数量。在增量数据集的情况下，视图的数量将等于`SNAPSHOT`事务的数量。

一个视图可能包含来自多个分支的事务。例如，给定一个从`SNAPSHOT`和一些`APPEND`事务开始的增量数据集的`master`分支，这些事务将构成分支上数据集视图的开始，如果分支上的后续事务也是`APPEND`（或严格来说，*不是*`SNAPSHOT`）事务。

## 模式

模式是定义如何解释视图内文件的*数据集视图*上的元数据。这包括如何解析视图中的文件，以及文件中的列或字段如何命名或类型化。Foundry中最常见的模式是*表格*的——它们描述数据集中的列，包括它们的名称和[字段类型](#supported-field-types)。

请注意，不能保证数据集中的文件实际符合指定的模式。例如，可以将Parquet模式应用于包含CSV文件的数据集。在这种情况下，尝试读取数据集内容的客户端应用程序将遇到由于某些文件不符合模式而导致的出错。

因为模式存储在*数据集视图*上，所以模式可以随时间更改。这很有用，因为数据集的内容可能会随着时间的推移而发生结构性变化。例如，新事务可能会向表格数据集中引入新列或更改字段的类型。

在Foundry中，您可以通过导航到**详细信息**选项卡并选择**模式**来查看[数据集预览](/zh/foundry/dataset-preview/overview/)应用程序中的任何数据集的模式。

### 支持的字段类型

以下是数据集中可用的字段类型列表：

* `BOOLEAN`
* `BYTE`
* `SHORT`
* `INTEGER`
* `LONG`
* `FLOAT`
* `DOUBLE`
* `DECIMAL`
* `STRING`
* `MAP`
* `ARRAY`
* `STRUCT`
* `BINARY`
* `DATE`
* `TIMESTAMP`

一些字段类型需要附加参数：

* `DECIMAL`需要`precision`和`scale`。如果您不确定这些参数的设置，建议的默认值为`precision: 38`和`scale: 18`。`38`是可能的最高精度值。
* `MAP`需要`mapKeyType`和`mapValueType`，这两者都是字段类型。
* `ARRAY`需要`arraySubType`，一个字段类型。
* `STRUCT`需要`subSchemas`，一个字段类型列表。

有关上述字段类型的更多信息，包括描述和示例，请参阅[Spark数据类型文档 ↗](https://spark.apache.org/docs/latest/sql-ref-datatypes.html)。

### 模式选项

在数据集预览的**详细信息**选项卡的**模式**部分，您可以在模式元数据底部的`options`块中为CSV文件添加非必填解析配置。有关更多信息，请参阅[CSV解析](/zh/foundry/dataset-preview/csv-parsing/)文档。

### 文件格式

模式包括有关数据集中文件的底层存储格式的信息。最广泛使用的三种格式是：

* Parquet
* Avro
* 文本

文本文件格式可用于表示多种文件类型，包括各种CSV格式或JSON文件。有关文本应如何解析的附加信息存储在一个名为`customMetadata`的模式字段中。

实际上，对于非表格式（如JSON或XML），我们建议将文件存储在非结构化（无模式）数据集中，并在下游数据变换中应用模式，如[模式推断文档](/zh/foundry/building-pipelines/infer-schema/)中所述。

## 支持文件系统

在数据集中跟踪的文件不存储在Foundry本身。相反，维护了文件在Foundry中的*逻辑路径*与其在支持文件系统中的*物理路径*之间的映射。Foundry的支持文件系统由[Hadoop FileSystem ↗](https://hadoop.apache.org/docs/r2.7.0/api/org/apache/hadoop/fs/FileSystem.html)中的基础目录指定。这可以是自托管的HDFS集群，但更常见的是使用云存储提供商（如Amazon S3）配置。所有数据集文件都存储在支持文件系统基础目录下的文件夹层次结构中。

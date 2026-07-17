---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/hyperauto/v1-configuration-reference/",
  "title": "配置参考",
  "page_id": "v1-configuration-reference",
  "category_id": "data-integration",
  "section_id": "hyperauto",
  "previous": "/zh/foundry/hyperauto/v1-cockpit/",
  "next": "/zh/foundry/hyperauto/v1-to-v2-differences/",
  "scraped_at": "2026-07-13T05:33:40.362385+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 配置参考

:::callout{theme="warning" title="警告"}
本节介绍了高级手动设置，如果未正确应用，可能会导致您的SDDI管道处于损坏状态。在部署到生产环境之前，请始终在分支上验证更改。
:::

SDDI的管道由一个全自动代码库生成。[Cockpit](/zh/foundry/hyperauto/v1-cockpit/)是与这些配置交互的默认位置，但您可能需要手动修改配置文件以获取高级参数或配置非标准源类型。

:::callout{theme="neutral"}
要查看所涉及的步骤，请阅读关于[管道生成](/zh/foundry/hyperauto/v1-overview/#pipeline-generation)的内容。
:::

配置在位于`transforms-bellhop/src/config/`文件夹中的两个主要文件中进行：

* [SourceConfig.yaml](#sourceconfigyaml)
* [PipelineConfig.yaml](#pipelineconfigyaml)

## SourceConfig.yaml

以下是一个完整定义的SourceConfig文件的示例。

```yaml
sourceName: MY_SOURCE  # 数据源名称
sourceRid: ri.magritte..source.abcdefgh-1234-5678-910a-zyxwvut  # 数据源的唯一标识符
sapContext:
  type: direct  # 数据连接类型，直接连接
rawFolderStructure:
  raw: /HyperAuto/source/raw  # 原始数据存储路径
  dataDictionary: /HyperAuto/source/metadata  # 数据字典存储路径
cleaningLibraries:
  - convert_all_columns_to_clean_types  # 数据清洗库，用于将所有列转换为清晰类型
deploymentSemanticVersion: 2  # 部署的语义版本
metadataSparkProfiles:
  - DRIVER_MEMORY_MEDIUM  # Spark配置，驱动器内存中等
languageKey: 'E'  # 语言键，'E'代表英语
tables:
  - tableName: ABCD  # 表名
    datasetTransformsConfig:
      datasetName: ABCD  # 数据集名称
      deduplicationComparisonColumns: []  # 去重比较列，当前为空
      batchUnionComponents: []  # 批量合并组件，当前为空
      tableCleaningLibraries: []  # 表清洗库，当前为空
  - tableName: WXYZ  # 表名
    datasetTransformsConfig:
      datasetName: WXYZ  # 数据集名称
      deduplicationComparisonColumns:
        - /PALANTIR/TIMESTAMP  # 去重比较列，时间戳
        - /PALANTIR/ROWNO  # 去重比较列，行号
      batchUnionComponents:
        - WXYZ_historical  # 批量合并组件，历史数据
        - WXYZ_incremental  # 批量合并组件，增量数据
      tableCleaningLibraries:
        - parse_timestamp_column  # 表清洗库，用于解析时间戳列
      sparkProfiles:
        profiles:
          - EXECUTOR_MEMORY_MEDIUM  # Spark配置，执行器内存中等
          - NUM_EXECUTORS_4  # Spark配置，执行器数量为4
```

上述YAML配置文件用于定义数据源及其相关的表信息，主要涉及数据清洗、去重、批量合并和Spark执行环境设置等内容。

### 参数描述

| 参数 | 描述 |
|---|---|
| `sourceName` | 用于识别源系统的名称。用于为主键和外键添加前缀。 |
| `sourceRid` | 附加到此SDDI实例的源的RID。 |
| [`sapContext`](#sapcontext) | （非必填）SAP上下文的详细信息。 |
| [`rawFolderStructure`](#rawfolderstructure) | 定义原始数据和元数据所在的文件夹。 |
| [`cleaningLibraries`](#cleaninglibraries) | 应用于所有表的清理库列表。 |
| [`deduplicationConfig`](#deduplicationConfig) | （非必填，默认：无）用于指定用于去重逻辑的列的配置。 |
| [`metadataSparkProfiles`](#metadataSparkProfiles) | （非必填，默认：无）用于应用于元数据生成的Spark配置文件列表。 |
| `languageKey` | （非必填，默认：'E'）用于丰富内容的语言。 |
| [`deploymentSemanticVersion`](#deploymentsemanticversion) | （非必填，默认：0）管道的语义版本；递增它将强制创建快照。 |
| [`tables`](#tables) | 要由SDDI处理的源表列表。 |

#### `sapContext`

（非必填）SAP上下文的详细信息。SAP Explorer将使用此信息预先选择上下文。每个上下文都需要有自己的SourceConfig文件。

#### `rawFolderStructure`

定义原始数据和元数据所在的文件夹。

字段:

* **`raw`**: 原始表导入的文件夹路径。
* **`dataDictionary`**: （非必填，默认：`raw`）元数据表导入的文件夹路径。

#### `cleaningLibraries`

应用于所有表的清理库列表。清理函数在`transforms-bellhop/src/software_defined_integrations/transforms/cleaned/function_libraries`中定义。

添加或删除函数需要增加[`deploymentSemanticVersion`](#deploymentsemanticversion)。

#### `deduplicationConfig`

（非必填，默认：无）用于指定去重逻辑的列的配置。此处定义的配置应用于所有表。

字段:

* **`comparisonColumns`**: 用于确定主键唯一性的最大值列。
* **`changeModeColumn`**: （非必填）如果指定，具有值`D`的行将在此列中被删除。

#### `deploymentSemanticVersion`

（非必填，默认：0）管道的语义版本；递增它将强制创建快照。

参见[增量变换](/zh/foundry/transforms-python/incremental-reference/)以了解`deploymentSemanticVersion`对增量和快照变换的影响。

#### `metadataSparkProfiles`

（非必填，默认：无）用于应用于元数据数据集生成（`objects`、`fields`、`links`和`diffs`）的Spark配置文件列表。

确保在此之前[将配置文件添加到存储库](/zh/foundry/code-repositories/spark-profiles/#importing-spark-profiles)。

#### `tables`

定义源中要由SDDI处理的表列表。

字段:

* **`tableName`**: 元数据中的表名。
* **`datasetTransformsConfig`**
  * **`datasetName`**: 原始数据的Foundry数据集名称。
  * **`deduplicationComparisonColumns`**: 表特定的配置，用于去重数据并指定用于去重逻辑的列。应用于全局去重字段之后。
  * **`changeModeColumn`**: （非必填）如果指定，具有值`D`的行将在此列中被删除。应用于全局更改模式列。
  * **`batchUnionComponents`**: 应在清理步骤之前合并的输入数据集名称列表。
  * **`sparkProfiles`**: （非必填）在不同变换阶段应用的Spark配置文件。
    * **`profiles`**: Spark配置文件；参见[将其添加到存储库的详细信息](/zh/foundry/code-repositories/spark-profiles/#importing-spark-profiles)。
    * **`stages`**: （非必填，默认：无）配置文件应用于的变换阶段。值应为\[CLEANED, DERIVED, ENRICHED, FINAL, RENAMED, RENAMED\_CHANGELOG]。如果为无，配置文件将应用于所有阶段。
  * **`tableCleaningLibraries`**: 应用于此表的清理库列表。清理函数在`transforms-bellhop/src/software_defined_integrations/transforms/cleaned/function_libraries`中定义。添加或删除函数将需要增加[`deploymentSemanticVersion`](#deploymentsemanticversion)。
  * **`enforceUniquePrimaryKeys`**: （非必填，默认：false）。如果为true并定义了`deduplicationComparisonColumns`，则保证在去重阶段每个主键只保留一个记录。这可能导致非确定性行为。

## PipelineConfig.yaml

一个完整定义的PipelineConfig文件示例。

```yaml
sourceName: HyperAuto
sourceType: SAP_ERP
sourceConfigFileNames:
  - SourceConfig.yaml  # 配置文件名称列表
outputFolder: /HyperAuto/source/output  # 输出文件夹路径
workflows:
  my_workflow:  # 工作流定义
    variables:  # 工作流变量
      - name: my_variable_name
        value: my_variable_value
    enrichments:  # 丰富操作列表
      - my_enrichment_name
tables:
  ABCD:  # 表定义
    displayName: Header Table  # 显示名称
    types:
      - OBJECT  # 表类型
  WXYZ:
    displayName: Item Table
    types:
      - OBJECT
      - METADATA  # 元数据类型
disableForeignKeyGeneration: False  # 是否禁用外键生成
disableEnrichedStage: False  # 是否禁用丰富阶段
disableRenamedStage: False  # 是否禁用重命名阶段
```

此配置文件用于定义数据源配置及处理流程，主要涉及表格定义、工作流变量、以及是否禁用特定阶段的选项。

### 参数描述

| 参数 | 描述 |
|---|---|
| `projectName` | 项目名称。用作Ontology对象的前缀。 |
| `sourceType` | SDDI支持的源类型。应为\[SAP\_ERP, SALESFORCE, ORACLE\_NETSUITE]之一。 |
| `sourceConfigFileNames` | 要在管道中包含的SourceConfig文件名列表。 |
| `outputFolder` | 定义将输出数据集写入的文件夹。 |
| `workflows`| 部署的工作流列表，包含配置。 |
| [`tables`](#tables) | 在此SDDI管道中处理的表列表。 |
| `disableEnrichedStage` | (非必填，默认: false) 如果启用，将不会生成富数据集。请谨慎使用，因为启用将导致工作流失败。 |
| `disableRenamedStage` | (非必填，默认: false) 如果启用，将不会生成renamed\_changelog数据集。请谨慎使用，因为启用将导致工作流失败。 |
| `disableForeignKeyGeneration` | 如果启用，将不会生成外键列。请谨慎使用，因为启用将导致工作流失败。 |

#### `tables`

在此SDDI管道中处理的表列表：

* **`displayName`**: 表的可读名称。输出数据集名称将以 `displayName (technicalName)` 的形式构建。
* **`types`**: 此表表示的数据类型列表（可以有多个）。
  * **OBJECT**: 构成Ontology中对象的主数据表。
  * **METADATA**: 包含对象信息和构建主键的元数据表。
  * **CUSTOMIZATION**: 在SDDI管道的`enriched`步骤中合并到主数据表的富化表。

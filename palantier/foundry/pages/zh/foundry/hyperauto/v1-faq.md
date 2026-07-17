---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/hyperauto/v1-faq/",
  "title": "HyperAuto V1 常见问题",
  "page_id": "v1-faq",
  "category_id": "data-integration",
  "section_id": "hyperauto",
  "previous": "/zh/foundry/hyperauto/v1-to-v2-differences/",
  "next": "/zh/foundry/data-integration/external-transforms/",
  "scraped_at": "2026-07-13T05:33:42.341330+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# HyperAuto V1 常见问题

## 一般使用技巧和指导

* [我可以在 SDDI 仓库中调试和预览代码吗？](#can-i-debug-and-preview-code-in-an-sddi-repository)
* [我可以配置一个自动添加新表的计划吗？](#can-i-configure-a-schedule-to-which-new-tables-will-be-automatically-added)
* [我的一个表/派生元素由于 `MODULE_UNREACHABLE` 出错，我该怎么办？](#one-of-my-tables--derived_element-is-failing-due-to-module_unreachable-what-should-i-do)
* [我将表 `<TABLE_NAME>` 添加到我的管道中，但当我尝试搭建我的管道时，出现 `AssertionError: 0 instances of <TABLE_NAME> found in 'objects' metadata table` 出错](#i-added-table-table_name-to-my-pipeline-but-when-i-try-to-build-my-pipeline-it-is-failing-with-assertionerror-0-instances-of-table_name-found-in-objects-metadata-table)
* [如果我在 Bellhop 配置文件中添加新表，是否需要增加语义版本？](#do-i-need-to-increase-semantic-version-if-i-add-new-tables-to-bellhop-config-files)
* [我可以禁用 SDDI 仓库生成的一些中间阶段吗？](#can-i-disable-some-of-the-intermediate-stages-generated-by-an-sddi-repositiory)

### 我可以在 SDDI 仓库中调试和预览代码吗？

可以，您可以在 SDDI 仓库中调试和预览代码。在 SDDI 仓库中，导航到文件 `/transforms-bellhop/src/software_defined_data_integrations/transforms/pipeline_builder.py` 并从 [预览](/zh/foundry/code-repositories/preview-transforms/) 按钮中选择您要预览的变换。

### 我可以配置一个自动添加新表的计划吗？

一个 SDDI 仓库会生成一个名为 `BUILD` 的数据集，该数据集连接到仓库生成的所有最终数据集。为了确保所有新引入的表都被搭建，创建一个新的完整搭建计划（包括上游数据集），以这个 `BUILD` 数据集为目标。智能调度器将仅为原始数据已刷新的管道部分启动搭建。

### 我的一个表/派生元素由于 `MODULE_UNREACHABLE` 出错，我该怎么办？

`MODULE_UNREACHABLE` 通常表示您的 Spark 环境中的 DRIVER\_MEMORY 不足。您可以在 SourceConfig.yaml 文件中为选定的表应用 Spark 配置文件；详情请参阅[配置参考](/zh/foundry/hyperauto/v1-configuration-reference/#tables)。不要忘记首先将[指派的配置文件](/zh/foundry/code-repositories/spark-profiles/#importing-spark-profiles)导入到您的仓库配置中。

### 我将表 `<TABLE_NAME>` 添加到我的管道中，但当我尝试搭建我的管道时，出现 `AssertionError: 0 instances of <TABLE_NAME> found in 'objects' metadata table` 出错

确保在新表被引入并添加到您的 SDDI 管道后，重新运行元数据数据集 `objects`、`links`、`fields` 和 `diffs`。

### 如果我在 Bellhop 配置文件中添加新表，是否需要增加语义版本？

不，在 Bellhop 配置文件中添加新表后，您不需要增加语义版本。但是，您需要重新搭建元数据数据集 `objects`、`links`、`fields` 和 `diffs`。

### 我可以禁用 SDDI 仓库生成的一些中间阶段吗？

可以。可以通过使用 [PipelineConfig 文件中的参数](/zh/foundry/hyperauto/v1-configuration-reference/#parameters-description-1) 来禁用外键生成、丰富阶段和重命名阶段。需要增加 [`deploymentSemanticVersion`](/zh/foundry/hyperauto/v1-configuration-reference/#deploymentsemanticversion) 以使更改生效。

:::callout{theme="warning"}
禁用任何或所有这些步骤将导致数据架构后果，并可能导致数据的下游使用中断。
:::

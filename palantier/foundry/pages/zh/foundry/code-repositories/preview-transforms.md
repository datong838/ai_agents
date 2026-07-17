---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/code-repositories/preview-transforms/",
  "title": "预览变换",
  "page_id": "preview-transforms",
  "category_id": "data-integration",
  "section_id": "code-repositories",
  "previous": "/zh/foundry/code-repositories/faq/",
  "next": "/zh/foundry/code-repositories/debug-transforms/",
  "scraped_at": "2026-07-13T06:01:43.548798+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 预览变换

在代码库中使用预览工具以有限的输入数据集样本运行代码，以快速预览输出。预览生成一个样本输出，而不提交更改、运行检查或在 Foundry 中实现任何数据集。预览可以加速开发周期，消除触发搭建以测试代码更改的需求。

:::callout{theme="success" title="提示"}
预览适用于所有 Foundry 数据集，包括带有[文件](/zh/foundry/building-pipelines/unstructured-overview/)和[模型](/zh/foundry/model-integration/overview/)的数据集。
:::

## 运行预览

可以从代码库中的两个地方触发预览。

(1) 在代码编辑器选项面板中选择预览：

![从代码编辑器选项运行预览](../../../images/foundry/code-repositories/preview-run-1.png)

(2) 在助手面板中选择预览：

![从助手面板运行预览 - 第一步](../../../images/foundry/code-repositories/preview-run-2-1.png)

![从助手面板运行预览 - 第二步](../../../images/foundry/code-repositories/preview-run-2-2.png)

一旦预览执行完毕，输出将显示：

![预览输出](../../../images/foundry/code-repositories/preview-run-3.png)

## 使用文件配置预览

预览可用于包含[非结构化文件](/zh/foundry/building-pipelines/unstructured-overview/)的数据集。在首次对包含文件的数据集运行预览时，必须配置将在样本中使用的文件。

![配置文件](../../../images/foundry/code-repositories/preview-config-files-1.png)

![选择文件](../../../images/foundry/code-repositories/preview-config-files-2.png)

选定样本文件后，可以通过从输入列表中选择相关输入来重新配置它们。保存配置后，预览将在选定的文件样本上执行代码。再次运行预览时，无需重新配置输入文件。一旦预览执行完毕，您可以以行或文件的形式查看样本输出。如果您有必要的权限，还可以选择下载输出文件。

## 使用模型配置预览

### 模型资产

无需额外配置，预览支持[模型资产](/zh/foundry/integrate-models/integrate-overview/)，这些资产可以是[在 Foundry 中训练的](/zh/foundry/integrate-models/model-asset-code-repositories/)、[由预训练文件支持的](/zh/foundry/integrate-models/model-asset-files/)、或是[导入的语言模型](/zh/foundry/integrate-models/language-models-import/)。

[容器支持的模型](/zh/foundry/integrate-models/container-overview/)和[外部托管的模型](/zh/foundry/integrate-models/external-model-connection/)目前不支持预览。

![模型输入的模型预览](../../../images/foundry/code-repositories/model-asset-preview-model-input.png)

## 数据集支持的模型

配置预览以与数据集支持的模型一起工作的过程与[使用文件配置预览](#configuring-preview-with-files)相同。请确保选择所有必要的建模特定文件，以确保预览能够成功执行。有关在代码库中开发模型的更多信息，请参阅[训练模型资产](/zh/foundry/integrate-models/model-asset-code-repositories/)。

## 预览在变换生成器中创建的变换

在[变换生成器](/zh/foundry/transforms-python/transforms-pipelines/#transform-generation)中创建的变换共享函数的名称；为了更容易选择预览的预期变换，更改生成的变换的`__name__`属性以生成有意义的名称。例如：

```python
from transforms.api import transform_df, Output

def generate_transforms():
    transforms = []
    for output_dataset_name in ["One", "Two", "Three"]:
        @transform_df(
            Output(f"/output/path/{output_dataset_name}"))
        def my_transform(ctx, output_dataset_name=output_dataset_name):
            # 默认情况下，生成的转换将被命名为 `my_transform (1)`, `my_transform (2)`...
            cols = ['id', 'value']  # 定义数据框的列名
            vals = [
                (0, f'{output_dataset_name}'),
                (1, f'{output_dataset_name}'),
                (2, f'{output_dataset_name}')
            ]  # 定义数据框的值，每个值都是一个元组 (id, value)
            df = ctx.spark_session.createDataFrame(vals, cols)  # 使用 Spark 创建数据框
            return df
        transforms.append(my_transform)
        transforms[-1].__name__ = f'{output_dataset_name}_{transforms[-1].__name__}' # 重写转换的名称
    return transforms

TRANSFORMS = generate_transforms()
```

该代码定义了一个函数 `generate_transforms()`，该函数会为每个指定的输出数据集名称创建一个转换函数 `my_transform`，并将其添加到 `transforms` 列表中。每个转换函数会生成一个包含三行数据的 Spark 数据框，其中的 `value` 列根据输出数据集名称动态设置。转换函数的名称也会被动态重命名，以包含输出数据集名称。

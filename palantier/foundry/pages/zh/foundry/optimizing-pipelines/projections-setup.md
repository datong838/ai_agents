---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/optimizing-pipelines/projections-setup/",
  "title": "设置投影",
  "page_id": "projections-setup",
  "category_id": "data-integration",
  "section_id": "optimizing-pipelines",
  "previous": "/zh/foundry/optimizing-pipelines/projections-overview/",
  "next": "/zh/foundry/optimizing-pipelines/projections-advanced/",
  "scraped_at": "2026-07-13T05:44:33.630078+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 设置投影

以下信息将指导您完成启用、配置和搭建数据集投影的过程。

:::callout{theme="neutral"}
*Noho* 是一个管理数据集投影的服务。
:::

## 为您的数据集启用投影

通过配置`noho: true`在数据集的模式中启用投影。

您可以在从变换中写入数据集时配置数据集的模式，或者在**详情**标签中手动修改模式。

```python
from transforms.api import transform, Input, Output

@transform(
    output_dataset=Output('/examples/example_output'),
    input_dataset=Input('/examples/example_input'),
)
def compute(output_dataset, input_dataset):
    # 将输入数据集转换为DataFrame
    input_dataset = input_dataset.dataframe()
    # 将DataFrame写入输出数据集，带有选项参数
    output_dataset.write_dataframe(input_dataset, options={"noho": "true"})
```

## 导航到投影选项卡

当查看一个数据集时，如果其在模式中配置了 `noho: true` 且您有权限编辑该数据集，您将看到一个 **投影** 选项卡。

## 打开创建对话框

选择 `添加新投影`。

## 选择投影列

选择要包含在投影中的列。

在大多数情况下，`所有列` 是合适的。然而，如果您知道查询只会选择部分列，您可以进行调整。

## 选择投影类型

选择投影的类型。

* 以 [筛选优化的投影](/zh/foundry/optimizing-pipelines/projections-overview/#filtering-on-a-list-of-columns) 为例，选择要筛选的列。
  * 顺序很重要，因为投影只会加速这个列表前缀上的查询。
* 以 [合并优化的投影](/zh/foundry/optimizing-pipelines/projections-overview/#joining-on-a-set-of-columns) 为例，选择合并列和桶数。
  * 只有在这组确切的列上，合并才会加速。
  * 当与显式分桶的数据集或其他合并优化的数据集进行合并时，桶数必须相等。

## 创建投影

选择 `创建投影` 按钮。

投影现在已存在但不包含数据。这由投影旁的红色警告图标表示。要在查询中使用投影，必须按照接下来的步骤进行构建。

## 设置搭建

为使您更好地控制资源使用，维护投影的内部搭建不会自动安排；您需要明确设置一个。

首先，切换开关 `在当前分支上启用投影搭建`。这允许搭建在**当前**分支上运行。

然后，配置搭建的计划。如果您想在不同的分支上安排搭建，您需要导航到该分支并重复此过程。

## （非必填）搭建投影

如果您不想等待搭建，选择 **搭建** 按钮来明确搭建投影。

现在，等待搭建完成。在投影更新之前，可能会运行多个搭建。`投影搭建状态` 行旁的绿色勾号表示投影现已完全更新。

投影现在是最新的，并将用于数据集的读取。

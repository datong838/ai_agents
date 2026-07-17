---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/preparation/advanced-examples/",
  "title": "高级示例",
  "page_id": "advanced-examples",
  "category_id": "data-integration",
  "section_id": "preparation",
  "previous": "/zh/foundry/preparation/basic-examples/",
  "next": "/zh/foundry/preparation/faq/",
  "scraped_at": "2026-07-13T06:05:47.850110+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 高级示例

本页探讨了在Preparations界面中清理和准备数据的高级变换和工作流示例。

## 编写表达式

Preparation的**应用表达式**功能允许您使用Contour丰富的表达式语言对数据列进行高级变换。了解更多关于[表达式语法和函数参考](/zh/foundry/contour/expressions-syntax/)的信息。

## 在不同的数据集上重复使用准备

1. 通过选择**复制文件**从准备文件名旁边向下箭头指示的操作菜单中复制准备。

   <img src="../../foundry-docs/preparation/media/preparation_duplicate_file.png" style="max-height: 119.5px;" />

2. 如需更改起始数据集，首先滚动到更改日志底部的起始数据集。

3. 接下来，点击设置菜单并选择**更改**。

4. 最后，选择所需的起始数据集。

   <img src="../../foundry-docs/preparation/media/preparation_change_dataset.png" style="max-height: 164.5px;" />

:::callout{theme="warning"}
更新数据集的模式或数据中的一些差异（例如，不同的列名或类型）可能与准备中所做的更改不兼容。如果是这样，您将看到一条出错消息，并且更改会以红色突出显示。根据需要删除指示的更改。
:::

## 使用多个输出数据集分支

准备可以使用多个输出数据集分支。执行此操作的说明如下。

### 创建新分支

1. 点击准备名称下方标题中的分支选择器下拉菜单。
2. 在弹出窗口中输入新分支名称，然后点击**创建分支**按钮。

   <img src="../../foundry-docs/preparation/media/dataset_create_branch.png" style="max-height: 200px;" />

### 保存到不同分支

1. 点击**操作**菜单按钮，然后选择**保存到另一个分支**。在更新数据集下拉菜单中，选择要保存到的分支。

   <img src="../../foundry-docs/preparation/media/dataset_save_branch.png" style="max-height: 200px;" />

2. 确认提示并点击**保存**。

   <img src="../../foundry-docs/preparation/media/dataset_save_branch_alert.png" style="max-height: 200px;" />

### 切换当前分支

点击准备名称下方标题中的分支选择器下拉菜单。在输入字段中输入内容以筛选可用分支列表。

<img src="../../foundry-docs/preparation/media/dataset_branch_selector.png" />

### 恢复已保存的版本

1. 切换到您希望恢复的保存版本的分支。
2. 点击**操作**下拉按钮，然后点击**恢复已保存版本**选项。

<img src="../../foundry-docs/preparation/media/dataset_restore_saved.png" style="max-height: 200px;" />

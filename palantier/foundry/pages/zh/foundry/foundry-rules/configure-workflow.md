---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/foundry-rules/configure-workflow/",
  "title": "配置工作流",
  "page_id": "configure-workflow",
  "category_id": "ontology",
  "section_id": "foundry-rules",
  "previous": "/zh/foundry/foundry-rules/deploy-workflow/",
  "next": "/zh/foundry/foundry-rules/author-and-run-a-rule/",
  "scraped_at": "2026-07-14T04:47:52.920885+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 配置工作流

完成[部署工作流模板](/zh/foundry/foundry-rules/deploy-workflow/)后，以下步骤将指导您完成[配置工作流](/zh/foundry/foundry-rules/foundry-rules-workflow-configuration/)的过程。

1. **访问现有规则：** 从Foundry Rules主页中，通过选择项目从现有规则列表中选择一个。或者，您也可以在**文件**中找到相应项目并选择它。

   ![Foundry Rules中现有规则列表](../../../images/foundry/foundry-rules/overview@2x.png)

2. **添加工作流输入：** 查看规则时，选择**添加输入**按钮以添加Object或数据集输入到工作流中。这将成为下一部分中编写的规则的输入。

   * 您可以在此处添加任意数量的输入，但所有工作流必须至少包含一个输入。
   * 当添加Object类型输入时，链接类型部分将显示在每个Object类型下方。选择的任何链接将在[规则管理应用程序](/zh/foundry/foundry-rules/workshop-application/)中用于合并不同的Object。

   ![添加新工作流输入按钮](../../../images/foundry/foundry-rules/add_workflow_input.png)

:::callout{theme="neutral"}
受限视图支持的Object不能直接用作输入。相反，将支持受限视图的数据集配置为[备用支持数据集](/zh/foundry/foundry-rules/configure-workflow/#alternate-backing-datasets)。
:::

3. **添加工作流输出：** 在编辑器的第三部分，点击**添加数据集输出**并提供数据集的名称和位置，以输出规则结果。

   ![添加新工作流输出按钮](../../../images/foundry/foundry-rules/add_workflow_output.png)

   * 提供将在**规则管理应用程序**中显示给规则作者的输出名称 (a)。
   * 点击**添加列**以向输出添加至少一列 (b)。为此列提供一个将在数据集中使用的名称和一个将在规则应用程序中显示给规则作者的显示名称。您可以配置列的类型并确定在编写规则时是否需要提供此列。了解更多关于[允许和默认输出值](/zh/foundry/foundry-rules/permitted-and-default-output-values/)的信息。
   * 为您希望从规则结果中捕获的每条信息添加一列。例如，警报工作流可能包含`Alert ID`、`Severity`和`Assignee`的列，以及捕获触发警报的Object的标识符的列（例如`Machine ID`）。

   ![配置工作流输出](../../../images/foundry/foundry-rules/workflow_output_configuration.png)

4. **保存工作流：** 在配置编辑器的右上角，点击保存按钮。

   * 保存工作流后，您应该会看到编辑器顶部出现绿色横幅，表示[变换管道](/zh/foundry/foundry-rules/foundry-rules-workflow-configuration/#rule-execution)已成功创建。

   ![显示变换管道已成功创建的横幅](../../../images/foundry/foundry-rules/transforms-pipeline-success-banner.png)

完成上述步骤后，了解如何[编写和运行规则](/zh/foundry/foundry-rules/author-and-run-a-rule/)。

## 高级配置

### 备用支持数据集

您可以为Object输入配置备用支持数据集。这意味着您的规则将在提供的备用支持数据集上进行评估，而不是在Ontology中配置的数据输出（或支持）数据集上。

这在以下情况中很有用：

* 编写基于受限视图的Object的规则
* 在Object的支持数据的子集上运行规则

<img src="../../foundry-docs/foundry-rules/media/configuring_alternate_backing_datasets.png" alt="配置备用支持数据集" width="800" />

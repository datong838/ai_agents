---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-java/getting-started/",
  "title": "入门指南",
  "page_id": "getting-started",
  "category_id": "data-integration",
  "section_id": "transforms-java",
  "previous": "/zh/foundry/transforms-java/overview/",
  "next": "/zh/foundry/transforms-java/transforms-pipelines/",
  "scraped_at": "2026-07-13T06:08:32.230171+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 入门指南

:::callout{theme="success" title="提示"}
以下说明逐步介绍一个简单的Java数据变换。如果您刚开始使用数据变换，建议先浏览批处理管道教程 [Pipeline Builder](/zh/foundry/building-pipelines/create-batch-pipeline-pb/) 或 [代码库](/zh/foundry/building-pipelines/create-batch-pipeline-cr/)。
:::

按照以下步骤开始编写您的第一个Java变换：

1. 创建一个新的Transforms Java代码库。导航到一个项目，选择 **+ 新建** > **代码库**，并在 **语言模板** 下选择 **Java**。

2. 下载此示例数据集：[`下载 titanic.zip`](../../foundry-docs/transforms-java/media/titanic.zip)。将此数据集导入到Foundry中。

3. 导航到您的代码库。您的数据变换代码位于 `myproject/datasets/HighLevelAutoTransform.java` 中。此文件中的示例代码被注释掉了，因此请确保取消注释，然后再继续。

4. 通过将 `/path/to/input/dataset` 替换为您的 `titanic` 数据集的完整路径来更新输入数据集。

5. 通过将 `/path/to/output/dataset` 替换为您期望的输出数据集位置的完整路径来更新输出数据集。

6. 让我们修改默认的变换代码，以筛选基于性别的 `titanic` 数据集，获取所有女性乘客。在 `my_compute_function` 中更新您的数据变换代码：

   ```java
   @Compute
   // 将此替换为输出数据集的完整路径。
   @Output("/path/to/output/dataset")
   // 将此替换为 "titanic" 数据集的完整路径。
   public Dataset<Row> myComputeFunction(@Input("/path/to/input/dataset") Dataset<Row> myInput) {
       return myInput.filter(myInput.col("Sex").equalTo("female"));
   }
   ```

7. 成功提交更改到您的分支后，您可以打开并搭建您的输出数据集！

这个示例定义了一个使用自动注册的高层变换。有关Transforms Java中支持的不同类型数据变换的更多信息，以及模板项目结构和包含的文件的说明，请参阅[此文档](/zh/foundry/transforms-java/transforms-pipelines/)。

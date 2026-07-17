---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/code-repositories/spark-profiles/",
  "title": "Spark 配置文件",
  "page_id": "spark-profiles",
  "category_id": "data-integration",
  "section_id": "code-repositories",
  "previous": "/zh/foundry/code-repositories/repository-upgrades/",
  "next": "/zh/foundry/code-repositories/artifact-settings/",
  "scraped_at": "2026-07-13T06:02:01.763407+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Spark 配置文件

存储库设置用于指定在存储库中使用的 [Spark 配置文件](/zh/foundry/optimizing-pipelines/spark-concepts/#tuning-spark-profiles)。在存储库设置中配置 Spark 配置文件后，您可以[在代码中使用配置文件](/zh/foundry/optimizing-pipelines/apply-spark-profiles/)。

在应用给定的配置文件之前，必须将其导入项目。配置文件有两种类型：

* *无限制配置文件*：可以由所有用户导入到存储库的配置文件。
* *限制配置文件*：只能由管理员导入的配置文件。

已经可用于存储库中的 Spark 配置文件可以在**设置**选项卡下的 **Spark** 部分的**已启用配置文件**中找到。

### 导入 Spark 配置文件

为了在变换任务中使用 Spark 配置文件，必须首先将配置文件导入包含该任务的项目，否则在尝试发布变换时检查将失败。

可以通过代码存储库编辑器中的 Spark 配置选项卡浏览并导入 Spark 配置文件到项目。

要将配置文件导入项目，请转到**设置**选项卡并选择 **Spark**。点击**添加配置文件**以在下拉菜单中找到所需的配置文件。将鼠标悬停在您需要的配置文件上：

* 如果配置文件是无限制的，您可以点击**导入**将配置文件导入项目。
* 如果配置文件是限制的，您可能会看到它旁边有一个锁。

默认情况下，任何 [资源管理](/zh/foundry/resource-management/overview/) 管理员都具有导入限制 Spark 配置文件的必要权限。此外，可能有一个名为 `spark-profile-admins` 的用户组也具有必要的权限。普通用户必须请求管理员将配置文件导入他们的项目，然后他们才能使用。

![spark-profiles-settings](../../../images/foundry/code-repositories/spark-profiles-settings-3.gif)

### 已启用的 Spark 配置文件

项目中已启用的所有配置文件都可以在项目的总结侧边栏的[引用窗格](/zh/foundry/projects/use-project-navigation-panel/#references)中发现。当导入到存储库时，配置文件会自动添加为整个项目的引用，并作为项目中所有存储库的“已启用配置文件”提供。

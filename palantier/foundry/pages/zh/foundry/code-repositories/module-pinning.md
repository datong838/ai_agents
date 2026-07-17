---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/code-repositories/module-pinning/",
  "title": "在平台内固定 Spark 模块",
  "page_id": "module-pinning",
  "category_id": "data-integration",
  "section_id": "code-repositories",
  "previous": "/zh/foundry/code-repositories/unit-tests/",
  "next": "/zh/foundry/code-repositories/libraries/",
  "scraped_at": "2026-07-13T06:00:35.159929+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 在平台内固定 Spark 模块

代码库允许您为某个库固定一个 Spark 模块。这会强制使用特定版本的 Spark。您可以为新的和现有的搭建固定一个 Spark 模块。

:::Callout{theme="neutral"}
我们建议您始终使用最新版本的 Spark，以获取最新的性能和安全功能。固定 Spark 模块应为临时措施。
:::

## 如何固定 Spark 模块

导航到代码库中的 **Settings** 标签页，然后选择 **Runtime overrides**。

![The Runtime overrides tab](../../../images/foundry/code-repositories/Module_pinning_2.png)

### 创建固定

在 **Runtime overrides** 标签页中，选择 **Set pin**。

![Creating a pin on all branches](../../../images/foundry/code-repositories/Module_pinning_3.png)

您可以在所有分支上或特定分支上创建固定。您可以选择要固定的 Spark 模块版本（对于给定库中可用的每种模块类型），并指定一个过期日期。过期日期不能超过当前日期的90天。固定将在90天期限结束时或您指定的过期日期时失效，以较早者为准。过期日期之后，您的搭建可能会失败。

#### 在所有分支上创建固定

首先指定您要固定的 Spark 版本和过期日期。

![Selecting a version](../../../images/foundry/code-repositories/Module_pinning_4.png)

:::callout{theme="neutral"}
不稳定和不推荐的版本前缀有警告标志，因为我们不建议使用它们，除非绝对必要。
:::

完成后，选择 **Save** 以设置固定。

#### 在特定分支上创建固定

您可以为每个分支固定版本。您还可以为未指定的分支选择版本。

![Selecting versions per branch](../../../images/foundry/code-repositories/Module_pinning_6.png)

完成后，选择 **Save** 以设置固定。在下面的示例截图中，我们为所有分支创建了版本1.916.0的固定，该固定将于2023年12月20日凌晨12:00过期。

![Pre-Save screen](../../../images/foundry/code-repositories/Module_pinning_7.png)

设置固定后，您可以查看固定已创建的确认信息。

![Confirmation](../../../images/foundry/code-repositories/Module_pinning_8.png)

## 编辑现有固定

选择 **Edit** 允许您修改固定。您可以使用与创建固定相同的工作流程更改分支、版本和过期日期。选择 **Archive** 将删除固定，并将 `Expired` 标签添加到您之前设置的固定中。

![Archiving confirmation](../../../images/foundry/code-repositories/Module_pinning_9.png)

您可以选择 **Restore** 以重新创建您存档的固定。

![Expired label](../../../images/foundry/code-repositories/Module_pinning_10.png)

## 查看您的固定

在 **Build Preview > view details** 页面上，您可以查看为库固定的版本。

![Build preview view](../../../images/foundry/code-repositories/Module_pinning_11.png)

## 使用固定来控制代码库 CI 中的变换版本

在代码库中运行持续集成（CI）搭建时，会根据当前库模板版本选择[变换库](/zh/foundry/transforms-python/transforms-python-api/)的版本。如果应用了固定，CI 将使用固定版本的库，前提是它高于模板声明的最低版本。用户可以利用固定更快地访问 API 的新版本以及代码辅助和[本地开发](/zh/foundry/transforms-python/local-development/)的新功能。

## 常见问题

### 1. 为什么固定在90天后过期？为什么我不能将其用于更长时间？

我们建议您始终使用最新版本的 Spark。否则可能会错过性能和安全修复和改进，这可能对您的搭建产生不利影响。

话虽如此，我们理解可能有特定的用例使得固定是必要的，因此提供了这一功能，但需注意它应为临时使用。过期日期之前，我们建议您在您这边进行所需更改以兼容最新版本的 Spark。

### 2. 当我的固定即将过期时，我可以通过 UI 获取通知吗？

此功能正在开发中。

### 3. 我可以通过任务跟踪器 UI 固定单个搭建吗？

此功能正在开发中。

### 4. 我是否需要升级或在我这边进行更改以使用此功能？

您无需进行任何升级或操作。

### 5. 此功能是为新搭建提供的吗，还是可以应用于现有搭建？

您可以将此功能用于新搭建和现有搭建。

### 6. 如果我的任务已经在 cdconfig 中固定，会发生什么？

平台内固定将始终优先。

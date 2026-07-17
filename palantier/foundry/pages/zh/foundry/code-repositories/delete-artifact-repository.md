---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/code-repositories/delete-artifact-repository/",
  "title": "删除 Artifact 仓库",
  "page_id": "delete-artifact-repository",
  "category_id": "data-integration",
  "section_id": "code-repositories",
  "previous": "/zh/foundry/code-repositories/create-artifact-repository/",
  "next": "/zh/foundry/code-repositories/publish-artifact/",
  "scraped_at": "2026-07-13T06:00:37.430343+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 删除 Artifact 仓库

:::callout{theme="danger"}
删除 Artifact 仓库将移除其中包含的所有 Artifact。这被视为重大更改，所有使用已删除 Artifact 的用户都会受到影响。删除 Artifact 仓库时请小心。
:::

要删除 Artifact 仓库，首先导航到包含该 Artifact 仓库的项目。然后，右键点击 Artifact 仓库并选择 **移至回收站**。

<img src="../../foundry-docs/code-repositories/media/ar-delete.png" alt ="删除" width="300">

要永久删除 Artifact 仓库，请导航到项目中的 **回收站** 标签。右键点击 Artifact 仓库并选择 **永久删除**。此操作无法撤销。

可能可以恢复 Artifact 仓库。首先，导航到项目中的 **回收站** 标签。然后，右键点击 Artifact 仓库并选择 **恢复**。如果您没有看到 **回收站** 标签，请确保您在项目概览中，而不是项目内的某个文件夹中。

<img src="../../foundry-docs/code-repositories/media/ar-restore.png" alt ="恢复" width="400">

了解更多关于[在 Foundry 中删除和恢复文件](/zh/foundry/projects/use-project-navigation-panel/#trash)。

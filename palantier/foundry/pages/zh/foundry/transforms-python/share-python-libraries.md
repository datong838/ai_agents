---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/share-python-libraries/",
  "title": "共享Python库",
  "page_id": "share-python-libraries",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/use-python-libraries/",
  "next": "/zh/foundry/transforms-python/local-development/",
  "scraped_at": "2026-07-13T06:07:43.821739+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 共享Python库

跨多个变换Python库共享代码的推荐工作流程是发布一个Python库包——特别是[Conda ↗](https://conda.io/docs/)库。在Transforms Python 1.23.1+中支持发布Python库。

## 发布Python库

以下是发布Python库所需的步骤：

1. **创建一个新仓库**，该仓库将包含用于共享库的Python代码。

2. **命名你的仓库。** 初始化时，你的库将以仓库名称命名。其他代码仓库将使用此名称来发现和使用你的库。你可以通过访问`gradle.properties`文件并编辑`condaPackageName`参数来稍后重命名它（此文件是隐藏的，因此你可能需要先在文件编辑器中选择“显示隐藏文件”）。

:::callout{title="库命名"}
请注意，`condaPackageName`只能包含ASCII小写字母、数字或连字符。任何非字母数字/非连字符字符的序列将被替换为单个连字符（例如，`my_library repo`将发布为`my-library-repo`，而`Foobar _baz$$$`将发布为`foobar-baz-`）。
:::

3. 在**Python库**模板部分中点击**创建**按钮。

4. **创建一个包：** 你的库中包含`__init__.py`文件的任何文件夹将被发布为一个包。你的仓库将以这样的文件夹初始化 - 根据需要重命名它并添加其他包。

5. **创建模块：** 在你的包文件夹中，你可以添加包含代码的Python文件。这些模块稍后将被其他仓库导入。

![Artifact仓库和变换仓库之间映射的示意图](../../../images/foundry/transforms-python/meta-yaml-mapping.png)

6. **标记你的仓库：** 当你准备好发布时，导航到“分支”选项卡，选择“标签”并创建一个新标签。默认情况下，你的Python库只会为带标签的提交发布。要更改此默认行为，你必须修改`build.gradle`文件。

![python-package-tagging](../../../images/foundry/transforms-python/python-package-tagging.png)

:::callout{theme="warning" title="警告"}
请注意，标签名称必须符合SLS版本控制，具体请参阅[SLS版本文档 ↗](https://github.com/palantir/sls-version-java)。
:::

7. 检查成功完成后，你的库版本将被发布。你可以在标签列表和仓库的检查选项卡中查看检查的状态。

:::callout{theme="neutral"}
默认情况下，只有当你创建标签时，你的库更改才会被发布。你可以为某个分支的当前状态或某个特定提交创建标签。一旦检查通过，你的库将被发布，用户将能够升级到最新版本。
:::

:::callout{theme="neutral"}
当发布新版本时，消费仓库不会自动升级以使用最新版本。
要手动升级你的仓库以使用最新版本，请参阅有关[发现和使用Python库](/zh/foundry/transforms-python/use-python-libraries/)和[Conda锁定文件](/zh/foundry/transforms-python/use-python-libraries/#conda-lock-files)以重新解析Conda环境的文档。
:::

8. 确保你为库消费者授予权限。默认情况下，用户在共享仓库中应具有“只读”角色。在变换仓库设置的Artifacts选项卡下添加对库仓库的引用。

![仓库设置Artifacts选项卡的截图](../../../images/foundry/transforms-python/repository-artifact-settings-tab.png)

此时，你的库应该可以供其他应用程序和仓库使用。阅读更多关于[发现和使用Python包](/zh/foundry/transforms-python/use-python-libraries/)的信息。

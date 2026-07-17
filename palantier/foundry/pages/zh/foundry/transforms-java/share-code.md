---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-java/share-code/",
  "title": "在代码库之间共享代码",
  "page_id": "share-code",
  "category_id": "data-integration",
  "section_id": "transforms-java",
  "previous": "/zh/foundry/transforms-java/user-defined-functions/",
  "next": "/zh/foundry/transforms-java/local-development/",
  "scraped_at": "2026-07-13T06:08:46.886270+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 在代码库之间共享代码

本节介绍在代码库之间共享Java代码的基本工作流程。

## 前提条件

在继续阅读之前，请确保您已创建一个包含将依赖于其他代码库的Java代码/宏的单独代码库。在本指南中，我们将把包含要共享的Java代码/宏的代码库称为\_共享代码库\_，而将依赖于\_共享代码库\_的任何代码库称为\_依赖代码库\_。

在将Java代码/宏添加到您的\_共享代码库\_后，请确保通过提交您的更改来编译该代码库。

## 权限设置

为了共享代码，您必须确保\_依赖代码库\_可以访问由\_共享代码库\_生成的工件。要配置可以从\_依赖代码库\_引用的工件，请导航到\_设置\_选项卡的\_工件\_部分。[了解更多关于工件设置的信息。](/zh/foundry/code-repositories/artifact-settings/)

## Gradle 设置

### 针对依赖代码库

:::callout{theme="neutral"}
在代码库之间共享代码（包括Java代码和宏）时，\_依赖代码库\_的Gradle设置是必需的。
:::

Jemma会自动发布由\_共享代码库\_生成的工件。因此，在设置上述所需权限后，所有\_依赖代码库\_需要做的就是指向已发布的工件。这将涉及在\_依赖代码库\_的语言特定子项目的`build.gradle`文件末尾添加如下块：

```gradle
dependencies {
    // 添加依赖项
    // <SHARED_CODE_REPO_RID> 表示共享代码库的标识符
    // <SHARED_CODE_REPO_GRADLE_SUBPROJECT> 表示共享代码库中的子项目
    // <SHARED_CODE_REPO_VERSION> 表示共享代码库的版本
    compile '<SHARED_CODE_REPO_RID>:<SHARED_CODE_REPO_GRADLE_SUBPROJECT>:<SHARED_CODE_REPO_VERSION>'
}
```

让我们逐步了解获取所需信息并将其添加到 `build.gradle` 文件的过程。

1. 首先，您需要 `SHARED_CODE_REPO_RID`，即 *共享代码库* 的 RID。您可以从仓库 URL 获取此信息。或者，您可以在工件设置选项卡上点击仓库条目，以便将上面的 `compile` 行与填充的共享仓库 RID（例如 `compile 'ri.stemma.repository.some-random-rid:<SHARED_CODE_REPO_GRADLE_SUBPROJECT>:<SHARED_CODE_REPO_VERSION>'`）复制到您的剪贴板。

   ![工件设置选项卡](../../../images/foundry/transforms-java/artifacts-copy-dependency.png)

2. 接下来，您需要获取 `SHARED_CODE_REPO_GRADLE_SUBPROJECT` 和 `SHARED_CODE_REPO_VERSION` 的值。为获取这些信息，请通过在 *共享代码库* 的 `ci.yml` 文件中添加 `--info` 来修改最后一行（起始为 `./gradlew`）。例如：

   ```
   ./gradlew --no-daemon --build-cache --stacktrace patch publish
   ```

   变为：

   ```
   ./gradlew --no-daemon --build-cache --stacktrace patch publish --info
   ```

   然后，查看 *共享代码库* 中最新 Jemma 任务的 CI 输出。在 CI 输出中查找与以下形式之一匹配的行：

   ```
   Upload https://<MAVEN_REPO_URL>/maven-repository-proxy/authz/user-code/<SHARED_CODE_REPO_RID>/<SHARED_CODE_REPO_GRADLE_SUBPROJECT>/<SHARED_CODE_REPO_VERSION>/<SHARED_CODE_REPO_GRADLE_SUBPROJECT>-<SHARED_CODE_REPO_VERSION>.jar
   ```

   或

   ```
   Uploading: ri/stemma/main/repository/<SHARED_CODE_REPO_UUID>/<SHARED_CODE_REPO_GRADLE_SUBPROJECT>/<SHARED_CODE_REPO_VERSION>/<SHARED_CODE_REPO_GRADLE_SUBPROJECT>-<SHARED_CODE_REPO_VERSION>.jar to repository remote at https://<ARTIFACTS_URL>/artifacts/api/legacy/mrp/authz/user-code/
   ```

   或

   ```
   Uploading: ri/stemma/main/repository/<SHARED_CODE_REPO_UUID>/<SHARED_CODE_REPO_GRADLE_SUBPROJECT>/<SHARED_CODE_REPO_VERSION>/<SHARED_CODE_REPO_GRADLE_SUBPROJECT>-<SHARED_CODE_REPO_VERSION>.jar to repository remote at https://<ARTIFACTS_URL>/artifacts/api/repositories/<SHARED_CODE_REPO_UUID>/contents/release/maven/
   ```

   使用 CI 输出中的信息，您可以构建引用 *共享代码库* 生成的工件的 Maven 坐标。请注意，您在 Maven 坐标中提供的 `<SHARED_CODE_REPO_RID>` 应为 `ri.stemma.main.repository.{RID_VALUE}` 形式。

3. 现在，您拥有了 Maven 坐标，可以更新 `build.gradle` 文件。请确保在特定语言的子项目文件夹中编辑 `build.gradle` 文件（例如 `transforms-java/build.gradle`），**而不是在仓库的根目录下**。您更新后的 `build.gradle` 应类似如下（注意两个 `dependencies` 块）：

   ```gradle
   buildscript {
       // ...
       dependencies {
           classpath "com.palantir.transforms.java:lang-java-gradle-plugin:${transformsJavaVersion}"
       }
   }

   apply plugin: 'com.palantir.transforms.lang.java'
   apply plugin: 'com.palantir.transforms.lang.java-defaults'

   dependencies {
       compile '<SHARED_CODE_REPO_RID>:<SHARED_CODE_REPO_GRADLE_SUBPROJECT>:<SHARED_CODE_REPO_VERSION>'
   }
   ```

您现在应该可以在 *依赖代码库* 中访问 *共享代码库* 中的代码了！

:::callout{theme="warning" title="警告"}
当您更新 *共享代码库* 中的代码时，您需要更新 Maven 坐标中的 `<SHARED_CODE_REPO_VERSION>`，以确保 *依赖库* 使用的是共享代码的最新版本。每次编译 *共享代码库* 时，检查 CI 输出以找到您应该引用的更新版本号。
:::

## 结论

现在，您已准备好在仓库之间共享代码。对于任何需要引用 *共享代码库* 中代码的 *依赖库*，请确保您已采取上述步骤来设置正确的权限和依赖关系。

:::callout{theme="neutral"}
与 Python 不同，代码库不支持创建 Java 库，仅支持共享 Java 仓库。这意味着标签等功能也不支持 Java。
:::

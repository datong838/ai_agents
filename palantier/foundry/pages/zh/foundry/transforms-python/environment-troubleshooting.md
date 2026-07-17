---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/environment-troubleshooting/",
  "title": "故障排查指南",
  "page_id": "environment-troubleshooting",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/environment-creation-overview/",
  "next": "/zh/foundry/transforms-python/use-python-libraries/",
  "scraped_at": "2026-07-13T06:08:10.775711+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 故障排查指南

按照本指南中的步骤调试最常见的Python环境创建问题：

* [故障排查指南](#故障排查指南)
  * [包解析时检查失败](#包解析时检查失败)
    * [新的Mamba错误信息](#新的mamba错误信息)
      * [依赖树](#依赖树)
      * [直接冲突](#直接冲突)
      * [直接依赖冲突](#直接依赖冲突)
      * [传递依赖冲突](#传递依赖冲突)
      * [解释新的错误信息](#解释新的错误信息)
    * [旧版Mamba错误信息](#旧版mamba错误信息)
      * [找不到包](#找不到包)
      * [找不到依赖](#找不到依赖)
      * [重复包错误](#重复包错误)
      * [调试权限错误](#调试权限错误)
      * [包冲突](#包冲突)
        * [调试包冲突](#调试包冲突)
        * [为什么解除版本固定不能解决解析失败？](#为什么解除版本固定不能解决解析失败)
      * [请求包无更改的失败](#请求包无更改的失败)
  * [如果您的`meta.yml`没有更改，调试缓慢](#如果您的metayml没有更改调试缓慢)
  * [如果您的`meta.yml`有更改，任务超时](#如果您的metayml有更改任务超时)
  * [构建失败和Conda错误](#构建失败和conda错误)
    * [多次下载失败](#多次下载失败)
  * [构建失败和入口点错误](#构建失败和入口点错误)
  * [需要同时包含Conda包和JAR的包](#需要同时包含conda包和jar的包)
  * [避免依赖冲突的最佳实践](#避免依赖冲突的最佳实践)
    * [避免依赖冲突的最佳实践：Python](#避免依赖冲突的最佳实践python)
      * [Python版本支持](#python版本支持)
    * [避免依赖冲突的最佳实践：除Python以外的包](#避免依赖冲突的最佳实践除python以外的包)
  * [其他问题](#其他问题)

## 包解析时检查失败

对于以下检查失败，您可以在代码库的“检查”选项卡中查看检查日志。使用这些日志，您可以发现检查失败的原因。

### 新的Mamba错误信息

Palantir通过提供更好的环境初始化错误信息格式，[贡献 ↗](https://medium.com/@AntoineProuvost/managing-conflicts-with-mamba-6a5fa10ed6a)给开源Mamba社区。截至2023年2月，Foundry服务受益于更能代表因环境失败而被侵犯的依赖树的错误信息。

#### 依赖树

在以下示例中：

```
packageA
   ├─ packageB
   └─ packageC
        └─ packageD
```

以上是一个目录结构示例，其中：

* `packageA` 是顶层包。
* `packageB` 和 `packageC` 是 `packageA` 的子包。
* `packageD` 是 `packageC` 的子包。

这种结构通常用于组织代码，以便更好地管理和维护项目。
`packageB`和`packageC`是`packageA`的**直接依赖**。`packageD`是`packageC`的直接依赖，但它是`packageA`的**传递依赖**。虽然`packageA`对`packageD`没有直接约束，但`packageA`对`packageC`的直接要求间接地对`packageD`施加了约束。请参见下面的实际示例以了解这一概念：
虽然可能一开始并不明显，`statsmodels`通过对`matplotlib`的约束间接地对`libpng`施加了约束。

#### 直接冲突

直接冲突发生在同一环境中请求不同版本的同一包时。想象一下在一个简单环境中请求`python 3.7`和`python 3.8`。这是一个**直接冲突**，将导致环境失败。新的出错信息将提供以下信息：

```
无法解决环境规范问题
以下软件包不兼容
├─ 请求并可安装 python 3.7**；
└─ 无法安装 python 3.8**，因为它与之前报告的任何可安装版本冲突。
```

这是一个关于Python环境的错误信息，指出当前环境中请求的Python版本与其他可能已安装或需要的版本不兼容。
上面的消息正确说明了 `python 3.7` 确实可以安装。然而，如果安装了该版本，任何尝试安装额外的不同版本都会导致冲突。可以通过从环境中移除任一版本的 python 约束来解决此环境。

然而，与由依赖项和传递依赖项引发的冲突相比，直接冲突是相当少见的。

#### 直接依赖冲突

[NumPy 文档 ↗](https://numpy.org/devdocs/release/1.22.0-notes.html#python-3-7-is-no-longer-supp) 特别提到 `numpy >=1.22.0` 需要 `python >=3.8`。因此，尝试创建一个同时请求 `python 3.7.*` 和 `numpy 1.22.0` 的环境将导致一个**直接依赖冲突**。以下错误消息将随之而来：

```
无法解决环境规格问题
以下软件包不兼容
├─ numpy 1.22.0** 可以通过以下潜在选项安装
│  ├─ numpy 1.22.0 需要
│  │  ├─ python >=3.9,<3.10.0a0 ，可以安装；
│  │  └─ python_abi 3.9.* *_cp39，可以安装；
│  ├─ numpy 1.22.0 需要
│  │  ├─ python >=3.10,<3.11.0a0 ，可以安装；
│  │  └─ python_abi 3.10.* *_cp310，可以安装；
│  └─ numpy 1.22.0 需要
│     ├─ python >=3.8,<3.9.0a0 ，可以安装；
│     └─ python_abi 3.8.* *_cp38，可以安装；
└─ python 3.7** 无法安装，因为没有可行的选项
   ├─ python [3.7.10|3.7.11|...|3.7.9] 与任何之前报告的可安装版本冲突；
   ├─ python [3.7.0|3.7.1|3.7.2|3.7.3|3.7.6] 需要
   │  └─ python_abi * *_cp37m，与任何之前报告的可安装版本冲突；
   └─ python [3.7.10|3.7.12|...|3.7.9] 需要
      └─ python_abi 3.7.* *_cp37m，与任何之前报告的可安装版本冲突。
```

这个错误信息表明当前的 Python 版本（3.7）不兼容 numpy 1.22.0 版本的安装要求。numpy 1.22.0 需要 Python 版本在 3.8 到 3.10 之间（不包括 3.10），而 Python 3.7 没有满足该条件的可行安装选项。因此，为了解决这个问题，您可能需要升级 Python 到兼容的版本（如 3.8、3.9 或 3.10）。
此错误消息表明 numpy 1.22.0 可以在 Python 3.8、3.9 或 3.10 上安装，但与请求的 3.7.\* 版本冲突。可以通过放宽对 Python 或 NumPy 的约束来解决此环境。例如，`python 3.8.*` 和 `numpy 1.22.0`，或 `python 3.7.*` 和 `numpy 1.*` 都会导致成功的环境。

:::callout{theme="neutral"}
为了解决环境问题，您可以假设 `python` 和 `python_abi` 版本是密切相关的。您可以通过调整 `python` 版本来调整 `python_abi` 版本，而不是在您的环境中指定 `python_abi`。
:::

#### 传递依赖冲突

同样，由于传递依赖，可能会发生包冲突。由于传递依赖的性质，仅请求少量包可能会导致在环境解决操作中添加数百个约束。考虑 `statsmodels` 包：

```
statsmodels
├─ numpy         # 数值计算库
├─ scipy         # 科学计算库
├─ matplotlib    # 绘图库
│  │  ├─ libpng      # PNG图像格式支持库
│  │  ├─ setuptools  # Python包管理工具
│  │  ├─ cycler      # 用于定义颜色循环的库
│  │  ├─ dateutil    # 日期处理库
│  │  └─ kiwisolver  # 数学表达式求解器
```

请求特定的`statsmodels`版本会对`setuptools`的允许版本施加限制，因为该包依赖于`matplotlib`。因此，如果环境请求的`statsmodels`和`setuptools`版本不兼容，则可能会发生传递依赖冲突，因为`statsmodels`本身对`setuptools`施加了限制。

例如，以下环境请求`huggingface-adapter 0.1.1*`和`transforms 1.645.0`:

```markdown
The following packages are incompatible
  ├─ huggingface-adapter 0.1.1** * is installable and it requires
  │  └─ palantir_models >=0.551.0 *, which requires
  │     └─ pyspark-src >=3.2.1,<3.3.0a0 *, which can be installed;
  │       # `huggingface-adapter` 0.1.1 可安装，它需要 `palantir_models` 版本大于等于 0.551.0，
  │       # 而 `palantir_models` 又需要 `pyspark-src` 的版本大于等于 3.2.1 且小于 3.3.0a0，
  │       # 这个版本是可以安装的。
  └─ transforms 1.645.0 * is uninstallable because it requires
     └─ pyspark-src 3.2.1_palantir.36 *, which conflicts with any installable versions previously reported
       # `transforms` 1.645.0 无法安装，因为它需要 `pyspark-src` 版本为 3.2.1_palantir.36，
       # 这个版本与之前报告的所有可安装版本冲突。
```

一开始可能不太明显为什么这两个包不兼容。错误信息有助于识别问题来自于`huggingface-adapter`的传递依赖与`transforms`对`pyspark-src`的直接依赖冲突。通过放松`transforms`或`huggingface-adapter`的约束，可以解决此环境问题，以便Mamba能够识别出一个版本对，使得`pyspark-src`的要求兼容。

#### 解释新的错误信息

下面是新mamba错误信息可能提供的所有措辞列表，如何解释这些信息，以及一些解决它们的指导：

* `以下软件包不兼容` 或 `无法安装以下软件包`：这些通常是详细错误信息的第一句话。这表明整体问题是由不兼容的版本导致的软件包冲突，或者是在安装必要软件包本身时出现的问题。
  * 如何解决：直接阅读语句下方的必要信息。
* `可以安装`：这句话通常出现在树依赖关系的顶部，意味着软件包本身可以在没有额外约束的情况下安装。然而，假设安装了这个特定版本，可能会由于其他软件包依赖与已安装版本冲突而引发一系列冲突。例如，`python 3.7** 被请求且可以安装`意味着Python 3.7可以在环境中安装。直接在此语句下列出的其他所有冲突都假定Python 3.7已安装在环境中。
* `没有可行选项`：没有可安装的版本能够符合请求环境中其他规范所施加的约束。例如，消息`python 3.7** 无法安装因为没有可行选项`表明如果不是由于另一个包或约束特别请求不同的Python版本，`python 3.7.*`的版本可以安装。
  * 如何解决：放松导致允许版本范围不在此软件包可行选项之外的软件包的约束。
* `不存在，也许是（拼写错误或）缺少通道`：未找到要安装的软件包。这可能意味着软件包被错误指定，或者没有配置的通道（代码库中的**设置 > 库**或代码工作簿中的[环境配置](/zh/foundry/administration/configure-code-workbook-profiles/#configuring-code-workbook-profiles)）包含该软件包。例如，请求一个包含`python 3.423.*`（不存在的版本）和`pthon 3.8.*`（明显的拼写错误）的环境会导致以下错误信息：

```
Could not solve for environment specs
  The following packages are incompatible
  ├─ pthon 3.8**  does not exist (perhaps a typo or a missing channel);  # "pthon" 应该是 "python" 的拼写错误
  └─ python 3.423** does not exist (perhaps a typo or a missing channel).  # "python 3.423" 应该是错误的版本号
```

在上述代码中，"pthon" 是 "python" 的拼写错误，同时 "python 3.423" 也不是一个有效的 Python 版本。可能需要检查配置文件中是否存在类似的拼写错误或版本错误。

* 如何补救：确保软件包中没有任何拼写错误，或确保所有请求的软件包都可以被环境使用。请参阅[发现Python库](/zh/foundry/transforms-python/use-python-libraries/#discover-python-libraries)，以获取如何在Foundry中搜索软件包存在的建议。

* `is installable and it requires`: 软件包及其附加版本可以在环境中安装，但会给环境带来一系列额外的约束。

* `is uninstallable because it requires`: 软件包及其附加版本无法安装，因为其某些依赖项在环境中产生了冲突。
  * 如何补救：检查消息下方列出的有问题的依赖项要求，放宽它们的约束，或放宽此特定软件包的约束。

* `is installable with the potential options`: 软件包有一系列可用的、无冲突的版本可以在环境中安装。选择其中一个版本可能会导致进一步的约束。

* `conflicts with any installable versions previously reported`: 通常与上文提到的版本形成对比，这表明已经确定的该软件包的一个`可安装`版本在其他地方已被确定，因此此版本将无法满足。

  * 如何补救：确保同一环境不会直接或间接地请求同一软件包的两个不同版本。

* `is missing on the system`: 这指的是缺失的[虚拟包↗](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-virtual.html)。某些软件包只能在特定的操作系统环境中运行。例如，[cudatoolkit ↗](https://github.com/conda-forge/cudatoolkit-feedstock/blob/main/recipe/meta.yaml#L578)软件包需要特定版本的`__cuda`，这是一个系统级功能，需要作为虚拟包存在于环境中以确保软件包可以在现有架构上运行。

* `which cannot be installed (as previously explained)`: 软件包无法安装，要么是因为前面已经描述的冲突，要么是因为另一个软件包包含的完全相同的约束已经在前面描述过。

### 旧版Mamba错误消息

以下是引入[新版Mamba错误消息](#new-mamba-error-messages)之前的旧版错误消息中的常见错误消息列表。

#### 未找到软件包

在这种情况下，没有配置的频道提供软件包`A`的依赖项。

```javascript
问题：没有提供所请求的 A.a.a.a
```

如果您固定版本的软件包不存在，可能会发生这种情况。如果是这种情况，请尝试在`meta.yml`中放宽或删除软件包的版本限制。例如，`matplotlib 1.1.1`可以变为`matplotlib`。

如果您收到此出错，则可以按照以下特定应用程序的说明添加您的软件包：

* [了解更多关于如何在**代码库**中添加软件包。](/zh/foundry/transforms-python/use-python-libraries/#discover-and-use-python-libraries)
* [了解更多关于如何在**代码工作簿**中添加软件包。](/zh/foundry/transforms-python/environment-creation-overview/)

![foundry-add-dependencies](../../../images/foundry/transforms-python/foundry-ml-add-dependencies.png)

#### 找不到依赖项

在这种情况下，软件包`A`包含一个必需的依赖项`B`，但没有任何渠道提供该依赖项。

```javascript
// 问题描述: A-a.a.a 需要 B-b.b.b，但目前没有提供 B-b.b.b。
```

请注意，`B` 可以是用户在 `meta.yml/foundry-ml/vector` 配置文件中明确请求的包，也可以是传递依赖项。

如果 `B` 无法在您的注册中安装，则可能会发生这种情况；例如，`B` 可能已被召回，因此无法安装。

如果是这种情况，请尝试移除 `A` 的固定版本，以防有一个版本的 `A` 具有其所有可用的依赖项，或者联系您的 Palantir 代表以将必要的包导入 Foundry。

#### 重复包出错

```javascript
// 无法同时安装 X.a.b.c 和 X.d.e.f
```

如果您尝试安装相同的包 `X` 并且为其设置了两个不同版本的固定，就会出现此错误。例如，如果您在 `meta.yml` 中同时固定 `python 3.9.*` 和 `python 3.10.*`，您可能会收到此错误。您可以通过删除其中一个重复的包版本固定来解决此问题。

#### 调试权限错误

```javascript
CondaService:ReadRepositoryPermissionDenied
// 表示Conda服务中读取仓库权限被拒绝的错误信息
```

如果您收到此出错信息，可能是因为您需要的所有资产和包在您的注册中不可用。一旦它们全部安装在您的注册中，请确保重新部署。

#### 包冲突

在这种情况下，包 `A` 对包 `B` 的版本有要求，但此版本的 `B` 与其他包冲突：

```javascript
// 问题描述：包 A-a.a.a 需要 B 的版本在 >=2.2.5 且 <2.3.0a0 之间，但没有可用的提供者可以安装
```

请注意，包`B`可能指的是`A`的传递依赖项，而您并未在`meta.yaml`文件中明确列为要求。有关传递依赖项的更多信息，请参阅[环境创建介绍](/zh/foundry/transforms-python/environment-creation-overview/)。

##### 调试包冲突

* 创建一个失败求解的最小示例。移除包直到环境成功解决，然后逐个添加包，直到确定哪些包是阻碍因素。
* 尝试放宽约束（移除包固定）。

  * 您可以在不同窗口中打开多个存储库或同一存储库的多个分支，以加快此过程（在代码存储库中）或配置文件中（在代码工作簿中）。
    \:::提示
    在代码工作簿中，您可以为`pandas`、`matplotlib`和`numpy`添加最低版本，以防止其默认为`pandas=0`、`matplotlib=2`和`numpy<1.20`。如果您需要高于这些默认值的版本，请导航到**环境 > 自定义Spark环境 > 自定义配置文件**，并从下拉菜单中为每个包选择一个版本，以满足您的版本要求。
    \:::

  ![更改最低版本](../../../images/foundry/transforms-python/changing-minimum-versioning.png)

  * 我们建议使用二分搜索发现问题。尝试在一个存储库中移除所有约束，在另一个存储库中移除一半约束，然后在另一个存储库中移除另一半约束，依此类推。
* 您还可以为Mamba生成的日志添加额外的详细信息，这在追踪树下的传递依赖项时可能会有所帮助（***注意：这将导致检查变慢***）。要添加详细信息，请在CI日志中找到检查失败的任务行`Execution failed for task ':transforms-python:<task-name>'.`。例如，如果失败的任务是`condaPackRun`，请在内部`transforms-python/build.gradle`文件的底部添加以下代码块：

```javascript
tasks.condaPackRun {
    // 添加附加参数 "-vvv" 用于详细输出日志信息
    additionalArguments "-vvv"
}
```

##### 为什么取消固定版本未能解决出错？

即使在完全放松限制的情况下，满足需求列表所需的软件包或软件包版本可能仍然：

* 不可用。您可以使用[软件包选项卡](/zh/foundry/transforms-python/use-python-libraries/#discover-and-use-python-libraries)检查可用的软件包和版本。如有必要，您可以联系您的Palantir代表请求添加这些软件包。
* 不兼容。即使我们可以访问所有可能发布的版本，这些软件包定义可能永远无法兼容。例如，您依赖的一个Conda软件包可能已经升级（[查看升级PRs](/zh/foundry/code-repositories/repository-settings/#repository-upgrades)）到一个已损坏的新版本。
* 与您的`meta.yml`中的Python版本不兼容。

为了检查这种情况，您可以比较与成功检查相关的[Conda锁文件](/zh/foundry/transforms-python/use-python-libraries/#conda-lock-files)和失败检查的锁文件。要访问Conda锁文件，请在设置齿轮中选择`显示隐藏文件和文件夹`选项，并导航到`transforms-python/conda-versions.run.linux-64.lock`。将成功和失败运行之间更改的库版本固定到`meta.yaml`文件中的不同版本。

#### 请求的软件包没有更改却出错

可能发生这种情况的两个主要原因：

1. 由于您的变换可能依赖于外部软件包（参见[公开管理的Conda渠道](/zh/foundry/transforms-python/use-python-libraries/#publicly-managed-conda-channels)），不幸的是，如果上游某些东西出错，它可能会出错。
2. 合并升级PR将在检查运行时触发环境的重新解析，在极少数情况下可能导致软件包解析出错，特别是在您有一个过度约束的环境时。这是因为升级PR可能带来新的依赖关系，导致环境需要重新计算。您可以通过测试如果您还原应用升级PR的提交，检查是否通过来确认升级PR是原因。然后您可以按照[上面章节](#checks-fail-during-package-resolution)的步骤重新应用升级PR。

## 如果没有更改您的`meta.yml`，如何调试缓慢问题

&#x5728;***代码库***&#x4E2D;：

1. 升级您的分支（有关更多信息，请参见[手动分支升级](/zh/foundry/code-repositories/repository-settings/#repository-upgrades)）。
2. ***如果您仍然遇到缓慢并且您在`@transform_df`标签之外进行了代码更改***，那么此代码可能导致检查变慢。评估此代码的性能（如适用）。

## 如果更改了您的`meta.yml`，任务超时

如果您在长时间运行的任务上收到内存不足（OOM）错误，这可能是由于软件包版本不兼容导致无法解决的环境。为了解决这个问题，首先升级您的分支，然后进行[上面列出的调试步骤](#debugging-a-package-conflict)。

## 使用Conda时构建失败出错

```javascript
CondaEnvironmentSetupError // Conda环境设置错误
```

如果您遇到搭建出错，解决步骤如下：

1. 检查您的[驱动程序日志](/zh/foundry/transforms-python/debugging/)以查找出错信息。
2. ***如果您更改了代码或`meta.yml`文件***（要查看此更改，请使用[任务比较](/zh/foundry/optimizing-pipelines/debug-job/#compare-jobs)工具），请将其还原，看看是否能解决搭建问题。如果还原`meta.yml`文件的更改解决了问题，那么很可能是包冲突，可以按照[上文](#debugging-a-package-conflict)描述的方法进行调试。如果您没有更改meta.yml文件，请检查您搭建的Python模块版本（如以下步骤中所述）。如果仍无法解决搭建问题，那么由于分支升级或底层升级（[查看升级PR](/zh/foundry/code-repositories/repository-settings/#repository-upgrades)）可能导致环境无法解决。在这种情况下，您应检查[上文](#debugging-a-package-conflict)中提到的调试步骤。
3. ***如果您没有做任何更改***，是否存在成功搭建时与失败搭建时运行的Python模块版本不同的情况？检查\*“Infra details”*、*“Environment”*和*“SparkModuleVersion”\*。联系您的Palantir代表，讨论恢复到此版本。

![infra-details-button](../../../images/foundry/transforms-python/infra-details-button.png)
![spark-module-version](../../../images/foundry/transforms-python/spark-module-version.png)

### 多重下载失败

```javascript
RuntimeError: Multi-download failed
// 运行时错误：多重下载失败
// 这是一个运行时错误，表示尝试进行多重下载操作时失败。
// 可能的原因包括网络连接问题、文件权限问题或目标服务器错误等。
```

此出错意味着您无权访问下载包的[artifacts channel](/zh/foundry/transforms-python/environment-creation-overview/#channel)，或者在注册时工件不可用。实际失败情况可以在[driver logs](/zh/foundry/transforms-python/debugging/)中查看。

如果您尝试为此存储库创建模板，请导航到您的[Conda channels](/zh/foundry/transforms-python/use-python-libraries/#discover-and-use-python-libraries)列表，检查列出的渠道是否有任何警告。如果列出的渠道上有警告，请按照以下步骤操作：

1. 删除损坏的渠道（如果适用，请向您的Palantir代表请求权限）。
2. 重新触发检查。
3. 重新触发搭建。

## 搭建失败及入口点错误

```javascript
transforms._errors.EntryPointError: "Key {name} was not found, please check your repo's meta.yaml and setup.py files"
// transforms._errors.EntryPointError: “未找到键 {name}，请检查您的仓库中的 meta.yaml 和 setup.py 文件”
// 该错误通常意味着在 meta.yaml 和 setup.py 中未定义某个关键的入口点。
```

此出错意味着根文件中缺少触发搭建所需的某些内容。您可能可以使用数据集预览，但搭建将失败。

要调试此问题，请检查`meta.yaml`或`setup.py`中是否缺少任何必要信息。作为参考，您可以创建一个新的Python代码仓库，并检查新仓库中的`meta.yaml`和`setup.py`文件。

在`meta.yaml`和/或`setup.py`中添加任何缺失的信息后，提交更改，等待检查成功，然后重新触发搭建。

## 需要同时使用Conda包和JAR的包

某些包需要同时使用Conda包和JAR才能可用。一个常见的例子是graphframes包（其中Conda包包含Python API，而JAR包含实际实现）。如果您只添加了Conda包，但没有添加必要的JAR，您可能会遇到以下出错：

```java
o257.loadClass.: java.lang.ClassNotFoundException:<Class>
// 这行代码表示在尝试加载一个类时，抛出了 ClassNotFoundException 异常
// 其中 `<Class>` 应该被替换为实际找不到的类名
// ClassNotFoundException 是在 Java 中表示类在运行时未找到的异常
```

或者，您可能会遇到此错误：

> **Java类路径引用错误** -
> 您使用的某个Python依赖项尝试引用类路径中不存在的Java jar。检查最近添加的Python依赖项，并在build.gradle文件中添加对必要Java包（JARs）的依赖。

此类包需要通过两步过程添加：

1. 通过[包选项卡](/zh/foundry/transforms-python/use-python-libraries/#discover-and-use-python-libraries)以正常方式将Conda包添加到存储库。
2. 在设置齿轮中选择`显示隐藏文件和文件夹`选项，并选择内部的`transforms-python/build.gradle`文件。在文件底部，添加以下块：

```gradle
dependencies {
    // 添加 Conda 仓库中指定组、名称和版本的依赖项
    condaJars '<group_name>:<name>:<version>'
}
```

如果这些软件包在单元测试中也需要使用，则需要在测试时提供。为此，请将以下代码块添加到您的gradle文件中（注意，测试插件必须在sparkJars依赖项之前声明）：

```gradle
// 应用测试插件
apply plugin: 'com.palantir.transforms.lang.pytest-defaults'

dependencies {
    // 添加 Conda 相关库的依赖
    condaJars '<group_name>:<name>:<version>'
    // 添加 Spark 相关库的依赖
    sparkJars '<group_name>:<name>:<version>'
}
```

另一个需要同时使用 Conda 包和 JAR 的外部库示例是 [Spark-NLP ↗](https://github.com/JohnSnowLabs/spark-nlp) 包。请注意，Spark-NLP 的 JAR 依赖项需要在 build.gradle 文件中添加。

首先，[将 Spark-NLP 添加为外部库](/zh/foundry/transforms-python/use-python-libraries/#discover-python-libraries)。

![spark-nlp-conda-add-button](../../../images/foundry/transforms-python/spark-nlp-conda.png)

将与您在上面添加的库版本兼容的 JAR 添加到子项目内的 build.gradle 文件中，通常是 `transforms-python/build.gradle`。例如，上述 Spark-NLP 的库版本是 5.0.2，因此在下面的步骤中，我们将添加一个满足版本期望的 JAR。通过使用格式 `<group_name>:<name>:<version>`，我们可以使用以下代码将 JAR 添加到我们的 build.gradle 脚本中：

```
// 添加依赖项
dependencies {
     // 指定 Spark NLP 库的版本和 Scala 版本
     condaJars 'com.johnsnowlabs.nlp:spark-nlp_2.12:5.0.2'
}
```

如果您不确定名称中指定的目标版本，请访问 [Maven ↗](https://mvnrepository.com/artifact/)，搜索所需的库，并找到您在 Foundry 中观察到的库版本的兼容目标版本。

## 避免依赖冲突的最佳实践

从上述提到的出错情况来看，出错的最常见原因是依赖冲突。为了减少依赖冲突，请遵循以下最佳实践。

### 避免依赖冲突的最佳实践：Python

遵循 Python 的 ***major.minor*** 版本控制。

* 在**代码库**中，Python `3.9.*`、`3.10.*` 和 `3.11.*` 是可用的。建议您不锁定 Python 版本，只需指定包名 `python`。但是，如果您的代码需要在特定版本的 Python 上运行，则应在搭建和运行部分中锁定所选版本。Python `3.8.*` 现已弃用；它仍然可以使用，但将在 2025 年 1 月后不再支持。Python `3.6.*` 和 `3.7.*` 不再支持。

![build-and-run-python-versions-same](../../../images/foundry/transforms-python/build-and-run-python-versions-same.png)

:::callout{theme="neutral"}
确保搭建和运行部分中的 Python 依赖项是相同的。Python 依赖项之间的不匹配可能导致不期望的结果和失败。

范围如 `python >=3.9` 或 `python >3.9,<=3.10.11` 不支持 Python 版本。如果使用不支持的 Python 版本，我们将默认为 Python `3.6.*`。请注意，Python `3.6.*` 已弃用，因此请确保在您的 `meta.yaml` 中为支持的 Python 版本设置有效的锁定。
:::

* 在**代码工作簿**中，您可以通过将 **自动** 更改为您需要的版本来切换版本控制。

![code-workbooks-python-versioning](../../../images/foundry/transforms-python/code-workbooks-python-versioning.png)

#### Python 版本支持

从 Python 3.9 起，Foundry 将遵循 [Python End Of Life ↗](https://devguide.python.org/versions/) 定义的时间表，这意味着如果某个 Python 版本被宣布为终止支持，该版本将不会在平台上得到支持。查看 [Python 版本](/zh/foundry/transforms-python/python-versions/) 页面以获取更多详细信息。

### 避免依赖冲突的最佳实践：除 Python 以外的包

避免显式锁定版本，因为这可能导致依赖冲突。即使是 *major.minor* 版本也可能导致冲突。

:::callout
请注意，在代码工作簿中，您可以为 `pandas`、`matplotlib` 和 `numpy` 添加最低版本控制，因为代码工作簿将在自动设置中默认为 `pandas=0`、`matplotlib=2` 和 `numpy<1.20`。
:::

## 其他问题

如果上述指导不足以解决您的问题，或者如果您遇到了本指南范围之外的问题，请联系您的 Palantir 代表，并提供您尝试的任何调试步骤的详细信息。

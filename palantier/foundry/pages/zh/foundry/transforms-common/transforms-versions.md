---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-common/transforms-versions/",
  "title": "变换版本",
  "page_id": "transforms-versions",
  "category_id": "data-integration",
  "section_id": "transforms-common",
  "previous": "/zh/foundry/transforms-common/local-preview/",
  "next": "/zh/foundry/time-series/time-series-overview/",
  "scraped_at": "2026-07-13T06:09:15.260447+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 变换版本

在变换中，使用的Spark和Java版本取决于搭建过程中变换的版本。变换会在后台自动升级，以确保任务始终与最新的安全性和性能改进保持一致。根据[Spark版本政策 ↗](https://spark.apache.org/versioning-policy.html)，API在版本之间保持一致，并启用旧版配置以防止行为变化。这些配置在[Spark迁移指南 ↗](https://spark.apache.org/docs/latest/sql-migration-guide.html)中有记录。

## 发布

使用的版本在下表中列出。

### Python

| 变换版本	       | Spark版本	    | Java版本	 |
|------------------|----------------|-------------|
| 1.1048.0+	       | 3.4.1	        | 17	         |
| 2.0.0+	          | 3.5.1	        | 17	         |

### Java

| 变换版本	       | Spark版本	    | Java版本	 |
|------------------|----------------|-------------|
| 1.1015.0+	       | 3.4.1	        | 17	         |
| 2.0.0+	          | 3.5.1	        | 17	         |

### SQL

| 变换版本	       | Spark版本	    | Java版本	 |
|------------------|----------------|-------------|
| 1.861.0+	        | 3.4.1	        | 17	         |
| 2.0.0+	          | 3.5.1	        | 17	         |

## 环境页面

环境页面可以从任务追踪器中通过选择**Spark Details > Environment**访问。在这里，您可以看到搭建的关键配置详情，包括变换和Spark版本。

`sparkModuleVersion`对应于变换版本，`sparkVersion`对应于搭建中使用的Spark版本。

![在环境页面查看变换和spark版本](../../../images/foundry/transforms-common/environment-page.png)

## 运行时版本控制

每次运行搭建时都会选择一个变换的运行时版本。一个称为“裁定”的系统用于确保您的搭建不会升级到一个不再有效的版本；裁定过程有选择地测试升级，并在必要时回退到旧版本。当有新的Spark版本出现时，它将被自动测试并在可行的情况下在您的管道中实现，无需用户干预。如果升级不成功，您的管道将继续在旧的Spark版本上运行。每次Spark版本升级将与[公告](/zh/foundry/announcements/)一起发布。要暂时停留在现有的Spark版本上，请使用[模块固定](/zh/foundry/code-repositories/module-pinning/)将管道固定到一个固定的版本。

在运行时版本发布大约一个月后，将发送仓库升级提示以通知用户无法自动升级的问题。您应该能够根据仓库中的检查出错来调试这些情况。

## 调试任务

如果您怀疑变换升级导致管道中断，请使用调试任务诊断问题。在失败的任务上，选择**操作**和**重新运行为调试任务**以指定一个先前成功的版本，并确认变换版本的更改是导致中断的原因。如果遇到变换升级破坏管道的情况，请联系Palantir客服支持以获得进一步帮助。

![在设定版本上运行调试任务](../../../images/foundry/transforms-common/debug-job.png)

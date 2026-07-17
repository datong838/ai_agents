---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/compute-modules/deploying-compute-module/",
  "title": "部署计算模块",
  "page_id": "deploying-compute-module",
  "category_id": "data-integration",
  "section_id": "compute-modules",
  "previous": "/zh/foundry/compute-modules/authoring-locally-python/",
  "next": "/zh/foundry/data-lineage/overview/",
  "scraped_at": "2026-07-13T06:02:07.927404+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 部署计算模块

:::callout{theme="warning" title="Beta"}
计算模块功能处于测试阶段，可能并非所有注册用户都可以使用。如果您的注册中可以使用计算模块，请导航至计算模块应用程序以获取最新文档。
:::

## 先决条件

本节假定您已经创建了一个计算模块Docker容器。如果没有，您可以按照指南[创建一个基础的Python计算模块](/zh/foundry/compute-modules/authoring-locally-python/)。

## 将您的计算模块发布到Foundry

1. 首先导航到Foundry中您希望放置计算模块的项目。
2. 选择 **New** -> **Artifacts Repository**。
3. 在 **Publish** 部分，从下拉菜单中选择 **Docker**。

![Artifacts Repository](/resources/foundry/compute-modules/artifacts-docker-repository.png)

4. 在 **Parameters** 下更改 **Image Name** 为您的Docker镜像名称。

:::callout{theme="warning"}
计算模块不支持使用标签 `latest`。
:::

5. 按照屏幕上的说明将您的镜像发布到存储库。
6. 将您的镜像发布到存储库后，返回概览页面，您应该在1-2分钟内看到您的镜像显示出来。

![Artifacts Docker Image View](/resources/foundry/compute-modules/artifacts-docker-image-view.png)

## 配置您的计算模块

现在您已在Foundry中拥有Docker镜像，您可以准备将其作为计算模块运行。

1. 导航到Foundry中您希望放置计算模块的项目。
2. 选择 **New** -> **Compute Module**。
3. 导航到 **Configure** 标签。

![Compute Module Configure](/resources/foundry/compute-modules/compute-module-configure.png)

4. 选择 **Add Container**。
5. 输入一个名称，如 `mycomputemodule`。请注意，名称必须是小写的，且不能包含空格或除 `-` 之外的特殊字符。
6. 选择您在上一步中发布Docker镜像的存储库。
7. 选择您要运行的镜像和镜像的标签。

![Compute Module Container](/resources/foundry/compute-modules/compute-module-container.png)

8. 选择 **Confirm**。
9. 在 **Runtime** 下，确保选择了 **Runtime V1**。
10. 对于这个示例计算模块，您不需要挂载任何卷、添加任何外部访问或更改任何缩放限制。
11. 选择 **Save**。

![Fully Configured Compute Module](/resources/foundry/compute-modules/fully-configured-compute-module.png)

您的计算模块现在已准备好启动。

## 运行您的计算模块

1. 导航到计算模块的 **Overview** 标签。
2. 选择 **Start**。
3. 等待您的计算模块进入 **Running** 状态。

![Running compute module](/resources/foundry/compute-modules/running-compute-module.png)

## 查询您的计算模块

现在您的计算模块正在运行，您可以通过发送测试查询来验证模块是否正常工作。

1. 在概览屏幕底部选择 **Query** 标签。

![Query Compute Module](/resources/foundry/compute-modules/query-compute-module.png)

2. 输入您的计算模块的函数名称。该函数名称将在请求中传递给您的计算模块，因此可能因计算模块而异。对于您在[前一节](/zh/foundry/compute-modules/authoring-locally-python/)中构建的计算模块，支持的查询是 `divide` 和 `multiply`。
3. 输入要执行上述指定函数的值。
4. 选择 **Run**，您应该会看到计算模块的结果。请注意，如果启用了缩放至零，则首次查询可能需要一些时间。

   ![Multiply Query Result](/resources/foundry/compute-modules/multiply-query-compute-module.png)

计算模块可以提供多种函数服务；上面的示例执行了 `multiply`，但也可以调用函数 `divide`。

![Divide Query Result](/resources/foundry/compute-modules/divide-query-compute-module.png)

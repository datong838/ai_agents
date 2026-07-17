---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/compute-modules/authoring-locally-python/",
  "title": "创建Python计算模块",
  "page_id": "authoring-locally-python",
  "category_id": "data-integration",
  "section_id": "compute-modules",
  "previous": "/zh/foundry/compute-modules/authoring-locally-overview/",
  "next": "/zh/foundry/compute-modules/deploying-compute-module/",
  "scraped_at": "2026-07-13T06:02:34.949139+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 创建Python计算模块

:::callout{theme="warning" title="测试版"}
计算模块功能处于测试阶段，可能并不适用于所有注册。如果您的注册中可用计算模块，请导航至计算模块应用程序以获取最新文档。
:::

本教程提供了如何创建运行Python的基础计算模块的逐步演练。

## 前提条件

* 必须安装Docker客户端
* 必须安装Python

## 编写计算模块

1. 首先为您的计算模块创建一个新目录。
2. 在目录中创建一个名为`Dockerfile`的文件。
3. 将以下内容复制并粘贴到Dockerfile中：

```python
# 根据您的Foundry资源队列更改平台
FROM --platform=linux/amd64 python:latest  # 指定使用amd64平台的最新Python镜像

COPY requirements.txt .  # 将requirements.txt文件复制到镜像中
RUN pip install -r requirements.txt  # 使用pip安装requirements.txt中列出的所有依赖包
COPY src .  # 将src目录中的所有内容复制到镜像中

# 这是在Foundry中运行计算模块所需的
USER 5000  # 以用户ID 5000运行容器，通常用于非root用户环境
CMD ["python", "app.py"]  # 执行app.py脚本作为容器启动命令
```

4. 创建一个名为 `requirements.txt` 的新文件。此文件指定了我们Python应用程序的依赖项。将以下内容复制并粘贴到文件中:

```
requests == 2.31.0
```

这是一个Python包管理工具`pip`的需求文件中的一行，指定了需要安装的`requests`库的版本为2.31.0。

* `requests` 是一个用于发送HTTP请求的流行Python库。
* `2.31.0` 是特定的版本号，确保项目使用的是该版本以避免兼容性问题。

5. 创建一个名为 `src` 的新子目录。我们将在这里放置我们的 Python 应用程序。
6. 在 `src` 目录中，创建一个名为 `app.py` 的文件。
7. 现在您的目录应该如下所示：

```
MyComputeModule
|- Dockerfile           # Docker容器配置文件，用于定义镜像构建过程
|- requirements.txt     # Python项目依赖文件，列出所需的库及其版本
|- src                  # 源代码目录
   |- app.py            # 主应用程序文件，包含主要逻辑
```

8. 在 `app.py` 中复制并粘贴以下代码：

```python
import requests
import os
import time
import logging as log
import json

log.basicConfig(level=log.INFO)

# 从环境变量中获取证书路径
certPath = os.environ['CONNECTIONS_TO_OTHER_PODS_CA_PATH']

# 从环境变量中读取模块认证令牌
with open(os.environ["MODULE_AUTH_TOKEN"], 'r') as f:
    moduleAuthToken = f.read()

# 获取工作任务的URI
getJobUri = "https://localhost:8945/interactive-module/api/internal-query/job"
# 提交结果的URI
postResultUri = "https://localhost:8945/interactive-module/api/internal-query/results"


# 从运行时获取任务。当状态码为200时表示存在任务。
# 如果返回204状态码则再次尝试获取。
# 该接口启用了长轮询，可以无限制调用。
def getJobBlocking():
    while True:
        response = requests.get(
                getJobUri,
                headers={"Module-Auth-Token": moduleAuthToken},
                verify=certPath)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 204:
            log.info("No job found, trying again!")

# 根据类型处理查询
def get_result(query_type, query):
    if query_type == "multiply":
        return float(query) * 2  # 如果类型是“multiply”，则将查询值乘以2
    elif query_type == "divide":
        return float(query) / 2  # 如果类型是“divide”，则将查询值除以2
    else:
        log.info(f"Unknown query type: {query_type}")  # 未知的查询类型

# 将任务结果提交到运行时。所有接收到的任务都必须提交结果，
# 否则可能不会有新的任务被分配到这个工作节点。
def postResult(jobId, result):
    response = requests.post(
            f"{postResultUri}/{jobId}",
            data=json.dumps(result).encode('utf-8'),
            headers={"Module-Auth-Token": moduleAuthToken, "Content-Type": "application/octet-stream"},
            verify=certPath)
    if response.status_code != 204:
        log.info(f"Failed to post result: {response.status_code}")

# 无限循环尝试
while True:
    try:
        job = getJobBlocking()
        v1 = job["computeModuleJobV1"]
        job_id = v1['jobId']
        query_type = v1['queryType']
        query = v1['query']
        result = get_result(query_type, query)
        postResult(job_id, result)
    except Exception as e:
        log.info(f"Something failed {str(e)}")
        time.sleep(1)  # 出现异常时，等待1秒后重试
```

9. 运行 `docker build -t mycomputemodule:0.0.1 .` 以创建名为 `mycomputemodule` 的 Docker 镜像。

:::callout{theme="warning"}
计算模块不支持标签 `latest`。
:::

您现在已成功创建可以在 Foundry 中运行的计算模块。

要在 Foundry 中运行您的容器，请继续阅读关于如何[部署计算模块](/zh/foundry/compute-modules/deploying-compute-module/)的教程。

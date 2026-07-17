---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/sap/install-sap-fixpack/",
  "title": "安装修补包",
  "page_id": "install-sap-fixpack",
  "category_id": "data-integration",
  "section_id": "sap",
  "previous": "/zh/foundry/sap/install-sap-support-package/",
  "next": "/zh/foundry/sap/configure-sap-slt/",
  "scraped_at": "2026-07-13T05:38:34.022291+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 安装修补包

:::callout{theme="neutral"}
修补包仅对指定的SP级别有效。
:::

## 安装

Palantir Foundry Connector 2.0 以SAP应用程序（"Connector"）SPxx修补包的形式作为SAP请求发布，通过SAP传输管理系统进行传输。请按照以下步骤将请求导入SAP系统。

1. [下载安装包](/zh/foundry/sap/download-sap-addon/)。
2. 将Connector SPxx修补包解压到一个文件夹中。文件如下（请求号可能因要安装的版本而异）：

* Connector文件
  * `K900xxx.D04`
  * `R900xxx.D04`
* 远程代理文件
  * `K900xxx.D02`
  * `R900xxx.D02`

3. 文件名以"R"开头的是**数据文件**；文件名以"K"开头的是**控制文件**。将文件分别复制到SAP应用服务器上相应的文件夹中：

```
    /usr/sap/trans/cofiles
    /usr/sap/trans/data
```

4. 使用有权使用STMS（SAP传输管理系统）的用户登录SAP系统。
5. 运行`STMS`事务。
6. 选择传输的目标系统。
7. 从工具栏菜单中选择**附加功能** > **其他请求** > **添加**，然后输入请求号。请求号的格式如下：`D04K9000xx`。前三位是请求文件扩展名；其余的数字是解压文件中看到的K文件名。
8. 请求列在导入队列中。通过选择请求号选择请求，然后在工具栏上选择**导入**。
9. 转到**选项**选项卡，选择**稍后导入时保留传输请求在队列中**和**忽略无效组件版本**。然后，开始传输。
10. 通过选择工具栏上的日志按钮检查导入日志。
11. 检查是否有任何错误信息。成功的导入应无错误完成。

---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-connection/source-exploration/",
  "title": "源探索",
  "page_id": "source-exploration",
  "category_id": "data-integration",
  "section_id": "data-connection",
  "previous": "/zh/foundry/data-connection/set-up-source/",
  "next": "/zh/foundry/data-connection/set-up-sync/",
  "scraped_at": "2026-07-13T05:31:41.165301+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 源探索

在从源设置同步时，您可能希望探索源及其包含的数据，以便在将数据引入Foundry之前预览同步。根据源类型，Data Connection允许您通过**探索**页面预览同步中的数据。

要访问**探索**页面，请按照以下步骤操作：

1. 导航到**源**页面，点击您要配置的源名称。
2. 从同步页面的**探索和创建同步**组件中选择**探索**链接。

![数据库探索器](../../../images/foundry/data-connection/db-explorer.png)

## 基于表格的数据

1. **左侧面板：** 从源系统中查找并添加表和视图到图中。使用自由文本搜索助手查找特定表，或浏览树以查找资源。

2. **图：** 探索表和视图及其之间的关系。您也可以通过右键单击表格从图中创建同步。当选择具有关系的表时，外键将在可展开的列列表中突出显示，并在链接上方显示。
   * 请注意，图不总是可用于基于表格的数据探索。例如，对于基于表格的REST API模型的探索，由于没有明确的对象关系，图将不会出现。

3. **表详情：** 预览所选表的样本。

4. **右侧面板：** 查看所选表，并为表创建同步。

## 基于文件的数据

1. **左侧面板：** 探索并选择包含要同步到Foundry的内容的目录。

2. **预览：** 查看将被同步的文件预览。可以添加筛选来控制哪些文件被导入到Foundry。

3. **右侧面板：** 查看所选表，并为表创建同步。

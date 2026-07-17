---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/building-pipelines/compass-file-lister/",
  "title": "Compass 文件列出器",
  "page_id": "compass-file-lister",
  "category_id": "data-integration",
  "section_id": "building-pipelines",
  "previous": "/zh/foundry/building-pipelines/create-a-connected-flow/",
  "next": "/zh/foundry/building-pipelines/recommended-project-structure/",
  "scraped_at": "2026-07-13T05:41:50.750245+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Compass 文件列出器

Compass 文件列出器是一种自动化工具，用于将给定**输入文件夹**中资源的 rid（资源标识符）列入代码库中。运行时，将在**输出库**中打开一个新的拉取请求，它将创建文件或覆盖现有文件。生成的文件默认存储在以下路径：`compass-lister/rids.json`。查看[创建连接流](/zh/foundry/building-pipelines/create-a-connected-flow/)以获取逐步指南。

## 配置选项

* 你可以通过在配置块中设置 `generated_file_path` 来覆盖输出库中的基本路径。如果将其设置为 `transforms-python/generated`，则输出将写入 `transforms-python/generated/rids.json`。

* 如果在配置块中将 `merge_when_ready` 设置为 `true`，则可以允许生成的 PR 自动合并。查看你的输出库设置以审查允许 PR 合并的条件。

### 配置示例

```json
{
  "generated_file_path": "transforms-python/generated", // 生成文件的路径
  "merge_when_ready": true // 当准备好时自动合并
}
```

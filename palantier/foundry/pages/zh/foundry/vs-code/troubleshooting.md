---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/vs-code/troubleshooting/",
  "title": "故障排除",
  "page_id": "troubleshooting",
  "category_id": "data-integration",
  "section_id": "vs-code",
  "previous": "/zh/foundry/vs-code/overview/",
  "next": "/zh/foundry/palantir-extension-for-visual-studio-code/overview/",
  "scraped_at": "2026-07-13T06:01:44.957105+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 故障排除

本页面包含在使用 Visual Studio Code 的 Palantir 扩展时可能遇到问题的故障排除提示。

## Code Workspaces 出错

Palantir 平台中的 VS Code 使用 Code Workspaces 基础设施；有关更多信息，请参阅 [Code Workspaces 故障排除页面](/zh/foundry/code-workspaces/troubleshooting/)。

## VS Code 工作区加载失败或显示空白屏幕

如果 VS Code 加载失败或仅显示空白屏幕，可能是浏览器缓存出现问题。在这种情况下，请执行浏览器页面的强制重新加载以解决您的问题。

* 按住 `Cmd`（macOS）或 `Ctrl`（Windows），然后选择 **重新加载**。
* 使用 `Cmd+R`（macOS）或 `Ctrl+R`（Windows）重新加载。
* 在 Chrome 中，通过导航到 **视图 > 开发者 > 开发者工具** 或使用 `F12` 键打开 **开发者工具** 面板。然后，右键单击搜索栏左侧的 **重新加载** 按钮，选择 **清空缓存并进行硬重载**。

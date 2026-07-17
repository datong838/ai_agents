---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/linter/sweep-schedules/",
  "title": "扫描计划",
  "page_id": "sweep-schedules",
  "category_id": "data-integration",
  "section_id": "linter",
  "previous": "/zh/foundry/linter/rules/",
  "next": "/zh/foundry/linter/impact-tracking/",
  "scraped_at": "2026-07-13T06:05:03.560474+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 扫描计划

Linter扫描计划是一种Linter配置，用于定义以下内容：

* **资源范围**：将根据计划被扫描的Foundry资源集。
* **规则范围**：将在资源范围上运行的一组规则。

扫描计划必须属于一个[空间](/zh/foundry/platform-security-management/manage-orgs-and-spaces/#space)，并且规则将在属于该空间的项目中的Foundry资源上运行。您可以从[控制面板](/zh/foundry/administration/control-panel/)的**Spaces**标签下的注册设置中查看、编辑或创建新的Linter配置。在列出的空间上的**操作**下拉菜单中的**Linter配置**选项可用于配置扫描计划。

**Linter配置**页面列出了现有的扫描计划。在这里，您可以查看最近扫描的状态并创建新的扫描计划。每个计划都可以从**操作**下拉菜单中编辑、暂停、触发或删除。

![显示其状态、操作和最近扫描的示例扫描计划](../../../images/foundry/linter/sweep-schedules.png)

您还可以通过选择**最近扫描**查看最近10次扫描的详细状态。

![显示开始和结束时间及持续时间的扫描状态示例列表。](../../../images/foundry/linter/sweep-status.png)

## 编辑扫描计划

<img src="../../foundry-docs/linter/media/sweep-schedule-edit.png" alt="Sweep schedule edit form" width="600" />

您可以在**编辑扫描计划**页面中编辑计划元数据，如名称和描述，并更改规则范围。

### 规则范围

规则范围允许用户定义将由扫描计划使用的[规则](/zh/foundry/linter/rules/)。定义规则范围有三种方式：

* **规则预设**：一组推荐规则，可以批量添加。例如，添加`PIPELINE_COST_RULES`预设会添加所有与成本相关的规则。
* **规则**：您可以多选特定规则以包含在规则范围中。
* **排除规则**：您可以指定要从扫描计划中移除的规则。

操作顺序遵循上述顺序：首先应用规则预设，然后添加单个规则，最后从规则范围中移除排除的规则。

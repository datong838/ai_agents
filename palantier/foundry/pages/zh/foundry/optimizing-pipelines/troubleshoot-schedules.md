---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/optimizing-pipelines/troubleshoot-schedules/",
  "title": "排查计划",
  "page_id": "troubleshoot-schedules",
  "category_id": "data-integration",
  "section_id": "optimizing-pipelines",
  "previous": "/zh/foundry/optimizing-pipelines/troubleshoot-ooms/",
  "next": "/zh/foundry/optimizing-pipelines/spark-concepts/",
  "scraped_at": "2026-07-13T05:43:53.065356+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 排查计划

### 调度器指标页面

开始排查计划问题的最佳方法之一是查看[调度器指标页面](/zh/foundry/building-pipelines/view-modify-schedules/#view-metrics)。指标页面可以告诉您失败的原因，包括常见的失败模式，例如：

* [计划的搭建失败](#scheduled-builds-are-failing)。您将在`运行历史`选项卡中看到失败搭建的证据，点击这些搭建将导航到搭建应用程序中的搭建报告以查看完整日志。
* [计划的搭建被忽略](#scheduled-builds-were-ignored)。对于任何触发但未搭建的任务，`运行历史`选项卡将在状态列中显示`忽略`。
* [计划未按预期时间或节奏触发](#schedule-failing-to-trigger)。在这种情况下，`运行历史`选项卡可能不会显示预期触发的搭建。

`版本`选项卡显示过去的计划版本和编辑，如果您的计划突然开始表现得与预期不同，这可能会有所帮助。检查是否有任何与此更改相关联的计划版本更改，并考虑将您的计划恢复到先前正常工作的状态。

### 计划搭建失败

您可以通过检查[调度器指标页面](/zh/foundry/building-pipelines/view-modify-schedules/#view-metrics)上的`运行历史`选项卡来验证计划是否按预期时间触发。

如果计划已触发，但随后搭建出错，您可以按照[调试指导](/zh/foundry/optimizing-pipelines/debug-job/)进行调试。

如果未设置适当的权限，计划也会无法搭建。计划的权限取决于计划所在的词元模式。有关详细信息，请参阅[项目范围的计划](/zh/foundry/data-integration/schedules/#project-scope)。

### 计划搭建被忽略

您可以通过检查[调度器指标页面](/zh/foundry/building-pipelines/view-modify-schedules/#view-metrics)上的`运行历史`选项卡来验证计划是否按预期时间触发。这通常也会给出计划被忽略的原因。

#### 所有数据集都是最新的

如果所有目标数据集都是最新的，即如果它们的输入自上次在该数据集上的搭建后没有更新，则计划运行将被忽略。如果是这种情况，您将在`运行历史`选项卡中看到此原因。在[计划编辑器](/zh/foundry/building-pipelines/create-schedule/#navigate-to-the-schedule-editor)中，导航到计划列表。然后，您将有选项按`过期`来为数据沿袭图上色，这将为您提供哪些任务规格被视为过期的概览。

在特殊情况下，可以使用[高级设置](/zh/foundry/building-pipelines/create-schedule/#advanced-settings)中的`强制搭建`选项来覆盖此行为，尽管在这些情况下之外这样做在计算上是浪费的。如果任何目标数据集是通过留声机同步、通过API调用变换或数据连接同步搭建的，则它们可能不会显示为过期，可能需要启用`强制搭建`选项才能运行计划。

### 计划搭建数据集的子集

如果计划仅触发数据集的子集，您将在[调度器指标页面](/zh/foundry/building-pipelines/view-modify-schedules/#view-metrics)上的`运行历史`选项卡中看到证据。

其中一个原因是只有数据集的子集是过期的。调度器将仅搭建过期的数据集，而那些最新的数据集将在搭建过程中被忽略。有关更多排查细节，请参阅[所有数据集都是最新的](#all-datasets-are-up-to-date)。如果所有这些数据集都是最新的，则搭建被`忽略`的情况会发生。

另一个原因可能是数据集未包含在搭建的数据集图中。在[计划编辑器](/zh/foundry/building-pipelines/create-schedule/#navigate-to-the-schedule-editor)中，当选择一个计划时，待搭建的数据集在数据沿袭图中会被高亮显示。数据集选择取决于[搭建类型](/zh/foundry/building-pipelines/create-schedule/#build-type)。如果使用`连接搭建`，您尤其需要注意验证是否存在连接数据集，以便在多个分支上使用相同数据集的计划。

### 计划未触发

您可以通过检查[调度器指标页面](/zh/foundry/building-pipelines/view-modify-schedules/#view-metrics)上的`运行历史`选项卡来验证计划是否按预期时间触发。一些常见的调试步骤包括：

* 检查[计划是否未暂停](/zh/foundry/building-pipelines/view-modify-schedules/#pause-a-schedule)。暂停的计划在未取消暂停之前不会触发。
* 检查[计划触发配置](/zh/foundry/building-pipelines/triggers-reference/)。如果之前成功过，请检查计划历史以查看触发器是否最近发生了更改。
* 如果计划使用事件触发器，验证预期事件是否实际发生。例如，如果搭建应在输入更新时触发，请检查输入上的最后一次搭建是否成功，并且此搭建上的事务是否在[数据集预览历史视图](/zh/foundry/dataset-preview/overview/)中成功提交。

### 计划重试与配置不同

请注意，并非所有类型的失败都可重试。当计划运行时，重试次数将被限制为管理员配置的最大值。有关更多信息，请参阅[高级设置](/zh/foundry/building-pipelines/create-schedule/#advanced-settings)。

### 计划因JobSpecInputsTrashed或JobSpecOutputsTrashed失败，或数据沿袭警告某些数据集被删除

这意味着计划包含或读取了被删除的资源。您可以执行以下操作之一来解决：

* 从回收站中恢复被删除的数据集。
* 从计划中排除被删除的数据集。如果该数据集在计划中用作另一个下游数据集的输入，您还需要执行以下操作之一：
  * 将下游数据集与被删除的数据集一起排除。
  * 修改下游数据集的逻辑，使其不再将被删除的数据集作为输入。

### 调度器权限

如果您遇到无法编辑计划的问题，项目范围权限可能是根本原因。

要在[项目范围模式](/zh/foundry/data-integration/schedules/#project-scope)中编辑计划，用户必须拥有目标数据集的`编辑`权限、触发数据集的`查看`权限和计划所定位项目的`编辑`权限。如果有一个数据集您已经失去了权限，请在保存更改之前从计划中移除此数据集。

要编辑、删除或暂停计划，用户需要对目标数据集和计划所定位项目拥有`编辑`权限。要查看计划，用户需要对目标数据集拥有`查看`权限。

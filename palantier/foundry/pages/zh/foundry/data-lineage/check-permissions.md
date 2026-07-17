---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-lineage/check-permissions/",
  "title": "检查资源权限",
  "page_id": "check-permissions",
  "category_id": "data-integration",
  "section_id": "data-lineage",
  "previous": "/zh/foundry/data-lineage/manage-schedules/",
  "next": "/zh/foundry/data-lineage/see-impact-marking-changes/",
  "scraped_at": "2026-07-13T06:04:51.178707+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 检查资源权限

您可以使用数据沿袭通过"权限"着色选项检查用户查看数据集或制品的权限。为此，请首先在图中添加节点。您可以使用侧面板上的搜索助手来完成此操作。

![在图中添加节点](../../../images/foundry/data-lineage/data_lineage_permissions_1.gif)

然后展开图以查看通向您的资源的沿袭（阅读更多关于[探索沿袭](/zh/foundry/data-lineage/explore-lineage/)的信息）。

![展开图以查看沿袭](../../../images/foundry/data-lineage/data_lineage_permissions_2.gif)

完成此操作后，使用**节点颜色选项**下拉菜单选择**权限**配色方案。

![选择权限配色方案](../../../images/foundry/data-lineage/data_lineage_permissions_3.gif)

从**以...查看**下拉菜单中选择用户的姓名。这样您就可以看到用户对图中每个节点的权限。

![从下拉菜单中选择用户名](../../../images/foundry/data-lineage/data_lineage_permissions_4.gif)

您可以按两种权限类型进行着色：

* [数据集中的数据访问](#data-access-in-datasets)
* [资源访问](#resource-access)

![节点着色的权限类型](../../../images/foundry/data-lineage/data_lineage_permissions_5.png)

### 数据集中的数据访问

使用此选项来排查权限问题。请记住，用户的数据访问受数据沿袭影响（参见[平台安全性](/zh/foundry/security/checking-permissions/)）。通过根据用户对数据的访问权限为节点着色，您可以轻松查看可能限制用户访问数据的上游数据集。

请注意，此选项仅适用于数据集节点。

### 资源访问

这将使您可以看到为选定用户在选定资源上设置的[角色](/zh/foundry/security/projects-and-roles/)（例如编辑者、只读等）。

使用此选项查看用户对您的制品的访问级别。

:::callout{theme="neutral"}
角色与数据沿袭的对应关系与数据访问不同。例如，用户在轮廓分析中为"编辑者"并不保证他们有权限查看分析所依赖的数据。在与用户共享资源时，确保他们可以访问基础数据。
:::

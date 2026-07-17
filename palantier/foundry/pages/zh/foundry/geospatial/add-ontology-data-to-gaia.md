---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/geospatial/add-ontology-data-to-gaia/",
  "title": "将Ontology数据添加到Gaia",
  "page_id": "add-ontology-data-to-gaia",
  "category_id": "data-integration",
  "section_id": "geospatial",
  "previous": "/zh/foundry/geospatial/ontology/",
  "next": "/zh/foundry/geotemporal-series/overview/",
  "scraped_at": "2026-07-13T06:22:58.185179+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 将Ontology数据添加到Gaia

您可以通过多种方法将配置为Foundry Ontology一部分的地理空间数据添加到Gotham的Gaia应用程序中，这取决于您的应用案例。为了使Foundry Ontology数据在Gotham中可访问，您需要通过Foundry的[Ontology Manager](/zh/foundry/ontology-manager/overview/)进行类型映射，建立跨两者的Ontology统一表示。

:::callout{theme="neutral"}
类型映射是Foundry和Gaia之间*所有*工作流的前提条件。您可以参考Foundry的Ontology文档中的详细[类型映射](/zh/foundry/object-link-types/enable-gotham-integration/)说明。
:::

## 比较将Foundry数据添加到Gaia的可用方法

一旦在Foundry中进行了对象类型的类型映射以启用Gotham集成，您可以使用六种方法之一将Foundry Ontology中的数据添加到Gaia：

* [拖放](#drag-and-drop-individual-objects-and-saved-explorations)
* [Foundry对象搜索](#search-for-your-foundry-object-type-in-gaia)
* [搜索模板](#create-a-search-template)
* [地时序列同步](#configure-a-real-time-geotemporal-series-sync-in-foundry)
* [函数支持的企业地图层](#use-a-function-backed-enterprise-map-layer)
* [版本化对象集支持的企业地图层](#use-a-versioned-object-set-backed-enterprise-map-layer)

下面的表格中提供了有关每种方法的更多信息：

|| [拖放](#drag-and-drop-individual-objects-and-saved-explorations) | [Foundry对象搜索](#search-for-your-foundry-object-type-in-gaia) | [搜索模板](#create-a-search-template) | [地时序列同步](#configure-a-real-time-geotemporal-series-sync-in-foundry) | [函数支持的企业地图层](#use-a-function-backed-enterprise-map-layer) | [版本化对象集支持的企业地图层](#use-a-versioned-object-set-backed-enterprise-map-layer) |
| ----- | ----- | ----- | ----- | ----- | ----- |----- |
| *支持的对象数量* | 一次1个对象*或*一个最多包含5,000个对象的对象集 | 5,000 | 5,000  | 5,000,000 | 5,000 | 5,000
| *数据刷新延迟* | 静态 | 静态*或*30秒 | 静态*或*30秒 | 实时 | 可配置 | 可配置
| *数据筛选功能* | 在Foundry的[Object Explorer](/zh/foundry/object-explorer/overview/)中 | 在Gaia地图的左侧面板中 | 在Gaia地图的左侧面板中 | 在Gaia地图的左侧面板中 | 在Gaia地图的左侧面板或Foundry的[Code Repositories](/zh/foundry/code-repositories/overview/)中 | 在Foundry的Object Explorer中
| *推荐的应用案例* | 快速将对象从Foundry的Object Explorer移动到Gaia中 | 执行简单的对象搜索 | 通过YAML在对象集中创建一组特定的筛选，以便在Gaia地图中重用 | 集成实时更新的大规模数据 | 利用Foundry Ontology[Functions](/zh/foundry/functions/overview/)的灵活性和强大功能 | 确保当对象从Foundry中添加或移除时地图层更新
| *用户管理前提条件* | 无 | 无 | 访问Gaia管理应用程序 | 无 | 访问Gaia管理应用程序 | 访问Gaia管理应用程序
| *实施的工作量* | 低 | 低 | 中 | 高 | 高 | 高

:::callout{theme="neutral"}
要通过搜索模板、函数支持的企业地图层或版本化对象集支持的企业地图层将Foundry数据添加到Gaia，您需要访问Gaia的管理应用程序。请联系Palantir支持团队了解有关管理应用程序访问的问题。
:::

下面的部分提供了实施每种集成方法的详细说明。

### 拖放个别对象和已保存的探索

您可以将个别对象或从已保存的探索中派生的对象集（其中可能包含多达5,000个对象）从Foundry拖放到Gaia地图上。

要将个别对象从Foundry拖放到您的Gaia地图：

1. 在Foundry中启动Object Explorer。
2. 搜索一个对象类型。
3. 在Object Explorer屏幕最右侧的**结果**面板中选择一个对象。
4. 选择Object Explorer屏幕左上角的对象图标。
5. 将对象从Foundry拖动并放置在Gaia地图的任何位置 - 您现在可以在地图上查看对象，并在左侧面板中作为一个名为`Dropped Object Layer [Date] [Time]`的默认层的一部分查看。

在您可以从Foundry拖放对象集到Gaia地图之前，必须首先从现有对象类型创建一个版本化对象集。要创建版本化对象集：

1. 在Foundry中启动Object Explorer。
2. 搜索并选择您的对象类型。
3. 选择Object Explorer屏幕顶部中间的**结果**。
4. 使用搜索栏筛选要添加到对象集的对象，通过对象类型的属性缩小选择范围。
   * 例如，如果您的对象类型捕获了由`name`属性定义的位置，您可以通过输入`where name is location_1 or where name is location_2`并在键盘上按`enter`或`return`筛选出一组选定的`location`对象。
5. 选择蓝色的**保存**按钮，将选定的对象保存为公共项目中的[**探索**](/zh/foundry/object-explorer/save-explorations/#saving-an-exploration)。

:::callout{theme="success"}
您还可以通过在对象类型的Ontology Explorer视图中直接应用对象筛选来筛选对象。
:::

<img src="../../foundry-docs/geospatial/media/ontology-explorer-save-object-set-public.png" alt="Foundry的Object Explorer中的保存探索或列表弹出窗口，允许用户将一组选定的对象保存为探索或对象集。" width=500>

创建并保存版本化对象集作为探索后，您可以按照以下步骤将其拖放到Gaia地图：

1. 从Object Explorer视图的顶部功能区中选择**新探索**。
2. 根据创建时给定的名称搜索并选择您的对象集。对象集也可能出现在Object Explorer搜索栏下的**我的探索和列表**中。
3. 选择Object Explorer屏幕左上角的对象集图标。
4. 将对象集从Foundry拖动并放置在Gaia地图的任何位置。对象将单独在地图上显示，并在左侧面板中自动嵌套在一个搜索层中，名称为您保存的探索。

![显示了一张地图，其中包含从Foundry拖放到Gaia的个别对象和对象集。](../../../images/foundry/geospatial/drag-and-drop-foundry-object-set-to-gaia-v3.png)

:::callout{theme="success"}
您还可以从Gotham中的其他对象视图将对象拖放到Gaia地图。
:::

### 在Gaia中搜索Foundry对象类型

您可以在Gaia左侧面板的**数据源**部分中搜索Foundry对象类型。此外，您可以在将对象添加到地图之前应用几何和时间筛选。要从Gaia搜索Foundry对象类型：

1. 在地图的左侧面板中选择**数据源**。
2. 根据其在Foundry中的名称搜索您的对象类型，它会出现在左侧面板底部的**对象类型**下。
3. 选择对象类型旁边的**搜索对象**。
4. 选择要添加到地图的对象，并在对象搜索面板的顶部功能区中应用任何必要的几何筛选。
   * `All`将把发现的对象类型中的所有对象添加到您的地图。
   * `View`将只添加当前地图视图中可用的对象。
   * `Draw`将添加位于您可以从搜索面板配置和添加的绘制形状内的对象。
   * `Select`使您能够从活动地图中选择一项。
5. 应用任何必要的时间筛选以加载在`Static range`或`Rolling window`内活动的对象。
6. 非必填地切换**实时更新搜索结果**，这将根据与您的筛选参数匹配的新创建对象每30秒更新您的对象或对象集。
7. 在**搜索标题**中输入对象搜索的名称并选择**搜索**。

<img src="../../foundry-docs/geospatial/media/search-for-foundry-object-in-gaia.png" alt="显示了Gaia的对象搜索面板。" width=300>

:::callout{theme="neutral"}
如果在完成Foundry中的类型映射前提条件后仍无法在Gotham中搜索对象，则可能是您的Gotham注册中未启用Foundry搜索功能。请联系Palantir支持团队以获取启用此功能的帮助。
:::

### 创建搜索模板

您可以在Gaia管理应用程序中创建搜索模板，以在通过左侧面板的**数据源**标签将Foundry对象添加到地图时预配置自定义对象搜索界面。

要创建和实施搜索模板，请启动Gaia管理应用程序并按照以下步骤操作：

1. 找到**地理搜索**面板并选择**显示**以查看您Gotham注册中的所有活动地理搜索。
2. 滚动到地理搜索列表底部并选择**添加**。
3. 为您的搜索命名并填写每个配置输入框。
   * `描述`将出现在搜索模板界面的顶部。
   * `Tab ID`将使您的地理搜索与搜索模板之间的映射成为可能。
   * `Tab 图标`将出现在用户搜索时的**数据源**标签中。
   * `模板 ID`将匹配`Tab ID`并使您的地理搜索与搜索模板之间的映射成为可能。
   * `分类`，这可能是非必填的，具体取决于您的注册。
   * `ACL组`将设置组访问权限。
4. 根据需要输入其他配置。
5. 选择顶部右侧功能区中的**预览和保存**，以在配置搜索模板之前在Gaia管理应用程序中保存您的地理搜索。

您可以参考一个示例地理搜索，它使用户能够搜索法国城市并在Gaia地图上显示其地理边界，一旦与搜索模板配对。

<img src="../../foundry-docs/geospatial/media/geosearch-search-template.png" alt="在Gaia管理应用程序中显示了配置好的地理搜索面板。">

6. 找到**搜索模板**面板并选择**显示**以查看您Gotham注册中的所有活动搜索模板。
7. 滚动到现有`templates:`的底部并插入包含您的搜索模板配置和地理搜索映射的YAML代码。您可以参考下面的示例搜索模板YAML代码块。

```yaml
- id: french_cities # 匹配 `Tab ID` 和 `Template ID` 字段，用于地理搜索。
    title: French cities # 搜索模板名称，将显示在 `Data sources` 面板中。
    query:
      queryType: AND # 定义查询类型，并插入相关的子查询。
      subqueries:
        - inputId: keyword
          queryType: KEYWORD # 使用关键字进行搜索。
        - field: object_type
          queryType: OBJECT_TYPE # 对象类型查询。
          value:
            - # Object Type 的 RID（资源标识符）
    dataSource: foundry-federation # 数据来源。
    namespaces:
      - foundry-federation # 命名空间。
    description: Search for French cities and display their boundaries. # 搜索法国城市并显示其边界。
    integratedDataSetIds: [] # 集成数据集ID，当前为空。
    inputs:
      - hint: Type a keyword... # 输入提示。
        id: keyword
        inputType: TEXTFIELD # 启用自由文本搜索。
        label: Keyword # 输入标签。
    aggregations: [] # 聚合，目前为空。
```

8. 在右上角功能区选择 **预览并保存** 来保存您的搜索模板。

您可以返回到您的 Gaia 地图以测试您的搜索模板。在左侧面板的 **数据来源** 选项卡中输入您的搜索模板名称，或从 **集成数据来源** 小节中手动选择。选择您的搜索模板以启动由您的地理搜索和 YAML 配置支持的预配置界面。使用 **关键词** 搜索栏或 YAML 代码中进行的任何其他自定义配置来搜索对象，然后在选择左侧面板底部的蓝色 **搜索** 按钮之前输入 **搜索标题**。

您的搜索结果将出现在您的 Gaia 地图上，以供进一步探索。

### 在 Foundry 中配置实时地理时间序列同步

您可以使用 Foundry 的 Pipeline Builder 从现有数据集[创建地理时间序列同步](/zh/foundry/pipeline-builder/outputs-add-geotemporal-series-output/#create-a-geotemporal-series-output)，使您能够将大规模、实时的地理时间数据添加到您的 Gaia 地图，而无需额外配置。

在 Foundry 中创建地理时间序列同步的步骤：

1. 导航到您的数据集，并确保其包含所有[前提条件字段](/zh/foundry/geotemporal-series/data-modeling/#observation-schema)以启用地理时间序列同步。

2. 选择 **所有操作** > **创建新管道** 来启动 Pipeline Builder。

3. 选择您的数据集节点，并在垂直弹出菜单的顶部选择 **变换**。

4. 搜索并选择 **构建 GeoPoint 列** 来映射您的 `latitude` 和 `longitude` 字段，并创建一个新的 `geo_point` 列。

5. 通过变换左上角的编辑框将您的变换重命名为 `创建 GeoPoint`。

6. 选择屏幕右上角的绿色箭头图标来 **保存** 您的变换。

7. 选择变换右上角的 **返回图形** 导航回您的 Pipeline Builder 图形。

8. 选择 `创建 GeoPoint` 变换节点的 **添加输出** 按钮，并选择 **新的地理时间序列同步**。下图显示了 Pipeline Builder 中可用的输出类型菜单。

9. 为您的新输出命名，并指派其 **目标命名空间**，例如 `Local System`。

10. 配置所有 **主字段** 以确保同步引用其支持数据集中的正确列。

11. 通过选择每个右侧的 `X` 图标或 **清除未映射属性** 按钮来清除所有未映射属性。

12. 在 **属性** 下将 **观察模式** 留空 - Foundry 将自动填充为您在上方 **元数据** 中为您的系列同步输出分配的名称。

13. 验证 **源系统** 在 **高级设置** 下是否映射到您的管道名称。下图描述了同步输出的所有必要配置。

14. 选择屏幕右上角的绿色箭头图标来 **保存** 您的同步。

15. 选择 **保存** 旁边的锤子图标以 **部署管道**。

16. 导航 **返回图形**。您将在 `创建 GeoPoint` 变换右侧看到一个新的地理时间序列同步输出节点，节点底部的绿色 `部署最新` 文本确认部署成功。

将新创建的地理时间序列同步添加到您的 Gaia 地图：

1. 打开 Gaia 左侧面板中的 **数据来源** 选项卡。
2. 搜索您的地理时间序列同步名称，并选择 **轨迹和观察搜索**。
3. 应用对象搜索面板顶部功能区中提供的任何必要几何筛选。
   * `All` 将添加发现的对象类型中的所有对象到您的地图。
   * `View` 仅会添加当前地图视图中可用的对象。
   * `Draw` 将添加位于您可以从搜索面板配置和添加的绘制形状内的对象到地图。
   * `Select` 使您能够从活动地图中选择一个项目。
4. 选择适当的时间窗口，选择 **历史搜索** 或 **实时馈送**。
5. 选择 **添加到地图**。

一旦您的地理时间序列同步作为 Gaia 的 **地图图层** 的一部分加载，您可以选择单个实体 - 例如特定的航线 - 并进行额外的配置。

### 使用函数支持的企业地图图层

您可以将数据作为企业地图图层（EML）的一部分添加到您的 Gaia 地图中，该图层由在 Foundry 中编写的函数支持并发布到您的 Ontology。

要创建输出对象集的[TypeScript 函数](/zh/foundry/functions/input-output-types/)以支持 Gaia EML 的现有对象类型：

1. 导航到包含您对象类型支持数据集的项目文件夹。
2. 选择 **新建** > **代码库**。
3. 在 `您正在构建什么？` 下选择 **函数** 选项，并选择 **TypeScript 函数** 作为您的语言。
4. 为您的代码库命名，并将其保存在公共项目文件夹中，以在选择屏幕底部的 **初始化代码库** 之前启用 Foundry Ontology API 访问。
5. 选择屏幕右侧的绿色 **转到 index.ts** 按钮以编写您的函数。
6. 按照嵌入在草稿 `index.ts` 文件中的编写提示并插入您自己的函数；您可以参考下面的示例代码。

```typescript
import { Function, Integer } from "@foundry/functions-api";
import { Objects, ObjectSet, ObjectTypeName };

// 定义一个名为 MyEmlFunction 的类
export class MyEmlFunction{

    // 使用装饰器 @Function() 标记此方法为函数
    @Function()
    // 定义一个名为 myFunctionName 的公共方法，返回类型为 ObjectSet<ObjectTypeName>
    public myFunctionName(): ObjectSet<ObjectTypeName> {
        // 调用 Objects 对象的 search 方法，获取 ObjectTypeName，并通过 filter 过滤
        // 过滤条件是 location 对象的 propertyTypeToSearch 属性与 "match-parameter" 完全匹配
        return Objects.search().ObjectTypeName().filter(location => location.propertyTypeToSearch.exactMatch("match-parameter"));
    }
}
```

7. 在顶部功能区选择**提交**。
8. 选择**标记版本**以将函数发布到Foundry Ontology。
9. 在Foundry Ontology管理器的**函数**选项卡中查看您新创建的函数。

接下来，启动Gaia的管理应用程序以建立一个Foundry函数支持的EML。导航到Gaia管理应用后，您可以：

1. 搜索并选择**企业地图层**页面。
2. 在页面底部选择**添加**以创建新的EML。
3. 将EML类型设置为`Foundry函数EML`。
4. 输入EML的**描述**并指明其**功能**。
5. 非必填输入一个**标签图标**。
6. 指明EML的**分类**。
7. 根据需要添加**ACL组**以限制EML访问。
8. 插入您的**函数rid**——您可以从Foundry的Ontology管理器应用程序中的函数概览选项卡中将其复制到剪贴板。
9. 非必填设置EML的**刷新间隔（秒）**——如果留空，EML将不会刷新。
10. 非必填插入一个**地理筛选属性id**，以便在您将EML添加为参考数据层时在Gaia中启用对象地理筛选；您可以使用来自您的对象类型的`geohash`属性ID。

:::callout{theme="neutral"}
您可以在Ontology Manager的对象类型**属性**页面中定位并复制属性ID；为此，请选择您的`geohash`属性右侧的省略号图标，然后选择**复制属性id**。
:::

您现在可以通过在左侧面板的**数据源**选项卡中搜索其名称，将您的Foundry函数支持的EML添加到您的Gaia地图。Gaia将EML分组为**精选数据源**下的`参考数据层`。

![显示了一个具有Foundry函数支持的EML的Gaia地图，其中包含一个集合的杂货店对象。](../../../images/foundry/geospatial/add-function-backed-enterprise-map-layer2.png)

您可以通过左侧面板或选择当前视图中的对象图标来选择或隐藏来自EML的单个对象。

### 使用版本化对象集支持的企业地图层

您可以将数据作为EML的一部分添加到您的Gaia地图中，该EML由您从Foundry Ontology中的对象类型创建的版本化对象集支持。

要创建版本化对象集，请按照[拖放单个对象和已保存的探索](#drag-and-drop-individual-objects-and-saved-explorations)部分中的说明进行操作。

要在Gaia管理应用程序中建立一个版本化对象集支持的EML，请按照[使用函数支持的企业地图层](#drag-and-drop-individual-objects-and-saved-explorations)部分中的说明进行操作。将EML类型设置为`版本化对象集EML`而不是`Foundry函数EML`；您将不需要插入**函数rid**。

您现在可以通过在左侧面板的**数据源**选项卡中搜索其名称，将您的版本化对象集支持的EML添加到您的Gaia地图中；Gaia将EML分组为**精选数据源**下的`参考数据层`。

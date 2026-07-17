---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/optimizing-pipelines/apply-spark-profiles/",
  "title": "应用Spark配置文件",
  "page_id": "apply-spark-profiles",
  "category_id": "data-integration",
  "section_id": "optimizing-pipelines",
  "previous": "/zh/foundry/optimizing-pipelines/native-acceleration/",
  "next": "/zh/foundry/optimizing-pipelines/spark-profiles-reference/",
  "scraped_at": "2026-07-13T05:44:29.500866+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 应用Spark配置文件

您可能希望对您的变换任务应用自定义Spark属性。

要将Spark属性应用于特定任务：

1. 按照指南将[Spark配置文件导入](/zh/foundry/code-repositories/spark-profiles/)到您的代码库中。
2. 按照[下面](#transforms-profile-syntax)的文档，在代码中引用变换配置文件。

您可以在[Spark配置文件参考](/zh/foundry/optimizing-pipelines/spark-profiles-reference/)部分了解可用的默认Spark配置文件的特征。

另请注意[调整Spark配置文件的推荐最佳实践](/zh/foundry/optimizing-pipelines/spark-concepts/#for-adjusting-spark-profiles)。

## 变换配置文件语法

所有[语言](/zh/foundry/building-pipelines/supported-languages/)均支持指定自定义Spark配置文件。在下面的所有情况下，设置是从左到右进行评估的。如果多个配置文件指定相同的设置，则列表末尾的配置将优先。

### Python

您可以在Python代码中使用`configure`装饰器来包装您的Transform对象，从而引用`profile1`和`profile2`配置文件。此装饰器接受一个`profile`参数，指向您的自定义变换配置文件列表：

```python
from transforms.api import configure

# 使用 @configure 装饰器配置数据转换函数的运行环境
@configure(profile=['profile1', 'profile2'])
@transform(
    # 定义输入数据集
    my_input=Input("/path/to/input/dataset"),
    # 定义输出数据集
    my_ouput=Output("/path/to/output/dataset"),
)
# 数据转换函数
def my_compute_function(my_input):
    # 直接返回输入数据集，未进行任何处理
    return my_input
```

### Java

自动注册的变换可以通过在计算函数中使用`TransformProfiles`注解在Java代码中引用`profile1`和`profile2`配置文件。此注解接收一个参数，该参数指的是自定义Spark配置文件的数组：

```java
import com.palantir.transforms.lang.java.api.TransformProfiles;

/**
* 这是一个用于自动注册的低级转换示例。
*/
public final class LowLevel {
     @Compute
     @TransformProfiles({ "profile1", "profile2" }) // 指定转换配置文件
     public void myComputeFunction(
             @Input("/path/to/input/dataset") FoundryInput myInput, // 输入数据集路径
             @Output("/path/to/output/dataset") FoundryOutput myOutput) { // 输出数据集路径
         Dataset<Row> limited = myInput.asDataFrame().read().limit(10); // 读取数据集并限制为10行
         myOutput.getDataFrameWriter(limited).write(); // 将处理后的数据集写入输出路径
     }
 }
```

或者，如果您使用手动注册，可以使用`builder`方法`transformProfiles()`:

```java
public final class MyPipelineDefiner implements PipelineDefiner {

    @Override
    public void define(Pipeline pipeline) {
        LowLevelTransform lowLevelManualTransform = LowLevelTransform.builder()
               // 设置转换配置文件列表
               .transformProfiles(ImmutableList.of("profile1", "profile2"))
               // 传入要使用的计算函数。在这里，“LowLevelManualFunction”对应于低级转换的计算函数的类名。
               .computeFunctionInstance(new LowLevelManualFunction())
               // 设置输入数据集的参数别名
               .putParameterToInputAlias("myInput", "/path/to/input/dataset")
               // 设置输出数据集的参数别名
               .putParameterToOutputAlias("myOutput", "/path/to/output/dataset")
               .build();
        // 注册低级手动转换到管道中
        pipeline.register(lowLevelManualTransform);
    }
}
```

### SQL

您可以通过为表设置 `foundry_transform_profiles` 属性，在SQL代码中引用 `profile1` 和 `profile2` 配置文件：

```sql
CREATE TABLE `/path/to/output` TBLPROPERTIES (foundry_transform_profiles = 'profile1, profile2')
    -- 创建一个新表，路径为`/path/to/output`，并设置表属性
    -- `foundry_transform_profiles`指定了转换配置文件
    AS SELECT * FROM `/path/to/input`
    -- 从`/path/to/input`路径的表中选择所有数据并插入到新创建的表中
```

这是使用替代 SQL 语法的另一个示例：

```sql
CREATE TABLE `/path/to/output` USING foo_bar OPTIONS (foundry_transform_profiles = 'profile1, profile2')
    AS SELECT * FROM `/path/to/input`;
```

这段SQL代码用于创建一个新表，并将其保存到指定路径`/path/to/output`。

* `USING foo_bar`指定了数据源或存储格式为`foo_bar`。
* `OPTIONS (foundry_transform_profiles = 'profile1, profile2')`用于设置选项，在这里特别指定了转换配置文件为`profile1`和`profile2`。
* `AS SELECT * FROM `/path/to/input\`\`表示从输入路径`/path/to/input`中选择所有数据来创建这个新表。
  请注意，目前在 ANSI SQL 模式下不支持指定自定义变换配置文件。

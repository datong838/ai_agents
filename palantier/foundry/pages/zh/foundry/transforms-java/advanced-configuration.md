---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-java/advanced-configuration/",
  "title": "高级配置",
  "page_id": "advanced-configuration",
  "category_id": "data-integration",
  "section_id": "transforms-java",
  "previous": "/zh/foundry/transforms-java/unit-tests/",
  "next": "/zh/foundry/transforms-java/incremental-transforms/",
  "scraped_at": "2026-07-13T06:08:48.228318+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 高级配置

本节介绍如何在Java变换中使用高级配置选项。

## 最大搭建持续时间

为了确保数据的新鲜度或限制成本，可能需要限制任务的运行时间。例如，如果一个任务正在与外部服务交互并变得无响应，限制其运行时间是有用的，因为它可能无法完成。在代码库中，可以通过使用`MaxAllowedDuration`和`Compute`装饰器来限制任务的持续时间，如下所示：

```java
package myproject.datasets;

import com.palantir.transforms.lang.java.api.*;
import java.time.Duration;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;

public final class FilterTransform {

   // 限制计算函数的最大允许执行时间为2小时
   @MaxAllowedDuration(value = "PT2H")
   @Compute
   public void myComputeFunction(
           // 输入数据集路径
           @Input("/examples/students_hair_eye_color") FoundryInput myInput,
           // 输出数据集路径
           @Output("/examples/students_hair_eye_color_filtered") FoundryOutput myOutput) {
       // 读取输入数据集并转换为DataFrame
       Dataset<Row> inputDf = myInput.asDataFrame().read();
       // 过滤DataFrame中眼睛颜色为棕色的记录，并写入输出数据集
       myOutput.getDataFrameWriter(inputDf.filter("eye = 'Brown'")).write();
   }
}
```

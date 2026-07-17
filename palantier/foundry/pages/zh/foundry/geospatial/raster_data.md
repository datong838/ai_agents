---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/geospatial/raster_data/",
  "title": "使用栅格数据",
  "page_id": "raster_data",
  "category_id": "data-integration",
  "section_id": "geospatial",
  "previous": "/zh/foundry/geospatial/example_workflows/",
  "next": "/zh/foundry/geospatial/vector_data_in_transforms/",
  "scraped_at": "2026-07-13T06:18:51.470094+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 使用栅格数据

Foundry 通过[媒体集](/zh/foundry/data-integration/media-sets/)以一流的方式支持大规模处理栅格数据。[文件级别变换](/zh/foundry/transforms-python/unstructured-files/)也支持自定义图像预处理，或处理当前媒体集不支持的任何文件格式。

了解有关不同类型[地理空间数据](/zh/foundry/geospatial/types_of_geospatial_data/)的更多信息。

## 数据格式和来源

支持的媒体集栅格文件格式：

* TIFF / GeoTIFF
* NITF
* JPEG2000

只能在文件级别处理的其他栅格文件格式：

* PNG
* JPEG

## 在媒体集中使用栅格数据

1. 将支持的栅格文件格式导入为媒体集。您可以通过数据连接或本地机器上传创建新的媒体集。了解不同的[导入媒体](/zh/foundry/data-integration/media-sets/#import-media)方法。

2. 导入后，您可以通过媒体引用利用媒体集。通过[Pipeline Builder](/zh/foundry/building-pipelines/create-batch-pipeline-pb-media-set/#get-media-references)或[变换](/zh/foundry/building-pipelines/create-batch-pipeline-cr-media-sets/)选择媒体引用。

3. 在Ontology中创建一个Object类型，可以作为Pipeline Builder中的管道输出或直接在Ontology Manager中创建。确保Object类型具有媒体引用属性作为媒体引用类型，并且您已在**Capabilities**中声明了支持的媒体集，以便平台知道在哪里以及如何引用您的媒体项。

![媒体引用属性类型](../../../images/foundry/geospatial/media-reference-property.png)

![媒体引用能力数据源](../../../images/foundry/geospatial/media-reference-data-source.png)

一旦您有了一个Object类型，您可以将其导入到地图应用程序中进行查看。在地图上显示大于67 MB的栅格文件不受支持。

![在地图中支持媒体集的Object类型](../../../images/foundry/geospatial/media-set-map-example.png)

## 在变换中使用栅格数据

对于当前媒体集不支持的栅格文件类型，您仍然可以在变换中处理它们。您可以在下面的部分中查看推荐的库和代码示例。

变换也非常适合预处理支持的媒体集文件类型。例如，您可以使用变换通过`MediaSetInput`更新图像的大小，并使用`MediaSetOutput`输出一个媒体集，如下例所示。[了解更多关于如何编写媒体集批处理管道](/zh/foundry/building-pipelines/create-batch-pipeline-cr-media-sets/)。

```python
from transforms.api import transform
from transforms.mediasets import MediaSetInput, MediaSetOutput

@transform(
    images=MediaSetInput('/examples/images'),  # 输入媒体集路径
    output_images=MediaSetOutput('/examples/output_images')  # 输出媒体集路径
)
def translate_images(images, output_images):
    ...
```

以上代码使用了一个装饰器`@transform`，定义了一个用于处理图片的函数`translate_images`。该函数接受`images`作为输入，并将处理后的图片输出到`output_images`。路径`/examples/images`和`/examples/output_images`分别指定了输入和输出的媒体集路径。

### 推荐的Python库

有几个常见的开源库在Foundry中处理栅格数据时效果很好，包括：

* [Rasterio ↗](https://rasterio.readthedocs.io/en/latest/)
* [PIL ↗](https://pillow.readthedocs.io/en/stable/)

### 代码示例

#### 使用Rasterio从数据集中打开一个GeoTIFF文件

```python
from transforms.api import transform, Input, Output, FileSystem
import rasterio
import tempfile
import shutil
import math

@transform(
    output=Output("OUTPUT_DATASET"),
    my_input=Input("INPUT_DATASET"),
)
def my_compute_function(output, my_input):
    def process_file(file_status):
        # 使用临时文件下载文件以便 Image 可以正确打开
        with tempfile.NamedTemporaryFile() as tmp:
            with my_input.filesystem().open(file_status.path, 'rb') as f:
                shutil.copyfileobj(f, tmp)
                tmp.flush()
                # 使用 rasterio 打开文件
                with rasterio.open(tmp.name, driver='GTiff') as dataset:
                    """ 在此处填写 rasterio 逻辑 """

    # 列出输入数据集中的所有文件
    files = list(my_input.filesystem().ls())
    # 对每个文件应用 process_file 函数
    map(process_file, files)
    return
```

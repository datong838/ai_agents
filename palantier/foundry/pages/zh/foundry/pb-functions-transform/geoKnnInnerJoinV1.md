---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/geoKnnInnerJoinV1/",
  "title": "几何 knn 内部合并",
  "page_id": "geoKnnInnerJoinV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/geoIntersectionJoinV1/",
  "next": "/zh/foundry/pb-functions-transform/geoKnnLeftJoinV1/",
  "scraped_at": "2026-07-13T05:58:42.558878+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 几何 knn 内部合并

> 支持于: 批处理

从邻居数据集中为基数据集中的每个有效输入几何选择k个最近点。在内部将输入数据集转换为给定的坐标参考系，然后再转换回WGS84。整个邻居数据集必须能够适合驱动程序和执行器内存。一个3 gb的执行器应能够处理邻居数据集中多达100万个点。

**变换类别**: 地理空间, 合并

## 声明的参数

* **基数据集** - 在合并中使用的基数据集。<br>*表格*
* **左侧选择列的条件** - 将测试左侧输入架构中的所有列是否符合此条件。如果符合，列将在输出中被选择。<br>*列谓词*
* **右侧选择列的条件** - 将测试右侧输入架构中的所有列是否符合此条件。如果符合，列将在输出中被选择。<br>*列谓词*
* **合并键** - 查询数据集中的GeoJSON列和邻居数据集中的地理点列。<br>*元组<列<几何>, 列<地理点>>*
* **K** - 从右侧数据集中为左侧数据集中每个有效几何选择的邻居数量。<br>*字面值<整数>*
* **邻居数据集** - 在合并中使用的潜在邻居的数据集。<br>*表格*
* **投影坐标系** - 输入几何将在合并之前转换为此坐标系，并且距离将以给定坐标系的单位进行测量。格式为"authority:id"，例如UTM 18N区可以通过EPSG:32618识别。<br>*字面值<字符串>*
* *非必填* **右侧列的前缀** - 为右侧所有列名添加的前缀。<br>*字面值<字符串>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **基数据集**: ri.foundry.main.dataset.left
* **左侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryCol, lhsCol],<br>)
* **右侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryCol, col],<br>)
* **合并键**: (`geometryCol`, `geometryCol`)
* **K**: 2
* **邻居数据集**: ri.foundry.main.dataset.right
* **投影坐标系**: epsg:2868
* **右侧列的前缀**: rhs\_

**输入:**
ri.foundry.main.dataset.left

| geometryCol | lhsCol |
| ----- | ----- |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 42.0 |

ri.foundry.main.dataset.right

| geometryCol | col |
| ----- | ----- |
| {<br> **latitude**: 33.440609443703586,<br> **longitude**: -112.14843750000001,<br>} | rhsVal1 |
| {<br> **latitude**: 33.44082430962016,<br> **longitude**: -112.14560508728029,<br>} | rhsVal2 |
| {<br> **latitude**: 33.440895931474124,<br> **longitude**: -112.11796760559083,<br>} | rhsVal3 |

**输出:**

| geometryCol | lhsCol | rhs\_geometryCol | rhs\_col |
| ----- | ----- | ----- | ----- |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 42.0 | {<br> **latitude**: 33.440609443703586,<br> **longitude**: -112.14843750000001,<br>} | rhsVal1 |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 42.0 | {<br> **latitude**: 33.44082430962016,<br> **longitude**: -112.14560508728029,<br>} | rhsVal2 |

***

### 示例 2: 基本情况

**参数值:**

* **基数据集**: ri.foundry.main.dataset.left
* **左侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryColLhs, lhs-1],<br>)
* **右侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryColRhs, rhs-1],<br>)
* **合并键**: (`geometryColLhs`, `geometryColRhs`)
* **K**: 1
* **邻居数据集**: ri.foundry.main.dataset.right
* **投影坐标系**: epsg:2868
* **右侧列的前缀**: *null*

**输入:**
ri.foundry.main.dataset.left

| geometryColLhs | lhs-1 |
| ----- | ----- |

ri.foundry.main.dataset.right

| geometryColRhs | rhs-1 |
| ----- | ----- |

**输出:**

| geometryColLhs | lhs-1 | geometryColRhs | rhs-1 |
| ----- | ----- | ----- | ----- |

***

### 示例 3: 基本情况

**参数值:**

* **基数据集**: ri.foundry.main.dataset.left
* **左侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryCol, lhsCol],<br>)
* **右侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryCol, col],<br>)
* **合并键**: (`geometryCol`, `geometryCol`)
* **K**: 2
* **邻居数据集**: ri.foundry.main.dataset.right
* **投影坐标系**: epsg:2868
* **右侧列的前缀**: rhs\_

**输入:**
ri.foundry.main.dataset.left

| geometryCol | lhsCol |
| ----- | ----- |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 42.0 |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 43.0 |

ri.foundry.main.dataset.right

| geometryCol | col |
| ----- | ----- |
| {<br> **latitude**: 33.440609443703586,<br> **longitude**: -112.14843750000001,<br>} | rhsVal1 |
| {<br> **latitude**: 33.44082430962016,<br> **longitude**: -112.14560508728029,<br>} | rhsVal2 |
| {<br> **latitude**: 33.440895931474124,<br> **longitude**: -112.11796760559083,<br>} | rhsVal3 |

**输出:**

| geometryCol | lhsCol | rhs\_geometryCol | rhs\_col |
| ----- | ----- | ----- | ----- |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 42.0 | {<br> **latitude**: 33.440609443703586,<br> **longitude**: -112.14843750000001,<br>} | rhsVal1 |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 43.0 | {<br> **latitude**: 33.440609443703586,<br> **longitude**: -112.14843750000001,<br>} | rhsVal1 |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 42.0 | {<br> **latitude**: 33.44082430962016,<br> **longitude**: -112.14560508728029,<br>} | rhsVal2 |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 43.0 | {<br> **latitude**: 33.44082430962016,<br> **longitude**: -112.14560508728029,<br>} | rhsVal2 |

***

### 示例 4: 基本情况

**参数值:**

* **基数据集**: ri.foundry.main.dataset.left
* **左侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryCol, lhsCol],<br>)
* **右侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryCol, col],<br>)
* **合并键**: (`geometryCol`, `geometryCol`)
* **K**: 3
* **邻居数据集**: ri.foundry.main.dataset.right
* **投影坐标系**: epsg:2868
* **右侧列的前缀**: rhs\_

**输入:**
ri.foundry.main.dataset.left

| geometryCol | lhsCol |
| ----- | ----- |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 42.0 |

ri.foundry.main.dataset.right

| geometryCol | col |
| ----- | ----- |
| {<br> **latitude**: 33.440609443703586,<br> **longitude**: -112.14843750000001,<br>} | rhsVal1 |
| {<br> **latitude**: 33.440609443703586,<br> **longitude**: -112.14843750000001,<br>} | rhsVal1 |
| {<br> **latitude**: 33.44082430962016,<br> **longitude**: -112.14560508728029,<br>} | rhsVal2 |
| {<br> **latitude**: 33.44082430962016,<br> **longitude**: -112.14560508728029,<br>} | rhsVal2 |
| {<br> **latitude**: 33.440895931474124,<br> **longitude**: -112.11796760559083,<br>} | rhsVal3 |

**输出:**

| geometryCol | lhsCol | rhs\_geometryCol | rhs\_col |
| ----- | ----- | ----- | ----- |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 42.0 | {<br> **latitude**: 33.440609443703586,<br> **longitude**: -112.14843750000001,<br>} | rhsVal1 |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 42.0 | {<br> **latitude**: 33.440609443703586,<br> **longitude**: -112.14843750000001,<br>} | rhsVal1 |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 42.0 | {<br> **latitude**: 33.44082430962016,<br> **longitude**: -112.14560508728029,<br>} | rhsVal2 |

***

### 示例 5: 基本情况

**参数值:**

* **基数据集**: ri.foundry.main.dataset.left
* **左侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryColLhs, lhs-1],<br>)
* **右侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryColRhs, rhs-1],<br>)
* **合并键**: (`geometryColLhs`, `geometryColRhs`)
* **K**: 1
* **邻居数据集**: ri.foundry.main.dataset.right
* **投影坐标系**: epsg:2868
* **右侧列的前缀**: *null*

**输入:**
ri.foundry.main.dataset.left

| geometryColLhs | lhs-1 |
| ----- | ----- |

ri.foundry.main.dataset.right

| geometryColRhs | rhs-1 |
| ----- | ----- |
| {<br> **latitude**: 33.44082430962016,<br> **longitude**: -112.14560508728029,<br>} | *null* |
| {<br> **latitude**: 33.440895931474124,<br> **longitude**: -112.11796760559083,<br>} | rhsVal2 |
| *null* | rhsVal3 |

**输出:**

| geometryColLhs | lhs-1 | geometryColRhs | rhs-1 |
| ----- | ----- | ----- | ----- |

***

### 示例 6: 基本情况

**参数值:**

* **基数据集**: ri.foundry.main.dataset.left
* **左侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryColLhs, lhs-1],<br>)
* **右侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryColRhs, rhs-1],<br>)
* **合并键**: (`geometryColLhs`, `geometryColRhs`)
* **K**: 1
* **邻居数据集**: ri.foundry.main.dataset.right
* **投影坐标系**: epsg:2868
* **右侧列的前缀**: *null*

**输入:**
ri.foundry.main.dataset.left

| geometryColLhs | lhs-1 |
| ----- | ----- |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 42.0 |
| {"coordinates": \[-112.14560508728029,33.44082430962016], "type":"Point"} | 43.0 |

ri.foundry.main.dataset.right

| geometryColRhs | rhs-1 |
| ----- | ----- |

**输出:**

| geometryColLhs | lhs-1 | geometryColRhs | rhs-1 |
| ----- | ----- | ----- | ----- |

***

### 示例 7: 基本情况

**参数值:**

* **基数据集**: ri.foundry.main.dataset.left
* **左侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryCol, lhsCol],<br>)
* **右侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryCol, col1, arrayCol],<br>)
* **合并键**: (`geometryCol`, `geometryCol`)
* **K**: 5
* **邻居数据集**: ri.foundry.main.dataset.right
* **投影坐标系**: epsg:4326
* **右侧列的前缀**: rhs\_

**输入:**
ri.foundry.main.dataset.left

| geometryCol | lhsCol |
| ----- | ----- |
| {"coordinates": \[\[\[0.0, 0.0], \[10.0, 0.0], \[10.0, 10.0], \[0.0, 10.0], \[0.0, 0.0]]], "type": "Polygon"} | 42.0 |

ri.foundry.main.dataset.right

| geometryCol | col1 | arrayCol | toDrop |
| ----- | ----- | ----- | ----- |
| {<br> **latitude**: 33.440609443703586,<br> **longitude**: -112.14843750000001,<br>} | rhsVal1 | \[ 0.0, 1.1 ] | 1.0 |
| {<br> **latitude**: 33.44082430962016,<br> **longitude**: -112.14560508728029,<br>} | rhsVal2 | \[ 0.0, 1.1 ] | 1.0 |
| {<br> **latitude**: 33.440895931474124,<br> **longitude**: -112.11796760559083,<br>} | rhsVal3 | \[ 0.0, 1.1 ] | 1.0 |

**输出:**

| geometryCol | lhsCol | rhs\_geometryCol | rhs\_col1 | rhs\_arrayCol |
| ----- | ----- | ----- | ----- | ----- |
| {"coordinates": \[\[\[0.0, 0.0], \[10.0, 0.0], \[10.0, 10.0], \[0.0, 10.0], \[0.0, 0.0]]], "type": "Polygon"} | 42.0 | {<br> **latitude**: 33.440609443703586,<br> **longitude**: -112.14843750000001,<br>} | rhsVal1 | \[ 0.0, 1.1 ] |
| {"coordinates": \[\[\[0.0, 0.0], \[10.0, 0.0], \[10.0, 10.0], \[0.0, 10.0], \[0.0, 0.0]]], "type": "Polygon"} | 42.0 | {<br> **latitude**: 33.44082430962016,<br> **longitude**: -112.14560508728029,<br>} | rhsVal2 | \[ 0.0, 1.1 ] |
| {"coordinates": \[\[\[0.0, 0.0], \[10.0, 0.0], \[10.0, 10.0], \[0.0, 10.0], \[0.0, 0.0]]], "type": "Polygon"} | 42.0 | {<br> **latitude**: 33.440895931474124,<br> **longitude**: -112.11796760559083,<br>} | rhsVal3 | \[ 0.0, 1.1 ] |

***

### 示例 8: 基本情况

**参数值:**

* **基数据集**: ri.foundry.main.dataset.left
* **左侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryColLhs, lhs-1],<br>)
* **右侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryColRhs, rhs-1],<br>)
* **合并键**: (`geometryColLhs`, `geometryColRhs`)
* **K**: 1
* **邻居数据集**: ri.foundry.main.dataset.right
* **投影坐标系**: epsg:2868
* **右侧列的前缀**: *null*

**输入:**
ri.foundry.main.dataset.left

| geometryColLhs | lhs-1 |
| ----- | ----- |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 42.0 |
| *null* | 43.0 |

ri.foundry.main.dataset.right

| geometryColRhs | rhs-1 |
| ----- | ----- |
| {<br> **latitude**: 33.44082430962016,<br> **longitude**: -112.14560508728029,<br>} | *null* |
| {<br> **latitude**: 33.440895931474124,<br> **longitude**: -112.11796760559083,<br>} | rhsVal2 |
| *null* | rhsVal3 |

**输出:**

| geometryColLhs | lhs-1 | geometryColRhs | rhs-1 |
| ----- | ----- | ----- | ----- |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 42.0 | {<br> **latitude**: 33.44082430962016,<br> **longitude**: -112.14560508728029,<br>} | *null* |

***

### 示例 9: 基本情况

**参数值:**

* **基数据集**: ri.foundry.main.dataset.left
* **左侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryColLhs, lhs-1],<br>)
* **右侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[],<br>)
* **合并键**: (`geometryColLhs`, `geometryColRhs`)
* **K**: 1
* **邻居数据集**: ri.foundry.main.dataset.right
* **投影坐标系**: epsg:2868
* **右侧列的前缀**: *null*

**输入:**
ri.foundry.main.dataset.left

| geometryColLhs | lhs-1 |
| ----- | ----- |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 42.0 |
| {"coordinates": \[-112.14560508728029,33.44082430962016], "type":"Point"} | 43.0 |

ri.foundry.main.dataset.right

| geometryColRhs | rhs-1 |
| ----- | ----- |
| {<br> **latitude**: 33.44082430962016,<br> **longitude**: -112.14560508728029,<br>} | *null* |
| {<br> **latitude**: 33.440895931474124,<br> **longitude**: -112.11796760559083,<br>} | rhsVal2 |
| *null* | rhsVal3 |

**输出:**

| geometryColLhs | lhs-1 |
| ----- | ----- |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 42.0 |
| {"coordinates": \[-112.14560508728029,33.44082430962016], "type":"Point"} | 43.0 |

***

### 示例 10: 基本情况

**参数值:**

* **基数据集**: ri.foundry.main.dataset.left
* **左侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[],<br>)
* **右侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryColRhs, rhs-1],<br>)
* **合并键**: (`geometryColLhs`, `geometryColRhs`)
* **K**: 1
* **邻居数据集**: ri.foundry.main.dataset.right
* **投影坐标系**: epsg:2868
* **右侧列的前缀**: *null*

**输入:**
ri.foundry.main.dataset.left

| geometryColLhs | lhs-1 |
| ----- | ----- |
| {"coordinates": \[-112.14843750000001,33.440609443703586], "type":"Point"} | 42.0 |
| {"coordinates": \[-112.14560508728029,33.44082430962016], "type":"Point"} | 43.0 |

ri.foundry.main.dataset.right

| geometryColRhs | rhs-1 |
| ----- | ----- |
| {<br> **latitude**: 33.44082430962016,<br> **longitude**: -112.14560508728029,<br>} | *null* |
| {<br> **latitude**: 33.440895931474124,<br> **longitude**: -112.11796760559083,<br>} | rhsVal2 |
| *null* | rhsVal3 |

**输出:**

| geometryColRhs | rhs-1 |
| ----- | ----- |
| {<br> **latitude**: 33.44082430962016,<br> **longitude**: -112.14560508728029,<br>} | *null* |
| {<br> **latitude**: 33.44082430962016,<br> **longitude**: -112.14560508728029,<br>} | *null* |

***

### 示例 11: 基本情况

**参数值:**

* **基数据集**: ri.foundry.main.dataset.left
* **左侧选择列的条件**: <br>allColumns(<br><br>)
* **右侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[geometryCol, col1, arrayCol],<br>)
* **合并键**: (`geometryCol`, `geometryCol`)
* **K**: 1
* **邻居数据集**: ri.foundry.main.dataset.right
* **投影坐标系**: epsg:4326
* **右侧列的前缀**: rhs\_

**输入:**
ri.foundry.main.dataset.left

| geometryCol | lhsCol |
| ----- | ----- |
| {"coordinates": \[\[\[0.0, 0.0], \[10.0, 0.0], \[10.0, 10.0], \[0.0, 10.0], \[0.0, 0.0]]], "type": "Polygon"} | 42.0 |
| {"coordinates": \[55.0, 5.0], "type":"Point"} | 43.0 |
| {"coordinates": \[\[40.0, 0.0], \[0.0, 40.0]], "type":"LineString"} | 44.0 |
| {"coordinates": \[\[\[20.0, 10.0], \[27.0, 10.0], \[27.0, 17.0], \[20.0, 17.0], \[20.0, 10.0]]], "type": "Polygon"} | 45.0 |
| {"coordinates": \[\[\[21.0, 21.0], \[27.0, 21.0], \[27.0, 27.0], \[21.0, 27.0], \[21.0, 21.0]]], "type": "Polygon"} | 46.0 |
| {"coordinates": \[\[\[\[2.0, 2.0], \[7.0, 2.0], \[7.0, 7.0], \[2.0, 7.0], \[2.0, 2.0]]], \[\[\[12.0, 12.0], \[17.0, 12.0], \[17.0, 17.0], \[12.0, 17.0], \[12.0, 12.0]]]], "type":"MultiPolygon"} | 47.0 |
| {"coordinates": \[\[\[\[170.0, 170.0], \[190.0, 170.0], \[190.0, 190.0], \[170.0, 190.0], \[170.0, 170.0]]], \[\[\[12.0, 12.0], \[17.0, 12.0], \[17.0, 17.0], \[12.0, 17.0], \[12.0, 12.0]]]], "type":"MultiPolygon"} | 48.0 |

ri.foundry.main.dataset.right

| geometryCol | col1 | arrayCol | toDrop |
| ----- | ----- | ----- | ----- |
| {<br> **latitude**: 5.0,<br> **longitude**: 5.0,<br>} | rhsVal1 | \[ 0.0, 1.1 ] | 1.0 |
| {<br> **latitude**: 100.0,<br> **longitude**: 100.0,<br>} | rhsVal2 | \[ 0.0, 1.1 ] | 1.0 |

**输出:**

| geometryCol | lhsCol | rhs\_geometryCol | rhs\_col1 | rhs\_arrayCol |
| ----- | ----- | ----- | ----- | ----- |
| {"coordinates": \[\[\[0.0, 0.0], \[10.0, 0.0], \[10.0, 10.0], \[0.0, 10.0], \[0.0, 0.0]]], "type": "Polygon"} | 42.0 | {<br> **latitude**: 5.0,<br> **longitude**: 5.0,<br>} | rhsVal1 | \[ 0.0, 1.1 ] |
| {"coordinates": \[55.0, 5.0], "type":"Point"} | 43.0 | {<br> **latitude**: 5.0,<br> **longitude**: 5.0,<br>} | rhsVal1 | \[ 0.0, 1.1 ] |
| {"coordinates": \[\[40.0, 0.0], \[0.0, 40.0]], "type":"LineString"} | 44.0 | {<br> **latitude**: 5.0,<br> **longitude**: 5.0,<br>} | rhsVal1 | \[ 0.0, 1.1 ] |
| {"coordinates": \[\[\[20.0, 10.0], \[27.0, 10.0], \[27.0, 17.0], \[20.0, 17.0], \[20.0, 10.0]]], "type": "Polygon"} | 45.0 | {<br> **latitude**: 5.0,<br> **longitude**: 5.0,<br>} | rhsVal1 | \[ 0.0, 1.1 ] |
| {"coordinates": \[\[\[21.0, 21.0], \[27.0, 21.0], \[27.0, 27.0], \[21.0, 27.0], \[21.0, 21.0]]], "type": "Polygon"} | 46.0 | {<br> **latitude**: 5.0,<br> **longitude**: 5.0,<br>} | rhsVal1 | \[ 0.0, 1.1 ] |
| {"coordinates": \[\[\[\[2.0, 2.0], \[7.0, 2.0], \[7.0, 7.0], \[2.0, 7.0], \[2.0, 2.0]]], \[\[\[12.0, 12.0], \[17.0, 12.0], \[17.0, 17.0], \[12.0, 17.0], \[12.0, 12.0]]]], "type":"MultiPolygon"} | 47.0 | {<br> **latitude**: 5.0,<br> **longitude**: 5.0,<br>} | rhsVal1 | \[ 0.0, 1.1 ] |
| {"coordinates": \[\[\[\[170.0, 170.0], \[190.0, 170.0], \[190.0, 190.0], \[170.0, 190.0], \[170.0, 170.0]]], \[\[\[12.0, 12.0], \[17.0, 12.0], \[17.0, 17.0], \[12.0, 17.0], \[12.0, 12.0]]]], "type":"MultiPolygon"} | 48.0 | {<br> **latitude**: 5.0,<br> **longitude**: 5.0,<br>} | rhsVal1 | \[ 0.0, 1.1 ] |

***

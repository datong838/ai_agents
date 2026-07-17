---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/constructDelegatedMediaGidV1/",
  "title": "构建委托媒体 Gotham 标识符 (GID)",
  "page_id": "constructDelegatedMediaGidV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/constructGeoPointV1/",
  "next": "/zh/foundry/pb-functions-expression/dmsToGeoPointV1/",
  "scraped_at": "2026-07-13T05:53:24.707303+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 构建委托媒体 Gotham 标识符 (GID)

> 支持于: 批处理，流处理

从组件构建有效的委托媒体 Gotham 标识符 (GID) 的表达式。如果结果超过1024个字符，则产生空行。

**表达式类别**: 其他

## 声明的参数

* **媒体定位器** - 委托媒体的非空定位器。空值或空字符串将导致输出为空。<br>*Expression<字符串>*
* **媒体类型** - 委托媒体的非空类型。空值或空字符串将导致输出为空。<br>*Expression<字符串>*
* **生产者实例** - 媒体生产者的UUID。无效的UUID将使所有输出为空。<br>*Literal<字符串>*

**输出类型:** *委托媒体 Gotham 标识符 (GID)*

## 示例

### 示例 1: 基础案例

**参数值:**

* **媒体定位器**: `locator`
* **媒体类型**: `mediaType`
* **生产者实例**: invalidUuid

| mediaType | locator | **输出** |
| ----- | ----- | ----- |
| testaudiotype | *空字符串* | *null* |

***

### 示例 2: 基础案例

**参数值:**

* **媒体定位器**: `locator`
* **媒体类型**: `mediaType`
* **生产者实例**: invalidUuid

| mediaType | locator | **输出** |
| ----- | ----- | ----- |
| *空字符串* | testlocator | *null* |

***

### 示例 3: 基础案例

**参数值:**

* **媒体定位器**: `locator`
* **媒体类型**: `mediaType`
* **生产者实例**: invalidUuid

| mediaType | locator | **输出** |
| ----- | ----- | ----- |
| testaudiotype | testlocator | *null* |

***

### 示例 4: 基础案例

**参数值:**

* **媒体定位器**: `locator`
* **媒体类型**: `mediaType`
* **生产者实例**: 12345678-1234-1234-1234-123456789012

| mediaType | locator | **输出** |
| ----- | ----- | ----- |
| *null* | testlocator | *null* |

***

### 示例 5: 基础案例

**参数值:**

* **媒体定位器**: `locator`
* **媒体类型**: `mediaType`
* **生产者实例**: 12345678-1234-1234-1234-123456789012

| mediaType | locator | **输出** |
| ----- | ----- | ----- |
| testaudiotype | *null* | *null* |

***

### 示例 6: 基础案例

**参数值:**

* **媒体定位器**: `locator`
* **媒体类型**: `mediaType`
* **生产者实例**: 12345678-1234-1234-1234-123456789012

| mediaType | locator | **输出** |
| ----- | ----- | ----- |
| testaudiotype | testlocator | ri.gotham-delegated-media.12345678-1234-1234-1234-123456789012.testaudiotype.testlocator |

***

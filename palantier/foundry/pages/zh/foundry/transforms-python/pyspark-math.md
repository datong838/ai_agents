---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/pyspark-math/",
  "title": "数学",
  "page_id": "pyspark-math",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/pyspark-strings/",
  "next": "/zh/foundry/transforms-python/pyspark-joins/",
  "scraped_at": "2026-07-13T06:08:19.733055+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数学

## 四舍五入

* `F.bround(x, scale=0)`
  * 使用`HALF_EVEN`舍入模式将给定列x的值四舍五入到scale个小数位，如果`scale >= 0`，否则在`scale < 0`时取整。

* `F.ceil(x)`
  * 计算给定值的向上取整。

* `F.round(column, scale=0)`

* `F.floor(column)`

## 对数

* `F.log(arg1, arg2=None)`
* `F.log10(column)`
* `F.log1p(column)`

## 随机

* `F.rand(seed=None)`
  * 从均匀分布\[0.0, 1.0]中独立同分布 (i.i.d.) 抽样

* `F.randn(seed=None)`
  * 从标准正态分布中独立同分布 (i.i.d.) 抽样

## 三角函数

* `F.cos(x)`
  * 计算数值列x的余弦。

* `F.sin(x)`

* `F.tan(x)`

* `F.acos(x)`
  * 计算数值列x的反余弦；返回的角度范围是`[0.0, π]`。
    cos<sup>-1</sup>(x)

* `F.asin(x)`
  * 计算数值列x的反正弦；返回的角度范围是`[-π/2, π/2]`。
    sin<sup>-1</sup>(x)

* `F.atan(x)`
  * 计算数值列x的反正切。
    tan<sup>-1</sup>(x)

* `F.atan2(x, y)`
  * 将表示为列x, y的直角坐标`(x, y)`转换为极坐标`(r, theta)`并返回角度theta。

* `F.cosh(x)`
  * 计算列x的双曲余弦。

* `F.sinh(x)`

* `F.tanh(x)`

## 角度

* `F.degrees(column)`
* `F.radians(column)`

## 杂项

* `F.abs(x)`
  * `x`的绝对值
* `F.cbrt(x)`
  * 计算给定值的**立方根**。
* `F.exp(x)`
* `F.expm1(x)`
* `F.factorial(x)`
* `F.greatest(*cols)`
* `F.hypot(x, y)`
* `F.least(*cols)`
* `F.pow(x, y)`
  * `x`的`y`次幂
* `F.rint(column)`
* `F.signum(column)`
* `F.sqrt(column)`

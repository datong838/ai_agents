---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/sap/configure-extractors/",
  "title": "提取器",
  "page_id": "configure-extractors",
  "category_id": "data-integration",
  "section_id": "sap",
  "previous": "/zh/foundry/sap/configure-bex-query/",
  "next": "/zh/foundry/sap/configure-functions/",
  "scraped_at": "2026-07-13T05:39:01.516165+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 提取器

## 概述

Palantir Foundry Connector 2.0 以SAP应用程序（“连接器”）支持通过多个提取接口（称为 **SAP 提取器**）进行数据摄取。它们最初被设计用于从SAP操作系统提取数据到SAP业务仓库（BW）。

提取器有三种类型：

* **业务内容提取器** 是SAP为各种应用组件（如FI、CO、LO Cockpit等）标准预交付的。它们在源系统中默认未激活，需要通过`RSA5`事务代码激活后使用。
* **客户生成提取器** 通常根据客户实施和配置设置生成。
* **通用提取器** 高度可定制。每个客户可以基于数据库表/视图、信息集和函数模块生成自己的提取逻辑。这些提取器高度可定制，提取逻辑由客户控制。

:::callout{theme="neutral"}
连接器只能使用ODP启用的提取器。完整的“ODP数据复制API 2.0”可通过适用组件（PI\_BASIS、SAP\_BW或DW4CORE）的以下支持包（SP）获得，参考SAP注释 `1931427` - *ODP数据复制API 2.0*。确保满足以下前提条件：

* PI\_BASIS 730 SP 14（属于SAP NetWeaver 7.30 SP 14）+
* PI\_BASIS 731 SP 16（属于SAP NetWeaver 7.03 SP 16和7.31 SP 16）+
* PI\_BASIS 740 SP 11（属于SAP NetWeaver 7.40 SP 11）+
* SAP\_BW 750 SP 0（包括以前的PI\_BASIS包）+
* DW4CORE 100 SP 0（包括以前的PI\_BASIS包）+
* DW4CORE 200 SP 0（包括以前的PI\_BASIS包）+
:::

:::callout{theme="neutral"}
对于ODP启用提取器所在源系统中的授权，请参考SAP注释 `2855052` - *ODP数据复制API 2.0 所需的授权*。
连接器还为提取器设有一个单独的角色：为Foundry技术用户指派`/PALANTIR/CONTENT_EXT_ALL`授权角色。
:::

## 提取器的配置

### 从单一源系统（连接器版本低于v2.20.0 (< SP20)）

* 创建一个从连接器到提取器所在SAP源系统的RFC连接。
* 使用`/n/palantir/param`事务来维护以下参数：
  * RFC参数
    * **Param ID**: `EXTRACTOR`
    * **Param Name**: `RFC_CONFIGURATION`
    * **Param Value**: `<RFC连接名称>`
  * 上下文配置
    * **Param ID**: `EXTRACTOR`
    * **Param Name**: `CONTEXT_CONFIGURATION`
    * **Param Value**: `SAPI`

### 从多个源系统（连接器版本v2.20.0或更新版本 (>= SP20)）

从连接器的SP20版本开始，可以从多个源系统（也称为“上下文”）提取数据。

要配置多个上下文，请按照以下步骤：

* 运行`/PALANTIR/PARAM_E1`事务并定义每个上下文：
  * **Extractor ID**: `<源系统ID>`
  * **Description**: `<源系统描述>`
* 运行`/PALANTIR/PARAM_E2`事务并定义每个上下文参数：
  * **Extractor ID**: `<上下文ID>`
  * **Param ID**: `<连接器参数ID>`
  * **Param Name**: `<连接器参数名称>`
  * **Param Value**: `<参数值>`

:::callout{theme="neutral"}
RFC和SOURCE参数是多上下文特定的；其他提取器参数是标准连接器[参数](/zh/foundry/sap/addon-parameters/)。
:::

* 可以将其中一个上下文设置为默认。在这种情况下，如果Foundry未指定上下文信息，连接器将使用默认上下文。要定义默认上下文，请使用以下参数值运行`/PALANTIR/PARAM`事务：
  * **Param ID**: `EXTRACTOR`
  * **Param Name**: `DEFAULT_CONFIGURATION`
  * **Param Value**: `<EXTRACTOR ID>`

## 使用提取器

* 使用程序`RODPS_OS_EXPOSE`在SAP源系统中公开SAP提取器。
* 重新启动Foundry [数据连接代理](/zh/foundry/data-connection/core-concepts/#agents)以刷新缓存。
* 创建一个新的[BW内容提取器](/zh/foundry/sap/sap-object-types/#bw-content-extractor)同步。

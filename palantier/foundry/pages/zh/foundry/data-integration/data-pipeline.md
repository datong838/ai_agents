---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-integration/data-pipeline/",
  "title": "什么是数据管道？",
  "page_id": "data-pipeline",
  "category_id": "data-integration",
  "section_id": null,
  "previous": "/zh/foundry/data-integration/connecting-to-data/",
  "next": "/zh/foundry/data-integration/application-reference/",
  "scraped_at": "2026-07-13T05:30:11.998856+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 什么是数据管道？

在Foundry中，数据集成的总体目标是提供您组织内客观现实的数字视图。实现这一目标通常需要从多个源系统同步数据，施加通用模式，合并数据集，并使团队能够在通用的数据基础上搭建应用案例。

在这个背景下，术语“数据管道”广泛用于指代数据从源系统通过中间数据集流动，最终生成高质量的、经过整理的数据集，这些数据集可以结构化到[Ontology](/zh/foundry/ontology/overview/)中或作为[机器学习](/zh/foundry/model-integration/overview/)和[分析](/zh/foundry/analytics/overview/)工作流的基础。

虽然在Foundry中，通过变换逻辑连接在一起的任何两个数据集都可以被视为管道，但实际上，我们所称的“数据管道”更加受限。通常情况下，管道有一个*所有权*的概念——由一个人或一组人负责监督管道，以确保数据定期和可靠地流过它，从而支持业务流程。

除了所有权概念之外，优质的、生产就绪的数据管道还具备其他几个特征。我们将在本文档的其余部分探讨这些概念，并提供学习更多内容的链接：

* [什么是数据管道？](#what-is-a-data-pipeline)
  * [管道设置](#pipeline-setup)
  * [搭建调度](#build-scheduling)
  * [数据质量](#data-quality)
  * [安全和治理](#security-and-governance)
  * [支持流程和文档](#support-processes-and-documentation)

除了所有管道共有的特性外，还需考虑根据数据规模、延迟要求和维护复杂性等因素为您的数据基础创建哪种类型的管道。在Foundry中，有三种主要类型的管道：批处理、增量和流式。[了解更多关于管道类型的信息。](/zh/foundry/building-pipelines/pipeline-types/)

## 管道设置

Foundry的管道搭建器使用户能够通过简化的点选界面快速轻松地设置管道。使用管道搭建器，用户可以获得Git风格的更改管理、数据健康检查、多模式安全和细粒度数据审计的好处。

技术用户可以比以往更快速地搭建和维护管道，专注于对其端到端管道和期望输出的声明性描述。此外，管道搭建器的点选、基于表单的界面使技术水平较低的用户能够通过简化的方法创建管道。

* 学习如何[使用管道搭建器搭建管道](/zh/foundry/pipeline-builder/overview/)。

## 搭建调度

简单地说，一系列数据变换必须定期运行才能被视为数据管道。在Foundry中定义搭建[调度](/zh/foundry/data-integration/schedules/)是构建管道的基本步骤，因为下游数据消费者期望数据能够定期更新。数据通过管道流动的频率受组织需求的影响：某些管道可能仅每周或每天运行，而其他管道则可能每小时甚至更频繁地运行。

以下资源可以帮助您开始在Foundry中调度搭建：

* 学习如何[创建一个调度](/zh/foundry/building-pipelines/create-schedule/)。
* 了解[调度最佳实践](/zh/foundry/building-pipelines/scheduling-best-practices/)。
* 学习如何[排除现有调度的故障](/zh/foundry/optimizing-pipelines/troubleshoot-schedules/)。

## 数据质量

在定义管道的初始阶段，我们建议在每一步都经常检查输入和输出的质量。从源系统同步的数据通常包含未定义的值以及格式不佳或不一致的数据。清理和规范化数据是搭建管道过程的核心部分。

Foundry中提供了检查数据集假设的工具：

* [数据集预览](/zh/foundry/dataset-preview/overview/#data-preview)支持计算数据集任意列的统计信息，并筛选到行的子集以快速检查预期。
* 代码库对[调试变换](/zh/foundry/code-repositories/debug-transforms/)的支持可用于检查输入数据集在编写变换逻辑时是否按预期结构化。
* Foundry分析套件中的应用程序，特别是[Contour](/zh/foundry/contour/overview/)，对于以点选方式验证数据集的假设非常有帮助。

在您的管道建立之后，[健康检查](/zh/foundry/data-integration/health-checks/)是验证数据在时间上保持高质量的推荐方法。以下是一些开始健康检查的资源：

* 了解[推荐的健康检查](/zh/foundry/maintaining-pipelines/recommended-health-checks/)。
* 阅读[检查参考](/zh/foundry/data-health/checks-reference/)以了解可用检查的范围。

## 安全和治理

Foundry的平台安全原语为保护数据基础和确保敏感数据得到适当处理提供了最佳的能力。[项目](/zh/foundry/security/projects-and-roles/)和[权限标记](/zh/foundry/security/markings/)的跨领域概念分别支持自由裁量和强制控制，可用于满足全面的治理要求。

要了解有关如何在您的管道中安全处理数据的更多信息，请参考以下部分：

* [推荐的项目结构](/zh/foundry/building-pipelines/recommended-project-structure/)提供了一个适用于大多数管道的简单框架。
* [保护数据基础](/zh/foundry/security/securing-a-data-foundation/)通过一个端到端的示例介绍了最佳实践。
* [保护敏感数据](/zh/foundry/security/protecting-sensitive-data/)描述了如何处理高度敏感的数据，如个人身份信息或PII。

## 支持流程和文档

一旦管道按照上述指南发布到生产中，从组织的角度考虑管道的长期性就很重要。管道维护的支持流程应详细制定，期望值应明确定义，并应提供文档，以便即使在团队之间移交时，管道仍能保持高质量。

了解更多关于这些最佳实践的信息：

* [管道定义和期望](/zh/foundry/building-pipelines/building-production-pipeline/#pipeline-definition-and-expectations)
* [设置支持流程](/zh/foundry/maintaining-pipelines/support-processes/)

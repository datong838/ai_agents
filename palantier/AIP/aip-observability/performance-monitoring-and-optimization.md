> Source: https://www.palantir.com/docs/foundry/aip-observability/performance-monitoring-and-optimization/

- 
- 
- 
- 
- 
- 
- AIP observability • Performance monitoring and optimization • Palantir
- 
- 
- 
- 
- 
- 
- 
- Search
[Palantir](https://www.palantir.com/docs/)
- Documentation

- [Documentation](https://www.palantir.com/docs/foundry/)
- [Apollo](https://www.palantir.com/docs/apollo/)
- [Gotham](https://www.palantir.com/docs/gotham/)Search documentation
Searchkarat

+

K
[API Reference ↗](https://www.palantir.com/docs/foundry/api-reference/)Send feedbackenenjpkrzhABXYABXYABXYABXYABXYABXYABXY
- Capabilities

- [AI Platform (AIP)](https://www.palantir.com/docs/foundry/aip/overview/)
- [Data connectivity & integration](https://www.palantir.com/docs/foundry/data-integration/overview/)
- [Model connectivity & development](https://www.palantir.com/docs/foundry/model-integration/overview/)
- [Ontology building](https://www.palantir.com/docs/foundry/ontology/overview/)
- [Developer toolchain](https://www.palantir.com/docs/foundry/dev-toolchain/overview/)
- [Use case development](https://www.palantir.com/docs/foundry/app-building/overview/)
- [Observability](https://www.palantir.com/docs/foundry/observability/overview/)
- [Analytics](https://www.palantir.com/docs/foundry/analytics/overview/)
- [Product delivery](https://www.palantir.com/docs/foundry/devops/overview/)
- [Security & governance](https://www.palantir.com/docs/foundry/security/overview/)
- [Management & enablement](https://www.palantir.com/docs/foundry/administration/overview/)
- [Getting started](https://www.palantir.com/docs/foundry/getting-started/overview/)
- [Architecture center](https://www.palantir.com/docs/foundry/architecture-center/overview/)
- Platform updates

- [Announcements](https://www.palantir.com/docs/foundry/announcements/)
- [Release notes](https://www.palantir.com/docs/foundry/announcements/release-notes/)

## Observability
Hide sidebar

- [Overview](https://www.palantir.com/docs/foundry/observability/overview/)
- [Release notes ↗](https://www.palantir.com/docs/foundry/announcements/release-notes/?filters=observability)
- Monitoring
- [Data Health](https://www.palantir.com/docs/foundry/observability/data-health/)
- 

Monitoring views
- [Overview](https://www.palantir.com/docs/foundry/monitoring-views/overview/)
- [Alert debug page](https://www.palantir.com/docs/foundry/monitoring-views/alert-debug-page/)
- [Core concepts](https://www.palantir.com/docs/foundry/monitoring-views/core-concepts/)
- [Sending alerts to external systems](https://www.palantir.com/docs/foundry/monitoring-views/external-systems/)
- [Monitoring rules reference](https://www.palantir.com/docs/foundry/monitoring-views/rules-reference/)
- [Monitoring FAQ](https://www.palantir.com/docs/foundry/monitoring-views/monitoring-faq/)
- [Check groups [Sunset]](https://www.palantir.com/docs/foundry/monitoring-views/check-groups/)
- 

Health checks
- [Overview](https://www.palantir.com/docs/foundry/health-checks/overview/)
- [Types of checks](https://www.palantir.com/docs/foundry/health-checks/check-types/)
- [Check evaluation](https://www.palantir.com/docs/foundry/health-checks/check-evaluation/)
- [Watching checks](https://www.palantir.com/docs/foundry/health-checks/watching-checks/)
- [Notifications and issues](https://www.palantir.com/docs/foundry/health-checks/notifications/)
- [Add health checks to a Marketplace product](https://www.palantir.com/docs/foundry/health-checks/marketplace-data-health/)
- [Builds and checks FAQ](https://www.palantir.com/docs/foundry/health-checks/builds-checks-faq/)
- [Checks reference](https://www.palantir.com/docs/foundry/health-checks/checks-reference/)
- Debugging
- 

AIP observability
- [Overview](https://www.palantir.com/docs/foundry/aip-observability/overview/)
- [Execution history](https://www.palantir.com/docs/foundry/aip-observability/run-history/)
- [Tracing](https://www.palantir.com/docs/foundry/aip-observability/trace-view/)
- [Logging and debugging](https://www.palantir.com/docs/foundry/aip-observability/service-logs-and-debugging/)
- [Log search](https://www.palantir.com/docs/foundry/aip-observability/log-search/)
- [Log permissions](https://www.palantir.com/docs/foundry/aip-observability/log-permissioning/)
- [Metrics](https://www.palantir.com/docs/foundry/aip-observability/metrics/)
- [Performance monitoring and optimization](https://www.palantir.com/docs/foundry/aip-observability/performance-monitoring-and-optimization/)
- [Dashboards](https://www.palantir.com/docs/foundry/observability/dashboards/)[Observability](https://www.palantir.com/docs/foundry/observability/overview/)[AIP observability](https://www.palantir.com/docs/foundry/aip-observability/overview/)[Performance monitoring and optimization](https://www.palantir.com/docs/foundry/aip-observability/performance-monitoring-and-optimization/)

# [](https://www.palantir.com#performance-monitoring-and-optimization)Performance monitoring and optimization

AIP observability provides comprehensive tools to monitor, analyze, and optimize the performance of your workflows and AIP applications. By leveraging trace data, execution metrics, and detailed logs, you can identify bottlenecks, optimize resource usage, and ensure your applications run efficiently at scale.

## [](https://www.palantir.com#why-performance-monitoring-matters)Why performance monitoring matters

Performance monitoring is crucial for:

- **User experience:** Slow workflows can frustrate users and reduce adoption.

- **Cost efficiency:** Optimized workflows use fewer resources and reduce compute costs.

- **Reliability:** Identifying performance issues early prevents outages and failures.

- **Scalability:** Understanding performance characteristics can help you plan for growth.

## [](https://www.palantir.com#identifying-performance-issues)Identifying performance issues

You can use the trace view to identify slow operations.

- **Long-running spans:** Look for operations that take significantly longer than others.

- **Sequential bottlenecks:** Identify operations that could potentially run in parallel.

- **Repeated operations:** Find redundant calls that could be optimized.

- **Model latency:** Monitor LLM response times and consider using different models for time-sensitive operations.

In the screenshot below, you can see an example of AIP observability helping identify unbatched model calls that could be optimized.

![](images/performance-monitoring-and-optimization_workflow-lineage-performance-monitory-models.png)

## [](https://www.palantir.com#optimization-strategies)Optimization strategies

- **Parallel execution:** When possible, design workflows to execute independent operations concurrently.

- **Model selection:** Balance performance and quality by choosing appropriate models for each task.

- **Batch operations:** Group similar operations to reduce overhead.

- **Error handling:** Add proper error handling to prevent cascading failures.
[←PREVIOUSMetrics](https://www.palantir.com/docs/foundry/aip-observability/metrics/)[NEXTDashboards→](https://www.palantir.com/docs/foundry/observability/dashboards/)
© 2026 Palantir Technologies Inc. All rights reserved.
[Cookies Statement ↗](https://www.palantir.com/cookie-statement/)[Privacy Statement ↗](https://www.palantir.com/privacy-and-security/)[Terms of Use ↗](https://www.palantir.com/terms-and-conditions/)Cookie Settings

## Contents

- [Performance monitoring and optimization](https://www.palantir.com#performance-monitoring-and-optimization)
- [Why performance monitoring matters](https://www.palantir.com#why-performance-monitoring-matters)
- [Identifying performance issues](https://www.palantir.com#identifying-performance-issues)
- [Optimization strategies](https://www.palantir.com#optimization-strategies)

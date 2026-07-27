> Source: https://www.palantir.com/docs/foundry/aip-observability/metrics/

- 
- 
- 
- 
- 
- 
- AIP observability • Metrics • Palantir
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
- [Dashboards](https://www.palantir.com/docs/foundry/observability/dashboards/)[Observability](https://www.palantir.com/docs/foundry/observability/overview/)[AIP observability](https://www.palantir.com/docs/foundry/aip-observability/overview/)[Metrics](https://www.palantir.com/docs/foundry/aip-observability/metrics/)

# [](https://www.palantir.com#metrics)Metrics

Foundry provides near real-time metrics for functions, actions, and AIP Logic resources. You can access these metrics through [Ontology Manager](https://www.palantir.com/docs/foundry/ontology-manager/overview/) or in [Workflow Lineage](https://www.palantir.com/docs/foundry/workflow-lineage/overview/) by selecting the resource node for a given execution. These metrics give you visibility into the health and performance of your Ontology and AIP workflows over the last 30 days.

## [](https://www.palantir.com#available-metrics)Available metrics

The following metrics are available for each resource type:

- **Success/failure metrics:** Monitor the current status of your executions with success and failure counts. This enables rapid identification of issues and supports proactive troubleshooting.

![](images/metrics_logic-metric-in-wfl-executions.png)

- **P95 duration metric:** Track the 95th percentile (P95) execution duration. This metric highlights the upper range of execution times, helping you detect performance bottlenecks and optimize workflows.

![](images/metrics_logic-metric-in-wfl-p95.png)

All metrics are updated in near real-time using the latest data from the Foundry Telemetry Service (FTS).

## [](https://www.palantir.com#resource-specific-metrics)Resource-specific metrics

Each resource type has its own metrics page with details on available failure categories and how to access metrics:

- [Function metrics](https://www.palantir.com/docs/foundry/functions/function-metrics/)

- [Action metrics](https://www.palantir.com/docs/foundry/action-types/action-metrics/)

- [AIP Logic metrics](https://www.palantir.com/docs/foundry/logic/logic-metrics/)

## [](https://www.palantir.com#permissions)Permissions

To view metrics, you must be a `viewer` on the resource. For more details, see the [log permissions](https://www.palantir.com/docs/foundry/aip-observability/log-permissioning/) page.

## [](https://www.palantir.com#related-resources)Related resources

- **[Execution history](https://www.palantir.com/docs/foundry/aip-observability/run-history/):** View a complete history of executions over the past 30 days.

- **[Observability Chart widget](https://www.palantir.com/docs/foundry/workshop/widgets-observability-chart/):** Embed metrics in a [Workshop](https://www.palantir.com/docs/foundry/workshop/overview/) application to build operational dashboards.

- **[Function monitoring](https://www.palantir.com/docs/foundry/functions/monitoring/):** Set up alerts for function performance and failure rates.

- **[Action monitoring](https://www.palantir.com/docs/foundry/action-types/monitoring/):** Configure monitoring rules for action performance and reliability.
[←PREVIOUSLog permissions](https://www.palantir.com/docs/foundry/aip-observability/log-permissioning/)[NEXTPerformance monitoring and optimization→](https://www.palantir.com/docs/foundry/aip-observability/performance-monitoring-and-optimization/)
© 2026 Palantir Technologies Inc. All rights reserved.
[Cookies Statement ↗](https://www.palantir.com/cookie-statement/)[Privacy Statement ↗](https://www.palantir.com/privacy-and-security/)[Terms of Use ↗](https://www.palantir.com/terms-and-conditions/)Cookie Settings

## Contents

- [Metrics](https://www.palantir.com#metrics)
- [Available metrics](https://www.palantir.com#available-metrics)
- [Resource-specific metrics](https://www.palantir.com#resource-specific-metrics)
- [Permissions](https://www.palantir.com#permissions)
- [Related resources](https://www.palantir.com#related-resources)

> Source: https://www.palantir.com/docs/foundry/aip-observability/run-history/

- 
- 
- 
- 
- 
- 
- AIP observability • Execution history • Palantir
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
- [Dashboards](https://www.palantir.com/docs/foundry/observability/dashboards/)[Observability](https://www.palantir.com/docs/foundry/observability/overview/)[AIP observability](https://www.palantir.com/docs/foundry/aip-observability/overview/)[Execution history](https://www.palantir.com/docs/foundry/aip-observability/run-history/)

# [](https://www.palantir.com#run-history)Run history

To see the run history for a Function, Action or automation, navigate to the resource, then select the **Run history** tab. This provides a complete view of all executions over the past 30 days.

![](images/run-history_workflow-lineage-run-history.png)

## [](https://www.palantir.com#run-history-data)Run history data

The **Run history** table includes:

- **Timestamp:** When each execution finished.

- **Status:** Success (✓) or failure (✗).

- **Runtime:** Total execution time.

- **Caller:** The resource that triggered the execution; this can be a Workshop application, Agent, Third-party application, Automation, Action, or other system component.

- **Source executor:** The top level executable resource type (limited to Function, Action, or Automation) in the call chain.

The run history displays executions from the past 30 days, sorted by timestamp.

## [](https://www.palantir.com#limitations)Limitations

- **UDFs in Pipeline Builder:** Execution history is not available for user-defined functions (UDFs) run from a sidecar container, such as in [Python](https://www.palantir.com/docs/foundry/functions/python-functions-builder/) or [Java](https://www.palantir.com/docs/foundry/transforms-java/user-defined-functions/) UDFs.

## [](https://www.palantir.com#filter-run-history)Filter run history

You can filter the results by:

- **Status:** View successful or failed executions.

- **Timestamp range:** View executions within a specified date range.

- **User:** View executions triggered by a specific user.

- **Run time range:** View executions within a specified duration range.

- **Version:** View executions for a specified version (only applicable for functions).

- **Caller:** View executions originating from a specified resource.

- **Failure type:** View executions that failed for a specific reason. Learn more about [function](https://www.palantir.com/docs/foundry/functions/function-metrics/#function-failure-types) and [action](https://www.palantir.com/docs/foundry/action-types/action-metrics/#action-failure-types) failure types.

If more than one filter is specified, the results will be filtered to include only those that match all specified filters.

## [](https://www.palantir.com#inspect-a-specific-execution)Inspect a specific execution

To inspect a specific execution, select the **View log details** option to access the full trace and debugging information.

![](images/run-history_workflow-lineage-view-log-details.png)

## [](https://www.palantir.com#next-steps)Next steps

- View [trace details](https://www.palantir.com/docs/foundry/aip-observability/trace-view/) to understand execution flow.

- Access [service logs](https://www.palantir.com/docs/foundry/aip-observability/service-logs-and-debugging/) for detailed debugging.

- Configure [log permissions](https://www.palantir.com/docs/foundry/aip-observability/log-permissioning/) to enable log visibility.
[←PREVIOUSOverview](https://www.palantir.com/docs/foundry/aip-observability/overview/)[NEXTTracing→](https://www.palantir.com/docs/foundry/aip-observability/trace-view/)
© 2026 Palantir Technologies Inc. All rights reserved.
[Cookies Statement ↗](https://www.palantir.com/cookie-statement/)[Privacy Statement ↗](https://www.palantir.com/privacy-and-security/)[Terms of Use ↗](https://www.palantir.com/terms-and-conditions/)Cookie Settings

## Contents

- [Run history](https://www.palantir.com#run-history)
- [Run history data](https://www.palantir.com#run-history-data)
- [Limitations](https://www.palantir.com#limitations)
- [Filter run history](https://www.palantir.com#filter-run-history)
- [Inspect a specific execution](https://www.palantir.com#inspect-a-specific-execution)
- [Next steps](https://www.palantir.com#next-steps)

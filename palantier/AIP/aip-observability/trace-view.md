> Source: https://www.palantir.com/docs/foundry/aip-observability/trace-view/

- 
- 
- 
- 
- 
- 
- AIP observability • Tracing • Palantir
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
- [Dashboards](https://www.palantir.com/docs/foundry/observability/dashboards/)[Observability](https://www.palantir.com/docs/foundry/observability/overview/)[AIP observability](https://www.palantir.com/docs/foundry/aip-observability/overview/)[Tracing](https://www.palantir.com/docs/foundry/aip-observability/trace-view/)

# [](https://www.palantir.com#trace-views)Trace views

The **Trace** view provides a visual timeline of your workflow execution, showing how different services interact and where time is spent. Specifically, a *distributed trace* is the timeline comprising all of the events between the generation of a request and the receipt of a response; these events can cross process, network and security boundaries. Distributed traces are key to understanding the path a request takes within your application.

## [](https://www.palantir.com#permission-required)Permission required

To view traces and service logs, an administrator must enable [log access](https://www.palantir.com/docs/foundry/aip-observability/log-permissioning/) for the relevant project. Users always have access to logs for their own executions from the past 24 hours, except on [CBAC stacks](https://www.palantir.com/docs/foundry/security/classification-based-access-controls/), where log access must be enabled to view trace and service logs.

## [](https://www.palantir.com#key-elements-of-the-trace-view)Key elements of the trace view

![](images/trace-view_workflow-lineage-trace-view.png)

- **Timeline visualization:** Horizontal bars show the duration of each operation.

- **Service hierarchy:** Nested spans show parent-child relationships between operations.

- **Resource types:** Coloring indicating whether each span was produced from a function, action, automation, model, or LLM call.

- **Performance metrics:** Each span displays its execution time.

## [](https://www.palantir.com#analyzing-trace-details)Analyzing trace details

You can select any span to see the full **Trace Log Details** for that specific operation.

Trace details include:

- **Operation name:** The specific function, action, language model, automation, model, or inner operation being executed.

- **Duration:** Execution time for the operation.

- **Input/output data:** For Function execution requests, you can view the parameters passed to and returned from the operation.

- **Model interactions:** For LLM calls, you can view the prompt, response, and token usage.

- **Error information:** Stack traces and error messages for failed operations.

- **Trace identifiers:** `foundryTraceId`, the Foundry-assigned identifier used to fetch telemetry, and `x-b3-traceid`, the standard distributed-tracing identifier included in the **tags** field on each service log entry (best-effort; may be absent on logs originating outside Foundry, such as applications built with the Ontology SDK).

![](images/trace-view_workflow-lineage-trace-log-details.png)

## [](https://www.palantir.com#related-features)Related features

- [Execution history](https://www.palantir.com/docs/foundry/aip-observability/run-history/): View all recent executions before diving into traces.

- [Service logs](https://www.palantir.com/docs/foundry/aip-observability/service-logs-and-debugging/): Access detailed log messages for each span.

- [Performance monitoring](https://www.palantir.com/docs/foundry/aip-observability/performance-monitoring-and-optimization/): Analyze trace data to identify optimization opportunities.
[←PREVIOUSExecution history](https://www.palantir.com/docs/foundry/aip-observability/run-history/)[NEXTLogging and debugging→](https://www.palantir.com/docs/foundry/aip-observability/service-logs-and-debugging/)
© 2026 Palantir Technologies Inc. All rights reserved.
[Cookies Statement ↗](https://www.palantir.com/cookie-statement/)[Privacy Statement ↗](https://www.palantir.com/privacy-and-security/)[Terms of Use ↗](https://www.palantir.com/terms-and-conditions/)Cookie Settings

## Contents

- [Trace views](https://www.palantir.com#trace-views)
- [Permission required](https://www.palantir.com#permission-required)
- [Key elements of the trace view](https://www.palantir.com#key-elements-of-the-trace-view)
- [Analyzing trace details](https://www.palantir.com#analyzing-trace-details)
- [Related features](https://www.palantir.com#related-features)

> Source: https://www.palantir.com/docs/foundry/aip-observability/service-logs-and-debugging/

- 
- 
- 
- 
- 
- 
- AIP observability • Logging and debugging • Palantir
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
- [Dashboards](https://www.palantir.com/docs/foundry/observability/dashboards/)[Observability](https://www.palantir.com/docs/foundry/observability/overview/)[AIP observability](https://www.palantir.com/docs/foundry/aip-observability/overview/)[Logging and debugging](https://www.palantir.com/docs/foundry/aip-observability/service-logs-and-debugging/)

# [](https://www.palantir.com#service-logs-and-debugging)Service logs and debugging

To access detailed logging information, navigate to the **Details** view after selecting the **View log details** option for a specific execution.

The service logs provide:

- **Chronological log entries:** All log messages generated during execution.

- **Log levels:** `INFO`, `WARN`, `ERROR`, `DEBUG`, and `TRACE` messages.

- **Custom log messages:** Any console.log() or logging statements from your functions or models.

![](images/service-logs-and-debugging_workflow-lineage-service-logs.png)

## [](https://www.palantir.com#permission-required)Permission required

To view traces and service logs, an administrator must enable [log access](https://www.palantir.com/docs/foundry/aip-observability/log-permissioning/) for the relevant project. Users always have access to logs for their own executions from the past 24 hours, except on [CBAC stacks](https://www.palantir.com/docs/foundry/security/classification-based-access-controls/), where log access must be enabled to view trace and service logs.

## [](https://www.palantir.com#filtering-logs)Filtering logs

To filter for specific log levels, use the **log levels** selector at the top of the table:

![](images/service-logs-and-debugging_workflow-lineage-service-log-filter.png)

Available log levels:

- **ERROR:** Error messages and stack traces

- **WARN:** Warnings about potential issues

- **INFO:** General information about execution flow

- **DEBUG:** Detailed debugging information

- **TRACE:** Detailed trace information

To see the full details of any log entry, select the **Content** field:

![](images/service-logs-and-debugging_workflow-lineage-service-log-details.png)

## [](https://www.palantir.com#writing-effective-logs-in-your-functions)Writing effective logs in your functions

Effective logging helps you debug issues quickly and understand your function&#x27;s behavior in production. Follow these best practices:

### [](https://www.palantir.com#choose-appropriate-log-levels)Choose appropriate log levels

- **INFO:** Use for normal operation flow and key business events.

- **WARN:** Use for recoverable issues or unexpected conditions that don&#x27;t prevent execution.

- **ERROR:** Use for failures that prevent normal operation.

- **DEBUG:** Use for detailed diagnostic information (avoid in production).

### [](https://www.palantir.com#include-relevant-context)Include relevant context

We recommend including identifiers and relevant data that can help you understand what has happened:

TypeScript v1TypeScript v2
Copied!

`1
2
3
4
5
``// TypeScript v1 example - Good logging practices
console.log("Processing order", orderId, "for user", userId); // Include relevant IDs
console.log("Retrieved", results.length, "items from Ontology"); // Include counts/metrics
console.warn("Retry attempt", attemptNumber, "of", maxRetries, "for operation", operationId); // Include retry context
console.error("Failed to process order", orderId, "Error:", error.message); // Include error details`
```

Copied!

`1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
``import { logs } from "@opentelemetry/api-logs";
const logger = logs.getLogger("my-function");

// TypeScript v2 example - Good logging practices
logger.emit({
 severityText: "INFO",
 attributes: { LOG_MESSAGE: `Processing order ${orderId} for user ${userId}` }, // Include relevant IDs
 body: { orderId, userId },
});
logger.emit({
 severityText: "WARN",
 attributes: { LOG_MESSAGE: `Retry attempt ${attemptNumber} of ${maxRetries} for operation ${operationId}` }, // Include retry context
 body: { attemptNumber, maxRetries, operationId },
});
logger.emit({
 severityText: "ERROR",
 attributes: { LOG_MESSAGE: `Failed to process order ${orderId}. Error: ${error.message}` }, // Include error details
 body: { orderId, error: error.message },
});`
```

### [](https://www.palantir.com#avoid-logging-sensitive-data)Avoid logging sensitive data

Never log sensitive information that could compromise security:

Copied!

`1
2
3
4
5
6
7
``// ❌ Don&#x27;t do this
console.log("User credentials", username, password);
console.log("API response", fullApiResponse); // May contain sensitive data

// ✅ Do this instead
console.log("Authentication attempt for user", username);
console.log("API call completed with status", response.status);`
```

## [](https://www.palantir.com#see-also)See also

- [Log search](https://www.palantir.com/docs/foundry/aip-observability/log-search/): Search across logs from all executions for a source executor.

- [Log permissions](https://www.palantir.com/docs/foundry/aip-observability/log-permissioning/): Configure who can view logs.

- [Trace view](https://www.palantir.com/docs/foundry/aip-observability/trace-view/): Correlate logs with execution timeline.
[←PREVIOUSTracing](https://www.palantir.com/docs/foundry/aip-observability/trace-view/)[NEXTLog search→](https://www.palantir.com/docs/foundry/aip-observability/log-search/)
© 2026 Palantir Technologies Inc. All rights reserved.
[Cookies Statement ↗](https://www.palantir.com/cookie-statement/)[Privacy Statement ↗](https://www.palantir.com/privacy-and-security/)[Terms of Use ↗](https://www.palantir.com/terms-and-conditions/)Cookie Settings

## Contents

- [Service logs and debugging](https://www.palantir.com#service-logs-and-debugging)
- [Permission required](https://www.palantir.com#permission-required)
- [Filtering logs](https://www.palantir.com#filtering-logs)
- [Writing effective logs in your functions](https://www.palantir.com#writing-effective-logs-in-your-functions)
- [See also](https://www.palantir.com#see-also)

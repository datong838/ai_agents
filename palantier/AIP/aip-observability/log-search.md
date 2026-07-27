> Source: https://www.palantir.com/docs/foundry/aip-observability/log-search/

- 
- 
- 
- 
- 
- 
- AIP observability • Log search • Palantir
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
- [Dashboards](https://www.palantir.com/docs/foundry/observability/dashboards/)[Observability](https://www.palantir.com/docs/foundry/observability/overview/)[AIP observability](https://www.palantir.com/docs/foundry/aip-observability/overview/)[Log search](https://www.palantir.com/docs/foundry/aip-observability/log-search/)

# [](https://www.palantir.com#log-search)Log search

The **Search logs** tab in [Workflow Lineage](https://www.palantir.com/docs/foundry/workflow-lineage/overview/) allows you to search across all [service logs](https://www.palantir.com/docs/foundry/aip-observability/service-logs-and-debugging/) produced by a selected source executor over the past 30 days. Unlike the per-execution service logs view, log search aggregates logs from every execution originating from a given source executor, making it useful for investigating recurring errors or finding specific log messages across multiple runs.

A source executor is the first executable resource in the call chain and can be a function, action, automation, AIP logic, AIP agent, or model live deployment. When a function is backed by another resource, such as AIP logic, a language model, or an AIP agent, the log search panel displays the backing resource as the source executor rather than the underlying function.

## [](https://www.palantir.com#accessing-log-search)Accessing log search

To access log search:

- Open [Workflow Lineage](https://www.palantir.com/docs/foundry/workflow-lineage/overview/) and navigate to the workflow containing your resource.

- Select an executable resource node.

- Select the **Search logs** tab in the bottom panel.

![](images/log-search_workflow-lineage-log-search.png)

## [](https://www.palantir.com#searching-logs)Searching logs

The search bar at the top of the **Search logs** panel accepts text queries. Type a search term and the results will populate the results table. The search is case-sensitive and matches against the full log line, including both the **Message** and **Content** fields.

You can use `*` as a wildcard character to match any sequence of characters. For example:

- `connection failed` matches log lines containing the exact phrase "connection failed"

- `timeout*retry` matches log lines containing "timeout" followed by "retry" with any characters in between

- `Error` matches "Error" but not "error" or "ERROR"

![](images/log-search_log-search-automate.png)

The Search logs tab displays logs for executions where the selected resource is the *source executor*. Logs from executions where the resource was called by another resource are not included. In the example below, the function produced logs during execution but is not the source executor — it was called by an automation. Searching from the function returns no results; to find these logs, search from the automation node instead.

### [](https://www.palantir.com#source-executor-suggestions)Source executor suggestions

If no logs are found for the selected resource, the **Search logs** panel checks whether it was recently called by other source executors and displays them as suggestions. Select a suggested source executor to navigate to that node in the graph and search its logs instead. The panel header also displays an **Also recently executed by** indicator. You can select this indicator to see and navigate to source executors.

![](images/log-search_log-search-function-no-logs.png)

## [](https://www.palantir.com#filter-results)Filter results

The filter sidebar on the left side of the **Search logs** panel allows you to narrow down log results. Select the filter icon to expand or collapse the sidebar. The following filters are available:

- **Log level:** Filter logs by severity level. Select a log level from the dropdown to show only logs matching that level. The available levels are `ERROR`, `FATAL`, `WARN`, `INFO`, `DEBUG`, and `TRACE`. By default, all log levels are shown.

- **Timestamp range:** Restrict results to a specific time window. You can choose from predefined relative ranges such as `Past 1 day` or `Past 1 hour`, or specify a custom date and time range. The default range `Past one day`. The maximum selectable range is 30 days, matching the log retention period.

- **Producing resource:** Filter logs by the resource that produced them. Use this filter when a source executor&#x27;s call chain includes multiple downstream resources and you want to isolate logs from a specific function, action, automation, AIP logic, or AIP agent. Select the clear button next to the filter to remove the selection.

When multiple filters are active, they are combined with `AND` logic; only log entries matching all selected filters are returned. Select **Reset** in the sidebar header to clear all filters and return to the default view.

## [](https://www.palantir.com#understanding-the-results-table)Understanding the results table

Search results are displayed in a table sorted by timestamp, with the most recent logs appearing first. The table includes the following columns:

ColumnDescription**Log level**A color-coded icon indicating the severity: red for `ERROR` and `FATAL`, orange for `WARN`, and neutral for `INFO`, `DEBUG`, and `TRACE`**Timestamp**The date and time the log entry was recorded**Message**The primary log message. Select the field to open a detail dialog**Content**Additional structured content, often in JSON format. Select the field to open a detail dialog**Producing resource**The resource that emitted the log entry

Matching text from your search query is highlighted in the **Message** and **Content** columns.

When you hover over a log row, a **View trace** button appears on the right side of the row. Select this button to open the [trace view](https://www.palantir.com/docs/foundry/aip-observability/trace-view/) for the execution that produced that log entry. This allows you to see the full execution timeline and identify where in the call chain the log was emitted.

![](images/log-search_log-search-view-trace.png)

## [](https://www.palantir.com#viewing-log-details)Viewing log details

Select any **Message** or **Content** cell to open a detail dialog with the full log entry. The dialog provides:

- **Message** and **Content** tabs to switch between the two fields

- A text search bar to find specific content within the log entry

- A **Wrap lines** toggle for easier reading of long log lines

- Automatic JSON formatting for structured content

![](images/log-search_log-search-log-details.png)

## [](https://www.palantir.com#log-retention-and-pagination)Log retention and pagination

Log search covers the most recent 30 days of logs. Logs older than 30 days are automatically deleted and cannot be recovered. Results are loaded in pages of 100 entries. Scroll to the bottom of the table to load additional results. Logs are not streamed live; to view additional logs produced after the initial search, refresh the page.

## [](https://www.palantir.com#permissions)Permissions

Log search uses the same permission model as [execution history](https://www.palantir.com/docs/foundry/aip-observability/run-history/). To search logs for a resource, you must have **edit** permission on the resource. If log access has been enabled for the source executor&#x27;s project, and you have access to all the necessary markings, you can search logs across all executions. If log access has not been enabled, you can only search logs for your own executions from the past 24 hours, but **edit** permission on the resource is still required. On [CBAC stacks](https://www.palantir.com/docs/foundry/security/classification-based-access-controls/), this self-execution exception does not apply; log access must be enabled to search logs.

![](images/log-search_log-search-action-no-perms.png)

For full details on log access configuration, see [log permissions](https://www.palantir.com/docs/foundry/aip-observability/log-permissioning/).

## [](https://www.palantir.com#related-features)Related features

- [Service logs](https://www.palantir.com/docs/foundry/aip-observability/service-logs-and-debugging/): View logs for a specific execution

- [Execution history](https://www.palantir.com/docs/foundry/aip-observability/run-history/): Browse all recent executions for a resource

- [Trace views](https://www.palantir.com/docs/foundry/aip-observability/trace-view/): Visualize the execution timeline and correlate with log data

- [Log permissions](https://www.palantir.com/docs/foundry/aip-observability/log-permissioning/): Configure who can access logs
[←PREVIOUSLogging and debugging](https://www.palantir.com/docs/foundry/aip-observability/service-logs-and-debugging/)[NEXTLog permissions→](https://www.palantir.com/docs/foundry/aip-observability/log-permissioning/)
© 2026 Palantir Technologies Inc. All rights reserved.
[Cookies Statement ↗](https://www.palantir.com/cookie-statement/)[Privacy Statement ↗](https://www.palantir.com/privacy-and-security/)[Terms of Use ↗](https://www.palantir.com/terms-and-conditions/)Cookie Settings

## Contents

- [Log search](https://www.palantir.com#log-search)
- [Accessing log search](https://www.palantir.com#accessing-log-search)
- [Searching logs](https://www.palantir.com#searching-logs)
- [Filter results](https://www.palantir.com#filter-results)
- [Understanding the results table](https://www.palantir.com#understanding-the-results-table)
- [Viewing log details](https://www.palantir.com#viewing-log-details)
- [Log retention and pagination](https://www.palantir.com#log-retention-and-pagination)
- [Permissions](https://www.palantir.com#permissions)
- [Related features](https://www.palantir.com#related-features)

# 128 · W-L20 ToolBinding resolver + Bundle publisher 1.3.0

> 状态：`GREEN` · 2026-08-20  
> 清单：`59` §8.5 **W-L20** · 上游 19/49、W6-01、W-L4 assignee  
> 证据：`aos-platform-w1-aip/.evidence/aip/2026-08-20-w-l20-toolbinding-resolver/`  
> 边界：仅 `aos-platform-w1-aip`；防租户全局误点亮；不改 w2

## 1. 目标

1. **AssigneeResolutionReceipt**：四 kind（Human / Agent / Tool / Provider）真实解析收据  
2. **ToolBinding resolver**：缺 exact 绑定 fail-closed，禁止「租户有任一 tool 就全局点亮」  
3. Bundle publisher 契约对齐 **1.3.0**（锁测）  
4. 解析结果可被 ProductionStart / Overlay 消费，不得 silent fallback 到全局 catalog

## 2. 不做

- 前端工具面板大改版  
- 伪造跨租户 Provider 可用性  
- 在无 ToolBinding 时用 Capability 名冒充已解析 Tool

## 3. 实现

- Migration `aip13_001`：`aip_tool_binding` + `aip_assignee_resolution_receipt`  
- API：`POST /v1/aip/assignee-authority/tool-bindings`、`POST .../resolutions`  
- ToolBinding 必须绑定 `agent_instance_id`（非空），缺绑定 → `TOOL_BINDING_MISSING`

## 4. 验收

- [x] 四 kind resolver + Receipt 持久化（本波覆盖 Human/Tool + Publisher 锁；Agent/Provider 路径在 store 内）  
- [x] 负向：无实例绑定 → blocked  
- [x] publisher bundleVersion == 1.3.0 锁测  
- [x] pytest GREEN

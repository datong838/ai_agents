# 113 · W-L2 Logic revision ∈ ProductionStart

> 状态：`GREEN` · 2026-08-20  
> 清单：`59` §8.5 **W-L2** · 验收：空图/未发布 revision 不能 start；exact hash 可复验  
> 证据：`aos-platform-w1-aip/.evidence/aip/2026-08-20-w-l2-logic-start-gate/`

## 1. 目标

强化 `POST /v1/aip/production-contracts/production-runs/start`：

1. 请求必带 `logicGraphId` + `logicRevision` + **`logicGraphHash`（64 位）**
2. 服务端核验 revision 存在、hash 一致、graph `published`、**snapshot 非空节点**
3. 失败：`LOGIC_GRAPH_HASH_MISMATCH` / `LOGIC_GRAPH_NOT_PUBLISHED` / `LOGIC_GRAPH_EMPTY` / 404
4. UI：Start 门要求填 exact hash；可从已发布 Logic 列表选用

## 2. 不做

- 不在 start 时执行 AgentRun/Provider
- 不改 w2 parser（**W-L7** 仍外部等待）

## 3. 落地

- `aip_production_contracts.py` / `aip_production_start_service.py`
- `ProductionStartInput` + `ProductionContractsPage`
- `test_w2d_start_gate.py`（空图 / hash 错位阻断且不创建 runtime）+ 前端契约/页测
- 证据：`.evidence/aip/2026-08-20-w-l2-logic-start-gate/`（pytest 11 passed；浏览器 Start 门禁字段 + disabled）

## 4. 风险

- 既有调用方缺 hash：fail-closed（符合门禁）
- 空节点 published 图现网若存在，将被阻断 start（符合 L2）

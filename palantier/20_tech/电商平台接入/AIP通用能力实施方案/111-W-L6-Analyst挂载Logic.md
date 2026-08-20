# 111 · W-L6 Analyst 挂载 Logic（联 J6）

> 状态：`GREEN` · 2026-08-20  
> 证据：`.evidence/aip/2026-08-20-w-l6-analyst-logic-mount/` · 挂载 `ecommerce.logic.V01@r1`  
> 清单：`59` §8.5 / §7.10 **W-L6** · 验收：Analyst 可引用真实 Logic revision；缺权威时 blocked，无假数

## 1. 目标

在 `/aip/analyst`（J6 真实查询之上）增加 **Logic 挂载点**：

1. 从 `/v1/aip/logic/graphs` 读取已保存图；空列表诚实阻断，不注入演示图
2. 选中后展示 exact `id@revision` + `graph_hash`，并可深链 `/aip/logic?graph=`
3. URL 可携带 `logicId` / `logicRevision` / `logicHash`，刷新后仍挂同一 revision
4. 证据栏显示当前挂载；无图时文案明确「不可派发 / 不可冒充 TaskGraph」

## 2. 不做

- 不做完整 TaskGraph materialize / QueryJob（**W-L17**）
- 不改 w2；不伪造 Skill/Task refs
- 不把挂载当成已执行 Logic

## 3. 最小改动

- `AipAnalystPage.tsx`：listLogicGraphs + 挂载 UI + URL 同步
- 单测：空图 blocked；有图可选中 exact
- 证据：`.evidence/aip/2026-08-20-w-l6-analyst-logic-mount/`

## 4. 风险

- Logic API 失败：与 Object Type 同口径，显示错误、禁用挂载
- 仅 persisted 图可挂；未保存草稿不进列表

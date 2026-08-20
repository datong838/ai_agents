# 110 · W-J6 Analyst 真实查询（无演示假数）

> 状态：`GREEN` · 2026-08-20  
> 证据：`.evidence/aip/2026-08-20-w-j6-analyst-query/` · Order `niushop:1:1`  
> 清单：`59` §7.10 **W-J6** · 验收：语义查询走权威 API，无演示行/本地编造结果

## 1. 目标

`/aip/analyst` 运行受治理查询时：

1. Object Type 下拉来自租户已安装 ontology（`/v1/ontology/object-types`），不硬编码演示类型
2. 结果只展示 `POST /v1/aip/analyst/query` 回包；blocked/empty/error 保持诚实空态
3. 浏览器验收：对真实类型（如 `Order`）跑出 `complete` 且行 ID 来自 ontology，非 `demo-*`

## 2. 不做

- 不全量 AIP-8 QueryJob 异步编排（属 **W-L17** / **W-K07**）
- 不装配地图底图 / Metric adapter（缺则诚实不适用）
- 不改 w2-workshop

## 3. 最小改动

- `AipAnalystPage.tsx`：拉取已发布 object types；无类型时禁用运行并说明
- 证据：API JSON + 浏览器截图入 `.evidence/aip/2026-08-20-w-j6-analyst-query/`

## 4. 风险

- ontology 空：页面保持阻断，不算假 GREEN
- 时钟：cutoff 不得晚于服务端 now（页面已用 `new Date().toISOString()`）

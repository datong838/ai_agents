# 10f · 知识检索幽灵 dataset_ids 说明

> 日期：2026-07-16  
> 范围：本机 Dify Chatflow「知识库实验辅助」  
> 原则：**不是操作失误**；UI 无法删幽灵 ID；先改数据，源码侧记缺陷。

## 现象

- 编排页知识检索只显示 `qiyuehui-kb`，看不到另外两个库，也删不掉。
- 每次「只勾 qiyuehui-kb → 保存/发布」后，DB 里 `dataset_ids` 仍可能残留 2 个已删库 UUID。
- 一般不影响经济库 N 路召回（API 会忽略不存在的 dataset），但属于脏数据。

## 根因（代码缺陷 + 数据残留）

文件：`mybuddy-v01/dify/web/.../knowledge-retrieval/hooks/use-knowledge-dataset-selection.ts`

加载节点时：

1. 用完整 `dataset_ids` 调 `/datasets?ids=...`，接口只返回**仍存在**的库 → UI 只画 `qiyuehui-kb`。
2. 写回节点时却执行 `draft.dataset_ids = datasetIds`（**原数组未裁剪**）→ 幽灵 ID 一直留在 graph。
3. 用户在 UI 上「看不见 → 删不了」；若未触发真正改写列表的 `onChange`，发布仍带着幽灵 ID。

结论：**上游 Dify 前端缺陷**（展示与持久化不一致），不是试用人员漏操作。

## 修复方案（最小）

| 步骤 | 动作 | 风险 |
| --- | --- | --- |
| 1 | SQL：draft + 当前已发布 workflow 的知识检索节点 `dataset_ids` 只保留真实库 `2456acc6-91c7-4bcf-8632-471527c9d986` | 低；仅改该 app 的 graph JSON |
| 2 | 源码补丁：加载后将 `dataset_ids` 收敛为接口返回的 id 列表 | 当前 Web 跑 Docker 镜像，补丁需重建前端才生效；本仓保留补丁便于二期 |
| 3 | 故障话术补充一行 | 无 |

**不做**：全库扫描、改 Dify API、装 OpenAI、新建应用。

## 自检

```sql
-- 期望 ds 仅 1 个 id，且等于 qiyuehui-kb
SELECT version, graph::jsonb->'nodes'->1->'data'->'dataset_ids' AS ds
FROM workflows
WHERE app_id='804cfc3a-088f-4cb4-9588-dd613568438e'
  AND (version='draft' OR version NOT IN ('draft'))
ORDER BY created_at DESC
LIMIT 2;
```

## 回滚

从 workflows 历史版本恢复 graph（本库保留多次 publish 快照）；或重新在 UI 添加知识库后发布。

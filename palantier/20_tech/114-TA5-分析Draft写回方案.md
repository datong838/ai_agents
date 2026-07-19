# 114 · TA.5 分析 → Draft 写回方案

| 字段 | 内容 |
|------|------|
| 状态 | **已落地** |
| 关联 | [73](./73-产品1.3分析建模下一阶段方案.md) **TA.5** · [113](./113-TA4-分析读数方案.md) · Draft `/v1/aip/drafts` · TB.4 lineage |
| 索引口径 | **v1.0.83** |

## 1. 目标 / 非目标

**目标（DoD）**

- `/analytics` 可把读数上下文 **提交为 Draft**（`productionWritten=false`）。
- **禁止**分析员自批：`autoApprove=true` → **400**；本页无「批准写生产」按钮。
- 批准仍走 **Draft 审批台**（既有 `POST /v1/aip/drafts/{id}/approve`）→ 对象变更 + `decision_lineage`（复用 TB.4 路径）。
- 需 **Idempotency-Key**（与 Action execute HITL 同形）。

**非目标**

- 分析页内一键写生产 / papermill 批量跑 notebook。
- Dataset 物理湖文件写回（仍走对象 props / 既有 Action）。
- Marking 导出治理加深（TA.6）。

## 2. 架构

```
/analytics 读数结果
      │ POST /v1/analytics/writeback/propose + Idempotency-Key
      ▼
  draft_dataset (status=proposed)  ← 不写 obj_instance
      │
      │ 审批台 POST .../approve（非分析员自批）
      ▼
  apply_draft_approval → obj_instance + decision_lineage
```

## 3. 契约

### `POST /v1/analytics/writeback/propose`

| 字段 | 说明 |
|------|------|
| `objectType` | 必填 |
| `objectId` | 必填 |
| `proposed` | 变更字段；CloseWorkOrder 需 `reason` |
| `actionTypeId` | 默认 `CloseWorkOrder` |
| `title` | 可选 |
| `analysisNote` | 可选；写入 `proposed.analysisNote`，并在缺 `reason` 时回填 |
| `autoApprove` | 若 true → **400** `ANALYTICS_SELF_APPROVE_FORBIDDEN` |
| Header `Idempotency-Key` | **必填** |

成功 **201/200**：

```json
{
  "mode": "ta5-writeback",
  "id": "draft-...",
  "status": "proposed",
  "productionWritten": false,
  "approvePath": "/aip/drafts",
  "actionTypeId": "CloseWorkOrder",
  "objectType": "WorkOrder",
  "objectId": "wo-1001",
  "proposed": { "reason": "...", "status": "closed", "analysisNote": "..." }
}
```

## 4. UI

| 控件 | 行为 |
|------|------|
| objectId / status / reason | 可读数结果预填 |
| **提交为 Draft** | 调 propose；展示 draftId |
| 链接「Draft 审批台」 | 去批准；**本页无批准钮** |

诚实文案：提交 ≠ 写生产；须审批后生效并记 lineage。

## 5. 工程落点

| 路径 | 说明 |
|------|------|
| `aos_api/routers/analytics.py` | `writeback/propose` |
| `apps/web/.../analytics.tsx` | 写回表单 |
| OpenAPI | 登记 |
| `tests/test_analytics_ta5_114.py` | 单测 |

## 6. 验收

```text
# propose
curl -X POST .../v1/analytics/writeback/propose \
  -H "Idempotency-Key: ta5-1" -d '{"objectType":"WorkOrder","objectId":"wo-1001","proposed":{"reason":"from-analytics","status":"closed"}}'
# → productionWritten=false

# approve（审批台路径）
curl -X POST .../v1/aip/drafts/{id}/approve -H "Idempotency-Key: ta5-appr"
# → lineageId · 对象变更

pytest tests/test_analytics_ta5_114.py -q
```

## 7. 风险

| 风险 | 缓解 |
|------|------|
| 误做成自批 | 显式拒 autoApprove；UI 无批准钮 |
| Action criteria 失败 | 透传 VALIDATION；UI 提示填 reason |
| 与 demo run-story 混淆 | 分析路径不自动 approve |

## 8. 下一刀

~~**TA.6**~~ → ✅ [115](115-TA6-分析治理方案.md)。下一刀 **TA.7** 演示故事。

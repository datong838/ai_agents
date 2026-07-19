# 112 · TA.3 Ontology 左栏插片段方案

| 字段 | 内容 |
|------|------|
| 状态 | **已落地** |
| 关联 | [73](./73-产品1.3分析建模下一阶段方案.md) **TA.3** · [111](./111-TA2-Facade会话票据方案.md) · Ontology `/v1/ontology/*` · `/v1/objects/*` · `/v1/datasets` |
| 索引口径 | **v1.0.81** |

## 1. 目标 / 非目标

**目标（DoD）**

- `/analytics` 页具备 **左栏**：Object Type · 实例（抽样）· Dataset。
- 点击项 → 向「单元格缓冲」**插入可运行意图的代码片段**（pandas/aos 风格占位）。
- 数据来自 **真 Facade 聚合**（PG Ontology + 现有 datasets 目录），非前端写死假目录。
- 创建会话可带当前选中的 `objectType` 上下文。

**非目标（→ TA.4+）**

- 真 Notebook 7 单元格执行 / Arrow 读数（TA.4）。
- 写回 Draft（TA.5）；左栏插入 **只读探索片段**，不直接写生产。
- 完整对象浏览器 / 属性编辑（走 Ontology 深页）。

## 2. 架构

```
/analytics 页
  ┌─────────────┬──────────────────────────┐
  │ Ontology 左栏│ 会话 · 单元格缓冲 · health │
  │ OT / 实例   │ 点击左栏 → append snippet │
  │ Dataset     │ Copy · 清空 · 开 uiUrl    │
  └─────────────┴──────────────────────────┘
         ▲
         │ GET /v1/analytics/ontology-rail
         ▼
      aos-api（聚合 object-types + objects 抽样 + datasets）
```

## 3. 契约

### `GET /v1/analytics/ontology-rail`

Auth：Bearer。

响应：

```json
{
  "mode": "ta3-rail",
  "objectTypes": [
    {
      "id": "WorkOrder",
      "name": "WorkOrder",
      "kind": "objectType",
      "snippet": "# ...\ndf = aos.objects.list(\"WorkOrder\")\n",
      "instances": [
        {
          "id": "wo-1001",
          "kind": "object",
          "snippet": "obj = aos.objects.get(\"WorkOrder\", \"wo-1001\")\n"
        }
      ]
    }
  ],
  "datasets": [
    {
      "rid": "ri.dataset....",
      "name": "WorkOrder-demo",
      "kind": "dataset",
      "snippet": "df = aos.datasets.preview(\"ri.dataset....\", limit=100)\n"
    }
  ]
}
```

| 参数 | 说明 |
|------|------|
| `typeLimit` | OT 最多条数，默认 20，最大 50 |
| `instanceLimit` | 每类型实例抽样，默认 5，最大 20 |
| `datasetLimit` | Dataset 最多条数，默认 20，最大 50 |

片段约定：

- 使用 `aos.objects.*` / `aos.datasets.*` **占位 API**（TA.4 绑真读数）。
- 注释标明 `# TA.4 binds`；禁止暗示已写生产。

## 4. UI

| 区域 | 行为 |
|------|------|
| 左栏 · Object Types | 列表；展开见实例；点 OT/实例 → append snippet |
| 左栏 · Datasets | 点行 → append snippet |
| 主区 · 单元格缓冲 | textarea；Copy / 清空 |
| 主区 · 会话 | 沿用 TA.2；创建时带 `selectedObjectType` |

诚实文案：左栏插片段 ≠ 内核已执行；读数属 TA.4。

## 5. 工程落点

| 路径 | 说明 |
|------|------|
| `aos_api/routers/analytics.py` | `ontology-rail` |
| `apps/web/.../analytics.tsx` | 双栏布局 |
| `packages/contracts/openapi/v1.yaml` | 路径登记 |
| `tests/test_analytics_ta3_112.py` | 单测 |

## 6. 验收

```text
curl -H "Authorization: Bearer dev" http://127.0.0.1:8080/v1/analytics/ontology-rail
# → objectTypes / datasets 非空（有种子时）· 每项含 snippet

pytest tests/test_analytics_ta3_112.py -q
# 打开 /analytics：点 WorkOrder → 缓冲出现 list 片段
```

## 7. 风险

| 风险 | 缓解 |
|------|------|
| OT 很多导致慢 | limit + 实例抽样 |
| datasets 仅内存目录 | 与现有 `/v1/datasets` 同源；空则诚实空列表 |
| 片段不可执行 | 标注 TA.4；不宣称已跑通 pandas |

## 8. 下一刀

~~**TA.4**~~ → ✅ [113](113-TA4-分析读数方案.md)。下一刀 **TA.5** Draft 写回。

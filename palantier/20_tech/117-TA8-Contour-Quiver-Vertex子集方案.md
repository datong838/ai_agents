# 117 · TA.8 Contour / Quiver / Vertex 子集一页方案

| 字段 | 内容 |
|------|------|
| 状态 | **已落地** |
| 关联 | [73](./73-产品1.3分析建模下一阶段方案.md) **TA.8** · [116](./116-TA7-分析演示故事方案.md) · [115](./115-TA6-分析治理方案.md) |
| 索引口径 | **v1.0.86** |

## 1. 目标 / 非目标

**目标（DoD）**

- `/analytics` 内 **探索分析**三块：分组 · 时序 · 实验登记（产品面无「演示 / TA.*」文案）。
- Facade API 真读/真写（KV 实验登记）；数据来自 ObjectSet / decision_lineage。
- 不进包：Superset / Metabase / Grafana / MLflow Server / 分布式训练。

**非目标**

- Contour/Quiver/Vertex **全集**或「基于 Superset 的 AOS」。
- Plotly/ECharts 新依赖（本刀用 CSS 条形 + 表；图表库后置）。
- 真 Jupyter 训模型 / sklearn 内核预装（Vertex 仅实验元数据 + 可选 MediaSet 挂接）。

## 2. API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/analytics/contour/explore` | `objectType` + `groupBy`（默认 `status`）→ 分桶计数 |
| GET | `/v1/analytics/quiver/series` | `objectType` → 按 `decision_lineage.created_at` 日桶（无谱系则空系列诚实） |
| GET | `/v1/analytics/vertex/experiments` | 列出实验（`meta_aip_kv`） |
| POST | `/v1/analytics/vertex/experiments` | 登记实验（name/params/metrics/mediaRid）；**不**写 Ontology |

响应一律带 `mode: ta8-*-subset` · `disclaimer` · `productionWritten: false`（Vertex 登记除外仍不写生产对象）。

## 3. UI

`/analytics` 主栏下方增加 **「探索子集 · TA.8」**：

- 三 Tab：Contour / Quiver / Vertex。
- Banner：**子集可讲 · 非全集 · 非 Superset/MLflow 服务端**。
- Contour：条形分桶；Quiver：点列/日计数；Vertex：表单登记 + 列表。

## 4. 验收

```text
GET /v1/analytics/contour/explore?objectType=WorkOrder
# → buckets 非空（有种子时）

GET /v1/analytics/quiver/series?objectType=WorkOrder
# → mode=ta8-quiver-subset · points 数组

POST /v1/analytics/vertex/experiments  → 201 · id
GET  /v1/analytics/vertex/experiments  → 含该 id

pytest tests/test_analytics_ta8_117.py -q
```

## 5. 下一刀

**阶段退出** ✅ [118](118-产品1.3分析建模阶段退出收口.md)；全集 BI/ML / 真 Jupyter / R 进停车场。

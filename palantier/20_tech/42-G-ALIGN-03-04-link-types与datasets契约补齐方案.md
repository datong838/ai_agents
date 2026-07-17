# 42 · G-ALIGN-03/04 link-types · datasets/syncs 契约补齐方案

> **版本**：v1.0 · 2026-07-17  
> **任务**：关闭 [31](31-波次交付结果台账.md) **G-ALIGN-03** · **G-ALIGN-04**  
> **对齐**：[T-API](T-API-aos-api稳定契约.md) §2.2 / §2.4 · [T06](T06-Ontology与Action-Function详细技术方案.md) · [T05](T05-L1数据集成详细技术方案.md)  
> **工程**：`aos-platform/services/aos-api`  
> **硬规则**：最小改动；邻接表 `graph_edge` 语义不变；写实例仍经 Action/Draft

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文通过后再改代码 |
| 最小更改 | Meta 增 `meta_link_type`；datasets/syncs 走内存 Facade，复用 sources/pipelines |
| 不影响已有 | neighbors / object-types / media / pipeline 行为不变 |

---

## 1. 未完成项盘点（本刀范围）

| ID | 状态 | 本刀 |
| --- | --- | --- |
| **G-ALIGN-03** `/v1/ontology/link-types` | ⚪ | **关闭** |
| **G-ALIGN-04** `/v1/datasets/*` · `/v1/syncs` | ⚪ | **关闭**（MVP Facade） |
| T-UI S2 业务深页 | ⚪ | **不做**（下一刀） |
| TX.2 指标 | ☐ | **不做**（后置） |
| TX.4 完整 Marking | 🔄 | **不做** |
| T0.9/T0.10 · T5.1 安装包 · T5.6 Ferry | ☐/⚠/⚪ | **不做**（阻塞/显式延期） |
| 真 Keycloak JWKS | B-TX3-01 | **不做** |

---

## 2. G-ALIGN-03 · Link Types

### 2.1 表

```sql
CREATE TABLE IF NOT EXISTS meta_link_type (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  src_type TEXT NOT NULL,
  dst_type TEXT NOT NULL,
  rel TEXT NOT NULL,
  cardinality TEXT NOT NULL DEFAULT 'MANY_TO_MANY',
  expected_edges BIGINT NOT NULL DEFAULT 0,
  mdo_approved BOOLEAN NOT NULL DEFAULT FALSE,
  published BOOLEAN NOT NULL DEFAULT FALSE,
  description TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

Seed（与现有边一致）：`related_to` · WorkOrder→WorkOrder · `expected_edges=1` · published。

### 2.2 API

| Method | Path | 行为 |
| --- | --- | --- |
| GET | `/v1/ontology/link-types` | 列表 |
| POST | `/v1/ontology/link-types` | 创建；规模门禁 |
| GET | `/v1/ontology/link-types/{id}` | 详情 |
| PUT | `/v1/ontology/link-types/{id}` | 更新（含规模门禁） |
| DELETE | `/v1/ontology/link-types/{id}` | 删元数据（**不**级联删 `graph_edge`） |

Body 字段：`id, name, srcType, dstType, rel, cardinality?, expectedEdges?, mdoApproved?, published?, description?`

### 2.3 解法 B 规模校验

若 `expectedEdges > 1_000_000` 且 `mdoApproved != true` → **422** `LINK_SCALE_BLOCKED`（T-API 错误码表）。

邻居查询仍用 `graph_edge`；LinkType 只描述「允许的边类型」，不强制实例边必须先登记（Dev 友好）；可选后续加硬校验。

---

## 3. G-ALIGN-04 · datasets · syncs

| Method | Path | 行为 |
| --- | --- | --- |
| GET/POST | `/v1/syncs` | 内存 Sync Job；绑 `sourceId`；POST 即 SUCCEEDED（Dev） |
| GET | `/v1/syncs/{id}` | 详情 |
| GET | `/v1/datasets` | 列表（内存注册 + 可由 pipeline 创建时写入） |
| GET | `/v1/datasets/{rid}` | 详情；缺失 404 |
| GET | `/v1/datasets/{rid}/history` | 版本/构建历史（pipeline builds 或 sync 记录） |

创建 pipeline 时若带 `datasetRid` 或默认 `ri.dataset.{pipelineId}`，写入 `_datasets`。

**非目标：** Iceberg 真湖、Airbyte 真 Sync、替换现有 sources/pipelines 路径。

---

## 4. 文件落点

| 路径 | 变更 |
| --- | --- |
| `aos_api/db.py` | `meta_link_type` + seed |
| `aos_api/routers/ontology.py` | link-types CRUD |
| `aos_api/routers/wave_ext.py` | syncs + datasets |
| `tests/test_align_link_datasets.py` | 新测 |
| `26` / `31` / `00` | 关闭 G-ALIGN-03/04 |

OpenAPI：若仓库内 yaml 尚无路径，本刀以 T-API 为准；可后补 yaml。

---

## 5. 自测

- [x] link-types CRUD + seed 可见
- [x] expectedEdges>1e6 无 mdo → LINK_SCALE_BLOCKED
- [x] syncs POST/GET
- [x] datasets GET + history
- [x] 既有 ontology pytest 不回归（`test_align_link_datasets` + `test_ontology` = 10 passed）

---

## 6. 风险

| 风险 | 缓解 |
| --- | --- |
| datasets 与 obj_instance 双真源 | 文档标明 Facade；rid 前缀 `ri.dataset.` |
| link 与边不同步 | MVP 不强制；neighbors 仍独立 |

---

*v1.0 · 关闭 G-ALIGN-03/04*

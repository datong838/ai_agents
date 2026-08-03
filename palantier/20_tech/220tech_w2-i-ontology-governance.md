# W2-I · Ontology 治理组微规格（#31 / #38 / #69）

> **版本**：v1.0 · 2026-07-22
> **所属 Wave**：W2+ 中优先级
> **关联差距**：#31 图谱健康度 / #38 Ontology 使用指标 / #69 Ontology 图查询
> **代码位置**：`aos-platform/services/aos-api/aos_api/`

---

## 1. 范围与目标

| 编号 | 差距项 | 当前状态 | 本批目标 | 优先级 |
|------|--------|----------|----------|--------|
| #31 | 图谱健康度 | 🟡 有基础（graph-health 端点已存在） | 确认并标记完成（dangling/conflict/orphan/score 已覆盖） | 中 |
| #38 | Ontology 使用指标 | 🔴 基础计数 | 新增 Reads/Writes/Active Users/使用来源 30 天指标 | 中 |
| #69 | Ontology 图查询 | 🟡 基础（1-hop neighbors） | 新增多跳 BFS + 最短路径查询 | 中 |

---

## 2. #31 图谱健康度 · 现状确认

### 2.1 现有端点

`GET /v1/ontology/graph-health` — `aos-platform/services/aos-api/aos_api/routers/ontology.py#L647-L799`

### 2.2 覆盖核对

| 差距项要求 | 现有实现 | 状态 |
|-----------|----------|------|
| 悬空 Link 检测 | `danglingEdges` — graph_edge 端点在 obj_instance 中不存在的边计数 | ✅ |
| 冲突检测 | `propConflicts` — 实例 props 含未声明属性键的冲突计数 + 采样 | ✅ |
| 僵尸检测 | `orphanInstances` — 无 graph_edge 关联的孤立实例计数 | ✅ |
| 健康评分 | `score` — 0-100 综合分（基于 dangling/conflict/orphan 加权） | ✅ |
| 问题列表 | `issues` — GH-01~GH-04 分级问题（bad/warn/info） | ✅ |
| 归档候选 | `archivePreview` — TTL 归档预览（来自 ttl_job） | ✅ |
| 基础指标 | `objectTypes / instances / edges` 计数 | ✅ |

**结论**：#31 图谱健康度已完整覆盖差距要求，本批直接标记为 ✅ 已完成，**零代码变更**。

---

## 3. #38 Ontology 使用指标 · 设计

### 3.1 数据模型

使用内存计数器 + 滑动窗口（30 天），按 Object Type / Link Type 维度聚合。

```python
class UsageMetric(BaseModel):
    """使用指标快照（30 天滑动窗口）"""
    reads: int = 0           # 读次数
    writes: int = 0          # 写次数
    interactions: int = 0    # 交互次数（Action 触发等）
    active_users: int = 0    # 活跃用户数（30 天去重）
    sources: dict[str, int] = Field(default_factory=dict)  # 使用来源：workshop/quiver/slate/api
    daily_series: list[dict[str, Any]] = Field(default_factory=list)  # 近 30 天趋势
```

### 3.2 使用来源归因规则

| 来源标记 | 触发条件 |
|----------|----------|
| `workshop` | Workshop 模块内请求 / `X-Aos-Source: workshop` header |
| `quiver` | 分析类 API / `X-Aos-Source: quiver` |
| `slate` | 文档类 API / `X-Aos-Source: slate` |
| `api` | 其他直接 API 调用（默认） |

### 3.3 指标记录点

- **Reads**：对象查询 / 邻居查询 / 搜索 等 GET 请求
- **Writes**：对象创建/更新/删除、Action 执行写回
- **Interactions**：Action 执行（含副作用触发）
- **Active Users**：按 user_id 每日去重计数

### 3.4 API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/ontology/usage` | 全局使用指标概览（30 天） |
| GET | `/v1/ontology/usage/object-types/{object_type}` | 指定 Object Type 的使用指标 |
| GET | `/v1/ontology/usage/link-types/{link_type}` | 指定 Link Type 的使用指标 |
| POST | `/v1/ontology/usage/record` | 手动上报指标事件（测试/外部系统用） |

### 3.5 响应示例

```json
{
  "objectType": "Employee",
  "reads": 12450,
  "writes": 832,
  "interactions": 1205,
  "activeUsers": 47,
  "sources": {
    "workshop": 8200,
    "quiver": 3100,
    "api": 1150
  },
  "dailySeries": [
    {"date": "2026-07-21", "reads": 520, "writes": 38, "activeUsers": 22}
  ],
  "windowDays": 30
}
```

---

## 4. #69 Ontology 图查询 · 设计

### 4.1 新增端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/objects/{object_type}/{object_id}/neighbors/{hops}` | 多跳邻居（BFS，hops=1~5） |
| POST | `/v1/ontology/graph/path` | 最短路径查询（两节点之间） |
| POST | `/v1/ontology/graph/expand` | 子图扩展（从种子节点向外展开 N 跳） |

### 4.2 多跳邻居（BFS）

**请求**：`GET /v1/objects/Employee/emp-001/neighbors/2?rel=reports_to&direction=out`

参数：
- `hops`: 1-5（限制最大深度，防爆炸）
- `rel`: 可选，指定关系类型过滤
- `direction`: `out` / `in` / `both`（默认 `out`）

**响应**：
```json
{
  "srcType": "Employee",
  "srcId": "emp-001",
  "hops": 2,
  "totalNodes": 15,
  "totalEdges": 18,
  "nodes": [
    {"type": "Employee", "id": "emp-002", "depth": 1},
    {"type": "Department", "id": "dept-eng", "depth": 2}
  ],
  "edges": [
    {"rel": "reports_to", "srcType": "Employee", "srcId": "emp-001",
     "dstType": "Employee", "dstId": "emp-002", "depth": 1}
  ]
}
```

### 4.3 最短路径

**请求**：
```json
{
  "srcType": "Employee",
  "srcId": "emp-001",
  "dstType": "Employee",
  "dstId": "emp-099",
  "maxHops": 6,
  "rels": ["reports_to", "works_with"]
}
```

**响应**：
```json
{
  "found": true,
  "distance": 3,
  "path": [
    {"type": "Employee", "id": "emp-001"},
    {"type": "Employee", "id": "emp-015", "rel": "reports_to"},
    {"type": "Department", "id": "dept-eng", "rel": "member_of"},
    {"type": "Employee", "id": "emp-099", "rel": "managed_by"}
  ],
  "explored": 42
}
```

### 4.4 子图扩展

**请求**：
```json
{
  "seeds": [
    {"type": "Employee", "id": "emp-001"}
  ],
  "hops": 2,
  "maxNodes": 200
}
```

### 4.5 安全限制

- 最大跳数：5（多跳邻居）/ 6（路径查询）
- 最大节点数：500（子图扩展）
- 超时：5 秒
- 关系过滤必须提供时深度可放宽

---

## 5. 实现计划

### 5.1 新增文件

| 文件 | 用途 |
|------|------|
| `aos_api/ontology_governance.py` | 核心引擎：UsageMetricsEngine + GraphQueryEngine |
| `aos_api/routers/ontology_governance.py` | API 路由：usage + graph query |
| `tests/test_ontology_governance.py` | 单元测试 |

### 5.2 修改文件

| 文件 | 修改内容 |
|------|----------|
| `aos_api/main.py` | 注册新路由 |
| `aos_api/routers/ontology.py` | （可选）将 graph-health 移入 governance 路由组 |

### 5.3 测试计划

| 测试类 | 用例数 | 覆盖点 |
|--------|--------|--------|
| #38 Usage Metrics | ~10 | record/read/write/interaction/active_users/sources/daily_series/per_otype |
| #69 Graph Query | ~10 | multi-hop BFS/path found/path not found/expand/limit/rel filter/direction |
| 合计 | ~20 | |

---

## 6. 风险与回退

| 风险 | 缓解措施 |
|------|----------|
| 图查询深搜性能 | 限制最大跳数 5-6 / 最大节点 500 / 关系过滤推荐 |
| 指标内存占用 | 30 天滑动窗口 + 每日聚合 + 计数器而非逐条存储 |
| 影响现有 graph-health | #31 零代码变更，仅标记完成 |

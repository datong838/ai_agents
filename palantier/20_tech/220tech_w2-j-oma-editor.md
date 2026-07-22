# W2-J · OMA 编辑器增强组微规格（#28 / #34 / #35）

> **版本**：v1.0 · 2026-07-22
> **所属 Wave**：W2+ 中优先级
> **关联差距**：#28 OMA Property Editor / #34 OMA Property 独立编辑器 / #35 Ontology Proposals 审查工作流
> **代码位置**：`aos-platform/services/aos-api/aos_api/`

---

## 1. 范围与目标

| 编号 | 差距项 | 当前状态 | 本批目标 | 优先级 |
|------|--------|----------|----------|--------|
| #28 | OMA Property Editor | 无 | backing column / title key / TSP / origin mapping | 中 |
| #34 | OMA Property 独立编辑器 | 行内编辑 | 独立 Property CRUD API + 丰富元数据字段 | 中 |
| #35 | Ontology Proposals 审查工作流 | 分支 CRUD | 提案→审查→批准→发布 PR 式协作 | 中 |

**设计原则**：#28 和 #34 高度重叠，合并为一个 Property Editor 实现。

---

## 2. #28+#34 Property Editor · 设计

### 2.1 数据模型

```python
class PropertyEditor(BaseModel):
    """独立属性编辑器模型 — 远离行内编辑，支持完整元数据。"""
    id: str                          # 属性 ID（唯一）
    object_type: str                 # 所属 Object Type
    name: str                        # 属性名
    display_name: str = ""           # 显示名
    description: str = ""            # 描述
    data_type: str = "string"        # 数据类型
    # ── #28 核心字段 ──
    backing_column: str = ""         # 映射到数据源列名
    backing_dataset: str = ""        # 映射到数据源 RID
    title_key: bool = False          # 是否为标题键（用于展示）
    is_tsp: bool = False             # 是否为 Time Series Property
    tsp_config: dict = {}            # TSP 配置（采样频率/聚合方式等）
    origin: str = "manual"           # 来源：manual / derived / imported / function
    origin_mapping: dict = {}        # 来源映射（Function ID / Pipeline 节点等）
    # ── 通用元数据 ──
    nullable: bool = True
    indexed: bool = False
    unique: bool = False
    default_value: Any = None
    validation_rules: list[dict] = []  # 校验规则
    tags: list[str] = []
    created_at: str
    updated_at: str
```

### 2.2 API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/oma/property-types` | 列出所有属性（可按 object_type 过滤） |
| GET | `/v1/oma/property-types/{property_id}` | 获取单个属性详情 |
| POST | `/v1/oma/property-types` | 创建属性 |
| PUT | `/v1/oma/property-types/{property_id}` | 更新属性 |
| DELETE | `/v1/oma/property-types/{property_id}` | 删除属性 |
| POST | `/v1/oma/property-types/{property_id}/promote-title-key` | 设为 title key |
| GET | `/v1/oma/object-types/{object_type}/title-key` | 获取当前 title key |

### 2.3 约束

- 同一 Object Type 下仅一个 title key
- backing_column + backing_dataset 唯一性校验
- TSP 属性的 data_type 必须为 `timeseries`

---

## 3. #35 Ontology Proposals 审查工作流 · 设计

### 3.1 状态机

```
DRAFT → PENDING_REVIEW → IN_REVIEW → APPROVED → PUBLISHED
                      ↘ REJECTED
                      ↘ WITHDRAWN
```

### 3.2 数据模型

```python
class Proposal(BaseModel):
    id: str
    title: str
    description: str = ""
    branch_id: str                   # 关联分支
    status: ProposalStatus           # draft/pending_review/in_review/approved/rejected/withdrawn/published
    author: str                      # 提交者
    reviewers: list[str] = []        # 审查者列表
    comments: list[ProposalComment] = []
    created_at: str
    updated_at: str
    submitted_at: str | None = None
    reviewed_at: str | None = None
    published_at: str | None = None
    summary: dict = {}               # 变更摘要（diff 统计）

class ProposalComment(BaseModel):
    author: str
    body: str
    action: str = "comment"          # comment/approve/reject/request_changes
    created_at: str
```

### 3.3 API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/ontology/proposals` | 列出提案（可按 status 过滤） |
| POST | `/v1/ontology/proposals` | 创建提案（关联分支） |
| GET | `/v1/ontology/proposals/{proposal_id}` | 获取提案详情 |
| POST | `/v1/ontology/proposals/{proposal_id}/submit` | 提交审查（DRAFT → PENDING_REVIEW） |
| POST | `/v1/ontology/proposals/{proposal_id}/start-review` | 开始审查（PENDING_REVIEW → IN_REVIEW） |
| POST | `/v1/ontology/proposals/{proposal_id}/approve` | 批准（IN_REVIEW → APPROVED） |
| POST | `/v1/ontology/proposals/{proposal_id}/reject` | 拒绝（IN_REVIEW → REJECTED） |
| POST | `/v1/ontology/proposals/{proposal_id}/withdraw` | 撤回（→ WITHDRAWN） |
| POST | `/v1/ontology/proposals/{proposal_id}/publish` | 发布（APPROVED → PUBLISHED，触发 merge） |
| POST | `/v1/ontology/proposals/{proposal_id}/comments` | 添加评论 |

### 3.4 状态转换规则

| 当前状态 | 允许的操作 | 目标状态 |
|----------|-----------|----------|
| DRAFT | submit | PENDING_REVIEW |
| DRAFT | withdraw | WITHDRAWN |
| PENDING_REVIEW | start_review | IN_REVIEW |
| PENDING_REVIEW | withdraw | WITHDRAWN |
| IN_REVIEW | approve | APPROVED |
| IN_REVIEW | reject | REJECTED |
| IN_REVIEW | withdraw | WITHDRAWN |
| APPROVED | publish | PUBLISHED |
| REJECTED | submit | PENDING_REVIEW |

---

## 4. 实现计划

### 4.1 新增文件

| 文件 | 用途 |
|------|------|
| `aos_api/oma_editor.py` | 核心引擎：PropertyEditorEngine + ProposalEngine |
| `aos_api/routers/oma_editor.py` | API 路由 |
| `tests/test_oma_editor.py` | 单元测试 |

### 4.2 修改文件

| 文件 | 修改内容 |
|------|----------|
| `aos_api/main.py` | 注册新路由 |

### 4.3 测试计划

| 测试类 | 用例数 | 覆盖点 |
|--------|--------|--------|
| Property Editor | ~10 | CRUD / backing_column / title_key 唯一 / TSP / origin |
| Proposals | ~12 | 创建/提交/审查/批准/拒绝/撤回/发布/评论/状态转换非法 |
| 合计 | ~22 | |

---

## 5. 风险与回退

| 风险 | 缓解措施 |
|------|----------|
| 影响 ObjectType 现有 properties 字段 | Property Editor 独立运行，不修改 meta_object_type 表 |
| 发布时 merge 失败 | publish 前检查 branch diff，失败返回错误不改变状态 |

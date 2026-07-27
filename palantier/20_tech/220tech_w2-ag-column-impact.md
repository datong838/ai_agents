# 220tech · W2-AG · 列级影响分析 + Data Connection 管理组（#109 / #114 / #115）

> **版本**：v1.0 · 2026-07-22
> **状态**：✅ 方案定稿 · 可编码
> **对齐**：
> - 差距分析 [220w](./220w-与目标系统差距分析.md) §11 #109/#114/#115
> - 220plan v4.5 已交付 82/166，本批收口 3 项 → 85/166
> **范围**：W2-AG 收口血缘增量与 DC 管理三件 — 列级影响分析（#109 增量补丁，CRUD 部分已在 W2-E #4 交付）+ Agent 管理 + 源探索
> **不替换底层**：本组纯新增；lineage_views.py 的 W2-E #4 列级血缘 CRUD 保持不变

---

## 0. 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文回答 | 文档与代码注释均中文 |
| 先方案后编码 | 本文先定稿，再写引擎/路由/测试 |
| 最小更改 | 仅新增 `aos_api/column_impact.py` + `aos_api/data_connection_admin.py` + 路由 + 测试；`main.py` 加 4 行 |
| 不影响已有功能 | 不修改 lineage_views.py；W2-E #4 CRUD 保持原样 |
| 自测验证 | 单测全绿 + 全量回归 + 方案对照 |
| 编码前复习方案 | 已核对 W2-AE/W2-AF 引擎模式（单例 + 200 条 FIFO） |

---

## 1. 背景与边界

### 1.1 现状

| 能力 | 现状 | 缺口 |
| --- | --- | --- |
| 列级影响分析 | W2-E #4 已交付列级血缘 CRUD（set/get），无递归影响分析 | 🔴 缺 |
| Agent 管理 | W2-AF #112/#113 已交付 Proxy/Worker，无统一管理面（注册/下载/日志/驱动/证书/升级） | 🔴 缺 |
| 源探索 | 无 ER 关系图/资源树/样本预览 | 🔴 缺 |

### 1.2 边界

- ✅ 本组做：
  - #109 列级影响分析：新增 ColumnImpactEngine（不动 W2-E #4 已有 CRUD），register/list/analyze_impact（基于规则做下游传播）
  - #114 Agent 管理：AgentAdminEngine register/heartbeat/push_log/upgrade/list_drivers/list_certificates/get_download_url
  - #115 源探索：SourceExplorerEngine register/explore_er/explore_resource_tree/preview_sample
- ❌ 本组不做：
  - 修改 W2-E #4 的 lineage_views.py（保持原样）
  - 真实数据库 ER 元数据抓取（explore_er 返回模板结构）
  - 实际驱动安装/证书签发（仅记录元数据）

---

## 2. 数据模型

### 2.1 #109 ColumnImpactRule

```python
class ColumnImpactRule(BaseModel):
    """列级影响规则（来源 → 下游列表）。"""
    id: str
    source_dataset_rid: str
    source_column: str
    downstream_datasets: list[str] = []     # 受影响的下游 dataset RID 列表
    downstream_columns: list[str] = []      # 受影响的下游列名（带 dataset 前缀 "ds.col"）
    transform_expr: str = ""                # 变换表达式（可选）
    created_at: float = 0.0


class ImpactResult(BaseModel):
    """影响分析结果。"""
    source_dataset_rid: str
    source_column: str
    impacted_datasets: list[str] = []
    impacted_columns: list[str] = []
    depth: int = 0
    analyzed_at: float = 0.0
```

### 2.2 #114 AgentAdmin

```python
class AgentDriver(BaseModel):
    """驱动元数据。"""
    name: str
    version: str
    type: str                 # jdbc / odbc / python / generic


class AgentCertificate(BaseModel):
    """证书元数据。"""
    id: str
    name: str
    issuer: str = ""
    expires_at: float = 0.0


class AgentLogEntry(BaseModel):
    """Agent 日志条目。"""
    timestamp: float
    level: str                # info / warn / error
    message: str


class AgentAdmin(BaseModel):
    """Data Connection Agent 管理记录。"""
    id: str
    agent_id: str
    name: str
    version: str = "1.0.0"
    status: str = "registered"        # registered / active / deprecated
    download_url: str = ""
    drivers: list[AgentDriver] = []
    certificates: list[AgentCertificate] = []
    logs: list[AgentLogEntry] = []
    auto_upgrade: bool = False
    last_heartbeat: float = 0.0
    created_at: float = 0.0


_VALID_ADMIN_STATUSES = {"registered", "active", "deprecated"}
_VALID_DRIVER_TYPES = {"jdbc", "odbc", "python", "generic"}
_VALID_LOG_LEVELS = {"info", "warn", "error"}
```

### 2.3 #115 SourceSchema

```python
class ERRelation(BaseModel):
    """ER 关系。"""
    from_table: str
    to_table: str
    from_column: str
    to_column: str
    relation_type: str = "many_to_one"   # one_to_one / one_to_many / many_to_one / many_to_many


class ResourceNode(BaseModel):
    """资源树节点。"""
    name: str
    type: str                             # database / schema / table / column
    children: list[str] = []              # 子节点名（简化）


class SourceSchema(BaseModel):
    """数据源 schema 探索记录。"""
    id: str
    source_id: str
    dataset_name: str
    er_diagram: list[ERRelation] = []
    resource_tree: list[ResourceNode] = []
    sample_preview: list[dict[str, Any]] = []
    created_at: float = 0.0


_VALID_RELATION_TYPES = {"one_to_one", "one_to_many", "many_to_one", "many_to_many"}
_VALID_RESOURCE_TYPES = {"database", "schema", "table", "column"}
```

---

## 3. 引擎设计

文件：`aos_api/column_impact.py` + `aos_api/data_connection_admin.py`（新增，3 个引擎）

### 3.1 ColumnImpactEngine（#109）

```python
class ColumnImpactEngine:
    def register(self, rule: ColumnImpactRule) -> ColumnImpactRule: ...
    def get(self, rule_id: str) -> ColumnImpactRule: ...
    def list(self, source_dataset_rid: str | None = None) -> list[ColumnImpactRule]: ...
    def delete(self, rule_id: str) -> bool: ...
    def analyze_impact(self, source_dataset_rid: str, source_column: str) -> ImpactResult: ...
    """递归查找所有下游影响（基于 register 的规则图）"""
```

**analyze_impact 流程**：
1. 取 source (dataset, column)
2. BFS：从 source 出发，找所有 source_dataset_rid=当前 dataset 且 source_column=当前 column 的规则
3. 收集 downstream_datasets + downstream_columns
4. 推进到下游，循环（防环路：visited set）
5. 返回 ImpactResult

### 3.2 AgentAdminEngine（#114）

```python
class AgentAdminEngine:
    def register(self, admin: AgentAdmin) -> AgentAdmin: ...
    def get(self, admin_id: str) -> AgentAdmin: ...
    def list(self, agent_id: str | None = None, status: str | None = None) -> list[AgentAdmin]: ...
    def update(self, admin_id: str, updates: dict[str, Any]) -> AgentAdmin: ...
    def delete(self, admin_id: str) -> bool: ...
    def heartbeat(self, admin_id: str) -> AgentAdmin: ...
    def push_log(self, admin_id: str, level: str, message: str) -> AgentAdmin: ...
    """追加 AgentLogEntry，200 条 log 滚动"""
    def upgrade(self, admin_id: str, new_version: str) -> AgentAdmin: ...
    """推进 version + status=active"""
    def list_drivers(self, admin_id: str) -> list[AgentDriver]: ...
    def list_certificates(self, admin_id: str) -> list[AgentCertificate]: ...
    def get_download_url(self, admin_id: str) -> str: ...
    """返回 download_url，校验 status≠deprecated 否则抛 AGENT_DEPRECATED"""
```

### 3.3 SourceExplorerEngine（#115）

```python
class SourceExplorerEngine:
    def register(self, schema: SourceSchema) -> SourceSchema: ...
    def get(self, schema_id: str) -> SourceSchema: ...
    def list(self, source_id: str | None = None) -> list[SourceSchema]: ...
    def update(self, schema_id: str, updates: dict[str, Any]) -> SourceSchema: ...
    def delete(self, schema_id: str) -> bool: ...
    def explore_er(self, schema_id: str) -> list[ERRelation]: ...
    """返回 ER 关系图"""
    def explore_resource_tree(self, schema_id: str) -> list[ResourceNode]: ...
    """返回资源树"""
    def preview_sample(self, schema_id: str, limit: int = 10) -> list[dict[str, Any]]: ...
    """返回样本预览（前 limit 条）"""
```

### 3.4 单例与持久化

- 3 个引擎均用**双重检查锁单例**
- 内存态为主，各 200 条上限（admin logs 200 条滚动）

---

## 4. API 设计

文件：`aos_api/routers/column_impact.py` + `aos_api/routers/data_connection_admin.py`（新增）

### 4.1 #109 Column Impact

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/column-impact/rules` | 注册规则 |
| GET | `/v1/column-impact/rules` | 列表 |
| GET | `/v1/column-impact/rules/{rule_id}` | 单条 |
| DELETE | `/v1/column-impact/rules/{rule_id}` | 删除 |
| POST | `/v1/column-impact/analyze` | 影响分析 |

### 4.2 #114 Agent Admin

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/agent-admins` | 注册 Agent 管理 |
| GET | `/v1/agent-admins` | 列表 |
| GET | `/v1/agent-admins/{admin_id}` | 单条 |
| PUT | `/v1/agent-admins/{admin_id}` | 更新 |
| DELETE | `/v1/agent-admins/{admin_id}` | 删除 |
| POST | `/v1/agent-admins/{admin_id}/heartbeat` | 心跳 |
| POST | `/v1/agent-admins/{admin_id}/logs` | 推送日志 |
| POST | `/v1/agent-admins/{admin_id}/upgrade` | 升级版本 |
| GET | `/v1/agent-admins/{admin_id}/drivers` | 驱动列表 |
| GET | `/v1/agent-admins/{admin_id}/certificates` | 证书列表 |
| GET | `/v1/agent-admins/{admin_id}/download-url` | 下载链接 |

### 4.3 #115 Source Explorer

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/source-explorer/schemas` | 注册 schema |
| GET | `/v1/source-explorer/schemas` | 列表 |
| GET | `/v1/source-explorer/schemas/{schema_id}` | 单条 |
| PUT | `/v1/source-explorer/schemas/{schema_id}` | 更新 |
| DELETE | `/v1/source-explorer/schemas/{schema_id}` | 删除 |
| GET | `/v1/source-explorer/schemas/{schema_id}/er` | ER 关系图 |
| GET | `/v1/source-explorer/schemas/{schema_id}/resource-tree` | 资源树 |
| GET | `/v1/source-explorer/schemas/{schema_id}/sample` | 样本预览 |

---

## 5. 集成点

### 5.1 main.py（最小更改）

```python
from aos_api.routers import (..., column_impact, data_connection_admin, ...)
application.include_router(column_impact.router)
application.include_router(data_connection_admin.router)
```

---

## 6. 测试计划

文件：`tests/test_column_impact.py` + `tests/test_data_connection_admin.py`（新增，约 45 个用例）

### 6.1 ColumnImpactEngine（13）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 缺 source_dataset | MISSING_SOURCE_DATASET |
| 3 | register 缺 source_column | MISSING_SOURCE_COLUMN |
| 4 | get 未找到 | NOT_FOUND |
| 5 | list 默认 | 列表 |
| 6 | list 按 source_dataset 过滤 | 仅匹配 |
| 7 | delete | 删除成功 |
| 8 | analyze_impact 单层 | impacted_datasets 1 项 |
| 9 | analyze_impact 多层 | impacted_datasets 2 项 |
| 10 | analyze_impact 环路 | 不无限递归 |
| 11 | analyze_impact 无规则 | impacted_datasets 为空 |
| 12 | analyze_impact 同列多规则 | 全部下游收集 |
| 13 | 200 条规则上限 | 旧记录淘汰 |

### 6.2 AgentAdminEngine（17）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 缺 agent_id | MISSING_AGENT |
| 3 | register 缺 name | MISSING_NAME |
| 4 | register 未知 driver type | INVALID_DRIVER_TYPE |
| 5 | get 未找到 | NOT_FOUND |
| 6 | list 默认 | 列表 |
| 7 | list 按 agent_id 过滤 | 仅匹配 |
| 8 | list 按 status 过滤 | 仅匹配 |
| 9 | update | 修改后返回新值 |
| 10 | delete | 删除成功 |
| 11 | heartbeat | last_heartbeat 推进 |
| 12 | push_log | logs 增长 |
| 13 | push_log 200 条滚动 | 旧日志淘汰 |
| 14 | push_log 未知 level | INVALID_LOG_LEVEL |
| 15 | upgrade | version 推进 + status=active |
| 16 | list_drivers | 返回驱动列表 |
| 17 | get_download_url deprecated | AGENT_DEPRECATED |

### 6.3 SourceExplorerEngine（13）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 缺 source_id | MISSING_SOURCE |
| 3 | register 缺 dataset_name | MISSING_DATASET_NAME |
| 4 | register 未知 relation_type | INVALID_RELATION_TYPE |
| 5 | register 未知 resource type | INVALID_RESOURCE_TYPE |
| 6 | get 未找到 | NOT_FOUND |
| 7 | list 默认 | 列表 |
| 8 | list 按 source_id 过滤 | 仅匹配 |
| 9 | update | 修改后返回新值 |
| 10 | delete | 删除成功 |
| 11 | explore_er | 返回 ER 关系列表 |
| 12 | explore_resource_tree | 返回资源树 |
| 13 | preview_sample limit | 返回前 N 条 |

### 6.4 单例（3）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | impact 单例 | 同一实例 |
| 2 | admin 单例 | 同一实例 |
| 3 | explorer 单例 | 同一实例 |

---

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 影响分析死循环 | visited set 防环路 |
| Agent 日志膨胀 | 200 条滚动上限 |
| deprecated Agent 误用 | get_download_url 校验 status |
| ER 关系类型错误 | register 校验 INVALID_RELATION_TYPE |
| 资源树节点类型错误 | register 校验 INVALID_RESOURCE_TYPE |

---

## 8. 交付物清单

| 路径 | 状态 | 说明 |
| --- | --- | --- |
| `docs/palantier/20_tech/220tech_w2-ag-column-impact.md` | ✅ 本文件 | 微规约 |
| `aos_api/column_impact.py` | ⬜ 待编码 | ColumnImpactEngine |
| `aos_api/data_connection_admin.py` | ⬜ 待编码 | AgentAdminEngine + SourceExplorerEngine |
| `aos_api/routers/column_impact.py` | ⬜ 待编码 | 5 端点 |
| `aos_api/routers/data_connection_admin.py` | ⬜ 待编码 | ~19 端点 |
| `tests/test_column_impact.py` | ⬜ 待编码 | ~13 用例 |
| `tests/test_data_connection_admin.py` | ⬜ 待编码 | ~30 用例 |
| `aos_api/main.py` | ⬜ +4 行 | 2 import + 2 include_router |

---

*v1.0 · w2-ag*

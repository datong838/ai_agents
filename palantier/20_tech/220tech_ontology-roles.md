# 220tech · W1-17 Ontology 角色体系

> **版本**：v1.0 · 2026-07-22
> **关联**：220plan §1.2.2 W1-17 · Phase 3 · 高优先级
> **依赖**：无（独立权限模块）；后续 W1-18 / ShellCore 可查询权限
> **范围**：四级角色（Owner/Editor/Viewer/Discoverer）+ 元数据与数据权限分离 + 对象类型级授权

---

## 1. 目标与差距

| 维度 | 当前 | 目标 |
| --- | --- | --- |
| 角色模型 | 无 | 四级：Owner / Editor / Viewer / Discoverer |
| 权限粒度 | 无 | 元数据（schema/字段）vs 数据（记录）分离 |
| 授权对象 | 无 | 对象类型（object_type）级别，支持多 principal |
| 权限查询 | 无 | check_permission(object_type, principal, permission) |

## 2. 四级角色 × 六种权限矩阵

| 角色 | READ_META | WRITE_META | READ_DATA | WRITE_DATA | DELETE_DATA | ADMIN |
| --- | --- | --- | --- | --- | --- | --- |
| **OWNER** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **EDITOR** | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| **VIEWER** | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ |
| **DISCOVERER** | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |

**设计要点**：
- Discoverer 只能看到对象类型存在（READ_META），看不到具体数据
- Viewer 能读数据但不能改
- Editor 能改数据但不能删/管理
- Owner 全权（含授权管理 ADMIN）

## 3. 数据模型

```python
class Role(str, Enum):
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"
    DISCOVERER = "discoverer"

class Permission(str, Enum):
    READ_META = "read_meta"
    WRITE_META = "write_meta"
    READ_DATA = "read_data"
    WRITE_DATA = "write_data"
    DELETE_DATA = "delete_data"
    ADMIN = "admin"

class RoleAssignment(BaseModel):
    object_type: str
    principal: str            # user:xxx 或 group:xxx
    role: Role
    granted_at: str
    granted_by: str = ""
```

## 4. OntologyRoleStore

```python
class OntologyRoleStore:
    def assign(self, object_type, principal, role, granted_by="") -> RoleAssignment
    def revoke(self, object_type, principal) -> None
    def get_roles(self, object_type) -> list[RoleAssignment]
    def get_assignments_for(self, principal) -> list[RoleAssignment]
    def check_permission(self, object_type, principal, permission) -> bool
    def list_principals(self, object_type) -> dict[str, str]   # principal -> role
```

### 4.1 权限解析算法

```
1. 查 (object_type, principal) 的 role；不存在 → False
2. 查 ROLE_PERMISSIONS[role] 是否含 permission；含 → True
3. 否则 → False
```

### 4.2 重复 assign 语义

- 同一 (object_type, principal) 再次 assign → 更新 role（upsert）
- revoke 不存在的 assignment → 静默成功（幂等）

## 5. REST API

> 命名空间 `/v1/ontology/roles`（与 actions/types 等区分）。

| 方法 | 路径 | 功能 |
| --- | --- | --- |
| POST | `/v1/ontology/roles/assign` | 授权（body: {object_type, principal, role, granted_by}） |
| DELETE | `/v1/ontology/roles/assign` | 撤权（query: object_type, principal） |
| GET | `/v1/ontology/roles/{object_type}` | 列出该对象类型所有授权 |
| POST | `/v1/ontology/roles/check` | 校验权限（body: {object_type, principal, permission}） |
| GET | `/v1/ontology/roles/permissions` | 列出所有可用权限 |
| GET | `/v1/ontology/roles/principals/{principal}` | 列出 principal 的所有授权 |

## 6. 测试用例（≥ 16）

### 6.1 引擎（≥ 10）

1. assign + get_roles
2. assign 重复 → upsert 更新 role
3. revoke 已存在
4. revoke 不存在 → 幂等无错
5. check_permission owner → 所有权限 True
6. check_permission editor → DELETE_DATA False, WRITE_DATA True
7. check_permission viewer → WRITE_META False, READ_DATA True
8. check_permission discoverer → READ_DATA False, READ_META True
9. check_permission 未授权 → False
10. list_principals
11. get_assignments_for(principal)
12. 非法 role → BAD_ROLE

### 6.2 API（≥ 6）

13. POST /assign
14. DELETE /assign
15. GET /{object_type}
16. POST /check（owner 全 True）
17. GET /permissions
18. GET /principals/{principal}
19. POST /check（未授权 False）

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 群组继承 | 本期仅支持 user:xxx，群组在 Phase 6 |
| 权限缓存 | 本期内存直查；Phase 6 加 LRU |
| 跨对象类型泄漏 | check 必须带 object_type，不全局查询 |
| 并发 assign | threading.Lock 保护 dict |

## 8. 文件清单

| 路径 | 类型 | 说明 |
| --- | --- | --- |
| `aos_api/ontology_roles.py` | 新增 | Role/Permission/RoleAssignment + OntologyRoleStore |
| `aos_api/routers/ontology_roles.py` | 新增 | 6 个 REST 端点 |
| `aos_api/main.py` | 修改 | 注册 router |
| `tests/test_ontology_roles.py` | 新增 | 19 个测试 |

## 9. 不做的事

- ❌ 群组/角色继承（Phase 6）
- ❌ ABAC（属性级权限，Phase 6）
- ❌ 权限缓存（Phase 6）
- ❌ 集成到现有 actions/ontology 路由的鉴权中间件（Phase 6 渐进式接入）

# 61 · OpenFGA 生产模型扩展（org / project / editor·owner / marking）

> **版本**：v1.0 · 2026-07-17  
> **任务**：台账下一刀 #1 — OpenFGA 生产模型扩展  
> **对齐**：[55](55-TX.4-Marking继承与OpenFGA-Facade方案.md) · [58](58-OpenFGA真边车Dev方案.md) · [T-CROSS](T-CROSS-横切能力详细技术方案.md) §2 · [60](60-生产IdP联调手册.md)（org/project claims）  
> **工程**：`deploy/dev/openfga/model.json` · `aos_api/openfga.py` · `routers/authz.py` · bootstrap/probe · 单测  
> **硬规则**：前端不直连 OpenFGA；Markings 集合判定 **不删**；无元组对象仍不拦；旧 `viewer` 种子兼容

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文后改 |
| 最小更改 | 扩模型 + Facade 目录/校验 + 本地 read 蕴含；不改 UI |
| 不影响主路径 | 无 authz 元组时行为不变；Marking 继承不变 |
| 诚实 | 「生产模型」= 对齐 T-CROSS 的 type/relation 真源；**非** OpenFGA 集群 HA |

---

## 1. 目标 / 非目标

| 目标（DoD） | 非目标 |
| --- | --- |
| 模型含 `organization` · `project` · `object`(viewer/editor/owner) · `marking` | 替换 Markings 引擎 |
| `viewer` ← `editor` ← `owner`（远程 computed；本地 OR 蕴含） | UI 策略编辑器 · Expand API |
| `GET /v1/authz/model` 返回 type/relation 目录 | 强制全对象上元组 |
| bootstrap 多种子 + relation 白名单写校验 | 生产多区域 HA |
| 单测绿；probe 未起仍 SKIP | JWT 自动写 org 元组（现场联调另刀） |

---

## 2. 模型（DSL 真源 → JSON）

```
type user

type organization
  relations
    define member: [user]

type project
  relations
    define parent: [organization]
    define member: [user] or member from parent

type object
  relations
    define owner: [user]
    define editor: [user] or owner
    define viewer: [user] or editor

type marking
  relations
    define bearer: [user]
```

**对象键约定（保持 [55]/[58]）：**

| OpenFGA object | 示例 |
| --- | --- |
| `object:{Type}:{id}` | `object:WorkOrder:wo-fga-demo` |
| `organization:{org_id}` | `organization:dev-org` |
| `project:{project_id}` | `project:dev-project` |
| `marking:{label}` | `marking:restricted` |

**种子（bootstrap + 本地可选）：**

| 元组 | 用途 |
| --- | --- |
| `user:secret-user#viewer@object:WorkOrder:wo-fga-demo` | 兼容旧测 |
| `user:secret-user#member@organization:dev-org` | org |
| `organization:dev-org#parent@project:dev-project` | project←org |
| `user:secret-user#bearer@marking:restricted` | marking 关系化（演示；读路径仍走 Markings） |

---

## 3. Facade 行为

| 项 | 行为 |
| --- | --- |
| Check | 不变；relation 可为 viewer/editor/owner/member/parent/bearer |
| Write | relation **白名单**；未知 → `400 AUTHZ_RELATION_UNKNOWN` |
| `ensure_object_viewer` | 远程：Check `viewer`（computed 含 editor/owner）；本地：viewer\|\|editor\|\|owner |
| `GET /v1/authz/model` | 静态目录（与 model.json 对齐） |
| `GET /v1/authz/status` | 增 `modelVersion=aos-prod-v1` · `types=[…]` |
| Markings | **不变**；bearer 元组仅供 Check 演示 / 后续组合 |

**兼容：** 仅有旧 viewer 元组 → 仍过；仅有 editor/owner 无 viewer → 本地/远程读均过。

---

## 4. 落点

| 路径 | 变更 |
| --- | --- |
| `docs/.../61-*.md` | 本文 |
| `deploy/dev/openfga/model.json` | 生产形模型 |
| `deploy/dev/openfga/model.fga` | DSL 可读副本 |
| `aos_api/openfga.py` | 键助手 · 白名单 · read 蕴含 · model catalog |
| `routers/authz.py` | `/v1/authz/model` · write 校验 |
| `bootstrap-openfga.ps1` | 多种子 |
| `openapi/v1.yaml` | model path |
| 单测 | `test_openfga_model.py` |
| 26/31/00/27 | 回写 |

---

## 5. 自测

- [x] `pytest tests/test_openfga_model.py tests/test_openfga_remote.py tests/test_marking_inherit_openfga.py` 绿（17）  
- [x] model.json 含 organization/project/marking + editor/owner  
- [x] `GET /v1/authz/model` 200（client 测）  
- [x] 未知 relation 写元组 → 400  
- [x] 与 [55]/[58]/T-CROSS 交叉一致  
- [x] probe 未起 SKIP

---

## 6. 风险

| 风险 | 缓解 |
| --- | --- |
| 已 bootstrap 的旧 store 模型过时 | 重新跑 bootstrap（新建 store）或现场 WriteAuthorizationModel |
| 本地无 computed | Facade OR 蕴含；文档写明 |
| parent 元组 user 形态 | 用 `organization:…` 非 `user:…` |

---

*v1.0*

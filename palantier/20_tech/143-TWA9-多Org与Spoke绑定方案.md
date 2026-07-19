# 143 · TWA.9 多 Org / Hub+Spoke 绑定

> **版本**：v1.0.1 · 2026-07-19  
> **状态**：✅ 方案定稿 · ✅ 已编码 · ✅ 已自测  
> **对齐**：[20a](20a-多用户与工作区整站隔离方案.md) P3 · [T09](T09-Apollo交付引擎详细技术方案.md) T09-G2 · [26 §14 TWA.9](26-AOS目标态开发计划.md)

## 1. 目标（DoD）

| 项 | 验收 |
| --- | --- |
| Org 列表 | `GET /v1/orgs` 仅返回主体有成员资格的组织 |
| Org 切换 | `POST /v1/orgs/{id}/enter` → 返回默认工作区；无成员 → 403 |
| `/v1/me` | 含 `orgs[]` · `orgName` |
| Spoke 绑 Org | `apollo_spoke.org_id`；`GET /v1/apollo/spokes` **按当前 Org 过滤**；跨 Org 直链 → 404 |
| Web | 顶栏「组织」切换器（单 Org 可折叠/仍显示当前名） |
| 话术 | UI 称「组织」；不与 Marking 混谈 |

## 2. 非目标

- SaaS 开通台 / 配额（→ **TWB.6**）  
- Ferry 气隙端版本矩阵（→ **TWB.7**）  
- Full Spoke 运行时、Realm/IdP 多 Realm 真对接  

## 3. 落点

| 路径 | 改动 |
| --- | --- |
| `aos_api/orgs.py` | Org 目录 + 主体可见性 |
| `aos_api/routers/orgs.py` | list / enter |
| `aos_api/routers/me.py` | 扩展 orgs |
| `aos_api/apollo_catalog.py` | spoke.org_id · list/get 过滤 |
| `apps/web/.../OrgSwitcher.tsx` | 组织切换 |
| `tests/test_twa9_orgs.py` | 无 PG 单测 |

## 4. 控制面 vs 数据面

- **Channel 目录**（晋升轨）本刀仍可 Org 共享（Hub 控制面）  
- **Spoke 实例**属数据面 → **必须**绑 `org_id`，列表不串租  

## 5. 自测

```bash
pytest tests/test_twa9_orgs.py -q
```

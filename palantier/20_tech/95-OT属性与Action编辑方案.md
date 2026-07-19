# 95 · Object Type 属性编辑 · Action Type 轻量编辑

> **版本**：v1.0 · 2026-07-19  
> **状态**：✅ 已落地  
> **上游**：[94](94-本体下一刀方案.md)  
> **Rules**：保存即真持久化 · Constitution lint 守 publish · 最小更改

---

## 1. 范围

| # | 能力 | 做法 |
| --- | --- | --- |
| **A** | OT 元数据更新 | `PUT /v1/ontology/object-types/{id}`（name/desc/properties/publish） |
| **B** | Properties Tab 可编辑 | 增删改属性行 → PUT；publish 时 lint |
| **C** | Action Type 编辑器 | `GET/PUT /v1/actions/types/{id}` + `/ontology/action-types/:id` |
| **D** | 索引修订记录 | `00` 补 88–95 / v1.0.64 |

非目标：删 OT 级联 · Action 参数可视化设计器 · Wiki PUT。

---

## 2. 契约

```json
PUT /v1/ontology/object-types/{id}
{ "name", "description", "properties": [{"name","type"}], "publish": false }
→ 同 POST；publish=true 时 lint 失败 422

GET /v1/actions/types/{id}
PUT /v1/actions/types/{id}  // body = ActionTypeIn，id 须匹配
```

---

## 3. 文件

| 路径 | 变更 |
| --- | --- |
| `ontology.py` | PUT object-types |
| `actions.py` | GET/PUT by id |
| `objectTypeDetail.tsx` | Properties 编辑 |
| `ObjectTypeDetailPage.tsx` | 刷新 meta |
| `ActionTypeEditorPage.tsx` + routes | C |
| `00-技术方案索引.md` | D |
| 本文 | 登记 |

---

## 4. 自测

1. PUT OT properties → GET 列表已变 ✅  
2. publish+空 properties → 422 ✅  
3. Action 编辑 name 保存 → 列表可见 ✅  
4. Properties Tab 增一行保存成功（UI 接 PUT；API 已测）  

pytest：`tests/test_ontology.py` · `tests/test_actions.py` → **9 passed**

---

## 5. 风险

| 风险 | 处理 |
| --- | --- |
| 改掉 PK 属性名 | UI 提示首行常为 PK；不强制 |
| Action 改 objectType | 允许，诚实提示影响 Draft |


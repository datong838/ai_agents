# 99 · Action 模板插件化（对齐 20 §3.1）

> **版本**：v1.0 · 2026-07-19  
> **状态**：✅ 已落地 · 自测通过  
> **上游**：[98](98-插件化剩余域收口方案.md) · [20 §3.1](20-AOS整体技术方案.md) · T06  
> **Rules**：种子不写死在 SQL · 运行时仍走 `meta_action_type` · 最小更改

---

## 1. 问题

`actions.py` 把 `CloseWorkOrder` / `UpdateWikiCard` **硬编码 INSERT**；§3.1 要求 Action 类型模板可横向扩展。

## 2. 目标

| 项 | 做法 |
| --- | --- |
| 落点 | `plugins/actions/<id>/manifest.json` |
| 种子 | `ensure_action_schema` 从已装插件 upsert，删硬编码 VALUES |
| API | `GET /v1/action-plugins` · install→写入 DB |
| 兼容 | 既有 `/v1/actions/types` CRUD / validate 不变 |

非目标：Function 执行器插件 · 删 OT 级联 · 改 UpdateWikiCard 运行时分支。

## 3. 首批

| id | 默认已装 |
| --- | --- |
| `CloseWorkOrder` | ✅ |
| `UpdateWikiCard` | ✅ |
| `AssignWorkOrder` | stub 可装（仅模板，无特殊 runtime） |

## 4. 自测

1. GET action-plugins ≥2 · required 已装 ✅  
2. 空库启动后 types 仍有 CloseWorkOrder（来自插件种子） ✅  
3. install AssignWorkOrder → types 列表可见 ✅  
4. validate CloseWorkOrder 仍 200/400 如常 ✅  

pytest：`test_action_plugins_99` + `test_actions` + `test_wave3_drafts` + `test_pluginization_98` → **16 passed**

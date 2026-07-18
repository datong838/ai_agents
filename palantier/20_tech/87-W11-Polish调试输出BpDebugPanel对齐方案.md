# 87 · W11 Polish · 调试输出 BpDebugPanel 对齐方案

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[84](84-蓝图与实现全面审计台账.md) P2 收口 · [86](86-P2尾项DiscoverCard与Draft-Logic对齐方案.md)  
> **规则**：禁 JSON 主面板 · JSON 仅 `<details>` 折叠

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 UI |
| 先方案后编码 | 本文 → 组件 + 页 |
| 最小更改 | 新增 `BpDebugPanel` 复用，不改 API |
| 禁 JSON 主面板 | 主区 PropGrid；完整 JSON 折叠 |

---

## 1. 范围

| 项 | 文件 | 落地 |
| --- | --- | --- |
| `BpDebugPanel` + `flattenRecordProps` | `blueprintUi.tsx` | 可复用调试面板 |
| `JsonBlock` 升级 | `shared.tsx` | 自动惠及 data/lineage |
| Capability  invoke 结果 | `CapabilityPage.tsx` | BpDebugPanel |
| Tools / ModelRouter 试聊 | `s2/aip.tsx` | BpDebugPanel |
| Apollo Release 操作 | `remainder.tsx` | action/upgrade PropGrid |
| Studio toolCalls | `StudioPage.tsx` | BpTable + 折叠 JSON |

---

## 2. 验收

1. 上述页主区无裸露 `<pre>` JSON ✅  
2. `npm test` 绿 ✅  

---

*v1.0*

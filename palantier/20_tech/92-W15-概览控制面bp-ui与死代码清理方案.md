# 92 · W15 概览控制面 bp-ui 对齐与死代码清理方案

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[79](79-W5概览与AIP-Draft-Lineage蓝图对齐方案.md) · [91](91-W14-Workshop运行态链路与Apollo延后方案.md)  
> **约束**：Apollo 不深化 · 概览**无**业务主链区块（用户要求）

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 UI |
| 20_tech 约束 | 仅改 web 展示层 |
| 最小更改 | 删未引用组件 · 控制面换 bp-ui |
| Apollo 延后 | 四域 Apollo 面板仅导航 |

---

## 1. 范围

| 项 | 动作 |
| --- | --- |
| 业务主链区块 | 已从概览移除（用户） |
| `StoryChainPanel.tsx` | 删除（无引用） |
| 控制面 `panel/tile-grid` | → `BpDomainPanel` + `BpMetricGrid` + `BpIndexTile` |

---

## 2. 验收

1. `/` 无业务主链 section ✅  
2. 控制面风格与四域 grid 一致 ✅  
3. `npm test` 绿 ✅  

---

*v1.0*

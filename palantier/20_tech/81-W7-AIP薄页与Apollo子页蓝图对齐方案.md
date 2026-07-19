# 81 · W7 AIP 薄页与 Apollo 子页蓝图对齐方案

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[78](78-蓝图页面对齐差距台账与去演示Hub方案.md) §6 P2  
> **蓝图**：`aip-tools` · `aip-maturity` · `aip-evals` · `apollo-spoke` · `apollo-config` · `apollo-assets`

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| 最小 API | 复用 `/v1/aip/tools` · `/v1/aip/evals*` · `/v1/apollo/*` |
| 禁 JSON 主面板 | 主区卡片/表格/指标；invoke 结果可折叠 |
| 诚实 | Full Spoke 运行时仍标注延期 |

---

## 1. 范围

| 页 | 路径 | 落地 |
| --- | --- | --- |
| 工具面板 | `/aip/tools` | 三栏目录/已启用/细项 + invoke |
| 成熟度 | `/aip/maturity` | L1～L4 楼梯 + Evals 状态条 |
| Evals | `/aip/evals` | 指标卡 + 门控表 + 放行/阻断 |
| Spoke | `/apollo/spoke` | 出站 banner + 形态 + 目录表 |
| Config | `/apollo/config` | 维护窗 + Vault ref 表 |
| Assets | `/apollo/assets` | 资产包表 + 打包结果 |
| Release/Ferry | `/apollo/release` · `/apollo/ferry` | Hub 指标卡替 JSON 主面板 |

---

## 2. 验收

1. 上述路径主区无大块 `JsonBlock` ✅  
2. API 真值驱动 gate/spoke/tools ✅  
3. `npm test` 绿 ✅  

---

*v1.0*

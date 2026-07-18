# 85 · P1 数据 + Workshop/Studio 蓝图对齐方案

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[84](84-蓝图与实现全面审计台账.md) §7 P1/P2  
> **蓝图**：`source-new` · `source-detail` · `schedules` · `pipeline-proposals` · `workshop` · `agents` · `aip-model-providers`

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 UI |
| 先方案后编码 | 本文 → 改页 |
| 最小更改 | 复用 `/v1/sources` · schedules · pipelines |
| 禁 JSON 主面板 | ToolCalls 等折叠 |

---

## 1. 范围

| 页 | 路径 | 落地 |
| --- | --- | --- |
| 数据连接 | `/data` | Tab：Hub / 新建 Source / Source 详情 |
| 计划编辑器 | `/data/schedules` | Cron 预设 + Tab + 表格 |
| 管道提案 | `/data/pipeline-proposals` | 待审/历史 Tab + 提案卡 |
| 应用列表 | `/workshop` | Module 卡片 grid |
| Chatbot Studio | `/aip/studio` | Prompt 面板 + 试聊 |
| 模型供应商 | `/aip/model-providers` | 卡片 + 接入表单区 |

---

## 2. 验收

1. P1 三页主区 bp-ui ✅  
2. P2 三页布局对齐蓝图 ✅  
3. `npm test` 绿 ✅  

---

*v1.0*

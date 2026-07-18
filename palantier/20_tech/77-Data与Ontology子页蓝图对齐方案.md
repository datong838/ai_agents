# 77 · Data / Ontology 子页蓝图对齐方案

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 方案 · **本波落地**  
> **蓝图真源**：`docs/palantier/foundry/html/`（DEMO_PAGES 侧栏映射页）  
> **工程**：`aos-platform/apps/web/src/pages/s2/`  
> **硬规则**：布局/区块/链接语义跟蓝图 HTML；**禁止**纯 JSON 面板替代 UI

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 不偏离蓝图 | 每页对照同名 `.html` 区块顺序 |
| 先方案后编码 | 本文 |
| 最小 API 改动 | 复用已有 `/v1/*`；缺字段用 API 真值 + 蓝图占位文案 |
| 迭代升级 | D1 JSON → D2 卡片/表格/分栏 |

---

## 1. Ontology 子页（5）

| 蓝图 | 路径 | 布局要点 | API |
| --- | --- | --- | --- |
| ontology-graph-health | `/ontology/graph-health` | GH 指标卡 + 问题列表 + Draft/Funnel 链 | `GET /v1/ontology/graph-health` |
| ontology-funnel | `/ontology/funnel` | 四阶段纵向流水线 + Live/Replacement + 错误区 | `GET /v1/funnel/WorkOrder/status` · `.../worker` |
| ontology-wiki | `/ontology/wiki` | Tab + 左 Object 属性 / 右 Wiki 卡片 | `GET /v1/wiki/WorkOrder/wo-1001` · `GET /v1/objects/...` |
| ontology-branches | `/ontology/branches` | 分支表格 + 警告条 | `GET /v1/ontology/branches` |
| okf-funnel / funnel | `/ontology/okf-funnel` | 行业选择 + 映射表 + Lint | `GET /v1/funnel/...` · `POST constitution/lint` |

---

## 2. Data 子页（10）

| 蓝图 | 路径 | 布局要点 | API |
| --- | --- | --- | --- |
| media-sets | `/data/media-sets` | 列表卡 + 上传解析 | `GET/POST /v1/media-sets` · parsers |
| pipeline-list | `/data/pipelines` | 左项目树 + 管道卡片 | `GET /v1/pipelines` |
| pipeline-proposals | `/data/pipeline-proposals` | 提案列表 + 新建 | `POST/GET /v1/pipelines` |
| schedules | `/data/schedules` | 表单 + 列表（74 已有，保留） | schedules CRUD |
| builds | `/data/builds` | 左 Build 列表 + 右任务/日志 | `GET /v1/builds` |
| dataset | `/data/datasets` | Tab 预览/历史 + 统计卡 + 表 | `GET /v1/datasets` · history |
| code-repositories | `/data/code-repos` | 仓库表格 | `GET /v1/code-repos` |
| lineage | `/data/lineage` | Dataset→Sync 沿袭链 | datasets history + syncs |
| health | `/data/health` | L1 汇总卡 + 检查表 + 链到图谱健康 | object-store/mysql probe + dlq |
| data-connection-agents | `/data/agents` | 左代理列表 + 右详情 | `GET /v1/edge/agents/local` |

---

## 3. 实现落点

| 文件 | 职责 |
| --- | --- |
| `s2/blueprintUi.tsx` | Tab / 指标卡 / 阶段流水线 / 分栏 / 表格 |
| `s2/ontology.tsx` | 5 个 ontology 深页 |
| `s2/data.tsx` | 10 个 data 深页 |
| `s2/remainder.tsx` | okf-funnel / proposals / code-repos / lineage 加深 |
| `styles.css` | `.bp-*` 蓝图视觉辅助类 |

---

## 4. 验收

1. 打开上述路径 **无大块 JSON**（仅详情/调试可折叠）  
2. 区块标题/链路与蓝图 HTML 一致  
3. `npm test` 绿 · API 掉线时有 76 中文提示  

---

## 5. 完成勾选

| 域 | 页 | 状态 |
| --- | --- | --- |
| Ontology | graph-health / funnel / wiki / branches / okf-funnel | ✅ |
| Data | media / pipelines / proposals / schedules / builds / datasets / code-repos / lineage / health / agents | ✅ |

---

## 变更日志

| 版本 | 说明 |
| --- | --- |
| v1.0 | 15 子页蓝图 D2 落地 |

*77 · 严格跟 foundry/html · 子页 D2 化*
